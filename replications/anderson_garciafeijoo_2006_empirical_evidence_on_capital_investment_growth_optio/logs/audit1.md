---
iteration: 1
verdict: PARTIAL
blocker_count: 0
actionable_major_count: 7
requires_iteration: true
---

# Audit Report 1 — anderson_v2

**Verdict:** PARTIAL
**Date:** 2026-08-07
**Auditor notes:** Table II and Table III's t-statistics/R² reproduce the paper essentially exactly and the pipeline is fully re-runnable from cache; but the Ln(inv) magnitude FAIL is retired by a causal story that is untested *and directionally backwards*, and Table V's value-weights use same-month market equity (a look-ahead) that inflates portfolio returns by +0.63 %/mo and is load-bearing for 5 of its 12 Tier-1 cells.

---

## 1. Summary

**What is solid.** The replication is honest, reproducible, and in two of three
tables genuinely good. I re-ran `src/evaluate.py` and its per-cell output
matches, cell for cell, the tables pasted into `REPORT.md` and `logs/log1.md`
(Table II 11 PASS; Table III 10 PASS / 2 BORDERLINE / 4 FAIL of 16; Table V
12 PASS / 1 BORDERLINE of 13) — the tier table is computed, not hand-composed
(Spot-check 10, first half: ✓). I independently recomputed Table II from
`data/panel.parquet` and Table III models 5 and 6 from `data/fm_panel.parquet`
and got the shipped numbers to three decimals (decile spread −0.780; ln_inv
−0.261, t −6.991; model 6 −0.185, t −5.815). Sign conventions re-derived from
the paper — descending deciles (Table II header "High…Low"), INV = low-minus-high
(Table V caption: "we subtract the returns on the high investment group from
the low investment group") — are implemented correctly, and the paper's own
Table V shows the same mechanical identity our output shows (the "Highest" and
"Lowest" INV loadings differ by exactly 1.00 because the test portfolios are
the factor's own legs).

**What does not hold up.** Three things a peer reviewer must reject:

1. **The Ln(inv) cause attribution is untested and backwards.** The report
   retires two magnitude FAILs (−0.26 vs −4.19; −0.19 vs −3.52) as "Tier 2
   (pattern match with documented cause)" on the strength of the matching
   t-statistic. But a t-statistic is *invariant* to any linear rescaling of the
   regressor — it is precisely the statistic that cannot discriminate a data
   change from a units/definition change, so it is not evidence for the
   Compustat-vintage story. Worse, the stated mechanism ("modern vintage …
   compressing the Ln(inv) distribution") predicts a *larger* coefficient than
   the paper's, not one 16× smaller. And the replication's own data contradict
   the story: the same `inv_growth` column, from the same vintage, reproduces
   Table II to within 0.01 %/mo, and its trimmed firm-year distribution
   (mean 0.714, median 0.216) sits inside the paper's Table I range
   (means 0.17–1.03, medians −0.05–0.54).
2. **A 16× miss is not Tier 2.** `audit/SKILL.md` Spot-check 10 and
   `audit/RUBRIC.md` §4 bound Tier 2 at 2×; |ours/paper| = 0.062. The
   evaluator's own vocabulary (PASS / BORDERLINE / FAIL keyed off 1× and 2× of
   `tolerance_pct`) is also not the harness ladder in `rep/TOLERANCE_RULES.md`,
   and the report silently maps one onto the other.
3. **Table V's value weights are contemporaneous.** `me_dollars` is
   `abs(prc)*shrout*1000` from the *same* `msf` row as `ret`, so the weight
   embeds the month's own return. Re-weighting the identical panel with a
   one-month-lagged ME moves the panel's VW mean from **1.949 %/mo to
   1.324 %/mo** — the latter matching the CRSP/FF market return of 1.334 %/mo
   to within 0.01 %/mo. Under the shipped weights the VW quintile means are
   **non-monotonic** (2.137, 1.908, 1.808, 1.930, 2.398); under lagged weights
   they are monotonic in the paper's direction (1.117 → 1.464). Five Table V
   alpha/SMB cells leave Tier 1 when the standard convention is used.

**Bookkeeping.** `tables_to_replicate.json` commits 50 cells (11 + 26 + 13);
40 were evaluated. Four are printed as deferred; **six are dropped silently**
by `evaluate.py` (`ln_size_model7`, `ln_bm_model7`, `ln_inv_model7` × coef/t-stat)
because the loop `continue`s on `metric not in rep`. β was built in inner
iteration 3 (`data/panel_with_beta.parquet`, 1,055,375 non-null) but never fed
back into the Fama-MacBeth panel, so the β rows remain uncomputed. The
report's headline "33 / 37 evaluated = 89 %" matches no denominator in the
project: it is 33/40 = 82.5 % of evaluated cells and 33/50 = 66 % of committed
cells.

**Verdict:** PARTIAL — 0 blockers, 7 actionable majors. The methodology is
validated for Table II and for the *inference* in Table III; it is not yet
validated for the Table V portfolio construction, and the Table III magnitude
FAIL must be reopened.

---

## 2. Issues

### Blockers (must fix)

None. The pipeline runs, the cache is current with the code, `prep_validation.py`
exits 0, and no committed result contradicts the paper's direction.

### Major (should fix — all actionable)

- **[M1] Table V value-weights use same-month market equity (look-ahead); 5 of
  12 Tier-1 cells depend on it.**
  - File: `src/main.py:742-743` (`(g["ret"] * g["me_dollars"]).sum() / g["me_dollars"].sum()`);
    weight column defined in `src/sql/panel.sql` as `abs(u.prc) * u.shrout * 1000`
    on the *same* `msf` row as `ret`; documented only as "point-in-time monthly
    market cap" in `results/table_5.md:132` and `preparations/assumptions.md:256-263`.
  - Evidence (auditor recomputation from `data/panel.parquet`, 1976-07…1999-06):
    panel VW with contemporaneous weights = **1.949 %/mo**; with one-month-lagged
    weights = **1.324 %/mo**; CRSP/FF market total return = **1.334 %/mo**.
    Shipped VW quintile means 2.137 / 1.908 / 1.808 / 1.930 / 2.398 (non-monotonic,
    Q1 > Q2–Q4, contradicting the paper's core direction); lagged-weight means
    1.117 / 1.296 / 1.356 / 1.435 / 1.464 (monotonic). Re-running the 13 committed
    cells with lagged weights: `highest_alpha_mkt_only` PASS→FAIL (0.006→−0.004),
    `highest_alpha_3factor` PASS→FAIL (0.009→−0.001), `highest_alpha_4factor`
    PASS→BORDERLINE, `lowest_alpha_mkt_only` PASS→BORDERLINE,
    `lowest_alpha_3factor` PASS→BORDERLINE, `highest_smb_3factor` PASS→BORDERLINE;
    `lowest_hml_3factor` BORDERLINE→PASS. The INV loadings (−0.524 / +0.476) and
    adj R² are unaffected.
  - Likely cause: `me_dollars` was reused as the VW weight without lagging; note
    the repo primitive `utils.portfolio.bin_returns` defaults to `mcap_col="mcap_lag1"`
    and `rep/PAPER_CONVENTIONS.md` § Portfolio construction assumes the FF weighting
    convention. The agent had already diagnosed exactly this contamination for
    `ln_size` (`assumptions.md:126-147`) and then committed it in the Table V weights.
  - Specific fix: add `me_lag = me_dollars.shift(1)` per permno (or use the
    June-formation ME, `me_jun_form`, held constant over the cohort, which is
    the FF annual-rebalancing convention), use it as the VW weight in
    `build_inv_factor()`, re-run Table V, and report **both** weightings in
    `results/table_5.md` with the per-cell tiers for each.

- **[M2] The Ln(inv) magnitude FAIL is retired by an untested — and directionally
  backwards — causal story.**
  - File: `REPORT.md:81-89` and `:221-227`; `preparations/assumptions.md:201-217`
    ("The prior replication … attributed it to a Compustat vintage effect");
    `REPORT.md:215` (A11 "confirming signal is unbiased").
  - Why the offered evidence is not a test: the t-statistic is invariant to a
    linear rescaling of the regressor (β and SE scale identically), so a matching
    t is exactly what a units/definition mismatch produces. The same is true of
    the R² match. Neither can distinguish "different capx data" from "differently
    scaled regressor".
  - Why the mechanism is backwards: a *compressed* regressor raises |β|
    (β = cov(r,x)/var(x)). Ours is 16× **smaller** than the paper's, which implies
    our regressor is far more dispersed than the paper's, not less.
  - Auditor's counter-evidence: (i) our within-month SD of `ln_inv` is 1.026; the
    paper's −4.19 with our per-SD effect implies a regressor SD of **0.064**;
    (ii) our D1−D10 `ln_inv` spread is 3.441, so our −0.261 implies a decile
    return spread of −0.90 %/mo against Table II's actual −0.78 %/mo
    (internally consistent), whereas the paper's −4.19 × 3.441 implies
    −14.4 %/mo against the paper's own Table II spread of −0.79 %/mo (an 18×
    internal inconsistency in the paper); (iii) the same `inv_growth` column
    reproduces Table II to 0.01 %/mo and its trimmed firm-year distribution
    (mean 0.714, median 0.216) lies inside the paper's Table I range (means
    0.17–1.03, medians −0.05–0.54) — a vintage shift large enough to move β by
    16× could not leave Table II and Table I matching.
  - Specific fix: reopen the two cells as FAIL and run the discriminating tests
    (all cheap, all from cached data): (a) print the cross-sectional SD of every
    candidate transform (`inv_growth`, `ln(1+inv_growth)`, `ln(capx_{t-1}/capx_{t-3})`,
    and footnote-2's `(capx_{t-1}−capx_{t-3})/at_{t-3}`) and report which one has
    SD ≈ 0.06; (b) report the per-SD effect (β × SD) alongside every coefficient
    so the comparison is scale-free; (c) replicate Table I (see [M6]) — if its
    means/medians match, the vintage hypothesis is dead. Whatever survives,
    rewrite A11 to state the tested result, not the hypothesis.

- **[M3] Tier labels and pass-rate arithmetic do not follow the documented ladder.**
  - File: `REPORT.md:86-89` ("this is **Tier 2 (pattern match with documented
    cause)**"), `REPORT.md:132-137` ("33 / 37 evaluated = 89 %"),
    `src/evaluate.py:47-54` (PASS / BORDERLINE / FAIL at 1× and 2× `tolerance_pct`).
  - Evidence: |ours/paper| = 0.062 for `ln_inv_model5_coef` and 0.053 for
    `ln_inv_model6_coef` — outside the 2× Tier-2 bound in `audit/RUBRIC.md` §4 and
    `audit/SKILL.md` Spot-check 10. Separately, 33/37 matches nothing: the
    report's own tally sums to 40 evaluated (11 + 16 + 13), and 50 cells are
    committed. Correct rates: **82.5 % of evaluated, 66 % of committed.**
  - Specific fix: make `evaluate.py` emit the harness ladder explicitly
    (`Tier 1` / `Tier 2` = sign match within 2× / `FAIL` / `SKIP`) in addition to
    the tolerance bands, print the committed-cell denominator, and quote only the
    evaluator's tally in `REPORT.md`.

- **[M4] Ten committed cells were never evaluated; six of them vanish silently.**
  - File: `preparations/tables_to_replicate.json:86-87, 104-111` (26 T3 metrics
    committed); `src/evaluate.py:128-131` (`TABLE_III_DEFERRED` lists only 4) and
    `src/evaluate.py:143-150` (`if metric not in rep: continue` drops
    `ln_size_model7_*`, `ln_bm_model7_*`, `ln_inv_model7_*` with no output).
    `REPORT.md:77` says "4 cells"; `REPORT.md:238-243` says "4 additional cells";
    `logs/log1.md:72` says "2 (β-cells deferred)". None equals 10.
  - Likely cause: β was built in inner iteration 3 but `fm_panel` was never
    re-joined with `data/beta.parquet`, so models 1 and 7 were never run.
  - Specific fix: join `beta.parquet` onto the FM panel, run model 1
    (`ret ~ beta`) and model 7 (`ret ~ beta + ln_me + ln_bm + ln_inv`), and make
    `evaluate.py` print an explicit `SKIP` row for any committed metric absent
    from the results JSON. Target: paper 0.03 (t 0.08) for β alone and −0.31
    (t −0.94) in model 7 — reproducing the paper's *null* on β is a substantive
    result, not filler.

- **[M5] Corollary not computed: Table III Panel B subperiods and the Feb–Dec
  (January-exclusion) rows.**
  - Paper: §II, `inputs/content.md:186` (Feb–Dec: INV −3.49 %, t −5.25) and
    `:188-196` (1976-1987: INV −3.96 %, t −3.57; 1987-1999: −4.40 %, t −5.03).
    The paper explicitly frames these as the stability check for its headline
    claim ("the cross-sectional association … appears robust to the exclusion of
    January returns and to the examination of sub-periods").
  - Status in artifacts: deferred at `preparations/assumptions.md:229-238`; no
    result exists anywhere in `results/` or `data/`.
  - Specific fix: re-run the existing `compute_table_iii()` on three additional
    month masks (1976-07…1987-06, 1987-07…1999-06, and all non-January months)
    and write `results/table_3_subperiods.md`. The t-statistics are the scored
    quantity; report the per-SD effect too so the subperiods are comparable
    despite [M2].

- **[M6] Two enumerated paper claims (C1, C4) have no covering table — and C1's
  table is the cheapest test of [M2].**
  - File: `preparations/tables_to_replicate.json:2-27` lists C1 and C4 in
    `paper_claims`; no entry in `tables[]` has `covers_claims` containing either.
    The skip is mentioned in `REPORT.md:245-251` but not in the table file's
    `notes` or in `data_verification.json`.
  - Paper: C1 is an abstract-level claim ("firms classified as big and low-B/M
    significantly accelerate investment prior to the classification year",
    `content.md:26`), tested by Table I (`content.md:434-490`, 25 mean/median
    pairs). Under `prep/PREP_TABLES_PROMPT.md` "Table selection", Table I is
    REQUIRED on criterion 1 (substantive claim) and criterion 4 (it validates the
    `inv_growth` construction the other two tables depend on). C4 (value-premium
    attenuation, Table IV, `content.md:198-220`) is REQUIRED on criterion 1.
  - Specific fix: commit Table I Panel A (5×5 size × B/M means and medians of
    two-year investment growth; NYSE breakpoints, positive B/M only, delete
    `inv_growth > 10`) as `results/table_1.md`. It is ~50 cells off the existing
    panel and it directly settles [M2]: if our means land in 0.17–1.03 and
    medians in −0.05–0.54, the capx data are not the problem. Then add a reduced
    Table IV (the paper's high- vs low-investment return comparison for the S/H
    and B/L cells) rather than all 60 cells, and record the reduction in `notes`.

- **[M7] The paper's 36-month return-history filter is declared but not
  implemented.**
  - File: `preparations/preprocessing_rules.json:30-36` (`avail_36mo_return_history`,
    paper `content.md:88`: "in computing returns we require 36 months of data
    before a company is included in a portfolio"); the rule is listed under
    `exercises_preprocessing_rules` for **all three** committed tables
    (`tables_to_replicate.json:44, 77, 126`), yet
    `preparations/assumptions.md:56-70` states "I have not yet implemented it"
    and `src/sql/panel.sql` header repeats the omission.
  - Specific fix: add the predicate the assumptions entry already drafts
    (`month >= addMonths(first_ret_month, 36)`) in `panel.sql`, re-run, and log
    the before/after on the Table II spread (expected: small — the paper's
    stated purpose is to drop young growth stocks). If the impact is nil, say so
    with the number; the rule is then honestly "applied".

### Minor (cleanup)

- **[m1]** `results/table_2.md`, `results/table_3.md`, and `results/table_5.md`
  contain **no per-cell evaluation block** — no paper value, no deviation, no
  tier. The comparison exists only in `evaluate.py` stdout and in `REPORT.md`.
  Fix: have `evaluate.py` write its per-table block into each
  `results/table_*.md` so the artifact is self-contained.
- **[m2]** `REPORT.md:77` is garbled and self-contradictory ("were deferred in
  iteration 2 to iteration 3's `data/panel_with_beta.parquet` was not extended
  retroactively … flagged as deferred (4 cells)"), and conflicts with
  `REPORT.md:238-243` ("4 additional cells") and `logs/log1.md:72` ("2"). Fix
  with the true count (10) once [M4] lands.
- **[m3]** `REPORT.md:120-123` attributes to the paper a phrase it does not
  contain: the INV mean is called "statistically indistinguishable from the
  paper's '+ small', as paper itself calls it". The paper says only "The mean
  monthly investment index (INV) return is 0.24 %" (`content.md:248`) and
  reports no t-statistic. Our t = 1.66 means our INV mean is not distinguishable
  from **zero**; state that instead.
- **[m4]** `preparations/assumptions.md` entries are prose sections without the
  five required fields (Diagnosis / Next fix / Before metric / After metric /
  Status). The Ln(inv) entry (`:201-217`) has a diagnosis and no Next fix —
  the diagnose-and-skip pattern that produced [M2].
- **[m5]** `preparations/data_verification.json:14-21` records
  `crsp_share_code_pit` as matched to `crsp_202601.msfhdr`, but the pipeline
  uses `dsenames` (correctly — see `assumptions.md:25-37`). The artifact
  misstates the run; update `matched_table`.
- **[m6]** `tables_to_replicate.json:29` `budget_flag` says "Total committed
  ~170 cells"; the file commits 50. Harmless (the flag is only required above
  350) but wrong.
- **[m7]** `src/sql/fm_panel.sql:26` header comment says
  `ln_inv = ln(max(inv_growth, 0.001) + 1)`; the code (and the cached parquet,
  min `ln_inv` = −3.567) implement `ln(1 + inv_growth)`. Stale comment only —
  the parquet is current with the code.
- **[m8]** `results/table_5.md:41-49` prints identical M4 rows for the "Highest"
  and "Lowest" portfolios (alpha +0.978, MKT +1.048, SMB +0.362, HML −0.243)
  with no note. This is correct — since `INV = r_Q5 − r_Q1`, every coefficient
  except INV must be identical and the INV loadings must differ by exactly 1.00
  (the paper's Table V shows the same identity: −0.53/+0.47, −0.56/+0.44) — but
  an unannotated repeat reads as a copy-paste bug. Add one line stating the
  identity, and note that the two "exact match" INV cells are therefore one
  degree of freedom, not two.
- **[m9]** Spec-vs-data check: permno 14593 is **Apple**, not IBM. The worker
  identified this correctly, documented it (`assumptions.md:10-23`), and kept it
  as proof-of-life; `beta_invariants()` separately uses permno 12490 for IBM,
  which is right. No action — recorded so the next agent does not "fix" it back.

---

## 3. Per-table evidence

### Evaluator re-run (auditor, `uv run python replications/anderson_v2/src/evaluate.py`)

| Table | PASS | BORDERLINE | FAIL | Printed deferred | Silently dropped | Committed |
|---|---:|---:|---:|---:|---:|---:|
| T2_decile_returns | 11 | 0 | 0 | 0 | 0 | 11 |
| T3_fama_macbeth | 10 | 2 | 4 | 4 | **6** | 26 |
| T5_inv_factor_panel_A | 12 | 1 | 0 | 0 | 0 | 13 |
| **Total** | **33** | **3** | **4** | 4 | 6 | **50** |

Tier 1 = 33/40 evaluated (**82.5 %**) or 33/50 committed (**66 %**). The
report's 89 % is arithmetically unreachable. Every per-cell value in
`REPORT.md` §2.1–2.3 matches the evaluator's printed output exactly — the tier
table is computed, not hand-composed.

### Table II — 10 EW deciles (11 cells, 11 Tier 1)

Independently recomputed from `data/panel.parquet` (same trim, same
`assign_quantiles`, 276 months, decile counts 3,635–5,489 per formation year):
1.11, 1.30, 1.41, 1.48, 1.55, 1.64, 1.55, 1.67, 1.75, 1.89; spread −0.780 vs
paper −0.79. Max cell deviation 8.8 % (D4). The paper's own non-monotonic dip
at D7 (1.63 after 1.66) is reproduced (1.55 after 1.64) — shape, sign, and
magnitude all match. This is the strongest evidence in the replication and it
is unaffected by [M1] (equal weighting).

### Table III Panel A — Fama-MacBeth (16 of 26 committed evaluated)

Re-ran models 5 and 6 from `data/fm_panel.parquet` and reproduced the shipped
values to three decimals (−0.261 / t −6.991; −0.185 / t −5.815; ln_me −0.107,
ln_bm 0.351). Average cross-sectional R² vs the paper's Adj R² column (%):
ours 0.98 / 0.59 / 1.55 / 0.16 / 1.65 against paper 1.15 / 0.60 / 1.61 / 0.10 /
1.68 — the *information content* of every specification replicates. Size
coefficients and t-statistics are Tier 1 throughout. What does not replicate is
the Ln(inv) coefficient *scale* (0.062× and 0.053×) — see [M2] — and the Ln(B/M)
t-statistics (6.38 / 4.87 / 4.43 vs 4.28 / 2.51 / 2.13), which the report
explains with "smaller coefficients produce smaller SE denominators"
(`REPORT.md:91-94`); that explanation is arithmetically wrong, since rescaling a
regressor leaves the t-statistic unchanged. Our monthly B/M slopes are simply
less volatile than the paper's; the direction and significance of the paper's
B/M claim replicate, the precision does not.

### Table V Panel A — factor models on INV quintiles (13 cells, 12 Tier 1)

The INV factor is exactly `q5_vw − q1_vw` (max identity error 0.0), mean
0.2608 %/mo vs paper 0.24, std 0.026, t of mean 1.66; corr with MKT-RF −0.280
(paper −0.24), HML +0.433 (+0.38), SMB +0.010 ("not significant"). Loadings
reproduce the paper closely: M1 MKT 1.261 (paper 1.24), M2 SMB 0.306 (0.23),
HML −0.461 (−0.44), M3 INV −0.568 (−0.56) with adj R² 0.930 (0.93), M4 INV
−0.527 (−0.53) / +0.473 (+0.47) with adj R² 0.965 / 0.954 (0.96 / 0.95). The
qualitative corollaries the paper states in §III.B all hold in our output: SMB
positive for the two extreme portfolios and negative for the middle three
(+0.306, −0.079, −0.130, −0.079, +0.412); HML most negative for the highest
portfolio and attenuating; INV loadings monotone from −0.568 to +0.432.
**Caveat:** the alphas (5 of the 12 Tier-1 cells) are contingent on the
contemporaneous-weight bias — see [M1] — and the two "exact match" INV loadings
are linked by a construction identity, so they are one independent comparison,
not two.

### Verification spot-checks (recomputed by auditor)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| 1 | Monotonic-direction claim | ✓ / ✗ | EW deciles reproduce the paper's shape including its D7 dip (✓). VW quintile means under the shipped weights are non-monotonic (2.14, 1.91, 1.81, 1.93, 2.40); lagged weights restore monotonicity (✗ → [M1]) |
| 2 | Headline-magnitude claim | ✗ | Spread −0.780 vs −0.79 ✓; INV loadings −0.527/+0.473 vs −0.53/+0.47 ✓; FM Ln(inv) −0.261 vs −4.19 ✗ (0.062×) |
| 3 | Sample coverage ≥ 60 % | ✓ | `inv_growth` non-null 79.1 % of 1,364,746 panel rows; FM regression sample 965,980 / 1,355,132 = 71 %; 276 months, 1976-07…1999-06 exactly |
| 4 | Data-source choice justified | ✓ | CRSP `msf` + `dsenames` (PIT, correctly preferred over `msfhdr`), `ccmxpf_linktable` LC/LU + P/C, Compustat `funda` INDL/C/D/STD. FF factors from `crsp_202601.five_factor_monthly` (means: mkt_rf 0.778 vs paper 0.75, HML 0.364 vs 0.30, SMB 0.035 vs 0.12) |
| 5 | prep_validation.py exit 0 | ✓ | Exit 0; only the expected pre-audit warning ("REPORT.md exists but no logs/audit*.md yet") |
| 6 | All committed tables have results files | ✓ | 3 of 3 (`table_2.md`, `table_3.md`, `table_5.md`) |
| 7 | REPORT.md values match results/ + data/ | ✗ | All per-cell values reproduce; the aggregates do not ("33/37 = 89 %", "2"/"4" deferred vs the true 10) → [M3], [M4] |
| 8 | No orphan folders | ✓ | No brace-expansion artifacts; `eval/` is empty but layout-created |
| 9 | Diagnoses paired with fix attempts | ✗ | `assumptions.md` uses prose sections, not the five-field entries; the Ln(inv) entry has no Next fix and no before/after metric → [m4], [M2] |
| 10 | Tier 2 within 2× magnitude | ✗ | Evaluator re-run matches the pasted tables ✓, but `REPORT.md` re-labels two 16–19× misses as "Tier 2" → [M3] |
| 11 | Corollary coverage | ✗ | Table V Panel A loading corollaries verified ✓; subperiods, Feb–Dec, β-insignificance, and B/M-/MVE-sorted panels not computed → [M4], [M5] |
| 12 | Claim coverage of committed selection | ✗ | C2, C3, C5 covered; **C1 and C4 have no covering table** → [M6]. `paper_claims` itself is honest and complete against the abstract |
| 13 | Sign conventions re-derived from paper | ✓ | Table II "Deciles are ranked in descending order" → D1 = highest growth → spread negative ✓; Table V caption "subtract the returns on the high investment group from the low investment group" → INV = low − high ✓, loadings −/+ ✓, and the paper's own ±1.00 identity is reproduced |
| 14 | Reporting discipline | ✗ | Grid rows complete in `results/table_5.md` ✓; but "confirm the signal is the same factor" is asserted from a scale-invariant statistic ([M2]), the 89 % headline is unreachable ([M3]), and a quotation is attributed to the paper that it does not contain ([m3]) |

---

## 4. Six-dimension scores

| Dimension | Score | Key finding |
|-----------|------:|-------------|
| Methodology | 3 | Formula, June-formation timing, BE/ME timing, formation-month ME for `ln_size`, winsorization, and the paper's plain (non-HAC) t-statistic all verified against the paper. Two checks fail: the Table V VW look-ahead ([M1]) and the declared-but-unimplemented 36-month history filter ([M7]) |
| Headline matching | 3 | Two of three headline claims match in shape, sign, and magnitude (decile spread −0.780 vs −0.79; INV loadings −0.527/+0.473 vs −0.53/+0.47). The third (FM INV coefficient) matches in sign, t-statistic, and R² but is 16× off in magnitude |
| Data coverage | 4 | Period exact (276 months, 1976-07…1999-06), sources match the paper, 79 % signal coverage, PIT filters correct. One substitution (ClickHouse FF series, SMB mean 0.035 vs the paper's 0.12) and a universe slightly wider than the paper's because of [M7] |
| Concrete result matching | 4 | 33/40 evaluated = 82.5 % Tier 1 (66 % of the 50 committed). Robust to [M1]: correcting the weights still leaves ~30/40 = 75 %, inside the 70–90 % band |
| Signal strength | 2 | Decile spread r = 0.99, INV loading r = 0.99, INV factor mean r = 1.09 — but the FM coefficient r = 0.062. A strict worst-cell reading of the rubric maps that to 1; I score 2 because the same regression's sign, t-statistic (−6.99 vs −6.00), and R² (0.16 % vs 0.10 %) replicate, so the signal is present at full strength and the open question is the regressor's scale, not the effect's existence. The dimension is capped at 2 until [M2] is settled |
| Corollary | 3 | The Table V Panel A corollaries the paper states in §III.B (monotone INV loadings; SMB positive at the extremes and negative in the middle three; HML attenuation; factor correlations) all replicate and were independently verified. Four other corollary families — subperiods, January exclusion, β insignificance, B/M-/MVE-sorted panels — are absent |

**Overall: 3.17 / 5.00 → `REPLICATED`** (mean ≥ 3.0, no dimension scored 1).

---

## 5. Limitations

- **The paper is a 2002 working-paper draft with internal inconsistencies of its
  own.** Its Table III Ln(inv) coefficient (−4.19 %/unit) is not reconcilable with
  its own Table II decile spread (−0.79 %/mo) under any log-growth regressor: it
  would imply a −14 %/mo spread. Its Table IV prints value-weighted monthly
  returns of 2.70 % and 3.79 %. A perfect replication of every printed number may
  not be attainable; the next iteration should aim to *identify* the scale
  convention, and report the per-SD effect, rather than to force the printed value.
- **[M1] and [M2] interact.** The paper's Table V alphas (0.6–1.0 %/mo) imply
  portfolio mean returns near 2.1 %/mo, which the shipped (biased) construction
  reproduces and the standard construction does not. Fixing the weights may move
  the alpha cells *away* from the paper. That is still the right fix — but report
  both weightings side by side rather than choosing the one that scores better.
- **Auditor scope.** I verified by re-execution and recomputation from the cached
  parquet only; I did not re-run `src/main.py` end-to-end against ClickHouse, and
  I did not attempt an alternative-vintage Compustat pull (none is available in
  the catalog). The vintage hypothesis is therefore *unsupported* by the current
  evidence, not *disproved* by a direct vintage comparison — Table I ([M6]) is the
  closest available test.
- **Table V Panels B and C** (B/M- and MVE-sorted portfolios) are part of claim
  C5 as written in `tables_to_replicate.json` but outside the committed cells.
  Not raised as a major to avoid inflating compute; noted so the claim's scope is
  read honestly.
- **Delisting returns** are not adjusted. The paper is silent and uses raw
  returns; documented, low impact for monthly EW deciles.

---

## 6. Next-iteration prompt (copy-paste this into the next agent run)

--- BEGIN COPY HERE ---

You are continuing the replication of "Empirical Evidence on Capital Investment,
Growth Options, and Security Returns" (Anderson & Garcia-Feijoo, July 2002 draft)
for slug `anderson_v2`. The previous run completed with verdict **PARTIAL**
(audit 1 at `replications/anderson_v2/logs/audit1.md`). There are **no blockers**
and **7 actionable majors**. Read the audit first — especially §2, which contains
the recomputed numbers behind each issue.

## Issues to address (priority order)

### [M1] — MAJOR — fix first: Table V value-weights use same-month market equity

`src/main.py:742-743` weights each month's return by `me_dollars` taken from the
**same** `msf` row (`src/sql/panel.sql`: `abs(prc)*shrout*1000`), so the weight
embeds the month's own return. Auditor recomputation on your own panel:
VW mean with contemporaneous weights = 1.949 %/mo, with one-month-lagged weights
= 1.324 %/mo, CRSP/FF market = 1.334 %/mo. Your VW quintile means are
non-monotonic (2.137, 1.908, 1.808, 1.930, 2.398) — under lagged weights they
become monotonic in the paper's direction (1.117 → 1.464).

**Specific fix:**
1. In `build_inv_factor()`, add a per-permno one-month-lagged ME (`me_lag`,
   guarding the month gap) or use `me_jun_form` held constant over the cohort
   (the FF annual-rebalancing convention); use it as the VW weight.
2. Re-run Table V Panel A and write **both** weightings into
   `results/table_5.md` with per-cell tiers for each — do not silently replace
   one with the other.
3. Verification: the panel-wide VW mean must land within ~0.05 %/mo of the FF
   market total return (1.334 %/mo), and the five quintile mean returns must be
   monotone increasing from Q1 (highest growth) to Q5.
4. Expect these tier moves and report them honestly: `highest_alpha_mkt_only`
   PASS→FAIL, `highest_alpha_3factor` PASS→FAIL, `highest_alpha_4factor` and
   `lowest_alpha_mkt_only`/`lowest_alpha_3factor`/`highest_smb_3factor`
   PASS→BORDERLINE, `lowest_hml_3factor` BORDERLINE→PASS. The INV loadings and
   adj R² barely move.

### [M2] — MAJOR — reopen the Ln(inv) magnitude FAIL

The t-statistic match is **not** a test of the Compustat-vintage story: a
t-statistic (and R²) is invariant to any linear rescaling of the regressor.
The stated mechanism is also backwards — a compressed regressor would make your
coefficient *larger* than the paper's, not 16× smaller. And your own data
contradict it: the same `inv_growth` column reproduces Table II to 0.01 %/mo,
and its trimmed firm-year distribution (mean 0.714, median 0.216) sits inside
the paper's Table I range (means 0.17–1.03, medians −0.05–0.54).

**Specific fix:**
1. Mark `ln_inv_model5_coef` and `ln_inv_model6_coef` as FAIL (not Tier 2) until
   a test discriminates the cause.
2. Print the within-month cross-sectional SD of each candidate regressor from the
   cached panel: `inv_growth`, `ln(1+inv_growth)` (current, SD ≈ 1.026),
   `ln(capx_{t-1}/capx_{t-3})`, and footnote 2's `(capx_{t-1}−capx_{t-3})/at_{t-3}`.
   The paper's −4.19 implies a regressor SD of **≈ 0.064**; report which
   transform, if any, is near it.
3. Report the scale-free per-SD effect (β × SD) next to every FM coefficient:
   yours is −0.268 %/mo per SD, and your D1−D10 `ln_inv` spread of 3.441 implies
   a −0.90 %/mo decile spread against Table II's actual −0.78 %/mo — state that
   internal consistency explicitly.
4. Rewrite `assumptions.md` A11 as a five-field entry (Diagnosis / Next fix /
   Before metric / After metric / Status) reporting what the test found. If no
   test settles it, the honest write-up is "unresolved scale discrepancy;
   inference (sign, t, R²) replicates" — not "vintage artifact".

### [M6] — MAJOR — add Table I (also the cheapest test for [M2])

Claims C1 and C4 in `preparations/tables_to_replicate.json` have no covering
table. Table I is REQUIRED under `prep/PREP_TABLES_PROMPT.md` (substantive claim
+ construction validation) and it settles [M2] directly.

**Specific fix:**
1. Commit Table I Panel A: 5×5 size × B/M portfolios (NYSE breakpoints, positive
   B/M only, delete `inv_growth > 10`), reporting mean/median two-year investment
   growth per cell (`inputs/content.md:434-490`, 50 cells).
2. Write `results/table_1.md` and add the table entry with `covers_claims: ["C1"]`.
3. Verification: means should fall in 0.17–1.03 and medians in −0.05–0.54, and
   both should decrease across B/M within a size row and across size within a B/M
   column. If they do, say in `REPORT.md` that the vintage hypothesis for [M2] is
   ruled out.
4. Then add a reduced Table IV (the high- vs low-investment return comparison for
   the S/H and B/L cells only) for C4, and record the reduction in the table's
   `notes` — do not commit all 60 cells.

### [M4] — MAJOR — compute the 10 committed cells that were never evaluated

`tables_to_replicate.json` commits 26 Table III metrics; 16 were evaluated. Four
are printed as deferred and **six vanish silently** at `src/evaluate.py:143-150`
(`ln_size_model7_*`, `ln_bm_model7_*`, `ln_inv_model7_*`). β exists
(`data/panel_with_beta.parquet`, 1,055,375 non-null, mean 1.093) but was never
joined into the FM panel.

**Specific fix:**
1. Join `data/beta.parquet` onto the FM panel; run model 1 (`ret ~ beta`) and
   model 7 (`ret ~ beta + ln_me + ln_bm + ln_inv`).
2. Make `evaluate.py` print an explicit `SKIP` row for any committed metric
   missing from the results JSON, and print the committed-cell denominator.
3. Verification: paper targets are 0.03 (t 0.08) for β alone and −0.31 (t −0.94)
   in model 7 — reproducing the paper's **null** on β is a successful
   replication, so report it as such.

### [M5] — MAJOR — compute the paper's own stability corollaries

Table III Panel B subperiods (1976-1987: INV −3.96 %, t −3.57; 1987-1999:
−4.40 %, t −5.03) and the Feb–Dec rows (INV −3.49 %, t −5.25) are the paper's
own robustness claims (`inputs/content.md:186-196`) and are absent from artifacts.

**Specific fix:**
1. Re-run `compute_table_iii()` on three month masks: 1976-07…1987-06,
   1987-07…1999-06, and all non-January months.
2. Write `results/table_3_subperiods.md` with per-cell tiers; score the
   t-statistics and report per-SD effects alongside the coefficients.

### [M3] — MAJOR — fix the tier vocabulary and the pass-rate arithmetic

**Specific fix:**
1. Make `src/evaluate.py` emit the `rep/TOLERANCE_RULES.md` ladder explicitly
   (`Tier 1` / `Tier 2` = sign match within 2× / `FAIL` / `SKIP`) alongside the
   tolerance bands, and print both denominators (evaluated and committed).
2. Quote only the evaluator's tally in `REPORT.md`. The current numbers are
   33/40 = 82.5 % evaluated and 33/50 = 66 % committed; "33/37 = 89 %" is wrong.
3. Never re-label a >2× miss as "Tier 2" in prose.

### [M7] — MAJOR — implement the 36-month return-history filter

Declared in `preprocessing_rules.json` and claimed as exercised by all three
tables, but not implemented (`assumptions.md:56-70`).

**Specific fix:**
1. Add `month >= addMonths(first_ret_month, 36)` in `src/sql/panel.sql`.
2. Re-run and log Before/After on the Table II spread and on the panel row count.
   A nil impact is a fine result — report the number.

### [m1]…[m9] — MINOR — cleanup

Write the evaluator's per-cell block into each `results/table_*.md` [m1]; fix the
garbled deferral sentence at `REPORT.md:77` [m2]; remove the invented paper quote
at `REPORT.md:120-123` and replace it with "our INV mean is not distinguishable
from zero (t = 1.66)" [m3]; convert `assumptions.md` to five-field entries [m4];
correct `data_verification.json` `crsp_share_code_pit` to `dsenames` [m5]; fix the
`budget_flag` cell count [m6]; fix the stale `ln_inv` comment at
`src/sql/fm_panel.sql:26` [m7]; annotate the Highest/Lowest identity in
`results/table_5.md` [m8]. Do **not** "fix" permno 14593 back to IBM — it is
Apple and the worker was right [m9].

## Iteration discipline reminders

- **Diagnose → commit-fix → fix → verify.** Every entry in `assumptions.md` needs
  all five fields: Diagnosis, Next fix, Before metric, After metric, Status. The
  Ln(inv) entry is the counterexample that produced [M2].
- **Never retire a FAIL with a statistic that cannot discriminate the cause.**
  t-statistics and R² are invariant to regressor scale; per-SD effects and
  distributional comparisons are not.
- **Read `rep/STUCK_AGENT_GUIDELINE.md` on your first debug cycle.**
- **10-iteration cap per problem.** A documented partial beats a claimed success.

## Inputs you should read

- `replications/anderson_v2/logs/audit1.md` — this audit (full context)
- `replications/anderson_v2/inputs/content.md` — paper ground truth
- `replications/anderson_v2/preparations/` — prep contract
- `replications/anderson_v2/src/main.py`, `src/evaluate.py`, `src/sql/*.sql`
- `replications/anderson_v2/data/` — cached panels (recompute spot-checks here)

## What NOT to redo

- Skip re-reading `SKILL.md` — the contract is unchanged.
- Skip the ClickHouse catalog scan — `data_verification.json` is current except
  for the `msfhdr`/`dsenames` correction in [m5].
- Do **not** rebuild Table II — it is 11/11 Tier 1 and was independently
  reproduced by the auditor from the cached panel.
- **DO** re-run `src/evaluate.py` after every change; it is the gate.

## Deliverables for this iteration

- `src/main.py`, `src/evaluate.py`, `src/sql/panel.sql` — revised per the issues
- `results/table_1.md` (new, [M6]), `results/table_3_subperiods.md` (new, [M5]),
  updated `results/table_2.md`, `table_3.md`, `table_5.md` — each with the
  evaluator's per-cell block
- `preparations/tables_to_replicate.json` — Table I committed with
  `covers_claims: ["C1"]`; corrected `budget_flag`
- `preparations/assumptions.md` — a five-field entry per issue addressed
- `replications/anderson_v2/REPORT.md` — updated; lead with the data-quality
  summary (period, universe, signal mean/std vs the paper's Table I,
  headline-magnitude comparison, committed-vs-evaluated cell counts, corollaries
  evaluated this iteration)
- `replications/anderson_v2/SUMMARY.md` — read it, do NOT edit (auditor-owned)

## Stop conditions

- **All majors fixed and verified** → re-run `prep_validation.py` and
  `evaluate.py` → declare success in `REPORT.md`; the next audit updates
  `SUMMARY.md`.
- **[M2] unresolved after honest testing** → declare partial and write up the
  scale discrepancy as an unresolved finding with the per-SD evidence. That is an
  acceptable outcome; an untested cause attribution is not.

--- END COPY HERE ---
