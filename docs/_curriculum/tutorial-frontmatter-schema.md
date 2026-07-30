---
title: Tutorial frontmatter schema
description: Required YAML frontmatter for every REBASH Academy tutorial.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Tutorial frontmatter schema

Every tutorial under `docs/<technology>/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Human-readable title"
description: "One or two sentences for SEO and search."
difficulty: beginner          # beginner | intermediate | advanced | expert
estimated_time: "45–90 min"
technology: linux             # curriculum technology id
module: "Module 1 · Fundamentals"
career_paths:
  - devops-engineer
  - linux-administrator
skills:
  - linux-fundamentals
prerequisites:
  - linux/some-earlier-tutorial
next:
  - linux/next-tutorial
related:
  - networking/introduction-to-networking
labs:
  - labs/linux-production-incident-triage
projects:
  - projects/status-api-portfolio
interview: interview/linux
certifications:
  - RHCSA
tags:
  - linux
  - devops
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Rules

- `technology` and `career_paths` must match ids in `curriculum.yaml`.
- Prefer stable slug paths (`technology/slug`) for `prerequisites`, `next`, and `related`.
- Do not invent certifications not listed in the curriculum certification mapping.
- Navigation (previous / next) can later be generated from `curriculum.yaml` without duplicating tutorials.
