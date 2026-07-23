-- universe_monthly.sql
-- Purpose: Point-in-time universe monthly returns + market equity + exchange code.
--          Universe (paper rule universe_exchanges_sic, L73): NYSE/AMEX/NASDAQ
--          ordinary common stocks, excluding financials (SIC 6000-6999).
--          Applied point-in-time via msfhdr (begdat <= date <= enddat).
-- Tables: crsp_202601.msf, crsp_202601.msfhdr
-- Output columns: permno, date, ret, prc, me, hexcd
-- Depends on: (none)
-- Notes:
--   * DATES ARE ISO STRINGS. The PIT join compares m.date vs h.begdat/h.enddat as
--     strings (zero-padded YYYY-MM-DD sorts chronologically). We do NOT use
--     toDate() because ClickHouse Date clamps pre-1970 dates to the epoch and
--     this sample starts in 1965.
--   * Market equity DOLLARS me = abs(prc) * shrout * 1000 (prc is $/share and
--     SIGNED -> abs(); shrout is in THOUSANDS of shares).
--   * Window starts 1965-01 (BHRET36 at the June-1968 formation needs Jul-1965
--     onward) and ends 2003-12 (panel ends Jun-2003; slack through year-end).
--   * Universe filter uses msfhdr header codes (hshrcd/hexcd/hsiccd); the
--     per-month exchange code msf.hexcd is carried for the NYSE size-group
--     breakpoints (point-in-time as of each month).
--   * ret is the raw CRSP holding-period return (delisting adjustment applied
--     downstream in main.py using msedelist).
SELECT
    m.permno AS permno,
    m.date AS date,
    m.ret AS ret,
    abs(m.prc) AS prc,
    abs(m.prc) * m.shrout * 1000 AS me,
    m.hexcd AS hexcd
FROM crsp_202601.msf AS m
INNER JOIN crsp_202601.msfhdr AS h
    ON m.permno = h.permno
   AND m.date >= h.begdat
   AND m.date <= h.enddat
WHERE m.date >= '1965-01-01'
  AND m.date <= '2003-12-31'
  AND m.permno IS NOT NULL
  AND h.hshrcd IN (10, 11)
  AND h.hexcd IN (1, 2, 3)
  AND NOT (h.hsiccd >= 6000 AND h.hsiccd <= 6999)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
