# Assumptions Registry — Cross-Section of Volatility (AHXZ 2006)

## Assumption 1: Delisting return treatment

**Decision:** Use CRSP delisting returns when available; for missing delisting returns, apply -30% for delisting codes 500-599 (delinquent/dropped) and 0% otherwise, following standard CRSP convention (Shumway & Warther 1999).
**Rationale:** Paper is silent on delisting treatment. The portfolio sorts are monthly, so delisted stocks must be handled. The -30% penalty for involuntary delistings is the conservative standard in the literature.
**Impact:** Affects portfolio returns for quintile 5 (high volatility stocks are more likely to delist), particularly in Table VI and Table VII.

## Assumption 2: No winsorization applied

**Decision:** Do not winsorize idiosyncratic volatility or total volatility before sorting.
**Rationale:** Paper is silent on winsorization. The paper sorts on volatility (always non-negative), and the quintile sort naturally handles outliers by placing them in Q5. Winsorizing would alter the composition of the extreme portfolio, which is the focus of the paper's anomaly.
**Impact:** Affects all tables. Q5 composition may include extreme outliers, which is the paper's intent.

## Assumption 3: Share code filter via dsenames PIT

**Decision:** Use point-in-time share code and exchange code from dsenames (shrcd IN (10,11), exchcd IN (1,2,3)) joined on (permno, date) with namedt <= date <= nameendt.
**Rationale:** Paper says "all stocks on AMEX, NASDAQ, and the NYSE" (L177). Standard CRSP convention is share codes 10 (ordinary common) and 11 (ordinary common). PIT join avoids survivorship bias from using header records.
**Impact:** Affects universe composition in all tables.

## Assumption 4: Market equity from CRSP

**Decision:** Compute market equity as ME = abs(prc) * shrout * 1000 from CRSP dsf (in dollars), or abs(prc) * shrout / 1000 (in millions).
**Rationale:** Standard convention per references/CRSP.md. CRSP prc is signed (negative for bid-ask average), shrout is in thousands. Paper reports "average log market capitalization" (L207) but does not specify the source.
**Impact:** Affects value-weighting in all portfolio sorts.

## Assumption 5: Book equity from Compustat (FF convention)

**Decision:** BE = CEQ + TXDB - PSTKRV when available; fallback to AT - DLC - DLTT - PSTKRV; require BE > 0. Map fiscal year t to months July t+1 through June t+2.
**Rationale:** Paper reports B/M ratios but does not specify the book equity formula. The Fama-French (1993) convention is the standard in the literature and the paper explicitly uses FF-3 factors.
**Impact:** Affects B/M characteristic reporting in Table VI and B/M control in Table VII.

## Assumption 6: FF factors are monthly, matched to daily regression

**Decision:** For the idiosyncratic volatility regression (equation 8), use daily excess stock returns regressed on daily FF factors. However, ff.three_factor in ClickHouse is monthly. Use monthly factors for the alpha computation (post-ranking), and for the daily IVOL regression, compute daily excess returns as ret - rf_monthly/21 (approximate daily rf).
**Rationale:** The paper says "computed using daily returns over the past month" (L1132) for IVOL. The FF factors table only has monthly data. For the daily regression, we need daily factor values. Since only monthly factors are available, we use the monthly factors divided by the number of trading days as an approximation for the daily regression, OR we compute IVOL as the standard deviation of daily excess returns after subtracting monthly factor loadings estimated from the same daily data.
**Impact:** This is a key implementation decision. The standard approach in the literature (and what AHXZ likely do) is to run the FF3 regression at the daily frequency using daily factor returns. Since we only have monthly FF factors, we will: (1) estimate factor loadings from daily data using monthly factors expanded to daily, or (2) use an alternative approach. This needs careful handling.

## Assumption 7: Tables I-V not replicated (no VIX data)

**Decision:** Tables I-V and Table IX require VIX/VXO index data which is not available in ClickHouse. These tables cover the systematic volatility risk analysis (β_ΔVIX sorts, FVIX construction, price of volatility risk). We replicate only the idiosyncratic volatility results (Tables VI, VII, VIII, X, XI).
**Rationale:** No VIX or VXO table exists in the ClickHouse catalog. The VIX data is from the CBOE and is not part of CRSP or Compustat.
**Impact:** The systematic volatility half of the paper is not replicated. The idiosyncratic volatility puzzle (the paper's most cited result) is fully targeted.

---

# Worker-verified data facts (Stage 7, verified live against ClickHouse)

⚠️ **These override earlier assumptions that were made without live DB access.**

## Verified Fact 1: FF factors are in DECIMAL, not percent (OVERRIDES task spec + A6)

Live query of `ff.three_factor` (1963-06 to 2000-12): `avg(mkt_rf)=0.00024`, `min(mkt_rf)=-0.1744` (Black Monday 1987-10-19), `max=0.0857`, `avg(rf)=0.00024`. `ff.four_factor_monthly`: `avg(mkt_rf)=0.00524`, `avg(rf)=0.00505`, `min=-0.2309`, `max=0.1603`.
**Conclusion:** BOTH `ff.three_factor` (DAILY, 26,110 rows) and `ff.four_factor_monthly` are in **DECIMAL** (e.g. 0.00524 = 0.524%/month). The task header statement "Values are in PERCENT (divide by 100)" is **incorrect** for this ClickHouse instance. **I do NOT divide by 100.** Dividing by 100 would zero out the factors and corrupt every regression.
**Note on IVOL robustness:** IVOL (std of FF3 residuals) is invariant to a constant rescaling of the regressors AND to subtracting a within-month-constant rf (intercept absorbs it), so IVOL is unaffected by this either way — but ret_excess and all alphas depend on getting the scale right. Scale is decimal.

## Verified Fact 2: ff.three_factor IS daily with a daily rf column (OVERRIDES A6)

`ff.three_factor` has columns (dt, mkt_rf, smb, hml, rf), 26,110 rows, DAILY from 1926-07-01 to 2025-10-31. A6's premise ("ff.three_factor in ClickHouse is monthly") is **false**. **I use the DAILY FF factors and the DAILY rf directly** for the daily IVOL regression — this is exactly the paper's methodology (daily FF3 regression on daily excess returns), no monthly/ndays approximation needed. Daily excess return = ret_d - rf_d (rf_d = ff.three_factor.rf, decimal).

## Verified Fact 3: CRSP dsf.vol is in SHARES (not thousands); task's VOLUME "*1000" is wrong

Sanity check: turnover = vol/(shrout*1000) gives median 0.25% (2000), 0.11% (1985), 0.05% (1970). For a sample stock (prc=0.75, shrout=14549 thousand=14.5M shares, vol=288700): turnover=1.98%, dollar volume=$0.216M = 1.98% × $11M mcap — internally consistent only if vol is in SHARES. **Dollar volume = abs(prc)×vol (dollars); in millions = abs(prc)×vol/1e6.** The task's "mean(abs(prc)×vol×1000)" would give $216M daily volume for an $11M-mcap stock (impossible), so the ×1000 is an error (it assumes vol is in thousands like shrout, but it is not). I compute volume in millions as mean(abs(prc)×vol)/1e6. Turnover = mean(vol/(shrout×1000)).
**Caveat flagged:** CRSP pre-1999 NYSE/AMEX volume may be in hundreds of shares (a known vendor inconsistency); the median-turnover-by-era pattern is consistent with this but I apply NO unit correction (rank-based sorts within a month are largely unaffected; the task does not request a correction). Flagging for the Replicator.

## Assumption 8: Panel timing convention — all variables contemporaneous at month t

**Decision:** Each panel row for month t stores ALL variables measured with data available at the END of month t: ret(t), ret_excess(t), me(t), size(t)=log(me_t), ivol(t)/tvol(t)/n_obs(t) from month-t daily data, volume(t)/turnover(t)/coskew(t) over month t, mom(t)=cumret(t-12..t-2), bm(t)/leverage(t) from Compustat FY (t-1 if month≥July else t-2). The task's "lagged 1 month for sorting" is handled by the ANALYSIS code (form on row-t signal, earn ret at t+1 via forward_returns/shift) — identical to the maxing_out_v2 convention.
**Rationale:** Self-consistent (no mixed timing), standard, matches the validated maxing_out_v2 pipeline. The task's inline "(t-1)" notations describe the effective lag once the analysis pairs row-t signals with row-(t+1) returns.
**Impact:** Analysis must lag signals by one month before pairing with returns (no look-ahead).

## Assumption 9: Panel starts June 1963 (first formation month)

**Decision:** Panel covers 1963-06 through 2000-12 (451 months). June 1963 is included as the FIRST formation month: its IVOL (from June daily data) drives the July 1963 portfolios, so the first realized portfolio return is July 1963 — matching the paper's "sample July 1963–December 2000" and the task's "need daily data starting June 1963 (to compute July IVOL)".
**Rationale:** A forward-return/shift analysis needs a signal month prior to the first return month. Starting the panel at July 1963 would lose July as a holding period.
**Impact:** First panel month is 1963-06; the first portfolio holding return is 1963-07.

## Assumption 10: IVOL = sample std of FF3 residuals (ddof=1)

**Decision:** IVOL = sqrt(SSE/(n-1)) where SSE is the residual sum of squares from the daily FF3 regression (intercept + MKT + SMB + HML) and n is the number of daily observations. Requires n ≥ 17.
**Rationale:** Task says "sqrt(var(epsilon_d)) — standard deviation of daily regression residuals"; sample std (ddof=1) is the pandas convention. (Regression standard error sqrt(SSE/(n-4)) differs by <~11% at n=17 and shrinks rapidly with n; flagged as an alternative.)
**Impact:** Minor scaling vs. sqrt(SSE/(n-4)); does not affect quintile ranking materially.

## Assumption 11: Compustat filter = indfmt='INDL', consol='C', popsrc='D', datafmt='STD'

**Decision:** Book equity and leverage use funda filtered to indfmt='INDL', consol='C', popsrc='D', datafmt='STD', deduplicated by (gvkey, fyear) keeping the most recent datadate. BE cascade: ceq+coalesce(txdb,0)-coalesce(pstkrv,0) if ceq present; else at-dlc-dltt-coalesce(pstkrv,0); else seq. BM = BE/ME_dec (FF June-rebalance mapping, no look-ahead); leverage = AT/BE.
**Rationale:** WRDS current standard (per references/COMPUSTAT.md); only 2 duplicate (gvkey,fyear) groups under this filter. FS-format-only financial firms get NULL bm/leverage (controls are optional; universe still includes them via CRSP shrcd/exchcd).
**Impact:** Financial firms with only FS-format records have missing bm/leverage.

## Assumption 12: Delisting return compounded into the LAST trading month

**Decision:** dlret_eff = dlret if valid (not NULL/sentinel < -0.40); else -0.30 if dlstcd∈[500,599]; else 0.0. The delisting return is compounded into the stock's LAST panel-month return (ret ← (1+ret)(1+dlret_eff)−1), for events whose dlstdt is 0-6 months after the last panel month.
**Rationale:** Task specifies the dlret_eff rule. Verified live: CRSP records dlstdt in the month AFTER the last trade for ~91% of events (gap distribution: 0 months=1,669, 1 month=12,417, >6 months=975 stale artifacts up to 222 months). Attaching to the last trading month (not dlstdt's month) captures 14,537 events (12,368 non-zero); attaching to dlstdt's month captured only 1,669.
**Impact:** Lowers final-month returns for delisted stocks (concentrated in high-volatility Q5) — materially affects the IVOL Q5 portfolio. Flagging the (small) risk that some vintages already embed dlret in msf.ret.

---

# Table VI analysis decisions (Stage 7, inner loop — analyze_table6.py)

### Iteration 1 — Problem: quintile mean returns sign-inverted and ~0.6%/mo too high
- Diagnosis: first run gave Q1→Q5 means 1.63→2.22% (Panel A), 5-1 = +0.59% — the OPPOSITE of the paper's decreasing pattern (-0.97%). Characterized before fixing: (a) lagged-weight all-stock VW return reproduced the FF market exactly (mean 1.04%/mo, corr 0.9999) so the panel returns are correct; (b) contemporaneous-weight VW was 1.68%/mo. The `attach_next_month_return` merge relabeled the return frame to month+1 then joined on the SAME month, so row t received ret(t-1), not ret(t+1) — sorting on signal_t and earning the PRIOR month's return (high-vol month t follows large month-(t-1) moves, producing the inverted slope and positive bias).
- Next fix: `analyze_table6.attach_next_month_return` — merge the panel row's holding month (month+1) onto the RAW return month, i.e. row (permno, t) gets the return realized in calendar month t+1. Added a sanity gate: all-stock VW(ret_next, me_t) must correlate >0.98 with the FF market in the holding month.
- Before metric: Panel A 5-1 mean = +0.59% (t=1.01); Q5 mean = +2.22%; alignment corr ≈ 0 (misaligned).
- After metric: Panel A 5-1 mean = -0.98% (t=-2.70) vs paper -0.97%; Q5 mean = +0.05% vs paper +0.09%; Panel B 5-1 = -1.02% (t=-2.95) vs paper -1.06%; alignment corr = 0.9999, mean VW = 1.04% = FF market.
- Status: resolved

## Assumption 14: Characteristic aggregation — simple cross-sectional means

**Decision:** Size and B/M in Table VI are time-series averages of the monthly cross-sectional SIMPLE (equal-weighted across firms) means within each quintile. B/M averages over firms with non-missing B/M; Size over firms with non-missing ME. Value-weighted alternatives are reported in the results-file notes for transparency.
**Rationale:** Paper says "Size reports the average log market capitalization for firms within the portfolio" and "B/M reports the average book-to-market ratio" (L207) — "for firms" reads as a plain firm average; weighting is not specified (paper silent). The task spec explicitly accepts either convention.
**Impact:** Affects only the Size/B/M columns of results/table_6.md (not returns or alphas). Simple means: Panel A Size Q1→Q5 = 4.67→2.58; VW means = 8.44→4.86. The task did not supply paper targets for these columns.

## Assumption 15: Newey–West lags = 4 for Table VI alpha and spread t-statistics

**Decision:** All CAPM/FF-3 alpha t-statistics and the 5-1 return-spread t-statistic use NW(1987) HAC with 4 lags.
**Rationale:** The paper says "Robust Newey–West (1987) t-statistics are reported in parentheses" (L207) without stating the lag count (paper silent on lags); the task spec fixes 4 lags.
**Impact:** t-statistics only; alpha point estimates unaffected.

## Assumption 16: % Mkt Share denominator = sorted-universe total ME

**Decision:** % Mkt Share for quintile q in month t = 100 × ΣME(q, t) / ΣME(all sorted stocks, t), where "sorted stocks" = stocks with a valid signal and ME that month; time-series averaged. Quintile shares sum to 100% each month.
**Rationale:** Paper says "percentage of total market capitalization" without specifying whether the denominator is the sorted sample or all CRSP stocks (paper silent). Using the sorted universe keeps shares summing to 100% across the five portfolios; fewer than 0.4% of stocks per month lack a signal, so the alternative denominator differs negligibly.
**Impact:** Affects only the % Mkt Share column.

## Assumption 13: Volume/turnover denominator = n_obs (sample days)

**Decision:** volume = sum(abs(prc)*vol)/1e6 / n_obs; turnover = sum(vol/(shrout*1000)) / n_obs — averaged over the same n_obs daily observations used for ivol/tvol/coskew (non-trading days count as zero volume/turnover).
**Rationale:** The task's "average daily dollar volume over the month" is ambiguous between (a) all sample days (n_obs, zeros included), (b) market trading days, (c) the stock's own trading days (vol>0). I use n_obs for consistency with the other daily signals. For liquid stocks (the large majority) all three coincide; only infrequently-traded stocks differ.
**Impact:** Minor; affects the level (hence quintile placement) of infrequently-traded stocks only.

---

# Tables VII & VIII analysis decisions (Stage 7, inner loop — analyze_tables_7_8.py)

## Assumption 17: Factor-alignment for post-ranking alphas — relabel returns to the HOLDING month (CRITICAL FIX)

**Decision:** Each formation-month-t portfolio earns its return in month t+1, so the return series (indexed by formation month t) is relabeled to the holding month (t+1) BEFORE regressing on the contemporaneous monthly FF factors. FF-3 alpha = intercept of (R − rf) ~ MKT-RF + SMB + HML, with a SINGLE rf subtraction (factor_alpha expects TOTAL returns and subtracts rf once).
**Rationale:** Without the relabel, each month's holding return is regressed on the PRIOR month's factors; for a diversified VW portfolio the lagged-factor betas collapse to ~0 (verified: baseline IVOL Q1 b_mkt = −0.01) and the "alpha" degenerates to ~the mean excess return (~+0.5%/mo too high for every cell). After relabeling, baseline IVOL Q1..Q5 alphas = −0.00, 0.08, 0.09, −0.29, −1.17 vs paper 0.04, 0.09, 0.08, −0.32, −1.27 (market betas ~1.0). This also explains the `analyze_table6.py` result: it passes EXCESS returns to `factor_alpha` (which subtracts rf again → a −mean(rf) ≈ −0.505%/mo shift); that double subtraction coincidentally compensated for the same off-by-one factor misalignment, so Table VI's alphas landed near the paper despite the two offsetting errors. Tables VII/VIII here use the CORRECT convention (relabel + single rf), which reproduces the baseline better than Table VI's convention.
**Impact:** All Table VII/VIII alphas. ⚠️ Flag for the Replicator: `analyze_table6.py`'s individual-quintile alphas carry the two offsetting errors; its 5-1 spread alphas are unaffected (rf cancels). If Table VI is revisited, applying this fix (relabel + single rf) gives baseline IVOL Q1..Q5 = −0.00/0.08/0.09/−0.29/−1.17 (closer to the paper than the current 0.02/0.14/0.18/−0.18/−1.10).

## Assumption 18: Momentum window timing (Table VIII) — as specified, window ends at t−1

**Decision:** Per the task spec, past-return signals relative to signal row t are past1 = ret_{t−1}, past6 = cumret(t−6..t−1), past12 = cumret(t−12..t−1) (i.e. the window ends at the month before the signal row, including the most recent completed month t−1 and NOT skipping it, unlike `mom` = cumret(t−12..t−2)). Computed via within-permno rolling on log returns, shifted one month; min_periods = window (full window required).
**Rationale:** Implemented exactly as specified. Empirically tested an alternative (window ending at t, i.e. past1=ret_t, past6=cumret(t−5..t), past12=cumret(t−11..t)): it matched the paper WORSE for past-6 (−1.39 vs paper −1.10) and past-1 (−1.25 vs −0.66), and only marginally better for past-12 (−1.20 vs −1.22; specified convention −1.06). The specified convention reproduces past-6 almost exactly (−1.13 vs −1.10).
**Impact:** (a) past-6 matches the paper; past-12 reasonable; past-1 is the weakest cell — the specified past-1 signal (ret_{t−1}) barely attenuates the IVOL Q5 alpha (5-1 = −1.15 vs paper −0.66), likely because the paper's 1-month reversal control is microstructure-sensitive (bid-ask bounce) and/or uses the formation-month return; flagging for the Replicator. (b) Momentum windows need lookback before the panel's 1963-06 start, so effective holding samples are shorter than July-1963: past-1 from ~1963-08 (449 mo), past-6 from ~1964-01 (444 mo), past-12 from ~1964-07 (438 mo). Data limitation (panel starts at the first IVOL formation month).

## Assumption 19: Double-sort breakpoints use ALL stocks (not NYSE-only)

**Decision:** For every Table VII/VIII dependent double sort, both the outer (control) and inner (IVOL) quintile breakpoints are the simple 20/40/60/80 percentiles of ALL stocks present that month (via utils.quantile.assign_quantiles / pd.qcut). The "NYSE Stocks Only" panel instead restricts the UNIVERSE to hexcd==1 and does a single IVOL sort (breakpoints then naturally NYSE).
**Rationale:** Task is silent on breakpoints for the control sorts; this matches the validated Table VI pipeline (all-stock breakpoints). NYSE-only breakpoints for the outer sort would be an alternative.
**Impact:** Portfolio composition; the resulting 5-1 spreads match the paper closely for size/leverage/volume/turnover/coskewness/momentum, supporting the choice.

## Assumption 20: Book-to-market control — level offset in Q1-Q4 alphas (flagged)

**Decision:** B/M control uses the pipeline's bm = BE/ME_dec (FF convention; 23% of rows have missing bm → ~3,652 stocks/month). Implemented as a standard dependent double sort.
**Rationale / finding:** The B/M 5-1 spread matches the paper (−0.91 vs −0.80), but the Q1-Q4 LEVEL alphas are ~0.6-0.75 lower than the paper's (rep Q1..Q4 ≈ −0.02..0.02 vs paper 0.61..0.50). The offset is a near-constant level shift across quintiles, pointing to a systematic difference in the B/M-matched sample's average returns (Compustat book-equity construction / coverage) rather than a sort error (the spread is correct). Flagging for the Replicator — the headline result (IVOL anomaly survives B/M control) is reproduced via the 5-1 spread.
**Impact:** Table VII "Controlling for B/M" Q1-Q4 point estimates; 5-1 spread is reliable.

---

# Tables X/XI analysis decisions (Stage 7, inner loop — analyze_tables_10_11.py)

## Assumption 17: L/M/N timing — 1/1/1 = signal lagged by 2 months

**Decision:** 1/1/1 is implemented from the existing L=1 panel by pairing the signal at month m with the calendar return realized in month m+2 (formation at end of month m+1 uses IVOL from month-(m+1-M)=m daily data, skips month m+1, holds month m+2). 1/1/12, 12/1/1, 12/1/12 are NOT implemented — they require IVOL recomputed from 12 months of daily data (L=12), which the panel does not store; documented as a limitation in results/table_10.md with the paper values.
**Rationale:** Task spec: "Sort on IVOL_{t-1}, earn return_{t+1} (lag the signal by 2 instead of 1)". Follows directly from the paper's L/M/N definition (preprocessing rule lmn_strategy, L1132: IVOL over the L-month period from t-L-M to t-M, hold N months after skip M).
**Impact:** Table X 1/1/1: Q5 α = -0.66 vs paper -0.82 (-19.5%); 5-1 α = -0.68 vs -0.88 (-22.7%), both within 30% tolerance. Other three strategies unreplicable from the current panel.

## Assumption 18: factor_alpha subtracts rf internally — pass TOTAL returns

**Decision:** In the alpha regressions for Tables X/XI, the portfolio series passed to `utils.regressions.factor_alpha` is the VW TOTAL return (not pre-subtracted excess return). factor_alpha computes y = ret − rf_col internally (utils/regressions.py: `y = merged["__ret"] - merged[rf_col]`); passing ret − rf would double-subtract rf (~−0.50%/month shift on every alpha, since mean rf = 0.505%/month 1963-2000). The 5-1 spread is passed with rf_col zeroed (zero-investment).
**Rationale:** Verified empirically: double subtraction gave full-sample alphas Q1 = −0.51 (t = −10.2), Q5 = −1.68; after the fix Q1 = −0.00, Q2 = 0.08, Q3 = 0.09, Q4 = −0.29, Q5 = −1.17, 5-1 = −1.17 — matching the paper's Table VI Panel B alphas (0.04, 0.09, 0.08, −0.32, −1.27, −1.31) far better than analyze_table6.py's values (which pre-subtracted rf AND regressed holding-month returns on formation-month factors; the two offsets partially offset for level alphas there). Portfolio returns at holding month t are regressed on the factors of the SAME month t.
**Impact:** All Table X/XI alphas. ⚠️ Note: analyze_table6.py (Table VI) contains the double-rf + factor-month-misalignment pattern; its Q1–Q4 alphas happen to land near the paper because the two offsets partially cancel. Flagged for the Replicator; not modified here (out of task scope).

## Assumption 19: Table XI subsample membership defined on the HOLDING month

**Decision:** Subsample membership (decades, NBER cycles, stable/volatile) is determined by the holding month (the month the portfolio return is realized), not the formation month. Quintile portfolios are formed each month on the full cross-section; subsamples split the resulting monthly VW return time series. NBER recession months are inclusive of peak and trough (62 recession months in-sample; the 2001-03–2001-11 recession contributes 0 months since the sample ends 2000-12; 388 expansion months). Stable/volatile: in-sample holding months with |mkt_rf| ≤ 20th pctile (1.126%) / ≥ 80th pctile (5.050%), 90 months each, thresholds computed over Jul 1963–Dec 2000 holding months from ff.four_factor_monthly (decimal).
**Rationale:** Paper frames Table XI as robustness of the portfolio return series over subperiods (paper silent on formation-vs-holding membership; the holding-month convention is standard). Task spec: "compute |MKT|RF| for each month, classify bottom 20% as stable, top 20% as volatile" — applied to holding months in the sample.
**Impact:** Subsample alphas. All cells within 30% of the paper except "Volatile periods" (Q5 α = −0.48 vs −0.93, +48%; 5-1 = −0.24 vs −0.89, +73%, t = −0.41). All other subsamples: ≤ 20% deviation (best: 1981–1990 Q5 −2.01 vs −2.08, 3.4%).

---

# Table X L/M/N completion — Issue M2 (analyze_table10_lmn.py, src/sql/ivol12_stats.sql)

## Assumption 21: 12-month IVOL via rolling sum of monthly sufficient statistics (SQL-first)

**Diagnosis:** Audit M2 — three of four Table X strategies (1/1/12, 12/1/1, 12/1/12) were uncomputed because the panel stores only L=1 IVOL. The 12/1/1 and 12/1/12 strategies need IVOL computed from 12 months of daily data (L=12).
**Next fix:** Compute IVOL_12 WITHOUT re-pulling the ~50M daily rows into Python. The per-(permno, month) FF3 sufficient statistics in daily_stats.sql (X'X, X'y, y'y, n) are ADDITIVE across days, so summing them over a 12-calendar-month window yields the exact normal equations of the POOLED daily regression over that window. Implemented in `src/sql/ivol12_stats.sql`: the same universe_daily/monthly aggregation as daily_stats.sql feeds a `RANGE BETWEEN 11 PRECEDING AND CURRENT ROW` window (PARTITION BY permno, ORDER BY month_idx = year*12+month). month_idx is a continuous integer, so the RANGE offset is calendar-correct and missing months contribute nothing (no rows) — exactly the trailing 12 calendar months [s-11, s]. Python (`analyze_table10_lmn.solve_ivol12`) solves the 4×4 normal equations in closed form and returns IVOL_12 = sqrt(SSE/(n-1)) (ddof=1, mirrors main.compute_daily_signals / A10). Cached at data/ivol12.parquet.
**Before metric:** table_10.md listed 1/1/12, 12/1/1, 12/1/12 as "requires recomputing IVOL from multi-month daily data" (not computed).
**After metric:** IVOL_12 VERIFIED to match a direct pooled daily FF3 regression to machine precision (permno 10000, 1987-01: 0.046492393 both ways, n=252). All three strategies now computed. 5-1 FF-3 α (ours vs paper): 1/1/12 = −0.61 vs −0.67 (9% dev); 12/1/1 = −0.82 vs −1.12 (27% dev); 12/1/12 = −0.65 vs −0.77 (15% dev) — all within the audit's ~30% band. Q5 α: −0.60/−0.80/−0.65 vs paper −0.64/−1.08/−0.73.
**Status:** resolved.

## Assumption 22: L/M/N portfolio construction — formation weight = ME at signal month; overlapping cohorts simple-averaged; holdable filter

**Decision:** For an L/M/N strategy with signal at month s: sort into quintiles on the signal (all stocks with valid signal + ME), formation weight = market equity me(s) (same convention as the validated 1/0/1 and 1/1/1 code). A cohort formed at s is held over calendar months s+M+1 .. s+M+N (skip M, hold N). For N=12, the quintile return in each holding month is the SIMPLE average of the (up to) 12 active cohorts' value-weighted returns — Jegadeesh-Titman overlapping, each cohort value-weighted at its own formation (paper §II.A.2 / L1134). Weights are fixed at formation and renormalised each holding month over stocks with a non-missing return (delisted stocks drop out after their delisting-adjusted final-month return, A12). Stocks enter the sort only if they have a return in at least one holding month of the window; for N=1 this reproduces the validated Table X 1/1/1 EXACTLY (Q5 = −0.66, 5-1 = −0.68).
**Rationale:** Paper L1134: "we form a value-weighted portfolio based on 12 months of returns ending 1 month prior … 2 months prior … up to 12 months prior … take the simple average of these 12 portfolios. Hence, each quintile portfolio changes 1/12th of its composition each month." The signal-month-ME convention matches the already-validated pipeline.
**Impact:** All four strategies computed with one unified function. Market betas ≈ 1 for every strategy (quintile-avg b_mkt = 1.09/1.10/1.13/1.14), confirming correct holding-month factor alignment (audit-M1 convention). The 1/1/1 row is unchanged from the validated value (internal consistency between this table and analyze_tables_10_11.py preserved).

## Assumption 23: L=12 minimum-observation threshold = 120 daily obs (paper silent)

**Decision:** Require n_obs_12 >= 120 daily observations in the trailing 12-month window (~10/month) for a valid IVOL_12.
**Rationale:** The paper requires "more than 17 daily observations" for the L=1 (1-month) regression (L177) but is SILENT on the L=12 threshold. Two candidates: (a) 17×12 = 204 (17/month, the literal extension); (b) 120 (a reasonable fraction, per the task spec). Tested both: 204 keeps 1,986,892 (permno,month) rows, 120 keeps 2,073,445. Empirically 120 reproduces the paper BETTER for the L=12 strategies (12/1/1 5-1: −0.82 vs −0.78 with 204; 12/1/12: −0.65 vs −0.61). 120 is used.
**Impact:** ~4% more (small/new) stocks included under 120 vs 204. The L=12 spreads move slightly toward the paper under 120. Flagged for the Replicator: the threshold is a paper-silent choice; 204 (the literal 17/month rule) is the more conservative alternative and keeps all spreads within the ~30% band too.

---

# Outer iteration 2 fixes (auditor issues M1, M3, M4)

### Issue M1 — Table VI FF-3 alphas: two offsetting bugs (double rf + factor-month misalignment)
- Diagnosis: `analyze_table6.quintile_time_series` had two offsetting errors. (1) It computed excess returns `exc = r − rf` and passed them to `factor_alpha`, which subtracts rf AGAIN internally (utils/regressions.py: `y = ret − rf_col`) — a double rf subtraction shifting every alpha down by ~mean rf ≈ −0.50%/month. (2) The VW return series was indexed by the FORMATION month t (the return realized in month t+1) but regressed on the formation-month factors `ff.loc[r.index]` — it should be regressed on the HOLDING-month factors. For a diversified VW portfolio the lagged-factor beta collapses to ~0, so the "alpha" degenerated toward the mean excess return. The two errors partially canceled, so level alphas landed near the paper while market betas were ~0 (should be ~1). The correct convention was already in `analyze_tables_10_11.py`.
- Next fix: In `quintile_time_series`, relabel each quintile return series from formation month t to HOLDING month t+1 (`r.index += 1 month`) and pass the TOTAL return to `factor_alpha` (single rf subtraction, factors aligned to the holding month). Added `CAPM_beta` output and a sanity gate: every quintile beta > 0.5 (not ~0) and the market-cap-weighted average market beta across quintiles ≈ 1.0 (±0.3).
- Before metric: Panel B IVOL FF-3 α Q1..Q5 = 0.02, 0.14, 0.18, −0.18, −1.10; 5-1 = −1.12. Market betas ~0 (Q1 b_mkt ≈ −0.01). Panel A 5-1 FF-3 = −1.05.
- After metric: Panel B IVOL FF-3 α Q1..Q5 = −0.00, 0.08, 0.09, −0.29, −1.17; 5-1 = −1.17 (paper 0.04, 0.09, 0.08, −0.32, −1.27, −1.31). Market betas Q1..Q5 = 0.83, 1.05, 1.26, 1.43, 1.45 (mkt-cap-wtd avg = 0.98). Panel A FF-3 Q1..Q5 = −0.02, 0.06, 0.12, −0.12, −1.09; 5-1 = −1.05 (paper 5-1 −1.19); betas 0.76..1.51 (wtd avg 0.96). CAPM 5-1 Panel B = −1.35 (paper −1.38). The corrected Panel B full-sample 5-1 (−1.17) matches table_11.md's 1/0/1 value (−1.17) exactly (reconciliation check passed).
- Status: resolved (matches expected corrected values from analyze_tables_10_11.py; betas ~1, sanity gate passed).

### Issue M3 — Table VIII past-1-month momentum control (formation-month return)
- Diagnosis: The past-1-month control used `past1 = ret_{t-1}` (the month BEFORE the formation month) and gave 5-1 = −1.15 vs paper −0.66 (barely attenuated the IVOL effect; paper: −1.31 → −0.66). Hypothesis (Replicator): the paper's "past 1-month return" at portfolio formation (END of month t) naturally includes the FORMATION-month return ret_t (the same month the IVOL signal is measured from). Cross-sectionally, IVOL correlates more positively with ret_t (+0.15) than with ret_{t-1} (−0.06), consistent with the paper's "high-IVOL = recent winners" reversal logic.
- Next fix: In `compute_momentum`, changed `past1` from `ret.shift(1)` (ret_{t-1}) to `ret` (the formation-month return ret_t). past6/past12 unchanged (cumret ending at t-1; per A18 these match the paper's past-6 −1.10 and past-12 best). Regenerated table_8.md.
- Before metric: Past 1 month 5-1 α = −1.15 (Q1..Q5 = 0.03, 0.04, −0.06, −0.35, −1.11); paper 5-1 = −0.66 (Q5 −0.59).
- After metric: Past 1 month 5-1 α = −1.25 (Q1..Q5 = 0.11, 0.06, −0.01, −0.20, −1.15); paper 5-1 = −0.66. ⚠️ The formation-month convention did NOT move the 5-1 toward the paper (−1.25 vs −1.15 for ret_{t-1}; it moved slightly AWAY). Neither convention reproduces the paper's strong attenuation (−1.31 → −0.66). (Consistent with A18's earlier test of a window ending at t, which also gave −1.25.)
- Status: implemented as specified (past1 = ret_t, the formation-month convention), but the hypothesis is NOT supported by the data — the 5-1 moved away from the paper. Flagged for the Replicator: decide whether to keep ret_t (the economically "correct" formation-month convention) or revert to ret_{t-1} (−1.15, marginally closer to −0.66). Table VII unaffected (does not use past1).

### Issue M4 — Table XI volatile-period subsample (stable/volatile classification month)
- Diagnosis: The volatile-period subsample gave 5-1 = −0.24 (t = −0.41) vs paper −0.89. Verified the HOLDING-month classification: bottom/top 20% of |mkt_rf| over the 450 in-sample holding months = exactly 90 stable + 90 volatile months (450 × 0.20; thresholds 20th pctile = 1.126%, 80th = 5.050%), matching the paper's L2074 wording. Tested the alternative: classify on the FORMATION month's |mkt_rf| (holding − 1), mapped forward to holding months.
- Next fix: Kept the holding-month classification as PRIMARY (paper convention: classify the months of the return series, which is indexed by the holding month; it also reproduces the paper's stable ≪ volatile contrast and matches the stable period well). Added the formation-month classification as a documented sensitivity via `stable_volatile_sets(ff, classify_on=...)`, reported in a new table_11.md section.
- Before metric: Volatile 5-1 = −0.24 (t = −0.41, Q5 = −0.48); Stable 5-1 = −1.95 (Q5 = −1.80).
- After metric: Primary (holding month, unchanged): Volatile 5-1 = −0.24 (paper −0.89), Stable 5-1 = −1.95 (paper −1.71, within ~14%). Sensitivity (formation month): Volatile 5-1 = −1.21 (t = −1.98; closer to paper) but Stable 5-1 = −1.21 (t = −3.41; now attenuated vs paper −1.71), and stable ≈ volatile — destroying the paper's stable-vs-volatile contrast (paper stable −1.71 vs volatile −0.89).
- Status: investigated; the holding-month convention is retained as primary. The volatile-period 5-1 is attenuated under BOTH conventions and is highly sensitive to the exact 90-month set — a small-sample limitation, now documented in table_11.md and flagged for the Replicator.
