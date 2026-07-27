#!/usr/bin/env python3
"""Check internal links in the built MkDocs site."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE_DIR = Path(__file__).resolve().parent.parent / "site"
LINK_PATTERN = re.compile(r'href="([^"#]+)"')
SKIP_PREFIXES = ("javascript:", "mailto:", "tel:", "http://", "https://", "//")


def is_skipped(url: str) -> bool:
    return url.startswith("#") or url.startswith(SKIP_PREFIXES)


def main() -> int:
    if not SITE_DIR.exists():
        print("Site directory not found. Run 'mkdocs build' first.")
        return 1

    errors: list[str] = []
    checked = 0

    for html_file in SITE_DIR.rglob("*.html"):
        content = html_file.read_text(encoding="utf-8", errors="ignore")
        for match in LINK_PATTERN.finditer(content):
            href = unquote(match.group(1))
            if is_skipped(href) or "{" in href:
                continue

            target = (html_file.parent / href).resolve()
            checked += 1

            if not target.exists():
                rel_page = html_file.relative_to(SITE_DIR)
                errors.append(f"{rel_page}: broken link -> {href}")

    if errors:
        print("Broken internal links:")
        for error in errors[:50]:
            print(f"  - {error}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more")
        return 1

    print(f"Links OK ({checked} internal links checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
