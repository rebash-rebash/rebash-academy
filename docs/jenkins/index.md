---
title: Overview
description: "Jenkins for Cloud & DevOps Engineers — 16 modules from CI/CD and LTS install through Declarative Pipeline, agents, Docker, shared libraries, security, Kubernetes, Terraform, JCasC, and operations."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-07-31"
category: jenkins
tags:
  - jenkins
  - cicd
  - devops
  - course
comments: false
---

# Jenkins for Cloud & DevOps Engineers

**Duration:** 8–10 weeks · **Difficulty:** Beginner → Advanced
{ .ra-facts }

Production Continuous Integration and Continuous Delivery (CI/CD) with Jenkins Long-Term Support (LTS) — install and operate a controller, author Declarative Pipelines, isolate agents, reuse shared libraries, secure credentials, and integrate Docker, Kubernetes, and Terraform.

!!! tip "Course status"
    Curriculum follows the REBASH Jenkins technology prompt (**16 modules**) and the official [Jenkins User Documentation](https://www.jenkins.io/doc/) (User Handbook, Pipeline syntax, and tutorials). Tutorials use the academy standard with **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Blue Ocean is legacy UI only — Declarative Pipeline is the path. Start with [Introduction to Jenkins and CI/CD](introduction-to-jenkins-and-ci-cd.md).

## 1. Course overview

### Purpose

Treat delivery as software: Jenkinsfiles in source control, agents that protect the controller, reviewable Pipeline changes, and configuration you can recreate with Jenkins Configuration as Code (JCasC).

### Target roles

DevOps · Cloud · Platform · SRE · DevSecOps · Infrastructure Engineer

### Prerequisites

- [Git](../git/index.md) (required)
- [Docker](../docker/index.md) (required for labs)
- [Kubernetes](../kubernetes/index.md) before Module 13
- [Terraform](../terraform/index.md) before Module 14
- Basic cloud knowledge

### Learning arc

| Phase | Modules | Level |
|-------|---------|-------|
| Foundations | 1–3 | Beginner |
| Pipeline core | 4–7 | Intermediate |
| Delivery patterns | 8–10 | Intermediate |
| Hardening & quality | 11–12 | Intermediate → Advanced |
| Platforms & ops | 13–16 | Advanced |

### Capstone outcomes

LTS install · Declarative Jenkinsfiles · agent isolation · shared libraries · security · Docker builds · Kubernetes agents · Terraform plan gates · JCasC · upgrade runbooks

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | CI/CD and Jenkins | [Introduction](introduction-to-jenkins-and-ci-cd.md) |
| 2 | Install LTS | [Docker Compose LTS](installing-jenkins-lts.md) |
| 3 | Jobs, views, folders | [Using Jenkins](using-jenkins-jobs-views-and-folders.md) |
| 4 | Declarative Pipeline | [Pipeline fundamentals](pipeline-fundamentals-declarative.md) |
| 5 | Jenkinsfile in SCM | [SCM Pipelines](jenkinsfile-in-scm.md) |
| 6 | Agents and executors | [Agents · nodes](agents-nodes-and-executors.md) |
| 7 | Multibranch and PRs | [Multibranch](multibranch-pipelines-and-prs.md) |
| 8 | Docker agents | [Docker Pipeline](docker-with-jenkins-pipeline.md) |
| 9 | Shared libraries | [Shared libraries](shared-libraries.md) |
| 10 | Plugins, tools, CLI | [Managing Jenkins](managing-jenkins-plugins-tools-and-cli.md) |
| 11 | Security | [Securing Jenkins](securing-jenkins.md) |
| 12 | Tests and gates | [Testing · reports](testing-reports-and-quality-gates.md) |
| 13 | Kubernetes | [K8s agents · deploys](kubernetes-agents-and-deploys.md) |
| 14 | Terraform | [Terraform Pipelines](terraform-pipelines-in-jenkins.md) |
| 15 | JCasC and scale | [JCasC · ops](jcasc-scaling-and-operations.md) |
| 16 | Troubleshoot · upgrades | [Troubleshooting](troubleshooting-and-upgrades.md) |

## 3. Practice

- [Labs](labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)
- [Roadmap](roadmap.md) · [FAQ](faq.md) · [Certifications](certifications/index.md)

## Diagrams

Excalidraw SVGs live under `docs/assets/excalidraw/` (for example `jenkins-architecture.svg`).

## Related

- [Git](../git/index.md) · [Docker](../docker/index.md) · [Kubernetes](../kubernetes/index.md)
- [Terraform](../terraform/index.md) · [GitHub Actions](../github-actions/index.md) · [GitLab CI/CD](../gitlab/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
