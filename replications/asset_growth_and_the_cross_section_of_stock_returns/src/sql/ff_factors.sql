-- ff_factors.sql
-- Purpose: Fama-French monthly factors for risk adjustment (later tasks).
--          FF3 = (mkt_rf, smb, hml, rf) dropping mom (Assumption 5);
--          Carhart 4-factor = (mkt_rf, smb, hml, mom, rf).
-- Tables: ff.four_factor_monthly
-- Output columns: month, mkt_rf, smb, hml, mom, rf
-- Depends on: (none)
-- Notes:
--   * dt is a STRING month-end date (YYYY-MM-DD). Returned as-is (renamed month);
--     parsed in Python. (toDate() would clamp pre-1970 dates to the epoch.)
--   * All factors are DECIMAL (e.g. 0.02 = 2%).
SELECT
    dt AS month,
    mkt_rf,
    smb,
    hml,
    mom,
    rf
FROM ff.four_factor_monthly
WHERE dt >= '1968-01-01'
  AND dt <= '2003-12-31'
  AND dt IS NOT NULL
SETTINGS max_execution_time = 120,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
