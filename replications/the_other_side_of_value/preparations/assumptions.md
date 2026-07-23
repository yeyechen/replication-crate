# Assumptions Registry — Novy-Marx (2013) "The Other Side of Value"

Paper-silent decisions made during replication. Updated every iteration.

---

## Assumption 1: Delisting return treatment

**Decision:** Use CRSP dlret from dsedelist when available; no special imputation for missing dlret (paper is silent on delisting treatment).
**Rationale:** Paper does not mention delisting returns. The standard CRSP default is to use dlret when available. Since the paper uses monthly returns from msf (which already incorporate some delisting adjustment), and the focus is on annual June-rebalanced portfolios where delisting events are relatively rare for the large-cap stocks that drive VW results, the impact is expected to be small.
**Impact:** Affects all portfolio return calculations in Tables 2, 6, 7. Expected to be a second-order effect on VW returns.

## Assumption 2: Compustat standard filters

**Decision:** Apply indfmt='INDL', consol='C', popsrc='D', datafmt='STD' to comp_202601.funda.
**Rationale:** Paper says "The sample excludes financial firms (those with one-digit SIC codes of six)" but does not specify the standard Compustat data filters. These filters are the WRDS standard for obtaining unique, consolidated, domestic, standardized observations from funda. The indfmt='INDL' filter combined with the SIC 6xx exclusion ensures we get industrial-format observations only.
**Impact:** Affects all Compustat-derived variables (GP/A, BE, B/M, earnings, FCF). Standard practice.

## Assumption 3: GP/A computation when REVT or COGS missing

**Decision:** Use GP (Compustat data item) as fallback when REVT or COGS is missing. GP = REVT - COGS by definition. If GP is also missing, drop the observation.
**Rationale:** Paper defines GP/A as (REVT - COGS) / AT but also notes "Gross profits and earnings before extraordinary items are Compustat data items GP and IB, respectively" (footnote 2, L117). Compustat provides GP directly as a convenience item. Using GP as fallback maximizes coverage while maintaining consistency with the paper's definition.
**Impact:** Affects GP/A signal for all tables. Expected to add coverage for some firm-years where REVT or COGS is individually missing but GP is reported.

## Assumption 4: Book equity — missing PSTX handling

**Decision:** When PSTX is missing (not available in comp_202601.funda), use the fallback path: SEQ → AT-LT (skipping the CEQ+PSTX path). For preferred stock, use PSTKR → PSTK (skipping PSTKRL which is also missing).
**Rationale:** The paper specifies tiered definitions (L127): SEQ if available, else CEQ+PSTX, else AT-LT. Since PSTX is missing from our Compustat vintage, the CEQ+PSTX path is unavailable. The SEQ and AT-LT fallbacks cover the vast majority of observations. Similarly, PSTKRL is missing but PSTKR and PSTK are available.
**Impact:** Affects book equity computation. SEQ is available for most firm-years, so the CEQ+PSTX path is rarely needed. Expected minimal impact.

## Assumption 5: CRSP-Compustat link filter

**Decision:** Use ccmxpf_linktable with linkprim IN ('P','C') and usedflag=1 for primary links. Take the first valid link per (gvkey, lpermno) pair.
**Rationale:** Paper is silent on the specific link table filter. The WRDS standard is to use primary links (linkprim='P') with usedflag=1. Including 'C' (combined) as a secondary option increases coverage slightly. This is the standard approach in the literature.
**Impact:** Affects the Compustat-CRSP merge for all tables. Standard practice with minimal impact.

## Assumption 6: Market equity for B/M — 6-month lag

**Decision:** Use CRSP market equity at December of year t-1 for fiscal year t's B/M ratio. Specifically, for a firm with fiscal year ending in calendar year t, ME is measured at end of December t-1 (6 months before end of June t when the signal is used for portfolio formation).
**Rationale:** Paper states "Book-to-market is book equity scaled by market equity, where market equity is lagged six months to avoid taking unintentional positions in momentum" (L117). The FF (1992) convention maps fiscal year t data to July t+1, so the 6-month lag means ME at December t.
**Impact:** Affects B/M ratio for all tables. Critical for correct signal timing.

## Assumption 7: FF49 industry classification

**Decision:** Derive FF49 industry assignments from SIC codes using the standard Fama-French 49-industry SIC mapping. Apply to GP/A, earnings/BE, and FCF/BE for industry-demeaned variables in Table 1 Panel B.
**Rationale:** Paper uses "Fama and French (1997) 49 industry portfolios" for industry adjustment (L119). The FF49 classification is a standard mapping from 4-digit SIC codes. SIC codes are available in both Compustat (sich) and CRSP (hsiccd/siccd).
**Impact:** Affects Table 1 Panel B (industry-adjusted variables). Does not affect Tables 2, 6, 7.

## Assumption 8: Returns in decimal vs percentage

**Decision:** Store and compute returns in decimal form internally. Convert to percentage (×100) only for reporting to match paper's format. FM regression coefficients reported ×10^2 as in the paper.
**Rationale:** Paper reports returns in percent per month (e.g., 0.31% per month) and FM coefficients ×10^2. CRSP returns are in decimal. FF factors in ClickHouse are in percent (divide by 100 for decimal). Consistent internal representation prevents scaling errors.
**Impact:** Affects all tables. Critical for correct magnitude matching.

> ⚠️ **rep-worker correction (2026-07-22, data pipeline):** the parenthetical
> "FF factors in ClickHouse are in percent" is **wrong for this instance** —
> verified live: `ff.four_factor_monthly` values are in **DECIMALS**
> (`mkt_rf = -0.0472` for 2000-01 ≈ the actual −4.72% market excess return;
> `rf ≈ 0.004` = 40 bps/month). No ÷100 applied anywhere in the pipeline.
> The ×100 conversion for *reporting* percent figures stands.

---

# rep-worker flags — data pipeline iteration (2026-07-22)

## Flag A: PSTX fallback diverges from Assumption 4

Assumption 4 says skip the CEQ+PSTX tier entirely (SEQ → AT−LT).
The pipeline instead substitutes **PSTK** for the missing PSTX
(SEQ → CEQ+PSTK → AT−LT, requiring both CEQ and PSTK non-missing),
which is the canonical Davis-Fama-French / WRDS implementation when
PSTX is unavailable. Only affects firm-years where SEQ is missing
but CEQ and PSTK are both present (mostly pre-1985). Replicator to
decide; one-line change in `src/sql/compustat_funda.sql` if the
skip-tier reading is preferred.

## Flag B: B/M timing — Assumption 6 is self-contradictory

Assumption 6's first sentence says "ME at December t−1" (with t =
fiscal-year-end year) while its last sentence says "ME at December t".
Implemented the standard FF/NM convention: `bm(fy y) = BE(y) /
ME(December y)` — December of the fiscal-year-END calendar year,
which is December t−1 relative to the June-t formation (6-month lag).
This is consistent with the assumption's last sentence and with
NM's "market equity is lagged six months". Verified on IBM FY2009:
BE 23,107 / ME-Dec-2009 172,000 → bm 0.1344.

## Flag C: link filter adds linktype IN ('LC','LU')

Assumption 5 specifies linkprim IN ('P','C') + usedflag=1. The
pipeline additionally requires linktype IN ('LC','LU') (the full
WRDS-recommended filter). With usedflag=1 this is nearly a no-op;
flagged for completeness.

## Flag D: financials excluded at BOTH the CRSP and Compustat levels

The paper cites the Compustat SIC. The pipeline excludes SIC 6xx at
the CRSP PIT level too (`dsenames.siccd`, which is why dsenames is
listed as a data source in the task), so financial stock-months
never enter the panel even without Compustat coverage. NULL SIC
rows are kept at both levels.

## Flag E: missing-data details (paper silent)

- FCF = NI + DP − WCAPCH − CAPX with missing DP/WCAPCH/CAPX treated
  as 0 (NI required). Firm-years require AT > 0.
- B/M set to NULL for book equity ≤ 0 (negative-BE firms excluded
  from B/M); earnings_be / fcf_be computed whenever BE ≠ 0 — extreme
  outliers exist (earnings_be min −9,033) and are handled by the
  paper's 1%/99% trim, which is applied at the FM stage only
  (downstream), NOT to the panel.
- r_12_2 requires all 11 months non-missing AND contiguous (strict
  reading of "cumulative return from month t−12 to t−2"); r_1_0
  requires the prior row to be the prior calendar month.
- `log_me` uses the formation-June ME (constant over the holding
  year), matching NM's six-month-lagged size control; current-month
  ME is carried as `me_crsp` for VW weighting.
- June rows carry the PRIOR portfolio year's accounting data; the
  July cross-section is where formation-measured variables line up
  (downstream FM should slice July rows).

## Flag F: ClickHouse `Date` cannot hold pre-1970 dates

`toDate` clamps pre-1970 dates to 1970-01-01 on this instance; all
date parsing in the SQL uses `toDate32` / `makeDate32`.

## Flag G: GP/A fallback rarely binding

GP = REVT − COGS with fallback to the GP data item; the GP item
covers ~93% of firm-years in this extract (78,996/84,731 in the
1970s decade), so the fallback adds modest coverage when REVT or
COGS is individually missing.

---

# rep-worker flags — Table 2 iteration (2026-07-22)

## Flag H: June formation cross-section taken from the July rows

The Table 2 task text says "take the cross-section at each June
formation." Literally reading the panel's June rows is wrong on two
counts: (1) Flag E — June rows carry the PRIOR portfolio year's
accounting data (FY t−2 at June t), not the formation signal; (2) no
June-1963 row exists (panel starts July 1963), so literal June
formation drops the paper's first holding year. Implemented: the
June-t formation cross-section = July-t rows (the first month of
holding year July t–June t+1), which carry the FY t−1 data that
became available at end of June t — matching the paper's fiscal-year
mapping and covering all 570 months (48 formations, avg 3,433
stocks/formation on GP/A). A literal-June diagnostic is preserved in
`run_table2()`: it gives a weaker H-L spread (0.19%, t=1.43 vs 0.32%,
t=2.51 main / paper 0.31%, t=2.49), confirming the July-row reading.

## Flag I: VW weights use PRIOR-month me_crsp (deviation from task wording)

⚠️ The Table 2 task text said "Weight = me_crsp" at each holding-year
month (contemporaneous). Contemporaneous weights date the weight at
the same month as the return: VW_cont = (R + Σwᵢrᵢ²)/(1+R), biasing
EVERY portfolio up by roughly the weighted cross-sectional return
variance — measured here at +0.6 to +0.7%/month (+0.36%/mo in the
1960s growing to +1.04%/mo in the 2000s, tracking idiosyncratic
volatility). This inflates every r^e and FF3 alpha by the same amount
while leaving spreads and loadings intact. Verified against the paper:
contemporaneous weights give Low/High r^e = 0.99/1.19 (alphas
0.48/0.90) vs paper 0.31/0.62 (−0.18/0.34); prior-month weights give
0.30/0.62 (−0.21/0.34) and H-L 0.32% t=2.51 (paper 0.31% t=2.49).
Standard FF value-weighting (and any cap-weighted index) uses
beginning-of-period weights, so prior-month is the methodology-
consistent reading. Implemented: me_w = me_crsp lagged one month
within permno; falls back to contemporaneous me_crsp where the lag is
unavailable (every stock's first panel month — July 1963 — and IPO
months). The contemporaneous variant is preserved as a diagnostic in
`run_table2()`. Replicator to confirm.

## Flag J: characteristics reported as portfolio aggregates

"Portfolio-level GP/A, B/M" implemented as monthly aggregates:
GP/A = Sum(GP)/Sum(AT) (GP = gp_a×at) and B/M = Sum(BE)/Sum(ME) over
firms with BE > 0, then time-series averaged. The aggregate convention
is required to match the paper's Low-quintile GP/A (0.10): the
equal-weighted firm average is ~0.02 because the Low quintile holds
many microcaps with negative gross profits. Aggregate results vs
paper: GP/A [0.10, 0.21, 0.32, 0.45, 0.71] vs paper [0.10, 0.20,
0.30, 0.42, 0.68] — all Tier 1. B/M [0.90, 0.74, 0.60, 0.41, 0.28]
vs paper [1.10, 0.98, 1.00, 0.53, 0.33] — 4 Tier 1, Q3 Tier 2
(−40%); the paper's flat-then-steep B/M shape is not reproduced by
any single convention tested (EW firm avg [1.05, 1.07, 0.96, 0.85,
0.73] — 3 Tier 1; ME-weighted firm avg [0.95, 0.78, 0.64, 0.45,
0.30] — 4 Tier 1). n runs ~12-17% below the paper in every quintile
(Compustat-coverage difference in this vintage) and ME per firm ~0-13%
above; both Tier 1. Replicator to confirm the B/M convention.

## Flag K: main.py caches the panel by default

`main()` loads data/panel.parquet + data/ff_factors.parquet when both
exist; pass `--rebuild` to re-extract from ClickHouse. Added to make
Table 2 iterations fast (the full extraction takes several minutes).
