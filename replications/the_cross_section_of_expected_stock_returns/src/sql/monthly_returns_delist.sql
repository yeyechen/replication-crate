-- monthly_returns_delist.sql
-- Purpose: monthly stock returns with the delisting adjustment (binding
--          Assumption 5). For each (permno, month):
--            1) msf.ret if valid (not NULL, > -1.0, not a CRSP missing-return
--               sentinel); else
--            2) msedelist.dlret if the stock delisted that month and dlret is
--               valid (not NULL, > -1.0, not in {-44,-55,-66,-77,-88,-99});
--               else (dlret missing)
--            3) -0.30 if dlstcd BETWEEN 500 AND 599 (performance delisting);
--            4)  0.00 if dlstcd BETWEEN 200 AND 399 (merger/exchange);
--            5) NULL otherwise.
--          All monthly CRSP sentinels (-44/-55/-66/-77/-88/-99) are < -1.0,
--          so `ret > -1.0` excludes them; the explicit NOT IN list documents
--          the exclusion and also catches any daily-style sentinels.
-- Tables: crsp_202601.msf, crsp_202601.msedelist
-- Output columns:
--   permno Int32
--   ym     UInt32 month key YYYYMM
--   mdate  Nullable(String) month-end msf date (NULL for pure delisting months
--          with no msf record)
--   ret    Nullable(Float64) delisting-adjusted monthly return (decimal)
-- Window: ym 195807 .. 199106 (pre-ranking windows start July 1958 for
--         formation year 1963; final holding month is June 1991).
-- Depends on: (none)
-- Note: no universe filter here — delisting-adjusted returns are needed for
--       every permno (universe/qualification applied downstream in Python).
--       One msf row per (permno, month) verified (0 duplicates 1963-1991);
--       argMax(..., date) is a safety net. Same for msedelist per
--       (permno, month of dlstdt).
WITH msf_m AS (
    SELECT
        assumeNotNull(permno)      AS permno,
        toYYYYMM(toDate32(date))   AS ym,
        max(date)                  AS mdate,
        argMax(ret, date)          AS ret
    FROM crsp_202601.msf
    WHERE date >= '1958-06-01' AND date <= '1991-07-31'
      AND permno IS NOT NULL
    GROUP BY permno, ym
),
dl AS (
    SELECT
        assumeNotNull(permno)        AS permno,
        toYYYYMM(toDate32(dlstdt))   AS ym,
        argMax(dlstcd, dlstdt)       AS dlstcd,
        argMax(dlret, dlstdt)        AS dlret
    FROM crsp_202601.msedelist
    WHERE dlstdt >= '1958-06-01' AND dlstdt <= '1991-07-31'
      AND dlstdt IS NOT NULL AND dlstdt != ''
      AND permno IS NOT NULL
    GROUP BY permno, ym
),
grid AS (
    SELECT permno, ym FROM msf_m
    UNION DISTINCT
    SELECT permno, ym FROM dl
)
SELECT
    g.permno AS permno,
    g.ym     AS ym,
    m.mdate  AS mdate,
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
WHERE g.ym BETWEEN 195807 AND 199106
SETTINGS join_algorithm = 'partial_merge', max_execution_time = 900;
