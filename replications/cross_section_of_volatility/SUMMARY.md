---
schema_version: 2
slug: cross_section_of_volatility
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 4.17
methodology: 4
headline_matching: 5
data_coverage: 4
concrete_result: 4
signal_strength: 4
corollary: 4
generated_at: 2026-07-22T17:40:00
---

# Replication Summary

## The Cross-Section of Volatility and Expected Returns (Ang, Hodrick, Xing & Zhang 2006)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.17 / 5.00 (audit 1: 3.83)
**Audit state:** `PASS` (0 blockers, 0 actionable majors; iteration loop closed)

The paper's central and most-cited claim — that stocks with high idiosyncratic volatility (relative to the Fama–French three-factor model) earn abysmally low average returns — is strongly reproduced. The value-weighted high-minus-low quintile spread in mean monthly returns is −1.02% (paper −1.06%; auditor recomputation −1.03%), and the monotonically decreasing return pattern from low- to high-volatility quintiles is recreated almost exactly. The corrected FF-3 alpha spread is −1.17% (paper −1.31%), now internally consistent with the Table XI full-sample alpha and produced with market betas ≈ 1. The anomaly survives every replicable cross-sectional control (size, book-to-market, leverage, volume, turnover, coskewness), all four L/M/N formation/holding-horizon strategies (up to one year), and seven of eight subsamples. The two remaining robustness misses (past-1-month momentum attenuation, volatile-period subsample) were tested under both alternative conventions and are documented as microstructure/small-sample limitations, not methodology errors. The systematic-volatility half of the paper (Tables I–V, IX) is out of scope because the required VIX/VXO data is unavailable in the database.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Audit-1's methodology bug (Table VI double-rf + factor-month misalignment) is fixed and auditor-verified: holding-month relabel + single rf gives betas ≈ 1 (sanity-gated in code) and 5-1 α = −1.177 (auditor recomputation) reconciled exactly with Table XI. Signal construction (daily FF-3 residual std, n ≥ 17), PIT universe filters, value-weighting, signal→return timing, look-ahead-free Compustat mapping, and NW(4) inference all check out; remaining deviations are paper-silent choices documented with justification (one — the past-1-month window — tested under both conventions). |
| Headline matching | 5/5 | Shape (rise then precipitous drop), sign (negative spread), and magnitude class all match; raw 5-1 spread within ~3–4%, FF-3 alpha spread within ~10–11% of the paper. |
| Data coverage | 4/5 | Exact period (Jul 1963–Dec 2000, 450 holding months, ~4,742 stocks/formation month), universe consistent with the paper's reported market-share statistics (Q1 53.7% vs 53.5%; Q5 1.98% vs 1.9%), matching sources (CRSP, Compustat, daily + monthly Fama–French). Deducted for the uncovered systematic-volatility half (no VIX/VXO). |
| Concrete result matching | 4/5 | Auditor tally of 69 headline cells: 89.9% Tier 1, 8.7% Tier 2, 1.4% FAIL. All four Table X strategies and the corrected Table VI alphas are Tier 1; the sole FAIL is the volatile-period 5-1 (ratio 0.27). Just under the 90% band for a 5. |
| Signal strength | 4/5 | Headline raw spread r ≈ 0.96 (within 10%) but FF-3 alpha spread r ≈ 0.89 — just outside the 10% band for a 5, comfortably within 20%. |
| Corollary | 4/5 | All four L/M/N horizon strategies replicate (1/1/12 9%, 12/1/12 15%, 12/1/1 27%, 1/1/1 22%; all t ≤ −3.0), all seven cross-sectional controls, 7/8 subsamples, and the loser/winner momentum asymmetry. Two documented deviations (past-1-month, volatile period); Table IX externally blocked. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table VI Panel B (IVOL sorts — core result) | Quintile means 1.04→0.01% reproduce the paper's shape; 5-1 raw spread −1.02% vs −1.06%; corrected FF-3 5-1 α −1.17 vs −1.31 with betas ≈ 1 (auditor recomputation: −1.177, betas 0.92–1.20); Q5 size 2.52 (exact), market share 1.98% vs 1.9%. | Correct IVOL signal, sorting, value-weighting, timing, alpha convention, and the headline anomaly itself. |
| Table VI Panel A (total-volatility sorts) | 5-1 raw spread −0.98% vs −0.97%; FF-3 5-1 α −1.08 vs −1.19; same monotonic-then-drop shape. | The anomaly is not an artifact of the FF-3 residualization. |
| Table VII (cross-sectional controls) | All seven 5-1 FF-3 alpha spreads within ~20% (size −1.01 vs −1.04, auditor-verified; turnover −1.40 vs −1.46; size-quintile-2 detail −1.91 exact). | The effect is not subsumed by size, value, leverage, volume, turnover, or coskewness, and is strongest in mid-caps. |
| Table VIII (momentum controls) | Past-6-month (−1.13 vs −1.10) and past-12-month (−1.06 vs −1.22) match; loser 5-1 −2.69 vs −2.25, winner −0.52 vs −0.48. | The effect persists within every momentum quintile, asymmetrically strongest among past losers. |
| Table X (L/M/N horizons — completed this iteration) | All four strategies: 1/1/1 5-1 α −0.68 vs −0.88; 1/1/12 −0.61 vs −0.67 (auditor re-implementation matched exactly); 12/1/1 −0.82 vs −1.12; 12/1/12 −0.65 vs −0.77. 12-month IVOL verified to machine precision vs direct pooled daily regression. | The anomaly is not a short-horizon or contemporaneous-measurement artifact; it persists across formation and holding periods up to one year. |
| Table XI (subsamples) | All four decades (1981–90: −2.12 vs −2.23), NBER expansions (−1.16 vs −1.25) and recessions (−1.44 vs −1.79), stable periods (−1.95 vs −1.71); full-sample row reconciles exactly with Table VI (−1.17 = −1.17, auditor-verified). | Temporal stability of the anomaly across regimes. |

## Important gaps

- **Past-1-month momentum attenuation does not replicate (documented limitation):** the paper's strong attenuation (5-1 α −1.31 → −0.66) is not reproduced under either convention (−1.15 with ret_{t−1}, −1.25 with ret_t; both auditor-verified, both Tier 2 at ratio < 2). Likely microstructure (bid-ask bounce) not recoverable from monthly CRSP returns; both conventions documented in results/table_8.md.
- **Volatile-period subsample attenuated (documented limitation):** 5-1 α −0.24 vs paper −0.89 (the sole FAIL cell). The 90-month classification was verified exactly (1.126%/5.050% thresholds) and a formation-month sensitivity was tested (−1.21, but it destroys the stable-vs-volatile contrast); the cell is genuinely small-sample-sensitive under both conventions.
- **Systematic-volatility analysis not replicated (external limitation):** Tables I–V and IX (β_ΔVIX sorts, FVIX factor, price of volatility risk) require CBOE VIX/VXO data absent from the database (assumptions.md A7).
- **Minor bookkeeping (see logs/audit2.md):** REPORT.md and table_8.md disagree on which past-1-month convention shipped (−1.15 vs −1.25); data/ivol12.parquet trips the prep_validation allowlist (rename suggested). Neither affects any result.
