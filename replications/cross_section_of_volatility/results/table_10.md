# Table X — FF-3 Alphas for L/M/N Strategies
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Value-weighted quintile portfolios sorted on idiosyncratic volatility
(relative to FF-3). L = formation months of daily data, M = skip months, N = holding months. At month t, IVOL is computed from daily
data over the L-month window ending at month t-M; portfolios are value weighted and held N months. For N=12 the return each month is
the simple average of the 12 active Jegadeesh-Titman cohorts (L1132/L1134). Alphas in percent per month from FF-3 time-series
regressions; Newey-West (1987) t-statistics (4 lags) in parentheses.
Sample: holding months 1963-07 to 2000-12.

### All four strategies — this replication (FF-3 alphas, %/month)

| Strategy | L/M/N | n | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1/1/1 | L=1, M=1, N=1 | 449 | 0.02 | 0.02 | 0.11 | -0.08 | -0.66 | -0.68 |
| 1/1/12 | L=1, M=1, N=12 | 449 | 0.01 | -0.03 | -0.06 | -0.17 | -0.60 | -0.61 |
| 12/1/1 | L=12, M=1, N=1 | 444 | 0.01 | 0.07 | 0.01 | -0.21 | -0.80 | -0.82 |
| 12/1/12 | L=12, M=1, N=12 | 444 | 0.00 | 0.01 | -0.07 | -0.33 | -0.65 | -0.65 |

### Paper values (FF-3 alphas, %/month)

| Strategy | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| 1/1/1 | 0.06 | 0.04 | 0.09 | -0.18 | -0.82 | -0.88 |
| 1/1/12 | 0.03 | 0.02 | -0.02 | -0.17 | -0.64 | -0.67 |
| 12/1/1 | 0.04 | 0.08 | -0.01 | -0.29 | -1.08 | -1.12 |
| 12/1/12 | 0.04 | 0.04 | -0.02 | -0.35 | -0.73 | -0.77 |

### Headline comparison (Q5 and 5-1 FF-3 alphas)

| Strategy | Q5 (ours) | Q5 (paper) | 5-1 (ours) | 5-1 (paper) | 5-1 t | 5-1 dev. |
|---|---:|---:|---:|---:|---:|---:|
| 1/1/1 | -0.66 | -0.82 | -0.68 | -0.88 | (-3.46) | 22% |
| 1/1/12 | -0.60 | -0.64 | -0.61 | -0.67 | (-3.85) | 9% |
| 12/1/1 | -0.80 | -1.08 | -0.82 | -1.12 | (-3.56) | 27% |
| 12/1/12 | -0.65 | -0.73 | -0.65 | -0.77 | (-2.98) | 15% |

### t-statistics (this replication)

| Strategy | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| 1/1/1 | (0.48) | (0.48) | (1.41) | (-0.75) | (-3.87) | (-3.46) |
| 1/1/12 | (0.29) | (-0.59) | (-1.02) | (-2.02) | (-4.47) | (-3.85) |
| 12/1/1 | (0.40) | (1.11) | (0.11) | (-1.49) | (-3.83) | (-3.56) |
| 12/1/12 | (0.10) | (0.12) | (-0.81) | (-2.89) | (-3.30) | (-2.98) |

## Notes

- **12-month IVOL (L=12).** IVOL_12 for signal month s is the std of
  residuals from ONE pooled FF3 regression over all daily excess
  returns in months [s-11, s]. Computed SQL-first by summing the
  additive monthly sufficient statistics (X'X, X'y, y'y, n) over a
  calendar-correct 12-month RANGE window (src/sql/ivol12_stats.sql)
  and solving the 4x4 normal equations in closed form (ddof=1,
  mirrors main.py; verified to match a direct pooled daily   regression). Requires n_obs_12 >= 120.
- **Min-obs threshold (paper silent for L=12).** 120 daily   obs over the 12-month window (~10/month). The literal 17x12=204
  (17/month, mirroring the L=1 rule) was also tested and moves the   L=12 spreads slightly further from the paper; 120 reproduces the
  paper better and is used here.
- **Overlapping cohorts (N=12).** Each month 12 cohorts are active;   the quintile return is the simple average of the cohorts' VW
  returns, each cohort value-weighted at its own formation (paper   §II.A.2 / L1134). Formation weight = market equity at the signal
  month (consistent with the validated 1/0/1 and 1/1/1 pipeline).
- **Alpha convention (correct per audit M1).** Returns are indexed   by the HOLDING month and regressed on the same-month FF factors;
  TOTAL returns are passed to factor_alpha (single rf subtraction);   the 5-1 spread is zero-investment (rf zeroed). Mean market beta
  across quintiles is ~1 for every strategy (VW diversified   portfolio) — see diagnostics below.
- Breakpoints: simple quintile cuts of ALL stocks with a valid   signal + ME each signal month (Assumption A19).
- FF factors from ff.four_factor_monthly (decimal). L=12 strategies   start a few months after 1963-07 (need a 12-month window), so
  their n is slightly below the L=1 strategies' 449.
- Mean market beta per strategy (quintile average): 1/1/1 = 1.09; 1/1/12 = 1.10; 12/1/1 = 1.13; 12/1/12 = 1.14.
