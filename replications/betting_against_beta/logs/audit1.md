---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 5
requires_iteration: true
---

# Audit Report 1 — betting_against_beta

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Headline BAB factor replicates within tolerance on all 8 metrics and the run is fully deterministic (auditor re-ran `table_3_v2.py` → byte-identical `table_3.md`). No blockers. The replication is trustworthy on the central claim but leaves the paper's named corollaries (subsample stability, factor loadings, size/IVOL splits, robustness) uncomputed and 7 decile multi-factor alphas outside Tier 1. Five actionable majors → `requires_iteration: true`.

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4/5 | Beta estimation (1y vol / 5y corr / 3-day overlap / 120-750 minima / Vasicek w=0.6→1) and BAB construction (median split, rank weights, unit-beta rescale, Eq. 16/17) match the paper exactly; deviations (Shumway/BMP delisting, PIT exchcd filter, `dlret=-1.0` as missing, Case-B delist timing) are all paper-silent and documented. |
| Headline matching | 5/5 | BAB (the central claim) matches within 5% on all 8 cells (FF3 α 0.748 vs 0.73; Sharpe 0.75 vs 0.78; leverage 1.44/0.69 vs 1.40/0.70); monotonic Sharpe/alpha decline and flat SML reproduce in shape and sign. |
| Data coverage | 4/5 | Universe 23,407 vs 23,538 stocks (0.6% off), June mean ME 0.996 vs 0.99 $B, sources (CRSP dsf/msf/dsi/dsenames/dsedelist + FF) all match; period end exact but effective start 1928-08 vs 1926-01 (750-day beta warmup). |
| Concrete result matching | 4/5 | 25/32 cells Tier 1 (78.1%); the 7 fails are decile FF3/FF4 (and P10 CAPM) alphas — 6 keep sign and stay within 2× (Tier-2-eligible), P10 FF4 flips sign (0.03 vs −0.13). All 8 BAB cells Tier 1. |
| Signal strength | 5/5 | Headline cells r=|ours/paper|: BAB FF3 α 1.025, FF4 α 1.047, Sharpe 0.962, excess ret 1.021 — all in [0.9,1.1]. |
| Corollary | 2/5 | Decile cross-sectional pattern replicates, but none of the paper's named corollaries are computed: subsample stability (four 20-yr subperiods), BAB factor loadings (Table B1), size/IVOL splits (Tables B3/B5), beta-window robustness (Table B2), TED time-series (Table 9). |

**Overall: 4.00 / 5.00 → binary verdict `REPLICATED`** (mean ≥ 3.0, no dimension scored 1).

## 2. Issues by severity

### Blockers (must fix)

None. (The current `prep_validation.py` exit 1 is solely because `logs/audit1.md` and `SUMMARY.md` do not yet exist — both are produced by this audit; the contract itself is otherwise clean.)

### Major (should fix)

- [M1] Corollary 'subsample stability' not computed in artifacts
  - File: `inputs/content.md` p.2 (abstract) — BAB "realizes a significant positive return in each of the four 20-year subperiods between 1926 and 2012"; also Table B4.
  - Paper claim: the US BAB factor is significantly positive in each of four 20-year subperiods.
  - Artifact needed: a subsample table of BAB excess return / FF3 α / FF4 α / Sharpe over ~1926-1946, 1946-1966, 1966-1986, 1986-2012 (e.g. `results/table_3_subsample.md`). Computable from the existing `panel.parquet` + FF factors — no new data required.
  - Specific fix: split the monthly BAB series (already produced by `bab_factor()` in `src/table_3_v2.py`) into four subperiods and report α/Sharpe per subperiod vs the paper.
  - actionable: true

- [M2] Corollary 'BAB factor loadings' computed but not reported
  - File: `inputs/content.md` Table B1 + p.9 ("relative to high-beta stocks, low-beta stocks are likely to be larger, have higher book-to-market ratios, and higher return over the prior 12 months").
  - Paper claim: US BAB goes long $1.40 / short $0.70 with realized SMB/HML/UMD loadings that do not explain the alpha.
  - Artifact needed: realized factor loadings (mkt, SMB, HML, UMD) for the BAB factor and the deciles. The FF3/FF4 regressions are already run in `portfolio_row()`; only the alpha is retained and the loadings are dropped.
  - Specific fix: in `src/table_3_v2.py:portfolio_row` also capture `capm0["betas"]`/`ff3_0["betas"]`/`ff4_0["betas"]` and emit a loadings block (leverage already verified: long 1.435 / short 0.688).
  - actionable: true

- [M3] Corollary 'cross-sectional variation' not computed (size / idiosyncratic-vol splits)
  - File: `inputs/content.md` Table B3 (size splits) and Table B5 (control for idiosyncratic volatility); abstract/p.2 ("consistent ... within deciles sorted by size, and within deciles sorted by idiosyncratic risk").
  - Paper claim: BAB holds within size deciles and after controlling for idiosyncratic volatility.
  - Artifact needed: BAB α/Sharpe within size groups (uses the existing `me` column, lagged one month) and a BAB-with-IVOL-control spec.
  - Specific fix: add `results/table_3_size.md` computing BAB within large/mid/small size terciles from the panel; flag IVOL if the daily residual-vol computation is out of reach this iteration.
  - actionable: true

- [M4] Corollary 'robustness specs' not computed (beta windows / benchmark)
  - File: `inputs/content.md` Table B2 (different beta window lengths and local vs global benchmarks) and §3.1 ("results are robust to alternative beta estimation procedures").
  - Paper claim: BAB is robust to alternative beta-estimation windows and benchmark choice.
  - Artifact needed: BAB re-estimated under at least one alternative (e.g., monthly-data beta, or a different correlation window) — `results/table_3_robustness.md`.
  - Specific fix: parameterize `CORR_WINDOW`/`VOL_WINDOW` in `src/main.py`, rebuild one alternative beta, and report BAB α/Sharpe delta.
  - actionable: true

- [M5] Decile multi-factor alphas systematically too high; P10 four-factor alpha flips sign
  - File: `results/table_3.md:62-79` — P1 FF3 0.486 vs 0.40 (+21.6%), P5 FF3 0.214 vs 0.13 (+64.6%), P10 FF3 −0.346 vs −0.49 (+29.4%), P10 FF4 0.030 vs −0.13 (sign flip, +123%), P10 CAPM −0.078 vs −0.10 (+22.2%).
  - Paper claim: decile alphas decline to about −0.49% (P10 FF3) and −0.13% (P10 FF4).
  - Diagnosis so far: agent attributes the gap to sample-start (1928-08 vs 1926-01), data vintage, and beta-estimation subtleties (assumptions.md A22). Partially a data-vintage ceiling, but the P10 FF4 sign flip is a concrete outlier worth isolating.
  - Specific fix: run the decile alphas restricted to the paper-comparable post-1962 sub-window (where the momentum factor and vintage are better aligned) to test whether the P10 FF4 sign flip is an early-sample artifact; document the residual as vintage-limited.
  - actionable: true (investigation; residual likely data-vintage-limited)

Non-actionable (data-limited, already documented — do NOT block the loop):
- 5-factor alpha — Pastor-Stambaugh liquidity factor not in ClickHouse (Assumption 2; paper covers 1968-2011 only).
- International equities (Tables 4-5) — Xpressfeed Global not in ClickHouse.
- Other asset classes (Tables 6-8: Treasuries, credit, futures) — proprietary data not available.
- TED-spread time-series (Table 9, Proposition 3) and beta-compression (Proposition 4) — TED series (from 1984) likely not in ClickHouse.
- Constrained-investor holdings (Proposition 5, Tables 10) — mutual-fund/brokerage/LBO/13F data not available.

### Minor (cleanup)

- [m1] Stale/orphan pipeline artifacts. `results/panel_diagnostics.md` describes a 9-column panel (2,442,622 rows; cols `beta_ts, hexcd_eom, n_vol12, n_corr60`) and references SQL files `bab_mkt_daily.sql, bab_daily_univ.sql, bab_monthly_stats.sql, bab_panel.sql, panel_pull.sql` that do not exist in `src/sql/`. `src/build_panel.py` (the generator, per `logs/build_panel_run3-5.log`) is superseded by the current `src/main.py`, which produces the actual 6-column, 3,180,822-row `data/panel.parquet` (confirmed by `data/pipeline_summary.txt`).
  - Specific fix: delete or archive `results/panel_diagnostics.md` and `src/build_panel.py` (and the `build_panel_run*.log` files) so the only documented pipeline is `main.py`.

- [m2] REPORT.md quotes v1 (pre-revision) BAB t-stats that do not match the final `table_3.md`. REPORT.md §2: "FF3 t-statistic is 7.28 ... FF4 t-statistic is 5.71"; final `table_3.md` (v2) shows iid FF3 t=7.11, iid FF4 t=5.54 (NW: FF3 5.71, FF4 4.44). The 7.28/5.71 pair is the v1 / NW mix from `logs/log1.md`. REPORT.md also lists BAB excess return 0.72 vs table 0.71 (rounding of 0.715).
  - Specific fix: update REPORT.md §2 BAB table to the v2 iid t-stats (7.11 / 5.54) and note the NW values separately.

- [m3] Committed Table 1 has no dedicated results file. `tables_to_replicate.json` commits to `T1` (US summary statistics) but there is no `results/table_1.md`. The T1 metrics are reported informally and DO pass on the full panel (auditor recomputed: total stocks 23,407 vs 23,538 = 0.6% off; June mean firm ME 0.996 vs 0.99 $B = 0.7% off; mean total June market cap 3,054 vs 3,215 $B = 5.0% off; start 1926 / end 2012 exact).
  - Specific fix: add `results/table_1.md` with a per-cell evaluation block citing these four metrics.

- [m4] `data_verification.json` maps the delisting requirement to table `crsp_202601.dse` (line 62), but the code actually reads `crsp_202601.dsedelist` (`src/sql/delisting.sql:18`, `src/table_3_v2.py`).
  - Specific fix: correct the `matched_table` for `crsp_delisting` to `crsp_202601.dsedelist`.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Reproduced `table_3.md`: Sharpe 0.73→0.30 monotonic P1→P10; alphas decline across CAPM/FF3/FF4; ex-ante beta 0.61→1.77 increasing. |
| 2 | Headline-magnitude claim | ✓ | Auditor re-ran `src/table_3_v2.py` (exit 0, deterministic, byte-identical output): BAB FF3 α 0.748 vs 0.73, FF4 α 0.576 vs 0.55, Sharpe 0.75 vs 0.78, leverage 1.435/0.688 vs 1.40/0.70 — all within tolerance. |
| 3 | Sample coverage ≥ 60% | ✓ | 2,412,874/3,180,822 stock-months have a valid beta = 75.9%; analysis sample 1,004 months (1928-08..2012-03), ~2,403 stocks/month. |
| 4 | Data-source choice justified | ✓ | CRSP dsf/msf/dsi/dsenames/dsedelist + `ff.four_factor_monthly` all match the paper; exchcd filter (A10) and Shumway/BMP delisting (A1, paper-silent) documented in assumptions.md. |
| 5 | prep_validation.py exit 0 | ✗ | Exits 1 — but only because `logs/audit1.md` and `SUMMARY.md` are absent (created by this audit). No contract/data errors reported. Re-run after this write should pass. |
| 6 | All committed tables have results files | ✗ | `T3`→`results/table_3.md` ✓; `T1` committed but no `results/table_1.md` (metrics pass informally — see [m3]). |
| 7 | SUMMARY.md matches results/table_*.md | ✗ | SUMMARY.md absent (written here). Pre-existing REPORT.md cites v1 BAB t-stats (7.28/5.71) ≠ final table (iid 7.11/5.54) — see [m2]. |
| 8 | No orphan folders | ✓ | No literal-brace/shell-error folders at slug root. (Orphan files build_panel.py + panel_diagnostics.md flagged in [m1].) |
| 9 | Diagnoses paired with fix attempts | ✓ | `log1.md` inner-loop trace: v1 decile-alpha failures diagnosed (all-stock breakpoints + no delisting) → inner-iter-3 fix (NYSE breakpoints + delisting) → verified 23/32→25/32. assumptions.md pairs each decision with rationale/impact. |
| 10 | Tier 2 within 2× magnitude | ✓ | Agent labels all 7 out-of-tolerance cells FAIL (no Tier-2 inflation). 6 keep sign and stay within 2× (Tier-2-eligible); P10 FF4 is a genuine sign-flip FAIL. Labeling is conservative/honest. |
| 11 | Corollary coverage | ✗ | Subsample stability, BAB factor loadings, size/IVOL splits, beta-window robustness, and TED time-series are neither computed in artifacts nor surfaced as gaps → raised as [M1]-[M5]. |

## 4. Issues the agent should have caught (didn't)

1. **REPORT.md carries v1 t-stats into the "SUCCESS" writeup.** The headline section quotes FF3 t=7.28 / FF4 t=5.71, which are the v1 (all-stock, no-delist) and NW figures, not the final v2 iid t-stats (7.11/5.54) that `table_3.md` actually prints. A careful reviewer re-reading the final table against the report would catch the mismatch.
2. **No `results/table_1.md` for a committed table.** The agent committed to T1 in `tables_to_replicate.json` and even computed the matching numbers (stock count, ME), but never emitted the per-cell results file the contract implies.
3. **Left a superseded pipeline (`build_panel.py` + `panel_diagnostics.md`) referencing deleted `bab_*.sql` files.** The diagnostics file describes a 9-column panel that no longer exists and points at SQL that is gone — a reproducibility hazard for the next reader.
4. **`data_verification.json` still names `crsp_202601.dse`** for delisting while the code uses `dsedelist` — a stale catalog entry.
5. **Corollaries were silently scoped out.** The abstract's "significant positive return in each of the four 20-year subperiods" is a headline corollary computable from the existing BAB series, yet it was neither computed nor flagged as a gap.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Betting against beta" (Frazzini &
Pedersen, 2014) for slug `betting_against_beta`. The previous agent run
completed with verdict **PARTIAL** (audit 1 at
`replications/betting_against_beta/logs/audit1.md`). Read the audit first.

The headline result is solid: the US BAB factor replicates within tolerance
on all 8 Table 3 metrics (FF3 alpha 0.748 vs 0.73, t≈7.1; Sharpe 0.75 vs
0.78; leverage 1.44/0.69 vs 1.40/0.70), and your run is deterministic. This
iteration is about closing the corollary gaps and the decile-alpha drift —
NOT re-building the panel or the BAB factor (they work).

## Issues to address (priority order)

### [M1] — MAJOR — subsample stability corollary
Paper (abstract, p.2): BAB "realizes a significant positive return in each
of the four 20-year subperiods between 1926 and 2012" (also Table B4).

**Specific fix:**
1. Reuse the monthly BAB series already produced by `bab_factor()` in
   `src/table_3_v2.py` (do not recompute betas).
2. Split it into four ~20-year windows (e.g. 1928-08..1948, ..1968, ..1988,
   ..2012-03) and compute excess return, FF3 alpha, FF4 alpha, and Sharpe
   per window.
3. Write `results/table_3_subsample.md` with a per-cell block vs the paper's
   claim ("significant in each subperiod"). Verify: all four subperiod
   alphas should be positive and at least the later ones significant.

### [M2] — MAJOR — report BAB factor loadings (Table B1)
Paper (Table B1, p.9): BAB long $1.40 / short $0.70 with realized SMB/HML/UMD
loadings that do not explain the alpha.

**Specific fix:**
1. In `src/table_3_v2.py:portfolio_row`, capture the factor loadings already
   returned by `factor_alpha(...)` (`capm0["betas"]`, `ff3_0["betas"]`,
   `ff4_0["betas"]`) instead of dropping them.
2. Emit a loadings block (mkt, SMB, HML, UMD) for the deciles and BAB.
   Leverage is already verified (long 1.435 / short 0.688).
3. Extend `results/table_3.md` (or add `results/table_b1.md`) with the
   loadings and compare signs to the paper (low-beta stocks larger, higher
   B/M, higher prior momentum).

### [M5] — MAJOR — decile multi-factor alpha drift / P10 FF4 sign flip
`results/table_3.md:62-79`: P10 FF4 alpha = 0.030 vs paper −0.13 (sign flip);
P5 FF3 0.214 vs 0.13 (+65%); P10 FF3 −0.346 vs −0.49 (+29%).

**Specific fix:**
1. Re-run the decile alphas restricted to a paper-comparable post-1962
   sub-window (momentum factor well-populated, vintage aligned) to test
   whether the P10 FF4 sign flip is an early-sample artifact.
2. If it persists, test one alternative beta window (see [M4]) as the likely
   driver. Document the residual as data-vintage-limited in REPORT.md and
   assumptions.md (Diagnosis / Next fix / Before / After / Status).

### [M3] — MAJOR — cross-sectional robustness (size split, Table B3)
**Specific fix:** add `results/table_3_size.md` computing BAB alpha/Sharpe
within large/mid/small size terciles using the existing `me` column (lag `me`
one month to avoid look-ahead — see assumptions.md A9). Flag IVOL control
(Table B5) as out-of-scope this iteration if the daily residual-vol
computation is not reachable.

### [M4] — MAJOR — beta-estimation robustness (Table B2)
**Specific fix:** parameterize `CORR_WINDOW`/`VOL_WINDOW` in `src/main.py`,
rebuild ONE alternative beta (e.g., shorter correlation window), and report
the BAB alpha/Sharpe delta in `results/table_3_robustness.md`.

### Minors — cleanup
- [m1] Delete/archive `results/panel_diagnostics.md`, `src/build_panel.py`,
  and `logs/build_panel_run*.log` (superseded 9-column pipeline referencing
  deleted `bab_*.sql`).
- [m2] Fix REPORT.md §2 BAB t-stats to the final v2 iid values (FF3 7.11,
  FF4 5.54); list NW (5.71 / 4.44) separately.
- [m3] Add `results/table_1.md` (committed table) — metrics already pass:
  stocks 23,407 vs 23,538; June mean firm ME 0.996 vs 0.99 $B; June total
  market cap 3,054 vs 3,215 $B; period 1926-2012.
- [m4] Correct `data_verification.json` delisting `matched_table` from
  `crsp_202601.dse` to `crsp_202601.dsedelist`.

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every iteration log entry in
  `assumptions.md` must have all five fields: Diagnosis, Next fix, Before
  metric, After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.
- **Do not re-derive the BAB factor or beta pipeline** — they are verified
  and deterministic. Build corollaries on top of the existing BAB series.

## Inputs you should read

- `replications/betting_against_beta/logs/audit1.md` — this audit
- `replications/betting_against_beta/inputs/content.md` — paper (Tables B1-B5,
  abstract subperiod claim)
- `replications/betting_against_beta/src/table_3_v2.py` — has `bab_factor()`,
  `portfolio_row()`, `factor_alpha(...)` loadings
- `replications/betting_against_beta/data/panel.parquet` — cached panel
- `replications/betting_against_beta/results/table_3.md` — current Table 3

## What NOT to redo

- Skip re-reading `SKILL.md`.
- Skip re-running `scripts/prep_validation.py` unless you change a prep
  artifact (after this audit it should pass).
- Skip rebuilding the panel / re-estimating betas for [M1]/[M2]/[M3]/[M5] —
  reuse the cached series. Only [M4] needs an alternative beta.

## Deliverables for this iteration

- `results/table_3_subsample.md` ([M1]), `results/table_3.md` or
  `results/table_b1.md` ([M2]), `results/table_3_size.md` ([M3]),
  `results/table_3_robustness.md` ([M4]) — each citing the paper section/table.
- `results/table_1.md` ([m3]).
- `preparations/assumptions.md` — append a 5-field iteration-log entry for
  every issue addressed.
- `REPORT.md` — update; lead with the data-quality summary and the
  corollaries evaluated this iteration; fix the v1 t-stats ([m2]).
- Do NOT edit `SUMMARY.md` (auditor-owned).

## Stop conditions

- **All [M] corollaries computed and verified** → re-run prep_validation.py;
  declare success or note remaining majors in REPORT.md.
- **Data-limited gaps (5-factor, international, other asset classes, TED,
  Prop-5 holdings)** are NON-actionable — document them as limitations, do
  not loop on them.
- **10-iteration cap** on a single problem → escalate, write a partial
  REPORT.md; do not edit SUMMARY.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This is a strong, honest replication of the paper's central result. The
standout is rigor: the beta primitive is validated to machine precision
against an independent pandas computation (`--selftest`), the BAB
construction follows Eqs. (16)/(17) verbatim (rank weights, median split,
unit-beta rescale), the look-ahead handling is careful (beta sampled at
month-end t−1 and assigned to month t; 3-day overlapping returns indexed
backward to avoid a boundary look-ahead; Date32 used to avoid ClickHouse's
pre-1970 epoch clamping), and the FF-factor scale is auto-detected rather
than hard-coded. The agent also did the right thing methodologically by
revising v1 (all-stock breakpoints, no delisting) into v2 (NYSE breakpoints +
Shumway/BMP delisting) and by reporting an honest ablation showing the
methodologically-faithful config is NOT the one that maximizes the pass count
(A22) — it chose fidelity over score, which is exactly the behavior an audit
wants to see.

The one structural weakness is scope discipline on corollaries: the agent
declared "SUCCESS" after nailing Table 3 but never surfaced that the paper's
own abstract sells four more claims (subperiod stability, factor loadings,
size/IVOL robustness, TED time-series) that were neither computed nor flagged
as gaps. Four of those are computable from the existing panel and FF factors,
so they are legitimate actionable majors rather than data excuses. The
decile multi-factor alphas are the genuine soft spot (systematically too high;
P10 FF4 flips sign), and the agent's own diagnosis (sample start + vintage)
is plausible but unverified — the post-1962 sub-window test in [M5] is the
cheap way to confirm it. Finally, the leftover `build_panel.py` /
`panel_diagnostics.md` pair (a superseded 9-column pipeline pointing at
deleted SQL) and the stale v1 t-stats in REPORT.md are small hygiene issues
that a careful reader would trip on; fixing them costs minutes and removes the
only reproducibility hazard in an otherwise clean artifact set.
