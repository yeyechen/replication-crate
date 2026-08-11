# Table 1 -- Annual Summary Statistics

**Replication of**: Frankel & Lee (1998) -- Table 1
**Sample period**: 1976-1993 (portfolio-formation years)
**Universe**: NYSE/AMEX/NASDAQ ordinary common shares (shrcd 10/11, exchcd 1/2/3) x Compustat non-financial (SIC first digit != 6) x fiscal-year-end in [6, 12] x June 30 price >= $1

**Filters applied** (in order):
1. CRSP shrcd IN (10, 11) AND exchcd IN (1, 2, 3) -- PIT at June 30 of year t.
2. Compustat non-financial: SIC first digit NOT = 6 (funda.sich with company.sic fallback).
3. Fiscal-year-end month (fyr) in [6, 12].
4. Fiscal year ending in calendar year t-1 has non-missing ceq, ib, dvc, at.
5. CRSP price at June 30 of year t exists and abs(prc) >= 1.
6. |ROE| < 1, 0 <= k <= 1, ceq > 0.
7. I/B/E/S FY1 coverage: each (gvkey, fyear=year_t-1) has a one-year-ahead EPS forecast in the May statpers of year t (fpi='2', fpedats in year_t+1, measure='EPS', meanest non-missing). Compustat CUSIP (first 8 chars) / ticker / oftic linked to IBES CUSIP / ticker (union of three IBES id identifiers).

**Definitions** (paper's notation):
- **No. firm**: count of (permno, year_t) firm-years.
- **ME**: market equity at June 30 of year t in millions of dollars = abs(prc) * shrout / 1000.
- **k**: payout ratio = dvc / ib (or dvc / (0.06 * at) when ib <= 0), clipped to [0, 1].
- **ROE**: ib / ((B_t + B_{t-1}) / 2), where B = ceq (Compustat Item 60).
- **B**: book equity per share in dollars = ceq / csho (Compustat csho, unit-adjusted). ceq is in millions of dollars, csho is in millions of shares.
- **P/B**: stock price at June 30 / book equity per share.
- **1/(Avg B/P)**: reciprocal of the average B/P ratio.
- **ROA**: ib / at.

Each annual cell is the equally-weighted mean across firm-years in that year.

**Total firm-years (All years row)**: 21,707

| Year | No. firm | Avg ME | Avg k | Avg ROE | Avg B | Avg P/B | 1/(Avg B/P) | Avg ROA |
|---|---|---|---|---|---|---|---|---|
| 1976 | 354 | 844 | 0.349 | 0.144 | 21.83 | 1.89 | 1.29 | 0.075 |
| 1977 | 295 | 887 | 0.296 | 0.168 | 22.08 | 1.61 | 1.22 | 0.084 |
| 1978 | 509 | 598 | 0.312 | 0.163 | 21.66 | 1.53 | 1.13 | 0.078 |
| 1979 | 690 | 537 | 0.286 | 0.175 | 21.06 | 1.53 | 1.12 | 0.081 |
| 1980 | 762 | 588 | 0.290 | 0.180 | 21.21 | 1.51 | 1.01 | 0.082 |
| 1981 | 903 | 615 | 0.299 | 0.166 | 20.20 | 1.77 | 1.22 | 0.076 |
| 1982 | 1,016 | 446 | 0.303 | 0.153 | 18.57 | 1.41 | 0.93 | 0.072 |
| 1983 | 1,152 | 653 | 0.320 | 0.117 | 17.26 | 2.48 | 1.60 | 0.059 |
| 1984 | 1,415 | 471 | 0.247 | 0.107 | 14.54 | 1.94 | 1.33 | 0.053 |
| 1985 | 1,390 | 555 | 0.217 | 0.125 | 13.35 | 2.12 | 1.45 | 0.060 |
| 1986 | 1,393 | 763 | 0.233 | 0.091 | 13.53 | 2.51 | 1.69 | 0.044 |
| 1987 | 1,531 | 830 | 0.213 | 0.087 | 11.70 | 2.63 | 1.78 | 0.038 |
| 1988 | 1,555 | 738 | 0.196 | 0.105 | 10.86 | 2.41 | 1.65 | 0.043 |
| 1989 | 1,569 | 823 | 0.193 | 0.126 | 11.28 | 2.40 | 1.66 | 0.056 |
| 1990 | 1,615 | 815 | 0.200 | 0.117 | 10.68 | 2.49 | 1.53 | 0.054 |
| 1991 | 1,646 | 842 | 0.215 | 0.106 | 10.66 | 2.34 | 1.42 | 0.048 |
| 1992 | 1,841 | 843 | 0.219 | 0.073 | 10.07 | 2.47 | 1.48 | 0.034 |
| 1993 | 2,071 | 889 | 0.192 | 0.077 | 8.88 | 2.82 | 1.79 | 0.031 |
| **All years** | **21,707** | **726** | **0.236** | **0.115** | **13.60** | **2.25** | **1.44** | **0.053** |

## Per-cell comparison (paper vs ours, All-years row)

Paper All-years row (L298-299 of the paper, replicated by us from the paper):

| Metric | Paper | Ours | Diff |
| --- | ---: | ---: | ---: |
| No. firm    | 18,162  | 21,707  | +3,545 |
| Avg ME      | 1,167   | 726   | -441 |
| Avg k       | 0.27  | 0.24  | -0.03 |
| Avg ROE     | 0.13  | 0.11  | -0.02 |
| Avg B       | 16.87 | 13.60 | -3.27 |
| Avg P/B     | 2.18 | 2.25 | +0.07 |
| Avg ROA     | 0.06  | 0.05  | -0.01 |

## Notes

**Universe size after I/B/E/S coverage filter**: the panel has 21,707 firm-years after the CUSIP/ticker/oftic union-based I/B/E/S FY1 coverage filter (vs the paper's 18,162). The ~20% overage relative to the paper is attributable to (a) the I/B/E/S data vintage -- the post-1998 I/B/E/S database has slightly more records than the 1998 vintage the paper used; and (b) the FY1-only filter -- the paper also requires FY2 coverage, but the I/B/E/S data in this vintage has zero FY2 records in May pre-1984 and only sparse coverage 1984-1993, so we use FY1 only (see assumptions.md assumption 17/19). The per-year pattern matches the paper: growth from ~360 firms in 1976 to ~1,600-2,000 in 1993, with the IBES filter disproportionately dropping early years where analyst coverage was sparse.
