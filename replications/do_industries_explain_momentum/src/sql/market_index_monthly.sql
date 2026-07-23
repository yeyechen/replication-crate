-- market_index_monthly.sql
-- Purpose: CRSP monthly market index returns (value-weighted and
--          equal-weighted, with dividends) for 1962-01 .. 1995-07.
--          Merged onto the panel by YEAR-MONTH as vw_mkt / ew_mkt
--          (msi.date = calendar month end, msf.date = last trading day).
-- Tables: crsp_202601.msi
-- Output columns: date (month-end), vw_mkt, ew_mkt
-- Depends on: (none)
-- Settings: max_execution_time=60
SELECT
    toDate32(date) AS date,
    CAST(vwretd AS Nullable(Float64)) AS vw_mkt,
    CAST(ewretd AS Nullable(Float64)) AS ew_mkt
FROM crsp_202601.msi
WHERE toDate32(date) >= toDate32('1962-01-01')
  AND toDate32(date) <= toDate32('1995-07-31')
SETTINGS max_execution_time = 60,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0
