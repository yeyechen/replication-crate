# Table VI — Out-of-Sample Fama–MacBeth, Panel A (1-month), Sep 1932 – Dec 1969
## (Pontiff & Woodgate 2008)

**Universe:** `univ_all` (A14).  **Regression months:** Sep 1932 – Dec 1969 (448 calendar months support valid cross-sections; the paper prints 444).  **Dependent variable:** `ret×100` (1-month), percent scaling mandatory (A3).  All RHS winsorized 1%/99% per monthly cross-section (A5).  T-stats are **plain FM** (holding period k=1 ⇒ Pontiff AR order n=0, A4/A16).  `DT_DUM_FLIP=True` (headline DT-Dum = 1 for NO 5-yr history).

> 🚫 **BM omitted — DFF book equity unavailable (A8).** The paper's OOS BM uses the Davis-Fama-French (2000) book-equity file (L2445), absent from ClickHouse. Per the Replicator's decision the eight horse-race specs are estimated WITHOUT bm/bm_dum:
>
> - **PRIMARY rows (R2, R3, R5, R6, R7)** are BM-free in the paper too ⇒ fully comparable; these drive the Tier tally.
> - **SECONDARY rows (R1, R4, R8)** are BM-inclusive in the paper. Our BM-free versions are labeled **pattern-only**: their ME/MOM/ISSUE/DT coefficients are shown for pattern comparison but are NOT directly comparable to the paper's BM-inclusive rows and are excluded from the Tier tally. R1 (= const + BM + BM Dum) reduces to a constant-only row and is not comparable (SKIP).

> ⚠️ **Degenerate-cross-section guard (A17 extension).** Pre-1950 share issuance is near-universally zero; in some months the 1%/99% winsorization collapses the ISSUE cross-sectional spread to ~0 and the FM slope divides by ~0 (one month reaches −11648), wrecking the time-series average (unguarded R5 ISSUE = −29). ISSUE-containing months with winsorized ISSUE std < 0.01 are dropped (a numerical safeguard, NOT a sample/universe change): R5/R7/R8 fit 438 months (10 dropped) vs 448 for the non-ISSUE rows.

> ⚠️ **OOS sample size.** Paper: 373,590 firm-obs over 444 months. Our CRSP-only cross-section is LARGER (R8 ≈ 464,718); the paper's count reflects DFF book-equity availability (its single consistent sample requires BM even for the BM-free rows). Documented, not forced.

## Panel A — dependent variable: 1-month return (ret×100)

| Row | Class | Intercept | BM | BM Dum. | ME | MOM | ISSUE | DT-ISSUE | DT-Dum | Avg R² | N (firm-mo) | Months |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | pattern-only | 1.58 (4.41) | SKIP | SKIP |  |  |  |  |  | -0.00 | 503,063 | 448 |
| R2 | PRIMARY | 3.92 (4.05) | SKIP | SKIP | -0.25 (-3.36) |  |  |  |  | 2.55 | 495,639 | 448 |
| R3 | PRIMARY | 1.40 (4.64) | SKIP | SKIP |  | 0.77 (1.54) |  |  |  | 2.28 | 497,200 | 448 |
| R4 | pattern-only | 3.64 (4.14) | SKIP | SKIP | -0.24 (-3.41) | 0.85 (1.96) |  |  |  | 4.39 | 492,013 | 448 |
| R5 | PRIMARY | 1.51 (4.57) | SKIP | SKIP |  |  | -1.27 (-1.73) |  |  | 0.12 | 467,941 | 438 |
| R6 | PRIMARY | 1.54 (4.39) | SKIP | SKIP |  |  |  | 0.01 (0.09) | 0.10 (1.24) | 0.43 | 503,063 | 448 |
| R7 | PRIMARY | 1.45 (4.46) | SKIP | SKIP |  |  | -1.56 (-2.54) | 0.18 (1.33) | 0.14 (1.64) | 0.46 | 467,941 | 438 |
| R8 | pattern-only | 3.40 (4.18) | SKIP | SKIP | -0.21 (-3.35) | 0.93 (2.18) | -1.30 (-2.33) | 0.09 (0.79) | -0.01 (-0.14) | 4.62 | 464,718 | 438 |

_BM / BM Dum. columns are SKIP for every row (A8). Cells show coef (plain FM t-stat). R1 is constant-only (BM omitted) ⇒ not comparable to the paper's R1 (const + BM + BM Dum)._

### Paper Panel A targets (for reference)

| Row | Paper (BM-inclusive) |
|---|---|
| R1 | int 1.40 (3.94), BM 0.34 (3.05), BM Dum −0.02 (−0.19), R² 1.86 |
| R2 | int 3.58 (3.79), ME −0.22 (−3.04), R² 2.58 |
| R3 | int 1.35 (4.56), MOM 0.68 (1.34), R² 2.27 |
| R4 | int 2.77 (3.88), BM 0.15 (2.08), BM Dum 0.17 (2.00), ME −0.16 (−3.16), MOM 0.70 (1.59), R² 5.12 |
| R5 | int 1.52 (4.29), ISSUE 0.52 (0.43), R² 0.12 |
| R6 | int 1.51 (4.31), DT-ISSUE 0.00 (−0.03), DT-Dum 0.00 (0.12), R² 0.17 |
| R7 | int 1.51 (4.32), ISSUE 0.27 (0.21), DT-ISSUE 0.06 (0.46), R² 0.23 |
| R8 | int 2.76 (3.90), BM 0.15 (2.06), ME −0.16 (−3.15), MOM 0.72 (1.66), ISSUE 0.84 (0.68), R² 5.33 |

---

## Paper narrative pattern claims (L3507) — verification

- **(i) ISSUE slopes positive and insignificant in all 1-month specs (|t| < 2)**
  - Verdict: ⚠️ NOT CONFIRMED — see evidence
  - Evidence: R5: ISSUE=-1.27 (t=-1.73); R7: ISSUE=-1.56 (t=-2.54); R8: ISSUE=-1.30 (t=-2.33)
- **(ii) ME significantly negative**
  - Verdict: ✅ CONFIRMED (negative & |t|≥2 in all)
  - Evidence: R2: ME=-0.25 (t=-3.36); R4: ME=-0.24 (t=-3.41); R8: ME=-0.21 (t=-3.35)
- **(iii) MOM positive but 1-month insignificant**
  - Verdict: ⚠️ PARTIAL — positive in all, but significant in some (paper: none significant)
  - Evidence: R3: MOM=0.77 (t=1.54, insig); R4: MOM=0.85 (t=1.96, insig); R8: MOM=0.93 (t=2.18, SIG)

> **Note on (i):** the ISSUE *significance* claim (|t|<2, no predictability) is the paper's central pre-1970 point and is the meaningful guard against overfitting the post-1970 pipeline (ISSUE = −2.23, t = −7.08 post-1970). Our OOS ISSUE slopes are small in magnitude (|β| ≤ ~1.6 vs −2.23 post-1970) but come out weakly NEGATIVE rather than the paper's weakly positive, and are significant in R7/R8. The likely driver is the larger CRSP-only sample (≈1,068 firms/mo vs the paper's ≈841/mo DFF-restricted sample): the extra small-cap firms, excluded by the paper's book-equity requirement, have sparse issuance. Documented as a deviation, not forced.

---

## Appendix — per-cell evaluation vs tables_to_replicate.json (T6)

**Tally (evaluated cells: top-level + PRIMARY R2/R3/R5/R6/R7 + SKIP BM cells):** Tier 1 = 17 · Tier 2 = 11 · FAIL = 3 · SKIP = 12

**Pattern-only cells (R4/R8 non-BM, excluded from the Tier tally):** 14. Their evaluated status is shown for reference but NOT counted above.

Categories: `primary` = BM-free in the paper (in tally); `skip` = BM/BM-Dum cells or R1 row (DFF unavailable, A8; in tally as SKIP); `pattern` = R4/R8 non-BM cells (pattern-only, NOT in tally).

| Metric | Cat. | Paper | Ours | Ours (NW) | Tol% | Rel.dev | Status |
|---|---|---:|---:|---:|---:|---:|---|
| oos_n_obs_regressions | top | 373590.00 | 464718.00 | — | 10 | 24.4% | Tier 2 |
| oos_n_months | top | 444.00 | 438.00 | — | 1 | 1.4% | Tier 2 |
| oos_pA_r1_intercept | skip | 1.40 | 1.58 | — | 40 | — | SKIP |
| oos_pA_r1_intercept_t | skip | 3.94 | 4.41 | 4.41 | 40 | — | SKIP |
| oos_pA_r1_bm | skip | 0.34 | — | — | 40 | — | SKIP |
| oos_pA_r1_bm_t | skip | 3.05 | — | — | 40 | — | SKIP |
| oos_pA_r1_bm_dum | skip | -0.02 | — | — | 100 | — | SKIP |
| oos_pA_r1_bm_dum_t | skip | -0.19 | — | — | 100 | — | SKIP |
| oos_pA_r1_avg_r2 | skip | 1.86 | -0.00 | — | 25 | — | SKIP |
| oos_pA_r2_intercept | primary | 3.58 | 3.92 | — | 40 | 9.6% | Tier 1 |
| oos_pA_r2_intercept_t | primary | 3.79 | 4.05 | 4.05 | 40 | 7.0% | Tier 1 |
| oos_pA_r2_me | primary | -0.22 | -0.25 | — | 40 | 14.2% | Tier 1 |
| oos_pA_r2_me_t | primary | -3.04 | -3.36 | -3.36 | 40 | 10.7% | Tier 1 |
| oos_pA_r2_avg_r2 | primary | 2.58 | 2.55 | — | 25 | 1.1% | Tier 1 |
| oos_pA_r3_intercept | primary | 1.35 | 1.40 | — | 40 | 3.9% | Tier 1 |
| oos_pA_r3_intercept_t | primary | 4.56 | 4.64 | 4.64 | 40 | 1.8% | Tier 1 |
| oos_pA_r3_mom | primary | 0.68 | 0.77 | — | 40 | 13.5% | Tier 1 |
| oos_pA_r3_mom_t | primary | 1.34 | 1.54 | 1.54 | 40 | 15.1% | Tier 1 |
| oos_pA_r3_avg_r2 | primary | 2.27 | 2.28 | — | 25 | 0.3% | Tier 1 |
| oos_pA_r4_intercept | pattern | 2.77 | 3.64 | — | 40 | 31.6% | Tier 1 (pattern-only) |
| oos_pA_r4_intercept_t | pattern | 3.88 | 4.14 | 4.14 | 40 | 6.8% | Tier 1 (pattern-only) |
| oos_pA_r4_bm | skip | 0.15 | — | — | 40 | — | SKIP |
| oos_pA_r4_bm_t | skip | 2.08 | — | — | 40 | — | SKIP |
| oos_pA_r4_bm_dum | skip | 0.17 | — | — | 40 | — | SKIP |
| oos_pA_r4_bm_dum_t | skip | 2.00 | — | — | 40 | — | SKIP |
| oos_pA_r4_me | pattern | -0.16 | -0.24 | — | 40 | 47.4% | Tier 2 (pattern-only) |
| oos_pA_r4_me_t | pattern | -3.16 | -3.41 | -3.41 | 40 | 7.8% | Tier 1 (pattern-only) |
| oos_pA_r4_mom | pattern | 0.70 | 0.85 | — | 40 | 21.6% | Tier 1 (pattern-only) |
| oos_pA_r4_mom_t | pattern | 1.59 | 1.96 | 1.96 | 40 | 23.2% | Tier 1 (pattern-only) |
| oos_pA_r4_avg_r2 | pattern | 5.12 | 4.39 | — | 25 | 14.3% | Tier 1 (pattern-only) |
| oos_pA_r5_intercept | primary | 1.52 | 1.51 | — | 40 | 0.4% | Tier 1 |
| oos_pA_r5_intercept_t | primary | 4.29 | 4.57 | 4.57 | 40 | 6.6% | Tier 1 |
| oos_pA_r5_issue | primary | 0.52 | -1.27 | — | 100 | 344.1% | FAIL |
| oos_pA_r5_issue_t | primary | 0.43 | -1.73 | -1.73 | 100 | 503.2% | Tier 2 |
| oos_pA_r5_avg_r2 | primary | 0.12 | 0.12 | — | 50 | 0.9% | Tier 1 |
| oos_pA_r6_intercept | primary | 1.51 | 1.54 | — | 40 | 1.8% | Tier 1 |
| oos_pA_r6_intercept_t | primary | 4.31 | 4.39 | 4.39 | 40 | 1.9% | Tier 1 |
| oos_pA_r6_dt_issue | primary | 0.00 | 0.01 | — | 100 | 1.3% | Tier 2 |
| oos_pA_r6_dt_issue_t | primary | -0.03 | 0.09 | 0.09 | 100 | 405.2% | Tier 2 |
| oos_pA_r6_dt_dum | primary | 0.00 | 0.10 | — | 100 | 10.0% | Tier 2 |
| oos_pA_r6_dt_dum_t | primary | 0.12 | 1.24 | 1.24 | 100 | 932.8% | Tier 2 |
| oos_pA_r6_avg_r2 | primary | 0.17 | 0.43 | — | 50 | 150.9% | Tier 2 |
| oos_pA_r7_intercept | primary | 1.51 | 1.45 | — | 40 | 4.2% | Tier 1 |
| oos_pA_r7_intercept_t | primary | 4.32 | 4.46 | 4.46 | 40 | 3.2% | Tier 1 |
| oos_pA_r7_issue | primary | 0.27 | -1.56 | — | 100 | 678.4% | FAIL |
| oos_pA_r7_issue_t | primary | 0.21 | -2.54 | -2.54 | 100 | 1311.0% | FAIL |
| oos_pA_r7_dt_issue | primary | 0.06 | 0.18 | — | 100 | 195.5% | Tier 2 |
| oos_pA_r7_dt_issue_t | primary | 0.46 | 1.33 | 1.33 | 100 | 189.8% | Tier 2 |
| oos_pA_r7_avg_r2 | primary | 0.23 | 0.46 | — | 50 | 98.2% | Tier 2 |
| oos_pA_r8_intercept | pattern | 2.76 | 3.40 | — | 40 | 23.1% | Tier 1 (pattern-only) |
| oos_pA_r8_intercept_t | pattern | 3.90 | 4.18 | 4.18 | 40 | 7.3% | Tier 1 (pattern-only) |
| oos_pA_r8_bm | skip | 0.15 | — | — | 40 | — | SKIP |
| oos_pA_r8_me | pattern | -0.16 | -0.21 | — | 40 | 30.8% | Tier 1 (pattern-only) |
| oos_pA_r8_mom | pattern | 0.72 | 0.93 | — | 40 | 29.8% | Tier 1 (pattern-only) |
| oos_pA_r8_issue | pattern | 0.84 | -1.30 | — | 100 | 254.4% | FAIL (pattern-only) |
| oos_pA_r8_issue_t | pattern | 0.68 | -2.33 | -2.33 | 100 | 443.1% | FAIL (pattern-only) |
| oos_pA_r8_avg_r2 | pattern | 5.33 | 4.62 | — | 25 | 13.3% | Tier 1 (pattern-only) |

