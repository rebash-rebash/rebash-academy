---
title: Blog frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy engineering journal article.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Blog frontmatter schema

Every article under `docs/blog/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Human-readable article title"
description: "One or two sentences for SEO, RSS, and social previews."
author: Shaik Basha
date: "2026-07-29"
updated: "2026-07-29"
category: engineering              # primary nav category — see categories below
type: engineering-insights         # article type — see types below
difficulty: intermediate           # beginner | intermediate | advanced | expert
estimated_reading_time: "8 min"
learning_paths:
  - devops-engineer
technologies:
  - kubernetes
  - terraform
skills:
  - platform-design
series: null                       # e.g. kubernetes-deep-dive — or series slug
series_part: null                  # 1, 2, 3 … when part of a series
tags:
  - kubernetes
  - gitops
  - platform-engineering
related_tutorials:
  - kubernetes/kubectl-essentials-and-workflows
related_labs:
  - labs/kubernetes-deployment-triage
related_projects:
  - projects/status-api-portfolio
related_cheatsheets:
  - cheatsheets/kubernetes
related_certifications:
  - CKA
featured: false                    # true for homepage / featured section promotion
comments: false
---
```

## Body template

Every article follows this structure:

1. **Summary** — lead paragraph: what the reader will learn or decide
2. **Table of contents** — for articles over ~600 words
3. **Body** — sections with clear H2/H3 hierarchy
4. **Key takeaways** — bullet list of actionable points
5. **Related tutorials** — deep-dive links into Academy tracks
6. **Related labs** — hands-on follow-ups
7. **Related projects** — portfolio builds that apply the topic
8. **Related cheat sheets** — quick reference
9. **Related learning paths** — when role context matters
10. **References** — official documentation and primary sources first

Blog articles **complement** tutorials. They may discuss opinions, trends, incidents, and trade-offs — they do not replace structured tutorial content.

## Article categories

Primary `category` values map to nav groups under `docs/blog/`:

| Category | `category` | Topics |
|----------|------------|--------|
| Engineering | `engineering` | General engineering, Linux, Python, Git, networking |
| Cloud | `cloud` | AWS, Azure, GCP, multi-cloud |
| DevOps | `devops` | Delivery culture, pipelines, automation |
| Containers | `containers` | Docker, Kubernetes, Helm |
| Infrastructure | `infrastructure` | Terraform, Ansible, OpenTofu |
| Security | `security` | DevSecOps, compliance, threat modelling |
| Observability | `observability` | Metrics, logs, traces, SRE |
| Architecture | `architecture` | System design, landing zones, HA, DR |
| AI | `ai` | AI for DevOps, practical ML workflows |
| Career | `career` | Career advice, interviews, certifications |
| Community | `community` | Contributors, events, open source |
| Release notes | `release-notes` | Site updates, new tutorials, changelog |

Subfolders mirror categories as the catalogue grows, e.g. `docs/blog/containers/kubernetes/`.

## Article types

| Type | `type` | When to use |
|------|--------|-------------|
| Engineering insights | `engineering-insights` | Technical deep dives and analysis |
| Opinion | `opinion` | Engineering opinions with reasoned trade-offs |
| Architecture discussion | `architecture-discussion` | Design decisions and alternatives |
| Best practices | `best-practices` | Production patterns and anti-patterns |
| Lessons learned | `lessons-learned` | Post-project or post-incident reflection |
| Case study | `case-study` | Real-world implementation narrative |
| Migration story | `migration-story` | Platform or cloud migration chronicle |
| Incident analysis | `incident-analysis` | Outage or incident walkthrough (sanitised) |
| Performance investigation | `performance-investigation` | Tuning and bottleneck analysis |
| Security analysis | `security-analysis` | Threat, vuln, or hardening review |
| Release notes | `release-notes` | Academy or product release summary |
| Community update | `community-update` | Community news and highlights |
| Roadmap update | `roadmap-update` | Content and product direction |
| Conference summary | `conference-summary` | Event takeaways |
| Book review | `book-review` | Technical book notes |
| Tool review | `tool-review` | Honest tool comparison |
| Career advice | `career-advice` | Role and growth guidance |
| AI research summary | `ai-research-summary` | Practical AI developments for ops |

## Tagging strategy

Use `tags` for cross-cutting discovery beyond `category`:

| Tag family | Examples |
|------------|----------|
| Technology | `kubernetes`, `terraform`, `aws`, `docker`, `linux`, `python` |
| Practice | `gitops`, `monitoring`, `security`, `platform-engineering`, `sre`, `devsecops` |
| Audience | `career`, `certification`, `beginner-friendly` |
| Theme | `ai`, `cost-optimisation`, `incident-response`, `migration` |

Keep tags lowercase, hyphenated, and consistent with curriculum technology ids where applicable.

## Related content model

Every article links outward to Academy assets readers should use next:

| Relation | Frontmatter field | Purpose |
|----------|-------------------|---------|
| Tutorials | `related_tutorials` | Structured learning |
| Labs | `related_labs` | Hands-on proof |
| Projects | `related_projects` | Portfolio application |
| Cheat sheets | `related_cheatsheets` | Command recall |
| Learning paths | `learning_paths` | Role context |
| Certifications | `related_certifications` | Exam alignment |

Reverse links: tutorials may reference blog articles in body when an article provides context (optional future field).

## Article series

Multi-part articles share a `series` slug:

| Series slug | Theme |
|-------------|-------|
| `kubernetes-deep-dive` | Kubernetes internals and operations |
| `terraform-best-practices` | IaC patterns and module design |
| `aws-architecture` | AWS design decisions |
| `linux-internals` | Linux for operators |
| `devops-journey` | Career and skill progression |
| `platform-engineering` | IDP and golden paths |
| `sre-fundamentals` | Reliability engineering |
| `ai-for-devops` | Practical AI in operations |

Series index pages live at `docs/blog/series/<slug>/index.md` when a series has three or more parts.

## Featured sections (landing page)

The blog landing template (`blog.html`) supports:

| Section | Source |
|---------|--------|
| Featured articles | `featured: true` in frontmatter |
| Latest articles | Sort by `date` descending |
| Browse by category | Filterable category cards |
| Editor's picks | Curated in template until CMS automation |

## Content guidelines

Articles should:

- **Teach, inform, or analyse** — not chase clicks
- **Use practical examples** — commands, diagrams, and real constraints
- **Discuss trade-offs** — no single-vendor cheerleading without reasoning
- **Reference official documentation** — primary sources first
- **Use British English** — per REBASH Academy style guide
- **Avoid clickbait and sensational titles** — precise, professional headlines

Do not duplicate tutorial content verbatim; link to the tutorial instead.

## Repository layout

```
docs/blog/
  index.md                      # landing (blog.html)
  engineering/
  cloud/
  containers/
  infrastructure/
  security/
  observability/
  architecture/
  ai/
  career/
  community/
  release-notes/
  series/                       # multi-part series indexes
```

Each category folder contains an `index.md` listing articles in that category. Flat slugs at `docs/blog/<slug>.md` are acceptable for early articles.

## Navigation structure

```
Blog (Engineering Journal)
  Overview
  Latest (auto or manual pin)
  Engineering
  Cloud
  Containers
  Infrastructure
  Security
  Observability
  Architecture
  AI
  Career
  Community
  Release Notes
```

Update `docs/blog/.pages` as category folders and articles ship.

## RSS and SEO

- `description` powers meta tags and future RSS summaries
- `date` / `updated` support freshness signals
- One H1 per article (title); logical heading hierarchy below
- Canonical tutorial links use site-root paths
