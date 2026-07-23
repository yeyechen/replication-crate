-- formation_dates.sql
-- Purpose: The 22 annual portfolio-formation dates for LSV (1994) — the last
--          CRSP trading day of April for each year 1968..1989. Portfolios are
--          formed at end of April "to ensure that the previous year's accounting
--          numbers were available at the time of formation" (L122; 22 formation
--          periods, end of April 1968 through end of April 1989).
-- Tables: crsp_202601.msf
-- Output columns: fy (formation year), form_date (YYYY-MM-DD, last April trading day)
-- Depends on: (none)
-- Note: msf.date is a Nullable(String) in ISO form; toDate() does NOT parse it
--       reliably in this instance, so year/month are extracted via substring and
--       all date filtering uses lexicographic (ISO-safe) string comparison.
SELECT toUInt32(substring(date, 1, 4)) AS fy,
       max(date)                        AS form_date
FROM crsp_202601.msf
WHERE date >= '1968-04-01'
  AND date <= '1989-04-30'
  AND substring(date, 6, 2) = '04'
GROUP BY fy
ORDER BY fy
SETTINGS max_execution_time = 120,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
