# Table VI — Fama & French (1992), The Cross-Section of Expected Stock Returns

Means, standard deviations, and t-statistics of monthly returns on the NYSE value-weighted (VW) and equal-weighted (EW) portfolios, and of the slopes and intercepts of two Fama-MacBeth regressions, for the full period and two subperiods:

- **reg(a):** return on ln(ME) and ln(BE/ME);
- **reg(b):** return on β, ln(ME), and ln(BE/ME).

**Methodology.** Same as Table III: raw monthly returns, monthly OLS with intercept, ln(BE/ME) clipped at the monthly 0.005/0.995 fractiles (β and ln(ME) not winsorized), plain time-series statistics (no Newey-West). Per coefficient: Mean = time-series mean of the monthly estimates ×100, Std = time-series SD ×100, t(Mn) = Mean / (Std / √N_months), all in percent/month. Subperiod splits: July 1963 – December 1976 (162 months) and January 1977 – December 1990 (168 months). NYSE benchmarks: all NYSE common stocks (PIT exchcd = 1, shrcd 10/11, NOT restricted to the Compustat-data-eligible subset) with delisting-adjusted returns (Assumptions 5 and 10); EW = mean of valid monthly returns, VW = sum(prior-month-end ME × return) / sum(prior-month-end ME) over stocks with a valid return and a valid lagged ME (cached in data/nyse_benchmark_returns.parquet). NYSE membership is screened point-in-time at each calendar month-end, so mid-month delistings are excluded from that month's benchmark.

## Replicated values

| Row | **July 1963 – Dec. 1990** |  |  | **July 1963 – Dec. 1976** |  |  | **Jan. 1977 – Dec. 1990** |  |  |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|  | **Mean** | **Std** | **t(Mn)** | **Mean** | **Std** | **t(Mn)** | **Mean** | **Std** | **t(Mn)** |
| NYSE VW | 0.92 | 4.47 | 3.72 | 0.65 | 4.30 | 1.93 | 1.17 | 4.64 | 3.27 |
| NYSE EW | 1.15 | 5.60 | 3.72 | 0.97 | 5.83 | 2.11 | 1.32 | 5.37 | 3.18 |
| **(a) ret ~ ln(ME), ln(BE/ME)** |  |  |  |  |  |  |  |  |  |
| intercept | 1.72 | 8.43 | 3.70 | 1.73 | 10.02 | 2.20 | 1.71 | 6.58 | 3.36 |
| b2 ln(ME) | -0.11 | 1.02 | -1.92 | -0.14 | 1.24 | -1.47 | -0.07 | 0.75 | -1.27 |
| b3 ln(BE/ME) | 0.34 | 1.48 | 4.20 | 0.32 | 1.57 | 2.58 | 0.36 | 1.39 | 3.40 |
| **(b) ret ~ β, ln(ME), ln(BE/ME)** |  |  |  |  |  |  |  |  |  |
| intercept | 2.07 | 5.63 | 6.67 | 1.66 | 6.12 | 3.46 | 2.46 | 5.10 | 6.24 |
| b1 β | -0.21 | 5.11 | -0.73 | 0.08 | 5.38 | 0.20 | -0.48 | 4.83 | -1.30 |
| b2 ln(ME) | -0.12 | 0.90 | -2.45 | -0.14 | 1.02 | -1.81 | -0.10 | 0.76 | -1.66 |
| b3 ln(BE/ME) | 0.32 | 1.27 | 4.50 | 0.31 | 1.41 | 2.77 | 0.32 | 1.13 | 3.71 |

## Comparison with paper

**Table VI: 78/81 targeted cells pass**.
Failing cells (3):
- NYSE VW [7/63-12/76] mean: ours 0.65 vs paper 0.56 (|Δ| 0.09, 16.2% > 15%).
- NYSE EW [7/63-12/90] mean: ours 1.15 vs paper 0.97 (|Δ| 0.18, 18.2% > 15%).
- NYSE EW [7/63-12/76] mean: ours 0.97 vs paper 0.77 (|Δ| 0.20, 25.6% > 15%).

Tolerances (preparations/tables_to_replicate.json): NYSE Mean 15%, Std 10%, t(Mn) 40%; FM intercept/slope Mean 40%, Std 10%, t(Mn) 40%.

| Cell | Stat | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| NYSE VW [7/63-12/90] | mean | 0.81 | 0.92 | 0.11 | 15% | ✅ pass |
| NYSE VW [7/63-12/90] | std | 4.47 | 4.47 | 0.00 | 10% | ✅ pass |
| NYSE VW [7/63-12/90] | t | 3.27 | 3.72 | 0.45 | 40% | ✅ pass |
| NYSE VW [7/63-12/76] | mean | 0.56 | 0.65 | 0.09 | 15% | ❌ FAIL |
| NYSE VW [7/63-12/76] | std | 4.26 | 4.30 | 0.04 | 10% | ✅ pass |
| NYSE VW [7/63-12/76] | t | 1.67 | 1.93 | 0.26 | 40% | ✅ pass |
| NYSE VW [1/77-12/90] | mean | 1.04 | 1.17 | 0.13 | 15% | ✅ pass |
| NYSE VW [1/77-12/90] | std | 4.66 | 4.64 | 0.02 | 10% | ✅ pass |
| NYSE VW [1/77-12/90] | t | 2.89 | 3.27 | 0.38 | 40% | ✅ pass |
| NYSE EW [7/63-12/90] | mean | 0.97 | 1.15 | 0.18 | 15% | ❌ FAIL |
| NYSE EW [7/63-12/90] | std | 5.49 | 5.60 | 0.11 | 10% | ✅ pass |
| NYSE EW [7/63-12/90] | t | 3.19 | 3.72 | 0.53 | 40% | ✅ pass |
| NYSE EW [7/63-12/76] | mean | 0.77 | 0.97 | 0.20 | 15% | ❌ FAIL |
| NYSE EW [7/63-12/76] | std | 5.70 | 5.83 | 0.13 | 10% | ✅ pass |
| NYSE EW [7/63-12/76] | t | 1.72 | 2.11 | 0.39 | 40% | ✅ pass |
| NYSE EW [1/77-12/90] | mean | 1.15 | 1.32 | 0.17 | 15% | ✅ pass |
| NYSE EW [1/77-12/90] | std | 5.28 | 5.37 | 0.09 | 10% | ✅ pass |
| NYSE EW [1/77-12/90] | t | 2.82 | 3.18 | 0.36 | 40% | ✅ pass |
| reg(a) intercept [7/63-12/90] | mean | 1.77 | 1.72 | 0.05 | 40% | ✅ pass |
| reg(a) intercept [7/63-12/90] | std | 8.51 | 8.43 | 0.08 | 10% | ✅ pass |
| reg(a) intercept [7/63-12/90] | t | 3.77 | 3.70 | 0.07 | 40% | ✅ pass |
| reg(a) intercept [7/63-12/76] | mean | 1.86 | 1.73 | 0.13 | 40% | ✅ pass |
| reg(a) intercept [7/63-12/76] | std | 10.10 | 10.02 | 0.08 | 10% | ✅ pass |
| reg(a) intercept [7/63-12/76] | t | 2.33 | 2.20 | 0.13 | 40% | ✅ pass |
| reg(a) intercept [1/77-12/90] | mean | 1.69 | 1.71 | 0.02 | 40% | ✅ pass |
| reg(a) intercept [1/77-12/90] | std | 6.67 | 6.58 | 0.09 | 10% | ✅ pass |
| reg(a) intercept [1/77-12/90] | t | 3.27 | 3.36 | 0.09 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/90] | mean | -0.11 | -0.11 | 0.00 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/90] | std | 1.02 | 1.02 | 0.00 | 10% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/90] | t | -1.99 | -1.92 | 0.07 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/76] | mean | -0.16 | -0.14 | 0.02 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/76] | std | 1.25 | 1.24 | 0.01 | 10% | ✅ pass |
| reg(a) b2 ln(ME) [7/63-12/76] | t | -1.62 | -1.47 | 0.15 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [1/77-12/90] | mean | -0.07 | -0.07 | 0.00 | 40% | ✅ pass |
| reg(a) b2 ln(ME) [1/77-12/90] | std | 0.73 | 0.75 | 0.02 | 10% | ✅ pass |
| reg(a) b2 ln(ME) [1/77-12/90] | t | -1.16 | -1.27 | 0.11 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/90] | mean | 0.35 | 0.34 | 0.01 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/90] | std | 1.45 | 1.48 | 0.03 | 10% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/90] | t | 4.43 | 4.20 | 0.23 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/76] | mean | 0.36 | 0.32 | 0.04 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/76] | std | 1.53 | 1.57 | 0.04 | 10% | ✅ pass |
| reg(a) b3 ln(BE/ME) [7/63-12/76] | t | 2.96 | 2.58 | 0.38 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [1/77-12/90] | mean | 0.35 | 0.36 | 0.01 | 40% | ✅ pass |
| reg(a) b3 ln(BE/ME) [1/77-12/90] | std | 1.37 | 1.39 | 0.02 | 10% | ✅ pass |
| reg(a) b3 ln(BE/ME) [1/77-12/90] | t | 3.30 | 3.40 | 0.10 | 40% | ✅ pass |
| reg(b) intercept [7/63-12/90] | mean | 2.07 | 2.07 | 0.00 | 40% | ✅ pass |
| reg(b) intercept [7/63-12/90] | std | 5.75 | 5.63 | 0.12 | 10% | ✅ pass |
| reg(b) intercept [7/63-12/90] | t | 6.55 | 6.67 | 0.12 | 40% | ✅ pass |
| reg(b) intercept [7/63-12/76] | mean | 1.73 | 1.66 | 0.07 | 40% | ✅ pass |
| reg(b) intercept [7/63-12/76] | std | 6.22 | 6.12 | 0.10 | 10% | ✅ pass |
| reg(b) intercept [7/63-12/76] | t | 3.54 | 3.46 | 0.08 | 40% | ✅ pass |
| reg(b) intercept [1/77-12/90] | mean | 2.40 | 2.46 | 0.06 | 40% | ✅ pass |
| reg(b) intercept [1/77-12/90] | std | 5.25 | 5.10 | 0.15 | 10% | ✅ pass |
| reg(b) intercept [1/77-12/90] | t | 5.92 | 6.24 | 0.32 | 40% | ✅ pass |
| reg(b) b1 β [7/63-12/90] | mean | -0.17 | -0.21 | 0.04 | 40% | ✅ pass |
| reg(b) b1 β [7/63-12/90] | std | 5.12 | 5.11 | 0.01 | 10% | ✅ pass |
| reg(b) b1 β [7/63-12/90] | t | -0.62 | -0.73 | 0.11 | 40% | ✅ pass |
| reg(b) b1 β [7/63-12/76] | mean | 0.10 | 0.08 | 0.02 | 40% | ✅ pass |
| reg(b) b1 β [7/63-12/76] | std | 5.33 | 5.38 | 0.05 | 10% | ✅ pass |
| reg(b) b1 β [7/63-12/76] | t | 0.25 | 0.20 | 0.05 | 40% | ✅ pass |
| reg(b) b1 β [1/77-12/90] | mean | -0.44 | -0.48 | 0.04 | 40% | ✅ pass |
| reg(b) b1 β [1/77-12/90] | std | 4.91 | 4.83 | 0.08 | 10% | ✅ pass |
| reg(b) b1 β [1/77-12/90] | t | -1.17 | -1.30 | 0.13 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/90] | mean | -0.12 | -0.12 | 0.00 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/90] | std | 0.89 | 0.90 | 0.01 | 10% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/90] | t | -2.52 | -2.45 | 0.07 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/76] | mean | -0.15 | -0.14 | 0.01 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/76] | std | 1.03 | 1.02 | 0.01 | 10% | ✅ pass |
| reg(b) b2 ln(ME) [7/63-12/76] | t | -1.91 | -1.81 | 0.10 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [1/77-12/90] | mean | -0.09 | -0.10 | 0.01 | 40% | ✅ pass |
| reg(b) b2 ln(ME) [1/77-12/90] | std | 0.74 | 0.76 | 0.02 | 10% | ✅ pass |
| reg(b) b2 ln(ME) [1/77-12/90] | t | -1.64 | -1.66 | 0.02 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/90] | mean | 0.33 | 0.32 | 0.01 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/90] | std | 1.24 | 1.27 | 0.03 | 10% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/90] | t | 4.80 | 4.50 | 0.30 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/76] | mean | 0.34 | 0.31 | 0.03 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/76] | std | 1.36 | 1.41 | 0.05 | 10% | ✅ pass |
| reg(b) b3 ln(BE/ME) [7/63-12/76] | t | 3.17 | 2.77 | 0.40 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [1/77-12/90] | mean | 0.31 | 0.32 | 0.01 | 40% | ✅ pass |
| reg(b) b3 ln(BE/ME) [1/77-12/90] | std | 1.10 | 1.13 | 0.03 | 10% | ✅ pass |
| reg(b) b3 ln(BE/ME) [1/77-12/90] | t | 3.67 | 3.71 | 0.04 | 40% | ✅ pass |

## Notes / flags

- **All 63 FM cells pass** (reg(a) and reg(b): intercepts, slopes, Stds, t(Mn) across the three periods), including the headline subperiod results: reg(b) β 0.08 (t 0.20) in 1963–76 and −0.48 (t −1.30) in 1977–90 (paper 0.10/0.25 and −0.44/−1.17); BE/ME slopes stable at 0.31–0.36 in both subperiods (paper 0.34–0.36).
- ⚠️ **NYSE benchmark means run ~0.1–0.2 %/mo above the paper** (the 3 failing cells: EW full 1.15 vs 0.97, EW 63–76 0.97 vs 0.77, VW 63–76 0.65 vs 0.56). The computation is validated against CRSP's own NYSE index in this extract (msia: VW 0.91/SD 4.46 vs our 0.92/SD 4.47), and the SDs match the paper's within ≤0.14 — the gap is a mean-level data-vintage shift (this CRSP vintage also runs ~0.1 above the paper on the combined msi index). Mid-month delistings are excluded from the month of delisting (month-end PIT membership screen); financials are included (NYSE market benchmark).
- NYSE VW/EW computed with delisting-adjusted returns per binding Assumptions 5/10; EW over valid returns, VW on prior-month-end ME.

---
*Computed by src/table_3_6.py. FM coefficients from data/panel.parquet; NYSE VW/EW from src/sql/nyse_benchmark.sql cached in data/nyse_benchmark_returns.parquet.*