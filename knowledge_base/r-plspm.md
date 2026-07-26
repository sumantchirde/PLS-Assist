# plspm — Complete Workflow Guide

## Overview

**plspm** (Partial Least Squares Path Modeling) is one of the earliest R packages for PLS-SEM. It uses adjacency matrix-based model specification and provides core PLS-PM functionality. While less actively maintained than seminr or cSEM, it remains useful for simple models, teaching, and legacy codebases.

**Installation**:
```r
install.packages("plspm")
library(plspm)
```

**Limitations compared to seminr/cSEM**:
- No built-in PLSc
- No PLSpredict or CVPAT
- No CCA / model fit assessment (CCA not recommended anyway)
- No built-in MGA or MICOM
- Limited higher-order construct support
- Less active development

---

## 1. Model Specification

plspm uses three components for model specification:
1. **Path matrix**: An adjacency matrix defining structural relationships
2. **Blocks**: A list of vectors specifying which indicators belong to each construct
3. **Modes**: A character vector specifying Mode A (reflective) or Mode B (formative) for each construct

### Path Matrix

```r
# Define constructs and their relationships
# Rows = "from" (causes), Columns = "to" (effects)
# 1 = path exists, 0 = no path

# Example: Quality -> Satisfaction, Value -> Satisfaction, Satisfaction -> Loyalty
Quality      <- c(0, 0, 0, 0)
Value        <- c(0, 0, 0, 0)
Satisfaction <- c(1, 1, 0, 0)
Loyalty      <- c(0, 0, 1, 0)

path_matrix <- rbind(Quality, Value, Satisfaction, Loyalty)
colnames(path_matrix) <- rownames(path_matrix)

# Verify
path_matrix
#              Quality Value Satisfaction Loyalty
# Quality            0     0            0       0
# Value              0     0            0       0
# Satisfaction       1     1            0       0
# Loyalty            0     0            1       0
```

**Important**: The matrix encodes "this row variable receives a path from the column variable." Specifically, a 1 in row i, column j means "construct j predicts construct i." The row and column ordering must match.

### Alternative path matrix construction:

```r
# Using a more intuitive approach
path_matrix <- matrix(
  c(0, 0, 0, 0,
    0, 0, 0, 0,
    1, 1, 0, 0,
    0, 0, 1, 0),
  nrow = 4, ncol = 4, byrow = TRUE,
  dimnames = list(
    c("Quality", "Value", "Satisfaction", "Loyalty"),
    c("Quality", "Value", "Satisfaction", "Loyalty")
  )
)
```

### Indicator Blocks

```r
# List of indicator column indices or names for each construct
# Order must match path_matrix row/column order

blocks <- list(
  Quality      = c("qual_1", "qual_2", "qual_3", "qual_4", "qual_5"),
  Value        = c("val_1", "val_2", "val_3"),
  Satisfaction = c("sat_1", "sat_2", "sat_3", "sat_4"),
  Loyalty      = c("loy_1", "loy_2", "loy_3")
)

# Alternatively, using column indices:
blocks <- list(
  c(1, 2, 3, 4, 5),    # Quality: columns 1-5
  c(6, 7, 8),           # Value: columns 6-8
  c(9, 10, 11, 12),     # Satisfaction: columns 9-12
  c(13, 14, 15)         # Loyalty: columns 13-15
)
```

### Measurement Modes

```r
# "A" = reflective (Mode A), "B" = formative (Mode B)
modes <- c("A", "A", "A", "A")  # all reflective

# With a formative construct:
modes <- c("A", "B", "A", "A")  # Value is formative
```

---

## 2. Model Estimation

```r
result <- plspm(
  Data      = my_data,
  path_matrix = path_matrix,
  blocks    = blocks,
  modes     = modes,
  scheme    = "centroid",     # "centroid" (default), "path", "factorial"
  scaled    = TRUE,          # standardize indicators
  tol       = 1e-06,         # convergence tolerance
  maxiter   = 100,           # max iterations
  boot.val  = FALSE          # set TRUE for bootstrapping (see below)
)
```

### Accessing Results

```r
# Summary
summary(result)

# Path coefficients (structural model)
result$path_coefs

# Inner model (regression results for each endogenous construct)
result$inner_model
# Each element contains: Estimate, Std. Error, t value, Pr(>|t|)

# Outer model (loadings/weights)
result$outer_model
# Contains: name, block, weight, loading, communality, redundancy for each indicator

# Construct scores
result$scores

# R-squared
result$inner_summary
# Contains: Type, R2, Block_Communality, Mean_Redundancy, AVE

# Unidimensionality (reliability)
result$unidim
# Contains: Mode, MVs, C.alpha, DG.rho, eig.1st, eig.2nd
```

---

## 3. Bootstrapping

```r
result_boot <- plspm(
  Data        = my_data,
  path_matrix = path_matrix,
  blocks      = blocks,
  modes       = modes,
  scheme      = "centroid",
  boot.val    = TRUE,
  br          = 5000    # number of bootstrap subsamples
)

# Bootstrap results for path coefficients
result_boot$boot

# Contains:
result_boot$boot$paths     # bootstrapped path coefficients
result_boot$boot$rsq       # bootstrapped R²
result_boot$boot$total.efs # bootstrapped total effects
```

### Interpreting Bootstrap Output

The `$boot$paths` contains:
- Original: Original path estimate
- Mean.Boot: Mean of bootstrap estimates
- Std.Error: Standard error
- perc.025: 2.5th percentile (lower CI)
- perc.975: 97.5th percentile (upper CI)

---

## 4. Measurement Model Assessment

### Reflective Constructs

```r
# Outer loadings
result$outer_model
# Look for 'loading' column

# Internal consistency
result$unidim
# C.alpha = Cronbach's alpha
# DG.rho  = Dillon-Goldstein rho (≈ composite reliability)
# eig.1st, eig.2nd = eigenvalues (first should dominate)

# AVE
result$inner_summary$AVE

# Cross-loadings (discriminant validity check)
result$crossloadings
```

### Formative Constructs (Mode B)

```r
# Outer weights
result$outer_model
# For Mode B constructs, look at 'weight' column

# VIF is not directly provided by plspm
# Compute manually:
library(car)
formative_data <- my_data[, blocks$Value]
vif_values <- sapply(1:ncol(formative_data), function(i) {
  formula <- as.formula(paste(names(formative_data)[i], "~ ."))
  1 / (1 - summary(lm(formula, data = formative_data))$r.squared)
})
names(vif_values) <- names(formative_data)
vif_values
```

### HTMT (Not Built-in)

plspm does not compute HTMT natively. Compute manually:

```r
# Manual HTMT computation
compute_htmt <- function(data, blocks) {
  n_constructs <- length(blocks)
  construct_names <- names(blocks)
  htmt_matrix <- matrix(NA, n_constructs, n_constructs,
                         dimnames = list(construct_names, construct_names))

  for (i in 1:(n_constructs - 1)) {
    for (j in (i + 1):n_constructs) {
      items_i <- blocks[[i]]
      items_j <- blocks[[j]]

      # Between-construct correlations (heterotrait)
      het_cors <- abs(cor(data[, items_i], data[, items_j]))
      mean_het <- mean(het_cors)

      # Within-construct correlations (monotrait)
      if (length(items_i) > 1) {
        mono_i <- cor(data[, items_i])
        mono_i_vals <- abs(mono_i[upper.tri(mono_i)])
        mean_mono_i <- mean(mono_i_vals)
      } else {
        mean_mono_i <- 1
      }

      if (length(items_j) > 1) {
        mono_j <- cor(data[, items_j])
        mono_j_vals <- abs(mono_j[upper.tri(mono_j)])
        mean_mono_j <- mean(mono_j_vals)
      } else {
        mean_mono_j <- 1
      }

      htmt_matrix[j, i] <- mean_het / sqrt(mean_mono_i * mean_mono_j)
    }
  }
  return(htmt_matrix)
}

htmt <- compute_htmt(my_data, blocks)
htmt
```

---

## 5. Structural Model Assessment

### Path Coefficients

```r
# Path coefficients
result$path_coefs

# Detailed regression results per endogenous construct
result$inner_model
# For each endogenous construct: Estimate, Std. Error, t value, Pr(>|t|)
```

### R²

```r
# R-squared for endogenous constructs
result$inner_summary[, "R2"]
```

### Effect Size (f²)

plspm does not compute f² directly. Compute manually:

```r
# Manual f² computation
# Run the full model and a model without each predictor
compute_f2 <- function(full_r2, reduced_r2) {
  (full_r2 - reduced_r2) / (1 - full_r2)
}

# Example: f² for Quality -> Satisfaction
# Full model R² for Satisfaction
r2_full <- result$inner_summary["Satisfaction", "R2"]

# Re-estimate without Quality -> Satisfaction path
path_matrix_reduced <- path_matrix
path_matrix_reduced["Satisfaction", "Quality"] <- 0
result_reduced <- plspm(my_data, path_matrix_reduced, blocks, modes)
r2_reduced <- result_reduced$inner_summary["Satisfaction", "R2"]

f2_quality <- compute_f2(r2_full, r2_reduced)
f2_quality
```

### Total Effects

```r
# Direct and indirect effects
result$effects
# Contains: relationships, direct, indirect, total
```

---

## 6. Visualization

```r
# Plot the path model
plot(result)

# Plot outer model (loadings)
plot(result, what = "loadings")

# Plot inner model (path coefficients)
plot(result, what = "inner")
```

### Custom Visualization with Graphing

```r
# plspm provides basic plots; for publication-quality figures,
# extract coefficients and use ggplot2 or DiagrammeR

# Extract path coefficients for custom plotting
paths_df <- data.frame(
  from = character(),
  to = character(),
  coefficient = numeric(),
  stringsAsFactors = FALSE
)

for (i in 1:nrow(path_matrix)) {
  for (j in 1:ncol(path_matrix)) {
    if (path_matrix[i, j] == 1) {
      paths_df <- rbind(paths_df, data.frame(
        from = colnames(path_matrix)[j],
        to = rownames(path_matrix)[i],
        coefficient = result$path_coefs[i, j]
      ))
    }
  }
}
paths_df
```

---

## 7. Complete Workflow Example

```r
library(plspm)

# --- 1. Define path matrix ---
Quality      <- c(0, 0, 0, 0)
Value        <- c(0, 0, 0, 0)
Satisfaction <- c(1, 1, 0, 0)
Loyalty      <- c(0, 0, 1, 0)

path_matrix <- rbind(Quality, Value, Satisfaction, Loyalty)
colnames(path_matrix) <- rownames(path_matrix)

# --- 2. Define indicator blocks ---
blocks <- list(
  Quality      = c("qual_1", "qual_2", "qual_3", "qual_4", "qual_5"),
  Value        = c("val_1", "val_2", "val_3"),
  Satisfaction = c("sat_1", "sat_2", "sat_3", "sat_4"),
  Loyalty      = c("loy_1", "loy_2", "loy_3")
)

# --- 3. Define modes ---
modes <- c("A", "B", "A", "A")  # Value is formative

# --- 4. Estimate with bootstrapping ---
result <- plspm(
  Data = my_data,
  path_matrix = path_matrix,
  blocks = blocks,
  modes = modes,
  scheme = "centroid",
  scaled = TRUE,
  boot.val = TRUE,
  br = 5000
)

# --- 5. Review results ---
summary(result)

# --- 6. Measurement model ---
# Loadings
result$outer_model

# Reliability
result$unidim

# AVE
result$inner_summary[, "AVE"]

# Cross-loadings
result$crossloadings

# --- 7. Structural model ---
# Path coefficients
result$path_coefs

# Detailed inner model results
result$inner_model

# R²
result$inner_summary[, "R2"]

# Bootstrap results
result$boot$paths

# Total effects
result$effects

# --- 8. Visualize ---
plot(result)
```

---

## 8. Mediation Analysis in plspm

plspm provides indirect effects through `$effects`:

```r
# Model with mediation: X -> M -> Y, and X -> Y
X <- c(0, 0, 0)
M <- c(1, 0, 0)
Y <- c(1, 1, 0)

path_matrix_med <- rbind(X, M, Y)
colnames(path_matrix_med) <- rownames(path_matrix_med)

blocks_med <- list(
  X = c("x_1", "x_2", "x_3"),
  M = c("m_1", "m_2", "m_3"),
  Y = c("y_1", "y_2", "y_3")
)

modes_med <- c("A", "A", "A")

result_med <- plspm(my_data, path_matrix_med, blocks_med, modes_med, boot.val = TRUE, br = 5000)

# Direct, indirect, and total effects
result_med$effects
# Indirect effect = a * b (for X -> M -> Y)

# For significance: use bootstrap results
result_med$boot$paths
# The indirect effect significance must be assessed manually from bootstrap distributions
```

---

## When to Use plspm vs. Alternatives

| Scenario | Recommendation |
|---|---|
| Simple PLS-PM model, teaching | plspm is adequate |
| Need PLSc, HTMT, or modern criteria | Use seminr or cSEM |
| Need PLSpredict / CVPAT | Use seminr |
| Need CCA / model fit | CCA not recommended; use PLSpredict/CVPAT in seminr instead |
| Need MGA / MICOM | Use cSEM |
| Legacy code compatibility | plspm |
| Publication-ready analysis | seminr or cSEM preferred |

---

## Tips and Common Issues

- **Path matrix direction**: The most common error is getting the path matrix direction wrong. Remember: `path_matrix[i, j] = 1` means "construct j predicts construct i" (j → i)
- **Block ordering**: The order of blocks, modes, and path_matrix rows/columns must all match exactly
- **Missing data**: plspm does not handle missing data internally; preprocess missing values before estimation
- **Indicator names**: Use column names (strings) rather than indices for clarity and robustness
- **No PLSc**: If consistent estimates are needed, use seminr or cSEM instead
- **Scale direction**: Ensure all indicators are coded in the same direction (reverse-code as needed before analysis)
