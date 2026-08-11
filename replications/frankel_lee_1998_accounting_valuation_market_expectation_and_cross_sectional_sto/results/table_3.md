# Table 3 -- Characteristics of Quintile Portfolios (ME, B/P, V_f/P)

**Replication of**: Frankel & Lee (1998) -- Table 3
**Sample period**: 1977-1992 (paper's Table 3 caption)
**Universe**: NYSE/AMEX/NASDAQ ordinary common shares x Compustat non-financial x fiscal-year-end in [6, 12] x June 30 price >= $1 x I/B/E/S FY1 coverage

Each firm-year is assigned to a quintile by the indicated sort variable. Quintile breakpoints are computed annually: Panel A uses NYSE-only firms' ME; Panels B, C, D use in-sample breakpoints. ME is market equity at June 30 of year t (in $M); B/P and V_f/P use book equity per share in calendar year t-1 and the EBO V_f value (T=3, FY1+FY2 forecasts), respectively. Ret12/24/36 are buy-and-hold returns for 12/24/36 months beginning July of year t. Q5-Q1 Diff. is the difference in means between the top (Q5) and bottom (Q1) quintiles; the paper's significance stars are not reproduced (assumption 20).

## Panel A - ME (NYSE size quintiles)

Total firm-years in panel: **10,319**

|  | Q1 (Low) | Q2 | Q3 | Q4 | Q5 (High) | All Firms | Q5-Q1 Diff. |
|---|---|---|---|---|---|---|---|
| ME | 66 | 235 | 496 | 1,061 | 4,748 | 817 | +4,682 |
| B/P | 0.795 | 0.653 | 0.678 | 0.720 | 0.650 | 0.724 | -0.145 |
| V_f/P | 1.314 | 1.152 | 1.130 | 1.103 | 1.127 | 1.204 | -0.187 |
| Ret12 | 0.137 | 0.158 | 0.156 | 0.151 | 0.140 | 0.146 | +0.003 |
| Ret24 | 0.258 | 0.287 | 0.286 | 0.301 | 0.273 | 0.275 | +0.016 |
| Ret36 | 0.418 | 0.481 | 0.479 | 0.478 | 0.441 | 0.450 | +0.023 |
| Obs. | 4,283 | 2,075 | 1,499 | 1,294 | 1,168 | 10,319 |  |

## Panel B - ME (in-sample size quintiles)

Total firm-years in panel: **10,319**

|  | Q1 (Low) | Q2 | Q3 | Q4 | Q5 (High) | All Firms | Q5-Q1 Diff. |
|---|---|---|---|---|---|---|---|
| ME | 34 | 93 | 208 | 524 | 3,220 | 817 | +3,186 |
| B/P | 0.896 | 0.737 | 0.658 | 0.669 | 0.658 | 0.724 | -0.238 |
| V_f/P | 1.492 | 1.241 | 1.135 | 1.101 | 1.070 | 1.204 | -0.421 |
| Ret12 | 0.170 | 0.130 | 0.148 | 0.138 | 0.141 | 0.146 | -0.029 |
| Ret24 | 0.305 | 0.247 | 0.273 | 0.270 | 0.280 | 0.275 | -0.025 |
| Ret36 | 0.503 | 0.403 | 0.440 | 0.454 | 0.447 | 0.450 | -0.055 |
| Obs. | 2,070 | 2,061 | 2,059 | 2,061 | 2,068 | 10,319 |  |

## Panel C - B/P quintiles

Total firm-years in panel: **10,319**

|  | Q1 (Low) | Q2 | Q3 | Q4 | Q5 (High) | All Firms | Q5-Q1 Diff. |
|---|---|---|---|---|---|---|---|
| ME | 927 | 843 | 966 | 776 | 673 | 837 | -254 |
| B/P | 0.250 | 0.453 | 0.644 | 0.860 | 1.409 | 0.723 | +1.160 |
| V_f/P | 1.142 | 1.136 | 1.207 | 1.226 | 1.300 | 1.204 | +0.158 |
| Ret12 | 0.129 | 0.134 | 0.142 | 0.160 | 0.163 | 0.146 | +0.034 |
| Ret24 | 0.216 | 0.253 | 0.293 | 0.300 | 0.314 | 0.275 | +0.098 |
| Ret36 | 0.352 | 0.397 | 0.463 | 0.505 | 0.531 | 0.450 | +0.179 |
| Obs. | 2,070 | 2,061 | 2,059 | 2,061 | 2,068 | 10,319 |  |

## Panel D - V_f/P quintiles

Total firm-years in panel: **9,718**

|  | Q1 (Low) | Q2 | Q3 | Q4 | Q5 (High) | All Firms | Q5-Q1 Diff. |
|---|---|---|---|---|---|---|---|
| ME | 643 | 1,261 | 1,007 | 852 | 598 | 872 | -45 |
| B/P | 0.684 | 0.640 | 0.741 | 0.809 | 0.814 | 0.738 | +0.131 |
| V_f/P | 0.485 | 0.835 | 1.024 | 1.263 | 2.396 | 1.201 | +1.911 |
| Ret12 | 0.145 | 0.138 | 0.171 | 0.145 | 0.137 | 0.147 | -0.008 |
| Ret24 | 0.237 | 0.277 | 0.305 | 0.294 | 0.267 | 0.276 | +0.030 |
| Ret36 | 0.391 | 0.446 | 0.501 | 0.476 | 0.471 | 0.457 | +0.080 |
| Obs. | 1,950 | 1,939 | 1,944 | 1,939 | 1,946 | 9,718 |  |

## Per-cell comparison vs paper (Q5-Q1 Diff., All-years)

Paper Q5-Q1 Diff values (All-years column; All Firms row):

| Panel | Metric | Paper | Ours | Status |
| --- | --- | ---: | ---: | --- |
| Panel A - ME (NYSE size quintiles) | B/P | -0.770 | -0.145 | FAIL (+0.625) |
| Panel A - ME (NYSE size quintiles) | V_f/P | -0.420 | -0.187 | FAIL (+0.233) |
| Panel A - ME (NYSE size quintiles) | Ret12 | -0.233 | +0.003 | FAIL (+0.236) |
| Panel A - ME (NYSE size quintiles) | Ret24 | -0.210 | +0.016 | FAIL (+0.226) |
| Panel A - ME (NYSE size quintiles) | Ret36 | -0.338 | +0.023 | FAIL (+0.361) |
| Panel B - ME (in-sample size quintiles) | B/P | -0.320 | -0.238 | Tier 1 (+0.082) |
| Panel B - ME (in-sample size quintiles) | V_f/P | -0.050 | -0.421 | FAIL (-0.371) |
| Panel B - ME (in-sample size quintiles) | Ret12 | +0.001 | -0.029 | Tier 1 (-0.030) |
| Panel B - ME (in-sample size quintiles) | Ret24 | +0.045 | -0.025 | Tier 2 (-0.070) |
| Panel B - ME (in-sample size quintiles) | Ret36 | +0.066 | -0.055 | FAIL (-0.121) |
| Panel C - B/P quintiles | V_f/P | +0.260 | +0.158 | Tier 2 (-0.102) |
| Panel C - B/P quintiles | Ret12 | +0.049 | +0.034 | Tier 1 (-0.015) |
| Panel C - B/P quintiles | Ret24 | +0.082 | +0.098 | Tier 1 (+0.016) |
| Panel C - B/P quintiles | Ret36 | +0.151 | +0.179 | Tier 1 (+0.028) |
| Panel D - V_f/P quintiles | B/P | +0.250 | +0.131 | Tier 2 (-0.119) |
| Panel D - V_f/P quintiles | Ret12 | +0.031 | -0.008 | Tier 1 (-0.039) |
| Panel D - V_f/P quintiles | Ret24 | +0.152 | +0.030 | FAIL (-0.122) |
| Panel D - V_f/P quintiles | Ret36 | +0.306 | +0.080 | FAIL (-0.226) |

## Notes

**NYSE-only breakpoints (Panel A)**: Panel A uses breakpoints computed from NYSE-only firms (exchcd=1) per FF (1992, 1993). When a firm's exchange code is missing or the NYSE subset is too small, we fall back to in-sample breakpoints.

**Beta**: per the task spec, beta is skipped in this iteration. The paper estimates beta using monthly returns over the next 36 months (post-formation). Beta is in Table 3 Panel A-D but does not drive a claim; it is included for completeness in a future iteration.
