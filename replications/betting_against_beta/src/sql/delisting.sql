-- delisting.sql
-- Purpose: Delisting returns + codes for adjusting the last-month return of
--          stocks that delist (Shumway 1997 / BMP 2007). Raw msf.ret does NOT
--          include the delisting return, which biases high-beta portfolio
--          returns upward (high-beta names are more likely to delist for
--          performance reasons and lose value at delisting).
-- Tables: crsp_202601.dsedelist
-- Output columns:
--   permno : Int32 stock identifier
--   dlstdt : Nullable(String) delisting date
--   dlret  : Nullable(Float64) delisting return, DECIMAL (same units as ret).
--            Missing sentinels appear as NULL in this vintage (the -44/-55/
--            -66/-77/-88/-99 codes) or as -1.0 (CRSP "worthless" flag); the
--            Python side treats dlret <= -1.0 or NULL as "missing".
--   dlstcd : Nullable(Int32) delisting code (500-599 = performance-related,
--            the set eligible for the Shumway/BMP imputation when dlret missing)
--   hexcd  : Nullable(Int32) exchange code AT delisting (1=NYSE,2=AMEX,3=NASDAQ),
--            used to pick the Shumway imputation (-0.30 NYSE/AMEX, -0.55 NASDAQ)
-- Depends on: (none)
-- Settings: max_execution_time=120
SELECT
    permno,
    dlstdt,
    dlret,
    dlstcd,
    hexcd
FROM crsp_202601.dsedelist
WHERE permno IS NOT NULL
  AND dlstdt IS NOT NULL
SETTINGS max_execution_time = 120;
