-- size_deciles.sql
-- Purpose: Size-decile assignment for the SAAR benchmark and delisting
--          replacement. Assumption A5: at the end of the previous calendar year
--          (last trading day of December t-1), rank ALL NYSE/AMEX common stocks
--          (PIT at that December date, same shrcd IN (10,11)/exchcd IN (1,2)
--          filter) by market equity and assign deciles 1..10 (1 = smallest) via
--          the full-universe decile breakpoints (ntile(10)). The assigned decile
--          is FIXED for all five holding years of formation year t.
-- Tables: crsp_202601.msf (December dates + ME), crsp_202601.dsenames (PIT codes)
-- Output columns: fy, permno, me_dec, size_dec
-- Depends on: (none; December-date logic inlined)
WITH dec_dates AS (
    -- last trading day of December for years 1967..1988, labelled by the
    -- formation year it serves (December t-1 -> formation year t)
    SELECT toUInt32(substring(date, 1, 4)) + 1 AS fy, max(date) AS dec_date
    FROM crsp_202601.msf
    WHERE substring(date, 6, 2) = '12'
      AND date >= '1967-12-01' AND date <= '1988-12-31'
    GROUP BY substring(date, 1, 4)
),
dec_univ AS (
    -- PIT NYSE/AMEX common universe at each December date (same codes as A1)
    SELECT DISTINCT d.fy AS fy, d.dec_date AS dec_date, n.permno AS permno
    FROM crsp_202601.dsenames AS n
    CROSS JOIN dec_dates AS d
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1988-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1967-01-01'
      AND n.namedt <= d.dec_date AND ifNull(n.nameendt, '2100-01-01') >= d.dec_date
),
dec_me AS (
    -- December market equity; require a positive ME so the rank is meaningful
    SELECT u.fy AS fy, u.permno AS permno, abs(m.prc) * m.shrout * 1000 AS me_dec
    FROM dec_univ AS u
    INNER JOIN crsp_202601.msf AS m
        ON m.permno = u.permno AND m.date = u.dec_date
    WHERE m.date >= '1967-12-01' AND m.date <= '1988-12-31'
      AND abs(m.prc) * m.shrout * 1000 > 0
)
SELECT
    fy,
    permno,
    me_dec,
    ntile(10) OVER (PARTITION BY fy ORDER BY me_dec ASC) AS size_dec
FROM dec_me
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
