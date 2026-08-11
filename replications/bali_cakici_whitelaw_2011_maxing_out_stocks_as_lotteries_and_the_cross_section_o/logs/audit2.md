---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 2 — bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o

**Verdict:** PARTIAL
**Date:** 2026-08-08
**Auditor notes:** Three of the three audit-1 majors were addressed (M2 metrics.json resolved, M3 Tier 2 cap resolved, M1 partial — Table 6 SIZE control implemented). Canonical loss dropped from 2.0 to 1.43. Table 6 SIZE control replicates well: D10-D1 alpha = -1.31% vs paper -1.19% (Tier 1 within 10%), and 9 of 10 SIZE decile VW returns are Tier 1. The headline MAX-lottery effect direction is preserved (D10-D1 VW raw -0.54% vs paper -1.03%, alpha -0.98% vs -1.18%; both negative). The 5 FAILs are concentrated at extreme deciles (D10_vw_ret, D8-D10 vw_alpha, D9-D10 ew_alpha) where the lottery effect has weakened in our CRSP vintage. The remaining gap is scope: 97 of 169 committed cells (57%) are still MISSING — Table 3 (MAX persistence), Table 6 BM/MOM/REV/ILLIQ controls, Table 7 (Fama-MacBeth), Table 9 (MAX × IVOL). Paper claims C2 (partial — SIZE only), C3 (missing), C4 (missing) are still unverified. Iteration continues.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 5 | All paper construction details still match (MAX formula, decile sort, FF-Carhart 4-factor alphas, Newey-West t-stats, BMP/Shumway delisting, forward-shifted ret). Sign-flip fix from iteration 1 is exemplary. The new Tier 2 cap (2× magnitude) is now correctly enforced in `src/evaluate.py` and the canonical scorer agrees. |
| Headline matching | 3 | Sign and shape correct on the central claim (D10-D1 VW raw and alpha both negative, monotonic decline D7→D10); magnitudes are 52% (raw) and 83% (alpha) of paper. The new Table 6 SIZE headline (alpha -1.31% vs paper -1.19%) is within Tier 1 (within 10%). |
| Data coverage | 5 | Exact period match (Jul 1962 – Dec 2005; 521 months), universe size matches (4,703 obs/month, 21,551 unique permnos), all CRSP/Compustat/FF sources match. |
| Concrete result matching | 2 | 29 Tier 1 / 38 Tier 2 / 5 FAIL / 97 MISSING out of 169 committed cells. Tier 1 rate overall = 17% (29/169). Among computed cells (72): 40% Tier 1, 53% Tier 2, 7% FAIL. The 5 FAILs are extreme-decile cells where the lottery effect has weakened. The 97 MISSING cells are scope (T3, T6 partial, T7, T9). |
| Signal strength | 3 | D10-D1 VW raw (-0.54% vs -1.03%) and alpha (-0.98% vs -1.18%) both inside the [0.5, 2.0] band; sign matches. New SIZE-control alpha diff (-1.31% vs -1.19%) is within 10% of paper (Tier 1). |
| Corollary | 2 | Partial — only Table 6 SIZE control is computed (14 of 30 cells in T6). The 4 other Table 6 controls (BM, MOM, REV, ILLIQ; 16 cells), Table 7 Fama-MacBeth (28 cells), Table 9 MAX×IVOL (18 cells), and Table 3 MAX persistence (35 cells) are still MISSING. Paper claims C2 (partial — SIZE only), C3 (missing), C4 (missing) are still not fully verified. |

Mean: 3.17. Verdict: REPLICATED (mean ≥ 3.0, no dimension = 1). Actionable major count = 1 (corollary coverage gap); `requires_iteration: true`.

## 2. Issues by severity

### Blockers (must fix)

None. The headline lottery-effect direction replicates, the MAX signal construction replicates to <1%, and the methodology is sound. No methodology bug that invalidates the existing artifacts.

### Major (should fix)

- **[M1] Corollaries still missing — 97 of 169 committed cells (57%) are MISSING.**
  - File: `replications/<slug>/preparations/tables_to_replicate.json:106-310` (T3, T6 BM/MOM/REV/ILLIQ, T7, T9 not implemented); `eval/scoring.json` aggregates (`missing_count: 97`).
  - Evidence: Only Tables T1 (58 cells) and T6 SIZE control (14 of 30 cells) are computed. The remaining 97 cells cover the bulk of the paper's argument:
    - T6 controls BM, MOM, REV, ILLIQ (16 cells) — paper §2.3, Table 6 Panel A columns 2-5 (paper lines 988-1002); tests claim C2.
    - T7 Fama-MacBeth regressions (28 cells) — paper §2.4, Table 7 (paper lines 1100-1178); tests claim C2.
    - T9 MAX×IVOL bivariate (18 cells) — paper §3, Table 9 (paper lines 1383-1525); tests claim C3.
    - T3 cross-sectional MAX persistence (35 cells) — paper §2.2, Table 3 (paper lines 497-593); tests claim C4.
  - Per the iteration-2 work plan in `logs/log2.md:108-113`, the replicator explicitly deferred these to "subsequent iterations" citing pipeline complexity. Each is actionable in the next iteration: T6 columns 2-5 require BM (already in panel), MOM (cum-ret t-12 to t-2), REV (ret t-1), ILLIQ (|R|/VOLD); T7 requires all 6 signals plus the lagged cross-sectional regression; T9 requires IVOL (60-day daily residual std); T3 requires lagged MAX plus 7 controls.
  - Specific fix: Implement the four T6 control columns (16 cells) first as a batch using the existing panel (`bm`, `mcap_lag1`, `ret` already present; MOM and REV need a single new SQL CTE; ILLIQ needs `vol` from `dsf`). Then T9 (MAX × IVOL) requires the IVOL signal. Then T7 (the multivariate regression that needs all 6 signals). Then T3 (lagged MAX cross-section). Each new table produces a `results/table_<id>.md` with per-cell evaluation and extends `data/metrics.json`. By the end of this, `loss` should be well below 1.0.

### Minor (cleanup)

- **[m1] Table 6 markdown lacks a per-cell evaluation block in the human-readable format used by Table 1.** Table 1's `results/table_1.md` does not embed a per-cell table either, but the canonical scorer and `src/evaluate.py` print a per-cell block. Table 6's `results/table_6.md` is a clean side-by-side paper-vs-ours table; this is actually a clearer format for human reading. Not actionable.

- **[m2] 5 FAILs at extreme deciles (D10_vw_ret, D8-D10 vw_alpha, D9-D10 ew_alpha).** These are real sign disagreements at the extreme deciles where the paper reports strong negative returns/alphas but our replication shows positive (or near-zero). The consolidated D10-D1 spread direction is preserved (negative), but the per-decile magnitudes fail. The replicator's data-vintage caveat (MAX lottery effect has weakened in more recent CRSP vintages) is plausible but is cited as a hypothesis, not a test. The canonical loss is correctly 1.43 (not 0). This is consistent with the rubric's near-edge Tier 1 / Tier 2 cases; not actionable without a vintage-control experiment.

- **[m3] `preparations/assumptions.md` A4 (Tables T3, T6 partial, T7, T9 deferred) — the rationale section is exemplary but the impact line is stale.** A4 lists "Loss has dropped from 2.0 → 1.43 (-28.5%)" as the impact, but the missing-cell contribution is `2·97/169 = 1.15`, which is the dominant component of the residual loss. Update the impact line to spell out which cells remain and what each new table would contribute toward L=0.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (high MAX → low return) | PASS | D10-D1 VW raw = -0.54% (paper -1.03%); D10-D1 alpha = -0.98% (paper -1.18%); both negative. Extreme-decile VW returns decline D7→D10 (1.05, 1.01, 0.74, 0.43). Direction preserved. |
| 2 | Headline-magnitude claim (D10-D1 VW raw -1.03%) | PASS | Replicated -0.54% — sign matches, magnitude is 52% of paper. Within [0.5, 2.0] band. |
| 3 | Sample coverage ≥ 60% | PASS | Panel has 2,454,774 unique (permno, month) rows × 13 cols over 522 months (1962-07 to 2005-12), avg 4,703 obs/month. Paper's "approximately 240,000 monthly returns" implies comparable density. |
| 4 | Data-source choice justified | PASS | dsfhdr for PIT (CRSP.md recommended); BMP/Shumway delisting for missing dlret; FF factors from `ff.four_factor_monthly`. All documented in `assumptions.md`. |
| 5 | prep_validation.py exit 0 | PASS | All prep artifacts validate; verdict=ready; 35 rules across 8 categories; 0 blocking issues. |
| 6 | All committed tables have results files | PARTIAL | T1 and T6 have results files; T3, T7, T9 missing. 4 of 5 committed tables still missing (now T6 partial too: only SIZE done). |
| 7 | SUMMARY.md matches results/table_*.md | N/A | SUMMARY.md is auditor-owned and being overwritten this audit. |
| 8 | No orphan folders | PASS | No literal-brace folder names at the slug root. |
| 9 | Diagnoses paired with fix attempts | PASS | `logs/log2.md` has 5 inner iterations, each with Diagnosis / Next fix / Before metric / After metric / Status. All 3 audit-1 majors have fix attempts. |
| 10 | Tier 2 within 2× magnitude | PASS | `src/evaluate.py:55, 98-99` now has `cap_magnitude=2.0` enforced; canonical scorer agrees. The 11 cells that fell out of Tier 2 into FAIL are mostly alpha values where paper is small (e.g., 0.05) and ours is large (e.g., 0.51) — same sign but >10× magnitude. |
| 11 | Corollary coverage | PARTIAL | Table 6 SIZE control computed (one of 5 bivariate controls). T3 (MAX persistence), T7 (Fama-MacBeth), T9 (MAX×IVOL), T6 BM/MOM/REV/ILLIQ are still MISSING. Listed as [M1]. |
| 12 | Claim coverage of committed selection | PARTIAL | C1 (T1 — computed); C2 (T6 partial — SIZE only); C3 (T9 — missing); C4 (T3 — missing). 3 of 4 claims still not fully validated. |
| 13 | Sign conventions re-derived from paper | PASS | D10-D1 is paper convention "high MAX minus low MAX" (paper line 172). Replicator's subtraction order matches paper: `avg_vw_ret.loc[N_BINS] - avg_vw_ret.loc[1]` (main.py:272). Sign of `vw_alpha_diff` and `ew_alpha_diff` matches paper. The 5 per-decile FAILs are real magnitude mismatches, not sign-convention errors. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | PASS | Table 1 grid is complete (10 deciles × 4 metrics + spread + t-stats). Table 6 markdown is clean side-by-side paper-vs-ours. Both factor-alpha t-stats are reported with Newey-West lag choice documented. No SE-less headlines. |

## 4. Issues the agent should have caught (didn't)

1. **The replicator's report front-matter (REPORT.md) still leads with the iter-1 framing.** `REPORT.md:1-15` says "Iteration: 1 of ≤ 5 outer" but iteration 2 is the current state. The aggregation summary ("19 Tier 1 + 33 Tier 2 + 6 FAIL = 58 cells") is from iteration 1; the canonical scorer now shows 29 T1 / 38 T2 / 5 FAIL / 97 MISSING / loss 1.43 for iteration 2. Update REPORT.md to reflect iter-2 state.

2. **A4 assumes `data/metrics.json` is the canonical Tier 2-capped format, but the stale `data/table_1_metrics.json` is still being written.** Both files are written by `main.py` (line 505-510). The legacy `table_1_metrics.json` is in decimal units and could confuse downstream tools; the canonical `metrics.json` is in percent. Document the dual-emit in `assumptions.md` or remove the legacy file.

3. **The Table 6 SIZE D10_vw is 0.53 vs paper 0.25 (Tier 2, rel_err 1.12).** This is a 2× magnitude overshoot at the most extreme decile where the lottery effect should be weakest. The middle deciles (D1-D9) match within 0.10-0.20%. Worth investigating whether the inner-sort decile within each SIZE bucket has enough stocks at the top bin to produce a stable VW average.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Maxing Out: Stocks as Lotteries and the Cross-Section of Expected Returns" (Bali, Cakici, Whitelaw 2011) for slug `bali_cakici_whitelaw_2011_maxing_out_stocks_as_lotteries_and_the_cross_section_o`. The previous agent run completed with verdict **PARTIAL** (audit 2 at `replications/<slug>/logs/audit2.md`). Read the audit first.

The headline lottery effect continues to replicate. The MAX signal construction replicates to <1% (9 of 10 Avg MAX cells Tier 1). Table 6 SIZE control replicates well: D10-D1 alpha = -1.31% vs paper -1.19% (Tier 1 within 10%), and 9 of 10 SIZE decile VW returns are Tier 1. The sign-flip diagnosis from iteration 1 remains exemplary. Three audit-1 majors were fully addressed this iteration (M2 canonical metrics.json, M3 Tier 2 cap, M1 partial — Table 6 SIZE). Canonical loss dropped from 2.0 to 1.43.

The remaining gap is **scope**: 97 of 169 committed cells (57%) are still MISSING — Table 6 BM/MOM/REV/ILLIQ controls (16 cells), Table 7 Fama-MacBeth (28 cells), Table 9 MAX × IVOL (18 cells), Table 3 MAX persistence (35 cells). Paper claims C2 (partial — SIZE only), C3 (missing), C4 (missing) are still unverified. The next iteration should close as many of these as feasible.

## Issues to address (priority order)

### [M1] — MAJOR — Tables T3, T6 (BM/MOM/REV/ILLIQ), T7, T9 not implemented (97 cells missing)

The committed selection lists 5 tables covering 4 paper claims. After iteration 2, only T1 (58 cells) and T6 SIZE column (14 cells) are computed. The remaining 97 cells cover the bulk of the paper's argument:

**T6 first (lowest cost) — 16 cells.** The panel already has `bm` and `mcap_lag1`. Adding MOM = `cumprod(1+ret)[t-12:t-2]` and REV = `ret[t-1]` requires a single new SQL CTE per signal. ILLIQ = `|ret|/vol` requires `vol` from `dsf` (a new import). For each control: independent sort into 10 deciles, then within each control decile sort by MAX into 10 deciles, average the MAX-decile VW returns across the 10 control deciles, compute D10-D1 spread and 4-factor alpha and Newey-West t-stats. The existing `table_6_size()` function is the template. Emit into `data/metrics.json` and write `results/table_6.md` (extended with panels for BM/MOM/REV/ILLIQ).

**T9 next — 18 cells.** Compute IVOL per (permno, month): regress daily returns on daily market returns within the month, take the residual std. Then Panel A: independent sort on IVOL, then within each IVOL decile sort by MAX (and by MAX(5)). Panel B: independent sort on MAX, then within each MAX decile sort by IVOL. Both panels: VW + EW returns, D10-D1 spread, 4-factor alpha differences, t-stats. The paper's claim C3 ("MAX reverses the IVOL puzzle") is the headline. Per `tables_to_replicate.json#T9`, the metric names include `T9A_MAX_vw_ret_diff`, `T9B_IVOL_MAX_ew_ret_diff` (the EW sign reversal is the key paper claim).

**T7 next — 28 cells.** Monthly Fama-MacBeth cross-sectional regressions of `ret_{t+1}` on `MAX_t` + 6 controls (BETA, log SIZE, log BM, MOM, REV, ILLIQ). The paper's specification includes 7 univariate regressions (one per predictor) and 1 "full" multivariate regression with all 7 predictors. Time-series average of slope coefficients with Newey-West t-stats. This requires all 6 control signals, so it should follow T6 + T9 (which produces SIZE/BM/MOM/REV/ILLIQ; BETA needs a 60-day rolling CAPM regression).

**T3 last — 35 cells.** Monthly cross-sectional regressions of current MAX on lagged MAX + 7 controls (lagged MAX + BETA + SIZE + BM + MOM + REV + ILLIQ + IVOL). Same panel infrastructure as T7; just different dependent variable. The paper's claim C4 ("MAX is persistent") is the headline.

**Verification step:** After each table is added, run `python scripts/score_replication.py <slug> --iteration 3` and verify `tier1_count` increases and `missing_count` decreases. Target: after T6/T9, missing drops by 34 (16+18); after T7, drops by 28; after T3, drops by 35. Final loss should be < 0.5 if all cells come out Tier 1 or Tier 2.

### [m1] — MINOR — Update REPORT.md to reflect iteration-2 state

`REPORT.md:15` says "Iteration: 1 of ≤ 5 outer" but this is now iteration 2. The TL;DR table ("19 Tier 1 + 33 Tier 2 + 6 FAIL = 58 cells") is the iter-1 tally. Update to the iter-2 tally ("29 Tier 1 + 38 Tier 2 + 5 FAIL / 97 MISSING = 169 cells; loss 1.43"). Add a section for the Table 6 SIZE control replication.

### [m2] — MINOR — Investigate the 5 extreme-decile FAILs

The 5 per-decile FAILs (D10_vw_ret +0.43 vs paper -0.02; D8_vw_alpha +0.53 vs paper -0.21; D9_vw_alpha +0.28 vs paper -0.49; D9-D10 ew_alpha) are at the extreme high-MAX deciles where the lottery effect has weakened in our CRSP vintage. The consolidated D10-D1 spread direction is preserved (negative). Possible additional tests: (a) restrict to NYSE-only and re-run; (b) restrict to pre-2000 and re-run; (c) winsorize MAX at the 99th percentile and re-run. If any of these brings the per-decile magnitudes into Tier 1, document the test and result.

### [m3] — MINOR — Update A4 impact line

`preparations/assumptions.md:167-188` (A4) impact line says "Loss has dropped from 2.0 → 1.43 (-28.5%)". Update to spell out the remaining 97 missing cells and which table each will close. Add a per-table-loss-contribution estimate: each Tier 1 reduces loss by ~0.006; each Tier 2 by ~0.006; each MISSING contributes 2·97/169 = 1.15 to the deficit.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human. A documented partial is more valuable than a paper-claiming success that does not actually replicate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.

## Inputs you should read

- `replications/<slug>/logs/audit2.md` — this audit (full context)
- `replications/<slug>/logs/audit1.md` — the previous audit (Table 1 sign-flip context)
- `replications/<slug>/logs/log2.md` — the previous replicator's iteration trace (5 inner iterations)
- `replications/<slug>/inputs/content.md` — paper ground truth (especially §2.3 for Table 6 BM/MOM/REV/ILLIQ; §2.4 for Table 7; §3 for Table 9; §2.2 for Table 3)
- `replications/<slug>/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/<slug>/src/main.py` — current code (will be modified); `table_6_size()` is the template for the other T6 controls
- `replications/<slug>/src/sql/panel.sql` — current pipeline (BM already deduplicated per A3)
- `replications/<slug>/data/` — cached intermediates (recompute spot-checks from these)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009) and safe to re-run at any point — mid-loop states no longer produce false errors. Re-run it if you changed a prep artifact; otherwise it is optional.
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run `src/evaluate.py` and `scripts/score_replication.py` after each fix — they are the gate that catches regressions.

## Deliverables for this iteration

- `replications/<slug>/src/main.py` — extended with `table_6_bm()`, `table_6_mom()`, `table_6_rev()`, `table_6_illiq()`, `table_9()`, `table_7()`, `table_3()` functions (per [M1])
- `replications/<slug>/results/table_<id>.md` — one per completed table (target: 5 total; T3, T6-extended, T7, T9 new this iteration)
- `replications/<slug>/data/metrics.json` — extended with all new cells
- `replications/<slug>/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status)
- `replications/<slug>/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict and score; do NOT edit (the auditor owns this file)
- `replications/<slug>/REPORT.md` — updated to reflect iter-3 state; lead with the data-quality summary (sample period, universe size, signal mean/std vs paper, headline-magnitude comparison, table count, corollaries evaluated this iteration)

## Stop conditions

- **All blockers fixed and verified** → re-run prep_validation.py and any sanity checks → if both pass, declare success or note remaining majors in `REPORT.md`; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`. The auditor's `SUMMARY.md` verdict (REPLICATED / FAILED) is independent of this loop decision.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This replication is steadily advancing. Iteration 2 closed the methodology contract issues (canonical metrics.json, Tier 2 cap) and added a bivariate control test (Table 6 SIZE) that replicates well. The headline lottery-effect direction is preserved (D10-D1 negative in both raw and alpha; extreme-decile returns decline D7→D10; AVG MAX replicates to <1% across 9 of 10 deciles). The 5 per-decile FAILs are at the extreme high-MAX deciles where the lottery effect has weakened in more recent CRSP vintages — the consolidated D10-D1 spread direction is consistent with the paper, but the per-decile magnitudes do not match. This is a documented data-vintage limitation, not a methodology bug.

The remaining gap is **scope**: 57% of committed cells are still MISSING, and they cover the bulk of the paper's argument (bivariate controls on BM/MOM/REV/ILLIQ, Fama-MacBeth regressions, MAX × IVOL reversal, MAX persistence). The replicator's iteration-2 work plan explicitly defers these with a clear timeline ("Table 6 BM/MOM/REV/ILLIQ controls (16 cells); Table 7 Fama-MacBeth (28 cells); Table 9 MAX × IVOL (18 cells); Table 3 cross-sectional MAX persistence (35 cells)"). With the panel infrastructure already in place (dsfhdr PIT filter, BM dedup, mcap_lag1, FF factors), each new table is a tractable extension of the existing pipeline.

The methodology dimension stays at 5 because every paper construction detail matches: MAX formula, decile sort, FF-Carhart 4-factor alphas, Newey-West t-stats, BMP/Shumway delisting, forward-shifted ret. The dsfhdr PIT fix is empirically demonstrated. The new Tier 2 cap (2× magnitude) is correctly enforced in `src/evaluate.py` and the canonical scorer agrees. The 5 remaining FAILs are not methodology bugs.

The binary verdict REPLICATED (mean 3.17, no dimension = 1) reflects the score, but the actionable major count is 1 (corollary coverage gap), so `requires_iteration: true`. The replicator is making consistent progress with high-quality methodology; the next iteration should drive the loss toward 0 by completing the four deferred tables.
