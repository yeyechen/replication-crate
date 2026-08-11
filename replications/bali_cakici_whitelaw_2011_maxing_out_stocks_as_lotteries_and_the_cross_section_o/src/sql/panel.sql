-- panel.sql
-- Purpose: Final CTE pipeline that assembles the monthly panel with
--          (month, permno, ret, max_signal, mcap_lag1, bm, mkt_rf, smb,
--          hml, mom, rf). Includes Shumway/BMP delisting-return imputation.
--
--          mcap_lag1: at month t, use mcap from end of month t-1.
--          bm: lookup by (permno, fyear_use) where
--              month >= 7 -> fyear_use = year(month) - 1
--              month <  7 -> fyear_use = year(month) - 2.
--          FF factors: aligned on calendar year-month tuple.
--          Delisting returns: dlret added to ret at delisting month.
--              Missing dlret on actual delistings (dlstcd != 100) is
--              substituted with -0.30 (NYSE/AMEX, hexcd IN 1,2) or
--              -0.55 (NASDAQ, hexcd = 3) per Shumway (1997) / BMP (2007).
--          Universe filter uses crsp_202601.dsfhdr (PIT-safe;
--          non-overlapping begdat/enddat) — NOT dsenames, which
--          produces ~18% duplicate (permno, month) rows.
-- Tables: crsp_202601.msf, crsp_202601.dsf, crsp_202601.dsfhdr,
--         crsp_202601.dsedelist, comp_202601.funda,
--         crsp_202601.ccmxpf_linktable, ff.four_factor_monthly
-- Output columns: month, permno, ret, max_signal, mcap, mcap_lag1, bm,
--                 mkt_rf, smb, hml, mom, rf
-- Depends on: (none) — self-contained CTE pipeline
-- Settings: join_algorithm=partial_merge, max_execution_time=600
WITH
  -- 1. PIT-filtered monthly returns (no dlret yet) using dsfhdr
  monthly_raw AS (
      SELECT m.permno                        AS permno,
             makeDate32(toYear(toDate32OrNull(m.date)), toMonth(toDate32OrNull(m.date)), 1) AS month,
             toDate32OrNull(m.date)          AS date,
             m.ret                           AS ret,
             abs(m.prc) * m.shrout           AS mcap_thousands,
             m.hexcd                         AS hexcd
      FROM crsp_202601.msf AS m
      INNER JOIN crsp_202601.dsfhdr AS h
          ON m.permno = h.permno
         AND m.date >= h.begdat
         AND m.date <= h.enddat
      WHERE h.hshrcd IN (10, 11)
        AND h.hexcd IN (1, 2, 3)
        AND m.date BETWEEN '1962-01-01' AND '2006-06-30'
        AND m.ret IS NOT NULL
        AND m.ret > -0.5
  ),
  -- 2. Delisting returns from dsedelist with BMP imputation for missing
  --    dlret on actual delistings (dlstcd != 100 = not still trading)
  delist AS (
      SELECT d.permno                          AS permno,
             makeDate32(toYear(toDate32OrNull(d.dlstdt)),
                        toMonth(toDate32OrNull(d.dlstdt)), 1) AS month,
             if(d.dlstcd = 100, 0.0,
                if(d.dlret IS NOT NULL AND isFinite(d.dlret), d.dlret,
                   if(d.hexcd IN (1, 2), -0.30,
                      if(d.hexcd = 3, -0.55, -0.30)))) AS dlret
      FROM crsp_202601.dsedelist AS d
      WHERE d.dlstdt IS NOT NULL
        AND d.dlstdt BETWEEN '1962-01-01' AND '2006-06-30'
  ),
  -- 3. Monthly returns with delisting return added (if any)
  monthly AS (
      SELECT mr.permno        AS permno,
             mr.month         AS month,
             mr.date          AS date,
             mr.ret + coalesce(d.dlret, 0.0) AS ret,
             mr.mcap_thousands AS mcap_thousands,
             mr.hexcd         AS hexcd
      FROM monthly_raw AS mr
      LEFT JOIN delist AS d
          ON mr.permno = d.permno AND mr.month = d.month
  ),
  -- 4. Lagged ME (mcap_t-1): at month t, use mcap from end of month t-1
  monthly_with_lag AS (
      SELECT permno,
             month,
             ret,
             hexcd,
             mcap_thousands,
             lagInFrame(mcap_thousands, 1) OVER w AS mcap_lag1_thousands
      FROM monthly
      WINDOW w AS (
          PARTITION BY permno
          ORDER BY month
          ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
      )
  ),
  -- 5. MAX signal per (permno, month) — using dsfhdr for PIT filter
  max_sig AS (
      SELECT permno,
             makeDate32(toYear(toDate32OrNull(d.date)), toMonth(toDate32OrNull(d.date)), 1) AS month,
             max(d.ret)              AS max_signal
      FROM crsp_202601.dsf AS d
      INNER JOIN crsp_202601.dsfhdr AS h
          ON d.permno = h.permno
         AND d.date >= h.begdat
         AND d.date <= h.enddat
      WHERE h.hshrcd IN (10, 11)
        AND h.hexcd IN (1, 2, 3)
        AND d.date BETWEEN '1962-01-01' AND '2006-06-30'
        AND d.ret IS NOT NULL
        AND d.ret > -0.5
      GROUP BY permno, month
  ),
  -- 6. Monthly illiquidity proxy: mean daily |ret|/vol per month per permno.
  --    Standard Amihud-style ILLIQ using daily volume from dsf.
  --    Aggregated to monthly by averaging across trading days in the month.
  illiq_monthly AS (
      SELECT permno,
             makeDate32(toYear(toDate32OrNull(date)), toMonth(toDate32OrNull(date)), 1) AS month,
             avg(if(vol > 0 AND ret IS NOT NULL, abs(ret) / vol, 0)) AS illiq_dv
      FROM crsp_202601.dsf AS d
      INNER JOIN crsp_202601.dsfhdr AS h
          ON d.permno = h.permno
         AND d.date >= h.begdat
         AND d.date <= h.enddat
      WHERE h.hshrcd IN (10, 11)
        AND h.hexcd IN (1, 2, 3)
        AND d.date BETWEEN '1962-01-01' AND '2006-06-30'
        AND d.ret IS NOT NULL
        AND d.vol IS NOT NULL AND d.vol > 0
      GROUP BY permno, month
  ),
  -- 6b. Book equity per (gvkey, fyear)
  be_primary AS (
      SELECT gvkey, fyear,
             coalesce(ceq, 0) + coalesce(txdb, 0) - coalesce(pstkrv, 0) AS be_primary
      FROM comp_202601.funda
      WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
        AND fyear IS NOT NULL AND fyear BETWEEN 1961 AND 2005
  ),
  be_fallback AS (
      SELECT gvkey, fyear,
             coalesce(at, 0) - coalesce(dlc, 0) - coalesce(dltt, 0) - coalesce(pstkrv, 0) AS be_alt
      FROM comp_202601.funda
      WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
        AND fyear IS NOT NULL AND fyear BETWEEN 1961 AND 2005
  ),
  book_equity AS (
      SELECT b.gvkey, b.fyear,
             if(b.be_primary > 0, b.be_primary,
                if(fb.be_alt > 0, fb.be_alt, NULL)) AS be
      FROM be_primary AS b
      LEFT JOIN be_fallback AS fb
          ON b.gvkey = fb.gvkey AND b.fyear = fb.fyear
  ),
  -- 7. Link: gvkey -> permno (deduplicate; the link table records
  --    the same (gvkey, permno) pair multiple times for different
  --    link windows / liids — pick the longest active link per pair)
  link AS (
      SELECT gvkey, permno FROM (
          SELECT gvkey, lpermno AS permno,
                 dateDiff('day',
                          if(linkdt = '', '1925-01-01', toDate32OrNull(linkdt)),
                          if(linkenddt = '', '2099-12-31', toDate32OrNull(linkenddt))) AS link_span
          FROM crsp_202601.ccmxpf_linktable
          WHERE linktype IN ('LC', 'LU') AND linkprim IN ('P', 'C') AND usedflag = 1
      )
      GROUP BY gvkey, permno
  ),
  -- 8. December ME per (permno, calendar year)
  dec_me AS (
      SELECT permno,
             toYear(toDate32OrNull(date)) AS cyear,
             abs(prc) * shrout AS me_dec_thousands
      FROM crsp_202601.msf
      WHERE toMonth(toDate32OrNull(date)) = 12
        AND prc IS NOT NULL AND shrout IS NOT NULL AND shrout > 0
  ),
  -- 9. BM per (permno, fyear) — pair fiscal year Y with Dec of Y-1.
  --    Deduplicate by (permno, fyear) — when a permno is linked to multiple
  --    gvkeys (corporate restructuring / name change), take the BE from
  --    the most recently active link at fyear time.
  bm_table AS (
      SELECT permno, fyear, avg(bm) AS bm FROM (
          SELECT l.permno AS permno,
                 b.fyear  AS fyear,
                 (b.be * 1000000.0) / nullIf(d.me_dec_thousands * 1000.0, 0) AS bm
          FROM book_equity AS b
          INNER JOIN link AS l ON b.gvkey = l.gvkey
          LEFT JOIN dec_me AS d
              ON l.permno = d.permno AND b.fyear = d.cyear - 1
          WHERE b.be IS NOT NULL AND b.be > 0
      )
      GROUP BY permno, fyear
  ),
  -- 10. FF factors
  ff AS (
      SELECT toDate32OrNull(dt) AS month,
             mkt_rf, smb, hml, mom, rf
      FROM ff.four_factor_monthly
      WHERE toDate32OrNull(dt) BETWEEN toDate32('1962-07-01') AND toDate32('2005-12-31')
  ),
  -- 11. Assemble: monthly + max_sig + bm (via fyear_use) + ff factors
  base AS (
      SELECT m.month              AS month,
             m.permno             AS permno,
             m.ret                AS ret,
             ms.max_signal        AS max_signal,
             m.mcap_thousands     AS mcap,
             m.mcap_lag1_thousands AS mcap_lag1,
             m.hexcd              AS hexcd
      FROM monthly_with_lag AS m
      INNER JOIN max_sig AS ms
          ON m.permno = ms.permno AND m.month = ms.month
      WHERE m.mcap_lag1_thousands IS NOT NULL
        AND m.mcap_lag1_thousands > 0
  ),
  base_with_bm AS (
      SELECT b.month        AS month,
             b.permno       AS permno,
             b.ret          AS ret,
             b.max_signal   AS max_signal,
             b.mcap         AS mcap,
             b.mcap_lag1    AS mcap_lag1,
             b.hexcd        AS hexcd,
             if(toMonth(b.month) >= 7,
                toYear(b.month) - 1,
                toYear(b.month) - 2) AS fyear_use,
             bm.bm          AS bm,
             il.illiq_dv    AS illiq
      FROM base AS b
      LEFT JOIN bm_table AS bm ON b.permno = bm.permno AND (
          if(toMonth(b.month) >= 7, toYear(b.month) - 1, toYear(b.month) - 2) = bm.fyear
      )
      LEFT JOIN illiq_monthly AS il ON b.permno = il.permno AND b.month = il.month
  )
SELECT bb.month        AS month,
       bb.permno       AS permno,
       bb.ret          AS ret,
       bb.max_signal   AS max_signal,
       bb.mcap         AS mcap,
       bb.mcap_lag1    AS mcap_lag1,
       bb.hexcd        AS hexcd,
       bb.bm           AS bm,
       bb.illiq        AS illiq,
       f.mkt_rf        AS mkt_rf,
       f.smb           AS smb,
       f.hml           AS hml,
       f.mom           AS mom,
       f.rf            AS rf
FROM base_with_bm AS bb
INNER JOIN ff AS f
    ON toYear(bb.month)  = toYear(f.month)
   AND toMonth(bb.month) = toMonth(f.month)
WHERE bb.month >= toDate32('1962-07-01')
SETTINGS join_algorithm = 'partial_merge',
         max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0