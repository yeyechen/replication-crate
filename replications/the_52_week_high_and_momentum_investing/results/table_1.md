# Table I — George & Hwang (2004): average monthly returns, (6,6) strategies, EW, all months 1963-07 .. 2001-12 (462 months)

Machinery: signal at formation f -> 30/30 sort (signal asc, permno asc tie-break) -> cohort held f+1..f+6 -> month-t value = mean of the 6 cohorts formed at t-6..t-1. No skip month. Returns in percent.

Holding-period returns: panel column `ret_dl` (delisting-adjusted); ranking signals always on original ret.

## Official metrics (wh_* = PRIMARY signal wh_sig_dc)

| cell name | paper value | our value | deviation pp | deviation % | tier |
|---|---:|---:|---:|---:|---|
| jt_winner | 1.5300 | 1.5224 | -0.0076 | -0.5% | Tier 1 |
| jt_loser | 1.0500 | 1.0504 | +0.0004 | +0.0% | Tier 1 |
| jt_w_minus_l | 0.4800 | 0.4720 | -0.0080 | -1.7% | Tier 1 |
| jt_w_minus_l_tstat | 2.3500 | 2.2505 | -0.0995 | -4.2% | Tier 1 |
| mg_winner | 1.4800 | 1.5240 | +0.0440 | +3.0% | Tier 1 |
| mg_loser | 1.0300 | 0.9494 | -0.0806 | -7.8% | Tier 1 |
| mg_w_minus_l | 0.4500 | 0.5747 | +0.1247 | +27.7% | Tier 1 |
| mg_w_minus_l_tstat | 3.4300 | 4.5364 | +1.1064 | +32.3% | Tier 1 |
| wh_winner | 1.5100 | 1.4680 | -0.0420 | -2.8% | Tier 1 |
| wh_loser | 1.0600 | 1.0447 | -0.0153 | -1.4% | Tier 1 |
| wh_w_minus_l | 0.4500 | 0.4233 | -0.0267 | -5.9% | Tier 1 |
| wh_w_minus_l_tstat | 2.0000 | 1.7568 | -0.2432 | -12.2% | Tier 1 |

**Hit rate: 12 Tier 1 / 0 Tier 2 / 0 FAIL out of 12**

_Tier 2 ⚠ = sign matches but |ours/paper| > 2 (magnitude far off; see audit1.md spot-check 10). FAIL cells with |paper| < 0.05 are rounding-boundary artifacts unless noted._

## 52WH signal adjudication (PRIMARY wh_sig_dc vs VARIANT wh_sig_hi_abs = |prc|/max(|askhi|))

| metric | paper | wh_sig_dc (PRIMARY) | err pp | wh_sig_hi_abs (VARIANT) | err pp |
|---|---:|---:|---:|---:|---:|
| wh_winner | 1.5100 | 1.4680 | -0.0420 | 1.4634 | -0.0466 |
| wh_loser | 1.0600 | 1.0447 | -0.0153 | 1.0492 | -0.0108 |
| wh_w_minus_l | 0.4500 | 0.4233 | -0.0267 | 0.4142 | -0.0358 |
| wh_w_minus_l_tstat | 2.0000 | 1.7568 | -0.2432 | 1.7290 | -0.2710 |

- |W-L error|: wh_sig_dc 0.0267pp vs wh_sig_hi_abs 0.0358pp
- Sum of |error| over the 4 metrics: wh_sig_dc 0.3271 vs wh_sig_hi_abs 0.3641
- **Pick: wh_sig_dc (PRIMARY)** (for the Replicator to lock)

## Universe size at formation (per signal, over the 467 formation months 1963-01-31 .. 2001-11-30)

| signal | mean n | min n | max n | months with n<4 |
|---|---:|---:|---:|---:|
| jt_sig | 4552.1 | 1896 | 7122 | 0 |
| mg_sig | 4552.1 | 1896 | 7122 | 0 |
| wh_sig_dc | 4784.7 | 1951 | 7396 | 0 |
| wh_sig_hi_abs | 4784.7 | 1951 | 7396 | 0 |

- Min cohorts available per holding month across all W/L series: 6 (6 = no cohort ever dropped by missing returns).