---
title: Learning Roadmap
description: "Structured 20-module learning roadmap for Terraform for Cloud & DevOps Engineers."
technology_id: terraform
hide:
  - toc
author: Shaik Basha
category: terraform
tags:
  - terraform
  - roadmap
---

# Terraform — Learning Roadmap

Follow the course in order:

1. **Course overview** — scope, prerequisites, outcomes
2. **Modules 1–20** — tutorials in sequence
3. **Labs / quizzes / projects** — practice
4. **Capstone** — production infrastructure platform
5. **Interview & certifications** — Terraform Associate

![Terraform workflow](../assets/excalidraw/terraform-workflow.svg)

![Remote state backend](../assets/excalidraw/terraform-remote-backend.svg)

## Modules

| # | Focus | Tutorials |
|---|-------|-----------|
| 1 | IaC fundamentals | [Introduction](introduction-to-terraform-and-iac.md) |
| 2 | Installing Terraform | [Install & CLI](installing-terraform-and-the-cli-workflow.md) |
| 3 | Terraform basics | [Init · plan · apply](terraform-workflow-init-plan-apply.md) |
| 4 | HCL fundamentals | [Blocks & expressions](hcl-fundamentals-blocks-arguments-and-expressions.md) |
| 5 | Providers | [Providers & plugins](providers-and-the-terraform-plugin-model.md) |
| 6 | Resources | [Resources & meta-arguments](resources-dependencies-and-meta-arguments.md) |
| 7 | Variables & outputs | [Variables · locals · outputs](variables-locals-and-outputs.md) |
| 8 | State management | [State](terraform-state-fundamentals.md) · [Remote backends](remote-state-and-backends.md) |
| 9 | Modules | [Create modules](modules-creating-reusable-infrastructure.md) · [Registry](registry-modules-and-composition.md) |
| 10 | Expressions & functions | [Functions & dynamic blocks](functions-templates-and-dynamic-blocks.md) |
| 11 | Data sources | [Data sources](data-sources-and-existing-infrastructure.md) |
| 12 | Workspaces | [Workspaces & envs](workspaces-and-environment-strategies.md) |
| 13 | Cloud & Enterprise | [HCP Terraform](terraform-cloud-and-hcp-terraform.md) |
| 14 | Testing | [Format · validate · test](format-validate-and-terraform-test.md) |
| 15 | Security | [Secrets & policy](terraform-security-and-secrets.md) |
| 16 | CI/CD | [Pipelines](terraform-in-ci-cd-pipelines.md) |
| 17 | Multi-cloud | [AWS · Azure · GCP](multi-cloud-terraform.md) |
| 18 | Kubernetes | [Clusters & providers](kubernetes-infrastructure-with-terraform.md) |
| 19 | Production | [Production patterns](production-terraform-patterns.md) |
| 20 | Troubleshooting | [Troubleshooting](troubleshooting-terraform.md) |

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```
