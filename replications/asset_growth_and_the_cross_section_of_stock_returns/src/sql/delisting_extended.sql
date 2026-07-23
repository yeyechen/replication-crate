-- delisting_extended.sql
-- Purpose: CRSP monthly delisting events for the EXTENDED event-time window
--          1968-07 .. 2007-06 (companion to universe_monthly_extended.sql; the
--          foundation's delisting.sql ends 2003-12). Used to adjust monthly
--          holding returns in the delisting month exactly as in the foundation
--          (Assumption 1).
-- Tables: crsp_202601.msedelist
-- Output columns: permno, dlstdt, dlret, dlstcd
-- Depends on: (none)
-- Notes:
--   * Downstream rule (Assumption 1, main.adjust_delistings): combine as
--     (1+ret)*(1+dlret)-1 in the delisting month; if dlret is missing use -0.30
--     when dlstcd in 500..599 (performance-related) else 0; synthesize a
--     delisting-month row if no msf record exists that month.
--   * dlstdt returned as ISO string (pre-1970 dates -> cannot use toDate()).
SELECT
    permno,
    dlstdt AS dlstdt,
    dlret,
    dlstcd
FROM crsp_202601.msedelist
WHERE permno IS NOT NULL
  AND dlstdt IS NOT NULL
  AND dlstdt >= '1968-07-01'
  AND dlstdt <= '2007-06-30'
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
