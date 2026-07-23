---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 3
requires_iteration: true
---

# Audit Report 1 — illiquidity_and_stock_returns

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Faithful, well-documented replication of Amihud (2002) Tables 1–4. All headline claims independently reproduced from cached artifacts (k_ILLIQMA 0.166/t 6.56 vs 0.162/6.55; annual g2 −24.24 vs −23.57; monthly g1 0.845/g2 −4.18 vs 0.712/−5.52, R² 0.143 vs 0.144). Three actionable majors keep this at PARTIAL: (M1) the reported tier aggregate uses the repo TOLERANCE_RULES definition, under which 34 Tier-2 cells are outside the audit rubric's 2× bound (strict count 199/52/44, not 199/86/10); (M2) the paper's §3.3 six-subperiod robustness corollary is reported in the paper but never computed; (M3) `prep_validation.py` exits 1 on five non-canonical parquet names in `data/`. No blockers; headline claims are trustworthy.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass; two documented deviations (annual Rf = compounded 1m bill, A2; Table 3 NW maxlags=0 selected by lag sweep, A8-revised) and two paper-silent choices (A5-revised open-NYSE universe for the TS aggregates, A7 SW 1-lead/1-lag). No methodology bugs found on independent recompute. |
| Headline matching | 4 | Sign, significance and shape replicate everywhere; magnitudes within ~20% except annual g1(market) coef +38.5% (its t-stat matches within 18%) and monthly g2(market) −24%. k_ILLIQMA and annual g2 match to ≤3%. |
| Data coverage | 4 | Exact period (1963–1996 chars, 1964–1997 FM, 1964–1996 TS); CRSP+FF sources match; one documented Rf substitute. Admitted counts 1,047–1,771 inside the paper's 1,061–2,291 range in 33/34 years, but the 1990s upper bound is never approached (−23% at max; documented vintage drift, A12, filter verified not-too-tight). |
| Concrete result matching | 3 | Tier 1 share 199/295 = 67.5% (auditor-recomputed tallies match the results files exactly). Under the rubric's 2× Tier-2 bound the strict split is 199/52/44 — the Tier-1 share (the scored quantity) is unchanged, but the reported "86 Tier 2 / 10 FAIL" understates FAILs. |
| Signal strength | 4 | Flagship coefficient ratios vs paper: k 1.02, g1-annual 1.39, g2-annual 1.03, g1-monthly 1.19, g2-monthly 0.76; all t-stat ratios within [0.82, 1.18]. Two coefficients break the 1.2 band (worst-cell reading → 3); pair/average reading → 4. Scored 4 with the worst-cell caveat on record. |
| Corollary | 3 | Subsample stability (Table 2 windows), SZ2 (strict, both tables), AR(1)+Kendall dynamics all replicate; SZ1 directional only (3/4 and 2/4 adjacent pairs), size-portfolio JANDUM/R² magnitudes inflated, and the §3.3 six-subperiod g1/g2 robustness is in the paper but not computed. |

## 2. Issues by severity

### Blockers (must fix)

- None. Headline cells verified by independent recomputation; no units errors, no sign flips in headline claims, no look-ahead, artifacts self-consistent and reproducible from `data/` + `src/sql/`.

### Major (should fix)

- [M1] Tier-2 labels violate the audit rubric's 2× magnitude bound (actionable: true)
  - File: `src/main.py` `cell_eval()` (≈L626–641); aggregate lines in `REPORT.md` §3 and `logs/log1.md` per-cell table.
  - Evidence: the results files define Tier 2 as "sign ok, |dev| > tol" following `rep/TOLERANCE_RULES.md`, but `audit/RUBRIC.md` defines Tier 2 as "sign match AND magnitude within 2× of paper; FAIL otherwise". Auditor recompute: 34 of the 86 Tier-2 cells have |ours/paper| outside [0.5, 2] — Table 2: 19 (model-b BETA coef/t with paper t ≤ 0.79, ratios 2.7–4.1; DIVYLD coef/t, ratios 0.23–0.49; constants at paper |t| ≤ 1; lnSIZE 1981–97 coef 2.07×); Table 3: 2 (g1_rsz10 t-cells vs paper t = 0.13/0.14, ratios ≈ 10.8 — a statistically zero paper cell); Table 4: 13 (g0 size-portfolio coef/t cells, ratios 0.01–0.31, the A16 anomaly cluster; g1_rsz4 t ≈ 0.48). Strict tally: **199 Tier 1 / 52 Tier 2 / 44 FAIL** (vs reported 199/86/10). All 34 cells are statistically vacuous in the paper or carry documented causes (A13, A15, A16) — no hidden discrepancy — but the human-facing aggregate overstates pattern-matches.
  - Likely cause: repo rule (`rep/TOLERANCE_RULES.md`) and audit rubric (`audit/RUBRIC.md`) use different Tier-2 definitions; the replicator followed the repo rule only.
  - Specific fix: add the 2× bound to `cell_eval()` (or report a second "strict" tally), regenerate the four `results/table_*.md` summaries, and restate the aggregate in `REPORT.md` as both conventions (repo-rule 199/86/10; rubric-strict 199/52/44) with the one-line note that all 34 reclassified cells are paper-side noise cells or documented A13/A15/A16 gaps.

- [M2] Corollary 'six-subperiod stability' not computed in artifacts (actionable: true)
  - Paper: §3.3, `inputs/content.md` L772–777 — "the sample of 408 months is divided into six equal subperiods of 68 months... All six coefficients g1 are positive, with mean 0.871 and median 0.827. All six coefficients g2 are negative with mean −7.089 and median −5.984."
  - Evidence: no subperiod split anywhere in `results/`, `data/`, `REPORT.md`, or `logs/log1.md`. This is the paper's stated time-series robustness check, and its reported g2 mean (−7.089) is materially more negative than the full-sample −5.52 — against our full-sample −4.18, the subperiod mean is the more demanding comparison and is currently unverified.
  - Specific fix: split the 1964-01..1996-12 sample (T=396) into six 66-month windows (the paper's "68 months" is of the 408-month series; document the convention), re-estimate model (10m) market column per window from `data/{milliq,market_ret,rf,rsz}.parquet`, and report sign count + mean/median of g1 and g2 vs the paper's 0.871/0.827 and −7.089/−5.984 in `results/table_4_subperiods.md`. Optionally add the Chow-test stability claim (paper L561, L759) for the annual/monthly AR(1).

- [M3] `prep_validation.py` exits 1 (actionable: true)
  - File: `data/` layout; run `python scripts/prep_validation.py illiquidity_and_stock_returns`.
  - Evidence: exit 1 with three errors — two are auditor-owned and fixed by this audit (missing `logs/audit*.md`, missing `SUMMARY.md`); the third remains: "data/ contains 5 unexpected parquet(s): ailliq, market_ret, milliq, rf, rsz". `rf.parquet` and `rsz.parquet` are effectively raw ff/msib extracts; the validator's allowlist does not recognize these names as computed artifacts.
  - Specific fix: move the five auxiliary series to `data/_cache/` (or rename to allowlisted artifact names), update the five `LAYOUT.data_path(...)` read/write sites in `src/main.py` (`main()` L435–442, `_load_ts_inputs()` L1026–1053), re-run `src/main.py` to confirm the four results files are byte-stable, and re-run the validator to exit 0.

### Minor (cleanup)

- [m1] A11 arithmetic cited against the wrong series.
  - File: `preparations/assumptions.md` A11; `results/table_4.md` AR(1) note; `REPORT.md` §3.
  - Evidence: "(1 − 0.768) × mean(ln MILLIQ) ≈ 0.313 to 0.006" holds for the *admitted* series (mean ln = −1.325 → −0.308) but not the *adopted open* series (mean ln = +0.0067 → +0.0015; auditor-verified). The decisive anomaly — paper intercept 0.313 with slope 0.945 implies mean ln MILLIQ = +5.7, contradicting the paper's own Table 1 level (0.337×10⁶, ln ≈ −1.1) — holds under either series, so the conclusion stands; only the citation needs pinning to the admitted series.
  - Specific fix: annotate A11 and the table_4.md note that the (1−0.768)×mean coincidence is computed on the admitted series; keep the e^5.7 internal-consistency argument as the primary justification.

- [m2] Annual Rf substitute sensitivity untested (A2).
  - File: `preparations/assumptions.md` A2.
  - Evidence: Table 3's g0_market is Tier 2 (+43%); the constant absorbs the Rf level, and `mcti` holds t90ret/1y-bill-return proxies that may approximate the paper's beginning-of-year one-year bill yield better than the compounded 1-month bill (especially 1979–82). Slopes g1/g2 are nearly invariant to this choice, so this is optional.
  - Specific fix: one sensitivity re-run of the Table 3 market column with an mcti-based annual Rf; report the g0/g1/g2 deltas in table_3.md's sensitivity block.

- [m3] `logs/log1.md` ends with a duplicate "## Summary (pending)" stub after the completed summary.
  - Specific fix: delete the trailing stub.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (SZ1/SZ2) | ✓ (partial) | SZ2 strictly holds in both tables (4/4 adjacent pairs, verified from results tables); SZ1 directional only — g1(RSZ2) > g1(RSZ10) both tables but 3/4 (Table 3) and 2/4 (Table 4) adjacent pairs strictly monotone. Paper claims strict monotonicity (L717–729). |
| 2 | Headline-magnitude claim | ✓ | Independently recomputed from `data/panel.parquet`: k_ILLIQMA(model a, all) = 0.1657, t = 6.56 (paper 0.162, 6.55); median k 0.1417, 63.24% positive, autocorr 0.051 — all match `results/table_2.md` to the printed digit. Table 3 market column recomputed: g1 14.166 (t 3.17)[NW0 2.82], g2 −24.244 (t −4.10)[−4.18], R² 0.5048, DW 2.530 — exact. Table 4 market column: g0 0.732, g1 0.845 (t 2.88), g2 −4.182 (t −6.04)[White −3.22], g3 4.981, R² 0.1428, N 396 — exact. Annual AR(1) −0.161+0.715 (R² 0.477, DW 1.494, KC 0.810) and monthly AR(1) −0.003+0.907 (R² 0.820, DW 2.468, KC 0.916) — exact. corr(u^M_open, market excess) = −0.255 (admitted −0.434), matching the logged pivot rationale. |
| 3 | Sample coverage ≥ 60% | ✓ | Panel 58,609 rows × 26 cols, 3,844 permnos; admitted cross-section mean 1,353 stocks/month (min 1,028 / max 1,758), inside the paper's 1,061–2,291 band in 33/34 characteristic years (1963: 1,047, −1.3%); zero null rates among admitted rows for all 11 characteristics. Upper-bound shortfall documented (A12) with the filter verified not-too-tight (dsfhdr PIT universe broader than the dsenames alternative). |
| 4 | Data-source choice justified | ✓ | CRSP dsf/msf/dsfhdr/dsedelist/dsedist/msib match the paper's CRSP; FF rf is one documented substitute for the paper's beginning-of-year 1y bill yield (A2, catalog-checked); RM = NYSE-only EW from dsf follows the paper's explicit wording (L579/L768) with the CRSP msi blend retained as a sensitivity (and confirmed worse on the market column, g2 −30.0 vs −24.2). |
| 5 | prep_validation.py exit 0 | ✗ | Exit 1 — see [M3]. Two of three errors are auditor-owned (fixed by this audit); the data/ parquet-name error remains. |
| 6 | All committed tables have results files | ✓ | T1–T4 all present with per-cell evaluation blocks; Table 5 out of scope with a verified data-availability rationale (no BAA/AAA/long-Treasury yield tables in the ClickHouse catalog; A1). |
| 7 | SUMMARY/REPORT values match results files | ✓ | Spot-checked k = 0.166/t 6.56, annual g1 14.17/g2 −24.24, monthly g1 0.845/g2 −4.18, R² 0.143 vs 0.144, Table 1 ILLIQ mean 0.347 — all reproduce from `results/table_*.md` and from the parquets. Caveat: the aggregate "199/86/10" is correct only under the repo rule — see [M1]. |
| 8 | No orphan folders | ✓ | Slug root clean; `data/_cache/` and `src/__pycache__/` are intentional. |
| 9 | Diagnoses paired with fix attempts | ✓ | `assumptions.md` iteration entries 1–4 carry Diagnosis/Next fix/Before/After/Status; the two methodology pivots (A5-revised annual AILLIQ, A8-revised NW) each show before/after metrics, and the monthly MILLIQ pivot was adopted under a four-part rule pre-registered in log1.md inner iteration 4 *before* the iteration-5 diagnostic numbers — good practice, not target-fitting. |
| 10 | Tier 2 within 2× magnitude | ✗ | 34 cells outside [0.5, 2] — see [M1]. Strict split: 199/52/44. |

## 4. Issues the agent should have caught (didn't)

1. **The rubric's 2× Tier-2 bound.** The agent cites `rep/TOLERANCE_RULES.md` (Tier 2 = sign ok, no magnitude cap) but the audit rubric caps Tier 2 at 2×. A careful self-review would have reported both tallies — especially since the affected cluster (model-b BETA at paper t ≤ 0.79, DIVYLD, Table 4 g0 intercepts) is exactly the set where "sign match" is statistically meaningless.
2. **The §3.3 six-subperiod corollary.** The paper reports concrete numbers (g1 mean 0.871/median 0.827; g2 mean −7.089/median −5.984) that are computable from the existing artifacts; the iteration log never mentions them. Notably the paper's subperiod g2 mean is more negative than its full-sample value, which would have been the sharper test of the open-universe fix.
3. **A11's arithmetic under the adopted series.** The "(1 − 0.768) × mean ≈ 0.313" coincidence was derived on the admitted series; after adopting the open series (mean ln +0.007) the identity no longer holds. The e^5.7 internal-consistency argument survives, but the citation should have been re-pinned in iteration 5.
4. **prep_validation.py was never run.** The iteration log and REPORT.md do not mention it; the slug has been validation-failed since the pipeline build.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Illiquidity and stock returns: cross-section and time-series effects" (Amihud 2002) for slug `illiquidity_and_stock_returns`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/illiquidity_and_stock_returns/logs/audit1.md`). Read the audit first. The core pipeline is converged and auditor-verified — every headline number reproduced from the cached artifacts. Do NOT re-touch the converged construction (admission criteria, ILLIQ/ILLIQMA, open-universe AILLIQ/MILLIQ, AR(1)+Kendall, Tables 1–4 regressions) except where an issue below says so.

## Issues to address (priority order)

### [M1] — MAJOR — report the rubric-strict tier tally
The audit rubric defines Tier 2 as sign-match AND magnitude within 2× of the paper; `cell_eval()` in `src/main.py` (≈L626) implements the repo rule (sign-match only). 34 cells labeled Tier 2 fall outside 2× (Table 2: 19 — model-b BETA/DIVYLD/constants; Table 3: 2 — g1_rsz10 t-cells vs paper t = 0.13; Table 4: 13 — g0 size-column cells + g1_rsz4 t). All are statistically vacuous in the paper or documented (A13/A15/A16); nothing substantive changes.

**Specific fix:**
1. In `cell_eval()`, add the 2× bound (sign ok AND 0.5 ≤ |ours/paper| ≤ 2, else FAIL) — or keep the repo-rule label and emit a second strict tally per table.
2. Regenerate `results/table_1.md` … `table_4.md`; expected strict aggregate: **199 Tier 1 / 52 Tier 2 / 44 FAIL** of 295.
3. Restate the aggregate in `REPORT.md` §3 and §7 under both conventions, with one line noting the 34 reclassified cells are paper-side noise cells (paper |t| ≤ 1) or documented A13/A15/A16 gaps.

### [M2] — MAJOR — compute the §3.3 six-subperiod robustness corollary
Paper (`inputs/content.md` L772–777): the 408-month sample split into six equal subperiods gives all-six-positive g1 (mean 0.871, median 0.827) and all-six-negative g2 (mean −7.089, median −5.984). Not computed anywhere in artifacts.

**Specific fix:**
1. From `data/{milliq,market_ret,rf}.parquet`, estimate model (10m) on the market column over six consecutive 66-month windows of 1964-01..1996-12 (document the 66-vs-68-month convention: the paper's 68 is of the 408-month MILLIQ span; the 396-month regression window gives 66).
2. Write `results/table_4_subperiods.md`: per-window g0/g1/g2/g3 with OLS t, sign counts, and mean/median of g1 and g2 vs the paper's 0.871/0.827 and −7.089/−5.984. Note the paper's g2 mean (−7.089) is more negative than its full-sample −5.52 — compare ours (full-sample −4.18) honestly.
3. Optional: add a Chow-test check of AR(1) stability (paper L561/L759) as a note.

### [M3] — MAJOR — make prep_validation.py exit 0
`python scripts/prep_validation.py illiquidity_and_stock_returns` exits 1: five parquets in `data/` (ailliq, market_ret, milliq, rf, rsz) are not allowlisted artifact names (after audit 1, this is the only remaining validator error).

**Specific fix:**
1. Move the five auxiliary series to `data/_cache/` (or rename to allowlisted names) and update the write sites in `src/main.py` `main()` (≈L435–442) and the read sites in `_load_ts_inputs()` (≈L1026–1053).
2. Re-run `src/main.py`; confirm the four `results/table_*.md` files are byte-stable (the regressions read these artifacts).
3. Re-run the validator; it must exit 0.

### [m1] — MINOR — re-pin the A11 citation
The "(1 − 0.768) × mean(ln MILLIQ) ≈ 0.313" identity holds for the admitted series (mean ln −1.325) but not the adopted open series (mean ln +0.0067). Annotate `assumptions.md` A11 and the `results/table_4.md` AR(1) note accordingly; keep the decisive argument (paper intercept 0.313 + slope 0.945 ⇒ mean ln MILLIQ = +5.7, contradicting the paper's own Table 1 level 0.337×10⁶).

### [m2] — MINOR (optional) — annual Rf sensitivity
One Table-3 market-column re-run with an mcti-based annual bill return (t90ret/b1ret) in place of the compounded 1-month bill (A2); report the g0/g1/g2 deltas in table_3.md's sensitivity block. g0_market is +43% Tier 2 and the constant absorbs the Rf level.

### [m3] — MINOR — delete the trailing "## Summary (pending)" stub in logs/log1.md.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Exit gate:** before declaring success, verify every diagnosed problem has a log entry with a non-empty `Next fix` and a before/after metric — iteration 1's exit gate was clean; keep it that way.

## Inputs you should read

- `replications/illiquidity_and_stock_returns/logs/audit1.md` — this audit (full context)
- `replications/illiquidity_and_stock_returns/inputs/content.md` — paper ground truth (§3.3 L772–777 for [M2])
- `replications/illiquidity_and_stock_returns/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/illiquidity_and_stock_returns/src/main.py` — current code
- `replications/illiquidity_and_stock_returns/data/` — cached intermediates (recompute spot-checks from these)

## What NOT to redo

- Do NOT re-run the ClickHouse pipeline or re-derive any series — the cached artifacts are auditor-verified and the two universe pivots (A5-revised annual AILLIQ, open monthly MILLIQ) and the NW maxlags=0 choice (A8-revised) are accepted as documented.
- Do NOT re-evaluate Tables 1–4 cells beyond the [M1] reclassification.
- Do NOT attempt Table 5 (bond yields absent from ClickHouse; A1, non-actionable).
- Do NOT edit `SUMMARY.md` (auditor-owned).
- Skip re-reading `SKILL.md` and re-running the catalog scan.

## Deliverables for this iteration

- `src/main.py` — [M1] cell_eval bound (or dual tally); [M3] artifact relocation
- `results/table_1.md` … `table_4.md` — regenerated with the strict tally; `results/table_4_subperiods.md` — new ([M2])
- `preparations/assumptions.md` — append an iteration-6 entry per issue (Diagnosis, Next fix, Before metric, After metric, Status); re-pin A11 ([m1])
- `REPORT.md` — updated aggregate under both conventions; subperiod corollary result; validator status
- `logs/log1.md` — remove the pending stub ([m3]); do NOT edit `SUMMARY.md`

## Stop conditions

- **All three majors fixed and verified** (strict tally in results files; `table_4_subperiods.md` written; validator exit 0) → declare success; the next audit updates `SUMMARY.md`.
- **Subperiod g2 mean far from −7.089** → do NOT chase it with further universe variants (the open-universe adoption rule is locked); document the gap as a vintage/paper-side partial in `REPORT.md`.
- **10-iteration cap** on any single problem → escalate to the human.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the cleaner replications in the repo. The iteration log is exemplary: every pivot was diagnose-then-fix with before/after metrics, and the two decisions most exposed to target-fitting criticism survive scrutiny. (i) The open-NYSE-universe annual AILLIQ is the *literal* text of §3.1 L503 ("the average across all stocks... excluding stocks whose ILLIQ_iy is in the upper 1% tail"), which genuinely conflicts with §2.3.1 L206's admitted-sample average; the replicator used each reading where the paper places it (cross-section denominator vs time-series aggregate), and the AR(1) dynamics — slope 0.715, DW 1.494, and the DW-implied residual ρ +0.228 against the paper's +0.215 — discriminate between the variants cleanly. (ii) The monthly open-MILLIQ adoption was gated on a four-part rule committed in writing *before* the diagnostic ran (log1.md inner iteration 4), and the resulting corr(u^M, market excess) = −0.255 lands exactly on the paper-implied ≈ −0.23; my independent recompute confirms every reported number to the printed digit. The NW maxlags=0 choice (A8-revised) is the weakest methodological point — it reduces Newey-West to a heteroskedasticity-robust sandwich while the paper's footnote claims autocorrelation robustness — but it is documented, sweep-selected, and reproduces the paper's own bracketed t-stats (which barely move from OLS: 2.68→2.74, 4.52→4.11, suggesting the paper itself used effectively zero lags); I accept it as a documented deviation, not a bug. The honest residuals are vintage-driven (DIVYLD −18%, compressed size-portfolio betas, 1990s count shortfall, inflated small-decile g1/g2 magnitudes) and paper-driven (the monthly AR intercept and Table 4 g0 cluster — I verified the A11 anomaly independently: 0.313/(1−0.945) = +5.7 in log units, impossible against the paper's own Table 1). What keeps this at PARTIAL rather than PASS is reporting hygiene, not science: the tier aggregate is stated under the looser of two definitions ([M1]), a paper-reported corollary was skipped ([M2]), and the validator was never run ([M3]) — all three are cheap, mechanical, and worth one more pass.
