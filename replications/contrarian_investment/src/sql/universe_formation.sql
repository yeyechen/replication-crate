-- universe_formation.sql
-- Purpose: Point-in-time NYSE/AMEX common-stock universe at each of the 22 annual
--          formation dates (last trading day of April, 1968..1989). One row per
--          (formation year, permno).
--          Assumption A1: shrcd IN (10,11) (ordinary common shares),
--          exchcd IN (1,2) (NYSE, AMEX; NASDAQ excluded), applied point-in-time
--          via dsenames intervals active at the formation date
--          (namedt <= form_date AND nameendt >= form_date).
-- Tables: crsp_202601.msf (formation dates), crsp_202601.dsenames (PIT codes)
-- Output columns: fy, form_date, permno
-- Depends on: formation_dates.sql (formation CTE replicated inline for standalone use)
WITH formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30'
      AND substring(date, 6, 2) = '04'
    GROUP BY fy
)
-- Implementation: the PIT condition (namedt <= form_date AND nameendt >=
-- form_date) is a pure interval-overlap with NO equality key, so hash/partial
-- merge joins cannot be used. `formation` is only 22 rows, so a CROSS JOIN with
-- the interval predicate in WHERE (22 x ~118k comparisons) is exact and cheap.
-- Validated 2026-07-22: 2,104 stocks at 1968-04-30 and 1,968 at 1989-04-28
-- (matches Assumption A1 sanity check).
SELECT DISTINCT
    f.fy        AS fy,
    f.form_date AS form_date,
    n.permno    AS permno
FROM crsp_202601.dsenames AS n
CROSS JOIN formation AS f
WHERE n.shrcd IN (10, 11)
  AND n.exchcd IN (1, 2)
  AND n.permno IS NOT NULL
  -- loose pre-filters (do not change result; bound the dsenames scan)
  AND n.namedt <= '1989-12-31'
  AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
  -- point-in-time interval overlap with the formation date
  AND n.namedt <= f.form_date
  AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
