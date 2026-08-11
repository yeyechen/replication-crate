-- ccm_link.sql
-- Purpose: PIT-join Compustat firm-quarter (from comp_fundamentals) to the
--          CRSP CCM linktable (ccmxpf_linktable) to obtain the permno valid
--          on each firm's quarterly-announcement date (rdq).
--
-- Tables: crsp_202601.ccmxpf_linktable
-- Output columns: gvkey, datadate, rdq, fyearq, fqtr, ibq, atq,
--                 epspxq, ceqq, cshoq, prccq, oancfy, xidocy, permno
-- Depends on: comp_fundamentals.sql
-- Settings: join_algorithm=partial_merge, max_execution_time=600
--
-- Notes:
--   * Standard WRDS-recommended link filter:
--       linktype IN ('LC', 'LU') AND linkprim IN ('P', 'C') AND usedflag = 1
--   * Temporal predicate:
--       toDate32OrNull(c.rdq) >= toDate32OrNull(l.linkdt)
--       AND coalesce(nullIf(l.linkenddt, ''), '2099-12-31') >= c.rdq
--     The nullIf / coalesce handles both NULL and empty-string linkenddt
--     (representing "still active").
--   * A gvkey can have multiple valid permnos at rdq (multiple share classes
--     for the same parent). We dedupe with GROUP BY + any(toInt32(lpermno))
--     so the result is one row per (gvkey, datadate, rdq).
--   * lpermno is Nullable(Float64) in this extract; we cast to Int32 to
--     match crsp_202601.dsf.permno.

WITH comp_fundamentals AS (
    SELECT gvkey, datadate, rdq, fyearq, fqtr,
           ibq, atq, epspxq, ceqq, cshoq, prccq, oancfy, xidocy
    FROM comp_202601.fundq
    WHERE rdq BETWEEN '1976-01-01' AND '2005-12-31'
      AND ibq IS NOT NULL
      AND atq IS NOT NULL
      AND rdq IS NOT NULL
)
SELECT
    c.gvkey,
    c.datadate,
    c.rdq,
    c.fyearq,
    c.fqtr,
    c.ibq,
    c.atq,
    c.epspxq,
    c.ceqq,
    c.cshoq,
    c.prccq,
    c.oancfy,
    c.xidocy,
    any(toInt32(l.lpermno)) AS permno
FROM comp_fundamentals AS c
INNER JOIN crsp_202601.ccmxpf_linktable AS l
    ON c.gvkey = l.gvkey
   AND toDate32OrNull(c.rdq) >= toDate32OrNull(l.linkdt)
   AND coalesce(nullIf(l.linkenddt, ''), '2099-12-31') >= c.rdq
   AND l.linktype IN ('LC', 'LU')
   AND l.usedflag = 1
   AND l.linkprim IN ('P', 'C')
   AND l.lpermno IS NOT NULL
GROUP BY
    c.gvkey, c.datadate, c.rdq, c.fyearq, c.fqtr,
    c.ibq, c.atq, c.epspxq, c.ceqq, c.cshoq, c.prccq,
    c.oancfy, c.xidocy
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600
