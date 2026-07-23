"""
Report-support ARTIFACT 2 — consolidated per-cell evaluation summary.

Reads the four per-table eval JSONs (results/table_{1..4}_eval.json) and writes
results/evaluation_summary.md with:
  1. OVERALL tally (Tier 1 / Tier 2 / FAIL / SKIP + total cells).
  2. PER-TABLE tally.
  3. A table of EVERY FAIL cell.
  4. A table of EVERY SKIP cell (if any).
  5. A grouped summary of the Tier-2 cells by driver, with counts.

Parsing is robust: the per-metric entries are read defensively (fields may be
named metric/name, ours/value, paper/paper_value, status/tier, reason/note).
The recount is cross-checked against the `tally` block each JSON stores.

This script only READS the eval JSONs and WRITES results/evaluation_summary.md.
It does not touch any table output, the foundation, or the parquets.
"""
from __future__ import annotations

import json
from collections import Counter, OrderedDict
from pathlib import Path

SLUG_DIR = Path(__file__).resolve().parents[1]
RESULTS = SLUG_DIR / "results"
EVAL_FILES = OrderedDict([
    ("Table I",   RESULTS / "table_1_eval.json"),
    ("Table II",  RESULTS / "table_2_eval.json"),
    ("Table III", RESULTS / "table_3_eval.json"),
    ("Table IV",  RESULTS / "table_4_eval.json"),
])

STATUS_KEYS = ["Tier 1", "Tier 2", "FAIL", "SKIP"]


# ---------------------------------------------------------------------------
# robust entry extraction
# ---------------------------------------------------------------------------
def _pick(d: dict, *names, default=None):
    for n in names:
        if n in d and d[n] is not None:
            return d[n]
    return default


def extract_entries(raw: dict) -> list[dict]:
    """Return a normalized list of {metric, paper, ours, status, reason}."""
    evals = _pick(raw, "evaluation", "evaluations", "cells", "metrics", default=[])
    out = []
    for e in evals:
        if not isinstance(e, dict):
            continue
        metric = _pick(e, "metric", "name", "cell", "id", default="?")
        status = _pick(e, "status", "tier", "result", "verdict", default="?")
        out.append({
            "metric": str(metric),
            "paper": _pick(e, "paper", "paper_value", "target", "paper_val"),
            "ours":  _pick(e, "ours", "value", "our_value", "computed", "val"),
            "status": str(status),
            "reason": str(_pick(e, "reason", "note", "comment", "explanation", default="")),
        })
    return out


def extract_tally(raw: dict) -> dict:
    t = _pick(raw, "tally", "summary", default={}) or {}
    return {k: int(_pick(t, k, default=0) or 0) for k in STATUS_KEYS}


# ---------------------------------------------------------------------------
# Tier-2 driver classification (rule-based, deterministic)
# ---------------------------------------------------------------------------
# Driver labels (grouped). Each Tier-2 cell maps to exactly one driver.
D_ASSETG   = "ASSETG upper-tail / attenuation vintage (Assumption 7)"
D_LOWGR    = "Low-growth / median decile level shift (ASSETG compressed toward 0)"
D_ISSUANCE = "ISSUANCE raw-csho split (Assumption 8)"
D_VWSHARPE = "VW-spread Sharpe volatility (return-vol vintage)"
D_ACCR     = "ACCRUALS / ΔCurAsst / ΔOthAssets missingness + shell dilution (data vintage)"
D_MVUNITS  = "MV units (FM slope scaling)"
D_NOISE    = "Noise-level sign flip on a ~0 coefficient"
D_BROAD    = "Broad characteristic level shift (2026 Compustat/CRSP universe vintage)"

# Order matters: most-specific rules first.
DRIVER_ORDER = [D_ASSETG, D_LOWGR, D_ISSUANCE, D_VWSHARPE, D_ACCR,
                D_MVUNITS, D_NOISE, D_BROAD]

# Short per-driver explanation used in the summary table.
DRIVER_NOTE = {
    D_ASSETG:   "2026 Compustat vintage fattens the ASSETG upper tail (D10 1.14 vs 0.84) and attenuates ASSETG slopes once controls enter; lower tail/median and monotonicity match (Assumption 7).",
    D_LOWGR:    "Low (D1) and median (D5) ASSETG deciles are compressed toward zero in our vintage (D1 −0.18 vs −0.21).",
    D_ISSUANCE: "5-yr share change uses raw Compustat csho; unadjusted stock splits inflate it ~1.5-3× the paper. Sign + monotonicity correct (Assumption 8).",
    D_VWSHARPE: "VW spread mean matches (~12%/yr) but annual spread std is higher (17.6% vs ~11.6% implied) on the 2026 vintage, lowering the Sharpe; sign strongly positive.",
    D_ACCR:     "Accruals / current-assets / other-assets components are poorly measured (act−ch ~18% missing; sparse pre-1971 cross-sections; dormant-shell ROA dilution) → attenuated descriptive cells and FM slopes. Sign correct.",
    D_MVUNITS:  "FM slope on MV is unit-dependent; MV in $billions (−0.0036) is 18% off the paper's −0.0044 and the t-stat matches. A scaling/units note, not an economics gap.",
    D_NOISE:    "Target spread is ≈0 (paper +0.0165); ours −0.0158. Sign flips but the magnitude is economically meaningless (noise).",
    D_BROAD:    "Descriptive characteristic levels (size, B/M, E/P, leverage, ROA, past returns, total assets) shift between the ~2005 paper vintage and our 2026 vintage (universe composition); sign + monotonicity preserved.",
}


def classify_driver(table: str, metric: str) -> str:
    m = metric
    # ISSUANCE — raw csho split (Assumption 8)
    if m.startswith("ISSUANCE"):
        return D_ISSUANCE
    # VW-spread Sharpe volatility (Table II)
    if table == "Table II" and "Sharpe" in m:
        return D_VWSHARPE
    # MV units (Table III FM slope on MV)
    if table == "Table III" and m == "M1_MV":
        return D_MVUNITS
    # Noise-level sign flip on ~0 coefficient (Table I Leverage spread)
    if table == "Table I" and m == "Leverage_spread_10_1":
        return D_NOISE
    # ASSETG coefficient / upper-tail vintage (Assumption 7)
    #   includes Table I ASSETG/L2ASSETG upper-tail+spread+t cells, the Table II
    #   Panel-A ASSETG year-1 spread/t, and the Table III ASSETG coefficient t in
    #   the ACCRUALS-augmented model (M6_ACCRUALS_ASSETG_t == ASSETG t-stat).
    #   Within the ASSETG family ONLY, the low/median decile cells (D1, D5) are a
    #   level shift (compressed toward zero) — a distinct driver from the upper
    #   tail. (Other characteristics' D1 cells, e.g. ASSETS_D1 / MV_D1, fall
    #   through to the broad-level-shift bucket below.)
    if "ASSETG" in m and not m.endswith("ACCRUALS_t"):
        if m.endswith("_D1") or m.endswith("_D5"):
            return D_LOWGR
        return D_ASSETG
    # ACCRUALS / ΔCurAsst / ΔOthAssets missingness + shell dilution
    if "ACCRUALS" in m:
        return D_ACCR
    if table == "Table IV" and ("dCurAsst" in m or "dOthAssets" in m):
        return D_ACCR
    # Table I descriptive characteristics not covered above → broad level shift
    if table == "Table I":
        return D_BROAD
    return "other (uncategorized)"


# ---------------------------------------------------------------------------
# formatting helpers
# ---------------------------------------------------------------------------
def fmt(x) -> str:
    if x is None:
        return "—"
    if isinstance(x, (int,)):
        return str(x)
    try:
        f = float(x)
    except (TypeError, ValueError):
        return str(x)
    a = abs(f)
    if a != 0 and (a < 1e-3 or a >= 1e5):
        return f"{f:.3e}"
    if a >= 100:
        return f"{f:.1f}"
    return f"{f:.4f}".rstrip("0").rstrip(".")


def main():
    per_table = OrderedDict()     # table -> entries
    stored_tally = OrderedDict()  # table -> tally dict
    for tname, path in EVAL_FILES.items():
        raw = json.loads(Path(path).read_text())
        per_table[tname] = extract_entries(raw)
        stored_tally[tname] = extract_tally(raw)

    # ---- recount + cross-check -------------------------------------------
    recount = OrderedDict()
    mismatches = []
    for tname, entries in per_table.items():
        c = Counter(e["status"] for e in entries)
        rc = {k: c.get(k, 0) for k in STATUS_KEYS}
        recount[tname] = rc
        st = stored_tally[tname]
        for k in STATUS_KEYS:
            if rc[k] != st.get(k, 0):
                mismatches.append((tname, k, rc[k], st.get(k, 0)))
        if len(entries) != sum(st.get(k, 0) for k in STATUS_KEYS):
            mismatches.append((tname, "TOTAL", len(entries),
                               sum(st.get(k, 0) for k in STATUS_KEYS)))

    overall = {k: sum(recount[t][k] for t in recount) for k in STATUS_KEYS}
    total_cells = sum(overall.values())

    # ---- collect FAIL / SKIP / Tier-2 ------------------------------------
    fails, skips = [], []
    tier2 = []
    for tname, entries in per_table.items():
        for e in entries:
            row = {"table": tname, **e}
            if e["status"] == "FAIL":
                fails.append(row)
            elif e["status"] == "SKIP":
                skips.append(row)
            elif e["status"] == "Tier 2":
                row["driver"] = classify_driver(tname, e["metric"])
                tier2.append(row)

    driver_counts = Counter(r["driver"] for r in tier2)
    driver_cells = OrderedDict((d, []) for d in DRIVER_ORDER)
    for r in tier2:
        driver_cells.setdefault(r["driver"], []).append(r)

    # ---- render markdown -------------------------------------------------
    L = []
    L.append("# Consolidated Per-Cell Evaluation Summary")
    L.append("")
    L.append("Asset Growth and the Cross-Section of Stock Returns "
             "(Cooper, Gulen, Schill 2008) — Tables I-IV. ")
    L.append("Source: `results/table_{1..4}_eval.json` (read-only). "
             "Each cell is graded **Tier 1** (within tolerance), **Tier 2** "
             "(correct sign/pattern, outside tolerance — documented data-vintage "
             "or definitional driver), **FAIL** (wrong sign/magnitude on a "
             "meaningful cell), or **SKIP** (not computed).")
    L.append("")

    # 1. OVERALL tally
    L.append("## 1. Overall tally")
    L.append("")
    L.append("| Grade | Count |")
    L.append("|---|---:|")
    for k in STATUS_KEYS:
        L.append(f"| {k} | {overall[k]} |")
    L.append(f"| **Total cells** | **{total_cells}** |")
    L.append("")
    n_tier12 = overall["Tier 1"] + overall["Tier 2"]
    L.append(f"Tier 1 + Tier 2 (correct sign/pattern) = **{n_tier12} of {total_cells}** "
             f"({100*n_tier12/total_cells:.1f}%). FAIL = {overall['FAIL']}; "
             f"SKIP = {overall['SKIP']}.")
    L.append("")

    # 2. PER-TABLE tally
    L.append("## 2. Per-table tally")
    L.append("")
    L.append("| Table | Tier 1 | Tier 2 | FAIL | SKIP | Total |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for tname in per_table:
        rc = recount[tname]
        tot = sum(rc.values())
        L.append(f"| {tname} | {rc['Tier 1']} | {rc['Tier 2']} | {rc['FAIL']} "
                 f"| {rc['SKIP']} | {tot} |")
    L.append(f"| **All** | **{overall['Tier 1']}** | **{overall['Tier 2']}** "
             f"| **{overall['FAIL']}** | **{overall['SKIP']}** | **{total_cells}** |")
    L.append("")

    # cross-check note
    if mismatches:
        L.append("**⚠ Recount vs stored-tally mismatches:**")
        for tname, k, rc_v, st_v in mismatches:
            L.append(f"- {tname} {k}: recount {rc_v} vs stored {st_v}")
        L.append("")
    else:
        L.append("_Cross-check: the per-cell recount matches the `tally` block "
                 "stored in every eval JSON (no discrepancies)._")
        L.append("")

    # 3. FAIL table
    L.append("## 3. Every FAIL cell")
    L.append("")
    if not fails:
        L.append("_None._")
    else:
        L.append("| Table | Metric | Paper | Ours | One-line reason |")
        L.append("|---|---|---:|---:|---|")
        for r in fails:
            L.append(f"| {r['table']} | {r['metric']} | {fmt(r['paper'])} "
                     f"| {fmt(r['ours'])} | {r['reason']} |")
    L.append("")

    # 4. SKIP table
    L.append("## 4. Every SKIP cell")
    L.append("")
    if not skips:
        L.append("_None._ (All committed cells were computed; the Table II "
                 "Section E event-time spread that was initially SKIP was filled "
                 "in Iteration 5 and is now Tier 1 — see Assumption 11.)")
    else:
        L.append("| Table | Metric | Reason |")
        L.append("|---|---|---|")
        for r in skips:
            L.append(f"| {r['table']} | {r['metric']} | {r['reason']} |")
    L.append("")

    # 5. Tier-2 grouped by driver
    L.append("## 5. Tier-2 cells grouped by driver")
    L.append("")
    L.append("| Driver | # Tier-2 cells |")
    L.append("|---|---:|")
    for d in DRIVER_ORDER:
        n = driver_counts.get(d, 0)
        if n:
            L.append(f"| {d} | {n} |")
    # any uncategorized
    for d, cells in driver_cells.items():
        if d not in DRIVER_ORDER and cells:
            L.append(f"| {d} | {len(cells)} |")
    L.append(f"| **Total Tier-2** | **{len(tier2)}** |")
    L.append("")
    L.append("### Driver detail")
    L.append("")
    for d in list(DRIVER_ORDER) + [x for x in driver_cells if x not in DRIVER_ORDER]:
        cells = driver_cells.get(d, [])
        if not cells:
            continue
        cell_list = ", ".join(f"{c['table']}:{c['metric']}" for c in cells)
        L.append(f"- **{d} ({len(cells)}):** {DRIVER_NOTE.get(d, '')} "
                 f"Cells: {cell_list}.")
    L.append("")

    # per-table Tier-2 breakdown (compact matrix)
    L.append("### Per-table Tier-2 matrix (by driver)")
    L.append("")
    tables = list(per_table.keys())
    header = "| Driver | " + " | ".join(tables) + " |"
    L.append(header)
    L.append("|---|" + "---:|" * len(tables))
    for d in DRIVER_ORDER:
        row = [d]
        for tname in tables:
            n = sum(1 for r in tier2 if r["driver"] == d and r["table"] == tname)
            row.append(str(n) if n else "·")
        L.append("| " + " | ".join(row) + " |")
    totrow = ["**Total**"] + [f"**{sum(1 for r in tier2 if r['table']==t)}**" for t in tables]
    L.append("| " + " | ".join(totrow) + " |")
    L.append("")

    out = RESULTS / "evaluation_summary.md"
    out.write_text("\n".join(L))
    print(f"wrote {out}")

    # ---- console summary ----
    print(f"\nOVERALL: {overall}  total={total_cells}")
    for tname in per_table:
        print(f"  {tname}: {recount[tname]}  (stored {stored_tally[tname]})")
    print(f"\nFAIL ({len(fails)}):")
    for r in fails:
        print(f"  {r['table']} {r['metric']}: paper={fmt(r['paper'])} ours={fmt(r['ours'])} | {r['reason']}")
    print(f"\nSKIP ({len(skips)})")
    print(f"\nTier-2 drivers ({len(tier2)} total):")
    for d in DRIVER_ORDER:
        if driver_counts.get(d):
            print(f"  {driver_counts[d]:2d}  {d}")


if __name__ == "__main__":
    main()
