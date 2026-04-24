from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.generation.answer_generator import AnswerGenerator
from src.main import LexAINCSession, build_demo_prompt


EXAMPLE_QUESTIONS = [
    "Can my landlord lock me out without a court order in North Carolina?",
    "How many days do I have to appeal an eviction in NC?",
    "When does a landlord have to return a security deposit in North Carolina?",
    "Can a landlord shut off utilities if I do not pay?",
]


st.set_page_config(page_title="HomeHelp NC", page_icon="NC", layout="wide")


def get_session() -> LexAINCSession:
    if "homehelp_session" not in st.session_state:
        st.session_state.homehelp_session = LexAINCSession()
    return st.session_state.homehelp_session


def reset_session() -> None:
    st.session_state.homehelp_session = LexAINCSession()
    st.session_state.pending_example = ""


def render_sources(results: list[dict]) -> None:
    st.subheader("Retrieved Sources")
    for idx, item in enumerate(results, start=1):
        chunk = item["chunk"]
        methods = ", ".join(item.get("methods", []))
        snippet_words = chunk.text.split()[:90]
        snippet = " ".join(snippet_words)
        if len(chunk.text.split()) > 90:
            snippet += " ..."
        with st.expander(f"{idx}. {chunk.title}"):
            st.write(f"**URL:** {chunk.source_url}")
            st.write(f"**Issue category:** {chunk.issue_category}")
            st.write(f"**Methods:** {methods or 'unknown'}")
            st.write(f"**Score:** {item.get('score', 0.0):.3f}")
            st.write(snippet)


def render_state(session: LexAINCSession) -> None:
    st.subheader("Tracked State")
    st.json(
        {
            "county": session.state.county,
            "issue_category": session.state.issue_category,
            "urgency": session.state.urgency_level,
            "written_lease": session.state.has_written_lease,
            "facts": session.state.facts,
        }
    )


def generate_reply(run) -> str:
    try:
        generator = AnswerGenerator()
        return generator.generate(run.prompt)
    except Exception as exc:
        return (
            "Generation failed after retrieval.\n\n"
            f"Reason: {exc}\n\n"
            "You can still use retrieval or prompt inspection mode while finishing local setup."
        )


st.title("HomeHelp NC")
st.caption("North Carolina housing legal information assistant")

with st.sidebar:
    st.header("Controls")
    mode = st.radio(
        "Response mode",
        ["Full Answer", "Retrieval Debug", "Prompt Preview"],
        index=0,
    )
    if st.button("Start New Conversation", use_container_width=True):
        reset_session()
        st.rerun()

    st.markdown("### Example Questions")
    for example in EXAMPLE_QUESTIONS:
        if st.button(example, key=f"example::{example}", use_container_width=True):
            st.session_state.pending_example = example
            st.rerun()

session = get_session()
st.session_state.setdefault("pending_example", "")

st.markdown("### Conversation")
st.write(
    "Ask a housing question below. This chat keeps conversation history and tracked case facts across turns."
)

for turn in session.memory.turns:
    with st.chat_message("user" if turn.role == "user" else "assistant"):
        st.markdown(turn.content)

user_input = st.chat_input("Describe your housing problem")
pending_example = st.session_state.get("pending_example", "")

current_input = user_input or pending_example
if current_input:
    st.session_state.pending_example = ""
    with st.chat_message("user"):
        st.markdown(current_input)

    with st.spinner("Retrieving relevant North Carolina sources..."):
        run = session.run_retrieval(current_input)

    if isinstance(run, str):
        reply = run
        with st.chat_message("assistant"):
            st.warning(reply)
        session.memory.add_turn("assistant", reply)
    else:
        if mode == "Full Answer":
            with st.spinner("Generating grounded answer..."):
                reply = generate_reply(run)
            with st.chat_message("assistant"):
                st.markdown(reply)
                render_state(session)
                render_sources(run.results)
            session.memory.add_turn("assistant", reply)
        elif mode == "Retrieval Debug":
            reply = f"Tracked state: {run.state.summary()}"
            with st.chat_message("assistant"):
                st.info(reply)
                render_state(session)
                render_sources(run.results)
            session.memory.add_turn("assistant", reply)
        else:
            prompt = build_demo_prompt(current_input)
            reply = "Prompt preview generated."
            with st.chat_message("assistant"):
                st.code(prompt)
                render_state(session)
                render_sources(run.results)
            session.memory.add_turn("assistant", reply)

if not session.memory.turns:
    st.info("Try one of the example questions from the sidebar, or type your own question below.")
