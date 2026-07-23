-- firm_turnover.sql
-- Purpose: Fiscal-year share turnover for every firm-year staged in
--          write_yeye.{src_table} (gvkey, fyear, permno, datadate):
--            turnover = sum(vol)*100 / avg(shrout*1000)
--          over the 12 month-ends ending in the fiscal year-end month, i.e. the
--          window [addMonths(toStartOfMonth(datadate), -11) .. datadate] (the
--          firm's own fiscal year; content.md L2526 "total number of shares
--          traded during the prior fiscal year scaled by the average number of
--          shares outstanding during the year"). Used for Table 5 Panel B:
--          volume tercile cutoffs (full linked universe) AND panel turnover.
-- Tables: write_yeye.{src_table}, crsp_202601.msf
-- Output columns: gvkey, fyear, turnover, n_months
-- Depends on: main.py stages {src_table} = linked ME>0 funda universe
--             FY1986-1995 (fetch_pv_universe: standard filter, ME=prcc_f*csho>0,
--             CRSP P/C point-in-time link — superset of the high-BM panel).
-- UNITS (verified by single-firm + distribution spot check, Rule 10): in this
--   CRSP vintage `vol` is in HUNDREDS of shares and `shrout` in THOUSANDS. The
--   *100 converts vol to shares. Evidence: FY1990 December-FYE linked firms
--   (n=3,358) have median annual turnover 0.37 with vol*100 vs 0.004 without
--   (0.004 = 0.4%/yr is implausibly low for the broad Compustat universe). The
--   factor 100 is a constant across firms, so tercile ASSIGNMENT (the only thing
--   Table 5 Panel B uses) is identical with or without it; it is applied so the
--   reported turnover is economically meaningful.
-- Notes: avg() over the traded months = average shares outstanding over the
--        months with data; n_months = # traded month-ends in the window (12 for
--        a fully-listed year). HAVING n_months >= 1 keeps any firm-year with at
--        least one traded month (main.py reports the n_months distribution).
-- Settings: join_algorithm=partial_merge, max_execution_time=600, max_rows_to_read=10e9

WITH fm AS (
    SELECT u.gvkey AS gvkey, u.fyear AS fyear,
           toFloat64(m.vol) AS vol, toFloat64(m.shrout) AS shrout
    FROM write_yeye.{src_table} AS u
    INNER JOIN crsp_202601.msf AS m
            ON m.permno = u.permno
    WHERE m.date >= '{msf_start}' AND m.date <= '{msf_end}'
      AND m.vol IS NOT NULL AND m.shrout IS NOT NULL AND m.shrout > 0
      AND toDate(parseDateTimeBestEffort(m.date)) >= addMonths(toStartOfMonth(u.datadate), -11)
      AND toDate(parseDateTimeBestEffort(m.date)) <= u.datadate
)
SELECT gvkey, fyear,
       sum(vol) * 100 / avg(shrout * 1000) AS turnover,
       count() AS n_months
FROM fm
GROUP BY gvkey, fyear
HAVING n_months >= 1
ORDER BY gvkey, fyear
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
