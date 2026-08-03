---
title: Overview
description: "Helm for Kubernetes Engineers — 12 modules covering charts, templates, values, releases, security, GitOps, and production practices."
difficulty: intermediate
estimated_time: "3–4 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: helm
tags:
  - helm
  - kubernetes
  - devops
  - course
comments: false
---

# Helm for Kubernetes Engineers

**Duration:** 3–4 weeks · **Difficulty:** Intermediate
{ .ra-facts }

Production Helm for Kubernetes Administrators, DevOps, Platform, and SRE — create, release, secure, and GitOps-deploy charts.

!!! tip "Course status"
    Curriculum follows the REBASH Helm technology prompt (**12 modules**). Tutorials use the academy standard with **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Regenerate with `python3 scripts/generate-excalidraw-svg.py`. Start with [Introduction to Helm](introduction-to-helm.md).

## 1. Course overview

### Purpose

Ship Kubernetes applications as versioned packages — charts you can lint, test, release, roll back, and sync with GitOps.

### Target roles

Kubernetes Administrator · DevOps · Platform · SRE · DevSecOps · Cloud Engineer

### Prerequisites

- [Kubernetes](../kubernetes/index.md) · [Docker](../docker/index.md)
- [Git](../git/index.md) · Linux fundamentals

### Capstone outcomes

Production charts · reusable templates · OCI publishing · multi-env values · GitOps · security validation · troubleshooting

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | Fundamentals | [Introduction](introduction-to-helm.md) · [Architecture](helm-architecture-and-components.md) |
| 2 | Installing Helm | [Install & repos](installing-helm-and-repositories.md) |
| 3 | Working with charts | [Chart structure](working-with-helm-charts.md) |
| 4 | Templates | [Go templating](helm-templates-and-go-templating.md) |
| 5 | Values | [Values & overrides](helm-values-and-overrides.md) |
| 6 | Dependencies | [Chart dependencies](helm-chart-dependencies.md) |
| 7 | Releases | [Release lifecycle](helm-releases-and-lifecycle.md) |
| 8 | Testing | [Testing & validation](helm-testing-and-validation.md) |
| 9 | Security | [Helm security](helm-security.md) |
| 10 | GitOps | [GitOps integration](helm-gitops-integration.md) |
| 11 | Production | [Production practices](production-helm-practices.md) |
| 12 | Troubleshooting | [Troubleshooting](troubleshooting-helm.md) |

## 3. Practice

- [Labs](../labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)

## Diagrams

```bash title="Terminal"
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Kubernetes](../kubernetes/index.md) · [Argo CD](../argocd/index.md) · [GitOps (Git)](../git/gitops-fundamentals.md)
- [Kubernetes Engineer path](../career-paths/kubernetes-engineer/index.md)
