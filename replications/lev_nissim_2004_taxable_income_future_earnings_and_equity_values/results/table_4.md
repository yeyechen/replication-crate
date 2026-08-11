# Table 4 — Cross-Sectional Regressions of E/P*

E/P* = α_indu + β_1 GROW + β_2 LNTA + β_3 BETA + β_4 VOL + β_5 LEV + β_6 PAY + β_7 R_TAX + β_8 R_DEF + β_9 R_CFO + ε
two-digit SIC industry fixed effects, annual cross-sections, time-series mean (t = mean / std across years).

Our sample period: fyear 1987-2000 (pre-1987 sparse per assumption #6). Panel A: 1987-1992 (paper: 1973-1992). Panel B: 1993-2000 (paper: 1993-2000).

**Assumption #9**: BETA, VOL, GROW are unavailable in this iteration. Model 2 (M1 + GROW) and Model 4 (M3 + BETA + VOL) are skipped or fall back to M1 / M3. See assumptions.md.

Each cell shows `mean(t-stat)`. R² and n are the time-series means of the per-year fit. Variables: β_1 = R_TAX, β_2 = R_DEF, β_3 = R_CFO, β_4 = LNTA (ln ME at FYE), β_5 = LEV, β_6 = PAY.

## Panel A: Pre-SFAS 109 (1987-1992)

| Model | β R_TAX | β R_DEF | β R_CFO | β LNTA | β LEV | β PAY | R² | n | # years used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 (R_* only) | -0.212 (-1.75) | +0.122 ( 0.85) | -0.410 (-2.60) |   -     |   -     |   -     | 0.152 | 1022 | 5 |
| M3 (M1+LNTA+LEV+PAY) | -0.157 (-1.51) | -0.018 (-0.13) | -0.423 (-2.21) | -0.309 (-3.09) | +3.445 ( 2.49) | -0.447 (-2.42) | 0.197 | 1014 | 5 |

## Panel B: Post-SFAS 109 (1993-2000)

| Model | β R_TAX | β R_DEF | β R_CFO | β LNTA | β LEV | β PAY | R² | n | # years used |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1 (R_* only) | -0.512 (-2.84) | +0.138 ( 1.30) | -0.452 (-2.17) |   -     |   -     |   -     | 0.156 | 1406 | 8 |
| M3 (M1+LNTA+LEV+PAY) | -0.324 (-2.66) | -0.048 (-0.70) | -0.458 (-1.95) | -0.660 (-1.76) | +3.700 ( 2.04) | -0.722 (-2.74) | 0.231 | 1392 | 8 |

## Paper-vs-replication spot checks

| Cell | Paper | Ours |
|---|---:|---:|
| T4_A R_TAX spec 1 β (mean) | -0.083 | -0.212 |
| T4_A R_TAX spec 1 t-stat | -1.364 | -1.748 |
| T4_A R_TAX spec 3 β (mean) | -0.063 | -0.157 |
| T4_A R_TAX spec 3 t-stat | -0.814 | -1.515 |
| T4_A mean n | 535 | 1,014 |
| T4_B R_TAX spec 1 β (mean) | -0.288 | -0.512 |
| T4_B R_TAX spec 1 t-stat | -11.349 | -2.844 |
| T4_B R_TAX spec 3 β (mean) | -0.212 | -0.324 |
| T4_B R_TAX spec 3 t-stat | -8.483 | -2.657 |
| T4_B mean n | 911 | 1,392 |
