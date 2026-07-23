"""
LSV (1994) "Contrarian Investment, Extrapolation, and Risk" — Tables I, II, III
(+ Figure 1). Reads data/panel.parquet (built by main.py) and emits:
    results/table_1.md, table_2.md, table_3.md
    results/table_I_cells.json, table_II_cells.json, table_III_cells.json
    results/figure_1.png
Metric names in the cells JSONs match preparations/tables_to_replicate.json
exactly. Run:
    cd <internal>/rep-it-up && \
        uv run python replications/contrarian_investment/src/tables.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # for sortlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from utils.paths import paper_layout  # noqa: E402
import sortlib as S  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
PANEL_PATH = LAYOUT.data_path("panel.parquet")
RES = LAYOUT.results_dir
TARGETS = json.loads(
    LAYOUT.preparations_path("tables_to_replicate.json").read_text())
TARGET_NAMES = {t["id"]: {m["name"] for m in t["metrics"]}
                for t in TARGETS["tables"]}

STATS_FULL = [f"R_{k}" for k in range(1, 6)] + ["AR", "CR_5", "SAAR"]
STATS_SUMMARY = ["AR", "CR_5", "SAAR"]
ROW_LABEL = {**{f"R_{k}": f"R_{k}" for k in range(1, 6)},
             "AR": "AR", "CR_5": "CR_5", "SAAR": "SAAR"}

# signal metadata: var -> (signal column, display name)
SIG = {"bm": "bm", "cp": "cp", "ep": "ep", "gs": "gs_rank_frac"}
DISP = {"bm": "B/M", "cp": "C/P", "ep": "E/P", "gs": "GS"}

# Table I panels: (letter, var)
TABLE_I_PANELS = [("A", "bm"), ("B", "cp"), ("C", "ep"), ("D", "gs")]
# Table II/III pairs: (letter, label, var1, var2, glamour_corner, value_corner)
PAIRS = [
    ("A", "C/PxGS",  "cp", "gs", (1, 3), (3, 1)),
    ("B", "E/PxGS",  "ep", "gs", (1, 3), (3, 1)),
    ("C", "B/MxGS",  "bm", "gs", (1, 3), (3, 1)),
    ("D", "E/PxB/M", "ep", "bm", (1, 1), (3, 3)),
    ("E", "B/MxC/P", "bm", "cp", (1, 1), (3, 3)),
]


def valid_mask(df: pd.DataFrame, var: str) -> pd.Series:
    if var == "bm":
        return (df["be_valid"] == 1) & df["bm"].notna()
    if var == "cp":
        return df["cp_pos"] == 1
    if var == "ep":
        return df["ep_pos"] == 1
    if var == "gs":
        return df["gs_rank_frac"].notna()
    raise ValueError(var)


# --- Table I ---------------------------------------------------------------
def compute_table_I(panel: pd.DataFrame, L: pd.DataFrame) -> dict:
    res = {}
    for P, var in TABLE_I_PANELS:
        vm = valid_mask(panel, var)
        dec = pd.Series(pd.NA, index=panel.index, dtype="Int64")
        for _, idx in panel.groupby("fy").groups.items():
            ii = idx[vm.loc[idx]]
            if len(ii) >= 10:
                dec.loc[ii] = S.assign_deciles(panel.loc[ii, SIG[var]], 10)
        grp = pd.DataFrame({"fy": panel["fy"], "permno": panel["permno"],
                            "grp": dec}).dropna(subset=["grp"])
        grp["grp"] = grp["grp"].astype(int)
        tfy, cnt = S.group_stats(L, grp)
        tv = S.table_values(tfy)
        res[P] = {"var": var, "label": DISP[var], "tv": tv, "tfy": tfy,
                  "cnt": cnt, "n_assigned": int(len(grp.drop_duplicates(['fy','permno'])))}
    return res


# --- Table II / III --------------------------------------------------------
def compute_pairs(panel: pd.DataFrame, L: pd.DataFrame) -> dict:
    res = {}
    for P, lab, v1, v2, glam, val in PAIRS:
        g1 = pd.Series(pd.NA, index=panel.index, dtype="Int64")
        g2 = pd.Series(pd.NA, index=panel.index, dtype="Int64")
        m1, m2 = valid_mask(panel, v1), valid_mask(panel, v2)
        for _, idx in panel.groupby("fy").groups.items():
            i1 = idx[m1.loc[idx]]
            i2 = idx[m2.loc[idx]]
            if len(i1):
                g1.loc[i1] = S.assign_304030(panel.loc[i1, SIG[v1]])
            if len(i2):
                g2.loc[i2] = S.assign_304030(panel.loc[i2, SIG[v2]])
        both = g1.notna() & g2.notna()
        grp = pd.DataFrame({
            "fy": panel["fy"][both], "permno": panel["permno"][both],
            "grp": g1[both].astype(str) + "_" + g2[both].astype(str),
        })
        tfy, cnt = S.group_stats(L, grp)
        tv = S.table_values(tfy)
        res[P] = {"label": lab, "v1": v1, "v2": v2, "glam": glam, "val": val,
                  "tv": tv, "tfy": tfy, "cnt": cnt}
    return res


# --- cells JSON builders ---------------------------------------------------
def cells_table_I(res: dict) -> dict:
    cells = {}
    for P, r in res.items():
        lab = r["label"]
        tv = r["tv"]
        for d in range(1, 11):
            if d not in tv.index:
                continue
            for stat in STATS_FULL:
                name = f"Panel {P} ({lab}) decile {d} {stat}"
                cells[name] = round(float(tv.loc[d, stat]), 6)
    return cells


def cells_pairs(res: dict, stats: list) -> dict:
    cells = {}
    for P, r in res.items():
        lab, v1n, v2n = r["label"], DISP[r["v1"]], DISP[r["v2"]]
        tv = r["tv"]
        for a in (1, 2, 3):
            for b in (1, 2, 3):
                key = f"{a}_{b}"
                if key not in tv.index:
                    continue
                for stat in stats:
                    name = (f"Panel {P} ({lab}) cell ({v1n}{a},{v2n}{b}) {stat}")
                    cells[name] = round(float(tv.loc[key, stat]), 6)
        g = f"{r['glam'][0]}_{r['glam'][1]}"
        v = f"{r['val'][0]}_{r['val'][1]}"
        if g in tv.index and v in tv.index:
            cells[f"Panel {P} ({lab}) AR spread value-glamour"] = \
                round(float(tv.loc[v, "AR"] - tv.loc[g, "AR"]), 6)
            cells[f"Panel {P} ({lab}) SAAR spread value-glamour"] = \
                round(float(tv.loc[v, "SAAR"] - tv.loc[g, "SAAR"]), 6)
    return cells


def emit_json(cells: dict, table_id: str, path: Path) -> int:
    targets = TARGET_NAMES[table_id]
    out = {k: cells[k] for k in targets if k in cells}
    path.write_text(json.dumps(out, indent=2))
    return len(out)


# --- markdown writers ------------------------------------------------------
def _fmt(x, nd=3):
    return "-" if pd.isna(x) else f"{x:.{nd}f}"


def md_decile_table(tv: pd.DataFrame, direction: str) -> str:
    cols = list(range(1, 11))
    head = "| Statistic | " + " | ".join(f"D{c}" for c in cols) + " |"
    sep = "|" + "---|" * (len(cols) + 1)
    rows = [head, sep]
    for stat in STATS_FULL:
        rows.append("| " + ROW_LABEL[stat] + " | " +
                    " | ".join(_fmt(tv.loc[c, stat]) if c in tv.index else "-"
                               for c in cols) + " |")
    return f"*({direction})*\n\n" + "\n".join(rows)


def md_cell_table(tv: pd.DataFrame, v1n: str, v2n: str,
                  stats: list) -> str:
    cells = [(a, b) for a in (1, 2, 3) for b in (1, 2, 3)]
    col_labels = [f"({v1n}{a},{v2n}{b})" for a, b in cells]
    head = "| Statistic | " + " | ".join(col_labels) + " |"
    sep = "|" + "---|" * (len(cells) + 1)
    rows = [head, sep]
    for stat in stats:
        vals = []
        for a, b in cells:
            key = f"{a}_{b}"
            vals.append(_fmt(tv.loc[key, stat]) if key in tv.index else "-")
        rows.append("| " + ROW_LABEL[stat] + " | " + " | ".join(vals) + " |")
    return "\n".join(rows)


def member_footnote(cnt: pd.Series, grp_labels) -> str:
    # cnt indexed (fy, grp) -> per grp min/median members across formations
    parts = []
    for g in grp_labels:
        try:
            s = cnt.xs(g, level="grp")
        except KeyError:
            continue
        parts.append(f"{g}: min={int(s.min())}, median={int(s.median())}, "
                     f"n_formations={len(s)}")
    return "; ".join(parts)


def write_table_1(res: dict, path: Path) -> None:
    out = ["# Table I — Univariate decile sorts (LSV 1994)",
           "",
           "Decile portfolios formed at the end of each April, 1968-1989 "
           "(22 formations), ascending on the signal within the valid subset "
           "(equal-count). Returns are equally-weighted annual buy-and-hold; "
           "table entries are means across the 22 formations. B/M, C/P, E/P are "
           "ordered Glamour (D1) -> Value (D10); GS is ordered Value (D1, low "
           "growth) -> Glamour (D10, high growth).", ""]
    titles = {"A": "Panel A — B/M (Glamour -> Value)",
              "B": "Panel B — C/P (Glamour -> Value)",
              "C": "Panel C — E/P (Glamour -> Value)",
              "D": "Panel D — GS (Value -> Glamour)"}
    directions = {"A": "glamour -> value", "B": "glamour -> value",
                  "C": "glamour -> value", "D": "value -> glamour"}
    foot = ["", "## Formation counts (members per decile, across formations)", ""]
    for P, _ in TABLE_I_PANELS:
        r = res[P]
        out += [f"## {titles[P]}", "",
                md_decile_table(r["tv"], directions[P]), ""]
        foot.append(f"- **Panel {P} ({r['label']})**: " +
                    member_footnote(r["cnt"], range(1, 11)))
    out += foot
    path.write_text("\n".join(out) + "\n")


def write_pairs(res: dict, path: Path, stats: list, heading: str,
                intro: str) -> None:
    out = [heading, "", intro, ""]
    for P, lab, v1, v2, glam, val in PAIRS:
        r = res[P]
        out += [f"## Panel {P} — {lab} "
                f"(glamour corner {r['glam']}, value corner {r['val']})", "",
                md_cell_table(r["tv"], DISP[v1], DISP[v2], stats), ""]
    out += ["## Formation counts (members per cell, across formations)", ""]
    for P, lab, v1, v2, *_ in PAIRS:
        r = res[P]
        labels = [f"{a}_{b}" for a in (1, 2, 3) for b in (1, 2, 3)]
        out.append(f"- **Panel {P} ({lab})**: " +
                   member_footnote(r["cnt"], labels))
    path.write_text("\n".join(out) + "\n")


# --- Figure 1 --------------------------------------------------------------
def make_figure_1(res_II: dict, path: Path) -> None:
    r = res_II["A"]  # C/P x GS
    tv = r["tv"]
    cp_groups = [1, 2, 3]
    gs_groups = [1, 2, 3]
    corners = {(1, 3), (3, 1)}          # annotated below -> skip their bar labels
    x = np.arange(len(cp_groups))
    width = 0.26
    fig, ax = plt.subplots(figsize=(9, 5.5))
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]
    for j, gs in enumerate(gs_groups):
        vals = [float(tv.loc[f"{cp}_{gs}", "CR_5"])
                if f"{cp}_{gs}" in tv.index else np.nan for cp in cp_groups]
        bars = ax.bar(x + (j - 1) * width, vals, width,
                      label=f"GS group {gs}", color=colors[j])
        for cp, b, v in zip(cp_groups, bars, vals):
            if not np.isnan(v) and (cp, gs) not in corners:
                ax.text(b.get_x() + b.get_width() / 2, v + 0.02, f"{v:.2f}",
                        ha="center", va="bottom", fontsize=7)
    # annotate glamour / value corners
    glam = tv.loc["1_3", "CR_5"]   # (C/P1, GS3)
    val = tv.loc["3_1", "CR_5"]    # (C/P3, GS1)
    ax.annotate(f"glamour (C/P1,GS3) = {glam:.2f}", xy=(0 + width, glam),
                xytext=(0.45, 1.55), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.annotate(f"value (C/P3,GS1) = {val:.2f}", xy=(2 - width, val),
                xytext=(1.3, 2.05), fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.set_ylim(0, max(val, glam) + 0.95)
    ax.set_xticks(x)
    ax.set_xticklabels([f"C/P group {g}\n(bottom→top 30/40/30)"
                        for g in cp_groups])
    ax.set_ylabel("Compounded 5-year postformation return (CR_5)")
    ax.set_title("Figure 1. Compounded 5-year return for portfolios formed on "
                 "C/P and GS")
    ax.legend(title="Growth-in-sales (GS)", fontsize=8)
    fig.text(0.01, 0.01,
             "9 groups formed each April 1968-1989; independent ascending "
             "30/40/30 sorts on C/P and GS. CR_5 = compounded 5-year return "
             "with annual rebalancing (formation-mean across 22 cohorts).",
             fontsize=7, wrap=True)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(path, dpi=150)
    plt.close(fig)


# --- diagnostics -----------------------------------------------------------
def diagnostics(res_I: dict, res_II: dict, res_III: dict) -> None:
    print("\n" + "=" * 74)
    print("TABLE DIAGNOSTICS — LSV (1994) Tables I, II, III")
    print("=" * 74)

    # [1] headline spreads vs paper
    paper = {
        "I_AR_spread": {"A": 0.105, "B": 0.110, "C": 0.076, "D": -0.068},
        "I_SAAR_D1": {"A": -0.043, "B": -0.049},
        "I_SAAR_D10": {"A": 0.035, "B": 0.039},
    }
    print("\n[1] Headline spreads vs paper")
    print("  Table I (D10-D1 for B/M,C/P,E/P; D1-D10=value-glamour for GS shown as D10-D1):")
    for P, var in TABLE_I_PANELS:
        tv = res_I[P]["tv"]
        spread = tv.loc[10, "AR"] - tv.loc[1, "AR"]
        note = "(glamour-value)" if var == "gs" else "(value-glamour)"
        print(f"    Panel {P} ({DISP[var]}): AR D1={tv.loc[1,'AR']:.3f} "
              f"D10={tv.loc[10,'AR']:.3f} D10-D1={spread:.3f} {note} "
              f"[paper {paper['I_AR_spread'][P]:+.3f} glamour-value]")
    for tbl, res in [("II", res_II), ("III", res_III)]:
        r = res["A"]
        g = f"{r['glam'][0]}_{r['glam'][1]}"; v = f"{r['val'][0]}_{r['val'][1]}"
        print(f"  Table {tbl} Panel A (C/PxGS): AR glamour={r['tv'].loc[g,'AR']:.3f} "
              f"value={r['tv'].loc[v,'AR']:.3f} spread={r['tv'].loc[v,'AR']-r['tv'].loc[g,'AR']:.3f} | "
              f"SAAR glamour={r['tv'].loc[g,'SAAR']:.3f} value={r['tv'].loc[v,'SAAR']:.3f} "
              f"spread={r['tv'].loc[v,'SAAR']-r['tv'].loc[g,'SAAR']:.3f}")
    print("    [paper II: AR 0.114/0.221 spread 0.107; SAAR -0.033/0.054 spread 0.087]")
    print("    [paper III: AR 0.106/0.184 spread 0.078; SAAR -0.039/0.048 spread 0.087]")

    # [2] monotonicity of AR across Table I deciles
    print("\n[2] AR monotonicity across Table I deciles (D1..D10):")
    for P, var in TABLE_I_PANELS:
        tv = res_I[P]["tv"]
        ar = [tv.loc[d, "AR"] for d in range(1, 11)]
        inc = all(ar[i] <= ar[i + 1] for i in range(9))
        dec = all(ar[i] >= ar[i + 1] for i in range(9))
        nviol_inc = sum(1 for i in range(9) if ar[i] > ar[i + 1])
        nviol_dec = sum(1 for i in range(9) if ar[i] < ar[i + 1])
        expect = "decreasing" if var == "gs" else "increasing"
        if expect == "increasing":
            status = "MONOTONE INC" if inc else f"{nviol_inc} violations of inc"
        else:
            status = "MONOTONE DEC" if dec else f"{nviol_dec} violations of dec"
        print(f"    Panel {P} ({DISP[var]}): expect {expect}; {status}; "
              f"AR={['%.3f'%a for a in ar]}")

    # [3] non-empty bins/cells + median members
    print("\n[3] Coverage (non-empty bins/cells) & median members:")
    for P, var in TABLE_I_PANELS:
        tv = res_I[P]["tv"]
        ndec = sum(1 for d in range(1, 11) if d in tv.index)
        med = res_I[P]["cnt"].groupby("grp").median().median()
        print(f"    Table I Panel {P} ({DISP[var]}): {ndec}/10 non-empty deciles, "
              f"median members/decile~{med:.0f}")
    for tbl, res in [("II", res_II), ("III", res_III)]:
        for P, lab, *_ in PAIRS:
            r = res[P]
            ncell = sum(1 for a in (1, 2, 3) for b in (1, 2, 3)
                        if f"{a}_{b}" in r["tv"].index)
            med = r["cnt"].groupby("grp").median().median()
            print(f"    Table {tbl} Panel {P} ({lab}): {ncell}/9 non-empty cells, "
                  f"median members/cell~{med:.0f}")

    # [4] full Table I arrays
    print("\n[4] Full Table I per-panel arrays:")
    for P, var in TABLE_I_PANELS:
        tv = res_I[P]["tv"]
        print(f"  Panel {P} ({DISP[var]}):")
        for stat in STATS_FULL:
            vals = [_fmt(tv.loc[d, stat]) for d in range(1, 11)]
            print(f"    {stat:5s}: " + " ".join(f"{v:>6s}" for v in vals))

    # [5] cells-JSON counts
    print("\n[5] Cells-JSON counts (emitted / target metrics):")
    for tid, fname in [("table_I", "table_I_cells.json"),
                       ("table_II", "table_II_cells.json"),
                       ("table_III", "table_III_cells.json")]:
        p = RES / fname
        n = len(json.loads(p.read_text()))
        print(f"    {fname}: {n} / {len(TARGET_NAMES[tid])}")
    print("=" * 74)


def main() -> None:
    RES.mkdir(parents=True, exist_ok=True)
    panel = pd.read_parquet(PANEL_PATH)
    L = S.returns_long(panel)
    print(f"Loaded panel: {panel.shape}")

    print("Computing Table I ...")
    res_I = compute_table_I(panel, L)

    print("Computing Table II ...")
    res_II = compute_pairs(panel, L)

    print("Computing Table III (largest-50% subsample) ...")
    big = pd.Series(False, index=panel.index)
    for _, idx in panel.groupby("fy").groups.items():
        me = panel.loc[idx, "me_apr"]
        med = me.median()
        big.loc[idx] = (me >= med) & me.notna()
    psub = panel[big].reset_index(drop=True)
    print(f"  top-50% subsample: {len(psub)} of {len(panel)} rows")
    res_III = compute_pairs(psub, L)

    # markdown tables
    write_table_1(res_I, RES / "table_1.md")
    write_pairs(res_II, RES / "table_2.md", STATS_FULL,
                "# Table II — Two-dimensional independent 30/40/30 sorts "
                "(LSV 1994)",
                "Independent 30/40/30 sorts on two variables; 9 intersection "
                "portfolios formed each April 1968-1989. Returns equally-"
                "weighted annual buy-and-hold; entries are means across the 22 "
                "formations. Glamour/value corners: A/B/C glamour=(1,3), "
                "value=(3,1); D/E glamour=(1,1), value=(3,3).")
    write_pairs(res_III, RES / "table_3.md", STATS_SUMMARY,
                "# Table III — Two-dimensional sorts, largest 50% of firms "
                "(LSV 1994)",
                "Same 30/40/30 machinery as Table II, but the sorting universe "
                "each formation is the largest 50% of the formation universe by "
                "April market equity (breakpoint = within-formation median "
                "me_apr); breakpoints recomputed within the subsample. Rows: "
                "AR, CR_5, SAAR (formation-means).")

    # cells JSONs (intersect with target metric names)
    cI = cells_table_I(res_I)
    cII = cells_pairs(res_II, STATS_FULL)
    cIII = cells_pairs(res_III, STATS_SUMMARY)
    nI = emit_json(cI, "table_I", RES / "table_I_cells.json")
    nII = emit_json(cII, "table_II", RES / "table_II_cells.json")
    nIII = emit_json(cIII, "table_III", RES / "table_III_cells.json")
    print(f"Emitted cells JSON: I={nI}, II={nII}, III={nIII}")

    # figure
    make_figure_1(res_II, RES / "figure_1.png")
    print("Wrote results/figure_1.png")

    diagnostics(res_I, res_II, res_III)


if __name__ == "__main__":
    main()
