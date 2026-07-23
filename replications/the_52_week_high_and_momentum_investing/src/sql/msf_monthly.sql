-- msf_monthly.sql
-- Purpose: Monthly CRSP stock data for George & Hwang (2004), "The 52-Week
--          High and Momentum Investing". Pulls all stock-months 1957-12 ..
--          2002-12 (Dec-1957 is needed as the lagged market cap for
--          Jan-1958 industry returns; the analysis grid starts 1958-01).
--          Hygiene filter (methodology, verified):
--            * ret IS NOT NULL AND ret > -1  — drops CRSP missing-return
--              sentinels (-55 .. -99); a genuine -100% month has
--              ret = -1.0 exactly and is KEPT.
--            * prc IS NOT NULL AND abs(prc) > 0 — valid month-end price.
--          NO universe filter here: rolling signals (jt_sig, 52-week-high,
--          g_gh) are computed on the FULL msf history per permno; the
--          point-in-time common-stock filter (dsenames shrcd IN (10, 11))
--          is applied in main.py before saving the panel
--          (dsenames_common.sql). The calendar month-end key is derived in
--          main.py (date + MonthEnd(0)) because ClickHouse date-arithmetic
--          functions saturate pre-1970 dates on the Date type.
-- Tables: crsp_202601.msf
-- Output columns: permno, date (last trading day of the month, Date32 —
--                 toDate32 because the Date type cannot hold pre-1970
--                 dates), ret, prc, vol, shrout, bidlo, askhi, hexcd,
--                 hsiccd
-- Units (verified against ClickHouse): prc $/share (negative = bid/ask
--                 quote convention), shrout in THOUSANDS of shares,
--                 vol in HUNDREDS of shares (msf.vol x 100 = sum of dsf
--                 daily vol, up to rounding of msf.vol to whole hundreds).
-- Depends on: (none)
SELECT
    permno,
    toDate32(date) AS date,
    ret,
    prc,
    vol,
    shrout,
    bidlo,
    askhi,
    hexcd,
    hsiccd
FROM crsp_202601.msf
WHERE date >= '1957-12-01' AND date <= '2002-12-31'
  AND ret IS NOT NULL AND ret > -1
  AND prc IS NOT NULL AND abs(prc) > 0
SETTINGS
    max_execution_time = 600,
    max_rows_to_read = 10000000000,
    timeout_before_checking_execution_speed = 0
