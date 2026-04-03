#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'HELP'
Usage: ./uninstall.sh [--help]

Removes standalone Prompt Buddy installs from:
- ~/.agents/skills/dob-prompt-buddy
- ~/.codex/skills/dob-prompt-buddy
- ~/.claude/skills/dob-prompt-buddy
- ~/.local/bin/dob-prompt-buddy
HELP
}

case "${1:-}" in
  --help|-h|help)
    usage
    exit 0
    ;;
  "")
    ;;
  *)
    echo "Unknown flag: $1" >&2
    echo >&2
    usage >&2
    exit 1
    ;;
esac

rm -rf \
  "$HOME/.agents/skills/dob-prompt-buddy" \
  "$HOME/.codex/skills/dob-prompt-buddy" \
  "$HOME/.claude/skills/dob-prompt-buddy" \
  "$HOME/.local/bin/dob-prompt-buddy"
echo "Removed standalone installs for dob-prompt-buddy from Codex/Claude skill paths and ~/.local/bin"
