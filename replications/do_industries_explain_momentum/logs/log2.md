---
iteration: 2
slug: do_industries_explain_momentum
inner_iterations: 1
worker_spawns: 1
---

# Outer Iteration 2 — Reasoning Trace

Audit 1 verdict: PARTIAL, overall 3.83/5.00 (REPLICATED), blocker_count=0,
actionable_major_count=1 (M4), requires_iteration=true. M1–M3 classified
non-actionable (documented CRSP-vintage limitations) — not re-litigated per
the audit's next-iteration prompt.

## Inner iteration 1: [M4] long/short leg-asymmetry corollary + minors m1-m3
**Task spec → rep-worker:**
Compute the paper's abstract-level leg-asymmetry claim (L35: industry momentum
long-driven; individual momentum loser-driven; §IV.B L1159: (1,1) industry
strategy balanced) from the frozen cohorts. Legs measured against the
equal-weighted market r̄_t (L246; footnote-14 EW index). Deliver
results/legs_long_short.md + results/cells_legs.json with binary PASS/FAIL on
each claim; reuse tables_1_2_3 engines; integrity-check spreads against
0.004135/2.311 and 0.003972/2.359.

**rep-worker report:**
- Benchmarks: r̄ = 0.012891/mo (corr 0.999 with panel ew_mkt, per footnote 14); r̄_ind = 0.010161/mo.
- Individual (6,6): W = 0.013067, L = 0.008931. Long contribution (W−r̄) = +0.000176 (t=0.11); short contribution (r̄−L) = +0.003959 (t=2.64). Verdict: LOSER-DRIVEN → matches paper. Spread integrity exact (0.004135/2.311, max leg-engine deviation 2.8e-17). Matches the audit's independent recompute (+0.0040/+0.0002).
- Industry (6,6): Wi = 0.012423, Lo = 0.008451. Long (Wi−r̄_ind) = +0.002261 (t=2.34); short (r̄_ind−Lo) = +0.001711 (t=1.89). Verdict: LONG-DRIVEN → matches paper. Spread integrity exact (0.003972/2.359). Honest caveat: the paper's Wi−Mid/Mid−Lo split (0.0036/0.0007) is reversed in our magnitudes (0.0015/0.0025, both Tier 2) — reported as a vintage finding; the market-relative decomposition supports the directional claim.
- Industry (1,1): long +0.005592 (t=5.09), short +0.006632 (t=6.15); |Δ| = 0.0010 ≤ 0.002 → BALANCED → matches §IV.B.
- cells_legs.json: 3 binary claims PASS, 4 contribution cells corroborate_claim, 2 Tier-2 (wimid/midlo).
- prep_validation.py exit 0 after the worker's changes.

**Replicator decision:** ACCEPT. M4 resolved — all three abstract-corollary claims corroborated with exact integrity checks. REPORT.md updated (bottom line, §2 leg-asymmetry paragraph with the Wi−Mid/Mid−Lo caveat, §6 audit-closure note).

**Minors closed by the replicator (no worker needed):**
- [m1] REPORT.md bottom line now states all three pass-rate conventions explicitly: Tier-1 only 50.5%; Tier-1 + 2×-bounded Tier-2 80.7% (657/814; audit's symmetric variant 78.6%); sign-only Tier-1+Tier-2 91.0%. Beyond-2× Tier-2 cells enumerated (84; 14 non-t-stat, listed in the iteration-2 computation).
- [m2] REPORT.md §1 + log1.md L44 corrected: universe counts that match exactly are at the SQL/msenames-join layer; the frozen panel runs 1–73 stocks lower per date (1980-06: 4,559, −1.6%).
- [m3] The two duplicate Assumption-18 entries merged into one (winsorization decision + fat-tail diagnosis + residual ret_1_1 finding).

## Assumption decisions this iteration
- M4 iteration entry appended to assumptions.md by the worker (Diagnosis/Next fix/Before "corollary not computed"/After: four contribution numbers + verdicts/Status resolved).
- A18 deduplicated (no content change to the decision).

## Per-cell evaluation (supplement: legs corollary, 9 cells)
| Cell | Paper | Ours | Status |
|------|-------|------|--------|
| stk_66_loser_driven | 1 | 1 | PASS |
| ind_66_long_driven | 1 | 1 | PASS |
| ind_11_balanced | 1 | 1 | PASS |
| stk_66_long_contrib / short_contrib | — | +0.0002 / +0.0040 | corroborates |
| ind_66_long_contrib / short_contrib | — | +0.0023 / +0.0017 | corroborates |
| ind_66_wimid / midlo | 0.0036 / 0.0007 | 0.0015 / 0.0025 | Tier 2 (ordering reversed, both same-sign) |

Contracted-table tallies unchanged (frozen): T1 105/18/11 · T2 10/8/6 · T3 100/127/13 · T6 196/177/43 · TOTAL 411/330/73/0 of 814.

## Summary
The single actionable major from audit 1 (M4) is resolved: the paper's abstract leg-asymmetry claims are all corroborated (individual loser-driven; industry long-driven; (1,1) balanced), with spread integrity verified to machine precision, and the one magnitude-level disagreement (Wi−Mid vs Mid−Lo ordering at (6,6)) is reported honestly as a vintage finding. Minors m1–m3 closed. M1–M3 remain documented non-actionable vintage limitations per the audit's classification. Ready for audit 2.
