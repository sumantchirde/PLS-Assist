# r_pipeline/runner.py
import os
import json
import uuid
import tempfile
import subprocess
from pathlib import Path


RSCRIPT_PATH = os.getenv("RSCRIPT_PATH", "Rscript")   # add to .env if non-default
R_SCRIPT     = Path(__file__).parent / "run_model.R"
STATS_PATH   = os.getenv("STATS_PATH", "./model_stats.json")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

_raw_stats_path = os.getenv("STATS_PATH", "./model_stats.json")
STATS_PATH = (
    Path(_raw_stats_path)
    if Path(_raw_stats_path).is_absolute()
    else PROJECT_ROOT / _raw_stats_path.lstrip("./")
)

print(f"[runner.py] STATS_PATH resolved to: {STATS_PATH}")  # remove after confirming

def run_plssem_pipeline(
    csv_bytes: bytes,
    constructs: list[dict],
    paths: list[dict]
) -> dict:
    """
    Full pipeline:
      1. Write CSV to a temp file
      2. Write model_spec.json
      3. Call Rscript run_model.R
      4. Read and return model_stats.json
      5. Clean up temp files

    Args:
        csv_bytes:  raw bytes from st.file_uploader
        constructs: list of {name, type, indicators} from Streamlit UI
        paths:      list of {from, to} from Streamlit UI

    Returns:
        dict: parsed model_stats.json content
    
    Raises:
        RuntimeError: if R script exits with non-zero code
    """
    # 1. Write CSV to temp file (R-only access)
    tmp_csv = tempfile.NamedTemporaryFile(
        suffix=".csv",
        prefix="plsassist_",
        delete=False
    )
    tmp_csv.write(csv_bytes)
    tmp_csv.close()

    # 2. Write model_spec.json
    spec = {
        "constructs":       constructs,
        "paths":            paths,
        "csv_path":         tmp_csv.name,
        "stats_output_path": str(STATS_PATH)
    }
    spec_path = tmp_csv.name.replace(".csv", "_spec.json")
    with open(spec_path, "w") as f:
        json.dump(spec, f, indent=2)

    # 3. Call R
    try:
        result = subprocess.run(
            [RSCRIPT_PATH, str(R_SCRIPT), spec_path],
            capture_output=True,
            text=True,
            timeout=300          # 5-minute timeout for large datasets
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"R script failed (exit {result.returncode}):\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )
    finally:
        # 4. Always clean up temp files, even on R failure
        for p in [tmp_csv.name, spec_path]:
            if os.path.exists(p):
                os.remove(p)

    # 5. Read and return model_stats.json
    if not os.path.exists(STATS_PATH):
        raise RuntimeError("R script completed but model_stats.json was not created.")

    with open(STATS_PATH, "r") as f:
        return json.load(f)