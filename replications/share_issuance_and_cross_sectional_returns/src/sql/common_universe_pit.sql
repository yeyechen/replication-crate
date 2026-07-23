-- common_universe_pit.sql
-- Purpose: Distinct (permno, midx) for which the security's POINT-IN-TIME share
--   code is 10 or 11 (ordinary common shares) per the dsenames validity window.
--   Used to build univ_common = univ_all AND shrcd in {10,11}. The main paper
--   sample ("all firm observations in CRSP") is univ_all; univ_common is the
--   narrower common-stock subset for reconciliation.
--   PIT join on date BETWEEN namedt AND ifNull(nameendt,'2099-12-31'); namedt is
--   NOT date-filtered (references/CRSP.md gotcha). midx is epoch-proof.
-- Paper: §I Sample (L51); shrcd 10/11 = ordinary common shares (references/CRSP.md).
-- Tables: crsp_202601.msf, crsp_202601.dsenames
-- Output columns: permno, midx
-- Depends on: (none)
SELECT DISTINCT
    m.permno,
    toYear(toDate32(m.date)) * 12 + (toMonth(toDate32(m.date)) - 1) AS midx
FROM crsp_202601.msf AS m
INNER JOIN crsp_202601.dsenames AS n
  ON m.permno = n.permno
 AND toDate32(m.date) >= ifNull(toDate32(n.namedt),   toDate32('1900-01-01'))
 AND toDate32(m.date) <= ifNull(toDate32(n.nameendt), toDate32('2099-12-31'))
WHERE m.date >= '1926-12-01' AND m.date <= '2006-12-31'
  AND m.permno IS NOT NULL
  AND n.shrcd IN (10, 11)
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 1200,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
