---
iteration: 2
slug: seasonality_international_evidence
inner_iterations: 2
worker_spawns: 2
---

# Outer Iteration 2 — Reasoning Trace

Audit 1 verdict: PARTIAL, requires_iteration=true, 0 blockers, 4 actionable
majors (M1 computable corollaries Tables 4/5; M2 Table 11 correlations +
Table 12 quintiles; M3 dual-scheme tier evaluation; M4 committed sensitivity
battery), 7 minors, 1 non-actionable major (M5 French international value
factors unavailable). Audit independently verified the panel, the Table
1/2/3/7 computations, and the A13 battery direction — no methodology changes
this iteration; all work is additive.

Prep extension (replicator): tables_to_replicate.json extended with T4 (312
cells, calendar months), T5 (144, size groups), T11 (11 committed named
correlation cells + full matrices as supplementary), T12 (240,
quintiles/triciles). Paper values parsed directly from content.md with
verified line numbers; internal consistency check (5−1 = Q5−Q1) confirms the
parse. Total committed cells now 1,613. prep_validation.py exits 0.

## Inner iteration 1: M1 + M2 corollary tables

**Task spec → rep-worker:** src/compute_t4_t5.py (Table 4 calendar-month
EW Panel A spreads; Table 5 monthly 30/40/30 USD size groups, intracountry +
intercountry breakpoints, Y1/Y23/Y45 rows) and src/compute_t11_t12.py
(Table 11 per-country annual-strategy correlation matrices; Table 12
quintile/tricile EW Panel A sorts), all from data/panel.parquet, emitting
cells_t4/t5/t11/t12.json + table md files.

**rep-worker report:** src/compute_t4_t5.py (imports the verified compute_t3
engine) and src/compute_t11_t12.py (imports compute_t7 + compute_t3
mechanics). Engines re-validated: T4 monthly series reproduce cells_t3.json
EW Panel A means to 0.00; T11 signals bit-identical to compute_t7; T5
from-scratch reimplementation matches to 0.00. Coverage exact: cells_t4 312,
cells_t5 144, cells_t11 11, cells_t12 240.
Key results — T4: y23 nonannual negative 11/12 months, Feb-Dec -0.0126
(t -4.64) vs paper -0.0122 (-6.15) ✓; y23 difference positive 10/12 months,
Feb-Dec +0.0113 (t 3.77) vs +0.0155 (7.12) ✓; annual rows still weak
(5/12 positive, Feb-Dec ≈ 0) — same documented annual-strategy attenuation.
T5: y23 difference positive in ALL 6 size columns (46-89% of paper);
nonannual y23/y45 negative 6/6; y45 annual inter_large +0.0030 (1.80) vs
+0.0031 (1.73) near-exact. T11: mean pairwise ρ = 0.111 (y1) / 0.052 (y23) /
0.015 (y45) — abstract's low-correlation claim holds; FRA-DEU y1 0.39 vs
paper 0.43; one NLD-GBR y23 outlier (0.90, single-month penny-stock driven;
leave-one-month ρ = -0.08) flagged, no committed metric uses it. T12: 11/12
rows keep decile signs (sole exception y23 annual, all bins noise-level);
long-horizon spreads within ±15% of the paper; 148/240 cells Tier 1.

**Replicator decision:** ACCEPT. M1 and M2 closed (Table 6 deferred as A14 —
panel lacks price/volume; audit-permitted option). Corollary evidence
strengthens the replication: calendar/size/breadth/correlation/bin-count
robustness claims all hold for the long-horizon rows; annual-row attenuation
is the single systematic deviation, consistent across every table.

## Inner iteration 2 — evaluation

**rep-worker report:** src/evaluate.py — dual-scheme tiers over all 1,613
committed cells: repo rules 613 T1 / 713 T2 / 287 FAIL (82% sign-consistent);
rubric rules 613 / 299 / 701 (57% T1+T2). All 9 audit-1 anchor assertions
pass exactly. src/sensitivity_y1.py — pinned-semantics battery: baseline
-0.0053 (t -1.62, matches engine to 1e-12), drop-Canada +0.0002, |ret|>100%
+0.0058 (2.26), |ret|>60% +0.0149 (6.79), top-50% cap +0.0066 (1.77);
secondary semantics +0.0049/+0.0117 documented alongside.

**Replicator decision:** ACCEPT. M3 and M4 closed. REPORT.md updated:
dual-scheme evaluation table (8 tables), new §4.5-4.8 corollary sections,
§6.3 committed battery numbers, and all seven minors fixed (m1 firm-month
counts, m2 lag-3 miss acknowledged, m3 Canada Y45 reworded, m4 extreme-return
count, m5 qunit removed from data_verification.json, m6 breadth claim
qualified + log1 correction appended, m7 covered by evaluate.py). A14 added
(Table 6 deferred).

## Summary (iteration 2)

All four actionable majors and all seven minors from audit 1 addressed and
verified. Committed cells grew 906 → 1,613 (Tables 4/5/11/12 added).
Tier 1 count grew 319 → 613. Non-actionable M5 (French international value
factors) remains documented in REPORT §8. Ready for audit 2.
