-- exchcd.sql
-- Purpose: Point-in-time (PIT) exchange codes for US common stocks, used to
--          compute NYSE decile breakpoints for the Table 3 beta-sorted
--          portfolios. The paper: "The ranked stocks are assigned to one of
--          ten deciles portfolios based on NYSE breakpoints." (Table 3 desc.)
-- Tables: crsp_202601.dsenames
-- Output columns:
--   permno   : Int32 stock identifier
--   namedt   : Nullable(String) start of the name record's validity window
--   nameendt : Nullable(String) end of the validity window (may be NULL = still active)
--   exchcd   : Int32 exchange code for THIS record's window
--              (1=NYSE, 2=NYSE MKT/AMEX, 3=NASDAQ, 4=Arca, 5=BZX, 6=IEX)
-- Depends on: (none)
-- Settings: max_execution_time=120
--
-- Notes:
--   * Universe filter shrcd IN (10,11) matches the panel's universe so the PIT
--     windows align with the rows we are labelling.
--   * exchcd in dsenames is the exchange code valid over [namedt, nameendt];
--     merging by permno with namedt <= month <= nameendt gives the PIT exchange.
--   * nameendt is kept (may be NULL); the Python side treats NULL as "still
--     active" (far-future) so recent records still cover the panel months.
SELECT
    permno,
    namedt,
    nameendt,
    exchcd
FROM crsp_202601.dsenames
WHERE shrcd IN (10, 11)
  AND permno IS NOT NULL
  AND namedt IS NOT NULL
  AND exchcd IS NOT NULL
SETTINGS max_execution_time = 120;
