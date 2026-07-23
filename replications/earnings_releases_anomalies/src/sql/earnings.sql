-- earnings.sql
-- Purpose: Compustat quarterly earnings (epspxq) for Foster-Olsen-Shevlin (1984),
--          1970Q2-1981Q4 earnings file (A1, A2, sample_earnings_file_range).
--          Screen 1 (>=10 consecutive non-missing epspxq quarters, A5) is applied
--          in Python on this pull; NULL-epspxq rows are dropped there as well.
-- Tables: comp_202601.fundq
-- Output columns: gvkey, fyearq, fqtr, datadate (Date), rdq (Nullable Date), epspxq
-- Depends on: (none)
SELECT
    gvkey,
    fyearq,
    fqtr,
    toDate(datadate) AS datadate,
    toDateOrNull(nullIf(rdq, '')) AS rdq,
    epspxq
FROM comp_202601.fundq
WHERE consol = 'C'
  AND indfmt = 'INDL'
  AND popsrc = 'D'
  AND fqtr IN (1, 2, 3, 4)
  AND datadate BETWEEN '1970-04-01' AND '1981-12-31'
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0;
