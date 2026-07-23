-- nyse_daily.sql
-- Purpose: PIT NYSE common-stock daily data for the size-decile benchmark
--          (A8, factor_size_decile_construction). Universe at each date:
--          shrcd IN (10,11) AND exchcd = 1 via dsenames validity windows
--          (namedt <= date <= COALESCE(nameendt,'2100-01-01')). Covers
--          1972-12-01 .. 1982-12-31: Dec-1972 prices are needed for the
--          year-start ME of the 1973 ranking (fallback: first January
--          trading day, applied in Python). NULL-ret rows are kept (needed
--          for ME on the ranking date); ret sentinels are dropped; the EW
--          decile means in Python use non-missing ret only.
-- Tables: crsp_202601.dsf, crsp_202601.dsenames
-- Output columns: permno (Int32), date (Date), ret (Nullable Float64),
--                 prc (Float64), shrout (Float64)
-- Depends on: (none)
SELECT
    d.permno AS permno,
    toDate(d.date) AS date,
    d.ret AS ret,
    d.prc AS prc,
    d.shrout AS shrout
FROM crsp_202601.dsf AS d
INNER JOIN (
    SELECT
        permno,
        toDate(namedt) AS namedt,
        toDate(ifNull(nameendt, '2100-01-01')) AS nameendt
    FROM crsp_202601.dsenames
    WHERE shrcd IN (10, 11)
      AND exchcd = 1
) AS n
  ON d.permno = n.permno
 AND toDate(d.date) >= n.namedt
 AND toDate(d.date) <= n.nameendt
WHERE d.date BETWEEN '1972-12-01' AND '1982-12-31'
  AND d.prc IS NOT NULL AND abs(d.prc) > 0
  AND d.shrout IS NOT NULL AND d.shrout > 0
  AND (d.ret IS NULL OR d.ret > -1.0)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0;
