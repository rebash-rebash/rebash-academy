#!/usr/bin/env python3
"""Audit thin or stub documentation pages for SEO / content readiness.

Reports Markdown under docs/ that look thin (short body), planned stubs,
or missing descriptions. Does not modify files.

Usage:
  uv run python scripts/audit_thin_pages.py
  uv run python scripts/audit_thin_pages.py --min-words 120 --json
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WORD_RE = re.compile(r"[A-Za-z0-9']+")
SKIP_DIRS = {"assets", "_curriculum", "includes", "stylesheets", "javascripts", "overrides"}


def parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FM_RE.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line or line.strip().startswith("-"):
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip().strip("\"'")
    return meta, text[match.end() :]


def strip_markup(body: str) -> str:
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]+`", " ", body)
    body = re.sub(r"!?\[[^\]]*\]\([^)]+\)", " ", body)
    body = re.sub(r"{%.*?%}", " ", body, flags=re.DOTALL)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"^#+\s*", " ", body, flags=re.MULTILINE)
    return body


def iter_pages():
    for path in sorted(DOCS.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def is_moved_notice(path: Path, meta: dict, body: str) -> bool:
    title = (meta.get("title") or path.stem).lower()
    body_lower = body.lower()
    return any(marker in title for marker in ("(moved)", "(renamed)")) or any(
        marker in body_lower
        for marker in (
            '!!! tip "renamed"',
            '!!! tip "superseded"',
            "this project is now",
            "this project is replaced by",
            "was renamed to",
            "was superseded by",
        )
    )


def classify(path: Path, meta: dict, body: str, words: int, min_words: int) -> list[str]:
    reasons: list[str] = []
    status = (meta.get("status") or "").lower()
    template = meta.get("template") or ""
    desc = meta.get("description") or ""
    body_hint = (meta.get("title") or path.stem).lower()
    moved_notice = is_moved_notice(path, meta, body)

    if status == "planned":
        reasons.append("status:planned")
    if words < min_words and not moved_notice and template not in {
        "home.html",
        "career-paths.html",
        "technologies.html",
        "labs.html",
        "hub.html",
        "course.html",
        "modules.html",
        "course-labs.html",
        "learning-path.html",
        "module.html",
    }:
        # Template-driven index shells often have short Markdown on purpose.
        if path.name == "index.md" and template:
            pass
        elif words < min_words:
            reasons.append(f"thin:{words}<{min_words}")
    if moved_notice:
        reasons.append("notice:moved")
    if not desc and path.name != "index.md":
        reasons.append("missing:description")
    if "being prepared" in body_hint or "coming soon" in body_hint:
        reasons.append("stub-language")
    robots = (meta.get("robots") or "").lower()
    if "noindex" in robots:
        reasons.append("robots:noindex")
    return reasons


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-words", type=int, default=150)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = []
    for path in iter_pages():
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta, body = parse_frontmatter(text)
        words = len(WORD_RE.findall(strip_markup(body)))
        reasons = classify(path, meta, body, words, args.min_words)
        if not reasons:
            continue
        rel = path.relative_to(ROOT).as_posix()
        findings.append(
            {
                "path": rel,
                "words": words,
                "status": meta.get("status", ""),
                "template": meta.get("template", ""),
                "robots": meta.get("robots", ""),
                "reasons": reasons,
            }
        )

    findings.sort(key=lambda item: (item["words"], item["path"]))

    if args.json:
        print(json.dumps({"count": len(findings), "pages": findings}, indent=2))
    else:
        print(f"Thin/stub audit — {len(findings)} pages (min_words={args.min_words})\n")
        for item in findings[:80]:
            print(f"{item['words']:4d}  {item['path']}")
            print(f"      {', '.join(item['reasons'])}")
        if len(findings) > 80:
            print(f"\n… and {len(findings) - 80} more. Re-run with --json for full list.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
