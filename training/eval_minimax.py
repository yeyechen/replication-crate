#!/usr/bin/env python3
"""Run MiniMax over the corpus (and perturbations) and grade the answers.

Stdlib only. Needs MINIMAX_API_KEY. The prompt file is the ONLY thing the
optimization loop may vary (pass --prompt to test a candidate prompt without
touching the committed one); cases, gold labels, and grade.py stay frozen.

  python3 eval_minimax.py --split train
  python3 eval_minimax.py --split dev --prompt candidate_prompt.md
  python3 eval_minimax.py --perturbations         # boundary set
  python3 eval_minimax.py --split sealed --once   # scored once, at the end
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
API_URL = "https://api.minimax.io/v1/chat/completions"


def candidate_view(case: dict) -> dict:
    hidden = {"gold_answer", "split", "status", "status_reason",
              "gold_status", "base_case_id", "perturbation"}
    return {k: v for k, v in case.items() if k not in hidden}


def call_minimax(api_key: str, system: str, user: str, model: str,
                 max_tokens: int) -> dict:
    # NOTE: no reasoning_split -- that flag splits reasoning/content at an
    # arbitrary token boundary, chopping the head off the answer. Without it
    # the content is "<think>...</think>" + answer, which parses cleanly.
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "max_tokens": max_tokens,
    }
    req = Request(API_URL, data=json.dumps(body).encode(),
                  headers={"Authorization": f"Bearer {api_key}",
                           "Content-Type": "application/json"},
                  method="POST")
    with urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", choices=("train", "dev", "sealed", "all"))
    ap.add_argument("--perturbations", action="store_true")
    ap.add_argument("--prompt", default=str(HERE / "minimax_prompt.md"))
    ap.add_argument("--model", default="MiniMax-M3")
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--out", default=None)
    ap.add_argument("--once", action="store_true",
                    help="refuse to run if an output file already exists "
                         "(sealed-set discipline)")
    args = ap.parse_args()

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("MINIMAX_API_KEY is not set", file=sys.stderr)
        return 2

    cases = json.loads((HERE / "cases.json").read_text())
    targets: list[dict] = []
    if args.perturbations:
        targets += json.loads((HERE / "perturbations.json").read_text())
    if args.split:
        targets += [c for c in cases
                    if args.split == "all" or c.get("split") == args.split]
    if not targets:
        ap.error("nothing selected: pass --split and/or --perturbations")

    tag = args.perturbations and "perturb" or args.split
    out = Path(args.out or HERE / f"results_{tag}_{Path(args.prompt).stem}.jsonl")
    if args.once and out.exists():
        print(f"{out} already exists and --once was set; refusing to rerun",
              file=sys.stderr)
        return 3

    system = Path(args.prompt).read_text()
    with open(out, "w") as fh:
        for i, case in enumerate(targets):
            user = "CASE EVIDENCE\n" + json.dumps(
                candidate_view(case), ensure_ascii=False,
                separators=(",", ":"))
            for attempt in (1, 2, 3):
                try:
                    body = call_minimax(api_key, system, user, args.model,
                                        args.max_tokens)
                    break
                except Exception as exc:  # HTTP errors, timeouts, resets
                    detail = exc.read().decode(errors="replace")[:200] \
                        if isinstance(exc, HTTPError) else repr(exc)[:200]
                    print(f"  retry {attempt} {case['case_id']}: {detail}",
                          file=sys.stderr)
                    time.sleep(5 * attempt)
            else:
                print(f"  FAILED {case['case_id']}", file=sys.stderr)
                continue
            full = body["choices"][0]["message"].get("content", "")
            answer = full
            if "</think>" in answer:
                answer = answer.rsplit("</think>", 1)[1].strip()
            if "STATUS:" not in answer and "STATUS:" in full:
                # stray think tag inside the answer; recover from full text
                answer = full[full.index("STATUS:"):].replace("</think>", "")
            if "STATUS:" not in answer:
                # reasoning ate the whole budget; one retry with more room
                try:
                    body = call_minimax(api_key, system, user, args.model,
                                        args.max_tokens + 3000)
                    answer = body["choices"][0]["message"].get("content", "")
                    if "</think>" in answer:
                        answer = answer.rsplit("</think>", 1)[1].strip()
                except Exception as exc:
                    print(f"  big-budget retry failed {case['case_id']}: "
                          f"{repr(exc)[:150]}", file=sys.stderr)
            fh.write(json.dumps({
                "case_id": case["case_id"], "answer": answer,
                "usage": body.get("usage", {}),
                "prompt": Path(args.prompt).name}) + "\n")
            fh.flush()
            print(f"[{i+1}/{len(targets)}] {case['case_id']} "
                  f"({body.get('usage', {}).get('total_tokens', '?')} tok)")
            time.sleep(1)
    print(f"wrote {out}; now: python3 {HERE}/grade.py --answers {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
