-- first_valid_month.sql
-- Purpose: First month (as integer midx) each permno appears in msf with a
--   NON-MISSING return. Feeds the listing-age inclusion rule: a security
--   enters the cross-section at month t only if t - first_midx >= 6 months
--   (paper: "in the CRSP database for at least 6 months").
--   midx = year*12 + (month-1) is epoch-proof (see msf_monthly_base.sql).
-- Paper: §I Sample (L51).
-- Tables: crsp_202601.msf
-- Output columns: permno, first_midx
-- Depends on: (none)  [same source/filter as msf_monthly_base.sql]
SELECT
    permno,
    min(toYear(toDate32(date)) * 12 + (toMonth(toDate32(date)) - 1)) AS first_midx
FROM crsp_202601.msf
WHERE date >= '1926-12-01' AND date <= '2006-12-31'
  AND permno IS NOT NULL
  AND ret IS NOT NULL AND ret > -1.0   -- nonmissing return (sentinels excluded)
GROUP BY permno
SETTINGS max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
