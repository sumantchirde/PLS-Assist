# test_agent.py
import uuid
from agent.graph import run_agent

thread = str(uuid.uuid4())

tests = [
    "What are the path coefficients in the model?",           # → get_model_statistics
    "What threshold should AVE exceed for convergent validity?", # → search_plssem_docs
    "Is the AVE acceptable for all constructs?",              # → both tools
    "Which construct has the weakest R² and what does that mean for the business?",
]

for q in tests:
    print(f"\nQ: {q}")
    result = run_agent(q, thread_id=thread)
    print(f"   Tools used : {result['tool_calls']}")
    print(f"   Answer     : {result['answer'][:300]}")
    print("=" * 60)