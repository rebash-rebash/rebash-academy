#!/usr/bin/env bash
# REBASH Academy – Build script
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "==> Building REBASH Academy documentation..."
mkdocs build --strict
echo "==> Build complete. Output: site/"
