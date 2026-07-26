# r_pipeline/run_model.R
library(seminr)
library(jsonlite)

# ── 0. Arguments ──────────────────────────────────────────────────────────────
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript run_model.R <path_to_model_spec.json>")

spec_path <- args[1]
cat("Reading spec from:", spec_path, "\n")

# ── 1. Load spec ──────────────────────────────────────────────────────────────
spec        <- fromJSON(spec_path, simplifyVector = FALSE)
csv_path    <- spec$csv_path
output_path <- spec$stats_output_path

# ── 2. Load and validate dataset ──────────────────────────────────────────────
cat("Loading dataset from:", csv_path, "\n")
data <- read.csv(csv_path, stringsAsFactors = FALSE)

# Check all indicator columns exist in the dataset
all_indicators <- unlist(lapply(spec$constructs, function(c) c$indicators))
missing_cols   <- setdiff(all_indicators, colnames(data))
if (length(missing_cols) > 0) {
  stop(paste("Missing columns in dataset:", paste(missing_cols, collapse = ", ")))
}

cat("Dataset loaded:", nrow(data), "rows,", ncol(data), "columns\n")

# ── 3. Build measurement model (outer model) ──────────────────────────────────
mm_list <- lapply(spec$constructs, function(con) {
  indicators <- unlist(con$indicators)

  if (con$type == "reflective") {
    reflective(con$name, indicators)
  } else {
    composite(con$name, indicators, weights = mode_B)
  }
})

measurement_model <- do.call(constructs, mm_list)

# Step 3b — portable measurement model construction
measurement_model <- do.call(
  constructs,
  lapply(spec$constructs, function(con) {
    indicators <- unlist(con$indicators)

    if (tolower(con$type) == "reflective") {
      reflective(con$name, indicators)
    } else {
      composite(con$name, indicators, weights = mode_B)
    }
  })
)

# ── 4. Build structural model (inner model) ───────────────────────────────────
path_list <- lapply(spec$paths, function(p) {
  paths(from = p$from, to = p$to)
})
structural_model <- do.call(relationships, path_list)

# ── 5. Estimate PLS model ─────────────────────────────────────────────────────
cat("Estimating PLS model...\n")
pls_model <- estimate_pls(
  data              = data,
  measurement_model = measurement_model,
  structural_model  = structural_model,
  inner_weights     = path_weighting,   # path weighting scheme (default)
  missing           = mean_replacement  # mean replacement for missing values
)

model_summary <- summary(pls_model)

# ── 6. Bootstrap for path significance and CIs ────────────────────────────────
cat("Bootstrapping (1000 iterations)...\n")
boot_model   <- bootstrap_model(pls_model, nboot = 1000, seed = 42)
boot_summary <- summary(boot_model)

# Add this temporarily after boot_summary is created in run_model.R
cat("Bootstrap path colnames:", paste(colnames(boot_summary$bootstrapped_paths), collapse=" | "), "\n")
cat("Bootstrap path rownames:", paste(rownames(boot_summary$bootstrapped_paths), collapse=" | "), "\n")

# ── 7. Blindfolding for Q² (predictive relevance) ────────────────────────────
cat("Blindfolding for Q²...\n")
blindfold <- NULL
blind_summary <- NULL

if ("blindfold_pl" %in% ls("package:seminr")) {
  blindfold <- blindfold_pl(pls_model, k = 7)
  blind_summary <- summary(blindfold)
} else {
  message("Skipping Q²: blindfolding not available in this version of seminr.")
}

# ── 8. Extract all statistics ─────────────────────────────────────────────────

# Helper: safely convert matrix/df to named list, replacing NaN/Inf with NULL
safe_matrix <- function(m) {
  if (is.null(m)) return(NULL)
  m[is.nan(m) | is.infinite(m)] <- NA
  as.data.frame(m)
}

# 8a. Outer loadings (reflective indicators)
loadings_df <- safe_matrix(model_summary$loadings)

# 8b. Outer weights (formative indicators)
weights_df  <- safe_matrix(model_summary$weights)

# 8c. Reliability: AVE, CR, Cronbach alpha
reliability <- list()
if (!is.null(model_summary$reliability)) {
  rel <- as.data.frame(model_summary$reliability)
  for (construct in rownames(rel)) {
    reliability[[construct]] <- list(
      cronbach_alpha        = rel[construct, "alpha"],
      composite_reliability = rel[construct, "rhoC"],
      AVE                   = rel[construct, "AVE"],
      rho_A                 = rel[construct, "rhoA"]
    )
  }
}

# 8d. Discriminant validity — HTMT
htmt_df <- safe_matrix(model_summary$validity$htmt)

# 8e. Discriminant validity — Fornell-Larcker
fl_df   <- safe_matrix(model_summary$validity$fl_criteria)

# ── 8f. Structural paths — extract ONLY path coefficients (not R² rows) ──────

paths_out <- list()
if (!is.null(model_summary$paths)) {
  path_mat <- model_summary$paths

  # seminr puts R^2 and AdjR^2 as rows — filter them out
  # Keep only rows whose names match "construct -> construct" pattern
  all_row_names <- rownames(path_mat)
  path_row_names <- all_row_names[
    !all_row_names %in% c("R^2", "AdjR^2", "R2", "AdjR2")
  ]

  for (rn in path_row_names) {
    # Find columns that are not NA for this row (those are the actual paths)
    row_vals <- path_mat[rn, ]
    non_na_cols <- names(row_vals[!is.na(row_vals) & row_vals != 0])

    for (col in non_na_cols) {
      path_key <- paste(rn, "->", col)
      paths_out[[path_key]] <- list(
        coefficient = as.numeric(path_mat[rn, col])
      )
    }
  }
}

#R² extraction ───────────────────────────────────────────
r_squared <- list()
tryCatch({
  if (!is.null(model_summary$paths)) {
    path_mat <- as.data.frame(model_summary$paths)
    r2_rowname <- rownames(path_mat)[grepl("R", rownames(path_mat), fixed = TRUE) & grepl("2", rownames(path_mat), fixed = TRUE) & !grepl("Adj", rownames(path_mat), fixed = TRUE)]
    if (length(r2_rowname) > 0) {
      r2_row <- path_mat[r2_rowname[1], , drop = FALSE]
      for (col in colnames(r2_row)) {
        val <- as.numeric(r2_row[1, col])
        if (!is.na(val) && val != 0) {
          r_squared[[col]] <- val
        }
      }
    }
  }
}, error = function(e) {
  cat("R² extraction failed:", conditionMessage(e), "\n")
})

#f² extraction ───────────────────────────────────────────
fSquared <- list()
tryCatch({
  if (!is.null(model_summary$fSquare)) {
    fs <- as.data.frame(model_summary$fSquare)
    for (rn in rownames(fs)) {
      fSquared[[rn]] <- as.list(fs[rn, , drop = FALSE])
    }
  }
}, error = function(e) {
  cat("f² extraction failed:", conditionMessage(e), "\n")
})

# ── 8g. Bootstrap path CIs — fix p_value scalar extraction ───────────────────

boot_paths <- list()
if (!is.null(boot_summary$bootstrapped_paths)) {
  bp <- boot_summary$bootstrapped_paths

  for (rn in rownames(bp)) {
    # as.numeric() forces each cell to a scalar — prevents [] serialisation
    p_val_raw <- bp[rn, "Bootstrap P Val"]
    p_val     <- if (length(p_val_raw) == 0 || is.na(p_val_raw)) {
      # Derive from t-stat using two-tailed normal approximation if missing
      t_val <- as.numeric(bp[rn, "T Stat."])
      if (!is.na(t_val)) round(2 * (1 - pnorm(abs(t_val))), 4) else NA
    } else {
      as.numeric(p_val_raw)
    }

    boot_paths[[rn]] <- list(
      original       = as.numeric(bp[rn, "Original Est."]),
      bootstrap_mean = as.numeric(bp[rn, "Bootstrap Mean"]),
      t_stat         = as.numeric(bp[rn, "T Stat."]),
      p_value        = p_val,        # now guaranteed scalar or NA
      ci_lower       = as.numeric(bp[rn, "2.5% CI"]),
      ci_upper       = as.numeric(bp[rn, "97.5% CI"])
    )
  }
}

# 8h. Q² predictive relevance
q_squared <- list()

if (!is.null(blindfold) &&
    !is.null(blind_summary) &&
    !is.null(blind_summary$q2_predict)) {

  for (cn in names(blind_summary$q2_predict)) {
    q_squared[[cn]] <- blind_summary$q2_predict[[cn]]
  }

} else {
  message("Q² results unavailable (blindfolding was skipped).")
}

# ── 9. Assemble and write model_stats.json ────────────────────────────────────
model_stats <- list(
  metadata    = list(
    n_obs       = nrow(data),
    n_constructs = length(spec$constructs),
    n_paths      = length(spec$paths),
    seminr_version = as.character(packageVersion("seminr"))
  ),
  constructs  = lapply(spec$constructs, function(c) list(
    name       = c$name,
    type       = c$type,
    indicators = c$indicators
  )),
  loadings    = loadings_df,
  weights     = weights_df,
  reliability = reliability,
  validity    = list(
    htmt             = htmt_df,
    fornell_larcker  = fl_df
  ),
  paths       = paths_out,
  r_squared   = r_squared,
  f_squared   = fSquared,
  bootstrapped_paths = boot_paths,
  q_squared   = q_squared
)

cat("Writing model_stats.json to:", output_path, "\n")
write(toJSON(model_stats, auto_unbox = TRUE, pretty = TRUE, na = "null"),
      file = output_path)
cat("Done.\n")

# ── 10. Delete the CSV (privacy enforcement) ──────────────────────────────────
if (file.exists(csv_path)) {
  file.remove(csv_path)
  cat("CSV deleted from:", csv_path, "\n")
}