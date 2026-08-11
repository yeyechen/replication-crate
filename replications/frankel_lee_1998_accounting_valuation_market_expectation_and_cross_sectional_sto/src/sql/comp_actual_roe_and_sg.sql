-- comp_actual_roe_and_sg.sql
-- Purpose: Pull comp_202601.funda rows for our panel's gvkeys at all
--          fyear values needed for Tables 6-9:
--   (1) Actual ROE_{t+2}: fyear = year_t+1 (and fyear = year_t for
--       the 2-year average denominator)
--   (2) SG (5-year sales growth from year_t-6 to year_t-1): fyear
--       values in [year_t-6, year_t-1]
--
-- We pull the union of all fyears any panel row would need. Panel
-- year_t range = 1976..1993, so fyear in [1970, 1994] covers
-- every needed offset. Merging into the panel (one merge per offset
-- column) happens in main.py.
--
-- Output columns: gvkey (String), fyear (UInt16), ib, ceq, sale
-- Tables: comp_202601.funda
-- Depends on: _panel_gvkeys (uploaded by main.py)
-- Settings: max_execution_time=600

SELECT
    CAST(c.gvkey, 'String')          AS gvkey,
    CAST(c.fyear, 'UInt16')          AS fyear,
    c.ib                              AS ib,
    c.ceq                             AS ceq,
    c.sale                            AS sale
FROM comp_202601.funda AS c
INNER JOIN _panel_gvkeys AS pk
    ON c.gvkey = pk.gvkey
WHERE c.fyear BETWEEN 1970 AND 1994
  AND c.indfmt = 'INDL'
  AND c.consol = 'C'
  AND c.popsrc = 'D'
  AND c.datafmt = 'STD'
  AND c.gvkey IS NOT NULL
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0