#!/usr/bin/env bash
# Remove Co-authored-by trailers from all commits on the current branch.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FILTER='grep -vi "^co-authored-by:" || true'

FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --msg-filter "$FILTER" HEAD

echo "History rewritten. Verify with: git log --format=%B | rg -i 'co-authored-by' || echo clean"
echo "Then push: git push --force-with-lease origin main"
