-- ibes_analyst.sql
-- Purpose: Build Anal_REV_t (analyst forecast revision), SUR_t (annual
--          earnings surprise) and FE_{t+1} (next-year forecast error) for
--          each (gvkey, fyear) in the panel, using IBES consensus snapshots
--          + IBES actuals + IBES EARNINGS ANNOUNCEMENT DATES.
--
-- Definitions (paper §II):
--   Anal_REV_t = first median consensus of FY t+1 EPS made AFTER the year-t
--                earnings announcement - last median consensus of FY t+1 EPS
--                made BEFORE the year-t earnings announcement, scaled by
--                stock price (scaling done in main.py). Paper L460.
--   SUR_t      = realized annual IBES earnings for year t - most recent
--                pre-announcement median forecast of FY t EPS. Paper L397.
--   FE_{t+1}   = realized FY t+1 EPS - the median FY t+1 consensus from the
--                MONTH PRIOR TO THE ANNOUNCEMENT OF t+1 EARNINGS. Paper L480.
--
-- ─── audit [M5] fix (assumption 25) ────────────────────────────────────────
-- Iteration 2 used the Compustat `datadate` (fiscal year END) as the
-- announcement boundary for all three variables. That is 1.5-3 months EARLY:
-- the median IBES annual EPS announcement lands 47 days after the fiscal
-- period end (p25=33d, p75=79d). For FE_{t+1} in particular, using
-- datadate(t+1) picks a consensus formed ~2 months before the announcement
-- instead of the month immediately prior, which inflates the dispersion of
-- FE and therefore every Table 9 coefficient.
--
-- This version uses the IBES earnings-announcement date as the primary
-- boundary and falls back to the Compustat datadate when the announcement
-- date is missing:
--     boundary_t     = coalesce(anndats of the FY-t   announcement, datadate_t)
--     boundary_next  = coalesce(anndats of the FY-t+1 announcement, datadate_next)
--
-- SOURCE OF anndats — deviation from the audit's literal instruction. The
-- audit asked for `ibes_202601.detu_epsus.anndats`. In the IBES DETAIL file
-- `anndats` is the date the ANALYST ANNOUNCED THE ESTIMATE, not the date the
-- company announced earnings; it is the wrong field for this boundary (and
-- detu_epsus is 35M rows). The correct field is the announcement date
-- attached to the ACTUAL: `ibes_202601.actu_epsus` (unadjusted US actuals,
-- pdicity='ANN', measure='EPS') carries (pends, anndats, value) — the fiscal
-- period end, the earnings announcement date, and the realized EPS. That is
-- what is used here. `surpsumu.anndats` carries the same information but is
-- keyed on (pyear, pmon) rather than the period-end date.
--
-- ─── period matching ──────────────────────────────────────────────────────
-- IBES periods are matched to Compustat fiscal years on the (year, month) of
-- the period-end date rather than on the fiscal-year LABEL. Compustat's
-- `fyear` for a fiscal year ending Jan-May of calendar year Y is Y-1, while
-- IBES's `pyear` is Y — matching on labels mis-aligns those firms by one
-- year. Matching `toYYYYMM(pends) = toYYYYMM(datadate)` is label-free.
--
-- ─── gvkey -> IBES ticker link (assumption 28, audit [M6]) ────────────────
-- Union of (a) comp_202601.security.ibtic and (b) gvkey -> permno ->
-- crsp_202601.dsenames.ncusip (8-char, point-in-time) = ibes cusip. Path (a)
-- takes priority when both exist. See src/sql/ibes_link.sql for the coverage
-- comparison.
--
-- Tables: comp_202601.funda, comp_202601.security,
--         crsp_202601.ccmxpf_linktable, crsp_202601.dsenames,
--         ibes_202601.statsumu_epsus, ibes_202601.actu_epsus
--
-- Output columns:
--   gvkey (String), fyear (Int32),
--   Anal_REV_raw, SUR_raw, FE_raw            -- anndats boundary (primary)
--   Anal_REV_raw_dd, SUR_raw_dd, FE_raw_dd   -- datadate boundary (iteration-2
--                                               proxy, kept for the before/after
--                                               diagnostic in assumption 25)
--   has_anndats_t, has_anndats_next          -- UInt8 boundary-source flags
--
-- Depends on: ibes_link.sql (linking logic, replicated here as CTEs)
-- Settings: max_execution_time=900, join_algorithm=partial_merge

WITH
  -- ── Step 0: gvkey -> IBES ticker (union link, ibtic preferred) ──────────
  ibes_ticker_universe AS (
    SELECT DISTINCT ticker, substring(cusip, 1, 8) AS cusip8
    FROM ibes_202601.statsumu_epsus
    WHERE ticker IS NOT NULL AND cusip IS NOT NULL AND cusip != ''
  ),
  gvkey_ncusip AS (
    SELECT DISTINCT
      l.gvkey                   AS gvkey,
      substring(n.ncusip, 1, 8) AS cusip8
    FROM crsp_202601.ccmxpf_linktable AS l
    INNER JOIN crsp_202601.dsenames AS n
      ON n.permno = toInt32(l.lpermno)
    WHERE l.linktype IN ('LC', 'LU') AND l.linkprim IN ('P', 'C')
      AND l.lpermno IS NOT NULL AND l.gvkey IS NOT NULL
      AND n.ncusip IS NOT NULL AND n.ncusip != ''
  ),
  link_candidates AS (
    SELECT s.gvkey AS gvkey, s.ibtic AS ticker, 1 AS pri
    FROM comp_202601.security AS s
    WHERE s.gvkey IS NOT NULL AND s.ibtic IS NOT NULL AND s.ibtic != ''
    UNION ALL
    SELECT g.gvkey AS gvkey, t.ticker AS ticker, 2 AS pri
    FROM gvkey_ncusip AS g
    INNER JOIN ibes_ticker_universe AS t ON t.cusip8 = g.cusip8
  ),
  ibes_link AS (
    -- One ticker per gvkey; ibtic (pri=1) wins over the ncusip path (pri=2).
    SELECT gvkey, argMin(ticker, pri) AS ticker
    FROM link_candidates
    GROUP BY gvkey
  ),
  -- ── Step 1: (gvkey, fyear, datadate) skeleton + next year's datadate ────
  comp_min AS (
    SELECT gvkey, fyear, toDate32OrNull(datadate) AS datadate
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D'
      AND datafmt = 'STD' AND fyear BETWEEN 1984 AND 2003
      AND datadate IS NOT NULL
  ),
  comp_panel AS (
    SELECT gvkey, fyear, datadate
    FROM (
      SELECT gvkey, fyear, datadate,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_min
    )
    WHERE rn = 1
  ),
  comp_next AS (
    SELECT
      p.gvkey       AS gvkey,
      p.fyear       AS fyear,
      p.datadate    AS datadate,
      n.datadate    AS datadate_next,
      l.ticker      AS ticker
    FROM comp_panel AS p
    INNER JOIN ibes_link AS l ON l.gvkey = p.gvkey
    LEFT JOIN comp_panel AS n
      ON n.gvkey = p.gvkey AND n.fyear = p.fyear + 1
    WHERE p.fyear BETWEEN 1984 AND 2002
  ),
  -- ── Step 2: IBES annual actuals + earnings announcement dates ──────────
  actuals AS (
    SELECT
      ticker,
      pend_ym,
      min(ann_d)                AS anndats,
      argMin(eps_value, ann_d)  AS actual_eps
    FROM (
      SELECT
        ticker,
        toYYYYMM(toDate32OrNull(pends)) AS pend_ym,
        toDate32OrNull(anndats)         AS ann_d,
        value                           AS eps_value
      FROM ibes_202601.actu_epsus
      WHERE pdicity = 'ANN' AND measure = 'EPS'
        AND pends IS NOT NULL AND value IS NOT NULL
        AND toDate32OrNull(pends) BETWEEN toDate32('1984-01-01')
                                      AND toDate32('2004-12-31')
    )
    GROUP BY ticker, pend_ym
  ),
  -- ── Step 3: IBES monthly consensus snapshots (annual EPS, USD) ─────────
  snaps AS (
    SELECT
      ticker,
      toYYYYMM(toDate32OrNull(fpedats)) AS fpe_ym,
      toDate32OrNull(statpers)          AS stat_d,
      medest
    FROM ibes_202601.statsumu_epsus
    WHERE measure = 'EPS' AND fiscalp = 'ANN' AND curcode = 'USD'
      AND medest IS NOT NULL AND fpedats IS NOT NULL AND statpers IS NOT NULL
      AND toDate32OrNull(fpedats) BETWEEN toDate32('1984-01-01')
                                      AND toDate32('2004-12-31')
  ),
  -- ── Step 4: attach the two announcement boundaries to each firm-year ───
  bounds AS (
    SELECT
      c.gvkey         AS gvkey,
      c.fyear         AS fyear,
      c.ticker        AS ticker,
      c.datadate      AS datadate,
      c.datadate_next AS datadate_next,
      a0.anndats      AS anndats_t,
      a1.anndats      AS anndats_next,
      a0.actual_eps   AS actual_t,
      a1.actual_eps   AS actual_next,
      -- Primary boundary = IBES announcement date; fallback = Compustat
      -- fiscal year-end (the iteration-2 proxy).
      coalesce(a0.anndats, c.datadate)      AS bound_t,
      coalesce(a1.anndats, c.datadate_next) AS bound_next
    FROM comp_next AS c
    LEFT JOIN actuals AS a0
      ON a0.ticker = c.ticker AND a0.pend_ym = toYYYYMM(c.datadate)
    LEFT JOIN actuals AS a1
      ON a1.ticker = c.ticker AND a1.pend_ym = toYYYYMM(c.datadate_next)
  ),
  -- ── Step 5: FY t+1 consensus snapshots (drive Anal_REV and FE) ─────────
  snaps_next AS (
    SELECT
      b.gvkey, b.fyear,
      b.bound_t, b.bound_next, b.datadate, b.datadate_next,
      s.stat_d   AS statpers,
      s.medest   AS medest
    FROM bounds AS b
    INNER JOIN snaps AS s
      ON s.ticker = b.ticker AND s.fpe_ym = toYYYYMM(b.datadate_next)
  ),
  next_agg AS (
    -- bound_t / bound_next / datadate / datadate_next are constant within
    -- (gvkey, fyear), so they go in the GROUP BY and can be referenced
    -- directly inside the FILTER predicates.
    SELECT
      gvkey, fyear,
      -- Anal_REV, anndats boundary
      argMax(medest, statpers) FILTER (WHERE statpers <  bound_t) AS rev_pre,
      argMin(medest, statpers) FILTER (WHERE statpers >= bound_t) AS rev_post,
      -- Anal_REV, datadate boundary (iteration-2 proxy)
      argMax(medest, statpers) FILTER (WHERE statpers <= datadate)  AS rev_pre_dd,
      argMin(medest, statpers) FILTER (WHERE statpers >  datadate)  AS rev_post_dd,
      -- FE, anndats boundary: last consensus strictly before the t+1
      -- earnings announcement = "the month prior to the announcement".
      argMax(medest, statpers) FILTER (WHERE statpers < bound_next) AS fe_pre,
      -- FE, datadate boundary (iteration-2 proxy)
      argMax(medest, statpers) FILTER (WHERE statpers < datadate_next) AS fe_pre_dd
    FROM snaps_next
    GROUP BY gvkey, fyear, bound_t, bound_next, datadate, datadate_next
  ),
  -- ── Step 6: FY t consensus snapshots (drive SUR) ───────────────────────
  snaps_cur AS (
    SELECT
      b.gvkey, b.fyear, b.bound_t, b.datadate,
      s.stat_d   AS statpers,
      s.medest   AS medest
    FROM bounds AS b
    INNER JOIN snaps AS s
      ON s.ticker = b.ticker AND s.fpe_ym = toYYYYMM(b.datadate)
  ),
  cur_agg AS (
    SELECT
      gvkey, fyear,
      argMax(medest, statpers) FILTER (WHERE statpers <  bound_t) AS sur_pre,
      argMax(medest, statpers) FILTER (WHERE statpers <= datadate) AS sur_pre_dd
    FROM snaps_cur
    GROUP BY gvkey, fyear, bound_t, datadate
  )
SELECT
  b.gvkey                        AS gvkey,
  toInt32(b.fyear)               AS fyear,
  n.rev_post - n.rev_pre         AS Anal_REV_raw,
  b.actual_t - c.sur_pre         AS SUR_raw,
  b.actual_next - n.fe_pre       AS FE_raw,
  n.rev_post_dd - n.rev_pre_dd   AS Anal_REV_raw_dd,
  b.actual_t - c.sur_pre_dd      AS SUR_raw_dd,
  b.actual_next - n.fe_pre_dd    AS FE_raw_dd,
  toUInt8(b.anndats_t    IS NOT NULL) AS has_anndats_t,
  toUInt8(b.anndats_next IS NOT NULL) AS has_anndats_next
FROM bounds AS b
LEFT JOIN next_agg AS n ON n.gvkey = b.gvkey AND n.fyear = b.fyear
LEFT JOIN cur_agg  AS c ON c.gvkey = b.gvkey AND c.fyear = b.fyear
SETTINGS max_execution_time = 900,
         join_algorithm = 'partial_merge',
         max_rows_to_read = 2000000000,
         timeout_before_checking_execution_speed = 0
