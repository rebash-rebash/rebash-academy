---
title: Capstone frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy capstone.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Capstone frontmatter schema

Every capstone under `docs/capstones/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

```yaml
---
title: "Capstone — Human-readable title"
description: "One or two sentences for SEO and search."
difficulty: advanced                 # intermediate | advanced | expert
capstone_level: professional         # associate | professional | expert | architect
estimated_time: "24–40 hours"
learning_paths:
  - devops-engineer
  - platform-engineer
technologies:
  - kubernetes
  - terraform
  - gitlab
skills:
  - gitops-delivery
  - platform-design
prerequisites:
  - learning-paths/devops-engineer
related_courses:
  - kubernetes/
  - terraform/
related_projects:
  - projects/status-api-portfolio
environment:
  - local
  - kubernetes
cloud_provider: aws                  # aws | azure | gcp | multi | null
estimated_cost: low                  # free | low | moderate — with cleanup note in body
github_repository: null              # optional learner repo template URL
portfolio_ready: true
interview_ready: true
tags:
  - capstones
  - devops-engineer
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template

Every capstone page follows this structure:

1. **Capstone overview** — purpose, audience, duration, estimated cost
2. **Business problem** — realistic scenario and constraints
3. **Business requirements**
4. **Functional requirements**
5. **Non-functional requirements** — availability, security, cost, operability
6. **Target audience** — role and experience level
7. **Learning objectives**
8. **Prerequisites** — learning paths, tutorials, labs, and projects
9. **Architecture** — D2 diagram(s) for topology and data flow
10. **Implementation phases** — ordered build stages with milestones
11. **Milestones** — checkpoint deliverables per phase
12. **Deliverables** — repo artefacts learners must produce
13. **Validation** — functional acceptance criteria
14. **Testing** — unit, integration, smoke, and chaos where relevant
15. **Security review** — threat model and hardening checklist
16. **Performance review** — load, latency, and capacity targets
17. **Cost optimisation** — spend controls and teardown
18. **Operations guide** — runbooks, on-call, and day-two tasks
19. **Disaster recovery** — backup, restore, and failover
20. **Documentation requirements** — README, ADRs, and presentation
21. **Assessment rubric** — link to review criteria below
22. **Future improvements**
23. **References** — official docs first

## Capstone levels

| Level | `capstone_level` | Typical `difficulty` | Expectations |
|-------|------------------|----------------------|--------------|
| Associate | `associate` | intermediate | Single-domain proof — one primary technology stack |
| Professional | `professional` | advanced | Multi-tool delivery — CI/CD, IaC, or observability combined |
| Expert | `expert` | expert | Production-grade platform — security, ops, and validation |
| Architect | `architect` | expert | Cross-domain design — multi-account, multi-cloud, or IDP scale |

## Implementation phases

Standard phase order (adapt per capstone):

| Phase | Focus |
|-------|--------|
| Planning | Scope, requirements, success criteria |
| Architecture | Diagrams, ADRs, interface contracts |
| Infrastructure | Terraform, Ansible, cloud foundations |
| Application | Workloads, services, configuration |
| Automation | CI/CD, GitOps, policy as code |
| Security | IAM, scanning, secrets, compliance gates |
| Observability | Metrics, logs, traces, alerting |
| Validation | Acceptance tests and review gates |
| Documentation | README, ops guides, presentation |
| Presentation | Demo script and portfolio narrative |

## Assessment framework

Every capstone includes a self-review and peer-review checklist:

| Review | Criteria |
|--------|----------|
| Functional validation | All requirements met; demo reproducible from README |
| Architecture review | Diagrams match implementation; trade-offs documented |
| Code review | Idiomatic IaC and app code; modules and tests where applicable |
| Security review | Least privilege, secrets handling, scanning evidence |
| Performance review | Baseline metrics or load test results where NFRs apply |
| Documentation review | Clear setup, validation, troubleshooting, and cleanup |
| Operational readiness | Runbooks, monitoring, and on-call playbooks |

## Deliverables

| Deliverable | Required |
|-------------|----------|
| GitHub repository | Yes |
| README | Yes |
| Architecture diagram | Yes |
| D2 diagrams | When topology or flow matters |
| Infrastructure code | When IaC is in scope |
| CI/CD | When delivery automation is in scope |
| Deployment guide | Yes |
| Operations guide | Recommended |
| Monitoring | When observability is in scope |
| Troubleshooting guide | Yes |
| Screenshots | Recommended for dashboards and UIs |
| Lessons learned | Recommended in README |
| Project presentation | Recommended — slides or demo script |

## Learning path mapping

Each capstone declares one or more `learning_paths` ids. Recommended capstone per path:

| Learning path | Example capstone |
|-------------|------------------|
| `cloud-engineer` | Production AWS Platform |
| `devops-engineer` | Enterprise DevOps Platform |
| `kubernetes-engineer` | Enterprise Kubernetes Platform |
| `platform-engineer` | Internal Developer Platform |
| `devsecops-engineer` | Secure Software Factory |
| `site-reliability-engineer` | Enterprise Reliability Platform |
| `cloud-architect` | Multi-cloud Enterprise Platform |
| `ai-for-devops` | AI-assisted Platform Operations |
| `linux-administrator` | Enterprise Linux Server Platform |

Cross-link from [`learning-paths/`](../learning-paths/index.md) pages to the capstone that completes each path.

## Portfolio strategy

Learners should graduate with **5–10 production-quality repositories** suitable for interviews:

1. At least one **path-ending capstone** per target learning path
2. One **multi-stack portfolio build** (e.g. Status API or GitOps platform)
3. One **observability or SRE** proof where targeting SRE roles
4. One **security or DevSecOps** proof where targeting DevSecOps roles
5. README quality consistent across all repos — architecture, validation, cleanup

Capstone builds may initially ship under `docs/projects/` until dedicated `docs/capstones/<slug>/` pages are authored. Link both ways in frontmatter.

## Repository layout

Recommended public site structure as the catalogue grows:

```
docs/capstones/
  index.md              # landing (capstones.html)
  cloud/
  devops/
  kubernetes/
  platform/
  devsecops/
  sre/
  architecture/
  ai/
```

Each published capstone is a single markdown file or folder with `index.md`. Nav groups by learning path in `.pages` as content ships.

## Related project vs capstone

| Aspect | Project | Capstone |
|--------|---------|----------|
| Scope | Single or few technologies | Multi-technology, path-ending |
| Audience | Skill application | Career-path graduation |
| Assessment | Self-validation | Full review rubric |
| Duration | 3–40 hours | Typically 20–80 hours |

Projects at `project_level: capstone` may be promoted to dedicated capstone pages when the full rubric and career-path mapping are authored.
