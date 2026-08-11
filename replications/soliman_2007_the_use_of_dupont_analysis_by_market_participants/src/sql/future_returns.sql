-- future_returns.sql
-- Purpose: Build Table 7's R_{t+1} — future abnormal stock returns.
--            Future stock returns are measured using compounded buy-hold
--            market-adjusted returns, beginning 4 months after fiscal
--            year-end and continuing for 12 months.
--
--          R_{t+1} = (1 + firm_12m_ret)^1 / (1 + mkt_12m_ret)^1 - 1
--          where firm_12m_ret = prod(1 + ret_i) - 1 for daily returns in
--          (datadate + 4 months, datadate + 16 months], and mkt_12m_ret is
--          the same for vwretd.
--
--          Delisting substitution (Shumway 1997 per paper footnote 23):
--          when a firm delists during the 12-month window, substitute
--          -35% for NYSE/AMEX (exchcd IN 1,2) and -55% for NASDAQ (3)
--          (and other exchanges) on the last trading day. Use CRSP
--          dsedelist.dlret first; if missing AND dlstcd IN
--          (500, 520-584), apply the Shumway substitution.
--
--          This CTE builds R_{t+1} at the (gvkey, fyear) level.
-- Tables: crsp_202601.dsf, crsp_202601.dsi, crsp_202601.dsedelist,
--         crsp_202601.ccmxpf_linktable, comp_202601.funda
-- Output columns: gvkey, fyear, datadate, R_future
-- Depends on: (none)
-- Settings: max_execution_time=600, max_rows_to_read=5e8

WITH
  -- 1) Compustat (gvkey, fyear, datadate) tuples for the universe.
  comp_periods AS (
    SELECT
      f.gvkey,
      f.fyear AS fyear,
      toDate32OrNull(f.datadate) AS datadate
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND NOT (toInt32OrZero(c.sic) BETWEEN 6000 AND 6999)
  ),
  comp_periods_dedup AS (
    SELECT *
    FROM (
      SELECT gvkey, fyear, datadate,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_periods
    ) WHERE rn = 1
  ),
  -- 2) Map (gvkey, fyear) -> permno via PIT-valid link.
  comp_with_permno AS (
    SELECT DISTINCT
      c.gvkey, c.fyear, c.datadate,
      toInt32(l.lpermno) AS permno
    FROM comp_periods_dedup AS c
    INNER JOIN crsp_202601.ccmxpf_linktable AS l
      ON l.gvkey = c.gvkey
     AND l.linktype IN ('LC', 'LU')
     AND l.linkprim IN ('P', 'C')
     AND l.lpermno IS NOT NULL
     AND c.datadate >= toDate32OrNull(l.linkdt)
     AND (l.linkenddt IS NULL OR c.datadate <= toDate32OrNull(l.linkenddt))
  ),
  -- 3) Pull delisting info: for each (permno), the delisting return and
  --    the (exchange code) needed for Shumway substitution if dlret is
  --    missing or delisting is performance-related.
  delist_info AS (
    SELECT
      permno,
      toDate32OrNull(dlstdt) AS dlstdt,
      dlstcd,
      dlret,
      hexcd
    FROM crsp_202601.dsedelist
    WHERE dlstdt IS NOT NULL
  ),
  -- 4) Pull daily firm returns in the 12-month window starting at
  --    (datadate + 4 months, datadate + 16 months].
  firm_daily AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.permno,
      toDate32OrNull(d.date) AS ret_d,
      d.ret,
      d.hexcd
    FROM comp_with_permno AS c
    INNER JOIN crsp_202601.dsf AS d
      ON d.permno = c.permno
     AND toDate32OrNull(d.date) >  addMonths(c.datadate, 4)
     AND toDate32OrNull(d.date) <= addMonths(c.datadate, 16)
     AND d.ret IS NOT NULL
     AND d.ret > -0.5 AND d.ret < 1.0
  ),
  -- 5) For firms that delist during the 12-month window: append a
  --    synthetic observation with the Shumway substitute return on the
  --    day after the delisting date. If CRSP's dlret is valid (not a
  --    missing sentinel), use it; otherwise substitute based on dlstcd
  --    being a performance-related code (500, 520-584) and exchange code.
  delist_synth AS (
    SELECT
      c.gvkey, c.fyear, c.datadate, c.permno,
      addDays(di.dlstdt, 1) AS ret_d,
      -- Shumway substitution when:
      --   - dlret is one of the missing sentinels, OR
      --   - dlret is NULL AND dlstcd is performance-related
      if(
        (di.dlret IS NOT NULL AND di.dlret > -0.4),
        di.dlret,
        -- Missing dlret or performance-related delisting: substitute
        -- based on exchange code (Shumway 1997):
        --   NYSE/AMEX (1,2): -0.35
        --   NASDAQ (3): -0.55
        if(coalesce(di.hexcd, 1) IN (1, 2), -0.35, -0.55)
      ) AS ret,
      di.hexcd
    FROM comp_with_permno AS c
    INNER JOIN delist_info AS di
      ON di.permno = c.permno
     AND di.dlstdt >  addMonths(c.datadate, 4)
     AND di.dlstdt <= addMonths(c.datadate, 16)
    WHERE (di.dlret IS NOT NULL AND di.dlret > -0.4)
       OR di.dlstcd IN (500, 520, 521, 522, 523, 524, 525, 526, 527, 528,
                        530, 540, 550, 560, 570, 580, 581, 582, 583, 584)
  ),
  firm_daily_full AS (
    SELECT gvkey, fyear, datadate, permno, ret_d, ret FROM firm_daily
    UNION ALL
    SELECT gvkey, fyear, datadate, permno, ret_d, ret FROM delist_synth
  ),
  -- 6) Market returns for the same window.
  mkt_daily AS (
    SELECT
      c.gvkey, c.fyear, c.datadate,
      toDate32OrNull(d.date) AS mkt_d,
      d.vwretd
    FROM comp_with_permno AS c
    CROSS JOIN crsp_202601.dsi AS d
    WHERE toDate32OrNull(d.date) >  addMonths(c.datadate, 4)
      AND toDate32OrNull(d.date) <= addMonths(c.datadate, 16)
      AND d.vwretd IS NOT NULL
      AND d.vwretd > -0.5 AND d.vwretd < 1.0
  ),
  firm_12mo AS (
    SELECT
      gvkey, fyear, datadate,
      arrayProduct(groupArray(1 + ret)) - 1 AS firm_12m_ret
    FROM firm_daily_full
    GROUP BY gvkey, fyear, datadate
  ),
  mkt_12mo AS (
    SELECT
      gvkey, fyear, datadate,
      arrayProduct(groupArray(1 + vwretd)) - 1 AS mkt_12m_ret
    FROM mkt_daily
    GROUP BY gvkey, fyear, datadate
  )
SELECT
  f.gvkey           AS gvkey,
  f.fyear           AS fyear,
  f.datadate        AS datadate,
  f.firm_12m_ret - m.mkt_12m_ret AS R_future
FROM firm_12mo AS f
INNER JOIN mkt_12mo AS m
  ON f.gvkey = m.gvkey AND f.fyear = m.fyear AND f.datadate = m.datadate
WHERE f.firm_12m_ret > -0.95 AND f.firm_12m_ret < 50.0
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0
