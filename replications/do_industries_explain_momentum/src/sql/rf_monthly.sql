-- rf_monthly.sql
-- Purpose: monthly risk-free rate (3-month T-bill) from the Fama-French
--          four-factor file, 1962-01 .. 1995-07. Merged onto the panel by
--          YEAR-MONTH as rf (ff.dt is the calendar month end while msf.date
--          is the last trading day — exact-date merges would fail for ~30%
--          of months); exret = ret - rf. Cast to Float64 in case the ff
--          table stores Decimals.
-- Tables: ff.four_factor_monthly
-- Output columns: date (month-end), rf
-- Depends on: (none)
-- Settings: max_execution_time=60
SELECT
    toDate32(dt) AS date,
    CAST(rf AS Nullable(Float64)) AS rf
FROM ff.four_factor_monthly
WHERE toDate32(dt) >= toDate32('1962-01-01')
  AND toDate32(dt) <= toDate32('1995-07-31')
SETTINGS max_execution_time = 60,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0
