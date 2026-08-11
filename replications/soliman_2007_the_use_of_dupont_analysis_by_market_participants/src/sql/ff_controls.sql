-- ff_controls.sql
-- Purpose: Build FF risk-control variables for Table 7:
--            BM     = ceq / (abs(prc) * shrout * 1000)  -- book-to-market
--            log_mve = log(abs(prc) * shrout)            -- log market value
--          Both use the stock price at end of fiscal year t-1 (matching
--          the EARN convention: Compustat datadate of fiscal year t-1).
--
--          NOTE: Beta is NOT computed here (the paper's 2-year weekly
--          market-model regression is non-trivial to replicate; we omit
--          the Beta control and document this as a paper-silent
--          decision in assumptions.md#16).
-- Tables: crsp_202601.msf, crsp_202601.dsf, crsp_202601.ccmxpf_linktable,
--         comp_202601.funda
-- Output columns: gvkey, fyear, datadate, BM, log_mve
-- Depends on: (none)
-- Settings: max_execution_time=600, max_rows_to_read=5e8

WITH
  comp_raw AS (
    SELECT
      f.gvkey,
      f.fyear AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      f.ceq AS CEQ
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.ceq IS NOT NULL
      AND NOT (toInt32OrZero(c.sic) BETWEEN 6000 AND 6999)
  ),
  comp_dedup AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, CEQ,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_raw
    ) WHERE rn = 1
  ),
  -- Lag fiscal-year-end datadate (datadate of fyear-1) per (gvkey, fyear).
  comp_lag AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.CEQ,
      prev.datadate AS lag_datadate
    FROM comp_dedup AS c
    LEFT JOIN comp_dedup AS prev
      ON prev.gvkey = c.gvkey AND prev.fyear = c.fyear - 1
  ),
  -- Map (gvkey, fyear) -> permno via PIT-valid link on the lagged
  -- fiscal-year-end datadate (so the link is valid as of the price date).
  comp_with_permno AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.CEQ, c.lag_datadate,
      toInt32(l.lpermno) AS permno
    FROM comp_lag AS c
    INNER JOIN crsp_202601.ccmxpf_linktable AS l
      ON l.gvkey = c.gvkey
     AND l.linktype IN ('LC', 'LU')
     AND l.linkprim IN ('P', 'C')
     AND l.lpermno IS NOT NULL
     AND c.lag_datadate >= toDate32OrNull(l.linkdt)
     AND (l.linkenddt IS NULL OR c.lag_datadate <= toDate32OrNull(l.linkenddt))
  ),
  -- Last trading day price/shares at or before the lagged datadate.
  -- Use msf (month-end) ASOF LEFT JOIN for efficiency.
  msf_prices AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.CEQ, c.lag_datadate, c.permno,
      p.prc,
      p.shrout
    FROM comp_with_permno AS c
    ASOF LEFT JOIN
      (SELECT permno, toDate32OrNull(date) AS date, prc, shrout
       FROM crsp_202601.msf
       WHERE prc IS NOT NULL AND prc != 0) AS p
      ON p.permno = c.permno AND p.date <= c.lag_datadate
  ),
  -- Fallback to dsf ASOF for the small subset missing in msf.
  dsf_prices AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.CEQ, c.lag_datadate, c.permno,
      p.prc,
      p.shrout
    FROM comp_with_permno AS c
    ASOF LEFT JOIN
      (SELECT permno, toDate32OrNull(date) AS date, prc, shrout
       FROM crsp_202601.dsf
       WHERE prc IS NOT NULL AND prc != 0) AS p
      ON p.permno = c.permno AND p.date <= c.lag_datadate
    WHERE c.permno NOT IN (
      SELECT permno FROM msf_prices GROUP BY permno HAVING count() > 0
    )
  ),
  combined AS (
    SELECT gvkey, fyear, datadate, CEQ, lag_datadate, permno, prc, shrout
    FROM msf_prices
    UNION ALL
    SELECT gvkey, fyear, datadate, CEQ, lag_datadate, permno, prc, shrout
    FROM dsf_prices
  )
SELECT
  gvkey,
  fyear,
  datadate,
  -- BM = CEQ / (abs(prc) * shrout * 1000). Paper §III defines MVE as
  -- shares × price (Compustat #25 × #199), so the multiplier is
  -- `* 1000` to put prc*shrout into dollars (shrout is in thousands).
  -- We filter to |prc| > 0 and shrout > 0 to avoid division by zero.
  if((abs(prc) * shrout * 1000.0) > 0,
     CEQ / (abs(prc) * shrout * 1000.0),
     NULL) AS BM,
  -- log_mve = log(abs(prc) * shrout). shrout is in thousands; the
  -- constant factor cancels in the regression (it shifts all log_mve
  -- by the same constant, absorbed by the intercept).
  if((abs(prc) * shrout) > 0,
     log(abs(prc) * shrout),
     NULL) AS log_mve
FROM combined
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0
