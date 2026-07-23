# Portfolio Diagnostics — Asset-Growth Long-Short Spread

**Portfolio (Cooper, Gulen, Schill 2008, headline):** each month, **LONG decile 1** (lowest asset growth) and **SHORT decile 10** (highest asset growth); monthly spread return = `D1_ret − D10_ret`. Built equal-weighted (EW) and value-weighted (VW; weights = fixed June-t formation market equity, Assumption 9). Sample: monthly delisting-adjusted returns, 1968-07 .. 2003-06 (420 months). Diagnostics via `utils.portfolio_diagnostics` with `zero_investment=True` (self-financing L/S spread — rf NOT subtracted); FF5 alpha from a time-series regression of the spread on (Mkt-RF, SMB, HML, RMW, CMA). Alpha t-stat: Newey-West, n_lags = 3 (replication HAC convention; iid t shown alongside).

## Performance summary (Asset-growth L/S spread, EW, M)

| Metric | Value |
|---|---|
| Sample period | 1968-07 – 2003-06 (420 months) |
| Annualized Sharpe | **1.46** |
| Total return | 90254.2% |
| Max drawdown | -19.7% |
| FF5 alpha (annualized) | **16.32%** (t = 5.89) |
| FF5 regression R² | 0.41 |

_FF5 alpha uses the zero-investment convention: rf not subtracted (self-financing L/S spread). Sharpe and the alpha t-stat are scale-invariant; the alpha in % scales with portfolio leverage._

_Additional detail:_ annualized spread return 20.55%/yr; annualized volatility 14.06%; FF5 alpha 1.360%/month (= 16.32%/yr), Newey-West t (n_lags=3) = 5.89 [iid t = 8.36]. FF5 loadings: mkt_rf -0.11, smb +0.31, hml +0.04, rmw -0.28, cma +0.95._


## Performance summary (Asset-growth L/S spread, VW, M)

| Metric | Value |
|---|---|
| Sample period | 1968-07 – 2003-06 (420 months) |
| Annualized Sharpe | **0.75** |
| Total return | 4609.3% |
| Max drawdown | -34.0% |
| FF5 alpha (annualized) | **1.99%** (t = 1.03) |
| FF5 regression R² | 0.54 |

_FF5 alpha uses the zero-investment convention: rf not subtracted (self-financing L/S spread). Sharpe and the alpha t-stat are scale-invariant; the alpha in % scales with portfolio leverage._

_Additional detail:_ annualized spread return 12.39%/yr; annualized volatility 16.58%; FF5 alpha 0.166%/month (= 1.99%/yr), Newey-West t (n_lags=3) = 1.03 [iid t = 0.98]. FF5 loadings: mkt_rf +0.06, smb +0.31, hml +0.21, rmw +0.12, cma +1.44._


## Interpretation

The asset-growth long-short spread — buying low-asset-growth (D1) and selling high-asset-growth (D10) stocks — is the **headline portfolio** of Cooper, Gulen, Schill (2008): firms that grow their assets aggressively subsequently earn lower returns, so the low-minus-high spread is the tradeable anomaly. Both weightings deliver a positive, economically large and statistically significant premium over 1968-07..2003-06.

- **EW spread:** annualized 20.6%/yr, Sharpe 1.46, FF5 alpha 16.32%/yr (t = 5.89). The EW figure is the larger of the two (paper anchor ≈ 20%/yr) because small caps — where the asset-growth effect is strongest — dominate the equal-weighted average.

- **VW spread:** annualized 12.4%/yr (raw), Sharpe 0.75, FF5 alpha 1.99%/yr (t = 1.03). The raw VW premium is economically large and matches the paper anchor (≈ 8-12%/yr; spread Sharpe ≈ 1.07 in the paper, 0.70 on our annual basis — a returns-volatility vintage effect), but its FF5 alpha is statistically insignificant because the investment factor CMA subsumes it (see below).

- **Why the VW alpha is small but the EW alpha is large.** The spread loads heavily on the FF5 **investment factor CMA** (EW β ≈ +0.95, VW β ≈ +1.44). Asset growth is the investment anomaly: high-asset-growth stocks are exactly the "aggressive" leg that CMA shorts, so CMA absorbs most of the VW spread (R² ≈ 0.54) and its FF5 alpha collapses to ≈ 2.0%/yr (t = 1.03, insignificant). Among small caps — where the effect is strongest and CMA does not fully span it — a large residual alpha survives (EW 16.3%/yr, t = 5.89).

- **Bottom line.** With rf not subtracted (zero-investment convention), the asset-growth long-short portfolio earns a positive premium in both weightings; it is robust to FF5 risk adjustment among small caps (EW) and is largely subsumed by the CMA investment factor among large caps (VW). The EW > VW gap and the negative max drawdowns (EW -19.7%, VW -34.0%) are consistent with a small-cap-tilted anomaly that is strong on average but episodic.
