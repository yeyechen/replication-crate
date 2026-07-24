#!/usr/bin/env python3
"""Checker-panel evaluator: six targeted MiniMax checkers, a MECHANICAL
status aggregator (no model has status authority), and a composer with no
status power. Output is grade.py-compatible.

Aggregation (ordered, pure code):
  QUARANTINE if sign_legs=FAIL or construction=FAIL or leakage=FAIL
  else QUALIFIED if verification=UNVERIFIED or magnitude in
       {REGRESSION_ONLY, ATTENUATED, COLLAPSED} or data_limits=MATERIAL
  else ACCEPTED

Usage:
  python3 eval_panel.py --split dev
  python3 eval_panel.py --perturbations --out results_perturb_panel.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PANEL = HERE / "panel"
CHECKERS = ["sign_legs", "construction", "leakage", "verification",
            "magnitude", "data_limits"]
VALID = {
    "sign_legs": {"PASS", "FAIL"},
    "construction": {"PASS", "FAIL"},
    "leakage": {"PASS", "FAIL"},
    "verification": {"VERIFIED", "UNVERIFIED"},
    "magnitude": {"OK", "REGRESSION_ONLY", "ATTENUATED", "COLLAPSED"},
    "data_limits": {"NONE", "IMMATERIAL", "MATERIAL"},
}

sys.path.insert(0, str(HERE))
from eval_minimax import call_minimax, candidate_view  # noqa: E402


def strip_think(text: str) -> str:
    if "</think>" in text:
        text = text.rsplit("</think>", 1)[1]
    return text.strip()


def extract_json(text: str) -> dict | None:
    text = strip_think(text)
    start = text.find("{")
    if start < 0:
        return None
    depth = 0
    for j in range(start, len(text)):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:j + 1])
                except json.JSONDecodeError:
                    return None
    return None


def run_checker(api_key: str, name: str, evidence: str, model: str) -> dict:
    system = (PANEL / f"{name}.md").read_text()
    for attempt in (1, 2):
        try:
            body = call_minimax(api_key, system, evidence, model, 2500)
            out = extract_json(body["choices"][0]["message"].get("content", ""))
            if out and out.get("verdict") in VALID[name]:
                out["_tokens"] = body.get("usage", {}).get("total_tokens", 0)
                return out
        except Exception as exc:
            print(f"    {name} attempt {attempt}: {repr(exc)[:120]}",
                  file=sys.stderr)
            time.sleep(4 * attempt)
    return {"verdict": "PARSE_FAIL", "finding": "checker did not return valid JSON"}


def aggregate(v: dict) -> str:
    if any(v[c].get("verdict") == "FAIL"
           for c in ("sign_legs", "construction", "leakage")):
        return "QUARANTINE"
    # unparseable hard-gate checker -> conservative QUARANTINE, never silent pass
    if any(v[c].get("verdict") == "PARSE_FAIL"
           for c in ("sign_legs", "construction", "leakage")):
        return "QUARANTINE"
    if v["verification"].get("verdict") != "VERIFIED":
        return "QUALIFIED"
    if v["magnitude"].get("verdict") != "OK":
        return "QUALIFIED"
    if v["data_limits"].get("verdict") == "MATERIAL":
        return "QUALIFIED"
    return "ACCEPTED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("train", "dev", "sealed", "all"))
    ap.add_argument("--perturbations", action="store_true")
    ap.add_argument("--cases", help="external cases file (minted)")
    ap.add_argument("--model", default="MiniMax-M3")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("MINIMAX_API_KEY is not set", file=sys.stderr)
        return 2

    targets: list[dict] = []
    if args.cases:
        targets += json.loads(Path(args.cases).read_text())
    if args.perturbations:
        targets += json.loads((HERE / "perturbations.json").read_text())
    if args.split:
        cases = json.loads((HERE / "cases.json").read_text())
        targets += [c for c in cases
                    if args.split == "all" or c.get("split") == args.split]
    if not targets:
        ap.error("nothing selected")

    tag = args.perturbations and "perturb" or (args.split or "cases")
    out = Path(args.out or HERE / f"results_{tag}_panel.jsonl")
    with open(out, "w") as fh:
        for i, case in enumerate(targets):
            evidence = "CASE EVIDENCE\n" + json.dumps(
                candidate_view(case), ensure_ascii=False,
                separators=(",", ":"))
            verdicts = {c: run_checker(api_key, c, evidence, args.model)
                        for c in CHECKERS}
            status = aggregate(verdicts)
            findings = "\n".join(
                f"- [{c}] {verdicts[c].get('verdict')}: "
                f"{verdicts[c].get('finding', '')}" for c in CHECKERS)
            comp_user = (evidence + "\n\nCHECKER FINDINGS\n" + findings
                         + f"\n\nFINAL STATUS (already decided): {status}")
            body = call_minimax(api_key,
                                (PANEL / "composer.md").read_text(),
                                comp_user, args.model, 3500)
            composed = strip_think(
                body["choices"][0]["message"].get("content", ""))
            if "TRADE:" in composed:
                composed = composed[composed.index("TRADE:"):]
            answer = f"STATUS: {status}\n" + composed
            fh.write(json.dumps({
                "case_id": case["case_id"], "answer": answer,
                "panel": {c: verdicts[c].get("verdict") for c in CHECKERS},
                "findings": {c: verdicts[c].get("finding") for c in CHECKERS},
            }) + "\n")
            fh.flush()
            print(f"[{i+1}/{len(targets)}] {case['case_id']} -> {status} "
                  f"({[verdicts[c].get('verdict') for c in CHECKERS]})")
    print(f"wrote {out}; grade with: python3 {HERE}/grade.py --answers {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
