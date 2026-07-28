#!/usr/bin/env bash
# Enable repo git hooks that strip Co-authored-by trailers.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

chmod +x scripts/git-hooks/prepare-commit-msg scripts/git-hooks/commit-msg
git config core.hooksPath scripts/git-hooks

echo "Git hooks enabled: core.hooksPath=scripts/git-hooks"
echo "Co-authored-by trailers will be stripped from every commit."
