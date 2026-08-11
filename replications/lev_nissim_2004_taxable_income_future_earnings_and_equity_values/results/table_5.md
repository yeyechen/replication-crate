# Table 5 — Cross-Sectional Regressions of One-Year-Ahead Stock Returns

R = α_indu + β_1 SIZE + β_2 B/P + β_3 E/P + β_4 BETA + β_5 VOL + β_6 R_TAX + β_7 R_DEF + β_8 R_CFO + ε
two-digit SIC industry fixed effects, annual cross-sections, time-series mean (t = mean / std across years).

Dependent variable: one-year buy-and-hold return from May of (t+1) to April of (t+2). Winsorization applied to X only (rule 27: stock returns not winsorized).

Our sample period: fyear 1987-2000 (pre-1987 sparse per assumption #6). Panel A: 1987-1992 (paper: 1973-1992). Panel B: 1993-2000 (paper: 1993-2000).

**Assumption #9**: BETA, VOL are unavailable. Model 3 (M2 + BETA + VOL) falls back to M2. **Assumption #10**: Delisting reinvestment not implemented; uses raw cum_ret.

Each cell shows `mean(t-stat)`. R² and n are the time-series means of the per-year fit. Variables: β_1 = R_TAX, β_2 = R_DEF, β_3 = R_CFO, β_4 = SIZE (log April ME), β_5 = B/P, β_6 = E/P.

## Panel A: Pre-SFAS 109 (1987-1992)

| Model | β R_TAX | β R_DEF | β R_CFO | β SIZE | β B/P | β E/P | R² | n | # years used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 (R_* only) | +0.007 ( 1.86) | -0.005 (-0.29) | +0.008 ( 0.55) |   -     |   -     |   -     | 0.101 | 1016 | 5 |
| M2 (M1+SIZE+B/P+E/P) | +0.007 ( 1.38) | -0.009 (-0.50) | +0.008 ( 0.65) | -0.008 (-0.78) | -0.023 (-0.28) | +0.000 ( 0.00) | 0.111 | 1015 | 5 |

## Panel B: Post-SFAS 109 (1993-2000)

| Model | β R_TAX | β R_DEF | β R_CFO | β SIZE | β B/P | β E/P | R² | n | # years used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 (R_* only) | +0.003 ( 0.12) | -0.003 (-0.13) | +0.033 ( 2.21) |   -     |   -     |   -     | 0.105 | 1391 | 8 |
| M2 (M1+SIZE+B/P+E/P) | +0.005 ( 0.19) | -0.006 (-0.29) | +0.032 ( 2.07) | -0.010 (-0.34) | +0.002 ( 0.03) | +0.000 ( 0.02) | 0.116 | 1390 | 8 |

## Paper-vs-replication spot checks

| Cell | Paper | Ours |
|---|---:|---:|
| T5_A R_TAX spec 1 β (mean) | +0.013 | +0.007 |
| T5_A R_TAX spec 1 t-stat | +3.913 | +1.861 |
| T5_A R_TAX spec 2 β (mean) | +0.014 | +0.007 |
| T5_A R_TAX spec 2 t-stat | +3.851 | +1.376 |
| T5_A mean n | 978 | 1,015 |
| T5_A R² spec 1 | 0.155 | 0.101 |
| T5_B R_TAX spec 1 β (mean) | +0.003 | +0.003 |
| T5_B R_TAX spec 1 t-stat | +0.673 | +0.119 |
| T5_B R_TAX spec 2 β (mean) | +0.003 | +0.005 |
| T5_B R_TAX spec 2 t-stat | +0.486 | +0.187 |
| T5_B mean n | 1378 | 1,390 |
