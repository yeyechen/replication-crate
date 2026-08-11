---
iteration: 1
verdict: FAIL
blocker_count: 1
actionable_major_count: 5
requires_iteration: true
---

# Audit Report 1 — frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto

**Verdict:** FAIL
**Date:** 2026-08-08
**Auditor notes:** 3 of 8 committed tables produced; canonical scorer shows L=2.0 because `data/metrics.json` is missing (BLOCKER). Headline B/P effect (Table 3 Panel C) replicated within Tier 1. Methodology faithfully follows the paper, but data-vintage gaps prevent tight replication of V_f-based cells.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4/5 | EBO Eqs. 3.1-3.3 + Appendix A FROE faithfully implemented; documented deviations (constant r_e=0.12, FY2/Ltg unavailable). |
| Headline matching | 3/5 | Table 3 Panel C (B/P quintile spreads) Tier 1; Table 2 V_f correlation off by -0.16 (FAIL); Table 1 Avg ME off by -38% (FAIL). |
| Data coverage | 3/5 | Period matches (1976-1993), but final panel is 76% of paper's 18,162 firm-years; I/B/E/S FY2/Ltg not available. |
| Concrete result | 2/5 | 56 of 140 cells MISSING (Tables 4, 6, 7, 8, 9 not produced); another 53 FAIL (mostly data-vintage). |
| Signal strength | 3/5 | B/P quintile BHAR spread (the headline) within Tier 1; V_f correlation signal is present but compressed by vintage inflation. |
| Corollary | 2/5 | 5 of 8 tables not produced; PErr construction, predictive regressions, and year-by-year strategy returns (the main corollaries of the paper) cannot be checked. |

## 2. Issues by severity

### Blockers (must fix)

- [B1] `data/metrics.json` is missing. The canonical scorer (`scripts/score_replication.py`) reads this file to map metric names to computed values; without it, every committed cell is scored MISSING, so `eval/scoring.json` records `loss = 2.0` and `missing_count = 140`. The replicator's self-reported `L = 1.65` is from a hand-rolled `src/evaluate.py` that produces a different (and unreliable) tally than the canonical scorer.
  - File: `replications/frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto/data/metrics.json` (missing); cf. `eval/scoring.json` lines 4-8 (warning banner); `eval/loss_trace.json` (one row, all MISSING).
  - Likely cause: pipeline runs did not call the metric-extraction step that writes the canonical JSON artifact.
  - Specific fix: have `src/main.py` emit `data/metrics.json` keyed by metric name (the same names as `preparations/tables_to_replicate.json#tables[].metrics[].name`) with one float per cell. Re-run `scripts/score_replication.py` and confirm `missing_count` drops to whatever the agent's hand tally says (expected ~56 for the 5 unproduced tables) and `loss` matches the agent's self-report.

### Major (should fix)

- [M1] Tables 4, 6, 7, 8, 9 not produced (5 of 8 committed tables MISSING in results). `results/` only contains `table_1.md`, `table_2.md`, `table_3.md`. Per the iteration log, this is because iteration 4's `load_comp_actual_roe_sg` SQL join caused a memory blow-up. The committed cells for these tables (84 cells, including the headline regression coefficients from Tables 6-8 and the year-by-year PErr/V_f/P combined-strategy returns from Table 9) cannot be checked until they exist.
  - Files: `results/table_4.md`, `results/table_6.md`, `results/table_7.md`, `results/table_8.md`, `results/table_9.md` (all missing).
  - Specific fix: per the agent's own diagnosis (REPORT.md § "Next iteration"), add the missing year_t predicate to the cartesian join in `src/sql/comp_actual_roe_and_sg.sql` (the join on `c.gvkey = pk.gvkey` lacks a year filter, producing one row per (gvkey, fyear) per panel row); then re-run `src/main.py` end-to-end. After fix, `results/table_4/6/7/8/9.md` should populate. Note: `compute_table_4` does not exist in `src/main.py` (verified by grep) — needs implementation first, not just re-running.

- [M2] `src/evaluate.py` has a parsing bug that produces unreliable per-cell tier counts for Table 1. The `parse_results_table` function keys metrics by `row_label | col_header` (e.g., `"1976 | avg p/b"`) but the metric names in `tables_to_replicate.json` use `t76_avg_pb` style tokens. The fuzzy-match fallback (token overlap) cannot disambiguate year-specific rows — for example, `t76_avg_pb` ends up with value 844 (Avg ME for 1976) because the highest-overlap match for the `t76_*` prefix falls on whichever column has the most shared tokens (`avg`, `me`) rather than the column actually named in the metric. The evaluator's printed tally (18 Tier 1 / 13 Tier 2 / 53 FAIL / 56 MISSING) is therefore unreliable for Tables 1 and 3.
  - File: `src/evaluate.py:25-68` (the parser), `src/evaluate.py:88-104` (the fuzzy fallback).
  - Specific fix: build the evaluator's metric lookup from a structured JSON (e.g., parse the hand-curated per-cell comparison block in `results/table_1.md` directly, or write the computed values to a JSON during the pipeline run). The canonical scorer is the right vehicle — see [B1].

- [M3] V_f correlation gap is closed by an untested causal story. The agent's claim that "modern I/B/E/S FY1 forecasts are 1.29× current EPS (vs ~1.05× in the 1998 vintage)" is hedged language ("most likely", "consistent with") with no sample comparison demonstrating the magnitude. The paper's Table 2 has `corr(V_f T=2) = 0.81` and the replication gets `0.65` (-0.16); this is the largest single FAIL cell, and it propagates into the V_f/P quintile spreads in Table 3 Panel D (Ret36 spread FAIL -0.226). Without a test, the cause attribution is a hypothesis, not a demonstration (per `audit/SKILL.md` Step 2 item 5).
  - File: `results/table_2.md:48-50`; `assumptions.md` lines 614-620.
  - Specific fix: run the cheap test the cause implies — compute `FY1 / current_EPS` for a 1976-1993 firm-year subsample in the current I/B/E/S vintage and report the median (and the equivalent median for a 1998-vintage IBES extract, if accessible). Document the comparison in `assumptions.md`. If the inflation is smaller than expected (e.g., < 1.10×), reopen the FAIL and look for an actual methodology bug (e.g., the Appendix A FROE_{t+1} sequence).

- [M4] Avg ME gap on Table 1 (-38%) is closed by the same untested causal story. The replication gets `Avg ME = 726` vs paper's `1167`. The agent attributes this to I/B/E/S data-vintage "bias toward smaller firms" but cites no test (e.g., comparison of CRSP-only universe mean ME for the same years, or a year-by-year ME decomposition). This is a load-bearing headline cell for the sample-construction claim of the paper.
  - File: `results/table_1.md:58-59`; `REPORT.md:37` (Avg ME row).
  - Specific fix: decompose the gap. (a) Recompute Avg ME on the 21,707-row pre-dedup panel; (b) compare to the paper's per-year ME values to see whether the gap is concentrated in early years (1976-1985) or late years; (c) cross-check that the panel's CRSP-only ME distribution matches the paper's universe ME distribution. Document the result in `assumptions.md`.

- [M5] FY1 / FY2 fpi convention is internally inconsistent across the assumption registry. `assumption 27` (lines 487-491) says FY1 = `fpi='2'` with `fpedats in year_t+1`; `assumption 29` (lines 581-583) says FY1 = `fpi='1'` (current FY, `fpedats in statpers_year`). The results file `results/table_1.md:14` uses `fpi='2'`, matching assumption 27. This contradiction should be reconciled — either the panel was built with `fpi='2'` and assumption 29 is stale, or vice versa.
  - Files: `assumptions.md` A27 vs A29; `results/table_1.md:14`.
  - Specific fix: pick one. Per `rep/IBES.md`, `fpi='1'` is current FY and `fpi='2'` is next FY; "FY1 (one-year-ahead)" in the paper corresponds to `fpi='2'` with `fpedats_year = statpers_year + 1 = year_t+1`. Drop the stale paragraph from assumption 29 and cite the convention.

### Minor (cleanup)

- [m1] `REPORT.md:55` and the agent's log claim Table 4's methodology is implemented in `src/main.py` as `compute_table_4`-equivalent. A grep of `src/main.py` finds no Table 4 implementation (only `compute_table_6/7/8/9`). The claim is a documentation error; remove it from REPORT.md and add Table 4 to the implementation list in the next iteration's plan.

- [m2] Stale impact statement in `assumptions.md` A26 (lines 442-475). The 42,937 firm-year count was the iteration-1 state; after iteration 2 added IBES coverage the count is 21,707 (per `assumptions.md` A27) and after iteration 3's dedup it is 13,787. A26's "Impact" still cites the 42,937 number without a dated correction note.

- [m3] `results/table_3.md` Panel D `V_f/P` Q5 mean of 2.396 is much higher than Q1 mean of 0.485 (paper has 1.54 vs 0.40), consistent with V_f inflation. The 1.911 Q5-Q1 spread is far wider than the paper's 1.14, but the resulting `Ret36` quintile spread is only 0.080 vs paper's 0.306 — i.e., the inflated V_f/P sorts firms randomly rather than by fundamental value. This pattern (wide V_f/P sort, narrow return spread) is the structural signature of the data-vintage issue [M3] and should be highlighted in REPORT.md, not buried in the Notes section.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (B/P quintile BHAR spread) | ✓ | Table 3 Panel C: Ret12 diff +0.034 (paper +0.049, Tier 1); Ret24 diff +0.098 (paper +0.082, Tier 1); Ret36 diff +0.179 (paper +0.151, Tier 1). The Q5-Q1 spread is positive in all three horizons, matching the paper's directional claim. |
| 2 | Headline-magnitude claim (Table 1 all-years row) | ✗ | Avg ME 726 vs paper 1167 (-38%, FAIL). All other cells within tolerance (k -13%, ROE -12%, B -19%, P/B +3%, ROA -12%). Avg ME is the only FAIL. |
| 3 | Sample coverage >= 60% | ✓ | 13,787 / 18,162 = 76%. Documented as data-vintage coverage. |
| 4 | Data-source choice justified | ✓ | All 4 substitutions documented in `data_verification.json` and `assumptions.md` (FF 48-industry, Ltg fallback, FY1-only). |
| 5 | prep_validation.py exit 0 | ✓ | Validation passes; loss_function.json absent (informational); scoring.json present. |
| 6 | All committed tables have results files | ✗ | 5 of 8 committed tables missing results files (Tables 4, 6, 7, 8, 9). |
| 7 | SUMMARY.md matches results/table_*.md | n/a | No existing SUMMARY.md (first audit); will write one. |
| 8 | No orphan folders | ✓ | No literal-brace or shell-expansion-failure folders in the slug root. |
| 9 | Diagnoses paired with fix attempts | ✓ | log1.md shows 3 inner iterations each with diagnosis + next fix + before/after metric. Iteration 4 (Tables 4-9) lacks a "next fix" entry because the run was killed. |
| 10 | Tier 2 within 2x magnitude | ✓ (in REPORT.md's hand-curated blocks) | The agent's per-cell comparison blocks (manually maintained, not the evaluator output) assign Tier 1 / Tier 2 within tolerance. The evaluator's parser is broken (see [M2]) so its printed tally is unreliable, but the hand-curated blocks in `results/table_1.md`, `table_2.md`, `table_3.md` are consistent with the paper's bounds. |
| 11 | Corollary coverage | ✗ | The paper's headline corollary is "PErr has incremental predictive power beyond V_f/P" (Table 8 Panel B M6, Table 9 Panel D combined strategy). Neither Table 8 nor Table 9 was produced; corollary not evaluable. Subsample stability is also not addressed (the paper does not split, so this is N/A). |
| 12 | Claim coverage of committed selection | ✓ | `paper_claims` (C1-C4) are mapped to tables; C1 → Table 2 + 3, C2 → Table 4 + 8, C3 → Table 6 + 7, C4 → Table 8 + 9. Claim-to-table mapping is complete in `tables_to_replicate.json`. |
| 13 | Sign conventions re-derived from paper | ✓ | All signed cells (Ret12/24/36 spreads, V_f correlations, regression coefficients) match the paper's directional claims. No sign flips or absolute-value comparisons found. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | ✗ | Panel A "Q5-Q1 Diff" rows in `results/table_3.md` have 5 FAIL cells for Ret12/24/36 spreads (paper shows monotonic small-cap effect, replication shows noise). The agent's per-cell block labels these FAIL but does not cite a t-stat or SE — only the mean differences. Per Spot-check 14 (b), this is a reporting-discipline issue. |

## 4. Issues the agent should have caught (didn't)

1. The agent's own `src/evaluate.py` returns wildly inconsistent per-cell tier counts depending on row-label parsing. Running it produces e.g. `t76_avg_pb -> 844` (the Avg ME value for 1976), not the actual P/B value. This was visible the moment the agent ran the evaluator; instead of fixing the parser, the agent reported the hand-curated per-cell comparison blocks in `results/table_*.md` without flagging the discrepancy with the evaluator output.

2. The agent diagnosed the iteration-4 memory blow-up as "likely a Cartesian join on `c.gvkey = pk.gvkey` without the year_t predicate" but did not grep `src/sql/comp_actual_roe_and_sg.sql` to confirm the absence of the year predicate. A 5-second grep would have shown the join lacks `c.fyear = pk.year_t + offset`, confirming the diagnosis and giving the next iteration a one-line fix.

3. The agent's claim "V_f correlation lags paper by 0.16 due to data vintage" cites no test (e.g., comparing the median FY1 / current_EPS ratio in the panel to the paper's implied vintage). This is a hedged causal attribution, exactly the failure mode `audit/SKILL.md` Step 2 item 5 flags.

4. `REPORT.md:55` claims Table 4's methodology is in `src/main.py` as `compute_table_4`-equivalent. A grep shows no such function exists. The claim is a documentation error.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Frankel & Lee (1998) — Accounting valuation, market expectation, and cross-sectional stock returns" for slug `frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto`. The previous agent run completed with verdict **FAIL** (audit 1 at `replications/frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [B1] — BLOCKER — fix first
`data/metrics.json` is missing, so `scripts/score_replication.py` scores every committed cell as MISSING (loss = 2.0, missing_count = 140). The agent's self-reported `L = 1.65` comes from a hand-rolled `src/evaluate.py` whose parser is also broken (see [M2]). The canonical scorer is the only writer of `eval/scoring.json`, so the BBF-audit loophole (DEV-018/019) stays open until metrics.json exists.

**Specific fix:**
1. In `src/main.py`, after each `compute_table_N(...)` call, emit a flat dict `{metric_name: value}` covering every metric in `preparations/tables_to_replicate.json#tables[N].metrics[]`. The dict keys MUST match the metric `name` strings exactly.
2. Merge into a single `metrics: {<name>: <value>}` and write to `LAYOUT.data_path("metrics.json")` before `main()` exits.
3. Run `python scripts/score_replication.py replications/<slug> --iteration 2` and confirm `eval/scoring.json` `missing_count` drops to roughly the count of cells in unproduced tables (expected: ~56 for Tables 4, 6, 7, 8, 9 if those remain unproduced). The `loss` field should be in the 1.5-2.0 range and the `tier1_count` should be > 0.

### [M1] — MAJOR — fix after [B1]
Tables 4, 6, 7, 8, 9 are not produced (5 of 8 committed tables MISSING in `results/`). The iteration-4 memory blow-up was a Cartesian join in `src/sql/comp_actual_roe_and_sg.sql` (the join `c.gvkey = pk.gvkey` lacks a year filter).

**Specific fix:**
1. Open `src/sql/comp_actual_roe_and_sg.sql` and confirm the join is `c.gvkey = pk.gvkey` without a `fyear` predicate. The panel needs `comp` rows for `fyear in [year_t-6, year_t+1]` for each `year_t`; the current `WHERE c.fyear BETWEEN 1970 AND 1994` pulls ALL comp rows for the universe's gvkeys, then the join explodes the row count by `~25 ×` per panel row.
2. Restructure the query: pull comp rows for the EXACT (gvkey, fyear) pairs the panel needs, not for all years. Either (a) push the year predicate into the join (`ON c.gvkey = pk.gvkey AND c.fyear BETWEEN pk.year_t - 6 AND pk.year_t + 1`), or (b) generate a `(gvkey, fyear)` lookup from the panel and join on `(gvkey, fyear)` directly.
3. `compute_table_4` does not exist in `src/main.py` (verified by grep). Implement it before re-running: it needs bi-dimensional quintile sorts on (V_f/P × in-sample ME) for Panel A and (V_f/P × B/P) for Panel B, using the same `compute_table_3_panel` skeleton extended to two sort columns.
4. Re-run `src/main.py` end-to-end and confirm `results/table_4.md`, `table_6.md`, `table_7.md`, `table_8.md`, `table_9.md` are produced.

### [M2] — MAJOR — fix after [M1]
`src/evaluate.py` parser is broken (fuzzy-token match cannot disambiguate year rows). Once [B1] is fixed, the canonical scorer replaces `evaluate.py` and this becomes moot, but until then the printed tally is misleading.

**Specific fix:**
1. Either delete `src/evaluate.py` (the canonical scorer is the single source of truth per SKILL.md) or rewrite it to read `data/metrics.json` directly (which [B1] creates) and call `scripts/score_replication.py`'s tier-classification logic. The fuzzy-token parsing at `src/evaluate.py:88-104` should be removed.
2. The per-cell comparison blocks in `results/table_1.md`, `table_2.md`, `table_3.md` are hand-curated and consistent — keep those. The evaluator's printed output is what is wrong.

### [M3] — MAJOR — fix after [M1]
V_f correlation gap (-0.16) is closed by an untested causal story. Hedged language ("most likely", "consistent with") without a sample comparison is not evidence (per `audit/SKILL.md` Step 2 item 5).

**Specific fix:**
1. Compute `FY1_eps / current_EPS` for each panel firm-year and report the median (and p25/p75) per `year_t`. If the median in 1985-1993 is ~1.29× as the agent claims, the diagnosis is supported; if it is closer to 1.05×, reopen the V_f FAIL and audit the Appendix A FROE_{t+1} computation.
2. If I/B/E/S Detail History (the 1998 vintage) is accessible, repeat on that vintage for a 5-year overlap window. Even a partial comparison (e.g., 1985 only) demonstrates the magnitude.
3. Document the test result in `preparations/assumptions.md` with the data and a date stamp. If the test confirms the inflation, leave the FAIL as `actionable: false` (non-actionable data-vintage limitation). If the test contradicts the inflation, the FAIL is actionable and the methodology needs another pass.

### [M4] — MAJOR — fix after [M3]
Avg ME gap (-38%) on Table 1 has the same untested-causal-story pattern as [M3].

**Specific fix:**
1. Compute Avg ME on the 21,707-row pre-dedup panel and on the 13,787-row post-dedup panel; report both.
2. Year-by-year decomposition: list Avg ME for each year_t on the pre-dedup panel and on the post-dedup panel. The gap should concentrate in years where IBES coverage is widest (1985+) if the data-vintage story is correct.
3. Cross-check with a CRSP-only panel (no IBES filter) — if the CRSP-only panel's Avg ME is closer to the paper's 1167 than the IBES-restricted panel, the IBES filter is selecting a smaller-firm subset, supporting the diagnosis.

### [M5] — MAJOR — fix after [M4]
FY1 / FY2 fpi convention is internally inconsistent (`assumption 27` says `fpi='2'`, `assumption 29` says `fpi='1'`). `results/table_1.md:14` uses `fpi='2'`, matching A27.

**Specific fix:**
1. Confirm which fpi convention was actually used in `src/sql/ibes_fy1_fy2_ltg.sql`.
2. Update `assumptions.md` A29 to match the convention that was implemented (delete the contradictory paragraph).
3. Cite `references/IBES.md` for the fpi convention.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `preparations/assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **Don't retire a FAIL with an untested causal story.** Hedged language ("most likely", "probably", "consistent with") is a hypothesis, not a demonstration. Run the cheap test or reopen the FAIL.

## Inputs you should read

- `replications/<slug>/logs/audit1.md` — this audit (full context)
- `replications/<slug>/inputs/content.md` — paper ground truth
- `replications/<slug>/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/<slug>/src/main.py` — current code (will be modified)
- `replications/<slug>/src/sql/comp_actual_roe_and_sg.sql` — the SQL that needs the year predicate fix
- `replications/<slug>/data/panel.parquet`, `panel_with_v.parquet`, `bhar_returns.parquet` — cached intermediates (recompute spot-checks from these)
- `replications/<slug>/results/table_1.md`, `table_2.md`, `table_3.md` — committed table outputs (hand-curated per-cell comparison blocks)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point. Re-run it if you changed a prep artifact; otherwise optional.
- Skip re-doing the ClickHouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/<slug>/src/main.py` — revised with [B1] (write metrics.json), [M1] (Table 4 implementation + year predicate fix), [M5] (reconcile A27/A29)
- `replications/<slug>/results/table_4.md`, `table_6.md`, `table_7.md`, `table_8.md`, `table_9.md` — produced end-to-end
- `replications/<slug>/data/metrics.json` — emitted by [B1] fix
- `replications/<slug>/preparations/assumptions.md` — append iteration log entries for [B1] through [M5] with the test results for [M3] and [M4]
- `replications/<slug>/eval/scoring.json` — overwritten by `scripts/score_replication.py`; verify `missing_count` and `loss` drop
- `replications/<slug>/REPORT.md` — updated; lead with the data-quality summary, the metric-test results from [M3] and [M4], and the Tier counts from `eval/scoring.json` (not from `src/evaluate.py`)
- `replications/<slug>/SUMMARY.md` — read-only (auditor owns this file)

## Stop conditions

- **All blockers fixed and verified** → re-run `scripts/prep_validation.py` and `scripts/score_replication.py` → if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes

The replicator's iteration log is exemplary on inner iterations 1-3 (each has diagnosis + next fix + before/after metric), but iteration 4 (the Tables 4-9 attempt) is missing — the run was killed by the orchestrator before a diagnosis could be written. The methodology that *was* run (EBO Eqs. 3.1-3.3 + Appendix A FROE, June-end quintile sorts, BHAR construction, dedup logic) faithfully follows the paper, and the headline B/P effect (Table 3 Panel C) replicates within Tier 1. The two structural issues are (a) the data-vintage inflation of FY1 forecasts that compresses V_f's correlation with price, and (b) the iteration-4 SQL memory blow-up that blocked 5 of 8 committed tables. Both are documented but neither is closed by a test (per `audit/SKILL.md` Step 2 item 5, hedged causal attribution is a hypothesis, not a demonstration). The missing `data/metrics.json` is a separate, independent blocker that the replicator must close before the canonical scorer can verify any result. The agent's `src/evaluate.py` parser bug should be retired in favor of the canonical scorer.
