#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
import textwrap

try:
    import curses
    import curses.textpad
except ImportError as exc:  # pragma: no cover - depends on platform build
    curses = None
    CURSES_IMPORT_ERROR = exc
else:
    CURSES_IMPORT_ERROR = None

from prompt_buddy_core import AnalysisResult, analyze, findings_lines, next_files_lines

MIN_HEIGHT = 18
MIN_WIDTH = 72


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return " ".join(args.prompt).strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    return ""


def normalize_prompt_text(text: str) -> str:
    lines = [line.rstrip() for line in text.replace("\r", "").splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def wrap_block(text: str, width: int, prefix: str = "") -> list[str]:
    body_width = max(20, width - len(prefix))
    lines: list[str] = []
    for raw_line in text.splitlines() or [""]:
        if not raw_line.strip():
            lines.append(prefix.rstrip())
            continue
        wrapped = textwrap.wrap(
            raw_line,
            width=body_width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        lines.extend(f"{prefix}{line}" for line in wrapped)
    return lines or [prefix.rstrip()]


def format_plain_report(result: AnalysisResult) -> str:
    lines = [
        "Prompt Buddy Sidecar",
        f"Severity: {result.severity}",
        f"Domain guess: {result.domain}",
        "",
        "Likely slips:",
    ]

    lines.extend(findings_lines(result))

    lines.extend(["", "Nudge:", f"- {result.nudge}"])

    if result.next_files:
        lines.extend(["", "Next files/checklists:"])
        lines.extend(next_files_lines(result))

    lines.extend(["", "Next-step stub:", result.stub])
    return "\n".join(lines)


def init_colors() -> None:
    assert curses is not None
    if not curses.has_colors():
        return
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_RED, -1)


def severity_attr(severity: str) -> int:
    assert curses is not None
    if not curses.has_colors():
        return curses.A_BOLD
    if severity == "green":
        return curses.color_pair(2) | curses.A_BOLD
    if severity == "high":
        return curses.color_pair(4) | curses.A_BOLD
    return curses.color_pair(3) | curses.A_BOLD


def draw_small_terminal(stdscr: curses.window, message: str) -> None:
    stdscr.erase()
    height, width = stdscr.getmaxyx()
    stdscr.addnstr(1, 2, "Prompt Buddy Sidecar", max(1, width - 4), curses.A_BOLD)
    stdscr.addnstr(3, 2, message, max(1, width - 4))
    stdscr.addnstr(5, 2, "Resize the terminal or press q to quit.", max(1, width - 4))
    stdscr.refresh()


def build_report_lines(result: AnalysisResult, width: int) -> list[str]:
    lines = ["Likely slips:"]
    for line in findings_lines(result):
        lines.extend(wrap_block(line, width))

    lines.extend(["", "Nudge:"])
    lines.extend(wrap_block(f"- {result.nudge}", width))

    if result.next_files:
        lines.extend(["", "Next files/checklists:"])
        for line in next_files_lines(result):
            lines.extend(wrap_block(line, width))

    lines.extend(["", "Next-step stub:"])
    lines.extend(wrap_block(result.stub, width))
    return lines


class SidecarApp:
    def __init__(self, initial_prompt: str) -> None:
        self.prompt = initial_prompt

    def run(self, stdscr: curses.window) -> int:
        stdscr.keypad(True)
        curses.curs_set(0)
        init_colors()

        mode = "report" if self.prompt else "edit"
        while True:
            if mode == "edit":
                updated = self.edit_prompt(stdscr, self.prompt)
                if updated is None:
                    return 0
                self.prompt = updated
                mode = "report"
                continue

            action = self.show_report(stdscr, self.prompt)
            if action == "quit":
                return 0
            if action == "new":
                self.prompt = ""
            mode = "edit"

    def edit_prompt(self, stdscr: curses.window, initial_text: str) -> str | None:
        assert curses is not None
        prompt_seed = initial_text

        while True:
            height, width = stdscr.getmaxyx()
            if height < MIN_HEIGHT or width < MIN_WIDTH:
                draw_small_terminal(stdscr, f"Need at least {MIN_WIDTH}x{MIN_HEIGHT} for the editor.")
                key = stdscr.getch()
                if key in {ord("q"), ord("Q"), 3}:
                    return None
                continue

            stdscr.erase()
            stdscr.addnstr(1, 2, "Prompt Buddy Sidecar", width - 4, curses.A_BOLD | curses.color_pair(1))
            stdscr.addnstr(2, 2, "Terminal sidecar MVP. Paste or type a prompt, then press Ctrl-G to analyze.", width - 4)
            stdscr.addnstr(3, 2, "Ctrl-C quits from the editor. Multi-line paste works in the box below.", width - 4)

            top = 5
            left = 2
            box_height = height - 8
            box_width = width - 4
            curses.textpad.rectangle(stdscr, top - 1, left - 1, top + box_height, left + box_width - 1)
            editor = curses.newwin(box_height, box_width - 1, top, left)
            editor.keypad(True)

            if prompt_seed:
                for row, line in enumerate(prompt_seed.splitlines()):
                    if row >= box_height:
                        break
                    editor.addnstr(row, 0, line, box_width - 2)

            stdscr.refresh()
            editor.refresh()
            curses.curs_set(1)
            textbox = curses.textpad.Textbox(editor, insert_mode=True)

            def validator(ch: int) -> int:
                if ch == 3:
                    raise KeyboardInterrupt
                return ch

            try:
                gathered = textbox.edit(validator)
            except KeyboardInterrupt:
                curses.curs_set(0)
                return None

            curses.curs_set(0)
            prompt = normalize_prompt_text(gathered)
            if prompt:
                return prompt

            stdscr.addnstr(height - 2, 2, "Prompt is empty. Press any key to keep editing or q to quit.", width - 4, curses.A_BOLD)
            stdscr.refresh()
            key = stdscr.getch()
            if key in {ord("q"), ord("Q"), 3}:
                return None
            prompt_seed = ""

    def show_report(self, stdscr: curses.window, prompt: str) -> str:
        assert curses is not None
        result = analyze(prompt)
        scroll = 0

        while True:
            height, width = stdscr.getmaxyx()
            if height < MIN_HEIGHT or width < MIN_WIDTH:
                draw_small_terminal(stdscr, f"Need at least {MIN_WIDTH}x{MIN_HEIGHT} for the report.")
                key = stdscr.getch()
                if key in {ord("q"), ord("Q"), 3}:
                    return "quit"
                continue

            content_width = width - 4
            report_lines = build_report_lines(result, content_width)
            viewport_height = height - 6
            max_scroll = max(0, len(report_lines) - viewport_height)
            scroll = max(0, min(scroll, max_scroll))

            stdscr.erase()
            stdscr.addnstr(1, 2, "Prompt Buddy Sidecar", content_width, curses.A_BOLD | curses.color_pair(1))
            stdscr.addnstr(2, 2, f"Severity: {result.severity}", content_width, severity_attr(result.severity))
            stdscr.addnstr(2, min(width // 2, width - 22), f"Domain guess: {result.domain}", max(1, width - min(width // 2, width - 22) - 2))

            for row in range(viewport_height):
                index = scroll + row
                if index >= len(report_lines):
                    break
                stdscr.addnstr(4 + row, 2, report_lines[index], content_width)

            footer = "[e] edit  [n] new  [j/k] scroll  [q] quit"
            if max_scroll:
                footer = f"{footer}  {scroll + 1}-{min(len(report_lines), scroll + viewport_height)} / {len(report_lines)}"
            stdscr.addnstr(height - 2, 2, footer, content_width, curses.A_DIM)
            stdscr.refresh()

            key = stdscr.getch()
            if key in {ord("q"), ord("Q"), 3}:
                return "quit"
            if key in {ord("e"), ord("E")}:
                return "edit"
            if key in {ord("n"), ord("N")}:
                return "new"
            if key in {curses.KEY_DOWN, ord("j")}:
                scroll = min(max_scroll, scroll + 1)
            elif key in {curses.KEY_UP, ord("k")}:
                scroll = max(0, scroll - 1)
            elif key == curses.KEY_NPAGE:
                scroll = min(max_scroll, scroll + viewport_height)
            elif key == curses.KEY_PPAGE:
                scroll = max(0, scroll - viewport_height)
            elif key == ord("g"):
                scroll = 0
            elif key == ord("G"):
                scroll = max_scroll


def run_interactive(initial_prompt: str) -> int:
    if curses is None:
        if initial_prompt:
            print(format_plain_report(analyze(initial_prompt)))
            return 0
        print(f"Prompt Buddy sidecar needs Python curses support for interactive mode: {CURSES_IMPORT_ERROR}", file=sys.stderr)
        return 1

    def runner(stdscr: curses.window) -> int:
        return SidecarApp(initial_prompt).run(stdscr)

    try:
        return curses.wrapper(runner)
    except curses.error as exc:
        if initial_prompt:
            print(format_plain_report(analyze(initial_prompt)))
            return 0
        print(f"Prompt Buddy sidecar needs a real terminal with curses support: {exc}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Terminal sidecar MVP for Prompt Buddy. Launch it with no prompt to paste/edit, or use --plain for a one-shot report.",
    )
    parser.add_argument("--plain", action="store_true", help="Print a sidecar-style report to stdout instead of launching the interactive TUI.")
    parser.add_argument("prompt", nargs="*", help="Optional prompt text. If omitted, stdin is used when piped, otherwise the editor opens.")
    args = parser.parse_args()

    prompt = read_prompt(args)
    if args.plain or (prompt and not sys.stdout.isatty()) or (prompt and not sys.stdin.isatty()):
        if not prompt:
            parser.print_help(sys.stderr)
            return 1
        print(format_plain_report(analyze(prompt)))
        return 0

    return run_interactive(prompt)


if __name__ == "__main__":
    raise SystemExit(main())
