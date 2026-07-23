-- msedelist.sql
-- Purpose: Delisting events for the George & Hwang (2004) delisting-return
--          experiment. Pulls every delisting with dlstdt in 1958-01-01 ..
--          2003-12-31 (the analysis grid is 1958-01 .. 2002-12; 2003 events
--          are pulled per spec and dropped in main.py when their month-end
--          falls outside the grid). dlret is used ONLY to adjust the
--          holding-period return column (ret_dl) — the panel's ranking
--          signals stay on the original msf.ret.
--          Verified in this vintage: dlstdt is an ISO 'YYYY-MM-DD' string
--          (string range comparison is exact), permno/dlstdt never NULL in
--          the window, one row per permno (no duplicate (permno, month)),
--          NO negative sentinels in dlret (missing = NULL only), and
--          dlret = -1.0 exactly marks worthless-stock delistings.
-- Tables: crsp_202601.msedelist
-- Output columns: permno, dlstdt, dlstcd, dlret, dlretx
-- Depends on: (none)
SELECT
    permno,
    dlstdt,
    dlstcd,
    dlret,
    dlretx
FROM crsp_202601.msedelist
WHERE dlstdt IS NOT NULL
  AND dlstdt >= '1958-01-01'
  AND dlstdt <= '2003-12-31'
SETTINGS
    max_execution_time = 300,
    max_rows_to_read = 10000000000,
    timeout_before_checking_execution_speed = 0
