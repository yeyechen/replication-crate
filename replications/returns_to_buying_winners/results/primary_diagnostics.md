# Primary-portfolio diagnostics — PA 6/6 zero-cost strategy (RAW primary, 300 months, 1965-01..1989-12)

Generated: 2026-07-22T21:06:49. Persisted as diag_* keys in computed_values.json (audit-1 m2). The series is the Table I PA 6/6 buy-sell series (bit-identical to the All column of Tables IV/V/VI).

| diagnostic | value | REPORT.md §3 | within tol |
|------------|------:|-------------:|:----------:|
| Mean monthly return | 0.008797 | 0.008797 | True |
| t-stat (iid, n=300) | 2.9087 | 2.91 | True |
| Sharpe (annualized, sqrt(12)·mean/std) | 0.5817 | 0.58 | True |
| Total return ((prod(1+r)−1)×100) | 786.5% | 786.5% | True |
| Max drawdown | -60.2% | −60.2% | True |
| Arithmetic annualized (12·mean×100) | 10.56% | 10.56% | True |
| Geometric annualized ((prod(1+r))^(12/300)−1) | 9.12% | 9.12% | True |
| FF5 alpha (annualized) — RAW return on mkt_rf,smb,hml,rmw,cma (P18: rf NOT subtracted) | 14.50% | 14.50% | True |
| FF5 alpha t-stat | 3.88 | 3.88 | True |
| FF5 R² | 0.1582 | 0.16 | True |
| FF5 alpha rf-subtracted variant (documentation only): (zc − rf) on the 5 factors | 7.70% | 7.70% | True |

FF5 regression detail: n = 300; factors = mkt_rf, smb, hml, rmw, cma from ff.five_factor_monthly; rf-sub alpha t = 2.06; rf-sub R² = 0.1567.
