# Table III — Fama–MacBeth Regressions of Annual Stock Returns on Asset Growth and Other Variables

Cooper, Gulen, and Schill (2008), *Asset Growth and the Cross-Section of Stock Returns* (Journal of Finance). Caption (content.md L1642): "Annual stock returns from July 1968 to June 2003 are regressed on lagged accounting and return-based variables. ... Panel A reports regressions for all firms, and Panels B, C, and D report regressions for small, medium, and large firms, respectively. Beta estimates are time-series averages of cross-sectional regression betas obtained from annual cross-sectional regressions. The t-statistics, in parentheses, are adjusted for autocorrelation in the beta estimates."

**Inference convention (footnote 13, L1628).** Annual cross-sectional OLS each year (35 years); coefficient = time-series mean of the annual slopes; SE = std(slopes, ddof=1)/√N × √((1+ρ)/(1−ρ)) with ρ the first-order autocorrelation of the annual slope series; t = mean/SE. **Main spec = no winsorization** (Assumption 7); the 1%/99% winsorized M1 is the paper's documented robustness (L2592). Dependent variable: geometrically compounded annual firm return, decimal (L1622). Inclusion filter (L1622): non-missing {BM, MV, BHRET6, ASSETG} and book equity (FY t−1) > 0; extra regressors enter via OLS listwise deletion per model.

**MV units note.** The paper's M1 MV coefficient (−0.0044) is hard to reconcile with MV in raw $millions on a decimal-return dependent; per the task diagnostic we report BOTH the raw-MV coefficient (MV = June-t market equity, $M, rule var_mv) and a log_MV = ln(MV[$M]) variant of M1 below. The headline target is the ASSETG coefficient/t-stat, which is robust to the MV specification.

## Panel A — All Firms (annual returns; N and avg obs/yr per model)

| Variable | M1 | M2 | M3 | M4 | M5 | M6 | M7 |
|---|---|---|---|---|---|---|---|
| Constant | 0.1386 (4.55) | 0.1442 (4.73) | 0.1371 (4.75) | 0.1443 (4.82) | 0.2084 (3.62) | 0.0837 (1.43) | 0.1727 (6.38) |
| ASSETG | -0.0649 (-5.34) | -0.0599 (-5.62) | -0.0789 (-8.86) | -0.0700 (-6.05) | -0.0651 (-5.06) | -0.1103 (-2.23) | -0.0690 (-7.75) |
| L2ASSETG |   | -0.0360 (-3.46) |   |   |   |   |   |
| BM | 0.0284 (3.11) | 0.0269 (3.03) | 0.0280 (4.13) | 0.0263 (2.81) | 0.0315 (3.78) | 0.0378 (3.58) | 0.0250 (3.50) |
| MV | -0.000004 (-1.39) | -0.000004 (-1.42) | -0.000003 (-1.47) | -0.000004 (-1.55) | -0.000004 (-1.50) | -0.000005 (-1.61) | -0.000003 (-1.39) |
| BHRET6 | 0.0278 (1.48) | 0.0230 (1.22) | 0.0245 (1.25) | 0.0315 (1.56) | 0.0260 (1.39) | -0.1252 (-0.78) | 0.0244 (1.22) |
| BHRET36 | 0.0028 (0.27) | 0.0038 (0.38) | 0.0041 (0.46) | 0.0031 (0.29) | 0.0024 (0.24) | -0.0022 (-0.11) | 0.0019 (0.21) |
| 5YSALESG |   |   | 0.0026 (0.08) |   |   |   |   |
| CI |   |   |   | -0.0041 (-2.72) |   |   |   |
| NOA/A |   |   |   |   | -0.1057 (-2.28) |   |   |
| ACCRUALS |   |   |   |   |   | -0.1977 (-1.07) |   |
| 5YASSETG |   |   |   |   |   |   | -0.0605 (-2.16) |
| **N** | 81,333 (2324/yr, 35 yrs) | 81,251 (2321/yr, 35 yrs) | 63,953 (1827/yr, 35 yrs) | 76,574 (2188/yr, 35 yrs) | 81,333 (2324/yr, 35 yrs) | 65,576 (1874/yr, 35 yrs) | 64,558 (1845/yr, 35 yrs) |

Paper Panel A targets: M1 Constant 0.1373 (4.55), ASSETG −0.0922 (−6.52), BM 0.029 (3.40), MV −0.0044 (−1.57), BHRET6 0.0248 (1.09), BHRET36 0.0056 (0.57). M3: ASSETG t −7.41, 5YSALESG t −0.27. M4: ASSETG t −6.05, CI t −3.32. M5: ASSETG t −6.10, NOA/A t −2.43. M6: ASSETG t −5.65 (prose L2570; the Panel A HTML cell shows −5.24), ACCRUALS t −4.00. M7: ASSETG t −6.98, 5YASSETG −0.0275 (−2.22).

### MV unit diagnostic (M1)

| Specification | Size coef | Size t | ASSETG coef | ASSETG t |
|---|---|---|---|---|
| M1 raw MV ($M) | -0.0000036 | -1.39 | -0.0649 | -5.34 |
| M1 MV ($billions = $M/1000) | -0.0036 | -1.39 | -0.0649 | -5.34 |
| M1 log_MV = ln($M) | -0.0126 | -1.84 | -0.0641 | -5.44 |

Paper MV = −0.0044 (t −1.57). **Neither raw $M (-0.0000036) nor log_MV (-0.0126) literally equals −0.0044, but MV expressed in $billions gives -0.0036 ≈ −0.0044** (t -1.39 vs −1.57; the t-stat is scale-invariant and matches under any scaling). The paper's reported MV coefficient is consistent with MV measured in $billions (i.e., our $M coefficient ×1000). ASSETG is essentially invariant to the size specification (t −5.34 / −5.34 / −5.44).

## Robustness around M1

### (a) Winsorized M1 — regressors clipped to 1%/99% within each year (L2592)

| Variable | Coef | t (paper-adj) | Paper t |
|---|---|---|---|
| Constant | 0.1375 | 4.15 |  |
| ASSETG | -0.0947 | -6.64 | -9.47 |
| BM | 0.0346 | 2.42 | 3.27 |
| MV | -0.0000 | -1.39 | -1.58 |
| BHRET6 | 0.0356 | 1.63 |  |
| BHRET36 | 0.0041 | 0.35 |  |

### (b) Size groups — M1 within small / medium / large (Panels B/C/D; Assumption 4)

| Size | N | Years | ASSETG coef | ASSETG t | Paper ASSETG t |
|---|---|---|---|---|---|
| small | 43,161 | 35 | -0.0670 | -4.90 | -5.18 |
| medium | 22,361 | 35 | -0.0675 | -3.26 | -3.8 |
| large | 15,811 | 35 | -0.0541 | -2.35 | -3.6 |

### (c) Monthly-return dependent — M1 on monthly returns, June-t regressors repeated over the 12 holding months (L2594)

420 monthly cross-sections. ASSETG coef -0.00571, **t = -5.94** (paper −7.36). BM t 3.92, MV t -1.77.

### (d) Subperiod stability — monthly M1 split on formation_year (L2590)

| Subperiod | Months | ASSETG t | Paper | BM t | Paper BM |
|---|---|---|---|---|---|
| 1968-1980 | 144 | -3.10 | -3.98 | 2.10 | 1.4 |
| 1981-1990 | 120 | -5.26 | -4.46 | 3.31 | 2.12 |
| 1991-2003 | 156 | -5.28 | -6.14 | 1.73 | 2.23 |

### M6 (ACCRUALS) diagnostic — why M6 runs weaker than the paper

Our M6 gives ASSETG t -2.23 / ACCRUALS t -1.07 (paper −5.65 / −4.00). Root cause: the 1968–1970 ACCRUALS cross-sections are near-empty (1968: 13 firms, 1969: 15 firms, 1970: 19 firms) because pre-1971 Compustat `act`/`lct`/`txp`/`dp` are largely missing (e.g., `txp` is 44–61% null in FY 1966–1968), so those annual regressions rest on <20 firms and produce outlier slopes (1960s ACCRUALS slope mean ≈ −1.95 vs ≈ −0.15 from 1971). Dropping the <100-obs years (32 yrs, 1971–2002) gives ASSETG t -3.28 and ACCRUALS t -1.27 — improved but still below the paper, consistent with the documented data-vintage attenuation of the ASSETG upper tail (Assumption 7; our raw M1 ASSETG t −5.34 vs the paper's −6.52). ACCRUALS itself is not heavy-tailed (whole-sample std 0.16, max 1.9; winsorizing M1-style leaves the t at −0.86). Main-spec M6 is reported as-is (Tier 2).

## Variable construction notes

- 5YASSETG / 5YSALESG (Appendix L4392/L4394): weighted average of cross-sectional ranks in years t−5..t−2 (t−1 omitted), weights 0.10/0.20/0.30/0.40; rank normalization = (average ascending rank − 1) / (N_year − 1) ∈ [0,1] (low growth = 0). Ranks computed at the gvkey level from the deduped funda (same ASSETG/SALESG formulas + 2-year backfill as the foundation) for june_years 1963–2002, extending the foundation window back to 1963 (the paper's Compustat start, L73) so all 35 formation years are covered; all four yearly ranks required, else NaN.
- NOA/A (var_noa L4404, caption L1642): NOA = dlc + dltt + mib + pstk + ceq − ch at FY t−1 (missing sub-items → 0); NOA/A = NOA / CURRENT total assets (at, FY t−1); mapped to (permno, june_year) via the foundation's PIT CRSP–Compustat link (src/sql/noa_fundamentals.sql, dedup Assumption 3).