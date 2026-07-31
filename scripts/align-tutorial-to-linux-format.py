#!/usr/bin/env python3
"""Align a Helm-style tutorial body to the Linux de facto format.

Usage:
  python3 scripts/align-tutorial-to-linux-format.py docs/aws/*.md
  python3 scripts/align-tutorial-to-linux-format.py --course aws

Idempotent for files that already have Code Walkthrough + Interview Questions.
Preserves frontmatter. Rewrites body section order and fills missing trailing sections.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_TAIL = [
    "Code Walkthrough",
    "Security Considerations",
    "Common Mistakes",
    "Best Practices",
    "Troubleshooting",
    "Summary",
    "Interview Questions",
    "Related Tutorials",
]


def split_fm(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[: end + 5], text[end + 5 :].lstrip("\n")


def extract_sections(body: str) -> dict[str, str]:
    """Map H2 title -> content (without the H2 line)."""
    parts = re.split(r"(?m)^## ", body)
    sections: dict[str, str] = {}
    preamble = parts[0].strip()
    if preamble:
        sections["__preamble__"] = preamble
    for part in parts[1:]:
        title, _, rest = part.partition("\n")
        sections[title.strip()] = rest.strip()
    return sections


def get_title(preamble: str, fm: str) -> str:
    m = re.search(r"(?m)^#\s+(.+)$", preamble)
    if m:
        return m.group(1).strip()
    m = re.search(r'(?m)^title:\s*"?([^"\n]+)"?', fm)
    return m.group(1).strip() if m else "Tutorial"


def get_tech(fm: str, path: Path) -> str:
    m = re.search(r"(?m)^(?:technology|category):\s*[\"']?([a-z0-9-]+)", fm)
    if m:
        return m.group(1)
    return path.parent.name


def get_module(fm: str, overview: str) -> str:
    m = re.search(r'(?m)^module:\s*"?([^"\n]+)"?', fm)
    if m:
        return m.group(1).strip()
    m = re.search(r"Module\s+(\d+)\s*[·:]\s*([^\n*]+)", overview)
    if m:
        return f"Module {m.group(1)} · {m.group(2).strip()}"
    return "Module"


def extract_diagram(text: str) -> str:
    m = re.search(r"!\[([^\]]*)\]\(([^)]*excalidraw[^)]+)\)", text)
    if m:
        return f"![{m.group(1)}]({m.group(2)})"
    m = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    if m:
        return f"![{m.group(1)}]({m.group(2)})"
    return ""


def normalize_theory(theory: str) -> str:
    theory = theory.replace("### Why it matters for Cloud / DevOps", "### Why it matters")
    theory = theory.replace("### Why it matters for Kubernetes / DevOps", "### Why it matters")
    theory = theory.replace("### Key concepts or comparisons", "### Key concepts and comparisons")
    theory = theory.replace("### Common pitfalls / misconceptions", "### Common pitfalls")
    # Fold deep dive into theory as a named concepts section
    theory = theory.replace("### Concept deep dive", "### Concept deep dive")
    return theory.strip()


def build_lab(existing: str, tech: str, title: str) -> str:
    # Keep existing bash/yaml content; wrap with Linux lab scaffolding if needed
    existing = existing.strip()
    if "### Step 1" in existing or "### Step 1 –" in existing:
        body = existing
        # ensure heading Focus
        if "**Focus:**" not in body:
            body = f"**Focus:** practise the core workflow for {title}\n\n" + body
        return body

    # Extract first mkdir path if present
    lab_dir = f"~/rebash-{tech}/lab01"
    m = re.search(r"mkdir -p (~/rebash-[^\s]+)", existing)
    if m:
        lab_dir = m.group(1)

    # Strip Environment-like leading mkdir if we'll re-add
    code = existing
    focus = f"**Focus:** hands-on practice for {title}"
    return f"""Create a workspace for this tutorial.

```bash
mkdir -p {lab_dir} && cd {lab_dir}
```

{focus}

### Step 1 – Core exercise

{code}

### Final step – Cleanup note

```bash
# Keep ~/rebash-{tech}/ for later tutorials; destroy disposable cloud resources from this lab
```
"""


def build_validation(lab_hint: str) -> str:
    return f"""- [ ] Lab commands run under `{lab_hint}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic
"""


def build_tail(title: str, tech: str, next_link: str, index_link: str, pitfalls: str) -> dict[str, str]:
    # Derive 2 warning titles from pitfalls bullets if possible
    bullets = re.findall(r"(?m)^-\s+(.+)$", pitfalls)
    w1 = bullets[0] if bullets else f"Skipping fundamentals for {title}"
    w2 = bullets[1] if len(bullets) > 1 else f"Treating lab defaults as production-ready for {title}"
    w1 = w1[:90]
    w2 = w2[:90]

    return {
        "Code Walkthrough": f"""Production practice for **{title}** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.
""",
        "Security Considerations": f"""- Treat credentials and tokens for {tech} as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces
""",
        "Common Mistakes": f"""!!! warning "{w1}"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "{w2}"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).
""",
        "Best Practices": f"""- Encode {title} changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible
""",
        "Troubleshooting": f"""| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |
""",
        "Summary": f"""**{title}** is essential for Cloud and DevOps engineers working with {tech}. Practise the lab until the inspection and change path is muscle memory, then continue the track.
""",
        "Interview Questions": f"""1. How does **{title}** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.
""",
        "Related Tutorials": f"""- [Course overview]({index_link})
- {next_link}
""",
    }


def convert(path: Path, dry_run: bool = False) -> str:
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    if "## Code Walkthrough" in body and "## Interview Questions" in body and "## Architecture" in body:
        return "skip-already-linux"

    sections = extract_sections(body)
    preamble = sections.pop("__preamble__", "")
    title = get_title(preamble, fm)
    tech = get_tech(fm, path)

    # Gather content from either Linux or Helm-style keys
    overview = sections.get("Overview", "")
    goal = sections.get("Goal", "")
    if goal and goal not in overview:
        overview = (goal.strip() + "\n\n" + overview).strip()
    # Strip diagram from overview (moves to Architecture)
    diagram = extract_diagram(overview) or extract_diagram(sections.get("Architecture", ""))
    overview_nodiag = re.sub(r"!\[[^\]]*\]\([^)]+\)\s*", "", overview).strip()
    overview_nodiag = re.sub(r"(?im)^Diagrams use \*\*Excalidraw\*\* only\.?\s*", "", overview_nodiag).strip()

    # Ensure tutorial line
    module = get_module(fm, overview_nodiag + "\n" + sections.get("Theory", ""))
    course_name = {
        "aws": "AWS for Cloud & DevOps Engineers",
        "helm": "Helm for Kubernetes Engineers",
        "terraform": "Terraform for Cloud & DevOps Engineers",
        "gitlab": "GitLab CI/CD for Cloud & DevOps Engineers",
        "github-actions": "GitHub Actions for Cloud & DevOps Engineers",
        "docker": "Docker for Cloud & DevOps Engineers",
        "kubernetes": "Kubernetes for Cloud & DevOps Engineers",
        "git": "Git for Cloud & DevOps Engineers",
        "networking": "Networking for Cloud & DevOps Engineers",
        "python": "Python for Cloud & DevOps Engineers",
        "linux": "Linux for Cloud & DevOps Engineers",
        "shell": "Shell Scripting for DevOps Engineers",
    }.get(tech, f"{tech} course")
    if "This is **Tutorial" not in overview_nodiag and "Tutorial" not in overview_nodiag[:200]:
        overview_nodiag += (
            f"\n\nThis is a core tutorial in **{module}** of the REBASH Academy "
            f"**{course_name}** series — written for Cloud, DevOps, Platform, and SRE engineers."
        )

    prereq = sections.get("Prerequisites", "- See the course overview for prerequisites")
    learn = sections.get("Learning Objectives") or sections.get("Learning objectives", "")
    if learn and not learn.startswith("By the end"):
        # ensure checkbox list has intro
        if "- [ ]" in learn:
            learn = "By the end of this tutorial, you will be able to:\n\n" + learn
    if not learn:
        learn = (
            "By the end of this tutorial, you will be able to:\n\n"
            f"- [ ] Apply the core ideas of “{title}” in a real environment\n"
            "- [ ] Complete the hands-on lab with clear outputs\n"
            "- [ ] Relate this topic to Cloud, DevOps, and production operations\n"
            "- [ ] Explain the failure modes you would check first in an incident\n"
        )

    theory = normalize_theory(sections.get("Theory", ""))
    lab_src = sections.get("Hands-on Lab") or sections.get("Hands-on lab") or ""
    env = sections.get("Environment setup", "")
    if env and env not in lab_src:
        lab_src = env + "\n\n" + lab_src
    lab = build_lab(lab_src, tech, title)

    lab_hint = f"~/rebash-{tech}/"
    m = re.search(r"mkdir -p (~/rebash-[^\s]+)", lab)
    if m:
        lab_hint = m.group(1)

    validation = sections.get("Validation", "")
    if "- [ ]" not in validation:
        validation = build_validation(lab_hint)

    refs = sections.get("References", f"- Track index: [Course overview](index.md)")
    # Next / Related
    next_sec = sections.get("Next", "")
    related_existing = sections.get("Related Tutorials", "")
    next_link = next_sec.strip() if next_sec.strip() else "- Continue from the course [index](index.md)"
    if next_link and not next_link.startswith("-"):
        next_link = "- " + next_link.replace("\n", "\n- ")

    pitfalls = ""
    if "### Common pitfalls" in theory:
        pitfalls = theory.split("### Common pitfalls", 1)[1]
    tail = build_tail(title, tech, next_link, "index.md", pitfalls)
    # Prefer existing sections if present
    for k in REQUIRED_TAIL:
        if k in sections and sections[k].strip():
            # Related Tutorials: merge next if needed
            if k == "Related Tutorials":
                continue
            tail[k] = sections[k].strip() + "\n"

    if related_existing.strip():
        related = related_existing.strip() + "\n"
    else:
        related = tail["Related Tutorials"]

    arch_intro = (
        sections.get("Architecture", "").strip()
        or "This topic’s control points and relationships are shown below."
    )
    # Remove diagram from arch if duplicated
    arch_intro = re.sub(r"!\[[^\]]*\]\([^)]+\)\s*", "", arch_intro).strip()
    if not arch_intro:
        arch_intro = "This topic’s control points and relationships are shown below."
    if not diagram:
        diagram = f"![Architecture diagram for {title}](../assets/excalidraw/{tech}-architecture.svg)"

    new_body = f"""# {title}

## Overview

{overview_nodiag}

## Prerequisites

{prereq.strip()}

## Learning Objectives

{learn.strip()}

## Architecture

{arch_intro}

{diagram}

## Theory

{theory}

## Hands-on Lab

{lab.strip()}

## Validation

{validation.strip()}

## Code Walkthrough

{tail['Code Walkthrough'].strip()}

## Security Considerations

{tail['Security Considerations'].strip()}

## Common Mistakes

{tail['Common Mistakes'].strip()}

## Best Practices

{tail['Best Practices'].strip()}

## Troubleshooting

{tail['Troubleshooting'].strip()}

## Summary

{tail['Summary'].strip()}

## Interview Questions

{tail['Interview Questions'].strip()}

## Related Tutorials

{related.strip()}

## References

{refs.strip()}
"""
    out = (fm + "\n\n" if fm else "") + new_body.strip() + "\n"
    if dry_run:
        return "dry-run-ok"
    path.write_text(out, encoding="utf-8")
    return "converted"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--course", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    paths: list[Path] = [Path(p) for p in args.paths]
    for c in args.course:
        paths.extend(sorted(Path(f"docs/{c}").glob("*.md")))
    skip_names = {
        "index.md",
        "roadmap.md",
        "faq.md",
    }
    counts = {"converted": 0, "skip-already-linux": 0, "skip-hub": 0, "error": 0}
    for path in paths:
        if path.name in skip_names:
            counts["skip-hub"] += 1
            continue
        if path.parent.name in {
            "modules",
            "labs",
            "projects",
            "quizzes",
            "cheatsheets",
            "interview",
            "certifications",
            "capstone",
        }:
            counts["skip-hub"] += 1
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"error {path}: {e}")
            counts["error"] += 1
            continue
        if "## Theory" not in text:
            counts["skip-hub"] += 1
            continue
        status = convert(path, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:20} {path}")
    print(counts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
