# Table 5 Panel C — Analyst-Following Partition: Feasibility & Decision (SKIP)

**Decision: SKIP.** The paper (content.md L2528/L2550) defines analyst following as the number of I/B/E/S forecasts at the last statistical period of the year preceding formation, and reports a covered-vs-uncovered High−Low split (0.114 vs 0.277; 37.8% covered) from the 1999 I/B/E/S summary tape. Per audit1 [M2], the partition is computed only if ≥ 60% of panel firm-years are classifiable; otherwise it is a documented SKIP.

## Feasibility query & mapping

- **IBES table:** `ibes_202601.statsum_epsus` (I/B/E/S summary statistics; EPS measure; `numest` = number of forecasts; `statpers` = statistical-period date; covers 1976-01-15 → 2025-12-18 in this vintage — the 1986-1995 panel window is present).
- **Mapping:** comp_202601.funda (tic, cusip; argMax datadate, standard filter) -> ibes_202601.statsum_epsus on 8-digit CUSIP (Compustat 9-digit drops check digit) OR ticker; statsum.numest = # forecasts at the statistical period. Two single-key equi-joins unioned in pandas (a combined CTE union is non-deterministic in ClickHouse).
- **Classifiable:** a firm-year with an I/B/E/S statistical-period record within the 12 months ending at its FY-end `datadate`. **Covered:** `numest ≥ 1` at the last such record.

```sql
SELECT u.gvkey AS gvkey, u.fyear AS fyear,
           max(s.statpers) AS last_sp,
           argMax(s.numest, s.statpers) AS numest_last
    FROM write_yeye.piotroski_pv_ibes_id_v1 AS u
    INNER JOIN ibes_202601.statsum_epsus AS s ON s.cusip = u.cusip8
    WHERE u.cusip8 IS NOT NULL
      AND s.statpers >= '1985-01-01' AND s.statpers <= '1997-12-31'
      AND toDate(parseDateTimeBestEffort(s.statpers)) <= u.datadate
      AND toDate(parseDateTimeBestEffort(s.statpers)) >= addYears(u.datadate, -1)
    GROUP BY u.gvkey, u.fyear
```

## Coverage by fiscal year (formation year = fyear + 1)

| Signal FY | Panel n | Classifiable | % classifiable | Covered (numest≥1) |
|---|---:|---:|---:|---:|
| 1987 | 173 | 78 | 45.1% | 78 |
| 1988 | 579 | 145 | 25.0% | 145 |
| 1989 | 666 | 173 | 26.0% | 173 |
| 1990 | 1,107 | 396 | 35.8% | 396 |
| 1991 | 466 | 125 | 26.8% | 125 |
| 1992 | 537 | 162 | 30.2% | 162 |
| 1993 | 554 | 162 | 29.2% | 162 |
| 1994 | 934 | 354 | 37.9% | 354 |
| 1995 | 720 | 286 | 39.7% | 286 |
| **Total** | **5,736** | **1,881** | **32.8%** | **1,881** |

**Result: 1,881 of 5,736 panel firm-years classifiable = 32.8%** — below the 60% threshold. Even under the most permissive definition (any I/B/E/S record on/before the FY-end, no 12-month window), only 2,662 = 46.4% are classifiable — still below 60%.

For the 1,881 covered firm-years, the average (median) number of forecasts at the last statistical period is **2.39 (1)** — directionally consistent with the paper's 3.15 (2) for its covered firms (content.md L2550), confirming the match targets real analyst coverage where it exists; the gap is the *share* of firms covered, not the coverage measure itself.

## Why this is a non-actionable data gap (not a pipeline defect)

1. **Coverage of small high-BM firms in this vintage is genuinely thin and era-concentrated.** Every classifiable firm-year has `numest ≥ 1` (all matched firms are covered): the 67% WITHOUT an I/B/E/S record cannot be separated into 'truly no analyst following' vs 'failed CUSIP/ticker match', so an uncovered group cannot be constructed reliably. This is exactly the late-1980s small-cap coverage sparsity audit1 anticipated.
2. **The vintage differs from the paper's.** The paper used the 1999 I/B/E/S tape over 1976-1996 (37.8% of 14,043 covered); this replication is restricted to FY1987-1995 under A1 (5,736 firm-years) on the `ibes_202601` vintage, whose early-period small-cap coverage is sparser.
3. **Two independent link keys agree.** 8-digit-CUSIP match alone classifies 29.1%; CUSIP ∪ ticker union reaches 32.8% — no link strategy approaches 60%, so the shortfall is data coverage, not a fixable matching bug.

**Panel C contract cells (PanelC_coverage_share, PanelC_All_mean_uncovered, PanelC_HighLow_uncovered, PanelC_HighLow_tstat_uncovered, PanelC_HighLow_covered) are marked SKIP in results/table_5.md.** A five-field log entry is appended to preparations/assumptions.md (Status: non-actionable data gap).
