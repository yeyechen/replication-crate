# Table 3 — Cross-Sectional Regressions with Nine Earnings Predictors

G = α_indu + β_1 R_TAX + β_2 R_DEF + β_3 R_CFO + γ_1 PRED_1 + ... + γ_9 PRED_9 + ε

Two-digit SIC industry fixed effects, annual cross-sections, time-series mean (t = mean / std across years).

Our sample period: fyear 1987-2000 (pre-1987 sparse per assumption #6). Panel A: 1987-1992 (paper: 1973-1992). Panel B: 1993-2000 (paper: 1993-2000).

Per footnote 25, the nine PRED coefficients are omitted from the published table for parsimony. We report only β_1 (R_TAX), β_2 (R_DEF), β_3 (R_CFO), R², and n. The PRED_1..PRED_9 definitions are below.

**PRED_1..PRED_9 definitions (paper footnote 25):**

- PRED_1: ratio of earnings to total assets = ib / at
- PRED_2: current period earnings change / at = (ib - ib_{t-1}) / at
- PRED_3: avg change in earnings over last 3 years / at = ((ib - ib_{t-3}) / 3) / at
- PRED_4: avg change in earnings over last 5 years / at = ((ib - ib_{t-5}) / 5) / at
- PRED_5: dividends / total assets = dv / at
- PRED_6: R&D / sales = xrd / sale
- PRED_7: capex / sales = capx / sale
- PRED_8: earnings-price ratio (FYE, percentage points) = 100 × ib / (prcc_f × csho)
- PRED_9: book-to-market = ceq / (prcc_f × csho)

## Panel A: Pre-SFAS 109 (1987-1992)

| Model | DepVar | β_1 R_TAX | β_2 R_DEF | β_3 R_CFO | R² | n | # years used |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 R_TAX | G1 | +0.467 ( 0.99) |   -     |   -     | 0.060 | 1244 | 6 |
| M1 R_TAX | G3 | +0.703 ( 1.13) |   -     |   -     | 0.058 | 998 | 6 |
| M2 R_DEF | G1 |   -     | +1.602 ( 2.37) |   -     | 0.048 | 1724 | 5 |
| M2 R_DEF | G3 |   -     | -0.499 (-0.30) |   -     | 0.055 | 1312 | 5 |
| M3 R_TAX+R_DEF | G1 | +0.450 ( 1.20) | -0.635 (-3.47) |   -     | 0.070 | 1125 | 5 |
| M3 R_TAX+R_DEF | G3 | +0.790 ( 3.62) | -0.988 (-3.64) |   -     | 0.065 | 913 | 5 |
| M4 Full | G1 | +0.097 (  -  ) | +0.485 (  -  ) | +0.484 (  -  ) | 0.349 | 432 | 1 |
| M4 Full | G3 | +0.397 (  -  ) | -0.613 (  -  ) | +0.933 (  -  ) | 0.275 | 350 | 1 |

## Panel B: Post-SFAS 109 (1993-2000)

| Model | DepVar | β_1 R_TAX | β_2 R_DEF | β_3 R_CFO | R² | n | # years used |
|---|---|---:|---:|---:|---:|---:|---:|
| M1 R_TAX | G1 | +1.862 ( 2.69) |   -     |   -     | 0.064 | 1681 | 7 |
| M1 R_TAX | G3 | +2.874 ( 3.50) |   -     |   -     | 0.054 | 1100 | 3 |
| M2 R_DEF | G1 |   -     | +0.918 ( 0.54) |   -     | 0.044 | 2481 | 7 |
| M2 R_DEF | G3 |   -     | -2.248 (-1.39) |   -     | 0.040 | 1429 | 3 |
| M3 R_TAX+R_DEF | G1 | +1.650 ( 3.57) | -1.246 (-1.09) |   -     | 0.068 | 1484 | 7 |
| M3 R_TAX+R_DEF | G3 | +2.534 ( 8.70) | -1.122 (-1.05) |   -     | 0.061 | 962 | 3 |
| M4 Full | G1 | -0.653 (-0.25) | -0.456 (-0.70) | +0.837 ( 1.08) | 0.452 | 479 | 7 |
| M4 Full | G3 | -0.739 (-0.21) | +0.687 ( 0.22) | +1.818 ( 1.21) | 0.217 | 341 | 3 |

## Paper-vs-replication spot checks

| Cell | Paper | Ours |
|---|---:|---:|
| T3_A R_TAX-only G1 β_1 (mean) | 0.160 | +0.467 |
| T3_A R_TAX-only G1 t-stat | 4.905 | +0.987 |
| T3_A R_TAX-only G3 β_1 (mean) | 0.223 | +0.703 |
| T3_A R_TAX-only G3 t-stat | 5.166 | +1.127 |
| T3_A Full-model G3 β_1 (mean) | 0.222 | +0.397 |
| T3_A Full-model G3 t-stat | 4.016 |  -  |
| T3_A Full-model G3 β_3 (R_CFO) | 0.201 | +0.933 |
| T3_B R_TAX-only G1 β_1 (mean) | 0.278 | +1.862 |
| T3_B R_TAX-only G1 t-stat | 4.454 | +2.688 |
| T3_B R_TAX-only G3 β_1 (mean) | 0.495 | +2.874 |
| T3_B R_TAX-only G3 t-stat | 10.993 | +3.502 |
| T3_B Full-model G3 β_1 (mean) | 0.516 | -0.739 |
| T3_B Full-model G3 t-stat | 6.442 | -0.207 |
| T3_B Full-model G3 β_3 (R_CFO) | 0.322 | +1.818 |
