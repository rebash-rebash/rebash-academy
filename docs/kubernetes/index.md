---
title: Overview
description: Kubernetes learning track — 20 tutorials from orchestration fundamentals to production GitOps, security, and capstone.
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - orchestration
comments: false
---

# Kubernetes

Deploy, scale, and operate containerized workloads at cluster scale — from your first Pod to production GitOps, autoscaling, and security hardening.

## Overview

The REBASH Academy **Kubernetes** track is a structured, 20-tutorial curriculum for DevOps engineers, SREs, and platform teams. Kubernetes is the standard orchestration layer for containers in production. Each tutorial follows our [documentation standards](../about.md#documentation-standards) with theory, hands-on labs, YAML manifests, best practices, and interview questions.

!!! tip "Learning Path"
    Complete the [Docker track](../docker/index.md) first — especially [From Docker to Kubernetes](../docker/from-docker-to-kubernetes.md). Linux and networking fundamentals from the [DevOps learning path](../learning-paths/index.md) are strongly recommended.

## Curriculum Plan

```d2
direction: down

M1: "Module 1: Foundations"
    M2: "Module 2: Workloads"
    M1 -> M2
    M3: "Module 3: Configuration & Storage"
    M2 -> M3
    M4: "Module 4: Networking & Operations"
    M3 -> M4
    M5: "Module 5: Security & Tooling"
    M4 -> M5
    M6: "Module 6: Production"
    M5 -> M6
```

### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to Kubernetes and Orchestration](introduction-to-kubernetes-and-orchestration.md) | Beginner | 30 min |
| 2 | [Kubernetes Architecture and Components](kubernetes-architecture-and-components.md) | Beginner | 35 min |
| 3 | [Installing Kubernetes and kubectl](installing-kubernetes-and-kubectl.md) | Beginner | 40 min |

### Module 2 – Workloads

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 4 | [kubectl Essentials and Workflows](kubectl-essentials-and-workflows.md) | Beginner | 35 min |
| 5 | [Pods — The Atomic Unit](pods-the-atomic-unit.md) | Beginner | 40 min |
| 6 | [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md) | Intermediate | 45 min |

### Module 3 – Configuration & Storage

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 7 | [Services and Cluster Networking](services-and-cluster-networking.md) | Intermediate | 45 min |
| 8 | [ConfigMaps and Secrets](configmaps-and-secrets.md) | Intermediate | 40 min |
| 9 | [Persistent Volumes and Storage](persistent-volumes-and-storage.md) | Intermediate | 45 min |

### Module 4 – Networking & Operations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 10 | [Ingress and External Access](ingress-and-external-access.md) | Intermediate | 45 min |
| 11 | [Namespaces and Resource Management](namespaces-and-resource-management.md) | Intermediate | 35 min |
| 12 | [Health Checks — Probes and Self-Healing](health-checks-probes-and-self-healing.md) | Intermediate | 40 min |

### Module 5 – Security & Tooling

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 13 | [RBAC and Kubernetes Security Basics](rbac-and-kubernetes-security-basics.md) | Intermediate | 45 min |
| 14 | [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md) | Advanced | 50 min |
| 15 | [Helm — Package Management](helm-package-management.md) | Intermediate | 45 min |

### Module 6 – Production

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 16 | [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md) | Advanced | 50 min |
| 17 | [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md) | Advanced | 55 min |
| 18 | [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md) | Advanced | 50 min |
| 19 | [Kubernetes Security Hardening](kubernetes-security-hardening.md) | Advanced | 55 min |
| 20 | [Kubernetes Capstone and Next Steps](kubernetes-capstone-and-next-steps.md) | Advanced | 45 min |

## Learning Objectives

By completing this track, you will be able to:

- [ ] Explain Kubernetes architecture and run a local cluster with minikube or kind
- [ ] Deploy and manage workloads with Deployments, Services, and Ingress
- [ ] Configure applications with ConfigMaps, Secrets, and persistent storage
- [ ] Implement health probes, RBAC, and systematic troubleshooting workflows
- [ ] Package releases with Helm and operate clusters with GitOps patterns
- [ ] Apply production patterns: HPA, PDB, affinity, monitoring, and security hardening

## Related Sections

Continue to [Terraform](../terraform/index.md) for infrastructure as code, [GitLab CI/CD](../gitlab/index.md) for pipelines, or browse [Learning Paths](../learning-paths/index.md).
