---
iteration: 1
verdict: FAILED
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 1 — jegadeesh_1990_evidence_of_predictable_behavior_of_security_returns

**Verdict:** FAILED
**Date:** 2026-08-11
**Auditor notes:** Strong replication with 88/89 cells Tier 1/2 (98.9%). Headline S0 P1-P10 spread (C1) and serial-correlation coefficients (C2) reproduce cleanly. One FAIL on a January-only S1 P1 alpha (low-statistics cell) and one Tier-1 magnitude violation (R² for Q1/Q3 size subsamples uses unadjusted R² instead of the paper's adjusted R²).

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | 7/8 sub-checks pass; Q1/Q3 R² reported unadjusted despite tables_to_replicate.json describing it as adjusted (Assumption 16 documents the choice; both series emitted in metrics.json). |
| Headline matching | 5 | S0 P1-P10 spread 0.0286 vs paper 0.0249 (C1), a_1 = -0.0969 vs -0.0923 (C2), a_12 = 0.0317 vs 0.0339 (C3), Feb-Dec pattern preserved (C4). All headline claims reproduce. |
| Data coverage | 5 | Panel 1929-1982 has 1,868 stocks/month avg; 1934-1987 has 2,339 stocks/month; 1963-1987 has 3,980 stocks/month. Join hygiene clean (0 duplicates). Periods and universe match. |
| Concrete result matching | 5 | 88/89 = 98.9% within tolerance (Tier 1 + Tier 2). Only single FAIL on `s1_p1_alpha_jan` (low-statistics January-only regression, n=54). |
| Signal strength | 1 | Worst-case headline r = 3.63 on `s1_p1_alpha_jan` (FAIL). Even excluding FAIL, `all_jan_a12` has r=2.72, `s0_p10_posprop_jandec` r=2.57. r=3.63 outside [0.33, 3.0] band → score 1 per rubric. |
| Corollary | 5 | All 13 corollary cells (T4 6/6, T5 7/7) are Tier 1/2 (100%). Spearman rank correlations Tier 1, size-model spread alphas Tier 1. |
| Overall | 3.50 | Mean of 6 dimensions; bright line ≥ 3.0 → REPLICATED, but a Signal Strength = 1 forces FAILED per rubric § Kill switch. |

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] **Single FAIL on `s1_p1_alpha_jan`** — paper 0.0085, ours 0.0308 (r=3.63). This is a January-only S1 P1 regression with 54 monthly obs, so statistical power is low, but the ratio is far outside the 2x Tier-2 cap and drives Signal Strength to band 1. Root cause plausibly explained (Assumption 17: paper footnote 15 says January a_jt should come from January-only regressions in the previous 5 years; replicator uses standard 5-year rolling window for all months). The replicator's documented partial is consistent with a paper-silent convention deviation, but the magnitude gap is also a candidate for sample-vintage sensitivity.
  - File: `eval/metrics.json:s1_p1_alpha_jan` (0.0308); `preparations/assumptions.md:215` (Assumption 17 rationale); `logs/log1.md:86-88` (replicator classifies as "likely sample-period sensitivity").
  - Specific fix: implement footnote 15's January-only forecast regression (54 monthly estimates using January CS regressions over the previous 5 years, then average to form the January forecast coefficients). Re-run S0 P1 January alpha and S1 P1 January alpha. If the FAIL persists at this r level after the convention fix, retire it with `[CONVENTION-APPLIED]` evidence — but the convention deviation alone is the more likely cause than sample drift, so the fix is in reach.

- [M2] **Q1/Q3 R² cells use unadjusted R² despite tables_to_replicate.json describing "adjusted R^2"** — paper R² for Q1 is 0.093 (matches adjusted-R² convention per Assumption 16: q1_r2_adj=0.085 vs paper 0.093 = Tier 1; instead we shipped unadjusted 0.144 = Tier 2 with rel_err 0.55). Same for Q3 (paper 0.113, our adj 0.122 = Tier 1; unadj 0.194 = Tier 2).
  - File: `eval/metrics.json:q1_r2=0.1440` (unadjusted); `inputs/tables_to_replicate.json:77,82` (target named "adjusted R^2"); `preparations/assumptions.md:189-204` (Assumption 16 documents the choice but ships unadjusted as the headline metric).
  - Specific fix: emit `q1_r2_adj` and `q3_r2_adj` as the metric values (already computed in metrics.json as q1_r2_adj=0.0847, q3_r2_adj=0.1220). Re-run `src/evaluate.py`. The q1/q3 R² cells should move from Tier 2 to Tier 1 (paper 0.093 vs our 0.085 = -9% rel_err, paper 0.113 vs our 0.122 = +8% rel_err, both within the 30% tolerance).

### Minor (cleanup)

- [m1] **Stale impact in Assumption 16**: the assumption's Impact line says "Both are reported so the Replicator can choose; no silent switch was made" but the metric shipped is unadjusted R², with adjusted R² sitting in a sibling column. The replicator DID choose (chose unadjusted) but frames it as no-silent-switch. Update the Impact note or move q1_r2_adj into the canonical metric key.
- [m2] **tables_to_replicate.json file location inconsistency**: file is at `inputs/tables_to_replicate.json` but `scripts/score_replication.py` looks for `preparations/tables_to_replicate.json` (which I had to copy for the scorer to run). Either move the file to preparations/ or update the layout helper. This is a layout hygiene issue, not a methodology issue.
- [m3] **`size_quintile.parquet` has 47/15/12/11/10 distribution, not 20/20/20/20/20**: documented in Assumption 14 as an unavoidable consequence of NYSE breakpoints applied to a multi-exchange universe. The carry-along `size_quintile_allstock` diagnostic shows true 20/20/20/20/20. No fix available (paper silent), but the next iteration could note that Q1 a_1 = -0.1362 (close to paper -0.1342) suggests the regression is robust to the size split choice.
- [m4] **`size_s0_spread_jandec` is +0.0282 vs paper +0.0246 (r=1.15)**: a Tier 1 cell (within 25% tolerance), but worth noting the slight upward bias. The replicator documents it as `[CONVENTION-APPLIED]` decile-to-quintile aggregation. No fix needed unless a closer decile series is available.
- [m5] **Table III `s0_p10_posprop_jandec` r=2.57 (paper 0.204, ours 0.524)**: a Tier 2 cell, but at the upper magnitude bound. Replicator documents (Assumption 18) that residual std is lower in this vintage's CRSP, producing less extreme negative tails. Documented as a vintage mismatch in `preparations/assumptions.md:228-253`.
- [m6] **Table IV overlap cells are 30-50% below paper** (`overlap_s0_s1=0.323 vs 0.516`, `overlap_s0_s12=0.151 vs 0.220`, `overlap_s1_s12=0.066 vs 0.128`): signs and ordering match; Spearman correlations Tier 1. The discrepancy is in stock-list composition, not signal ranking. Replicator explains as sample-composition sensitivity (no special fix). Tier 2 cells already.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | S0 P1-P10 alphas monotonically decline in Table II Jan-Dec (P1=+0.0131, P5=+0.0024, P10=-0.0154). Paper expectation: "Portfolios P1 to P5 experience positive abnormal returns, while the abnormal returns on the rest of the portfolios are negative" (paper L657). Verified. |
| 2 | Headline-magnitude claim | ✓ | C1 S0 P1-P10 spread: ours 0.0286 vs paper 0.0249 (+15%, within 20% tolerance). C2 a_1: ours -0.0969 vs paper -0.0923 (+5%, within 15% tolerance). C3 a_12: ours 0.0317 vs paper 0.0339 (-7%, within 15% tolerance). |
| 3 | Sample coverage ≥ 60% | ✓ | Panel 1929-1982 has lag36 non-null 76% (within 60% threshold); all earlier lags > 89%. 1934-1987 panel ~2,339 stocks/month avg (consistent with raw CRSP in the post-1962 period when AMEX/NASDAQ joined). |
| 4 | Data-source choice justified | ✓ | All four primary CRSP tables used (msf, dsf, msenames, msi) plus FF rf. Every substitution documented: FF rf for CRSP rf (Assumption 4, `[CONVENTION-APPLIED]`); NYSE-only size breakpoints (Assumption 14, `[CONVENTION-APPLIED]`); 5 quintile series for Table V (Assumption 20, `[CONVENTION-APPLIED]`). |
| 5 | prep_validation.py exit 0 | ✓ | Ran `uv run python scripts/prep_validation.py <slug>` → all 7 requirements full, 27 rules across 8 categories, scoring.json present, validation passes. |
| 6 | All committed tables have results files | ✓ | 6 tables in tables_to_replicate.json ↔ 6 files in results/ (table_1.md through table_6.md). |
| 7 | SUMMARY.md matches results/table_*.md | n/a | No prior SUMMARY.md; this audit writes the first one. Spot-check of values matches between eval/metrics.json and results/table_*.md (e.g., S0 P1-P10 spread = 0.0286 in both; Q1 a_1 = -0.1362 in both). |
| 8 | No orphan folders | ✓ | Slug root has standard structure: data/, eval/, inputs/, logs/, preparations/, results/, src/. No literal-brace shell-expansion failures. |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md has 21 numbered assumptions, each with Decision / Rationale / Impact. Inner-loop log (logs/log1.md) shows 5 inner iterations with Diagnose → fix → verify → next-step pattern. |
| 10 | Tier 2 within 2× magnitude | ✓/✗ | Tier 2 cells are classified by relative error ≤ 2.0 in evaluate.py (CAP_MAGNITUDE=2.0). However, two Tier 2 cells have |ours/paper| > 2.0: `all_jan_a12` (r=2.72) and `s0_p10_posprop_jandec` (r=2.57). These pass the tolerance-band check (rel_err<2.0) but their raw ratios exceed 2x — a borderline case the rubric notes for band 3 vs band 2 distinction. The replicator's Tier 2 classification is consistent with the evaluator's tolerance-based logic, but the underlying ratios are at the boundary. |
| 11 | Corollary coverage | ✓ | All paper claims (C1-C6) are covered by at least one committed table. The replicator's claim list is complete and matches the paper's headline / robustness claims. |
| 12 | Claim coverage of committed selection | ✓ | All 6 paper claims (C1-C6) have at least one table in `covers_claims`. No fabricated claim. `budget_flag` is present. No SKIPped tables that should be REQUIRED. |
| 13 | Sign conventions re-derived from paper | ✓ | S0 P1-P10 spread = +0.0286 (paper +0.0249, same sign). S1 P1-P10 spread = +0.0265 (paper +0.0199, same sign). S12 P1-P10 spread = +0.0104 (paper +0.0093, same sign). S0 P1 alpha positive (+0.0131, paper +0.0111). S0 P10 alpha negative (-0.0154, paper -0.0138). Spearman correlations all signed correctly. P1-P10 positive-proportion spread = +0.44 (paper +0.796, same sign but lower magnitude — sample sensitivity). No sign flips anywhere in the per-cell table. |
| 14 | Reporting discipline | ✓/✗ | Grid completeness: all committed cells appear in results/table_*.md. Significance categories match (a_1 t=-18.55, paper t=-18.58, both |t|>18 — 1% level). No "reversal" / "exact-match" over-vocabulary. Headline cells (C1, C2) cite t-stats. No SE-less headlines detected. One concern: `s1_p1_alpha_jan` is the single FAIL cell, but it is mentioned in REPORT.md limitations without an SE-style quantification of the gap (the agent calls it "likely sample-period sensitivity" without a t-stat or alternative-vintage comparison — `[m7]` below). |

## 4. Issues the agent should have caught (didn't)

1. **R² reporting discipline**: tables_to_replicate.json describes the R² column as "adjusted R²" (line 41: "Cross-sectional regression estimates (a_0, a_1, a_12, a_24) and adjusted R^2"). The replicator ships unadjusted R² as the headline metric and reports adjusted R² in a sibling column, but the committed `q1_r2` and `q3_r2` targets are unadjusted R² and miss the paper by 55% / 72%. The replicator documented the choice in Assumption 16 but the simpler fix — switch the metric to adjusted R² which is already computed — was available and would have moved 2 cells from Tier 2 to Tier 1.
2. **Stale impact statement**: Assumption 16's Impact section claims "Both are reported so the Replicator can choose; no silent switch was made" but the metric file shipped unadjusted R² as the value, with adjusted R² as the diagnostic. This is precisely the kind of silent switch the assumption denies; the impact line should be updated or the metric should be switched.
3. **Layout inconsistency**: tables_to_replicate.json lives in `inputs/` but `scripts/score_replication.py` reads from `preparations/`. The replicator ran the per-cell evaluator (`src/evaluate.py`) successfully but did not run the canonical scorer, which would have errored out and surfaced this. The auditor ran the canonical scorer (after copying the file to its expected location).
4. **Lack of impact quantification on the single FAIL**: the replicator's REPORT.md and log say the FAIL is "likely sample-period sensitivity" but offers no SE, alternative-vintage spot check, or filtered re-run to support the claim. Per `rep/STUCK_AGENT_GUIDELINE.md`, hedged language without a test result does not retire a FAIL. The next iteration should either fix the underlying convention (Assumption 17: implement footnote 15) or run the alternative-vintage spot check.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Jegadeesh (1990) Evidence of Predictable Behavior of Security Returns" for slug `jegadeesh_1990_evidence_of_predictable_behavior_of_security_returns`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/<slug>/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [M1] — MAJOR — fix after [M2]
`s1_p1_alpha_jan` is the only FAIL cell (paper 0.0085, ours 0.0308, r=3.63). This is a January-only S1 P1 alpha regression. Per paper footnote 15 (L631), January a_jt should be estimated from January-only regressions in the previous 5 years. The replicator's Assumption 17 says it uses the standard 5-year rolling window for all months including January. The gap is large (3.6x), so this is a likely cause.

**Specific fix:**
1. In `src/main.py`, modify the S0/S1 forecast regression path so that for month t in January, the 60-month rolling-window regressions are restricted to January months only (5 January regressions per window).
2. Re-run `src/main.py` for the affected Table II cells (`s1_p1_alpha_jan` and any other January-only cells that may have moved).
3. Verify: `s1_p1_alpha_jan` should drop from 0.0308 toward 0.0085. If r drops below 2.0, the cell moves to Tier 2; if r drops below 1.0, the cell moves to Tier 1. Either is an improvement.
4. Also re-check `s0_p1_alpha_jan` (currently Tier 1 at 0.0244 vs paper 0.0241, r=1.01) — should remain Tier 1 but the convention fix may tighten the estimate.

### [M2] — MAJOR — fix first (cheap)
`q1_r2` and `q3_r2` cells are Tier 2 with unadjusted R² (0.144 vs paper 0.093, 0.194 vs paper 0.113). The adjusted R² values are already computed in `eval/metrics.json` (`q1_r2_adj=0.0847`, `q3_r2_adj=0.1220`) and would be Tier 1 if reported. The committed `tables_to_replicate.json` describes the column as "adjusted R^2" but the metric file ships the unadjusted version.

**Specific fix:**
1. Open `inputs/tables_to_replicate.json` (or `preparations/tables_to_replicate.json` if you've moved it there — see layout note below).
2. For cells `q1_r2`, `q3_r2`, `all_r2`, `all_febdec_r2`, change the value to the paper's reported R² (already there) but make sure the metric in `eval/metrics.json` for `q1_r2`, `q3_r2` is the adjusted R² series.
3. Concretely: modify `src/main.py` so that when writing `q1_r2` and `q3_r2` to `eval/metrics.json`, write the adjusted R² (`q1_r2_adj`, `q3_r2_adj`), not the unadjusted. The "All" rows should remain on unadjusted R² (paper reports 0.108 unadjusted, our 0.1088 is a clean Tier 1 match).
4. Alternatively: add a one-line note in `tables_to_replicate.json` flagging that the Q1/Q3 R² is unadjusted (the document is in fact ambiguous), but the cleaner fix is to ship adjusted R² since that matches the document text and is closer to the paper.
5. Verify: `q1_r2` rel_err should drop from 0.548 to ~0.085 (Tier 1); `q3_r2` rel_err should drop from 0.719 to ~0.078 (Tier 1).

## Layout hygiene (do this first, takes 30 seconds)

`scripts/score_replication.py` reads `tables_to_replicate.json` from `preparations/`, but the file currently lives at `inputs/tables_to_replicate.json`. The per-cell evaluator (`src/evaluate.py`) reads from `inputs/` and works fine; the canonical scorer does not.

**Specific fix:**
1. Either move the file to `preparations/tables_to_replicate.json` (preserving the contents) or update `utils/paths.py` so the scorer reads from `inputs/`.
2. Re-run `uv run python scripts/score_replication.py replications/<slug> --iteration 2` and confirm the per-cell tallies match the per-cell block in `logs/log2.md`.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human. A documented partial is more valuable than a paper-claiming success that does not actually replicate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **No silent switches on committed metrics.** If a metric ships as unadjusted R² while the target spec says adjusted R², either update the spec with a `notes:` justification OR change the metric. Don't claim "both are reported so no silent switch was made" when the file ships only one series.

## Inputs you should read

- `replications/<slug>/logs/audit1.md` — this audit (full context)
- `replications/<slug>/inputs/content.md` — paper ground truth (L631 has the footnote 15 quote; L585 has size-quintile wording)
- `replications/<slug>/preparations/assumptions.md` — Assumptions 16 (R²), 17 (January-only forecast), 18 (positive-proportion), 20 (size-quintile aggregation) are the load-bearing ones
- `replications/<slug>/src/main.py` — current code (will be modified for [M1] and [M2])
- `replications/<slug>/data/` — cached intermediates (recompute spot-checks from these)
- `replications/<slug>/eval/scoring.json` — canonical machine-readable score, includes loss and per-cell flags

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point.
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/<slug>/src/main.py` — revised with fix attempts logged per issue above ([M1] January-only forecast, [M2] adjusted R² for Q1/Q3)
- `replications/<slug>/results/table_<n>.md` — updated for each committed table (one per `tables_to_replicate.json` entry)
- `replications/<slug>/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status). Update Assumption 16's Impact line to reflect the [M2] fix.
- `replications/<slug>/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict and score; do NOT edit (the auditor owns this file)
- `replications/<slug>/REPORT.md` — updated; lead with the data-quality summary (sample period, universe size, signal mean/std vs paper, headline-magnitude comparison, table count, corollaries evaluated this iteration)

## Stop conditions

- **All blockers fixed and verified** → re-run prep_validation.py and any sanity checks → if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is a high-quality replication. The headline claim (C1: S0 P1-P10 spread of 2.49%/month) reproduces at 2.86%/month with the same direction, similar magnitude, and similar t-stat (17.6 vs 16.8). The cross-sectional regression in Table I matches cell-for-cell on the All-sample row, including a_1 = -0.0969 vs paper -0.0923 and a_12 = +0.0317 vs paper +0.0339, with the size-based 3-factor model in Table V reproducing exactly. The single FAIL on `s1_p1_alpha_jan` (r=3.63) drives Signal Strength to band 1 per the rubric, which forces a FAILED bright-line verdict, but the substance of the replication is sound. The Q1/Q3 R² cells are Tier 2 only because of an unadjusted-vs-adjusted R² reporting choice that the agent documented in Assumption 16 but did not implement per its own `tables_to_replicate.json` description.

The replicator's iteration log is exemplary — 5 inner iterations, each with Diagnose → fix → verify → next-step, and a final evaluator tally of 88/89 cells in tolerance. The assumptions.md is the strongest artifact: 21 numbered assumptions with paper citations for every paper-silent decision. The score-replication canonical scorer was not run by the replicator (it would have errored on the layout inconsistency), but the per-cell evaluator at `src/evaluate.py` runs cleanly and matches the log. Both files were verified to disk by the auditor.
