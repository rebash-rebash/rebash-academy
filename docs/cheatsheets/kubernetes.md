---
title: "Kubernetes Cheat Sheet"
description: "Quick-reference commands and patterns for the REBASH Academy Kubernetes track."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - kubernetes
comments: false
---

# Kubernetes Cheat Sheet

Scannable commands and patterns for the [Kubernetes track](../kubernetes/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Quick reference

| Area | Commands / notes |
|------|------------------|
| Context | `kubectl config get-contexts`; `kubectl cluster-info` |
| Get | `kubectl get pods -A`; `-o wide`; `-w` |
| Describe | `kubectl describe pod NAME`; Events section first |
| Logs | `kubectl logs deploy/NAME -f`; `--previous` |
| Apply | `kubectl apply -f`; `diff -f`; `delete -f` |
| Workloads | Deployment, StatefulSet, DaemonSet, Job/CronJob |
| Expose | Service ClusterIP/NodePort/LB; Ingress |
| Config | ConfigMap / Secret; envFrom; mounts |
| Rollout | `kubectl rollout status`; `undo`; `restart` |
| Debug | `kubectl get events --sort-by=.lastTimestamp` |

## Common mistakes

- Copy-pasting without reading expected output
- Skipping cleanup (leftover containers, state, or temp files)
- Mixing production credentials into lab shells

## Related

- Track: [Kubernetes](../kubernetes/index.md)
- Start: [Kubernetes introduction](../kubernetes/introduction-to-kubernetes-and-orchestration.md)
- Interview bank: [Kubernetes interview prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
