---
title: Course homepage schema
description: Reusable metadata and repository layout for every REBASH Academy technology course.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Course homepage schema

Every technology track is a **standalone online course** — not a flat documentation index. The course homepage uses `template: course.html`; tutorials appear only after entering a module.

Align module structure with [`curriculum.yaml`](../../curriculum.yaml). Display metadata (icons, related courses, catalog counts) lives in [`course-display.yaml`](course-display.yaml).

## Repository layout

```text
docs/<technology-id>/
├── index.md              # Course homepage (template: course.html)
├── roadmap.md            # Learning roadmap
├── faq.md                # Course FAQ
├── .pages                # Course sidebar (no flat tutorial list)
├── modules/
│   ├── module-01/
│   │   └── index.md      # Module landing (template: module.html)
│   └── module-02/
│       └── index.md
├── labs/index.md
├── quizzes/index.md
├── projects/index.md
├── capstone/index.md
├── cheatsheets/index.md
├── interview/index.md
└── certifications/index.md
```

Tutorial files stay at `docs/<technology-id>/<tutorial-slug>.md` — **do not move** published URLs.

Regenerate navigation after curriculum changes:

```bash
uv run python scripts/generate-course-structure.py
```

## Course homepage frontmatter

```yaml
---
title: Overview
description: "One or two sentences for SEO and the course hero."
template: course.html
technology_id: linux
difficulty: beginner
estimated_duration: "8–10 weeks"
status: ready
category: linux
tutorial_count: 25
target_roles:
  - DevOps Engineer
  - Linux Administrator
prerequisites:
  - Basic computer literacy
tags:
  - linux
  - course
comments: false
hide:
  - toc
---
```

## Module page frontmatter

```yaml
---
title: "Module 1 · Fundamentals"
description: "Module overview for the Linux course."
template: module.html
technology_id: linux
module_id: linux-m1
hide:
  - toc
---
```

## Sidebar navigation

The course sidebar exposes:

1. Overview
2. Roadmap
3. Modules (nested — tutorials appear under each module)
4. Labs
5. Quizzes
6. Projects
7. Capstone
8. Cheat Sheets
9. Interview Preparation
10. Certifications
11. FAQ

Do **not** list every tutorial at the top level of the course nav.

## Templates and hooks

| Asset | Purpose |
|-------|---------|
| `overrides/course.html` | Course homepage layout |
| `overrides/module.html` | Module landing layout |
| `hooks/course_context.py` | Injects `course` and `module` from `curriculum.yaml` |
| `docs/assets/d2/course-navigation.d2` | Learning flow diagram |
| `docs/assets/images/course-navigation.svg` | Rendered diagram |

## D2 diagram

Store the course navigation flow at `docs/assets/d2/course-navigation.d2` and render to `docs/assets/images/course-navigation.svg`.

## Related schemas

- [`technology-frontmatter-schema.md`](technology-frontmatter-schema.md) — legacy technology index fields
- [`tutorial-frontmatter-schema.md`](tutorial-frontmatter-schema.md) — individual lessons
