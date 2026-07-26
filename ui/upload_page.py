# ui/upload_page.py
import streamlit as st
import pandas as pd
import uuid
import sys
import os
from pathlib import Path

# Allow imports from project root
sys.path.append(str(Path(__file__).parent.parent))
from r_pipeline.runner import run_plssem_pipeline


# ─────────────────────────────────────────────────────────────────────────────
# Page config & session state initialisation
# ─────────────────────────────────────────────────────────────────────────────

def init_session_state():
    """Initialise all session state keys on first load."""
    defaults = {
        "uploaded_filename": None,
        "uploaded_df":      None,   # pandas DataFrame of the uploaded CSV
        "csv_bytes":        None,   # raw bytes for passing to R
        "columns":          [],     # list of column names from CSV
        "constructs":       [],     # list of {name, type, indicators}
        "paths":            [],     # list of {from, to}
        "model_stats":      None,   # dict returned by run_plssem_pipeline
        "run_complete":     False,  # True once model_stats.json is written
        "validation_errors": [],    # list of error strings shown before run
        "chat_history":       [],   # list of {role, content, tools_used}
        "chat_thread_id":     None, # LangGraph thread ID — one per session
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# ui/upload_page.py (continued)

# ui/upload_page.py — section_upload()

def section_upload():
    st.header("1 · Upload Dataset")
    st.caption(
        "Upload your survey CSV. Column names will be used as indicator "
        "names when defining constructs. The raw data will be deleted "
        "after the model is estimated."
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="CSV with respondent rows and indicator columns (e.g. SAT_1, SAT_2 …)"
    )

    if uploaded_file is not None:
        # ── FIX: only reset downstream state when file name changes ──────────
        if uploaded_file.name != st.session_state.get("uploaded_filename"):
            try:
                import io
                csv_bytes = uploaded_file.read()
                df = pd.read_csv(io.BytesIO(csv_bytes))

                st.session_state["uploaded_filename"] = uploaded_file.name
                st.session_state["uploaded_df"]       = df
                st.session_state["csv_bytes"]         = csv_bytes
                st.session_state["columns"]           = list(df.columns)
                # Only reset constructs/paths when a NEW file is uploaded
                st.session_state["constructs"]        = []
                st.session_state["paths"]             = []
                st.session_state["model_stats"]       = None
                st.session_state["run_complete"]      = False

            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                return
        # ── If same file, just use existing session state — don't reset ──────

    if st.session_state["uploaded_df"] is not None:
        df = st.session_state["uploaded_df"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Rows",          df.shape[0])
        col2.metric("Columns",       df.shape[1])
        col3.metric("Missing values", int(df.isnull().sum().sum()))

        with st.expander("Preview first 5 rows"):
            st.dataframe(df.head(), use_container_width=True)

        with st.expander("All column names"):
            st.code("\n".join(st.session_state["columns"]))

# ui/upload_page.py (continued)

def section_constructs():
    """Section 2: Define latent constructs and their indicators."""
    if not st.session_state["columns"]:
        st.info("Upload a CSV first to define constructs.")
        return

    st.header("2 · Define Constructs")
    st.caption(
        "Add each latent construct, choose its type, and select "
        "the indicator columns from your CSV."
    )

    # ── Add new construct form ────────────────────────────────────────────────
    with st.form("add_construct_form", clear_on_submit=True):
        st.subheader("Add a construct")
        col1, col2 = st.columns([2, 1])

        new_name = col1.text_input(
            "Construct name",
            placeholder="e.g. Satisfaction",
            help="Use a short descriptive name. No spaces — use underscores if needed."
        )
        new_type = col2.selectbox(
            "Measurement type",
            options=["reflective", "formative"],
            help=(
                "Reflective: indicators are caused by the construct (e.g. attitude items). "
                "Formative: indicators cause the construct (e.g. index components)."
            )
        )
        new_indicators = st.multiselect(
            "Indicator columns",
            options=st.session_state["columns"],
            help="Select all CSV columns that measure this construct."
        )

        submitted = st.form_submit_button("Add Construct", type="primary")

        if submitted:
            # Validate inputs
            errors = []
            if not new_name.strip():
                errors.append("Construct name cannot be empty.")
            if " " in new_name.strip():
                errors.append("Construct name cannot contain spaces. Use underscores.")
            if len(new_indicators) < 2:
                errors.append("A construct needs at least 2 indicators.")

            existing_names = [c["name"] for c in st.session_state["constructs"]]
            if new_name.strip() in existing_names:
                errors.append(f"Construct '{new_name.strip()}' already exists.")

            # Check for indicators already used in another construct
            all_used = [ind for c in st.session_state["constructs"]
                        for ind in c["indicators"]]
            already_used = [ind for ind in new_indicators if ind in all_used]
            if already_used:
                errors.append(
                    f"These indicators are already assigned: {', '.join(already_used)}"
                )

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state["constructs"].append({
                    "name":       new_name.strip(),
                    "type":       new_type,
                    "indicators": new_indicators
                })
                st.success(f"Added construct: {new_name.strip()}")

    # ── Display current constructs ────────────────────────────────────────────
    if st.session_state["constructs"]:
        st.subheader("Current constructs")
        for i, construct in enumerate(st.session_state["constructs"]):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.markdown(
                    f"**{construct['name']}** — "
                    f"`{construct['type']}` — "
                    f"{len(construct['indicators'])} indicators"
                )
                col2.caption(", ".join(construct["indicators"]))
                if col3.button("Remove", key=f"remove_construct_{i}"):
                    # Also remove any paths that reference this construct
                    removed_name = construct["name"]
                    st.session_state["constructs"].pop(i)
                    st.session_state["paths"] = [
                        p for p in st.session_state["paths"]
                        if p["from"] != removed_name and p["to"] != removed_name
                    ]
                    st.rerun()
            st.divider()
    else:
        st.caption("No constructs defined yet.")

# ui/upload_page.py (continued)

def section_paths():
    """Section 3: Define structural paths between constructs."""
    constructs = st.session_state["constructs"]

    if len(constructs) < 2:
        st.info("Define at least 2 constructs before specifying paths.")
        return

    st.header("3 · Define Structural Paths")
    st.caption(
        "Type FROM → TO pairs to define the structural (inner) model. "
        "Both names must exactly match a construct defined above."
    )

    construct_names = [c["name"] for c in constructs]

    # ── Reference box ─────────────────────────────────────────────────────────
    with st.expander("Your construct names (copy from here)"):
        st.code("\n".join(construct_names))

    # ── Add path form ─────────────────────────────────────────────────────────
    with st.form("add_path_form", clear_on_submit=True):
        st.subheader("Add a path")
        col1, col2 = st.columns(2)

        from_construct = col1.text_input(
            "FROM construct",
            placeholder="e.g. Satisfaction",
            help="The predictor / exogenous construct"
        )
        to_construct = col2.text_input(
            "TO construct",
            placeholder="e.g. Loyalty",
            help="The outcome / endogenous construct"
        )

        submitted = st.form_submit_button("Add Path", type="primary")

        if submitted:
            errors = []
            from_c = from_construct.strip()
            to_c   = to_construct.strip()

            if not from_c or not to_c:
                errors.append("Both FROM and TO construct names are required.")
            if from_c == to_c:
                errors.append("FROM and TO cannot be the same construct (no self-loops).")
            if from_c not in construct_names:
                errors.append(
                    f"'{from_c}' does not match any defined construct. "
                    f"Valid names: {', '.join(construct_names)}"
                )
            if to_c not in construct_names:
                errors.append(
                    f"'{to_c}' does not match any defined construct. "
                    f"Valid names: {', '.join(construct_names)}"
                )

            existing_paths = [(p["from"], p["to"]) for p in st.session_state["paths"]]
            if (from_c, to_c) in existing_paths:
                errors.append(f"Path {from_c} → {to_c} already exists.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state["paths"].append({"from": from_c, "to": to_c})
                st.success(f"Added path: {from_c} → {to_c}")

    # ── Display current paths ─────────────────────────────────────────────────
    if st.session_state["paths"]:
        st.subheader("Current paths")
        for i, path in enumerate(st.session_state["paths"]):
            col1, col2 = st.columns([4, 1])
            col1.markdown(f"**{path['from']}** → **{path['to']}**")
            if col2.button("Remove", key=f"remove_path_{i}"):
                st.session_state["paths"].pop(i)
                st.rerun()
        st.divider()
    else:
        st.caption("No paths defined yet.")

# ui/upload_page.py (continued)

def validate_spec() -> list[str]:
    """
    Validate the full model spec before sending to R.
    Returns a list of error strings — empty list means valid.
    """
    errors = []
    df      = st.session_state["uploaded_df"]
    constructs = st.session_state["constructs"]
    paths      = st.session_state["paths"]

    if df is None:
        errors.append("No dataset uploaded.")
        return errors

    if len(constructs) < 2:
        errors.append("Define at least 2 constructs.")

    if len(paths) < 1:
        errors.append("Define at least 1 structural path.")

    csv_columns = set(df.columns)

    for construct in constructs:
        # Check minimum indicators
        if len(construct["indicators"]) < 2:
            errors.append(
                f"Construct '{construct['name']}' has fewer than 2 indicators."
            )
        # Check each indicator column exists in the CSV
        for indicator in construct["indicators"]:
            if indicator not in csv_columns:
                errors.append(
                    f"Indicator '{indicator}' in construct "
                    f"'{construct['name']}' not found in the uploaded CSV. "
                    f"Check for typos or extra spaces."
                )

    # Check all path constructs still exist (guard against removed constructs)
    construct_names = {c["name"] for c in constructs}
    for path in paths:
        if path["from"] not in construct_names:
            errors.append(f"Path FROM construct '{path['from']}' no longer exists.")
        if path["to"] not in construct_names:
            errors.append(f"Path TO construct '{path['to']}' no longer exists.")

    # Check for endogenous constructs (every TO must have at least one FROM)
    to_constructs = {p["to"] for p in paths}
    if to_constructs:
        for to_c in to_constructs:
            from_constructs = [p["from"] for p in paths if p["to"] == to_c]
            if not from_constructs:
                errors.append(f"Construct '{to_c}' has no predictors (no FROM paths).")

    return errors

# ui/upload_page.py (continued)

def section_run():
    """Section 4: Validate spec and run the R pipeline."""
    if not st.session_state["constructs"] or not st.session_state["paths"]:
        return

    st.header("4 · Validate & Run Model")

    # ── FIX: if model already ran, skip validation and show success ───────────
    if st.session_state["run_complete"]:
        st.success("Model has been estimated successfully. See results below.")
        return
    # ─────────────────────────────────────────────────────────────────────────

    with st.expander("Review model specification"):
        st.json({
            "constructs": st.session_state["constructs"],
            "paths":      st.session_state["paths"]
        })

    errors = validate_spec()
    if errors:
        st.error("Fix the following issues before running:")
        for e in errors:
            st.markdown(f"- {e}")
        return

    st.success("Model specification is valid. Ready to run.")

    if st.button("Run PLS-SEM Model", type="primary", use_container_width=True):
        with st.spinner("Running seminr model in R… this may take 30–90 seconds."):
            try:
                stats = run_plssem_pipeline(
                    csv_bytes  = st.session_state["csv_bytes"],
                    constructs = st.session_state["constructs"],
                    paths      = st.session_state["paths"]
                )
                st.session_state["model_stats"]  = stats
                st.session_state["run_complete"] = True
                st.session_state["csv_bytes"]    = None
                st.session_state["uploaded_df"]  = None
                st.success("Model estimated successfully!")
                st.rerun()

            except RuntimeError as e:
                st.error("R pipeline failed:")
                st.code(str(e), language="bash")

# ui/upload_page.py — replace section_results() entirely

def safe_round(val, digits=3):
    """Safely round a value that may be a dict, list, None, or numeric."""
    if isinstance(val, dict):
        # R sometimes serialises a single value as {"construct_name": value}
        # Extract the first numeric value found
        for v in val.values():
            try:
                return round(float(v), digits)
            except (TypeError, ValueError):
                continue
        return "—"
    if isinstance(val, list):
        # Take first element if R returned a length-1 array
        try:
            return round(float(val[0]), digits)
        except (TypeError, ValueError, IndexError):
            return "—"
    if val is None:
        return "—"
    try:
        return round(float(val), digits)
    except (TypeError, ValueError):
        return "—"


def section_results():
    """Section 5: Show a summary of model_stats.json after a successful run."""
    if not st.session_state["run_complete"]:
        return

    stats = st.session_state["model_stats"]
    st.header("5 · Model Results Summary")
    st.caption("Full interpretation is available in the Chatbot tab.")

    # ── Metadata ──────────────────────────────────────────────────────────────
    meta = stats.get("metadata", {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Observations",   meta.get("n_obs", "—"))
    c2.metric("Constructs",     meta.get("n_constructs", "—"))
    c3.metric("Paths",          meta.get("n_paths", "—"))
    c4.metric("seminr version", meta.get("seminr_version", "—"))

    # ── Reliability table ─────────────────────────────────────────────────────
    if stats.get("reliability"):
        st.subheader("Reliability & Convergent Validity")
        rel_rows = []
        for construct, values in stats["reliability"].items():
            # values may be a dict of dicts from R JSON — use safe_round
            rel_rows.append({
                "Construct":             construct,
                "Cronbach α":            safe_round(values.get("cronbach_alpha")),
                "Composite Reliability": safe_round(values.get("composite_reliability")),
                "AVE":                   safe_round(values.get("AVE")),
                "ρA":                    safe_round(values.get("rho_A")),
            })
        rel_df = pd.DataFrame(rel_rows).set_index("Construct")

        def highlight_ave(val):
            try:
                return "background-color: #fee2e2" if float(val) < 0.5 else ""
            except (TypeError, ValueError):
                return ""

        st.dataframe(
            rel_df.style.map(highlight_ave, subset=["AVE"]),
            use_container_width=True
        )
        st.caption("Red cells: AVE < 0.50 — convergent validity concern.")

    # ── Path coefficients ─────────────────────────────────────────────────────
    if stats.get("bootstrapped_paths"):
        st.subheader("Structural Paths (Bootstrapped)")
        path_rows = []
        for path_name, values in stats["bootstrapped_paths"].items():
            path_rows.append({
                "Path":        path_name,
                "Coefficient": safe_round(values.get("original")),
                "t-stat":      safe_round(values.get("t_stat")),
                "p-value":     safe_round(values.get("p_value")),
                "2.5% CI":     safe_round(values.get("ci_lower")),
                "97.5% CI":    safe_round(values.get("ci_upper")),
            })
        path_df = pd.DataFrame(path_rows).set_index("Path")

        def highlight_pvalue(val):
            try:
                return "background-color: #dcfce7" if float(val) < 0.05 else ""
            except (TypeError, ValueError):
                return ""

        st.dataframe(
            path_df.style.map(highlight_pvalue, subset=["p-value"]),
            use_container_width=True
        )
        st.caption("Green cells: p < 0.05 — statistically significant path.")

    # ── R² ────────────────────────────────────────────────────────────────────
    if stats.get("r_squared"):
        st.subheader("R² (Explanatory Power)")
        r2_df = pd.DataFrame(
            [{"Construct": k, "R²": safe_round(v)}
             for k, v in stats["r_squared"].items()]
        ).set_index("Construct")
        st.dataframe(r2_df, use_container_width=True)

    # ── Navigate to chatbot ───────────────────────────────────────────────────
    st.divider()
    st.info(
        "Your model is ready. Switch to the **Chatbot** tab to ask "
        "business questions about these results."
    )

# ui/upload_page.py (continued)

def show():
    """Main entry point called from app.py."""
    init_session_state()

    # ── If model has been run, show only results + start over button ──────────
    if st.session_state["run_complete"]:
        st.title("PLS-Assist · Model Setup")
        st.divider()
        section_results()
        st.divider()
        if st.button("🔄 Start Over", type="secondary", use_container_width=True):
            # Reset all state back to defaults
            for key in [
                "uploaded_filename", "uploaded_df", "csv_bytes",
                "columns", "constructs", "paths",
                "model_stats", "run_complete", "validation_errors",
                "chat_history", "chat_thread_id"
            ]:
                st.session_state[key] = None if key in [
                    "uploaded_filename", "uploaded_df", "csv_bytes",
                    "model_stats", "chat_thread_id"
                ] else [] if key in [
                    "columns", "constructs", "paths",
                    "chat_history", "validation_errors"
                ] else False
            st.rerun()
        return

    # ── Normal flow — model not yet run ──────────────────────────────────────
    st.title("PLS-Assist · Model Setup")
    st.markdown(
        "Upload your dataset, define your constructs and structural paths, "
        "then run the PLS-SEM model. Your raw data never leaves this pipeline."
    )
    st.divider()
    section_upload()
    st.divider()
    section_constructs()
    st.divider()
    section_paths()
    st.divider()
    section_run()