-- coercion_counts.sql
-- Purpose: Diagnostic for Assumption A6's "NULL monthly rets -> 0" rule. Counts,
--          over the holding-window months (May 1968 .. April 1994) and across all
--          stocks that ever appear in an April-formation or December (prior-year)
--          universe: (a) msf rows with ret IS NULL, (b) msf rows whose ret is a
--          missing-return sentinel (< -1.0, e.g. -55/-66/-88/-99), and (c) total
--          msf rows. Rows in (a)+(b) are treated as missing and coalesced to the
--          delisting return (if the delisting falls in that month) else 0.
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: n_msf_null, n_msf_sentinel, n_msf_total
-- Depends on: (none; universe CTEs inlined)
WITH formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
dec_dates AS (
    SELECT toUInt32(substring(date, 1, 4)) + 1 AS fy, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12' AND date >= '1967-12-01' AND date <= '1988-12-31'
    GROUP BY substring(date, 1, 4)
),
univ_permno AS (
    SELECT DISTINCT permno FROM (
        SELECT n.permno AS permno
        FROM crsp_202601.dsenames AS n CROSS JOIN formation AS f
        WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
          AND n.namedt <= '1989-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
          AND n.namedt <= f.form_date AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
        UNION ALL
        SELECT n.permno AS permno
        FROM crsp_202601.dsenames AS n CROSS JOIN dec_dates AS d
        WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
          AND n.namedt <= '1988-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
          AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
    )
)
SELECT
    countIf(m.ret IS NULL)  AS n_msf_null,
    countIf(m.ret < -1.0)   AS n_msf_sentinel,
    count()                 AS n_msf_total
FROM crsp_202601.msf AS m
INNER JOIN univ_permno AS u ON u.permno = m.permno
WHERE m.date >= '1968-05-01' AND m.date <= '1994-04-30'
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
