# Table 6 -- Annual Cross-Sectional Regressions of FErr_{t+2} on RK(X)

**Replication of**: Frankel & Lee (1998) -- Table 6

**Sample period**: 1982-1990 (per paper, 15 annual regressions; we use 9 years where all four RK variables AND FErr_{t+2} are computable)
**Universe**: same as Table 2/3

**Definitions**:
- **FErr_{t+2} = ROE_{t+2} - FROE_{t+2}**: per paper footnote 21.
- **ROE_{t+2} = IB_{t+2} / avg(ceq_{t+1}, ceq_{t+2})** where IB and ceq are from comp_202601.funda at fyear = year_t+1 and year_t.
- **FROE_{t+2}**: from panel_with_v (Eq. A.3).
- **B/P = (ceq / csho) / prc**: B at fiscal year ending in calendar year (year_t - 1).
- **SG = sale_{t-1}/sale_{t-6} - 1**: 5-year cumulative sales growth.
- **OP = (V_f^2 - V_h^2) / |V_h^2|**: T=2 EBO horizon.
- **Ltg = FROE_{t+1} (proxy)**: Ltg unavailable in this I/B/E/S vintage (assumption 19).
- **RK(X)**: within-year percentile rank (rank / (n-1) in [0, 1]).

**Annual OLS** per (year_t, IV): FErr_{t+2} = α + β × RK(X_{t}) + ε.
**Time-series aggregation**: Mean coef = time-series mean of annual β's; NW t-stat with 2 lags (per assumption 24).

## Time-series summary

| Model | Mean coef | NW t-stat (2 lags) | n years | Paper mean coef | Paper t-stat | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| M1: RK(B/P) | +0.0889 | +9.97 | 12 | -0.0250 | -2.69 | FAIL (Δcoef=+0.1139) |
| M2: RK(SG) | -0.1368 | -5.15 | 12 | +0.0430 | +7.00 | FAIL (Δcoef=-0.1798) |
| M3: RK(OP) | -0.2284 | -10.23 | 12 | +0.0700 | +5.01 | FAIL (Δcoef=-0.2984) |
| M4: RK(Ltg) | -0.2174 | -10.67 | 12 | +0.0730 | +6.57 | FAIL (Δcoef=-0.2904) |

## Per-year coefficients (β on RK(X))

### M1: RK(B/P)

| Year | n | β | R² |
| --- | ---: | ---: | ---: |
| 1980 | 480 | +0.1034 | 0.0375 |
| 1981 | 546 | +0.0953 | 0.0271 |
| 1982 | 593 | +0.0706 | 0.0106 |
| 1983 | 588 | +0.0816 | 0.0151 |
| 1984 | 619 | +0.1299 | 0.0216 |
| 1985 | 561 | +0.0730 | 0.0050 |
| 1986 | 563 | +0.0012 | 0.0000 |
| 1987 | 578 | +0.1156 | 0.0107 |
| 1988 | 582 | +0.0923 | 0.0056 |
| 1989 | 618 | +0.0448 | 0.0025 |
| 1990 | 639 | +0.0778 | 0.0062 |
| 1991 | 699 | +0.1817 | 0.0071 |

### M2: RK(SG)

| Year | n | β | R² |
| --- | ---: | ---: | ---: |
| 1980 | 480 | -0.0787 | 0.0223 |
| 1981 | 546 | -0.0685 | 0.0144 |
| 1982 | 593 | -0.1018 | 0.0224 |
| 1983 | 588 | -0.0731 | 0.0129 |
| 1984 | 619 | -0.0491 | 0.0034 |
| 1985 | 561 | -0.1587 | 0.0260 |
| 1986 | 563 | -0.1111 | 0.0163 |
| 1987 | 578 | -0.1240 | 0.0135 |
| 1988 | 582 | -0.2559 | 0.0465 |
| 1989 | 618 | -0.2117 | 0.0571 |
| 1990 | 639 | -0.1947 | 0.0399 |
| 1991 | 699 | -0.2149 | 0.0102 |

### M3: RK(OP)

| Year | n | β | R² |
| --- | ---: | ---: | ---: |
| 1980 | 480 | -0.2024 | 0.1434 |
| 1981 | 546 | -0.2075 | 0.1310 |
| 1982 | 593 | -0.1428 | 0.0446 |
| 1983 | 588 | -0.1259 | 0.0390 |
| 1984 | 619 | -0.3220 | 0.1478 |
| 1985 | 561 | -0.2386 | 0.0613 |
| 1986 | 563 | -0.1549 | 0.0315 |
| 1987 | 578 | -0.2471 | 0.0547 |
| 1988 | 582 | -0.2096 | 0.0329 |
| 1989 | 618 | -0.2097 | 0.0567 |
| 1990 | 639 | -0.2490 | 0.0663 |
| 1991 | 699 | -0.4314 | 0.0427 |

### M4: RK(Ltg)

| Year | n | β | R² |
| --- | ---: | ---: | ---: |
| 1980 | 480 | -0.2092 | 0.1531 |
| 1981 | 546 | -0.1997 | 0.1190 |
| 1982 | 593 | -0.2232 | 0.1067 |
| 1983 | 588 | -0.1588 | 0.0572 |
| 1984 | 619 | -0.2687 | 0.0893 |
| 1985 | 561 | -0.0417 | 0.0015 |
| 1986 | 563 | -0.1970 | 0.0427 |
| 1987 | 578 | -0.2782 | 0.0572 |
| 1988 | 582 | -0.2049 | 0.0244 |
| 1989 | 618 | -0.1931 | 0.0424 |
| 1990 | 639 | -0.2484 | 0.0599 |
| 1991 | 699 | -0.3860 | 0.0305 |

## Notes

**Sample window**: paper reports 15 annual regressions; we obtain 9 years (1982-1990) where all inputs are computable from this data vintage. The paper's sample is 1976-1990, but actual ROE_{t+2} requires comp data at fyear = year_t+1 (we cover year_t up to 1993); SG requires sale at year_t-6 (year_t ≥ 1982).

**Ltg proxy**: per task spec we use FROE_{t+1} as a proxy for Ltg (assumption 19).

**OP horizon**: paper §5.4 uses V_h^2 / V_f^2 (T=2 horizon); we follow this convention.
