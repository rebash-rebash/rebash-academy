---
title: Quizzes backlog
description: Quiz delivery backlog — ordered from beginner foundations to expert assessments.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Quizzes backlog

Master list for quiz authoring and curriculum alignment. Align frontmatter with [`quiz-frontmatter-schema.md`](quiz-frontmatter-schema.md) and ids with [`curriculum.yaml`](../../curriculum.yaml).

**Status values:** `published` (live under `docs/quizzes/`) · `planned` (on roadmap) · `draft` (in progress)

**Priority:** `P0` foundations · `P1` path-critical · `P2` depth · `P3` stretch

## Published quizzes (12)

Ordered beginner → expert within each technology group.

| Quiz ID | Technology | Module | Title | Type | Difficulty | Questions | Pass | Career paths | Related tutorials | Related labs | Certifications | Priority | Status |
|---------|------------|--------|-------|------|------------|-----------|------|--------------|-------------------|--------------|----------------|----------|--------|
| `quizzes/linux-for-cloud-devops-fundamentals` | linux | Course | Linux for Cloud & DevOps Fundamentals | course | intermediate | 40 | 70% | devops-engineer, linux-administrator | linux track | linux-production-incident-triage | RHCSA | P0 | published |
| `quizzes/linux-fundamentals` | linux | Course | Linux Fundamentals | course | intermediate | 40 | 70% | devops-engineer, linux-administrator | linux track | linux-services-and-logs-lab | RHCSA | P0 | published |
| `quizzes/linux-servers` | linux | Servers | Linux Servers | module | intermediate | 25 | 70% | linux-administrator | linux servers modules | linux-app-server-from-zero | RHCSA | P1 | published |
| `quizzes/shell-scripting-for-devops-fundamentals` | shell | Course | Shell Scripting for DevOps Fundamentals | course | intermediate | 40 | 70% | devops-engineer | shell track | shell-ops-script-hardening | — | P0 | published |
| `quizzes/shell-scripting-fundamentals` | shell | Course | Shell Scripting Fundamentals | course | intermediate | 40 | 70% | devops-engineer | shell track | shell-linux-operations-toolkit | — | P1 | published |
| `quizzes/python-for-devops-engineers-fundamentals` | python | Course | Python for DevOps Engineers Fundamentals | course | intermediate | 40 | 70% | devops-engineer, platform-engineer | python track | python-cicd-automation-tool | — | P0 | published |
| `quizzes/python-for-devops-fundamentals` | python | Course | Python for DevOps Fundamentals | course | intermediate | 40 | 70% | devops-engineer | python track | python-log-analyser | — | P1 | published |
| `quizzes/networking-production` | networking | Production | Networking Production | module | advanced | 25 | 70% | devops-engineer, sre | networking M7 | networking-dns-firewall-triage | — | P1 | published |
| `quizzes/aws-fundamentals` | aws | Course | AWS Fundamentals | course | intermediate | 40 | 70% | cloud-engineer, devops-engineer | aws track | aws-iam-vpc-triage | AWS SAA | P0 | published |
| `quizzes/cicd-fundamentals` | gitlab | Course | CI/CD Fundamentals | course | intermediate | 40 | 70% | devops-engineer, devsecops-engineer | gitlab track | cicd-pipeline-triage | — | P1 | published |
| `quizzes/docker-fundamentals` | docker | Course | Docker Fundamentals | course | intermediate | 40 | 70% | devops-engineer | docker track | docker-compose-stack-recovery | — | P1 | published |
| `quizzes/kubernetes-fundamentals` | kubernetes | Course | Kubernetes Fundamentals | course | intermediate | 40 | 70% | devops-engineer, kubernetes-engineer, sre | kubernetes track | kubernetes-deployment-triage | CKA | P1 | published |

## Planned quiz tracks

| Technology | Target count | First quiz (planned) | Certifications | Priority | Status |
|------------|--------------|----------------------|----------------|----------|--------|
| git | 4 | Git workflow fundamentals | — | P1 | planned |
| terraform | 8 | Terraform plan and state | Terraform Associate | P1 | planned |
| ansible | 8 | Playbook idempotency | — | P2 | planned |
| azure | 8 | Azure identity and networking | AZ-104 | P2 | planned |
| gcp | 8 | GCP core services | GCP ACE | P2 | planned |
| helm | 6 | Chart lifecycle | CKA | P2 | planned |
| github-actions | 6 | Workflow fundamentals | — | P2 | planned |
| jenkins | 6 | Pipeline troubleshooting | — | P3 | planned |
| argocd | 6 | GitOps sync concepts | — | P2 | planned |
| prometheus | 6 | PromQL and alerting | PCA | P2 | planned |
| grafana | 6 | Dashboard design | — | P3 | planned |
| loki | 6 | Log query patterns | — | P3 | planned |
| tempo | 6 | Trace pipeline concepts | — | P3 | planned |
| opentelemetry | 6 | Instrumentation basics | — | P3 | planned |
| devsecops | 8 | Pipeline security gates | — | P1 | planned |
| platform-engineering | 6 | IDP golden paths | — | P2 | planned |
| sre | 8 | SLOs and error budgets | — | P2 | planned |
| cloud-architecture | 6 | Landing zone design | GCP PCA, AZ-305 | P3 | planned |
| ai | 6 | AI for DevOps workflows | — | P3 | planned |

## Assessment framework

| Assessment | Typical size | Pass mark | When |
|------------|--------------|-----------|------|
| Lesson quiz | 5–10 questions | 70% | After a single tutorial |
| Module quiz | 25 questions | 70% (18) | End of module |
| Course quiz | 40 questions | 70% (28) | End of technology track |
| Technology assessment | 50+ questions | 75% | Pre-project gate |
| Career path assessment | Multi-quiz | 70% each | Path milestone |
| Certification readiness | Exam-domain mapped | 80% | Pre-exam check |

## Learning progression

```
Tutorial → Knowledge quiz → Lab → Practice quiz → Project → Final assessment → Capstone
```

## Navigation

Public browse: [Quizzes overview](../quizzes/index.md) · Sidebar: `docs/quizzes/.pages` · Do not move published quiz URLs when adding subfolders.
