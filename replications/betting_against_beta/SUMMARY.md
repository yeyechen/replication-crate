> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: betting_against_beta
iteration: 3
audit_verdict: PARTIAL
verdict: REPLICATED
overall: 4.17
methodology: 4
headline_matching: 5
data_coverage: 4
concrete_result: 4
signal_strength: 5
corollary: 3
generated_at: 2026-07-22T18:05:00Z
---

# Replication Summary

## Betting Against Beta (Frazzini & Pedersen, 2014)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.17 / 5.00
**Audit state:** `PARTIAL` (one documentation-only major + two trivial reporting fixes remain)

The paper's central claim — that a Betting-Against-Beta factor (long
leveraged low-beta US stocks, short de-leveraged high-beta stocks) earns
large, significant risk-adjusted returns — replicates cleanly. The BAB
factor matches the paper within tolerance on all eight Table 3 metrics
(Fama-French 3-factor alpha 0.75% vs 0.73%, iid t=7.11 vs 7.39; annualized
Sharpe 0.75 vs 0.78; leverage $1.44/$0.69 vs $1.40/$0.70), and the signature
patterns — a flat security market line, and Sharpe ratios and alphas that
decline monotonically from low- to high-beta deciles — all reproduce.

Four corollaries are now verified (the auditor re-derived the newest one
number-for-number with independent code):
- **Subsample stability [M1]**: BAB positive in all four 20-year subperiods,
  significant in 3 of 4 (SP1 1928-1948 positive but sub-significant).
- **Factor loadings [M2]**: all four BAB loadings carry the paper-predicted
  sign (market ≈0, HML positive, UMD positive, SMB ≈0).
- **Decile-alpha diagnosis [M5]**: post-1962 test confirms the P10 FF4 sign
  flip is economically negligible (t=0.08); P1 FF4 matches the paper exactly.
- **Cross-sectional variation by size [M3]**: BAB positive and significant
  in all three lagged-ME size terciles (all FF3 |t|>3.7), confirming the
  paper's "within deciles sorted by size" claim (Table B3).

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Beta estimation and BAB construction match the paper exactly; deviations are paper-silent and documented. |
| Headline matching | 5/5 | BAB factor within ~5% on all 8 cells; monotonic patterns reproduce. |
| Data coverage | 4/5 | CRSP + Fama-French sources match; universe within 1%; effective start 1928-08 vs 1926-01. |
| Concrete result matching | 4/5 | 25/32 cells (78%) within tolerance; 7 misses are decile multi-factor alphas (diagnosed as data-vintage-limited). |
| Signal strength | 5/5 | Headline BAB alpha, Sharpe, and excess return all within 10%. |
| Corollary | 3/5 | Subsample (directional), factor loadings (full), decile diagnosis (full), size split (full). Beta-window robustness and IVOL control uncomputed. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table 3 — BAB factor | All 8 metrics within tolerance: FF3 α 0.75% (t=7.11), Sharpe 0.75, realized beta −0.06, leverage $1.44/$0.69. | The paper's headline result and the unit-beta, rank-weighted construction. |
| Table 3 — beta deciles | Sharpe ratios fall monotonically 0.73→0.30; excess returns are flat; ex-ante betas rise 0.62→1.77. | The flat security market line (Proposition 1). |
| Table 1 — summary stats | 23,407 stocks vs 23,538 (0.6%); June mean firm ME 0.996 vs 0.99 $B. | Correct CRSP universe and market-equity computation. |
| Subsample stability [M1] | BAB positive in all four 20-year subperiods, significant in 3/4. | Temporal robustness of the BAB premium. |
| Factor loadings [M2] | Market ≈0, HML +0.061, UMD +0.200; decile SMB gradient confirms low-beta = larger. | BAB alpha not explained by standard risk factors. |
| Size split [M3] | BAB positive & significant in all 3 size terciles (FF3 |t|>3.7). | Cross-sectional robustness (Table B3). |

## Important gaps

- Beta-window robustness (Table B2) not computed (scope-out documented below).
- Idiosyncratic-vol control (Table B5) not computed (needs daily residual-vol).
- Five-factor alpha not replicated (Pastor-Stambaugh liquidity factor unavailable).
- International equities, other asset classes, TED-spread tests, and constrained-investor holdings not replicated (data unavailable).
- Decile multi-factor alphas run systematically high; confirmed as data-vintage-limited via post-1962 test.
