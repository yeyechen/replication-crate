# Table III — Fama–MacBeth Cross-Sectional Regressions, 1970–2003
## (Pontiff & Woodgate 2008)

**Universe:** `univ_all` (A14).  **Regression months:** Jan 1970 – Dec 2003 (our data supports all **408** months; the paper reports 396 — see flag below).  **Dependent variables:** Panel A = `ret×100` (1-month); Panel B = `r6×100` (6-month).  PERCENT scaling is mandatory (A3).  All RHS variables winsorized at 1%/99% within each monthly cross-section (A5).  Cells show **coef (Pontiff t-stat)**; Newey-West(k−1) t-stats are listed in the appendix.  `DT_DUM_FLIP=True` — **headline DT-Dum polarity: FLIPPED (dt_dum=1 ⇒ NO 5-yr history)**.

> ⚠️ **Month-count flag:** Jan 1970–Dec 2003 inclusive is 408 calendar months; the paper prints 396 (= 33 yr) while naming the 1970–2003 range — an internal inconsistency in the paper. Our panel has valid regressions in all 408 months, so we use 408. Coefficients (time-series means) are essentially unaffected by the 12-month difference.

> ✅ **DT-Dum polarity (REPLICATOR-RATIFIED: `DT_DUM_FLIP=True`).** The panel stores `dt_dum=1` for firms WITH a 5-year share history (paper L94: "set the D-T dummy = 0 [for <5-yr firms]; otherwise = 1"). With that as-built definition the DT-Dum slope is **positive** (+0.50/+0.33/+0.35 in R6/R7/R8), the OPPOSITE sign of the paper's printed **negative** values (−0.41/−0.31/−0.32) → 3 FAILs. Three independent lines of evidence show the paper's *reported numbers* use the COMPLEMENT (`dt_dum=1` = NO 5-year history): (1) the Table III caption parenthetical "DT-Dum is set to one if shares outstanding exists at t−65 (hence DT-ISSUE is zero)" only parses if DT-Dum=1 ⇔ DT-ISSUE=0 ⇔ no history; (2) flipping reproduces the negative DT-Dum slopes AND the R6/R7 intercepts (diagnostic below); (3) economics — young/recently-listed firms (no history) underperform (new-issues puzzle), so a no-history dummy should load negative. **Headline = flipped** (the 3 DT-Dum cells reconcile to Tier 1 and the R6/R7 intercepts move 1.02/1.19 → 1.52/1.52, paper 1.48/1.48). The as-built numbers are retained in the diagnostic table below for transparency. A 0/1 dummy flip changes ONLY the intercept and DT-Dum's own coefficient; every other coefficient (BM, ME, MOM, ISSUE, DT-ISSUE) is identical under both polarities.

## Panel A — dependent variable: 1-month return (ret×100)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 0.93 (3.49) | 0.42 (5.64) | 0.53 (6.09) |  |  |  |  |  | 0.73 | 2,409,708 |
| R2 | 2.88 (4.04) |  |  | -0.15 (-2.95) |  |  |  |  | 1.14 | 2,375,719 |
| R3 | 1.17 (4.42) |  |  |  | 0.52 (1.53) |  |  |  | 1.24 | 2,367,675 |
| R4 | 2.43 (3.58) | 0.28 (3.93) | 0.58 (7.12) | -0.15 (-2.95) | 0.46 (1.47) |  |  |  | 2.89 | 2,348,275 |
| R5 | 1.39 (4.95) |  |  |  |  | -2.06 (-7.00) |  |  | 0.20 | 2,203,273 |
| R6 | 1.52 (5.86) |  |  |  |  |  | -0.68 (-5.21) | -0.50 (-3.76) | 0.56 | 2,409,708 |
| R7 | 1.52 (5.86) |  |  |  |  | -1.51 (-6.37) | -0.42 (-3.63) | -0.33 (-2.74) | 0.62 | 2,203,273 |
| R8 | 2.95 (4.41) | 0.21 (3.16) | 0.44 (5.11) | -0.17 (-3.26) | 0.32 (1.06) | -1.23 (-6.12) | -0.33 (-3.43) | -0.35 (-4.42) | 3.32 | 2,182,151 |

_Panel A: holding period k=1 → Pontiff AR order n=0, Newey-West lags=0 (n=0 ⇒ plain FM t-stat). Months fitted: 408._

## Panel B — dependent variable: 6-month return (r6×100)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 5.52 (3.63) | 2.63 (5.38) | 3.52 (4.71) |  |  |  |  |  | 1.34 | 2,409,708 |
| R2 | 15.71 (3.86) |  |  | -0.73 (-2.77) |  |  |  |  | 1.50 | 2,375,719 |
| R3 | 7.45 (5.16) |  |  |  | 6.75 (4.99) |  |  |  | 1.21 | 2,367,675 |
| R4 | 13.76 (3.45) | 1.77 (3.42) | 3.60 (6.29) | -0.78 (-2.80) | 6.37 (5.07) |  |  |  | 3.87 | 2,348,275 |
| R5 | 8.43 (5.65) |  |  |  |  | -12.88 (-7.68) |  |  | 0.40 | 2,203,273 |
| R6 | 9.16 (6.98) |  |  |  |  |  | -4.11 (-5.11) | -2.74 (-2.50) | 1.16 | 2,409,708 |
| R7 | 9.17 (6.98) |  |  |  |  | -9.81 (-7.63) | -2.47 (-3.47) | -1.86 (-1.77) | 1.27 | 2,203,273 |
| R8 | 16.27 (4.37) | 1.38 (3.10) | 2.78 (4.29) | -0.86 (-3.16) | 5.74 (4.75) | -7.78 (-7.38) | -1.74 (-3.02) | -1.59 (-2.34) | 4.53 | 2,182,151 |

_Panel B: holding period k=6 → Pontiff AR order n=5, Newey-West lags=5 (n=0 ⇒ plain FM t-stat). Months fitted: 408._

---

## Newey-West(k−1) t-statistics (reference; primary = Pontiff above)

| Panel | Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | R1 | 3.49 | 5.64 | 6.09 |  |  |  |  |  |
| A | R2 | 4.04 |  |  | -2.95 |  |  |  |  |
| A | R3 | 4.42 |  |  |  | 1.53 |  |  |  |
| A | R4 | 3.58 | 3.93 | 7.12 | -2.95 | 1.47 |  |  |  |
| A | R5 | 4.95 |  |  |  |  | -7.00 |  |  |
| A | R6 | 5.86 |  |  |  |  |  | -5.21 | -3.76 |
| A | R7 | 5.86 |  |  |  |  | -6.37 | -3.63 | -2.74 |
| A | R8 | 4.41 | 3.16 | 5.11 | -3.26 | 1.06 | -6.12 | -3.43 | -4.42 |
| B | R1 | 3.51 | 6.46 | 6.76 |  |  |  |  |  |
| B | R2 | 3.67 |  |  | -2.69 |  |  |  |  |
| B | R3 | 4.76 |  |  |  | 5.88 |  |  |  |
| B | R4 | 3.19 | 3.84 | 7.10 | -2.60 | 5.93 |  |  |  |
| B | R5 | 5.27 |  |  |  |  | -8.98 |  |  |
| B | R6 | 6.36 |  |  |  |  |  | -5.75 | -3.22 |
| B | R7 | 6.37 |  |  |  |  | -8.46 | -3.86 | -2.29 |
| B | R8 | 4.04 | 3.33 | 4.96 | -2.93 | 5.53 | -7.80 | -3.13 | -2.93 |

---

## Diagnostic — DT-Dum polarity reconciliation (Panel A R6/R7/R8)

Both DT-Dum polarities side by side. **FLIPPED (dt_dum=1 ⇒ NO 5-yr history) is the HEADLINE** used in the table above and in the per-cell tally; AS-BUILT (L94, dt_dum=1 ⇒ history exists) is shown for transparency. Only the intercept and DT-Dum coefficient differ; ISSUE / DT-ISSUE / all other coefficients are identical under both polarities.

| Row | Intercept (as-built → **FLIPPED**) | DT-Dum (as-built → **FLIPPED**) | DT-ISSUE | Paper Intercept | Paper DT-Dum | Paper DT-ISSUE |
|---|---|---|---:|---:|---:|---:|
| R6 | 1.02 → **1.52** | 0.50 → **-0.50** | -0.68 | 1.48 | -0.41 | -0.71 |
| R7 | 1.19 → **1.52** | 0.33 → **-0.33** | -0.42 | 1.48 | -0.31 | -0.38 |
| R8 | 2.59 → **2.95** | 0.35 → **-0.35** | -0.33 | 2.48 | -0.32 | -0.29 |

Under the HEADLINE flipped polarity the DT-Dum slopes match the paper (negative, within tolerance) and the R6/R7 intercepts move from 1.02/1.19 (as-built) to 1.52/1.52 (paper 1.48/1.48). The DT-Dum coefficient cells and the R6/R7/R8 intercepts are the ONLY cells affected by this choice.

---

## Appendix — per-cell evaluation vs tables_to_replicate.json (T3)

**Tally:** Tier 1 = 99 · Tier 2 = 2 · FAIL = 0 · SKIP = 0

Coefficients/intercepts/R²/counts compare our value to the paper. For t-stat metrics the **primary (Pontiff)** t is compared; the NW t is shown for reference. Tier 2 for a t-stat means the significance class (|t|≥2) matches even if magnitude is outside tolerance.

| Metric | Paper | Ours (Pontiff) | Ours (NW) | Tol% | Rel.dev | Status |
|---|---:|---:|---:|---:|---:|---|
| n_obs_regressions | 2155945.00 | 2182151.00 | — | 5 | 1.2% | Tier 1 |
| n_months | 396.00 | 408.00 | — | 1 | 3.0% | Tier 2 |
| pA_r1_intercept | 0.80 | 0.93 | — | 40 | 16.7% | Tier 1 |
| pA_r1_intercept_t | 3.04 | 3.49 | 3.49 | 40 | 14.7% | Tier 1 |
| pA_r1_bm | 0.39 | 0.42 | — | 40 | 7.4% | Tier 1 |
| pA_r1_bm_t | 5.86 | 5.64 | 5.64 | 40 | 3.7% | Tier 1 |
| pA_r1_bm_dum | 0.73 | 0.53 | — | 40 | 27.8% | Tier 1 |
| pA_r1_bm_dum_t | 8.86 | 6.09 | 6.09 | 40 | 31.3% | Tier 1 |
| pA_r1_avg_r2 | 0.66 | 0.73 | — | 25 | 10.4% | Tier 1 |
| pA_r2_intercept | 2.69 | 2.88 | — | 40 | 7.0% | Tier 1 |
| pA_r2_intercept_t | 3.67 | 4.04 | 4.04 | 40 | 10.0% | Tier 1 |
| pA_r2_me | -0.13 | -0.15 | — | 40 | 13.5% | Tier 1 |
| pA_r2_me_t | -2.50 | -2.95 | -2.95 | 40 | 18.2% | Tier 1 |
| pA_r2_avg_r2 | 1.23 | 1.14 | — | 25 | 7.1% | Tier 1 |
| pA_r3_intercept | 1.19 | 1.17 | — | 40 | 1.9% | Tier 1 |
| pA_r3_intercept_t | 4.56 | 4.42 | 4.42 | 40 | 3.1% | Tier 1 |
| pA_r3_mom | 0.62 | 0.52 | — | 40 | 16.2% | Tier 1 |
| pA_r3_mom_t | 1.84 | 1.53 | 1.53 | 40 | 17.0% | Tier 1 |
| pA_r3_avg_r2 | 1.23 | 1.24 | — | 25 | 0.7% | Tier 1 |
| pA_r4_intercept | 2.06 | 2.43 | — | 40 | 18.1% | Tier 1 |
| pA_r4_intercept_t | 2.97 | 3.58 | 3.58 | 40 | 20.6% | Tier 1 |
| pA_r4_bm | 0.28 | 0.28 | — | 40 | 0.9% | Tier 1 |
| pA_r4_bm_t | 4.28 | 3.93 | 3.93 | 40 | 8.1% | Tier 1 |
| pA_r4_bm_dum | 0.74 | 0.58 | — | 40 | 21.8% | Tier 1 |
| pA_r4_bm_dum_t | 9.72 | 7.12 | 7.12 | 40 | 26.7% | Tier 1 |
| pA_r4_me | -0.12 | -0.15 | — | 40 | 23.7% | Tier 1 |
| pA_r4_me_t | -2.42 | -2.95 | -2.95 | 40 | 22.0% | Tier 1 |
| pA_r4_mom | 0.55 | 0.46 | — | 40 | 16.1% | Tier 1 |
| pA_r4_mom_t | 1.77 | 1.47 | 1.47 | 40 | 16.7% | Tier 1 |
| pA_r4_avg_r2 | 2.84 | 2.89 | — | 25 | 1.8% | Tier 1 |
| pA_r5_intercept | 1.36 | 1.39 | — | 40 | 2.4% | Tier 1 |
| pA_r5_intercept_t | 4.88 | 4.95 | 4.95 | 40 | 1.4% | Tier 1 |
| pA_r5_issue | -2.23 | -2.06 | — | 40 | 7.8% | Tier 1 |
| pA_r5_issue_t | -7.08 | -7.00 | -7.00 | 40 | 1.2% | Tier 1 |
| pA_r5_avg_r2 | 0.22 | 0.20 | — | 25 | 10.4% | Tier 1 |
| pA_r6_intercept | 1.48 | 1.52 | — | 40 | 2.5% | Tier 1 |
| pA_r6_intercept_t | 5.74 | 5.86 | 5.86 | 40 | 2.1% | Tier 1 |
| pA_r6_dt_issue | -0.71 | -0.68 | — | 40 | 3.8% | Tier 1 |
| pA_r6_dt_issue_t | -4.92 | -5.21 | -5.21 | 40 | 5.8% | Tier 1 |
| pA_r6_dt_dum | -0.41 | -0.50 | — | 40 | 21.4% | Tier 1 |
| pA_r6_dt_dum_t | -3.19 | -3.76 | -3.76 | 40 | 18.0% | Tier 1 |
| pA_r6_avg_r2 | 0.53 | 0.56 | — | 25 | 5.2% | Tier 1 |
| pA_r7_intercept | 1.48 | 1.52 | — | 40 | 2.7% | Tier 1 |
| pA_r7_intercept_t | 5.75 | 5.86 | 5.86 | 40 | 2.0% | Tier 1 |
| pA_r7_issue | -1.77 | -1.51 | — | 40 | 14.6% | Tier 1 |
| pA_r7_issue_t | -6.90 | -6.37 | -6.37 | 40 | 7.6% | Tier 1 |
| pA_r7_dt_issue | -0.38 | -0.42 | — | 40 | 11.0% | Tier 1 |
| pA_r7_dt_issue_t | -3.03 | -3.63 | -3.63 | 40 | 19.9% | Tier 1 |
| pA_r7_dt_dum | -0.31 | -0.33 | — | 40 | 6.5% | Tier 1 |
| pA_r7_dt_dum_t | -2.61 | -2.74 | -2.74 | 40 | 5.1% | Tier 1 |
| pA_r7_avg_r2 | 0.63 | 0.62 | — | 25 | 1.6% | Tier 1 |
| pA_r8_intercept | 2.48 | 2.95 | — | 40 | 18.8% | Tier 1 |
| pA_r8_intercept_t | 3.68 | 4.41 | 4.41 | 40 | 20.0% | Tier 1 |
| pA_r8_bm | 0.21 | 0.21 | — | 40 | 0.5% | Tier 1 |
| pA_r8_bm_t | 3.58 | 3.16 | 3.16 | 40 | 11.6% | Tier 1 |
| pA_r8_bm_dum | 0.68 | 0.44 | — | 40 | 35.0% | Tier 1 |
| pA_r8_bm_dum_t | 9.03 | 5.11 | 5.11 | 40 | 43.4% | Tier 2 |
| pA_r8_me | -0.14 | -0.17 | — | 40 | 18.6% | Tier 1 |
| pA_r8_me_t | -2.79 | -3.26 | -3.26 | 40 | 16.9% | Tier 1 |
| pA_r8_mom | 0.47 | 0.32 | — | 40 | 31.4% | Tier 1 |
| pA_r8_mom_t | 1.57 | 1.06 | 1.06 | 40 | 32.7% | Tier 1 |
| pA_r8_issue | -1.43 | -1.23 | — | 40 | 14.0% | Tier 1 |
| pA_r8_issue_t | -6.72 | -6.12 | -6.12 | 40 | 8.9% | Tier 1 |
| pA_r8_dt_issue | -0.29 | -0.33 | — | 40 | 14.8% | Tier 1 |
| pA_r8_dt_issue_t | -2.82 | -3.43 | -3.43 | 40 | 21.5% | Tier 1 |
| pA_r8_dt_dum | -0.32 | -0.35 | — | 40 | 10.2% | Tier 1 |
| pA_r8_dt_dum_t | -3.88 | -4.42 | -4.42 | 40 | 13.9% | Tier 1 |
| pA_r8_avg_r2 | 3.15 | 3.32 | — | 25 | 5.3% | Tier 1 |
| pB_r1_intercept | 4.61 | 5.52 | — | 40 | 19.6% | Tier 1 |
| pB_r1_intercept_t | 3.10 | 3.63 | 3.51 | 40 | 17.0% | Tier 1 |
| pB_r1_bm | 2.39 | 2.63 | — | 40 | 10.2% | Tier 1 |
| pB_r1_bm_t | 6.05 | 5.38 | 6.46 | 40 | 11.1% | Tier 1 |
| pB_r1_bm_dum | 4.57 | 3.52 | — | 40 | 23.0% | Tier 1 |
| pB_r1_bm_dum_t | 5.69 | 4.71 | 6.76 | 40 | 17.2% | Tier 1 |
| pB_r1_avg_r2 | 1.18 | 1.34 | — | 25 | 14.0% | Tier 1 |
| pB_r2_intercept | 14.23 | 15.71 | — | 40 | 10.4% | Tier 1 |
| pB_r2_intercept_t | 3.56 | 3.86 | 3.67 | 40 | 8.5% | Tier 1 |
| pB_r2_me | -0.60 | -0.73 | — | 40 | 21.0% | Tier 1 |
| pB_r2_me_t | -2.33 | -2.77 | -2.69 | 40 | 18.8% | Tier 1 |
| pB_r2_avg_r2 | 1.52 | 1.50 | — | 25 | 1.4% | Tier 1 |
| pB_r3_intercept | 7.40 | 7.45 | — | 40 | 0.7% | Tier 1 |
| pB_r3_intercept_t | 5.17 | 5.16 | 4.76 | 40 | 0.2% | Tier 1 |
| pB_r3_mom | 7.30 | 6.75 | — | 40 | 7.5% | Tier 1 |
| pB_r3_mom_t | 5.53 | 4.99 | 5.88 | 40 | 9.8% | Tier 1 |
| pB_r3_avg_r2 | 1.23 | 1.21 | — | 25 | 1.8% | Tier 1 |
| pB_r4_intercept | 11.35 | 13.76 | — | 40 | 21.2% | Tier 1 |
| pB_r4_intercept_t | 2.88 | 3.45 | 3.19 | 40 | 19.8% | Tier 1 |
| pB_r4_bm | 1.69 | 1.77 | — | 40 | 5.0% | Tier 1 |
| pB_r4_bm_t | 3.79 | 3.42 | 3.84 | 40 | 9.8% | Tier 1 |
| pB_r4_bm_dum | 4.59 | 3.60 | — | 40 | 21.5% | Tier 1 |
| pB_r4_bm_dum_t | 6.43 | 6.29 | 7.10 | 40 | 2.2% | Tier 1 |
| pB_r4_me | -0.64 | -0.78 | — | 40 | 22.3% | Tier 1 |
| pB_r4_me_t | -2.31 | -2.80 | -2.60 | 40 | 21.4% | Tier 1 |
| pB_r4_mom | 6.86 | 6.37 | — | 40 | 7.2% | Tier 1 |
| pB_r4_mom_t | 5.63 | 5.07 | 5.93 | 40 | 9.9% | Tier 1 |
| pB_r4_avg_r2 | 3.73 | 3.87 | — | 25 | 3.8% | Tier 1 |
| pB_r5_intercept | 8.11 | 8.43 | — | 40 | 3.9% | Tier 1 |
| pB_r5_intercept_t | 5.42 | 5.65 | 5.27 | 40 | 4.3% | Tier 1 |
| pB_r5_issue | -13.82 | -12.88 | — | 40 | 6.8% | Tier 1 |
| pB_r5_issue_t | -7.26 | -7.68 | -8.98 | 40 | 5.7% | Tier 1 |
| pB_r5_avg_r2 | 0.43 | 0.40 | — | 25 | 6.6% | Tier 1 |

