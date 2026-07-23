---
iteration: 3
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 3 — the_52_week_high_and_momentum_investing

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Metadata-only hygiene iteration, verified as such. Audit 2's single actionable major [M7] is CLOSED: `tables_to_replicate.json` T6 and T9 now carry `exercises_preprocessing_rules` (11 valid rule_ids each; all present in `preprocessing_rules.json`'s 27 rules / 8 categories, including the purpose-built `fm_persistence_k` for T6 and `var_52wl_measure` for T9), and `prep_validation.py` now EXITS 0 once this audit clears the log3↔audit3 layout gate (verified by the auditor: all three prep artifacts pass). No scientific artifact changed: the four baseline caches are sha256-identical to the audit-2 baselines (panel 7a5950cd…, fm_coefficients bf442e51…, fm_coefficients_gh ee066141…, strategy_returns 3b261ae7…), all seven `results/table_*.md` files are untouched (mtimes ≤ iteration 2; hit-rate blocks still read T1 12/0/0, T2 23/1/0, T3 31/15/2, T5 150/42/0, T6 73/64/55, T7 122/102/16, T9 126/58/8 — running tally 537/282/81 of 900, re-summed), and `data/` holds only the allowlisted panel.parquet + delisting_stats.json. Both audit-2 minors are addressed (REPORT.md §2 now reads 20 cols; assumptions.md carries the cache-relocation note). The five non-actionable majors N1–N5 remain documented and unchanged. The audit-2 full recomputation (all 900 cells: values, t-stats, and per-cell tiers, 0 mismatches; both abstract corollaries confirmed) therefore stands without re-derivation. The prep contract is now fully green and the replication is complete: no blockers, no actionable majors, loop terminates.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Unchanged from audit 2 (no code or cache touched — verified by sha256 and mtime): engine traces to paper lines; additive Table VI/IX extensions proven byte-identical; only documented, justified minor deviations (daily-close-max 52WH; GH 60-lag min; MG ordinal tie-break, sensitivity-cleared). |
| Headline matching | 4 | Unchanged: every shape/sign/ordering the paper claims has an artifact and reproduces, including both abstract corollaries; the only >20% headline drift (Table V pure-WH spread 0.69–0.83×; two Jan-included raw-column inversions) remains quantified, tested, and flagged. |
| Data coverage | 4 | Unchanged: exact 462-month period (1963-07..2001-12), same CRSP + FF sources, Jul-1963 universe 1,977; panel 2,387,326 × 20 (now also stated correctly in REPORT.md §2); GH rankable coverage 47% remains the one sub-60% signal, documented (N1). |
| Concrete result matching | 3 | Unchanged: 537 Tier 1 / 282 Tier 2 / 81 FAIL of 900 = 59.7% (band 3). All seven hit-rate blocks re-read this audit and identical to the audit-2 re-derivation (0 mismatches then; files untouched since). |
| Signal strength | 3 | Unchanged: corollary anchors tight (Table VI WH spread 1.11×; Table IX jt_spread 1.06×) but worst headline cell WH RA Jan-incl 0.69× and MG 1.28–1.62× keep it inside [0.5,2.0], outside a uniform 20%. |
| Corollary | 4 | Unchanged: January stability, (6,12) robustness, long-run non-reversal, and 52-week-low unprofitability all replicate; residual deviations (GH-dominance variant B, nested-loser small cells, JT/MG reversal attenuation) documented and non-actionable. |
| **Overall** | **3.67** | REPLICATED by the bright line (mean ≥ 3.0, no dimension = 1). Audit verdict PARTIAL (trustworthy, known non-actionable gaps), actionable_major_count 0, requires_iteration: false — the loop terminates. |

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

None actionable. **[M7] from audit 2 is CLOSED:**
- `preparations/tables_to_replicate.json` — `tables[5]` (T6) and `tables[6]` (T9) now carry `exercises_preprocessing_rules` with 11 rule_ids each, every id present in `preparations/preprocessing_rules.json` (27 rules, 8 categories; cross-checked programmatically: 0 invalid, 0 duplicates). T6 leads with the purpose-built `fm_persistence_k`; T9 with `var_52wl_measure` — exactly the audit-2 suggested sets.
- `uv run python scripts/prep_validation.py replications/the_52_week_high_and_momentum_investing` now exits **0** (verified by the auditor after this audit file cleared the log3↔audit3 layout gate): preprocessing_rules.json (27 rules / 8 categories) PASS, tables_to_replicate.json (7 tables, all required fields) PASS, data_verification.json (verdict ready) PASS.

### Non-actionable majors (documented; do not loop on) — all carried unchanged from audit 2

- [N1] Table VII GH-dummy side (16 FAILs; gh_spread ~0; gh_loser sign-flips in 5/8 columns). actionable: false — variant B was run and rejected by the pre-committed all-three criterion; root cause is 1970s monthly-volume missingness thinning the 60-month GH reference price; WH-side claims unaffected (16/16 Tier 1). Documented in REPORT.md §5 item 3.
- [N2] Jan-included raw-column dominance inversion (Table V (6,6)+(6,12) raw Jan-incl: JT>WH vs paper WH>JT). actionable: false — A13 rankable-only sensitivity run and rejected; classified a CRSP-2026-vintage small-cap-January effect; all ex-January and risk-adjusted columns reproduce WH>JT>MG with margin. REPORT.md §5 item 5.
- [N3] MG spreads +28–62% hot across all tables. actionable: false — industry-level cutoff variant run (0 boundary ties) and every MG cell moves the wrong way; SIC-vintage/industry-momentum composition, not cutoff mechanics. REPORT.md §5 items 1 and 6.
- [N4] Table VI JT/MG reversal attenuation (JT winner decays by k≥24; MG winner does not reverse). actionable: false — same JT/MG over-persistence as N3; the paper's 52WH non-reversal claim is unaffected and near-exact. REPORT.md §5 item 7.
- [N5] Table III nested-loser spreads ~45–55% of paper; Jan-included FM intercepts ~25–46% high. actionable: false — paper footnote 6 flags the loser cells as unbalanced and supersedes them with the regression tables, which replicate. REPORT.md §5 items 2 and 4.

### Minor (cleanup)

None open. Audit-2 [m1] closed (REPORT.md §2 now reads "2,387,326 rows × 20 cols" with g_gh_b / wh_lo_sig named). Audit-2 [m2] closed (assumptions.md header note: iteration-1/2 entries citing `data/fm_coefficients*.parquet` refer to pre-relocation paths; caches now in `results/intermediate/` with unchanged hashes; REPORT.md §6 authoritative).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Dominance / direction claim | partial | Unchanged (artifacts untouched): WH>JT>MG holds in all ex-Jan + RA Table V columns, 16/16 Table VII wh_spread Tier 1, Table III winner/middle, Table VI non-reversal, Table IX JT absorption; still inverts in the two Jan-included RAW columns (N2, tested, documented). |
| 2 | Headline-magnitude claim | partial | Unchanged: Table I WH 0.94×, Table II ex-Jan 0.96×, Table VII WH 1.02–1.09×, Table VI WH spread 1.11×, Table IX jt_spread 1.06× tight; Table V pure-WH 0.69–0.83× and MG 1.28–1.62× exceed the 20% band (documented). |
| 3 | Sample coverage ≥ 60% | partial | Unchanged: jt/mg/wh/wl signals non-null 94–99.4%; g_gh 47.4% (below 60%, documented, tied to N1). |
| 4 | Data-source choice justified | pass | Unchanged: CRSP msf/dsf/dsenames/msedelist + FF; 2026 vintage documented; daily-close-max 52WH justified (askhi quote-sign contamination). |
| 5 | prep_validation.py exit 0 | **pass** | M7 CLOSED. With this audit clearing the log3↔audit3 layout gate, the validator exits 0: preprocessing_rules (27/8), tables_to_replicate (7 tables; T6/T9 each 11 valid rule_ids, 0 invalid), data_verification (ready). T6/T9 rule_ids programmatically cross-checked against preprocessing_rules.json. |
| 6 | All committed tables have results files | pass | tables_to_replicate.json still commits T1,T2,T3,T5,T6,T7,T9 (900 metrics); every table has results/table_<n>.md (untouched since iteration 2). |
| 7 | REPORT/SUMMARY values match artifacts | pass | REPORT.md §2 col-count slip fixed (20 cols, matching the auditor-verified panel). Running tally 537/282/81 re-summed from the seven hit-rate blocks: T1 12/0/0, T2 23/1/0, T3 31/15/2, T5 150/42/0, T6 73/64/55, T7 122/102/16, T9 126/58/8 — identical to audit-2's re-derivation. |
| 8 | No orphan folders | pass | Slug root clean; data/ holds only allowlisted panel.parquet + delisting_stats.json; all 8 derived caches in results/intermediate/. |
| 9 | Diagnoses paired with fix attempts | pass | log3.md's M7 entry carries all five fields (Diagnosis / Next fix / Before: exit 1 "tables[5]/tables[6] missing exercises_preprocessing_rules" / After: exit 0 / Status: resolved); assumptions.md M1–M5 entries unchanged and complete. |
| 10 | Tier 2 within 2× magnitude | pass | Unchanged: tiers independently re-derived in audit 2 (0 mismatches); the seven table files are byte-untouched since (mtimes ≤ 20:22, iteration 3 began ≥ 20:50). |
| 11 | Corollary coverage | pass | Unchanged: all paper corollaries either verified (January stability, (6,12) robustness, long-run non-reversal, 52-week-low unprofitability) or documented non-actionable (GH-dominance, nested-loser cells, JT/MG attenuation). |

**Iteration-3 verification evidence (auditor):**
- Hashes re-verified this audit (sha256sum): `data/panel.parquet` 7a5950cd77cd1e22…, `results/intermediate/fm_coefficients.parquet` bf442e51864c5f17…, `results/intermediate/fm_coefficients_gh.parquet` ee06614114ad04fd…, `results/intermediate/strategy_returns.parquet` 3b261ae7cf0e1690… — all four byte-identical to the audit-2 baselines. The audit-2 recomputation record (all 900 cells, values + t-stats + tiers, 0 mismatches; both corollary anchors) therefore stands without re-derivation.
- Metadata-only scope confirmed by mtime: iteration-3 writes (≥ 20:50) are exactly tables_to_replicate.json, REPORT.md, assumptions.md, SUMMARY.md (replicator transcription of the audit-2 content), log3.md; every scientific artifact (seven table_*.md, panel, all eight intermediate caches) last modified ≤ 20:22 (iteration 2).
- Prep contract: `preprocessing_rules.json` = 27 rules / 8 categories (universe 1, variable 10, delisting 1, sort 5, sample 1, winsorize 1, fm 7, factor 1). T6's 11 rule_ids include `fm_persistence_k`; T9's 11 include `var_52wl_measure` and `fm_j2_7_averaging`; 13 unique rule_ids across the two, 0 invalid, 0 duplicates.
- Validator: `uv run python scripts/prep_validation.py replications/the_52_week_high_and_momentum_investing` → exit 0 after this audit file cleared the only remaining (layout) error.

## 4. Issues the agent should have caught (didn't)

None this iteration. The hygiene round was disciplined: it touched only the two prep-metadata fields and the two report-text minors, re-ran the validator to a genuine exit 0, left every verified artifact byte-identical (provable by hash), and recorded the iteration-2 lesson (always clear known layout gates before declaring the validator green) in the log. The replicator's SUMMARY.md transcription of the audit-2 assessment was appropriate given the auditor's harness-blocked write in audit 2; this audit supersedes it.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The 52-Week High and Momentum Investing" (George & Hwang 2004, JF) for slug `the_52_week_high_and_momentum_investing`. The previous run completed with audit verdict **PARTIAL**, `requires_iteration: false` (audit 3 at `replications/the_52_week_high_and_momentum_investing/logs/audit3.md`). **The replicator–auditor loop has TERMINATED — no further iteration is required.**

There are zero blockers and zero actionable majors. The last actionable item (audit-2 [M7], the missing `exercises_preprocessing_rules` on T6/T9) is closed and `prep_validation.py` exits 0. All 900 cells were independently recomputed in audit 2 (values, t-stats, and per-cell tiers; 0 mismatches) and every scientific artifact is byte-identical to those audited baselines (panel 7a5950cd…, fm_coefficients bf442e51…, fm_coefficients_gh ee066141…, strategy_returns 3b261ae7…).

**If you are nonetheless invoked (e.g., for maintenance or review):**
1. Read `logs/audit3.md` and `SUMMARY.md` — they are the current assessment.
2. Do NOT regenerate caches, re-run the FM/EW engines, or edit any `results/` artifact or `SUMMARY.md` (auditor-owned). Any number change will regress a fully verified replication.
3. The five remaining majors (N1–N5 in audit 3 §2: GH-dummy columns, Jan-included raw-column inversion, MG levels, JT/MG reversal attenuation, nested-loser small cells) are **non-actionable** — each has a failed pre-committed fix attempt on record and a documented root cause (CRSP-2026 vintage / 1970s volume missingness). Do not re-litigate them without new data.
4. If you must change a prep artifact, re-run `scripts/prep_validation.py` and confirm exit 0 before stopping.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is the model hygiene iteration. Audit 2 found exactly one actionable problem — a two-field prep-contract omission that the iteration-2 self-check had masked behind a layout gate — and this round fixed precisely that, nothing more: no engine runs, no cache regeneration, no number touched, provably so (sha256 identity on all four baselines and mtimes showing iteration-3 writes confined to the two metadata files and two report texts). The validator now exits 0 for the right reason — all three prep artifacts genuinely pass, not because a layout error short-circuited the checks — and the pipeline lesson from audit 2 (clear known gates before declaring green) is recorded in the log. The scientific record stands exactly as audited in iteration 2: 537/282/81 of 900 cells, every tier independently re-derived with zero disagreements, both abstract corollaries (long-run non-reversal; 52-week-low unprofitability) reproducing near-exactly, and each residual miss (GH columns, January-included inversion, MG heat, JT/MG attenuation, nested-loser cells) localized by failed pre-committed fix attempts to CRSP-2026-vintage and 1970s-volume-missingness causes rather than arithmetic. Binary verdict REPLICATED (overall 3.67, no dimension below 3); audit verdict PARTIAL with zero actionable majors and requires_iteration: false. The replication is complete.
