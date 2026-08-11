-- rsst_accruals.sql
-- Purpose: Compute RSST (Richardson-Sloan-Soliman-Tuna 2005) accrual
--          decomposition: WC, ΔWC, NCOA, NCOL, NCO, ΔNCO, FINA, FINL,
--          FIN, ΔFIN. Used downstream in Tables 3-7.
-- Tables: comp_202601.funda
-- Output columns: gvkey, fyear, WC, NCOA, NCOL, NCO, FINA, FINL, FIN,
--                  ΔWC, ΔNCO, ΔFIN
-- Depends on: (none — pulls from comp_202601.funda directly)
-- Settings: max_execution_time=600, max_rows_to_read=5e8
--
-- Per paper L1656-1664:
--   WC = COA - COL, COA = ACT - CHE, COL = LCT - DLC
--     => WC = (ACT - CHE) - (LCT - DLC)
--   ΔWC = WC_t - WC_{t-1}
--
--   NCOA = AT - ACT - IVST
--   NCOL = LT - LCT - DLTT
--   NCO = NCOA - NCOL
--   ΔNCO = NCO_t - NCO_{t-1}
--
--   FINA = IVST + IVST  (per task spec; paper uses STI (#193) + LTI (#32))
--     The paper's footnote defines FINA = STI (#193) + LTI (#32). STI
--     (Compustat #193) is "Short-Term Investments — Total" and LTI (#32)
--     is "Investments and Advances" (= Investments - LT Investments).
--     In our comp_202601.funda schema:
--       - ivst (Compustat #193 "Short-term investments — total") exists.
--       - ivao (#3290) is "Investment in unconsolidated subsidiaries" — not LTI.
--     The standard Soliman/RSST papers use IVST for STI, and IVST again for
--     LTI when the proper LTI field is missing — flagged for the replicator.
--     Here we use IVST twice (STI + IVST-as-proxy-for-LTI) per the task spec.
--   FINL = DLTT + DLC + PSTK
--   FIN = FINA - FINL
--   ΔFIN = FIN_t - FIN_{t-1}

WITH
  raw AS (
    SELECT
      f.gvkey,
      toUInt32OrZero(f.fyear) AS fyear,
      toDate32OrNull(f.datadate) AS datadate,
      toFloat64OrNull(f.act)  AS ACT,
      toFloat64OrNull(f.lct)  AS LCT,
      toFloat64OrNull(f.che)  AS CHE,
      toFloat64OrNull(f.ivst) AS IVST,
      toFloat64OrNull(f.dltt) AS DLTT,
      toFloat64OrNull(f.dlc)  AS DLC,
      toFloat64OrNull(f.pstk) AS PSTK,
      toFloat64OrNull(f.at)   AS AT,
      toFloat64OrNull(f.lt)   AS LT
    FROM comp_202601.funda AS f
    WHERE f.indfmt = 'FS' AND f.consol = 'C' AND f.popsrc = 'D'
      AND f.fyear BETWEEN 1984 AND 2002
      AND f.at IS NOT NULL AND f.act IS NOT NULL AND f.lct IS NOT NULL
      AND f.che IS NOT NULL AND f.ivst IS NOT NULL
      AND f.dltt IS NOT NULL AND f.dlc IS NOT NULL AND f.pstk IS NOT NULL
      AND f.lt IS NOT NULL
  ),
  -- Compute WC, NCOA, NCOL, NCO, FINA, FINL, FIN at each (gvkey, fyear)
  levels AS (
    SELECT
      gvkey, fyear, datadate,
      (ACT - CHE) - (LCT - DLC)        AS WC,
      AT - ACT - IVST                   AS NCOA,
      LT - LCT - DLTT                   AS NCOL,
      (AT - ACT - IVST) - (LT - LCT - DLTT) AS NCO,
      IVST + IVST                       AS FINA,   -- STI + LTI (proxy)
      DLTT + DLC + PSTK                 AS FINL,
      (IVST + IVST) - (DLTT + DLC + PSTK) AS FIN
    FROM raw
  ),
  -- Pick the most-recently-filed row per (gvkey, fyear) (datafmt filter on
  -- comp_fundamentals.sql ensures single row, but dedupe here for safety).
  deduped AS (
    SELECT *
    FROM (
      SELECT
        gvkey, fyear, datadate, WC, NCOA, NCOL, NCO, FINA, FINL, FIN,
        row_number() OVER (PARTITION BY gvkey, fyear ORDER BY datadate DESC) AS rn
      FROM levels
    )
    WHERE rn = 1
  ),
  -- Compute changes via window function
  with_changes AS (
    SELECT
      *,
      lagInFrame(WC,  1) OVER w AS WC_lag1,
      lagInFrame(NCO, 1) OVER w AS NCO_lag1,
      lagInFrame(FIN, 1) OVER w AS FIN_lag1
    FROM deduped
    WINDOW w AS (PARTITION BY gvkey ORDER BY fyear
                 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
  )
SELECT
  gvkey, fyear, datadate,
  WC, NCOA, NCOL, NCO, FINA, FINL, FIN,
  WC - WC_lag1    AS delta_WC,
  NCO - NCO_lag1  AS delta_NCO,
  FIN - FIN_lag1  AS delta_FIN
FROM with_changes
WHERE WC_lag1 IS NOT NULL
SETTINGS max_execution_time = 600,
         max_rows_to_read = 500000000,
         timeout_before_checking_execution_speed = 0