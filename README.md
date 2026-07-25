# replication-crate

> **Status notes (2026-07-25).** (1) Per-paper `SUMMARY.md` verdicts are
> superseded by the corrected corpus in `training/cases.json` (16 papers:
> 9 accepted / 6 qualified / 1 quarantine, plus 8 pilot records). (2) The
> replication folders are NOT standalone-rebuildable from a fresh clone:
> pipelines import shared utilities from the private `rep-it-up` repo and
> data caches are gitignored by design. Reproducibility from raw sources
> requires ClickHouse access and those utilities.


This repo contains replications of published academic finance papers, done by a multi-agent system (rep-it-up). Each paper has a stand-alone folder with implementation code (SQL + Python), a detailed report and a scored summary comparing our results against the paper's original findings.

Data panels are excluded; the SQL in the src/ directory documents how every dataset is constructed and results can be rebuilt from the source database.

## Papers

<!-- BEGIN PAPER LIST -->
- [Quality minus junk (Asness, Frazzini, Pedersen 2019)](replications/quality_minus_junk/)
- [Betting Against Beta (Frazzini & Pedersen, 2014)](replications/betting_against_beta/)
- [The Other Side of Value: The Gross Profitability Premium (Novy-Marx 2013, JFE)](replications/the_other_side_of_value/)
- [Moskowitz, Ooi & Pedersen (2012), "Time Series Momentum" (JFE 104: 228–250)](replications/time_series_momentum/)
- [Seasonality in the Cross Section of Stock Returns: The International Evidence (Heston & Sadka 2010, JFQA)](replications/seasonality_international_evidence/)
- [Asset Growth and the Cross-Section of Stock Returns (Cooper, Gulen & Schill 2008)](replications/asset_growth_and_the_cross_section_of_stock_returns/)
- [Pontiff & Woodgate (2008), "Share Issuance and Cross-sectional Returns", *Journal of Finance* 63(2)](replications/share_issuance_and_cross_sectional_returns/)
- [The Cross-Section of Volatility and Expected Returns (Ang, Hodrick, Xing & Zhang 2006)](replications/cross_section_of_volatility/)
- [The 52-Week High and Momentum Investing (George & Hwang 2004, Journal of Finance)](replications/the_52_week_high_and_momentum_investing/)
- [Amihud (2002), "Illiquidity and stock returns: cross-section and time-series effects"](replications/illiquidity_and_stock_returns/)
- [Piotroski (2000), "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers Among Value Stocks" (Journal of Accounting Research, Vol. 38)](replications/value_investing_f_score/)
- [Do Industries Explain Momentum? (Moskowitz & Grinblatt, 1999)](replications/do_industries_explain_momentum/)
- [Lakonishok, Shleifer & Vishny (1994) — "Contrarian Investment, Extrapolation, and Risk"](replications/contrarian_investment/)
- [Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency](replications/returns_to_buying_winners/)
- [The Cross-Section of Expected Stock Returns (Fama & French 1992, *Journal of Finance* 47(2))](replications/the_cross_section_of_expected_stock_returns/)
- [Earnings Releases, Anomalies, and the Behavior of Security Returns (Foster, Olsen & Shevlin 1984)](replications/earnings_releases_anomalies/)
<!-- END PAPER LIST -->
