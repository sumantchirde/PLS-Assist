# cSEM — Complete Workflow Guide

## Overview

**cSEM** (Composite-based Structural Equation Modeling) provides a unified framework for composite-based SEM, supporting PLS-PM, GSCA (Generalized Structured Component Analysis), unit weights, and more. It uses lavaan-style model syntax and offers comprehensive `assess()`, `summarize()`, and `predict()` functions. cSEM is particularly strong for PLSc and MGA.

**Installation**:
```r
install.packages("cSEM")
library(cSEM)
```

---

## 1. Model Specification

cSEM uses lavaan-style syntax with some extensions.

### Basic Syntax

```r
model <- "
# Measurement model (reflective: =~, formative: <~)

# Reflective constructs
Quality      =~ qual_1 + qual_2 + qual_3 + qual_4 + qual_5
Satisfaction =~ sat_1 + sat_2 + sat_3 + sat_4
Loyalty      =~ loy_1 + loy_2 + loy_3

# Formative constructs
Value        <~ val_1 + val_2 + val_3

# Structural model
Satisfaction ~ Quality + Value
Loyalty      ~ Satisfaction
"
```

**Syntax rules**:
- `=~` defines reflective measurement (Mode A / common factor)
- `<~` defines formative/composite measurement (Mode B)
- `~` defines structural (regression) relationships
- `+` separates multiple indicators or predictors
- Comments with `#`

### Interaction Terms

```r
model <- "
Quality      =~ qual_1 + qual_2 + qual_3
Involvement  =~ inv_1 + inv_2 + inv_3
Satisfaction =~ sat_1 + sat_2 + sat_3

# Structural model with interaction
Satisfaction ~ Quality + Involvement + Quality.Involvement
"

# Specify the interaction in the csem() call
result <- csem(data, model,
               .PLS_approach_cf = "dist_squared_euclid",
               .PLS_modes = NULL)  # auto-detected from =~ and <~
```

Interactions are defined in the model syntax using dot notation (e.g., `Quality.Involvement`). cSEM automatically creates the interaction term from the specified constructs.

### Higher-Order Constructs

```r
model <- "
# First-order constructs
Cognitive  =~ cog_1 + cog_2 + cog_3
Affective  =~ aff_1 + aff_2 + aff_3
Behavioral =~ beh_1 + beh_2 + beh_3

# Second-order construct (reflective HOC)
Attitude   =~ Cognitive + Affective + Behavioral

# Structural paths
Outcome    =~ out_1 + out_2 + out_3
Outcome    ~ Attitude
"
```

For formative HOC, use `<~`:
```r
# Formative second-order construct
Attitude   <~ Cognitive + Affective + Behavioral
```

---

## 2. Model Estimation

### Standard PLS-SEM

```r
result <- csem(
  .data  = my_data,
  .model = model
)
```

cSEM auto-detects the measurement mode from the model syntax (`=~` → Mode A, `<~` → Mode B).

### PLSc (Consistent PLS)

```r
# PLSc is applied automatically when all constructs are reflective (=~)
# To force consistent estimation:
result <- csem(
  .data = my_data,
  .model = model,
  .disattenuate = TRUE   # applies PLSc correction (default for =~ models)
)
```

### Estimation Options

```r
result <- csem(
  .data = my_data,
  .model = model,
  .PLS_weight_scheme_inner = "path",        # "path" (default), "centroid", "factorial"
  .tolerance = 1e-05,                        # convergence criterion (default)
  .iter_max = 100,                           # max iterations
  .PLS_modes = NULL,                         # auto from syntax; or c(modeA = "...", modeB = "...")
  .disattenuate = TRUE,                      # PLSc correction
  .PLS_approach_cf = "dist_squared_euclid",  # correction factor approach
  .resample_method = "none"                  # no resampling at estimation (use infer/assess later)
)
```

---

## 3. Results Extraction

### summarize()

```r
s <- summarize(result)
s

# Key outputs:
s$Estimates$Loading_estimates        # outer loadings
s$Estimates$Weight_estimates         # outer weights
s$Estimates$Path_estimates           # structural path coefficients
s$Estimates$VIF                      # structural VIF
s$Estimates$R2                       # R² for endogenous constructs
s$Estimates$Effect_estimates         # direct, indirect, total effects, VAF
```

### Direct Access

```r
# Construct scores
result$Estimates$Construct_scores

# Path coefficients
result$Estimates$Path_estimates

# Loadings
result$Estimates$Loading_estimates

# Weights
result$Estimates$Weight_estimates
```

---

## 4. Model Assessment with assess()

The `assess()` function provides a comprehensive model assessment in one call.

```r
a <- assess(result)
a

# Available assessment criteria:
a$AVE                    # Average Variance Extracted
a$Reliability            # Cronbach's alpha, rho_C, rho_A, rho_T
a$HTMT                   # HTMT matrix
a$R2                     # R-squared
a$R2_adj                 # Adjusted R-squared
a$VIF                    # Structural VIF
a$VIF_modeB              # VIF for formative indicators (Mode B)
a$F2                     # f-squared effect sizes
a$GoF                    # Goodness of Fit (Tenenhaus et al.)
a$SRMR                   # SRMR
a$DG                     # Geodesic distance
a$DL                     # Squared Euclidean distance
```

### Specific Assessment Functions

```r
# Reliability
assess(result, .quality_criterion = "reliability")

# Discriminant validity (HTMT)
assess(result, .quality_criterion = "htmt")

# Effect sizes
assess(result, .quality_criterion = "f2")

# Model fit
assess(result, .quality_criterion = c("srmr", "dg", "dl"))
```

---

## 5. Inference (Bootstrapping and Permutation)

### Bootstrapping

```r
# Method 1: Resample during estimation
result_boot <- csem(
  .data = my_data,
  .model = model,
  .resample_method = "bootstrap",
  .R = 5000,                        # number of bootstrap subsamples
  .seed = 123
)

# Method 2: Resample post-estimation
result_boot <- resamplecSEMResults(result, .resample_method = "bootstrap", .R = 5000, .seed = 123)

# Inference
infer <- infer(result_boot)
infer

# Access bootstrap CIs and p-values
infer$Path_estimates       # path coefficients with CIs
infer$Loading_estimates    # loadings with CIs
infer$Weight_estimates     # weights with CIs
infer$Total_effect         # total effects with CIs
infer$Indirect_effect      # indirect effects with CIs
```

### Confidence Interval Types

```r
infer <- infer(result_boot,
  .alpha = 0.05,                          # significance level
  .quantity = c("mean", "sd", "CI_percentile", "CI_basic", "CI_bc", "CI_bca")
)
```

Available CI types:
- `CI_percentile` — percentile bootstrap CI
- `CI_basic` — basic bootstrap CI
- `CI_bc` — bias-corrected CI
- `CI_bca` — bias-corrected and accelerated CI (recommended)

---

## 6. Model Fit (CCA) — Not Recommended

cSEM provides `testOMF()` for CCA model fit assessment, but CCA is **not recommended** for PLS-SEM. These fit indices have limited power and borrowed cutoffs from CB-SEM. Use PLSpredict/CVPAT for predictive assessment instead.

---

## 7. Prediction

### predict()

```r
pred <- predict(result,
  .test_data = NULL,         # NULL = cross-validation; or provide test data
  .cv_folds = 10,            # number of CV folds
  .r = 10,                   # repetitions for stability
  .seed = NULL               # seed only works when .r = 1
)

# Access prediction metrics
pred$Prediction_metrics      # RMSE, MAE for each indicator
# Compares PLS model against linear model (LM) benchmark
```

### Interpreting Prediction Results

Same logic as PLSpredict:
1. Compare PLS RMSE vs Mean RMSE (basic predictive power)
2. Compare PLS RMSE vs LM RMSE (predictive power of the structural model)
3. Majority of indicators with PLS < LM → medium to high predictive power

---

## 8. Multigroup Analysis (MGA)

### MICOM (Measurement Invariance)

```r
# First, estimate the model with .id to define groups
result_group <- csem(
  .data = my_data,
  .model = model,
  .id = "group_variable"            # column name for grouping (splits data)
)

# Test measurement invariance on the grouped result
micom <- testMICOM(
  .object = result_group,
  .R = 5000,
  .seed = 123
)

micom
# Reports: Step 2 (compositional invariance) and Step 3 (equality of means/variances)
# Step 1 (configural) is assumed by using the same model
```

### MGA Comparison

```r
# Estimate model per group
result_group <- csem(
  .data = my_data,
  .model = model,
  .id = "group_variable",           # splits data by this column
  .resample_method = "bootstrap",
  .R = 5000,
  .seed = 123
)

# Compare groups
mga <- testMGD(result_group,
  .approach_mgd = c("Klesel", "Chin", "Sarstedt", "Keil", "Nitzl", "Henseler"),
  .R_permutation = 5000,
  .seed = 123
)

mga
# Reports p-values for each comparison method:
# - Sarstedt (PLS-MGA)
# - Chin (parametric)
# - Permutation-based tests
# - Confidence interval overlap
```

---

## 9. Mediation Analysis

```r
model <- "
X =~ x_1 + x_2 + x_3
M =~ m_1 + m_2 + m_3
Y =~ y_1 + y_2 + y_3

Y ~ X + M
M ~ X
"

result <- csem(my_data, model, .resample_method = "bootstrap", .R = 5000, .seed = 123)

# Indirect effects
infer_result <- infer(result)
infer_result$Indirect_effect   # specific indirect effects with CIs
infer_result$Total_effect      # total effects

# The indirect effect X -> M -> Y is automatically computed
# Check if CI excludes 0 for significance
```

---

## 10. Complete Workflow Example

```r
library(cSEM)

# --- 1. Define model ---
model <- "
# Measurement model
Quality      =~ qual_1 + qual_2 + qual_3 + qual_4 + qual_5
Value        <~ val_1 + val_2 + val_3
Satisfaction =~ sat_1 + sat_2 + sat_3 + sat_4
Loyalty      =~ loy_1 + loy_2 + loy_3

# Structural model
Satisfaction ~ Quality + Value
Loyalty      ~ Satisfaction
"

# --- 2. Estimate ---
result <- csem(
  .data = my_data,
  .model = model,
  .resample_method = "bootstrap",
  .R = 10000,
  .seed = 42
)

# --- 3. Summarize ---
s <- summarize(result)
s

# --- 4. Assess measurement model ---
a <- assess(result)
a$AVE             # Convergent validity
a$Reliability     # Internal consistency (alpha, rho_C, rho_A)
a$HTMT            # Discriminant validity
a$VIF_modeB       # Formative VIF

# --- 5. Inference ---
inf <- infer(result)
inf$Path_estimates       # path coefficients with CIs
inf$Loading_estimates    # loadings with CIs
inf$Weight_estimates     # weights with CIs

# --- 6. Structural model ---
a$R2              # R-squared
a$R2_adj          # Adjusted R-squared
a$F2              # Effect sizes
a$VIF             # Structural VIF

# --- 7. Model fit (CCA) --- NOT RECOMMENDED; use PLSpredict/CVPAT instead
# fit <- testOMF(result, .R = 5000, .seed = 42)

# --- 8. Prediction ---
pred <- predict(result, .cv_folds = 10, .r = 10)
pred$Prediction_metrics

# --- 9. MGA (if applicable) ---
# result_group <- csem(my_data, model, .id = "gender",
#                      .resample_method = "bootstrap", .R = 5000, .seed = 42)
# micom <- testMICOM(result_group, .R = 5000, .seed = 42)
# mga <- testMGD(result_group, .R_permutation = 5000, .seed = 42)
```

---

## Key Differences from SEMinR

| Feature | cSEM | SEMinR |
|---|---|---|
| Model syntax | lavaan-style text | R functions |
| PLSc | Auto for `=~` constructs | Explicit `PLSc()` call |
| CCA / Model fit | `testOMF()` available (not recommended) | Not available (not recommended) |
| MGA / MICOM | `testMICOM()`, `testMGD()` built-in | Not built-in |
| Prediction | `predict()` | `predict_pls()` with CVPAT |
| CVPAT | `testCVPAT()` built-in | Available |
| IPMA | `doIPMA()` built-in | Built-in |
| Assessment | `assess()` — comprehensive | `summary()` plus manual extraction |
| GSCA support | Yes | No |

---

## Tips and Common Issues

- **Formative vs reflective syntax**: `<~` for formative, `=~` for reflective — mixing them up changes the estimation fundamentally
- **PLSc auto-detection**: cSEM automatically applies PLSc when all constructs use `=~`; to force standard PLS, set `.disattenuate = FALSE`
- **Group variable**: Specify via `.id` in `csem()` (not `.group_var`). Must be a character or factor column in the data; does not need to be in the model syntax
- **Speed**: Bootstrapping in cSEM can be slower than SEMinR for complex models; reduce `.R` during exploration
- **Model syntax errors**: Check for typos in indicator names; cSEM's error messages can be cryptic for syntax issues
