# Table 1 — Summary statistics of admitted-sample characteristics

Amihud (2002), Table 1. Source: data/panel.parquet rows with `admitted = 1`; characteristic years 1963-1996 (panel column `y` is the returns year = characteristic year + 1; 34 years).

Per year: cross-sectional mean, sample SD (n-1), and bias-adjusted Fisher-Pearson skewness (scipy `skew(bias=False)`). Aggregation over the 34 years: mean of annual means, mean of annual SDs, median of annual means, mean of annual skewness, min/max annual mean (paper's convention).

Tolerances: 5% (means / SDs / medians), 10% (skewness), 15% (min/max annual means). Status (repo rule, rep/TOLERANCE_RULES.md): Tier 1 = |dev| <= tol; Tier 2 = sign ok, |dev| > tol; FAIL = sign flip. Strict (audit/RUBRIC.md): Tier 1 = within tol; Tier 2 = sign ok AND 0.5 <= |ours/paper| <= 2; FAIL = sign flip OR ratio outside [0.5, 2].

## ILLIQ (x10^6)

| Statistic | OURS | PAPER | %dev | Status | Strict |
|---|---:|---:|---:|:---:|:---:|
| Mean of annual means | 0.3471 | 0.337 | +3.0% | Tier 1 | Tier 1 |
| Mean of annual SDs | 0.5379 | 0.512 | +5.1% | Tier 2 | Tier 2 |
| Median of annual means | 0.3116 | 0.308 | +1.2% | Tier 1 | Tier 1 |
| Mean of annual skewness | 3.072 | 3.095 | -0.7% | Tier 1 | Tier 1 |
| Min annual mean | 0.07217 | 0.056 | +28.9% | Tier 2 | Tier 2 |
| Max annual mean | 0.9831 | 0.967 | +1.7% | Tier 1 | Tier 1 |

## SIZE ($ millions)

| Statistic | OURS | PAPER | %dev | Status | Strict |
|---|---:|---:|---:|:---:|:---:|
| Mean of annual means | 836.3 | 792.6 | +5.5% | Tier 2 | Tier 2 |
| Mean of annual SDs | 1677 | 1612 | +4.1% | Tier 1 | Tier 1 |
| Median of annual means | 534.2 | 538.3 | -0.8% | Tier 1 | Tier 1 |
| Mean of annual skewness | 5.325 | 5.417 | -1.7% | Tier 1 | Tier 1 |
| Min annual mean | 256.1 | 263.1 | -2.6% | Tier 1 | Tier 1 |
| Max annual mean | 2587 | 2195 | +17.9% | Tier 2 | Tier 2 |

## DIVYLD (percent)

| Statistic | OURS | PAPER | %dev | Status | Strict |
|---|---:|---:|---:|:---:|:---:|
| Mean of annual means | 3.411 | 4.14 | -17.6% | Tier 2 | Tier 2 |
| Mean of annual SDs | 5.096 | 5.48 | -7.0% | Tier 2 | Tier 2 |
| Median of annual means | 3.461 | 4.16 | -16.8% | Tier 2 | Tier 2 |
| Mean of annual skewness | 5.995 | 5.385 | +11.3% | Tier 2 | Tier 2 |
| Min annual mean | 1.691 | 2.43 | -30.4% | Tier 2 | Tier 2 |
| Max annual mean | 6.513 | 6.68 | -2.5% | Tier 1 | Tier 1 |

## SDRET (percent, daily return x100)

| Statistic | OURS | PAPER | %dev | Status | Strict |
|---|---:|---:|---:|:---:|:---:|
| Mean of annual means | 2.135 | 2.08 | +2.6% | Tier 1 | Tier 1 |
| Mean of annual SDs | 0.7841 | 0.75 | +4.5% | Tier 1 | Tier 1 |
| Median of annual means | 2.101 | 2.07 | +1.5% | Tier 1 | Tier 1 |
| Mean of annual skewness | 1.068 | 1.026 | +4.1% | Tier 1 | Tier 1 |
| Min annual mean | 1.584 | 1.58 | +0.3% | Tier 1 | Tier 1 |
| Max annual mean | 2.889 | 2.83 | +2.1% | Tier 1 | Tier 1 |

**24-cell summary (repo rule, rep/TOLERANCE_RULES.md):** Tier 1 = 15, Tier 2 = 9, FAIL = 0. **Rubric-strict (audit/RUBRIC.md):** Tier 1 = 15, Tier 2 = 9, FAIL = 0.

**Rubric-strict note (audit/RUBRIC.md, per audit 1 [M1]):** the 34 repo-rule Tier-2 cells that become FAIL under the 2x magnitude bound are all paper-side noise cells (paper |t| <= 1 or statistically-zero coefficients) or documented A13/A15/A16 gaps: Table 2 = 19 (model-b BETA coef/t 6 at paper |t| <= 0.79, ratios 2.7-4.1, A15 compressed portfolio betas; DIVYLD coef/t 6, ratios 0.23-0.49, A13 dividend-yield vintage gap; near-zero constants 6 at paper |t| <= 1 — model-a all coef/t, model-a nojan t, model-a 1981-97 coef/t, model-b 1981-97 coef; lnSIZE 1981-97 coef 1 at 2.07x); Table 3 = 2 (g1_rsz10 OLS + NW t vs paper t = 0.13/0.14, ratios ~10.8 — statistically-zero paper cell, RSZ10 g1 = -0.447); Table 4 = 13 (g0 size-portfolio coef/t cluster 11, ratios 0.01-0.31, A16 paper-side intercept inconsistency; g1_rsz4 OLS + White t 2, ratios ~0.47-0.49). The repo-rule Status column (rep/TOLERANCE_RULES.md) remains the per-cell source of truth; the Strict column reports the audit-rubric classification.
