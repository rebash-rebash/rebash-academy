---
title: Overview
description: "Kubernetes for Cloud & DevOps Engineers — 20 modules from architecture and workloads through security, GitOps, managed clusters, and production operations."
difficulty: intermediate
estimated_time: "10–12 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: kubernetes
tags:
  - kubernetes
  - devops
  - platform
  - course
comments: false
---

# Kubernetes for Cloud & DevOps Engineers

**Duration:** 10–12 weeks · **Difficulty:** Intermediate → Advanced
{ .ra-facts }

Production Kubernetes for Cloud, DevOps, Platform, and SRE — deploy, secure, observe, troubleshoot, and operate clusters (local and managed).

!!! tip "Course status"
    Curriculum follows the REBASH Kubernetes technology prompt (**20 modules**). All **Modules 1–20** tutorials use the academy standard with **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Regenerate with `python3 scripts/generate-excalidraw-svg.py`. Start with [Introduction to Kubernetes and Orchestration](introduction-to-kubernetes-and-orchestration.md).

## 1. Course overview

### Purpose

Deploy and operate production workloads on Kubernetes — from first Pod to GitOps, HA operations, and managed platforms (EKS/AKS/GKE).

### Target roles

Kubernetes Administrator · DevOps · Cloud · Platform · SRE · DevSecOps · Infrastructure Engineer

### Prerequisites

- [Linux](../linux/index.md) · [Networking](../networking/index.md) · [Docker](../docker/index.md)
- [Git](../git/index.md) · Shell · basic Python helpful

### Capstone outcomes

Workloads · Services/Ingress · storage · RBAC · NetPol · autoscaling · Helm · GitOps · backup/DR · managed K8s · operational excellence

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | Fundamentals | [Introduction](introduction-to-kubernetes-and-orchestration.md) · [Architecture](kubernetes-architecture-and-components.md) |
| 2 | Cluster setup | [Install](installing-kubernetes-and-kubectl.md) · [kubectl](kubectl-essentials-and-workflows.md) |
| 3 | Objects | [Pods](pods-the-atomic-unit.md) · [Labels & namespaces](kubernetes-objects-labels-and-namespaces.md) |
| 4 | Workloads | [Deployments](deployments-managing-replicated-pods.md) · [Controllers](workload-controllers-statefulset-daemonset-jobs.md) |
| 5 | Services | [Services & networking](services-and-cluster-networking.md) |
| 6 | Ingress | [Ingress & Gateway API](ingress-and-external-access.md) |
| 7 | Storage | [PV / PVC / CSI](persistent-volumes-and-storage.md) |
| 8 | Configuration | [ConfigMaps & Secrets](configmaps-and-secrets.md) · [Quotas](resource-quotas-and-limit-ranges.md) |
| 9 | Scheduling | [Scheduling](kubernetes-scheduling.md) |
| 10 | Security | [RBAC](rbac-and-kubernetes-security-basics.md) · [Hardening](kubernetes-security-hardening.md) |
| 11 | Networking deep dive | [CNI, DNS, NetPol](kubernetes-networking-deep-dive.md) |
| 12 | Observability | [Monitoring & logging](monitoring-and-logging-in-kubernetes.md) |
| 13 | Autoscaling | [HPA, VPA, CA, KEDA](kubernetes-autoscaling.md) |
| 14 | Helm | [Package management](helm-package-management.md) |
| 15 | GitOps | [GitOps & CI/CD](gitops-and-cicd-with-kubernetes.md) |
| 16 | Platform engineering | [Operators & multi-tenancy](platform-engineering-on-kubernetes.md) |
| 17 | Production operations | [Upgrades, etcd, DR](kubernetes-production-operations.md) |
| 18 | Troubleshooting | [Troubleshooting](troubleshooting-kubernetes-workloads.md) |
| 19 | Managed Kubernetes | [EKS · AKS · GKE](managed-kubernetes-eks-aks-gke.md) |
| 20 | Production Kubernetes | [Excellence](production-kubernetes-excellence.md) |

## 3. Practice

- [Labs](../labs/index.md)

## Diagrams

``` {.bash .ra-terminal title="Terminal"}
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Docker](../docker/index.md) · [Helm](../helm/index.md) · [Argo CD](../argocd/index.md)
- [Kubernetes Engineer path](../learning-paths/kubernetes-engineer/index.md)
