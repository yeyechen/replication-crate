-- daily_stats.sql
-- Purpose: Per-(permno, month) sufficient statistics for the idiosyncratic
--   volatility (FF3) regression, total volatility, coskewness, dollar
--   volume, and turnover — all computed from DAILY data in one scan of
--   dsf. main.py pulls these aggregates (NOT the raw daily rows) and
--   solves the per-stock FF3 regression in closed form.
-- Tables: crsp_202601.dsf, crsp_202601.dsenames, ff.three_factor
-- Output columns (one row per permno, month):
--   permno, month, n_obs,
--   sum_y, sum_y2, sum_m, sum_s, sum_h,
--   sum_m2, sum_s2, sum_h2, sum_ms, sum_mh, sum_sh,
--   sum_ym, sum_ys, sum_yh,
--   sum_ri, sum_ri2, sum_ri_m, sum_ri_m2,
--   sum_dvol_million, n_vol, sum_turn, n_turn
-- Depends on: (none)
-- Conventions:
--   * Universe (A3): PIT dsenames join, shrcd IN (10,11), exchcd IN (1,2,3),
--     ret > -1.0 (drops CRSP sentinels).
--   * FF factors (Verified Fact 1,2): ff.three_factor is DAILY and in
--     DECIMAL. Join on the SAME date as the stock return. Daily excess
--     return y = ret - rf  (rf = ff.three_factor.rf, decimal). NO /100.
--   * Sufficient statistics let main.py build the 4x4 normal equations
--     X'X (X = [1, mkt, smb, hml]) and X'y, solve for betas, and get
--     SSE = sum_y2 - b'X'y  =>  IVOL = sqrt(SSE/(n-1)).
--   * TVOL uses raw returns: var = (sum_ri2 - sum_ri^2/n)/(n-1).
--   * Coskewness (Harvey-Siddique) uses raw stock return (ri) and the
--     market factor (m): needs sum_ri, sum_ri2, sum_m, sum_m2, sum_ri_m,
--     sum_ri_m2 (third cross-moment).
--   * Dollar volume (Verified Fact 3): vol is in SHARES, so dollar volume
--     = abs(prc)*vol (dollars); sum_dvol_million = sum(abs(prc)*vol)/1e6.
--     Turnover = vol/(shrout*1000) (shrout in thousands). The task's
--     "*1000" on volume is an error (would imply vol in thousands).
--   * Date range 1963-06-01 .. 2000-12-31 (A9: June 1963 needed for the
--     first formation month).

WITH universe_daily AS (
    SELECT
        d.permno                                                  AS permno,
        toDate32(date_trunc('month', toDate32(d.date)))           AS month,
        toFloat64(d.ret)                                          AS ret,
        abs(toFloat64(d.prc))                                     AS prc_abs,
        toFloat64(d.vol)                                          AS vol,
        toFloat64(d.shrout)                                       AS shrout,
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
)
SELECT
    permno,
    month,
    count()                                                       AS n_obs,
    -- excess return y = ret - rf  (FF3 regression dependent variable)
    sum(ret - rf)                                                 AS sum_y,
    sum((ret - rf) * (ret - rf))                                  AS sum_y2,
    -- factor sums / cross-products (X'X blocks)
    sum(mkt)      AS sum_m,
    sum(smb)      AS sum_s,
    sum(hml)      AS sum_h,
    sum(mkt * mkt) AS sum_m2,
    sum(smb * smb) AS sum_s2,
    sum(hml * hml) AS sum_h2,
    sum(mkt * smb) AS sum_ms,
    sum(mkt * hml) AS sum_mh,
    sum(smb * hml) AS sum_sh,
    -- X'y blocks (y on each factor)
    sum((ret - rf) * mkt) AS sum_ym,
    sum((ret - rf) * smb) AS sum_ys,
    sum((ret - rf) * hml) AS sum_yh,
    -- raw-return moments (TVOL + coskewness)
    sum(ret)              AS sum_ri,
    sum(ret * ret)        AS sum_ri2,
    sum(ret * mkt)        AS sum_ri_m,
    sum(ret * mkt * mkt)  AS sum_ri_m2,
    -- dollar volume ($ millions) and turnover
    sum(prc_abs * vol) / 1000000.0                                AS sum_dvol_million,
    countIf(vol > 0 AND prc_abs > 0)                              AS n_vol,
    sum(if(shrout > 0, vol / (shrout * 1000.0), 0.0))             AS sum_turn,
    countIf(shrout > 0 AND vol IS NOT NULL)                       AS n_turn
FROM universe_daily
GROUP BY permno, month
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
