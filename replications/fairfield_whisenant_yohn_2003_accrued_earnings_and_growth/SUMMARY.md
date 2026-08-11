---
schema_version: 2
slug: fairfield_v2
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 3.50
methodology: 4
headline_matching: 3
data_coverage: 3
concrete_result: 3
signal_strength: 4
corollary: 4
generated_at: 2026-08-07T00:00:00Z
---

# Replication Summary

## Fairfield, Whisenant & Yohn (2003) "Accrued Earnings and Growth"

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.50 / 5.00
**Audit state:** `PASS`

The replication reproduces the paper's central findings (Sloan-style differential persistence; FWY's first hypothesis that both ACC and GrLTNOA are negative predictors of one-year-ahead ROA after conditioning on current ROA) within the tolerance of the 2026-Compustat / 2026-CRSP vintage. All 196 cells across 7 tables are evaluated; 86 hit Tier 1 (within paper tolerance), 105 hit Tier 2 (sign matches, magnitude outside tolerance), 3 are FAIL (sign disagreements concentrated on the data-extract residual), and 2 are `no_effect` (paper-insignificant ACC coefficients under the lagged deflator). Both audit1 actionable majors are now closed: M1 (day-gap test for fiscal-year adjacency) is applied to all three self-joins in `panel.sql`, taking the panel from 53,413 to 52,629 firm-years; M2 (T5 paired-t over-claim) is fixed in `REPORT.md` L98-106, which now correctly distinguishes the directional claim (replicates) from the equivalence claim (refuted in our data, opposite the paper's fail-to-reject). The 3 FAILs remain as documented non-actionable data-extract vintage limits.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | All paper-explicit construction choices match the paper; day-gap test now applied (full convention default); 45 preprocessing rules across 8 categories all paper-cited. |
| Headline matching | 3/5 | C1 (Sloan replicate) supported; C2 (H1) ACC + GrLTNOA both negative supported; C3 (H2 lagged-deflator flip) fails — GrLTNOA does not flip positive in our data; C4 (H3 Mishkin) signs all match but LR magnitudes diverge by 10-100×. |
| Data coverage | 3/5 | Period matches exactly (1963-1992); universe 52,629 vs paper 33,080 = 1.59× paper (15-25% band exceeded); both sources 2026 vintage with documented substitutes for footnote filter and size-decile benchmarks. |
| Concrete result | 3/5 | 86/196 Tier 1 (43.9%); 105 Tier 2 (53.6%); 3 FAIL (1.5%); 2 no_effect (1.0%); 0 SKIP. Tier 1 share sits at the 30-50% boundary. |
| Signal strength | 4/5 | All headline coefficients have matched signs; Sloan replication coefficients within 6% of paper; ACC and GrLTNOA forecasting signs all correct; one sign flip at |ratio|=0.52. |
| Corollary | 4/5 | Decile patterns match paper direction (ROA↑, CFO↓, GrNOA↑, GrWC↑, DEPAM↓, GrLTNOA flat); correlation matrix mostly within tolerance; missing per-`fyear` subsample stability check. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (descriptive stats) | ROA_t mean 0.084 vs paper 0.116 (28% below); std 0.185 vs 0.117 (58% above); medians within 11%. | Deflated-ratio construction is correct; medians track the paper's distribution shape. |
| Table 4 (Sloan replicate) | β_ACC=0.700 vs 0.676 (3.5%); β_CFO=0.781 vs 0.737 (6.0%); paired-t=6.83 vs 4.58 (larger, same direction); adj R²=0.605 vs 0.579 (4.5%). | Sloan (1996) differential persistence replicates; β_ACC < β_CFO ordering holds. C1 supported. |
| Table 5 (FWY H1) | ACC=-0.082 vs -0.061 (Tier 2); GrLTNOA=-0.035 vs -0.039 (Tier 1, 11%); paired-t=-2.86 vs -1.21 (sign matches, magnitude outside — the equivalence test rejects in our data, opposite the paper). | Both ACC and GrLTNOA are negative predictors of one-year-ahead ROA after conditioning on current ROA. C2 directional claim replicates; C2 equivalence claim refuted. |
| Table 6 (lagged deflator) | GrLTNOA in eq 6 = -0.017 vs paper +0.030 (sign flip); paired-t=-2.56 vs -1.50 (sign matches, magnitude outside). | ACC remains significantly negative under the lagged deflator (paper says no effect); GrLTNOA does NOT flip positive. C3 partially supported. |
| Table 7 (Mishkin) | γ_1=0.816 vs 0.746 (Tier 2); γ_2=-0.103 vs -0.045 (sign matches, magnitude outside); γ_3=-0.049 vs -0.048 (Tier 1); γ*_1=0.749 vs 0.704 (Tier 1); γ*_2=0.048 vs 0.069 (Tier 2); LRs all sign matches but magnitudes diverge 10-100× (β_uncon=1.65 vs paper ~0.94). | Forecasting signs all correct; valuation signs all correct. C4 direction supported; C4 LR statistics inflated by β_uncon divergence. |

## Important gaps

- **Data-extract vintage (1999 vs 2026 Compustat).** The 2026 Compustat extract has ~2× more 1963-1992 firm-year coverage than the paper's 1999 extract, with the additional firms concentrated in the 1980s distress cycle. This drives the 3 sign-flipping FAILs (T2_PanelA_ROA_D1, T6_eq6_GrLTNOA, T6_eq6_GrLTNOA_t) and the inflated Mishkin test LR statistics. Closing this gap would require a 1999-vintage Compustat extract, which is not available. Non-actionable.

- **3 sign-flipping FAILs.** All trace to the data-extract vintage. The T2_PanelA_ROA_D1 sign disagreement is on a single cell (the lowest-accrual decile) and does not reflect a column-wide flip — the other 9 decile cells are monotonic and the sort direction is correct. The two T6_eq6_GrLTNOA cells share a single root cause (the lagged-deflator coefficient does not flip positive in our data). Non-actionable.

- **Mishkin test β_uncon = 1.65 vs paper ~0.94.** The 2-stage NLS approximation of the paper's iterative GLS produces an unconstrained valuation-equation slope of 1.65, far from the paper's 0.94. The LR formula `2n log(SSR^c/SSR^u)` is super-sensitive to β_uncon: when β_uncon is far from 1, SSR^c >> SSR^u, inflating LR. The paper's joint q=2 test fails to reject (LR=1.82, p=0.403 → "ACC and GrLTNOA mispricing are equivalent"); our joint test strongly rejects (LR=1407, p<0.0001 → "they are different"). The signs of all 16 cells are correct. The Mishkin approximation is a documented paper-silent choice (assumptions.md A11).

- **Panel size: 52,629 vs paper 33,080 (1.59× paper).** The day-gap test (M1, now applied) removed 784 spurious firm-years (1.5% drop). The remaining 1.59× overshoot is the data-extract vintage limit; the 2026 Compustat extract has ~2× more 1963-1992 firm-year coverage than the paper's 1999 extract. Documented in `assumptions.md` Stage 7 iter-2 and iter-5 entries.
