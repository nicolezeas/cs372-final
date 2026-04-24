from __future__ import annotations

from src.conversation.memory import ConversationMemory
from src.conversation.state_tracker import UserCaseState
from src.prompting.fewshot import FEW_SHOT_EXAMPLES


def build_fewshot_block() -> str:
    lines = ["Few-shot style guidance:"]
    for idx, example in enumerate(FEW_SHOT_EXAMPLES, start=1):
        lines.extend(
            [
                f"Example {idx} question: {example['question']}",
                f"Example {idx} answer style: {example['answer_style']}",
            ]
        )
    return "\n".join(lines)


def build_grounded_prompt(
    user_question: str,
    retrieved_context: list[dict],
    memory: ConversationMemory,
    state: UserCaseState,
) -> str:
    context_text = "\n\n".join(
        f"Source: {item['chunk'].title}\nURL: {item['chunk'].source_url}\nText: {item['chunk'].text}"
        for item in retrieved_context
    )
    history_text = "\n".join(
        f"{turn.role}: {turn.content}" for turn in memory.recent_history()
    )
    facts_text = "\n".join(
        f"- {key}: {value}" for key, value in state.facts.items()
    ) or "- none recorded"
    fewshot_text = build_fewshot_block()

    return f"""
You are HomeHelp NC, a legal information assistant for low-income North Carolina tenants.
You are not a lawyer and must not present your answer as legal advice.
Use only the retrieved sources when making factual claims.
If the sources are insufficient, say that clearly and suggest legal aid or court help resources.

Known user state:
- County: {state.county}
- Issue category: {state.issue_category}
- Urgency: {state.urgency_level}

Known user facts:
{facts_text}

{fewshot_text}

Recent conversation:
{history_text}

Retrieved context:
{context_text}

User question:
{user_question}

Write a response with these sections:
1. Short answer
2. What the NC sources suggest
3. What facts matter
4. Next steps
5. Disclaimer

In the Disclaimer section, refer to the assistant as "HomeHelp NC".
""".strip()
