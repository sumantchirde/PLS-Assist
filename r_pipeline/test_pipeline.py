# test_pipeline.py
from runner import run_plssem_pipeline

# Load mobi CSV as bytes (simulating st.file_uploader)
with open("/tmp/mobi_test.csv", "rb") as f:
    csv_bytes = f.read()

constructs = [
    {"name": "Expectation",  "type": "reflective", "indicators": ["CUEX1","CUEX2","CUEX3"]},
    {"name": "Quality",      "type": "reflective", "indicators": ["PERQ1","PERQ2","PERQ3","PERQ4","PERQ5","PERQ6","PERQ7"]},
    {"name": "Satisfaction", "type": "reflective", "indicators": ["CUSA1","CUSA2","CUSA3"]},
    {"name": "Loyalty",      "type": "reflective", "indicators": ["CUSL1","CUSL2","CUSL3"]},
]
paths = [
    {"from": "Expectation",  "to": "Quality"},
    {"from": "Expectation",  "to": "Satisfaction"},
    {"from": "Quality",      "to": "Satisfaction"},
    {"from": "Satisfaction", "to": "Loyalty"},
]

stats = run_plssem_pipeline(csv_bytes, constructs, paths)

print("Metadata:", stats["metadata"])
print("Reliability keys:", list(stats["reliability"].keys()))
print("Path keys:", list(stats["bootstrapped_paths"].keys()))
print("R²:", stats["r_squared"])
print("\nPhase 1 pipeline working correctly.")