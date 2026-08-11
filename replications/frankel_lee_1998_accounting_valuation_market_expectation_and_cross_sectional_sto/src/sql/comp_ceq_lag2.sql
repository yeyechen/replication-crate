-- comp_ceq_lag2.sql
-- Purpose: For each (gvkey, fyear), return ceq from two fiscal years
--          prior (i.e., ceq for fyear-2). Used as B_{t-2} in the EBO
--          V_f computation (Appendix A Step 1: FROE_t = FY1 /
--          [(B_{t-1} + B_{t-2}) / 2]).
--
-- Output columns: gvkey, fyear, ceq_prior2 (B_{t-2})
-- Tables: comp_202601.funda
-- Depends on: (none)
-- Settings: max_execution_time=600

SELECT gvkey,
       fyear,
       ceq AS ceq_prior2
FROM comp_202601.funda
WHERE fyear BETWEEN 1974 AND 1990
  AND indfmt = 'INDL'
  AND consol = 'C'
  AND popsrc = 'D'
  AND datafmt = 'STD'
  AND ceq IS NOT NULL
  AND ceq > 0
SETTINGS max_execution_time = 600,
         max_rows_to_read = 10000000000,
         timeout_before_checking_execution_speed = 0
