# Table XI — FF-3 Alphas Across Subsamples (1/0/1 Strategy)
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Value-weighted quintile portfolios sorted on idiosyncratic volatility
(relative to FF-3), 1/0/1 strategy (sort on month-t IVOL, hold month
t+1). Alphas in percent per month; Newey–West (1987) t-statistics
(4 lags) in parentheses. Quintile portfolios are formed each month on
the full cross-section; subsamples split the resulting monthly return
series by HOLDING month.
Average stocks per formation month: 4,742.

### Full sample (Jul 1963 – Dec 2000)

| Portfolio | FF-3 α | (t) | Mean |
|---|---:|---:|---:|
| Q1 | -0.00 | (-0.06) | 1.04 |
| Q2 | 0.08 | (1.44) | 1.16 |
| Q3 | 0.09 | (1.22) | 1.20 |
| Q4 | -0.29 | (-2.95) | 0.85 |
| Q5 | -1.17 | (-6.53) | 0.01 |
| 5-1 | -1.17 | (-5.71) | -1.02 |

### Subsample alphas

| Subsample | n | Q1 α | Q2 α | Q3 α | Q4 α | Q5 α | (t) | 5-1 α | (t) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jul 1963 – Dec 1970 | 90 | 0.06 | 0.03 | 0.11 | -0.35 | -0.90 | (-5.36) | -0.95 | (-5.24) |
| Jan 1971 – Dec 1980 | 120 | -0.24 | 0.31 | 0.23 | 0.08 | -0.92 | (-5.03) | -0.68 | (-2.70) |
| Jan 1981 – Dec 1990 | 120 | 0.11 | 0.04 | -0.11 | -0.60 | -2.01 | (-8.96) | -2.12 | (-8.04) |
| Jan 1991 – Dec 2000 | 120 | 0.06 | 0.05 | 0.10 | -0.48 | -1.22 | (-2.59) | -1.28 | (-2.37) |
| NBER Expansions | 388 | 0.03 | 0.03 | 0.08 | -0.33 | -1.13 | (-5.80) | -1.16 | (-5.27) |
| NBER Recessions | 62 | -0.17 | 0.45 | 0.09 | -0.20 | -1.61 | (-2.94) | -1.44 | (-2.22) |
| Stable periods | 90 | 0.15 | -0.06 | -0.14 | -0.72 | -1.80 | (-8.56) | -1.95 | (-7.72) |
| Volatile periods | 90 | -0.24 | 0.19 | 0.26 | 0.30 | -0.48 | (-0.91) | -0.24 | (-0.41) |

**Paper values (Q5 α and 5-1 α, FF-3):**

| Subsample | Q5 α (paper) | 5-1 α (paper) |
|---|---:|---:|
| Jul 1963 – Dec 1970 | -0.94 | -1.00 |
| Jan 1971 – Dec 1980 | -1.02 | -0.77 |
| Jan 1981 – Dec 1990 | -2.08 | -2.23 |
| Jan 1991 – Dec 2000 | -1.39 | -1.55 |
| NBER Expansions | -1.19 | -1.25 |
| NBER Recessions | -1.88 | -1.79 |
| Stable periods | -1.66 | -1.71 |
| Volatile periods | -0.93 | -0.89 |

## Notes

- Decade subsamples (a–d) and NBER cycle subsamples (e–f) use holding
  months in the given ranges. NBER recessions (peak–trough, inclusive):
  1969-12–1970-11, 1973-11–1975-03, 1980-01–1980-07, 1981-07–1982-11,
  1990-07–1991-03, 2001-03–2001-11 (the last falls after the sample
  end 2000-12 and contributes 0 months). Expansions = all other
  in-sample months.
- Stable/volatile subsamples: months with |MKT|RF| (ff.four_factor_monthly
  mkt_rf, decimal) in the lowest/highest 20% of in-sample holding months
  (20th pctile = 1.126%, 80th pctile = 5.050%); exactly 90
  months in each (450 × 0.20).
- 5-1 spread regression is zero-investment (no rf subtraction).
- FF factors from ff.four_factor_monthly (decimal).

### Sensitivity — stable/volatile classified on the FORMATION month

Issue M4: the paper (L2074) classifies months by |MKT|RF|. The return series is indexed by the HOLDING month, so the primary table classifies on the holding month. As a sensitivity, classifying on the FORMATION month (holding − 1; 20th pctile = 1.126%, 80th pctile = 5.050%) gives:

| Subsample | n | Q5 α | 5-1 α | (t) | Paper 5-1 |
|---|---:|---:|---:|---:|---:|
| Stable (formation) | 90 | -1.18 | -1.21 | (-3.41) | -1.71 |
| Volatile (formation) | 90 | -1.21 | -1.21 | (-1.98) | -0.89 |

The formation-month convention moves the volatile-period 5-1 closer to the paper (less attenuated) but makes stable ≈ volatile (both near -1.21), destroying the paper's stable-vs-volatile contrast (paper stable -1.71 vs volatile -0.89). The holding-month convention (primary table) reproduces that contrast and matches the stable period well. The volatile-period 5-1 is attenuated under BOTH conventions and is highly sensitive to the exact 90-month set — a small-sample limitation.
