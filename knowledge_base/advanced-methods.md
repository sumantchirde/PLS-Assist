# Advanced PLS-SEM Methods — Detailed Guide

> **Causal reasoning companion**: For causal identification (DAGs, backdoor/front-door criteria, good/bad controls), causal mediation assumptions (Pearl's NDE/NIE), endogeneity diagnosis through DAGs, sensitivity analysis for unmeasured confounding, and calibrating causal vs. predictive claims, use the `/causal-methods` skill.

---

## 0. Interpretational Confounding (IC) and StablePLS

### The Problem

PLS-SEM's inner weighting step feeds structural model information back into construct score estimation. When a structural path is weak or zero, this feedback can **displace** a construct score away from its own indicators toward structural neighbours. The construct's empirical meaning then diverges from its theoretical definition — this is **interpretational confounding** (Burt, 1976).

### Two Sources of IC

| Source | Origin | Remedy |
|---|---|---|
| IC-from-misspecification (Bollen, 2007) | Omitted paths/variables in any SEM | Improve model specification |
| IC-from-algorithm | PLS inner weighting step, even in correctly specified models | StablePLS inner weighting |

### The Three Cs (Bollen & Bauldry, 2011)

Understanding IC requires distinguishing three indicator-construct relationships:

1. **Effect indicators** (reflective: η → y): Common factor model. PLS Mode A approximates but does not estimate this exactly. IC distorts the approximation.
2. **Causal indicators** (formative with disturbance: x → η + ζ): IC avoidable via correct specification in CB-SEM. In PLS-SEM, IC-from-algorithm adds an additional source.
3. **Composite indicators** (formative without disturbance: x → C): Inherently model-dependent. PLS estimates this type. Some model-dependence is expected, but IC makes it excessive — the construct becomes more about its neighbours than its indicators.

### Diagnosing IC: Epistemic Rho (ρε)

**Definition**: ρε = |cor(η_PLS, PC1)|, where η_PLS is the PLS construct score and PC1 is the first principal component of the construct's own indicators.

- Measures whether the construct is dominated by its own indicators (high ρε) or has been displaced by structural neighbours (low ρε)
- **Threshold**: ρε ≥ 0.70 (parallels AVE ≥ 0.50 convention: 0.70² ≈ 0.50)
- Especially critical for **formative (Mode B)** constructs, where no alternative epistemic diagnostic exists

**Sensitivity assessment**: Compare ρε across model specifications (e.g., add/remove a path). Change > 0.15 signals IC vulnerability.

**Bootstrap testing**: H₀: ρε < 0.70 (confounding). Reject if bootstrap 5th percentile > 0.70.

### StablePLS: Correcting IC-from-Algorithm

**Mechanism**: Sets the inner weight matrix diagonal to 1 (standard PLS has diagonal = 0), giving each construct a self-referencing anchor that competes with structural neighbour information.

**Properties**:
- **Self-regulating**: When structural relationships are strong (β > 0), the self-reference makes negligible difference. When relationships are weak or zero, the self-reference dominates, preventing displacement.
- Improves ρε by 0.12–0.24 points under confounded conditions
- Halves Mode A Type I error inflation at β = 0
- Eliminates PLSc correction failures (100% valid estimates where standard PLSc fails up to 31%)
- Does **NOT** resolve Mode B Type I error (Mode B instability originates in the outer regression step, not inner weighting)

### Structural Sufficiency

Mode B constructs should have **≥ 2 structural connections**. With only one connection, when that connection is weak, neither standard PLS nor StablePLS can fully recover epistemic meaning. This is a fundamental identifiability limitation, not a software issue.

### Inner Weighting Scheme and IC Severity

| Scheme | Informativeness | IC severity |
|---|---|---|
| Path weighting | Highest (uses regression coefficients) | Highest |
| Factorial | Medium (uses correlations) | Medium |
| Centroid | Lowest (uses correlation signs) | Lowest |

Path weighting is the default in most software. If IC is a concern and StablePLS is not available, switching to centroid weighting reduces (but does not eliminate) IC.

### Practical Workflow

1. Estimate with standard PLS → compute ρε for all constructs
2. If all ρε ≥ 0.70 → proceed with standard results
3. If any ρε < 0.70:
   - Check structural sufficiency (Mode B constructs: ≥ 2 connections?)
   - Re-estimate with StablePLS → recompute ρε
   - Report both standard and StablePLS ρε
4. For Mode A constructs: StablePLS + PLSc corrects both IC and attenuation
5. For Mode B constructs with one connection: acknowledge limitation; consider model redesign

### Key References
- Burt, R.S. (1976). Interpretational Confounding of Unobserved Variables in Structural Equation Models. *Sociological Methods & Research*, 5(1), 3–52.
- Bollen, K.A. (2007). Interpretational Confounding Is Due to Misspecification. *Psychological Methods*, 12(2), 219–228.
- Bollen, K.A. & Bauldry, S. (2011). Three Cs in Measurement Models. *Psychological Methods*, 16(3), 265–284.
- Howell, R.D., Breivik, E. & Wilcox, J.B. (2007). Reconsidering Formative Measurement. *Psychological Methods*, 12(2), 205–218.

---

## 1. Mediation Analysis

### Conceptual Foundation

Mediation examines whether the effect of an exogenous construct (X) on an endogenous construct (Y) is transmitted through an intervening construct (M — the mediator). The indirect effect is the product of the paths: a × b, where a = X → M and b = M → Y.

### Types of Mediation (Zhao, Lynch & Chen, 2010)

| Type | Direct effect (c') | Indirect effect (a × b) | a × b × c' | Interpretation |
|---|---|---|---|---|
| Complementary | Significant | Significant | Positive | Partial mediation; consistent signs |
| Competitive | Significant | Significant | Negative | Partial mediation; opposite signs |
| Indirect-only | Not significant | Significant | — | Full mediation |
| Direct-only | Significant | Not significant | — | No mediation; direct effect only |
| No effect | Not significant | Not significant | — | No effect at all |

### Testing Procedure

1. **Estimate the full model** with both direct and indirect paths (do NOT compare "with" vs "without" mediator models — the Baron-Kenny causal steps approach is outdated)
2. **Bootstrap the indirect effect** (a × b): Use ≥ 5,000 bootstrap subsamples with BCa confidence intervals
3. **Assess significance**: The indirect effect is significant if the BCa CI does not include 0
4. **Classify the mediation** using the Zhao et al. (2010) typology above
5. **Report specific indirect effects** when multiple mediators exist (not just the total indirect effect)

### Effect Size for Indirect Effects

#### Upsilon (υ) — Preferred (Cepeda et al., 2024)

The upsilon effect size measures the strength of the indirect effect, bounded and interpretable:
- υ = 0.01: Small indirect effect
- υ = 0.04: Medium indirect effect
- υ = 0.09: Large indirect effect

Preferred over VAF because it is bounded [0, 1] and does not suffer from sign or magnitude instability.

#### Variance Accounted For (VAF) — Use with Caution

VAF = indirect effect / total effect = (a × b) / (a × b + c')

- VAF > 0.80: Full mediation
- 0.20 ≤ VAF ≤ 0.80: Partial mediation
- VAF < 0.20: No mediation

**Caution**: VAF is unstable and can exceed 1.0 or be negative with competitive mediation. Bootstrap CIs of the indirect effect are more reliable. Use VAF as supplementary information only.

### Multiple Mediators

- **Parallel mediation**: X → M₁ → Y and X → M₂ → Y (mediators at the same level)
- **Serial mediation**: X → M₁ → M₂ → Y (sequential mediators)
- Test each **specific indirect effect** separately (not just the total)
- Specific indirect effect for path through M₁: a₁ × b₁
- Total indirect effect: Σ(aᵢ × bᵢ) + serial paths

### Conditional Mediation (Moderated Mediation)

- The indirect effect varies depending on the level of a moderator
- Test by including the moderator on one or both paths (a or b)
- Bootstrap the conditional indirect effect at different moderator levels
- **Key reference**: Cheah, J.-H. et al. (2021). A Primer on Conditional Mediation Analysis in PLS-SEM. *ACM SIGMIS Database*, 52(SI), 43–100.

### Quantifying Mediation Model Selection Uncertainty

When multiple plausible mediation model specifications exist (e.g., full mediation vs. partial mediation), standard practice selects one model and ignores the uncertainty of that choice. Sarstedt & Moisescu (2024) propose using **Akaike weights** (derived from BIC values) and **weighted bootstrapping** to quantify this uncertainty:

**4-Step Procedure**:
1. **Compute Akaike weights** from BIC values of competing mediation models: w_i = exp(-0.5 * delta_BIC_i) / sum(exp(-0.5 * delta_BIC_j)). Each weight represents the probability that model i is the best model.
2. **Draw weighted bootstrap samples**: For each model i, draw R * w_i bootstrap subsamples (where R >= 10,000 total). This proportionally samples from each model according to its plausibility.
3. **Combine** all bootstrap estimates into a single set of R indirect effect estimates.
4. **Compare** the combined confidence interval (which incorporates model selection uncertainty) with individual model CIs.

**Key insights**:
- The combined CI is typically wider than any individual model's CI, reflecting the additional uncertainty from model selection
- BIC is recommended over AIC as the model selection criterion (Sharma et al., 2019, 2021)
- This approach extends the Zhao et al. (2010) mediation classification by adding a formal uncertainty perspective
- Use at least R = 10,000 total bootstrap samples

### Why PLS-SEM, Not PROCESS (Sarstedt et al., 2020)

Do NOT supplement PLS-SEM with the PROCESS macro for mediation analysis. PLS-SEM is sufficient and superior:

1. **PROCESS ignores model context**: Each regression is piecemeal, ignoring antecedent constructs and parallel paths. This biases estimates, especially in complex models.
2. **PROCESS ignores measurement error**: It uses sum/mean scores. The reliability of an interaction term equals the product of component reliabilities (e.g., ρ_X × ρ_M = 0.80 × 0.80 = 0.64), which falls below acceptable thresholds.
3. **PLS-SEM advantages**: Estimates the full model simultaneously, produces determinate scores that account for measurement error, handles formative constructs natively.

### Predictive Contribution of the Mediator (PCM)

When adding a mediator to a model, it is important to evaluate not only whether the indirect effect is significant (explanatory mediation testing) but also whether the added complexity improves **out-of-sample predictive accuracy**. The PCM metric (Danks, 2021) provides this complementary evidence.

#### The Piggy-in-the-Middle Problem

Mediators serve a dual role: they are both antecedents (of the outcome Y) and outcomes (of the exogenous construct X). Their measurement indicators now compete with the antecedent's indicators in predicting Y. Three prediction strategies resolve this:

| Strategy | What it uses | When to prefer |
|---|---|---|
| **EA (Earliest Antecedents)** | Only earliest exogenous indicators; mediator bypassed in prediction | Archival data where mediator indicators unavailable |
| **DA (Direct Antecedents)** | Direct predictors of Y (including mediator) | Maximizing predictive accuracy |
| **Ensemble** | Average of EA and DA predictions | Theory building, comparing models/datasets |

**Key finding from simulation (Danks, 2021)**: The DA approach consistently generates the highest predictive accuracy (58.3% for full mediation, 65.9% for partial mediation), far exceeding both EA and Ensemble approaches.

#### PCM Formula

For each focal mediation path (X → M → Y), isolate the partial mediation sub-model (X → M, M → Y, X → Y) and compute:

1. **ΔMETRIC** = METRIC_EA − METRIC_DA (equation 1)
2. **PCM** = ΔMETRIC / METRIC_EA (equation 2)

Where METRIC is out-of-sample RMSE or MAE from cross-validated predictions (PLSpredict with `predict_DA` and `predict_EA` techniques).

- **PCM > 0**: Mediator improves predictive accuracy (DA outperforms EA)
- **PCM < 0**: Mediator damages predictive accuracy
- **PCM ≈ 0**: Mediator has no predictive contribution

#### Rules of Thumb

| PCM Range | Classification | Interpretation |
|---|---|---|
| < 0 | Negative | Mediator damages prediction; reconsider inclusion |
| 0 to 0.05 | Weak | Small predictive contribution |
| 0.05 to 0.10 | Moderate | Meaningful predictive contribution |
| > 0.10 | Strong | Substantial predictive contribution |

These boundaries were derived from Monte Carlo simulations across varying sample sizes (100–500), path coefficients (0.1–0.5), indicator loadings (AVE 0.50–0.81), and mediation types (full, partial, none). PCM correctly identifies positive predictive contribution in >80% of cases when mediation is present and negative contribution in >80% of cases when no mediation exists.

#### Procedure

1. **Establish mediation** using standard bootstrapped indirect effects (Zhao et al., 2010 classification)
2. **Isolate the focal mediation model** — for complex models with multiple antecedents, estimate PCM on the sub-model containing only the focal antecedent (X), mediator (M), and outcome (Y) with a direct path X → Y. This prevents attenuation from other constructs.
3. **Run cross-validated predictions** using both DA and EA approaches (e.g., `predict_pls()` with `technique = predict_DA` and `technique = predict_EA`, 10-fold CV with 10 repetitions)
4. **Compute PCM** per indicator of the outcome construct
5. **Report alongside mediation testing** — PCM provides complementary predictive evidence; it does not replace significance testing of indirect effects

#### Decision Tree for Prediction Approach Selection

```
Is prediction the goal of the analysis?
├── Yes → Use DA approach (highest accuracy)
└── No → Are mediator indicator scores available?
    ├── Yes → Use Ensemble approach (most inclusive)
    └── No → Use EA approach (only option)
```

In all cases, compute PCM to evaluate whether the mediator contributes predictively, regardless of which approach is used for generating final predictions.

#### Implementation in SEMinR

Available via `assess_pcm()` in the **seminrExtras** package:

```r
library(seminr)
library(seminrExtras)

# Estimate mediation model
model <- estimate_pls(data, measurement_model, structural_model)

# Compute PCM for all mediation paths to target
pcm <- assess_pcm(model, target = "Loyalty", noFolds = 10, reps = 10)
pcm              # concise overview
summary(pcm)     # per-indicator detail
plot(pcm)        # barplot with threshold lines
```

The function automatically identifies all mediation paths (X → M → Y) to the specified target, isolates sub-models, and computes PCM. Interaction constructs and higher-order constructs are handled automatically (excluded and skipped with warnings, respectively).

### Common Mistakes in Mediation Analysis

- Using the Baron-Kenny causal steps approach (requiring a significant total effect before testing mediation — not necessary)
- Using the Sobel test (assumes normality of the indirect effect distribution — use bootstrapping instead)
- Running PROCESS macro separately from PLS-SEM (use PLS-SEM's built-in bootstrapping — see above)
- Not reporting specific indirect effects in multiple mediator models
- Confusing total indirect effect with specific indirect effects
- Selecting a single mediation model specification without quantifying model selection uncertainty
- Not reporting effect sizes for indirect effects (use upsilon υ)
- **Not evaluating the predictive contribution of the mediator** (use PCM alongside traditional mediation testing)

### Key References
- Nitzl, C., Roldán, J.L. & Cepeda Carrión, G. (2016). Mediation Analysis in PLS Path Modeling. *IMDS*, 116(9), 1849–1864.
- Danks, N.P. (2021). The Piggy in the Middle: The Role of Mediators in PLS-SEM Prediction. *The DATA BASE for Advances in Information Systems*, 52(SI), 24–42.
- Sarstedt, M., Hair, J.F., Nitzl, C., Ringle, C.M. & Howard, M.C. (2020). Beyond a Tandem Analysis of SEM and PROCESS. *IJMR*, 62(3), 288–299.
- Cheah, J.-H. et al. (2021). A Primer on Conditional Mediation Analysis in PLS-SEM. *ACM SIGMIS Database*, 52(SI), 43–100.
- Sarstedt, M. & Moisescu, O.-I. (2024). Quantifying Uncertainty in PLS-SEM-based Mediation Analyses. *JMA*, 12(1), 87–96.
- Rigdon, E.E., Sarstedt, M. & Moisescu, O.I. (2023). Quantifying Model Selection Uncertainty via Bootstrapping and Akaike Weights. *IJCS* (forthcoming).

---

## 2. Moderation Analysis

### Conceptual Foundation

Moderation occurs when the effect of X on Y depends on the level of a third variable (W — the moderator). The interaction effect (X × W) captures how the X → Y relationship changes across levels of W.

### Conceptualizing Moderation Hypotheses

The seven-step framework by Andersson, Cuervo-Cazurra & Nielsen (2014) is strongly recommended for justifying moderation hypotheses (Memon et al., 2019):

1. **Identify the theory** that explains both the direct and moderating effects
2. **Apply the theory** to the research question — explain the direct effect and the mechanisms behind it
3. **Provide theoretical justification** for the choice of moderator variable (M)
4. **Explain the direct effect of M on Y** — clarify how it differs from the moderating effect (Z)
5. **Explain how the moderating effect changes the mechanism** — strengthening or weakening the direct relationship
6. **Theoretically rule out the reverse interaction** — that is, X moderating the M → Y relationship
7. **Return to theory when interpreting results** — explain from a theoretical viewpoint, not just statistical significance

**Key principle**: The inclusion of moderating effects must be justified by theory, not by trial and error or the desire to make the model complex. Hypotheses should explicitly state the direction of the interaction (e.g., "The relationship between X and Y will be stronger when M is present").

### When to Test Moderation

- Unexpectedly weak or inconsistent X → Y relationship across studies (Baron & Kenny, 1986; Frazier et al., 2004)
- A contextual factor from a different field provides new theoretical insights (Andersson et al., 2014)
- Inconsistent findings in past studies suggest a boundary condition

### Approaches for Creating the Interaction Term

Four approaches have been compared in the literature (Henseler & Chin, 2010):

#### Product Indicator Approach
- Creates all possible pairwise products of X and W indicators
- These product indicators become the indicators of the interaction construct (X × W)
- **Best for**: Reflective X and reflective W
- **Advantage**: Uses all available information; good prediction accuracy
- **Disadvantage**: Creates many indicators; can be cumbersome with many original indicators

#### Two-Stage Approach
- **Stage 1**: Estimate the model without the interaction term; save construct scores for X, W
- **Stage 2**: Create a single product term (X_score × W_score) as a single-item construct and re-estimate
- **Best for**: Formative constructs, single-item constructs, or when the product indicator approach is impractical
- **Advantage**: Works with any measurement model type; simpler; highest statistical power (Henseler & Chin, 2010)
- **Recommended as the default approach** in recent literature (Becker, Ringle & Sarstedt, 2018)

#### Orthogonalizing Approach
- Residual-centers the product indicators on the main effect indicators
- Reduces collinearity between main effects and interaction
- **Best parameter accuracy** in Monte Carlo comparison (Henseler & Chin, 2010)
- **Best prediction accuracy** alongside the product indicator approach
- Less commonly used in current PLS-SEM practice

#### Hybrid Approach (Wold, 1982)
- Uses both product indicator and two-stage logic: product terms are created from Stage 1 construct scores and original indicators
- **Advantage**: High statistical power (comparable to two-stage)
- **Disadvantage**: More complex to implement; less parsimonious

### Monte Carlo Evidence (Henseler & Chin, 2010)

| Criterion | Best Approach |
|---|---|
| Parameter accuracy | Orthogonalizing |
| Statistical power | Two-stage and hybrid |
| Prediction accuracy | Orthogonalizing and product indicator |
| Overall recommendation | Orthogonalizing (best balance); two-stage (best for formative) |

### Data Treatment Warnings (Becker, Ringle & Sarstedt, 2018)

- **AVOID** unstandardized data with the product indicator approach (severe bias; PLSc-SEM can yield negative estimates for positive true values)
- **AVOID** mean-centering indicators before creating interaction terms (triggers considerable biases)
- The two-stage approach uses standardized construct scores by design (no data treatment issue)
- Product indicator with standardized data performs comparably to two-stage only for purely reflective models
- The orthogonalizing approach overestimates the interaction effect when used with PLSc-SEM

### Interpreting Moderation Results

1. **Interaction path coefficient**: The coefficient of X × W → Y
   - Significant interaction indicates moderation exists
   - The sign indicates direction: positive means W strengthens the X → Y effect; negative means W weakens it
2. **Simple slopes analysis**: Plot the X → Y relationship at different levels of W (typically: mean, +1 SD, −1 SD)
3. **Interaction plot**: Visual representation of simple slopes — essential for interpretation
4. **f² of the interaction**: Effect size of the moderating effect
   - Moderation f² tend to be small; use **Kenny (2016) thresholds for moderation**: f² = 0.005 small, 0.01 medium, 0.025 large (Memon et al., 2019)
   - These are lower than the standard Cohen (1988) thresholds used for direct effects
   - Do not dismiss small interaction effects — they can be theoretically meaningful (Aguinis et al., 2005)

### Moderating Effect on Formative Constructs

- Use the two-stage approach (product indicator doesn't work well for formative)
- The moderator can be formative or reflective — two-stage handles both

### Categorical Moderators

- If the moderator is categorical (e.g., gender, country), use **Multigroup Analysis (MGA)** instead of creating product terms
- MGA splits the sample by groups and compares path coefficients

### Quadratic Effects (Nonlinear)

- A special case of moderation where a construct moderates its own effect: X² → Y
- Creates a quadratic (U-shaped or inverted-U) relationship
- In PLS-SEM: create a squared term using the two-stage approach
- Interpret: significant quadratic term indicates nonlinearity; plot the curve
- **Key reference**: Basco, R., Hair, J.F., Ringle, C.M. & Sarstedt, M. (2022). Advancing Family Business Research Through Modeling Nonlinear Relationships. *JFBS*, 13(3), 100457.

### Pre-Analysis Guidelines (Memon et al., 2019)

1. **Use sufficient scale points**: A 7-point Likert scale is preferred for detecting moderating effects; fewer points risk information loss
2. **Pretest the instrument** using protocol analysis or debriefing techniques with target participants before main data collection
3. **Keep moderator items prominent** in the questionnaire order, especially if the survey is lengthy
4. **Run power analysis twice**: Before data collection (to determine required sample size) and after (to confirm sufficient power was achieved). Target power ≥ 0.80
5. **Screen suspicious responses**: Straight-lining, zigzag patterns, and responses with SD < 0.5 should be flagged
6. **Do not convert continuous moderators to categorical**: Artificial dichotomization (e.g., median splits) discards information, biases estimates downward, and reduces statistical power (Aguinis, 1995; Aguinis & Gottfredson, 2010)

### Common Mistakes in Moderation Analysis

- Interpreting a non-significant interaction as "no moderation" without considering statistical power (target ≥ 0.80)
- Not plotting the interaction — numbers alone can be misleading
- Confusing moderation with mediation
- Using MGA when the moderator is continuous (MGA requires groups; use product terms for continuous moderators)
- Artificially dichotomizing continuous moderators via median splits (loses information, biases estimates downward)
- Not reporting reliability of the interaction term — the product term's reliability equals the product of component reliabilities (e.g., ρ_X × ρ_M = 0.70 × 0.70 = 0.49), which can fall below acceptable thresholds (Aguinis et al., 2017)
- Interpreting the X → Y direct effect without the interaction term when an interaction exists — when moderation is present, X has a range of effects (simple slopes), not a single unique effect (Aiken & West, 1991)
- Not striving for balanced group sizes when the moderator is categorical (e.g., 80/20 gender split leads to underestimation of the moderating effect)

### Key References
- Henseler, J. & Chin, W.W. (2010). A Comparison of Approaches for the Analysis of Interaction Effects. *SEM*, 17(1), 82–109.
- Henseler, J. & Fassott, G. (2010). Testing Moderating Effects in PLS Path Models. In *Handbook of PLS*, Springer, 713–735.
- Becker, J.-M., Ringle, C.M. & Sarstedt, M. (2018). Estimating Moderating Effects in PLS-SEM and PLSc-SEM. *JASEM*, 2(2), 1–21.
- Memon, M.A. et al. (2019). Moderation Analysis: Issues and Guidelines. *JASEM*, 3(1), i–ix.

---

## 3. Multigroup Analysis (MGA)

### Purpose

MGA tests whether path coefficients differ significantly across pre-defined groups (e.g., gender, country, customer segments). It is the PLS-SEM equivalent of multi-sample analysis in CB-SEM.

### Prerequisite: MICOM (Measurement Invariance of Composite Models)

Before comparing groups, measurement invariance must be assessed to ensure constructs have the same meaning across groups (Henseler, Ringle & Sarstedt, 2016).

#### Step 1: Configural Invariance
- Same indicators per construct, same structural model, same algorithm settings across groups
- Typically satisfied by design (same model specification)

#### Step 2: Compositional Invariance
- Test whether composite weights produce constructs with the same meaning across groups
- **Permutation test**: Correlate composite scores across groups; the correlation should be close to 1.0
- If the permutation-based CI includes the observed correlation → compositional invariance is established
- **This step is critical** — without it, group comparisons may be invalid

#### Step 3: Equality of Composite Mean Values and Variances
- Tests if the means and variances of composites are equal across groups
- Required for **full measurement invariance**
- If not established, **partial invariance** (Steps 1 + 2) is sufficient for MGA of path coefficients
- Use permutation test: if CIs include observed mean/variance differences → equality holds

#### MICOM Decision Summary

| Steps Established | Invariance Level | Implication |
|---|---|---|
| Step 1 only | Configural only | Cannot compare groups |
| Steps 1 + 2 | Partial (compositional) | Can compare path coefficients via MGA |
| Steps 1 + 2 + 3 | Full | Can compare path coefficients, means, and variances |

### MGA Methods

#### PLS-MGA (Nonparametric)
- Compares the bootstrap distributions of path coefficients between groups
- If p < 0.05 (or > 0.95) → significant difference
- Does not assume normality
- **Most commonly used** in PLS-SEM

#### Parametric Test (Welch-Satterthwaite)
- Assumes bootstrap path coefficient estimates are normally distributed
- Standard t-test comparison
- Less robust than nonparametric approaches

#### Permutation Test
- **Most robust** method; recommended as primary
- Randomly reassigns observations to groups and re-estimates
- Compares observed difference to the permutation distribution
- Does not assume normality or equal variances

#### Confidence Interval-Based Comparison
- Check if the CI of one group's path coefficient includes the point estimate of the other group
- Less formal than statistical tests

### MGA for More Than Two Groups (Cheah et al., 2023)

When comparing K > 2 groups, a two-step procedure is recommended:

#### Step 1: Omnibus Test

Before conducting pairwise comparisons, test whether **any** group differences exist using one of three omnibus tests:

| Test | Method | Advantages |
|---|---|---|
| **OTG** (Omnibus Test of Group differences) | Compares bootstrap confidence intervals across all K groups | Simple; conceptually straightforward |
| **NDT** (Non-parametric Difference Test) | Extends PLS-MGA to K groups simultaneously | Does not assume normality |
| **NPT** (Non-parametric Permutation Test) | Permutation-based omnibus test | Most robust; recommended as primary |

If the omnibus test is **not significant** → stop; no group differences exist.

#### Step 2: Pairwise Comparisons

If the omnibus test is significant:
1. Conduct pairwise MGA comparisons (PLS-MGA or permutation) for all K(K−1)/2 pairs
2. Apply **Bonferroni correction** (or less conservative alternatives like Holm-Bonferroni) for multiple comparisons: adjusted α = 0.05 / number of pairwise comparisons
3. Report all pairwise comparisons in a matrix format

#### Measurement Invariance for K > 2 Groups

MICOM must be established across **all groups simultaneously**, not just pairwise. Compositional invariance (Step 2) should hold for all group combinations.

**Beyond MICOM Steps 1–3** (Liengaard, 2024): For rigorous group comparisons, consider extending to metric and scalar invariance:
- **Metric invariance**: Tests whether composite weights are equal across groups (stronger than compositional invariance)
- **Scalar invariance**: Tests whether indicator intercepts are equal across groups (required for comparing construct means)
- Metric invariance is sufficient for comparing path coefficients; scalar invariance is required for comparing construct scores/means

### Hybrid Multigroup PLS-SEM (Pathmox + MGA)

When there are **many potential categorical segmentation variables** and no strong theory to select among them, the hybrid multigroup approach combines **pathmox analysis** with MGA (Lamberti, 2023):

**Three-step procedure**:

1. **Determine the hybrid segmentation variable via pathmox**:
   - (a) Perform pathmox tree analysis to identify the most significant subgroups from all available segmentation variables
   - (b) Define the hybrid segmentation variable according to the resulting tree nodes
   - (c) Interpret the levels of the hybrid segmentation variable based on which segmentation variables drive each split

2. **Estimate separate PLS-SEM models** for each hybrid segment and assess measurement/structural models

3. **Run MGA comparisons** across segments using parametric test, PLS-MGA, permutation test, or omnibus test

**Pathmox parameters**:
- Significance threshold for splits: p = 0.05
- Maximum tree depth: 2 recommended (for interpretability)
- Minimum node size: 10% of total sample
- Uses F-global test (adapted Fisher's F-test for equality in regression models) to determine optimal binary splits

**When to use**: Exploratory segmentation with many demographic/categorical variables (e.g., age, gender, education, job level, tenure). Classical MGA becomes unwieldy with many segmentation variables because interactions and mixed effects are hard to identify.

**R package**: `genpathmox` (Lamberti, 2014) for pathmox analysis; SmartPLS or other PLS-SEM software for MGA.

**MICOM** must still be assessed before MGA comparisons across pathmox-identified segments.

### Common Mistakes in MGA
- Skipping MICOM (comparing groups without establishing measurement invariance)
- Using MGA with very small group sizes (minimum ~50–100 per group recommended)
- Not correcting for multiple comparisons when testing > 2 groups
- Using MGA for continuous moderators (use product indicator or two-stage approach instead)

### Key References
- Henseler, J., Ringle, C.M. & Sarstedt, M. (2016). Testing Measurement Invariance of Composites Using PLS. *International Marketing Review*, 33(3), 405–431.
- Sarstedt, M., Henseler, J. & Ringle, C.M. (2011). Multigroup Analysis in PLS Path Modeling. *AIM*, 22, 195–218.
- Cheah, J. et al. (2020). Multigroup Analysis using SmartPLS. *AJBR*, 10(3), 1–19.
- Cheah, J.-H. et al. (2023). Multigroup analysis of more than two groups in PLS-SEM. *JBR*, 156, 113539.
- Liengaard, B.D. (2024). Measurement Invariance Testing in PLS-SEM. *JBR*, 177, 114581.
- Lamberti, G. (2023). Hybrid Multigroup PLS-SEM: An Application to Bank Employee Satisfaction and Loyalty. *Quality & Quantity*, 57, S683–S705.

---

## 4. IPMA (Importance-Performance Map Analysis)

### Conceptual Foundation

IPMA extends basic PLS-SEM results by considering both the **importance** (total effect) and **performance** (rescaled mean value) of each construct/indicator in predicting a target construct.

### Procedure

1. **Importance**: Compute unstandardized total effects of each construct on the target construct
2. **Performance**: Rescale indicator data to a 0–100 range using: Performance = (observed − min) / (max − min) × 100
3. **Plot**: X-axis = importance (total effect); Y-axis = performance (rescaled mean)
4. **Interpret**: Focus on constructs in the **high importance, low performance** quadrant — these represent the greatest opportunity for improvement

### Requirements

- Indicator data must be coded in the same direction (higher = better / more)
- Unstandardized effects are needed (not standardized)
- The target construct must be specified (IPMA is always relative to one target)
- **All outer weights must be positive** — negative outer weights invalidate the performance rescaling; reverse-code indicators or check model specification if negative weights appear (Ringle & Sarstedt, 2016)
- **Exclude moderating constructs** from IPMA — interaction terms lack a meaningful performance interpretation on the 0–100 scale

### Interpretation Guidelines

| Quadrant | Importance | Performance | Action |
|---|---|---|---|
| Q1 | High | Low | **Priority area** — highest impact improvement opportunities |
| Q2 | High | High | Maintain — already performing well on important factors |
| Q3 | Low | Low | Low priority — limited impact even if improved |
| Q4 | Low | High | Over-performing — resources may be reallocated |

### cIPMA (Combined IPMA)

**cIPMA** extends IPMA by integrating **Necessary Condition Analysis (NCA)** to distinguish between necessary and sufficient conditions (Hauff et al., 2024; Sarstedt et al., 2024).

- **Standard IPMA**: Identifies important (sufficient) conditions based on total effects
- **cIPMA addition**: Identifies which constructs are also **necessary** conditions (without which the outcome cannot reach high levels)
- A construct can be important (strong total effect) but not necessary, or necessary but not a strong sufficient predictor

#### cIPMA Procedure (Sarstedt et al., 2024)

1. **Run PLS-SEM** and assess measurement and structural models fully
2. **Compute IPMA**: Obtain unstandardized total effects (importance) and rescaled performance scores (0–100) for each construct
3. **Run NCA** on construct scores from PLS-SEM for each predictor → target pair:
   - Compute CE-FDH and CR-FDH ceiling lines
   - Compute NCA effect sizes (d); d ≥ 0.1 considered meaningful
   - Test significance via permutation test
4. **Create the cIPMA map**: Plot constructs on a 2D map with importance (x-axis) and performance (y-axis), then overlay NCA results:
   - Mark constructs that are **necessary conditions** (significant NCA effect size ≥ 0.1) distinctly from those that are only sufficient
   - Use different symbols or colors: e.g., filled circles for necessary + sufficient, open circles for sufficient only
5. **Interpret the combined map**:

| Construct Type | Importance | NCA Necessary? | Interpretation |
|---|---|---|---|
| High importance, necessary | High total effect | Yes (d ≥ 0.1, sig.) | **Top priority** — both necessary and strongly influential |
| High importance, not necessary | High total effect | No | Important driver but not a bottleneck; can be compensated by other factors |
| Low importance, necessary | Low total effect | Yes (d ≥ 0.1, sig.) | **Bottleneck risk** — not a strong driver on average, but its absence blocks high outcomes |
| Low importance, not necessary | Low total effect | No | Low priority |

6. **Generate bottleneck tables** for necessary constructs: show minimum required predictor levels for given outcome levels
7. **Derive managerial implications**: Prioritize constructs that are both important AND necessary; also address bottleneck constructs that may be overlooked by standard IPMA

### Key References
- Ringle, C.M. & Sarstedt, M. (2016). Gain More Insight from Your PLS-SEM Results: The IPMA. *IMDS*, 119(9), 1865–1886.
- Sarstedt, M., Richter, N.F., Hauff, S. & Ringle, C.M. (2024). Combined Importance-Performance Map Analysis (cIPMA): A SmartPLS 4 Tutorial. *JMA*, 12, 746–760.
- Hauff, S. et al. (2024). Importance and Performance in PLS-SEM and NCA: Introducing the cIPMA. *JRCS*, 78, 103723.

---

## 5. Necessary Condition Analysis (NCA)

### Conceptual Foundation

NCA tests whether a predictor is a **necessary condition** for an outcome — i.e., without a certain level of X, a certain level of Y is impossible, regardless of other predictors. This is fundamentally different from PLS-SEM's sufficiency-based regression logic.

### Key Concepts

- **Necessary condition**: X must be above a threshold for Y to reach a certain level (ceiling line)
- **Sufficient condition**: Higher X is associated with higher Y on average (regression slope)
- A predictor can be necessary but not sufficient, sufficient but not necessary, both, or neither

### 8-Step Combined PLS-SEM + NCA Procedure (Richter et al., 2020)

1. **Run PLS-SEM** and assess measurement/structural models fully
2. **Identify significant determinants** from PLS-SEM results for NCA analysis
3. **Create scatter plots** of X vs. Y for each predictor-outcome pair (NCA is bivariate — run separately for each pair)
4. **Detect and handle outliers**: z-score > 3 for approximately normal data; visual inspection for skewed data
5. **Run NCA** with both ceiling line techniques:
   - **CE-FDH** (Ceiling Envelopment - Free Disposal Hull): Step function; 100% accuracy by definition; more conservative
   - **CR-FDH** (Ceiling Regression - Free Disposal Hull): Regression on ceiling; smoother; accuracy may be < 100%
   - Report both; if they diverge substantially, investigate why
6. **Evaluate NCA effect size** d = ceiling zone / scope
7. **Test significance** via permutation test (10,000 permutations, p < 0.05)
8. **Construct bottleneck tables** showing the minimum required level of X (in % of range) for each desired level of Y

### Effect Size Interpretation

| d | Interpretation |
|---|---|
| d < 0.1 | Small / not meaningful |
| 0.1 ≤ d < 0.3 | Medium necessary condition |
| 0.3 ≤ d < 0.5 | Large necessary condition |
| d ≥ 0.5 | Very large necessary condition |

Always report the permutation p-value alongside the effect size.

### Three Interpretation Scenarios (Richter et al., 2020)

| PLS-SEM Result | NCA Result | Interpretation |
|---|---|---|
| Significant sufficient determinant | Necessary condition (d ≥ 0.1) | **Strongest finding**: X is both necessary and sufficient |
| Significant sufficient determinant | NOT necessary | X contributes to Y on average but can be compensated by other predictors |
| NOT significant sufficient | Necessary condition | X is a prerequisite (gate-keeper) but does not drive Y on its own |

### Bottleneck Table

Shows the minimum required level of X for each desired level of Y:
- E.g., "To achieve Y ≥ 80%, X must be ≥ 60%"
- Directly actionable for practitioners
- Set bottleneck table steps to 20 for adequate granularity

### Construct Type Considerations

- **Reflective constructs**: Use LV (latent variable) scores in NCA
- **Formative constructs**: Run NCA on both LV scores AND individual indicator scores (since formative indicators capture distinct facets)

### Integration with PLS-SEM and IPMA

- NCA complements PLS-SEM by adding necessary condition logic
- Run NCA on construct scores obtained from PLS-SEM
- Combine with IPMA for **cIPMA** (see Section 4): visualize importance, performance, and necessity in a single framework
- Available in the R package `NCA` and SmartPLS 4

### Sensitivity Extension (NCA-ESSE)

Becker et al. (2026) propose a sensitivity-based extension (NCA-ESSE) that examines how robust the "necessary" designation is to changes in the data. This helps distinguish true necessary conditions from artifacts of the specific sample. Evaluates whether small perturbations to the data change the necessity conclusion.

### Key References
- Richter, N.F. et al. (2020). When Predictors of Outcomes are Necessary: Guidelines for PLS-SEM and NCA. *IMDS*, 120(12), 2243–2267.
- Richter, N.F. et al. (2023). How to Apply NCA in PLS-SEM. In *Partial Least Squares Path Modeling*, Springer, 267–297.
- Becker, J.-M. et al. (2026). Must-have, Or Maybe Not? A Sensitivity-based Extension to NCA. *JBR*, 206, 115920.

---

## 6. Endogeneity

### The Problem

Endogeneity occurs when an exogenous construct correlates with the error term of an endogenous construct, typically due to omitted variables that affect both. This biases path coefficient estimates.

### Sources of Endogeneity

- **Omitted variables**: A relevant variable is not included in the model
- **Simultaneity / reverse causality**: X → Y and Y → X simultaneously
- **Measurement error**: Systematic measurement bias (less common in PLS-SEM)
- **Common method bias**: A shared method variance inflates relationships

### When Endogeneity Matters: Explanation vs. Prediction

Before applying any endogeneity correction, researchers must consider their research goal (Hult et al., 2018):

- **Explanatory / causal inference**: Endogeneity directly threatens the validity of causal claims. Controlling for endogeneity is essential.
- **Predictive modeling**: Endogeneity does not bias predictions per se; correcting for it may even reduce predictive power. Testing for endogeneity is less critical in purely predictive contexts.

Most PLS-SEM applications balance both goals. When in doubt, test for endogeneity as a robustness check.

### Systematic Procedure for Addressing Endogeneity (Hult et al., 2018)

The recommended procedure follows four stages:

1. **Stage 1 -- Decide if endogeneity testing is needed**: Consider whether the research goal is primarily explanatory (endogeneity matters) or predictive (endogeneity is less relevant)
2. **Stage 2 -- Use prior knowledge**: Identify potential endogeneity sources from theory and prior research. Include **control variables** as single-item constructs in the PLS model to account for omitted variable bias. Alternatively, collect data on instrumental variables for later use
3. **Stage 3 -- Apply the Gaussian copula approach**: If control variables and prior knowledge are insufficient, use the Gaussian copula to statistically detect endogeneity (see below)
4. **Stage 4 -- Explain endogeneity**: If the Gaussian copula detects endogeneity, add control variables or apply the IV approach to correct the bias. Report corrected and uncorrected estimates

### Comparison of Endogeneity Approaches (Hult et al., 2018)

| Criterion | Control Variables | Instrumental Variables | Gaussian Copula |
|---|---|---|---|
| Additional variables needed | Yes (must be collected) | Yes (IVs must be identified/collected) | No |
| Distribution assumptions | None | None | Endogenous regressors must be non-normal |
| Variable type | Discrete or continuous | Continuous | Discrete or continuous |
| Statistical test for endogeneity | Not necessary | Test for significance and relevance | Test for significance of copula term |
| Acceptance in the literature | Widely used | Widely accepted but rarely used | Relatively new but growing |
| Software support | No additional implementation | Supported by SPSS, Stata, R | Supported by REndo R package |

### The Gaussian Copula Approach (Technical Details)

The primary IV-free method for detecting and addressing endogeneity in PLS-SEM (Hult et al., 2018; Becker, Proksch & Ringle, 2022).

**Technical Procedure** (Becker, Proksch & Ringle, 2022; Liengaard et al., 2025):
1. **Assess endogeneity concerns** theoretically (omitted variables? reverse causality?)
2. **Test non-normality** of each potentially endogenous regressor using Anderson-Darling or Cramér-von Mises tests (preferred over Shapiro-Wilk; more sensitive in tails). Alternatively, use Kolmogorov-Smirnov with Lilliefors correction.
3. **Create copula terms**: For each non-normal regressor X, compute Φ⁻¹(H(X)), where H(X) is the empirical CDF and Φ⁻¹ is the inverse normal CDF. Use the adjusted F4 estimator (Liengaard et al., 2025) rather than the standard F3 ECDF when the model contains an intercept.
4. **Evaluate**: If the copula term's coefficient is significant (p < 0.05 via bootstrapping) → endogeneity is present. Use the copula-corrected model for inference. Compare OLS vs. corrected estimates.

**Requirements and Thresholds** (Becker, Proksch & Ringle, 2022):
- The endogenous regressor must be **continuous** (cannot handle binary or ordinal)
- The regressor must be **non-normally distributed** — specific thresholds:
  - N ≥ 1,000: Skewness > 0.774 is sufficient for identification
  - N < 1,000: Skewness > 2.0 or Anderson-Darling statistic > 20 is needed
  - Near-normal regressors produce unreliable results regardless of sample size
- **Minimum sample size**: N ≥ 200 for detection; N ≥ 1,000 for reliable correction with adequate power
- Non-normality can be assessed at the **system level** — at least one endogenous regressor must be non-normal (Liengaard et al., 2025)
- When multiple variables are potentially endogenous, test all combinations of copula terms

### Instrumental Variables (Alternative)

- Requires a valid instrument: correlated with the endogenous regressor but not with the error term of the outcome
- Finding valid instruments is difficult in practice
- 2SLS (two-stage least squares) adaptation for PLS-SEM

### Best Practices

- Test for endogeneity as a robustness check, even if not theoretically expected
- Report results of endogeneity tests (even if no endogeneity is found)
- If endogeneity is detected, report both uncorrected and corrected estimates
- Acknowledge limitations: the Gaussian copula approach has assumptions that may not hold

### Key References
- Hult, G.T.M. et al. (2018). Addressing Endogeneity in International Marketing Applications of PLS-SEM. *JIM*, 26(3), 1–21.
- Becker, J.-M., Proksch, D. & Ringle, C.M. (2022). Revisiting Gaussian Copulas to Handle Endogenous Regressors. *JAMS*, 50, 46–66.
- Liengaard, B.D. et al. (2025). Dealing with Regression Models' Endogeneity by Means of an Adjusted Estimator for the Gaussian Copula Approach. *JAMS*, 53, 279–299.

---

## 7. Note on Model Fit (CCA)

CCA (Confirmatory Composite Analysis) using SRMR, d_ULS, and d_G is **not recommended** for PLS-SEM model assessment. These indices have limited power to detect specific misspecifications, fixed cutoffs borrowed from CB-SEM do not apply to composites, and the approach remains contested. GoF (Goodness-of-Fit) is also unsuitable (Henseler & Sarstedt, 2013). Focus on predictive assessment (PLSpredict, CVPAT) and substantive evaluation instead.

---

## 8. Unobserved Heterogeneity (FIMIX-PLS and Related Methods)

### The Problem

Aggregate-level PLS-SEM results may mask subgroup differences. If the population consists of unobserved segments with different path coefficients, the aggregate model estimates are biased and misleading.

### FIMIX-PLS (Finite Mixture PLS)

FIMIX-PLS uses the EM (Expectation-Maximization) algorithm to probabilistically assign observations to K latent segments, each with segment-specific structural path coefficients.

**Systematic 4-Step Procedure** (Ringle, Sarstedt & Mooi, 2010):

1. **Estimate the PLS path model** on the full sample
2. **Apply FIMIX-PLS** for K = 1, 2, 3, ... segments, evaluating information criteria:
   - **AIC4**: Best performing single criterion in simulation (58% accuracy; Sarstedt, Becker, Ringle & Schwaiger, 2011)
   - **AIC3**: Recommended alongside CAIC. **Joint AIC3 + CAIC**: when both agree on K, accuracy reaches ~84%
   - **CAIC** (Consistent AIC): Conservative; tends to prefer fewer segments
   - **BIC** (Bayesian Information Criterion): Similar to CAIC
   - **Entropy (EN)**: Classification quality measure (closer to 1 is better); EN > 0.50 indicates adequate segment separation. **Not suitable as a primary criterion** for selecting K
   - AIC/AICc tend to overfit (prefer too many segments); MDL5/InLc/ICL-BIC/AWE tend to underfit
3. **Select the number of segments** based on information criteria convergence, interpretability, and minimum segment size (~50 observations per segment, or 10× the number of predictors in the most complex regression)
4. **Conduct ex-post analysis**: Profile segments using observed variables (demographics, behaviors); aim for ≥ 60% overlap between FIMIX segments and observed group variables

**Limitations of FIMIX-PLS**:
- Assumes normally distributed disturbances within each segment
- Applies only to the inner (structural) model; does not segment measurement models
- Less effective with formative constructs (FIMIX operates on inner model residuals)
- K-means clustering is inappropriate for forming segments with distinctive inner model estimates (Sarstedt & Ringle, 2009) — use FIMIX-PLS or distance-based methods instead

### Taxonomy of PLS-SEM Segmentation Approaches

| Approach | Type | Mechanism | Strengths |
|---|---|---|---|
| **FIMIX-PLS** | Model-based | EM algorithm; probabilistic assignment | Determines K via information criteria |
| **PLS-POS** | Distance-based | Maximizes explained variance difference | Works with formative constructs (Becker et al., 2013) |
| **PLS-GAS** | Distance-based | Genetic algorithm + hill-climbing | Most accurate segment recovery; distribution-free (Ringle et al., 2014) |
| **PLS-IRRS** | Distance-based | Iterative reweighted regressions (M-estimators) | Comparable hit rates to PLS-GAS; 50–5000x faster; works with Mode A and Mode C (Schlittgen et al., 2016) |
| **PATHMOX** | Tree-based | Binary partitioning by observed variables | Interpretable; identifies segmentation variables |
| **REBUS-PLS** | Distance-based | Residual-based; iterative reassignment | Identifies structural heterogeneity; ~50% hit rate in simulations |

### UHD (Unobserved Heterogeneity Detection) Process (Becker et al., 2013)

Recommended multi-method workflow:
1. **FIMIX-PLS** to determine the number of segments (K) via information criteria
2. **PLS-IRRS or PLS-GAS** for definitive segment assignment (both outperform FIMIX-PLS and REBUS-PLS in segment recovery accuracy; PLS-IRRS is 50–5000x faster than PLS-GAS with comparable hit rates)
3. **Validate** by profiling segments against observed characteristics

### Follow-Up Analysis

After identifying segments:
1. Profile segments using observed variables (demographics, behaviors)
2. Use hard clustering (assign observations to the most likely segment) for segment-specific PLS-SEM estimation
3. Run PLS-SEM separately for each segment
4. Compare path coefficients across segments (similar to MGA)
5. Interpret substantively: Why do these segments differ?

**Best practice**: Always check for unobserved heterogeneity as a robustness check, even if it is not the primary research question.

### Key References
- Sarstedt, M. & Ringle, C.M. (2009). Treating Unobserved Heterogeneity in PLS Path Modelling. *Journal of Applied Statistics*.
- Ringle, C.M., Sarstedt, M. & Mooi, E.A. (2010). Response-Based Segmentation Using Finite Mixture PLS. In *Data Mining*, Springer, 19–49.
- Rigdon, E.E., Ringle, C.M. & Sarstedt, M. (2010). Structural Modeling of Heterogeneous Data with PLS. *Review of Marketing Research*, 7, 255–296.
- Sarstedt, M. et al. (2011). Uncovering and Treating Unobserved Heterogeneity with FIMIX-PLS. *SBR*, 63(1), 34–62.
- Sarstedt, M., Becker, J.-M., Ringle, C.M. & Schwaiger, M. (2011). Uncovering and Treating Unobserved Heterogeneity with FIMIX-PLS: Which Model Selection Criterion Provides an Appropriate Number of Segments? *SBR*, 63(1), 34–62.
- Becker, J.-M., Rai, A., Ringle, C.M. & Völckner, F. (2013). Discovering Unobserved Heterogeneity in SEM. *MIS Quarterly*, 37(3), 665–694.
- Ringle, C.M., Sarstedt, M. & Schlittgen, R. (2014). Genetic Algorithm Segmentation in PLS-SEM. *OR Spectrum*, 36, 251–276.
- Schlittgen, R., Ringle, C.M., Sarstedt, M. & Becker, J.-M. (2016). Segmentation of PLS Path Models by Iterative Reweighted Regressions. *JBR*, 69(10), 4583–4592.
- Hair, J.F. et al. (2016). Identifying and Treating Unobserved Heterogeneity with FIMIX-PLS: Part I. *EBR*, 28(1), 63–76.
- Matthews, L. et al. (2016). Identifying and Treating Unobserved Heterogeneity with FIMIX-PLS: Part II. *EBR*, 28(2), 208–224.
- Sarstedt, M. et al. (2022). Latent Class Analysis in PLS-SEM: A Review. *JBR*, 138, 398–407.

---

## 9. Robustness Checks

### Three Types of Uncertainty (Sarstedt et al., 2024)

Robustness checks address uncertainty beyond statistical significance:

1. **Methodological uncertainty**: Different SEM methods (PLS, PLSc, CB-SEM, GSCA) can produce different parameter estimates for the same model/data
2. **Model estimation uncertainty**: Within the same method, different analytical workflow decisions (indicator treatment, algorithm settings, assessment criteria) lead to different results
3. **Interpretational uncertainty**: Researchers interpret identical numerical results differently regarding significance, effect sizes, and implications

### Recommended Robustness Procedures (Sarstedt et al., 2020; Vaithilingam et al., 2024)

1. **Nonlinear effects**: First apply **Ramsey's RESET test** on each structural equation (non-significant F-test = linear model is robust). If RESET is significant, include quadratic interaction terms and test via bootstrapping.
2. **Endogeneity**: Apply the Gaussian copula approach (see Section 6). Test non-normality first using Kolmogorov-Smirnov with Lilliefors correction.
3. **Unobserved heterogeneity**: Run FIMIX-PLS (see Section 8)
4. **Sensitivity to influential observations**: Check for outliers and their impact on results
5. **Alternative model specifications**: Test competing theoretical models; use BIC/GM weights for model comparison
6. **Measurement model alternatives**: Test alternative indicator assignments; use CTA-PLS
7. **PLSc comparison**: Compare standard PLS and PLSc results for reflective models
8. **Multiverse analysis**: Run multiple specifications/methods and report the range of results to convey robustness (or lack thereof)

### Reporting Robustness

- Report that robustness checks were conducted (even if results are consistent)
- If results change under robustness checks, discuss implications
- Present robustness results in supplementary materials or an appendix
- Document all analytical decisions transparently (method choice rationale, algorithm settings, indicator removal decisions, threshold choices)

### Key References
- Sarstedt, M. et al. (2020). Structural Model Robustness Checks in PLS-SEM. *Tourism Economics*, 26(4), 531–554.
- Vaithilingam, S. et al. (2024). Robustness Checks in PLS-SEM: A Review. *JBR*, 173, 114465.

---

## 10. Missing Data in PLS-SEM

### Common Approaches

| Method | Description | When to Use |
|---|---|---|
| Mean replacement | Replace missing values with variable mean | Simple; biases variance estimates |
| EM algorithm | Iterative maximum likelihood estimation | Better than mean replacement; assumes MAR |
| Multiple imputation | Creates multiple complete datasets; pools results | Gold standard; accounts for uncertainty |
| Casewise deletion | Remove observations with any missing data | Only with MCAR and low missing rate |

### Recommendation Hierarchy (Amusa & Hossana, 2024; Liu et al., 2025)

Based on Monte Carlo simulation across MCAR, MAR, and MNAR conditions:

| Rank | Method | Best for | Notes |
|---|---|---|---|
| 1 | **Regression imputation** | All mechanisms, all rates | Least biased across conditions |
| 2 | **EM imputation** | MCAR, MAR | Strong second choice |
| 3 | **Multiple imputation** | MAR, moderate rates | Gold standard for uncertainty; accounts for imputation uncertainty |
| 4 | **Casewise deletion** | MCAR only, < 5% missing | Performance degrades rapidly at higher rates |
| 5 | **Mean replacement** | **Avoid** | Consistently worst; biases variance estimates |

**By missing rate**:
- < 5%: EM or regression imputation adequate; casewise deletion acceptable under MCAR
- 5–20%: Regression or multiple imputation recommended
- \> 20%: All methods degrade substantially; investigate the cause; consider whether data are usable
- Under MNAR: All methods produce some bias; regression imputation shows least bias

Always report the missing data rate, mechanism assessment, and treatment method.

### Key References
- Amusa, L.B. & Hossana, T. (2024). An Empirical Comparison of Some Missing Data Treatments in PLS-SEM. *PLOS ONE*, 19(1), e0297037.
- Liu, Y. et al. (2025). Tackling Missing Data in PLS-SEM: Strategies and Insights. *JBR*, 201, 115739.

---

## 11. PLS-SEM Combined with fsQCA

### Conceptual Foundation

PLS-SEM identifies **net effects** of individual predictors (symmetric, variable-oriented), while fsQCA identifies **configurations** (combinations) of conditions that produce an outcome (asymmetric, case-oriented). Combining them provides a more complete picture of complex phenomena (Rasoolimanesh et al., 2021).

### When to Combine PLS-SEM and fsQCA

- When equifinality is expected: multiple paths to the same outcome
- When the research question asks both "what matters on average?" (PLS-SEM) and "what combinations of factors lead to the outcome?" (fsQCA)
- When predictors may have asymmetric effects (presence vs. absence matters differently)

### Procedure

1. **Run PLS-SEM** to identify net effects, assess measurement models, and obtain construct scores
2. **Calibrate PLS-SEM construct scores** into fuzzy-set membership scores:
   - Full membership threshold: 0.95
   - Crossover point: 0.50
   - Full non-membership threshold: 0.05
3. **Run fsQCA** using calibrated scores:
   - Test for necessary conditions (consistency ≥ 0.90)
   - Identify sufficient configurations (consistency ≥ 0.80, conservative: ≥ 0.85)
   - Coverage threshold ≥ 0.20 for empirical relevance
4. **Compare and integrate** results: PLS-SEM shows average effects; fsQCA shows configurational pathways

### Key Reference
- Rasoolimanesh, S.M., Ringle, C.M., Sarstedt, M. & Olya, H. (2021). The Combined Use of Symmetric and Asymmetric Approaches: PLS-SEM and fsQCA. *IJCHM*, 33(5), 1571–1592.

---

## 12. Weighted PLS-SEM (WPLS-SEM)

### Purpose

When the sample does not represent the target population (e.g., oversampling of certain groups), standard PLS-SEM results may be biased. WPLS-SEM incorporates **sampling weights** to correct for non-representative samples (Becker & Ismail, 2016; Cheah et al., 2021). The WPLS algorithm modifies all calculations in the PLS iterative algorithm — weighted means, weighted variances, and weighted covariances — rather than naively pre-weighting the data matrix (which breaks due to PLS's internal standardization).

### 4-Step Procedure

1. **Choose the auxiliary variable** for sampling weights (must be correlated with the variable of interest; must NOT be an endogenous variable from the model; must NOT be related to response/non-response)
2. **Determine sampling weights**: Weight = (Proportion in Population) / (Proportion in Sample)
3. **Insert the weighting variable** into the PLS-SEM analysis
4. **Run weighted PLS-SEM** and compare results to unweighted analysis

### Requirements

- Minimum within-cell sample size: 10–20 observations
- Auxiliary variable must be available for both sample and population
- WPLS-SEM can produce different significance levels, effect sizes, mediation conclusions, and prediction results compared to standard PLS-SEM

### Key References
- Becker, J.-M. & Ismail, I.R. (2016). Accounting for Sampling Weights in PLS Path Modeling: Simulations and Empirical Examples. *EMJ*, 34(6), 606–617.
- Cheah, J.-H., Roldan, J.L., Ciavolino, E., Ting, H. & Ramayah, T. (2021). Sampling Weight Adjustments in PLS-SEM: Guidelines and Illustrations. *TQM&BE*, 32(13–14), 1594–1613.

---

## 13. Conditional Mediation (Moderated Mediation)

### Conceptual Foundation

Conditional mediation (CoMe) occurs when the strength of a mediated (indirect) effect depends on the level of a moderator. It extends both mediation and moderation analysis by examining whether the indirect effect varies across moderator levels.

### Five CoMe Model Types (Cheah et al., 2021)

| Model | What is Moderated | Description |
|---|---|---|
| **Model A** | Path b (M → Y) | Moderator affects the mediator-to-outcome path |
| **Model B** | Path a (X → M) | Moderator affects the predictor-to-mediator path |
| **Model C** | Both paths a and b (same moderator) | Same moderator affects both paths |
| **Model D** | Both paths a and b (different moderators) | Different moderators for each path |
| **Model E** | Direct effect (X → Y) | Moderator affects the direct path, not the indirect |

### CoMe Index (ω)

The conditional indirect effect at a specific moderator value is computed using the CoMe index:
- For Model A: ω = a × (b₁ + b₃ × W), where b₃ is the interaction coefficient
- For Model B: ω = (a₁ + a₃ × W) × b
- Evaluate at moderator values: mean, ±1 SD

### Procedure

1. Assess whether mediation exists (is the indirect effect significant?)
2. Assess whether the mediation is conditional (is the interaction term on a or b significant?)
3. Identify which path is moderated → select the appropriate model type
4. Use bootstrap percentile confidence intervals for all inference
5. Report: unconditional indirect effect, interaction effect, conditional indirect effects at moderator values, CoMe index, CIs

### Key Reference
- Cheah, J.-H., Nitzl, C., Roldán, J.L., Cepeda-Carrion, G. & Gudergan, S.P. (2021). A Primer on Conditional Mediation Analysis in PLS-SEM. *ACM SIGMIS Database*, 52(SI), 43–100.
