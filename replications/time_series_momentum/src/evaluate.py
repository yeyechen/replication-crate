"""
Inner iteration 3 — TSMOM strategy engine + Table 1 / Table 2 evaluation.

Builds (from the frozen data/panel.parquet):
  * TSMOM(k,h) monthly strategy returns, §3.2 exact timing:
      - formation month j, lookback k: R(k)_{s,j} = prod_{m=j-k+1..j}(1+ret) - 1
        (requires all k months present, else no signal);
      - holding month m in {j+1..j+h}: position return =
        sign(R(k)_{s,j}) x (1/sigma_end_j) x ret_{s,m}, with sigma_end_j =
        ex ante vol at END of month j = panel sigma at month j+1 (the panel's
        sigma column is already lagged one month);
      - month t strategy return = average over the h active cohorts
        (formed at t-h..t-1); each cohort is equal-weighted over the
        instruments available in that cohort and in month t.
  * Alpha regressions per (k,h) x panel (A all / B commodity / C equity /
    D bond): r = a + b1 MKT + b2 BOND + b3 GSCI + b4 SMB + b5 HML + b6 UMD.
    MKT/BOND/GSCI = equal-weighted RAW monthly excess returns of the paper's
    own equity/bond/commodity futures (A2 proxies); SMB/HML/UMD from
    ff.four_factor_monthly (decimals, A7). Intercept t-stat with Newey-West
    h-1 lags (A10); plain OLS at h=1.
  * §4.1 artifacts (k=12, h=1): security-level sign x 40%/sigma x ret
    returns, diversified + per-class TSMOM factors, passive-long analogs
    (sign -> +1), MKT/BOND/GSCI proxies -> data/strategy_artifacts.parquet.
  * Table 1 / Table 2 evaluations -> results/table_1.md, eval_t1.csv,
    results/table_2.md, eval_t2.csv (tier rules per rep/TOLERANCE_RULES.md).
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_SRC_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SRC_DIR.parents[1]
sys.path.insert(0, str(_PROJECT_ROOT))

from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("time_series_momentum")

EVAL_START = pd.Timestamp("1985-01-31")   # month-ends
EVAL_END = pd.Timestamp("2009-12-31")
K_GRID = [1, 3, 6, 9, 12, 24, 36, 48]
H_GRID = [1, 3, 6, 9, 12, 24, 36, 48]
# T2 panels evaluated (Panel E currencies OCR-truncated in the source)
PANELS = {
    "all_assets": None,                     # all instruments
    "commodity": "commodity",
    "equity_index": "equity",
    "bond": "bond",
}
# T1 metric instrument names (tables_to_replicate.json) -> our instrument codes
T1_NAME_MAP = {
    "ASX_SPI200": "SPI200", "FTSE_MIB": "FTSEMIB", "JP10Y": "JGB10Y",
    "UK10Y": "GILT", "US30Y": "USLONG",
}


# --- tier logic (rep/TOLERANCE_RULES.md) ---------------------------------
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


# --- strategy engine ------------------------------------------------------
def build_signal(ret_wide: pd.DataFrame, k: int) -> pd.DataFrame:
    """R(k)_{s,j} = prod_{j-k+1..j}(1+ret)-1, NaN unless all k months present."""
    out = {}
    for s in ret_wide.columns:
        r = ret_wide[s]
        roll = r.rolling(k, min_periods=k)
        out[s] = roll.apply(lambda w: float((1.0 + w).prod() - 1.0), raw=True)
    return pd.DataFrame(out, index=ret_wide.index)


def tsmom_strategy(ret_wide: pd.DataFrame, sig_end: pd.DataFrame,
                   k: int, h: int) -> pd.Series:
    """Monthly TSMOM(k,h) return: mean over h active cohorts of the
    equal-weighted (over available instruments) cohort position returns.

    Position formed at j for holding month m: sign(R_k[j]) x ret[m] / sig_end[j]
    where sig_end[j] = ex ante vol at end of month j (= panel sigma at j+1).
    """
    Rk = build_signal(ret_wide, k)
    pos = np.sign(Rk) / sig_end                      # formation-month positions
    pos = pos.replace([np.inf, -np.inf], np.nan)
    months = ret_wide.index
    t_lo = months.searchsorted(EVAL_START)
    t_hi = months.searchsorted(EVAL_END, side="right")
    eval_months = months[t_lo:t_hi]
    vals = np.full(len(eval_months), np.nan)
    for i, t in enumerate(eval_months):
        cohort_rets = []
        for d in range(1, h + 1):                    # cohorts formed at t-d
            j_loc = months.get_loc(t) - d
            if j_loc < 0:
                continue
            j = months[j_loc]
            p = pos.loc[j].to_numpy() * ret_wide.loc[t].to_numpy()
            p = p[np.isfinite(p)]
            if len(p):
                cohort_rets.append(p.mean())
        if cohort_rets:
            vals[i] = float(np.mean(cohort_rets))
    return pd.Series(vals, index=eval_months)


def alpha_tstat(y: pd.Series, X: pd.DataFrame, h: int) -> float:
    """OLS intercept t-stat; Newey-West h-1 lags for h>1 (A10), plain OLS h=1."""
    from statsmodels.regression.linear_model import OLS
    from statsmodels.tools import add_constant

    df = pd.concat([y.rename("y"), X], axis=1).dropna()
    if len(df) < 24:
        return float("nan")
    res = OLS(df["y"].to_numpy(),
              add_constant(df[X.columns].to_numpy())).fit(
                  cov_type="HAC", cov_kwds={"maxlags": h - 1}) if h > 1 else \
        OLS(df["y"].to_numpy(), add_constant(df[X.columns].to_numpy())).fit()
    return float(res.tvalues[0])


# --- main -----------------------------------------------------------------
def main() -> None:
    rules = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t1_metrics = {m["name"]: m for m in rules["tables"][0]["metrics"]}
    t2_metrics = {m["name"]: m for m in rules["tables"][1]["metrics"]}

    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    panel["month"] = pd.to_datetime(panel["month"])
    panel = panel.sort_values(["instrument", "month"])

    # SMB/HML/UMD from ff.four_factor_monthly (decimals, A7)
    from clickhouse_driver import Client
    from utils.env import get_clickhouse_config
    import os
    cfg = get_clickhouse_config()
    cli = Client(host=os.getenv("CLICKHOUSE_HOST", cfg["host"]),
                 port=int(os.getenv("CLICKHOUSE_PORT", cfg["port"])),
                 user=os.getenv("CLICKHOUSE_USER", cfg["user"]),
                 password=os.getenv("CLICKHOUSE_PASSWORD", cfg["password"]),
                 settings={"max_execution_time": 60})
    rows, cols = cli.execute(
        "SELECT dt, smb, hml, mom FROM ff.four_factor_monthly "
        "WHERE dt >= '1984-01-01' AND dt <= '2009-12-31'", with_column_types=True)
    ff = pd.DataFrame(rows, columns=[c[0] for c in cols])
    ff["month"] = pd.to_datetime(ff["dt"])
    ff = ff.set_index("month")[["smb", "hml", "mom"]].astype(float)

    # wide matrices
    ret_wide = panel.pivot(index="month", columns="instrument", values="ret").sort_index()
    sig_wide = panel.pivot(index="month", columns="instrument", values="sigma").sort_index()
    cls = panel.drop_duplicates("instrument").set_index("instrument")["asset_class"]

    # sigma at END of month j = panel sigma at month j+1 (panel sigma already
    # lagged one month): shift(-1) on the month-sorted index
    sig_end = sig_wide.shift(-1)

    # passive class proxies (RAW EW excess returns, A2)
    proxies = {}
    for name, c in [("MKT", "equity"), ("BOND", "bond"), ("GSCI", "commodity")]:
        insts = cls.index[cls == c]
        proxies[name] = ret_wide[insts].mean(axis=1)
    factors = pd.DataFrame(proxies)
    factors[["SMB", "HML", "UMD"]] = ff
    factors.index.name = "month"

    # ---------------- Table 1 ----------------
    t1_rows = []
    counts_t1 = {"mean": {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0},
                 "vol": {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}}
    for mname, m in t1_metrics.items():
        _, kind, inst = mname.split("_", 2)                    # ann_mean_X / ann_vol_X
        code = T1_NAME_MAP.get(inst, inst)
        sub = panel[panel.instrument == code]
        if kind == "mean":
            ours = sub["ret"].mean() * 12 * 100 if len(sub) > 1 else float("nan")
        else:
            ours = sub["ret"].std(ddof=1) * math.sqrt(12) * 100 if len(sub) > 2 else float("nan")
        t = tier(ours, m["value"], m["tolerance_pct"])
        counts_t1["mean" if kind == "mean" else "vol"][t] += 1
        t1_rows.append({"cell": mname, "instrument": code, "stat": kind,
                        "paper": m["value"], "ours": ours, "tolerance_pct": m["tolerance_pct"],
                        "tier": t, "paper_location": m["paper_location"]})
    t1_df = pd.DataFrame(t1_rows)
    t1_df.to_csv(LAYOUT.result_path("eval_t1.csv"), index=False)

    md = ["# Table 1 — annualized mean / vol of futures excess returns (full sample, panel window)",
          "", "Tiers: Tier 1 = |ours-paper|/|paper| <= tolerance (mean 15%, vol 10%); "
          "Tier 2 = sign match; FAIL = sign flip.",
          f"Counts — mean cells: {counts_t1['mean']}  |  vol cells: {counts_t1['vol']}",
          "NOTE (A1): means use the US T-bill rf for all instruments -> ~-4pp/yr uniform "
          "shift vs the paper's means (documented assumption; mean cells expected at Tier 2 "
          "on bonds/FX, sign-flips flagged for inspection).", "",
          "| instrument | mean (ours) | mean (paper) | tier | vol (ours) | vol (paper) | tier |",
          "|---|---:|---:|---|---:|---:|---|"]
    insts_t1 = sorted({r["instrument"] for r in t1_rows})
    for inst in insts_t1:
        a = t1_df[(t1_df.instrument == inst) & (t1_df.stat == "mean")].iloc[0]
        b = t1_df[(t1_df.instrument == inst) & (t1_df.stat == "vol")].iloc[0]
        flag = " **SIGN-FLIP**" if (a.tier == "FAIL" or b.tier == "FAIL") else ""
        md.append(f"| {inst}{flag} | {a.ours:+.2f} | {a.paper:+.2f} | {a.tier} "
                  f"| {b.ours:.2f} | {b.paper:.2f} | {b.tier} |")
    (LAYOUT.result_path("table_1.md")).write_text("\n".join(md) + "\n")

    # ---------------- TSMOM(k,h) grid + Table 2 ----------------
    strat_cache: dict[tuple[str, int, int], pd.Series] = {}
    t2_rows = []
    counts_t2 = {p: {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0} for p in PANELS}
    for pname, pcls in PANELS.items():
        insts = list(cls.index) if pcls is None else list(cls.index[cls == pcls])
        rw = ret_wide[insts]
        sw = sig_end[insts]
        for k in K_GRID:
            ks_bond = [1, 3, 6, 9, 12] if pname == "bond" else K_GRID
            if k not in ks_bond:
                continue
            for h in H_GRID:
                s = tsmom_strategy(rw, sw, k, h)
                strat_cache[(pname, k, h)] = s
                t = alpha_tstat(s, factors, h)
                cell = f"alpha_tstat_{pname}_k{k}_h{h}"
                m = t2_metrics.get(cell)
                if m is None:
                    continue
                ti = tier(t, m["value"], m["tolerance_pct"])
                counts_t2[pname][ti] += 1
                t2_rows.append({"cell": cell, "panel": pname, "k": k, "h": h,
                                "paper": m["value"], "ours": t, "tier": ti,
                                "n_obs": int(s.notna().sum()),
                                "paper_location": m["paper_location"]})
    t2_df = pd.DataFrame(t2_rows)
    t2_df.to_csv(LAYOUT.result_path("eval_t2.csv"), index=False)

    titles = {"all_assets": "Panel A: All assets", "commodity": "Panel B: Commodity futures",
              "equity_index": "Panel C: Equity index futures", "bond": "Panel D: Bond futures"}
    md2 = ["# Table 2 — t-statistics of TSMOM(k,h) alphas (7-factor: MKT/BOND/GSCI proxies + SMB/HML/UMD)",
           "", "Intercept t-stat, Newey-West h-1 lags (A10; plain OLS at h=1). Cell format: ours (paper).",
           "Tiers: Tier 1 within 200% relative tolerance; Tier 2 sign match; FAIL sign flip.",
           "MKT/BOND/GSCI are EW of the paper's own equity/bond/commodity futures (A2 — MSCI World / "
           "Barclays Agg / S&P GSCI not in ClickHouse).", ""]
    for pname in PANELS:
        sub = t2_df[t2_df.panel == pname]
        ks = sorted(sub.k.unique())
        md2.append(f"## {titles[pname]}  (tiers: {counts_t2[pname]})")
        md2.append("")
        md2.append("| k\\h | " + " | ".join(str(h) for h in H_GRID) + " |")
        md2.append("|---|" + "---:|" * len(H_GRID))
        for k in ks:
            cells = []
            for h in H_GRID:
                r = sub[(sub.k == k) & (sub.h == h)]
                if len(r):
                    r = r.iloc[0]
                    mark = {"Tier 1": "", "Tier 2": "·", "FAIL": "**!!**", "SKIP": "na"}[r.tier]
                    cells.append(f"{r.ours:+.2f} ({r.paper:+.2f}){mark}")
                else:
                    cells.append("—")
            md2.append(f"| {k} | " + " | ".join(cells) + " |")
        md2.append("")
    fails = t2_df[t2_df.tier == "FAIL"]
    md2.append(f"## FAIL cells ({len(fails)})")
    for _, r in fails.iterrows():
        md2.append(f"- {r.cell}: ours {r.ours:+.2f} vs paper {r.paper:+.2f}")
    (LAYOUT.result_path("table_2.md")).write_text("\n".join(md2) + "\n")

    # ---------------- §4.1 artifacts (k=12, h=1) ----------------
    R12 = build_signal(ret_wide, 12)
    sig_hold = sig_wide                      # panel sigma[m] = sigma at end of m-1 (holding month m)
    sec = (np.sign(R12.shift(1)) * (0.40 / sig_hold) * ret_wide)   # Eq. (5) at holding month m
    sec = sec.replace([np.inf, -np.inf], np.nan)
    pas = (0.40 / sig_hold) * ret_wide                             # passive-long analog
    pas = pas.replace([np.inf, -np.inf], np.nan)
    ev = sec.index[(sec.index >= EVAL_START) & (sec.index <= EVAL_END)]
    art = {}
    for s in sec.columns:
        art[f"tsmom_{s}"] = sec.loc[ev, s]
        art[f"passive_{s}"] = pas.loc[ev, s]
    art["TSMOM_ALL"] = sec.loc[ev].mean(axis=1)
    art["PASSIVE_ALL"] = pas.loc[ev].mean(axis=1)
    for c in ["commodity", "equity", "bond", "currency"]:
        insts = list(cls.index[cls == c])
        art[f"TSMOM_{c.upper()}"] = sec.loc[ev, insts].mean(axis=1)
        art[f"PASSIVE_{c.upper()}"] = pas.loc[ev, insts].mean(axis=1)
    for name in ["MKT", "BOND", "GSCI"]:
        art[name] = proxies[name].loc[ev]
    artifacts = pd.DataFrame(art)
    artifacts.index.name = "month"
    artifacts.to_parquet(LAYOUT.data_path("strategy_artifacts.parquet"))

    # ---------------- diagnostics ----------------
    k12 = strat_cache[("all_assets", 12, 1)]
    ann_mean = k12.mean() * 12 * 100
    ann_vol = k12.std(ddof=1) * math.sqrt(12) * 100
    sharpe = k12.mean() / k12.std(ddof=1) * math.sqrt(12)
    print("=" * 72)
    print("T1 tiers — mean:", counts_t1["mean"], "| vol:", counts_t1["vol"])
    print("T2 tiers per panel:")
    for p in PANELS:
        print(f"  {p:<13}: {counts_t2[p]}")
    print(f"\nk=12,h=1 ALL-ASSETS TSMOM: ann mean {ann_mean:+.2f}%  ann vol {ann_vol:.2f}%  "
          f"Sharpe {sharpe:.2f}  (n={int(k12.notna().sum())})")
    print("  (paper: ~1.5%/month, ~12% annual vol)")
    print("\nT1 FAIL cells:")
    for _, r in t1_df[t1_df.tier == "FAIL"].iterrows():
        print(f"  {r.cell}: ours {r.ours:+.2f} vs paper {r.paper:+.2f}")
    print("\nT2 FAIL cells:")
    for _, r in fails.iterrows():
        print(f"  {r.cell}: ours {r.ours:+.2f} vs paper {r.paper:+.2f}")
    print("\nSignature pattern (Panel A all_assets, h=1 column by k):")
    a = t2_df[(t2_df.panel == "all_assets") & (t2_df.h == 1)]
    print("  " + "  ".join(f"k{k}:{r.ours:+.2f}({r.paper:+.2f})" for _, r in a.iterrows() for k in [r.k]))
    print("\nPanel A full grid (ours):")
    piv = t2_df[t2_df.panel == "all_assets"].pivot(index="k", columns="h", values="ours")
    print(piv.round(2).to_string())
    print("\nWrote results/table_1.md, eval_t1.csv, results/table_2.md, eval_t2.csv, "
          "data/strategy_artifacts.parquet")


if __name__ == "__main__":
    main()
