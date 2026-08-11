# Table 1 — MAX-Sorted Decile Portfolios

**Replication of**: Bali, Cakici, Whitelaw (2011) — Table 1
**Sample period**: July 1962 – December 2005 (monthly)
**Universe**: NYSE/AMEX/Nasdaq common shares (shrcd 10/11, exchcd 1/2/3)
**N months**: 521
**N observations (stock-months)**: 2,433,223
**Avg obs/month**: 4670.3

Returns and alphas are in **percent per month**. MAX is in **percent**.

| Decile | VW Ret | VW Alpha | EW Ret | EW Alpha | Avg MAX |
|---|---|---|---|---|---|
| D1 | 0.97 | 0.51 | 1.41 | 0.81 | 1.13 |
| D2 | 1.03 | 0.64 | 1.48 | 0.96 | 2.38 |
| D3 | 1.00 | 0.58 | 1.60 | 1.07 | 3.20 |
| D4 | 1.15 | 0.69 | 1.60 | 1.05 | 4.00 |
| D5 | 1.08 | 0.61 | 1.58 | 1.04 | 4.88 |
| D6 | 1.22 | 0.78 | 1.57 | 1.02 | 5.92 |
| D7 | 1.05 | 0.58 | 1.51 | 0.92 | 7.23 |
| D8 | 1.01 | 0.53 | 1.51 | 0.90 | 9.04 |
| D9 | 0.74 | 0.28 | 1.30 | 0.66 | 12.15 |
| D10 | 0.43 | -0.08 | 1.27 | 0.47 | 23.52 |
| --- | --- | --- | --- | --- | --- |
| **D10 - D1** | -0.54 | -0.98 | -0.14 | -0.74 |   |

## t-statistics (Newey-West)

Newey-West lags for D10-D1 raw return spread: n_lags = 4
Newey-West lags for FF-Carhart alpha t-stat: n_lags = 4

| Spread | t-stat |
| --- | --- |
| VW raw return | -1.45 |
| EW raw return | -0.35 |
| VW FF-Carhart alpha | -2.39 |
| EW FF-Carhart alpha | -2.06 |
