-- beta.sql
-- Purpose: Compute per-permno monthly beta via 60-month rolling regression
--          of (ret - rf) on mkt_rf, requiring at least 24 months of
--          overlapping observations. Follows Fama-French (1992) convention.
-- Tables:  crsp_202601.msf, crsp_202601.dsenames,
--          ff.five_factor_monthly
-- Output columns: permno, month, beta
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600

WITH
  -- CRSP universe: same filter as panel.sql (shrcd 10/11, exchcd 1/2/3,
  -- non-financial), ret > -1.0.
  crsp_universe AS (
    SELECT
      m.permno,
      toStartOfMonth(toDate32(m.date)) AS month,
      m.ret
    FROM crsp_202601.msf AS m
    INNER JOIN crsp_202601.dsenames AS d
      ON m.permno = d.permno
     AND toDate32(m.date) >= toDate32(d.namedt)
     AND toDate32(m.date) <= ifNull(toDate32(d.nameendt), toDate32('2099-12-31'))
    WHERE toDate32(m.date) BETWEEN toDate32('1976-01-01') AND toDate32('2000-12-31')
      AND d.shrcd IN (10, 11)
      AND d.exchcd IN (1, 2, 3)
      AND (d.siccd < 6000 OR d.siccd >= 7000)
      AND m.ret IS NOT NULL
      AND m.ret > -1.0
  ),

  -- FF factors: convert calendar month-end to start-of-month for joining
  -- with the panel's month column (which is toStartOfMonth(msf.date)).
  ff AS (
    SELECT
      toStartOfMonth(toDate32OrNull(dt)) AS month,
      mkt_rf,
      rf
    FROM ff.five_factor_monthly
    WHERE toDate32OrNull(dt) BETWEEN toDate32('1976-01-01') AND toDate32('2000-12-31')
  ),

  -- Inner join on month: each (permno, month) row gets its mkt_rf / rf.
  joined AS (
    SELECT
      p.permno,
      p.month,
      p.ret - f.rf        AS y_excess,
      f.mkt_rf            AS x_mkt
    FROM crsp_universe AS p
    INNER JOIN ff AS f
      ON p.month = f.month
  ),

  -- Rolling 60-month regression quantities per permno.
  rolling AS (
    SELECT
      permno,
      month,
      y_excess,
      x_mkt,
      count() OVER w                      AS n_obs,
      sum(x_mkt)    OVER w                AS sum_x,
      sum(y_excess) OVER w                AS sum_y,
      sum(x_mkt * y_excess) OVER w        AS sum_xy,
      sum(x_mkt * x_mkt) OVER w           AS sum_x2
    FROM joined
    WINDOW w AS (
      PARTITION BY permno
      ORDER BY month
      ROWS BETWEEN 59 PRECEDING AND CURRENT ROW
    )
  )

SELECT
  permno,
  month,
  -- OLS slope: beta = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x^2)
  -- Guard with n_obs >= 24 (FF 1992 threshold) and variance > 0.
  CASE
    WHEN n_obs >= 24
     AND (n_obs * sum_x2 - sum_x * sum_x) > 0
      THEN (n_obs * sum_xy - sum_x * sum_y)
         / (n_obs * sum_x2 - sum_x * sum_x)
    ELSE NULL
  END AS beta
FROM rolling
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 5000000000,
         timeout_before_checking_execution_speed = 0
