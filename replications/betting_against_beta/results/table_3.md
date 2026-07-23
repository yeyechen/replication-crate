# Table 3 — Beta-sorted decile portfolios and BAB factor (US equities) — v2

**Source:** Frazzini & Pedersen (2014), "Betting Against Beta", Table 3.
**Sample:** 1928-08-01 .. 2012-03-01
(1004 months; portfolios start when betas become estimable).
**Weighting:** equal-weighted within decile, rebalanced monthly.
**Returns & alphas:** monthly percent. **Volatility & Sharpe:** annualized.

## v2 fixes (vs table_3.py v1)
1. **NYSE breakpoints** — decile breakpoints are the 10th..90th percentiles of
   beta among **NYSE (exchcd==1) stocks only** each month (PIT exchange code
   merged from `crsp_202601.dsenames`); all stocks are then assigned to deciles
   on those breakpoints. (Paper: "assigned to one of ten deciles portfolios
   based on NYSE breakpoints.")
2. **Delisting returns** — each stock's last-month return is combined with its
   CRSP delisting return from `crsp_202601.dsedelist`:
   `adjusted = (1+ret)(1+dlret_eff)-1`. `dlret_eff` = reported `dlret` when
   valid (`dlret > -1.0`, not NULL), else the Shumway(1997)/BMP(2007) imputation
   for performance-related delistings (dlstcd 500-599): -0.30 NYSE/AMEX,
   -0.55 NASDAQ. Both Case A (delisting month == last panel month) and Case B
   (delisting month == last panel month + 1, i.e. the delisting-month CRSP
   return is a missing sentinel) are applied.

## FF factor units
DECIMAL in source (median |mkt_rf|=0.0298) -> used as-is. CRSP `ret` is decimal, so excess = ret - rf with no extra scaling.

## Table 3

| Metric | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | BAB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Excess return | 0.94 | 0.97 | 1.05 | 1.01 | 1.09 | 1.18 | 1.09 | 1.14 | 1.09 | 1.06 | 0.71 |
| _t-stat_ | (6.67) | (5.80) | (5.43) | (4.92) | (4.67) | (4.64) | (4.01) | (3.87) | (3.35) | (2.70) | (6.85) |
| CAPM alpha | 0.55 | 0.46 | 0.45 | 0.36 | 0.35 | 0.37 | 0.23 | 0.21 | 0.08 | -0.08 | 0.75 |
| _t-stat_ | (6.38) | (5.66) | (5.10) | (4.22) | (3.57) | (3.50) | (1.99) | (1.67) | (0.52) | (-0.36) | (7.16) |
| 3-factor alpha | 0.49 | 0.39 | 0.35 | 0.25 | 0.21 | 0.22 | 0.06 | 0.02 | -0.13 | -0.35 | 0.75 |
| _t-stat_ | (7.07) | (6.51) | (6.03) | (4.88) | (3.71) | (3.60) | (0.99) | (0.34) | (-1.57) | (-2.34) | (7.11) |
| 4-factor alpha | 0.49 | 0.41 | 0.40 | 0.29 | 0.26 | 0.33 | 0.16 | 0.19 | 0.10 | 0.03 | 0.58 |
| _t-stat_ | (6.98) | (6.69) | (6.69) | (5.53) | (4.54) | (5.60) | (2.56) | (2.88) | (1.22) | (0.22) | (5.54) |
| Beta (ex ante) | 0.61 | 0.79 | 0.88 | 0.96 | 1.04 | 1.12 | 1.21 | 1.31 | 1.45 | 1.77 | 0.00 |
| Beta (realized) | 0.64 | 0.84 | 0.99 | 1.08 | 1.22 | 1.33 | 1.42 | 1.53 | 1.66 | 1.87 | -0.06 |
| Volatility | 15.45 | 18.35 | 21.17 | 22.49 | 25.63 | 27.87 | 29.75 | 32.25 | 35.62 | 42.84 | 11.44 |
| Sharpe ratio | 0.73 | 0.63 | 0.59 | 0.54 | 0.51 | 0.51 | 0.44 | 0.42 | 0.37 | 0.30 | 0.75 |

_t-stats below each coefficient are **standard (iid)** time-series t-stats,
matching the paper's convention. The excess-return t-stat uses mean/(std/sqrt(n))._

### Newey-West (HAC, 6 lags) alpha t-stats — supplementary

| Portfolio | CAPM t(NW) | FF3 t(NW) | FF4 t(NW) |
|---|---:|---:|---:|
| P1 | 5.78 | 6.34 | 6.19 |
| P5 | 3.51 | 4.02 | 4.92 |
| P10 | -0.36 | -2.23 | 0.18 |
| BAB | 5.52 | 5.71 | 4.44 |

## Validation vs paper (tolerance from tables_to_replicate.json)

| Portfolio | Metric | Ours | Paper | Tol % | Diff % | Pass |
|---|---|---:|---:|---:|---:|:--:|
| P1 | excess_ret | 0.940 | 0.910 | 15 | 3.3 | PASS |
| P1 | capm_alpha | 0.549 | 0.520 | 20 | 5.6 | PASS |
| P1 | ff3_alpha | 0.486 | 0.400 | 20 | 21.6 | FAIL |
| P1 | ff4_alpha | 0.490 | 0.400 | 20 | 22.5 | FAIL |
| P1 | beta_exante | 0.615 | 0.640 | 10 | 4.0 | PASS |
| P1 | beta_realized | 0.645 | 0.670 | 10 | 3.8 | PASS |
| P1 | vol | 15.452 | 15.700 | 10 | 1.6 | PASS |
| P1 | sharpe | 0.730 | 0.700 | 15 | 4.2 | PASS |
| P5 | excess_ret | 1.091 | 1.050 | 15 | 4.0 | PASS |
| P5 | capm_alpha | 0.350 | 0.340 | 20 | 3.1 | PASS |
| P5 | ff3_alpha | 0.214 | 0.130 | 20 | 64.6 | FAIL |
| P5 | ff4_alpha | 0.265 | 0.180 | 20 | 47.0 | FAIL |
| P5 | beta_exante | 1.043 | 1.050 | 10 | 0.7 | PASS |
| P5 | beta_realized | 1.223 | 1.220 | 10 | 0.2 | PASS |
| P5 | vol | 25.626 | 25.560 | 10 | 0.3 | PASS |
| P5 | sharpe | 0.511 | 0.490 | 15 | 4.3 | PASS |
| P10 | excess_ret | 1.056 | 0.970 | 15 | 8.8 | PASS |
| P10 | capm_alpha | -0.078 | -0.100 | 20 | 22.2 | FAIL |
| P10 | ff3_alpha | -0.346 | -0.490 | 20 | 29.4 | FAIL |
| P10 | ff4_alpha | 0.030 | -0.130 | 20 | 123.4 | FAIL |
| P10 | beta_exante | 1.768 | 1.700 | 10 | 4.0 | PASS |
| P10 | beta_realized | 1.870 | 1.850 | 10 | 1.1 | PASS |
| P10 | vol | 42.836 | 41.680 | 10 | 2.8 | PASS |
| P10 | sharpe | 0.296 | 0.280 | 15 | 5.6 | PASS |
| BAB | excess_ret | 0.715 | 0.700 | 15 | 2.1 | PASS |
| BAB | capm_alpha | 0.749 | 0.730 | 20 | 2.6 | PASS |
| BAB | ff3_alpha | 0.748 | 0.730 | 20 | 2.5 | PASS |
| BAB | ff4_alpha | 0.576 | 0.550 | 20 | 4.7 | PASS |
| BAB | beta_exante | 0.000 | 0.000 | 10 | 0.000 (abs) | PASS |
| BAB | beta_realized | -0.056 | -0.060 | 10 | 7.0 | PASS |
| BAB | vol | 11.443 | 10.750 | 10 | 6.4 | PASS |
| BAB | sharpe | 0.750 | 0.780 | 15 | 3.9 | PASS |

**Cells passing: 25 / 32 (v1 was 23 / 32).**

## Ablation — effect of each fix (headline cells; full per-cell in validation above)

| Config | Pass/32 | P1:ff3_alpha | P1:ff4_alpha | P1:capm_alpha | P1:beta_exante | P1:excess_ret | P5:ff3_alpha | P5:ff4_alpha | P5:capm_alpha | P5:beta_exante | P5:excess_ret | P10:ff3_alpha | P10:ff4_alpha | P10:capm_alpha | P10:beta_exante | P10:excess_ret | BAB:ff3_alpha | BAB:ff4_alpha | BAB:capm_alpha | BAB:beta_exante | BAB:excess_ret |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| v1 (all-stock, no delist) | 23/32 | 0.51 | 0.51 | 0.58 | 0.57 | 0.95 | 0.27 | 0.34 | 0.42 | 1.00 | 1.14 | -0.31 | 0.08 | -0.05 | 1.78 | 1.09 | 0.77 | 0.59 | 0.77 | 0.00 | 0.73 |
| NYSE bp only | 25/32 | 0.51 | 0.52 | 0.58 | 0.61 | 0.97 | 0.23 | 0.28 | 0.36 | 1.04 | 1.10 | -0.30 | 0.08 | -0.02 | 1.77 | 1.11 | 0.77 | 0.59 | 0.77 | 0.00 | 0.73 |
| NYSE bp + delist A | 25/32 | 0.51 | 0.51 | 0.57 | 0.61 | 0.96 | 0.23 | 0.28 | 0.36 | 1.04 | 1.10 | -0.30 | 0.07 | -0.03 | 1.77 | 1.11 | 0.76 | 0.59 | 0.76 | 0.00 | 0.73 |
| all-stock bp + delist AB | 27/32 | 0.47 | 0.47 | 0.53 | 0.57 | 0.90 | 0.26 | 0.32 | 0.40 | 1.00 | 1.13 | -0.36 | 0.03 | -0.11 | 1.78 | 1.03 | 0.75 | 0.58 | 0.75 | 0.00 | 0.71 |
| v2 (NYSE bp + delist AB) | 25/32 | 0.49 | 0.49 | 0.55 | 0.61 | 0.94 | 0.21 | 0.26 | 0.35 | 1.04 | 1.09 | -0.35 | 0.03 | -0.08 | 1.77 | 1.06 | 0.75 | 0.58 | 0.75 | 0.00 | 0.71 |

Column key: `P1:ff3_alpha` = P1 3-factor alpha (monthly %), etc. Configs isolate
the breakpoint fix (NYSE bp only) and the delisting fix (delist A = Case A only;
delist AB = Cases A+B). v2 = NYSE bp + delist AB (the headline configuration).

## Observations per portfolio (months with a return)
{'P1': 1004, 'P5': 1004, 'P10': 1004, 'BAB': 1004}

## Remaining limitations (see preparations/assumptions.md)
1. **5-factor alpha skipped** — Pastor-Stambaugh liquidity factor not in
   ClickHouse (covers 1968-2011 only).
2. **`dlret = -1.0` treated as missing** per the task spec (CRSP's Data
   Descriptions Guide flags -1.0 as the "worthless security" return = -100%;
   treating it as missing routes those cases to the Shumway imputation). 383
   performance-related delistings affected — second-order effect on decile means.
3. **Case B attributes the terminal return to the last holding month** (standard
   approximation; the true delisting month has no valid CRSP return to combine).

---
_Generated by src/table_3_v2.py — runtime 40.6s._
