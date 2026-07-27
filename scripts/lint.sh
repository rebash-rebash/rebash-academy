#!/usr/bin/env bash
# REBASH Academy – Lint script
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ERRORS=0

echo "==> Linting YAML files..."
if command -v yamllint &>/dev/null; then
  yamllint -d relaxed mkdocs.yml .github/workflows/*.yml 2>/dev/null || ERRORS=$((ERRORS + 1))
else
  python3 -c "
import yaml, sys
from pathlib import Path
for f in ['mkdocs.yml'] + list(Path('.github/workflows').glob('*.yml')):
    if f.exists():
        yaml.safe_load(f.read_text())
        print(f'  OK: {f}')
" || ERRORS=$((ERRORS + 1))
fi

echo "==> Checking Markdown files..."
if command -v markdownlint &>/dev/null; then
  markdownlint docs/**/*.md docs/*.md 2>/dev/null || ERRORS=$((ERRORS + 1))
else
  echo "  (markdownlint not installed – skipping)"
fi

echo "==> Validating mkdocs config..."
if [[ -d ".venv" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi
mkdocs build --strict --quiet 2>/dev/null || ERRORS=$((ERRORS + 1))

if [[ $ERRORS -gt 0 ]]; then
  echo "==> Lint failed with $ERRORS error(s)"
  exit 1
fi

echo "==> Lint passed"
