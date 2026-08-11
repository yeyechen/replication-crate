-- comp_fundamentals.sql
-- Purpose: Pull required Compustat quarterly fields for the BBF (2009) sample window.
--          Universe: firm-quarters with rdq (announcement date) in 1976-2005
--          AND ibq (Compustat Quarterly data8, earnings before extraordinary items)
--          AND atq (Compustat Quarterly data44, beginning-of-quarter total assets)
--          non-missing.
--
-- Tables: comp_202601.fundq
-- Output columns: gvkey, datadate, rdq, fyearq, fqtr, ibq, atq, epspxq, ceqq, cshoq, prccq, oancfy, xidocy
-- Depends on: (none)
-- Settings: max_execution_time=300
--
-- Notes:
--   * `rdq` is stored as Nullable(String) in YYYY-MM-DD format. We filter on the
--     string range so ClickHouse can use a simple comparison.
--   * We pull more columns than the primary filter requires (epspxq, ceqq,
--     cshoq, prccq, oancfy, xidocy) so the supplementary samples (SUE, BM,
--     Accruals) can be evaluated against the same base panel without
--     re-querying fundq.

SELECT
    gvkey,
    datadate,
    rdq,
    fyearq,
    fqtr,
    ibq,
    atq,
    epspxq,
    ceqq,
    cshoq,
    prccq,
    oancfy,
    xidocy
FROM comp_202601.fundq
WHERE rdq BETWEEN '1976-01-01' AND '2005-12-31'
  AND ibq IS NOT NULL
  AND atq IS NOT NULL
  AND rdq IS NOT NULL
SETTINGS max_execution_time = 300
