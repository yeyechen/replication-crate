# §III profit-decomposition statistics (audit-1 M3)

Jegadeesh & Titman (1993), §III (L320–530). The four in-text statistics underpinning the paper's causal claim that relative-strength profits are NOT systematic risk (term 1), NOT factor timing (term 2), NOT common-factor lead-lag (term-§III.D), and ARE consistent with idiosyncratic underreaction (term 3). All computed from the existing panel + dsi EW/VW indexes (index_monthly_1964.sql, 1964-01..1989-12) + the PA 6/6 machinery. PRIMARY = RAW series (A3-revision).

## The four statistics (ours vs paper)

| # | statistic | ours | paper | dev |
|---|-----------|-----:|------:|----:|
| dec_wrss_mean | 0.021149 | 0.045 | -53.0% |
| dec_wrss_t | 1.062075 | 2.99 | -64.5% |
| dec_wrss_corr | 0.962590 | 0.95 | +1.3% |
| dec_serialcov_ew | -0.006100 | -0.0028 | -117.9% |
| dec_serialcov_resid | 0.001199 | 0.0012 | -0.0% |
| dec_theta | -1.980739 | -2.29 | +13.5% |
| dec_theta_t | -3.383367 | -1.74 | -94.4% |
| dec_theta_h1 | -2.207606 | -2.55 | +13.4% |
| dec_theta_h1_t | -2.618732 | -2.65 | +1.2% |
| dec_theta_h2 | -1.578321 | -1.83 | +13.8% |
| dec_theta_h2_t | -4.370899 | -2.52 | -73.4% |

## Construction notes (paper-silent / off-spec resolutions — see P27)

- **A1 WRSS** — 50 non-overlapping half-years (returns 1965-H1..1989-H2; formation ordinals 1964-12..1989-06 so the forward window [f+1, f+6] coincides with the 6/6 holding window and stays inside the panel — the task's '1965-01..1989-07' is off by one and its last period would need 1990-01). Weight w_i = past-6m ret_raw [f-5,f] (A13: aligned with the corrected decile signal cumret at f+1) minus the EW-index past-6m compound. PRIMARY profit = dollar-neutral weighted long-short (weighted winner return - weighted loser return) = the paper's 'profit per dollar long'; correlation vs the 6/6 single-cohort semiannual zero-cost returns y_f (apples-to-apples non-overlapping). The raw cross-sectional covariance mean(w_i*fut_i) — the task's literal formula — is +0.00044 (a covariance, ~20x below the 0.045 per-$-long anchor; corr vs calendar-time semiannual zc = +0.8574).
- **A2** — the paper's decomposition (eq. 4) is over NON-overlapping 6-month periods, so the anchor-comparable value is the semiannual serial covariance (-0.00610, 49 pairs). The overlapping-monthly estimate (299 pairs) is +0.02990: mechanically POSITIVE (consecutive overlapping 6-month windows share 5 of 6 months) and therefore NOT the quantity the paper reports as -0.0028.
- **A3** — market model per stock on overlapping 6-month returns (300 obs, >= 60; VW market primary per L526). The period-level serial covariance Cov(e_it, e_{it-1}) of consecutive NON-overlapping periods is lag 6 in the monthly-indexed residual series (lag 1 = +0.030-scale, mechanically inflated by the 5-month overlap). Cross-sectional average over 3196 stocks (VW); EW-market alternative -0.00030 over 3196 stocks.
- **A4** — y_f = cohort 6-month zero-cost cumulative return (compounded decile10 - decile1, h=1..6). x_f = squared FULL-sample-demeaned VW 6-month return over the lookback window [f-5, f] (A13: the corrected ranking window cumret at f+1 = [f-5, f]; equals the paper's 'months t-6..t-1' under t = f+1; the pre-A13 [f-6,f-1] variant gives theta -2.0307, t -3.389). OLS with Newey-West HAC t (Bartlett; full-sample L=5, h1 L=4, h2 L=4). Half-samples use the FULL-sample demeaning mean.

## Plain-language verdict on the paper's three causal claims

1. **Dispersion in expected returns / factor timing is NOT the source.** The EW-index 6-month serial covariance is -0.00610 (paper -0.0028): REPLICATED (sign) — NEGATIVE, so factor-timing (term 2, which needs a POSITIVE factor serial covariance) REDUCES rather than generates the profits. (Table II betas/mcaps, computed elsewhere, address term 1.)
2. **Idiosyncratic serial covariance is positive.** The average market-model-residual serial covariance is +0.00120 (paper +0.0012): REPLICATED (sign) — POSITIVE, consistent with stocks underreacting to firm-specific information (term 3).
3. **Lead-lag is NOT the source.** The squared-lagged-market slope is theta = -1.9807 (paper -2.29): REPLICATED (sign) — NEGATIVE, so WRSS profits are NOT positively related to squared past market returns as the lead-lag model (eq. 8) would require; this rejects lead-lag as the source and again points to firm-specific underreaction.

DEVIATIONS (documented, no tuning): A1 mean/t run below the paper (per-$-long profit and its dispersion are vintage-sensitive; the correlation anchor 0.95 IS matched at +0.963); A2 magnitude is ~2x the paper (same negative sign); A3 matches to 4 dp; A4 theta sign matches with the same negative half-sample ordering caveat (our |t| is larger because our y_f series is less autocorrelated — the same NW-SE effect documented for Table VII, P14).

**Anchor statistics (§III decomposition — not a contract table):** 4 in-text anchors from the 11 dec_* keys — WRSS per-$-long mean +0.021149 (paper +0.045), EW 6m serial covariance -0.006100 (paper -0.0028), residual serial covariance +0.001199 (paper +0.0012), θ -1.980739 (paper -2.29); all four causal verdicts replicate (sign).
