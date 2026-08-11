---
schema_version: 2
slug: anderson_v2
iteration: 2
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 3.50
methodology: 4
headline_matching: 4
data_coverage: 4
concrete_result: 3
signal_strength: 3
corollary: 4
generated_at: 2026-08-07T00:00:00Z
---

# Replication Summary

## Anderson & Garcia-Feijoo — "Empirical Evidence on Capital Investment, Growth Options, and Security Returns" (2002 draft)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.50 / 5.00
**Audit state:** `PARTIAL`

The paper's central claim — that firms which grew capital expenditures fastest over the prior two years earn systematically lower subsequent stock returns, and that an investment-based factor prices investment-sorted portfolios as well as the Fama-French three-factor model — reproduces. All seven audit-1 majors are resolved with verified evidence: the Table V value-weight look-ahead is fixed using lagged ME (FF-conformant), the Ln(inv) magnitude FAIL is no longer retired by an untested causal story (Table I range and per-SD effect diagnostic together retire the Compustat-vintage hypothesis and re-classify the gap as an unidentified regressor-scale difference), the 36-month return-history filter is implemented, β is joined into the FM panel, subperiod and January-exclusion results are computed, and Table I Panel A is added. The remaining gaps are documented non-actionable data-availability limits (no alternative-vintage Compustat pull available; β distribution broader than FF-NYSE-only convention).

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | All six major methodology checks pass; β universe documented as broader than FF-NYSE-only convention; 36-mo filter implemented; lagged VW weights; formation-month ME for ln_size; plain t-stat |
| Headline matching | 4/5 | Three of five headline cells match in shape, sign, and magnitude class (decile spread, INV loadings Q1/Q5, INV factor mean). Ln(inv) FM coefficient 16× off in raw units but per-SD effect matches within 0.02 %/mo |
| Data coverage | 4/5 | Period exact (276 months, 1976-07…1999-06); sources match; 79 % signal coverage; 36-mo filter applied |
| Concrete result matching | 3/5 | 28/50 = 56 % Tier 1 (in 50-70 % band); 42/50 = 84 % Tier 1 + Tier 2 (would be 4/5). Ln(inv) coefficients and β cells account for the FAILs |
| Signal strength | 3/5 | Headline cells: spread r=0.99, INV loadings r≈0.99, INV factor mean r=1.43. Ln(inv) FM coefficient r=0.062 but per-SD effect matches |
| Corollary | 4/5 | Subperiods, Jan-exclusion, INV loadings monotone, factor correlations, SMB sign pattern all replicate. β-null corollary does not replicate as a null; documented as non-actionable |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table II — 10 EW decile returns (claim C2) | Decile spread −0.78 %/mo vs paper −0.79; max cell deviation 0.14 %/mo; 11/11 PASS, 9/11 Tier 1 | Universe construction, FF-style annual rebalancing, decile sort, EW returns. The paper's core empirical claim. |
| Table III Panel A — Fama-MacBeth (claim C3) | Ln(size) 7/7 Tier 1; Ln(B/M) coefficients Tier 1; Ln(inv) t-statistics Tier 1/Tier 2 across 4 models; subperiod stability ✓ | FM procedure, plain (non-HAC) t-statistic, formation-month ME for `ln_size`. The paper's strongest cross-sectional claim. |
| Table III subperiods | Ln(inv) t = −5.15 / −4.85 / −6.16 across 1976-87 / 1987-99 / Feb-Dec masks | Robustness: effect holds across subperiods and after January exclusion |
| Table V Panel A — INV factor (claim C5) | INV factor mean 0.34 %/mo vs paper 0.24; loadings Q1 −0.524 / Q5 +0.476 vs paper −0.530 / +0.470; corr(INV, MKT-RF) −0.29 vs −0.24; corr(INV, HML) +0.44 vs +0.38 | INV factor construction, FF-style VW with lagged weights, the investment factor's identity as a priced factor |
| Table I Panel A (claim C1) | Means 0.197-1.292 (paper 0.17-1.03); medians −0.024-0.715 (paper −0.05-0.54); monotone pattern across B/M within size | Universe construction with NYSE breakpoints; the `inv_growth` distribution matches the paper's distribution. Retires the Compustat-vintage hypothesis for the Ln(inv) magnitude gap. |

## Important gaps

- **Ln(inv) FM coefficient magnitude is 16× off in absolute units** (β = −0.26 vs paper −4.19). Per-SD effect matches within 0.02 %/mo and Table I range rules out the Compustat-vintage hypothesis; the specific regressor/units form used by the paper is not identifiable from this single-vintage pull. Non-actionable.
- **β null in models 1 and 7 does not replicate as a null.** β distribution (std 0.75) is broader than the FF-NYSE-only convention (std 0.3-0.5). Substantive inference (β does not dominate the Ln(inv) signal) still replicates. Non-actionable.
- **Table IV (joint investment × size × B/M, claim C4) not replicated.** Out-of-scope for this iteration.
- **Table V Panels B and C (B/M- and MVE-sorted) not replicated.** Only Panel A is committed.
- **Delisting returns not adjusted.** Paper silent; uses raw returns throughout. Low impact for monthly EW deciles.
