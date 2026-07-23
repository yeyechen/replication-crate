-- delisting_returns.sql
-- Purpose: Effective delisting return per delisting event for the
--   delisting adjustment (A1, A12). dlret_eff = dlret when valid;
--   else -0.30 for dlstcd in [500, 599]; else 0.0. main.py compounds
--   dlret_eff into the delisting-month return of each delisted permno.
-- Tables: crsp_202601.dsedelist
-- Output columns: permno, dlstdt, dlstcd, dlret_eff
-- Depends on: (none)
-- Conventions:
--   * "Missing" dlret = NULL OR sentinel (< -0.40: CRSP uses -44, -55,
--     -66, -77, -88, -99 as missing codes).
--   * Task rule: dlstcd 500-599 with missing dlret -> -0.30; other
--     missing -> 0.0; valid dlret used as-is.
--   * Date range covers the panel (1963-06 .. 2000-12) with a buffer on
--     both ends so delistings near the boundaries are captured.

SELECT
    toInt32(permno)                                         AS permno,
    toDate32(dlstdt)                                        AS dlstdt,
    toInt32(dlstcd)                                         AS dlstcd,
    CASE
        WHEN dlret IS NOT NULL AND toFloat64(dlret) > -0.40
            THEN toFloat64(dlret)
        WHEN toInt32(dlstcd) >= 500 AND toInt32(dlstcd) <= 599
            THEN -0.30
        ELSE 0.0
    END                                                     AS dlret_eff
FROM crsp_202601.dsedelist
WHERE dlstdt IS NOT NULL
  AND dlstcd IS NOT NULL
  AND dlstdt BETWEEN '1962-01-01' AND '2002-12-31'
SETTINGS max_execution_time = 120,
         max_rows_to_read = 1000000,
         timeout_before_checking_execution_speed = 0
