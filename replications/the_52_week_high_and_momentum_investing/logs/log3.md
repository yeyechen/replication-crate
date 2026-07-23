---
iteration: 3
slug: the_52_week_high_and_momentum_investing
inner_iterations: 0
worker_spawns: 0
---

# Outer Iteration 3 — Reasoning Trace (hygiene round)

Triggered by audit 2 (logs/audit2.md): verdict PARTIAL, blocker_count 0,
actionable_major_count 1 (M7), requires_iteration true. Audit 2 independently
recomputed all 900 cells (values, t-stats, AND per-cell tiers) with zero
mismatches and confirmed both abstract corollaries; the science is final and
byte-identical to the audited baselines. This iteration is a metadata-only
hygiene round — no engine, no cache, no number is touched.

## M7 fix — exercises_preprocessing_rules for T6/T9

**Diagnosis:** tables_to_replicate.json entries T6 and T9 (added by the
iteration-2 worker transcription) lacked the required
`exercises_preprocessing_rules` field; the iteration-2 self-check missed it
because the log2↔audit2 layout error short-circuited the validator's artifact
checks (lesson recorded: always clear known layout gates and re-run the
validator before declaring it green).
**Next fix:** add valid rule_id arrays to both entries — T6: fm_persistence_k +
the FM block (fm_skip_month, fm_regression_controls, fm_averaging_j,
fm_dummy_definitions, fm_percent_units, factor_risk_adjustment, var_52wh_measure,
var_jt_past_return, var_mg_signal, var_size); T9: var_52wl_measure + the same FM
block + fm_j2_7_averaging. All 13 referenced rule_ids verified present in
preprocessing_rules.json (27 rules).
**Before metric:** prep_validation.py exit 1 ("tables[5]/tables[6] missing
exercises_preprocessing_rules").
**After metric:** prep_validation.py exit 0 — all four prep artifacts pass
(preprocessing_rules 27 rules/8 categories; tables_to_replicate 7 tables;
data_verification verdict ready). Executed by the replicator directly
(prep-contract metadata, replicator-owned).
**Status:** resolved.

## Minors

- m1 (audit 2): REPORT.md §2 panel dims corrected 18 → 20 cols (the two
  iteration-2 columns g_gh_b and wh_lo_sig named).
- m2 (audit 2): assumptions.md header note added — iteration-1/2 entries citing
  data/fm_coefficients*.parquet refer to the pre-relocation paths; caches now in
  results/intermediate/ with unchanged hashes (REPORT.md §6 inventory is
  authoritative).
- SUMMARY.md: transcribed the auditor's iteration-2 content verbatim (the
  auditor's own SUMMARY.md write was harness-blocked in audit 2 and the content
  was returned for transcription; audit 3 supersedes it).

## Deliverables

- preparations/tables_to_replicate.json — T6/T9 exercises_preprocessing_rules added.
- REPORT.md §2 fix; assumptions.md relocation note.
- prep_validation.py: EXIT 0 (verified).
- No scientific artifact touched: panel 7a5950cd…, fm_coefficients bf442e51…,
  fm_coefficients_gh ee066141…, strategy_returns 3b261ae7…, all seven
  results/table_*.md unchanged.

Proceeding to Step 4: auditor spawn (audit 3) to clear M7 and update SUMMARY.md.
