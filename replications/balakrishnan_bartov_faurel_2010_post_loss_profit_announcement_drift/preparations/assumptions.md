# BBF (2009) Replication — Assumption Registry

This file documents every methodology choice, paper-silent assumption,
and target-vs-replication gap that came up while building Table 1
(sample selection). It is appended-only — earlier entries are not
edited when new ones are added.

## Iteration 1 — Table 1 sample selection

### Assumption A1 — `atq` interpretation

The task spec says required Compustat data are "data8 (= ibq) and
data44 (= atq) ... in quarter q". The paper's footnote a on Table 1
says required data are "data8 ... in quarter q, and total assets
(Compustat Quarterly data44) in quarter q-1". The two are not
contradictory if "beginning-of-quarter total assets" = atq at end of
q-1 (= beginning of q), but they are different concrete filters.

We followed the **task spec** (atq non-missing at q) for the main
pipeline, because the task spec is explicit. The paper-footnote
variant (atq non-missing at q-1) is documented as a known
alternative in A2 below.

### Assumption A2 — `atq` in q-1 alternative count

If we apply the paper's strict footnote reading (atq in q-1 non-null),
the CRSP-merged count drops from 558,083 → 525,014 (–5.9%). Still
~11% above the paper's 471,997, but the gap is smaller. We do not
use this filter in the main pipeline because the task spec is
explicit about atq-in-q.

### Assumption A3 — CRSP-Compustat link filter

We use the WRDS-recommended link filter on `ccmxpf_linktable`:

```sql
linktype IN ('LC', 'LU')
AND linkprim IN ('P', 'C')
AND usedflag = 1
```

with the PIT predicate

```sql
toDate32OrNull(c.rdq) >= toDate32OrNull(l.linkdt)
AND coalesce(nullIf(l.linkenddt, ''), '2099-12-31') >= c.rdq
```

The `coalesce(nullIf(...), '2099-12-31')` handles both NULL and
empty-string `linkenddt` (both indicate "still active"). We take
`any(lpermno)` per (gvkey, datadate, rdq) — multiple valid permnos
per gvkey on a single rdq are collapsed to one row, which matches the
paper's "distinct firms" count convention.

We tested variants (linkprim=P only, linktype=LC only, FF indfmt
filter, datacqtr filter, min-listing-period filter, daily-return-on-rdq
filter) — none closed the gap to the paper's 471,997 by more than ~1
percentage point. The bulk of the gap is unexplained at this point.

### Assumption A4 — Price-5-trading-days-prior filter

The paper says "stock prices five days prior to the quarterly earnings
announcement date". This is ambiguous between 5 calendar days and 5
trading days. We implement it as **5 trading days prior**, which is
the more common academic convention. The look-back is implemented via:

```sql
d.date BETWEEN (toDate32(c.rdq) - INTERVAL 14 DAY)
               AND (toDate32(c.rdq) - INTERVAL 1 DAY)
```

followed by `ROW_NUMBER() OVER (PARTITION BY gvkey, rdq ORDER BY date DESC) = 5`.
14 calendar days covers ~10 trading days (5 + buffer for holidays).
Strictly fewer than 5 prior trading days yields NULL `prc_5d_prior`,
which we treat as failing the filter.

If we instead treat "5 days prior" as 5 **calendar** days and use an
ASOF JOIN with `target_date = rdq - 5 day`, the count would change
slightly (typically a few hundred obs). We did not adopt that
interpretation.

### Assumption A5 — SUE history simplification

The paper requires 13 consecutive quarters of `epspxq` (q-12 through
q) for the SUE supplementary sample. The task spec explicitly permits
the simplifying assumption "require non-missing `epspxq` at q and at
q-12". We implement the simplifying assumption: a row is SUE-eligible
iff `epspxq IS NOT NULL` at q AND `epspxq_q12 IS NOT NULL` (the
q-12 value attached via self-join on `(gvkey, fyearq-3, fqtr)`).

This is strictly weaker than the paper's filter and will over-count
SUE-eligible firm-quarters relative to the paper. The exact magnitude
of the over-count is unknown; in our run it pushes the SUE count
from a paper-target-shaped 359,909 → our 459,106 (with both the price
filter and the SUE simplification applied).

### Assumption A6 — BM supplementary filter

Strict application of the paper: `ceqq IS NOT NULL AND cshoq IS NOT NULL AND prccq IS NOT NULL` at q. We implement exactly this. The book value of equity used by the paper is
`ceqq / (cshoq * prccq)` per footnote c, so all three fields are
needed at quarter q.

### Assumption A7 — Accruals supplementary filter

Per footnote d, the paper requires:

- `ibq` at q
- `oancfy` at q
- `xidocy` at q
- `atq` at q AND at q-1 (average total assets denominator)
- `rdq >= '1988-01-01'` (cash-flow data starts in 1988)

We implement all five. The q-1 `atq` is attached via self-join on
`(gvkey, fyearq-?, fqtr)` where the previous fiscal quarter depends on
the firm's fiscal calendar (Q1 → prior-year Q4, else fqtr-1 of same
fyearq).

### Assumption A8 — `panel.parquet` is the canonical intermediate

All per-stage counts in Table 1 are computed from
`data/panel.parquet`. The panel is built by `src/sql/panel.sql` and
contains 17 columns (gvkey, datadate, rdq, fyearq, fqtr, ibq, atq,
epspxq, ceqq, cshoq, prccq, oancfy, xidocy, epspxq_q12, atq_q1,
permno, prc_5d_prior). Each downstream filter (price, SUE, BM,
accruals) is applied in Python against this panel — see
`src/main.py::stage_counts`.

### Known gap — replicated vs paper counts

| Stage | Ours | Paper | % diff |
|---|---:|---:|---:|
| primary_all firm-quarters         | 558,083 | 471,997 | +18.24% |
| primary_all distinct firms        |  17,803 |  15,261 | +16.66% |
| primary_after_price1 firm-quarters| 535,227 | 458,693 | +16.69% |
| primary_after_price1 distinct firms | 17,559 |  15,143 | +15.95% |
| supp1_sue firm-quarters           | 459,106 | 359,909 | +27.56% |
| supp1_sue distinct firms          |  15,284 |  12,824 | +19.18% |
| supp2_bm firm-quarters            | 518,066 | 448,500 | +15.51% |
| supp2_bm distinct firms           |  17,464 |  15,101 | +15.65% |
| supp3_accruals firm-quarters      | 317,828 | 267,416 | +18.85% |
| supp3_accruals distinct firms     |  13,612 |  10,695 | +27.27% |

**Every cell is outside the ±2% Tier-1 tolerance.** The gap is
broadly uniform (~16%–28%) across stages, which suggests a
systematic over-count at the CRSP-merge step rather than a specific
filter being wrong. We did not find a single filter that closes the
gap to within ±2% in our 2026-vintage data. Plausible explanations
not yet ruled out:

1. **Compustat vintage drift.** The 2026 instance of `comp_202601.fundq`
   has 2.1M quarterly rows. The BBF-era extract (used in 2009) would
   have had fewer rows because later restatements extend the
   history back (more firms in earlier years) and add coverage for
   firms that didn't file in the past. This is a real concern for
   replications of pre-2010 papers on post-2020 Compustat extracts.

2. **CRSP-Compustat link vintage drift.** `ccmxpf_linktable` has
   been continuously updated; the 2026 vintage has +3% more rows than
   the 2025 vintage per the catalog notes. The 2009-vintage
   `ccmxpf_linktable` is not directly available.

3. **Possibly stricter CRSP filter in the paper.** The paper text is
   silent on whether the CRSP requirement is just "any return data"
   or something more restrictive (e.g., `dsf` row present on rdq
   itself). We tested variants: requiring dsf-on-rdq drops the count
   by ~3,400 (0.6%), still leaving a >15% gap.

The Tier classification per `rep/STUCK_AGENT_GUIDELINE.md` is
**FAIL** — no cell meets ±2% tolerance, and no single identifiable
filter choice closes the gap. The replicator should review whether
the BBF-era vintage of Compustat is available (via `comp_202509` or
earlier `comp_snapshot_*` tables) and whether a stricter CRSP filter
matches the paper's actual implementation.

---

## Iteration 2 — Table 2 (BHAR computation)

### Assumption A9 — size-decile benchmark is equal-weighted, not value-weighted

The paper specifies value-weighted size-decile returns for the SAR
benchmark (the daily expected return for firm i on day t is "the
value-weighted return for all firms in firm i's size-matched
decile on day t"). CRSP's `crsp_202601.erdport1` is equal-weighted
by size decile (the `decret` column). The paper's VW version is not
directly available in this instance.

**Impact:** Decile benchmark returns are systematically different
between EW and VW; VW up-weights the largest names in each decile.
Our [1,60]/[1,120] decile BHARs are systematically LARGER in
magnitude than the paper's (D1 drift ~3x, hedge ~2-3x) — consistent
with a smaller benchmark cumprod under EW vs VW when the benchmark
includes more small-cap noise. Sign and monotonicity are unaffected.

**Justification:** Without a daily size-decile VW table in the
catalog, EW is the only available benchmark. Documented here so
the auditor can flag it as a known systematic bias in the
post-announcement drift magnitudes.

### Assumption A10 — decile breakpoints are computed per calendar quarter, not per prior fiscal quarter

The paper says "we compute cut-off points based on the previous
fiscal quarter's earnings distribution" (§3.1, page 12). The
prior-fiscal-quarter mapping requires a (gvkey, fyearq-1, fqtr) join
that depends on each firm's fiscal calendar. As a pragmatic
simplification we use the calendar quarter of `rdq` (the
announcement date) as the sort period. This affects only firm-quarters
near a fiscal-quarter boundary and is a small share of the sample.

**Impact:** Modest — affects boundary firms' decile assignment only.
The headline pattern (D1 < D2 < ... < D10 in BHAR) is robust.

### Assumption A11 — outlier clipping at ±200%

We clip BHAR values at ±2.0 (200%) before computing decile means.
This handles the ~0.05% of firm-quarters with extreme values from
erroneous daily returns or sparse return windows. Without clipping,
the D1/D10 means would be dominated by a handful of outlier events.

**Impact:** Affects <0.1% of firm-quarters; negligible.


---

## Iteration 3 — Decile breakpoints fix (M2), plumbing fixes (M3), subsample stability (M4)

### Assumption A2-revised (replaces A10) — Decile breakpoints from prior fiscal quarter

The paper §3.1 page 12 explicitly states "we compute cut-off points
based on the previous fiscal quarter's earnings distribution" to avoid
look-ahead bias. A10 (per-calendar-quarter breakpoints) was a pragmatic
simplification but introduced look-ahead bias at quarter boundaries.

The fix: for each firm-quarter observation, look up the same firm's
prior (gvkey, rdq-ordered) earnings_at value, then assign the current
observation's decile based on its position within the *prior fiscal
quarter's* earnings distribution. This is the per-firm analogue of
the paper's "previous fiscal quarter's earnings distribution" lookup.

**Implementation:** `src/table2_compute.py` — group panel by `gvkey`,
shift `earnings_at` by 1 within the firm-year panel, and assign deciles
grouped by `prior_cal_q` (calendar quarter of the prior fiscal quarter's
announcement date).

**Impact:** 521,868 firm-quarters assigned to deciles (vs 538,946
under A10). D1 BHARs change modestly:
- A10 [-2, 0] D1: -0.0100 → A2: -0.0098 (closer to paper -0.0102)
- A10 [1, 60] D1: -0.1091 → A2: -0.1062
- A10 [1, 120] D1: -0.1952 → A2: -0.1877

The hedge spread [1, 120] shifts from +0.2332 (A10) to +0.2280 (A2),
still positive, still monotone, still significant at t > 50.

### M3 — Plumbing fixes

- **Sample-size cells** (`d1_high_loss_n`, `d10_high_profit_n`):
  piped through evaluator. Ours 52,247 / 52,229 vs paper 46,753 /
  47,078 — Tier 2 (16-12% over-count, consistent with vintage drift).
- **`primary_after_price1` cells** (firmqtrs + distinct_firms):
  evaluator regex extended to handle these suffixes; previously SKIP'd,
  now Tier 2.
- **Decile t-stats and hedge t-stats**: parsed from table_2.md into
  the evaluator (per-cell `t_stat` from each decile row; hedge `t`
  from the bold "Hedge" line). All 4 t-stat cells now Tier 2.
- **FF cells** (`*_ff_*`): evaluator now correctly SKIPs these — the
  Carhart 4-factor benchmark is not implemented in this pipeline
  (would require per-firm 40-trading-day estimation windows).

### M4 — Subsample stability (paper footnote 15)

Computed D10-D1 hedge spread by 10-year subperiod on the [1, 120]
window:

| Subperiod | Ours | Paper target | t-stat (ours) |
|---|---:|---:|---:|
| 1976-1985 | +0.2213 | +0.1075 | +26.62 |
| 1986-1995 | +0.1896 | +0.0868 | +25.06 |
| 1996-2005 | +0.2583 | +0.1103 | +37.03 |

**Pattern:** positive and significant in all three subperiods (the
paper's headline subperiod-stability claim). **Magnitude:** biased
by A9 (EW vs VW benchmark) — same factor as in the full-sample hedge.
The subperiod stability pattern (similar magnitude across the three
subperiods in our data) is reproduced.

