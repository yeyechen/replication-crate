"""
LSV (1994) Table VI (year-by-year value-glamour, 1/3/5-yr horizons) + Figure 2.

Reads data/panel.parquet. Emits results/table_6.md, results/table_VI_cells.json
(exact target names from preparations/tables_to_replicate.json) and
results/figure_2.png.

Panel definitions (value - glamour, per-formation k-yr cumulative spread):
  P1 C/P : pooled deciles (9,10) vs (1,2)            [cp_pos subset]
  P2 C/PxGS: cell (C/P3,GS1) vs cell (C/P1,GS3)      [30/40/30]
  P3 B/M : pooled deciles (9,10) vs (1,2)            [be_valid subset]
  NOTE: the paper's Panel 3 CAPTION (L2210) says "highest vs lowest decile"
  (single), but the table HEADER (L2220 "B/M: 9,10 - 1,2"), the body text
  (L2278) and the metric label "B/M D10,9-D1,2" all use the POOLED 2-decile
  spread, which also reproduces the paper's numbers (single D10-D1 for 1968 =
  0.043 vs paper 0.098; pooled = 0.104). We follow the header/label/values.

CRITICAL sample boundary: a horizon observation is dropped if its holding
window ends after April 1990 -> 1-yr 1968-1989 (22), 3-yr 1968-1987 (20),
5-yr 1968-1985 (18). t-stats: 1-yr iid; 3-yr Hansen-Hodrick lag<=1 (k=2);
5-yr Hansen-Hodrick lag<=3 (k=4), per A12 (verified to reproduce the paper's
published t's; the textbook MA(H-1) truncation is unstable at T=18).

Run: cd repo-root && uv run python replications/contrarian_investment/src/table6.py
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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from clickhouse_driver import Client  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO_ROOT / ".env")
from utils.env import get_clickhouse_config  # noqa: E402
from utils.paths import paper_layout  # noqa: E402
import sortlib as S  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
RES = LAYOUT.results_dir
TARGETS = json.loads(LAYOUT.preparations_path("tables_to_replicate.json")
                     .read_text())
T6_NAMES = {m["name"] for t in TARGETS["tables"] if t["id"] == "table_VI"
            for m in t["metrics"]}
PAPER = {m["name"]: m["value"] for t in TARGETS["tables"]
         if t["id"] == "table_VI" for m in t["metrics"]}

SIG = {"bm": "bm", "cp": "cp", "gs": "gs_rank_frac"}


def vmask(df, var):
    return {"bm": (df["be_valid"] == 1) & df["bm"].notna(),
            "cp": df["cp_pos"] == 1,
            "gs": df["gs_rank_frac"].notna()}[var]


# --- group assignments -----------------------------------------------------
def pooled_decile_groups(panel: pd.DataFrame, var: str) -> pd.Series:
    vm = vmask(panel, var)
    dec = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    for _, idx in panel.groupby("fy").groups.items():
        ii = idx[vm.loc[idx]]
        if len(ii) >= 10:
            dec.loc[ii] = S.assign_deciles(panel.loc[ii, SIG[var]], 10)
    grp = pd.Series(np.nan, index=panel.index, dtype=object)
    grp[dec.isin([9, 10])] = "V"
    grp[dec.isin([1, 2])] = "G"
    return grp


def cpgs_corner_groups(panel: pd.DataFrame) -> pd.Series:
    g1 = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    g2 = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    m1, m2 = vmask(panel, "cp"), vmask(panel, "gs")
    for _, idx in panel.groupby("fy").groups.items():
        i1 = idx[m1.loc[idx]]
        i2 = idx[m2.loc[idx]]
        if len(i1):
            g1.loc[i1] = S.assign_304030(panel.loc[i1, "cp"])
        if len(i2):
            g2.loc[i2] = S.assign_304030(panel.loc[i2, "gs_rank_frac"])
    grp = pd.Series(np.nan, index=panel.index, dtype=object)
    grp[(g1 == 3) & (g2 == 1)] = "V"
    grp[(g1 == 1) & (g2 == 3)] = "G"
    return grp


# --- spreads ---------------------------------------------------------------
MAXFY = {1: 1989, 3: 1987, 5: 1985}   # sample-end boundary


def spreads(panel: pd.DataFrame, L: pd.DataFrame, grp: pd.Series) -> dict:
    sub = pd.DataFrame({"fy": panel["fy"], "permno": panel["permno"],
                        "grp": grp}).dropna(subset=["grp"])
    tfy, _ = S.group_stats(L, sub)
    out = {}
    for k in range(1, 6):
        cum = {}
        for (fy, g), row in tfy.iterrows():
            prod, ok = 1.0, True
            for j in range(1, k + 1):
                r = row[f"R_{j}"]
                if pd.isna(r):
                    ok = False
                    break
                prod *= 1 + r
            cum[(fy, g)] = prod - 1 if ok else np.nan
        sp = {}
        for fy in sorted(panel["fy"].unique()):
            v, gl = cum.get((fy, "V")), cum.get((fy, "G"))
            sp[fy] = (v - gl if v is not None and gl is not None
                      and not (pd.isna(v) or pd.isna(gl)) else np.nan)
        out[k] = sp
    return out


def hh_var(x: np.ndarray, maxlag: int) -> float:
    T = len(x)
    xc = x - x.mean()
    g = [np.mean(xc[:T - j] * xc[j:]) for j in range(maxlag + 1)]
    return (g[0] + 2 * sum(g[1:maxlag + 1])) / T


def tstat(series: np.ndarray, horizon: int) -> float:
    T = len(series)
    mu = series.mean()
    if horizon == 1:
        return mu / (series.std(ddof=1) / np.sqrt(T))
    return mu / np.sqrt(hh_var(series, horizon - 2))   # A12: 3yr->lag1, 5yr->lag3


# --- Table VI assembly -----------------------------------------------------
LABEL = {"P1": "C/P D9,10-D1,2", "P2": "C/PxGS 3,1-1,3",
         "P3": "B/M D10,9-D1,2"}


def build_table_6(panel, L):
    sp = {
        "P1": spreads(panel, L, pooled_decile_groups(panel, "cp")),
        "P2": spreads(panel, L, cpgs_corner_groups(panel)),
        "P3": spreads(panel, L, pooled_decile_groups(panel, "bm")),
    }
    cells, md_rows = {}, {P: {} for P in sp}
    for P in sp:
        for k in (1, 3, 5):
            yrs = list(range(1968, MAXFY[k] + 1))
            ser = np.array([sp[P][k][y] for y in yrs])
            avg = float(ser.mean())
            t = float(tstat(ser, k))
            for y in yrs:
                v = sp[P][k][y]
                if not pd.isna(v):
                    cells[f"{LABEL_PREFIX(P)} {y} {hor(k)}"] = round(v, 6)
                    md_rows[P].setdefault(y, {})[k] = v
            cells[f"{LABEL_PREFIX(P)} average {hor(k)}"] = round(avg, 6)
            cells[f"{LABEL_PREFIX(P)} t-stat {hor(k)}"] = round(t, 6)
            md_rows[P]["avg_" + str(k)] = avg
            md_rows[P]["t_" + str(k)] = t
    return cells, md_rows, sp


def LABEL_PREFIX(P):
    return f"{P} ({LABEL[P]})"


def hor(k):
    return f"{k}-Year"


# --- markdown --------------------------------------------------------------
def write_table_6(md_rows, path):
    yrs = list(range(1968, 1990))
    cols = ["Year"]
    for P in ["P1", "P2", "P3"]:
        cols += [f"{P}-1Y", f"{P}-3Y", f"{P}-5Y"]
    lines = ["# Table VI — Year-by-Year Returns: Value - Glamour (LSV 1994)",
             "",
             "Holding-horizon spread (value portfolio k-yr cumulative return "
             "minus glamour's), per formation, where k-yr cumulative = "
             "prod(1+R_1..R_k)-1 from the same equal-weighted sort machinery "
             "as Tables I-II. P1 = C/P pooled (9,10)-(1,2); P2 = (C/P3,GS1)-"
             "(C/P1,GS3); P3 = B/M pooled (9,10)-(1,2) [paper header/text/"
             "label; the P3 caption's 'single decile' wording is the "
             "inconsistent part]. Sample boundary = April 1990: 1-yr "
             "1968-89 (22), 3-yr 1968-87 (20), 5-yr 1968-85 (18). t-stats: "
             "1-yr iid; 3/5-yr Hansen-Hodrick (A12).", "",
             "| " + " | ".join(cols) + " |",
             "|" + "---|" * len(cols)]

    def c(v):
        return "-" if v is None or (isinstance(v, float) and pd.isna(v)) \
            else f"{v:.3f}"

    for y in yrs:
        row = [str(y)]
        for P in ["P1", "P2", "P3"]:
            d = md_rows[P].get(y, {})
            row += [c(d.get(1)), c(d.get(3)), c(d.get(5))]
        lines.append("| " + " | ".join(row) + " |")
    avg = ["Average"]
    tst = ["t-statistic"]
    for P in ["P1", "P2", "P3"]:
        avg += [f"{md_rows[P]['avg_1']:.3f}", f"{md_rows[P]['avg_3']:.3f}",
                f"{md_rows[P]['avg_5']:.3f}"]
        tst += [f"{md_rows[P]['t_1']:.3f}", f"{md_rows[P]['t_3']:.3f}",
                f"{md_rows[P]['t_5']:.3f}"]
    lines += ["| " + " | ".join(avg) + " |", "| " + " | ".join(tst) + " |"]
    path.write_text("\n".join(lines) + "\n")


# --- Figure 2 --------------------------------------------------------------
RECESSION_YEARS = {1969, 1970, 1973, 1974, 1980, 1981, 1982}


def fetch_ew_annual():
    cfg = get_clickhouse_config()
    c = Client(host=cfg["host"], port=int(cfg["port"]), user=cfg["user"],
               password=cfg["password"])
    rows = c.execute(
        "SELECT date, ewretd FROM crsp_202601.msi "
        "WHERE date >= '1968-05-01' AND date <= '1990-04-30' "
        "  AND substring(date,6,2) IN "
        "('05','06','07','08','09','10','11','12','01','02','03','04') "
        "ORDER BY date "
        "SETTINGS max_execution_time=120, max_rows_to_read=10000000000, "
        "timeout_before_checking_execution_speed=0")
    df = pd.DataFrame(rows, columns=["date", "ewretd"])
    df["y"] = df["date"].str[:4].astype(int)
    df["mo"] = df["date"].str[5:7].astype(int)
    # holding-year label: May..Apr -> year = calendar year if month>=5 else -1
    df["hy"] = np.where(df["mo"] >= 5, df["y"], df["y"] - 1)
    out = {}
    for hy, g in df.groupby("hy"):
        r = g["ewretd"].fillna(0.0)
        out[int(hy)] = float((1 + r).prod() - 1)
    return out


def make_figure_2(p2_1yr, ew_annual, path):
    yrs = list(range(1968, 1990))
    vals = [p2_1yr[y] for y in yrs]
    flags = []
    for y in yrs:
        if y in RECESSION_YEARS:
            flags.append("R")
        elif ew_annual.get(y, 0.0) < 0:
            flags.append("D")
        else:
            flags.append("")
    colors = []
    for y, f in zip(yrs, flags):
        if f == "R":
            colors.append("#d62728")
        elif f == "D":
            colors.append("#7f7f7f")
        else:
            colors.append("#1f77b4")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    bars = ax.bar(yrs, vals, color=colors, edgecolor="black", linewidth=0.4)
    ax.axhline(0, color="black", linewidth=0.8)
    for y, v, f in zip(yrs, vals, flags):
        ax.text(y, v + (0.01 if v >= 0 else -0.03), f, ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9, fontweight="bold")
    ax.set_xticks(yrs)
    ax.set_xticklabels([str(y) for y in yrs], rotation=90, fontsize=7)
    ax.set_ylabel("Annual buy-and-hold return: Value - Glamour (C/P x GS)")
    ax.set_title("Figure 2. Year-by-year returns: Value minus glamour "
                 "(C/P x GS classification)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#d62728", label="R = NBER recession year"),
                       Patch(color="#7f7f7f",
                             label="D = CRSP EW index declined that year"),
                       Patch(color="#1f77b4", label="other year")],
              loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8)
    fig.text(0.01, 0.01,
             "9 groups formed each April 1968-1989 by independent ascending "
             "30/40/30 sorts on C/P and GS. Value = (C/P3,GS1), glamour = "
             "(C/P1,GS3). Numbers are annual buy-and-hold V-G returns from end "
             "of April. R = NBER recession year; D = year the CRSP equally "
             "weighted index declined in nominal terms.",
             fontsize=7, wrap=True)
    fig.tight_layout(rect=[0, 0.06, 0.82, 1])
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return flags


# --- diagnostics -----------------------------------------------------------
def diagnostics(sp, md_rows, flags, ew_annual):
    print("\n" + "=" * 74)
    print("TABLE VI + FIGURE 2 DIAGNOSTICS")
    print("=" * 74)
    paper_avg = {"P1": {1: 0.079, 3: 0.357, 5: 0.841},
                 "P2": {1: 0.102, 3: 0.464, 5: 1.073},
                 "P3": {1: 0.063, 3: 0.344, 5: 0.842}}
    paper_t = {"P1": {1: 3.379, 3: 6.164, 5: 7.630},
               "P2": {1: 3.746, 3: 4.524, 5: 5.939},
               "P3": {1: 2.076, 3: 3.475, 5: 7.104}}
    print("\n[1] Average + t-stat vs paper:")
    for P in ["P1", "P2", "P3"]:
        for k in (1, 3, 5):
            a = md_rows[P][f"avg_{k}"]; t = md_rows[P][f"t_{k}"]
            print(f"    {P} {k}-yr: avg={a:.3f} (paper {paper_avg[P][k]:.3f})  "
                  f"t={t:.3f} (paper {paper_t[P][k]:.3f})  "
                  f"T={MAXFY[k]-1968+1}")

    # [2] per-year match vs paper grid
    print("\n[2] Year-by-year vs paper (tolerance 50%); biggest deviations:")
    ptable = {  # paper per-year (transcribed from content.md L2235-2256)
        "P1": {1: [0.022, 0.123, 0.135, -0.078, 0.155, 0.021, -0.007, 0.262,
                   0.174, 0.193, 0.048, -0.168, 0.039, 0.203, -0.032, 0.204,
                   0.192, 0.014, 0.108, 0.093, 0.092, -0.063],
               3: [0.287, 0.195, 0.246, 0.231, 0.319, 0.382, 0.496, 0.816,
                   0.673, 0.247, -0.106, -0.102, 0.745, 0.650, 0.338, 0.332,
                   0.552, 0.322, 0.339, 0.170],
               5: [0.474, 0.410, 0.428, 0.478, 0.693, 0.846, 1.343, 1.310,
                   1.468, 0.764, 0.272, 0.274, 1.225, 1.584, 1.253, 0.851,
                   0.888, 0.576]},
        "P2": {1: [0.144, 0.065, 0.002, -0.144, 0.134, 0.152, 0.069, 0.379,
                   0.217, 0.219, 0.039, -0.176, 0.110, 0.236, 0.118, 0.252,
                   0.052, -0.032, 0.196, 0.111, 0.089, 0.010],
               3: [0.153, -0.143, 0.160, 0.196, 0.362, 0.702, 0.650, 1.115,
                   0.715, 0.149, -0.072, 0.098, 1.246, 0.940, 0.539, 0.578,
                   0.641, 0.531, 0.427, 0.290],
               5: [0.267, 0.283, 0.356, 0.531, 0.932, 1.416, 1.597, 1.229,
                   1.235, 0.844, 0.581, 0.757, 2.000, 2.134, 1.886, 1.470,
                   1.092, 0.708]},
        "P3": {1: [0.098, 0.074, 0.023, -0.108, 0.098, 0.042, 0.050, 0.418,
                   0.132, 0.195, 0.037, -0.207, -0.034, 0.185, 0.240, 0.221,
                   0.043, -0.007, 0.051, 0.078, -0.037, -0.207],
               3: [0.201, 0.070, 0.032, 0.156, 0.328, 0.450, 0.642, 1.034,
                   0.727, 0.181, -0.264, -0.123, 1.066, 0.810, 0.589, 0.256,
                   0.324, 0.237, 0.149, 0.015],
               5: [0.344, 0.303, 0.279, 0.463, 0.784, 0.925, 1.726, 1.182,
                   0.993, 0.614, 0.286, 0.569, 1.676, 1.955, 1.477, 0.648,
                   0.640, 0.299]},
    }
    total = matched = 0
    devs = []
    for P in ["P1", "P2", "P3"]:
        for k in (1, 3, 5):
            base = 1968
            for i, pv in enumerate(ptable[P][k]):
                y = base + i
                mv = sp[P][k].get(y, np.nan)
                if pd.isna(mv):
                    continue
                total += 1
                denom = max(abs(pv), 0.01)
                rel = abs(mv - pv) / denom
                if rel <= 0.50:
                    matched += 1
                devs.append((rel, P, k, y, pv, mv))
    devs.sort(reverse=True)
    print(f"    matched {matched}/{total} within 50%")
    print("    biggest 6 deviations (rel, panel, hor, year, paper, mine):")
    for rel, P, k, y, pv, mv in devs[:6]:
        print(f"      {rel:.2f}  {P} {k}Y {y}: paper {pv:+.3f} mine {mv:+.3f}")

    # [3] value beats glamour in every 5-yr window?
    print("\n[3] Value beats glamour in every 5-Year window (all panels)?")
    for P in ["P1", "P2", "P3"]:
        ok = all(sp[P][5][y] > 0 for y in range(1968, 1986)
                 if not pd.isna(sp[P][5][y]))
        npos = sum(1 for y in range(1968, 1986)
                   if not pd.isna(sp[P][5][y]) and sp[P][5][y] > 0)
        print(f"    {P}: {ok}  ({npos}/18 positive)")

    # figure flags
    rec = [y for y in range(1968, 1990) if y in RECESSION_YEARS]
    dyears = [y for y in range(1968, 1990)
              if y not in RECESSION_YEARS and ew_annual.get(y, 0) < 0]
    print(f"\n[Fig2] recession(R) years={rec}")
    print(f"       EW-decline(D) years={dyears}")
    print("=" * 74)


def main():
    RES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    L = S.returns_long(panel)
    print(f"Loaded panel {panel.shape}")

    cells, md_rows, sp = build_table_6(panel, L)
    out = {n: cells[n] for n in T6_NAMES if n in cells}
    (RES / "table_VI_cells.json").write_text(json.dumps(out, indent=2))
    print(f"Emitted table_VI_cells.json: {len(out)} / {len(T6_NAMES)}")

    write_table_6(md_rows, RES / "table_6.md")
    print("Wrote results/table_6.md")

    ew = fetch_ew_annual()
    make_figure_2(sp["P2"][1], ew, RES / "figure_2.png")
    print("Wrote results/figure_2.png")

    diagnostics(sp, md_rows, None, ew)


if __name__ == "__main__":
    main()
