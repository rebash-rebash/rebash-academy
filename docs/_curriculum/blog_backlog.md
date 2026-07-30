---
title: Blog backlog
description: Engineering journal article backlog for REBASH Academy — ordered by priority and audience.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Blog backlog

Master backlog for engineering journal articles. Align with [`blog-frontmatter-schema.md`](blog-frontmatter-schema.md) and [`curriculum.yaml`](../../curriculum.yaml).

**Status values:** `published` · `draft` · `planned`

No articles are published yet. The landing page and nav ship with the framework; articles appear in the sidebar as they are authored.

## Planned — Release notes & product

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `release-notes-launch` | release-notes | REBASH Academy launch — what is live today | release-notes | beginner | 5 min | — | beginner | P1 | planned |
| `release-notes-monthly-template` | release-notes | Monthly content release template | release-notes | beginner | 3 min | — | — | P2 | planned |
| `roadmap-q3-update` | release-notes | Content roadmap update | roadmap-update | beginner | 6 min | — | — | P2 | planned |

## Planned — Engineering & DevOps

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `why-linux-first` | engineering | Why Linux still comes first in DevOps hiring | opinion | beginner | 8 min | linux | beginner, devops-engineer | P1 | planned |
| `git-recovery-stories` | engineering | Git recovery patterns every team needs | lessons-learned | intermediate | 10 min | git | devops-engineer | P2 | planned |
| `shell-strict-mode-production` | engineering | Strict mode in production Bash scripts | best-practices | intermediate | 8 min | shell, linux | devops-engineer | P2 | planned |
| `python-automation-tradeoffs` | engineering | When to reach for Python vs Shell | architecture-discussion | intermediate | 10 min | python, shell | devops-engineer | P2 | planned |

## Planned — Cloud & infrastructure

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `aws-landing-zone-intro` | cloud | Landing zones without the buzzwords | architecture-discussion | advanced | 12 min | aws, terraform | cloud-engineer, cloud-architect | P1 | planned |
| `terraform-state-lessons` | infrastructure | Terraform state mistakes and fixes | lessons-learned | intermediate | 10 min | terraform | devops-engineer, cloud-engineer | P1 | planned |
| `multi-cloud-reality` | cloud | Multi-cloud — when it helps and when it hurts | opinion | advanced | 12 min | aws, azure, gcp | cloud-architect | P2 | planned |

## Planned — Containers & Kubernetes

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `k8s-deep-dive-01-control-plane` | containers | Kubernetes deep dive — control plane | engineering-insights | advanced | 15 min | kubernetes | kubernetes-engineer | P1 | planned |
| `k8s-deep-dive-02-networking` | containers | Kubernetes deep dive — networking | engineering-insights | advanced | 15 min | kubernetes | kubernetes-engineer | P1 | planned |
| `docker-compose-to-k8s` | containers | From Compose to Kubernetes — a pragmatic path | migration-story | intermediate | 12 min | docker, kubernetes | devops-engineer | P2 | planned |
| `gitops-drift-real-world` | containers | GitOps drift — what actually breaks in production | incident-analysis | advanced | 12 min | kubernetes, argocd | platform-engineer | P2 | planned |

## Planned — Security, observability & SRE

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `pipeline-security-gates` | security | Security gates that teams keep enabled | best-practices | intermediate | 10 min | devsecops, gitlab | devsecops-engineer | P1 | planned |
| `incident-postmortem-template` | observability | Writing postmortems that change behaviour | best-practices | intermediate | 10 min | sre | site-reliability-engineer | P1 | planned |
| `prometheus-alert-fatigue` | observability | Alert fatigue — symptoms and fixes | lessons-learned | intermediate | 10 min | prometheus, grafana | site-reliability-engineer | P2 | planned |
| `slo-burn-rate-primer` | observability | SLO burn rates for busy on-call engineers | engineering-insights | advanced | 12 min | sre, prometheus | site-reliability-engineer | P2 | planned |

## Planned — Platform, architecture & AI

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `idp-golden-paths` | architecture | Golden paths without boiling the ocean | architecture-discussion | advanced | 12 min | platform-engineering, kubernetes | platform-engineer | P1 | planned |
| `platform-team-boundaries` | architecture | Where platform teams should stop | opinion | advanced | 10 min | platform-engineering | platform-engineer | P2 | planned |
| `ai-ops-practical` | ai | Practical AI in operations — what works today | ai-research-summary | intermediate | 10 min | ai-for-devops, python | ai-for-devops | P2 | planned |

## Planned — Career & community

| Article ID | Category | Title | Type | Difficulty | Reading time | Technologies | Career paths | Priority | Status |
|------------|----------|-------|------|------------|--------------|--------------|--------------|----------|--------|
| `devops-career-path-2026` | career | DevOps career paths in 2026 — skills that matter | career-advice | beginner | 10 min | — | devops-engineer, beginner | P1 | planned |
| `portfolio-projects-interviews` | career | Portfolio projects that survive technical interviews | career-advice | intermediate | 10 min | — | devops-engineer, kubernetes-engineer | P1 | planned |
| `community-contributor-guide` | community | Contributing to REBASH Academy | community-update | beginner | 6 min | — | — | P2 | planned |
| `kubecon-summary-template` | community | Conference takeaways — what to publish after KubeCon | conference-summary | intermediate | 8 min | kubernetes | — | P3 | planned |

## Article series roadmap

| Series slug | Parts planned | First article ID | Priority |
|-------------|---------------|------------------|----------|
| `kubernetes-deep-dive` | 5+ | `k8s-deep-dive-01-control-plane` | P1 |
| `terraform-best-practices` | 4+ | `terraform-state-lessons` | P1 |
| `aws-architecture` | 4+ | `aws-landing-zone-intro` | P1 |
| `linux-internals` | 3+ | `why-linux-first` | P2 |
| `devops-journey` | 3+ | `devops-career-path-2026` | P2 |
| `platform-engineering` | 4+ | `idp-golden-paths` | P2 |
| `sre-fundamentals` | 4+ | `slo-burn-rate-primer` | P2 |
| `ai-for-devops` | 3+ | `ai-ops-practical` | P3 |

## Featured editorial themes (landing page)

Until `featured: true` articles exist, the landing page highlights these planned themes:

1. **Release notes** — Academy changelog and milestones
2. **Kubernetes deep dive** — multi-part series
3. **Terraform best practices** — IaC lessons learned
4. **Incident analysis** — production postmortems
5. **Platform engineering** — IDP and golden paths
6. **AI for DevOps** — practical automation with AI

## Authoring order

1. `release-notes-launch` — announce what is live and link to Getting Started
2. `why-linux-first` — SEO-friendly entry point aligned with beginner path
3. `devops-career-path-2026` — career hub content
4. `terraform-state-lessons` — high search intent, links to Terraform track
5. `k8s-deep-dive-01-control-plane` — start flagship Kubernetes series
6. `portfolio-projects-interviews` — cross-link projects and interview prep

## Navigation rollout

1. **Phase 1** — Overview landing (`blog.html`) only
2. **Phase 2** — First articles in flat `docs/blog/<slug>.md` files
3. **Phase 3** — Category subfolders and `.pages` groups
4. **Phase 4** — Series indexes under `docs/blog/series/`
5. **Phase 5** — RSS feed and featured/latest automation
