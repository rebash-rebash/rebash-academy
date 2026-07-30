#!/usr/bin/env bash
# Render every docs/assets/d2/*.d2 source to docs/assets/images/<name>.svg
# in Excalidraw-like sketch style. Usage: bash scripts/render-d2-diagrams.sh
set -euo pipefail
cd "$(dirname "$0")/.."

command -v d2 >/dev/null || { echo "d2 CLI not found (https://d2lang.com)"; exit 1; }

printf '%s\n' docs/assets/d2/*.d2 | xargs -P 8 -n 1 sh -c '
  name=$(basename "$1" .d2)
  d2 --sketch --theme=3 --dark-theme=201 --layout=dagre --pad=48 --scale=1 \
     --no-xml-tag --omit-version "$1" "docs/assets/images/$name.svg" \
     >/dev/null 2>&1 || echo "FAILED: $name"
' _
echo "Rendered $(ls docs/assets/d2/*.d2 | wc -l | tr -d ' ') diagrams."
