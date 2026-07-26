# agent/graph.py
import os
from dotenv import load_dotenv
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,
    streaming=True
)

# agent/graph.py (continued)

SYSTEM_PROMPT = """You are PLS-Assist, an AI agent that helps business users
understand the results of a PLS-SEM model estimated using the seminr R package.

You have access to two tools:
1. get_model_statistics — retrieves the actual numerical results from the model
   estimated on the uploaded dataset.
2. search_plssem_docs — searches a knowledge base of PLS-SEM methodology
   documents to explain statistical concepts and interpretation guidelines.

The model_stats.json file has these sections:
- metadata: n_obs, n_constructs, n_paths, seminr_version
- constructs: construct names, types, and indicator lists
- loadings: outer loadings for each indicator
- reliability: cronbach_alpha, composite_reliability (rhoC), AVE, rho_A per construct
- validity.htmt: HTMT ratios between construct pairs
- validity.fornell_larcker: Fornell-Larcker criterion matrix
- paths: raw path coefficients from the structural model
- bootstrapped_paths: ALWAYS USE THIS for significance — contains original
  coefficient, bootstrap_mean, t_stat, p_value, ci_lower, ci_upper per path
- r_squared: R² for each endogenous construct
- f_squared: Cohen's f² effect sizes
- q_squared: Stone-Geisser Q² predictive relevance

Your behaviour rules:
- For ANY question about path significance, p-values, t-statistics, or
  confidence intervals: call get_model_statistics(aspect='bootstrapped_paths').
- For reliability or validity questions: call get_model_statistics(aspect='reliability')
  or get_model_statistics(aspect='validity').
- For R², f², Q²: call get_model_statistics with the relevant aspect key.
- When in doubt: call get_model_statistics(aspect='all') to get everything.
- For methodology questions (what thresholds mean, how to interpret):
  call search_plssem_docs.
- For most business questions, use BOTH tools: get the numbers first,
  then get methodology context to interpret them correctly.
- Translate statistical results into plain business language.
- Never invent numbers. If a statistic is not in the model output, say so
  AND suggest the user re-run the model if data appears missing.
- Never attempt to access the raw dataset. You only have aggregate statistics.
- Keep answers concise. Use bullet points for multi-part answers."""

# agent/graph.py (continued)
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from agent.tools import get_model_statistics, search_plssem_docs

def build_agent():
    tools       = [get_model_statistics, search_plssem_docs]
    checkpointer = MemorySaver()

    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer,
        prompt=SystemMessage(content=SYSTEM_PROMPT),
    )
    return agent

# Singleton — built once, reused across all Streamlit reruns
agent_graph = build_agent()

# agent/graph.py (continued)
from langchain_core.messages import HumanMessage

def run_agent(user_message: str, thread_id: str) -> dict:
    """
    Run the agent for one user message within a conversation thread.
    Returns the final answer and which tools were called (for UI display).
    """
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [HumanMessage(content=user_message)]}

    tool_calls_made = []
    final_answer    = ""

    for chunk in agent_graph.stream(inputs, config=config, stream_mode="values"):
        for msg in chunk.get("messages", []):
            # Capture tool names for transparency panel in UI
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_made.append(tc["name"])
            # Last AIMessage with content and no pending tool calls = final answer
            if (hasattr(msg, "content") and msg.content
                    and not getattr(msg, "tool_calls", None)):
                final_answer = msg.content

    return {
        "answer":     final_answer,
        "tool_calls": list(dict.fromkeys(tool_calls_made))  # deduplicated, order preserved
    }