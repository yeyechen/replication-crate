-- comp_actual_roe_for_panel.sql
-- Purpose: Pull comp_202601.funda rows for the panel's gvkeys at fyear
--          values needed for Tables 6/7 FErr_{t+2} and SG (5-year sales
--          growth).
--
--          Panel year_t range = 1976..1993, so fyear in [1974, 1992]
--          covers every needed offset:
--             (1) Actual ROE_{t+2}: fyear = year_t + 1 (and fyear = year_t)
--             (2) SG: sale at fyear = year_t - 6 and year_t - 1
--
--          The KEY safety property (per task spec) is the `gvkey IN
--          (SELECT DISTINCT gvkey FROM _panel_gvkeys)` filter. This pulls
--          comp rows ONLY for the universe's gvkeys (avoiding the
--          Cartesian explosion seen in iteration 4 where the join
--          produced ~25 rows per panel row).
--
-- Output columns: gvkey (String), fyear (UInt16), ib, ceq, sale
-- Tables: comp_202601.funda
-- Depends on: _panel_gvkeys (uploaded by main.py as (gvkey, year_t))
-- Settings: max_execution_time=600, max_rows_to_read large enough

SELECT
    CAST(c.gvkey, 'String')          AS gvkey,
    CAST(c.fyear, 'UInt16')          AS fyear,
    c.ib                              AS ib,
    c.ceq                             AS ceq,
    c.sale                            AS sale
FROM comp_202601.funda AS c
WHERE c.fyear BETWEEN 1974 AND 1992
  AND c.indfmt = 'INDL'
  AND c.consol = 'C'
  AND c.popsrc = 'D'
  AND c.datafmt = 'STD'
  AND c.gvkey IS NOT NULL
  AND c.gvkey IN (SELECT DISTINCT gvkey FROM _panel_gvkeys)
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0

