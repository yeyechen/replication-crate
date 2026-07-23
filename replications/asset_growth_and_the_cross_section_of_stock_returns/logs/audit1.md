---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 1 — asset_growth_and_the_cross_section_of_stock_returns

**Verdict:** PARTIAL
**Date:** 2026-07-23
**Auditor notes:** A genuinely faithful replication of Cooper, Gulen & Schill (2008). The auditor independently re-derived the headline numbers from the cached parquets and ClickHouse — Year-1 EW/VW decile returns and spreads, FF3/Carhart4 alpha spreads (all firms and size groups), the Table III Model-1 Fama–MacBeth coefficients/t-stats (AR(1)-adjusted SE reimplemented from scratch), the winsorized M1, and the Table IV standalone/full-model t-stats — and every one reproduced the reported values to the reported precision. The data-vintage explanation is real (verified: 2026 funda has `ch` 93% null / `txp` 56% null in FY1966–68, and the ASSETG cross-sectional std is 28.7 vs the paper's ~0.60), and it is not a cover for a methodology bug, because the lower tail, the median, and — decisively — the portfolio returns all match the paper within ~2%. One actionable major remains (ISSUANCE split-adjustment never executed; 4 Tier-2 cells), plus a labeling gap: 13 of 43 Tier-2 cells violate the auditor's 2× magnitude bound (30/43 pass) and should be re-flagged honestly. No blockers.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass under independent verification (signal formula, FF1992 timing, PIT universe filter, no look-ahead, exact footnote-13 AR(1) SE reproduced to 2 decimals, decomposition identities to 1e-13); deviations (NW3 for Table II vs paper's GMM/delta-HAC; full-universe signal sort; monthly-portfolio event time) are all documented with paper-grounded justification |
| Headline matching | 4 | EW spread −1.713 vs −1.73 (1.0%), VW −1.033 vs −1.05 (1.6%), EW perfectly monotonic as the paper states; FF3 alpha spreads within 9–21%; only the raw FM ASSETG coefficient drifts ~30% (its t-stat within 18%, and the winsorized coefficient matches the paper's main coefficient to 3%) |
| Data coverage | 4 | Exact period (Jul 1968–Jun 2003; Compustat from 1963; event window to 2007); same sources (CRSP/Compustat/FF) with one documented equivalent substitution (FF3 = monthly subset of four_factor_monthly); universe composition vintage-shifted (more small/dormant firms), which is the documented driver of the level shifts |
| Concrete result matching | 3 | 74/119 = 62% Tier 1 (auditor re-tallied from the four eval JSONs); 117/119 sign-correct; the 2 FAILs are honest noise-level sign flips on statistically zero coefficients |
| Signal strength | 3 | Headline return spreads r = 0.98–0.99, EW FF3 alpha r = 0.91, but VW FF3 alpha r = 0.80, FM ASSETG coefficient r = 0.70, VW Sharpe r = 0.66, 5-yr cumulative r = 1.21 — all inside [0.5, 2.0] but not all inside [0.8, 1.2]; the signal is unquestionably present and strong |
| Corollary | 4 | All central corollaries computed and mostly replicated: decade subperiods (incl. the paper's own lone VW 1968–80 exception), size groups (all negative/significant), FF4 and FF5 adjustment, 5-year event-time persistence (−106.5% vs −88.0%), winsorization, monthly dependent, dominance over 5YSALESG/CI/NOA/ACCRUALS/5YASSETG, balance-sheet decomposition; minor deviations (large-cap VW alpha, ΔCurAsst/ΔOthAssets slopes) are explained |

## 2. Issues by severity

### Blockers (must fix)

_None._

### Major (should fix)

- [M1] ISSUANCE (Table I, 4 cells) uses raw Compustat `csho` and runs 1.85–3.9× the paper (D1 0.148 vs 0.080; D10 1.013 vs 0.301; spread 0.865 vs 0.221; t 12.11 vs 8.36). The agent diagnosed the likely cause (unadjusted stock splits inflate raw share counts) and identified the fix (split-adjusted shares via CRSP cumulative adjustment factors) in Assumption 8 but never executed it. This is the one Tier-2 driver with a concrete, unattempted fix. (actionable: true)
  - File: src/main.py:221-222 (`base["ISSUANCE"] = (csho − csho_t5)/csho_t5`); preparations/assumptions.md Assumption 8
  - Likely cause: raw `csho` counts mechanical split-induced share increases as "issuance"; the paper's magnitudes (0.08–0.30 over 5 years) are consistent with split-adjusted net issuance
  - Specific fix: compute 5-year share change from split-adjusted shares (CRSP cumulative adjustment factors, e.g. `factor*(1+facshr)` chain, or CRSP `shrout` June-to-June 5 years back) for the Table I column only; compare the new decile medians to 0.0803/0.3012/0.2209/8.36 and re-evaluate the 4 ISSUANCE cells

- [M2] Tier-2 labeling is looser than the auditor's 2× magnitude bound: 13 of 43 Tier-2 cells have |ours/paper| outside [0.5, 2.0] (auditor recomputed every ratio from the eval JSONs). Under the strict convention the tally is 74 Tier-1 / 30 Tier-2 / 15 FAIL, not 74/43/2. The 13 are: L2ASSETG_D1 (8.6×, paper value ≈0), L2ASSETG_t (0.48×), ROA_D1 (0.41×), ROA_t (0.42×), BHRET6_t (11.2× on a spread that matches to 10%), ACCRUALS_D10 (3.1×), ISSUANCE_D10 (3.4×), ISSUANCE_spread (3.9×), M1_MV (units; 0.82× in $billions with matching t), M6_ACCRUALS_ASSETG_t (0.39×), M6_ACCRUALS_t (0.27×), dOthAssets_alone_t (0.10×), dCurAsst_full_t (0.29×). The root causes are genuine and mostly non-actionable (below), but the labels overstate match quality. (actionable: partial — relabel; the underlying gaps are not fixable except ISSUANCE, see M1)
  - File: results/table_{1,3,4}_eval.json ("reason" strings use "sign matches, outside tol%" with no 2× check); results/evaluation_summary.md
  - Likely cause: the evaluation harness implements TOLERANCE_RULES.md's Tier-2 definition ("sign matches, magnitude outside tolerance") without the audit-side 2× cap
  - Specific fix: add a `within_2x` flag to each Tier-2 cell, reclassify the 13 as FAIL-with-documented-cause (or "Tier 2 (near-zero target)" for the ≈0 cells), and update the tally table in REPORT.md and evaluation_summary.md

- [M3] The five attenuation cells M6_ACCRUALS_ASSETG_t (0.39×), M6_ACCRUALS_t (0.27×), ACCRUALS_D10 (3.1×), dOthAssets_alone_t (0.10×), dCurAsst_full_t (0.29×) trace to pre-1971 Compustat missingness — **auditor-verified directly in `comp_202601.funda`**: `ch` is 93.2–93.5% null and `txp` 52.8–56.4% null in FY1966–1968 (vs ~9–11%/~4% by FY1974–75). ACCRUALS and ΔCurAsst (`act−ch`) therefore rest on 13/15/19 firms in 1968–1970. This is an external data-coverage limitation of the 2026 vintage, not a methodology bug (the formulas match the Appendix exactly, and the 1971–2002 sensitivity improves but does not close the gap, consistent with a genuine vintage effect). No honest fix exists — imputing missing items would fabricate data. (actionable: false)
  - File: results/table_3.md (M6 diagnostic); results/table_4.md (data-vintage diagnostic)
  - Specific fix: none (documented limitation); fold these into the M2 relabeling as FAIL-with-documented-external-cause

### Minor (cleanup)

- [m1] Table I `Leverage_spread_10_1` is labeled "Tier 2 (lenient, ~0 target)" but is an opposite-sign cell (paper +0.0165, ours −0.0158); under the strict convention it is a FAIL, albeit on an economically zero spread. Label it FAIL-with-noise-explanation for transparency (the explanation itself is correct).
  - File: results/table_1_eval.json (Leverage_spread_10_1)
  - Specific fix: change status to FAIL with reason "sign flip on ~0 spread (noise); both |spread| < 0.02"
- [m2] Latent path bug: `src/main.py:36` `REPO = Path(__file__).resolve().parents[2]` resolves to `rep-it-up/replications`, and `LAYOUT.ensure()` created an empty nested `replications/<slug>/{data,src,results,logs,inputs,preparations}` tree inside the slug (0 files, verified). Results are unaffected (all outputs are in the correct locations), but the orphan tree should be deleted and the path fixed.
  - File: src/main.py:36; orphan dir: `replications/asset_growth_and_the_cross_section_of_stock_returns/replications/`
  - Specific fix: `parents[3]` (or import the layout without the manual sys.path insert) and remove the empty nested directory
- [m3] REPORT.md §7 and log1.md report the tally as 74/43/2/0 without noting that 13 Tier-2 cells fall outside the 2× bound under the auditor's convention; add a one-line note once M2 is done so the headline count is not read as a strict-Tier-2 claim.
  - File: REPORT.md:75-85
  - Specific fix: footnote the tally with the strict-convention count (74/30/15)
- [m4] The 5-year cumulative event-time spread (−106.47%, Tier 1) depends on the extended return window through Jun-2007, which is not cached in `data/`; the auditor verified the construction on the cache-verifiable Year-1 portion (exact match) and the overlap claim, but not Years 2–5. Consider caching the extended panel (or the 35×10×5 event-time matrix) so the committed metric is fully re-derivable from `data/`.
  - File: src/table_2_event_time.py (extended window pulled live from ClickHouse)
  - Specific fix: write the extended panel or the event-time return cube to `data/` as a cached intermediate

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Auditor recomputed from panel.parquet: EW Year-1 means strictly decreasing D1→D10 (2.024→0.311 %/mo), matching the paper's "perfectly monotonic across all 10 deciles" (content.md L1530); VW shows the same mild mid-decile hump the paper's own VW panel has |
| 2 | Headline-magnitude claim | ✓ | EW spread −1.7128 (paper −1.73, 1.0% off), VW −1.0314 (paper −1.05, 1.6% off); iid t −8.64/−4.41 (paper −8.45/−5.04); ASSETG decile medians D1 −0.1817/D5 0.0750/D10 1.1409 reproduce the eval JSON exactly |
| 3 | Sample coverage ≥ 60% | ✓ | 104,006 formation firm-years / 35 years (avg 2,972 stocks/yr; 1990 = 2,953; 2000 = 4,325); FM inclusion keeps 99,402 (95.6%); panel 1,203,865 firm-months over 420 months; control non-null rates 80–100% by design; zero duplicate (permno, june_year) |
| 4 | Data-source choice justified | ✓ | CRSP/Compustat/FF identical to paper; FF3 taken as the Mkt-RF/SMB/HML/RF subset of `ff.four_factor_monthly` (no monthly three-factor table exists; documented A5 and data_verification.json); delisting −0.30 convention, December-(t−1) BM denominator, and funda de-duplication all documented in assumptions.md with paper citations |
| 5 | prep_validation.py exit 0 | ✓* | Pre-audit run exits 1 with exactly two layout errors: missing `logs/audit*.md` and missing `SUMMARY.md` — i.e., the auditor's own deliverables; the prep contract itself validates clean. Re-run after writing this audit + SUMMARY.md |
| 6 | All committed tables have results files | ✓ | T1–T4 each have `results/table_<n>.md` + `table_<n>_eval.json`; Table V exclusion documented (SEO/repurchase announcement data unavailable) |
| 7 | SUMMARY.md/REPORT.md matches results | ✓ | Spot-checked ~12 numbers: 119-cell tally (74/43/2/0) matches the four eval-JSON tallies; EW/VW spreads, FF3 alphas, M1 coef/t, M4 ASSETG t −6.05, ΔPPE t −5.00, diagnostics Sharpe/FF5 numbers all traceable to results/ files |
| 8 | No orphan folders | ✗ (minor) | One empty nested `replications/<slug>/` tree inside the slug (0 files) from the `parents[2]` path bug — [m2] |
| 9 | Diagnoses paired with fix attempts | ✓ | All 5 iteration-log entries in assumptions.md carry Diagnosis / Next fix / Before / After / Status; the VW-weighting bug was caught, fixed with a paper-grounded change (Assumption 9), and the spec-literal event-time variant was computed, flagged, and rejected with evidence |
| 10 | Tier 2 within 2× magnitude | ✗ | 30 of 43 Tier-2 cells are within 2×; 13 are outside (ratios from 0.10× to 11.2×) — [M2]. None touch the headline claims; root causes verified as noise-level (5), definitional (4, = M1), data-coverage (4, = M3, auditor-verified in ClickHouse) |
| 11 | Corollary coverage | ✓ | Every central paper corollary has a computed, checkable result: subperiod stability (Table II-F and Table III-d; the paper's own lone VW 1968–80 exception reproduces), size groups (all three negative/significant), factor loadings (FF3, FF4; FF5/CMA as a documented supplementary lens), 5-year persistence (event time), robustness specs (winsorization, monthly dependent, EW/VW), predictor dominance (M2–M7), decomposition mechanism |

### Additional methodology verifications (re-executed by auditor)

| Check | Result | Notes |
|---|---|---|
| FF3/FF4 alpha spreads | ✓ | Re-derived with Period-aligned factors: EW all-firm −1.4874 (eval −1.4874; paper −1.63), VW −0.5559 (−0.5566; −0.70); size groups EW −1.6224/−0.7084/−0.5773 and VW −1.3299/−0.5602/−0.4383 all reproduce the eval JSON; FF4 EW −1.2873 / VW −0.4183 ✓. (An initial auditor mismatch came from timestamp-vs-Period alignment in the auditor's own script, not the replication.) |
| VW fixed-formation-weight convention (A9) | ✓ | Fixed June-t ME reproduces the paper's VW levels (D1 1.47/D10 0.44); contemporaneous `me` weighting independently reproduced the rejected 2.77/1.83/−0.94 bias |
| Table III M1 Fama–MacBeth | ✓ | Auditor's independent FM implementation (annual geometric return, paper inclusion filter → 99,402 firm-years, listwise 81,333, 2,323.8/yr): const 0.1386 (t 4.55) ≈ paper 0.1373 (4.55); ASSETG −0.0649 (−5.34) = eval exactly (paper −0.0922, −6.52; 29.6%/18.1% off, within the ±40% tol); BM 0.0284 (3.11); MV $B −0.0036 (−1.39) |
| AR(1) SE convention (footnote 13) | ✓ | `SE × √((1+ρ)/(1−ρ))` reimplemented from scratch; all M1 t-stats match the eval JSON to 2 decimals |
| Winsorized M1 (paper robustness) | ✓ | −0.0947 (t −6.64) reproduced exactly on the post-filter sample — it lands on the paper's main coefficient −0.0922, strong corroboration that the methodology is right and the raw-coefficient gap is the vintage tail |
| Table IV | ✓ | ΔPPE standalone −0.0977 (t −5.00) ≈ prose −4.80; full-model const t 5.62 ≈ paper 5.61; ΔPPE full −3.93 (−2.76); identity residuals 1.1e-13 / 5.7e-14 |
| No look-ahead / FF1992 timing | ✓ | `june_year = fyear + 1` (src/main.py:176); non-December fiscal year-ends only increase the lag; sort uses FY t−1 vs t−2 data; holding returns are forward July t–June t+1 |
| Universe filter | ✓ | PIT join on msfhdr begdat/enddat, hshrcd ∈ (10,11), hexcd ∈ (1,2,3), SIC 6000–6999 excluded (src/sql/universe_monthly.sql); CCM link linkprim='P', linktype ∈ ('LU','LC'), usedflag=1, PIT windows |
| De-duplication (A3) | ✓ | SQL keeps non-null-`at`, latest datadate per (gvkey, fyear); 0 duplicate keys in formation.parquet |
| Delisting (A1) | ✓ | 27,986 panel months with ret ≤ −0.295 (adjusted/imputed); 0 months with ret < −1 |
| Data-vintage claim | ✓ | Auditor-verified: whole-sample P5 = −0.2135 ≈ paper D1 −0.2115, median 0.0936 ≈ paper D5 0.0961; 363 obs with ASSETG > 10 (max 47,500); yearly cross-sectional std 28.67 (88.1 last decade) vs paper's ~0.60/~0.95 (content.md L114); pre-1971 `ch` 93% null / `txp` 53–56% null confirmed in funda |
| Paper target values | ✓ | Spot-checked cited paper lines: L166/230/310/326/342 (−0.2115/0.0961/0.8357/1.0471/15.60), L1530 (1.99/0.26/−1.73/−8.45; 1.48/0.43/−1.05/−5.04), L33 (Sharpe 1.07; 18%/5%; 71%/91%), L1554/1566 (−87.99%, −49.67%, t −8.63/−4.25), L1667/1668/1682 (0.1373/−0.0922/−6.52), L2658 (−3.34 to −4.80; −3.74/−2.76). The prose-vs-table −4.80 ambiguity is genuine in the parsed paper; the replication's resolution in favor of the prose (ΔPPE −5.00 ≈ −4.80) is sound |
| Annual stats | ✓ | EW low>high 97.1% (paper 91), VW 77.1% (71); VW annual spread Sharpe 0.702 (1.07); annualized VW D1 19.18%/D10 5.43% (paper ~18/5.2) |
| Event-time Year 1 | ✓ | Auditor recomputed the offset-averaged construction from the cache: EW D1/D10/spread 26.37/3.53/−22.84 — exact match to the reported values; VW 18.99/5.32/−13.68 ≈ reported 19.01/5.32/−13.69. Years 2–5 use the uncached extended window (see [m4]) |

## 4. Issues the agent should have caught (didn't)

1. **The 2× Tier-2 bound.** The evaluation harness graded Tier 2 as "sign matches, outside tolerance" with no magnitude cap, so cells at 3.9× and 0.10× were labeled pattern-matches. A pre-audit self-check against the audit convention would have pre-labeled the 13 cells and avoided overstating the 43-cell Tier-2 count.
2. **ISSUANCE fix left on the table.** Assumption 8 correctly identifies split-adjusted shares as the likely paper convention but stops at "additional data work" — it is a cheap computation (CRSP adjustment factors) that would have settled whether the 4 ISSUANCE cells are definitional or vintage.
3. **The Leverage spread sign flip was laundered into Tier 2** as "lenient." The honest label is FAIL-on-a-null-effect (which is what the agent's prose says anyway).
4. **The `parents[2]` path bug** was diagnosed and worked around but left an empty nested `replications/<slug>/` tree in the slug and was never cleaned up.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Asset Growth and the Cross-Section of Stock Returns" (Cooper, Gulen & Schill 2008) for slug `asset_growth_and_the_cross_section_of_stock_returns`. The previous agent run completed with verdict **PARTIAL** (audit 1 at `replications/asset_growth_and_the_cross_section_of_stock_returns/logs/audit1.md`). Read the audit first. The headline replication is verified sound — the auditor independently re-derived the Year-1 spreads, FF3/FF4 alphas, the Table III Model-1 statistics, the winsorized M1, and the Table IV t-stats from the cached data and all matched. Do NOT rebuild the foundation.

## Issues to address (priority order)

### [M1] — MAJOR (actionable) — ISSUANCE split-adjustment
Table I ISSUANCE (5-year share change) uses raw Compustat `csho` and runs 1.85–3.9× the paper (D1 0.148 vs 0.0803; D10 1.013 vs 0.3012; spread 0.865 vs 0.2209; t 12.11 vs 8.36). Assumption 8 already diagnosed the cause (mechanical split-induced share increases counted as issuance) and identified the fix but never executed it.

**Specific fix:**
1. In `src/main.py` (or a Table-I-only extension), compute 5-year share change using split-adjusted shares — CRSP cumulative adjustment factors chained over FY t−5 → FY t−1 (or CRSP `shrout`/`cfacshr` at the corresponding dates). Keep the raw-`csho` version alongside for transparency.
2. Recompute the 4 ISSUANCE cells in `results/table_1.md` + `table_1_eval.json` and compare to 0.0803/0.3012/0.2209/8.36. Verification: if the new magnitudes fall within ~1.5× of the paper, adopt the split-adjusted column as primary and document it as the refinement of Assumption 8; if not, keep raw with the documented ambiguity and relabel per [M2].
3. Update the ISSUANCE row discussion in REPORT.md §6/§8 either way.

### [M2] — MAJOR (partially actionable) — honest Tier-2 relabeling
13 of 43 Tier-2 cells violate the 2× magnitude bound (audit §2 M2 lists every cell and ratio): L2ASSETG_D1, L2ASSETG_t_spread, ROA_D1, ROA_t_spread, BHRET6_t_spread, ACCRUALS_D10, ISSUANCE_D10, ISSUANCE_spread_10_1, M1_MV, M6_ACCRUALS_ASSETG_t, M6_ACCRUALS_t, dOthAssets_alone_t, dCurAsst_full_t.

**Specific fix:**
1. Add a `within_2x` boolean to every Tier-2 cell in `results/table_{1,3,4}_eval.json`; reclassify the 13 as FAIL-with-documented-cause (data-coverage cells: M6_ACCRUALS_*, ACCRUALS_D10, dOthAssets_alone_t, dCurAsst_full_t — auditor verified pre-1971 `ch` 93%/`txp` 56% null in funda, so these are external limitations; near-zero cells: L2ASSETG_D1, ROA_D1/t, BHRET6_t; units cell: M1_MV — flag "$B scaling, t matches").
2. Update the tally in `results/evaluation_summary.md` and REPORT.md §7: strict-convention count is 74 Tier-1 / 30 Tier-2 / 15 FAIL (117/119 still sign/pattern-correct). The FAILs must be grouped by cause (noise-level nulls, documented data coverage, one definitional ambiguity) so the honest picture is clear.
3. [m1] Relabel `Leverage_spread_10_1` as FAIL-with-noise-explanation (sign flip on a ±0.016 spread).

### [m2] — MINOR — cleanup
Fix `src/main.py:36` (`REPO = parents[2]` → the wrong root) and delete the empty nested `replications/asset_growth_and_the_cross_section_of_stock_returns/replications/` directory tree. Verify `uv run python src/main.py` still resolves `utils.*` and writes to the correct `data/` location.

### [m4] — MINOR — cache the event-time intermediate
Write the extended (through Jun-2007) delisting-adjusted panel or the 35×10×5 event-time return cube to `data/` so the committed `EW_cumulative_Y1_5_spread` is re-derivable from cached artifacts without a live ClickHouse pull.

### Optional (not required to exit)
The paper's $10M total-assets screen robustness (content.md L1570) would be a clean independent adjudicator of the vintage story — running it on this vintage and reporting whether the raw ASSETG coefficient moves toward −0.0922 would strengthen Assumption 7. Only do this if budget remains; it is an unreported-in-the-paper robustness and is not required.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in `assumptions.md` must have all five fields: Diagnosis, Next fix, Before metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate to the human.
- **Do not game:** no invented screens or filters to force cells into tolerance — the audit verified the anti-gaming stance of iteration 1 and it should hold.

## Inputs you should read

- `replications/asset_growth_and_the_cross_section_of_stock_returns/logs/audit1.md` — this audit (full context)
- `replications/asset_growth_and_the_cross_section_of_stock_returns/inputs/content.md` — paper ground truth
- `replications/asset_growth_and_the_cross_section_of_stock_returns/preparations/` — prep contract + assumptions
- `replications/asset_growth_and_the_cross_section_of_stock_returns/src/main.py` — current code
- `replications/asset_growth_and_the_cross_section_of_stock_returns/data/` — cached intermediates

## What NOT to redo

- Do NOT rebuild the data foundation, the panel, or Tables II–IV results — the auditor re-derived them and they match. Regenerate only what M1/M2 touch.
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact.
- Skip the ClickHouse catalog scan — `data_verification.json` is current.

## Deliverables for this iteration

- `src/main.py` (+ table_1.py) — split-adjusted ISSUANCE; path-bug fix
- `results/table_1.md` + `results/table_1_eval.json` — updated ISSUANCE cells; `within_2x` flags on all Tier-2 cells across all four eval JSONs
- `results/evaluation_summary.md` — strict-convention tally with cause-grouped FAILs
- `preparations/assumptions.md` — append iteration-log entries (all five fields) for M1, M2, m2, m4
- `REPORT.md` — update the tally and the ISSUANCE discussion; lead with the data-quality summary
- Do NOT edit `SUMMARY.md` (auditor-owned)

## Stop conditions

- M1 executed (split-adjusted ISSUANCE computed and compared, outcome documented either way), M2 relabeling done, minors cleaned up → declare success for this iteration; the next audit updates SUMMARY.md.
- If split-adjusted shares are genuinely unavailable for the 5-year windows (e.g., adjustment factors missing pre-1983), document the attempt with before/after metrics and exit partial on that cell.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the cleaner replications I have audited. The decisive evidence is structural: if the signal, universe, timing, weighting, or delisting treatment were wrong, the Year-1 decile returns could not land within 1–2% of the paper's — and they do, independently recomputed from the cached parquets (EW spread −1.713 vs −1.73; VW −1.031 vs −1.05; EW perfectly monotonic). The Fama–MacBeth pipeline reproduces to two decimals under a from-scratch reimplementation of the paper's unusual footnote-13 AR(1) SE adjustment, the intercept matches the paper's almost exactly (0.1386 vs 0.1373), and the winsorized coefficient landing on the paper's main coefficient (−0.0947 vs −0.0922) is exactly the corroboration pattern one wants: methodology right, vintage different. The data-vintage story is not a rhetorical cover — I verified in ClickHouse that the 2026 funda vintage has 93% null `ch` and 53–56% null `txp` in FY1966–68 and that the ASSETG cross-sectional standard deviation is ~29 (88 in the last decade) against the paper's reported ~0.60; meanwhile the lower tail and median of the distribution match the paper's decile medians almost exactly, which is the signature of a fattened upper tail, not a formula error. The two FAILs are honest noise (sign flips on coefficients that are statistically zero in both papers), and the Table IV prose-vs-table −4.80 ambiguity is real in the parsed paper — the replication's resolution in favor of the prose is well-grounded. The remaining work is small and mostly cosmetic: execute the already-diagnosed ISSUANCE split-adjustment, and relabel the 13 Tier-2 cells that exceed the 2× bound under the strict audit convention so the published tally (74/43/2) cannot be read as a strict-pattern claim. With those done, this replication is at PASS quality.
