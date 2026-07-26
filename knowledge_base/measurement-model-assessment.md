# Measurement Model Assessment — Detailed Guide

## Overview

Measurement model assessment is the **first mandatory step** before evaluating the structural model. The procedures differ fundamentally between reflective and formative measurement models. Never apply reflective criteria to formative constructs or vice versa.

---

## Preliminary: Confirming Measurement Model Specification (CTA-PLS)

Before applying reflective or formative assessment criteria, researchers should have a theoretical basis for specifying indicators as reflective or formative. When uncertainty exists, **Confirmatory Tetrad Analysis for PLS (CTA-PLS)** (Gudergan, Ringle, Wende & Will, 2008) provides a statistical test to distinguish reflective from formative measurement models.

### What is CTA-PLS?

A tetrad is the difference of the product of a pair of covariances and the product of another pair: τ₁₂₃₄ = σ₁₂σ₃₄ − σ₁₃σ₂₄. Under a reflective (common factor) model, all model-implied non-redundant vanishing tetrads equal zero. Under a formative model, no tetrads vanish.

### CTA-PLS Procedure

1. **Form and compute** all vanishing tetrads for each measurement model (requires ≥ 4 indicators per construct; constructs with fewer indicators borrow indicators from connected constructs)
2. **Identify model-implied** vanishing tetrads (tetrads that should equal zero under a reflective specification)
3. **Eliminate redundant** model-implied vanishing tetrads (algebraic substitution)
4. **Bootstrap significance test** for each non-redundant vanishing tetrad (H₀: τ = 0; BCa confidence intervals; Bonferroni adjustment for multiple testing)
5. **Evaluate results**: If all non-redundant tetrads are non-significant (CIs include 0), the reflective model is supported. If any tetrad is significant, the reflective model is rejected in favor of a formative specification.

### Interpretation

| CTA-PLS Result | Interpretation |
|---|---|
| All tetrads non-significant | Reflective specification supported |
| One or more tetrads significant | Reflective specification rejected; consider formative |
| Formative construct (no vanishing tetrads expected) | No tetrads should vanish — CTA confirms if this holds |

### When to Use CTA-PLS

- When theoretical grounds for reflective vs. formative classification are ambiguous
- As a supplementary check to strengthen measurement model specification arguments
- When reviewers question measurement model specification

### Multiple Testing Corrections (Cefis et al., 2025)

The number of tetrads grows combinatorially with indicators (e.g., 4 indicators = 3 tetrads, 6 indicators = 45 tetrads). Without correction, Type I error inflates with more indicators.

| Correction | Behavior | Recommendation |
|---|---|---|
| **Benjamini-Hochberg (BH)** | Controls false discovery rate; balanced power | **Recommended as default** |
| **Bonferroni** | Controls family-wise error rate; very conservative | Use when strict Type I control is paramount |
| **None (unadjusted)** | Inflated Type I error | Avoid with > 4 indicators per construct |

- Minimum sample size for reliable CTA-PLS: N ≥ 200
- With N < 200, CTA-PLS has limited power regardless of correction method

### Why Correct Specification Matters: Misdisattenuation (Rhemtulla et al., 2020)

Fitting the wrong measurement model has consequences beyond poor fit. When the true data-generating process is composite (formative) but a common factor model is fitted, the disattenuation correction **overestimates** structural correlations by a quantifiable factor:

**Misdisattenuation factor** = √[(1 + (p−1)c) / (pc)], where p = number of indicators and c = average inter-indicator correlation.

This bias is equal in magnitude but **opposite in direction** to attenuation — creating systematic overestimation rather than underestimation. Model fit indices (RMSEA) may still appear acceptable despite substantial structural parameter bias.

**Implication**: Researchers must determine whether constructs are reflective or formative **before** estimation, not post-hoc. Use CTA-PLS or strong theoretical justification.

### Limitations

- Requires ≥ 4 indicators per construct (or borrows from connected constructs)
- Uses bootstrapping adapted for PLS assumptions (non-parametric)
- In ambiguous cases, defer to theory alongside statistical evidence

### Key References
- Gudergan, S.P., Ringle, C.M., Wende, S. & Will, A. (2008). Confirmatory Tetrad Analysis in PLS Path Modeling. *Journal of Business Research*, 61(12), 1238–1249.
- Cefis, M., Angelelli, M., Carpita, M. & Ciavolino, E. (2025). Confirmatory Tetrad Analysis in PLS-SEM: A Multiple Testing Correction Perspective. *Social Indicators Research* (advance online).
- Rhemtulla, M., van Bork, R. & Borsboom, D. (2020). Worse than Measurement Error. *Psychological Methods*, 25(1), 30–45.

---

## Reflective Measurement Model Assessment

### Step 1: Indicator Reliability (Outer Loadings)

**What it measures**: The proportion of indicator variance explained by the construct.

**Metric**: Outer loading (λ). Indicator reliability = λ².

**Thresholds**:
- λ ≥ 0.708 → retain (explains ≥ 50% of variance)
- 0.40 ≤ λ < 0.708 → consider removal only if it improves AVE or CR above thresholds
- λ < 0.40 → remove from the model

**Decision tree for loadings between 0.40–0.708**:
1. Calculate AVE and CR without the indicator
2. If AVE or CR increases above the threshold → remove the indicator
3. If AVE and CR are already above thresholds → retain the indicator (content validity)
4. Document the rationale for retention or removal

**Common mistakes**:
- Removing indicators purely based on loading cutoffs without considering content validity
- Using standardized loadings from one group in MGA when loadings differ across groups
- Confusing outer loadings (reflective) with outer weights (formative)

**Edge cases**:
- Cross-loadings: An indicator should load highest on its intended construct. If it loads higher on another construct, consider reassignment or removal
- Newly developed scales: More lenient thresholds (0.60) are acceptable in early-stage research
- Single-item constructs: Loading is fixed at 1.0; skip indicator reliability assessment

### Step 2: Internal Consistency Reliability

**What it measures**: How consistently indicators measure the same construct.

**Metrics** (report all three for transparency):

| Metric | Formula basis | Properties | Threshold |
|---|---|---|---|
| Cronbach's alpha (α) | Assumes equal loadings (tau-equivalence) | Lower bound of reliability | 0.70–0.90 |
| Composite reliability (CR / rho_c) | Based on actual loadings | Upper bound of reliability | 0.70–0.90 |
| rho_A (ρ_A) | Consistent reliability (Dijkstra & Henseler, 2015) | Exact reliability (between α and CR) | 0.70–0.90 |

**Interpretation**:
- Values < 0.60: Lack of internal consistency (even for exploratory research)
- 0.60–0.70: Acceptable in exploratory research only
- 0.70–0.90: Satisfactory for confirmatory research
- \> 0.95: Problematic — indicates redundant indicators (not desirable; consider reducing indicators)

**Common mistakes**:
- Reporting only Cronbach's alpha (it underestimates reliability when loadings differ)
- Treating CR > 0.95 as "excellent" (it signals item redundancy)
- Using Cronbach's alpha for formative constructs (it's meaningless for formative models)

### Step 3: Convergent Validity (AVE)

**What it measures**: The extent to which indicators of the same construct converge (share variance).

**Metric**: Average Variance Extracted (AVE) = Σλ²ᵢ / n

**Threshold**: AVE ≥ 0.50 (the construct explains at least 50% of indicator variance on average)

**If AVE < 0.50**:
1. Identify indicators with the lowest loadings
2. Check if removing them raises AVE ≥ 0.50 without compromising content validity
3. Consider whether the construct is poorly defined or too broad

**Edge case**: A construct can have CR > 0.70 but AVE < 0.50 if loadings vary widely (some very high, some low). This signals heterogeneous indicator quality.

### Step 4: Discriminant Validity

**What it measures**: The extent to which a construct is empirically distinct from other constructs.

#### HTMT (Heterotrait-Monotrait Ratio) — Preferred Method

The HTMT is the ratio of between-trait correlations to within-trait correlations (Henseler, Ringle & Sarstedt, 2015).

**Thresholds**:
- HTMT < 0.90: Standard threshold for conceptually distinct constructs
- HTMT < 0.85: Conservative threshold for conceptually similar constructs
- **HTMT inference**: Bootstrap confidence interval should not include the chosen threshold (0.85 or 0.90; Ringle et al., 2023)

**Decision tree**:
1. Compute HTMT for all construct pairs
2. If any HTMT ≥ 0.90 (or 0.85 for similar constructs) → discriminant validity concern
3. Run bootstrap HTMT inference (percentile CI) → if CI includes the threshold (0.85 or 0.90), discriminant validity is not established (Ringle et al., 2023)
4. Remedies: Remove problematic indicators, merge constructs if theoretically justified, or reconsider the conceptual distinction

**Common mistakes**:
- Using only the Fornell-Larcker criterion (it fails to detect discriminant validity problems in many scenarios; HTMT is superior)
- Not reporting HTMT bootstrap confidence intervals
- Ignoring HTMT issues and proceeding to structural model assessment

#### Fornell-Larcker Criterion (Legacy — Not Recommended as Sole Criterion)

- Each construct's AVE should exceed the squared correlation with every other construct
- Known to perform poorly when loadings are similar across indicators (Henseler et al., 2015)
- Report for backward compatibility but rely on HTMT

#### Cross-Loadings (Supplementary)

- Each indicator should load highest on its intended construct
- The difference between the loading on its own construct and on other constructs should be substantial (no strict cutoff, but > 0.10 is a common heuristic)

### Summary Decision Table — Reflective Model

| Step | Criterion | Metric | Threshold | Action if Not Met |
|---|---|---|---|---|
| 1 | Indicator reliability | Loading (λ) | ≥ 0.708 | Remove if < 0.40; consider removal if < 0.708 and improves AVE/CR |
| 2 | Internal consistency | CR, rho_A | 0.70–0.90 | Revise indicators; check for redundancy if > 0.95 |
| 3 | Convergent validity | AVE | ≥ 0.50 | Remove weakest indicators; reconsider construct definition |
| 4 | Discriminant validity | HTMT | < 0.90 (< 0.85 conservative) | Remove indicators; merge constructs; check conceptual overlap |
| 4 | Discriminant validity | HTMT CI | Does not include 1 | Same remedies as HTMT threshold |

---

## Formative Measurement Model Assessment

### Important Conceptual Notes

Formative indicators are **not interchangeable** — each captures a unique facet of the construct. Removing an indicator changes the construct's meaning. Therefore:
- Do NOT apply reliability or convergent validity criteria designed for reflective models
- Content validity (ensuring all relevant facets are captured) is paramount
- Assessment focuses on indicator contribution, collinearity, and external validity

### Step 1: Convergent Validity (Redundancy Analysis)

**What it measures**: Whether the formatively measured construct correlates sufficiently with a reflective measure of the same concept.

**Procedure**:
1. Include a single global reflective item (or reflective construct) measuring the same concept
2. Estimate the path from the formative construct to this reflective measure
3. The path coefficient should be ≥ 0.70 (R² ≥ 0.49), indicating the formative construct captures the essence of the concept

**If the path < 0.70**:
- The formative indicators may not adequately capture the construct
- Review indicator content coverage
- Consider adding missing facets

**Single-item vs. multi-item criterion measure** (Cheah, Sarstedt, Ringle, Ramayah & Ting, 2018):
- A **global single item** (e.g., "Overall, I am satisfied with X") is sufficient for redundancy analysis and is often preferable to a multi-item reflective scale
- Single items produce path coefficients ≥ 0.70 for typical sample sizes (up to N ≈ 300) and yield equal or better out-of-sample prediction (PLSpredict RMSE)
- Multi-item criterion measures require a high number of indicators (6+) to outperform a single item in terms of convergent validity, and only at larger sample sizes (N ≥ 400)
- Given that formative models already include many indicators, adding a full reflective scale as a criterion measure unnecessarily increases survey length
- **Recommendation**: Use a global single item as the criterion unless a validated multi-item measure is readily available and sample size is large

**Common mistakes**:
- Skipping redundancy analysis entirely
- Using an inappropriate reflective criterion measure (must genuinely capture the same concept)
- Applying AVE to formative constructs (AVE is meaningless for formative models)

### Step 2: Collinearity Assessment (VIF)

**What it measures**: Whether formative indicators are too highly correlated with each other, which destabilizes weight estimation.

**Metric**: Variance Inflation Factor (VIF) among indicators

**Thresholds**:
- VIF < 3: Ideal; no collinearity concern
- 3 ≤ VIF < 5: Potential concern; inspect carefully
- VIF ≥ 5: Critical collinearity; remedial action needed
- VIF ≥ 10: Severe collinearity; action required

**Remedies for high VIF**:
1. Merge highly correlated indicators into a single indicator
2. Create a higher-order construct with the collinear indicators as separate sub-dimensions
3. Remove one of the collinear indicators (with caution — this changes construct meaning)
4. Transform indicators (e.g., create a composite index)

### Step 3: Significance and Relevance of Outer Weights

**What it measures**: Each indicator's relative contribution to forming the construct, controlling for other indicators.

**Procedure**:
1. Run bootstrapping (≥ 5,000 subsamples; percentile confidence intervals)
2. Assess significance of each outer weight (p < 0.05 or CI does not include 0)
3. Assess the relative size of weights to understand indicator importance

**Decision tree for non-significant weights**:

```
Outer weight significant?
├── YES → Retain indicator (significant relative contribution)
└── NO → Check outer loading
    ├── Loading ≥ 0.50 → Retain (absolute contribution is meaningful)
    └── Loading < 0.50 → Consider removal
        ├── Content validity supports retention → Retain with justification
        └── Content validity does not require it → Remove
```

**Important**: Even with a non-significant weight, an indicator can have a significant **loading**, indicating it has an absolute contribution to the construct (bivariate, not controlling for other indicators). This is sufficient reason to retain it.

**Common mistakes**:
- Removing indicators solely because weights are non-significant (ignoring loadings)
- Interpreting formative weights like regression betas (they are standardized within the construct)
- Not reporting both weights and loadings for formative indicators
- Applying Cronbach's alpha or CR to formative constructs

### Step 4: Epistemic Reliability — Epistemic Rho (ρε)

**What it measures**: Whether the PLS composite score is dominated by its own indicators (epistemic meaning) or has been displaced by structural neighbours due to interpretational confounding from the inner weighting step.

**Metric**: ρε = |cor(η_PLS, PC1)|, where η_PLS is the PLS-estimated construct score and PC1 is the first principal component of the construct's indicators.

**Thresholds**:
- ρε ≥ 0.70: Epistemic reliability established (parallels the AVE ≥ 0.50 logic: 0.70² ≈ 0.50)
- ρε < 0.70: Interpretational confounding suspected — the construct score has been pulled away from its indicators by structural information

**When to assess**:
- Especially critical for **formative (Mode B)** constructs, where no alternative epistemic diagnostic exists (CR, rho_A, AVE are meaningless for formative models)
- Also relevant for Mode A constructs, particularly when structural connections are weak or zero
- Most likely to fail when constructs have few structural connections (e.g., a single path) and that path is weak

**Complementary sensitivity assessment**:
- Compare ρε across model specifications (e.g., add/remove a structural path)
- A change in ρε > 0.15 between specifications signals IC vulnerability
- More informative than a single ρε value because it reveals model-dependence

**Bootstrap hypothesis testing**:
- H₀: ρε < 0.70 (confounding present)
- Bootstrap the ρε statistic; reject H₀ if the 5th percentile of the bootstrap distribution exceeds 0.70
- This provides a formal significance test for epistemic reliability

**Remedies when ρε < 0.70**:
1. Check **structural sufficiency**: Mode B constructs should have ≥ 2 structural connections. With only one weak connection, no method can fully recover epistemic meaning
2. Apply **StablePLS** inner weighting (sets diagonal of inner weight matrix to 1): typically improves ρε by 0.12–0.24 points under confounded conditions
3. If Mode A: StablePLS + PLSc correction resolves both IC and attenuation issues
4. If Mode B with only one structural connection: consider whether the model specification is adequate

**Background — Interpretational confounding (IC)**:
- **IC-from-misspecification** (Bollen, 2007): Arises in any SEM from omitted paths/variables. Addressed by improving model specification.
- **IC-from-algorithm**: Unique to PLS-SEM. The inner weighting step feeds structural relationships back into construct score estimation. When a structural path is weak or zero, the inner weighting can push a construct away from its indicators toward its structural neighbours. This occurs even in correctly specified models.
- Inner weighting schemes differ in IC severity: path weighting (most informative, most IC-prone) > factorial > centroid (least informative, least IC-prone)

**Key references**:
- Burt, R.S. (1976). Interpretational Confounding of Unobserved Variables in Structural Equation Models. *Sociological Methods & Research*, 5(1), 3–52.
- Bollen, K.A. (2007). Interpretational Confounding Is Due to Misspecification. *Psychological Methods*, 12(2), 219–228.
- Bollen, K.A. & Bauldry, S. (2011). Three Cs in Measurement Models. *Psychological Methods*, 16(3), 265–284.
- Howell, R.D., Breivik, E. & Wilcox, J.B. (2007). Reconsidering Formative Measurement. *Psychological Methods*, 12(2), 205–218.

### Summary Decision Table — Formative Model

| Step | Criterion | Metric | Threshold | Action if Not Met |
|---|---|---|---|---|
| 1 | Convergent validity | Redundancy analysis path | ≥ 0.70 | Review content coverage; add facets |
| 2 | Collinearity | VIF | < 5 (ideally < 3) | Merge indicators; create HOC; remove carefully |
| 3 | Significance | Weight p-value | < 0.05 | Check loading; retain if loading ≥ 0.50 |
| 3 | Absolute contribution | Loading (when weight n.s.) | ≥ 0.50 | Retain; document justification |
| 4 | Epistemic reliability | ρε = \|cor(η_PLS, PC1)\| | ≥ 0.70 | Check structural sufficiency; apply StablePLS |
| 4 | Epistemic sensitivity | Δρε across specifications | < 0.15 | Investigate IC vulnerability; consider StablePLS |

---

## Special Cases and Edge Cases

### Mixed Models (Both Reflective and Formative Constructs)

- Apply reflective criteria to reflective constructs and formative criteria to formative constructs
- Report separate tables for each measurement model type
- Ensure the structural model is assessed only after both measurement models pass

### Second-Order / Higher-Order Constructs

- **Type I (Reflective-Reflective)**: Assess LOCs with reflective criteria; assess HOC with reflective criteria at the LOC level (LOC loadings on HOC)
- **Type II (Reflective-Formative)**: Assess LOCs with reflective criteria; assess HOC with formative criteria (LOC weights on HOC, VIF among LOCs)
- **Type III (Formative-Reflective)**: Assess LOCs with formative criteria; assess HOC with reflective criteria
- **Type IV (Formative-Formative)**: Assess LOCs with formative criteria; assess HOC with formative criteria

### PLSc Implications

When using PLSc (consistent PLS):
- All reflective criteria still apply, but estimates are corrected for attenuation
- HTMT values may differ from standard PLS — use PLSc-corrected correlations
- CR and AVE are based on consistent estimates
- The reliability measure used is rho_A

### Bootstrapping Best Practices

- **Number of subsamples**: ≥ 5,000 (10,000 for publication)
- **Confidence interval type**: Percentile CI as default; BCa (bias-corrected and accelerated) for highly asymmetric distributions (Becker et al., 2023)
- **Significance level**: α = 0.05 (two-tailed) unless justified otherwise
- **Reporting**: Always report CIs alongside p-values; CIs are more informative
- **Sign changes**: Use "individual sign changes" option to handle sign indeterminacy (some software defaults differ)

---

## References

- Dijkstra, T.K. & Henseler, J. (2015). Consistent Partial Least Squares Path Modeling. *MIS Quarterly*, 39(2), 297–316.
- Hair, J.F., Risher, J.J., Sarstedt, M. & Ringle, C.M. (2019). When to Use and How to Report the Results of PLS-SEM. *European Business Review*, 31(1), 2–24.
- Hair, J.F., Sarstedt, M., Ringle, C.M., Sharma, P.N. & Liengaard, B.D. (2024). Going Beyond the Untold Facts in PLS-SEM and Moving Forward. *European Journal of Marketing*, 58(13), 81–106.
- Henseler, J., Ringle, C.M. & Sarstedt, M. (2015). A New Criterion for Assessing Discriminant Validity in Variance-Based SEM. *JAMS*, 43(1), 115–135.
- Sarstedt, M., Diamantopoulos, A. & Salzberger, T. (2016). Should We Use Single Items? Better Not. *JBR*, 69(8), 3199–3203.
