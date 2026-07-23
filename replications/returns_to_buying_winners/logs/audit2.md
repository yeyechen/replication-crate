---
iteration: 2
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — returns_to_buying_winners

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** All four audit-1 actionable majors (T6/T7, T8, T9, §III decomposition) are delivered and independently verified, and the A13 timing correction is the real fix it claims to be: I recomputed the PA 6/6 strategy from `data/panel.parquet` with my own code and reproduced the artifact to 6 dp (buy-sell 0.008797/month, t 2.908658; sell 0.008110 vs paper 0.0079; buy 0.016908 vs 0.0174), hand-checked the paper's Jan-1980 cohort, reproduced the Table V/VI, Table VII/VIII event-time values and all four §III decomposition statistics (incl. the residual serial covariance +0.001199 vs paper +0.0012) independently, and the full pipeline re-run is md5-idempotent. Zero blockers, zero actionable majors. The only blemish is text hygiene: REPORT.md carries four stale pre-A13 numbers and one arithmetic slip (the results artifacts themselves are all correct).

## 1. Scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 4 | A13 is verified correct: `formation_deciles` ranks formation f on `cumret_J_raw` at row f+1 (`src/main.py:661-662`), i.e. signal [f−5, f] = the paper's [t−6, t−1] under t=f+1, holding f+1..f+K — auditor's independent recomputation reproduces the artifact to 6 dp and the Jan-1980 cohort hand-check matches; every knock-on (WRSS window, θ x-window, earnings cohorts, count asserts) is implemented and logged (A13, P29). Residual unverifiables: Panel A F-stat construction (7 secondary cells, 3 variants reported, M5 of audit 1) and a few paper-silent conventions (T8 event-window bound, WRSS normalization) — all documented. |
| Headline matching | 4 | Central 6/6 buy-sell −7.4% of the paper (0.008797 vs 0.0095 — auditor-recomputed exactly), sell +2.7%, buy −2.8%, t 2.91 vs 3.07; all 32 strategies positive (31/32 significant at 1.645; PA 3/3 is nil in the paper too, t 1.10); January effect (−5.5%/+1.7%), event-time inverted-U (C₁₂ +7.3%) and 4-of-5 subperiods replicate; the C₃₆ endpoint (+71%, paper t 0.67) and Panel A crash-era magnitude (84% of paper) keep this at 4. |
| Data coverage | 4 | Exact reporting period (1965-01..1989-12, 300 months) plus a verified 1926-07 extension for the back-test (in-code snapshot gate asserts the 1965–89 region is bit-identical on rebuild; panel 1,097,807×15); same sources as the paper (CRSP daily, dsi indexes, Compustat fundq, CCM link, FF factors); one documented substitution each (2026 vs 1990 CRSP and Compustat vintages), quantified where it matters (Table IX √n inflation). |
| Concrete result matching | 4 | 1,127/1,327 Tier 1 (84.9%), 130 Tier 2, 70 FAIL — tally independently reproduced from the contract + `computed_values.json` (0 value mismatches across all 1,327 cells); all 70 FAILs verified nil (37 t-cells with paper |t| ≤ 1.13, 33 return cells with |paper| ≤ 0.01). Tier 2 is defined as sign-match + deviation ≤ 200% (see m3). |
| Signal strength | 5 | The paper's most prominent numbers — 0.95%/month and t 3.07 for the 6/6 strategy, 12.01%/yr compounded — map to ours 0.008797 (ratio 0.926), t 2.908658 (0.947), 11.08%/yr (0.92): every headline cell ratio lies in [0.9, 1.1]. The audit-1 worst anchor (ratio 1.214) is gone. |
| Corollary | 4 | All four audit-1 corollaries now computed and checked: Table VIII (Panel B C₁₂ 0.0621 vs 0.0583 +6.6%, "dissipation by month 24" reproduced; Panel A month-1 −0.0501 vs −0.0495 essentially exact, C₃₆ −0.342 vs −0.408, sign/shape with vintage-attributed magnitude), Table IX (months 1–7 mean +0.0072, 7/7 positive and significant; months 11–18 mean −0.0048; 11/13 of months 8–20 loser-dominated), §III decomposition (all three causal verdicts reproduce; residual serial covariance +0.001199 exact; corr(WRSS,6/6) 0.963 vs 0.95; WRSS mean −53% with the correlation anchor matched; θ −1.98 vs −2.29, halves ordered correctly), Tables V/VI (Apr 0.96, Feb–Dec 0.709, All 0.667; Jan 70–74 −0.1129 vs −0.1070). Plus the audit-1 set (size/SW-beta subsamples, risk non-explanation, footnote-11, seasonality). Deviations documented with evidence. |
| 7 | SUMMARY.md matches results/table_*.md | ✗ | All results artifacts reproduce from `computed_values.json` (0 mismatches) and the table md files carry correct post-A13 values — but REPORT.md re-used four pre-A13 anchor numbers in its §4 prose (T6 January proportion; T7 Jan-70–74 and 1975–79 cells; T1 PA 3/3) and has one arithmetic slip in §3 (11.13% should be 11.08%); see m1. The previous SUMMARY.md (audit-1 era) is overwritten by this audit. |

## 2. Issues by severity

### Blockers (must fix)

None.

### Major (should fix)

None actionable. The audit-1 non-actionable majors stand:

- [M5, carried] Panel A F-statistics (7 cells) — paper's overlapping-series F construction unidentified; three variants reported (P20). Non-actionable (paper-side ambiguity; the decile means the F-tests are about do replicate).
- [M6, carried] Sell-side vintage attribution — the residual is now small (sell +2.7% post-A13) and the optional universe-scope bounding test was skipped this iteration as attribution-only. Non-actionable (1990 CRSP vintage unavailable; the A13 correction resolved the bulk of the original shortfall).

### Minor (cleanup)

- [m1] REPORT.md carries four stale PRE-A13 numbers and one arithmetic slip (all the underlying artifacts are correct and still within tolerance — no narrative change is implied):
  - File: `REPORT.md:172-174` — "January 0.24 (0.0% dev)"; artifact `prop_jan_all` = 0.20 (5/25 Januaries), deviation −16.7% (Tier 1 at tol 50; `results/t6_table_v.md` shows the correct 0.20).
  - File: `REPORT.md:179` — "January 1970–74 −10.1% vs −10.7% (t −2.51 vs −2.54)"; artifact `sp_all_jan_7074` = −0.112865 (t −2.467), i.e. −11.3% vs −10.7%.
  - File: `REPORT.md:178` — "All −0.33%/mo vs paper −0.44%, t −0.4 vs −0.51"; artifact `sp_all_all_7579` = −0.006356 (t −0.826), i.e. −0.64%/mo.
  - File: `REPORT.md:126` — "PA 3/3 buy-sell 0.0038 vs 0.0032"; artifact `PA_J3_buy_sell_K3` = 0.002333 (−27.1%, Tier 1 at tol 100 — the paper prints t 1.10 for this cell).
  - File: `REPORT.md:97-99` — "(1.008797)¹²−1 = 11.13%"; (1.008797)¹²−1 = 11.08% (arithmetic 10.56% and geometric 9.12% in the same sentence are correct).
  - Specific fix: replace the five values from `computed_values.json` / a calculator; the qualitative claims ("essentially exactly", "dip reproduces", "J=3 cells now pass") all remain true at the correct values.

- [m2] The per-cell classifier that produces `results/cell_classification.json` is not committed (no script in the repo generates it; audit-1 m4 — per-table tier counts surfaced only in the JSON — remains open). I reverse-engineered and reproduced its rule exactly (see m3), so the tallies are verifiable, but the artifact is not regenerable from committed code.
  - File: `results/cell_classification.json` (generator absent from `src/`).
  - Specific fix: commit the harness as `src/classify.py` (contract + `computed_values.json` in → classification + per-table tier-count block appended to each `results/table_*.md` out).

- [m3] The classification rule is undocumented. The harness applies: Tier 1 = within `tolerance_pct`; Tier 2 = same sign AND deviation ≤ 200% (i.e. |ours| ≤ 3×|paper| — the "2×" read as a deviation bound); FAIL = opposite sign, |ours| > 3×|paper|, or paper = 0. Under the rubric's strict ratio reading ([0.5, 2.0] both sides), 54 cells move Tier 2 → FAIL (25 magnitude-underestimates incl. the 7 F-stats; 29 just-over-2 ratios ≤ 2.97); Tier 1 is unaffected (1,127 either way) and every affected cell is statistically nil in the paper (t-stats or ≤0.3%/mo cells).
  - File: generator absent (see m2); rule statement nowhere in `REPORT.md` §4 or the results md files.
  - Specific fix: state the rule in the harness and in one line of REPORT §4; either reading is defensible, but the choice should be explicit.

- [m4] `results/primary_diagnostics.md`'s "REPORT.md §3" comparison column still prints the PRE-A13 REPORT values (0.011530 / 4.17 / 0.83 / 2078.0% / −41.9% / 16.84%…) next to the correct new diagnostics, so every row shows "within tol: False". It is labeled informational (the runtime assert was retired to a note — correctly, see §6), but the stale column is misleading to a reader.
  - File: `results/primary_diagnostics.md:1-20`; generator constants in `src/main.py` (`compute_primary_diagnostics`).
  - Specific fix: update the comparison constants to the post-A13 REPORT §3 values (or drop the column; the diag_* keys are the persisted record).

- [m5] Carried advisories from audit 1, intentionally untouched: the central cell's tolerance (`PA_J6_buy_sell_K6`, still 98%) could be tightened now that the deviation is −7.4%, so the headline carries more weight in the hit-rate (audit-1 m5); and the optional M6 universe-scope bounding test for the (now small) sell residual remains unrun. Neither has any status consequence.

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ | Auditor-recomputed decile mean profile (PA 6/6, 1965–89 cohort-months): 0.00811, 0.01149, 0.01281, 0.01302, 0.01341, 0.01405, 0.01405, 0.01480, 0.01556, 0.01691 — increasing except a d6/d7 inversion of 6.1e-6 (0.06 bp/mo; economically flat mid-deciles, endpoints intact); all 32 zero-cost spreads positive; beta-group spreads increasing as in audit 1. |
| 2 | Headline-magnitude claim | ✓ | Independent from-scratch recomputation from `data/panel.parquet` (own code: signal = cumret_6_raw at row f+1, floor-rank/permno-tie deciles, K=6 overlap, 300 months, every month exactly 6 cohorts): sell **0.008110** (t 1.615090), buy **0.016908** (t 4.218487), buy-sell **0.008797** (t 2.908658, std 0.052387) — identical to `computed_values.json` to 6 dp; vs paper 0.0095 = −7.4%. cumret_6_raw window verified calendar-aligned [m−6, m−1] on all 1,059,755 non-null rows (max\|diff\| 3.6e-8, FP noise). Jan-1980 cohort hand-check: formation f=1979-12 ranks on cumret_6_raw@1980-01 = compound of ret_raw over [1979-07, 1979-12] (|diff| ≤ 5e-10 on sampled permnos), N=2,205 ranked, decile-1/10 h=1 (1980-01) EW returns computed straight from the panel. |
| 3 | Sample coverage ≥ 60% | ✓ | Panel 1,097,807×15, 1926-07..1989-12; every one of the 300 reporting months has exactly K=6 contributing cohorts in all 32 grids (asserted in code; auditor re-derivation confirmed 6/6 for every month); back-test cohorts complete inside their windows (asserted; auditor-reproduced n_1=167/n_12=156/n_36=132 for Panel A, 287/276/252 for Panel B). |
| 4 | Data-source choice justified | ✓ | A3 raw-PRIMARY remains the faithful choice post-A13 — and more clearly so: auditor-recomputed, the adjusted series' delisting drag is sell −0.001131/mo vs buy −0.000103, so adjusted bs 0.009825 (+3.4% vs paper) vs raw 0.008797 (−7.4%); but the adjusted SELL leg is −11.7% from the paper's 0.0079 while the raw sell is +2.7% — the paper's own sell leg is inconsistent with dlret drag, so the spread "match" of the adjusted series is quantified coincidence (drag differential +0.001028/mo offsetting the raw gap), exactly as the replicator argues. The audit-1 evidence chain (12/12 msf = raw daily compound; paper L139 compounding; Shumway 1997 on this paper's vintage) stands. |
| 5 | prep_validation.py exit 0 | ✗→✓ | Exit 1 on arrival — the only error is the auditor's own missing deliverable ("logs/log2.md exists but logs/audit2.md is missing"); the prep contract itself validates. Exit 0 after this audit + SUMMARY.md land. |
| 6 | All committed tables have results files | ✓ | 9 contract tables (1,327 cells) → `table_1.md`…`table_5.md`, `t6_table_v.md`, `t7_table_vi.md`, `t8_table_viii.md`, `table_7_earnings.md` + `table_8_decomposition.md`; `computed_values.json` has exactly 1,349 keys (1,327 + 11 dec_* + 11 diag_*); classification 'ours' vs `computed_values.json`: 0/1,327 mismatches. |
| 7 | SUMMARY/REPORT values match results | ✗ | All table md files and JSON artifacts are mutually consistent and auditor-reproduced; REPORT.md §4/§3 prose carries 4 stale pre-A13 values + 1 arithmetic slip (m1). The old SUMMARY.md is overwritten by this audit. |
| 8 | No orphan folders | ✓ | Slug root: data/, inputs/, logs/, preparations/, results/, src/, REPORT.md, SUMMARY.md only. |
| 9 | Diagnoses paired with fix attempts | ✓ | log2.md's three inner-iteration entries and the assumptions.md A13 entry (L1141–1231) all carry Problem/Diagnosis/Next fix/Before/After/Status with quantified metrics; the A13 before/after was independently re-verified (the "after" numbers reproduce exactly; the "before" numbers are the audit-1-verified pre-A13 values). |
| 10 | Tier 2 within 2× magnitude | ✓ (rule-dependent) | Under the harness rule (deviation ≤ 200%) the classification reproduces exactly from contract + computed_values (0/1,327 discrepancies once the rule is identified). Under the rubric's strict [0.5, 2.0] ratio, 54 cells shift Tier 2 → FAIL — all statistically nil (F-stats, ≤0.3%/mo event/subperiod cells, near-zero t's); Tier 1 (1,127) is identical under both readings. See m3. |
| 11 | Corollary coverage | ✓ | All four audit-1 corollaries computed and auditor-checked: Table VIII (reproduced exactly under the documented convention — see below), Table IX (pattern, not t-stats — the deliverable the paper's abstract claims), §III decomposition (all four statistics recomputed independently), Tables V/VI. Audit-1's verified corollaries (subsamples, risk, footnote-11, seasonality, event-time reversal) stand. M5/M6 documented non-actionable. |

**Independent recomputations performed by the auditor (own code, from `data/panel.parquet` + own `dsi` queries):**

- **PA 6/6 strategy (A13):** sell/buy/buy-sell means and t-stats identical to the artifact to 6 dp (0.008110 / 0.016908 / 0.008797; t 1.615090 / 4.218487 / 2.908658). Table V proportions from my own series: Jan 5/25 = 0.20, Apr 24/25 = 0.96, Feb–Dec 195/275 = 0.7091, All 200/300 = 0.6667 — exactly the `prop_*` keys. Table VI All-column subperiod means and t-stats (65–69 +0.011650/1.824; 70–74 +0.009116/1.016; 75–79 −0.006356/−0.826; 80–84 +0.012969/2.796; 85–89 +0.016608/3.372; Jan 70–74 −0.112865/−2.467) — exactly the `sp_*` keys.
- **Event time (T5/T8):** under the documented convention (event month h averages cohorts with f+h ≤ window end; C_h = arithmetic sum of event-month means), my implementation reproduces `event_t*` and all 12 sampled `bt_a_*`/`bt_b_*` anchors to ≤4.2e-7 (rounding): C₁₂ 0.102072, C₃₆ 0.069595; Panel A month-1 −0.050050, C₃₆ −0.341976; Panel B C₁₂ 0.062140, C₂₄ 0.020877, C₃₆ 0.018667. The T8 window-bound convention (holdings contained in 1927–40 / 1941–64) is a faithful reading of the paper's "returns in the 36 event months over the 1927 to 1940 time period" and mirrors the data-end restriction the paper's Table VII is forced to use; the unrestricted variant (my computation: Panel A C₃₆ −0.4369, month-1 −0.05135) is closer on C₃₆ but worse on month 1 — the paper's own convention is not recoverable, and the choice is documented (`src/main.py:2650-2653`).
- **§III decomposition (all four, own code + own `dsi` pull):** residual serial covariance (lag-6, VW market, 3,196 stocks) **+0.001199** = artifact = paper +0.0012 to 4 dp; θ −1.9807 (t −3.38), halves −2.2076/−1.5783 — exactly the `dec_*` keys; WRSS per-$-long 0.02115 (t 1.06), corr 0.9626 — exact; EW semiannual serial covariance −0.00610 (overlapping variant +0.0299) — exact.
- **Table IX:** `ea_*` keys give months 1–7 mean +0.007187 (7/7 positive), months 11–18 mean −0.004792, months 8–20 negative in 11/13 (months 8–9 small positives +0.0015/+0.0006, reported honestly), near-zero 21–36 — the paper's abstract-level pattern. Recomputation not performed (needs the full fundq→CCM→dsf path); verified against the artifact + paper pattern claim.
- **Pipeline determinism:** full re-run `uv run python replications/returns_to_buying_winners/src/main.py` (exit 0, cached panel) reproduced 12/14 hashed artifacts **bit-identically**; the two exceptions (`primary_diagnostics.md`, `sell_diagnostic.md`) carry `Generated:` timestamp lines — the documented timestamp exception; all data-bearing outputs are deterministic.

## 4. Issues the agent should have caught (didn't)

1. **Four stale pre-A13 numbers in the post-A13 REPORT rewrite.** The inner-iteration-1 (pre-A13) M4 report quoted January proportion 0.24, Jan-70–74 −10.05%, and the pre-A13 run had PA 3/3 at 0.0038; the inner-iteration-3 re-run moved them (0.20, −11.29%, 0.002333 — all in `computed_values.json` and the table md files), but the REPORT rewrite re-used the old anchors. The agent's own `t6_table_v.md` anchor block shows prop_jan_all −16.7% — the inconsistency was visible in the artifacts.
2. **The 11.13% slip.** (1.008797)¹²−1 is 11.08%; the m3 wording fix (like-for-like compounding) was the right move but introduced a small arithmetic error in the replacement text.
3. **The classifier is uncommitted and its rule unstated.** The m1 hygiene fix ("sign-opposite cells are now FAIL") and the 200%-deviation Tier-2 bound live in a harness no one can re-run from the repo; the rule had to be reverse-engineered during this audit (it reproduces the JSON exactly, so the artifact is trustworthy — but it should be committed and documented).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Returns to Buying Winners and
Selling Losers: Implications for Stock Market Efficiency" (Jegadeesh &
Titman 1993) for slug `returns_to_buying_winners`. The previous agent
run completed with verdict **PARTIAL** (audit 2 at
`replications/returns_to_buying_winners/logs/audit2.md`) with
`requires_iteration: false` — zero blockers, zero actionable majors.
The replication is DONE in substance: all nine tables (1,327 cells,
84.9% Tier 1) replicate, the A13 timing correction was independently
re-verified by the auditor to 6 dp, and all four audit-1 corollaries
were delivered and checked. This prompt is CLEANUP ONLY — do not
reopen any methodology.

## Issues to address (priority order — all minor)

### [m1] — MINOR — fix five REPORT.md numbers (text-only edit)
REPORT.md carries four stale pre-A13 values and one arithmetic slip;
the underlying artifacts are correct, so no computation is needed.

**Specific fix:**
1. `REPORT.md` §4 T6 block: "January 0.24 (0.0% dev)" → "January 0.20
   (−16.7%; 5/25 Januaries; Tier 1 at tol 50)" (artifact prop_jan_all
   = 0.2 in `results/computed_values.json`; `results/t6_table_v.md`
   already shows 0.20).
2. §4 T7 block: "January 1970–74 −10.1% vs −10.7% (t −2.51 vs −2.54)"
   → "−11.3% vs −10.7% (t −2.47 vs −2.54)"; "All −0.33%/mo vs paper
   −0.44%, … t −0.4 vs −0.51" → "All −0.64%/mo vs paper −0.44%, …
   t −0.83 vs −0.51" (artifacts sp_all_jan_7074 = −0.112865,
   sp_all_all_7579 = −0.006356).
3. §4 T1 block: "PA 3/3 buy-sell 0.0038 vs 0.0032" → "0.0023 vs 0.0032
   (−27%, Tier 1; paper t 1.10)" (artifact PA_J3_buy_sell_K3 = 0.002333).
4. §3: "(1.008797)¹²−1 = 11.13%" → "= 11.08%".
5. Verification: grep REPORT.md for each old string (should be gone);
   do NOT re-run anything else.

### [m2] — MINOR — commit the classification harness
`results/cell_classification.json` has no generator in the repo.

**Specific fix:**
1. Commit the harness as `src/classify.py`: read
   `preparations/tables_to_replicate.json` + `results/computed_values.json`,
   emit `results/cell_classification.json` (byte-identical to the
   current one) and print the per-table tier counts.
2. Append a one-line tier-count block ("n cells: X Tier 1 / Y Tier 2
   / Z FAIL") to each `results/table_*.md` (closes audit-1 m4).
3. Verification: `uv run python …/src/classify.py` regenerates the
   JSON with md5 == current; counts match REPORT §4's table.

### [m3] — MINOR — document the classification rule
The harness rule (Tier 1 = within tolerance_pct; Tier 2 = same sign
AND deviation ≤ 200%, i.e. |ours| ≤ 3×|paper|; FAIL = opposite sign /
> 3× / paper = 0) appears nowhere. Under the rubric's strict
[0.5, 2.0] ratio reading, 54 nil cells shift Tier 2 → FAIL (Tier 1
unchanged at 1,127) — either reading is defensible; the choice must
be explicit.

**Specific fix:** state the rule in `src/classify.py`'s docstring and
in one sentence of REPORT §4 (or switch to the symmetric rule and
update the tallies — your call, but do not silently keep the status
quo).

### [m4] — MINOR — fix the stale comparison column in primary_diagnostics.md
The "REPORT.md §3" column prints pre-A13 values (0.011530 / 4.17 /
0.83 / 2078.0% / −41.9% / 16.84%), so every row reads "within tol:
False".

**Specific fix:** update the comparison constants in
`compute_primary_diagnostics` (src/main.py) to the post-A13 REPORT §3
values — or drop the column (the diag_* keys are the persisted
record) — and re-run main.py (deterministic; md5 check the other 11
artifacts stay identical).

### [m5] — optional advisory (no obligation)
Tighten the central cell's tolerance (PA_J6_buy_sell_K6 is still 98%
in the contract; the deviation is now −7.4%) and/or run the audit-1
M6 universe-scope bounding test (recompute PA 6/6 sell without the
shrcd filter; attribution only — do NOT change the primary universe).

## Iteration discipline reminders

- **This is a cleanup iteration.** Do not re-run the panel, do not
  touch `formation_deciles`, do not reopen the delisting decision
  (A3 raw-PRIMARY — auditor re-verified post-A13 that the adjusted
  sell leg is −11.7% from the paper while raw is +2.7%; the spread
  "match" of the adjusted series is the quantified delisting-drag
  offset, not grounds to switch).
- **Diagnose → commit-fix → fix → verify.** Any log entry you add
  carries all five fields.
- **10-iteration cap per problem.** Hard stop and escalate.

## Inputs you should read

- `replications/returns_to_buying_winners/logs/audit2.md` — this audit
- `replications/returns_to_buying_winners/REPORT.md` — the five text
  fixes (m1)
- `replications/returns_to_buying_winners/results/computed_values.json`
  — source of truth for every number
- `replications/returns_to_buying_winners/SUMMARY.md` — the auditor's
  current assessment; do NOT edit

## What NOT to redo

- Skip re-reading `SKILL.md`.
- Skip `scripts/prep_validation.py` unless you change a prep artifact
  (it passes at audit 2).
- Skip re-running main.py except for m4 (and if you do, md5-check the
  other artifacts for idempotence).
- Do NOT recompute any table — every number is verified.

## Deliverables for this iteration

- `replications/returns_to_buying_winners/REPORT.md` — the five text
  fixes (m1)
- `replications/returns_to_buying_winners/src/classify.py` — committed
  harness (m2) + rule docstring (m3); per-table tier counts in the
  table md files
- `replications/returns_to_buying_winners/src/main.py` — m4 constant
  update (or column removal) only
- `replications/returns_to_buying_winners/preparations/assumptions.md`
  — one short entry per item addressed (five fields each)

## Stop conditions

- **m1–m4 fixed and verified** → declare success; the next audit (if
  any) updates SUMMARY.md.
- If any "cleanup" change moves a number, STOP and report — nothing
  in this iteration should change a computed value.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

The A13 correction is the standout of this iteration and it was handled exactly as a methodology-first replication should be: diagnosed by code inspection (the formation month f was in neither the signal window [f−6, f−1] nor the holding window [f+1, f+K] — a silent one-month skip that 6-month momentum smoothness had masked), fixed with a single minimal change plus its forced knock-ons, hand-verified on the paper's Jan-1980 cohort, and reported with honest before/after numbers — including the WRSS mean, which moved *away* from its anchor under the corrected alignment and was reported as such rather than tuned back (the discriminating correlation anchor matches at 0.963 vs 0.95). My independent checks confirmed the load-bearing claims exactly: the PA 6/6 series recomputed from the parquet to 6 dp, the Table V/VI series fell out of my own recomputation identically, the Table VII/VIII event-time values reproduced under the documented convention to ≤4e-7, all four §III statistics reproduced from my own code and my own dsi pull (the +0.001199 residual serial covariance against the paper's +0.0012 is the kind of exact match that identifies the paper's actual convention — non-overlapping-period, lag-6), and the full pipeline re-run was bit-identical on every data-bearing artifact. On the retired guards: I endorse both retirements with my own numbers — the raw-PRIMARY choice is *more* clearly faithful post-A13, not less, because the adjusted series' sell leg is −11.7% from the paper while the raw sell is +2.7%; the adjusted spread's closer match is a quantified delisting-drag offset (+0.001028/mo, almost entirely on the sell side), and a paper whose own sell leg is 0.0079 cannot have been computed with dlret drag. The diagnostics-vs-REPORT assert's retirement to an informational note is the correct response to §3 legitimately moving under a methodology fix. The replication's one genuine blemish is text hygiene: the post-A13 REPORT rewrite re-used four pre-A13 anchor numbers (all of which, by bad luck, overstated agreement — the true post-A13 values are all still Tier 1, so no conclusion changes, but a careful reader comparing REPORT §4 to `t6_table_v.md` will stumble), plus an 11.13%-vs-11.08% arithmetic slip. These are thirty seconds of editing, flagged as m1 with the exact replacements. The remaining deviations are honestly earned vintage effects (crash-era Panel A magnitudes at 84% of the paper; WRSS mean; NW t-stats running |larger| because the 2026-vintage series are less autocorrelated; Table IX √n inflation from richer Compustat coverage) — none is a methodology error, and none is fixable without the paper's 1990 data vintages.
