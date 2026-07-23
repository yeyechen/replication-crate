"""
Dual-scheme tier evaluation of committed metrics (audit-1 issues M3 + m7).

Reads ONLY preparations/tables_to_replicate.json (8 tables, 1,613 committed
metrics) and results/cells_*.json (our computed values) — no ClickHouse, no
panel access. Classifies every committed metric under BOTH schemes and emits
results/evaluation_summary.json (overwritten).

Classification rules
--------------------
repo_rules — per rep/TOLERANCE_RULES.md:
    Tier1:  |ours - paper| / |paper| <= tolerance_pct / 100
    Tier2:  sign matches but magnitude outside tolerance (ANY magnitude;
            the repo definition has no 2x bound — there is no "T2x" bucket
            under these rules)
    FAIL:   sign opposite
    SKIP:   either side missing

rubric_rules — per audit/RUBRIC.md spot-check 10 (the audit's strict rule):
    Tier1:  same tolerance test as repo_rules
    Tier2:  sign matches AND ratio |ours/paper| in [0.5, 2.0]
    FAIL:   everything else (sign flip, OR a sign-matching ratio outside
            [0.5, 2.0])
    SKIP:   either side missing

Near-zero paper values (|paper| < 1e-9 — the paper prints exactly 0.0 for
7 of the 1,613 committed metrics): the relative-error and ratio formulas
divide by |paper| and are undefined at 0, so a dedicated rule applies:
    |ours| < 1e-4  ->  Tier1 under both schemes (effectively zero vs zero:
                       a match);
    |ours| >= 1e-4 ->  the paper's exact 0.0 is treated as non-negative for
                       the sign test. ours < 0 is a sign flip: FAIL under
                       both schemes. ours >= 0 SIGN-MATCHES: Tier2 under
                       repo_rules; also Tier2 under rubric_rules — the
                       rubric FAIL set is "sign flips, or sign-matching
                       ratio outside [0.5, 2.0]", and at paper = 0 the
                       ratio |ours/paper| is UNDEFINED (not a number
                       outside the band), so a sign-matching near-zero
                       cell is vacuously not a rubric FAIL and falls to
                       Tier2.
This convention is exactly the one used in the audit-1 tallies (sign flips
cannot occur at paper = 0), and reproduces the audit-1 anchor counts below.

Output: results/evaluation_summary.json
    {"repo_rules":   {"per_table": {<table id>: {"Tier1","Tier2","FAIL","SKIP"}},
                      "total": {...}},
     "rubric_rules": {"per_table": {...}, "total": {...}},
     "notes": "<semantics + near-zero rule + anchor verification>"}

Table ids are iterated from the JSON (not hardcoded).

VERIFY — audit-1 anchor counts (original four tables T1/T2/T3/T7):
  repo_rules:   total Tier1 = 319; FAIL (sign flips) = 143;
                per-table FAIL: T1=0, T2=21, T3=52, T7=70
  rubric_rules: Tier1 = 319, Tier2 = 184, FAIL = 403
The script asserts all of the above and prints the full eight-table totals
under both schemes.

Usage:  python3 src/evaluate.py
"""
from __future__ import annotations

import json
from pathlib import Path

# ────────────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
TABLES_JSON = ROOT / "preparations" / "tables_to_replicate.json"
RESULTS_DIR = ROOT / "results"
OUT_PATH = RESULTS_DIR / "evaluation_summary.json"

NEAR_ZERO_PAPER = 1e-9   # |paper| below this => near-zero rule
NEAR_ZERO_OURS = 1e-4    # |ours| below this (paper ~ 0) => Tier1 match
RATIO_LO, RATIO_HI = 0.5, 2.0   # rubric Tier-2 magnitude band

# Audit-1 anchors (original committed set; the four tables present in
# iteration 1's evaluation_summary.json). Used ONLY for verification — the
# classification loop iterates whatever the JSON contains.
ANCHOR_TABLES = ["T1", "T2", "T3", "T7"]
BUCKETS = ["Tier1", "Tier2", "FAIL", "SKIP"]


# ────────────────────────────────────────────────────────────────────────────
def same_sign(paper: float, ours: float) -> bool:
    """True if the signs are compatible. For non-zero paper this is the
    strict sign test; a paper value of exactly 0.0 is non-negative, so any
    ours >= 0 sign-matches it (the near-zero rule handles the magnitude)."""
    return (paper >= 0 and ours >= 0) or (paper <= 0 and ours <= 0)


def classify_repo(paper, ours, tol_pct) -> str:
    """repo_rules tier per rep/TOLERANCE_RULES.md (see module docstring)."""
    if paper is None or ours is None:
        return "SKIP"
    if abs(paper) < NEAR_ZERO_PAPER:
        if abs(ours) < NEAR_ZERO_OURS:
            return "Tier1"
        return "Tier2" if ours >= 0 else "FAIL"   # 0.0 is non-negative
    if abs(ours - paper) / abs(paper) <= tol_pct / 100.0:
        return "Tier1"
    if same_sign(paper, ours):
        return "Tier2"   # any magnitude — repo Tier 2 has no 2x bound
    return "FAIL"


def classify_rubric(paper, ours, tol_pct) -> str:
    """rubric_rules tier per audit/RUBRIC.md spot-check 10."""
    if paper is None or ours is None:
        return "SKIP"
    if abs(paper) < NEAR_ZERO_PAPER:
        if abs(ours) < NEAR_ZERO_OURS:
            return "Tier1"
        # ours < 0 is a sign flip => FAIL. ours >= 0 sign-matches; the
        # ratio |ours/paper| is UNDEFINED at paper = 0 — not a ratio
        # outside [0.5, 2.0] — so the cell is not a rubric FAIL and
        # falls to Tier2 (matches the audit-1 tally).
        return "FAIL" if ours < 0 else "Tier2"
    if abs(ours - paper) / abs(paper) <= tol_pct / 100.0:
        return "Tier1"
    if same_sign(paper, ours):
        ratio = abs(ours / paper)
        if RATIO_LO <= ratio <= RATIO_HI:
            return "Tier2"
        return "FAIL"
    return "FAIL"


# ────────────────────────────────────────────────────────────────────────────
def main() -> None:
    tables = json.loads(TABLES_JSON.read_text())["tables"]

    ours: dict = {}
    cell_files = sorted(RESULTS_DIR.glob("cells_*.json"))
    assert cell_files, f"no results/cells_*.json found under {RESULTS_DIR}"
    for f in cell_files:
        ours.update(json.loads(f.read_text()))

    per_table = {"repo_rules": {}, "rubric_rules": {}}
    n_metrics = 0
    n_near_zero = 0
    for tbl in tables:                       # JSON order — no hardcoded ids
        tid = tbl["id"]
        repo = {b: 0 for b in BUCKETS}
        rubr = {b: 0 for b in BUCKETS}
        for m in tbl["metrics"]:
            n_metrics += 1
            paper, our = m["value"], ours.get(m["name"])
            tol = m["tolerance_pct"]
            if paper is not None and abs(paper) < NEAR_ZERO_PAPER:
                n_near_zero += 1
            repo[classify_repo(paper, our, tol)] += 1
            rubr[classify_rubric(paper, our, tol)] += 1
        per_table["repo_rules"][tid] = repo
        per_table["rubric_rules"][tid] = rubr

    total = {scheme: {b: sum(per_table[scheme][t][b] for t in per_table[scheme])
                      for b in BUCKETS}
             for scheme in per_table}

    # ── VERIFY: audit-1 anchor counts on the original four tables ──
    def sub4(scheme):
        agg = {b: 0 for b in BUCKETS}
        for tid in ANCHOR_TABLES:
            if tid in per_table[scheme]:
                for b in BUCKETS:
                    agg[b] += per_table[scheme][tid][b]
        return agg

    repo4, rubr4 = sub4("repo_rules"), sub4("rubric_rules")
    print("=== VERIFY: audit-1 anchors (original four tables "
          f"{[t for t in ANCHOR_TABLES if t in per_table['repo_rules']]}) ===")
    checks = [
        ("repo  Tier1 total == 319", repo4["Tier1"], 319),
        ("repo  FAIL total  == 143", repo4["FAIL"], 143),
        ("repo  T1 FAIL == 0",  per_table["repo_rules"]["T1"]["FAIL"], 0),
        ("repo  T2 FAIL == 21", per_table["repo_rules"]["T2"]["FAIL"], 21),
        ("repo  T3 FAIL == 52", per_table["repo_rules"]["T3"]["FAIL"], 52),
        ("repo  T7 FAIL == 70", per_table["repo_rules"]["T7"]["FAIL"], 70),
        ("rubric Tier1 == 319", rubr4["Tier1"], 319),
        ("rubric Tier2 == 184", rubr4["Tier2"], 184),
        ("rubric FAIL  == 403", rubr4["FAIL"], 403),
    ]
    for label, got, want in checks:
        status = "PASS" if got == want else "FAIL"
        print(f"  [{status}] {label} (got {got})")
        assert got == want, f"anchor check failed: {label} — got {got}, want {want}"

    notes = (
        "Generated by src/evaluate.py from preparations/tables_to_replicate.json "
        f"({len(tables)} tables, {n_metrics} committed metrics) and "
        f"{len(cell_files)} results/cells_*.json files. "
        "repo_rules (rep/TOLERANCE_RULES.md): Tier1 = |ours-paper|/|paper| <= "
        "tolerance_pct/100; Tier2 = sign matches, any magnitude; FAIL = sign "
        "opposite; SKIP = missing. rubric_rules (audit/RUBRIC.md spot-check 10): "
        "Tier1 = same; Tier2 = sign matches AND |ours/paper| in [0.5, 2.0]; "
        "FAIL = everything else; SKIP = missing. "
        f"Near-zero rule ({n_near_zero} metrics with |paper| < 1e-9, all printed "
        "as exactly 0.0): |ours| < 1e-4 -> Tier1; else ours >= 0 -> sign-matching "
        "(repo Tier2; rubric Tier2, since the ratio |ours/paper| is undefined at "
        "paper=0 and is therefore vacuously not a ratio outside [0.5, 2.0]); "
        "ours < 0 -> FAIL in both schemes. This convention reproduces the "
        "audit-1 anchors exactly: "
        "original four tables give repo Tier1=319/FAIL=143 (per-table FAIL "
        "T1=0, T2=21, T3=52, T7=70) and rubric Tier1=319/Tier2=184/FAIL=403 — "
        "all asserted in the script. Under repo_rules, Tier2 subsumes the "
        "iteration-1 'T2x' bucket (the repo definition has no 2x bound)."
    )

    summary = {
        "repo_rules": {"per_table": per_table["repo_rules"],
                       "total": total["repo_rules"]},
        "rubric_rules": {"per_table": per_table["rubric_rules"],
                         "total": total["rubric_rules"]},
        "notes": notes,
    }
    OUT_PATH.write_text(json.dumps(summary, indent=2) + "\n")

    # ── report: full eight-table totals under both schemes ──
    print(f"\n=== Eight-table evaluation ({n_metrics} metrics, "
          f"{n_near_zero} near-zero paper cells) ===")
    for scheme in ["repo_rules", "rubric_rules"]:
        print(f"\n[{scheme}]")
        print(f"  {'table':6s} {'Tier1':>6s} {'Tier2':>6s} {'FAIL':>6s} "
              f"{'SKIP':>6s} {'total':>7s}")
        for tid in per_table[scheme]:
            c = per_table[scheme][tid]
            n = sum(c.values())
            print(f"  {tid:6s} {c['Tier1']:6d} {c['Tier2']:6d} {c['FAIL']:6d} "
                  f"{c['SKIP']:6d} {n:7d}")
        c = total[scheme]
        n = sum(c.values())
        print(f"  {'TOTAL':6s} {c['Tier1']:6d} {c['Tier2']:6d} {c['FAIL']:6d} "
              f"{c['SKIP']:6d} {n:7d}")

    print(f"\nWrote: {OUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
