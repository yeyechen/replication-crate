-- daily_panel.sql
-- Purpose: Daily CRSP returns 1963-1987 with last-trading-day-of-month flag
--          for Panel II of Table VI (bid-ask bounce robustness check).
-- Tables: crsp_202601.dsf, crsp_202601.dsenames
-- Output columns: permno, date (Date32), month (Date32), ret, prc,
--                 is_last_trading_day_of_month (UInt8)
-- Depends on: (none)
-- Settings: max_execution_time=900
--
-- "Last trading day of month" is the MAX(date) per (permno, month)
-- where ret is non-null. Filter `ret IS NOT NULL AND ret > -50`
-- excludes the missing-return sentinels (-55, -66, -77, -88, -99) which
-- appear as non-NULL floats per CRSP convention (see CRSP.md).

WITH
  daily_filt AS (
    SELECT
      d.permno                                                AS permno,
      toDate32OrNull(d.date)                                  AS date32,
      toDate32(toDate32OrNull(d.date) - toIntervalDay(dayOfMonth(toDate32OrNull(d.date)) - 1)) AS month,
      d.ret                                                   AS ret,
      d.prc                                                   AS prc
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
      ON d.permno = n.permno
     AND toDate32OrNull(d.date) >= toDate32OrNull(n.namedt)
     AND toDate32OrNull(d.date) <= toDate32OrNull(n.nameendt)
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND toDate32OrNull(d.date) BETWEEN toDate32('1963-01-01') AND toDate32('1987-12-31')
      AND d.ret IS NOT NULL
      AND d.ret > -50
  ),
  with_last AS (
    SELECT
      permno                                                  AS permno,
      date32                                                  AS date32,
      month                                                   AS month,
      ret                                                     AS ret,
      prc                                                     AS prc,
      max(date32) OVER w                                      AS month_max_date
    FROM daily_filt
    WINDOW w AS (PARTITION BY permno, month
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
  permno                                                     AS permno,
  date32                                                     AS date,
  month                                                      AS month,
  ret                                                        AS ret,
  prc                                                        AS prc,
  if(date32 = month_max_date, 1, 0)                          AS is_last_trading_day_of_month
FROM with_last
SETTINGS max_execution_time = 900,
         join_algorithm = 'partial_merge'