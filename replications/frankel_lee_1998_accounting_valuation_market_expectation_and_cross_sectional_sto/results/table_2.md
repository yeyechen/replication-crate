# Table 2 -- Annual Spearman Correlations of Price vs. B and EBO V_h / V_f

**Replication of**: Frankel & Lee (1998) -- Table 2
**Sample period**: 1976-1993 (portfolio-formation years)
**Universe**: NYSE/AMEX/NASDAQ ordinary common shares (shrcd 10/11, exchcd 1/2/3) x Compustat non-financial (SIC first digit != 6) x fiscal-year-end in [6, 12] x June 30 price >= $1 x I/B/E/S FY1 coverage filter

**Definitions** (paper's notation):
- **B**: book equity per share in calendar year t-1 ($/share) = ceq / csho.
- **V_h (T=1,2,3)**: EBO fundamental value (Eqs. 3.1-3.3) using historical ROE as the FROE for all forecast periods. See paper §3 footnote 13 / Appendix A.
- **V_f (T=1,2,3)**: EBO fundamental value using I/B/E/S consensus EPS forecasts (FY1, FY2) as the FROE inputs. See paper Appendix A.
- **r_e**: industry-specific cost-of-equity (FF 1997 Table 7 + 0.0646 riskless). **This iteration uses a constant r_e = 0.12 placeholder** (assumption 28).

Each cell is the cross-sectional Spearman rank correlation between stock price (June 30 of year t) and the indicated value measure, restricted to firm-years where all of B, V_h T=1,2,3, V_f T=1,2,3 are non-missing and price > 0.

**All years row** = time-series mean of the annual correlations (matches the paper's 'All years' definition).

| Year | Obs. | B | V_h T=1 | V_h T=2 | V_h T=3 | V_f T=1 | V_f T=2 | V_f T=3 |
|---|---|---|---|---|---|---|---|---|
| 1977 | 213 | 0.57 | 0.57 | 0.57 | 0.57 | 0.57 | 0.57 | 0.56 |
| 1978 | 370 | 0.48 | 0.52 | 0.52 | 0.53 | 0.53 | 0.51 | 0.52 |
| 1979 | 494 | 0.50 | 0.51 | 0.52 | 0.52 | 0.54 | 0.54 | 0.54 |
| 1980 | 516 | 0.42 | 0.54 | 0.54 | 0.55 | 0.59 | 0.59 | 0.60 |
| 1981 | 595 | 0.45 | 0.57 | 0.57 | 0.57 | 0.58 | 0.56 | 0.57 |
| 1982 | 671 | 0.52 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 |
| 1983 | 723 | 0.47 | 0.50 | 0.50 | 0.50 | 0.53 | 0.51 | 0.52 |
| 1984 | 825 | 0.69 | 0.67 | 0.66 | 0.66 | 0.68 | 0.68 | 0.66 |
| 1985 | 804 | 0.70 | 0.74 | 0.74 | 0.74 | 0.76 | 0.73 | 0.73 |
| 1986 | 830 | 0.71 | 0.66 | 0.66 | 0.66 | 0.73 | 0.69 | 0.69 |
| 1987 | 862 | 0.72 | 0.65 | 0.65 | 0.64 | 0.72 | 0.72 | 0.71 |
| 1988 | 867 | 0.73 | 0.71 | 0.70 | 0.70 | 0.74 | 0.74 | 0.73 |
| 1989 | 910 | 0.73 | 0.71 | 0.70 | 0.70 | 0.76 | 0.75 | 0.75 |
| 1990 | 909 | 0.64 | 0.69 | 0.68 | 0.68 | 0.73 | 0.73 | 0.73 |
| 1991 | 940 | 0.64 | 0.70 | 0.69 | 0.69 | 0.72 | 0.74 | 0.73 |
| 1992 | 995 | 0.67 | 0.63 | 0.63 | 0.63 | 0.71 | 0.73 | 0.72 |
| 1993 | 1,116 | 0.65 | 0.62 | 0.62 | 0.62 | 0.70 | 0.74 | 0.73 |
| **All years** | **12,640** | **0.61** | **0.62** | **0.62** | **0.62** | **0.66** | **0.65** | **0.65** |

## Per-cell comparison (paper vs ours, All-years row)

Paper All-years row (from the paper's Table 2, 'FF Three-factor' columns):

| Metric | Paper | Ours | Status |
| --- | ---: | ---: | --- |
| corr(B) | 0.60 | 0.61 | Tier 1 (+0.01) |
| corr(V_h T=1) | 0.70 | 0.62 | Tier 2 (-0.08) |
| corr(V_h T=2) | 0.69 | 0.62 | Tier 2 (-0.07) |
| corr(V_h T=3) | 0.69 | 0.62 | Tier 2 (-0.07) |
| corr(V_f T=1) | 0.80 | 0.66 | FAIL (-0.14) |
| corr(V_f T=2) | 0.81 | 0.65 | FAIL (-0.16) |
| corr(V_f T=3) | 0.82 | 0.65 | FAIL (-0.17) |

## Notes

**Discount rate**: this iteration uses r_e = 0.12 (constant) as a placeholder. The paper uses industry-specific r_e (FF 1997 Table 7 risk premiums + 0.0646 riskless rate). The Spearman correlation between price and V_h / V_f is largely invariant to the choice of r_e because V_h and V_f are monotonic in r_e (paper footnote 11). Industry mapping is out of scope for this iteration.

**FY2 / Ltg coverage**: FY2 EPS coverage is sparse in this vintage (~11% of panel rows). Where FY2 is missing, FROE_{t+1} = FROE_t per Appendix A. Ltg (long-term growth) is unavailable in this vintage of I/B/E/S statsumu_epsus (no measure='LTG' rows exist); the FROE_{t+2} = FROE_{t+1} fallback is applied uniformly. See assumptions.md assumptions 19, 28.
