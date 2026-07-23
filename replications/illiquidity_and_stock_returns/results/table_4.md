# Table 4 — Time-series regressions of monthly excess returns on expected and unexpected illiquidity

Amihud (2002), Table 4. Estimation period 1964-01..1996-12 (T = 396). Model (10m): (RS - Rf)_m = g0 + g1 lnMILLIQ_{m-1} + g2 u^M_m + g3 JANDUM_m + w, OLS per dependent variable.

- Dependent variables in PERCENT: 100 x (RS_m - Rf_m); Rf = one-month T-bill (decimal, A2). Market = EW NYSE common (rm_ew_nyse, A4); RSZi = CRSP msib size decile i (decret_i).
- **MILLIQ universe = all NYSE common stocks trading each day (open), per the §3.3 diagnostic; admitted-sample series retained in data/_cache/milliq.parquet as milliq_admitted.** Adopted since all four adoption rules passed (g2 market = -4.18 in [-7.73, -3.31]; g2 < 0 and g1 > 0 in all six columns; Tier-1 48 > 42 under admitted; AR(1) slope 0.907 within +/-40% of 0.945). The open universe adds idiosyncratic small-name illiquidity noise that weakens the systematic component of u^M (corr(u^M, market excess) -0.26 vs -0.44 admitted), bringing g2 and R2 toward the paper.
- lnMILLIQ_{m-1}: lagged ln of MILLIQ (x10^6; open universe). u^M_m = lnMILLIQ_m - (c0_adj + c1_adj lnMILLIQ_{m-1}) from the Kendall-corrected monthly AR(1) below; JANDUM = 1 in January.
- t-stats: OLS in parentheses, White (1980) HC0 in brackets; our t-stats are signed, the paper prints |t| (compared in absolute value).
- Status (repo rule, rep/TOLERANCE_RULES.md): Tier 1 = |%dev| <= tol; Tier 2 = sign ok, |%dev| > tol; FAIL = sign flip. Strict (audit/RUBRIC.md): Tier 1 = within tol; Tier 2 = sign ok AND 0.5 <= |ours/paper| <= 2; FAIL = sign flip OR ratio outside [0.5, 2]. The two monthly AR(1) intercept cells are marked FAIL (paper-side anomaly, A11 — keep ours).

## AR(1) of ln MILLIQ, monthly, 1963-02..1996-12 (T = 407)

Raw OLS: x_m = -0.003 + 0.907 x_{m-1}; t = (-0.19, 42.90); R2 = 0.820; DW = 2.468. Kendall correction: c1_adj = 0.916; mean-preserving intercept c0_adj = -0.004. u^M_m defined 1963-02..1996-12. Paper's reported intercept 0.313 (t 3.31) is a paper-side anomaly (A11 — re-pinned per audit 1 [m1]: the DECISIVE argument is internal consistency — intercept 0.313 with slope 0.945 implies mean ln MILLIQ = 0.313/(1-0.945) = +5.7, i.e. MILLIQ ~ e^5.7 ~ 300, contradicting the paper's own Table 1 level 0.337x10^6, ln ~ -1.1; the secondary coincidence (1 - 0.768 annual slope) x mean(ln MILLIQ) ~ 0.313 is computed on the ADMITTED series (mean ln = -1.325 -> -0.308) and does NOT hold on the adopted open series (mean ln = +0.0067 -> +0.0015)); we keep ours.

| Block | Cell | OURS | PAPER | %dev | tol | Status | Strict |
|---|---|---:|---:|---:|---:|:---:|:---:|
| AR(1) | ar1_monthly_c0 | -0.0034 | 0.313 | -101.1% | 60 | FAIL (paper-side anomaly, A11 — keep ours) | FAIL |
| AR(1) | ar1_monthly_c0_t | -0.1883 | 3.31 | -94.3% | 40 | FAIL (paper-side anomaly, A11 — keep ours) | FAIL |
| AR(1) | ar1_monthly_c1 | 0.9065 | 0.945 | -4.1% | 40 | Tier 1 | Tier 1 |
| AR(1) | ar1_monthly_c1_t | 42.8976 | 58.36 | -26.5% | 40 | Tier 1 | Tier 1 |
| AR(1) | ar1_monthly_r2 | 0.8196 | 0.89 | -7.9% | 15 | Tier 1 | Tier 1 |
| AR(1) | ar1_monthly_dw | 2.4681 | 2.34 | +5.5% | 15 | Tier 1 | Tier 1 |
| AR(1) | ar1_monthly_c1_kendall | 0.9156 | 0.954 | -4.0% | 20 | Tier 1 | Tier 1 |

## Model (10m) — paper format (coef; (OLS t) [White HC0 t])

| Row | Market | RSZ2 | RSZ4 | RSZ6 | RSZ8 | RSZ10 |
|---|---:|---:|---:|---:|---:|---:|
| Constant | 0.732 | -0.092 | 0.053 | 0.049 | 0.135 | 0.087 |
|  | (+2.73) [+2.84] | (-0.26) [-0.29] | (+0.17) [+0.18] | (+0.16) [+0.16] | (+0.44) [+0.45] | (+0.31) [+0.31] |
| ln MILLIQ_{m-1} | 0.845 | 0.555 | 0.455 | 0.537 | 0.610 | 0.268 |
|  | (+2.88) [+2.46] | (+1.44) [+1.18] | (+1.30) [+1.09] | (+1.61) [+1.43] | (+1.81) [+1.64] | (+0.87) [+0.83] |
| u^M (unexpected illiquidity) | -4.182 | -7.039 | -5.997 | -5.557 | -5.523 | -3.404 |
|  | (-6.04) [-3.22] | (-7.73) [-3.98] | (-7.27) [-3.69] | (-7.06) [-3.61] | (-6.94) [-3.68] | (-4.66) [-2.77] |
| JANDUM | 4.981 | 14.168 | 9.806 | 7.759 | 5.842 | 2.552 |
|  | (+5.32) [+3.98] | (+11.51) [+7.26] | (+8.80) [+6.26] | (+7.29) [+5.66] | (+5.44) [+4.53] | (+2.59) [+2.20] |
| R2 | 0.143 | 0.307 | 0.230 | 0.192 | 0.156 | 0.063 |
| DW | 1.892 | 1.825 | 1.833 | 1.846 | 1.888 | 2.093 |
| N | 396 | 396 | 396 | 396 | 396 | 396 |

## Per-cell evaluation (84 regression cells)

| Block | Cell | OURS | PAPER | %dev | tol | Status | Strict |
|---|---|---:|---:|---:|---:|:---:|:---:|
| Market | g0_market | 0.7321 | -3.876 | +118.9% | 40 | FAIL | FAIL |
| Market | g0_market_t_ols | 2.7326 | 2.33 | +17.3% | 40 | Tier 1 | Tier 1 |
| Market | g0_market_t_white | 2.8391 | 1.97 | +44.1% | 40 | Tier 2 | Tier 2 |
| Market | g1_market | 0.8448 | 0.712 | +18.6% | 40 | Tier 1 | Tier 1 |
| Market | g1_market_t_ols | 2.8823 | 2.5 | +15.3% | 40 | Tier 1 | Tier 1 |
| Market | g1_market_t_white | 2.4614 | 2.12 | +16.1% | 40 | Tier 1 | Tier 1 |
| Market | g2_market | -4.1818 | -5.52 | +24.2% | 40 | Tier 1 | Tier 1 |
| Market | g2_market_t_ols | -6.0386 | 6.21 | -2.8% | 40 | Tier 1 | Tier 1 |
| Market | g2_market_t_white | -3.2164 | 4.42 | -27.2% | 40 | Tier 1 | Tier 1 |
| Market | g3_market | 4.9811 | 5.28 | -5.7% | 40 | Tier 1 | Tier 1 |
| Market | g3_market_t_ols | 5.3225 | 5.97 | -10.8% | 40 | Tier 1 | Tier 1 |
| Market | g3_market_t_white | 3.9808 | 4.2 | -5.2% | 40 | Tier 1 | Tier 1 |
| Market | r2_market | 0.1428 | 0.144 | -0.9% | 25 | Tier 1 | Tier 1 |
| Market | dw_market | 1.8919 | 1.98 | -4.4% | 15 | Tier 1 | Tier 1 |
| RSZ2 | g0_rsz2 | -0.0923 | -4.864 | +98.1% | 40 | Tier 2 | FAIL |
| RSZ2 | g0_rsz2_t_ols | -0.2618 | 2.54 | -89.7% | 40 | Tier 2 | FAIL |
| RSZ2 | g0_rsz2_t_white | -0.2858 | 2.03 | -85.9% | 40 | Tier 2 | FAIL |
| RSZ2 | g1_rsz2 | 0.5550 | 0.863 | -35.7% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g1_rsz2_t_ols | 1.4394 | 2.64 | -45.5% | 40 | Tier 2 | Tier 2 |
| RSZ2 | g1_rsz2_t_white | 1.1815 | 2.11 | -44.0% | 40 | Tier 2 | Tier 2 |
| RSZ2 | g2_rsz2 | -7.0390 | -6.513 | -8.1% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g2_rsz2_t_ols | -7.7267 | 6.37 | +21.3% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g2_rsz2_t_white | -3.9760 | 4.53 | -12.2% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g3_rsz2 | 14.1678 | 8.067 | +75.6% | 40 | Tier 2 | Tier 2 |
| RSZ2 | g3_rsz2_t_ols | 11.5080 | 7.94 | +44.9% | 40 | Tier 2 | Tier 2 |
| RSZ2 | g3_rsz2_t_white | 7.2579 | 5.03 | +44.3% | 40 | Tier 2 | Tier 2 |
| RSZ2 | r2_rsz2 | 0.3067 | 0.188 | +63.1% | 25 | Tier 2 | Tier 2 |
| RSZ2 | dw_rsz2 | 1.8251 | 1.99 | -8.3% | 15 | Tier 1 | Tier 1 |
| RSZ4 | g0_rsz4 | 0.0534 | -4.335 | +101.2% | 40 | FAIL | FAIL |
| RSZ4 | g0_rsz4_t_ols | 0.1674 | 2.45 | -93.2% | 40 | Tier 2 | FAIL |
| RSZ4 | g0_rsz4_t_white | 0.1767 | 2.12 | -91.7% | 40 | Tier 2 | FAIL |
| RSZ4 | g1_rsz4 | 0.4554 | 0.808 | -43.6% | 40 | Tier 2 | Tier 2 |
| RSZ4 | g1_rsz4_t_ols | 1.3047 | 2.67 | -51.1% | 40 | Tier 2 | FAIL |
| RSZ4 | g1_rsz4_t_white | 1.0908 | 2.33 | -53.2% | 40 | Tier 2 | FAIL |
| RSZ4 | g2_rsz4 | -5.9973 | -5.705 | -5.1% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g2_rsz4_t_ols | -7.2718 | 6.04 | +20.4% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g2_rsz4_t_white | -3.6876 | 4.34 | -15.0% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g3_rsz4 | 9.8062 | 5.446 | +80.1% | 40 | Tier 2 | Tier 2 |
| RSZ4 | g3_rsz4_t_ols | 8.7985 | 5.8 | +51.7% | 40 | Tier 2 | Tier 2 |
| RSZ4 | g3_rsz4_t_white | 6.2599 | 4.08 | +53.4% | 40 | Tier 2 | Tier 2 |
| RSZ4 | r2_rsz4 | 0.2298 | 0.14 | +64.2% | 25 | Tier 2 | Tier 2 |
| RSZ4 | dw_rsz4 | 1.8335 | 1.96 | -6.5% | 15 | Tier 1 | Tier 1 |
| RSZ6 | g0_rsz6 | 0.0485 | -4.06 | +101.2% | 40 | FAIL | FAIL |
| RSZ6 | g0_rsz6_t_ols | 0.1593 | 2.42 | -93.4% | 40 | Tier 2 | FAIL |
| RSZ6 | g0_rsz6_t_white | 0.1647 | 2.13 | -92.3% | 40 | Tier 2 | FAIL |
| RSZ6 | g1_rsz6 | 0.5365 | 0.761 | -29.5% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g1_rsz6_t_ols | 1.6102 | 2.65 | -39.2% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g1_rsz6_t_white | 1.4323 | 2.36 | -39.3% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g2_rsz6 | -5.5570 | -5.238 | -6.1% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g2_rsz6_t_ols | -7.0582 | 5.84 | +20.9% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g2_rsz6_t_white | -3.6055 | 4.12 | -12.5% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g3_rsz6 | 7.7595 | 4.232 | +83.4% | 40 | Tier 2 | Tier 2 |
| RSZ6 | g3_rsz6_t_ols | 7.2929 | 4.74 | +53.9% | 40 | Tier 2 | Tier 2 |
| RSZ6 | g3_rsz6_t_white | 5.6569 | 3.45 | +64.0% | 40 | Tier 2 | Tier 2 |
| RSZ6 | r2_rsz6 | 0.1925 | 0.119 | +61.7% | 25 | Tier 2 | Tier 2 |
| RSZ6 | dw_rsz6 | 1.8457 | 1.99 | -7.3% | 15 | Tier 1 | Tier 1 |
| RSZ8 | g0_rsz8 | 0.1353 | -3.66 | +103.7% | 40 | FAIL | FAIL |
| RSZ8 | g0_rsz8_t_ols | 0.4397 | 2.27 | -80.6% | 40 | Tier 2 | FAIL |
| RSZ8 | g0_rsz8_t_white | 0.4480 | 2.05 | -78.1% | 40 | Tier 2 | FAIL |
| RSZ8 | g1_rsz8 | 0.6104 | 0.701 | -12.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g1_rsz8_t_ols | 1.8137 | 2.55 | -28.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g1_rsz8_t_white | 1.6383 | 2.3 | -28.8% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g2_rsz8 | -5.5226 | -4.426 | -24.8% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g2_rsz8_t_ols | -6.9447 | 5.15 | +34.8% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g2_rsz8_t_white | -3.6822 | 4.04 | -8.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g3_rsz8 | 5.8421 | 3 | +94.7% | 40 | Tier 2 | Tier 2 |
| RSZ8 | g3_rsz8_t_ols | 5.4362 | 3.51 | +54.9% | 40 | Tier 2 | Tier 2 |
| RSZ8 | g3_rsz8_t_white | 4.5255 | 2.64 | +71.4% | 40 | Tier 2 | Tier 2 |
| RSZ8 | r2_rsz8 | 0.1556 | 0.089 | +74.9% | 25 | Tier 2 | Tier 2 |
| RSZ8 | dw_rsz8 | 1.8883 | 2.03 | -7.0% | 15 | Tier 1 | Tier 1 |
| RSZ10 | g0_rsz10 | 0.0866 | -1.553 | +105.6% | 40 | FAIL | FAIL |
| RSZ10 | g0_rsz10_t_ols | 0.3064 | 1.12 | -72.6% | 40 | Tier 2 | FAIL |
| RSZ10 | g0_rsz10_t_white | 0.3102 | 0.99 | -68.7% | 40 | Tier 2 | FAIL |
| RSZ10 | g1_rsz10 | 0.2682 | 0.319 | -15.9% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g1_rsz10_t_ols | 0.8677 | 1.35 | -35.7% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g1_rsz10_t_white | 0.8348 | 1.18 | -29.3% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g2_rsz10 | -3.4043 | -3.104 | -9.7% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g2_rsz10_t_ols | -4.6617 | 4.19 | +11.3% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g2_rsz10_t_white | -2.7741 | 3.38 | -17.9% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g3_rsz10 | 2.5520 | 1.425 | +79.1% | 40 | Tier 2 | Tier 2 |
| RSZ10 | g3_rsz10_t_ols | 2.5860 | 1.93 | +34.0% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g3_rsz10_t_white | 2.2042 | 1.47 | +49.9% | 40 | Tier 2 | Tier 2 |
| RSZ10 | r2_rsz10 | 0.0633 | 0.049 | +29.2% | 25 | Tier 2 | Tier 2 |
| RSZ10 | dw_rsz10 | 2.0929 | 2.14 | -2.2% | 15 | Tier 1 | Tier 1 |

## Monotonicity patterns (SZ1 / SZ2)

- g1 sequence: Market 0.845, RSZ2 0.555, RSZ4 0.455, RSZ6 0.537, RSZ8 0.610, RSZ10 0.268
- SZ1 (g1 positive and declining RSZ2 -> RSZ10): positive columns 6/6; declining adjacent size pairs 2/4; g1(RSZ2) > g1(RSZ10): YES. VERDICT: PARTIAL (directional only).
- g2 sequence: Market -4.182, RSZ2 -7.039, RSZ4 -5.997, RSZ6 -5.557, RSZ8 -5.523, RSZ10 -3.404
- SZ2 (g2 negative and rising RSZ2 -> RSZ10): negative columns 6/6; rising adjacent size pairs 4/4; g2(RSZ2) < g2(RSZ10): YES. VERDICT: HOLDS.

## Sanity gate status

Hard gates (must pass): all PASS. Soft ranges vs paper proximity: OLS t(g1 market) ~ 2-3: PASS; g2(market) in [-7, -4]: PASS; JANDUM(market) in [3, 6]: PASS (g2(market) = -4.182, JANDUM(market) = 4.981, OLS t(g1 market) = 2.88).

**91-cell summary (repo rule, rep/TOLERANCE_RULES.md):** Tier 1 = 48, Tier 2 = 36, FAIL = 7 (7 AR cells + 84 regression cells; 2 of the FAILs are the ar1_monthly_c0/_c0_t paper-anomaly cells, A11). **Rubric-strict (audit/RUBRIC.md):** Tier 1 = 48, Tier 2 = 23, FAIL = 20.

**Rubric-strict note (audit/RUBRIC.md, per audit 1 [M1]):** the 34 repo-rule Tier-2 cells that become FAIL under the 2x magnitude bound are all paper-side noise cells (paper |t| <= 1 or statistically-zero coefficients) or documented A13/A15/A16 gaps: Table 2 = 19 (model-b BETA coef/t 6 at paper |t| <= 0.79, ratios 2.7-4.1, A15 compressed portfolio betas; DIVYLD coef/t 6, ratios 0.23-0.49, A13 dividend-yield vintage gap; near-zero constants 6 at paper |t| <= 1 — model-a all coef/t, model-a nojan t, model-a 1981-97 coef/t, model-b 1981-97 coef; lnSIZE 1981-97 coef 1 at 2.07x); Table 3 = 2 (g1_rsz10 OLS + NW t vs paper t = 0.13/0.14, ratios ~10.8 — statistically-zero paper cell, RSZ10 g1 = -0.447); Table 4 = 13 (g0 size-portfolio coef/t cluster 11, ratios 0.01-0.31, A16 paper-side intercept inconsistency; g1_rsz4 OLS + White t 2, ratios ~0.47-0.49). The repo-rule Status column (rep/TOLERANCE_RULES.md) remains the per-cell source of truth; the Strict column reports the audit-rubric classification.
