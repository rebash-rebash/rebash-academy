#!/usr/bin/env python3
"""Copy built course books into docs/assets/books for the free-download page."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS_SRC = ROOT / "books"
SITE_BOOKS = ROOT / "docs" / "assets" / "books"
DEFAULT_COURSES = ("linux", "shell", "networking", "python")


def sync_course(course: str) -> list[str]:
    src_dir = BOOKS_SRC / course
    dst_dir = SITE_BOOKS / course
    if not src_dir.is_dir():
        raise SystemExit(f"Missing build output: {src_dir} (run build_course_book.py {course})")

    dst_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for ext in ("pdf", "epub"):
        src = src_dir / f"{course}.{ext}"
        if not src.is_file():
            print(f"  skip missing {src.relative_to(ROOT)}", file=sys.stderr)
            continue
        dst = dst_dir / src.name
        shutil.copy2(src, dst)
        copied.append(str(dst.relative_to(ROOT)))
        print(f"  {dst.relative_to(ROOT)} ({dst.stat().st_size // 1024} KB)")
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "courses",
        nargs="*",
        default=list(DEFAULT_COURSES),
        help="Course slugs to sync (default: linux shell networking python)",
    )
    args = parser.parse_args()

    print(f"Syncing books → {SITE_BOOKS.relative_to(ROOT)}")
    total = 0
    for course in args.courses:
        print(f"[{course}]")
        total += len(sync_course(course))
    print(f"Done — {total} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
