# 52-week-high signal granularity: wh_sig_dc (daily close) vs wh_sig_cl (month-end close)

George & Hwang (2004). Side-by-side per-cell comparison for the 48 Table III cells + the 4 Table I 52WH metrics. The ONLY thing that differs between the two columns is the 52WH price series used for the inner ranking:
- `cl` = wh_sig_cl = |prc(f)| / max of MSF month-end closes over f-11..f
- `dc` = wh_sig_dc = |prc(f)| / max of DSF daily closes over f-11..f (literal 'highest price achieved', L122)

Everything else identical: same jt_sig outer rankings, 30/40/30 sorts, (6,6) timing, nonempty-cell W-L rule. |err| and tiers are vs the paper value. Tiers use each metric's tolerance_pct from tables_to_replicate.json.

| cell name | paper | cl | dc | \|err_cl\| | \|err_dc\| | tier_cl | tier_dc |
|---|---:|---:|---:|---:|---:|---|---|
| pa_winner_winner_all | 1.6300 | 1.6581 | 1.6616 | 0.0281 | 0.0316 | Tier 1 | Tier 1 |
| pa_winner_winner_exjan | 1.4100 | 1.4147 | 1.4552 | 0.0047 | 0.0452 | Tier 1 | Tier 1 |
| pa_winner_loser_all | 1.1700 | 1.3114 | 1.2730 | 0.1414 | 0.1030 | Tier 1 | Tier 1 |
| pa_winner_loser_exjan | 0.3100 | 0.8776 | 0.7680 | 0.5676 | 0.4580 | Tier 2 | Tier 2 |
| pa_winner_w_minus_l_all | 0.4600 | 0.3467 | 0.3886 | 0.1133 | 0.0714 | Tier 1 | Tier 1 |
| pa_winner_w_minus_l_all_tstat | 2.1500 | 3.0206 | 2.6840 | 0.8706 | 0.5340 | Tier 2 | Tier 1 |
| pa_winner_w_minus_l_exjan | 1.1100 | 0.5370 | 0.6873 | 0.5730 | 0.4227 | Tier 2 | Tier 1 |
| pa_winner_w_minus_l_exjan_tstat | 6.1100 | 4.9008 | 5.0897 | 1.2092 | 1.0203 | Tier 1 | Tier 1 |
| pa_middle_winner_all | 1.3000 | 1.3623 | 1.3471 | 0.0623 | 0.0471 | Tier 1 | Tier 1 |
| pa_middle_winner_exjan | 1.1000 | 1.1516 | 1.1786 | 0.0516 | 0.0786 | Tier 1 | Tier 1 |
| pa_middle_loser_all | 1.0400 | 1.0680 | 1.0901 | 0.0280 | 0.0501 | Tier 1 | Tier 1 |
| pa_middle_loser_exjan | 0.2400 | 0.4144 | 0.3900 | 0.1744 | 0.1500 | Tier 2 | Tier 2 |
| pa_middle_w_minus_l_all | 0.2600 | 0.2943 | 0.2570 | 0.0343 | 0.0030 | Tier 1 | Tier 1 |
| pa_middle_w_minus_l_all_tstat | 1.3300 | 1.8040 | 1.3100 | 0.4740 | 0.0200 | Tier 1 | Tier 1 |
| pa_middle_w_minus_l_exjan | 0.8600 | 0.7372 | 0.7886 | 0.1228 | 0.0714 | Tier 1 | Tier 1 |
| pa_middle_w_minus_l_exjan_tstat | 6.2800 | 5.2684 | 4.5999 | 1.0116 | 1.6801 | Tier 1 | Tier 1 |
| pa_loser_winner_all | 1.2700 | 1.1242 | 1.3018 | 0.1458 | 0.0318 | Tier 1 | Tier 1 |
| pa_loser_winner_exjan | 1.0400 | 0.0618 | 0.3353 | 0.9782 | 0.7047 | Tier 2 | Tier 2 |
| pa_loser_loser_all | 1.0500 | 1.0364 | 1.0455 | 0.0136 | 0.0045 | Tier 1 | Tier 1 |
| pa_loser_loser_exjan | 0.0100 | -0.0280 | -0.0496 | 0.0380 | 0.0596 | FAIL | FAIL |
| pa_loser_w_minus_l_all | 0.5600 | 0.0878 | 0.2751 | 0.4722 | 0.2849 | Tier 2 | Tier 2 |
| pa_loser_w_minus_l_all_tstat | 1.6200 | 0.2656 | 0.6708 | 1.3544 | 0.9492 | Tier 2 | Tier 2 |
| pa_loser_w_minus_l_exjan | 0.9800 | 0.0898 | 0.4106 | 0.8902 | 0.5694 | Tier 2 | Tier 2 |
| pa_loser_w_minus_l_exjan_tstat | 3.1300 | 0.2914 | 1.0449 | 2.8386 | 2.0851 | Tier 2 | Tier 2 |
| pb_winner_winner_all | 1.6300 | 1.6581 | 1.6616 | 0.0281 | 0.0316 | Tier 1 | Tier 1 |
| pb_winner_winner_exjan | 1.4100 | 1.4147 | 1.4552 | 0.0047 | 0.0452 | Tier 1 | Tier 1 |
| pb_winner_loser_all | 1.2700 | 1.1242 | 1.3018 | 0.1458 | 0.0318 | Tier 1 | Tier 1 |
| pb_winner_loser_exjan | 1.0400 | 0.0618 | 0.3353 | 0.9782 | 0.7047 | Tier 2 | Tier 2 |
| pb_winner_w_minus_l_all | 0.2200 | 0.5339 | 0.3581 | 0.3139 | 0.1381 | Tier 2 | Tier 2 |
| pb_winner_w_minus_l_all_tstat | 0.6800 | 1.4493 | 0.8206 | 0.7693 | 0.1406 | Tier 2 | Tier 1 |
| pb_winner_w_minus_l_exjan | 0.2400 | 1.3529 | 1.1170 | 1.1129 | 0.8770 | Tier 2 | Tier 2 |
| pb_winner_w_minus_l_exjan_tstat | 0.7400 | 4.1017 | 2.7877 | 3.3617 | 2.0477 | Tier 2 | Tier 2 |
| pb_middle_winner_all | 1.4800 | 1.4322 | 1.4978 | 0.0478 | 0.0178 | Tier 1 | Tier 1 |
| pb_middle_winner_exjan | 1.0300 | 0.9839 | 1.0271 | 0.0461 | 0.0029 | Tier 1 | Tier 1 |
| pb_middle_loser_all | 1.2100 | 1.1354 | 1.1089 | 0.0746 | 0.1011 | Tier 1 | Tier 1 |
| pb_middle_loser_exjan | 0.7300 | 0.5845 | 0.5941 | 0.1455 | 0.1359 | Tier 1 | Tier 1 |
| pb_middle_w_minus_l_all | 0.2700 | 0.2968 | 0.3888 | 0.0268 | 0.1188 | Tier 1 | Tier 1 |
| pb_middle_w_minus_l_all_tstat | 2.1200 | 2.2475 | 2.5074 | 0.1275 | 0.3874 | Tier 1 | Tier 1 |
| pb_middle_w_minus_l_exjan | 0.3000 | 0.3994 | 0.4330 | 0.0994 | 0.1330 | Tier 1 | Tier 1 |
| pb_middle_w_minus_l_exjan_tstat | 2.3500 | 3.0267 | 2.7021 | 0.6767 | 0.3521 | Tier 1 | Tier 1 |
| pb_loser_winner_all | 1.1700 | 1.3114 | 1.2730 | 0.1414 | 0.1030 | Tier 1 | Tier 1 |
| pb_loser_winner_exjan | 0.3100 | 0.8776 | 0.7680 | 0.5676 | 0.4580 | Tier 2 | Tier 2 |
| pb_loser_loser_all | 1.0500 | 1.0364 | 1.0455 | 0.0136 | 0.0045 | Tier 1 | Tier 1 |
| pb_loser_loser_exjan | 0.0100 | -0.0280 | -0.0496 | 0.0380 | 0.0596 | FAIL | FAIL |
| pb_loser_w_minus_l_all | 0.1200 | 0.2750 | 0.2275 | 0.1550 | 0.1075 | Tier 2 | Tier 2 |
| pb_loser_w_minus_l_all_tstat | 0.7600 | 1.3412 | 1.1577 | 0.5812 | 0.3977 | Tier 2 | Tier 2 |
| pb_loser_w_minus_l_exjan | 0.2900 | 0.9056 | 0.8175 | 0.6156 | 0.5275 | Tier 2 | Tier 2 |
| pb_loser_w_minus_l_exjan_tstat | 1.9600 | 5.9856 | 5.5918 | 4.0256 | 3.6318 | Tier 2 | Tier 2 |
| T1_wh_winner | 1.5100 | 1.5059 | 1.5010 | 0.0041 | 0.0090 | Tier 1 | Tier 1 |
| T1_wh_loser | 1.0600 | 1.0790 | 1.0850 | 0.0190 | 0.0250 | Tier 1 | Tier 1 |
| T1_wh_w_minus_l | 0.4500 | 0.4269 | 0.4161 | 0.0231 | 0.0339 | Tier 1 | Tier 1 |
| T1_wh_w_minus_l_tstat | 2.0000 | 1.9282 | 1.7034 | 0.0718 | 0.2966 | Tier 1 | Tier 1 |

## Hit-rate summaries

**Table III (48 cells):**
- cl (wh_sig_cl): 27 Tier 1 / 19 Tier 2 / 2 FAIL
- dc (wh_sig_dc): 30 Tier 1 / 16 Tier 2 / 2 FAIL

**Combined (48 Table III + 4 Table I 52WH = 52 cells):**
- cl (wh_sig_cl): 31 Tier 1 / 19 Tier 2 / 2 FAIL
- dc (wh_sig_dc): 34 Tier 1 / 16 Tier 2 / 2 FAIL

## Total |deviation| from paper (sum of |ours - paper|)

| scope | cl (wh_sig_cl) | dc (wh_sig_dc) | better |
|---|---:|---:|---|
| Table III (48 cells) | 26.2946 | 20.0304 | dc |
| Table I 52WH (4 metrics) | 0.1179 | 0.3645 | cl |
| **All 48 + 4 = 52 cells** | **26.4125** | **20.3949** | **dc** |

## Recommendation

- **Lock `wh_sig_dc` as the single primary 52WH signal** for all remaining tables.
- Margin (total |deviation| across 52 cells): cl 26.4125 vs dc 20.3949 -> dc better by 6.0176 (22.8% lower total error).
- Table III only: cl 26.2946 vs dc 20.0304 (margin 6.2642).