-- diag_cfacpr_yearend.sql
-- DIAGNOSTIC ONLY (task B split-event fraction). First/last cfacpr of
-- each (permno, y) for the NYSE common-stock PIT universe (shrcd 10/11,
-- hexcd 1 via dsfhdr — same universe as characteristics_annual.sql),
-- y = 1963..1996. A within-year cfacpr change (cf_start != cf_end) flags
-- a split/stock-dividend event during the year.
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr
-- Output columns: permno, y, cf_start, cf_end, n_cf_days
WITH univ AS (
    SELECT
        d.permno         AS permno,
        toDate32(d.date) AS date32,
        d.cfacpr         AS cfacpr
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hshrcd IN (10, 11)
      AND h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1996-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
      AND d.cfacpr > 0
)
SELECT
    permno,
    toYear(date32)          AS y,
    argMin(cfacpr, date32)  AS cf_start,
    argMax(cfacpr, date32)  AS cf_end,
    count()                 AS n_cf_days
FROM univ
GROUP BY permno, y
ORDER BY permno, y
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
