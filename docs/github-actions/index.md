---
title: Overview
description: "GitHub Actions for Cloud & DevOps Engineers — 16 modules from CI/CD fundamentals through enterprise pipelines, OIDC, Kubernetes, Terraform, and production operations."
difficulty: beginner
estimated_time: "6–8 weeks"
author: Shaik Basha
last_updated: "2026-07-31"
category: github-actions
tags:
  - github-actions
  - cicd
  - devops
  - course
comments: false
---

# GitHub Actions for Cloud & DevOps Engineers

**Duration:** 6–8 weeks · **Difficulty:** Beginner → Expert
{ .ra-facts }

Production Continuous Integration and Continuous Delivery (CI/CD) with GitHub Actions — design workflows, operate runners, ship containers, deploy to Kubernetes and cloud, automate Terraform, and harden the supply chain.

!!! tip "Course status"
    Curriculum follows the REBASH GitHub Actions technology prompt (**16 modules**). Tutorials use the academy standard with **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Regenerate with `python3 scripts/generate-excalidraw-svg.py`. Start with [CI/CD Fundamentals](cicd-fundamentals-and-github-actions.md).

## 1. Course overview

### Purpose

Treat delivery as software: versioned workflows under `.github/workflows/`, reviewable checks on pull requests, OIDC to cloud (no long-lived keys), reusable actions, and environment-gated production deploys.

### Target roles

DevOps · Cloud · Platform · SRE · DevSecOps · Software Engineer

### Prerequisites

- [Git](../git/index.md) (required)
- [Docker](../docker/index.md) · [Kubernetes](../kubernetes/index.md) · [Terraform](../terraform/index.md) for later modules
- Basic cloud knowledge (AWS, Azure, or Google Cloud)

### Learning arc

| Phase | Modules | Level |
|-------|---------|-------|
| Foundations | 1–2 | Beginner |
| Core CI | 3–6 | Intermediate |
| Delivery & platforms | 7–10 | Intermediate → Advanced |
| Hardening & scale | 11–14 | Advanced |
| Production & ops | 15–16 | Advanced → Expert |

### Capstone outcomes

Reusable workflows · self-hosted runners · OIDC · multi-cloud · Kubernetes · Terraform automation · security scanning · release automation · rollbacks

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | CI/CD fundamentals | [Fundamentals](cicd-fundamentals-and-github-actions.md) |
| 2 | Actions basics | [Workflows · jobs · steps](github-actions-basics-workflows-jobs-steps.md) |
| 3 | Runners | [Hosted & self-hosted](github-hosted-and-self-hosted-runners.md) |
| 4 | Workflow syntax | [Matrix & reusable](workflow-syntax-matrix-and-reusable.md) |
| 5 | Secrets & variables | [Secrets · OIDC](secrets-variables-and-oidc.md) |
| 6 | Artifacts & caching | [Artifacts & cache](artifacts-and-caching.md) |
| 7 | Docker pipelines | [Docker · GHCR](docker-pipelines-with-github-actions.md) |
| 8 | Kubernetes | [Deploy with Actions](kubernetes-deployments-with-github-actions.md) |
| 9 | Terraform | [Plan & apply](terraform-pipelines-with-github-actions.md) |
| 10 | Cloud deployments | [AWS · Azure · GCP](multi-cloud-deployments-with-github-actions.md) |
| 11 | Security | [Supply chain](security-scanning-and-supply-chain.md) |
| 12 | Testing | [Tests & gates](testing-in-github-actions.md) |
| 13 | Releases | [Tags & releases](release-management-and-versioning.md) |
| 14 | Reusable components | [Composite & workflows](composite-actions-and-reusable-workflows.md) |
| 15 | Production | [Environments & CD](production-pipelines-and-environments.md) |
| 16 | Troubleshooting | [Debug & optimise](troubleshooting-github-actions.md) |

## 3. Practice

- [Labs](../labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)
- [Roadmap](roadmap.md) · [FAQ](faq.md) · [Certifications](certifications/index.md)

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Git](../git/index.md) · [Docker](../docker/index.md) · [Kubernetes](../kubernetes/index.md)
- [Terraform](../terraform/index.md) · [GitLab CI/CD](../gitlab/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
