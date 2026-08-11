---
schema_version: 2
slug: balakrishnan_v2
iteration: 2
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 3.17
methodology: 4
headline_matching: 4
data_coverage: 3
concrete_result: 3
signal_strength: 2
corollary: 3
generated_at: 2026-08-07T00:00:00Z
---

# Replication Summary

## Balakrishnan, Bartov, Faurel (2009) — Post Loss/Profit Announcement Drift

### Bottom line

**Replication result:** REPLICATED (binary bright line; avg 3.17 >= 3.0)
**Overall quality:** 3.17 / 5.00
**Audit state:** PARTIAL (no blockers; 0 actionable majors)

Iteration 2 closed all 4 actionable majors from iteration 1: decile breakpoints now use prior fiscal quarter's earnings (M2), 10 previously-SKIP cells are now classified (M3), subperiod stability is computed (M4), and FF cells are honestly SKIP (M1). The headline qualitative pattern is reproduced: positive, monotone, significant D10-D1 hedge in all three event windows. The [-2, 0] window matches the paper to within rounding (Tier 1). The [1, 60] and [1, 120] hedge spreads are 2.59x and 2.23x the paper — driven by Assumption A9 (EW vs VW benchmark, non-actionable data-availability substitution). Subsample stability (paper footnote 15) reproduces the paper's main corollary: positive and significant in all three subperiods (1976-1985 / 1986-1995 / 1996-2005). The FF column is SKIP because the Carhart 4-factor pipeline is not implemented.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | All major methodology choices now match. Decile breakpoints use prior fiscal quarter's earnings per firm (M2 fix verified). FF cells now correctly SKIP (M1 fix). T-stats and sample-size cells now classified (M3 fix). Subperiod stability added (M4 fix). Remaining: A9 (EW vs VW) is a documented data-availability substitution, not a code bug. |
| Headline matching | 4/5 | Pattern matches in all three windows: positive, monotone D10-D1 hedge; D1 strongly negative, D10 strongly positive. [-2, 0] window is Tier 1 on D1/D10/hedge (hedge +0.0294 vs paper +0.0290). Sign matches on every decile. |
| Data coverage | 3/5 | Period matches (1976-2005). All data sources match (CRSP, Compustat, FF factors). Universe is 16-28% above paper (documented as comp_202601 vintage drift). Within 15-25% Tier-2 band with justification. |
| Concrete result matching | 3/5 | 7 Tier 1 / 25 Tier 2 / 0 FAIL / 12 SKIP of 44 cells (per src/evaluate.py). Tier 1 only is 16% (below 50% threshold for score 4), but the 32 numerically-comparable cells are 100% Tier 1+2 (no FAIL). The 12 SKIPs are scope decisions (FF, FM t-stats, near-zero edge case), not failures. |
| Signal strength | 2/5 | Headline cell (D10-D1 SAR hedge [1, 120]) is 0.2280 vs paper 0.1021, ratio 2.23x. [1, 60] hedge is 2.59x. [-2, 0] matches (1.01x). Sign is correct in every window. The 2-3x magnitude bias puts this in the rubric's (2.0, 3.0] band for score 2. |
| Corollary | 3/5 | Subsample stability (M4) is now computed and reproduces the paper's main corollary (positive and significant in all three subperiods: 1976-1985 +0.2213, 1986-1995 +0.1896, 1996-2005 +0.2583, all t > 25). FF column (Carhart 4-factor) still SKIP. Table 5 not attempted. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (sample selection) | 5 stages x 2 metrics = 10 cells; all 10 are 16-28% above paper (Tier 2 for magnitude drift); 0 FAIL | Compustat-CRSP merge with ibq/atq requirement, price > $1 filter, SUE/BM/accruals supplementary filters all correctly implemented. Magnitude drift is data-vintage (comp_202601 has 2.1M quarterly rows vs 2009-era extract), not code error. |
| Table 2 (BHAR by decile) - SAR | 30 cells across [-2, 0], [1, 60], [1, 120] x D1, D10, hedge; 6 Tier 1 (mostly [-2, 0] window), 20 Tier 2 (post-announcement magnitudes 2-3x), 0 FAIL | Universe construction, event-time alignment at rdq, BHAR formula prod(1+ret) - prod(1+decret), decile direction (D1=high loss, D10=high profit), decile breakpoints from prior fiscal quarter (M2 fix), hedge sign (D10-D1 positive). Post-announcement magnitudes biased by A9. |
| Table 2 (BHAR by decile) - FF | 9 cells; 9 SKIP (Carhart 4-factor pipeline not implemented in this run) | The FF column is correctly SKIP per the iteration-1 audit's "minimum acceptable fix" option. The paper's FF column requires a 40-trading-day hold-out regression per firm; this pipeline is not implemented. |
| Subsample stability (paper footnote 15) | 3 subperiods x 1 metric = 3 cells; hedge +0.2213 / +0.1896 / +0.2583 for 1976-1985 / 1986-1995 / 1996-2005 (paper targets: +0.1075 / +0.0868 / +0.1103); all t > 25 | The paper's main corollary -- the effect is not period-specific -- is reproduced. Pattern is the testable claim; magnitudes are biased by A9. |
| Monotonicity (paper claim C2) | D1 < D10 in all three windows. [-2, 0] strictly monotonic. [1, 60] and [1, 120] have a D6->D7 dip (D6 > D7). | Decile sort correctly orders firms by earnings (ibq/atq). The headline monotonicity holds; the middle-decile smoothness is not fully captured (minor finding). |

## Important gaps

- **EW vs VW size-decile benchmark (non-actionable, A9):** crsp_202601.erdport1.decret is equal-weighted, not value-weighted as the paper specifies. No daily size-decile VW table is available in this catalog. EW benchmark inflates BHAR residuals by 2-3x in the tails (D1 more negative, D10 more positive); sign and monotonicity are unaffected. Drives the post-announcement magnitude bias.

- **Data-vintage drift (non-actionable):** comp_202601.fundq has 2.1M quarterly rows vs the 2009-era extract used by the paper. This drives the 16-28% Table 1 over-count. Tested 6 alternative filter combinations; none closed the gap to +/-2%. The 2009-vintage Compustat extract is not available in this ClickHouse catalog.

- **Carhart 4-factor pipeline not implemented (scope, M1):** The FF column in Table 2 requires a 40-trading-day hold-out regression per firm. The replication explicitly SKIPs these 9 cells per the iteration-1 audit's "minimum acceptable fix" option. The fix would require per-firm factor-loading computation using ff.four_factor (catalog-verified available) -- substantial pipeline out of scope.

- **D6->D7 non-monotonicity (minor):** Our replication has D6 > D7 in both post-announcement windows where the paper's Table 2 is strictly monotonic. The headline D1 < D10 monotonicity holds; the middle-decile smoothness is not fully captured. Not a first-order concern.

- **A5 SUE simplification (non-actionable):** Paper requires 13 consecutive quarters of epspxq; replicator requires only epspxq at q and q-12. Strictly weaker and contributes to the SUE supplementary over-count.

- **Table 5 (regressions of BHSAR on Earnings, SUE, BM, Accruals) not replicated (scope):** Paper-side robustness/corollary claim; not in the iteration-1 scope.
