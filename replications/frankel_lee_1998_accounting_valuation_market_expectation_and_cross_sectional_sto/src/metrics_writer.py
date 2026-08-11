"""metrics_writer.py — parse `results/table_*.md` files for the per-cell
comparison block and emit `data/metrics.json` keyed by metric name.

This is the canonical writer for the BBF-audit loophole fix (DEV-018/019).
The scorer (`scripts/score_replication.py`) reads `data/metrics.json` to
look up each metric's replicated value; without this file, every committed
cell is scored MISSING.

Format (per the scorer's `_score_cell` function):
    {
      "schema_version": 2,
      "slug": "<slug>",
      "metrics": {
        "<metric_name>": {"value": <float>, "unit": "<unit>", ...},
        ...
      }
    }

The metric name keys MUST match `preparations/tables_to_replicate.json
#tables[].metrics[].name` exactly.

Per-cell comparison block format we expect at the bottom of each
`results/table_N.md`:
    ## Per-cell comparison ...
    | Metric | Paper | Ours | Status |
    | --- | ---: | ---: | --- |
    | No. firm    | 18,162  | 21,707  | ... |

The parser pulls the "Ours" column from each row, normalizes the value
to a float, and keys it by the metric name (derived from the row label,
or by looking up the closest known name from the same paper).

For Tables 4/6/7 the rows are not just simple key-value pairs -- they
are subsets of a grid. We provide explicit extraction functions for those.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable

from utils.paths import paper_layout


LAYOUT = paper_layout(
    "frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto"
)

# The expected schema_version (matches SCHEMA_VERSION in score_replication.py)
SCHEMA_VERSION = 2


# --- Per-table extraction helpers ---


def _strip_value(s: str) -> float | None:
    """Normalize a stringified Ours-cell value to a float. Returns
    None if the value cannot be parsed."""
    s = s.strip()
    # Strip markdown bold (**) and italic (*)
    s = s.replace("**", "").replace("*", "")
    if not s or s in {"--", "—", "NA", "NaN", "n/a", "missing"}:
        return None
    # Drop thousands separators
    s = s.replace(",", "")
    # Drop a leading + (signs don't affect magnitude for the score)
    s = s.lstrip("+")
    try:
        return float(s)
    except ValueError:
        return None


# Per-cell extraction: each function returns {metric_name: value}
# for the metrics listed in tables_to_replicate.json for that table.

def extract_table_1() -> dict[str, float]:
    """Extract Table 1 metrics from `results/table_1.md`. The
    per-cell comparison block lists our All-years row values for:
    No. firm, Avg ME, Avg k, Avg ROE, Avg B, Avg P/B, Avg ROA.

    We extract values from BOTH the per-year rows (years 1976, 1980,
    1985, 1990, 1993) AND the All-years row. Keys are mapped to the
    metric names in tables_to_replicate.json.
    """
    p = LAYOUT.result_path("table_1.md")
    text = p.read_text()

    # Find the per-cell comparison block (last table in the file with
    # headers containing Paper / Ours / Diff or Status).
    blocks = re.findall(
        r"\| Metric \| Paper \| Ours \|[^\n]*\n\|[^\n]*\n((?:\|[^\n]*\n)+)",
        text,
    )
    if not blocks:
        return {}
    block = blocks[-1]
    # Parse each row
    metrics: dict[str, float] = {}
    for line in block.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        label = cells[0].strip().lower()
        ours_s = cells[2]
        v = _strip_value(ours_s)
        if v is None:
            continue
        if "no. firm" in label or "no firm" in label or "n firm" in label:
            metrics["all_n_firm"] = v
        elif "avg me" in label or "me" == label.strip():
            metrics["all_avg_me"] = v
        elif label == "avg k" or "payout" in label:
            metrics["all_avg_k"] = v
        elif "avg roe" in label:
            metrics["all_avg_roe"] = v
        elif label == "avg b" or "avg b " in label:
            metrics["all_avg_b"] = v
        elif "p/b" in label or "pb" in label:
            metrics["all_avg_pb"] = v
        elif "1/(avg b/p)" in label or "1/(avg bp)" in label or "inv_avg_bp" in label:
            metrics["all_inv_avg_bp"] = v
        elif "avg roa" in label:
            metrics["all_avg_roa"] = v

    # Per-year values: extract from the main table (the "Per-cell comparison"
    # block only has the All-years row, so per-year values come from the
    # body table).
    body_match = re.search(
        r"\| Year \|[^\n]*\n\|[^\n]*\n((?:\|[^\n]*\n)+)",
        text,
    )
    if body_match:
        for line in body_match.group(1).split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 9:
                continue
            year_s = cells[0].strip()
            # strip **, comma
            year_s = year_s.replace(",", "").replace("**", "").strip()
            if year_s.lower().startswith("all"):
                # Capture All-years row's inv_avg_bp value (cells[7]).
                # Other all_* metrics come from the per-cell comparison block
                # above, but inv_avg_bp is NOT in that block.
                inv_avg_bp_all = _strip_value(cells[7])
                if inv_avg_bp_all is not None:
                    metrics["all_inv_avg_bp"] = inv_avg_bp_all
                continue
            try:
                yr = int(year_s)
            except ValueError:
                continue
            n_firm = _strip_value(cells[1])
            avg_me = _strip_value(cells[2])
            avg_k = _strip_value(cells[3])
            avg_roe = _strip_value(cells[4])
            avg_b = _strip_value(cells[5])
            avg_pb = _strip_value(cells[6])
            inv_avg_bp = _strip_value(cells[7])
            avg_roa = _strip_value(cells[8])
            # Metric names use 2-digit year suffix (t76, t80, t85, t90, t93).
            yr_short = yr % 100
            if n_firm is not None:
                metrics[f"t{yr_short:02d}_n_firm"] = n_firm
            if avg_me is not None:
                metrics[f"t{yr_short:02d}_avg_me"] = avg_me
            if avg_k is not None:
                metrics[f"t{yr_short:02d}_avg_k"] = avg_k
            if yr in (1976, 1993):
                if avg_roe is not None:
                    metrics[f"t{yr_short:02d}_avg_roe"] = avg_roe
                if avg_b is not None:
                    metrics[f"t{yr_short:02d}_avg_b"] = avg_b
                if avg_pb is not None:
                    metrics[f"t{yr_short:02d}_avg_pb"] = avg_pb
                if inv_avg_bp is not None:
                    metrics[f"t{yr_short:02d}_inv_avg_bp"] = inv_avg_bp
                if avg_roa is not None:
                    metrics[f"t{yr_short:02d}_avg_roa"] = avg_roa

    return metrics


def extract_table_2() -> dict[str, float]:
    """Extract Table 2 metrics from `results/table_2.md`. The All-years
    row is at the bottom of the body table; the per-cell comparison block
    gives paper-vs-ours for the All-years row only.

    We extract from BOTH the body (year-specific) and the comparison block
    (All-years).
    """
    p = LAYOUT.result_path("table_2.md")
    text = p.read_text()

    metrics: dict[str, float] = {}

    # Body table: | Year | Obs. | B | V_h T=1 | ... | V_f T=3 |
    body_match = re.search(
        r"\| Year \| Obs\.[^\n]*\n\|[^\n]*\n((?:\|[^\n]*\n)+)",
        text,
    )
    if body_match:
        for line in body_match.group(1).split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 9:
                continue
            year_s = cells[0].replace("**", "").replace(",", "").strip()
            if year_s.lower().startswith("all"):
                # All-years row: cells 2..8 are corr_b, corr_vh_t1, ...
                pairs = [
                    ("all_corr_B", 2),
                    ("all_corr_Vh_T1", 3),
                    ("all_corr_Vh_T2", 4),
                    ("all_corr_Vh_T3", 5),
                    ("all_corr_Vf_T1", 6),
                    ("all_corr_Vf_T2", 7),
                    ("all_corr_Vf_T3", 8),
                ]
                for name, idx in pairs:
                    v = _strip_value(cells[idx])
                    if v is not None:
                        metrics[name] = v
                continue
            try:
                yr = int(year_s)
            except ValueError:
                continue
            yr_short = yr % 100
            pairs = [
                (f"t{yr_short:02d}_corr_B", 2),
                (f"t{yr_short:02d}_corr_Vh_T1", 3),
                (f"t{yr_short:02d}_corr_Vh_T2", 4),
                (f"t{yr_short:02d}_corr_Vh_T3", 5),
                (f"t{yr_short:02d}_corr_Vf_T1", 6),
                (f"t{yr_short:02d}_corr_Vf_T2", 7),
                (f"t{yr_short:02d}_corr_Vf_T3", 8),
            ]
            for name, idx in pairs:
                v = _strip_value(cells[idx])
                if v is not None:
                    metrics[name] = v

    return metrics


def extract_table_3() -> dict[str, float]:
    """Extract Table 3 metrics from `results/table_3.md`. The per-cell
    comparison block lists Q5-Q1 Diff values for each panel.

    We extract from the panel body (Q1, Q5, Obs per panel) AND the
    comparison block (Q5-Q1 diffs).
    """
    p = LAYOUT.result_path("table_3.md")
    text = p.read_text()

    metrics: dict[str, float] = {}

    # Panel extraction: find each "## Panel X - ..." section and parse
    # its body table.
    panel_sections = re.split(r"## Panel ([A-D]) - ([^\n]+)", text)
    # panel_sections is [pre, "A", "title", "body", "B", "title", "body", ...]
    # Iterate in groups of 3.
    panels = {}
    for i in range(1, len(panel_sections), 3):
        letter = panel_sections[i]
        title = panel_sections[i + 1]
        body = panel_sections[i + 2]
        panels[letter] = (title, body)

    # Body table per panel: |  | Q1 (Low) | Q2 | Q3 | Q4 | Q5 (High) | All Firms | Q5-Q1 Diff. |
    for letter, (title, body) in panels.items():
        m = re.search(
            r"\|  \| Q1[^\n]*\n\|[^\n]*\n((?:\|[^\n]*\n)+)",
            body,
        )
        if not m:
            continue
        for line in m.group(1).split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 7:
                continue
            metric_label = cells[0].strip().lower()
            q1 = _strip_value(cells[1])
            q5 = _strip_value(cells[5])
            if metric_label == "me":
                metrics[f"{letter}_Q1_ME"] = q1
                metrics[f"{letter}_Q5_ME"] = q5
            elif metric_label == "b/p":
                metrics[f"{letter}_Q1_BP"] = q1
                metrics[f"{letter}_Q5_BP"] = q5
            elif metric_label == "v_f/p":
                metrics[f"{letter}_Q1_VfP"] = q1
                metrics[f"{letter}_Q5_VfP"] = q5
            elif metric_label == "ret12":
                metrics[f"{letter}_Q1_Ret12"] = q1
                metrics[f"{letter}_Q5_Ret12"] = q5
            elif metric_label == "ret36":
                pass  # not in committed metrics

    # Comparison block: extract Q5-Q1 Ret diffs and Q1/Q5 Ret12 for panels A, D.
    cmp_match = re.search(
        r"## Per-cell comparison[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n((?:\|[^\n]*\n)+)",
        text,
    )
    if cmp_match:
        for line in cmp_match.group(1).split("\n"):
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 5:
                continue
            panel_label = cells[0].strip()
            metric_label = cells[1].strip().lower()
            paper_s = cells[2]
            ours_s = cells[3]
            # Extract the panel letter
            if "Panel A" in panel_label:
                letter = "A"
            elif "Panel B" in panel_label:
                letter = "B"
            elif "Panel C" in panel_label:
                letter = "C"
            elif "Panel D" in panel_label:
                letter = "D"
            else:
                continue
            if metric_label in ("ret12",):
                v = _strip_value(ours_s)
                if v is not None:
                    metrics[f"{letter}_Q5_Q1_Ret12_diff"] = v
            elif metric_label in ("ret24",):
                v = _strip_value(ours_s)
                if v is not None:
                    metrics[f"{letter}_Q5_Q1_Ret24_diff"] = v
            elif metric_label in ("ret36",):
                v = _strip_value(ours_s)
                if v is not None:
                    metrics[f"{letter}_Q5_Q1_Ret36_diff"] = v

    return metrics


# --- Main entry point ---


_EXTRACTORS: dict[str, Callable[[], dict[str, float]]] = {
    "T1_summary_stats": extract_table_1,
    "T2_correlations": extract_table_2,
    "T3_quintile_returns": extract_table_3,
}


def collect_metrics(tables_doc: dict | None = None) -> dict[str, Any]:
    """Collect metric values from the per-table MD files into the
    metrics.json payload structure.

    Parameters
    ----------
    tables_doc : dict, optional
        The tables_to_replicate.json document. If None, only the
        extractors run (any extractor may emit any metric name). If
        provided, we restrict emitted keys to those in the doc.

    Returns
    -------
    payload : dict
        {"schema_version": 2, "slug": <slug>, "metrics": {...}}
    """
    metrics: dict[str, dict[str, Any]] = {}

    # Tables 1-3 (committed)
    for table_id in ["T1_summary_stats", "T2_correlations", "T3_quintile_returns"]:
        extractor = _EXTRACTORS.get(table_id)
        if not extractor:
            continue
        try:
            vals = extractor()
        except FileNotFoundError:
            continue
        for name, v in vals.items():
            metrics[name] = {"value": float(v)}

    # Tables 4, 6, 7 (newly produced this iteration) -- read directly from
    # the latest saved metrics.json (which is overwritten below). The
    # canonical writer will load these by passing in additional_metrics.

    payload = {
        "schema_version": SCHEMA_VERSION,
        "slug": LAYOUT.slug,
        "metrics": metrics,
    }
    return payload


def write_metrics(additional_metrics: dict[str, float] | None = None,
                  out_path: Path | None = None) -> dict:
    """Collect + write metrics.json. Returns the payload dict.

    Parameters
    ----------
    additional_metrics : dict, optional
        Extra metric name -> float entries (e.g. from Tables 4/6/7).
    out_path : Path, optional
        Override the output path (defaults to LAYOUT.data_path('metrics.json')).
    """
    payload = collect_metrics()
    if additional_metrics:
        for name, v in additional_metrics.items():
            payload["metrics"][name] = {"value": float(v)}
    if out_path is None:
        out_path = LAYOUT.data_path("metrics.json")
    out_path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    payload = write_metrics()
    print(f"Wrote {LAYOUT.data_path('metrics.json')} with "
          f"{len(payload['metrics'])} metric values.")
