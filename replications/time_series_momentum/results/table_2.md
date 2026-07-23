# Table 2 — t-statistics of TSMOM(k,h) alphas (7-factor: MKT/BOND/GSCI proxies + SMB/HML/UMD)

Intercept t-stat, Newey-West h-1 lags (A10; plain OLS at h=1). Cell format: ours (paper).
Tiers: Tier 1 within 200% relative tolerance; Tier 2 sign match; FAIL sign flip.
MKT/BOND/GSCI are EW of the paper's own equity/bond/commodity futures (A2 — MSCI World / Barclays Agg / S&P GSCI not in ClickHouse).

## Panel A: All assets  (tiers: {'Tier 1': 56, 'Tier 2': 6, 'FAIL': 2, 'SKIP': 0})

| k\h | 1 | 3 | 6 | 9 | 12 | 24 | 36 | 48 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | +3.60 (+4.34) | +3.42 (+4.68) | +3.25 (+3.83) | +3.64 (+4.29) | +5.46 (+5.12) | +2.90 (+3.02) | +1.90 (+2.74) | +2.00 (+1.90) |
| 3 | +4.40 (+5.35) | +2.30 (+4.42)· | +2.06 (+3.54)· | +4.24 (+4.73) | +5.11 (+4.50) | +2.55 (+2.60) | +1.56 (+1.97) | +1.75 (+1.52) |
| 6 | +3.02 (+5.03) | +1.80 (+4.54)· | +3.43 (+4.93) | +5.20 (+5.32) | +4.40 (+4.43) | +2.01 (+2.79) | +1.22 (+1.89) | +1.49 (+1.42) |
| 9 | +3.23 (+6.06)· | +3.73 (+6.13) | +4.92 (+5.78) | +4.72 (+5.07) | +3.77 (+4.10) | +1.85 (+2.57) | +1.13 (+1.45) | +1.29 (+1.19) |
| 12 | +5.33 (+6.61) | +4.80 (+5.60) | +4.11 (+4.44) | +3.80 (+3.69) | +3.01 (+2.85) | +1.50 (+1.68) | +0.94 (+0.66) | +1.13 (+0.46) |
| 24 | +3.04 (+3.95) | +2.70 (+3.19) | +2.12 (+2.44) | +1.75 (+1.95) | +1.18 (+1.50) | +0.37 (+0.20) | +0.47 (-0.09)**!!** | +0.53 (-0.33)**!!** |
| 36 | +1.83 (+2.70) | +1.58 (+2.20) | +1.06 (+1.44) | +0.92 (+0.96) | +0.65 (+0.62) | +0.45 (+0.28) | +0.43 (+0.07)· | +0.70 (+0.20)· |
| 48 | +1.61 (+1.84) | +1.46 (+1.55) | +1.32 (+1.16) | +1.00 (+1.00) | +0.70 (+0.86) | +0.31 (+0.38) | +0.50 (+0.46) | +0.69 (+0.74) |

## Panel B: Commodity futures  (tiers: {'Tier 1': 15, 'Tier 2': 16, 'FAIL': 33, 'SKIP': 0})

| k\h | 1 | 3 | 6 | 9 | 12 | 24 | 36 | 48 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | +0.47 (+2.44)· | +0.61 (+2.89)· | -0.91 (+2.81)**!!** | -1.64 (+2.16)**!!** | +0.38 (+3.26)· | -1.13 (+1.81)**!!** | -1.38 (+1.56)**!!** | +0.06 (+1.94) |
| 3 | +1.65 (+4.54)· | -0.26 (+3.79)**!!** | -1.77 (+3.20)**!!** | -0.91 (+3.12)**!!** | +0.51 (+3.29)· | -0.64 (+1.51)**!!** | -0.58 (+1.28)**!!** | +0.21 (+1.62) |
| 6 | -0.09 (+3.86)**!!** | -1.45 (+3.53)**!!** | -1.08 (+3.34)**!!** | +0.17 (+3.43)· | +0.21 (+2.74)· | -0.54 (+1.59)**!!** | -0.54 (+1.25)**!!** | +0.50 (+1.48) |
| 9 | -1.33 (+3.77)**!!** | -0.90 (+4.05)**!!** | +0.18 (+3.89)· | +0.37 (+3.06)· | +0.12 (+2.31)· | -0.18 (+1.27)**!!** | -0.26 (+0.71)**!!** | +0.71 (+1.04) |
| 12 | +1.89 (+4.66)· | +1.02 (+4.08)· | +0.28 (+2.64)· | +0.08 (+1.85) | -0.08 (+1.46)**!!** | -0.36 (+0.58)**!!** | -0.25 (+0.14)**!!** | +0.73 (+0.57) |
| 24 | -0.21 (+2.83)**!!** | -0.62 (+2.15)**!!** | -0.71 (+1.24)**!!** | -0.80 (+0.58)**!!** | -1.13 (+0.18)**!!** | -1.30 (-0.60) | -0.38 (-0.33) | -0.21 (-0.14) |
| 36 | -0.79 (+1.28)**!!** | -0.85 (+0.74)**!!** | -1.15 (+0.07)**!!** | -1.02 (-0.25)· | -1.09 (-0.34)· | -0.54 (-0.03)· | -0.16 (+0.34)**!!** | -0.10 (+0.65)**!!** |
| 48 | +0.36 (+1.19) | +0.24 (+1.17) | +0.27 (+1.04) | +0.11 (+1.01) | -0.08 (+0.92)**!!** | -0.14 (+0.75)**!!** | +0.10 (+1.16) | +0.22 (+1.29) |

## Panel C: Equity index futures  (tiers: {'Tier 1': 12, 'Tier 2': 29, 'FAIL': 23, 'SKIP': 0})

| k\h | 1 | 3 | 6 | 9 | 12 | 24 | 36 | 48 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | +0.25 (+1.05) | +0.15 (+2.36)· | +0.87 (+2.89)· | +0.19 (+3.08)· | +0.66 (+3.24)· | +0.03 (+2.28)· | -0.58 (+1.93)**!!** | -0.47 (+1.28)**!!** |
| 3 | -0.37 (+1.48)**!!** | +0.17 (+2.23)· | +0.22 (+2.21)· | +0.29 (+2.81)· | +0.22 (+2.78)· | -0.54 (+2.00)**!!** | -1.27 (+1.57)**!!** | -0.99 (+1.14)**!!** |
| 6 | +1.11 (+3.50)· | +0.44 (+3.18)· | +0.81 (+3.49)· | +0.72 (+3.52)· | +1.07 (+3.03)· | +0.17 (+2.08)· | -0.90 (+1.36)**!!** | -0.51 (+0.88)**!!** |
| 9 | +1.28 (+4.21)· | +1.08 (+3.94)· | +1.24 (+3.79)· | +0.98 (+3.30)· | +0.98 (+2.64)· | -0.02 (+1.96)**!!** | -1.10 (+1.21)**!!** | -0.76 (+0.75)**!!** |
| 12 | +1.87 (+3.77)· | +1.39 (+3.55)· | +1.13 (+3.03)· | +0.95 (+2.58)· | +0.72 (+2.02)· | -0.40 (+1.57)**!!** | -1.32 (+0.78)**!!** | -1.00 (+0.33)**!!** |
| 24 | +0.78 (+2.04)· | +0.94 (+2.22)· | +0.72 (+1.96) | +0.50 (+1.70) | +0.42 (+1.49) | -0.92 (+0.87)**!!** | -0.83 (+0.43)**!!** | -0.95 (+0.13)**!!** |
| 36 | +1.90 (+1.86) | +1.52 (+1.66) | +1.30 (+1.26) | +0.88 (+0.90) | +0.62 (+0.66) | +0.16 (+0.34) | -0.01 (+0.02)**!!** | +0.71 (+0.08)· |
| 48 | -0.27 (+0.81)**!!** | +0.13 (+0.84) | +0.06 (+0.58) | -0.02 (+0.44)**!!** | -0.17 (+0.36)**!!** | -0.62 (+0.12)**!!** | -0.17 (+0.01)**!!** | +0.90 (+0.23)· |

## Panel D: Bond futures  (tiers: {'Tier 1': 15, 'Tier 2': 25, 'FAIL': 0, 'SKIP': 0})

| k\h | 1 | 3 | 6 | 9 | 12 | 24 | 36 | 48 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | +5.11 (+3.31)· | +5.31 (+2.66)· | +4.80 (+1.84) | +4.86 (+2.65)· | +5.09 (+2.88)· | +3.43 (+1.76) | +3.44 (+1.60) | +4.14 (+1.40) |
| 3 | +5.27 (+2.45)· | +4.16 (+1.52) | +3.82 (+1.10)· | +5.28 (+1.99) | +5.09 (+1.80) | +3.57 (+1.27) | +3.42 (+1.05)· | +4.42 (+1.00)· |
| 6 | +3.31 (+2.16)· | +3.28 (+2.04)· | +3.95 (+2.18)· | +4.85 (+2.53)· | +4.44 (+2.24)· | +3.03 (+1.71) | +2.92 (+1.36) | +4.27 (+1.37)· |
| 9 | +4.63 (+2.93)· | +4.45 (+2.61)· | +4.55 (+2.68)· | +4.61 (+2.55)· | +4.31 (+2.43)· | +3.02 (+1.83) | +3.20 (+1.17) | +4.30 (+1.40)· |
| 12 | +4.93 (+3.53) | +4.54 (+2.82)· | +4.21 (+2.57)· | +4.43 (+2.42)· | +4.12 (+2.18)· | +2.80 (+1.47) | +3.16 (+1.12) | +4.40 (+0.96)· |

## FAIL cells (58)
- alpha_tstat_all_assets_k24_h36: ours +0.47 vs paper -0.09
- alpha_tstat_all_assets_k24_h48: ours +0.53 vs paper -0.33
- alpha_tstat_commodity_k1_h6: ours -0.91 vs paper +2.81
- alpha_tstat_commodity_k1_h9: ours -1.64 vs paper +2.16
- alpha_tstat_commodity_k1_h24: ours -1.13 vs paper +1.81
- alpha_tstat_commodity_k1_h36: ours -1.38 vs paper +1.56
- alpha_tstat_commodity_k3_h3: ours -0.26 vs paper +3.79
- alpha_tstat_commodity_k3_h6: ours -1.77 vs paper +3.20
- alpha_tstat_commodity_k3_h9: ours -0.91 vs paper +3.12
- alpha_tstat_commodity_k3_h24: ours -0.64 vs paper +1.51
- alpha_tstat_commodity_k3_h36: ours -0.58 vs paper +1.28
- alpha_tstat_commodity_k6_h1: ours -0.09 vs paper +3.86
- alpha_tstat_commodity_k6_h3: ours -1.45 vs paper +3.53
- alpha_tstat_commodity_k6_h6: ours -1.08 vs paper +3.34
- alpha_tstat_commodity_k6_h24: ours -0.54 vs paper +1.59
- alpha_tstat_commodity_k6_h36: ours -0.54 vs paper +1.25
- alpha_tstat_commodity_k9_h1: ours -1.33 vs paper +3.77
- alpha_tstat_commodity_k9_h3: ours -0.90 vs paper +4.05
- alpha_tstat_commodity_k9_h24: ours -0.18 vs paper +1.27
- alpha_tstat_commodity_k9_h36: ours -0.26 vs paper +0.71
- alpha_tstat_commodity_k12_h12: ours -0.08 vs paper +1.46
- alpha_tstat_commodity_k12_h24: ours -0.36 vs paper +0.58
- alpha_tstat_commodity_k12_h36: ours -0.25 vs paper +0.14
- alpha_tstat_commodity_k24_h1: ours -0.21 vs paper +2.83
- alpha_tstat_commodity_k24_h3: ours -0.62 vs paper +2.15
- alpha_tstat_commodity_k24_h6: ours -0.71 vs paper +1.24
- alpha_tstat_commodity_k24_h9: ours -0.80 vs paper +0.58
- alpha_tstat_commodity_k24_h12: ours -1.13 vs paper +0.18
- alpha_tstat_commodity_k36_h1: ours -0.79 vs paper +1.28
- alpha_tstat_commodity_k36_h3: ours -0.85 vs paper +0.74
- alpha_tstat_commodity_k36_h6: ours -1.15 vs paper +0.07
- alpha_tstat_commodity_k36_h36: ours -0.16 vs paper +0.34
- alpha_tstat_commodity_k36_h48: ours -0.10 vs paper +0.65
- alpha_tstat_commodity_k48_h12: ours -0.08 vs paper +0.92
- alpha_tstat_commodity_k48_h24: ours -0.14 vs paper +0.75
- alpha_tstat_equity_index_k1_h36: ours -0.58 vs paper +1.93
- alpha_tstat_equity_index_k1_h48: ours -0.47 vs paper +1.28
- alpha_tstat_equity_index_k3_h1: ours -0.37 vs paper +1.48
- alpha_tstat_equity_index_k3_h24: ours -0.54 vs paper +2.00
- alpha_tstat_equity_index_k3_h36: ours -1.27 vs paper +1.57
- alpha_tstat_equity_index_k3_h48: ours -0.99 vs paper +1.14
- alpha_tstat_equity_index_k6_h36: ours -0.90 vs paper +1.36
- alpha_tstat_equity_index_k6_h48: ours -0.51 vs paper +0.88
- alpha_tstat_equity_index_k9_h24: ours -0.02 vs paper +1.96
- alpha_tstat_equity_index_k9_h36: ours -1.10 vs paper +1.21
- alpha_tstat_equity_index_k9_h48: ours -0.76 vs paper +0.75
- alpha_tstat_equity_index_k12_h24: ours -0.40 vs paper +1.57
- alpha_tstat_equity_index_k12_h36: ours -1.32 vs paper +0.78
- alpha_tstat_equity_index_k12_h48: ours -1.00 vs paper +0.33
- alpha_tstat_equity_index_k24_h24: ours -0.92 vs paper +0.87
- alpha_tstat_equity_index_k24_h36: ours -0.83 vs paper +0.43
- alpha_tstat_equity_index_k24_h48: ours -0.95 vs paper +0.13
- alpha_tstat_equity_index_k36_h36: ours -0.01 vs paper +0.02
- alpha_tstat_equity_index_k48_h1: ours -0.27 vs paper +0.81
- alpha_tstat_equity_index_k48_h9: ours -0.02 vs paper +0.44
- alpha_tstat_equity_index_k48_h12: ours -0.17 vs paper +0.36
- alpha_tstat_equity_index_k48_h24: ours -0.62 vs paper +0.12
- alpha_tstat_equity_index_k48_h36: ours -0.17 vs paper +0.01
