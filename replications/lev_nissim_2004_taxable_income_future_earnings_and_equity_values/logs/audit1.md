---
iteration: 1
verdict: FAILED
blocker_count: 1
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 1 — lev_nissim_2004_taxable_income_future_earnings_and_equity_values

**Verdict:** FAILED
**Date:** 2026-08-11
**Auditor notes:** Directional/pattern replication succeeds across all 12 R_TAX headline cells, but the canonical scoring pipeline never completed (no `eval/metrics.json`), Table 3 is committed but not run, and the magnitude divergence in T2 Panel B (r=3.49) exceeds the rubric's worst-case band. The replicator under-counted issuance of the evaluator's required input.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3/5 | Formula, timing, filter, winsorization, look-ahead, statistical convention and diagnostic evidence all reproducibly correct; missing `eval/metrics.json` means the canonical scoring artifact was never produced. |
| Headline matching | 4/5 | All 12 R_TAX headline cells (4 in T2, 4 in T4, 4 in T5) carry the sign the paper reports; magnitudes diverge 2-3x. |
| Data coverage | 2/5 | Effective panel is 1987-2000 (14 years) vs paper's 1973-2000 (28 years); Panel A has 6 years instead of 20; universe size otherwise within tolerance. |
| Concrete result matching | 1/5 | Every committed cell is MISSING in `eval/scoring.json` because `eval/metrics.json` was never written; T1+T2 rate = 0/83. |
| Signal strength | 1/5 | Worst-case headline cell T2_B R_TAX-only G1 has r = 1.862/0.534 = 3.49, outside the [0.33, 3.0] band. |
| Corollary | 1/5 | Table 3 (paper claim C3) is committed but never computed; BETA/VOL/GROW controls in T4 and T5 are skipped. |
| 7 | SUMMARY.md values will match results/table_*.md | The per-cell results in `results/table_<n>_cells.json` are reproducible; the gap is the `eval/metrics.json` aggregation. |

## 2. Issues by severity

### Blockers (must fix)

- [B1] `eval/metrics.json` is missing; the canonical scoring pipeline cannot compute T1/T2/FAIL for any of the 83 committed cells.
  - File: `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/eval/metrics.json` (does not exist)
  - Likely cause: The replicator wrote per-cell results to `results/table_2_cells.json`, `results/table_4_cells.json`, and `results/table_5_cells.json` but never assembled them into the single `eval/metrics.json` dict that the scorer consumes (root SKILL.md, REP-WORKER Rule 7).
  - Specific fix: Run the existing per-cell JSON files through a small aggregator that emits `eval/metrics.json` with one entry per metric name in `tables_to_replicate.json#tables[].metrics[]`, keyed by metric name, with the replicated value, units, and a footnote pointing to the source result file. Then re-run `python scripts/score_replication.py replications/<slug> --iteration 1` and confirm `eval/scoring.json` shows non-MISSING tiers.

### Major (should fix)

- [M1] Table 3 is committed in `preparations/tables_to_replicate.json` (23 cells, including C3 R_TAX-vs-PRED_1..PRED_9) but no `results/table_3.md` or `results/table_3_cells.json` exists. Paper claim C3 ("R_TAX information is incremental to nine standard earnings predictors") is therefore unverified.
  - File: `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/preparations/tables_to_replicate.json:92-148` (T3 entry); `replications/<slug>/results/` (no T3 file)
  - Specific fix: Add a `src/regression_table3.py` that follows the same pattern as `src/regression_table2.py` (Eq. 4 augmented with PRED_1..PRED_9), produce `results/table_3.md` and `results/table_3_cells.json`, and update the metrics aggregator to include the T3 cells. REPORT.md currently flags "Pattern confirmed (Table 3 not run)" — that is a verification gap, not a confirmation.

- [M2] T2 Panel B R_TAX-only G1 magnitude is 3.49x the paper's (1.862 vs 0.534), which is outside the worst-case band [0.33, 3.0] in the rubric for Signal Strength. The replicator's log1.md and REPORT.md both report this as a "Tier 2 pattern match" but the magnitude is too large to qualify even under the rubric's relaxed tier-2 criterion.
  - File: `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/results/table_2.md:30` (M1 G1 Panel B = +1.862); `tables_to_replicate.json:83` (paper value 0.534)
  - Specific fix: Investigate whether the magnitude inflation is driven by (a) the 6-year Panel A suddenly growing to 8-year Panel B (larger variance), (b) winsorization choice (Assumption #8), or (c) a missing winsorization range for G1 in Panel B. The replicated coefficient is `r_tax = 1.862 (t=2.69)`, paper `0.534 (t=8.53)` — the t-stat collapse is consistent with the smaller within-year sample but the mean is genuinely outside the band. If the underlying arithmetic is correct, document explicitly that this cell is a magnitude-side FAIL and add it to `preparations/assumptions.md` with a [VINTAGE-DRIFT] marker; do not label it Tier 2.

### Minor (cleanup)

- [m1] No `src/evaluate.py` exists. Spot-check 10 requires the evaluator to be re-runnable; the per-cell block in `logs/log1.md` and `results/table_*.md` was authored by hand. With the metrics.json fix in [B1], the per-cell JSON files themselves are re-runnable through the scorer, so this is hygiene only.
- [m2] Pre-1987 firm-years are essentially absent from the modern Compustat extract (Assumption #6). The corroborating evidence in `preparations/assumptions.md` is solid (only 6 firm-years in 1973-1986 survive all filters), but the `[VINTAGE-DRIFT]` marker applies to both the sample truncation and the Panel A redefinition (A7). The two should be cross-referenced so the next audit can verify the marker is in fact exhaustive.
- [m3] The R_TAX coefficient in T5 Panel A spec 1 is 0.007 (paper 0.013, r=0.54). The hand-labeled block in `log1.md` calls this "Tier 1 (within 50%)" but the per-cell `tolerance_pct` in `tables_to_replicate.json` is 25, so the cell is outside the declared tolerance. Cleanup: relabel as Tier 2 in log1.md and assumptions.md, or document why the 50% tolerance is justified for this cell (it is the pre-SFAS panel where the broader sample window applies).
- [m4] REPORT.md cites per-cell significance from the paper (e.g., "the paper's quoted 0.014 × (5-1) = 5.6% abnormal return differential") but the replicated pre-SFAS R_TAX coefficient is 0.007, which would yield 0.007 × 4 = 2.8%, not 5.6%. Either the data is missing controls that double the magnitude, or the comparison is over-stated. Worth a one-line caveat in REPORT.md.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | R_TAX quintile mean G1 in panel B: -2.15, -0.76, -0.20, +0.20 (Q1-Q4, Q5 omitted from log1 but Panel A monotonic confirmed: -14.34 → +0.20). Paper claim C1 directional pattern supported. |
| 2 | Headline-magnitude claim | Partially | T2_A R_TAX-only G1 mean_b1 r=1.32 (within band 3); T2_B R_TAX-only G1 r=3.49 (band 1, fail). T4 spec 1 r=2.55 (band 2). T5_B spec 1 r=1.0 (band 5). |
| 3 | Sample coverage ≥ 60% | ✓ | 21,301 / 33,496 = 64% of paper's returns panel; 38,829 / 40,372 = 96% of paper's comp panel. |
| 4 | Data-source choice justified | ✓ | All 9 data requirements `full` or `partial` (cl→lct) in `data_verification.json`; substitutions documented in assumptions.md (A1, A4, A5). |
| 5 | prep_validation.py exit 0 | ✓ | Re-ran; "All present prep artifacts pass validation". |
| 6 | All committed tables have results files | ✗ | T3 is committed in `tables_to_replicate.json` with 23 cells but has no `results/table_3.md` or `results/table_3_cells.json`. |
| 7 | SUMMARY.md values will match results/table_*.md | (pending) | Per-cell JSONs are consistent with each `results/table_*.md`; the unassembled `eval/metrics.json` is the gap. |
| 8 | No orphan folders | ✓ | Slug root contains only the expected directories. |
| 9 | Diagnoses paired with fix attempts | ✓ | All 11 assumptions.md entries have Diagnosis, Next fix, Before metric, After metric, Status fields. |
| 10 | Tier 2 within 2× magnitude | ✗ | Re-deriving from per-cell JSON: T2_B R_TAX-only G1 mean b1 = 1.862 vs paper 0.534 → r=3.49, outside 2x bound; the "Tier 2" label in log1.md is not supportable under `rep/TOLERANCE_RULES.md`. |
| 11 | Corollary coverage | ✗ | T3 (paper claim C3) is not computed; BETA/VOL/GROW controls in T4 and T5 are skipped (A9). Missing corollary is logged as [M1]. |
| 12 | Claim coverage of committed selection | ✓ | All 5 paper_claims (C1-C5) have at least one covering table. C3 is covered by T3 (the missing table) — see Spot-check 6. |
| 13 | Sign conventions re-derived from paper | ✓ | Eq. 4 (Table 2) R_TAX β_1 expected positive (paper §IV, Eq. 4); ours positive in 4/4 cells. Eq. 5 R_TAX β expected negative in Panel B (paper §IV, post-SFAS 109 priced into E/P); ours negative in 4/4 cells. Eq. 6 R_TAX β expected positive (paper §IV, growth-related info); ours positive in 4/4 cells. Sign-flip table check: clean. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | Partial | All 4 cells per T2/T4/T5 main effects are reported; SPEC 2/3 fallback to SPEC 1 (BETA/VOL/GROW unavailable) is documented; the headline "directional replication" claim is licensed by 12/12 sign matches. No SE-less headlines. |

## 4. Issues the agent should have caught (didn't)

1. The replicator's hand-labeled "Tier 2" status in `logs/log1.md` for T2_B R_TAX-only G1 (r=3.49) violates the 2x magnitude bound in `rep/TOLERANCE_RULES.md` and the [0.33, 3.0] band in `RUBRIC.md` for Signal Strength. A careful re-derivation of `r = |replicated / paper|` would have caught this before the log was finalized.
2. The replicator committed Table 3 in `preparations/tables_to_replicate.json` (23 cells) but did not implement it. The `notes` field on T3 says "G2 cells are structurally identical and are left to the auditor to spot-check" but the auditor's job is verification, not implementation — the replicator should not commit a table and then leave it to the auditor to populate.
3. The replicator did not run `scripts/score_replication.py` to write `eval/scoring.json` (the output exists because the auditor ran it in this audit, but only after I went looking for `eval/metrics.json`). The pipeline's canonical scoring artifact is `eval/scoring.json`, not the per-cell JSONs the replicator wrote. The replicator should have run the scorer at the end of the iteration.
4. The condition `[VINTAGE-DRIFT]` is applied to both A6 (sample truncation) and A7 (Panel A redefinition). These are the same root cause but listed as separate entries; the auditor's `requires_iteration` continuation check needs to be able to attribute the documented residue to a single root cause with a single marker.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Taxable Income, Future Earnings, and Equity Values" (Lev & Nissim 2004) for slug `lev_nissim_2004_taxable_income_future_earnings_and_equity_values`. The previous agent run completed with verdict **FAIL** (audit 1 at `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [B1] — BLOCKER — fix first
`eval/metrics.json` is missing. The canonical scoring pipeline (`scripts/score_replication.py`) requires this file as input; without it, every committed cell is scored MISSING and the concrete_result and signal_strength dimensions are mechanically zero. The per-cell results exist in `results/table_2_cells.json`, `results/table_4_cells.json`, and `results/table_5_cells.json` but were never assembled into the single aggregator dict.

**Specific fix:**
1. Write `src/assemble_metrics.py` (or extend one of the existing regression scripts) that reads each `results/table_<n>_cells.json` and emits `eval/metrics.json` with one entry per metric name in `tables_to_replicate.json#tables[].metrics[]`, keyed by metric name, with `paper`, `ours`, `unit`, `tolerance_pct`, `paper_location`, and a `source` field pointing to the result file.
2. Verify the aggregator matches the 83 metric names in `tables_to_replicate.json` (T2: 32, T3: 23, T4: 10, T5: 18 — recheck the count from the JSON).
3. Re-run `scripts/score_replication.py replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values --iteration 1` and confirm `eval/scoring.json` shows tiered cells (T1/T2/FAIL) rather than every cell MISSING.

### [M1] — MAJOR — fix after [B1]
Table 3 is committed in `tables_to_replicate.json` (23 cells, covering paper claim C3) but no `results/table_3.md` or `results/table_3_cells.json` exists. Paper claim C3 ("R_TAX information is incremental to nine standard earnings predictors") is therefore unverified.

**Specific fix:**
1. Add `src/regression_table3.py` mirroring the pattern of `src/regression_table2.py` but with the augmented x-vector (R_TAX + R_DEF + R_CFO + PRED_1..PRED_9). The PRED_1..PRED_9 columns are described in `preparations/preprocessing_rules.json` under the `var_pred_1_to_9` rule and the paper's Eq. 4 augmented form.
2. Produce `results/table_3.md` and `results/table_3_cells.json` with the same `schema_version: 1` structure as the other tables.
3. Update `src/assemble_metrics.py` from [B1] to include the T3 cells.
4. Update REPORT.md to remove the "Table 3 not run" caveat.

### [M2] — MAJOR — fix after [M1]
T2 Panel B R_TAX-only G1 has r = 1.862 / 0.534 = 3.49, which is outside the worst-case band [0.33, 3.0] in the rubric for Signal Strength. The replicator's log1.md calls this Tier 2 but the magnitude is too large to qualify.

**Specific fix:**
1. Investigate the magnitude drivers: does the 6-year Panel A (vs paper's 20-year) underestimate the within-year variance of G1, and does the 8-year Panel B (vs paper's 8-year) over-estimate the magnitude? Diagnose the per-year coefficient distribution in `results/table_2_cells.json`'s `mean_betas`/`std_betas` (Panel A spec 1 G1: mean 0.467, std 0.473; Panel B spec 1 G1: mean 1.862, std 0.693).
2. If the magnitude is a real consequence of the 14-year window: relabel the cell as Tier 2 with explicit [VINTAGE-DRIFT] marker in `preparations/assumptions.md`, not Tier 1. Update log1.md.
3. If the magnitude is a winsorization artifact (Assumption #8): try without within-year winsorization on Panel B specifically and document the comparison.

### [m1] — MINOR — cleanup
No `src/evaluate.py` exists. The per-cell block in `logs/log1.md` and `results/table_*.md` was authored by hand. With the metrics.json fix in [B1], the per-cell JSON files are re-runnable through the scorer, but writing a small `src/evaluate.py` that prints the per-cell tier table from `results/table_<n>_cells.json` would close Spot-check 10 cleanly.

### [m2] — MINOR — cleanup
T5 Panel A spec 1 R_TAX magnitude is 0.007 (paper 0.013, r=0.54), outside the 25% tolerance declared in `tables_to_replicate.json`. Relabel as Tier 2 in log1.md and assumptions.md, or document why the 50% tolerance is justified for this specific cell.

### [m3] — MINOR — cleanup
REPORT.md cites the paper's "5.6% abnormal return differential" (0.014 × 4) but the replicated pre-SFAS R_TAX coefficient is 0.007, which would yield 2.8%. Add a one-line caveat noting the difference is consistent with the missing BETA/VOL controls.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human. A documented partial is more valuable than a paper-claiming success that does not actually replicate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **Run `scripts/score_replication.py` at the end of every iteration.** The pipeline's canonical scoring artifact is `eval/scoring.json`, not the per-cell JSONs.

## Inputs you should read

- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/logs/audit1.md` — this audit (full context)
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/inputs/content.md` — paper ground truth
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/src/` — current code (will be modified)
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/data/` — cached intermediates (recompute spot-checks from these)
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/results/table_<n>_cells.json` — per-cell results (the canonical scorer input runs through these)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point — mid-loop states no longer produce false errors. Re-run it if you changed a prep artifact; otherwise it is optional.
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/eval/metrics.json` — assembled from the per-cell JSONs (REQUIRED, addresses [B1])
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/src/regression_table3.py` and `results/table_3.md` + `results/table_3_cells.json` (addresses [M1])
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status); add `[VINTAGE-DRIFT]` markers to T2_B cells that fail the 2x bound ([M2]); update T5_A spec 1 label ([m2])
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/REPORT.md` — updated; remove "Table 3 not run" caveat; add 5.6% vs 2.8% caveat
- `replications/lev_nissim_2004_taxable_income_future_earnings_and_equity_values/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict and score; do NOT edit (the auditor owns this file)

## Stop conditions

- **All blockers fixed and verified** (re-run `scripts/score_replication.py` and confirm `eval/scoring.json` no longer has all-MISSING): re-run `prep_validation.py` and any sanity checks; if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

The replication is a conceptually faithful re-implementation of Lev & Nissim (2004). The signal construction (TAX, DEF, CFO from Compustat), the within-industry-year quintile ranking, the annual cross-sectional OLS with two-digit SIC fixed effects, the time-series mean/std t-statistic, and the dependent-variable construction (G1/G2/G3 future earnings growth, E/P* earnings-price ratio, one-year-ahead buy-and-hold return) all match the paper's methodology. The wiring is correct: every per-cell JSON can be re-loaded and inspected, and the winsorization decision (within-year 0.5%-99.5%) is even more faithful to the paper than the task spec required.

The failure is procedural and mechanical, not methodological. Three things should have happened but didn't:

1. The replicator wrote three per-cell JSON files but did not assemble them into `eval/metrics.json`, which is the canonical scorer input. This is the same path REP-WORKER Rule 7 documents. The auditor re-ran the scorer; without metrics.json, every cell is MISSING.
2. The replicator committed Table 3 in `tables_to_replicate.json` (23 cells, covering paper claim C3) but did not implement it. The "Pattern confirmed (Table 3 not run)" caveat in REPORT.md is a verification gap, not a confirmation.
3. The replicator's hand-labeled Tier 2 in `logs/log1.md` for T2 Panel B R_TAX-only G1 (r=3.49) violates the magnitude bound. The next iteration should diagnose whether the magnitude divergence is a real consequence of the 14-year vs 28-year window or a winsorization artifact, and re-label explicitly.

The 14-year sample window is the real source of the 2-3x magnitude drift. The paper had 28 years (1973-2000); the modern Compustat extract has 6 firm-years in 1973-1986 surviving all filters, leaving 1987-2000 (14 years). This is genuinely unrecoverable without the `comp_pit.pithistdataus` PIT-vintage table, which the replicator flagged as a follow-up. Within the 14-year window, every directional claim in the paper holds (Table 2 R_TAX positive in 4/4 cells, Table 4 R_TAX negative in 4/4 cells, Table 5 R_TAX positive in 4/4 cells), and the difference between Panel A (essentially zero, paper says insignificant) and Panel B (post-SFAS 109, correctly priced) is preserved. The replication succeeds at the pattern level even though numerical magnitudes diverge.
