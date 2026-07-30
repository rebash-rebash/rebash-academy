#!/usr/bin/env python3
"""Generate course navigation structure from curriculum.yaml for every technology track."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_PATH = ROOT / "curriculum.yaml"
DISPLAY_PATH = ROOT / "docs" / "_curriculum" / "course-display.yaml"
DOCS = ROOT / "docs"

ICON_BY_TECH = {
    "linux": "material/linux",
    "shell": "material/bash",
    "python": "material/language-python",
    "networking": "material/lan",
    "git": "material/git",
    "docker": "material/docker",
    "kubernetes": "material/kubernetes",
    "terraform": "material/terraform",
    "aws": "material/aws",
    "gitlab": "material/gitlab",
    "helm": "material/ship-wheel",
    "ansible": "material/ansible",
    "azure": "material/microsoft-azure",
    "gcp": "material/google-cloud",
    "github-actions": "material/github",
    "jenkins": "material/cog",
    "argocd": "material/sync",
    "prometheus": "material/chart-line",
    "grafana": "material/monitor",
    "loki": "material/text-box-search",
    "tempo": "material/timeline-clock",
    "opentelemetry": "material/pulse",
    "devsecops": "material/shield-lock",
    "platform-engineering": "material/layers",
    "sre": "material/pulse",
    "architecture": "material/sitemap",
    "ai": "material/brain",
    "monitoring": "material/monitor",
    "security": "material/lock",
}


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def tutorial_index(curriculum: dict) -> dict[str, dict]:
    return {item["id"]: item for item in curriculum.get("tutorials", [])}


def module_number(module_id: str, fallback: int) -> int:
    match = re.search(r"-m(\d+)$", module_id)
    return int(match.group(1)) if match else fallback


def tutorial_filename(tutorial_id: str) -> str:
    slug = tutorial_id.split("/")[-1]
    return f"{slug}.md"


def tutorial_nav_title(tutorial_id: str, index: dict[str, dict]) -> str:
    meta = index.get(tutorial_id, {})
    return meta.get("title", tutorial_id.split("/")[-1].replace("-", " ").title())


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def section_stub(tech: dict, title: str, global_section: str, section_key: str) -> str:
    tech_id = tech["id"]
    tech_title = tech["title"]
    return f"""---
title: {title}
description: "{title} for the {tech_title} course — curriculum-aware list from the Academy catalog."
technology_id: {tech_id}
template: course-section.html
section: {section_key}
hide:
  - toc
---

# {title}

Curriculum-aware section hub — rendered by the site theme from published **{tech_title}** resources.
Browse the wider [{global_section} catalog](../../{global_section}/) for related material.
"""


def roadmap_stub(tech: dict) -> str:
    title = tech["title"]
    tech_id = tech["id"]
    lines = [
        "---",
        "title: Learning Roadmap",
        f'description: "Structured learning roadmap for the {title} course."',
        f"technology_id: {tech_id}",
        "hide:",
        "  - toc",
        "---",
        "",
        f"# {title} — Learning Roadmap",
        "",
        "Follow the course in order:",
        "",
        "1. **Course overview** — understand scope, prerequisites, and outcomes",
        "2. **Modules** — work through tutorials module by module",
        "3. **Labs** — hands-on practice after core lessons",
        "4. **Quizzes** — check understanding before projects",
        "5. **Projects** — portfolio builds that connect multiple skills",
        "6. **Capstone** — end-to-end proof of production readiness",
        "7. **Interview preparation** — role-specific questions and scenarios",
        "8. **Certifications** — map lessons to industry exams",
        "",
        "![Course navigation flow](../assets/images/course-navigation.svg)",
        "",
        "## Modules",
        "",
    ]
    index = tutorial_index(load_yaml(CURRICULUM_PATH))
    for idx, module in enumerate(tech.get("modules", []), start=1):
        number = module_number(module.get("id", ""), idx)
        lines.append(f"### {module.get('title', f'Module {number}')}")
        lines.append("")
        for tutorial_id in module.get("tutorials", []):
            slug = tutorial_id.split("/")[-1]
            ttitle = tutorial_nav_title(tutorial_id, index)
            lines.append(f"- [{ttitle}](../{slug}/)")
        lines.append("")
    return "\n".join(lines) + "\n"


def faq_stub(tech: dict) -> str:
    title = tech["title"]
    tech_id = tech["id"]
    status = tech.get("status", "planned")
    return f"""---
title: FAQ
description: "Frequently asked questions about the {title} course."
technology_id: {tech_id}
template: course-faq.html
status: {status}
hide:
  - toc
---

# {title} — FAQ

FAQ hub — rendered by the site theme from live course metadata.
"""


def module_index(tech_id: str, module: dict, number: int) -> str:
    return f"""---
title: "{module.get('title', f'Module {number}')}"
description: "Module {number} of the {tech_id.replace('-', ' ').title()} course."
template: module.html
technology_id: {tech_id}
module_id: {module.get('id', f'{tech_id}-m{number}')}
hide:
  - toc
---

# {module.get('title', f'Module {number}')}

Module landing page — rendered by the course template. Open a tutorial from the list below or the sidebar.
"""


def course_index_frontmatter(tech: dict, existing: dict | None) -> str:
    tech_id = tech["id"]
    display = load_yaml(DISPLAY_PATH).get(tech_id, {})
    merged = dict(existing or {})
    merged.setdefault("title", "Overview")
    merged["template"] = "course.html"
    merged["technology_id"] = tech_id
    merged.setdefault("description", display.get("tagline", f"{tech['title']} course on REBASH Academy."))
    merged.setdefault("difficulty", tech.get("difficulty", "intermediate"))
    merged.setdefault("status", tech.get("status", "planned"))
    merged.setdefault("category", tech_id)
    merged.setdefault("tutorial_count", tech.get("tutorial_count", 0))
    merged.setdefault("comments", False)
    merged.setdefault("hide", ["toc"])
    if "tags" not in merged:
        merged["tags"] = [tech_id, "course"]
    return yaml.safe_dump(merged, sort_keys=False, allow_unicode=True).strip()


def modules_index_stub(tech: dict) -> str:
    tech_id = tech["id"]
    title = tech["title"]
    count = len(tech.get("modules", []))
    return f"""---
title: Modules
description: "Browse all {count} modules in the {title} course."
template: modules.html
technology_id: {tech_id}
hide:
  - toc
---

# {title} Modules

Module catalog — rendered by the course template.
"""


def build_pages_nav(tech: dict, index: dict[str, dict]) -> str:
    tech_id = tech["id"]
    icon = ICON_BY_TECH.get(tech_id, "material/book-open-variant")
    lines = [
        f"title: {tech['title']}",
        f"icon: {icon}",
        "",
        "nav:",
        "  - Overview: index.md",
        "  - Roadmap: roadmap.md",
    ]

    if tech.get("modules"):
        lines.append("  - Modules:")
        lines.append("    - Browse Modules: modules/index.md")
        for idx, module in enumerate(tech["modules"], start=1):
            number = module_number(module.get("id", ""), idx)
            mod_title = module.get("title", f"Module {number}")
            mod_dir = f"modules/module-{number:02d}/index.md"
            tutorials = module.get("tutorials", [])
            if tutorials:
                lines.append(f"    - \"{mod_title}\":")
                lines.append(f"      - Overview: {mod_dir}")
                for tutorial_id in tutorials:
                    fname = tutorial_filename(tutorial_id)
                    ttitle = tutorial_nav_title(tutorial_id, index)
                    lines.append(f"      - \"{ttitle}\": {fname}")
            else:
                lines.append(f"    - \"{mod_title}\": {mod_dir}")

    lines.extend(
        [
            "  - Labs: labs/index.md",
            "  - Quizzes: quizzes/index.md",
            "  - Projects: projects/index.md",
            "  - Capstone: capstone/index.md",
            "  - Cheat Sheets: cheatsheets/index.md",
            "  - Interview Preparation: interview/index.md",
            "  - Certifications: certifications/index.md",
            "  - FAQ: faq.md",
            "",
        ]
    )
    return "\n".join(lines)


def parse_existing_frontmatter(path: Path) -> dict | None:
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1)) or {}


def generate_for_technology(tech: dict, index: dict[str, dict]) -> int:
    tech_id = tech["id"]
    tech_dir = DOCS / tech_id
    if not tech_dir.is_dir():
        print(f"skip {tech_id}: docs/{tech_id}/ missing")
        return 0

    changed = 0
    tech_dir.mkdir(parents=True, exist_ok=True)

    # Course index
    index_path = tech_dir / "index.md"
    existing_fm = parse_existing_frontmatter(index_path)
    fm = course_index_frontmatter(tech, existing_fm)
    index_body = (
        f"# {tech['title']}\n\n"
        "Course homepage — rendered by the site theme. "
        "Browse modules from the sidebar or start with the first module.\n"
    )
    index_content = f"---\n{fm}\n---\n\n{index_body}"
    if write_if_changed(index_path, index_content):
        changed += 1

    stubs = {
        "roadmap.md": roadmap_stub(tech),
        "faq.md": faq_stub(tech),
        "quizzes/index.md": section_stub(tech, "Quizzes", "quizzes", "quizzes"),
        "projects/index.md": section_stub(tech, "Projects", "projects", "projects"),
        "capstone/index.md": section_stub(tech, "Capstone", "capstones", "capstone"),
        "cheatsheets/index.md": section_stub(tech, "Cheat Sheets", "cheatsheets", "cheatsheets"),
        "interview/index.md": section_stub(tech, "Interview Preparation", "interview", "interview"),
        "certifications/index.md": section_stub(tech, "Certification Mapping", "certifications", "certifications"),
        "labs/index.md": (
            "---\n"
            f"title: Labs\n"
            f'description: "Hands-on labs for the {tech["title"]} course."\n'
            f"technology_id: {tech['id']}\n"
            "template: course-labs.html\n"
            "hide:\n"
            "  - toc\n"
            "---\n\n"
            "# Labs\n\n"
            "Course labs hub — rendered by the site theme from published lab pages.\n"
        ),
    }
    if tech.get("modules"):
        stubs["modules/index.md"] = modules_index_stub(tech)
    for rel, content in stubs.items():
        if write_if_changed(tech_dir / rel, content):
            changed += 1

    for idx, module in enumerate(tech.get("modules", []), start=1):
        number = module_number(module.get("id", ""), idx)
        mod_path = tech_dir / f"modules/module-{number:02d}/index.md"
        if write_if_changed(mod_path, module_index(tech_id, module, number)):
            changed += 1

    pages_path = tech_dir / ".pages"
    pages_content = build_pages_nav(tech, index)
    if write_if_changed(pages_path, pages_content):
        changed += 1

    return changed


def main() -> int:
    curriculum = load_yaml(CURRICULUM_PATH)
    index = tutorial_index(curriculum)
    total = 0
    for tech in curriculum.get("technologies", []):
        count = generate_for_technology(tech, index)
        total += count
        print(f"{tech['id']}: {count} file(s) updated")
    print(f"Done — {total} file(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
