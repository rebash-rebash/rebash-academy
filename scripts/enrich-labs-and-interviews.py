#!/usr/bin/env python3
"""Enrich Hands-on Lab and Interview Questions with topic-specific content.

Usage:
  python3 scripts/enrich-labs-and-interviews.py --course kubernetes
  python3 scripts/enrich-labs-and-interviews.py --course all-priority
  python3 scripts/enrich-labs-and-interviews.py --course terraform --dry-run --limit 3
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))

from enrichment import banks_cicd_git_docker_aws as banks_b  # noqa: E402
from enrichment import banks_jenkins as banks_j  # noqa: E402
from enrichment import banks_k8s_tf_helm as banks_a  # noqa: E402
from enrichment.formatters import interview_body, lab_body, bash  # noqa: E402

SKIP_NAMES = {"index.md", "roadmap.md", "faq.md"}
PRIORITY = [
    "kubernetes",
    "terraform",
    "helm",
    "gitlab",
    "github-actions",
    "git",
    "docker",
    "aws",
    "jenkins",
]

GENERIC_IQ = re.compile(
    r"How does \*\*[^*]+\*\* show up when operating Cloud or production platforms\?",
    re.M,
)


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
    preamble = parts[0]
    sections["__preamble__"] = preamble
    for part in parts[1:]:
        title, _, rest = part.partition("\n")
        sections[title.strip()] = rest
    return sections


def rebuild_body(sections: dict[str, str], order: list[str]) -> str:
    preamble = sections.get("__preamble__", "")
    out = [preamble.rstrip(), ""]
    for title in order:
        if title not in sections or title.startswith("__"):
            continue
        content = sections[title].rstrip() + "\n"
        out.append(f"## {title}\n")
        out.append(content)
        if not content.endswith("\n\n"):
            out.append("\n")
    return "\n".join(out).rstrip() + "\n"


def section_order(body: str, sections: dict[str, str]) -> list[str]:
    found = re.findall(r"(?m)^## (.+)$", body)
    # Preserve original order; ensure known sections still present
    order = [t for t in found if t in sections]
    for t in sections:
        if not t.startswith("__") and t not in order:
            order.append(t)
    return order


def fm_get(fm: str, key: str) -> str:
    m = re.search(rf'(?m)^{key}:\s*"?([^"\n]+)"?', fm)
    return m.group(1).strip() if m else ""


def theory_headings(theory: str) -> list[str]:
    return re.findall(r"(?m)^###\s+(.+)$", theory)


def lab_dir_for(tech: str, slug: str, existing_lab: str, fm: str) -> str:
    m = re.search(r"mkdir -p (~/rebash-[^\s&]+)", existing_lab)
    if m:
        return m.group(1)
    module = fm_get(fm, "module")
    m2 = re.search(r"(\d+)", module)
    if m2:
        return f"~/rebash-{tech}/lab{int(m2.group(1)):02d}"
    # Prefer short slug path used by many pages
    short = slug.replace("_", "-")
    if len(short) > 40:
        short = short[:40].rstrip("-")
    return f"~/rebash-{tech}/{short}"


def lookup_lab(tech: str, slug: str, title: str, lab_dir: str) -> str | None:
    for mod in (banks_a, banks_b, banks_j):
        if tech in mod.supported_techs():
            return mod.lab_for(tech, slug, title, lab_dir)
    return None


def lookup_iq(tech: str, slug: str, title: str) -> str | None:
    for mod in (banks_a, banks_b, banks_j):
        if tech in mod.supported_techs():
            return mod.interview_for(tech, slug, title)
    return None


def fallback_lab(tech: str, title: str, lab_dir: str, headings: list[str]) -> str:
    hint = headings[0] if headings else title
    return lab_body(
        lab_dir,
        f"practise the core workflow for {title}",
        [
            (
                "Topic exercise",
                bash(
                    f"""tee README-LAB.txt << 'EOF'
Topic: {title}
Theory focus: {hint}
Complete the commands from the Theory section until you have an observable result
(file, resource Ready, plan, HTTP 200, or validated YAML).
EOF
cat README-LAB.txt
# Add topic commands below as you learn — prefer local/sandbox tools for {tech}."""
                ),
            ),
            (
                "Capture evidence",
                bash(
                    """date -u +%Y-%m-%dT%H:%M:%SZ | tee evidence-timestamp.txt
ls -la | tee evidence-listing.txt"""
                ),
            ),
        ],
        f"# Keep ~/rebash-{tech}/ for later tutorials; destroy disposable cloud resources from this lab",
    )


def fallback_iq(title: str, tech: str, headings: list[str]) -> str:
    h = headings[0] if headings else title
    return interview_body(
        [
            f"What problem does **{title}** solve for teams working with {tech}?",
            f"If **{h}** misbehaves in production, what do you check first?",
            f"Which trade-offs should engineers understand when adopting **{title}**?",
            f"What security control should accompany **{title}** in production?",
            f"How would you verify **{title}** automatically in CI or a scheduled check?",
        ],
        {
            2: f"Start with blast radius and recent changes, gather evidence specific to {tech} "
            f"(status, logs, plan/diff, health checks), then fix forward with a known rollback path.",
            4: f"Apply least privilege, keep secrets out of Git and images, and ensure auditability "
            f"for changes related to {title}.",
        },
    )


def enrich_file(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    if "## Hands-on Lab" not in body and "## Hands-on lab" not in body:
        return "skip-no-lab"

    sections = extract_sections(body)
    order = section_order(body, sections)
    tech = fm_get(fm, "technology") or fm_get(fm, "category") or path.parent.name
    title = fm_get(fm, "title") or path.stem.replace("-", " ").title()
    slug = path.stem
    theory = sections.get("Theory", "")
    headings = theory_headings(theory)
    existing_lab = sections.get("Hands-on Lab") or sections.get("Hands-on lab") or ""
    lab_dir = lab_dir_for(tech, slug, existing_lab, fm)

    lab = lookup_lab(tech, slug, title, lab_dir) or fallback_lab(tech, title, lab_dir, headings)
    iq = lookup_iq(tech, slug, title) or fallback_iq(title, tech, headings)

    # Normalise section key to Hands-on Lab
    if "Hands-on lab" in sections and "Hands-on Lab" not in sections:
        del sections["Hands-on lab"]
        order = ["Hands-on Lab" if x == "Hands-on lab" else x for x in order]

    sections["Hands-on Lab"] = "\n" + lab.strip() + "\n"
    sections["Interview Questions"] = "\n" + iq.strip() + "\n"

    new_body = rebuild_body(sections, order)
    new_text = (fm + "\n\n" + new_body) if fm else new_body
    if new_text == text:
        return "unchanged"
    if dry_run:
        return "would-write"
    path.write_text(new_text, encoding="utf-8")
    return "updated"


def iter_course(course: str) -> list[Path]:
    if course == "all-priority":
        courses = PRIORITY
    else:
        courses = [course]
    files: list[Path] = []
    for c in courses:
        d = DOCS / c
        if not d.is_dir():
            print(f"warn: missing course dir {d}", file=sys.stderr)
            continue
        for p in sorted(d.glob("*.md")):
            if p.name in SKIP_NAMES:
                continue
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--course",
        required=True,
        help=f"Course folder under docs/, or all-priority ({', '.join(PRIORITY)})",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("paths", nargs="*", type=Path, help="Optional explicit markdown paths")
    args = ap.parse_args()

    files = [Path(p) for p in args.paths] if args.paths else iter_course(args.course)
    if args.limit:
        files = files[: args.limit]

    counts: dict[str, int] = {}
    for path in files:
        if not path.is_file():
            counts["missing"] = counts.get("missing", 0) + 1
            continue
        status = enrich_file(path, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:12} {path.resolve().relative_to(ROOT)}")

    print("---")
    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
