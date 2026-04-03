#!/usr/bin/env bash
set -euo pipefail

SLUG="dob-prompt-buddy"
SKILL_NAME="dob-prompt-buddy"
TITLE="DayOneBuilder Prompt Buddy by Ben Ison"
REPO_URL="https://github.com/DayOneBuilder/dob-prompt-buddy"
PRODUCT_URL="https://dayonebuilder.online/products/prompt-buddy/"
SUPPORT_URL="https://checkout.dayonebuilder.online/donate/prompt-buddy"
OBSERVE_SCRIPT="observe-prompt-buddy.py"
SIDECAR_SCRIPT="sidecar-prompt-buddy.py"
SCAFFOLD_SCRIPT="scaffold-prompt-buddy.sh"

INSTALL_CODEX=1
INSTALL_CLAUDE=1
INSTALL_LAUNCHER=1

usage() {
  cat <<'HELP'
Usage: ./install.sh [--codex-only] [--claude-only] [--no-launcher] [--help]

Installs the self-contained Prompt Buddy skill into a Codex and/or Claude skills directory,
plus an optional `dob-prompt-buddy` launcher in `~/.local/bin`.

Flags:
- --codex-only   Install only the Codex skill copy
- --claude-only  Install only the Claude skill copy
- --no-launcher  Skip the standalone launcher install
- --help         Show this help text and exit
HELP
}

while [ $# -gt 0 ]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --codex-only)
      INSTALL_CLAUDE=0
      ;;
    --claude-only)
      INSTALL_CODEX=0
      ;;
    --no-launcher)
      INSTALL_LAUNCHER=0
      ;;
    *)
      echo "Unknown flag: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_SKILL_DIR="$ROOT/skills/$SKILL_NAME"
if [ ! -d "$SRC_SKILL_DIR" ]; then
  echo "Skill directory not found: $SRC_SKILL_DIR" >&2
  exit 1
fi

choose_codex_base() {
  if [ -n "${CODEX_SKILLS_DIR:-}" ]; then
    printf '%s\n' "$CODEX_SKILLS_DIR"
  elif [ -d "$HOME/.codex/skills" ]; then
    printf '%s\n' "$HOME/.codex/skills"
  else
    printf '%s\n' "$HOME/.agents/skills"
  fi
}

CODEX_BASE="$(choose_codex_base)"
CLAUDE_BASE="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
LAUNCHER_PATH="$HOME/.local/bin/$SLUG"

install_skill() {
  local base="$1"
  local dest="$base/$SKILL_NAME"
  mkdir -p "$base"
  rm -rf "$dest"
  cp -R "$SRC_SKILL_DIR" "$dest"
  chmod +x "$dest/scripts/"* 2>/dev/null || true
  printf '%s\n' "$dest"
}

CODEX_DEST=""
CLAUDE_DEST=""
if [ "$INSTALL_CODEX" -eq 1 ]; then
  CODEX_DEST="$(install_skill "$CODEX_BASE")"
fi
if [ "$INSTALL_CLAUDE" -eq 1 ]; then
  CLAUDE_DEST="$(install_skill "$CLAUDE_BASE")"
fi

if [ "$INSTALL_LAUNCHER" -eq 1 ]; then
  mkdir -p "$HOME/.local/bin"
  cat > "$LAUNCHER_PATH" <<'LAUNCHER'
#!/usr/bin/env bash
set -euo pipefail
OBSERVE_SCRIPT="observe-prompt-buddy.py"
SIDECAR_SCRIPT="sidecar-prompt-buddy.py"
SCAFFOLD_SCRIPT="scaffold-prompt-buddy.sh"
SKILL_NAME="dob-prompt-buddy"
resolve_skill_dir() {
  for base in "${CODEX_SKILLS_DIR:-}" "$HOME/.codex/skills" "$HOME/.agents/skills" "${CLAUDE_SKILLS_DIR:-}" "$HOME/.claude/skills"; do
    [ -n "$base" ] || continue
    if [ -x "$base/$SKILL_NAME/scripts/$OBSERVE_SCRIPT" ]; then
      printf '%s\n' "$base/$SKILL_NAME"
      return 0
    fi
  done
  return 1
}
SKILL_DIR="$(resolve_skill_dir || true)"
if [ -z "$SKILL_DIR" ]; then
  echo "Installed skill not found for $SKILL_NAME." >&2
  exit 1
fi
OBSERVE_PATH="$SKILL_DIR/scripts/$OBSERVE_SCRIPT"
SIDECAR_PATH="$SKILL_DIR/scripts/$SIDECAR_SCRIPT"
SCAFFOLD_PATH="$SKILL_DIR/scripts/$SCAFFOLD_SCRIPT"

print_help() {
  cat <<HELP
DayOneBuilder Prompt Buddy by Ben Ison
Repo: https://github.com/DayOneBuilder/dob-prompt-buddy
Product page: https://dayonebuilder.online/products/prompt-buddy/
Support: https://checkout.dayonebuilder.online/donate/prompt-buddy

Installed skill path:
- $SKILL_DIR

This is a terminal sidecar/TUI plus observer/scaffold helpers. It is not a desktop overlay.

Commands:
- dob-prompt-buddy sidecar
- dob-prompt-buddy sidecar --plain "<prompt>"
- dob-prompt-buddy observe "<prompt>"
- dob-prompt-buddy scaffold [path]
HELP
}

if [ $# -eq 0 ] || [ "${1:-}" = "--help" ] || [ "${1:-}" = "help" ]; then
  print_help
  exit 0
fi
case "${1:-}" in
  sidecar)
    shift
    exec python3 "$SIDECAR_PATH" "$@"
    ;;
  observe)
    shift
    exec python3 "$OBSERVE_PATH" "$@"
    ;;
  scaffold)
    shift
    exec "$SCAFFOLD_PATH" "$@"
    ;;
  *)
    echo "Unknown command: ${1:-}" >&2
    echo >&2
    print_help >&2
    exit 1
    ;;
esac
LAUNCHER
  chmod +x "$LAUNCHER_PATH"
fi

echo "Installed $TITLE"
echo "- Repo: $REPO_URL"
echo "- Product page: $PRODUCT_URL"
if [ -n "$CODEX_DEST" ]; then echo "- Codex skill: $CODEX_DEST"; fi
if [ -n "$CLAUDE_DEST" ]; then echo "- Claude skill: $CLAUDE_DEST"; fi
if [ "$INSTALL_LAUNCHER" -eq 1 ]; then echo "- Launcher: $LAUNCHER_PATH"; fi
echo
echo "Notes:"
echo "- Codex repo-scoped use: launch Codex inside this repo; it auto-discovers .agents/skills/"
echo "- Claude plugin use: launch Claude with --plugin-dir . inside this repo"
echo "- Terminal sidecar: dob-prompt-buddy sidecar"
echo "- Local observer: dob-prompt-buddy observe \"review this wallet\""
echo "- Starter scaffold: dob-prompt-buddy scaffold ./prompt-buddy-starter"
