-- ff5_factors_monthly.sql
-- Purpose: Monthly Fama-French FIVE factors for the report-support portfolio
--          diagnostics on the asset-growth long-short spread (src/diagnostics.py).
--          FF5 = (mkt_rf, smb, hml, rmw, cma) + rf.
-- Tables: ff.five_factor_monthly
-- Output columns: month (YYYY-MM-DD string), mkt_rf, smb, hml, rmw, cma, rf
-- Depends on: (none)
-- Notes:
--   * `dt` is a STRING month-end date (YYYY-MM-DD). Returned as-is (renamed
--     month); parsed + converted to a monthly Period in Python for alignment
--     with the portfolio series (keyed by CRSP last-trading-day dates).
--     We do NOT use toDate() because ClickHouse Date clamps pre-1970 dates to
--     the epoch and this sample starts in 1968.
--   * All factors are DECIMAL fractions (0.02 = 2%). rf is the monthly
--     risk-free rate. NOTE: for the zero-investment L/S spread, rf is NOT
--     subtracted (zero_investment=True in portfolio_diagnostics); rf is only
--     carried here for completeness.
--   * Window covers the full panel sample (holding Jul-1968..Jun-2003) with a
--     little slack on both ends.
SELECT
    dt AS month,
    mkt_rf,
    smb,
    hml,
    rmw,
    cma,
    rf
FROM ff.five_factor_monthly
WHERE dt >= '1968-01-01'
  AND dt <= '2003-12-31'
  AND dt IS NOT NULL
SETTINGS max_execution_time = 120,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
