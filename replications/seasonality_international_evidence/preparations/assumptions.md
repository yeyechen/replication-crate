# Assumptions Registry — seasonality_international_evidence

Paper-silent decisions for the replication of Heston & Sadka (2010, JFQA),
"Seasonality in the Cross Section of Stock Returns: The International Evidence".
Updated every inner-loop iteration.

---

# Assumption 1: Data source substitution (Compustat Global + NA for FactSet)

**Decision:** Build the international equity panel from Compustat Global daily
(`comp_202601.g_secd`) for the 13 non-Canada countries (classified by
`g_company.loc`), and from Compustat North America daily
(`comp_202601.secd`, `security.excntry='CAN'`) for Canada. Convert everything
to USD with `comp_202601.g_exrt_dly` GBP-base cross rates.
**Rationale:** The paper's FactSet monthly file is proprietary and not present
in the data catalog. Verified alternatives: WRDS Datastream in
`tr_ds_equities_202303` contains only index-level series (`wrds_ds_indexmerged`
= 4,073 indices, none joinable to equity names); TRTH (`tr_common.prcisr`) is a
13k-row instrument code table with no price series; Compustat Global monthly
(`g_secm`) starts 2007-01-31 (zero overlap with the 1985–2006 sample). Compustat
Global *daily* covers 1913–2026 and was verified live to carry 2,460 firms in
1985 → ~9,800 in 2005 across the 13 countries (paper: 18,117 unique firms,
~9,500 firm-months/month pooled); Compustat NA carries 448 Canadian firms in
1985 → 3,472 in 2005 (paper: 2,714 total).
**Impact:** Affects every cell. Absolute firm counts (Table 1) cannot match
exactly — evaluated at Tier 2 (pattern level). Returns/spreads (Tables 2, 3, 7)
are targeted at Tier 1; the large-cap tilt of Compustat vs FactSet's broader
coverage may compress spread magnitudes, which would be logged as Tier 2 with
this justification.

# Assumption 2: Primary-issue universe, no security-type filter

**Decision:** One security per firm: the primary issue (`g_security.iid =
g_company.prirow`) for global firms; all issues with `excntry='CAN'` for
Canada. No `tpci`/share-code or financial-firm exclusion.
**Rationale:** Paper silent — it describes the sample simply as "stocks"
(L39) with no share-code or industry filter. The primary-issue convention
avoids double-counting cross-listings (e.g., gvkey 001166 has simultaneous
NLD/DEU/GBR/MEX listings in `g_security`). Delisted firms remain in both
security masters, matching the paper's survivorship-free claim (L39).
**Impact:** Universe size and composition for all tables.

# Assumption 3: Monthly aggregation from daily prices

**Decision:** Monthly price = price on the last trading day of the calendar
month (max `datadate` within month, per security). Monthly local return
r = (prccd_t/ajexdi_t)/(prccd_{t-1}/ajexdi_{t-1}) − 1; missing if either
month-end price is absent. Panel starts 1979-12 (month-end) so that the
lag-60 signal and regression for the first reported month (February 1985)
are available.
**Rationale:** The paper uses monthly returns (L39) and the source is daily
prices; last-trading-day month-end is the standard convention. The
`prccd/ajexdi` adjustment was verified empirically: NTT (gvkey 007908) shows
ajexdi = 1 → 10,200 over history (splits/dividends accumulate in ajexdi),
and its implied market cap at 2000-06-30 (prccd × cshoc × FX) is $211bn,
matching NTT's actual ~$210bn — confirming both the adjustment direction
and that `cshoc` is in actual shares with no `qunit` rescaling needed.
**Impact:** Every return series (Tables 2, 3, 7).

# Assumption 4: USD conversion via GBP-base cross rates

**Decision:** g_exrt_dly stores rates as units of currency X per 1 GBP
(fromcurd='GBP'). Define USD-per-unit-X = rate(GBP→USD)/rate(GBP→X) — units:
(USD/GBP)/(X/GBP) = USD/X; the fraction is inverted relative to the stored
quotes (the worker's F1 finding, verified against the NTT $211bn and
JPY/USD=107 anchors). GBP cancels in month-over-month FX ratios. Month-end
FX = last available rate on or before month-end, carried forward. USD return
= (1 + r_local) × (USDperX_t / USDperX_{t-1, own prior currency}) − 1, where
the t-1 rate uses the security's own prior-month curcdd so the 1999 euro
redenomination cancels exactly (prccd redenominates, ajexdi does not — see
F2). Market cap me_usd = prccd × cshoc × USDperX.
**Rationale:** Verified live: GBP→X daily series exist for every currency
appearing in the 1985–2006 universe (ATS, BEF, CAD, CHF, DEM, ESP, EUR, FIM,
FRF, ITL, JPY, NLG, NOK, SEK, USD, CZK, EGP, ILS, XEU), each covering
1984-12-03 through 2006-06-30. Spot check: rate(GBP→USD)/rate(GBP→JPY) =
1.618/173.4 = 0.00933 USD/JPY (i.e. 107.2 JPY/USD) in early 2000, matching
actuals (~105–107). Eurozone Jan-1999 ret_usd shows no spurious drop (min
-0.47, mean -0.032).
**Impact:** All USD-denominated returns and market caps.

# Assumption 5: Arithmetic (not ratio) country-excess returns

**Decision:** Intracountry return = r_i,usd − rbar_c,usd (arithmetic
difference from the equal-weighted country-month mean return); intercountry
component = rbar_c,usd. Sort signals are averages of these monthly arithmetic
excesses over the strategy's lag set.
**Rationale:** Table 3's columns satisfy Total = Intra + Inter exactly as an
arithmetic sum (e.g., Y1 nonannual EW Panel A: 0.0121 = 0.0117 + 0.0004,
L265-272), which pins the convention to arithmetic differences. The paper
also notes excess-return results are numeraire-robust (L49), consistent with
first-order arithmetic excesses on USD returns.
**Impact:** Table 3 Panels A/B, all intra/inter cells, Table 7, and every
sort signal.

# Assumption 6: Strategy lag sets

**Decision:** Year 1: annual = {12}, nonannual = {1..11}, all = {1..12}.
Years 2–3: annual = {24, 36}, nonannual = {13..23, 25..35}, all = {13..36}.
Years 4–5: annual = {48, 60}, nonannual = {37..47, 49..59}, all = {37..60}.
Signals = average monthly excess (Panel A) or total (Panel B) return over the
lag set. Difference strategy = annual − nonannual spread return.
**Rationale:** Paper L210: annual = lags that are multiples of 12 ("Year 1
annual strategies represent decile portfolios sorted on a single lag
12-month return"; "Year 1 nonannual strategies choose stocks based on the
most recent 11 months"); L234: Years 4–5 annual "ranks stocks according to
their average returns during the historical lags 48 and 60"; L210 "All" =
"all 12 of the past Year 1 returns".
**Impact:** Every Table 3 and Table 7 strategy cell.

# Assumption 7: Equal-count pooled deciles, monthly rebalancing

**Decision:** Each month t ∈ [1985-02, 2006-06], rank all stocks with
non-missing signal and non-missing holding return; assign ascending ranks to
10 consecutive groups of as-equal size as possible (top decile = highest
signal). Spread = mean month-t USD return of decile 10 minus decile 1 (EW);
VW weights = prior month-end me_usd within each decile. Rebalance monthly,
1-month holding.
**Rationale:** L234 "10 portfolios (with equal number of stocks in each
portfolio)"; L206 "rebalance these portfolios monthly ... holding period of
1 month". No NYSE-style breakpoints — the paper sorts the full pooled
cross-section.
**Impact:** All Table 3/7 spreads.

# Assumption 8: WLS weights = reciprocal of pooled country variance

**Decision:** Heteroskedasticity-adjusted Table 2 regressions weight every
firm observation in country c by 1/σ²_c, where σ²_c is the pooled
cross-sectional-and-time-series variance of that country's firm returns over
the full sample. Reported for All-countries and Europe samples only.
**Rationale:** L112: "we estimate return responses with a weighted least
squares regression (1), determining weights by the (reciprocal) of estimated
variances in each country" (L122's wording is loose; L112 is the methodology
statement and a WLS weight must be inverse-variance to downweight volatile
countries — the stated purpose).
**Impact:** Table 2 WLS columns (All, Europe).

# Assumption 9: No winsorization

**Decision:** No trimming/winsorization of returns or signals.
**Rationale:** Paper silent — no mention anywhere (logged also in
preprocessing_rules.json#winsorize_none_paper_silent).
**Impact:** All tables.

# Assumption 10: Missing shares outstanding carried forward

**Decision:** When `cshoc` is NULL on a month-end day, carry the last
non-missing value within the security; drop the observation only if the
security never has a shares value.
**Rationale:** Paper silent; Compustat frequently leaves cshoc blank between
reporting dates. Carry-forward is the standard convention and only affects
value-weighting (Table 3 VW panel), not EW results.
**Impact:** Table 3 VW panel, size diagnostics.

---

## rep-worker findings — inner iteration 1 (panel build, appended)

# Finding F1: FX fraction in the spawn prompt was inverted (resolved)

The task prompt wrote `usd_per_x = rate(GBP->X) / rate(GBP->USD)`, but that
fraction equals *X per USD* (units of X per dollar), not USD per X. The verified
anchors pin the opposite direction: log1.md states
`me_usd = prccd × cshoc × rate(GBP→USD)/rate(GBP→cur)`, and NTT (gvkey 007908)
me_usd @ 2000-06-30 must be ~2.1e11 USD, which requires multiplying by
USD/JPY = rate(GBP→USD)/rate(GBP→JPY) ≈ 0.00945 (the reciprocal fraction gives
2.4e15, off by 107²). **Implemented `usd_per_x = rate(GBP→USD)/rate(GBP→X)`**
(USD per 1 unit of X). Verified live: NTT me_usd = $2.110e11; USD/JPY = 0.00934
=> JPY/USD = 107.04 in Jan 2000. The X='GBP' (→rate(GBP→USD)) and X='USD' (→1)
special cases are consistent with this direction.

# Finding F2: ret_usd FX denominator uses the security's OWN prior-month currency

`ret_usd(t) = (1+ret_local(t)) * usd_per_x(curcdd_t, t)/usd_per_x(curcdd_{t-1},
t-1) - 1`, where `curcdd_{t-1}` is the security's currency in month t-1 (carried
in the stage table), NOT the same currency's lag. This is essential at currency
redenominations — the 1999 euro transition for 8 of the 13 countries
(ATS/BEF/FIM/FRF/DEM/ITL/NLG/ESP → EUR): `prccd` redenominates (e.g. /6.55957 for
FRF) while `ajexdi` does NOT adjust, so `ret_local` carries a spurious ~-85% to
~-100% drop in Jan 1999. The FX ratio usd_per_x(EUR,Jan99)/usd_per_x(FRF,Dec98)
= conv-rate (6.557 ≈ official 6.55957) exactly cancels it. Verified on the built
panel: eurozone-8 Jan-1999 ret_usd min = -0.47, mean = -0.032 (no -0.85 cluster).
For stable currencies curcdd_{t-1}=curcdd and this reduces to the ordinary
month-over-month FX change. (Using a same-currency lag would have left the
spurious drop in ret_usd for all eurozone securities in Jan 1999.)

# Finding F3: Compustat Global/NA prices effectively start Dec 1985 — the
1979-12 window is unfilled

The SQL data window is 1979-12-01 .. 2006-06-30 as specified, but the source data
does not reach back that far. Verified: g_secd rows for the 13 countries exist
from ~1985-01 but `prccd` is NULL before 1985-12; priced observations begin
1985-12-31 for 11 countries (BEL 1983-12-30, GBR a single 1984-04 row), with true
DAILY coverage from 1986-01. **No securities exist before 1983-12** (0 rows before
1982-02). Consequences: the panel's first month-end is 1983-12-31 (BEL); the first
monthly return is 1984-01 (BEL) / 1986-01 for the bulk; the paper's Jan-1985
sample start cannot be met (1985 has prices only at Dec month-end). The lag-60
signal/Year-4-5 strategies are therefore feasible only from ~1990-12 (1985-12 +
60m) for the main countries, not Feb-1985. This is a hard Compustat-vintage
limitation (consistent with A1's Tier-2 framing).

# Finding F4: Canada multi-issue firms duplicate gvkey in the gvkey-only output

Per A2 the Canada universe keeps ALL `excntry='CAN'` issues. 5,194 distinct
(gvkey,iid) vs 4,763 distinct gvkey; 22,725 of 421,233 Canadian (gvkey,month)
groups carry >1 iid (25,855 extra rows). The output schema has gvkey only (no
iid), so these appear as duplicate (gvkey,month) rows — they count as separate
"stocks" in cross-sections and inflate Canadian firm-month counts. Global has 0
such duplicates (one primary issue per firm). Flagged for the Replicator; not
changed (output schema is fixed).

# Finding F5: ret_local is spurious at redenomination months (by design)

Because ret_local = (prccd/ajexdi)_t/(prccd/ajexdi)_{t-1}-1 and ajexdi does not
adjust for currency redenomination, ret_local shows the spurious euro drops. Of
438 ret_local beyond [-0.99, 10], 364 are in Jan-1999 (euro). ret_usd is NOT
affected (see F2). Downstream tables that use USD returns (ret_usd) are clean;
any table using ret_local directly would inherit the redenomination spikes. No
winsorization applied (A9). 72 ret_usd beyond [-0.99, 10] are genuine penny-stock
spikes (mostly Canada/dot-com era; ret_local ≈ ret_usd, no FX distortion).

# Assumption 11: Effective sample start 1986-01 (Compustat vintage limit)

**Decision:** Keep the SQL window 1979-12..2006-06 as the paper specifies, but
accept that priced Compustat observations for the 13 global countries begin at
month-end 1985-12 (BEL 1983-12), so the first bulk monthly return is 1986-01.
Report every table over the paper's stated window (Feb 1985-June 2006) using
all available observations per month, exactly as the paper conditions on
"firms with returns available in month t and t-k" (L112). Consequently:
Table 2 regressions run from the first feasible month per lag (lags 1-12 from
1986-02; lag 24 from 1988-01; lag 36 from 1989-01; lag 48 from 1990-01; lag 60
from 1991-01), each averaged over its own feasible months; Table 3/7 Year 1
and Years 2-3 strategies span ~1987..2006 and ~1989..2006 respectively;
Years 4-5 strategies (need lags 37-60) span ~1991-01..2006-06 (~186 months vs
the paper's 257). Early-1986 cross-sections are also thinner than the paper's
(~2,900 firms vs the paper's full FactSet universe).
**Rationale:** No substitute source covers 1980-1984 for these markets
(verified: Datastream indices only, TRTH code tables only, g_secm from 2007).
The paper's own methodology conditions on availability; our vintage simply
starts later. This compresses the averaging windows for long-lag cells —
documented per-table in REPORT.md; long-lag cells are evaluated with this in
mind (Tier 2 where the shorter window moves magnitudes beyond tolerance).
**Impact:** All long-lag cells of Table 2 (lags 24-60), Table 3/7 Years 2-3
and Years 4-5 rows, and the early-month composition of every average.

# Assumption 12: One security per Canadian firm

**Decision:** For the Compustat NA Canada universe, keep exactly one iid per
gvkey: the issue with the largest total market cap over the sample (sum of
prccd x cshoc across months), tie-broken on the lexically smallest iid.
**Rationale:** The paper's unit of analysis is the firm (Table 1 counts unique
firms; deciles hold "stocks" but the global file contributes one primary issue
per firm, so Canada must match to avoid over-weighting multi-issue firms in
the pooled cross-section). The panel build found 5,194 distinct (gvkey,iid)
vs 4,763 gvkey for Canada (25,855 duplicate firm-month rows, ~6% of Canadian
obs); Compustat NA has no prirow-style primary flag per listing in the
security file, so the largest-listing rule is the deterministic proxy for the
primary quote (multi-issue firms' secondary classes are typically small or
preferred-style lines). Additionally, firms domiciled in one of the 13 global
countries but cross-listed in Canada (16 gvkeys with Canadian prices) are
kept under their domicile country (global source), so the two data sources are
disjoint at the gvkey level — one firm, one country, matching the paper's
country assignment (see F6). Verified after the fix: 0 duplicate
(gvkey, month) groups anywhere, 0 gvkeys under >1 country, Canada = 4,747
firms (1985: 425 → 2005: 3,436).
**Impact:** Canadian firm counts (Table 1), and every pooled cell where
Canadian firms appear (Tables 2, 3, and Table 7's Canada column).

# Finding F6: Canada single-issue dedup + cross-source overlap exclusion
#            (rep-worker, inner iter 1 revision)

Implemented Assumption 12 in `universe_canada.sql` and the `can_uni` CTE of
`month_end_prices.sql`:

(a) **One iid per Canadian gvkey.** The winning iid is selected by
`row_number() OVER (PARTITION BY gvkey ORDER BY tot_me DESC, iid ASC)`, where
`tot_me = sum(if(cshoc>0, prccd*cshoc, 0))` summed over month-end observations in
the 1979-12..2006-06 window (NULL me skipped; `sum`→0 for an issue with no valid
me, so data-bearing issues always outrank empty ones, and ties fall to the
lexically smallest iid). Picks confirmed sane (e.g. gvkey 002369 of 34 iids →
iid 01C, tot_me 8.3e11 > runner-up 6.2e11). This removed the 25,855 duplicate
(gvkey,month) rows from multi-issue firms.

(b) **Cross-source gvkey overlap exclusion (needed for "zero duplicates
anywhere").** After (a), 442 duplicate (gvkey,month) rows remained — 11 firms
domiciled in the 13 global countries (GBR 5, SWE 2, JPN/DEU/FRA/CHE/NLD-ish) that
are ALSO cross-listed in Canada (security.excntry='CAN'), so they appeared once
from g_secd (domicile) and once from secd (Canada). To keep the two sources
disjoint at the gvkey level (one firm, one country = domicile, matching the
paper), `can_issues` now also filters
`AND gvkey NOT IN (SELECT gvkey FROM g_company WHERE loc IN <13 countries>)`.
55 Canadian-listed gvkeys are domiciled in the 13 countries; 16 of those had
Canadian price data (11 true duplicates kept on the global side + 5 foreign
firms' Canadian listings with no global data, dropped entirely).

**Result on the rebuilt panel:** Canada = 4,747 gvkey = 4,747 (gvkey,iid) (one
issue each); **zero (gvkey,month) duplicate groups anywhere**; zero gvkeys under
more than one country. Panel 1,955,687 rows; 19,685 unique gvkey. ret_usd summary
essentially unchanged (mean 0.01309→0.01308, std 0.30187→0.29999). Supersedes the
F4 flag. Everything else unchanged (global universe, month-end logic, FX, ret_usd
euro handling, output schema). If the Replicator prefers foreign cross-listings
counted under Canada instead, flip (b) to exclude from the global side.

# Finding F7: Table 3 Year-1 spreads near-zero / sign-flipped vs paper —
#            verified data-source effect, not an implementation bug
#            (rep-worker, inner iter — Table 3)

Implemented Table 3 (`src/compute_t3.py`) exactly per the fixed spec (A5/A6/A7/
A9/A11). Long-horizon cells reproduce the paper closely, e.g. EW Panel A total:
Y23 nonannual -0.0151 (paper -0.0143), Y23 all -0.0141 (-0.0127), Y45 nonannual
-0.0052 (-0.0056), Y45 all -0.0042 (-0.0042, exact to rounding). Year-1 cells
diverge: EW Panel A Y1 nonannual -0.0053 (paper +0.0121, sign flip), Y1 all
-0.0040 (+0.0131), and the annual strategies are systematically weak across all
three groups (|ours| ≲ 0.002 vs paper 0.004-0.008).

Verified the divergence is NOT an implementation artifact:
(a) The vectorized (gvkey×month) engine matches a fully independent pandas-merge
    brute force to 0.00e+00 on every tested month × panel × weighting (EW & VW,
    Panel A & B), including decile assignment, EW/VW and intra/inter spreads.
(b) Intra/inter additivity (Total = Intra + Inter) holds to 3.25e-18 across all
    144 return cells.
(c) The Year-1 signal uses ~10.5 of 11 lags in steady state (no NaN-induced
    signal weakening); feasible T match the spec's expectation (EW Y1=257,
    VW Y1=245; Y45=233 from the 1987-02 Canada-only start, Y45 annual=222).
(d) The Year-1 divergence is flat across the sample: 1987+ steady-state gives
    Y1 nonannual EW Panel A -0.0053 (full -0.0053) and Panel B +0.0009 (full
    +0.0010) — i.e. NOT driven by the thin 1985-86 early months. Short-horizon
    Year-1 momentum is genuinely near-zero in the Compustat data.

Interpretation (for the Replicator to tier): the pattern — long-horizon reversal
replicates, short-horizon Year-1 momentum collapses — is consistent with A1's
Compustat large-cap tilt (FactSet's broader, smaller-cap universe carries the
short-horizon momentum). Recommend Tier 2 for Year-1 and annual-lag cells, Tier 1
for the long-horizon nonannual/all cells. No methodology change made.

# Assumption 13: No microcap/penny-stock exclusion despite diagnosed contamination

**Decision:** Keep A9 — no filtering of extreme returns. Report the Table 3
Year-1 cells as they fall in the Compustat universe, evaluated at Tier 2 with
documented justification.
**Rationale:** Diagnosis (inner iteration 3): the Y1 nonannual EW Panel A
spread is −0.0053 (t −1.62) vs paper +0.0121 (t 4.17). Sensitivity tests pin
the divergence to microcap penny-stock contamination, not methodology:
(a) dropping Canada → +0.0002 (68% of extreme returns are Canadian TSX-V-style
microcaps); (b) dropping firm-months with |ret_usd| > 100% → +0.0055 (t 1.91);
(c) |ret_usd| > 60% → +0.0119 (t 4.72), matching the paper almost exactly;
(d) top-50% market cap → +0.0059. A ±60% filter was considered and rejected:
it replicates the paper's cell only because it removes the junk tier, and
selecting the threshold that reproduces the target cell is the
"tweaking-to-fit" failure mode the skill prohibits. The alternative
justification — calibrating the filter to the paper's reported cross-sectional
volatility (L112: Belgium 10.6%, Canada 25.9%) — was checked and fails:
unfiltered Canadian cross-sectional std is 0.299 (already near the paper's
0.259) and European countries are BELOW the paper's range, so volatility
matching does not select the filter that fixes momentum. The paper applies no
filter and explicitly includes small stocks (Table 5); the FactSet vintage was
simply cleaner (institutional-grade coverage). The long-horizon cells that the
filter does not touch replicate at Tier 1 (Y23 nonannual −0.0151 vs −0.0143;
Y45 nonannual −0.0052 vs −0.0056), which is the cleanest evidence the
methodology itself is correct. The sensitivity battery is reported in
REPORT.md as universe-composition evidence, mirroring the paper's own
size/liquidity subsample logic (Tables 5-6).
**Impact:** Y1 nonannual/all cells (24 cells) FAIL on sign; Y23/Y45 annual
cells are weak (Tier 2); the headline Y23/Y45 differences and long-horizon
reversals are Tier 1. 52 of 288 T3 cells FAIL overall, of which ~24 are the
documented Y1 contamination, ~20 are noise-level inter-country or
statistically-insignificant difference cells (|paper value| < 0.003 with
|t| < 2 in the paper itself), and 8 are weak annual-strategy cells.

# Finding F8: Tables 4/5/11/12 implementation conventions and one data artifact
#            (rep-worker, outer iteration 2 — audit M1/M2)

Implemented `src/compute_t4_t5.py` (Tables 4, 5) and `src/compute_t11_t12.py`
(Tables 11, 12), importing the verified engines (`compute_t3`, `compute_t7`)
without modifying them. Verification: the Table 4 monthly spread series are
bit-identical (max |diff| = 0.00e+00 over all 12 group x row series) to the
audit-verified `cells_t3.json` EW Panel A total series; the Table 11 annual
signal matrices are bit-identical to `compute_t7.compute_signals`' annual
slices; a fully independent pandas re-implementation of the Table 5 sorts for
2000-06 matches the engine to 0.00e+00 in all six size columns (both
breakpoint conventions).

Conventions fixed as specified by the Replicator (documenting the exact
boundary semantics for auditability):
- **Table 5 size assignment** (monthly, from me_usd at t-1, finite and > 0):
  breakpoints = 30th/70th percentiles (np.percentile, linear interpolation);
  small: me <= q30; medium: q30 < me <= q70; large: me > q70
  (np.searchsorted([q30,q70], me, side='left')). Percentiles computed over
  all firms with a valid size at t-1 (intracountry: within each country;
  intercountry: pooled cross-section). Firms without a valid prior-month
  size are not size-classified and do not enter the Table 5 sorts that month.
  Deciles are then formed WITHIN each size group, pooled across countries,
  with the same signals and rank mechanics as Table 3.
- **Table 11 correlations**: Pearson over pairwise-complete (common) months
  of the per-country EW Panel A annual-strategy spread series (pandas
  DataFrame.corr). t11_text_sig_threshold emitted as the paper's stated
  constant 0.12.
- **Table 4**: per-calendar-month means/t-stats of the pooled EW Panel A
  monthly spread series (identical to Table 3's); Feb-Dec = all sort months
  except January; difference row = annual[t] - nonannual[t] on common months.

**Data artifact (reported, not altered):** the Years 2-3 matrix carries one
pair above |rho| 0.6 — NLD-GBR = +0.90 — which is single-month-driven:
dropping 2002-12 alone gives rho = -0.078. Cause: one Dutch microcap
(gvkey 132538, me_usd ~$6.5M) returned +8,589% in 2002-12 and sits in the
Netherlands bottom decile, so the NLD annual spread that month is -4.52 —
the unwinsorized-panel penny-stock class already documented in A13/F7 (no
filter applied, per A13). The cell is flagged in table_11_correlations.md;
no committed T11 metric involves that pair. Mean pairwise y23 excluding the
pair = +0.043 (vs +0.052 with it).

# Assumption 14: Table 6 (liquidity subsamples) deferred — panel lacks price/volume fields

**Decision:** Do not compute Table 6 in this run; document as a data-blocked
gap rather than extending the panel.
**Rationale:** Table 6's three filters (price ≥ $5 USD, top 75% of price
within country, top 50% of volume within country) require month-end price in
USD and trading volume. The validated panel carries me_usd but neither shares
(cshoc), price, nor volume (cshtrd). Extending src/sql/month_end_prices.sql
to carry them would rebuild data/panel.parquet; audit 1 verified the panel
end-to-end and instructed iteration 2 not to touch it, so the extension was
deferred to preserve the verified artifact set. The liquidity claim is
partially covered by Table 5 (size groups, which the paper presents as the
liquidity proxy — L1200: "Small stocks are less liquid") and by the A13
sensitivity (top-50% market cap restores Year-1 momentum).
**Impact:** Table 6 (3 panels × 4 rows × 3 filters) is absent from results;
not committed in tables_to_replicate.json. Marked actionable in a future run
that rebuilds the panel with price/volume columns.

---

## Outer iteration 2 — issue log (audit 1 findings)

### Iteration 2 — M1: computable corollaries Tables 4 and 5
- Diagnosis: audit 1 flagged Tables 4/5 as computable from the panel but
  absent (corollary score 2/5).
- Next fix: src/compute_t4_t5.py importing the verified compute_t3 engine —
  calendar-month averaging (T4) and monthly 30/40/30 USD size groups with
  intracountry + intercountry breakpoints (T5); 312 + 144 committed cells.
- Before metric: 0 of 456 corollary cells computed.
- After metric: 456/456 cells; T4 nonannual negative 11/12 months, Feb-Dec
  difference +0.0113 (t 3.77) vs paper +0.0155 (7.12); T5 Y23 difference
  positive in 6/6 size columns (46-89% of paper magnitude); engines
  re-validated vs from-scratch reimplementations (max diff 0.00).
- Status: resolved (Table 6 deferred — A14).

### Iteration 2 — M2: Table 11 correlations and Table 12 bin robustness
- Diagnosis: audit 1 flagged the missing cross-country correlation matrix
  (abstract claim) and quintile/tricile robustness.
- Next fix: src/compute_t11_t12.py — per-country annual-strategy series via
  compute_t7 mechanics → 14×14 Pearson matrices per panel (T11: 11 committed
  cells + full matrices in the md); compute_t3 engine with 5 and 3 bins
  (T12: 240 cells).
- Before metric: neither corollary computed.
- After metric: mean pairwise ρ = 0.111 (y1), 0.052 (y23), 0.015 (y45) —
  the abstract's low-correlation claim holds; FRA-DEU y1 0.39 vs paper 0.43;
  quintile/tricile signs match deciles in 11/12 rows; 148/240 T12 cells
  Tier 1. One NLD-GBR y23 outlier pair (0.90, single-month penny-stock
  driven) flagged in the md, no committed metric uses it.
- Status: resolved.

### Iteration 2 — M3: dual-scheme tier evaluation
- Diagnosis: audit 1 flagged that the repo's Tier 2 (any sign match) is
  looser than the rubric's 2× rule, and the evaluation logic was uncommitted.
- Next fix: src/evaluate.py — both schemes over all 1,613 committed cells;
  near-zero-paper rule documented in the script.
- Before metric: ad hoc single-scheme counts (319/379/65/143 for 4 tables).
- After metric: repo rules 613 T1 / 713 T2 / 287 FAIL; rubric rules 613 /
  299 / 701; all 9 audit-1 anchor assertions pass exactly (repo 319/143;
  rubric 319/184/403 for the original four tables).
- Status: resolved.

### Iteration 2 — M4: committed sensitivity battery
- Diagnosis: audit 1 flagged the A13 battery as prose-only; its re-
  implementation diverged on two t-stats because filter semantics were
  unpinned.
- Next fix: src/sensitivity_y1.py — pinned primary semantics (recompute in
  filtered universe) + secondary semantics reported for completeness.
- Before metric: ad hoc +0.0055 (t 1.91) / +0.0119 (t 4.72), unreproducible.
- After metric: committed primary −0.0053→+0.0002→+0.0058 (2.26)→+0.0149
  (6.79)→+0.0066; secondary +0.0049/+0.0117; baseline matches the engine to
  1e-12; auditor's independent numbers reproduced at display precision.
- Status: resolved.

### Iteration 2 — minors m1-m7
- m1 (firm-month counts clarified in REPORT §4.1), m2 (lag-3 All-OLS miss
  acknowledged in §4.2), m3 (Canada Y45 reworded in §4.4), m4 (extreme-return
  count fixed in §2: 57 above +1,000%, 68 two-tailed), m5 (qunit removed from
  data_verification.json), m6 (Y23-difference breadth claim qualified in
  §4.4 and corrected in logs/log1.md), m7 (covered by src/evaluate.py).
- Status: all resolved.
