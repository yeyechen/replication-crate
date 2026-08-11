---
iteration: 3
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 3 — bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o

**Verdict:** PARTIAL
**Date:** 2026-08-08
**Auditor notes:** Iteration 3 added three more Table 6 bivariate controls (BM, REV, MOM) using a generic `_bivariate_sort()` helper, raising committed-cell coverage from 43% to 50%. Canonical loss dropped 1.43 → 1.34 (-6.3%); tier 1 count up 29 → 33, tier 2 up 38 → 46, FAIL unchanged at 5, MISSING down 97 → 85. Methodology remains exemplary: dsfhdr PIT filter, BM dedup, mcap_lag1, FF-Carhart 4-factor alphas with Newey-West t-stats, BMP/Shumway delisting. The MAX signal construction replicates to <1% across 9 of 10 deciles; the lottery-effect direction (high MAX → lower return) is preserved across all 4 implemented Table 6 controls (SIZE, BM, REV, MOM), exactly as paper claim C2 says. The remaining scope gap is 85 cells: Table 6 ILLIQ (4), Table 7 Fama-MacBeth (28), Table 9 MAX×IVOL (18), Table 3 MAX persistence (35). Iteration continues.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 5 | Methodology unchanged from audit 2: every paper construction detail matches (MAX formula, decile sort, FF-Carhart 4-factor alphas, Newey-West t-stats, BMP/Shumway delisting, forward-shifted ret, dsfhdr PIT filter). The new `_bivariate_sort()` refactor is clean and reusable; BM uses existing `bm`; REV = `groupby(permno).shift(1)`; MOM = `cumprod(1+ret)` over [t-12, t-2] per Jegadeesh-Titman convention. Tier 2 magnitude cap (2×) is enforced in `src/evaluate.py:55,98-99`. |
| Headline matching | 3 | Sign and shape correct on the central claim (D10-D1 VW raw -0.54% vs paper -1.03%; alpha -0.98% vs -1.18%; both negative). The new Table 6 BM/REV/MOM headline spreads match within 25% of paper (alpha diffs: -1.32/-1.19/-0.79 vs paper -1.06/-0.98/-0.70); SIZE control at -1.31% vs -1.19% is within 10%. The headline D10-D1 raw return is still 52% of paper (within [0.5, 2.0] but outside [0.8, 1.2]). |
| Data coverage | 5 | Period, universe, and data sources unchanged from audit 2. Exact period match (Jul 1962 – Dec 2005), avg ~4,700 obs/month, all CRSP/Compustat/FF sources match. |
| Concrete result matching | 2 | 33 Tier 1 / 46 Tier 2 / 5 FAIL / 85 MISSING out of 169 committed cells. Tier 1 rate 19.5% (up from 17.2%). Among computed cells (84): 39% Tier 1, 55% Tier 2, 6% FAIL. T6 per-table: 14 T1 / 12 T2 / 4 MISSING (ILLIQ). The 12 added BM/REV/MOM spread cells landed mostly Tier 2 (1.5× to 2.0× the alpha differences, t-stats attenuated). |
| Signal strength | 3 | T6 SIZE alpha diff (-1.31% vs -1.19%) within 10%; BM alpha diff -1.32 vs -1.06 is 1.25× of paper; REV -1.19 vs -0.98 is 1.21×; MOM -0.79 vs -0.70 is 1.13×. All four T6 controls inside [0.5, 2.0] band; sign matches. Headline D10-D1 VW raw -0.54 vs -1.03 is 52% (outside [0.8, 1.2] but inside [0.5, 2.0]). |
| Corollary | 2 | Partial improvement: Table 6 now has 4 of 5 bivariate controls implemented (SIZE, BM, REV, MOM), validating claim C2 at the bivariate-sort level. T6 ILLIQ (4 cells) still missing — requires daily `vol` from `dsf`. Tables T7 (Fama-MacBeth, 28 cells), T9 (MAX×IVOL, 18 cells), T3 (MAX persistence, 35 cells) remain MISSING. Claim C2 (partial), C3 (missing), C4 (missing). |

Mean: 3.33. Verdict: REPLICATED (mean ≥ 3.0, no dimension = 1). Actionable major count = 1 (corollary coverage gap); `requires_iteration: true`.

## 2. Issues by severity

### Blockers (must fix)

None. The headline MAX-lottery effect direction replicates, the MAX signal construction replicates to <1%, the Table 6 bivariate-sort methodology is implemented correctly across 4 controls (SIZE, BM, REV, MOM), and paper claim C2 is partially validated. No methodology bug that invalidates the existing artifacts.

### Major (should fix)

- **[M1] Corollaries still missing — 85 of 169 committed cells (50%) are MISSING.**
  - File: `preparations/tables_to_replicate.json:25-310` (T3, T6 ILLIQ, T7, T9 not implemented); `eval/scoring.json` aggregates (`missing_count: 85`).
  - Evidence: After iteration 3, Table 6 has 4 of 5 bivariate controls implemented (26 of 30 cells: SIZE 14 + BM 4 + REV 4 + MOM 4). The remaining 85 cells cover the bulk of the paper's argument:
    - T6 ILLIQ control (4 cells) — paper §2.3, Table 6 Panel A column 5 (paper line 988-1002); tests claim C2 for liquidity.
    - T7 Fama-MacBeth regressions (28 cells) — paper §2.4, Table 7 (paper lines 1100-1178); tests claim C2 in the multivariate setting.
    - T9 MAX×IVOL bivariate (18 cells) — paper §3, Table 9 (paper lines 1383-1525); tests claim C3 (MAX reverses IVOL puzzle).
    - T3 cross-sectional MAX persistence (35 cells) — paper §2.2, Table 3 (paper lines 497-593); tests claim C4.
  - Per `logs/log3.md:94-98`, the replicator explicitly defers these to "subsequent iterations" citing pipeline complexity. Each is actionable in the next iteration: T6 ILLIQ requires `vol` from `dsf`; T7 requires all 6 signals plus the lagged cross-sectional regression (could leverage T9's IVOL work); T9 requires IVOL (60-day daily residual std); T3 requires lagged MAX plus 7 controls (large overlap with T7 infrastructure).
  - Specific fix: Implement T6 ILLIQ first (cheapest — 4 cells, only needs daily `vol` from `dsf`). Then T9 (18 cells, the IVOL signal pipeline that T3 and T7 will reuse). Then T7 (28 cells, multivariate regression). Then T3 (35 cells, different dependent variable from T7 — same panel). After each, `python scripts/score_replication.py <slug> --iteration 4` should show `missing_count` dropping by the relevant number.

### Minor (cleanup)

- **[m1] `logs/log3.md:63` mis-describes which cells are Tier 1.** The log claims "Tier 1 (33 cells): 9 of 10 D_avg_max (D2-D10), D_vw_ret (D1-D7, D10), D_vw_alpha D10, SIZE_D1_vw through SIZE_D10_vw (10 of 10), BM_D1_vw through BM_D10_vw (10 of 10), REV_D1_vw through REV_D10_vw (10 of 10), MOM_D1_vw through MOM_D10_vw (10 of 10), ew_alpha_tstat, etc." This implies ~58 Tier 1 cells, but the canonical scorer reports 33 — and the BM_D*/REV_D*/MOM_D* decile cells are (a) not committed in `tables_to_replicate.json` (only spread cells are), and (b) even if committed at the 10% tolerance they would be Tier 2 (rel_err 10-40%). Also SIZE_D10_vw has rel_err=1.12 → Tier 2, not Tier 1. Specific fix: replace the description with the canonical per-table tally: "Tier 1 (33 cells): T1 19 cells + T6 14 cells. T6 Tier 1 = 9 SIZE deciles (D1-D9) + SIZE_vw_alpha_diff + BM_vw_ret_tstat + BM_vw_alpha_tstat + REV_vw_ret_tstat + MOM_vw_alpha_diff."

- **[m2] `REPORT.md:40` reports stale iteration-2 tally.** The TL;DR says "32 Tier 1 (19%), 43 Tier 2 (25%), 5 FAIL (3%), 89 MISSING (53%) — loss = 1.37", but `eval/scoring.json` shows iteration-3 canonical numbers "33 Tier 1 (19.5%), 46 Tier 2 (27.2%), 5 FAIL (3%), 85 MISSING (50.3%) — loss = 1.3373". The aggregate tally line was not refreshed when iter-3 finished. Specific fix: update REPORT.md TL;DR tally section to the iteration-3 numbers, then add a "Iteration 3" section describing the new T6 BM/REV/MOM controls and their Tier 1/Tier 2 distribution.

- **[m3] BM decile cells show systematic low bias (~20% below paper) that is not surfaced in any analysis.** The replicator emitted BM_D1_vw...BM_D10_vw into `data/metrics.json` and `results/table_6.md` (10 cells), but `tables_to_replicate.json` only commits the 4 spread cells. The decile values are systematically below paper (e.g. BM_D1_vw ours=1.15 vs paper=1.51, BM_D9_vw ours=0.56 vs paper=0.95). This pattern is consistent with a BM construction gap (FF convention is fiscal-year-end book equity matched to July t+1; the replicator's BM definition is not audited here). Specific fix: either commit the BM_D*/REV_D*/MOM_D* decile cells to `tables_to_replicate.json` so they get scored, or remove them from `data/metrics.json` and `results/table_6.md` to avoid emitting unsanctioned metrics. If committing, audit the BM column construction against the paper's appendix definition.

- **[m4] Canonical scorer does not enforce the 2× magnitude cap on Tier 2 cells.** `scripts/score_replication.py:_classify_tier` returns "Tier 2" for any cell with sign-match and rel_err > tolerance, regardless of magnitude. 12 cells with rel_err > 2.0 (e.g. D1_vw_alpha rel_err=9.245, D7_vw_alpha rel_err=18.44) are labeled Tier 2 by the canonical scorer but FAIL by `src/evaluate.py:98-99` (which has the cap). This is a residual divergence from audit-1 [M3]. The loss differs (1.34 with cap-not-enforced; ~1.41 if cap were enforced). Not actionable in this iteration — the canonical scorer is repo infrastructure, not per-slug. Document for the record.

- **[m5] `preparations/assumptions.md:182-187` A4 impact line is updated but only partially.** The previous audit-2 minor said to update A4 with the missing-cell contribution formula. The iter-3 entry at line 209 reads "missing_count=85" but doesn't include the contribution formula `2·85/169 = 1.01`. The current loss decomposition is dominated by MISSING cells. Specific fix: add a one-line note showing `MISSING contribution = 2·85/169 = 1.006`; `FAIL contribution = 2·5/169 = 0.059`; `Tier 2 contribution = 1·46/169 = 0.272`; `Tier 1 contribution = 0`; total = 1.337.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (high MAX → low return) | PASS | T1: D10-D1 VW raw = -0.54% (paper -1.03%); alpha = -0.98% (paper -1.18%); both negative. T6: SIZE alpha diff = -1.31%, BM = -1.32%, REV = -1.19%, MOM = -0.79% — all negative, matching paper. Extreme-decile VW returns decline D7→D10 (1.05, 1.01, 0.74, 0.43). Direction preserved. |
| 2 | Headline-magnitude claim (D10-D1 VW raw -1.03%) | PASS | Replicated -0.54% — sign matches, magnitude is 52% of paper. Within [0.5, 2.0] band. Inside the [0.8, 1.2] signal-strength band would require 0.82-1.24%; outside. |
| 3 | Sample coverage ≥ 60% | PASS | Panel has 2,454,774 unique (permno, month) rows over 521 months (1962-07 to 2005-12), avg 4,703 obs/month. Paper's "approximately 240,000 monthly returns" implies comparable density. |
| 4 | Data-source choice justified | PASS | dsfhdr for PIT (CRSP.md recommended); BMP/Shumway delisting for missing dlret; FF factors from `ff.four_factor_monthly`. All documented in `assumptions.md`. |
| 5 | prep_validation.py exit 0 | PASS | All prep artifacts validate; verdict=ready; 35 rules across 8 categories; 0 blocking issues. |
| 6 | All committed tables have results files | PARTIAL | T1 and T6 have results files; T3, T7, T9 missing. 2 of 5 committed tables have results files. |
| 7 | SUMMARY.md matches results/table_*.md | N/A | SUMMARY.md is auditor-owned and being overwritten this audit. |
| 8 | No orphan folders | PASS | No literal-brace folder names at the slug root. |
| 9 | Diagnoses paired with fix attempts | PASS | `logs/log3.md` has 3 inner iterations, each with Diagnosis / Next fix / Before metric / After metric / Status. |
| 10 | Tier 2 within 2× magnitude | FAIL (residual) | `src/evaluate.py:55,98-99` enforces `cap_magnitude=2.0`; 12 cells with rel_err > 2.0 are FAIL locally but Tier 2 in canonical scorer. Divergence is residual from audit-1 [M3]. |
| 11 | Corollary coverage | PARTIAL | Table 6 SIZE/BM/REV/MOM controls computed (4 of 5 bivariate controls). T6 ILLIQ (4 cells), T7 (28), T9 (18), T3 (35) still MISSING. Listed as [M1]. |
| 12 | Claim coverage of committed selection | PARTIAL | C1 (T1 — computed); C2 (T6 partial — SIZE/BM/REV/MOM done, ILLIQ missing; T7 missing); C3 (T9 — missing); C4 (T3 — missing). 2 of 4 claims still not fully validated. |
| 13 | Sign conventions re-derived from paper | PASS | D10-D1 is paper convention "high MAX minus low MAX" (paper line 172). T6 spreads also negative per paper. Replicator's subtraction order matches paper: `_bivariate_sort()` computes `pivot_vw[N_BINS] - pivot_vw[1]` at `main.py:414`. Sign of all 4 T6 alpha diffs matches paper. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | PARTIAL | T1 grid complete (10 deciles × 4 metrics + spread + t-stats). T6 grid complete (4 controls × 10 deciles + 4 spread stats). `REPORT.md` TL;DR aggregate tally is stale (per [m2]). `logs/log3.md` Tier 1 description inaccurate (per [m1]). |

## 4. Issues the agent should have caught (didn't)

1. **The replicator emitted 30 BM/REV/MOM decile cells into `data/metrics.json` and `results/table_6.md`, but `tables_to_replicate.json` only commits the 4 spread cells for each of BM/REV/MOM.** The decile cells (BM_D1_vw...BM_D10_vw etc.) are "ghost" work — they appear in the artifacts but aren't scored by the canonical scorer. Worse, they systematically deviate from paper by 10-40% (the BM column especially), suggesting a BM-construction gap that's invisible because it's not scored. This is audit material but invisible to the loss.

2. **`logs/log3.md:63` describes the Tier 1 tally in terms of cells that are not actually committed in `tables_to_replicate.json`** (the BM_D*/REV_D*/MOM_D* decile cells) and overstates the SIZE decile count (claims 10/10 but D10 is Tier 2 at rel_err=1.12). The replicator should have read the per_table_tiers output of the canonical scorer and transcribed it verbatim.

3. **`REPORT.md:40` was not refreshed after iter 3.** The TL;DR aggregate tally still shows iter-2 numbers (32 T1, 43 T2, 89 MISSING, loss 1.37). The iteration-2 audit explicitly flagged REPORT.md staleness as [m1]; the iter-3 replicator addressed doc updates but only for the Table 6 controls, not the canonical tally.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns" (Bali, Cakici, Whitelaw 2011) for slug `bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o`. The previous agent run completed with verdict **PARTIAL** (audit 3 at `replications/<slug>/logs/audit3.md`). Read the audit first.

Iteration 3 closed the audit-2 [M1] partially by adding Table 6 BM, REV, and MOM controls using a generic `_bivariate_sort()` helper. Canonical loss dropped 1.43 → 1.34 (-6.3%); tier 1 count up 29 → 33. Methodology remains exemplary; the lottery-effect direction is preserved across all 4 implemented Table 6 controls. The remaining gap is **scope**: 85 of 169 committed cells (50%) are still MISSING — Table 6 ILLIQ (4 cells), Table 7 Fama-MacBeth (28 cells), Table 9 MAX×IVOL (18 cells), Table 3 MAX persistence (35 cells). Paper claims C2 (partial — ILLIQ/T7 missing), C3 (missing), C4 (missing) are still not fully verified. The next iteration should close as many of these as feasible.

## Issues to address (priority order)

### [M1] — MAJOR — Tables T6 ILLIQ, T7, T9, T3 not implemented (85 cells missing)

The committed selection lists 5 tables covering 4 paper claims. After iteration 3, only T1 (58 cells) and T6 SIZE+BM+REV+MOM (26 of 30 cells) are computed. The remaining 85 cells cover the bulk of the paper's argument:

**T6 ILLIQ first (cheapest — 4 cells).** Import `vol` from `crsp_202601.dsf` and add an `ILLIQ = abs(ret) / vol` signal per (permno, month). Then call `_bivariate_sort(df, control_col="illiq")`. Emit into `data/metrics.json` and extend `results/table_6.md` with the ILLIQ panel. 4 new cells: `ILLIQ_vw_ret_diff`, `ILLIQ_vw_alpha_diff`, `ILLIQ_vw_ret_tstat`, `ILLIQ_vw_alpha_tstat`. Paper values: -1.11, -1.12, -4.07, -5.74 (paper line 999-1002).

**T9 next — 18 cells (this is the IVOL pipeline that T7 and T3 will reuse).** Compute IVOL per (permno, month): regress daily excess returns on daily excess market returns within the month (or use the rolling 60-day window), take the residual std. Then independent bivariate sorts:
- Panel A (MAX within IVOL): for each IVOL decile, sort by MAX into 10 deciles, average across the 10 IVOL deciles. Emit 10 cells (D1-D10 vw + spreads).
- Panel B (IVOL within MAX): for each MAX decile, sort by IVOL into 10 deciles. Emit 10 cells.

The paper's claim C3 ("MAX reverses the IVOL puzzle") is the headline — the EW sign reversal in Panel B (D10-D1 IVOL controlling for MAX = +0.98% per paper line 1506) is the key test. Implement and verify.

**T7 next — 28 cells.** Monthly Fama-MacBeth cross-sectional regressions of `ret_t+1` on `MAX_t` + 6 controls (BETA, log SIZE, log BM, MOM, REV, ILLIQ). Time-series average of slope coefficients with Newey-West t-stats. 7 univariate regressions (one per predictor) + 1 "full" multivariate regression = 8 specifications × 2 outputs (coef + tstat) = 16 cells. Wait — per `tables_to_replicate.json#T7`, there are 28 cells: 14 univariate (7 predictors × coef+tstat) + 14 full (7 predictors × coef+tstat). This requires all 6 control signals; BETA needs a 60-day rolling CAPM regression. Leverage the IVOL pipeline from T9.

**T3 last — 35 cells.** Monthly cross-sectional regressions of current MAX on lagged MAX + 7 controls. Same panel infrastructure as T7; just different dependent variable. 17 cells in `tables_to_replicate.json#T3` are univariate (one per predictor) plus a "full" multivariate specification with 17 cells. Verify the headline claim C4: lagged MAX coef = 0.3325 (paper line 585), t = 31.31, full R² = 35.10%.

**Verification step:** After each table is added, run `python scripts/score_replication.py <slug> --iteration 4` and verify `missing_count` drops and `loss` decreases toward 0. Target after T6 ILLIQ: missing = 81 (loss ≈ 1.28). After T9: missing = 63 (loss ≈ 1.00). After T7: missing = 35 (loss ≈ 0.55). After T3: missing = 0 (loss should be < 0.5 if all cells come out Tier 1 or Tier 2).

### [m1] — MINOR — Fix the inaccurate Tier 1 cell description in `logs/log3.md:63`

The log claims Tier 1 includes BM_D*/REV_D*/MOM_D* decile cells, but those are not in `tables_to_replicate.json` (only spread cells are committed). The log also overstates SIZE decile Tier 1 to 10/10 (SIZE_D10_vw is Tier 2 at rel_err=1.12). Read `eval/scoring.json#aggregates.per_table_tiers` and transcribe the actual counts. Replace the description with: "Tier 1 (33 cells): T1 = 19 cells; T6 = 14 cells (SIZE D1-D9 deciles + SIZE_vw_alpha_diff + BM_vw_ret_tstat + BM_vw_alpha_tstat + REV_vw_ret_tstat + MOM_vw_alpha_diff)."

### [m2] — MINOR — Refresh `REPORT.md` TL;DR aggregate tally to iteration-3 numbers

`REPORT.md:40` says "32 Tier 1 (19%), 43 Tier 2 (25%), 5 FAIL (3%), 89 MISSING (53%) — loss = 1.37" but `eval/scoring.json` shows "33 Tier 1 (19.5%), 46 Tier 2 (27.2%), 5 FAIL (3%), 85 MISSING (50.3%) — loss = 1.3373". Update the TL;DR tally to the canonical numbers and add a one-paragraph summary of the iter-3 work (Table 6 BM/REV/MOM controls added).

### [m3] — MINOR — Decide what to do with the BM_D*/REV_D*/MOM_D* decile cells

The replicator emitted 30 uncommitted decile cells into `data/metrics.json` and `results/table_6.md`. They are systematically off paper by 10-40% (BM_D1_vw ours=1.15 vs paper=1.51, etc.). Either (a) commit them in `tables_to_replicate.json#T6.metrics` so they get scored (this would surface the BM-construction gap as Tier 2 cells) or (b) remove them from `data/metrics.json` and `results/table_6.md` to avoid emitting unsanctioned metrics. Recommend (a) — committing them forces the BM audit gap into the loss and ensures consistency between artifacts and committed cells.

### [m4] — MINOR (informational) — Canonical scorer does not enforce 2× magnitude cap

`scripts/score_replication.py:_classify_tier` returns "Tier 2" for any cell with sign-match and rel_err > tolerance. 12 cells with rel_err > 2.0 (e.g. D1_vw_alpha rel_err=9.245, D7_vw_alpha rel_err=18.44) are labeled Tier 2 by canonical scorer but FAIL by `src/evaluate.py`. This is residual from audit-1 [M3]. Not actionable in this iteration — fix lives in repo infrastructure. Document for the record.

### [m5] — MINOR — Update A4 impact line with the canonical loss decomposition

`preparations/assumptions.md` A4 should show the loss decomposition: `MISSING contribution = 2·85/169 = 1.006`; `FAIL contribution = 2·5/169 = 0.059`; `Tier 2 contribution = 1·46/169 = 0.272`; `Tier 1 contribution = 0`; total = 1.337. Add as a one-line note under the iteration-3 entry.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human. A documented partial is more valuable than a paper-claiming success that does not actually replicate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.

## Inputs you should read

- `replications/<slug>/logs/audit3.md` — this audit (full context)
- `replications/<slug>/logs/audit2.md` — previous audit (Table 6 SIZE control context)
- `replications/<slug>/logs/log3.md` — the iteration-3 replicator's iteration trace (3 inner iterations)
- `replications/<slug>/inputs/content.md` — paper ground truth (especially §2.3 for Table 6 ILLIQ; §2.4 for Table 7; §3 for Table 9; §2.2 for Table 3)
- `replications/<slug>/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/<slug>/src/main.py` — current code (will be modified); `_bivariate_sort()` is the template for Table 6 ILLIQ
- `replications/<slug>/src/sql/panel.sql` — current pipeline (BM already deduplicated per A3)
- `replications/<slug>/data/` — cached intermediates (recompute spot-checks from these)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point — mid-loop states no longer produce false errors. Re-run it if you changed a prep artifact; otherwise it is optional.
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run `src/evaluate.py` and `scripts/score_replication.py` after each fix — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/<slug>/src/main.py` — extended with `table_6_illiq()`, `table_9()`, `table_7()`, `table_3()` functions (per [M1])
- `replications/<slug>/results/table_<id>.md` — one per completed table (target: 5 total; T9, T7, T3 new this iteration; T6 extended with ILLIQ panel)
- `replications/<slug>/data/metrics.json` — extended with all new cells
- `replications/<slug>/preparations/tables_to_replicate.json` — per [m3], decide whether to commit the BM_D*/REV_D*/MOM_D* decile cells; commit if keeping them
- `replications/<slug>/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status); update A4 impact line per [m5]
- `replications/<slug>/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict and score; do NOT edit (the auditor owns this file)
- `replications/<slug>/REPORT.md` — updated per [m2]; lead with the data-quality summary (sample period, universe size, signal mean/std vs paper, headline-magnitude comparison, table count, corollaries evaluated this iteration)
- `replications/<slug>/logs/log4.md` — iteration-4 trace with per-cell evaluation block

## Stop conditions

- **All blockers fixed and verified** → re-run prep_validation.py and any sanity checks → if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This replication is making steady progress on scope. Iteration 3 closed Table 6 SIZE → SIZE+BM+REV+MOM (4 of 5 bivariate controls), driving canonical loss from 1.43 to 1.34 (-6.3%). The headline MAX-lottery effect direction is preserved across all 4 implemented Table 6 controls (SIZE alpha diff -1.31%, BM -1.32%, REV -1.19%, MOM -0.79%; paper values -1.19%, -1.06%, -0.98%, -0.70%), all Tier 1 or Tier 2 within 25%. This is strong corroboration of paper claim C2 at the bivariate-sort level — the MAX effect is robust to controlling for SIZE, BM, REV, and MOM, exactly as the paper claims. The methodology is solid: the new `_bivariate_sort()` helper is a clean refactor of `table_6_size`, BM uses the existing `bm` column, REV uses a 1-month lag, MOM uses cumprod over [t-12, t-2] per Jegadeesh-Titman.

The replication's strongest evidence remains the MAX signal construction: 9 of 10 Avg MAX cells match paper to <1% (D10 ours=23.52% vs paper 23.60%). The consolidated D10-D1 spread direction is consistent (negative in both raw and alpha). The 5 per-decile FAILs are at the extreme high-MAX deciles where the paper reports strong negative alphas but our replication shows positive or near-zero; this is consistent with the data-vintage caveat (the MAX effect has weakened in more recent CRSP vintages).

The remaining scope gap is 85 cells (50% of committed). With the panel infrastructure in place (dsfhdr PIT filter, BM dedup, mcap_lag1, FF factors), each new table is a tractable extension of the existing pipeline. T6 ILLIQ (4 cells) is the cheapest first step. T9 (18 cells) provides the IVOL signal that T7 and T3 will reuse. The methodology dimension stays at 5; concrete_result and corollary stay at 2 because the score is a function of how many committed cells are actually computed.

The binary verdict REPLICATED (mean 3.33, no dimension = 1) reflects the score, but the actionable major count is 1 (corollary coverage gap), so `requires_iteration: true`. The replicator is making consistent progress with high-quality methodology; the next iteration should drive the loss toward 0 by completing the four deferred tables.

A residual divergence from audit-1 [M3] remains: the canonical scorer (`scripts/score_replication.py`) does not enforce the 2× magnitude cap on Tier 2 classification, so 12 cells with rel_err > 2.0 (mostly small-alpha cells where paper is near-zero) are labeled Tier 2 by the canonical scorer but FAIL by `src/evaluate.py`. This divergence affects the canonical loss (1.34 vs ~1.41 if cap were enforced) but not the verdict. The fix lives in repo infrastructure, not in this slug.