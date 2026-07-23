-- stock_returns_monthly.sql
-- Purpose: Monthly holding returns (delisting return absorbed) for every stock
--          that ever appears in a formation-year universe, over the months
--          needed for the five-year holding windows (May 1968 .. April 1994).
--          Monthly return = coalesce(clean msf.ret, clean dlret in the delisting
--          month, 0)  [Assumption A6]. A stock present in a month (has an msf row,
--          OR delists in that month with no msf row) yields exactly one row; months
--          in which the stock is absent (already delisted / not yet listed) produce
--          no row. Return sentinels (< -1.0, e.g. -55/-66/-88/-99) are treated as
--          missing before the coalesce (per references/CRSP.md).
--          Used by the panel's annual holding-year return computation. This is the
--          RAW stock return series (formation-universe membership), distinct from
--          monthly_returns.sql (the point-in-time-monthly universe used by Table VII).
-- Tables: crsp_202601.msf, crsp_202601.dsenames, crsp_202601.dsedelist
-- Output columns: permno, mnum (= year*12 + month), ret
-- Depends on: universe_formation (universe CTE inlined to derive the permno set)
WITH formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
dec_dates AS (
    -- December t-1 dates (size-decile ranking dates), labelled by formation year t
    SELECT toUInt32(substring(date, 1, 4)) + 1 AS fy, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12' AND date >= '1967-12-01' AND date <= '1988-12-31'
    GROUP BY substring(date, 1, 4)
),
univ_permno AS (
    -- Union of April-formation-universe permnos (panel stocks) and December
    -- (prior-year) universe permnos (size-decile benchmark members), so the return
    -- series covers every stock that can appear in a holding portfolio or a benchmark.
    SELECT DISTINCT permno FROM (
        SELECT n.permno AS permno
        FROM crsp_202601.dsenames AS n
        CROSS JOIN formation AS f
        WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
          AND n.namedt <= '1989-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
          AND n.namedt <= f.form_date AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
        UNION ALL
        SELECT n.permno AS permno
        FROM crsp_202601.dsenames AS n
        CROSS JOIN dec_dates AS d
        WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
          AND n.namedt <= '1988-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
          AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
    )
),
msf_u AS (
    SELECT
        m.permno AS permno,
        toUInt32(substring(m.date, 1, 4)) * 12 + toUInt32(substring(m.date, 6, 2)) AS mnum,
        if(m.ret IS NOT NULL AND m.ret >= -1.0, m.ret, NULL) AS clean_ret
    FROM crsp_202601.msf AS m
    INNER JOIN univ_permno AS u ON u.permno = m.permno
    WHERE m.date >= '1963-05-01' AND m.date <= '1994-04-30'
),
delist AS (
    SELECT
        e.permno AS permno,
        toUInt32(substring(e.dlstdt, 1, 4)) * 12 + toUInt32(substring(e.dlstdt, 6, 2)) AS dl_mnum,
        if(e.dlret IS NOT NULL AND e.dlret >= -1.0, e.dlret, NULL) AS clean_dlret
    FROM crsp_202601.dsedelist AS e
    INNER JOIN univ_permno AS u ON u.permno = e.permno
    WHERE e.dlstdt >= '1963-05-01' AND e.dlstdt <= '1994-04-30' AND e.dlstdt IS NOT NULL
),
present_msf AS (
    -- months with an msf row: absorb dlret if the delisting falls in that month
    SELECT m.permno AS permno, m.mnum AS mnum,
        coalesce(m.clean_ret, d.clean_dlret, 0) AS ret
    FROM msf_u AS m
    LEFT JOIN delist AS d ON d.permno = m.permno AND d.dl_mnum = m.mnum
),
msf_months AS (
    SELECT DISTINCT permno, mnum FROM msf_u
),
delist_only AS (
    -- delisting month with NO msf row: the stock still earns coalesce(dlret, 0)
    SELECT d.permno AS permno, d.dl_mnum AS mnum,
        coalesce(d.clean_dlret, 0) AS ret
    FROM delist AS d
    LEFT JOIN msf_months AS mm ON mm.permno = d.permno AND mm.mnum = d.dl_mnum
    WHERE mm.permno IS NULL
)
SELECT permno, mnum, ret FROM present_msf
UNION ALL
SELECT permno, mnum, ret FROM delist_only
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
