---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 1 — fairfield_v2

**Verdict:** PARTIAL
**Date:** 2026-08-07
**Auditor notes:** Honest replication with methodologically faithful pipeline; 3 FAILs are non-actionable data-extract residue (1999 vs 2026 Compustat), but two actionable majors uncovered — a convention-skip on the day-gap test and a report over-claim on the T5 paired-t interpretation.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All paper-explicit construction choices match; one documented convention-skip (day-gap test) on fiscal-year adjacency. |
| Headline matching | 3 | C1 (Sloan replicate) and C2 (H1, ACC + GrLTNOA both negative) supported; C3 (H2 lagged-deflator flip) fails; C4 (H3 signs) supported but LR magnitudes diverge. |
| Data coverage | 3 | Period matches exactly (1963-1992); universe 53,413 vs paper 33,080 = 1.61× paper (15-25% band exceeded); both vintage sources are 2026 with documented substitutes for the footnote filter and size-decile benchmarks. |
| Concrete result | 3 | 86/196 Tier 1 (43.9%) + 105 Tier 2 (53.6%); 3 FAIL (1.5%) + 2 no_effect (1.0%); 0 SKIP. Aggregate Tier 1 share sits at the 30-50% boundary. |
| Signal strength | 4 | All headline coefficients have matched signs; Sloan replication coefficients within 6% of paper; ACC forecasting signs all correct; one sign flip (T6_eq6_GrLTNOA) at |ratio|=0.52. |
| Corollary | 4 | Decile patterns match paper direction (ROA↑, CFO↓, GrNOA↑, GrWC↑, DEPAM↓, GrLTNOA flat); correlation matrix mostly within tolerance; missing the per-`fyear` subsample stability check. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | All cached numbers verified against the per-cell block. |

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] **Convention-skip on the day-gap test for fiscal-year adjacency.** `preparations/assumptions.md` A3 applies the **first** half of the documented default (`fyear` difference == 1) but skips the **second** half (`datadate` gap in [300, 430] days). The default is in `rep/PAPER_CONVENTIONS.md` § Annual accounting panels: "in FWY (2003) the label join admitted ~2,900 spurious firm-years the day-gap test rejected." The agent's only justification is "Paper silent on non-December fiscal years; FF default applied" — which addresses non-Dec fiscal years, not the day-gap test. The day-gap test's required data (`datadate`) is catalog-available per `data_verification.json`. Per the SKILL convention-skip check, "paper silent" alone is not a justification.
  - File: `replications/fairfield_v2/preparations/assumptions.md` (A3, lines 62-66); `replications/fairfield_v2/src/sql/panel.sql` (no day-gap predicate).
  - Specific fix: add a `WHERE` filter on the t-1 / t join that requires `dateDiff('day', toDate32OrNull(b_prev.datadate), toDate32OrNull(b.datadate)) BETWEEN 300 AND 430` to the panel pipeline. Re-run `panel.sql` and re-evaluate. The expected drop is ~2,900 rows; the panel will move from 53,413 to ~50,500. Whether this flips the 3 FAILs depends on whether the spurious rows are the 1980s distress firms (data-extract) — likely not, but the methodology is the documented default.

- [M2] **Report over-claim on T5 paired-t interpretation.** `REPORT.md` L89-92 claims: "the test of equivalence between the two coefficients fails to reject in our data (paired t = -3.04 on a magnitude scale consistent with the paper's -1.21 — same direction, both clearly indistinguishable from zero within tolerance)." The statistic contradicts the claim: |t|=3.04 with 29 paired years (df=28) exceeds the 5% critical value of 2.048 *and* the 1% critical value of 2.763. The paper's |t|=1.21 fails to reject; ours rejects. The economic conclusion flips. Per Spot-check 14(b), over-vocabulary claims of "fails to reject" require the licensing statistic to support them — the statistic here rejects.
  - File: `replications/fairfield_v2/REPORT.md` L89-92.
  - Specific fix: revise the C2 claim to acknowledge the test rejects equivalence in our data, even though the directional claim (both coefficients negative) holds. The claim should be re-stated as: "the directional claim (both ACC and GrLTNOA negative predictors) holds; the equivalence claim (paper fails to reject; ours rejects) is refuted by the larger, more raw 2026 sample." Cite the t-stat and the 28-df critical value alongside the claim.

### Minor (cleanup)

- [m1] **T2_PanelA_ROA_D1 sign disagreement is a single-cell FAIL, not a column-wide flip.** The other 9 decile cells in T2 Panel A are monotonic increasing (D1 < D2 < ... < D10 with one 0.001 rounding wobble at D7-D8) and the ACC decile sort direction is correct (D1=lowest ACC, D10=highest). The FAIL is on the magnitude cell D1 only, not the entire column. Worth documenting the distinction so the auditor reading the report does not conflate "D1 sign flip" with "all ROA values sign-flipped." (No fix needed; clarification only.)

- [m2] **iter-2 sanity claims about "the day-gap test would drop 2,900 firm-years" are forecast-grade.** The convention note cites this as the magnitude observed in the convention author's prior reproduction run; the agent's own panel might be different. A re-run with the day-gap test is the only way to verify the panel-size impact. (Resolved by M1.)

- [m3] **β_uncon = 1.65 in the Mishkin test's stage-1 eq. 8 is the load-bearing driver of the T7 LR magnitude divergence.** The paper's β_uncon ≈ 0.94 (centered near 1, where the LR formula is well-behaved). Our β_uncon = 1.65 inflates the LR magnitudes by 10-100×. The signs are all correct (γ_q negative, γ*_q positive), and Tier 2 verdicts are correct per the magnitude-ladder, but the substantive joint-test conclusion inverts (paper LR_joint=1.82 fails to reject; ours LR_joint=1404 strongly rejects). The economic interpretation requires a footnote acknowledging this. (No fix needed; clarity in REPORT.md.)

- [m4] **T6_eq6_GrLTNOA and T6_eq6_GrLTNOA_t share a single root cause.** Both cells FAIL because the GrLTNOA coefficient under the lagged deflator is -0.016 (paper +0.030); the t-stat is the same coefficient / SE. The evaluator correctly counts 2 cells, but it is one underlying coefficient failure. (Acceptable per the evaluator's per-cell contract; no fix needed.)

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim (T2 Panel A) | ✓ | D1-D10 ROA: -0.011, 0.063, 0.088, 0.095, 0.102, 0.109, 0.120, 0.119, 0.130, 0.137. CFO monotonically decreasing. Matches paper pattern; D1 magnitude has sign disagreement only. |
| 2 | Headline-magnitude claim (T1 ROA) | ✓ (partial) | Paper: mean 0.116, std 0.117, median 0.111. Ours: mean 0.0839, std 0.1849, median 0.0990. std inflates ~58% (data-extract). Median within 11%. |
| 3 | Sample coverage ≥ 60% | ✓ | 53,413 firm-years / 30 years = 1,780/year (paper 1,100/year). 1.61× paper target; over the 5-15% band but coverage threshold met. |
| 4 | Data-source choice justified | ✓ | comp_202601 + crsp_202601 (latest, per PAPER_CONVENTIONS.md data-vintage defaults). Footnote-code filter and size-decile benchmark substitutions documented. |
| 5 | prep_validation.py exit 0 | ✓ | `python scripts/prep_validation.py fairfield_v2` returns 0; "All present prep artifacts pass validation." |
| 6 | All committed tables have results files | ✓ | `results/table_1.md` through `results/table_7.md` all present; `all_metrics.json` has 211 keys (196 cells + 15 diagnostics). |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | Tier counts in `REPORT.md` match evaluator; table_5.md shows Eq 4 coef -0.083, t -7.25 (matches all_metrics.json). |
| 8 | No orphan folders | ✓ | No literal-brace folder names; slug root is clean. |
| 9 | Diagnoses paired with fix attempts | ✓ | assumptions.md has 7 paper-silent decisions + 4 stage-7 iterations (all 5 fields populated: Diagnosis, Next fix, Before metric, After metric, Status). |
| 10 | Tier 2 within 2× magnitude | ✓ | All Tier 2 cells have sign matches; the 3 FAILs are sign disagreements (correctly classified FAIL). |
| 11 | Corollary coverage | ✓ | Decile patterns reproduced (T2); correlation matrix reproduced (T3); BHAR is computed (T7). Missing: per-`fyear` subsample stability check (deferred, not a paper corner). |
| 12 | Claim coverage of committed selection | ✓ | All 4 paper_claims (C1-C4) covered by committed tables (T4-T7). No claims silently dropped. |
| 13 | Sign conventions re-derived from paper | ✓ | T2_PanelA_ROA_D1: paper +0.06, ours -0.011; T6_eq6_GrLTNOA: paper +0.030, ours -0.016; T6_eq6_GrLTNOA_t: paper +2.20, ours -1.26. All 3 are single-cell sign disagreements, not column-wide flips. T7 signs all match (γ_q negative, γ*_q positive). |
| 14 | Reporting discipline (grid completeness, claim citations, SE-less headlines) | ✗ | T5 paired-t claim "fails to reject" contradicts the |t|=3.04 statistic (M2). All other claims cite t-values or paired-t. |

## 4. Issues the agent should have caught (didn't)

1. **Convention-skip on the day-gap test.** The agent applied the first half of the documented fiscal-year adjacency default (fyear difference == 1) but skipped the second half (datadate gap in [300, 430] days). The default is in `rep/PAPER_CONVENTIONS.md` "Annual accounting panels" and is specifically motivated by FWY (2003): "in FWY (2003) the label join admitted ~2,900 spurious firm-years the day-gap test rejected." The agent's assumption A3 cites "paper silent" but the convention is documented and the data is available. Per the SKILL convention-skip check, "paper silent" alone is not a justification.

2. **T5 paired-t "fails to reject" claim contradicts the statistic.** With 29 paired years, the test has 28 df. The 5% two-sided critical value is 2.048; the 1% is 2.763. |t|=3.04 exceeds both. The agent's report claims "fails to reject" — this is factually wrong. The substantive C2 finding (equivalence of ACC and GrLTNOA coefficients) is refuted in our data, even though the directional claim (both coefficients negative) holds. The agent should have re-stated the claim as: "the directional claim holds, the equivalence claim is refuted in our data."

3. **Data-extract divergence is documented but the test that would close it has not been run.** The replicator attributes the 3 FAILs to the 2026 vs 1999 Compustat vintage. The cheap test for "is this the right diagnosis" is a same-extract under a 1999-vintage-like filter (e.g., a stricter Compustat quality filter that drops more post-1970 firms). The replicator did not run this. The diagnostic is acceptable as `data-extract vintage` per the SKILL, but a sub-figure "1980s firm count" would have made the argument self-evident.

## 5. Cross-check against preparation artifacts

### preprocessing_rules.json
- 45 rules across 8 categories (universe, sample, variable, sort, winsorize, factor, fm, delisting). All paper-cited (L116-1387). Two paper-silent rules (`factor_paper_silent`, `delist_paper_silent`) marked correctly.

### data_verification.json
- Verdict: `partial`. 7 requirements: 6 full, 1 partial (size-decile benchmark — `erdport1` columns inadequate, computed inline). 2 blocking_issues: (1) `erdport1` decile-portfolio lookup, justification documented; (2) `comp_footnote_codes` legacy-1999 vs modern-2026 mismatch, approximation documented. Both blocking_issues are correctly logged as substitutions; the catalog coverage is honest.

### tables_to_replicate.json
- 7 tables, 196 cells across 4 paper_claims (C1-C4). Coverage:
  - C1: T4 (Sloan eq 2)
  - C2: T5 (FWY eq 4)
  - C3: T6 (lagged-deflator eq 6)
  - C4: T7 (Mishkin test)
- All 4 paper claims are connected to at least one committed table. Reasonable tolerances per cell (8-15% for main coefficients, 15-25% for paired-t, 25-50% for LR stats).

### assumptions.md
- All 7 paper-silent decisions documented with rationale (A1-A11).
- All 4 Stage 7 iterations have all 5 fields populated (Diagnosis, Next fix, Before metric, After metric, Status).
- A3 (fiscal-year alignment) cites PAPER_CONVENTIONS.md but applies only the fyear half of the default — see [M1].

## 6. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Fairfield, Whisenant & Yohn (2003) Accrued Earnings and Growth" for slug `fairfield_v2`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/fairfield_v2/logs/audit1.md`). Read the audit first.

## Issues to address (priority order)

### [M1] — MAJOR — fix first

**Convention-skip on the day-gap test for fiscal-year adjacency.**

The agent's `panel.sql` joins by `fyear` difference == 1 but does NOT apply the `datadate` gap in [300, 430] days test documented in `rep/PAPER_CONVENTIONS.md` § Annual accounting panels. The convention is specifically motivated by FWY (2003): "in FWY (2003) the label join admitted ~2,900 spurious firm-years the day-gap test rejected."

**Specific fix:**
1. In `src/sql/panel.sql`, add a `WHERE` predicate on the t-1 / t joins: `dateDiff('day', toDate32OrNull(b_prev.datadate), toDate32OrNull(b.datadate)) BETWEEN 300 AND 430`.
2. Re-run `python src/main.py` to refresh `data/panel.parquet`.
3. Re-run `python src/evaluate.py` and check the per-cell tier tally.
4. Update `preparations/assumptions.md` A3 to reflect the full convention application (not just the fyear half).

### [M2] — MAJOR — fix after [M1]

**Report over-claim on T5 paired-t interpretation.**

`REPORT.md` L89-92 says "the test of equivalence between the two coefficients fails to reject in our data (paired t = -3.04)." This is factually wrong — |t|=3.04 with 28 df exceeds both the 5% (2.048) and 1% (2.763) critical values. The substantive C2 claim refutes in our data.

**Specific fix:**
1. In `REPORT.md` L89-92, replace the "fails to reject" claim with: "the directional claim (both ACC and GrLTNOA are negative predictors) holds, but the equivalence test statistic in our data rejects (paired-t = -3.04, |t|>1.96), opposite to the paper's fail-to-reject" — cite the 28-df critical value of 2.048 alongside the t-stat.
2. Update `assumptions.md` Stage 7 iter-3 entry to record the corrected wording.

### [m1] — MINOR — cleanup

`T2_PanelA_ROA_D1` is a single-cell sign disagreement, not a column-wide flip. Note in `REPORT.md` Section 4 that the other 9 decile cells are monotonic and the sort direction is correct.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.** Don't rediscover failures that are already documented.
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Convention-skip is a Major.** Apply the documented default unless the entry carries a substantive "why the default is wrong here" justification. "Paper silent" alone is not a justification.

## Inputs you should read

- `replications/fairfield_v2/logs/audit1.md` — this audit (full context)
- `replications/fairfield_v2/inputs/content.md` — paper ground truth
- `replications/fairfield_v2/preparations/` — prep contract (rules, tables, data verification, assumptions)
- `replications/fairfield_v2/src/main.py` and `src/sql/panel.sql` — current pipeline (will be modified)
- `replications/fairfield_v2/data/panel.parquet` — cached panel (recompute after M1 fix)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- `scripts/prep_validation.py` is loop-aware (DEV-009).
- Skip re-doing the clickhouse catalog scan — `data_verification.json` is current.
- **DO** re-run `python src/main.py` after M1 fix to refresh the panel parquet.
- **DO** re-run `python src/evaluate.py` after M1 fix to refresh the per-cell tally.

## Deliverables for this iteration

- `replications/fairfield_v2/src/sql/panel.sql` — add day-gap predicate
- `replications/fairfield_v2/preparations/assumptions.md` — append A3 update
- `replications/fairfield_v2/REPORT.md` — fix T5 paired-t claim
- `replications/fairfield_v2/results/table_5.md` — re-print if values change
- `replications/fairfield_v2/results/all_metrics.json` — re-emit after M1 fix
- `replications/fairfield_v2/SUMMARY.md` — read the latest combined assessment; do NOT edit (the auditor owns this file)

## Stop conditions

- **All blockers fixed and verified** → re-run `prep_validation.py` and `evaluate.py`; if both pass and the 3 FAILs are unchanged (data-extract vintage is the irreducible driver), declare success.
- **10-iteration cap reached** on a single problem → escalate to the human.
- **All blockers fixed but the 3 FAILs remain** → declare partial and document the data-extract limit in `REPORT.md`.

--- END COPY HERE ---

## 7. Auditor's notes

This is a high-quality replication. The pipeline is methodologically faithful (45 preprocessing rules, 8 categories, all paper-cited), the SQL is well-structured (fyear-based join, CRSP-coverage gate, 3-year-window non-null gate), the evaluator is deterministic and reproducible, and the algebraic identities (acc + cfo = roa; grnoa = acc + grltnoa; acc = grwc - depam) all hold to floating-point precision. The 4 inner iterations demonstrate disciplined diagnose-fix-verify cycles.

The 3 FAILs are honest empirical divergences from the paper, not artifacts. The data-extract divergence (2026 vs 1999 Compustat) is the structural driver: the 2026 extract has ~2× more 1963-1992 firm-year coverage than the 1999 extract used by the paper, and the additional firms are concentrated in the 1980s distress cycle. This drives the lowest-accrual ROA decile (T2_PanelA_ROA_D1) negative, the lagged-deflator GrLTNOA coefficient (T6_eq6_GrLTNOA) into sign disagreement, and the Mishkin test's β_uncon away from 1 (which inflates the LR statistics by 10-100×). Closing these would require a 1999-vintage Compustat extract, which is not available.

The two actionable majors are both small in scope but real in substance:

- **M1** is a methodologically-motivated convention-skip. The day-gap test is a one-line `WHERE` clause; the question is whether the spurious firm-years it would drop affect the 3 FAILs. Probably not (the 1980s distress firms are mostly legitimate), but the convention default exists and the skip is unjustified.

- **M2** is a wording fix. The substantive finding (equivalence is refuted in our data) is supported by the statistic; the report's claim of "fails to reject" is unsupported. This is a Spot-check 14(b) reporting discipline issue.

If the next iteration addresses both M1 and M2, the run can be declared done with the 3 FAILs as documented non-actionable data-extract limitations. The binary verdict would be REPLICATED (overall 3.5/5).
