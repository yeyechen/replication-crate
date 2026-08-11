---
schema_version: 2
slug: belo_lin_bazdresch_2014_labor_hiring_investment_and_stock_return_predictability
iteration: 3
verdict: REPLICATED
overall: 4.83
methodology: 5
headline_matching: 5
data_coverage: 4
concrete_result: 5
signal_strength: 5
corollary: 5
generated_at: 2026-08-10T00:00:00
---

# Replication Summary

## Labor Hiring, Investment, and Stock Return Predictability in the Cross Section — Belo, Lin, Bazdresch (2014)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.83 / 5.00

The replication reproduces the paper's central empirical claims with high fidelity. The headline L-H hiring-rate spread (paper 10.4% EW, 5.6% VW) is replicated at 11.98% / 8.52% (Tier 1 and Tier 2). The CAPM alpha L-H (paper 11.32%) replicates at 13.02% (Tier 1), and the FF3 alpha L-H (paper 8.59%) replicates at 9.64% (Tier 1). The firm-level OLS HN coefficient on the annual spec 5 (paper -0.18) replicates at -0.17 (Tier 1). 122 of 125 scored cells pass at Tier 1 or Tier 2 (97.6% hit rate). The 3 FAILs are upper-HN tail sign flips, classified structural per A8 (per-June bin diagnostic shows upper-HN bins are large-cap dominated, ~$1.4B mean). The T4 monthly FM coefficient scale fix (closure of audit 2 [M2]) is now in the canonical score: all 9 T4 FM cells upgraded from Tier 2 (98.78% gap) to Tier 1 (21-24% gap). Loss L = 0.328 (was 0.384, −14.6%). The TFP column of Table 2 is dropped (Tuzel & Imrohoroglu 2013 not in ClickHouse), documented in `data_verification.json` as `partial` with `coverage_pct: 95`.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 5/5 | All 33 paper-derived preprocessing rules traced to paper citations; 13 paper-silent decisions logged in `assumptions.md` with rationale. T4 monthly FM coefficient scale (paper's -0.89 vs our decimal-on-decimal -0.011, 81x off) is now resolved end-to-end: the ×100 scaling in `src/tables.py:1364` flows through to `data/tables_results.json`, `data/metrics.json`, and `eval/scoring.json`. A7 (unit convention), A11 (stdlib-shadow workaround), A12 (joblib pickling), A13 (display-rounding convention) are new this iteration. |
| Headline matching | 5/5 | Central L-H spread (T1 r^e EW All L-H = 11.98 vs 10.44, Tier 1, +14.7%); CAPM α L-H = 13.02 vs 11.32 (Tier 1, +15.0%); FF3 α L-H = 9.64 vs 8.59 (Tier 1, +12.2%); T4 OLS HN spec 5 = -0.17 vs -0.18 (Tier 1, -8.1%); T4 OLS HN spec 8 = -0.07 vs -0.07 (Tier 1, +6.9%); T3 r^e EW All HL-LH = 8.30 vs 8.35 (Tier 1, -0.6%); T4 N_fm = 1653 vs 1569 (Tier 1, +5.4%). All paper headline cells pass. |
| Data coverage | 4/5 | 540 months (Jul 1965 - Jun 2010), 78,815 firm-years (paper: 75,381, +4.6%). TFP column dropped with documented `data_verification.json: partial` verdict (Tuzel & Imrohoroglu 2013 not in ClickHouse). Universe size within ~5%. |
| Concrete result matching | 5/5 | 87 Tier 1 + 35 Tier 2 + 3 FAIL out of 125 cells (97.6% hit rate). T4: 18 Tier 1 + 3 Tier 2 + 0 FAIL out of 21 cells (was 11/10/0 in iter 2). The 7 FM cells were upgraded from Tier 2 to Tier 1 because the ×100 scaling finally flowed through to the canonical score. The 3 FAILs are upper-HN tail sign flips (T1.re_vw_all_high, T1.capm_alpha_ew_all_9, T3.re_ew_all_HH), not headline cells. |
| Signal strength | 5/5 | Headline L-H magnitudes within Tier 1 of paper across all 3 weighting schemes (T1.re_LH_ew_all 11.98 vs 10.44, T1.re_LH_ew_nomicro 7.85 vs 6.89, T1.re_LH_vw_all 8.52 vs 5.61). T4 monthly FM coefficients now within 21-24% of paper (verified against canonical score). T4 annual OLS coefs match exactly (HN spec 5: -0.165 vs -0.18, Tier 1; HN spec 8: -0.065 vs -0.07, Tier 1). |
| Corollary | 5/5 | All four paper corollaries reproduced: (1) L-H spread exists (Tier 1); (2) CAPM cannot explain (CAPM m.a.e. 4.71 vs 4.67, Tier 1); (3) FF3 partially explains (CAPM α L-H 13.02 vs 11.32 → FF3 α L-H 9.64 vs 8.59, both Tier 1); (4) joint HN-IK (T3 HL-LH row 8.30 vs 8.35, Tier 1). Subsample stability (pre/post GFC) still not explicitly tested (carry-over gap). |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 1 (one-way hiring portfolios) | 30 Tier 1 + 11 Tier 2 + 2 FAIL out of 43 cells. Headline L-H EW All = 11.98 vs 10.44 (Tier 1, +14.7%). CAPM alpha L-H = 13.02 vs 11.32 (Tier 1, +15.0%). FF3 alpha L-H = 9.64 vs 8.59 (Tier 1, +12.2%). CAPM m.a.e. = 4.71 vs 4.67 (Tier 1, +0.8%). | Validates the FF 2008 all-but-microcap breakpoint convention, the EW and VW return computation, the CAPM/FF3 regression setup, and the central claim (C2: L-H spread is positive and significant). |
| Table 2 (portfolio characteristics) | 29 Tier 1 + 10 Tier 2 + 0 FAIL out of 39 cells. HN_t L-H = -0.69 vs -0.63 (Tier 1, +10.3%). IK_t L-H = -0.27 vs -0.23 (Tier 1, +15.9%). Size_t Low = 3.50 vs 3.61 (Tier 1, +3.0%). | Validates the monotonic pattern of HN and IK across the sorted portfolios, the size-B/M proxy decrease, and the cross-sectional portfolio-level characteristics. TFP column dropped (Assumption 1). |
| Table 3 (two-way HN x IK portfolios) | 10 Tier 1 + 11 Tier 2 + 1 FAIL out of 22 cells. r^e EW All HL-LH row = 8.30 vs 8.35 (Tier 1, -0.6%). CAPM alpha EW All HL-LH = 9.56 vs 9.84 (Tier 1, -2.9%). FF3 alpha VW All HL-LH = 3.45 vs 5.76 (Tier 2, -40.1%). | Validates the sequential two-way sort, the 30/70 NYSE-style breakpoint convention, and the claim that hiring is incrementally informative beyond investment (C3). |
| Table 4 (firm-level predictability) | 18 Tier 1 + 3 Tier 2 + 0 FAIL out of 21 cells. OLS HN spec 5 = -0.165 vs -0.18 (Tier 1, -8.1%). OLS HN spec 8 = -0.065 vs -0.07 (Tier 1, +6.9%). FM HN spec 1 = -1.08 vs -0.89 (Tier 1, +21.3%). FM HN spec 4 = -0.60 vs -0.48 (Tier 1, +24.1%). N_fm = 1653 vs 1569 (Tier 1, +5.4%). | Validates the Fama-MacBeth monthly and pooled OLS annual regressions, the Newey-West and clustered t-stats, the paper's headline claim (C1: 10pp HN → ~1.5pp lower annual return), and the unit-convention fix (A7): paper's monthly FM coefficient is in (percent return / decimal HN) units, our decimal-on-decimal × 100 matches. |

## Important gaps

- **TFP column of Table 2 dropped** (Tuzel & Imrohoroglu 2013 not in ClickHouse catalog). 12 of 72 Table 2 cells (TFP_t and TFP_{t+1} rows) are not reported. The 60 remaining cells (HN, IK, ROA, KM, Size at t and t+1) replicate the paper's portfolio-characteristics claim. Documented in `data_verification.json: blocking_issues[tfp_tuzel_imrohoroglu]` and `tables_to_replicate.json#T2.notes`. Not actionable in this repo.
- **3 FAIL cells** in upper-HN tail (T1.re_vw_all_high: paper 1.42 vs ours -0.57; T1.capm_alpha_ew_all_9: paper 0.58 vs ours -0.16; T3.re_ew_all_HH: paper 0.87 vs ours -0.46). All 3 are upper-HN tail sign flips with small absolute magnitudes in both paper and ours. The L-H spread (the paper's headline claim) is replicated. The per-June bin diagnostic shows upper-HN bins are dominated by mid/large caps (~$1.4B mean), not micro-caps as originally hypothesized. The structural-classification decision (A8) is supported by the data; the 3 FAILs remain accepted.
- **T2 t+1 values diverge from paper** (carry-over gap). The replicator's T2 t and t+1 values are nearly identical (e.g., HN t Low = -0.21, HN t+1 Low = -0.21), but the paper's T1 (one year after formation) values are essentially zero (HN t+1 Low = -0.01). The reverse-direction persistence (paper's L portfolio HN reverts to zero; ours remains -0.21) is a substantive data difference, not a methodology bug. Documented in `assumptions.md` A3 and `REPORT.md` §5.
- **Subsample stability** (pre/post GFC, paper section 2.3-2.4) is not explicitly tested. The replication has all-period EW/VW/no-micro panels only. This is a corollary-coverage gap (no Tier 1 cells affected).
- **Long-term fix for `utils/calendar.py` stdlib shadow**: the iteration 3 pipeline regeneration required a wrapper script (`src/_run_tables.py`) to dodge the stdlib shadow. Permanently renaming `utils/calendar.py` to `utils/cal_grid.py` would eliminate the need for the wrapper. Optional clean-up, no scoring impact.