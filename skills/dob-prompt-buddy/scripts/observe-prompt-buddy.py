#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from prompt_buddy_core import analyze, format_observer_report


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return " ".join(args.prompt).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Observer-style prompt coach for crypto workflows. Feed a prompt and get a concise intervention report.",
    )
    parser.add_argument("prompt", nargs="*", help="Prompt text. If omitted, stdin is used.")
    args = parser.parse_args()

    prompt = read_prompt(args)
    if not prompt:
        parser.print_help(sys.stderr)
        return 1

    print(format_observer_report(analyze(prompt)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
