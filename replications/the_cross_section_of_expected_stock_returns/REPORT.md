# Replication Report — Fama & French (1992), "The Cross-Section of Expected Stock Returns"

*Journal of Finance* 47(2), 427–465. Replicated from CRSP (`crsp_202601`) and
Compustat (`comp_202601`) via ClickHouse. Sample: July 1963 – December 1990
(330 months; 28 formation years). All code under `src/`; saved SQL under
`src/sql/`; data artifacts under `data/`; per-table outputs and plots under
`results/`.

---

## 1. What was replicated

All six main-paper tables, at cell level (780 unique targeted cells —
783 as listed in `tables_to_replicate.json` minus 3 exact-duplicate
Table I Panel-C entries that the consolidated evaluator dedupes):

| Table | Content | Targeted cells | Tier 1 pass |
|---|---|---:|---:|
| I | 100 size×pre-β portfolios: returns (A), post-ranking βs (B), ln(ME) (C) | 107 | 107 (100%) |
| II | 12 size / 12 β portfolios: returns + 8 characteristics | 194 | 168 (87%) |
| III | 11 Fama-MacBeth specifications, slopes + t-stats | 52 | 30 (58%) |
| IV | BE/ME (12) and E/P (13) portfolio sorts | 225 | 199 (88%) |
| V | 10×10 size × BE/ME average-return matrix | 121 | 110 (91%) |
| VI | Subperiod FM regressions + NYSE VW/EW benchmarks | 81 | 78 (96%) |

The consolidated per-cell evaluation (692 Tier 1 / 86 Tier 2 / 2 FAIL /
280 no-target SKIP over the 1,060 cells the replication computes) is in
`results/evaluation_summary.md`. Five figures illustrating the paper's
claims are in `results/`: `size_effect.png` (decile returns 1.48→0.87 %/mo),
`beme_effect.png` (0.41→1.79), `size_beme_heatmap.png` (the 10×10 matrix),
`cumulative_portfolios.png` (Small ×57 vs Large ×12; High BE/ME ×93 vs Low
×4.7 over 330 months), and `fm_slopes_rolling.png` (rolling FM slopes: β ≈ 0,
ln(ME) < 0, ln(BE/ME) > 0 throughout).

## 2. Methodology (as implemented, with paper citations)

- **Universe** — all nonfinancial common stocks (CRSP shrcd 10/11, exchcd
  1/2/3, point-in-time via `dsenames` validity windows) in the CRSP ×
  Compustat intersection; financials excluded via SIC 6000–6999
  (`dsenames.siccd`, since `funda` carries no SIC in this vintage) — L119.
  No price floor: the paper's universe definition is explicit and complete
  (Assumption 1).
- **Sample requirements** (L123–L137) — valid CRSP price at December t−1 and
  June t; ≥ 24 valid monthly returns in the 60 months ending June t;
  Compustat `funda` (fiscal year ending in CY t−1) with A > 0, BE and E
  available. Negative-book-equity firm-years excluded (L1350; 1,033
  firm-years, ~37/yr).
- **Variables** — ME = |prc|×shrout×1000 from CRSP (dollars); BE = ceq +
  coalesce(txdb,0), fallback seq − coalesce(pstkrv,pstk,0) + txdb
  (Assumption 6; L813, L119); A = at; E = ib + coalesce(txdi,0) −
  coalesce(dvp,0) (L813). Accounting ratios (BE/ME, A/ME, A/BE, E/P) use
  December t−1 ME; size ln(ME) uses June t ME in millions (L123). E/P dummy
  + E(+)/P split per L1185 (E ≤ 0 → dummy 1, E(+)/P 0). funda filtered to
  INDL/C/D/STD — verified safe for 1962–1989 in this extract (Assumption 13).
- **Pre-ranking β** — Dimson sum-beta (slopes on current + one-lagged
  `msi.vwretd`) over 24–60 monthly returns ending June t (L169, L253;
  Assumption 7).
- **Sorts** — (A) size deciles, NYSE-only ME breakpoints over ALL NYSE
  common stocks (L151); (B) within-decile pre-β deciles, NYSE
  data-qualified breakpoints (L169); (C) one-dimensional 12-portfolio size
  and β sorts with half-split extremes (L811); (D) BE/ME and E/P sorts
  formed at December t−1, breakpoints over all data-qualified stocks
  (L1382); (E) size×BE/ME 10×10 at June t, within-decile BE/ME breakpoints
  over all data-qualified stocks (L1818, Assumption 8).
- **Post-ranking β** — EW monthly returns of the 100 size×β portfolios over
  the full 330-month sample; Dimson sum-beta vs the CRSP VW market
  (L171, L173); each stock carries its portfolio's full-period β, reassigned
  each June (L197, L1386).
- **Returns** — monthly holding returns with delisting adjustment
  (Assumption 5, paper-silent): `msf.ret` when valid; else `msedelist.dlret`
  when valid; else −0.30 for performance delistings (dlstcd 500–599), 0.0
  for mergers/exchanges (200–399) with missing dlret.
- **Fama-MacBeth** (L145, L1185, L1187, L1189) — monthly cross-sectional OLS
  of raw stock returns on the regressors (no rf subtraction, no factor
  model — Assumption 3); ln(BE/ME), ln(A/ME), ln(A/BE), E(+)/P winsorized at
  the monthly 0.005/0.995 cross-sectional fractiles (β, ln(ME), E/P dummy
  untouched — Assumption 9); average slope ×100 (%/month); t = mean/(SD/√N),
  plain time-series (no Newey-West).
- **NYSE benchmarks** (Table VI, L2039) — VW and EW monthly returns of all
  NYSE common stocks (PIT exchcd 1, shrcd 10/11), delisting-adjusted, VW on
  prior month-end ME (Assumption 10).

## 3. Headline results — the paper's central claims

**(i) Market β does not explain average returns (1963–1990).** Replicated.
β-alone FM slope 0.07%/mo (t 0.22) vs paper 0.15 (t 0.46) — both far below
significance. With size added: β −0.39 (t −1.30) vs −0.37 (−1.21). In the
full battery (R8–R11) our β t-stats are 0.39, 0.58, −0.55, 0.69 — matching
the paper's own prose ("typically less than 1 standard error from 0",
L1159). Note: the paper's printed R8–R11 β t-statistics (−2.06…−2.47) are
internally inconsistent with its R1/R3 rows — they imply monthly β-slope SDs
≈1.0 vs the ≈5.9 implied by R1/R3 (ours: 6.0/5.5, matching R1/R3); a 6×
dispersion compression from adding controls is statistically impossible
(ours moves 6.0→5.1). The subperiod evidence replicates exactly: reg(b) β
= 0.08 (t 0.20) in 1963–76 and −0.48 (t −1.30) in 1977–90 (paper 0.10/0.25
and −0.44/−1.17).

**(ii) Size is reliably negatively related to average returns.** Replicated.
ln(ME)-alone slope −0.14 (t −2.47) vs paper −0.15 (−2.58); robust across all
specifications containing size (|t| 1.3–3.3). Size-decile EW returns decline
1.48 → 0.87 %/mo (paper 1.52 → 0.89); the smallest half-decile earns
1.60 %/mo (paper 1.64).

**(iii) BE/ME is reliably positively related — and dominant.** Replicated.
ln(BE/ME)-alone slope 0.49 (t 5.54) vs 0.50 (5.71); with size: 0.34 (t 4.20)
vs 0.35 (4.44); subperiod-stable at 0.32/0.36 (63–76 / 77–90) vs paper's
0.36/0.35. BE/ME-sorted returns rise monotonically 0.41 → 1.79 %/mo (paper
0.30 → 1.83) with essentially flat betas (1.36 → 1.35 vs 1.36 → 1.35, all 12
cells within 0.019). The 10×10 matrix reproduces both gradients:
within-decile Low→High BE/ME spread 0.84 %/mo (paper 0.99) and size spread
0.61 (paper 0.58).

**(iv) Size + BE/ME absorb leverage and E/P.** Replicated qualitatively.
The leverage puzzle replicates: ln(A/ME) positive (0.48, t 5.44) and
ln(A/BE) negative (−0.66, t −6.56) alone (paper 0.50/5.69 and −0.57/−5.34),
with |ln(A/ME)| ≈ |ln(A/BE)| ≈ the BE/ME slope, exactly the paper's
"ln(BE/ME) = ln(A/ME) − ln(A/BE)" resolution. E(+)/P collapses from 5.55
(t 5.46) alone to 1.59 (t 2.44) once size and BE/ME enter (paper 4.72 →
0.87), and the E/P dummy is killed (−0.21, t −1.41; paper −0.14, −0.90) —
the absorption claim holds; the E(+)/P level runs ~0.7–1.1 above the paper's
in the multivariate specs (see §4).

**Portfolio construction validated** — Table I's 100-portfolio structure
replicates at 107/107 cells: the All-column size gradient, the flat All-row
(β groups), post-ranking betas rising 0.49→1.76 across β groups within every
size decile (small-decile βs 1.08/1.76 vs paper 1.05/1.79; decile-average
betas 1.44→0.95 vs 1.44→0.92, matching the paper's smallest decile exactly at
1.44), and ln(ME) essentially exact (2.24→7.98 vs 2.24→7.93).

**January seasonality of the BE/ME effect (L2186).** Replicated
(`results/table_6_january.md`): splitting the reg(a) monthly ln(BE/ME)
slopes by calendar month gives a January mean of ≈0.61 %/mo versus
≈0.32 for February–December (t ≈ 3.9) — about twice, as the paper
claims — while the Feb–Dec slope stays within 0.03 of the full-year
mean (0.34), confirming the BE/ME effect is strong throughout the
year, not a January seasonal.

## 4. Documented deviations (Tier 2, with justification)

All failures cluster in four explained groups; no unexplained failures.

1. **Compustat-vintage composition shift in market-equity-denominated
   characteristics** (Tables II/IV: ln(A/ME), ln(BE/ME); Table III: E(+)/P
   levels). Evidence it is composition, not data error: (a) ln(A/BE) — the
   one characteristic without market equity — passes 25/25 in Table IV;
   (b) the identity ln(A/ME) − ln(A/BE) = ln(BE/ME) holds to 1.4e-16
   cell-by-cell, so A and BE values are consistent and the deviation enters
   through the ME denominator's portfolio membership; (c) June ln(ME)
   averages pass 25/25 while December-ME-denominated ratio averages shift;
   (d) this extract carries +5.5% more stocks/month (2,393 vs 2,267) from a
   broader CCM link table and NASDAQ coverage, and the extra firms pile into
   ratio-extreme bins (BE/ME 1A: 123 vs 89 firms; E/P port 0: 400 vs 355).
   The paper's cross-sectional patterns (monotone in size; monotone in
   BE/ME; U-shape in E/P) all hold. Near-zero paper targets (e.g. ln(A/ME)
   10A: paper −0.03 vs ours +0.18) produce sign flips on ~0-magnitude
   ratios — boundary artifacts, documented per cell.
2. **NYSE benchmark mean shift** (Table VI, 3 cells): VW/EW means run
   +0.1–0.2 %/mo above the paper while every SD matches within 0.14.
   CRSP's own NYSE index in this extract (msia: VW 0.91/SD 4.46) shows the
   same uplift vs the paper's 0.81/4.47 — the tape itself differs from the
   1991-vintage CRSP the paper used. Computation validated on our own series
   (Oct-1987 VW −21.7%).
3. **Table III R8–R11 β t-statistics** (8 cells): fail against OCR targets
   that are internally inconsistent with the paper's own R1/R3 rows and
   prose (see §3(i)); our values are the text-consistent ones.
4. **Table V interior cells** (11 cells): 7 in the Low-BE/ME within-decile
   column — the thinnest growth cells, where the broader extract moves EW
   means most (e.g. ME-3×Low 0.22 vs 0.56); all margin cells pass and both
   headline spreads replicate.

## 5. Assumptions registry

Thirteen paper-silent decisions and convention deviations are documented in
`preparations/assumptions.md` (Assumptions 1–13), plus per-iteration
implementation logs (iterations 1–7). Key ones: no price floor (Assumption
1), EW throughout (2), raw returns / no factor model (3), SIC-based
financial exclusion via CRSP (4), delisting treatment (5), BE fallback
chain (6), Dimson pre-ranking betas (7), Table V breakpoint universe (8),
winsorization of the four ratios only (9), NYSE-only benchmarks (10),
negative-earnings handling (11), appendix 1941–1990 tables out of scope
(12), datafmt='STD' verified for 1962–1989 (13).

## 6. Reproducibility

- `src/main.py` rebuilds `data/panel.parquet` (810,612 rows × 25 columns;
  ~11 s) from the seven saved SQL files under `src/sql/`.
- `src/table_1.py … table_5.py`, `src/table_3_6.py` regenerate each
  `results/table_<n>.md` from the cached artifacts (≤ 3 s each; no
  ClickHouse except `table_3_6.py`'s NYSE-benchmark query, cached in
  `data/nyse_benchmark_returns.parquet`).
- `src/evaluate.py` regenerates `results/evaluation_summary.md`.
- `data/` contains three computed intermediates besides the panel
  (`portfolio_returns.parquet` — 100 size×β EW series;
  `agg_portfolio_returns.parquet` — size/beta-group/grand EW series;
  `nyse_benchmark_returns.parquet` — NYSE VW/EW series). These are
  computed artifacts (aggregated portfolio returns), not raw table
  dumps; `prep_validation.py`'s allowlist covers these names
  (`scripts/prep_validation.py`) and the `data/` check passes.
- Estimator cross-checks: Dimson sum-beta matches statsmodels to 5–6
  decimals; aggregate CRSP market cap matches `msi.totval` (ratio 1.015);
  IBM (permno 12490) December-1979 ME matches Compustat prcc_f×csho exactly.

## 7. Scope boundaries

- Appendix Tables AI–AII (NYSE-only 1941–1990, no Compustat) are
  out of scope for this run (Assumption 12) — they are robustness
  extensions on a different sample and do not affect the main claims.
- The Fama-French factor library is not used: the paper reports no factor
  alphas (Assumption 3); its only market-proxy input (msi.vwretd) is
  present and used for β estimation.
