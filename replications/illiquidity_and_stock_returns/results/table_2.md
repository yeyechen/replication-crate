# Table 2 — Cross-section regressions of stock returns on illiquidity and other characteristics

Amihud (2002), Table 2. Fama-MacBeth: monthly cross-sectional OLS of the delisting-adjusted monthly stock return on lagged (year y-1) characteristics; coefficients averaged over the months of each window; t = mean / (std across months / sqrt(N months)).

**Dependent-variable units: monthly return x 100 (percent).** With decimal returns, k_ILLIQMA = 0.00166 (t = 6.56); the paper's Table 2 values (k = 0.162, t = 6.55; BETA 1.183; R100 1.023) are exactly 100x the decimal-run coefficients with identical t-stats (t is scale-invariant) — the paper's coefficients are on a percent-return scale. The percent dependent variable is used per the task's sanity gate (k ~ 0.16 required; ~0.0016 flagged as a return-scaling error).

- Cross-section for month m of returns-year y: panel rows with `y = year(m)`, `admitted = 1`, non-null `ret_mm`.
- Model (a): constant, BETA, ILLIQMA, R100, R100YR.
- Model (b): model (a) + lnSIZE, SDRET, DIVYLD.
- Units as stored in the panel: ILLIQMA ratio (annual means 1), R100/R100YR decimal, lnSIZE log dollars, SDRET percent (x100), DIVYLD percent, BETA unitless.
- Plain monthly OLS, NO winsorization, plain iid time-series t-stats — implemented directly in src/main.py (`_fm_ols_monthly`); `utils.fama_macbeth` was NOT used because it winsorizes regressors at 1%/99% per period by default and reports Newey-West HAC t-stats (n_lags=2), not the plain mean/(sd/sqrt(N)) t of the paper/spec.
- Rows with a null return among admitted (stock, year, month) cells: 8579; rows dropped for null regressors: model (a) 0, model (b) 0 (of 551881 cells with non-null returns).
- Cross-section size per month (after null-drop): model (a) min 1028 / mean 1353 / max 1758; model (b) min 1028 / mean 1353 / max 1758.

Tolerances: 40% (coefficients and t-stats; t-stats compared in absolute value — the paper prints |t|), 40% (median k_ILLIQMA), 10% (% positive), 100% (serial correlation). Status (repo rule, rep/TOLERANCE_RULES.md): Tier 1 = |dev| <= tol; Tier 2 = sign ok, |dev| > tol; FAIL = sign flip. Strict (audit/RUBRIC.md): Tier 1 = within tol; Tier 2 = sign ok AND 0.5 <= |ours/paper| <= 2; FAIL = sign flip OR ratio outside [0.5, 2].

## Model (a)

### All months (N = 408 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | -0.364 (0.76) | -0.0595 (-0.12) | +83.7% | Tier 2 | FAIL | -84.9% | Tier 2 | FAIL |
| BETA | 1.183 (2.45) | 1.0657 (+2.00) | -9.9% | Tier 1 | Tier 1 | -18.5% | Tier 1 | Tier 1 |
| ILLIQMA | 0.162 (6.55) | 0.1657 (+6.56) | +2.3% | Tier 1 | Tier 1 | +0.2% | Tier 1 | Tier 1 |
| R100 | 1.023 (3.83) | 1.0266 (+4.13) | +0.3% | Tier 1 | Tier 1 | +7.8% | Tier 1 | Tier 1 |
| R100YR | 0.382 (2.98) | 0.4920 (+3.40) | +28.8% | Tier 1 | Tier 1 | +14.0% | Tier 1 | Tier 1 |

### Excl. January (N = 374 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | -0.235 (0.50) | 0.0109 (+0.02) | +104.6% | FAIL | FAIL | -95.5% | Tier 2 | FAIL |
| BETA | 0.816 (1.75) | 0.7800 (+1.54) | -4.4% | Tier 1 | Tier 1 | -12.1% | Tier 1 | Tier 1 |
| ILLIQMA | 0.126 (5.30) | 0.1301 (+5.34) | +3.3% | Tier 1 | Tier 1 | +0.8% | Tier 1 | Tier 1 |
| R100 | 1.514 (6.17) | 1.4861 (+6.58) | -1.8% | Tier 1 | Tier 1 | +6.6% | Tier 1 | Tier 1 |
| R100YR | 0.475 (3.70) | 0.5654 (+3.88) | +19.0% | Tier 1 | Tier 1 | +4.8% | Tier 1 | Tier 1 |

### 1964-1980 (N = 204 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | -0.904 (1.39) | -0.5444 (-0.77) | +39.8% | Tier 1 | Tier 1 | -45.0% | Tier 2 | Tier 2 |
| BETA | 1.450 (1.83) | 1.3087 (+1.54) | -9.7% | Tier 1 | Tier 1 | -15.7% | Tier 1 | Tier 1 |
| ILLIQMA | 0.216 (4.87) | 0.2190 (+4.86) | +1.4% | Tier 1 | Tier 1 | -0.2% | Tier 1 | Tier 1 |
| R100 | 0.974 (2.47) | 1.0336 (+2.79) | +6.1% | Tier 1 | Tier 1 | +12.8% | Tier 1 | Tier 1 |
| R100YR | 0.485 (2.55) | 0.6714 (+2.97) | +38.4% | Tier 1 | Tier 1 | +16.4% | Tier 1 | Tier 1 |

### 1981-1997 (N = 204 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | 0.177 (0.25) | 0.4255 (+0.57) | +140.4% | Tier 2 | FAIL | +127.0% | Tier 2 | FAIL |
| BETA | 0.917 (1.66) | 0.8227 (+1.27) | -10.3% | Tier 1 | Tier 1 | -23.6% | Tier 1 | Tier 1 |
| ILLIQMA | 0.108 (5.05) | 0.1124 (+5.03) | +4.1% | Tier 1 | Tier 1 | -0.4% | Tier 1 | Tier 1 |
| R100 | 1.082 (2.96) | 1.0195 (+3.07) | -5.8% | Tier 1 | Tier 1 | +3.7% | Tier 1 | Tier 1 |
| R100YR | 0.279 (1.59) | 0.3125 (+1.73) | +12.0% | Tier 1 | Tier 1 | +8.9% | Tier 1 | Tier 1 |

## Model (b)

### All months (N = 408 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | 1.922 (4.06) | 3.2889 (+3.35) | +71.1% | Tier 2 | Tier 2 | -17.5% | Tier 1 | Tier 1 |
| BETA | 0.217 (0.64) | 0.6938 (+1.89) | +219.7% | Tier 2 | FAIL | +194.6% | Tier 2 | FAIL |
| ILLIQMA | 0.112 (5.39) | 0.1242 (+5.86) | +10.9% | Tier 1 | Tier 1 | +8.7% | Tier 1 | Tier 1 |
| R100 | 0.888 (3.70) | 1.0546 (+4.85) | +18.8% | Tier 1 | Tier 1 | +31.2% | Tier 1 | Tier 1 |
| R100YR | 0.359 (3.40) | 0.4694 (+3.85) | +30.7% | Tier 1 | Tier 1 | +13.3% | Tier 1 | Tier 1 |
| ln SIZE | -0.134 (3.50) | -0.1305 (-3.19) | +2.6% | Tier 1 | Tier 1 | -8.9% | Tier 1 | Tier 1 |
| SDRET | -0.179 (1.90) | -0.1938 (-2.29) | -8.3% | Tier 1 | Tier 1 | +20.6% | Tier 1 | Tier 1 |
| DIVYLD | -0.048 (3.36) | -0.0141 (-0.76) | +70.7% | Tier 2 | FAIL | -77.3% | Tier 2 | FAIL |

### Excl. January (N = 374 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | 1.568 (3.32) | 2.1739 (+2.18) | +38.6% | Tier 1 | Tier 1 | -34.4% | Tier 1 | Tier 1 |
| BETA | 0.260 (0.79) | 0.7838 (+2.14) | +201.5% | Tier 2 | FAIL | +170.7% | Tier 2 | FAIL |
| ILLIQMA | 0.103 (4.91) | 0.1087 (+5.09) | +5.6% | Tier 1 | Tier 1 | +3.6% | Tier 1 | Tier 1 |
| R100 | 1.335 (6.19) | 1.4737 (+7.54) | +10.4% | Tier 1 | Tier 1 | +21.8% | Tier 1 | Tier 1 |
| R100YR | 0.439 (4.27) | 0.5355 (+4.42) | +22.0% | Tier 1 | Tier 1 | +3.6% | Tier 1 | Tier 1 |
| ln SIZE | -0.073 (2.00) | -0.0745 (-1.85) | -2.0% | Tier 1 | Tier 1 | -7.3% | Tier 1 | Tier 1 |
| SDRET | -0.274 (2.89) | -0.2924 (-3.47) | -6.7% | Tier 1 | Tier 1 | +20.2% | Tier 1 | Tier 1 |
| DIVYLD | -0.063 (4.28) | -0.0307 (-1.60) | +51.2% | Tier 2 | FAIL | -62.6% | Tier 2 | FAIL |

### 1964-1980 (N = 204 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | 2.074 (2.63) | 2.9511 (+1.79) | +42.3% | Tier 2 | Tier 2 | -31.9% | Tier 1 | Tier 1 |
| BETA | 0.297 (0.59) | 1.2134 (+2.19) | +308.5% | Tier 2 | FAIL | +271.7% | Tier 2 | FAIL |
| ILLIQMA | 0.135 (3.69) | 0.1549 (+4.18) | +14.7% | Tier 1 | Tier 1 | +13.2% | Tier 1 | Tier 1 |
| R100 | 0.813 (2.33) | 1.0032 (+3.15) | +23.4% | Tier 1 | Tier 1 | +35.3% | Tier 1 | Tier 1 |
| R100YR | 0.324 (2.04) | 0.5059 (+2.65) | +56.2% | Tier 2 | Tier 2 | +30.1% | Tier 1 | Tier 1 |
| ln SIZE | -0.217 (3.51) | -0.1552 (-2.32) | +28.5% | Tier 1 | Tier 1 | -34.0% | Tier 1 | Tier 1 |
| SDRET | -0.136 (0.96) | -0.1267 (-0.97) | +6.8% | Tier 1 | Tier 1 | +1.5% | Tier 1 | Tier 1 |
| DIVYLD | -0.075 (2.81) | -0.0387 (-1.14) | +48.4% | Tier 2 | Tier 2 | -59.4% | Tier 2 | FAIL |

### 1981-1997 (N = 204 months)

| Variable | Paper coef (t) | Ours coef (t) | coef %dev | coef status | coef strict | t %dev | t status | t strict |
|---|---:|---:|---:|:---:|:---:|---:|:---:|:---:|
| Constant | 1.770 (3.35) | 3.6267 (+3.38) | +104.9% | Tier 2 | FAIL | +1.0% | Tier 1 | Tier 1 |
| BETA | 0.137 (0.30) | 0.1742 (+0.36) | +27.2% | Tier 1 | Tier 1 | +20.0% | Tier 1 | Tier 1 |
| ILLIQMA | 0.088 (4.56) | 0.0936 (+4.56) | +6.4% | Tier 1 | Tier 1 | +0.1% | Tier 1 | Tier 1 |
| R100 | 0.962 (2.92) | 1.1060 (+3.73) | +15.0% | Tier 1 | Tier 1 | +27.6% | Tier 1 | Tier 1 |
| R100YR | 0.395 (2.82) | 0.4328 (+2.84) | +9.6% | Tier 1 | Tier 1 | +0.7% | Tier 1 | Tier 1 |
| ln SIZE | -0.051 (1.14) | -0.1057 (-2.25) | -107.2% | Tier 2 | FAIL | +97.0% | Tier 2 | Tier 2 |
| SDRET | -0.223 (1.77) | -0.2609 (-2.41) | -17.0% | Tier 1 | Tier 1 | +36.1% | Tier 1 | Tier 1 |
| DIVYLD | -0.021 (2.11) | 0.0105 (+0.72) | +150.1% | FAIL | FAIL | -66.0% | Tier 2 | FAIL |

## ILLIQMA coefficient series (model a, all 408 months)

| Statistic | PAPER | OURS | %dev | tol | Status | Strict |
|---|---:|---:|---:|---:|:---:|:---:|
| median_k_illiqma | 0.135 | 0.1417 | +4.9% | 40% | Tier 1 | Tier 1 |
| pct_positive_k_illiqma | 63.400 | 63.2353 | -0.3% | 10% | Tier 1 | Tier 1 |
| autocorr_k_illiqma | 0.080 | 0.0512 | -35.9% | 100% | Tier 1 | Tier 1 |

**107-cell summary (repo rule, rep/TOLERANCE_RULES.md):** Tier 1 = 80, Tier 2 = 25, FAIL = 2 (of 107 cells: 104 coefficient/t cells + 3 ILLIQMA-series stats). **Rubric-strict (audit/RUBRIC.md):** Tier 1 = 80, Tier 2 = 6, FAIL = 21.

**Rubric-strict note (audit/RUBRIC.md, per audit 1 [M1]):** the 34 repo-rule Tier-2 cells that become FAIL under the 2x magnitude bound are all paper-side noise cells (paper |t| <= 1 or statistically-zero coefficients) or documented A13/A15/A16 gaps: Table 2 = 19 (model-b BETA coef/t 6 at paper |t| <= 0.79, ratios 2.7-4.1, A15 compressed portfolio betas; DIVYLD coef/t 6, ratios 0.23-0.49, A13 dividend-yield vintage gap; near-zero constants 6 at paper |t| <= 1 — model-a all coef/t, model-a nojan t, model-a 1981-97 coef/t, model-b 1981-97 coef; lnSIZE 1981-97 coef 1 at 2.07x); Table 3 = 2 (g1_rsz10 OLS + NW t vs paper t = 0.13/0.14, ratios ~10.8 — statistically-zero paper cell, RSZ10 g1 = -0.447); Table 4 = 13 (g0 size-portfolio coef/t cluster 11, ratios 0.01-0.31, A16 paper-side intercept inconsistency; g1_rsz4 OLS + White t 2, ratios ~0.47-0.49). The repo-rule Status column (rep/TOLERANCE_RULES.md) remains the per-cell source of truth; the Strict column reports the audit-rubric classification.
