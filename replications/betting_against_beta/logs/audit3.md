---
iteration: 3
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 1
requires_iteration: true
---

# Audit Report 3 — betting_against_beta

**Verdict:** PARTIAL
**Date:** 2026-07-22
**Auditor notes:** Iteration 3 closed the one remaining *cheap* actionable major from audit 2 — [M3] cross-sectional variation by size — and I **independently re-derived every new number from scratch** (my own lagged-ME merge, my own tercile sort, my own median-split/rank-weighted/unit-beta BAB construction, and my own statsmodels excess-on-factor regressions). Every cell in `results/table_3_size.md` reproduces **exactly**, the file regenerates **byte-identical** from `src/size_terciles.py`, and the shared v2 pass leaves the audit-1/2-verified `table_3.md` **unchanged** (md5-identical; still 25/32, BAB FF3 α 0.748 / t 7.11 / Sharpe 0.75) as do the three earlier corollary files ([M1]/[M2]/[M5], all md5-identical). BAB is positive and significant (all FF3 |t| > 3.7) in all three size terciles — the paper's "within deciles sorted by size" claim (Table B3) is supported. No blockers. **Two things keep the loop open.** (1) The [M4] beta-window robustness corollary was *scoped out*, and the scope-out **rationale is sound but was never committed to any artifact** — it exists only in the orchestrator handoff to me, not in `REPORT.md` §5 or `preparations/assumptions.md`, even though audit 2 explicitly required "a rigorous scope-out with justification." That documentation gap is the single remaining actionable major (cheap to fix). (2) The two trivial reporting fixes audit 2 asked for were **not done**: [m5] the stale Newey-West parentheticals in `REPORT.md:48` (5.85/4.58 vs the committed 5.71/4.44) and the self-contradictory `table_1.md` ME note. The bright line is cleared (`REPLICATED`, overall 4.17/5); `requires_iteration: true` is driven only by the missing [M4] scope-out documentation plus the two carried-over minors.

## 1. Scores

| Dimension | Score (it.2 → it.3) | Key finding |
|-----------|:---:|-------------|
| Methodology | 4 → **4/5** | Unchanged, verified pipeline. The new size split uses **lagged ME on the full panel** (month t sorts on month t−1 ME via an exact (month+1) self-merge) — I confirmed this is the correct no-look-ahead convention: my own from-scratch calendar-merge reproduces it exactly, and my first attempt (lagging on the post-warmup panel) diverged (n=1003), confirming their convention is right. One documented deviation: **all-stock** size-tercile breakpoints (A24) rather than the NYSE breakpoints audit 2 suggested / the FF convention uses — flagged by the agent, conclusion robust, exact Table B3 cell values unavailable in the parsed paper. |
| Headline matching | 5 → **5/5** | Unchanged. BAB within ~5% on all 8 cells (FF3 α 0.748 vs 0.73; Sharpe 0.75 vs 0.78; leverage 1.44/0.69 vs 1.40/0.70); flat SML and monotonic Sharpe/alpha decline reproduce. |
| Data coverage | 4 → **4/5** | Unchanged. Universe 23,407 vs 23,538 (0.6%); CRSP dsf/msf/dsi/dsenames/dsedelist + FF all match; effective start 1928-08 vs 1926-01 (750-day beta warmup). |
| Concrete result matching | 4 → **4/5** | Still **25/32 Tier 1 (78.1%)** — the size split adds corollary evidence, not new Table 3 cells, and the committed `table_3.md` is byte-identical to audit 2. The 7 fails (P1/P5/P10 FF3 & FF4, P10 CAPM alphas) persist; diagnosed (not fixed) as data-vintage-limited via [M5]. |
| Signal strength | 5 → **5/5** | Unchanged. Headline cells r=|ours/paper|: BAB FF3 α 1.025, FF4 α 1.047, Sharpe 0.962, excess 1.021 — all in [0.9,1.1]. |
| Corollary | 3 → **3/5** | **Improved within band (now top of 3).** [M3] size split now **fully** replicates — BAB positive & significant in all three terciles (Small FF3 +0.762 t=5.18, Medium +0.768 t=6.79, Large +0.521 t=5.08; all |t|>3.7), independently verified. [M2] loadings full; [M1] subsample still directional (positive all 4 windows, significant 3/4); [M5] decile diagnosis full. **Remaining gaps:** [M4] beta-window robustness still **not computed and its scope-out not documented in-repo**, and IVOL control (Table B5) still **not computed** (scope-out documented in A24). Two named corollary predictions the paper sells (§3.1 robustness; abstract idiosyncratic-risk) thus remain unmet → still "some replicate with notable gaps." Audit 2 calibrated that *both* [M3] and [M4] must close to reach 4–5; only [M3] closed. |

**Overall: 4.17 / 5.00 → binary verdict `REPLICATED`** (mean ≥ 3.0, no dimension scored 1). Unchanged numerically from iteration 2 (corollary improved within the 3 band but does not cross to 4 until a second named corollary closes).

## 2. Issues by severity

### Blockers (must fix)

None. `prep_validation.py` will pass once `logs/audit3.md` (this file) exists and `SUMMARY.md` is overwritten; the contract is otherwise clean.

### Major (should fix) — 1 remaining (carried over from audit 2, reclassified as a documentation gap)

- [M4] Corollary 'robustness specs' (beta-window / benchmark) — **scope-out rationale NOT committed to any artifact** — PRIORITY (cheap as documentation; expensive as computation)
  - File: `inputs/content.md` Table B2 (different beta window lengths, local vs global benchmarks); §3.1 line 925 ("results are robust to alternative beta estimation procedures as we report in Appendix B").
  - Paper claim: BAB is robust to alternative beta-estimation windows and benchmark choice.
  - Status: the orchestrator chose to **scope this out** with a reasonable rationale (beta primitives validated to machine precision via `--selftest`; BAB matches on all 8 cells; [M5] confirms the decile-alpha drift is data-vintage-limited; marginal value of an alternative window is low given the verified headline). **However, that rationale lives only in the handoff note to the auditor — it is not in `REPORT.md` §5 Limitations, not in `preparations/assumptions.md` (no M4 / Table B2 entry exists; grep confirms), and there is no `logs/log3.md`.** Audit 2 explicitly permitted a scope-out but required it be *documented* ("document a rigorous scope-out with justification — which window, why it is expected to be immaterial, pointer to the paper's own robustness claim"). As a committed record the corollary is therefore still open.
  - Specific fix (pick one):
    - **(a) CHEAP — commit the scope-out.** Add an `assumptions.md` entry (A25+) with the 5-field iteration-log format AND a `REPORT.md` §5 limitation, stating: which robustness spec is omitted (alternative CORR_WINDOW/VOL_WINDOW, local vs global benchmark — Table B2), why it is expected to be immaterial here (beta primitives machine-precision-validated by `--selftest` against independent pandas; the full BAB already matches the paper on all 8 cells; the only residual — decile multi-factor alphas — is independently diagnosed as data-vintage-limited by [M5], which an alternative beta window would not resolve), and a pointer to §3.1/Table B2. This closes the actionable item without a rebuild.
    - **(b) EXPENSIVE — compute it.** Parameterize `CORR_WINDOW`/`VOL_WINDOW` in `src/main.py`, rebuild **one** alternative beta (e.g. a 3-year correlation window), and report the BAB α/Sharpe delta in `results/table_3_robustness.md`. This is the only item that needs the ~6-min daily beta pipeline, and is the path that would lift the corollary dimension 3→4.
  - actionable: true

Resolved this iteration (independently verified — see §3):
- [M3] Cross-sectional variation by size — **RESOLVED (full).** `results/table_3_size.md` (cites Table B3): BAB positive (excess, FF3, FF4 all > 0) AND significant (FF3 |t|>1.96) in **all three** lagged-ME size terciles — Small excess +0.928%/mo (t=6.14), FF3 +0.762 (t=5.18), FF4 +0.547 (t=3.73), Sharpe 0.67; Medium +0.741 (t=6.50), FF3 +0.768 (t=6.79), FF4 +0.599 (t=5.33), Sharpe 0.71; Large +0.413 (t=3.79), FF3 +0.521 (t=5.08), FF4 +0.424 (t=4.09), Sharpe 0.41. Raw excess declines monotonically with size (Small>Medium>Large; economically largest among small caps); Sharpe peaks in Medium, weakest in Large. I re-derived every cell with my own code (see §3 check 2). Honestly notes the full-cross-section reference row (FF3 +0.753, t=7.20) tracks the headline BAB (0.748, t=7.11) on the size-sortable subset, and that the paper's claim is about within-group sign/significance, not matching the full-cross-section level. IVOL (Table B5) correctly flagged out-of-scope (A24).

Carried over, still open (from audit 2 — not addressed this iteration):
- [M1] Subsample stability — resolved *directionally* in audit 2 (positive all 4 windows, significant 3/4; SP1 1928-1948 sub-significant, honestly attributed to the 1928-08 start). Unchanged this iteration (file md5-identical). Not blocking.

Non-actionable (data-limited — do NOT block the loop, unchanged from audits 1/2):
- 5-factor alpha (Pastor-Stambaugh liquidity factor not in ClickHouse; A2).
- International equities (Tables 4-5) — Xpressfeed Global not in catalog.
- Other asset classes (Tables 6-8) — proprietary data unavailable.
- TED time-series (Table 9, Prop 3) and beta-compression (Prop 4) — TED series likely unavailable.
- Constrained-investor holdings (Prop 5, Tables 10) — mutual-fund/brokerage/13F data unavailable.

### Minor (cleanup)

- [m5] **CARRIED OVER (2nd flag) — still unfixed.** `REPORT.md:48` still reads "FF3 t-statistic is 7.11 … Newey-West: 5.85 … FF4 t-statistic is 5.54 … Newey-West: 4.58". The iid values (7.11/5.54) correctly match the final `table_3.md`, but the NW parentheticals (5.85/4.58) are the **v1** NW(6) figures; the committed `table_3.md:54` NW block shows BAB **FF3 NW 5.71, FF4 NW 4.44**. REPORT.md still pairs v2 iid with v1 NW — internally inconsistent with the committed table. This is the same error class audit 1 flagged as [m2]; it has now survived three iterations.
  - Fix: change REPORT.md §2 NW parentheticals (5.85/4.58) → (5.71/4.44). The iid values are correct — leave them.
- [m6] **CARRIED OVER (nit) — still unfixed.** `results/table_1.md` notes still say the mean-ME metric is "averaged across all stock-months (not June-only as the paper describes)" and then state "the June-only mean firm ME is 0.996 $B, matching the paper." The reported value (0.996, the June figure) is correct; the explanatory sentence is self-contradictory. Fix: state the metric is the June mean; drop the contradictory clause.
- [m7] **NEW (nit).** A24 uses **all-stock** size-tercile breakpoints; the paper's Table B3 (FF convention) and audit 2's suggested fix use **NYSE** breakpoints. Documented and flagged by the agent, and the sign/significance conclusion is robust (all |t|>3.7), so this is not a blocker — but the agent should note in A24/table_3_size.md that exact tercile *levels* (avg ME, stocks/mo) could shift under NYSE breakpoints even though the qualitative result holds. Optional one-line clarification.

Confirmed fixed / stable from audit 2:
- [M3] computed and verified (this iteration). ✓
- No orphan files introduced; `src/size_terciles.py` is thin and reuses the verified v2 pass. ✓
- The three audit-2 corollary files ([M1]/[M2]/[M5]) are md5-identical — not disturbed. ✓
- `table_3.md` md5-identical — headline table not disturbed by the shared pass. ✓

## 3. Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Determinism of `table_3_size.md` | ✓ | Backed up the file, re-ran `src/size_terciles.py` (exit 0, 11.5s). Output **byte-identical** to committed except the `_Runtime_` line (10.9s→11.5s). Console reproduced: Small 0.928/6.14/0.762/5.18/0.547/3.73/0.67, Medium 0.741/…/0.71, Large 0.413/…/0.41, FULL 0.721/6.95/0.753/7.20/0.76. |
| 2 | [M3] size-tercile numbers — **independent from scratch** | ✓ | Wrote my own script reusing only the verified v2 panel (`df` + `ff`), and independently re-implemented: lagged-ME (calendar (month+1) self-merge on the **full** panel), within-month 1/3–2/3 tercile assignment, the median-split/rank-weighted/unit-beta BAB, and plain-statsmodels excess-on-factor regressions (intercept = alpha; iid t; Sharpe = mean/std_pop·√12). Result reproduced **every cell exactly**: Small n=1004, 801 stk/mo, $14.9M, ex 0.928(t6.14), FF3 0.762(t5.18), FF4 0.547(t3.73), Shp 0.672; Medium 800/$93.6M/0.741(6.50)/0.768(6.79)/0.599(5.33)/0.711; Large 800/$2236.9M/0.413(3.79)/0.521(5.08)/0.424(4.09)/0.415; FULL 2401/$781.8M/0.721(6.95)/0.753(7.20)/0.582(5.63)/0.760. (My *first* attempt lagged ME on the post-warmup panel and got n=1003 / slightly different values — confirming their full-panel lag is the correct convention, not a bug.) |
| 3 | Lagged-ME no-look-ahead convention | ✓ | `size_terciles.lag_me` shifts each stock's ME forward one calendar month via exact (month+1) self-merge on the full panel (so month-t sort uses only month-(t−1) ME; monthly gaps do not leak an older ME). My independent calendar-merge matched it exactly. Rows with null/zero lagged ME dropped (1,983). |
| 4 | Headline table undisturbed | ✓ | `table_3.md` md5-identical to the audit-2 backup. Still **25/32**; BAB excess 0.715 / FF3 α 0.748 (t 7.11) / Sharpe 0.750 — the audit-1/2-verified series. The shared v2 pass in `size_terciles.py` does not rewrite it. |
| 5 | Earlier corollaries undisturbed | ✓ | `table_3_subsample.md`, `table_b1.md`, `table_3_post1962.md` all md5-identical to audit-2 backups ([M1]/[M2]/[M5] byte-stable). |
| 6 | REPORT.md §4 ↔ table_3_size.md consistency | ✓ | REPORT.md §4 size table (Small +0.93/6.14, FF3 +0.76/5.18; Medium +0.74/6.50, FF3 +0.77/6.79; Large +0.41/3.79, FF3 +0.52/5.08; Sharpes 0.67/0.71/0.41) matches `table_3_size.md` to rounding. |
| 7 | [M3] conclusion robustness | ✓ | BAB positive & significant (FF3 |t|>1.96, in fact all >3.7) in all 3 terciles — the qualitative Table B3 claim holds strongly and is not sensitive to the all-stock-vs-NYSE breakpoint choice at the sign/significance level. |
| 8 | Iteration-log discipline (A24 + M3 entry) | ✓ | `assumptions.md` A24 (all-stock tercile decision) + the [M3] iteration-log block each carry Diagnosis / Next fix / Before / After / Status; IVOL scope-out documented (A24 line 425). |
| 9 | [M4] scope-out documentation present? | ✗ (finding) | Grepped all `*.md`/`*.py` for M4 / beta-window / Table B2 / "6 min" / "immaterial" / scope-out phrases: **no** M4 or beta-window scope-out entry exists in `REPORT.md` or `assumptions.md`. The rationale is only in the orchestrator handoff. This is [M4] above. |
| 10 | [m5] NW parentheticals fixed? | ✗ (carried) | `REPORT.md:48` still shows NW 5.85/4.58 (v1) while `table_3.md:54` shows 5.71/4.44 (v2). |
| 11 | [m6] table_1.md ME note fixed? | ✗ (carried) | Still self-contradictory ("averaged across all stock-months … the June-only mean firm ME is 0.996"). |
| 12 | Conservative tier labeling / no inflation | ✓ | Agent still labels the 7 decile alphas FAIL (25/32 unchanged); the size split is framed as corollary evidence, not a pass-count change; A24 flags the breakpoint deviation and the IVOL scope-out honestly. |

## 4. Issues the agent should have caught (didn't)

1. **The [M4] scope-out was never written into the repo.** The orchestrator's handoff says [M4] was "documented as scope-out with justification," but no such documentation exists in any committed file — not `REPORT.md` §5, not `assumptions.md` (there is no M4/Table B2 entry), and there is no `logs/log3.md`. Audit 2 explicitly required the scope-out be *documented* with justification; the justification is reasonable but must be committed to count. This is the single remaining major and is a trivial documentation fix.
2. **The [m5] Newey-West reporting slip survived a third iteration.** Audit 1 flagged the v1↔v2 t-stat mismatch ([m2]); the agent fixed the iid values but left the adjacent NW values at v1 (5.85/4.58); audit 2 re-flagged this as [m5]; iteration 3 did not touch it. `REPORT.md:48` still pairs v2 iid (7.11/5.54) with v1 NW (5.85/4.58) while the committed `table_3.md:54` reads 5.71/4.44. Trivial but a recurring reproducibility paper-cut.
3. **The `table_1.md` ME note is still self-contradictory** (June vs all-months) — the audit-2 nit was not applied.
4. **(nit) The all-stock size-breakpoint deviation could carry a one-line caveat** that exact tercile *levels* may differ under the paper's NYSE breakpoints (the sign/significance conclusion is unaffected).

## 5. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Betting against beta" (Frazzini &
Pedersen, 2014) for slug `betting_against_beta`. The previous run completed
with audit verdict **PARTIAL** (audit 3 at
`replications/betting_against_beta/logs/audit3.md`). Read that audit first.

State of play — the replication is strong and **already clears the bright line
(`REPLICATED`, overall 4.17/5)**. The headline US BAB factor replicates within
tolerance on all 8 Table 3 metrics (FF3 α 0.748 vs 0.73, iid t 7.11; Sharpe
0.75 vs 0.78; leverage 1.44/0.69 vs 1.40/0.70); the run is deterministic; and
four corollaries are now verified (the auditor re-derived the new one
number-for-number): subsample stability ([M1], positive in all four 20-yr
windows, significant 3/4), factor loadings ([M2], all four signs match), the
post-1962 decile-alpha diagnosis ([M5], P1 FF4 matches the paper exactly;
P10 FF4 flip statistically zero), and **cross-sectional variation by size
([M3], BAB positive & significant in all three lagged-ME terciles — Table B3)**.
This iteration closes the **last open items**, all of them cheap — no pipeline
rebuild is required unless you *choose* option (b) on [M4].

## Issues to address (priority order)

### [M4] — MAJOR — beta-window robustness scope-out is NOT documented in-repo
The decision to scope out Table B2 (alternative beta windows / local vs global
benchmark) is reasonable, but the justification lives only in the orchestrator
handoff — it is in NO committed file. Audit 2 required it be documented. Pick
ONE:
- **(a) CHEAP (preferred) — commit the scope-out.** Add `assumptions.md` A25
  (5-field iteration-log format) AND a `REPORT.md` §5 limitation stating: which
  spec is omitted (alternative CORR_WINDOW/VOL_WINDOW + local/global benchmark,
  Table B2 / §3.1), why it is expected to be immaterial here (beta primitives
  machine-precision-validated by `src/main.py --selftest` against independent
  pandas; the full BAB already matches the paper on all 8 cells; the only
  residual — decile multi-factor alphas — is independently diagnosed by [M5] as
  data-vintage-limited, which an alternative beta window would not fix), and a
  pointer to §3.1/Table B2. This closes the actionable item with no rebuild.
- **(b) EXPENSIVE — compute one alternative beta window** (parameterize
  CORR_WINDOW/VOL_WINDOW in `src/main.py`, rebuild e.g. a 3-year correlation
  window via the ~6-min daily pipeline, report the BAB α/Sharpe delta in
  `results/table_3_robustness.md`). This is the path that would lift the
  corollary dimension 3→4, but it is optional given (a) is acceptable.

### Minor — cleanup (both carried over, both trivial)
- [m5] Fix `REPORT.md` §2 NW parentheticals from (FF3 5.85 / FF4 4.58) to the
  committed-table values (FF3 5.71 / FF4 4.44) to match `results/table_3.md:54`.
  The iid values (7.11 / 5.54) are already correct — leave them.
- [m6] In `results/table_1.md` notes, state the mean-ME metric is the June mean;
  remove the contradictory "averaged across all stock-months" clause.
- [m7] (optional) Add a one-line caveat in A24 / `table_3_size.md` that the size
  terciles use all-stock breakpoints (the paper/FF convention is NYSE) and that
  exact tercile *levels* could shift under NYSE breakpoints even though the
  sign/significance result is robust.

## Iteration discipline reminders
- **Diagnose → commit-fix → fix → verify.** Every iteration-log entry in
  `assumptions.md` keeps all five fields: Diagnosis, Next fix, Before metric,
  After metric, Status.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** Hard stop at 10 and escalate.

## Inputs you should read
- `replications/betting_against_beta/logs/audit3.md` — this audit
- `replications/betting_against_beta/inputs/content.md` — §3.1 line 925 +
  Table B2 (the beta-window robustness claim)
- `replications/betting_against_beta/REPORT.md` — §2 NW parentheticals ([m5]),
  §5 limitations ([M4] scope-out), §4 corollary evidence
- `replications/betting_against_beta/preparations/assumptions.md` — add A25

## What NOT to redo
- Skip re-reading `SKILL.md`.
- Do NOT recompute [M1]/[M2]/[M3]/[M5] — all verified and byte-stable.
- Do NOT rebuild the panel or re-derive the BAB factor (verified).
- Do NOT rebuild betas for [M4] unless you deliberately choose option (b).
- Skip re-running `scripts/prep_validation.py` unless you change a prep artifact
  (after this audit it should pass).

## Deliverables for this iteration
- [M4]: `assumptions.md` A25 + `REPORT.md` §5 scope-out (option a), OR
  `results/table_3_robustness.md` + A25 (option b).
- [m5]/[m6]/[m7]: the trivial REPORT.md / table_1.md / A24 edits.
- Do NOT edit `SUMMARY.md` (auditor-owned).

## Stop conditions
- **[M4] scope-out committed (option a) OR one alternative beta computed
  (option b)** → re-run prep_validation.py; declare success.
- **Data-limited gaps (5-factor, international, other asset classes, TED,
  Prop-5 holdings, IVOL/Table B5)** are NON-actionable — document, do not loop.
- **10-iteration cap** on a single problem → escalate, write a partial
  REPORT.md; do not edit SUMMARY.md.

--- END COPY HERE ---

## 6. Auditor's notes (free-form)

This was another clean, honest, additive iteration. The [M3] size split is
exactly the cheap, high-value corollary audit 2 asked for, and it is done the
right way: it reuses the verified v2 pass (no beta re-estimation, no panel
rebuild), it lags ME one month on the full panel for a genuine no-look-ahead
sort, and it reuses the same delisting-adjusted returns so the within-tercile
factors are apples-to-apples with the headline BAB. I could reproduce **every**
cell with my own from-scratch code — including a nice self-check: my first
independent attempt lagged ME on the *post-warmup* panel and came out at n=1003
with slightly different values, which both explained the discrepancy and
confirmed that their full-panel lag is the correct convention. The conclusion
(BAB positive and significant in all three size terciles, all FF3 |t|>3.7) is
strong and robust to the all-stock-vs-NYSE breakpoint choice.

Two things keep this at PARTIAL rather than closing the loop, and both are about
*documentation discipline* rather than substance. First, the [M4] beta-window
robustness corollary was scoped out — a defensible call, and the rationale
(beta primitives machine-precision-validated, BAB matches on all 8 cells, the
only residual is the data-vintage-limited decile alphas that an alternative
window would not fix) is the right one — but that rationale was never written
into the repo. It exists only in the handoff to me; there is no M4/Table B2
entry in `assumptions.md` or `REPORT.md`. Audit 2 explicitly allowed a scope-out
but required it be documented, so this stays open as a (trivially fixable) major.
Second, the two trivial reporting fixes audit 2 requested were simply not done:
the stale Newey-West parentheticals in `REPORT.md:48` (now flagged for the
second time, having survived three iterations in various forms) and the
self-contradictory `table_1.md` ME note. Neither is hard; they are just the kind
of reproducibility paper-cuts a careful reader trips on.

On scoring: the corollary dimension improved within the 3 band — [M3] is now a
clean full replication alongside [M2] loadings and the [M5] diagnosis — but it
does not cross to 4 because two named corollary predictions the paper sells
remain unmet: beta-window robustness (§3.1/Table B2, uncomputed and
undocumented) and the idiosyncratic-vol control (Table B5, uncomputed; scope-out
documented). Audit 2 calibrated that *both* [M3] and [M4] must close to reach
4–5; only [M3] closed, so 3/5 holds (now at the top of the band). The overall
stays 4.17/5, `REPLICATED`. Committing the [M4] scope-out (option a) plus the two
minors would bring this to a clean terminal state at 4.17; actually *computing*
one alternative beta window (option b) is the one move that would lift corollary
to 4 and the overall to ~4.33.

Bottom line: `REPLICATED`, overall 4.17/5, with one documentation-only major
([M4] scope-out) and two trivial reporting fixes ([m5], [m6]) standing between
this and a clean close.
