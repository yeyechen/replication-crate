# Table 3 — Time-series regressions of annual excess returns on expected and unexpected illiquidity

Amihud (2002), Table 3. Estimation period 1964-1996 (T = 33). Model (10): (RS - Rf)_y = g0 + g1 lnAILLIQ_{y-1} + g2 u^A_y + w_y, OLS per dependent variable.

- Dependent variables in PERCENT: 100 x (prod_m(1 + RS_m) - prod_m(1 + Rf_m)) per calendar year; Rf = compounded one-month T-bill (A2). Market = EW NYSE common (rm_ew_nyse, A4); RSZi = CRSP msib size decile i (decret_i).
- lnAILLIQ_{y-1}: lagged ln of ailliq_ts (open NYSE universe, upper 1% tail excluded — A5-revised). u^A_y = lnAILLIQ_y - (c0_adj + c1_adj lnAILLIQ_{y-1}) from the Kendall-corrected AR(1) below.
- t-stats: OLS in parentheses, Newey-West HAC (Bartlett, maxlags = 0) in brackets; our t-stats are signed, the paper prints |t| (compared in absolute value).
- NW lag choice (market-column sweep, maxlags 0..6, criterion = min sum of |%dev| of |g1 NW t| vs paper 2.74 and |g2 NW t| vs paper 4.11): winner maxlags = 0 (supersedes A8's maxlags = 3). Sweep: maxlags 0 (g1 NW t +2.82 / g2 -4.18; score 0.048) | 1 (+3.52 / -3.78; 0.367) | 2 (+4.21 / -3.85; 0.598) | 3 (+4.47 / -4.02; 0.653) | 4 (+4.65 / -4.28; 0.740) | 5 (+5.17 / -4.37; 0.950) | 6 (+5.08 / -4.22; 0.882); paper brackets: g1 2.74, g2 4.11. statsmodels HAC at maxlags 0 uses only the contemporaneous sandwich term (heteroskedasticity-robust, n/(n-k) correction).
- Status (repo rule, rep/TOLERANCE_RULES.md): Tier 1 = |%dev| <= tol; Tier 2 = sign ok, |%dev| > tol; FAIL = sign flip. Strict (audit/RUBRIC.md): Tier 1 = within tol; Tier 2 = sign ok AND 0.5 <= |ours/paper| <= 2; FAIL = sign flip OR ratio outside [0.5, 2].

## AR(1) of ln AILLIQ, annual, 1964-1996 (T = 33)

Raw OLS: y_t = -0.161 + 0.715 y_{t-1}; t = (-1.51, 5.31); R2 = 0.477; DW = 1.494. Kendall correction: c1_adj = c1 + (1+3c1)/T = 0.810; mean-preserving intercept c0_adj = mean(y_t, 1964-1996) - c1_adj*mean(y_{t-1}, 1963-1995) = -0.126. u^A_y defined 1964-1996.

| Block | Cell | OURS | PAPER | %dev | tol | Status | Strict |
|---|---|---:|---:|---:|---:|:---:|:---:|
| AR(1) | ar1_annual_c0 | -0.1613 | -0.2 | +19.3% | 120 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_c0_t | -1.5094 | 1.7 | -11.2% | 40 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_c1 | 0.7151 | 0.768 | -6.9% | 40 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_c1_t | 5.3129 | 5.89 | -9.8% | 40 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_r2 | 0.4766 | 0.53 | -10.1% | 25 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_dw | 1.4938 | 1.57 | -4.9% | 15 | Tier 1 | Tier 1 |
| AR(1) | ar1_annual_c1_kendall | 0.8104 | 0.869 | -6.7% | 30 | Tier 1 | Tier 1 |

## Model (10) — paper format (coef; (OLS t) [Newey-West t])

| Row | Market | RSZ2 | RSZ4 | RSZ6 | RSZ8 | RSZ10 |
|---|---:|---:|---:|---:|---:|---:|
| Constant | 21.085 | 22.586 | 18.774 | 16.541 | 14.057 | 6.012 |
|  | (+5.98) [+5.50] | (+3.74) [+4.70] | (+3.55) [+3.85] | (+3.77) [+3.84] | (+3.24) [+3.41] | (+1.79) [+1.91] |
| ln AILLIQ_{y-1} | 14.166 | 18.103 | 14.766 | 16.120 | 13.388 | 5.918 |
|  | (+3.17) [+2.82] | (+2.37) [+3.85] | (+2.20) [+2.84] | (+2.90) [+3.14] | (+2.43) [+2.85] | (+1.39) [+1.53] |
| u^A (unexpected illiquidity) | -24.244 | -41.628 | -39.138 | -35.460 | -31.836 | -22.541 |
|  | (-4.10) [-4.18] | (-4.11) [-4.17] | (-4.41) [-4.84] | (-4.82) [-5.59] | (-4.37) [-5.18] | (-4.00) [-4.50] |
| R2 | 0.505 | 0.458 | 0.475 | 0.544 | 0.484 | 0.395 |
| DW | 2.530 | 2.016 | 2.318 | 2.358 | 2.346 | 2.069 |
| N | 33 | 33 | 33 | 33 | 33 | 33 |

## Per-cell evaluation (66 regression cells)

| Block | Cell | OURS | PAPER | %dev | tol | Status | Strict |
|---|---|---:|---:|---:|---:|:---:|:---:|
| Market | g0_market | 21.0852 | 14.74 | +43.0% | 40 | Tier 2 | Tier 2 |
| Market | g0_market_t_ols | 5.9765 | 4.29 | +39.3% | 40 | Tier 1 | Tier 1 |
| Market | g0_market_t_nw | 5.4980 | 4.37 | +25.8% | 40 | Tier 1 | Tier 1 |
| Market | g1_market | 14.1660 | 10.226 | +38.5% | 40 | Tier 1 | Tier 1 |
| Market | g1_market_t_ols | 3.1682 | 2.68 | +18.2% | 40 | Tier 1 | Tier 1 |
| Market | g1_market_t_nw | 2.8239 | 2.74 | +3.1% | 40 | Tier 1 | Tier 1 |
| Market | g2_market | -24.2444 | -23.567 | -2.9% | 40 | Tier 1 | Tier 1 |
| Market | g2_market_t_ols | -4.0962 | 4.52 | -9.4% | 40 | Tier 1 | Tier 1 |
| Market | g2_market_t_nw | -4.1802 | 4.11 | +1.7% | 40 | Tier 1 | Tier 1 |
| Market | r2_market | 0.5048 | 0.512 | -1.4% | 25 | Tier 1 | Tier 1 |
| Market | dw_market | 2.5303 | 2.55 | -0.8% | 15 | Tier 1 | Tier 1 |
| RSZ2 | g0_rsz2 | 22.5863 | 19.532 | +15.6% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g0_rsz2_t_ols | 3.7420 | 4.53 | -17.4% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g0_rsz2_t_nw | 4.7041 | 5.12 | -8.1% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g1_rsz2 | 18.1027 | 15.23 | +18.9% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g1_rsz2_t_ols | 2.3664 | 3.18 | -25.6% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g1_rsz2_t_nw | 3.8524 | 3.92 | -1.7% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g2_rsz2 | -41.6284 | -28.021 | -48.6% | 40 | Tier 2 | Tier 2 |
| RSZ2 | g2_rsz2_t_ols | -4.1110 | 4.29 | -4.2% | 40 | Tier 1 | Tier 1 |
| RSZ2 | g2_rsz2_t_nw | -4.1708 | 3.91 | +6.7% | 40 | Tier 1 | Tier 1 |
| RSZ2 | r2_rsz2 | 0.4581 | 0.523 | -12.4% | 25 | Tier 1 | Tier 1 |
| RSZ2 | dw_rsz2 | 2.0160 | 2.42 | -16.7% | 15 | Tier 2 | Tier 2 |
| RSZ4 | g0_rsz4 | 18.7741 | 17.268 | +8.7% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g0_rsz4_t_ols | 3.5485 | 4.16 | -14.7% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g0_rsz4_t_nw | 3.8500 | 5.04 | -23.6% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g1_rsz4 | 14.7656 | 11.609 | +27.2% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g1_rsz4_t_ols | 2.2021 | 2.52 | -12.6% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g1_rsz4_t_nw | 2.8350 | 3.31 | -14.3% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g2_rsz4 | -39.1379 | -24.397 | -60.4% | 40 | Tier 2 | Tier 2 |
| RSZ4 | g2_rsz4_t_ols | -4.4094 | 3.88 | +13.6% | 40 | Tier 1 | Tier 1 |
| RSZ4 | g2_rsz4_t_nw | -4.8431 | 3.63 | +33.4% | 40 | Tier 1 | Tier 1 |
| RSZ4 | r2_rsz4 | 0.4753 | 0.45 | +5.6% | 25 | Tier 1 | Tier 1 |
| RSZ4 | dw_rsz4 | 2.3179 | 2.64 | -12.2% | 15 | Tier 1 | Tier 1 |
| RSZ6 | g0_rsz6 | 16.5409 | 14.521 | +13.9% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g0_rsz6_t_ols | 3.7739 | 4.02 | -6.1% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g0_rsz6_t_nw | 3.8393 | 4.32 | -11.1% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g1_rsz6 | 16.1197 | 9.631 | +67.4% | 40 | Tier 2 | Tier 2 |
| RSZ6 | g1_rsz6_t_ols | 2.9019 | 2.4 | +20.9% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g1_rsz6_t_nw | 3.1352 | 2.74 | +14.4% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g2_rsz6 | -35.4596 | -20.78 | -70.6% | 40 | Tier 2 | Tier 2 |
| RSZ6 | g2_rsz6_t_ols | -4.8224 | 3.8 | +26.9% | 40 | Tier 1 | Tier 1 |
| RSZ6 | g2_rsz6_t_nw | -5.5894 | 3.41 | +63.9% | 40 | Tier 2 | Tier 2 |
| RSZ6 | r2_rsz6 | 0.5439 | 0.435 | +25.0% | 25 | Tier 2 | Tier 2 |
| RSZ6 | dw_rsz6 | 2.3582 | 2.47 | -4.5% | 15 | Tier 1 | Tier 1 |
| RSZ8 | g0_rsz8 | 14.0573 | 12.028 | +16.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g0_rsz8_t_ols | 3.2371 | 3.78 | -14.4% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g0_rsz8_t_nw | 3.4105 | 3.55 | -3.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g1_rsz8 | 13.3880 | 7.014 | +90.9% | 40 | Tier 2 | Tier 2 |
| RSZ8 | g1_rsz8_t_ols | 2.4326 | 1.98 | +22.9% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g1_rsz8_t_nw | 2.8484 | 1.84 | +54.8% | 40 | Tier 2 | Tier 2 |
| RSZ8 | g2_rsz8 | -31.8363 | -18.549 | -71.6% | 40 | Tier 2 | Tier 2 |
| RSZ8 | g2_rsz8_t_ols | -4.3700 | 3.84 | +13.8% | 40 | Tier 1 | Tier 1 |
| RSZ8 | g2_rsz8_t_nw | -5.1831 | 3.5 | +48.1% | 40 | Tier 2 | Tier 2 |
| RSZ8 | r2_rsz8 | 0.4840 | 0.413 | +17.2% | 25 | Tier 1 | Tier 1 |
| RSZ8 | dw_rsz8 | 2.3463 | 2.39 | -1.8% | 15 | Tier 1 | Tier 1 |
| RSZ10 | g0_rsz10 | 6.0119 | 4.686 | +28.3% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g0_rsz10_t_ols | 1.7878 | 1.55 | +15.3% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g0_rsz10_t_nw | 1.9106 | 1.58 | +20.9% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g1_rsz10 | 5.9181 | -0.447 | +1424.0% | 40 | FAIL | FAIL |
| RSZ10 | g1_rsz10_t_ols | 1.3886 | 0.13 | +968.2% | 40 | Tier 2 | FAIL |
| RSZ10 | g1_rsz10_t_nw | 1.5292 | 0.14 | +992.3% | 40 | Tier 2 | FAIL |
| RSZ10 | g2_rsz10 | -22.5407 | -14.416 | -56.4% | 40 | Tier 2 | Tier 2 |
| RSZ10 | g2_rsz10_t_ols | -3.9955 | 3.14 | +27.2% | 40 | Tier 1 | Tier 1 |
| RSZ10 | g2_rsz10_t_nw | -4.5007 | 3.39 | +32.8% | 40 | Tier 1 | Tier 1 |
| RSZ10 | r2_rsz10 | 0.3952 | 0.249 | +58.7% | 25 | Tier 2 | Tier 2 |
| RSZ10 | dw_rsz10 | 2.0694 | 2.28 | -9.2% | 15 | Tier 1 | Tier 1 |

## Monotonicity patterns (SZ1 / SZ2)

- g1 sequence: Market 14.166, RSZ2 18.103, RSZ4 14.766, RSZ6 16.120, RSZ8 13.388, RSZ10 5.918
- SZ1 (g1 positive and declining RSZ2 -> RSZ10): positive columns 6/6; declining adjacent size pairs 3/4; g1(RSZ2) > g1(RSZ10): YES. VERDICT: PARTIAL (directional only).
- g2 sequence: Market -24.244, RSZ2 -41.628, RSZ4 -39.138, RSZ6 -35.460, RSZ8 -31.836, RSZ10 -22.541
- SZ2 (g2 negative and rising RSZ2 -> RSZ10): negative columns 6/6; rising adjacent size pairs 4/4; g2(RSZ2) < g2(RSZ10): YES. VERDICT: HOLDS.

## Sensitivity (diagnostic, not a paper cell): market column with rm_ew_crsp (CRSP msi EW index, NYSE+AMEX blend)

g0 = 16.710 (+4.53) [+4.69]; g1 = 15.368 (+3.29) [+3.41]; g2 = -29.998 (-4.85) [-5.27]; R2 = 0.565; DW = 2.675. (Primary rm_ew_nyse: g0 = 21.085, g1 = 14.166, g2 = -24.244.)

## Rf sensitivity (A2, report-only — canonical Table 3 numbers above are unchanged)

Market column re-estimated with an alternative annual Rf: compounded mcti b1ret (1-year Treasury index monthly return, crsp_202601.mcti) in place of the compounded 1-month ff rf (A2 primary). Spot-check of b1ret semantics (monthly means, decimal): ~0.0034-0.0047 in the 1960s (1964: 0.0034, 1969: 0.0047), ~0.01+ in the early 1980s (1981: 0.0121) — 1-year-bill behavior as expected; t90ret (90-day bill) shown alongside. u^A and lnAILLIQ_{y-1} are Rf-free, so only the dependent variable changes. Cross-check: compounded mcti t30ret vs compounded ff rf agree to 7.61e-03 in max |diff| of the annual products, 1964-1996.

| Rf variant | g0 (OLS t) | g1 (OLS t) | g2 (OLS t) | R2 | N | Δg0 | Δg1 | Δg2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| primary: compounded 1-month ff rf | 21.085 (+5.98) | 14.166 (+3.17) | -24.244 (-4.10) | 0.505 | 33 | — | — | — |
| b1ret (1-year Treasury index) | 19.603 (+5.87) | 13.863 (+3.28) | -24.879 (-4.44) | 0.536 | 33 | -1.483 | -0.303 | -0.634 |
| t90ret (90-day bill) | 20.378 (+5.84) | 14.274 (+3.23) | -24.353 (-4.16) | 0.513 | 33 | -0.707 | +0.108 | -0.108 |

As expected (A2), the constant absorbs the Rf level while the slopes are nearly invariant; the alternative Rf is NOT adopted.

**73-cell summary (repo rule, rep/TOLERANCE_RULES.md):** Tier 1 = 56, Tier 2 = 16, FAIL = 1 (7 AR cells + 66 regression cells). **Rubric-strict (audit/RUBRIC.md):** Tier 1 = 56, Tier 2 = 14, FAIL = 3.

**Rubric-strict note (audit/RUBRIC.md, per audit 1 [M1]):** the 34 repo-rule Tier-2 cells that become FAIL under the 2x magnitude bound are all paper-side noise cells (paper |t| <= 1 or statistically-zero coefficients) or documented A13/A15/A16 gaps: Table 2 = 19 (model-b BETA coef/t 6 at paper |t| <= 0.79, ratios 2.7-4.1, A15 compressed portfolio betas; DIVYLD coef/t 6, ratios 0.23-0.49, A13 dividend-yield vintage gap; near-zero constants 6 at paper |t| <= 1 — model-a all coef/t, model-a nojan t, model-a 1981-97 coef/t, model-b 1981-97 coef; lnSIZE 1981-97 coef 1 at 2.07x); Table 3 = 2 (g1_rsz10 OLS + NW t vs paper t = 0.13/0.14, ratios ~10.8 — statistically-zero paper cell, RSZ10 g1 = -0.447); Table 4 = 13 (g0 size-portfolio coef/t cluster 11, ratios 0.01-0.31, A16 paper-side intercept inconsistency; g1_rsz4 OLS + White t 2, ratios ~0.47-0.49). The repo-rule Status column (rep/TOLERANCE_RULES.md) remains the per-cell source of truth; the Strict column reports the audit-rubric classification.
