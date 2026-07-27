#!/usr/bin/env python3
"""Quote Mermaid node/subgraph labels that break Mermaid 11+ parsing."""

from __future__ import annotations

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

# Characters that require quoted labels in Mermaid 11 flowcharts
SPECIAL = re.compile(r"[:\→/\\&|<>()]")

SUBGRAPH_UNQUOTED = re.compile(
    r"^(\s*subgraph\s+)([A-Za-z][A-Za-z0-9_]*)\s+([^\[\n\"]+)$",
    re.MULTILINE,
)

# Node shapes: [], {}, (()), [[]], etc. — only unquoted labels
NODE = re.compile(
    r"(\b[A-Za-z0-9_]+)"
    r"(\[\[|\[|\{\{|\{|\(\(|\()"
    r"([^\]\"'\n\}]+?)"
    r"(\]\]|\]|\}\}|\}|\)\)|\))",
)


def needs_quotes(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    if text.startswith('"') and text.endswith('"'):
        return False
    return bool(SPECIAL.search(text)) or " " in text and ":" in text


def quote_node(match: re.Match[str]) -> str:
    node_id, open_br, label, close_br = match.groups()
    label = label.strip()
    if not needs_quotes(label):
        return match.group(0)
    escaped = label.replace('"', "#quot;")
    return f'{node_id}{open_br}"{escaped}"{close_br}'


def fix_subgraph(line: str) -> str:
    m = SUBGRAPH_UNQUOTED.match(line)
    if not m:
        return line
    prefix, node_id, title = m.groups()
    title = title.strip()
    if not title or title.startswith("["):
        return line
    escaped = title.replace('"', "#quot;")
    return f'{prefix}{node_id}["{escaped}"]'


def fix_block(block: str) -> str:
    trailing_newline = block.endswith("\n")
    lines = block.splitlines()
    out: list[str] = []
    for line in lines:
        out.append(fix_subgraph(line))
    text = NODE.sub(quote_node, "\n".join(out))
    if trailing_newline and not text.endswith("\n"):
        text += "\n"
    return text


def process_file(path: Path) -> bool:
    content = path.read_text()
    parts = content.split("```mermaid")
    if len(parts) == 1:
        return False

    changed = False
    rebuilt = [parts[0]]
    for chunk in parts[1:]:
        end = chunk.find("```")
        if end == -1:
            rebuilt.append("```mermaid" + chunk)
            continue
        block = chunk[:end]
        rest = chunk[end:]
        fixed = fix_block(block)
        if fixed != block:
            changed = True
        rebuilt.append("```mermaid" + fixed + rest)

    if changed:
        path.write_text("".join(rebuilt))
    return changed


def main() -> None:
    updated = 0
    for path in sorted(DOCS.rglob("*.md")):
        if process_file(path):
            updated += 1
            print(f"fixed: {path.relative_to(DOCS.parent)}")
    print(f"Updated {updated} file(s)")


if __name__ == "__main__":
    main()
