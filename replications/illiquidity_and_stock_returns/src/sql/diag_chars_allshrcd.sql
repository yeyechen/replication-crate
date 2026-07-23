-- diag_chars_allshrcd.sql
-- DIAGNOSTIC ONLY (task A3). Same ILLIQ construction as
-- characteristics_annual.sql, but the universe is ALL NYSE securities
-- with daily data (hexcd = 1 PIT via dsfhdr, NO shrcd filter — includes
-- ADRs, closed-end funds, REITs, units, etc.). One row per (permno, y),
-- y = 1963..1996. Only illiq + n_days are needed downstream.
-- Valid ILLIQ day: ret non-null AND ret > -1 AND vol > 0 AND |prc| > 0.
-- ILLIQ_iY = 1e6 * mean over valid days of |ret|/(|prc|*vol).
-- Tables: crsp_202601.dsf, crsp_202601.dsfhdr
-- Output columns: permno, y, illiq, n_days
WITH univ AS (
    SELECT
        d.permno         AS permno,
        toDate32(d.date) AS date32,
        d.ret            AS ret,
        abs(d.prc)       AS abs_prc,
        d.vol            AS vol,
        (d.ret IS NOT NULL AND d.ret > -1
         AND d.vol IS NOT NULL AND d.vol > 0
         AND abs(d.prc) > 0)                       AS iv
    FROM crsp_202601.dsf AS d
    INNER JOIN crsp_202601.dsfhdr AS h
        ON d.permno = h.permno
    WHERE h.hexcd = 1
      AND d.date >= '1963-01-01' AND d.date <= '1996-12-31'
      AND toDate32(d.date) >= toDate32(h.begdat)
      AND toDate32(d.date) <= toDate32(h.enddat)
)
SELECT
    permno,
    toYear(date32)  AS y,
    if(countIf(iv) > 0,
       1e6 * avgIf(abs(ret) / nullIf(abs_prc * vol, 0), iv),
       NULL)        AS illiq,
    countIf(iv)     AS n_days
FROM univ
GROUP BY permno, y
ORDER BY permno, y
SETTINGS max_execution_time = 1800,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
