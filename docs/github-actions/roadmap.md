---
title: Learning Roadmap
description: "Structured 16-module beginner-to-expert roadmap for GitHub Actions for Cloud & DevOps Engineers."
technology_id: github-actions
hide:
  - toc
author: Shaik Basha
category: github-actions
tags:
  - github-actions
  - roadmap
last_updated: "2026-08-03"
---

# GitHub Actions — Learning Roadmap

Follow the course in order for the smoothest path. Allow **6–8 weeks** at 5–8 hours per week, or compress Modules 1–6 if you already run CI elsewhere.

## Path overview

1. **Course overview** — scope, prerequisites, outcomes ([index](index.md))
2. **Modules 1–16** — beginner foundations through expert production ops
3. **Labs / quizzes / projects** — hands-on under `~/rebash-github-actions/module-NN`
4. **Capstone** — production CI/CD platform (capstone)
5. **Interview & certifications** — GitHub Foundations / Actions / Administration

![GitHub Actions architecture](../assets/excalidraw/gha-architecture.svg)

![Workflow lifecycle](../assets/excalidraw/gha-workflow-lifecycle.svg)

## Pacing guide

| Week | Modules | Focus | Approx. time |
|------|---------|-------|--------------|
| 1 | 1–2 | CI/CD concepts; first workflow | 6–8 h |
| 2 | 3–4 | Runners; matrix & conditionals | 6–8 h |
| 3 | 5–6 | Secrets, OIDC intro; artefacts & cache | 6–8 h |
| 4 | 7–8 | Docker/GHCR; Kubernetes deploy | 8–10 h |
| 5 | 9–10 | Terraform plan/apply; multi-cloud OIDC stubs | 8–10 h |
| 6 | 11–12 | Security scanning; testing layers | 8–10 h |
| 7 | 13–14 | Releases; composite & reusable workflows | 6–8 h |
| 8 | 15–16 | Production environments; troubleshooting | 8–10 h |

Adjust pace if you skip cloud deploy labs until sandbox accounts are ready — Modules 9–11 remain valuable offline.

## Modules

| # | Focus | Level | Tutorial | Diagram |
|---|-------|-------|----------|---------|
| 1 | CI/CD fundamentals | Beginner | [Fundamentals](cicd-fundamentals-and-github-actions.md) | `gha-workflow-lifecycle.svg` |
| 2 | Actions basics | Beginner | [Workflows · jobs · steps](github-actions-basics-workflows-jobs-steps.md) | `gha-basics.svg` |
| 3 | Runners | Intermediate | [Hosted & self-hosted](github-hosted-and-self-hosted-runners.md) | `gha-runner-architecture.svg` |
| 4 | Workflow syntax | Intermediate | [Matrix & reusable](workflow-syntax-matrix-and-reusable.md) | `gha-workflow-syntax.svg` |
| 5 | Secrets & variables | Intermediate | [Secrets · OIDC](secrets-variables-and-oidc.md) | `gha-secrets-oidc.svg` |
| 6 | Artifacts & caching | Intermediate | [Artifacts & cache](artifacts-and-caching.md) | `gha-artifacts-cache.svg` |
| 7 | Docker pipelines | Intermediate | [Docker · GHCR](docker-pipelines-with-github-actions.md) | `gha-docker-pipeline.svg` |
| 8 | Kubernetes | Advanced | [Deploy with Actions](kubernetes-deployments-with-github-actions.md) | `gha-kubernetes-pipeline.svg` |
| 9 | Terraform | Advanced | [Plan & apply](terraform-pipelines-with-github-actions.md) | `gha-terraform-pipeline.svg` |
| 10 | Cloud deployments | Advanced | [AWS · Azure · GCP](multi-cloud-deployments-with-github-actions.md) | `gha-multi-cloud.svg` |
| 11 | Security | Advanced | [Supply chain](security-scanning-and-supply-chain.md) | `gha-security.svg` |
| 12 | Testing | Intermediate | [Tests & gates](testing-in-github-actions.md) | `gha-testing.svg` |
| 13 | Releases | Intermediate | [Tags & releases](release-management-and-versioning.md) | `gha-release-pipeline.svg` |
| 14 | Reusable components | Advanced | [Composite & workflows](composite-actions-and-reusable-workflows.md) | `gha-reusable-components.svg` |
| 15 | Production | Expert | [Environments & CD](production-pipelines-and-environments.md) | `gha-production.svg` |
| 16 | Troubleshooting | Expert | [Debug & optimise](troubleshooting-github-actions.md) | `gha-troubleshooting.svg` |

## Diagrams

All course diagrams are **Excalidraw** sources under `docs/assets/excalidraw/`. Key assets for Modules 9–16:

- `gha-terraform-pipeline.svg` — init/validate/plan/apply gates
- `gha-multi-cloud.svg` — OIDC to AWS, Azure, GCP
- `gha-security.svg` — CodeQL, Trivy, SBOM, pinning
- `gha-testing.svg` — unit/integration/E2E job graph
- `gha-release-pipeline.svg` — SemVer tags and GitHub Releases
- `gha-reusable-components.svg` — composite actions and reusable workflows
- `gha-production.svg` — staging → production promotion
- `gha-troubleshooting.svg` — failed-job ladder

Regenerate rendered SVGs after editing `.excalidraw` sources:

``` {.bash .ra-terminal title="Terminal"}
python3 scripts/generate-excalidraw-svg.py
```

## After Module 16

- Complete the Capstone — enterprise platform with reusables, OIDC, scanning, releases
- Review Interview questions for workflow design and production scenarios
- Cross-study [Jenkins](../jenkins/roadmap.md) or [Git](../git/roadmap.md) for pipeline comparisons in interviews

## Related

- [Course index](index.md) · [FAQ](faq.md)
- [DevOps Engineer path](../learning-paths/devops-engineer/index.md)
