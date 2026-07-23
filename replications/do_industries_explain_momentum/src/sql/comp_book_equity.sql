-- comp_book_equity.sql
-- Purpose: Book-equity line items from Compustat funda, filtered (FF/vintage
--          convention: indfmt='INDL', consol='C', popsrc='D') and deduped per
--          (gvkey, fyear) keeping datafmt='STD' (fall back to SUMM_STD), latest
--          datadate on remaining ties. The BE cascade (ceq+txdb-pstkrv > seq >
--          at-dlc-dltt-pstkrv) and the scale conversion (millions -> dollars)
--          are applied downstream in src/add_fundamentals.py.
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, datadate, at, ceq, txdb, pstkrv, seq, dlc, dltt
-- Depends on: (none)
-- Settings: max_execution_time=600
SELECT
    gvkey,
    fyear,
    datadate,
    at,
    ceq,
    txdb,
    pstkrv,
    seq,
    dlc,
    dltt
FROM (
    SELECT
        gvkey, fyear, datadate, at, ceq, txdb, pstkrv, seq, dlc, dltt,
        row_number() OVER (
            PARTITION BY gvkey, fyear
            ORDER BY CASE WHEN datafmt = 'STD' THEN 0 ELSE 1 END,
                     datadate DESC
        ) AS rn
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc = 'D'
      AND fyear BETWEEN 1961 AND 1994
      AND gvkey IS NOT NULL
      AND gvkey != ''
      AND datadate IS NOT NULL
)
WHERE rn = 1
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
