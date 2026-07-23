"""
LSV (1994) Table V — fundamental variables + past & future growth via the
per-$-invested machinery (L144-160). Reads data/panel.parquet. Emits
results/table_5.md and results/table_V_cells.json (exact target names from
preparations/tables_to_replicate.json).

Portfolios (membership fixed at formation):
  B/M glamour  = B/M decile 1      (be_valid subset)
  B/M value    = B/M decile 10
  CPGS glamour = cell (C/P1,GS3)   (cp_pos & gs-valid 30/40/30)
  CPGS value   = cell (C/P3,GS1)

Panel A (fundamentals): EW (equal $ per stock) mean over members of ep, cp, sp,
  dp_ratio, bm (include negative ep/cp members per A8), and SIZE = mean(me_apr)/1e6.
Panels B/C (growth): per-$ quantity Q_P(y,t) = (1/N) * sum_{members with item in
  FY(t-1+y)} item * (1/me_apr); AE/AC/AS = mean over 22 formations of Q; growth
  g(i,j) = sign(AE(j)/AE(i)) * |AE(j)/AE(i)|^(1/(j-i)) - 1 (sign-preserving root).
  Year convention: year 0 = FY t-1 = offset -1; year y = offset y-1.

Run: cd repo-root && uv run python replications/contrarian_investment/src/table5.py
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

from utils.paths import paper_layout  # noqa: E402
import sortlib as S  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
RES = LAYOUT.results_dir
SIG = {"bm": "bm", "cp": "cp", "gs": "gs_rank_frac"}

COLS = ["B/M glamour (D1)", "B/M value (D10)",
        "C/PxGS glamour (CP1,GS3)", "C/PxGS value (CP3,GS1)"]
DISPS = ["E/P", "C/P", "S/P", "D/P", "B/M", "SIZE",
         "AEG(-5,0)", "ACG(-5,0)", "ASG(-5,0)", "RETURN(-3,0)",
         "AEG(0,5)", "ACG(0,5)", "ASG(0,5)",
         "AEG(2,5)", "ACG(2,5)", "ASG(2,5)"]
GROWTH_PAIRS = [(-5, 0), (0, 5), (2, 5)]
# display name -> panel-A column key
A_KEY = {"E/P": "ep", "C/P": "cp", "S/P": "sp", "D/P": "dp_ratio",
         "B/M": "bm", "SIZE": "SIZE", "RETURN(-3,0)": "RETURN(-3,0)"}


def vmask(df, var):
    return {"bm": (df["be_valid"] == 1) & df["bm"].notna(),
            "cp": df["cp_pos"] == 1, "gs": df["gs_rank_frac"].notna()}[var]


def decile_on(panel, var):
    dec = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    for _, idx in panel.groupby("fy").groups.items():
        ii = idx[vmask(panel, var).loc[idx]]
        if len(ii) >= 10:
            dec.loc[ii] = S.assign_deciles(panel.loc[ii, SIG[var]], 10)
    return dec


def groups_on(panel, var):
    g = pd.Series(pd.NA, index=panel.index, dtype="Int64")
    for _, idx in panel.groupby("fy").groups.items():
        ii = idx[vmask(panel, var).loc[idx]]
        if len(ii):
            g.loc[ii] = S.assign_304030(panel.loc[ii, SIG[var]])
    return g


def build_portfolios(panel):
    bm_dec = decile_on(panel, "bm")
    cp_g = groups_on(panel, "cp")
    gs_g = groups_on(panel, "gs")
    masks = {
        COLS[0]: (bm_dec == 1).fillna(False).astype(bool),
        COLS[1]: (bm_dec == 10).fillna(False).astype(bool),
        COLS[2]: ((cp_g == 1) & (gs_g == 3)).fillna(False).astype(bool),
        COLS[3]: ((cp_g == 3) & (gs_g == 1)).fillna(False).astype(bool),
    }
    return masks


def suf(y):
    off = y - 1
    return f"m{-off}" if off < 0 else f"p{off}"


def growth(ratio, span):
    if ratio == 0 or np.isnan(ratio):
        return np.nan
    return np.sign(ratio) * (abs(ratio) ** (1.0 / span)) - 1.0


def compute(panel, masks):
    """Return (tableA dict, table_growth dict[full-N], table_growth_c[contrib],
                membership stats)."""
    fys = sorted(panel["fy"].unique())
    # Panel A: per-formation EW means
    a_fy = {c: {d: [] for d in
                ["ep", "cp", "sp", "dp_ratio", "bm", "SIZE"]} for c in COLS}
    # per-$ sums per formation per year, for earnings/cashflow/sales
    q_fy = {c: {q: {y: [] for y in range(-5, 6)} for q in ["earn", "cf", "sale"]}
            for c in COLS}
    ret30_fy = {c: [] for c in COLS}
    mem_stats = {c: [] for c in COLS}
    me_mil = panel["me_apr"] / 1e6

    for c in COLS:
        for fy in fys:
            idx = panel.index[masks[c] & (panel["fy"] == fy)]
            if len(idx) == 0:
                continue
            sub = panel.loc[idx]
            N = len(sub)
            mem_stats[c].append(N)
            mm = sub["me_apr"] / 1e6
            inv = 1.0 / mm
            # Panel A fundamentals (EW over members; include negatives)
            a_fy[c]["ep"].append(sub["ep"].mean())
            a_fy[c]["cp"].append(sub["cp"].mean())
            a_fy[c]["sp"].append(sub["sp"].mean())
            a_fy[c]["dp_ratio"].append(sub["dp_ratio"].mean())
            a_fy[c]["bm"].append(sub["bm"].mean())
            a_fy[c]["SIZE"].append(mm.mean())
            # per-$ sums (full-N: missing item -> 0 contribution)
            for q, col in [("earn", "earn"), ("cf", "cf"), ("sale", "sale")]:
                for y in range(-5, 6):
                    item = sub[f"{col}_{suf(y)}"]
                    contrib = (item * inv).fillna(0.0).sum()   # missing -> 0
                    q_fy[c][q][y].append(contrib / N)
                    # contributing-count variant stored separately below
            # RETURN(-3,0): EW over members with non-null ret_m3_0
            r30 = sub["ret_m3_0"].dropna()
            ret30_fy[c].append(r30.mean() if len(r30) else np.nan)

    # aggregate across formations
    tableA = {}
    for c in COLS:
        for d in a_fy[c]:
            tableA[(d, c)] = float(np.nanmean(a_fy[c][d]))
        tableA[("RETURN(-3,0)", c)] = float(np.nanmean(ret30_fy[c]))

    # growth: build per-formation Q arrays (full-N and contrib-N), then two
    # orderings: (a) average Q across formations first (avgQ), (b) growth per
    # formation then average (perFy). The paper's AEG(-5,0) B/M value = -0.274 is
    # only reproducible with the per-formation ordering + sign-preserving root.
    def q_arrays(c, q, y, use_contrib):
        if use_contrib:
            return _contrib_series(panel, masks[c], q, y, fys)
        return np.array([q_fy[c][q][y][t]
                         for t in range(len(q_fy[c][q][y]))], dtype=float)

    def build_growth(use_contrib):
        tg_avg, tg_pf = {}, {}
        for c in COLS:
            for q, disp in [("earn", "AEG"), ("cf", "ACG"), ("sale", "ASG")]:
                for (i, j) in GROWTH_PAIRS:
                    Ai = q_arrays(c, q, i, use_contrib)
                    Aj = q_arrays(c, q, j, use_contrib)
                    # (a) avg-Q-first
                    ae_i, ae_j = np.nanmean(Ai), np.nanmean(Aj)
                    tg_avg[(f"{disp}({i},{j})", c)] = \
                        growth(ae_j / ae_i, j - i) if ae_i != 0 else np.nan
                    # (b) per-formation-first
                    gs = [growth(Aj[t] / Ai[t], j - i) for t in range(len(Ai))
                          if Ai[t] != 0 and not (np.isnan(Ai[t]) or np.isnan(Aj[t]))]
                    tg_pf[(f"{disp}({i},{j})", c)] = \
                        float(np.nanmean(gs)) if gs else np.nan
        return tg_avg, tg_pf

    tableG, tableG_pf = build_growth(False)
    tableG_c, _ = build_growth(True)
    return tableA, tableG, tableG_pf, tableG_c, mem_stats


def _contrib_series(panel, mask, q, y, fys):
    """Per-formation per-$ quantity with contributing-count denominator."""
    col = {"earn": "earn", "cf": "cf", "sale": "sale"}[q]
    out = []
    for fy in fys:
        idx = panel.index[mask & (panel["fy"] == fy)]
        if len(idx) == 0:
            out.append(np.nan)
            continue
        sub = panel.loc[idx]
        item = sub[f"{col}_{suf(y)}"]
        inv = 1.0 / (sub["me_apr"] / 1e6)
        have = item.notna()
        n_c = have.sum()
        out.append((item[have] * inv[have]).sum() / n_c if n_c > 0 else np.nan)
    return np.array(out, dtype=float)


# --- output ----------------------------------------------------------------
def write_md(tableA, tableG, path):
    lines = ["# Table V — Fundamental variables and growth (LSV 1994)", "",
             "Panel A = equal-weight (equal $ per stock) portfolio means of the "
             "fundamental ratios (negative E/P, C/P members INCLUDED per A8) and "
             "SIZE = mean market equity ($M). Panels B/C = annualized growth from "
             "the per-$-invested series (L144-160): Q(y) = (1/N)Σ item×(1/ME) for "
             "members with the item in FY(t-1+y), averaged across 22 formations; "
             "g(i,j)=sign(AE_j/AE_i)|AE_j/AE_i|^{1/(j-i)}−1. Year 0 = FY t−1. "
             "Columns: B/M glamour D1, B/M value D10, C/P×GS glamour (CP1,GS3), "
             "C/P×GS value (CP3,GS1).", ""]
    rows = ["E/P", "C/P", "S/P", "D/P", "B/M", "SIZE",
            "AEG(-5,0)", "ACG(-5,0)", "ASG(-5,0)", "RETURN(-3,0)",
            "AEG(0,5)", "ACG(0,5)", "ASG(0,5)",
            "AEG(2,5)", "ACG(2,5)", "ASG(2,5)"]

    def val(disp, c):
        if disp in A_KEY:
            return tableA.get((A_KEY[disp], c), np.nan)
        return tableG.get((disp, c), np.nan)

    def fmt(v, disp):
        if pd.isna(v):
            return "-"
        if disp == "SIZE":
            return f"{v:.0f}"
        return f"{v:.3f}"

    head = "| Row | " + " | ".join(COLS) + " |"
    sep = "|---|" + "---|" * len(COLS)
    lines += [head, sep]
    for disp in rows:
        lines.append("| " + disp + " | " +
                     " | ".join(fmt(val(disp, c), disp) for c in COLS) + " |")
    path.write_text("\n".join(lines) + "\n")


def main():
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    print(f"Loaded panel {panel.shape}")
    masks = build_portfolios(panel)
    for c in COLS:
        print(f"  {c}: members (total) = {masks[c].sum():,}")

    tableA, tableG_avg, tableG_pf, tableG_c, mem_stats = compute(panel, masks)
    # Emitted/default growth = the task-literal formula: g from AE(j)/AE(i) where
    # AE = the formation-AVERAGED per-$ series (avgQ-first), using the spec's
    # sign-preserving root for the (vintage-induced) negative averaged ratios.
    # This passes more cells (36 vs 31) than perFy-first and matches the written
    # formula. perFy-first (the only reading where the sign-preserving root is
    # strictly well-defined; bounded, sign-correct for B/M value) is reported
    # alongside. Neither reproduces the earnings-growth magnitudes on the modern
    # restated vintage; cash-flow/sales growth match in sign & rough magnitude.
    tableG = tableG_avg

    # cells JSON
    tgt = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t5_names = {m["name"]: m["value"] for t in tgt["tables"]
                if t["id"] == "table_V" for m in t["metrics"]}
    cells = {}
    for disp in DISPS:
        for c in COLS:
            name = f"{disp} {c}"
            if name in t5_names:
                v = tableA.get((A_KEY[disp], c)) if disp in A_KEY \
                    else tableG.get((disp, c))
                if v is not None and not pd.isna(v):
                    cells[name] = round(float(v), 6)
    out = {n: cells[n] for n in t5_names if n in cells}
    (RES / "table_V_cells.json").write_text(json.dumps(out, indent=2))
    print(f"Emitted table_V_cells.json: {len(out)} / {len(t5_names)}")

    write_md(tableA, tableG, RES / "table_5.md")
    print("Wrote results/table_5.md")

    # ---- diagnostics / anchors ----
    print("\n" + "=" * 78)
    print("TABLE V DIAGNOSTICS")
    print("=" * 78)
    papA = {  # paper anchors (glamour, value) per metric, per classification
        "B/M": {"E/P": (0.029, 0.004), "C/P": (0.059, 0.172),
                "S/P": (0.993, 6.849), "D/P": (0.012, 0.032),
                "B/M": (0.225, 1.998), "SIZE": (663, 120)},
        "CPGS": {"E/P": (0.054, 0.114), "C/P": (0.080, 0.279),
                 "S/P": (1.115, 5.279), "D/P": (0.014, 0.039),
                 "B/M": (0.385, 1.414), "SIZE": (681, 390)},
    }
    print("\n[Panel A] mine (glamour, value) vs paper:")
    for cls, cols in [("B/M", (COLS[0], COLS[1])), ("CPGS", (COLS[2], COLS[3]))]:
        for m in ["E/P", "C/P", "S/P", "D/P", "B/M", "SIZE"]:
            k = A_KEY[m]
            mine = (tableA[(k, cols[0])], tableA[(k, cols[1])])
            pap = papA[cls][m]
            print(f"  {cls:4s} {m:5s}: mine ({mine[0]:.3f},{mine[1]:.3f})  "
                  f"paper ({pap[0]:.3f},{pap[1]:.3f})")

    papB = {"AEG(-5,0)": {"B/M": (0.309, -0.274), "CPGS": (0.142, 0.082)},
            "ACG(-5,0)": {"B/M": (0.217, -0.013), "CPGS": (0.210, 0.078)},
            "ASG(-5,0)": {"B/M": (0.091, 0.030), "CPGS": (0.112, 0.013)},
            "RETURN(-3,0)": {"B/M": (1.455, -0.119), "CPGS": (1.390, 0.225)}}
    papC = {"AEG(0,5)": {"B/M": (0.050, 0.436), "CPGS": (0.089, 0.086)},
            "ACG(0,5)": {"B/M": (0.127, 0.070), "CPGS": (0.112, 0.052)},
            "ASG(0,5)": {"B/M": (0.062, 0.020), "CPGS": (0.100, 0.037)},
            "AEG(2,5)": {"B/M": (0.070, 0.215), "CPGS": (0.084, 0.147)},
            "ACG(2,5)": {"B/M": (0.086, 0.111), "CPGS": (0.095, 0.088)},
            "ASG(2,5)": {"B/M": (0.059, 0.023), "CPGS": (0.082, 0.038)}}
    def _p(x):
        return f"{x:+.3f}" if x is not None and not pd.isna(x) else "   nan"

    # RETURN(-3,0) is a Panel-A metric (was mis-routed to the growth dict above)
    print("\n[RETURN(-3,0)] (EW cum 3-yr pre-formation return):")
    for cls, cols in [("B/M", (COLS[0], COLS[1])), ("CPGS", (COLS[2], COLS[3]))]:
        mine = (tableA[("RETURN(-3,0)", cols[0])],
                tableA[("RETURN(-3,0)", cols[1])])
        pap = papB["RETURN(-3,0)"][cls]
        print(f"  {cls:4s}: mine ({mine[0]:+.3f},{mine[1]:+.3f})  "
              f"paper ({pap[0]:+.3f},{pap[1]:+.3f})")

    print("\n[Panels B/C] growth (avgQ-first | perFy-first), full-N, vs paper:")
    for d, dd in {**papB, **papC}.items():
        if d == "RETURN(-3,0)":
            continue
        for cls, cols in [("B/M", (COLS[0], COLS[1])),
                          ("CPGS", (COLS[2], COLS[3]))]:
            g = tableG_avg.get((d, cols[0])), tableG_avg.get((d, cols[1]))
            gf = tableG_pf.get((d, cols[0])), tableG_pf.get((d, cols[1]))
            pap = dd[cls]
            print(f"  {d:11s} {cls:4s}: avgQ({_p(g[0])},{_p(g[1])}) "
                  f"perFy({_p(gf[0])},{_p(gf[1])}) paper({_p(pap[0])},{_p(pap[1])})")

    # internal consistency: CPGS glamour C/P grown at ACG(0,5) for 5 yrs
    cp_g = tableA[(A_KEY["C/P"], COLS[2])]; acg = tableG[("ACG(0,5)", COLS[2])]
    cp_v = tableA[(A_KEY["C/P"], COLS[3])]; acg_v = tableG[("ACG(0,5)", COLS[3])]
    print("\n[internal consistency] CPGS glamour C/P %.3f * (1+%.3f)^5 = %.3f "
          "(paper ~0.136)" % (cp_g, acg, cp_g * (1 + acg) ** 5))
    print("                     CPGS value   C/P %.3f * (1+%.3f)^5 = %.3f "
          "(paper ~0.360)" % (cp_v, acg_v, cp_v * (1 + acg_v) ** 5))

    # membership
    print("\n[membership] median members per portfolio across formations:")
    for c in COLS:
        s = mem_stats[c]
        print(f"  {c:<28s} median={np.median(s):.0f} min={min(s)} "
              f"max={max(s)} n_formations={len(s)}")
    print("=" * 78)


if __name__ == "__main__":
    main()
