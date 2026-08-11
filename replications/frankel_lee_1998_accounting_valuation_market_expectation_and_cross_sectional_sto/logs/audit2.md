---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 2
requires_iteration: true
---

# Audit Report 2 — frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto

**Verdict:** PARTIAL  
**Date:** 2026-08-08  
**Auditor notes:** The canonical score now verifies most of the produced work (42 Tier 1, 50 Tier 2, 21 FAIL, 27 MISSING; loss 1.0429), and the B/P return result remains credible. The prior metrics blocker is closed, but T8/T9 remain unproduced and the report is materially stale; the forecast-error sign failures are documented as a data-vintage limitation rather than a coding error.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4/5 | EBO construction, June sorts, filters, deduplication, and scoped Compustat extraction are documented and implemented; constant discount rate and missing LTG/FY2 substitutions remain. |
| Headline matching | 3/5 | The paper's B/P long-horizon return pattern is positive and close, but V_f-based correlations and V_f/P spreads show material vintage-driven drift. |
| Data coverage | 3/5 | The 1976–1993 period is covered and sample coverage is 13,787/18,162 = 76%; modern I/B/E/S vintage and linkage change the universe and forecast inputs. |
| Concrete result matching | 2/5 | Only 42/140 cells are Tier 1 (30%); 50 are Tier 2, 21 FAIL, and 27 remain MISSING. |
| Signal strength | 3/5 | The B/P Q5–Q1 spreads are within the rubric's 2x/50% band, while the V_f/P return spread and forecast-error coefficients are substantially distorted. |
| Corollary | 3/5 | Tables 4, 6, and 7 are available for checking, but the incremental PErr strategy and yearly robustness outputs in Tables 8 and 9 remain missing. |

## 2. Issues by severity

### Blockers (must fix)

None. The prior [B1] metrics artifact exists and the scorer completed successfully.

### Major (should fix)

- [M1] **Actionable — Tables 8 and 9 remain uncomputed.** The paper explicitly claims that PErr adds predictive power to V_f/P and that the combined top-V_f/P/bottom-PErr strategy earns more than 45% over 36 months (paper `inputs/content.md:50-52`). The canonical scorer records 27 MISSING cells, concentrated in T8/T9, and `results/table_8.md`/`table_9.md` contain no computed values. The claim-to-table contract identifies these as C4 outputs (`preparations/tables_to_replicate.json:17-20`). **Specific fix:** complete the existing Table 8/9 pipeline, emit their metric values, and add per-cell comparison/evaluation blocks; then rerun the canonical scorer.
  - File: `data/metrics.json` and `eval/scoring.json` (iteration 2 scoring; 27 missing cells); `results/table_8.md`, `results/table_9.md`.

- [M2] **Actionable — current REPORT.md materially contradicts the artifacts.** It still says only Tables 1–3 were produced and Tables 4–9 were not produced (`REPORT.md:8`, `52-55`), whereas `logs/log1.md:114-139`, the result directory, and the scorer show Tables 4, 6, and 7 produced. It also reports the old hand-tallied loss and counts (`REPORT.md:58-64`) rather than the canonical iteration-2 values. This is a report-level reproducibility problem, even though the current audit relies on the canonical artifacts. **Specific fix:** update REPORT.md in the next replication iteration to lead with the iteration-2 table status and the exact `eval/scoring.json` counts/loss, without claiming T8/T9 or any unverified corollary is complete.

- [M3] **Non-actionable data limitation — forecast-error regression signs.** T6/T7 have 16 FAIL cells, with modern I/B/E/S forecasts over-predicting and producing negative `FErr = ROE_actual - FROE_predicted`, opposite the paper's convention. The sign convention and median FY1/current-EPS evidence are documented in `logs/log1.md:134-136` and `preparations/assumptions.md:614-620`; this is not accepted as a subtraction-order fix, but as a documented vintage mismatch. **Specific fix:** no feasible code-only correction is required; retain the limitation and report the sign divergence explicitly rather than presenting these cells as replicated.

- [M4] **Non-actionable data limitation — V_f-related return cells.** Five T3 FAILs (including V_f/P and size/composition-related spreads) remain, consistent with the modern I/B/E/S vintage and the smaller-firm composition documented in `logs/log1.md:123-132` and `REPORT.md:47-50`. **Specific fix:** preserve the paper-consistent method and disclose the vintage/composition limitation; do not relabel these FAILs as Tier 2 merely because the qualitative story is similar.

### Minor (cleanup)

- [m1] The canonical scorer warns that `loss_function.json` is absent. This is informational under the current closed-vocabulary tier-count loss, but the warning should not be confused with a scoring failure.
- [m2] `src/evaluate.py` remains an obsolete hand parser after the canonical `metrics.json` path was added; avoid using its tally in future reports.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | B/P Q5–Q1 Ret12/24/36 spreads are positive; log reports +0.034, +0.098, +0.179 versus paper +0.049, +0.082, +0.151. |
| 2 | Headline-magnitude claim | ✗ | Table 1 Avg ME is 726 versus 1,167 (−38%); Table 2 V_f correlation is 0.65 versus 0.81. |
| 3 | Sample coverage ≥60% | ✓ | Final unique panel is 13,787/18,162 = 76%, per `REPORT.md:15` and `logs/log1.md:89-94`. |
| 4 | Data-source choice justified | ✓ | I/B/E/S, LTG, constant r_e, and vintage substitutions are documented in the assumptions registry and data verification artifact. |
| 5 | prep_validation.py exit 0 | ✗ | Validation reached the loop-state error because `logs/log2.md` is absent while audit1 required another iteration; this audit file is the required continuation artifact. No metrics-schema failure occurred. |
| 6 | All committed tables have results files | ✓ | All eight committed table files now exist; T8/T9 are present but remain uncomputed/MISSING. |
| 7 | SUMMARY.md matches results/table_*.md | ✗ | The pre-audit summary/report state is stale; this audit overwrites SUMMARY.md with iteration-2 values. |
| 8 | No orphan folders | ✓ | No literal-brace or shell-expansion folders found at the slug root. |
| 9 | Diagnoses paired with fix attempts | ✓ | The iteration-2 diagnosis/fix/metric trail is present in `logs/log1.md:114-139`; the remaining T8/T9 omission is explicit. |
| 10 | Tier 2 within 2x magnitude | ✓ | Canonical scorer's Tier 2 assignments are within the defined magnitude bound; 21 non-missing FAILs are not relabeled. |
| 11 | Corollary coverage | ✗ | The PErr incremental strategy corollary is not computed: T8/T9 remain MISSING. |
| 12 | Claim coverage of committed selection | ✓ | C1–C4 are mapped to committed tables; C4 is not yet evidenced because its T8/T9 outputs are missing. |
| 13 | Sign conventions re-derived from paper | ✓ | The forecast-error discrepancy is a genuine reported sign divergence under the documented FErr convention, not an absolute-value comparison or silent sign flip. |
| 14 | Reporting discipline | ✗ | The stale REPORT.md omits the newly computed T4/T6/T7 grid and reports superseded counts; exact directional claims should be accompanied by their uncertainty statistics. |

## 4. Issues the agent should have caught (didn't)

1. The run's REPORT.md was not refreshed after the successful Table 4/6/7 and metrics work, leaving a material contradiction between the self-report and the filesystem.
2. The remaining 27 MISSING cells should have been stated as an unresolved C4 corollary gap rather than treating the partial table expansion as a completed replication.
3. The negative T6/T7 forecast-error signs should be presented prominently as a limitation; they cannot validate the paper's optimism direction even if the modern-vintage cause is plausible and documented.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

Continue the Frankel & Lee (1998) replication. Read `logs/audit2.md` first.

Priority issues:

1. **[M1] Complete Tables 8 and 9.** Produce the PErr incremental return-prediction regressions and year-by-year strategy returns required for C4, including all metric values and per-cell evaluation blocks. Re-run `scripts/score_replication.py` and verify that the 27 MISSING cells fall to zero (or document any genuinely unavailable input).
2. **[M2] Refresh REPORT.md.** Replace the stale “3 of 8 tables” and old hand tally with the actual iteration-2 status and exact canonical scorer counts/loss. Clearly separate produced, failed, and missing outputs.
3. Preserve the documented, non-actionable modern I/B/E/S vintage limitations for the T3 and T6/T7 FAILs. Do not fix them by reversing signs or using absolute values.

Every assumptions entry must include Diagnosis, Next fix, Before metric, After metric, and Status. Re-run the validator and scorer after the changes.

--- END COPY HERE ---

## 6. Auditor's notes

This is a materially improved and auditable partial replication. The B/P long-horizon return pattern is the strongest evidence: all three reported spreads are positive and close enough to support the qualitative value effect. The canonical metrics path also closes the prior audit's main infrastructure failure. However, the core paper sells analyst-based V_f/P and the incremental PErr strategy, and the latter remains untested while V_f-dependent cells are visibly vintage-sensitive. The iteration should continue for T8/T9 and reporting correction, while retaining the current data-vintage failures as transparent limitations rather than pretending to have matched the 1998 sample.
