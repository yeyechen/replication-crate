---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — contrarian_investment

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** Both audit-1 majors independently verified as fixed from scratch.
M2: the Table VII window is bounded to May 1968–Apr 1994 (312 months), the in-horizon
assertion exists and holds (my own re-derivation: 260 classified months, 0 violations;
max classified month Apr 1994 = the 1989 cohort's last Year +5 month), the 124/188 sign
split and 25/88/122/25 + 52 partition reproduce exactly, W_25 and B_25 month-sets are
provably identical to the old 324-month window (25/25 and 25/25 overlap), and ten
independently recomputed state cells match the artifact to six decimals (W25 glamour
−0.123768 / value −0.086284, 1B spread 0.008593 — the audit-1-era values, unchanged).
M1: every corrected REPORT number matches the artifact (E/P×GS spread 0.099606 = 10.0pp;
beta gaps −0.05/−0.07/−0.18; std reversal 0.287 > 0.264 disclosed); "11.0" survives only
as the paper's C/P citation. The other seven cells JSONs are value-identical (879/879
cells, 0 deviations vs evaluation_iter6; tables IV/V/VIII byte-identical). No blockers,
no actionable majors; four cosmetic minors, none touching a paper-facing number.
`requires_iteration: false` — the loop may close.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass; the two audit-1 imperfections are resolved — Table VII now enforces `mnum ≤ (fy+5)·12+4` per classified month (0 violations in my own recompute) and A15 no longer claims the median explanation (tested, rejected, residual left unattributed). Remaining deviations are documented conventions forced by paper-side ambiguity (unrecoverable 260-month EW window → semantic partition; pooled P3; mean SIZE), each with an empirical tie-breaker. |
| Headline matching | 5 | All five claims re-verified: AR spreads B/M +10.8/+10.5, C/P +11.3/+11.0, E/P×GS +10.0/+11.2 (artifact 0.099606), CPGS 21.3/22.1 vs 10.9/11.4; 18/18 five-year windows ×3; FM B/M collapse (t 0.55); EW beta 1.339 vs 1.304; W25 value −0.086 = paper exactly. |
| Data coverage | 4 | Exact period (formations Apr 1968–1989, holdings through Apr 1994, monthly May 1968–Apr 1994); crsp_202601 + comp_202601.funda + ff; 48,994 rows, be_valid 76.6%; one documented external gap (BEA GNP → Table VII Panel 2 not computed). |
| Concrete result matching | 5 | 1,169 Tier-1 / 1,290 = 90.6% (≥90% band) + 55 PATTERN = 94.9%; all 55 PATTERN cells same-sign and |rep/paper| ∈ [0.5, 2.0] (0 violations); eval6 `paper` == target for all 1,290 rows. |
| Signal strength | 4 | Headline cells within ~5% (spreads, beta, 18/18); supporting extrapolation magnitudes drift 15–50% (Table V levels, E/P+/C/P+ slopes ≈½) — all vintage, all sign/significance-correct. |
| Corollary | 4 | All six corollary types computed and checked (large-cap T III, horizon 18/18 T VI, downside W25/N88 T VII, beta-can't-explain T VIII, significance T IV, extrapolation T V); the one deviating corollary (C/P×GS raw-std order) is now disclosed in REPORT §3 with the vintage explanation; GNP states remain documented out-of-scope (external data). |
| 7 | REPORT.md matches results/*.json | ✓ | Every paper-facing number now matches the artifacts (M1 fixed, verified by grep + JSON lookup); the only residuals are internal bookkeeping (header tally 1,167/57 and the `evaluation_iter5.json` reference are stale vs iter6's 1,169/55) — minor m1. |

Overall (mean of six): **4.33 / 5.00** → binary verdict **REPLICATED** (≥3.0, no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

None actionable. Audit-1 majors verified resolved:

- [M1] RESOLVED — REPORT.md self-report now consistent with the artifacts.
  Verified: (a) `grep -n "11\.0" REPORT.md` returns only line 14, where it is the
  paper's C/P spread citation "(+11.0)" — the E/P×GS context now reads "+10.0pp
  (artifact 0.0996; paper 11.2pp)" (REPORT.md:15, :56), matching
  `results/table_II_cells.json` "Panel B (E/PxGS) AR spread value-glamour" = 0.099606.
  (b) Beta gap reported per classification (REPORT.md:80): "C/P deciles −0.05
  (1.311 − 1.362), B/M deciles −0.07 (1.341 − 1.407), C/P×GS corners −0.18
  (1.307 − 1.486)" — all three deltas reproduce from `results/table_8.md` Panel 1
  (D10−D1 = 1.311−1.362 = −0.051), Panel 3 (1.341−1.407 = −0.066), Panel 2
  (1.307−1.486 = −0.179); the ≤0.18 × 8% ≈ 1.4pp/yr arithmetic is correct.
  (c) Raw-std reversal disclosed (REPORT.md:80): "glamour 0.287 > value 0.264" —
  matches `table_8.md` Panel 2 std row (C1,G3)=0.287 / (C3,G1)=0.264 — with the
  vintage explanation and the mid-decile size-adjusted "virtually identical" caveat.
- [M2] RESOLVED — Table VII window bounded to in-horizon cohorts. Verified from
  scratch (auditor's own code, ClickHouse + `data/panel.parquet`):
  - `src/table7.py:44` sets `WIN_LO, WIN_HI = 23621, 23932` (May 1968 … Apr 1994;
    arithmetic verified: 1968·12+5 = 23621, 1994·12+4 = 23932, 312 months); the
    assertion at `src/table7.py:153-158` checks every classified month against
    `mnum ≤ (fy+5)·12+4` and passes on re-run (no AssertionError emitted).
  - My own EW pull over the window: 312 months, 124 negative / 188 positive — exact
    match to the `table_7.md` window note; semantic partition yields 25/88/122/25
    classified + 52 unclassified (= 312 − 260), as claimed.
  - My own horizon check over all 260 classified months: **0 violations**; the max
    classified month is Apr 1994 with active cohort 1989 and bound (1989+5)·12+4 =
    Apr 1994 — i.e., Apr 1994 is exactly the 1989 cohort's last Year +5 month.
  - W_25 and B_25 month-sets are provably invariant under the truncation: comparing
    my 312- vs 324-month partitions, both states overlap 25/25 with zero
    additions/drops (W25 max month Sep 1990; none of the 12 dropped months —
    May 1994…Apr 1995 — rank in the worst/best 25). N_88 shifted 3 months; P_122
    dropped 5 and added 5 earlier ones (counts verified; the log's enumeration of
    *which* P_122 months is slightly off — minor m3).
  - Ten independently recomputed cells match the artifact to ≤5e-6: W25 1A
    glamour −0.123768 / value −0.086284 (the audit-1 values, and value = paper's
    −0.086 exactly), W25 1B spread 0.008593 / t 1.821954 (bit-identical to the
    audit-1-era spread, as claimed), N88 1A/1B, P122 t −1.954195, B25 spread, EW
    index −0.104165. V−G spreads positive in W25 (+0.0375 / +0.0086) and N88
    (+0.0201 / +0.0057), both classifications — the paper's downside claim holds.
  - Re-running `table7.py` reproduces `table_VII_cells.json` byte-for-byte
    (md5 e45d3a20… unchanged). The other 7 cells JSONs: tables IV/V/VIII
    byte-identical on re-run; tables I/II/III/VI re-emit with value-identical
    content (879/879 cells, 0 value deviations vs `evaluation_iter6.json`) but
    non-deterministic key order across processes (minor m4).
  - `evaluation_iter6.json`: 1,169/55/66; all 45 rows differing iter5→iter6 are
    table_VII N_88/P_122 cells (zero rows change in the other seven tables); two
    cells moved PATTERN→MATCH (82→84 MATCH, as claimed); the sole Table VII FAIL
    is the 1B P_122 t-stat (−1.954 vs paper −0.168) — moderate-month composition
    vs the paper's unrecoverable 260-month EW window; numerical, documented,
    non-actionable.

Non-actionable residuals (documented, vintage- or data-driven; listed for completeness,
none triggers iteration): near-zero SAAR cells (Tables I–III, VIII saar_std D1);
Table V SIZE/growth levels; Table IV E/P+/C/P+ magnitudes (~½, sign/significance
correct); Table VI early-formation year cells; Table VII moderate-month composition
(P_122 t-stat); C/P×GS raw-std reversal (disclosed); E/P D10 dip not reproduced;
Table VII Panel 2 GNP states (no BEA data); OCR-truncated Table VIII P2 cells unscored.

### Minor (cleanup)

- [m1] REPORT.md header bookkeeping is stale after the iter6 regeneration: line 4
  reads "Outer iteration: 1" (now 2); line 6 reads "1,167 MATCH (Tier 1) + 57
  PATTERN" (the current per-table rows and `evaluation_iter6.json` sum to
  1,169/55 — the 94.9% hit rate is unchanged and correct); line 41 references
  `evaluation_iter5.json` (iter6 is current). All paper-facing numbers are correct.
  Specific fix: update the three header strings. `actionable: false` (cosmetic).
- [m2] `src/table7.py` docstrings are stale: the module docstring (line 4) still
  says "filtered to May 1968-Apr 1995 = 324 months", and `classify_states` (lines
  64–70) still narrates "Over 324 months (129 neg/195 pos) … 64 moderate-positive
  months UNclassified". The emitted `table_7.md` window note is correct; only the
  in-code comments lag. Specific fix: sync the two docstrings to 312/124/188/52.
  `actionable: false` (cosmetic).
- [m3] The M2 record's month enumeration is slightly inaccurate: `logs/log2.md:43-44`
  and `preparations/assumptions.md:246-247` say P_122 "dropped 5 post-horizon
  months (Oct–Dec 1994, Apr 1995)"; the auditor's set diff shows the 5 dropped
  P_122 months are Aug 1994 + Jan–Apr 1995 (Oct 1994 was unclassified; Nov/Dec
  1994 were among the 3 dropped N_88 months, with Jun 1994). The counts (5
  dropped / 3 shifted) and every downstream number are correct. Also
  `logs/log2.md:31` writes "W_25 (max month Sep 1981)" — the actual max is Sep
  1990 (immaterial; both are far inside the horizon). Specific fix: correct the
  month lists if the log is ever revisited. `actionable: false` (documentation).
- [m4] `tables.py` and `table6.py` emit cells JSONs with non-deterministic key
  order across processes: consecutive re-runs change the md5 (e.g.
  `table_I_cells.json` 4c11fd0b… → e6a925fc…) while all 879 cells are
  value-identical (verified against `evaluation_iter6.json`, 0 deviations). The
  "byte-identical md5" gate therefore passes only by luck of hash seed; the
  underlying values are perfectly reproducible. Specific fix:
  `json.dumps(..., sort_keys=True)` in the two emitters so the byte gate is
  meaningful. `actionable: false` (hygiene; no value drift).
- [m5] (carried, optional) per-table hit-rate footers in `results/table_{1..8}.md`
  — skipped again as non-load-bearing; Table VII now carries the window note,
  which is the substantive version of this. `actionable: false`.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | tables.py re-run reproduces identical values; B/M, C/P, E/P AR strictly increasing D1→D10; GS decreasing with the two paper-noted wobbles. |
| 2 | Headline-magnitude claim | ✓ | E/P×GS AR spread 0.099606 (paper 0.112); CPGS AR 0.1086/0.2133 (0.114/0.221); EW beta 1.339 (1.304); W25 value −0.086284 = paper −0.086. |
| 3 | Sample coverage ≥ 60% | ✓ | 48,994 rows reloaded; be_valid 76.6%, every formation ≥1,968 stocks (audit-1 recompute; panel unchanged — md5-stable inputs). |
| 4 | Data-source choice justified | ✓ | crsp_202601 + comp_202601.funda (dominant filter combo) + ff; GNP omission documented in REPORT §7. |
| 5 | prep_validation.py exit 0 | ✓* | Exit 1 at audit start solely because this file (audit2.md) did not yet exist ("log2.md exists but audit2.md is missing"); re-run after writing this file + SUMMARY.md clears it, as in audit 1. |
| 6 | All committed tables have results | ✓ | 8/8 tables with table_<n>.md + table_<roman>_cells.json; 2 figures present. |
| 7 | REPORT matches results/*.json | ✓ | M1 class fixed: all paper-facing numbers verified against `table_II_cells.json` (0.099606) and `table_8.md` (betas 1.486/1.307; std 0.287/0.264; decile gaps −0.051/−0.066). Residual: internal tally header stale by 2 cells (minor m1). |
| 8 | No orphan folders | ✓ | Slug root holds only data/ inputs/ logs/ preparations/ results/ src/ + REPORT.md + SUMMARY.md. |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md "Iteration 3" has full five-field records for M1 and M2 (Diagnosis / Next fix / Before metric / After metric / Status), including before/after month counts, spreads, and tallies. |
| 10 | Tier 2 within 2× magnitude | ✓ | All 55 PATTERN cells same-sign with |rep/paper| ∈ [0.5, 2.0] (0 violations, recomputed). |
| 11 | Corollary coverage | ✓ | All six types checked; the one reversing corollary (CPGS raw-std order) now disclosed in REPORT §3; GNP out-of-scope documented (external data, non-actionable). |

**Independent recomputation cross-check (auditor's own code, this audit):**
- EW window: 312 months (124 neg/188 pos) vs old 324 (129/195); semantic partition
  25/88/122/25 + 52 unclassified; W_25 and B_25 sets identical across windows
  (25/25 and 25/25 overlap); N_88 shifted 3; P_122 dropped 5 / added 5.
- Horizon: 0/260 classified months exceed (fy+5)·12+4; tail case = Apr 1994 /
  cohort 1989 / bound Apr 1994 (last Year +5 month, inclusive).
- Table VII cells: 10/10 recomputed values match `table_VII_cells.json` to ≤5e-6;
  W25 1B spread 0.008593 bit-identical to the audit-1 value; V−G positive in
  W25 (+0.0375/+0.0086) and N88 (+0.0201/+0.0057).
- Reproducibility: `table7.py` re-run → `table_VII_cells.json` byte-identical
  (md5 e45d3a20…); tables IV/V/VIII byte-identical; tables I/II/III/VI
  value-identical with unstable key order (minor m4).
- Evaluation integrity: `evaluation_iter6.json` `paper` field equals the
  `tables_to_replicate.json` target for all 1,290 rows; the 45 iter5→iter6 value
  changes are all table_VII N_88/P_122 cells; totals 1,169/55/66 (90.6% Tier 1,
  94.9% Tier 1+2).

## 4. Issues the agent should have caught (didn't)

1. **REPORT header not swept with the §3 edits.** The per-table tallies and the
   Table VII paragraph were updated for iter6, but the header's 1,167/57 count,
   the "Outer iteration: 1" line, and the `evaluation_iter5.json` reference were
   not. A final grep of REPORT for "1,167" / "iter5" / "Outer iteration" would
   have caught all three. (Minor — no paper-facing number affected.)
2. **Stale docstrings in table7.py after the window change.** The fix updated the
   constants, the assertion, and the emitted markdown note, but left the module
   and `classify_states` docstrings narrating the old 324-month/64-unclassified
   window. (Minor.)
3. **Loose month enumeration in the M2 log record.** "Oct–Dec 1994, Apr 1995" is
   not the P_122 drop set (actual: Aug 1994 + Jan–Apr 1995); the count of 5 is
   right, the list was written from memory rather than the set diff. (Minor.)
4. **md5 gate over hash-unstable JSON.** The byte-identity claim was made over
   files whose key order varies with PYTHONHASHSEED; it happened to hold in the
   worker's run. A `sort_keys=True` dump would make the gate real. (Minor —
   values verified identical.)

## 5. Closure note (requires_iteration: false — no next-iteration prompt)

Both audit-1 majors ([M1] self-report consistency; [M2] Table VII in-horizon
window) and both actionable minors ([m1] A15 wording; [m2] §5b enumeration) are
verified fixed by independent recomputation; the M2 fix additionally repaired a
latent pooled-return index-alignment bug and improved the Table VII match count
(82→84). Blocker count = 0, actionable-major count = 0. The five minors above
are cosmetic/documentation items (`actionable: false` — none touches a
paper-facing number or a computed cell), and every remaining residual is a
documented vintage or external-data limitation that a further iteration cannot
close. The replication is trustworthy on every headline claim and corollary; the
replicator-auditor loop may close. If a polish pass is ever scheduled anyway,
minors m1–m4 are each one-line fixes.

## 6. Auditor's notes (free-form)

This iteration did exactly what a PARTIAL→PASS pass should look like: the two
majors were bounded, fixed, and — importantly — verified with before/after
evidence in the assumptions log (month counts, spreads, tallies), and the M2
work surfaced and fixed a real latent bug (within-state pooled returns leaving
misaligned month indices in sparse states) rather than just truncating the
window. I re-derived the entire Table VII machinery independently — my own EW
pull, my own partition, my own cohort mapping, my own state means — and ten of
ten cells matched to six decimals, with the W_25/B_25 invariance proven as set
identity rather than asserted. The headline W25 value cell (−0.086) remains an
exact paper match, and the downside-risk claim holds in both classifications.
The REPORT hygiene fixes (M1) are clean: every corrected number traces to the
artifact, and the raw-std reversal that audit 1 found undisclosed is now
disclosed with the right explanation. What keeps Methodology and Corollary at 4
rather than 5 is not any fixable defect but the honest floor of this paper on
modern data: the 260-month EW window is unrecoverable from the OCR (the semantic
partition is the correct response, and it now operates on a horizon-clean month
set), the GNP-state panel needs BEA data that is not in the warehouse, and one
corollary (raw-volatility ordering) genuinely reverses on the 2026 vintage —
now surfaced rather than hidden. The four new minors are all documentation
hygiene (a stale header line, two stale docstrings, a sloppy month list in the
log, and hash-unstable JSON key order) and none of them warrants another outer
iteration. Closing the loop here is the right call; this is a faithful
replication of LSV (1994) with a fully diagnosed, vintage-driven ~5% residual.
