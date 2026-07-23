-- daily_futures.sql
-- Purpose: daily settlement prices for the selected continuous futures calc
--          series (instrument mapping in src/instrument_map.csv).
--          wrds_fut_series has MULTIPLE rows per (calcseriescode, date_) —
--          one per contract month (cmonth) with identical settlement — so we
--          dedupe with GROUP BY and keep one settlement per day. Rows with
--          missing or non-positive settlement are dropped (they carry no
--          return information). Filtering on date_ (sort-key prefix) keeps
--          the scan bounded.
-- Tables: tr_ds_fut_202606.wrds_fut_series
-- Output columns: calcseriescode, date_, settle, volume, openinterest
-- Depends on: (none)
-- Settings: max_execution_time=900
-- Usage: {codes}, {start_date}, {end_date} substituted by main.py.
-- Note: output alias is `settle` (not `settlement`) so the WHERE clause
-- binds to the raw column, not the aggregate alias.
SELECT calcseriescode,
       date_,
       any(settlement)   AS settle,
       max(volume)       AS volume,
       max(openinterest) AS openinterest
FROM tr_ds_fut_202606.wrds_fut_series
WHERE calcseriescode IN ({codes})
  AND date_ >= '{start_date}'
  AND date_ <= '{end_date}'
  AND settlement IS NOT NULL
  AND settlement > 0
GROUP BY calcseriescode, date_
SETTINGS max_execution_time = 900,
         max_rows_to_read = 100000000000,
         timeout_before_checking_execution_speed = 0
