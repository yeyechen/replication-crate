"""
src/evaluate.py — per-cell Tier 1/2/FAIL/SKIP per rep/TOLERANCE_RULES.md.

Loads:
  - preparations/tables_to_replicate.json (targets)
  - results/table_1.md (Table 1 replicated counts, parsed from text)
  - results/table_2.md (Table 2 replicated means)

Compares each cell to the paper target with the configured tolerance_pct,
classifies Tier 1 (within ±tol), Tier 2 (sign match, magnitude off), FAIL (sign
opposite), SKIP (missing on either side), and prints a per-cell table plus an
aggregate tally.

The printed output is what gets pasted into the iteration log and into the
results/table_<n>.md files. Hand-composing a tier table is forbidden
(rep/TOLERANCE_RULES.md).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from utils.paths import paper_layout

LAYOUT = paper_layout("balakrishnan_v2")


def parse_table_1_counts(text: str) -> dict[str, tuple[int, int]]:
    """Pull (firm_quarters, distinct_firms) for each stage from
    results/table_1.md. Reads from the FIRST table (Replicated counts)
    which has columns: Stage | ours_fq | paper_fq | flag | ours_nf | paper_nf | flag."""
    counts = {}
    stage_map = {
        "All firm-quarters with required quarterly data on Compustat and return data on CRSP during sample period 1976-2005": "primary_all",
        "With stock price five days prior to the quarterly earnings announcement date above $1": "primary_after_price1",
        "Primary tests sample with additional data constraints to compute SUE": "supp1_sue",
        "Primary tests sample with additional data constraints to compute book-to-market": "supp2_bm",
        "Primary tests sample with additional data constraints to compute accruals": "supp3_accruals",
    }
    # Skip header rows
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|--") or line.startswith("|---"):
            continue
        if "Stage" in line and "Firm-quarters" in line:
            continue  # header row
        for prefix, key in stage_map.items():
            if prefix in line:
                cells = [c.strip() for c in line.split("|")]
                # [0]='', [1]=stage, [2]=ours_fq, [3]=paper_fq, [4]=flag,
                # [5]=ours_nf, [6]=paper_nf, [7]=flag, [8]=''
                try:
                    ours_fq = int(cells[2].replace(",", ""))
                    ours_nf = int(cells[5].replace(",", ""))
                    counts[key] = (ours_fq, ours_nf)
                except (IndexError, ValueError):
                    pass
                break
    return counts


def parse_table_2_deciles(text: str) -> dict[str, dict[int, float]]:
    """Return {window: {decile: mean_bhar}}."""
    out = {}
    cur_window = None
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"### Window \[(\w+)\]", line)
        if m:
            cur_window = m.group(1)
            out[cur_window] = {}
            continue
        if cur_window is None:
            continue
        m = re.match(r"^\|\s+(\d+)\s*\|.*\|\s*(-?[\d.]+)\s*\|\s*(-?[\d.]+)\s*\|\s*$", line)
        if m:
            decile = int(m.group(1))
            mean_bhar = float(m.group(2))
            out[cur_window][decile] = mean_bhar
    return out


def parse_table_2_hedge(text: str) -> dict[str, float]:
    """Return {window: hedge_value}."""
    out = {}
    for m in re.finditer(r"### Window \[(\w+)\].*?Hedge \(D10 - D1\): ([+-]?[\d.]+)", text, flags=re.DOTALL):
        out[m.group(1)] = float(m.group(2))
    return out


def parse_table_2_tstats(text: str) -> dict[str, dict[int, float]]:
    """Return {window: {decile: t_stat}}."""
    out = {}
    cur_window = None
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"### Window \[(\w+)\]", line)
        if m:
            cur_window = m.group(1)
            out[cur_window] = {}
            continue
        if cur_window is None:
            continue
        m = re.match(r"^\|\s+(\d+)\s*\|.*\|\s*(-?[\d.]+)\s*\|\s*(-?[\d.]+)\s*\|\s*$", line)
        if m:
            decile = int(m.group(1))
            t_stat = float(m.group(3))
            out[cur_window][decile] = t_stat
    return out


def parse_table_2_hedge_tstats(text: str) -> dict[str, float]:
    """Return {window: hedge_t_stat}."""
    out = {}
    for m in re.finditer(r"### Window \[(\w+)\].*?Hedge \(D10 - D1\): [+-]?[\d.]+ \(t = ([+-]?[\d.]+)\)", text, flags=re.DOTALL):
        out[m.group(1)] = float(m.group(2))
    return out


def parse_table_2_n(text: str) -> dict[int, int]:
    """Return {decile: n} from the last 'Per-decile N' table in table_2.md.

    Note: per-decile N from the per-window tables (e.g., D1=53,951, D10=53,933)
    is also valid; we use the per-window tables as the canonical source.
    """
    out = {}
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^\|\s+(\d+)\s*\|\s+([\d,]+)\s*\|", line)
        if m:
            decile = int(m.group(1))
            n = int(m.group(2).replace(",", ""))
            out[decile] = n
    return out


def classify(ours: float, paper: float, tol_pct: float) -> str:
    """Apply the Tier ladder from rep/TOLERANCE_RULES.md.

    Near-zero rule: when |paper| < 0.005, use an absolute band of ±0.01
    (twice the printing half-width for a 4-decimal table).
    """
    if ours is None or paper is None:
        return "SKIP"
    # Near-zero handling: use absolute band ±0.01
    if abs(paper) < 0.005:
        if abs(ours - paper) <= 0.01:
            return "Tier 1"
        # Sign match (incl. both effectively zero)
        if (ours >= 0 and paper >= 0) or (ours <= 0 and paper <= 0):
            return "Tier 2"
        return "FAIL"
    # Sign disagreement → FAIL
    if (ours > 0) != (paper > 0):
        return "FAIL"
    if abs(ours - paper) / max(abs(paper), 1e-12) <= tol_pct / 100.0:
        return "Tier 1"
    # Sign match → Tier 2
    if (ours >= 0 and paper >= 0) or (ours <= 0 and paper <= 0):
        return "Tier 2"
    return "FAIL"


def main() -> int:
    targets_doc = json.loads(
        LAYOUT.preparations_path("tables_to_replicate.json").read_text()
    )
    table_1_text = LAYOUT.result_path("table_1.md").read_text()
    table_2_text = LAYOUT.result_path("table_2.md").read_text()

    # Parse replicated values
    t1_counts = parse_table_1_counts(table_1_text)
    t2_deciles = parse_table_2_deciles(table_2_text)
    t2_hedge = parse_table_2_hedge(table_2_text)
    t2_tstats = parse_table_2_tstats(table_2_text)
    t2_hedge_tstats = parse_table_2_hedge_tstats(table_2_text)
    t2_n_per_decile = parse_table_2_n(table_2_text)

    rows = []
    for tab in targets_doc["tables"]:
        for metric in tab["metrics"]:
            paper_v = metric["value"]
            tol = metric["tolerance_pct"]
            name = metric["name"]
            ours_v = None
            # Match name to replicated value
            if tab["id"] == "T1_sample_selection":
                # Names: primary_all_firmqtrs, primary_all_distinct_firms, etc.
                # Names without suffix (e.g., primary_after_price1) are
                # the firm-quarters version.
                # t1_counts has keys like 'primary_all' with (fq, nf)
                if name.endswith("_firmqtrs"):
                    stage = name.replace("_firmqtrs", "")
                    if stage in t1_counts:
                        ours_v = t1_counts[stage][0]
                elif name.endswith("_distinct_firms") or name.endswith("_firms"):
                    stage = name.replace("_distinct_firms", "").replace("_firms", "")
                    if stage in t1_counts:
                        ours_v = t1_counts[stage][1]
                elif name in t1_counts:
                    ours_v = t1_counts[name][0]
            elif tab["id"] == "T2_table2_main":
                # Names: d1_sar_m2_0, d10_sar_1_120, hedge_sar_1_120, etc.
                # N cells
                m = re.match(r"d(\d+)_high_(loss|profit)_n", name)
                if m:
                    decile_n = int(m.group(1))
                    if decile_n in t2_n_per_decile:
                        ours_v = t2_n_per_decile[decile_n]
                # FF cells: the FF column requires a per-firm Carhart 4-factor
                # regression with a 40-day estimation window prior to rdq,
                # which is not implemented. Mark all FF cells SKIP.
                if "_ff_" in name or name.startswith("hedge_ff_") or name.startswith("d1_ff_") or name.startswith("d10_ff_"):
                    ours_v = None
                # Decile-mean BHAR cells
                m = re.match(r"d(\d+)_(sar|ff)_(\w+)$", name)
                if m and "sar" in m.group(2):
                    decile_n = int(m.group(1))
                    window = m.group(3)
                    win_key = window.replace("1_", "")
                    if win_key in t2_deciles and decile_n in t2_deciles[win_key]:
                        ours_v = t2_deciles[win_key][decile_n]
                # Hedge cells
                m = re.match(r"hedge_(sar|ff)_(\w+)$", name)
                if m and "sar" in m.group(1):
                    window = m.group(2)
                    win_key = window.replace("1_", "")
                    if win_key in t2_hedge:
                        ours_v = t2_hedge[win_key]
                # Decile t-stat cells (SAR only — FF skipped)
                m = re.match(r"d(\d+)_(sar|ff)_(\w+)_t$", name)
                if m and "sar" in m.group(2):
                    decile_n = int(m.group(1))
                    window = m.group(3)
                    win_key = window.replace("1_", "")
                    if win_key in t2_tstats and decile_n in t2_tstats[win_key]:
                        ours_v = t2_tstats[win_key][decile_n]
                # Hedge t-stat cells (SAR only — FF skipped)
                m = re.match(r"hedge_(sar|ff)_(\w+)_t$", name)
                if m and "sar" in m.group(1):
                    window = m.group(2)
                    win_key = window.replace("1_", "")
                    if win_key in t2_hedge_tstats:
                        ours_v = t2_hedge_tstats[win_key]
                # FM t-stats (paper-only — we don't compute Fama-MacBeth
                # t-stats; mark SKIP)
                if "_t_fmb" in name:
                    ours_v = None

            status = classify(ours_v, paper_v, tol)
            rows.append({
                "table": tab["id"],
                "metric": name,
                "paper": paper_v,
                "ours": ours_v,
                "tolerance_pct": tol,
                "status": status,
            })

    # Per-cell table
    print(f"\n=== Per-cell evaluation ({len(rows)} cells) ===")
    print(f"{'Table':<25s} {'Metric':<28s} {'Paper':>10s} {'Ours':>12s} {'Tol%':>5s} Status")
    print("-" * 95)
    for r in rows:
        ours_str = f"{r['ours']:.4f}" if isinstance(r["ours"], (int, float)) else "—"
        print(f"{r['table']:<25s} {r['metric']:<28s} "
              f"{r['paper']:>10g} {ours_str:>12s} {r['tolerance_pct']:>5g} {r['status']}")

    # Aggregate tally
    counts = {"Tier 1": 0, "Tier 2": 0, "FAIL": 0, "SKIP": 0}
    for r in rows:
        counts[r["status"]] += 1
    n = sum(counts.values())
    print("\n=== Aggregate tally ===")
    for k, v in counts.items():
        print(f"  {k:<10s}: {v:>3d} / {n}  ({100*v/n:.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())