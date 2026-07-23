---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 2 — the_52_week_high_and_momentum_investing

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Five of the six audit-1 majors (M1–M5) and all five minors (m1–m5) are addressed and independently verified, and the scope is now seven tables / 900 cells. I recomputed every value, t-stat, AND per-cell tier of the four Fama–MacBeth tables (V, VI, VII, IX = 816 cells) from the relocated coefficient caches with FF3 pulled read-only from ClickHouse (0 mismatches) and recomputed Tables I/II from the strategy-returns cache (exact). The two added abstract corollaries reproduce: 52-week-high non-reversal (Table VI, all 8 wh_spread cells within ±0.05pp; anchor (6,~12,12) ex-Jan 0.1776 t 2.39 vs paper 0.16 t 1.93) and 52-week-low unprofitability (Table IX, all 8 wl_spreads insignificant, JT absorption 1.11 vs 1.05). The four pre-registered sensitivities were run against pre-committed adoption criteria and all failed to move the numbers toward the paper, so the residual gaps are documented, tested, and NON-actionable. The audited Table V/VII caches are byte-identical to iteration 1 (sha256 re-verified). **However, audit-1 [M6] is NOT fully closed:** the cache relocation is done (data/ is clean), but `prep_validation.py` STILL exits 1 — the two new tables T6 and T9 in `tables_to_replicate.json` are missing the required `exercises_preprocessing_rules` field. This error was masked by the log2↔audit2 layout error during the iteration-2 self-check, so the run was reported green prematurely. One actionable major remains; the loop needs one short fix iteration.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Engine extended ADDITIVELY for Table VI (k_offset) and Table IX (wl slot) with the official path proven byte-identical (sha256 bf442e51…/ee066141… re-verified by auditor); all formulas/timing/universe/FF3-RA/FM-t conventions still trace to paper lines; only documented minor deviations (daily-close-max 52WH; GH 60-lag min; MG ordinal tie-break — the last now sensitivity-tested and cleared as not the driver). No methodology bug. |
| Headline matching | 4 | Every shape/sign/ordering the paper claims now has an artifact and reproduces, including the two abstract corollaries (non-reversal near-exact; 52-low insignificant near-exact); Table I WH 0.42/0.45 (0.94x), Table VII WH 16/16 Tier 1 (1.02–1.09x), Table V ex-Jan + RA ordering WH>JT>MG with margin. Residual: Table V pure-WH spread 0.69–0.83x and the WH-vs-JT inversion in the two Jan-included raw columns (M3-tested, unrecoverable vintage effect) — the only >20% headline drift, now quantified and flagged, not silenced. |
| Data coverage | 4 | Exact 462-month period (1963-07..2001-12), same CRSP + FF sources, Jul-1963 universe 1,977; panel now 2,387,326 × 20 (540 months, 0 dup keys) with wh_lo_sig (null frac 0.006, coverage = wh_sig_dc) and g_gh_b added. GH rankable coverage 38–62% (1970s volume missingness) remains the one sub-60% signal, documented and tied to the broken GH columns. |
| Concrete result matching | 3 | 537 Tier 1 / 282 Tier 2 / 81 FAIL of 900 = 59.7% Tier 1 (band 3). Aggregate fell from 65.5% (516) as Table VI's RA-only persistence grid is 73/192 (38% — loser dummies + long-k JT/MG winner cells), offset by Table IX 126/192 (66%). All tiers independently re-derived: 0 mismatches across V/VI/VII/IX. |
| Signal strength | 3 | New corollary anchors are tight (Table VI WH spread 1.11x; Table IX jt_spread 1.06x), but the worst headline cell is unchanged — Table V RA Jan-incl WH spread 0.59/0.86 = 0.69x — and MG runs 1.28–1.62x; all within [0.5,2.0] (band 3), none within a uniform 20%. |
| Corollary | 4 | January stability + (6,12) robustness replicate; the two previously-missing abstract corollaries now computed and replicate (long-run non-reversal; 52-week-low unprofitability). Residual documented deviations: GH-dominance-over-JT/MG (variant B tested, not reproduced — data-coverage limit), nested-loser small cells (paper footnote 6), JT/MG reversal attenuation (same vintage offset). |
| **Overall** | **3.67** | REPLICATED by the bright line (mean ≥ 3.0, no dimension = 1). Audit verdict PARTIAL with one actionable major (validator gate), requires_iteration: true. |

## 2. Issues by severity

### Blockers (must fix)

None. Every committed cell I recomputed from the relocated caches reproduces to 4 dp (values and t-stats) and every per-cell tier re-derives exactly (0 mismatches across the 816 FM cells of Tables V/VI/VII/IX plus the 48+24 EW cells of Tables I/II). The replication science is sound; the remaining issue is a prep-contract metadata field, not a number.

### Major (should fix)

- [M7] `prep_validation.py` STILL exits 1 — audit-1 [M6] not fully closed. The cache relocation is verified done (data/ holds only allowlisted panel.parquet + delisting_stats.json; all 8 derived caches in results/intermediate/), but the two new tables committed this iteration are missing a required prep-contract field, so the validator's "exit 0" goal is not met. The iteration-2 self-check reported the validator green because the log2↔audit2 layout error masked this artifact error; once this audit clears the layout gate, the artifact error surfaces.
  - File: preparations/tables_to_replicate.json — `tables[5]` (id T6) and `tables[6]` (id T9) lack `exercises_preprocessing_rules` (required by scripts/prep_validation.py:56 `REQUIRED_TABLE_FIELDS`; raised at :318-320). The other five tables (T1,T2,T3,T5,T7) all carry this field; T6/T9 do not.
  - Likely cause: when T6/T9 were transcribed into the prep contract this iteration, the `exercises_preprocessing_rules` key was omitted; the validator was run while the layout error short-circuited the artifact checks, so the omission was never seen.
  - Specific fix: add an `exercises_preprocessing_rules` list of valid rule_ids to both T6 and T9 (rule_ids must exist in preparations/preprocessing_rules.json, which has 27; the validator cross-checks them at scripts/prep_validation.py:327-330). Natural choices: T6 (persistence) → `fm_persistence_k` (purpose-built for the (6,k,12) gap) plus the FM rules it shares with Table V (`fm_skip_month`, `fm_regression_controls`, `fm_averaging_j`, `fm_dummy_definitions`, `fm_percent_units`, `factor_risk_adjustment`, `var_52wh_measure`, `var_jt_past_return`, `var_mg_signal`, `var_size`); T9 (52-week-low, Table V layout) → `var_52wl_measure` (purpose-built) plus the same FM/var block. Then re-run `python scripts/prep_validation.py replications/the_52_week_high_and_momentum_investing` and confirm exit 0 (no other artifact errors are queued — preprocessing_rules.json (27 rules/8 categories) and data_verification.json (verdict ready) already pass).
  - actionable: true

### Non-actionable majors (documented; do not loop on)

- [N1] Table VII GH-dummy side (16 FAILs; gh_spread ~0; gh_loser sign-flips in 5/8 columns). actionable: false — the pre-committed coverage-relaxation fix (variant B) was RUN (results/table_7_variantB.md): it moved all 8 gh_spreads toward the paper (s66_raw_janexcl 0.012→0.105 vs 0.44, auditor-verified) but could not flip the gh_loser sign (+0.257→+0.213) and lowered Tier-1 (122→118), so strict-60 stays official per the pre-committed all-three criterion. Root cause is 1970s monthly-volume missingness thinning the 60-month GH reference price under either variant; the WH-side claims are unaffected (16/16 Tier 1).
- [N2] Jan-included raw-column dominance inversion (Table V (6,6)+(6,12) raw Jan-incl: JT>WH vs paper WH>JT). actionable: false — the pre-registered A13 rankable-only sensitivity was RUN (results/table_5_sensitivity_rankable.md, auditor-verified): restricting to stocks rankable on all three signals (90.8% retained) leaves the inversion intact (WH 0.483 vs JT 0.542) and costs 6 Tier-1 cells, so it is not an un-rankable-dilution artifact; classified an all-exchange/2026-vintage small-cap-January effect. All ex-January and risk-adjusted columns reproduce WH>JT>MG with margin.
- [N3] MG spreads +28–62% hot across all tables. actionable: false — the industry-level top/bottom-6 cutoff variant was RUN (results/table_1_sensitivity_mg.md, auditor-verified): 0 boundary ties (ordinal tie-break irrelevant) and every MG cell moves the WRONG way (mg_w_minus_l 0.5747→0.5954 vs 0.45; FM mg_spread 0.3804→0.4098 vs 0.25), so the offset is SIC-vintage/industry-momentum composition, not cutoff mechanics. MG remains the weakest strategy everywhere.
- [N4] Table VI JT/MG reversal attenuation (JT winner reverses at k=12 but decays by k≥24; MG winner does not reverse). actionable: false — same JT/MG over-persistence as N3; the paper's claim (52WH non-reversal) is unaffected and near-exact.
- [N5] Table III nested-loser spreads ~45–55% of paper; Jan-included FM intercepts ~25–46% high. actionable: false — carried from audit-1 (N1/N2 there); paper footnote 6 flags the loser cells as unbalanced and supersedes them with the regression tables, which replicate; intercepts driven by stronger small-cap January in this vintage (ex-Jan intercepts within ~18%).

### Minor (cleanup)

- [m1] REPORT.md §2 states the panel is "2,387,326 rows × 18 cols" but the iteration-2 rebuild added two columns (g_gh_b, wh_lo_sig) — the panel is now 20 cols (auditor-verified: 2,387,326 × 20, 540 months, 0 dup keys). log2.md records the correct count. Specific fix: update "18 cols" → "20 cols" in REPORT.md §2.
- [m2] Six iteration-2 notes in preparations/assumptions.md (M1–M5 entries) still reference the pre-relocation cache path `data/fm_coefficients*.parquet`; the caches now live in `results/intermediate/` (REPORT.md §6 is correct). Historical point-in-time log entries, so cosmetic. Specific fix: optionally note the relocation in those entries (REPORT.md §6 already points to results/intermediate/).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Dominance / direction claim | partial | WH>JT>MG holds in 6/8 Table V columns (all ex-Jan + both RA), 16/16 Table VII wh_spread Tier 1, Table III winner/middle, and now Table VI (non-reversal) + Table IX (JT absorption); STILL inverts in the two Jan-included RAW columns — now M3-tested and documented (N2). |
| 2 | Headline-magnitude claim | partial | Table I WH 0.94x, Table II ex-Jan 0.96x, Table VII WH 1.02–1.09x, Table VI WH spread 1.11x, Table IX jt_spread 1.06x (all tight); Table V pure-WH 0.69–0.83x and MG 1.28–1.62x exceed the 20% band (unchanged, documented). |
| 3 | Sample coverage ≥ 60% | partial | jt/mg/wh/wl signals non-null 94–99.4%; g_gh 47.4% (below 60%, documented, tied to N1). |
| 4 | Data-source choice justified | pass | CRSP msf/dsf/dsenames/msedelist + FF; 2026 vintage documented; msf.vol in hundreds verified; daily-close-max 52WH justified (askhi quote-sign contamination). |
| 5 | prep_validation.py exit 0 | **fail** | The log2↔audit2 layout gate is cleared by this audit, AND the parquet allowlist is fixed (data/ clean) — but the artifact check still fails: T6/T9 missing required `exercises_preprocessing_rules` (M7). Exit code 1. |
| 6 | All committed tables have results files | pass | tables_to_replicate.json commits T1,T2,T3,T5,T6,T7,T9 (12/24/48/192/192/240/192 = 900 metrics); every table has results/table_<n>.md. T6/T9 paper anchors transcribed correctly (spot-verified against content.md L1007-1268 / L2178-2444). |
| 7 | REPORT/SUMMARY values match artifacts | pass | All numeric claims I checked reproduce from the caches; the cumulative_wl.png caption is now honest (MG>JT>WH, m5 fixed). One descriptive slip: REPORT.md §2 "18 cols" vs actual 20 (m1). |
| 8 | No orphan folders | pass | Nested empty `replications/<slug>/` tree deleted (m1 from audit-1 cleared); no literal-brace dirs. |
| 9 | Diagnoses paired with fix attempts | pass | assumptions.md M1–M5 entries all carry the five fields (Diagnosis/Next fix/Before/After/Status) with auditor-verified Before/After metrics; the four pre-registered fixes were RUN, not skipped. |
| 10 | Tier 2 within 2× magnitude | pass (annotated) | Tiering is internally consistent and independently re-derived (0 mismatches); the 131 Tier-2 cells with |ratio|>2 now carry "Tier 2 ⚠" flags (m2 from audit-1 cleared). |
| 11 | Corollary coverage | pass | Long-run non-reversal (Table VI) and 52-week-low (Table IX) now computed and reproduce; GH-dominance computed, tested (variant B), documented non-actionable; nested-loser partial (paper-acknowledged). No corollary silently skipped. |

**Recomputation evidence (auditor, from relocated caches + ClickHouse FF3):**
- Tables I/II from `strategy_returns.parquet` (sha256 3b261ae7…, n=462): Table I jt_wl 0.4720 t 2.2505, mg_wl 0.5747 t 4.5364, wh_wl 0.4233 t 1.7568; Table II Panel A wh_wl 1.1812 t 6.5247, Panel B jt_wl −6.2650 t −4.3012 — exact to 4 dp (W−L difference series equals mean(w)−mean(l)).
- Table V from `fm_coefficients.parquet` (sha256 bf442e51…): all 96 (value,t) pairs recomputed (raw = c-series mean/t; RA = OLS intercept/t of c on FF3-in-percent), max |Δ| = 5.0e-05 — exact. Per-cell tiers re-derived from targets' tol% with the repo tier rule (TOL=1e-12): 150/42/0, 0 mismatches of 192.
- Table VII from `fm_coefficients_gh.parquet` (sha256 ee066141…): all 120 (value,t) pairs, max |Δ| = 4.9e-05 — exact.
- Table VI from `fm_coefficients_persist.parquet` (RA-only, all 8 columns k12/24/36/48 × Jan incl/excl): 96 (value,t) pairs, max |Δ| = 5.0e-05; tiers re-derived 73/64/55, 0 mismatches of 192. WH non-reversal anchor confirmed (k12_janexcl wh_spread 0.1776 t 2.39).
- Table IX from `fm_coefficients_low.parquet`: 96 (value,t) pairs, max |Δ| = 5.0e-05; tiers re-derived 126/58/8, 0 mismatches of 192. wl_spread |t|<1 in all 8 columns; jt_spread s66_raw_janexcl 1.1106.
- Sensitivity caches independently recomputed: variant B gh_spread s66_raw_janexcl 0.1046 / gh_loser +0.2126 / wh_spread 0.5238 (fm_coefficients_gh_variantB); rankable-only wh_spread 0.4831 / jt_spread 0.5418 / mg_spread 0.3830 s66_raw_janincl (fm_coefficients_rankable); MG-industry mg_spread 0.4098 s66_raw_janincl (fm_coefficients_mg_ind) — all match the sensitivity .md files and the assumptions.md After-metrics.
- Running tally 537/282/81 of 900 re-summed from the seven hit-rate blocks (T1 12/0/0, T2 23/1/0, T3 31/15/2, T5 150/42/0, T6 73/64/55, T7 122/102/16, T9 126/58/8).
- Hashes re-verified: panel.parquet 7a5950cd…, fm_coefficients bf442e51…, fm_coefficients_gh ee066141…, strategy_returns 3b261ae7… (the audited Table V/VII caches are byte-identical to iteration 1).
- Validator: `prep_validation.py` exit 1 — preprocessing_rules.json (27 rules/8 categories) PASS, data_verification.json (verdict ready) PASS, but tables_to_replicate.json FAILS with 2 errors: tables[5] (T6) and tables[6] (T9) missing `exercises_preprocessing_rules`.

## 4. Issues the agent should have caught (didn't)

1. **The validator was not actually green.** The iteration-2 self-check (log2.md inner 4) states "prep_validation.py: the ONLY remaining error is the log2↔audit2 audit gate." That is false: the layout error short-circuited the artifact checks, masking that T6 and T9 were committed to `tables_to_replicate.json` WITHOUT the required `exercises_preprocessing_rules` field (present on all five original tables). Running the validator after clearing the layout gate (which this audit does) reveals exit 1. A careful check would clear the known gate first, then re-run to catch what surfaces. This is the one substantive miss of the iteration (M7).
2. REPORT.md §2 still reads "18 cols" after the panel grew to 20 (g_gh_b, wh_lo_sig); log2.md has the correct count (m1).
3. The five iteration-2 assumptions.md entries cite the pre-relocation cache path `data/fm_coefficients*.parquet`; the M6 move to `results/intermediate/` happened the same iteration but the earlier notes were not back-referenced (m2; REPORT.md §6 is correct, so low-stakes).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The 52-Week High and Momentum Investing" (George & Hwang 2004, JF) for slug `the_52_week_high_and_momentum_investing`. The previous run completed with audit verdict **PARTIAL**, `requires_iteration: true` (audit 2 at `replications/the_52_week_high_and_momentum_investing/logs/audit2.md`). Read that audit first.

**This is a short hygiene iteration — the science is DONE and fully verified.** Audit 2 independently recomputed every value, t-stat, and per-cell tier of all seven tables (900 cells; 0 mismatches) and confirmed both added abstract corollaries (Table VI non-reversal, Table IX 52-week-low) reproduce. All audit-1 majors M1–M5 and minors m1–m5 are closed. **Do NOT re-run any engine, regenerate any cache, or touch any table number** — the caches are byte-identical to the audited baselines and the loop will regress if you do.

## Issues to address (priority order)

### [M7] — MAJOR — make `prep_validation.py` actually exit 0 (residual of audit-1 M6)
The cache relocation is done and data/ is clean, but the validator STILL exits 1: the two new tables T6 and T9 in `preparations/tables_to_replicate.json` are missing the required `exercises_preprocessing_rules` field (every other table has it). The iteration-2 self-check missed this because the log2↔audit2 layout error masked the artifact error.

**Specific fix:**
1. In `preparations/tables_to_replicate.json`, add an `exercises_preprocessing_rules` array of valid rule_ids to the T6 entry (`tables[5]`) and the T9 entry (`tables[6]`). Valid rule_ids are the 27 in `preparations/preprocessing_rules.json` (the validator cross-checks them). Purpose-built ids exist: `fm_persistence_k` for Table VI and `var_52wl_measure` for Table IX.
   - Suggested T6: `["fm_persistence_k", "fm_skip_month", "fm_regression_controls", "fm_averaging_j", "fm_dummy_definitions", "fm_percent_units", "factor_risk_adjustment", "var_52wh_measure", "var_jt_past_return", "var_mg_signal", "var_size"]`
   - Suggested T9: `["var_52wl_measure", "fm_skip_month", "fm_regression_controls", "fm_j2_7_averaging", "fm_averaging_j", "fm_dummy_definitions", "fm_percent_units", "factor_risk_adjustment", "var_jt_past_return", "var_mg_signal", "var_size"]`
   (Adjust to taste, but every id must exist in preprocessing_rules.json.)
2. Re-run `python scripts/prep_validation.py replications/the_52_week_high_and_momentum_investing` and confirm **exit 0**. (preprocessing_rules.json and data_verification.json already pass; the T6/T9 field is the only remaining artifact error.)

### Minors (cleanup, optional)
- [m1] REPORT.md §2: change "2,387,326 rows × 18 cols" → "× 20 cols" (iteration-2 rebuild added g_gh_b and wh_lo_sig; log2.md already records 20).
- [m2] Optional: back-reference the cache relocation (data/ → results/intermediate/) in the five iteration-2 assumptions.md entries (REPORT.md §6 is already correct).

## Iteration discipline reminders

- **Do NOT regenerate caches or re-run the FM/EW engines.** The numbers are final and byte-identical to the audited baselines (panel 7a5950cd…, fm_coefficients bf442e51…, fm_coefficients_gh ee066141…, strategy_returns 3b261ae7…). Only edit the prep JSON (and optionally the two report-text minors).
- Re-run `scripts/prep_validation.py` after the edit and confirm exit 0 — that is the exit gate for this iteration.

## Deliverables for this iteration

- `preparations/tables_to_replicate.json` — T6 and T9 gain `exercises_preprocessing_rules` (M7).
- Optional: REPORT.md §2 col-count fix (m1); assumptions.md relocation back-reference (m2).
- Do NOT edit SUMMARY.md (auditor-owned) or any results/ artifact.

## Stop conditions

- `prep_validation.py` exits 0 → the next audit clears M7 and updates SUMMARY.md; the replication is complete (no blockers, no other actionable majors).
- If anything in the fix touches a number, STOP — you have drifted out of scope; revert and only edit the prep JSON.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This iteration did almost everything an outer iteration is for, and did it cleanly: it left the verified machinery untouched (byte-identity of the Table V/VII caches re-confirmed by sha256 and by recomputing all 216 cells), closed the two genuine scope gaps (the paper's third abstract claim, long-run non-reversal, and the 52-week-low robustness) with tables whose cells I recompute to 4 dp and whose tiers I re-derive with zero disagreements, and ran the four pre-registered sensitivities to honest, pre-committed conclusions rather than declaring victory or silently dropping them. The single blemish is procedural: the replicator reported `prep_validation.py` green on the strength of "the only remaining error is the audit gate," but that self-check was run while the layout error was still masking the artifact checks — and once I cleared the gate, the validator surfaced that T6 and T9 were committed without the required `exercises_preprocessing_rules` field. It is a two-line prep-JSON fix, not a science problem, which is exactly why this is PARTIAL-with-one-actionable-major rather than FAIL: every number is trustworthy and the bright-line verdict is REPLICATED, but the structural gate the pipeline relies on is not yet satisfied. The lesson for the pipeline is to always clear a known layout gate and re-run the validator before declaring it green, since layout errors short-circuit the artifact checks. The residual scientific misses (GH side, Jan-included inversion, MG heat, JT/MG reversal attenuation) are a CRSP-2026-vintage / 1970s-volume-missingness story, not an arithmetic one — they recur consistently across two independent methodologies (EW sorts and FM dummies), which is the strongest possible localization, and each now has a failed fix attempt on record. Binary verdict REPLICATED; audit verdict PARTIAL with requires_iteration: true (one prep-contract field).
