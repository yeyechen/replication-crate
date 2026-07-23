"""
Inner iteration 4 — strict per-metric recount + Tables 3/4/5 + figures.

1. Re-tally every T1/T2 cell against its OWN committed tolerance_pct from
   preparations/tables_to_replicate.json (T1: means 15%, vols 10%; T2: 40%
   for |paper t| >= 2, 200% for |t| < 2 noise cells). Rewrite eval_t1.csv /
   eval_t2.csv with the tolerance_pct column used per cell.
2. Table 3 Panel A: TSMOM_ALL on MKT proxy + SMB + HML + UMD (4 regressors),
   monthly (OLS) + non-overlapping quarterly (compounded), 22 cells.
3. Table 4: within-class avg pairwise instrument correlations (TSMOM and
   passive) + across-class correlations of the four EW class factors, 20 cells.
4. Table 5 Panel C: XSMOM per A11 (12-month formation skipping the most recent
   month; rank-median weights; 40%/sigma scaling); regress XSMOM_{ALL,COM,EQ,
   FI,FX}, UMD, HML, SMB on TSMOM_ALL, 40 cells.
5. Figures: Fig. 3 analog (cumulative log), Fig. 2 analog (Sharpe bars by
   class), Fig. 4 analog (TSMOM smile vs SP500 quarterly).
"""

from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SRC_DIR.parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("time_series_momentum")
EVAL_START = pd.Timestamp("1985-01-31")
EVAL_END = pd.Timestamp("2009-12-31")
CLASS_OF_COL = {"COM": "commodity", "EQ": "equity", "FI": "bond", "FX": "currency"}


def tier(ours: float, paper: float, tol_pct: float) -> str:
    if ours is None or paper is None or (isinstance(ours, float) and math.isnan(ours)):
        return "SKIP"
    if paper == 0:
        return "Tier 1" if ours == 0 else "Tier 2"
    if ours != 0 and (paper > 0) != (ours > 0):
        return "FAIL"
    if abs(ours - paper) / abs(paper) <= tol_pct / 100.0:
        return "Tier 1"
    return "Tier 2"


def ols_fit(y: pd.Series, X: pd.DataFrame):
    from statsmodels.regression.linear_model import OLS
    from statsmodels.tools import add_constant
    d = pd.concat([y.rename("y"), X], axis=1).dropna()
    res = OLS(d["y"].to_numpy(), add_constant(d[X.columns].to_numpy())).fit()
    return res, d


def main() -> None:
    rules = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    T = {t["id"]: {m["name"]: m for m in t["metrics"]} for t in rules["tables"]}

    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    art = pd.read_parquet(LAYOUT.data_path("strategy_artifacts.parquet"))
    art.index = pd.to_datetime(art.index)
    cls = panel.drop_duplicates("instrument").set_index("instrument")["asset_class"]

    # FF factors (decimals, A7)
    from clickhouse_driver import Client
    from utils.env import get_clickhouse_config
    cfg = get_clickhouse_config()
    cli = Client(host=os.getenv("CLICKHOUSE_HOST", cfg["host"]),
                 port=int(os.getenv("CLICKHOUSE_PORT", cfg["port"])),
                 user=os.getenv("CLICKHOUSE_USER", cfg["user"]),
                 password=os.getenv("CLICKHOUSE_PASSWORD", cfg["password"]),
                 settings={"max_execution_time": 60})
    rows, cols = cli.execute(
        "SELECT dt, smb, hml, mom FROM ff.four_factor_monthly "
        "WHERE dt >= '1983-01-01' AND dt <= '2009-12-31'", with_column_types=True)
    ff = pd.DataFrame(rows, columns=[c[0] for c in cols])
    ff["month"] = pd.to_datetime(ff["dt"])
    ff = ff.set_index("month")[["smb", "hml", "mom"]].astype(float)
    ff.columns = ["SMB", "HML", "UMD"]

    # ============ 1. STRICT RECOUNT (per-metric committed tolerances) ============
    for tid, csv_name, extra_cols in [("T1", "eval_t1.csv", ["instrument", "stat"]),
                                      ("T2", "eval_t2.csv", ["panel", "k", "h"])]:
        df = pd.read_csv(LAYOUT.result_path(csv_name))
        tols, tiers = [], []
        for _, r in df.iterrows():
            m = T[tid][r["cell"]]
            tols.append(m["tolerance_pct"])
            tiers.append(tier(r["ours"], r["paper"], m["tolerance_pct"]))
        df["tolerance_pct"] = tols
        df["tier"] = tiers
        df.to_csv(LAYOUT.result_path(csv_name), index=False)
    t1 = pd.read_csv(LAYOUT.result_path("eval_t1.csv"))
    t2 = pd.read_csv(LAYOUT.result_path("eval_t2.csv"))
    print("STRICT RECOUNT (per-metric committed tolerances):")
    print("T1:", t1.groupby(["stat", "tier"]).size().unstack(fill_value=0).to_dict())
    print("T2:", t2.groupby(["panel", "tier"]).size().unstack(fill_value=0).to_dict())

    # ============ 2. TABLE 3 Panel A (4 regressors: MKT proxy + SMB/HML/UMD) ============
    y = art["TSMOM_ALL"]
    X3 = pd.DataFrame({"MKT": art["MKT"], "SMB": ff["SMB"], "HML": ff["HML"], "UMD": ff["UMD"]})
    res_m, d_m = ols_fit(y, X3)
    names = ["const", "MKT", "SMB", "HML", "UMD"]
    pm, pm_t = dict(zip(names, res_m.params)), dict(zip(names, res_m.tvalues))
    # quarterly non-overlapping
    qtr = lambda s: s.groupby([s.index.year, s.index.quarter]).apply(lambda g: (1 + g).prod() - 1)
    yq = qtr(y)
    Xq = pd.DataFrame({c: qtr(X3[c]) for c in X3.columns})
    res_q, d_q = ols_fit(yq, Xq)
    pq, pq_t = dict(zip(names, res_q.params)), dict(zip(names, res_q.tvalues))

    t3 = {"beta_msci_monthly": pm["MKT"], "beta_smb_monthly": pm["SMB"],
          "beta_hml_monthly": pm["HML"], "beta_umd_monthly": pm["UMD"],
          "alpha_monthly": pm["const"] * 100, "r2_monthly": res_m.rsquared,
          "t_beta_msci_monthly": pm_t["MKT"], "t_beta_smb_monthly": pm_t["SMB"],
          "t_beta_hml_monthly": pm_t["HML"], "t_beta_umd_monthly": pm_t["UMD"],
          "t_alpha_monthly": pm_t["const"],
          "beta_msci_quarterly": pq["MKT"], "beta_smb_quarterly": pq["SMB"],
          "beta_hml_quarterly": pq["HML"], "beta_umd_quarterly": pq["UMD"],
          "alpha_quarterly": pq["const"] * 100, "r2_quarterly": res_q.rsquared,
          "t_beta_msci_quarterly": pq_t["MKT"], "t_beta_smb_quarterly": pq_t["SMB"],
          "t_beta_hml_quarterly": pq_t["HML"], "t_beta_umd_quarterly": pq_t["UMD"],
          "t_alpha_quarterly": pq_t["const"]}
    rows3 = []
    for n, m in T["T3"].items():
        rows3.append({"cell": n, "paper": m["value"], "ours": t3[n],
                      "tolerance_pct": m["tolerance_pct"],
                      "tier": tier(t3[n], m["value"], m["tolerance_pct"])})
    t3_df = pd.DataFrame(rows3)
    t3_df.to_csv(LAYOUT.result_path("eval_t3.csv"), index=False)
    md3 = ["# Table 3 Panel A — TSMOM_ALL on MKT proxy + SMB + HML + UMD (4 regressors)",
           "", "MKT = EW of the paper's 9 equity index futures (A2 proxy for MSCI World). "
           "Monthly OLS; quarterly = non-overlapping calendar-quarter compounded returns.",
           "", "| metric | ours | paper | tol% | tier |", "|---|---:|---:|---:|---|"]
    for r in rows3:
        md3.append(f"| {r['cell']} | {r['ours']:+.3f} | {r['paper']:+.3f} | {r['tolerance_pct']} | {r['tier']} |")
    md3 += ["", f"Monthly: n={len(d_m)}, R²={res_m.rsquared:.3f} (paper 0.14); "
            f"alpha {pm['const']*100:+.3f}%/mo (t {pm_t['const']:.2f}, paper 1.58, t 7.99)",
            f"Quarterly: n={len(d_q)}, R²={res_q.rsquared:.3f} (paper 0.23); "
            f"alpha {pq['const']*100:+.3f}%/qtr (t {pq_t['const']:.2f}, paper 4.75, t 7.73)"]
    (LAYOUT.result_path("table_3.md")).write_text("\n".join(md3) + "\n")

    # ============ 3. TABLE 4 (correlations) ============
    tsmom_cols = {c: c.replace("tsmom_", "") for c in art.columns if c.startswith("tsmom_")}
    pass_cols = {c: c.replace("passive_", "") for c in art.columns if c.startswith("passive_")}
    t4 = {}
    for prefix, cols in [("tsmom", tsmom_cols), ("passive", pass_cols)]:
        # Panel A: within-class avg pairwise correlation (common months)
        for short, c in CLASS_OF_COL.items():
            sub = art[[col for col, inst in cols.items() if cls.get(inst) == c]]
            pairs = []
            cs = sub.columns
            for i in range(len(cs)):
                for j in range(i + 1, len(cs)):
                    pairs.append(sub[cs[i]].corr(sub[cs[j]]))
            t4[f"corr_within_{prefix}_{short.lower()}"] = float(np.nanmean(pairs))
        # Panel B: across-class factor correlations
        base = "TSMOM" if prefix == "tsmom" else "PASSIVE"
        fcols = {"com": f"{base}_COMMODITY", "eq": f"{base}_EQUITY",
                 "fi": f"{base}_BOND", "fx": f"{base}_CURRENCY"}
        for a, b in [("eq", "com"), ("fi", "com"), ("fi", "eq"),
                     ("fx", "com"), ("fx", "eq"), ("fx", "fi")]:
            t4[f"corr_across_{prefix}_{a}_{b}"] = float(art[fcols[a]].corr(art[fcols[b]]))
    rows4 = []
    for n, m in T["T4"].items():
        rows4.append({"cell": n, "paper": m["value"], "ours": t4[n],
                      "tolerance_pct": m["tolerance_pct"],
                      "tier": tier(t4[n], m["value"], m["tolerance_pct"])})
    t4_df = pd.DataFrame(rows4)
    t4_df.to_csv(LAYOUT.result_path("eval_t4.csv"), index=False)
    md4 = ["# Table 4 — correlations of TSMOM and passive-long positions",
           "", "Panel A: within-class average pairwise correlation of per-instrument k=12 "
           "TSMOM (resp. passive) returns over common 1985-2009 months.",
           "Panel B: correlations among the four EW class-level factors.",
           "", "| metric | ours | paper | tol% | tier |", "|---|---:|---:|---:|---|"]
    for r in rows4:
        md4.append(f"| {r['cell']} | {r['ours']:+.3f} | {r['paper']:+.3f} | {r['tolerance_pct']} | {r['tier']} |")
    (LAYOUT.result_path("table_4.md")).write_text("\n".join(md4) + "\n")

    # ============ 4. TABLE 5 Panel C (XSMOM per A11) ============
    ret_wide = panel.pivot(index="month", columns="instrument", values="ret").sort_index()
    sig_wide = panel.pivot(index="month", columns="instrument", values="sigma").sort_index()
    months = ret_wide.index
    # cumulative excess over t-12..t-2 (skip most recent month), all 11 months required:
    # rolling(11) at m covers m-10..m; shift(2) -> at t covers t-12..t-2
    cum = ret_wide.rolling(11, min_periods=11).apply(lambda w: (1 + w).prod() - 1, raw=True).shift(2)
    # sigma at end of formation month t = panel sigma at t+1
    sig_end = sig_wide.shift(-1)

    xs = {}
    for name, subset in [("ALL", None), ("COM", "commodity"), ("EQ", "equity"),
                         ("FI", "bond"), ("FX", "currency")]:
        insts = list(cls.index) if subset is None else list(cls.index[cls == subset])
        csub = cum[insts]
        out = {}
        for t_loc in range(len(months) - 1):
            t = months[t_loc]
            t1 = months[t_loc + 1]
            if not (EVAL_START <= t1 <= EVAL_END):
                continue
            ranks = csub.loc[t].dropna().rank()
            if len(ranks) < 3:
                continue
            med = ranks.median()
            denom = (ranks - med).abs().sum()
            if denom == 0:
                continue
            w = (ranks - med) / denom
            s = sig_end.loc[t].reindex(w.index)
            r = ret_wide.loc[t1].reindex(w.index)
            contrib = w * (0.40 / s) * r
            contrib = contrib.replace([np.inf, -np.inf], np.nan).dropna()
            if len(contrib):
                out[t1] = float(contrib.sum())
        xs[f"XSMOM_{name}"] = pd.Series(out)
    xsmom = pd.DataFrame(xs)
    tsmom_all = art["TSMOM_ALL"]
    reg_set = {"XSMOM_ALL": xsmom["XSMOM_ALL"], "XSMOM_COM": xsmom["XSMOM_COM"],
               "XSMOM_EQ": xsmom["XSMOM_EQ"], "XSMOM_FI": xsmom["XSMOM_FI"],
               "XSMOM_FX": xsmom["XSMOM_FX"], "UMD": ff["UMD"], "HML": ff["HML"], "SMB": ff["SMB"]}
    t5 = {}
    for rname, ry in reg_set.items():
        res, _ = ols_fit(ry, pd.DataFrame({"TSMOM": tsmom_all}))
        t5[f"beta_tsmom_on_{rname}"] = res.params[1]
        t5[f"t_beta_{rname}"] = res.tvalues[1]
        t5[f"alpha_{rname}"] = res.params[0] * 100
        t5[f"t_alpha_{rname}"] = res.tvalues[0]
        t5[f"r2_{rname}"] = res.rsquared
    rows5 = []
    for n, m in T["T5"].items():
        rows5.append({"cell": n, "paper": m["value"], "ours": t5[n],
                      "tolerance_pct": m["tolerance_pct"],
                      "tier": tier(t5[n], m["value"], m["tolerance_pct"])})
    t5_df = pd.DataFrame(rows5)
    t5_df.to_csv(LAYOUT.result_path("eval_t5.csv"), index=False)
    md5 = ["# Table 5 Panel C — regressions on the diversified TSMOM factor",
           "", "XSMOM per A11: 12-month formation skipping the most recent month; weights "
           "(rank − median rank)/Σ|rank − median rank|; 40%/σ scaling. Rows: XSMOM variants + "
           "UMD/HML/SMB regressed on TSMOM_ALL (DJCS rows excluded — not in ClickHouse).",
           "", "| row | beta (t) | alpha %/mo (t) | R² | paper beta (t) | paper alpha (t) | paper R² |",
           "|---|---|---|---:|---|---|---:|"]
    for rname in reg_set:
        g = lambda k: next(r for r in rows5 if r["cell"] == k)
        b, tb, a, ta, r2 = g(f"beta_tsmom_on_{rname}"), g(f"t_beta_{rname}"), \
            g(f"alpha_{rname}"), g(f"t_alpha_{rname}"), g(f"r2_{rname}")
        md5.append(f"| {rname} | {b['ours']:+.2f} ({tb['ours']:+.2f}) | {a['ours']:+.2f} ({ta['ours']:+.2f}) "
                   f"| {r2['ours']:.2f} | {b['paper']:+.2f} ({tb['paper']:+.2f}) "
                   f"| {a['paper']:+.2f} ({ta['paper']:+.2f}) | {r2['paper']:.2f} |")
    (LAYOUT.result_path("table_5.md")).write_text("\n".join(md5) + "\n")

    # ============ 5. FIGURES ============
    # Fig 3 analog: cumulative log returns
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for col, label, c in [("TSMOM_ALL", "TSMOM (diversified, 40%/σ)", "tab:blue"),
                          ("PASSIVE_ALL", "Passive long (same ex ante vol)", "tab:orange")]:
        cumr = (1 + art[col]).cumprod()
        ax.plot(cumr.index, cumr.values, label=label, color=c, lw=1.8)
    ax.set_yscale("log")
    ax.set_title("Cumulative excess return: diversified TSMOM vs passive long (1985–2009, log scale)")
    ax.set_xlabel("month"); ax.set_ylabel("cumulative return (log)")
    ax.legend(loc="upper left"); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(LAYOUT.result_path("tsmom_factor_vs_passive.png"), dpi=130)
    plt.close(fig)

    # Fig 2 analog: per-instrument Sharpe bars grouped by class
    sharpe, labels, colors = [], [], []
    cmap = {"commodity": "tab:olive", "equity": "tab:blue", "bond": "tab:purple", "currency": "tab:cyan"}
    order = ["commodity", "equity", "bond", "currency"]
    by_class = {c: sorted([i for i in cls.index if cls[i] == c]) for c in order}
    for c in order:
        for inst in by_class[c]:
            s = art[f"tsmom_{inst}"].dropna()
            sharpe.append(s.mean() / s.std(ddof=1) * math.sqrt(12))
            labels.append(inst)
            colors.append(cmap[c])
    n_pos = sum(v > 0 for v in sharpe)
    fig, ax = plt.subplots(figsize=(14, 5.5))
    xs = np.arange(len(sharpe))
    ax.bar(xs, sharpe, color=colors, width=0.8)
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(xs); ax.set_xticklabels(labels, rotation=75, fontsize=7)
    ax.set_title(f"Annualized Sharpe of 12-month TSMOM by instrument, grouped by asset class "
                 f"({n_pos}/{len(sharpe)} positive; paper: 58/58)")
    ax.set_ylabel("Sharpe ratio (ann.)"); ax.grid(alpha=0.3, axis="y")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=cmap[c], label=c) for c in order], loc="upper right", fontsize=8)
    fig.tight_layout(); fig.savefig(LAYOUT.result_path("sharpe_by_instrument.png"), dpi=130)
    plt.close(fig)

    # Fig 4 analog: TSMOM smile vs SP500 quarterly
    sp = panel[panel.instrument == "SP500"].set_index("month")["ret"]
    spq = qtr(sp); tq = qtr(art["TSMOM_ALL"])
    dq = pd.DataFrame({"sp": spq, "ts": tq}).dropna()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(dq["sp"] * 100, dq["ts"] * 100, s=22, color="tab:blue", alpha=0.7)
    ax.axhline(0, color="black", lw=0.8); ax.axvline(0, color="black", lw=0.8)
    if (dq.index.get_level_values(0) == 2008).any() and 4 in dq.index.get_level_values(1):
        p = dq.loc[(2008, 4)]
        ax.scatter([p["sp"] * 100], [p["ts"] * 100], s=80, facecolor="none", edgecolor="red", lw=2)
        ax.annotate("2008Q4", (p["sp"] * 100, p["ts"] * 100),
                    xytext=(p["sp"] * 100 + 2, p["ts"] * 100 - 1.5), fontsize=9, color="red")
    # quadratic fit to visualize the smile
    x = dq["sp"].values * 100
    coef = np.polyfit(x, dq["ts"].values * 100, 2)
    xx = np.linspace(x.min(), x.max(), 100)
    ax.plot(xx, np.polyval(coef, xx), color="tab:red", lw=1.5, ls="--",
            label=f"quadratic fit (curvature {coef[0]:+.3f})")
    ax.set_xlabel("S&P 500 futures quarterly return (%)")
    ax.set_ylabel("TSMOM quarterly return (%)")
    ax.set_title("TSMOM 'smile': quarterly TSMOM vs S&P 500 futures (1985–2009)")
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(LAYOUT.result_path("tsmom_smile.png"), dpi=130)
    plt.close(fig)

    # ============ summary ============
    print("\nT3 tiers:", t3_df.tier.value_counts().to_dict())
    print("T4 tiers:", t4_df.tier.value_counts().to_dict())
    print("T5 tiers:", t5_df.tier.value_counts().to_dict())
    for name, df in [("T3", t3_df), ("T4", t4_df), ("T5", t5_df)]:
        f = df[df.tier == "FAIL"]
        if len(f):
            print(f"\n{name} FAILS:")
            for _, r in f.iterrows():
                print(f"  {r.cell}: ours {r.ours:+.3f} vs paper {r.paper:+.3f} (tol {r.tolerance_pct}%)")
    print(f"\nTable 3 monthly: alpha {pm['const']*100:+.3f}%/mo t={pm_t['const']:.2f} "
          f"(paper 1.58, t 7.99); UMD beta {pm['UMD']:+.2f} t={pm_t['UMD']:.2f} "
          f"(paper 0.28, t 6.78); MKT beta {pm['MKT']:+.2f} t={pm_t['MKT']:.2f}; R²={res_m.rsquared:.3f}")
    print(f"Table 3 quarterly: alpha {pq['const']*100:+.3f}%/qtr t={pq_t['const']:.2f} "
          f"(paper 4.75, t 7.73); UMD beta {pq['UMD']:+.2f}; R²={res_q.rsquared:.3f}")
    print(f"\nT5 XSMOM_ALL on TSMOM: beta {t5['beta_tsmom_on_XSMOM_ALL']:+.3f} "
          f"(t {t5['t_beta_XSMOM_ALL']:.2f}), R² {t5['r2_XSMOM_ALL']:.3f}  (paper 0.66, t 15.17, R² 0.44)")
    print(f"Sharpe bars: {n_pos}/{len(sharpe)} instruments positive (paper: 58/58)")
    print(f"Smile quadratic curvature: {coef[0]:+.4f} (positive => straddle/smile pattern)")
    print("\nFigures: results/tsmom_factor_vs_passive.png, sharpe_by_instrument.png, tsmom_smile.png")


if __name__ == "__main__":
    main()
