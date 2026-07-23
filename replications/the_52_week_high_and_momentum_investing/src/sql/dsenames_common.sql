-- dsenames_common.sql
-- Purpose: Point-in-time CRSP name records for ordinary common shares
--          (shrcd IN (10, 11)). Used in main.py to (a) flag universe
--          stock-months — a stock-month is in the universe iff some record
--          has namedt <= month-end <= nameendt — and (b) source the
--          point-in-time SIC code (siccd; fallback to msf.hsiccd if null)
--          for the 20 MG-style industries.
--          NO exchange-code filter: the paper says "We use all stocks on
--          CRSP from 1963 to 2001" (universe_all_crsp rule). exchcd is
--          pulled for auditability only.
-- Tables: crsp_202601.dsenames
-- Output columns: permno, namedt, nameendt, shrcd, exchcd, siccd
-- Notes: Verified in this vintage: nameendt has 0 NULLs (every record is
--        closed-ended), validity intervals of a permno never overlap, and
--        siccd has 0 NULLs among shrcd 10/11 records — so a backward
--        merge_asof on namedt plus the coverage check is exactly equivalent
--        to the "exists a covering record" semantics.
-- Depends on: (none)
--        Dates use toDate32: records start in 1925 and the ClickHouse
--        Date type cannot hold pre-1970 dates (they saturate to
--        1970-01-01).
SELECT
    permno,
    toDate32(namedt) AS namedt,
    toDate32(nameendt) AS nameendt,
    shrcd,
    exchcd,
    siccd
FROM crsp_202601.dsenames
WHERE shrcd IN (10, 11)
SETTINGS
    max_execution_time = 300,
    max_rows_to_read = 10000000000,
    timeout_before_checking_execution_speed = 0
