-- ff_factors.sql
-- Purpose: Load Fama-French-Carhart 4-factor monthly from ff.four_factor_monthly.
--          Parse the string `dt` column to Date32. Restrict to the sample window.
-- Tables: ff.four_factor_monthly
-- Output columns: month (Date32), mkt_rf, smb, hml, mom, rf
-- Depends on: (none)
-- Settings: max_execution_time=60
SELECT toDate32OrNull(dt)         AS month,
       mkt_rf                     AS mkt_rf,
       smb                        AS smb,
       hml                        AS hml,
       mom                        AS mom,
       rf                         AS rf
FROM ff.four_factor_monthly
WHERE toDate32OrNull(dt) BETWEEN toDate32('1962-07-01') AND toDate32('2005-12-31')
SETTINGS max_execution_time = 60,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
