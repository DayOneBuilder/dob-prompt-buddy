#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT/skills/dob-prompt-buddy/scripts/sidecar-prompt-buddy.py" "$@"
