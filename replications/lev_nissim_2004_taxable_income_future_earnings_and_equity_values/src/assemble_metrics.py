"""
assemble_metrics.py — Aggregate per-table cells JSONs into the single
eval/metrics.json consumed by scripts/score_replication.py.

The canonical scorer reads `eval/metrics.json` with the structure:
  {
    "schema_version": 2,
    "slug": ...,
    "metrics": {
      "<metric_name>": {
        "value": <float>,           # the replicated value (none → cell = MISSING)
        "paper": <float>,           # paper value (from tables_to_replicate.json)
        "unit": "<unit>",           # informational
        "tolerance_pct": <float>,   # from tables_to_replicate.json
        "paper_location": "<L...>", # from tables_to_replicate.json
        "source": "<cell_path>"     # which per-table JSON the cell came from
      },
      ...
    }
  }

Lookup convention (replicates["results/table_*_cells.json"]):
  T2 cells:
    T2_A_R_TAX_only_G1_mean_b1     → panels.A.models.1.g_vars.g1.mean_betas.r_tax
    T2_A_R_TAX_only_G1_t_b1        → panels.A.models.1.g_vars.g1.t_stats.r_tax
    T2_A_R_TAX_only_G1_R2          → panels.A.models.1.g_vars.g1.mean_r2
    T2_A_R_TAX_only_G1_n           → panels.A.models.1.g_vars.g1.mean_n
    T2_A_full_model_G1_mean_b1     → panels.A.models.4.g_vars.g1.mean_betas.r_tax
    T2_A_full_model_G1_mean_b3     → panels.A.models.4.g_vars.g1.mean_betas.r_cfo
    ... (same pattern for B and for G2/G3)
  T3 cells: same convention as T2.
  T4 cells:
    T4_A_R_TAX_spec1_mean_b        → panels.A.models.1.result.mean_betas.r_tax
    T4_A_R_TAX_spec1_t_b           → panels.A.models.1.result.t_stats.r_tax
    T4_A_n                         → panels.A.models.3.result.mean_n
    ... (same for B)
  T5 cells:
    T5_A_R_TAX_spec1_mean_b        → panels.A.models.1.result.mean_betas.r_tax
    T5_A_R_TAX_spec1_t_b           → panels.A.models.1.result.t_stats.r_tax
    T5_A_n                         → panels.A.models.1.result.mean_n
    T5_A_R2_spec1                  → panels.A.models.1.result.mean_r2
    ... (same for B)

For metrics we cannot compute (e.g. T3 cells prior to outer iteration
2), we set `ours: null` so the scorer marks them MISSING.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout  # noqa: E402

SLUG = "lev_nissim_2004_taxable_income_future_earnings_and_equity_values"
LAYOUT = paper_layout(SLUG)

# Panels / G-vars / Models — for the T2/T3 lookup convention
PANELS = ("A", "B")
G_VARS = ("g1", "g2", "g3")
T2_T3_MODELS = {"R_TAX_only": "1", "full_model": "4"}


def _lookup_t2_t3(
    cells: dict, panel: str, model_id: str, g_var: str
) -> dict | None:
    """Return the cell dict for T2/T3 (panel, model, g_var)."""
    return (cells.get("panels", {})
                .get(panel, {})
                .get("models", {})
                .get(model_id, {})
                .get("g_vars", {})
                .get(g_var))


def _lookup_t4_t5(
    cells: dict, panel: str, model_id: str
) -> dict | None:
    """Return the cell dict for T4/T5 (panel, model)."""
    return (cells.get("panels", {})
                .get(panel, {})
                .get("models", {})
                .get(model_id, {})
                .get("result"))


def _maybe_load(path: Path) -> dict | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text())


def build_metric_entry(
    metric: dict, source_files: dict[str, dict]
) -> dict | None:
    """Return the entry in eval/metrics.json for one metric.

    Returns None when the metric cannot be computed in this iteration —
    the caller will then omit the entry entirely so the canonical scorer
    marks the cell MISSING (a metric dict with `value: None` would crash
    the scorer's relative-error calculation).

    When the entry is returned, it carries `value`, `paper`, `unit`,
    `tolerance_pct`, `paper_location`, and `source`.
    """
    name = metric["name"]
    paper_value = metric["value"]
    unit = metric.get("unit", "")
    tolerance_pct = metric.get("tolerance_pct", 0)
    paper_location = metric.get("paper_location", "")

    # Default: no replication value (metrics we haven't computed yet).
    ours_value: float | None = None
    source: str = ""

    # --- T2 / T3 cells ---
    if name.startswith("T2_") or name.startswith("T3_"):
        # e.g. T2_A_R_TAX_only_G1_mean_b1
        parts = name.split("_")
        # Position: [T2, A, R, TAX, only, G1, mean, b1]
        # OR       [T3, A, R, TAX, only, G1, mean, b1]
        # OR       [T2, A, full, model, G1, mean, b3]
        # OR       [T2, A, full, model, G1, R2]  (6 parts)
        if len(parts) >= 7 and parts[2] == "R" and parts[3] == "TAX" and parts[4] == "only":
            panel = parts[1]
            g_var = parts[5].lower()
            stat = "_".join(parts[6:])  # e.g. "mean_b1", "t_b1", "R2", "n"
            model_id = T2_T3_MODELS["R_TAX_only"]
        elif len(parts) >= 6 and parts[2] == "full" and parts[3] == "model":
            panel = parts[1]
            g_var = parts[4].lower()
            stat = "_".join(parts[5:])  # "mean_b1", "mean_b3", "t_b1", "t_b3", "R2", "n"
            model_id = T2_T3_MODELS["full_model"]
        else:
            return None

        table = ("T2" if name.startswith("T2_") else "T3").lower()
        cells = source_files.get(table)
        if cells is None:
            return None
        cell = _lookup_t2_t3(cells, panel, model_id, g_var)
        if cell is None:
            return None
        ours_value = _stat_from_cell(cell, stat)
        source = f"results/table_{table}_cells.json"
        if ours_value is None:
            return None

    # --- T4 cells ---
    elif name.startswith("T4_"):
        # T4_A_R_TAX_spec1_mean_b  → parts = ['T4','A','R','TAX','spec1','mean','b']
        # T4_A_n                   → parts = ['T4','A','n']
        parts = name.split("_")
        if len(parts) == 3 and parts[2] == "n":
            panel = parts[1]
            cell = _lookup_t4_t5(source_files.get("t4"), panel, "3")
            if cell is not None:
                ours_value = float(cell["mean_n"])
                source = "results/table_4_cells.json"
        elif len(parts) >= 7 and parts[2] == "R" and parts[3] == "TAX":
            panel = parts[1]
            spec_token = parts[4]  # "spec1" or "spec3"
            model_id = spec_token[len("spec"):]  # "1" or "3"
            stat = "_".join(parts[5:])  # "mean_b", "t_b"
            cell = _lookup_t4_t5(source_files.get("t4"), panel, model_id)
            if cell is not None:
                ours_value = _stat_from_cell(cell, stat)
                source = "results/table_4_cells.json"

    # --- T5 cells ---
    elif name.startswith("T5_"):
        parts = name.split("_")
        if len(parts) == 3 and parts[2] == "n":
            panel = parts[1]
            cell = _lookup_t4_t5(source_files.get("t5"), panel, "1")
            if cell is not None:
                ours_value = float(cell["mean_n"])
                source = "results/table_5_cells.json"
        elif len(parts) >= 6 and parts[2] == "R" and parts[3] == "TAX":
            # T5_A_R_TAX_spec1_mean_b
            panel = parts[1]
            spec_token = parts[4]
            model_id = spec_token[len("spec"):]
            stat = "_".join(parts[5:])
            cell = _lookup_t4_t5(source_files.get("t5"), panel, model_id)
            if cell is not None:
                ours_value = _stat_from_cell(cell, stat)
                source = "results/table_5_cells.json"
        elif len(parts) >= 4 and parts[2] == "R2":
            # T5_A_R2_spec1
            panel = parts[1]
            spec_token = parts[3]
            model_id = spec_token[len("spec"):]
            cell = _lookup_t4_t5(source_files.get("t5"), panel, model_id)
            if cell is not None:
                ours_value = float(cell["mean_r2"])
                source = "results/table_5_cells.json"

    return {
        "value": ours_value,
        "paper": paper_value,
        "unit": unit,
        "tolerance_pct": tolerance_pct,
        "paper_location": paper_location,
        "source": source,
    }


def _stat_from_cell(cell: dict, stat: str) -> float | None:
    """Extract a stat from a T2/T3/T4/T5 cell dict.

    stat codes:
      mean_b1 / mean_b3 / mean_b     → mean_betas[<var>]
      t_b1 / t_b3 / t_b              → t_stats[<var>]
      R2                             → mean_r2
      n                              → mean_n

    The `b1`/`b3`/`b` suffix follows the paper's β indexing:
      b1 (T2/T3) or `_b` (T4/T5) = R_TAX
      b3                  = R_CFO
    """
    if stat == "R2":
        return float(cell["mean_r2"])
    if stat == "n":
        return float(cell["mean_n"])

    # Decode the variable suffix → column-name suffix used in JSON keys.
    # The suffix AFTER "mean_b" / "t_b" / "_b" is a single digit / empty.
    # b1 → r_tax, b3 → r_cfo, b → r_tax (T4/T5 the headline is R_TAX only).
    term_to_col = {
        "b1": "r_tax",
        "b3": "r_cfo",
        "b": "r_tax",
    }

    # Determine which term this is.
    if stat.startswith("mean_b"):
        term = stat[len("mean_b") - 1:]  # "b1", "b3", or "b"
        mb = cell.get("mean_betas", {})
        if term in term_to_col:
            v = mb.get(term_to_col[term])
            if v is None and mb:
                v = next(iter(mb.values()))
            return float(v) if v is not None else None
        # Unknown term — fall back to first coef
        if mb:
            v = next(iter(mb.values()))
            return float(v)
        return None

    if stat.startswith("t_b"):
        term = stat[len("t_b") - 1:]
        ts = cell.get("t_stats", {})
        if term in term_to_col:
            v = ts.get(term_to_col[term])
            if v is None and ts:
                v = next(iter(ts.values()))
            return float(v) if v is not None else None
        if ts:
            v = next(iter(ts.values()))
            return float(v)
        return None
    return None


def main() -> int:
    """Build eval/metrics.json from the per-table JSONs."""
    LAYOUT.ensure()

    # Load tables_to_replicate.json — the source of truth for metric names.
    tables_path = LAYOUT.preparations_path("tables_to_replicate.json")
    tables_doc = json.loads(tables_path.read_text())

    # Load per-table result files.
    sources: dict[str, dict] = {}
    for n in (2, 3, 4, 5):
        c = _maybe_load(LAYOUT.result_path(f"table_{n}_cells.json"))
        if c is not None:
            sources[f"t{n}"] = c

    # Walk every metric in every table and build the entry.
    metrics_out: dict[str, dict] = {}
    for tbl in tables_doc["tables"]:
        for m in tbl["metrics"]:
            entry = build_metric_entry(m, sources)
            if entry is None:
                # skip — the scorer will treat this as MISSING
                continue
            metrics_out[m["name"]] = entry

    # Write eval/metrics.json.
    payload = {
        "schema_version": 2,
        "slug": SLUG,
        "metrics": metrics_out,
    }
    out_path = LAYOUT.eval_path("metrics.json")
    out_path.write_text(json.dumps(payload, indent=2, default=float))
    print(f"✅ wrote {out_path} with {len(metrics_out)} metric entries")

    # Sanity report.
    n_with_value = sum(1 for e in metrics_out.values() if e["value"] is not None)
    n_missing = sum(1 for e in metrics_out.values() if e["value"] is None)
    print(f"   replicated: {n_with_value}")
    print(f"   missing:    {n_missing}")
    # Show the missing cells per table.
    per_table_missing: dict[str, int] = {}
    for name, e in metrics_out.items():
        if e["value"] is None:
            tbl = name.split("_")[0]
            per_table_missing[tbl] = per_table_missing.get(tbl, 0) + 1
    if per_table_missing:
        print("   missing cells by table:")
        for tbl, n in sorted(per_table_missing.items()):
            print(f"     {tbl}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
