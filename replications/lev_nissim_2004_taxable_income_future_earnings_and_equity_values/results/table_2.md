# Table 2 — Cross-Sectional Regressions of Future Earnings Growth

G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + ε, two-digit SIC industry fixed effects, annual cross-sections, time-series mean (t = mean / std across years).

Our sample period: fyear 1987-2000 (pre-1987 sparse per assumption #6). Panel A: 1987-1992 (paper: 1973-1992). Panel B: 1993-2000 (paper: 1993-2000).

Each cell shows `mean(t-stat)`. R² and n are the time-series means of the per-year fit. Variables: β_1 = R_TAX coefficient, β_2 = R_DEF, β_3 = R_CFO.

## Panel A: Pre-SFAS 109 (1987-1992)

| Model | DepVar | β_1 R_TAX | β_2 R_DEF | β_3 R_CFO | R² | n | # years used |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 R_TAX | G1 | +0.467 ( 0.99) |   -     |   -     | 0.060 | 1244 | 6 |
| M1 R_TAX | G2 | +0.532 ( 0.90) |   -     |   -     | 0.064 | 1122 | 6 |
| M1 R_TAX | G3 | +0.703 ( 1.13) |   -     |   -     | 0.058 | 998 | 6 |
| M2 R_DEF | G1 |   -     | +1.602 ( 2.37) |   -     | 0.048 | 1724 | 5 |
| M2 R_DEF | G2 |   -     | +0.650 ( 0.79) |   -     | 0.046 | 1510 | 5 |
| M2 R_DEF | G3 |   -     | -0.499 (-0.30) |   -     | 0.055 | 1312 | 5 |
| M3 R_TAX+R_DEF | G1 | +0.450 ( 1.20) | -0.635 (-3.47) |   -     | 0.070 | 1125 | 5 |
| M3 R_TAX+R_DEF | G2 | +0.518 ( 1.61) | -0.694 (-2.71) |   -     | 0.073 | 1025 | 5 |
| M3 R_TAX+R_DEF | G3 | +0.790 ( 3.62) | -0.988 (-3.64) |   -     | 0.065 | 913 | 5 |
| M4 Full | G1 | +0.457 ( 1.33) | -0.621 (-2.56) | +0.312 ( 0.53) | 0.071 | 1076 | 5 |
| M4 Full | G2 | +0.505 ( 1.78) | -0.652 (-2.13) | +0.562 ( 0.89) | 0.076 | 982 | 5 |
| M4 Full | G3 | +0.806 ( 3.36) | -1.001 (-4.02) | +0.428 ( 0.46) | 0.069 | 875 | 5 |

## Panel B: Post-SFAS 109 (1993-2000)

| Model | DepVar | β_1 R_TAX | β_2 R_DEF | β_3 R_CFO | R² | n | # years used |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 R_TAX | G1 | +1.862 ( 2.69) |   -     |   -     | 0.064 | 1681 | 7 |
| M1 R_TAX | G2 | +2.594 ( 3.62) |   -     |   -     | 0.055 | 1405 | 5 |
| M1 R_TAX | G3 | +2.874 ( 3.50) |   -     |   -     | 0.054 | 1100 | 3 |
| M2 R_DEF | G1 |   -     | +0.918 ( 0.54) |   -     | 0.044 | 2481 | 7 |
| M2 R_DEF | G2 |   -     | -0.001 (-0.00) |   -     | 0.052 | 1912 | 5 |
| M2 R_DEF | G3 |   -     | -2.248 (-1.39) |   -     | 0.040 | 1429 | 3 |
| M3 R_TAX+R_DEF | G1 | +1.650 ( 3.57) | -1.246 (-1.09) |   -     | 0.068 | 1484 | 7 |
| M3 R_TAX+R_DEF | G2 | +2.381 ( 2.46) | -1.837 (-2.56) |   -     | 0.060 | 1225 | 5 |
| M3 R_TAX+R_DEF | G3 | +2.534 ( 8.70) | -1.122 (-1.05) |   -     | 0.061 | 962 | 3 |
| M4 Full | G1 | +1.718 ( 3.27) | -1.303 (-1.17) | +0.555 ( 1.52) | 0.074 | 1428 | 7 |
| M4 Full | G2 | +2.470 ( 2.48) | -1.845 (-2.56) | +0.661 ( 0.78) | 0.063 | 1181 | 5 |
| M4 Full | G3 | +2.639 ( 8.66) | -1.144 (-1.00) | +1.075 ( 1.23) | 0.064 | 930 | 3 |

## Paper-vs-replication spot checks

| Cell | Paper | Ours |
|---|---:|---:|
| T2_A R_TAX-only G1 β_1 (mean) | 0.354 | +0.467 |
| T2_A R_TAX-only G1 t-stat | 10.36 | +0.987 |
| T2_A R_TAX-only G3 β_1 (mean) | 0.545 | +0.703 |
| T2_A R_TAX-only G3 t-stat | 15.25 | +1.127 |
| T2_A Full-model G3 β_1 (mean) | 0.618 | +0.806 |
| T2_A Full-model G3 t-stat | 14.46 | +3.365 |
| T2_B R_TAX-only G1 β_1 (mean) | 0.534 | +1.862 |
| T2_B R_TAX-only G1 t-stat | 8.53 | +2.688 |
