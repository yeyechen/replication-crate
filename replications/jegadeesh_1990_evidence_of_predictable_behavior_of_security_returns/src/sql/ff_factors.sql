-- ff_factors.sql
-- Purpose: Fama-French monthly factors (risk-free rate for market model)
-- Tables: ff.four_factor_monthly
-- Output columns: dt (Date32), month (Date32), mkt_rf, smb, hml, rf, mom
-- Depends on: (none)
-- Settings: max_execution_time=60
--
-- FF monthly factors carry the rf column as the 1-month T-bill rate used
-- as the risk-free proxy in the market-model alpha regressions.
-- dt is calendar month-end (e.g. 1977-07-31), which differs from CRSP
-- msf.date which is the last trading day of the month. Downstream joins
-- must use the (year, month) tuple, not date-equality.

SELECT
  toDate32OrNull(dt)                                         AS dt32,
  toDate32(toDate32OrNull(dt) - toIntervalDay(dayOfMonth(toDate32OrNull(dt)) - 1)) AS month,
  mkt_rf                                                     AS mkt_rf,
  smb                                                        AS smb,
  hml                                                        AS hml,
  rf                                                         AS rf,
  mom                                                        AS mom
FROM ff.four_factor_monthly
WHERE dt IS NOT NULL
SETTINGS max_execution_time = 60