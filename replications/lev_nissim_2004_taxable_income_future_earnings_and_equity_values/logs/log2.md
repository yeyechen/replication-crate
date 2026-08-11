---
iteration: 2
slug: lev_nissim_2004_taxable_income_future_earnings_and_equity_values
inner_iterations: 1
worker_spawns: 1
---

# Outer Iteration 2 — Reasoning Trace

## Iteration context

Audit 1 (`logs/audit1.md`, verdict FAIL) blocked the replication with
`requires_iteration: true` due to:
- **[B1] blocker**: `eval/metrics.json` missing — canonical scorer cannot
  produce per-cell tiers (everything = MISSING).
- **[M1] major**: Table 3 not implemented (29 cells MISSING).
- **[M2] major**: T2_B R_TAX-only G1 magnitude is 3.49x the paper's,
  outside the 2x Tier 2 cap.

This outer iteration addresses all three.

## Inner iteration 1: Build [B1] metrics.json, [M1] Table 3, [M2] diagnostics

**Task spec → rep-worker:**
1. Build `src/assemble_metrics.py` to walk the 83 metric names from
   `preparations/tables_to_replicate.json` and emit `eval/metrics.json`
   by looking up each cell in the per-table JSONs.
2. Build `src/regression_table3.py` mirroring `regression_table2.py`
   but with the augmented x-vector (R_TAX + R_DEF + R_CFO + PRED_1..9).
3. Investigate T2_B R_TAX-only G1 magnitude divergence (no winsorize,
   1%/99%, full-sample 0.5%/99.5%).
4. Add `src/evaluate.py` for per-cell tier printing.
5. Append iteration log entries to `preparations/assumptions.md` with
   all five required fields.

**rep-worker report:**

### [B1] — `eval/metrics.json` built

`src/assemble_metrics.py` written and tested end-to-end. The aggregator
walks the 83 metric names in `preparations/tables_to_replicate.json` and
looks up each replicated value in the appropriate
`results/table_<n>_cells.json`. For metrics we cannot compute (Table 3
cells before [M1]), the entry is omitted entirely so the canonical
scorer marks them MISSING.

**Tweaks applied during iteration:**
- Initial lookup failed for T2 full_model G1 R2 (6-element metric name
  failed a `len >= 7` check) — dropped to `len >= 6`.
- Initial lookup returned R_TAX for both b1 and b3 (suffix-collision
  via `mean_b1` → `coef=1` → `r_1`, which doesn't exist). Restructured
  the suffix map to use `term_to_col = {"b1": "r_tax", "b3": "r_cfo", "b": "r_tax"}`.
- After fixing, 54 cells populated (T2: 33, T4: 10, T5: 11), the 29 T3
  cells remained missing for [M1].

**Scorer output after [B1]:**
```
loss              = 1.2530
n_total_evaluated = 83
tier1_count       = 10
tier2_count       = 42
fail_count        = 2
missing_count     = 29  (T3 cells)
```

The 2 FAIL cells (T2_B R_TAX-only G1 mean_b1, T2_B full_model G3
mean_b1) are the [M2] magnitude divergence that the next substep
addresses.

### [M1] — Table 3 implemented

`src/regression_table3.py` written. The script:
- Constructs `pred_1` through `pred_9` via `add_pred_columns()` using
  `ib`, `at`, `dv`, `xrd`, `capx`, `sale`, `prcc_f`, `csho`, `ceq`,
  and 3-year / 5-year earnings lags (computed via
  `groupby(gvkey).shift(3/5)`).
- Runs 4 model variants per panel × G1/G3 = 16 cells.
- Reports β_1 (R_TAX), β_2 (R_DEF), β_3 (R_CFO), R², and n. The nine
  PRED coefficients are omitted from the markdown table per the
  paper's footnote 25 (parsimony).

**Caveat:** Model 4 (full model with PRED_1..PRED_9) for Panel A uses
1 year (1992) because PRED_3 needs lag_ib_3 (requires ib in 1989) and
PRED_4 needs lag_ib_5 (requires ib in 1987, but our panel only has
sparse pre-1987 data). For Panel B, Model 4 uses 7 years for G1 and 3
years for G3 (because G3 needs g3 to be non-null, which requires
1996-2000 data).

**Outputs:** `results/table_3.md` and `results/table_3_cells.json`
(with the same `schema_version: 1` structure as the other tables).

**Scorer output after [M1]:**
```
loss              = 0.9880
n_total_evaluated = 83
tier1_count       = 10
tier2_count       = 64
fail_count        = 9     (T2_B + T3_B magnitude divergence)
missing_count     = 0     (all 83 cells populated)
```

### [M2] — T2_B R_TAX-only G1 magnitude investigation

Three experiments ran via the panel iterating each year with different
winsorization:

| Winsorization | Mean β_1 | Ratio to paper (0.534) | t-stat |
|---|---:|---:|---:|
| None | +3.09 | 5.79x | (large std) |
| Within-year 0.5%-99.5% (current) | +1.86 | 3.49x | 2.69 |
| Within-year 1%-99% | +1.53 | 2.87x | 2.51 |
| Full-sample 0.5%-99.5% (paper literal) | +1.69 | 3.16x | 6.32 |

None of the winsorization variants brings the magnitude within the
2.0x Tier 2 cap. The 14-year vs 28-year window (sample truncation,
Assumption #6) is the dominant factor — within-year variance in
1993-2000 is consistently higher than the paper's 1973-2000
within-year variance, regardless of winsorization.

**Decision:** Keep the within-year 0.5%-99.5% winsorization (consistent
across T2, T3, T4, T5). Mark T2_B R_TAX-only G1 (and the T3_B
magnitude cousins) as FAIL with a [VINTAGE-DRIFT] marker. The
directional pattern (R_TAX positive) is preserved in 12/12 headline
cells.

### [m1] — `src/evaluate.py` written

`src/evaluate.py` reads `eval/metrics.json` and prints a per-cell
tier table with `--tier` and `--table` filters. Closes Spot-check 10.
A bug in the rel_err printing (tuple-unpacking mismatch) was caught
and fixed mid-iteration.

### [m2] — T5_A spec 1 R_TAX relabel

The previous log1.md labeled T5_A R_TAX spec 1 (0.007 vs paper 0.013,
r=0.54) as "Tier 1 (within 50%)" but the per-cell `tolerance_pct` is
25. Re-labeled as Tier 2 in `assumptions.md` (Assumption #15) with
[VINTAGE-DRIFT] marker cross-referenced to Assumption #6.

### [m3] — REPORT.md 5.6% caveat

The REPORT.md cannot be edited by the rep-worker (write-scope hook).
The 5.6% vs 2.8% caveat is appended to Assumption #15 instead, which
gives the next-iteration auditor and the orchestrator the same
documentation.

## Per-cell evaluation

Headline spot-check summary (per `eval/scoring.json` after iter 2):

| Table | Tier 1 | Tier 2 | FAIL | MISSING |
|---|---:|---:|---:|---:|
| T2 | 7 | 24 | 2 | 0 |
| T3 | 0 | 22 | 7 | 0 |
| T4 | 0 | 10 | 0 | 0 |
| T5 | 3 | 8 | 0 | 0 |
| **Total** | **10** | **64** | **9** | **0** |

**Loss:** 0.988 (target: 0 for full Tier 1 replication).

The 9 FAIL cells are all magnitude-divergence cells in T2_B and T3_B
(2-3.5× the paper's values) — documented with [VINTAGE-DRIFT] marker
because the cause is the 14-year vs 28-year sample window.

## Assumption decisions this iteration

- **A12** [CONVENTION-APPLIED]: Build `eval/metrics.json` from the
  per-table JSONs (the canonical scorer input).
- **A13** [CONVENTION-APPLIED]: Table 3 implemented with the augmented
  Eq. (4) (R_TAX + R_DEF + R_CFO + PRED_1..PRED_9).
- **A14** [VINTAGE-DRIFT]: T2_B R_TAX-only G1 magnitude (1.862 vs paper
  0.534, r=3.49) — within-year variance in 1993-2000 is higher than
  the paper's 1973-2000 variance. Documented as FAIL, not Tier 2.
- **A15** [VINTAGE-DRIFT]: T5_A R_TAX spec 1 (0.007 vs paper 0.013,
  r=0.54) — labeled Tier 2 with explicit [VINTAGE-DRIFT] cross-ref
  to A6.

## Summary

Three issues from audit 1 addressed in this outer iteration:

1. **[B1]** `eval/metrics.json` built and scorer now produces tiered
   results (loss = 0.99, down from 2.0).
2. **[M1]** Table 3 implemented end-to-end (29 cells now populated).
3. **[M2]** T2_B magnitude divergence investigated; magnitude is
   consistent with the 14-year vs 28-year window and the
   [VINTAGE-DRIFT] marker is applied.

The replication succeeds at the directional / pattern level (12/12
sign matches across T2, T4, T5; 12/12 across T3 model 1 and
full-model R_TAX-only G1 cells). Numerical magnitudes diverge 2-3.5x
the paper's for some T2_B and T3_B cells, documented with the
[VINTAGE-DRIFT] marker.

The next iteration could consider:
1. Recovering pre-1987 firm-years via `comp_pit.pithistdataus` to
   extend the 14-year window to 28 years.
2. Implementing BETA / VOL / GROW to unlock the deferred cells in
   Tables 4 and 5 (currently M2/M4 in T4 and M3 in T5).
3. Implementing delisting-return reinvestment in the T5 dependent
   variable.
