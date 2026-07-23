# Table 3 Panel A — TSMOM_ALL on MKT proxy + SMB + HML + UMD (4 regressors)

MKT = EW of the paper's 9 equity index futures (A2 proxy for MSCI World). Monthly OLS; quarterly = non-overlapping calendar-quarter compounded returns.

| metric | ours | paper | tol% | tier |
|---|---:|---:|---:|---|
| beta_msci_monthly | +0.032 | +0.090 | 200 | Tier 1 |
| beta_smb_monthly | +0.022 | -0.050 | 200 | FAIL |
| beta_hml_monthly | -0.140 | -0.010 | 200 | Tier 2 |
| beta_umd_monthly | +0.229 | +0.280 | 40 | Tier 1 |
| alpha_monthly | +1.198 | +1.580 | 50 | Tier 1 |
| r2_monthly | +0.116 | +0.140 | 25 | Tier 1 |
| t_beta_msci_monthly | +0.720 | +1.890 | 200 | Tier 1 |
| t_beta_smb_monthly | +0.341 | -0.840 | 200 | FAIL |
| t_beta_hml_monthly | -1.999 | -0.210 | 200 | Tier 2 |
| t_beta_umd_monthly | +5.394 | +6.780 | 40 | Tier 1 |
| t_alpha_monthly | +5.855 | +7.990 | 40 | Tier 1 |
| beta_msci_quarterly | +0.054 | +0.070 | 200 | Tier 1 |
| beta_smb_quarterly | +0.054 | -0.180 | 200 | FAIL |
| beta_hml_quarterly | -0.184 | +0.010 | 200 | FAIL |
| beta_umd_quarterly | +0.326 | +0.320 | 40 | Tier 1 |
| alpha_quarterly | +3.492 | +4.750 | 50 | Tier 1 |
| r2_quarterly | +0.204 | +0.230 | 25 | Tier 1 |
| t_beta_msci_quarterly | +0.723 | +1.000 | 200 | Tier 1 |
| t_beta_smb_quarterly | +0.383 | -1.440 | 200 | FAIL |
| t_beta_hml_quarterly | -1.790 | +0.110 | 200 | FAIL |
| t_beta_umd_quarterly | +4.150 | +4.440 | 40 | Tier 1 |
| t_alpha_quarterly | +5.219 | +7.730 | 40 | Tier 1 |

Monthly: n=300, R²=0.116 (paper 0.14); alpha +1.198%/mo (t 5.85, paper 1.58, t 7.99)
Quarterly: n=100, R²=0.204 (paper 0.23); alpha +3.492%/qtr (t 5.22, paper 4.75, t 7.73)
