# Table VII — Returns across EW-index market states (LSV 1994)

> Window (M2): bounded to May 1968-Apr 1994 = 312 months (the last month any cohort is within its 5-year holding window; the prior Apr-1995 bound let ~8 P_122 + ~2 N_88 months reuse the 1989 cohort at Year +5.5/+6, which the paper's portfolio definitions forbid). In this window the EW index has 124 negative / 188 positive months. Semantic partition: W_25=25, N_88=88, P_122=122, B_25=25, unclassified=52 (these counts differ from the paper's 260-month 25/88/122/25 totals because the paper's exact EW window is not recoverable; the semantic rule is preserved). An in-horizon assertion (mnum <= (fy+5)*12+4 for every classified month) is enforced in code.

States (semantic, over the bounded window): W_25 = 25 worst, N_88 = next 88 worst, B_25 = 25 best, P_122 = 122 best moderate-positives (positive ex-best-25); remainder unclassified. Active cohort per month = most recent April formation. 1A = C/PxGS cells; 1B = B/M deciles (pooled (9,10)-(1,2) spread). 3 decimals.

## Panel 1A — C/P x GS cells (state-mean monthly return)

| State | EW idx | (CP1,GS1) | (CP1,GS2) | (CP1,GS3) | (CP2,GS1) | (CP2,GS2) | (CP2,GS3) | (CP3,GS1) | (CP3,GS2) | (CP3,GS3) |
|---|---|---|---|---|---|---|---|---|---|---|
| W_25 | -0.104 | -0.109 | -0.096 | -0.124 | -0.089 | -0.090 | -0.115 | -0.086 | -0.082 | -0.114 |
| N_88 | -0.029 | -0.026 | -0.026 | -0.039 | -0.019 | -0.023 | -0.035 | -0.019 | -0.020 | -0.032 |
| P_122 | 0.044 | 0.046 | 0.049 | 0.052 | 0.044 | 0.045 | 0.050 | 0.044 | 0.043 | 0.046 |
| B_25 | 0.121 | 0.132 | 0.100 | 0.128 | 0.106 | 0.096 | 0.128 | 0.116 | 0.104 | 0.131 |

## Panel 1B — B/M deciles + pooled spread (state-mean monthly return)

| State | EW idx | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | spread | t-stat |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| W_25 | -0.104 | -0.110 | -0.110 | -0.105 | -0.100 | -0.095 | -0.095 | -0.091 | -0.087 | -0.097 | -0.106 | 0.009 | 1.822 |
| N_88 | -0.029 | -0.033 | -0.030 | -0.029 | -0.028 | -0.026 | -0.025 | -0.024 | -0.022 | -0.023 | -0.028 | 0.006 | 1.782 |
| P_122 | 0.044 | 0.051 | 0.050 | 0.048 | 0.048 | 0.046 | 0.045 | 0.042 | 0.043 | 0.044 | 0.046 | -0.006 | -1.954 |
| B_25 | 0.121 | 0.112 | 0.109 | 0.112 | 0.106 | 0.102 | 0.105 | 0.109 | 0.112 | 0.126 | 0.158 | 0.032 | 2.104 |
