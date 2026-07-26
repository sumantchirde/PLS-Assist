# Structural Model Assessment — Detailed Guide

## Prerequisites

**Only proceed to structural model assessment after the measurement model has been established.** If reflective or formative measurement model criteria are not met, fix measurement issues first. Structural path coefficients are meaningless if the constructs they connect are poorly measured.

---

## Sample Size Determination

Adequate sample size is critical for reliable PLS-SEM estimation. The outdated "10-times rule" (10× the maximum number of arrows pointing at any construct) provides only a rough lower bound and frequently underestimates required sample sizes.

### Recommended Approaches

#### 1. Power Analysis (Preferred)

Use a priori power analysis to determine the minimum sample size needed to detect effects of a given size at a specified significance level.

**Using G*Power or equivalent**:
- Specify the maximum number of predictors for any endogenous construct
- Set minimum effect size (f² = 0.02 for small, 0.15 for medium, 0.35 for large)
- Set significance level (α = 0.05) and power (1 − β = 0.80, or 0.90 for conservative)
- Use "F tests → Linear multiple regression: Fixed model, R² increase" in G*Power
- The resulting sample size ensures adequate power for the most complex regression in the model

**Rule of thumb from power analysis** (Hair et al., 2022):
- To detect R² ≥ 0.10 at α = 0.05, power = 0.80: n ≈ 90–100 for models with ≤ 5 predictors
- To detect R² ≥ 0.25: n ≈ 40–50 for ≤ 5 predictors
- To detect small effects (f² = 0.02): n ≈ 400+ depending on complexity

#### 2. Inverse Square Root Method (Kock & Hadaya, 2018)

A quick formula-based approach when path coefficients are anticipated:

**Formula**: n_min > (z_α / |p_min|)² where p_min is the minimum absolute expected path coefficient and z_α is the critical z-value (1.96 for α = 0.05, 2.486 for two-tailed at α ≈ 0.01).

**At α = 0.05 (two-tailed)**: n_min > (1.96 / |p_min|)²

| Expected minimum |β| | Minimum n (α = 0.05) |
|---|---|
| 0.30 | 43 |
| 0.20 | 97 |
| 0.15 | 171 |
| 0.10 | 385 |
| 0.05 | 1,537 |

#### 3. The "10-Times Rule" (Legacy — Use with Caution)

n ≥ 10 × max(number of indicators for any formative construct, number of paths pointing at any endogenous construct). **This is an absolute minimum floor, not a recommendation.** Power analysis or inverse square root should be used instead.

### Sample Size for Specific Analyses

- **Bootstrapping**: Requires at least 5,000 (ideally 10,000) subsamples, but the original sample size determines the quality of bootstrap estimates. Bootstrapping does not compensate for small samples.
- **PLSpredict**: k-fold cross-validation requires sufficient observations per fold (minimum ~30–50 per fold with k = 10)
- **CVPAT**: Power analysis specific to CVPAT shows that detecting predictive differences between PLS and LM benchmarks requires larger samples when differences are small (Liengaard et al., 2021; Sharma et al., 2023)
- **FIMIX-PLS**: Each segment should contain ≥ 50 observations (or 10× the most complex regression); total sample must support the intended number of segments
- **MGA**: Each group should have ≥ 50–100 observations for stable path estimates

### Key References
- Kock, N. & Hadaya, P. (2018). Minimum Sample Size Estimation in PLS-SEM: The Inverse Square Root and Gamma-Exponential Methods. *ISJ*, 28(1), 227–261.
- Hair, J.F., Hult, G.T.M., Ringle, C.M. & Sarstedt, M. (2022). *A Primer on Partial Least Squares Structural Equation Modeling (PLS-SEM)*, 3rd ed. Sage.
- Cohen, J. (1992). A Power Primer. *Psychological Bulletin*, 112(1), 155–159.

---

## Step-by-Step Assessment Procedure

### Step 1: Collinearity Among Predictor Constructs

**Why**: High collinearity among predictor constructs inflates standard errors and biases path coefficient estimates (similar to multicollinearity in regression).

**Metric**: Variance Inflation Factor (VIF) for each set of predictor constructs targeting a given endogenous construct.

**Thresholds**:
- VIF < 3: No concern
- 3 ≤ VIF < 5: Potential concern; inspect
- VIF ≥ 5: Problematic; remedial action needed

**Remedies**:
- Merge highly correlated predictors into a higher-order construct
- Remove one of the collinear predictors (if theoretically justified)
- Create a composite predictor
- Use PLS-SEM's inherent handling (less affected than OLS, but still biased)

**Note**: Structural VIF is computed among the constructs predicting each endogenous variable, not among indicators. This is separate from the formative indicator VIF in measurement model assessment.

---

### Step 2: Path Coefficients (Significance and Relevance)

**What**: Standardized regression coefficients representing the strength and direction of relationships between constructs in the inner model.

**Estimation**: OLS regression of endogenous construct scores on their predictor construct scores.

**Significance testing**:
- **Bootstrapping**: ≥ 5,000 subsamples (10,000 for publication)
- **Confidence intervals**: Percentile CI as default; BCa (bias-corrected and accelerated) when bootstrap distributions are highly asymmetric (Becker et al., 2023)
- **Report**: Path coefficient (β), standard error, t-value, p-value, and 95% CI
- A path is significant if p < 0.05 (or the CI does not include 0)

**Relevance assessment**:
- Statistical significance alone is insufficient — effect must be practically meaningful
- Consider the magnitude of the coefficient relative to other paths
- Paths < 0.10 are often trivially small even if significant (in large samples)
- Domain knowledge should guide interpretation of "meaningful" effect sizes

**Interpreting signs**:
- Positive β: As predictor increases, outcome increases
- Negative β: As predictor increases, outcome decreases
- Unexpected signs may indicate suppression effects, specification errors, or collinearity

**Standardized vs. unstandardized**:
- PLS-SEM typically reports standardized coefficients (β)
- For IPMA, unstandardized total effects are needed
- For comparing groups in MGA, use the same metric (typically standardized)

---

### Step 3: Coefficient of Determination (R²)

**What**: The proportion of variance in an endogenous construct explained by its predictors.

**Thresholds** (Hair et al., 2011 — discipline-dependent):
- R² ≈ 0.25: Weak
- R² ≈ 0.50: Moderate
- R² ≈ 0.75: Substantial

**Contextual interpretation**:
- In consumer behavior/marketing: R² ≈ 0.20 may be acceptable
- In technology adoption (TAM): R² > 0.40 is typical
- In tightly controlled experimental designs: R² > 0.60 expected
- Always compare to field norms and prior studies

**Adjusted R²**: Accounts for the number of predictors. Use when comparing models with different numbers of exogenous constructs. Adjusted R² = 1 − [(1 − R²)(n − 1) / (n − k − 1)] where n = sample size, k = number of predictors.

**Reporting**: Report R² and adjusted R² for all endogenous constructs. Include in the structural model results table.

---

### Step 4: Effect Size (f²)

**What**: The contribution of a specific exogenous construct to the R² of an endogenous construct. Measures the change in R² when a predictor is omitted.

**Formula**: f² = (R²_included − R²_excluded) / (1 − R²_included)

Where:
- R²_included: R² of the endogenous construct when the predictor is included
- R²_excluded: R² when the predictor is removed from the model

**Thresholds** (Cohen, 1988):
- f² ≈ 0.02: Small effect
- f² ≈ 0.15: Medium effect
- f² ≈ 0.35: Large effect
- f² < 0.02: No practical effect

**Important notes**:
- f² values close to 0 can still be significant in large samples — interpret substantively
- f² is computed for each exogenous → endogenous relationship individually
- In PLS-SEM, most software computes f² automatically (SEMinR, SmartPLS)
- f² can be negative in rare cases due to suppression effects — report but flag

**Common mistakes**:
- Ignoring f² when paths are significant (a significant but trivially small effect is not meaningful)
- Not reporting f² at all (required by most PLS-SEM reporting guidelines)
- Computing f² manually incorrectly (ensure the model is re-estimated, not just the R² recalculated)

---

### Step 5: Predictive Relevance (Q²) — Blindfolding

**What**: Stone-Geisser's Q² assesses the model's out-of-sample predictive relevance using a blindfolding procedure.

**Procedure**:
1. Systematically omit a portion of the data matrix (omission distance D)
2. Re-estimate the model using the remaining data
3. Use the estimates to predict the omitted values
4. Compare predictions to actual values

**Omission distance (D)**:
- Typically D = 7 (default in most software)
- D must not be a divisor of sample size n
- Values between 5 and 10 are acceptable

**Thresholds**:
- Q² > 0: The model has predictive relevance (better than trivially predicting the mean)
- 0 < Q² ≤ 0.25: Small predictive relevance
- 0.25 < Q² ≤ 0.50: Medium predictive relevance
- Q² > 0.50: Large predictive relevance

**Types of Q²**:
- **Cross-validated redundancy (Q²_predict)**: Uses structural model estimates (path coefficients) to predict — preferred; tests the full model
- **Cross-validated communality**: Uses only measurement model — tests measurement model prediction

**Common mistakes**:
- Choosing D that divides sample size (creates systematic patterns)
- Using cross-validated communality instead of cross-validated redundancy
- Not reporting Q² for all endogenous constructs

---

### Step 6: PLSpredict (Out-of-Sample Prediction)

**What**: A holdout sample-based procedure for assessing the model's predictive power (Shmueli et al., 2019). Unlike blindfolding Q², PLSpredict uses a proper training/test split with k-fold cross-validation.

**Procedure**:
1. Divide data into k folds (typically k = 10)
2. For each fold: train the model on k−1 folds, predict the holdout fold
3. Compute prediction error metrics (RMSE, MAE) for each endogenous indicator
4. Compare PLS model predictions against two benchmarks:
   - **LM (linear model)**: Regression of indicators on all exogenous indicators directly
   - **Mean**: Naive prediction using the training sample mean

**Interpretation** (indicator-level comparison of RMSE):

| Comparison | Interpretation |
|---|---|
| All indicators: PLS RMSE < LM RMSE | **High** predictive power |
| Majority of indicators: PLS RMSE < LM RMSE | **Medium** predictive power |
| Minority of indicators: PLS RMSE < LM RMSE | **Low** predictive power |
| No indicators: PLS RMSE < LM RMSE | **No** predictive power (model adds nothing beyond direct regression) |
| PLS RMSE > Mean RMSE | Model performs worse than naive mean prediction — serious concern |

**Decision tree**:
```
PLS RMSE vs. Mean RMSE?
├── PLS RMSE > Mean RMSE → Model fails; lacks basic predictive power
└── PLS RMSE ≤ Mean RMSE → Compare PLS RMSE vs. LM RMSE
    ├── All indicators: PLS < LM → High predictive power
    ├── Majority: PLS < LM → Medium predictive power
    ├── Minority: PLS < LM → Low predictive power
    └── None: PLS < LM → No predictive power beyond LM
```

**Additional considerations**:
- Use RMSE for symmetric loss; MAE for absolute loss interpretation
- Repeat with different random seeds to check stability
- Report prediction errors for each indicator, not just summaries
- Highly skewed indicators may show different results for RMSE vs MAE

**Key reference**: Shmueli, G. et al. (2019). Predictive Model Assessment in PLS-SEM: Guidelines for Using PLSpredict. *European Journal of Marketing*, 53(11), 2322–2347.

---

### Step 7: CVPAT (Cross-Validated Predictive Ability Test)

**What**: A formal statistical test for comparing the overall predictive ability of the PLS-SEM model against a benchmark (Liengaard et al., 2021). Unlike PLSpredict, which assesses indicator-by-indicator, CVPAT provides a single overall test.

**Procedure**:
1. Compute the average loss differential between the PLS model and a benchmark (LM or IA — indicator average)
2. Use a t-test on the average loss differentials across cross-validation folds
3. If the average loss differential is significantly negative → PLS model predicts better than the benchmark

**Benchmarks**:
- **IA benchmark**: Tests if the model predicts better than indicator averages (floor test — weakest counterfactual)
- **LM benchmark**: Tests if the structural model adds predictive value beyond direct indicator regression (conservative test). However, LM estimates more parameters than PLS from the same training data, creating an asymmetric overfitting disadvantage in finite samples.
- **PCR benchmark** (proposed): Extracts the same number of principal components as PLS composites, matching PLS's compression ratio. Tests whether the theory-driven block assignments contribute beyond generic dimensionality reduction.

**Prediction pipeline**: CVPAT predictions use the W × B × L^T pipeline: outer_weights → path_coef → outer_loadings → predicted indicators. When `reflective()` constructs are present, PLSc-corrected path_coef and outer_loadings are used. This means PLSc vs. standard PLS affects prediction results.

**Regularization entanglement**: "Strong predictive validity" (beating both IA and LM) may partly reflect regularization — the mechanical benefit of compressing many indicators into few composites — rather than genuine structural model contribution. The compression ratio (number of indicator predictors vs. composites) amplifies this effect. A bias correction based on the ratio of parameters to training observations can restore near-nominal false positive rates. The PCR benchmark separates regularization from structural contributions:
- If PLS ≈ PCR: predictive advantage is from regularization (common factor measurement)
- If PLS >> PCR: genuine structural contribution (composite/formative measurement)

**Interpretation**:
- Significant negative average loss → PLS model outperforms the benchmark
- Non-significant → No evidence that PLS model predicts better
- Significant positive → Benchmark outperforms PLS model

**When to use**:
- CVPAT provides an overall test; PLSpredict provides indicator-level detail
- Use both: CVPAT for the overall conclusion, PLSpredict for diagnostic detail
- CVPAT is available in SEMinR (`assess_cvpat()` in seminrExtras)

**Key references**:
- Liengaard, B.D. et al. (2021). Prediction: Coveted, Yet Forsaken? Introducing CVPAT in PLS Path Modeling. *Decision Sciences*, 53(2), 362–392.
- Sharma, P.N. et al. (2023). Predictive Model Assessment and Selection: Extensions and Guidelines for Using CVPAT. *European Journal of Marketing*, 57(6), 1662–1677.

---

### Step 7c: PCM (Predictive Contribution of the Mediator)

**What**: When the model includes mediation, PCM evaluates whether the mediating construct improves out-of-sample predictive accuracy beyond the direct antecedent alone (Danks, 2021). It compares predictions from the Direct Antecedents (DA) approach against the Earliest Antecedents (EA) approach on an isolated sub-model for each mediation path.

**Formula**: PCM = (METRIC_EA − METRIC_DA) / METRIC_EA, where METRIC is RMSE or MAE.

**Interpretation**: PCM < 0.05 = Weak, 0.05–0.10 = Moderate, > 0.10 = Strong. Negative values indicate the mediator damages predictive accuracy.

**When to use**: After establishing mediation significance via bootstrap indirect effects. PCM provides complementary predictive evidence that the added complexity of the mediator is justified by out-of-sample performance.

**Implementation**: `assess_pcm()` in seminrExtras. See `advanced-methods.md` § Mediation for the full procedure and decision tree.

**Key reference**: Danks, N.P. (2021). The Piggy in the Middle: The Role of Mediators in PLS-SEM Prediction. *The DATA BASE for Advances in Information Systems*, 52(SI), 24–42.

---

### Simulation Design Principles for PLS-SEM Monte Carlo Studies

**DGP-Estimator Alignment**: The estimator must match the data-generating process. This is the most critical design decision:
- **Common factor DGP** (indicators = λξ + ε): Use PLSc (`reflective()` in seminr). Standard PLS on common factor data conflates measurement philosophy with estimation artifact.
- **Composite DGP** (independent indicators, construct = weighted sum): Use standard PLS (`composite(mode_A)`). PLSc overcorrects when no attenuation exists.
- **Mixed DGP** (some constructs common factor, some composite): Use `reflective()` for common factor constructs and `composite()` for composite constructs within the same model.

This principle is endorsed by Sarstedt et al. (2016), Guenther et al. (2025), and is implemented in the BIC_sys and CVPAT simulation studies.

**Prediction procedure consistency**: When comparing PLS predictions against benchmarks (PCR, LM, IA), the PLS prediction must use the same pipeline as the assessment tool (e.g., `assess_cvpat()`). The standard pipeline is W × B × L^T: outer_weights → path_coef → outer_loadings → predicted indicators → unstandardize. Do NOT substitute with fresh OLS regression of indicators on composites, as this bypasses path_coef and outer_loadings (and therefore bypasses PLSc corrections).

**Terminology**: Keep DGP labels descriptive of the data generation ("common factor DGP", "composite DGP"). Use formative/reflective for the theoretical construct conceptualization. Use PLSc/PLS for the estimation method. Never equate "reflective = common factor" or "formative = composite" — these are conceptually distinct levels.

---

### Step 7b: Model Selection Criteria (When Comparing Competing Models)

When multiple structural model specifications are plausible, use information criteria to select the best model on predictive grounds (Sharma et al., 2021; Chin et al., 2020).

**Available criteria**:

| Criterion | What it penalizes | Tendency |
|---|---|---|
| **AIC** | # parameters (light penalty) | Favors more complex models |
| **BIC** | # parameters + sample size | Favors parsimony; **recommended** |
| **GM** (Geweke-Meese) | Geometric mean of BIC components | Similar to BIC; alternative diagnostic |

**Weighted variants** for model probability:
- **BICw** (BIC weights / Akaike weights from BIC): w_i = exp(−0.5 × ΔBIC_i) / Σ exp(−0.5 × ΔBIC_j)
- **GMw**: Analogous weights based on GM
- Weights sum to 1.0 across candidate models; each weight = probability that model i is the best model

**When to use**:
- Comparing nested or non-nested alternative structural models
- Evaluating whether adding/removing paths improves the model
- Quantifying mediation model selection uncertainty (see mediation section)
- **Do not rely solely on R² or Q²** for model comparison — they always favor more complex models

**Key references**:
- Sharma, P.N. et al. (2021). Prediction-oriented Model Selection in PLS Path Modeling. *Decision Sciences*, 52(3), 567–607.
- Chin, W.W. et al. (2020). Demystifying the Role of Causal-Predictive Modeling Using PLS-SEM. *IMDS*, 120(12), 2161–2209.

---

### Note on Model Fit (CCA)

CCA (Confirmatory Composite Analysis) using SRMR, d_ULS, and d_G is **not recommended** for PLS-SEM model assessment. These indices have limited power to detect specific misspecifications, fixed cutoffs borrowed from CB-SEM do not apply well to composites, and the approach remains contested in the literature. Focus instead on predictive assessment (PLSpredict, CVPAT) and substantive evaluation of path coefficients, effect sizes, and theory alignment.

---

## Summary: Complete Structural Assessment Checklist

| Step | What | Key Metric(s) | Threshold / Benchmark |
|---|---|---|---|
| 1 | Collinearity | VIF (predictor constructs) | < 5 (ideally < 3) |
| 2 | Path significance | β, t, p, 95% CI | p < 0.05; CI excludes 0 |
| 3 | Explanatory power | R² (adjusted R²) | 0.25 weak / 0.50 moderate / 0.75 substantial |
| 4 | Effect size | f² | 0.02 small / 0.15 medium / 0.35 large |
| 5 | Predictive relevance | Q² (blindfolding) | > 0 |
| 6 | Out-of-sample prediction | PLSpredict (RMSE vs. LM) | PLS < LM for majority of indicators |
| 7 | Overall prediction test | CVPAT | Significant negative avg. loss differential |
| 8 | Model fit (CCA) | Not recommended | Focus on PLSpredict/CVPAT instead |

---

## Additional Considerations

### Total Effects

- Total effect = direct effect + sum of all indirect effects (through mediators)
- Report total effects when mediation is present
- Used as the "importance" metric in IPMA

### Prediction vs. Explanation

PLS-SEM models should be assessed on both dimensions (Sarstedt & Danks, 2022; Shmueli et al., 2016):

- **Explanatory power**: R², f², path significance (how well does the model explain the data it was estimated on?)
- **Predictive power**: Q², PLSpredict, CVPAT (how well does the model predict new, unseen data?)
- A model can explain well but predict poorly (overfitting) or predict well but have weak explanatory paths
- Both should be reported for a complete evaluation

### Bootstrapping Best Practices (Structural Model)

- **Subsamples**: ≥ 5,000 (10,000 for publication)
- **CI type**: Percentile CI as default; BCa for highly asymmetric distributions (Becker et al., 2023)
- **Two-tailed vs. one-tailed**: Use two-tailed unless strong theoretical justification for directionality
- **Report**: Always include CIs (not just p-values); CIs convey effect size uncertainty
- **Complete bootstrapping**: Ensures valid inference for indirect effects, f², HTMT

---

## References

- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum.
- Hair, J.F., Ringle, C.M. & Sarstedt, M. (2011). PLS-SEM: Indeed a Silver Bullet. *JMTP*, 19(2), 139–152.
- Hair, J.F., Howard, M.C. & Nitzl, C. (2020). Assessing Measurement Model Quality Using CCA. *JBR*, 109, 101–110.
- Henseler, J. & Sarstedt, M. (2013). Goodness-of-Fit Indices for PLS Path Modeling. *Computational Statistics*, 28(2), 565–580.
- Liengaard, B.D. et al. (2021). Prediction: Coveted, Yet Forsaken? Introducing CVPAT. *Decision Sciences*, 53(2), 362–392.
- Sarstedt, M. & Danks, N.P. (2022). Prediction in HRM Research: A Gap Between Rhetoric and Reality. *HRMJ*, 32(2), 485–513.
- Sharma, P.N. et al. (2023). Extensions and Guidelines for Using CVPAT. *EJM*, 57(6), 1662–1677.
- Shmueli, G. et al. (2016). The Elephant in the Room. *JBR*, 69(10), 4552–4564.
- Shmueli, G. et al. (2019). Guidelines for Using PLSpredict. *EJM*, 53(11), 2322–2347.
