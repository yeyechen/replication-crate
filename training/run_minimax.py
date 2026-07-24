#!/usr/bin/env python3
"""Run one direct MiniMax investment-result extraction pilot."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


HERE = Path(__file__).resolve().parent
API_URL = "https://api.minimax.io/v1/chat/completions"


def load_cases() -> list[dict]:
    return json.loads((HERE / "cases.json").read_text(encoding="utf-8"))


def candidate_view(case: dict) -> dict:
    hidden = {"gold_answer", "split", "status", "status_reason"}
    return {key: value for key, value in case.items() if key not in hidden}


def render(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def build_messages(target: dict, mode: str) -> list[dict]:
    if mode == "baseline":
        return [
            {
                "role": "system",
                "content": (
                    "Summarize the investment strategy and replication result "
                    "from the supplied evidence. Be concise and accurate."
                ),
            },
            {
                "role": "user",
                "content": render(candidate_view(target)),
            },
        ]

    return [
        {
            "role": "system",
            "content": (HERE / "minimax_prompt.md").read_text(encoding="utf-8"),
        },
        {
            "role": "user",
            "content": "CASE EVIDENCE\n" + render(candidate_view(target)),
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", required=True, dest="case_id")
    parser.add_argument(
        "--mode",
        choices=("baseline", "rules"),
        default="rules",
    )
    parser.add_argument("--model", default="MiniMax-M3")
    parser.add_argument("--max-tokens", type=int, default=2400)
    args = parser.parse_args()

    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        print("MINIMAX_API_KEY is not set", file=sys.stderr)
        return 2

    cases = load_cases()
    target = next((case for case in cases if case["case_id"] == args.case_id), None)
    if target is None:
        print(f"Unknown case: {args.case_id}", file=sys.stderr)
        return 2

    request_body = {
        "model": args.model,
        "messages": build_messages(target, args.mode),
        "max_tokens": args.max_tokens,
        "reasoning_split": True,
    }
    request = Request(
        API_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"MiniMax API error {exc.code}: {detail}", file=sys.stderr)
        return 1
    result = {
        "case_id": args.case_id,
        "mode": args.mode,
        "model": body.get("model", args.model),
        "answer": body["choices"][0]["message"].get("content", ""),
        "usage": body.get("usage", {}),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
