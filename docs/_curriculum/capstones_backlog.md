---
title: Capstones backlog
description: Associate through architect capstone backlog for REBASH Academy — ordered by level and learning path.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Capstones backlog

Master backlog for career-path capstones. Align IDs and metadata with [`capstone-frontmatter-schema.md`](capstone-frontmatter-schema.md) and [`curriculum.yaml`](../../curriculum.yaml).

**Status values:** `published` · `draft` · `planned`

**Note:** Several capstone-level builds ship today under `docs/projects/` until dedicated capstone pages are authored. The `related_projects` column links to those builds.

## Published — path-ending builds (via projects)

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Related projects | Skills | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|------------------|--------|----------|--------|
| `linux-enterprise-ops-platform` | linux-administrator, site-reliability-engineer | Enterprise Linux Server Platform | expert | expert | 20–30 h | linux, shell | projects/linux-production-operations-platform | hardening, backup, alerting | P1 | published |
| `shell-automation-framework` | devops-engineer, platform-engineer | Production Shell Automation Framework | expert | expert | 20–30 h | shell, linux | projects/shell-production-automation-framework | modular Bash, strict mode, logging | P1 | published |
| `python-devops-automation-platform` | devops-engineer, platform-engineer, ai-for-devops | Enterprise DevOps Automation Platform | expert | expert | 24–40 h | python, docker, kubernetes | projects/python-devops-automation-framework | CLI, plugins, cloud, CI | P1 | published |
| `python-platform-engineering-framework` | platform-engineer | Internal Developer Platform (Python) | professional | expert | 16–24 h | python | projects/python-platform-engineering-framework | plugins, packaging, golden paths | P1 | published |
| `status-api-portfolio-gateway` | devops-engineer, kubernetes-engineer | Multi-stack Portfolio Gateway | associate | intermediate | 3–4 h | git, docker, kubernetes, terraform | projects/status-api-portfolio | GitOps foundations, IaC metadata | P1 | published |

## Planned — Cloud Engineering

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|----------|--------|
| `terraform-enterprise-landing-zone` | cloud-engineer, cloud-architect | Enterprise Landing Zone | architect | expert | 40–60 h | terraform, aws | P1 | planned |
| `aws-production-platform` | cloud-engineer | Production AWS Platform | expert | expert | 30–45 h | aws, terraform, networking | P1 | planned |
| `azure-enterprise-platform` | cloud-engineer | Enterprise Azure Platform | expert | expert | 30–45 h | azure, terraform | P2 | planned |
| `gcp-enterprise-platform` | cloud-engineer | Enterprise GCP Platform | expert | expert | 30–45 h | gcp, terraform, kubernetes | P2 | planned |
| `multi-cloud-enterprise-platform` | cloud-architect | Multi-cloud Enterprise Platform | architect | expert | 50–80 h | aws, azure, gcp, terraform | P1 | planned |

## Planned — DevOps & delivery

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|----------|--------|
| `enterprise-devops-platform` | devops-engineer | Enterprise DevOps Platform | expert | expert | 30–45 h | gitlab, docker, kubernetes, terraform | P1 | planned |
| `github-actions-ci-platform` | devops-engineer | Enterprise CI Platform | professional | advanced | 20–30 h | github-actions, docker | P2 | planned |
| `jenkins-enterprise-platform` | devops-engineer | Enterprise Jenkins Platform | professional | advanced | 20–30 h | jenkins, docker | P3 | planned |
| `gitlab-devsecops-pipeline` | devsecops-engineer | Enterprise DevSecOps Pipeline | expert | expert | 30–45 h | gitlab, devsecops, kubernetes | P1 | planned |
| `secure-software-factory` | devsecops-engineer | Secure Software Factory | expert | expert | 35–50 h | devsecops, gitlab, kubernetes | P1 | planned |

## Planned — Kubernetes & platform

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|----------|--------|
| `kubernetes-enterprise-platform` | kubernetes-engineer, platform-engineer | Enterprise Kubernetes Platform | expert | expert | 35–50 h | kubernetes, helm, terraform | P1 | planned |
| `argocd-gitops-platform` | kubernetes-engineer, platform-engineer | Enterprise GitOps Platform | expert | expert | 30–45 h | argocd, kubernetes, gitlab | P1 | planned |
| `docker-container-platform` | devops-engineer | Enterprise Container Platform | professional | advanced | 20–30 h | docker, compose | P2 | planned |
| `internal-developer-platform` | platform-engineer | Internal Developer Platform | architect | expert | 45–60 h | kubernetes, terraform, gitlab, backstage | P1 | planned |

## Planned — Observability & SRE

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|----------|--------|
| `prometheus-monitoring-platform` | site-reliability-engineer | Enterprise Monitoring Platform | professional | advanced | 20–30 h | prometheus, grafana | P2 | planned |
| `loki-logging-platform` | site-reliability-engineer | Centralised Logging Platform | professional | advanced | 20–30 h | loki, grafana | P2 | planned |
| `tempo-tracing-platform` | site-reliability-engineer | Distributed Tracing Platform | professional | advanced | 20–30 h | tempo, opentelemetry | P3 | planned |
| `observability-enterprise-platform` | site-reliability-engineer, platform-engineer | Enterprise Observability Platform | expert | expert | 35–50 h | prometheus, grafana, loki, tempo | P1 | planned |
| `enterprise-reliability-platform` | site-reliability-engineer | Enterprise Reliability Platform | expert | expert | 35–50 h | prometheus, kubernetes, terraform | P1 | planned |

## Planned — Architecture, operations & AI

| Capstone ID | Learning path | Title | Level | Difficulty | Duration | Technologies | Priority | Status |
|-------------|-------------|-------|-------|------------|----------|--------------|----------|--------|
| `enterprise-hybrid-network` | cloud-engineer, cloud-architect | Enterprise Hybrid Network | expert | expert | 25–35 h | networking, aws, terraform | P2 | planned |
| `ai-assisted-platform-ops` | ai-for-devops, site-reliability-engineer | AI-assisted Platform Operations | expert | expert | 25–40 h | python, ai-for-devops, kubernetes | P2 | planned |

## Capstone categories

| Category | Capstones |
|----------|-----------|
| Cloud Engineering | Landing zone, AWS/Azure/GCP platforms |
| DevOps | DevOps platform, CI platforms, portfolio gateway |
| Kubernetes | Enterprise Kubernetes, GitOps |
| Platform Engineering | IDP, Python platform framework |
| DevSecOps | DevSecOps pipeline, secure software factory |
| Site Reliability Engineering | Observability stack, reliability platform |
| Cloud Architecture | Multi-cloud enterprise platform |
| AI for DevOps | AI-assisted platform operations |
| Multi-Cloud | Multi-cloud enterprise platform |
| Enterprise Operations | Linux server platform, hybrid network |

## Portfolio graduation targets

Every learner targeting job readiness should aim for:

| # | Repository type | Example |
|---|-----------------|---------|
| 1 | Path-ending capstone | Enterprise DevOps Automation Platform |
| 2 | Multi-stack portfolio | Status API Portfolio Build |
| 3 | Cloud or IaC proof | Enterprise Landing Zone |
| 4 | Kubernetes or GitOps proof | Enterprise GitOps Platform |
| 5 | Observability or SRE proof | Enterprise Observability Platform |
| 6–10 | Domain depth | DevSecOps, IDP, or multi-cloud as role requires |

Each repo must include README, architecture diagram, validation steps, and cleanup instructions.

## Navigation structure

Public MkDocs nav under `docs/capstones/`:

```
Capstones
  Overview
  Cloud Engineer capstones (future group)
  DevOps Engineer capstones (future group)
  Kubernetes Engineer capstones (future group)
  Platform Engineer capstones (future group)
  DevSecOps Engineer capstones (future group)
  SRE capstones (future group)
  Cloud Architect capstones (future group)
  AI for DevOps capstones (future group)
```

The landing page (`capstones.html`) is the visual catalogue until per-path nav groups are populated.

## Promotion workflow

When a capstone moves from project to dedicated page:

1. Author `docs/capstones/<slug>.md` using the capstone schema
2. Add full assessment rubric and career-path mapping
3. Add nav entry under the relevant career-path group in `.pages`
4. Keep `related_projects` pointing to the original project build for continuity
5. Update career-path index to link to the capstone page
