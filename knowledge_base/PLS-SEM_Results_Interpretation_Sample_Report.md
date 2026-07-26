# PLS-SEM Model Results — Sample Interpretation Report

**Model:** Satisfaction → Loyalty
**Software:** seminr v2.5.0
**Sample size (N):** 250 observations
**Constructs:** 2 (Satisfaction, Loyalty)
**Structural paths:** 1 (Satisfaction → Loyalty)

---

## 1. Overview

This report interprets the output of a two-construct Partial Least Squares Structural Equation Model (PLS-SEM). The model tests a single hypothesised relationship: that **Satisfaction** predicts **Loyalty**. Before trusting the structural path result, PLS-SEM requires that each construct first pass a **measurement model assessment** (reliability and convergent validity). Only once the measurement model is sound should the structural (path) results be interpreted with confidence.

---

## 2. Reliability & Convergent Validity

| Construct | Cronbach's α | Composite Reliability (CR) | AVE | ρA (rho_A) |
|---|---|---|---|---|
| Satisfaction | 0.779 | 0.780 | 0.544 | 0.792 |
| Loyalty | 0.472 | 0.588 | **0.385** ⚠️ | 0.758 |

### What each metric means

- **Cronbach's α** — measures internal consistency: do the items in a construct correlate strongly enough to be treated as one thing? Conventionally, ≥ 0.70 is acceptable, ≥ 0.60 is tolerable for exploratory work with few items.
- **Composite Reliability (CR)** — a less restrictive internal-consistency measure than α, since it accounts for differing item loadings rather than assuming all items are equally weighted. Threshold: ≥ 0.70 (0.60–0.70 acceptable in exploratory research).
- **AVE (Average Variance Extracted)** — the average amount of variance a construct explains in its own indicators, relative to measurement error. This is the key test of **convergent validity**. Threshold: **≥ 0.50** (the construct explains at least half the variance in its items — the rest is noise).
- **ρA (rho_A)** — Dijkstra-Henseler's consistent reliability coefficient, generally considered the most accurate reliability estimate in PLS-SEM, sitting between α (conservative) and CR (liberal). Threshold: ≥ 0.70.

### Interpretation of these results

**Satisfaction** passes every measurement criterion: α = 0.779, CR = 0.780, AVE = 0.544, and ρA = 0.792 all clear their respective thresholds. This construct is both **reliable** and **convergently valid** — its indicators consistently and sufficiently capture the underlying concept.

**Loyalty** is more concerning:
- Its **AVE of 0.385** falls below the 0.50 threshold, meaning **less than 39% of the variance in the Loyalty indicators is explained by the Loyalty construct itself** — the majority is attributable to measurement error. This is flagged as a **convergent validity concern**.
- Its **Cronbach's α (0.472)** and **CR (0.588)** are also below conventional thresholds, reinforcing that the indicators for Loyalty are not cohering well as a single construct.
- Interestingly, **ρA (0.758)** looks acceptable on its own — this divergence between ρA and the other three metrics is a common symptom of **one or more weak/poorly-loading indicators** dragging down AVE and α while ρA (which weights loadings differently) looks more forgiving.

**Practical implication:** Before reporting the structural path involving Loyalty, it would be standard practice to inspect individual **indicator loadings** for the Loyalty construct. Likely one or more items have loadings below ~0.60–0.70 and should be considered for removal (assuming there are more than 2 indicators; note: with very few indicators, α is known to underestimate reliability — this may explain part of the low α here). Reporting this model "as-is" without addressing the AVE concern would typically draw a reviewer's objection in an academic write-up.

---

## 3. Structural Path Results (Bootstrapped)

| Path | Coefficient (β) | t-statistic | p-value | 95% CI (2.5%) | 95% CI (97.5%) |
|---|---|---|---|---|---|
| Satisfaction → Loyalty | 0.851 | 10.794 | — | 0.689 | 0.994 |

### What each metric means

- **Path coefficient (β)** — the standardised effect size of the predictor on the outcome, analogous to a standardised regression coefficient. Ranges roughly -1 to 1; larger absolute values indicate stronger effects.
- **t-statistic** — from bootstrapping (resampling the dataset many times to estimate the sampling distribution of β without assuming normality, which PLS-SEM does not assume). A t-value **> 1.96** conventionally corresponds to significance at the 5% level (two-tailed).
- **p-value** — not populated here (shown as "—"), but can be derived from the bootstrap t-distribution; in this report we instead rely on the bootstrap confidence interval, which is the standard alternative under PLS-SEM.
- **Bootstrapped confidence interval (CI)** — if the 95% CI **does not contain zero**, the path is considered statistically significant at α = 0.05, regardless of whether a p-value is separately reported.

### Interpretation of this result

The path from **Satisfaction to Loyalty is strong and statistically significant**:
- β = 0.851 indicates a very strong positive effect — a one standard-deviation increase in Satisfaction is associated with roughly a 0.85 standard-deviation increase in Loyalty.
- t = 10.794 is far above the 1.96 threshold.
- The 95% CI [0.689, 0.994] excludes zero comfortably, confirming significance.

**Caveat:** Because the Loyalty construct itself did not clear the AVE threshold, this strong path coefficient should be interpreted cautiously — a structurally significant relationship built on a measurement model with convergent validity concerns may be **inflated or biased**. The recommended next step is to refine the Loyalty construct (e.g., drop weak indicators, re-run the model) before treating β = 0.851 as a final, reportable effect size.

---

## 4. Summary & Recommendations

| Check | Satisfaction | Loyalty | Status |
|---|---|---|---|
| Internal consistency (α, CR) | ✅ Pass | ❌ Below threshold | Review Loyalty items |
| Convergent validity (AVE ≥ 0.50) | ✅ Pass (0.544) | ❌ Fail (0.385) | Convergent validity concern |
| Structural path significance | — | — | ✅ Significant (β = 0.851, CI excludes 0) |

**Recommended next steps:**
1. Examine individual indicator loadings for Loyalty; consider removing low-loading items to raise AVE above 0.50.
2. Re-run the bootstrapped model after any indicator changes, since the structural path estimate may shift.
3. Report both the measurement model issue and the structural result transparently — this is standard, expected practice in PLS-SEM write-ups (e.g., Hair et al.'s guidelines) rather than a sign of a "failed" model.

---

*This is a template interpretation structure — swap in your own construct names, thresholds, and results tables as your PLS-SEM pipeline output changes.*
