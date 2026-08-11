# Table III replication — Fama-MacBeth monthly regressions (Panel A, full sample)

Per-month cross-sectional OLS of `ret` on the indicated controls,
then time-series average of monthly slopes. t-statistic is mean /
(std / sqrt(N)) (plain, NOT Newey-West).

Coefficients are in **percent units** (raw decimal return x 100).
Sample: July 1976 through June 1999 (276 months expected).

| Model | Variable | Coef (%/unit) | t-stat |
|---|---|---:|---:|
| 1: ret ~ beta | beta | 0.43 | 1.37 |
| 2: ret ~ ln_size | ln_size | -0.14 | -2.73 |
| 3: ret ~ ln_bm | ln_bm | 0.49 | 6.38 |
| 4: ret ~ ln_size + ln_bm | ln_size | -0.11 | -2.12 |
|  | ln_bm | 0.39 | 4.87 |
| 5: ret ~ ln_inv | ln_inv | -0.26 | -6.99 |
| 6: ret ~ ln_size + ln_bm + ln_inv | ln_size | -0.11 | -2.03 |
|  | ln_bm | 0.35 | 4.43 |
|  | ln_inv | -0.19 | -5.82 |
| 7: ret ~ beta + ln_size + ln_bm + ln_inv | beta | 0.58 | 1.86 |
|  | ln_size | -0.10 | -1.91 |
|  | ln_bm | 0.40 | 6.20 |
|  | ln_inv | -0.22 | -6.48 |

**Notes:**

- Model 1 reports the β coefficient (the JSON spec's `alpha_model1_beta_only` is a misnomer; the paper's row 1 column shows the β coefficient value).
- Subperiod results (1976-1987, 1987-1999) and Feb-Dec exclusion now in `results/table_3_subperiods.md`.
- `ln_size` here is `ln_me = log(abs(prc) * shrout * 1000)`,
  per the paper's `Ln(size)` convention.
- Months in sample: 276
- Stock-month observations after require-non-null filters: 965,980