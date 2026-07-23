-- milliq_open_monthly.sql
-- Purpose: Monthly market illiquidity MILLIQ_open_m, 1963-01 .. 1996-12,
--          over the OPEN universe (§3.3 diagnostic, Task A): for each
--          day d of month m, average |R_idm|/VOLD_idm across ALL NYSE
--          common stocks trading that day — NO admission filters
--          (no >200-day / >$5 / year-end listing criteria), NO tail
--          exclusions; then average the daily cross-sectional means
--          over the trading days of m; x1e6 scaling (same as the
--          admitted-universe MILLIQ in milliq_monthly.sql).
-- Universe: hshrcd IN (10,11), hexcd = 1, point-in-time via dsfhdr
--          begdat/enddat (same PIT pattern as milliq_monthly.sql).
-- Valid stock-day: ret non-null AND ret > -1 (drops missing sentinels)
--          AND vol > 0 AND |prc| > 0. |R|/VOLD = |ret|/(|prc|*vol).
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr
-- Output columns: month (Date32 first-of-month), milliq (x1e6),
--                 n_days (trading days with a valid cross-section),
--                 n_stocks (distinct stocks with >=1 valid stock-day
--                 in the month)
-- Depends on: (none)
-- Note: toDate32 everywhere (Date saturates pre-1970).
WITH univ AS (
    SELECT
        d.permno         AS permno,
        toDate32(d.date) AS date32,
        abs(d.ret) / (abs(d.prc) * d.vol) AS illiq_d
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hshrcd IN (10, 11)
      AND h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1996-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
      AND d.ret IS NOT NULL AND d.ret > -1
      AND d.vol IS NOT NULL AND d.vol > 0
      AND abs(d.prc) > 0
),
day_rows AS (
    SELECT
        -- month built from string parts: toStartOfMonth() returns Date,
        -- which saturates pre-1970 dates to 1970-01-01
        toDate32(concat(toString(toYear(date32)), '-',
                 leftPad(toString(toMonth(date32)), 2, '0'),
                 '-01'))         AS month,
        date32                   AS date32,
        permno                   AS permno,
        illiq_d                  AS illiq_d
    FROM univ
),
day_agg AS (
    SELECT month, date32, avg(illiq_d) AS cs_mean
    FROM day_rows
    GROUP BY month, date32
),
stock_agg AS (
    SELECT month, uniqExact(permno) AS n_stocks
    FROM day_rows
    GROUP BY month
)
SELECT
    d.month                 AS month,
    1e6 * avg(d.cs_mean)    AS milliq,
    count()                 AS n_days,
    any(s.n_stocks)         AS n_stocks
FROM day_agg AS d
INNER JOIN stock_agg AS s ON d.month = s.month
GROUP BY d.month
ORDER BY d.month
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
