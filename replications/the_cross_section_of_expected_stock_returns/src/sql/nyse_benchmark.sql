-- nyse_benchmark.sql
-- Purpose: monthly delisting-adjusted returns and month-end market equity (ME)
--          for NYSE common stocks (PIT exchcd = 1, shrcd 10/11), July 1963 -
--          December 1990. Feeds the Table VI NYSE VW/EW benchmark returns
--          (paper L2039/L2065: "the value-weighted and equal-weighted (VW and
--          EW) portfolios of NYSE stocks"), computed in Python
--          (src/table_3_6.py) as:
--            EW_t = mean of valid returns over NYSE common stocks in month t;
--            VW_t = sum(ME_{t-1} * ret_t) / sum(ME_{t-1}) over stocks with a
--                   valid ret_t and a valid lagged ME (binding Assumption 10).
--          The delisting-adjusted return logic is identical to
--          src/sql/monthly_returns_delist.sql (binding Assumption 5); ME =
--          abs(prc)*shrout*1000 dollars, identical to me_formation.sql.
--          NYSE membership is point-in-time: the dsenames record whose
--          validity window [namedt, nameendt] covers the calendar month-end
--          date of each month (same PIT-window convention as
--          universe_pit_june.sql). Financials are NOT excluded — the paper's
--          benchmark is the NYSE market (consistent with the Sort-A NYSE
--          breakpoint universe, iteration-1 flag 1). Stocks that delist
--          mid-month carry no month-end membership record and are excluded
--          from that month's benchmark (documented in table_3_6.py).
-- Tables: crsp_202601.dsenames, crsp_202601.msf, crsp_202601.msedelist
-- Output columns:
--   permno Int32
--   ym     UInt32 month key YYYYMM, 196306..199012 (331 months; the June 1963
--          row supplies the first lagged VW weight for July 1963)
--   ret    Nullable(Float64) delisting-adjusted monthly return (decimal)
--   me     Nullable(Float64) month-end market equity (dollars)
-- Depends on: (none)
-- Note: msf has one row per (permno, month) in this extract (verified in the
--       monthly_returns_delist.sql header); argMax(..., date) is a safety
--       net. Same for msedelist per (permno, month of dlstdt).
WITH months AS (
    SELECT
        toYYYYMM(addMonths(toDate32('1963-06-01'), number))     AS ym,
        toString(addMonths(toDate32('1963-07-01'), number) - 1) AS m_end
    FROM numbers(331)
),
nyse AS (
    SELECT m.ym AS ym, assumeNotNull(n.permno) AS permno
    FROM months AS m
    CROSS JOIN crsp_202601.dsenames AS n
    WHERE n.permno IS NOT NULL
      AND n.namedt IS NOT NULL AND n.namedt != ''
      AND n.namedt <= m.m_end
      AND (n.nameendt IS NULL OR n.nameendt = '' OR n.nameendt >= m.m_end)
      AND n.namedt <= '1990-12-31'
      AND (n.nameendt IS NULL OR n.nameendt = '' OR n.nameendt >= '1963-06-30')
      AND n.shrcd IN (10, 11)
      AND n.exchcd = 1
    GROUP BY m.ym, n.permno
),
msf_m AS (
    SELECT
        assumeNotNull(permno)    AS permno,
        toYYYYMM(toDate32(date)) AS ym,
        argMax(prc, date)        AS prc,
        argMax(shrout, date)     AS shrout,
        argMax(ret, date)        AS ret
    FROM crsp_202601.msf
    WHERE date >= '1963-06-01' AND date <= '1991-01-31'
      AND permno IS NOT NULL
    GROUP BY permno, ym
),
dl AS (
    SELECT
        assumeNotNull(permno)      AS permno,
        toYYYYMM(toDate32(dlstdt)) AS ym,
        argMax(dlstcd, dlstdt)     AS dlstcd,
        argMax(dlret, dlstdt)      AS dlret
    FROM crsp_202601.msedelist
    WHERE dlstdt >= '1963-06-01' AND dlstdt <= '1990-12-31'
      AND dlstdt IS NOT NULL AND dlstdt != ''
      AND permno IS NOT NULL
    GROUP BY permno, ym
),
grid AS (
    SELECT permno, ym FROM msf_m WHERE ym BETWEEN 196306 AND 199012
    UNION DISTINCT
    SELECT permno, ym FROM dl WHERE ym BETWEEN 196306 AND 199012
),
rets AS (
    SELECT
        g.permno AS permno,
        g.ym     AS ym,
        multiIf(
            -- 1) valid msf return
            m.ret IS NOT NULL AND m.ret > -1.0
                AND m.ret NOT IN (-44, -55, -66, -77, -88, -99),
            m.ret,
            -- 2) valid delisting return (dlret sentinels are all < -1.0)
            d.dlret IS NOT NULL AND d.dlret > -1.0
                AND d.dlret NOT IN (-44, -55, -66, -77, -88, -99),
            d.dlret,
            -- dlret missing/invalid: impute by delisting-code category
            d.permno IS NOT NULL,
            multiIf(
                d.dlstcd BETWEEN 500 AND 599, toNullable(toFloat64(-0.30)),
                d.dlstcd BETWEEN 200 AND 399, toNullable(toFloat64(0.0)),
                CAST(NULL, 'Nullable(Float64)')
            ),
            -- no msf return and no delisting record
            CAST(NULL, 'Nullable(Float64)')
        ) AS ret
    FROM grid AS g
    LEFT JOIN msf_m AS m ON g.permno = m.permno AND g.ym = m.ym
    LEFT JOIN dl    AS d ON g.permno = d.permno AND g.ym = d.ym
),
me AS (
    SELECT
        permno,
        ym,
        if(prc IS NOT NULL AND abs(prc) > 0 AND shrout IS NOT NULL AND shrout > 0,
           abs(prc) * shrout * 1000,
           CAST(NULL, 'Nullable(Float64)')) AS me
    FROM msf_m
    WHERE ym BETWEEN 196306 AND 199012
)
SELECT
    n.ym     AS ym,
    n.permno AS permno,
    r.ret    AS ret,
    e.me     AS me
FROM nyse AS n
LEFT JOIN rets AS r ON n.permno = r.permno AND n.ym = r.ym
LEFT JOIN me   AS e ON n.permno = e.permno AND n.ym = e.ym
SETTINGS join_algorithm = 'partial_merge', max_execution_time = 900;
