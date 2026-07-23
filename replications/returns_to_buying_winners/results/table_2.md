# Table II — Post-ranking betas and average market capitalizations

Jegadeesh & Titman (1993), Table II. The ten 6-month/6-month relative-strength
portfolios, Jan 1965 – Dec 1989 (300 months). PRIMARY = RAW series (A3-revision).
Beta: OLS slope of the overlapping 300-month EW decile return series on the CRSP
value-weighted monthly index (dsi.vwretd compounded daily→monthly) over the same
300 months (A6). Average market cap: time-series average across the 300 formation
cohorts of the equal-weighted mean of member me_millions (|prc|·shrout·1000/1e6)
at formation, $ millions.

| Portfolio | Post-ranking beta | Avg market cap ($ millions) |
|-----------|------------------:|----------------------------:|
| P1 (decile 1) | 1.42 | 170.77 |
| P2 (decile 2) | 1.23 | 340.23 |
| P3 (decile 3) | 1.18 | 462.22 |
| P4 (decile 4) | 1.15 | 532.38 |
| P5 (decile 5) | 1.13 | 600.91 |
| P6 (decile 6) | 1.13 | 634.82 |
| P7 (decile 7) | 1.13 | 685.12 |
| P8 (decile 8) | 1.15 | 685.17 |
| P9 (decile 9) | 1.19 | 580.81 |
| P10 (decile 10) | 1.29 | 364.92 |
| P10 − P1 (zero-cost) | -0.13 | — |

## Anchor checks (ours vs paper)

| metric | ours | paper | deviation |
|--------|-----:|------:|----------:|
| P1_beta | 1.418775 | 1.36 | +4.3% |
| P1_mcap_musd | 170.765964 | 208.24 | -18.0% |
| P5_beta | 1.132216 | 1.09 | +3.9% |
| P5_mcap_musd | 600.912098 | 692.89 | -13.3% |
| P10_beta | 1.290168 | 1.28 | +0.8% |
| P10_mcap_musd | 364.924816 | 495.13 | -26.3% |
| P10_P1_beta | -0.128607 | -0.08 | -60.8% |

**Per-cell evaluation:** 21 cells — 18 Tier 1 / 3 Tier 2 / 0 FAIL (rule: within tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; else FAIL).
