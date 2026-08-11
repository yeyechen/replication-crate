# Table VI. Bid-Ask Spread Bias Correction

Market model: R_pt − R_ft = α_p + β_p (R_mt − R_ft) + u_pt.  Sample period 1963-01-01 .. 1987-12-31.  White (1980) HC1 standard errors.

Panel I: standard lag1 (full prior-month return).  Panel II: lag1_excl_last_day — prior-month return computed from daily returns EXCLUDING the last trading day of month t-1; stocks not trading on the last day of t-1 are dropped (paper §III.C).

## Panel I (full lag1)

| Strategy | Sub-period | α (per month) | t(α) | β | n_obs |
|---|---|---|---|---|---|
| S0 | Jan-Dec | +0.0297 | (+15.38) | +0.287 | 300 |
| S0 | January | +0.0299 | (+2.28) | +0.702 | 25 |
| S0 | Feb-Dec | +0.0273 | (+14.78) | +0.155 | 275 |
| S1 | Jan-Dec | +0.0284 | (+13.44) | +0.329 | 298 |
| S1 | January | +0.0393 | (+2.71) | +0.764 | 25 |
| S1 | Feb-Dec | +0.0249 | (+12.61) | +0.169 | 273 |

## Panel II (lag1 excl last day)

| Strategy | Sub-period | α (per month) | t(α) | β | n_obs |
|---|---|---|---|---|---|
| S0 | Jan-Dec | +0.0251 | (+12.39) | +0.240 | 269 |
| S0 | January | +nan | (+nan) | +nan | 22 |
| S0 | Feb-Dec | +0.0232 | (+11.94) | +0.131 | 247 |
| S1 | Jan-Dec | +0.0212 | (+10.26) | +0.312 | 299 |
| S1 | January | +0.0256 | (+1.84) | +0.779 | 24 |
| S1 | Feb-Dec | +0.0182 | (+9.35) | +0.160 | 275 |

