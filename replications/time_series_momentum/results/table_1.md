# Table 1 — annualized mean / vol of futures excess returns (full sample, panel window)

Tiers: Tier 1 = |ours-paper|/|paper| <= tolerance (mean 15%, vol 10%); Tier 2 = sign match; FAIL = sign flip.
Counts — mean cells: {'Tier 1': 3, 'Tier 2': 21, 'FAIL': 29, 'SKIP': 0}  |  vol cells: {'Tier 1': 34, 'Tier 2': 19, 'FAIL': 0, 'SKIP': 0}
NOTE (A1): means use the US T-bill rf for all instruments -> ~-4pp/yr uniform shift vs the paper's means (documented assumption; mean cells expected at Tier 2 on bonds/FX, sign-flips flagged for inspection).

| instrument | mean (ours) | mean (paper) | tier | vol (ours) | vol (paper) | tier |
|---|---:|---:|---|---:|---:|---|
| AEX | +2.93 | +7.72 | Tier 2 | 20.35 | 19.18 | Tier 1 |
| ALUMINUM | +2.12 | +0.97 | Tier 2 | 19.46 | 23.50 | Tier 2 |
| AUDUSD **SIGN-FLIP** | -2.31 | +1.85 | FAIL | 11.33 | 10.86 | Tier 1 |
| AUS10Y **SIGN-FLIP** | -3.82 | +3.83 | FAIL | 1.50 | 8.53 | Tier 2 |
| AUS3Y **SIGN-FLIP** | -3.48 | +1.34 | FAIL | 1.63 | 2.57 | Tier 2 |
| BRENTOIL | +9.03 | +13.87 | Tier 2 | 33.65 | 32.51 | Tier 1 |
| CAC40 | +2.32 | +6.73 | Tier 2 | 19.74 | 20.87 | Tier 1 |
| CADUSD **SIGN-FLIP** | -5.46 | +0.60 | FAIL | 6.43 | 6.29 | Tier 1 |
| CAN10Y **SIGN-FLIP** | -2.59 | +4.04 | FAIL | 9.92 | 7.36 | Tier 2 |
| CATTLE **SIGN-FLIP** | -3.01 | +4.52 | FAIL | 17.26 | 17.14 | Tier 1 |
| COCOA **SIGN-FLIP** | -0.57 | +5.61 | FAIL | 31.37 | 32.38 | Tier 1 |
| COFFEE | +0.04 | +5.72 | Tier 2 | 38.01 | 38.62 | Tier 1 |
| COPPER | +7.79 | +8.90 | Tier 1 | 27.04 | 27.39 | Tier 1 |
| CORN | -0.75 | -3.19 | Tier 2 | 26.51 | 24.37 | Tier 1 |
| COTTON **SIGN-FLIP** | -0.23 | +1.41 | FAIL | 28.94 | 24.35 | Tier 2 |
| CRUDE | +4.92 | +11.61 | Tier 2 | 34.18 | 34.72 | Tier 1 |
| DAX | +5.61 | +6.33 | Tier 1 | 21.59 | 20.41 | Tier 1 |
| EURO10Y **SIGN-FLIP** | -1.53 | +2.40 | FAIL | 5.16 | 5.74 | Tier 2 |
| EURO2Y **SIGN-FLIP** | -2.64 | +1.02 | FAIL | 1.72 | 1.53 | Tier 2 |
| EURO30Y **SIGN-FLIP** | -1.91 | +4.71 | FAIL | 8.20 | 11.70 | Tier 2 |
| EURO5Y **SIGN-FLIP** | -2.02 | +2.56 | FAIL | 3.50 | 3.22 | Tier 1 |
| EURUSD **SIGN-FLIP** | -3.07 | +1.57 | FAIL | 11.47 | 11.21 | Tier 1 |
| FTSE100 | +3.22 | +6.97 | Tier 2 | 16.39 | 17.77 | Tier 1 |
| FTSEMIB | +2.47 | +6.13 | Tier 2 | 23.15 | 24.59 | Tier 1 |
| GASOIL | +3.28 | +11.95 | Tier 2 | 33.57 | 33.18 | Tier 1 |
| GILT **SIGN-FLIP** | -3.05 | +3.00 | FAIL | 8.47 | 9.12 | Tier 1 |
| GOLD **SIGN-FLIP** | -0.57 | +5.36 | FAIL | 21.75 | 21.37 | Tier 1 |
| HEATOIL | +2.87 | +9.79 | Tier 2 | 30.74 | 33.78 | Tier 1 |
| HOGS | +1.98 | +3.39 | Tier 2 | 33.73 | 26.01 | Tier 2 |
| IBEX35 | +9.05 | +9.37 | Tier 1 | 21.40 | 21.84 | Tier 1 |
| JGB10Y **SIGN-FLIP** | -2.82 | +3.66 | FAIL | 5.60 | 5.40 | Tier 1 |
| JPYUSD **SIGN-FLIP** | -1.33 | +1.35 | FAIL | 12.34 | 11.66 | Tier 1 |
| NATGAS **SIGN-FLIP** | +9.68 | -9.74 | FAIL | 44.04 | 53.30 | Tier 2 |
| NICKEL | +10.76 | +12.69 | Tier 2 | 36.42 | 35.76 | Tier 1 |
| NOKUSD | +5.76 | +1.37 | Tier 2 | 9.96 | 10.56 | Tier 1 |
| NZDUSD **SIGN-FLIP** | -0.92 | +2.31 | FAIL | 13.63 | 12.01 | Tier 2 |
| PLATINUM | +0.31 | +13.15 | Tier 2 | 23.28 | 20.95 | Tier 2 |
| SEKUSD **SIGN-FLIP** | +10.63 | -0.05 | FAIL | 11.01 | 11.06 | Tier 1 |
| SILVER **SIGN-FLIP** | -0.32 | +3.17 | FAIL | 27.97 | 31.11 | Tier 2 |
| SOYBEANS **SIGN-FLIP** | -1.13 | +5.57 | FAIL | 24.79 | 27.26 | Tier 1 |
| SOYMEAL **SIGN-FLIP** | -0.13 | +6.14 | FAIL | 27.28 | 24.59 | Tier 2 |
| SOYOIL **SIGN-FLIP** | -0.42 | +1.07 | FAIL | 27.17 | 25.39 | Tier 1 |
| SP500 | +4.34 | +3.47 | Tier 2 | 15.34 | 15.45 | Tier 1 |
| SPI200 | +2.79 | +7.25 | Tier 2 | 13.40 | 18.33 | Tier 2 |
| SUGAR | +8.47 | +4.44 | Tier 2 | 46.95 | 42.87 | Tier 1 |
| TOPIX **SIGN-FLIP** | -6.61 | +2.29 | FAIL | 20.07 | 18.66 | Tier 1 |
| UNLEADED | +13.47 | +15.92 | Tier 2 | 40.68 | 37.36 | Tier 1 |
| US10Y **SIGN-FLIP** | -3.16 | +3.80 | FAIL | 7.46 | 9.30 | Tier 2 |
| US2Y **SIGN-FLIP** | -3.14 | +1.65 | FAIL | 2.20 | 1.86 | Tier 2 |
| US5Y **SIGN-FLIP** | -2.99 | +3.17 | FAIL | 4.81 | 4.25 | Tier 2 |
| USLONG **SIGN-FLIP** | -4.16 | +9.50 | FAIL | 12.00 | 18.56 | Tier 2 |
| WHEAT | -0.51 | -1.84 | Tier 2 | 25.85 | 25.11 | Tier 1 |
| ZINC | +6.35 | +1.98 | Tier 2 | 26.17 | 24.76 | Tier 1 |
