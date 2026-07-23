# Table III — Fama–MacBeth Cross-Sectional Regressions, 1970–2003
## Panels C–E: 1-year, 2nd-year and 3rd-year holding periods (Pontiff & Woodgate 2008)

**Universe:** `univ_all` (A14).  **Regression months:** Jan 1970 – Dec 2003 (all **408** months; the paper prints 396 — see the month-count flag in `table_3.md`).  **Dependent variables:** Panel C = `r12×100` (1-year, k=12); Panel D = `r24_y2×100` (2nd-year window t+12..t+23, k=24); Panel E = `r36_y3×100` (3rd-year window t+24..t+35, k=36).  PERCENT scaling is mandatory (A3).  The year-2 and year-3 windows are EWRETD-imputed past delisting (A7); those panel columns are pre-built and verified.  All RHS variables winsorized at 1%/99% within each monthly cross-section (A5).  Cells show **coef (Pontiff t-stat)** with AR order n=k−1 (A4/A16: AR(11)/AR(23)/AR(35)); Newey-West(k−1) t-stats are listed in the appendix.  `DT_DUM_FLIP=True` — headline DT-Dum polarity: FLIPPED (dt_dum=1 ⇒ NO 5-yr history).

## Panel C — dependent variable: 1-year return (r12×100)

### Ours — coef (Pontiff t-stat)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 12.49 (4.57) | 4.84 (4.32) | 6.45 (5.02) |  |  |  |  |  | 1.58 | 2,409,708 |
| R2 | 32.53 (3.50) |  |  | -1.45 (-2.11) |  |  |  |  | 1.27 | 2,375,719 |
| R3 | 16.38 (7.19) |  |  |  | 8.61 (3.44) |  |  |  | 1.15 | 2,367,675 |
| R4 | 28.91 (3.22) | 3.34 (2.74) | 6.86 (7.45) | -1.54 (-2.30) | 7.76 (3.41) |  |  |  | 3.79 | 2,348,275 |
| R5 | 17.87 (7.56) |  |  |  |  | -25.68 (-8.07) |  |  | 0.45 | 2,203,273 |
| R6 | 19.15 (9.39) |  |  |  |  |  | -8.11 (-5.60) | -4.91 (-2.45) | 1.33 | 2,409,708 |
| R7 | 19.16 (9.36) |  |  |  |  | -19.16 (-5.89) | -5.05 (-3.24) | -3.27 (-1.46) | 1.44 | 2,203,273 |
| R8 | 33.39 (3.90) | 2.56 (2.53) | 5.69 (5.52) | -1.69 (-2.69) | 6.88 (3.10) | -15.40 (-8.13) | -3.62 (-3.17) | -2.87 (-2.22) | 4.49 | 2,182,151 |

### Paper targets (content.md)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 10.36 (3.84) | 4.56 (5.41) | 8.39 (7.54) |  |  |  |  |  | 1.37 | — |
| R2 | 28.88 (3.21) |  |  | -1.15 (-1.76) |  |  |  |  | 1.28 | — |
| R3 | 15.92 (7.17) |  |  |  | 9.62 (3.61) |  |  |  | 1.17 | — |
| R4 | 23.30 (2.71) | 3.33 (3.65) | 8.58 (9.48) | -1.20 (-1.93) | 8.66 (3.58) |  |  |  | 3.59 | — |
| R5 | 16.95 (7.32) |  |  |  |  | -27.32 (-7.51) |  |  | 0.49 | — |
| R6 | 18.17 (8.95) |  |  |  |  |  | -8.38 (-5.94) | -4.68 (-2.32) | 1.22 | — |
| R7 | 18.20 (8.94) |  |  |  |  | -20.71 (-5.08) | -4.81 (-2.87) | -3.60 (-1.74) | 1.43 | — |
| R8 | 27.25 (3.38) | 2.59 (3.33) | 7.96 (8.54) | -1.37 (-2.32) | 8.02 (3.50) | -16.52 (-5.61) | -3.41 (-2.60) | -3.24 (-2.63) | 4.27 | — |

_Panel C: holding period k=12 → Pontiff AR order n=11, Newey-West lags=11. Months fitted: 408; R8 firm-months 2,182,151._

## Panel D — dependent variable: 2nd-year return (r24_y2×100)

### Ours — coef (Pontiff t-stat)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 13.82 (3.49) | 3.86 (4.49) | 4.69 (3.07) |  |  |  |  |  | 1.29 | 2,409,708 |
| R2 | 29.69 (2.85) |  |  | -1.19 (-1.66) |  |  |  |  | 1.21 | 2,375,719 |
| R3 | 17.03 (5.46) |  |  |  | -4.11 (-1.78) |  |  |  | 0.44 | 2,367,675 |
| R4 | 24.76 (2.39) | 2.89 (2.57) | 5.67 (5.36) | -1.07 (-1.47) | -4.86 (-2.44) |  |  |  | 2.93 | 2,348,275 |
| R5 | 17.73 (5.67) |  |  |  |  | -18.88 (-4.68) |  |  | 0.29 | 2,203,273 |
| R6 | 18.44 (6.53) |  |  |  |  |  | -5.87 (-3.93) | -3.51 (-1.64) | 1.04 | 2,409,708 |
| R7 | 18.46 (6.53) |  |  |  |  | -13.39 (-3.10) | -3.87 (-2.36) | -2.67 (-1.10) | 1.11 | 2,203,273 |
| R8 | 27.05 (2.74) | 2.31 (2.61) | 5.10 (4.40) | -1.12 (-1.69) | -5.14 (-2.54) | -11.32 (-4.00) | -3.02 (-2.68) | -2.49 (-1.79) | 3.53 | 2,182,151 |

### Paper targets (content.md)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 12.98 (5.52) | 3.38 (4.33) | 5.75 (5.50) |  |  |  |  |  | 1.02 | — |
| R2 | 30.14 (4.14) |  |  | -1.13 (-2.25) |  |  |  |  | 1.45 | — |
| R3 | 17.55 (8.69) |  |  |  | -2.78 (-1.35) |  |  |  | 0.46 | — |
| R4 | 23.26 (3.27) | 2.38 (3.28) | 6.46 (6.94) | -0.93 (-1.87) | -3.69 (-1.97) |  |  |  | 2.71 | — |
| R5 | 17.93 (8.70) |  |  |  |  | -20.03 (-6.20) |  |  | 0.31 | — |
| R6 | 18.13 (8.96) |  |  |  |  |  | -5.40 (-3.25) | -1.82 (-0.44) | 0.51 | — |
| R7 | 18.19 (8.98) |  |  |  |  | -13.69 (-4.00) | -3.55 (-1.97) | -1.70 (-0.41) | 0.60 | — |
| R8 | 23.81 (3.40) | 2.10 (3.02) | 6.32 (6.86) | -0.92 (-1.84) | -3.94 (-2.19) | -11.63 (-3.88) | -2.68 (-1.86) | -0.80 (-0.20) | 3.14 | — |

_Panel D: holding period k=24 → Pontiff AR order n=23, Newey-West lags=23. Months fitted: 408; R8 firm-months 2,182,151._

## Panel E — dependent variable: 3rd-year return (r36_y3×100)

### Ours — coef (Pontiff t-stat)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 15.33 (4.15) | 2.98 (2.24) | 2.95 (3.11) |  |  |  |  |  | 1.12 | 2,409,708 |
| R2 | 25.08 (2.51) |  |  | -0.75 (-1.13) |  |  |  |  | 1.07 | 2,375,719 |
| R3 | 17.39 (5.99) |  |  |  | -3.57 (-2.31) |  |  |  | 0.69 | 2,367,675 |
| R4 | 21.77 (2.12) | 2.18 (1.72) | 3.74 (6.92) | -0.67 (-0.94) | -3.99 (-3.67) |  |  |  | 2.68 | 2,348,275 |
| R5 | 17.74 (5.79) |  |  |  |  | -14.78 (-3.03) |  |  | 0.21 | 2,203,273 |
| R6 | 18.03 (6.62) |  |  |  |  |  | -4.36 (-1.92) | -2.59 (-0.90) | 0.86 | 2,409,708 |
| R7 | 18.05 (6.63) |  |  |  |  | -10.94 (-2.90) | -2.60 (-1.31) | -2.21 (-0.86) | 0.82 | 2,203,273 |
| R8 | 23.22 (2.39) | 1.81 (1.67) | 3.84 (4.90) | -0.74 (-1.14) | -3.69 (-3.81) | -9.42 (-4.18) | -1.74 (-1.69) | -1.88 (-1.64) | 3.04 | 2,182,151 |

### Paper targets (content.md)

| Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 13.55 (6.08) | 3.17 (3.87) | 5.35 (6.48) |  |  |  |  |  | 0.92 | — |
| R2 | 27.81 (4.03) |  |  | -0.91 (-1.87) |  |  |  |  | 1.37 | — |
| R3 | 17.77 (9.26) |  |  |  | -1.72 (-0.54) |  |  |  | 0.79 | — |
| R4 | 21.67 (3.19) | 2.07 (2.80) | 5.90 (8.66) | -0.75 (-1.55) | -2.24 (-0.83) |  |  |  | 2.78 | — |
| R5 | 17.97 (9.14) |  |  |  |  | -14.18 (-3.17) |  |  | 0.25 | — |
| R6 | 18.12 (9.44) |  |  |  |  |  | -4.38 (-2.27) | 1.98 (0.70) | 0.44 | — |
| R7 | 18.13 (9.43) |  |  |  |  | -9.52 (-2.34) | -2.96 (-1.50) | 2.21 (0.75) | 0.50 | — |
| R8 | 21.90 (3.25) | 1.85 (2.63) | 5.79 (8.77) | -0.73 (-1.50) | -2.42 (-0.94) | -9.00 (-2.97) | -2.14 (-1.27) | 3.12 (1.02) | 3.10 | — |

_Panel E: holding period k=36 → Pontiff AR order n=35, Newey-West lags=35. Months fitted: 408; R8 firm-months 2,182,151._

---

## Newey-West(k−1) t-statistics (reference; primary = Pontiff above)

| Panel | Row | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C | R1 | 4.01 | 5.36 | 5.56 |  |  |  |  |  |
| C | R2 | 3.60 |  |  | -2.48 |  |  |  |  |
| C | R3 | 5.50 |  |  |  | 3.71 |  |  |  |
| C | R4 | 3.29 | 3.42 | 6.37 | -2.50 | 3.62 |  |  |  |
| C | R5 | 5.80 |  |  |  |  | -8.90 |  |  |
| C | R6 | 6.94 |  |  |  |  |  | -6.11 | -2.73 |
| C | R7 | 6.93 |  |  |  |  | -7.35 | -3.97 | -1.83 |
| C | R8 | 4.07 | 2.98 | 4.64 | -2.85 | 3.33 | -8.90 | -3.48 | -2.52 |
| D | R1 | 4.11 | 3.86 | 3.73 |  |  |  |  |  |
| D | R2 | 3.35 |  |  | -2.06 |  |  |  |  |
| D | R3 | 5.63 |  |  |  | -2.45 |  |  |  |
| D | R4 | 2.77 | 2.64 | 5.41 | -1.75 | -3.32 |  |  |  |
| D | R5 | 5.76 |  |  |  |  | -6.09 |  |  |
| D | R6 | 6.74 |  |  |  |  |  | -4.04 | -1.91 |
| D | R7 | 6.75 |  |  |  |  | -5.05 | -2.72 | -1.43 |
| D | R8 | 3.32 | 2.40 | 4.41 | -1.99 | -3.50 | -6.20 | -2.58 | -2.19 |
| E | R1 | 4.52 | 2.87 | 2.95 |  |  |  |  |  |
| E | R2 | 2.97 |  |  | -1.38 |  |  |  |  |
| E | R3 | 6.03 |  |  |  | -1.71 |  |  |  |
| E | R4 | 2.60 | 2.07 | 5.67 | -1.20 | -2.43 |  |  |  |
| E | R5 | 5.94 |  |  |  |  | -4.31 |  |  |
| E | R6 | 6.84 |  |  |  |  |  | -2.49 | -1.38 |
| E | R7 | 6.84 |  |  |  |  | -4.31 | -1.65 | -1.30 |
| E | R8 | 3.01 | 1.89 | 4.59 | -1.43 | -2.45 | -5.01 | -1.50 | -2.02 |

---

## Paper's horizon-stability claims — verification (our estimates)

Paper claims (content.md L31: "Our results remain strong for holding periods ranging from one month to 3 years"; L2128 horse-race and DT-ISSUE statements):

- **(i) ISSUE slope negative at all three horizons (R5; also R7/R8)**
  - Verdict: ✅ PASS
  - Evidence: C-R5 ISSUE=-25.68 (t=-8.07); D-R5 ISSUE=-18.88 (t=-4.68); E-R5 ISSUE=-14.78 (t=-3.03)
- **(ii) |t_ISSUE| > |t_BM|, |t_ME|, |t_MOM| in the univariate comparison at each horizon (horse race)**
  - Verdict: ✅ PASS (our t-stats at all three horizons). NOTE: the paper's OWN printed 3-year t-stats violate this claim (ISSUE |t|=3.17 < BM |t|=3.87, Panel E) — our estimates satisfy it.
  - Evidence: C: |t_ISSUE|=8.07 vs BM=4.32, ME=2.11, MOM=3.44 (wins all); D: |t_ISSUE|=4.68 vs BM=4.49, ME=1.66, MOM=1.78 (wins all); E: |t_ISSUE|=3.03 vs BM=2.24, ME=1.13, MOM=2.31 (wins all)
- **(iii) DT-ISSUE significant (|t|>=2) in the 1-year FULL (R8) but insignificant in the 2- and 3-year FULL (R8) specs**
  - Verdict: ⚠️ PARTIAL
  - Evidence: 1-yr R8 DT-ISSUE t=-3.17 (sig; paper -2.60); 2-yr R8 t=-2.68 (sig; paper -1.86); 3-yr R8 t=-1.69 (insig; paper -1.27) — at the 2-year horizon OUR DT-ISSUE is borderline-significant (|t|=2.68>=2) where the paper prints insignificant (-1.86); both are near |t|=2 (overlap-t-stat sensitivity).

> **DT-Dum polarity note (Panel E).** Under the ratified `DT_DUM_FLIP=True` headline the Panel E DT-Dum *coefficient* comes out NEGATIVE, whereas the paper prints POSITIVE (R6 +1.98, R7 +2.21, R8 +3.12). This is the mirror image of the A15 finding: Panels A–D require the flipped (no-history) sign to reconcile the paper's negative DT-Dum slopes, but Panel E's printed DT-Dum sign matches the as-built polarity. It is a paper-side DT-Dum polarity inconsistency at the 3-year horizon and is the ONLY sign deviation here (the 3 FAIL cells below). It does not touch any ratified convention and leaves the polarity-invariant ISSUE / DT-ISSUE coefficients and all other cells unaffected.

---

## Appendix — per-cell evaluation vs tables_to_replicate.json (T3cde)

**Tally:** Tier 1 = 166 · Tier 2 = 29 · FAIL = 3 · SKIP = 0

Coefficients/intercepts/R² compare our value to the paper (±40% coef/t, ±25% R²). For t-stat metrics the **primary (Pontiff)** t is compared; the NW t is shown for reference. Tier 2 for a t-stat means the significance class (|t|≥2) or the sign matches even if magnitude is outside tolerance.

| Metric | Paper | Ours (Pontiff) | Ours (NW) | Tol% | Rel.dev | Status |
|---|---:|---:|---:|---:|---:|---|
| pC_r1_intercept | 10.36 | 12.49 | — | 40 | 20.6% | Tier 1 |
| pC_r1_intercept_t | 3.84 | 4.57 | 4.01 | 40 | 19.0% | Tier 1 |
| pC_r1_bm | 4.56 | 4.84 | — | 40 | 6.2% | Tier 1 |
| pC_r1_bm_t | 5.41 | 4.32 | 5.36 | 40 | 20.1% | Tier 1 |
| pC_r1_bm_dum | 8.39 | 6.45 | — | 40 | 23.1% | Tier 1 |
| pC_r1_bm_dum_t | 7.54 | 5.02 | 5.56 | 40 | 33.4% | Tier 1 |
| pC_r1_avg_r2 | 1.37 | 1.58 | — | 25 | 15.6% | Tier 1 |
| pC_r2_intercept | 28.88 | 32.53 | — | 40 | 12.6% | Tier 1 |
| pC_r2_intercept_t | 3.21 | 3.50 | 3.60 | 40 | 9.1% | Tier 1 |
| pC_r2_me | -1.15 | -1.45 | — | 40 | 26.2% | Tier 1 |
| pC_r2_me_t | -1.76 | -2.11 | -2.48 | 40 | 20.2% | Tier 1 |
| pC_r2_avg_r2 | 1.28 | 1.27 | — | 25 | 0.8% | Tier 1 |
| pC_r3_intercept | 15.92 | 16.38 | — | 40 | 2.9% | Tier 1 |
| pC_r3_intercept_t | 7.17 | 7.19 | 5.50 | 40 | 0.3% | Tier 1 |
| pC_r3_mom | 9.62 | 8.61 | — | 40 | 10.5% | Tier 1 |
| pC_r3_mom_t | 3.61 | 3.44 | 3.71 | 40 | 4.7% | Tier 1 |
| pC_r3_avg_r2 | 1.17 | 1.15 | — | 25 | 1.6% | Tier 1 |
| pC_r4_intercept | 23.30 | 28.91 | — | 40 | 24.1% | Tier 1 |
| pC_r4_intercept_t | 2.71 | 3.22 | 3.29 | 40 | 18.7% | Tier 1 |
| pC_r4_bm | 3.33 | 3.34 | — | 40 | 0.2% | Tier 1 |
| pC_r4_bm_t | 3.65 | 2.74 | 3.42 | 40 | 24.8% | Tier 1 |
| pC_r4_bm_dum | 8.58 | 6.86 | — | 40 | 20.1% | Tier 1 |
| pC_r4_bm_dum_t | 9.48 | 7.45 | 6.37 | 40 | 21.4% | Tier 1 |
| pC_r4_me | -1.20 | -1.54 | — | 40 | 28.0% | Tier 1 |
| pC_r4_me_t | -1.93 | -2.30 | -2.50 | 40 | 19.1% | Tier 1 |
| pC_r4_mom | 8.66 | 7.76 | — | 40 | 10.4% | Tier 1 |
| pC_r4_mom_t | 3.58 | 3.41 | 3.62 | 40 | 4.6% | Tier 1 |
| pC_r4_avg_r2 | 3.59 | 3.79 | — | 25 | 5.4% | Tier 1 |
| pC_r5_intercept | 16.95 | 17.87 | — | 40 | 5.4% | Tier 1 |
| pC_r5_intercept_t | 7.32 | 7.56 | 5.80 | 40 | 3.3% | Tier 1 |
| pC_r5_issue | -27.32 | -25.68 | — | 40 | 6.0% | Tier 1 |
| pC_r5_issue_t | -7.51 | -8.07 | -8.90 | 40 | 7.4% | Tier 1 |
| pC_r5_avg_r2 | 0.49 | 0.45 | — | 25 | 9.0% | Tier 1 |
| pC_r6_intercept | 18.17 | 19.15 | — | 40 | 5.4% | Tier 1 |
| pC_r6_intercept_t | 8.95 | 9.39 | 6.94 | 40 | 4.9% | Tier 1 |
| pC_r6_dt_issue | -8.38 | -8.11 | — | 40 | 3.3% | Tier 1 |
| pC_r6_dt_issue_t | -5.94 | -5.60 | -6.11 | 40 | 5.8% | Tier 1 |
| pC_r6_dt_dum | -4.68 | -4.91 | — | 40 | 4.9% | Tier 1 |
| pC_r6_dt_dum_t | -2.32 | -2.45 | -2.73 | 40 | 5.5% | Tier 1 |
| pC_r6_avg_r2 | 1.22 | 1.33 | — | 25 | 9.2% | Tier 1 |
| pC_r7_intercept | 18.20 | 19.16 | — | 40 | 5.3% | Tier 1 |
| pC_r7_intercept_t | 8.94 | 9.36 | 6.93 | 40 | 4.7% | Tier 1 |
| pC_r7_issue | -20.71 | -19.16 | — | 40 | 7.5% | Tier 1 |
| pC_r7_issue_t | -5.08 | -5.89 | -7.35 | 40 | 16.0% | Tier 1 |
| pC_r7_dt_issue | -4.81 | -5.05 | — | 40 | 5.0% | Tier 1 |
| pC_r7_dt_issue_t | -2.87 | -3.24 | -3.97 | 40 | 12.8% | Tier 1 |
| pC_r7_dt_dum | -3.60 | -3.27 | — | 40 | 9.1% | Tier 1 |
| pC_r7_dt_dum_t | -1.74 | -1.46 | -1.83 | 40 | 15.9% | Tier 1 |
| pC_r7_avg_r2 | 1.43 | 1.44 | — | 25 | 0.8% | Tier 1 |
| pC_r8_intercept | 27.25 | 33.39 | — | 40 | 22.5% | Tier 1 |
| pC_r8_intercept_t | 3.38 | 3.90 | 4.07 | 40 | 15.5% | Tier 1 |
| pC_r8_bm | 2.59 | 2.56 | — | 40 | 1.0% | Tier 1 |
| pC_r8_bm_t | 3.33 | 2.53 | 2.98 | 40 | 24.1% | Tier 1 |
| pC_r8_bm_dum | 7.96 | 5.69 | — | 40 | 28.6% | Tier 1 |
| pC_r8_bm_dum_t | 8.54 | 5.52 | 4.64 | 40 | 35.3% | Tier 1 |
| pC_r8_me | -1.37 | -1.69 | — | 40 | 23.2% | Tier 1 |
| pC_r8_me_t | -2.32 | -2.69 | -2.85 | 40 | 16.0% | Tier 1 |
| pC_r8_mom | 8.02 | 6.88 | — | 40 | 14.2% | Tier 1 |
| pC_r8_mom_t | 3.50 | 3.10 | 3.33 | 40 | 11.4% | Tier 1 |
| pC_r8_issue | -16.52 | -15.40 | — | 40 | 6.8% | Tier 1 |
| pC_r8_issue_t | -5.61 | -8.13 | -8.90 | 40 | 44.9% | Tier 2 |
| pC_r8_dt_issue | -3.41 | -3.62 | — | 40 | 6.1% | Tier 1 |
| pC_r8_dt_issue_t | -2.60 | -3.17 | -3.48 | 40 | 22.0% | Tier 1 |
| pC_r8_dt_dum | -3.24 | -2.87 | — | 40 | 11.4% | Tier 1 |
| pC_r8_dt_dum_t | -2.63 | -2.22 | -2.52 | 40 | 15.4% | Tier 1 |
| pC_r8_avg_r2 | 4.27 | 4.49 | — | 25 | 5.2% | Tier 1 |
| pD_r1_intercept | 12.98 | 13.82 | — | 40 | 6.5% | Tier 1 |
| pD_r1_intercept_t | 5.52 | 3.49 | 4.11 | 40 | 36.8% | Tier 1 |
| pD_r1_bm | 3.38 | 3.86 | — | 40 | 14.1% | Tier 1 |
| pD_r1_bm_t | 4.33 | 4.49 | 3.86 | 40 | 3.7% | Tier 1 |
| pD_r1_bm_dum | 5.75 | 4.69 | — | 40 | 18.4% | Tier 1 |
| pD_r1_bm_dum_t | 5.50 | 3.07 | 3.73 | 40 | 44.2% | Tier 2 |
| pD_r1_avg_r2 | 1.02 | 1.29 | — | 25 | 26.0% | Tier 2 |
| pD_r2_intercept | 30.14 | 29.69 | — | 40 | 1.5% | Tier 1 |
| pD_r2_intercept_t | 4.14 | 2.85 | 3.35 | 40 | 31.1% | Tier 1 |
| pD_r2_me | -1.13 | -1.19 | — | 40 | 5.3% | Tier 1 |
| pD_r2_me_t | -2.25 | -1.66 | -2.06 | 40 | 26.3% | Tier 1 |
| pD_r2_avg_r2 | 1.45 | 1.21 | — | 25 | 16.5% | Tier 1 |
| pD_r3_intercept | 17.55 | 17.03 | — | 40 | 3.0% | Tier 1 |
| pD_r3_intercept_t | 8.69 | 5.46 | 5.63 | 40 | 37.1% | Tier 1 |
| pD_r3_mom | -2.78 | -4.11 | — | 40 | 47.9% | Tier 2 |
| pD_r3_mom_t | -1.35 | -1.78 | -2.45 | 40 | 31.9% | Tier 1 |
| pD_r3_avg_r2 | 0.46 | 0.44 | — | 25 | 3.5% | Tier 1 |
| pD_r4_intercept | 23.26 | 24.76 | — | 40 | 6.5% | Tier 1 |
| pD_r4_intercept_t | 3.27 | 2.39 | 2.77 | 40 | 27.0% | Tier 1 |
| pD_r4_bm | 2.38 | 2.89 | — | 40 | 21.3% | Tier 1 |
| pD_r4_bm_t | 3.28 | 2.57 | 2.64 | 40 | 21.6% | Tier 1 |
| pD_r4_bm_dum | 6.46 | 5.67 | — | 40 | 12.2% | Tier 1 |
| pD_r4_bm_dum_t | 6.94 | 5.36 | 5.41 | 40 | 22.8% | Tier 1 |
| pD_r4_me | -0.93 | -1.07 | — | 40 | 14.7% | Tier 1 |
| pD_r4_me_t | -1.87 | -1.47 | -1.75 | 40 | 21.2% | Tier 1 |
| pD_r4_mom | -3.69 | -4.86 | — | 40 | 31.7% | Tier 1 |
| pD_r4_mom_t | -1.97 | -2.44 | -3.32 | 40 | 23.9% | Tier 1 |
| pD_r4_avg_r2 | 2.71 | 2.93 | — | 25 | 8.3% | Tier 1 |
| pD_r5_intercept | 17.93 | 17.73 | — | 40 | 1.1% | Tier 1 |
| pD_r5_intercept_t | 8.70 | 5.67 | 5.76 | 40 | 34.8% | Tier 1 |
| pD_r5_issue | -20.03 | -18.88 | — | 40 | 5.8% | Tier 1 |
| pD_r5_issue_t | -6.20 | -4.68 | -6.09 | 40 | 24.4% | Tier 1 |
| pD_r5_avg_r2 | 0.31 | 0.29 | — | 25 | 6.1% | Tier 1 |
| pD_r6_intercept | 18.13 | 18.44 | — | 40 | 1.7% | Tier 1 |
| pD_r6_intercept_t | 8.96 | 6.53 | 6.74 | 40 | 27.1% | Tier 1 |
| pD_r6_dt_issue | -5.40 | -5.87 | — | 40 | 8.6% | Tier 1 |
| pD_r6_dt_issue_t | -3.25 | -3.93 | -4.04 | 40 | 20.9% | Tier 1 |
| pD_r6_dt_dum | -1.82 | -3.51 | — | 40 | 93.0% | Tier 2 |
| pD_r6_dt_dum_t | -0.44 | -1.64 | -1.91 | 40 | 273.7% | Tier 2 |
| pD_r6_avg_r2 | 0.51 | 1.04 | — | 25 | 103.0% | Tier 2 |
| pD_r7_intercept | 18.19 | 18.46 | — | 40 | 1.5% | Tier 1 |
| pD_r7_intercept_t | 8.98 | 6.53 | 6.75 | 40 | 27.2% | Tier 1 |
| pD_r7_issue | -13.69 | -13.39 | — | 40 | 2.2% | Tier 1 |
| pD_r7_issue_t | -4.00 | -3.10 | -5.05 | 40 | 22.5% | Tier 1 |
| pD_r7_dt_issue | -3.55 | -3.87 | — | 40 | 8.9% | Tier 1 |
| pD_r7_dt_issue_t | -1.97 | -2.36 | -2.72 | 40 | 19.9% | Tier 1 |
| pD_r7_dt_dum | -1.70 | -2.67 | — | 40 | 57.1% | Tier 2 |
| pD_r7_dt_dum_t | -0.41 | -1.10 | -1.43 | 40 | 169.2% | Tier 2 |
| pD_r7_avg_r2 | 0.60 | 1.11 | — | 25 | 84.5% | Tier 2 |
| pD_r8_intercept | 23.81 | 27.05 | — | 40 | 13.6% | Tier 1 |
| pD_r8_intercept_t | 3.40 | 2.74 | 3.32 | 40 | 19.3% | Tier 1 |
| pD_r8_bm | 2.10 | 2.31 | — | 40 | 10.0% | Tier 1 |
| pD_r8_bm_t | 3.02 | 2.61 | 2.40 | 40 | 13.5% | Tier 1 |
| pD_r8_bm_dum | 6.32 | 5.10 | — | 40 | 19.3% | Tier 1 |
| pD_r8_bm_dum_t | 6.86 | 4.40 | 4.41 | 40 | 35.8% | Tier 1 |
| pD_r8_me | -0.92 | -1.12 | — | 40 | 21.8% | Tier 1 |
| pD_r8_me_t | -1.84 | -1.69 | -1.99 | 40 | 8.0% | Tier 1 |
| pD_r8_mom | -3.94 | -5.14 | — | 40 | 30.5% | Tier 1 |
| pD_r8_mom_t | -2.19 | -2.54 | -3.50 | 40 | 16.2% | Tier 1 |
| pD_r8_issue | -11.63 | -11.32 | — | 40 | 2.6% | Tier 1 |
| pD_r8_issue_t | -3.88 | -4.00 | -6.20 | 40 | 3.0% | Tier 1 |
| pD_r8_dt_issue | -2.68 | -3.02 | — | 40 | 12.6% | Tier 1 |
| pD_r8_dt_issue_t | -1.86 | -2.68 | -2.58 | 40 | 44.1% | Tier 2 |
| pD_r8_dt_dum | -0.80 | -2.49 | — | 40 | 210.8% | Tier 2 |
| pD_r8_dt_dum_t | -0.20 | -1.79 | -2.19 | 40 | 795.5% | Tier 2 |
| pD_r8_avg_r2 | 3.14 | 3.53 | — | 25 | 12.5% | Tier 1 |
| pE_r1_intercept | 13.55 | 15.33 | — | 40 | 13.2% | Tier 1 |
| pE_r1_intercept_t | 6.08 | 4.15 | 4.52 | 40 | 31.8% | Tier 1 |
| pE_r1_bm | 3.17 | 2.98 | — | 40 | 5.9% | Tier 1 |
| pE_r1_bm_t | 3.87 | 2.24 | 2.87 | 40 | 42.1% | Tier 2 |
| pE_r1_bm_dum | 5.35 | 2.95 | — | 40 | 44.9% | Tier 2 |
| pE_r1_bm_dum_t | 6.48 | 3.11 | 2.95 | 40 | 52.0% | Tier 2 |
| pE_r1_avg_r2 | 0.92 | 1.12 | — | 25 | 21.3% | Tier 1 |
| pE_r2_intercept | 27.81 | 25.08 | — | 40 | 9.8% | Tier 1 |
| pE_r2_intercept_t | 4.03 | 2.51 | 2.97 | 40 | 37.7% | Tier 1 |
| pE_r2_me | -0.91 | -0.75 | — | 40 | 17.2% | Tier 1 |
| pE_r2_me_t | -1.87 | -1.13 | -1.38 | 40 | 39.4% | Tier 1 |
| pE_r2_avg_r2 | 1.37 | 1.07 | — | 25 | 22.2% | Tier 1 |
| pE_r3_intercept | 17.77 | 17.39 | — | 40 | 2.1% | Tier 1 |
| pE_r3_intercept_t | 9.26 | 5.99 | 6.03 | 40 | 35.3% | Tier 1 |
| pE_r3_mom | -1.72 | -3.57 | — | 40 | 107.6% | Tier 2 |
| pE_r3_mom_t | -0.54 | -2.31 | -1.71 | 40 | 328.6% | Tier 2 |
| pE_r3_avg_r2 | 0.79 | 0.69 | — | 25 | 12.8% | Tier 1 |
| pE_r4_intercept | 21.67 | 21.77 | — | 40 | 0.5% | Tier 1 |
| pE_r4_intercept_t | 3.19 | 2.12 | 2.60 | 40 | 33.6% | Tier 1 |
| pE_r4_bm | 2.07 | 2.18 | — | 40 | 5.2% | Tier 1 |
| pE_r4_bm_t | 2.80 | 1.72 | 2.07 | 40 | 38.7% | Tier 1 |
| pE_r4_bm_dum | 5.90 | 3.74 | — | 40 | 36.5% | Tier 1 |
| pE_r4_bm_dum_t | 8.66 | 6.92 | 5.67 | 40 | 20.0% | Tier 1 |
| pE_r4_me | -0.75 | -0.67 | — | 40 | 11.2% | Tier 1 |
| pE_r4_me_t | -1.55 | -0.94 | -1.20 | 40 | 39.5% | Tier 1 |
| pE_r4_mom | -2.24 | -3.99 | — | 40 | 78.2% | Tier 2 |
| pE_r4_mom_t | -0.83 | -3.67 | -2.43 | 40 | 341.8% | Tier 2 |
| pE_r4_avg_r2 | 2.78 | 2.68 | — | 25 | 3.6% | Tier 1 |
| pE_r5_intercept | 17.97 | 17.74 | — | 40 | 1.3% | Tier 1 |
| pE_r5_intercept_t | 9.14 | 5.79 | 5.94 | 40 | 36.6% | Tier 1 |
| pE_r5_issue | -14.18 | -14.78 | — | 40 | 4.2% | Tier 1 |
| pE_r5_issue_t | -3.17 | -3.03 | -4.31 | 40 | 4.3% | Tier 1 |
| pE_r5_avg_r2 | 0.25 | 0.21 | — | 25 | 16.0% | Tier 1 |
| pE_r6_intercept | 18.12 | 18.03 | — | 40 | 0.5% | Tier 1 |
| pE_r6_intercept_t | 9.44 | 6.62 | 6.84 | 40 | 29.8% | Tier 1 |
| pE_r6_dt_issue | -4.38 | -4.36 | — | 40 | 0.4% | Tier 1 |
| pE_r6_dt_issue_t | -2.27 | -1.92 | -2.49 | 40 | 15.3% | Tier 1 |
| pE_r6_dt_dum | 1.98 | -2.59 | — | 40 | 230.9% | FAIL |
| pE_r6_dt_dum_t | 0.70 | -0.90 | -1.38 | 40 | 228.6% | Tier 2 |
| pE_r6_avg_r2 | 0.44 | 0.86 | — | 25 | 96.4% | Tier 2 |
| pE_r7_intercept | 18.13 | 18.05 | — | 40 | 0.5% | Tier 1 |
| pE_r7_intercept_t | 9.43 | 6.63 | 6.84 | 40 | 29.7% | Tier 1 |
| pE_r7_issue | -9.52 | -10.94 | — | 40 | 14.9% | Tier 1 |
| pE_r7_issue_t | -2.34 | -2.90 | -4.31 | 40 | 23.8% | Tier 1 |
| pE_r7_dt_issue | -2.96 | -2.60 | — | 40 | 12.3% | Tier 1 |
| pE_r7_dt_issue_t | -1.50 | -1.31 | -1.65 | 40 | 12.5% | Tier 1 |
| pE_r7_dt_dum | 2.21 | -2.21 | — | 40 | 200.2% | FAIL |
| pE_r7_dt_dum_t | 0.75 | -0.86 | -1.30 | 40 | 214.9% | Tier 2 |
| pE_r7_avg_r2 | 0.50 | 0.82 | — | 25 | 64.2% | Tier 2 |
| pE_r8_intercept | 21.90 | 23.22 | — | 40 | 6.0% | Tier 1 |
| pE_r8_intercept_t | 3.25 | 2.39 | 3.01 | 40 | 26.5% | Tier 1 |
| pE_r8_bm | 1.85 | 1.81 | — | 40 | 2.1% | Tier 1 |
| pE_r8_bm_t | 2.63 | 1.67 | 1.89 | 40 | 36.4% | Tier 1 |
| pE_r8_bm_dum | 5.79 | 3.84 | — | 40 | 33.6% | Tier 1 |
| pE_r8_bm_dum_t | 8.77 | 4.90 | 4.59 | 40 | 44.2% | Tier 2 |
| pE_r8_me | -0.73 | -0.74 | — | 40 | 1.5% | Tier 1 |
| pE_r8_me_t | -1.50 | -1.14 | -1.43 | 40 | 24.2% | Tier 1 |
| pE_r8_mom | -2.42 | -3.69 | — | 40 | 52.7% | Tier 2 |
| pE_r8_mom_t | -0.94 | -3.81 | -2.45 | 40 | 305.6% | Tier 2 |
| pE_r8_issue | -9.00 | -9.42 | — | 40 | 4.7% | Tier 1 |
| pE_r8_issue_t | -2.97 | -4.18 | -5.01 | 40 | 40.8% | Tier 2 |
| pE_r8_dt_issue | -2.14 | -1.74 | — | 40 | 18.5% | Tier 1 |
| pE_r8_dt_issue_t | -1.27 | -1.69 | -1.50 | 40 | 33.3% | Tier 1 |
| pE_r8_dt_dum | 3.12 | -1.88 | — | 40 | 160.2% | FAIL |
| pE_r8_dt_dum_t | 1.02 | -1.64 | -2.02 | 40 | 260.4% | Tier 2 |
| pE_r8_avg_r2 | 3.10 | 3.04 | — | 25 | 1.8% | Tier 1 |

