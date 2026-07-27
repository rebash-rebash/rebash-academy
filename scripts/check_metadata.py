#!/usr/bin/env python3
"""Validate that documentation pages include required front matter metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("title", "description", "author", "category", "tags")
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
SKIP_FILES = {"includes/abbreviations.md"}


def parse_front_matter(content: str) -> dict[str, str]:
    """Extract simple key-value pairs from YAML front matter."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.strip().startswith("-"):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta


def main() -> int:
    errors: list[str] = []

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel = md_file.relative_to(DOCS_DIR).as_posix()
        if rel in SKIP_FILES or rel.startswith("includes/"):
            continue

        content = md_file.read_text(encoding="utf-8")
        meta = parse_front_matter(content)

        if not meta:
            errors.append(f"{rel}: missing front matter")
            continue

        for field in REQUIRED_FIELDS:
            if field not in meta or not meta[field]:
                errors.append(f"{rel}: missing '{field}' in front matter")

    if errors:
        print("Metadata validation errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Metadata OK ({len(list(DOCS_DIR.rglob('*.md')))} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
