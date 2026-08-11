-- ibes_fy1_fy2_ltg.sql
-- Purpose: Extract I/B/E/S FY1 (one-year-ahead), FY2 (two-year-ahead)
--          consensus EPS forecasts and Ltg (long-term growth) for each
--          (gvkey, fyear) firm-year in the Frankel & Lee (1998) panel.
--
-- IBES convention in this vintage (per assumptions.md, assumption 17/18):
--   - fpi='1' = current fiscal year (the year of the May statistical
--     period = year t in the paper's notation). The paper's "FY1" is
--     the consensus forecast for the portfolio-formation year t.
--     fpedats year = stat_year = year t = fyear + 1.
--   - fpi='2' = next fiscal year (year t+1) = "FY2" in the paper.
--     fpedats year = stat_year + 1 = year t + 1 = fyear + 2.
--   - LTG: measure='LTG' rows in statsumu_epsus. NOTE: this vintage
--     has zero LTG rows in statsumu_epsus; the only growth data is in
--     ibes_202601.ptgsumu (measure='PTG'). Per the task spec, we
--     filter for measure='LTG' first; the agent's Python fallback
--     applies the Appendix A Step 3 substitution (FROE_{t+2} =
--     FROE_{t+1}) for missing Ltg.
--
-- Output columns: gvkey, fyear, fy1_eps, fy2_eps, ltg
-- Tables: comp_202601.funda (source of gvkey, fyear, cusip, tic),
--         ibes_202601.id (canonical ticker <-> IBES id mapping),
--         ibes_202601.statsumu_epsus (EPS and LTG consensus rows).
-- Depends on: (none)
-- Settings: join_algorithm=partial_merge, max_execution_time=600

WITH
  -------------------------------------------------------------------
  -- 1. Compustat gvkey -> (cusip8, tic) map for the firm-years in
  --    our panel. Restrict to FYR in [6,12] and the year range that
  --    covers fyear=1974..1992 (so we get FY1 forecasts for the
  --    1976..1993 portfolio-formation window).
  -------------------------------------------------------------------
  comp_id AS (
      SELECT DISTINCT
             gvkey,
             fyear,
             LEFT(cusip, 8) AS cusip8,
             tic
      FROM comp_202601.funda
      WHERE fyear BETWEEN 1974 AND 1992
        AND indfmt = 'INDL'
        AND consol = 'C'
        AND popsrc = 'D'
        AND datafmt = 'STD'
        AND fyr BETWEEN 6 AND 12
        AND ceq IS NOT NULL AND ceq > 0
        AND ib IS NOT NULL
        AND dvc IS NOT NULL
        AND at IS NOT NULL
        AND cusip IS NOT NULL AND cusip != ''
        AND tic IS NOT NULL AND tic != ''
  ),

  -------------------------------------------------------------------
  -- 2. CUSIP-based FY1 FY2 LTG: match by LEFT(cusip,8) on IBES.
  -------------------------------------------------------------------
  ibes_via_cusip AS (
      SELECT DISTINCT
             c.gvkey                          AS gvkey,
             c.fyear                          AS fyear,
             anyIf(s.meanest,
                   s.fpi = '1'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS fy1_eps,
             anyIf(s.meanest,
                   s.fpi = '2'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 2
                   AND s.meanest IS NOT NULL
             )                               AS fy2_eps,
             anyIf(s.meanest,
                   s.measure = 'LTG'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.statpers)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS ltg
      FROM comp_id AS c
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON c.cusip8 = s.cusip
      GROUP BY c.gvkey, c.fyear
  ),

  -------------------------------------------------------------------
  -- 3. Ticker-based FY1 FY2 LTG fallback: match comp.tic to
  --    IBES.id.ticker, then look up statsumu_epsus by ticker.
  -------------------------------------------------------------------
  ibes_via_tic AS (
      SELECT DISTINCT
             c.gvkey                          AS gvkey,
             c.fyear                          AS fyear,
             anyIf(s.meanest,
                   s.fpi = '1'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS fy1_eps,
             anyIf(s.meanest,
                   s.fpi = '2'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 2
                   AND s.meanest IS NOT NULL
             )                               AS fy2_eps,
             anyIf(s.meanest,
                   s.measure = 'LTG'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.statpers)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS ltg
      FROM comp_id AS c
      INNER JOIN ibes_202601.id AS i
          ON c.tic = i.ticker
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON s.ticker = i.ticker
      WHERE i.ticker != ''
      GROUP BY c.gvkey, c.fyear
  ),

  -------------------------------------------------------------------
  -- 4. Officer-ticker-based FY1 FY2 LTG fallback: comp.tic = IBES.oftic
  --    via IBES.id. Recovers firms whose IBES-tracked ticker and
  --    Compustat-tracked officer ticker differ.
  -------------------------------------------------------------------
  ibes_via_oftic AS (
      SELECT DISTINCT
             c.gvkey                          AS gvkey,
             c.fyear                          AS fyear,
             anyIf(s.meanest,
                   s.fpi = '1'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS fy1_eps,
             anyIf(s.meanest,
                   s.fpi = '2'
                   AND s.measure = 'EPS'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.fpedats)) = c.fyear + 2
                   AND s.meanest IS NOT NULL
             )                               AS fy2_eps,
             anyIf(s.meanest,
                   s.measure = 'LTG'
                   AND toMonth(toDate32OrNull(s.statpers)) = 5
                   AND toYear(toDate32OrNull(s.statpers)) = c.fyear + 1
                   AND s.meanest IS NOT NULL
             )                               AS ltg
      FROM comp_id AS c
      INNER JOIN ibes_202601.id AS i
          ON c.tic = i.oftic
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON s.ticker = i.ticker
      WHERE i.oftic != ''
      GROUP BY c.gvkey, c.fyear
  ),

  -------------------------------------------------------------------
  -- 5. Union of the three IBES-coverage sources. Aggregate to one row
  --    per (gvkey, fyear) using coalesce so each forecast column has
  --    the first non-NULL across the three sources.
  -------------------------------------------------------------------
  ibes_all AS (
      SELECT gvkey, fyear, fy1_eps, fy2_eps, ltg FROM ibes_via_cusip
      UNION ALL
      SELECT gvkey, fyear, fy1_eps, fy2_eps, ltg FROM ibes_via_tic
      UNION ALL
      SELECT gvkey, fyear, fy1_eps, fy2_eps, ltg FROM ibes_via_oftic
  )

SELECT
  gvkey,
  fyear,
  any(fy1_eps) AS fy1_eps,
  any(fy2_eps) AS fy2_eps,
  any(ltg)     AS ltg
FROM ibes_all
GROUP BY gvkey, fyear
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
