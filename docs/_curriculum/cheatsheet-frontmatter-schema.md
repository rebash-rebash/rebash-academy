---
title: Cheat sheet frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy cheat sheet.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Cheat sheet frontmatter schema

Every cheat sheet under `docs/cheatsheets/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Cheat Sheet — Human-readable title"
description: "One or two sentences for SEO and search."
technology: linux                 # curriculum technology id
category: command-reference         # see types below
difficulty: beginner                # beginner | intermediate | advanced
estimated_time: "15 min"
learning_paths:
  - devops-engineer
  - linux-administrator
skills:
  - linux-fundamentals
prerequisites:
  - linux/introduction-to-linux
related_tutorials:
  - linux/linux-essential-commands
related_labs:
  - labs/linux-install-and-first-boot
related_projects:
  - projects/linux-system-information-utility
certifications:
  - RHCSA
tags:
  - cheatsheets
  - linux
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every cheat sheet page follows this structure:

1. **Quick overview** — one paragraph on scope and when to use this sheet
2. **Table of contents** — anchor links to sections below
3. **Essential commands** — scannable tables or grouped lists
4. **Common syntax** — flags, patterns, and config snippets
5. **Examples** — copy-paste ready, minimal commentary
6. **Common workflows** — task-oriented sequences (deploy, triage, rollback)
7. **Best practices** — production-focused do's and don'ts
8. **Security tips** — least privilege, secrets, hardening
9. **Performance tips** — when relevant to the technology
10. **Troubleshooting** — symptom → command → fix tables
11. **Common mistakes** — pitfalls learners hit in labs and on the job
12. **Useful links** — related tutorials, labs, and projects on REBASH Academy
13. **Official references** — upstream docs first

Cheat sheets are **not tutorials**. Keep prose minimal; favour tables, lists, and code blocks.

## Cheat sheet types

| Type | `category` | When to use |
|------|------------|-------------|
| Command reference | `command-reference` | CLI commands grouped by task |
| CLI reference | `cli-reference` | Full tool flag and subcommand index |
| Syntax guide | `syntax-guide` | Language or config syntax patterns |
| Configuration reference | `configuration-reference` | Config file keys and values |
| Architecture reference | `architecture-reference` | Component diagrams and terminology |
| Troubleshooting guide | `troubleshooting` | Symptom-led diagnostic flows |
| Best practices | `best-practices` | Production checklists and patterns |
| Keyboard shortcuts | `keyboard-shortcuts` | IDE, terminal, or tool shortcuts |
| Quick start guide | `quick-start` | Minimum steps to get running |
| Production checklist | `production-checklist` | Pre-deploy and go-live gates |
| Decision matrix | `decision-matrix` | When to choose A vs B |
| Comparison guide | `comparison-guide` | Tool or approach comparisons |

## Organisation per technology

Each technology should eventually include multiple focused sheets. Example roadmap:

| Technology | Planned sheets |
|------------|----------------|
| Linux | Commands, filesystem, permissions, networking, systemd, storage, users, troubleshooting |
| Docker | CLI, Dockerfile, Compose, networking, volumes, images, containers |
| Kubernetes | kubectl, YAML, pods, deployments, services, ingress, RBAC, storage, troubleshooting |
| Terraform | CLI, providers, variables, modules, state, outputs, functions |
| AWS | CLI, IAM, EC2, S3, networking, monitoring, security |

Publish one consolidated sheet per technology first; split into topic sheets as the catalogue grows under `docs/cheatsheets/<technology>/`.

## Learning flow

Cheat sheets reinforce learning between tutorials and hands-on practice:

| Stage | Role of cheat sheets |
|-------|----------------------|
| After tutorial | Quick recall before starting a lab |
| During lab | Command lookup without leaving the exercise |
| During project | Syntax and workflow reference on the job |
| Interview prep | Scannable revision alongside quizzes |
| Production | Day-two reference at the keyboard |

See [`cheatsheet-learning-flow.d2`](../assets/d2/cheatsheet-learning-flow.d2) for the visual progression.

## Learning path mapping

Every cheat sheet declares one or more `learning_paths` ids. Examples:

| Cheat sheet | Typical paths |
|-------------|---------------|
| Linux | `linux-administrator`, `devops-engineer`, `beginner` |
| kubectl | `devops-engineer`, `kubernetes-engineer`, `platform-engineer`, `site-reliability-engineer` |
| Terraform CLI | `cloud-engineer`, `devops-engineer`, `cloud-architect` |
| PromQL | `site-reliability-engineer`, `platform-engineer` |

## Certification mapping

Map `certifications` to exam domains where the sheet supports revision:

| Certification | Example cheat sheets |
|---------------|---------------------|
| RHCSA / RHCE | Linux commands, systemd, storage, networking |
| CKA / CKAD / CKS | kubectl, YAML, RBAC, troubleshooting, security |
| Terraform Associate | CLI, state, modules, providers |
| AWS / Azure / GCP associate | Cloud CLI, IAM, core services |

Cross-reference [`certification_mapping.md`](certification_mapping.md) for full tutorial ↔ exam coverage.

## Repository layout

Recommended public site structure as the catalogue grows:

```
docs/cheatsheets/
  index.md              # landing (cheatsheets.html)
  linux.md              # consolidated sheet (today)
  linux/                # topic sheets (future)
    commands.md
    systemd.md
  docker/
  kubernetes/
  terraform/
  aws/
  cicd/
  observability/
  ...
```

Nav groups by technology in `.pages` as topic sheets ship.

## Flat vs topic sheets

| Approach | Use when |
|----------|----------|
| Single `linux.md` | Technology has one published track and moderate command surface |
| `linux/commands.md`, etc. | Technology has 8+ distinct topics or sheets exceed ~300 lines |

Keep consolidated sheets scannable with clear H2 sections and anchor links.
