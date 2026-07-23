"""
Diagnostic Task A: MILLIQ over the OPEN universe (all NYSE common
stocks trading each day — no admission filters, no tail exclusions)
vs the current admitted-sample MILLIQ.

Steps:
  1. Compute/cache MILLIQ_open_m 1963-01..1996-12 via
     src/sql/milliq_open_monthly.sql (x1e6).
  2. AR(1) of ln MILLIQ_open, 1963-02..1996-12 (T=407): c0, c1,
     t-stats, R2, DW; Kendall correction; u_open_m residuals
     (first at 1963-02; regression window 1964-01..1996-12).
  3. Re-estimate model (10m) with MILLIQ_open for market + RSZ
     2/4/6/8/10 (percent excess returns; OLS t + White HC0 t; R2; DW)
     — identical machinery to main.build_table_4.
  4. Side-by-side table (admitted vs open vs paper) + corr(u, market
     excess) + Tier counts (91-cell T4 evaluation) under each variant.
  5. Mechanical adoption rules (a)-(d) — reported only; canonical
     artifact regeneration is done by the worker after inspection.

Outputs: prints the full report; saves data/_cache/diag_milliq_open.json.
Does NOT modify data/milliq.parquet, results/, or src/main.py.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_SRC = Path(__file__).resolve().parent
sys.path.insert(0, str(_SRC))
import main as M  # noqa: E402  (canonical pipeline module; __main__-guarded)


def load_milliq_open() -> pd.DataFrame:
    def build():
        df = M.q_file("milliq_open_monthly.sql")
        for c in ["milliq", "n_days", "n_stocks"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return M._to_month_end(df).sort_values("month").reset_index(drop=True)
    return M.cached("milliq_open_monthly.parquet", build)


def estimate_10m(ln_m: pd.Series, d: dict) -> dict:
    """Replicates main.build_table_4 estimation for an arbitrary
    ln-MILLIQ monthly series (408 months 1963-01..1996-12)."""
    ar = M.ar1_kendall(ln_m.to_numpy())
    u_m = pd.Series(ar["u"], index=ln_m.index[1:], name="u_m")
    ln_lag = ln_m.shift(1).rename("ln_milliq_lag")

    frame = pd.DataFrame({"rf": d["rf"], "rm_nyse": d["mkt"]["rm_ew_nyse"]})
    for i in (2, 4, 6, 8, 10):
        frame[f"rsz{i}"] = d["rsz"][f"decret{i}"]
    frame = frame.dropna()
    frame = frame[(frame.index >= pd.Period("1964-01", "M"))
                  & (frame.index <= pd.Period("1996-12", "M"))]

    import statsmodels.api as sm
    from statsmodels.stats.stattools import durbin_watson

    est = {}
    for col in M.TS_COLS:
        ysrc = M.TS_DEP_SRC[col]
        dep = 100.0 * (frame[ysrc] - frame["rf"])
        reg = pd.concat([dep.rename("y"), ln_lag, u_m], axis=1)
        reg["jandum"] = (reg.index.month == 1).astype(float)
        reg = reg.dropna()
        X = sm.add_constant(reg[["ln_milliq_lag", "u_m", "jandum"]].to_numpy())
        yv = reg["y"].to_numpy()
        ols = sm.OLS(yv, X).fit()
        wh = sm.OLS(yv, X).fit(cov_type="HC0")
        est[col] = {"coef": np.asarray(ols.params, dtype=float),
                    "t_ols": np.asarray(ols.tvalues, dtype=float),
                    "t_w": np.asarray(wh.tvalues, dtype=float),
                    "r2": float(ols.rsquared),
                    "dw": float(durbin_watson(ols.resid)),
                    "n": int(ols.nobs)}
    # corr(u^M, market excess return), 1964-01..1996-12 (scale-invariant)
    mkt_excess = frame["rm_nyse"] - frame["rf"]
    corr_u_mkt = float(np.corrcoef(u_m.reindex(mkt_excess.index).to_numpy(),
                                   mkt_excess.to_numpy())[0, 1])
    return {"ar": ar, "est": est, "corr_u_mkt": corr_u_mkt, "u_m": u_m}


def evaluate_t4(ar: dict, est: dict) -> dict:
    """Replicates main.build_table_4 91-cell evaluation (7 AR cells
    with the 2 A11 forced-FAIL intercept cells + 84 regression cells)."""
    paper = M._load_ts_paper("T4")
    force_fail = {"ar1_monthly_c0", "ar1_monthly_c0_t"}
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0}
    per_cell = {}

    def ev(name, ours, is_t):
        pv, tol = paper[name]
        o, dev, st = M.cell_eval(ours, pv, tol, is_tstat=is_t)
        if name in force_fail:
            st = "FAIL"
        counts[st] += 1
        per_cell[name] = (float(ours), pv, dev, st)

    for name, ours, is_t in (
            ("ar1_monthly_c0", ar["c0"], False),
            ("ar1_monthly_c0_t", ar["t_c0"], True),
            ("ar1_monthly_c1", ar["c1"], False),
            ("ar1_monthly_c1_t", ar["t_c1"], True),
            ("ar1_monthly_r2", ar["r2"], False),
            ("ar1_monthly_dw", ar["dw"], False),
            ("ar1_monthly_c1_kendall", ar["c1_adj"], False)):
        ev(name, ours, is_t)
    for col in M.TS_COLS:
        e = est[col]
        for k in (0, 1, 2, 3):
            ev(f"g{k}_{col}", e["coef"][k], False)
            ev(f"g{k}_{col}_t_ols", e["t_ols"][k], True)
            ev(f"g{k}_{col}_t_white", e["t_w"][k], True)
        ev(f"r2_{col}", e["r2"], False)
        ev(f"dw_{col}", e["dw"], False)
    assert sum(counts.values()) == 91
    return {"counts": counts, "per_cell": per_cell}


def fmt_row(label: str, vals: list) -> str:
    return "| " + label + " | " + " | ".join(vals) + " |"


def main() -> None:
    print("=== Task A: MILLIQ_open diagnostic ===")

    # --- open series ---
    opq = load_milliq_open()
    print(f"\n[1] MILLIQ_open: {len(opq)} months "
          f"({opq['month'].min()}..{opq['month'].max()})")
    print(f"    milliq (x1e6): mean={opq['milliq'].mean():.4f}, "
          f"min={opq['milliq'].min():.4f}, max={opq['milliq'].max():.4f}")
    print(f"    n_days: mean={opq['n_days'].mean():.1f}; "
          f"n_stocks: mean={opq['n_stocks'].mean():.0f}, "
          f"min={opq['n_stocks'].min()}, max={opq['n_stocks'].max()}")

    admq = pd.read_parquet(M.LAYOUT.data_path("milliq.parquet"))
    print(f"    MILLIQ_admitted (current): mean={admq['milliq'].mean():.4f}, "
          f"n_stocks mean={admq['n_stocks'].mean():.0f} "
          f"(open universe is {opq['n_stocks'].mean() / admq['n_stocks'].mean():.2f}x "
          f"the admitted count)")

    ln_open = pd.Series(np.log(opq["milliq"].astype(float)).to_numpy(),
                        index=pd.to_datetime(opq["month"]).dt.to_period("M"),
                        name="ln_milliq_open").sort_index()
    ln_adm = pd.Series(np.log(admq["milliq"].astype(float)).to_numpy(),
                       index=pd.to_datetime(admq["month"]).dt.to_period("M"),
                       name="ln_milliq_adm").sort_index()

    d = M._load_ts_inputs()

    res_open = estimate_10m(ln_open, d)
    res_adm = estimate_10m(ln_adm, d)
    ar_o, ar_a = res_open["ar"], res_adm["ar"]

    # --- AR(1) comparison ---
    print("\n[2] AR(1) of ln MILLIQ, 1963-02..1996-12 (T = 407)")
    hdr = f"{'variant':<10} {'c0':>8} {'c1':>7} {'t_c0':>7} {'t_c1':>8} " \
          f"{'R2':>7} {'DW':>7} {'c1_adj':>8}"
    print(hdr)
    for lab, ar in (("paper", None), ("admitted", ar_a), ("open", ar_o)):
        if ar is None:
            print(f"{'paper':<10} {'0.313':>8} {'0.945':>7} {'3.31':>7} "
                  f"{'58.36':>8} {'0.89':>7} {'2.34':>7} {'0.954':>8}")
        else:
            print(f"{lab:<10} {ar['c0']:>8.3f} {ar['c1']:>7.3f} "
                  f"{ar['t_c0']:>7.2f} {ar['t_c1']:>8.2f} {ar['r2']:>7.3f} "
                  f"{ar['dw']:>7.3f} {ar['c1_adj']:>8.3f}")

    # --- side-by-side 10m table ---
    paper = M._load_ts_paper("T4")
    print("\n[3] Model (10m) side-by-side: admitted | open | paper")
    labels = [("g0", 0, "coef"), ("g0 OLS t", 0, "t_ols"),
              ("g0 White t", 0, "t_w"),
              ("g1", 1, "coef"), ("g1 OLS t", 1, "t_ols"),
              ("g1 White t", 1, "t_w"),
              ("g2", 2, "coef"), ("g2 OLS t", 2, "t_ols"),
              ("g2 White t", 2, "t_w"),
              ("g3", 3, "coef"), ("g3 OLS t", 3, "t_ols"),
              ("g3 White t", 3, "t_w")]
    for col in M.TS_COLS:
        ea, eo = res_adm["est"][col], res_open["est"][col]
        print(f"\n  --- {M.TS_COL_LABEL[col]} ---")
        print(f"  {'row':<10} | {'admitted':>26} | {'open':>26} | {'paper':>14}")
        for lab, k, kind in labels:
            va, vo = ea[kind][k], eo[kind][k]
            pkey = f"g{k}_{col}" + ("" if kind == "coef"
                                    else f"_t_{('ols' if kind == 't_ols' else 'white')}")
            pv = paper[pkey][0]
            print(f"  {lab:<10} | {va:>26.4f} | {vo:>26.4f} | {pv:>14.3f}")
        print(f"  {'R2':<10} | {ea['r2']:>26.4f} | {eo['r2']:>26.4f} | "
              f"{paper[f'r2_{col}'][0]:>14.3f}")
        print(f"  {'DW':<10} | {ea['dw']:>26.4f} | {eo['dw']:>26.4f} | "
              f"{paper[f'dw_{col}'][0]:>14.3f}")

    print(f"\n  corr(u^M, market excess): admitted = "
          f"{res_adm['corr_u_mkt']:.4f}; open = {res_open['corr_u_mkt']:.4f}")

    # --- Tier counts ---
    ev_a = evaluate_t4(ar_a, res_adm["est"])
    ev_o = evaluate_t4(ar_o, res_open["est"])
    print("\n[4] Tier counts (91-cell T4 evaluation, incl. 2 A11 forced FAILs)")
    for lab, ev in (("admitted", ev_a), ("open", ev_o)):
        c = ev["counts"]
        print(f"    {lab:<10} Tier 1 = {c['Tier 1']:>3}, "
              f"Tier 2 = {c['Tier 2']:>3}, FAIL = {c['FAIL']:>3}")

    # --- adoption rules ---
    g2_mkt = float(res_open["est"]["market"]["coef"][2])
    rule_a = -7.73 <= g2_mkt <= -3.31
    g2_neg_all = all(res_open["est"][c]["coef"][2] < 0 for c in M.TS_COLS)
    g1_pos_all = all(res_open["est"][c]["coef"][1] > 0 for c in M.TS_COLS)
    rule_b = bool(g2_neg_all and g1_pos_all)
    rule_c = ev_o["counts"]["Tier 1"] > ev_a["counts"]["Tier 1"]
    c1_lo, c1_hi = 0.945 * 0.6, 0.945 * 1.4
    rule_d = bool(c1_lo <= ar_o["c1"] <= c1_hi)
    adopt = bool(rule_a and rule_b and rule_c and rule_d)

    print("\n[5] ADOPTION RULES")
    print(f"    (a) g2(market) open = {g2_mkt:.3f} in [-7.73, -3.31] "
          f"(paper -5.520, +/-40%): {'PASS' if rule_a else 'FAIL'}")
    g2seq = ", ".join(f"{c} {res_open['est'][c]['coef'][2]:.3f}"
                      for c in M.TS_COLS)
    g1seq = ", ".join(f"{c} {res_open['est'][c]['coef'][1]:.3f}"
                      for c in M.TS_COLS)
    print(f"        g2 all 6 < 0: {g2_neg_all} [{g2seq}]")
    print(f"        g1 all 6 > 0: {g1_pos_all} [{g1seq}]")
    print(f"    (b) g2<0 in all 6 AND g1>0 in all 6: "
          f"{'PASS' if rule_b else 'FAIL'}")
    print(f"    (c) Tier-1 total: open {ev_o['counts']['Tier 1']} vs "
          f"admitted {ev_a['counts']['Tier 1']} "
          f"(open > admitted): {'PASS' if rule_c else 'FAIL'}")
    print(f"    (d) monthly AR(1) slope open = {ar_o['c1']:.4f} within "
          f"+/-40% of 0.945 ([{c1_lo:.3f}, {c1_hi:.3f}]): "
          f"{'PASS' if rule_d else 'FAIL'}")
    print(f"\n    DECISION: {'ADOPT the open universe' if adopt else 'KEEP admitted universe'}")

    # --- per-cell status changes (open vs admitted) ---
    print("\n[6] Cell-level status changes (open vs admitted):")
    for name in sorted(set(ev_a["per_cell"]) | set(ev_o["per_cell"])):
        sa = ev_a["per_cell"].get(name, (None,) * 4)[3]
        so = ev_o["per_cell"].get(name, (None,) * 4)[3]
        if sa != so:
            oa = ev_a["per_cell"].get(name, (float("nan"),) * 4)[0]
            oo = ev_o["per_cell"].get(name, (float("nan"),) * 4)[0]
            print(f"    {name:<28} {sa} -> {so}  "
                  f"(admitted {oa:.4f}, open {oo:.4f})")

    # --- persist summary ---
    summary = {
        "ar_open": {k: ar_o[k] for k in
                    ["c0", "c1", "t_c0", "t_c1", "r2", "dw", "n",
                     "c1_adj", "c0_adj"]},
        "ar_admitted": {k: ar_a[k] for k in
                        ["c0", "c1", "t_c0", "t_c1", "r2", "dw", "n",
                         "c1_adj", "c0_adj"]},
        "corr_u_mkt": {"admitted": res_adm["corr_u_mkt"],
                       "open": res_open["corr_u_mkt"]},
        "counts": {"admitted": ev_a["counts"], "open": ev_o["counts"]},
        "est_open": {c: {"coef": res_open["est"][c]["coef"].tolist(),
                         "t_ols": res_open["est"][c]["t_ols"].tolist(),
                         "t_w": res_open["est"][c]["t_w"].tolist(),
                         "r2": res_open["est"][c]["r2"],
                         "dw": res_open["est"][c]["dw"],
                         "n": res_open["est"][c]["n"]}
                     for c in M.TS_COLS},
        "est_admitted": {c: {"coef": res_adm["est"][c]["coef"].tolist(),
                             "t_ols": res_adm["est"][c]["t_ols"].tolist(),
                             "t_w": res_adm["est"][c]["t_w"].tolist(),
                             "r2": res_adm["est"][c]["r2"],
                             "dw": res_adm["est"][c]["dw"],
                             "n": res_adm["est"][c]["n"]}
                         for c in M.TS_COLS},
        "rules": {"a": rule_a, "b": rule_b, "c": rule_c, "d": rule_d,
                  "adopt": adopt, "g2_market_open": g2_mkt},
        "n_stocks": {"open_mean": float(opq["n_stocks"].mean()),
                     "admitted_mean": float(admq["n_stocks"].mean())},
    }
    out = M.CACHE_DIR / "diag_milliq_open.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"\n[7] summary -> {out}")


if __name__ == "__main__":
    main()
