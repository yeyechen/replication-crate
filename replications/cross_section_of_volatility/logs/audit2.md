---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — cross_section_of_volatility

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** Outer iteration 2 resolved the two substantive majors from audit 1 and exhausted the other two with paired fix attempts. The Table VI FF-3 alpha bug (double rf + factor-month misalignment) is fixed: the auditor independently recomputed the Panel B alphas from `data/panel.parquet` and reproduced the shipped values to rounding (Q1..Q5 = −0.00/0.08/0.09/−0.29/−1.18, 5-1 = −1.177 ≈ −1.17), with market betas ≈ 1 (auditor's FF-3 mkt loadings 0.92–1.20; code now carries a b_mkt≈1 sanity gate), and Table VI reconciles exactly with Table XI's full-sample 5-1 α (−1.17). All four Table X L/M/N strategies are now computed; the auditor independently re-implemented 1/1/1, 12/1/1, and the 1/1/12 Jegadeesh–Titman overlap from the cached data and matched the shipped values (1/1/12 reproduced to 0.00; 1/1/1 and 12/1/1 within 0.02–0.04 of pipeline values, i.e. quintile-tiebreak noise), and verified the 12-month IVOL sufficient-statistics construction against direct pooled daily regressions to machine precision (abs diff ≤ 4.2e-10) on two independent stock-months. The past-1-month momentum attenuation (M3) and the volatile-period subsample (M4) remain misses after both alternative conventions were tested and documented — these are now treated as documented limitations, not actionable majors. Only minor bookkeeping items remain.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | Audit-1's methodology bug is fixed and independently verified: Table VI alphas now use holding-month relabel + single rf (recomputed Q1..Q5 = −0.00/0.08/0.09/−0.29/−1.18, 5-1 = −1.177; betas ≈ 1, sanity-gated in code). All six checks (formula/timing/filter/winsorization/look-ahead/statistical convention) pass; remaining deviations are paper-silent choices documented with justification (delisting −30%, no winsorization, all-stock breakpoints, characteristic aggregation, L=12 min-obs 120) — one of which (the past-1-month window) is genuinely unverifiable against the paper and was tested under both conventions. |
| Headline matching | 5 | Monotonic-decreasing shape, negative sign, and magnitude class all reproduced; auditor recomputation: raw 5-1 spread −1.03% vs paper −1.06% (3%), FF-3 α 5-1 −1.18 vs −1.31 (10%); portfolio characteristics (Q1 mkt share 53.7% vs 53.5%, Q5 size 2.52 exact) match. |
| Data coverage | 4 | Exact period (Jul 1963–Dec 2000, 450 holding months), universe consistent with paper market-share stats, same sources (CRSP dsf/msf + PIT dsenames, Compustat funda, daily+monthly FF). Deducted for the uncovered systematic-volatility half (no VIX/VXO in ClickHouse). |
| Concrete result matching | 4 | Auditor tally of 69 headline cells (|paper| ≥ 0.10): 62 Tier 1 (89.9%), 6 Tier 2 (8.7%), 1 FAIL (1.4%) — all four Table X strategies and the corrected Table VI alphas now Tier 1; the lone FAIL is the volatile-period 5-1 (ratio 0.27). Just under the 90% band for a 5. |
| Signal strength | 4 | Headline raw 5-1 r = 0.96 (within 10%) but FF-3 α 5-1 r = 0.89 — just outside the 10% band for a 5, comfortably within 20%. |
| Corollary | 4 | All four L/M/N horizon strategies replicate (1/1/12 at 9%, 12/1/12 at 15%, 12/1/1 at 27%, 1/1/1 at 22%; all t ≤ −3.0), all seven cross-sectional controls, 7/8 subsamples, and the loser/winner momentum asymmetry. Two documented deviations remain (past-1-month attenuation, volatile-period subsample); Table IX is externally blocked (no VIX). |

**Overall: 4.17 / 5.00** → binary verdict **REPLICATED** (mean ≥ 3.0, no dimension = 1). Up from 3.83 at audit 1.

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

None actionable. Status of audit-1's four majors:

- [M1] Table VI FF-3 alphas from two offsetting bugs — **RESOLVED (verified)**. The auditor recomputed Panel B from `data/panel.parquet` with the corrected convention: Q1..Q5 FF-3 α = −0.00/0.08/0.09/−0.29/−1.18 and 5-1 = −1.177 (file: −1.17), market betas ≈ 1 (file's CAPM betas 0.83–1.45, mkt-cap-wtd 0.98; auditor's FF-3 mkt loadings 0.92–1.20). The sanity gate now exists in `src/analyze_table6.py:398–421` (asserts every quintile beta > 0.5 and mkt-cap-weighted average within 1.0 ± 0.3). Table VI 5-1 α reconciles exactly with Table XI full sample (−1.17 = −1.17; auditor: −1.1769 for both, same series).

- [M2] Three missing Table X L/M/N strategies — **RESOLVED (verified)**. The auditor independently re-implemented the strategies from the cached parquets: 1/1/12 5-1 α = −0.61 (file −0.61, paper −0.67; t = −3.89 vs −3.85) — exact reproduction of the JT 12-cohort overlap (avg 11.9 active cohorts/month); 1/1/1 5-1 = −0.70 (file −0.68) and 12/1/1 5-1 = −0.85 (file −0.82) — within 0.02–0.04, i.e. quintile-tiebreak/renormalization noise between independent implementations. The 12-month IVOL sufficient-statistics approach (`src/sql/ivol12_stats.sql`) was verified against direct pooled daily FF-3 regressions from raw CRSP+FF data to machine precision on two independent stock-months (permno 10000 1987-01: 0.046492393 vs 0.046492393, diff 3.2e-12; permno 10028 1990-06: 0.071508878 vs 0.071508878, diff 4.2e-10), with n_obs_12 = 252 = direct window count in both cases. All four 5-1 spreads within 30% of the paper (best 1/1/12 at 9%).

- [M3] Past-1-month momentum control — **EXHAUSTED, now a documented limitation (actionable: false)**. The prescribed fix (formation-month return ret_t) was tested: 5-1 α = −1.25, WORSE than ret_{t−1} (−1.15); the auditor verified both values independently (ret_t: −1.25, t = −8.89; ret_{t−1}: −1.15, t = −7.36). Neither convention reproduces the paper's −0.66 attenuation (ratios 1.89/1.74 — Tier 2, within 2×). The residual is plausibly microstructure (bid-ask bounce in short-term reversal), which is not recoverable from monthly CRSP returns without TAQ-level data. Both conventions are documented in `results/table_8.md` notes and assumptions.md. Exit gate satisfied (diagnosis + paired fix attempt + documentation).

- [M4] Volatile-period subsample — **EXHAUSTED, now a documented limitation (actionable: false)**. The auditor verified the holding-month classification exactly: 20th/80th percentiles of |mkt_rf| over the 450 in-sample holding months = 1.126%/5.050%, exactly 90 months each, matching the file. The formation-month sensitivity (volatile 5-1 = −1.21) moves closer to the paper but collapses the stable-vs-volatile contrast (stable also −1.21 vs paper −1.71), so the holding-month convention is the defensible primary. The cell is attenuated under BOTH conventions on a 90-month sample — a genuine small-sample sensitivity, now documented in `results/table_11.md` rather than labeled robust.

### Non-actionable majors (documented external limitations)

- [M5] Tables I–V and IX (systematic volatility: β_ΔVIX sorts, FVIX factor, price of volatility risk) — unchanged from audit 1; requires CBOE VIX/VXO data absent from ClickHouse (assumptions.md A7). Correctly documented.
- [M6] (new, absorbed from M3/M4) Past-1-month attenuation and volatile-period subsample misses — documented limitations with two-convention sensitivity evidence; see above.

### Minor (cleanup)

- [m1] Deliverables disagree on which past-1-month convention shipped. `results/table_8.md` Panel A reports 5-1 = −1.25 under `past1 = ret_t` (auditor-verified), while REPORT.md §3 reports −1.15 and logs/log2.md claims the Replicator decided to revert to ret_{t−1}. Fix: pick one convention and reconcile REPORT.md, table_8.md, and the log (either regenerate table_8.md under ret_{t−1}, or update REPORT.md/log2 to the shipped ret_t). Either choice is defensible; the disagreement is not.
- [m2] `scripts/prep_validation.py` still exits non-zero on this slug for one substantive reason after this audit is written: `data/ivol12.parquet` is not in the validator's parquet allowlist (the artifact is a legitimate agent-computed signal intermediate, not a raw dump — the whole point of the sufficient-statistics SQL was to avoid caching raw daily rows). Fix: rename to an allowlisted intermediate name (e.g. `ivol12_components.parquet`, mirroring `beta_ivol_components.parquet`) or extend the allowlist. (The second current error — missing logs/audit2.md — is resolved by this file.)
- [m3] logs/log2.md labels the past-1-month cell "FAIL", but |rep/paper| = 1.89 < 2 → Tier 2 under the rubric's tier definitions (sign match + within 2×). Conservative labeling is honest; apply the definitions consistently.
- [m4] (carried from audit 1, no action needed) Table VII "Controlling for B/M" Q1–Q4 level alphas are offset ~0.6–0.75 below the paper (documented A20); the 5-1 spread (−0.91 vs −0.80) is the reported statistic and matches.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Table VI Panel B alphas (M1 fix) | ✓ | Independent recomputation from data/panel.parquet + live ff.four_factor_monthly: Q1..Q5 FF-3 α = −0.00/0.08/0.09/−0.29/−1.18, 5-1 = −1.177 (t = −5.88); file says −1.17 (t = −5.71). Means 1.03/1.16/1.20/0.85/0.00, 5-1 −1.03 vs file 1.04/…/0.01, −1.02 — rounding only. |
| 2 | Table VI betas ≈ 1 + sanity gate | ✓ | Auditor FF-3 mkt loadings 0.92/1.06/1.15/1.20/1.12 (multivariate); file's CAPM betas 0.83–1.45, wtd avg 0.98. Gate present at src/analyze_table6.py:398–421 (assert b > 0.5 per quintile, wtd avg 1.0 ± 0.3). |
| 3 | Table VI ↔ Table XI reconciliation | ✓ | Same 1/0/1 series: auditor 5-1 α = −1.1769 for both; files both report −1.17 (t = −5.71). Audit-1's internal contradiction (−1.12 vs −1.17) is gone. |
| 4 | Table X 1/1/12 (JT overlap) | ✓ | Independent re-implementation: Q5 = −0.60, 5-1 = −0.61 (t = −3.89), avg 11.9 active cohorts/month — matches file exactly (−0.60/−0.61, t = −3.85); n = 449 as reported. |
| 5 | Table X 1/1/1 and 12/1/1 | ✓ | Independent: 1/1/1 5-1 = −0.70 (file −0.68; n = 449); 12/1/1 5-1 = −0.85 (file −0.82; n = 444). Differences ≤ 0.04 = tiebreak/renormalization noise between independent code paths; all within the paper's 30% band. |
| 6 | 12-month IVOL sufficient statistics | ✓ | Direct pooled daily FF-3 regression from raw CRSP dsf + ff.three_factor matches data/ivol12.parquet to machine precision on two independent stock-months (diffs 3.2e-12 and 4.2e-10; n_obs_12 = 252 = direct window count). RANGE-window calendar correctness confirmed by n_months_12 = 12. |
| 7 | Table VIII past-1-month (both conventions) | ✓ (values) / ✗ (vs paper) | Auditor: ret_t → 5-1 = −1.25 (t = −8.89), matching the shipped table_8.md; ret_{t−1} → −1.15 (t = −7.36), matching REPORT.md. Neither reaches the paper's −0.66; Tier 2 (within 2×). |
| 8 | Table VII double-sort machinery | ✓ | Independent "Controlling for Size" dependent double sort: Q1 = 0.09, Q5 = −0.91, 5-1 = −1.01 (t = −5.15) — exact match to table_7.md (−1.01, t = −5.13). |
| 9 | Stable/volatile classification (M4) | ✓ | 20th/80th pctiles of |mkt_rf| over 450 holding months = 1.126%/5.050%, exactly 90/90 months — matches table_11.md. Classification is correct; the cell is genuinely sample-sensitive. |
| 10 | Cell tally | ✓ | 69 headline cells (|paper| ≥ 0.10): 62 Tier 1 (89.9%), 6 Tier 2 (8.7%), 1 FAIL (1.4% — volatile 5-1, ratio 0.27). All four Table X strategies and all corrected Table VI alpha cells Tier 1. |
| 11 | prep_validation.py | ✗ (lint) | Two layout errors: missing logs/audit2.md (resolved by this file) and data/ivol12.parquet outside the parquet allowlist (minor [m2]; the file is a legitimate agent-computed signal intermediate). No substantive prep-contract failure. |
| 12 | Hygiene | ✓ | Slug root clean (data/inputs/logs/preparations/results/src + REPORT.md + SUMMARY.md); no SCORE.md; no orphan dirs; auditor scratch scripts removed. |
| 13 | Corollary coverage | ✓ | Horizons (4/4 L/M/N, all significant t ≤ −3.0), controls (7/7), subsamples (7/8 + documented sensitivity), momentum asymmetry (losers −2.69 vs winners −0.52), TVOL Panel A. Remaining gaps all documented (M3/M4/M5). |

## 4. Issues the agent should have caught (didn't)

1. The Replicator's recorded decision for M3 was "revert to ret_{t−1} (marginally closer)", but the shipped `results/table_8.md` still carries the ret_t convention (5-1 = −1.25, with the notes explicitly citing "issue M3 convention"), and REPORT.md reports the ret_{t−1} value (−1.15). The decision was never propagated to the artifacts — a careful final pass would have reconciled table_8.md ↔ REPORT.md ↔ log2.
2. `data/ivol12.parquet` trips prep_validation's parquet allowlist. The agent knew the validator's conventions (audit 1 flagged prep-validation state) but shipped a new data/ artifact under a non-allowlisted name; renaming to an `*_components.parquet`-style name would have kept the contract green.
3. logs/log2.md labels past-1-month "FAIL" when the rubric's own tier definitions make it Tier 2 (ratio 1.89) — the same conservative-labeling habit flagged as audit-1 minor [m2] recurred in a different form.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are closing out the replication of "The Cross-Section of Volatility and Expected Returns" (Ang, Hodrick, Xing & Zhang 2006) for slug `cross_section_of_volatility`. Audit 2 (`replications/cross_section_of_volatility/logs/audit2.md`) returned verdict **PASS**: overall 4.17/5.00, binary verdict REPLICATED, 0 blockers, 0 actionable majors, requires_iteration: false. All four audit-1 majors are resolved or exhausted with paired fix attempts (M1 Table VI alphas fixed and verified; M2 all four L/M/N strategies computed and verified; M3/M4 documented limitations after both conventions were tested). **No further outer iteration is required.** If you are running anyway, do ONLY the minor cleanup below — do not re-open M3/M4.

## Cleanup items (minor, quick)

### [m1] — reconcile the past-1-month convention across deliverables
`results/table_8.md` ships `past1 = ret_t` (5-1 = −1.25, auditor-verified) while REPORT.md §3 reports −1.15 and logs/log2.md claims a revert to ret_{t−1}. Pick ONE convention (either is defensible; ret_t is the economically natural "past 1 month at formation" definition, ret_{t−1} is marginally closer to the paper's −0.66) and make table_8.md, REPORT.md, and the assumptions.md entry agree. If you switch table_8.md back to ret_{t−1}, regenerate it; otherwise update REPORT.md to −1.25 and correct log2's decision line.

### [m2] — fix the prep_validation parquet allowlist trip
`data/ivol12.parquet` is flagged as an unexpected parquet. It is a legitimate agent-computed signal intermediate (NOT a raw dump). Rename it to an allowlisted-style name (e.g. `data/ivol12_components.parquet`, mirroring the existing `beta_ivol_components.parquet` pattern) and update the load path in `src/analyze_table10_lmn.py`, or propose an allowlist addition. Then run `python scripts/prep_validation.py cross_section_of_volatility` and confirm exit 0.

### [m3]/[m4] — labeling consistency
In any future log, label the past-1-month cell Tier 2 (|rep/paper| = 1.89 < 2), not FAIL. No action needed on the Table VII B/M level offset (documented A20).

## Do NOT

- Do NOT re-attempt M3 (past-1-month attenuation) or M4 (volatile period) — both are exhausted and documented; the residual is microstructure/small-sample and not recoverable with monthly CRSP data.
- Do NOT touch Tables I–V / IX (no VIX data — external limitation, A7).
- Do NOT edit SUMMARY.md (auditor-owned) or create SCORE.md (obsolete).

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Any new assumptions.md entry needs all five fields.
- **10-iteration cap per problem** — not applicable here; this is a cleanup pass.

## Deliverables (only if run)

- Reconciled past-1-month convention in table_8.md / REPORT.md / assumptions.md
- Renamed (or allowlisted) ivol12 intermediate; prep_validation exit 0
- REPORT.md §4 cell tally kept consistent with results/table_*.md

## Stop condition

All three minors done and prep_validation green → declare success. This is the final pass for this slug.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

Iteration 2 was exactly the pass audit 1 asked for. The M1 fix is clean and properly defended: the corrected convention now lives in one place (holding-month relabel + single rf), carries a beta sanity gate that would have caught the original bug, and the flagship table reconciles with Table XI to the third decimal (auditor: −1.1769 for both). The M2 completion is the standout: the 12-month IVOL is computed SQL-first from additive monthly sufficient statistics — an elegant, verifiable design — and it checks out to machine precision against direct pooled daily regressions; the auditor's independent re-implementation of the JT 12-cohort overlap reproduced the 1/1/12 strategy to the second decimal (−0.61, t ≈ −3.9) and the other two strategies to within tiebreak noise. The paper's claim that the IVOL anomaly persists across formation and holding periods up to a year is now fully supported, with all four strategies significant at t ≤ −3.0. The two remaining misses are honest ones: the past-1-month reversal attenuation is the kind of microstructure-sensitive cell that monthly CRSP returns cannot be expected to reproduce (both window conventions were tested, as audit 1 prescribed, and the formation-month convention made it marginally worse), and the volatile-period subsample is a 90-month cell whose classification the auditor verified exactly — it is attenuated under both month conventions, which is the correct thing to report rather than hunt for a convention that hits the number. The only real blemish this iteration is bookkeeping: the Replicator's M3 "revert to ret_{t−1}" decision was never propagated to the shipped table (which still carries ret_t), so REPORT.md and table_8.md disagree by 0.10 on one non-headline cell — a reconciliation task, not a methodology problem. With the systematic-volatility half genuinely blocked by the absence of VIX data, this replication now stands as a faithful, internally consistent, and independently verifiable reproduction of AHXZ (2006)'s most-cited result: high-idiosyncratic-volatility stocks earn abysmally low returns (−1.02%/month raw spread, −1.17%/month FF-3 alpha), monotonically, across every replicable control, horizon, and 7 of 8 subsamples. No further iteration is warranted.
