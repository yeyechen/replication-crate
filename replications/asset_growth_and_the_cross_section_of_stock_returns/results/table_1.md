# Table I — Formation-Period Characteristics of Asset-Growth Deciles

Cooper, Gulen, and Schill (2008), *Asset Growth and the Cross-Section of Stock Returns* (Journal of Finance). "At the end of June of each year t over 1968 to 2002, stocks are allocated into deciles based on asset growth (ASSETG). The numbers in each cell are time-series averages of yearly cross-sectional medians, with the exception of average market value (MV-AVG), in millions of $, which is the time-series average of yearly cross-sectional mean capitalization." (content.md L140)

**Statistics convention (rule sample_stats_convention, L140):** each decile cell is the time-series average (over 35 June formation years, 1968-2002) of the yearly cross-sectional median within the decile, computed with nanmedian decile-by-decile; MV-AVG uses the yearly cross-sectional mean instead. Spread (10-1) = D10 minus D1 under the same per-column convention. t(spread) is the time-series t-statistic of the yearly D10-D1 cross-sectional spread (mean divided by std(ddof=1)/sqrt(N_years), N_years = 35). Ratio variables (ASSETG, L2ASSETG, BM, EP, Leverage, ROA, BHRET6, BHRET36, ACCRUALS, ISSUANCE) are in decimal form; ASSETS, MV, MV-AVG in $millions.

**Data-vintage note (Assumption 7):** the 2026 Compustat vintage contains more small-denominator dormant-shell records than the paper's ~2005 vintage, so the ASSETG upper-tail (D8-D10) medians run above the paper's values. No extra filter is applied; this is reported honestly, not forced to match.

**ISSUANCE split-adjustment (Assumption 8 refinement, audit M1):** the ISSUANCE column is the 5-year change in SPLIT-ADJUSTED shares outstanding, `csho * cfacshr` at each fiscal-year-end (CRSP's cumulative share-adjustment factor attached via the foundation's PIT CRSP-Compustat link), so mechanical stock-split share increases are NOT counted as issuance. Convention verified on permno 10032 (gvkey 012945): on a 2:1 split shrout doubles while cfacshr halves, keeping shrout*cfacshr continuous. This brings ISSUANCE from the raw-csho magnitudes (D1 0.148 / D10 1.013 / spread 0.865 / t 12.11, i.e. 1.85-3.91x the paper) to D1 0.071 / D10 0.392 / spread 0.321 / t 7.81 (0.88-1.45x the paper; paper D1 0.0803 / D10 0.3012 / spread 0.2209 / t 8.36). The raw-csho values are retained in table_1_eval.json (`table.ISSUANCE.raw_csho`).

| Row | ASSETG | L2ASSETG | ASSETS | MV | MV-AVG | BM | EP | Leverage | ROA | BHRET6 | BHRET36 | ACCRUALS | ISSUANCE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 (Low) | -0.1817 | 0.0352 | 29.32 | 20.89 | 170.46 | 0.8980 | -0.1265 | 0.2328 | -0.0077 | 0.0854 | -0.2891 | -0.1346 | 0.0709 |
| 2 | -0.0505 | 0.0441 | 70.82 | 39.74 | 392.00 | 1.0649 | 0.0258 | 0.2402 | 0.0917 | 0.1001 | -0.0416 | -0.0725 | 0.0273 |
| 3 | 0.0040 | 0.0535 | 134.19 | 80.02 | 829.23 | 1.0087 | 0.0699 | 0.2430 | 0.1218 | 0.0914 | 0.1324 | -0.0499 | 0.0181 |
| 4 | 0.0412 | 0.0662 | 185.60 | 121.99 | 1149.83 | 0.9418 | 0.0822 | 0.2440 | 0.1348 | 0.0814 | 0.2570 | -0.0368 | 0.0203 |
| 5 | 0.0750 | 0.0831 | 179.57 | 135.57 | 1248.24 | 0.8656 | 0.0846 | 0.2322 | 0.1443 | 0.0817 | 0.3135 | -0.0267 | 0.0253 |
| 6 | 0.1124 | 0.1062 | 170.30 | 141.56 | 1286.30 | 0.7687 | 0.0831 | 0.2169 | 0.1515 | 0.0722 | 0.3738 | -0.0182 | 0.0353 |
| 7 | 0.1609 | 0.1329 | 141.20 | 140.65 | 1085.33 | 0.6908 | 0.0794 | 0.2111 | 0.1579 | 0.0685 | 0.4442 | -0.0091 | 0.0525 |
| 8 | 0.2391 | 0.1662 | 106.92 | 128.65 | 1049.30 | 0.6119 | 0.0737 | 0.2085 | 0.1617 | 0.0650 | 0.5466 | 0.0064 | 0.0816 |
| 9 | 0.4105 | 0.2177 | 86.21 | 113.64 | 811.20 | 0.5231 | 0.0651 | 0.2296 | 0.1525 | 0.0517 | 0.6753 | 0.0283 | 0.1683 |
| 10 (High) | 1.1409 | 0.3190 | 54.19 | 95.74 | 476.83 | 0.4167 | 0.0446 | 0.2170 | 0.1144 | 0.0146 | 0.8863 | 0.1065 | 0.3921 |
| Spread (10-1) | 1.3227 | 0.2838 | 24.87 | 74.85 | 306.36 | -0.4814 | 0.1712 | -0.0158 | 0.1221 | -0.0708 | 1.1754 | 0.2411 | 0.3212 |
| t(spread) | 7.95 | 12.47 | 4.39 | 4.61 | 3.53 | -7.46 | 6.06 | -1.26 | 8.73 | -3.68 | 15.55 | 18.49 | 7.81 |
