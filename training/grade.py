#!/usr/bin/env python3
"""Deterministic grader for MiniMax investment-result answers.

Pure code, no LLM judge: this file (plus cases.json and the frozen prompt) is
the entire supervision loop once no strong model is in the picture. FROZEN
during prompt optimization -- the optimizer may edit minimax_prompt.md, never
this file or the gold labels.

Grades an answer against its own case record:
  status      exact match to the case's gold status (or gold_status for
              perturbation cases)
  format      all five sections present, in order, nothing before STATUS
  grounding   numbers in PRIMARY RESULT must come from the case's own
              paper/candidate anchors (rounding-tolerant)
  contamination  distinctive numbers belonging only to OTHER cases' anchors
              must not appear anywhere in the answer
  legacy      no Tier/tolerance/quality-score/pass-rate vocabulary
  trade_legs  directional vocabulary of the gold TRADE (long/short/tilt...)
              must be present in the answer's TRADE

Usage:
  python3 grade.py --answers results.jsonl            # grade a run
  python3 grade.py --self-test                        # gold answers score 1.0
Each line of results.jsonl: {"case_id":..., "answer":...}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

SECTIONS = ["STATUS", "TRADE", "PRIMARY RESULT", "REASSURANCE", "CAVEATS"]
STATUS_VALUES = {"ACCEPTED", "QUALIFIED", "QUARANTINE"}
GOLD_STATUS = {"accepted": "ACCEPTED", "qualified": "QUALIFIED",
               "quarantine": "QUARANTINE"}
LEGACY_PATTERNS = [
    r"\btier\s*[12]\b", r"\btolerance (band|threshold|percent)",
    r"per-cell tolerance", r"quality score",
    r"\bpass[- ]rate", r"\b\d(?:\.\d+)?\s*/\s*5(?:\.0+)?\b",
    r"\boverall score\b",
]
DIRECTION_WORDS = ["long", "short", "overweight", "underweight", "tilt",
                   "favor", "buy", "sell"]
# numbers that are too generic to attribute to any case
GENERIC_NUMBERS = {"0", "1", "2", "3", "4", "5", "6", "9", "10", "12", "30",
                   "40", "50", "52", "100"}


def load_corpus() -> list[dict]:
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    pfile = HERE / "perturbations.json"
    if pfile.exists():
        cases = cases + json.loads(pfile.read_text(encoding="utf-8"))
    return cases


def numbers_in(obj) -> set[str]:
    """All numeric literals in a JSON fragment, normalized as strings."""
    out: set[str] = set()
    if isinstance(obj, dict):
        for v in obj.values():
            out |= numbers_in(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= numbers_in(v)
    elif isinstance(obj, (int, float)):
        out.add(repr(float(obj)))
    elif isinstance(obj, str):
        for m in re.findall(r"-?\d+(?:\.\d+)?", obj):
            out.add(repr(float(m)))
    return out


def variants(x: float) -> set[str]:
    """Rounding/percent/sign-display variants under which a grounded number
    may legitimately appear in prose."""
    vs: set[str] = set()
    for base in {x, abs(x)}:
        for v in {base, base * 100, base / 100}:  # pct <-> decimal display
            for nd in (0, 1, 2, 3, 4):
                vs.add(repr(round(v, nd)))
            vs.add(repr(v))
    return vs


def anchor_numbers(case: dict) -> set[str]:
    grounded: set[str] = set()
    for key in ("paper_anchors", "candidate_anchors", "strategy",
                "reassurance", "caveats"):
        for n in numbers_in(case.get(key)):
            grounded |= variants(float(n))
    return grounded


def parse_sections(answer: str) -> dict[str, str] | None:
    idx = []
    for s in SECTIONS:
        m = re.search(rf"^{s}:", answer, flags=re.M)
        if not m:
            return None
        idx.append((m.start(), s))
    if idx != sorted(idx):
        return None
    parts: dict[str, str] = {}
    for (start, name), nxt in zip(idx, idx[1:] + [(len(answer), None)]):
        parts[name] = answer[start + len(name) + 1: nxt[0]].strip()
    return parts


def grade_one(case: dict, answer: str, others_numbers: set[str]) -> dict:
    res: dict = {"case_id": case["case_id"]}
    parts = parse_sections(answer)
    res["format"] = 1.0 if parts else 0.0
    gold = GOLD_STATUS[case.get("status") or case.get("gold_status")]
    if not parts:
        res.update(status=0.0, grounding=0.0, contamination=0.0,
                   legacy=0.0, trade_legs=0.0, overall=0.0)
        return res

    got_raw = "".join(parts["STATUS"].split()).upper()
    got = next((s for s in STATUS_VALUES if got_raw.startswith(s)), got_raw[:12])
    res["status"] = 1.0 if got == gold else 0.0
    res["status_got"] = got

    grounded = anchor_numbers(case)
    nums = [repr(float(m)) for m in
            re.findall(r"-?\d+(?:\.\d+)?", parts["PRIMARY RESULT"])]
    nums = [n for n in nums if repr(abs(float(n))) not in
            {repr(float(g)) for g in GENERIC_NUMBERS}]
    if nums:
        hits = sum(1 for n in nums if n in grounded)
        res["grounding"] = hits / len(nums)
        res["ungrounded"] = sorted({n for n in nums if n not in grounded})
    else:
        res["grounding"] = 0.0  # a primary result with no numbers is wrong
        res["ungrounded"] = []

    foreign = others_numbers - grounded
    contam = sorted(n for n in
                    {repr(float(m)) for m in
                     re.findall(r"-?\d+(?:\.\d+)?", answer)}
                    if n in foreign)
    res["contamination"] = 0.0 if contam else 1.0
    res["contaminants"] = contam

    low = answer.lower()
    res["legacy"] = 0.0 if any(re.search(p, low) for p in LEGACY_PATTERNS) \
        else 1.0

    gold_trade = (case.get("gold_answer") or "").lower()
    m = re.search(r"trade:(.*?)(?:\nprimary result:)", gold_trade, re.S)
    want = {w for w in DIRECTION_WORDS if m and w in m.group(1)}
    have = {w for w in DIRECTION_WORDS if w in parts["TRADE"].lower()}
    res["trade_legs"] = 1.0 if not want or want <= have else \
        len(want & have) / len(want)

    res["overall"] = round(
        0.40 * res["status"] + 0.25 * res["grounding"]
        + 0.15 * res["contamination"] + 0.10 * res["legacy"]
        + 0.05 * res["format"] + 0.05 * res["trade_legs"], 4)
    return res


def build_others_numbers(corpus: list[dict], case_id: str) -> set[str]:
    out: set[str] = set()
    for c in corpus:
        if c["case_id"] != case_id and c.get("base_case_id") != case_id \
                and case_id != c.get("base_case_id"):
            for key in ("paper_anchors", "candidate_anchors"):
                out |= numbers_in(c.get(key))
    # drop numbers too short to be distinctive (e.g. 0.45, 1.05 could recur)
    return {n for n in out if len(n.replace("-", "").replace(".", "")) >= 4}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    corpus = load_corpus()
    by_id = {c["case_id"]: c for c in corpus}

    if args.self_test:
        bad = 0
        for c in corpus:
            if not c.get("gold_answer"):
                continue
            r = grade_one(c, c["gold_answer"],
                          build_others_numbers(corpus, c["case_id"]))
            flag = "" if r["overall"] >= 0.95 else "  <-- CHECK"
            if r["overall"] < 0.95:
                bad += 1
            print(f"{r['overall']:.3f} status={r['status']:.0f} "
                  f"ground={r['grounding']:.2f} contam={r['contamination']:.0f} "
                  f"{c['case_id']}{flag}")
            if flag and r.get("ungrounded"):
                print(f"       ungrounded: {r['ungrounded'][:8]}")
            if flag and r.get("contaminants"):
                print(f"       contaminants: {r['contaminants'][:8]}")
        print(f"self-test: {bad} gold answers below 0.95")
        return 1 if bad else 0

    if not args.answers:
        ap.error("--answers or --self-test required")
    rows = [json.loads(l) for l in open(args.answers) if l.strip()]
    results = []
    for row in rows:
        case = by_id[row["case_id"]]
        r = grade_one(case, row["answer"],
                      build_others_numbers(corpus, row["case_id"]))
        r["split"] = case.get("split")
        results.append(r)
        print(f"{r['overall']:.3f} status={r['status']:.0f}"
              f"({r.get('status_got','')}) ground={r['grounding']:.2f} "
              f"contam={r['contamination']:.0f} legacy={r['legacy']:.0f} "
              f"[{case.get('split')}] {r['case_id']}")
    for split in ("train", "dev", "sealed", None):
        sel = [r for r in results if r.get("split") == split]
        if sel:
            print(f"{split or 'perturb'}: mean overall "
                  f"{sum(r['overall'] for r in sel)/len(sel):.3f} "
                  f"status acc {sum(r['status'] for r in sel)/len(sel):.2f} "
                  f"n={len(sel)}")
    out = Path(args.answers).with_suffix(".graded.json")
    out.write_text(json.dumps(results, indent=1))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
