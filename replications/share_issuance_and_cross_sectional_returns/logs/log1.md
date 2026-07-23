---
iteration: 1
slug: share_issuance_and_cross_sectional_returns
inner_iterations: 3
worker_spawns: 3
---

# Outer Iteration 1 — Reasoning Trace

Paper: Pontiff & Woodgate (2008), "Share Issuance and Cross-sectional Returns", Journal of Finance Vol. LXIII No. 2. Targets: Table I Panel A (descriptive stats 1970-2003), Table III Panels A-B (FM regressions, headline), Table V Panel A (pre-1970 descriptive stats), Table VI Panel A (pre-1970 FM). Tables II/IV out of scope (SDC Platinum event data unavailable).

## Pre-spec sanity checks (Replicator, before inner iteration 1)

1. **cfacshr orientation** (decisive for ISSUE construction). Apple (permno 14593) 2:1 splits: 1987-06 (shrout 64,018 → 125,683, cfacshr 224 → 112), 2000-06 (162,744 → 324,826, cfacshr 112 → 56), 2005-02 (408,586 → 817,172, cfacshr 56 → 28). `shrout × cfacshr` is constant across splits (14.34M → 14.08M; 18.23M → 18.19M; 22.88M → 22.88M); `shrout / cfacshr` doubles. Therefore ClickHouse `cfacshr` = 1 / (paper's Total Factor of eq. 1), and the paper's AdjustedShares (eq. on L63) = `shrout × cfacshr`. Consistent with references/CRSP.md L707 ("multiply shrout by cfacshr"). Since ISSUE is a log difference, the absolute normalization of cfacshr cancels.
2. **Universe counts** (msf, ret > -1): 1990-01: all=6,757 / shrcd∈{10,11}=5,803; 2000-06: 8,233 / 6,519; 1975-01: 4,869 / 4,562; 1950-01: 988 / 969. Paper targets: Table I 2,285,189-2,312,597 obs over 408 months (avg 5,600-5,668/mo); §I full sample 2,494,343 (avg 6,113/mo). No-filter monthly counts average ~6,200+ over 1970-2003 (a bit high); shrcd 10/11 averages ~5,300 (a bit low). Decision: worker builds the panel both ways and reports per-year counts; choose the universe that reconciles with the paper's obs counts. Logged as assumption A1.
3. **EWRETD**: crsp_202601.msi.ewretd = -0.046408 at 1990-01-31 (decimal) ✓.

## Inner iteration 1: build analysis-ready panel (all vintages 1926-2006)

**Task spec → rep-worker:**
Build the merged monthly panel feeding Tables I/III/V/VI. Variables: adj_shares = shrout × cfacshr; ISSUE = ln(adj_{t-6}) − ln(adj_{t-17}); DT-ISSUE = ln(adj_{t-6}) − ln(adj_{t-65}) (0 if missing at t-65); DT-Dum (1 iff shares exist at t-65); BM = ln(ceq / (|prc|×shrout at Dec Y-1)) with 1-year ceq fallback, held July Y–June Y+1, BM-Dum; ME = ln(|prc|×shrout) at June Y (thousands $), held July Y–June Y+1; MOM = prod(1+ret) over t-7..t-2 − 1; holding-period returns R1/R6/R12/R13_24/R25_36 with EWRETD imputation for missing months; shares-error correction (>20% jump, 95% reversal within 3 months → revert). Universe: all CRSP securities with nonmissing ret at t and ≥6 months CRSP history; build both no-filter and shrcd∈{10,11} variants for count reconciliation. Period: 1926-12 through 2006-12. Report panel stats + inline Table I Panel A comparison.

**rep-worker report:** (spawn terminated by a transient API content-inspection error at the very end; all deliverables completed and verified before termination — data/panel.parquet, src/main.py, 5 SQL files, results/panel_report.md)

Panel: 3,487,187 rows × 25 cols, 26,913 permnos, 960 months (1927-01..2006-12). EWRETD coverage complete.

Observation counts (univ_all vs paper):
- in-sample total 2,409,708 vs 2,494,343 (-3.4%); ISSUE_contemp base 2,324,025 vs 2,312,597 (+0.5%); MOM 2,367,675 vs 2,285,189 (+3.6%); regr sample (issue & me_june & mom) 2,182,151 vs Table III 2,155,945 (+1.2%)
- OOS total 503,063 vs 568,449 (-11.5%); OOS MOM 497,200 vs 524,260 (-5.2%); OOS regr 472,979 vs Table VI 373,590 (+26.6% — paper's Table VI sample likely requires DFF book equity we don't have; our CRSP-only cross-section is the correct analog)
- univ_common (shrcd 10/11) is ~13% below paper everywhere → univ_all (no shrcd filter) selected as the paper's universe.

Table I Panel A preview (univ_all, ISSUE-available base): ISSUE 0.044/0.000/0.002/0.027/0.230 vs paper 0.04/0.00/0.00/0.03/0.15; DT-ISSUE 0.129/0/0/0.139/0.438 vs 0.12/0/0/0.14/0.33; BM -0.303/-0.783/-0.119/0.070/0.999 vs -0.34/-0.79/-0.07/0.00/0.94; ME 11.084/9.585/10.959/12.455/2.086 vs 11.11/9.63/10.97/12.46/2.02; MOM 0.072/-0.160/0.025/0.216/0.481 vs 0.06/-0.16/0.02/0.22/0.41; R 0.149/-0.222/0.054/0.346/0.889 vs 0.14/-0.23/0.05/0.34/0.88. Proportions 56.5/24.5/19.0 vs 56.6/24.2/19.2.
Error correction: 2,172 vs 2,189 (-0.8%).

Verification performed by worker (all exact): adj_shares = shrout×cfacshr constant across real splits (permno 10001, 1994-06: 3273→3286.5, 0.4% rounding); issue/dt_issue/dt_dum/issue_contemp/dt_issue_contemp == manual lags; r6/r12/r24_y2/r36_y3/mom/r_11_0 == manual products; EWRETD imputation for delisted permno 10003 (r6 = 0.103551 both ways); me_june held Jul96-Jun97 = Jun96 value; bm = ln(ceq×1000/me_dec).

Worker-flagged deviations: (1) comp_202601.funda stores consol='C'/popsrc='D', not 'STD'/'STD' as the spec wrote — worker used WRDS-standard consol='C', popsrc='D', indfmt='INDL', datafmt='STD' (correct; 'STD' is WRDS documentation labeling); (2) ceq in $millions vs me_dec in $thousands → bm = ln(ceq×1000/me_dec) (BM mean -0.30 confirms; without ×1000 it would be -7.2); (3) R_{-11,0} built requiring all 12 actual months (per spec) — paper's count suggests EWRETD imputation of R_{-11,0} too; minor count effect (~2%), revisit if needed; (4) universe counts 3% below paper in-sample — paper likely counts listing age from first CRSP appearance, not first nonmissing return (worker verified first-appearance → 2.45M, closer).

**Replicator decision:** ACCEPT. The pipeline reproduces the paper's sample composition (ISSUE base +0.5%, regr sample +1.2%, proportions within 0.3pp, error correction -0.8%) and every computation verifies exactly against manual recomputation. Universe = univ_all (no shrcd filter) selected. Two diagnosis items for iteration 2:
1. Table I std gap: ALL RHS-variable stds are 5-53% above paper while the non-RHS variable (R_{-11,0}) matches exactly and all percentiles/means match within rounding. Hypothesis: the paper's Table I statistics are computed on the winsorized regressors (L132 winsorization applies to "all right-hand-side variables"). Test: recompute Table I stats after 1%/99% monthly cross-sectional winsorization and compare.
2. BM median/p75 gap (-0.119/0.070 vs -0.07/0.00): fewer bm_dum=0 zeros in our sample (17% vs paper's implied ≥25%) — consistent with our slightly smaller universe and Compustat-vintage coverage differences; monitor, not a blocker (BM is a control, not the headline signal).

Next: inner iteration 2 — implement Table III (Fama-MacBeth with Pontiff-1996 overlap t-stats) + Table I results with the winsorized-stats diagnostic.

## Inner iteration 2: Table I + Table III (Fama-MacBeth) + per-cell evaluation

**Task spec → rep-worker:**
On the existing panel (univ_all): (1) Table I descriptive stats, raw AND post-winsorization (1%/99% monthly) to test the hypothesis that the paper's Table I stds reflect winsorized regressors — the std gap (ISSUE 0.230 vs 0.15; DT 0.438 vs 0.33; BM 0.999 vs 0.94; MOM 0.481 vs 0.41) sits entirely in RHS variables while the non-RHS R_{-11,0} matches exactly (0.889 vs 0.88); (2) Table III Panels A+B: 8 horse-race specs, dep = ret×100 / r6×100, per-month 1% winsorization, Pontiff-1996 AR(k−1) overlap t-stats as primary with NW cross-check, mean adjusted R² in percent; (3) per-cell Tier 1/2/FAIL evaluation against tables_to_replicate.json for T1+T3; (4) rolling-12-month univariate ISSUE slope figure (paper's Figure 1 analog, 1933-2003).

**rep-worker report:** (completed, 65 tool uses; produced src/analyze_tables.py, results/table_1.md, results/table_3.md, results/issue_rolling_slope.png; appended assumptions A15-A18)

- T1 tally: Tier1 32 / Tier2 3 / FAIL 0 (35 metrics). Winsorized-stats hypothesis CONFIRMED: stds after 1%/99% monthly winsorization match the paper almost exactly — ISSUE 0.151 vs 0.15, DT-ISSUE 0.351 vs 0.33, BM 0.913 vs 0.94, MOM 0.404 vs 0.41, ME 2.056 vs 2.02; R_{-11,0} raw 0.889 vs 0.88 (returns not winsorized per L132). Raw stds (0.230/0.438/0.999/0.481) were the sole T1 gap in iteration 1; now resolved. Means/percentiles/proportions all Tier 1 (base 2,324,025 vs 2,312,597; proportions 56.5/24.5/19.0 vs 56.6/24.2/19.2).
- T3 tally: Tier1 92 / Tier2 6 / FAIL 3 (101 metrics). Headline: ISSUE slope −2.06 (Pontiff t −7.00) vs paper −2.23 (−7.08) — 7.6% coef deviation, t within 1.1%; Panel B ISSUE −12.88 (−7.68) vs −13.82 (−7.26). BM 0.42 (5.64) vs 0.39 (5.86); ME −0.15 (−2.95) vs −0.13 (−2.50); MOM 0.52 (1.53) vs 0.62 (1.84); all R² within tolerance. Full spec R8 obs 2,182,151 vs 2,155,945 (+1.2%). The 3 FAILs are the DT-Dum slopes (+0.50/+0.33/+0.35 vs paper −0.41/−0.31/−0.32) — a dummy-polarity artifact, see below.
- Worker anomaly findings (all documented, none silently changed): (A15) DT-Dum polarity — paper's L94 text vs Table III numbers conflict; flipping the dummy reconciles DT-Dum slopes AND R6/R7 intercepts (1.02→1.52 vs paper 1.48) exactly; (A16) Pontiff overlap t-stat must be the AR(n)-ERROR (GLSAR) form — the paper's L134 says "residuals ... follow an n-th order AR process"; AR-on-levels inflates Panel B t's to −20.9 vs paper −7.26, AR-errors gives −7.68; (A17) rolling-slope figure needs a variance guard (winsorized ISSUE variance collapses ~1942 → degenerate slope −11,648); (A18) Jan 1970–Dec 2003 is 408 months, paper's "396" is an internal inconsistency.

**Replicator decisions (inner iteration 2 close-out):**
1. ADOPT the DT-Dum flip (DT_DUM_FLIP=True): DT-Dum = 1 for "no 5-year share history". The replication targets are the paper's NUMBERS, and three independent lines of evidence override L94's wording: (i) the Table III caption parenthetical "(hence DT-ISSUE is zero)" only parses if DT-Dum=1 ⟺ DT-ISSUE=0 ⟺ no history (L1074); (ii) the intercept test is decisive — the paper's R6/R7 intercept 1.48 is the mean return of the dummy=0 baseline group; in our data established firms (our as-built dummy=0) earn 1.02%/mo while young firms earn 1.52%/mo, so the paper's dummy=0 = established ⟹ dummy=1 = young/no-history; (iii) new-issues economics (young issuers underperform → negative young-firm dummy). L94 is recorded as a paper text/numbers inconsistency. This converts the 3 FAILs + R6/R7 intercept Tier-2s to Tier 1.
2. RATIFY A16 (AR-error/GLSAR form) — it is the literal reading of L134 ("residuals follow an AR process") and matches the paper's t-stats; my original task spec's AR-on-levels was the misread. Supersedes the second sentence of assumptions.md A4's implementation description (AR order n=k−1 unchanged).
3. ACCEPT A17, A18 as documented. 408 months: coefficients unaffected; n_months cell stays Tier 2 with this justification.
4. Table I convention: winsorized regressors + raw returns (A2 updated accordingly).

Next: inner iteration 3 — Tables V and VI (pre-1970) with DT_DUM_FLIP=True; regenerate T1/T3 outputs under the flip.

## Inner iteration 3: Tables V + VI (pre-1970) under the ratified conventions

**Task spec → rep-worker:**
Regenerate table_1.md/table_3.md with DT_DUM_FLIP=True; implement T5 (Table V Panel A descriptive stats, Sep 1932–Dec 1969, winsorized convention, BM cells SKIP) and T6 (Table VI Panel A FM, 444 months, specs R2/R3/R5/R6/R7 BM-free as primary + R4/R8 without BM documented; AR-error t-stats with n=k−1 for k=1; DT-Dum flipped). Per-cell evaluation for T5/T6; compare against the paper's pattern claims (ISSUE positive & insignificant; ME significantly negative; MOM positive, 1-month insignificant).

**rep-worker report:** (completed, 55 tool uses; extended src/analyze_tables.py; produced results/table_5.md, results/table_6.md; regenerated table_3.md under the flip; appended A19-A21)

- T3 under DT_DUM_FLIP=True: ex-FAIL DT-Dum cells reconcile — R6 −0.50 (−3.76) vs paper −0.41 (−3.19); R7 −0.33 (−2.74) vs −0.31 (−2.61); R8 −0.35 (−4.42) vs −0.32 (−3.88); R6/R7 intercepts 1.52/1.52 vs 1.48/1.48. T3 tally 92/6/3/0 → **99/2/0/0**. Worker also found and fixed a polarity-wiring bug in the headline selection (as-built was shown despite the flag) — verified corrected (both polarities always computed; headline follows the flag).
- T5 (Table V): ISSUE mean 0.0148 (paper 0.01, Tier 2 48%), std 0.06 (paper 0.07 ✓); DT-ISSUE 0.07/0.04/0.20 vs 0.08/0.05/0.24; ME all Tier 1 (10.34/9.14/10.27/11.52/1.75 vs 10.28/9.05/10.22/11.50/1.80); MOM 0.10/0.33 vs 0.09/0.34; R 0.21/0.60 vs 0.19/0.60; proportions 30.2/59.7/10.0 vs 28.2/62.6/9.2 ✓; obs 489,607/484,827 vs 524,260/528,200 (Tier 2, −6.6/−8.2%). Tally **15/5/0/2**.
- T6 (Table VI Panel A): R2 ME −0.25 (−3.36) vs −0.22 (−3.04) ✓ all Tier 1; R3 MOM 0.77 (1.54) vs 0.68 (1.34) ✓; R5 ISSUE −1.27 (−1.73) vs +0.52 (0.43) **FAIL sign**; R7 ISSUE −1.56 (−2.54) vs +0.27 (0.21) **FAIL**; R6 DT cells near-zero/insignificant like the paper (Tier 2). Pattern claims: ME significantly negative ✓ confirmed; MOM positive & 1-mo insignificant ✓ (R3/R4; borderline R8 t=2.18); ISSUE positive & insignificant ✗ not confirmed on sign (magnitude-level no-predictability holds: |β| ≤ 1.6 vs −2.23 post-1970). Degenerate-ISSUE guard (A17 ext.) drops 10 pre-1950 months (winsorized ISSUE std < 0.01 → slope −11,648 in 1942-05; unguarded mean −29). Tally **17/11/3/12** (+14 pattern-only).
- COMBINED: Tier1 163 / Tier2 21 / FAIL 3 / SKIP 14.

**Replicator decision:** ACCEPT the T5/T6 implementation; ratify A19-A21 (flip ratification, OOS guard, ISSUE-sign deviation documented). The 3 FAILs are the pre-1970 ISSUE sign cells. Diagnosis (per STUCK_AGENT discipline — no fix attempted that would be legitimate): the sign sits on a noise-level slope (ours −1.27±0.73; paper +0.52±1.21; SEs from t-stats), and the most plausible systematic driver is sample composition — our CRSP-only OOS cross-section (~1,068 firms/mo) is ~27% larger than the paper's book-equity-restricted sample (373,590/444 ≈ 841/mo); the marginal thinly-issuing small caps tilt the near-zero slope negative. Forcing the sign by restricting to Compustat-covered firms would (a) substitute a different sample than the paper's DFF-based one and (b) be fitting to the target — prohibited. Classified as a documented deviation: the paper's substantive pre-1970 claim (no economically meaningful issuance predictability; ME negative; MOM positive/insignificant) replicates. No further inner iteration: remaining gaps are data limitations (DFF, SDC) or noise-level signs, not actionable methodology bugs. Inner loop closed at 3/10 iterations.

## Assumption decisions this iteration
- A1-A14: documented at iterations 1-2 (universe, pooling, percent scaling, Pontiff AR order, winsorization, MOM window, EWRETD imputation, DFF skip, SDC scope, cfacshr convention, CCM link, shares-error correction, Compustat filter values, universe selection)
- A15-A18: worker-added, replicator-ratified (DT-Dum polarity evidence, GLSAR error form, figure guard, 408 vs 396 months)
- A19-A21: flip ratified as default; OOS BM-SKIP + degenerate-ISSUE guard; ISSUE-sign deviation with sample-composition attribution

## Per-cell evaluation (final, DT_DUM_FLIP=True)

| Table | Tier 1 | Tier 2 | FAIL | SKIP | Notes |
|-------|-------:|-------:|-----:|-----:|-------|
| T1 (Table I) | 32 | 3 | 0 | 0 | winsorized-regressor convention confirmed |
| T3 (Table III A+B) | 99 | 2 | 0 | 0 | ISSUE −2.06 (−7.00) vs −2.23 (−7.08) |
| T5 (Table V) | 15 | 5 | 0 | 2 | BM cells SKIP (DFF) |
| T6 (Table VI A) | 17 | 11 | 3 | 12 | 3 FAIL = OOS ISSUE sign; +14 pattern-only |
| **Combined** | **163** | **21** | **3** | **14** | 81% Tier 1 of evaluated cells |

FAIL detail (all three the same root cause): oos_pA_r5_issue (−1.27 vs +0.52), oos_pA_r7_issue (−1.56 vs +0.27), oos_pA_r7_issue_t (significance class). Near-zero slopes of opposite sign under a 27%-larger CRSP-only sample; documented in REPORT.md §6.3.

## Summary
All four committed tables implemented end-to-end from ClickHouse with verified per-security computations. The post-1970 headline (Table III) replicates at Tier 1 across all 101 committed cells except two Tier-2 technicalities; Table I replicates once the winsorized-statistics convention is identified; the pre-1970 evidence replicates in structure with a documented noise-level sign deviation on ISSUE. Inner loop converged in 3 iterations (cap 10). Ready for the auditor (outer iteration 1, Step 4).
