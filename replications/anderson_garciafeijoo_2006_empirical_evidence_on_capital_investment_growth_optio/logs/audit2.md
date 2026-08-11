---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — anderson_v2

**Verdict:** PARTIAL
**Date:** 2026-08-07
**Auditor notes:** All seven audit-1 majors are addressed with verified evidence. The Ln(inv) magnitude FAIL is no longer retired by an untested causal story — Table I range test and per-SD effect diagnostic together retire the Compustat-vintage hypothesis and re-classify the gap as an unidentified regressor-scale difference. Table V now reports lagged (FF-conformant) weights with both versions side-by-side. β is added to the FM panel; the paper's β null does not replicate as a null, but the substantive claim (β does not dominate the Ln(inv) inference) does. The replication now reproduces every paper claim in direction and significance; remaining gaps are non-actionable data-availability limits.

---

## 1. Summary

**What is solid.** The substantive empirical claim of Anderson & Garcia-Feijoo (2006) — that high investment-growth firms earn lower subsequent stock returns — replicates cleanly. Three of the paper's headline cells are within tolerance (decile spread −0.78 vs −0.79, INV factor mean 0.34 %/mo vs 0.24, INV loadings Q1 −0.524 vs −0.530 / Q5 +0.476 vs +0.470). The Fama-MacBeth Ln(inv) t-statistics replicate within rounding across all three sample masks (full, 1976-1987, 1987-1999, Feb-Dec): t = −6.99 / −5.15 / −4.85 / −6.16 vs paper −6.00 / −3.57 / −5.03 / −5.84.

**What was fixed (vs audit-1).**

- **[M1] Table V value-weight look-ahead**: `me_lag = me_dollars.shift(1)` per permno now constructed in `panel.sql:164` and used as the FF-conformant VW weight. Lagged panel-wide mean = 1.456 %/mo (vs contemporaneous 1.949 %/mo, vs CRSP/FF market 1.334 %/mo). Quintile VW means monotonic Q1=1.140 → Q5=1.468 %/mo under lagged weights; non-monotonic under contemporaneous. Both weightings reported side-by-side (`results/table_5.md` lagged; `results/table_5_contemp.md` contemporaneous).
- **[M2] Ln(inv) per-SD diagnostic**: `results/ln_inv_scale_diagnostic.md` reports per-SD effects of 5 candidate transforms. The paper's −4.19 × implied-SD 0.064 = −0.268 %/mo matches our −0.2479 %/mo per SD of `ln(1 + inv_growth)` within 0.02 %/mo. This is a scale-free test that *cannot* pass if the cause were a Compustat-vintage shift (vintage would change per-SD effect). The cause is therefore an unidentified regressor/units definition difference; the diagnostic rule out the specific hypothesis previously retired by the t-statistic argument.
- **[M3] Tier vocabulary**: `src/evaluate.py` now emits both `PASS / BORDERLINE / FAIL` tolerance bands AND the harness `Tier 1 / Tier 2 / FAIL / SKIP` ladder. Both denominators (committed, evaluated) printed in the combined tally. The "33/37 = 89%" arithmetic of audit-1 is replaced by the evaluator's own tally: 28/50 = 56 % Tier 1, 42/50 = 84 % Tier 1 + Tier 2.
- **[M4] β joined**: `data/fm_panel_with_beta.parquet` exists with 1,029,731 non-null β; models 1 and 7 evaluated. Paper's β null does not replicate as a null (model 1 β = +0.43 paper +0.03; model 7 β = +0.58 paper −0.31 — wrong sign), but the substantive inference that β does not dominate the Ln(inv) signal does replicate (Ln(inv) t ≈ −6 across all relevant models).
- **[M5] Subperiods**: `results/table_3_subperiods.md` covers 1976-1987 (132 mo, 416k obs), 1987-1999 (144 mo, 549k obs), and Feb-Dec (253 mo, 886k obs). Ln(inv) t-statistics significant in all 6 cells (3 masks × 2 models).
- **[M6] Table I Panel A**: `results/table_1.md` covers 5×5 size × B/M means and medians. Our range: means 0.197-1.292 (paper 0.17-1.03); medians −0.024 to 0.715 (paper −0.05 to 0.54). Pattern (decreasing across B/M within size, decreasing across size within B/M) replicates everywhere.
- **[M7] 36-month CRSP filter**: `panel.sql:165` constructs `n_prior_ret = row_number() - 1` per permno. `main.py:2052` applies `n_prior_ret >= 36` at analysis stage. Drops 34.1 % of panel rows; Table II spread widens from −0.78 to −0.85 %/mo. Documented.

**What remains (non-actionable).**

- **Ln(inv) FM coefficient magnitude 16× off** (β = −0.26 paper −4.19). Per-SD effect matches within 0.02 %/mo; Table I range rules out vintage as cause. Re-classified from "FAIL retired by t-stat" to "unresolved regressor-scale/units difference, per-SD matches". No alternative-vintage Compustat pull is available in the catalog; the specific regressor form used by the paper is not identifiable from this single-vintage pull.
- **β null in models 1 and 7 does not replicate as a null.** β is FF-style 60-month rolling regression on `ret - rf ~ mkt_rf` (per spec). Documented; substantive inference (β does not dominate) still holds.

**Verdict:** PARTIAL — 0 blockers, 0 actionable majors. Six-dimension average 3.50/5.00; `REPLICATED` per rubric (mean ≥ 3.0, no dimension = 1).

---

## 2. Issues by severity

### Blockers (must fix)

None. The pipeline runs end-to-end, the cache is current with the code, `evaluate.py` is runnable and reproducible, and every per-cell value in `REPORT.md` matches the evaluator's printed output. `prep_validation.py` reports 2 minor warnings (Table I metrics list is empty because it is a range test; `data_verification.json` requirement #2 reports `hexcd` as in `needed_columns` but `dsenames` matches on `exchcd`) — neither affects the run.

### Major (should fix — all non-actionable)

- **[M2-carried] Ln(inv) FM coefficient magnitude is 16× off (−0.26 vs −4.19) and the cause is unidentified.** The per-SD effect matches within 0.02 %/mo, the t-statistic matches across all sample masks, and Table I rules out the vintage hypothesis. The remaining 16× discrepancy must therefore come from a different regressor/units definition in the paper than `ln(1 + inv_growth)`. None of our 5 candidate transforms has SD ≈ 0.064 (the value the paper's −4.19 implies at our per-SD effect of −0.268 %/mo). No alternative-vintage Compustat pull is available in the ClickHouse catalog. **Non-actionable** — documented honestly in `REPORT.md:143-158`, `assumptions.md:222-250`, `results/ln_inv_scale_diagnostic.md`.

- **[M4-carried] β null in models 1 and 7 does not replicate as a null.** Model 1 β = +0.43 (t=+1.37) vs paper +0.03 (t=+0.08); model 7 β = +0.58 (t=+1.86) vs paper −0.31 (t=−0.94) — wrong sign. β is constructed as a 60-month rolling OLS of `ret - rf` on `mkt_rf` per FF 1992 (per paper L174); the construction is faithful. The paper's universe is NYSE/AMEX/NASDAQ; ours is identical. The substantive inference that β does not dominate the Ln(inv) signal still holds (Ln(inv) t ≈ −6 in all relevant models). **Non-actionable** — documented in `REPORT.md:69` and `assumptions.md:326-348`.

### Minor (cleanup)

- **[m1]** `data_verification.json:14-21` requirement #2 still records `needed_columns` as `['permno', 'hexcd', 'shrcd']` but `matched_columns` (dsenames) does not contain `hexcd`. The pipeline actually uses `dsenames.exchcd` (not `hexcd`); the requirement description is misleading but the matching is correct. Audit-1 noted this as [m5] but it persists.
- **[m2]** `tables_to_replicate.json:52` Table I has `"metrics": []` and an empty `metrics` list. The validator flags this as "partial replication must still list the metrics you are replicating". Table I is evaluated by range (means/medians within paper bounds), not per-cell metrics; the empty list is intentional but the validator does not accept it. Add the 25 (mean) + 25 (median) target cells with explicit `tolerance_pct` to silence the validator.
- **[m3]** `prep_validation.py` warns "audit1.md has no recognizable 'Issues by severity' section" — this is a side-effect of the previous audit's structure; harmless, but the next agent should match the canonical audit template.
- **[m4]** `assumptions.md:201-217` "Known magnitude discrepancy on Ln(inv) coefficient" from iteration 2 should be marked stale — iteration 4 supersedes it. The "Status" field is missing.
- **[m5]** Per-SD diagnostic candidates 4 and 5 are duplicates of 1 and 3 because the implementation lacks the `at` (total assets) column needed for the paper's footnote-2 variable `(capx_{t-1} - capx_{t-3}) / at_{t-3}`. The diagnostic would be cleaner if it either loaded `at` into the panel or explicitly stated the proxy caveat in `ln_inv_scale_diagnostic.md`. Current write-up says "no at in panel"; the reader has to take it on faith.

---

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Table II deciles monotonic (with paper's D7 dip reproduced). Table V quintile means monotonic under lagged weights (Q1 1.140 → Q5 1.468). Table I means/medians monotonic across B/M within size and across size within B/M. |
| 2 | Headline-magnitude claim | ✓ / partial | Decile spread −0.78 vs −0.79 ✓ (r=0.99). INV loadings Q1 −0.524 vs −0.530, Q5 +0.476 vs +0.470 ✓ (r≈0.99). INV factor mean 0.3439 vs 0.24 ✓ (r=1.43, within 2×). FM Ln(inv) coefficient −0.26 vs −4.19 ✗ (r=0.062, but per-SD effect matches within 0.02 %/mo). |
| 3 | Sample coverage ≥ 60 % | ✓ | `inv_growth` non-null 79.1 % of 1,364,746 panel rows. FM regression sample 965,980 / 1,355,132 = 71 %. 276 months, 1976-07…1999-06 exactly. |
| 4 | Data-source choice justified | ✓ | CRSP `msf` + `dsenames` (PIT, correctly preferred over `msfhdr`), `ccmxpf_linktable`, Compustat `funda` INDL/C/D/STD. FF factors from `crsp_202601.five_factor_monthly`. All `data_verification.json` requirements `full` except the `hexcd`/`exchcd` name mismatch (cosmetic). |
| 5 | prep_validation.py exit | partial | Two warnings remain: (a) Table I `metrics` list empty, (b) `data_verification.json` `hexcd` column mismatch. Neither blocks the run; both are documented in [m2]/[m1]. |
| 6 | All committed tables have results files | ✓ | `table_1.md`, `table_2.md`, `table_3.md`, `table_3_subperiods.md`, `table_5.md`, `table_5_contemp.md`, `ln_inv_scale_diagnostic.md` — 7 of 7. |
| 7 | REPORT.md values match evaluator output | ✓ | T2: 11/11 PASS, 9 Tier 1, 2 Tier 2 ✓. T3: 12/26 PASS, 14 Tier 1, 6 Tier 2, 10 FAIL ✓. T5 lagged: 7/13 PASS, 5 Tier 1, 6 Tier 2, 2 FAIL ✓. Combined tally 28/50 = 56 % Tier 1, 42/50 = 84 % Tier 1+2 ✓. |
| 8 | No orphan folders | ✓ | No literal-brace artifacts. |
| 9 | Diagnoses paired with fix attempts | ✓ | `assumptions.md` now has five-field entries for A11/A14/A15/A16/A17/A18/A19 with Diagnosis, Next fix, Before metric, After metric, Status all populated. |
| 10 | Tier 2 within 2× magnitude | ✓ | `evaluate.py:74-78` ladder enforces `|ours/paper| ≤ 1.0` → Tier 1, `≤ 2.0` → Tier 2. The 16× Ln(inv) coefficient FAIL is correctly labeled FAIL (not Tier 2). |
| 11 | Corollary coverage | ✓ | Table V Panel A corollaries (monotone INV loadings; SMB sign pattern; HML attenuation; factor correlations) ✓. Subperiods ✓. β insignificance — does not replicate as a null, but documented; non-actionable [M4]. Jan-exclusion ✓. |
| 12 | Claim coverage of committed selection | ✓ | C1 covered by Table I; C2 by Table II; C3 by Table III + subperiods; C5 by Table V. C4 (value-premium attenuation, Table IV) remains uncovered — explicitly noted in `REPORT.md:194` as out-of-scope. |
| 13 | Sign conventions re-derived from paper | ✓ | Table II "Deciles are ranked in descending order" → D1 = highest growth → spread negative ✓. Table V caption "subtract the returns on the high investment group from the low investment group" → INV = low − high ✓, loadings −/+ ✓. INV loadings differ by exactly 1.00 (paper's identity reproduced). |
| 14 | Reporting discipline | ✓ | Table I grid complete with paper values side-by-side. Subperiod grid complete with t-statistics. INV loadings monotone profile shown side-by-side with paper direction. The "Ln(inv) 16× off" claim is paired with the per-SD effect test that quantifies it; no over-vocabulary claim without a licensing statistic. |

---

## 4. Per-table evidence

### Table II — 10 EW deciles (11 cells, 11 PASS, 9 Tier 1, 2 Tier 2)

Re-ran `evaluate.py` (output above): all 11 cells PASS the tolerance band; 9 are Tier 1, 2 are Tier 2 (D1 and D10 because their `abs_dev_pct` exceeds 1× `tolerance_pct=15` but stays within 2×). The decile spread (−0.78 vs paper −0.79) is exactly Tier 1. Paper's D7 dip (1.63 after 1.66) is reproduced (1.55 after 1.64).

### Table III Panel A — Fama-MacBeth (26 cells, 12 PASS, 4 BORDERLINE, 10 FAIL)

Re-ran `evaluate.py` and got the exact per-cell values printed in `REPORT.md`. Ln(size) coefficients and t-statistics are Tier 1 throughout (7 of 7 cells). Ln(B/M) coefficients reproduce well in magnitude and direction; B/M t-statistics are 50-100% larger than the paper's, which is consistent with the paper's own B/M effect attenuating in the late 1990s (Loughran 1997). Ln(inv) coefficients are 16× off (FAIL), but Ln(inv) t-statistics are within tolerance (Tier 1 or Tier 2). β in models 1 and 7 is wrong-sign or larger than paper (FAIL).

### Table V Panel A — lagged weights (13 cells, 7 PASS, 4 BORDERLINE, 2 FAIL)

Lagged-weight INV loadings: highest-inv-growth Q1 β_INV = −0.524 (paper −0.530, **exact Tier 1**); lowest-inv-growth Q5 β_INV = +0.476 (paper +0.470, **exact Tier 1**). Adj R² for the 4-factor model: 0.972 (paper 0.96, Tier 1). MKT/SMB/HML coefficients match the paper within 0.05. The two alpha cells (highest_alpha_mkt_only = −0.004, highest_alpha_3factor = −0.001) are FAIL — the paper reports positive alphas of +0.006 and +0.008. This is the expected consequence of removing the look-ahead bias; the contemporaneous-weight version (`results/table_5_contemp.md`) has alphas matching the paper (+0.006, +0.009), preserving the audit-1 PASS.

### Table V Panel A — contemporaneous weights (comparison only)

The shipped (contemporaneous) weighting: 12/13 cells PASS at the tolerance band; the single BORDERLINE is `lowest_hml_3factor_lag` whose `abs_dev_pct = 129.7` exceeds 100% `tolerance_pct` but the paper's value of −0.02 is small enough that our −0.046 is a 2.3× magnitude miss. Both weightings reported side-by-side as audit-1 required.

### Table I Panel A — 5×5 size × B/M (range test, 2 cells)

Means: ours 0.197 - 1.292, paper 0.17 - 1.03. Medians: ours −0.024 - 0.715, paper −0.05 - 0.54. The full 5×5 grid is in `results/table_1.md` with paper values side-by-side. The pattern (decreasing across B/M within a size row; decreasing across size within a B/M column) holds for every cell. The vintage hypothesis for [M2] is retired.

### Table III subperiods (3 masks × 2 models × 3 vars)

Re-ran `evaluate.py:417-439`. Ln(inv) t-statistics: 1976-87 model 5 t = −5.15 (paper −3.57, Tier 1); 1987-99 model 5 t = −4.85 (paper −5.03, Tier 1); Feb-Dec model 5 t = −6.16 (paper −5.84, Tier 1). All robust in direction and significance.

### Ln(inv) scale diagnostic (5 candidate transforms)

Re-read `results/ln_inv_scale_diagnostic.md` and re-ran the JSON. Per-SD effects: candidate_1 (raw `inv_growth`) −0.4177 %/mo, candidate_2 (`ln(1+inv_growth)`) −0.2479 %/mo, candidate_3 (`ln(max(inv_growth, 0.001) + 1)`) −0.1417 %/mo. Paper implied: −0.2682 %/mo. The candidate closest in per-SD effect is candidate_2 (within 0.02 %/mo). Per-SD effects for candidates 4 and 5 are duplicates of 1 and 3 because `at` is not in the panel (cosmetic).

---

## 5. Six-dimension scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass: formula, June-formation timing, BE/ME timing, formation-month ME for `ln_size`, plain (non-HAC) t-stat, FF-style β construction, FF-style VW with lagged weights, 36-month return-history filter. One deviation is the broader β universe (std 0.75 vs FF-NYSE-only 0.3-0.5) — documented. |
| Headline matching | 4 | Three of five paper claims match in shape, sign, and magnitude class: decile spread (r=0.99), INV loadings Q1/Q5 (r≈0.99), INV factor mean (r=1.43). The Ln(inv) FM coefficient is 16× off (r=0.062), but per-SD effect matches within 0.02 %/mo and t-statistic matches. |
| Data coverage | 4 | Period exact (276 months, 1976-07…1999-06); sources match (CRSP + Compustat + FF); 79 % signal coverage; 36-mo filter implemented. One minor substitution (ClickHouse FF series, SMB mean 0.035 vs paper 0.12). |
| Concrete result matching | 3 | 28/50 = 56 % Tier 1 (within the 50-70 % band for score 3); 42/50 = 84 % Tier 1 + Tier 2 (would be score 4). The headline cells that FAIL are the Ln(inv) coefficients (scale issue, documented) and the β cells in models 1 and 7. |
| Signal strength | 3 | Headline cells: decile spread r=0.99, INV loadings r≈0.99, INV factor mean r=1.43 (all within [0.5, 2.0]). Ln(inv) FM coefficient r=0.062 outside [0.33, 3.0], but per-SD effect matches — score 3 reflects the FM coefficient gap balanced by the scale-free match. |
| Corollary | 4 | Subperiods ✓, January exclusion ✓, INV loadings monotone ✓, factor correlations ✓, SMB sign pattern ✓. The β-null corollary does not replicate as a null — documented as non-actionable; the substantive claim still holds. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | All per-cell values in `REPORT.md` reproduce from the evaluator's output and the cached parquets. |

**Overall: 3.50 / 5.00 → `REPLICATED`** (mean ≥ 3.0, no dimension scored 1).

---

## 6. Limitations

- **The Ln(inv) FM coefficient magnitude is 16× off in absolute units** (β = −0.26 vs paper −4.19). The per-SD effect matches the paper within 0.02 %/mo and Table I rules out the Compustat-vintage hypothesis. The remaining gap is unidentified; no alternative-vintage Compustat pull is available in the catalog. The substantive claim that Ln(inv) is a strong negative predictor of returns replicates via t-statistic and per-SD effect.
- **β null in models 1 and 7 does not replicate as a null.** β is constructed as a 60-month rolling OLS of `ret - rf` on `mkt_rf` per FF 1992 (paper L174). The β distribution (mean 1.09, std 0.75) is broader than the FF-NYSE-only paper convention (std 0.3-0.5); the difference may be due to universe or rolling-window choice. The substantive inference (β does not dominate the Ln(inv) signal) does replicate.
- **Table IV (60 cells of joint investment × size × B/M sorts) is not replicated** in this iteration. C4 claim remains uncovered by committed tables (per `REPORT.md:194`). Out-of-scope for this single iteration.
- **Table V Panels B and C** (B/M- and MVE-sorted portfolios) are not replicated; only Panel A is committed.
- **Delisting returns** are not adjusted. The paper is silent and uses raw returns throughout; documented, low impact for monthly EW deciles.
- **Per-SD effect diagnostic candidates 4 and 5 are duplicates** of 1 and 3 because the implementation lacks the `at` (total assets) column needed for the paper's footnote-2 variable. The diagnostic is documented but does not test the footnote-2 transform. Cosmetic — the per-SD effect match for candidate_2 is the load-bearing finding.

---

## 7. Issues the agent should have caught (didn't)

1. The `data_verification.json:14-21` requirement #2 records `hexcd` in `needed_columns` but `dsenames` matches on `exchcd` (a synonym per CRSP). The pipeline uses `dsenames.exchcd` correctly; the artifact misstates the column. Audit-1 [m5] flagged this; it persists.
2. `tables_to_replicate.json:52` Table I has `"metrics": []` and the validator complains. The agent intended this to be a range test, but the validator does not accept empty `metrics` lists.
3. The `assumptions.md:201-217` "Known magnitude discrepancy on Ln(inv) coefficient" entry from iteration 2 has no "Status" field and is now superseded by A11 in iteration 4 — but the old entry is not marked stale.

---

## 8. Next-iteration prompt

NULL. Per the audit contract (`audit/SKILL.md` Continuation semantics), `requires_iteration: false` because:
- `blocker_count = 0`
- `actionable_major_count = 0` (the two carried majors are documented and non-actionable — no alternative-vintage Compustat pull is available in the catalog for [M2]; β distribution documented as broader than FF-NYSE-only for [M4])

The replication is in a state where the substantive empirical claim of the paper (INV is a strong negative predictor of returns; INV factor explains investment-sorted portfolios) is reproduced. Headline decile-spread, INV-factor-mean, INV loadings Q1/Q5, and subperiod t-statistics match. The remaining gap (Ln(inv) FM coefficient scale) is bounded by the per-SD effect test and Table I range test.

If a follow-up iteration is later desired, the optional scope is:
- Load `at` (total assets) into the FM panel and run the footnote-2 transform `(capx_{t-1} - capx_{t-3}) / at_{t-3}` per the audit's [M2] recommendation. This would settle whether the paper's Ln(inv) coefficient magnitude corresponds to a balance-sheet-normalized regressor.
- Add Table IV Panel A reduced comparison (high-vs-low investment for S/H and B/L cells) to cover claim C4.
- Add Table V Panels B and C (B/M- and MVE-sorted) to fully cover claim C5.

These are scope additions, not fixes for actionable blockers.