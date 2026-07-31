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

![Kubernetes architecture](../assets/excalidraw/k8s-architecture.svg)

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


### Scale and safety together

HPA scales replicas under load; PDBs limit voluntary disruption during drains; affinity/anti-affinity influence placement for resilience. Miscombined, they fight each other (a PDB that cannot be satisfied blocks node upgrades; an uncapped HPA overwhelms databases). Set max replicas thoughtfully, keep replica counts high enough for your PDB, and verify drain behaviour in staging.


### Practice mindset

As you work through this tutorial, narrate *why* each control or command exists — not only *how* to type it. Production incidents are rarely solved by memorising flags; they are solved by connecting symptoms to the architecture (daemon vs kubelet, image vs running container, Service vs Endpoints, volume vs writable layer). After the lab, write three bullet notes in your own words: what you verified, what would break in production if skipped, and what you would monitor next.


### Connecting the lab to production reviews

When a teammate asks “is this ready?”, answer with evidence from this tutorial’s controls: image provenance, privilege level, network exposure, health signals, and teardown/rollback. Copy-pasting a working lab snippet into production without those answers is how quiet misconfigurations become incidents. Prefer small, reviewable changes — one Dockerfile improvement, one RBAC binding, one probe — over large untested stacks.

### Observability while you learn

Get into the habit of watching state while commands run: `docker events` / `kubectl get events`, resource usage, and logs in a second pane. Many failures are timing issues (probes, readiness, volume attach) that disappear if you only look at the final steady state. Capturing a short timeline of what you saw will also make your Troubleshooting section notes far more valuable later.

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

**Expected result:** The commands succeed and produce the outcomes described in this step.


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

**Expected result:** The commands succeed and produce the outcomes described in this step.


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

**Expected result:** The commands succeed and produce the outcomes described in this step.


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

**Expected result:** The commands succeed and produce the outcomes described in this step.


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

**Expected result:** The commands succeed and produce the outcomes described in this step.


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

**Expected result:** The commands succeed and produce the outcomes described in this step.


Document in GitOps values; validate in staging before prod.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| HPA | HorizontalPodAutoscaler exists and reacts to load or metrics as labbed |
| PDB | PodDisruptionBudget admitted and visible via kubectl |
| Affinity | Scheduling rules affect Pod placement as documented |
| Cleanup | HPA/PDB/demo workloads removed |

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

- Cap HPA max replicas to protect downstream dependencies and your cloud bill
- Pair PodDisruptionBudgets with enough replicas — a PDB of minAvailable=1 on a single replica blocks drains forever or forces unsafe bypasses
- Use affinity/anti-affinity to improve resilience, not to pin everything to one tainted node
- Prevent autoscaling on insecure images by gating deploys with admission policy
- Watch that scale-up does not bypass Pod Security or quota unexpectedly
- Test drain/eviction behaviour in staging before relying on PDBs in production


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
