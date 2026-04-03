#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/skills/dob-prompt-buddy/scripts/scaffold-prompt-buddy.sh" "$@"
