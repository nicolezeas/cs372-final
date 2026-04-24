from __future__ import annotations

import argparse
from dataclasses import dataclass

from src.conversation.memory import ConversationMemory
from src.conversation.state_tracker import UserCaseState
from src.data.chunk import chunk_documents
from src.data.clean import clean_documents
from src.data.collect import load_documents
from src.generation.answer_generator import AnswerGenerator
from src.prompting.templates import build_grounded_prompt
from src.retrieval.hybrid import HybridRetriever
from src.safety.guardrails import detect_unsafe_request, low_support_response


@dataclass
class RetrievalRun:
    prompt: str
    results: list[dict]
    state: UserCaseState
    memory: ConversationMemory


class LexAINCSession:
    def __init__(self) -> None:
        documents = clean_documents(load_documents())
        chunks = chunk_documents(documents)
        self.retriever = HybridRetriever(chunks)
        self.memory = ConversationMemory()
        self.state = UserCaseState()

    def build_contextual_query(self, user_question: str) -> str:
        recent_user_messages = self.memory.recent_user_messages(max_messages=3)
        base_parts: list[str] = []

        for message in recent_user_messages:
            if message not in base_parts:
                base_parts.append(message)

        if self.state.county and all(self.state.county.lower() not in part.lower() for part in base_parts):
            base_parts.append(f"County: {self.state.county}")
        if self.state.issue_category and all(self.state.issue_category.lower() not in part.lower() for part in base_parts):
            base_parts.append(f"Issue: {self.state.issue_category}")
        for key, value in self.state.facts.items():
            fact_line = f"{key.replace('_', ' ')}: {value}"
            if fact_line not in base_parts:
                base_parts.append(fact_line)

        return "\n".join(base_parts) if base_parts else user_question

    def run_retrieval(self, user_question: str) -> RetrievalRun | str:
        self.state.infer_from_text(user_question)
        self.memory.add_turn("user", user_question)

        if detect_unsafe_request(user_question):
            return "This request is outside the tool's safe-use boundaries."

        retrieval_query = self.build_contextual_query(user_question)
        results = self.retriever.search(retrieval_query, top_k=5)

        if not results:
            return low_support_response()

        prompt = build_grounded_prompt(
            user_question=user_question,
            retrieved_context=results,
            memory=self.memory,
            state=self.state,
        )
        return RetrievalRun(
            prompt=prompt,
            results=results,
            state=self.state,
            memory=self.memory,
        )


def run_retrieval(user_question: str) -> RetrievalRun | str:
    session = LexAINCSession()
    return session.run_retrieval(user_question)


def build_demo_prompt(user_question: str) -> str:
    run = run_retrieval(user_question)
    if isinstance(run, str):
        return run
    return run.prompt


def build_retrieval_report(user_question: str) -> str:
    run = run_retrieval(user_question)
    if isinstance(run, str):
        return run

    lines = [
        f"Question: {user_question}",
        "",
        f"Tracked state: {run.state.summary()}",
        "",
        f"Retrieved {len(run.results)} source chunks.",
        "",
        "Top results:",
    ]

    for idx, result in enumerate(run.results, start=1):
        chunk = result["chunk"]
        score = result.get("score", 0.0)
        methods = ", ".join(result.get("methods", []))
        snippet = " ".join(chunk.text.split()[:45]).strip()
        if len(chunk.text.split()) > 45:
            snippet += " ..."
        lines.extend(
            [
                f"{idx}. {chunk.title}",
                f"   URL: {chunk.source_url}",
                f"   Issue category: {chunk.issue_category}",
                f"   Issue tags: {', '.join(getattr(chunk, 'issue_tags', [])) or chunk.issue_category}",
                f"   Methods: {methods or 'unknown'}",
                f"   Score: {score:.3f}",
                f"   Snippet: {snippet}",
                "",
            ]
        )

    lines.extend(
        [
            "Grounded prompt preview:",
            run.prompt,
        ]
    )
    return "\n".join(lines)


def answer_question(user_question: str) -> str:
    run = run_retrieval(user_question)

    if isinstance(run, str):
        return run

    prompt = run.prompt

    try:
        generator = AnswerGenerator()
        return generator.generate(prompt)
    except Exception as exc:
        return (
            "Generation failed after retrieval.\n\n"
            f"Reason: {exc}\n\n"
            "If your Gemini setup is not ready yet, run the same command with "
            "--prompt-only to inspect retrieval and prompting."
        )


def chat_loop(retrieval_only: bool = True) -> None:
    session = LexAINCSession()
    print("HomeHelp NC chat mode. Type 'exit' to quit.")
    print("This mode keeps conversation history and tracked user state across turns.\n")

    while True:
        try:
            user_question = input("You: ").strip()
        except EOFError:
            print()
            break

        if not user_question:
            continue
        if user_question.lower() in {"exit", "quit"}:
            break

        run = session.run_retrieval(user_question)
        if isinstance(run, str):
            print(f"\nAssistant:\n{run}\n")
            session.memory.add_turn("assistant", run)
            continue

        if retrieval_only:
            report_lines = [
                "Assistant (retrieval-only mode):",
                f"Tracked state: {run.state.summary()}",
                "Top sources:",
            ]
            for idx, result in enumerate(run.results[:3], start=1):
                chunk = result["chunk"]
                snippet = " ".join(chunk.text.split()[:35]).strip()
                if len(chunk.text.split()) > 35:
                    snippet += " ..."
                report_lines.extend(
                    [
                        f"{idx}. {chunk.title}",
                        f"   URL: {chunk.source_url}",
                        f"   Snippet: {snippet}",
                    ]
                )
            reply = "\n".join(report_lines)
        else:
            try:
                generator = AnswerGenerator()
                reply = generator.generate(run.prompt)
            except Exception as exc:
                reply = (
                    "Generation failed after retrieval.\n\n"
                    f"Reason: {exc}\n\n"
                    "You can still use --retrieval-only or --chat for multi-turn retrieval debugging."
                )

        print(f"\n{reply}\n")
        session.memory.add_turn("assistant", reply)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the HomeHelp NC retrieval and answer flow.")
    parser.add_argument(
        "--question",
        default="My landlord changed my locks in Durham after I asked for repairs.",
        help="Question to run through the current retrieval pipeline.",
    )
    parser.add_argument(
        "--prompt-only",
        action="store_true",
        help="Print the grounded prompt instead of generating an answer.",
    )
    parser.add_argument(
        "--retrieval-only",
        action="store_true",
        help="Print a retrieval report with top sources and the prompt preview.",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Start a multi-turn CLI chat loop with full answers and preserved memory/state.",
    )
    parser.add_argument(
        "--chat-retrieval-only",
        action="store_true",
        help="Start a multi-turn CLI chat loop that shows retrieval debugging instead of full answers.",
    )
    args = parser.parse_args()
    if args.chat:
        chat_loop(retrieval_only=False)
    elif args.chat_retrieval_only:
        chat_loop(retrieval_only=True)
    elif args.retrieval_only:
        print(build_retrieval_report(args.question))
    elif args.prompt_only:
        print(build_demo_prompt(args.question))
    else:
        print(answer_question(args.question))
