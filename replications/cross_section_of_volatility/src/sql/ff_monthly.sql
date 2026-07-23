-- ff_monthly.sql
-- Purpose: Monthly Fama-French four factors + risk-free rate for
--   (a) computing monthly excess returns (ret_excess = ret - rf) and
--   (b) downstream post-ranking alpha regressions (Tables VI-XI).
-- Tables: ff.four_factor_monthly
-- Output columns: month, mkt_rf, smb, hml, mom, rf
-- Depends on: (none)
-- Conventions:
--   * Values are in DECIMAL (Verified Fact 1) — NO division by 100.
--   * month truncated to month-start Date32 for joining to the panel.

SELECT
    toDate32(date_trunc('month', toDate32(dt))) AS month,
    toFloat64(mkt_rf)                           AS mkt_rf,
    toFloat64(smb)                              AS smb,
    toFloat64(hml)                              AS hml,
    toFloat64(mom)                              AS mom,
    toFloat64(rf)                               AS rf
FROM ff.four_factor_monthly
WHERE dt BETWEEN '1963-06-01' AND '2000-12-31'
  AND mkt_rf IS NOT NULL
  AND smb IS NOT NULL
  AND hml IS NOT NULL
  AND rf IS NOT NULL
ORDER BY month
SETTINGS max_execution_time = 60,
         max_rows_to_read = 100000,
         timeout_before_checking_execution_speed = 0
