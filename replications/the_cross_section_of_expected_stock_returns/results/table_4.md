# Table IV — Fama & French (1992), The Cross-Section of Expected Stock Returns

Properties of the portfolios formed at the end of **December of year t−1** on **BE/ME** (Panel A, 12 portfolios) and on **E/P** (Panel B, 13 portfolios; portfolio 0 = stocks with negative earnings). Portfolios 2–9 cover deciles of the ranking variable; 1A/1B split the bottom decile and 10A/10B split the top decile. BE/ME and E/P breakpoints are the ranked values of the variable for **all** stocks satisfying the CRSP–COMPUSTAT data requirements (L1382). Equal-weighted; sample July 1963 – December 1990 (330 months; 28 formation years, 1963–1990).

**Averaging conventions (paper notes L1384/L1386, same as Table II).** *Return*: time-series average (over the 330 months) of the monthly equal-weighted portfolio return ×100 (monthly EW = mean of valid stock returns in the portfolio that month). *β*: mean of the stock-level post-ranking βs (each stock carries the full-period post-ranking β of its size×pre-β cell, assigned each June) over members each month, then time-series mean. *ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P dummy, E(+)/P*: mean of the stock-level firm-year value over the members present each month, then time-series mean over the 330 months. *Firms*: mean over months of the number of assigned members per month (panel rows per (month, portfolio), counted regardless of return validity).

## Panel A — portfolios formed on BE/ME (December t−1)

### Replicated values

| Portfolio | 1A | 1B | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10A | 10B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Return | 0.41 | 0.72 | 0.79 | 0.97 | 0.97 | 1.11 | 1.26 | 1.46 | 1.48 | 1.58 | 1.72 | 1.79 |
| β | 1.36 | 1.35 | 1.32 | 1.29 | 1.27 | 1.27 | 1.26 | 1.26 | 1.28 | 1.31 | 1.33 | 1.35 |
| ln(ME) | 4.58 | 4.61 | 4.64 | 4.51 | 4.47 | 4.33 | 4.18 | 4.02 | 3.74 | 3.43 | 2.93 | 2.57 |
| ln(BE/ME) | -2.14 | -1.38 | -0.98 | -0.67 | -0.45 | -0.27 | -0.10 | 0.06 | 0.23 | 0.44 | 0.68 | 1.09 |
| ln(A/ME) | -1.16 | -0.64 | -0.27 | 0.06 | 0.31 | 0.48 | 0.64 | 0.78 | 0.97 | 1.17 | 1.40 | 1.85 |
| ln(A/BE) | 0.98 | 0.74 | 0.72 | 0.73 | 0.75 | 0.75 | 0.74 | 0.72 | 0.74 | 0.73 | 0.72 | 0.76 |
| E/P dummy | 0.29 | 0.16 | 0.11 | 0.09 | 0.09 | 0.09 | 0.09 | 0.10 | 0.12 | 0.16 | 0.25 | 0.35 |
| E(+)/P | 0.03 | 0.05 | 0.06 | 0.08 | 0.09 | 0.10 | 0.11 | 0.11 | 0.12 | 0.12 | 0.11 | 0.12 |
| Firms | 123 | 123 | 246 | 246 | 246 | 246 | 245 | 245 | 246 | 245 | 123 | 123 |

### Comparison with paper

**Pass/fail: 92/108 targeted cells pass**.  Largest relative deviations: ln(A/ME) 3: ours 0.06 vs paper -0.05 (|Δ| 0.109, 217.4%); ln(BE/ME) 7: ours 0.06 vs paper 0.03 (|Δ| 0.031, 103.1%); ln(A/ME) 4: ours 0.31 vs paper 0.20 (|Δ| 0.107, 53.3%).

| Row | Port | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Return | 1A | 0.30 | 0.41 | 0.106 | 25% | ❌ FAIL |
| Return | 1B | 0.67 | 0.72 | 0.053 | 25% | ✅ pass |
| Return | 2 | 0.87 | 0.79 | 0.080 | 25% | ✅ pass |
| Return | 3 | 0.97 | 0.97 | 0.001 | 25% | ✅ pass |
| Return | 4 | 1.04 | 0.97 | 0.068 | 25% | ✅ pass |
| Return | 5 | 1.17 | 1.11 | 0.064 | 25% | ✅ pass |
| Return | 6 | 1.30 | 1.26 | 0.044 | 25% | ✅ pass |
| Return | 7 | 1.44 | 1.46 | 0.017 | 25% | ✅ pass |
| Return | 8 | 1.50 | 1.48 | 0.016 | 25% | ✅ pass |
| Return | 9 | 1.59 | 1.58 | 0.013 | 25% | ✅ pass |
| Return | 10A | 1.92 | 1.72 | 0.195 | 25% | ✅ pass |
| Return | 10B | 1.83 | 1.79 | 0.036 | 25% | ✅ pass |
| β | 1A | 1.36 | 1.36 | 0.005 | 15% | ✅ pass |
| β | 1B | 1.34 | 1.35 | 0.007 | 15% | ✅ pass |
| β | 2 | 1.32 | 1.32 | 0.002 | 15% | ✅ pass |
| β | 3 | 1.30 | 1.29 | 0.006 | 15% | ✅ pass |
| β | 4 | 1.28 | 1.27 | 0.010 | 15% | ✅ pass |
| β | 5 | 1.27 | 1.27 | 0.002 | 15% | ✅ pass |
| β | 6 | 1.27 | 1.26 | 0.005 | 15% | ✅ pass |
| β | 7 | 1.27 | 1.26 | 0.006 | 15% | ✅ pass |
| β | 8 | 1.27 | 1.28 | 0.007 | 15% | ✅ pass |
| β | 9 | 1.29 | 1.31 | 0.019 | 15% | ✅ pass |
| β | 10A | 1.33 | 1.33 | 0.004 | 15% | ✅ pass |
| β | 10B | 1.35 | 1.35 | 0.003 | 15% | ✅ pass |
| ln(ME) | 1A | 4.53 | 4.58 | 0.046 | 10% | ✅ pass |
| ln(ME) | 1B | 4.67 | 4.61 | 0.055 | 10% | ✅ pass |
| ln(ME) | 2 | 4.69 | 4.64 | 0.053 | 10% | ✅ pass |
| ln(ME) | 3 | 4.56 | 4.51 | 0.048 | 10% | ✅ pass |
| ln(ME) | 4 | 4.47 | 4.47 | 0.003 | 10% | ✅ pass |
| ln(ME) | 5 | 4.38 | 4.33 | 0.051 | 10% | ✅ pass |
| ln(ME) | 6 | 4.23 | 4.18 | 0.047 | 10% | ✅ pass |
| ln(ME) | 7 | 4.06 | 4.02 | 0.044 | 10% | ✅ pass |
| ln(ME) | 8 | 3.85 | 3.74 | 0.113 | 10% | ✅ pass |
| ln(ME) | 9 | 3.51 | 3.43 | 0.082 | 10% | ✅ pass |
| ln(ME) | 10A | 3.06 | 2.93 | 0.134 | 10% | ✅ pass |
| ln(ME) | 10B | 2.65 | 2.57 | 0.076 | 10% | ✅ pass |
| ln(BE/ME) | 1A | -2.22 | -2.14 | 0.081 | 10% | ✅ pass |
| ln(BE/ME) | 1B | -1.51 | -1.38 | 0.132 | 10% | ✅ pass |
| ln(BE/ME) | 2 | -1.09 | -0.98 | 0.107 | 10% | ✅ pass |
| ln(BE/ME) | 3 | -0.75 | -0.67 | 0.079 | 10% | ❌ FAIL |
| ln(BE/ME) | 4 | -0.51 | -0.45 | 0.063 | 10% | ❌ FAIL |
| ln(BE/ME) | 5 | -0.32 | -0.27 | 0.054 | 10% | ❌ FAIL |
| ln(BE/ME) | 6 | -0.14 | -0.10 | 0.037 | 10% | ❌ FAIL |
| ln(BE/ME) | 7 | 0.03 | 0.06 | 0.031 | 10% | ❌ FAIL |
| ln(BE/ME) | 8 | 0.21 | 0.23 | 0.022 | 10% | ❌ FAIL |
| ln(BE/ME) | 9 | 0.42 | 0.44 | 0.023 | 10% | ✅ pass |
| ln(BE/ME) | 10A | 0.66 | 0.68 | 0.019 | 10% | ✅ pass |
| ln(BE/ME) | 10B | 1.02 | 1.09 | 0.073 | 10% | ✅ pass |
| ln(A/ME) | 1A | -1.24 | -1.16 | 0.083 | 10% | ✅ pass |
| ln(A/ME) | 1B | -0.79 | -0.64 | 0.153 | 10% | ❌ FAIL |
| ln(A/ME) | 2 | -0.40 | -0.27 | 0.132 | 10% | ❌ FAIL |
| ln(A/ME) | 3 | -0.05 | 0.06 | 0.109 | 10% | ❌ FAIL |
| ln(A/ME) | 4 | 0.20 | 0.31 | 0.107 | 10% | ❌ FAIL |
| ln(A/ME) | 5 | 0.40 | 0.48 | 0.083 | 10% | ❌ FAIL |
| ln(A/ME) | 6 | 0.56 | 0.64 | 0.077 | 10% | ❌ FAIL |
| ln(A/ME) | 7 | 0.71 | 0.78 | 0.073 | 10% | ❌ FAIL |
| ln(A/ME) | 8 | 0.91 | 0.97 | 0.057 | 10% | ✅ pass |
| ln(A/ME) | 9 | 1.12 | 1.17 | 0.051 | 10% | ✅ pass |
| ln(A/ME) | 10A | 1.35 | 1.40 | 0.051 | 10% | ✅ pass |
| ln(A/ME) | 10B | 1.75 | 1.85 | 0.101 | 10% | ✅ pass |
| ln(A/BE) | 1A | 0.94 | 0.98 | 0.042 | 10% | ✅ pass |
| ln(A/BE) | 1B | 0.71 | 0.74 | 0.030 | 10% | ✅ pass |
| ln(A/BE) | 2 | 0.68 | 0.72 | 0.035 | 10% | ✅ pass |
| ln(A/BE) | 3 | 0.70 | 0.73 | 0.030 | 10% | ✅ pass |
| ln(A/BE) | 4 | 0.71 | 0.75 | 0.044 | 10% | ✅ pass |
| ln(A/BE) | 5 | 0.71 | 0.75 | 0.039 | 10% | ✅ pass |
| ln(A/BE) | 6 | 0.70 | 0.74 | 0.040 | 10% | ✅ pass |
| ln(A/BE) | 7 | 0.68 | 0.72 | 0.043 | 10% | ✅ pass |
| ln(A/BE) | 8 | 0.70 | 0.74 | 0.035 | 10% | ✅ pass |
| ln(A/BE) | 9 | 0.70 | 0.73 | 0.028 | 10% | ✅ pass |
| ln(A/BE) | 10A | 0.70 | 0.72 | 0.022 | 10% | ✅ pass |
| ln(A/BE) | 10B | 0.73 | 0.76 | 0.028 | 10% | ✅ pass |
| E/P dummy | 1A | 0.29 | 0.29 | 0.004 | 30% | ✅ pass |
| E/P dummy | 1B | 0.15 | 0.16 | 0.011 | 30% | ✅ pass |
| E/P dummy | 2 | 0.10 | 0.11 | 0.009 | 30% | ✅ pass |
| E/P dummy | 3 | 0.08 | 0.09 | 0.010 | 30% | ✅ pass |
| E/P dummy | 4 | 0.08 | 0.09 | 0.007 | 30% | ✅ pass |
| E/P dummy | 5 | 0.08 | 0.09 | 0.009 | 30% | ✅ pass |
| E/P dummy | 6 | 0.09 | 0.09 | 0.004 | 30% | ✅ pass |
| E/P dummy | 7 | 0.09 | 0.10 | 0.010 | 30% | ✅ pass |
| E/P dummy | 8 | 0.11 | 0.12 | 0.008 | 30% | ✅ pass |
| E/P dummy | 9 | 0.15 | 0.16 | 0.013 | 30% | ✅ pass |
| E/P dummy | 10A | 0.22 | 0.25 | 0.032 | 30% | ✅ pass |
| E/P dummy | 10B | 0.36 | 0.35 | 0.013 | 30% | ✅ pass |
| E(+)/P | 1A | 0.03 | 0.03 | 0.002 | 30% | ✅ pass |
| E(+)/P | 1B | 0.04 | 0.05 | 0.007 | 30% | ✅ pass |
| E(+)/P | 2 | 0.06 | 0.06 | 0.003 | 30% | ✅ pass |
| E(+)/P | 3 | 0.08 | 0.08 | 0.001 | 30% | ✅ pass |
| E(+)/P | 4 | 0.09 | 0.09 | 0.001 | 30% | ✅ pass |
| E(+)/P | 5 | 0.10 | 0.10 | 0.002 | 30% | ✅ pass |
| E(+)/P | 6 | 0.11 | 0.11 | 0.003 | 30% | ✅ pass |
| E(+)/P | 7 | 0.11 | 0.11 | 0.004 | 30% | ✅ pass |
| E(+)/P | 8 | 0.12 | 0.12 | 0.000 | 30% | ✅ pass |
| E(+)/P | 9 | 0.11 | 0.12 | 0.010 | 30% | ✅ pass |
| E(+)/P | 10A | 0.10 | 0.11 | 0.011 | 30% | ✅ pass |
| E(+)/P | 10B | 0.10 | 0.12 | 0.021 | 30% | ✅ pass |
| Firms | 1A | 89 | 123 | 34.4 | 20% | ❌ FAIL |
| Firms | 1B | 98 | 123 | 24.7 | 20% | ❌ FAIL |
| Firms | 2 | 209 | 246 | 36.6 | 20% | ✅ pass |
| Firms | 3 | 222 | 246 | 23.5 | 20% | ✅ pass |
| Firms | 4 | 226 | 246 | 19.6 | 20% | ✅ pass |
| Firms | 5 | 230 | 246 | 15.6 | 20% | ✅ pass |
| Firms | 6 | 235 | 245 | 10.4 | 20% | ✅ pass |
| Firms | 7 | 237 | 245 | 8.5 | 20% | ✅ pass |
| Firms | 8 | 239 | 246 | 6.6 | 20% | ✅ pass |
| Firms | 9 | 239 | 245 | 6.5 | 20% | ✅ pass |
| Firms | 10A | 120 | 123 | 3.3 | 20% | ✅ pass |
| Firms | 10B | 117 | 123 | 5.7 | 20% | ✅ pass |

## Panel B — portfolios formed on E/P (December t−1; portfolio 0 = negative earnings)

### Replicated values

| Portfolio | 0 | 1A | 1B | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10A | 10B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Return | 1.25 | 0.90 | 0.92 | 0.83 | 0.96 | 1.06 | 1.20 | 1.33 | 1.40 | 1.47 | 1.66 | 1.71 | 1.70 |
| β | 1.46 | 1.40 | 1.34 | 1.31 | 1.27 | 1.24 | 1.24 | 1.25 | 1.23 | 1.25 | 1.27 | 1.31 | 1.34 |
| ln(ME) | 2.46 | 3.59 | 4.37 | 4.54 | 4.69 | 4.67 | 4.60 | 4.51 | 4.42 | 4.25 | 4.00 | 3.76 | 3.31 |
| ln(BE/ME) | -0.12 | -0.76 | -0.86 | -0.73 | -0.57 | -0.44 | -0.31 | -0.20 | -0.07 | 0.02 | 0.14 | 0.26 | 0.44 |
| ln(A/ME) | 0.91 | -0.04 | -0.20 | -0.06 | 0.11 | 0.24 | 0.38 | 0.48 | 0.62 | 0.72 | 0.87 | 1.03 | 1.33 |
| ln(A/BE) | 1.03 | 0.72 | 0.66 | 0.67 | 0.68 | 0.69 | 0.69 | 0.69 | 0.70 | 0.70 | 0.73 | 0.77 | 0.88 |
| E/P dummy | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| E(+)/P | 0.00 | 0.02 | 0.03 | 0.05 | 0.07 | 0.08 | 0.09 | 0.11 | 0.12 | 0.14 | 0.16 | 0.20 | 0.31 |
| Firms | 424 | 102 | 102 | 203 | 203 | 203 | 203 | 203 | 203 | 203 | 203 | 102 | 102 |

### Comparison with paper

**Pass/fail: 107/117 targeted cells pass**.  Largest relative deviations: ln(A/ME) 3: ours 0.11 vs paper 0.03 (|Δ| 0.083, 278.2%); ln(A/ME) 2: ours -0.06 vs paper -0.16 (|Δ| 0.101, 62.8%); E(+)/P 1A: ours 0.02 vs paper 0.01 (|Δ| 0.006, 57.2%).

| Row | Port | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Return | 0 | 1.46 | 1.25 | 0.208 | 25% | ✅ pass |
| Return | 1A | 1.04 | 0.90 | 0.137 | 25% | ✅ pass |
| Return | 1B | 0.93 | 0.92 | 0.014 | 25% | ✅ pass |
| Return | 2 | 0.94 | 0.83 | 0.108 | 25% | ✅ pass |
| Return | 3 | 1.03 | 0.96 | 0.069 | 25% | ✅ pass |
| Return | 4 | 1.18 | 1.06 | 0.122 | 25% | ✅ pass |
| Return | 5 | 1.22 | 1.20 | 0.019 | 25% | ✅ pass |
| Return | 6 | 1.33 | 1.33 | 0.003 | 25% | ✅ pass |
| Return | 7 | 1.42 | 1.40 | 0.022 | 25% | ✅ pass |
| Return | 8 | 1.46 | 1.47 | 0.011 | 25% | ✅ pass |
| Return | 9 | 1.57 | 1.66 | 0.088 | 25% | ✅ pass |
| Return | 10A | 1.74 | 1.71 | 0.033 | 25% | ✅ pass |
| Return | 10B | 1.72 | 1.70 | 0.023 | 25% | ✅ pass |
| β | 0 | 1.47 | 1.46 | 0.009 | 15% | ✅ pass |
| β | 1A | 1.40 | 1.40 | 0.001 | 15% | ✅ pass |
| β | 1B | 1.35 | 1.34 | 0.007 | 15% | ✅ pass |
| β | 2 | 1.31 | 1.31 | 0.002 | 15% | ✅ pass |
| β | 3 | 1.28 | 1.27 | 0.007 | 15% | ✅ pass |
| β | 4 | 1.26 | 1.24 | 0.019 | 15% | ✅ pass |
| β | 5 | 1.25 | 1.24 | 0.006 | 15% | ✅ pass |
| β | 6 | 1.26 | 1.25 | 0.010 | 15% | ✅ pass |
| β | 7 | 1.24 | 1.23 | 0.014 | 15% | ✅ pass |
| β | 8 | 1.23 | 1.25 | 0.019 | 15% | ✅ pass |
| β | 9 | 1.24 | 1.27 | 0.030 | 15% | ✅ pass |
| β | 10A | 1.28 | 1.31 | 0.026 | 15% | ✅ pass |
| β | 10B | 1.31 | 1.34 | 0.029 | 15% | ✅ pass |
| ln(ME) | 0 | 2.48 | 2.46 | 0.017 | 10% | ✅ pass |
| ln(ME) | 1A | 3.64 | 3.59 | 0.046 | 10% | ✅ pass |
| ln(ME) | 1B | 4.33 | 4.37 | 0.038 | 10% | ✅ pass |
| ln(ME) | 2 | 4.61 | 4.54 | 0.069 | 10% | ✅ pass |
| ln(ME) | 3 | 4.64 | 4.69 | 0.046 | 10% | ✅ pass |
| ln(ME) | 4 | 4.63 | 4.67 | 0.040 | 10% | ✅ pass |
| ln(ME) | 5 | 4.58 | 4.60 | 0.020 | 10% | ✅ pass |
| ln(ME) | 6 | 4.49 | 4.51 | 0.019 | 10% | ✅ pass |
| ln(ME) | 7 | 4.37 | 4.42 | 0.054 | 10% | ✅ pass |
| ln(ME) | 8 | 4.28 | 4.25 | 0.030 | 10% | ✅ pass |
| ln(ME) | 9 | 4.07 | 4.00 | 0.069 | 10% | ✅ pass |
| ln(ME) | 10A | 3.82 | 3.76 | 0.065 | 10% | ✅ pass |
| ln(ME) | 10B | 3.52 | 3.31 | 0.209 | 10% | ✅ pass |
| ln(BE/ME) | 0 | -0.10 | -0.12 | 0.020 | 10% | ❌ FAIL |
| ln(BE/ME) | 1A | -0.76 | -0.76 | 0.005 | 10% | ✅ pass |
| ln(BE/ME) | 1B | -0.91 | -0.86 | 0.052 | 10% | ✅ pass |
| ln(BE/ME) | 2 | -0.79 | -0.73 | 0.065 | 10% | ✅ pass |
| ln(BE/ME) | 3 | -0.61 | -0.57 | 0.044 | 10% | ✅ pass |
| ln(BE/ME) | 4 | -0.47 | -0.44 | 0.026 | 10% | ✅ pass |
| ln(BE/ME) | 5 | -0.33 | -0.31 | 0.021 | 10% | ✅ pass |
| ln(BE/ME) | 6 | -0.21 | -0.20 | 0.007 | 10% | ✅ pass |
| ln(BE/ME) | 7 | -0.08 | -0.07 | 0.008 | 10% | ✅ pass |
| ln(BE/ME) | 8 | 0.02 | 0.02 | 0.001 | 10% | ✅ pass |
| ln(BE/ME) | 9 | 0.15 | 0.14 | 0.008 | 10% | ✅ pass |
| ln(BE/ME) | 10A | 0.26 | 0.26 | 0.005 | 10% | ✅ pass |
| ln(BE/ME) | 10B | 0.40 | 0.44 | 0.043 | 10% | ❌ FAIL |
| ln(A/ME) | 0 | 0.90 | 0.91 | 0.005 | 10% | ✅ pass |
| ln(A/ME) | 1A | -0.05 | -0.04 | 0.012 | 10% | ❌ FAIL |
| ln(A/ME) | 1B | -0.27 | -0.20 | 0.072 | 10% | ❌ FAIL |
| ln(A/ME) | 2 | -0.16 | -0.06 | 0.101 | 10% | ❌ FAIL |
| ln(A/ME) | 3 | 0.03 | 0.11 | 0.083 | 10% | ❌ FAIL |
| ln(A/ME) | 4 | 0.18 | 0.24 | 0.062 | 10% | ❌ FAIL |
| ln(A/ME) | 5 | 0.31 | 0.38 | 0.070 | 10% | ❌ FAIL |
| ln(A/ME) | 6 | 0.44 | 0.48 | 0.044 | 10% | ❌ FAIL |
| ln(A/ME) | 7 | 0.58 | 0.62 | 0.045 | 10% | ✅ pass |
| ln(A/ME) | 8 | 0.70 | 0.72 | 0.025 | 10% | ✅ pass |
| ln(A/ME) | 9 | 0.85 | 0.87 | 0.019 | 10% | ✅ pass |
| ln(A/ME) | 10A | 1.01 | 1.03 | 0.020 | 10% | ✅ pass |
| ln(A/ME) | 10B | 1.25 | 1.33 | 0.076 | 10% | ✅ pass |
| ln(A/BE) | 0 | 0.99 | 1.03 | 0.035 | 10% | ✅ pass |
| ln(A/BE) | 1A | 0.70 | 0.72 | 0.017 | 10% | ✅ pass |
| ln(A/BE) | 1B | 0.63 | 0.66 | 0.030 | 10% | ✅ pass |
| ln(A/BE) | 2 | 0.63 | 0.67 | 0.036 | 10% | ✅ pass |
| ln(A/BE) | 3 | 0.64 | 0.68 | 0.040 | 10% | ✅ pass |
| ln(A/BE) | 4 | 0.65 | 0.69 | 0.036 | 10% | ✅ pass |
| ln(A/BE) | 5 | 0.64 | 0.69 | 0.049 | 10% | ✅ pass |
| ln(A/BE) | 6 | 0.65 | 0.69 | 0.037 | 10% | ✅ pass |
| ln(A/BE) | 7 | 0.66 | 0.70 | 0.037 | 10% | ✅ pass |
| ln(A/BE) | 8 | 0.68 | 0.70 | 0.024 | 10% | ✅ pass |
| ln(A/BE) | 9 | 0.71 | 0.73 | 0.017 | 10% | ✅ pass |
| ln(A/BE) | 10A | 0.75 | 0.77 | 0.025 | 10% | ✅ pass |
| ln(A/BE) | 10B | 0.86 | 0.88 | 0.023 | 10% | ✅ pass |
| E/P dummy | 0 | 1.00 | 1.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 1A | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 1B | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 2 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 3 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 4 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 5 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 6 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 7 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 8 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 9 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 10A | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E/P dummy | 10B | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E(+)/P | 0 | 0.00 | 0.00 | 0.000 | 30% | ✅ pass |
| E(+)/P | 1A | 0.01 | 0.02 | 0.006 | 30% | ❌ FAIL |
| E(+)/P | 1B | 0.03 | 0.03 | 0.003 | 30% | ✅ pass |
| E(+)/P | 2 | 0.05 | 0.05 | 0.001 | 30% | ✅ pass |
| E(+)/P | 3 | 0.06 | 0.07 | 0.006 | 30% | ✅ pass |
| E(+)/P | 4 | 0.08 | 0.08 | 0.000 | 30% | ✅ pass |
| E(+)/P | 5 | 0.09 | 0.09 | 0.002 | 30% | ✅ pass |
| E(+)/P | 6 | 0.11 | 0.11 | 0.005 | 30% | ✅ pass |
| E(+)/P | 7 | 0.12 | 0.12 | 0.000 | 30% | ✅ pass |
| E(+)/P | 8 | 0.14 | 0.14 | 0.003 | 30% | ✅ pass |
| E(+)/P | 9 | 0.16 | 0.16 | 0.003 | 30% | ✅ pass |
| E(+)/P | 10A | 0.20 | 0.20 | 0.002 | 30% | ✅ pass |
| E(+)/P | 10B | 0.28 | 0.31 | 0.028 | 30% | ✅ pass |
| Firms | 0 | 355 | 424 | 68.6 | 20% | ✅ pass |
| Firms | 1A | 88 | 102 | 14.2 | 20% | ✅ pass |
| Firms | 1B | 90 | 102 | 11.6 | 20% | ✅ pass |
| Firms | 2 | 182 | 203 | 21.2 | 20% | ✅ pass |
| Firms | 3 | 190 | 203 | 13.2 | 20% | ✅ pass |
| Firms | 4 | 193 | 203 | 10.2 | 20% | ✅ pass |
| Firms | 5 | 196 | 203 | 7.5 | 20% | ✅ pass |
| Firms | 6 | 194 | 203 | 9.0 | 20% | ✅ pass |
| Firms | 7 | 197 | 203 | 6.0 | 20% | ✅ pass |
| Firms | 8 | 195 | 203 | 8.3 | 20% | ✅ pass |
| Firms | 9 | 195 | 203 | 8.0 | 20% | ✅ pass |
| Firms | 10A | 95 | 102 | 7.2 | 20% | ✅ pass |
| Firms | 10B | 91 | 102 | 10.6 | 20% | ✅ pass |

## Overall summary

- **Targeted cells: 199/225 pass** (tolerances: Return 25%, β 15%, ln-ratios 10%, E/P rows 30%, Firms 20%; from preparations/tables_to_replicate.json).
  - BE/ME panel (A): 92/108 pass.
  - E/P panel (B): 107/117 pass.
- Pass rates by row:
  - Return: 24/25.
  - β: 25/25.
  - ln(ME): 25/25.
  - ln(BE/ME): 17/25.
  - ln(A/ME): 11/25.
  - ln(A/BE): 25/25.
  - E/P dummy: 25/25.
  - E(+)/P: 24/25.
  - Firms: 23/25.

- **Headline spreads:** Panel A Return rises monotonically 0.41% (1A) → 1.79% (10B) (paper 0.30 → 1.83). Panel B Return is U-shaped: 1.25% (portfolio 0, negative earnings) → 0.83% (2, the minimum among positive-E/P portfolios) → 1.70% (10B) (paper 1.46 → 0.93 → 1.72).
- **Failing cells (26):**
  - Panel A Return 1A: ours 0.41 vs paper 0.30 (|Δ| 0.106, 35.3% > 25%).
  - Panel A ln(BE/ME) 3: ours -0.67 vs paper -0.75 (|Δ| 0.079, 10.5% > 10%).
  - Panel A ln(BE/ME) 4: ours -0.45 vs paper -0.51 (|Δ| 0.063, 12.3% > 10%).
  - Panel A ln(BE/ME) 5: ours -0.27 vs paper -0.32 (|Δ| 0.054, 16.9% > 10%).
  - Panel A ln(BE/ME) 6: ours -0.10 vs paper -0.14 (|Δ| 0.037, 26.5% > 10%).
  - Panel A ln(BE/ME) 7: ours 0.06 vs paper 0.03 (|Δ| 0.031, 103.1% > 10%).
  - Panel A ln(BE/ME) 8: ours 0.23 vs paper 0.21 (|Δ| 0.022, 10.7% > 10%).
  - Panel A ln(A/ME) 1B: ours -0.64 vs paper -0.79 (|Δ| 0.153, 19.3% > 10%).
  - Panel A ln(A/ME) 2: ours -0.27 vs paper -0.40 (|Δ| 0.132, 33.1% > 10%).
  - Panel A ln(A/ME) 3: ours 0.06 vs paper -0.05 (|Δ| 0.109, 217.4% > 10%).
  - Panel A ln(A/ME) 4: ours 0.31 vs paper 0.20 (|Δ| 0.107, 53.3% > 10%).
  - Panel A ln(A/ME) 5: ours 0.48 vs paper 0.40 (|Δ| 0.083, 20.6% > 10%).
  - Panel A ln(A/ME) 6: ours 0.64 vs paper 0.56 (|Δ| 0.077, 13.8% > 10%).
  - Panel A ln(A/ME) 7: ours 0.78 vs paper 0.71 (|Δ| 0.073, 10.4% > 10%).
  - Panel A Firms 1A: ours 123 vs paper 89 (|Δ| 34.4, 38.7% > 20%).
  - Panel A Firms 1B: ours 123 vs paper 98 (|Δ| 24.7, 25.2% > 20%).
  - Panel B ln(BE/ME) 0: ours -0.12 vs paper -0.10 (|Δ| 0.020, 19.8% > 10%).
  - Panel B ln(BE/ME) 10B: ours 0.44 vs paper 0.40 (|Δ| 0.043, 10.7% > 10%).
  - Panel B ln(A/ME) 1A: ours -0.04 vs paper -0.05 (|Δ| 0.012, 23.8% > 10%).
  - Panel B ln(A/ME) 1B: ours -0.20 vs paper -0.27 (|Δ| 0.072, 26.7% > 10%).
  - Panel B ln(A/ME) 2: ours -0.06 vs paper -0.16 (|Δ| 0.101, 62.8% > 10%).
  - Panel B ln(A/ME) 3: ours 0.11 vs paper 0.03 (|Δ| 0.083, 278.2% > 10%).
  - Panel B ln(A/ME) 4: ours 0.24 vs paper 0.18 (|Δ| 0.062, 34.2% > 10%).
  - Panel B ln(A/ME) 5: ours 0.38 vs paper 0.31 (|Δ| 0.070, 22.6% > 10%).
  - Panel B ln(A/ME) 6: ours 0.48 vs paper 0.44 (|Δ| 0.044, 10.1% > 10%).
  - Panel B E(+)/P 1A: ours 0.02 vs paper 0.01 (|Δ| 0.006, 57.2% > 30%).
- Identity check ln(A/ME)−ln(A/BE)=ln(BE/ME): max discrepancy 1.39e-16 across all 25 portfolio cells.
- Portfolio-month coverage: every portfolio appears in all 330 months.
- Months covered: 330 (paper = 330).

## Notes / flags

1. ⚠️ 26 failing cells (ln(A/ME) 14, ln(BE/ME) 8, Firms 2, Return 1, E(+)/P 1). The accounting-ratio failures are the same systematic Compustat-vintage shift documented in iterations 2–3 (Table II accounting-ratio rows; Table III E(+)/P levels): our ln(BE/ME) runs less negative and ln(A/ME) above the paper, while **ln(A/BE) — the pure accounting ratio with no market equity in it — passes 13/13 in both panels combined (25/25 overall)**. The two deviations are near-identical per cell (max discrepancy between the two gaps 1.4e-16 by construction), i.e. the shift is consistent with a December-t−1 ME-level / composition difference in this extract (≈5.5% more obs/month than the paper), not with the A/BE accounting data. Return (24/25), β (25/25), ln(ME) (25/25) and E/P dummy (25/25) are unaffected.
2. ⚠️ Panel A Firms 1A/1B (123/123 vs 89/98) and Return 1A (0.41 vs 0.30) are composition effects at the low-BE/ME extreme: this extract's extra firms land disproportionately in the bottom BE/ME bin (portfolio 0 of Panel B shows the same: 400 valid-return firms/mo vs paper 355). The Firms gap is NOT an all-members-vs-valid-returns counting artifact — our mean monthly VALID-return counts are 119 / 120 / 240 / 240 / 240 / 240 / 240 / 239 / 240 / 238 / 120 / 118 (Panel A), still above the paper's 89–239; membership counts are uniform (~246/decile) because breakpoints are quantiles of the December cross-section and membership is fixed within the firm-year (the paper's 209–239 gradient is not reproduced — reported as fact, no methodology change).
3. Panel B portfolio 0 is, by construction, the negative-earnings set: E/P dummy = 1.00 and E(+)/P = 0.00 exactly (paper 1.00 / 0.00). The Panel B U-shape replicates: the minimum return among the positive-E/P portfolios is at portfolio 2 (0.83; paper 0.93 at 1A/2), rising to 1.70 at 10B (paper 1.72).
4. Methodology implemented exactly as specified — no deviations. The December-t−1 sorts (beme12/ep13) use all-data-qualified breakpoints per L1382; membership eligibility is the single-June-t universe screen flagged in iteration 1 (assumptions.md, flag 2).

---
*Computed by src/table_4.py from data/panel.parquet (iteration-1 pipeline; columns beme12 / ep13 added by the pipeline). All statistics are time-series means of monthly cross-sectional portfolio means; Firms is the mean monthly member count.*