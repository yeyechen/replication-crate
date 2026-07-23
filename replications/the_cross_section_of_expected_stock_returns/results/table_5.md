# Table V — Fama & French (1992), The Cross-Section of Expected Stock Returns

Average monthly equal-weighted returns (%, July 1963 – December 1990, 330 months) on the size × BE/ME portfolio matrix. In June of each year t, stocks meeting the CRSP–COMPUSTAT data requirements are allocated to 10 size portfolios using the NYSE ME breakpoints; the stocks in each size decile are then sorted into 10 BE/ME portfolios using book-to-market ratios for year t−1 (within-decile breakpoints on all data-qualified stocks, L1818). Rows: size (All, Small-ME = decile 1, …, Large-ME = decile 10). Columns: BE/ME (All, Low = group 1, …, High = group 10).

**Cell construction.** *Interior (100 cells)*: time-series mean over the 330 months of the monthly EW return ×100 (stock-level mean of valid returns within each (month, size decile, BE/ME group)). *"All" column*: the EW size-decile portfolios — reuses the Table I stock-level size_1..size_10 series (data/agg_portfolio_returns.parquet), identical to the Table I Panel A All column. *"All" row*: EW portfolios of each BE/ME group pooling size deciles, computed at the stock level (mean(ret) per (month, BE/ME group) — the group is the second component of the size_beme label, e.g. "3_7" → group 7 — then time-series mean ×100; NOT the mean of the 10 decile cells). *All/All*: the grand EW series.

## Replicated 11×11 matrix (% per month)

| Size \ BE/ME | All | Low | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | High |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| All | 1.19 | 0.72 | 0.88 | 1.01 | 1.11 | 1.23 | 1.18 | 1.36 | 1.38 | 1.49 | 1.56 |
| Small-ME | 1.48 | 0.90 | 1.10 | 1.21 | 1.46 | 1.54 | 1.50 | 1.68 | 1.63 | 1.77 | 1.95 |
| ME-2 | 1.20 | 0.57 | 0.91 | 1.23 | 0.98 | 1.41 | 1.11 | 1.48 | 1.30 | 1.41 | 1.60 |
| ME-3 | 1.24 | 0.22 | 1.14 | 1.11 | 1.07 | 1.12 | 1.35 | 1.58 | 1.78 | 1.66 | 1.36 |
| ME-4 | 1.24 | 0.60 | 0.81 | 1.35 | 1.33 | 1.40 | 1.06 | 1.45 | 1.37 | 1.55 | 1.50 |
| ME-5 | 1.29 | 0.89 | 1.05 | 1.19 | 1.51 | 1.23 | 1.32 | 1.35 | 1.51 | 1.43 | 1.46 |
| ME-6 | 1.13 | 0.85 | 0.82 | 1.09 | 0.95 | 1.16 | 1.05 | 1.17 | 1.35 | 1.38 | 1.46 |
| ME-7 | 1.08 | 0.96 | 0.96 | 0.88 | 0.92 | 1.03 | 0.91 | 1.17 | 1.21 | 1.27 | 1.41 |
| ME-8 | 1.08 | 1.00 | 0.86 | 0.94 | 0.82 | 0.98 | 0.94 | 1.15 | 1.08 | 1.41 | 1.54 |
| ME-9 | 0.93 | 0.67 | 0.72 | 0.97 | 1.12 | 1.08 | 0.78 | 0.89 | 0.95 | 0.90 | 1.21 |
| Large-ME | 0.87 | 0.88 | 0.83 | 0.83 | 0.75 | 0.87 | 0.77 | 0.88 | 0.81 | 0.95 | 1.07 |

## Comparison with paper

**Full-metric pass/fail: 110/121 targeted cells pass** (tolerance 25% everywhere).

**All row (BE/ME portfolios pooling size)**

| Row | Col | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| All | All | 1.23 | 1.19 | 0.037 | 25% | ✅ pass |
| All | Low | 0.64 | 0.72 | 0.084 | 25% | ✅ pass |
| All | 2 | 0.98 | 0.88 | 0.098 | 25% | ✅ pass |
| All | 3 | 1.06 | 1.01 | 0.046 | 25% | ✅ pass |
| All | 4 | 1.17 | 1.11 | 0.061 | 25% | ✅ pass |
| All | 5 | 1.24 | 1.23 | 0.010 | 25% | ✅ pass |
| All | 6 | 1.26 | 1.18 | 0.082 | 25% | ✅ pass |
| All | 7 | 1.39 | 1.36 | 0.029 | 25% | ✅ pass |
| All | 8 | 1.40 | 1.38 | 0.018 | 25% | ✅ pass |
| All | 9 | 1.50 | 1.49 | 0.013 | 25% | ✅ pass |
| All | High | 1.63 | 1.56 | 0.068 | 25% | ✅ pass |

**All column (size portfolios)**

| Row | Col | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| All | All | 1.23 | 1.19 | 0.037 | 25% | ✅ pass |
| Small-ME | All | 1.47 | 1.48 | 0.008 | 25% | ✅ pass |
| ME-2 | All | 1.22 | 1.20 | 0.020 | 25% | ✅ pass |
| ME-3 | All | 1.22 | 1.24 | 0.018 | 25% | ✅ pass |
| ME-4 | All | 1.19 | 1.24 | 0.049 | 25% | ✅ pass |
| ME-5 | All | 1.24 | 1.29 | 0.053 | 25% | ✅ pass |
| ME-6 | All | 1.15 | 1.13 | 0.020 | 25% | ✅ pass |
| ME-7 | All | 1.07 | 1.08 | 0.006 | 25% | ✅ pass |
| ME-8 | All | 1.08 | 1.08 | 0.003 | 25% | ✅ pass |
| ME-9 | All | 0.95 | 0.93 | 0.020 | 25% | ✅ pass |
| Large-ME | All | 0.89 | 0.87 | 0.024 | 25% | ✅ pass |

**Small-ME row (size decile 1)**

| Row | Col | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Small-ME | All | 1.47 | 1.48 | 0.008 | 25% | ✅ pass |
| Small-ME | Low | 0.70 | 0.90 | 0.204 | 25% | ❌ FAIL |
| Small-ME | 2 | 1.14 | 1.10 | 0.042 | 25% | ✅ pass |
| Small-ME | 3 | 1.20 | 1.21 | 0.006 | 25% | ✅ pass |
| Small-ME | 4 | 1.43 | 1.46 | 0.032 | 25% | ✅ pass |
| Small-ME | 5 | 1.56 | 1.54 | 0.021 | 25% | ✅ pass |
| Small-ME | 6 | 1.51 | 1.50 | 0.009 | 25% | ✅ pass |
| Small-ME | 7 | 1.70 | 1.68 | 0.015 | 25% | ✅ pass |
| Small-ME | 8 | 1.71 | 1.63 | 0.082 | 25% | ✅ pass |
| Small-ME | 9 | 1.82 | 1.77 | 0.052 | 25% | ✅ pass |
| Small-ME | High | 1.92 | 1.95 | 0.033 | 25% | ✅ pass |

**Large-ME row (size decile 10)**

| Row | Col | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| Large-ME | All | 0.89 | 0.87 | 0.024 | 25% | ✅ pass |
| Large-ME | Low | 0.93 | 0.88 | 0.049 | 25% | ✅ pass |
| Large-ME | 2 | 0.88 | 0.83 | 0.053 | 25% | ✅ pass |
| Large-ME | 3 | 0.84 | 0.83 | 0.006 | 25% | ✅ pass |
| Large-ME | 4 | 0.71 | 0.75 | 0.042 | 25% | ✅ pass |
| Large-ME | 5 | 0.79 | 0.87 | 0.080 | 25% | ✅ pass |
| Large-ME | 6 | 0.83 | 0.77 | 0.055 | 25% | ✅ pass |
| Large-ME | 7 | 0.81 | 0.88 | 0.073 | 25% | ✅ pass |
| Large-ME | 8 | 0.96 | 0.81 | 0.148 | 25% | ✅ pass |
| Large-ME | 9 | 0.97 | 0.95 | 0.021 | 25% | ✅ pass |
| Large-ME | High | 1.18 | 1.07 | 0.107 | 25% | ✅ pass |

## Headline spreads

- **Within-decile BE/ME spread** (All row, High − Low): ours 1.56 − 0.72 = **0.84%/mo** (paper 1.63 − 0.64 = 0.99%/mo).
- **Size spread** (All column, Small-ME − Large-ME): ours 1.48 − 0.87 = **0.61%/mo** (paper 1.47 − 0.89 = 0.58%/mo).

## Overall summary

- **Targeted cells: 110/121 pass** (25% tolerance, from preparations/tables_to_replicate.json).
- By slice: All row 11/11, All column 11/11, Small-ME row 10/11, Large-ME row 11/11, interior 100 cells 89/100.
- **Failing cells (11):**
  - Small-ME × Low: ours 0.90 vs paper 0.70 (|Δ| 0.204, 29.1% > 25%).
  - ME-2 × Low: ours 0.57 vs paper 0.43 (|Δ| 0.136, 31.6% > 25%).
  - ME-2 × 3: ours 1.23 vs paper 0.96 (|Δ| 0.272, 28.4% > 25%).
  - ME-3 × Low: ours 0.22 vs paper 0.56 (|Δ| 0.339, 60.5% > 25%).
  - ME-3 × 2: ours 1.14 vs paper 0.88 (|Δ| 0.256, 29.0% > 25%).
  - ME-3 × 8: ours 1.78 vs paper 1.40 (|Δ| 0.381, 27.2% > 25%).
  - ME-4 × Low: ours 0.60 vs paper 0.39 (|Δ| 0.214, 54.9% > 25%).
  - ME-4 × 3: ours 1.35 vs paper 1.06 (|Δ| 0.293, 27.6% > 25%).
  - ME-5 × 2: ours 1.05 vs paper 0.65 (|Δ| 0.396, 60.9% > 25%).
  - ME-8 × Low: ours 1.00 vs paper 0.66 (|Δ| 0.343, 52.0% > 25%).
  - ME-9 × Low: ours 0.67 vs paper 0.44 (|Δ| 0.231, 52.4% > 25%).
- Months covered: 330 (paper = 330); every one of the 100 size×BE/ME cells exists in 330–330 months (all 330).

## Notes / flags

1. Stock-level aggregation matters for the margins: the All row is the EW over pooled stocks, not the mean of the 10 decile cells (cells hold 13–3,700+ stocks/month), and the All column/All-All cell reuse the exact Table I stock-level series (verified in iteration 2: stock-level grand EW ≠ simple mean of the 100 cells).
2. Returns are computed from the same delisting-adjusted CRSP returns as Tables I/II/IV (assumption 5); no methodology change. The within-decile BE/ME breakpoints use all data-qualified stocks (assumption 8, paper-specified for Table V).
3. ⚠️ 11 failing cells, of which 6 are in the Low-BE/ME column (within-decile growth portfolios of the small/mid size deciles — the thinnest cells, where this extract's ~5.5% extra firms and different Compustat link table move the EW mean most; e.g. ME-3×Low 0.22 vs 0.56). All margin cells pass: the All row (11/11), the All column (11/11, the Table I size series) and the Large-ME row (11/11); both headline spreads replicate (within-decile 0.84 vs 0.99; size 0.61 vs 0.58). Reported as fact; no methodology changed — see the full comparison appendix for exact deviations.

## Appendix: full 121-cell comparison

| Row | Col | Paper | Ours | \|Δ\| | Tol | Result |
|---|---|---:|---:|---:|---:|:---:|
| All | All | 1.23 | 1.19 | 0.037 | 25% | ✅ pass |
| All | Low | 0.64 | 0.72 | 0.084 | 25% | ✅ pass |
| All | 2 | 0.98 | 0.88 | 0.098 | 25% | ✅ pass |
| All | 3 | 1.06 | 1.01 | 0.046 | 25% | ✅ pass |
| All | 4 | 1.17 | 1.11 | 0.061 | 25% | ✅ pass |
| All | 5 | 1.24 | 1.23 | 0.010 | 25% | ✅ pass |
| All | 6 | 1.26 | 1.18 | 0.082 | 25% | ✅ pass |
| All | 7 | 1.39 | 1.36 | 0.029 | 25% | ✅ pass |
| All | 8 | 1.40 | 1.38 | 0.018 | 25% | ✅ pass |
| All | 9 | 1.50 | 1.49 | 0.013 | 25% | ✅ pass |
| All | High | 1.63 | 1.56 | 0.068 | 25% | ✅ pass |
| Small-ME | All | 1.47 | 1.48 | 0.008 | 25% | ✅ pass |
| Small-ME | Low | 0.70 | 0.90 | 0.204 | 25% | ❌ FAIL |
| Small-ME | 2 | 1.14 | 1.10 | 0.042 | 25% | ✅ pass |
| Small-ME | 3 | 1.20 | 1.21 | 0.006 | 25% | ✅ pass |
| Small-ME | 4 | 1.43 | 1.46 | 0.032 | 25% | ✅ pass |
| Small-ME | 5 | 1.56 | 1.54 | 0.021 | 25% | ✅ pass |
| Small-ME | 6 | 1.51 | 1.50 | 0.009 | 25% | ✅ pass |
| Small-ME | 7 | 1.70 | 1.68 | 0.015 | 25% | ✅ pass |
| Small-ME | 8 | 1.71 | 1.63 | 0.082 | 25% | ✅ pass |
| Small-ME | 9 | 1.82 | 1.77 | 0.052 | 25% | ✅ pass |
| Small-ME | High | 1.92 | 1.95 | 0.033 | 25% | ✅ pass |
| ME-2 | All | 1.22 | 1.20 | 0.020 | 25% | ✅ pass |
| ME-2 | Low | 0.43 | 0.57 | 0.136 | 25% | ❌ FAIL |
| ME-2 | 2 | 1.05 | 0.91 | 0.136 | 25% | ✅ pass |
| ME-2 | 3 | 0.96 | 1.23 | 0.272 | 25% | ❌ FAIL |
| ME-2 | 4 | 1.19 | 0.98 | 0.215 | 25% | ✅ pass |
| ME-2 | 5 | 1.33 | 1.41 | 0.079 | 25% | ✅ pass |
| ME-2 | 6 | 1.19 | 1.11 | 0.085 | 25% | ✅ pass |
| ME-2 | 7 | 1.58 | 1.48 | 0.097 | 25% | ✅ pass |
| ME-2 | 8 | 1.28 | 1.30 | 0.021 | 25% | ✅ pass |
| ME-2 | 9 | 1.43 | 1.41 | 0.023 | 25% | ✅ pass |
| ME-2 | High | 1.79 | 1.60 | 0.192 | 25% | ✅ pass |
| ME-3 | All | 1.22 | 1.24 | 0.018 | 25% | ✅ pass |
| ME-3 | Low | 0.56 | 0.22 | 0.339 | 25% | ❌ FAIL |
| ME-3 | 2 | 0.88 | 1.14 | 0.256 | 25% | ❌ FAIL |
| ME-3 | 3 | 1.23 | 1.11 | 0.119 | 25% | ✅ pass |
| ME-3 | 4 | 0.95 | 1.07 | 0.116 | 25% | ✅ pass |
| ME-3 | 5 | 1.36 | 1.12 | 0.237 | 25% | ✅ pass |
| ME-3 | 6 | 1.30 | 1.35 | 0.049 | 25% | ✅ pass |
| ME-3 | 7 | 1.30 | 1.58 | 0.278 | 25% | ✅ pass |
| ME-3 | 8 | 1.40 | 1.78 | 0.381 | 25% | ❌ FAIL |
| ME-3 | 9 | 1.54 | 1.66 | 0.123 | 25% | ✅ pass |
| ME-3 | High | 1.60 | 1.36 | 0.244 | 25% | ✅ pass |
| ME-4 | All | 1.19 | 1.24 | 0.049 | 25% | ✅ pass |
| ME-4 | Low | 0.39 | 0.60 | 0.214 | 25% | ❌ FAIL |
| ME-4 | 2 | 0.72 | 0.81 | 0.087 | 25% | ✅ pass |
| ME-4 | 3 | 1.06 | 1.35 | 0.293 | 25% | ❌ FAIL |
| ME-4 | 4 | 1.36 | 1.33 | 0.034 | 25% | ✅ pass |
| ME-4 | 5 | 1.13 | 1.40 | 0.275 | 25% | ✅ pass |
| ME-4 | 6 | 1.21 | 1.06 | 0.149 | 25% | ✅ pass |
| ME-4 | 7 | 1.34 | 1.45 | 0.108 | 25% | ✅ pass |
| ME-4 | 8 | 1.59 | 1.37 | 0.217 | 25% | ✅ pass |
| ME-4 | 9 | 1.51 | 1.55 | 0.035 | 25% | ✅ pass |
| ME-4 | High | 1.47 | 1.50 | 0.030 | 25% | ✅ pass |
| ME-5 | All | 1.24 | 1.29 | 0.053 | 25% | ✅ pass |
| ME-5 | Low | 0.88 | 0.89 | 0.006 | 25% | ✅ pass |
| ME-5 | 2 | 0.65 | 1.05 | 0.396 | 25% | ❌ FAIL |
| ME-5 | 3 | 1.08 | 1.19 | 0.114 | 25% | ✅ pass |
| ME-5 | 4 | 1.47 | 1.51 | 0.037 | 25% | ✅ pass |
| ME-5 | 5 | 1.13 | 1.23 | 0.101 | 25% | ✅ pass |
| ME-5 | 6 | 1.43 | 1.32 | 0.111 | 25% | ✅ pass |
| ME-5 | 7 | 1.44 | 1.35 | 0.086 | 25% | ✅ pass |
| ME-5 | 8 | 1.26 | 1.51 | 0.255 | 25% | ✅ pass |
| ME-5 | 9 | 1.52 | 1.43 | 0.092 | 25% | ✅ pass |
| ME-5 | High | 1.49 | 1.46 | 0.032 | 25% | ✅ pass |
| ME-6 | All | 1.15 | 1.13 | 0.020 | 25% | ✅ pass |
| ME-6 | Low | 0.70 | 0.85 | 0.155 | 25% | ✅ pass |
| ME-6 | 2 | 0.98 | 0.82 | 0.155 | 25% | ✅ pass |
| ME-6 | 3 | 1.14 | 1.09 | 0.050 | 25% | ✅ pass |
| ME-6 | 4 | 1.23 | 0.95 | 0.275 | 25% | ✅ pass |
| ME-6 | 5 | 0.94 | 1.16 | 0.222 | 25% | ✅ pass |
| ME-6 | 6 | 1.27 | 1.05 | 0.224 | 25% | ✅ pass |
| ME-6 | 7 | 1.19 | 1.17 | 0.021 | 25% | ✅ pass |
| ME-6 | 8 | 1.19 | 1.35 | 0.155 | 25% | ✅ pass |
| ME-6 | 9 | 1.24 | 1.38 | 0.142 | 25% | ✅ pass |
| ME-6 | High | 1.50 | 1.46 | 0.036 | 25% | ✅ pass |
| ME-7 | All | 1.07 | 1.08 | 0.006 | 25% | ✅ pass |
| ME-7 | Low | 0.95 | 0.96 | 0.013 | 25% | ✅ pass |
| ME-7 | 2 | 1.00 | 0.96 | 0.044 | 25% | ✅ pass |
| ME-7 | 3 | 0.99 | 0.88 | 0.106 | 25% | ✅ pass |
| ME-7 | 4 | 0.83 | 0.92 | 0.092 | 25% | ✅ pass |
| ME-7 | 5 | 0.99 | 1.03 | 0.042 | 25% | ✅ pass |
| ME-7 | 6 | 1.13 | 0.91 | 0.223 | 25% | ✅ pass |
| ME-7 | 7 | 0.99 | 1.17 | 0.184 | 25% | ✅ pass |
| ME-7 | 8 | 1.16 | 1.21 | 0.054 | 25% | ✅ pass |
| ME-7 | 9 | 1.10 | 1.27 | 0.169 | 25% | ✅ pass |
| ME-7 | High | 1.47 | 1.41 | 0.062 | 25% | ✅ pass |
| ME-8 | All | 1.08 | 1.08 | 0.003 | 25% | ✅ pass |
| ME-8 | Low | 0.66 | 1.00 | 0.343 | 25% | ❌ FAIL |
| ME-8 | 2 | 1.13 | 0.86 | 0.273 | 25% | ✅ pass |
| ME-8 | 3 | 0.91 | 0.94 | 0.032 | 25% | ✅ pass |
| ME-8 | 4 | 0.95 | 0.82 | 0.127 | 25% | ✅ pass |
| ME-8 | 5 | 0.99 | 0.98 | 0.007 | 25% | ✅ pass |
| ME-8 | 6 | 1.01 | 0.94 | 0.070 | 25% | ✅ pass |
| ME-8 | 7 | 1.15 | 1.15 | 0.002 | 25% | ✅ pass |
| ME-8 | 8 | 1.05 | 1.08 | 0.029 | 25% | ✅ pass |
| ME-8 | 9 | 1.29 | 1.41 | 0.120 | 25% | ✅ pass |
| ME-8 | High | 1.55 | 1.54 | 0.015 | 25% | ✅ pass |
| ME-9 | All | 0.95 | 0.93 | 0.020 | 25% | ✅ pass |
| ME-9 | Low | 0.44 | 0.67 | 0.231 | 25% | ❌ FAIL |
| ME-9 | 2 | 0.89 | 0.72 | 0.173 | 25% | ✅ pass |
| ME-9 | 3 | 0.92 | 0.97 | 0.048 | 25% | ✅ pass |
| ME-9 | 4 | 1.00 | 1.12 | 0.122 | 25% | ✅ pass |
| ME-9 | 5 | 1.05 | 1.08 | 0.033 | 25% | ✅ pass |
| ME-9 | 6 | 0.93 | 0.78 | 0.147 | 25% | ✅ pass |
| ME-9 | 7 | 0.82 | 0.89 | 0.074 | 25% | ✅ pass |
| ME-9 | 8 | 1.11 | 0.95 | 0.163 | 25% | ✅ pass |
| ME-9 | 9 | 1.04 | 0.90 | 0.137 | 25% | ✅ pass |
| ME-9 | High | 1.22 | 1.21 | 0.007 | 25% | ✅ pass |
| Large-ME | All | 0.89 | 0.87 | 0.024 | 25% | ✅ pass |
| Large-ME | Low | 0.93 | 0.88 | 0.049 | 25% | ✅ pass |
| Large-ME | 2 | 0.88 | 0.83 | 0.053 | 25% | ✅ pass |
| Large-ME | 3 | 0.84 | 0.83 | 0.006 | 25% | ✅ pass |
| Large-ME | 4 | 0.71 | 0.75 | 0.042 | 25% | ✅ pass |
| Large-ME | 5 | 0.79 | 0.87 | 0.080 | 25% | ✅ pass |
| Large-ME | 6 | 0.83 | 0.77 | 0.055 | 25% | ✅ pass |
| Large-ME | 7 | 0.81 | 0.88 | 0.073 | 25% | ✅ pass |
| Large-ME | 8 | 0.96 | 0.81 | 0.148 | 25% | ✅ pass |
| Large-ME | 9 | 0.97 | 0.95 | 0.021 | 25% | ✅ pass |
| Large-ME | High | 1.18 | 1.07 | 0.107 | 25% | ✅ pass |

---
*Computed by src/table_5.py from data/panel.parquet (size_beme labels, iteration-1 pipeline) and data/agg_portfolio_returns.parquet (All column + All/All). Returns are time-series means of monthly stock-level EW returns ×100.*