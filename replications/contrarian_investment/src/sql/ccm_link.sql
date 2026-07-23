-- ccm_link.sql
-- Purpose: Point-in-time CRSP<->Compustat link at each formation date. Maps each
--          formation-year permno to its Compustat gvkey using the link that is
--          active at the formation date:
--              linkdt <= form_date AND coalesce(linkenddt,'2100-01-01') >= form_date
--          Filter: linkprim = 'P' (primary), linktype IN ('LC','LU').
--          One gvkey per (fy, permno) (most recent link start wins on conflict),
--          so the panel stays one-row-per-(fy,permno). A gvkey may map to several
--          permnos (multiple share classes) — those are kept as distinct rows.
-- Tables: crsp_202601.ccmxpf_lnkhist (lpermno is Float64 -> cast toInt32),
--         crsp_202601.msf (formation dates)
-- Output columns: fy, form_date, permno, gvkey
-- Depends on: formation_dates.sql (formation CTE replicated inline)
WITH formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
link_pit AS (
    SELECT
        f.fy            AS fy,
        f.form_date     AS form_date,
        toInt32(l.lpermno) AS permno,
        l.gvkey         AS gvkey,
        l.linkdt        AS linkdt,
        row_number() OVER (
            PARTITION BY f.fy, toInt32(l.lpermno)
            ORDER BY l.linkdt DESC, l.gvkey ASC
        ) AS rn
    FROM crsp_202601.ccmxpf_lnkhist AS l
    CROSS JOIN formation AS f
    WHERE l.linkprim = 'P'
      AND l.linktype IN ('LC', 'LU')
      AND l.lpermno IS NOT NULL
      AND l.gvkey IS NOT NULL
      AND l.linkdt <= f.form_date
      AND ifNull(l.linkenddt, '2100-01-01') >= f.form_date
)
SELECT fy, form_date, permno, gvkey
FROM link_pit
WHERE rn = 1
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
