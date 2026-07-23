"""
LSV (1994) Table IV — Fama-MacBeth cross-sectional regressions of Year +1 stock
return (stock_ret_1) on characteristics, 22 formations (A9). Reads panel.parquet.
Emits results/table_4.md + results/table_IV_cells.json (exact target names).

Covariates: GS=gs_rank_frac (gs-valid); B/M=bm (be_valid); SIZE=ln(me_apr/1e6);
E/P+=max(ep,0); DE/P=1{ep<=0}; C/P+=max(cp,0); DC/P=1{cp<=0} (the +/- and dummies
defined for ALL firms, A8/L1909). 9 specs (paper order); per-spec cross-section =
firms with alive_1==1 & stock_ret_1 not null & non-missing covariates for that spec.
FM coef = mean of 22 OLS slopes; t = mean/(std(ddof=1)/sqrt(22)).

Run: cd repo-root && uv run python replications/contrarian_investment/src/table4.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from utils.paths import paper_layout  # noqa: E402

LAYOUT = paper_layout("contrarian_investment",
                      replications_root=REPO_ROOT / "replications")
RES = LAYOUT.results_dir

COLS = ["Int.", "GS", "B/M", "SIZE", "E/P+", "DE/P", "C/P+", "DC/P"]
# spec -> list of covariate columns (Int. always present)
SPECS = {
    1: ["GS"],
    2: ["B/M"],
    3: ["SIZE"],
    4: ["E/P+"],
    5: ["C/P+"],
    6: ["GS", "B/M", "C/P+", "DC/P"],
    7: ["B/M", "SIZE", "C/P+", "DC/P"],
    8: ["GS", "B/M", "SIZE", "C/P+", "DC/P"],
    9: ["GS", "B/M", "SIZE", "E/P+", "DE/P"],
}
VALID = {"GS": lambda d: d["gs_rank_frac"].notna(),
         "B/M": lambda d: d["be_valid"] == 1,
         # E/P+/DE/P need raw ep non-missing (ep==0 KEPT so DE/P varies);
         # C/P+/DC/P need raw cp non-missing (cp==0 KEPT so DC/P varies).
         "E/P+": lambda d: d["ep"].notna(),
         "DE/P": lambda d: d["ep"].notna(),
         "C/P+": lambda d: d["cp"].notna(),
         "DC/P": lambda d: d["cp"].notna()}


def build_covariates(panel):
    d = panel.copy()
    d["GS"] = d["gs_rank_frac"]
    d["B/M"] = d["bm"]
    me_mil = d["me_apr"] / 1e6
    d["SIZE"] = np.where(me_mil > 0, np.log(me_mil), np.nan)
    d["E/P+"] = d["ep"].clip(lower=0.0).fillna(0.0)
    d["DE/P"] = (d["ep"].fillna(1.0) <= 0).astype(float)   # NaN ep -> not counted (filtered by VALID)
    d["C/P+"] = d["cp"].clip(lower=0.0).fillna(0.0)
    d["DC/P"] = (d["cp"].fillna(1.0) <= 0).astype(float)
    return d


def ols_coefs(y, X):
    """Return dict col->slope for columns of X (with intercept handled outside)."""
    Xc = X - X.mean(axis=0)
    yc = y - y.mean()
    XtX = Xc.T @ Xc
    try:
        b = np.linalg.solve(XtX, Xc.T @ yc)
    except np.linalg.LinAlgError:
        return None
    return b


def run_fm(panel):
    d = build_covariates(panel)
    base_ok = (d["alive_1"] == 1) & d["stock_ret_1"].notna() & d["SIZE"].notna()
    y_all = d["stock_ret_1"]
    fys = sorted(d["fy"].unique())
    # results[spec][col] = list of per-formation coefs
    res = {s: {c: [] for c in (["Int."] + SPECS[s])} for s in SPECS}
    nsec = {s: [] for s in SPECS}
    for s, covs in SPECS.items():
        ok = base_ok.copy()
        for c in covs:
            if c in VALID:
                ok = ok & VALID[c](d)
        for fy in fys:
            idx = d.index[ok & (d["fy"] == fy)]
            if len(idx) < len(covs) + 2:
                res_s_none = True
                for c in (["Int."] + covs):
                    res[s][c].append(np.nan)
                nsec[s].append(0)
                continue
            nsec[s].append(len(idx))
            X = d.loc[idx, covs].values
            y = y_all.loc[idx].values
            b = ols_coefs(y, X)
            if b is None:
                for c in (["Int."] + covs):
                    res[s][c].append(np.nan)
            else:
                res[s]["Int."].append(float(y.mean() - X.mean(axis=0) @ b))
                for j, c in enumerate(covs):
                    res[s][c].append(float(b[j]))
    return res, nsec


def fm_stat(coefs):
    a = np.array([x for x in coefs if not (pd.isna(x) if isinstance(x, float)
                                            else False)], dtype=float)
    a = a[~np.isnan(a)]
    if len(a) < 2:
        return np.nan, np.nan
    m = a.mean()
    t = m / (a.std(ddof=1) / np.sqrt(len(a)))
    return float(m), float(t)


def write_md(res, path):
    lines = ["# Table IV — Fama-MacBeth regressions of Year +1 return (LSV 1994)",
             "",
             "22 cross-sectional OLS (one per formation), dependent var = stock_ret_1; "
             "coefficient = mean of 22 slopes, t = mean/(std/sqrt(22)). Covariates: "
             "GS=gs_rank_frac, B/M=bm, SIZE=ln(ME$M), E/P+=max(ep,0), DE/P=1{ep<=0}, "
             "C/P+=max(cp,0), DC/P=1{cp<=0}. Blank = not in spec.", ""]
    head = "| Spec | " + " | ".join(COLS) + " |"
    sep = "|---|" + "---|" * len(COLS)
    lines += [head, sep]
    for s in sorted(SPECS):
        mean_row = [f"{s} Mean"]
        t_row = [f"{s} t"]
        for c in COLS:
            if c in res[s]:
                m, t = fm_stat(res[s][c])
                mean_row.append("-" if pd.isna(m) else f"{m:.3f}")
                t_row.append("-" if pd.isna(t) else f"{t:.3f}")
            else:
                mean_row.append("")
                t_row.append("")
        lines.append("| " + " | ".join(mean_row) + " |")
        lines.append("| " + " | ".join(t_row) + " |")
    path.write_text("\n".join(lines) + "\n")


def main():
    panel = pd.read_parquet(LAYOUT.data_path("panel.parquet"))
    print(f"Loaded panel {panel.shape}")
    res, nsec = run_fm(panel)

    tgt = json.loads(LAYOUT.preparations_path("tables_to_replicate.json").read_text())
    t4 = {m["name"]: m["value"] for t in tgt["tables"] if t["id"] == "table_IV"
          for m in t["metrics"]}
    cells = {}
    for s in sorted(SPECS):
        for c in (["Int."] + SPECS[s]):
            m, t = fm_stat(res[s][c])
            for kind, val in [("coefficient (mean)", m), ("t-statistic", t)]:
                name = f"spec {s} {c} {kind}"
                if name in t4 and not pd.isna(val):
                    cells[name] = round(float(val), 6)
    out = {n: cells[n] for n in t4 if n in cells}
    (RES / "table_IV_cells.json").write_text(json.dumps(out, indent=2))
    print(f"Emitted table_IV_cells.json: {len(out)} / {len(t4)}")
    write_md(res, RES / "table_4.md")
    print("Wrote results/table_4.md")

    # diagnostics
    print("\n" + "=" * 70)
    print("TABLE IV DIAGNOSTICS")
    print("=" * 70)
    pap = {1: {"Int.": (0.180, 3.251), "GS": (-0.061, -2.200)},
           2: {"B/M": (0.039, 2.132)}, 3: {"SIZE": (-0.009, -1.095)},
           4: {"E/P+": (0.526, 2.541)}, 5: {"C/P+": (0.356, 4.240)},
           6: {"GS": (-0.058, -2.832), "B/M": (0.006, 0.330),
               "C/P+": (0.301, 3.697), "DC/P": (-0.029, -1.222)},
           8: {"GS": (-0.044, -2.125), "B/M": (0.000, 0.005),
               "SIZE": (-0.009, -1.062), "C/P+": (0.296, 4.553),
               "DC/P": (-0.036, -1.625)},
           9: {"GS": (-0.051, -2.527), "B/M": (0.016, 1.036),
               "SIZE": (-0.009, -1.065), "E/P+": (0.394, 2.008),
               "DE/P": (-0.032, -1.940)}}
    print("\n[anchors] mine coef/t vs paper coef/t:")
    for s in sorted(pap):
        for c, (pc, pt) in pap[s].items():
            m, t = fm_stat(res[s][c])
            print(f"  spec{s} {c:5s}: mine {m:+.3f}/t{t:+.3f}  "
                  f"paper {pc:+.3f}/t{pt:+.3f}")
    print("\n[N cross-section per formation] (median across 22):")
    for s in sorted(SPECS):
        nz = [x for x in nsec[s] if x > 0]
        print(f"  spec{s}: median={np.median(nz):.0f} min={min(nz)} "
              f"max={max(nz)} (n_formations_with_obs={len(nz)})")
    # key claim: B/M ~0 with t<1 in specs 6-8
    print("\n[key claim] B/M collapses in specs 6-8 (|t|<1?):")
    for s in (6, 7, 8):
        m, t = fm_stat(res[s]["B/M"])
        print(f"  spec{s} B/M coef={m:+.3f} t={t:+.3f}  |t|<1 = {abs(t) < 1}")
    print("  GS & C/P+ significant (|t|>2) in spec6:",
          abs(fm_stat(res[6]['GS'])[1]) > 2, abs(fm_stat(res[6]['C/P+'])[1]) > 2)
    print("=" * 70)


if __name__ == "__main__":
    main()
