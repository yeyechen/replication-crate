-- compustat_funda.sql
-- Purpose: Compustat annual accounting data for fiscal years 1962..1989,
--          matched to formation years t = 1963..1990 as fyear = t - 1
--          ("the latest fiscal year ending in calendar year t-1", L121/L137;
--          fyear is the calendar year of the fiscal yearend in Compustat).
--          Standard FF filter: indfmt='INDL', consol='C', popsrc='D',
--          datafmt='STD' (binding Assumption 13 — verified valid for
--          1962-1989 in this extract).
--          Variables (paper L813):
--            A  = at (total book assets)
--            BE = ceq + txdb; if ceq missing: seq - coalesce(pstkrv, pstk, 0)
--                 + txdb (binding Assumption 6; missing txdb = 0)
--            E  = ib + txdi - dvp (income before extraordinary items +
--                 income-statement deferred taxes - preferred dividends);
--                 NULL when ib is missing (E-presence requirement, L137)
--          UNITS: Compustat dollar items are in $ MILLIONS; the output A/BE/E
--          are scaled by 1e6 to DOLLARS so the ratios BE/ME_dec, A/ME_dec,
--          E/ME_dec are unit-consistent with CRSP market equity in dollars
--          (ME = abs(prc)*shrout*1000). A/BE is scale-invariant.
-- Tables: comp_202601.funda
-- Output columns:
--   gvkey   String
--   fyear   Int32  fiscal year (= calendar year of datadate)
--   datadate String fiscal yearend
--   A       Nullable(Float64) total assets, $ (millions x 1e6)
--   BE      Nullable(Float64) book equity (fallback chain applied), $
--   E       Nullable(Float64) earnings (NULL if ib missing), $
-- Window: fyear 1962..1989 (fiscal yearends in calendar years t-1).
-- Depends on: (none)
-- Note: funda is not uniquely keyed by (gvkey, fyear) even after the 4-flag
--       filter (2 duplicate pairs in 1962-1989 here) — deduplicated via
--       argMax(..., datadate), keeping the most recent datadate row per
--       (gvkey, fyear) (references/COMPUSTAT.md fiscal-year-uniqueness).
WITH f AS (
    SELECT
        gvkey,
        fyear,
        -- NB: alias must NOT be named `datadate` — the new analyzer would
        -- substitute the alias into the argMax(...) second arguments below
        -- (aggregate-inside-aggregate error).
        argMax(datadate, datadate) AS dd,
        argMax(at,     datadate)   AS at,
        argMax(ceq,    datadate)   AS ceq,
        argMax(seq,    datadate)   AS seq,
        argMax(txdb,   datadate)   AS txdb,
        argMax(pstkrv, datadate)   AS pstkrv,
        argMax(pstk,   datadate)   AS pstk,
        argMax(ib,     datadate)   AS ib,
        argMax(txdi,   datadate)   AS txdi,
        argMax(dvp,    datadate)   AS dvp
    FROM comp_202601.funda
    WHERE fyear >= 1962 AND fyear <= 1989
      AND indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc = 'D'
      AND datafmt = 'STD'
      AND gvkey IS NOT NULL AND gvkey != ''
      AND fyear IS NOT NULL
    GROUP BY gvkey, fyear
)
SELECT
    gvkey,
    fyear,
    dd AS datadate,
    toNullable(at * 1e6) AS A,
    multiIf(
        ceq IS NOT NULL, toNullable((ceq + ifNull(txdb, 0)) * 1e6),
        seq IS NOT NULL, toNullable((seq - coalesce(pstkrv, pstk, 0) + ifNull(txdb, 0)) * 1e6),
        CAST(NULL, 'Nullable(Float64)')
    ) AS BE,
    if(ib IS NOT NULL,
       toNullable((ib + ifNull(txdi, 0) - ifNull(dvp, 0)) * 1e6),
       CAST(NULL, 'Nullable(Float64)')) AS E
FROM f
SETTINGS max_execution_time = 600;
