---
iteration: 2
slug: the_52_week_high_and_momentum_investing
inner_iterations: 4
worker_spawns: 4
---

# Outer Iteration 2 — Reasoning Trace

Triggered by audit 1 (logs/audit1.md): verdict PARTIAL, blocker_count 0,
actionable_major_count 6, requires_iteration true. Audit 1 independently recomputed
every raw + RA cell of Tables I/II/III/V/VII from the cached series (FF3 pulled from
ClickHouse) — all match to 4 dp — so this iteration closes SCOPE and the two deferred
diagnostics, it does not redo verified machinery.

Plan (audit's priority order):
- Inner 1: M2 — g_gh variant B (renormalized over available lags, min 24 months) +
  wh_lo_sig added to panel; re-run Table VII under B; adopt iff Tier-1 rises and
  wh_spread stays Tier 1. Anchors: gh_spread s66_raw_janexcl 0.0123 → toward 0.44;
  gh_loser s66_raw_janexcl +0.2572 → toward −0.19.
- Inner 2: M1 + M4 — Table VI (6,k,12) persistence k=12/24/36/48 (RA-only) and
  Table IX (52-week-low FM table).
- Inner 3: M3 — A13 rankable-only Table V sensitivity + per-column dominance-ordering
  rows; M5 — MG industry-level (top/bottom 6 of 20) cutoff sensitivity.
- Inner 4: M6 — relocate derived caches out of data/ (prep_validation exit 0);
  minors m1-m5; REPORT.md + this log finalized; auditor spawn (audit 2).

## Inner iteration 1: M2 — GH reference-price variant B + 52-week-low signal

**Task spec → rep-worker:** (see spawn prompt; panel gains g_gh_b and wh_lo_sig;
Table VII re-run under A vs B; recommendation with before/after grid)

**rep-worker report:** (pending)

**Replicator decision:** (pending)

--- (inner iteration 1 results) ---
**rep-worker report:**
Panel rebuilt (2,387,326 × 20: +g_gh_b, +wh_lo_sig; sha256-deterministic across
runs; rebuild guard PASS — all pre-existing columns bit-exact; Tables I/V caches
bit-identical). g_gh_b coverage: null frac 0.526 → 0.323 (by decade: 1960s
0.47→0.22, 1970s 0.58→0.48, 1980s 0.65→0.40, 1990s 0.43→0.21, 2000s 0.40→0.18);
where A and B are both defined (1,064,415 rows) values are bit-identical; B's
left tail is NOT less extreme (same −233 observation). wh_lo_sig clean: ≥1
everywhere, p50 1.29, null frac 0.006.
Table VII under B (results/table_7_variantB.md): adoption checks — (1) Tier-1
count 122 → 118 FAIL; (2) gh_spread s66_raw_janexcl 0.0123 → 0.1046 (closer to
0.44) PASS; (3) wh_spread cells stay 16/16 Tier 1 PASS (values shift ≤0.05pp by
Frisch-Waugh — joint regression; my spec's bit-identity assertion was wrong,
substantive check passes). gh_loser s66_raw_janexcl +0.257 → +0.213 (sign STILL
not flipped). Worker recommends KEEP A.
**Replicator decision:** KEEP variant A (strict-60) per the pre-registered
all-three criterion. Before/after recorded: gh_spread s66_raw_janexcl 0.012→
0.105 (toward 0.44 but 4× off); gh_loser sign unfixable by coverage alone.
Diagnosis refined: coverage composition is ONE driver (all spreads move the
right way) but the sign anomaly has an additional source — plausibly 1970s
NASDAQ volume QUALITY (zero/erratic prints feeding the turnover weights) or the
paper's unpublished GH implementation (footnote 10: they also tried weekly
turnover — their main measure may differ in ways the text does not say). M2 is
now a DOCUMENTED PARTIAL with a fix attempt on record (exit gate satisfied);
variant-B artifacts kept as evidence (table_7_variantB.md,
fm_coefficients_gh_variantB.parquet). assumptions.md A11 updated by worker.
wh_lo_sig ready for Table IX (inner iteration 2).

## Inner iteration 2: M1 (Table VI persistence) + M4 (Table IX 52-week low)

**Task spec → rep-worker:** see spawn prompt — table_6.py: (6,k,12) at
k=12/24/36/48, dummies at f=t−k−j, j=2..13, RA-only columns (FF3 intercepts,
Jan incl/excl), 12 rows × 8 cols × 4 k; table_9.py: Table V layout with FLH/FLL
dummies from wh_lo_sig replacing FHH/FHL.
**rep-worker report:** (pending)
**Replicator decision:** (pending)

--- (inner iteration 2 results) ---
**rep-worker report:**
Engine extended additively (k_offset, wl spread slot); identity proven —
fm_coefficients.parquet + fm_coefficients_gh.parquet sha256-identical after
re-running CFG_V/CFG_VII under ret_dl; table_5/7.md, panel, strategy_returns
all unchanged.
- Table VI (192 cells): 73 Tier 1 / 64 Tier 2 / 55 FAIL. THE PATTERN
  REPRODUCES: wh_spread small/positive at every k, wh dummies NEVER negative —
  all 8 wh_spread cells within ±0.05pp of paper; anchor (6,~12,12) Jan-excl
  0.1776 (t 2.39) vs paper 0.16 (1.93). JT reversal attenuated: jt_winner
  −0.068 (t −2.09) at k=12 [paper −0.18, −4.76 — sign+significance match],
  decaying to ~0 by k≥24; mg_winner does NOT reverse (stays positive) — same
  documented JT/MG over-persistence/hotness as Table V. FAILs = loser dummies
  + long-k JT/MG winner cells (vintage effect, not engine).
- Table IX (192 cells): 126 Tier 1 / 58 Tier 2 / 8 FAIL. CLAIM REPRODUCES:
  all 8 wl_spread cells insignificant (|t| < 1, paper also insignificant);
  jt_spread jumps to 1.11 Jan-excl (Table V: 0.64) vs paper 1.05 — near-exact;
  all 16 jt_spread cells Tier 1. The 8 FAILs are sign flips on economically-
  zero spreads (paper +0.01..+0.12 vs ours −0.07..−0.03, insignificant both
  sides). One OCR correction flagged (Table IX size s612_raw_janincl t-stat
  printed (3.68) read as −3.68 — dropped-minus, magnitude not guessed).
**Replicator decision:** ACCEPT both tables. M1 and M4 CLOSED: the abstract's
third claim (52WH profits do not reverse) replicates at the pattern level with
the WH cells near-exact; the 52-week-low unprofitability replicates with the
insignificance pattern exact and the JT-absorption jump near-exact. The JT/MG
reversal attenuation in Table VI is the same systematic offset documented for
Tables I/V (JT/MG dummies hot/over-persistent in this vintage) — classified
non-actionable (consistent cross-table diagnosis; no fix would move only these
cells without disturbing the verified ones). New running tally across 7 tables
(900 cells): 537 Tier 1 / 282 Tier 2 / 81 FAIL. Proceeding to inner
iteration 3 (M3 + M5 sensitivities).

## Inner iteration 3: M3 (A13 rankable-only FM sample) + M5 (MG industry-level cutoff)

**Task spec → rep-worker:** (see spawn prompt)
**rep-worker report:** (pending)
**Replicator decision:** (pending)

--- (inner iteration 3 results) ---
**rep-worker report:**
Engine extended additively (rankable_only flag, industry-cutoff ranking);
regression gates prove official path bit-identical (CFG_V re-run == on-disk
fm_coefficients.parquet bf442e51…; tables_1_3 re-run == strategy_returns).
- M3 rankable-only: restricted avg sample 4,361/(t,j) (90.8% retained).
  s66_raw_janincl wh_spread 0.4896 → 0.4831 (paper 0.65), jt_spread 0.5295 →
  0.5418 (paper 0.38) — inversion PERSISTS; restriction additionally inverts
  s66_ra_janincl and s612_ra_janincl (WH 0.586 vs JT 0.587 etc.). Adoption
  checks: C1 FAIL, C2 PASS, C3 FAIL (150→144 Tier 1). Recommendation: KEEP.
- M5 industry-level cutoff: 0/467 boundary ties (ordinal tie-break irrelevant).
  mg_w_minus_l 0.5747 → 0.5954 (paper 0.45 — FARTHER); FM mg_spread worse in
  ALL 8 columns. Adoption: C1 FAIL, C2 PASS (MG weakest everywhere under both).
  Recommendation: KEEP. MG offset = SIC-vintage/industry-momentum-hotness, not
  cutoff mechanics.
- Identity hashes: fm_coefficients.parquet, table_5.md, table_1.md,
  strategy_returns.parquet, panel.parquet ALL unchanged.
**Replicator decision:** ACCEPT both recommendations — KEEP official sample
and official MG sort. M3 and M5 CLOSED as tested-and-documented non-actionables:
the Jan-included raw-column inversion and the MG overshoot are CRSP-2026-
vintage effects — both targeted hypotheses were run to completion with
pre-committed adoption criteria, both failed to move the numbers toward the
paper, so no further iteration can be justified (documented partials per audit
stop-conditions). New artifacts: table_5_sensitivity_rankable.md,
table_1_sensitivity_mg.md (+ caches). assumptions.md: two five-field entries.
Proceeding to inner iteration 4 (M6 hygiene + minors → prep_validation exit 0
→ audit 2).

## Inner iteration 4: M6 validator hygiene + minors (m2 annotations)

**Task spec → rep-worker:** relocate 8 derived caches from data/ to
results/intermediate/ (keep panel.parquet + delisting_stats.json in data/),
update all readers/writers, add "Tier 2 ⚠ (|r|>2)" annotations to table-md
writers, regenerate, prove prep_validation.py exits 0, report new hashes.
**rep-worker report:**
All 8 caches moved to results/intermediate/, each byte-identical pre-move vs
after-regeneration (sha256 table in report; fm_coefficients bf442e51…,
fm_coefficients_gh ee066141…, strategy_returns 3b261ae7…, + 5 more). Worker
surfaced and repaired a real trap: tables_1_3/5/7.py main() defaults used ret
while the official (ratified) artifacts are ret_dl-based — running them
directly had overwritten the official caches with ret-based versions during
the relocation; detected via the engine identity guard, regenerated under
ret_dl (hashes back to the audited baselines), and driver defaults changed to
ret_dl so plain `python tables_5.py` reproduces official artifacts. panel
unchanged (7a5950cd…). Annotations: 131 Tier-2⚠ flags across the 7 tables;
normalized diff shows 0 non-blank residual lines (values/t-stats/tier
assignments untouched). plots.py re-run OK from the new cache location.
prep_validation.py: the ONLY remaining error is the log2↔audit2 audit gate
(expected mid-iteration; cleared by the auditor spawn below).
**Replicator decision:** ACCEPT. M6 and m2 CLOSED; m1 (orphan tree) and m4
(log1 linearization) and m5 (caption) done by the replicator directly. Inner
iteration 4 complete — all six audit-1 majors (M1-M6) and all five minors
addressed. Proceeding to Step 4: auditor spawn for audit 2.
