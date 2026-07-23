# Table 5 Panel C — regressions on the diversified TSMOM factor

XSMOM per A11: 12-month formation skipping the most recent month; weights (rank − median rank)/Σ|rank − median rank|; 40%/σ scaling. Rows: XSMOM variants + UMD/HML/SMB regressed on TSMOM_ALL (DJCS rows excluded — not in ClickHouse).

| row | beta (t) | alpha %/mo (t) | R² | paper beta (t) | paper alpha (t) | paper R² |
|---|---|---|---:|---|---|---:|
| XSMOM_ALL | +0.72 (+16.28) | -0.39 (-2.28) | 0.47 | +0.66 (+15.17) | -0.16 (-1.17) | 0.44 |
| XSMOM_COM | +0.45 (+7.46) | -0.82 (-3.52) | 0.16 | +0.65 (+14.61) | -0.09 (-0.66) | 0.42 |
| XSMOM_EQ | +0.10 (+1.83) | +0.16 (+0.77) | 0.01 | +0.39 (+7.32) | +0.29 (+1.86) | 0.15 |
| XSMOM_FI | +0.09 (+1.18) | +0.13 (+0.43) | 0.00 | +0.37 (+6.83) | -0.14 (-0.87) | 0.14 |
| XSMOM_FX | +0.24 (+2.99) | -0.37 (-1.19) | 0.03 | +0.75 (+19.52) | -0.19 (-1.71) | 0.56 |
| UMD | +0.41 (+5.64) | +0.14 (+0.51) | 0.10 | +0.49 (+6.56) | -0.28 (-0.93) | 0.13 |
| HML | -0.14 (-2.92) | +0.54 (+2.88) | 0.03 | -0.07 (-1.46) | +0.43 (+2.08) | 0.01 |
| SMB | +0.08 (+1.44) | -0.12 (-0.57) | 0.01 | -0.01 (-0.26) | +0.10 (+0.49) | 0.00 |
