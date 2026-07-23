-- panel.sql
-- Purpose: FINAL analysis-ready monthly international equity panel. Joins the
--          month-end price panel (ret_local, forward-filled cshoc, plus each
--          security's prior-month currency/month) to the USD conversion factors
--          and computes:
--            ret_usd(t) = (1 + ret_local(t))
--                         * usd_per_x(curcdd_t, t) / usd_per_x(curcdd_{t-1}, t-1) - 1
--            me_local   = prccd * cshoc          (cshoc forward-filled)
--            me_usd     = me_local * usd_per_x(curcdd_t, t)
--
--          The FX denominator uses the security's OWN prior-month currency
--          (curcdd_prev), NOT the same currency's lag. This is essential at
--          currency redenominations (the 1999 euro transition for 8 of the 13
--          countries): prccd redenominates (e.g. /6.55957 for FRF) while ajexdi
--          does not adjust, so ret_local carries a spurious drop; the FX ratio
--          usd_per_x(EUR,Jan99)/usd_per_x(FRF,Dec98) = conv-rate exactly cancels
--          it, leaving the true USD return. For stable currencies curcdd_prev =
--          curcdd and this reduces to the ordinary month-over-month FX change.
--
--          ret_usd is only defined when ret_local is defined (which already
--          guarantees month_prev is the immediately preceding calendar month and
--          curcdd_prev is that month's currency). USD fields are NULL when FX is
--          unavailable for the relevant currency/month — this only affects
--          1979-12..1982-01 (FX begins 1982-02) and minor-currency edge gaps.
--
-- Tables (scratch, materialized by main.py): write_yeye.hs_month_end,
--        write_yeye.hs_fx
-- Output columns (exactly the panel schema):
--   gvkey (String), country (String), curcdd (String), month (Date, last-day),
--   ret_local (Nullable Float64), ret_usd (Nullable Float64), me_usd (Nullable Float64)
-- Depends on: month_end_prices.sql -> write_yeye.hs_month_end ;
--             fx_gbp_cross.sql      -> write_yeye.hs_fx
-- Settings: join_algorithm=hash (small fx table on the right), join_use_nulls=1
--           (unmatched fx -> NULL, not 0), max_execution_time, max_rows_to_read.
SELECT
    p.gvkey     AS gvkey,
    p.country   AS country,
    p.curcdd    AS curcdd,
    p.month     AS month,
    p.ret_local AS ret_local,
    if(p.ret_local IS NOT NULL
       AND fx_t.usd_per_x    IS NOT NULL AND fx_t.usd_per_x    > 0
       AND fx_p.usd_per_x    IS NOT NULL AND fx_p.usd_per_x    > 0,
       (1 + p.ret_local) * (fx_t.usd_per_x / fx_p.usd_per_x) - 1,
       NULL) AS ret_usd,
    if(p.prccd IS NOT NULL AND p.cshoc IS NOT NULL AND p.cshoc > 0
       AND fx_t.usd_per_x IS NOT NULL AND fx_t.usd_per_x > 0,
       p.prccd * p.cshoc * fx_t.usd_per_x,
       NULL) AS me_usd
FROM write_yeye.hs_month_end AS p
LEFT JOIN write_yeye.hs_fx AS fx_t
  ON fx_t.cur = p.curcdd AND fx_t.month = p.month
LEFT JOIN write_yeye.hs_fx AS fx_p
  ON fx_p.cur = p.curcdd_prev AND fx_p.month = p.month_prev
SETTINGS join_algorithm = 'hash',
         join_use_nulls = 1,
         max_execution_time = 900,
         max_rows_to_read = 200000000,
         timeout_before_checking_execution_speed = 0
