#!/usr/bin/env bash
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$(pwd)/dob-prompt-buddy-starter}"
mkdir -p "$TARGET/checklists" "$TARGET/examples"
cp "$SKILL_DIR/references/README.md" "$TARGET/README.md"
cp "$SKILL_DIR/references/intervention-ladder.md" "$TARGET/intervention-ladder.md"
cp "$SKILL_DIR/references/training-map.md" "$TARGET/training-map.md"
cp "$SKILL_DIR/references/checklists/"*.md "$TARGET/checklists/"
cp "$SKILL_DIR/references/examples/"*.md "$TARGET/examples/"
echo "Scaffolded Prompt Buddy starter at: $TARGET"
