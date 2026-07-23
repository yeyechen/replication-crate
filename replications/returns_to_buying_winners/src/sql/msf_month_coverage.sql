-- msf_month_coverage.sql
-- Purpose: DIAGNOSTIC ONLY (PART 0, read-only) — the set of (permno, 'YYYY-MM')
--          stock-months for which crsp_202601.msf has a row with ret IS NOT
--          NULL, over 1965-02 .. 1990-06 (the holding months of the 300 PA 6/6
--          cohorts, formation 1965-01 .. 1989-12 x h=1..6). Used by
--          sell_diagnostic() to test whether partial-month stock-months (those
--          with NO monthly-file record) explain the residual sell-decile
--          shortfall vs the paper. This query feeds the diagnostic ONLY; it
--          does not touch the primary panel or any primary series.
-- Tables: crsp_202601.msf
-- Output columns: permno, month ('YYYY-MM' string — P8: never toDate() pre-1970)
-- Depends on: (none)
SELECT permno, substring(date, 1, 7) AS month
FROM crsp_202601.msf
WHERE date >= '1965-02-01' AND date <= '1990-06-30'
  AND permno IS NOT NULL
  AND ret IS NOT NULL
SETTINGS max_execution_time = 600,
         max_rows_to_read = 20000000,
         timeout_before_checking_execution_speed = 0;
