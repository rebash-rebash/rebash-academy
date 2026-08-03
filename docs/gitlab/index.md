---
title: Overview
description: "GitLab CI/CD for Cloud & DevOps Engineers — 18 modules covering pipelines, runners, Docker, Kubernetes, Terraform, DevSecOps, and enterprise GitLab."
difficulty: intermediate
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: gitlab
tags:
  - gitlab
  - gitlab-ci
  - cicd
  - devops
  - course
comments: false
---

# GitLab CI/CD for Cloud & DevOps Engineers

**Duration:** 8–10 weeks · **Difficulty:** Intermediate → Advanced
{ .ra-facts }

Production GitLab CI/CD — design pipelines, operate runners, ship containers, deploy to Kubernetes and cloud, automate Terraform, and run enterprise DevSecOps platforms.

!!! tip "Course status"
    Curriculum follows the REBASH GitLab CI technology prompt (**18 modules**). Tutorials use the academy standard with **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Regenerate with `python3 scripts/generate-excalidraw-svg.py`. Start with [GitLab CI/CD Fundamentals](gitlab-ci-fundamentals.md).

## 1. Course overview

### Purpose

Build and operate Continuous Integration and Continuous Delivery (CI/CD) on GitLab: `.gitlab-ci.yml`, runners, merge-request pipelines, secure variables, container builds, Kubernetes via the GitLab Agent, Terraform plans, multi-cloud OIDC, and production promotion.

### Target roles

DevOps · Cloud · Platform · SRE · DevSecOps · Infrastructure

### Prerequisites

- [Git](../git/index.md) · [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md) · [Terraform](../terraform/index.md)
- Basic cloud knowledge (AWS, Azure, or Google Cloud)

### Capstone outcomes

Enterprise pipelines · autoscaling runners · GitLab Agent · Terraform automation · multi-cloud deploys · security scanning · release automation · GitOps · monitoring · DR awareness

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | CI/CD fundamentals | [Fundamentals](gitlab-ci-fundamentals.md) |
| 2 | Projects | [MRs & releases](gitlab-projects-mrs-and-releases.md) |
| 3 | Runners | [Runners & executors](gitlab-runners-and-executors.md) |
| 4 | Pipeline syntax | [`.gitlab-ci.yml`](pipeline-syntax-gitlab-ci-yml.md) |
| 5 | Pipeline design | [DAGs & includes](pipeline-design-dags-and-includes.md) |
| 6 | Variables & secrets | [Variables · OIDC](variables-secrets-and-oidc.md) |
| 7 | Artifacts & cache | [Artifacts & cache](artifacts-caches-and-dependencies.md) |
| 8 | Docker pipelines | [Docker builds](building-docker-images-in-ci.md) |
| 9 | Kubernetes | [Agent & deploys](kubernetes-deploys-and-gitlab-agent.md) |
| 10 | Terraform | [TF pipelines](terraform-pipelines-in-gitlab.md) |
| 11 | Cloud deployments | [AWS · Azure · GCP](multi-cloud-deployments-with-gitlab.md) |
| 12 | DevSecOps | [Security scanning](security-scanning-and-devsecops.md) |
| 13 | Testing | [Tests & gates](testing-reports-and-quality-gates.md) |
| 14 | Releases | [Tags & releases](release-management-and-versioning.md) |
| 15 | Production | [Promotion & approvals](production-pipelines-and-environments.md) |
| 16 | Monitoring | [Observability](pipeline-monitoring-and-observability.md) |
| 17 | Troubleshooting | [Troubleshooting](troubleshooting-gitlab-ci.md) |
| 18 | Enterprise | [Groups & governance](enterprise-gitlab.md) |

## 3. Practice

- [Labs](../labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)
- [Roadmap](roadmap.md) · [FAQ](faq.md) · [Certifications](certifications/index.md)

## Diagrams

```bash title="Terminal"
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Git](../git/index.md) · [Docker](../docker/index.md) · [Kubernetes](../kubernetes/index.md)
- [Terraform](../terraform/index.md) · [Helm](../helm/index.md) · [GitHub Actions](../github-actions/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
