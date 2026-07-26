# PLS-SEM Reporting Guidelines

## Overview

This document provides publication-ready table templates and a checklist for reporting PLS-SEM results. Following these guidelines ensures compliance with the standards set by Hair et al. (2019), Becker et al. (2023), and journal editorial expectations.

---

## Essential Reporting Checklist

### Minimum Requirements for Any PLS-SEM Paper

- [ ] Sample size and characteristics
- [ ] Model specification (inner and outer model diagram)
- [ ] Software and version used (SEMinR, cSEM, SmartPLS, etc.)
- [ ] Algorithm settings (weighting scheme, convergence criterion, max iterations)
- [ ] Measurement model results (reflective and/or formative, as applicable)
- [ ] Discriminant validity (HTMT)
- [ ] Structural model results (paths, significance, R², f²)
- [ ] Bootstrapping details (number of subsamples, CI type)
- [ ] Predictive assessment (PLSpredict, CVPAT)
- [ ] Model diagram with path coefficients

### Additional (When Applicable)

- [ ] MICOM results (if MGA is conducted)
- [ ] MGA comparison results
- [ ] Mediation results (specific indirect effects, PCM per mediator)
- [ ] Moderation results (interaction effects, simple slopes plot)
- [ ] IPMA results (importance-performance map)
- [ ] NCA results (ceiling analysis)
- [ ] Robustness checks (endogeneity, FIMIX, nonlinear effects)
- [ ] ~~CCA / model fit~~ (not recommended; use PLSpredict/CVPAT instead)
- [ ] PLSc note (if consistent PLS was used)
- [ ] Epistemic rho (ρε) for formative constructs (especially when structural connections are few or weak)
- [ ] StablePLS comparison (if IC detected via ρε < 0.70)

---

## Table Templates

### Table 1: Reflective Measurement Model Results

| Construct | Indicator | Loading | CR (rho_c) | rho_A | AVE | Cronbach's alpha |
|---|---|---|---|---|---|---|
| Quality | qual_1 | 0.854 | 0.921 | 0.895 | 0.700 | 0.891 |
| | qual_2 | 0.831 | | | | |
| | qual_3 | 0.867 | | | | |
| | qual_4 | 0.798 | | | | |
| | qual_5 | 0.842 | | | | |
| Satisfaction | sat_1 | 0.891 | 0.938 | 0.916 | 0.791 | 0.912 |
| | sat_2 | 0.876 | | | | |
| | sat_3 | 0.905 | | | | |
| | sat_4 | 0.884 | | | | |
| Loyalty | loy_1 | 0.912 | 0.929 | 0.901 | 0.813 | 0.885 |
| | loy_2 | 0.897 | | | | |
| | loy_3 | 0.896 | | | | |

**Notes**: Loadings > 0.708; CR and rho_A between 0.70 and 0.90; AVE > 0.50.

---

### Table 2: Discriminant Validity — HTMT

| | Quality | Satisfaction | Loyalty |
|---|---|---|---|
| Quality | | | |
| Satisfaction | 0.782 | | |
| Loyalty | 0.654 | 0.831 | |

**Notes**: All HTMT values < 0.90. Bootstrap 95% percentile confidence intervals (not shown) do not include the threshold (0.85 or 0.90). Discriminant validity is established.

**Alternative: HTMT with confidence intervals**:

| Construct pair | HTMT | 95% CI |
|---|---|---|
| Quality ↔ Satisfaction | 0.782 | [0.714, 0.843] |
| Quality ↔ Loyalty | 0.654 | [0.572, 0.729] |
| Satisfaction ↔ Loyalty | 0.831 | [0.776, 0.882] |

---

### Table 3: Formative Measurement Model Results

| Construct | Indicator | Weight | t-value | p-value | 95% CI | Loading | VIF |
|---|---|---|---|---|---|---|---|
| Value | val_1 | 0.452 | 3.821 | <0.001 | [0.221, 0.684] | 0.823 | 1.542 |
| | val_2 | 0.387 | 2.956 | 0.003 | [0.131, 0.643] | 0.791 | 1.387 |
| | val_3 | 0.312 | 1.876 | 0.061 | [-0.014, 0.639] | 0.714 | 1.298 |

**Notes**: VIF values < 5 (no collinearity concern). val_3 weight is not significant (p = 0.061), but loading (0.714) exceeds 0.50, indicating absolute contribution; indicator retained. Redundancy analysis path coefficient = 0.78 (> 0.70 threshold).

---

### Table 4: Structural Model Results

| Path | Coefficient (β) | t-value | p-value | 95% CI | f² | Decision |
|---|---|---|---|---|---|---|
| Quality → Satisfaction | 0.423 | 6.892 | <0.001 | [0.302, 0.543] | 0.213 | Supported |
| Value → Satisfaction | 0.318 | 4.567 | <0.001 | [0.182, 0.455] | 0.121 | Supported |
| Satisfaction → Loyalty | 0.641 | 12.345 | <0.001 | [0.539, 0.743] | 0.698 | Supported |

**Notes**: 10,000 bootstrap subsamples; percentile confidence intervals; two-tailed tests.

---

### Table 5: Explanatory and Predictive Power

| Endogenous Construct | R² | Adjusted R² | Q² |
|---|---|---|---|
| Satisfaction | 0.523 | 0.519 | 0.387 |
| Loyalty | 0.411 | 0.409 | 0.312 |

**Notes**: R² values indicate moderate explanatory power. Q² > 0 for all endogenous constructs, confirming predictive relevance.

---

### Table 6: PLSpredict Results

| Indicator | PLS RMSE | PLS MAE | LM RMSE | LM MAE | PLS − LM (RMSE) |
|---|---|---|---|---|---|
| sat_1 | 0.891 | 0.687 | 0.923 | 0.712 | −0.032 |
| sat_2 | 0.876 | 0.671 | 0.901 | 0.695 | −0.025 |
| sat_3 | 0.912 | 0.702 | 0.945 | 0.731 | −0.033 |
| sat_4 | 0.898 | 0.691 | 0.918 | 0.709 | −0.020 |
| loy_1 | 0.945 | 0.734 | 0.967 | 0.752 | −0.022 |
| loy_2 | 0.932 | 0.721 | 0.941 | 0.728 | −0.009 |
| loy_3 | 0.958 | 0.741 | 0.952 | 0.737 | +0.006 |

**Interpretation**: 6 of 7 indicators (majority) show PLS RMSE < LM RMSE → **medium to high predictive power**. All PLS RMSE values are well below the naive mean RMSE (not shown), confirming basic predictive relevance.

**CVPAT**: Average loss differential = −0.021 (p = 0.003). The PLS model significantly outperforms the LM benchmark.

---

### Table 7: Mediation Results

| Mediation Path | Indirect Effect (a × b) | 95% CI | t-value | p-value | VAF | Type |
|---|---|---|---|---|---|---|
| Quality → Satisfaction → Loyalty | 0.271 | [0.186, 0.367] | 5.432 | <0.001 | 0.56 | Complementary partial |
| Value → Satisfaction → Loyalty | 0.204 | [0.112, 0.306] | 3.876 | <0.001 | 0.72 | Complementary partial |

**Notes**: Significance of indirect effects assessed via bootstrapping (10,000 subsamples, BCa CI). VAF = indirect effect / total effect. Both direct and indirect effects are significant and positive → complementary partial mediation.

### Table 7b: Predictive Contribution of the Mediator (PCM)

| Mediation Path | Indicator | RMSE (DA) | RMSE (EA) | PCM (RMSE) | Conclusion |
|---|---|---|---|---|---|
| Quality → Satisfaction → Loyalty | CUSL1 | 1.409 | 1.481 | 0.049 | Weak |
| Quality → Satisfaction → Loyalty | CUSL2 | 1.127 | 1.161 | 0.029 | Weak |
| Quality → Satisfaction → Loyalty | CUSL3 | 1.253 | 1.295 | 0.032 | Weak |
| Value → Satisfaction → Loyalty | CUSL1 | 2.361 | 2.419 | 0.024 | Weak |
| Value → Satisfaction → Loyalty | CUSL2 | 2.858 | 2.835 | −0.008 | Negative |
| Value → Satisfaction → Loyalty | CUSL3 | 1.677 | 1.883 | 0.109 | Strong |

**Notes**: PCM = (RMSE_EA − RMSE_DA) / RMSE_EA (Danks, 2021). Thresholds: < 0.05 weak, 0.05–0.10 moderate, > 0.10 strong. Negative values indicate the mediator damages prediction. Each path is evaluated on an isolated partial mediation sub-model. Report alongside Table 7 to provide complementary predictive evidence for mediation.

---

### Table 8: Moderation Results

| Interaction | Coefficient (β) | t-value | p-value | 95% CI | f² |
|---|---|---|---|---|---|
| Quality × Involvement → Satisfaction | 0.089 | 2.134 | 0.033 | [0.007, 0.171] | 0.018 |

**Notes**: Two-stage approach used. Involvement moderates the Quality → Satisfaction relationship (β = 0.089, p = 0.033). The small but significant f² (0.018) is typical for moderation effects. Simple slope analysis: at low Involvement (−1 SD), Quality → Satisfaction = 0.334; at high Involvement (+1 SD), Quality → Satisfaction = 0.512.

*(Include a simple slopes / interaction plot as a figure)*

---

### Table 9: MGA Results

**MICOM Assessment**:

| Composite | Step 2: Correlation (c) | 95% CI | Step 2 Result | Step 3: Mean Diff | Step 3: Var Diff | Step 3 Result |
|---|---|---|---|---|---|---|
| Quality | 0.998 | [0.997, 1.000] | Established | −0.051 | 0.032 | Established |
| Satisfaction | 0.999 | [0.998, 1.000] | Established | 0.187 | −0.089 | Not established |
| Loyalty | 0.997 | [0.995, 1.000] | Established | 0.234 | 0.112 | Not established |

**Notes**: Partial measurement invariance (Steps 1 + 2) established for all constructs. Comparison of path coefficients via MGA is valid.

**MGA Path Comparison**:

| Path | Group 1 (β) | Group 2 (β) | Difference | PLS-MGA p | Permutation p | Significant? |
|---|---|---|---|---|---|---|
| Quality → Satisfaction | 0.512 | 0.334 | 0.178 | 0.012 | 0.018 | Yes |
| Satisfaction → Loyalty | 0.623 | 0.658 | −0.035 | 0.387 | 0.412 | No |

---

### Table 10: IPMA Results (Construct Level)

| Construct | Importance (Total Effect) | Performance (0–100) |
|---|---|---|
| Quality | 0.423 | 62.4 |
| Value | 0.318 | 71.2 |
| Satisfaction | 0.641 | 55.8 |

**Target construct**: Loyalty. Quality has moderate importance but relatively low performance → priority area for improvement. *(Include IPMA map as a figure)*

---

### Table 11: NCA Results

| Predictor → Outcome | Effect Size (d) | p-value (permutation) | Necessary? |
|---|---|---|---|
| Quality → Loyalty | 0.234 | 0.003 | Yes |
| Value → Loyalty | 0.087 | 0.142 | No |
| Satisfaction → Loyalty | 0.312 | <0.001 | Yes |

**Notes**: CE-FDH ceiling line. Effect size ≥ 0.1 considered meaningful. Quality and Satisfaction are necessary conditions for Loyalty; Value is not.

**Bottleneck Table** (for Quality → Loyalty):

| Loyalty Level (%) | Minimum Quality Required (%) |
|---|---|
| 50 | 32 |
| 60 | 41 |
| 70 | 53 |
| 80 | 67 |
| 90 | 79 |

---

### Table 12: Epistemic Reliability (ρε) Results

| Construct | Mode | ρε (Standard PLS) | ρε (StablePLS) | Bootstrap 5th %ile | Δρε (Sensitivity) | Epistemic? |
|---|---|---|---|---|---|---|
| Quality | A | 0.987 | 0.991 | 0.978 | 0.004 | Yes |
| Value | B | 0.723 | 0.891 | 0.712 | 0.168 | Yes (with StablePLS) |
| Satisfaction | A | 0.951 | 0.964 | 0.932 | 0.013 | Yes |
| Loyalty | A | 0.968 | 0.975 | 0.951 | 0.007 | Yes |

**Notes**: ρε = |cor(η_PLS, PC1)| measures whether each construct is dominated by its own indicators. Threshold: ρε ≥ 0.70. Bootstrap test: H₀ is confounding (ρε < 0.70); rejected if 5th percentile > 0.70. Sensitivity (Δρε) compares ρε across model specifications; values > 0.15 indicate IC vulnerability. Value shows IC under standard PLS (Δρε = 0.168 > 0.15), corrected by StablePLS.

---

### Table 13: Robustness Check Summary

| Check | Method | Result |
|---|---|---|
| Nonlinear effects | Quadratic terms | No significant quadratic effects |
| Endogeneity | Gaussian copula | No evidence of endogeneity (copula terms n.s.) |
| Unobserved heterogeneity | FIMIX-PLS (K = 1–4) | BIC favors K = 1; no evidence of segments |
| Measurement model | PLSc comparison | Results consistent with standard PLS |

---

## Figure Guidelines

### Figure 1: Path Model Diagram

Must include:
- All constructs (rectangles or ovals)
- Indicators connected to constructs (with measurement model type indicated)
- Structural paths with coefficients (β) and significance indicators (*, **, ***)
- R² values inside endogenous constructs
- Significance legend (e.g., * p < 0.05, ** p < 0.01, *** p < 0.001)

### Figure 2: IPMA Map (if applicable)
- X-axis: Importance (total effect)
- Y-axis: Performance (rescaled 0–100)
- Each construct as a labeled point
- Quadrant lines at the mean or median of each axis

### Figure 3: Interaction Plot (if moderation tested)
- X-axis: Independent variable
- Y-axis: Dependent variable
- Lines for moderator at −1 SD, mean, +1 SD
- Legend indicating moderator levels

---

## Methodology Section Template

When describing the PLS-SEM methodology in a paper, include:

### Sample and Data Collection
- Describe the sample (size, characteristics, sampling method)
- Response rate and missing data treatment
- Scale sources and adaptation

### Analytical Approach
> "We employed Partial Least Squares Structural Equation Modeling (PLS-SEM) using [software/package] version [X] to test our hypotheses. PLS-SEM was chosen because [justification — e.g., the model includes formative constructs, the research goal emphasizes prediction, the model is complex]. We followed the two-stage analytical approach recommended by Hair et al. (2019): first assessing the measurement model, then evaluating the structural model."

### Algorithm Settings
> "We used the path weighting scheme with a maximum of 300 iterations and a convergence criterion of 10⁻⁷. Significance was assessed using bootstrapping with 10,000 subsamples and percentile confidence intervals (Becker et al., 2023).""

### If PLSc Was Used
> "Since all constructs in our model are reflective, we applied consistent PLS (PLSc; Dijkstra & Henseler, 2015) to obtain consistent parameter estimates comparable to those of covariance-based SEM."

---

## Practice-Gap Statistics (Sarstedt et al., 2022)

A review of 239 PLS-SEM studies (486 models) in top 30 marketing journals (2011–2020) reveals persistent gaps between best practices and actual reporting:

### Reflective Measurement Model

| Criterion | Reporting Rate | Notes |
|---|---|---|
| Indicator loadings | 81.42% | Up from 61.81% (1981–2010) |
| Internal consistency (any metric) | 80.59% | |
| — Cronbach's alpha & CR (ρ_c) | 39.67% | Most common combination |
| — CR only | 27.56% | |
| — rho_A reported | 2.51% | **Very low despite being recommended** |
| — All three (alpha, CR, rho_A) | 1.88% | Best practice rarely followed |
| AVE | 77.45% | Up from 57.48% |
| Discriminant validity assessed | 71.61% | |
| — HTMT (any form) | 15.66% | **Far too low — should be standard** |
| — Fornell-Larcker only | 36.74% | Outdated as sole criterion |
| — HTMT with bootstrap CI | 2.56% | Best practice rarely followed |

### Formative Measurement Model

| Criterion | Reporting Rate | Notes |
|---|---|---|
| Reflective criteria incorrectly applied | 8.93% | Down from 23.08% — improvement |
| Collinearity (VIF) assessed | 47.32% | Should be routine |
| Redundancy analysis | 5.36% | **Critically underreported** |
| Indicator weights reported | 66.07% | |
| Significance of weights | 32.14% | |
| CTA-PLS used | 2.51% | Almost never used |

### Structural Model

| Criterion | Reporting Rate | Notes |
|---|---|---|
| Path coefficients | 98.77% | Near-universal |
| Significance via bootstrapping | 86.12% | |
| Confidence intervals reported | 11.11% | **Should be routine alongside p-values** |
| f² effect size | 17.70% | Up from 5.14% but still far too low |
| R² | 88.48% | Standard |
| Q² (blindfolding) | 33.33% | Up from 16.40% |
| PLSpredict | 4.73% | **Very low — should be standard** |
| SRMR / model fit | 8.23% | |
| FIMIX / heterogeneity | 4.18% | |
| Model comparison (BIC, GM) | 4.18% | Almost never done |

### MGA and Advanced Methods

| Criterion | Reporting Rate | Notes |
|---|---|---|
| Observed heterogeneity considered | 48.12% | |
| MICOM before MGA | 21% (12 of 57) | **Measurement invariance skipped in ~79% of MGA studies** |
| Higher-order constructs | 29.71% of studies | But only 8 studies correctly applied all HOC criteria |
| Algorithm settings transparent | ~5% | Weighting scheme, iterations, convergence rarely reported |

**Key takeaway**: The largest practice gaps are in discriminant validity (HTMT), formative measurement (redundancy analysis), predictive assessment (PLSpredict), effect sizes (f²), and measurement invariance (MICOM before MGA). Researchers should prioritize these areas.

**Reference**: Sarstedt, M., Hair, J.F., Pick, M., Liengaard, B.D., Radomir, L. & Ringle, C.M. (2022). Progress in Partial Least Squares Structural Equation Modeling Use in Marketing Research in the Last Decade. *Psychology & Marketing*, 39, 1035–1064.

---

## Common Reporting Mistakes to Avoid

1. **Not reporting HTMT** (relying only on Fornell-Larcker or cross-loadings)
2. **Omitting confidence intervals** (reporting only p-values)
3. **Not reporting f² effect sizes** alongside path coefficients
4. **Skipping predictive assessment** (PLSpredict / Q²)
5. **Not justifying the choice of PLS-SEM** over CB-SEM
6. **Not specifying bootstrapping parameters** (number of subsamples, CI type)
7. **Applying reflective criteria to formative constructs** (or vice versa)
8. **Reporting Cronbach's alpha as the sole reliability measure**
9. **Not reporting rho_A** alongside CR and alpha
10. **Omitting the model diagram** or presenting it without coefficients

---

## References

- Becker, J.-M. et al. (2023). PLS-SEM's Most Wanted Guidance. *IJCHM*, 35(1), 321–346.
- Hair, J.F., Risher, J.J., Sarstedt, M. & Ringle, C.M. (2019). When to Use and How to Report the Results of PLS-SEM. *European Business Review*, 31(1), 2–24.
- Legate, A.E., Ringle, C.M. & Hair, J.F. (2024). PLS-SEM: A Method Demonstration in the R Statistical Environment. *HRDQ*, 35(4), 501–529.
- Sarstedt, M., Hair, J.F. & Ringle, C.M. (2023). "PLS-SEM: Indeed a silver bullet" — Retrospective observations and recent advances. *JMTP*, 31(3), 261–275.
