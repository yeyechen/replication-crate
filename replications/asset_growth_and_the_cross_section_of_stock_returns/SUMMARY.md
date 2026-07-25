> **NOTICE (2026-07-25): the binary verdict below is SUPERSEDED.** Corrected investment-first records with accepted/qualified/quarantine statuses live in `training/cases.json`; see `training/README.md`.

---
schema_version: 2
slug: asset_growth_and_the_cross_section_of_stock_returns
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 3.67
methodology: 4
headline_matching: 4
data_coverage: 4
concrete_result: 3
signal_strength: 3
corollary: 4
generated_at: 2026-07-23T00:00:00Z
---

# Replication Summary

## Asset Growth and the Cross-Section of Stock Returns (Cooper, Gulen & Schill 2008)

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 3.67 / 5.00
**Audit state:** `PASS`

The paper's central claim — that the year-over-year change in total assets (ASSETG) strongly and negatively predicts subsequent stock returns — replicates closely. Independent auditor re-derivation from the cached data reproduces the monotonic decile returns (EW Year-1 spread −1.71% vs the paper's −1.73%; VW −1.03% vs −1.05%), the negative, significant Fama–French three-factor alpha spreads across all firms and size groups (EW all-firm −1.49 vs −1.63), and the Fama–MacBeth Model-1 statistics (intercept 0.139 vs 0.137; ASSETG dominant in every model). Outer iteration 2 closed the one actionable item from audit 1: the Table I ISSUANCE column is now split-adjusted (shares × CRSP `cfacshr`, a convention the auditor verified on a documented split stock), moving it from 1.85–3.9× the paper to 0.88–1.45×, and every pattern-match cell was relabeled against the strict 2× magnitude bound. The binary result does not mean every one of the 119 committed cells matched exactly: 76 are within numerical tolerance and 109 (91.6%) match in sign and pattern, while the 10 strict FAILs are all documented, non-actionable causes (three noise-level sign flips on statistically zero coefficients, five pre-1971 Compustat data-coverage cells, two vintage-attenuated t-stats). The dominant deviation is a genuine, auditor-verified 2026 Compustat data-vintage effect, not a methodology error. No methodology bugs remain and no filters were invented to chase a match; the run is complete.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Signal formula, FF1992 timing, point-in-time universe filter, no look-ahead, the paper's footnote-13 AR(1) SE adjustment, and the balance-sheet decomposition identities all verified independently; ISSUANCE is now the paper-consistent split-adjusted share change (cfacshr convention verified on a split stock); residual deviations (NW3 for Table II, full-universe signal sort, monthly-portfolio event time) are documented with paper-grounded justification |
| Headline matching | 4/5 | Return spreads and monotonicity match within ~2% (EW −1.71 vs −1.73; VW −1.03 vs −1.05); FF3/FF4 alpha spreads within 9–21%; only the raw Fama–MacBeth ASSETG coefficient drifts ~30% (its t-stat and the winsorized coefficient match) |
| Data coverage | 4/5 | Exact sample period (event window to Jun 2007 now cached) and the same CRSP/Compustat/FF sources with one documented equivalent substitution; universe composition is vintage-shifted (more small/dormant firms), the documented driver of the characteristic level shifts |
| Concrete result matching | 3/5 | 76/119 (63.9%) strict Tier-1 cells; 109/119 (91.6%) sign- and pattern-correct; all 10 strict FAILs carry documented non-actionable causes (noise-level nulls, pre-1971 data coverage, vintage-attenuated t-stats) |
| Signal strength | 3/5 | Central return spreads at 0.98–0.99 of the paper and the EW alpha at 0.91, but the VW alpha (0.80), the raw FM coefficient (0.70), and the VW-spread Sharpe (0.66) keep the worst-case ratio outside the 0.8–1.2 band; the signal itself is unambiguously present and strong |
| Corollary | 4/5 | Subsample stability (including the paper's own lone 1968–80 VW exception), size-group variation, FF4/FF5 risk adjustment, 5-year event-time persistence (−106% vs −88%, now cache-derivable), winsorization and monthly-dependence robustness, dominance over alternative predictors, and the investment/financing decomposition all replicate, with minor documented deviations in large-cap VW and the accrual-linked components |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Table I (formation characteristics) | All cross-sectional patterns, signs, and monotonic trends match; ISSUANCE now split-adjusted (0.88–1.45× the paper vs 1.85–3.9× raw); remaining level shifts traced to the data vintage | Correct data ingestion, universe construction, ASSETG formula/timing, and the control-variable pipeline |
| Table II (returns and alphas) | EW/VW Year-1 spreads within 1–2% of the paper and perfectly monotonic; negative FF3 alpha spreads in every size group; decade-subperiod and year-consistency patterns match (97%/77% vs 91%/71%); 5-year cumulative spread −106% vs −88% | The paper's central result: asset growth negatively and persistently predicts returns, robust to FF3/Carhart4 adjustment and size |
| Table III (Fama–MacBeth) | Intercept matches almost exactly; ASSETG is the strongest, most significant predictor in every model and size group, dominating B/M, size, momentum, accruals, capital investment, sales growth, and NOA | Asset growth dominates the established cross-sectional predictors; the regression pipeline and AR(1)-adjusted inference are faithful |
| Table IV (decomposition) | Components sum to ASSETG to machine precision; ΔPPE strongest standalone (t −5.00 ≈ prose −4.80); debt and stock financing dominate while retained earnings are insignificant | The operating-asset / debt-and-stock mechanism behind the effect |

## Important gaps

- **Table V not replicated (non-actionable):** requires SEO/repurchase announcement data (Thomson/SDC) unavailable in the ClickHouse set.
- **2026 data-vintage effects (non-actionable):** a fattened ASSETG upper tail and heavy pre-1971 Compustat missingness (auditor-verified: `ch` 93–94% null, `txp` 44–62% null in FY1966–68) attenuate the ASSETG D10 median, the raw FM coefficient, and the accruals/current-assets/other-assets slopes, without changing any sign, pattern, or conclusion.
- **Ten strict-convention FAILs (non-actionable):** three noise-level sign flips on statistically zero coefficients/spreads, five pre-1971 data-coverage cells, and two vintage-attenuated t-stats whose underlying spreads are within-2× pattern matches; each is documented with its cause and none affects any claim.
- **Resolved this iteration:** the ISSUANCE split-adjustment (audit [M1]) and the honest strict 2× relabeling (audit [M2]/[m1]) are complete and independently verified; the path bug ([m2]) and event-time cache ([m4]) are fixed.
