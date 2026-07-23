-- universe_global.sql
-- Purpose: GLOBAL (13-country) equity universe for Heston & Sadka (2010).
--          One security per firm — the PRIMARY issue (g_company.prirow is the
--          primary-issue iid), classified by g_company.loc (ISO3 domicile).
--          This avoids double-counting cross-listings (a firm may have several
--          iids across exchanges; prirow picks exactly one).
-- Tables: comp_202601.g_company  (one row per gvkey; prirow is a String)
-- Output columns: gvkey (String), iid (String), country (String)
-- Depends on: (none)
-- Settings: max_execution_time, max_rows_to_read guards
--
-- Countries (13 non-Canada sample countries):
--   AUT BEL FIN FRA DEU ITA JPN NLD NOR ESP SWE CHE GBR
SELECT
    gvkey  AS gvkey,
    prirow AS iid,
    loc    AS country
FROM comp_202601.g_company
WHERE loc IN ('AUT','BEL','FIN','FRA','DEU','ITA','JPN','NLD','NOR','ESP','SWE','CHE','GBR')
  AND gvkey  IS NOT NULL
  AND prirow IS NOT NULL
SETTINGS max_execution_time = 120,
         max_rows_to_read = 1000000,
         timeout_before_checking_execution_speed = 0
