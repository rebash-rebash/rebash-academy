#!/usr/bin/env python3
"""Validate that documentation pages include required front matter metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

REQUIRED_FIELDS = ("title", "description", "author", "category", "tags")
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
SKIP_FILES = {"includes/abbreviations.md"}


def parse_front_matter(content: str) -> dict:
    """Extract YAML front matter as a dictionary."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    if yaml is not None:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else {}

    # Minimal fallback parser for the repository's front matter style.
    # It supports top-level scalars and simple block lists such as:
    #
    # tags:
    #   - linux
    #   - devops
    meta: dict = {}
    current_list_key: str | None = None
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("-") and current_list_key:
            value = stripped[1:].strip().strip('"').strip("'")
            if value:
                meta.setdefault(current_list_key, []).append(value)
            continue

        current_list_key = None
        if ":" not in line or stripped.startswith("-"):
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value:
            meta[key] = value.strip('"').strip("'")
        else:
            meta[key] = []
            current_list_key = key
    return meta


def field_present(meta: dict, field: str) -> bool:
    value = meta.get(field)
    if value is None:
        return False
    if field == "tags" and isinstance(value, list):
        return len(value) > 0
    return bool(str(value).strip())


def main() -> int:
    errors: list[str] = []
    checked = 0

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel = md_file.relative_to(DOCS_DIR).as_posix()
        if rel in SKIP_FILES or rel.startswith("includes/"):
            continue

        checked += 1
        content = md_file.read_text(encoding="utf-8")
        meta = parse_front_matter(content)

        if not meta:
            errors.append(f"{rel}: missing front matter")
            continue

        for field in REQUIRED_FIELDS:
            if not field_present(meta, field):
                errors.append(f"{rel}: missing '{field}' in front matter")

    if errors:
        print("Metadata validation errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Metadata OK ({checked} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
