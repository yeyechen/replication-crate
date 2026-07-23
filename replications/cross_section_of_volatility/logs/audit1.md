---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 4
requires_iteration: true
---

# Audit Report 1 — cross_section_of_volatility

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** The AHXZ (2006) idiosyncratic-volatility puzzle (Tables VI–XI) is strongly and honestly replicated — the headline 5-1 raw-return spread (−1.02% vs paper −1.06%) and the monotonically decreasing quintile pattern reproduce almost exactly, and the anomaly survives every replicable cross-sectional control and 7 of 8 subsamples. Four actionable majors remain: (1) the reported Table VI FF-3 alphas are produced by two offsetting bugs and are internally inconsistent with the correct Table XI full-sample alpha; (2) three of four Table X L/M/N strategies are uncomputed; (3) the past-1-month momentum control misses; (4) the volatile-period subsample misses. The systematic-volatility half (Tables I–V, IX) is out of scope for a documented external reason (no VIX in ClickHouse).

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3 | Signal/sort/weighting/filters/timing/look-ahead all faithful and independently verified; but the reported Table VI FF-3 alphas (incl. the headline 5-1 α) come from a double-rf + factor-month-misalignment bug (mkt beta ≈ 0), inconsistent with the correct Table XI value. |
| Headline matching | 5 | Monotonic-decreasing shape, negative sign, and magnitude class all reproduced; raw 5-1 spread within 4%, FF-3 α spread within ~11%. |
| Data coverage | 4 | Exact period (Jul 1963–Dec 2000), universe matches paper market-share stats (Q1 53.7% vs 53.5%, Q5 1.98% vs 1.9%), same sources (CRSP/Compustat/daily+monthly FF); systematic-volatility half uncovered (no VIX). |
| Concrete result matching | 4 | Paper-emphasized 5-1 spreads / Q5 alphas match within tolerance at ~90%+ of the 38 key cells; secondary cells (B/M levels, past-1-month, volatile period, some Table VIII Panel B detail) miss. |
| Signal strength | 4 | Raw 5-1 r=0.96 and FF-3 α 5-1 r≈0.89 both within 20% of paper; just outside the 10% band for a 5. |
| Corollary | 3 | All 7 cross-sectional controls, 7/8 subsamples, and the momentum loser/winner asymmetry replicate; notable gaps: volatile period, past-1-month, 3/4 L/M/N strategies, Table IX. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | REPORT.md numbers reconcile with results/table_*.md and with auditor recomputation; no fabricated values. |

**Overall: 3.83 / 5.00** → binary verdict **REPLICATED** (mean ≥ 3.0, no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None. The central claim is valid; no methodology gap invalidates all downstream metrics, coverage is 99.9% (≥60%), and the only prep_validation errors were the missing auditor deliverables written by this audit.

### Major (should fix)

- [M1] Table VI FF-3 alphas are produced by two offsetting bugs and are internally inconsistent with the correct Table XI full-sample alpha (actionable: true)
  - File: src/analyze_table6.py:165 (`exc = r - ff.loc[r.index, "rf"]`) + utils/regressions.py:587 (`factor_alpha` subtracts rf again) ; factor/return month misalignment from `attach_next_month_return` + `monthly_quintile_stats` (returns labeled by formation month t, regressed on formation-month factors).
  - Evidence: auditor recomputation reproduces table_6.md exactly — Panel B Q1 FF-3 α=0.02 … Q5=−1.10, 5-1=−1.12, with market betas ≈ 0 (Q1 b_mkt=−0.01, Q5 b_mkt=0.23). The correct convention (relabel to holding month + single rf, as in analyze_tables_10_11.py) gives Q1=−0.00 … Q5=−1.17, 5-1=−1.17 with b_mkt≈1, which is what table_11.md's full-sample row reports. So the same 1/0/1 strategy yields 5-1 α = −1.12 (Table VI) vs −1.17 (Table XI) — an internal contradiction, and Table VI's betas are nonsensical (a VW portfolio must have b_mkt≈1).
  - Likely cause: `analyze_table6.py` passes excess returns to `factor_alpha` (which subtracts rf a second time) AND regresses holding-month returns on formation-month factors; the two errors partially cancel so the alphas land near the paper by luck. The agent documented this (assumptions.md A17/A18) but left Table VI unfixed.
  - Specific fix: in `quintile_time_series`, relabel each quintile's return series to its holding month and pass TOTAL returns to `factor_alpha` (single rf), exactly as `analyze_tables_10_11.py` does; verify Q1..Q5 alphas move to −0.00/0.08/0.09/−0.29/−1.17 and b_mkt≈1, and that Table VI 5-1 α reconciles with Table XI (−1.17).

- [M2] Corollary 'L/M/N formation & holding periods' (Table X) not computed for 3 of 4 strategies (actionable: true)
  - File: results/table_10.md (rows 1/1/12, 12/1/1, 12/1/12 marked "requires recomputing IVOL from multi-month daily data"); paper §II.F and Table X rows 2–4 (inputs/content.md L2022–2048).
  - Paper claim: the IVOL anomaly persists for 1/1/12 (5-1 α −0.67), 12/1/1 (−1.12), and 12/1/12 (−0.77), i.e. it is not a short-horizon/contemporaneous-measurement artifact.
  - What to add: recompute L=12 IVOL from 12 months of daily data (the daily CRSP + FF series are already in ClickHouse — this is a pipeline pass, not a data limitation) and report the three strategies as `results/table_10.md` rows, citing L1132/L1134 for the J T-style overlapping construction.
  - Specific fix: extend the daily-stats SQL / panel to store 12-month-window IVOL, build the 12 overlapping VW cohorts, average them, and run the FF-3 alpha regression (correct convention per M1).

- [M3] Corollary 'robustness to past-1-month returns' (Table VIII Panel A) fails (actionable: true)
  - File: results/table_8.md Panel A "Past 1 month" row — rep 5-1 α = −1.15 vs paper −0.66 (74% off); Q5 = −1.11 vs −0.59; Q4 = −0.35 vs −0.05.
  - Paper claim (inputs/content.md L1732, L1772): controlling for past 1-month returns attenuates the 5-1 alpha to −0.66% (Q5 −0.59%), i.e. short-term reversal absorbs much of the effect. The replication's control barely attenuates it.
  - Likely cause: the past-1-month signal is `ret_{t-1}` (assumptions.md A18); the paper's 1-month reversal control is microstructure-sensitive (bid-ask bounce) and may use the formation-month return.
  - Specific fix: test the alternative past-1-month window (include the formation-month return / align to the paper's reversal definition) and confirm the 5-1 α moves toward −0.66 before declaring the cell; document whichever convention is chosen in assumptions.md.

- [M4] Corollary 'volatile-period subsample' (Table XI) fails (actionable: true)
  - File: results/table_11.md "Volatile periods" row — rep 5-1 α = −0.24 (t=−0.41) vs paper −0.89 (73% off; |rep/paper|=0.27, outside the 2× bound → genuine FAIL); Q5 = −0.48 vs −0.93.
  - Paper claim (inputs/content.md L2074, L2169): the effect persists (5-1 α −0.89%, significant) in the highest-20%-|market-return| months.
  - Likely cause: the stable/volatile threshold (top/bottom 20% of |mkt_rf| over in-sample holding months; assumptions.md A19) and the small sample (90 months) make this cell sensitive to the exact classification.
  - Specific fix: audit the volatile-month selection against the paper's definition (ex post highest-20% absolute market moves), verify the 90-month membership, and re-report; if it remains attenuated, document the sensitivity explicitly rather than labeling it robust.

### Non-actionable majors (documented external limitations)

- [M5] Tables I–V and Table IX (systematic volatility: β_ΔVIX sorts, FVIX factor, price of volatility risk, and the "aggregate-volatility-risk does not explain IVOL" test) are not replicated (actionable: false)
  - File: preparations/assumptions.md A7; REPORT.md §5.1/§5.3.
  - Reason: these require CBOE VIX/VXO data, which is not present in the ClickHouse catalog. This is a genuine external data limitation, documented in assumptions.md and REPORT.md; re-trying would not close it. Recorded for completeness, not for the iteration loop.

### Minor (cleanup)

- [m1] Iteration-log cell tallies are internally inconsistent. File: logs/log1.md "Per-cell evaluation" summary states "33 Tier 1, 3 Tier 2, 2 FAIL out of 38", but the per-cell table above it lists ~30 Tier 1, 5 Tier 2, 2 FAIL (=37). Fix: reconcile the counts.
- [m2] The agent's three "Tier 2" labels are actually within the stated 30% tolerance (T6B Q5 FF-3 α 13.4%, T6B 5-1 FF-3 α 14.5%, T6A 5-1 FF-3 α 11.8%, T11 1991–00 17.4%, T11 Recession 19.6%) — i.e. Tier 1. The labeling is conservative (honest), but the tier definitions should be applied consistently. Fix: relabel within-tolerance cells as Tier 1.
- [m3] Table VII "Controlling for B/M" Q1–Q4 level alphas are off by ~0.6–0.75 vs paper (rep ≈ −0.02..0.02 vs paper 0.61..0.50). File: results/table_7.md; documented in assumptions.md A20 as a Compustat book-equity/coverage level shift. The reported statistic (5-1 spread −0.91 vs −0.80) matches, so this is a non-headline level offset; fix only if revisiting B/M construction.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Panel B means Q1→Q5 = 1.04/1.16/1.20/0.85/0.01 (recomputed from data/panel.parquet), reproducing the paper's rise-then-precipitous-drop shape (1.04/1.16/1.20/0.87/−0.02). TVOL Panel A same shape. |
| 2 | Headline-magnitude claim | ✓ | Raw 5-1 spread −1.02% vs paper −1.06% (3.8%); IVOL signal mean 0.0296 / median 0.0223 (panel_summary.md), consistent with ~3% daily idiosyncratic vol. |
| 3 | Sample coverage ≥ 60% | ✓ | IVOL non-null 2,157,744 / 2,159,548 = 99.9%; 4,742 stocks/formation-month; 450 holding months (1963-07..2000-12). |
| 4 | Data-source choice justified | ✓ | CRSP dsf/msf + dsenames PIT, Compustat funda (FF BE convention), daily ff.three_factor (26,110 rows, DECIMAL) for IVOL, monthly ff.four_factor_monthly for alphas — matches the paper; DECIMAL scale and daily-FF facts verified live. |
| 5 | prep_validation.py exit 0 | ✗→✓ | Pre-audit run flagged only the two missing auditor deliverables (no logs/audit*.md, no SUMMARY.md); both are written by this audit. No substantive prep-contract failure. |
| 6 | All committed tables have results files | ✓ | tables_to_replicate T6A/T6B→table_6.md, T7→table_7.md, T8→table_8.md, T10→table_10.md, T11→table_11.md all present. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | Every REPORT.md figure spot-checked (T6B means/alphas, T7 5-1 spreads, T8 controls, T10 1/1/1, T11 subsamples) reconciles with results/table_*.md and with auditor recomputation. |
| 8 | No orphan folders | ✓ | Slug root contains only data/inputs/logs/preparations/results/src + REPORT.md; no literal-brace or shell-expansion directories. |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md iteration entries carry Diagnosis / Next fix / Before / After / Status (e.g. the Iteration-1 signal→return misalignment fix, +0.59%→−0.98%). |
| 10 | Tier 2 within 2× magnitude | ✓ | Cells labeled Tier 2 are within tolerance (conservative); the "FAIL" past-1-month (|rep/paper|=1.74) is actually within 2× → Tier 2, and "FAIL" volatile (|rep/paper|=0.27) is correctly outside 2× → FAIL. No inflated Tier 2. |
| 11 | Corollary coverage | ✓ | Subsample stability ✓ (7/8), cross-sectional controls ✓ (7/7), momentum asymmetry ✓ (losers/winners), TVOL ✓; past-1-month and volatile period flagged as M3/M4; L/M/N (3/4 missing) flagged as M2; Table IX flagged as non-actionable M5. No silently-skipped corollary. |

## 4. Issues the agent should have caught (didn't)

1. The agent diagnosed the Table VI alpha bug precisely (assumptions.md A17/A18) and even implemented the correct method for Tables X/XI, yet shipped table_6.md with the buggy alphas — leaving a direct internal contradiction (Table VI 5-1 α = −1.12 vs Table XI full-sample 5-1 α = −1.17 for the identical strategy/sample). A careful reviewer would have reconciled the two before declaring Table VI done.
2. The Table VI market betas (~0) are an obvious red flag for a value-weighted portfolio (should be ≈1); the alignment sanity gate checked the return↔market correlation but not the regression's factor-month alignment, so the misalignment slipped through.
3. The per-cell tally in logs/log1.md (33/3/2) does not match its own table (~30/5/2), and several "Tier 2" labels are within the stated tolerance (i.e. Tier 1) — the bookkeeping was not reconciled.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The Cross-Section of Volatility and Expected Returns" (Ang, Hodrick, Xing & Zhang 2006) for slug `cross_section_of_volatility`. The previous run completed with verdict **PARTIAL** (audit 1 at `replications/cross_section_of_volatility/logs/audit1.md`). The headline IVOL puzzle is solidly replicated (raw 5-1 spread −1.02% vs paper −1.06%; monotonic pattern; anomaly survives all replicable controls and 7/8 subsamples). Read the audit first.

## Issues to address (priority order)

### [M1] — MAJOR — fix first: Table VI FF-3 alphas come from two offsetting bugs
`src/analyze_table6.py:165` computes `exc = r - rf` then calls `factor_alpha(exc, ...)`, which subtracts rf a second time (utils/regressions.py:587). The return series is also indexed by formation month t while the regression uses formation-month factors (holding-month returns on formation-month factors). Auditor recomputation confirms Table VI Panel B market betas ≈ 0 (Q1 b_mkt=−0.01, Q5 b_mkt=0.23) and 5-1 FF-3 α = −1.12, whereas the correct convention (already used in analyze_tables_10_11.py) gives betas ≈ 1 and 5-1 α = −1.17 — which is what table_11.md's full-sample row reports. Table VI and Table XI currently contradict each other for the same strategy/sample.

**Specific fix:**
1. In `quintile_time_series`, relabel each quintile's monthly return series to its HOLDING month (formation month + 1) and pass TOTAL returns (not pre-subtracted excess) to `factor_alpha` so rf is subtracted exactly once — mirror `analyze_tables_10_11.py`.
2. Re-run `python src/analyze_table6.py` (or `--table-6`) and regenerate results/table_6.md.
3. Verify: Panel B Q1..Q5 FF-3 α move to ≈ −0.00/0.08/0.09/−0.29/−1.17 with b_mkt ≈ 1, and the 5-1 α reconciles with table_11.md (−1.17, vs paper −1.31).

### [M2] — MAJOR — compute the missing Table X L/M/N strategies
results/table_10.md leaves 1/1/12, 12/1/1, 12/1/12 uncomputed ("requires recomputing IVOL from multi-month daily data"). The daily CRSP + FF series are already in ClickHouse, so this is a pipeline pass, not a data limitation. Paper Table X rows 2–4 (inputs/content.md L2022–2048) report 5-1 α of −0.67 / −1.12 / −0.77.

**Specific fix:**
1. Extend the daily-stats SQL / panel to store an L=12 (12-month daily-window) IVOL.
2. Build the 12 overlapping value-weighted cohorts per Jegadeesh–Titman (inputs/content.md L1134), average them, and run the FF-3 alpha regression using the CORRECT convention from M1.
3. Verify the three new 5-1 α land within ~30% of −0.67 / −1.12 / −0.77; report in results/table_10.md citing L1132/L1134.

### [M3] — MAJOR — past-1-month momentum control misses (Table VIII)
results/table_8.md Panel A "Past 1 month": rep 5-1 α = −1.15 vs paper −0.66 (74% off; Q5 −1.11 vs −0.59). The control barely attenuates the IVOL effect, contradicting the paper's claim (inputs/content.md L1732) that 1-month reversal absorbs much of it.

**Specific fix:**
1. Test the alternative past-1-month window (include the formation-month return / align to the paper's reversal definition) instead of `ret_{t-1}` (assumptions.md A18).
2. Verify the 5-1 α moves toward −0.66; document the chosen convention in assumptions.md either way.

### [M4] — MAJOR — volatile-period subsample misses (Table XI)
results/table_11.md "Volatile periods": rep 5-1 α = −0.24 (t=−0.41) vs paper −0.89 (73% off, outside 2×). 

**Specific fix:**
1. Audit the top-20%-|mkt_rf| volatile-month selection (assumptions.md A19) against the paper's ex post highest-20% absolute-market-move definition (inputs/content.md L2074); verify the 90-month membership.
2. Re-report; if still attenuated, document the threshold sensitivity explicitly rather than labeling it robust.

### [m1]/[m2]/[m3] — MINOR — cleanup
Reconcile the logs/log1.md per-cell tally (33/3/2 vs the table's ~30/5/2); relabel within-30%-tolerance cells as Tier 1 (not Tier 2); the Table VII B/M Q1–Q4 level offset (~0.6–0.75, documented A20) needs no action unless you revisit B/M construction.

## Non-actionable (do NOT spend iterations on)
Tables I–V and IX (systematic-volatility / β_ΔVIX / FVIX / price-of-volatility-risk) require CBOE VIX/VXO data not in ClickHouse (assumptions.md A7). This is a documented external limitation — leave it documented, do not attempt to fabricate it.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every new assumptions.md entry must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate; a documented partial beats a false success.
- **Pair every diagnosis with a fix attempt (exit gate)** before declaring `partial`.

## Inputs you should read

- `replications/cross_section_of_volatility/logs/audit1.md` — this audit (full context)
- `replications/cross_section_of_volatility/inputs/content.md` — paper ground truth (Tables VI–XI at L1164, L1326, L1746, L1991, L2070)
- `replications/cross_section_of_volatility/preparations/` — rules, tables, data verification, assumptions log
- `replications/cross_section_of_volatility/src/analyze_table6.py` and `analyze_tables_10_11.py` — the buggy vs correct alpha conventions
- `replications/cross_section_of_volatility/data/panel.parquet` — cached panel (recompute spot-checks from here)

## What NOT to redo

- Skip re-reading `SKILL.md` — contract unchanged.
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact (it passed after audit 1 wrote its deliverables).
- Skip the ClickHouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add/modify, and add a regression sanity gate asserting Table VI market betas ≈ 1 (catches the M1 misalignment).

## Deliverables for this iteration

- `src/analyze_table6.py` — corrected alpha convention (M1), with a b_mkt≈1 sanity gate
- `results/table_6.md` — regenerated with correct alphas reconciled to Table XI
- `results/table_10.md` — add 1/1/12, 12/1/1, 12/1/12 (M2)
- `results/table_8.md` / `results/table_11.md` — updated for M3 / M4
- `preparations/assumptions.md` — append a five-field iteration entry per issue addressed
- `SUMMARY.md` — read only; do NOT edit (auditor-owned)
- `REPORT.md` — update; lead with the data-quality summary and headline-magnitude comparison

## Stop conditions

- **All majors fixed and verified** (Table VI reconciled to Table XI; L/M/N strategies added; past-1-month and volatile cells either matched or documented) → re-run prep_validation + sanity gates → declare success.
- **10-iteration cap reached** on a single problem → escalate, write a partial REPORT.md; do not edit SUMMARY.md.
- **M1 fixed but M3/M4 remain genuinely resistant** → declare partial and document; the auditor's SUMMARY.md verdict is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is a high-quality, unusually honest replication. The data pipeline is sound and fully verified: the IVOL signal (daily FF-3 residual std, n≥17), the PIT universe filter, the value-weighting, the signal_t→return_{t+1} timing, and the look-ahead-free Compustat mapping all check out, and the agent caught and fixed a genuine signal/return misalignment during the run (assumptions.md Iteration 1). The headline result — high-IVOL stocks earn abysmally low returns — reproduces almost exactly (raw 5-1 spread within 4%, perfect monotonic shape), and the anomaly's robustness across seven cross-sectional controls and seven of eight subsamples is convincing. The agent's self-criticism is exemplary: it diagnosed the Table VI double-rf / factor-misalignment bug, implemented the correct method for Tables X/XI, and flagged every paper-silent decision. The single real blemish is that it then shipped Table VI with the buggy alphas anyway, creating an internal contradiction (−1.12 vs −1.17) and nonsensical (~0) market betas in the paper's flagship table — easily fixed by porting the correct convention already present in the codebase. The remaining gaps (three L/M/N strategies, past-1-month and volatile-period cells) are addressable in a next pass; the systematic-volatility half (Tables I–V, IX) is genuinely blocked by the absence of VIX data and is correctly documented as such. Overall this reads as a faithful replication of the paper's most-cited result with a small, well-understood set of fixable gaps.
