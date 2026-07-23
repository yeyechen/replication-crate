"""
LSV (1994) Table VIII — betas & standard deviations (22 annual Year+1 obs per
portfolio, A11). Reads panel.parquet; pulls ff.four_factor_monthly.rf (DECIMAL in
this extract — verified rf_ann~0.08; the task's '/100' hint is WRONG here) and
msi.vwretd / msi.ewretd. Per portfolio: beta = OLS slope of (R1-rf) on (VW-rf);
std = std(R1, ddof=1); saar_std = std(R1 - B, ddof=1) where B = mean sizedec_ret_1
over that year's members. EW-index row = beta/std of annual EW returns vs VW
excess (saar_std = '--'). Emits table_8.md (all deciles/cells) + table_VIII_cells.json
(P1 dec1-10; P2 EW index only; P3 dec1-6 + EW index, per OCR-truncated targets).

Run: cd repo-root && uv run python replications/contrarian_investment/src/table8.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dotenv import load_dotenv  # noqa: E402
load_dotenv(REPO_ROOT / ".env")
from clickhouse_driver import Client  # noqa: E402
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402
import sortlib as S  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
RES = LAYOUT.results_dir
FYS = list(range(1968, 1990))


def vmask(df, var):
    return {"bm": (df["be_valid"] == 1) & df["bm"].notna(),
            "cp": df["cp_pos"] == 1, "gs": df["gs_rank_frac"].notna()}[var]


def q(sql):
    cfg = get_clickhouse_config()
    c = Client(host=cfg["host"], port=int(cfg["port"]), user=cfg["user"],
               password=cfg["password"],
               settings={"max_execution_time": 200,
                         "max_rows_to_read": 10000000000,
                         "timeout_before_checking_execution_speed": 0})
    data, cols = c.execute(sql, with_column_types=True)
    return pd.DataFrame(data, columns=[x[0] for x in cols])


def annual(df, datecol, valcol):
    """compound May fy..Apr fy+1 per formation fy -> Series indexed by fy."""
    df = df.copy()
    df["y"] = df[datecol].str[:4].astype(int)
    df["mo"] = df[datecol].str[5:7].astype(int)
    df["fy"] = np.where(df["mo"] >= 5, df["y"], df["y"] - 1)
    out = {}
    for fy in FYS:
        sub = df[df["fy"] == fy].sort_values(datecol)
        out[fy] = float(np.prod(1 + sub[valcol].fillna(0.0)) - 1)
    return pd.Series(out)


def ols_beta(y, x):
    y = np.asarray(y, float); x = np.asarray(x, float)
    m = ~(np.isnan(y) | np.isnan(x))
    y, x = y[m], x[m]
    if len(y) < 3:
        return np.nan
    xc = x - x.mean()
    den = (xc * xc).sum()
    return float((xc * (y - y.mean())).sum() / den) if den > 0 else np.nan


def build_portfolios(panel):
    """dict port_name -> boolean mask over panel (membership at formation)."""
    cp_dec = pd.Series(np.nan, index=panel.index)
    bm_dec = pd.Series(np.nan, index=panel.index)
    cp_g = pd.Series(np.nan, index=panel.index)
    gs_g = pd.Series(np.nan, index=panel.index)
    for _, idx in panel.groupby("fy").groups.items():
        ic = idx[vmask(panel, "cp").loc[idx]]
        ib = idx[vmask(panel, "bm").loc[idx]]
        ig = idx[vmask(panel, "gs").loc[idx]]
        if len(ic) >= 10:
            cp_dec.loc[ic] = S.assign_deciles(panel.loc[ic, "cp"], 10).astype(float)
        if len(ib) >= 10:
            bm_dec.loc[ib] = S.assign_deciles(panel.loc[ib, "bm"], 10).astype(float)
        if len(ic):
            cp_g.loc[ic] = S.assign_304030(panel.loc[ic, "cp"]).astype(float)
        if len(ig):
            gs_g.loc[ig] = S.assign_304030(panel.loc[ig, "gs_rank_frac"]).astype(float)
    ports = {}
    for d in range(1, 11):
        ports[f"P1_d{d}"] = (cp_dec == d)
        ports[f"P3_d{d}"] = (bm_dec == d)
    for a in (1, 2, 3):
        for b in (1, 2, 3):
            ports[f"P2_{a}_{b}"] = ((cp_g == a) & (gs_g == b))
    return ports


def port_annual(panel, mask):
    """R1 (EW mean stock_ret_1) and B (EW mean sizedec_ret_1) per formation."""
    sub = panel.loc[mask & (panel["alive_1"] == 1) &
                    panel["stock_ret_1"].notna()].copy()
    R1 = sub.groupby("fy")["stock_ret_1"].mean()
    B = sub.groupby("fy")["sizedec_ret_1"].mean()
    return R1.reindex(FYS), B.reindex(FYS)


def main():
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    print(f"Loaded panel {panel.shape}")
    ff = q("SELECT dt, rf FROM ff.four_factor_monthly "
           "WHERE dt >= '1968-05-01' AND dt <= '1990-04-30' "
           "SETTINGS max_execution_time=120, max_rows_to_read=10000000000, "
           "timeout_before_checking_execution_speed=0")
    msi = q("SELECT date, vwretd, ewretd FROM crsp_202601.msi "
            "WHERE date >= '1968-05-01' AND date <= '1990-04-30' "
            "SETTINGS max_execution_time=120, max_rows_to_read=10000000000, "
            "timeout_before_checking_execution_speed=0")
    rf_ann = annual(ff, "dt", "rf")          # DECIMAL units (NOT /100)
    vw_ann = annual(msi, "date", "vwretd")
    ew_ann = annual(msi, "date", "ewretd")
    mkt_ex = vw_ann - rf_ann
    ew_ex = ew_ann - rf_ann

    ports = build_portfolios(panel)
    stats = {}   # name -> dict(beta, std, saar_std, R1)
    for name, mask in ports.items():
        R1, B = port_annual(panel, mask)
        beta = ols_beta(R1.values - rf_ann.values, mkt_ex.values)
        std = float(R1.std(ddof=1))
        sa = R1 - B
        saar_std = float(sa.std(ddof=1))
        stats[name] = {"beta": beta, "std": std, "saar_std": saar_std, "R1": R1}
    # EW index row
    ew_beta = ols_beta(ew_ex.values, mkt_ex.values)
    ew_std = float(ew_ann.std(ddof=1))
    stats["EW"] = {"beta": ew_beta, "std": ew_std, "saar_std": np.nan}

    # ---- cells JSON ----
    tgt = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t8 = {m["name"]: m["value"] for t in tgt["tables"] if t["id"] == "table_VIII"
          for m in t["metrics"]}
    cells = {}

    def put(name, val):
        if name in t8 and val is not None and not pd.isna(val):
            cells[name] = round(float(val), 6)

    for d in range(1, 11):
        for stat in ["beta", "std", "saar_std"]:
            put(f"P1 (C/P) decile {d} {stat}", stats[f"P1_d{d}"][stat])
    for stat in ["beta", "std"]:
        put(f"P1 (C/P) EW index {stat}", stats["EW"][stat])
    for stat in ["beta", "std"]:
        put(f"P2 (C/PxGS) EW index {stat}", stats["EW"][stat])
    for d in range(1, 7):
        for stat in ["beta", "std", "saar_std"]:
            put(f"P3 (B/M) decile {d} {stat}", stats[f"P3_d{d}"][stat])
    for stat in ["beta", "std"]:
        put(f"P3 (B/M) EW index {stat}", stats["EW"][stat])
    out = {n: cells[n] for n in t8 if n in cells}
    (RES / "table_VIII_cells.json").write_text(json.dumps(out, indent=2))
    print(f"Emitted table_VIII_cells.json: {len(out)} / {len(t8)}")

    # ---- markdown (all 10 deciles / 9 cells) ----
    write_md(stats)
    print("Wrote results/table_8.md")

    # ---- diagnostics ----
    print("\n" + "=" * 70)
    print("TABLE VIII DIAGNOSTICS (rf used as DECIMAL; /100 NOT applied)")
    print("=" * 70)
    pap = {"P1_beta": {1: 1.268, 10: 1.384, "EW": 1.304},
           "P1_std": {1: 0.224, 10: 0.252, "EW": 0.250},
           "P1_saar": {1: 0.037, 10: 0.058},
           "P2_EW": {"beta": 1.304, "std": 0.250},
           "P3_beta": {1: 1.248, 6: 1.214},
           "P3_std": {1: 0.223},
           "P3_saar": {1: 0.076, 6: 0.040}}
    print("\n[beta] P1 D1/D10/EW:",
          {k: round(stats['P1_d%d' % k]['beta'], 3) if isinstance(k, int)
           else round(stats['EW']['beta'], 3) for k in [1, 10, 'EW']},
          "paper", pap['P1_beta'])
    print("[std ] P1 D1/D10/EW:",
          {k: round(stats['P1_d%d' % k]['std'], 3) if isinstance(k, int)
           else round(stats['EW']['std'], 3) for k in [1, 10, 'EW']},
          "paper", pap['P1_std'])
    print("[saar] P1 D1/D10:",
          {k: round(stats['P1_d%d' % k]['saar_std'], 3) for k in [1, 10]},
          "paper", pap['P1_saar'])
    print("[P2 EW] beta/std:", round(stats['EW']['beta'], 3),
          round(stats['EW']['std'], 3), "paper", pap['P2_EW'])
    print("[P3 beta] D1/D6:", round(stats['P3_d1']['beta'], 3),
          round(stats['P3_d6']['beta'], 3), "paper", pap['P3_beta'])
    print("[P3 saar] D1/D6:", round(stats['P3_d1']['saar_std'], 3),
          round(stats['P3_d6']['saar_std'], 3), "paper", pap['P3_saar'])
    # claim: value beta ~0.1 higher than glamour; saar_std ~ identical
    b1 = stats["P1_d1"]["beta"]; b10 = stats["P1_d10"]["beta"]
    s1 = stats["P1_d1"]["saar_std"]; s10 = stats["P1_d10"]["saar_std"]
    print(f"\n[claim] P1 value-glamour beta gap = {b10-b1:+.3f} (paper ~+0.1); "
          f"saar_std D1={s1:.3f} D10={s10:.3f} (nearly identical?)")
    print("=" * 70)


def write_md(stats):
    L = ["# Table VIII — Betas & standard deviations (LSV 1994)", "",
         "22 annual Year+1 EW portfolio returns; beta = OLS slope of (R1-rf) on "
         "(VW-rf); std = std(R1); saar_std = std(R1 - size-benchmark). rf in "
         "DECIMAL (verified). 3 decimals.", ""]

    # P1 C/P deciles
    L += ["## Panel 1 — C/P deciles", "",
          "| Stat | " + " | ".join(f"D{d}" for d in range(1, 11)) + " | EW idx |",
          "|---|" + "---|" * 11]
    for stat, key in [("beta", "beta"), ("std", "std"), ("saar_std", "saar_std")]:
        vals = [f"{stats[f'P1_d{d}'][key]:.3f}" for d in range(1, 11)]
        ew = "-" if pd.isna(stats['EW'][key]) else f"{stats['EW'][key]:.3f}"
        L.append("| " + stat + " | " + " | ".join(vals) + f" | {ew} |")
    # P2 C/PxGS cells
    L += ["", "## Panel 2 — C/P x GS cells", "",
          "| Stat | " + " | ".join(f"(C{a},G{b})" for a in (1, 2, 3)
                                   for b in (1, 2, 3)) + " | EW idx |",
          "|---|" + "---|" * 10]
    for stat in ["beta", "std", "saar_std"]:
        vals = [f"{stats[f'P2_{a}_{b}'][stat]:.3f}" for a in (1, 2, 3)
                for b in (1, 2, 3)]
        ew = "-" if pd.isna(stats['EW'][stat]) else f"{stats['EW'][stat]:.3f}"
        L.append("| " + stat + " | " + " | ".join(vals) + f" | {ew} |")
    # P3 B/M deciles
    L += ["", "## Panel 3 — B/M deciles", "",
          "| Stat | " + " | ".join(f"D{d}" for d in range(1, 11)) + " | EW idx |",
          "|---|" + "---|" * 11]
    for stat in ["beta", "std", "saar_std"]:
        vals = [f"{stats[f'P3_d{d}'][stat]:.3f}" for d in range(1, 11)]
        ew = "-" if pd.isna(stats['EW'][stat]) else f"{stats['EW'][stat]:.3f}"
        L.append("| " + stat + " | " + " | ".join(vals) + f" | {ew} |")
    (RES / "table_8.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
