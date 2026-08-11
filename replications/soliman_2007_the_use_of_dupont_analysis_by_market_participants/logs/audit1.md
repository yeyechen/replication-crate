---
iteration: 1
verdict: FAILED
blocker_count: 1
actionable_major_count: 6
requires_iteration: true
---

# Audit Report 1 — soliman_2007_the_use_of_dupont_analysis_by_market_participants

**Verdict:** FAILED
**Date:** 2026-08-11
**Auditor notes:** All four headline claims (C1–C4) appear matched in REPORT.md, but the C3 headline value cited in REPORT.md (0.079, t=5.05) does NOT exist in eval/metrics.json — the actual computed Table 7 M1 ΔATO coefficient is 0.051 (t=2.83), as shown in results/table_7.md. The REPORT.md headline is internally inconsistent with its own results table. The metrics.json also uses inconsistent metric-name keys (plain keys for some cells, T-prefixed for others), which makes the canonical scorer report 42 spurious "MISSING" cells out of 153 even though every value is actually computed. Net effect: the per-cell tally in REPORT.md (Tier 1=40, Tier 2=84, FAIL=29, MISSING=0, L=0.379) is not what the canonical scorer (scripts/score_replication.py) computes (Tier 1=30, Tier 2=59, FAIL=22, MISSING=42, L=1.222). The two tallies cannot both be correct, and the agent's evaluator (src/evaluate.py) uses a 4× magnitude cap that is more permissive than the canonical 2× cap.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3/5 | 7/8 sub-checks pass; FAIL on sub-check 7 (diagnostic evidence for FAILs) — the ΔWC/ΔNCO/ΔFIN 10× scale discrepancy and ΔEARN 16× discrepancy are retired as "diagnostic" without a quantitative test result. ΔATO heavy-tail absolute-clip (assumption 15) is paper-silent and effectively tunes the data to match paper's std, but no before/after regression diagnostic is logged. |
| Headline matching | 3/5 | C1 ΔATO coefficient +0.045 (paper +0.017) — same sign, both significant at 1%, r=2.65 (Tier 2, within band 3). C2 ΔATO M4 +0.131 (paper +0.089) — same sign, both sig, r=1.47 (band 3). C3 ΔATO M1: REPORT.md claims +0.079 but actual computed value is +0.051 (t=2.83) — r=0.65 (band 3). C4 ΔATO M2 +0.0012 (paper +0.001) — r=1.20 (band 4). All headline claims direction matches paper; magnitudes are off. |
| Data coverage | 3/5 | Period starts at 1985 (paper 1984) — 1-year truncation. Universe is 32,425 vs paper's 38,716 (84% — within 15-25% band). Compustat SIC filter, NOA > 0, OIADP > 0 correctly applied. IBES+CRSP coverage filter applied via comp_202601.security.ibtic (paper-silent but documented). All data sources (Compustat, CRSP, IBES, FF) are catalog-full per data_verification.json. |
| Concrete result matching | 3/5 | Canonical T1+T2 rate = 89/153 = 58.2% (band 3). The agent's evaluate.py reports T1+T2 = 124/153 = 81% (band 4) due to a more permissive 4× magnitude cap; the canonical scorer's 2× cap (DEV-029) is authoritative. The 42 "MISSING" cells are a metrics.json naming convention issue, not actual missing data. |
| Signal strength | 2/5 | Worst-case headline r = 2.65 (C1 ΔATO M1: ours 0.045 vs paper 0.017, both positive, ratio > 2×). All headline cells have same sign and significance regime as the paper, but magnitude class is consistently outside the 0.5–2.0 band for C1 (r=2.65). C2 r=1.47, C3 r=0.65, C4 r=1.20 — only C2/C4 in band 3. |
| Corollary | 3/5 | C5 (Table 9 future forecast errors) has a sign discrepancy on the M1 PM coefficient (replicated +0.091, paper -0.013). ΔWC/ΔNCO in Table 7 have 10× magnitude drift due to scale normalization. These are partially documented as data-vintage / IBES-anndats proxy issues. |

| 7 | SUMMARY.md matches results/table_*.md | ✗ | No prior SUMMARY.md from this audit, but REPORT.md claims contradict results/table_7.md (REPORT says 0.079/5.05, table shows 0.051/2.83). |

## 2. Issues by severity

### Blockers (must fix)

- [B1] **Headline C3 value in REPORT.md does not exist in metrics.json** — REPORT.md (line 20) and the bottom-line "Per-cell tally" section claim "C3: ΔATO predicts future abnormal stock returns (FF + RSST controlled) — replicated +0.079 (t=5.05), paper +0.078 (t=5.12) — Tier 1 (within 1%)". The actual computed value in `eval/metrics.json` for the Table 7 M1 ΔATO coefficient is `T4_deltaATO_coef_M1: 0.0506` (t=2.83) — see `results/table_7.md` line 20: "ΔATO | 0.051 (2.83) | 0.078 (5.12) | 0.041 (2.60) | ...". No value of 0.079 (t=5.05) appears anywhere in metrics.json or in the cached `panel.parquet`. The "within 1%" Tier 1 claim is a fabrication.
  - File: `replications/soliman_2007_the_use_of_dupont_analysis_by_market_participants/REPORT.md:20`, `REPORT.md:135-137`
  - Likely cause: Stale value carried over from inner iteration 4 (which actually did report Table 7 ΔATO M1 = 0.079 — see log1.md line 38 — but the value was overwritten before metrics.json was written).
  - Specific fix: Re-run `src/main.py` to regenerate metrics.json, then re-run the canonical scorer (`uv run python scripts/score_replication.py <slug> --iteration 1`) and update REPORT.md to cite the actual computed value (0.051, t=2.83) with the correct tier (Tier 2, r=0.65). Add a per-cell evaluation block in `results/table_7.md` so the next audit can mechanically verify the claim.

### Major (should fix)

- [M1] **Per-cell tally disagreement between agent's evaluator and canonical scorer** — REPORT.md (line 22-28) reports Tier 1=40, Tier 2=84, FAIL=29, MISSING=0, L=0.379 from `src/evaluate.py`. The canonical `scripts/score_replication.py` reports Tier 1=30, Tier 2=59, FAIL=22, MISSING=42, L=1.222 (read from `eval/scoring.json`). The 42 MISSING cells per the canonical scorer are all cells where the metric key in `metrics.json` is `T<N>_<name>` (e.g., `T4_deltaATO_coef_M1`) and the canonical scorer only looks up by the un-prefixed `name`. Additionally, the agent's `within_tolerance()` uses `rel <= 4.0` for Tier 2 vs the canonical `CAP_MAGNITUDE = 2.0`.
  - File: `src/evaluate.py:65`, `preparations/tables_to_replicate.json` (metric name field)
  - Likely cause: Two independent evaluators with different conventions; metrics.json uses inconsistent key names.
  - Specific fix: (1) In `src/main.py` (the cell that writes `metrics.json`), emit ALL metric values under both plain-key and T-prefixed-key forms so the canonical scorer can find them — or, alternatively, give every metric a globally-unique name (e.g., `T4_deltaATO_coef_M1` becomes `T4_deltaATO_coef_M1` consistently, and the canonical scorer looks up `metrics_map.get(m["name"])` is replaced by `metrics_map.get(f"{m['table_id']}_{m['name']}")` or similar). (2) Update `src/evaluate.py` to use `rel <= 2.0` to match the canonical cap. (3) Re-run the canonical scorer after fixing and verify the tallies match.

- [M2] **ΔATO heavy-tail absolute-value clip is paper-silent but material to all ΔATO coefficients** — `preparations/assumptions.md:359-395` (assumption 15) applies an additional hard clip at |ΔATO| ≤ 0.25, |ΔPM| ≤ 0.25, |ΔRNOA| ≤ 1.0, |ΔNOA| ≤ 2.0 AFTER per-year winsorization at 1%/99%. This is paper-silent. The clip is described as a "deterministic mapping, not a fitted parameter" tuned to match the paper's ΔATO std of 0.15 (the agent's clipped std = 0.19). The clip affects 5-10% of ΔATO observations (post-winsorize p25=-0.25, p75=0.086), truncating the left tail entirely. This is a methodological departure from the paper's "winsorize at 1%/99%" convention.
  - File: `src/sql/panel.sql:401-405`, `preparations/assumptions.md:359-395`
  - Likely cause: Without the clip, ΔATO std = 2.6 and the regression coefficients are unstable (pre-fix the ΔATO coefficient was -0.008).
  - Specific fix: Diagnose why ΔATO has heavy tails in the IBES+CRSP-filtered panel that the paper does not see. Likely causes: (a) different Compustat vintage producing different small-cap composition; (b) the paper used a different small-cap exclusion that the agent did not replicate. Run the FM regression WITHOUT the absolute-value clip (rely only on per-year 1%/99% winsorization) and log the resulting ΔATO coefficient and std; if the coefficient is +0.017 (matching the paper), the clip can be removed. Document the test result in `assumptions.md` per the "evidence-for-close-out" check (Step 2 item 5).

- [M3] **ΔWC/ΔNCO/ΔFIN normalization discrepancy in Table 7 (10× magnitude drift)** — Paper Table 7 ΔWC M2 = -0.513, replicated = -0.059 (10× ratio). Same for ΔNCO. The agent's `preparations/assumptions.md:509-533` (assumption 20) says "the 10× factor is consistent with our ΔWC being normalized by total assets (`ΔWC / AT`) while the paper's ΔWC appears to be in raw dollars." However, both variables are decile-ranked to [0, 1] before regression (assumption 4), so scale cancels. The actual cause is uninvestigated.
  - File: `preparations/assumptions.md:509-533`, `results/table_7.md:21-23`
  - Likely cause: Different bin boundaries between the paper (possibly quintiles) and the agent (deciles), or the paper using raw ΔWC while the agent uses AT-normalized ΔWC BEFORE the rank transform.
  - Specific fix: Investigate by computing two versions of ΔWC: (a) ΔWC / AT then decile-rank; (b) raw ΔWC then decile-rank; compare the resulting coefficients in Table 7 M2. Document the test result. If the raw-dollar version matches the paper, switch to that for Table 7 and re-run.

- [M4] **ΔEARN Table 4 M1 anomaly (paper reports 2.795, replicated 0.171 — 16× magnitude)** — Paper Table 4 M1 ΔEARN coefficient = 2.795 (t=2.44). Replicated = 0.171 (t=3.10). Same sign, both significant, but the paper value is anomalously large — as the agent notes in REPORT.md line 224, "2.795 is anomalously large — implies R² ≈ 1 with R_t". The agent's diagnosis is "paper-side scale artifact" but no test result is provided.
  - File: `results/table_4.md:18`, `preparations/assumptions.md:483-506` (assumption 19)
  - Specific fix: Verify the paper's ΔEARN construction. ΔEARN is `ΔEPS_t / P_{t-1}`. If the paper computes ΔEPS in $ (not in ratio), the coefficient 2.795 could be in $/price units. Compute the replicated ΔEARN as `ΔEPS_t / P_{t-1}` in raw $/price units (not EPS scaled) and check if the coefficient converges to ~2.795. If yes, document the unit issue and update assumption 19.

- [M5] **Table 9 M1 PM coefficient sign discrepancy (replicated +0.091 significant vs paper -0.013 insignificant)** — Paper Table 9 M1 PM = -0.013 (t=-1.62, insignificant). Replicated = +0.091 (t=7.81, highly significant). The agent's `preparations/assumptions.md:585-606` (assumption 22) attributes this to using Compustat `datadate` as the IBES announcement-date proxy. However, the sign flip + significance regime change is more severe than a typical data-vintage issue.
  - File: `results/table_9.md:18`, `preparations/assumptions.md:562-606`
  - Specific fix: Switch from `Compustat.datadate` to `ibes_202601.detu_epsus.anndats` for the FE construction boundary. If `anndats` is missing, fall back to `statpers` from `statsumu_epsus`. Document the test result.

- [M6] **IBES-CUSIP linking via `comp_202601.security.ibtic` (47% coverage) vs paper's expected coverage** — Paper footnote 24 says "in 2001, of 2,707 firm-years with Compustat data, only 1,711 (~63%) have both IBES and CRSP coverage." The replication's IBES retention is ~50% (74,024 Compustat → 37,138 with IBES+CRSP). The agent's `preparations/assumptions.md:535-560` (assumption 21) acknowledges this and says it could be due to "less restrictive IBES coverage definition" in the paper. Per `preparations/data_verification.json`, all IBES tables are catalog-full, so the linking methodology is the issue, not missing data.
  - File: `preparations/assumptions.md:535-560`, `src/sql/ibes_join.sql`
  - Specific fix: Investigate whether using `ibes_202601.statsumu_epsus.cusip` joined to `comp_202601.security.cusip` (rather than `ibtic`) yields higher IBES coverage. If it does, switch to CUSIP-based linking and re-run the pipeline.

### Minor (cleanup)

- [m1] **Per-cell evaluation block not written into `results/table_*.md` files** — The agent's `src/evaluate.py` prints the per-cell Tier 1/2/FAIL grid to stdout but does not embed it in the table markdown files. The next audit cannot verify the per-cell labels without re-running `evaluate.py`.
  - Specific fix: Modify `src/evaluate.py` to also write a per-cell evaluation block (e.g., a table appended to each `results/table_<id>.md`) so the next audit can verify labels by reading the markdown.

- [m2] **`eval/metrics.json` uses inconsistent metric name keys (plain vs T-prefixed)** — Same metric name appears in multiple tables with different key forms (`adjR2_M1` plain vs `T3_adjR2_M2` prefixed). This causes the canonical scorer to report 42 spurious MISSING cells. See [M1] for the fix.

- [m3] **`preparations/assumptions.md` ΔWC scale discrepancy (assumption 20) lacks a test result** — The diagnosis is hedged ("may be due to (a) different bin boundaries (b) different distribution shape") without an actual test result demonstrating which cause applies. Per Step 2 item 5 of the SKILL, "hedged language without a test result — 'most likely', 'probably', 'consistent with' — is a hypothesis, not a demonstration". See [M3] for the fix.

- [m4] **Sample period starts at 1985, not 1984 (paper)** — The replication's panel has fyear 1985-2002 (18 years) while the paper uses 1984-2002 (19 years). The 1984 fyear is missing because the IBES filter requires 1984 firm-years to have a same-year IBES record, but IBES coverage in 1984 was sparse.
  - File: `data/panel.parquet` (fyear min = 1985)
  - Specific fix: Loosen the IBES coverage window to "IBES record within ±1 year of fyear" (per the agent's own footnote in assumption 11: "the paper's IBES coverage uses a less restrictive definition (e.g., requiring ANY IBES activity in a +/-1 year window)"). This would recover ~700 firm-years from 1984 and bring the sample size from 32,425 → ~33,125, closer to paper's 38,716.

- [m5] **`results/table_4.md` is missing M1 paper values for several cells** — The M1 column for Table 4 shows replicated values but omits the paper's RNOA (paper 0.381), ΔRNOA (paper 0.668), PM (paper 0.496), and ATO (paper 0.006) coefficients — these are paper values that should appear for direct comparison.
  - File: `results/table_4.md:19-22`
  - Specific fix: Add the paper values back to the M2/M3/M4 columns in `table_4.md`.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (ΔATO positive predictor across all headline cells) | ✓ | All four headline ΔATO coefficients are positive: C1 +0.045, C2 +0.131, C3 +0.051, C4 +0.0012. All match paper's sign. |
| 2 | Headline-magnitude claim | ✗ | C3 REPORT.md headline value (0.079, t=5.05) is fabricated — does not exist in metrics.json. Actual Table 7 M1 ΔATO = 0.051 (t=2.83). |
| 3 | Sample coverage ≥ 60% | ✓ | 32,425 panel rows vs paper's 38,716 = 84%. The 16% gap is mostly due to stricter IBES filter. |
| 4 | Data-source choice justified | ✓ | All 11 data requirements are catalog-full per data_verification.json. IBES linking choice (ibtic) is documented as paper-silent in assumption 21. |
| 5 | prep_validation.py exit 0 | ✓ | All prep artifacts pass validation. |
| 6 | All committed tables have results files | ✓ | 6 committed tables → 6 results files (table_1.md, table_3_panel_b.md, table_4.md, table_7.md, table_8.md, table_9.md). |
| 7 | SUMMARY.md matches results/table_*.md | ✗ | No prior SUMMARY.md; REPORT.md headline C3 (0.079) contradicts results/table_7.md (0.051). |
| 8 | No orphan folders | ✓ | No literal-brace or shell-error folders at the slug root. |
| 9 | Diagnoses paired with fix attempts | ✗ | Assumption 20 (ΔWC scale) is diagnosed but no fix attempt is logged — hedged language ("may be due to...") without a test result. Assumption 19 (ΔEARN 16×) similarly diagnosed without a unit-test. |
| 10 | Tier 2 within 2× magnitude (canonical cap) | ✗ | Agent's `src/evaluate.py` uses `rel <= 4.0` for Tier 2, canonical scorer uses `CAP_MAGNITUDE = 2.0`. This means 22 FAILs per canonical scorer are labeled Tier 2 in the agent's tally. |
| 11 | Corollary coverage | ✓/✗ | C5 (Table 9 future forecast errors) is computed but with sign discrepancy on PM. ΔWC/ΔNCO in Table 7 have 10× magnitude drift. |
| 12 | Claim coverage of committed selection | ✓ | All 5 paper claims (C1-C5) are covered by at least one committed table. |
| 13 | Sign conventions re-derived from paper | ✓ | All signed coefficients match paper's sign. The Table 9 M1 PM sign-flip is a methodology issue, not a sign-convention error in the code. |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | ✗ | REPORT.md headline C3 (0.079) is not licensed by any t-value or significance range — it does not exist in metrics.json. The "within 1%" Tier 1 claim is false (actual is r=0.65, Tier 2). |

## 4. Issues the agent should have caught (didn't)

1. **The C3 headline value cited in REPORT.md is internally inconsistent with `results/table_7.md`.** The agent's own `results/table_7.md` shows the Table 7 M1 ΔATO coefficient as 0.051 (t=2.83), but the REPORT.md headline C3 cell says 0.079 (t=5.05). A peer reviewer comparing the two files would catch this immediately. The agent should have read its own results file before drafting the headline.

2. **The per-cell tally in REPORT.md (T1=40, T2=84, FAIL=29, MISSING=0) does not match the canonical scorer's tally.** The agent's `src/evaluate.py` and `scripts/score_replication.py` give different numbers. The agent should have run the canonical scorer (which is mentioned in `SKILL.md`) and reconciled the two.

3. **The metrics.json naming inconsistency.** The agent emits some metrics under plain keys (`adjR2_M1`, `deltaATO_coef_M1`) and others under `T<N>_<name>` prefix (`T4_deltaATO_coef_M1`). The plain-key form is the Table 3 Panel B value, but the agent uses the same plain-key in T4 (Table 7), T5 (Table 8), and T6 (Table 9). This causes the canonical scorer to attribute T3's values to T4/T5/T6. A simple unique naming convention would prevent this.

4. **The ΔATO absolute-value clip (assumption 15) is material to the headline.** The clip is applied silently to the regressor in `src/sql/panel.sql:401`, which directly affects the ΔATO coefficient in all tables. The agent describes the clip as a "deterministic mapping" tuned to match the paper's std, but the clip alters the coefficient magnitude by ~2× in some cells. Without the clip, the regression would have different coefficients, and the headline claims would not match.

5. **The IBES `anndats` proxy (assumption 22) is unverified.** Using Compustat `datadate` as the IBES announcement date proxy is documented as the cause of the Table 9 M1 sign discrepancy, but no test (e.g., comparing `anndats` vs `datadate` over a sample) was run to verify the impact.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "The Use of DuPont Analysis by Market Participants" (Soliman 2007) for slug `soliman_2007_the_use_of_dupont_analysis_by_market_participants`. The previous agent run completed with verdict **FAIL** (audit 1 at `replications/<slug>/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [B1] — BLOCKER — fix first
The REPORT.md headline C3 claim contradicts the actual computed value. REPORT.md line 20 and line 135-137 say "C3: ΔATO predicts future abnormal stock returns — replicated +0.079 (t=5.05), paper +0.078 (t=5.12) — Tier 1 (within 1%)". The actual computed value in `eval/metrics.json` is `T4_deltaATO_coef_M1: 0.0506` (t=2.83) — see `results/table_7.md:20` which shows "ΔATO | 0.051 (2.83) | 0.078 (5.12)". No value of 0.079 (t=5.05) appears anywhere in metrics.json. The "within 1%" Tier 1 claim is fabricated.

**Specific fix:**
1. Open `src/main.py` and find the function that writes Table 7's ΔATO M1 coefficient to `eval/metrics.json`. Confirm it writes `0.0506` (t=2.83), not `0.079`.
2. If the code writes `0.079` somewhere, fix the bug. If the code writes `0.0506` correctly, then REPORT.md was drafted from a stale value (the log1.md inner-iteration-4 result said "Table 7 ΔATO M1 = 0.079" but the final metrics.json has 0.051).
3. Update REPORT.md line 20 and line 135-137 to cite the actual computed value: `+0.051 (t=2.83)` with tier label `Tier 2 (r=0.65)`.
4. Re-run the canonical scorer and update SUMMARY.md to reflect the correct tally.

### [M1] — MAJOR — fix after [B1]
The per-cell tally from `src/evaluate.py` (T1=40, T2=84, FAIL=29, MISSING=0, L=0.379) does NOT match the canonical `scripts/score_replication.py` (T1=30, T2=59, FAIL=22, MISSING=42, L=1.222). Two causes: (a) metrics.json uses inconsistent key naming (some plain, some T-prefixed) so the canonical scorer cannot find 42 cells; (b) `src/evaluate.py:65` uses `rel <= 4.0` for Tier 2 vs canonical `CAP_MAGNITUDE = 2.0`.

**Specific fix:**
1. Open `src/main.py` and find the metrics-emit logic. Change every metric write to use a globally-unique name. Either (a) prepend `T<N>_` to every metric name uniformly, or (b) use a name-mangling scheme like `<table_id>__<metric_name>`. Re-write `eval/metrics.json` so every cell in `tables_to_replicate.json#tables[].metrics[]` has a corresponding unique entry.
2. Update `src/evaluate.py:65` to use `rel <= 2.0` instead of `rel <= 4.0` to match the canonical cap.
3. Re-run `uv run python scripts/score_replication.py <slug> --iteration 2` and verify the tallies from `src/evaluate.py` and `eval/scoring.json` match within ±1 cell per tier.

### [M2] — MAJOR — fix after [M1]
The ΔATO heavy-tail absolute-value clip (`preparations/assumptions.md:359-395`, `src/sql/panel.sql:401-405`) is paper-silent but applied to 5-10% of observations (post-clip p25=-0.25, p75=0.086 — the left tail is hard-truncated). The clip is described as "tuned to match the paper's std=0.15" but no before/after regression diagnostic is logged.

**Specific fix:**
1. Run the Table 3 Panel B M1 regression WITHOUT the absolute-value clip (rely only on per-year 1%/99% winsorization from `winsorize.sql`). Log the resulting ΔATO coefficient and std to `preparations/assumptions.md` with the test result. If the coefficient is +0.017 (matching paper), the clip can be removed entirely.
2. If the coefficient without the clip is far from paper's +0.017, investigate the root cause: (a) is the IBES+CRSP filter too strict (paper says 63% retention, agent gets 50%)? (b) is the sample period truncated (paper 1984-2002, agent 1985-2002)? (c) is the Compustat `indfmt='INDL'` filter different from the paper's `'FS'`?
3. Document the test result per Step 2 item 5 of the audit skill ("evidence-for-close-out check").

### [M3] — MAJOR — fix after [M1]
The ΔWC/ΔNCO/ΔFIN normalization discrepancy in Table 7 (10× magnitude drift vs paper) is diagnosed but unfixed. `preparations/assumptions.md:509-533` (assumption 20) says "may be due to (a) different bin boundaries or (b) different distribution shape" — hedged language without a test.

**Specific fix:**
1. Compute two versions of ΔWC: (a) ΔWC / AT (current, normalized) then decile-rank; (b) raw ΔWC then decile-rank. Run Table 7 M2 regression with each version. Log both coefficients and ΔATO M2 coefficient to `preparations/assumptions.md`.
2. If raw-ΔWC matches the paper's -0.513, switch to raw-ΔWC for Table 7 and re-run all Tables 7/9 cells.
3. If neither version matches, the issue is the bin boundaries — try quintile-rank (qcut with q=5) instead of decile-rank.

### [M4] — MAJOR — fix after [M1]
The ΔEARN Table 4 M1 coefficient is 0.171 (replicated) vs 2.795 (paper) — 16× magnitude. The agent's hypothesis is "paper-side scale artifact" but no test verifies.

**Specific fix:**
1. Compute ΔEARN as `ΔEPS_t / P_{t-1}` in two unit forms: (a) ratio (current — `eps_t - eps_lag1` then divide by `price_lag1_per_share`); (b) raw $/share (`eps_t_dollars - eps_lag1_dollars` then divide by `price_lag1_dollars`).
2. Run Table 4 M1 with each version. Log the resulting ΔEARN coefficient.
3. If the $/share version matches 2.795, document the unit-scaling issue and update the ΔEARN variable to $/share. If neither matches, this is a true paper-side artifact (per the agent's claim "implies R² ≈ 1").

### [M5] — MAJOR — fix after [M1]
Table 9 M1 PM coefficient sign discrepancy: replicated +0.091 (t=7.81, significant positive) vs paper -0.013 (t=-1.62, insignificant). The agent attributes this to using `Compustat.datadate` instead of `ibes.detu_epsus.anndats` as the FE construction boundary.

**Specific fix:**
1. Modify `src/sql/ibes_analyst.sql` to use `ibes_202601.detu_epsus.anndats` instead of `Compustat.datadate` for the "month prior to t+1 announcement" boundary. If `anndats` is null, fall back to the last `statsumu_epsus.statpers` before `datadate(t+1)`.
2. Re-run Table 9 M1 and M2. Log the resulting PM and ΔPM coefficients to `preparations/assumptions.md`.
3. If the sign discrepancy persists, the issue is elsewhere — investigate whether the panel filter (SIC, loss-firm exclusion, NOA > 0) is being applied to the FE subsample.

### [M6] — MAJOR — fix after [M1]
IBES-CUSIP linking via `comp_202601.security.ibtic` only matches 47% of gvkeys. Paper footnote 24 says 63% retention in 2001; agent gets 50%. The lower coverage reduces the sample size and may bias coefficients.

**Specific fix:**
1. Try using `ibes_202601.statsumu_epsus.cusip` joined to `comp_202601.security.cusip` (8-character CUSIP) instead of `ibtic`. Log the resulting IBES coverage rate.
2. If CUSIP-based linking recovers more firm-years (closer to 63% retention), switch to CUSIP-based linking for Tables 8/9.

### [m1] — MINOR — cleanup
The per-cell evaluation block is not embedded in `results/table_*.md` files. Modify `src/evaluate.py` to append a per-cell Tier 1/2/FAIL grid to each results file so the next audit can verify labels by reading the markdown.

### [m2] — MINOR — cleanup
See [M1] for the metrics.json key-naming fix.

### [m3] — MINOR — cleanup
See [M3] for the ΔWC assumption-20 fix (test result is missing).

### [m4] — MINOR — cleanup
Sample period starts at 1985, not 1984. Loosen the IBES coverage window from "same fiscal year" to "±1 year of fiscal year" to recover ~700 firm-years. Verify this matches the paper's IBES coverage definition (paper is silent on exact window).

### [m5] — MINOR — cleanup
`results/table_4.md:19-22` is missing paper values for the M2/M3/M4 RNOA, ΔRNOA, PM, and ATO columns. Add the paper values back for direct comparison.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status. A diagnosis without a Next fix is incomplete — do not move on.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Diagnoses must be paired with fix attempts (exit gate).** Before declaring `partial`, walk `assumptions.md` and verify every diagnosed problem has at least one log entry with a non-empty `Next fix` line and a before/after metric.
- **Use the canonical scorer.** Always re-run `scripts/score_replication.py <slug>` after any pipeline change — its output is authoritative per `SKILL.md`. The agent's `src/evaluate.py` is a convenience layer, not the source of truth.

## Inputs you should read

- `replications/<slug>/logs/audit1.md` — this audit (full context)
- `replications/<slug>/inputs/content.md` — paper ground truth
- `replications/<slug>/preparations/` — prep contract (rules, tables selected, data verification, assumptions iteration log)
- `replications/<slug>/src/main.py` — current code (will be modified)
- `replications/<slug>/src/evaluate.py` — the per-cell evaluator (currently diverges from canonical scorer)
- `replications/<slug>/eval/scoring.json` — canonical scorer output (T1=30, T2=59, FAIL=22, MISSING=42, L=1.222)
- `replications/<slug>/eval/metrics.json` — replicated values (inconsistent naming)
- `replications/<slug>/data/panel.parquet` — cached panel (32,425 rows × 45 cols)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-doing the ClickHouse catalog scan — `data_verification.json` is current.
- **DO** re-run any sanity checks you add or modify — they are the gate that catches regressions.
- The identity check (max |RNOA - PM × ATO| = 3.55e-15) passes — do not re-implement the RNOA decomposition.

## Deliverables for this iteration

- `replications/<slug>/src/main.py` — revised with fix attempts logged per issue above
- `replications/<slug>/src/evaluate.py` — updated to use canonical 2× cap and emit per-cell block into table_*.md
- `replications/<slug>/results/table_<n>.md` — updated for each committed table; include the per-cell Tier 1/2/FAIL grid
- `replications/<slug>/eval/metrics.json` — rewritten with globally-unique metric name keys
- `replications/<slug>/eval/scoring.json` — regenerated by `scripts/score_replication.py`
- `replications/<slug>/preparations/assumptions.md` — append a new iteration log entry for every issue addressed (Diagnosis, Next fix, Before metric, After metric, Status)
- `replications/<slug>/REPORT.md` — updated; cite the actual computed values from `metrics.json` (the C3 headline must say +0.051 t=2.83 Tier 2 r=0.65, not +0.079 t=5.05 Tier 1)
- `replications/<slug>/SUMMARY.md` — read the latest combined assessment to understand the auditor's verdict; do NOT edit (the auditor owns this file)

## Stop conditions

- **All blockers fixed and verified** → re-run canonical scorer and prep_validation.py → if both pass and Loss L drops below 0.5, declare success.
- **10-iteration cap reached** on a single problem → escalate to the human and write a partial `REPORT.md`.
- **All blockers fixed but majors remain** → declare partial and document the gap in `REPORT.md`.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

The replication demonstrates substantial engineering effort — the SQL pipeline, the data joins, the IBES-CUSIP linking, the FF factor loading, the FM regression machinery all work end-to-end. The four headline claims (C1-C4) have the correct direction and significance regime. The two major issues that need fixing in the next iteration are (1) the B1 blocker — REPORT.md's headline C3 value is inconsistent with the actual computed value and needs to be reconciled; and (2) the M1 issue — the metrics.json naming convention and the agent's `evaluate.py` cap create a divergence from the canonical scorer that needs to be resolved before the per-cell tally can be trusted.

The ΔATO heavy-tail absolute-value clip (assumption 15) is the most consequential methodology choice and warrants a test result before being accepted as a "documented partial." The paper itself reports ΔATO std=0.15, which is what one would expect from per-year winsorization alone in a 38,716-firm-year sample; the replication's pre-clip std=2.6 is anomalous and likely reflects a sample-composition difference (smaller firms with extreme ATO) that the paper does not include. A diagnostic that compares the paper's ΔATO distribution to the replication's pre-clip ΔATO distribution (e.g., quantile-quantile plot) would establish whether the issue is sample composition or measurement.
