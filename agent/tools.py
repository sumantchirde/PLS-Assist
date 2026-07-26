# agent/tools.py
import os, json
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from retriever import load_vector_store, build_retriever

load_dotenv()

# Anchor to project root (one level up from agent/)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Resolve STATS_PATH relative to project root if it's a relative path
_raw_stats_path = os.getenv("STATS_PATH", "./model_stats.json")
STATS_PATH = (
    Path(_raw_stats_path)
    if Path(_raw_stats_path).is_absolute()
    else PROJECT_ROOT / _raw_stats_path.lstrip("./")
)

print(f"[tools.py] STATS_PATH resolved to: {STATS_PATH}")  # remove after confirming

# Initialise once at import time — not on every tool call
_vectorstore = load_vector_store()
_retriever   = build_retriever(_vectorstore)

@tool
def search_plssem_docs(query: str) -> str:
    """Search the PLS-SEM methodology knowledge base.
    Use this for questions about how to interpret loadings, path coefficients,
    R-squared, AVE, composite reliability, HTMT, discriminant validity,
    bootstrapping, or any PLS-SEM concept or guideline.
    Input should be a clear natural-language question."""
    docs = _retriever.invoke(query)
    if not docs:
        return "No relevant methodology documentation found for that query."

    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "unknown")
        formatted.append(f"[{i}] ({source})\n{doc.page_content.strip()}")

    return "\n\n".join(formatted)

# agent/tools.py (continued)

STATS_PATH = os.getenv("STATS_PATH", "../model_stats.json")

@tool
def get_model_statistics(aspect: str = "all") -> str:
    """Retrieve PLS-SEM model results estimated from the uploaded dataset.
    Use this for questions about THIS model's specific numbers:
    path coefficients, outer loadings, R-squared, AVE, composite reliability,
    Cronbach alpha, HTMT ratios, or bootstrapped confidence intervals.

    The 'aspect' argument can be: 'all', 'paths', 'loadings',
    'reliability', 'validity', 'model_fit', or 'constructs'.
    """
    print(f"DEBUG — looking for stats at: {os.path.abspath(STATS_PATH)}")
    print(f"DEBUG — file exists: {os.path.exists(STATS_PATH)}")
    if not os.path.exists(STATS_PATH):
        return (
            "No model has been estimated yet. "
            "Please upload a dataset and run the PLS-SEM model first."
        )
    with open(STATS_PATH, "r") as f:
        stats = json.load(f)

    if aspect == "all" or aspect not in stats:
        return json.dumps(stats, indent=2)
    return json.dumps({aspect: stats[aspect]}, indent=2)