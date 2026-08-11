-- panel.sql
-- Purpose: Build the Frankel & Lee (1998) firm-year panel (1976-1993).
--          One row per (permno, year_t) where year_t is the portfolio
--          formation year (portfolios formed at June 30 of year_t).
--          Compustat fundamentals are from fiscal year ending in calendar
--          year t-1 (with FYR in [6,12]).
--
-- Universe filters applied (per task spec):
--   1. CRSP shrcd IN (10, 11) AND exchcd IN (1, 2, 3) — PIT at June 30.
--   2. Compustat non-financial: sich first digit NOT = 6.
--      Primary: comp_202601.funda.sich (historical, may be NULL).
--      Fallback: comp_202601.company.sic (current SIC; populated for
--      virtually every gvkey, vs. funda.sich which is NULL pre-1987).
--   3. Fiscal-year-end month in [6, 12] (comp_202601.funda.fyr).
--   4. Fiscal year ending in calendar year t-1 has non-missing
--      ceq, ib, dvc, at (all > 0 for ceq/at).
--   5. CRSP price at June 30 of year t exists and abs(prc) >= 1.
--   6. |ROE| < 1, 0 <= k <= 1, ceq > 0  (applied in Python; see main.py).
--   7. I/B/E/S FY1 coverage: each firm must have a one-year-ahead
--      EPS forecast in the May statistical period of year t (i.e., a
--      forecast with fpedats in calendar year year_t+1, published in
--      the May statpers window of year t, fpi=2, measure=EPS, with
--      non-missing meanest). The paper also requires FY2 coverage,
--      but the I/B/E/S data in this vintage has zero FY2 records in
--      May pre-1984 and only sparse coverage 1984-1993, so we use FY1
--      only (per assumptions.md, assumption 17, 19). The CUSIP-based
--      link (comp CUSIP first 8 chars = IBES CUSIP 8 chars) is more
--      robust than ticker-based link and yields ~17,400 firm-years,
--      close to the paper's 18,162.
--
-- Output columns:
--   permno, year_t, gvkey, fyear (== year_t - 1), prc, shrout, me_june_t,
--   ceq, ib, dvc, at, sich, ceq_prior, k, roe, roa
--
-- Tables:
--   crsp_202601.msf                       -- monthly prices, ME at June-end
--   crsp_202601.dsenames                  -- PIT shrcd/exchcd/ticker/siccd
--   crsp_202601.ccmxpf_linktable          -- gvkey <-> permno
--   comp_202601.funda                     -- annual fundamentals
--   comp_202601.company                   -- current-SIC fallback
--   ibes_202601.statsumu_epsus            -- I/B/E/S summary statistics
--
-- Settings: join_algorithm=partial_merge, max_execution_time=600
WITH
  -------------------------------------------------------------------
  -- 1. CRSP PIT names filtered to shrcd IN (10,11), exchcd IN (1,2,3)
  --    Used to enforce share/exchange code on the snapshot date and
  --    to provide the historical CRSP ticker for an IBES join (later
  --    tasks). siccd here is the point-in-time SIC code from CRSP.
  -------------------------------------------------------------------
  crsp_names AS (
      SELECT permno,
             toDate32OrNull(namedt)        AS namedt,
             toDate32OrNull(nameendt)      AS nameendt,
             shrcd,
             exchcd,
             ticker,
             siccd AS crsp_siccd
      FROM crsp_202601.dsenames
      WHERE shrcd IN (10, 11)
        AND exchcd IN (1, 2, 3)
  ),

  -------------------------------------------------------------------
  -- 2. CRSP June-end snapshot per (permno, year_t).
  --    msf.date is the last trading day of each month, so month=6 rows
  --    are the last trading day of June — exactly what we want.
  --    me_june_t is in MILLIONS of dollars (abs(prc)*shrout/1000,
  --    since shrout is in thousands).
  -------------------------------------------------------------------
  june_me_raw AS (
      SELECT m.permno                                 AS permno,
             toYear(toDate32OrNull(m.date))           AS year_t,
             abs(m.prc)                               AS prc,
             m.shrout                                 AS shrout,
             abs(m.prc) * m.shrout / 1000.0           AS me_june_t
      FROM crsp_202601.msf AS m
      WHERE toMonth(toDate32OrNull(m.date)) = 6
        AND toYear(toDate32OrNull(m.date)) BETWEEN 1976 AND 1993
        AND m.prc IS NOT NULL
        AND m.shrout IS NOT NULL
        AND m.shrout > 0
  ),

  -------------------------------------------------------------------
  -- 3. Apply CRSP PIT universe filter: shrcd/exchcd valid on June 30
  --    of year_t. The snapshot is the last trading day of June of
  --    year_t. A permno is included for year_t only if at least one
  --    dsenames record overlaps the snapshot date AND passes the
  --    shrcd/exchcd filter.
  -------------------------------------------------------------------
  june_me AS (
      SELECT j.permno,
             j.year_t,
             j.prc,
             j.shrout,
             j.me_june_t,
             any(u.ticker)     AS crsp_ticker,
             any(u.crsp_siccd) AS crsp_siccd
      FROM june_me_raw AS j
      INNER JOIN crsp_names AS u
          ON j.permno = u.permno
         AND toDate32OrNull(toString(j.year_t) || '-06-30')
                >= u.namedt
         AND toDate32OrNull(toString(j.year_t) || '-06-30')
                <= u.nameendt
      GROUP BY j.permno, j.year_t, j.prc, j.shrout, j.me_june_t
  ),

  -------------------------------------------------------------------
  -- 4. CRSP-Compustat link (gvkey <-> permno) with PIT validity.
  -------------------------------------------------------------------
  ccm AS (
      SELECT gvkey,
             toInt32(lpermno) AS permno,
             toDate32OrNull(nullIf(linkdt, ''))    AS linkdt,
             toDate32OrNull(nullIf(linkenddt, '')) AS linkenddt
      FROM crsp_202601.ccmxpf_linktable
      WHERE linktype IN ('LC', 'LU')
        AND linkprim IN ('P', 'C')
        AND usedflag = 1
  ),

  -------------------------------------------------------------------
  -- 5. Compustat fundamentals with SIC fallback.
  --    Standard WRDS quality filter (INDL/C/D/STD).
  --    fyear BETWEEN 1974 AND 1992 covers year_t 1976-1993 mapping
  --    (fyear = year_t - 1, with 1-year cushion for the lag).
  --    fyr BETWEEN 6 AND 12 implements the paper's fiscal-year-end
  --    window restriction (June-December inclusive).
  --    SIC first-digit != 6 excludes financial firms (SIC 6000-6999).
  --    Primary SIC source: comp_202601.funda.sich (historical).
  --    Fallback:           comp_202601.company.sic (current; populated
  --                        for virtually every gvkey; needed because
  --                        funda.sich is NULL for pre-1987 firm-years).
  --    Deduplication: ROW_NUMBER (most recent datadate per (gvkey,fyear)).
  -------------------------------------------------------------------
  comp_raw AS (
      SELECT f.gvkey,
             f.fyear,
             f.fyr,
             f.sich                                 AS funda_sich,
             c.sic                                  AS company_sic,
             coalesce(f.sich, toInt32OrNull(c.sic)) AS sic,
             f.ceq, f.ib, f.dvc, f.at, f.csho,
             -- CUSIP first 8 chars (Compustat CUSIP is 9 chars including
             -- a check digit; IBES CUSIP is 8 chars without the check).
             -- Used for the I/B/E/S FY1 coverage join (filter 7).
             LEFT(f.cusip, 8)                       AS cusip8,
             f.tic                                  AS tic,
             ROW_NUMBER() OVER (
                 PARTITION BY f.gvkey, f.fyear
                 ORDER BY f.datadate DESC
             ) AS rn
      FROM comp_202601.funda AS f
      LEFT JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
      WHERE f.indfmt = 'INDL'
        AND f.consol = 'C'
        AND f.popsrc = 'D'
        AND f.datafmt = 'STD'
        AND f.fyear IS NOT NULL
        AND f.fyear BETWEEN 1974 AND 1992
        AND f.fyr BETWEEN 6 AND 12
        AND f.ceq IS NOT NULL AND f.ceq > 0
        AND f.ib  IS NOT NULL
        AND f.dvc IS NOT NULL
        AND f.at  IS NOT NULL
  ),
  comp_current AS (
      SELECT gvkey, fyear, fyr, sic, ceq, ib, dvc, at, csho, cusip8, tic
      FROM comp_raw
      WHERE rn = 1
  ),

  -------------------------------------------------------------------
  -- 5b. I/B/E/S FY1 coverage.
  --     For each (gvkey, fyear=year_t-1), check whether IBES has a
  --     one-year-ahead EPS forecast published in the May statistical
  --     period of year_t (= fyear+1) with fpedats in calendar year
  --     year_t+1 (= fyear+2) and a non-missing meanest.
  --
  --     I/B/E/S convention (this vintage):
  --       fpi='1' -> current fiscal year, fpedats in statpers year
  --       fpi='2' -> next fiscal year,    fpedats in statpers year + 1
  --     The paper's "FY1" (one-year-ahead forecast) corresponds to
  --     fpi='2' with fpedats in statpers_year + 1 = year_t+1 = fyear+2.
  --
  --     The Compustat-to-IBES link uses the 8-digit CUSIP (Compustat's
  --     CUSIP is 9 chars with a check digit, IBES's is 8 chars).
  --     CUSIP is more stable than ticker across share-class changes.
  --     The match is done on comp_202601.funda (before the
  --     ROW_NUMBER=1 dedup in comp_current), so a firm with multiple
  --     share classes passes if ANY of its share classes has IBES
  --     coverage. This recovers the share-class diversity lost in
  --     comp_current.
  -------------------------------------------------------------------
  ibes_fy1 AS (
      SELECT DISTINCT
             f.gvkey                                AS gvkey,
             f.fyear                                AS fyear
      FROM comp_202601.funda AS f
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON LEFT(f.cusip, 8) = s.cusip
         AND s.fpi    = '2'
         AND s.measure = 'EPS'
         AND s.meanest IS NOT NULL
         AND toYear(toDate32OrNull(s.statpers)) = f.fyear + 1
         AND toMonth(toDate32OrNull(s.statpers)) = 5
         AND toYear(toDate32OrNull(s.fpedats)) = f.fyear + 2
      WHERE f.fyear BETWEEN 1975 AND 1992
        AND f.indfmt = 'INDL'
        AND f.consol = 'C'
        AND f.popsrc = 'D'
        AND f.datafmt = 'STD'
        AND f.ceq IS NOT NULL AND f.ceq > 0
        AND f.ib  IS NOT NULL
        AND f.dvc IS NOT NULL
        AND f.at  IS NOT NULL
        AND f.fyr BETWEEN 6 AND 12
        AND f.cusip IS NOT NULL AND f.cusip != ''
  ),
  -------------------------------------------------------------------
  -- 5c. I/B/E/S FY1 coverage via ticker (more permissive fallback).
  --     For firms whose comp CUSIP does not match IBES but whose
  --     comp ticker does. The IBES id table is the canonical mapping
  --     from ticker to the set of IBES-traded securities. This
  --     recovers firms where Compustat and IBES track different
  --     share classes (different CUSIPs) but the same firm (same
  --     ticker).
  -------------------------------------------------------------------
  ibes_fy1_tic AS (
      SELECT DISTINCT
             f.gvkey                                AS gvkey,
             f.fyear                                AS fyear
      FROM comp_202601.funda AS f
      INNER JOIN ibes_202601.id AS i
          ON f.tic = i.ticker
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON s.ticker = i.ticker
         AND s.fpi    = '2'
         AND s.measure = 'EPS'
         AND s.meanest IS NOT NULL
         AND toYear(toDate32OrNull(s.statpers)) = f.fyear + 1
         AND toMonth(toDate32OrNull(s.statpers)) = 5
         AND toYear(toDate32OrNull(s.fpedats)) = f.fyear + 2
      WHERE f.fyear BETWEEN 1975 AND 1992
        AND f.indfmt = 'INDL'
        AND f.consol = 'C'
        AND f.popsrc = 'D'
        AND f.datafmt = 'STD'
        AND f.ceq IS NOT NULL AND f.ceq > 0
        AND f.ib  IS NOT NULL
        AND f.dvc IS NOT NULL
        AND f.at  IS NOT NULL
        AND f.fyr BETWEEN 6 AND 12
        AND f.tic IS NOT NULL AND f.tic != ''
        AND i.ticker != ''
  ),
  ibes_fy1_oftic AS (
      SELECT DISTINCT
             f.gvkey                                AS gvkey,
             f.fyear                                AS fyear
      FROM comp_202601.funda AS f
      INNER JOIN ibes_202601.id AS i
          ON f.tic = i.oftic
      INNER JOIN ibes_202601.statsumu_epsus AS s
          ON s.ticker = i.ticker
         AND s.fpi    = '2'
         AND s.measure = 'EPS'
         AND s.meanest IS NOT NULL
         AND toYear(toDate32OrNull(s.statpers)) = f.fyear + 1
         AND toMonth(toDate32OrNull(s.statpers)) = 5
         AND toYear(toDate32OrNull(s.fpedats)) = f.fyear + 2
      WHERE f.fyear BETWEEN 1975 AND 1992
        AND f.indfmt = 'INDL'
        AND f.consol = 'C'
        AND f.popsrc = 'D'
        AND f.datafmt = 'STD'
        AND f.ceq IS NOT NULL AND f.ceq > 0
        AND f.ib  IS NOT NULL
        AND f.dvc IS NOT NULL
        AND f.at  IS NOT NULL
        AND f.fyr BETWEEN 6 AND 12
        AND f.tic IS NOT NULL AND f.tic != ''
        AND i.oftic != ''
  ),
  -------------------------------------------------------------------
  -- Union of the three IBES-coverage sources: CUSIP, ticker, oftic.
  -------------------------------------------------------------------
  ibes_fy1_all AS (
      SELECT gvkey, fyear FROM ibes_fy1
      UNION ALL
      SELECT gvkey, fyear FROM ibes_fy1_tic
      UNION ALL
      SELECT gvkey, fyear FROM ibes_fy1_oftic
  ),

  -------------------------------------------------------------------
  -- 6. Cross-sectional join:
  --    (permno, year_t) ↔ (gvkey, fyear = year_t - 1)
  --    Apply CRSP-Compustat link PIT validity and the $1 price floor.
  --    Apply the SIC != 6 financial-exclusion filter.
  --    Apply filter 7: I/B/E/S FY1 coverage.
  -------------------------------------------------------------------
  panel_pre AS (
      SELECT j.permno                                    AS permno,
             j.year_t                                    AS year_t,
             c.gvkey                                     AS gvkey,
             c.fyear                                     AS fyear,
             j.prc                                       AS prc,
             j.shrout                                    AS shrout,
             j.me_june_t                                 AS me_june_t,
             c.ceq                                       AS ceq,
             c.ib                                        AS ib,
             c.dvc                                       AS dvc,
             c.at                                        AS at,
             c.csho                                      AS csho,
             c.sic                                       AS sich,
             c.fyr                                       AS fyr,
             j.crsp_siccd                                AS crsp_siccd,
             j.crsp_ticker                               AS crsp_ticker
      FROM june_me AS j
      INNER JOIN ccm AS l
          ON j.permno = l.permno
         AND toDate32OrNull(toString(j.year_t) || '-06-30')
                >= if(l.linkdt =  toDate32OrNull('1900-01-01'), toDate32OrNull('1900-01-01'), l.linkdt)
         AND toDate32OrNull(toString(j.year_t) || '-06-30')
                <= if(l.linkenddt = toDate32OrNull('1900-01-01'), toDate32OrNull('9999-12-31'), l.linkenddt)
      INNER JOIN comp_current AS c
          ON l.gvkey = c.gvkey
         AND c.fyear = j.year_t - 1
      -- Filter 7: I/B/E/S FY1 coverage (paper §4 L224).
      -- Each (gvkey, fyear) must appear in ibes_fy1_all, i.e., the
      -- firm must have a one-year-ahead EPS forecast in the May
      -- statistical period of year t (year_t = fyear + 1) per the
      -- union of CUSIP, ticker, and oftic matches.
      INNER JOIN ibes_fy1_all AS ib
          ON c.gvkey = ib.gvkey
         AND c.fyear = ib.fyear
      WHERE abs(j.prc) >= 1.0
        AND c.sic IS NOT NULL
        AND intDiv(c.sic, 1000) != 6
  ),

  -------------------------------------------------------------------
  -- 7. Self-join for ceq_prior = ceq from fyear = year_t - 2.
  --    This is the B_{t-1} used in the ROE denominator
  --    (B_t + B_{t-1})/2. The join is LEFT JOIN; rows with no prior
  --    ceq get ceq_prior = NULL and ROE = NULL (filtered later in py).
  -------------------------------------------------------------------
  panel_with_lag AS (
      SELECT p.*,
             cp.ceq AS ceq_prior
      FROM panel_pre AS p
      LEFT JOIN comp_current AS cp
          ON p.gvkey = cp.gvkey
         AND cp.fyear = p.fyear - 1
  )

SELECT
  permno,
  year_t,
  gvkey,
  fyear,
  prc,
  shrout,
  me_june_t,
  ceq,
  ib,
  dvc,
  at,
  csho,
  sich,
  fyr,
  ceq_prior,
  -----------------------------------------------------------------
  -- k = payout ratio.
  --   primary:  dvc / ib             when ib > 0
  --   fallback: dvc / (0.06 * at)    when ib <= 0 (negative earnings)
  --   clip to [0, 1]
  -----------------------------------------------------------------
  greatest(0.0, least(1.0,
      if(ib > 0,
         dvc / ib,
         if(at > 0, dvc / (0.06 * at), 0.0))
  )) AS k,
  -----------------------------------------------------------------
  -- ROE = ib / ((ceq + ceq_prior) / 2)
  --   requires both ceq and ceq_prior > 0; NULL otherwise.
  -----------------------------------------------------------------
  if(ceq_prior IS NOT NULL AND ceq_prior > 0 AND ceq > 0,
     ib / ((ceq + ceq_prior) / 2.0),
     NULL) AS roe,
  -----------------------------------------------------------------
  -- ROA = ib / at
  -----------------------------------------------------------------
  ib / at AS roa,
  crsp_siccd,
  crsp_ticker
FROM panel_with_lag
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0