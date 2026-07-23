-- compustat_funda.sql
-- Purpose: Novy-Marx (2013) annual fundamentals — GP/A (the key signal),
--          book equity, earnings/BE, FCF/BE — with the standard Compustat
--          quality filter and financials (SIC 6xx) excluded.
-- Tables: comp_202601.funda
-- Output columns: gvkey, datadate, calyear, fyear, sich, at, gross_profit,
--                 gp_a, stockholders_equity, deferred_taxes,
--                 preferred_stock, book_equity, earnings_be, fcf_be
-- Depends on: (none)
-- Notes:
--   * Standard filter: indfmt='INDL', consol='C', popsrc='D',
--     datafmt='STD'. With these, (gvkey, datadate) is unique in this
--     extract (verified: 407,360 rows = 407,360 keys, fyear 1962-2010).
--   * GP = REVT - COGS, falling back to the GP data item when REVT or
--     COGS is missing (paper footnote 2; GP item covers ~90% of rows
--     pre-2000 in this extract).
--   * Book equity (paper footnote 2):
--       (SEQ, else CEQ + PSTK [PSTX unavailable in this extract],
--        else AT - LT)
--     + (TXDITC, else TXDB + ITCB, else 0)
--     - (PSTKR, else PSTK [PSTKRL unavailable in this extract], else 0)
--   * Earnings = IB; FCF = NI + DP - WCAPCH - CAPX (missing DP / WCAPCH /
--     CAPX treated as 0; NI required).
--   * GP/A requires AT > 0; earnings_be / fcf_be require BE != 0.
--   * datadate is a String in this extract -> cast to Date.
--   * All Compustat items are in $ millions (Compustat native units).
SELECT
    gvkey,
    -- datadate is a String; toDate32 (NOT toDate — `Date` clamps
    -- pre-1970 dates to 1970-01-01)
    toDate32(datadate)                          AS datadate,
    toYear(toDate32(datadate))                  AS calyear,
    fyear,
    sich,
    at,
    -- Gross profits: REVT - COGS, fallback to GP item
    if(revt IS NOT NULL AND cogs IS NOT NULL, revt - cogs, gp)
                                                AS gross_profit,
    if(at > 0,
       if(revt IS NOT NULL AND cogs IS NOT NULL, revt - cogs, gp) / at,
       NULL)                                    AS gp_a,
    -- Book equity tiers
    coalesce(seq, ceq + pstk, at - lt)          AS stockholders_equity,
    coalesce(txditc, txdb + itcb, 0)            AS deferred_taxes,
    coalesce(pstkr, pstk, 0)                    AS preferred_stock,
    coalesce(seq, ceq + pstk, at - lt)
        + coalesce(txditc, txdb + itcb, 0)
        - coalesce(pstkr, pstk, 0)              AS book_equity,
    -- Earnings-to-book: IB / BE
    if(coalesce(seq, ceq + pstk, at - lt)
         + coalesce(txditc, txdb + itcb, 0)
         - coalesce(pstkr, pstk, 0) != 0,
       ib / (coalesce(seq, ceq + pstk, at - lt)
             + coalesce(txditc, txdb + itcb, 0)
             - coalesce(pstkr, pstk, 0)),
       NULL)                                    AS earnings_be,
    -- Free-cash-flow-to-book: (NI + DP - WCAPCH - CAPX) / BE
    if(ni IS NOT NULL
       AND coalesce(seq, ceq + pstk, at - lt)
             + coalesce(txditc, txdb + itcb, 0)
             - coalesce(pstkr, pstk, 0) != 0,
       (ni + coalesce(dp, 0) - coalesce(wcapch, 0) - coalesce(capx, 0))
         / (coalesce(seq, ceq + pstk, at - lt)
            + coalesce(txditc, txdb + itcb, 0)
            - coalesce(pstkr, pstk, 0)),
       NULL)                                    AS fcf_be
FROM comp_202601.funda
WHERE indfmt = 'INDL'
  AND consol = 'C'
  AND popsrc = 'D'
  AND datafmt = 'STD'
  AND fyear BETWEEN 1962 AND 2010
  AND datadate IS NOT NULL
  AND at IS NOT NULL
  AND at > 0
  AND (sich IS NULL OR intDiv(sich, 1000) != 6)   -- exclude financials
SETTINGS max_execution_time = 300,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
