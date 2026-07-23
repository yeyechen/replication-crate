-- mcti_bill_monthly.sql
-- Purpose: Monthly Treasury bill/bond index returns from CRSP mcti for
--          the A2 annual-Rf sensitivity check (Amihud 2002 Table 3,
--          market column; audit 1 [m2], report-only).
--   b1ret  = 1-year Treasury index monthly return (decimal), the
--            alternative annual Rf: annual Rf_alt_y = prod(1 + b1ret_m)
--            over the 12 months of year y.
--   t90ret = 90-day T-bill index monthly return (decimal), shown
--            alongside as a second alternative.
--   t30ret = 30-day T-bill monthly return (decimal), used only for the
--            cross-check vs ff.four_factor_monthly rf (the A2 primary).
-- Spot-check verified: b1ret monthly mean ~0.003-0.005 in the 1960s,
-- ~0.01+ in 1979-1982 (1-year bill behavior); no /100 conversion
-- needed (decimal, same convention as mcti t30ret = 0.00251 in
-- 1963-01 per ff_rf.sql).
-- Tables: crsp_202601.mcti (caldt = end-of-month date, String)
-- Output columns: month (Date32 first-of-month), b1ret, t90ret, t30ret
-- Depends on: (none)
SELECT
    toDate32(concat(toString(toYear(toDate32(caldt))), '-',
             leftPad(toString(toMonth(toDate32(caldt))), 2, '0'),
             '-01')) AS month,
    b1ret   AS b1ret,
    t90ret  AS t90ret,
    t30ret  AS t30ret
FROM crsp_202601.mcti
WHERE caldt >= '1964-01-01' AND caldt <= '1996-12-31'
ORDER BY caldt
SETTINGS max_execution_time = 60
