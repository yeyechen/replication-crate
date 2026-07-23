-- diag_div_coverage.sql
-- DIAGNOSTIC ONLY (task C). Cash-dividend counts per (permno, y),
-- y = 1990..1996, distcd 1000-1999, divamt non-null. Attribution date =
-- paydt, fallback exdt (same convention as divyld_annual.sql).
-- Downstream: merged with the admitted sample to report payer fraction
-- and mean dividend count among payers.
-- Tables: crsp_202601.dsedist
-- Output columns: permno, y, n_div
WITH attributed AS (
    SELECT
        permno,
        multiIf(
            paydt IS NOT NULL AND paydt != '', paydt,
            exdt  IS NOT NULL AND exdt  != '', exdt,
            ''
        ) AS attr_dt
    FROM crsp_202601.dsedist
    WHERE distcd BETWEEN 1000 AND 1999
      AND divamt IS NOT NULL
)
SELECT
    permno,
    toYear(toDate32(attr_dt)) AS y,
    count()                   AS n_div
FROM attributed
WHERE attr_dt >= '1990-01-01' AND attr_dt <= '1996-12-31'
GROUP BY permno, y
ORDER BY permno, y
SETTINGS max_execution_time = 300
