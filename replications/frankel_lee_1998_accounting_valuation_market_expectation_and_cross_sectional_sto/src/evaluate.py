"""Evaluator: prints per-cell tier status + aggregate tally for the
Frankel & Lee (1998) replication.

Reads:
- preparations/tables_to_replicate.json (target cells with paper value + tolerance)
- results/table_1.md, table_2.md, table_3.md (computed values)

Per the rep-it-up TOLERANCE_RULES.md:
- Tier 1: |ours - paper| / |paper| <= tolerance_pct/100
- Tier 2: |ours - paper| / |paper| <= 2 × tolerance_pct/100, OR sign matches magnitude differs
- FAIL: otherwise
- MISSING: cell not produced (paper not replicated)

Loss: L = (2*FAIL + 2*MISSING + 1*Tier2) / (Tier1 + Tier2 + FAIL + MISSING)
"""
import json
import re
from pathlib import Path

PROJECT_ROOT = Path("/home/ra_alan_mike_share/rep-it-up")
SLUG = "frankel_lee_1998_accounting_valuation_market_expectation_and_cross_sectional_sto"
REP = PROJECT_ROOT / "replications" / SLUG


def parse_results_table(md_path: Path, table_id: str) -> dict:
    """Parse a results/table_N.md file to extract computed values keyed by metric name."""
    if not md_path.exists():
        return {}
    text = md_path.read_text()
    out = {}
    # Pattern 1: table_1.md uses | metric | value | unit | ... rows
    # Pattern 2: table_2.md uses | Year t | No. firm | Avg ME | ... rows
    # Pattern 3: table_3.md has Panel A/B/C/D with quintile rows
    # Try to find numeric values keyed by surrounding metric/header labels.
    # For simplicity, parse any "metric | value" rows.
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("|==="):
            continue
        # Skip header rows: e.g., "Year | No. firm | Avg ME"
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    # Heuristic: extract first numeric column per row, keyed by column header.
    if not rows:
        return {}
    # Find header row (first non-empty row)
    header = rows[0]
    # Skip header + separator
    data_rows = [r for r in rows[1:] if r and any(c for c in r)]
    if not data_rows:
        return {}
    # Build a flat dict of metric -> value, using "row_label col_header" as key.
    metrics = {}
    for r in data_rows:
        if len(r) < 2:
            continue
        row_label = r[0]
        for col_idx in range(1, min(len(r), len(header))):
            col_label = header[col_idx]
            val_str = r[col_idx].replace(",", "").replace("$", "").replace("*", "").strip()
            try:
                val = float(val_str)
                key = f"{row_label}|{col_label}".lower()
                metrics[key] = val
            except ValueError:
                continue
    return metrics


def main():
    targets_path = REP / "preparations" / "tables_to_replicate.json"
    targets = json.loads(targets_path.read_text())

    # Build a flat list of cells with their paper values, tolerances, and our computed values
    all_cells = []
    for table in targets["tables"]:
        table_id = table["id"]
        results_md = REP / "results" / f"{table_id_to_filename(table_id)}.md"
        computed = parse_results_table(results_md, table_id)
        for metric in table["metrics"]:
            name = metric["name"]
            paper_val = metric["value"]
            tol_pct = metric["tolerance_pct"]
            unit = metric.get("unit", "")
            # Try several key patterns to find our value
            ours_val = None
            for key_pattern in [name, name.replace("_", " "), name.lower()]:
                if key_pattern in computed:
                    ours_val = computed[key_pattern]
                    break
            if ours_val is None:
                # try fuzzy match on tokens
                tokens = set(name.lower().split("_"))
                best = None
                best_score = 0
                for k, v in computed.items():
                    k_tokens = set(re.findall(r"[a-z0-9]+", k))
                    score = len(tokens & k_tokens)
                    if score > best_score:
                        best_score = score
                        best = v
                if best_score >= 1:
                    ours_val = best
            all_cells.append({
                "table": table_id,
                "metric": name,
                "paper": paper_val,
                "ours": ours_val,
                "tol_pct": tol_pct,
                "unit": unit,
            })

    # Per-cell status
    n_t1 = n_t2 = n_fail = n_missing = 0
    print(f"{'Table':<22} {'Metric':<32} {'Paper':>12} {'Ours':>12} {'Status':<10}")
    print("-" * 92)
    for c in all_cells:
        paper = c["paper"]
        ours = c["ours"]
        tol_pct = c["tol_pct"]
        if ours is None:
            status = "MISSING"
            n_missing += 1
        else:
            if paper == 0:
                # avoid divide by zero: use absolute tolerance
                if abs(ours - paper) <= 0.005 * (tol_pct / 10):
                    status = "Tier 1"
                    n_t1 += 1
                elif abs(ours - paper) <= 0.01 * (tol_pct / 10):
                    status = "Tier 2"
                    n_t2 += 1
                else:
                    status = "FAIL"
                    n_fail += 1
            else:
                rel_err = abs(ours - paper) / abs(paper)
                if rel_err <= tol_pct / 100:
                    status = "Tier 1"
                    n_t1 += 1
                elif rel_err <= 2 * tol_pct / 100:
                    status = "Tier 2"
                    n_t2 += 1
                else:
                    status = "FAIL"
                    n_fail += 1
        ours_str = f"{ours:.4g}" if ours is not None else "—"
        paper_str = f"{paper:.4g}"
        print(f"{c['table']:<22} {c['metric']:<32} {paper_str:>12} {ours_str:>12} {status:<10}")

    total = n_t1 + n_t2 + n_fail + n_missing
    print("-" * 92)
    print(f"{'TOTAL':<22} {'':<32} {'':<12} {'':<12} {'':<10}")
    print(f"Tier 1:     {n_t1:>3}")
    print(f"Tier 2:     {n_t2:>3}")
    print(f"FAIL:       {n_fail:>3}")
    print(f"MISSING:    {n_missing:>3}")
    print(f"Total cells: {total:>3}")
    if total > 0:
        L = (2 * n_fail + 2 * n_missing + 1 * n_t2) / total
        print(f"Loss L:     {L:.4f}  (L=0 iff every cell Tier 1)")


def table_id_to_filename(table_id: str) -> str:
    # T1_summary_stats -> table_1, T3_quintile_returns -> table_3, etc.
    m = re.match(r"^T(\d+)", table_id)
    if m:
        return f"table_{m.group(1)}"
    return table_id


if __name__ == "__main__":
    main()
