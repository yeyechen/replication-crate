-- delisting.sql
-- Purpose: CRSP monthly delisting events (delisting date, return, code) used to
--          adjust monthly holding returns in the delisting month (Assumption 1).
-- Tables: crsp_202601.msedelist
-- Output columns: permno, dlstdt, dlret, dlstcd
-- Depends on: (none)
-- Notes:
--   * dlret is a DECIMAL (e.g. -0.30). In this extract there are no negative
--     missing-sentinels (min dlret = -1.0, a legitimate total loss); a NULL
--     dlret is the only "missing" signal and is handled downstream.
--   * Downstream rule (Assumption 1): if dlret non-missing, use it; else if
--     dlstcd in 500..599 (performance-related) use -0.30; else use 0.
--   * dlstdt returned as ISO string (pre-1970 dates -> cannot use toDate()).
SELECT
    permno,
    dlstdt AS dlstdt,
    dlret,
    dlstcd
FROM crsp_202601.msedelist
WHERE permno IS NOT NULL
  AND dlstdt IS NOT NULL
  AND dlstdt >= '1965-01-01'
  AND dlstdt <= '2003-12-31'
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
