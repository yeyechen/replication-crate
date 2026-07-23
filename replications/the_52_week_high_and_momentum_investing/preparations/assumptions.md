# Assumptions Registry — George & Hwang (2004), "The 52-Week High and Momentum Investing"

Paper-silent decisions (the paper does not specify these). Updated every inner iteration.
Paper-derived rules live in `preprocessing_rules.json` (with verbatim quotes).

> Note (outer iteration 2, M6): the derived coefficient caches cited as
> `data/fm_coefficients*.parquet` / `data/strategy_returns.parquet` in the
> iteration-1/2 entries below were relocated to `results/intermediate/`
> (validator-allowlist hygiene); all hashes unchanged. REPORT.md §6 has the
> current inventory.

---

## Assumption 1: Universe = common stocks (shrcd 10/11), all exchanges

**Decision:** Filter to securities with CRSP share codes 10 and 11 (ordinary common shares), point-in-time via `dsenames` (namedt ≤ month-end ≤ nameendt), with NO exchange-code filter.
**Rationale:** The paper says "We use all stocks on CRSP from 1963 to 2001" (§I, L73) and "The sample includes all stocks on CRSP" (Table I caption, L81) — taken literally this includes every CRSP security. "Stocks" is interpreted as common equity: shrcd 10/11 excludes closed-end funds, REITs, ADRs, units, and certificates, which are not "stocks" in the JT/MG tradition this paper follows ("collected exactly as described in MG"). No exchange filter is applied because the paper does not restrict to NYSE/AMEX/NASDAQ (unlike JT 1993), and MG (1999) — whose data procedure this paper adopts — used all CRSP stocks. Considered alternative: no shrcd filter at all (literal "all securities"); rejected because funds/REITs would enter momentum sorts and distort the EW portfolios.
**Impact:** Affects every cell in every table (universe is the foundation). Checked empirically: ~2,088 stocks/month in Jul 1963 growing to ~8,300 by 2001, consistent with "all CRSP common stocks" of that era.

## Assumption 2: Delisting treatment — dlret folded into HOLDING-period returns (ret_dl) — RATIFIED after inner-iteration-6 experiment

**Decision (supersedes the original no-adjustment default):** Official holding-period return column is `ret_dl`: for delisting events with valid dlret (non-NULL, > −1), the delisting month gets (1+ret)(1+dlret)−1 (1,214 existing rows adjusted) or, when no hygiene-clean panel row exists at the delisting month but the stock was an active holding at m−1, an added row with ret_dl = dlret (13,908 rows, ret = NaN so the plain-ret variant stays bit-identical). Signals, industry returns, rankings, and the FM R_{t-1} control stay on ORIGINAL ret — only portfolio/regression DEPENDENT variables use ret_dl. No Shumway/BMP imputation for the 524 NULL/worthless-dlret events (post-paper methodology).
**Rationale:** Paper silent. The experiment (results/delisting_experiment.md) ran all five tables under both variants; the pre-registered criterion (total Tier-1 hit rate) favors ret_dl 338 vs 332 of 516 (+6), with the JT-loser cell in Table I moving from 1.089 to 1.0504 against the paper's 1.05 (essentially exact) and the Table V wh_loser dummy moving toward the paper (−0.29 → −0.31 vs −0.48). Cost: mg_loser slightly worse (0.95 vs 1.03) and 2 extra FAILs inside the already-broken Table VII GH cells (the gh_loser sign anomaly proved NOT delisting-driven: +0.256 → +0.257). Net evidence favors adjustment; it is also the modern-standard treatment.
**Impact:** Loser-containing cells across all tables; full before/after in results/delisting_experiment.md.

## Assumption 3: Missing-return filter

**Decision:** Drop stock-months with missing `ret` (NULL) or CRSP missing-return sentinels (`ret <= -1` covers the -55/-66/-77/-88/-99 sentinels and true total-loss months are retained since they are > -1... correction: a true -100% loss has ret = -1.0 exactly; sentinels are < -1). Also require `prc` non-null with `abs(prc) > 0` for any price-based signal.
**Rationale:** Paper silent; standard CRSP hygiene. Sentinels like -99.0 would destroy compounding and EW averages if not removed.
**Impact:** All cells; small effect (few observations).

## Assumption 4: 52-week-high price = max of DAILY closing prices (wh_sig_dc) — LOCKED

**Decision (locked, inner iteration 3):** Primary signal: wh_sig_dc(f) = abs(prc_f) / max over months f-11..f of the max daily |close| (from dsf, aggregated to monthly max-close, rolling 12-month max). Variants tested and rejected, in ascending fit order: (1) max(msf.askhi) signed — contaminated: 20.3% of stock-months non-positive (CRSP quote-sign convention, pre-1983 NASDAQ); (2) wh_sig_hi_abs = |prc|/max(|askhi|) — loses to cl/dc on every Table I metric; (3) wh_sig_cl = |prc|/max(month-end |close|) — close second, marginally better on Table I alone (Σ|err| 0.118 vs 0.365, all Tier 1 either way) but materially worse on Table III (Σ|err| 26.29 vs 20.03; Tier-1 count 27 vs 30 of 48).
**Rationale:** Paper: "high_{i,t-1} is the highest price of stock i during the 12-month period that ends on the last day of month t-1" (L122). The max of daily closing prices is the most literal "price achieved during the period" series that is immune to the quote-sign artifact; it wins the pre-registered total-deviation criterion across all 52 cells (Table I 52WH + Table III): dc 20.39 vs cl 26.41 (−22.8%). A true intraday-high variant (max of daily askhi from dsf) was not tested — daily closes already dominate the monthly alternatives decisively.
**Impact:** Every cell involving the 52-week-high strategy (all tables).

## Assumption 5: Cumulative 6-month return compounds (JT and MG signals)

**Decision:** JT signal = Π_{s=f-5..f}(1 + ret_s) − 1 over the 6 months ending at formation month f; MG signal = Π(1 + industry VW return_s) − 1 over the same 6 months. Require all 6 months non-missing, else the signal is missing for that stock-month.
**Rationale:** JT (1993) — whose procedure this paper adopts — ranks on cumulative (compounded) 6-month returns. "Stocks are ranked based on their own individual returns over months t-6 to t-1" (L122) refers to the cumulative return over that window in the JT convention. Paper silent on minimum months; requiring all 6 is the conservative standard.
**Impact:** JT cells in all tables; MG cells in all tables.

## Assumption 6: MG 20-industry aggregation of 2-digit SIC — EXACT MG (1999) Table I mapping

**Decision:** Map the 2-digit SIC code (siccd // 100) into MG's 20 industries exactly as printed in Moskowitz & Grinblatt (1999) Table I: (1) Mining 10-14; (2) Food 20; (3) Apparel 22-23; (4) Paper 26; (5) Chemical 28; (6) Petroleum 29; (7) "Construction" 32 [MG's label for SIC 32, Stone/Clay/Glass]; (8) Prim. Metals 33; (9) Fab. Metals 34; (10) Machinery 35; (11) Electrical Eq. 36; (12) Transport Eq. 37; (13) Manufacturing 38-39; (14) Railroads 40; (15) Other Transport. 41-47; (16) Utilities 49; (17) Dept. Stores 53; (18) Retail 50-52, 54-59; (19) Financial 60-69; (20) Other — everything else (incl. 00-09, 15-19, 21, 24-25, 27, 30-31, 48, 70-99). SIC taken point-in-time from `dsenames.siccd` (fallback `msf.hsiccd`); MG note: "CRSP SIC codes, which allow for time-variation in industrial classification".
**Rationale:** George-Hwang say "Two-digit SIC codes are used to form the 20 industries shown in Table I of MG" (L73); the MG (1999) paper was retrieved and its Table I read verbatim, so this mapping is paper-grounded, not guessed. Note MG's idiosyncrasies: SIC 32 is labeled "Construction", Tobacco (21), Lumber (24-25), Printing (27), Rubber (30-31), Communications (48), and all Services (70-99) fall into "Other".
**Impact:** All MG-strategy cells (Tables I–IV MG rows; MG dummies in Tables V, VII).

## Assumption 7: Industry value-weighting uses lagged (end-of-prior-month) market cap

**Decision:** Monthly industry VW return = Σ_i ret_i × mcap_{i,f-1} / Σ_i mcap_{i,f-1} over industry members with non-missing ret and positive prior mcap.
**Rationale:** Paper: "a value-weighted average return is created for each of these industries" (L73) without specifying weights' timing. Lagged weights are the universal convention (avoid look-ahead) and match MG.
**Impact:** MG cells.

## Assumption 8: 30/30 sort cutoffs — percentile thresholds with deterministic ties

**Decision:** At each formation month, loser = signal ≤ 30th cross-sectional percentile, winner = signal ≥ 70th percentile (inclusive), middle = remainder. Ties broken deterministically by (signal value, permno) ordinal rank. MG ranking is by the stock's industry's cumulative return (many ties across stocks in one industry — ordinal ranks still split them 30/40/40... correction: 30/40/30 by count).
**Rationale:** Paper: top/bottom "30% of stocks" (L81, L120). Percentile-of-count with ordinal tie-breaking is the standard implementation; tie-handling is paper-silent.
**Impact:** All sort-based cells.

## Assumption 9: Regression units — R_t in percent, R_{t-1} in decimal, size = ln(market cap in dollars)

**Decision:** Fama-MacBeth regressions use dependent R_{i,t} in percent (ret×100), regressor R_{i,t-1} in decimal (ret), and size_{i,t-1} = ln(|prc_{t-1}| × shrout_{t-1} × 1000).
**Rationale:** Unit triangulation from reported coefficients: the R_{t-1} coefficient of ≈ −6.5 is only economically sensible with R_{t-1} in decimals (a 10% past-month return predicts −0.65%, the standard monthly-reversal magnitude); the size coefficient of ≈ −0.20 per log-unit is the standard size-effect slope (invariant to the dollar/million scaling); the intercept 3.62 then pins down ln(dollars) rather than ln(millions) (with ln(millions) the intercept would be ≈ 0.9). The paper says coefficients "are in percent per month" (L631).
**Impact:** All Table V/VII coefficient cells (intercept, R_{t-1}, size rows especially).

## Assumption 10: Risk adjustment = FF 3-factor (Mkt-RF, SMB, HML)

**Decision:** Risk-adjusted columns regress the monthly averaged coefficient series c_{kt} on contemporaneous `ff.three_factor` (mkt_rf, smb, hml, in percent) and report the intercept.
**Rationale:** Paper: "Our risk adjustment is equivalent to hedging out the strategy's Fama–French (1996) factor exposure" (L596). FF (1996) is the 3-factor model. Taken from `ff.four_factor_monthly` (month-end dates, decimals ×100 → percent; covers exactly the paper's 462 months 1963-07..2001-12). `ff.three_factor` is daily and is NOT used.
**Impact:** Risk-adjusted columns of Tables V and VII.

## Assumption 11: GH turnover from msf volume (×100 shares) and shares outstanding, capped at 1

**Decision:** V_f = min(1, msf.vol_f × 100 / (msf.shrout_f × 1000)). Reference price R_f = Σ_{s=1..60} w_s P_{f-s} / Σ w_s with w_s = V_{f-s} Π_{r=f-s+1..f}(1 − V_r) (equation 2, L1312), computed by recursion with a 60-lag window. g_f = (P_f − R_f)/P_f. Require 60 months of non-missing P and V; else g missing.
**Rationale:** Verified empirically that `msf.vol` in this CRSP vintage is in hundreds of shares (ratio to dsf share volume = 100.0 exactly). `shrout` is in thousands. Capping V at 1: turnover above 100%/month is a data error (negative weights would result otherwise); fraction of capped months is reported by the pipeline. Paper: "V_t is turnover in month t, defined as trading volume in shares divided by the number of shares outstanding" (L1315).
**Impact:** All GH cells (Table VII).

## Assumption 12: (6,6) overlapping portfolio return — equal weight across cohorts and across stocks

**Decision:** Month-t strategy return = (1/6) Σ_{f=t-6..t-1} R_f,t where R_f,t = equally weighted mean of month-t returns of stocks held in the cohort formed at f (survivors with non-missing ret_t). Stocks missing in month t drop out of that cohort's EW average for that month.
**Rationale:** Paper: "the equally weighted average of the month t returns from six separate winner portfolios, each formed in one of the 6 consecutive prior months t−6 to t−1" (L120). Missing-month handling is paper-silent; dropping (conditional EW) is the standard convention.
**Impact:** All of Tables I–IV.

## Assumption 13: Fama-MacBeth sample — stocks present in month t with non-missing R_t, R_{t-1}, size_{t-1}; strategy dummies default to 0 for stocks not rankable at formation t−j

**Decision:** Cross-section at (t, j) = stocks with non-missing ret_t, ret_{t-1}, mcap_{t-1}. Each strategy's winner/loser dummies are computed on the subset of stocks rankable on that strategy's signal at formation f = t−j (top/bottom 30%); a stock not rankable on a given strategy gets 0/0 dummies for that strategy (stays in the regression, counted in the intercept).
**Rationale:** Paper: dummies are "zero otherwise" (L570); whether un-rankable stocks stay in the cross-section is paper-silent. Keeping them matches the "all stocks in month t" cross-section reading and gives the intercept its documented meaning ("return to a neutral portfolio", L572). Sensitivity: if Table V misses, re-estimate restricting the sample to stocks rankable on all three signals.
**Impact:** All Table V/VII cells.

---

## Adjudication note (inner iteration 2): 52WH signal variant check executed

**Result (facts; the Replicator locks):** Table I's 52WH row was computed under (a) PRIMARY `wh_sig_cl` = |prc|/max(|prc|) and (b) VARIANT `wh_sig_hi_abs` = |prc|/max(|askhi|) (column added to the panel in this iteration):

| metric | paper | wh_sig_cl | err | wh_sig_hi_abs | err |
|---|---|---|---|---|---|
| winner | 1.51 | 1.5059 | -0.0041 | 1.4943 | -0.0157 |
| loser | 1.06 | 1.0790 | +0.0190 | 1.0895 | +0.0295 |
| W-L | 0.45 | 0.4269 | -0.0231 | 0.4048 | -0.0452 |
| t(W-L) | 2.00 | 1.9282 | -0.0718 | 1.6667 | -0.3333 |

|W-L error|: cl 0.0231pp vs hi_abs 0.0452pp; sum of |err| over all 4 metrics: cl 0.1179 vs hi_abs 0.4237. `wh_sig_cl` wins on every single metric. Recommendation to lock: **wh_sig_cl (PRIMARY)**, as anticipated in Assumption 4.

## Delisting-experiment note (Stage 7 experiment): Assumption 2 superseded by `ret_dl` (for the Replicator to ratify)

**Experiment (one committed change):** fold `msedelist.dlret` into the holding-period return series as a NEW panel column `ret_dl` (dependent variables of portfolios/FM regressions only; signals, industry returns, and rankings stay on original `ret`; no Shumway/BMP imputation). All 5 tables were run under BOTH `ret` and `ret_dl` (src/delisting_experiment.py → results/delisting_experiment.md).

**Rule:** event with valid dlret (non-NULL, > −1) → panel row at the delisting month: ret_dl = (1+ret)(1+dlret)−1 (1,214 rows); no panel row but the stock was an active holding at m−1 → ADD a row with ret=NaN (ret variant untouched) and ret_dl = (1+ret_msf)(1+dlret)−1 if a hygiene-clean msf return exists at m (536 rows), else dlret (13,372 rows). NULL/worthless dlret left as-is (524 events). In this vintage dsenames nameendt = dlstdt < month-end, so mid-month delistings fail universe coverage at the delisting month — the reason most final months were absent from the panel.

**Result:** total Tier 1 across Tables I+II+III+V+VII: ret 332 vs **ret_dl 338 (+6)**; FAIL 16 vs 18 (+2, both inside Table VII gh cells, whose sign anomaly is NOT delisting-driven: gh_loser s66_raw_janexcl moves +0.2555 → +0.2572). Diagnostic anchors: Table I jt_loser 1.0890 → 1.0504 (paper 1.05, |err| 0.039 → 0.0004); wh_loser (T V, s66_raw_janincl) −0.2873 → −0.3079 (paper −0.48, closer); Table I wh_loser 1.0850 → 1.0447 (paper 1.06, closer); Table I mg_loser 0.9771 → 0.9494 (paper 1.03, WORSE as anticipated). Pre-registered criterion: **adopt ret_dl** as the official holding-period return column. Official outputs were regenerated under ret_dl after the comparison was written. `ret` remains in the panel and every table machinery accepts RET_COL (default "ret").

## M2 experiment note (outer iteration 2): g_gh variant B adjudication — RUN; KEEP variant A (for the Replicator to ratify)

**Diagnosis:** the Table VII GH-dummy side is broken under variant A (strict-60-consecutive-month GH embedded gain, Assumption 11): 16 FAILs; gh_spread s66_raw_janexcl 0.0123 vs paper 0.44; gh_loser sign-flipped in 5 of 8 columns (+0.2572 vs −0.19). Variant A leaves 52.6% of stock-months null (1970s monthly-volume missingness ~40%), so the early-sample GH bins are a thin, unrepresentative subset. The paper's formula (2) writes 60 terms but never states a minimum-coverage rule — the strict-60 requirement was this replication's conservative default (log1.md iter 5 pre-registered this fix).

**Next fix (pre-registered log1.md iter 5, executed now):** g_gh variant B — reference price renormalized over AVAILABLE lags. For each (permno, f): candidate lags s = 1..min(60, L) with L = run length of consecutive non-null capped turnover V ending at f (same capped V series as A); a lag is usable iff P(f-s) is non-null (and its weight well-defined); require ≥ 24 usable lags, else NaN; w_s = V(f-s)·Π_{r=f-s+1..f}(1−V(r)) and R_f = Σ_{usable} w_s·P(f-s)/Σ_{usable} w_s exactly as in equation (2), summed over usable lags only. Additive panel column `g_gh_b` (g_gh untouched; rebuild guard passed — all 18 pre-existing columns bit-exact, deterministic rebuild, identical sha256 across runs). Table VII re-run under g_gh_b via src/m2_experiment.py → results/table_7_variantB.md (+ data/fm_coefficients_gh_variantB.parquet); official results/table_7.md and data/fm_coefficients_gh.parquet NOT overwritten — the Replicator ratifies adoption.

**Before metric (variant A):** g_gh null frac 0.526 (formation window; by decade 1960s 0.470 / 1970s 0.581 / 1980s 0.646 / 1990s 0.428 / 2000s 0.403); Table VII Tier 1 122 / Tier 2 102 / FAIL 16; gh_spread s66_raw_janexcl 0.0123 (t 0.15); gh_loser s66_raw_janexcl +0.2572 (t 3.42); gh_spread s66_ra_janexcl 0.0976 (t 1.31).

**After metric (variant B):** g_gh_b null frac 0.323 (by decade 0.218 / 0.484 / 0.403 / 0.207 / 0.177; +43% rankable stock-months; where A and B are both defined — 1,064,415 rows — values are bit-identical). Distribution (formation window): mean −0.393, p01 −5.14, p10 −1.11, p50 −0.093, p90 0.251, p99 0.472, std 1.588, min −233.44 (the SAME extreme observation as A's min; the left tail is NOT less extreme — p01 −5.14 vs A −4.42). Table VII under B: Tier 1 **118** / Tier 2 108 / FAIL **14**; gh_spread s66_raw_janexcl **0.1046** (t 1.22); gh_loser s66_raw_janexcl **+0.2126** (t 2.79 — still FAIL, sign not restored); gh_spread s66_ra_janexcl **0.2059** (t 2.64). Adoption criteria: (1) total Tier-1 118 < 122 → **FAIL**; (2) gh_spread anchor closer to paper (|B−0.44| 0.335 vs |A−0.44| 0.428) → **PASS**; (3) wh_spread 16/16 Tier 1 → **PASS**. Spec-flagged fact: the 16 wh_spread cells are NOT bit-identical A vs B (values shift ≤ 0.049, t-stats ≤ 0.42): the WH dummy matrix is identical, but the FM regression is joint (GH/GL dummies are extra regressors), so by Frisch-Waugh the WH coefficients shift when the GH columns change; all 16 stay Tier 1. Tables I and V re-run under the rebuilt panel and verified BIT-IDENTICAL (data/strategy_returns.parquet and data/fm_coefficients.parquet reproduce exactly in memory; neither table uses g_gh).

**Status:** **KEEP variant A** per the pre-committed rule (adopt B iff ALL three criteria hold; criterion 1 fails). B directionally improves every gh_spread cell toward the paper (all 8 columns move toward the paper value) and removes 2 of the 16 FAILs, but 4 Tier-1 cells (mostly GH t-stat cells) move to Tier 2, so the total Tier-1 criterion fails. `g_gh_b` stays in the panel as an additive diagnostic column; the official Table VII consumer remains on g_gh, and the GH-side anomaly stands documented as a 1970s-volume-missingness data-coverage limitation under either variant. Also added this iteration (audit M4 prep): `wh_lo_sig` = |prc(f)| / rolling 12-month min of daily min-close (≥ 1 by construction; null frac 0.0059, identical coverage to wh_sig_dc; src/sql/dsf_monthly_minclose.sql) — ready for the Table IX 52-week-low run.

## M1 corollary note (outer iteration 2): Table VI persistence of profits — RUN (for the Replicator to ratify)

**Diagnosis:** the paper's 3rd abstract claim — "future returns forecast using the 52-week high do not reverse in the long run" (Table VI, inputs/content.md:981-1005 + values L1007-1268) — had NO artifact and was never surfaced as a gap (audit1.md [M1]). The committed five-table scope froze it out even though `candidate_assessment.json` listed it.

**Next fix (executed now):** extend the shared FM engine `src/tables_5.py` ADDITIVELY with a persistence gap `k_offset` on `TableConfig` (formation `f = t − k_offset − j`; default 0 keeps the Table V/VII timing) plus a "wl" slot in `SPREAD_ORDER` (no effect on V/VII, which contain only wh/jt/mg/gh). New driver `src/tables_6_9.py::run_table_6` runs the (6,k,12) layout at k=12,24,36,48: same cross-sectional OLS as Table V (dependent `ret_dl`, R_{t-1}/size controls and 30/30 dummies from jt_sig/mg_sig/wh_sig_dc on the original signals), 12 lags j=2..13, c_{k,t}=mean_j, RISK-ADJUSTED-ONLY columns = intercept+t of c_{k,t} on contemporaneous FF3, Jan incl/excl → `results/table_6.md` (12 rows × 8 cols = 192 cells) + `data/fm_coefficients_persist.parquet`. Paper targets transcribed to `preparations/tables_to_replicate.json` (T6). Engine identity PROVED: re-running CFG_V and CFG_VII under `ret_dl` after the edit reproduces the official `data/fm_coefficients.parquet` (sha256 bf442e51…) and `data/fm_coefficients_gh.parquet` (sha256 ee066141…) byte-for-byte, and `table_5.md`/`table_7.md` unchanged.

**Before metric:** no artifact.

**After metric:** Table VI hit rate **Tier 1 73 / Tier 2 64 / FAIL 55 of 192**. The headline NON-reversal anchor reproduces well — 52WH spread by k (Jan-excl), ours vs paper: k12 **+0.1776 (t 2.39)** vs +0.16 (t 1.93); k24 +0.0813 (t 1.11) vs +0.08 (t 1.00); k36 +0.0645 (t 0.98) vs +0.04 (t 0.60); k48 +0.0868 (t 1.47) vs +0.07 (t 1.11) — stays small/positive, never reverses (the paper's central claim). The 8 wh_spread cells (Jan incl/excl) all land within ±0.05 of the paper (Jan-incl cells hover ~0 with tiny sign wobble, all insignificant). Reversal-pattern check (Jan-excl): jt_winner ours k12 −0.0675 (t −2.09, sign+sig match paper −0.18/−4.76) then decays to ≈0 at k=24/36/48 (paper stays −0.10..−0.13 significant); mg_winner ours stays POSITIVE (+0.05→+0.12) where the paper turns negative at k=12/24; wh_winner ours +0.14..+0.17 (significant) vs paper ≈0 — never negative in either, consistent with "no 52WH reversal".

**Status:** **PARTIAL** (documented, not looped). The 52-week-high non-reversal claim reproduces (wh_spread matches; wh dummies never reverse). The JT/MG momentum-reversal leg is attenuated in this vintage: the jt_winner reversal shows at k=12 but washes out by k=24, and mg_winner does not reverse — the same direction as the documented Table V offsets (JT/MG dummies run +28..+62% hot here, wh_loser ~0.64× paper; audit [M3]/[N2]), so stronger/over-persistent JT/MG momentum mechanically dampens the long-horizon reversal. No OCR skips (all 192 Table VI cells legible).

## M4 corollary note (outer iteration 2): Table IX 52-week low — RUN (for the Replicator to ratify)

**Diagnosis:** the paper's 52-week-LOW robustness corollary (Table IX, inputs/content.md:2173-2176 + values L2178-2444) — "a strategy based on the 52-week low is not profitable" — had NO artifact and was not surfaced as a gap (audit1.md [M4]). The required signal `wh_lo_sig` = |prc(f)| / rolling 12-month min of daily |close| (≥ 1) was already added to `data/panel.parquet` (null frac 0.0059, coverage identical to wh_sig_dc).

**Next fix (executed now):** run the EXACT Table V machinery via a new `TableConfig` (CFG_IX in `src/tables_6_9.py`) with strat_sig {"jt":jt_sig,"mg":mg_sig,"wl":wh_lo_sig} — FLH/FLL dummies (top 30% = farthest ABOVE the low = winners; bottom 30% = nearest the low = losers) replacing FHH/FHL, JT/MG identical to Table V. Both horizons (6,6)+(6,12), raw+RA, Jan incl/excl, dependent `ret_dl` → `results/table_9.md` (12 rows × 8 cols × 2 = 192 cells) + `data/fm_coefficients_low.parquet`. Paper targets transcribed to `preparations/tables_to_replicate.json` (T9). Official Table V artifacts untouched (engine identity as in M1).

**Before metric:** no artifact.

**After metric:** Table IX hit rate **Tier 1 126 / Tier 2 58 / FAIL 8 of 192**. Both of the paper's Table IX claims reproduce: (1) the 52-week-LOW spread is economically small and INSIGNIFICANT — wl_spread |t| < 1.96 in ALL 8 columns (s66 raw Jan-incl ours 0.1090 t 0.79 vs paper 0.13 t 0.95; Jan-excl −0.0283 t −0.20 vs 0.12 t 0.84; all 8 insignificant in ours and in the paper); (2) JT spreads become LARGER than in Table V — jt_spread s66_raw_janexcl ours 1.1106 (t 8.65) vs Table V ours 0.6449 (paper 0.46→1.05), and s66_raw_janincl ours 0.7093 vs Table V 0.5295 (paper 0.38→0.71). All 16 jt_spread/mg_spread cells are Tier 1 on value+t except mg_spread (Tier 2, +40..+90% hot — same MG offset as Table V). The 8 FAILs are the near-zero wl_spread cells (paper +0.01..+0.12, ours −0.07..+0.01) that flip SIGN on an economically-zero, insignificant spread — tiered FAIL by the sign-match rule only; magnitude is within ±0.08pp and both sides are insignificant.

**Status:** **DONE** — the corollary is evaluated and both qualitative claims hold. OCR: one correction, NOT a skip — size s612_raw_janincl t-stat OCR'd "(3.68)" transcribed as −3.68 (dropped minus; coefficient −0.17 is negative and Table V's analog is −4.27). No cells unreadable.

## M3 sensitivity note (outer iteration 2, inner 3): A13 rankable-only FM sample — RUN; KEEP official sample (for the Replicator to ratify)

**Diagnosis:** the paper's lead dominance cell inverts in the replication: Table V (6,6) raw Jan-included, paper WH 0.65 > JT 0.38 > MG 0.25 vs ours JT 0.5295 > WH 0.4896 > MG 0.3804 (same in (6,12) raw Jan-incl: JT 0.3295 > WH 0.3091). Two-sided cause: wh_loser dummy only ~0.64x paper (−0.3079 vs −0.48) while jt/mg spreads run +39%/+52%. A13 pre-registered the fix-on-miss sensitivity ("re-estimate restricting the sample to stocks rankable on all three signals"); Table V partially misses on wh_loser → executed now (audit1.md [M3]).

**Next fix (executed now):** re-estimated Table V (both horizons, all 8 columns, 12 rows) restricting EACH (t,j) cross-section to stocks rankable on jt_sig AND mg_sig AND wh_sig_dc SIMULTANEOUSLY at formation f = t−j, with the 30/30 dummies re-built on that common rankable cross-section (same ordinal convention), same controls (R_{t-1} on original ret, ln mcap), same ret_dl dependent, same j-averaging, Jan split and FF3 RA — everything else identical to CFG_V. Engine extended ADDITIVELY (build_rank_sets/rankable_only, run_horizon/sample_mat, rankable_by_decade/intersect_key; defaults off — regression gate PASS: official CFG_V re-run in memory reproduces data/fm_coefficients.parquet BIT-EXACTLY, sha256 bf442e51…). Outputs: results/table_5_sensitivity_rankable.md (full 12×8 restricted-sample grid + per-column official/rankable-only/paper anchor block + per-column dominance-ordering rows) + data/fm_coefficients_rankable.parquet. Official table_5.md / fm_coefficients.parquet NOT overwritten.

**Before metric (official sample):** avg cross-section n 4,803.6 per (t); s66_raw_janincl wh_spread 0.4896 (t 3.02), jt_spread 0.5295 (t 4.96) — ordering JT>WH>MG; wh_loser −0.3079 (t −2.92), wh_winner 0.1817, mg_spread 0.3804, intercept 4.6407 (t 5.34); s612_raw_janincl wh_spread 0.3091, jt_spread 0.3295 — JT>WH; Table V hit rate Tier 1 **150** / Tier 2 42 / FAIL 0 of 192.

**After metric (rankable-only sample):** avg RESTRICTED cross-section n **4,361.1** per (t,j) regression (s66 4,422.1 / s612 4,300.1; min 1,066, max 7,044; 90.8% of the official sample retained; all 2,772/5,544 regressions still fit). s66_raw_janincl wh_spread 0.4831 (t 3.00), jt_spread 0.5418 (t 4.94) — STILL JT>WH; wh_loser −0.2996 (t −2.78, moves AWAY from paper −0.48), wh_winner 0.1835, mg_spread 0.3830, intercept 4.8061 (t 5.58); s612_raw_janincl wh_spread 0.3078, jt_spread 0.3408 — STILL JT>WH. Dominance orderings: the restriction RESTORES nothing and additionally inverts s66_ra_janincl and s612_ra_janincl from WH>JT to JT>WH (6/8 columns match the paper's WH>JT>MG under both samples; the 2 raw Jan-incl columns stay JT>WH under both). Hit rate Tier 1 **144** / Tier 2 48 / FAIL 0 of 192 (−6). Adoption checks (adopt iff ALL hold): [C1] WH>JT restored in BOTH raw Jan-incl columns → **FAIL** (s66 0.4831<0.5418; s612 0.3078<0.3408); [C2] all 8 wh_spread cells stay Tier 1 → **PASS** (8/8); [C3] total Tier-1 does not degrade → **FAIL** (144 < 150).

**Status:** **KEEP the official sample** per the pre-registered rule (all three checks required). The rankable-only restriction barely moves the WH cells (wh_spread shifts ≤0.01), does NOT restore the paper's WH>JT ordering in either raw Jan-included column, inverts 2 more RA Jan-incl columns, and costs 6 Tier-1 cells at a 9.2% sample-size cost — the inversion is NOT an un-rankable-stock dilution artifact. Documented as an all-exchange/2026-vintage small-cap January effect (the joint JT/MG-loser hotness + WH-loser shortfall of N2/M3), now with the pre-registered sensitivity on record → reclassified NON-ACTIONABLE.

## M5 sensitivity note (outer iteration 2, inner 3): MG industry-level cutoff — RUN; KEEP official ordinal sort A8 (for the Replicator to ratify)

**Diagnosis:** MG spreads run +28%..+62% everywhere (Tier-1 by tolerance but the largest systematic offset; Table I mg_w_minus_l 0.5747 vs paper 0.45; FM mg_spread s66_raw_janincl 0.3804 vs 0.25). A8 ranks individual stocks by their industry's cumulative return with a permno-ordinal tie-break, arbitrarily splitting the boundary industry's stocks across winner/middle/loser; the MG-intended reading ranks the 20 INDUSTRIES (top/bottom 6). The tie-handling choice was never sensitivity-tested (audit1.md [M5]).

**Next fix (executed now):** industry-level MG variant implemented ADDITIVELY (tables_1_3.industry_cum_returns / industry_rank_groups / build_cohorts_industry for the Table I EW machinery; tables_5.build_rank_sets_industry for the FM dummies). At each formation f: the 20 industries' 6-month cumulative VW returns recomputed from the panel with the official A7 formula (lagged-mcap weights, 6 consecutive months), industries ranked (value desc, id asc tie-break), winner = stocks in the top-6 industries AT f, loser = bottom-6; boundary ties keep all members of tied industries (inclusive cutoffs). Same EW (6,6) machinery / Table V engine, dependent ret_dl; official defaults untouched (regression gates PASS: in-memory re-runs reproduce data/strategy_returns.parquet and data/fm_coefficients.parquet BIT-EXACTLY). Outputs: results/table_1_sensitivity_mg.md (Table I full grid under both variants + tie frequency + FM mg_spread all 8 columns + MG-weakest table + adoption checks) + data/fm_coefficients_mg_ind.parquet. Official table_1.md/table_5.md NOT overwritten. Note: the independent industry-cumret recompute differs from the official per-stock mg_sig by ≤1e-3 in 4.6% of (industry, month) cells — a switcher-membership artifact (stocks changing MG industry inside the 6-month window carry a mixed path in mg_sig); immaterial to the ranking of the 20 industries.

**Before metric (official ordinal 30/30):** Table I mg_winner 1.5240 / mg_loser 0.9494 / mg_w_minus_l 0.5747 (t 4.5364); |mg_w_minus_l − paper| = **0.1247**; FM mg_spread s66_raw_janincl 0.3804 (t 4.62; paper 0.25), s66_raw_janexcl 0.3573 (t 4.21; paper 0.22); MG weakest in 8/8 Table V columns; boundary-tie months n/a (ordinal split).

**After metric (industry-level top/bottom 6):** Table I mg_winner **1.5135** (closer to paper 1.48) / mg_loser **0.9181** (farther from paper 1.03) / mg_w_minus_l **0.5954** (t 4.5713); |mg_w_minus_l − paper| = **0.1454 — gap WIDENS**; FM mg_spread s66_raw_janincl **0.4098** (t 4.59), s66_raw_janexcl **0.3790** (t 4.09) — both farther from paper; MG weakest in **8/8** columns under the variant (PASS); industry-tie frequency **0** of 467 Table I formation months and 0 of 473 FM formation months (no exact ties at either boundary — the variant differs from the official ONLY through the whole-industry vs permno-ordinal cutoff); all 20 industries present every month (mean 20.0, min 20); variant cohort sizes avg W 1,421.9 / M 2,135.4 / L 1,255.8 (vs official forced 1,365/1,365); rankable-set overlap 94.6% (variant 4,813/mo vs official 4,552/mo). Adoption checks (adopt iff BOTH hold): [C1] MG gap shrinks → **FAIL** (0.1247 → 0.1454); [C2] MG weakest everywhere → **PASS**.

**Status:** **KEEP the official ordinal sort (A8)** per the pre-registered rule. The industry-level cutoff moves EVERY MG cell the WRONG way (W-L spread +3.6%, both FM spreads +6-8%) — the MG offset is NOT a tie-break artifact; with ties empirically absent, the residual is the SIC-vintage industry composition shift (panel_summary's Financial 1,294 vs MG ~891) plus the same vintage momentum hotness that drives the JT overshoot (M3/N2). Documented as non-actionable; the variant artifacts are kept as evidence.
