---
schema_version: 2
slug: the_cross_section_of_expected_stock_returns
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 4.17
methodology: 4
headline_matching: 4.5
data_coverage: 4
concrete_result: 4
signal_strength: 4
corollary: 4.5
generated_at: 2026-07-22T18:56:24Z
---

# Replication Summary

## The Cross-Section of Expected Stock Returns (Fama & French 1992, *Journal of Finance* 47(2))

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.17 / 5.00
**Audit state:** `PASS`

All four of the paper's central claims replicate from CRSP/Compustat over July 1963 – December 1990, and the iteration-2 audit confirms the replication is complete: market β is not priced (β-alone slope 0.07 %/mo, t 0.22; every combined-regression β t-stat within 0.7 of zero, matching the paper's own prose), size is reliably negatively priced (ln(ME) −0.14, t −2.47; size-decile returns 1.48→0.87 vs the paper's 1.52→0.89), BE/ME is positively priced and dominant (0.49, t 5.54; BE/ME-sorted returns 0.41→1.79 with flat betas), and size plus BE/ME absorb leverage and E/P (E(+)/P collapses 5.55→1.59; the E/P dummy is killed). The strongest evidence is Table I's 100-portfolio structure (107/107 targeted cells) and the Fama-MacBeth matrix, where every priced-variable coefficient lands within ~10% of the paper. The previously-missing January-seasonality corollary is now computed and auditor-verified: January ln(BE/ME) slopes 0.606 %/mo versus February–December 0.318 (1.9×, Feb–Dec t 3.85, within 0.024 of the full-year mean) — all three elements of the paper's claim hold. A `REPLICATED` verdict does not mean every printed number matched: 88.7% of targeted cells are within tolerance, and the remaining deviations are diagnosed data-vintage effects plus two sign flips on statistically null coefficients.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Frozen in iteration 2 and verified unchanged: every construction rule traces to a paper citation (June sorts with NYSE breakpoints, Dimson sum-betas, December-t−1 ME for ratios / June-t ME for size, 0.5% winsorization of the four ratios, plain time-series Fama-MacBeth t-stats). Paper-silent choices (delisting returns, BE fallback chain, breakpoint universes) are documented with justification; no methodology bugs found. |
| Headline matching | 4.5/5 | Sign, shape, and significance of all four claims match; core coefficients within ~10% of the paper. Minor magnitude drift only on E(+)/P levels in multivariate specs (+0.7–1.1 %/mo) and the Table V within-decile spread (0.84 vs 0.99). |
| Data coverage | 4/5 | Exact 330-month period; universe 2,393 stocks/month vs the paper's 2,267 (+5.5%) from a broader modern CRSP-Compustat link; same data sources with one documented substitute (financial-firm SIC from CRSP, since Compustat carries no SIC in this vintage). |
| Concrete result matching | 4/5 | 692/780 targeted cells within tolerance (Tier 1, auditor-recomputed), 99.7% Tier 1+2; the evaluator's 2× magnitude bound on same-sign Tier-2 cells is now enforced with a documented near-null exception. The only two outright failures are sign flips on a statistically null coefficient (Table III R11 E/P dummy, |t| < 0.6 on both sides). |
| Signal strength | 4/5 | All priced-variable headline cells within 20% of the paper (ln(ME) 92%, ln(BE/ME) 99%, size and BE/ME spreads 85–105%); the β null replicates as a null. |
| Corollary | 4.5/5 | All in-scope corollaries replicate: subperiod stability (Table VI 63/63 cells; β insignificant in both halves; BE/ME 0.31–0.36), pre/post-ranking β ordering (including the paper's 1B quirk), the leverage identity, E/P absorption, both Table V gradients, and — newly surfaced and auditor-verified — the January-seasonality corollary (3/3 claim elements). Only the documented appendix Tables AI–AIV scope exclusion (a different NYSE-only/CRSP-only sample) keeps this below 5. |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I (100 size×β portfolios) | 107/107 targeted cells; the size gradient (1.48→0.87 vs 1.52→0.89), flat β-row, post-ranking betas rising across β groups within every size decile, ln(ME) 2.24→7.98 vs 2.24→7.93 | Portfolio construction, Dimson β estimation, NYSE size breakpoints, and the paper's Table I claims |
| Table II (size and β sorts) | Size-sorted returns 1.60→0.85 vs 1.64→0.90; β-sorted returns flat (1.15 vs 1.11) while post-ranking β runs 0.81→1.73, essentially exact | The informal size and β tests, including the paper's noted 1B ordering quirk |
| Table III (Fama-MacBeth) | Priced-variable slopes within ~10%: ln(ME) −0.14 (t −2.47) vs −0.15 (−2.58); ln(BE/ME) 0.49 (5.54) vs 0.50 (5.71); leverage pair 0.48/−0.66 vs 0.50/−0.57; E(+)/P absorption 5.55→1.59 | The four central asset-pricing claims; the paper's printed R8–R11 β cells are internally inconsistent with its own R1/R3, and the replication's β values match the paper's prose instead |
| Table IV (BE/ME and E/P sorts) | BE/ME returns monotone 0.41→1.79 vs 0.30→1.83 with betas flat within 0.02; E/P U-shape 1.25→0.83→1.70 vs 1.46→0.93→1.72; negative-E portfolio shows dummy 1.00 / E(+)/P 0.00 exactly | The book-to-market and earnings-price portfolio evidence |
| Table V (size × BE/ME matrix) | Both gradients replicate: within-size-decile BE/ME spread 0.84 vs 0.99 %/mo; size spread 0.61 vs 0.58; all margins pass | BE/ME captures strong cross-sectional variation controlling for size, and a size effect remains within BE/ME groups |
| Table VI (subperiods + NYSE benchmarks) | All 63 Fama-MacBeth cells pass: β insignificant in both subperiods (0.08, t 0.20; −0.48, t −1.30), BE/ME stable at 0.31–0.36; NYSE return standard deviations match the paper within 0.14 | Subsample stability of the size and BE/ME premiums |
| January-seasonality corollary (§III.C, L2186) | January ln(BE/ME) slope 0.606 %/mo = 1.9× the February–December 0.318 (t 3.85, ~4 SE from 0), within 0.024 of the full-year 0.341 — all three claim elements PASS, auditor-recomputed | A January seasonal in the BE/ME effect exists, but the positive BE/ME relation is strong throughout the year — the paper's closing corollary |

## Important gaps

- **Data vintage (non-actionable).** The 2026 CRSP/Compustat extract carries ~5.5% more stocks/month than the paper's ~1991 tape; the extra firms pile into ratio-extreme bins, shifting market-equity-denominated characteristics and E(+)/P levels while leaving every CRSP-built row and the pure-accounting ratio ln(A/BE) essentially exact; NYSE benchmark means run 0.1–0.2 %/mo above the paper with matching standard deviations (confirmed as a tape-level shift on CRSP's own NYSE index). No code change can close a vintage gap.
- **Paper-side inconsistency (non-actionable).** Table III's printed R8–R11 β cells cannot be reconciled with the paper's own R1/R3 rows or its prose; the replication reports the text-consistent values, documented per cell.
- **Appendix out of scope (documented).** Appendix Tables AI–AIV (NYSE-only 1941–1990) are a robustness extension on a different sample (CRSP-only pre-1962) and were excluded by documented decision; they do not affect the main claims.
- **Cosmetic residuals (non-actionable).** Two stale REPORT.md sentences (validator-flag wording now fixed; iteration count 1–6 → 1–7) and a backfilled assumptions.md entry out of chronological order; an empty stray directory skeleton recreated during iteration 2 was removed by the auditor. None affects any claim, count, or artifact value.
