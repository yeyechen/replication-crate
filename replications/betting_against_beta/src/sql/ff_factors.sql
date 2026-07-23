-- ff_factors.sql
-- Purpose: Fama-French 4-factor monthly returns + risk-free rate, for the
--          CAPM / FF3 / Carhart 4-factor alpha regressions in Table 3 and
--          for converting raw CRSP returns to excess returns (rf column).
-- Tables: ff.four_factor_monthly
-- Output columns: dt, mkt_rf, smb, hml, mom, rf
--   dt     : Nullable(String) month-end date 'YYYY-MM-DD' (parsed in Python)
--   mkt_rf : market excess return (VW CRSP - T-bill), DECIMAL (e.g. 0.03 = 3%)
--   smb    : small-minus-big, DECIMAL
--   hml    : high-minus-low book-to-market, DECIMAL
--   mom    : momentum (winners-minus-losers, UMD), DECIMAL (first non-null 1926-12)
--   rf     : one-month T-bill rate, DECIMAL (e.g. 0.0022 = 0.22%/mo)
-- Depends on: (none)
-- NOTE on units: this ClickHouse vintage stores the FF factors in DECIMAL, not
--   percent (verified: mkt_rf median |x| ~ 0.03, rf median ~ 0.0022). The
--   downstream code auto-detects the scale at runtime and converts if needed.
-- NOTE on dates: dt is a month-END string. We parse it to a first-of-month
--   Period in Python (robust to pre-1970 dates, unlike ClickHouse `Date`).
SELECT dt, mkt_rf, smb, hml, mom, rf
FROM ff.four_factor_monthly
WHERE dt IS NOT NULL
ORDER BY dt
SETTINGS max_execution_time = 120;
