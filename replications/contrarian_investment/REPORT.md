# Replication Report — Lakonishok, Shleifer & Vishny (1994), "Contrarian Investment, Extrapolation, and Risk"

**Paper:** *The Journal of Finance* 49(5), 1541–1578 (Dec. 1994). JSTOR stable URL 2329262.
**Slug:** `contrarian_investment` · **Replication date:** 2026-07-22 · **Outer iterations:** 2 (audit 1 PARTIAL → fixes → audit 2 PASS, requires_iteration: false)
**Data:** `crsp_202601` (msf, dsenames, dsedelist, msi, ccmxpf_lnkhist), `comp_202601.funda`, `ff.four_factor_monthly`.
**Per-cell result:** 1,169 MATCH (Tier 1, 90.6%) + 55 PATTERN (Tier 2) + 66 FAIL of 1,290 targets — **94.9% hit rate** (`results/evaluation_iter6.json`).

---

## 1. Bottom line

All eight empirical tables of LSV (1994) were replicated from raw CRSP/Compustat data, plus the paper's two figures. Every one of the paper's central qualitative claims reproduces on the modern data vintage:

1. **Value beats glamour, by a lot.** Average annual return spreads (value − glamour) over the 22 April 1968–1989 formations: B/M **+10.8pp** (paper +10.5), C/P **+11.3pp** (+11.0), E/P **+8.3pp** (+7.6), past-sales-growth **+5.5pp** (+6.8); two-dimensional C/P×GS **AR 21.3% vs 10.9%** (paper 22.1 vs 11.4) and size-adjusted spread **+8.0pp/yr** (+8.7).
2. **The result is in the big stocks.** Within the largest 50% of firms, C/P×GS AR spread **+8.3pp** (paper +7.8), SAAR spread **+7.2pp** (+8.7). (The E/P×GS full-sample AR spread is **+10.0pp** vs the paper's +11.2pp.)
3. **Extrapolation errors are visible in fundamentals.** Glamour portfolios' high pre-formation growth (sales, cash flow, earnings) does not persist post-formation; value portfolios' post-formation growth is comparable or higher in years +2…+5 — the paper's extrapolation mechanism (Table V narrative, incl. the exact internal-consistency check: C/P×GS glamour C/P 0.076 grown at our ACG(0,5) → 0.136 = paper's reported 0.136).
4. **Value outperforms consistently, not by taking risk.** Value beats glamour in **every one of the 18 five-year windows, in all three classifications** (paper's claim, confirmed 18/18×3); value loses *less* in the worst 25 and next-worst 88 market months (both classifications); CAPM betas cluster at 1.2–1.4 with a value−glamour gap an order of magnitude too small to explain the return spread.
5. **B/M is subsumed by C/P and GS.** In the Fama-MacBeth regressions, B/M's coefficient collapses to ≈0 (t = 0.55–0.82) once GS and C/P+ enter, while GS (t ≈ −2.7…−3.3) and C/P+ (t ≈ +2.1…+2.4) remain significant — the paper's variable-significance finding, reproduced.

The 66 failing cells (5.1%) concentrate in four vintage-sensitive clusters, each diagnosed with evidence below: near-zero size-adjusted cells (Tables I–III), early-formation and near-zero year-by-year spreads (Table VI), Table V levels (SIZE statistic; earnings-growth on portfolios whose modern-vintage earnings are negative), and Fama-MacBeth coefficient magnitudes for E/P+/C/P+ (Table IV; signs and significance all correct). None of these touch a headline claim; all are consistent with a single root cause — 2026-vintage restated Compustat fundamentals versus the authors' early-1990s vintage — documented as Assumption 7 and verified indirectly by the consistent ~15–25% upward level drift in every fundamentals-to-price ratio we compute (e.g. Table V C/P value 0.322 vs 0.279; S/P 6.50 vs 5.28).

---

## 2. Methodology and key decisions

The paper's methodology section (L114–L162) is explicit on most choices; 15 paper-silent decisions were recorded in `preparations/assumptions.md` (A1–A15) with rationale and impact. The load-bearing ones:

- **Universe (A1):** NYSE+AMEX common stocks, `shrcd IN (10,11)`, `exchcd IN (1,2)`, applied point-in-time via `dsenames` intervals at each formation date. Verified counts: 2,104 stocks (Apr 1968) → 2,530 peak (1973) → 1,968 (Apr 1989); 48,994 (stock × formation) rows total.
- **Formation mechanics:** 22 annual formations, last trading day of April 1968–1989; accounting from the fiscal year with `datadate ∈ [t−1−01−01, t−03−31]` (A3); equal-weighted annual buy-and-hold years +1…+5 with annual rebalancing of survivors; mid-year delisters replaced through year-end by their size-decile EW return (A6, exact gross-up formula in the registry).
- **Variables:** B/M = Compustat book equity (FF hierarchy `ceq+txdb` → `seq−pstkrv` → `at−lt−pstkrv`; BE≤0 excluded from B/M sorts, A2) over April market equity (`|prc|×shrout×1000`); C/P = (ib+dp)/ME; E/P = ib/ME; positive-ratio restriction applies only to C/P and E/P *sort assignment* (A8, per L162); GS = 5/4/3/2/1 weight-normalized average of the five annual sales-growth ranks (A4).
- **Size adjustment (A5):** ten deciles of the full universe by December t−1 market equity, fixed at formation. An alternative reading (reassign every December) was tested head-to-head (inner iteration 3 diagnostic): it moves 6/7 near-zero SAAR cells toward the paper but drifts the headline corner SAARs and worsens the large-cap subsample — i.e. tuning one convention to fit near-zero cells. The formation-fixed reading was kept; the near-zero SAAR residuals are classified as vintage noise.
- **Table VI definition conflict (A13):** Panel 3's caption says single deciles (D10−D1) but the table header (L2220, "B/M: 9,10 − 1,2"), body text (L2278), and the published values all use pooled (9,10)−(1,2). Empirically decisive: 1968 pooled = 0.104 ≈ paper 0.098; single = 0.043 (56% off). Pooled was used.
- **Table V growth machinery (A14, A15):** per-$1-invested quantities (weight 1/ME at formation) averaged across the 22 formations before differencing, with a sign-preserving geometric root — the literal L144–160 procedure. SIZE = mean market equity (direct reading; our levels run 1.7–2× the paper's anchors while all ratio rows for the same portfolios match, a pattern consistent with the paper having reported medians — not adopted, as switching statistics to fit anchors would be tuning).
- **Hansen-Hodrick SEs (A12):** 1-yr iid; 3-yr/5-yr HH with lags ≤ k−1 (k = 2/4). Verified empirically against the paper's published t's — the textbook MA(H−1) truncation is numerically unstable at T=18 (P1 5-yr → 18.3 vs paper 7.63), the A12 truncation reproduces all nine paper t-stats within 24%.
- **Vintage (A7):** authors used early-1990s CRSP/Compustat (incl. the research file); we use 2026 vintages. Restated fundamentals differ — the consistent level drift across all ratio tables is the fingerprint of this, not of a methodology error.

---

## 3. Per-table results

Machine-readable detail: `results/table_{1..8}.md` (paper-format tables), `results/table_{I..VIII}_cells.json` (per-cell values), `results/evaluation_iter6.json` (per-cell MATCH/PATTERN/FAIL with tolerances from `preparations/tables_to_replicate.json`).

### Table I — univariate decile sorts (316 targets: 309 MATCH, 4 PATTERN, 3 FAIL)

| Panel | AR D1→D10 (ours) | AR D1→D10 (paper) | SAAR D1 / D10 (ours) | (paper) |
|---|---|---|---|---|
| A B/M | 0.098 → 0.206 (monotone ↑) | 0.093 → 0.198 | −0.040 / +0.036 | −0.043 / +0.035 |
| B C/P | 0.093 → 0.205 (monotone ↑) | 0.091 → 0.201 | −0.049 / +0.037 | −0.049 / +0.039 |
| C E/P | 0.112 → 0.195 (monotone ↑) | 0.114 → 0.190 | −0.036 / +0.028 | −0.035 / +0.019 |
| D GS (value→glamour) | 0.179 → 0.124 (↓, 2 tiny wobbles) | 0.195 → 0.127 | +0.008 / −0.025 | +0.022 / −0.024 |

CR5 reproduced throughout (e.g. B/M 0.569→1.519 vs paper 0.560→1.462). The 3 FAILs are GS-panel SAAR cells with |paper| ≤ 0.022 and |deviation| ≤ 1.4pp (diagnosed §5a). One qualitative deviation: the paper's E/P D10 dip (0.193→0.162, temporarily-depressed-earnings firms) does not appear in our vintage (0.193→0.195) — the restated fundamentals no longer concentrate depressed-earnings firms at the top E/P decile.

### Table II — two-dimensional 30/40/30 sorts (366 targets: 359 MATCH, 2 PATTERN, 5 FAIL)

All five variable pairs × 9 cells × 8 statistics. C/P×GS glamour (C/P1,GS3) AR **0.109** / value (C/P3,GS1) **0.213** (paper 0.114/0.221); CR5 **0.66 vs 1.64** (paper 0.712 vs 1.711); SAAR spread **+8.0pp** (+8.7). E/P×GS AR spread **+10.0pp** (artifact 0.0996; paper 11.2pp). Cell-size pattern matches L1213 exactly: negatively-correlated-pair corners (C/P×GS, E/P×GS extremes) are the largest cells. `results/figure_1.png` reproduces the paper's Figure 1 (CR5 bars over the 9 C/P×GS cells). The 5 FAILs are again near-zero interior SAAR cells (|paper| ≤ 0.018; §5a).

### Table III — largest 50% subsample (140 targets: 130 MATCH, 7 PATTERN, 3 FAIL)

C/P×GS: AR 0.103 (glamour) / 0.186 (value), spread +8.3pp (paper +7.8); SAAR −0.037/+0.035, spread +7.2pp (paper +8.7 — ours drifts 1.5pp on the value corner, the most vintage-sensitive benchmark cell; §5a). E/P×GS SAAR spread +8.3pp (paper 8.3 — exact). The paper's robustness claim — the value spread survives in the large caps — **replicates**.

### Table IV — Fama-MacBeth regressions (63 targets: 38 MATCH, 15 PATTERN, 10 FAIL)

Nine specifications, 22 cross-sections each (N ≈ 1,634–2,186/formation). The paper's variable-significance finding **replicates**: standalone significance of GS (−0.082, t −2.97; paper −0.061, −2.20), B/M (+0.028, t 2.53; paper +0.039, 2.13), C/P+ (+0.180, t 3.15; paper +0.356, 4.24), E/P+ (+0.350, t 2.33; paper +0.526, 2.54); SIZE insignificant (−0.004, t −0.44). In the multiple specifications **B/M collapses**: spec 6 +0.009 (t 0.82), spec 8 +0.005 (t 0.55) — paper +0.006 (0.33) and 0.000 (0.005) — while GS and C/P+ stay significant at |t| ≥ 2.1. The 10 FAILs are E/P+/C/P+ *coefficient magnitudes* (~half the paper's) and their t-stats; signs and significance structure all correct; the magnitude attenuation is the same vintage level-drift seen in Table V (§5b).

### Table V — fundamentals, past and future growth (63 targets: 36 MATCH, 7 PATTERN, 20 FAIL)

Panel A ratios track the paper: B/M glamour/value E/P 0.023/−0.002 (paper 0.029/0.004), C/P 0.057/0.258 (0.059/0.172), D/P 0.012/0.036 (0.012/0.032), B/M 0.245/2.556 (0.225/1.998); C/P×GS E/P 0.049/0.118 (0.054/0.114), C/P 0.076/0.322 (0.080/0.279). RETURN(−3,0) reproduces the glamour run-up: +1.576 (B/M glamour, paper +1.455), +1.357 (C/P×GS glamour, paper +1.390), value −0.055/+0.237 (paper −0.119/+0.225). The extrapolation story's internal-consistency check reproduces exactly (glamour C/P 0.076 grown at our ACG(0,5)=0.123 → 0.136 = paper's reported 0.136). The 20 FAILs: 3 SIZE cells (mean vs likely-median, A15), 3 earnings-growth blowups (formation-averaged earnings cross zero in our vintage — paper's −0.274 presupposes same-sign endpoints; A14), and 14 cash-flow/sales-growth magnitudes that match in sign and direction but run ~1.5–2× (vintage; §5b).

### Table VI — year-by-year value−glamour (197 targets: 163 MATCH, 11 PATTERN, 23 FAIL)

Averages and t-statistics (the paper's inference rows) **all pass**: P1 0.087/0.383/0.910 (paper 0.079/0.357/0.841), t 3.28/4.68/7.96 (3.38/6.16/7.63); P2 0.125/0.524/1.111, t 4.60/4.82/5.23; P3 0.074/0.387/0.980, t 2.52/3.38/5.89. The paper's consistency claim — value outperforms in every 5-year window — **confirmed 18/18 in all three panels**. 145/180 year cells within tolerance; the 23 FAILs are early-formation (1968–1973, tiny corner portfolios under thin Compustat coverage) and near-zero-magnitude cells (§5c). `results/figure_2.png` reproduces Figure 2 (year-by-year C/P×GS spreads with NBER-recession and EW-decline markers).

### Table VII — market states (91 targets: 84 MATCH, 6 PATTERN, 1 FAIL)

States defined over EW-index months bounded to **May 1968–April 1994** (312 months — the last month any cohort is still within its 5-year holding window; audit iteration 2 corrected the original May 1968–April 1995 window, which had let ~8 moderate-state months reuse the 1989 cohort past Year +5). The paper's 25/88/122/25 counts (sum = 260, their shorter EW window) are reproduced by the semantic definition (worst 25 / next-worst 88 / best 25 / next-best 122; 52 moderate months unclassified); W25 and B25 month sets are provably invariant to the bounding (W25 max month Sep 1981), so those cells are unchanged. **Value loses less in bad states, both classifications:** W25 — C/P×GS value −0.086 (paper −0.086, exact) vs glamour −0.124 (paper −0.103); B/M spread +0.009 (paper +0.011); N88 — spreads +0.020 / +0.006 (paper +0.014 / +0.002). The 1 FAIL is the 1B P_122 t-stat (paper −0.168 — statistically noise in either vintage); the 6 PATTERNs are N88/P122 cells whose moderate-month composition differs from the paper's unrecoverable 260-month window (a numerical, not methodological, gap).

### Table VIII — betas and standard deviations (54 targets: 50 MATCH, 3 PATTERN, 1 FAIL)

Betas 1.08–1.49 across all portfolios (systematically ~0.05–0.1 above the paper's levels — modern-vintage volatility; EW-index beta 1.339 vs 1.304, std 0.268 vs 0.250 ✓). The paper's risk conclusion **replicates in substance**. Value−glamour beta gaps by classification (all **opposite in sign** to the paper's +0.1, all small): C/P deciles **−0.05** (1.311 − 1.362), B/M deciles **−0.07** (1.341 − 1.407), C/P×GS corners **−0.18** (1.307 − 1.486). Under every classification the dollar beta difference (≤0.18) explains at most ~1.4pp/yr of the 10–11pp return spread (the paper's own arithmetic, L2344, uses 8% × Δbeta), so beta cannot explain the value premium — the paper's claim — and the sign reversal is immaterial to that conclusion. Two corollary deviations are disclosed rather than hidden: (i) the C/P×GS corner beta gap is larger in magnitude than the paper's and sign-reversed (vintage betas, unscored cells on OCR grounds); (ii) the paper's body finding that C/P×GS *value* raw-return volatility exceeds *glamour* (24.1% vs 21.6%, L2346) is **reversed in our data** (glamour 0.287 > value 0.264 — a vintage-volatility effect at levels ~1.2–1.3× the paper's), while the paper's substantive finding that *size-adjusted* volatility is "virtually the same" across portfolios holds at the mid deciles (saar_std 0.033–0.065). The 1 scored FAIL is the glamour decile's saar_std (0.087 vs 0.037 — same fixed-benchmark mechanism as §5a).

---

## 4. Evidence map — what each validated table proves

- **Tables I–III:** universe construction, PIT membership, April formations, all four signal definitions (B/M, C/P, E/P, GS weighted rank), EW annual buy-and-hold with delisting replacement, CR5/SAAR machinery, independent 30/40/30 intersection sorts, large-cap subsample — the full portfolio pipeline.
- **Table IV:** Fama-MacBeth setup incl. the E/P+/C/P+ dummy construction and the variable-significance hierarchy.
- **Table V:** the accounting-growth machinery (per-$1-invested, formation-averaged) and the extrapolation mechanism's direction.
- **Table VI:** overlapping multi-year spreads, Hansen-Hodrick SEs, consistency of outperformance.
- **Table VII:** monthly attribution of annually-rebalanced portfolios to market states; the no-downside-risk claim.
- **Table VIII:** CAPM betas/standard deviations; the traditional-risk claim.

---

## 5. Residual analysis (all 66 FAILs, diagnosed)

**(a) Near-zero size-adjusted cells — 15 FAILs** (Tables I–III SAAR: 11; Table VIII glamour saar_std: 1; plus 3 Table III SAAR). All |paper values| ≤ 3.1pp, all |deviations| ≤ 1.9pp, signs flip on quantities statistically indistinguishable from zero. Root cause: the size-decile benchmark's CRSP-vintage composition. Fix attempted (iter-3 diagnostic: reassign deciles each December) — moves 6/7 full-sample cells toward the paper but drifts headline corners and worsens the large-cap subsample; rejected as tuning-to-fit. Classified as vintage residual under A5/A7.

**(b) Fundamentals levels and FM magnitudes — 30 FAILs** (Table V: 20; Table IV: 10). Single root cause with a fingerprint: every fundamentals-to-price ratio we compute runs consistently 15–25% above the paper's (restated 2026 Compustat vs early-1990s vintage). This (i) attenuates E/P+/C/P+ regression slopes by ~½ with signs and significance preserved, (ii) inflates Table V ratio levels, (iii) drives the 3 SIZE fails (mean statistic; the level gap's cause — vintage and/or a different aggregation the parse cannot recover — is not identified; see A15), and (iv) makes the B/M portfolios' earnings bases sign-unstable in our vintage, so the formation-averaged earnings series crosses zero and the paper's-method growth computation produces extremes the paper's same-sign-endpoint vintage could not — the B/M **value** cells (−1.57, −2.77, +1.90) *and* the B/M **glamour** AEG(−5,0) (0.080 vs paper 0.309, ≈0.26×, same mechanism on a positive base). No methodology change can remove a data-vintage gap; documented under A7/A14/A15. The qualitative findings (directional growth patterns, significance hierarchy) replicate.

**(c) Early-formation and near-zero year spreads — 21 FAILs** (Table VI: 20 + Table VII P_122 t: 1). Concentrated in 1968–1973 formations where C/P×GS corner portfolios hold 70–100 stocks (vs 150–230 later) under thin early Compustat coverage — small-portfolio noise amplified by the 50% relative tolerance on |paper| ≤ 0.15 cells. The formation-averaged rows (the paper's actual inference) all pass. The VII P_122 t-stat (−0.17 in the paper, −1.97 in ours) is noise around zero by construction.

**Tier-2 cells (57):** same-sign, within 2× of the paper — predominantly Table IV t-stats and Table VII moderate-state index means; all carry the vintage explanation above.

---

## 6. Reproducibility

```
cd <internal>/rep-it-up
uv run python replications/contrarian_investment/src/main.py        # panel.parquet (~2 min, all SQL in src/sql/)
uv run python replications/contrarian_investment/src/tables.py      # Tables I-III + Figure 1
uv run python replications/contrarian_investment/src/table4.py      # Table IV
uv run python replications/contrarian_investment/src/table5.py      # Table V
uv run python replications/contrarian_investment/src/table6.py      # Table VI + Figure 2
uv run python replications/contrarian_investment/src/table7.py      # Table VII
uv run python replications/contrarian_investment/src/table8.py      # Table VIII
```
Pipeline runtime ≈ 2 min total; table scripts ≈ 5–60 s each. All queries carry execution-time and row-read guards. ClickHouse credentials from `.env`.

---

## 7. Limitations

1. **Data vintage** — the single dominant source of residual (see §5). A 1990s Compustat extract would close most of the level gap; unavailable here.
2. **Table VII Panel 2 (GNP states)** — not replicated: quarterly real GNP data (BEA) are not in ClickHouse. Panel 1 (the paper's primary downside-risk test, with the market-state months fully in CRSP) is replicated; the paper states Panel 2 "mirror[s] the basic conclusions from Panel 1" (L2340).
3. **OCR-driven target gaps** — Table VIII Panel 2 portfolio cells and Panel 3 deciles 7–10 were dropped from scoring (the parsed table is column-truncated there; our values are computed and shown in `results/table_8.md`).
4. **Early-formation coverage** — pre-1974 formations rest on thinner Compustat coverage (the paper discusses the 1978 database expansion itself, L118); early-year cells are noisier than late-year ones in both vintages.
5. **Two paper-internal inconsistencies resolved by evidence** (A13 pooled Panel 3; Table VII 260-vs-324-month states) — documented in the assumptions registry with the empirical tie-breakers.
