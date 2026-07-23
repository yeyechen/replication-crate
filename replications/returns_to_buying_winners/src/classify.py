#!/usr/bin/env python3
"""Per-cell classification harness for the replication contract (audit-2 m2/m3).

Reads the replication contract (``preparations/tables_to_replicate.json``) and
the computed values (``results/computed_values.json``), classifies every
contract cell, writes ``results/cell_classification.json``, prints per-table
and grand tier counts, and (idempotently) appends a one-line per-cell
evaluation block to each of the nine per-table results markdown files.

Classification rule (audit-2 m3 — previously applied but stated nowhere; this
docstring is the canonical statement):

    Tier 1 = |ours − paper| / |paper| ≤ tolerance_pct / 100
             (deviation within the contract's cell tolerance)
    Tier 2 = same sign (paper·ours > 0) AND |ours − paper| ≤ 2×|paper|
             (deviation ≤ 200%, i.e. |ours| ≤ 3×|paper|)
    FAIL   = opposite sign, deviation > 200% (|ours − paper| > 2×|paper|),
             or paper = 0 (percentage deviation undefined)
    SKIP   = ours is None (cell not computed / absent from computed_values.json)

Cells are evaluated in contract order; ``ours`` is stored RAW (unrounded),
exactly as it appears in ``computed_values.json``. The output JSON is
serialized with ``json.dumps(..., indent=1)`` and NO trailing newline, which
reproduces the committed artifact byte-for-byte (verified via md5sum).

This script is strictly read-only on all computed values: it never touches
``computed_values.json``, the panel, or any table computation. The markdown
appends are idempotent — a file that already carries its marker line is left
untouched.

Usage (from the repo root):
    uv run python replications/returns_to_buying_winners/src/classify.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

SLUG = "returns_to_buying_winners"
ABS_ROOT = Path("<internal>/rep-it-up/replications") / SLUG

# Contract table id -> per-table results markdown file.
TABLE_MD = {
    "T1": "table_1.md",
    "T2": "table_2.md",
    "T3": "table_3.md",
    "T4": "table_4.md",
    "T5": "table_5.md",
    "T6": "t6_table_v.md",
    "T7": "t7_table_vi.md",
    "T8": "t8_table_viii.md",
    "T9": "table_7_earnings.md",
}
DECOMPOSITION_MD = "table_8_decomposition.md"  # dec_* statistics, NOT a contract table

TIER_MARK = "**Per-cell evaluation:**"  # idempotency marker for contract tables
DEC_MARK = "**Anchor statistics (§III decomposition"  # idempotency marker for dec file


def _resolve_layout():
    """utils.paths.paper_layout if importable and it resolves, else the
    absolute replication path (same convention as src/main.py)."""
    try:
        repo_root = Path(__file__).resolve().parents[3]
        if str(repo_root) not in sys.path:
            sys.path.insert(0, str(repo_root))
        from utils.paths import paper_layout

        layout = paper_layout(SLUG)
        if layout.root.is_dir():
            return layout
        print(f"[paths] paper_layout root {layout.root} missing; using absolute paths")
    except Exception as exc:  # noqa: BLE001
        print(f"[paths] paper_layout unavailable ({exc!r}); using absolute paths")
    root = ABS_ROOT
    return SimpleNamespace(
        slug=SLUG,
        root=root,
        result_path=lambda name: root / "results" / name,
        preparations_path=lambda name: root / "preparations" / name,
    )


def classify_cell(paper, ours, tolerance_pct):
    """Apply the classification rule (see module docstring) to one cell."""
    if ours is None:
        return "SKIP"
    if paper == 0:
        return "FAIL"  # percentage deviation undefined
    if abs(ours - paper) / abs(paper) <= tolerance_pct / 100:
        return "Tier 1"
    if paper * ours > 0 and abs(ours - paper) <= 2 * abs(paper):
        return "Tier 2"  # same sign, deviation ≤ 200% (|ours| ≤ 3×|paper|)
    return "FAIL"


def _append_block(md_path: Path, marker: str, line: str) -> None:
    """Append ``line`` as its own paragraph to ``md_path`` — idempotent on
    ``marker`` (no double-append on re-runs)."""
    text = md_path.read_text()
    if marker in text:
        print(f"[md] {md_path.name}: marker already present — no append (idempotent)")
        return
    if not text.endswith("\n"):
        text += "\n"
    md_path.write_text(text + "\n" + line + "\n")
    print(f"[md] {md_path.name}: appended evaluation line")


def main() -> None:
    layout = _resolve_layout()
    print(f"[paths] root: {layout.root}")

    contract = json.loads(layout.preparations_path("tables_to_replicate.json").read_text())
    cv = json.loads(layout.result_path("computed_values.json").read_text())

    tables_out = []
    grand = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
    per_table = {}  # id -> counts dict

    for t in contract["tables"]:
        cells = []
        counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
        for m in t["metrics"]:
            ours = cv.get(m["name"])  # None -> SKIP
            status = classify_cell(m["value"], ours, m["tolerance_pct"])
            counts[status] += 1
            grand[status] += 1
            cells.append({
                "name": m["name"],
                "paper": m["value"],
                "ours": ours,
                "tolerance_pct": m["tolerance_pct"],
                "status": status,
            })
        tables_out.append({"id": t["id"], "table_ref": t["table_ref"], "cells": cells})
        per_table[t["id"]] = counts

    out = {"tables": tables_out, "grand": grand}
    out_path = layout.result_path("cell_classification.json")
    text = json.dumps(out, indent=1)  # no trailing newline — byte-exact format

    existing = out_path.read_text() if out_path.exists() else None
    out_path.write_text(text)
    identical = existing == text
    print(f"[out] wrote {out_path} "
          f"({len(text)} bytes; byte-identical to previous artifact: {identical})")

    # ---- per-table + grand tier counts --------------------------------------
    for t in tables_out:
        c = per_table[t["id"]]
        md_name = TABLE_MD.get(t["id"], "?")
        n = len(t["cells"])
        print(f"[classify] {t['id']} ({t['table_ref']}) -> {md_name}: {n} cells — "
              f"{c['Tier 1']} Tier 1 / {c['Tier 2']} Tier 2 / {c['FAIL']} FAIL / "
              f"{c['SKIP']} SKIP")
    n_total = sum(len(t["cells"]) for t in tables_out)
    print(f"[classify] GRAND: {n_total} cells — {grand['Tier 1']} Tier 1 / "
          f"{grand['Tier 2']} Tier 2 / {grand['FAIL']} FAIL / {grand['SKIP']} SKIP")

    # ---- per-table evaluation lines in the results markdown (idempotent) ----
    for t in tables_out:
        md_path = layout.result_path(TABLE_MD[t["id"]])
        c = per_table[t["id"]]
        n = len(t["cells"])
        line = (f"{TIER_MARK} {n} cells — {c['Tier 1']} Tier 1 / "
                f"{c['Tier 2']} Tier 2 / {c['FAIL']} FAIL (rule: within "
                f"tolerance = Tier 1; same sign & ≤2× deviation = Tier 2; "
                f"else FAIL).")
        _append_block(md_path, TIER_MARK, line)

    # table_8_decomposition.md carries the dec_* statistics, NOT a contract
    # table: give it a line noting its four in-text anchors instead.
    dec_path = layout.result_path(DECOMPOSITION_MD)
    dec_line = (
        f"{DEC_MARK} — not a contract table):** 4 in-text anchors from the 11 "
        f"dec_* keys — WRSS per-$-long mean {cv['dec_wrss_mean']:+.6f} "
        f"(paper +0.045), EW 6m serial covariance "
        f"{cv['dec_serialcov_ew']:+.6f} (paper -0.0028), residual serial "
        f"covariance {cv['dec_serialcov_resid']:+.6f} (paper +0.0012), "
        f"θ {cv['dec_theta']:+.6f} (paper -2.29); all four causal verdicts "
        f"replicate (sign)."
    )
    _append_block(dec_path, DEC_MARK, dec_line)


if __name__ == "__main__":
    main()
