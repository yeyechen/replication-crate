-- series_info.sql
-- Purpose: metadata for the selected calc series (Datastream mnemonic, full
--          series name, roll method) — used to populate src/instrument_map.csv.
-- Tables: tr_ds_fut_202606.wrds_cseries_info
-- Output columns: calcseriescode, dsmnem, calcseriesname, rollmethoddesc,
--                 positionfwddesc
-- Depends on: (none)
-- Settings: max_execution_time=60
-- Usage: {codes} substituted by main.py.
SELECT calcseriescode,
       dsmnem,
       calcseriesname,
       rollmethoddesc,
       positionfwddesc
FROM tr_ds_fut_202606.wrds_cseries_info
WHERE calcseriescode IN ({codes})
SETTINGS max_execution_time = 60
