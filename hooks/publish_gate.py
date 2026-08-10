"""Publish gate: only ready content is built and served.

Removes stub technology trees and empty “coming soon” section hubs from the
MkDocs file set so they do not appear in navigation, search, or the sitemap.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from mkdocs.structure.files import Files

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_PATH = ROOT / "curriculum.yaml"
DOCS = ROOT / "docs"

# Technologies with no real course body — never publish until content ships.
STUB_TECHS = frozenset(
    {
        "azure",
        "prometheus",
        "grafana",
        "loki",
        "tempo",
        "opentelemetry",
        "devsecops",
        "platform-engineering",
        "sre",
        "architecture",
        "monitoring",
        "security",
    }
)

# Site-wide shells with no substantive pages yet.
STUB_SITE_DIRS = frozenset(
    {
        "community",
        "youtube",
        "capstones",
        "certifications",
        "career-paths",
    }
)

# Per-technology section folders that are publishable only when they contain
# at least one non-index markdown page.
SECTION_DIRS = frozenset(
    {
        "quizzes",
        "projects",
        "capstone",
        "certifications",
        "cheatsheets",
        "interview",
        "labs",
    }
)


def _load_stub_techs() -> set[str]:
    """Prefer curriculum status; fall back to the hard-coded stub set."""
    stubs = set(STUB_TECHS)
    if not CURRICULUM_PATH.is_file():
        return stubs
    try:
        data = yaml.safe_load(CURRICULUM_PATH.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return stubs
    for item in data.get("technologies") or []:
        tech_id = str(item.get("id") or "").strip()
        status = str(item.get("status") or "").lower()
        tutorial_count = item.get("tutorial_count") or 0
        try:
            tutorial_count = int(tutorial_count)
        except (TypeError, ValueError):
            tutorial_count = 0
        if not tech_id:
            continue
        if status in {"stub", "planned"} and tutorial_count == 0:
            # Keep techs that already have deep on-disk tutorials even if
            # curriculum.yaml has not been refreshed yet.
            tech_dir = DOCS / tech_id
            leaf = 0
            if tech_dir.is_dir():
                leaf = sum(
                    1
                    for path in tech_dir.rglob("*.md")
                    if path.name != "index.md"
                    and path.parent.name not in SECTION_DIRS
                    and path.name not in {"faq.md", "roadmap.md"}
                )
            if leaf < 5:
                stubs.add(tech_id)
            elif tech_id in stubs:
                stubs.discard(tech_id)
        elif status == "ready" and tech_id in stubs:
            stubs.discard(tech_id)
    return stubs


def _section_has_leaf_pages(section_dir: Path) -> bool:
    if not section_dir.is_dir():
        return False
    return any(path.name != "index.md" for path in section_dir.rglob("*.md"))


def _should_exclude(src_path: str, stub_techs: set[str]) -> bool:
    uri = src_path.replace("\\", "/").lstrip("./")
    if not uri.endswith(".md") and not uri.endswith(".pages"):
        # Keep assets; only gate documentation pages and nav files under stubs.
        parts = uri.split("/")
        if parts and parts[0] in stub_techs | STUB_SITE_DIRS:
            return True
        return False

    parts = uri.split("/")
    if not parts:
        return False

    top = parts[0]
    if top in stub_techs or top in STUB_SITE_DIRS:
        return True

    # Empty per-tech section hubs (index-only quizzes/projects/…)
    if len(parts) >= 2 and parts[1] in SECTION_DIRS:
        section_dir = DOCS / parts[0] / parts[1]
        if section_dir.is_dir() and not _section_has_leaf_pages(section_dir):
            return True

    return False


def on_files(files: Files, config) -> Files:
    stub_techs = _load_stub_techs()
    keep = []
    removed = 0
    for file in files:
        src = file.src_uri.replace("\\", "/")
        if _should_exclude(src, stub_techs):
            removed += 1
            continue
        keep.append(file)
    if removed:
        print(f"[publish_gate] excluded {removed} unpublished stub/coming-soon files")
    return Files(keep)


def on_page_markdown(markdown, page, config, files):
    """Mark any remaining planned/stub shells as noindex + search-excluded."""
    meta = page.meta or {}
    status = str(meta.get("status") or "").lower()
    try:
        tutorial_count = int(meta["tutorial_count"]) if meta.get("tutorial_count") is not None else None
    except (TypeError, ValueError):
        tutorial_count = None

    if status in {"planned", "stub"} and (tutorial_count == 0 or tutorial_count is None):
        if not meta.get("robots"):
            page.meta["robots"] = "noindex, follow"
        search_meta = meta.get("search")
        if not isinstance(search_meta, dict):
            search_meta = {}
        search_meta["exclude"] = True
        page.meta["search"] = search_meta

    return markdown


def on_page_context(context, page, config, nav):
    """Expose robots directive to overrides/main.html."""
    robots = None
    if page and page.meta:
        robots = page.meta.get("robots")
    context["seo_robots"] = robots or "index, follow"
    return context
