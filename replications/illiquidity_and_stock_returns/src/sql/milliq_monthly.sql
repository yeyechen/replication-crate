-- milliq_monthly.sql
-- Purpose: Monthly market illiquidity MILLIQ_m, 1963-01 .. 1996-12
--          (Amihud 2002 §3.3, Assumption 5):
--          for each day d of month m, average |R_idm|/VOLD_idm across
--          the stocks admitted to the sample in the calendar year
--          containing m (criteria i-iv of that year); then average the
--          daily cross-sectional means over the trading days of m;
--          x1e6 scaling (same as annual ILLIQ).
-- Valid stock-day: ret non-null AND ret > -1 (drops missing sentinels)
--          AND vol > 0 AND |prc| > 0. |R|/VOLD = |ret|/(|prc|*vol).
-- Admission set is provided by main.py via session temp table
--          _amihud_adm(permno, y).
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr, session temp _amihud_adm
-- Output columns: month (Date32 first-of-month), milliq (x1e6),
--                 n_days (trading days with a valid cross-section),
--                 n_stocks (distinct admitted stocks with >=1 valid
--                 stock-day in the month)
-- Depends on: temp table _amihud_adm (permno Int32, y Int32)
-- Note: toDate32 everywhere (Date saturates pre-1970).
WITH univ AS (
    SELECT
        d.permno         AS permno,
        toDate32(d.date) AS date32,
        toYear(toDate32(d.date)) AS y,
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
adm_days AS (
    SELECT
        -- month built from string parts: toStartOfMonth() returns Date,
        -- which saturates pre-1970 dates to 1970-01-01
        toDate32(concat(toString(toYear(u.date32)), '-',
                 leftPad(toString(toMonth(u.date32)), 2, '0'),
                 '-01'))         AS month,
        u.date32                 AS date32,
        u.permno                 AS permno,
        u.illiq_d                AS illiq_d
    FROM univ AS u
    INNER JOIN _amihud_adm AS a
        ON u.permno = a.permno AND u.y = a.y
),
day_agg AS (
    SELECT month, date32, avg(illiq_d) AS cs_mean
    FROM adm_days
    GROUP BY month, date32
),
stock_agg AS (
    SELECT month, uniqExact(permno) AS n_stocks
    FROM adm_days
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
