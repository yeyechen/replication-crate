# Assumptions Registry — Asset Growth and the Cross-Section of Stock Returns (Cooper, Gulen, Schill 2008)

This registry records **paper-silent** decisions — choices the agent had to make
that the paper does not specify. Paper-**derived** rules live in
`preparations/preprocessing_rules.json` (verbatim paper quotes). Every Stage-7
iteration appends an entry here.

---

## Assumption 1: Delisting-return treatment

**Decision:** Incorporate CRSP monthly delisting returns (`crsp_202601.msedelist.dlret`)
into each stock's monthly return at the delisting month. Where `dlret` is missing and the
delisting code (`dlstcd`) indicates a performance-related delisting (codes 500–599), substitute
−0.30; for other missing-dlret delistings use 0. Delisting returns are combined with the final
monthly holding-period return in the standard CRSP way.
**Rationale:** Paper is silent on delisting treatment (no "delist" passage in content.md; logged as
`delisting_paper_silent` in preprocessing_rules.json). The paper uses CRSP monthly returns and forms
1-year portfolios, so delisting events within the holding year must be handled to avoid upward-biased
returns (delisted stocks otherwise just stop returning data). The −0.30 performance-delisting fallback
is the standard convention (Shumway 1997; PAPER_CONVENTIONS.md "Delisting returns → Adjust").
Considered alternative: ignore delistings (treat as missing) — rejected because it biases high-growth
decile returns upward (high-growth firms delist more), mechanically widening the spread and overstating
replication quality.
**Impact:** Affects every monthly portfolio return in Table II (Panels B, C, D) and the annual returns
used in Tables III–IV. Expected to be a second-order effect on the decile spread but applied for fidelity.

## Assumption 2: Book-to-market denominator (market equity source)

**Decision:** BM denominator = market equity at the end of December of year t−1, computed from CRSP as
`abs(prc) × shrout × 1000` at the last CRSP trading day of December t−1 (in dollars), converted to
$millions. Book equity (numerator) follows Davis–Fama–French (2000): `seq + txdb − pstk` with the
preferred-stock fallback order `pstkrv → pstkl → pstk`, and `ceq + txdb − pstk` / `at − dlc − dltt − pstk`
fallbacks when `seq` is missing.
**Rationale:** The paper says price-scaled ratios "use price or market value from December of year t−1"
(preprocessing rule `sample_bm_price_timing`, L87) and the Appendix defines BM "as in Davis, Fama, and
French (2000) … ME is the price times shares outstanding at the end of December" (var_bm, L4368). It does
not state whether the December ME comes from CRSP or Compustat. CRSP December ME is the more common
implementation of "price times shares outstanding at the end of December" and is consistent with the
firm-capitalization rule that uses CRSP ME. Considered alternative: Compustat `prcc_f × csho` (fiscal
year-end) — rejected because fiscal year-ends are not generally December and would mismatch the paper's
explicit "end of December" timing.
**Impact:** Affects BM in Table I and the BM control in Tables III–V.

## Assumption 3: Compustat funda de-duplication

**Decision:** Restrict `comp_202601.funda` to one record per (`gvkey`, `fyear`) before computing any
accounting variable: keep industrial-format consolidated standard records (`indfmt='INDL'`,
`datafmt='STD'`, `consol='C'` when those columns are populated) and, if more than one row remains,
keep the row with non-null `at` (and, as a final tie-break, the latest `datadate`).
**Rationale:** Paper is silent on handling Compustat's multiple records per firm-year (different
consolidation/data formats produce duplicate `gvkey`–`fyear` rows; verified empirically — e.g. gvkey
001690 fyear 2001 has both a populated row and a NULL row). Keeping duplicates would double-count firms
in cross-sectional medians and regressions. The indfmt/datafmt/consol filter plus non-null-`at` tie-break
is the standard WRDS convention. Considered alternative: keep all rows — rejected (double counting).
**Impact:** Affects every Compustat-derived variable (ASSETG and all controls) in all four tables.

## Assumption 4: Size-group breakpoints (NYSE 30th/70th ME percentiles)

**Decision:** The small/medium/large size groups are formed each June t by computing the 30th and 70th
percentiles of June-t market equity using **NYSE-only** stocks (hexcd = 1) in the universe, then applying
those two cutoffs to **all** universe stocks.
**Rationale:** The paper states the groups use "the 30th and 70th NYSE market equity percentiles in June
of year t" (preprocessing rule `sort_size_groups`, L401). "NYSE … percentiles" means the breakpoints are
computed from NYSE stocks only (standard Fama–French convention, PAPER_CONVENTIONS.md "Breakpoint
universe → NYSE only"), then applied to the full universe. Considered alternative: percentiles of all
stocks — rejected because NASDAQ's many small caps would pull the 30th percentile down and misclassify
small firms, contradicting the explicit "NYSE" wording.
**Impact:** Affects the small/medium/large breakdowns in Table II Panels C/D and Tables III–IV Panels B–D.

## Assumption 5: Monthly Fama–French three-factor source

**Decision:** Monthly FF3 factors (Mkt-RF, SMB, HML) and the risk-free rate are taken from
`ff.four_factor_monthly` (columns `mkt_rf`, `smb`, `hml`, `rf`), dropping the momentum column `mom`.
The Carhart four-factor robustness uses the same table including `mom`.
**Rationale:** The `ff` database has no `three_factor_monthly` table — `ff.three_factor` is a DAILY file
(26,110 rows) while `ff.four_factor_monthly` is monthly (1,192 rows, 1926-07→2025-10) and contains the FF3
columns as a subset. The paper's three-factor model (Fama–French 1993) uses exactly Mkt-RF, SMB, HML, RF.
This is logged in data_verification.json (`ff_three_factor_monthly`). Considered alternative: aggregate the
daily `ff.three_factor` to monthly — rejected as unnecessary since the monthly four-factor table already
carries the identical FF3 series.
**Impact:** Affects every three-factor alpha (Table II Panels C/D) and four-factor robustness alpha.

## Assumption 6: Asset-growth decile sort uses the full universe

**Decision:** The ten asset-growth deciles are formed each June t by sorting **all** universe stocks on
ASSETG (equal-frequency deciles across the full cross-section). NYSE breakpoints are NOT used for the
asset-growth sort — they are used only for the (unreported) market-cap decile sorts and for the size groups
(Assumption 4).
**Rationale:** Footnote 7 (preprocessing rule `sort_nyse_breakpoints`, L124) explicitly reserves NYSE
breakpoints for "the market capitalization decile sorts," implying the asset-growth decile sort itself uses
the full cross-section. This is the standard convention for signal sorts (PAPER_CONVENTIONS.md "Breakpoint
universe → NYSE only … Applies only to size-based sorting; for signal-based sorting use all stocks in the
universe"). Borderline paper-derived rather than paper-silent; logged here because it is an interpretation
of which sorts the NYSE-breakpoint convention applies to.
**Impact:** Affects the decile assignments underlying Tables I, II, and the all-firms panels of III–IV.

## Assumption 7: Asset-growth upper tail / data-vintage treatment (main analysis)

**Decision:** The main analysis applies ONLY the paper's stated sample rules for ASSETG — nonzero total
assets in both FY t-1 and FY t-2 (rule `sample_assetg_nonzero_assets`, L96) plus the 2-year Compustat
backfill (rule `sample_backfill_2yr`, L87). No minimum-asset screen and no winsorization is applied to the
main portfolio sorts (Tables I and II), because in the paper those are explicitly ROBUSTNESS tests, not the
main analysis: the 1%/99% winsorization (L2592) and the $10M total-assets screen (L1570) are described as
screens whose inferences "are unchanged." For the Fama-MacBeth regressions (Table III), where a handful of
ASSETG > 10 observations exert disproportionate cross-sectional leverage, BOTH the raw specification (the
paper's main spec, target t = −6.52) and the paper's documented 1%/99% winsorization (target t = −9.47) are
estimated and reported, each compared to its corresponding paper target.
**Rationale:** The 2026 Compustat vintage contains many more small-denominator placeholder / dormant-shell
records than the paper's ~2005 vintage (e.g. a shell with FY1998 total assets of $1,000 that reactivates in
FY1999 produces ASSETG = 47,500). This fattens the ASSETG upper tail: decile-10 formation median 1.14 vs paper
0.84, and yearly cross-sectional std 28.7 (88.1 over the last 10 years) vs the paper's reported ~0.60 / ~0.95
(L114). This is a documented data-vintage difference, NOT a methodology error — three independent pieces of
evidence: (1) the lower tail and median match the paper closely (whole-sample P5 = −0.2135 ≈ paper D1 −0.2115;
median 0.0936 ≈ paper D5 0.0961); (2) the decile pattern is monotonic; and (3) most decisively, the resulting
decile portfolio returns reproduce the paper's central results almost exactly (Year-1 EW spread −1.71% vs paper
−1.73%; VW −1.03% vs −1.05%; EW perfectly monotonic across all 10 deciles). Inventing an ad-hoc denominator
floor or asset screen to force the D10 median to 0.84 would be "tweaking to fit" and is rejected; the only
screens used are the paper's own documented ones, reported as robustness. Affected cells (ASSETG D10 median in
Table I; the raw Table III coefficient) are evaluated as Tier-2 pattern matches with this vintage explanation
where they fall outside tolerance.
**Impact:** Table I ASSETG upper-tail medians (Tier 2); Table III raw ASSETG coefficient/t-stat (reported both
raw and winsorized). Tables II returns and the Table IV decomposition are essentially unaffected because the
extreme-ASSETG firms are tiny and average out in the portfolio aggregation.

## Assumption 8: Table I ISSUANCE (5-year share change) definition — REFINED to split-adjusted (audit M1)

**Decision (refined, iteration 6):** Table I `ISSUANCE` = 5-year percentage change in
**SPLIT-ADJUSTED** common shares outstanding:
`split_adj_shares[FY t-1] / split_adj_shares[FY t-5] − 1`, where
`split_adj_shares = csho × cfacshr` — Compustat `csho` at the fiscal-year-end `datadate`
multiplied by CRSP's cumulative share-adjustment factor `cfacshr` (from `crsp_202601.msf`)
attached at that datadate by `permno` through the **same PIT CRSP–Compustat link** the
foundation uses (`ccmxpf_linktable`, linkprim='P', linktype IN ('LU','LC'), usedflag=1).
The superseded raw-csho version `(csho[FY t-1] − csho[FY t-5]) / csho[FY t-5]` is retained
in `results/table_1_eval.json` (`table.ISSUANCE.raw_csho`) and each ISSUANCE evaluation
entry carries `raw_csho_value`.
**Verified split convention:** on a 2:1 split `shrout` DOUBLES while `cfacshr` HALVES, so the
product `shrout × cfacshr` is CONTINUOUS across the split — i.e. multiplying shares by
`cfacshr` REMOVES the mechanical split jump (cfacshr is a multiplier here, not a divisor).
Verified on permno 10032 = gvkey 012945 (2:1 splits 1997-08-29 and 2000-09-29):
`7246×4.0 = 28984 → 14492×2.0 = 28984` (the raw 2.01× share jump in 2000 becomes a ~0.7%
genuine change). `cfacshr` is ~99.5% populated back to 1965 (no pre-1983 gap), covering the
full sample. The cfacshr base level cancels in the 5-year ratio; only its change over the
window matters.
**Rationale:** The Table I description (var_issuance_tableI, L140) says only "ISSUANCE is a
5-year change in the number of equity shares outstanding," without specifying split adjustment.
The raw-csho version matched sign and monotonicity but ran 1.85–3.91× the paper (D1 0.148 vs
0.0803; D10 1.013 vs 0.3012; spread 0.865 vs 0.2209; t 12.11 vs 8.36) because raw `csho`
counts mechanical split-induced share increases as issuance. Split adjustment removes that
artifact: the split-adjusted magnitudes fall within ~1.5× of the paper — D1 0.0709 (0.88×),
D10 0.3921 (1.30×), spread 0.3212 (1.45×), t 7.81 (≈8.36) — so per the audit-M1 decision rule
(within ~1.5× and strictly closer than raw) the split-adjusted column is adopted as PRIMARY.
Split-adjusted coverage is 70.4% of (permno, june_year) vs 82.8% for raw (the 5-year window
needs a valid `cfacshr` in both FY t-1 and FY t-5); the t-stat IMPROVED to 7.81 (near the
paper's 8.36) despite the lower coverage. Deciles and (permno, june_year) keys are unchanged
(read from `data/formation.parquet`, not recomputed).
**Impact:** Table I ISSUANCE cells only — D1 and t(spread) move from Tier 2 to Tier 1 (tally
17/35/1/0 → 19/33/1/0); D10 and spread remain Tier 2 but with far smaller relative error
(30%/45% vs 236%/291%). NO effect on Tables II–IV (ISSUANCE is a descriptive Table I column;
the Table III/V `ISSUANCE` is the distinct Daniel–Titman log-market-equity measure,
var_issuance L4414).

---

## Assumption 9: Value-weighting uses FIXED June-t formation market equity, not same-month ME

**Decision:** All value-weighted (VW) portfolio returns are computed as
Σ(ret·w)/Σ(w) with w = the **June-t formation market equity** (MV, in $M, carried in
`data/formation.parquet` and merged into the panel on `(permno, formation_year)`), held
fixed over the 12-month holding year. The contemporaneous monthly `me` column in
`data/panel.parquet` is NOT used as the VW weight.
**Rationale:** This is paper-derived (rule `sample_me_timing`, L87: "for firm
capitalization we use the market value of the firm's equity from CRSP at the end of June
of year t") combined with the standard annual-rebalanced VW convention (weights fixed at
formation, rebalanced each July). It is logged here because the panel's `me` column is the
*contemporaneous* end-of-month market equity, so a naive `VW = Σ(ret·me)/Σ(me)` (the literal
reading of the worker task) uses same-month weights that are positively correlated with the
same-month return and bias VW returns UP by ~1.3pp/month (contemporaneous-weighted VW gives
D1 = 2.77%, D10 = 1.83%, spread −0.94% — wrong levels; June-weighted VW gives D1 = 1.47%,
D10 = 0.44%, spread −1.03%, matching the paper's 1.48 / 0.43 / −1.05 exactly). Considered
alternative: same-month `me` weighting — rejected because it reproduces neither the paper's
VW decile levels nor the standard annual-rebalance convention. EW (equal-weighted mean of
returns) is unaffected and matches the paper closely either way.
**Impact:** Every VW figure in Table II (Panels B.2, C.2, D, F). EW figures are unaffected.

---

## Assumption 10: Table III construction details (rank normalization, 5Y-window extension, NOA/A and dependent-variable missingness)

**Decision:** Four paper-silent implementation choices for Table III (src/table_3.py):
1. **5YASSETG / 5YSALESG rank normalization** (var_5yassetg L4392, var_5ysalesg L4394): each
   june_year, firms are ranked ascending by ASSETG (resp. SALESG) and scaled to [0,1] as
   `(average ascending rank − 1) / (N_year − 1)` (low growth = 0, high growth = 1; ties get
   the average rank). 5YASSETG(t) = 0.10·rank(t−5) + 0.20·rank(t−4) + 0.30·rank(t−3) +
   0.40·rank(t−2) (year t−1 OMITTED), requiring all four yearly ranks, else NaN.
2. **Rank-window extension to 1963:** the foundation's formation.parquet covers june_years
   1968–2002, but the 5-year variables at June 1968 need ranks back to 1963 — which is
   exactly why the paper's Compustat sample starts in 1963 (L73). Ranks for june_years
   1963–2002 are therefore computed at the gvkey level from the deduped funda (same
   ASSETG/SALESG formulas + 2-year backfill filter as the foundation), then mapped to
   (permno, june_year) through the foundation's PIT CRSP–Compustat link. All 35 formation
   years are covered (avg ~4,561 ranked gvkeys/yr).
3. **NOA/A missing sub-items → 0** (var_noa L4404, caption L1642): NOA = dlc + dltt + mib +
   pstk + ceq − ch at FY t−1 with missing ch/dlc/dltt/mib/pstk/ceq filled with 0 (standard
   practice; `at` must be non-missing and > 0); NOA/A = NOA / CURRENT total assets per the
   Table III caption (NOT lagged assets as in the Appendix prose).
4. **Annual dependent variable (fm_dependent_annual L1622):** prod(1+ret)−1 over the
   available months of July(t)–June(t+1); months with missing ret are skipped (0.43% of
   panel months; 7.1% of firm-years have <12 months, virtually all delistings, whose
   delisting return is already embedded in the delisting month).

**Rationale:** The paper specifies the 5-year weights and the omission of t−1 but not the
rank scaling or how to handle firms with fewer than four historical ranks; the (rank−1)/(N−1)
scaling is the standard percentile-rank convention and makes the variable comparable across
years of varying cross-section size. Considered alternatives: (a) ranks over
formation.parquet only (1968+) — rejected because it drops 1968–1972 from Models 3/7, while
the paper's 1963 Compustat start shows it had the full history; (b) NOA/A scaled by LAGGED
assets (Appendix prose) — the task spec follows the Table III caption (current assets),
implemented as specified. Missing-item zero-fill for NOA components is the convention in
Hirshleifer et al. (2004).
**Impact:** Table III Models 3, 5, 7 (M3 5YSALESG t = +0.08 vs paper −0.27 — both ≈0 and
insignificant; M5 NOA/A t = −2.28 vs −2.43 ✓; M7 5YASSETG t = −2.16 vs −2.22 ✓) and the
annual-return dependent of all Panel A models.

---

## Stage-7 iteration log

### Iteration 1 — Problem: build the analysis-ready data foundation
- Diagnosis: N/A (construction, not debug). Pipeline built end-to-end; sanity checks pass.
- Next fix: N/A — validate against Table I characteristics, then Table II returns.
- Before metric: (no prior pipeline)
- After metric: 35 formation years (1968–2002); avg 2,972 stocks/yr (1990: 2,953; 2000: 4,325); ASSETG decile medians D1=−0.182/D5=0.075/D10=1.141 (paper −0.212/0.096/0.836); Year-1 EW spread −1.713% (paper −1.73%), VW spread −1.031% (paper −1.05%); MV verified exactly vs raw CRSP.
- Status: resolved (foundation accepted). ASSETG upper-tail vintage gap diagnosed → Assumption 7.

### Iteration 2 — Problem: replicate Table I (formation-period characteristics)
- Diagnosis: N/A (first computation of Table I). Aggregation independently re-verified by hand (BHRET36 t-stat 15.55, MV-AVG D10 476.83, MV median D10 95.74, 1990 D5 ASSETG median 0.0584) — no implementation error.
- Next fix: none required — deviations are data-vintage (Assumption 7) and a definition ambiguity (Assumption 8); no methodology bug to fix. Proceed to Table II.
- Before metric: (no prior Table I)
- After metric: Tier 1 = 17, Tier 2 = 35, FAIL = 1, SKIP = 0 (of 53 cells). Matches: ASSETG monotonic; BM declining D2→D10 (0.417 D10 ≈ paper 0.426); BHRET36 spread 1.175 (paper 1.044, t 15.55 ≈ 15.65); ACCRUALS D1 −0.135 ≈ −0.125; MV D10 95.74 ≈ 85.61. Documented Tier-2 drivers: ASSETG upper tail (D10 1.14 vs 0.84), low-growth-decile level shift (D1 less negative −0.182 vs −0.212), ROA/ACCRUALS D10 shell-dilution, ISSUANCE 1.5–3× (raw csho split issue). The single FAIL is Leverage_t_spread (−1.26 vs +1.17), a noise-level sign flip on a spread that is ≈0 in both (paper spread +0.0165, ours −0.0158) — economically meaningless.
- Status: resolved (Table I accepted as a faithful methodology replication; no gaming). ISSUANCE definition logged as Assumption 8.

### Iteration 3 — Problem: replicate Table II (Year-1 returns, FF3/FF4 alphas, size groups, subperiods, annual stats)
- Diagnosis: N/A (first Table II computation). One real implementation bug caught and fixed during build: VW weighting initially used the panel's contemporaneous `me` (gave VW D1=2.77% vs paper 1.48%); switched to fixed June-t formation ME (`me_june` from formation.parquet), reproducing the paper's VW D1=1.47/D10=0.44/spread −1.03 exactly → Assumption 9.
- Next fix: none required for A–D/F. Section E (event-time Year 1–5 buy-and-hold) left not-yet-computed (needs CRSP msf through Jun 2007, outside the foundation window).
- Before metric: (no prior Table II)
- After metric: Tier 1 = 32, Tier 2 = 3, FAIL = 0, SKIP = 1 (of 36). All Year-1 raw returns (EW D1 2.02/D10 0.31/spread −1.71; VW D1 1.47/D10 0.44/spread −1.03), all FF3 alphas (EW spread −1.49; VW −0.56; size-group spreads −1.62/−0.71/−0.58 EW, −1.33/−0.56/−0.44 VW), FF4 robustness (EW −1.29, VW −0.42), consistency (EW 97%, VW 77%), annualized high-growth (VW 5.4%, EW 3.8%), and subperiods (VW 1968–80 −0.29, t −1.49) are Tier 1. The 3 Tier-2 cells: PanelA_ASSETG_year1_spread 1.32 vs 1.05 and _t 7.95 vs 15.60 (ASSETG upper-tail vintage, == Table I, Assumption 7), and VW_spread_Sharpe_annual 0.70 vs 1.07 (mean 12.4% matches but annual spread std 17.6% vs ~11.6% implied — a returns-volatility vintage effect; sign strongly positive). SKIP = EW_cumulative_Y1_5_spread (Section E). t-stat convention = Newey-West n_lags=3 (paper uses GMM/delta HAC; iid values reported alongside and are within tolerance too).
- Status: resolved (Table II accepted as a faithful methodology replication across A–D/F; no gaming). VW weight source logged as Assumption 9.

### Iteration 4 — Problem: replicate Table IV (balance-sheet decomposition Fama-MacBeth)
- Diagnosis: N/A (first Table IV computation). Components VERIFIED two ways: (1) both sum-to-ASSETG identities hold to max residual 1.1e-13 (investment) / 5.7e-14 (financing); (2) an independent recomputation from comp_202601.funda via src/sql/decomp_components.sql, mapped through the foundation's PIT CRSP-Compustat link, matches formation.parquet to max|Δ| = 0.00e+00 (every component + ASSETG, identical null pattern). So the foundation's d_* columns use the exact paper formulas (Δ FY t−2→t−1 ÷ at[FY t−2]) and the correct mapping — REUSE path taken, no recompute needed; foundation (main.py / formation.parquet / panel.parquet) left untouched. Inference imported from table_3.py (build_annual_dependent, paper_ts_stats, fm_ols) so it is byte-identical to Table III.
- Next fix: none — the slope gaps are data-vintage (below), not a construction or inference bug. No gaming.
- Before metric: (no prior Table IV)
- After metric: Tier 1 = 2, Tier 2 = 2, FAIL = 0, SKIP = 0 (of 4 committed T4 metrics). dPPE_alone_t −5.00 vs −4.80 (Tier 1), dPPE_full_t −3.93 vs −2.76 (Tier 1). dOthAssets_alone_t −0.34 vs −3.34 and dCurAsst_full_t −1.09 vs −3.74 are Tier 2 (correct negative sign, attenuated by data-vintage). Qualitative pattern fully reproduced: investment ΔPPE strongest + ΔCash insignificant; financing ΔDebt/ΔStock strong + ΔRE insignificant; size groups show ΔPPE negative/significant everywhere and ΔCurAsst/ΔOthAssets losing significance in the large group (exactly as the paper's prose states). The all-firms regression CONSTANT matches the paper almost exactly (full-investment t 5.62 vs 5.61; full-financing 5.42 vs 5.59), confirming the sample + dependent variable are correct.
- Status: resolved (Table IV accepted as a faithful methodology replication; the weaker ΔCurAsst/ΔOthAssets slopes are a documented data-vintage effect). **Refinement to Assumption 7's "Impact" re Table IV:** Assumption 7 stated the decomposition is "essentially unaffected because extreme-ASSETG firms are tiny and average out in the portfolio aggregation" — that holds for *portfolio aggregation* but NOT for Fama-MacBeth *slopes*: the poorly-measured components (ΔCurAsst `act−ch` 18% missing, ΔOthAssets residual) are attenuated in the FM cross-sectional regressions (ΔCurAsst slope ≈ −0.002 over 1991–2002, near-zero and noisy in the sparse pre-1971 cross-sections), while the well-measured ΔPPE (`ppegt` 0.5% missing) is robust (standalone t −5.00 ≈ paper −4.80; full t −3.93, or −2.81 with the Table III base filter, ≈ paper −2.76). The standalone −4.80 is attributed to ΔPPE by the paper's prose (L2658) and matches our ΔPPE (−5.00); the parsed Table IV HTML's placement of −4.80 on ΔCurAsst is not supported by our data (our ΔCurAsst standalone −2.30) — flagged as either an OCR column-alignment artifact or the same ΔCurAsst vintage difference, not asserted.

## Assumption 11: Section E event-time window + cumulative-spread construction for the committed metric

**Decision:** (a) *Return window extended to Jun-2007.* The Section E event-time
analysis pulls an extended, delisting-adjusted monthly series
(`src/sql/universe_monthly_extended.sql` + `delisting_extended.sql`,
1968-07..2007-06) with the SAME universe filter and the SAME Assumption-1
delisting adjustment as the foundation (the adjustment code is imported from
`main.py`); it is verified here to reproduce `data/panel.parquet` exactly on the
overlap 1968-07..2003-06 (1,198,633 non-NaN (permno,month) pairs bit-identical;
5,232 NaN on both sides, 0 one-sided mismatches). The paper's Figure 2 caption
(L1552) only states "July 1968 to June 2003," but the Year-1..5 cumulative for
the latest cohort (formed Jun-2002) necessarily needs returns through Jun-2007,
so the 2003 figure-2 caption is understood as the *return-averaging* end while
the cumulative statistic uses the later years. (b) *Cumulative [1,5] spread
construction.* The committed metric `EW_cumulative_Y1_5_spread` is built from the
**monthly-portfolio event-time series** (the paper's Figure 2 method, L1552): for
each fixed cohort t, decile d and event-month offset k=1..60 the within-month
EW mean / fixed-June-t-ME VW return over surviving members is computed, then
averaged across the 35 cohorts at each offset; annual = product of the year's 12
event-month means − 1; cumulative = product of the 60 event-month means − 1;
spread = D10 − D1. The committed t-stats (paper −8.63 EW / −4.25 VW) are over
the 35 cohort-level 60-month cumulative spreads.
**Rationale:** The task spec's literal formula (average each member's per-stock
annual buy-and-hold return across the cross-section, then compound those means)
produces economically meaningless decile means on the 2026 CRSP vintage — the
cross-sectional mean of per-stock annual BHRs is dominated by a handful of
sub-penny shell stocks (e.g. one +39,120% stock-year pulls a single 1995 D1
cohort's mean to +275% vs a +50% median), giving D1 ≈ +860%/yr and a cumulative
spread of −17M%. The paper's own Figure 2 caption reports average MONTHLY
returns in event time, and its −87.99% cumulative spread is necessarily
constructed from the monthly portfolio series, so the monthly-portfolio
construction is the faithful replication of the paper's metric (it yields EW
−106.5% / VW −61.9% and reproduces the paper's t-stats −10.14 / −4.71 vs −8.63 /
−4.25). Per rep-worker protocol this spec deviation is implemented AND flagged
in the report; the spec-literal variant is computed and reported alongside for
transparency, and a per-cohort annual-compounding variant (EW −112.2% / VW
−57.4%) is also reported. Considered alternative: use the spec-literal value for
the committed metric — rejected (Tier 2 by sign-only on a 5-orders-of-magnitude
error, a farcical replication of the paper's headline cumulative statistic; the
paper demonstrably did not average per-stock annual BHRs).
**Impact:** Fills the previously-SKIP `EW_cumulative_Y1_5_spread` as Tier 1
(−106.47% vs −87.99%, 21% rel error, within the 50% tol). All other Table II
sections/outputs unchanged. Foundation, panel.parquet and formation.parquet
untouched.

### Iteration 5 — Problem: replicate Table II Section E (event-time Year 1–5 cumulative spread)
- Diagnosis: N/A (first Section E computation). One spec-vs-data conflict caught
  and surfaced: the literal per-stock-annual-BHR averaging in the task spec is
  outlier-dominated on this vintage → Assumption 11; the committed metric is
  evaluated on the paper's monthly-portfolio event-time construction.
- Next fix: none — the monthly-portfolio cumulative spread reproduces the paper
  in magnitude, sign and t-stat; the residual gap (EW −106.5% vs −87.99%) is a
  combination of data-vintage (stronger Year-1 spread, same driver as Assumption 7)
  and the 5-year compounding of that spread.
- Before metric: EW_cumulative_Y1_5_spread SKIP; tally 32/3/0/1.
- After metric: EW_cumulative_Y1_5_spread **Tier 1** (−106.47% vs −87.99%, 21% rel).
  tally **Tier 1 = 33, Tier 2 = 3, FAIL = 0, SKIP = 0** (of 36). VW cumulative
  −61.91% (paper −49.67, 24.6% rel; cohort t −4.71 vs −4.25). Event-time EW
  cumulative D1 +195.9% / D10 +89.4%, VW D1 +135.5% / D10 +73.6%; monotonic
  decline D1→D10. Cohort-level cumulative spread EW mean −99.4% (t −10.14) / VW
  −54.5% (t −4.71). Overlap with foundation verified bit-exact.
- Status: resolved (Section E now computed and committed metric Tier 1; no gaming).
  Window-extension + cumulative-convention decision logged as Assumption 11.

### Iteration 6 — Problem (audit M1): Table I ISSUANCE ran 1.85–3.9× the paper (raw csho counts splits as issuance)
- Diagnosis: Table I `ISSUANCE` used RAW Compustat `csho` — `(csho[FY t-1]−csho[FY t-5])/csho[FY t-5]`
  — which counts mechanical stock-split share increases as "issuance," inflating the measure for
  split-active firms (raw D1 0.148/D10 1.013/spread 0.865/t 12.11 vs paper 0.0803/0.3012/0.2209/8.36,
  i.e. 1.85–3.91×). Assumption 8 had diagnosed this but not executed the fix.
- Next fix: compute a SPLIT-ADJUSTED 5-year share change. Verified the CRSP `cfacshr` convention on a
  documented split stock (permno 10032 = gvkey 012945, 2:1 splits in 1997-08 and 2000-09): on a 2:1 split
  `shrout` doubles while `cfacshr` halves, so `shrout×cfacshr` is continuous → `split_adj_shares = csho×cfacshr`
  REMOVES splits. Confirmed `cfacshr` is ~99.5% populated back to 1965 (no pre-1983 gap). Built
  `src/sql/issuance_split_adjusted.sql` (funda csho + cfacshr at each fiscal-year-end datadate via the SAME
  PIT CRSP-Compustat link) and `src/build_issuance_split_adjusted.py` → `data/issuance_split_adjusted.parquet`
  keyed on the IDENTICAL (permno, june_year, decile) as formation.parquet (deciles read, not recomputed).
  Wired `src/table_1.py` to use the split-adjusted column (raw retained as ISSUANCE_raw / in the eval JSON).
- Before metric: ISSUANCE raw-csho — D1 0.1482 (1.85×), D10 1.0130 (3.36×), spread 0.8648 (3.91×), t 12.11;
  all 4 ISSUANCE cells Tier 2. Table I tally 17/35/1/0.
- After metric: ISSUANCE split-adjusted — D1 **0.0709** (0.88×), D10 **0.3921** (1.30×), spread **0.3212**
  (1.45×), t **7.81** (≈ paper 8.36). All magnitudes within ~1.5× of the paper (vs raw 1.85–3.91×) →
  **ADOPT split-adjusted as primary** (audit-M1 decision rule). ISSUANCE_D1 and ISSUANCE_t_spread move
  Tier 2 → **Tier 1**; ISSUANCE_D10 (30.2% rel) and ISSUANCE_spread (45.4% rel) stay Tier 2 but with far
  smaller error (was 236%/291%). Table I tally **19/33/1/0**. Split-adj coverage 70.4% vs raw 82.8%.
  Other 49 Table I cells unchanged (byte-identical). Verified on the split stock: raw 5-yr change
  FY96→FY01 = +542% (two 2:1 splits) vs split-adjusted +60.6% (genuine issuance).
- Status: resolved (split-adjusted ISSUANCE adopted as primary; decision rule satisfied; no gaming —
  no screens/filters added, only the documented split adjustment). Assumption 8 refined accordingly.

### Iteration 7 — Problem (audit m2): latent path bug left an empty orphan tree in the slug
- Diagnosis: `src/main.py:36` used `REPO = Path(__file__).resolve().parents[2]`, which resolves to
  `rep-it-up/replications` (the WRONG root — `utils/` lives one level up). Combined with
  `utils.env.get_replications_path()` falling back to `<cwd>/replications` when run from inside the
  slug, `LAYOUT.ensure()` created an empty nested orphan tree
  `<slug>/replications/<slug>/{data,src,results,logs,inputs,preparations}` (0 files). All actual outputs
  were written to the correct locations (table_*.py resolve the slug dir from `__file__`), so results
  were unaffected.
- Next fix: set `REPO = parents[3]` (the rep-it-up project root carrying `utils/`) and pin
  `os.environ.setdefault("REPLICATIONS_PATH", str(REPO/"replications"))` so `paper_layout()` is
  cwd-independent; delete the empty orphan tree after verifying it holds 0 files.
- Before metric: orphan tree present (8 empty dirs, 0 files); `REPO` = `rep-it-up/replications`.
- After metric: orphan tree deleted (verified 0 files first). Import-resolution check run FROM INSIDE the
  slug dir (the orphan-creating scenario): `REPO = rep-it-up` (contains `utils/` ✓),
  `LAYOUT.root = <repo>/replications/<slug>` (correct slug root ✓), `data_path('formation.parquet')`
  resolves and exists ✓, `utils.*` import works ✓. No full rebuild performed.
- Status: resolved (path fixed, layout now cwd-independent, orphan removed, resolution verified).

### Iteration 8 — Problem (audit m4): committed event-time spread depended on a live ClickHouse pull
- Diagnosis: `src/table_2_event_time.py`'s `load_extended()` pulled the extended (through Jun-2007)
  delisting-adjusted return panel live from ClickHouse on every run, so the committed
  `EW_cumulative_Y1_5_spread` (−106.47%, Tier 1) was not re-derivable from `data/` alone.
- Next fix: cache the re-derivable extended delisting-adjusted panel to
  `data/event_time_returns.parquet` (permno, date, ret_adj, me; 1968-07 .. 2007-06) and make
  `load_extended()` read it if present (write-if-missing); `ym` is reconstructed from `date` on read.
- Before metric: extended panel pulled live each run; `data/` had only formation.parquet + panel.parquet.
- After metric: `data/event_time_returns.parquet` written (2,064,870 rows × 4 cols). First run (live)
  built the cache and gave EW cumulative [1,5] spread **−106.47%** (Tier 1; overlap with panel.parquet
  bit-exact, max|Δret| = 0). Second run read FROM CACHE (no live query) and reproduced **−106.47%**
  exactly, overlap still bit-exact. Foundation parquets unchanged.
- Status: resolved (committed metric now fully re-derivable from cached artifacts; reproduced from cache).

### Iteration 9 — Problem (audit M2 + m1): Tier-2 labels were looser than the auditor's 2× magnitude bound
- Diagnosis: the evaluation harness graded Tier 2 as "sign matches, outside tolerance" with no magnitude
  cap, so cells at up to 3.9× and down to 0.10× of the paper were labeled pattern-matches. Under the
  audit's strict convention (Tier 2 requires 0.5 ≤ |ours/paper| ≤ 2.0 for |paper| ≥ 0.05), 13 of the 43
  Tier-2 cells (pre-M1) exceeded the bound. This is a LABELING gap, not a results gap.
- Next fix: add a `within_2x` flag (and documented cause/subtype) to every Tier-2/FAIL cell across all four
  eval JSONs; reclassify cells outside 2× as FAIL-with-documented-cause (data coverage / vintage attenuation /
  noise-level null) or, where division-by-~0 makes the ratio meaningless, as Tier-2 subtypes
  (near-zero-target / near-zero-spread / units). Relabel Leverage_spread_10_1 → FAIL (noise-level null) [m1].
  Regenerate evaluation_summary.md with the strict tally + cause-grouped FAILs. Use the M1-updated ISSUANCE
  values (ISSUANCE_D10 1.30× and ISSUANCE_spread 1.45× are now within 2× → legitimate pattern, not FAIL).
- Before metric: tolerance tally 76/40/3/0 (post-M1); audit's pre-M1 strict estimate 74/30/15; published
  tally read as a strict-pattern claim it did not satisfy.
- After metric: **strict tally 76 Tier 1 / 33 Tier 2 (28 pattern + 3 near-zero-target + 1 near-zero-spread +
  1 units) / 10 FAIL (3 noise-level null + 5 data coverage + 2 vintage attenuation) / 0 SKIP** (119). 109/119
  sign/pattern-correct (91.6%); 117/119 correct sign. **No result value changed** — every paper/ours value
  byte-identical (asserted in src/relabel_strict.py + diff; spot-checks unchanged); only tier-classification
  metadata added. The 10 strict FAILs are all documented non-actionable causes.
- Status: resolved (honest strict-convention labeling; M2 + m1 closed; this is documentation, not a new
  paper-silent methodology decision, hence no new Assumption number). Outer iteration 2 complete; replication
  at PASS quality per audit 1. Next: auditor N=2.
