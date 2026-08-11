-- ibes_link.sql
-- Purpose: DIAGNOSTIC for audit [M6] / assumption 28. Measures the
--          Compustat -> IBES linking coverage under three alternative
--          link paths, at the (gvkey, fyear) firm-year level over the
--          paper's 1984-2002 window:
--            (a) ibtic   : comp_202601.security.ibtic  = ibes.ticker
--            (b) cusip   : comp_202601.security.cusip[1:8] = ibes.cusip
--                          (the audit's proposed fix — note that
--                          security.cusip is the CURRENT CUSIP only,
--                          with no history)
--            (c) ncusip  : gvkey -> permno (ccmxpf_linktable) ->
--                          crsp_202601.dsenames.ncusip[1:8] = ibes.cusip
--                          (point-in-time CUSIP; the ICLINK-style path)
--          plus the union of (a) and (c) which is what panel.sql uses.
--
-- Tables: comp_202601.funda, comp_202601.company, comp_202601.security,
--         crsp_202601.ccmxpf_linktable, crsp_202601.dsenames,
--         ibes_202601.statsumu_epsus
-- Output columns: comp_firmyears, cov_ibtic, cov_cusip, cov_ncusip,
--                 cov_union_ibtic_ncusip (all counts of firm-years)
-- Depends on: (none)
-- Settings: max_execution_time=900, join_algorithm=partial_merge

WITH
  comp_u AS (
    -- The Compustat "denominator": non-financial INDL/C/D/STD firm-years
    -- with the fundamentals the panel requires, 1984-2002.
    SELECT DISTINCT f.gvkey AS gvkey, f.fyear AS fyear
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.at IS NOT NULL AND f.oiadp IS NOT NULL
      AND f.sale IS NOT NULL AND f.sale > 0
      AND c.sic IS NOT NULL
      AND NOT (toInt32OrZero(c.sic) BETWEEN 6000 AND 6999)
  ),
  ib AS (
    SELECT DISTINCT
      ticker,
      substring(cusip, 1, 8) AS cusip8,
      toInt32OrZero(substring(fpedats, 1, 4)) AS fy
    FROM ibes_202601.statsumu_epsus
    WHERE fpedats IS NOT NULL
      AND toInt32OrZero(substring(fpedats, 1, 4)) BETWEEN 1984 AND 2002
  ),
  gv2ncusip AS (
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
  cov_ibtic AS (
    SELECT DISTINCT s.gvkey AS gvkey, i.fy AS fyear
    FROM comp_202601.security AS s
    INNER JOIN ib AS i ON i.ticker = s.ibtic
    WHERE s.ibtic IS NOT NULL AND s.ibtic != ''
  ),
  cov_cusip AS (
    SELECT DISTINCT s.gvkey AS gvkey, i.fy AS fyear
    FROM comp_202601.security AS s
    INNER JOIN ib AS i ON i.cusip8 = substring(s.cusip, 1, 8)
    WHERE s.cusip IS NOT NULL AND s.cusip != ''
  ),
  cov_ncusip AS (
    SELECT DISTINCT g.gvkey AS gvkey, i.fy AS fyear
    FROM gv2ncusip AS g
    INNER JOIN ib AS i ON i.cusip8 = g.cusip8
  )
SELECT
  count() AS comp_firmyears,
  countIf((gvkey, fyear) IN (SELECT gvkey, fyear FROM cov_ibtic))  AS cov_ibtic,
  countIf((gvkey, fyear) IN (SELECT gvkey, fyear FROM cov_cusip))  AS cov_cusip,
  countIf((gvkey, fyear) IN (SELECT gvkey, fyear FROM cov_ncusip)) AS cov_ncusip,
  countIf((gvkey, fyear) IN (SELECT gvkey, fyear FROM cov_ibtic)
       OR (gvkey, fyear) IN (SELECT gvkey, fyear FROM cov_ncusip)) AS cov_union_ibtic_ncusip
FROM comp_u
SETTINGS max_execution_time = 900,
         join_algorithm = 'partial_merge',
         max_rows_to_read = 2000000000,
         timeout_before_checking_execution_speed = 0
