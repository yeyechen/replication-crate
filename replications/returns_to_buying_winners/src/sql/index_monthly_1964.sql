-- index_monthly_1964.sql
-- Purpose: CRSP equally-weighted AND value-weighted MONTHLY index returns,
--          1964-01 .. 1989-12 (312 months), each compounded from the daily dsi
--          series: exp(sum(log(1 + xwretd))) - 1 per calendar month. Extended
--          back from the Table II market_index_monthly.sql 1965-01 start so the
--          §III decomposition's 6-month windows (which reach back to 1964-07
--          for the first 1965-01 formation / overlapping 6-month return) are
--          complete (started at 1964-01 so the WRSS 1964-12 formation's past
--          window [1964-06, 1964-11] and the A2/A4 6-month windows are full).
--          Used by compute_decomposition() (audit-1 M3):
--            ew  -> WRSS past-window EW index return (A1), EW-index 6-month
--                   serial covariance (A2), and the EW-market alternative for
--                   the residual serial covariance (A3).
--            vw  -> market proxy for the market-model residuals (A3) and the
--                   squared-lagged-market regression (A4; L526 names the VW
--                   index as the factor proxy).
-- Tables: crsp_202601.dsi
-- Output columns: month ('YYYY-MM' string — P8), ew_ret, vw_ret
-- Depends on: (none)
SELECT
    substring(date, 1, 7) AS month,
    exp(sum(log(1 + ewretd))) - 1 AS ew_ret,
    exp(sum(log(1 + vwretd))) - 1 AS vw_ret
FROM crsp_202601.dsi
WHERE date >= '1964-01-01' AND date <= '1989-12-31'
  AND ewretd IS NOT NULL AND ewretd > -1.0
  AND vwretd IS NOT NULL AND vwretd > -1.0
GROUP BY month
ORDER BY month
SETTINGS max_execution_time = 300,
         timeout_before_checking_execution_speed = 0;
