#!/usr/bin/env bash
# REBASH Academy – Validation script
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

ERRORS=0

echo "==> Building site for link validation..."
mkdocs build --strict --quiet

echo "==> Checking for missing metadata..."
python3 scripts/check_metadata.py || ERRORS=$((ERRORS + 1))

echo "==> Checking internal links..."
python3 scripts/check_links.py || ERRORS=$((ERRORS + 1))

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Validation failed with $ERRORS error(s)"
  exit 1
fi

echo "==> Validation passed"
