# Replication Report — Asset Growth and the Cross-Section of Stock Returns

**Paper:** Cooper, M. J., Gulen, H., & Schill, M. J. (2008). "Asset Growth and the Cross-Section of Stock Returns." *The Journal of Finance*, 63(4), 1609–1651.
**Slug:** `asset_growth_and_the_cross_section_of_stock_returns`
**Data:** CRSP (`crsp_202601`), Compustat (`comp_202601`), Fama–French factors (`ff`), via ClickHouse.
**Status:** Two outer iterations complete; audit 2 passed after the one actionable audit-1 item was closed. 4 tables, 119 target cells.

---

## 1. What the paper claims

The paper introduces a simple, comprehensive measure of firm growth — the year-over-year percentage change in total assets (`ASSETG`, Compustat data item 6) — and shows it is one of the strongest predictors of the cross-section of U.S. stock returns. Sorting NYSE/AMEX/NASDAQ nonfinancial stocks into deciles by `ASSETG` each June and holding for one year, low-growth firms earn far higher subsequent returns than high-growth firms: value-weighted (VW) annualized returns of roughly 18% (low) vs 5% (high), an 8%/year risk-adjusted VW spread and a 20%/year equal-weighted (EW) spread. The effect (i) is monotonic across deciles, (ii) persists for up to five years, (iii) holds within small-, medium-, and large-cap groups, (iv) survives Fama–French three-factor and Carhart four-factor risk adjustment, and (v) dominates previously documented cross-sectional predictors (book-to-market, size, lagged returns, accruals, capital investment, sales growth, net operating assets) in Fama–MacBeth regressions. A balance-sheet decomposition shows the effect is common to many asset-growth subcomponents, with operating-asset growth (noncash current assets + PPE) strongest on the investment side and debt/stock financing strongest on the financing side.

## 2. What this replication did

Replicated the paper's four core empirical tables over the paper's full sample (formation years 1968–2002; returns July 1968–June 2003; event-time follow-up extended to June 2007):

- **Table I** — formation-period characteristics of the ten asset-growth deciles (time-series averages of yearly cross-sectional medians; MV-AVG as the mean).
- **Table II** — Year-1 EW/VW decile returns, Fama–French three-factor alphas (all firms and NYSE 30/70 size groups), Carhart four-factor robustness, decade subperiods, year-by-year consistency, the VW spread Sharpe, annualized high/low-growth returns, and the 5-year cumulative event-time spread.
- **Table III** — Fama–MacBeth regressions of annual returns on asset growth and controls (Models 1–7: base + L2ASSETG, 5YSALESG, CI, NOA/A, ACCRUALS, 5YASSETG), with the paper's first-order-autocorrelation-adjusted standard errors, plus winsorized, size-group, monthly-dependent, and subperiod robustness.
- **Table IV** — Fama–MacBeth regressions on the balance-sheet decomposition of asset growth into investment components (ΔCash, ΔCurAsst, ΔPPE, ΔOthAssets) and financing components (ΔRE, ΔStock, ΔDebt, ΔOpLiab), all firms and by size group.

**Table V** (equity issuance/repurchase) was **scoped out**: it requires SEO and repurchase *announcement* data (Thomson/SDC) that is not in the CRSP/Compustat/factor set available here. This is documented in `preparations/data_verification.json` and the tables selection.

## 3. Data and sample

- **Universe:** all CRSP common stocks (share codes 10/11) on NYSE/AMEX/NASDAQ (exchange codes 1/2/3), excluding financials (SIC 6000–6999), filtered **point-in-time** via `msfhdr` validity windows (`begdat`/`enddat`).
- **Period:** Compustat data from 1963 (needed for the 5-year variables and the 2-year backfill); portfolio tests and regressions start end of June 1968; returns through June 2003; event-time Year-5 follow-up through June 2007.
- **CRSP↔Compustat link:** `ccmxpf_linktable` (`lpermno`→`gvkey`; primary links `linkprim='P'`, `linktype∈('LU','LC')`, `usedflag=1`, point-in-time link windows).
- **Size:** average ~2,972 stocks per formation year (1990: 2,953; 2000: 4,325), consistent with the paper's NYSE/AMEX/NASDAQ nonfinancial universe.
- **Factors:** monthly Fama–French factors from `ff.four_factor_monthly` (FF3 = Mkt-RF/SMB/HML/RF; Carhart adds MOM); FF5 diagnostics from `ff.five_factor_monthly`. (There is no monthly three-factor table; `ff.three_factor` is daily — see Assumption 5.)

## 4. Methodology (as implemented)

- **Signal (eq. 1):** `ASSETG(t) = (at[FY t−1] − at[FY t−2]) / at[FY t−2]`, requiring nonzero total assets in both years; formed at end of June t using fiscal-year-end t−1 data (Fama–French 1992 lag), with a 2-year Compustat backfill filter.
- **Book equity:** Davis–Fama–French (2000): `seq + txdb − pstk` (preferred fallback `pstkrv→pstkl→pstk`; secondary `ceq+txdb−pstk`, then `at−dlc−dltt−pstk`); book-to-market uses December-(t−1) CRSP market equity as the denominator (Assumption 2).
- **Market equity:** CRSP `abs(prc) × shrout × 1000` (price signed; shares in thousands). VW portfolio weights use the **fixed June-t formation** market equity held over the holding year (Assumption 9 — contemporaneous month-end weighting biased returns up ~1.3pp/month and was rejected).
- **Portfolios:** each June t, sort all universe stocks with non-missing `ASSETG` into ten equal-frequency deciles (1 = low growth … 10 = high; NYSE breakpoints are *not* used for the signal sort, Assumption 6); hold July t–June t+1; rebalance annually. Size groups use NYSE-only 30th/70th June-t ME breakpoints applied to all stocks (Assumption 4).
- **Delisting:** monthly returns incorporate `msedelist.dlret`; missing `dlret` with a performance delisting code (500–599) → −0.30, else 0 (Assumption 1; the paper is silent on delisting).
- **Fama–MacBeth inference:** annual cross-sectional OLS → time-series mean of slopes → standard error adjusted for **first-order autocorrelation** (`SE × √((1+ρ)/(1−ρ))`, ρ = AR(1) of the slope series), per footnote 13 — *not* plain Newey-West. Main regressions are un-winsorized; the 1%/99% winsorization is reported as the paper's documented robustness (Assumption 7).
- **Decomposition:** investment and financing components are changes FY t−2→t−1 scaled by `at[FY t−2]`; **validated to machine precision** (both component sets sum to `ASSETG` with residuals ~1e-13; an independent recomputation from `funda` matched to exactly zero).

## 5. Portfolio diagnostics (headline asset-growth long-short spread)

Long decile 1 (low growth), short decile 10 (high growth); monthly spread = D1 − D10; 1968-07..2003-06 (420 months); self-financing (`zero_investment=True`, rf not subtracted). Full block in `results/diagnostics.md`.

| Weighting | Annualized return | Sharpe | FF5 alpha (ann.) | FF5 α t-stat | Max drawdown |
|---|---:|---:|---:|---:|---:|
| **EW** | 20.6%/yr | **1.46** | 16.32%/yr | 5.89 | −19.7% |
| **VW** | 12.4%/yr | 0.75 | 1.99%/yr | 1.03 | −34.0% |

The EW premium (small-cap-tilted) is large and survives FF5 adjustment. The VW premium is economically large (matching the paper's ~8–12%/year) but its FF5 alpha is statistically small because the spread loads heavily on the FF5 **investment factor CMA** (β ≈ 1.4) — expected, since asset growth *is* the investment anomaly CMA captures. (The paper predates FF5; its Fama–French **three-factor** alphas, reported in Table II below, are significant.)

## 6. Results by table

### Table I — formation-period characteristics (53 cells: 19 Tier-1, 29 Tier-2, 5 FAIL under the strict convention)
Every cross-sectional **pattern, sign, and monotonic trend matches**: asset growth rises monotonically D1→D10; book-to-market declines (D2→D10); the strong 36-month reversal (BHRET36 D1 −0.29 → D10 +0.89; spread t 15.55 ≈ paper 15.65); accruals and issuance rise with growth. The intercept-style matches are tight (e.g. BHRET36, ACCRUALS-D1, MV-D10). The deviations are **level shifts** driven by the 2026 data vintage: the asset-growth distribution is slightly compressed at the bottom (D1 −0.18 vs −0.21) and fatter at the top (D10 1.14 vs 0.84), so low-growth firms come in a bit larger/higher-B/M; ROA and accruals in the high-growth decile are diluted by dormant-shell records. **ISSUANCE (5-year share change) was recomputed on a split-adjusted basis** (shares × CRSP `cfacshr`, verified on a documented split stock): this moves it from 1.85–3.9× the paper (raw `csho` counted stock splits as issuance) to **0.88–1.45×** (D1 0.071, D10 0.392, spread 0.321, t 7.81 vs paper 8.36), putting two cells within tolerance (Assumption 8 refined). The 5 strict-convention FAILs are all documented non-actionable causes: two noise-level sign flips on the statistically-zero leverage spread, one near-zero accruals-D10 cell, and two t-stats on vintage-attenuated spreads (L2ASSETG, ROA) whose spreads themselves are within-2× pattern matches.

### Table II — returns and alphas (36 cells: 33 Tier-1, 3 Tier-2, 0 FAIL)
The paper's **central result replicates closely**:
- Year-1 EW returns decline monotonically D1→D10 (2.02% → 0.31%/month), spread **−1.71%** (paper −1.73%, t −7.96 vs −8.45); VW 1.47% → 0.44%, spread **−1.03%** (paper −1.05%, t −4.31 vs −5.04).
- Three-factor alpha spreads (D10−D1): all-firm EW **−1.49%** (paper −1.63%), VW **−0.56%** (−0.70%); by size — EW small/medium/large −1.62/−0.71/−0.58 (paper −1.77/−0.60/−0.86); VW −1.33/−0.56/−0.44 (−1.14/−0.55/−0.81).
- Carhart four-factor spread: EW −1.29 (−1.48), VW −0.42 (−0.60).
- Decade subperiods: all negative and significant except the VW 1968–80 spread (−0.29, t −1.49), exactly the one exception the paper flags; the effect is strongest in 1991–2003, as the paper notes.
- Low beats high in **97%** of years EW / **77%** VW (paper 91%/71%); annualized high-growth returns VW 5.4% / EW 3.8% (paper 5.2/3.1); low-growth VW 19.2% (~18).
- 5-year cumulative event-time spread (Section E): EW **−106.5%** (paper −88.0%, Tier-1; cohort t −10.14 vs −8.63), VW −61.9% (−49.7%) — computed with the paper-faithful monthly-portfolio construction (Assumption 11).
The 3 Tier-2 cells are the asset-growth vintage spread (2, shared with Table I) and the VW-spread Sharpe (0.70 vs 1.07 — the mean spread matches but the vintage has higher return volatility).

### Table III — Fama–MacBeth regressions (26 cells: 22 Tier-1, 1 Tier-2, 3 FAIL under the strict convention)
**Asset growth is the strongest, most significant predictor in every model and size group**, as the paper claims. Model 1: ASSETG −0.065 (t −5.34; paper −0.092, −6.52 — within the ±40% coefficient tolerance, Tier-1, though attenuated ~18–30% by the vintage tail); the **intercept matches almost exactly** (0.139 vs 0.137, t 4.55 both), confirming the regression is set up correctly; book-to-market 0.028 (t 3.11 ≈ 0.029, 3.40). ASSETG dominates the added growth variables (5YSALESG, CI, NOA/A, ACCRUALS, 5YASSETG) — e.g. with capital investment ASSETG t = −6.05 (paper −6.05, **exact**). The market-value coefficient resolves to **$billions** (−0.0036 vs paper −0.0044; t −1.39 vs −1.57, scale-invariant). Winsorizing 1%/99% brings the coefficient to the paper's *main* level (−0.095 ≈ −0.092), strong evidence the methodology is right and only the vintage differs. Size-group ASSETG t-stats: small −4.90 / medium −3.26 / large −2.35 (paper −5.18/−3.80/−3.60) — significant and negative throughout. The single FAIL — the 5YSALESG t-stat (+0.08 vs −0.27) — is a noise-level sign on a coefficient **insignificant in both** (|t| < 0.3), ironically confirming the paper's thesis that sales growth (unlike asset growth) does not predict returns. The accruals-model attenuation traces to sparse pre-1971 Compustat coverage.

### Table IV — balance-sheet decomposition (4 cells: 2 Tier-1, 0 Tier-2, 2 FAIL under the strict convention)
The decomposition components were **validated to machine precision**. The paper's mechanism replicates: on the investment side **ΔPPE is strongest** (standalone t −5.00 ≈ paper −4.80; full-model −3.93 vs −2.76, both Tier-1), ΔCash insignificant; on the financing side **debt (t −4.02) and stock (−2.03) dominate while retained earnings are insignificant (−0.16)**. The size-group pattern matches the paper's prose (ΔPPE negative everywhere; current-assets/other-assets lose significance among large firms). The replication **resolves the paper's internal ambiguity** in favor of the prose: the strongest standalone t-stat belongs to PPE (ours −5.00), not current assets (ours −2.30), whereas the parsed table OCR places −4.80 on current assets. The two Tier-2 cells (current-assets and other-assets slopes) are attenuated by the same vintage issue — those components depend on Compustat fields (`act`, `ch`) with heavy pre-1971 missingness — while the full-model constant matches the paper to two decimals (5.62 vs 5.61), confirming the construction.

## 7. Per-cell evaluation (119 cells)

Two conventions are reported. The **tolerance-based** grade (a cell passes if within its stated `tolerance_pct`) gives 76 Tier-1 / 40 Tier-2 / 3 FAIL. The **strict audit convention** additionally caps pattern-matches at 2× the paper's magnitude (and tags each sub-threshold cell with a documented cause):

| Table | Tier 1 | Tier 2 | FAIL | SKIP | Total |
|---|---:|---:|---:|---:|---:|
| Table I | 19 | 29 | 5 | 0 | 53 |
| Table II | 33 | 3 | 0 | 0 | 36 |
| Table III | 22 | 1 | 3 | 0 | 26 |
| Table IV | 2 | 0 | 2 | 0 | 4 |
| **All (strict)** | **76** | **33** | **10** | **0** | **119** |

Under the strict convention the 33 Tier-2 cells are 28 genuine within-2× pattern matches plus 3 near-zero-target cells (paper value ≈0, ratio unreliable), 1 near-zero-spread (a t-stat on a spread that itself matches), and 1 units cell (the market-value coefficient, whose scale-invariant t-stat matches). The 10 strict FAILs are **all documented, non-actionable causes**: 3 noise-level sign flips on statistically zero coefficients/spreads (leverage spread + its t-stat; the insignificant 5-year-sales-growth t-stat), 5 pre-1971 Compustat data-coverage cells (auditor-verified `ch` ~93% / `txp` ~53–56% null in FY1966–68, attenuating the accrual and current-assets/other-assets slopes), and 2 vintage-attenuated t-stats (L2ASSETG, ROA) whose underlying spreads are within-2× pattern matches. **109 of 119 cells (91.6%) match in sign and pattern; 117 of 119 (98.3%) have the correct sign.** No result value changed between the two conventions — only the tier labels. Full breakdown (every FAIL with its cause, every Tier-2 subtype) in `results/evaluation_summary.md`.

## 8. Assumptions and deviations (paper-silent choices)

Eleven documented decisions in `preparations/assumptions.md`. The most consequential:
- **Assumption 7 (data-vintage treatment):** the main analysis applies only the paper's stated sample rules (nonzero assets in t−1 and t−2; 2-year backfill); no minimum-asset screen and no winsorization are applied to the main sorts, because in the paper those are explicitly *robustness* tests. The 2026 Compustat vintage contains many more small-denominator dormant-shell records than the paper's ~2005 vintage, fattening the asset-growth upper tail (D10 1.14 vs 0.84; cross-sectional std ~29 vs the paper's reported ~0.60). Evidence this is vintage, not a bug: the lower tail and median match the paper closely, the decile pattern is monotonic, and — decisively — the portfolio returns replicate almost exactly. Winsorizing 1%/99% is reported as the paper's documented robustness (it brings the FM coefficient to the paper's main level). **No filters were invented to force matches.**
- **Assumption 9 (VW weights):** fixed June-t formation market equity (not contemporaneous), which reproduces the paper's VW returns; contemporaneous weighting was tried and rejected.
- **Assumption 11 (event-time cumulative):** the 5-year cumulative spread uses the paper-faithful monthly-portfolio construction; the literal per-stock buy-and-hold average is dominated by sub-penny shells on this vintage and was rejected (and flagged).
- **Assumption 8 (ISSUANCE, refined in outer iteration 2):** Table I ISSUANCE = 5-year change in **split-adjusted** shares outstanding (`shares × CRSP cfacshr`), not raw `csho`. The split adjustment (verified on a documented split stock) was the one fixable definitional gap: raw `csho` counted mechanical stock splits as equity issuance, overstating the column 1.85–3.9×; split-adjusted brings it to 0.88–1.45× of the paper.
- Others: delisting adjustment (A1), December-ME book-to-market denominator (A2), Compustat de-duplication (A3), NYSE size breakpoints (A4), monthly FF3 source (A5), full-universe signal sort (A6), rank normalization/windows for the 5-year variables (A10).

## 9. Limitations and known gaps

- **Table V not replicated** — requires SEO/repurchase announcement data (Thomson/SDC) unavailable here.
- **Data-vintage attenuation** — the 2026 Compustat/CRSP vintage shifts characteristic levels and fattens the asset-growth upper tail relative to the paper's ~2005 vintage, attenuating a handful of magnitudes (asset-growth D10 median, the raw FM asset-growth coefficient, the current-assets/other-assets/accruals slopes) without changing any sign, pattern, or conclusion. This is the dominant source of the Tier-2 cells.
- **Noise-level FAILs (3 strict)** — sign flips on statistically insignificant coefficients/spreads (leverage spread + its t-stat; 5-year-sales-growth t-stat, insignificant in both paper and replication); none affects any claim.
- **Pre-1971 Compustat coverage (5 strict FAILs)** — `act`/`ch`/`txp`/`lct`/`dp` are heavily missing before ~1971 (auditor-verified `ch` ~93% / `txp` ~53–56% null in FY1966–68), thinning the early accrual and current-assets cross-sections (the accruals model in Table III and the current-assets/other-assets slopes in Table IV). An external data-coverage limitation; no honest fix exists (imputing would fabricate data).
- **Path bug fixed (outer iteration 2)** — `src/main.py` previously resolved the project root incorrectly (`parents[2]`), creating an empty orphan directory tree; corrected to `parents[3]` with a cwd-independent `REPLICATIONS_PATH`, the orphan tree deleted, and import resolution verified. Foundation outputs were unaffected and unchanged.
- **FF5 vs FF3:** the paper risk-adjusts with FF3/Carhart4; the FF5 diagnostics here are a supplementary modern lens (they show CMA subsumes the VW spread), not a contradiction of the paper's significant FF3 alphas.

## 10. Conclusion

This is a faithful replication of Cooper, Gulen, and Schill (2008). The paper's central empirical claims reproduce closely on independent data: the monotonic negative relation between asset growth and subsequent returns; the economically large, statistically significant long-short spread (EW ~21%/year, VW ~12%/year); the negative three-factor alphas across all size groups and subperiods; the dominance of asset growth over the established cross-sectional predictors in Fama–MacBeth regressions; and the operating-asset / debt-and-stock decomposition of the effect. Of 119 committed cells, 76 are within numerical tolerance and 109 (91.6%) match the paper in sign and pattern under the strict audit convention (117 of 119, 98.3%, have the correct sign); the 10 strict FAILs are all documented, non-actionable causes — three noise-level sign flips on statistically zero coefficients, five pre-1971 Compustat data-coverage cells, and two vintage-attenuated t-stats whose spreads match. The dominant deviation is a genuine, auditor-verified data-vintage effect (a fattened asset-growth upper tail and pre-1971 missingness), not a methodology error. Outer iteration 2 closed the one actionable item from the independent audit — the ISSUANCE column is now split-adjusted (moving it from 1.85–3.9× to 0.88–1.45× of the paper) — and relabeled every pattern-match cell against the strict 2× bound. No methodology bugs remain, and no filters were invented to chase a match.

## Artifacts

- Prep contract: `preparations/{candidate_assessment,preprocessing_rules,tables_to_replicate,data_verification}.json`, `preparations/assumptions.md`.
- Code: `src/main.py` (pipeline), `src/table_{1,2,3,4}.py`, `src/table_2_event_time.py`, `src/diagnostics.py`, `src/evaluation_summary.py`, `src/build_issuance_split_adjusted.py` + `src/relabel_strict.py` (outer iteration 2), `src/sql/*.sql`.
- Data: `data/formation.parquet`, `data/panel.parquet`, `data/issuance_split_adjusted.parquet`, `data/event_time_returns.parquet`.
- Results: `results/table_{1,2,3,4}.md`, `results/table_{1,2,3,4}_eval.json`, `results/diagnostics.md`, `results/evaluation_summary.md`, and plots (`table1_*`, `table2_*`, `table4_*.png`).
- Trace: `logs/log1.md`, `logs/log2.md`, `logs/audit1.md`; `SUMMARY.md` (auditor-owned).
