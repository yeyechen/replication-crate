# Table VIII — Alphas of IVOL Portfolios Controlling for Past Returns
## Ang, Hodrick, Xing, Zhang (2006), "The Cross-Section of Volatility and Expected Returns"

Dependent double sorts controlling for past returns (momentum). Each formation
month, stocks are first sorted into quintiles on a past-return signal, then
within each momentum quintile into quintiles on IVOL; cell returns are
value-weighted and earned in month t+1. The five IVOL portfolios are averaged
(equal-weighted) across the five momentum quintiles (Panel A). Panel B reports
the full 5×5 past-12-month × IVOL grid of FF-3 alphas. Alphas in percent per
month; Newey–West(4) t-statistics in parentheses.

Past-return signals (relative to signal row t): past 1 month = ret_{t} (the
FORMATION-month return — portfolios are formed at the end of month t, so
"past 1-month return" includes month t; issue M3 convention); past 6 months =
cumret(t-6..t-1); past 12 months = cumret(t-12..t-1). The 6/12-month windows
include the most recent completed month (t-1), unlike the panel's `mom`
(= cumret(t-12..t-2), which skips t-1).

### Panel A: Controlling for Momentum (FF-3 alphas, %/month)

| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| Past 1 month (rep) | 0.11 | 0.06 | -0.01 | -0.20 | -1.15 | -1.25 |
| Past 1 month (paper) | 0.07 | 0.08 | 0.09 | -0.05 | -0.59 | -0.66 |
| Past 6 months (rep) | 0.01 | -0.11 | -0.25 | -0.41 | -1.12 | -1.13 |
| Past 6 months (paper) | -0.01 | -0.12 | -0.28 | -0.45 | -1.11 | -1.10 |
| Past 12 months (rep) | -0.08 | -0.15 | -0.33 | -0.52 | -1.15 | -1.06 |
| Past 12 months (paper) | 0.01 | -0.05 | -0.28 | -0.64 | -1.21 | -1.22 |

**Absolute differences (rep − paper):**

| Control | ΔQ1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| Past 1 month | 0.04 | -0.02 | -0.10 | -0.15 | -0.56 | -0.59 |
| Past 6 months | 0.02 | 0.01 | 0.03 | 0.04 | -0.01 | -0.03 |
| Past 12 months | -0.09 | -0.10 | -0.05 | 0.12 | 0.06 | 0.16 |

### Newey–West(4) t-statistics (replication, Panel A)

| Control | Q1 | Q2 | Q3 | Q4 | Q5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| Past 1 month | (2.48) | (1.22) | (-0.18) | (-2.17) | (-8.95) | (-8.85) |
| Past 6 months | (0.19) | (-1.59) | (-3.27) | (-4.58) | (-9.63) | (-7.82) |
| Past 12 months | (-1.18) | (-2.00) | (-4.26) | (-5.77) | (-10.95) | (-7.75) |

### Panel B: Past 12-Month Return × IVOL detail (5×5, FF-3 alphas, %/month)

| Quintile | IVOL 1 | 2 | 3 | 4 | 5 | 5-1 |
|---|---:|---:|---:|---:|---:|---:|
| Losers 1 (rep) | -0.59 | -1.08 | -1.57 | -2.20 | -3.28 | -2.69 |
| Losers 1 (paper) | -0.41 | -0.83 | -1.44 | -2.11 | -2.66 | -2.25 |
| 2 (rep) | -0.22 | -0.43 | -0.67 | -0.82 | -1.28 | -1.06 |
| 2 (paper) | -0.08 | -0.24 | -0.64 | -1.09 | -1.70 | -1.62 |
| 3 (rep) | -0.20 | -0.22 | -0.25 | -0.25 | -0.69 | -0.49 |
| 3 (paper) | -0.06 | -0.11 | -0.26 | -0.48 | -1.03 | -0.97 |
| 4 (rep) | 0.05 | 0.10 | 0.08 | 0.14 | -0.52 | -0.57 |
| 4 (paper) | 0.15 | 0.07 | 0.23 | -0.03 | -0.65 | -0.80 |
| Winners 5 (rep) | 0.54 | 0.86 | 0.76 | 0.52 | 0.03 | -0.52 |
| Winners 5 (paper) | 0.45 | 0.85 | 0.71 | 0.52 | -0.03 | -0.48 |

## Notes
- Average stocks/month (and # holding months) per momentum sort: Past 1 month=4742 (n_mo=450), Past 6 months=4533 (n_mo=444), Past 12 months=4331 (n_mo=438).
- Momentum windows need lookback before the panel's 1963-06 start, so the
  effective sample is shorter than July-1963: past-1 starts ~1963-08,
  past-6 ~1964-01, past-12 ~1964-07 (holding months). This is a data
  limitation (the panel starts at the first IVOL formation month).
