-- panel_no_clip.sql
-- DIAGNOSTIC VARIANT of panel.sql for audit [M2] (assumption 24).
-- Identical to panel.sql EXCEPT that the final `clipped` CTE passes the
-- per-year 1%/99% winsorized `delta_*_pre` columns through unchanged —
-- i.e. no +/-0.25 / +/-1.0 / +/-2.0 absolute-value clip. Used to show that
-- the ΔATO clip is load-bearing for the headline coefficient. Regenerated
-- from panel.sql in iteration 3 so it stays in sync with the union IBES
-- link (assumption 28) and the raw RSST columns (assumption 26).
-- NOT used for any reported table.
--
-- Purpose (inherited): Build the analysis-ready panel by composing:
--          (1) comp_fundamentals (NOA, PM, ATO, RNOA, avg_NOA),
--          (2) accounting changes (ΔNOA, ΔPM, ΔATO, ΔRNOA),
--          (3) IBES + CRSP coverage filter (paper §III, L488-498, footnote 24),
--          (4) RSST accruals (WC, NCO, FIN, ΔWC, ΔNCO, ΔFIN),
--          (5) winsorized columns (column-suffix _w),
--          (6) Δ-variable heavy-tail filter (assumption 15) — restrict to
--              firms with avg_NOA >= $10M (going-concern size filter that
--              removes microcap firms whose ATO ratios fluctuate wildly),
--              and apply an absolute-value clip on each Δ variable AFTER
--              per-year winsorization to further tame the still-fat inter-
--              year tails (paper ΔATO std = 0.15; before this fix the per-
--              year-winsorized ΔATO had std = 2.6). Clip thresholds are
--              asset-class-appropriate:
--                 ΔATO:  +/-0.25 (matches paper std=0.15)
--                 ΔPM:   +/-0.25 (matches paper std=0.058)
--                 ΔRNOA: +/-1.0  (allows the wider spread the paper shows)
--                 ΔNOA:  +/-2.0  (already on a -1..+inf ratio scale)
-- Tables: comp_202601.funda, comp_202601.company, comp_202601.security,
--         ibes_202601.statsumu_epsus, crsp_202601.ccmxpf_linktable,
--         crsp_202601.dsenames, crsp_202601.dsf
-- Output columns: gvkey, fyear, datadate, sic, NOA, avg_NOA, PM, ATO, RNOA,
--                 delta_NOA, delta_PM, delta_ATO, delta_RNOA, delta_RNOA_future,
--                 NOA_w, PM_w, ATO_w, RNOA_w, delta_NOA_w, delta_PM_w,
--                 delta_ATO_w, delta_RNOA_w, delta_RNOA_future_w,
--                 WC, NCO, FIN, delta_WC_w, delta_NCO_w, delta_FIN_w,
--                 delta_WC_raw_w, delta_NCO_raw_w, delta_FIN_raw_w
-- Depends on: ibes_link.sql, ibes_join.sql, crsp_join.sql (folded as CTEs)
-- Settings: max_execution_time=600, max_rows_to_read=5e8

WITH
  -- Step 1a: Compustat fundamentals with NOA construction
  comp_raw AS (
    SELECT
      f.gvkey,
      f.fyear AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      c.sic AS sic,
      f.at    AS AT,
      f.act   AS ACT,
      f.lct   AS LCT,
      f.che   AS CHE,
      f.ivst  AS IVST,
      f.dltt  AS DLTT,
      f.dlc   AS DLC,
      f.ceq   AS CEQ,
      f.mib   AS MIB,
      f.pstk  AS PSTK,
      f.oiadp AS OIADP,
      f.sale  AS SALE
    FROM comp_202601.funda AS f
    INNER JOIN comp_202601.company AS c ON f.gvkey = c.gvkey
    WHERE f.indfmt = 'INDL'
      AND f.consol = 'C'
      AND f.popsrc  = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.at    IS NOT NULL
      AND f.oiadp IS NOT NULL
      AND f.sale  IS NOT NULL
      AND f.sale  > 0
      AND c.sic   IS NOT NULL
      AND NOT (toInt32OrZero(c.sic) BETWEEN 6000 AND 6999)
  ),
  comp_with_noa AS (
    SELECT
      gvkey, fyear, datadate, sic,
      AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
      OIADP, SALE,
      (DLTT + DLC + CEQ + MIB + PSTK) - (CHE + IVST) AS NOA
    FROM comp_raw
    WHERE OIADP > 0
      AND ACT IS NOT NULL AND LCT IS NOT NULL
      AND CHE IS NOT NULL AND IVST IS NOT NULL
      AND DLTT IS NOT NULL AND DLC IS NOT NULL
      AND CEQ IS NOT NULL AND MIB IS NOT NULL AND PSTK IS NOT NULL
  ),
  comp_dedup AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, sic,
        AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
        OIADP, SALE, NOA,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM comp_with_noa
    )
    WHERE rn = 1
  ),
  comp AS (
    SELECT * FROM comp_dedup
    WHERE NOA > 0 AND isFinite(NOA)
  ),
  -- Step 1b: Per-firm lagged NOA + ratios (PM, ATO, RNOA, avg_NOA).
  comp_with_lags AS (
    SELECT
      gvkey, fyear, datadate, sic,
      AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
      OIADP, SALE, NOA,
      lagInFrame(NOA, 1) OVER w AS NOA_lag1
    FROM comp
    WINDOW w AS (PARTITION BY gvkey ORDER BY fyear
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  ),
  ratios AS (
    SELECT
      gvkey, fyear, datadate, sic,
      AT, ACT, LCT, CHE, IVST, DLTT, DLC, CEQ, MIB, PSTK,
      OIADP, SALE, NOA, NOA_lag1,
      OIADP / SALE AS PM,
      (NOA + NOA_lag1) / 2.0 AS avg_NOA,
      SALE / ((NOA + NOA_lag1) / 2.0) AS ATO,
      OIADP / ((NOA + NOA_lag1) / 2.0) AS RNOA
    FROM comp_with_lags
    WHERE NOA_lag1 IS NOT NULL
  ),
  -- Step 1c: IBES coverage flag — see assumptions.md#11 and #28.
  -- gvkey -> IBES ticker via the UNION of two links (assumption 28,
  -- audit [M6]):
  --   (a) comp_202601.security.ibtic  (Compustat-native IBES ticker)
  --   (b) CRSP historical CUSIP path: gvkey -> permno (ccmxpf_linktable)
  --       -> dsenames.ncusip (8-char, point-in-time) -> ibes cusip
  --       (statsumu_epsus.cusip is the 8-char CUSIP).
  -- (b) is the ICLINK-style CUSIP link the audit asked for. NOTE:
  -- comp_202601.security.cusip is the CURRENT 9-char CUSIP only (no
  -- history), so joining it to IBES recovers FEWER firm-years than
  -- ibtic (47,250 vs 65,988 — see src/sql/ibes_link.sql). The CRSP
  -- ncusip path is point-in-time and does better (68,930). The union
  -- of (a) and (b) is used.
  ibes_ticker_universe AS (
    SELECT DISTINCT
      ticker,
      substring(cusip, 1, 8) AS cusip8,
      toInt32OrZero(substring(fpedats, 1, 4)) AS fy
    FROM ibes_202601.statsumu_epsus
    WHERE fpedats IS NOT NULL
      AND toInt32OrZero(substring(fpedats, 1, 4)) BETWEEN 1984 AND 2002
  ),
  gvkey_ncusip AS (
    SELECT DISTINCT
      l.gvkey                    AS gvkey,
      substring(n.ncusip, 1, 8)  AS cusip8
    FROM crsp_202601.ccmxpf_linktable AS l
    INNER JOIN crsp_202601.dsenames AS n
      ON n.permno = toInt32(l.lpermno)
    WHERE l.linktype IN ('LC', 'LU') AND l.linkprim IN ('P', 'C')
      AND l.lpermno IS NOT NULL AND l.gvkey IS NOT NULL
      AND n.ncusip IS NOT NULL AND n.ncusip != ''
  ),
  ibes_coverage AS (
    SELECT DISTINCT gvkey, fyear
    FROM (
      SELECT
        s.gvkey AS gvkey,
        t.fy    AS fyear
      FROM comp_202601.security AS s
      INNER JOIN ibes_ticker_universe AS t ON t.ticker = s.ibtic
      WHERE s.gvkey IS NOT NULL AND s.ibtic IS NOT NULL AND s.ibtic != ''
      UNION ALL
      SELECT
        g.gvkey AS gvkey,
        t.fy    AS fyear
      FROM gvkey_ncusip AS g
      INNER JOIN ibes_ticker_universe AS t ON t.cusip8 = g.cusip8
    )
  ),
  -- Step 1d: CRSP coverage flag — see assumptions.md#11.
  -- Map gvkey -> permno via crsp_202601.ccmxpf_linktable, PIT-joined on
  -- fiscal year-end datadate. Keep (gvkey, fyear) tuples where any
  -- linked permno has at least one dsf return record in the 12 months
  -- following fiscal year-end. The link table subquery pre-filters to
  -- primary links (linktype IN LC/LU, linkprim IN P/C, lpermno not null)
  -- and transforms NULL linkenddt to a far-future sentinel so the main
  -- date arithmetic is straightforward.
  crsp_coverage AS (
    SELECT DISTINCT c.gvkey AS gvkey, c.fyear AS fyear
    FROM comp AS c
    INNER JOIN (
      SELECT DISTINCT
        l.gvkey                AS gvkey,
        toInt32(l.lpermno)     AS permno,
        toDate32OrNull(l.linkdt) AS linkdt,
        if(l.linkenddt = '0000-00-00' OR l.linkenddt IS NULL,
           toDate32OrNull('2099-12-31'),
           toDate32OrNull(l.linkenddt)) AS linkenddt
      FROM crsp_202601.ccmxpf_linktable AS l
      WHERE l.linktype IN ('LC', 'LU')
        AND l.linkprim IN ('P', 'C')
        AND l.lpermno  IS NOT NULL
        AND l.gvkey    IS NOT NULL
    ) AS lk
      ON lk.gvkey = c.gvkey
     AND c.datadate >= lk.linkdt
     AND c.datadate <= lk.linkenddt
    INNER JOIN crsp_202601.dsf AS d
      ON d.permno = lk.permno
     AND toDate32OrNull(d.date) >  c.datadate
     AND toDate32OrNull(d.date) <= addMonths(c.datadate, 12)
     AND d.ret IS NOT NULL
  ),
  -- Step 1e: Compustat panel restricted to (gvkey, fyear) tuples with
  -- both IBES and CRSP coverage. This is the "final" comp universe
  -- matching the paper's §III Sample criteria.
  comp_filtered AS (
    SELECT DISTINCT gvkey, fyear
    FROM comp
    WHERE (gvkey, fyear) IN (
      SELECT gvkey, fyear FROM ibes_coverage
    )
    AND (gvkey, fyear) IN (
      SELECT gvkey, fyear FROM crsp_coverage
    )
  ),
  -- Step 2: ΔNOA, ΔPM, ΔATO via window lag; ΔRNOA via self-join.
  -- Restrict to comp_filtered (IBES+CRSP covered tuples). Use an explicit
  -- WHERE-clause semi-join via IN since ClickHouse's analyzer sometimes
  -- mis-resolves CTE references in joins when the CTE itself uses an
  -- inner subquery alias.
  changes AS (
    SELECT
      r.gvkey,
      r.fyear,
      r.datadate,
      r.sic,
      r.AT, r.ACT, r.LCT, r.CHE, r.IVST, r.DLTT, r.DLC, r.CEQ, r.MIB, r.PSTK,
      r.OIADP, r.SALE,
      r.NOA, r.NOA_lag1, r.avg_NOA,
      r.PM, r.ATO, r.RNOA,
      (r.NOA - r.NOA_lag1) / r.NOA_lag1 AS delta_NOA,
      r.PM - lagInFrame(r.PM, 1)  OVER (PARTITION BY r.gvkey ORDER BY r.fyear
                                        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_PM,
      r.ATO - lagInFrame(r.ATO, 1) OVER (PARTITION BY r.gvkey ORDER BY r.fyear
                                         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_ATO,
      -- ΔRNOA: TWO distinct quantities in the paper.
      --   delta_RNOA: current period's change = RNOA_t - RNOA_{t-1}
      --     (regressor in Table 3 Panel B; current change).
      --   delta_RNOA_future: future change = RNOA_{t+1} - RNOA_t
      --     (LHS dependent variable in Table 3 Panel B).
      -- The original implementation conflated these and used the LHS
      -- formula in reverse sign. See assumptions.md#12.
      r.RNOA - lagInFrame(r.RNOA, 1) OVER (PARTITION BY r.gvkey ORDER BY r.fyear
                                            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_RNOA,
      fwd.RNOA - r.RNOA    AS delta_RNOA_future
    FROM ratios AS r
    LEFT JOIN ratios AS fwd
        ON r.gvkey = fwd.gvkey AND r.fyear = fwd.fyear - 1
    WHERE (r.gvkey, r.fyear) IN (
      SELECT gvkey, fyear FROM comp_filtered
    )
  ),
  -- Step 3: RSST accruals (WC, NCO, FIN, ΔWC, ΔNCO, ΔFIN)
  rsst_raw AS (
    SELECT
      f.gvkey,
      f.fyear AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      f.act   AS ACT,
      f.lct   AS LCT,
      f.che   AS CHE,
      f.ivst  AS IVST,
      f.dltt  AS DLTT,
      f.dlc   AS DLC,
      f.pstk  AS PSTK,
      f.at    AS AT,
      f.lt    AS LT
    FROM comp_202601.funda AS f
    WHERE f.indfmt = 'INDL' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.datafmt = 'STD'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.at IS NOT NULL AND f.act IS NOT NULL AND f.lct IS NOT NULL
      AND f.che IS NOT NULL AND f.ivst IS NOT NULL
      AND f.dltt IS NOT NULL AND f.dlc IS NOT NULL AND f.pstk IS NOT NULL
      AND f.lt IS NOT NULL
  ),
  rsst_levels AS (
    SELECT
      gvkey, fyear, datadate,
      (ACT - CHE) - (LCT - DLC)        AS WC,
      AT - ACT - IVST                   AS NCOA,
      LT - LCT - DLTT                   AS NCOL,
      (AT - ACT - IVST) - (LT - LCT - DLTT) AS NCO,
      IVST + IVST                       AS FINA,
      DLTT + DLC + PSTK                 AS FINL,
      (IVST + IVST) - (DLTT + DLC + PSTK) AS FIN
    FROM rsst_raw
  ),
  -- Normalize RSST levels by total assets (Sloan 1996 / RSST 2005
  -- convention — accruals scaled by lagged total assets). This puts
  -- WC, NCO, FIN on the same scale as the LHS (ΔRNOA is a ratio).
  -- Without normalization the RSST regression coefficients come out
  -- essentially zero (e.g., a 1-unit change in raw ΔWC in millions
  -- of dollars on a ΔRNOA of ~0.1 ratio is 10^7 effect — see
  -- assumptions.md#14). We divide by total assets so the
  -- coefficients are interpretable in ratio units.
  -- We carry BOTH the AT-normalized levels (WC, NCO, FIN — used for the
  -- Table 3 Panel B / Table 7 baseline) AND the raw $-million levels
  -- (WC_raw, NCO_raw, FIN_raw) so that the raw-vs-normalized rank
  -- transform can be tested head-to-head (assumption 26, audit [M3]).
  rsst_scaled AS (
    SELECT
      l.gvkey, l.fyear, l.datadate,
      l.WC  / nullIf(r.AT, 0) AS WC,
      l.NCO / nullIf(r.AT, 0) AS NCO,
      l.FIN / nullIf(r.AT, 0) AS FIN,
      l.WC  AS WC_raw,
      l.NCO AS NCO_raw,
      l.FIN AS FIN_raw
    FROM rsst_levels AS l
    INNER JOIN rsst_raw AS r
      ON r.gvkey = l.gvkey AND r.fyear = l.fyear AND r.datadate = l.datadate
  ),
  rsst_dedup AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, WC, NCO, FIN, WC_raw, NCO_raw, FIN_raw,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM rsst_scaled
    )
    WHERE rn = 1
  ),
  rsst_changes AS (
    SELECT
      gvkey, fyear, datadate,
      WC, NCO, FIN,
      WC - lagInFrame(WC, 1)  OVER (PARTITION BY gvkey ORDER BY fyear
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_WC,
      NCO - lagInFrame(NCO, 1) OVER (PARTITION BY gvkey ORDER BY fyear
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_NCO,
      FIN - lagInFrame(FIN, 1) OVER (PARTITION BY gvkey ORDER BY fyear
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_FIN,
      WC_raw - lagInFrame(WC_raw, 1)  OVER (PARTITION BY gvkey ORDER BY fyear
                                    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_WC_raw,
      NCO_raw - lagInFrame(NCO_raw, 1) OVER (PARTITION BY gvkey ORDER BY fyear
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_NCO_raw,
      FIN_raw - lagInFrame(FIN_raw, 1) OVER (PARTITION BY gvkey ORDER BY fyear
                                     ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS delta_FIN_raw
    FROM rsst_dedup
  ),
  rsst AS (
    SELECT *
    FROM rsst_changes
    WHERE delta_WC IS NOT NULL
  ),
  -- Step 4: Join NOA/PM/ATO/RNOA panel with RSST panel, restricted to
  -- the IBES+CRSP coverage set AND the avg_NOA >= $10M "going-concern"
  -- size filter (assumption 15) that excludes very small firms whose
  -- ATO and ΔATO magnitudes fluctuate wildly.
  merged AS (
    SELECT
      ch.gvkey,
      ch.fyear,
      ch.datadate,
      ch.sic,
      ch.NOA, ch.avg_NOA,
      ch.PM, ch.ATO, ch.RNOA,
      ch.delta_NOA, ch.delta_PM, ch.delta_ATO, ch.delta_RNOA,
      ch.delta_RNOA_future,
      rs.WC, rs.NCO, rs.FIN,
      rs.delta_WC, rs.delta_NCO, rs.delta_FIN,
      rs.delta_WC_raw, rs.delta_NCO_raw, rs.delta_FIN_raw
    FROM changes AS ch
    INNER JOIN rsst AS rs ON ch.gvkey = rs.gvkey AND ch.fyear = rs.fyear
    WHERE ch.avg_NOA >= 10
  ),
  -- Step 5: Winsorize within fiscal year at 1%/99% per assumption 2
  bounds AS (
    SELECT
      fyear,
      quantileExact(0.01)(NOA)      AS NOA_p01,
      quantileExact(0.99)(NOA)      AS NOA_p99,
      quantileExact(0.01)(PM)       AS PM_p01,
      quantileExact(0.99)(PM)       AS PM_p99,
      quantileExact(0.01)(ATO)      AS ATO_p01,
      quantileExact(0.99)(ATO)      AS ATO_p99,
      quantileExact(0.01)(RNOA)     AS RNOA_p01,
      quantileExact(0.99)(RNOA)     AS RNOA_p99,
      quantileExact(0.01)(delta_NOA)  AS delta_NOA_p01,
      quantileExact(0.99)(delta_NOA)  AS delta_NOA_p99,
      quantileExact(0.01)(delta_PM)   AS delta_PM_p01,
      quantileExact(0.99)(delta_PM)   AS delta_PM_p99,
      quantileExact(0.01)(delta_ATO)  AS delta_ATO_p01,
      quantileExact(0.99)(delta_ATO)  AS delta_ATO_p99,
      quantileExact(0.01)(delta_RNOA) AS delta_RNOA_p01,
      quantileExact(0.99)(delta_RNOA) AS delta_RNOA_p99,
      quantileExact(0.01)(delta_RNOA_future) AS delta_RNOA_future_p01,
      quantileExact(0.99)(delta_RNOA_future) AS delta_RNOA_future_p99,
      quantileExact(0.01)(delta_WC) AS delta_WC_p01,
      quantileExact(0.99)(delta_WC) AS delta_WC_p99,
      quantileExact(0.01)(delta_NCO) AS delta_NCO_p01,
      quantileExact(0.99)(delta_NCO) AS delta_NCO_p99,
      quantileExact(0.01)(delta_FIN) AS delta_FIN_p01,
      quantileExact(0.99)(delta_FIN) AS delta_FIN_p99,
      quantileExact(0.01)(delta_WC_raw) AS delta_WC_raw_p01,
      quantileExact(0.99)(delta_WC_raw) AS delta_WC_raw_p99,
      quantileExact(0.01)(delta_NCO_raw) AS delta_NCO_raw_p01,
      quantileExact(0.99)(delta_NCO_raw) AS delta_NCO_raw_p99,
      quantileExact(0.01)(delta_FIN_raw) AS delta_FIN_raw_p01,
      quantileExact(0.99)(delta_FIN_raw) AS delta_FIN_raw_p99
    FROM merged
    GROUP BY fyear
  ),
  winsorized AS (
    SELECT
      m.gvkey,
      m.fyear,
      m.datadate,
      m.sic,
      m.NOA, m.avg_NOA,
      m.PM, m.ATO, m.RNOA,
      m.delta_NOA, m.delta_PM, m.delta_ATO, m.delta_RNOA,
      m.delta_RNOA_future,
      m.WC, m.NCO, m.FIN,
      m.delta_WC, m.delta_NCO, m.delta_FIN,
      least(greatest(m.NOA, b.NOA_p01), b.NOA_p99)        AS NOA_w,
      least(greatest(m.PM,  b.PM_p01),  b.PM_p99)         AS PM_w,
      least(greatest(m.ATO, b.ATO_p01), b.ATO_p99)        AS ATO_w,
      least(greatest(m.RNOA, b.RNOA_p01), b.RNOA_p99)     AS RNOA_w,
      -- Per-year winsorization then absolute-value clip on delta
      -- variables (assumption 15). The per-year 1%/99% winsorization
      -- catches the worst outliers within each year; the absolute
      -- clip catches the still-large inter-year tail. The paper's
      -- ΔATO std is 0.15; pre-fix the per-year-winsorized ΔATO had
      -- std = 2.6 with a fat left tail (p25 = -0.82, paper: -0.15).
      -- The clip at +/-0.25 brings ΔATO std down to ~0.18 -- much
      -- closer to the paper while preserving the bulk of the
      -- distribution. The clip thresholds reflect the order-of-
      -- magnitude of typical accounting-ratio changes:
      --   ΔATO can be much larger than ΔPM (sales/Numerator vs
      --     earnings/denominator)
      --   ΔRNOA / ΔRNOA_future are ratio-on-ratio changes that are
      --     bounded by larger ranges than ΔATO.
      least(greatest(m.delta_NOA,  b.delta_NOA_p01),  b.delta_NOA_p99)  AS delta_NOA_pre,
      least(greatest(m.delta_PM,   b.delta_PM_p01),   b.delta_PM_p99)   AS delta_PM_pre,
      least(greatest(m.delta_ATO,  b.delta_ATO_p01),  b.delta_ATO_p99)  AS delta_ATO_pre,
      least(greatest(m.delta_RNOA, b.delta_RNOA_p01), b.delta_RNOA_p99) AS delta_RNOA_pre,
      least(greatest(m.delta_RNOA_future, b.delta_RNOA_future_p01), b.delta_RNOA_future_p99) AS delta_RNOA_future_pre,
      least(greatest(m.delta_WC, b.delta_WC_p01), b.delta_WC_p99) AS delta_WC_w,
      least(greatest(m.delta_NCO, b.delta_NCO_p01), b.delta_NCO_p99) AS delta_NCO_w,
      least(greatest(m.delta_FIN, b.delta_FIN_p01), b.delta_FIN_p99) AS delta_FIN_w,
      least(greatest(m.delta_WC_raw, b.delta_WC_raw_p01), b.delta_WC_raw_p99) AS delta_WC_raw_w,
      least(greatest(m.delta_NCO_raw, b.delta_NCO_raw_p01), b.delta_NCO_raw_p99) AS delta_NCO_raw_w,
      least(greatest(m.delta_FIN_raw, b.delta_FIN_raw_p01), b.delta_FIN_raw_p99) AS delta_FIN_raw_w
    FROM merged AS m
    INNER JOIN bounds AS b ON m.fyear = b.fyear
  ),
  -- Apply absolute-value clip after per-year winsorization. Each
  -- delta variable is clipped to its +/- threshold.
  clipped AS (
    SELECT
      gvkey, fyear, datadate, sic,
      NOA, avg_NOA,
      PM, ATO, RNOA,
      delta_NOA, delta_PM, delta_ATO, delta_RNOA, delta_RNOA_future,
      delta_ATO_pre, delta_PM_pre, delta_RNOA_pre, delta_RNOA_future_pre, delta_NOA_pre,
      NOA_w, PM_w, ATO_w, RNOA_w,
      WC, NCO, FIN,
      -- NO-CLIP: pass through the per-year 1%/99% winsorized values
      -- directly (no +/-0.25 / +/-1.0 / +/-2.0 absolute-value threshold).
      delta_ATO_pre         AS delta_ATO_w,
      delta_PM_pre          AS delta_PM_w,
      delta_RNOA_pre        AS delta_RNOA_w,
      delta_RNOA_future_pre AS delta_RNOA_future_w,
      delta_NOA_pre         AS delta_NOA_w,
      delta_WC_w, delta_NCO_w, delta_FIN_w,
      delta_WC_raw_w, delta_NCO_raw_w, delta_FIN_raw_w
    FROM winsorized
  )
SELECT
  gvkey, fyear, datadate, sic,
  NOA, avg_NOA,
  PM, ATO, RNOA,
  delta_NOA, delta_PM, delta_ATO, delta_RNOA, delta_RNOA_future,
  NOA_w, PM_w, ATO_w, RNOA_w,
  delta_NOA_w, delta_PM_w, delta_ATO_w, delta_RNOA_w, delta_RNOA_future_w,
  WC, NCO, FIN,
  delta_WC_w, delta_NCO_w, delta_FIN_w,
  delta_WC_raw_w, delta_NCO_raw_w, delta_FIN_raw_w
FROM clipped
-- Deterministic row order. ClickHouse returns rows in a
-- parallelism-dependent order; the Python decile-rank transform
-- breaks ties with `rank(method='first')`, and the clipped Δ
-- variables have many exact ties at the +/- clip bounds. Without a
-- stable ORDER BY the Table 7 rank regressions were not
-- reproducible run-to-run (headline ΔATO moved 0.053 <-> 0.069).
ORDER BY gvkey, fyear
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0
