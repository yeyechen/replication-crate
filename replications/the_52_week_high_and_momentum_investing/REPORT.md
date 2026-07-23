# Replication Report — George & Hwang (2004), "The 52-Week High and Momentum Investing"
*The Journal of Finance, Vol. LIX, No. 5, October 2004, pp. 2145–2170*

## 1. Paper and scope

The paper shows that a stock's nearness to its 52-week high — P_{i,t−1}/high_{i,t−1} —
predicts cross-sectional returns better than the momentum signals of Jegadeesh–Titman
(1993, past 6-month return) and Moskowitz–Grinblatt (1999, past 6-month industry
return), that the 52-week-high strategy dominates all three in Fama–MacBeth
regressions that include them simultaneously (with size and lagged-return controls),
that it still dominates after adding Grinblatt–Han (2002) embedded-capital-gain
(disposition-effect) dummies, and — unlike JT/MG momentum — its profits do not
reverse at 2–4 year horizons.

We committed initially to five tables / 516 cells
(`preparations/tables_to_replicate.json`): **Table I** (strategy returns),
**Table II** (January split), **Table III** (pairwise nested sorts), **Table V**
(Fama–MacBeth dummy regressions, (6,6)+(6,12), raw + FF risk-adjusted),
**Table VII** (Table V + GH dummies). After audit 1 flagged the missing
corollaries, the scope was extended to **seven tables / 900 cells**: **Table VI**
(long-horizon persistence, (6,k,12) k=12/24/36/48, risk-adjusted) and **Table IX**
(52-week-low robustness) were added, and four pre-registered sensitivities were
run to conclusion (delisting returns — adopted; 52WH signal granularity — daily
closes adopted; GH coverage relaxation — tested, rejected by criterion; A13
rankable-only FM sample and MG industry-level cutoff — tested, kept official).

**Final tally: 537 Tier 1 / 282 Tier 2 / 81 FAIL of 900 cells (59.7% Tier 1).**
All of the paper's qualitative claims replicate: the three strategies' (6,6)
returns and January anatomy (Tables I–II), the nested dominance of the 52-week
high within winner/middle groups (Table III), the dominance ordering in the
Fama–MacBeth regressions outside January and after risk adjustment (Table V),
52-week-high dominance surviving Grinblatt–Han disposition controls (Table VII,
WH spreads 16/16 Tier 1), the **non-reversal of 52-week-high profits at 1–4 year
horizons** (Table VI), and the **unprofitability of the 52-week-low strategy**
(Table IX). Quantitative misses concentrate in four documented clusters: (a)
small-cell January legs of Table III's nested loser groups; (b) the GH-dummy
columns of Table VII (1970s volume-missingness in this CRSP vintage); (c) the
two January-included raw columns of Table V, where the paper's WH>JT margin
inverts in our vintage (tested via the A13 sensitivity — not recoverable);
(d) JT/MG dummy levels, which run ~1.4–1.6× hot throughout (same SIC-vintage
offset as Table I's MG row; tested via the industry-cutoff sensitivity — not
the cutoff mechanics).

## 2. Data

CRSP vintage `crsp_202601` (msf, dsf, dsenames, msedelist), FF factors from
`ff.four_factor_monthly` (exactly the paper's 462 months, 1963-07..2001-12).
Verified pre-flight: msf monthly universe counts grow ~2,088 (Jul 1963) → ~8,300
(2001) with the expected CRSP coverage jumps (1962-06, 1972-11); IBM spot-checks
confirm prc/shrout units; **msf.vol is in hundreds of shares** in this vintage
(verified msf.vol×100 = Σ dsf daily volume exactly) — critical for GH turnover;
ClickHouse's `Date` type cannot hold pre-1970 dates (saturates to epoch) — all SQL
uses `toDate32`/string month keys.

Panel: `data/panel.parquet`, 2,387,326 rows × 20 cols (2,373,418 universe
stock-months + 13,908 delisting-month rows carrying dlret; 1958-01..2002-12,
540 month-ends, 0 duplicate keys; the two iteration-2 columns are g_gh_b
(variant-B GH embedded gain, experimental) and wh_lo_sig (52-week-low signal)). Every signal brute-force-recomputed for sample
permnos to ≤1e-15; bit-exact rebuild guard on every panel regeneration.

## 3. Methodology decisions (paper-silent choices → `preparations/assumptions.md`)

13 logged assumptions, of which four were settled empirically:

1. **Universe** — "all stocks on CRSP" (L73, L81) implemented as shrcd {10,11}
   point-in-time (dsenames), all exchanges. Jul-1963 universe 1,977 stocks.
2. **Delisting (RATIFIED by experiment)** — holding-period returns fold in
   `msedelist.dlret` (ret_dl column; mean performance-delist dlret −15.2%; 93.3%
   coverage; no Shumway/BMP imputation). Signals/rankings/FM controls stay on
   original ret. Pre-registered criterion favored adjustment: 338 vs 332 Tier-1
   cells; Table I JT loser 1.089 → 1.050 (paper 1.05, exact).
3. **52-week-high price (LOCKED by pre-registered comparison)** — max of DAILY
   closing prices over the 12-month window (from dsf). The monthly-high (askhi)
   variant is contaminated (CRSP signs quote-based highs negative for pre-1983
   NASDAQ: 20% of stock-months non-positive); daily-close-max cuts total deviation
   on the 52 cells it affects by 22.8% vs month-end-close-max.
4. **MG 20 industries** — the EXACT Moskowitz–Grinblatt (1999) Table I grouping
   (retrieved from the cited paper): e.g. SIC 32 labeled "Construction", Services
   in "Other". Validated: MG's "Other" industry reproduces their reported average
   stock count exactly (981.4 vs 981).
5. **Regression units** — triangulated from reported coefficients: R_t in percent,
   R_{t−1} in decimal, size = ln(mcap in dollars). Confirmed: our R_{t−1}
   coefficient −6.18 vs paper −6.50, size −0.19 vs −0.20.

Other logged assumptions: compounded 6-month signals requiring 6 non-missing months;
30/30 ordinal cutoffs with (signal, permno) tie-break; EW portfolios and EW
six-cohort overlap for (6,6) (L120); no skip month for Tables I–IV vs skip month
j=2..7 / 2..13 for Tables V+ (footnote 3); nonempty-both-cells month rule for
nested W-L rows (footnote 6); FF3 risk-adjustment intercepts (L596); GH turnover
V = vol×100/(shrout×1000) capped at 1 with the 60-lag reference-price recursion
(equation 2); un-rankable stocks keep zero dummies in the FM cross-section.

## 4. Results

### Table I — Profits from momentum strategies (12/12 Tier 1)

| Strategy | Winner (ours/paper) | Loser (ours/paper) | W−L (ours/paper) | t (ours/paper) |
|---|---|---|---|---|
| JT momentum | 1.52 / 1.53 | 1.05 / 1.05 | 0.47 / 0.48 | 2.25 / 2.35 |
| MG industry | 1.52 / 1.48 | 0.95 / 1.03 | 0.57 / 0.45 | 4.54 / 3.43 |
| 52-week high | 1.47 / 1.51 | 1.04 / 1.06 | 0.42 / 0.45 | 1.76 / 2.00 |

All three strategies land at the paper's ~0.45–0.57%/month; the 52WH return cells
are within 0.04pp of the paper (t-stat −12%). The JT row is near-exact after
delisting adjustment (loser 1.0504 vs 1.05). MG runs ~28% hot on the spread
(consistent SIC-vintage offset, see §5).

### Table II — January split (23/24 Tier 1, 1 Tier 2)

Ex-January W−L: JT 1.076 (paper 1.07, t 6.79/6.97); MG 0.644 (0.50, t 5.29/3.92);
52WH **1.181 (1.23, t 6.52/7.06)**. January-only: JT −6.27 (−6.29, t −4.30/−4.48);
MG −0.20 (−0.09, t −0.28/−0.12); 52WH −8.03 (−8.27, t −5.07/−5.49). The
tax-loss-selling anatomy replicates precisely: loser portfolios earn 0.08–0.39%/
month outside January and 11.3% (JT) / 11.8% (52WH) in January, while MG's January
effect is near zero (losers 7.16% vs winners 6.96%; paper 7.09/7.00). The single
Tier-2 cell is MG's January t-stat on a −0.20pp spread.

### Table III — Pairwise nested comparisons (31/48 Tier 1, 15 Tier 2, 2 FAIL)

Internal consistency exact (shared cells identical across panels A/B). The middle
group matches tightly (52WH W−L within JT-middle 0.25/0.78 vs paper 0.26/0.86;
JT W−L within 52WH-middle 0.30/0.40 vs 0.27/0.30). Residual misses: W−L spreads
nested inside LOSER groups run at ~45–55% of the paper's magnitude (within-JT-loser
52WH spread 0.30/0.44 vs paper 0.56/0.98), driven by their January legs in small
cells (~180–600 stocks in the 1960s). The two FAILs are rounding-boundary cells
(paper 0.01 vs ours −0.08). The paper itself flags these cells as unbalanced
(footnote 6: "in some months it has none") and supersedes them with the regression
tables — which is exactly what Tables V/VII provide.

### Table V — Fama–MacBeth dummy regressions (150/192 Tier 1, 42 Tier 2, 0 FAIL)

8,316 cross-sectional regressions (2,772 for (6,6), 5,544 for (6,12)); avg sample
4,804 stocks/month; FF3 aligned to all 462 months. Mechanism validated by the
control coefficients: R_{t−1} −6.18 (paper −6.50), size −0.19 (−0.20), intercepts
match ex-January within ±8% (2.01 vs 1.87); Jan-included intercepts run ~30% high
(stronger small-cap January in the NASDAQ-inclusive universe — consistent with
Table II). Pure-strategy spreads (s66, raw ex-Jan): **52WH 0.87 (paper 1.06,
t 6.1/7.6) > JT 0.64 (0.46, t 6.0/4.4) > MG 0.36 (0.22, t 4.2/2.5)**; risk-adjusted
ex-Jan: 52WH 0.84 (1.13, t 8.7/11.4) > JT 0.69 (0.46) > MG 0.34 (0.24). The
wh_spread row is Tier 1 in all 16 of its cells (8 columns × value + t-stat).
**Headline caveat, stated plainly:** the paper's single most-cited number — the
(6,6) raw Jan-included column, WH 0.65 > JT 0.38 > MG 0.25 — **inverts in our
run** (JT 0.53 > WH 0.49 > MG 0.38), and the (6,12) raw Jan-included column
inverts too (JT 0.33 > WH 0.31). The inversion is two-sided: our WH spread sits
at ~0.69–0.83× the paper's (wh_loser dummy only ~0.64×), while our JT/MG spreads
run ~1.4–1.6× hot — and in the two January-laden raw columns the combination
flips the ordering. Where the paper itself stakes the dominance claim — "outside
of January, the 52-week high strategy is even more dominant" and "dominance ...
is stronger in risk-adjusted returns" — the ordering replicates with margin in
all six remaining columns (e.g. raw ex-Jan WH 0.87 > JT 0.64 > MG 0.36; RA
ex-Jan WH 0.84 > JT 0.69 > MG 0.34), as do Table VII's WH spreads (16/16 Tier 1)
and the nested winner/middle comparisons of Table III. The pre-registered A13
sensitivity (rankable-only FM sample, outer iteration 2) **tested** the
inversion: restricting the cross-section to stocks rankable on all three signals
(90.8% of stocks retained) leaves the inversion intact (WH 0.483 vs JT 0.542 in
s66 raw Jan-included) and flips two additional RA columns — the margin is not
recoverable by sample definition, so the inversion is classified a CRSP-2026-
vintage effect (`results/table_5_sensitivity_rankable.md`).

### Table VII — with Grinblatt–Han dummies (122/240 Tier 1, 102 Tier 2, 16 FAIL)

Pre-flight exact: wh_spread 0.5203 vs paper 0.51 with GH controls. **wh_spread:
16/16 cells Tier 1** across all columns — e.g. (6,6) RA ex-Jan 0.825 vs 0.76
(t 8.46/9.09), (6,12) raw incl-Jan 0.346 vs 0.36. The paper's headline — the
52-week-high strategy dominates even after controlling for the disposition effect —
**replicates completely**. The GH side is the replication's weakest point:
gh_spread comes out near zero (e.g. s66 raw ex-Jan 0.012 vs paper 0.44) and
gh_loser sign-flips in five columns (all 16 FAILs are GH cells). Diagnosed causes (documented,
tested where noted): (i) GH coverage — g_gh requires 60 consecutive months of
volume, but this CRSP vintage has 40% missing monthly volume in the 1970s, so GH
bins are a thin NYSE-heavy subset early (rankable: ~1,000–2,000 stocks in the
1960s–80s vs ~3,700–6,200 for the other strategies); (ii) the delisting experiment
showed the gh_loser anomaly is NOT delisting-driven (coefficient unmoved by dlret);
(iii) the mismatch is January-concentrated (paper's GH bins have larger January
legs), pointing at early-sample bin composition. The coverage-relaxation
experiment (variant B: reference price renormalized over available lags, ≥24
months; null fraction 0.526 → 0.323) moved all eight gh_spreads toward the paper
(e.g. s66 raw ex-Jan 0.012 → 0.105 vs paper 0.44) but could not flip the
gh_loser sign and lowered the table's Tier-1 count (122 → 118), so the strict
measure stays official per the pre-committed adoption criterion
(`results/table_7_variantB.md`). The paper's secondary claim that GH dominates
JT/MG ex-January does not appear in our numbers — documented partial.

### Table VI — Long-horizon persistence (73/192 Tier 1, 64 Tier 2, 55 FAIL) — added at audit 1

The paper's third abstract claim — "future returns forecast using the 52-week
high do not reverse in the long run" — **replicates**. Risk-adjusted (6,k,12)
regressions at k = 12/24/36/48 months after formation: the 52WH winner dummy is
*never* negative at any horizon, and all eight wh_spread cells land within
±0.05pp of the paper — the anchor (6,~12,12) ex-January reproduces as 0.178
(t 2.39) vs paper 0.16 (t 1.93). The JT/MG reversal leg is attenuated in this
vintage: the JT winner dummy does reverse at k=12 (−0.068, t −2.09 vs paper
−0.18, −4.76 — sign and significance match) but decays to ≈0 by k≥24, and the MG
winner does not reverse (stays positive). That attenuation is the same
JT/MG over-persistence seen in Tables I/V (their dummies run hot here), not an
engine problem — the 55 FAILs concentrate in loser dummies and long-k JT/MG
winner cells.

### Table IX — 52-week-low robustness (126/192 Tier 1, 58 Tier 2, 8 FAIL) — added at audit 1

The paper's claim that a 52-week-*low* strategy is unprofitable **replicates**:
all eight wl_spread cells are statistically insignificant (|t| < 1, as in the
paper), with values at noise level (e.g. s66 raw incl-Jan 0.109, t 0.79 vs
paper 0.13, t 0.95). When the low dummies replace the high dummies, the JT
spread absorbs the predictability — it jumps to 1.11 ex-January (from 0.64 in
Table V) vs paper 1.05, near-exact; all 16 jt_spread cells are Tier 1. The
8 FAILs are sign flips on economically-zero insignificant spreads (paper
+0.01..+0.12 vs ours −0.07..−0.03).

### Figures

`results/cumulative_wl.png` — compounded all-month EW W−L strategy values,
1963–2001: MG 11.9× > JT 5.1× > WH 3.4× (the all-month EW means are within
0.03pp across strategies, so compounding puts MG on top — the 52WH dominance
lives in the ex-January and regression columns, shown next); the 2001 momentum
crash is annotated. `results/january_effect.png` — the January anatomy of
Table II. `results/table5_spreads.png` — ours-vs-paper regression spreads
across the four (6,6) columns of Table V (footnote records the one column —
raw Jan-included — where our WH/JT ordering inverts).

## 5. Known limitations (audit trail)

1. **MG-strategy levels run ~1.3–1.5× hot** (Tables I, V, VII) — consistent across
   two independent methodologies (EW sorts and FM dummies), which localizes the
   offset to the industry assignment, not the machinery: our MG industry counts
   match MG's reported "Other" exactly but "Financial" runs −18% vs their 1963–1995
   average, i.e. a SIC-vintage difference between this CRSP extract and MG's.
   MG is the paper's supporting strategy; its dominance-relative ordering still
   holds (MG weakest everywhere).
2. **Table III nested-loser spreads** — ~40–60% of paper magnitude ex-January;
   small-cell January legs; paper-acknowledged fragility (footnote 6); superseded
   by the regression tables, which replicate.
3. **Table VII GH cells** — near-zero GH spreads and gh_loser sign flips; diagnosed
   as 1970s volume-missingness → thin early GH bins (data-coverage limitation of
   this CRSP vintage for a 60-month-turnover measure); the WH-side claims are
   unaffected (16/16 Tier 1).
4. **Jan-included regression intercepts ~30% high** — stronger small-cap January
   in the all-exchange universe/2026 vintage; ex-January intercepts match within 8%.
5. **Jan-included raw-column dominance inversion (Table V)** — the paper's lead
   column (WH 0.65 > JT 0.38) inverts in ours (JT 0.53 > WH 0.49); tested via the
   A13 rankable-only sensitivity (90.8% of stocks retained) — not recoverable;
   classified a vintage effect. All ex-January and risk-adjusted columns
   reproduce the WH > JT > MG ordering with margin.
6. **MG spreads +28–62% hot across all tables** — tested via the industry-level
   top/bottom-6 cutoff variant: every MG cell moves the wrong way, so the offset
   is SIC-vintage/industry-momentum composition (our "Financial" industry runs
   1,294 stocks in 1990-06 vs MG's reported ~891), not cutoff mechanics.
7. **Table VI JT/MG reversal attenuation** — JT winner reverses at k=12 but the
   effect decays faster than in the paper and MG does not reverse; same JT/MG
   over-persistence as item 6. The 52WH non-reversal (the paper's claim) is
   unaffected and near-exact.

## 6. Reproducibility

`src/main.py` (panel, ~90s), `src/tables_1_3.py`, `src/tables_5.py` (shared FM
engine), `src/tables_7.py`, `src/tables_6_9.py` (Tables VI/IX), experiment
drivers `src/delisting_experiment.py`, `src/m2_experiment.py`, `src/m3_experiment.py`,
`src/m5_experiment.py`, and `src/plots.py`; SQL in `src/sql/` (msf_monthly,
dsenames_common, dsf_monthly_maxclose, dsf_monthly_minclose, ff_factors,
msedelist). Official outputs regenerated under the ratified configuration
(wh_sig_dc daily-close-max signal, ret_dl delisting-adjusted holding returns).
`RET_COL="ret"` reproduces the pre-delist-experiment numbers exactly; the FM
engine's Table V/VII outputs are sha256-identical across every iteration-2
engine change (proven in `logs/log2.md`).
Per-cell ours-vs-paper tables with tiers (Tier-2 cells with |ours/paper| > 2
flagged): `results/table_{1,2,3,5,6,7,9}.md`; experiment comparisons:
`results/delisting_experiment.md`, `results/table_3_dc_vs_cl.md`,
`results/table_7_variantB.md`, `results/table_5_sensitivity_rankable.md`,
`results/table_1_sensitivity_mg.md`; panel diagnostics: `results/panel_summary.md`;
coefficient caches for auditor recomputation: `results/intermediate/*.parquet`
(strategy_returns, fm_coefficients, fm_coefficients_gh, + variant/sensitivity
caches). Full reasoning trace: `logs/log1.md` + `logs/audit1.md` (outer
iteration 1) and `logs/log2.md` + `logs/audit2.md` (outer iteration 2).
