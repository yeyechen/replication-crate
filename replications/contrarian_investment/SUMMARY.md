---
schema_version: 2
slug: contrarian_investment
iteration: 2
audit_verdict: PASS
verdict: REPLICATED
overall: 4.33
methodology: 4
headline_matching: 5
data_coverage: 4
concrete_result: 5
signal_strength: 4
corollary: 4
generated_at: 2026-07-22T00:00:00Z
---

# Replication Summary

## Lakonishok, Shleifer & Vishny (1994) — "Contrarian Investment, Extrapolation, and Risk"

### Bottom line

**Replication result:** `REPLICATED`
**Overall quality:** 4.33 / 5.00
**Audit state:** `PASS`

All eight empirical tables and both figures of LSV (1994) were rebuilt from raw
CRSP/Compustat, and every central claim was independently re-verified: value beats
glamour by ~10–11pp/yr, the spread survives in the largest 50% of firms, it holds in
all 18 five-year windows across all three classifications, value loses less in the
worst market months, book-to-market collapses once cash flow and past growth enter a
multiple regression, and the betas are far too small to explain the spread. 90.6% of
1,290 cells match the paper within tolerance (94.9% including same-sign pattern
matches). The two items that held audit 1 at PARTIAL are fixed and were verified from
scratch: the self-report now matches the computed artifacts throughout, and the Table
VII market-state window is bounded to months whose active cohort is within its 5-year
holding horizon (with the worst-25/best-25 month sets proven unchanged). The binary
`REPLICATED` label reflects that the headline findings and their derivative
predictions all hold on modern data; it does **not** mean every reported number
matched exactly — the residual ~5% of cells drift in a single, well-understood
direction (restated 2026 Compustat fundamentals vs the authors' early-1990s vintage).
No blockers and no actionable majors remain; the audit loop closes.

## Quality assessment

| Dimension | Score | Assessment |
|---|---:|---|
| Methodology | 4/5 | Full pipeline traces to line-cited rules; book-equity hierarchy, fiscal alignment, GS rank, delisting gross-up, Hansen-Hodrick SEs, and the pooled Panel-3 reading were each verified against the paper or tested head-to-head. Table VII now enforces an in-horizon assertion (0 violations in the auditor's recompute); the SIZE level gap is honestly left unattributed after the median hypothesis was tested and rejected. |
| Headline matching | 5/5 | All five central claims match in shape, sign, and magnitude class; AR spreads within ~3–6%, the 18/18 consistency exact, the FM B/M collapse exact, and the worst-month value cell matches the paper exactly (−0.086). |
| Data coverage | 4/5 | Exact sample period and matching CRSP + Compustat + FF sources; ~76% book-equity coverage (vintage-thin early years); one documented external gap (BEA GNP, so Table VII Panel 2 is not computed). |
| Concrete result matching | 5/5 | 90.6% Tier-1 (1,169/1,290), 94.9% Tier-1+2; all 55 pattern cells same-sign and within 2x of the paper; the auditor re-derived the Table VII machinery from scratch with ten of ten cells matching to six decimals. |
| Signal strength | 4/5 | Headline signal cells within ~5% (value-glamour spread, EW-index beta, the 18/18 consistency), but supporting extrapolation levels (Table V) and the E/P+/C/P+ regression slopes drift 15–50% on the modern vintage — all with correct sign and significance. |
| Corollary | 4/5 | Large-cap robustness, horizon consistency, downside risk, the beta/risk null, variable significance, and the extrapolation direction all reproduce; the one reversing corollary (C/P×GS raw-volatility ordering) is disclosed with its vintage explanation, and the GNP-state corollary is out of scope (no external data). |

## What replicated and what it validates

| Paper output | High-level evidence | What it supports |
|---|---|---|
| Tables I–III | Decile AR gradients strictly monotonic (B/M 0.098→0.206 vs 0.093→0.198; C/P, E/P likewise); C/P×GS corners 0.109/0.213 vs 0.114/0.221; large-cap spread +8.3pp vs +7.8. | Universe/PIT membership, April formations, all four signal definitions, EW annual buy-and-hold with delisting replacement, CR5/SAAR machinery, and the "the result is in the big stocks" robustness. |
| Table IV | B/M coefficient collapses to ~0 (t 0.55–0.82) once GS and C/P+ enter, while GS (t ~ −2.7) and C/P+ (t ~ +2.1…+2.4) stay significant. | The Fama-MacBeth variable-significance hierarchy and the claim that book-to-market is subsumed. |
| Table V | Glamour run-up RETURN(−3,0) +1.58 vs +1.46; the internal-consistency check 0.076×(1.123)^5 = 0.136 = the paper's 5-yr-ahead C/P. | The per-$1-invested growth machinery and the extrapolation mechanism's direction (level magnitudes carry the vintage drift). |
| Table VI | Mean spreads and t-stats within the paper's; **value > glamour in all 18 five-year windows in all three panels** (min spread +0.21…+0.42). | Overlapping-horizon inference (Hansen-Hodrick) and the consistency-of-outperformance prediction. |
| Table VII | W25 value −0.086 = the paper exactly; value loses less in W25 and N88 for both classifications; states now classified only over months within the active cohort's 5-year horizon (312 months, 25/88/122/25 semantic partition). | The no-downside-risk claim (Panel 1). Panel 2 (GNP states) is out of scope — external BEA data not in ClickHouse. |
| Table VIII | EW-index beta 1.339/std 0.268 vs 1.304/0.250; portfolio betas 1.1–1.5 with value−glamour gaps (−0.05 to −0.18 by classification) explaining ≤1.4pp/yr of the spread. | The "contrarian strategies are not fundamentally riskier" conclusion. |

## Important gaps

- **Data vintage (non-actionable):** the dominant residual. Restated 2026 Compustat fundamentals run ~15–50% above the authors' early-1990s extract for deep-value portfolios, which inflates ratio levels (Table V), halves the E/P+/C/P+ regression slopes (Table IV), shifts near-zero size-adjusted cells (Tables I–III, VIII), and reverses the C/P×GS raw-volatility ordering (now disclosed in REPORT §3). No methodology change closes a vintage gap; the qualitative findings all survive it.
- **External data unavailable (non-actionable):** Table VII Panel 2 (real-GNP states) needs quarterly BEA GNP, absent from ClickHouse; the paper states Panel 2 mirrors Panel 1, which is replicated.
- **OCR-unrecoverable window (non-actionable):** the paper's exact 260-month EW window for Table VII cannot be reconstructed from the parsed text; the semantic state rule is preserved on a horizon-bounded 312-month window, leaving one moderate-month-composition residual (P_122 t-stat) that is numerical, not methodological.
- **OCR truncation (non-actionable):** the parsed Table VIII Panel 2 (and Panel 3 deciles 7–10) is column-garbled, so those portfolio cells were computed but left unscored.
- **Early-formation coverage (non-actionable):** pre-1974 formations rest on thinner Compustat coverage (the paper's own 1978 expansion), making early-year cells noisier — the source of most Table VI year-cell and Table V earnings-growth residuals.
- **Cosmetic cleanup items (see `logs/audit2.md`, minors):** a stale REPORT header tally/reference, two stale in-code docstrings in table7.py, a slightly inaccurate month list in the iteration log, and hash-unstable JSON key order in two emitters (values verified identical). None touches a paper-facing number.
