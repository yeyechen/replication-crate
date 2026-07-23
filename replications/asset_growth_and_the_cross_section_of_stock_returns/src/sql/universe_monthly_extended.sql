-- universe_monthly_extended.sql
-- Purpose: Point-in-time universe monthly returns + market equity + exchange code,
--          EXTENDED WINDOW 1968-07 .. 2007-06 for the Table II Section E event-time
--          Year 1..5 buy-and-hold analysis. The latest formation is June 2002 and its
--          Year-5 holding period ends June 2007, so the foundation panel
--          (universe_monthly.sql, ends 2003-12) is extended 4 years.
--          SAME universe filter as the foundation (paper rule universe_exchanges_sic,
--          L73): NYSE/AMEX/NASDAQ ordinary common stocks, excluding financials
--          (SIC 6000-6999), applied point-in-time via msfhdr (begdat <= date <= enddat).
-- Tables: crsp_202601.msf, crsp_202601.msfhdr
-- Output columns: permno, date, ret, prc, me, hexcd
-- Depends on: (none)
-- Notes:
--   * DATES ARE ISO STRINGS. The PIT join compares m.date vs h.begdat/h.enddat as
--     strings (zero-padded YYYY-MM-DD sorts chronologically). We do NOT use
--     toDate() because ClickHouse Date clamps pre-1970 dates to the epoch and
--     this sample starts in 1968.
--   * Market equity DOLLARS me = abs(prc) * shrout * 1000 (prc is $/share and
--     SIGNED -> abs(); shrout is in THOUSANDS of shares).
--   * ret is the raw CRSP holding-period return. The SAME delisting adjustment as
--     the foundation (Assumption 1) is applied downstream in src/table_2_event_time.py
--     using delisting_extended.sql, by importing main.adjust_delistings so the logic
--     is byte-identical to the foundation's.
--   * table_2_event_time.py verifies that the delisting-adjusted series reproduces
--     data/panel.parquet EXACTLY on the overlapping 1968-07 .. 2003-06 window.
--   * Universe filter uses msfhdr header codes (hshrcd/hexcd/hsiccd); the
--     per-month exchange code msf.hexcd is carried for consistency with the
--     foundation schema (not used downstream here).
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
WHERE m.date >= '1968-07-01'
  AND m.date <= '2007-06-30'
  AND m.permno IS NOT NULL
  AND h.hshrcd IN (10, 11)
  AND h.hexcd IN (1, 2, 3)
  AND NOT (h.hsiccd >= 6000 AND h.hsiccd <= 6999)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
