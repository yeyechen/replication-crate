-- delistings.sql
-- Purpose: Delisting month for every stock that ever appears in a formation-year
--          universe. Used to (a) detect whether a stock delists inside each
--          holding year (delist_month_offset), (b) decide alive_k (delisted before
--          the holding-year start -> not a member), and (c) drive the size-decile
--          replacement for post-delisting months (Assumption A6). A permno delists
--          at most once, so permno -> dl_mnum is unique.
-- Tables: crsp_202601.dsedelist, crsp_202601.dsenames, crsp_202601.msf
-- Output columns: permno, dlstdt, dl_mnum (= year*12 + month of dlstdt)
-- Depends on: universe_formation (universe CTE inlined to derive the permno set)
WITH formation AS (
    SELECT toUInt32(substring(date, 1, 4)) AS fy, max(date) AS form_date
    FROM crsp_202601.msf
    WHERE date >= '1968-04-01' AND date <= '1989-04-30' AND substring(date, 6, 2) = '04'
    GROUP BY fy
),
univ_permno AS (
    SELECT DISTINCT n.permno AS permno
    FROM crsp_202601.dsenames AS n
    CROSS JOIN formation AS f
    WHERE n.shrcd IN (10, 11) AND n.exchcd IN (1, 2) AND n.permno IS NOT NULL
      AND n.namedt <= '1989-12-31' AND ifNull(n.nameendt, '2100-01-01') >= '1968-01-01'
      AND n.namedt <= f.form_date AND ifNull(n.nameendt, '2100-01-01') >= f.form_date
)
SELECT DISTINCT
    e.permno AS permno,
    e.dlstdt AS dlstdt,
    toUInt32(substring(e.dlstdt, 1, 4)) * 12 + toUInt32(substring(e.dlstdt, 6, 2)) AS dl_mnum
FROM crsp_202601.dsedelist AS e
INNER JOIN univ_permno AS u ON u.permno = e.permno
WHERE e.dlstdt IS NOT NULL
  AND e.dlstdt >= '1968-01-01' AND e.dlstdt <= '1996-12-31'
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
