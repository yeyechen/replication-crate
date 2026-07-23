-- diag_divyld_splitadj.sql
-- DIAGNOSTIC ONLY (task B2). Cash-dividend detail (distcd 1000-1999,
-- divamt non-null) 1963-1996 with CRSP cumulative price-adjustment
-- factors, one row per distribution.
-- Attribution date = paydt, falling back to exdt (same as canonical
-- divyld_annual.sql).
-- cfacpr_at  : cfacpr from dsf at the attr date; ASOF LEFT JOIN picks the
--              nearest PRIOR dsf day within the same calendar year when no
--              dsf row exists exactly at attr_dt (carry-forward fallback).
--              Rows with no dsf row at all in the year up to attr_dt get
--              cfacpr_at = NULL (counted downstream).
-- cfacpr_end : cfacpr on the last dsf trading day of the year (argMax by
--              date; cfacpr > 0 guard drops the 10 zero-cfacpr rows in
--              1963-1996).
-- cf_ratio   : cfacpr_end / cfacpr_at. Vintage check: cfacpr DECREASES at
--              splits (IBM 41.75 -> 20.87 at the 1968 2:1 split), so
--              divamt * cf_ratio converts the per-share dividend from
--              units-at-attr-date into year-end share units (ratio <= 1
--              when a split occurs between attr_dt and year-end).
-- B2 yield downstream: 100 * sum(divamt * cf_ratio) / |prc_end|.
-- Tables: crsp_202601.dsedist, crsp_202601.dsf
-- Output columns: permno, y, attr_dt, divamt, cfacpr_at, cf_exact,
--                 cfacpr_end, cf_ratio
WITH attributed AS (
    SELECT
        permno,
        multiIf(
            paydt IS NOT NULL AND paydt != '', paydt,
            exdt  IS NOT NULL AND exdt  != '', exdt,
            ''
        ) AS attr_dt,
        divamt
    FROM crsp_202601.dsedist
    WHERE distcd BETWEEN 1000 AND 1999
      AND divamt IS NOT NULL
),
attr AS (
    SELECT
        permno,
        toDate32(attr_dt)      AS attr_d32,
        toYear(toDate32(attr_dt)) AS y,
        divamt
    FROM attributed
    WHERE attr_dt >= '1963-01-01' AND attr_dt <= '1996-12-31'
),
cf AS (
    SELECT
        permno,
        toDate32(date)            AS dt,
        toYear(toDate32(date))    AS y,
        cfacpr
    FROM crsp_202601.dsf
    WHERE date >= '1963-01-01' AND date <= '1996-12-31'
      AND cfacpr > 0
),
cf_end AS (
    SELECT permno, y, argMax(cfacpr, dt) AS cfacpr_end
    FROM cf
    GROUP BY permno, y
),
joined AS (
    SELECT
        a.permno    AS permno,
        a.attr_d32  AS attr_d32,
        a.y         AS y,
        a.divamt    AS divamt,
        cf.cfacpr   AS cfacpr_at,
        cf.dt       AS cf_dt
    FROM attr AS a
    ASOF LEFT JOIN cf
        ON a.permno = cf.permno
       AND a.y = cf.y
       AND a.attr_d32 >= cf.dt
)
SELECT
    j.permno                                       AS permno,
    j.y                                            AS y,
    j.attr_d32                                     AS attr_dt,
    j.divamt                                       AS divamt,
    j.cfacpr_at                                    AS cfacpr_at,
    (j.cf_dt = j.attr_d32)                         AS cf_exact,
    e.cfacpr_end                                   AS cfacpr_end,
    if(j.cfacpr_at IS NOT NULL AND e.cfacpr_end IS NOT NULL,
       e.cfacpr_end / j.cfacpr_at, NULL)           AS cf_ratio
FROM joined AS j
LEFT JOIN cf_end AS e ON j.permno = e.permno AND j.y = e.y
ORDER BY j.permno, j.y, j.attr_d32
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
