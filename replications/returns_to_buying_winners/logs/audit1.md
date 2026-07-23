---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 4
requires_iteration: true
---

# Audit Report 1 — returns_to_buying_winners

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** A methodologically exemplary replication of the committed scope (Tables I–IV + VII, 791 cells): the headline machinery was independently recomputed by the auditor from `data/panel.parquet` to 6-dp exactness, the delisting evidence chain was re-verified against `dsedelist`/`msf`, and a full pipeline re-run is bit-identical. No blockers. The four actionable majors are all uncomputed paper corollaries (back-test §VII, earnings §VIII, decomposition §III, subperiods/win-rates Tables V–VI) whose data the replicator already verified available.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | All six checks pass (formation sort, EW deciles, K-cohort overlap, monthly rebalancing, PIT universe, iid/NW conventions) — auditor recomputed PA 6/6 from the parquet and got 0.011530 exactly; every deviation (A1–A12) is logged with paper-grounded rationale; the only unverifiable element is the Panel A F-stat construction (P20, 7 secondary cells, 3 variants evaluated). |
| Headline matching | 4 | Sign, shape, and significance replicate everywhere; central 6/6 buy-sell +21.4% (0.011530 vs 0.0095 — auditor-recomputed) sits at the edge of the ~20% band, driven entirely by the sell leg; buy leg +2.1%, buy t 4.36 vs 4.33, decile means monotone, event-time inverted-U and January effect reproduce. |
| Data coverage | 4 | Exact stated window (1962-07→1989-12 vintage; 1965–1989 reporting, 300 months); NYSE+AMEX common-stock universe ≈2,000–2,500/month (paper prints no count; Table III group sizes of ≈2,150/month are historically consistent); CRSP daily + FF factors exactly as paper; one documented substitution (2026 vs 1990 CRSP vintage). |
| Concrete result matching | 4 | 680/791 Tier 1 (86.0%) under the stated SE-based tolerances (consistent with `rep/TOLERANCE_RULES.md` 2SE/3SE picker); 98.6% Tier 1+2; all 11 FAILs are cells the paper itself prints as statistically nil (|t| ≤ 0.59 or α ≈ 0.0000) — verified. Sensitivity: uniform ±25% gives 67.6% Tier 1; strict rubric 2×/sign rule on Tier 2 gives 55 "FAIL"s dominated by yr-2/3 event-month noise and the 7 F-stats. |
| Signal strength | 4 | Headline-cluster mean ratio 1.057 (PA 6/6 1.214, PA 12/3 1.049, PB 12/3 0.925, PB 6/6 1.070, C_12 1.059, buy leg 1.021); the single worst anchor (1.214) is barely outside [0.8,1.2]; all 32 zero-cost spreads positive and significant, Sharpe 0.83 (auditor-recomputed). |
| Corollary | 3 | Subsample stability (size + SW-beta), risk non-explanation (post-ranking betas, market-model alphas), footnote-11 beta returns (auditor re-ran the beta SQL: 1.53/1.42/1.08 exact), seasonality, and event-time reversal all replicate — but §VII back-test, §VIII earnings (an abstract claim), §III decomposition statistics, and Tables V/VI are uncomputed despite verified-feasible data. |
| 7 | SUMMARY.md matches results/table_*.md | ✓ | Every REPORT/table anchor spot-checked (6/6 anchors, Jan/Feb–Dec, C_12/C_36, betas, mcaps, footnote-11) reproduces from `results/table_*.md` and `computed_values.json`; the §3 extra diagnostics (Sharpe 0.83, total return 2078.0%, MDD −41.9%, FF5 α 16.84% t 4.86, R² 0.13, geometric 13.12%) were independently recomputed by the auditor — all exact under the documented specs (see m2/m3 for two wording/persistence nits). |

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

- [M1] Corollary 'back-test 1927–1964' not computed in artifacts (actionable: true)
  - Paper: §VII, Table VIII, L1577–1595 — the paper replicates its Table VII event-time test on 1927–1940 (month 1 ≈ −5%, cumulative −40.81% at month 36, beta ≈ −0.5) and 1941–1964 ("very similar" to 1965–1989, dissipated by month 24). This is the paper's out-of-sample robustness result.
  - File: absent from `results/`; feasibility verified in `logs/log1.md` pre-flight (dsf/dsi span from 1925-12-31).
  - Specific fix: extend the `compute_table5` machinery to cohorts formed 1927-01..1940-12 and 1941-01..1964-12 (panel formation window back to ≈1926-07; sanity-check dsenames PIT coverage pre-1962 and note any universe thinning); write `results/table_6_backtest.md` with the 36 monthly + cumulative cells and NW t-stats per Panel A/B; append contract cells or cite the table as an extension.

- [M2] Corollary 'earnings-announcement returns' not computed in artifacts (actionable: true)
  - Paper: §VIII, Table IX, L2058–2060; this is an **abstract-level claim** ("A similar pattern of returns around the earnings announcements of past winners and losers is also documented"): past winners earn higher 3-day (days −2..0) announcement returns in the first 7 post-formation months, past losers higher in each of the following 13 months. Sample 1980–1989, Compustat quarterly industrial file.
  - File: absent from `results/`; feasibility verified (`comp_202601.fundq.rdq`: 145,650 announcements 1980–1989; `ccmxpf_linktable` link present — `preparations/data_verification.json`).
  - Specific fix: build the winner/loser decile cohorts (1980–1989 formations from the existing panel), join `fundq.rdq` via the link table, compute 3-day CARs (days −2..0) per announcement within 36 months of formation, average by (decile, post-formation month); write `results/table_7_earnings.md`.

- [M3] Corollary 'profit decomposition' not computed in artifacts (actionable: true)
  - Paper: §III.A/C/D — WRSS profits 4.5% per half-year (t 2.99, correlation 0.95 with the 6/6 strategy, L367); serial covariance of the EW index −0.0028 (L444); average serial covariance of market-model residuals +0.0012 (L458); squared-lagged-market regression θ = −2.29 (t −1.74; halves −2.55/−1.83, L526). These underpin the paper's central causal claim that profits are neither systematic risk nor common-factor lead-lag.
  - File: absent from `results/`; all inputs available (dsi EW/VW indexes, the auditor-verified 6/6 series, rf).
  - Specific fix: compute the four statistics from `dsi` + the existing panel (WRSS = cross-sectional covariance weighting by past-return-minus-EW-index; residual serial covariances from per-stock market-model residuals; NW-t regression of 6/6 cohort returns on squared demeaned 6-month VW index returns); write `results/table_8_decomposition.md`.

- [M4] Corollary 'subperiod stability and win rates' not computed in artifacts (actionable: true)
  - Paper: Table VI (5-year subperiod means; profits positive in 4 of 5 subperiods, the 1975–79 negative driven by small-firm January, L1120–1238) and Table V (positive-month proportions 0.67 all / 0.71 ex-January, L907). Both are corollary stability claims.
  - File: absent from `results/`; **zero new data or machinery required** — both derive trivially from the already-computed PA 6/6 calendar-month series (bit-identical to Table I, asserted at `src/main.py` t4 path) and the existing size-tercile series.
  - Specific fix: slice the existing 300-month zero-cost series (All/S1/S2/S3) into 1965–69…1985–89 (All/Jan/Feb–Dec rows) and compute positive-month proportions per calendar month; append to `results/table_4.md` or `results/table_4_subperiods.md`.

- [M5] Panel A F-statistics (7 cells) outside tolerance — paper's construction unidentified (actionable: false)
  - Evidence: ours 0.44–0.98 (stacked-dummies on overlapping monthly decile series) vs paper 1.69–4.51 (`results/table_3.md:24`); per-cohort ANOVA (2.18–4.15) and multivariate Wald (1.88–4.67) bracket the paper's range with no cell-exact match (P20, `preparations/assumptions.md:566-583`). Three fix variants evaluated — the exit-gate fix-attempt evidence is satisfied. The decile means the F-tests are about DO replicate (Table III Panel A).
  - Why non-actionable: paper-side ambiguity on overlapping-series F construction; a fourth variant would chase noise; all three plausible constructions are reported transparently.

- [M6] Residual sell-side shortfall classified as CRSP vintage drift (A12) — classification accepted (actionable: false)
  - Evidence: 6/6 sell −21.2% vs paper (0.006227 vs 0.0079); C_36 +71.7% (0.0697 vs 0.0406); our monthly spread std 0.0479 vs paper-implied 0.0537 (variance-side counterpart). Auditor verification of the classification: (i) buy side matches the paper <2% across all 32 cells — machinery correct; (ii) the A3 revision is faithful, not convenient — auditor re-ran the double-count test on 12 independent month-end delistings 1965–66: `msf.ret` equals the raw daily compound in 12/12 (|D−M| ≤ 8e-4) and the dlret-adjusted value in 0/12, and the permno-37882 hand trace reproduces exactly ((1+D)(1+dlret)−1 = −0.454546); (iii) the quantified fix attempt is real — sell_diagnostic.md arithmetic re-verified: excluding no-msf stock-months closes (0.006625−0.006227)/(0.0079−0.006227) = 23.7% of the gap; (iv) direction consistent with Shumway (1997) on this paper's vintage. This is an earned documented partial, not diagnose-and-skip.
  - Why non-actionable: the 1990 CRSP vintage is unavailable, so the vintage hypothesis cannot be falsified directly. If a future iteration runs for M1–M4 anyway, one cheap bounding test is worth doing: recompute the PA 6/6 sell on the exchange-code-only universe (drop the shrcd filter, +174 names/month per `results/sell_diagnostic.md:36-49`) to quantify the universe-scope contribution to the residual.

### Minor (cleanup)

- [m1] Classification hygiene: 8 T5 cells are labeled "Tier 2" with the **opposite sign** from the paper (event_t22/t23/t30/t35 monthly + their t-twins; e.g., `event_t22_monthly` paper −0.0034 vs ours +0.000129), while 11 cells with the same near-zero sign-flip behavior were labeled FAIL. `rep/TOLERANCE_RULES.md` defines opposite sign as FAIL — the rule is applied inconsistently (all 8 are yr-2/3 noise with paper |t| ≤ 1.39, so economically immaterial; grand totals move to 680/92/19 under consistent application). Document the near-zero classification rule in code.
- [m2] The REPORT.md §3 diagnostics (Sharpe 0.83, total return 2078.0%, MDD −41.9%, FF5 α 16.84% t 4.86, R² 0.13, geometric 13.12%) are not persisted in `computed_values.json` or any `table_*.md`. Auditor recomputed every one independently — all exact, including FF5 α (intercept of the RAW zero-cost return on FF5 factors, consistent with the P18 zero-cost convention; the rf-subtracted variant gives 10.05%, t 2.90 — the spec should be stated explicitly). Persist them with their specs.
- [m3] REPORT.md §3 wording conflates compounding conventions: "Compounded annualized return 13.12% … ours from 0.01153 is 13.12%" — 13.12% is the realized GEOMETRIC annualization (2078.0% over 300 months → 21.78^(12/300)−1); (1+0.01153)¹²−1 = 14.75%; the paper's 12.01% is arithmetic from its monthly mean. Reword to a like-for-like comparison (arithmetic 14.75% vs 12.01%, or geometric-vs-geometric with the paper's geometric not reported).
- [m4] `results/table_*.md` carry anchor-check blocks but not per-cell evaluation blocks; per-cell status lives only in `cell_classification.json`. Surface the per-table tier counts in each table md.
- [m5] The central cell's tolerance (PA_J6_buy_sell_K6, 98% ≈ 3SE under TOLERANCE_RULES deviation rule #1) is looser than deviation rule #3 recommends for "the paper's central claim" (tighten). No status consequence here (+21.4% passes the 30% spread default too), but future contracts should tighten the headline cell so it carries weight in the hit-rate.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Table III Panel A 'All' decile means strictly increasing 0.0062→0.0178 (auditor-recomputed series); buy > sell in all 32 Table I strategies; beta-group spreads increasing in beta (0.79/1.08/1.33) as the paper claims. |
| 2 | Headline-magnitude claim | ✓ | Auditor's from-scratch recomputation from `data/panel.parquet` (independent code, floor-rank/permno-tie deciles, K=6 overlap average, 300 months): PA 6/6 buy-sell **0.011530**, t 4.1665, std 0.047929, sell 0.006227, buy 0.017757 — all identical to `computed_values.json` to 6 dp; vs paper 0.0095 = +21.4% (buy leg +2.1%). |
| 3 | Sample coverage ≥ 60% | ✓ | `cumret_6_raw` non-null 95.8% of 1965–89 panel rows; every one of the 300 reporting months has exactly K=6 contributing cohorts in all 32 grids (asserted; auditor re-derivation confirmed ncoh=6 for every month); ≈2,000–2,500 stocks/month. |
| 4 | Data-source choice justified | ✓ | A3-revision evidence chain independently re-verified: 12/12 month-end delistings (1965–66, dlret non-null, msf row present) have msf.ret = raw daily compound (max |D−M| 8e-4) and ≠ (1+D)(1+dlret)−1; permno 37882 (1962-10, dlstcd 582) reproduces −0.454546 exactly; the unadjusted series is the one consistent with the paper's stated compounding (L139) and CRSP's own monthly file. |
| 5 | prep_validation.py exit 0 | ✗→✓ | Exit 1 on arrival, but the only two errors were the auditor's own missing deliverables ("REPORT.md exists but no logs/audit*.md"; "SUMMARY.md missing"). Prep contract itself validates; exit 0 confirmed after writing audit1.md + SUMMARY.md. |
| 6 | All committed tables have results files | ✓ | T1–T5 → `table_1.md`…`table_5.md`; `computed_values.json` has exactly 791 keys, zero mismatches vs `cell_classification.json` 'ours' values. |
| 7 | SUMMARY/REPORT values match results | ✓ | 12+ anchor values traced to `table_*.md`/`computed_values.json`; §3 extra diagnostics all independently recomputed (Sharpe 0.83, total return 2078.0%, MDD −41.9%, geometric 13.12%, FF5 α 16.84% t 4.86, R² 0.13 — exact). Caveats: m2 (not persisted), m3 (wording conflates geometric/arithmetic). |
| 8 | No orphan folders | ✓ | Slug root: data/, inputs/, logs/, preparations/, results/, src/, REPORT.md only (src/__pycache__ is normal). |
| 9 | Diagnoses paired with fix attempts | ✓ | All five inner-iteration log entries in `assumptions.md` carry Diagnosis/Next fix/Before/After/Status; the iteration-4 residual exit gate is satisfied with a quantified fix attempt (sell 0.006227→0.006625, 23.7% of gap closed — arithmetic re-verified by auditor). |
| 10 | Tier 2 within 2× magnitude | ✗ (immaterial) | Under the rubric ratio rule, 44/100 Tier-2 cells fall outside [0.5, 2.0] — 8 of them sign-opposite (should be FAIL under the repo's own rule, m1). Every one is an economically nil cell: yr-2/3 event months (paper |t| ≤ 1.4), the 7 Panel A F-stats (M5), 3/3-strategy cells (paper t 1.10), and ≈0.000-magnitude Panel B alphas. No economically meaningful cell is affected under either convention. |
| 11 | Corollary coverage | ✗ | Verified: subsample stability (size + SW beta), risk non-explanation (betas, market-model alphas), footnote-11 beta returns (auditor re-ran `sw_beta_yearly.sql`: 1.53/1.42/1.08 — exact match to the agent, vs paper 1.48/1.39/1.16), seasonality, event-time reversal. Missing (→ M1–M4): §VII back-test, §VIII earnings, §III decomposition, Tables V/VI — all with verified-feasible data. |

**Pipeline determinism:** full re-run of `uv run python replications/returns_to_buying_winners/src/main.py` (exit 0) reproduced all seven hashed artifacts **bit-identically** (md5-verified: computed_values.json, cell_classification.json, table_1..5.md).

## 4. Issues the agent should have caught (didn't)

1. The 8 sign-opposite T5 cells labeled "Tier 2" instead of FAIL — the agent applied its own sign rule inconsistently between event months 1/12/31 (FAIL) and 22/23/30/35 (Tier 2), despite identical near-zero sign-flip behavior (m1).
2. The REPORT §3 arithmetic/geometric conflation — "(1+0.01153)¹²−1" is 14.75%, not the stated 13.12% (m3); a careful reader of the report will stumble on this.
3. Table VI 5-year subperiods and Table V win rates were free: both fall out of the already-computed, bit-identical calendar-month series with a 20-line groupby. Listing them as "future work" understates how cheap they are — they would have directly evidenced subperiod stability (a core corollary) at essentially zero cost (M4).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Returns to Buying Winners and
Selling Losers: Implications for Stock Market Efficiency" (Jegadeesh &
Titman 1993) for slug `returns_to_buying_winners`. The previous agent
run completed with verdict **PARTIAL** (audit 1 at
`replications/returns_to_buying_winners/logs/audit1.md`). Read the
audit first.

State of the replication: the committed 5 tables (791 cells) replicate
well — 86% Tier 1, 98.6% Tier 1+2, headline 6/6 buy-sell +21.4% with
the buy leg at +2.1%, pipeline bit-identical across re-runs, and the
auditor independently re-verified the headline machinery (exact to 6
dp), the delisting evidence chain (12/12 msf = raw daily compound),
and the footnote-11 beta cross-check. No blockers. This iteration is
about the four uncomputed paper corollaries — all with data the
previous run already verified available — plus three cleanup nits.

## Issues to address (priority order)

### [M1] — MAJOR — corollary: Table VIII back-test 1927–1964
Paper §VII (L1577–1595) replicates the Table VII event-time test on
1927–1940 (month 1 ≈ −5%, cumulative −40.81% at month 36) and
1941–1964 ("very similar" to 1965–1989, positive cumulative
dissipating by month 24). Data verified: dsf/dsi span from 1925-12.

**Specific fix:**
1. Extend the panel's formation window back to ≈1926-07 (panel rebuild;
   sanity-check dsenames PIT coverage pre-1962 and report stocks/month
   by decade — the universe thins in the 1920s/30s; if dsenames windows
   are unreliable pre-1962, document and use the raw dsf+shrcd/exchcd
   file state, logged in assumptions.md).
2. Reuse `compute_table5` for cohorts formed 1927-01..1940-12 (Panel A)
   and 1941-01..1964-12 (Panel B): 36 monthly + cumulative cells, NW
   cumulative t-stats, same A10 convention.
3. Write `results/table_6_backtest.md` with anchor checks vs Table VIII
   (month 1 ≈ −0.0495, C_36 = −0.4081 for Panel A; sign pattern for
   Panel B). Add the cells to the contract and reclassify.

### [M2] — MAJOR — corollary: Table IX earnings-announcement returns
Paper §VIII (L2058–2060), an ABSTRACT-level claim: past winners earn
higher 3-day (days −2..0) announcement returns in months 1–7 after
formation, past losers higher in each of the following 13 months.
Sample 1980–1989. Data verified: comp_202601.fundq.rdq (145,650
announcements), ccmxpf_linktable present.

**Specific fix:**
1. Form winner/loser decile cohorts monthly 1980-01..1989-12 from the
   existing panel (cumret_6_raw signal).
2. Join gvkey via ccmxpf_linktable (PIT: linkdt ≤ rdq ≤ linkenddt),
   pull fundq.rdq announcements within 36 months of formation, compute
   3-day dsf returns days −2..0 around each rdq.
3. Average by (decile, post-formation month 1..20); write
   `results/table_7_earnings.md` with the paper's sign pattern check
   (winner > loser months 1–7; loser > winner months 8–20).

### [M3] — MAJOR — corollary: §III profit decomposition
The paper's causal claim (profits ≠ systematic risk ≠ common-factor
lead-lag) rests on four in-text statistics: WRSS profits 4.5%/half-year
(t 2.99, L367); EW-index 6-month return serial covariance −0.0028
(L444); average market-model-residual serial covariance +0.0012 (L458);
squared-lagged-market regression θ = −2.29 (t −1.74; halves −2.55/−1.83,
L526, NW t per L526).

**Specific fix:**
1. WRSS: at each formation, weight stocks by (past 6-month return −
   past EW-index 6-month return); profit = mean weighted 6-month
   forward return; report semiannual mean and t.
2. Serial covariances from dsi.ewretd (compounded to 6-month) and from
   per-stock market-model residuals (vs VW) — cross-sectional average.
3. θ-regression: 6/6 cohort returns on the squared demeaned 6-month VW
   index return (full sample + two halves), NW t (A5).
4. Write `results/table_8_decomposition.md` with the four anchors.

### [M4] — MAJOR — corollary: Table VI subperiods + Table V win rates
Both fall out of the ALREADY-COMPUTED PA 6/6 calendar-month series
(bit-identical to Table I) — no new data, no new machinery.

**Specific fix:**
1. Slice the 300-month zero-cost series (All/S1/S2/S3, already in the
   Table IV path) into 65–69, 70–74, 75–79, 80–84, 85–89; report All /
   Jan / Feb–Dec means + iid t per group vs Table VI (e.g., All 75–79
   paper −0.0044 (−0.51)).
2. Positive-month proportions per calendar month and All/ex-Jan (paper
   0.67 / 0.71) vs Table V.
3. Append to `results/table_4.md` (or `results/table_4_subperiods.md`);
   add contract cells.

### [m1] — MINOR — classification hygiene
8 T5 cells (event_t22/t23/t30/t35 monthly + t-twins) are labeled
"Tier 2" with the OPPOSITE sign from the paper, while the identical
behavior at months 1/12/31 was labeled FAIL. Apply the sign rule
consistently (these become FAIL — all are yr-2/3 near-zero noise, so
the change is cosmetic) and document the near-zero classification rule
wherever cell_classification.json is generated.

### [m2] — MINOR — persist the §3 diagnostics
Add the REPORT §3 diagnostics (Sharpe, total return, max drawdown,
geometric annualized, FF5 alpha + t + R²) to computed_values.json (or
a diagnostics block in table_1.md) WITH the FF5 spec stated: intercept
of the RAW zero-cost return on the five FF factors (zero-cost
convention per P18; the rf-subtracted variant gives 10.05%/yr, t 2.90).

### [m3] — MINOR — fix the compounding wording
REPORT.md §3: 13.12% is the realized geometric annualization
(2078%^(12/300)−1), NOT (1+0.01153)¹²−1 (which is 14.75%). Reword to
compare like-with-like against the paper's arithmetic 12.01%.

### If this iteration runs anyway (optional, bounded)
- [M6] bounding test for the A12 residual: recompute the PA 6/6 sell on
  the exchange-code-only universe (drop shrcd, +174 names/month) and
  report how much of the 0.0017/mo sell gap the universe scope
  explains. Do NOT adopt a non-common-share universe as primary
  whatever the result — this is attribution only.
- [M5] Panel A F-stats: only revisit if you find a paper-side citation
  for the construction; three variants are already reported (P20).

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry
  in `assumptions.md` must have all five fields: Diagnosis, Next fix,
  Before metric, After metric, Status. The previous run's log is a good
  template (every entry complete, fix attempts quantified).
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Diagnoses must be paired with fix attempts (exit gate).** Before
  declaring done, walk `assumptions.md` and verify every diagnosed
  problem has a log entry with a non-empty Next fix and a before/after
  metric.
- Keep the delisting treatment as-is (A3 revision, primary =
  unadjusted) — the auditor re-verified the evidence chain (12/12 msf
  = raw daily compound; permno 37882 hand trace exact). Do not reopen
  it without new evidence.

## Inputs you should read

- `replications/returns_to_buying_winners/logs/audit1.md` — this audit
- `replications/returns_to_buying_winners/inputs/content.md` — paper
  (§VII L1577+, §VIII L2050+, §III L360–530, Tables V/VI L1070–1238)
- `replications/returns_to_buying_winners/preparations/` — prep
  contract + assumptions.md (A1–A12, P1–P20)
- `replications/returns_to_buying_winners/src/main.py` — current code
  (extend; the Table V/IV path already has every series M4 needs)
- `replications/returns_to_buying_winners/data/` — cached panel
  (recompute spot-checks from these; extend the formation window only
  for M1)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is the same.
- Skip `scripts/prep_validation.py` until you add contract cells for
  the new tables (it passed at audit 1 once the auditor files landed).
- Skip the ClickHouse catalog scan — `data_verification.json` already
  verified dsf/dsi (from 1925-12), fundq.rdq, and the CCM link.
- Do NOT re-verify the Table I–VII machinery — bit-identical across
  re-runs (md5-verified by the auditor). Only re-run sanity checks you
  add or modify.

## Deliverables for this iteration

- `replications/returns_to_buying_winners/src/main.py` — extended with
  the four corollary computations, logged per issue above
- `replications/returns_to_buying_winners/results/table_6_backtest.md`,
  `table_7_earnings.md`, `table_8_decomposition.md`, and the
  subperiod/win-rate extension of `table_4.md` (one per M1–M4), each
  with anchor checks vs the paper and the paper location cited
- `replications/returns_to_buying_winners/preparations/assumptions.md`
  — append an iteration log entry for every issue addressed (five
  fields each), including any pre-1962 universe decision for M1
- `replications/returns_to_buying_winners/SUMMARY.md` — read the
  latest combined assessment; do NOT edit (auditor-owned)
- `replications/returns_to_buying_winners/REPORT.md` — updated; lead
  with the data-quality summary and add the corollaries evaluated this
  iteration; apply the m2/m3 fixes

## Stop conditions

- **M1–M4 computed and anchor-checked, m1–m3 fixed** → re-run
  prep_validation.py and sanity checks → declare success with any
  remaining deviations documented; the next audit updates SUMMARY.md.
- **A corollary's data turns out NOT to support computation** (e.g.,
  dsenames PIT coverage pre-1962 is unusable for M1) → document the
  block in assumptions.md with the evidence and declare partial for
  that table; do not fabricate.
- **10-iteration cap reached** on a single problem → escalate to the
  human; do not edit SUMMARY.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is one of the most rigorously verified replications I have audited. The diagnostic discipline is exceptional: every table's construction was hand-verified to <1e-12 on individual cohorts, the delisting decision was driven by empirical evidence (K-monotone sell-shift fingerprint → A3 revision) rather than convenience, and the fix attempt on the residual sell shortfall was quantified before classification rather than waved away. My independent checks confirmed the load-bearing claims exactly: the headline series recomputed from the parquet to 6 dp, the double-count test re-ran 12/12 in the agent's favor, the footnote-11 cross-check reproduced after re-executing the beta SQL, and the full pipeline re-run was bit-identical. The A3 revision deserves explicit endorsement: using the unadjusted series is the *faithful* choice — the paper compounded daily returns on a 1990 vintage that could not have contained dlret, and CRSP's own monthly file on the current vintage excludes it too; adjusting would replicate what the paper should have computed, not what it did. The replication's honest weaknesses are scope, not correctness: four paper corollaries (two of them full tables with verified-feasible data, one of them an abstract-level claim) were scoped out as stretch targets, and two of those (Tables V/VI) were nearly free from existing series. The +21.4% central-spread deviation is real but well-characterized — it sits on the sell leg, whose 1990-vintage location the replication cannot recover, and the buy side matches at 2.1%. One systemic observation for the pipeline: the per-cell tolerances follow the SE-based picker (good), but the central cell's 98% tolerance illustrates how 3SE tolerances can make the headline carry less weight than TOLERANCE_RULES deviation rule #3 intends — the cell passes at 30% anyway, so no harm here.
