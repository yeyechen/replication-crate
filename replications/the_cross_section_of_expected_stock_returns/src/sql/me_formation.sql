-- me_formation.sql
-- Purpose: market equity at the December t-1 and June t month-ends used by
--          Fama-French (1992): ME_dec (denominator of BE/ME, A/ME, E/P) and
--          ME_jun (size). Paper: "We use a firm's market equity at the end of
--          December of year t-1 to compute its book-to-market, leverage, and
--          earnings-price ratios for t-1, and we use its market equity for
--          June of year t to measure its size" (L123-L125).
--          ME = abs(prc) * shrout * 1000  (dollars; shrout in 1000s of
--          shares). NULL when the price is invalid (NULL or abs(prc) = 0) or
--          shrout is missing/non-positive (references/CRSP.md: prc signed ->
--          abs(); shrout in thousands).
-- Tables: crsp_202601.msf
-- Output columns:
--   permno Int32
--   ym     UInt32 month key YYYYMM, restricted to the 56 formation month-ends
--          {196212, 196306, 196312, ..., 198912, 199006}
--   me     Nullable(Float64) market equity in dollars
-- Window: msf date 1962-12-01 .. 1990-07-31 (formation years t = 1963..1990).
-- Depends on: (none)
-- Note: NO universe filter here — the NYSE size breakpoints (Tables I, II, V)
--       are computed over ALL NYSE common stocks on CRSP, not only the
--       data-qualified subset (paper L151; task spec Sort A). Universe flags
--       are attached downstream via universe_pit_june.sql.
WITH m AS (
    SELECT
        assumeNotNull(permno)    AS permno,
        toYYYYMM(toDate32(date)) AS ym,
        argMax(prc, date)        AS prc,
        argMax(shrout, date)     AS shrout
    FROM crsp_202601.msf
    WHERE date >= '1962-12-01' AND date <= '1990-07-31'
      AND permno IS NOT NULL
    GROUP BY permno, ym
)
SELECT
    permno,
    ym,
    if(prc IS NOT NULL AND abs(prc) > 0 AND shrout IS NOT NULL AND shrout > 0,
       abs(prc) * shrout * 1000,
       CAST(NULL, 'Nullable(Float64)')) AS me
FROM m
WHERE ym BETWEEN 196212 AND 199006 AND ym % 100 IN (6, 12)
SETTINGS max_execution_time = 600;
