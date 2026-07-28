#!/usr/bin/env bash
# Enable repo git hooks that block Cursor co-author trailers.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

chmod +x scripts/git-hooks/prepare-commit-msg scripts/git-hooks/commit-msg
git config core.hooksPath scripts/git-hooks

echo "Git hooks enabled: core.hooksPath=scripts/git-hooks"
echo "Cursor Co-authored-by trailers will be stripped and blocked."
