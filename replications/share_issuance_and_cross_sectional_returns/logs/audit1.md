---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — share_issuance_and_cross_sectional_returns

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** High-quality replication of Pontiff & Woodgate (2008). The post-1970 headline (Table III) reproduces almost exactly under independent recomputation (ISSUE −2.06/t −7.00 vs −2.23/−7.08; all key cells within 10%), Table I reconciles once the winsorized-statistics convention is applied, and the pre-1970 tables replicate in structure with a documented noise-level ISSUE-sign deviation. One actionable gap: the paper's 1–3 year holding-period panels (Table III C–E) were not computed even though the targets are legible and the panel columns exist.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass; deviations (DT-Dum flip vs L94, 408 vs 396 months, GLSAR AR-error form, OOS degenerate-month guard) are paper-side inconsistencies resolved against the paper's own numbers, documented, and independently verified |
| Headline matching | 5 | Headline ISSUE slope within 7.6% and t within 1.1% of the paper; ISSUE is the most significant predictor in every joint spec; R² hierarchy (0.20% vs 0.73–1.24%) matches the paper's "one-third of BM" claim |
| Data coverage | 4 | Exact in-sample and OOS periods; in-sample counts within 0.5–1.2%; same CRSP/Compustat sources; SDC and DFF book equity documented-unavailable; OOS cross-section 24% larger than the paper's DFF-restricted sample |
| Concrete result matching | 4 | 163/201 evaluated cells Tier 1 (81%); 3 FAIL (1.5%, all the same noise-level OOS ISSUE-sign cells); 14 SKIP (DFF) |
| Signal strength | 5 | All headline cells within [0.9, 1.1]: A-R5 ISSUE 0.924, A-R5 t 0.989, B-R5 ISSUE 0.932, B-R5 t 1.058, R6 DT-ISSUE 0.958 |
| Corollary | 3 | 6-month stability, horse-race signs, R² hierarchy, Figure 1 shape, OOS ME/MOM patterns all replicate; 1–3 year panels (C–E) not computed; OOS ISSUE sign flips; SDC robustness unavailable |

**Overall: 4.17 / 5.00 — REPLICATED** (mean ≥ 3.0, no dimension at 1)

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] Table III Panels C–E (1-year, 2-year, 3-year holding periods) not computed — the paper's headline corollary "Our results remain strong for holding periods ranging from one month to 3 years" (content.md L31) is only verified at 1-month and 6-month horizons. ACTIONABLE.
  - File: `src/analyze_tables.py:86-95` (SPECS covers only r1pct/r6pct); targets at `inputs/content.md` L1501 (Panel C), L1698 (Panel D), L1895 (Panel E) — all three panels have legible coefficient/t-stat cells (e.g. Panel C R1: 13.55 (6.08), BM 3.17 (3.87); Panel D R2: ME −1.13 (−2.25))
  - Likely cause: REPORT.md §6.5 asserts "OCR of those pages is ambiguous", but content.md contains the full tables — the claim is not supported and the extension was skipped
  - Specific fix: extend `analyze_tables.py` to run SPECS on `r12×100` (k=12), `r24_y2×100` (k=24), `r36_y3×100` (k=36) with Pontiff GLSAR AR(11/23/35); add Panel C/D/E metrics to `tables_to_replicate.json` from content.md; write `results/table_3_panes_cde.md`; verify ISSUE stays negative and the most significant predictor at the annual horizon

- [M2] Pre-1970 ISSUE sign deviation — 3 FAIL cells (oos_pA_r5_issue −1.27 vs +0.52; oos_pA_r7_issue −1.56 vs +0.27; oos_pA_r7_issue_t). NON-ACTIONABLE (actionable: false).
  - File: `results/table_6.md` appendix; diagnosis at `preparations/assumptions.md` A21
  - Likely cause: our CRSP-only OOS cross-section (1,067 firms/mo, verified) is ~27% larger than the paper's DFF-book-equity-restricted sample (841/mo); marginal thinly-issuing small caps tilt the noise-level slope negative. Auditor verified the sign is negative at every guard threshold 0.005–0.05 and unguarded (−29.1) — robust, not a guard artifact
  - Specific fix: none legitimate — the DFF (2000) book-equity file is not in ClickHouse (A8); restricting to Compustat-covered firms would substitute a different sample and fit to the target. Correctly documented, not forced

- [M3] Tables II and IV not replicated (Thomson SDC Platinum SEO/repurchase/merger data unavailable). NON-ACTIONABLE (actionable: false). Documented at A9 with catalog check.

- [M4] Pre-1970 BM cells SKIP (DFF 2000 book equity unavailable; 14 SKIP cells). NON-ACTIONABLE (actionable: false). Documented at A8.

### Minor (cleanup)

- [m1] Empty nested skeleton directory `replications/share_issuance_and_cross_sectional_returns/replications/share_issuance_and_cross_sectional_returns/` (32K, zero files) at the slug root — a `paper_layout().ensure()` artifact from a run with unresolved REPLICATIONS_PATH. Specific fix: `rm -rf` the nested dir; the current script sets REPLICATIONS_PATH correctly so it won't recur.
- [m2] REPORT.md §6.3 Limitation 3 parenthetical is garbled ("our 373K+ cross-section vs their 373,590 total") — ours is 464,718 vs paper 373,590. Specific fix: reword with the correct numbers.
- [m3] REPORT.md §6.5 states Panels C–E "were committed at pattern level (OCR of those pages is ambiguous)" — contradicted by the legible tables in content.md (see [M1]). Specific fix: correct the statement and compute the panels.
- [m4] Tier-2 labeling on near-zero OOS cells: oos_pA_r6_dt_dum_t (paper 0.12, ours 1.24, 10.3×), oos_pA_r6_avg_r2 (2.5×), oos_pA_r7_dt_issue (2.9×), and two flipped-sign t-stats (oos_pA_r5_issue_t, oos_pA_r6_dt_issue_t) pass under the repo's global rule (TOLERANCE_RULES.md: sign match → Tier 2; t-stat significance-class extension documented in table_6.md) but exceed the rubric's 2× heuristic. No score impact (Tier-1 share unchanged). Specific fix: optionally annotate |paper| < 0.5 cells as "noise-level" in the appendix.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction / hierarchy claim | ✓ | ISSUE is the most significant predictor in every joint spec (A-R5 \|t\| 7.00 vs BM 5.64, ME 2.95, MOM 1.53); R² hierarchy 0.20 vs 0.73/1.14/1.24/2.89 matches the paper's "issuance explains one-third of BM" claim |
| 2 | Headline-magnitude claim | ✓ | Auditor's own FM implementation: A-R5 ISSUE = −2.0557, t = −6.997, N = 2,203,273, 408 months — identical to table_3.md (−2.06/−7.00) and within 8%/1.1% of the paper (−2.23/−7.08); B-R5 = −12.883 with GLSAR(5) t = −7.68 (paper −13.82/−7.26); AR-on-levels contrast = −20.94 confirms the AR-error choice |
| 3 | Sample coverage ≥ 60% | ✓ | In-sample base 2,324,025 (exact match to table_1.md) vs paper 2,312,597 (+0.5%); regr sample 2,182,151 vs 2,155,945 (+1.2%); OOS 464,718 vs 373,590 (+24%, documented DFF cause) |
| 4 | Data-source choice justified | ✓ | cfacshr convention verified on Apple's three 2:1 splits (adj_shares = shrout×cfacshr split-invariant: 14.34M→14.08M/18.23M→18.19M/22.88M→22.88M); Compustat consol='C'/popsrc='D' justified (A13; 'STD' values don't exist in the vintage); CCM link = WRDS default |
| 5 | prep_validation.py exit 0 | ✓ | Failed before the audit (missing logs/audit*.md + SUMMARY.md — the auditor's own deliverables); passes after this audit writes them |
| 6 | All committed tables have results files | ✓ | T1→table_1.md, T3→table_3.md, T5→table_5.md, T6→table_6.md, each with a per-cell evaluation block |
| 7 | SUMMARY/REPORT values match results | ✓ | Spot-checked 12 numbers (−2.06/−7.00, −0.68/−5.21, −12.88/−7.68, 2,324,025, 56.5/24.5/19.0, 0.151, −1.27/−1.73, −0.25/−3.36, 0.77/1.54, 163/21/3/14, 2,172) against results md + independent recomputation; exception: REPORT §6.3 parenthetical typo [m2] |
| 8 | No orphan folders | ✓ (minor) | No literal-brace dirs; one empty nested layout skeleton [m1] |
| 9 | Diagnoses paired with fix attempts | ✓ | Every iteration-1/2 diagnosis in log1.md has a fix and before/after metrics (raw std 0.230 → winsorized 0.151; DT-Dum +0.50 → −0.50 with intercept 1.02 → 1.52; AR-levels t −20.9 → GLSAR −7.68); the OOS-sign diagnosis (A21) documents why no fix is legitimate |
| 10 | Tier 2 within 2× magnitude | ✓ (caveat) | All T1/T3/T5 Tier-2 cells within 2× (ratios 0.57–1.48). Five near-zero T6 cells exceed 2× or flip sign at noise level (paper \|value\| ≤ 0.46); valid under TOLERANCE_RULES.md's sign-match rule and the documented t-stat significance-class convention; zero score impact [m4] |
| 11 | Corollary coverage | ✗ (→ [M1]) | 6-mo stability ✓ (recomputed), Figure 1 shape ✓ (documented, deterministic regen), R² hierarchy ✓, horse-race signs ✓, OOS ME/MOM ✓ (recomputed), OOS ISSUE no-predictability partial ✓ at R5; 1–3 year stability NOT computed → [M1] major |

**Additional independent micro-checks (auditor's own code, not the agent's):**
- ISSUE = ln(adj_{t−6}) − ln(adj_{t−17}) and issue_contemp = ln(adj_t) − ln(adj_{t−11}): exact 8-decimal match on permno 14593 ✓
- MOM = ∏(1+ret) over t−7..t−2 − 1: exact match ✓
- me_june held Jul-96–Jun-97 = June-96 ln|prc|·shrout = 14.770824 both places ✓
- Table I winsorized ISSUE: mean 0.0437/std 0.1512 (table_1.md 0.04/0.15; paper 0.04/0.15); raw std 0.2305 ✓ — the winsorized-regressor convention is confirmed by the auditor's own recomputation, including the fingerprint that R_{-11,0} (a non-regressor) matches raw
- DT-Dum flip invariance: under both polarities DT-ISSUE = −0.683; only intercept (1.020 → 1.518) and DT-Dum (+0.498 → −0.498) change; flipped intercept 1.518 vs paper 1.48 supports the ratified polarity ✓
- OOS guard robustness: ISSUE slope negative at every threshold (0.005: −1.30; 0.01: −1.27; 0.02: −0.65; 0.05: −0.51; unguarded: −29.14 with a single −11,649 month) — the sign deviation is genuine, not a guard artifact ✓
- End-to-end rerun of `src/analyze_tables.py`: byte-identical markdown outputs (md5 match), deterministic ✓

## 4. Issues the agent should have caught (didn't)

1. **The "OCR is ambiguous" claim for Panels C–E (REPORT §6.5) is false** — content.md contains legible Panel C (L1501+), Panel D (L1698+), and Panel E (L1895+) coefficient grids. A careful pass would have extracted at least Panels C–D targets and run the 1–3 year specs; the machinery (`run_fama_macbeth` with k=12/24/36) and verified columns (`r12`, `r24_y2`, `r36_y3`) already exist. This is the reason for [M1] and `requires_iteration: true`.
2. **REPORT §6.3 typo** — "our 373K+ cross-section vs their 373,590" conflates our 464,718 with the paper's count [m2].
3. **Empty nested `replications/` skeleton at the slug root** [m1] — created by an early layout-resolution bug; the fix is in the script but the artifact was never cleaned.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Share Issuance and Cross-sectional Returns" (Pontiff & Woodgate 2008) for slug `share_issuance_and_cross_sectional_returns`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/share_issuance_and_cross_sectional_returns/logs/audit1.md`). Read the audit first.

The audit independently verified the entire pipeline (signal formulas exact at the security level; Table III A/B and Tables I/V/VI reproduce under the auditor's own recomputation; headline ISSUE slope within 7.6%, t within 1.1%). Do NOT rebuild the panel or change any ratified convention (A1–A21). The only substantive gap is one missing corollary.

## Issues to address (priority order)

### [M1] — MAJOR — Table III Panels C–E (1/2/3-year holding periods) not computed

The paper's abstract-level claim "Our results remain strong for holding periods ranging from one month to 3 years" (content.md L31) is currently verified only at 1-month and 6-month horizons. REPORT.md §6.5 claims the Panels C–E pages are OCR-ambiguous, but content.md contains legible targets: Panel C (1-year, L1501+; e.g. R1 intercept 13.55 (6.08), BM 3.17 (3.87), BM Dum 5.35 (6.48), R² 0.92; R2 intercept 27.81 (4.03), ME −0.91 (−1.87), R² 1.37), Panel D (2-year, L1698+; R1 12.98 (5.52), BM 3.38 (4.33); R2 ME −1.13 (−2.25), R² 1.45), Panel E (3-year, L1895+).

**Specific fix:**
1. Extract Panel C/D/E metric values from `inputs/content.md` (the HTML table rows after L1501/L1698/L1895) into `preparations/tables_to_replicate.json` as a new table entry (e.g. `T3cde`) with the standard ±40% coef/t and ±25% R² tolerances. If any individual cell is genuinely illegible, mark that cell SKIP with the reason — do not skip whole panels.
2. Extend `src/analyze_tables.py`: run the existing SPECS via `run_fama_macbeth` on `r12×100` (k=12), `r24_y2×100` (k=24), `r36_y3×100` (k=36) over the in-sample months with `DT_DUM_FLIP=True` — the Pontiff GLSAR AR(n=k−1) machinery already handles n=11/23/35. Write `results/table_3_cde.md` with per-cell evaluation.
3. Verify: the ISSUE slope should stay negative across horizons and remain the most significant issuance predictor; the multi-year t-stats are the real test of the AR(k−1)-error convention (cross-check NW(11/23/35) as in Panel B). Report the before/after in an assumptions.md entry (A22).
4. Optional same-machinery extension (do if time permits): Table VI Panels B–E (OOS multi-horizon, content.md L2887+) to test the paper's "40 specifications" claim (L3507) — expected to surface the same documented OOS ISSUE-sign deviation.

### [m1] — MINOR — cleanup
Delete the empty nested skeleton dir: `rm -rf replications/share_issuance_and_cross_sectional_returns/replications/`.

### [m2]/[m3] — MINOR — REPORT.md wording
Fix the §6.3 parenthetical (ours 464,718 vs paper 373,590) and replace the §6.5 "OCR ambiguous" claim with the computed Panels C–E results.

### Do NOT touch (verified, ratified)
- The panel build (`src/main.py`, `src/sql/`) — formulas verified exact by the auditor at the security level.
- DT_DUM_FLIP=True, the winsorized-Table-I convention, the GLSAR AR-error t-stat, the 408-month window, the OOS degenerate-ISSUE guard — all independently confirmed.
- [M2]/[M3]/[M4] are NON-ACTIONABLE data limitations (DFF book equity, SDC Platinum). Keep them documented; do not attempt sample restrictions to force the OOS ISSUE sign — the auditor verified the deviation is robust and correctly attributed, and fitting to the target is prohibited.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.

## Inputs you should read

- `replications/share_issuance_and_cross_sectional_returns/logs/audit1.md` — this audit (full context)
- `replications/share_issuance_and_cross_sectional_returns/inputs/content.md` — Panels C/D/E targets (L1501/L1698/L1895)
- `replications/share_issuance_and_cross_sectional_returns/src/analyze_tables.py` — extend SPECS loop
- `replications/share_issuance_and_cross_sectional_returns/data/panel.parquet` — r12/r24_y2/r36_y3 already verified

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip re-running `scripts/prep_validation.py` — already passed (unless you change a prep artifact).
- Skip the ClickHouse catalog scan and panel rebuild — `data_verification.json` is current and the parquet is verified.
- **DO** re-run `src/analyze_tables.py` after extending it and re-verify the existing tables are byte-stable.

## Deliverables for this iteration

- `replications/share_issuance_and_cross_sectional_returns/results/table_3_cde.md` — Panels C/D/E with per-cell evaluation
- `replications/share_issuance_and_cross_sectional_returns/preparations/tables_to_replicate.json` — new T3cde entry
- `replications/share_issuance_and_cross_sectional_returns/preparations/assumptions.md` — A22 entry (five fields)
- `replications/share_issuance_and_cross_sectional_returns/REPORT.md` — updated §3/§6 with the horizon-stability results and the [m2]/[m3] wording fixes
- `replications/share_issuance_and_cross_sectional_returns/SUMMARY.md` — read only; the auditor owns it

## Stop conditions

- **All blockers fixed and verified** → re-run prep_validation.py and sanity checks → declare success or note remaining majors; the next audit updates SUMMARY.md.
- **10-iteration cap reached** → escalate and write a partial REPORT.md.
- **All blockers fixed but majors remain** → declare partial and document in REPORT.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the cleaner replications I have audited. The agent's workflow was exemplary in several respects: every signal was verified at the individual-security level before any table was produced (and those verifications hold up under the auditor's independent recomputation — ISSUE, issue_contemp, MOM, me_june, and the split-adjusted share series all match to 8 decimals); every convention decision is traceable to a paper line or documented as a paper-silent choice in the 21-entry assumptions registry; and the two genuinely difficult judgment calls were handled with unusual discipline. The DT-Dum polarity flip is the right call: the paper's caption (content.md L1074) is self-contradictory ("set to one if shares outstanding exists at t−65 (hence DT-ISSUE is zero)"), and the flipped definition's intercept (my recomputation: 1.518) matches the paper's printed 1.48 while the as-built 1.020 does not — and the agent kept both polarities visible in the diagnostic table rather than silently choosing. The Pontiff overlap t-stat resolution (AR-error GLSAR vs AR-on-levels) is correct: I reproduced the −20.94 AR-on-levels inflation and the −7.68 GLSAR value independently. Most importantly, the agent refused to fit the pre-1970 ISSUE sign to the target — my threshold sweep confirms the sign is robustly negative in our larger CRSP-only sample, and documenting it as a deviation rather than restricting the sample is exactly the right discipline. The single thing that keeps this at PARTIAL rather than PASS is the skipped 1–3 year panels: the targets are legible, the columns are built and verified, the machinery exists — this is a 30-minute extension that was avoided on an inaccurate "OCR ambiguous" claim. One more outer iteration should close it.
