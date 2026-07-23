---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — illiquidity_and_stock_returns

**Verdict:** PASS
**Date:** 2026-07-22
**Auditor notes:** All three audit-1 majors are fixed and independently verified: [M1] the rubric-strict tallies embedded in `results/table_1..4.md` recompute exactly from the per-cell values (repo rule 199/86/10; strict **199/52/44** — auditor-parsed aggregates match all four summary lines); [M2] the §3.3 six-subperiod corollary was recomputed from scratch by the auditor from `data/_cache/{milliq,market_ret,rf}.parquet` — all six windows, sign counts (6/6 and 6/6), g1/g2 mean/median, and both Chow tests reproduce to the printed digit (my g2 mean −7.4824 vs file −7.482; Chow p = 0.9173 / 0.1096 vs 0.917 / 0.110); [M3] `data/` holds only `panel.parquet`, the five auxiliary series live in `data/_cache/` with all read/write sites in `src/main.py` updated (write sites L455–459, read sites L1128–1151), and the validator now fails only on the auditor-owned `audit2.md` pairing check (exit 0 after this file). Byte-stability confirmed by ~25 independent spot-checks across all four tables + the Rf sensitivity, every one matching the results files to the printed digit (k_ILLIQMA 0.1657/t 6.56, Table 1 block stats, Table 3 annual AR(1) + market column with OLS and NW0 t, Table 4 market column + monthly AR(1), b1ret/t90ret Rf rows). Minors [m1] (A11 re-pin) and [m2] (Rf sensitivity) verified; [m3] (log1.md stub) removed. One new trivial minor ([m4]): REPORT.md §4 still lists the five parquets at their pre-move `data/` paths, contradicting §7. No blockers, no actionable majors; the replication is complete.

## 1. Scores

| Dimension | Score | Change | Key finding |
|-----------|------:|:---:|-------------|
| Methodology | 4 | — | Unchanged: the converged construction was not re-touched (byte-stable cells confirmed). All six checks pass; two documented deviations (A2 annual Rf substitute — now with a sensitivity on record; A8-revised NW maxlags=0) and two paper-silent universe choices (A5-revised, A7). No methodology bugs on independent recompute. |
| Headline matching | 4 | — | Unchanged. Sign/significance/shape replicate on every headline claim; magnitudes within ~20% except annual g1(market) coef +38.5% (its t matches within 18%) and monthly g2(market) −24%. k_ILLIQMA (+2.3%) and annual g2 (+2.9%) within 3%; monthly R² 0.143 vs 0.144. |
| Data coverage | 4 | — | Unchanged. Exact 1963–1996/1964–1997 period; CRSP + FF sources with one documented Rf substitute; admitted counts inside the paper's range in 33/34 years, 1990s upper bound never approached (documented vintage drift, A12). |
| Concrete result matching | 3 | — | Tier-1 share is the scored quantity and is unchanged at 199/295 = 67.5% (50–70% band → 3) under both conventions. The strict split 199/52/44 is now reported honestly in every results file; I re-derived it from the per-cell OURS/PAPER/tol values with an independent parser and it matches exactly (one intentional, annotated conservative deviation: `ar1_monthly_c0_t` forced FAIL under the repo rule per the A11 paper-anomaly note — this *lowers* the replicator's tally, accepted as in audit 1). |
| Signal strength | 4 | — | Unchanged. Flagship coefficient ratios: k 1.02, g2-annual 1.03, g1-monthly 1.19, g2-monthly 0.76, g1-annual 1.39; all t-stat ratios within [0.82, 1.18]. Two coefficients break the ±20% band (worst-cell reading → 3; the rubric leaves the multi-cell combination open — combined reading → 4). Scored 4 with the worst-cell caveat on record, consistent with audit 1. |
| Corollary | 4 | ↑ from 3 | The §3.3 six-subperiod corollary is now computed and replicates: g1 positive 6/6 (paper 6/6), g2 negative 6/6 (paper 6/6); g2 mean −7.482 vs −7.089 (−5.5%) and median −6.450 vs −5.984 (−7.8%) — against the paper's *sharper* subperiod benchmark; both Chow tests fail to reject AR(1) stability (p = 0.917 annual, p = 0.110 monthly), consistent with the paper's claims. Together with the previously verified Table-2 window stability, strict SZ2 in both tables, and the AR(1)+Kendall dynamics, most corollaries now replicate with documented minor deviations: SZ1 strict monotonicity is directional only (3/4 and 2/4 adjacent pairs), size-portfolio JANDUM/R² magnitudes are inflated, and the subperiod g1 mean is +66% above the paper (honestly reported; same direction as the full-sample g1 overage). |

**Overall: (4+4+4+3+4+4)/6 = 3.83.** Bright line: average ≥ 3.0 and no dimension scored 1 → **REPLICATED**.

## 2. Issues by severity

### Blockers (must fix)

- None.

### Major (should fix)

- None. Audit 1's three majors are resolved:
  - [M1] RESOLVED — dual conventions in all four results files. Auditor recompute (independent markdown parser over the per-cell tables): T1 15/9/0, T2 80/25/2, T3 56/16/1, T4 48/36/7 → repo aggregate 199/86/10; strict T1 15/9/0, T2 80/6/21, T3 56/14/3, T4 48/23/20 → **199/52/44**, both matching the summary lines and REPORT.md §3. A second, stronger check re-derived each cell's repo and strict label from (OURS, PAPER, tol, sign, 2× ratio) across all 295 cells: 0 substantive mismatches — the single deviation is the intentional A11 forced-FAIL on `ar1_monthly_c0_t` (conservative; annotated in the file header; also the convention audit 1 counted under).
  - [M2] RESOLVED — `results/table_4_subperiods.md` added. Auditor recomputed everything independently from `data/_cache/*.parquet` (own AR(1)+Kendall, own window regressions, own Chow implementation): monthly AR(1) −0.0034 + 0.9065 (R² 0.8196, DW 2.468, Kendall 0.9156) exact; full-sample market column exact (g1 0.8448/t 2.88, g2 −4.1818/t −6.04, White −3.22, R² 0.1428, N 396); six 66-month windows match the file to ≤ 0.005 (rounding of the printed precision); g1 > 0 in 6/6, g2 < 0 in 6/6; g1 mean/median 1.4478/1.2299 (file 1.448/1.230; paper 0.871/0.827, +66.2%/+48.7% — honestly reported, not chased per the locked adoption rule); g2 mean/median −7.4824/−6.4504 (file −7.482/−6.450; paper −7.089/−5.984, −5.5%/−7.8%); Chow annual F = 0.0866 p = 0.9173 (17|16) and monthly F = 2.2227 p = 0.1096 (209|198), both vs file 0.087/0.917 and 2.223/0.110. The 66-vs-68-month convention (paper's 68 is six parts of its stated 408-month series; our 396-month regression window → 66) is documented in the file; the paper reports no per-window coefficients, so the summary statistics are the comparison.
  - [M3] RESOLVED — `data/` contains only `panel.parquet` (+ `_cache/`); the five auxiliary series (ailliq, milliq, rsz, rf, market_ret) live in `data/_cache/`; write sites `src/main.py` L455–459 and read sites L1128–1151 all use `CACHE_DIR`; no other `LAYOUT.data_path(...)` call remains. `python scripts/prep_validation.py illiquidity_and_stock_returns` now reports exactly one error — the auditor-owned "log2.md exists but audit2.md is missing" pairing check — and exits 0 once this file exists (re-verified after writing). Byte-stability: ~25 independent recomputes from the relocated parquets (Table 1 blocks, Table 2 k-series, Table 3 AR(1) + market column with both t-stat families, Table 4 AR(1) + market column, six subperiod windows, both Rf-sensitivity rows) all match the results files to the printed digit.

### Minor (cleanup)

- [m4] (NEW) REPORT.md §4 evidence-trail bullet (L235–238) still lists `data/ailliq.parquet`, `data/milliq.parquet`, `data/rsz.parquet`, `data/rf.parquet`, `data/market_ret.parquet` at their pre-move paths; the files now live in `data/_cache/` (as §7 and the results files correctly state). One-line path fix; no number affected. Non-iteration-worthy.
- Audit-1 minors all verified fixed: [m1] A11 re-pinned in `preparations/assumptions.md` (decisive e^5.7 argument primary; (1−0.768)×mean coincidence attributed to the admitted series with the note that it fails on the open series) and in the `table_4.md` AR(1) note; [m2] Rf sensitivity block in `table_3.md` (b1ret: g0 −1.48 / g1 −0.30 / g2 −0.63; t90ret: g0 −0.71 / g1 +0.11 / g2 −0.11 — auditor recomputed both rows from `data/_cache/mcti_bill_monthly.parquet`, exact; canonical Rf untouched); [m3] the trailing "## Summary (pending)" stub is gone from `logs/log1.md`.
- Carried over, documented, non-actionable: SZ1 directional only; size-portfolio JANDUM/R² magnitude inflation; subperiod g1 mean +66%; DIVYLD −18%; Table 5 out of scope (no bond yields in ClickHouse).

## 3. Verification spot-checks (recomputed by auditor, this iteration)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Strict aggregate 199/52/44 from per-cell tables | ✓ | Independent parser: per-table strict 15/9/0, 80/6/21, 56/14/3, 48/23/20 = 199/52/44; repo 15/9/0, 80/25/2, 56/16/1, 48/36/7 = 199/86/10. Both match every summary line. |
| 2 | Strict labels implement the rubric definition | ✓ | Re-derived repo + strict labels from (OURS, PAPER, tol, sign, \|ours/paper\| ∈ [0.5,2]) for all 295 cells: 0 substantive mismatches; 1 intentional conservative A11 forced-FAIL (`ar1_monthly_c0_t`), annotated, tally-lowering. |
| 3 | §3.3 six-subperiod windows | ✓ | Own implementation from `data/_cache/{milliq,market_ret,rf}.parquet`: all six windows' g0/g1/g2/g3/t/R² within 0.005 of the file (3dp/2dp rounding); sign counts 6/6 and 6/6; g1 mean/median 1.4478/1.2299; g2 mean/median −7.4824/−6.4504. |
| 4 | Chow AR(1) stability | ✓ | Own Chow implementation: annual F = 0.0866, p = 0.9173 (17\|16); monthly F = 2.2227, p = 0.1096 (209\|198). Both fail to reject at 5%, consistent with paper L561/L759. |
| 5 | data/ layout + main.py sites | ✓ | `data/` = panel.parquet + `_cache/` only; five series in `data/_cache/`; writes L455–459, reads L1128–1151, all via `CACHE_DIR`; no stray `data_path` calls. |
| 6 | Byte-stability of relocated artifacts | ✓ | ~25 independent recomputes match the results files to the printed digit: Table 1 (ILLIQ/SIZE/SDRET/DIVYLD blocks), Table 2 (k 0.1657, t 6.56, median 0.1417, 63.2353% positive, autocorr 0.0512, 408 months), Table 3 (AR −0.1613+0.7151, t 5.31, R² 0.4766, DW 1.4938, Kendall 0.8104; market g0 21.0852 / g1 14.1660 (3.17/2.82) / g2 −24.2444 (−4.10/−4.18), R² 0.5048, DW 2.530), Table 4 (AR −0.0034+0.9065, market column exact incl. White t), b1ret/t90ret Rf rows. |
| 7 | prep_validation.py | ✓ (post-audit) | Exit 1 before this file with exactly one error — the auditor-owned log2/audit2 pairing check; the audit-1 data-layout error is gone. Exits 0 after audit2.md + SUMMARY.md are written (re-verified). |
| 8 | Paper ground truth for §3.3 | ✓ | `inputs/content.md` L772–777: 408 months, six equal 68-month subperiods, g1 all positive mean 0.871/median 0.827, g2 all negative mean −7.089/median −5.984 — matches the quote and comparison targets in `table_4_subperiods.md`. |
| 9 | Iteration discipline | ✓ | `assumptions.md` iteration-6 entry carries Diagnosis/Next fix/Before/After/Status for each of M1/M2/M3/m1/m2; A11 re-pin and A2 sensitivity addendum in place; REPORT.md §3 (dual tallies, corollary, Rf sensitivity) and §7 (audit history) updated and internally consistent with the results files — except the stale §4 paths ([m4]). |
| 10 | No orphan/score artifacts | ✓ | No `SCORE.md`; `data/_cache/` and `src/__pycache__/` intentional; slug root clean. |

## 4. Issues the agent should have caught (didn't)

1. **The stale §4 evidence-trail paths ([m4]).** The iteration moved five parquets and updated §7, the results files, and all code sites, but the §4 bullet still reads `data/ailliq.parquet` etc. A final grep for `data/ailliq|data/milliq|data/rsz|data/rf|data/market_ret` would have caught it. Trivial.

Nothing else: the iteration did exactly what audit 1 prescribed, the worker's claimed numbers all survive independent recomputation, and the stop condition (don't chase the subperiod g1 gap) was honored.

## 5. Next-iteration prompt (copy-paste this into the next agent run)

**The replicator-auditor loop for this slug is COMPLETE (verdict PASS, requires_iteration: false). No further iteration is required.** If the slug is ever re-opened (e.g., a human review), the only outstanding item is the trivial minor below; everything else is finished and auditor-verified.

--- BEGIN COPY HERE ---

You are doing a one-line cleanup on the completed replication of "Illiquidity and stock returns" (Amihud 2002), slug `illiquidity_and_stock_returns`. Audit 2 (`replications/illiquidity_and_stock_returns/logs/audit2.md`) closed the loop with verdict PASS; do NOT re-touch anything else — the construction, tallies, §3.3 corollary, layout, and validator state are all auditor-verified.

### [m4] — MINOR — stale parquet paths in REPORT.md §4

`REPORT.md` §4 (the evidence-trail bullet around L235–238) still lists `data/ailliq.parquet`, `data/milliq.parquet`, `data/rsz.parquet`, `data/rf.parquet`, `data/market_ret.parquet`; the files moved to `data/_cache/` in iteration 2 (§7 and the results files already say so).

**Specific fix:** update that one bullet to the `data/_cache/` paths (keep `data/panel.parquet` as-is). Then re-run `python scripts/prep_validation.py illiquidity_and_stock_returns` — it must stay exit 0. Do not regenerate any results files and do not edit `SUMMARY.md` or `logs/audit*.md` (auditor-owned).

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This iteration was cheap, mechanical, and exactly right — the three audit-1 majors were reporting-hygiene/completeness items and they were resolved without disturbing the auditor-verified construction (the 0-diff-over-243-cells claim is credible: my own ~25-cell independent recompute from the relocated parquets hit every printed digit). Two verification results are worth recording for the record. First, the strict reclassification is honest in the strongest sense: I re-derived both labels for all 295 cells from the raw (OURS, PAPER, tol) triples and found zero substantive mismatches; the only deviation is a forced-FAIL that makes the replicator's own repo-rule tally look *worse* (the A11 monthly-intercept t-cell), which is the opposite direction of score-gaming. Second, the §3.3 corollary is genuinely informative: the paper's subperiod g2 mean (−7.089) is more negative than its full-sample −5.52, so it was the sharper benchmark for the open-universe construction — and the replication lands within 5.5% of it (−7.482), with 6/6 signs on both sides and both Chow tests agreeing with the paper's stability claim. The honest residual on the corollary is the subperiod g1 mean (+66% over the paper), which amplifies the full-sample +18.6% g1 overage in the small early-sample windows (1964–1974 g1 ≈ 1.1–1.4, 1975–1980 g1 = 3.30); it is reported with its %dev in the file and, correctly, not chased — the adoption rule is locked and the g2 side, the paper's emphasized statistic, is the one that matches. The one score change from audit 1 is corollary 3 → 4: with §3.3 computed and matching, the remaining corollary gaps (SZ1 strictness at 3/4 and 2/4 adjacent pairs, inflated size-portfolio JANDUM/R² magnitudes) are minor, documented, vintage-driven deviations rather than notable gaps. Concrete result stays at 3 — the scored quantity (Tier-1 share 67.5%) is convention-invariant and sits in the 50–70% band; the replication's defense there is not the share itself but that every remaining cell has a documented paper-side or vintage cause, and every headline cell is Tier 1. Final state: 0 blockers, 0 actionable majors, 1 trivial minor (stale §4 paths), validator green, REPLICATED at 3.83/5.
