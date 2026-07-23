-- universe_sensitivity.sql
-- Purpose: DIAGNOSTIC ONLY (PART 0, read-only) — average stocks/month in 1980
--          under (a) exchcd IN (1,2) & shrcd IN (10,11) [current universe
--          filter, Assumption A1] vs (b) exchcd IN (1,2) only. Counts distinct
--          permnos whose dsenames PIT validity window
--          (namedt .. coalesce(nameendt, '2100-01-01'), string comparison on
--          ISO dates) covers each 1980 month-end date. Quantifies the
--          non-common securities (ADR/fund/unit shrcds) removed by the shrcd
--          filter. Does not touch the primary panel.
-- Tables: crsp_202601.dsenames
-- Output columns: ym (1980 month-end date string), n_exch_only, n_exch_shrcd
-- Depends on: (none)
SELECT
    m.ym AS ym,
    uniq(n.permno) AS n_exch_only,
    uniqIf(n.permno, n.shrcd IN (10, 11)) AS n_exch_shrcd
FROM
(
    SELECT arrayJoin(['1980-01-31', '1980-02-29', '1980-03-31', '1980-04-30',
                      '1980-05-31', '1980-06-30', '1980-07-31', '1980-08-31',
                      '1980-09-30', '1980-10-31', '1980-11-30', '1980-12-31']) AS ym
) AS m
CROSS JOIN crsp_202601.dsenames AS n
WHERE n.exchcd IN (1, 2)
  AND n.namedt <= m.ym
  AND coalesce(n.nameendt, '2100-01-01') >= m.ym
GROUP BY m.ym
ORDER BY m.ym
SETTINGS max_execution_time = 300,
         timeout_before_checking_execution_speed = 0;
