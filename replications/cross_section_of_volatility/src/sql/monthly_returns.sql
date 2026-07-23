-- monthly_returns.sql
-- Purpose: PIT-filtered monthly returns, market equity, size, and momentum
--   for the AHXZ (2006) idiosyncratic-volatility panel. One row per
--   (permno, month). Anchors the final panel (every valid monthly return).
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, month, ret, me, hexcd, size, mom
-- Depends on: (none)
-- Conventions:
--   * Universe (A3): PIT join dsenames namedt<=date<=nameendt,
--     shrcd IN (10,11), exchcd IN (1,2,3). CRSP missing-return sentinels
--     dropped via ret > -1.0.
--   * me = abs(prc) * shrout / 1000  (market equity in $ MILLIONS; prc is
--     signed so abs(); shrout is in thousands of shares).
--   * size = log(me in millions).
--   * mom = cumret(t-12 .. t-2) = exp(sum_{t-12..t-2} log(1+ret)) - 1,
--     via a window function. msf is pulled from 1962-01-01 so momentum is
--     defined starting at the first panel month (1963-06).
--   * Timing (A8): all values contemporaneous at month t; the analysis
--     code lags signals by one month before pairing with forward returns.
--   * Panel output window: 1963-06 .. 2000-12 (A9: June 1963 is the first
--     formation month so the first holding return is July 1963).

WITH msf_u AS (
    SELECT
        m.permno                                                  AS permno,
        toDate32(date_trunc('month', toDate32(m.date)))           AS month,
        toFloat64(m.ret)                                          AS ret,
        abs(toFloat64(m.prc)) * toFloat64(m.shrout) / 1000.0      AS me,
        toInt32(m.hexcd)                                          AS hexcd
    FROM crsp_202601.msf AS m
    INNER JOIN crsp_202601.dsenames AS n
        ON m.permno = n.permno
       AND m.date >= n.namedt
       AND m.date <= ifNull(n.nameendt, '2099-12-31')
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND m.ret IS NOT NULL
      AND m.ret > -1.0
      AND m.date BETWEEN '1962-01-01' AND '2000-12-31'
),
msf_feat AS (
    SELECT
        permno,
        month,
        ret,
        me,
        hexcd,
        log(nullIf(me, 0))                                        AS size,
        exp(sum(log(1 + ret)) OVER (
            PARTITION BY permno ORDER BY month
            ROWS BETWEEN 12 PRECEDING AND 2 PRECEDING
        )) - 1.0                                                  AS mom
    FROM msf_u
)
SELECT
    permno,
    month,
    ret,
    me,
    hexcd,
    size,
    mom
FROM msf_feat
WHERE month BETWEEN toDate32('1963-06-01') AND toDate32('2000-12-01')
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
