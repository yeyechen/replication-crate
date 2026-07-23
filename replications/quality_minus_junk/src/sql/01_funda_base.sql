-- 01_funda_base.sql
-- Purpose: Compustat annual fundamentals (funda) with the standard quality
--          filter, deduplicated to one row per (gvkey, fyear), with the
--          per-row building blocks computed: working capital WC, book
--          equity BE, gross profits GP. Explicit column lists throughout
--          (no alias.* — ClickHouse keeps qualifiers in CTE column names).
-- Tables: comp_202601.funda
-- Output: write_yeye.qmj_funda_base — one row per (gvkey, fyear)
-- Depends on: (none)
-- Paper: Asness, Frazzini, Pedersen (2019) "Quality Minus Junk", Appendix 1:
--   * WC = ACT - LCT - CHE + DLC + TXP  (che/dlc/txp coalesced to 0 when
--     missing — standard convention for frequently-missing secondary
--     items; flagged for the Replicator)
--   * BE = (SEQ; else CEQ + PSTK; else AT - LT - MIB) - (PSTKRV; else
--     PSTKL; else PSTK)
--   * GP = REVT - COGS
-- Filter: indfmt='INDL', consol='C', popsrc='D', datafmt='STD'.
--   NOTE: the task spec said consol='STD' but no such value exists in the
--   data (values: C/D/R/P); 'C' (consolidated) is the WRDS standard per
--   references/COMPUSTAT.md. Flagged for the Replicator.
-- Dedup: funda is unique on (gvkey, datadate) under the filter (verified:
--   0 dups); 425 rows duplicate (gvkey, fyear) via fiscal-year changes —
--   keep the latest datadate per (gvkey, fyear).

CREATE OR REPLACE TABLE write_yeye.qmj_funda_base
ENGINE = MergeTree ORDER BY (gvkey, fyear) AS
WITH
filt AS (
    SELECT
        assumeNotNull(gvkey)            AS gvkey,
        assumeNotNull(toDate32(datadate)) AS datadate,
        assumeNotNull(fyear)            AS fyear,
        revt   AS revt,
        cogs   AS cogs,
        at     AS at,
        ib     AS ib,
        dp     AS dp,
        act    AS act,
        lct    AS lct,
        che    AS che,
        dlc    AS dlc,
        txp    AS txp,
        dltt   AS dltt,
        seq    AS seq,
        ceq    AS ceq,
        pstk   AS pstk,
        pstkrv AS pstkrv,
        pstkl  AS pstkl,
        lt     AS lt,
        mib    AS mib,
        mibt   AS mibt,
        capx   AS capx,
        sale   AS sale,
        pi     AS pi,
        prcc_f AS prcc_f,
        csho   AS csho,
        re     AS re,
        ebit   AS ebit
    FROM comp_202601.funda
    WHERE indfmt = 'INDL' AND consol = 'C' AND popsrc = 'D' AND datafmt = 'STD'
      AND gvkey IS NOT NULL AND datadate IS NOT NULL AND fyear IS NOT NULL
      AND toDate32(datadate) <= toDate32('2016-12-31')
),
dedup AS (
    SELECT
        gvkey, datadate, fyear,
        revt, cogs, at, ib, dp, act, lct, che, dlc, txp, dltt,
        seq, ceq, pstk, pstkrv, pstkl, lt, mib, mibt, capx, sale, pi,
        prcc_f, csho, re, ebit
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY gvkey, fyear
                                  ORDER BY datadate DESC) AS rn
        FROM filt
    )
    WHERE rn = 1
)
SELECT
    gvkey,
    datadate,
    fyear,
    revt, cogs, at, ib, dp, act, lct, dlc, dltt, lt, mibt, capx, sale, pi,
    prcc_f, csho, re, ebit, pstk,
    -- working capital (che/dlc/txp coalesced to 0)
    act - lct - coalesce(che, 0) + coalesce(dlc, 0) + coalesce(txp, 0)
        AS wc,
    -- book equity: (SEQ; else CEQ+PSTK; else AT-LT-MIB) - preferred
    multiIf(
        seq IS NOT NULL, seq,
        ceq IS NOT NULL, ceq + coalesce(pstk, 0),
        at IS NOT NULL AND lt IS NOT NULL, at - lt - coalesce(mib, 0),
        CAST(NULL, 'Nullable(Float64)')
    ) - coalesce(pstkrv, pstkl, pstk, 0) AS be,
    -- gross profits
    revt - cogs AS gp
FROM dedup
SETTINGS allow_experimental_analyzer = 0,
         max_execution_time = 900,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
