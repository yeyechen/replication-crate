-- ibes_join.sql
-- Purpose: Build the IBES coverage flag — for each (gvkey, fyear), whether
--          the firm has any IBES annual-EPS record whose fiscal period end
--          (fpedats) falls in fiscal year t.
-- Tables: comp_202601.security (gvkey -> IBES ticker via ibtic),
--         crsp_202601.ccmxpf_linktable + crsp_202601.dsenames
--           (gvkey -> permno -> point-in-time 8-char ncusip),
--         ibes_202601.statsumu_epsus (consensus snapshots; ticker + cusip)
-- Output columns: gvkey (String), fyear (Int32)
-- Depends on: (none — the same logic is folded into panel.sql as CTEs)
-- Settings: max_execution_time=900, join_algorithm=partial_merge
--
-- Linking strategy (assumption 28, audit [M6]). Two paths, unioned:
--   (a) comp_202601.security.ibtic = ibes.ticker. Compustat-native IBES
--       ticker; 26,487 of 56,858 gvkeys carry one.
--   (b) gvkey -> permno (CRSP-Compustat link) -> dsenames.ncusip (8-char,
--       point-in-time) = ibes.cusip.
-- The audit proposed joining comp_202601.security.cusip to the IBES cusip
-- directly. That was tested (see src/sql/ibes_link.sql) and RECOVERS FEWER
-- firm-years than ibtic (47,250 vs 65,988 over 1984-2002), because
-- security.cusip stores only the CURRENT CUSIP with no history, while IBES
-- carries the CUSIP that was in force at the snapshot date. Routing the
-- CUSIP match through CRSP's historical ncusip fixes that (68,930), and the
-- union of (a) and (b) gives 69,831 firm-years (+5.8% over ibtic alone).

WITH
  ibes_ticker_universe AS (
    SELECT DISTINCT
      ticker,
      substring(cusip, 1, 8) AS cusip8,
      toInt32OrZero(substring(fpedats, 1, 4)) AS fy
    FROM ibes_202601.statsumu_epsus
    WHERE fpedats IS NOT NULL
      AND toInt32OrZero(substring(fpedats, 1, 4)) BETWEEN 1984 AND 2002
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
  )
SELECT DISTINCT gvkey, fyear
FROM (
  SELECT s.gvkey AS gvkey, t.fy AS fyear
  FROM comp_202601.security AS s
  INNER JOIN ibes_ticker_universe AS t ON t.ticker = s.ibtic
  WHERE s.gvkey IS NOT NULL AND s.ibtic IS NOT NULL AND s.ibtic != ''
  UNION ALL
  SELECT g.gvkey AS gvkey, t.fy AS fyear
  FROM gvkey_ncusip AS g
  INNER JOIN ibes_ticker_universe AS t ON t.cusip8 = g.cusip8
)
SETTINGS max_execution_time = 900,
         join_algorithm = 'partial_merge',
         max_rows_to_read = 2000000000,
         timeout_before_checking_execution_speed = 0
