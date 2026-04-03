#!/usr/bin/env bash
set -euo pipefail
rm -rf       "$HOME/.agents/skills/dob-prompt-buddy"       "$HOME/.codex/skills/dob-prompt-buddy"       "$HOME/.claude/skills/dob-prompt-buddy"       "$HOME/.local/bin/dob-prompt-buddy"
echo "Removed standalone installs for dob-prompt-buddy from Codex/Claude skill paths and ~/.local/bin"
