# Table II — Fama & French (1992), The Cross-Section of Expected Stock Returns

Properties of the 12 one-dimensional portfolios formed at the end of June each year on **size (ME)** (Panel A) or **pre-ranking β** (Panel B). Columns 2–9 are deciles of the ranking variable; 1A/1B split the bottom decile and 10A/10B split the top decile. NYSE breakpoints; equal-weighted; sample July 1963 – December 1990 (330 months; 28 formation years, 1963–1990).

**Averaging conventions (paper notes L815/L817/L819).** *Return*: time-series average (over the 330 months) of the monthly equal-weighted portfolio return ×100 (monthly EW = mean of valid stock returns in the portfolio that month). *β*: mean of the stock-level post-ranking βs (each stock carries the full-period post-ranking β of its size×pre-β cell, assigned each June) over members each month, then time-series mean. *ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P dummy, E(+)/P*: mean of the stock-level firm-year value over the members present each month, then time-series mean over the 330 months. *Firms*: mean over months of the number of assigned members per month (panel rows per (month, portfolio), counted regardless of return validity).

## Panel A — portfolios formed on SIZE (ME)

### Replicated values

| Portfolio | 1A | 1B | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10A | 10B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Return | 1.60 | 1.15 | 1.20 | 1.24 | 1.24 | 1.29 | 1.13 | 1.08 | 1.08 | 0.93 | 0.88 | 0.85 |
| β | 1.44 | 1.43 | 1.39 | 1.36 | 1.34 | 1.25 | 1.19 | 1.18 | 1.07 | 1.01 | 0.97 | 0.93 |
| ln(ME) | 1.98 | 3.21 | 3.67 | 4.15 | 4.57 | 4.97 | 5.37 | 5.81 | 6.30 | 6.85 | 7.42 | 8.47 |
| ln(BE/ME) | -0.02 | -0.20 | -0.23 | -0.25 | -0.28 | -0.32 | -0.35 | -0.41 | -0.40 | -0.42 | -0.51 | -0.69 |
| ln(A/ME) | 0.77 | 0.54 | 0.50 | 0.49 | 0.44 | 0.40 | 0.37 | 0.29 | 0.31 | 0.30 | 0.18 | -0.06 |
| ln(A/BE) | 0.79 | 0.74 | 0.72 | 0.74 | 0.72 | 0.72 | 0.72 | 0.70 | 0.71 | 0.72 | 0.70 | 0.63 |
| E/P dummy | 0.27 | 0.14 | 0.12 | 0.09 | 0.06 | 0.04 | 0.04 | 0.03 | 0.03 | 0.02 | 0.02 | 0.01 |
| E(+)/P | 0.09 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.09 | 0.10 | 0.10 | 0.09 | 0.09 |
| Firms | 918 | 211 | 258 | 183 | 152 | 144 | 127 | 121 | 115 | 112 | 57 | 59 |

### Comparison with paper

**Pass/fail: 79/96 targeted cells pass** (+ 12 no-target cells shown but not scored).  Largest relative deviations: ln(A/ME) 10A: ours 0.18 vs paper -0.03 (|Δ| 0.214, 713.0%); ln(A/ME) 10B: ours -0.06 vs paper -0.03 (|Δ| 0.032, 108.1%); ln(A/ME) 9: ours 0.30 vs paper 0.17 (|Δ| 0.129, 75.6%).

> **No target:** the E(+)/P row is missing from the paper OCR for Panel A — our values are shown but not scored.

| Row | Port | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Return | 1A | 1.64 | 1.60 | 0.044 | 25% | ✅ pass |
| Return | 1B | 1.16 | 1.15 | 0.006 | 25% | ✅ pass |
| Return | 2 | 1.29 | 1.20 | 0.090 | 25% | ✅ pass |
| Return | 3 | 1.24 | 1.24 | 0.002 | 25% | ✅ pass |
| Return | 4 | 1.25 | 1.24 | 0.011 | 25% | ✅ pass |
| Return | 5 | 1.29 | 1.29 | 0.003 | 25% | ✅ pass |
| Return | 6 | 1.17 | 1.13 | 0.040 | 25% | ✅ pass |
| Return | 7 | 1.07 | 1.08 | 0.006 | 25% | ✅ pass |
| Return | 8 | 1.10 | 1.08 | 0.023 | 25% | ✅ pass |
| Return | 9 | 0.95 | 0.93 | 0.020 | 25% | ✅ pass |
| Return | 10A | 0.88 | 0.88 | 0.002 | 25% | ✅ pass |
| Return | 10B | 0.90 | 0.85 | 0.052 | 25% | ✅ pass |
| β | 1A | 1.44 | 1.44 | 0.001 | 15% | ✅ pass |
| β | 1B | 1.44 | 1.43 | 0.008 | 15% | ✅ pass |
| β | 2 | 1.39 | 1.39 | 0.000 | 15% | ✅ pass |
| β | 3 | 1.34 | 1.36 | 0.016 | 15% | ✅ pass |
| β | 4 | 1.33 | 1.34 | 0.006 | 15% | ✅ pass |
| β | 5 | 1.24 | 1.25 | 0.009 | 15% | ✅ pass |
| β | 6 | 1.22 | 1.19 | 0.026 | 15% | ✅ pass |
| β | 7 | 1.16 | 1.18 | 0.016 | 15% | ✅ pass |
| β | 8 | 1.08 | 1.07 | 0.008 | 15% | ✅ pass |
| β | 9 | 1.02 | 1.01 | 0.009 | 15% | ✅ pass |
| β | 10A | 0.95 | 0.97 | 0.021 | 15% | ✅ pass |
| β | 10B | 0.90 | 0.93 | 0.029 | 15% | ✅ pass |
| ln(ME) | 1A | 1.98 | 1.98 | 0.001 | 10% | ✅ pass |
| ln(ME) | 1B | 3.18 | 3.21 | 0.030 | 10% | ✅ pass |
| ln(ME) | 2 | 3.63 | 3.67 | 0.044 | 10% | ✅ pass |
| ln(ME) | 3 | 4.10 | 4.15 | 0.054 | 10% | ✅ pass |
| ln(ME) | 4 | 4.50 | 4.57 | 0.066 | 10% | ✅ pass |
| ln(ME) | 5 | 4.89 | 4.97 | 0.077 | 10% | ✅ pass |
| ln(ME) | 6 | 5.30 | 5.37 | 0.074 | 10% | ✅ pass |
| ln(ME) | 7 | 5.73 | 5.81 | 0.075 | 10% | ✅ pass |
| ln(ME) | 8 | 6.24 | 6.30 | 0.056 | 10% | ✅ pass |
| ln(ME) | 9 | 6.82 | 6.85 | 0.028 | 10% | ✅ pass |
| ln(ME) | 10A | 7.39 | 7.42 | 0.027 | 10% | ✅ pass |
| ln(ME) | 10B | 8.44 | 8.47 | 0.031 | 10% | ✅ pass |
| ln(BE/ME) | 1A | -0.01 | -0.02 | 0.006 | 10% | ❌ FAIL |
| ln(BE/ME) | 1B | -0.21 | -0.20 | 0.009 | 10% | ✅ pass |
| ln(BE/ME) | 2 | -0.23 | -0.23 | 0.003 | 10% | ✅ pass |
| ln(BE/ME) | 3 | -0.26 | -0.25 | 0.010 | 10% | ✅ pass |
| ln(BE/ME) | 4 | -0.32 | -0.28 | 0.036 | 10% | ❌ FAIL |
| ln(BE/ME) | 5 | -0.36 | -0.32 | 0.040 | 10% | ❌ FAIL |
| ln(BE/ME) | 6 | -0.44 | -0.35 | 0.093 | 10% | ❌ FAIL |
| ln(BE/ME) | 7 | -0.40 | -0.41 | 0.011 | 10% | ✅ pass |
| ln(BE/ME) | 8 | -0.42 | -0.40 | 0.019 | 10% | ✅ pass |
| ln(BE/ME) | 9 | -0.51 | -0.42 | 0.091 | 10% | ❌ FAIL |
| ln(BE/ME) | 10A | -0.65 | -0.51 | 0.135 | 10% | ❌ FAIL |
| ln(BE/ME) | 10B | -0.65 | -0.69 | 0.042 | 10% | ✅ pass |
| ln(A/ME) | 1A | 0.73 | 0.77 | 0.041 | 10% | ✅ pass |
| ln(A/ME) | 1B | 0.50 | 0.54 | 0.039 | 10% | ✅ pass |
| ln(A/ME) | 2 | 0.46 | 0.50 | 0.035 | 10% | ✅ pass |
| ln(A/ME) | 3 | 0.43 | 0.49 | 0.057 | 10% | ❌ FAIL |
| ln(A/ME) | 4 | 0.37 | 0.44 | 0.070 | 10% | ❌ FAIL |
| ln(A/ME) | 5 | 0.32 | 0.40 | 0.082 | 10% | ❌ FAIL |
| ln(A/ME) | 6 | 0.24 | 0.37 | 0.134 | 10% | ❌ FAIL |
| ln(A/ME) | 7 | 0.29 | 0.29 | 0.002 | 10% | ✅ pass |
| ln(A/ME) | 8 | 0.27 | 0.31 | 0.035 | 10% | ❌ FAIL |
| ln(A/ME) | 9 | 0.17 | 0.30 | 0.129 | 10% | ❌ FAIL |
| ln(A/ME) | 10A | -0.03 | 0.18 | 0.214 | 10% | ❌ FAIL |
| ln(A/ME) | 10B | -0.03 | -0.06 | 0.032 | 10% | ❌ FAIL |
| ln(A/BE) | 1A | 0.75 | 0.79 | 0.036 | 10% | ✅ pass |
| ln(A/BE) | 1B | 0.71 | 0.74 | 0.030 | 10% | ✅ pass |
| ln(A/BE) | 2 | 0.69 | 0.72 | 0.032 | 10% | ✅ pass |
| ln(A/BE) | 3 | 0.69 | 0.74 | 0.046 | 10% | ✅ pass |
| ln(A/BE) | 4 | 0.68 | 0.72 | 0.044 | 10% | ✅ pass |
| ln(A/BE) | 5 | 0.67 | 0.72 | 0.053 | 10% | ✅ pass |
| ln(A/BE) | 6 | 0.68 | 0.72 | 0.041 | 10% | ✅ pass |
| ln(A/BE) | 7 | 0.69 | 0.70 | 0.013 | 10% | ✅ pass |
| ln(A/BE) | 8 | 0.70 | 0.71 | 0.006 | 10% | ✅ pass |
| ln(A/BE) | 9 | 0.68 | 0.72 | 0.038 | 10% | ✅ pass |
| ln(A/BE) | 10A | 0.62 | 0.70 | 0.079 | 10% | ❌ FAIL |
| ln(A/BE) | 10B | 0.62 | 0.63 | 0.010 | 10% | ✅ pass |
| E/P dummy | 1A | 0.26 | 0.27 | 0.006 | 30% | ✅ pass |
| E/P dummy | 1B | 0.14 | 0.14 | 0.005 | 30% | ✅ pass |
| E/P dummy | 2 | 0.11 | 0.12 | 0.005 | 30% | ✅ pass |
| E/P dummy | 3 | 0.09 | 0.09 | 0.004 | 30% | ✅ pass |
| E/P dummy | 4 | 0.06 | 0.06 | 0.005 | 30% | ✅ pass |
| E/P dummy | 5 | 0.04 | 0.04 | 0.002 | 30% | ✅ pass |
| E/P dummy | 6 | 0.04 | 0.04 | 0.000 | 30% | ✅ pass |
| E/P dummy | 7 | 0.03 | 0.03 | 0.004 | 30% | ✅ pass |
| E/P dummy | 8 | 0.02 | 0.03 | 0.007 | 30% | ❌ FAIL |
| E/P dummy | 9 | 0.02 | 0.02 | 0.001 | 30% | ✅ pass |
| E/P dummy | 10A | 0.01 | 0.02 | 0.005 | 30% | ❌ FAIL |
| E/P dummy | 10B | 0.01 | 0.01 | 0.001 | 30% | ✅ pass |
| E(+)/P | 1A | — | 0.09 | — | — | no target |
| E(+)/P | 1B | — | 0.10 | — | — | no target |
| E(+)/P | 2 | — | 0.10 | — | — | no target |
| E(+)/P | 3 | — | 0.10 | — | — | no target |
| E(+)/P | 4 | — | 0.10 | — | — | no target |
| E(+)/P | 5 | — | 0.10 | — | — | no target |
| E(+)/P | 6 | — | 0.10 | — | — | no target |
| E(+)/P | 7 | — | 0.09 | — | — | no target |
| E(+)/P | 8 | — | 0.10 | — | — | no target |
| E(+)/P | 9 | — | 0.10 | — | — | no target |
| E(+)/P | 10A | — | 0.09 | — | — | no target |
| E(+)/P | 10B | — | 0.09 | — | — | no target |
| Firms | 1A | 772 | 918 | 145.8 | 20% | ✅ pass |
| Firms | 1B | 189 | 211 | 21.6 | 20% | ✅ pass |
| Firms | 2 | 236 | 258 | 21.7 | 20% | ✅ pass |
| Firms | 3 | 170 | 183 | 13.2 | 20% | ✅ pass |
| Firms | 4 | 144 | 152 | 8.1 | 20% | ✅ pass |
| Firms | 5 | 140 | 144 | 4.5 | 20% | ✅ pass |
| Firms | 6 | 125 | 127 | 2.2 | 20% | ✅ pass |
| Firms | 7 | 128 | 121 | 6.9 | 20% | ✅ pass |
| Firms | 8 | 119 | 115 | 4.5 | 20% | ✅ pass |
| Firms | 9 | 114 | 112 | 2.1 | 20% | ✅ pass |
| Firms | 10A | 60 | 57 | 3.3 | 20% | ✅ pass |
| Firms | 10B | 64 | 59 | 5.0 | 20% | ✅ pass |

## Panel B — portfolios formed on pre-ranking β

### Replicated values

| Portfolio | 1A | 1B | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10A | 10B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Return | 1.15 | 1.16 | 1.25 | 1.23 | 1.29 | 1.22 | 1.27 | 1.21 | 1.23 | 1.26 | 1.17 | 1.11 |
| β | 0.81 | 0.80 | 0.93 | 1.05 | 1.13 | 1.20 | 1.28 | 1.34 | 1.42 | 1.54 | 1.66 | 1.73 |
| ln(ME) | 4.13 | 4.76 | 4.64 | 4.65 | 4.55 | 4.43 | 4.33 | 4.17 | 3.95 | 3.71 | 3.48 | 3.09 |
| ln(BE/ME) | -0.20 | -0.15 | -0.22 | -0.21 | -0.22 | -0.21 | -0.21 | -0.22 | -0.23 | -0.25 | -0.32 | -0.48 |
| ln(A/ME) | 0.64 | 0.69 | 0.54 | 0.49 | 0.46 | 0.47 | 0.48 | 0.48 | 0.51 | 0.51 | 0.48 | 0.38 |
| ln(A/BE) | 0.84 | 0.84 | 0.76 | 0.71 | 0.68 | 0.68 | 0.69 | 0.70 | 0.73 | 0.75 | 0.80 | 0.86 |
| E/P dummy | 0.13 | 0.09 | 0.09 | 0.10 | 0.09 | 0.10 | 0.11 | 0.13 | 0.14 | 0.15 | 0.19 | 0.25 |
| E(+)/P | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.10 | 0.09 | 0.09 | 0.08 |
| Firms | 135 | 93 | 214 | 199 | 193 | 200 | 202 | 225 | 238 | 279 | 175 | 302 |

### Comparison with paper

**Pass/fail: 89/98 targeted cells pass** (+ 10 no-target cells shown but not scored).  Largest relative deviations: E/P dummy 1B: ours 0.09 vs paper 0.06 (|Δ| 0.026, 43.7%); ln(A/ME) 10B: ours 0.38 vs paper 0.31 (|Δ| 0.068, 22.0%); Firms 1A: ours 135 vs paper 116 (|Δ| 19.4, 16.7%).

> **No target:** for Panel B Return only 1A (1.20) and 10B (1.18) are prose-anchored; the interior Return cells lost one OCR cell and carry no target (computed and shown, not scored).

| Row | Port | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Return | 1A | 1.20 | 1.15 | 0.054 | 25% | ✅ pass |
| Return | 1B | — | 1.16 | — | — | no target |
| Return | 2 | — | 1.25 | — | — | no target |
| Return | 3 | — | 1.23 | — | — | no target |
| Return | 4 | — | 1.29 | — | — | no target |
| Return | 5 | — | 1.22 | — | — | no target |
| Return | 6 | — | 1.27 | — | — | no target |
| Return | 7 | — | 1.21 | — | — | no target |
| Return | 8 | — | 1.23 | — | — | no target |
| Return | 9 | — | 1.26 | — | — | no target |
| Return | 10A | — | 1.17 | — | — | no target |
| Return | 10B | 1.18 | 1.11 | 0.068 | 25% | ✅ pass |
| β | 1A | 0.81 | 0.81 | 0.001 | 15% | ✅ pass |
| β | 1B | 0.79 | 0.80 | 0.013 | 15% | ✅ pass |
| β | 2 | 0.92 | 0.93 | 0.010 | 15% | ✅ pass |
| β | 3 | 1.04 | 1.05 | 0.012 | 15% | ✅ pass |
| β | 4 | 1.13 | 1.13 | 0.003 | 15% | ✅ pass |
| β | 5 | 1.19 | 1.20 | 0.014 | 15% | ✅ pass |
| β | 6 | 1.26 | 1.28 | 0.018 | 15% | ✅ pass |
| β | 7 | 1.32 | 1.34 | 0.018 | 15% | ✅ pass |
| β | 8 | 1.41 | 1.42 | 0.014 | 15% | ✅ pass |
| β | 9 | 1.52 | 1.54 | 0.020 | 15% | ✅ pass |
| β | 10A | 1.63 | 1.66 | 0.030 | 15% | ✅ pass |
| β | 10B | 1.73 | 1.73 | 0.000 | 15% | ✅ pass |
| ln(ME) | 1A | 4.21 | 4.13 | 0.080 | 10% | ✅ pass |
| ln(ME) | 1B | 4.86 | 4.76 | 0.097 | 10% | ✅ pass |
| ln(ME) | 2 | 4.75 | 4.64 | 0.113 | 10% | ✅ pass |
| ln(ME) | 3 | 4.68 | 4.65 | 0.030 | 10% | ✅ pass |
| ln(ME) | 4 | 4.59 | 4.55 | 0.036 | 10% | ✅ pass |
| ln(ME) | 5 | 4.48 | 4.43 | 0.053 | 10% | ✅ pass |
| ln(ME) | 6 | 4.36 | 4.33 | 0.027 | 10% | ✅ pass |
| ln(ME) | 7 | 4.25 | 4.17 | 0.076 | 10% | ✅ pass |
| ln(ME) | 8 | 3.97 | 3.95 | 0.018 | 10% | ✅ pass |
| ln(ME) | 9 | 3.78 | 3.71 | 0.067 | 10% | ✅ pass |
| ln(ME) | 10A | 3.52 | 3.48 | 0.042 | 10% | ✅ pass |
| ln(ME) | 10B | 3.15 | 3.09 | 0.064 | 10% | ✅ pass |
| ln(BE/ME) | 1A | -0.18 | -0.20 | 0.021 | 10% | ❌ FAIL |
| ln(BE/ME) | 1B | -0.13 | -0.15 | 0.019 | 10% | ❌ FAIL |
| ln(BE/ME) | 2 | -0.22 | -0.22 | 0.002 | 10% | ✅ pass |
| ln(BE/ME) | 3 | -0.21 | -0.21 | 0.004 | 10% | ✅ pass |
| ln(BE/ME) | 4 | -0.23 | -0.22 | 0.008 | 10% | ✅ pass |
| ln(BE/ME) | 5 | -0.22 | -0.21 | 0.005 | 10% | ✅ pass |
| ln(BE/ME) | 6 | -0.22 | -0.21 | 0.011 | 10% | ✅ pass |
| ln(BE/ME) | 7 | -0.25 | -0.22 | 0.027 | 10% | ❌ FAIL |
| ln(BE/ME) | 8 | -0.23 | -0.23 | 0.004 | 10% | ✅ pass |
| ln(BE/ME) | 9 | -0.27 | -0.25 | 0.023 | 10% | ✅ pass |
| ln(BE/ME) | 10A | -0.31 | -0.32 | 0.013 | 10% | ✅ pass |
| ln(BE/ME) | 10B | -0.50 | -0.48 | 0.018 | 10% | ✅ pass |
| ln(A/ME) | 1A | 0.60 | 0.64 | 0.039 | 10% | ✅ pass |
| ln(A/ME) | 1B | 0.66 | 0.69 | 0.026 | 10% | ✅ pass |
| ln(A/ME) | 2 | 0.49 | 0.54 | 0.050 | 10% | ❌ FAIL |
| ln(A/ME) | 3 | 0.45 | 0.49 | 0.041 | 10% | ✅ pass |
| ln(A/ME) | 4 | 0.42 | 0.46 | 0.035 | 10% | ✅ pass |
| ln(A/ME) | 5 | 0.42 | 0.47 | 0.048 | 10% | ❌ FAIL |
| ln(A/ME) | 6 | 0.45 | 0.48 | 0.033 | 10% | ✅ pass |
| ln(A/ME) | 7 | 0.42 | 0.48 | 0.055 | 10% | ❌ FAIL |
| ln(A/ME) | 8 | 0.47 | 0.51 | 0.035 | 10% | ✅ pass |
| ln(A/ME) | 9 | 0.46 | 0.51 | 0.047 | 10% | ❌ FAIL |
| ln(A/ME) | 10A | 0.46 | 0.48 | 0.016 | 10% | ✅ pass |
| ln(A/ME) | 10B | 0.31 | 0.38 | 0.068 | 10% | ❌ FAIL |
| ln(A/BE) | 1A | 0.78 | 0.84 | 0.060 | 10% | ✅ pass |
| ln(A/BE) | 1B | 0.79 | 0.84 | 0.045 | 10% | ✅ pass |
| ln(A/BE) | 2 | 0.71 | 0.76 | 0.048 | 10% | ✅ pass |
| ln(A/BE) | 3 | 0.66 | 0.71 | 0.045 | 10% | ✅ pass |
| ln(A/BE) | 4 | 0.64 | 0.68 | 0.038 | 10% | ✅ pass |
| ln(A/BE) | 5 | 0.65 | 0.68 | 0.032 | 10% | ✅ pass |
| ln(A/BE) | 6 | 0.67 | 0.69 | 0.022 | 10% | ✅ pass |
| ln(A/BE) | 7 | 0.67 | 0.70 | 0.028 | 10% | ✅ pass |
| ln(A/BE) | 8 | 0.70 | 0.73 | 0.031 | 10% | ✅ pass |
| ln(A/BE) | 9 | 0.73 | 0.75 | 0.024 | 10% | ✅ pass |
| ln(A/BE) | 10A | 0.77 | 0.80 | 0.029 | 10% | ✅ pass |
| ln(A/BE) | 10B | 0.81 | 0.86 | 0.050 | 10% | ✅ pass |
| E/P dummy | 1A | 0.12 | 0.13 | 0.010 | 30% | ✅ pass |
| E/P dummy | 1B | 0.06 | 0.09 | 0.026 | 30% | ❌ FAIL |
| E/P dummy | 2 | 0.09 | 0.09 | 0.004 | 30% | ✅ pass |
| E/P dummy | 3 | 0.09 | 0.10 | 0.007 | 30% | ✅ pass |
| E/P dummy | 4 | 0.08 | 0.09 | 0.006 | 30% | ✅ pass |
| E/P dummy | 5 | 0.09 | 0.10 | 0.007 | 30% | ✅ pass |
| E/P dummy | 6 | 0.10 | 0.11 | 0.010 | 30% | ✅ pass |
| E/P dummy | 7 | 0.12 | 0.13 | 0.006 | 30% | ✅ pass |
| E/P dummy | 8 | 0.12 | 0.14 | 0.018 | 30% | ✅ pass |
| E/P dummy | 9 | 0.14 | 0.15 | 0.006 | 30% | ✅ pass |
| E/P dummy | 10A | 0.17 | 0.19 | 0.017 | 30% | ✅ pass |
| E/P dummy | 10B | 0.23 | 0.25 | 0.016 | 30% | ✅ pass |
| E(+)/P | 1A | 0.11 | 0.10 | 0.012 | 30% | ✅ pass |
| E(+)/P | 1B | 0.12 | 0.10 | 0.017 | 30% | ✅ pass |
| E(+)/P | 2 | 0.10 | 0.10 | 0.002 | 30% | ✅ pass |
| E(+)/P | 3 | 0.10 | 0.10 | 0.002 | 30% | ✅ pass |
| E(+)/P | 4 | 0.10 | 0.10 | 0.001 | 30% | ✅ pass |
| E(+)/P | 5 | 0.10 | 0.10 | 0.001 | 30% | ✅ pass |
| E(+)/P | 6 | 0.10 | 0.10 | 0.002 | 30% | ✅ pass |
| E(+)/P | 7 | 0.09 | 0.10 | 0.007 | 30% | ✅ pass |
| E(+)/P | 8 | 0.10 | 0.10 | 0.005 | 30% | ✅ pass |
| E(+)/P | 9 | 0.09 | 0.09 | 0.005 | 30% | ✅ pass |
| E(+)/P | 10A | 0.09 | 0.09 | 0.002 | 30% | ✅ pass |
| E(+)/P | 10B | 0.08 | 0.08 | 0.004 | 30% | ✅ pass |
| Firms | 1A | 116 | 135 | 19.4 | 20% | ✅ pass |
| Firms | 1B | 80 | 93 | 13.1 | 20% | ✅ pass |
| Firms | 2 | 185 | 214 | 28.6 | 20% | ✅ pass |
| Firms | 3 | 181 | 199 | 17.8 | 20% | ✅ pass |
| Firms | 4 | 179 | 193 | 14.4 | 20% | ✅ pass |
| Firms | 5 | 182 | 200 | 18.4 | 20% | ✅ pass |
| Firms | 6 | 185 | 202 | 17.0 | 20% | ✅ pass |
| Firms | 7 | 205 | 225 | 19.6 | 20% | ✅ pass |
| Firms | 8 | 227 | 238 | 11.4 | 20% | ✅ pass |
| Firms | 9 | 267 | 279 | 12.1 | 20% | ✅ pass |
| Firms | 10A | 165 | 175 | 10.2 | 20% | ✅ pass |
| Firms | 10B | 291 | 302 | 11.3 | 20% | ✅ pass |

## Overall summary

- **Targeted cells: 168/194 pass** (tolerances: Return 25%, β 15%, ln-ratios 10%, E/P rows 30%, Firms 20%; from preparations/tables_to_replicate.json).
  - Panel A: 79/96 pass.
  - Panel B: 89/98 pass.
- No-target cells (shown, not scored): 22 (Panel A E(+)/P ×12; Panel B interior Return ×10).
- **Failing cells (26):**
  - Panel A ln(BE/ME) 1A: ours -0.02 vs paper -0.01 (|Δ| 0.006, 55.1% > 10%).
  - Panel A ln(BE/ME) 4: ours -0.28 vs paper -0.32 (|Δ| 0.036, 11.2% > 10%).
  - Panel A ln(BE/ME) 5: ours -0.32 vs paper -0.36 (|Δ| 0.040, 11.0% > 10%).
  - Panel A ln(BE/ME) 6: ours -0.35 vs paper -0.44 (|Δ| 0.093, 21.2% > 10%).
  - Panel A ln(BE/ME) 9: ours -0.42 vs paper -0.51 (|Δ| 0.091, 17.8% > 10%).
  - Panel A ln(BE/ME) 10A: ours -0.51 vs paper -0.65 (|Δ| 0.135, 20.8% > 10%).
  - Panel A ln(A/ME) 3: ours 0.49 vs paper 0.43 (|Δ| 0.057, 13.2% > 10%).
  - Panel A ln(A/ME) 4: ours 0.44 vs paper 0.37 (|Δ| 0.070, 18.8% > 10%).
  - Panel A ln(A/ME) 5: ours 0.40 vs paper 0.32 (|Δ| 0.082, 25.7% > 10%).
  - Panel A ln(A/ME) 6: ours 0.37 vs paper 0.24 (|Δ| 0.134, 56.0% > 10%).
  - Panel A ln(A/ME) 8: ours 0.31 vs paper 0.27 (|Δ| 0.035, 13.0% > 10%).
  - Panel A ln(A/ME) 9: ours 0.30 vs paper 0.17 (|Δ| 0.129, 75.6% > 10%).
  - Panel A ln(A/ME) 10A: ours 0.18 vs paper -0.03 (|Δ| 0.214, 713.0% > 10%).
  - Panel A ln(A/ME) 10B: ours -0.06 vs paper -0.03 (|Δ| 0.032, 108.1% > 10%).
  - Panel A ln(A/BE) 10A: ours 0.70 vs paper 0.62 (|Δ| 0.079, 12.7% > 10%).
  - Panel A E/P dummy 8: ours 0.03 vs paper 0.02 (|Δ| 0.007, 34.1% > 30%).
  - Panel A E/P dummy 10A: ours 0.02 vs paper 0.01 (|Δ| 0.005, 52.6% > 30%).
  - Panel B ln(BE/ME) 1A: ours -0.20 vs paper -0.18 (|Δ| 0.021, 11.4% > 10%).
  - Panel B ln(BE/ME) 1B: ours -0.15 vs paper -0.13 (|Δ| 0.019, 14.9% > 10%).
  - Panel B ln(BE/ME) 7: ours -0.22 vs paper -0.25 (|Δ| 0.027, 10.8% > 10%).
  - Panel B ln(A/ME) 2: ours 0.54 vs paper 0.49 (|Δ| 0.050, 10.2% > 10%).
  - Panel B ln(A/ME) 5: ours 0.47 vs paper 0.42 (|Δ| 0.048, 11.4% > 10%).
  - Panel B ln(A/ME) 7: ours 0.48 vs paper 0.42 (|Δ| 0.055, 13.2% > 10%).
  - Panel B ln(A/ME) 9: ours 0.51 vs paper 0.46 (|Δ| 0.047, 10.2% > 10%).
  - Panel B ln(A/ME) 10B: ours 0.38 vs paper 0.31 (|Δ| 0.068, 22.0% > 10%).
  - Panel B E/P dummy 1B: ours 0.09 vs paper 0.06 (|Δ| 0.026, 43.7% > 30%).
- Identity check ln(A/ME)−ln(A/BE)=ln(BE/ME): max discrepancy 1.67e-16 across all 24 portfolio cells.
- Months covered: 330 (paper = 330).

---
*Computed by src/table_2.py from data/panel.parquet (iteration-1 pipeline). All statistics are time-series means of monthly cross-sectional portfolio means; Firms is the mean monthly member count. No-target cells reflect OCR gaps noted in preparations/tables_to_replicate.json.*