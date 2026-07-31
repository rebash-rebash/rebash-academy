---
title: "Managed Kubernetes — EKS, AKS, GKE"
description: "Compare Amazon EKS, Azure AKS, and Google GKE — control plane ownership, IAM, networking, and day-2 ops for Cloud DevOps."
difficulty: advanced
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 19 · Managed Kubernetes"
career_paths:
  - cloud-engineer
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - kubernetes
  - eks
  - aks
  - gke
prerequisites:
  - kubernetes/troubleshooting-kubernetes-workloads
next:
  - kubernetes/production-kubernetes-excellence
related:
  - aws/index
  - azure/index
  - gcp/index
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
tags:
  - kubernetes
  - eks
  - aks
  - gke
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Managed Kubernetes — EKS, AKS, GKE

## Overview



Compare EKS, AKS, and GKE on control-plane responsibility, identity, networking models, and what you still own (nodes, add-ons, workloads, cost).

Managed Kubernetes runs the **control plane** for you. You still design node pools, CNI/network plugins, IAM mapping, upgrades, and GitOps.

This is a core tutorial in **Module 19 · Managed Kubernetes** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Troubleshooting](troubleshooting-kubernetes-workloads.md)
- Cloud fundamentals helpful



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] State shared responsibility per cloud  
- [ ] Map IAM → Kubernetes RBAC (roughly)  
- [ ] Note default CNI / LB integrations  
- [ ] Plan upgrades on managed offerings



## Architecture



This topic’s control points and relationships are shown below.

![Production cluster](../assets/excalidraw/k8s-production-cluster.svg)



## Theory



### What it is

**Managed Kubernetes** offerings — **Amazon EKS**, **Azure AKS**, and **Google GKE** — run the control plane (API server, etcd, and core controllers) as a cloud service. You consume a stable API endpoint and attach compute (node groups, serverless nodes, or autopilot-style modes). Networking, IAM mapping, add-ons, and workloads remain shared-responsibility items you must design.

### Why it matters

Self-managing etcd HA and control-plane upgrades is real toil. Managed services reduce that burden so DevOps teams focus on platforms, GitOps, and applications. Choosing among EKS/AKS/GKE usually follows your cloud, identity model, and appetite for Autopilot/Fargate-style trade-offs versus node-level control.

### How it works (mental model)

1. Create a cluster in the cloud console/API/Terraform — provider runs the control plane.
2. Configure VPC/VNet, subnets, and CNI (AWS VPC CNI, Azure CNI/overlay, GKE dataplane).
3. Map cloud identities to Kubernetes RBAC (EKS access entries / aws-auth, Entra ID integration, Google IAM).
4. Attach node pools or enable serverless/autopilot; install cluster add-ons (CSI, metrics, ingress).
5. Point kubeconfig at the API; operate workloads as on any conformant cluster — controllers still reconcile desired state.

You do not SSH to etcd; you do still patch nodes, rotate credentials, and test restores of *your* data.

### Key concepts / comparisons

| | EKS | AKS | GKE |
|--|-----|-----|-----|
| Control plane | AWS-managed | Azure-managed | Google-managed |
| Identity | IAM + access entries / aws-auth | Entra ID / AAD | Google IAM |
| Nodes | Managed node groups / Fargate / Karpenter | Node pools / Virtual nodes | Node pools / Autopilot |
| Registry | ECR | ACR | Artifact Registry |

| Mode | Trade-off |
|------|-----------|
| Standard nodes | More control, more ops |
| Autopilot / Fargate-like | Less node ops, less flexibility |

### Common pitfalls

- Treating managed as “no ops” — upgrades, IAM, and cost still need owners.
- Wrong subnet/CNI design causing Pod IP exhaustion.
- Forgetting cluster auth maps — `kubectl` works for admins but CI roles get 403.
- Leaving public API endpoints open without IP allow lists or private-only access.
- Ignoring version deprecation calendars until the control plane blocks creates.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-19 && cd ~/rebash-k8s/module-19
```

**Focus:** Compare local cluster context with managed-Kubernetes operational checks (no paid cloud required)

### Step 1 – Document cluster identity and node pool shape

```bash
kubectl create namespace rebash-lab
kubectl config view --minify -o yaml | head -n 40
kubectl get nodes -o custom-columns=NAME:.metadata.name,INSTANCE:.metadata.labels.node\.kubernetes\.io/instance-type,ZONE:.metadata.labels.topology\.kubernetes\.io/zone
kubectl get ns kube-system -o jsonpath='{.metadata.annotations}{"
"}' || true
```

### Step 2 – Run a portability smoke test as you would after attaching a managed cluster

```bash
kubectl -n rebash-lab run managed-smoke --image=busybox:1.36 --restart=Never --command -- echo ok-from-cluster
kubectl -n rebash-lab wait --for=jsonpath='{.status.phase}'=Succeeded pod/managed-smoke --timeout=60s
kubectl -n rebash-lab logs managed-smoke
cat > MANAGED_NOTES.md <<'EOF'
EKS/AKS/GKE differences to revisit: IAM mapping, CNI, load balancers, add-ons, upgrades.
This lab only validates kubectl access patterns that stay the same across providers.
EOF
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-19/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Managed Kubernetes — EKS, AKS, GKE** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for kubernetes as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Treating managed as “no ops” — upgrades, IAM, and cost still need owners."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Wrong subnet/CNI design causing Pod IP exhaustion."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Managed Kubernetes — EKS, AKS, GKE changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible



## Troubleshooting



| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |



## Summary



**Managed Kubernetes — EKS, AKS, GKE** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What responsibilities typically remain with you on a managed Kubernetes service?
2. How does cloud IAM integration differ across EKS, AKS, and GKE at a high level?
3. Why pin node image/version upgrade strategies even when the control plane is managed?
4. What vendor lock-in trade-offs appear when using cloud-specific Ingress or identity add-ons?
5. How do you validate portability of an application across managed offerings?

!!! tip "Sample answer — question 2"
    You still own workloads, RBAC inside the cluster, networking design, upgrades of node pools, add-ons you install, and cost. The vendor usually operates the control plane API servers and etcd.

!!! tip "Sample answer — question 4"
    Cloud-native LB annotations and IAM roles simplify ops but couple manifests to one provider. Prefer portable core APIs where possible, and isolate provider-specific resources behind modules.



## Related Tutorials



- [Course overview](index.md)
- [Production Kubernetes Excellence](production-kubernetes-excellence.md)



## References



- [EKS](https://docs.aws.amazon.com/eks/) · [AKS](https://learn.microsoft.com/azure/aks/) · [GKE](https://cloud.google.com/kubernetes-engine/docs)
