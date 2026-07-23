"""
Diagnostic Task B: Newey-West lag sweep for the Table 3 annual
market-column regression (model 10), 1964-1996 (T = 33).

Re-estimates with statsmodels HAC at maxlags = 0..6; reports g1/g2
OLS t and NW t at each lag vs the paper (g1: OLS 2.68, NW 2.74;
g2: OLS -4.52, NW -4.11). Winner = lag minimizing the sum of
absolute %-deviations of |g1_t_nw| vs 2.74 and |g2_t_nw| vs 4.11.

Prints the full sweep + winner. Does NOT modify results/ or main.py;
the worker applies the winner (if != current 3) afterwards.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC))
import main as M  # noqa: E402

PAPER = {"g1_ols": 2.68, "g1_nw": 2.74, "g2_ols": -4.52, "g2_nw": -4.11}


def main() -> None:
    print("=== Task B: NW lag sweep (Table 3, market column) ===")
    d = M._load_ts_inputs()
    ln_a = d["ln_a"]

    # --- identical to main.build_table_3 ---
    ar = M.ar1_kendall(ln_a.to_numpy())
    yrs = pd.Index(range(1964, 1997), name="year")
    u_a = pd.Series(ar["u"], index=yrs, name="u_a")
    ln_lag = pd.Series(ln_a.to_numpy()[:-1], index=yrs,
                       name="ln_ailliq_lag")

    frame = pd.DataFrame({"rf": d["rf"], "rm_nyse": d["mkt"]["rm_ew_nyse"]})
    for i in (2, 4, 6, 8, 10):
        frame[f"rsz{i}"] = d["rsz"][f"decret{i}"]
    frame = frame.dropna()
    prod_cols = ["rm_nyse", "rf"]
    ann = {}
    for y, g in frame.groupby(frame.index.year):
        ann[int(y)] = {c: float((1.0 + g[c]).prod()) for c in prod_cols}
    ann = pd.DataFrame(ann).T.sort_index()
    dep = pd.DataFrame(index=yrs)
    dep["rm_nyse"] = 100.0 * (ann.loc[1964:1996, "rm_nyse"].to_numpy()
                              - ann.loc[1964:1996, "rf"].to_numpy())

    reg = pd.concat([dep[["rm_nyse"]].rename(columns={"rm_nyse": "y"}),
                     ln_lag, u_a], axis=1).dropna()
    X = sm.add_constant(reg[["ln_ailliq_lag", "u_a"]].to_numpy())
    yv = reg["y"].to_numpy()
    ols = sm.OLS(yv, X).fit()
    t_ols = np.asarray(ols.tvalues, dtype=float)

    print(f"\nT = {int(ols.nobs)}; g1 OLS t = {t_ols[1]:+.3f} (paper 2.68, "
          f"|dev| {abs(abs(t_ols[1]) - 2.68) / 2.68 * 100:.1f}%); "
          f"g2 OLS t = {t_ols[2]:+.3f} (paper -4.52, "
          f"|dev| {abs(abs(t_ols[2]) - 4.52) / 4.52 * 100:.1f}%)")

    print(f"\n{'maxlags':>7} | {'g1 NW t':>9} {'g1 |%dev|':>10} | "
          f"{'g2 NW t':>9} {'g2 |%dev|':>10} | {'score':>8}")
    rows = []
    for lag in range(0, 7):
        nw = sm.OLS(yv, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
        t_nw = np.asarray(nw.tvalues, dtype=float)
        d1 = abs(abs(t_nw[1]) - abs(PAPER["g1_nw"])) / abs(PAPER["g1_nw"]) * 100
        d2 = abs(abs(t_nw[2]) - abs(PAPER["g2_nw"])) / abs(PAPER["g2_nw"]) * 100
        score = d1 / 100.0 + d2 / 100.0
        rows.append({"lag": lag, "g1_t_nw": float(t_nw[1]),
                     "g2_t_nw": float(t_nw[2]),
                     "g1_pctdev": float(d1), "g2_pctdev": float(d2),
                     "score": float(score)})
        print(f"{lag:>7} | {t_nw[1]:>+9.3f} {d1:>9.1f}% | "
              f"{t_nw[2]:>+9.3f} {d2:>9.1f}% | {score:>8.4f}")

    winner = min(rows, key=lambda r: r["score"])
    print(f"\nWINNER: maxlags = {winner['lag']} "
          f"(score {winner['score']:.4f}; g1 NW t {winner['g1_t_nw']:+.3f}, "
          f"g2 NW t {winner['g2_t_nw']:+.3f}); current build_table_3 uses 3.")
    print(f"{'UPDATE build_table_3' if winner['lag'] != 3 else 'KEEP maxlags = 3'}")

    out = M.CACHE_DIR / "diag_nw_sweep.json"
    out.write_text(json.dumps({"rows": rows,
                               "winner_lag": winner["lag"],
                               "t_ols_g1": float(t_ols[1]),
                               "t_ols_g2": float(t_ols[2])}, indent=2))
    print(f"summary -> {out}")


if __name__ == "__main__":
    main()
