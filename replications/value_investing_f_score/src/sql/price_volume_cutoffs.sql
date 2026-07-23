-- price_volume_cutoffs.sql
-- Purpose: Prior-year portfolio-assignment tercile breakpoints over the FULL
--          Compustat universe (standard filter), per fiscal year, for Table 5:
--            * Share PRICE cutoffs (33.3/66.7 pct of prcc_f; universe = all
--              standard-filter firms with prcc_f > 0) — self-contained from funda,
--              following the bm_size_cutoffs.sql pattern.
--            * Trading VOLUME (turnover) cutoffs (33.3/66.7 pct of turnover;
--              universe = all LINKED-Compustat firm-years with turnover available,
--              the same population as the MOMENT/ACCRUAL deciles) — read from the
--              staged write_yeye.{turn_table} (gvkey, fyear, turnover) produced by
--              firm_turnover.sql over the linked ME>0 universe.
--          A firm in fyear t is classified with the cutoffs from fyear t-1 (no
--          lookahead, footnote 8 / Table 4 machinery). Covers fyear
--          {cutoff_start}..{cutoff_end} (= FY1986..FY1994), which assigns panel
--          fyear {cutoff_start+1}..{cutoff_end+1} (= FY1987..FY1995; the FY1987
--          cohort uses FY1986 cutoffs — computable, price needs no oancf).
-- Tables: comp_202601.funda, write_yeye.{turn_table}
-- Output columns: fyear, price_p33, price_p67, n_price, vol_p33, vol_p67, n_vol
-- Depends on: main.py stages {turn_table} via firm_turnover.sql (linked ME>0
--             universe FY1986-1995; the volume cutoff uses its FY1986-1994 rows).
-- Notes: quantileExact = deterministic empirical percentiles (identical
--        convention to bm_size_cutoffs.sql). Price universe needs no CRSP link
--        and no oancf (content.md L2524: "price per share at the end of the
--        fiscal year preceding portfolio formation"). Volume universe is the
--        linked-Compustat population with turnover available (content.md L2526).
--        LEFT JOIN keeps every price-cutoff year even if a volume cutoff is absent.
-- Settings: max_execution_time=300, max_rows_to_read=10e9

WITH funda_raw AS (
    SELECT gvkey, fyear, datadate, prcc_f
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND datafmt = 'STD' AND consol = 'C' AND popsrc = 'D'
      AND fyear BETWEEN {cutoff_start} AND {cutoff_end}
      AND gvkey IS NOT NULL AND fyear IS NOT NULL
),
funda AS (
    SELECT gvkey, fyear, argMax(prcc_f, datadate) AS prcc_f
    FROM funda_raw
    GROUP BY gvkey, fyear
),
price_cut AS (
    SELECT fyear,
           quantileExact(0.3333333)(prcc_f) AS price_p33,
           quantileExact(0.6666667)(prcc_f) AS price_p67,
           count() AS n_price
    FROM funda
    WHERE prcc_f IS NOT NULL AND prcc_f > 0
    GROUP BY fyear
),
vol_cut AS (
    SELECT fyear,
           quantileExact(0.3333333)(turnover) AS vol_p33,
           quantileExact(0.6666667)(turnover) AS vol_p67,
           count() AS n_vol
    FROM write_yeye.{turn_table}
    WHERE turnover IS NOT NULL
      AND fyear BETWEEN {cutoff_start} AND {cutoff_end}
    GROUP BY fyear
)
SELECT p.fyear AS fyear,
       p.price_p33 AS price_p33, p.price_p67 AS price_p67, p.n_price AS n_price,
       v.vol_p33 AS vol_p33, v.vol_p67 AS vol_p67, v.n_vol AS n_vol
FROM price_cut AS p
LEFT JOIN vol_cut AS v ON v.fyear = p.fyear
ORDER BY p.fyear
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
