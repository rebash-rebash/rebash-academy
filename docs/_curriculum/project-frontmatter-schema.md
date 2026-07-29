---
title: Project frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy project.
---

# Project frontmatter schema

Every project under `docs/projects/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Project — Human-readable title"
description: "One or two sentences for SEO and search."
difficulty: intermediate          # beginner | intermediate | advanced | expert
project_level: intermediate       # mini | intermediate | enterprise | capstone
project_type: automation          # automation | cloud-deployment | infrastructure | container-platform | kubernetes-platform | cicd-platform | monitoring-platform | gitops-platform | security-platform | migration | performance | architecture | ai-platform
estimated_time: "8–12 hours"
technology: linux                 # primary curriculum technology id
technologies:                     # all stacks used
  - linux
  - shell
career_paths:
  - devops-engineer
  - linux-administrator
skills:
  - bash-automation
prerequisites:
  - linux/linux-essential-commands
related_tutorials:
  - linux/linux-systemd-services
related_labs:
  - labs/linux-production-incident-triage
certifications:
  - RHCSA
cloud_provider: null              # aws | azure | gcp | null
environment:
  - local
estimated_cost: free              # free | low | moderate — with cleanup note in body
github_ready: true
portfolio_ready: true
tags:
  - projects
  - linux
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every project page follows this structure:

1. **Project overview** — goal, deliverable, estimated cost, time
2. **Business scenario** — realistic context and constraints
3. **Learning objectives**
4. **Prerequisites** — tutorials, labs, and tools required
5. **Requirements** — functional and non-functional
6. **Architecture** — D2 diagram when topology helps
7. **Implementation phases** — ordered build stages
8. **Validation** — how to prove the project works
9. **Testing** — unit, integration, or smoke checks
10. **Security considerations**
11. **Production considerations**
12. **Cost considerations** — cloud spend and cleanup
13. **Deliverables** — code, README, diagrams, guides
14. **GitHub repository structure** — recommended layout
15. **README requirements** — what the portfolio README must cover
16. **Future enhancements**
17. **References** — official docs first

## Project levels

| Level | `project_level` | `difficulty` typical | Learner experience |
|-------|-----------------|----------------------|-------------------|
| 1 | `mini` | beginner | Apply a few concepts from one track |
| 2 | `intermediate` | intermediate | Combine multiple tutorials and labs |
| 3 | `enterprise` | advanced / expert | Production-ready implementation |
| 4 | `capstone` | expert | Complete real-world platform |

## Project types

| Type | `project_type` | When to use |
|------|----------------|-------------|
| Automation | `automation` | Scripts, CLIs, scheduled jobs |
| Cloud deployment | `cloud-deployment` | Deploy workloads to a cloud provider |
| Infrastructure | `infrastructure` | Terraform, Ansible, landing zones |
| Container platform | `container-platform` | Docker images, Compose, registries |
| Kubernetes platform | `kubernetes-platform` | Cluster workloads, GitOps, operators |
| CI/CD platform | `cicd-platform` | Pipelines, gates, delivery automation |
| Monitoring platform | `monitoring-platform` | Metrics, logs, traces, alerting |
| GitOps platform | `gitops-platform` | Declarative delivery with Argo CD or Flux |
| Security platform | `security-platform` | Scanning, secrets, compliance gates |
| Migration | `migration` | Move workloads with rollback plan |
| Performance | `performance` | Measure, tune, and prove SLO impact |
| Architecture | `architecture` | Design and trade-off decisions |
| AI platform | `ai-platform` | AI-assisted ops workflows |

## Deliverables

Every project should produce:

| Deliverable | Required |
|-------------|----------|
| Working code | Yes |
| README | Yes |
| Architecture diagram | When topology matters |
| Deployment guide | When deploy steps are non-trivial |
| Validation guide | Yes |
| Troubleshooting guide | Recommended |
| Screenshots | Recommended for UI or dashboards |
| Lessons learned | Recommended in README |

## Repository structure

Recommended layout for learner GitHub repositories:

```
README.md
docs/
src/
terraform/
kubernetes/
scripts/
.github/
.gitlab/
ansible/
tests/
assets/
diagrams/
LICENSE
```

Include only directories relevant to the project — do not scaffold empty folders.

## Career path mapping

Every project declares one or more `career_paths` ids from `curriculum.yaml`. Examples:

| Project theme | Typical paths |
|---------------|---------------|
| Linux automation toolkit | `linux-administrator`, `devops-engineer` |
| GitOps platform | `devops-engineer`, `platform-engineer`, `site-reliability-engineer` |
| Cloud landing zone | `cloud-engineer`, `cloud-architect` |
| Observability stack | `site-reliability-engineer`, `platform-engineer` |

## Portfolio strategy

Flag `portfolio_ready: true` when the build is suitable for CV and interview demos. Recommended showcase projects:

- Cloud landing zone (Terraform)
- GitOps platform (Kubernetes + Argo CD)
- Observability platform (Prometheus + Grafana + Loki)
- DevSecOps pipeline
- Internal developer platform
- Multi-cloud infrastructure
- AI-assisted operations platform

Cross-link portfolio projects from [`capstones/`](../capstones/index.md) when they represent path-ending proof.

## Technology roadmaps

Each technology index under `docs/<technology>/` should eventually include a project roadmap table:

| Level | Example |
|-------|---------|
| Mini | Containerise an app (Docker) |
| Intermediate | Compose stack (Docker) |
| Enterprise | Production container platform (Docker) |
| Capstone | Enterprise container platform (Docker) |

Repeat for Terraform, Kubernetes, AWS, CI/CD, observability, and every curriculum technology.
