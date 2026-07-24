-- crsp_monthly.sql
-- Purpose: Novy-Marx (2013) monthly universe — PIT-filtered returns with
--          market equity, plus r_{1,0} (short-term reversal) and
--          r_{12,2} (momentum) computed as window functions.
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, ret, me, prc, hexcd, hsiccd,
--                 r_1_0, r_12_2
-- Depends on: (none)
-- Notes:
--   * Universe (PIT via dsenames namedt/nameendt windows):
--     shrcd IN (10,11), exchcd IN (1,2,3), financials excluded
--     (siccd 6000-6999; NULL siccd kept — unknown industry).
--   * me = abs(prc) * shrout * 1000  — DOLLARS (prc is signed; shrout is
--     in thousands of shares).
--   * CRSP missing-return sentinels (< -1, e.g. -88.0) set to NULL; a
--     valid return of exactly -1 (total loss) is kept.
--   * r_1_0 = ret(t-1); NULL unless the prior row is the prior calendar
--     month (guards against gaps in the msf record).
--   * r_12_2 = prod(1 + ret[t-12 .. t-2]) - 1; requires all 11 months
--     non-missing AND contiguous in calendar time.
--   * Starts 1962-01 so the June/July 1963 lags are fully populated
--     (r_12_2 at June 1963 needs returns back to June 1962).
SELECT
    permno,
    month,
    ret,
    me,
    prc,
    hexcd,
    hsiccd,
    if(dateDiff('month', lagInFrame(month, 1) OVER w_all, month) = 1,
       lagInFrame(ret, 1) OVER w_all,
       NULL)                                    AS r_1_0,
    if(count(ret) OVER w12 = 11
       AND dateDiff('month', first_value(month) OVER w12, month) = 12,
       exp(sum(log(1 + ret)) OVER w12) - 1,
       NULL)                                    AS r_12_2
FROM
(
    SELECT
        m.permno                                AS permno,
        -- month start as Date32 (`Date` clamps pre-1970 dates to
        -- 1970-01-01, so toStartOfMonth(toDate(...)) is NOT usable here)
        makeDate32(toYear(toDate32(m.date)), toMonth(toDate32(m.date)), 1)
                                                AS month,
        if(m.ret >= -1.0, m.ret, NULL)          AS ret,
        if(abs(m.prc) > 0 AND m.shrout > 0,
           abs(m.prc) * m.shrout * 1000, NULL)  AS me,
        abs(m.prc)                              AS prc,
        m.hexcd                                 AS hexcd,
        m.hsiccd                                AS hsiccd
    FROM crsp_202601.msf AS m
    INNER JOIN crsp_202601.dsenames AS n
        ON (m.permno = n.permno)
       AND (m.date >= n.namedt)
       AND (m.date <= ifNull(n.nameendt, '2099-12-31'))
    WHERE m.date >= '1962-01-01'
      AND m.date <= '2010-12-31'
      AND m.permno IS NOT NULL
      AND n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND (n.siccd IS NULL OR intDiv(n.siccd, 1000) != 6)
)
WINDOW
    w_all AS (PARTITION BY permno ORDER BY month
              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
    w12   AS (PARTITION BY permno ORDER BY month
              ROWS BETWEEN 12 PRECEDING AND 2 PRECEDING)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
