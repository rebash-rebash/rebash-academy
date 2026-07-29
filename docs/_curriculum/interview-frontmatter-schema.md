---
title: Interview frontmatter schema
description: Required YAML frontmatter and body sections for every REBASH Academy interview guide and question bank.
---

# Interview frontmatter schema

Every interview guide under `docs/interview/` must include this frontmatter. Values should align with [`curriculum.yaml`](../../curriculum.yaml).

## Topic / guide frontmatter

```yaml
---
title: "Interview Prep — Human-readable title"
description: "One or two sentences for SEO and search."
technology: linux                 # curriculum technology id
difficulty: intermediate          # beginner | intermediate | advanced | expert
experience_level: mid-level       # beginner | junior | mid-level | senior | architect
estimated_time: "45–60 min"
question_count: 28                # approximate count for the guide
career_paths:
  - devops-engineer
  - linux-administrator
skills:
  - linux-troubleshooting
prerequisites:
  - linux/linux-essential-commands
related_tutorials:
  - linux/linux-systemd-services
related_labs:
  - labs/linux-production-incident-triage
related_projects:
  - projects/linux-operations-toolkit
certifications:
  - RHCSA
tags:
  - interview
  - linux
author: Shaik Basha
last_updated: "2026-07-29"
comments: false
---
```

## Body template — technology guide

Every interview guide page follows this structure:

1. **How to practise** — timed answers, diagrams, failure modes, verification
2. **Preparation checklist** — tutorials, labs, cheat sheets to complete first
3. **Question banks** — grouped by module or theme
4. **Production scenarios** — outage, scaling, security incident prompts
5. **System design prompts** — when the technology appears in design interviews
6. **Reference materials** — cheat sheets, quizzes, official docs
7. **Related resources** — career paths, certifications, projects

## Question metadata

Each question (inline today; structured YAML in future) should support:

| Field | Purpose |
|-------|---------|
| `question_id` | Stable id, e.g. `linux-fundamentals-q03` |
| `technology` | Curriculum technology id |
| `module` | Module or theme the question belongs to |
| `difficulty` | beginner · intermediate · advanced · expert |
| `experience_level` | beginner · junior · mid-level · senior · architect |
| `question_type` | See types below |
| `career_paths` | Paths this question supports |
| `skills` | Skill tags tested |
| `certifications` | Exam domains where applicable |
| `related_tutorials` | Deep-dive links |
| `related_labs` | Hands-on reinforcement |
| `related_projects` | Portfolio tie-in |
| `estimated_time` | Expected answer duration, e.g. `2 min` |
| `tags` | Free-form tags |

## Question body structure

Every interview question includes:

| Section | Required |
|---------|----------|
| Question | Yes |
| Expected answer (summary) | Yes — in tip block or reveal |
| Detailed explanation | Recommended |
| Common mistakes | Recommended |
| Follow-up questions | For senior+ levels |
| Production scenario | For mid-level+ troubleshooting types |
| Best practices | When relevant |
| Official references | Yes — upstream docs first |
| Related tutorial / lab / project | Link when content exists |

## Experience levels

| Level | `experience_level` | Expectations |
|-------|-------------------|--------------|
| 1 | `beginner` | Definitions, basic commands, first-job readiness |
| 2 | `junior` | Explain how tools work; simple troubleshooting |
| 3 | `mid-level` | Scenario answers; tie to production constraints |
| 4 | `senior` | Trade-offs, failure modes, cross-team impact |
| 5 | `architect` | System design, cost, HA, DR, and org-scale decisions |

## Question types

| Type | `question_type` | Use when |
|------|-----------------|----------|
| Theory | `theory` | Definitions and fundamentals |
| Concept | `concept` | How something works internally |
| Command | `command` | CLI recall and flags |
| CLI | `cli` | Tool-specific operational commands |
| Configuration | `configuration` | Config files, YAML, manifests |
| Scenario | `scenario` | Realistic on-the-job situations |
| Troubleshooting | `troubleshooting` | Symptom → diagnosis → fix |
| Architecture | `architecture` | Component design and boundaries |
| System design | `system-design` | End-to-end platform design |
| Security | `security` | Threat model, hardening, compliance |
| Performance | `performance` | Latency, throughput, tuning |
| High availability | `high-availability` | Redundancy, failover, SLO impact |
| Cost optimisation | `cost-optimisation` | Spend controls and trade-offs |
| Production incident | `production-incident` | On-call and incident response |
| Best practices | `best-practices` | Production patterns and anti-patterns |
| Behavioural | `behavioural` | STAR-format soft skills |
| Leadership | `leadership` | Senior and architect stakeholder questions |

## Mock interview framework

Mock interviews are timed bundles of questions — authored under `docs/interview/mock-interviews/` as they ship.

| Format | Duration | Audience | Composition |
|--------|----------|----------|-------------|
| Quick screen | 30 min | Junior | Fundamentals + 1 scenario |
| Standard technical | 60 min | Mid-level | Concepts + troubleshooting + 1 design sketch |
| Deep technical | 90 min | Senior | Scenarios + system design + production incident |
| DevOps interview | 60–90 min | DevOps Engineer | Linux, CI/CD, containers, IaC mix |
| Platform Engineer | 60–90 min | Platform Engineer | K8s, IDP, GitOps, developer experience |
| SRE interview | 60–90 min | SRE | Observability, incidents, SLOs, scaling |
| Cloud Architect | 90 min | Cloud Architect | Landing zones, multi-cloud, HA, DR, cost |
| DevSecOps interview | 60 min | DevSecOps Engineer | Pipeline security, secrets, compliance |

Each mock interview page declares `question_ids` or embedded sections and a preparation checklist.

## System design section

Dedicated prompts under `docs/interview/system-design/` (planned):

| Topic | Typical paths |
|-------|---------------|
| Cloud architecture | `cloud-architect`, `cloud-engineer` |
| Kubernetes platform design | `kubernetes-engineer`, `platform-engineer` |
| Observability design | `site-reliability-engineer` |
| CI/CD design | `devops-engineer` |
| Landing zones | `cloud-architect`, `cloud-engineer` |
| Platform engineering | `platform-engineer` |
| High availability | `site-reliability-engineer`, `cloud-architect` |
| Disaster recovery | `cloud-architect`, `site-reliability-engineer` |
| Security architecture | `devsecops-engineer`, `cloud-architect` |
| Cost optimisation | `cloud-architect`, `cloud-engineer` |

## Production scenarios section

Scenario banks under each technology guide or `docs/interview/scenarios/` (planned):

- Production outages
- Incident response and escalation
- Root cause analysis
- Performance degradation
- Scaling failures
- Security incidents
- Cloud provider failures
- Disaster recovery execution

## Career path mapping

| Career path | Primary interview guides |
|-------------|-------------------------|
| `beginner` | Linux, Git, Networking fundamentals |
| `linux-administrator` | Linux, Shell, Networking |
| `cloud-engineer` | AWS, Terraform, Networking |
| `devops-engineer` | Linux, Shell, Docker, K8s, CI/CD, Terraform |
| `kubernetes-engineer` | Kubernetes, Docker, Networking |
| `platform-engineer` | Kubernetes, CI/CD, Terraform, Platform Engineering |
| `devsecops-engineer` | CI/CD, Docker, Kubernetes, DevSecOps |
| `site-reliability-engineer` | Linux, Kubernetes, Observability, SRE scenarios |
| `cloud-architect` | AWS, Terraform, Architecture, System design |
| `ai-for-devops` | Python, AI for DevOps |

## Certification mapping

| Certification | Interview guides |
|---------------|------------------|
| RHCSA / RHCE | Linux, Shell, Networking |
| CKA / CKAD / CKS | Kubernetes, Docker, Linux |
| Terraform Associate | Terraform, AWS |
| AWS Solutions Architect / DevOps Pro | AWS, Terraform, CI/CD |
| AZ-104 / AZ-305 | Azure (planned) |
| Google ACE / PCA / PCDOE | GCP (planned) |
| Prometheus Certified Associate | Prometheus (planned) |

Cross-reference [`certification_mapping.md`](certification_mapping.md).

## Repository layout

```
docs/interview/
  index.md                  # landing (interview.html)
  linux.md                  # technology guide (today)
  kubernetes.md
  mock-interviews/          # timed mock interviews (future)
  system-design/            # architecture prompts (future)
  scenarios/                # cross-cutting production scenarios (future)
  linux/                    # topic splits when banks grow (future)
```

Nav groups by technology in `.pages`; add Mock Interviews and System Design groups as content ships.

## Learning flow

| Stage | Role of interview prep |
|-------|------------------------|
| After tutorial | Spot knowledge gaps before labs |
| After lab | Explain what you did and why |
| After project | Defend architecture in portfolio reviews |
| Before applications | Timed mock interviews |
| With certifications | Exam-style drill alongside quizzes |

See [`interview-learning-flow.d2`](../assets/d2/interview-learning-flow.d2).
