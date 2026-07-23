# Table II — Asset Growth Decile Portfolio Returns and Three-Factor Alphas in Event Time

Cooper, Gulen, and Schill (2008), *Asset Growth and the Cross-Section of Stock Returns* (Journal of Finance). Caption (content.md L401): "Equal- and value-weighted portfolios are formed based on June(t) asset growth decile cutoffs. The portfolios are held for 1 year, from July of year t to June of year t+1, and then rebalanced. ... Panel C.1 reports three-factor alphas of the equal-weighted portfolios and Panel C.2 reports three-factor alphas of the value-weighted portfolios for all firms and for three size-sorted groups." The size groups use the 30th and 70th NYSE market-equity percentiles in June of year t (Assumption 4).

**Conventions.** Year-1 = the full 420-month series (every month is in the Year-1 holding period of its formation_year; annual July-t rebalance). Spread = D10 − D1 (high minus low, reported negative). EW = within-(month,decile) mean of delisting-adjusted returns; VW = Σ(ret·me_June)/Σ(me_June) using the FIXED June-t formation market equity as the weight (paper rule `sample_me_timing`; contemporaneous monthly me biases VW up ~1.3pp/mo). Three-factor alpha = intercept of (ret − rf) on (Mkt-RF, SMB, HML) ×100 (%/month); factors from `ff.four_factor_monthly` (Assumption 5). Spread alpha = intercept of the D10−D1 return (zero-investment, rf NOT subtracted) on the factors = α_D10 − α_D1. t-stats are Newey-West (HAC), n_lags=3, on the spread series (raw) / on the spread-regression intercept (alpha); the paper's extreme-decile alpha t uses a GMM/delta-method HAC joint test (footnote 12, L1574) — the NW spread t is the accepted approximation. iid (n_lags=0) t-stats are shown in parentheses.

## Panel A — Formation-Period Asset Growth (the sort variable; == Table I)

ASSETG spread (D10−D1), time-series avg of yearly cross-sectional medians: **1.3227** (t = 7.95); D1 = -0.1817, D10 = 1.1409. Paper: spread 1.0471 (t 15.60). Upper-tail vintage gap (Assumption 7) -> Tier 2, as in Table I.

## Panel B — Year-1 Average Monthly Raw Returns (%/month)

| Portfolio | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Spread(10-1) | t(NW3) | t(iid) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EW | 2.02 | 1.79 | 1.59 | 1.46 | 1.34 | 1.33 | 1.29 | 1.16 | 0.92 | 0.31 | -1.71 | -7.96 | -8.65 |
| VW | 1.47 | 1.19 | 1.27 | 1.03 | 1.01 | 1.04 | 1.01 | 0.88 | 0.78 | 0.44 | -1.03 | -4.31 | -4.42 |

Paper (Panel B Year 1): EW D1=1.99, D10=0.26, spread=−1.73, t=−8.45 (D2=1.76, D9=0.85); VW D1=1.48, D10=0.43, spread=−1.05, t=−5.04.

## Section B — Annual Year-1 Statistics (35 formation years)

- Consistency (% of 35 yrs with annual D1 > D10): **EW 97%** (paper 91), **VW 77%** (paper 71).
- Sharpe of the VW annual spread (D1−D10): **0.703** (paper 1.07). [EW spread Sharpe 1.145.]
- Annualized high-growth (D10) return: **VW 5.4%/yr** (paper 5.2), **EW 3.8%/yr** (paper 3.1) — (1+mean_monthly)^12−1.
- Annualized low-growth (D1) return: **VW 19.2%/yr** (paper ≈18), EW 27.2%/yr.
- (Mean of the 35 annual returns: VW D1 18.9 / D10 6.5; EW D1 27.1 / D10 4.3 %/yr.)

## Panel C — Year-1 Three-Factor Alphas (%/month), All Firms

| Weighting | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Spread(10-1) | t(NW3) | t(iid) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EW | 0.91 | 0.69 | 0.45 | 0.35 | 0.24 | 0.26 | 0.25 | 0.14 | -0.05 | -0.58 | -1.49 | -6.81 | -8.59 |
| VW | 0.25 | 0.08 | 0.13 | 0.06 | -0.03 | 0.12 | 0.17 | 0.13 | 0.05 | -0.31 | -0.56 | -3.14 | -2.91 |

Paper: EW D1 α=0.76 (t 3.28), D10=−0.87 (t −5.81), spread=−1.63 (t −8.33); VW D1=0.24 (1.65), D10=−0.46 (−3.74), spread=−0.70 (−3.84).

## Panel C — Three-Factor Spread Alphas by Size Group (D10−D1, %/month)

| Size | EW spread | EW t(NW3) | VW spread | VW t(NW3) |
|---|---|---|---|---|
| small | -1.62 | -6.91 | -1.33 | -6.35 |
| medium | -0.71 | -3.80 | -0.56 | -2.80 |
| large | -0.58 | -2.41 | -0.44 | -1.96 |

Paper: EW small −1.77 (−9.12), medium −0.60 (−2.85), large −0.86 (−3.12); VW small −1.14 (−6.46), medium −0.55 (−2.45), large −0.81 (−2.91).

## Section D — Carhart Four-Factor Robustness (all-firm D10−D1 spread)

| Weighting | Spread α | t(NW3) | t(iid) |
|---|---|---|---|
| EW | -1.29 | -6.21 | -7.41 |
| VW | -0.42 | -1.80 | -2.15 |

Paper: EW −1.48 (t −7.45); VW −0.60 (t −2.84).

## Section F (Panel D) — Decade-Subperiod Three-Factor Spread Alphas (D10−D1, %/month; split on formation_year)

| Subperiod | n months | EW spread | EW t(NW3) | VW spread | VW t(NW3) |
|---|---|---|---|---|---|
| 1968-1980 | 144 | -0.66 | -3.52 | -0.29 | -1.49 |
| 1981-1990 | 120 | -1.13 | -4.01 | -0.53 | -2.36 |
| 1991-2003 | 156 | -2.45 | -6.08 | -0.86 | -2.27 |

Paper: all subperiod spreads negative & significant except VW 1968–1980 = −0.35 (t −1.69).

## Section E — Event-Time Year 1..5 Buy-and-Hold

COMPUTED — see the 'Event-time (Years −/+ around formation)' section appended below (extended return window through Jun-2007, fixed buy-and-hold formation cohorts). Metric `EW_cumulative_Y1_5_spread` is now evaluated as **Tier 1** (ours -106.47% vs paper −87.99%).

## Event-time (Years −/+ around formation) — Year 1..5, fixed buy-and-hold formation cohorts

**Window.** This section uses an EXTENDED delisting-adjusted return window, **Jul-1968 .. Jun-2007** (`src/sql/universe_monthly_extended.sql` + `delisting_extended.sql`; the foundation panel ends Jun-2003). The latest formation (Jun-2002) needs Year 5 = Jul-2006..Jun-2007. The universe filter (msfhdr PIT: hshrcd 10/11, hexcd 1/2/3, hsiccd not 6000–6999) and the Assumption-1 delisting adjustment are IDENTICAL to the foundation (adjustment code imported from `main.py`); overlap spot-check 1968-07..2003-06: 1,203,865/1,203,865 (permno, month) pairs matched, max|Δret| = 0.00e+00, 0 mismatches > 1e-12. Decile MEMBERSHIP IS FIXED at each June-t formation — the cohort is held for 5 years (NOT re-sorted annually), per the Figure 2 event-time convention (content.md L1552). Event year y of cohort t = Jul(t+y−1)..Jun(t+y).

**Conventions.** Surviving-member rule: a member contributes in a month only if it has return data that month; the delisting return is embedded in the delisting month, so delisting members contribute their delisting-month return and then drop out (cohorts shrink in later event years — avg surviving members per decile-cohort: Y1 285/297, Y2 265/297, Y3 246/297, Y4 229/297, Y5 214/297). **EW** = within-month mean of member returns; **VW** = Σ(w_i·r_i)/Σ(w_i) with w_i the FIXED June-t formation ME (Assumption 9), denominator renormalized over surviving members. Portfolio returns are then averaged across the 35 cohorts at each event-month offset (Figure 2's exact method); annual = product of the year's 12 event-month means − 1; **cumulative [1,5] = product of the 60 event-month means − 1**; spread = D10 − D1. Cumulative spread t-statistics (paper: EW −8.63 / VW −4.25) are over the 35 cohort-level 60-month cumulative spreads. All values %/yr or % cumulative.

### EW returns in event time (%/yr)

| EW | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Spread(10-1) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Year 1 | 26.37 | 23.30 | 20.59 | 18.88 | 17.18 | 17.06 | 16.46 | 14.68 | 11.39 | 3.53 | -22.84 |
| Year 2 | 22.94 | 22.85 | 21.10 | 19.04 | 18.75 | 18.47 | 18.28 | 17.33 | 15.77 | 11.60 | -11.34 |
| Year 3 | 24.35 | 23.57 | 20.69 | 20.39 | 19.39 | 19.91 | 19.66 | 20.14 | 19.51 | 17.54 | -6.81 |
| Year 4 | 23.79 | 23.26 | 19.78 | 19.20 | 19.36 | 18.67 | 18.00 | 19.20 | 17.82 | 17.27 | -6.52 |
| Year 5 | 23.72 | 22.40 | 21.57 | 20.04 | 19.25 | 19.31 | 18.56 | 18.30 | 18.50 | 18.92 | -4.80 |
| **Cumulative [1,5]** | 195.86 | 182.42 | 156.63 | 143.77 | 136.47 | 135.45 | 130.60 | 127.94 | 115.16 | 89.38 | **-106.47** |

### VW returns in event time (%/yr)

| VW | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | Spread(10-1) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Year 1 | 19.01 | 15.18 | 16.33 | 13.04 | 12.73 | 13.17 | 12.70 | 10.96 | 9.67 | 5.32 | -13.69 |
| Year 2 | 16.94 | 17.54 | 16.64 | 13.30 | 13.48 | 13.07 | 12.80 | 12.12 | 12.26 | 9.03 | -7.91 |
| Year 3 | 20.56 | 17.56 | 16.40 | 15.46 | 14.61 | 13.65 | 13.99 | 14.81 | 14.90 | 13.71 | -6.85 |
| Year 4 | 17.72 | 16.33 | 14.57 | 13.49 | 14.70 | 11.70 | 14.76 | 15.61 | 12.84 | 15.05 | -2.67 |
| Year 5 | 19.24 | 15.26 | 16.36 | 15.67 | 13.29 | 13.86 | 14.26 | 13.72 | 16.63 | 15.57 | -3.67 |
| **Cumulative [1,5]** | 135.53 | 113.40 | 110.56 | 94.11 | 90.51 | 84.94 | 90.00 | 87.79 | 86.16 | 73.62 | **-61.91** |

### Cumulative Year 1..5 spread (committed metric + corroboration)

- **EW cumulative [1,5] spread (D10−D1) = -106.47%** — paper −87.99% (t = −8.63), content.md L1554 → **Tier 1** (within 50% tol (21.0%)). Cohort-level mean spread -99.42% (t = -10.14, n = 35).
- **VW cumulative [1,5] spread (D10−D1) = -61.91%** — paper −49.67% (t = −4.25), content.md L1566 (not a committed metric). Cohort-level mean spread -54.48% (t = -4.71, n = 35).
- Alternative conventions (same cohorts/weights): compounding the cohort-level annual portfolio returns (per-cohort annual compounding, then time-series mean) gives EW -112.21% / VW -57.41%.
- ⚠️ **Spec-literal per-stock annual buy-and-hold variant (FLAGGED):** averaging each member's annual buy-and-hold return across the cross-section (EW_ret_{d,y} = mean over members of prod(1+r)−1, then cumulative prod_y(1+EW_ret_{d,y})−1) gives EW -17236639.6% / VW -2356.9%. This is NOT used for the committed metric: on the 2026 CRSP vintage the cross-sectional mean of per-stock annual BHRs is dominated by a handful of sub-penny shell stocks (e.g. one +39,120% stock-year pulls a single cohort's D1 mean to +275% vs a +50% median), producing economically meaningless decile means (D1 ≈ +860%/yr). The paper's Figure 2 caption (L1552) shows it reported average MONTHLY returns in event time, so the Table II last-row cumulative spread is constructed from the monthly portfolio series above.
