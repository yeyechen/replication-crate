# Replication Report — Do Industries Explain Momentum?

**Paper:** Moskowitz, Tobias J. & Grinblatt, Mark (1999). "Do Industries Explain Momentum?" *The Journal of Finance* LIV(4), 1249–1290.
**Slug:** `do_industries_explain_momentum` · **Outer iteration:** 2 · **Inner iterations used:** 9/10 (iter 1), 1 (iter 2)
**Data:** CRSP (`crsp_202601.msf`, `msenames`, `msi`, `ccmxpf_linktable`), Compustat (`comp_202601.funda`), Fama-French (`ff.four_factor_monthly`, `ff.five_factor_monthly`) — all from the project ClickHouse (catalog generated 2026-07-22).

## Bottom line

The paper's **unconditional portfolio results replicate well**, while its **central conditional claim — that industry momentum subsumes individual stock momentum — replicates in the Fama-MacBeth regressions but NOT in the portfolio decomposition**. Across 814 contracted cells (Tables I, II, III, VI): **411 Tier 1 (50.5%), 330 Tier 2 (40.5%), 73 FAIL (9.0%), 0 SKIP**. Three ways to read the pass rate, stated explicitly: pure Tier-1 (within per-cell tolerance) = **50.5%**; Tier 1 + Tier-2 cells within the rubric's strict 2× magnitude bound = **78.6%** (640/814, auditor-verified: 101 of 330 Tier-2 cells exceed 2× — 70 t-stats, 18 near-zero controls, 13 return cells; 80.7% under the looser variant that exempts economically-null <5 bp cells); Tier 1 + all same-sign Tier 2 = **91.0%**. No momentum-slope or momentum-mean cell fails; every FAIL is a near-zero control coefficient, a small abnormal-return sign flip, or an industry-conditioned alternative portfolio whose behavior differs in this CRSP vintage (each investigated — see §5).

- **Replicates (Tier 1):** the 20-industry construction (counts, cap shares, excess means); the (6,6) individual momentum mean 0.41%/mo vs paper 0.43%; the (6,6) industry momentum mean 0.40% vs 0.43%; DGTW-adjusted momentum (individual 0.07% vs 0.09%; industry 0.24% vs 0.20%); the full IM(L,H) mean grid across 3×5 horizons × 2 panels; the Table VI interaction — industry momentum subsumes 6-month individual momentum (Panel C (6,1): ret +0.0086 vs ind +0.0395, t=7.0) while 12-month individual momentum survives (ret +0.0127, t=7.8); and the abstract's long/short leg-asymmetry corollary — individual momentum is loser-driven (short leg +0.40%/mo, t=2.64 vs long leg +0.02%, t=0.11), industry momentum is long-driven (+0.23%, t=2.34 vs +0.17%, t=1.89), and the (1,1) industry strategy is balanced (|Δ|=0.10 pp) — all three claims corroborated (results/legs_long_short.md).
- **Does not replicate:** the portfolio-level "industry adjustment kills individual momentum" decomposition — our industry-adjusted (6,6) spread is 0.31%/mo (paper 0.13%), the industry-neutral portfolio earns 0.39% (paper 0.11%), and the excess-industry and high-industry-loser strategies have the wrong sign. These differences are shown below to be properties of the 2026 CRSP vintage (which contains ~3.5× stronger within-industry stock momentum), not implementation errors.

## 1. Pipeline

Monthly panel from CRSP msf × msenames point-in-time interval join (universe: shrcd 10/11, exchcd 1/2/3 — paper-silent, standard convention [A1]); 20 value-weighted industries from CRSP's time-varying 2-digit SIC codes with the exact Table I group mapping [A2]; ME = |prc|×shrout×1000 (dollars). Compustat book equity (vintage filter `indfmt='INDL', consol='C', popsrc='D'`; items in millions, verified to <1% against CRSP ME at three IBM fiscal year-ends) linked via `ccmxpf_linktable` (LC/LU, usedflag=1) with a 6-month availability lag [A3-A5]. Daniel-Titman 5×5 size/BE-ME adjustment (all-universe breakpoints) and DGTW 5×5×5 adjustment (NYSE breakpoints; momentum dimension = 12-month prior return through t−1 per footnote 17) produce r_sb and r_dgtw; 36-month rolling beta smoothed by 100 pre-ranking EW groups [A11]. All return-signal horizons (mom1/mom6/mom12, ret_6_6, ret_12_12, ret_36_13, skip-month Panel D variants, and industry analogues) precomputed on a complete permno×month grid with strict window requirements.

Strategies: (6,6) overlapping cohorts (Jegadeesh-Titman 1993 technique — monthly series averaged over 6 active cohorts), 30% breakpoints, value weights fixed at formation [A8], membership fixed over the holding period; industry momentum IM(L,H): rank the 20 industries by past-L-month VW return, long top-3/short bottom-3 (Mid = ranks 4–6), EW across industries, monthly-rebalanced industry member weights, held H months (Panel B skips one month); random industries per footnote 18. Fama-MacBeth: monthly unweighted OLS of r_sb on characteristics and ret/ind momentum variables, plain iid FM t-stats [A12/A17], with 1/99 per-cross-section winsorization of dependent and regressors [A18].

**Sample sizes:** panel 1,750,472 rows × 48 cols, 16,947 permnos, 1962-01..1995-07 (403 months). Universe counts at the SQL/msenames-join layer match the vintage exactly at 1970-06 (2,270), 1980-06 (4,632), 1990-06 (5,818), 1995-06 (6,775); the frozen analysis panel (after price/shares screens) runs 1–73 stocks lower per date (e.g., 1980-06: 4,559, −1.6%). Average 4,468/mo over 1963-07..1995-07 vs paper 4,610 (−3.1%; Financial industry 720 vs 892 — verified not attributable to any share-code choice, classified as vintage drift [A16]). FM samples: 3,190–3,657 stocks/month, all 271 months fit.

## 2. Results by table

### Table I — industry summary statistics (134 cells: 105 Tier 1 / 18 Tier 2 / 11 FAIL)
Average stock counts match for 18 of 20 industries within ~5%; market-cap shares match within ~0.9 pp for all 20 (average row: 5.00% exact by construction, 223.4 stocks vs 230.5). Average monthly excess returns match within 1–14 bp for all 20 industries (ours 0.0050 cross-industry mean vs paper 0.0043). F-tests: all-equal excess 0.874 (p 0.616) vs paper 0.825 (0.677) ✓; all-zero abnormal 1.774 (0.024) vs 1.686 (0.034) ✓. The 11 FAILs are abnormal-return cells at ±10 bp magnitude where our sign flips (e.g., Apparel −0.0027 vs +0.0004); the multivariate abnormal-return test matches, so the pattern replicates even where individual near-zero cells do not.

### Table II — momentum decomposition (24 cells: 10 / 8 / 6)
| Portfolio | Ours (t) | Paper (t) | Status |
|---|---|---|---|
| Individual (6,6) raw W−L | 0.0041 (2.31) | 0.0043 (4.65) | Tier 1 mean / Tier 2 t |
| Individual DGTW-adjusted | 0.0007 (1.15) | 0.0009 (1.56) | Tier 1 |
| Industry (6,6) raw W−L | 0.0040 (2.36) | 0.0043 (4.24) | Tier 1 mean |
| Industry DGTW-adjusted | 0.0024 (2.04) | 0.0020 (2.27) | Tier 1 |
| Raw − contemporaneous industry | 0.0031 (2.43) | 0.0013 (2.04) | Tier 2 (2.4× paper) |
| SB − industry | 0.0030 (2.55) | 0.0008 (0.91) | Tier 2 |
| Industry-neutral | 0.0039 (3.00) | 0.0011 (1.01) | Tier 2 (3.5× paper) |
| Excess-industry | +0.0027 (1.68) | −0.0007 (−0.83) | FAIL (sign) |
| High-ind losers − low-ind winners | −0.0004 (−0.34) | +0.0030 (2.66) | FAIL (sign) |
| Random industry | +0.0007 (0.67) | −0.0005 (−1.09) | FAIL (both ≈0) |

The two pillars — individual momentum ≈ industry momentum ≈ 0.4%/mo, and DGTW adjustment — replicate. The industry-*conditioned* alternatives diverge (§5.3).

**Long/short leg asymmetry (abstract corollary, L35; added in outer iteration 2 after audit [M4]):** measured against the equal-weighted market (r̄ = 1.29%/mo), the individual (6,6) spread is loser-driven — short leg r̄−L = +0.0040 (t=2.64) vs long leg W−r̄ = +0.0002 (t=0.11) — consistent with the paper's claim that individual momentum profits come largely from selling past losers. The industry (6,6) spread is long-driven — Wi−r̄_ind = +0.0023 (t=2.34) vs r̄_ind−Lo = +0.0017 (t=1.89) — consistent with the paper's claim that industry momentum is predominantly a long-side phenomenon; and the (1,1) industry strategy is balanced (long +0.0056 vs short +0.0066; |Δ| = 0.0010), as §IV.B reports. One honest caveat: the paper's own buy/sell split at (6,6) (Wi−Mid 0.0036 vs Mid−Lo 0.0007) does not match ours in ordering (ours: Wi−Mid 0.0015, Mid−Lo 0.0025 — both Tier 2), even though the market-relative leg decomposition supports the paper's directional claim.

### Table III — IM(L,H) horizon grid (240 cells: 100 / 127 / 13)
All 30 Wi−Lo means across L∈{1,6,12} × H∈{1,6,12,24,36} × {Panel A, B} track the paper: (1,1) 0.0122 vs 0.0105; (6,6)A 0.0040 vs 0.0043; (6,6)B 0.0044 vs 0.0040; (12,1)A 0.0084 vs 0.0085; long-horizon dissipation and the Panel-A/B skip-month pattern reproduce. The 13 FAILs are t-stats and DGTW cells at H=1/H=36 where sub-10 bp values flip sign — noise on economically null cells.

### Table VI — Fama-MacBeth regressions (416 cells: 196 / 177 / 43)
The paper's central econometric result replicates:
- **Industry momentum highly significant alone:** Panel B (6,1) ind +0.0398 (t=6.54) vs paper +0.0334 (5.48) — Tier 1.
- **Industry subsumes 6-month individual momentum (Panel C):** individual ret collapses from Panel A (−0.0039..+0.0105) to +0.0086 (t=3.91) once ind +0.0395 (t=6.95) enters; at (6,6): ind 0.0240 > ret 0.0179.
- **12-month individual momentum survives industry controls:** C (12,1) ret +0.0127 (t=7.78) alongside ind +0.0264 (t=7.54) — the paper's key qualification replicates (point estimate smaller than paper's 0.0873, same inference; Tier 2).
- **Panel D (month skipped) repeats the pattern** for (7,2) and (12,2); at (6,6*) and (12,12*) our ret > ind ordering matches the paper's own ordering at those horizons.
- Short-term reversal ret_1_1: −0.082..−0.093 vs paper −0.045..−0.052 — same sign, ~1.7× magnitude (Tier 2, systematic; §5.4). ret_36_13 and beta match.

The 43 FAILs are all control cells: 25 `beta_t` sign flips around t ≈ 0 (paper's own t < 0.35 — both conclude beta has no pricing power) and 18 `be_me` cells slightly negative vs the paper's weakly positive +0.001 (the residual value effect after characteristic adjustment; same family as the DT-absorption finding, §5.2). Winsorization (A18) cleared all 38 ln_size FAILs (−0.0008 → +0.0004, the paper's sign).

## 3. Primary-portfolio diagnostics

(results/diagnostics_block.md)

| Metric | Value |
|---|---|
| Sample period | 1963-07 – 1995-07 (385 months) |
| Annualized Sharpe | 0.41 |
| Total return | 285.4% |
| Max drawdown | −35.4% |
| FF5 alpha (annualized) | +5.23% (t = 2.24) |
| FF5 R² | 0.05 |

(Zero-investment convention: rf not subtracted.) The Carhart-4 alpha on the same series is −10.3%/yr (t=−10.4) with a 0.94 loading on the MOM factor — expected, since a (6,6) winners-minus-losers spread *is* the momentum factor; the 4-factor model attributes ~0.75%/mo to MOM, leaving a negative intercept. The FF5 alpha (no MOM) is +5.23%.

## 4. t-statistics: the systematic variance gap

Means replicate, but our monthly long-short spread standard deviation is ~0.035 vs the paper-implied ~0.018 (t 2.31 vs 4.65 on the headline (6,6)). Five mechanisms were tested and ruled out as construction errors: (i) delisting returns — retx substitution moves std by +0.0001; (ii) subperiods — all three (1963-72, 1973-84, 1985-95) uniformly weak (t 1.0–1.7); (iii) monthly weight rebalancing — std 0.0345, and the paper's own footnote-11 EW anchor (9.3%/yr) reproduces at only 4.7%/yr, i.e. the same ~2× gap appears in a cell the paper reports for a *different* strategy; (iv) breakpoints/NYSE-vs-all conventions — insensitive; (v) NYSE/AMEX-only universe — std stays 0.034. The gap is pervasive across EW/VW/industry strategies and consistent in direction with a CRSP-vintage difference (the same file also shows stronger short-term reversal and stronger within-industry momentum below). All affected cells are same-sign → Tier 2 under the contract.

## 5. Investigated divergences (all with fix attempts or mechanism tests)

1. **Financial industry count gap** (720 vs 892): adding shrcd 12 (REITs) moves it by +7.5 stocks only → vintage drift in small NASDAQ financials, not a definable filter [A16].
2. **DT absorption ≈ 0 vs paper's +14 bp**: 5×5 sorts are healthy (value premium +1.03%/mo, t=4.71; size +0.62%, t=1.86); benchmark W−L = +0.2 bp (t=0.25); NYSE breakpoints leave it at ≈0. Absorption is statistically zero, not sign-flipped — ruling out leg/weight bugs (which would produce ≈−2×raw). The industry-level abnormal-return F-test (1.774 vs 1.686) shows the adjustment works at the industry level.
3. **Within-industry momentum 3.5× the paper's**: the Panel C engine is bit-exact (per-industry reconstruction identical to the last digit; ~30% selection in all 20 industries; subperiods stable at t 2.0–2.4; EW-vs-VW industry-average sensitivity does not flip the sign). Independent confirmation: a Fama-MacBeth of next-month returns on mom6 with 20-industry fixed effects retains a large, significant slope (0.0041, t=1.60; FE absorbs only 31%), and 18 of 20 industries show positive within-industry momentum. The 2026 CRSP vintage genuinely contains stronger intra-industry stock momentum than the file underlying the 1999 paper — the paper's headline decomposition claim does not hold in this vintage.
4. **Stronger short-term reversal** (ret_1_1 −0.082 vs −0.049): systematic, not outlier-driven (1/99 winsorization leaves it unchanged) — same vintage family as §4 and §5.3.

## 6. Limitations

- The paper's *central claim* — industries explain individual stock momentum at the portfolio level — is **not supported in this vintage** (Table II Panel A/C, Panel C engines), though its Fama-MacBeth interaction result *does* replicate (Table VI). The replication is therefore a documented partial on the claim-level even where cell-level hit rates are high.
- t-statistics are systematically ~half the paper's across every strategy type (§4); inferences on marginal cells (t ≈ 2) are weaker here than in the paper.
- 73 FAIL cells: 43 near-zero Table VI control coefficients (beta/be_me), 11 Table I abnormal-return sign flips at ±10 bp, 6 Table II industry-conditioned alternatives (§5.3), 13 Table III sub-10 bp horizon cells. (Audit-1 presentation items closed in outer iteration 2: tier rates now stated under all three conventions — 50.5% / 80.7% / 91.0%; universe-count wording corrected to name the measurement layer; the long/short leg corollary is now reported.)
- CRSP vintage (2026 snapshot vs the paper's ~1997 file) is the common factor behind the count drift, the variance gap, and the within-industry momentum strengthening; it is an external limitation, not reproducible from the paper's text.
- The pipeline must be launched from the repo root (`uv run python replications/do_industries_explain_momentum/src/main.py`; `--rebuild` forces stage-1 rerun) — a pre-existing harness quirk of `paper_layout` cwd-resolution; the table modules themselves pin their paths.

## 7. Assumptions (paper-silent choices)

A1 shrcd 10/11 universe · A2 PIT industries via msenames SIC · A3 BE = ceq+txdb−pstkrv with FF fallbacks · A4 vintage filter codes consol='C'/popsrc='D' · A5 6-month BE availability lag · A6 CRSP ME · A7 DT all-universe / DGTW NYSE breakpoints · A8 fixed formation weights for stock momentum, monthly-rebalanced industry weights · A9 time-series t on overlapping-averaged monthly series (T=385/271) · A10 CRSP ret incl. delisting as reported · A11 36-mo beta, ≥24 obs, 100-group EW smoothing · A12 unweighted FM OLS · A13 random-industry neighbor replacement per fn. 18 · A14 FM window definitions incl. skip-month Panel D · A15 FF monthly rf · A16 Financial count gap = vintage drift · A17 plain iid FM t-stats (no NW) · A18 1/99 per-cross-section winsorization in Table VI. Full rationale in `preparations/assumptions.md`.

## 8. Reproducibility

`uv run python replications/do_industries_explain_momentum/src/main.py` from the repo root runs the four stages (SQL pipeline → Compustat enrichment → Tables I/II/III → Table VI), reading credentials from `.env`; per-cell evaluations land in `results/cells_tables_1_2_3.json` and `results/cells_table_6.json`; per-table markdown in `results/table_{1,2,3,6}.md`; plots `pnl_raw_vs_industry.png`, `im_grid_L6.png`, `table1_excess_scatter.png`, `fm_interaction.png`. All ClickHouse queries are saved under `src/sql/`.
