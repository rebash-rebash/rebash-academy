---
title: Learning Roadmap
description: "Structured 20-module learning roadmap for Kubernetes for Cloud & DevOps Engineers."
technology_id: kubernetes
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: kubernetes
tags:
  - kubernetes
  - roadmap
---

# Kubernetes — Learning Roadmap

Follow the course in order:

1. **Course overview** — scope, prerequisites, outcomes  
2. **Modules 1–20** — tutorials in sequence  
3. **Labs / quizzes / projects** — practice  
4. **Capstone** — production Kubernetes platform  
5. **Interview & certifications** — KCNA · CKA · CKAD · CKS  

![Kubernetes architecture](../assets/excalidraw/k8s-architecture.svg)

![GitOps workflow](../assets/excalidraw/k8s-gitops-workflow.svg)

## Modules

| # | Focus | Tutorials |
|---|-------|-----------|
| 1 | Fundamentals | [Introduction](introduction-to-kubernetes-and-orchestration.md) · [Architecture](kubernetes-architecture-and-components.md) |
| 2 | Cluster setup | [Install](installing-kubernetes-and-kubectl.md) · [kubectl](kubectl-essentials-and-workflows.md) |
| 3 | Objects | [Pods](pods-the-atomic-unit.md) · [Labels & namespaces](kubernetes-objects-labels-and-namespaces.md) |
| 4 | Workloads | [Deployments](deployments-managing-replicated-pods.md) · [Controllers](workload-controllers-statefulset-daemonset-jobs.md) |
| 5 | Services | [Services](services-and-cluster-networking.md) |
| 6 | Ingress | [Ingress & Gateway API](ingress-and-external-access.md) |
| 7 | Storage | [PV/PVC/CSI](persistent-volumes-and-storage.md) |
| 8 | Configuration | [ConfigMaps/Secrets](configmaps-and-secrets.md) · [Quotas](resource-quotas-and-limit-ranges.md) |
| 9 | Scheduling | [Scheduling](kubernetes-scheduling.md) |
| 10 | Security | [RBAC](rbac-and-kubernetes-security-basics.md) · [Hardening](kubernetes-security-hardening.md) |
| 11 | Networking deep dive | [CNI/DNS/NetPol](kubernetes-networking-deep-dive.md) |
| 12 | Observability | [Monitoring & logging](monitoring-and-logging-in-kubernetes.md) |
| 13 | Autoscaling | [HPA/VPA/CA/KEDA](kubernetes-autoscaling.md) |
| 14 | Helm | [Package management](helm-package-management.md) |
| 15 | GitOps | [GitOps & CI/CD](gitops-and-cicd-with-kubernetes.md) |
| 16 | Platform engineering | [Operators & tenancy](platform-engineering-on-kubernetes.md) |
| 17 | Production operations | [Upgrades/etcd/DR](kubernetes-production-operations.md) |
| 18 | Troubleshooting | [Troubleshooting](troubleshooting-kubernetes-workloads.md) |
| 19 | Managed Kubernetes | [EKS/AKS/GKE](managed-kubernetes-eks-aks-gke.md) |
| 20 | Production excellence | [Excellence](production-kubernetes-excellence.md) |

## Related depth

- [Health checks](health-checks-probes-and-self-healing.md) · [Namespaces](namespaces-and-resource-management.md) · [HPA/PDB/affinity patterns](production-patterns-hpa-pdb-and-affinity.md) · [Capstone](kubernetes-capstone-and-next-steps.md)

## Diagrams

```bash
python3 scripts/generate-excalidraw-svg.py
```
