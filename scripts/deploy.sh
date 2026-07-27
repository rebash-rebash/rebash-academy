#!/usr/bin/env bash
# REBASH Academy – Deploy script (local helper)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

echo "==> Building for deployment..."
mkdocs build --strict

echo "==> Site ready in site/"
echo "    Deploy via GitHub Actions on push to main, or:"
echo "    mkdocs gh-deploy --force"
