---
title: Overview
description: "GitLab CI/CD learning track — 20 tutorials from pipeline foundations through secure deploys, production patterns, and a Terraform handoff."
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-28"
category: gitlab
tags:
  - cicd
  - gitlab
  - gitlab-ci
comments: false
---

# GitLab CI/CD

GitLab CI from pipeline foundations through secure deployment, production patterns, and a Terraform handoff.

## Overview

The REBASH Academy **GitLab CI/CD** track is a structured, 20-tutorial curriculum published under
`docs/gitlab/`. It teaches **GitLab CI** as the primary platform — `.gitlab-ci.yml`, runners, merge
request pipelines, and deploy environments — with hands-on labs on **GitLab.com** free tier and local
**lint / dry-run** paths (`glab ci lint`, `gitlab-ci-local`).

Other CI tools exist; Jenkins and GitHub Actions are covered in later REBASH tracks, not as peers in
this curriculum.

!!! tip "Prerequisites"
    Complete the [Git](../git/index.md) track first — branching, merge requests, and branch protection
    underpin every pipeline trigger. [Docker](../docker/index.md) becomes essential from Module 3 onward.

## Modules and tutorials

### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to CI/CD and Delivery Models](introduction-to-cicd-and-delivery-models.md) | Beginner | 35 min |
| 2 | [Pipeline Anatomy — Stages, Jobs, and Artifacts](pipeline-anatomy-stages-jobs-and-artifacts.md) | Beginner | 40 min |
| 3 | [GitLab CI Fundamentals](gitlab-ci-fundamentals.md) | Beginner | 50 min |
| 4 | [GitLab Merge Requests and Pipeline Triggers](gitlab-merge-requests-and-pipeline-triggers.md) | Beginner | 45 min |

### Module 2 – Runners and Configuration

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 5 | [GitLab Runners and Executors](gitlab-runners-and-executors.md) | Intermediate | 50 min |
| 6 | [GitLab Runner Tags and Scaling](gitlab-runner-tags-and-scaling.md) | Intermediate | 45 min |
| 7 | [Variables, Secrets, and Credentials](variables-secrets-and-credentials.md) | Intermediate | 50 min |
| 8 | [Triggers, Rules, and Branch Protection](triggers-rules-and-branch-protection.md) | Intermediate | 45 min |

### Module 3 – Build and Quality

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [Building Docker Images in CI](building-docker-images-in-ci.md) | Intermediate | 55 min |
| 10 | [Testing, Reports, and Quality Gates](testing-reports-and-quality-gates.md) | Intermediate | 45 min |
| 11 | [Artifacts, Caches, and Dependencies](artifacts-caches-and-dependencies.md) | Intermediate | 45 min |
| 12 | [Parallelism, Matrix, and Pipeline DAGs](parallelism-matrix-and-pipeline-dags.md) | Intermediate | 50 min |

### Module 4 – Secure Pipelines

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 13 | [Least-Privilege CI Identities](least-privilege-ci-identities.md) | Intermediate | 45 min |
| 14 | [Security Scanning in Pipelines](security-scanning-in-pipelines.md) | Intermediate | 50 min |
| 15 | [Secret Detection and Supply Chain Basics](secret-detection-and-supply-chain-basics.md) | Intermediate | 45 min |
| 16 | [Protected Environments and Approvals](protected-environments-and-approvals.md) | Intermediate | 45 min |

### Module 5 – Deploy and Capstone

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 17 | [GitLab Deployment Patterns](gitlab-deployment-patterns.md) | Intermediate | 50 min |
| 18 | [Kubernetes Deploys from CI](kubernetes-deploys-from-ci.md) | Advanced | 55 min |
| 19 | [GitLab CI Production Patterns](gitlab-ci-production-patterns.md) | Advanced | 45 min |
| 20 | [CI/CD Capstone and Terraform Handoff](cicd-capstone-and-terraform-handoff.md) | Advanced | 60 min |

**Total estimated time:** ~16 hours of hands-on learning

## Learning Objectives

After completing this track, you will be able to:

- [ ] Explain CI, continuous delivery, and deployment models with trunk-based Git workflow
- [ ] Author production `.gitlab-ci.yml` for merge request and default-branch pipelines
- [ ] Configure runners, tags, variables, secrets, triggers, and branch protection
- [ ] Build and scan container images; publish test reports and quality gates
- [ ] Design parallel jobs, matrix builds, and pipeline DAGs with `needs:`
- [ ] Apply least-privilege identities, security scanning, and secret detection in MR pipelines
- [ ] Gate production with protected environments and manual approvals
- [ ] Deploy to Kubernetes from GitLab CI and operate pipelines at production scale
- [ ] Complete a capstone pipeline and hand off infrastructure to [Terraform in CI/CD](../terraform/terraform-in-ci-cd-pipelines.md)

## Who Is This For?

| Audience | Benefit |
|----------|---------|
| **DevOps / Platform engineers** | Operate GitLab CI the way production teams do |
| **Software developers** | Understand pipeline triggers, artefacts, and deploy gates on your merge requests |
| **SREs** | Secure pipelines, observability hooks, and rollback-aware deploy patterns |
| **Career switchers** | Job-ready GitLab CI after the [Git](../git/index.md) track |

## Related Sections

- [Git](../git/index.md) — branching and merge requests pipelines depend on
- [Docker](../docker/index.md) — images built and promoted in Module 3
- [Kubernetes](../kubernetes/index.md) — deploy targets from Module 5
- [Terraform](../terraform/index.md) — [Terraform in CI/CD Pipelines](../terraform/terraform-in-ci-cd-pipelines.md) after the capstone
- [AWS](../aws/index.md) — cloud OIDC roles and deployment targets
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)

## Labs, Quiz, and Cheatsheet

| Resource | Link |
|----------|------|
| Lab — pipeline triage | [CI/CD Pipeline Failure Triage](../labs/cicd-pipeline-triage.md) |
| Lab — Docker secure gate | [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md) |
| Quiz | [CI/CD Fundamentals](../quizzes/cicd-fundamentals.md) |
| Cheat sheet | [CI/CD](../cheatsheets/cicd.md) |
| Interview prep | [CI/CD](../interview/cicd.md) |

Start with [Introduction to CI/CD and Delivery Models](introduction-to-cicd-and-delivery-models.md).
