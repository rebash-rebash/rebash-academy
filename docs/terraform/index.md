---
title: Overview
description: "Terraform for Cloud & DevOps Engineers — 20 modules from IaC fundamentals through HCL, state, modules, security, CI/CD, multi-cloud, Kubernetes, and production operations."
difficulty: intermediate
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: terraform
tags:
  - terraform
  - infrastructure-as-code
  - devops
  - course
comments: false
---

# Terraform for Cloud & DevOps Engineers

**Duration:** 8–10 weeks · **Difficulty:** Intermediate → Advanced
{ .ra-facts }

Production Infrastructure as Code (IaC) with [Terraform](https://developer.hashicorp.com/terraform/docs) — versioned HCL, reviewable plans, remote state, reusable modules, and CI/CD gates for Cloud, DevOps, Platform, and SRE roles.

!!! tip "Course status"
    **Ready** — 20 modules with production-grade labs: Docker provider stacks locally, **kind** for Kubernetes, LocalStack or AWS sandbox for cloud APIs, and real `terraform apply` with operational proof. Curriculum follows [HashiCorp Terraform documentation](https://developer.hashicorp.com/terraform/docs). Start with [Introduction to Terraform and IaC](introduction-to-terraform-and-iac.md).

## 1. Course overview

### Purpose

Treat infrastructure like software: declarative configuration, peer-reviewed plans, encrypted remote state, composable modules, and automated validation — from first `terraform apply` through multi-cloud platforms and production troubleshooting.

### Target roles

Cloud Engineer · DevOps · Platform · SRE · Infrastructure · DevSecOps

### Prerequisites

- [Linux](../linux/index.md) · [Networking](../networking/index.md)
- [Git](../git/index.md) · [Docker](../docker/index.md)
- Basic cloud knowledge (AWS, Azure, or Google Cloud)
- [GitHub Actions](../github-actions/index.md) or [GitLab CI](../gitlab/index.md) before Module 16

### Learning arc

| Phase | Modules | Level |
|-------|---------|-------|
| Foundations | 1–4 | Beginner |
| Core HCL & providers | 5–8 | Intermediate |
| Modules & expressions | 9–11 | Intermediate |
| Workspaces & platform | 12–14 | Advanced |
| Security & automation | 15–16 | Advanced |
| Multi-cloud & Kubernetes | 17–18 | Advanced |
| Production & ops | 19–20 | Advanced |

### Capstone outcomes

Reusable modules · remote state · pinned providers · CI plan gates · multi-cloud roots · Kubernetes platform wiring · production repo layout · structured troubleshooting

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
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

## 3. Practice

- [Labs](../labs/index.md)
- [Learning roadmap](roadmap.md) · [FAQ](faq.md)

## Related

- [AWS](../aws/index.md) · Azure · [GCP](../gcp/index.md)
- [Kubernetes](../kubernetes/index.md) · [Helm](../helm/index.md) · [Ansible](../ansible/index.md)
- [DevOps Engineer path](../learning-paths/devops-engineer/index.md)
