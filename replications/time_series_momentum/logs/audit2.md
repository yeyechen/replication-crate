---
iteration: 2
verdict: PASS
blocker_count: 0
actionable_major_count: 0
requires_iteration: false
---

# Audit Report 2 — time_series_momentum

**Verdict:** PASS
**Date:** 2026-07-22
**Scope:** Report-accuracy & cleanup pass (iteration 2). No numerical changes were claimed except
relocating raw-pull caches `data/ → <slug>/.cache/`; I re-verified the current artifacts against my
independent iteration-1 recomputations and found them numerically identical at every displayed
precision (raw factor mean 1.3150%/mo, vol 12.645%, Sharpe 1.2478; factor cross-section 25/32/49/53,
mean 44.2; every Table 3 and Table 5 cell; 2008Q4 SP500 −23.00% / TSMOM +10.21%; smile curvature
0.0044; per-instrument Sharpes). The no-numerical-change claim is corroborated.

**Auditor notes:** Every audit-1 issue is addressed and verified against artifacts, not just prose.
The REPORT now quotes its own eval CSVs faithfully: I re-checked all 40 cells of the §4 Table 5C
block against `eval_t5.csv`/`table_5.md` and all 22 cells of the §4 Table 3A block against
`eval_t3.csv`/`table_3.md` — all match at displayed precision. The "insignificant alpha" claim is
gone and replaced with the honest characterization (−0.39%/mo, t −2.28, Tier 1 only under the
committed 200% near-zero tolerance; the replicated claim is β ≈ 0.72 and R² ≈ 47%). The Tier-2
leniency disclosure is present with the rubric-strict tally, which I re-derived cell-by-cell
(180/49/191). One NEW minor item found: the §4 Table 1 *example* volatilities are stale 1985–2009
window values that now contradict the report's own m2-fixed "full panel window" prose. It changes
no claim and no tier, so it does not require another auditor cycle. The remaining
`prep_validation.py` layout error is a validator allowlist false positive (judgment below).

## 1. Verification of iteration-2 fixes

### (a) [M1] transcription fixes — ALL VERIFIED ✓

- **§4 Table 5C block (8 rows × 5 cells = 40 cells):** every ours/paper/(t)/R² value matches
  `results/eval_t5.csv` and `results/table_5.md` at displayed precision. Spot-verified all rows,
  including the five audit-1 corrections: XSMOM_ALL α −0.39 (t −2.28) [eval: −0.3874/−2.2754];
  XSMOM_COM α −0.82 (t −3.52), R² 15.7% [−0.8199/−3.5187/0.1573]; XSMOM_FX α −0.37 (t −1.19),
  R² 2.9% [−0.3666/−1.1919/0.0292]; HML −0.140 (t −2.92) / +0.54 (2.88) / R² 2.8%
  [−0.1403/−2.9200/0.5367/2.8823/0.0278]; XSMOM_ALL β 0.716 (16.28), R² 47.1% ✓.
- **§4 Table 3A block (22 cells):** all match `eval_t3.csv`/`table_3.md` (monthly α 1.20% (5.85),
  R² 11.6%; quarterly α 3.49% (5.22), R² 20.4%; UMD 0.23 (5.39) / 0.33 (4.15); HML −0.14 (−2.00) /
  −0.18 (−1.79)) ✓. Derived claims re-checked: "α within 24%/26%, UMD within 18%/2%" → −24.2%,
  −26.5%, −18.4%, +1.8% ✓.
- **§1 numbers:** XSMOM-ALL β 0.716 (t 16.3) R² 47% vs 0.66 (15.2) 44% ✓; α −0.39% (t −2.28) vs
  −0.16% (−1.17) ✓; UMD-on-TSMOM 0.41 (5.6) vs 0.49 (6.6) [0.4128/5.6427] ✓; intercept 1.20%
  (5.85) vs 1.58% (7.99), quarterly 3.49% (5.22) vs 4.75% (7.73), UMD 0.23 (5.4) vs 0.28 (6.78) ✓;
  horizon h=1 column +3.6/+4.4/+3.0/+3.2/+5.3 (paper +4.3/+5.4/+5.0/+6.1/+6.6) → +3.0/+1.8/+1.6
  at k24/36/48 — all match `table_2.md` ✓; Table 4 within-eq 0.49 (0.37), passive-eq 0.67 (0.60)
  and the 3 passive-FX FAILs match `table_4.md` ✓; FF5 α 15.9%/yr (t 6.0) matches
  `diagnostics_block.txt` (15.93%, t 6.02) ✓; tally 180/136/104 re-derived cell-by-cell from the
  five eval CSVs ✓ (T1 37/40/29, T2 98/76/58, T3 14/2/6, T4 14/3/3, T5 17/15/8).

### (b) "Insignificant alpha" claim — GONE ✓

`grep` confirms no residual "insignificant alpha" characterization of XSMOM_ALL. §1 and §4 now
state: small NEGATIVE alpha −0.39%/mo (t −2.28) vs paper −0.16% (−1.17); both small negatives;
Tier 1 only under the committed 200% near-zero tolerance; replicated claim is loading and R².
The remaining "insignificant" uses (T3 SMB/HML signs; T5 near-zero FAIL cells) are correct usages.

### (c) Factor bullet: raw mean vs intercept — FIXED ✓

§1 bullet now reads: raw mean **+1.315%/month**, 12.65% vol, Sharpe 1.25, with the Table 3A
intercept (+1.20%/mo, t 5.85) labeled distinctly. Auditor recompute from
`strategy_artifacts.parquet`: mean 1.3150%/mo, vol 12.645%, Sharpe 1.2478; internal consistency
1.25 ≈ 1.315×√12/12.65 = 1.248 ✓.

### (d) Minor items m1–m5 — ALL ADDRESSED ✓ (one residual, see [m6])

- **[m1] S_t labeling ✓:** §2 now distinguishes panel AVAILABILITY 27/36/51/54 from the factor
  CROSS-SECTION (signal AND σ available) 25/32/49/53, mean 44.2/month. Auditor recompute from
  artifacts: cross-section 25/32/49/53, mean 44.2 — exact match. (Mean availability recomputes to
  45.47 → the report's "45.4" is a rounding artifact of ~0.07; immaterial.)
- **[m2] Table 1 window prose ✓ (mostly — see [m6]):** §4 prose now says "each instrument's FULL
  panel window (futures listing → 2009-12; SP500 n = 326)", matching `table_1.md`'s header and
  `eval_t1.csv` values (SP500 vol 15.34, computed from 1982-11, n=326 — verified).
- **[m3] 2008Q4 ✓:** −23.0% in §1 and §5; auditor recompute from panel: SP500 −23.00%, TSMOM
  +10.21% on the quarter.
- **[m4] Caches relocated ✓:** `.cache/` now holds `cache_daily_futures.parquet`,
  `cache_rf_monthly.parquet`, `cache_codes.txt`; `data/` holds only `panel.parquet`,
  `strategy_artifacts.parquet`, `t1_preview.csv`. `src/main.py:465` uses
  `cache_dir = LAYOUT.root / ".cache"` with an explanatory comment. Numerical invariance
  corroborated: every auditor-recomputed statistic from the current artifacts matches the
  iteration-1 independent verification exactly (consistent with the claimed md5sum 7/7 OK).
- **[m5] SEKUSD exclusion ✓:** stated at the first "49 of 54" occurrence (§1): 55 instruments
  mapped; SEKUSD has 7 post-burn-in months in-window (auditor-verified: 7), no 12-month signal.
  Auditor recompute: exactly 49 of 54 signal-bearing instruments have positive 12-month TSMOM
  Sharpe; the 5 negatives are COTTON −0.17, CATTLE −0.10, GILT −0.09, SOYMEAL −0.05, USLONG −0.03
  — matches §5 exactly.

### (e) Tier-2 leniency disclosure — PRESENT ✓

§1 "Honesty note" discloses the committed Tier-2 = sign-match convention is looser than the
rubric's 2× standard, with both tallies: committed 180/136/104 (43/32/25%) vs strict 180/49/191
(43/12/45%). Both re-derived: committed cell-by-cell ✓; strict matches the audit-1 recount ✓.

## 2. New / residual issues

### Minor (cleanup; does NOT require an auditor cycle)

- **[m6] §4 Table 1 example volatilities are stale 1985–2009-window values**, contradicting the
  just-fixed "full panel window" prose two lines above and the committed artifacts.
  - File: `REPORT.md:125`. Examples quoted: SP500 **15.60**, EURUSD **11.10**, DAX **21.61**,
    COFFEE **39.41**, COPPER **27.07**. These match the `vol_8509` column of `data/t1_preview.csv`
    exactly (15.5996/11.1029/21.6057/39.4130/27.0733) — a diagnostic that also carries the
    full-window column.
  - Committed values (`table_1.md` / `eval_t1.csv`, full panel window): SP500 **15.34**, EURUSD
    **11.47**, DAX **21.59**, COFFEE **38.01**, COPPER **27.04** (auditor-verified against
    `eval_t1.csv` and recomputed for SP500 from `panel.parquet`: 15.3408).
  - Likely cause: the example line predates the full-window recompute and was not updated when the
    m2 prose fix landed; the m2 fix made the contradiction explicit.
  - Impact: none on claims or tiers — all five examples are Tier 1 under either window (max
    relative diff vs paper: 5.9% for DAX, well within the 10% vol tolerance), and the cited tier
    counts (34/19/0 vol; 3/21/29 mean) match `table_1.md`.
  - Fix: re-quote the five examples from `table_1.md` (15.34 / 11.47 / 21.59 / 38.01 / 27.04).
- **Observations (no action needed):** (i) §2 quotes mean availability as 45.4/month; auditor
  recompute is 45.47 → 45.5 (rounding-level, carried over from audit-1's own recompute). (ii)
  `logs/log2.md` says "W1–W13 stand" but `preparations/assumptions.md` contains W1–W11 (miscount
  in the log only; A1–A11 correct).

### Blockers / Majors

None.

## 3. Judgment: `prep_validation.py` strategy_artifacts.parquet flag

**The replicator's "allowlist false positive" justification HOLDS.** The validator's Check 2
(`scripts/prep_validation.py:573-588`) hardcodes an allowlist `{panel, bin_rets, ls_ew, ls_vw,
cop_p_factor}` drawn from CRSP sort-based replications; its own error text says `data/` should
hold "agent-computed artifacts only (panel, bin_rets, ls_ew, ls_vw, **etc.**), not raw ClickHouse
pulls." `strategy_artifacts.parquet` is unambiguously an agent-computed artifact: 110 per-instrument
TSMOM/passive strategy series (40%/σ-scaled, signal-constructed positions) plus class factors and
benchmark proxies, computed by the engine from `panel.parquet` — not a `SELECT *` dump. SKILL.md
("The data/ folder holds computed artifacts", lines 353-363) explicitly permits intermediate
*computed* parquets ("e.g., `amihud_daily.parquet`, `delisting_returns.parquet`") and bans only raw
dumps, which are now in `<slug>/.cache/`. The slug's `data/` is policy-compliant; the validator's
allowlist is a heuristic that predates this paper type. **Not a blocker and not actionable for the
replicator** — fixing it would mean either editing the shared validator or a pointless rename.
Platform note: generalize Check 2 to flag raw-dump *patterns* (`_raw`, `_dump`, `cache_*`) instead
of an allowlist, or read an optional per-slug manifest. After this audit file exists, the false
positive is the validator's only remaining complaint (exit 1 driven by it).

## 4. Issues the agent should have caught (didn't)

1. **[m6]** — the m2 fix updated the window prose but not the example numbers on the very next
   line. The same self-review discipline prescribed for [M1] ("every number in REPORT.md against
   the eval CSVs") would have caught it: the Table 1 examples are the only §4 numbers not taken
   from a results file (they came from the diagnostic `t1_preview.csv`'s secondary column).

## 5. Next-iteration prompt (copy-paste; OPTIONAL — no auditor cycle required)

--- BEGIN COPY HERE ---

You are doing an optional cleanup touch-up on slug `time_series_momentum` (audit 2 verdict: PASS,
0 blockers, 0 majors, requires_iteration: false — see `logs/audit2.md`). The replication is
complete and REPLICATED (overall 3.50). This is a 2-minute prose fix; do NOT re-estimate anything
and do NOT spawn workers.

**[m6] — the only open item.** `REPORT.md:125` quotes five Table 1 example volatilities from the
1985–2009 diagnostic window (`data/t1_preview.csv` `vol_8509` column), contradicting the "FULL
panel window" prose directly above and the committed `results/table_1.md` / `results/eval_t1.csv`.
Replace "SP500 15.60 vs 15.45, EURUSD 11.10 vs 11.21, DAX 21.61 vs 20.41, COFFEE 39.41 vs 38.62,
COPPER 27.07 vs 27.39" with the committed full-window values from `table_1.md`: "SP500 15.34 vs
15.45, EURUSD 11.47 vs 11.21, DAX 21.59 vs 20.41, COFFEE 38.01 vs 38.62, COPPER 27.04 vs 27.39".
All five remain Tier 1; no tier counts or other prose change.

**Optional cosmetics:** (a) `logs/log2.md` says "W1–W13" but `preparations/assumptions.md` has
W1–W11 — correct the count if you touch the log; (b) §2's "avg 45.4" availability recomputes to
45.47 — leave as is or write 45.5.

**Discipline:** no code changes, no re-runs, no assumptions changes; append a note to the existing
log rather than creating a new outer iteration unless you also start the deferred CFTC/Table 6
extension (REPORT.md §7). Do not create or modify SCORE.md; the auditor maintains SUMMARY.md.

--- END COPY HERE ---
