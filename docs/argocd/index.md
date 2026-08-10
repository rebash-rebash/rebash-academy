---
title: Overview
description: "Argo CD for Cloud & DevOps Engineers — 16 modules covering GitOps, Applications, sync, Helm, Kustomize, ApplicationSets, security, and production operations."
difficulty: intermediate
estimated_time: "5–7 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: argocd
tags:
  - argocd
  - gitops
  - kubernetes
  - devops
  - course
comments: false
---

# Argo CD for Cloud & DevOps Engineers

**Duration:** 5–7 weeks · **Difficulty:** Intermediate → Advanced
{ .ra-facts }

Declarative GitOps continuous delivery for Kubernetes with [Argo CD](https://github.com/argoproj/argo-cd) — Applications, sync policies, Helm and Kustomize sources, ApplicationSets, multi-cluster, and production operations.

!!! tip "Course status"
    Curriculum follows the REBASH Argo CD technology prompt (**16 modules**). Labs use create-file style (YAML fences, then `kubectl` / `argocd` verify). Diagrams under `docs/assets/excalidraw/`. Start with [Introduction to GitOps and Argo CD](introduction-to-gitops-and-argo-cd.md). Official docs: [argo-cd.readthedocs.io](https://argo-cd.readthedocs.io/en/stable/).

## 1. Course overview

### Purpose

Keep Kubernetes clusters aligned with Git as the source of truth — pull-based delivery that is auditable, reversible, and operable by platform teams.

### Target roles

DevOps · Platform · Cloud · SRE · Kubernetes Administrator · DevSecOps

### Prerequisites

- [Kubernetes](../kubernetes/index.md) · [Helm](../helm/index.md) · [Git](../git/index.md)
- [Docker](../docker/index.md) · CI basics ([GitHub Actions](../github-actions/index.md) or [GitLab CI](../gitlab/index.md))
- Local kind or minikube for install and sync labs

### Capstone outcomes

GitOps layouts · Applications and AppProjects · auto-sync and self-heal · Helm/Kustomize · ApplicationSets · multi-cluster · RBAC/SSO · CI promotion · troubleshooting drift

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | GitOps fundamentals | [Introduction](introduction-to-gitops-and-argo-cd.md) |
| 2 | Architecture | [Components](argo-cd-architecture-and-components.md) |
| 3 | Installation | [Install Argo CD](installing-argo-cd.md) |
| 4 | Applications | [Applications and Projects](argo-cd-applications-and-projects.md) |
| 5 | Repositories | [Repos and credentials](argo-cd-repositories-and-credentials.md) |
| 6 | Synchronisation | [Sync, options, and hooks](synchronisation-sync-options-and-hooks.md) |
| 7 | Helm | [Helm with Argo CD](helm-with-argo-cd.md) |
| 8 | Kustomize | [Kustomize with Argo CD](kustomize-with-argo-cd.md) |
| 9 | ApplicationSets | [ApplicationSets](applicationsets.md) |
| 10 | Multi-cluster | [Multi-cluster GitOps](multi-cluster-gitops.md) |
| 11 | Security | [RBAC and SSO](argo-cd-security-rbac-and-sso.md) |
| 12 | Notifications | [Notifications](argo-cd-notifications.md) |
| 13 | Progressive delivery | [Sync windows and delivery](progressive-delivery-and-sync-windows.md) |
| 14 | CI/CD | [CI/CD integration](ci-cd-integration-with-argo-cd.md) |
| 15 | Production | [Production GitOps](production-gitops-with-argo-cd.md) |
| 16 | Troubleshooting | [Troubleshooting](troubleshooting-argo-cd.md) |

## 3. Practice

- [Labs](../labs/index.md)
- [Learning roadmap](roadmap.md) · [FAQ](faq.md)

## Related

- [Kubernetes GitOps](../kubernetes/gitops-and-cicd-with-kubernetes.md) · [Helm GitOps](../helm/helm-gitops-integration.md)
- [Git GitOps fundamentals](../git/gitops-fundamentals.md)
- [Kubernetes Engineer path](../learning-paths/kubernetes-engineer/index.md)
