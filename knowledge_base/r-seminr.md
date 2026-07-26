# SEMinR — Complete Workflow Guide

## Overview

**SEMinR** (Structural Equation Modeling in R) provides a natural R syntax for specifying, estimating, and assessing PLS-SEM models. It supports reflective and formative constructs, higher-order constructs, PLSc, bootstrapping, PLSpredict, CVPAT, MGA, mediation significance testing, and moderation analysis.

**Installation**:
```r
install.packages("seminr")
library(seminr)
```

---

## 1. Model Specification

### Measurement Model

```r
# Reflective constructs
measurements <- constructs(
  reflective("Satisfaction", multi_items("sat_", 1:4)),
  reflective("Loyalty",     multi_items("loy_", 1:3)),
  reflective("Quality",     multi_items("qual_", 1:5)),

  # Formative construct (Mode B composite)
  composite("Value",  multi_items("val_", 1:3), weights = mode_B),

  # Single-item construct
  reflective("Price", single_item("price_1"))
)
```

**Key functions**:
- `reflective("Construct_Name", items)` — reflective measurement (Mode A weights + automatic PLSc correction of path coefficients and outer loadings). Use when construct is theoretically reflective and DGP is common factor.
- `composite("Construct_Name", items, weights = mode_A)` — composite measurement with correlation weights (Mode A). No PLSc correction. Use when construct is theoretically formative/composite.
- `composite("Construct_Name", items, weights = mode_B)` — composite measurement with regression weights (Mode B). Use for formative constructs where regression-based weights are desired.
- `multi_items("prefix_", range)` — generate indicator names (e.g., "sat_1", "sat_2", ...)
- `single_item("indicator_name")` — single indicator

**IMPORTANT — Conceptualization vs. Estimation**: `reflective()` and `composite()` are estimation choices, not just measurement model labels. `reflective()` triggers PLSc, which corrects path coefficients and outer loadings for attenuation bias. `composite(mode_A)` uses the same Mode A correlation weights but without correction. The choice should match the theoretical construct type:
- Reflective constructs (common factor DGP) → use `reflective()` (triggers PLSc)
- Formative/composite constructs → use `composite(mode_A)` or `composite(mode_B)`

There is no `formative()` function in SEMinR. Use `composite(..., weights = mode_B)` for formative constructs (Sarstedt et al., 2016; Guenther et al., 2025).

**Prediction implications**: PLSc correction affects out-of-sample predictions. The prediction pipeline is W × B × L^T: outer_weights → path_coef → outer_loadings → predicted indicators. When `reflective()` is used, PLSc-corrected path_coef and outer_loadings are used in this pipeline, affecting CVPAT and PLSpredict results.

### Structural Model

```r
structure <- relationships(
  paths(from = c("Quality", "Value"), to = "Satisfaction"),
  paths(from = "Satisfaction",        to = "Loyalty")
)
```

**Key functions**:
- `paths(from, to)` — specify directed paths
- Multiple `paths()` calls can be combined in `relationships()`

### Interaction Terms (Moderation)

```r
# Two-stage approach (recommended default)
measurements <- constructs(
  reflective("Quality",      multi_items("qual_", 1:5)),
  reflective("Satisfaction", multi_items("sat_", 1:4)),
  reflective("Involvement",  multi_items("inv_", 1:3)),
  interaction_term(iv = "Quality", moderator = "Involvement", method = two_stage)
)

structure <- relationships(
  paths(from = c("Quality", "Involvement", "Quality*Involvement"), to = "Satisfaction")
)
```

**Interaction methods**:
- `two_stage` — recommended default; works for all construct types
- `product_indicator` — for reflective constructs only
- `orthogonal` — orthogonalized product indicators

### Higher-Order Constructs

```r
# Two-stage approach for HOC
measurements <- constructs(
  reflective("Cognitive",  multi_items("cog_", 1:4)),
  reflective("Affective",  multi_items("aff_", 1:4)),
  reflective("Behavioral", multi_items("beh_", 1:3)),
  higher_composite("Attitude", c("Cognitive", "Affective", "Behavioral"),
                   method = two_stage, weights = mode_A)
)

```

**Parameters**:
- `method = two_stage` (only available method in seminr)
- `weights = mode_A` (reflective HOC) or `weights = mode_B` (formative HOC)

---

## 2. Model Estimation

### Standard PLS-SEM

```r
model <- estimate_pls(
  data = my_data,
  measurement_model = measurements,
  structural_model  = structure,
  inner_weights = path_weighting,  # path_weighting (default) or path_factorial
  missing = mean_replacement,      # mean_replacement (default) or NA
  missing_value = NA               # value representing missing data
)
```

### Consistent PLS (PLSc)

```r
model <- estimate_pls(
  data = my_data,
  measurement_model = measurements,
  structural_model  = structure
)

# Apply PLSc correction
model_plsc <- PLSc(model)
```

Or use `estimate_pls()` with consistent estimation when all constructs are reflective.

### Accessing Basic Results

```r
# Summary of results
summary(model)

# Path coefficients
model$path_coef

# Outer loadings
model$outer_loadings

# Outer weights
model$outer_weights

# R-squared
model$rSquared

# Construct scores
model$construct_scores
```

---

## 3. Bootstrapping

```r
boot <- bootstrap_model(
  seminr_model = model,
  nboot = 10000,       # number of bootstrap subsamples
  cores = parallel::detectCores(),  # parallel processing
  seed = 123           # for reproducibility
)

# Summary of bootstrap results
summary(boot)

# Access raw bootstrap matrices (from boot object directly)
boot$boot_paths      # bootstrap path coefficient samples
boot$boot_loadings   # bootstrap loading samples
boot$boot_weights    # bootstrap weight samples
boot$boot_HTMT       # bootstrap HTMT samples

# Access summarized bootstrap results (from summary object)
boot_summary <- summary(boot)
boot_summary$bootstrapped_paths     # Original, Mean, SD, T-Stat, 2.5%CI, 97.5%CI
boot_summary$bootstrapped_loadings
boot_summary$bootstrapped_weights
boot_summary$bootstrapped_HTMT
```

**Important**: `bootstrap_model()` defaults to `nboot = 500`. Always set `nboot = 10000` explicitly for publication-quality results.

### Bootstrap Summary Contents

The `summary(boot)` output includes:
- Path coefficients with t-values, p-values, and confidence intervals (2.5%, 97.5%)
- Outer loadings with significance tests
- Outer weights with significance tests
- HTMT with confidence intervals
- Total effects (direct + indirect)
- Specific indirect effects

---

## 4. Measurement Model Assessment

### Reflective Constructs

```r
model_summary <- summary(model)

# Reliability: Cronbach's alpha, rho_C (composite reliability), rho_A, AVE
model_summary$reliability

# Outer loadings
model_summary$loadings

# HTMT
model_summary$validity$htmt

# With bootstrap: HTMT confidence intervals
boot_summary <- summary(boot)
boot_summary$bootstrapped_HTMT
```

### Formative Constructs

```r
# Outer weights (with bootstrap significance)
boot_summary <- summary(boot)
boot_summary$bootstrapped_weights

# VIF for formative indicators
model_summary$validity$vif_items

# Outer loadings (for absolute contribution check)
model_summary$loadings
```

### Discriminant Validity

```r
# HTMT matrix
model_summary$validity$htmt

# Bootstrap HTMT (confidence intervals)
boot_summary$bootstrapped_HTMT
# Check that upper CI bound < threshold (0.85 or 0.90) for all pairs
```

---

## 5. Structural Model Assessment

### Path Coefficients and Significance

```r
boot_summary <- summary(boot)

# Bootstrapped paths: Original, Mean, SD, T-Stat, 2.5%CI, 97.5%CI
boot_summary$bootstrapped_paths

# Total effects
boot_summary$bootstrapped_total_paths
```

### R² and Adjusted R²

```r
model_summary <- summary(model)
model_summary$paths  # includes R² for each endogenous construct
```

### f² (Effect Size)

```r
model_summary$fSquare
```

### VIF (Structural Collinearity)

```r
model_summary$vif_antecedents
```

---

## 6. PLSpredict and CVPAT

### PLSpredict

```r
set.seed(123)  # set seed before calling for reproducibility
predictions <- predict_pls(
  model = model,
  technique = predict_DA,    # predict_DA (direct antecedents) or predict_EA (all antecedents)
  noFolds = 10,              # number of cross-validation folds
  reps = 10                  # repetitions for stability
)

# Summary: shows RMSE, MAE for PLS vs LM vs mean
summary(predictions)

# Access prediction errors per indicator
predictions$items$PLS_out_of_sample    # PLS predictions
predictions$items$lm_out_of_sample     # LM benchmark predictions (note lowercase 'lm')
```

### Interpreting PLSpredict Output

The summary compares:
1. **PLS RMSE vs. Mean RMSE**: If PLS < Mean → model has basic predictive power
2. **PLS RMSE vs. LM RMSE**:
   - All indicators PLS < LM → high predictive power
   - Majority → medium
   - Minority → low
   - None → no predictive power beyond direct regression

### CVPAT

```r
# CVPAT is integrated into predict_pls output
predictions <- predict_pls(
  model = model,
  technique = predict_DA,
  noFolds = 10,
  reps = 10
)

# Access CVPAT results
summary(predictions)
# Look for the CVPAT test statistic and p-value
# Significant negative average loss differential → PLS outperforms benchmark
```

---

## 7. IPMA (Importance-Performance Map Analysis)

SEMinR does not have a built-in `IPMA()` function. IPMA must be computed manually from model results.

```r
# --- Manual IPMA computation ---
model <- estimate_pls(data = data, measurement_model = mm, structural_model = sm)
boot <- bootstrap_model(model, nboot = 10000, cores = parallel::detectCores(), seed = 123)
boot_summary <- summary(boot)

# Step 1: Importance = unstandardized total effects on the target construct
# Use total effects from bootstrap summary
total_effects <- boot_summary$bootstrapped_total_paths
# Filter rows ending in " -> Loyalty" for the target construct
importance <- total_effects[grep("-> Loyalty$", rownames(total_effects)), "Original Est."]

# Step 2: Performance = rescaled construct scores (0-100)
# Rescale each indicator to 0-100 range, then compute construct scores
rescale_01 <- function(x) (x - min(x, na.rm = TRUE)) / (max(x, na.rm = TRUE) - min(x, na.rm = TRUE)) * 100
performance <- colMeans(apply(model$construct_scores, 2, rescale_01))

# Step 3: Plot
plot(importance, performance[names(importance)],
     xlab = "Importance (Total Effect)", ylab = "Performance (0-100)",
     pch = 19, cex = 1.5, xlim = c(0, max(importance) * 1.2))
text(importance, performance[names(importance)], labels = names(importance), pos = 3)
abline(h = mean(performance[names(importance)]), v = mean(importance), lty = 2, col = "grey")
```

**Requirements**: IPMA requires all indicators to have positive outer weights and no moderating effects in the model. Rescale indicators to a common scale (e.g., all 1–7 Likert) before estimation.

---

## 8. Mediation Analysis

```r
# Specify a mediation model
measurements <- constructs(
  reflective("X", multi_items("x_", 1:4)),
  reflective("M", multi_items("m_", 1:3)),
  reflective("Y", multi_items("y_", 1:4))
)

structure <- relationships(
  paths(from = "X", to = c("M", "Y")),  # X -> M (a path) and X -> Y (c' direct)
  paths(from = "M", to = "Y")           # M -> Y (b path)
)

model <- estimate_pls(data = my_data,
                      measurement_model = measurements,
                      structural_model = structure)

boot <- bootstrap_model(model, nboot = 10000, seed = 123)
boot_summary <- summary(boot)

# Total effects (direct + all indirect)
boot_summary$bootstrapped_total_paths

# Specific indirect effects with significance testing
specific_effect_significance(boot,
  from = "X", through = "M", to = "Y",
  alpha = 0.05)
# Returns: indirect effect estimate, t-value, p-value, CI

# Total indirect effect CI (sum of all indirect paths)
total_indirect_ci(boot, from = "X", to = "Y", alpha = 0.05)
```

### Multiple Mediators

```r
structure <- relationships(
  paths(from = "X", to = c("M1", "M2", "Y")),
  paths(from = c("M1", "M2"), to = "Y")
)

# Bootstrap will provide specific indirect effects for each path:
# X -> M1 -> Y
# X -> M2 -> Y
```

---

## 9. Moderation: Interaction Plots and Simple Slopes

```r
# After estimating a model with an interaction term
measurements <- constructs(
  reflective("Quality",      multi_items("qual_", 1:5)),
  reflective("Satisfaction", multi_items("sat_", 1:4)),
  reflective("Involvement",  multi_items("inv_", 1:3)),
  interaction_term(iv = "Quality", moderator = "Involvement", method = two_stage)
)

structure <- relationships(
  paths(from = c("Quality", "Involvement", "Quality*Involvement"), to = "Satisfaction")
)

model <- estimate_pls(data = data, measurement_model = measurements, structural_model = structure)
boot <- bootstrap_model(model, nboot = 10000, seed = 123)

# Simple slopes analysis
slope_analysis(
  moderated_model = model,
  dv = "Satisfaction",
  moderator = "Involvement",
  iv = "Quality",
  leg_place = "bottomright"  # legend placement
)
# Plots the relationship between IV and DV at low/mean/high levels of moderator
```

**Note**: `interaction_term()` default method is `product_indicator`. Always specify `method = two_stage` explicitly when working with formative constructs or mixed models.

---

## 10. Multigroup Analysis (MGA)

```r
# SEMinR provides basic PLS-MGA via estimate_pls_mga()
# Requires a grouping variable in the data

mga_results <- estimate_pls_mga(
  pls_model = model,
  condition = data$group_variable  # factor or character vector
)

# Results contain path comparisons between groups
# Includes difference in path coefficients and p-values
summary(mga_results)
```

**Note**: For full MICOM testing and advanced MGA (permutation tests), use cSEM or SmartPLS. SEMinR's MGA is a basic nonparametric comparison.

---

## 11. Plotting

```r
# Plot the path model with coefficients
plot(model)

# Plot with bootstrapped significance indicators
plot(boot)

# Customize the plot
plot(model,
     title = "PLS-SEM Results",
     theme = seminr_theme_dark())
```

---

## 12. Complete Workflow Example

```r
library(seminr)

# --- 1. Load data ---
data <- read.csv("survey_data.csv")

# --- 2. Specify measurement model ---
mm <- constructs(
  reflective("Quality",      multi_items("qual_", 1:5)),
  reflective("Satisfaction", multi_items("sat_", 1:4)),
  composite("Value",          multi_items("val_", 1:3), weights = mode_B),
  reflective("Loyalty",      multi_items("loy_", 1:3))
)

# --- 3. Specify structural model ---
sm <- relationships(
  paths(from = c("Quality", "Value"), to = "Satisfaction"),
  paths(from = "Satisfaction",        to = "Loyalty")
)

# --- 4. Estimate ---
model <- estimate_pls(data = data, measurement_model = mm, structural_model = sm)
model_summary <- summary(model)

# --- 5. Bootstrap ---
boot <- bootstrap_model(model, nboot = 10000, cores = parallel::detectCores(), seed = 42)
boot_summary <- summary(boot)

# --- 6. Measurement model assessment ---
# Reflective: loadings, CR, AVE, HTMT
model_summary$reliability        # alpha, rho_C, rho_A, AVE
model_summary$loadings           # outer loadings
model_summary$validity$htmt      # HTMT
boot_summary$bootstrapped_HTMT   # HTMT CIs

# Formative: VIF, weights, loadings
model_summary$validity$vif_items       # VIF
boot_summary$bootstrapped_weights      # weight significance

# --- 7. Structural model assessment ---
boot_summary$bootstrapped_paths        # path coefficients, t, p, CI
model_summary$paths                    # R²
model_summary$fSquare                  # f²
model_summary$vif_antecedents          # structural VIF

# --- 8. Prediction ---
set.seed(42)
pred <- predict_pls(model, technique = predict_DA, noFolds = 10, reps = 10)
summary(pred)

# --- 9. Plot ---
plot(boot)
```

---

## 13. Epistemic Rho (ρε) and Interpretational Confounding Diagnostics

Epistemic rho measures whether a PLS construct score is dominated by its own indicators or has been displaced by structural neighbours. This is especially important for formative constructs.

### Computing ρε Manually (Post-Estimation)

```r
# After estimating a PLS model
model <- estimate_pls(data = data, measurement_model = mm, structural_model = sm)

# Compute epistemic rho for a construct
compute_rho_epsilon <- function(model, construct_name) {
  # Get construct scores
  scores <- model$construct_scores[, construct_name]

  # Get indicator names for this construct
  # From the measurement model specification
  indicators <- model$mmMatrix[model$mmMatrix[, "construct"] == construct_name, "measurement"]

  # Get indicator data
  indicator_data <- model$rawdata[, indicators]

  # Compute first principal component
  pc1 <- prcomp(indicator_data, center = TRUE, scale. = TRUE)$x[, 1]

  # Epistemic rho = absolute correlation between PLS score and PC1
  rho_epsilon <- abs(cor(scores, pc1))

  return(rho_epsilon)
}

# Example usage
rho_eps_quality <- compute_rho_epsilon(model, "Quality")
rho_eps_value <- compute_rho_epsilon(model, "Value")

# Check all constructs
construct_names <- colnames(model$construct_scores)
rho_eps <- sapply(construct_names, function(c) compute_rho_epsilon(model, c))
print(rho_eps)
# All values should be >= 0.70
```

### Bootstrap Epistemic Rho

```r
# Bootstrap epistemic rho for hypothesis testing
# H0: rho_epsilon < 0.70 (confounding present)
# Reject if 5th percentile > 0.70

bootstrap_rho_epsilon <- function(model, construct_name, nboot = 5000, seed = 123) {
  set.seed(seed)
  data <- model$rawdata
  indicators <- model$mmMatrix[model$mmMatrix[, "construct"] == construct_name, "measurement"]

  rho_boot <- numeric(nboot)
  for (b in 1:nboot) {
    idx <- sample(nrow(data), replace = TRUE)
    boot_data <- data[idx, ]

    # Re-estimate PLS on bootstrap sample
    tryCatch({
      boot_model <- estimate_pls(
        data = boot_data,
        measurement_model = model$measurement_model,
        structural_model = model$structural_model
      )
      rho_boot[b] <- compute_rho_epsilon(boot_model, construct_name)
    }, error = function(e) {
      rho_boot[b] <<- NA
    })
  }

  rho_boot <- na.omit(rho_boot)
  list(
    original = compute_rho_epsilon(model, construct_name),
    mean_boot = mean(rho_boot),
    ci_5th = quantile(rho_boot, 0.05),
    ci_95th = quantile(rho_boot, 0.95),
    reject_H0 = quantile(rho_boot, 0.05) > 0.70
  )
}

# Usage
rho_test <- bootstrap_rho_epsilon(model, "Value", nboot = 5000)
# If reject_H0 = TRUE, epistemic reliability is established
```

### Sensitivity Assessment

```r
# Compare rho_epsilon across model specifications
# A change > 0.15 signals IC vulnerability

# Full model
model_full <- estimate_pls(data, mm, sm_full)
rho_full <- compute_rho_epsilon(model_full, "Value")

# Reduced model (remove a path)
sm_reduced <- relationships(
  paths(from = "Quality", to = "Satisfaction"),
  # Removed: paths(from = "Value", to = "Satisfaction")
  paths(from = "Satisfaction", to = "Loyalty")
)
model_reduced <- estimate_pls(data, mm, sm_reduced)
rho_reduced <- compute_rho_epsilon(model_reduced, "Value")

delta_rho <- abs(rho_full - rho_reduced)
cat("Delta rho_epsilon:", delta_rho, "\n")
cat("IC vulnerability:", ifelse(delta_rho > 0.15, "YES", "No"), "\n")
```

### Note on StablePLS

StablePLS modifies the inner weight matrix diagonal from 0 to 1. As of the current SEMinR release, StablePLS is not yet a built-in option. To implement it, either:
1. Use a development version of SEMinR that includes StablePLS support (check CRAN/GitHub for updates)
2. Implement manually by modifying the inner weighting step
3. Use an alternative package that supports the StablePLS modification

When StablePLS becomes available in SEMinR:
```r
# Expected syntax (check documentation for actual implementation)
model_stable <- estimate_pls(
  data = data,
  measurement_model = mm,
  structural_model = sm,
  inner_weights = path_weighting  # with StablePLS flag when available
)
```

---

## Predictive Contribution of the Mediator (PCM)

The PCM metric (Danks, 2021) evaluates whether a mediator improves out-of-sample predictive accuracy. Available via `assess_pcm()` in **seminrExtras**.

```r
library(seminrExtras)

# Estimate a mediation model
mobi_mm <- constructs(
  composite("Image",        multi_items("IMAG", 1:5)),
  composite("Expectation",  multi_items("CUEX", 1:3)),
  composite("Value",        multi_items("PERV", 1:2)),
  composite("Satisfaction", multi_items("CUSA", 1:3)),
  composite("Loyalty",      multi_items("CUSL", 1:3))
)
mobi_sm <- relationships(
  paths(from = "Image",       to = c("Expectation", "Satisfaction", "Loyalty")),
  paths(from = "Expectation", to = c("Value", "Satisfaction")),
  paths(from = "Value",       to = "Satisfaction"),
  paths(from = "Satisfaction", to = "Loyalty")
)
model <- estimate_pls(mobi, mobi_mm, mobi_sm)

# Compute PCM — auto-detects all mediation paths to target
pcm <- assess_pcm(model, target = "Loyalty", noFolds = 10, reps = 10)
pcm               # concise: avg PCM per path with classification
summary(pcm)      # detailed: per-indicator RMSE_DA, RMSE_EA, PCM_RMSE, PCM_MAE
plot(pcm)          # barplot with 0.05/0.10 threshold lines
```

PCM automatically:
- Identifies all X → M → Y mediation paths to the target
- Isolates each path into a partial mediation sub-model (X → M, M → Y, X → Y)
- Runs DA and EA cross-validated predictions via `predict_pls()`
- Computes PCM = (METRIC_EA − METRIC_DA) / METRIC_EA per indicator

Interpretation: < 0.05 = Weak, 0.05–0.10 = Moderate, > 0.10 = Strong, < 0 = Negative (mediator hurts).

---

## Tips and Common Issues

### Data Preparation
- Ensure indicator names in data match those in the model specification
- Missing values: use `missing = mean_replacement` or handle externally
- Scale data consistently (all indicators on the same direction and scale for IPMA)

### Performance
- Use `cores = parallel::detectCores()` for parallel bootstrapping
- For very large models, reduce `nboot` during exploration; use 10,000 for final results

### Common Errors
- **"Indicator not found in data"**: Check that column names match `multi_items()` or `single_item()` names exactly
- **Convergence issues**: Check for collinearity or near-zero-variance indicators
- **Negative R²**: Check model specification; possible suppression or misspecification

### Model Comparison
```r
# Compare nested models by examining changes in R², f², and path significance
# No built-in model comparison test; compare manually
```
