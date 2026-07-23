# Table I — Average monthly returns of relative-strength strategies

> PRIMARY = UNADJUSTED (raw daily-compound, no dlret) returns per the Assumption A3-revision (inner iteration 3); the delisting-adjusted series is retained as a sensitivity only (see REPORT.md).

Jegadeesh & Titman (1993), Table I. Sample: Jan 1965 – Dec 1989 (300 months).
Each cell: average monthly return, with the iid t-statistic beneath it.
Sell = decile 1 (past losers), Buy = decile 10 (past winners), Buy - Sell = zero-cost.
Signal: cumret_J_raw; holding returns: ret_raw. Panel A: portfolios formed immediately after the lagged returns are measured.
Panel B: 1-week skip — holding month 1 uses ret_skip5_raw, later months ret_raw (Assumption A4).
t-statistics: mean / (std / sqrt(300)), plain iid (Assumption A5).

## Panel A — formed immediately after the lagged returns are measured

| Lag J | Portfolio  | K = 3 | K = 6 | K = 9 | K = 12 |
|------:|------------|:-----:|:-----:|:-----:|:------:|
| 3 | Sell | 0.0111<br>(2.22) | 0.0091<br>(1.89) | 0.0091<br>(1.93) | 0.0086<br>(1.86) |
| 3 | Buy | 0.0134<br>(3.44) | 0.0144<br>(3.66) | 0.0149<br>(3.73) | 0.0153<br>(3.81) |
| 3 | Buy - Sell | 0.0023<br>(0.83) | 0.0053<br>(2.18) | 0.0057<br>(2.63) | 0.0067<br>(3.58) |
| 6 | Sell | 0.0093<br>(1.79) | 0.0081<br>(1.62) | 0.0074<br>(1.52) | 0.0081<br>(1.69) |
| 6 | Buy | 0.0163<br>(4.12) | 0.0169<br>(4.22) | 0.0171<br>(4.23) | 0.0163<br>(4.06) |
| 6 | Buy - Sell | 0.0070<br>(2.08) | 0.0088<br>(2.91) | 0.0098<br>(3.71) | 0.0082<br>(3.31) |
| 9 | Sell | 0.0084<br>(1.61) | 0.0067<br>(1.34) | 0.0073<br>(1.46) | 0.0083<br>(1.67) |
| 9 | Buy | 0.0179<br>(4.45) | 0.0182<br>(4.45) | 0.0173<br>(4.23) | 0.0162<br>(3.98) |
| 9 | Buy - Sell | 0.0095<br>(2.66) | 0.0115<br>(3.68) | 0.0100<br>(3.40) | 0.0079<br>(2.84) |
| 12 | Sell | 0.0066<br>(1.27) | 0.0068<br>(1.34) | 0.0076<br>(1.50) | 0.0089<br>(1.75) |
| 12 | Buy | 0.0188<br>(4.59) | 0.0178<br>(4.34) | 0.0168<br>(4.10) | 0.0156<br>(3.82) |
| 12 | Buy - Sell | 0.0123<br>(3.58) | 0.0110<br>(3.36) | 0.0091<br>(2.95) | 0.0067<br>(2.27) |

## Panel B — formed 1 week after the lagged returns are measured

| Lag J | Portfolio  | K = 3 | K = 6 | K = 9 | K = 12 |
|------:|------------|:-----:|:-----:|:-----:|:------:|
| 3 | Sell | 0.0056<br>(1.27) | 0.0064<br>(1.41) | 0.0073<br>(1.61) | 0.0073<br>(1.61) |
| 3 | Buy | 0.0125<br>(3.43) | 0.0140<br>(3.66) | 0.0146<br>(3.74) | 0.0151<br>(3.82) |
| 3 | Buy - Sell | 0.0069<br>(2.91) | 0.0076<br>(3.42) | 0.0072<br>(3.57) | 0.0078<br>(4.43) |
| 6 | Sell | 0.0045<br>(0.98) | 0.0057<br>(1.21) | 0.0058<br>(1.24) | 0.0069<br>(1.48) |
| 6 | Buy | 0.0149<br>(4.02) | 0.0162<br>(4.18) | 0.0167<br>(4.21) | 0.0160<br>(4.04) |
| 6 | Buy - Sell | 0.0104<br>(3.63) | 0.0105<br>(3.78) | 0.0109<br>(4.40) | 0.0091<br>(3.83) |
| 9 | Sell | 0.0039<br>(0.84) | 0.0044<br>(0.94) | 0.0058<br>(1.21) | 0.0071<br>(1.49) |
| 9 | Buy | 0.0163<br>(4.33) | 0.0174<br>(4.40) | 0.0168<br>(4.19) | 0.0158<br>(3.95) |
| 9 | Buy - Sell | 0.0124<br>(4.12) | 0.0130<br>(4.53) | 0.0110<br>(3.97) | 0.0086<br>(3.26) |
| 12 | Sell | 0.0026<br>(0.56) | 0.0048<br>(1.01) | 0.0063<br>(1.29) | 0.0079<br>(1.60) |
| 12 | Buy | 0.0171<br>(4.47) | 0.0169<br>(4.27) | 0.0162<br>(4.05) | 0.0151<br>(3.78) |
| 12 | Buy - Sell | 0.0145<br>(4.92) | 0.0121<br>(4.00) | 0.0099<br>(3.37) | 0.0073<br>(2.56) |

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| PA J6/K6 sell | 0.008110 | 0.0079 | +2.7% |
| PA J6/K6 sell t | 1.615090 | 1.56 | +3.5% |
| PA J6/K6 buy | 0.016908 | 0.0174 | -2.8% |
| PA J6/K6 buy t | 4.218487 | 4.33 | -2.6% |
| PA J6/K6 buy-sell  [CENTRAL CELL] | 0.008797 | 0.0095 | -7.4% |
| PA J6/K6 buy-sell t | 2.908658 | 3.07 | -5.3% |
| PA J12/K3 buy-sell | 0.012297 | 0.0131 | -6.1% |
| PA J12/K3 buy-sell t | 3.580941 | 3.74 | -4.3% |
| PB J12/K3 buy-sell | 0.014534 | 0.0149 | -2.5% |
| PB J12/K3 buy-sell t | 4.917711 | 4.28 | +14.9% |
| PA J3/K3 buy-sell | 0.002333 | 0.0032 | -27.1% |
| PA J3/K3 buy-sell t | 0.825522 | 1.1 | -25.0% |
| PA J6/K9 buy-sell | 0.009763 | 0.0102 | -4.3% |
| PA J6/K9 buy-sell t | 3.707034 | 3.76 | -1.4% |
| PB J6/K6 buy-sell | 0.010469 | 0.011 | -4.8% |
| PB J6/K6 buy-sell t | 3.782016 | 3.61 | +4.8% |
| PA J9/K6 buy-sell | 0.011531 | 0.0121 | -4.7% |
| PA J9/K6 buy-sell t | 3.682803 | 3.78 | -2.6% |

## Diagnostics

- PA 6/6 buy-sell monthly std: 0.052387 (paper-implied from 0.0095*sqrt(300)/3.07 ≈ 0.0537)
- PA 6/6 buy: mean=0.016908, std=0.069421 (paper: 0.0174, ≈0.0697)
- PA 6/6 sell: mean=0.008110, std=0.086976 (paper: 0.0079, ≈0.0868)
- Formation cohorts per J: J3=759, J6=756, J9=753, J12=750 (762 panel months minus warm-up; identical for A/B; pre-1965 cohorts are included in these counts but never enter the 1965-01..1989-12 Table I strategy window)
- Cohort counts: every (panel, J, K) grid has exactly K contributing cohorts in all 300 months (min = max = K, sell & buy deciles)
- J=3: avg stocks in decile 1 = 220.2, decile 10 = 219.3 (ranking on cumret_3_raw)
- J=6: avg stocks in decile 1 = 217.3, decile 10 = 216.4 (ranking on cumret_6_raw)
- J=9: avg stocks in decile 1 = 214.5, decile 10 = 213.6 (ranking on cumret_9_raw)
- J=12: avg stocks in decile 1 = 211.6, decile 10 = 210.7 (ranking on cumret_12_raw)

Hand-computed cohort (formation 1979-12, J=6, Panel A, h=1, RAW columns):
[hand-check] formation 1979-12, J=6 (signal=cumret_6_raw, holding=ret_raw): N=2205 ranked stocks
    decile  1: n= 221  cumret_6_raw cutoff [-0.556701, -0.175977]  next-month (1980-01) EW ret: hand=+0.111969 pipeline=+0.111969  match=True  (non-null ret_raw: 219/221)
    decile 10: n= 220  cumret_6_raw cutoff [+0.487298, +2.947377]  next-month (1980-01) EW ret: hand=+0.123485 pipeline=+0.123485  match=True  (non-null ret_raw: 215/220)

Ranking stability (A3-revision): % of stocks changing decile when ranked on cumret_J_raw instead of cumret_J (adjusted), formation 1979-12:
- J=3: 4/2220 stocks changed decile (0.18%)
- J=6: 4/2205 stocks changed decile (0.18%)
- J=9: 7/2185 stocks changed decile (0.32%)
- J=12: 6/2174 stocks changed decile (0.28%)

**Per-cell evaluation:** 192 cells — 192 Tier 1 / 0 Tier 2 / 0 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
