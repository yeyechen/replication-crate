# Assumptions Registry — Fama & French (1992), The Cross-Section of Expected Stock Returns

Paper-silent decisions and documented deviations from `rep/PAPER_CONVENTIONS.md`.
Paper-derived rules live in `preparations/preprocessing_rules.json`.

---

## Assumption 1: No minimum-price filter (convention deviation)

**Decision:** Do NOT apply the PAPER_CONVENTIONS default $5 price floor. The universe is exactly the paper's: all nonfinancial common stocks (shrcd 10/11, exchcd 1/2/3) in the CRSP × Compustat intersection that meet the paper's data requirements.
**Rationale:** The paper's universe definition is explicit and complete: "We use all nonfinancial firms in the intersection of (a) the NYSE, AMEX, and NASDAQ return files from CRSP and (b) the merged COMPUSTAT annual industrial files" (L119). No price screen is mentioned anywhere. A $5 filter would remove small firms the paper includes and would mechanically alter the equal-weighted small-stock portfolios (Table II's 1A has 772 firms/month). Convention defaults yield to explicit paper definitions.
**Impact:** All tables. Keeps the small-firm tail intact, which is essential for Table II Panel A (1A return 1.64%/mo) and the Table III intercepts.

## Assumption 2: Equal-weighting throughout (convention deviation)

**Decision:** EW portfolio returns everywhere; VW is computed only for the NYSE benchmark in Table VI.
**Rationale:** Paper-specified: "we calculate the equal-weighted monthly returns on the portfolios" (L171); all of Tables I–V report EW returns. Overrides the PAPER_CONVENTIONS VW default.
**Impact:** Tables I, II, IV, V (portfolio returns); Table VI (NYSE EW series as a reported benchmark).

## Assumption 3: No factor model / raw returns in regressions (convention deviation)

**Decision:** Fama-MacBeth regressions use raw stock returns (no risk-free subtraction), with no FF factors. The CRSP value-weighted index (msi.vwretd) is used only as the market proxy for beta estimation.
**Rationale:** Paper-specified (L145, L1185): FM regressions of "stock returns" on beta, ln(ME), ln(BE/ME), ln(A/ME), ln(A/BE), E/P variables. The paper predates the FF factor library and reports no alphas. Overrides the PAPER_CONVENTIONS factor-alpha default.
**Impact:** Tables III, VI.

## Assumption 4: Financial-firm exclusion via CRSP SIC codes

**Decision:** Exclude firms with SIC 6000–6999 using CRSP `dsenames.siccd` (point-in-time, as of the formation date).
**Rationale:** The paper excludes financial firms (L119) but does not specify the SIC source. `comp_202601.funda` carries no SIC column in this vintage (verified against the catalog), so CRSP's point-in-time SIC is used — the standard alternative.
**Impact:** All tables (universe size).

## Assumption 5: Delisting-return treatment (paper silent)

**Decision:** Monthly stock return = CRSP `msf.ret` when valid; for delisting months with missing `ret`, use `msedelist.dlret` when valid (not a sentinel in {-44,-55,-66,-77,-88,-99} and > -1.0); for performance-related delistings (dlstcd 500–590) with missing dlret, impute −0.30; otherwise treat as missing.
**Rationale:** Paper is silent on delisting treatment; it uses "the NYSE, AMEX, and NASDAQ return files from CRSP" (L119). Incorporating dlret is the conservative standard (Shumway 1997) and avoids understating small-stock losses. The −0.30 imputation applies only to the small set of performance delistings with no recorded dlret.
**Impact:** All portfolio-return cells (Tables I, II, IV, V) and Table VI EW/VW benchmarks.

## Assumption 6: Book-equity fallback chain

**Decision:** BE = ceq + coalesce(txdb, 0). If ceq is missing: BE = seq − coalesce(pstkrv, pstk, 0) + coalesce(txdb, 0).
**Rationale:** The paper defines BE as "the book value of common equity plus balance-sheet deferred taxes" (L813) and cites COMPUSTAT item 60 (ceq) (L119); it is silent on fallbacks when ceq is missing. The ceq → seq − preferred stock chain is the Davis–Fama–French–Wilkins convention used by the FF data library; treating missing txdb as 0 is documented in references/COMPUSTAT.md.
**Impact:** Every BE/ME, A/BE cell (Tables II, III, IV, V) and the negative-BE exclusion.

## Assumption 7: Pre-ranking betas use the Dimson sum-beta estimator

**Decision:** Pre-ranking betas (24–60 monthly returns ending June t) are estimated as the sum of the slopes on the current and one-lagged market return (msi.vwretd), the same estimator as the post-ranking betas.
**Rationale:** The paper specifies the sum-beta estimator for reported betas: "The pre- and post-ranking βs (here and in all other tables) are the sum of the slopes from a regression of monthly returns on the current and prior month's returns on the value-weighted portfolio..." (L253). The pre-ranking betas are used only for sorting, so the choice has second-order impact; matching the paper's stated estimator is the defensible default.
**Impact:** Composition of the 100 size-β portfolios (Table I) and the β-sorted portfolios (Table II Panel B).

## Assumption 8: Table V within-decile BE/ME breakpoints on all data-qualified stocks

**Decision:** Within each size decile, the 10 BE/ME breakpoints are computed from all NYSE/AMEX/NASDAQ data-qualified stocks in the decile (not NYSE-only).
**Rationale:** The Table V note says "The NYSE, AMEX, and NASDAQ stocks in each size decile are then sorted into 10 BE/ME portfolios using the book-to-market ratios for year t − 1" (L1818) without naming a breakpoint subset; the paper's only explicit BE/ME breakpoint convention is all-qualified-stocks (Table IV, L1382). NYSE breakpoints are specified only for size (L151) and pre-ranking β (L169).
**Impact:** Table V cell composition.

## Assumption 9: Winsorization applied to the log-ratio regressors

**Decision:** In the FM regressions, winsorize ln(BE/ME), ln(A/ME), ln(A/BE), and E(+)/P at the 0.005/0.995 cross-sectional fractiles each month (equivalently: winsorize the ratios BE/ME, A/ME, A/BE at the 0.005/0.995 fractiles before logging — identical cutoff ordering).
**Rationale:** The paper winsorizes "the smallest and largest 0.5% of the observations on E(+)/P, BE/ME, A/ME, and A/BE" (L1189). Since ln is monotone, fractile-clipping the logs is observation-identical to clipping the ratios.
**Impact:** Table III (slightly trims extreme slopes).

## Assumption 10: Table VI NYSE VW/EW benchmarks computed from CRSP NYSE common stocks

**Decision:** NYSE VW and EW monthly returns are computed from CRSP msf: NYSE-listed common stocks (PIT exchcd = 1, shrcd 10/11) with delisting-adjusted returns; VW weights are lagged end-of-month market caps.
**Rationale:** The paper reports "the value-weighted and equal-weighted (VW and EW) portfolios of NYSE stocks" (L2039). The CRSP msi index includes AMEX (from 1962) and NASDAQ (from 1972), so it is not the paper's NYSE-only series; computing from CRSP NYSE stocks matches the paper's definition.
**Impact:** Table VI benchmark rows (6 cells per subperiod).

## Assumption 11: Negative/zero earnings handled via the E/P dummy

**Decision:** If E ≤ 0: E/P dummy = 1, E(+)/P = 0. If E > 0: E/P dummy = 0, E(+)/P = E/ME_dec. (E exactly 0 is grouped with negative earnings.)
**Rationale:** Paper: "If earnings are positive, E(+)/P is the ratio of total earnings to market equity and E/P dummy is 0. If earnings are negative, E(+)/P is 0 and E/P dummy is 1" (L1185). The E = 0 case is a measure-zero edge; grouping with negatives is the conservative literal reading.
**Impact:** Table III E/P specifications, Table IV Panel B portfolio 0.

## Assumption 12: Appendix (1941–1990 NYSE) out of scope for this run

**Decision:** Replicate main-paper Tables I–VI. Appendix Tables AI–AII (NYSE-only, 1941–1990, no Compustat) are documented as out of scope.
**Rationale:** The appendix is a robustness extension ("further tests are appropriate", L2298) on a different sample (NYSE-only, pre-Compustat). The core claims live in Tables I–VI; the appendix requires separate 1941–1962 CRSP-only construction with different data requirements (L2348). Prioritizing the six main tables maximizes validated methodology coverage within the iteration budget.
**Impact:** No impact on main claims; documented scope boundary.

## Assumption 13: datafmt='STD' is valid for 1962–1989 in this extract

**Decision:** Filter comp_202601.funda with indfmt='INDL', consol='C', popsrc='D', datafmt='STD'.
**Rationale:** Verified against live ClickHouse: for fyear 1962–1989, the (STD, INDL, C, D) combination holds 169,400 firm-years — this extract stores pre-1987 data in standardized form, so the usual "STD drops pre-1987" warning (references/COMPUSTAT.md) does not apply here. SUMM_STD rows (51,178) are excluded as summarized duplicates.
**Impact:** Compustat universe for all tables.

---

## Iteration log entries (Stage 7)

(entries appended per inner iteration below)

### Iteration 1 — panel pipeline implemented (2026-07-22)

**Built:** `data/panel.parquet` (810,612 rows × 25 cols; 330 months July 1963 –
December 1990; 7,733 permnos) + `data/portfolio_returns.parquet` (100 size×pre-beta
portfolios × 330 EW monthly returns). SQL: `src/sql/{market_index_monthly,
monthly_returns_delist, me_formation, universe_pit_june, compustat_funda,
ccm_link_pit}.sql`. Sorts, Dimson betas (closed-form grouped OLS, cross-checked
against statsmodels to 6 decimals), and assembly in `src/main.py`.

**Implementation flags (for Replicator judgment, no methodology changed):**

1. ⚠️ **Size breakpoints and financials.** The Sort A spec enumerates the NYSE
   breakpoint set as "exchcd = 1, shrcd 10/11 PIT as of June t — NOT restricted
   to data-qualified, NOT restricted to Compustat-linked" with no SIC clause, so
   NYSE size breakpoints INCLUDE financial firms (matching the paper's "all NYSE
   stocks on CRSP", L151). This is in slight tension with the universe section,
   which defines the universe as excluding SIC 6000–6999 — if the Replicator
   intended breakpoints over the non-financial universe only, add the SIC filter
   to the `nyse_bp` set in `build_universe`.
2. ⚠️ **Universe evaluated at June t only.** The PIT universe screen (shrcd/
   exchcd/SIC) is applied at the June t formation date for the whole firm-year,
   including the December t−1-formed BE/ME and E/P sorts (Table IV). The spec's
   "point-in-time as of each formation date" could alternatively require the
   December t−1 screen for Table IV eligibility; implemented the single-June
   reading since the panel grain is one row per firm-year with all sort columns.
3. ⚠️ **Compustat units.** funda dollar items are $ millions; A/BE/E are scaled
   ×1e6 to dollars in `compustat_funda.sql` so BE/ME_dec, A/ME_dec, E/ME_dec are
   unit-consistent with CRSP dollar ME. Verified: IBM (permno 12490) panel
   ME_dec 1979 = $37.58bn matches Compustat prcc_f×csho = $37.57bn exactly.
4. **Data-vintage facts (not fixes):** avg 2,392.9 obs/month vs paper ~2,267
   (+5.5%, consistent with the crsp_202601 link table's ~3% more links and
   broader NASDAQ coverage); negative-BE drops 1,033 firm-years (avg 36.9/yr vs
   paper ~50/yr); fyear-1963 BE source (ceq or seq) covers only 1,519 firms in
   this extract (vs 2,110 for fyear 1962), producing the 1964 firm-count dip
   (385 < 534) — property of the extract, not the code.
5. **Delisting adjustment counts (196307–199012, all stocks):** 1,486,774 valid
   msf returns; 7,194 dlret substitutions; 260 imputed −0.30 (dlstcd 500–599);
   2 imputed 0.0 (dlstcd 200–399); 4 delistings left missing (other codes).
   dlret is substituted only when msf.ret is missing in the delisting month,
   exactly as specified (not compounded with a partial-month ret).

### Iteration 2 — Table I replicated (2026-07-22)

**Built:** `src/table_1.py` (analysis only; imports `grouped_dimson_beta`,
`ym_prev`, `q_file`, `LAYOUT` from `src/main.py` — no pipeline re-run).
`results/table_1.md` (Panels A/B/C, 11×11 each, + paper comparison) and
`data/agg_portfolio_returns.parquet` (21 EW series × 330 months: size_1..10,
beta_1..10, grand; columns series/ym/month/n_stocks/ret). Only ClickHouse
touch: `market_index_monthly.sql` (msi.vwretd, for the aggregated-series
Dimson betas). 100-cell betas reproduce the panel's stored post_beta to 0.0;
agg-series betas cross-checked against statsmodels to 5 decimals.

**Result: 107/107 targeted metrics pass** (A 51/51 @25%, B 15/15 @15%,
C 41/41 @10%, tolerances per tables_to_replicate.json).

**Facts / flags (for Replicator judgment, no methodology changed):**

1. Panel A runs slightly below the paper, largest in the high-β columns:
   All/All 1.19 vs 1.25; All×β-9 1.11 vs 1.25 (−0.14); All×High-β 1.03 vs
   1.14; Large×β-5 0.74 vs 0.93 (−0.19); Small×β-9 1.32 vs 1.50 (−0.18).
   All within the 25% tolerance. Size-decile All column is closer
   (max |Δ| 0.09 at ME-2).
2. Panel B: All column matches to ≤0.034; our 100-cell range is 0.49–1.76
   (paper 0.53–1.79) at the SAME cells (ME-8×Low-β, Small-ME×High-β).
3. Panel C: matches within ≤0.09 except All×Low-β (3.69 vs 3.86, −0.17,
   4.4%) and All×β-4 (4.28 vs 4.41, −0.13); both within 10%.
4. Stock-level grand EW (1.193%/mo) ≠ simple mean of the 100 cell returns
   (1.181%) — the stock-level aggregation the spec mandates for All
   column/row/All matters (cells have 13–3,679 stocks/month).
5. All 100 size×β cells exist in all 28 formation years; every EW series
   has exactly 330 monthly obs; 69,363 unique firm-years (avg 2,477/yr).

### Iteration 3 — Table II replicated (2026-07-22)

**Built:** `src/table_2.py` (analysis only; imports `LAYOUT` from `src/main.py`
— no ClickHouse, no pipeline re-run; reads `data/panel.parquet`).
`results/table_2.md`: both panels (9 rows × 12 cols 1A/1B/2-9/10A/10B;
2-decimal rounding, Firms integer) + cell-by-cell comparison block per panel
(ours vs paper, |Δ|, tolerance, pass) + overall summary. Targets/tolerances
read from `preparations/tables_to_replicate.json` (table_2). No-target cells
flagged: Panel A E(+)/P (×12, row absent from OCR) and Panel B interior Return
(×10; only 1A=1.20 and 10B=1.18 prose-anchored).

Aggregation implemented exactly per the paper notes (L815/L817/L819): every
statistic is the time-series mean (330 months) of the monthly cross-sectional
mean over the portfolio's members that month; Firms = mean over months of the
member COUNT (panel rows per (month, portfolio), regardless of return
validity). No portfolio-month is empty (min 8 / 19 valid-return members).
Identity ln(A/ME)−ln(A/BE)=ln(BE/ME) holds to 1.7e-16 across all 24 cells.

**Result: 168/194 targeted cells pass** (Panel A 79/96, Panel B 89/98).
Return, β, ln(ME), Firms and Panel B E(+)/P: 100% pass. Headline results
replicate — β-sorted returns are flat (Panel B 1A 1.15 vs 10B 1.11; paper
1.20 vs 1.18, both prose-anchored targets pass) while post-ranking β runs
0.81→1.73; size-sorted returns decline 1.60→0.85 (paper 1.64→0.90); ln(ME)
monotone 1.98→8.47 (paper 1.98→8.44, all ≤0.08).

**Facts / flags (for Replicator judgment, no methodology changed):**

1. All 26 failing cells are in the Compustat-accounting characteristic rows —
   ln(A/ME) 13, ln(BE/ME) 9, E/P dummy 3, ln(A/BE) 1 — i.e. the ratios built
   from Compustat A/BE/E and December ME. ZERO failures in Return, β, ln(ME),
   Firms or E(+)/P (the rows built from CRSP returns, post_beta, June ME, and
   membership counts), which reproduce the paper within tolerance.
2. The accounting-ratio deviations are a systematic data-level shift, not an
   aggregation artifact: the spec's monthly-mean method and a firm-year-mean
   alternative agree to ≤0.007 on every Panel A cell, whereas the paper gaps
   reach 0.21 (Panel A ln(A/ME) 10A 0.18 vs −0.03). Consistent with the
   iteration-1 vintage facts (+5.5% obs/month, different negative-BE drops,
   broader link table). Ours run HIGHER than the paper on ln(A/ME)/ln(A/BE)
   and LESS negative on ln(BE/ME) — largest at the large-firm end (10A/10B/9/6)
   where portfolios hold few stocks (10A 57, 10B 59) so a handful of extra
   firms move the mean.
3. Panel A 1A return 1.60 vs 1.64 (−0.04, 2.7%, PASS at 25%): our 1A holds
   918 firms/mo vs paper 772 (+19%); the extra microcaps dilute the EW return
   slightly, as the task anticipated. All other Panel A returns within ≤0.09.
4. Largest relative deviations are ratio cells with paper values near zero
   (Panel A ln(A/ME) 10A 713%, 10B 108% — paper −0.03; ln(BE/ME) 1A 55% —
   paper −0.01); the ABSOLUTE gaps (0.006–0.214) are in line with the rest of
   the row.

### Iteration 4 — Tables III & VI replicated (2026-07-22)

**Built:** `src/table_3_6.py` + `src/sql/nyse_benchmark.sql` (NYSE common
stocks, PIT exchcd = 1 / shrcd 10/11, delisting-adjusted returns identical to
monthly_returns_delist.sql + month-end ME, 196306..199012; the June 1963 row
supplies the first lagged VW weight). `results/table_3.md` (11-spec slope/t
matrix + Avg N + 52-cell comparison + flags), `results/table_6.md` (NYSE
VW/EW + reg(a)/reg(b) × 3 periods × Mean/Std/t(Mn), 81-cell comparison +
flags), `data/nyse_benchmark_returns.parquet` (330 months: month, ym, vw, ew,
n_stocks). FM estimation is a manual plain monthly-OLS loop (intercept;
valid-ret rows; the utils.fama_macbeth primitive always winsorizes every
regressor and uses HAC SEs, so the paper-exact procedure — pre-winsorize
ln_bm/ln_ame/ln_abe/ep_pos at the monthly 0.005/0.995 fractiles computed on
the valid-return sample, then plain OLS, plain time-series t per L1187, no
Newey-West — is implemented directly). reg(a) ≡ R7 verified identical.

**Results: Table III 30/52 targeted cells pass** (+2 no-target: R10 ln(ME)
slope/t, missing from the OCR). **Table VI 78/81 pass** — all 63 FM cells
pass; the 3 failures are NYSE benchmark Means (EW full 1.15 vs 0.97, EW
63–76 0.97 vs 0.77, VW 63–76 0.65 vs 0.56; 15% tolerance).

**Facts / flags (for Replicator judgment, no methodology changed):**

1. ⚠️ **The paper's Table III β cells R8–R11 are internally inconsistent
   with its own R1/R3, and our results match the paper's prose.** The printed
   β t-stats for R8–R11 (−2.06, −3.06, −2.47, −2.47) imply time-series SDs of
   the monthly β slopes of ≈0.96–1.11 %/mo, while R1 (0.15, t 0.46) and R3
   (−0.37, t −1.21) imply SDs ≈5.9/5.6 — ours are 6.0/5.5 (match). Adding
   controls cannot compress the monthly β-slope dispersion ~6× (ours move
   6.0→5.1 across R1→R10), and neither a time-series nor a pooled
   (mean ÷ avg monthly SE ≈ 0.87–0.99) t-stat on our monthly β slopes reaches
   |t| > 2. The paper's prose (L1159: β slopes in the combined regressions
   are "typically less than 1 standard error from 0") matches our R8–R11 β
   t-stats (0.39, 0.58, −0.55, 0.69). Our R1/R3/R10 β MEANS track the paper
   (0.07/0.15, −0.39/−0.37, −0.15/−0.13). 8 of the 22 Table III failures are
   R8–R11 β slope/t cells against OCR targets that cannot be reconciled with
   the paper's own R1/R3; R1 β (0.07 vs 0.15, 52%) is a genuine vintage-level
   gap, same sign, half the magnitude.
2. **E(+)/P runs systematically +0.7..+1.1 above the paper** in R9–R11
   (4.17/2.99, 1.59/0.87, 2.22/1.15) while the time-series SDs track the
   paper's implied SDs (≈12–18); the E/P dummy moves with it (small slopes,
   near-zero paper targets → large relative deviations). The qualitative
   result replicates: E(+)/P collapses once size and BE/ME enter
   (R6 5.55 (5.46) → R10 1.59 (2.44)) and the E/P dummy is killed
   (R10 −0.21, t −1.41). Consistent with the iteration-2 accounting-ratio
   vintage shift (our ln(A/ME)/ln(A/BE) higher, ln(BE/ME) less negative).
3. **All non-β, non-E/P cells of Table III replicate tightly**: R2
   −0.14 (−2.47)/−0.15 (−2.58); R3 ln(ME) −0.17 (−3.29)/−0.17 (−3.41);
   R4 0.49 (5.54)/0.50 (5.71); R5 0.48 (5.44), −0.66 (−6.56)/0.50 (5.69),
   −0.57 (−5.34); R7 −0.11 (−1.92), 0.34 (4.20)/−0.11 (−1.99), 0.35 (4.44);
   R8 ln(A/ME) 0.43 (5.41)/0.35 (4.32). Avg monthly N = 2,393 (paper ~2,267;
   +5.5%, iteration-1 vintage fact).
4. **Table VI FM regressions: 63/63 pass**, incl. reg(b) β subperiod slopes
   0.08 (0.20) / −0.48 (−1.30) vs paper 0.10 (0.25) / −0.44 (−1.17), and
   stable BE/ME slopes 0.32/0.36 (reg a) and 0.31/0.32 (reg b) vs 0.36/0.35
   and 0.34/0.31; intercepts within ≤0.13.
5. ⚠️ **NYSE benchmark means run ~0.1–0.2 %/mo above the paper** (the 3
   Table VI failures, all Mean at 15% tolerance; all Stds within ≤0.13 of
   the paper's). The stock-level computation is validated against CRSP's own
   NYSE index in this extract (msia: VW mean 0.908, SD 4.456 vs our
   0.92/4.47) — the gap is a mean-level vintage shift also visible on the
   combined msi index (0.894 vs the paper's ~0.81). Benchmark conventions:
   financials INCLUDED (NYSE market benchmark, consistent with the Sort-A
   NYSE breakpoint universe); month-end PIT membership screen excludes
   mid-month delistings from that month; VW weights = prior-month-end ME.

### Iteration 5 — Tables IV & V replicated (2026-07-22)

**Built:** `src/table_4.py` + `src/table_5.py` (analysis only; imports
`LAYOUT` from `src/main.py` and the row definitions / rounding helpers from
`src/table_2.py` — no ClickHouse, no pipeline re-run; reads
`data/panel.parquet` and, for Table V's margins, `data/agg_portfolio_returns.
parquet`). `results/table_4.md` (Panels A 12-col BE/ME + B 13-col E/P, 9 rows
each, 2-decimal rounding, Firms integer; cell-by-cell comparison blocks +
overall summary + flags) and `results/table_5.md` (full 11×11 matrix + All
row / All column / Small-ME row / Large-ME row comparison slices + full
121-cell appendix + headline spreads + flags). Table V construction exactly
per spec: interior 100 cells from stock-level monthly means within (month,
size_beme); "All" column reuses the Table I size_1..size_10 agg series;
"All" row computed at stock level per (month, BE/ME group = second component
of the size_beme label); All/All from the 'grand' series. Identity
ln(A/ME)−ln(A/BE)=ln(BE/ME) holds to 1.4e-16 across all 25 Table IV cells;
every Table IV portfolio and all 100 Table V cells exist in all 330 months.

**Results: Table IV 199/225 targeted cells pass** (Panel A 92/108,
Panel B 107/117; tolerances Return 25%, β 15%, ln-ratios 10%, E/P rows 30%,
Firms 20%). Row pass rates: Return 24/25, β 25/25, ln(ME) 25/25, ln(A/BE)
25/25, E/P dummy 25/25, E(+)/P 24/25, Firms 23/25, ln(BE/ME) 17/25,
ln(A/ME) 11/25. **Table V 110/121 pass** (25%): All row 11/11, All column
11/11, Large-ME row 11/11, Small-ME row 10/11, interior 89/100.

Headline results replicate — Panel A Return monotone 0.41→1.79 (paper
0.30→1.83; spread 1.39 vs 1.53); β U-shape 1.36→1.26→1.35 (paper
1.36→1.27→1.35, all 12 within ≤0.019); ln(ME) monotone 4.58→2.57 (paper
4.53→2.65); Panel B U-shape 1.25 (port 0) → 0.83 (port 2) → 1.70 (10B)
(paper 1.46→0.93→1.72); portfolio 0 E/P dummy = 1.00, E(+)/P = 0.00 exactly;
Table V within-decile spread 0.84%/mo (paper 0.99) and size spread 0.61
(paper 0.58); All/All 1.19 (paper 1.23).

**Facts / flags (for Replicator judgment, no methodology changed):**

1. ⚠️ The 26 Table IV failures are the same Compustat-vintage shift as
   iterations 2–3: ln(A/ME) 14 + ln(BE/ME) 8 (our ln(BE/ME) less negative,
   ln(A/ME) higher, largest at portfolios with few stocks), plus Firms 1A/1B
   (123/123 vs 89/98, composition), Return 1A (0.41 vs 0.30, low-BE/ME
   extreme, +0.11pp) and E(+)/P 1A of Panel B (0.016 vs 0.010, both ≈0).
   ln(A/BE) — the pure accounting ratio — passes 25/25, and the per-cell
   ln(A/ME) and ln(BE/ME) gaps are identical to machine precision, so the
   shift is a December-t−1 ME-level / composition difference, not the A/BE
   data. Our valid-return member counts (119–240/mo in Panel A) also exceed
   the paper's 89–239, so the Firms gap is not a counting-convention artifact
   (membership vs valid-return); our bins are exactly uniform (~246/decile)
   because breakpoints are December-cross-section quantiles and membership is
   fixed within the firm-year, so the paper's 209–239 count gradient is not
   reproduced — reported as fact.
2. ⚠️ 7 of Table V's 11 failures are in the Low-BE/ME (within-decile growth)
   column of the small/mid size deciles — the thinnest cells (e.g. ME-3×Low
   0.22 vs 0.56; ME-5×2 1.05 vs 0.65), where the extract's ~5.5% extra firms
   and different link table move the EW mean most; the remaining 4 are
   isolated interior cells (ME-2×3, ME-3×2, ME-3×8, ME-4×3), each 27–29%
   relative on paper values 0.65–1.06. Both margin dimensions and the
   Large-ME row pass 11/11.
3. Table V's "All" row/column are stock-level by construction (not means of
   the decile cells / series), per the spec and iteration 2's finding that
   stock-level grand EW ≠ simple mean of the 100 cells.

### Iteration 6 — Plots + consolidated per-cell evaluation (2026-07-22)

(Retroactive entry — the plots/evaluation worker delivered its report but
did not append this entry; backfilled by the Replicator.)

**Built:** `src/plots.py` → five paper-faithful figures in `results/`
(size_effect.png: decile EW means 1.48→0.87; beme_effect.png: 0.41→1.79;
size_beme_heatmap.png: full 10×10 matrix; cumulative_portfolios.png:
Small ×57 / Large ×12.2 and High BE/ME ×92.9 / Low BE/ME ×4.7 over 330
months; fm_slopes_rolling.png: rolling 60-month FM slopes, β ≈ 0, ln(ME)
negative, ln(BE/ME) positive throughout). `src/evaluate.py` →
`results/evaluation_summary.md`: recomputes all six tables from the data
artifacts (no markdown parsing) and classifies every cell against the 780
unique targets.

**Results:** Tier 1 = 692/780 (88.7%), Tier 2 = 86, FAIL = 2 (both Table
III R11 E/P dummy — sign flips on a null coefficient, |t| < 0.6 both
sides), SKIP = 280 (computed cells with no OCR target). Tier-2 citations:
vintage-composition 69, boundary-near-zero 10, ocr-inconsistent 7.

**Flags (adjudicated by Replicator):** (1) near-zero threshold unified at
|paper| ≤ 0.05 for tier decision and citation (my spec's ±0.02 / <0.05
were inconsistent; under the literal 0.02 rule two extra near-zero
ln(A/ME) cells would be FAIL — documented, accepted). (2) ocr-inconsistent
override extended to the R8–R11 β slopes as well as t-stats (7 cells),
per the iteration-4 documentation that the printed cells contradict the
paper's prose and R1/R3 SDs; audit 1 independently confirmed this.
(3) Composition-driven Return cells folded into vintage-composition.
Status: resolved (audit 1 verified every count independently).

### Iteration 7 — January-seasonality corollary [M1] + Tier-2 2× bound [m1] (2026-07-22)

Short finishing iteration following audit 1 (verdict PARTIAL 4.08/5; 0 blockers,
1 actionable major [M1], minor [m1]). **Methodology frozen** — NO table
computation changed; the two changes below are an additive corollary artifact
and a tier-rule clarification. Per-table Tier-1 counts re-verified unchanged at
107/168/30/199/110/78 (692 total).

**[M1] January-seasonality corollary for the ln(BE/ME) slope (paper L2186)**

- **Diagnosis:** the paper's paragraph-level January-seasonality corollary
  (`inputs/content.md` L2186: the average January ln(BE/ME) slopes are about
  twice those for February–December; the Feb–Dec slopes are about 4 standard
  errors from 0 and within 0.05 of the whole-year mean) was never computed or
  surfaced in `results/` — the plots iteration prioritized the five figures
  (audit [M1]). The auditor independently verified it HOLDS in
  `data/panel.parquet` (Jan 0.606, Feb–Dec 0.318 t 3.85, full-year 0.341, gap
  0.024; audit spot-check 11).
- **Next fix:** created `src/table_6_january.py`, importing `prewinsorize` +
  `fm_monthly` + `ts_stats` from `src/table_3_6.py` (same monthly
  0.005/0.995 winsorization; same reg(a) = ret ~ ln(ME) + ln(BE/ME)
  specification; plain monthly OLS; plain time-series t, NO Newey-West). Reads
  only `data/panel.parquet` (no ClickHouse). Split the 330 reg(a) ln_bm slopes
  into January (27 months) vs February–December (303 months); report each
  group's mean + t-stat, the full-year mean, and the gap |full-year − Feb–Dec|.
  Wrote `results/table_6_january.md` (decomposition + three-way comparison +
  per-claim-element PASS/FAIL with the L2186 citation) and added the corollary
  to the headline-results section of `results/evaluation_summary.md`, citing
  L2186.
- **Before metric:** no January corollary artifact; absent from all of
  `results/` ([M1]).
- **After metric:** January 0.606 %/mo (t 1.67, N 27); February–December
  0.318 %/mo (t 3.85, N 303); full year 0.341 %/mo (t 4.20, N 330).
  Jan/Feb–Dec = 1.91 (≈ 2× → PASS); Feb–Dec t = 3.85 (≈ 4 SE → PASS);
  |full-year − Feb–Dec| = 0.024 (< 0.05 → PASS). **3/3 claim elements PASS**;
  reproduces the auditor's independently verified values to rounding.
- **Status:** RESOLVED.

**[m1] Tier-2 2× magnitude bound**

- **Diagnosis:** the Tier-2 rule in `src/evaluate.py` did not enforce the 2×
  magnitude bound of audit spot-check 10 — three same-sign Tier-2 cells exceed
  2× of the paper on near-null targets (R9 E/P dummy slope 0.289 vs 0.06 =
  4.8×; R9 E/P dummy t 1.36 vs 0.38 = 3.6×; R11 E(+)/P t 3.19 vs 1.57 = 2.0×).
  ⚠️ **Spec concern:** the task stated all three flagged cells have
  |paper| ≤ 0.10, but only the R9 E/P dummy *slope* (0.06) does — the two
  t-stat cells have |paper| = 0.38 and 1.57, so the task's single
  |paper| ≤ 0.10 exception does NOT by itself cover them.
- **Next fix:** added the 2× bound to `classify()`: after the
  sign-reversal/near-zero/OCR logic determines TIER2, a same-sign cell that is
  not near-zero, has |paper| > 0.10, is not a documented near-null target, and
  has |ours/paper| > 2 is reclassified FAIL. Documented the near-null exception
  (|paper| ≤ 0.10) and added the audit-verified `NEAR_NULL_TARGETS` set (R9 E/P
  dummy, R11 E(+)/P — the E/P coefficients the paper shows are killed) so all
  three flagged cells stay Tier-2 as the task requires (precedent: the
  `OCR_BETA_T_SPECS` hardcode). Cited the exception in the flags section of
  `evaluation_summary.md`, including the threshold discrepancy.
- **Before metric:** Tier-1 692 (107/168/30/199/110/78), Tier-2 86, FAIL 2;
  three same-sign cells exceed 2× but were unflagged by the tier rule.
- **After metric:** counts **unchanged** — Tier-1 692 (107/168/30/199/110/78),
  Tier-2 86, FAIL 2. All 86 Tier-2 cells comply with the 2× bound (the only
  same-sign cells beyond 2× are the near-null targets, which are excepted).
  Note for the Replicator: the literal |paper| > 0.10 → FAIL rule (without the
  `NEAR_NULL_TARGETS` set) would move the two t-stat cells to FAIL (Tier-2 84 /
  FAIL 4) — documented in the flags; no claim is affected either way (they are
  noise on a null).
- **Status:** RESOLVED (threshold discrepancy flagged for the Replicator).

