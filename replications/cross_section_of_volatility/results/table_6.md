# Table VI — Portfolios Sorted on Volatility
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Value-weighted quintile portfolios, formed monthly on the signal measured
from month-t daily data and held for month t+1 (1/0/1 strategy).
Sample: 1963-07 to 2000-12 (450 holding months).
Breakpoints: simple quintile cuts (20/40/60/80 pctiles) of ALL stocks.
Mean / Std. Dev. are monthly TOTAL simple returns in percent.
CAPM / FF-3 alphas in percent per month; robust Newey–West (1987)
t-statistics (4 lags) in parentheses.
Average stocks per formation month: 4,742.

### Panel A: Total Volatility

| Portfolio | Mean | Std. Dev. | % Mkt Share | Size | B/M | CAPM α | (t) | FF-3 α | (t) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 1.03 | 3.63 | 43.16 | 4.67 | 0.93 | 0.12 | (1.60) | -0.02 | (-0.29) |
| Q2 | 1.13 | 4.46 | 33.09 | 4.71 | 0.89 | 0.11 | (2.01) | 0.06 | (1.07) |
| Q3 | 1.19 | 5.64 | 14.95 | 4.10 | 0.91 | 0.04 | (0.43) | 0.12 | (1.54) |
| Q4 | 0.99 | 7.20 | 6.46 | 3.48 | 0.94 | -0.29 | (-1.74) | -0.12 | (-0.94) |
| Q5 | 0.05 | 8.44 | 2.34 | 2.58 | 1.04 | -1.25 | (-4.83) | -1.09 | (-5.94) |
| 5-1 | -0.98 | 7.01 |  |  |  | -1.37 | (-4.34) | -1.08 | (-5.01) |

**Paper values (Panel A: Total Volatility):**

| Portfolio | Mean | Std. Dev. | CAPM α | FF-3 α |
|---|---:|---:|---:|---:|
| Q1 | 1.06 | 3.71 | 0.14 | 0.03 |
| Q2 | 1.15 | 4.48 | 0.13 | 0.08 |
| Q3 | 1.22 | 5.63 | 0.07 | 0.12 |
| Q4 | 0.99 | 7.15 | -0.28 | -0.17 |
| Q5 | 0.09 | 8.30 | -1.21 | -1.16 |
| 5-1 | -0.97 | — | -1.35 | -1.19 |

### Panel B: Idiosyncratic Volatility (relative to FF-3)

| Portfolio | Mean | Std. Dev. | % Mkt Share | Size | B/M | CAPM α | (t) | FF-3 α | (t) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Q1 | 1.04 | 3.83 | 53.69 | 4.84 | 0.91 | 0.09 | (1.37) | -0.00 | (-0.06) |
| Q2 | 1.16 | 4.72 | 27.24 | 4.71 | 0.88 | 0.10 | (2.00) | 0.08 | (1.44) |
| Q3 | 1.20 | 5.85 | 11.88 | 4.06 | 0.90 | 0.02 | (0.22) | 0.09 | (1.22) |
| Q4 | 0.85 | 7.10 | 5.20 | 3.41 | 0.95 | -0.41 | (-2.53) | -0.29 | (-2.95) |
| Q5 | 0.01 | 8.20 | 1.98 | 2.52 | 1.06 | -1.26 | (-4.88) | -1.17 | (-6.53) |
| 5-1 | -1.02 | 6.66 |  |  |  | -1.35 | (-4.34) | -1.17 | (-5.71) |

**Paper values (Panel B: Idiosyncratic Volatility (relative to FF-3)):**

| Portfolio | Mean | Std. Dev. | CAPM α | FF-3 α |
|---|---:|---:|---:|---:|
| Q1 | 1.04 | 3.83 | 0.11 | 0.04 |
| Q2 | 1.16 | 4.74 | 0.11 | 0.09 |
| Q3 | 1.20 | 5.85 | 0.04 | 0.08 |
| Q4 | 0.87 | 7.13 | -0.38 | -0.32 |
| Q5 | -0.02 | 8.16 | -1.27 | -1.27 |
| 5-1 | -1.06 | — | -1.38 | -1.31 |

## Notes

- Size = time-series average of the monthly cross-sectional SIMPLE mean of
  firm log market capitalization ($ millions), per the paper's wording
  ("average log market capitalization for firms within the portfolio").
  Value-weighted alternatives: Panel A Size(VW) =
  8.44, 7.95, 7.01,
  5.98, 4.86; Panel B Size(VW) =
  8.69, 7.55, 6.62,
  5.68, 4.68.
- B/M = time-series average of the monthly cross-sectional SIMPLE mean of
  firm book-to-market (firms with missing B/M excluded from the average).
  Value-weighted alternatives: Panel A B/M(VW) =
  0.65, 0.62, 0.64,
  0.67, 0.76; Panel B B/M(VW) =
  0.62, 0.63, 0.65,
  0.69, 0.78.
- % Mkt Share is relative to the total market cap of the sorted universe
  (stocks with a valid signal and ME) each month; quintile shares sum to 100%.
- FF factors from ff.four_factor_monthly (decimal); portfolio excess return
  = VW total return − monthly rf.
- Delisting returns are compounded into each stock's last trading-month
  return upstream (data pipeline, assumption A12).
