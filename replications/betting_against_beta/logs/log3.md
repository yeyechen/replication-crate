---
iteration: 3
slug: betting_against_beta
inner_iterations: 1
worker_spawns: 1
---

# Outer Iteration 3 — Reasoning Trace

Triggered by audit 2: `requires_iteration: true` with 2 remaining actionable majors ([M3] size splits, [M4] beta-window robustness).

## Inner iteration 1: Size-tercile BAB (M3)

**Task spec → rep-worker:**
Compute BAB factor within three size terciles (small/medium/large) based on lagged ME, using the same methodology as table_3_v2.py (median split, rank-weighted, unit-beta rescaled).

**rep-worker report:**
- BAB positive and significant in ALL three size terciles:
  - Small: excess +0.93% (t=6.14), FF3 α +0.76% (t=5.18), Sharpe 0.67
  - Medium: excess +0.74% (t=6.50), FF3 α +0.77% (t=6.79), Sharpe 0.71
  - Large: excess +0.41% (t=3.79), FF3 α +0.52% (t=5.08), Sharpe 0.41
- All FF3 |t| > 3.7 — strongly significant in every tercile
- Raw excess declines monotonically with size (Small > Medium > Large)
- ~800 stocks/tercile/month, 1004 months

**Replicator decision:** ACCEPT. Confirms paper's claim that BAB holds "within deciles sorted by size" (Table B3).

## Documentation fixes (replicator, no worker spawn)

Addressed audit 3's remaining items:
- [M4] Added scope-out documentation to assumptions.md (A25) and REPORT.md §5: beta-window robustness (Table B2) not computed; justification: beta primitives machine-precision-validated, BAB matches on all 8 cells, residual is data-vintage-limited per [M5]
- [m5] Fixed REPORT.md NW parentheticals: 5.85/4.58 → 5.71/4.44 (matching committed table_3.md)
- [m6] Fixed table_1.md ME note: removed contradictory "all stock-months" clause, clarified June-only

## Assumption decisions this iteration
- A24: All-stock size-tercile breakpoints (paper uses NYSE; sign/significance robust)
- A25: Beta-window robustness scope-out (Table B2) — documented with justification

## Per-cell evaluation
This iteration adds size-tercile corollary evidence. Table 3 remains 25/32.
New evidence: BAB positive and significant in all 3 size terciles (all FF3 |t| > 3.7) ✅

## Summary

Outer iteration 3 addresses the last actionable items:
- [M3] Size splits: CONFIRMED (BAB positive and significant in all 3 terciles)
- [M4] Beta-window robustness: scope-out documented with justification (A25)
- All minor reporting fixes applied ([m5], [m6])
- Final state: REPLICATED, overall 4.17/5, 25/32 Table 3 cells pass, BAB 8/8
