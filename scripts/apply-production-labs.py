#!/usr/bin/env python3
"""Replace Hands-on Lab sections with production-style executable labs.

Usage:
  python3 scripts/apply-production-labs.py --course kubernetes
  python3 scripts/apply-production-labs.py --course all
  python3 scripts/apply-production-labs.py --course linux --dry-run --limit 2
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))

from enrichment.production_lab import build_lab  # noqa: E402

SKIP_NAMES = {"index.md", "roadmap.md", "faq.md"}
ALL_COURSES = [
    "kubernetes",
    "terraform",
    "helm",
    "gitlab",
    "github-actions",
    "git",
    "docker",
    "aws",
    "jenkins",
    "linux",
    "shell",
    "python",
    "networking",
]


def split_fm(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[: end + 5], text[end + 5 :].lstrip("\n")


def extract_sections(body: str) -> dict[str, str]:
    parts = re.split(r"(?m)^## ", body)
    sections: dict[str, str] = {}
    sections["__preamble__"] = parts[0]
    for part in parts[1:]:
        title, _, rest = part.partition("\n")
        sections[title.strip()] = rest
    return sections


def section_order(body: str, sections: dict[str, str]) -> list[str]:
    found = re.findall(r"(?m)^## (.+)$", body)
    order = [t for t in found if t in sections]
    for t in sections:
        if not t.startswith("__") and t not in order:
            order.append(t)
    return order


def rebuild_body(sections: dict[str, str], order: list[str]) -> str:
    preamble = sections.get("__preamble__", "")
    out = [preamble.rstrip(), ""]
    for title in order:
        if title not in sections or title.startswith("__"):
            continue
        content = sections[title].rstrip() + "\n"
        out.append(f"## {title}\n\n")
        out.append(content)
        if not content.endswith("\n"):
            out.append("\n")
    return "\n".join(out).rstrip() + "\n"


def fm_get(fm: str, key: str) -> str:
    m = re.search(rf'(?m)^{key}:\s*"?([^"\n]+)"?', fm)
    return m.group(1).strip() if m else ""


def lab_dir_for(tech: str, existing: str, fm: str, slug: str) -> str:
    m = re.search(r"mkdir -p (~/rebash-[^\s&]+)", existing)
    if m:
        return m.group(1)
    m2 = re.search(r"Workspace:\s*`(~/rebash-[^`]+)`", existing)
    if m2:
        return m2.group(1)
    module = fm_get(fm, "module")
    m3 = re.search(r"(\d+)", module)
    if m3:
        return f"~/rebash-{tech}/module-{int(m3.group(1)):02d}"
    return f"~/rebash-{tech}/{slug[:40]}"


def apply_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    if "## Hands-on Lab" not in body and "## Hands-on lab" not in body:
        return "skip-no-lab"
    sections = extract_sections(body)
    order = section_order(body, sections)
    tech = fm_get(fm, "technology") or fm_get(fm, "category") or path.parent.name
    title = fm_get(fm, "title") or path.stem.replace("-", " ").title()
    slug = path.stem
    existing = sections.get("Hands-on Lab") or sections.get("Hands-on lab") or ""
    lab_dir = lab_dir_for(tech, existing, fm, slug)
    theory = sections.get("Theory", "")
    headings = re.findall(r"(?m)^###\s+(.+)$", theory)
    lab = build_lab(tech, slug, title, lab_dir, headings)
    if "Hands-on lab" in sections and "Hands-on Lab" not in sections:
        del sections["Hands-on lab"]
        order = ["Hands-on Lab" if x == "Hands-on lab" else x for x in order]
    sections["Hands-on Lab"] = "\n" + lab.strip() + "\n"
    new_body = rebuild_body(sections, order)
    new_text = (fm + "\n\n" + new_body) if fm else new_body
    if new_text == text:
        return "unchanged"
    if dry_run:
        return "would-write"
    path.write_text(new_text, encoding="utf-8")
    return "updated"


def iter_course(course: str) -> list[Path]:
    courses = ALL_COURSES if course == "all" else [course]
    files: list[Path] = []
    for c in courses:
        d = DOCS / c
        if not d.is_dir():
            print(f"warn: missing {d}", file=sys.stderr)
            continue
        for p in sorted(d.glob("*.md")):
            if p.name in SKIP_NAMES:
                continue
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--course", required=True, help="Course under docs/ or 'all'")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("paths", nargs="*", type=Path)
    args = ap.parse_args()
    files = [p.resolve() for p in args.paths] if args.paths else iter_course(args.course)
    if args.limit:
        files = files[: args.limit]
    counts: dict[str, int] = {}
    for path in files:
        if not path.is_file():
            counts["missing"] = counts.get("missing", 0) + 1
            continue
        status = apply_file(path, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        rel = path
        try:
            rel = path.resolve().relative_to(ROOT)
        except Exception:
            pass
        print(f"{status:12} {rel}")
    print("---")
    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
