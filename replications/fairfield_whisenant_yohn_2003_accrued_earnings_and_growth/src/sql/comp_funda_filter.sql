-- comp_funda_filter.sql
-- Purpose: Apply universe filters + footnote-code approximation to comp_202601.funda,
--          yielding one row per (gvkey, fyear) that survives. This is the
--          "filter breakout" file: panel.sql is the canonical pipeline but this
--          isolates the filtering for human review.
-- Tables: comp_202601.funda, comp_202601.funda_fncd
-- Output columns: gvkey, fyear, datadate, sich, fic, at, rect, invt, aco,
--                 ap, lco, ppent, intan, ao, lo, oiadp, dp, gdwl
-- Depends on: (none)
-- Settings: max_execution_time=300, max_rows_to_read=1e9

-- The base pulls fyear 1961-1993 so the 3-year-window self-joins (t-1, t+1, t-2)
-- in panel.sql can resolve the paper's 1963-1992 output window. The final
-- sample-window gate is applied in panel.sql.
WITH base AS (
    SELECT gvkey, fyear, toDate32OrNull(datadate) AS datadate,
           sich, fic,
           at, rect, invt, aco, ap, lco,
           ppent, intan, ao, lo, oiadp, dp, gdwl
    FROM comp_202601.funda
    WHERE fyear BETWEEN 1961 AND 1993
      AND indfmt = 'INDL'
      AND consol = 'C'
      AND popsrc = 'D'
      AND datafmt = 'STD'
      AND (sich < 6000 OR sich > 6999 OR sich IS NULL)
      AND at IS NOT NULL
      AND at > 0
),
fnd AS (
    -- Footnote codes restricted to the same filter mask.
    -- Modern WRDS extract only annotates a subset of the items in the paper's
    -- footnote 9 (oiadp, aco, lco, gdwl have no fncd column). Where the
    -- annotation is missing, those items pass through the footnote filter
    -- and we rely on the goodwill filter (gdwl YoY) for the noise removal.
    SELECT gvkey, fyear,
           at_fn, recta_fn AS rect_fn, invt_fn, ap_fn, dp_fn
    FROM comp_202601.funda_fncd
    WHERE fyear BETWEEN 1961 AND 1993
      AND indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
)
SELECT
    b.gvkey,
    b.fyear,
    b.datadate,
    b.sich,
    b.fic,
    b.at,
    b.rect,
    b.invt,
    b.aco,
    b.ap,
    b.lco,
    b.ppent,
    b.intan,
    b.ao,
    b.lo,
    b.oiadp,
    b.dp,
    b.gdwl
FROM base AS b
LEFT JOIN fnd AS fn
    ON  b.gvkey = fn.gvkey
    AND b.fyear = fn.fyear
WHERE
    -- Footnote filter: drop firm-years where any annotatable item has a
    -- non-null audit footnote flag. (See assumptions.md for the rationale.)
    fn.at_fn   IS NULL
    AND fn.rect_fn IS NULL
    AND fn.invt_fn IS NULL
    AND fn.ap_fn   IS NULL
    AND fn.dp_fn   IS NULL
SETTINGS max_execution_time = 300,
         max_rows_to_read = 1000000000,
         timeout_before_checking_execution_speed = 0
