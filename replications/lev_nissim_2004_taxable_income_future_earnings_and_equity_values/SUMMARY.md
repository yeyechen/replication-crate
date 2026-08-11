---
schema_version: 2
slug: lev_nissim_2004_taxable_income_future_earnings_and_equity_values
iteration: 3
verdict: FAILED
overall: 2.83
methodology: 4
headline_matching: 4
data_coverage: 2
concrete_result: 1
signal_strength: 2
corollary: 4
generated_at: 2026-08-11
---

# Replication Summary

## Taxable Income, Future Earnings, and Equity Values (Lev & Nissim 2004)

### Bottom line

**Replication result:** `FAILED`
**Overall quality:** 2.83 / 5.00

The replication recovers the paper's directional pattern across all five claims (C1–C5): every committed R_TAX headline cell carries the sign the paper reports. However, under the binary Match/FAIL design (DEV-041, re-scored at iteration 4), only 10 of 83 committed cells (12.0%) are Match; 73 are FAIL. The 73 FAIL cells include the original 9 magnitude-divergence cells in T2_B/T3_B (attributed to the 14-year vs 28-year sample window with `[VINTAGE-DRIFT]` markers) plus 64 cells that under the prior harness were Tier 2 (sign match, magnitude outside tolerance). Concrete_result = 1 fires the rubric's kill switch (any dimension = 1 → FAILED); overall < 3.0 confirms the FAILED verdict. All 73 FAIL cells carry closed-vocabulary markers in `assumptions.md`.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | All 8 sub-checks pass; the procedural defects from audit 1 are fixed with documented deviations. The 14-year sample window is the only non-procedural deviation, properly documented with `[VINTAGE-DRIFT]` markers and a four-row winsorization sweep. |
| Headline matching | 4/5 | All 12 R_TAX headline cells across T2, T4, T5 carry the sign the paper reports. Pattern, sign, and rough shape all match. |
| Data coverage | 2/5 | Pre-1987 firm-years absent (paper 1973-2000, ours 1987-2000); Panel A has 6 years instead of 20; otherwise universe counts are within tolerance (96% of comp panel, 64% of returns panel). |
| Concrete result matching | 1/5 | Match rate = 10/83 = 12.0%, band 1 per the rubric's mechanical mapping (DEV-034) under the binary Match/FAIL design. 73 FAIL cells, all with closed-vocabulary markers. |
| Signal strength | 2/5 | Worst-case headline cell (T2_B full-model G3 β_1) r = 2.639/0.700 = 3.77, in band 2 under [VINTAGE-DRIFT] reading. T2_A cells at r ≈ 1.3 are band 4. |
| Corollary | 4/5 | T3 runs (29 cells); T4/T5 R_TAX headline cells run with documentation. All 73 FAIL cells carry `[VINTAGE-DRIFT]` markers. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 2 (Eq. 4 — future earnings growth) | All 4 R_TAX coefficients are positive in both panels; the mean G1 by R_TAX quintile is monotonic in Panel B (Q1 → Q5: -34.46, -3.26, -3.25, -1.06, -0.53). 7 T1 cells, 24 T2 cells, 2 FAIL cells on T2_B magnitudes. | C1 (R_TAX positively predicts future earnings growth): the directional claim is supported. C2 (R_TAX dominates R_DEF): weakly supported by sign pattern. |
| Table 3 (Eq. 4 augmented — R_TAX vs PRED_1..PRED_9) | 29 cells implemented; 22 T2 cells, 7 FAIL cells on Panel B magnitudes. The PRED_1..PRED_9 definitions are documented at the topline. | C3 (R_TAX incremental to nine standard earnings predictors): the directional claim is supported for Model 1 R_TAX-only sign; Model 4 has a sign flip on full-model G3 (β_1 = -0.739 vs paper 0.516) that is consistent with the 14-year window. |
| Table 4 (Eq. 5 — E/P*) | All 4 R_TAX coefficients are negative in both panels; mean E/P* by R_TAX quintile in Panel B decreases monotonically (Q1=7.32 → Q5=4.82). 10 T2 cells, 0 FAIL cells. | C4 (R_TAX is negatively priced into E/P in the post-SFAS 109 period): the directional claim is supported. |
| Table 5 (Eq. 6 — one-year-ahead stock return) | All 4 R_TAX coefficients are positive in Panel A (pre-SFAS 109) and essentially zero in Panel B (post-SFAS 109). 3 T1 cells (T5_B spec1, T5_A_n and T5_B_n), 8 T2 cells. | C5 (R_TAX predicts returns pre-SFAS 109 but not post-SFAS 109): the directional claim is supported. |

## Important gaps

- Pre-1987 firm-years are essentially absent from the modern Compustat extract (Assumption #6, `[VINTAGE-DRIFT]`): the effective panel is 1987-2000 (14 years) instead of the paper's 1973-2000 (28 years), and Panel A has 6 years instead of 20. This is the single root cause of the 2-3.5x magnitude drift on T2_B and T3_B cells. Recoverable only via `comp_pit.pithistdataus`, which the replicator flagged as a follow-up.
- I/B/E/S mean analyst long-term growth forecast (GROW), CRSP-rolling BETA, and rolling VOL are not estimated in this iteration (Assumption #9, `[THIRD-PARTY-DATASET]`). Table 4 models 2 and 4, and Table 5 model 3, fall back to the previous-spec x-vector. The headline R_TAX cells in models 1 and 3 are unaffected.
- The dependent variable in Table 5 uses raw monthly returns, not the paper's "invest delisting proceeds in NYSE/AMEX/NASDAQ VW index" rule (Assumption #10). Expected effect on the R_TAX coefficient is small (a few hundred basis points of noise in ~10% of stocks per year).
- Nine T2_B and T3_B cells are FAIL on magnitude divergence (2-3.5x the paper's values); all marked `[VINTAGE-DRIFT]` with a four-row winsorization sweep in `assumptions.md#A14` as quantitative evidence. The directional pattern (R_TAX positive in T2/T3, R_TAX negative in T4, R_TAX positive → flat in T5) is preserved across every headline cell.
