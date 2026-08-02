#!/usr/bin/env python3
"""Build professional EPUB/PDF course books from REBASH Academy curricula.

Includes cover, copyright, TOC, list of figures, syntax-highlighted code,
headers/footers/page numbers, chapter numbering, glossary, index, QR codes
to online labs, Try-it-yourself boxes, and styled tips/warnings/interviews.

Examples::

    python3 scripts/build_course_book.py linux
    python3 scripts/build_course_book.py python --format epub
    python3 scripts/build_course_book.py --list-courses

See books/README.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow `python scripts/build_course_book.py` without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent))

from books.builder import build_course, die, list_courses  # noqa: E402


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("course", nargs="?", help="Course under docs/ (linux, shell, python, …)")
    p.add_argument(
        "--format",
        dest="formats",
        default="epub,pdf",
        help="Comma-separated: epub,pdf,html,md (default: epub,pdf)",
    )
    p.add_argument("--skip-index", action="store_true", default=True, help="Omit index.md (default: on)")
    p.add_argument("--include-index", action="store_true", help="Include course index.md")
    p.add_argument(
        "--author",
        default="Shaik Khadar Basha",
        help="Author name on cover, copyright, and about-the-author pages",
    )
    p.add_argument("--subtitle", default=None, help="Cover subtitle override")
    p.add_argument("--list-courses", action="store_true")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.list_courses:
        for c in list_courses():
            print(c)
        return 0
    if not args.course:
        die("course name required (or --list-courses)")
    formats = {f.strip().lower() for f in args.formats.split(",") if f.strip()} | {"md", "html"}
    unknown = formats - {"epub", "pdf", "html", "md"}
    if unknown:
        die(f"unknown formats: {', '.join(sorted(unknown))}")
    build_course(
        args.course,
        formats,
        skip_index=not args.include_index,
        author=args.author,
        subtitle=args.subtitle,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
