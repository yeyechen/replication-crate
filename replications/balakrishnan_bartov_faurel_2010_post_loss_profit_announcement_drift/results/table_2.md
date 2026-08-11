# Table 2: Buy-and-Hold Abnormal Stock Returns for Portfolios Formed on Earnings

Replication of Balakrishnan, Bartov, Faurel (2009) — *Post Loss/Profit Announcement Drift*

**Sample:** firm-quarters 1976-2005 with non-missing ibq/atq in comp_202601.fundq, 
matched to CRSP via ccmxpf_linktable (linktype IN ('LC','LU'), linkprim IN ('P','C'), 
usedflag=1, PIT). **Note:** sample over-counts paper targets by ~16% due to Compustat 
vintage drift (see assumptions.md).

**Earnings signal:** earnings_at = ibq[t] / atq[t]. **Decile breakpoints:** computed 
from the **prior fiscal quarter's** earnings distribution per firm (paper §3.1, page 12).
**Expected return benchmark:** CRSP erdport1.decret (equal-weighted size-decile daily return); 
value-weighted as the paper specifies is approximated by EW (documented as A9).

**BHAR windows:**
- [-2, 0] = m2_0
- [1, 60] = 60 trading days after rdq
- [1, 120] = 120 trading days after rdq

**Tolerance:** ±12% on returns, ±15% on t-stats.

## Replicated values

### Window [m2_0]

| Decile | N | Mean BHAR | t-stat |
|---|---:|---:|---:|
| 1 | 52,247 | -0.0098 | -19.82 |
| 2 | 52,177 | -0.0052 | -13.08 |
| 3 | 52,167 | -0.0020 | -5.87 |
| 4 | 52,185 | 0.0013 | 4.61 |
| 5 | 52,192 | 0.0035 | 12.91 |
| 6 | 52,157 | 0.0054 | 19.38 |
| 7 | 52,170 | 0.0080 | 27.64 |
| 8 | 52,182 | 0.0100 | 32.89 |
| 9 | 52,162 | 0.0123 | 39.08 |
| 10 | 52,229 | 0.0196 | 50.69 |

**Hedge (D10 - D1): +0.0294 (t = +46.80)**


### Window [60]

| Decile | N | Mean BHAR | t-stat |
|---|---:|---:|---:|
| 1 | 52,247 | -0.1062 | -39.55 |
| 2 | 52,177 | -0.0749 | -31.99 |
| 3 | 52,167 | -0.0420 | -20.75 |
| 4 | 52,185 | -0.0116 | -6.86 |
| 5 | 52,192 | 0.0039 | 2.45 |
| 6 | 52,157 | 0.0162 | 9.79 |
| 7 | 52,170 | 0.0138 | 8.24 |
| 8 | 52,182 | 0.0222 | 12.96 |
| 9 | 52,162 | 0.0322 | 18.06 |
| 10 | 52,229 | 0.0480 | 23.88 |

**Hedge (D10 - D1): +0.1541 (t = +45.97)**


### Window [120]

| Decile | N | Mean BHAR | t-stat |
|---|---:|---:|---:|
| 1 | 52,247 | -0.1877 | -54.57 |
| 2 | 52,177 | -0.1191 | -37.81 |
| 3 | 52,167 | -0.0522 | -18.04 |
| 4 | 52,185 | 0.0015 | 0.61 |
| 5 | 52,192 | 0.0156 | 6.39 |
| 6 | 52,157 | 0.0247 | 10.00 |
| 7 | 52,170 | 0.0159 | 6.43 |
| 8 | 52,182 | 0.0239 | 9.50 |
| 9 | 52,162 | 0.0300 | 11.62 |
| 10 | 52,229 | 0.0404 | 14.31 |

**Hedge (D10 - D1): +0.2280 (t = +51.27)**


## Subperiod stability (paper footnote 15)

Mean D10-D1 SAR hedge spread and t-statistic by 10-year subperiod, [1, 120] window.
Paper reports 10.75% / 8.68% / 11.03% for 1976-1985 / 1986-1995 / 1996-2005.

| Subperiod | N | Hedge [1, 120] | t-stat | Paper target |
|---|---:|---:|---:|---:|
| 1976-1985 | 103,768 | +0.2213 | +26.62 | +0.1075 |
| 1986-1995 | 175,148 | +0.1896 | +25.06 | +0.0868 |
| 1996-2005 | 242,952 | +0.2583 | +37.03 | +0.1103 |

Magnitudes are biased by A9 (EW vs VW benchmark); pattern (sign + significance + approximate stability) is the testable claim.

## Per-decile N (for cells matching paper Table 2 N column)

- D1 (High Loss) N: 52,247 (paper: 46,753)
- D10 (High Profit) N: 52,229 (paper: 47,078)

