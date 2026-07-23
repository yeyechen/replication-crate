-- ewretd_monthly.sql
-- Purpose: Monthly CRSP equal-weighted market return WITH dividends (EWRETD),
--   in decimal. Used to impute missing monthly stock returns inside the
--   holding-period windows (paper: after a stock delists / when a monthly
--   return is missing, invest the remaining value in the CRSP EW index).
--   midx is epoch-proof (see msf_monthly_base.sql). max() collapses the
--   (single) monthly row safely.
-- Paper: §I Returns (L116) "replacing the missing stock return with ... EWRETD".
-- Tables: crsp_202601.msi
-- Output columns: midx, ewretd
-- Depends on: (none)
SELECT
    toYear(toDate32(date)) * 12 + (toMonth(toDate32(date)) - 1) AS midx,
    max(ewretd) AS ewretd
FROM crsp_202601.msi
WHERE date >= '1926-12-01' AND date <= '2006-12-31'
GROUP BY midx
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
