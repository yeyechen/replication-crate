# Table 3 — NYSE Firm Size Deciles, 1973-1981

Mean daily EW decile return (percent/day) over 1973-1981; average annual OLS
market-model beta over 9 years (1973-1981, market = CRSP EW NYSE+AMEX dsi.ewretd,
A13); and the Dimson (1979) summed-beta estimator used here as the implementable
form of the Scholes-Williams (1977) non-synchronous-trading correction: for each
year y in 1974-1981 one OLS of the decile EW return on (r_m,t-1, r_m,t, r_m,t+1),
beta_SW,y = b_lag + b_contemp + b_lead, averaged over the 8 years (the paper's
exact SW formula variant is not stated; the previous iteration's
(beta_{y-1}+2beta_y+beta_{y+1})/(1+2rho_y) form was structurally incapable of
matching — see iteration-2 diagnosis).

| Size decile | Mean daily return (%) | Paper | Mean OLS beta | Paper | Mean SW/Dimson beta | Paper |
|---|---|---|---|---|---|---|
| 1 (smallest) | 0.112 | 0.111 | 1.32 | 1.11 | 1.35 | 1.16 |
| 2 | 0.090 | 0.084 | 1.33 | 1.10 | 1.30 | 1.10 |
| 3 | 0.077 | 0.070 | 1.33 | 1.07 | 1.26 | 1.06 |
| 4 | 0.069 | 0.063 | 1.28 | 1.02 | 1.21 | 1.01 |
| 5 | 0.063 | 0.061 | 1.22 | 1.00 | 1.16 | 0.98 |
| 6 | 0.057 | 0.053 | 1.18 | 0.97 | 1.08 | 0.94 |
| 7 | 0.051 | 0.048 | 1.17 | 0.96 | 1.06 | 0.93 |
| 8 | 0.049 | 0.046 | 1.10 | 0.93 | 1.01 | 0.90 |
| 9 | 0.034 | 0.038 | 1.09 | 0.92 | 0.97 | 0.88 |
| 10 (largest) | 0.023 | 0.021 | 1.06 | 0.92 | 0.91 | 0.83 |
