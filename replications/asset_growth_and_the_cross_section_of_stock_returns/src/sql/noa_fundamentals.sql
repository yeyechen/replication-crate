-- noa_fundamentals.sql
-- Purpose: Funda inputs for the Table III NOA/A regressor (net operating assets
--          divided by CURRENT total assets; var_noa L4404, Table III caption L1642):
--              OA  = at - ch
--              OL  = at - dlc - dltt - mib - pstk - ceq
--              NOA = OA - OL = dlc + dltt + mib + pstk + ceq - ch
--              NOA/A = NOA / at        (all items at fiscal year t-1; june_year = fyear+1)
--          One row per (gvkey, fyear), deduplicated per Assumption 3 (same WRDS
--          industrial filter + row_number tie-break as comp_fundamentals.sql).
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, at, ch, dlc, dltt, mib, pstk, ceq
-- Depends on: (none)
-- Notes:
--   * Same dedup convention as the foundation (Assumption 3): indfmt='INDL',
--     consol='C', datafmt='STD', popsrc='D'; row_number partitioned by
--     (gvkey, fyear) ordered by isNull(at) ASC, datadate DESC; keep rn = 1.
--   * fyear >= 1960 AND <= 2002: NOA/A at june_year t (=fyear+1) is needed for
--     t in 1968..2002 -> fyear 1967..2001 (1960 lower bound kept for symmetry
--     with comp_fundamentals.sql).
--   * at/ch/dlc/dltt/mib/pstk/ceq are in $MILLIONS. Missing sub-items are filled
--     with 0 downstream in table_3.py (standard practice; at must be > 0).
WITH filtered AS (
    SELECT
        gvkey,
        fyear,
        datadate,
        at, ch, dlc, dltt, mib, pstk, ceq
    FROM comp_202601.funda
    WHERE indfmt = 'INDL'
      AND consol = 'C'
      AND datafmt = 'STD'
      AND popsrc = 'D'
      AND fyear >= 1960 AND fyear <= 2002
      AND gvkey IS NOT NULL
      AND datadate IS NOT NULL
),
ranked AS (
    SELECT
        f.*,
        row_number() OVER (
            PARTITION BY f.gvkey, f.fyear
            ORDER BY isNull(f.at) ASC, f.datadate DESC
        ) AS rn
    FROM filtered AS f
)
SELECT
    gvkey,
    fyear,
    at, ch, dlc, dltt, mib, pstk, ceq
FROM ranked
WHERE rn = 1
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
