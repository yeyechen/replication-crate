---
iteration: 2
slug: time_series_momentum
inner_iterations: 0
worker_spawns: 0
---

# Outer Iteration 2 — Reasoning Trace (report-accuracy & cleanup pass)

Audit 1 verdict: PARTIAL, 0 blockers, 1 actionable major, requires_iteration: true. The auditor
independently verified the entire computational chain — TSMOM engine rebuild matched
strategy_artifacts.parquet with max |Δ| = 0.0; an independent from-scratch SP500 rebuild from raw
daily settlements matched the panel over all 326 months; Tables 3/4/5 recomputed to the reported
values; committed paper values verified against content.md; tier tallies verified cell-by-cell.
**No re-estimation required.** This iteration fixes report-accuracy defects and layout cleanup only.

## [M1] REPORT.md transcription errors — FIXED
The auditor found five digit-swap transcription errors where REPORT.md prose contradicted the
(correct) artifacts. Root cause: hand-copying cells into prose without cross-checking eval CSVs.
Fixes applied (all values now taken verbatim from results/eval_t5.csv / results/table_5.md):
- Table 5C block rewritten: XSMOM_ALL α −0.39 (t −2.28) [was −0.03 (−0.22)]; XSMOM_COM α −0.82
  (−3.52), R² 15.7% [was −0.02, 20%]; XSMOM_FX α −0.37, R² 2.9% [was +0.05, 6%]; HML row
  −0.14 (−2.92) / +0.54 (2.88) / R² 2.8% [was −0.13 (−2.35) / +0.38 (2.02) / 2%]; all eight rows
  now carry full (t) values matching table_5.md.
- Deleted the "insignificant alpha" claim for XSMOM_ALL: the true t is −2.28 (marginally
  significant, negative). REPORT now states: small negative alpha −0.39% vs paper −0.16%, Tier 1
  only under the committed 200% near-zero tolerance; the replicated claim is β ≈ 0.72 and R² ≈ 47%.
- §1 first bullet fixed: raw diversified-factor mean +1.315%/month (Sharpe 1.25 = 1.315×√12/12.65);
  +1.20%/month is the Table 3A regression intercept — now labeled distinctly.
- Verification: every number in the REPORT §4 Tables 3/5 blocks now matches results/eval_t3.csv and
  results/eval_t5.csv at the displayed precision (grep-checked).

## Tier-2 leniency disclosure — ADDED (auditor §4 item 4)
REPORT §1 now discloses that the committed Tier-2 definition (sign match) is looser than the
rubric's 2×-magnitude standard, and states the rubric-strict tally alongside the committed one:
committed 180/136/104 (Tier1/Tier2/FAIL) vs strict 180/49/191 (43/12/45%).

## Minor items — FIXED
- [m1] S_t labeling: REPORT §2 now distinguishes panel AVAILABILITY (27/36/51/54, mean 45.4) from
  the factor CROSS-SECTION (signal AND σ available: 25/32/49/53, mean 44.2/month) — auditor-
  recomputed values used.
- [m2] Table 1 window prose aligned with table_1.md: statistics computed over each instrument's
  FULL panel window (futures listing → 2009-12; SP500 n=326 from 1982-04), not "1985–2009".
- [m3] 2008Q4 S&P 500 futures quarterly return corrected −22% → −23.0% (TSMOM +10.2% on the
  quarter) in §1 and §5.
- [m4] Raw-pull caches relocated: data/cache_daily_futures.parquet, data/cache_rf_monthly.parquet,
  data/cache_codes.txt → <slug>/.cache/ (data/ holds computed artifacts only, per layout policy).
  src/main.py cache paths updated (cache_dir = LAYOUT.root / ".cache"). Pipeline re-run from the
  new location: data/panel.parquet, data/strategy_artifacts.parquet, and all five results/eval_t*.csv
  verified BYTE-IDENTICAL (md5sum -c: 7/7 OK) — zero numerical impact.
- [m5] SEKUSD exclusion stated where "49 of 54 signal-bearing instruments" first appears (55 mapped;
  SEKUSD has 7 post-burn-in months in-window, no 12-month signal).

## Scope of this iteration
No worker spawns (pure documentation + 4-line path change). No assumptions changed (A1–A11 and
W1–W11 stand; the auditor found no methodology bugs). The replication's numerical substance is
unchanged from iteration 1; only its presentation is corrected.

## Exit check
All audit-1 issues addressed (1 major + 5 minor). Re-invoking the auditor for iteration 2.

## Post-audit-2 touch-up [m6] (per audit2's optional-fix authorization)
Audit 2 found one residual minor: §4 Table 1 example volatilities (15.60/11.10/21.61/39.41/27.07)
were quoted from t1_preview.csv's 1985–2009 diagnostic column, contradicting the m2-fixed
full-window prose. Fixed in REPORT.md §4 to the committed table_1.md values
(15.34/11.47/21.59/38.01/27.04) — all five remain Tier 1 (max deviation 5.9%, DAX, within the 10%
vol tolerance); no tier counts or claims change. Also corrected the W1–W13 → W1–W11 miscount above
(assumptions.md holds worker notes W1–W11; A1–A11 correct). No numerical work, no new outer
iteration — authorized by audit2's next-iteration prompt as an optional cleanup.

## Post-audit-2 layout change: caches moved back to data/ (policy relaxed)
The data/ parquet constraint was relaxed project-wide: computed intermediates are now allowed
under any name, and validator Check 2 flags only raw-dump naming patterns (*_raw.parquet,
*_dump.parquet). The iteration-2 [m4] relocation to <slug>/.cache/ was therefore reverted at the
user's request: cache_daily_futures.parquet, cache_rf_monthly.parquet, and cache_codes.txt are back
in data/, src/main.py cache paths updated to LAYOUT.data_path(...) accordingly, and .cache/
removed. Pipeline re-run verified panel.parquet byte-identical (md5); validator re-run below.
No numerical impact; SUMMARY.md residual-cosmetics note updated to the current state.
