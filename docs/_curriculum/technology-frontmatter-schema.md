---
title: Technology page schema
description: Reusable metadata for every REBASH Academy technology index page.
---

# Technology page schema

Every technology lives at `docs/<technology-id>/index.md`. URLs are stable — do not move tracks under `docs/technologies/`.

Align values with [`curriculum.yaml`](../../curriculum.yaml).

## Technology index frontmatter

```yaml
---
title: "Linux"
description: "One or two sentences for SEO — production-focused scope of the track."
technology_id: linux
category: foundations          # foundations | containers | iac | cloud | cicd | observability | security | platform | reliability | architecture | ai
difficulty: beginner             # beginner | intermediate | advanced | expert
estimated_duration: "8–10 weeks"
status: ready                    # ready | planned | stub
career_paths:
  - devops-engineer
  - linux-administrator
modules: []                      # optional inline; canonical list in curriculum.yaml
tutorial_count: 25
labs: []
quizzes: []
projects: []
capstones: []
cheatsheets: []
interview_guides: []
certifications:
  - RHCSA
skills:
  - linux-fundamentals
  - systemd
tags:
  - linux
  - devops
author: Shaik Basha
last_updated: "2026-07-29"
---
```

## Required page sections

Every technology index should include these headings (ready tracks fill them in; planned/stub tracks keep the outline):

1. **Overview** — why the technology matters in production
2. **Learning objectives** — measurable outcomes
3. **Who should learn** — roles and intent
4. **Prerequisites** — prior tracks or tutorials
5. **Difficulty & duration**
6. **Modules** — ordered course structure
7. **Tutorial roadmap** — links to published lessons
8. **Hands-on labs**
9. **Quizzes**
10. **Projects**
11. **Capstones**
12. **Cheat sheets**
13. **Interview preparation**
14. **Certification mapping**
15. **Related technologies**
16. **Related career paths**
17. **References** — official documentation first

## Module template

Each module in `curriculum.yaml` should define:

| Field | Purpose |
|-------|---------|
| `id` | Stable module id (`linux-m1`) |
| `title` | Display name |
| `tutorials` | Ordered tutorial ids under `docs/` |
| `learning_objectives` | Optional bullet list |
| `lab` | Optional lab id |
| `quiz` | Optional quiz id |
| `mini_project` | Optional project id |

## Learning progression

```text
Overview → Module → Tutorial → Quiz → Lab → Mini project → Enterprise project → Capstone → Interview → Certification
```

## Skill matrix (example)

Document key skills per technology in the index or a linked cheatsheet — e.g. Linux: filesystem, permissions, systemd, networking; Docker: images, containers, volumes, Compose.

## Related content links

Link to sibling sections without duplicating tutorials:

- [Labs](../labs/index.md)
- [Quizzes](../quizzes/index.md)
- [Projects](../projects/index.md)
- [Capstones](../capstones/index.md)
- [Cheat sheets](../cheatsheets/index.md)
- [Interview guides](../interview/index.md)
- [Certifications](../certifications/index.md)
- [Career paths](../career-paths/index.md)
- [Technologies overview](../technologies/index.md)

## Visual catalog

The public browse experience lives at [Technologies overview](../technologies/index.md) (`template: technologies.html`). Individual tracks open from category cards there.
