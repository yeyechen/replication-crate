---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 1 — contrarian_investment

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** A genuinely strong replication — all five central claims and six
corollary predictions were independently re-verified from `data/panel.parquet` and
ClickHouse, the pipeline is bit-identical on re-run, and 94.9% of 1,290 cells are
Tier 1+2. No blockers. The PARTIAL verdict is driven by two bounded, fixable items:
three self-report numbers that contradict the computed artifacts (and one undisclosed
corollary reversal), and a Table VII month-window that lets 8 classified months use a
cohort past its 5-year horizon. Neither touches a headline claim.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | 27 line-cited rules + 15 documented assumptions; A5 tested head-to-head and rejected on evidence, A13 pooled-P3 and A12 HH verified against the paper's t's. Two documented imperfections: Table VII window extends to Apr 1995 (post-horizon cohort reuse in P122); A15's "paper used the median" rationale is not borne out (our median-of-means 298/41 ≠ paper 663/120). |
| Headline matching | 5 | All five claims match in shape/sign/magnitude class: AR spreads B/M +10.8/+10.5, C/P +11.3/+11.0, CPGS 21.3/22.1 vs 10.9/11.4; 18/18 five-year windows ×3; FM B/M collapses (t 0.55); EW beta 1.34/1.30. Every headline spot-check passes. |
| Data coverage | 4 | Exact period (formations 1968–1989, holdings through 1994, monthly back to 1963); sources crsp_202601 + comp_202601.funda + ff all match; be_valid ~76.6% (vintage-thin early years); one documented external gap (BEA GNP → Table VII Panel 2 not computed). |
| Concrete result matching | 5 | 1,167 Tier-1 / 1,290 = 90.5% (≥90% band); +57 Tier-2 = 94.9% Tier-1+2. Classification logic re-derived from scratch reproduces 1167/57/66 with zero mismatches. |
| Signal strength | 4 | Headline signal cells within ~5% (spread, beta, 18/18); but supporting extrapolation magnitudes drift 15–50% (Table V C/P value 0.322/0.172, SIZE 2×) and E/P+/C/P+ FM slopes ≈½ — all vintage, all sign/significance correct. |
| Corollary | 4 | Large-cap robustness (T III ✓), horizon consistency (T VI 18/18 ✓), downside risk (T VII W25 ✓), beta-can't-explain (T VIII ✓ in substance), variable significance (T IV ✓), extrapolation direction (T V ✓). GNP-state corollary not computed (documented, external data) and CPGS raw-std order reverses (undisclosed). |
| 7 | REPORT.md matches results/*.json | ✗ | E/P×GS AR spread stated 11.0pp but artifact = 9.96pp; Table VIII "−0.05 beta gap" cites the C/P-decile gap while the C/P×GS corner gap in the artifact is −0.179; CPGS raw-std reversal undisclosed. |

Overall (mean of six): **4.33 / 5.00** → binary verdict **REPLICATED** (≥3.0, no dimension = 1).

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] Self-report (REPORT.md §3) contains three values inconsistent with the computed
  artifacts, plus one undisclosed corollary reversal. (a) E/P×GS AR spread written
  "11.0pp (paper 11.2)" but `results/table_II_cells.json` "Panel B (E/PxGS) AR spread
  value-glamour" = 0.099606 (= 10.0pp); the target/paper value is 0.112, so the artifact
  MATCHes but the prose overstates the replication by 1pp. (b) REPORT §3 Table VIII writes
  "the value−glamour beta gap is −0.05 in our data vs +0.1 in the paper … trivial in
  magnitude"; −0.05 is the C/P-decile gap (P1 D10−D1 = 1.311−1.362), but the flagship
  C/P×GS corner gap in the *same* artifact (`results/table_8.md` Panel 2, 1.307−1.486) is
  −0.179, larger in magnitude than the paper's +0.1 and sign-reversed — not "trivial".
  (c) The paper's body claim (L2346) "value std 24.1% > glamour std 21.6%" for C/P×GS is
  reversed in our data (glamour 0.287 > value 0.264) and is never disclosed; these two
  body cells were dropped from scoring on the (legitimate) OCR-truncation ground, so the
  reversal is an unscored, undisclosed deviation.
  - File: `replications/contrarian_investment/REPORT.md:56` (E/P×GS); `:80` (beta gap + std);
    artifact `results/table_8.md:17-18`, `results/table_II_cells.json`.
  - Likely cause: report prose was written from memory / a different statistic than the
    one the artifact targets; the CPGS std reversal was simply not surfaced because the
    cells were out of the scored set.
  - Specific fix: in REPORT §3 set E/P×GS AR spread to +10.0pp; report the value−glamour
    beta gap **per classification** (C/P deciles −0.05, B/M deciles −0.07, C/P×GS corners
    −0.18) and state that all are too small in dollar terms to explain the 10–11pp spread
    (which remains true — even 0.18×8% ≈ 1.4pp/yr); add one disclosure line that the C/P×GS
    raw-return std is reversed vs the paper (vintage volatility, ~1.2–1.3× levels) while the
    paper's "size-adjusted std virtually identical" finding holds at the mid-deciles.
    `actionable: true`.

- [M2] Table VII month window (May 1968–Apr 1995, A10) lets classified months fall outside
  the last cohort's holding horizon. Over 324 months the rank-order rule yields the paper's
  25/88/122/25 by construction (129 negative, 195 positive), but 8 of the P_122 months and
  ~2 of the N_88 months are after 1994-04, where the "most recent April formation" (1989) is
  5.5–6 years old — i.e. the active cohort is reused past Year +5, which the paper's portfolio
  definitions do not permit. The downside-risk states the paper actually sells (W_25, and the
  N_88 bulk) are clean (W25 max date 1990-09), so no headline claim is affected; the taint is
  confined to P_122, which already holds the lone Table VII FAIL and several PATTERNs. The
  counts "matching the paper" is not a validation — it is forced by any window with ≥113
  negative / ≥147 positive months (A10 itself says "adjust the range to reproduce the counts").
  - File: `replications/contrarian_investment/src/table7.py:40` (`WIN_LO, WIN_HI = 23621, 23944`),
    `src/table7.py:58-79` (classify_states), `preparations/assumptions.md` A10.
  - Likely cause: window set to "cover the 22 cohorts + 1yr" without bounding each month to a
    cohort that is within its 5-year holding window; rank-order counts then look right by
    coincidence of sign-totals.
  - Specific fix: either (a) truncate the EW window to 1994-04 (the last month any cohort is in
    horizon) and only classify months where the active April cohort is ≤5 years old, or (b) drop
    any month whose active cohort exceeds Year +5 from the state averages; then recompute the
    25/88/122/25 partition (it will shift by a few months vs the paper, which is expected and
    should be disclosed) and re-emit `table_VII_cells.json` + `evaluation`. Report how many
    P_122/N_88 months move. `actionable: true`.

  (Marked actionable: both M1 and M2 are bounded one-session fixes; the replication is already
  trustworthy on every headline number, so the next iteration is polish + one clean window.)

### Minor (cleanup)

- [m1] A15's median rationale is empirically unsupported. The SIZE cells are correctly scored
  FAIL regardless, but `assumptions.md` A15 justifies keeping the mean by claiming the pattern
  is "consistent with the paper having reported the median"; the auditor's median-of-formation-means
  is G=298 / V=41 $M, which does **not** match the paper's 663/120 either (ratio 0.45, not ~1).
  The true cause of the SIZE level gap is not pinned (likely vintage + a different aggregation
  the parse cannot recover). File: `preparations/assumptions.md` A15.
  Specific fix: reword A15 to "mean is the direct reading; the level gap's cause (vintage /
  aggregation) is not identified; median was tested and does not close it either (298/41 vs
  663/120), so SIZE stays a documented residual." `actionable: false` (no recompute can fix the cell).
- [m2] §5b enumerates the B/M value earnings-growth blowups as "3 outlier cells" but the
  same mechanism also produces B/M **glamour** AEG(−5,0) = 0.080 vs paper 0.309 (≈0.26×, a
  4th extreme same-sign cell). File: `REPORT.md:99`, `:68`. Specific fix: widen the §5b
  enumeration to include the glamour AEG(−5,0) cell. `actionable: false`.
- [m3] The human-readable `results/table_{1..8}.md` carry the paper-format tables but no
  inline per-cell PASS/FAIL annotation (the evaluation lives only in `evaluation_iter5.json`).
  Not load-bearing. Specific fix (optional): append a one-line per-table hit-rate footer to
  each markdown. `actionable: false`.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | B/M, C/P, E/P AR strictly increasing D1→D10 (auditor recompute); GS decreasing with two minor wobbles (D1<D2, D7<D8), as the paper notes. |
| 2 | Headline-magnitude claim | ✓ | B/M AR 0.098/0.206 (paper 0.093/0.198); CPGS AR 0.109/0.213 (paper 0.114/0.221); EW beta 1.339 (paper 1.304). All re-derived from the panel / ClickHouse. |
| 3 | Sample coverage ≥ 60% | ✓ | 48,994 rows; every formation ≥1,968 stocks; be_valid 76.6%, ep_pos 70.5%, cp_pos 71.1%, gs 76.7%. |
| 4 | Data-source choice justified | ✓ | crsp_202601 + comp_202601.funda (dominant filter combo) + ff; shrcd 10/11 & exchcd 1/2 PIT; standard operationalization; GNP omission documented. |
| 5 | prep_validation.py exit 0 | ✓* | Prep contract (rules/tables/data/assumptions) passed. At audit start the validator returned exit 1 *only* because the two auditor-owned files (this file + SUMMARY.md) did not yet exist; that layout error clears once they are written. Re-run after writing. |
| 6 | All committed tables have results | ✓ | 8/8 tables have table_<n>.md + table_<roman>_cells.json; 2 figures present and valid. |
| 7 | REPORT matches results/*.json | ✗ | Three prose values inconsistent with artifacts (M1). Cells JSON themselves are faithful (eval paper == target paper for all 1,290; eval rep == cells JSON for all 1,290). |
| 8 | No orphan folders | ✓ | Slug root holds only data/ inputs/ logs/ preparations/ results/ src/ + REPORT.md; no literal-brace folders. |
| 9 | Diagnoses paired with fix attempts | ✓ | A5 alternative reading tested head-to-head (iter-3 diagnostic) with before/after and rejected on evidence; A13/A14/A15 ratified with empirical tie-breakers; every FAIL cluster (§5a/b/c) has diagnosis + evidence + classification. |
| 10 | Tier 2 within 2× magnitude | ✓ | All 57 PATTERN cells verified same-sign and |rep/paper| ∈ [0.5, 2.0] (0 violations). |
| 11 | Corollary coverage | ✓ | All 6 corollary types checked (T III size-robustness, T VI 18/18, T VII downside, T VIII risk, T IV significance, T V extrapolation) or documented out-of-scope as non-actionable (GNP). |

**Independent recomputation cross-check (auditor's own code, not the agent's):**
- Table I: B/M D1/D10 AR = 0.0983/0.2058, C/P 0.0927/0.2053, E/P 0.1121/0.1955 (D9 0.1926/D10 0.1955 — paper's distressed-firm dip 0.193>0.162 does **not** reproduce, as disclosed), GS 0.1785/0.1240; SAAR −0.0397/+0.0357 (paper −0.043/+0.035); CR5 0.569/1.519 (paper 0.560/1.462). Exact match to the replicator's claims.
- Table II C/P×GS: glamour(1,3) AR 0.1086 / value(3,1) 0.2133; CR5 0.662/1.635; SAAR spread +0.0800 (paper 0.087). Match.
- Table III: spread +0.0825 (paper +0.078); SAAR spread +0.0720 (paper +0.087). Match.
- Table VI means: P1 0.0872/0.3830/0.9103, P2 0.1247/0.5242/1.1111, P3 0.0739/0.3867/0.9804 — equal to the cells JSON; **18/18** five-year V>G in **all three** panels (min spreads +0.21/+0.42/+0.27). t-stats within the paper's (max dev P1 3-yr 4.7 vs 6.2 ≈ 24%, as the report states).
- Table IV: auditor FM gives spec8 B/M = +0.0051 (t +0.55), spec6 B/M = +0.0088 (t +0.82), GS −0.0665 (t −2.72), C/P+ +0.1097 (t +2.38) → B/M-absorption claim reproduced exactly. N/formation ≈ 1,634–2,186.
- Table V: B/M D/P 0.0123/0.0360; RETURN(−3,0) +1.5764/−0.0553; CPGS C/P 0.0761/0.3223; internal consistency 0.0761×(1+0.1234)^5 = 0.136 = paper's 5-yr-ahead C/P (verified arithmetically).
- Table VIII (ClickHouse): rf confirmed decimal (1968 ≈ 0.004/mo); EW-index beta(EWx~VWx) = 1.3387, std(EW) = 0.2682 — bit-equal to the report's 1.339/0.268. CPGS glamour/value beta = 1.475/1.296 (gap −0.179), std = 0.287/0.264 (order reversed vs paper 0.216/0.241).
- Reproducibility: all six table scripts re-run; every `table_*_cells.json` is **byte-identical** to the pre-run backup.

## 4. Issues the agent should have caught (didn't)

1. **REPORT overstates E/P×GS spread.** The artifact's E/P×GS AR spread is 9.96pp (a clean MATCH against the 11.2pp target), but REPORT §3 quotes 11.0pp. A careful pass over REPORT against `table_II_cells.json` would catch this.
2. **Table VIII beta-gap cherry-pick + undisclosed std reversal.** The "−0.05, trivial" line uses the C/P-decile gap; the C/P×GS corner gap (−0.179) and the CPGS raw-std reversal (glamour 0.287 > value 0.264 vs paper 21.6 < 24.1) are not surfaced. Because the cells were excluded from scoring on OCR grounds, the reversal is easy to overlook — but the body text states it as a finding, so it belongs in the residual discussion.
3. **Table VII window past the cohort horizon.** Extending to Apr 1995 means 8 P_122 + ~2 N_88 months reuse the 1989 cohort at Year +5.5/+6. The "25/88/122/25 matches the paper" check is not a validation (any window with the right sign-totals reproduces it); bounding each month to an in-horizon cohort is the correct implementation. W_25 (the state the paper sells) is unaffected, which is why this is not a blocker.
4. **A15 median claim.** Median-of-formation-means (298/41) does not match the paper (663/120), so "the paper reported the median" is not a supported explanation for the SIZE gap; the residual should be left unattributed rather than attributed to a median/mean choice that the data do not confirm.
5. **§5b undercounts the earnings-growth blowup cluster** (the B/M glamour AEG(−5,0) 0.080 vs 0.309 cell is the same mechanism and is not listed).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Contrarian Investment, Extrapolation, and Risk"
(Lakonishok, Shleifer & Vishny 1994) for slug `contrarian_investment`. The previous run
completed with verdict **PARTIAL** (audit 1 at
`replications/contrarian_investment/logs/audit1.md`). Read the audit first. The replication
is already trustworthy on every headline number (94.9% Tier-1+2, all five claims and six
corollaries independently re-verified, pipeline bit-identical on re-run); this iteration is
polish plus one clean Table VII window.

## Issues to address (priority order)

### [M1] — MAJOR — self-report inconsistent with the artifacts
REPORT.md §3 quotes three values that do not match the computed results, and omits one
corollary reversal: (a) E/P×GS AR spread is written "11.0pp" but `results/table_II_cells.json`
"Panel B (E/PxGS) AR spread value-glamour" = 0.0996 (10.0pp) — the target/paper is 0.112, so the
artifact is correct and the prose is wrong; (b) the Table VIII "value−glamour beta gap −0.05 …
trivial" line cites the C/P-decile gap, but the C/P×GS corner gap in `results/table_8.md` Panel 2
is −0.179 (1.307−1.486), larger in magnitude than the paper's +0.1 and sign-reversed; (c) the
paper's body claim (L2346) that C/P×GS value std (24.1%) > glamour std (21.6%) is reversed in our
data (glamour 0.287 > value 0.264) and is never disclosed (those cells are unscored on OCR
grounds, so the deviation is hidden).

**Specific fix:**
1. In REPORT §3 Table II, change the E/P×GS AR spread to +10.0pp (artifact value); keep paper 11.2pp.
2. In REPORT §3 Table VIII, report the value−glamour beta gap **per classification** (C/P deciles
   −0.05, B/M deciles −0.07, C/P×GS corners −0.18) and reword the conclusion as "under every
   classification the dollar beta difference (≤0.18) explains ≤1.4pp/yr of the 10–11pp spread, so
   beta cannot explain it — the paper's own arithmetic (L2344)."
3. Add one sentence disclosing that the C/P×GS raw-return std is reversed vs the paper (vintage
   volatility; levels ~1.2–1.3×) while the paper's "size-adjusted std virtually identical" finding
   holds at the mid-deciles.
4. Verification: grep REPORT for "11.0" (should be gone) and "0.179"/"−0.18" (should appear).

### [M2] — MAJOR — Table VII months reuse an out-of-horizon cohort
`src/table7.py` sets the EW window to May 1968–Apr 1995 (324 months). The rank-order rule yields
25/88/122/25 by construction (129 negative, 195 positive), but 8 P_122 months and ~2 N_88 months
are after 1994-04, where the "most recent April formation" (1989) is past Year +5. The headline
downside state W_25 is clean, so no claim flips, but the window is methodologically wrong.

**Specific fix:**
1. In `src/table7.py`, restrict state membership to months where the active April cohort is within
   its 5-year holding window (either truncate the window to 1994-04, or drop months whose active
   cohort exceeds Year +5 from the state averages in `cell_m`/`dec_m`).
2. Recompute the 25/88/122/25 partition on the bounded set; disclose the resulting counts and how
   many P_122/N_88 months moved relative to the unbounded window (they will shift — that is expected
   and correct; the paper's exact 260-month window is not recoverable from the OCR).
3. Re-emit `results/table_7.md`, `results/table_VII_cells.json`, and refresh
   `results/evaluation_iter5.json` for the affected Table VII cells.
4. Verification: assert no classified month's date > the active cohort's (formation_year+5)-04; the
   W_25/N_88 V−G spreads should remain positive (paper's claim).

### [m1] — MINOR — correct the A15 median rationale
`preparations/assumptions.md` A15 claims the SIZE level pattern is "consistent with the paper
having reported the median", but the auditor's median-of-formation-means is G=298 / V=41 $M, which
does not match the paper's 663/120 either. The SIZE cells stay FAIL (correctly), so no recompute is
needed.

**Specific fix:** reword A15 to state the mean is the direct reading, the level gap's cause is not
identified, and median was tested and does not close it (298/41 vs 663/120). Leave the cells as a
documented vintage/aggregation residual.

### [m2] — MINOR — widen the §5b blowup enumeration
REPORT §5b lists "3 earnings-growth blowups" but the same mechanism also yields B/M **glamour**
AEG(−5,0) = 0.080 vs paper 0.309 (≈0.26×). Add it to the enumeration. No recompute needed.

### [m3] — MINOR (optional) — per-table hit-rate footer in the markdowns
`results/table_{1..8}.md` carry the tables but no inline hit-rate; optionally append a one-line
"MATCH/PATTERN/FAIL = x/y/z" footer per table. Not load-bearing.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every new `assumptions.md` entry needs all five
  fields (Diagnosis, Next fix, Before metric, After metric, Status). M2 in particular must report
  before/after P_122/N_88 month counts and the W25/N88 spreads.
- **Read `rep/STUCK_AGENT_GUIDELINE.md`** before any new debug cycle.
- **Don't retune conventions to chase near-zero cells.** The A5 formation-fixed size deciles were
  correctly kept last iteration — do not revisit them; the near-zero SAAR residuals are vintage noise.
- **Verify REPORT against the cells JSON.** After editing REPORT, re-grep every number you changed
  against `results/table_*_cells.json` (the M1 errors were exactly a report/artifact drift).

## Inputs you should read

- `replications/contrarian_investment/logs/audit1.md` — this audit (full context)
- `replications/contrarian_investment/inputs/content.md` — paper ground truth
- `replications/contrarian_investment/preparations/assumptions.md` — A1–A15 + iteration log
- `replications/contrarian_investment/results/table_II_cells.json`, `table_8.md`,
  `table_VII_cells.json` — the artifacts the report must match
- `replications/contrarian_investment/src/table7.py` — window + cohort logic to bound (M2)

## What NOT to redo

- Skip re-reading the root `SKILL.md`; the contract is unchanged.
- Skip re-running the ClickHouse catalog scan; `data_verification.json` is current.
- Do **not** change the A5 size-decile convention or the avg-Q-first Table V default — both were
  evidence-based and re-trying them only chases noise.
- Do **not** edit `SUMMARY.md` (the auditor owns it).

## Deliverables for this iteration

- `src/table7.py` + regenerated `results/table_7.md`, `table_VII_cells.json`, and refreshed
  `results/evaluation_iter5.json` (M2)
- `REPORT.md` corrected per M1 (E/P×GS spread, per-classification beta gap, CPGS std disclosure)
  and §5b enumeration (m2)
- `preparations/assumptions.md` reworded A15 (m1) + a new iteration-log entry for M1/M2 with all
  five fields
- Re-run all table scripts and confirm byte-identical cells JSON except the Table VII cells you
  intentionally change

## Stop conditions

- M1 + M2 fixed and verified, m1/m2 cleaned → re-run `scripts/prep_validation.py` (should exit 0
  now that audit1.md + SUMMARY.md exist) and re-run the table scripts → the next audit should reach
  PASS with `requires_iteration: false`.
- If the bounded Table VII window shifts the 18/18 or W25/N88 claims (it should not), stop and
  document — that would be a real finding, not a fix.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the cleanest replications I have audited. The prep contract is exemplary (27
line-cited rules across all categories, 15 assumptions each with rationale + impact, a
data-verification verdict of "ready" on 7/7 requirements), and the inner-loop trace shows the
right discipline: the one convention that *could* have been tuned to fit (A5 per-December size
deciles) was tested head-to-head in inner iteration 3 and correctly *rejected* because it improved
near-zero cells at the cost of the headline corners — exactly the anti-tuning behaviour the
framework wants. I re-derived the classification engine from scratch and reproduced 1167/57/66 with
zero disagreement, re-ran all six table scripts to byte-identical output, and recomputed every
headline number from the cached panel (and the EW/VW/rf series straight from ClickHouse) — they all
match the report's *claims* even where they sit 15–50% off the paper's levels (vintage, correctly
diagnosed). The 66 FAILs are honestly clustered into near-zero size-benchmark cells, vintage level
drift, and early-formation noise; none touch a headline or corollary claim, and the 18/18
five-year consistency — the paper's most demanding qualitative prediction — reproduces with minimum
spreads of +0.21 to +0.42. The two things keeping this at PARTIAL are both small and both
trustworthiness/cleanliness rather than correctness: the self-report's three misstated numbers
(including silently dropping a corollary reversal) and a Table VII window that, by coincidence of
sign-totals, reproduces the paper's state counts while letting a handful of months borrow an
expired cohort. Both are one-session fixes. After them, this should clear to PASS.
