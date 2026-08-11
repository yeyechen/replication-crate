# Table V Panel A replication — factor-model regressions on investment-growth quintile portfolios

**VW weight:** Lagged (me_lag, prior month) — [M1] corrected

**Sample:** 23 formation years (cohort year0 1976..1998). Each cohort
contributes 12 months of returns (July Y to June Y+1). Total 276 months
for the regressions.

**Sort:** At end of June of each year, stocks are allocated to 5
investment-growth quintiles (Q1 = highest growth, Q5 = lowest).
Paper convention: rows labeled 'Highest' = Q1 (highest inv growth),
'Lowest' = Q5 (lowest inv growth).

**Returns:** Value-weighted monthly returns using the indicated weight,
per (month, quintile).

**INV factor:** VW(Q5, lowest INV) - VW(Q1, highest INV), per month.
Paper §III.A: 'subtract the returns on the high investment group from
the low investment group each month'.

**Regressions:** For each (quintile, model) pair, time-series OLS of
`excess_ret` (in PCT per month) on the indicated factors (also in PCT).
Reported coefficients and alpha intercepts are in **percent units**.
T-statistics are plain OLS t-stats.

## Factor-level diagnostics (paper §III.A)

| Statistic | Ours | Paper |
|---|---:|---:|
| INV factor mean monthly (pct) | 0.3439 | 0.24 |
| INV factor std dev (decimal)  | 0.024935 | -- |
| INV factor N months | 276 | 276 |
| corr(INV, MKT-RF) | -0.292 | -0.24 |
| corr(INV, SMB)    | -0.046 | ~0 (not significant) |
| corr(INV, HML)    | 0.444 | +0.38 |

## Compact summary — extreme portfolios × 2 key models

### Portfolio: Highest investment growth (Q1 in panel A row order)

| Model | Alpha (pct) | MKT | SMB | HML | INV | Adj R² |
|---|---:|---:|---:|---:|---:|---:|
| M2: FF3 (MKT+SMB+HML) | -0.126 | +1.068 | +0.356 | -0.429 | +nan | 0.931 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.002 | +1.037 | +0.382 | -0.220 | -0.524 | 0.972 |

### Portfolio: Lowest investment growth (Q5 in panel A row order)

| Model | Alpha (pct) | MKT | SMB | HML | INV | Adj R² |
|---|---:|---:|---:|---:|---:|---:|
| M2: FF3 (MKT+SMB+HML) | +0.118 | +1.008 | +0.405 | -0.030 | +nan | 0.918 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.002 | +1.037 | +0.382 | -0.220 | +0.476 | 0.963 |

Note: the 'Highest' and 'Lowest' portfolios share the same MKT/SMB/HML/INV
loadings in the M4 row because INV is constructed as Q5-Q1, so the two
portfolios are the INV factor's own legs (the loadings differ by exactly
1.00 in the INV column and are identical everywhere else).

## Full Table V Panel A — 5 quintiles × 6 model specifications

### Portfolio: Highest (inv_q=1)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | -0.407 | +1.246 | +nan | +nan | +nan | 0.877 | 276 |
| M2: FF3 (MKT+SMB+HML) | -0.126 | +1.068 | +0.356 | -0.429 | +nan | 0.931 | 276 |
| M3: MKT+INV | -0.130 | +1.148 | +nan | +nan | -0.584 | 0.935 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.002 | +1.037 | +0.382 | -0.220 | -0.524 | 0.972 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | -0.091 | +1.085 | +0.397 | +nan | -0.597 | 0.966 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | -0.018 | +1.087 | +nan | -0.261 | -0.499 | 0.943 | 276 |

### Portfolio: 2 (inv_q=2)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | -0.080 | +1.053 | +nan | +nan | +nan | 0.939 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.010 | +1.013 | -0.034 | -0.159 | +nan | 0.944 | 276 |
| M3: MKT+INV | +0.015 | +1.019 | +nan | +nan | -0.200 | 0.949 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.051 | +1.002 | -0.026 | -0.091 | -0.169 | 0.950 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.013 | +1.023 | -0.020 | +nan | -0.199 | 0.949 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.053 | +0.999 | +nan | -0.088 | -0.171 | 0.950 | 276 |

### Portfolio: 3 (inv_q=3)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.087 | +0.919 | +nan | +nan | +nan | 0.962 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.061 | +0.944 | -0.111 | +0.029 | +nan | 0.967 | 276 |
| M3: MKT+INV | +0.066 | +0.926 | +nan | +nan | +0.044 | 0.963 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.050 | +0.947 | -0.113 | +0.011 | +0.044 | 0.968 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.055 | +0.944 | -0.114 | +nan | +0.048 | 0.968 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.056 | +0.931 | +nan | +0.023 | +0.037 | 0.963 | 276 |

### Portfolio: 4 (inv_q=4)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.165 | +0.918 | +nan | +nan | +nan | 0.944 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.140 | +0.938 | -0.068 | +0.033 | +nan | 0.946 | 276 |
| M3: MKT+INV | +0.098 | +0.942 | +nan | +nan | +0.142 | 0.951 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.103 | +0.947 | -0.076 | -0.029 | +0.154 | 0.953 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.090 | +0.953 | -0.074 | +nan | +0.144 | 0.953 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.106 | +0.937 | +nan | -0.021 | +0.149 | 0.951 | 276 |

### Portfolio: Lowest (inv_q=5)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.066 | +1.079 | +nan | +nan | +nan | 0.874 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.118 | +1.008 | +0.405 | -0.030 | +nan | 0.918 | 276 |
| M3: MKT+INV | -0.130 | +1.148 | +nan | +nan | +0.416 | 0.913 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.002 | +1.037 | +0.382 | -0.220 | +0.476 | 0.963 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | -0.091 | +1.085 | +0.397 | +nan | +0.403 | 0.955 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | -0.018 | +1.087 | +nan | -0.261 | +0.501 | 0.924 | 276 |

## Pattern check (paper claim)

INV coef in M3 (MKT+INV) should be NEGATIVE for the highest-inv-growth
portfolio and POSITIVE for the lowest-inv-growth portfolio.

| Portfolio (highest to lowest INV) | INV coef (M3 model) |
|---|---:|
| Highest (inv_q=1) | -0.584 |
| 2 (inv_q=2) | -0.200 |
| 3 (inv_q=3) | +0.044 |
| 4 (inv_q=4) | +0.142 |
| Lowest (inv_q=5) | +0.416 |

Monotonically increasing INV coef from highest to lowest? YES

## Diagnostics

- N months used in regressions: 276 per portfolio
- INV factor coverage: 1976-07-01 .. 1999-06-01

## Notes

- INV factor sign is R_Q5 - R_Q1 (low - high inv growth). Since low-inv-growth
  firms earn higher returns, R_Q5 - R_Q1 averages positive.
- All VW return weights: Lagged (me_lag, prior month) — [M1] corrected.
- Universe: panel (shrcd 10/11, exchcd 1/2/3, non-financial, |inv_growth| <= 10).
- 5 quintiles use uniform all-stock breakpoints (NOT NYSE-only) per spec.