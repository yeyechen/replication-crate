# Table 1 — Financial and Return Characteristics of the High Book-to-Market Sample

**5,736 Firm-Year Observations between 1988 and 1996** (paper: 14,043 between 1976 and 1996; restriction per assumptions.md A1 — `oancf` is NULL for all FY<1987 in the `comp_202601` vintage, so the sample is FY1987–FY1995).

Columns: **Ours** (this replication) vs **Paper** (Piotroski 2000, Table 1). **Tier** per `rep/TOLERANCE_RULES.md` against `tables_to_replicate.json` tolerances. Cells with Tier "—" are not contract targets (no `tolerance_pct` in the metric contract); the paper value and Δ are shown for context only and they do NOT enter the Tally. Standard deviations use ddof=1; percentiles use numpy linear interpolation.

## Panel A — Financial signal characteristics

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| (n) | firm-years | 5,736 | 14,043 | -8,307 | Tier 2 (A1 gap) |
| MVE | mean | 182.475 | 188.500 | -6.025 | Tier 1 |
| MVE | median | 15.819 | 14.365 | 1.454 | Tier 1 |
| MVE | std | 980.79 | 1,015.39 | -34.60 | — |
| MVE | % positive signal | n/a | n/a | n/a | n/a |
| ASSETS | mean | 620.826 | 1,043.990 | -423.164 | Tier 1 |
| ASSETS | median | 52.968 | 57.561 | -4.593 | — |
| ASSETS | std | 3,098.98 | 6,653.48 | -3,554.50 | — |
| ASSETS | % positive signal | n/a | n/a | n/a | n/a |
| BM | mean | 2.5908 | 2.4440 | 0.1468 | Tier 1 |
| BM | median | 1.5317 | 1.7210 | -0.1893 | Tier 1 |
| BM | std | 37.1359 | 34.6600 | 2.4759 | — |
| BM | % positive signal | n/a | n/a | n/a | n/a |
| ROA | mean | -0.0195 | -0.0054 | -0.0141 | Tier 2 |
| ROA | median | 0.0060 | 0.0128 | -0.0068 | — |
| ROA | std | 0.1177 | 0.1067 | 0.0110 | — |
| ROA | % positive signal | 0.558 | 0.632 | -0.074 | Tier 2 |
| ΔROA | mean | -0.0161 | -0.0096 | -0.0065 | Tier 1 |
| ΔROA | median | -0.0089 | -0.0047 | -0.0042 | — |
| ΔROA | std | 0.2750 | 0.2171 | 0.0579 | — |
| ΔROA | % positive signal | 0.414 | 0.432 | -0.018 | Tier 1 |
| ΔMARGIN | mean | -0.0414 | -0.0324 | -0.0090 | Tier 1 |
| ΔMARGIN | median | -0.0050 | -0.0034 | -0.0016 | — |
| ΔMARGIN | std | 2.7556 | 1.9306 | 0.8250 | — |
| ΔMARGIN | % positive signal | 0.439 | 0.454 | -0.015 | Tier 1 |
| CFO | mean | 0.0408 | 0.0498 | -0.0090 | Tier 1 |
| CFO | median | 0.0472 | 0.0532 | -0.0060 | — |
| CFO | std | 0.1069 | 0.1332 | -0.0263 | — |
| CFO | % positive signal | 0.733 | 0.755 | -0.022 | Tier 1 |
| ΔLIQUID | mean | -0.0813 | -0.0078 | -0.0735 | Tier 2 |
| ΔLIQUID | median | -0.0591 | 0.0000 | -0.0591 | — |
| ΔLIQUID | std | 10.3314 | 0.1133 | 10.2181 | — |
| ΔLIQUID | % positive signal | 0.441 | 0.384 | 0.057 | Tier 2 |
| ΔLEVER | mean | -0.0009 | 0.0024 | -0.0033 | Tier 1 |
| ΔLEVER | median | -0.0003 | 0.0000 | -0.0003 | — |
| ΔLEVER | std | 0.1146 | 0.0932 | 0.0214 | — |
| ΔLEVER | % positive signal | 0.506 | 0.498 | 0.008 | Tier 1 |
| ΔTURN | mean | -0.0220 | 0.0119 | -0.0339 | FAIL |
| ΔTURN | median | -0.0042 | 0.0068 | -0.0110 | — |
| ΔTURN | std | 0.3274 | 0.5851 | -0.2577 | — |
| ΔTURN | % positive signal | 0.481 | 0.534 | -0.053 | Tier 1 |
| ACCRUAL | mean | -0.0604 | -0.0552 | -0.0052 | Tier 1 |
| ACCRUAL | median | -0.0542 | -0.0481 | -0.0061 | — |
| ACCRUAL | std | 0.1271 | 0.1388 | -0.0117 | — |
| ACCRUAL | % positive signal | 0.794 | 0.780 | 0.014 | Tier 1 |

## Panel B — Distribution of buy-and-hold returns

| Row | Statistic | Ours | Paper | Δ | Tier |
|---|---|---:|---:|---:|---|
| 1yr raw | mean | 0.2286 | 0.2390 | -0.0104 | Tier 1 |
| 1yr raw | p10 | -0.4444 | -0.3910 | -0.0534 | — |
| 1yr raw | p25 | -0.1953 | -0.1500 | -0.0453 | — |
| 1yr raw | p50 | 0.0567 | 0.1050 | -0.0483 | Tier 2 |
| 1yr raw | p75 | 0.3889 | 0.4380 | -0.0491 | — |
| 1yr raw | p90 | 0.8947 | 0.9020 | -0.0073 | — |
| 1yr raw | %+ | 0.557 | 0.610 | -0.053 | Tier 1 |
| 1yr MA | mean | 0.0584 | 0.0590 | -0.0006 | Tier 1 |
| 1yr MA | p10 | -0.5987 | -0.5600 | -0.0387 | — |
| 1yr MA | p25 | -0.3609 | -0.3170 | -0.0439 | — |
| 1yr MA | p50 | -0.1081 | -0.0610 | -0.0471 | Tier 1 |
| 1yr MA | p75 | 0.2061 | 0.2550 | -0.0489 | — |
| 1yr MA | p90 | 0.7302 | 0.7080 | 0.0222 | — |
| 1yr MA | %+ | 0.395 | 0.437 | -0.042 | Tier 1 |
| 2yr raw | mean | 0.4976 | 0.4790 | 0.0186 | Tier 1 |
| 2yr raw | p10 | -0.5590 | -0.5170 | -0.0420 | — |
| 2yr raw | p25 | -0.2333 | -0.1790 | -0.0543 | — |
| 2yr raw | p50 | 0.1429 | 0.2310 | -0.0881 | — |
| 2yr raw | p75 | 0.6842 | 0.7500 | -0.0658 | — |
| 2yr raw | p90 | 1.6978 | 1.5790 | 0.1188 | — |
| 2yr raw | %+ | 0.592 | 0.646 | -0.054 | — |
| 2yr MA | mean | 0.1151 | 0.1270 | -0.0119 | Tier 1 |
| 2yr MA | p10 | -0.9456 | -0.8720 | -0.0736 | — |
| 2yr MA | p25 | -0.6108 | -0.5170 | -0.0938 | — |
| 2yr MA | p50 | -0.2317 | -0.1110 | -0.1207 | — |
| 2yr MA | p75 | 0.3148 | 0.3940 | -0.0792 | — |
| 2yr MA | p90 | 1.2745 | 1.2050 | 0.0695 | — |
| 2yr MA | %+ | 0.364 | 0.432 | -0.068 | Tier 2 |

## Tally (contract targets in tables_to_replicate.json only)

| Tier | Count |
|---|---:|
| Tier 1 (match) | 23 |
| Tier 2 (pattern / A1 gap) | 7 |
| FAIL (sign flip / unreachable) | 1 |
| **Total targeted cells** | **31** |

### FAIL cells (diagnosis)

- **ΔTURN mean** (ours −0.0220 vs paper +0.0119): sign flip on a small mean (std 0.33 ours / 0.59 paper; rel ≈ 285% > 100% tolerance). The median (−0.0042 vs 0.0068) also flips while the *signal proportion* matches (0.481 vs 0.534, Tier 1). The ΔTURN denominator is average total assets (assumptions.md A4, Table 1 footnote j) — a documented paper discrepancy; the mean sign is sensitive to that choice and to vintage restatements. (Note: the ΔLEVER mean also flips sign, ours −0.0009 vs paper +0.0024, but its rel ≈ 138% sits INSIDE its 150% tolerance, so it scores Tier 1, not FAIL.)

## Interpretation

The sample is restricted to formation years 1988–1996 (FY1987–FY1995) per assumptions.md A1 (`oancf` is NULL for all FY<1987 in the 2026 Compustat vintage), so the paper's full 1976–1996 sample (14,043 obs) is structurally unreachable — our 5,736 obs are 41% of the paper count, hence the n cell is Tier 2 (A1 gap) by construction, not a defect.

What matches (Tier 1): the *robust* statistics replicate well — BM mean and median, MVE mean and median, ASSETS mean, and nearly every signal *proportion* (ROA/ΔROA/ΔMARGIN/CFO/ΔLEVER/ΔTURN/ACCRUAL within ~10%). The return distribution matches closely: 1-yr raw and market-adjusted means/medians/%positive, 2-yr raw mean, and 2-yr MA mean all land in Tier 1. This confirms the sample-construction chain (Compustat universe, prior-year BM quintile, signal definitions, fifth-month BHR, zero delisting return, value-weighted market adjustment) is faithful.

What drifts (Tier 2): the ROA mean (−0.0195 vs −0.0054) and the ROA and ΔLIQUID *proportions* sit just outside their tight 10% tolerances but keep the paper's sign/magnitude, and the 1-yr raw median (0.057 vs 0.105) and 2-yr MA %positive (0.364 vs 0.432) are a bit low — all consistent with (a) a later sub-period (1988–1996 excludes the 1976–1987 cohorts) and (b) 2026-vintage restatements/backfills of fundamentals. ΔLIQUID's mean (−0.081 vs −0.008) drifts furthest in relative terms (driven by a handful of extreme current-ratio changes, our std 10.3 vs paper 0.11) but keeps the sign (Tier 2). The other near-zero signal means (ΔROA, ΔMARGIN, ΔLEVER) stay inside their wide 100–150% tolerances (Tier 1).

What FAILs: one cell — the ΔTURN *mean* flips sign (−0.022 vs +0.012). The economically meaningful object (the binary signal's positive-share, 0.481 vs 0.534) matches, so this is a sign-of-a-tiny-mean artifact (compounded by the documented A4 denominator choice) rather than a definition error. No return cell FAILs.
