# Table I sensitivity — MG industry-level cutoff variant (audit1.md [M5])

Official MG sort (A8): rank individual STOCKS by their industry's 6-month
cumulative VW return with a permno-ordinal tie-break -> the boundary
industry's stocks are arbitrarily split across winner/middle/loser.
Variant (MG-intended reading): rank the 20 INDUSTRIES by their 6-month
cumulative VW return; winner = stocks in the top 6 industries, loser =
stocks in the bottom 6; boundary ties keep ALL members of the tied
industries (inclusive cutoffs). Industry cumrets recomputed from the panel
with the same VW formula as the official pipeline (A7, lagged-mcap weights,
6 consecutive months). Same EW (6,6) machinery, dependent `ret_dl`.

Note: the independent recompute of industry cumrets differs from the
official per-stock mg_sig by <= 1e-3 in 4.6% of (industry, month) cells —
a switcher-membership artifact (stocks changing MG industry inside the
6-month window carry a mixed path in mg_sig); immaterial to the ranking of
the 20 industries (adjacent-industry cumret gaps are orders of magnitude
larger). Official mg pipeline untouched.

## Table I full grid — both MG variants (jt/wh rows identical by construction)

| metric | paper | official (ordinal 30/30) | tier | industry-level | tier |
|---|---:|---:|---|---:|---|
| jt_winner | 1.5300 | 1.5224 | Tier 1 | 1.5224 | Tier 1 |
| jt_loser | 1.0500 | 1.0504 | Tier 1 | 1.0504 | Tier 1 |
| jt_w_minus_l | 0.4800 | 0.4720 | Tier 1 | 0.4720 | Tier 1 |
| jt_w_minus_l_tstat | 2.3500 | 2.2505 | Tier 1 | 2.2505 | Tier 1 |
| mg_winner | 1.4800 | 1.5240 | Tier 1 | 1.5135 | Tier 1 |
| mg_loser | 1.0300 | 0.9494 | Tier 1 | 0.9181 | Tier 1 |
| mg_w_minus_l | 0.4500 | 0.5747 | Tier 1 | 0.5954 | Tier 1 |
| mg_w_minus_l_tstat | 3.4300 | 4.5364 | Tier 1 | 4.5713 | Tier 1 |
| wh_winner | 1.5100 | 1.4680 | Tier 1 | 1.4680 | Tier 1 |
| wh_loser | 1.0600 | 1.0447 | Tier 1 | 1.0447 | Tier 1 |
| wh_w_minus_l | 0.4500 | 0.4233 | Tier 1 | 0.4233 | Tier 1 |
| wh_w_minus_l_tstat | 2.0000 | 1.7568 | Tier 1 | 1.7568 | Tier 1 |

## Industry-tie frequency and cohort sizes

- Table I formation window (1963-01-31 .. 2001-11-30, 467 months): winner-boundary ties in **0** months, loser-boundary ties in **0** months (a boundary tie = an industry exactly tied with the 6th-ranked industry; all its members stay in).
- Industries ranked per formation month: mean 20.0, min 20 (20 = all MG industries present).
- FM formation grid (473 months, f = t-j, j=2..13): **0** months with a boundary tie; 0 months with <12 industries.
- Avg cohort members: official ordinal split W 1365.1 / M 1821.8 / L 1365.1 (forced 30/30); industry-level W 1421.9 / M 2135.4 / L 1255.8 (members of 6/8/6 industries).
- Rankable-set overlap: variant (industry at f defined + cumret finite) 4813 stocks/month vs official (mg_sig non-null) 4552; 94.6% of the variant set is also mg_sig-rankable (the remainder = stocks that switch industry inside the window, rankable at f but not over the full 6 months).

## FM mg_spread before/after (industry-level variant; Table V layout, dependent `ret_dl`, all 8 columns)

| column | official (A8 ordinal) | industry-level | paper |
|---|---:|---:|---:|
| s66_raw_janincl | 0.3804 (t 4.62) | 0.4098 (t 4.59) | 0.2500 |
| s66_raw_janexcl | 0.3573 (t 4.21) | 0.3790 (t 4.09) | 0.2200 |
| s66_ra_janincl | 0.3400 (t 4.14) | 0.3697 (t 4.11) | 0.2500 |
| s66_ra_janexcl | 0.3399 (t 4.10) | 0.3622 (t 3.95) | 0.2400 |
| s612_raw_janincl | 0.2659 (t 3.78) | 0.2747 (t 3.59) | 0.1700 |
| s612_raw_janexcl | 0.2376 (t 3.23) | 0.2530 (t 3.17) | 0.1500 |
| s612_ra_janincl | 0.2895 (t 4.23) | 0.2990 (t 3.93) | 0.2200 |
| s612_ra_janexcl | 0.2701 (t 3.80) | 0.2858 (t 3.64) | 0.2000 |

Anchors: s66_raw_janincl official 0.3804 vs paper 0.25; s66_raw_janexcl official 0.3573 vs paper 0.22.

## MG-weakest check (mg_spread < jt_spread AND mg_spread < wh_spread, all 8 columns)

| column | official WH/JT/MG | MG weakest? | industry WH/JT/MG | MG weakest? |
|---|---|---|---|---|
| s66_raw_janincl | +0.4896 / +0.5295 / +0.3804 | yes | +0.4731 / +0.5203 / +0.4098 | yes |
| s66_raw_janexcl | +0.8745 / +0.6449 / +0.3573 | yes | +0.8550 / +0.6382 / +0.3790 | yes |
| s66_ra_janincl | +0.5916 / +0.5833 / +0.3400 | yes | +0.5821 / +0.5708 / +0.3697 | yes |
| s66_ra_janexcl | +0.8436 / +0.6875 / +0.3399 | yes | +0.8306 / +0.6777 / +0.3622 | yes |
| s612_raw_janincl | +0.3091 / +0.3295 / +0.2659 | yes | +0.2961 / +0.3221 / +0.2747 | yes |
| s612_raw_janexcl | +0.6731 / +0.4192 / +0.2376 | yes | +0.6581 / +0.4118 / +0.2530 | yes |
| s612_ra_janincl | +0.4242 / +0.4144 / +0.2895 | yes | +0.4142 / +0.4055 / +0.2990 | yes |
| s612_ra_janexcl | +0.6569 / +0.4926 / +0.2701 | yes | +0.6449 / +0.4839 / +0.2858 | yes |

NOTE: the FM regression is JOINT — changing the mg dummies shifts the jt/wh coefficients slightly (Frisch-Waugh; same effect as the M2 variant-B note), so the industry-column WH/JT values differ marginally from the official table_5.md.

## Adoption checks (Replicator to ratify)

Rule: adopt the industry-level variant iff BOTH:

1. the MG gap vs the paper shrinks: |mg_w_minus_l − 0.45| official 0.1247 vs industry 0.1454 -> FAIL;
2. MG remains the weakest strategy in EVERY Table V column under the variant (8/8) -> PASS.

**Recommendation: KEEP the official ordinal MG sort (A8); document the MG offset as a tie-break/SIC-vintage effect (non-actionable)**

Official artifacts untouched: results/table_1.md, results/table_5.md, data/strategy_returns.parquet, data/fm_coefficients.parquet. Variant c-series: data/fm_coefficients_mg_ind.parquet.