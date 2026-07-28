---
title: Production Patterns — HPA, PDB, and Affinity
description: Scale workloads with Horizontal Pod Autoscaler, protect availability with Pod Disruption Budgets, and control placement with affinity and topology spread.
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: kubernetes
tags:
  - kubernetes
  - hpa
  - pdb
  - affinity
  - production
prerequisites:
  - GitOps and CI/CD with Kubernetes
  - Health Checks, Probes, and Self-Healing
  - Deployments — Managing Replicated Pods
comments: false
---

# Production Patterns — HPA, PDB, and Affinity

## Overview

Running two replicas is not production-ready. Real clusters face traffic spikes, node maintenance, and hardware failures simultaneously. **Horizontal Pod Autoscaler (HPA)** scales replicas on metrics. **Pod Disruption Budgets (PDB)** ensure voluntary disruptions (drains, upgrades) never take down too many pods at once. **Affinity and topology spread** place workloads on the right nodes and spread them across failure domains.

This tutorial teaches the production control loop: scale out under load, scale in safely, survive node drains, and avoid single points of failure.

This is **Tutorial 17** in **Module 6: Production** of the REBASH Academy Kubernetes series.

## Prerequisites

- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md)
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- [Deployments — Managing Replicated Pods](deployments-managing-replicated-pods.md)
- [Namespaces and Resource Management](namespaces-and-resource-management.md)
- Cluster with **metrics-server** installed (required for CPU/memory HPA)
- Optional: Prometheus Adapter for custom metrics HPA

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Configure HPA on CPU, memory, and custom metrics
- [ ] Define PDBs that balance availability with cluster maintenance
- [ ] Apply node affinity, pod affinity, and anti-affinity rules
- [ ] Use topology spread constraints for zone and host distribution
- [ ] Combine resource requests with autoscaling for stable scheduling
- [ ] Validate scaling and disruption behaviour before production cutover

## Architecture

```d2
direction: down

Traffic: Traffic {
        USERS: "Users / Ingress"
    }
    Control: Control {
        HPA: "HPA controller"
        METRICS: "metrics-server / Prometheus"
        PDB: "PDB policy"
    }
    Workload: Workload {
        DEP: "Deployment — api"
        P1: Pod
        P2: Pod
        P3: Pod
    }
    Nodes: Nodes {
        N1: "Node AZ-a"
        N2: "Node AZ-b"
        N3: "Node AZ-c"
    }
    Traffic.USERS -> Workload.DEP
    Control.METRICS -> Control.HPA
    Control.HPA -> Workload.DEP: "scale replicas"
    Control.PDB -> Workload.DEP: "limits evictions"
    Workload.DEP -> Workload.P1
    Workload.P1 -> Nodes.N1
    Workload.P2 -> Nodes.N2
    Workload.P3 -> Nodes.N3
```

## Theory

### Horizontal Pod Autoscaler

HPA adjusts `Deployment.spec.replicas` based on observed metrics.

| Metric source | Use case |
|---------------|----------|
| CPU utilization | General web APIs |
| Memory utilization | Caches, JVM workloads |
| Custom metrics | Queue depth, RPS, latency |
| External metrics | CloudWatch, Pub/Sub backlog |

HPA formula (simplified):

```text
desiredReplicas = ceil(currentReplicas × (currentMetric / targetMetric))
```

Requirements for stable HPA:

1. **Resource requests** set on containers — HPA compares usage against requests
2. **metrics-server** running — provides CPU/memory via Metrics API
3. **Readiness probes** — only ready pods receive traffic after scale-up

Default behaviour: scale-up is aggressive (add pods quickly); scale-down has stabilization windows to prevent flapping.

### Pod Disruption Budget

Voluntary disruptions include node drains, cluster upgrades, and `kubectl delete pod`. **PDB** limits how many pods can be unavailable during these events.

| Field | Meaning |
|-------|---------|
| `minAvailable` | Minimum pods that must stay running (absolute or %) |
| `maxUnavailable` | Maximum pods that can be down during disruption |

PDB applies to pods matching its selector. It does **not** stop involuntary failures (node crash) — pair PDB with replica count and spread constraints.

Example: 5 replicas with `minAvailable: 3` allows at most 2 simultaneous evictions during a drain.

### Affinity and anti-affinity

| Type | Purpose |
|------|---------|
| **nodeAffinity** | Schedule on nodes with labels (GPU, SSD, zone) |
| **podAffinity** | Co-locate with another pod (same node) |
| **podAntiAffinity** | Spread away from another pod (avoid same node) |

**Required** rules (`requiredDuringSchedulingIgnoredDuringExecution`) are hard constraints — pod stays Pending if unsatisfied.

**Preferred** rules (`preferredDuringSchedulingIgnoredDuringExecution`) are soft — scheduler tries but may violate under pressure.

### Topology spread constraints

Modern alternative to anti-affinity for even distribution:

```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: votestack-api
```

`maxSkew: 1` means no zone can have more than one pod extra compared to another zone.

## Hands-on Lab

Labs extend the **VoteStack api** Deployment from [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md).

### Lab 1 — Verify metrics-server

```bash
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
kubectl top pods -n votestack
```

If missing on kind/minikube:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
# kind may need --kubelet-insecure-tls flag in metrics-server args
```

### Lab 2 — Baseline Deployment with resource requests

Ensure the api Deployment sets requests (HPA prerequisite):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: votestack-api
  namespace: votestack
spec:
  replicas: 2
  selector:
    matchLabels:
      app: votestack-api
  template:
    metadata:
      labels:
        app: votestack-api
    spec:
      containers:
        - name: api
          image: ghcr.io/org/votestack-api:abc1234
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 256Mi
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            periodSeconds: 10
```

Apply and confirm: `kubectl get deploy votestack-api -n votestack`

### Lab 3 — Create Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: votestack-api
  namespace: votestack
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: votestack-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

```bash
kubectl apply -f hpa-api.yaml
kubectl get hpa -n votestack
kubectl describe hpa votestack-api -n votestack
```

Load test to trigger scale-up:

```bash
kubectl run -it loadgen --rm --image=busybox --restart=Never -- \
  sh -c "while true; do wget -q -O- http://votestack-api.votestack.svc:8080/api/polls; done"
# Watch replicas in another terminal
kubectl get hpa,pods -n votestack -w
```

### Lab 4 — Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: votestack-api
  namespace: votestack
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: votestack-api
```

```bash
kubectl apply -f pdb-api.yaml
kubectl get pdb -n votestack
```

Simulate drain with PDB active:

```bash
NODE=$(kubectl get nodes -o jsonpath='{.items[0].metadata.name}')
kubectl drain "$NODE" --ignore-daemonsets --delete-emptydir-data --dry-run=client
# Real drain respects PDB — may block if minAvailable would be violated
```

### Lab 5 — Topology spread across zones

Label nodes (cloud clusters often have zone labels pre-set):

```yaml
# Add to Deployment pod template spec
spec:
  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: ScheduleAnyway
      labelSelector:
        matchLabels:
          app: votestack-api
    - maxSkew: 1
      topologyKey: kubernetes.io/hostname
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app: votestack-api
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - weight: 100
          podAffinityTerm:
            labelSelector:
              matchLabels:
                app: votestack-api
            topologyKey: kubernetes.io/hostname
```

Verify distribution:

```bash
kubectl get pods -n votestack -o wide -l app=votestack-api
```

### Lab 6 — Worker queue-depth HPA (custom metrics)

For the VoteStack **worker**, scale on Redis queue length via Prometheus Adapter:

```yaml
# prometheus-adapter config snippet — queue depth metric
rules:
  - seriesQuery: 'redis_list_length{list="votes"}'
    resources:
      overrides:
        namespace: { resource: "namespace" }
        pod: { resource: "pod" }
    name:
      matches: "redis_list_length"
      as: "redis_votes_queue_depth"
    metricsQuery: 'redis_list_length{list="votes",<<.LabelMatchers>>}'
```

HPA referencing custom metric:

```yaml
metrics:
  - type: Pods
    pods:
      metric:
        name: redis_votes_queue_depth
      target:
        type: AverageValue
        averageValue: "30"
```

Document in GitOps values; validate in staging before prod.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

```bash
# HPA inspection
kubectl autoscale deployment votestack-api --cpu-percent=70 --min=2 --max=10 -n votestack
kubectl get hpa -n votestack -w
kubectl describe hpa votestack-api -n votestack

# PDB
kubectl get pdb -A
kubectl describe pdb votestack-api -n votestack

# Scheduling debug
kubectl describe pod <pod> -n votestack | grep -A5 Events
kubectl get events -n votestack --sort-by='.lastTimestamp'

# VPA note (optional — different from HPA)
# Vertical Pod Autoscaler adjusts requests/limits, not replica count
```

| Resource | API version | Scope |
|----------|-------------|-------|
| HPA | `autoscaling/v2` | Namespaced |
| PDB | `policy/v1` | Namespaced |
| VPA | `autoscaling.k8s.io/v1` | Namespaced (optional add-on) |

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "HPA without resource requests"
    HPA cannot compute CPU utilization percentage if requests are unset — pods show `<unknown>` metrics.

!!! warning "PDB minAvailable equals replica count"
    With 2 replicas and `minAvailable: 2`, no voluntary eviction is ever allowed — node drains hang forever.

!!! warning "Hard anti-affinity on small clusters"
    `required` anti-affinity with 3 replicas on 2 nodes leaves pods Pending — use `preferred` or add nodes.

!!! warning "Scaling on CPU alone for I/O-bound apps"
    APIs waiting on postgres show low CPU while latency spikes — add custom metrics or RPS-based scaling.

!!! warning "Ignoring scale-down stabilization"
    Immediate scale-down after a spike causes thrashing — tune `stabilizationWindowSeconds`.

## Best Practices

!!! tip "Set requests from production profiling"
    Use VPA recommender or load-test data — HPA and scheduler depend on accurate requests.

!!! tip "PDB maxUnavailable for large deployments"
    With 50+ replicas, `maxUnavailable: 10%` is easier to reason about than fixed `minAvailable`.

!!! tip "Combine spread + PDB + HPA"
    These controls interact — test node drain during peak load in staging.

!!! tip "Use HPA v2 only"
    `autoscaling/v2` supports multiple metrics and behaviour policies — avoid deprecated v1.

!!! tip "Document min/max replica rationale"
    `maxReplicas` prevents runaway scaling costs; `minReplicas` ensures HA baseline — record both in runbooks.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| HPA shows `<unknown>` | metrics-server down or no requests | Fix metrics-server; set resource requests |
| Pods Pending after spread rules | Insufficient nodes/zones | Relax `whenUnsatisfiable` or add capacity |
| Drain blocked | PDB too strict | Temporarily adjust PDB or add replicas |
| HPA never scales down | stabilization window / high min | Review behaviour policy and actual load |
| Flapping replicas | Target too aggressive | Raise target CPU%; add scale-down delay |
| Custom metric missing | Prometheus Adapter misconfigured | Check adapter logs and metric discovery |

## Summary

- **HPA** scales replica count on CPU, memory, or custom metrics — requires resource requests and metrics-server
- **PDB** protects availability during voluntary disruptions like node drains and upgrades
- **Affinity and topology spread** control pod placement across nodes and availability zones
- Production workloads combine all three: scale under load, survive maintenance, distribute across failure domains
- Tune scale-down behaviour to prevent flapping; validate with load tests and drain simulations
- Next: [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md)

## Interview Questions

1. How does HPA calculate desired replica count for CPU utilization?
2. Why must containers define resource requests for CPU-based HPA?
3. What is the difference between voluntary and involuntary pod disruption?
4. When would you use `minAvailable` vs `maxUnavailable` in a PDB?
5. Explain hard vs soft pod anti-affinity.
6. What problem do topology spread constraints solve?
7. How would you autoscale a worker based on queue depth?
8. Why does HPA scale-down have a stabilization window?
9. What happens if PDB blocks a node drain during a security patch?
10. How do HPA and Cluster Autoscaler interact?

??? tip "Sample Answers (Questions 1, 4, and 10)"

    **Q1 — HPA CPU formula:** HPA reads current average CPU utilization across pods (as percentage of configured requests). `desiredReplicas = ceil(currentReplicas × (currentUtilization / targetUtilization))`. Example: 4 pods at 140% average with 70% target → ceil(4 × 2) = 8 replicas.

    **Q4 — minAvailable vs maxUnavailable:** `minAvailable: 3` guarantees at least 3 pods stay up during disruption — good when you think in terms of absolute HA floor. `maxUnavailable: 1` allows only one pod down at a time — intuitive for rolling maintenance on small deployments. Use percentages at scale.

    **Q10 — HPA + Cluster Autoscaler:** HPA adds pods when metrics exceed targets. If no node has capacity, pods stay Pending. Cluster Autoscaler detects Pending pods and provisions new nodes (on supported cloud providers). Without Cluster Autoscaler, HPA hits scheduling ceiling.

## Related Tutorials

- [GitOps and CI/CD with Kubernetes](gitops-and-cicd-with-kubernetes.md) *(previous)*
- [Monitoring and Logging in Kubernetes](monitoring-and-logging-in-kubernetes.md) *(next)*
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- [Namespaces and Resource Management](namespaces-and-resource-management.md)
- [Production Docker Patterns](../docker/production-docker-patterns.md)
- [Kubernetes – Category Overview](index.md)
- Cheat sheet: [Kubernetes Cheat Sheet](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes Interview Prep](../interview/kubernetes.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Kubernetes – Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [Kubernetes – Pod Disruption Budgets](https://kubernetes.io/docs/tasks/run-application/configure-pdb/)
- [Kubernetes – Assign Pods to Nodes (affinity)](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Kubernetes – Topology Spread Constraints](https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/)
- [Prometheus Adapter for Kubernetes](https://github.com/kubernetes-sigs/prometheus-adapter)
