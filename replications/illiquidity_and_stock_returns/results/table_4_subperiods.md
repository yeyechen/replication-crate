# Table 4 corollary — §3.3 six-subperiod robustness (model 10m, market column)

Amihud (2002), §3.3 (inputs/content.md L772-777): "the sample of 408 months is divided into six equal subperiods of 68 months each and model (10m) is estimated for each subperiod... All six coefficients g1 are positive, with mean 0.871 and median 0.827. All six coefficients g2 are negative with mean -7.089 and median -5.984."

Specification: identical to the build_table_4 market column — (RM - Rf)_m in percent = g0 + g1 lnMILLIQ_{m-1} + g2 u^M_m + g3 JANDUM_m + w, with u^M from the FULL-SAMPLE Kendall-corrected monthly AR(1) (as in Table 4); OLS t-stats; source data/_cache/{milliq,market_ret,rf}.parquet.

Window convention: the paper's "68 months" is six equal parts of its stated 408-month MILLIQ series (1963-01..1996-12). Applied to the 396-month regression window of model (10m) (1964-01..1996-12 — which loses the first month(s) to the lnMILLIQ_{m-1} lag, consistent with our Table 4 T = 396), the equal split is six windows of 66 months each.

| Window | g0 | g1 (OLS t) | g2 (OLS t) | g3 (OLS t) | R2 | N |
|---|---:|---:|---:|---:|---:|---:|
| 1964-01..1969-06 | 0.901 | 1.351 (+2.31) | -11.861 (-5.43) | 4.812 (+2.99) | 0.365 | 66 |
| 1969-07..1974-12 | -0.531 | 1.109 (+1.31) | -17.073 (-5.75) | 6.843 (+2.68) | 0.368 | 66 |
| 1975-01..1980-06 | 0.599 | 3.298 (+3.60) | -10.480 (-4.21) | 10.589 (+4.68) | 0.436 | 66 |
| 1980-07..1985-12 | 2.100 | 1.549 (+0.97) | -1.323 (-0.76) | 1.520 (+0.67) | 0.043 | 66 |
| 1986-01..1991-06 | 0.306 | 0.826 (+1.05) | -1.736 (-1.40) | 5.282 (+2.03) | 0.096 | 66 |
| 1991-07..1996-12 | 1.228 | 0.553 (+1.30) | -2.421 (-2.51) | 2.499 (+1.89) | 0.168 | 66 |

## Summary vs the paper

- Sign counts: g1 positive in 6/6 windows (paper: 6/6); g2 negative in 6/6 windows (paper: 6/6).
- g1 across the six windows: mean = 1.448 (paper 0.871, %dev +66.2%); median = 1.230 (paper 0.827, %dev +48.7%).
- g2 across the six windows: mean = -7.482 (paper -7.089, %dev -5.5%); median = -6.450 (paper -5.984, %dev -7.8%).
- Honest comparison: the paper's subperiod g2 mean (-7.089) is MORE negative than its own full-sample g2 (-5.52, Table 4); our full-sample g2(market) = -4.182 (Table 4), and our subperiod mean/median are -7.482/-6.450. The open-universe adoption is locked (A5-revised / §3.3 diagnostic, four pre-registered rules); this gap is reported as-is and NOT chased with further universe variants.

## Chow-style stability of the AR(1)s (paper L561, L759)

Classic Chow break test (F = ((RSS_p - RSS1 - RSS2)/k) / ((RSS1 + RSS2)/(n1 + n2 - 2k)), k = 2 parameters; the paper claims stability 'as indicated by the Chow test' for both AR(1)s without reporting the statistic):

- Annual AR(1) of ln AILLIQ (T = 33; split 1964-1980 (n1 = 17) vs 1981-1996 (n2 = 16)): F = 0.087, p = 0.917 — fail to reject stability at 5%.
- Monthly AR(1) of ln MILLIQ (T = 407; split 1963-02..1980-06 (n1 = 209) vs 1980-07..1996-12 (n2 = 198)): F = 2.223, p = 0.110 — fail to reject stability at 5%.
