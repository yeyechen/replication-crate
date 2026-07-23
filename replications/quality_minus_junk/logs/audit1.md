---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 6
requires_iteration: true
---

# Audit Report 1 — quality_minus_junk

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Honest, fully reproducible first-iteration replication of the US Long Sample. Every number in `REPORT.md` / `results/table_*.md` was independently recomputed from `data/panel.parquet` + ClickHouse FF factors and matches exactly. The central QMJ result replicates in sign, shape, and significance but at ~77% of the paper's headline magnitude; the residual gap is correctly traced to two documented upstream score approximations (plain CAPM beta, non-per-share growth). No blockers. Gaps: committed Table 9 missing, two methodology deviations, and corollary tests (subsample stability, FF5/6-factor robustness) not computed.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3 | 5 of 6 checks pass; formula check fails on two *documented* deviations — plain 60-mo CAPM beta instead of Frazzini-Pedersen (2014), and growth not computed per-share (Assumption 3, W6). |
| Headline matching | 3 | Sign + shape all correct (QMJ positive/significant; quality→return rising; quality safer); headline magnitudes ~23–29% below paper (QMJ 4F 0.46 vs 0.60; H-L ret 0.30 vs 0.42). |
| Data coverage | 4 | Period exact (Jun 1957–Dec 2016); universe 4,380/mo vs paper ~4,585 (within 4.5%); CRSP+Compustat NA+FF all match; one documented filter substitute (`consol='C'`). |
| Concrete result matching | 4 | 30/39 committed cells (T3+T4) within stated tolerance = 77% (auditor-recomputed); committed Table 9 (8 cells) has no results file. |
| Signal strength | 3 | Headline cells all in [0.5, 2.0]: QMJ 4F r=0.77, H-L ret r=0.72, H-L 4F r=0.77, QMJ 3F r=1.03; none in [0.8,1.2] band → not a 4. |
| Corollary | 2 | Factor loadings mostly replicate (MKT/SMB/HML negative ✓, UMD sign flip ✗); subsample stability, cross-sectional, and FF5/6-factor robustness not computed; Table 9 spanning missing. |

Spot-check 7 (SUMMARY/results match): ✓ — see Section 3.

## 2. Issues by severity

### Blockers (must fix)

None. The prep contract validates (the only `prep_validation.py` errors are the auditor-owned `audit*.md`/`SUMMARY.md` this audit creates); coverage is 88.7%; no methodology gap invalidates downstream metrics (the Profitability factor matches the paper at 0.49 vs 0.50, proving the core pipeline is sound).

### Major (should fix)

- [M1] Committed Table 9 (spanning tests) not implemented — `results/table_9.md` absent. (actionable: true)
  - File: `preparations/tables_to_replicate.json:336` (id "T9") vs `results/` (no table_9.md)
  - Likely cause: iteration stopped after Tables 3 & 4; Table 9 deferred to a later iteration (REPORT.md acknowledges "selected but not yet implemented").
  - Specific fix: regress SMB/HML/UMD on the standard factors with and without QMJ; targets in tables_to_replicate.json (e.g. SMB alpha 0.13→0.49, HML 0.79→1.01 with QMJ).

- [M2] Beta estimated as plain 60-month rolling CAPM instead of Frazzini-Pedersen (2014). (actionable: true)
  - File: `src/sql/06_beta_monthly.sql`; `preparations/assumptions.md:19` (A3) and W6; paper `inputs/content.md:273` (var_bab_beta).
  - Likely cause: first-pass simplification; FP(2014) needs daily returns (252-day vol × 1260-day 3-day corr). This flattens the Table 3 beta gradient (P3–P10 ≈ 0.95–1.01 vs paper's smooth 1.10→0.92) and weakens Safety 4F alpha (0.36 vs 0.51) and the QMJ MKT loading (-0.16 vs -0.20).
  - Specific fix: implement FP(2014) beta from `crsp_202601.dsf` + `dsi`; verify the Table 3 beta profile declines monotonically toward ~0.92 at P10 and Safety 4F alpha moves toward 0.51.

- [M3] Growth measures not computed on a per-share basis. (actionable: true)
  - File: `src/sql/02_funda_annual.sql`; `preparations/assumptions.md` W6; paper `inputs/content.md:255` (var_growth_per_share) and the "lowercase = per share" note at L3866.
  - Likely cause: deferred split-adjusted per-share computation; weakens the Growth sub-score (Growth 4F alpha 0.28 vs 0.46).
  - Specific fix: divide growth numerators by split-adjusted shares (`csho`/adjustment factors); verify Growth 4F alpha moves toward 0.46.

- [M4] Corollary 'subsample stability' not computed in artifacts. (actionable: true)
  - Paper: Fig. 2 (cumulative 4F alphas over time) and Table 15 (20-year subsamples / by size); paper claims "no particular subsample driving our results" (`inputs/content.md:2075`).
  - Likely cause: not attempted in iteration 1.
  - Specific fix: add `results/table_4_subsample.md` with QMJ 4F alpha split into 20-year windows (and pre/post-2008); confirm the sign stays positive and significant in each.

- [M5] Corollary 'robustness to alternative factor models' not computed. (actionable: true)
  - Paper: Table 5 (FF5 and 6-factor alphas; QMJ 16–38 bp/mo, large positive RMW loading) and Tables 17/18 (BAB controls), `inputs/content.md:2113`.
  - Likely cause: not attempted; `ff.five_factor_monthly` is present in the catalog (candidate_assessment.json).
  - Specific fix: add `results/table_5_robustness.md` regressing QMJ on FF5 and FF6; confirm positive alpha and positive RMW loading.

- [M6] QMJ UMD loading sign flip (+0.07 vs paper -0.09). (actionable: true)
  - File: `results/table_4.md:14`; committed metric `QMJ_umd_loading` (tables_to_replicate.json:284).
  - Likely cause: likely downstream of the M2/M3 score approximations (weak Safety/Growth change the momentum tilt of the quality sort), but not separately diagnosed.
  - Specific fix: after M2/M3, re-check the UMD loading; if still positive, inspect the 12-1 momentum exposure of the Quality vs Junk legs directly. Target: small negative loading.

### Minor (cleanup)

- [m1] Orphan nested directory `replications/quality_minus_junk/` (empty skeleton) inside the slug root.
  - File: `replications/quality_minus_junk/replications/quality_minus_junk/{data,src,results,logs,inputs,preparations}` (0 files, empty dirs)
  - Likely cause: a `LAYOUT.ensure()` / path call run with the wrong `replications_root`, creating a nested copy.
  - Specific fix: remove the empty nested `replications/` tree; confirm the real artifacts live at the slug root.

- [m2] Table 3 P10 Adjusted-R² displayed as 0.90 vs paper 0.59, not flagged.
  - File: `results/table_3.md:27` (comparison row shows "0.90 / 0.59")
  - Likely cause: likely a paper-extraction artifact (paper P10 = H-L = 0.59 is economically odd for a VW decile), but the agent displayed the gap without noting it.
  - Specific fix: add a one-line note that P10 Adj-R² is not part of the committed metrics and the paper value looks like an extraction anomaly.

- [m3] "Monotonically increasing P1→P10" overstates the series.
  - File: `REPORT.md:77`, `logs/log1.md:32`
  - Likely cause: shorthand; the replicated excess-return series dips at P4, P5, P9 (0.38/0.49/0.55/0.54/0.47/0.53/0.55/0.58/0.58/0.68).
  - Specific fix: reword to "rising on average / almost monotonic," matching the paper's own "almost monotonically" language (paper L1534).

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Quality→return rises P1→P10 (0.38→0.68) with positive H-L (+0.30); "almost monotonic" (dips at P4/P5/P9), consistent with the paper's own wording. Beta falls P1→P3 then flattens (see M2). |
| 2 | Headline-magnitude claim | ✓ | Auditor recomputation reproduces the agent exactly: QMJ 4F 0.462 (paper 0.60), H-L ret 0.301 (0.42), H-L 4F 0.813 (1.05), H-L beta -0.347 (-0.36). Agent's numbers are honest; vs paper they are 77%/72%/77%/96%. |
| 3 | Sample coverage ≥ 60% | ✓ | Quality non-NaN 88.7%; universe 4,380 obs/mo vs paper ~4,585 avg stocks/mo (95.5%). |
| 4 | Data-source choice justified | ✓ | `consol='C'` substitute documented (W1 — `STD` absent in data); FF columns verified as monthly decimals (Sep-08 mkt_rf = -0.0935), so no /100; universe shrcd 10/11 + non-OTC matches paper L332. |
| 5 | prep_validation.py exit 0 | ✓ | Exit 1 is solely the two auditor-owned files (`audit*.md`, `SUMMARY.md`) this audit writes; the prep contract itself raises no content errors. Exit 0 after this audit. |
| 6 | All committed tables have results files | ✗ | T3 ✓, T4 ✓, but **T9 committed (tables_to_replicate.json) with no `results/table_9.md`** — see M1. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | Auditor independently recomputed all Table 3 decile returns/alphas/betas and the Table 4 QMJ + sub-factor rows from `data/panel.parquet` + ClickHouse FF; every value matches `table_3.md`/`table_4.md` to rounding. Profitability 4F = 0.488 (agent 0.49). |
| 8 | No orphan folders | ✗ | No literal-brace errors, but an empty nested `replications/quality_minus_junk/` skeleton exists at the slug root — see m1. |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md W1–W13 each carry a diagnosis + root cause + recommended fix; A1–A8 logged with rationale; W13 names the exact next-iteration fixes (FP beta, per-share growth). |
| 10 | Tier 2 within 2× magnitude | ✓ | Failing cells that stay within 2× (P1 excess 1.37×, QMJ MKT 0.78×) are Tier-2-eligible; middle-decile 4F alphas (≈0.30× of paper) are correctly treated as FAIL, not Tier 2. |

## 4. Issues the agent should have caught (didn't)

1. **Table 3 P10 Adjusted-R² gap (0.90 vs paper 0.59)** is shown in the comparison table but never discussed or excluded; a careful reviewer flags or footnotes a 0.31 discrepancy in a displayed cell (see m2).
2. **The orphan nested `replications/` skeleton** at the slug root was left in place (see m1).
3. **The sub-score cross-sectional correlations (0.25–0.56, avg ≈0.41)** are noticeably below the paper's reported component correlation (~0.67, Table 13) — worth a sanity note that the three composites are less tightly linked than in the paper, which is consistent with the weaker Safety/Growth signals (caveat: paper's 0.67 is for factor *returns*, not raw scores, so not directly comparable).
4. **"Monotonically increasing"** overclaims a series that is only almost-monotonic (see m3); the paper is careful to say "almost monotonically."

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Quality minus junk" (Asness, Frazzini,
Pedersen 2019) for slug `quality_minus_junk`. The previous agent run completed
with verdict **PARTIAL** (audit 1 at
`replications/quality_minus_junk/logs/audit1.md`). Read the audit first.

The good news: every number you produced was independently recomputed from
`data/panel.parquet` + ClickHouse FF factors and matches exactly — the
replication is honest and the core pipeline is sound (Profitability 4F alpha
0.49 vs paper 0.50). The QMJ factor replicates in sign, shape, and
significance (4F alpha 0.46, t=8.1) at ~77% of the paper's 0.60. The work
below closes the residual magnitude gap and the missing corollary/table tests.

## Issues to address (priority order)

### [M2] — MAJOR — Frazzini-Pedersen (2014) beta (root cause #1)
The Safety/BAB term uses a plain 60-month rolling CAPM beta
(`src/sql/06_beta_monthly.sql`) instead of FP(2014) (1-yr daily vol × 5-yr
3-day correlations; paper Appendix 1, `inputs/content.md:273`). This flattens
the Table 3 beta gradient (P3–P10 ≈ 0.95–1.01 vs paper 1.10→0.92) and weakens
Safety 4F alpha (0.36 vs 0.51) and the QMJ MKT loading (-0.16 vs -0.20).

**Specific fix:**
1. Implement FP(2014) beta from `crsp_202601.dsf` (daily stock returns) and
   `crsp_202601.dsi` (daily market): 252-day rolling std × 1260-day rolling
   3-day-return correlation. Replace the beta feeding the `bab` sub-variable.
2. Re-run `src/main.py`, then `src/table3.py` and `src/table4.py` unchanged.
3. Verify: Table 3 beta declines smoothly toward ~0.92 at P10; Safety 4F alpha
   moves from 0.36 toward 0.51; QMJ MKT loading moves from -0.16 toward -0.20.

### [M3] — MAJOR — per-share growth measures (root cause #2)
Growth sub-variables are not on a per-share basis (paper `inputs/content.md:255`
var_growth_per_share and the "lowercase = per share" note at L3866). This
weakens the Growth sub-score (Growth 4F alpha 0.28 vs 0.46).

**Specific fix:**
1. In `src/sql/02_funda_annual.sql`, divide the growth numerators by
   split-adjusted shares outstanding (`csho` + adjustment factors) so the
   5-year residual differences are per-share.
2. Re-run the pipeline and `src/table4.py`.
3. Verify: Growth 4F alpha moves from 0.28 toward 0.46.

### [M1] — MAJOR — implement committed Table 9 (spanning tests)
`results/table_9.md` is missing although T9 is committed in
`preparations/tables_to_replicate.json` (id "T9").

**Specific fix:**
1. Regress SMB, HML, UMD on the remaining standard factors, excluding and
   including QMJ (paper L3731).
2. Verify against the committed targets: SMB alpha 0.13→0.49 and HML alpha
   0.79→1.01 when QMJ is added; UMD alpha ~1.22 without QMJ.
3. Write `results/table_9.md` with a per-cell comparison block.

### [M4] — MAJOR — corollary: subsample stability
Paper Fig. 2 / Table 15 claim "no particular subsample driving our results"
(`inputs/content.md:2075`). Not computed.

**Specific fix:**
1. Add `results/table_4_subsample.md`: QMJ (and H-L) 4F alpha split into
   20-year windows and pre-/post-2008.
2. Verify the alpha stays positive and significant in every window.

### [M5] — MAJOR — corollary: FF5 / 6-factor robustness
Paper Table 5 (`inputs/content.md:2113`): QMJ alpha 16–38 bp/mo under FF5/FF6
with a large positive RMW loading. Not computed. `ff.five_factor_monthly` is
available.

**Specific fix:**
1. Add `results/table_5_robustness.md`: regress QMJ on FF5 and on FF6
   (FF5 + UMD).
2. Verify a positive alpha and a positive RMW loading.

### [M6] — MAJOR — QMJ UMD loading sign flip
UMD loading is +0.07 vs paper -0.09 (`results/table_4.md:14`). Likely resolved
by M2/M3, but verify.

**Specific fix:**
1. After M2/M3, re-check the UMD loading; if still positive, inspect the 12-1
   momentum of the Quality vs Junk legs.
2. Target: a small negative UMD loading.

### [m1]–[m3] — MINOR — cleanup
- Remove the empty nested `replications/quality_minus_junk/` skeleton at the
  slug root (m1).
- Footnote the Table 3 P10 Adj-R² 0.90-vs-0.59 gap as a likely extraction
  artifact outside the committed metrics (m2).
- Reword "monotonically increasing" to "rising on average / almost monotonic"
  to match the paper (m3).

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in
  `assumptions.md` must have all five fields: Diagnosis, Next fix, Before
  metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring
  `partial`, walk `assumptions.md` and verify every diagnosed problem has a
  non-empty `Next fix` and a before/after metric.

## Inputs you should read

- `replications/quality_minus_junk/logs/audit1.md` — this audit (full context)
- `replications/quality_minus_junk/inputs/content.md` — paper ground truth
- `replications/quality_minus_junk/preparations/` — prep contract
- `replications/quality_minus_junk/src/main.py` + `src/sql/` — current code
- `replications/quality_minus_junk/data/panel.parquet` — cached intermediates

## What NOT to redo

- Skip re-reading `SKILL.md`.
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact.
- Skip re-doing the ClickHouse catalog scan (`data_verification.json` is current).
- The analysis layer (sorts, regressions) is verified correct (W12 sensitivity:
  ≤0.04%/mo across breakpoint variants) — do NOT re-architect it; the gap is
  upstream in the score. **DO** re-run any sanity checks you add or modify.

## Deliverables for this iteration

- `src/sql/06_beta_monthly.sql` (FP 2014 beta) and `src/sql/02_funda_annual.sql`
  (per-share growth), with fix attempts logged per M2/M3.
- `results/table_9.md`, `results/table_4_subsample.md`,
  `results/table_5_robustness.md` (new), plus refreshed `table_3.md`/`table_4.md`.
- `preparations/assumptions.md` — append a five-field iteration entry per issue.
- `SUMMARY.md` — read only; do NOT edit (auditor-owned).
- `REPORT.md` — updated; lead with the data-quality summary and the
  before/after on QMJ 4F alpha, Safety/Growth alphas, and the beta gradient.

## Stop conditions

- **All majors fixed and verified** → re-run prep_validation.py + sanity checks
  → declare success or note remaining gaps; the next audit updates `SUMMARY.md`.
- **10-iteration cap reached** on one problem → escalate, write a partial
  `REPORT.md`; do not edit `SUMMARY.md`.
- **All blockers fixed but majors remain** → declare partial; document in
  `REPORT.md`. The auditor's REPLICATED/FAILED verdict is independent.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is a high-quality first iteration. The agent's reasoning trail
(`assumptions.md` W1–W13, A1–A8) is exemplary: every paper-silent decision is
logged with a rationale, and the worker correctly caught two spec errors that
would have destroyed the results (FF factors are decimals, not percents — W9;
ClickHouse `Date` saturates pre-1970 dates — W8). Critically, the agent
*self-diagnosed* the residual gap as upstream (W13) and proved it with a
3-variant breakpoint sensitivity (≤0.04%/mo), which my audit confirms: the
analysis layer is correct and the gap lives in the score construction. My
independent recomputation reproduced every reported value to rounding, so the
~77% headline magnitude is an honest, earned partial — not a reporting
artifact. The two score approximations (plain CAPM beta, non-per-share growth)
are the clear, actionable root cause and are exactly the right next-iteration
targets. The replication already merits REPLICATED (overall 3.17, no dimension
at 1) because the central claim — QMJ earns significant positive risk-adjusted
returns and quality stocks are safer — holds; the PARTIAL/`requires_iteration`
signal reflects the missing Table 9, the two methodology deviations, and the
uncomputed subsample/robustness corollaries, all of which are plausibly
closeable next iteration.
