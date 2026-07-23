# Table III — Returns to buying winners and selling losers within size and beta subsamples

Jegadeesh & Titman (1993), Table III. 6-month/6-month strategy, Jan 1965 – Dec 1989. Each cell: average monthly return (Panel A) or market-model alpha (Panel B), with the t-statistic beneath. Columns: All, size terciles S1 (small) .. S3 (large), Scholes-Williams beta terciles β1 (low) .. β3 (high). PRIMARY = RAW series (A3-revision): signal cumret_6_raw, holding ret_raw; deciles formed WITHIN each group at each formation month (floor-rank, ties by permno). The All column is bit-identical to the Table I PA 6/6 decile series (max|diff| = 0.0, asserted).

- Size groups (A7): monthly terciles of formation-month me_millions (stocks with cumret_6_raw AND me_millions non-NULL), as in Table IV.
- Beta groups (A8): monthly terciles of prior-year Scholes-Williams daily beta (beta_SW = (β_lead + 2·β_0 + β_lag)/2; src/sql/sw_beta_yearly.sql; n ≥ 50 index-paired days per slope, else NULL — P17). First eligible formation is 1965-01 (1964 formations would need 1963 betas), so the beta groups report n = 299 months (1965-02..1989-12; months 1965-02..1965-06 average 1..5 overlapping cohorts); All/S groups: 300 months.
- Panel A F-stat: Wald F that the ten decile means are jointly EQUAL (stacked decile returns on intercept + 9 dummies). Panel B: alphas from OLS of (r_p − rf) on a constant and (r_m − rf) (A9; rf = ff 1-month T-bill, market = CRSP VW); the P10−P1 alpha regresses the zero-cost return WITHOUT an rf subtraction (zero investment; equals α10 − α1, matching the paper's exact P10−P1 = P10 − P1 arithmetic — P18). F-stat tests the ten decile coefficients in the no-intercept stacked excess-return regression. p-values in parentheses; p-values are NOT metrics (contract note).

## Panel A — Average monthly returns

| Portfolio | All | S1 (small) | S2 (medium) | S3 (large) | β1 (low β) | β2 (medium β) | β3 (high β) |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P1 (decile 1) | +0.0081<br>(+1.62) | +0.0075<br>(+1.24) | +0.0068<br>(+1.46) | +0.0095<br>(+2.58) | +0.0141<br>(+3.15) | +0.0093<br>(+1.98) | +0.0047<br>(+0.83) |
| P2 (decile 2) | +0.0115<br>(+2.83) | +0.0107<br>(+2.11) | +0.0115<br>(+2.83) | +0.0110<br>(+3.46) | +0.0142<br>(+4.34) | +0.0128<br>(+3.36) | +0.0080<br>(+1.64) |
| P3 (decile 3) | +0.0128<br>(+3.42) | +0.0137<br>(+2.90) | +0.0136<br>(+3.53) | +0.0113<br>(+3.79) | +0.0143<br>(+4.84) | +0.0137<br>(+3.80) | +0.0099<br>(+2.16) |
| P4 (decile 4) | +0.0130<br>(+3.69) | +0.0151<br>(+3.33) | +0.0139<br>(+3.72) | +0.0112<br>(+3.83) | +0.0140<br>(+5.05) | +0.0137<br>(+3.97) | +0.0107<br>(+2.38) |
| P5 (decile 5) | +0.0134<br>(+3.96) | +0.0152<br>(+3.50) | +0.0145<br>(+4.04) | +0.0115<br>(+4.04) | +0.0143<br>(+5.22) | +0.0141<br>(+4.20) | +0.0120<br>(+2.75) |
| P6 (decile 6) | +0.0141<br>(+4.22) | +0.0162<br>(+3.80) | +0.0154<br>(+4.33) | +0.0109<br>(+3.85) | +0.0144<br>(+5.26) | +0.0149<br>(+4.43) | +0.0123<br>(+2.87) |
| P7 (decile 7) | +0.0140<br>(+4.24) | +0.0158<br>(+3.77) | +0.0153<br>(+4.27) | +0.0116<br>(+4.08) | +0.0148<br>(+5.34) | +0.0150<br>(+4.50) | +0.0128<br>(+3.00) |
| P8 (decile 8) | +0.0148<br>(+4.38) | +0.0164<br>(+3.91) | +0.0159<br>(+4.37) | +0.0117<br>(+4.07) | +0.0151<br>(+5.33) | +0.0150<br>(+4.42) | +0.0136<br>(+3.18) |
| P9 (decile 9) | +0.0156<br>(+4.39) | +0.0170<br>(+3.98) | +0.0162<br>(+4.29) | +0.0132<br>(+4.33) | +0.0162<br>(+5.26) | +0.0165<br>(+4.71) | +0.0142<br>(+3.23) |
| P10 (decile 10) | +0.0169<br>(+4.22) | +0.0157<br>(+3.50) | +0.0180<br>(+4.29) | +0.0166<br>(+4.63) | +0.0181<br>(+4.90) | +0.0171<br>(+4.41) | +0.0151<br>(+3.28) |
| P10 − P1 | +0.0088<br>(+2.91) | +0.0082<br>(+2.40) | +0.0112<br>(+4.25) | +0.0071<br>(+2.88) | +0.0040<br>(+1.35) | +0.0078<br>(+2.78) | +0.0104<br>(+3.13) |
| F-stat | 0.41<br>(0.932) | 0.41<br>(0.929) | 0.63<br>(0.769) | 0.38<br>(0.947) | 0.16<br>(0.997) | 0.35<br>(0.959) | 0.47<br>(0.895) |

## Panel B — Market-model intercepts (alphas)

| Portfolio | All | S1 (small) | S2 (medium) | S3 (large) | β1 (low β) | β2 (medium β) | β3 (high β) |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| P1 (decile 1) | -0.0025<br>(-0.77) | -0.0034<br>(-0.73) | -0.0039<br>(-1.44) | -0.0005<br>(-0.29) | +0.0043<br>(+1.34) | -0.0010<br>(-0.34) | -0.0066<br>(-1.79) |
| P2 (decile 2) | +0.0015<br>(+0.63) | +0.0004<br>(+0.10) | +0.0013<br>(+0.61) | +0.0014<br>(+1.19) | +0.0052<br>(+2.48) | +0.0031<br>(+1.37) | -0.0029<br>(-1.05) |
| P3 (decile 3) | +0.0030<br>(+1.49) | +0.0037<br>(+1.09) | +0.0036<br>(+1.81) | +0.0019<br>(+2.01) | +0.0056<br>(+3.08) | +0.0040<br>(+2.11) | -0.0009<br>(-0.38) |
| P4 (decile 4) | +0.0033<br>(+1.90) | +0.0051<br>(+1.62) | +0.0039<br>(+2.17) | +0.0018<br>(+2.21) | +0.0053<br>(+3.45) | +0.0041<br>(+2.43) | -0.0001<br>(-0.02) |
| P5 (decile 5) | +0.0038<br>(+2.47) | +0.0053<br>(+1.80) | +0.0047<br>(+2.77) | +0.0022<br>(+3.00) | +0.0056<br>(+3.79) | +0.0045<br>(+2.94) | +0.0012<br>(+0.61) |
| P6 (decile 6) | +0.0044<br>(+3.13) | +0.0063<br>(+2.24) | +0.0055<br>(+3.41) | +0.0016<br>(+2.39) | +0.0056<br>(+3.99) | +0.0052<br>(+3.67) | +0.0016<br>(+0.85) |
| P7 (decile 7) | +0.0044<br>(+3.21) | +0.0060<br>(+2.14) | +0.0054<br>(+3.38) | +0.0023<br>(+3.56) | +0.0060<br>(+4.16) | +0.0053<br>(+3.85) | +0.0020<br>(+1.12) |
| P8 (decile 8) | +0.0051<br>(+3.62) | +0.0065<br>(+2.40) | +0.0059<br>(+3.69) | +0.0024<br>(+3.54) | +0.0062<br>(+4.35) | +0.0053<br>(+3.71) | +0.0029<br>(+1.57) |
| P9 (decile 9) | +0.0057<br>(+3.65) | +0.0070<br>(+2.57) | +0.0061<br>(+3.53) | +0.0037<br>(+4.34) | +0.0072<br>(+4.27) | +0.0067<br>(+4.37) | +0.0033<br>(+1.74) |
| P10 (decile 10) | +0.0067<br>(+3.28) | +0.0055<br>(+1.92) | +0.0076<br>(+3.53) | +0.0066<br>(+4.42) | +0.0085<br>(+3.89) | +0.0070<br>(+3.50) | +0.0042<br>(+1.81) |
| P10 − P1 | +0.0092<br>(+3.06) | +0.0089<br>(+2.61) | +0.0115<br>(+4.37) | +0.0071<br>(+2.90) | +0.0042<br>(+1.40) | +0.0081<br>(+2.88) | +0.0107<br>(+3.22) |
| F-stat | 4.55<br>(0.000) | 3.80<br>(0.000) | 5.24<br>(0.000) | 4.27<br>(0.000) | 8.57<br>(0.000) | 5.69<br>(0.000) | 1.92<br>(0.038) |

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| P1_all_pA | 0.008110 | 0.0079 | +2.7% |
| P1_all_pA_t | 1.615090 | 1.56 | +3.5% |
| P10_all_pA | 0.016908 | 0.0174 | -2.8% |
| P10_all_pA_t | 4.218487 | 4.33 | -2.6% |
| P10-1_all_pA | 0.008797 | 0.0095 | -7.4% |
| P10-1_all_pA_t | 2.908658 | 3.07 | -5.3% |
| P1_s1_pA | 0.007529 | 0.0083 | -9.3% |
| P1_s1_pA_t | 1.236689 | 1.35 | -8.4% |
| P10-1_s2_pA | 0.011174 | 0.0126 | -11.3% |
| P10-1_s2_pA_t | 4.245787 | 4.57 | -7.1% |
| P10-1_s3_pA | 0.007053 | 0.0075 | -6.0% |
| P10-1_s3_pA_t | 2.882678 | 3.03 | -4.9% |
| P1_b1_pA | 0.014078 | 0.0129 | +9.1% |
| P1_b1_pA_t | 3.152347 | 2.92 | +8.0% |
| P10-1_b1_pA | 0.004001 | 0.0062 | -35.5% |
| P10-1_b1_pA_t | 1.350527 | 2.05 | -34.1% |
| P10-1_b3_pA | 0.010420 | 0.0108 | -3.5% |
| P10-1_b3_pA_t | 3.131452 | 3.35 | -6.5% |
| f_stat_all_pA | 0.406328 | 2.83 | -85.6% |
| f_stat_b3_pA | 0.471352 | 1.69 | -72.1% |
| P1_all_pB | -0.002542 | -0.003 | +15.3% |
| P1_all_pB_t | -0.770444 | -0.89 | +13.4% |
| P10_all_pB | 0.006704 | 0.007 | -4.2% |
| P10_all_pB_t | 3.280383 | 3.24 | +1.2% |
| P10-1_all_pB | 0.009246 | 0.01 | -7.5% |
| P10-1_all_pB_t | 3.063140 | 3.23 | -5.2% |
| P10-1_s1_pB | 0.008853 | 0.0106 | -16.5% |
| P10-1_s1_pB_t | 2.610591 | 2.97 | -12.1% |
| P10-1_b3_pB | 0.010747 | 0.0111 | -3.2% |
| P10-1_b3_pB_t | 3.224642 | 3.42 | -5.7% |
| P10_b1_pB | 0.008478 | 0.0094 | -9.8% |
| P10_b1_pB_t | 3.890189 | 4.1 | -5.1% |
| f_stat_all_pB | 4.547558 | 5.291 | -14.1% |
| f_stat_s2_pB | 5.238379 | 8.3713 | -37.4% |

## Diagnostics

### Scholes-Williams betas (src/sql/sw_beta_yearly.sql)

- SW beta coverage: 59,033 of 60,225 (permno, year) rows have a non-NULL beta (98.02%; the 1,192 NULLs are stock-years with < 50 valid index-paired trading days, P17)
- Median beta by year: min across years = 0.717 (1988), max = 1.612 (1969)

| beta_year | stocks | with beta | median beta |
|----------:|-------:|----------:|------------:|
| 1964 | 2,118 | 2,089 | 0.932 |
| 1965 | 2,168 | 2,129 | 1.242 |
| 1966 | 2,195 | 2,158 | 1.175 |
| 1967 | 2,231 | 2,188 | 1.135 |
| 1968 | 2,259 | 2,189 | 1.385 |
| 1969 | 2,319 | 2,262 | 1.612 |
| 1970 | 2,376 | 2,340 | 1.527 |
| 1971 | 2,464 | 2,411 | 1.549 |
| 1972 | 2,588 | 2,537 | 1.225 |
| 1973 | 2,608 | 2,576 | 1.270 |
| 1974 | 2,577 | 2,542 | 0.972 |
| 1975 | 2,515 | 2,480 | 1.112 |
| 1976 | 2,489 | 2,464 | 1.138 |
| 1977 | 2,465 | 2,437 | 1.006 |
| 1978 | 2,417 | 2,373 | 1.301 |
| 1979 | 2,352 | 2,299 | 1.240 |
| 1980 | 2,316 | 2,259 | 0.952 |
| 1981 | 2,315 | 2,252 | 0.969 |
| 1982 | 2,246 | 2,205 | 0.905 |
| 1983 | 2,212 | 2,164 | 0.957 |
| 1984 | 2,223 | 2,175 | 0.987 |
| 1985 | 2,177 | 2,122 | 0.887 |
| 1986 | 2,168 | 2,107 | 0.942 |
| 1987 | 2,154 | 2,108 | 1.046 |
| 1988 | 2,184 | 2,131 | 0.717 |
| 1989 | 2,089 | 2,036 | 0.766 |

- Footnote-11 cross-check (EW monthly stock return within prior-year beta terciles, time-series mean 1965-01..1989-12; paper: low 1.48% / medium 1.39% / high 1.16%):
    - beta tercile 1 (low): ours 1.53% vs paper 1.48% (dev +3.2%)
    - beta tercile 2 (medium): ours 1.42% vs paper 1.39% (dev +2.4%)
    - beta tercile 3 (high): ours 1.08% vs paper 1.16% (dev -6.6%)
    - months covered: 300 of 300; stocks/month with a prior-year beta: n=300 mean=2133.476667 median=2083.000000 std=179.001176 min=1815.000000 max=2501.000000 p1=1832.940000 p99=2474.030000

### Group sizes (members per formation month, deciles formed within)

| group | formation months | avg members/month | avg members/decile |
|-------|-----------------:|------------------:|-------------------:|
| All | 756 | 1406.7 | 140.7 |
| S1 (small) | 756 | 467.6 | 46.8 |
| S2 (medium) | 756 | 467.3 | 46.7 |
| S3 (large) | 756 | 466.9 | 46.7 |
| β1 (low β) | 300 | 713.1 | 71.3 |
| β2 (medium β) | 300 | 712.8 | 71.3 |
| β3 (high β) | 300 | 712.5 | 71.2 |

Months entering the statistics: All n=300, S1 (small) n=300, S2 (medium) n=300, S3 (large) n=300, β1 (low β) n=300, β2 (medium β) n=300, β3 (high β) n=300 (beta groups start 1965-02 — 1965-01 has zero beta-eligible cohorts, P17).

**Per-cell evaluation:** 322 cells — 294 Tier 1 / 22 Tier 2 / 6 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
