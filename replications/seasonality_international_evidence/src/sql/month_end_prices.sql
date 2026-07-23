-- month_end_prices.sql
-- Purpose: MONTH-END price panel for the international equity universe.
--          For each (gvkey, iid, calendar month) take the row with the LAST
--          datadate carrying a positive price (prccd IS NOT NULL AND prccd > 0),
--          carrying prccd, ajexdi, cshoc, curcdd from that month-end row.
--          Then compute:
--            * adj      = prccd / ajexdi            (split/dividend-adjusted price;
--                                                  ajexdi accumulates upward, verified)
--            * ret_local = adj_t / adj_{t-1} - 1     (t-1 = IMMEDIATELY preceding
--                          calendar month; NULL if that month is missing for the
--                          security — multi-month gaps are NOT bridged)
--            * cshoc    = last-non-missing shares outstanding carried FORWARD
--                         within (gvkey, iid) (Assumption A10)
--          Month is represented as the LAST-DAY-OF-MONTH Date.
--
-- Tables: comp_202601.g_secd (global daily, 305M rows),
--         comp_202601.secd   (NA daily, 159M rows),
--         comp_202601.g_company (global universe), comp_202601.security (CAN universe)
-- Output columns: gvkey, iid, country, month (Date, last-day), prccd, ajexdi,
--                 cshoc (forward-filled), curcdd, curcdd_prev, month_prev, ret_local
-- Depends on: universe_global, universe_canada (inlined as CTEs below)
-- Settings: join_algorithm=hash (small universe -> large daily fact),
--           max_execution_time, max_rows_to_read guards. ALWAYS filtered on datadate.
--
-- Data window: datadate 1979-12-01 .. 2006-06-30 (panel starts 1979-12 so the
-- lag-60 signal for the first reported month, Feb 1985, is available).
WITH
glob_uni AS (
    SELECT gvkey, prirow AS iid, loc AS country
    FROM comp_202601.g_company
    WHERE loc IN ('AUT','BEL','FIN','FRA','DEU','ITA','JPN','NLD','NOR','ESP','SWE','CHE','GBR')
      AND gvkey IS NOT NULL AND prirow IS NOT NULL
),
-- CANADA universe: exactly ONE issue per gvkey (finding F6). Pick the iid with
-- the LARGEST total market cap over the sample (sum of month-end prccd x cshoc,
-- NULLs skipped); tie-break on the lexicographically smallest iid. Mirrors
-- universe_canada.sql so the two stay consistent.
can_issues AS (
    -- Canadian issues, excluding firms domiciled in the 13 global countries
    -- (those enter via glob_uni; keeps the two sources disjoint per gvkey, F6).
    SELECT DISTINCT gvkey, iid
    FROM comp_202601.security
    WHERE excntry = 'CAN' AND gvkey IS NOT NULL AND iid IS NOT NULL
      AND gvkey NOT IN (
          SELECT gvkey FROM comp_202601.g_company
          WHERE loc IN ('AUT','BEL','FIN','FRA','DEU','ITA','JPN','NLD','NOR','ESP','SWE','CHE','GBR')
            AND gvkey IS NOT NULL
      )
),
can_me AS (
    SELECT
        s.gvkey AS gvkey, s.iid AS iid,
        toDate(toStartOfMonth(toDate(s.datadate)) + INTERVAL 1 MONTH - INTERVAL 1 DAY) AS month,
        argMax(s.prccd, s.datadate) AS prccd,
        argMax(s.cshoc, s.datadate) AS cshoc
    FROM comp_202601.secd AS s
    INNER JOIN can_issues AS ci ON s.gvkey = ci.gvkey AND s.iid = ci.iid
    WHERE s.datadate >= '1979-12-01' AND s.datadate <= '2006-06-30'
      AND s.prccd IS NOT NULL AND s.prccd > 0
    GROUP BY s.gvkey, s.iid, month
),
can_tot AS (
    SELECT gvkey, iid,
           sum(if(cshoc IS NOT NULL AND cshoc > 0, prccd * cshoc, 0)) AS tot_me
    FROM can_me
    GROUP BY gvkey, iid
),
can_uni AS (
    SELECT gvkey, iid, 'CAN' AS country
    FROM (
        SELECT gvkey, iid,
               row_number() OVER (PARTITION BY gvkey ORDER BY tot_me DESC, iid ASC) AS rn
        FROM can_tot
    )
    WHERE rn = 1
),
-- month-end aggregation, GLOBAL: last trading day with a positive price per month
gme AS (
    SELECT
        s.gvkey AS gvkey, s.iid AS iid, u.country AS country,
        toDate(toStartOfMonth(toDate(s.datadate)) + INTERVAL 1 MONTH - INTERVAL 1 DAY) AS month,
        argMax(s.prccd,  s.datadate) AS prccd,
        argMax(s.ajexdi, s.datadate) AS ajexdi,
        argMax(s.cshoc,  s.datadate) AS cshoc,
        argMax(s.curcdd, s.datadate) AS curcdd
    FROM comp_202601.g_secd AS s
    INNER JOIN glob_uni AS u ON s.gvkey = u.gvkey AND s.iid = u.iid
    WHERE s.datadate >= '1979-12-01' AND s.datadate <= '2006-06-30'
      AND s.prccd IS NOT NULL AND s.prccd > 0
    GROUP BY s.gvkey, s.iid, u.country, month
),
-- month-end aggregation, CANADA
cme AS (
    SELECT
        s.gvkey AS gvkey, s.iid AS iid, u.country AS country,
        toDate(toStartOfMonth(toDate(s.datadate)) + INTERVAL 1 MONTH - INTERVAL 1 DAY) AS month,
        argMax(s.prccd,  s.datadate) AS prccd,
        argMax(s.ajexdi, s.datadate) AS ajexdi,
        argMax(s.cshoc,  s.datadate) AS cshoc,
        argMax(s.curcdd, s.datadate) AS curcdd
    FROM comp_202601.secd AS s
    INNER JOIN can_uni AS u ON s.gvkey = u.gvkey AND s.iid = u.iid
    WHERE s.datadate >= '1979-12-01' AND s.datadate <= '2006-06-30'
      AND s.prccd IS NOT NULL AND s.prccd > 0
    GROUP BY s.gvkey, s.iid, u.country, month
),
me AS (
    SELECT * FROM gme
    UNION ALL
    SELECT * FROM cme
),
-- window pass: adjusted price, 1-month lags (adjusted price, its month tag, and
-- the security's own prior-month currency) and the running count of non-null
-- cshoc (group id used to forward-fill cshoc). curcdd_prev is carried so the USD
-- return can use the security's OWN prior-month currency for the FX denominator
-- (essential at currency redenominations, e.g. the 1999 euro transition, where
-- curcdd switches FRF/DEM/ITL/.. -> EUR and prccd redenominates but ajexdi does
-- not adjust — the FX ratio usd_per_x(curcdd_t,t)/usd_per_x(curcdd_{t-1},t-1)
-- exactly cancels the redenomination so ret_usd stays correct).
w AS (
    SELECT
        gvkey, iid, country, month, prccd, ajexdi, cshoc, curcdd,
        if(ajexdi IS NOT NULL AND ajexdi > 0, prccd / ajexdi, NULL) AS adj,
        lagInFrame(if(ajexdi IS NOT NULL AND ajexdi > 0, prccd / ajexdi, NULL), 1) OVER ww AS adj_prev,
        lagInFrame(month, 1)  OVER ww AS month_prev,
        lagInFrame(curcdd, 1) OVER ww AS curcdd_prev,
        count(cshoc) OVER ww AS cshoc_grp
    FROM me
    WINDOW ww AS (PARTITION BY gvkey, iid ORDER BY month
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
),
-- forward-fill cshoc: within each (gvkey, iid, cshoc_grp) the first row carries
-- the (only) non-null shares value; max() propagates it to the trailing nulls.
ff AS (
    SELECT
        gvkey, iid, country, month, prccd, ajexdi, curcdd, curcdd_prev, month_prev,
        adj, adj_prev,
        max(cshoc) OVER (PARTITION BY gvkey, iid, cshoc_grp) AS cshoc
    FROM w
)
SELECT
    gvkey, iid, country, month, prccd, ajexdi, cshoc, curcdd, curcdd_prev, month_prev,
    if(month_prev = toDate(toStartOfMonth(month) - 1) AND adj_prev > 0 AND adj > 0,
       adj / adj_prev - 1, NULL) AS ret_local
FROM ff
SETTINGS join_algorithm = 'hash',
         max_execution_time = 2400,
         max_rows_to_read = 500000000000,
         timeout_before_checking_execution_speed = 0
