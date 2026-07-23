-- ivol12_stats.sql
-- Purpose: Per-(permno, month) sufficient statistics for the 12-MONTH
--   idiosyncratic-volatility (FF3) regression, i.e. the L=12 signal used
--   by the Table X 12/1/1 and 12/1/12 strategies (Issue M2).
--
--   METHOD (SQL-first, no raw-daily pull into Python):
--     1. universe_daily / monthly_stats reproduce the daily_stats.sql
--        monthly sufficient statistics (X'X, X'y, y'y, n) for the FF3
--        regression of daily excess returns y = ret - rf on
--        X = [1, mkt, smb, hml]. These statistics are ADDITIVE across
--        days, so summing them over a window of months gives the exact
--        normal equations of the POOLED regression over that window.
--     2. A RANGE window (PARTITION BY permno ORDER BY month_idx,
--        RANGE BETWEEN 11 PRECEDING AND CURRENT ROW) sums each monthly
--        statistic over the trailing 12 CALENDAR months (months s-11..s).
--        month_idx = year*12 + month is a continuous integer, so the
--        RANGE offset is calendar-correct and a stock's missing months
--        simply contribute nothing (no rows), exactly as required.
--     3. analyze_table10_lmn.py pulls these accumulated statistics and
--        solves the 4x4 normal equations in closed form:
--            SSE = sum_y2_12 - b' X'y_12,  b = (X'X_12)^-1 X'y_12
--            IVOL_12 = sqrt(SSE / (n_obs_12 - 1))   (sample std, ddof=1)
--        mirroring main.compute_daily_signals (Assumption A10).
--
-- Tables: crsp_202601.dsf, crsp_202601.dsenames, ff.three_factor
-- Output columns (one row per permno, month):
--   permno, month,
--   n_obs_12      total daily obs in the trailing 12 calendar months
--   n_months_12   # of distinct months (with data) in that window
--   sum_y_12, sum_y2_12,
--   sum_m_12, sum_s_12, sum_h_12,
--   sum_m2_12, sum_s2_12, sum_h2_12,
--   sum_ms_12, sum_mh_12, sum_sh_12,
--   sum_ym_12, sum_ys_12, sum_yh_12
-- Depends on: (none)  [self-contained; mirrors daily_stats.sql filters]
-- Conventions: identical to daily_stats.sql
--   * Universe (A3): PIT dsenames join, shrcd IN (10,11), exchcd IN (1,2,3),
--     ret > -1.0 (drops CRSP sentinels).
--   * FF factors (Verified Fact 1,2): ff.three_factor is DAILY and DECIMAL;
--     join on the SAME date; y = ret - rf. NO /100.
--   * Date range 1963-06-01 .. 2000-12-31 (A9). The first full 12-month
--     window ends at signal month 1964-05 (months 1963-06..1964-05);
--     earlier signal months have partial windows (n_months_12 < 12) and
--     are filtered in Python via n_obs_12.

WITH universe_daily AS (
    SELECT
        d.permno                                                  AS permno,
        toDate32(date_trunc('month', toDate32(d.date)))           AS month,
        toFloat64(d.ret)                                          AS ret,
        toFloat64(f.mkt_rf)                                       AS mkt,
        toFloat64(f.smb)                                          AS smb,
        toFloat64(f.hml)                                          AS hml,
        toFloat64(f.rf)                                           AS rf
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsenames AS n
        ON d.permno = n.permno
       AND d.date >= n.namedt
       AND d.date <= ifNull(n.nameendt, '2099-12-31')
    INNER JOIN ff.three_factor AS f
        ON d.date = f.dt
    WHERE n.shrcd IN (10, 11)
      AND n.exchcd IN (1, 2, 3)
      AND d.ret IS NOT NULL
      AND d.ret > -1.0
      AND f.mkt_rf IS NOT NULL
      AND f.smb IS NOT NULL
      AND f.hml IS NOT NULL
      AND f.rf IS NOT NULL
      AND d.date BETWEEN '1963-06-01' AND '2000-12-31'
),
monthly_stats AS (
    SELECT
        permno,
        month,
        -- continuous month index so the RANGE offset is calendar-correct
        toInt64(toYYYYMM(month))                                  AS yyyymm,
        toInt64(toYYYYMM(month) DIV 100) * 12
            + toInt64(toYYYYMM(month) % 100)                      AS month_idx,
        count()                                                   AS n_obs,
        sum(ret - rf)                                             AS sum_y,
        sum((ret - rf) * (ret - rf))                              AS sum_y2,
        sum(mkt)      AS sum_m,
        sum(smb)      AS sum_s,
        sum(hml)      AS sum_h,
        sum(mkt * mkt) AS sum_m2,
        sum(smb * smb) AS sum_s2,
        sum(hml * hml) AS sum_h2,
        sum(mkt * smb) AS sum_ms,
        sum(mkt * hml) AS sum_mh,
        sum(smb * hml) AS sum_sh,
        sum((ret - rf) * mkt) AS sum_ym,
        sum((ret - rf) * smb) AS sum_ys,
        sum((ret - rf) * hml) AS sum_yh
    FROM universe_daily
    GROUP BY permno, month
)
SELECT
    permno,
    month,
    sum(n_obs)   OVER w AS n_obs_12,
    count()      OVER w AS n_months_12,
    sum(sum_y)   OVER w AS sum_y_12,
    sum(sum_y2)  OVER w AS sum_y2_12,
    sum(sum_m)   OVER w AS sum_m_12,
    sum(sum_s)   OVER w AS sum_s_12,
    sum(sum_h)   OVER w AS sum_h_12,
    sum(sum_m2)  OVER w AS sum_m2_12,
    sum(sum_s2)  OVER w AS sum_s2_12,
    sum(sum_h2)  OVER w AS sum_h2_12,
    sum(sum_ms)  OVER w AS sum_ms_12,
    sum(sum_mh)  OVER w AS sum_mh_12,
    sum(sum_sh)  OVER w AS sum_sh_12,
    sum(sum_ym)  OVER w AS sum_ym_12,
    sum(sum_ys)  OVER w AS sum_ys_12,
    sum(sum_yh)  OVER w AS sum_yh_12
FROM monthly_stats
WINDOW w AS (
    PARTITION BY permno
    ORDER BY month_idx
    RANGE BETWEEN 11 PRECEDING AND CURRENT ROW
)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
