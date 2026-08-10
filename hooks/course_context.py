"""Inject course and module context from curriculum.yaml for course templates."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM_PATH = ROOT / "curriculum.yaml"
DISPLAY_PATH = ROOT / "docs" / "_curriculum" / "course-display.yaml"
DOCS = ROOT / "docs"

_CATALOG_COURSE_EXCLUDE = frozenset(
    {
        "assets",
        "includes",
        "_curriculum",
        "blog",
        "labs",
        "quizzes",
        "projects",
        "capstones",
        "cheatsheets",
        "interview",
        "certifications",
        "career-paths",
        "learning-paths",
        "technologies",
        "getting-started",
        "about",
        "architecture-guides",
        "youtube",
        "community",
    }
)


@lru_cache(maxsize=1)
def _load_curriculum() -> dict:
    with CURRICULUM_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _count_leaf_md(directory: Path) -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for f in directory.glob("*.md") if f.name != "index.md")


@lru_cache(maxsize=1)
def build_catalog_stats() -> dict:
    """Return inventory counts derived from docs/ (no marketing inflation)."""
    paths_dir = DOCS / "career-paths"
    paths = sum(1 for p in paths_dir.iterdir() if p.is_dir()) if paths_dir.is_dir() else 0
    courses = sorted(
        p.name
        for p in DOCS.iterdir()
        if p.is_dir() and p.name not in _CATALOG_COURSE_EXCLUDE and (p / "index.md").exists()
    )
    tutorials = 0
    for course in courses:
        for path in (DOCS / course).rglob("*.md"):
            if path.name == "index.md" or "modules" in path.parts:
                continue
            tutorials += 1
    return {
        "learning_paths": paths,
        "courses": len(courses),
        "tutorials": tutorials,
        "labs": _count_leaf_md(DOCS / "labs"),
        "quizzes": _count_leaf_md(DOCS / "quizzes"),
        "projects": _count_leaf_md(DOCS / "projects"),
        "cheatsheets": _count_leaf_md(DOCS / "cheatsheets"),
        "architecture_guides": _count_leaf_md(DOCS / "architecture-guides"),
        "blog_posts": _count_leaf_md(DOCS / "blog"),
    }


@lru_cache(maxsize=1)
def _load_display() -> dict:
    if not DISPLAY_PATH.is_file():
        return {}
    with DISPLAY_PATH.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


@lru_cache(maxsize=1)
def _tutorial_index() -> dict[str, dict]:
    curriculum = _load_curriculum()
    return {item["id"]: item for item in curriculum.get("tutorials", [])}


@lru_cache(maxsize=1)
def _technology_index() -> dict[str, dict]:
    curriculum = _load_curriculum()
    return {item["id"]: item for item in curriculum.get("technologies", [])}


@lru_cache(maxsize=1)
def _lab_index() -> dict[str, dict]:
    """Merge curriculum labs with docs/labs frontmatter (description, time)."""
    curriculum = _load_curriculum()
    index: dict[str, dict] = {}
    for item in curriculum.get("labs", []) or []:
        lab_id = item.get("id", "")
        if lab_id:
            index[lab_id] = dict(item)

    labs_dir = ROOT / "docs" / "labs"
    if labs_dir.is_dir():
        for path in labs_dir.glob("*.md"):
            lab_id = f"labs/{path.stem}"
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if not text.startswith("---"):
                continue
            parts = text.split("---", 2)
            if len(parts) < 3:
                continue
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                meta = {}
            entry = index.get(lab_id, {"id": lab_id})
            entry.update(
                {
                    "title": meta.get("title") or entry.get("title") or path.stem.replace("-", " ").title(),
                    "description": meta.get("description") or entry.get("description", ""),
                    "estimated_time": meta.get("estimated_time") or entry.get("estimated_time", ""),
                    "difficulty": meta.get("difficulty") or entry.get("difficulty", ""),
                    "status": entry.get("status") or meta.get("status") or "ready",
                    "path": entry.get("path") or f"labs/{path.stem}.md",
                }
            )
            index[lab_id] = entry
    return index


def _lab_href(lab_id: str) -> str:
    slug = lab_id.split("/")[-1] if "/" in lab_id else lab_id
    return f"labs/{slug}/"


def _labs_for_tech(tech_id: str, lab_ids: list[str] | None = None) -> list[dict]:
    """Resolve labs for a technology (and optional explicit id list)."""
    resolved = list(lab_ids or [])
    if not resolved:
        prefix = f"labs/{tech_id}-"
        resolved = sorted(lab_id for lab_id in _lab_index() if lab_id.startswith(prefix))

    icons = (
        "monitor",
        "folder-outline",
        "account-outline",
        "lock-outline",
        "package-variant",
        "cog-outline",
        "flask-outline",
        "console",
    )
    labs = []
    for i, lab_id in enumerate(resolved):
        meta = _lab_index().get(lab_id, {})
        slug = lab_id.split("/")[-1]
        title = meta.get("title", slug.replace("-", " ").title())
        title = re.sub(r"^Lab\s*[—–-]\s*", "", title).strip()
        labs.append(
            {
                "id": lab_id,
                "number_label": f"{i + 1:02d}",
                "title": title,
                "description": meta.get("description", ""),
                "estimated_time": meta.get("estimated_time") or "30–40 min",
                "url": _lab_href(lab_id),
                "icon": icons[i % len(icons)],
                "status": meta.get("status", "ready"),
            }
        )
    return labs


def _labs_for_module(tech_id: str, module: dict) -> list[dict]:
    """Resolve module labs, falling back to course labs for the technology."""
    lab_ids = list(module.get("labs") or [])
    if module.get("lab") and module["lab"] not in lab_ids:
        lab_ids.append(module["lab"])
    return _labs_for_tech(tech_id, lab_ids or None)


def _labs_for_course(tech_id: str) -> list[dict]:
    """All published labs for a technology course."""
    return _labs_for_tech(tech_id)


def _quiz_href(quiz_id: str) -> str:
    slug = quiz_id.split("/")[-1] if "/" in quiz_id else quiz_id
    return f"quizzes/{slug}/"


def _count_quiz_questions(body: str) -> int:
    return len(re.findall(r"(?m)^###\s+Question\s+\d+", body or ""))


def _quiz_index() -> dict[str, dict]:
    """Index docs/quizzes/*.md frontmatter for course/module quiz lists."""
    quizzes_dir = ROOT / "docs" / "quizzes"
    index: dict[str, dict] = {}
    if not quizzes_dir.is_dir():
        return index
    for path in quizzes_dir.glob("*.md"):
        if path.name == "index.md":
            continue
        quiz_id = f"quizzes/{path.stem}"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            meta = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            meta = {}
        body = parts[2]
        question_count = meta.get("question_count") or _count_quiz_questions(body)
        tags = meta.get("tags") or []
        tech = meta.get("technology")
        if not tech:
            for tag in tags:
                if isinstance(tag, str) and tag in _technology_index():
                    tech = tag
                    break
        if not tech:
            tech = _technology_from_lab_slug(path.stem, meta)
        index[quiz_id] = {
            "id": quiz_id,
            "title": meta.get("title") or path.stem.replace("-", " ").title(),
            "description": meta.get("description", ""),
            "difficulty": (meta.get("difficulty") or "intermediate").lower(),
            "estimated_time": meta.get("estimated_time", ""),
            "passing_score": meta.get("passing_score", "70%"),
            "question_count": int(question_count) if question_count else 0,
            "quiz_type": meta.get("quiz_type") or "course",
            "module": meta.get("module") or "",
            "technology": tech or "",
            "tags": tags,
            "status": meta.get("status") or "ready",
            "path": f"quizzes/{path.stem}.md",
        }
    return index


def _quizzes_for_module(tech_id: str, module: dict) -> list[dict]:
    """Resolve quizzes for a module from curriculum ids or technology/module match."""
    quiz_ids = list(module.get("quizzes") or [])
    if module.get("quiz") and module["quiz"] not in quiz_ids:
        quiz_ids.append(module["quiz"])

    index = _quiz_index()
    if not quiz_ids:
        module_title = (module.get("title") or "").lower()
        short = module_title.split("·", 1)[-1].strip().lower() if "·" in module_title else module_title
        number = _module_number(module.get("id", ""), 0)
        matched = []
        for quiz_id, meta in index.items():
            if meta.get("technology") != tech_id and not quiz_id.startswith(f"quizzes/{tech_id}-"):
                # also allow stem without trailing tech prefix patterns like cicd-* for gitlab
                tags = meta.get("tags") or []
                if tech_id not in tags and tech_id not in quiz_id:
                    continue
            mod_field = (meta.get("module") or "").lower()
            title = (meta.get("title") or "").lower()
            stem = quiz_id.split("/")[-1]
            # Explicit module frontmatter match
            if mod_field and (short in mod_field or f"module {number}" in mod_field or f"module {number:02d}" in mod_field):
                matched.append(quiz_id)
                continue
            # Keyword overlap with module short title (e.g. Fundamentals, Servers)
            tokens = [
                t
                for t in re.split(r"[^a-z0-9]+", short)
                if len(t) > 3 and t != tech_id.replace("-", "")
            ]
            if tokens and any(tok in title or tok in stem or tok in mod_field for tok in tokens):
                matched.append(quiz_id)
                continue
        if matched:
            quiz_ids = sorted(set(matched))
        elif number == 1:
            # First module: show technology course quizzes as the entry assessment
            quiz_ids = sorted(
                qid
                for qid, meta in index.items()
                if meta.get("technology") == tech_id
                or qid.startswith(f"quizzes/{tech_id}-")
                or tech_id in (meta.get("tags") or [])
            )

    icons = (
        "console",
        "folder-outline",
        "account-outline",
        "cog-outline",
        "package-variant",
        "shield-check-outline",
        "help-circle-outline",
        "clipboard-check-outline",
    )
    level_label = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "expert": "Expert",
    }
    quizzes = []
    for i, quiz_id in enumerate(quiz_ids):
        if not quiz_id.startswith("quizzes/"):
            quiz_id = f"quizzes/{quiz_id}" if "/" not in quiz_id else quiz_id
        meta = index.get(quiz_id, {})
        slug = quiz_id.split("/")[-1]
        title = meta.get("title", slug.replace("-", " ").title())
        title = re.sub(r"^Quiz\s*[—–-]\s*", "", title).strip()
        difficulty = (meta.get("difficulty") or "intermediate").lower()
        quizzes.append(
            {
                "id": quiz_id,
                "number_label": f"{i + 1:02d}",
                "title": title,
                "description": meta.get("description", ""),
                "question_count": meta.get("question_count") or 20,
                "difficulty": difficulty,
                "difficulty_label": level_label.get(difficulty, difficulty.title()),
                "estimated_time": meta.get("estimated_time") or "30–45 min",
                "url": _quiz_href(quiz_id),
                "icon": icons[i % len(icons)],
                "status": meta.get("status", "ready"),
            }
        )
    return quizzes


def _labs_total_time_label(labs: list[dict]) -> str:
    total = 0
    for lab in labs:
        total += _parse_minutes(lab.get("estimated_time", ""))
    if total <= 0:
        return "~2–3 hrs" if labs else "—"
    if total >= 60:
        lo = max(1, round(total / 60))
        hi = max(lo, round(total / 60 * 1.25))
        return f"~{lo}–{hi} hrs" if hi > lo else f"~{lo} hrs"
    return f"~{total} min"


def _module_number(module_id: str, fallback: int) -> int:
    match = re.search(r"-m(\d+)$", module_id)
    if match:
        return int(match.group(1))
    return fallback


def _tutorial_href(tutorial_id: str) -> str:
    if "/" not in tutorial_id:
        return f"{tutorial_id}/"
    prefix, slug = tutorial_id.split("/", 1)
    return f"{prefix}/{slug}/"


MODULE_CARD_THEMES = [
    {"icon": "linux", "accent": "blue"},
    {"icon": "console", "accent": "green"},
    {"icon": "folder-outline", "accent": "purple"},
    {"icon": "account-group-outline", "accent": "orange"},
    {"icon": "text-box-outline", "accent": "teal"},
    {"icon": "cog-outline", "accent": "pink"},
    {"icon": "server", "accent": "blue"},
    {"icon": "database", "accent": "green"},
    {"icon": "lan", "accent": "purple"},
    {"icon": "package-variant", "accent": "orange"},
    {"icon": "clock-outline", "accent": "teal"},
    {"icon": "chart-line", "accent": "pink"},
    {"icon": "shield-check-outline", "accent": "blue"},
    {"icon": "docker", "accent": "green"},
    {"icon": "wrench-outline", "accent": "purple"},
    {"icon": "cloud-outline", "accent": "orange"},
]


def _module_description(module: dict, short_title: str, tutorials: list[dict]) -> str:
    if module.get("description"):
        return module["description"]
    count = len(tutorials)
    if count == 1:
        return f"One tutorial covering core {short_title.lower()} skills for production work."
    if count > 1:
        topics = ", ".join(t["title"].lower() for t in tutorials[:2])
        extra = count - 2
        if extra > 0:
            return f"{count} tutorials covering {topics}, and {extra} more {short_title.lower()} topic{'s' if extra != 1 else ''}."
        return f"{count} tutorials covering {topics}."
    return f"Build practical {short_title.lower()} skills with guided tutorials and exercises."


def _parse_minutes(estimated_time: str) -> int:
    if not estimated_time:
        return 45
    nums = [int(x) for x in re.findall(r"\d+", estimated_time)]
    return sum(nums) // len(nums) if nums else 45


def _module_duration_label(tutorials: list[dict]) -> str:
    if not tutorials:
        return "~30 min"
    total = sum(_parse_minutes(t.get("estimated_time", "")) for t in tutorials)
    if total >= 60:
        hrs = round(total / 60 * 2) / 2
        label = f"{hrs:g}"
        return f"~{label} hrs"
    return f"~{total} min"


def _module_learning_outcomes(tutorials: list[dict], short_title: str) -> list[str]:
    if not tutorials:
        return [f"Build practical {short_title.lower()} skills with guided exercises."]
    outcomes = []
    for tutorial in tutorials[:4]:
        title = tutorial["title"].split("—")[0].split("–")[0].strip()
        outcomes.append(f"Understand {title.lower()} for production Linux work")
    return outcomes


def _module_prerequisites(tutorials: list[dict], module_number: int) -> list[str]:
    if not tutorials:
        return ["None"] if module_number == 1 else ["Complete earlier modules first"]
    meta = _tutorial_index().get(tutorials[0].get("id", ""), {})
    prereq_ids = meta.get("prerequisites") or []
    if not prereq_ids:
        return ["None"] if module_number == 1 else ["Complete earlier modules in this course"]
    labels = []
    for prereq_id in prereq_ids[:3]:
        labels.append(_tutorial_index().get(prereq_id, {}).get("title", prereq_id.split("/")[-1].replace("-", " ").title()))
    return labels


def _module_tagline(module: dict, short_title: str, tutorials: list[dict]) -> str:
    if module.get("description"):
        return module["description"]
    if len(tutorials) == 1:
        return f"Core {short_title.lower()} concepts for cloud and DevOps engineers."
    return f"{short_title} — {len(tutorials)} lessons covering essentials through production patterns."


def build_module_nav(active: str = "overview", *, module_path: str = "") -> list[dict]:
    """Build module-scoped nav. When module_path is set (lesson pages), links go to the module page."""
    items = [
        {"label": "Overview", "icon": "view-dashboard-outline", "hash": "overview", "active": active == "overview"},
        {"label": "Lessons", "icon": "book-open-variant", "hash": "lessons", "active": active == "lessons"},
        {"label": "Quiz", "icon": "help-circle-outline", "hash": "quiz", "active": active == "quiz"},
    ]
    for item in items:
        if module_path:
            item["href"] = f"{module_path}#tab-{item['hash']}"
            item["same_page"] = False
        else:
            item["href"] = f"#tab-{item['hash']}"
            item["same_page"] = True
    return items


def inject_lesson_layout(context: dict, course: dict, module: dict, tutorial: dict) -> None:
    """Inject lesson page context for a tutorial inside a course module."""
    tutorials = module.get("tutorials", [])
    index = next((i for i, t in enumerate(tutorials) if t.get("id") == tutorial.get("id")), 0)
    prev_tutorial = tutorials[index - 1] if index > 0 else None
    next_tutorial = tutorials[index + 1] if index + 1 < len(tutorials) else None
    module_path = course["path_prefix"] + module["url"]

    inject_course_layout(context, course, "modules", show_back=False)
    context["module"] = module
    context["lesson"] = tutorial
    context["lesson_index"] = index + 1
    context["lesson_total"] = len(tutorials)
    context["lesson_prev"] = prev_tutorial
    context["lesson_next"] = next_tutorial
    context["course_active_module"] = module["number"]
    context["course_active_lesson"] = tutorial.get("url") or tutorial.get("id", "")
    context["module_nav"] = build_module_nav("lessons", module_path=module_path)
    context["module_show_back"] = True
    context["module_back_url"] = module_path
    context["module_back_label"] = "Back to Module Overview"
    context["module_sidebar_cta_title"] = "Need help?"
    context["module_sidebar_cta_text"] = "Ask questions and learn with other engineers."
    context["module_sidebar_cta_label"] = "Visit Community"
    context["module_start_url"] = "about/"
    context["module_cta_external"] = False


def _enrich_module(tech_id: str, module: dict, index: int, *, course_difficulty: str = "intermediate") -> dict:
    tutorials = []
    for tutorial_id in module.get("tutorials", []):
        meta = _tutorial_index().get(tutorial_id, {})
        slug = tutorial_id.split("/")[-1]
        tutorials.append(
            {
                "id": tutorial_id,
                "title": meta.get("title", slug.replace("-", " ").title()),
                "url": _tutorial_href(tutorial_id),
                "status": meta.get("status", "planned"),
                "difficulty": meta.get("difficulty", ""),
                "estimated_time": meta.get("estimated_time", ""),
            }
        )

    number = _module_number(module.get("id", ""), index)
    short_title = module.get("title", f"Module {number}")
    if "·" in short_title:
        short_title = short_title.split("·", 1)[1].strip()

    theme = MODULE_CARD_THEMES[(number - 1) % len(MODULE_CARD_THEMES)]
    difficulty_key = (module.get("difficulty") or course_difficulty or "intermediate").lower()
    difficulty_label = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "expert": "Expert",
    }.get(difficulty_key, difficulty_key.title())
    first_tutorial_url = tutorials[0]["url"] if tutorials else ""
    labs = _labs_for_module(tech_id, module)
    quizzes = _quizzes_for_module(tech_id, module)

    return {
        "id": module.get("id", f"{tech_id}-m{number}"),
        "number": number,
        "number_label": f"{number:02d}",
        "title": module.get("title", f"Module {number}"),
        "short_title": short_title,
        "tagline": _module_tagline(module, short_title, tutorials),
        "description": _module_description(module, short_title, tutorials),
        "url": f"modules/module-{number:02d}/",
        "card_icon": theme["icon"],
        "card_accent": theme["accent"],
        "tutorials": tutorials,
        "tutorial_count": len(tutorials),
        "labs": labs,
        "labs_count": len(labs),
        "labs_total_time": _labs_total_time_label(labs),
        "quizzes": quizzes,
        "quiz_count": len(quizzes),
        "project_count": 1 if module.get("project") else 0,
        "duration_label": _module_duration_label(tutorials),
        "difficulty_label": difficulty_label,
        "learning_outcomes": module.get("learning_outcomes") or _module_learning_outcomes(tutorials, short_title),
        "prerequisites": _module_prerequisites(tutorials, number),
        "first_tutorial_url": first_tutorial_url,
    }


def build_course(tech_id: str) -> dict | None:
    tech = _technology_index().get(tech_id)
    if not tech:
        return None

    display_root = _load_display()
    display = display_root.get(tech_id, {})
    path_titles = display_root.get("career_path_titles", {})

    modules = [
        _enrich_module(tech_id, module, idx, course_difficulty=tech.get("difficulty", "intermediate"))
        for idx, module in enumerate(tech.get("modules", []), start=1)
    ]

    first_module_url = modules[0]["url"] if modules else ""
    first_tutorial_url = modules[0]["tutorials"][0]["url"] if modules and modules[0]["tutorials"] else ""

    related = []
    for related_id in display.get("related", []):
        related_tech = _technology_index().get(related_id, {})
        related_display = display_root.get(related_id, {})
        related.append(
            {
                "id": related_id,
                "title": related_tech.get("title", related_id.replace("-", " ").title()),
                "url": f"{related_id}/",
                "icon": related_display.get("icon", "book-open-variant"),
                "theme": related_display.get("theme", "devops"),
                "status": related_tech.get("status", "planned"),
            }
        )

    career_paths = []
    for path_id in display.get("career_paths", []):
        career_paths.append(
            {
                "id": path_id,
                "title": path_titles.get(path_id, path_id.replace("-", " ").title()),
                "url": f"career-paths/{path_id}/",
            }
        )

    certifications = display.get("certifications", [])
    if isinstance(certifications, list):
        cert_items = [{"name": name} for name in certifications]
    else:
        cert_items = []

    difficulty_key = (tech.get("difficulty") or "intermediate").lower()
    difficulty_label = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "expert": "Expert",
    }.get(difficulty_key, difficulty_key.title())

    tutorial_count = tech.get("tutorial_count") or sum(m["tutorial_count"] for m in modules)

    duration_label = _estimate_course_duration(len(modules), tutorial_count)
    prerequisites = []
    if related:
        prerequisites.append(f"Comfort with related foundations: {related[0]['title']}")
    if difficulty_key != "beginner":
        prerequisites.insert(0, "Complete an earlier foundations course (Linux, Git, or Networking) first")
    else:
        prerequisites.insert(0, "A laptop with terminal access and willingness to practise hands-on")

    return {
        "id": tech_id,
        "title": tech.get("title", tech_id.replace("-", " ").title()),
        "status": tech.get("status", "planned"),
        "difficulty": difficulty_key,
        "difficulty_label": difficulty_label,
        "duration_label": duration_label,
        "prerequisites": prerequisites,
        "path_prefix": tech.get("path_prefix", f"{tech_id}/"),
        "icon": display.get("icon", "book-open-variant"),
        "theme": display.get("theme", "devops"),
        "eyebrow": display.get("eyebrow", "Technology course"),
        "tagline": display.get("tagline", ""),
        "learning_outcomes": display.get("learning_outcomes", []),
        "build_summary": display.get(
            "build_summary",
            f"Apply {tech.get('title', tech_id)} skills in labs and projects that mirror production workflows.",
        ),
        "badges": [
            {"icon": "school-outline", "label": f"{difficulty_label} Friendly"},
            {"icon": "flask-outline", "label": "Hands-on Focused"},
            {"icon": "briefcase-check-outline", "label": "Industry Relevant"},
        ],
        "modules": modules,
        "module_count": len(modules),
        "tutorial_count": tutorial_count,
        "stats": {
            "modules": len(modules),
            "tutorials": tutorial_count,
            "labs": display.get("labs", 0),
            "quizzes": display.get("quizzes", 0),
            "projects": display.get("projects", 0),
            "capstones": display.get("capstones", 0),
            "cheatsheets": display.get("cheatsheets", 0),
            "interview": display.get("interview", 0),
            "certifications": len(cert_items),
        },
        "first_module_url": first_module_url,
        "first_tutorial_url": first_tutorial_url,
        "related_courses": related,
        "career_paths": career_paths,
        "certifications": cert_items,
    }


def _technology_from_page(page) -> str | None:
    meta_id = page.meta.get("technology_id") or page.meta.get("category")
    if meta_id and meta_id in _technology_index():
        return meta_id

    parts = Path(page.file.src_uri).parts
    if parts and parts[0] in _technology_index():
        return parts[0]

    # Standalone labs live under docs/labs/<tech>-*.md
    uri = page.file.src_uri.replace("\\", "/")
    if uri.startswith("labs/") and not uri.endswith("index.md"):
        return _technology_from_lab_slug(Path(uri).stem, page.meta)
    return None


def _technology_from_lab_slug(stem: str, meta: dict | None = None) -> str | None:
    meta = meta or {}
    tech = meta.get("technology_id")
    if tech and tech in _technology_index():
        return tech
    for tag in meta.get("tags") or []:
        if isinstance(tag, str) and tag in _technology_index():
            return tag
    if stem.startswith("cicd-"):
        return "gitlab" if "gitlab" in _technology_index() else None
    for tech_id in sorted(_technology_index().keys(), key=len, reverse=True):
        if stem == tech_id or stem.startswith(f"{tech_id}-"):
            return tech_id
    return None


def inject_lab_layout(context: dict, course: dict, labs: list[dict], lab: dict, index: int) -> None:
    """Inject standalone lab page context (docs/labs/*.md) using course navigation."""
    inject_course_layout(context, course, "labs", show_back=True)
    context["course_back_url"] = course["path_prefix"] + "labs/"
    context["course_back_label"] = "Back to Labs"
    context["course_sidebar_cta_title"] = "Learn by doing!"
    context["course_sidebar_cta_text"] = "Explore more guided labs across the Academy."
    context["course_sidebar_cta_label"] = "Browse Modules"
    context["course_start_url"] = course["path_prefix"] + "modules/"

    context["lab"] = lab
    context["lab_index"] = index + 1
    context["lab_total"] = len(labs)
    context["lab_prev"] = labs[index - 1] if index > 0 else None
    context["lab_next"] = labs[index + 1] if index + 1 < len(labs) else None


def _module_from_page(page, course: dict) -> dict | None:
    module_id = page.meta.get("module_id")
    if module_id:
        for module in course.get("modules", []):
            if module["id"] == module_id:
                return module

    match = re.search(r"modules/module-(\d+)/index\.md$", page.file.src_uri.replace("\\", "/"))
    if match:
        number = int(match.group(1))
        for module in course.get("modules", []):
            if module["number"] == number:
                return module
    return None


TECH_CATEGORY_TABS = [
    {"id": "all", "title": "All Categories"},
    {"id": "foundations", "title": "Foundations"},
    {"id": "cloud", "title": "Cloud"},
    {"id": "containers", "title": "Containers"},
    {"id": "iac", "title": "Infrastructure as Code"},
    {"id": "cicd", "title": "CI/CD"},
    {"id": "observability", "title": "Observability"},
    {"id": "security", "title": "Security"},
    {"id": "platform", "title": "Platform Engineering"},
    {"id": "architecture", "title": "Architecture"},
    {"id": "ai", "title": "Artificial Intelligence"},
]

TECH_TO_CATEGORY: dict[str, str] = {
    "linux": "foundations",
    "shell": "foundations",
    "python": "foundations",
    "networking": "foundations",
    "git": "foundations",
    "docker": "containers",
    "kubernetes": "containers",
    "helm": "containers",
    "terraform": "iac",
    "ansible": "iac",
    "aws": "cloud",
    "azure": "cloud",
    "gcp": "cloud",
    "gitlab": "cicd",
    "github-actions": "cicd",
    "jenkins": "cicd",
    "argocd": "cicd",
    "prometheus": "observability",
    "grafana": "observability",
    "loki": "observability",
    "tempo": "observability",
    "opentelemetry": "observability",
    "monitoring": "observability",
    "devsecops": "security",
    "security": "security",
    "platform-engineering": "platform",
    "sre": "platform",
    "architecture": "architecture",
    "ai": "ai",
}

POPULAR_PATHS = [
    {
        "title": "DevOps Engineer",
        "url": "career-paths/devops-engineer/",
        "icon": "infinity",
        "color": "#EA580C",
        "bg": "#FFF7ED",
        "tech_count": 12,
        "learners": "8.2K",
    },
    {
        "title": "Cloud Engineer",
        "url": "career-paths/cloud-engineer/",
        "icon": "cloud",
        "color": "#2563EB",
        "bg": "#EFF6FF",
        "tech_count": 10,
        "learners": "6.1K",
    },
    {
        "title": "Site Reliability Engineer",
        "url": "career-paths/site-reliability-engineer/",
        "icon": "cog",
        "color": "#9333EA",
        "bg": "#F3E8FF",
        "tech_count": 11,
        "learners": "4.7K",
    },
    {
        "title": "Platform Engineer",
        "url": "career-paths/platform-engineer/",
        "icon": "layers",
        "color": "#0D9488",
        "bg": "#ECFDF5",
        "tech_count": 13,
        "learners": "3.9K",
    },
    {
        "title": "Cloud Architect",
        "url": "career-paths/cloud-architect/",
        "icon": "sitemap",
        "color": "#7C3AED",
        "bg": "#EDE9FE",
        "tech_count": 14,
        "learners": "2.5K",
    },
]

POPULAR_TOPICS = [
    {
        "title": "Linux Commands",
        "desc": "Essential commands every engineer should know",
        "url": "linux/",
        "icon": "linux",
        "color": "#000000",
        "bg": "#F1F5F9",
    },
    {
        "title": "Bash Scripting",
        "desc": "Automate tasks with shell scripts",
        "url": "shell/",
        "icon": "bash",
        "color": "#4EAA25",
        "bg": "#DCFCE7",
    },
    {
        "title": "Docker Basics",
        "desc": "Container fundamentals and workflows",
        "url": "docker/",
        "icon": "docker",
        "color": "#2496ED",
        "bg": "#DBEAFE",
    },
    {
        "title": "Kubernetes Pods",
        "desc": "Deploy and manage workloads",
        "url": "kubernetes/",
        "icon": "kubernetes",
        "color": "#326CE5",
        "bg": "#DBEAFE",
    },
    {
        "title": "Terraform Modules",
        "desc": "Reusable Infrastructure as Code patterns",
        "url": "terraform/",
        "icon": "terraform",
        "color": "#7B42BC",
        "bg": "#F3E8FF",
    },
    {
        "title": "AWS EC2",
        "desc": "Launch and manage virtual machines",
        "url": "aws/",
        "icon": "aws",
        "color": "#FF9900",
        "bg": "#FFF7ED",
    },
]


def _format_difficulty(value: str) -> str:
    labels = {
        "beginner": "Beginner",
        "intermediate": "Intermediate",
        "advanced": "Advanced",
        "expert": "Expert",
    }
    return labels.get((value or "intermediate").lower(), value.title())


def _estimate_course_duration(module_count: int, tutorial_count: int) -> str:
    """Honest duration band from module/tutorial inventory."""
    if module_count >= 10:
        return f"{max(8, module_count // 2)}–{max(12, module_count)} weeks"
    if tutorial_count >= 8:
        lo = max(2, tutorial_count // 6)
        hi = max(lo + 2, tutorial_count // 3)
        return f"{lo}–{hi} weeks"
    if module_count > 0:
        return f"{max(2, module_count)}–{max(4, module_count * 2)} weeks"
    return "4–8 weeks"


def _course_skills(display: dict, modules: list[dict]) -> list[str]:
    outcomes = display.get("learning_outcomes") or []
    skills = []
    for item in outcomes:
        if isinstance(item, str) and item.strip():
            text = item.strip()
            if len(text) > 42:
                text = text[:39].rstrip() + "…"
            skills.append(text)
        if len(skills) >= 4:
            return skills
    for module in modules:
        title = (module.get("short_title") or module.get("title") or "").strip()
        if title and title not in skills:
            skills.append(title)
        if len(skills) >= 4:
            break
    return skills


def build_technology_card(tech_id: str) -> dict | None:
    tech = _technology_index().get(tech_id)
    if not tech:
        return None

    course = build_course(tech_id)
    if not course:
        return None

    display = _load_display().get(tech_id, {})
    difficulty_key = (tech.get("difficulty") or "intermediate").lower()
    tutorial_count = course.get("tutorial_count") or 0
    module_count = course.get("module_count") or 0
    stats = course.get("stats") or {}
    skills = _course_skills(display, course.get("modules") or [])
    duration = _estimate_course_duration(module_count, tutorial_count)

    return {
        "id": tech_id,
        "title": course["title"],
        "url": f"{tech_id}/",
        "icon": course["icon"],
        "summary": display.get("tagline", ""),
        "difficulty": _format_difficulty(difficulty_key),
        "difficulty_key": difficulty_key,
        "status": tech.get("status", "planned"),
        "category": TECH_TO_CATEGORY.get(tech_id, "foundations"),
        "tutorials": tutorial_count,
        "modules": module_count,
        "labs": stats.get("labs", 0),
        "projects": stats.get("projects", 0),
        "quizzes": stats.get("quizzes", 0),
        "duration": duration,
        "skills": skills,
        "popularity": tutorial_count + module_count * 2,
        "search": " ".join(
            [
                course["title"],
                display.get("tagline", ""),
                " ".join(skills),
                difficulty_key,
            ]
        ).lower(),
    }


PATH_STAGE_LADDER = [
    {"id": "beginner", "label": "Beginner"},
    {"id": "intermediate", "label": "Intermediate"},
    {"id": "advanced", "label": "Advanced"},
    {"id": "production", "label": "Production Engineer"},
    {"id": "architect", "label": "Architect"},
]


def _path_stage_index(difficulty: str, path_id: str) -> int:
    if path_id in {"cloud-architect"} or "architect" in path_id:
        return 4
    mapping = {
        "beginner": 0,
        "intermediate": 1,
        "advanced": 2,
        "expert": 3,
    }
    return mapping.get((difficulty or "intermediate").lower(), 1)


PATH_ICONS = {
    "beginner": "school",
    "linux-administrator": "linux",
    "cloud-engineer": "cloud",
    "devops-engineer": "robot",
    "kubernetes-engineer": "kubernetes",
    "platform-engineer": "server",
    "devsecops-engineer": "shield-lock",
    "site-reliability-engineer": "heart-pulse",
    "cloud-architect": "sitemap",
    "ai-for-devops": "brain",
}

FLAGSHIP_PATH_IDS = (
    "cloud-engineer",
    "devops-engineer",
    "kubernetes-engineer",
    "cloud-architect",
    "ai-for-devops",
)


def build_learning_path(path_id: str) -> dict | None:
    """Curriculum learning path with phase/course stages for path pages."""
    curriculum = _load_curriculum()
    path = next((p for p in curriculum.get("career_paths", []) if p.get("id") == path_id), None)
    if not path:
        return None

    difficulty_key = (path.get("difficulty") or "intermediate").lower()
    phases = []
    total_courses = 0
    for phase in path.get("phases") or []:
        courses = []
        for tech_id in phase.get("technologies") or []:
            tech = _technology_index().get(tech_id, {})
            display = _load_display().get(tech_id, {})
            courses.append(
                {
                    "id": tech_id,
                    "title": tech.get("title", tech_id.replace("-", " ").title()),
                    "url": f"{tech_id}/",
                    "icon": display.get("icon", "book-open-variant"),
                    "status": tech.get("status", "planned"),
                }
            )
        total_courses += len(courses)
        phases.append(
            {
                "name": phase.get("name") or "Stage",
                "courses": courses,
                "course_count": len(courses),
            }
        )

    stage_index = _path_stage_index(difficulty_key, path_id)
    stages = []
    for i, stage in enumerate(PATH_STAGE_LADDER):
        state = "done" if i < stage_index else ("current" if i == stage_index else "upcoming")
        stages.append({**stage, "state": state})

    return {
        "id": path_id,
        "title": path.get("title", path_id.replace("-", " ").title()),
        "badge": path.get("badge", ""),
        "duration": path.get("duration", ""),
        "difficulty": difficulty_key,
        "difficulty_label": _format_difficulty(difficulty_key),
        "summary": path.get("summary", ""),
        "job_roles": path.get("job_roles") or [],
        "phases": phases,
        "stages": stages,
        "stage_index": stage_index,
        "url": f"career-paths/{path_id}/",
        "certifications": path.get("certifications") or [],
        "icon": PATH_ICONS.get(path_id, "map-marker-path"),
        "course_count": total_courses,
        "phase_count": len(phases),
        "flagship": path_id in FLAGSHIP_PATH_IDS,
        "ready_count": sum(
            1 for phase in phases for course in phase["courses"] if course.get("status") == "ready"
        ),
        "planned_count": sum(
            1 for phase in phases for course in phase["courses"] if course.get("status") == "planned"
        ),
        "stub_count": sum(
            1 for phase in phases for course in phase["courses"] if course.get("status") == "stub"
        ),
    }


def _markdown_resource_index(folder: str) -> list[dict]:
    """Index leaf Markdown pages under docs/<folder>/ for course section hubs."""
    base = ROOT / "docs" / folder
    items: list[dict] = []
    if not base.is_dir():
        return items
    for path in sorted(base.glob("*.md")):
        if path.name == "index.md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        meta: dict = {}
        body = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                try:
                    meta = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    meta = {}
                body = parts[2]
        tags = meta.get("tags") or []
        tech = meta.get("technology_id") or meta.get("technology")
        category = meta.get("category")
        if not tech and category and category in _technology_index():
            tech = category
        if not tech:
            for tag in tags:
                if isinstance(tag, str) and tag in _technology_index():
                    tech = tag
                    break
        if not tech:
            tech = _technology_from_lab_slug(path.stem, meta)
        items.append(
            {
                "id": f"{folder}/{path.stem}",
                "title": meta.get("title") or path.stem.replace("-", " ").title(),
                "description": meta.get("description", ""),
                "url": f"{folder}/{path.stem}/",
                "technology": tech or "",
                "status": (meta.get("status") or "ready").lower(),
                "estimated_time": meta.get("estimated_time", ""),
                "difficulty": (meta.get("difficulty") or "").lower(),
                "words": len(re.findall(r"[A-Za-z0-9']+", body or "")),
            }
        )
    return items


COURSE_SECTION_META = {
    "projects": {
        "nav": "projects",
        "title": "Projects",
        "icon": "rocket-launch-outline",
        "catalog": "projects/",
        "catalog_label": "Academy projects catalog",
        "empty": "Projects for this track are being prepared. Complete the modules and labs first, then return for portfolio builds.",
        "folder": "projects",
    },
    "quizzes": {
        "nav": "quizzes",
        "title": "Quizzes",
        "icon": "help-circle-outline",
        "catalog": "quizzes/",
        "catalog_label": "Academy quizzes catalog",
        "empty": "Quizzes for this track are being prepared. Use module quizzes when available, or browse the academy catalog.",
        "folder": "quizzes",
    },
    "capstone": {
        "nav": "projects",
        "title": "Capstone",
        "icon": "trophy-outline",
        "catalog": "capstones/",
        "catalog_label": "Academy capstones catalog",
        "empty": "A capstone for this track is planned. Finish modules, labs, and projects first.",
        "folder": "capstones",
    },
    "cheatsheets": {
        "nav": "cheatsheets",
        "title": "Cheat Sheets",
        "icon": "file-document-outline",
        "catalog": "cheatsheets/",
        "catalog_label": "Academy cheat sheets",
        "empty": "A dedicated cheat sheet for this course is planned. Related sheets may already exist in the academy catalog.",
        "folder": "cheatsheets",
    },
    "interview": {
        "nav": "interview",
        "title": "Interview Preparation",
        "icon": "account-tie-voice",
        "catalog": "interview/",
        "catalog_label": "Academy interview prep",
        "empty": "Interview prep for this course is planned. Use module quizzes and production scenarios meanwhile.",
        "folder": "interview",
    },
    "certifications": {
        "nav": "certifications",
        "title": "Certifications",
        "icon": "certificate-outline",
        "catalog": "certifications/",
        "catalog_label": "Academy certifications",
        "empty": "Certification mapping for this course will appear here as exam guides are published.",
        "folder": None,
    },
}


def _resources_for_course(tech_id: str, section: str) -> list[dict]:
    """Published resources for a course section hub (honest inventory)."""
    meta = COURSE_SECTION_META.get(section)
    if not meta:
        return []

    if section == "certifications":
        course = build_course(tech_id)
        if not course:
            return []
        return [
            {
                "id": f"cert-{i}",
                "title": item.get("name") if isinstance(item, dict) else str(item),
                "description": "Mapped certification for this course.",
                "url": "certifications/",
                "status": "ready",
            }
            for i, item in enumerate(course.get("certifications") or [], start=1)
        ]

    if section == "quizzes":
        index = _quiz_index()
        items = []
        for i, quiz in enumerate(
            sorted(
                (q for q in index.values() if q.get("technology") == tech_id),
                key=lambda item: item.get("title", ""),
            ),
            start=1,
        ):
            items.append(
                {
                    "id": quiz["id"],
                    "number_label": f"{i:02d}",
                    "title": quiz["title"],
                    "description": quiz.get("description", ""),
                    "url": _quiz_href(quiz["id"]),
                    "status": quiz.get("status", "ready"),
                    "meta": f"{quiz.get('question_count', 0)} questions",
                }
            )
        return items

    folder = meta.get("folder")
    if not folder:
        return []

    items = []
    for i, resource in enumerate(
        [r for r in _markdown_resource_index(folder) if r.get("technology") == tech_id],
        start=1,
    ):
        items.append(
            {
                "id": resource["id"],
                "number_label": f"{i:02d}",
                "title": resource["title"],
                "description": resource.get("description", ""),
                "url": resource["url"],
                "status": resource.get("status", "ready"),
                "meta": resource.get("estimated_time") or "",
            }
        )
    return items


def _course_section_from_uri(uri: str, tech_id: str) -> str | None:
    mapping = {
        f"{tech_id}/projects/index.md": "projects",
        f"{tech_id}/quizzes/index.md": "quizzes",
        f"{tech_id}/capstone/index.md": "capstone",
        f"{tech_id}/cheatsheets/index.md": "cheatsheets",
        f"{tech_id}/interview/index.md": "interview",
        f"{tech_id}/certifications/index.md": "certifications",
        f"{tech_id}/faq.md": "faq",
    }
    return mapping.get(uri)


def build_learning_paths_page() -> dict:
    paths = []
    for item in _load_curriculum().get("career_paths", []) or []:
        built = build_learning_path(item["id"])
        if built:
            paths.append(built)
    return {
        "path_stage_ladder": PATH_STAGE_LADDER,
        "learning_paths_catalog": paths,
    }


def build_technologies_page() -> dict:
    cards = []
    for tech in _load_curriculum().get("technologies", []):
        card = build_technology_card(tech["id"])
        if card:
            cards.append(card)

    cards.sort(key=lambda item: (-item["popularity"], item["title"].lower()))

    popular_paths = []
    for path_id in FLAGSHIP_PATH_IDS:
        built = build_learning_path(path_id)
        if built:
            popular_paths.append(built)

    return {
        "tech_categories": TECH_CATEGORY_TABS,
        "tech_cards": cards,
        "tech_total": len(cards),
        "popular_paths": popular_paths,
        "popular_topics": POPULAR_TOPICS[:6],
    }


def build_course_nav(course: dict, active: str = "overview") -> list[dict]:
    prefix = course["path_prefix"]
    return [
        {"label": "Overview", "icon": "view-dashboard-outline", "path": prefix, "active": active == "overview"},
        {"label": "What You'll Learn", "icon": "lightbulb-on-outline", "path": prefix + "#learn", "active": False, "scroll": True},
        {"label": "Modules", "icon": "view-grid-outline", "path": prefix + "modules/", "active": active == "modules"},
        {"label": "Hands-on Labs", "icon": "flask-outline", "path": prefix + "labs/", "active": active == "labs"},
        {"label": "Quizzes", "icon": "help-circle-outline", "path": prefix + "quizzes/", "active": active == "quizzes"},
        {"label": "Projects", "icon": "rocket-launch-outline", "path": prefix + "projects/", "active": active == "projects"},
        {"label": "Cheat Sheets", "icon": "file-document-outline", "path": prefix + "cheatsheets/", "active": active == "cheatsheets"},
        {"label": "Interview Prep", "icon": "account-tie-voice", "path": prefix + "interview/", "active": active == "interview"},
        {"label": "Certifications", "icon": "certificate-outline", "path": prefix + "certifications/", "active": active == "certifications"},
        {"label": "Related Courses", "icon": "book-open-variant", "path": prefix + "#related", "active": False, "scroll": True},
        {"label": "FAQ", "icon": "help-circle-outline", "path": prefix + "faq/", "active": active == "faq"},
    ]


def _module_for_tutorial_page(page, course: dict) -> tuple[dict | None, dict | None]:
    """Return (module, tutorial) if the page is a tutorial inside the course."""
    uri = page.file.src_uri.replace("\\", "/")
    slug = Path(uri).stem
    for module in course.get("modules", []):
        for tutorial in module.get("tutorials", []):
            tut_id = tutorial.get("id", "")
            tut_slug = tut_id.split("/")[-1] if "/" in tut_id else tut_id
            if slug == tut_slug or uri.endswith(f"{tut_slug}.md"):
                return module, tutorial
    return None, None


def inject_course_layout(context: dict, course: dict, active: str = "overview", *, show_back: bool = False) -> None:
    start_path = course["path_prefix"] + (course["first_module_url"] or "roadmap/")
    context["course"] = course
    context["c"] = course
    context["course_nav"] = build_course_nav(course, active)
    context["course_start_url"] = start_path
    context["course_start_label"] = "Start Learning" if show_back else ("Start Here" if course["first_module_url"] else "View Roadmap")
    context["course_show_back"] = show_back
    if show_back:
        context["course_sidebar_cta_title"] = f"Ready to start your {course['title']} journey?"
        context["course_sidebar_cta_text"] = "Begin with the first module and build skills step by step."
        context["course_sidebar_cta_label"] = "Start Learning"
    else:
        context["course_sidebar_cta_title"] = f"New to {course['title']}?"
        context["course_sidebar_cta_text"] = "Start with the first module and build skills step by step."
        context["course_sidebar_cta_label"] = context["course_start_label"]


def _site_origin(config) -> str:
    url = (config.get("site_url") or "https://rebash.in/").rstrip("/") + "/"
    return url


def _absolute_url(config, path: str) -> str:
    origin = _site_origin(config).rstrip("/")
    if not path:
        return origin + "/"
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return origin + "/" + path.lstrip("/")


def _breadcrumb_list(page, config) -> dict:
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": _site_origin(config),
        }
    ]
    uri = page.file.src_uri.replace("\\", "/")
    parts = Path(uri).parts
    position = 2
    cumulative = []
    for part in parts:
        cumulative.append(part)
        name = part.replace(".md", "").replace("-", " ").replace("index", "").strip() or "Overview"
        if part == "index.md":
            continue
        if part.endswith(".md"):
            href = "/".join(cumulative)[:-3]  # drop .md via stem handling
            href = str(Path(*cumulative).with_suffix("")).replace("\\", "/") + "/"
            if href.endswith("index/"):
                href = href[: -len("index/")]
        else:
            href = "/".join(cumulative) + "/"
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": name.title() if name != "Overview" else page.title,
                "item": _absolute_url(config, href),
            }
        )
        position += 1
    # Prefer page title on the last crumb
    if len(items) > 1:
        items[-1]["name"] = page.title
        items[-1]["item"] = page.canonical_url or items[-1]["item"]
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def _inject_seo(context: dict, page, config) -> None:
    """Attach robots, social image, and JSON-LD payloads for templates."""
    meta = page.meta or {}
    description = meta.get("description") or config.get("site_description") or ""
    title = page.title or config.get("site_name") or "REBASH Academy"
    origin = _site_origin(config)
    og_image = _absolute_url(config, "assets/images/og-default.png")
    if meta.get("image"):
        og_image = _absolute_url(config, str(meta["image"]))

    status = str(meta.get("status") or "").lower()
    tutorial_count = meta.get("tutorial_count")
    try:
        tutorial_count_int = int(tutorial_count) if tutorial_count is not None else None
    except (TypeError, ValueError):
        tutorial_count_int = None

    robots = meta.get("robots")
    if not robots and status == "planned" and tutorial_count_int == 0:
        robots = "noindex, follow"
    course = context.get("course")
    if not robots and course and course.get("status") == "planned" and not course.get("tutorial_count"):
        robots = "noindex, follow"

    context["seo_robots"] = robots or "index, follow"
    context["seo_og_image"] = og_image
    context["seo_description"] = description

    graphs = [_breadcrumb_list(page, config)]
    provider = {
        "@type": "Organization",
        "name": "REBASH Academy",
        "url": origin,
        "logo": _absolute_url(config, "assets/images/logo.svg"),
    }

    template = meta.get("template", "")
    uri = page.file.src_uri.replace("\\", "/")

    if uri in {"index.md", ""} or template == "home.html":
        graphs.append(
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": "REBASH Academy",
                "url": origin,
                "description": config.get("site_description") or description,
                "publisher": provider,
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": origin + "?q={search_term_string}",
                    "query-input": "required name=search_term_string",
                },
            }
        )

    if course and template in {"course.html", "modules.html", "course-labs.html"}:
        graphs.append(
            {
                "@context": "https://schema.org",
                "@type": "Course",
                "name": course.get("title") or title,
                "description": course.get("tagline") or description,
                "provider": provider,
                "url": page.canonical_url or _absolute_url(config, course.get("path_prefix", "")),
                "educationalLevel": course.get("difficulty_label") or meta.get("difficulty"),
                "timeRequired": course.get("duration_label"),
                "image": og_image,
                "hasCourseInstance": {
                    "@type": "CourseInstance",
                    "courseMode": "online",
                    "courseWorkload": course.get("duration_label"),
                },
            }
        )

    if context.get("lesson") and template in {"lesson.html", ""}:
        graphs.append(
            {
                "@context": "https://schema.org",
                "@type": "LearningResource",
                "name": title,
                "description": description,
                "url": page.canonical_url,
                "learningResourceType": "Tutorial",
                "educationalLevel": meta.get("difficulty"),
                "timeRequired": meta.get("estimated_time"),
                "isPartOf": {
                    "@type": "Course",
                    "name": course.get("title") if course else None,
                    "url": _absolute_url(config, course.get("path_prefix", "")) if course else None,
                },
                "provider": provider,
                "image": og_image,
            }
        )

    learning_path = context.get("learning_path")
    if learning_path and template == "learning-path.html":
        graphs.append(
            {
                "@context": "https://schema.org",
                "@type": "Course",
                "name": learning_path.get("title") or title,
                "description": learning_path.get("summary") or description,
                "provider": provider,
                "url": page.canonical_url,
                "educationalLevel": learning_path.get("difficulty_label"),
                "timeRequired": learning_path.get("duration"),
                "image": og_image,
            }
        )

    context["seo_json_ld"] = json.dumps(graphs, ensure_ascii=False, indent=None)


def on_page_context(context, page, config, nav):
    try:
        return _on_page_context_body(context, page, config, nav)
    finally:
        _inject_seo(context, page, config)


def _on_page_context_body(context, page, config, nav):
    template = page.meta.get("template", "")
    uri = page.file.src_uri.replace("\\", "/")

    if template in {"home.html", "hub.html", "career-paths.html", "technologies.html", "labs.html", "learning-path.html"}:
        context["catalog"] = build_catalog_stats()

    if template == "technologies.html":
        context.update(build_technologies_page())
        return context

    if template == "career-paths.html":
        context.update(build_learning_paths_page())
        return context

    if template == "learning-path.html" or (
        uri.startswith("career-paths/") and uri.endswith("index.md") and uri.count("/") >= 2
    ):
        path_id = Path(uri).parts[1] if len(Path(uri).parts) > 1 else ""
        learning_path = build_learning_path(path_id)
        if learning_path:
            context["learning_path"] = learning_path
            context["path_stage_ladder"] = PATH_STAGE_LADDER
        if template == "learning-path.html":
            return context

    if template in {"home.html", "hub.html"}:
        return context

    tech_id = _technology_from_page(page)

    if not tech_id:
        return context

    course = build_course(tech_id)
    if not course:
        return context

    if template == "course.html":
        inject_course_layout(context, course, "overview")
        return context

    if template == "modules.html":
        inject_course_layout(context, course, "modules", show_back=False)
        context["modules_per_page"] = 12
        return context

    if template == "course-labs.html":
        labs = _labs_for_course(tech_id)
        inject_course_layout(context, course, "labs", show_back=False)
        context["course_labs"] = labs
        context["course_labs_count"] = len(labs)
        context["course_labs_total_time"] = _labs_total_time_label(labs)
        context["course_sidebar_cta_title"] = "Learn by doing!"
        context["course_sidebar_cta_text"] = "Start a lab, validate your work, then return to the modules."
        context["course_sidebar_cta_label"] = "Browse Modules"
        context["course_start_url"] = course["path_prefix"] + "modules/"
        return context

    if template == "course-section.html":
        section = page.meta.get("section") or _course_section_from_uri(uri, tech_id) or "projects"
        section_meta = COURSE_SECTION_META.get(section, COURSE_SECTION_META["projects"])
        items = _resources_for_course(tech_id, section)
        inject_course_layout(context, course, section_meta["nav"], show_back=True)
        context["course_section"] = section
        context["course_section_meta"] = section_meta
        context["course_section_items"] = items
        context["course_section_count"] = len(items)
        context["course_sidebar_cta_title"] = f"Continue {course['title']}"
        context["course_sidebar_cta_text"] = "Return to modules when you finish this section."
        context["course_sidebar_cta_label"] = "Browse Modules"
        context["course_start_url"] = course["path_prefix"] + "modules/"
        return context

    if template == "course-faq.html":
        inject_course_layout(context, course, "faq", show_back=True)
        context["course_sidebar_cta_title"] = f"Start {course['title']}"
        context["course_sidebar_cta_text"] = "Open the first module when you are ready."
        context["course_sidebar_cta_label"] = "Browse Modules"
        context["course_start_url"] = course["path_prefix"] + "modules/"
        return context

    if template == "lab.html":
        labs = _labs_for_course(tech_id)
        uri = page.file.src_uri.replace("\\", "/")
        stem = Path(uri).stem
        lab_id = f"labs/{stem}"
        index = next((i for i, item in enumerate(labs) if item["id"] == lab_id), -1)
        if index < 0:
            # Lab exists on disk but was not indexed under this tech prefix — synthesise entry
            meta = _lab_index().get(lab_id, {})
            title = meta.get("title", stem.replace("-", " ").title())
            title = re.sub(r"^Lab\s*[—–-]\s*", "", title).strip()
            lab = {
                "id": lab_id,
                "number_label": "01",
                "title": title,
                "description": meta.get("description", page.meta.get("description", "")),
                "estimated_time": meta.get("estimated_time") or page.meta.get("estimated_time") or "30–40 min",
                "url": _lab_href(lab_id),
                "icon": "flask-outline",
                "status": meta.get("status", "ready"),
            }
            labs = [lab]
            index = 0
        inject_lab_layout(context, course, labs, labs[index], index)
        return context

    if template == "module.html" or page.meta.get("module_id"):
        inject_course_layout(context, course, "modules", show_back=False)
        module = _module_from_page(page, course)
        if module:
            context["module"] = module
            context["course_active_module"] = module["number"]
            context["course_active_lesson"] = "overview"
            context["module_nav"] = build_module_nav("overview")
            context["module_start_url"] = module.get("first_tutorial_url") or course["first_module_url"]
            context["module_sidebar_cta_title"] = "Start your journey!"
            context["module_sidebar_cta_text"] = "Begin with the first lesson in this module."
            context["module_sidebar_cta_label"] = "Start Learning"
            context["module_show_back"] = True
        return context

    if template == "lesson.html":
        mod, tutorial = _module_for_tutorial_page(page, course)
        if mod and tutorial:
            inject_lesson_layout(context, course, mod, tutorial)
        return context

    mod, tutorial = _module_for_tutorial_page(page, course)
    if mod and tutorial:
        inject_lesson_layout(context, course, mod, tutorial)

    return context


def on_page_markdown(markdown, page, config, files):
    """Assign lesson template after frontmatter is loaded (on_pre_page runs before read_source)."""
    uri = page.file.src_uri.replace("\\", "/")

    # Standalone lab detail pages (docs/labs/*.md)
    if (
        uri.startswith("labs/")
        and uri.endswith(".md")
        and not uri.endswith("index.md")
        and not page.meta.get("template")
    ):
        page.meta["template"] = "lab.html"
        hide = list(page.meta.get("hide") or [])
        for item in ("navigation", "toc", "path", "footer"):
            if item not in hide:
                hide.append(item)
        page.meta["hide"] = hide
        return markdown

    tech_id = _technology_from_page(page)

    # Course labs hub — Hands-on Labs page linked from the course landing
    if tech_id and uri == f"{tech_id}/labs/index.md" and not page.meta.get("template"):
        page.meta["template"] = "course-labs.html"
        return markdown

    # Course section hubs — projects, quizzes, capstone, cheatsheets, interview, certifications
    section = _course_section_from_uri(uri, tech_id) if tech_id else None
    if tech_id and section == "faq" and not page.meta.get("template"):
        page.meta["template"] = "course-faq.html"
        return markdown
    if tech_id and section and section != "faq" and not page.meta.get("template"):
        page.meta["template"] = "course-section.html"
        page.meta["section"] = section
        return markdown

    # Thin planned course shells — keep crawlable paths but avoid ranking empty stubs
    status = str(page.meta.get("status") or "").lower()
    try:
        tutorial_count = int(page.meta.get("tutorial_count")) if page.meta.get("tutorial_count") is not None else None
    except (TypeError, ValueError):
        tutorial_count = None
    if (
        status in {"planned", "stub"}
        and (tutorial_count == 0 or tutorial_count is None)
        and not page.meta.get("robots")
    ):
        page.meta["robots"] = "noindex, follow"
        search_meta = page.meta.get("search")
        if not isinstance(search_meta, dict):
            search_meta = {}
        search_meta["exclude"] = True
        page.meta["search"] = search_meta

    if page.meta.get("template"):
        return markdown

    if not tech_id:
        return markdown

    if any(
        marker in uri
        for marker in (
            "/modules/",
            "/labs/",
            "/quizzes/",
            "/projects/",
            "/capstone/",
            "/cheatsheets/",
            "/interview/",
            "/certifications/",
            "/roadmap",
            "/faq",
        )
    ):
        return markdown
    if uri.endswith("index.md"):
        return markdown

    course = build_course(tech_id)
    if not course:
        return markdown

    mod, tutorial = _module_for_tutorial_page(page, course)
    if mod and tutorial:
        page.meta["template"] = "lesson.html"
        hide = list(page.meta.get("hide") or [])
        for item in ("navigation", "toc", "path", "footer"):
            if item not in hide:
                hide.append(item)
        page.meta["hide"] = hide

    return markdown
