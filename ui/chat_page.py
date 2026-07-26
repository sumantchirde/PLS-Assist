# ui/chat_page.py
import streamlit as st
import uuid
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from agent.graph import run_agent, agent_graph


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

TOOL_LABELS = {
    "get_model_statistics": "📊 Model Statistics",
    "search_plssem_docs":   "📚 PLS-SEM Knowledge Base",
}

SUGGESTED_QUESTIONS = [
    "Are the path coefficients statistically significant?",
    "Is the AVE acceptable for all constructs?",
    "How do I interpret the R² values in my model?",
    "What does the HTMT ratio tell us about discriminant validity?",
    "Which construct has the weakest explanatory power and why?",
    "Are the bootstrapped confidence intervals supporting my hypotheses?",
]

# ui/chat_page.py (continued)

def section_not_ready():
    """Shown when no model has been estimated yet."""
    st.header("💬 PLS-Assist Chatbot")
    st.warning(
        "No model has been estimated yet. "
        "Go to the **Model Setup** tab, upload your dataset, "
        "define your constructs and paths, then run the model."
    )
    st.image(
        "https://img.icons8.com/fluency/96/bar-chart.png",
        width=80
    )
    st.caption(
        "Once the model is ready, come back here to ask business "
        "questions about your PLS-SEM results."
    )

# ui/chat_page.py (continued)

def ensure_thread_id():
    """Create a thread ID once per session and store in session state."""
    if st.session_state["chat_thread_id"] is None:
        st.session_state["chat_thread_id"] = str(uuid.uuid4())

# ui/chat_page.py (continued)

def render_chat_history():
    """Replay all past messages from session state into the chat UI."""
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show tool badges under assistant messages
            if message["role"] == "assistant" and message.get("tools_used"):
                render_tool_badges(message["tools_used"])


def render_tool_badges(tools_used: list[str]):
    """Render small pill badges showing which tools the agent called."""
    if not tools_used:
        return
    cols = st.columns(len(tools_used))
    for col, tool_name in zip(cols, tools_used):
        label = TOOL_LABELS.get(tool_name, tool_name)
        col.markdown(
            f"<span style='"
            f"background:#1e3a5f; color:#93c5fd; font-size:11px; "
            f"padding:3px 10px; border-radius:20px; "
            f"display:inline-block; margin-top:6px;'>"
            f"{label}</span>",
            unsafe_allow_html=True
        )

# ui/chat_page.py (continued)

def stream_agent_response(user_message: str):
    """
    Call the LangGraph agent with streaming, render tokens live,
    then store the completed message in chat_history.
    """
    thread_id = st.session_state["chat_thread_id"]

    # Store user message immediately
    st.session_state["chat_history"].append({
        "role":       "user",
        "content":    user_message,
        "tools_used": []
    })

    # Render user message
    with st.chat_message("user"):
        st.markdown(user_message)

    # Stream assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        tool_placeholder     = st.empty()

        accumulated_text = ""
        tools_used       = []

        try:
            from langchain_core.messages import HumanMessage, AIMessageChunk

            config = {"configurable": {"thread_id": thread_id}}
            inputs = {"messages": [HumanMessage(content=user_message)]}

            # stream_mode="messages" yields (message_chunk, metadata) tuples
            for chunk, metadata in agent_graph.stream(
                inputs,
                config=config,
                stream_mode="messages"
            ):
                # Collect tool call names from ToolMessage metadata
                if hasattr(chunk, "name") and chunk.name in TOOL_LABELS:
                    if chunk.name not in tools_used:
                        tools_used.append(chunk.name)
                        # Update tool badge while streaming
                        with tool_placeholder:
                            render_tool_badges(tools_used)

                # Stream text tokens from AIMessageChunk
                if (isinstance(chunk, AIMessageChunk)
                        and chunk.content
                        and not getattr(chunk, "tool_calls", None)):
                    accumulated_text += chunk.content
                    response_placeholder.markdown(accumulated_text + "▌")

            # Final render without cursor
            response_placeholder.markdown(accumulated_text)
            with tool_placeholder:
                render_tool_badges(tools_used)

        except Exception as e:
            error_msg = f"Agent error: {str(e)}"
            response_placeholder.error(error_msg)
            accumulated_text = error_msg

    # Store completed assistant message in session state
    st.session_state["chat_history"].append({
        "role":       "assistant",
        "content":    accumulated_text,
        "tools_used": tools_used
    })

# ui/chat_page.py (continued)

def section_suggested_questions():
    """Show suggested question buttons when chat is empty."""
    if st.session_state["chat_history"]:
        return  # Only show when no messages yet

    st.caption("Not sure where to start? Try one of these:")
    cols = st.columns(2)
    for i, question in enumerate(SUGGESTED_QUESTIONS):
        col = cols[i % 2]
        if col.button(question, key=f"suggested_{i}", use_container_width=True):
            stream_agent_response(question)
            st.rerun()

# ui/chat_page.py (continued)

# REPLACE the entire section_sidebar() function with this:
def section_sidebar():
    with st.sidebar:
        st.header("💬 Chat Controls")

        if st.button("🗑 Clear chat history", use_container_width=True):
            st.session_state["chat_history"]   = []
            st.session_state["chat_thread_id"] = str(uuid.uuid4())
            st.rerun()

        n_messages = len(st.session_state["chat_history"])
        if n_messages:
            st.caption(f"{n_messages} message{'s' if n_messages != 1 else ''} in this session")

# ui/chat_page.py (continued)

def show():
    """Main entry point called from app.py."""
    # Always initialise state (in case user lands on chat tab first)
    from ui.upload_page import init_session_state
    init_session_state()

    # Block access if model not ready
    if not st.session_state["run_complete"]:
        section_not_ready()
        return

    ensure_thread_id()
    section_sidebar()

    # ── Main chat area ────────────────────────────────────────────────────────
    st.header("💬 PLS-Assist Chatbot")
    st.caption(
        "Ask business questions about your PLS-SEM model results. "
        "The agent has access to your model statistics and PLS-SEM methodology docs."
    )
    st.divider()

    # Render persisted history
    render_chat_history()

    # Suggested questions (only when chat is empty)
    section_suggested_questions()

    # ── Chat input ────────────────────────────────────────────────────────────
    user_input = st.chat_input(
        "Ask about your model results… e.g. 'Is the path from Satisfaction to Loyalty significant?'"
    )

    if user_input:
        stream_agent_response(user_input)
        st.rerun()