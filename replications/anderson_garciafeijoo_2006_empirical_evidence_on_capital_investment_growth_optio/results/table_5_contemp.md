# Table V Panel A replication — factor-model regressions on investment-growth quintile portfolios

**VW weight:** Contemporaneous (me_dollars) — original shipped weighting

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
| M2: FF3 (MKT+SMB+HML) | +0.896 | +1.082 | +0.306 | -0.461 | +nan | 0.922 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.978 | +1.048 | +0.362 | -0.243 | -0.527 | 0.965 |

### Portfolio: Lowest investment growth (Q5 in panel A row order)

| Model | Alpha (pct) | MKT | SMB | HML | INV | Adj R² |
|---|---:|---:|---:|---:|---:|---:|
| M2: FF3 (MKT+SMB+HML) | +1.052 | +1.018 | +0.412 | -0.046 | +nan | 0.908 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.978 | +1.048 | +0.362 | -0.243 | +0.473 | 0.954 |

Note: the 'Highest' and 'Lowest' portfolios share the same MKT/SMB/HML/INV
loadings in the M4 row because INV is constructed as Q5-Q1, so the two
portfolios are the INV factor's own legs (the loadings differ by exactly
1.00 in the INV column and are identical everywhere else).

## Full Table V Panel A — 5 quintiles × 6 model specifications

### Portfolio: Highest (inv_q=1)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.600 | +1.261 | +nan | +nan | +nan | 0.872 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.896 | +1.082 | +0.306 | -0.461 | +nan | 0.922 | 276 |
| M3: MKT+INV | +0.822 | +1.166 | +nan | +nan | -0.568 | 0.930 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.978 | +1.048 | +0.362 | -0.243 | -0.527 | 0.965 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.867 | +1.102 | +0.382 | +nan | -0.602 | 0.958 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.958 | +1.097 | +nan | -0.292 | -0.479 | 0.940 | 276 |

### Portfolio: 2 (inv_q=2)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.524 | +1.064 | +nan | +nan | +nan | 0.927 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.623 | +1.024 | -0.079 | -0.180 | +nan | 0.935 | 276 |
| M3: MKT+INV | +0.609 | +1.027 | +nan | +nan | -0.218 | 0.940 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.651 | +1.013 | -0.060 | -0.104 | -0.181 | 0.942 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.603 | +1.036 | -0.051 | +nan | -0.214 | 0.941 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.654 | +1.004 | +nan | -0.096 | -0.189 | 0.941 | 276 |

### Portfolio: 3 (inv_q=3)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.534 | +0.922 | +nan | +nan | +nan | 0.958 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.512 | +0.948 | -0.130 | +0.019 | +nan | 0.965 | 276 |
| M3: MKT+INV | +0.522 | +0.927 | +nan | +nan | +0.032 | 0.958 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.505 | +0.950 | -0.135 | +0.001 | +0.044 | 0.965 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.506 | +0.950 | -0.135 | +nan | +0.044 | 0.965 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.512 | +0.932 | +nan | +0.020 | +0.026 | 0.958 | 276 |

### Portfolio: 4 (inv_q=4)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.659 | +0.919 | +nan | +nan | +nan | 0.938 | 276 |
| M2: FF3 (MKT+SMB+HML) | +0.641 | +0.936 | -0.079 | +0.019 | +nan | 0.940 | 276 |
| M3: MKT+INV | +0.614 | +0.938 | +nan | +nan | +0.117 | 0.942 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.620 | +0.945 | -0.094 | -0.038 | +0.137 | 0.946 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.603 | +0.954 | -0.091 | +nan | +0.125 | 0.945 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.625 | +0.933 | +nan | -0.025 | +0.125 | 0.942 | 276 |

### Portfolio: Lowest (inv_q=5)

| Model | Alpha | MKT | SMB | HML | INV | Adj R² | N |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1: MKT only | +0.990 | +1.094 | +nan | +nan | +nan | 0.864 | 276 |
| M2: FF3 (MKT+SMB+HML) | +1.052 | +1.018 | +0.412 | -0.046 | +nan | 0.908 | 276 |
| M3: MKT+INV | +0.822 | +1.166 | +nan | +nan | +0.432 | 0.908 | 276 |
| M4: 4-factor (MKT+SMB+HML+INV) | +0.978 | +1.048 | +0.362 | -0.243 | +0.473 | 0.954 | 276 |
| M5: 4-factor no HML (MKT+SMB+INV) | +0.867 | +1.102 | +0.382 | +nan | +0.398 | 0.945 | 276 |
| M6: 4-factor no SMB (MKT+HML+INV) | +0.958 | +1.097 | +nan | -0.292 | +0.521 | 0.921 | 276 |

## Pattern check (paper claim)

INV coef in M3 (MKT+INV) should be NEGATIVE for the highest-inv-growth
portfolio and POSITIVE for the lowest-inv-growth portfolio.

| Portfolio (highest to lowest INV) | INV coef (M3 model) |
|---|---:|
| Highest (inv_q=1) | -0.568 |
| 2 (inv_q=2) | -0.218 |
| 3 (inv_q=3) | +0.032 |
| 4 (inv_q=4) | +0.117 |
| Lowest (inv_q=5) | +0.432 |

Monotonically increasing INV coef from highest to lowest? YES

## Diagnostics

- N months used in regressions: 276 per portfolio
- INV factor coverage: 1976-07-01 .. 1999-06-01

## Notes

- INV factor sign is R_Q5 - R_Q1 (low - high inv growth). Since low-inv-growth
  firms earn higher returns, R_Q5 - R_Q1 averages positive.
- All VW return weights: Contemporaneous (me_dollars) — original shipped weighting.
- Universe: panel (shrcd 10/11, exchcd 1/2/3, non-financial, |inv_growth| <= 10).
- 5 quintiles use uniform all-stock breakpoints (NOT NYSE-only) per spec.