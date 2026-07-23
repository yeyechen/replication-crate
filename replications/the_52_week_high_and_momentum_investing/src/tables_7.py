"""
George & Hwang (2004), "The 52-Week High and Momentum Investing", JF —
Table VII: Table V with the Grinblatt-Han (2002) embedded-capital-gain
winner/loser dummies added as explanatory variables.

"Table VII is identical to Table V, except that the GH winner and loser
dummies are added as explanatory variables." (L1327)

  R_{it}(%) = b0 + b1*R_{i,t-1} (decimal) + b2*ln(mcap_$ at t-1)
            + b3*JH + b4*JL + b5*MH + b6*ML
            + b7*GH + b8*GL + b9*FHH + b10*FHL + e

GH/GL at formation f: 30/30 ordinal rank of the cross-section with g_gh
NON-NULL (top 30% -> GH=1, bottom 30% -> GL=1). Stocks with g_gh null get
GH=GL=0 and STAY in the sample (same convention as the other strategies,
Assumption 13). g_gh is null for ~52% of stock-months (1970s turnover/vol
missingness), so early-sample GH dummies are sparse — expected; the avg
GH-rankable count per formation month by decade is reported in table_7.md.

Everything else is byte-for-byte the tables_5.py machinery (shared via
run_table): same t grid 1963-07..2001-12 (462), same j lags 2..7 (6,6) and
2..13 (6,12), same f = t-j, same 30/30 ordinal ranks, same sample rule,
same units, same j-averaging, same Jan incl/excl split, same FF3 risk
adjustment, same spread-from-difference-series t-stats.

Outputs:
  - results/intermediate/fm_coefficients_gh.parquet
                                     (extended c_{k,t} series, 11 coefs x 2 horizons;
                                      relocated out of data/ by audit1.md [M6])
  - results/table_7.md               (15 rows x 8 cols, 240 targets)
"""
from __future__ import annotations

import pandas as pd

from tables_5 import (CFG_V, COLS, LAYOUT, PRIMARY_WH, TableConfig,
                      intermediate_path, load_targets, run_table,
                      raw_mean_tstat, row_series)

# Table VII = Table V strategies + gh, with GH dummies inserted between MG and
# WH (regression order L1348-1349: JH JL MH ML GH GL FHH FHL).
STRAT_SIG_VII = {"jt": "jt_sig", "mg": "mg_sig", "gh": "g_gh", "wh": PRIMARY_WH}


def vii_preflight_gate(pf, pf_excl):
    """Stop-and-diagnose gate (task pre-flight spec). Checks the s66_raw
    Jan-incl sign pattern of the GH dummies and the wh_spread direction
    relative to Table V's ours (0.49 -> ~0.51 upward)."""
    problems = []
    gh_w, _ = pf["gh_winner"]
    gh_l, _ = pf["gh_loser"]
    whs, _ = pf["wh_spread"]
    # paper Jan-incl: gh_winner +0.13 AND gh_loser +0.10 (both positive)
    if not (gh_w > 0):
        problems.append(f"gh_winner {gh_w:.4f} <= 0 (paper janincl: +0.13)")
    if not (gh_l > 0):
        problems.append(f"gh_loser {gh_l:.4f} <= 0 (paper janincl: +0.10; "
                        f"both GH dummies are positive Jan-incl, "
                        f"gh_loser is -0.19 only ex-Jan)")
    if not (whs > 0.45):
        problems.append(f"wh_spread {whs:.4f} collapsed/flipped vs paper 0.51")
    # direction check vs Table V ours (fm_coefficients.parquet s66_wh_spread)
    try:
        t5 = pd.read_parquet(intermediate_path(CFG_V.coeff_parquet))
        v5 = float(t5["s66_wh_spread"].dropna().mean())
        if whs < v5 - 1e-4:
            problems.append(f"wh_spread moved DOWN vs Table V ({whs:.4f} < "
                            f"{v5:.4f}); expected the 0.49 -> ~0.51 upward "
                            f"direction, not a flip")
    except FileNotFoundError:
        pass  # Table V artifact absent; direction check skipped
    return problems


CFG_VII = TableConfig(
    table_id="T7",
    strat_sig=STRAT_SIG_VII,
    coeff_parquet="fm_coefficients_gh.parquet",
    md_name="table_7.md",
    title=("# Table VII — George & Hwang (2004): Table V + Grinblatt-Han "
           "embedded-capital-gain dummies"),
    dummy_pairs="JH/JL<-jt_sig, MH/ML<-mg_sig, GH/GL<-g_gh, FHH/FHL<-wh_sig_dc",
    preflight_rows=("intercept", "r_lag1", "size",
                    "gh_winner", "gh_loser", "wh_spread"),
    paper_preflight={"intercept": 3.27, "r_lag1": -7.06, "size": -0.17,
                     "gh_winner": 0.13, "gh_loser": 0.10, "wh_spread": 0.51},
    preflight_gate=vii_preflight_gate,
)


def main() -> None:
    bundle = run_table(CFG_VII)

    # --- qualitative claim checks (paper's key Table VII narrative) -----------
    results = bundle["results"]

    def val(col, row):
        return results[(col, row, "val")][0]

    print()
    print("QUALITATIVE CLAIM CHECKS")
    # ex-January raw s66: wh 0.75 > gh 0.44 > jt 0.29 / mg 0.16
    col = "s66_raw_janexcl"
    wh, gh, jt, mg = (val(col, f"{s}_spread") for s in ("wh", "gh", "jt", "mg"))
    print(f"  s66_raw_janexcl spreads: wh {wh:.4f} > gh {gh:.4f} > "
          f"jt {jt:.4f} / mg {mg:.4f}  "
          f"(paper 0.75 > 0.44 > 0.29 / 0.16)")
    print(f"  wh > gh: {wh > gh} | gh > jt: {gh > jt} | gh > mg: {gh > mg}")
    # gh spread insignificant Jan-incl (paper t 0.27)
    gh_t_incl = results[("s66_raw_janincl", "gh_spread", "tstat")][0]
    gh_v_incl = val("s66_raw_janincl", "gh_spread")
    print(f"  s66_raw_janincl gh_spread: {gh_v_incl:.4f} (t {gh_t_incl:.2f}) — "
          f"insignificant? {abs(gh_t_incl) < 1.96} (paper 0.03, t 0.27)")

    # --- the 16 spread-cell grid (4 strategies x 4 column-groups, x2 Jan) ------
    print()
    print("SPREAD CELL GRID (ours vs paper)")
    groups = [("s66 raw", ("s66_raw_janincl", "s66_raw_janexcl")),
              ("s66 RA", ("s66_ra_janincl", "s66_ra_janexcl")),
              ("s612 raw", ("s612_raw_janincl", "s612_raw_janexcl")),
              ("s612 RA", ("s612_ra_janincl", "s612_ra_janexcl"))]
    for s in ("wh", "jt", "mg", "gh"):
        for gname, (ci, ce) in groups:
            vi, pi, _, tri = results[(ci, f"{s}_spread", "val")]
            ve, pe, _, tre = results[(ce, f"{s}_spread", "val")]
            print(f"  {s}_spread {gname:8s}  janincl {vi:7.4f} (paper {pi:6.2f}, "
                  f"{tri}) | janexcl {ve:7.4f} (paper {pe:6.2f}, {tre})")


if __name__ == "__main__":
    main()
