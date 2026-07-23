---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — the_cross_section_of_expected_stock_returns

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** High-quality replication of Fama & French (1992). All six main tables independently recomputed by the auditor from `data/*.parquet` with a from-scratch implementation; every value checked reproduces the replicator's numbers to rounding. All four central claims replicate. Zero blockers; one actionable major (January-seasonality corollary holds in the data but is not surfaced in `results/`) plus minor cleanups → one short finishing iteration.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six rubric checks pass (formula, timing, filters, winsorization, look-ahead, statistical conventions); 30 paper-cited rules in `preparations/preprocessing_rules.json`, all implemented in `src/main.py`/`src/sql/`; deviations (delisting treatment, BE fallback chain, financials in NYSE size breakpoints, June-t PIT screen) are documented and justified — not zero-deviation, so 4 not 5. |
| Headline matching | 4.5 | All four claims match shape and sign: β unpriced (R1 0.07, t 0.22; combined-regression β t-stats 0.39/0.58/−0.55/0.69 matching the paper's own prose L1159), size negative (−0.14, t −2.47; deciles 1.60→0.85), BE/ME positive and dominant (0.49, t 5.54; 0.41→1.79), absorption of leverage and E/P. Core coefficients within ~10%; E(+)/P levels drift +0.7–1.1 in multivariate specs (documented vintage shift). |
| Data coverage | 4 | Exact period (330 months, Jul 1963–Dec 1990); universe 2,393 obs/mo vs 2,267 (+5.5%) and 2,477 firms/yr vs 2,317 (+6.9%) — within the 5–15% band; same sources (CRSP+Compustat), one documented substitute (SIC from CRSP dsenames), data-vintage drift documented and evidenced. |
| Concrete result matching | 4 | 692/780 targeted cells Tier 1 = 88.7% (auditor-verified counts: 107/168/30/199/110/78). In the 70–90% band → 4. The 2 FAILs are sign flips on statistically null coefficients (Table III R11 E/P dummy, |t| < 0.6 both sides). |
| Signal strength | 4 | Priced-variable headline cells all within 20%: ln(ME) r=0.92, ln(BE/ME) r=0.99, R7 r=0.98/0.97, size-decile 1A r=0.98, Table V spreads r=0.85/1.05, E(+)/P-alone r=1.18 → all in [0.8, 1.2]; not all within 10%, so 4. The β-alone null replicates as a null (t 0.22 vs 0.46). |
| Corollary | 4 | Subperiod stability (Table VI 63/63 cells; β insignificant in both halves; BE/ME 0.31–0.36 vs paper 0.34–0.36), pre/post-ranking β ordering (incl. the paper's 1B quirk), leverage resolution (identity to 9e-16), E/P absorption, and the Table V double gradient all replicate; January-seasonality corollary (L2186) holds in the data but is not surfaced in artifacts ([M1]); appendix Tables AI–AIV documented out of scope ([M2]). |

**Overall: 4.08 / 5 → REPLICATED** (mean ≥ 3.0 and no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] Corollary 'January seasonality of the BE/ME slope' not computed in artifacts. Actionable: true.
  - File: `inputs/content.md:2186` (paper claim); absent from `results/table_6.md` and all of `results/`.
  - Paper claim (L2186): "The average January slopes for ln(BE/ME) are about twice those for February to December… the average monthly February-to-December slopes for ln(BE/ME) are about 4 standard errors from 0, and they are close to (within 0.05 of) the average slopes for the whole year."
  - Auditor verification from `data/panel.parquet` (reg(a) monthly slopes, same winsorization as `src/table_3_6.py`): January mean 0.606 %/mo, Feb–Dec mean 0.318 (t = 3.85), full-year 0.341 (gap 0.024). The claim holds in the replication's own data — it just was never written out.
  - Likely cause: the plots iteration prioritized the five figures; this paragraph-level corollary was skipped.
  - Specific fix: add a January vs Feb–Dec decomposition of the monthly ln(BE/ME) slopes (from the existing `fm_monthly` output in `src/table_3_6.py`) to `results/table_6.md` or a new `results/table_6_january.md`; expected values: Jan ≈ 0.61, Feb–Dec ≈ 0.32 (t ≈ 3.9), gap < 0.05.

- [M2] Appendix Tables AI–AIV (NYSE-only, 1941–1990) not replicated. Actionable: false.
  - File: `preparations/assumptions.md` Assumption 12; `REPORT.md` §7.
  - The appendix is a robustness extension on a different sample (NYSE-only; pre-1962 portion is CRSP-only with different data requirements). The replicator documented the scope boundary with justification; the four main claims live in Tables I–VI, all replicated. Re-opening scope would chase a different sample, not a defect; non-actionable within this run.

### Minor (cleanup)

- [m1] `src/evaluate.py` Tier-2 rule does not enforce the 2× magnitude bound of auditor spot-check 10. Three same-sign Tier-2 cells exceed 2× of the paper: Table III R9 E/P dummy slope 0.289 vs 0.06 (4.8×) and t 1.36 vs 0.38 (3.6×); R11 E(+)/P t 3.19 vs 1.57 (2.03×). All are near-null targets (coefficients the paper itself shows are killed); reclassification changes no claim. Fix: relabel these three as FAIL-with-citation or add an explicit near-null exception to the tier rule.
- [m2] Orphan nested directory at the slug root: `replications/the_cross_section_of_expected_stock_returns/{data,src,results,logs,inputs,preparations}` — empty skeleton, likely `LAYOUT.ensure()` run from the wrong CWD. Fix: delete the nested `replications/` tree.
- [m3] `scripts/prep_validation.py` (exit 0) flags `data/agg_portfolio_returns.parquet`, `data/nyse_benchmark_returns.parquet`, `data/portfolio_returns.parquet` as unexpected — the validator's name allowlist doesn't cover these computed intermediates (they are computed artifacts, not raw dumps). Fix: rename to an allowed pattern or leave (validator exits 0).
- [m4] `REPORT.md` §1 says "783 targeted cells" while the consolidated evaluation counts 780 unique targets (3 exact-duplicate Table I Panel-C cells deduped). Fix: one-line consistency note in REPORT.md.

## 3. Verification spot-checks (recomputed by auditor)

All recomputations below were run by the auditor with an independent from-scratch implementation (own winsorization, own monthly OLS, own aggregations) reading only `data/*.parquet` — no `src/` code was imported.

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Auditor-recomputed from panel: size12 returns 1.60→0.85 (paper 1.64→0.90); BE/ME12 0.41→1.79 monotone (paper 0.30→1.83); β12 returns flat (1.15→1.11) while post-β runs 0.81→1.73 (paper 0.81→1.73 — essentially exact); E/P U-shape 1.25→0.83→1.70 (paper 1.46→0.93→1.72); E/P port-0 dummy = 1.00, E(+)/P = 0.00 exactly. |
| 2 | Headline-magnitude claim | ✓ | Independent FM: R1 β 0.072 (t 0.22); R2 ln(ME) −0.138 (−2.47) vs paper −0.15 (−2.58); R4 ln(BE/ME) 0.493 (5.54) vs 0.50 (5.71); R7 −0.108 (−1.92)/0.341 (4.20) vs −0.11 (−1.99)/0.35 (4.44); avg monthly N 2,393 vs 2,267. All match `results/table_3.md` to rounding. |
| 3 | Sample coverage ≥ 60% | ✓ | 330/330 months; 28/28 formation years; 2,477 firms/yr vs paper 2,317 (+6.9%); 97.4% of panel rows carry a valid return. |
| 4 | Data-source choice justified | ✓ | CRSP (msf, msedelist, msi, dsenames, ccmxpf_linktable) + Compustat funda — same sources as paper; one documented substitute (SIC via CRSP dsenames, Assumption 4, because funda carries no SIC); vintage drift (crsp_202601/comp_202601 vs ~1991 tape) documented with evidence (SDs match paper; mean shift corroborated by CRSP's own msia NYSE index in the extract). |
| 5 | prep_validation.py exit 0 | ✓ | Exit 0. Three advisory layout notes: the three computed intermediates in `data/` (allowlist false positive, see [m3]); missing audit1.md and SUMMARY.md — both created by this audit. |
| 6 | All committed tables have results files | ✓ | `results/table_1.md` … `table_6.md` + `evaluation_summary.md` + 5 plots; every table id in `tables_to_replicate.json` covered. |
| 7 | REPORT.md values reproducible | ✓ | ~30 cited numbers re-derived independently (FM matrix incl. R8–R11; Table I A/B/C interiors and margins; Tables II/IV/V/VI; identity ln(A/ME)−ln(A/BE)=ln(BE/ME) to 8.9e-16). All match. |
| 8 | No orphan folders | ✗ (minor) | Nested empty `replications/…/` skeleton at slug root ([m2]). No literal-brace dirs. |
| 9 | Diagnoses paired with fix attempts | ✓ | All 6 iteration entries in `preparations/assumptions.md` have Built/Results/Facts; every worker flag in `logs/log1.md` has an explicit Replicator adjudication (financials in breakpoints kept; June-t PIT accepted; near-zero threshold unified — consequences quantified). No diagnosed problem left undischarged. |
| 10 | Tier 2 within 2× magnitude | ✗ (minor) | 83/86 Tier-2 cells comply; 3 same-sign cells exceed 2× on near-null targets ([m1]); the 2 sign flips are |paper| ≤ 0.05 boundary cells; the 7 `ocr-inconsistent` cells are independently verified paper-side inconsistencies (see below). No claim affected. |
| 11 | Corollary coverage | ✓ (with [M1]/[M2] surfaced) | Subperiod stability, β-ordering, leverage resolution, absorption, Table V gradients: checked and pass. January seasonality (L2186): holds in the data (Jan 0.606 ≈ 1.9× Feb–Dec 0.318; Feb–Dec t 3.85; gap 0.024) but not in artifacts → [M1]. Appendix AI–AIV → [M2] non-actionable. |

**Auditor's independent verification of the three documented deviation groups:**

1. **Table III R8–R11 β cells (OCR-internal inconsistency).** Confirmed. The paper's printed β t-stats imply monthly β-slope SDs of ≈0.95–0.97 %/mo (e.g. R8: 0.11×√330/2.06 = 0.97), while its own R1/R3 imply 5.9/5.6 — the auditor's recomputed SDs are 5.06–6.01 in ALL eleven specifications (R1 6.01, R3 5.46, R8 5.70, R9 5.63, R10 5.06, R11 5.48), matching R1/R3. A 6× dispersion compression from adding controls is statistically impossible, and pooled-style t-stats (mean ÷ avg monthly SE ≈ 0.87–0.99) on the replication's monthly β slopes are all |t| ≤ 0.25. The paper's prose (L1159: "typically less than 1 standard error from 0") matches the replication's R8–R11 β t-stats (0.39, 0.58, −0.55, 0.69). The 7 `ocr-inconsistent` classifications are justified — these targets cannot be hit by any internally coherent construction.
2. **Compustat/CRSP vintage-composition shift.** Consistent with the evidence: the identity ln(A/ME) − ln(A/BE) = ln(BE/ME) holds to 8.9e-16 cell-by-cell in the panel; ln(A/BE) (no market equity) passes 25/25 in Table IV while ln(A/ME)/ln(BE/ME) drift; June ln(ME) averages pass 25/25 while December-ME-denominated ratios shift; universe is +5.5%/+6.9% over the paper. The deviation enters via portfolio membership, not accounting data. The 2 FAILs (R11 E/P dummy slope/t: +0.066/+0.39 vs −0.08/−0.56) are sign flips on a coefficient with |t| < 0.6 on both sides — noise on a null.
3. **NYSE benchmark mean shift (3 cells).** Confirmed structurally: auditor recomputation from `data/nyse_benchmark_returns.parquet` gives VW 0.915/EW 1.146 full-period means vs paper 0.81/0.97, while all six SDs match the paper within 0.13 (4.475 vs 4.47, 5.598 vs 5.49, 4.297 vs 4.26, 5.834 vs 5.70, 4.638 vs 4.66, 5.373 vs 5.28). An aggregation error would move SDs too; a mean-only shift across both weightings is the fingerprint of a tape-level vintage difference.

## 4. Issues the agent should have caught (didn't)

1. The January-seasonality corollary (L2186) is an explicit paper claim computable from the monthly slopes the replication already produces — and it holds (auditor-verified). It should have been surfaced in iteration 6 alongside the plots.
2. The orphan nested `replications/` skeleton at the slug root ([m2]) — a final `ls` of the slug root would have caught it.
3. The three Tier-2 cells beyond 2× ([m1]) — the evaluator's own flags section documents the near-zero threshold debate but does not mention the 2× bound on same-sign cells.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The Cross-Section of Expected Stock Returns" (Fama & French 1992) for slug `the_cross_section_of_expected_stock_returns`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/the_cross_section_of_expected_stock_returns/logs/audit1.md`; scores: methodology 4, headline 4.5, data 4, concrete 4, signal 4, corollary 4; overall 4.08 → REPLICATED). Read the audit first. The replication is in excellent shape — the auditor independently recomputed all six tables from `data/*.parquet` and every checked value reproduces. This is a short finishing iteration: one corollary artifact plus cleanup.

## Issues to address (priority order)

### [M1] — MAJOR — corollary not surfaced in artifacts (fix first)

The paper's January-seasonality claim for the BE/ME slope (`inputs/content.md` L2186: "The average January slopes for ln(BE/ME) are about twice those for February to December… the average monthly February-to-December slopes… are about 4 standard errors from 0, and… within 0.05 of the average slopes for the whole year") is not computed anywhere in `results/`. The auditor verified it HOLDS in `data/panel.parquet` using the reg(a) monthly slopes: January mean 0.606 %/mo, Feb–Dec 0.318 (t = 3.85), full-year 0.341 (gap 0.024).

**Specific fix:**
1. In `src/table_3_6.py` (or a new `src/table_6_january.py` importing `fm_monthly`/`prewinsorize`), split the reg(a) monthly ln(BE/ME) slopes into January vs Feb–Dec; report mean, t-stat, and the gap to the full-year mean.
2. Write `results/table_6_january.md` (or append a section to `results/table_6.md`) with the decomposition and the L2186 comparison. Expected: Jan ≈ 0.61, Feb–Dec ≈ 0.32 (t ≈ 3.9), |full-year − Feb–Dec| < 0.05.
3. Add the corollary to the `results/evaluation_summary.md` headline section and cite L2186.

### [m1] — MINOR — Tier-2 2× bound

Three same-sign Tier-2 cells exceed 2× of the paper's value (Table III R9 E/P dummy slope 0.289 vs 0.06; t 1.36 vs 0.38; R11 E(+)/P t 3.19 vs 1.57 — all near-null targets). In `src/evaluate.py` `classify()`, either add the audit-spot-check-10 bound (same-sign Tier 2 requires |ours/paper| ≤ 2 unless |paper| ≤ 0.10) or document the near-null exception explicitly; regenerate `results/evaluation_summary.md`.

### [m2] — MINOR — orphan directory

Delete the empty nested skeleton `<slug>/replications/the_cross_section_of_expected_stock_returns/` at the slug root (created by a misplaced `LAYOUT.ensure()`).

### [m3] — MINOR — validator allowlist

`prep_validation.py` (exit 0) flags the three computed intermediates in `data/` (`agg_portfolio_returns.parquet`, `nyse_benchmark_returns.parquet`, `portfolio_returns.parquet`) as unexpected. They are computed artifacts, not raw dumps; either rename to an allowlisted pattern or leave with a one-line justification in REPORT.md §6.

### [m4] — MINOR — wording

REPORT.md §1 says "783 targeted cells"; the consolidated evaluation uses 780 unique (3 exact-duplicate Table I Panel-C targets deduped). Add the one-line clarification.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every new iteration-log entry in `assumptions.md` needs all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle** (not expected here — this is a short iteration).
- **Do NOT touch the methodology** — the auditor verified it end-to-end; changes risk regressing the 692 Tier-1 cells. Re-run `src/evaluate.py` after any change and confirm the per-table counts (107/168/30/199/110/78) are unchanged.

## Inputs you should read

- `replications/the_cross_section_of_expected_stock_returns/logs/audit1.md` — this audit (full context)
- `replications/the_cross_section_of_expected_stock_returns/inputs/content.md` L2186 — the January-seasonality claim
- `replications/the_cross_section_of_expected_stock_returns/src/table_3_6.py` — existing monthly-slope machinery (`fm_monthly`)
- `replications/the_cross_section_of_expected_stock_returns/data/panel.parquet` — cached panel (all recomputation runs from here)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact.
- Skip the ClickHouse rebuild — `data/panel.parquet` is verified and current; the January decomposition needs only the panel.
- **DO** re-run `src/evaluate.py` and confirm the Tier counts are unchanged after your edits.

## Deliverables for this iteration

- `results/table_6_january.md` (or an extended `results/table_6.md`) — the January vs Feb–Dec ln(BE/ME) slope decomposition with the L2186 comparison
- `results/evaluation_summary.md` — regenerated (corollary noted; [m1] tier-bound fix if applied)
- `preparations/assumptions.md` — new iteration-log entry for M1 and each minor addressed (Diagnosis, Next fix, Before metric, After metric, Status)
- `REPORT.md` — updated; add the January corollary to §3 and the [m4] clarification
- `SUMMARY.md` — auditor-owned; do NOT edit

## Stop conditions

- All issues above are low-risk; verify the Tier counts are unchanged, re-run the validator, and declare success.
- If ClickHouse is unreachable for any reason, everything needed here is in `data/panel.parquet` — no queries required.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is an unusually disciplined replication. The iteration log reads like a proper research audit trail: every worker flag is adjudicated, every deviation is diagnosed before being accepted, and the global-to-local checks (sample period, universe size, ledgered preprocessing, weighting) were run before any per-table work. Two pieces of replicator reasoning deserve specific credit. First, the Table III R8–R11 β diagnosis: rather than quietly Tier-2-ing eight cells against impossible targets, the replicator proved from the paper's own R1/R3 that the printed t-stats imply a 6× compression of the monthly β-slope dispersion — the auditor recomputed the implied SDs (0.95–0.97 vs 5.5–5.9) and the pooled t-stats (all ≤ 0.25 in absolute value) and confirms the targets are paper-side inconsistencies; the replication's values match the paper's prose. Second, the vintage-composition diagnosis is triangulated from three independent angles (the machine-precision ln(A/ME)−ln(A/BE)=ln(BE/ME) identity, the ln(A/BE) 25/25 pass-through, and the CRSP-msia corroboration of the NYSE mean shift), which is exactly how a data-vintage claim should be evidenced. One environment note: the auditor could not re-execute the ClickHouse SQL (server not running in the audit environment), so the SQL layer was verified by code inspection of `src/sql/*.sql` plus full downstream recomputation from the parquets; the saved SQL contains every documented filter (shrcd 10/11, exchcd 1/2/3, PIT SIC 6000–6999, INDL/C/D/STD, LC/LU+P/C+usedflag=1 PIT links, the delisting cascade, ME = |prc|×shrout×1000). The only substantive gap found is the missing January-seasonality artifact — and since the claim holds in the existing data, the next iteration should be short.
