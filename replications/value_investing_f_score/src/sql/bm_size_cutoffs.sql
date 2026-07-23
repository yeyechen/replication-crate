-- bm_size_cutoffs.sql
-- Purpose: Prior-year portfolio-assignment breakpoints over the FULL Compustat
--          universe (standard filter), per fiscal year:
--            * BM quintile cutoffs  (20/40/60/80 pct of BM, firms with ME>0 AND BE>0)
--            * Size tercile cutoffs (33.3/66.7 pct of MVE, firms with ME>0)
--          A firm in fyear t is classified with the cutoffs from fyear t-1
--          (no-lookahead, footnote 8). Covers fyear {cutoff_start}..{cutoff_end}
--          (= FY_SIGNAL_START-1 .. FY_SIGNAL_END-1), which assigns fyear
--          {fy_signal_start}..{fy_end}.
-- Tables: comp_202601.funda
-- Output columns: fyear, bm_p20, bm_p40, bm_p60, bm_p80, me_p33, me_p67,
--                 n_bm_firms, n_size_firms
-- Depends on: (none) — recomputes the filtered/deduped funda base (same recipe as
--             funda_base.sql: standard filter, argMax dedup, ME = prcc_f*csho,
--             BE per assumption A3).
-- Notes: quantileExact = deterministic empirical percentiles. BM universe is
--        "sufficient price and book value data" (ME>0 AND BE>0); size universe
--        is ME>0 regardless of book equity (Table 4 footnote a: "all firms on
--        Compustat with sufficient size ... data").
-- Settings: max_execution_time=300, max_rows_to_read=10e9

WITH funda_raw AS (
    SELECT gvkey, fyear, datadate, at, lt, prcc_f, csho,
           ceq, seq, txdb, pstkrv, pstk
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND datafmt = 'STD' AND consol = 'C' AND popsrc = 'D'
      AND fyear BETWEEN {cutoff_start} AND {cutoff_end}
      AND gvkey IS NOT NULL AND fyear IS NOT NULL
),
funda AS (
    SELECT gvkey, fyear,
           argMax(prcc_f, datadate) AS prcc_f,
           argMax(csho, datadate)   AS csho,
           multiIf(
               argMax(ceq, datadate) IS NOT NULL,
                   argMax(ceq, datadate) + ifNull(argMax(txdb, datadate), 0)
                   - ifNull(argMax(pstkrv, datadate), 0),
               argMax(seq, datadate) IS NOT NULL,
                   argMax(seq, datadate) - ifNull(coalesce(argMax(pstk, datadate),
                                                           argMax(pstkrv, datadate)), 0),
               argMax(at, datadate) IS NOT NULL AND argMax(lt, datadate) IS NOT NULL,
                   argMax(at, datadate) - argMax(lt, datadate)
                   - ifNull(argMax(pstk, datadate), 0),
               CAST(NULL, 'Nullable(Float64)')
           ) AS be
    FROM funda_raw
    GROUP BY gvkey, fyear
),
me_bm AS (
    SELECT fyear,
           if(prcc_f IS NOT NULL AND csho IS NOT NULL AND prcc_f > 0 AND csho > 0,
              prcc_f * csho, CAST(NULL, 'Nullable(Float64)')) AS mve,
           be
    FROM funda
)
SELECT b.fyear AS fyear,
       b.bm_p20 AS bm_p20, b.bm_p40 AS bm_p40, b.bm_p60 AS bm_p60,
       b.bm_p80 AS bm_p80, b.n_bm_firms AS n_bm_firms,
       s.me_p33 AS me_p33, s.me_p67 AS me_p67, s.n_size_firms AS n_size_firms
FROM (
    SELECT fyear,
           quantileExact(0.2)(be / mve) AS bm_p20,
           quantileExact(0.4)(be / mve) AS bm_p40,
           quantileExact(0.6)(be / mve) AS bm_p60,
           quantileExact(0.8)(be / mve) AS bm_p80,
           count() AS n_bm_firms
    FROM me_bm
    WHERE mve IS NOT NULL AND be IS NOT NULL AND be > 0
    GROUP BY fyear
) AS b
INNER JOIN (
    SELECT fyear,
           quantileExact(0.3333333)(mve) AS me_p33,
           quantileExact(0.6666667)(mve) AS me_p67,
           count() AS n_size_firms
    FROM me_bm
    WHERE mve IS NOT NULL
    GROUP BY fyear
) AS s ON s.fyear = b.fyear
ORDER BY b.fyear
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
