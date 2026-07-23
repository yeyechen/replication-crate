-- 05_universe_monthly.sql
-- Purpose: point-in-time monthly universe (Step 3). CRSP msf ASOF-joined
--          to dsenames: ASOF picks the name record with the latest
--          namedt <= month-end date; the WHERE clause then enforces
--          date <= nameendt, giving exact namedt <= date <= nameendt
--          PIT semantics (ClickHouse does not support two-sided range
--          inequalities in JOIN ON). Filtered to common stocks
--          shrcd IN (10,11) excluding OTC (exchcd NOT IN (0)).
--          Window starts 1952-01 so the 60-month rolling beta has history
--          before the paper's June-1957 first date; ends 2017-01 so the
--          Dec-2016 signal row can be paired with its Jan-2017 return.
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output: write_yeye.qmj_univ_m — permno (Int32), month (Date, month
--         start), date (month-end Date), ret (sentinels > -1 only),
--         mcap (|prc|*shrout*1000, dollars), hexcd_eom, shrcd, exchcd
-- Depends on: (none)
-- Paper: "Common stocks are identified by a CRSP share code (SHRCD) of 10
--         or 11 ... We also drop stocks traded on over-the-counter (OTC)
--         exchanges." (L332). OTC = exchcd 0.
-- Note: msf ret has no sentinel rows (< -1.0) in this vintage (verified);
--       a ret > -1.0 guard is kept anyway. NULL exchcd treated as
--       non-universe (conservative).

CREATE OR REPLACE TABLE write_yeye.qmj_univ_m
ENGINE = MergeTree ORDER BY (permno, month) AS
WITH
m AS (
    SELECT
        assumeNotNull(permno)            AS permno,
        subtractDays(assumeNotNull(toDate32(date)), toDayOfMonth(assumeNotNull(toDate32(date))) - 1) AS month,
        assumeNotNull(toDate32(date))      AS date,
        if(ret > -1.0, ret, NULL)        AS ret,
        if(prc IS NULL OR prc = 0 OR shrout IS NULL,
           NULL,
           abs(prc) * shrout * 1000)     AS mcap,
        hexcd
    FROM crsp_202601.msf
    WHERE date >= '1952-01-01' AND date <= '2017-01-31'
      AND permno IS NOT NULL AND date IS NOT NULL
),
n AS (
    SELECT
        assumeNotNull(permno)           AS permno,
        assumeNotNull(toDate32(namedt))   AS namedt,
        ifNull(toDate32(nameendt), toDate32('2099-12-31')) AS nameendt,
        shrcd,
        exchcd
    FROM crsp_202601.dsenames
    WHERE shrcd IN (10, 11)
      AND exchcd IS NOT NULL
      AND exchcd NOT IN (0)
      AND permno IS NOT NULL
      AND namedt IS NOT NULL
)
SELECT
    m.permno      AS permno,
    m.month       AS month,
    any(m.date)   AS date,
    any(m.ret)    AS ret,
    any(m.mcap)   AS mcap,
    any(m.hexcd)  AS hexcd_eom,
    any(n.shrcd)  AS shrcd,
    any(n.exchcd) AS exchcd
FROM m
ASOF INNER JOIN n
    ON m.permno = n.permno
   AND n.namedt <= m.date
WHERE m.date <= n.nameendt
GROUP BY m.permno, m.month
SETTINGS allow_experimental_analyzer = 0,
         join_algorithm = 'hash',   -- required for ASOF joins on this server
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
