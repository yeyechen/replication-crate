# Table 8 -- Decile-Rank Regression of Returns on BP, ME, V_f/P, PErr

**Replication of**: Frankel & Lee (1998) -- Table 8

**Sample period**: 1979-1991 (PErr-eligible window per paper §5.6: 1979-1992)

**Definitions**:
- **BP**, **ME**, **V_f/P** are decile-ranked 0-1 within each year_t.
- **PErr** = α̂ + β̂1 RK(SG_{t-4}) + β̂2 RK(BP_{t-4}) + β̂3 RK(OP_{t-4}) + β̂4 RK(Ltg_{t-4}), where the β̂'s come from annual OLS of FErr_{t-1} on RK(X_{t-4}); then PErr is decile-ranked 0-1.
- **Ret12** / **Ret36**: 1-year / 3-year buy-and-hold returns starting July of year_t.

## Panel A (1-yr BHAR)

DV: `ret12`

| Model | IVs | Coef name | Mean coef | NW t-stat (2 lags) | Paper value | Status |
| --- | --- | --- | ---: | ---: | ---: | --- |
| M1 | b_over_p_decile | intercept | +0.1455 | +3.16 | +0.1510 | Tier 1 (Δ=-0.0055) |
| M1 | b_over_p_decile | b_over_p_decile | -0.0075 | -0.17 | +0.0510 | FAIL (Δ=-0.0585) |
| M1 | b_over_p_decile | R² | +0.0162 | -- | -- | no target |
| M2 | me_june_t_decile | intercept | +0.0970 | +2.15 | -- | no target |
| M2 | me_june_t_decile | me_june_t_decile | +0.0621 | +1.55 | -- | no target |
| M2 | me_june_t_decile | R² | +0.0086 | -- | -- | no target |
| M3 | v_f_p_t3_decile | intercept | +0.1296 | +3.79 | -- | no target |
| M3 | v_f_p_t3_decile | v_f_p_t3_decile | +0.0203 | +0.55 | +0.0420 | Tier 2 (Δ=-0.0217) |
| M3 | v_f_p_t3_decile | R² | +0.0106 | -- | -- | no target |
| M4 | perr | intercept | +0.1080 | +3.28 | -- | no target |
| M4 | perr | perr | +0.0641 | +2.07 | -0.0400 | FAIL (Δ=+0.1041) |
| M4 | perr | R² | +0.0177 | -- | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | intercept | +0.0908 | +1.74 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | b_over_p_decile | +0.0091 | +0.23 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | me_june_t_decile | +0.0654 | +1.88 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | R² | +0.0236 | -- | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | intercept | +0.0831 | +1.68 | +0.1760 | FAIL (Δ=-0.0929) |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | b_over_p_decile | -0.0274 | -0.49 | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | me_june_t_decile | +0.0545 | +1.51 | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | v_f_p_t3_decile | +0.0030 | +0.06 | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | perr | +0.0673 | +1.86 | -0.0350 | FAIL (Δ=+0.1023) |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | R² | +0.0521 | -- | +0.1900 | Tier 2 (Δ=-0.1379) |

## Panel B (3-yr BHAR)

DV: `ret36`

| Model | IVs | Coef name | Mean coef | NW t-stat (2 lags) | Paper value | Status |
| --- | --- | --- | ---: | ---: | ---: | --- |
| M1 | b_over_p_decile | intercept | +0.4073 | +5.33 | +0.4680 | Tier 1 (Δ=-0.0607) |
| M1 | b_over_p_decile | b_over_p_decile | +0.0778 | +0.54 | +0.1680 | Tier 2 (Δ=-0.0902) |
| M1 | b_over_p_decile | R² | +0.0119 | -- | -- | no target |
| M2 | me_june_t_decile | intercept | +0.4637 | +2.49 | -- | no target |
| M2 | me_june_t_decile | me_june_t_decile | -0.0284 | -0.15 | -- | no target |
| M2 | me_june_t_decile | R² | +0.0137 | -- | -- | no target |
| M3 | v_f_p_t3_decile | intercept | +0.3855 | +4.11 | -- | no target |
| M3 | v_f_p_t3_decile | v_f_p_t3_decile | +0.1403 | +1.64 | +0.3700 | FAIL (Δ=-0.2297) |
| M3 | v_f_p_t3_decile | R² | +0.0063 | -- | -- | no target |
| M4 | perr | intercept | +0.4683 | +3.70 | -- | no target |
| M4 | perr | perr | -0.0360 | -0.27 | -0.2770 | FAIL (Δ=+0.2410) |
| M4 | perr | R² | +0.0072 | -- | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | intercept | +0.4282 | +3.03 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | b_over_p_decile | +0.0511 | +0.47 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | me_june_t_decile | -0.0161 | -0.09 | -- | no target |
| M5 | b_over_p_decile, me_june_t_decile | R² | +0.0216 | -- | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | intercept | +0.4133 | +2.74 | +0.5390 | Tier 2 (Δ=-0.1257) |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | b_over_p_decile | +0.0018 | +0.01 | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | me_june_t_decile | -0.0125 | -0.09 | -- | no target |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | v_f_p_t3_decile | +0.0883 | +0.89 | +0.3430 | FAIL (Δ=-0.2547) |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | perr | +0.0036 | +0.03 | -0.2410 | FAIL (Δ=+0.2446) |
| M6 | b_over_p_decile, me_june_t_decile, v_f_p_t3_decile, perr | R² | +0.0336 | -- | +2.4700 | Tier 2 (Δ=-2.4364) |

## Notes

**Decile scaling**: 10-bin breakpoints within each year_t, scaled to 0-1 = (decile-1)/9, so β = long-short spread.

**PErr construction**: per task spec, regress FErr_{t-1} on RK(X_{t-4}) annually (OLS). PErr_t = α̂ + β̂ × RK(X_{t-4}). Decile-rank the resulting PErr across firms.
