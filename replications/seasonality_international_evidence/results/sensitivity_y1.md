# A13 Sensitivity Battery — EW Panel A Year-1 Nonannual Decile Spread

Heston & Sadka (2010), Table 3, EW Panel A Year-1 nonannual top-minus-bottom decile spread (lags 1..11, monthly sorts 1985-02..2006-06). Committed code (`src/sensitivity_y1.py`) resolving audit-1 issue M4: the iteration-1 battery (REPORT §6.3) existed only as prose, and the auditor's independent re-implementation diverged on two t-stats because the filter semantics were never pinned down. Reads `data/panel.parquet` only.

Engine: identical to `src/compute_t3.py` — country equal-weighted benchmark, arithmetic excess returns, signal = mean excess over lags 1..11, deciles = ceil(10·rank/N) on ascending average ranks, spread = mean(D10) − mean(D1), t = mean/(std/√T), T = feasible months.

## Pinned filter semantics

- **Primary (these are the REPORT §6.3 numbers):** recompute-in-filtered-universe. Offending firm-month rows are dropped BEFORE computing country means, excess returns, signals, sorts, and spreads — everything is recomputed in the filtered universe. Reproduces the auditor's independent re-implementation exactly (baseline −0.0053/t −1.62; drop-Canada +0.0002/t 0.06; |ret|>100% +0.0058/t 2.26; |ret|>60% +0.0149/t 6.79).
- **Secondary (reported for completeness):** benchmark kept from the full universe — country means, excess returns, signals, and decile breakpoints (ranks on the full candidate set) are all unfiltered; only sort membership is filtered: firm i is dropped from the month-t sort if any of its firm-months in the sort window (holding month t and signal lags t−1..t−11) is offending. The iteration-1 ad hoc numbers came from uncommitted interactive code; this pinned reading approximates them within 0.001 in mean and 0.3 in t.

## Primary semantics — recompute-in-filtered-universe

| # | Variant | Filter (rows dropped) | Mean spread | t-stat | T |
|---|---------|-----------------------|------------:|-------:|--:|
| 1 | baseline | none (full Compustat universe) | -0.0053 | -1.62 | 257 |
| 2 | drop Canada | country != 'CAN' (415,120 rows dropped) | +0.0002 | +0.06 | 245 |
| 3 | drop \|ret_usd\| > 100% | \|ret_usd\| <= 1.0 (6,675 rows dropped) | +0.0058 | +2.26 | 257 |
| 4 | drop \|ret_usd\| > 60% | \|ret_usd\| <= 0.6 (22,522 rows dropped) | +0.0149 | +6.79 | 257 |
| 5 | top-50% market cap | me_usd >= month p50, non-missing only (1,086,203 rows dropped) | +0.0066 | +1.77 | 245 |
| — | Paper (Table 3) | — | +0.0121 | +4.17 | — |

## Secondary semantics — full-universe benchmark, membership-only filter

| Variant | Mean spread | t-stat | T | Iteration-1 ad hoc (mean / t) |
|---------|------------:|-------:|--:|-----------------------------|
| Drop \|ret_usd\| > 100% | +0.0049 | +1.87 | 257 | +0.0055 / +1.91 |
| Drop \|ret_usd\| > 60% | +0.0117 | +4.98 | 257 | +0.0119 / +4.72 |

## Interpretation

The battery diagnoses microcap penny-stock contamination of short-horizon momentum: trimming the universe monotonically moves the Year-1 nonannual spread from −0.53%/mo (t −1.62) toward the paper's +1.21%/mo (t 4.17) — dropping Canada removes most of the divergence (68% of extreme observations are Canadian TSX-V-style firms; median market cap of extremes $5.9M vs $121M panel median), and dropping firm-months with |ret| > 60% overshoots the paper (+1.49%/mo, t +6.79 under primary semantics; +1.17%/mo, t +4.98 membership-only). **No filter is adopted for the main tables** — assumption A13 and the anti-tweaking rule: the paper applies no filter, and the ±60% threshold reproduces the paper's cell only because it was selected to do so (the volatility-calibration alternative was also checked and rejected on the facts — see assumptions.md). The cleanest counter-evidence that the methodology itself is sound: the long-horizon cells, which this contamination does not touch, replicate at Tier 1 under the identical filter-free pipeline.
