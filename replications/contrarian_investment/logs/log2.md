---
iteration: 2
slug: contrarian_investment
inner_iterations: 1
worker_spawns: 1
---

# Outer Iteration 2 — Reasoning Trace

Triggered by audit 1 (`logs/audit1.md`): verdict PARTIAL,
`requires_iteration: true`, 0 blockers, 2 actionable majors (M1
self-report drift; M2 Table VII window), plus minors m1 (A15
wording), m2 (§5b enumeration), m3 (optional footers — skipped as
non-load-bearing). The audit independently re-derived the per-cell
classification engine from scratch (1,167/57/66, zero disagreement)
and re-ran all six table scripts to byte-identical output.

## Inner iteration 6: M1 (replicator) + M2 (rep-worker)

**Task spec → rep-worker (M2 only; M1 owned by replicator):**
Bound src/table7.py to in-horizon cohorts: WIN_HI 23944 (Apr 1995)
→ 23932 (Apr 1994, last month any cohort is within Year +5); add
assertion mnum <= (fy+5)*12+4 per classified month; recompute the
semantic 25/88/122/25 partition over the bounded window; re-emit
table_7.md + table_VII_cells.json; run ONLY table7.py and verify the
other 7 cells JSONs byte-identical (md5); report before/after counts,
month shifts, W25/N88 spreads, new tally.

**rep-worker report (M2):**
- Diagnosis confirmed: ~12 post-Apr-1994 months reused the 1989
  cohort at +5.5/+6 yrs; W_25 (max month Sep 1981) clean.
- Fix applied: WIN_HI=23932; assertion passes (0 violations);
  semantic partition over 312 months (124 neg / 188 pos) →
  25/88/122/25 + 52 unclassified (was 64); window note added to
  table_7.md.
- Bonus latent bug found & fixed: pooled value/glamour monthly
  returns were computed WITHIN state, leaving mismatched month
  indices in sparse states (P_122 spread NaN). Moved to compute
  over all months first. No existing target affected (the target
  set has no 1B P_122 *spread* metric, only a t-stat — verified by
  exact-name lookup).
- Before → after: W_25 and B_25 month-sets PROVEN identical (W25 1B
  spread 0.008593 bit-identical; W25 max month Sep 1990); P_122
  dropped 5 post-horizon months (Aug 1994 + Jan–Apr 1995) and added
  5 earlier; N_88 shifted 3 (dropped Jun/Nov/Dec 1994); W25/N88 V−G
  spreads remain positive (+0.0375 / +0.0201); Table VII 82→84
  MATCH (2 P_122 cells moved into tolerance), 1 FAIL (P_122 t-stat
  −1.954 vs paper −0.168 — moderate-month composition vs the paper's
  unrecoverable 260-month window; numerical, not methodological).
  Other 7 tables' JSONs byte-identical (md5).
- Status: RESOLVED.

**Replicator actions (M1 + minors):**
- REPORT §3 Table II: E/P×GS AR spread corrected 11.0pp → 10.0pp
  (artifact 0.0996; paper 11.2).
- REPORT §3 Table VIII: beta gap now reported per classification
  (C/P deciles −0.05, B/M deciles −0.07, C/P×GS corners −0.18) with
  the conclusion restated via the paper's own arithmetic (≤0.18 ×
  8% ≈ 1.4pp/yr ≪ 10–11pp); C/P×GS raw-std reversal disclosed
  (glamour 0.287 > value 0.264 vs paper 21.6 < 24.1 — vintage
  volatility; size-adjusted "virtually identical" holds at
  mid-deciles).
- REPORT §3 Table VII paragraph rewritten for the bounded window.
- REPORT §5b enumeration widened to include the B/M glamour
  AEG(−5,0) cell (m2).
- A15 reworded: mean kept as direct reading; level gap left
  UNATTRIBUTED — median tested and does not close it (298/41 vs
  663/120) (m1).
- assumptions.md Iteration 3 entry appended with full five-field
  records for M1 and M2.
- Verification: grep confirms "11.0" gone, "−0.18" present;
  evaluation_iter6.json regenerated.

**Replicator decision:** both majors resolved with before/after
metrics; no convention re-tuning (A5 and avg-Q-first untouched per
audit guidance). Ready for audit 2.

## Per-cell evaluation (evaluation_iter6.json)
| Table | MATCH | PATTERN | FAIL |
|-------|-------|---------|------|
| I     | 309   | 4       | 3    |
| II    | 359   | 2       | 5    |
| III   | 130   | 7       | 3    |
| IV    | 38    | 15      | 10   |
| V     | 36    | 7       | 20   |
| VI    | 163   | 11      | 23   |
| VII   | 84    | 6       | 1    |
| VIII  | 50    | 3       | 1    |
| **All** | **1,169** | **55** | **66** |

Tier 1+2: 94.9% (1,169 MATCH = 90.6% Tier 1). FAIL clusters
unchanged in character (all documented vintage residuals: near-zero
SAAR/saar_std cells, fundamentals level drift + FM magnitudes,
early-formation year spreads, moderate-month composition in VII).

## Summary
Iteration 2 closed both audit-1 majors (self-report hygiene + Table
VII window) and both actionable minors; the M2 fix additionally
surfaced and repaired a latent index-alignment bug and improved the
Table VII match count. All headline claims remain intact (W25 cells
provably unchanged). Awaiting audit 2.
