---
title: "Quiz — Kubernetes Fundamentals"
description: "40-question Kubernetes quiz covering Pods, Deployments, Services, probes, RBAC, storage, troubleshooting, and production design."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - kubernetes
  - assessment
comments: false
---

# Quiz — Kubernetes Fundamentals

## Quiz Overview

Validate Kubernetes fundamentals used on the job: workload APIs, networking abstractions, probes, config/storage, RBAC, and production operations judgement.

| Attribute | Value |
|-----------|--------|
| Topic | Kubernetes |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice. Score yourself honestly — gaps are the point.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Explain Pods, Deployments, Services, and Namespaces
- [ ] Distinguish liveness vs readiness failure behaviour
- [ ] Use kubectl for logs, exec, and describe-driven triage
- [ ] Diagnose ImagePullBackOff, CrashLoopBackOff, scheduling, and probe mistakes
- [ ] Choose sensible production patterns (HPA, PDB, security baselines)

## Section 1 — Fundamentals

### Question 1

What is a Pod in Kubernetes?

**Difficulty:** Beginner

**Options:**

- **A.** A physical rack
- **B.** The smallest deployable unit: one or more containers sharing network namespace and volumes
- **C.** A cloud region
- **D.** A Helm repository only

??? success "Reveal answer"
    **Correct answer: B**

    Pods group containers with shared networking/storage abstractions.

    **Related concepts**

    - Pods

### Question 2

Which control plane component schedules Pods onto nodes?

**Difficulty:** Beginner

**Options:**

- **A.** kube-scheduler
- **B.** CoreDNS only
- **C.** etcd alone
- **D.** Ingress controller

??? success "Reveal answer"
    **Correct answer: A**

    kube-scheduler assigns Pods to nodes.

    **Related concepts**

    - Control plane
    - kube-scheduler

### Question 3

What does a Deployment manage?

**Difficulty:** Beginner

**Options:**

- **A.** PersistentVolumes directly
- **B.** ReplicaSets/Pods for declarative, rolling updates of stateless workloads
- **C.** Only Nodes
- **D.** etcd snapshots

??? success "Reveal answer"
    **Correct answer: B**

    Deployments own ReplicaSets and provide rollout strategies.

    **Related concepts**

    - Deployment
    - ReplicaSet

### Question 4

A ClusterIP Service provides:

**Difficulty:** Beginner

**Options:**

- **A.** A public load balancer on every cloud by default
- **B.** A stable virtual IP/DNS name for Pods inside the cluster
- **C.** Physical disk attachment
- **D.** TLS certificates automatically

??? success "Reveal answer"
    **Correct answer: B**

    ClusterIP is internal service discovery and load balancing.

    **Related concepts**

    - Service
    - ClusterIP

### Question 5

What happens when a liveness probe fails repeatedly?

**Difficulty:** Beginner

**Options:**

- **A.** Pod is removed from Service endpoints only
- **B.** kubelet restarts the container
- **C.** The node is cordoned automatically
- **D.** etcd is compacted

??? success "Reveal answer"
    **Correct answer: B**

    Failed liveness → container restart. Failed readiness → remove from endpoints.

    **Related concepts**

    - livenessProbe

### Question 6

What happens when a readiness probe fails?

**Difficulty:** Beginner

**Options:**

- **A.** Container is always killed immediately
- **B.** Pod is taken out of Service endpoints until ready again
- **C.** Namespace is deleted
- **D.** API server restarts

??? success "Reveal answer"
    **Correct answer: B**

    Readiness controls whether the Pod receives traffic via Services.

    **Related concepts**

    - readinessProbe
    - Endpoints

### Question 7

ConfigMaps are primarily for:

**Difficulty:** Beginner

**Options:**

- **A.** Storing non-sensitive configuration data
- **B.** Storing private keys as best practice
- **C.** Replacing etcd
- **D.** Billing data only

??? success "Reveal answer"
    **Correct answer: A**

    Non-sensitive config belongs in ConfigMaps; use Secrets for sensitive material.

    **Related concepts**

    - ConfigMap

### Question 8

kubectl apply is associated with which management style?

**Difficulty:** Beginner

**Options:**

- **A.** Imperative only
- **B.** Declarative configuration applied to the cluster
- **C.** SSH into nodes to edit binaries
- **D.** Manual etcd edits

??? success "Reveal answer"
    **Correct answer: B**

    apply reconciles desired manifests with live objects.

    **Related concepts**

    - kubectl apply

### Question 9

Namespaces are used to:

**Difficulty:** Beginner

**Options:**

- **A.** Partition cluster resources and scope names for multi-tenancy/environments
- **B.** Replace VPCs in all clouds
- **C.** Store container images
- **D.** Disable RBAC

??? success "Reveal answer"
    **Correct answer: A**

    Namespaces scope objects and policies within a cluster.

    **Related concepts**

    - Namespaces

### Question 10

Which object requests durable storage for a Pod?

**Difficulty:** Beginner

**Options:**

- **A.** Ingress
- **B.** PersistentVolumeClaim (bound to a PersistentVolume)
- **C.** ServiceAccount token only
- **D.** HorizontalPodAutoscaler

??? success "Reveal answer"
    **Correct answer: B**

    PVCs request storage; PVs are the provisioned volumes.

    **Related concepts**

    - PVC
    - PV

## Section 2 — Practical Knowledge

### Question 11

Which command tails logs from a Pod named `api-x` in namespace `prod`?

**Difficulty:** Beginner

**Options:**

- **A.** kubectl logs -n prod api-x -f
- **B.** docker compose logs
- **C.** journalctl -u api-x
- **D.** helm uninstall api-x

??? success "Reveal answer"
    **Correct answer: A**

    kubectl logs with -n and -f follows Pod logs.

    **Related concepts**

    - kubectl logs

### Question 12

You need to open a shell in a running container:

**Difficulty:** Beginner

**Options:**

- **A.** kubectl exec -it -n <ns> <pod> -- sh
- **B.** kubectl delete pod
- **C.** kubectl cordon
- **D.** kubectl proxy only

??? success "Reveal answer"
    **Correct answer: A**

    exec attaches a command/shell into the container.

    **Related concepts**

    - kubectl exec

### Question 13

ImagePullBackOff most often means:

**Difficulty:** Intermediate

**Options:**

- **A.** The scheduler is missing
- **B.** kubelet cannot pull the image (name/tag/auth/registry/network)
- **C.** The Service CIDR is wrong
- **D.** HPA is disabled

??? success "Reveal answer"
    **Correct answer: B**

    Check image reference and pull secrets/registry connectivity.

    **Related concepts**

    - ImagePullBackOff

### Question 14

CrashLoopBackOff indicates:

**Difficulty:** Intermediate

**Options:**

- **A.** Pod starts then the container exits repeatedly
- **B.** Node memory is always healthy
- **C.** DNS is perfect
- **D.** RBAC is unused

??? success "Reveal answer"
    **Correct answer: A**

    Investigate logs, probes, and command failures.

    **Related concepts**

    - CrashLoopBackOff

### Question 15

Which field sets CPU/memory requests and limits on a container?

**Difficulty:** Intermediate

**Options:**

- **A.** resources.requests / resources.limits
- **B.** replicas only
- **C.** hostNetwork: true
- **D.** strategy.type

??? success "Reveal answer"
    **Correct answer: A**

    requests affect scheduling; limits cap usage.

    **Related concepts**

    - Resources
    - QoS

### Question 16

A Deployment rolling update should keep capacity. Which helps?

**Difficulty:** Intermediate

**Options:**

- **A.** maxUnavailable / maxSurge settings appropriate to SLO
- **B.** delete the namespace mid-rollout
- **C.** set replicas to 0 first always
- **D.** disable readiness probes permanently

??? success "Reveal answer"
    **Correct answer: A**

    RollingUpdate parameters control surge and unavailability.

    **Related concepts**

    - RollingUpdate

### Question 17

RBAC: a Role is scoped to:

**Difficulty:** Intermediate

**Options:**

- **A.** A namespace (Role) vs cluster-wide (ClusterRole)
- **B.** Only etcd
- **C.** Only Ingress
- **D.** Only container images

??? success "Reveal answer"
    **Correct answer: A**

    Role is namespaced; ClusterRole is cluster-scoped.

    **Related concepts**

    - RBAC
    - Role
    - ClusterRole

### Question 18

Helm primarily helps you:

**Difficulty:** Intermediate

**Options:**

- **A.** Package, templatise, and release Kubernetes manifests as charts
- **B.** Replace container runtimes
- **C.** Compile the Linux kernel
- **D.** Provision bare metal only

??? success "Reveal answer"
    **Correct answer: A**

    Helm is the common package manager for Kubernetes apps.

    **Related concepts**

    - Helm

### Question 19

HPA scales Pods based on:

**Difficulty:** Intermediate

**Options:**

- **A.** Metrics such as CPU/memory/custom metrics (when metrics pipeline exists)
- **B.** Git commit messages
- **C.** Docker Hub stars
- **D.** Manual /etc/hosts edits

??? success "Reveal answer"
    **Correct answer: A**

    Horizontal Pod Autoscaler uses resource/custom metrics.

    **Related concepts**

    - HPA

### Question 20

PodDisruptionBudget (PDB) is meant to:

**Difficulty:** Advanced

**Options:**

- **A.** Limit voluntary disruptions so a minimum number/percentage of Pods stay available
- **B.** Encrypt etcd automatically
- **C.** Replace NetworkPolicies
- **D.** Disable node upgrades forever

??? success "Reveal answer"
    **Correct answer: A**

    PDBs protect availability during drains/upgrades.

    **Related concepts**

    - PDB

## Section 3 — Scenario-Based Questions

### Question 21

Intermittent 503s during deploy. Readiness path `/healthz` 404 while `/` works. Effect?

**Difficulty:** Intermediate

**Options:**

- **A.** Pods may never become Ready, so Services send no traffic (or only to old pods) — fix probe to a real path
- **B.** Nodes reboot
- **C.** etcd loses quorum always
- **D.** Images become unsigned

??? success "Reveal answer"
    **Correct answer: A**

    Bad readiness blocks endpoints. Align probes with the app contract.

    **Related concepts**

    - Readiness
    - Probes

### Question 22

Deployment stuck. describe shows FailedScheduling / Insufficient cpu. Fix direction?

**Difficulty:** Intermediate

**Options:**

- **A.** Reduce requests, add nodes, or free capacity — scheduling cannot place the Pod
- **B.** Delete kube-apiserver
- **C.** Change the app language
- **D.** Disable all Services

??? success "Reveal answer"
    **Correct answer: A**

    Scheduler needs fitting node resources.

    **Related concepts**

    - Scheduling
    - Requests

### Question 23

Secret mounted as env still shows old value after you apply a new Secret.

**Difficulty:** Advanced

**Options:**

- **A.** Pods do not automatically reload env from updated Secrets — rollout restart / redesign for dynamic reload
- **B.** Kubernetes never mounts Secrets
- **C.** Only Helm can update Secrets
- **D.** Need to reboot every node

??? success "Reveal answer"
    **Correct answer: A**

    Env-injected secrets are fixed at process start for typical apps.

    **Related concepts**

    - Secrets rotation

### Question 24

GitOps reports drift: live Deployment differs from Git. Correct response?

**Difficulty:** Advanced

**Options:**

- **A.** Change Git (or allowlisted sync) — avoid long-lived kubectl edit that fights the reconciler
- **B.** Always kubectl edit and ignore Git
- **C.** Turn off the cluster
- **D.** Delete Git history

??? success "Reveal answer"
    **Correct answer: A**

    Git is the source of truth; reconcile toward desired state.

    **Related concepts**

    - GitOps
    - Drift

### Question 25

Ingress returns 404 but Service curl from inside cluster works. Likely layer?

**Difficulty:** Intermediate

**Options:**

- **A.** Ingress rules/host/path or Ingress controller config
- **B.** Container runtime missing
- **C.** PVC pending only
- **D.** HPA minReplicas

??? success "Reveal answer"
    **Correct answer: A**

    Ingress is the external HTTP routing layer.

    **Related concepts**

    - Ingress

### Question 26

You need zero-downtime drain of a node. Useful sequence?

**Difficulty:** Intermediate

**Options:**

- **A.** cordon + drain (respecting PDBs), ensure replicas elsewhere, then maintain
- **B.** power off the node immediately
- **C.** delete the Deployment
- **D.** remove CoreDNS first

??? success "Reveal answer"
    **Correct answer: A**

    cordon/drain is the supported maintenance workflow.

    **Related concepts**

    - kubectl drain
    - PDB

### Question 27

NetworkPolicy default-deny in a namespace means new Pods:

**Difficulty:** Advanced

**Options:**

- **A.** May be isolated until explicit allow policies select them
- **B.** Automatically get Internet without rules
- **C.** Bypass Services
- **D.** Ignore DNS

??? success "Reveal answer"
    **Correct answer: A**

    Default-deny requires careful allowlists for expected traffic.

    **Related concepts**

    - NetworkPolicy

### Question 28

Init container fails; app container never starts. Why?

**Difficulty:** Intermediate

**Options:**

- **A.** Init containers must succeed before app containers start
- **B.** Init containers run after the app
- **C.** Init containers replace the scheduler
- **D.** Init containers only run on Windows

??? success "Reveal answer"
    **Correct answer: A**

    Init sequence gates startup.

    **Related concepts**

    - Init containers

### Question 29

type LoadBalancer on bare metal without cloud integration. What happens?

**Difficulty:** Advanced

**Options:**

- **A.** EXTERNAL-IP may stay pending unless MetalLB/equivalent provides IPs
- **B.** Kubernetes invents a public IP always
- **C.** The Pod becomes a Node
- **D.** RBAC is disabled

??? success "Reveal answer"
    **Correct answer: A**

    LoadBalancer needs an implementation to allocate addresses.

    **Related concepts**

    - LoadBalancer
    - MetalLB

### Question 30

Liveness probe too aggressive on a slow-starting JVM. Symptom?

**Difficulty:** Intermediate

**Options:**

- **A.** Container killed/restarted before it becomes healthy — use startupProbe or retune thresholds
- **B.** Faster cold starts magically
- **C.** More endpoints join early
- **D.** etcd grows slower

??? success "Reveal answer"
    **Correct answer: A**

    startupProbe or longer delays prevent premature liveness kills.

    **Related concepts**

    - startupProbe

## Section 4 — Troubleshooting

### Question 31

Pod Pending; events: failed to pull image `myapp:latst` (typo). Root cause?

**Difficulty:** Beginner

**Options:**

- **A.** Wrong image reference/tag
- **B.** CoreDNS crash only
- **C.** Missing Deployment name
- **D.** PDB conflict

??? success "Reveal answer"
    **Correct answer: A**

    Typos in image names cause pull failures.

    **Related concepts**

    - Image references

### Question 32

Service selects app=api but Pods are labelled app=backend. Effect?

**Difficulty:** Beginner

**Options:**

- **A.** Endpoints empty — no traffic to Pods
- **B.** Automatic label rewrite
- **C.** Nodes cordon
- **D.** HPA scales to zero always

??? success "Reveal answer"
    **Correct answer: A**

    Selector/label mismatch yields empty Endpoints.

    **Related concepts**

    - Selectors
    - Endpoints

### Question 33

OOMKilled in container status. Meaning?

**Difficulty:** Intermediate

**Options:**

- **A.** Exceeded memory limit (or node pressure killing)
- **B.** CPU throttle only
- **C.** DNS NXDOMAIN
- **D.** Successful probe

??? success "Reveal answer"
    **Correct answer: A**

    OOMKilled is a memory kill signal outcome.

    **Related concepts**

    - OOMKilled

### Question 34

`kubectl auth can-i delete deployments -n prod` returns no. Next?

**Difficulty:** Intermediate

**Options:**

- **A.** Check RoleBindings/ClusterRoleBindings for your identity; request least privilege access
- **B.** Disable RBAC cluster-wide
- **C.** Use --force on API server flags casually
- **D.** Store kubeconfig in a public gist

??? success "Reveal answer"
    **Correct answer: A**

    Fix RBAC bindings appropriately; do not disable RBAC.

    **Related concepts**

    - RBAC troubleshooting

### Question 35

PVC Pending forever in a cluster without default StorageClass. Likely?

**Difficulty:** Intermediate

**Options:**

- **A.** No provisioner/StorageClass to satisfy the claim
- **B.** Ingress misconfigured
- **C.** HPA missing
- **D.** Too many ConfigMaps

??? success "Reveal answer"
    **Correct answer: A**

    Dynamic provisioning needs a StorageClass; otherwise bind a matching PV.

    **Related concepts**

    - StorageClass
    - PVC Pending

## Section 5 — Architecture

### Question 36

For a stateless HTTP API, which pairing is most typical?

**Difficulty:** Intermediate

**Options:**

- **A.** Deployment + ClusterIP/Ingress + HPA + PDB
- **B.** one naked Pod on a specific node name forever without probes
- **C.** hostNetwork for every Pod
- **D.** Privileged DaemonSet as the web tier

??? success "Reveal answer"
    **Correct answer: A**

    Stateless HTTP commonly uses Deployment, Service/Ingress, and availability controls.

    **Related concepts**

    - Workload design

### Question 37

Why prefer requests+limits over unlimited containers?

**Difficulty:** Intermediate

**Options:**

- **A.** Predictable scheduling and noisy-neighbour protection
- **B.** They slow the API server only
- **C.** Required to use ConfigMaps
- **D.** Disable metrics

??? success "Reveal answer"
    **Correct answer: A**

    Resources enable fair scheduling and containment.

    **Related concepts**

    - Capacity planning

### Question 38

Multi-tenant cluster security baseline includes:

**Difficulty:** Advanced

**Options:**

- **A.** Namespaces, RBAC least privilege, NetworkPolicies, admission controls, non-root images
- **B.** A single cluster-admin kubeconfig for everyone
- **C.** Privileged pods by default
- **D.** No audit logs

??? success "Reveal answer"
    **Correct answer: A**

    Defence in depth across identity, network, and workload controls.

    **Related concepts**

    - Multi-tenancy
    - Hardening

### Question 39

Blue/green vs rolling update — trade-off summary?

**Difficulty:** Advanced

**Options:**

- **A.** Blue/green shifts traffic between versions with more capacity cost; rolling gradually replaces replicas in one Deployment
- **B.** They are identical
- **C.** Rolling always needs two clusters
- **D.** Blue/green forbids Services

??? success "Reveal answer"
    **Correct answer: A**

    Choose based on risk, capacity, and traffic switching needs.

    **Related concepts**

    - Deployment strategies

### Question 40

Where should cluster state backups focus first?

**Difficulty:** Advanced

**Options:**

- **A.** etcd (or control plane backup strategy) plus application data volumes
- **B.** Only worker node /tmp
- **C.** Only container stdout
- **D.** Only CNI IPAM files on one node

??? success "Reveal answer"
    **Correct answer: A**

    Control plane state and persistent app data are critical.

    **Related concepts**

    - Disaster recovery
    - etcd

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for interviews and labs at this track level |
| 28–35 | Good | Pass — revise weak sections, then retry |
| 20–27 | Needs improvement | Revisit tutorials for missed topics before labs |
| ≤19 | Restart foundations | Work the track in order, then retake |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

Weak on API objects → early Kubernetes tutorials. Weak on probes/rollouts → Health Checks tutorial + Deployment triage lab. Weak on RBAC/security → RBAC and hardening tutorials.

- Track: [Kubernetes](../kubernetes/index.md)
- Lab: [Kubernetes Deployment Triage](../labs/kubernetes-deployment-triage.md)
- Cheat sheet: [Kubernetes](../cheatsheets/kubernetes.md)
- Interview prep: [Kubernetes](../interview/kubernetes.md)
- Path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## Interview Connection

Be ready to explain probes, CrashLoopBackOff vs ImagePullBackOff, Service selectors, requests vs limits, and a drain/PDB story.

## References

1. [Kubernetes documentation](https://kubernetes.io/docs/home/)
2. [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
3. [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
