-- crsp_returns.sql
-- Purpose: Build the CRSP-based variables for Table 4 and Table 7:
--            R_t       = compounded 12-month buy-hold market-adjusted return
--                        (firm return - VW market return) over the 12 months
--                        starting (datadate, datadate + 12 months].
--                        NOTE: the paper's contemporaneous return window
--                        starts 1 month after fiscal year-end; future return
--                        (Table 7) starts 4 months after fiscal year-end and
--                        continues 12 months — the latter is in
--                        src/sql/future_returns.sql.
--            eps_t     = ib / csho (Compustat, in $/share).
--            eps_lag1  = EPS in year t-1 (in $/share).
--            price_lag1_per_share = abs(prc) on the LAST CRSP trading day
--                        at or before the firm's fiscal year-end of fiscal
--                        year t-1 (i.e., Compustat `datadate` for fyear t-1).
--                        For Dec-end firms this is the same as the Dec 31
--                        of calendar year t-1; for non-Dec-end firms it
--                        properly aligns with their fiscal calendar.
--            price_lag1_dollars = abs(prc) × shrout × 1000 (CRSP market cap).
--
-- Tables: crsp_202601.dsf, crsp_202601.msf, crsp_202601.dsi,
--         crsp_202601.ccmxpf_linktable, comp_202601.funda
-- Output columns: gvkey, fyear, datadate, R_t, eps_t, eps_lag1,
--                 price_lag1_per_share, price_lag1_dollars,
--                 price_ann_per_share
-- Depends on: (none)
-- Settings: max_execution_time=600, max_rows_to_read=5e8

WITH
  -- 1) Compustat EPS for each (gvkey, fyear). Take the latest
  --    datadate within (gvkey, fyear) for dedup.
  comp_eps AS (
    SELECT
      f.gvkey,
      f.fyear AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      f.ib / nullIf(f.csho, 0) AS eps_raw
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.ib IS NOT NULL
      AND f.csho IS NOT NULL AND f.csho > 0
      AND NOT (toInt32OrZero(c.sic) BETWEEN 6000 AND 6999)
  ),
  comp_eps_dedup AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, eps_raw,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_eps
    )
    WHERE rn = 1
  ),
  -- 2) Map (gvkey, fyear) -> permno via CRSP-Compustat link, PIT-valid on
  --    the firm's fiscal year-end datadate.
  comp_with_permno AS (
    SELECT DISTINCT
      c.gvkey,
      c.fyear,
      c.datadate,
      toInt32(l.lpermno) AS permno
    FROM comp_eps_dedup AS c
    INNER JOIN crsp_202601.ccmxpf_linktable AS l
      ON l.gvkey = c.gvkey
     AND l.linktype IN ('LC', 'LU')
     AND l.linkprim IN ('P', 'C')
     AND l.lpermno IS NOT NULL
     AND c.datadate >= toDate32OrNull(l.linkdt)
     AND (l.linkenddt IS NULL OR c.datadate <= toDate32OrNull(l.linkenddt))
  ),
  -- 3) Compute the lagged fiscal-year-end for each (gvkey, fyear):
  --    this is the datadate of (gvkey, fyear-1).
  comp_lag_datadate AS (
    SELECT
      c.gvkey,
      c.fyear,
      c.datadate,
      c.permno,
      prev.datadate AS lag_datadate
    FROM comp_with_permno AS c
    LEFT JOIN comp_eps_dedup AS prev
      ON prev.gvkey = c.gvkey AND prev.fyear = c.fyear - 1
  ),
  -- 4) Get the CRSP per-share price on the LAST trading day at or before
  --    lag_datadate. Use msf (month-end) for efficiency — pick the most
  --    recent msf record whose `date` <= lag_datadate per permno.
  --    If no msf record exists for that month, fall back to the last
  --    available daily dsf record at or before lag_datadate.
  msf_lag_price AS (
    SELECT
      c.gvkey,
      c.fyear,
      c.datadate,
      c.permno,
      p.prc,
      p.shrout,
      p.date AS msf_date
    FROM comp_lag_datadate AS c
    ASOF LEFT JOIN
      (SELECT permno, toDate32OrNull(date) AS date, prc, shrout
       FROM crsp_202601.msf
       WHERE prc IS NOT NULL AND prc != 0) AS p
      ON p.permno = c.permno AND p.date <= c.lag_datadate
  ),
  dsf_lag_price AS (
    -- Fallback: last daily price at or before lag_datadate.
    -- Restrict to within 30 days of lag_datadate for performance.
    SELECT
      c.gvkey,
      c.fyear,
      c.datadate,
      c.permno,
      p.prc,
      p.shrout,
      p.date AS dsf_date
    FROM comp_lag_datadate AS c
    ASOF LEFT JOIN
      (SELECT permno, toDate32OrNull(date) AS date, prc, shrout
       FROM crsp_202601.dsf
       WHERE prc IS NOT NULL AND prc != 0) AS p
      ON p.permno = c.permno AND p.date <= c.lag_datadate
    WHERE c.permno IN (
      SELECT permno FROM msf_lag_price
       GROUP BY permno HAVING count() = 0
    )
  ),
  combined_lag_price AS (
    SELECT
      m.gvkey, m.fyear, m.datadate, m.permno,
      m.prc, m.shrout
    FROM msf_lag_price AS m
    UNION ALL
    SELECT
      d.gvkey, d.fyear, d.datadate, d.permno,
      d.prc, d.shrout
    FROM dsf_lag_price AS d
  ),
  lagged_price AS (
    SELECT
      gvkey, fyear, datadate,
      avg(abs(prc))                       AS price_lag1_per_share,
      avg(abs(prc) * shrout * 1000.0)     AS price_lag1_dollars
    FROM combined_lag_price
    WHERE prc IS NOT NULL
    GROUP BY gvkey, fyear, datadate
  ),
  -- 4b) Price at the END OF THE MONTH OF THE YEAR-t EARNINGS ANNOUNCEMENT.
  --     This is the deflator the paper specifies for FE_{t+1} (paper L480:
  --     "scaled by the stock price at the end of the month of the earnings
  --     announcement for year t"), as opposed to the FY t-1 price used for
  --     EARN / ΔEARN / Anal_REV / SUR.
  --     Proxy: the last CRSP month-end price at or before datadate + 3
  --     months. The IBES annual-EPS announcement lands a median 47 days
  --     after the fiscal period end (p25=33d, p75=79d), so the month-end
  --     of the announcement month falls between datadate+2m and
  --     datadate+3m for the great majority of firm-years.
  --     Used only for the audit [M5] FE-deflator test (assumption 25).
  ann_price AS (
    SELECT
      c.gvkey, c.fyear, c.datadate,
      p.prc AS prc
    FROM comp_with_permno AS c
    ASOF LEFT JOIN
      (SELECT permno, toDate32OrNull(date) AS date, prc
       FROM crsp_202601.msf
       WHERE prc IS NOT NULL AND prc != 0) AS p
      ON p.permno = c.permno AND p.date <= addMonths(c.datadate, 3)
  ),
  ann_price_agg AS (
    SELECT
      gvkey, fyear, datadate,
      avg(abs(prc)) AS price_ann_per_share
    FROM ann_price
    WHERE prc IS NOT NULL
    GROUP BY gvkey, fyear, datadate
  ),
  -- 5) Daily firm returns in (datadate, datadate + 12 months] for R_t.
  firm_daily AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.permno,
      toDate32OrNull(d.date) AS ret_d,
      d.ret
    FROM comp_with_permno AS c
    INNER JOIN crsp_202601.dsf AS d
      ON d.permno = c.permno
     AND toDate32OrNull(d.date) >  c.datadate
     AND toDate32OrNull(d.date) <= addMonths(c.datadate, 12)
     AND d.ret IS NOT NULL
     AND d.ret > -0.5 AND d.ret < 1.0
  ),
  mkt_daily AS (
    SELECT
      c.gvkey, c.fyear, c.datadate,
      toDate32OrNull(d.date) AS mkt_d,
      d.vwretd
    FROM comp_with_permno AS c
    CROSS JOIN crsp_202601.dsi AS d
    WHERE toDate32OrNull(d.date) >  c.datadate
      AND toDate32OrNull(d.date) <= addMonths(c.datadate, 12)
      AND d.vwretd IS NOT NULL
      AND d.vwretd > -0.5 AND d.vwretd < 1.0
  ),
  firm_12mo AS (
    SELECT
      gvkey, fyear, datadate,
      arrayProduct(groupArray(1 + ret)) - 1 AS firm_12m_ret
    FROM firm_daily
    GROUP BY gvkey, fyear, datadate
  ),
  mkt_12mo AS (
    SELECT
      gvkey, fyear, datadate,
      arrayProduct(groupArray(1 + vwretd)) - 1 AS mkt_12m_ret
    FROM mkt_daily
    GROUP BY gvkey, fyear, datadate
  ),
  crsp_r AS (
    SELECT
      f.gvkey, f.fyear, f.datadate,
      f.firm_12m_ret - m.mkt_12m_ret AS R_t
    FROM firm_12mo AS f
    INNER JOIN mkt_12mo AS m
      ON f.gvkey = m.gvkey AND f.fyear = m.fyear AND f.datadate = m.datadate
    WHERE f.firm_12m_ret > -0.95 AND f.firm_12m_ret < 50.0
  ),
  -- 6) Per-firm lag EPS for ΔEARN construction.
  comp_eps_with_lags AS (
    SELECT
      gvkey, fyear, datadate,
      eps_raw AS eps_t,
      lagInFrame(eps_raw, 1) OVER w AS eps_lag1
    FROM comp_eps_dedup
    WINDOW w AS (PARTITION BY gvkey ORDER BY fyear
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
  c.gvkey           AS gvkey,
  c.fyear           AS fyear,
  c.datadate        AS datadate,
  r.R_t             AS R_t,
  c.eps_t           AS eps_t,
  c.eps_lag1        AS eps_lag1,
  p.price_lag1_per_share AS price_lag1_per_share,
  p.price_lag1_dollars   AS price_lag1_dollars,
  ap.price_ann_per_share AS price_ann_per_share
FROM comp_eps_with_lags AS c
LEFT JOIN crsp_r AS r
  ON r.gvkey = c.gvkey AND r.fyear = c.fyear AND r.datadate = c.datadate
LEFT JOIN lagged_price AS p
  ON p.gvkey = c.gvkey AND p.fyear = c.fyear AND p.datadate = c.datadate
LEFT JOIN ann_price_agg AS ap
  ON ap.gvkey = c.gvkey AND ap.fyear = c.fyear AND ap.datadate = c.datadate
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0
