-- msf_monthly_base.sql
-- Purpose: Base monthly CRSP data for ALL securities, 1926-12 through 2006-12.
--   The 1926-12 start provides pre-1970 lag history; the 2006-12 end provides
--   post-2003 holding-period leads. Sentinel returns (ret <= -1.0, i.e. the
--   CRSP non-NULL codes -55/-66/-77/-88/-99 and the -1 total-loss) are NULLed
--   but the ROW is kept (inclusion filter on ret is applied later, per spec).
--   Emits an integer month index midx = year*12 + (month-1) because ClickHouse
--   toStartOfMonth()/Date clamps pre-1970 dates to the 1970 epoch; midx is
--   epoch-proof and decodes to (year=midx//12, month=midx%12+1) in Python.
-- Paper: Pontiff & Woodgate (2008) "Share Issuance and Cross-sectional Returns",
--   J. Finance. §I Sample (L51); CRSP ret sentinels per references/CRSP.md.
-- Tables: crsp_202601.msf
-- Output columns: permno, date, yr, mo, midx, ret, prc_abs, shrout, cfacshr
-- Depends on: (none)
SELECT
    permno,
    date,
    toYear(toDate32(date))  AS yr,
    toMonth(toDate32(date)) AS mo,
    toYear(toDate32(date)) * 12 + (toMonth(toDate32(date)) - 1) AS midx,
    if(ret IS NOT NULL AND ret > -1.0, ret, NULL) AS ret,  -- NULL sentinels
    abs(prc) AS prc_abs,                                   -- prc<0 = bid/ask avg
    shrout,                                                -- in thousands
    cfacshr                                                -- reciprocal of paper Total Factor (pre-verified)
FROM crsp_202601.msf
WHERE date >= '1926-12-01' AND date <= '2006-12-31'
  AND permno IS NOT NULL
SETTINGS max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
