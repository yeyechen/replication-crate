---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 4
requires_iteration: true
---

# Audit Report 1 — balakrishnan_v2

**Verdict:** PARTIAL
**Date:** 2026-08-07
**Auditor notes:** Headline loss/profit pattern (positive, monotone, significant D10-D1 BHAR spread over [-2,0], [1,60], [1,120]) is reproduced. Sign is correct in every window. The [-2,0] window matches the paper to within rounding (Tier 1 on D1, D10, hedge). But magnitudes are 2-3x biased in the post-announcement windows due to documented Assumption A9 (EW vs VW size-decile benchmark), the FF column in Table 2 is currently computed as SAR duplicate (not the Carhart 4-factor model), 10 cells are SKIP (sample-size + t-stats), and the paper's three corollary claims (subsample stability, Carhart FF column, Table 5 incremental test) are not computed.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3/5 | Most major choices match (BHAR formula, decile direction, event-time alignment, delisting treatment, size decile benchmark universe). Notable deviations: (a) decile breakpoints use the CURRENT calendar quarter's distribution rather than the paper's PRIOR fiscal quarter's distribution (A10), introducing look-ahead bias the paper explicitly tried to avoid; (b) the FF column in Table 2 is SAR-duplicated, not actually benchmarked against Carhart 4-factor loadings. A9 (EW vs VW) is a documented data-availability substitution, not a code bug. |
| Headline Matching | 4/5 | Pattern matches in all three windows: positive, monotone D10-D1 hedge; D1 BHAR strongly negative and D10 BHAR positive. [-2,0] window is Tier 1 on D1/D10/hedge. [1,60] and [1,120] hedge spreads are 2.6x and 2.3x the paper, respectively, driven by A9. |
| Data Coverage | 3/5 | Period matches (1976-2005). All data sources match (CRSP dsf, dsenames, dsedelist, erdport1, ccmxpf_linktable; Compustat fundq; FF factors). Universe is 16-28% above paper, documented as comp_202601 vintage drift; this puts it outside the 5-15% Tier-1 band but within the 15-25% Tier-2 band with justification. |
| Concrete Result Matching | 3/5 | 8 Tier 1 / 26 Tier 2 / 0 FAIL / 10 SKIP of 44 cells (per `src/evaluate.py`). Numerically-comparable cells are 100% Tier 1+2 (no FAIL). But Tier 1 only is 18% — well below the 50% Tier-1 threshold for a score of 4. The 10 SKIPs are easy fixes (sample-size and t-stat cells that were not piped into the markdown render). |
| Signal Strength | 2/5 | Headline cell (D10-D1 SAR hedge [1,120]) is 0.2332 vs paper 0.1021, ratio = 2.28x. [1,60] hedge is 2.63x. [-2,0] matches. Sign is correct in every window, so this is a magnitude problem (within [0.33, 3.0] band). The replicator correctly attributes the bias to A9. |
| Corollary | 2/5 | Paper's three main corollaries are NOT evaluated: (a) subsample stability across 1976-1985/1986-1995/1996-2005 (paper footnote 15 reports 10.75%/8.68%/11.03% hedge returns); (b) Carhart 4-factor alternative (paper Table 2 FF column); (c) incremental-to-SUE/BM/accruals robustness (paper Table 5). FF column currently reuses SAR values. |

Aggregate: 2.83 / 5.00. Binary rule: REPLICATED (avg >= 3.0) — wait, average is 2.83 < 3.0. **FAILED by bright-line.** The replication reproduces the qualitative pattern (sign, monotonicity, significance) but is materially biased on magnitudes and missing the FF column and subperiod stability.

## 2. Issues by severity

### Blockers (must fix)

None. The pipeline runs end-to-end, produces the expected per-cell output, and the headline sign/monotonicity pattern is reproduced.

### Major (should fix)

- **[M1] FF column in Table 2 is computed as a duplicate of the SAR column, not the Carhart 4-factor model.** 
  - Evidence: `src/sql/bhar_panel.sql` lines 23-66 only compute the size-adjusted (SAR) BHAR via `crsp_202601.erdport1.decret`. There is no 40-trading-day factor-loading regression. `src/table2_compute.py` reads only `bhar_m20`, `bhar_60`, `bhar_120` from the parquet (lines 73, 99). `src/evaluate.py` parses the decile-by-decile mean and assigns the same value to both `*_sar_*` and `*_ff_*` cells (lines 156-164).
  - Impact: 6 cells (`d1_ff_m2_0`, `d1_ff_1_60`, `d1_ff_1_120`, `d10_ff_m2_0`, `d10_ff_1_60`, `d10_ff_1_120`, `hedge_ff_m2_0`, `hedge_ff_1_60`, `hedge_ff_1_120` — actually 9 FF cells) are validated against paper's FF column using SAR's value. This is a false Tier 2 — sign matches because SAR and FF have the same sign on the paper, but the magnitudes are not validated.
  - The replicator acknowledges this in `REPORT.md` limitations #3: "Per-firm Carhart 4-factor estimation (the FF column in Table 2) was not implemented... The FF column in the evaluator currently reuses the SAR benchmark, which is incorrect."
  - **Specific fix:** Either (a) implement the per-firm factor-loading regression (40-day hold-out from 55 days prior to rdq, then daily FF-abnormal return over [1,60] and [1,120]) using `ff.four_factor` (catalog-verified available), or (b) reclassify the FF cells as SKIP with explicit notes in the markdown render. Option (b) is the minimum acceptable fix; option (a) is the substantive fix.

- **[M2] A10 — decile breakpoints use current calendar quarter's distribution rather than the paper's prior fiscal quarter's distribution.**
  - Evidence: `src/table2_compute.py` lines 57-68 compute deciles per `cal_q = rdq.dt.to_period("Q")` using `pd.qcut(group["earnings_at"], 10, ...)`. The breakpoints are computed from the CURRENT quarter's earnings distribution. Paper §3.1 (line 256 of `inputs/content.md`) says "we compute cut-off points based on the previous fiscal quarter's earnings distribution" specifically to avoid look-ahead bias.
  - Impact: introduces look-ahead bias. The paper's argument is that a firm-quarter cannot know its current decile membership at the time the portfolio is formed. The replicator's claim that this affects "only firm-quarters near a fiscal-quarter boundary and is a small share of the sample" (`assumptions.md` A10) understates the deviation — the breakpoints are entirely different for firms whose fiscal calendar does not align with calendar quarters (i.e., the ~35% of firms with non-December fiscal year-ends).
  - **Specific fix:** Implement decile breakpoints from the prior fiscal quarter's earnings distribution. The panel has `fyearq` and `fqtr` columns; a `(fyearq-1, fqtr=4)` self-join gives the prior fiscal quarter. Lag `earnings_at` by one fiscal quarter, compute decile breakpoints per (year, fiscal-quarter) using the lagged distribution. Affects only `src/table2_compute.py`.

- **[M3] 10 SKIPs in the per-cell tally that are not data limitations but easy fixes.**
  - Evidence: 2 sample-size cells (`primary_after_price1`, `primary_after_price1_firms`) are in `results/table_1.md` but the evaluator regex in `src/evaluate.py` lines 49-54 doesn't match the prefix string exactly. 2 Table 2 sample-size cells (`d1_high_loss_n`, `d10_high_profit_n`) and 6 t-stat cells (`d1_sar_1_120_t`, `d10_sar_1_120_t`, `hedge_sar_1_120_t`, `hedge_ff_1_120_t`, `hedge_sar_1_120_t_fmb`, `hedge_ff_1_120_t_fmb`) are computed in `src/table2_compute.py` (line 80, 105 for t-stats) but not piped into the markdown render.
  - Impact: 22.7% of cells are SKIP. All 10 are easy fixes — the data is already computed; only the parsing/markdown render is incomplete.
  - **Specific fix:** (a) Fix the regex in `src/evaluate.py` parse_table_1_counts (lines 49-54) to match `primary_after_price1`. (b) Add `| N` and `| t-stat` columns correctly parsed in `src/table2_compute.py`'s markdown writer (lines 131-150). (c) Add n=46,753/47,078 columns to Table 2 output.

- **[M4] Subsample stability (paper footnote 15) not evaluated.**
  - Evidence: Paper `inputs/content.md` line 322: "the hedge portfolio size-adjusted returns in the first subperiod (10.75 percent), second subperiod (8.68 percent), and third subperiod (11.03 percent) are quite similar and highly statistically significant." This is the paper's main corollary prediction. `results/` has no subsample breakdown.
  - Impact: The paper's most prominent corollary (effect is not period-specific) is not tested. The replication cannot rule out a 1986-1995 specific effect, which is the very robustness concern the paper addresses.
  - **Specific fix:** Add `results/table_2_subsample.md` with hedge SAR [-2,0], [1,60], [1,120] per subperiod (1976-1985, 1986-1995, 1996-2005). Use `fyearq` (Compustat fiscal year) or `rdq.year` for split. Sample sizes per subperiod are also reportable.

### Minor (cleanup)

- **[m1] Table 1 universe over-count (16-28%) is documented as `comp_202601.fundq` vintage drift.** Tested 6 alternative filter combinations (FF indfmt, datacqtr, min-listing, daily-return-on-rdq, denser price filter, stricter linkprim); none closed the gap to ±2%. The pattern of uniform over-count across stages is consistent with broader Compustat coverage in 2026 vs 2009-era. Documented in `assumptions.md` lines 128-141. This is a non-actionable data-availability issue, not a code bug.

- **[m2] A9 — size-decile benchmark is EW (`erdport1.decret`), not VW as paper specifies.** Documented in `assumptions.md` lines 179-198. The `crsp_202601.erdport1` table is the only daily size-decile return table in this ClickHouse catalog. EW includes more small-cap noise, so subtracting EW from each stock's return produces a larger residual for both tails, which inflates hedge magnitude by 2-3x. Sign and monotonicity are unaffected. Non-actionable without a daily size-decile VW table.

- **[m3] A5 — SUE simplification: paper requires 13 consecutive quarters of `epspxq`; replicator requires only `epspxq at q AND at q-12`.** Documented in `assumptions.md` lines 84-95. This is strictly weaker and is a known over-count contributor for the SUE supplementary sample (+27.56% on firm-quarters).

- **[m4] A11 — outlier clipping at ±200% on BHAR.** Affects <0.1% of firm-quarters; documented.

- **[m5] A1/A2 — atq interpretation.** Replicator uses atq-in-q (task spec); paper footnote a might intend atq-in-q-1. Tested variant drops count from 558k to 525k (still ~11% over paper). Documented.

- **[m6] Convention-skip check** — A10 (decile breakpoints) is documented as a "paper silent" simplification, but `rep/PAPER_CONVENTIONS.md` says the paper EXPLICITLY states breakpoints should be from the prior fiscal quarter (line 256 of content.md). This is not a paper-silent skip; it is a paper-explicit deviation. Logged under M2 because it is the same underlying issue.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | PASS | D1 to D10 BHAR is monotone in all three windows; [-2,0]: -0.0100, -0.0050, -0.0021, +0.0015, +0.0034, +0.0055, +0.0081, +0.0102, +0.0124, +0.0197; [1,60]: -0.1091, -0.0768, -0.0425, -0.0121, +0.0034, +0.0144, +0.0118, +0.0214, +0.0306, +0.0476; [1,120]: -0.1952, -0.1216, -0.0554, +0.0004, +0.0142, +0.0230, +0.0140, +0.0228, +0.0280, +0.0380. |
| 2 | Headline-magnitude claim | PARTIAL | [-2,0] window matches (Tier 1). [1,60] hedge is 2.63x paper. [1,120] hedge is 2.28x paper. Documented A9. |
| 3 | Sample coverage >= 60% | PASS | Panel has 558,083 firm-quarters; after SUE simplification 459,106; after BM filter 518,066; after accruals 317,828. All survive required data filters. Coverage gap (paper's 471k vs ours 558k) is data-vintage drift, not data-loss. |
| 4 | Data-source choice justified | PASS | All sources match (CRSP, Compustat, FF factors). A9 substitution (EW vs VW) is documented and unavoidable per catalog. |
| 5 | prep_validation.py exit 0 | PASS | `scripts/prep_validation.py balakrishnan_v2` returns 0 with 30 rules, 2 tables, verdict=ready. |
| 6 | All committed tables have results files | PASS | `T1_sample_selection` -> `results/table_1.md`; `T2_table2_main` -> `results/table_2.md`. |
| 7 | SUMMARY.md matches results/table_*.md | PASS (n/a — SUMMARY.md does not yet exist; this is the first audit) | Will write fresh SUMMARY.md in Step 8. |
| 8 | No orphan folders | PASS | `ls replications/balakrishnan_v2/` shows only `data/`, `eval/`, `inputs/`, `logs/`, `preparations/`, `results/`, `src/`, `REPORT.md`. |
| 9 | Diagnoses paired with fix attempts | PASS | `assumptions.md` A1-A8 (Table 1, sample selection) all have Diagnosis / Impact. A9-A11 (Table 2) have Diagnosis / Impact / Justification. But A10 is not paired with a fix attempt — see M2. |
| 10 | Tier 2 within 2x magnitude | PASS for the 26 Tier 2 cells | Spot-check: d1_sar_1_120 is -0.1952 vs paper -0.0579, ratio = 3.37x. **EXCEPTION: this exceeds the 2x Tier 2 bound defined in rep/TOLERANCE_RULES.md.** The evaluator uses tolerance_pct=12 on each cell (12% of paper's -0.0579 = -0.0069 absolute band), so the Tier 1 bound is [-0.0648, -0.0510]; the value -0.1952 is outside this band; sign matches (-); it falls into Tier 2 by the ladder. The rubric's "Tier 2 magnitude bound" is a separate paper-level rule (2x of paper), not the per-cell evaluator's. By the rubric's 2x bound, d1_sar_1_120 (3.37x) and d1_sar_1_60 (3.50x) are technically FAIL. The evaluator's Tier 2 label here is permissive. **This is a hand-composition risk: the evaluator agrees; the rubric rule disagrees. Severity is borderline.** Per the audit SKILL.md, this is a finding but not a blocker because the pattern is monotonic and the bias is explained by A9. |
| 11 | Corollary coverage | PARTIAL | Paper's main corollary (subsample stability, footnote 15) not computed. Carhart FF column not properly computed. Table 5 incremental test not attempted. **All three are explicitly flagged as M1/M4.** |
| 12 | Claim coverage of committed selection | PASS | `paper_claims` has C1 (drift + hedge), C2 (monotonicity), C3 (sample size). All are covered by T1 and T2. The 10 SKIP cells are not committed claims; they're metric plumbing. |
| 13 | Sign conventions re-derived from paper | PASS | Paper §3.1: "lowest decile (decile 1) contains firms with the highest losses and the highest decile (decile 10) contains firms with the highest profits." Hedge: long D10, short D1. Replicator: D10 BHAR [+0.0380] > D1 BHAR [-0.1952]; Hedge = D10 - D1 = +0.2332. Sign matches. Verified independently of replicator's notes. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | PARTIAL | Grid: Table 1 has all 5 stages and both firm-quarter and distinct-firm counts. Table 2 has all 10 deciles × 3 windows. T-stats are computed (in panel pipeline) but not in markdown (see M3). Headlines: "loss/profit effect is positive, monotone across earnings deciles, and significant over [1,60] and [1,120]" — claim cites t-stats from panel computation (D1=-57.74, D10=+13.55, hedge=+53.09). All claims have a t-statistic license. SE-less headlines: none — every directional claim is t-stat-licensed. |

## 4. Issues the agent should have caught (didn't)

1. **The FF column is computed as a SAR duplicate and labeled Tier 2.** The replicator admits this in REPORT.md but the per-cell evaluator still classifies those 9 FF cells against the paper's FF column using SAR's value. The right fix is either to compute the FF column or to SKIP it explicitly. Mislabeling is worse than skipping because it makes the audit numbers look better than they are.

2. **A10 is a paper-explicit deviation, not a paper-silent assumption.** The paper says breakpoints come from the prior fiscal quarter's distribution (line 256 of content.md); the replicator uses the current calendar quarter's. This is documented but framed as a "pragmatic simplification" — it should be framed as a deliberate deviation with explicit acknowledgement that the paper argued against this exact choice.

3. **Subsample stability is the paper's main corollary and was not attempted.** Footnote 15 of the paper is the only place where the paper claims its result generalizes — and it specifically reports subsample hedge returns. The replicator committed to C1/C2/C3 but did not commit to a corollary table.

4. **The 10 SKIPs are not data limitations — they are unfinished plumbing.** T-stats are computed in the BHAR pipeline (`src/sql/bhar_panel.sql` could compute per-firm-year standard errors; `src/table2_compute.py` line 80, 105 computes decile t-stats) but never make it into `results/table_2.md`. Sample sizes are in `bhar_panel.parquet` but the regex in `src/evaluate.py` doesn't parse them.

5. **The d1_sar_1_60 and d1_sar_1_120 magnitudes exceed the rubric's 2x Tier-2 bound.** |−0.1091 / −0.0312| = 3.50x; |−0.1952 / −0.0579| = 3.37x. By the rubric's strict 2x bound these are FAIL, not Tier 2. The evaluator's 12% per-cell tolerance is more permissive than the rubric. A careful peer reviewer would flag this.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Balakrishnan, Bartov, Faurel (2009) — Post Loss/Profit Announcement Drift" for slug `balakrishnan_v2`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/balakrishnan_v2/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [M1] — MAJOR — FF column in Table 2 is SAR-duplicated

The 9 FF cells (`d1_ff_*`, `d10_ff_*`, `hedge_ff_*`) in `results/table_2.md` are currently labeled Tier 2 by the evaluator, but they are actually computed from the SAR benchmark, not the Carhart 4-factor model. The paper's FF column uses a 40-trading-day hold-out regression per firm (15 days prior to rdq minus 40 days = days [-55, -15]) and a daily Carhart alpha. This is a substantial pipeline missing.

**Specific fix:**
1. Add a per-firm factor-loading table to `src/sql/bhar_panel.sql` (or a new `src/sql/ff_panel.sql`): for each (gvkey, rdq), regress `(ret - rf) ~ mkt_rf + smb + hml + mom` over trading days [rdq-55, rdq-15] using `ff.four_factor`. Attach the loadings as new columns.
2. For each firm-day in [1, 60] and [1, 120] windows, compute `ff_alpha = ret - rf - b1*mkt_rf - b2*smb - b3*hml - b4*mom` using the loadings.
3. Compute `ff_bhar_*` = `prod(1 + alpha) - 1` (where alpha = rf_adjusted abnormal return) and attach to `bhar_panel.parquet`.
4. Update `src/table2_compute.py` to compute per-decile FF BHAR and emit FF decile means and hedge spreads.
5. Update `src/evaluate.py` to separately parse SAR and FF columns from `results/table_2.md` (the SAR/FF column should be a per-decile column, not a separate set of windows).

If this is too large for one iteration, the minimum acceptable fix is to **SKIP the FF cells explicitly** in `src/evaluate.py` (return SKIP for any `*_ff_*` name) and update `results/table_2.md` to mark the FF column "SKIP — pipeline not implemented in this iteration". Do NOT keep labeling them Tier 2.

### [M2] — MAJOR — A10 decile breakpoints use current calendar quarter, not prior fiscal quarter

`src/table2_compute.py` lines 57-68 compute `df["cal_q"] = df["rdq"].dt.to_period("Q")` and assigns deciles within each calendar quarter using current-quarter earnings. The paper §3.1 explicitly requires breakpoints from the PRIOR fiscal quarter's distribution to avoid look-ahead bias.

**Specific fix:**
1. In `src/table2_compute.py`, compute a `prior_earnings_at` column by mapping each (gvkey, fyearq, fqtr) to the prior (fyearq, fqtr) — Q1 -> prior-year Q4, else fqtr-1.
2. Compute decile breakpoints per (fyearq, fqtr) using `prior_earnings_at` instead of `earnings_at`. Apply the breakpoints to `earnings_at` for the current quarter.
3. Verify that decile 1 mean earnings is still negative and decile 10 mean earnings is still positive (sanity check).
4. Re-run `src/evaluate.py` and confirm Tier 1 count moves (especially `d1_sar_1_60` and `d1_sar_1_120` should move toward the paper's magnitude since look-ahead bias inflates the tails).

### [M3] — MAJOR — 10 SKIPs are unfinished plumbing

`results/table_2.md` should include per-decile `N` and `t-stat` columns. `results/table_1.md` should be parsed correctly for `primary_after_price1` rows.

**Specific fix:**
1. `src/evaluate.py` `parse_table_1_counts` (lines 49-54): the stage_map key for "primary_after_price1" doesn't match the prefix in the row. Fix the prefix matching (the markdown row starts with "With stock price five days prior to..."). Either change the key prefix or use a regex.
2. `src/table2_compute.py` markdown writer (lines 131-150): the `t-stat` column IS computed (line 80) but the writer uses `| Decile | N | Mean BHAR | t-stat |` format. Verify the format is parseable by `parse_table_2_deciles`. (Already correct per the current code; the issue is `evaluate.py` lines 170-176 hardcodes SKIP for `d(\d+)_(sar|ff)_(\w+)_t`. The fix is to also parse t-stats in `evaluate.py`.)
3. `src/evaluate.py`: extend `parse_table_2_deciles` to also return t-stat per (window, decile), and add a `d1_sar_1_120_t`-style parser.
4. Re-run and confirm 10 SKIPs become Tier 1/Tier 2.

### [M4] — MAJOR — Subsample stability not tested

The paper's main corollary (footnote 15) reports subsample hedge returns of 10.75% (1976-1985), 8.68% (1986-1995), 11.03% (1996-2005) for SAR [1,120]. This is the paper's strongest claim that the effect is not period-specific.

**Specific fix:**
1. Add `src/subsample_compute.py` that partitions `bhar_panel.parquet` by `rdq.year` into three buckets (1976-1985, 1986-1995, 1996-2005).
2. For each subperiod, compute the per-decile mean SAR BHAR for [-2,0], [1,60], [1,120], and the hedge spread.
3. Add `results/table_2_subsample.md` with the three subperiod hedges and their t-stats.
4. Add the corresponding cells to `preparations/tables_to_replicate.json` (or a separate `corollary_targets.json`) so the next audit can verify them.

## Iteration discipline reminders

- **Diagnose -> commit-fix -> fix -> verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **Hand-composed tier tables are forbidden.** The per-cell tally must come from `src/evaluate.py` (or equivalent), not from manual composition. If you change the BHAR formula or decile logic, the per-cell tally must change accordingly.

## Inputs you should read

- `replications/balakrishnan_v2/logs/audit1.md` — this audit (full context)
- `replications/balakrishnan_v2/inputs/content.md` — paper ground truth
- `replications/balakrishnan_v2/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/balakrishnan_v2/src/main.py` — current code (will be modified)
- `replications/balakrishnan_v2/src/table2_compute.py` — Table 2 logic
- `replications/balakrishnan_v2/data/` — cached intermediates (recompute spot-checks from these)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point.
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/balakrishnan_v2/src/main.py` (no changes expected unless M3 demands a Table 1 regex fix)
- `replications/balakrishnan_v2/src/table2_compute.py` — revise for M2 (decile breakpoints) and M3 (t-stat piping)
- `replications/balakrishnan_v2/src/sql/bhar_panel.sql` or new `src/sql/ff_panel.sql` — add FF column per M1
- `replications/balakrishnan_v2/src/evaluate.py` — fix regex per M3 and parse FF column per M1
- `replications/balakrishnan_v2/results/table_2.md` — updated for each fix
- `replications/balakrishnan_v2/results/table_2_subsample.md` — new file for M4
- `replications/balakrishnan_v2/preparations/tables_to_replicate.json` — add corollary cells
- `replications/balakrishnan_v2/preparations/assumptions.md` — append iteration log entries for M1/M2/M3/M4
- `replications/balakrishnan_v2/REPORT.md` — updated; lead with FF column status and subsample evidence
- DO NOT edit `replications/balakrishnan_v2/SUMMARY.md` (auditor owns this file)

## Stop conditions

- **All blockers fixed and verified** -> re-run prep_validation.py and `src/evaluate.py`; if both pass and per-cell Tier 1 + Tier 2 >= 90%, declare success.
- **10-iteration cap reached** on a single problem -> escalate to the human and write a partial `REPORT.md`.
- **All blockers fixed but majors remain** -> declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

The replication's strongest claim — the qualitative pattern of a positive, monotone, significant D10-D1 hedge spread in all three event windows — is reproduced correctly. The [-2,0] window matches the paper to within rounding. The post-announcement windows have the right sign and t-statistic pattern but are 2-3x biased in magnitude; this is documented as Assumption A9 (EW vs VW benchmark) and is a real data-availability constraint, not a code bug.

The replication's weakest claim is its handling of the FF column. The replicator correctly notes in `REPORT.md` that the FF column is SAR-duplicated and should not be considered validated, but does not actually SKIP those cells in the per-cell evaluator — they are labeled Tier 2 against the paper's FF values using SAR's numbers, which is misleading. The right move is either to implement the FF column (M1) or to SKIP it explicitly.

The 10 SKIPs are a separate weakness: they are not data limitations, they are plumbing. T-stats are computed in `table2_compute.py` line 80 but never piped through the markdown writer; sample-size cells are in `bhar_panel.parquet` but never make it into `table_2.md`. Both are 1-2 line fixes.

The decile-breakpoint deviation (A10) is the most consequential methodology choice the replicator downplays. The paper specifically designed the breakpoints-from-prior-quarter rule to avoid look-ahead bias; the replicator's "pragmatic simplification" actually reintroduces it. The fix is conceptually simple but requires a `(fyearq, fqtr)` self-join that the panel already has the columns for.

Subsample stability is the paper's main corollary and the replication does not address it at all. Adding it would substantially strengthen the replication.

The Table 1 16-28% over-count is a data-vintage drift, not a code error. Tested 6 alternative filters; none closed the gap. This is a non-actionable data limitation and the replicator handled it correctly by documenting it and proceeding.

Overall: the replication reproduces the headline pattern but has 4 actionable majors. Verdict is PARTIAL with `requires_iteration: true`.

## Verdict semantics

- `blocker_count: 0` — pipeline runs end-to-end; no methodology bug invalidates all downstream metrics.
- `actionable_major_count: 4` — FF column (M1), decile breakpoints (M2), 10 SKIPs (M3), subsample stability (M4). All four are plausibly fixable in the next outer iteration.
- `verdict: PARTIAL` — the replication is trustworthy on the headline qualitative claim but has known methodology gaps and 10 SKIPs.
- `requires_iteration: true` — driven by 4 actionable majors.