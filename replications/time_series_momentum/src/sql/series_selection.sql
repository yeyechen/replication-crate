-- series_selection.sql
-- Purpose: AUDIT query — coverage of candidate Datastream continuous futures
--          calc series used to select the instrument mapping (assumption A4).
--          For every candidate calcseriescode: first/last date with data,
--          count of distinct trading days, and count within the strategy
--          evaluation window 1985-01-01..2009-12-31. The selected series per
--          instrument (longest 1985-2009 coverage; prefer non-DEAD/plain-CS00
--          on ties; verified against wrds_cseries_info filters
--          positionfwddesc='First' and the four allowed roll methods) are
--          listed in src/instrument_map.csv and embedded in src/main.py.
-- Tables: tr_ds_fut_202606.wrds_fut_series
-- Output columns: calcseriescode, first_date, last_date, n_days, n_days_8509
-- Depends on: (none)
-- Settings: max_execution_time=900
-- Usage: {codes} is substituted by main.py with the candidate code list.
SELECT calcseriescode,
       min(date_)  AS first_date,
       max(date_)  AS last_date,
       count(DISTINCT date_) AS n_days,
       countIf(DISTINCT date_,
               date_ >= '1985-01-01' AND date_ <= '2009-12-31') AS n_days_8509
FROM tr_ds_fut_202606.wrds_fut_series
WHERE calcseriescode IN ({codes})
GROUP BY calcseriescode
SETTINGS max_execution_time = 900,
         max_rows_to_read = 100000000000,
         timeout_before_checking_execution_speed = 0
