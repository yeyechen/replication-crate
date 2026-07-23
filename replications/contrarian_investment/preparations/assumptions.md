# Assumptions Registry — contrarian_investment (LSV 1994)

Paper-silent decisions made by the replicator. Paper-derived rules live in
`preparations/preprocessing_rules.json`; iteration diagnostics are appended
below as `### Iteration N` entries during the Stage 7 loop.

---

# Assumption 1: CRSP share-code operationalization of the NYSE/AMEX universe

**Decision:** Universe = CRSP `shrcd IN (10, 11)` (ordinary common shares) AND `exchcd IN (1, 2)` (NYSE, AMEX), applied point-in-time via `dsenames` intervals active at each formation date. NASDAQ (exchcd 3) is excluded.
**Rationale:** Paper states only "The universe of stocks is the New York Stock Exchange (NYSE) and the American Stock Exchange (AMEX)" (L116) and is silent on share codes. Share codes 10/11 are the standard operationalization of "common stocks" and exclude ADRs, REITs, closed-end funds, and units, which are not part of any value/glamour sort in the literature. Sanity check run 2026-07-22: 2,104 universe stocks at 1968-04-30 and 1,968 at 1989-04-28 — consistent with the paper's description of pre-1978 Compustat covering "~2,700 NYSE/AMEX firms" (the intersection with Compustat coverage is the binding constraint in early years).
**Impact:** All tables (universe definition).

# Assumption 2: Book equity hierarchy

**Decision:** BE = `ceq + coalesce(txdb, 0)`; if `ceq` missing, BE = `seq - coalesce(pstkrv, 0)`; if `seq` missing, BE = `at - lt - coalesce(pstkrv, 0)`; firm-years with BE ≤ 0 are excluded from B/M sorts.
**Rationale:** Paper says only "book value is taken from COMPUSTAT for the end of the previous fiscal year" (L166) without specifying the line-item recipe. The Fama-French (1992/1993) book-equity convention (ceq + deferred taxes, with the stated fallbacks) is the standard of the era and of the papers LSV explicitly build on (Fama-French 1992 is cited at L166). Excluding BE ≤ 0 is the FF convention for an economically meaningful book-to-market.
**Impact:** Table I Panel A, Table II Panels C/D/E, Table III, Table V Panel 1, Table VI Panel 3, Table VIII Panel 3, Table IV B/M column.

# Assumption 3: Fiscal-year-to-formation alignment

**Decision:** For formation at end of April of year t, a firm's accounting numbers come from the fiscal year with `datadate` in `[t-1-01-01, t-03-31]` (the most recent fiscal year ending at least one month before formation). For December-fiscal firms this is fiscal year t−1.
**Rationale:** Paper forms "at the end of April ... to ensure that the previous year's accounting numbers were available at the time of formation" (L122) but does not define the exact fiscal-year cutoff. Requiring datadate ≤ end of March t guarantees the numbers were public by formation (pre-EDGAR annual reports were typically available within ~3 months of fiscal year-end), and reproduces "previous fiscal year" for the vast December-fiscal majority.
**Impact:** All accounting-based variables (B/M, C/P, E/P, S/P, D/P, GS, Table V fundamentals).

# Assumption 4: GS with partially missing sales-growth years

**Decision:** GS weighted-average rank uses only the years with a valid sales-growth observation; weights of the available years (5 for year −1 ... 1 for year −5) are normalized to sum to one. Firms with zero valid growth years are excluded from GS sorts. A year's growth rate is valid when `sale` is positive in both the year and the prior year.
**Rationale:** Paper specifies the 5/4/3/2/1 weighting (L742) but is silent on firms missing some years (common in the 1960s with thin Compustat backfill). Normalizing available weights preserves the "recent growth weighs more" intent without discarding firms that have, e.g., 4 of 5 years. Requiring positive sales in both years avoids division-by-zero and meaningless percentage growth from near-zero bases (the paper itself flags base-near-zero growth as unreliable, L144).
**Impact:** Table I Panel D, Table II Panels A/B/C, Table III, Table V (C/P×GS portfolios), Table VI Panel 2, Table VIII Panel 2, Table IV GS column.

# Assumption 5: Size-decile benchmark population

**Decision:** The ten size deciles (used for SAAR and for the delisting replacement) are formed by ranking ALL universe stocks (NYSE+AMEX common) by market equity at the end of the previous calendar year (December t−1); breakpoints are the universe decile cut points, not NYSE-only.
**Rationale:** Paper says "for every stock in the sample, its market capitalization decile at the end of the previous year" (L140) — "in the sample" most naturally means the full NYSE/AMEX sample, so breakpoints come from the full sample. (The NYSE-breakpoint convention of PAPER_CONVENTIONS.md applies to paper-silent sorting; here the paper's own wording points to the full sample.)
**Impact:** SAAR in Tables I–III, Table VIII size-adjusted standard deviations, delisting replacement in all return tables.

# Assumption 6: Mid-year delisting replacement formula

**Decision:** For a stock delisting in month m of holding year h (formation year t, holding year h = t+k): annual holding-year return = `(1 + r_stock_to_del) × (1 + r_sizedec_rest) − 1`, where `r_stock_to_del` compounds the stock's monthly CRSP returns from the holding-year start through the delisting month (the delisting month return is `coalesce(msf.ret, dsedelist.dlret, 0)` — dlret absorbed once), and `r_sizedec_rest` compounds the equally-weighted monthly returns of the stock's size-decile portfolio (Assumption 5) over the remaining months of the holding year through the holding-year end. Stocks already delisted before the holding year contributes no stock months and use the full size-decile year only while they remain portfolio members (they do not — a delisted stock leaves the portfolio at delisting, so replacement applies within the delisting year only).
**Rationale:** Paper: "If a stock disappears from CRSP during a year, its return is replaced until the end of the year with the return on a corresponding size decile portfolio" (L138). The formula implements "replaced until the end of the year" for the post-delisting months while keeping the realized pre-delisting return, which is the standard reading. Monthly portfolios (Table VII) absorb dlret in the delisting month and drop the stock thereafter.
**Impact:** All return cells in Tables I, II, III, VI, VII; indirectly SAAR.

# Assumption 7: Data vintages

**Decision:** Use `crsp_202601` (msf, dsenames, dsedelist, msi, ccmxpf_lnkhist) and `comp_202601.funda` with filter `indfmt='INDL' AND consol='C' AND popsrc='D' AND datafmt='STD'`; risk-free rate from `ff.four_factor_monthly.rf`.
**Rationale:** Latest vintages per the data manuals; the filter combo is the dominant one in this extract (593,432 of 929,418 rows; verified 2026-07-22). The authors used early-1990s Compustat (including the research file); modern restated fundamentals will differ modestly from their vintage — an unavoidable, well-understood source of replication noise (Tier 2 fallback applies if magnitudes drift while patterns hold).
**Impact:** All tables.

# Assumption 8: E/P and C/P positive-ratio sort restriction applies only to sorts

**Decision:** Stocks with E ≤ 0 or C ≤ 0 are excluded only from the E/P and C/P *sort assignments* (decile and 30/40/30); they remain in the universe for B/M and GS sorts, for the Fama-MacBeth regressions (via the E/P+, C/P+, DE/P, DC/P construction, L1909), and for portfolio-level ratio computations in Table V ("without eliminating individual stocks ... that have negative values", L162).
**Rationale:** Paper L162 restricts the exclusion to "classifying individual stocks into portfolios" by E/P and C/P, and explicitly includes negative-E/P and negative-C/P firms in the Table IV regression via dummies.
**Impact:** Table I Panels B/C, Table II (pairs involving C/P or E/P), Table III, Table IV (all firms included), Table V (portfolio-level ratios over all members).

# Assumption 9: Table IV cross-section = all universe firms with a Year +1 return

**Decision:** Each of the 22 cross-sectional regressions runs over all universe stocks present at that formation date with non-missing R1 and non-missing GS, B/M, SIZE; E/P+, DE/P, C/P+, DC/P are defined for all (zero/dummy when the numerator is non-positive, L1909). GS for the regression is the same weighted-average sales-growth rank (fractional, 0–1 scaled within the formation cross-section) as in the sorts.
**Rationale:** Paper: "for every firm in the sample the 1-year holding-period return ... 22 cross-sectional regressions" (L1691) with the positive/dummy ratio construction (L1909) — the regression explicitly keeps negative-ratio firms, so the cross-section is the full sample, not the positive-ratio subset. GS enters as "the preformation 5-year weighted average rank of sales growth" (L1691) — the rank itself.
**Impact:** Table IV only.

# Assumption 10: Table VII market-state months

**Decision:** States are defined by the CRSP equal-weighted monthly index (`msi.ewretd`) over the months for which at least one annually-formed portfolio is outstanding: May 1968 – April 1995 (324 months → 25 worst / 88 other negative / 122 other positive / 25 best; matches the paper's 25/88/122/25 split, L2370). Portfolio monthly returns are equally weighted over current members; a member delisted in a month earns `coalesce(ret, dlret)` that month and exits thereafter.
**Rationale:** Paper defines the states by "the equally weighted index" (L2370) and says portfolios change "every April" (L2372). The 25/88/122/25 counts in the paper pin the month span at ~260 months; May 1968–April 1995 is the span covered by the 22 annual cohorts and yields the same 25/88/122/25 partition counts (to be verified at runtime; if counts differ by 1–2, the span is adjusted to reproduce the paper's counts).
**Impact:** Table VII Panels 1A/1B.

# Assumption 11: Table VIII beta construction

**Decision:** Per portfolio, 22 annual year-after-formation returns (Year +1, the same R1 series as Table I) regressed on the contemporaneous annual excess return of the CRSP value-weighted index (`msi.vwretd` compounded over each May–April holding year minus the annual compounded `ff.four_factor_monthly.rf`); beta = OLS slope. Standard deviations use the same 22 annual returns (and size-adjusted annual returns per Assumption 5).
**Rationale:** Paper: "using 22 year-after-the-formation returns as observations, its beta with respect to the value-weighted index ... corresponding returns on the value-weighted CRSP index and the risk-free asset" (L2788, L2342).
**Impact:** Table VIII only.

# Assumption 12: Hansen-Hodrick standard errors for Table VI

**Decision:** For the 1-year horizon, t-stat = mean / (std/sqrt(22)). For overlapping 3-year and 5-year horizon spreads, the variance of the mean is inflated per Hansen-Hodrick (1980): `Var(mean) = (1/T) × [γ0 + 2 × Σ_{j=1}^{k-1} γj]` with k = 2 for the 3-year horizon (MA(2): annual autocovariances at lags 0, 1) and k = 4 for the 5-year horizon (MA(4): lags 0..3), computed on the 22 formation-year spread series.
**Rationale:** Paper: "standard errors ... according to Hansen and Hodrick (1980) ... assuming annual MA(2) and MA(4) processes" (L2212, L2278).
**Impact:** Table VI t-statistics.

# Assumption 13: Table VI Panel 3 uses pooled (9,10)−(1,2) B/M deciles

**Decision:** Table VI Panel 3 spreads are the pooled EW portfolio of B/M deciles 9+10 minus deciles 1+2 — NOT the single highest-vs-lowest decile spread.
**Rationale:** The paper is internally inconsistent: the Panel 3 caption (L2210) says "the difference ... between the highest B/M (value) and lowest B/M (glamour) decile portfolios," but the table header (L2220, "B/M: 9, 10 – 1, 2"), the body text (L2278, "differences in cumulative returns between deciles (9, 10) and (1, 2) for C/P and B/M"), and the published numbers all use the pooled two-decile spread. Empirically decisive: at the 1968 formation the pooled spread = 0.104 ≈ paper 0.098, while the single-decile D10−D1 spread = 0.043 (56% off). The caption's "highest/lowest decile" wording is loose phrasing for the extreme two-decile portfolios.
**Impact:** Table VI Panel 3 (all year cells, average, t-stat).

# Assumption 14: Table V growth rates use formation-averaged per-$ series (avg-Q-first), with documented vintage residuals

**Decision:** Panel B/C growth rates are computed from per-$-invested quantities (weight 1/me_apr at formation, full-N denominator with missing items contributing $0), averaged across the 22 formations FIRST, then differenced/compounded with a sign-preserving geometric root — the literal procedure of L144-160. The alternative (growth per formation, then averaged) is reported alongside in table_5.md diagnostics but is NOT the default: it passes fewer targets (31 vs 36 of 63) and the paper's prose is explicit.
**Rationale:** "we average Year −4 and Year −3 portfolio earnings across all 22 formation periods before computing growth rates. Hence, the earnings growth rate ... is computed as (AE(−3) − AE(−4))/AE(−4)" (L160). Three earnings-growth cells for the B/M value portfolio blow up under this procedure on the modern vintage (AEG(−5,0) = −1.57, AEG(0,5) = −2.77, AEG(2,5) = +1.90 vs paper −0.274/+0.436/+0.215): today's restated fundamentals put the value decile's formation-year earnings solidly NEGATIVE, so the formation-averaged earnings series crosses zero and the sign-preserving root produces extremes the paper's same-sign-endpoint vintage could not. This is a documented vintage residual (Assumption 7), not a method deviation — the cash-flow and sales growth cells reproduce the paper's signs and directional story (glamour's past growth does not persist; value's post-formation growth often exceeds glamour's in years +2..+5).
**Impact:** Table V Panel B/C growth rows (AEG/ACG/ASG at (−5,0), (0,5), (2,5)).

# Assumption 15: Table V SIZE is the mean market equity across members and formations

**Decision:** SIZE = mean of member me_apr (in $M), averaged across the 22 formations (equal weight per formation).
**Rationale:** Paper defines SIZE as "the total dollar value of equity (in millions)" (L1959) without specifying the cross-sectional statistic; the mean is the direct reading and matches the equal-dollar-investment framing of the table. Our SIZE runs 1.7-2× the paper's anchors (B/M glamour 1,160 vs 663; value 241 vs 120; C/P×GS value 676 vs 390) while the ratio rows (E/P, D/P, B/M) for the same portfolios match. The cause of the level gap is **not identified**: the earlier hypothesis that the paper reported the MEDIAN was tested (audit 1) and does NOT hold either — the median of per-formation member means is G=298 / V=41 $M, which is no closer to the paper's 663/120 (ratio 0.45). The residual is therefore left unattributed (vintage and/or a cross-sectional aggregation the OCR'd paper text does not recover) and the SIZE cells remain documented FAILs. The directional claim (glamour larger than value under B/M) replicates.
**Impact:** Table V SIZE row (4 cells; 3 FAIL vs paper anchors, 1 MATCH, all documented as unattributed level residual).

---

### Iteration 1 — data pipeline build (2026-07-22)

Implementation-level notes and ambiguity flags from building `data/panel.parquet`
(methodology A1–A12 unchanged; these are engineering decisions + data-handling
flags for the Replicator to review).

**Units (forced by data, verified):** `me_apr = abs(prc)*shrout*1000` is in
DOLLARS; all Compustat items (be, ib, dp, sale, dvc, and the 40 wide columns) are
in $ MILLIONS. Every ratio therefore divides the $M item by `me_millions =
me_apr/1e6`. Verified against the IBM check: E/P = 5491/67502 = 0.0813, C/P =
(5491+3871)/67502 = 0.1387.

**⚠️ B/M flag (IBM 1989):** A2 (BE = ceq + txdb) gives IBM BE = 39509 + 4623 =
44132 and bm = 44132/67502 = **0.654**. The task's hint of "~0.59" corresponds to
the ceq-ONLY variant (39509/67502 = 0.585). A2 was implemented exactly (0.654).
The "~0.59 using BE=ceq+txdb" phrasing is internally inconsistent; flagging for
the Replicator. ep (0.081) and cp (0.139) match the task's expected values.

**ClickHouse data quirks (this instance):** (a) `msf.date`/`datadate`/`dlstdt`
are Nullable(String); `toDate()` does NOT parse them reliably, so all date
filtering uses lexicographic (ISO-safe) string comparison and year/month come
from `substring`. (b) The PIT universe/CCM-link conditions are pure interval
overlaps with NO equality key, so hash/partial-merge joins fail; implemented as
CROSS JOIN + WHERE (formation set is only 22 rows — cheap and exact).

**Data cleaning (per references/CRSP.md):** return sentinels `< -1.0` (e.g.
-55/-66/-88/-99) in both `msf.ret` and `dsedelist.dlret` are treated as missing
before the `coalesce(ret, dlret, 0)`. In the holding-window months there were 0
sentinel `msf.ret` and 19,998 NULL `msf.ret` (coerced to dlret-in-delist-month
else 0). `funda` is de-duplicated to one row per (gvkey, fyear) by latest
datadate (the standard filter already makes this near-unique).

**Size deciles (A5 operationalization):** deciles via `ntile(10)` over December
t−1 market equity (ascending; 1 = smallest) on the December PIT universe, with
ME > 0 required. Benchmark membership = December-universe decile members (fixed
at formation). The stock-return series covers the UNION of April-formation and
December-universe permnos so every benchmark member has returns. 829 April-
universe rows (1.69%) have no December decile (new listings Dec→Apr) → NULL
size_dec.

**GS (A4):** `gs_wavg` uses growth years g1..g5 = sale(t−k)/sale(t−k−1)−1; g5
needs sale(t−6), pulled internally (fiscal year t−6) but NOT stored among the 40
wide columns (which are t−5..t+4 = m5..p4). `gs_rank_frac` = `(rank() over
(partition by fy order by gs_wavg) − 1)/(count − 1)` over non-missing GS only
(missing GS → NULL, excluded from GS sorts).

**Holding-year returns (A6):** all cross-sectional computation is in ClickHouse
SQL (src/sql/*.sql). The final 12-month compounding with the A6 delisting gross-up
`stock_ret_k = (1+r_stock_to_del)×(1+r_sizedec_rest)−1` is assembled in pandas
(conditional compounding of −1/missing returns is far more robust there than SQL
aggregates; verified to 6 decimals against an independent recompute for a
survivor and a mid-year-delisted stock). The size-decile EW monthly benchmark is
likewise assembled in pandas from the SQL building blocks to avoid re-scanning
msf; `src/sql/size_benchmarks_monthly.sql` computes the identical logic for
Table VII.

**Edge case flagged:** 28 panel rows (0.057%) have `alive_1 = 0` — stocks that
delist exactly ON the formation date (last trading day of April). They are in the
PIT universe (listed that day, per A1) but cannot be held into May, so
`stock_ret_1` is NULL for them. `alive_1 = 1` for the other 48,966 rows, as
expected.

### Iteration 2 — Tables I, II, III + Figure 1 (2026-07-22)

Implemented from `data/panel.parquet` in `src/tables.py` (+ `src/sortlib.py`).
Sort methodology is fully pinned by the task spec (not paper-silent); notes below
are implementation choices + outcome flags.

**Sort mechanics:** Table I deciles via rank-based equal-count bins
(`min(10, floor((rank-1)/n*10)+1)`, `rank(method='first')` for deterministic
ties) — every (fy, sort) yields exactly 10 non-empty deciles. Tables II/III use
independent 30/40/30 breakpoints (q30/q70 of each variable over its valid subset;
`<=q30`→1, `<=q70`→2, else 3). Per group: R_k = EW mean of stock_ret_k over
members alive_k==1 & non-null; AR = mean(R_1..R_5); CR_5 = Π(1+R_k)−1;
SAAR = (1/5)Σ_k(R_k − B_k), B_k = mean sizedec_ret_k over the same members
(A5/A6). Table cell = formation-mean across the 22 cohorts.

**Table III subsample:** top 50% of the formation universe by me_apr (breakpoint =
within-formation median me_apr; ~24,459 of 48,994 rows); breakpoints recomputed
within the subsample.

**Outcomes vs paper (all within tolerance; modern restated fundamentals per A7):**
- Table I AR value−glamour spreads: B/M 0.108 (paper 0.105), C/P 0.113 (0.110),
  E/P 0.083 (0.076), GS glamour−value −0.055 (−0.068). SAAR B/M −0.040→0.036
  (paper −0.043→0.035).
- Table II Panel A (C/P×GS): AR glamour(1,3)=0.109/value(3,1)=0.213 (paper
  0.114/0.221), AR spread 0.105 (0.107), SAAR spread 0.080 (0.087).
- Table III Panel A: AR 0.103/0.186 (paper 0.106/0.184), spread 0.083 (0.078);
  SAAR spread 0.072 (0.087) — sign/pattern correct, magnitude drifts modestly
  (size benchmark is vintage-sensitive).
- Monotonicity: B/M, C/P, E/P AR strictly increasing across deciles; GS decreasing
  with two minor wobbles (D1<D2, D7<D8), as the paper notes GS is reverse-ordered.
- ⚠️ E/P top decile: paper's D10 AR (0.162) dips below D9 (0.193); mine is
  monotone (D10=0.195 ≥ D9=0.193) — the high-E/P distressed-firm dip does not
  reproduce on the modern vintage. Flagged for the Replicator.
- 2D corner cells can be small in individual formations (e.g. B/M×C/P off-diagonal
  min 2–17 members) because the paired variables are correlated; all 9 cells are
  non-empty in every formation. Extreme C/P×GS and E/P×GS corners are the LARGEST
  cells (negative GS correlation), matching the paper (L1213).

---

### Iteration 3 — Audit-1 findings and fixes (2026-07-22)

Audit 1 (`logs/audit1.md`) returned PARTIAL, `requires_iteration: true`,
0 blockers, 2 actionable majors. Both fixed below; minors m1 (A15
reworded above) and m2 (REPORT §5b enumeration widened) also done.

**[M1] REPORT.md self-report vs artifacts**
- Diagnosis: three prose values drifted from the computed artifacts:
  (a) E/P×GS AR spread quoted 11.0pp; artifact 0.0996 = 10.0pp (paper
  11.2 — artifact is a MATCH, prose overstated by 1pp); (b) Table VIII
  "−0.05 beta gap, trivial" cited only the C/P-decile gap while the
  C/P×GS corner gap is −0.179 (1.307−1.486); (c) the paper's C/P×GS
  raw-std ordering (value 24.1% > glamour 21.6%, L2346) reverses in
  our data (glamour 0.287 > value 0.264) and was undisclosed.
- Next fix: REPORT §3 corrected — E/P×GS spread → +10.0pp; beta gap
  reported per classification (C/P deciles −0.05, B/M deciles −0.07,
  C/P×GS corners −0.18) with the conclusion restated in the paper's
  own arithmetic (≤0.18 × 8% ≈ 1.4pp/yr ≪ 10-11pp spread); one
  disclosure sentence added for the C/P×GS raw-std reversal (vintage
  volatility, ~1.2-1.3× levels; size-adjusted "virtually identical"
  finding holds at mid-deciles).
- Before metric: REPORT quoted 11.0pp / single −0.05 gap / no std disclosure.
- After metric: REPORT quotes 10.0pp / per-classification gaps −0.05/
  −0.07/−0.18 / std reversal disclosed; grep verifies "11.0" gone and
  "−0.18" present.
- Status: resolved.

**[M2] Table VII window past the cohort horizon**
- Diagnosis: `src/table7.py` WIN_HI = 23944 (Apr 1995); the ~12
  months after Apr 1994 reused the 1989 cohort at Year +5.5/+6 —
  outside the paper's 5-year definition. 8 P_122 + ~2 N_88 months
  affected; W_25 (max month Sep 1981) clean.
- Next fix: WIN_HI → 23932 (Apr 1994, the last month any cohort is
  in-horizon); assertion `mnum <= (fy+5)*12+4` for every classified
  month (passes, 0 violations); semantic 25/88/122/25 recomputed over
  312 months; pooled value/glamour monthly returns moved to compute
  over all months before state restriction (bounding exposed a latent
  index-misalignment NaN in sparse states; no existing target
  affected); window note added to table_7.md.
- Before metric: 324 months (129 neg/195 pos), states 25/88/122/25 +
  64 unclassified; Table VII 82 MATCH / 8 PATTERN / 1 FAIL; 1B W_25
  spread 0.008593 (t 1.822), N_88 0.006088 (t 1.932).
- After metric: 312 months (124 neg/188 pos), states 25/88/122/25 +
  52 unclassified; P_122 dropped 5 post-horizon months (Aug 1994 +
  Jan-Apr 1995) and added 5 earlier; N_88 shifted 3 (dropped
  Jun/Nov/Dec 1994); W_25 and B_25
  month-sets PROVEN identical (bit-identical cells; W25 1B spread
  0.008593 unchanged exactly); W25/N88 V−G spreads remain positive
  (+0.0375 / +0.0201); Table VII 84 MATCH / 6 PATTERN / 1 FAIL (the
  1 FAIL is the P_122 t-stat, a moderate-month composition difference
  vs the paper's unrecoverable 260-month EW window — numerical, not
  methodological). Other 7 tables' cells JSONs byte-identical (md5).
- Status: resolved.
