# Table VII — Alphas of IVOL Portfolios Controlling for Cross-Sectional Effects
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Dependent double sorts. Each formation month, stocks are first sorted into
quintiles on the control characteristic, then within each control quintile
into quintiles on IVOL (relative to FF-3); cell returns are value-weighted by
month-t market equity and earned in month t+1. The five IVOL portfolios are
then averaged (equal-weighted) across the five control quintiles. Reported:
FF-3 alphas in percent per month; Newey–West(4) t-statistics in parentheses.
"NYSE Stocks Only" restricts the universe to hexcd == 1 (single IVOL sort).
Breakpoints use all stocks (20/40/60/80 pctiles). Holding months 1963-07 to
2000-12. FF factors from ff.four_factor_monthly (decimal).

### Dependent double sorts (FF-3 alphas, %/month)

| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| NYSE Stocks Only (rep) | 0.02 | -0.02 | 0.02 | -0.05 | -0.51 | -0.54 |
| NYSE Stocks Only (paper) | 0.06 | 0.04 | 0.02 | -0.04 | -0.60 | -0.66 |
| Controlling for Size (rep) | 0.09 | 0.21 | 0.12 | -0.11 | -0.91 | -1.01 |
| Controlling for Size (paper) | 0.11 | 0.18 | 0.09 | -0.15 | -0.93 | -1.04 |
| Controlling for B/M (rep) | -0.02 | -0.00 | 0.02 | -0.25 | -0.93 | -0.91 |
| Controlling for B/M (paper) | 0.61 | 0.69 | 0.71 | 0.50 | -0.19 | -0.80 |
| Controlling for Leverage (rep) | 0.08 | 0.09 | 0.10 | -0.24 | -1.06 | -1.14 |
| Controlling for Leverage (paper) | 0.11 | 0.11 | 0.08 | -0.24 | -1.12 | -1.23 |
| Controlling for Volume (rep) | -0.10 | -0.02 | -0.13 | -0.36 | -1.13 | -1.03 |
| Controlling for Volume (paper) | -0.03 | 0.02 | -0.01 | -0.39 | -1.25 | -1.22 |
| Controlling for Turnover (rep) | 0.11 | 0.01 | -0.07 | -0.47 | -1.29 | -1.40 |
| Controlling for Turnover (paper) | 0.11 | 0.03 | -0.11 | -0.49 | -1.34 | -1.46 |
| Controlling for Coskew (rep) | -0.01 | 0.06 | 0.06 | -0.30 | -1.21 | -1.20 |
| Controlling for Coskew (paper) | -0.02 | -0.00 | 0.01 | -0.37 | -1.40 | -1.38 |

**Absolute differences (rep − paper):**

| Control | ΔQ1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| NYSE Stocks Only | -0.04 | -0.06 | 0.00 | -0.01 | 0.09 | 0.12 |
| Controlling for Size | -0.02 | 0.03 | 0.03 | 0.04 | 0.02 | 0.03 |
| Controlling for B/M | -0.63 | -0.69 | -0.69 | -0.75 | -0.74 | -0.11 |
| Controlling for Leverage | -0.03 | -0.02 | 0.02 | -0.00 | 0.06 | 0.09 |
| Controlling for Volume | -0.07 | -0.04 | -0.12 | 0.03 | 0.12 | 0.19 |
| Controlling for Turnover | 0.00 | -0.02 | 0.04 | 0.02 | 0.05 | 0.06 |
| Controlling for Coskew | 0.01 | 0.06 | 0.05 | 0.07 | 0.19 | 0.18 |

### Newey–West(4) t-statistics (replication)

| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| NYSE Stocks Only | (0.52) | (-0.33) | (0.29) | (-0.53) | (-5.01) | (-4.34) |
| Controlling for Size | (1.01) | (2.50) | (1.61) | (-1.33) | (-6.42) | (-5.13) |
| Controlling for B/M | (-0.54) | (-0.06) | (0.23) | (-2.86) | (-7.27) | (-5.75) |
| Controlling for Leverage | (1.93) | (1.99) | (1.45) | (-2.55) | (-7.27) | (-7.01) |
| Controlling for Volume | (-1.29) | (-0.22) | (-1.85) | (-4.59) | (-8.72) | (-5.97) |
| Controlling for Turnover | (2.34) | (0.16) | (-1.16) | (-5.88) | (-9.88) | (-9.98) |
| Controlling for Coskew | (-0.19) | (0.84) | (0.83) | (-3.11) | (-7.59) | (-6.21) |

### Size Quintiles detail (5×5: size × IVOL, FF-3 alphas, %/month)

Within each size quintile, stocks are sorted into IVOL quintiles; the cell
FF-3 alphas are reported (NOT averaged across size quintiles).

| Quintile | IVOL 1 | 2 | 3 | 4 | 5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| Small 1 (rep) | 0.07 | 0.29 | 0.34 | 0.05 | -0.53 | -0.61 |
| Small 1 (paper) | 0.11 | 0.26 | 0.31 | 0.06 | -0.43 | -0.55 |
| 2 (rep) | 0.19 | 0.26 | -0.03 | -0.55 | -1.72 | -1.91 |
| 2 (paper) | 0.19 | 0.20 | -0.07 | -0.65 | -1.73 | -1.91 |
| 3 (rep) | 0.12 | 0.25 | 0.06 | -0.20 | -1.41 | -1.53 |
| 3 (paper) | 0.12 | 0.21 | 0.03 | -0.27 | -1.49 | -1.61 |
| 4 (rep) | 0.03 | 0.21 | 0.22 | 0.03 | -0.78 | -0.80 |
| 4 (paper) | 0.03 | 0.22 | 0.17 | -0.03 | -0.82 | -0.86 |
| Large 5 (rep) | 0.04 | 0.02 | 0.02 | 0.12 | -0.13 | -0.18 |
| Large 5 (paper) | 0.09 | 0.04 | 0.03 | 0.14 | -0.17 | -0.26 |

## Notes
- Average stocks/month per control sort: NYSE Stocks Only=1735, Controlling for Size=4742, Controlling for B/M=3652, Controlling for Leverage=3853, Controlling for Volume=4122, Controlling for Turnover=4122, Controlling for Coskew=4669.
- Stocks missing a given control are dropped from that control's sort only.
- Book-to-market and leverage use Compustat-matched firms (financial firms
  with only FS-format records have missing bm/leverage → fewer stocks).
- Coskewness computed following Harvey & Siddique (2000) in the data pipeline.
