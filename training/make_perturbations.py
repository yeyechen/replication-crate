#!/usr/bin/env python3
"""Generate boundary-teaching perturbation cases from the gold corpus.

Each perturbation copies a real record and corrupts (or strips) exactly one
aspect, with a hand-assigned gold status. These teach the accept/qualify/
quarantine BOUNDARY rather than the roster of real cases, so the optimizer
cannot score well by memorizing the 16 papers. Run once; output is
perturbations.json (committed for review -- regenerate only via this script).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
cases = {c["case_id"]: c for c in
         json.loads((HERE / "cases.json").read_text())}


def derive(base_id: str, new_id: str, gold: str, why: str, edit) -> dict:
    p = copy.deepcopy(cases[base_id])
    for k in ("gold_answer", "status", "status_reason", "split"):
        p.pop(k, None)
    edit(p)
    p["case_id"] = new_id
    p["base_case_id"] = base_id
    p["gold_status"] = gold
    p["perturbation"] = why
    return p


out = []

# P1: strip all independent verification from a clean accepted case.
# The trade is unchanged, but the primary result now rests solely on the
# candidate's own claim -> qualified, not accepted and not quarantine.
def p1(p):
    p["verification_level"] = ("report_only; no independent recomputation "
                               "was performed; the data cache is absent from "
                               "the checkout")
    p["reassurance"] = [b for b in p["reassurance"]
                        if "auditor" not in b.lower()
                        and "independently" not in b.lower()]
    p["caveats"] = [c for c in p["caveats"]
                    if "recomputation" not in c.lower()
                    and "audit" not in c.lower()] + [
        "No audit or independent recomputation of any kind has been "
        "performed on this candidate's outputs."]
out.append(derive(
    "returns_to_buying_winners", "perturb_momentum_unverified", "qualified",
    "verification stripped: no independent recomputation anywhere; "
    "primary result rests on the candidate's own report", p1))

# P2: wrong signal construction on the primary trade -> quarantine,
# regardless of how good the headline numbers look.
def p2(p):
    p["strategy"]["signal"] = (
        "rolling market beta from a single 5-year monthly-return OLS "
        "regression, with no separate volatility/correlation windows and "
        "no Vasicek shrinkage")
    p["caveats"] = [
        "The beta estimator differs from the paper's one-year-volatility "
        "times five-year-correlation construction with Vasicek shrinkage; "
        "the ranking variable is therefore not the paper's signal."
    ] + p["caveats"]
out.append(derive(
    "betting_against_beta", "perturb_bab_wrong_signal", "quarantine",
    "signal construction contradicts the paper's estimator; defect touches "
    "the primary ranking variable", p2))

# P3: candidate anchors coincide with the paper to reported precision AND
# the record discloses the candidate saw the targets -> quarantine
# (numerical closeness must not be rewarded when targets leaked).
def p3(p):
    ca, pa = p["candidate_anchors"], p["paper_anchors"]
    for k, v in pa.items():
        if isinstance(v, (int, float)) and k in ca:
            ca[k] = v
    for k in list(ca):
        if isinstance(ca[k], (int, float)) and k not in pa:
            pass  # leave non-target metrics alone
    p["verification_level"] = (
        "the paper's target values were available to the candidate during "
        "generation; no independent recomputation was performed")
    p["caveats"] = ["Candidate outputs match the paper's reported values "
                    "exactly at every reported digit."] + p["caveats"]
out.append(derive(
    "the_other_side_of_value", "perturb_profitability_target_copy",
    "quarantine",
    "targets leaked to candidate and outputs match paper exactly; "
    "closeness alone must not be rewarded", p3))

# P4: reassurance entirely stripped from a verified accepted case ->
# STAYS accepted (missing reassurance is not a defect). Tests
# over-conservatism.
def p4(p):
    p["reassurance"] = []
    p["caveats"] = p["caveats"] + [
        "No corollary or robustness evidence is included in this record."]
out.append(derive(
    "asset_growth_and_the_cross_section_of_stock_returns",
    "perturb_asset_growth_no_reassurance", "accepted",
    "reassurance removed entirely; a verified primary result without "
    "corollaries is still acceptable", p4))

# P5: stated position direction contradicts the record's own anchors
# (legs silently reversed) -> quarantine.
def p5(p):
    p["strategy"]["position"] = (
        "long the loser portfolio (stocks farthest below their 52-week "
        "high) and short the winner portfolio (stocks nearest their "
        "52-week high)")
out.append(derive(
    "the_52_week_high_and_momentum_investing", "perturb_52wh_reversed_legs",
    "quarantine",
    "position direction reversed relative to the record's own positive "
    "winner-minus-loser anchors; sign inconsistency inside the record", p5))

(HERE / "perturbations.json").write_text(json.dumps(out, indent=1))
print(f"wrote {len(out)} perturbations")
for p in out:
    print(f"  {p['gold_status']:<10} {p['case_id']}  (base {p['base_case_id']})")
