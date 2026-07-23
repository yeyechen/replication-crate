-- market_index_monthly.sql
-- Purpose: CRSP value-weighted MONTHLY index return, 1965-01 .. 1989-12
--          (300 months), compounded from daily dsi.vwretd:
--          exp(sum(log(1 + vwretd))) - 1 per calendar month. Used for the
--          Table II post-ranking betas (Assumption A6: regress the PA 6/6
--          overlapping decile return series on this market series over the
--          same 300 months).
-- Tables: crsp_202601.dsi
-- Output columns: month ('YYYY-MM' string — P8: never toDate() pre-1970),
--                 mkt_ret
-- Depends on: (none)
SELECT
    substring(date, 1, 7) AS month,
    exp(sum(log(1 + vwretd))) - 1 AS mkt_ret
FROM crsp_202601.dsi
WHERE date >= '1965-01-01' AND date <= '1989-12-31'
  AND vwretd IS NOT NULL
  AND vwretd > -1.0
GROUP BY month
ORDER BY month
SETTINGS max_execution_time = 300,
         timeout_before_checking_execution_speed = 0;
