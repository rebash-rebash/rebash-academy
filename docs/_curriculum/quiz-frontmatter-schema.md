---
title: Quiz frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy quiz.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Quiz frontmatter schema

Every quiz under `docs/quizzes/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Quiz — Human-readable title"
description: "One or two sentences for SEO and search."
difficulty: intermediate          # beginner | intermediate | advanced | expert
estimated_time: "45–60 min"
quiz_type: course                 # lesson | module | course | technology | career-path | certification
technology: linux                 # curriculum technology id
module: "Module 1 · Fundamentals"
question_count: 40
passing_score: "70% (28/40)"
career_paths:
  - devops-engineer
  - linux-administrator
skills:
  - linux-fundamentals
prerequisites:
  - linux/linux-filesystem-hierarchy
related_tutorials:
  - linux/introduction-to-linux
related_labs:
  - labs/linux-production-incident-triage
related_projects:
  - projects/status-api-portfolio
certifications:
  - RHCSA
tags:
  - quizzes
  - linux
  - assessment
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every quiz page follows this structure:

1. **Quiz overview** — topic, question count, pass mark, format, estimated time
2. **Learning objectives**
3. **Prerequisites** — tutorials to complete first
4. **Instructions** — answer before revealing; self-mark honestly
5. **Questions** — numbered, with options and reveal blocks
6. **Scoring guide** — pass threshold and what to do if below
7. **Recommended study areas** — weak-topic remediation links
8. **Related resources** — tutorials, labs, cheat sheets, interview prep

## Question metadata

Each question should support (inline or in a future structured format):

| Field | Purpose |
|-------|---------|
| `question_id` | Stable id, e.g. `linux-fundamentals-q12` |
| `quiz_id` | Parent quiz slug |
| `technology` | Curriculum technology id |
| `module` | Module the question belongs to |
| `difficulty` | beginner · intermediate · advanced · expert |
| `question_type` | multiple-choice · multiple-select · true-false · scenario · troubleshooting |
| `skills` | Skill tags tested |
| `career_paths` | Paths this question supports |
| `certification_mapping` | Exam domains where applicable |
| `tags` | Free-form tags |

## Question structure

Every question includes:

- **Question** text
- **Options** (where applicable)
- **Correct answer**
- **Explanation** — why the answer is correct
- **Official reference** — link to docs where helpful
- **Related tutorial** — deep link for remediation
- **Related lab** — optional hands-on follow-up

## Quiz levels

| Level | Name | When to use |
|-------|------|-------------|
| 1 | Knowledge check | Simple understanding after a lesson |
| 2 | Concept validation | Scenario-based concepts after a module |
| 3 | Engineering assessment | Production-focused course quizzes |
| 4 | Expert challenge | Architecture and troubleshooting finals |

Map levels via `difficulty` and `quiz_type` — lesson/module quizzes tend toward levels 1–2; course and certification readiness toward 3–4.

## Assessment types

| Type | Scope |
|------|--------|
| `lesson` | Single tutorial recap |
| `module` | End-of-module check (e.g. 25 questions) |
| `course` | Full track fundamentals (e.g. 40 questions) |
| `technology` | Cross-module technology assessment |
| `career-path` | Multi-technology path check |
| `certification` | Exam-domain readiness |

## Certification mapping

Declare `certifications` in quiz frontmatter where relevant. Supported mappings include RHCSA, RHCE, CKA, CKAD, CKS, Terraform Associate, AWS SAA, AWS DevOps Engineer Professional, AZ-104, AZ-305, Google Associate Cloud Engineer, Google Professional Cloud Architect, Google Professional Cloud DevOps Engineer, and Prometheus Certified Associate.

See [`certification_mapping.md`](certification_mapping.md) for track-level coverage.

## Learning progression

```
Tutorial → Knowledge quiz → Lab → Practice quiz → Project → Final assessment → Capstone
```

## Navigation

- Public browse experience: [Quizzes overview](../quizzes/index.md) (`template: quizzes.html`)
- Individual quizzes stay at `docs/quizzes/<slug>.md` — do not move URLs when adding categories
- Sidebar structure: `docs/quizzes/.pages`

## Repository scale path

Future growth can add technology subfolders without breaking URLs:

```
docs/quizzes/
  index.md
  .pages
  linux/
    lesson/
    module/
    course/
    final/
```

Until subfolders exist, flat slugs remain the canonical pattern.

## Pass marks

- **40-question** course quizzes: **70% (28 correct)**
- **25-question** module quizzes: **70% (18 correct)**

State the pass mark in frontmatter and in the quiz overview table.
