#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"

KNOWN_CHAINS = [
    "ethereum",
    "base",
    "arbitrum",
    "optimism",
    "solana",
    "bsc",
    "bnb",
    "polygon",
    "avax",
    "avalanche",
    "hyperliquid",
    "blast",
    "berachain",
]

ACTION_WORDS = [
    "analyze",
    "review",
    "scan",
    "compare",
    "summarize",
    "explain",
    "plan",
    "debug",
    "write",
    "draft",
    "audit",
    "map",
    "find",
    "return",
    "list",
    "build",
    "implement",
]

FORMAT_MARKERS = [
    "return",
    "format",
    "json",
    "table",
    "csv",
    "bullet",
    "bullets",
    "steps",
    "sections",
    "columns",
    "checklist",
    "score",
]

VERIFY_MARKERS = [
    "verify",
    "verification",
    "evidence",
    "facts",
    "fact",
    "sources",
    "citations",
    "assumptions",
    "observable",
    "red flags",
    "test",
    "checks",
]

CONTEXT_MARKERS = [
    "repo",
    "file",
    "files",
    "folder",
    "directory",
    "env",
    "environment",
    "constraints",
    "budget",
    "chain",
    "token",
    "wallet",
    "protocol",
]

PLAN_MARKERS = [
    "plan",
    "steps",
    "sequence",
    "phase",
    "first",
    "then",
    "outline",
    "approach",
    "prioritize",
]

WALLET_RE = re.compile(r"0x[a-fA-F0-9]{8,}")
TOKEN_RE = re.compile(r"\b[A-Z]{2,10}\b")


class Finding(dict):
    @property
    def label(self) -> str:
        return self["label"]


def has_any(text: str, phrases: list[str]) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def detect_domain(prompt: str) -> str:
    lowered = prompt.lower()
    if WALLET_RE.search(prompt) or "wallet" in lowered or "address" in lowered:
        return "wallet-review"
    if any(word in lowered for word in ["yield", "apy", "farm", "farming", "lending", "stablecoin yield", "vault"]):
        return "yield-scan"
    if any(word in lowered for word in ["token", "coin", "ticker", "contract", "liquidity", "holder", "holders", "legit"]):
        return "token-dd"
    return "general"


def detect_chain(prompt: str) -> str | None:
    lowered = prompt.lower()
    for chain in KNOWN_CHAINS:
        if chain in lowered:
            return chain
    return None


def prompt_stub(domain: str, prompt: str) -> str:
    chain = detect_chain(prompt)
    wallet = WALLET_RE.search(prompt)
    upper_tokens = [t for t in TOKEN_RE.findall(prompt) if t not in {"JSON", "CSV", "API", "CLI"}]

    if domain == "wallet-review":
        wallet_value = wallet.group(0) if wallet else "<ADDRESS>"
        chain_value = chain or "<CHAIN>"
        return (
            f"Analyze wallet {wallet_value} on {chain_value}. Return: balance picture, transfer behavior, "
            "protocol exposure, suspicious signs, and next checks. Keep claims tied to observable behavior and do not invent wallet labels."
        )

    if domain == "yield-scan":
        chain_value = chain or "<CHAIN OR NICHE>"
        return (
            f"Scan {chain_value} for yield options relevant to <CAPITAL SIZE> and <RISK PROFILE>. "
            "Return: candidates, yield source, TVL/liquidity questions, risks, and what to verify. Do not rank by APY alone."
        )

    if domain == "token-dd":
        token_value = upper_tokens[0] if upper_tokens else "<TOKEN>"
        chain_value = chain or "<CHAIN>"
        return (
            f"Review {token_value} on {chain_value}. Return: what it is, legitimacy questions, liquidity questions, "
            "concentration risks, red flags, and 3 next checks. Separate facts from assumptions."
        )

    return (
        "Task: <specific job>. Context: <files / repo / chain / constraints>. Return: <exact output format>. "
        "Verification: <how to check the result or separate facts from assumptions>."
    )


def analyze(prompt: str) -> tuple[str, list[Finding], list[str], str, str]:
    text = prompt.strip()
    lowered = text.lower()
    words = re.findall(r"\b\w[\w./:-]*\b", text)
    word_count = len(words)
    domain = detect_domain(text)

    findings: list[Finding] = []

    weak_goal = word_count < 8 or (not has_any(lowered, ACTION_WORDS) and word_count < 18)
    if weak_goal:
        findings.append(
            Finding(
                label="Missing concrete goal or success criteria",
                reason="The ask is so short or generic that the agent can only guess what 'good' looks like.",
                nudge="Name the exact job and what a useful answer must include.",
                files=["references/checklists/before-send.md"],
            )
        )

    missing_format = not has_any(lowered, FORMAT_MARKERS)
    if missing_format:
        findings.append(
            Finding(
                label="Missing output format",
                reason="Without a shape for the answer, the agent will choose one for you.",
                nudge="Tell it whether you want bullets, sections, a table, JSON, or a short checklist.",
                files=["references/checklists/before-send.md"],
            )
        )

    missing_verification = not has_any(lowered, VERIFY_MARKERS)
    if missing_verification:
        findings.append(
            Finding(
                label="Missing evidence or verification rule",
                reason="The prompt does not force the agent to separate facts, assumptions, or next checks.",
                nudge="Add a verification line so the model has to show evidence, caveats, or next checks.",
                files=["references/intervention-ladder.md", "references/checklists/before-send.md"],
            )
        )

    missing_context = (
        not has_any(lowered, CONTEXT_MARKERS)
        and not detect_chain(text)
        and not WALLET_RE.search(text)
        and domain == "general"
    ) or (
        domain in {"token-dd", "wallet-review", "yield-scan"}
        and not detect_chain(text)
        and not has_any(lowered, ["risk", "angle", "capital", "why you care", "constraints"])
    )
    if missing_context:
        findings.append(
            Finding(
                label="Missing environment or task context",
                reason="There is not enough context about chain, repo, files, constraints, or why the task matters.",
                nudge="Add the environment: chain, repo area, files, constraints, risk profile, or why you care.",
                files=["references/training-map.md", "references/checklists/before-send.md"],
            )
        )

    giant_ambiguous = word_count > 50 and text.count(",") + lowered.count(" and ") >= 4 and not has_any(lowered, PLAN_MARKERS)
    if giant_ambiguous:
        findings.append(
            Finding(
                label="Giant ambiguous ask that should be split or planned first",
                reason="The prompt bundles too many moves together without a sequence.",
                nudge="Ask for a plan or split the job before you ask for the full execution.",
                files=["references/intervention-ladder.md", "references/checklists/before-send.md"],
            )
        )

    wrong_mode = has_any(lowered, ["build", "implement", "ship", "code", "make"]) and word_count > 18 and not has_any(lowered, PLAN_MARKERS)
    if wrong_mode:
        findings.append(
            Finding(
                label="Likely wrong mode: asking for execution before exploration",
                reason="The prompt jumps straight to building without first scoping, planning, or clarifying.",
                nudge="Ask for an approach or plan first if the task touches many files, tools, or moving parts.",
                files=["references/intervention-ladder.md"],
            )
        )

    domain_file = {
        "token-dd": "references/checklists/token-dd.md",
        "wallet-review": "references/checklists/wallet-review.md",
        "yield-scan": "references/checklists/yield-scan.md",
    }.get(domain)

    next_files: list[str] = []
    for finding in findings:
        for file_name in finding["files"]:
            if file_name not in next_files:
                next_files.append(file_name)
    if domain_file and domain_file not in next_files:
        next_files.append(domain_file)

    if not findings:
        severity = "green"
        nudge = "This is specific enough to send. If you want, add one verification line to tighten it further."
    elif any(f.label.startswith("Giant ambiguous") for f in findings) or len(findings) >= 4:
        severity = "high"
        nudge = findings[0]["nudge"]
    elif len(findings) >= 2:
        severity = "medium"
        nudge = findings[0]["nudge"]
    else:
        severity = "low"
        nudge = findings[0]["nudge"]

    return severity, findings, next_files, nudge, prompt_stub(domain, text)


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

    severity, findings, next_files, nudge, stub = analyze(prompt)
    domain = detect_domain(prompt)

    print("Prompt Buddy Observer")
    print(f"Severity: {severity}")
    print(f"Mode guess: {domain}")
    print()

    if findings:
        print("Likely slips:")
        for finding in findings:
            print(f"- {finding.label}: {finding['reason']}")
    else:
        print("Likely slips:")
        print("- None obvious. This prompt already has decent shape.")

    print()
    print("Nudge:")
    print(f"- {nudge}")

    if next_files:
        print()
        print("Open next:")
        for file_name in next_files:
            print(f"- {file_name}")

    print()
    print("Next-step stub:")
    print(stub)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
