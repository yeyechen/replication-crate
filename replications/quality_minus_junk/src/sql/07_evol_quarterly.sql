-- 07_evol_quarterly.sql
-- Purpose: EVOL = standard deviation of quarterly ROE over the trailing
--          60 quarters, requiring at least 12 nonmissing quarters (paper
--          Appendix 1). Quarterly ROE = ibq / ceqq (ceqq = 0 -> NULL).
--          fundq dedup: 1,584 (gvkey, datadate) duplicates resolved by
--          keeping the latest (fyearq, fqtr) record.
-- Tables: comp_202601.fundq
-- Output: write_yeye.qmj_evol (gvkey String, datadate Date, evol Float64)
-- Depends on: (none)
-- Note: ceqq coverage is thin pre-1980s; the annual-ROE 5-yr fallback
--       computed in 02_funda_annual.sql (evol_a) is coalesced in
--       08_funda_enriched.sql per the paper's fallback rule.

CREATE OR REPLACE TABLE write_yeye.qmj_evol
ENGINE = MergeTree ORDER BY (gvkey, datadate) AS
WITH
filt AS (
    SELECT
        assumeNotNull(gvkey)            AS gvkey,
        assumeNotNull(toDate32(datadate)) AS datadate,
        coalesce(fyearq, 0)             AS fyearq,
        coalesce(fqtr, 0)               AS fqtr,
        ibq,
        ceqq
    FROM comp_202601.fundq
    WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
      AND gvkey IS NOT NULL AND datadate IS NOT NULL
      AND toDate32(datadate) <= toDate32('2016-12-31')
),
dedup AS (
    SELECT gvkey, datadate, ibq, ceqq
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY gvkey, datadate
                                  ORDER BY fyearq DESC, fqtr DESC) AS rn
        FROM filt
    )
    WHERE rn = 1
),
roe AS (
    SELECT
        gvkey,
        datadate,
        ibq / nullIf(ceqq, 0) AS roeq
    FROM dedup
),
w AS (
    SELECT
        gvkey,
        datadate,
        count(roeq)       OVER wnd AS cnt,
        stddevSamp(roeq)  OVER wnd AS evol
    FROM roe
    WINDOW wnd AS (PARTITION BY gvkey ORDER BY datadate
                   ROWS BETWEEN 59 PRECEDING AND CURRENT ROW)
)
SELECT gvkey, datadate, evol
FROM w
WHERE cnt >= 12
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
