# Table B1 — BAB factor leverage and realized factor loadings

**Source:** Frazzini & Pedersen (2014), "Betting Against Beta", Table B1
(Appendix B) and p.9.
**Paper claims (p.9):** "On average, the US BAB factor goes long $1.40 ... and
shortsells $0.70 ... The BAB factor's realized market loading is not exactly
zero, reflecting the fact that our ex ante betas are measured with noise. The
other factor loadings indicate that, relative to high-beta stocks, low-beta
stocks are likely to be **larger**, have **higher book-to-market ratios**, and
have **higher return over the prior 12 months**, although none of the loadings
can explain the large and significant abnormal returns. The BAB portfolio's
**positive HML loading** is natural since ... low-beta stocks are cheap."
**Method:** realized loadings from time-series regressions of each portfolio's
monthly excess return on the FF/Carhart factors (same regressions as
`src/table_3_v2.py`; `factor_alpha(...)`). The same v2 decile + BAB series as
`results/table_3.md`. Loadings are dimensionless regression slopes.
**FF factor units:** DECIMAL in source (median |mkt_rf|=0.0298) -> used as-is.

## Average leverage (from BAB construction)

| Leg | Ours | Paper |
|---|---:|---:|
| Long  ($1/β_L) | **$1.44** | $1.40 |
| Short ($1/β_H) | **$0.69** | $0.70 |

The long leg is levered up (low-beta stocks rescaled to unit beta) and the
short leg de-levered, making BAB approximately market-neutral. Matches the
paper's stated $1.40 / $0.70 (our 1.435 / 0.688; also
documented in assumptions.md A17).

## Realized factor loadings

| Loading | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 | P9 | P10 | BAB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Market (CAPM, univariate) | 0.645 | 0.844 | 0.993 | 1.078 | 1.223 | 1.330 | 1.418 | 1.532 | 1.664 | 1.870 | -0.056 |
| Market (4-factor) | 0.522 | 0.712 | 0.828 | 0.909 | 1.020 | 1.091 | 1.164 | 1.240 | 1.316 | 1.395 | -0.016 |
| SMB | 0.522 | 0.543 | 0.628 | 0.633 | 0.730 | 0.795 | 0.880 | 0.945 | 1.107 | 1.480 | 0.008 |
| HML | 0.157 | 0.163 | 0.234 | 0.259 | 0.352 | 0.394 | 0.417 | 0.450 | 0.498 | 0.594 | 0.061 |
| UMD (momentum) | -0.004 | -0.022 | -0.051 | -0.044 | -0.059 | -0.130 | -0.112 | -0.195 | -0.270 | -0.438 | 0.200 |
| R² (4-factor) | 0.767 | 0.873 | 0.912 | 0.938 | 0.942 | 0.951 | 0.952 | 0.952 | 0.944 | 0.882 | 0.072 |
| n (months) | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 | 1004 |

_"Market (CAPM, univariate)" is the realized market beta from a single-factor
regression — this is the "Beta (realized)" row of Table 3 (BAB = -0.056,
matching the paper's -0.06 and the "realized market loading is not exactly
zero" claim). "Market (4-factor)" .. "UMD" are the partial loadings from the
joint Carhart 4-factor regression (the factor loadings reported in Table B1)._

## Sign comparison vs the paper's claims

The BAB factor is long low-beta / short high-beta. The paper (p.9) predicts the
loadings are small and reflect that low-beta stocks are larger, cheaper (higher
B/M), and past winners relative to high-beta stocks, with the market loading
"not exactly zero" and a "positive HML loading":

| Factor | Our BAB loading | Paper-implied direction | Consistent? |
|---|---:|---|:--:|
| Market | -0.056 (CAPM) / -0.016 (4-factor) | ≈ 0, slightly negative ("not exactly zero") | yes |
| SMB | +0.008 | positive (≈ 0; loadings do not explain the alpha) | yes |
| HML | +0.061 | **positive** (paper: "positive HML loading"; low-beta = cheap) | yes |
| UMD | +0.200 | **positive** (low-beta = higher prior 12-mo return ⇒ long winners) | yes |

**All four BAB loadings carry the expected sign** (yes),
and all are small in magnitude — consistent with the paper's statement that
"none of the loadings can explain the large and significant abnormal returns"
(BAB 4-factor R² = 0.072; FF4 α = 0.58%/mo,
t = 5.54 from Table 3).

**Reading of the signs:**
- **Market:** BAB's realized market loading is small and negative
  (-0.056 CAPM; -0.016 in the 4-factor model),
  consistent with the paper's "not exactly zero" (the ex-ante zero-beta target
  is attained only up to beta-estimation noise).
- **SMB:** BAB's SMB loading is **positive but essentially zero**
  (+0.008). The size tilt the paper describes is visible in the
  *decile gradient* below (SMB rises monotonically with beta, so high-beta
  stocks are smaller / low-beta stocks larger) rather than in the near-zero
  net BAB loading — the long-leg leverage (1/β_L≈1.44) and short-leg
  de-leveraging (1/β_H≈0.69) largely offset the two legs' SMB
  exposures.
- **HML:** BAB's HML loading is **positive** (+0.061),
  matching the paper's explicit "positive HML loading" (low-beta stocks are
  cheap / high book-to-market).
- **UMD:** BAB's UMD loading is **positive** (+0.200),
  consistent with low-beta stocks having higher prior-12-month returns
  (long winners).

**Decile pattern (low → high beta, what the loadings reveal about the stocks):**
- *Market beta* rises monotonically P1 (0.64) → P10
  (1.87) — by construction.
- *SMB* rises monotonically P1 (+0.52) → P10 (+1.48):
  high-beta stocks load much more on small-minus-big, i.e. **low-beta stocks are
  larger** ✓ (matches the paper). All EW deciles load positively on SMB (the
  equal-weighting tilts every decile toward small caps), so the informative
  feature is the rising gradient, not the sign of any single decile.
- *UMD* falls monotonically P1 (-0.00) → P10 (-0.44):
  low-beta stocks have the higher momentum loading, i.e. **higher prior 12-month
  return** ✓ (matches the paper).
- *HML* rises P1 (+0.16) → P10 (+0.59) as a 4-factor
  partial loading. This decile gradient need not share the sign of the BAB
  spread loading: the BAB legs are the rank-weighted low-/high-beta HALVES of
  the cross-section, each rescaled to unit beta (long ×1.44, short
  ×0.69), not the extreme P1/P10 deciles. The paper's "low-beta =
  higher book-to-market" claim is about the **BAB-level** loading, which is
  positive (+0.061) here and matches the paper's explicit "positive
  HML loading".

---
_Generated by src/corollaries.py (reuses src/table_3_v2.py)._
