# Assumptions Registry — Piotroski (2000) "Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers"

Paper-silent decisions and documented deviations. Paper-derived rules live in `preprocessing_rules.json`; this registry holds choices the paper does not specify (or where the data forces a deviation), each with rationale and impact.

---

# Assumption 1: Sample restricted to formation years 1988-1996 (FY1987-FY1995) — user-approved deviation

**Decision:** Restrict the sample to fiscal years 1987-1995 (portfolio formation years 1988-1996), instead of the paper's FY1975-FY1995 (1976-1996).

**Rationale:** The paper is silent on data vintage. In the 2026 Compustat vintage (`comp_202601.funda`), `oancf` (operating cash flow, item 308) is NULL for **every** firm-year with fyear < 1987 (verified: 0 non-null rows in FY1974-FY1986; 1,312 in FY1987; ~6,500-9,700 per year FY1988-FY1996). Two of the nine F_SCORE signals (`F_CFO`, `F_ACCRUAL`) require cash flow from operations, so the paper's F_SCORE cannot be computed as defined for FY<1987 without a proxy. Considered alternatives: (a) cascading fallback oancf → fopt → ib+dp (emulates the historical vintage but substitutes a differently-defined measure for 42% of sample years, silently changing signal definitions); (b) ib+dp proxy (simple but ignores working-capital changes in pre-1988 accruals); (c) restrict to FY1987+ (loses the early years but keeps every signal exactly as the paper defines it). The user chose (c): methodological exactness over sample-span coverage. Piotroski's 1990s Compustat tape contained partial pre-1988 cash-flow backfills from funds-flow statements, which no longer exist in current vintages — a known external data limitation.

**Impact:** The sample shrinks from 14,043 to an expected ~7,000-7,200 firm-years (the paper's Appendix A reports 7,205 observations across calendar years 1988-1996). All full-sample counts (14,043; per-score n's 57/339/.../333; size-partition n's 8,302/3,906/1,835) become structurally unmatchable at Tier 1 — they are retained as Tier-2 references, with sign/magnitude/pattern as the pass criteria. Full-period means (e.g., High-Low spread 0.230 over 1976-1996) are compared against our 1988-1996 estimate on magnitude and significance, not exact value. The restriction is *documented, not hidden*: every table's `notes` field and REPORT.md carry this caveat. The FY1987 cohort's BM quintile assignment uses FY1986 cutoffs (BM requires no cash-flow data), so the prior-year-cutoff machinery is unaffected.

---

# Assumption 2: Equity-issuance detection via Compustat `sstk` (sale of common & preferred stock)

**Decision:** `EQ_OFFER = 1` (good signal: no issuance) when `sstk` is missing or zero in the fiscal year preceding formation; `EQ_OFFER = 0` when `sstk > 0`.

**Rationale:** The paper defines the signal as "the firm did not issue common equity in the year preceding portfolio formation" (L240) and footnote 16 (L2745) states offerings "were identified through the firm's statement of cash flows or statement of sources and uses of funds (through Compustat)". The exact Compustat item is paper-silent. `sstk` (sale of common and preferred stock) is the cash-flow-statement equity-issuance item and is the standard choice in the F-score replication literature. Considered alternative: increase in shares outstanding (`csho`) — noisier (captures stock splits via rounding, buybacks netting against issuance) and not a cash-flow item, contradicting footnote 16. Missing `sstk` is treated as no issuance (Compustat convention: the item is omitted when zero/not applicable for older statements).

**Impact:** Affects the `EQ_OFFER` binary for every firm-year (one of nine signals) and the EQ_OFFER regressor in Table 7 (where it enters with the opposite sign: 1 = issued). `sstk` coverage is strong (5,700-10,200 non-null per year FY1975-FY1996 under the standard filter); the corr(F_SCORE, EQ_OFFER) = 0.366 target in Table 2 validates the resulting signal distribution.

---

# Assumption 3: Book equity construction (Compustat BE with standard fallbacks)

**Decision:** BE = `ceq + txdb - pstkrv`; if unavailable, `ceq`; if unavailable, `seq - ps`; if unavailable, `at - lt - pstkrv` (equivalently `at - dlc - dltt - ... `). Require BE > 0 and ME > 0; firm-years with non-positive book equity are dropped from BM formation (negative-BE firms are economically distressed beyond the value universe and are excluded by standard convention, Fama-French 1992).

**Rationale:** The paper says only "book value of equity at the end of fiscal year t, scaled by MVE" (L540) without specifying the Compustat recipe. The FF (1992)/Ken French library recipe (ceq + txdb - pstkrv with fallbacks) is the field standard for exactly this era and data. Considered alternative: `seq` alone (stockholders' equity) — ignores deferred taxes and preferred stock, systematically shifting BM levels; rejected.

**Impact:** Affects BM levels (Table 1 BM mean 2.444 / median 1.721 are validation targets), the high-BM quintile membership, and every downstream table. The BM median (robust to the recipe's tail effects) is the primary recipe check.

---

# Assumption 4: ΔTURN denominator — average total assets (Table 1 footnote j) over beginning-of-year assets (text)

**Decision:** Asset turnover = `sale / ((at_t + at_{t-1})/2)` per Table 1 footnote j (L554: "net sales scaled by average total assets for the year"), not `sale / at_{t-1}` per the §2.3.3 text (L246: "total sales scaled by beginning-of-the-year total assets").

**Rationale:** The paper contradicts itself between text and the formal variable-definition footnotes. The footnote table is the paper's formal definition apparatus and is internally consistent with ΔLEVER's average-assets denominator (L216, L552, both text and footnote agree on average assets for leverage). Table 1's reported ΔTURN statistics (mean 0.0119, median 0.0068, std 0.5851, proportion positive 0.534) are the discriminator: both definitions will be computed and the one matching Table 1 is adopted. The binary signal F_DTURN is largely insensitive to the denominator choice (the sign of the change rarely flips).

**Impact:** Affects F_DTURN for a small fraction of borderline firm-years; validated against Table 1 ΔTURN column.

**Post-test (iteration 3 diagnosis):** the Table 1 ΔTURN mean FAILED (ours −0.022 vs paper +0.0119, sign flip), triggering a committed test of the alternative definition. On FY1987-1995 funda (61,457 firm-years with t/t-1/t-2 data): average-assets ΔTURN → mean −0.0011, std 0.473, proportion positive 0.502; beginning-assets ΔTURN → mean −0.0843, **std 6.238** (extreme ratios when lagged assets are small), proportion 0.494. Paper targets: mean +0.0119, std 0.5851, proportion 0.534. The beginning-assets variant is decisively worse (std 10× the paper's); the average-assets variant matches the paper's dispersion and signal proportion closely, with only the tail-driven mean differing by 0.034 in absolute terms. Decision confirmed: keep average assets. The mean-sign FAIL is recorded as residual vintage drift (high-BM subsample) of a tail-dominated statistic, not a methodology error — no further fix to attempt.

---

# Assumption 5: Missing `dlc` treated as zero

**Decision:** When Compustat `dlc` (debt in current liabilities) is missing, treat it as 0 in the leverage ratio `(dltt + dlc) / avg(at)`.

**Rationale:** Standard Compustat convention: `dlc` is left blank when the firm has no current portion of long-term debt or the item was not collected. ΔLEVER's footnote (L552) requires "total long-term debt (including the portion of long-term debt classified as current)" — zero is the conservative reading of "not reported". Dropping the firm-year instead would lose firms with no current LTD, biasing the sample toward levered firms.

**Impact:** Small downward bias in leverage levels for firms with missing dlc; ΔLEVER (a *change*) is affected only when dlc reporting status changes between years. Validated against Table 1 ΔLEVER column (mean 0.0024, proportion positive signal 0.498).

---

# Assumption 6: CRSP value-weighted index (`msi.vwretd`) as the market proxy for market adjustment

**Decision:** Market buy-and-hold return = compound of CRSP value-weighted daily/total-market index returns (`crsp_202601.msi.vwretd`) over each firm's exact 12/24-month window.

**Rationale:** The paper says "the value-weighted market return over the corresponding time period" (L314, L560) without naming the index. The CRSP NYSE+AMEX(+NASDAQ from 1973) value-weighted index with dividends is the universal market proxy for this literature and era; it is also what FF's Mkt-RF is built from. Considered alternative: FF Mkt-RF + RF compounded — equivalent up to the T-bill rate addition, and less precise for firm-specific non-calendar windows; rejected.

**Impact:** Affects every market-adjusted return cell (Tables 1-4, 7, Appendix A). The paper's one-year market-adjusted "All Firms" mean (0.059) is the headline validation target for this choice.

---

# Assumption 7: No winsorization or trimming anywhere

**Decision:** Apply no winsorization to signals, ratios, or returns.

**Rationale:** Paper silent (no mention anywhere in §2-3). The binary-signal design immunizes F_SCORE against outliers; Table 1's reported dispersion (BM std 34.66, ΔMARGIN std 1.9306, ASSETS std 6,653) is consistent with un-winsorized data — winsorization would compress these dramatically. Documented as preprocessing rule `winsorize_none_paper_silent`.

**Impact:** Table 1 MEANS of skewed variables (MVE, ASSETS, BM) are sensitive to this choice — their match (or mismatch pattern) validates the decision. Medians and signal proportions are robust checks.

---

# Assumption 8: CRSP-Compustat link — primary + Compustat-confirmed secondary links

**Decision:** Join funda to CRSP via `ccmxpf_linktable` with `linkprim IN ('P','C') AND linktype IN ('LC','LU') AND usedflag = 1`, temporal validity at the fiscal year-end datadate (`linkdt <= datadate AND (linkenddt >= datadate OR linkenddt IS NULL)`), one permno per gvkey-fyear (argMax by linkdt, primary links beating secondaries on ties).

**Rationale:** Iteration-1 used primary links only (`linkprim='P'`), which linked just 66.9% of funda FY1987-1995 firm-years (verified). The data manual's standard FF filter (references/COMPUSTAT.md § CCM) is `linkprim IN ('P','C')`, which links 88.5% — a +21.6pp recovery of ~1,600 high-BM firm-years. 'C' links are Compustat-confirmed (not heuristic 'J' join-only links), so the match quality is comparable to 'P'. The paper is silent on link methodology (it predates the CCM linktable; the original study matched via CUSIP). usedflag=1 retained (dropping it does not change coverage, verified). Considered alternative: any link type (92.3%) — rejected; inactive/unconfirmed link forms (LX/LD/LS/LR, 'J') are known to mis-match.

**Impact:** Panel grows from 3,957 to ~5,500 firm-years (iteration 2). The recovered firms are predominantly smaller names whose Compustat-CRSP mapping was confirmed but not flagged primary; they are precisely the neglected small high-BM firms where the paper finds the strongest F_SCORE effect, so the High-Low spread is expected to move toward the paper's 0.230. Signal definitions and BM/size cutoffs are untouched (computed pre-link).

---

# Iteration 2 Log — audit1 follow-up (outer iteration 2)

Audit 1 (`logs/audit1.md`) returned PARTIAL with two actionable majors (Table 5
price/volume partitions never computed; analyst-coverage feasibility unchecked)
plus three minor documentation fixes. Entries below use the five-field iteration
format (Diagnosis / Next fix / Before metric / After metric / Status). The frozen
pipeline (`src/main.py` steps 1-10, `data/panel.parquet` 5,736×43) was NOT
touched; all new work is additional read-only queries + pandas joins in the
table-generation section (idempotent, re-runnable).

---

## I2-M1: Table 5 share-price / trading-volume partitions (MAJOR — closed)

**Diagnosis:** Table 5's price/volume partitions — an abstract-level claim
("not dependent on purchasing firms with low share prices", content.md L58,
§4.4.1 L2293-2337) — were silently dropped at prep: `candidate_assessment.json`
declared Tables 1-8 "all quantitative and reproducible", yet
`tables_to_replicate.json` committed to only six tables, and no `results/table_5.md`
existed. The partition needs no data beyond what the pipeline already uses
(`prcc_f` in the funda base; `vol`/`shrout` verified present in `crsp_202601.msf`).

**Next fix:** Added `src/sql/price_volume_cutoffs.sql` (prior-year full-Compustat
PRICE terciles over `prcc_f > 0`, self-contained like `bm_size_cutoffs.sql`) and
`src/sql/firm_turnover.sql` (fiscal-year share turnover = `sum(vol)*100 /
avg(shrout*1000)` over the 12 month-ends ending at the FY-end). In
`generate_tables`, the linked ME>0 universe FY1986-1995 is staged, turnover and
prior-year volume terciles computed over it (the MOMENT/ACCRUAL-decile
population), and the FROZEN panel is assigned `price_bucket`/`volume_bucket` with
the t−1 cutoffs (no rebuild). Wrote `results/table_5.md` with per-cell tiers
against the 24-metric table_5 contract. **Unit check (Rule 10):** CRSP `vol` is
in HUNDREDS of shares in this vintage (FY1990 Dec-FYE linked firms: median
turnover 0.37 with ×100 vs 0.004 without; 0.004 = 0.4%/yr is implausibly low).
The ×100 is a firm-invariant constant, so tercile ASSIGNMENT (all Panel B uses)
is identical with or without it; it is applied for economic meaning.

**Before metric:** table absent — 0 of 24 table_5 contract metrics evaluated;
no `results/table_5.md`.

**After metric:** 19 Panel A+B cells evaluated = **12 Tier 1, 5 Tier 2, 2 FAIL**
(+5 Panel-C SKIP, see I2-M2). Bucket shares ours vs paper (of 14,043): price
small/medium/large 56.3/30.1/13.5% (paper 51.6/32.0/16.4%); volume
low/medium/high 45.5/33.8/20.6% (paper 54.6/26.1/19.4%). High−Low spreads (ours
vs paper, Welch t): price +0.159 (1.59) / +0.041 (0.41) / +0.155 (0.85) vs
0.246 (4.533) / 0.258 (3.573) / 0.132 (1.852); volume +0.233 (2.44) / +0.092
(0.63) / −0.039 (−0.30) vs 0.239 (4.417) / 0.175 (2.050) / 0.203 (2.863).
**Qualitative claim "positive in all six buckets" = FAIL** (5 of 6: 3/3 price,
2/3 volume) — the high-volume bucket's spread collapses to ≈0 and flips sign.
The low-volume bucket replicates the paper's 0.239 almost exactly (+0.233,
Tier 1), and the large-price High−Low (+0.155) even slightly exceeds the paper's
0.132 (Tier 1). The 2 FAILs are both the high-volume bucket (mean + t sign flip).

**Status:** RESOLVED (major closed — table added and contracted). The high-volume
FAIL and the attenuated t-statistics are A1-structural (the restricted sub-period
thins the most-traded bucket to n=1,183 with a slightly-positive Low group, leaving
no left tail for F_SCORE to screen; magnitudes attenuate exactly like the headline
spread). Paper values are full-period references; cells read on sign + magnitude
plausibility, counts Tier 2 (A1 gap), per the contract `notes`.

---

## I2-M2: Table 5 Panel C analyst-coverage feasibility (MAJOR — SKIP, data gap)

**Diagnosis:** The analyst-coverage corollary (content.md L2550: no-coverage
High−Low 0.277 vs coverage 0.114; 37.8% of 14,043 covered, 1999 I/B/E/S tape) was
implicitly treated as out of scope — `data_verification.json` had no IBES
requirement — yet the ClickHouse catalog contains `ibes_202601.statsum_epsus`
(I/B/E/S summary statistics, EPS measure, `numest` = # forecasts, `statpers` =
statistical-period date), covering 1976-01-15 → 2025-12-18, so the 1986-1995
panel window is present. Feasibility had never been checked.

**Next fix:** Queried coverage: mapped panel `gvkey → (tic, cusip)`
(`comp_202601.funda`, argMax-by-datadate, standard filter) and joined to
`ibes_202601.statsum_epsus` on **8-digit CUSIP** (Compustat's 9-digit CUSIP drops
the check digit; I/B/E/S stores 8) **∪ ticker**. "Classifiable" = a statistical-
period record within the 12 months ending at the FY-end `datadate`; "covered" =
`numest ≥ 1` at the last such record. Two implementation traps were found and
fixed while building this: (a) an `ON (cusip OR ticker)` join is evaluated
non-deterministically by ClickHouse (observed 1,881 vs 1,360 on identical data),
so two single-key equi-joins are unioned in pandas; (b) the shared `q()` helper
coerces object columns with `pd.to_numeric`, which NaN'd the tickers and stripped
CUSIP leading zeros ('000354100'→354100) — a new `q_raw()` (no coercion) is used
for identifier columns. (b) alone explained the 1,360-vs-1,881 discrepancy.

**Before metric:** coverage unknown — never checked; Panel C treated as out of
scope without evidence.

**After metric:** **1,881 of 5,736 panel firm-years classifiable = 32.8%**
(12-month window). Per signal FY 1987→1995: 45.1 / 25.0 / 26.0 / 35.8 / 26.8 /
30.2 / 29.2 / 37.9 / 39.7%. Even the most permissive definition (any I/B/E/S
record on/before the FY-end, no window) reaches only **2,662 = 46.4%** — still
below the 60% threshold. 8-digit-CUSIP alone classifies 29.1%; CUSIP ∪ ticker
32.8%. Every classifiable firm-year has `numest ≥ 1` (all matched firms are
covered), so the 67% WITHOUT a record cannot be separated into "truly no analyst
following" vs "failed match" — an uncovered group cannot be constructed reliably.

**Status: NON-ACTIONABLE DATA GAP (Panel C = SKIP).** Decision path 2b: classifiable
share 32.8% < 60%, so the covered-vs-uncovered partition is a documented SKIP, not
a forced thin-data computation. Evidence (exact query + per-year counts + mapping)
is in `results/table_5_analyst.md`; the 5 Panel-C contract cells
(PanelC_coverage_share, PanelC_All_mean_uncovered, PanelC_HighLow_uncovered,
PanelC_HighLow_tstat_uncovered, PanelC_HighLow_covered) are marked SKIP in
`results/table_5.md`. The shortfall is data coverage, not a fixable bug: two
independent link keys agree (neither approaches 60%), the vintage (`ibes_202601`)
differs from the paper's 1999 tape, and late-1980s I/B/E/S coverage of small
high-BM firms is genuinely sparse — exactly the scenario audit1 anticipated.

---

## I2-m1: Tier-2 definitional footnote (minor — closed)

**Diagnosis:** The repo's `rep/TOLERANCE_RULES.md` defines Tier 2 as "sign matches,
no magnitude cap", while `audit/SKILL.md` spot-check 10 caps Tier 2 at 2× the
paper; ~20-25 A1-structural cells (e.g. Table 3 Panel B score-0 mean −0.236 vs
−0.061 = 3.87×; most count cells ≈ 0.4×) exceed 2× yet are labeled Tier 2, and
the tension was never flagged.

**Next fix:** Added footnote ¹ to `results/evaluation_summary.md` stating that
A1-structural cells are Tier-2-by-construction under the repo definition and would
exceed the audit's 2× pattern-match bound on ~20-25 cells; reclassifying them would
raise FAIL toward ~30+ WITHOUT changing any Tier-1 count (Tier 1 = 77, unaffected).
No reclassification performed.

**Before metric:** no footnote; the Tier-2/2× tension undocumented in the artifact.

**After metric:** footnote present in `evaluation_summary.md`; Tier-1 count
explicitly stated as unaffected (77).

**Status:** RESOLVED.

---

## I2-m2: Target-count bookkeeping (minor — closed)

**Diagnosis:** The denominator was opaque — `evaluation_summary.md` printed a total
that did not reconcile with the 138-metric contract (audit1 [m2]), and the
task-text extra `n_1996` (outside the JSON contract, flagged † in appendix_a.md)
was conflated with contract cells.

**Next fix:** Rewrote the `evaluation_summary.md` total to compute the contract
count from `tables_to_replicate.json` and state it explicitly.

**Before metric:** total line ambiguous (136 tallied vs 138 contract).

**After metric:** "**162 contract metrics = 138 (tables 1-4, 7, appendix_a) + 24
(table_5)**; **154 evaluated + 8 SKIP = 162**; the per-file 'Evaluated' column sums
to 155 because appendix_a.md ALSO tallies the 1 task-text extra `n_1996` (†,
outside the contract)." 8 SKIP = 3 pre-1988 Appendix-A cells (A1) + 5 Table-5
Panel-C analyst cells (I2-M2).

**Status:** RESOLVED.

---

## I2-audit4: Same-period benchmark anchor in Appendix A (minor — closed)

**Diagnosis:** The paper's own same-period (1988-1996) average spread — the single
most important benchmark for this A1-restricted replication — appeared only in
REPORT.md prose, not as a printed row in `results/appendix_a.md` (audit1 §4.4).

**Next fix:** Added a printed row to the Appendix-A annual-returns table.

**Before metric:** no same-period row in the artifact.

**After metric:** row "Paper avg, same-period 1988-1996 ‡" = **0.091** (computed
from the paper's printed annual rows: (0.168−0.036+0.157+0.166+0.070+0.020−0.001
+0.126+0.147)/9), next to ours (same 9 years) = **0.1040**, beside the full-period
0.097 target — anchoring the Tier-1 hedge claim to the like-for-like number inside
the artifact. Informational row, not a contract target.

**Status:** RESOLVED.
