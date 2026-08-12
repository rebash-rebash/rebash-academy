---
title: "Argo CD Interview Preparation"
description: "8 curated Argo CD interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: argocd
tags:
  - interview
  - argocd
comments: false
---

{% raw %}
# Argo CD Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is Argo Rollouts, and how does it implement progressive delivery?**

??? success "Reveal answer"
    **In short:** Argo Rollouts adds canary and blue-green progressive delivery on top of Kubernetes.
    
    **Key points**
    
    - **Rollout CR** replaces a plain Deployment for stepwise traffic shifts.
    - Steps like `setWeight: 10`, pause, and analysis gate promotion.
    - Works with Ingress, Service Mesh, or ALB for traffic splitting.
    - Failed analysis triggers automated rollback to the stable ReplicaSet.
    
    **Trap**
    
    - Skipping analysis templates turns canary into a slow rolling update with no real safety.

**2. What is the difference between GitOps and traditional CD pipelines?**

??? success "Reveal answer"
    **In short:** Traditional CD pushes with pipeline credentials; GitOps pulls and reconciles from Git.
    
    **Key points**
    
    - **Push CD** — CI holds kubeconfig and runs `kubectl`/`helm upgrade`.
    - **GitOps** — Git is the desired state; a controller syncs the cluster continuously.
    - Drift shows as OutOfSync; self-heal can revert unauthorised live changes.
    - Auditing improves because every change is a Git commit (or a logged sync).
    
    **Trap**
    
    - Emergency `kubectl apply` without committing creates silent drift GitOps will fight or hide.

**3. What are the key components of ArgoCD?**

??? success "Reveal answer"
    **In short:** Argo CD is a control plane of specialised controllers around Applications.
    
    **Key points**
    
    - **argocd-server** — UI, CLI, and API.
    - **repo-server** — clones Git and renders Helm/Kustomize manifests.
    - **application-controller** — compares live vs desired and syncs.
    - **Application / ApplicationSet** — unit of delivery and multi-cluster fan-out.
    - Redis and Dex (optional) support caching and SSO.
    
    **Trap**
    
    - Giving every Application `cluster-admin` collapses blast-radius controls.

**4. What is argocd and why we are using it?**

??? success "Reveal answer"
    **In short:** Argo CD keeps Kubernetes matching Git so deploys are reviewable, repeatable, and self-healing.
    
    **Key points**
    
    - Point it at manifests, Helm charts, or Kustomize overlays in Git.
    - Sync brings the cluster to the chosen revision; prune removes deleted resources.
    - Multi-cluster: one control plane can manage many destinations.
    - Teams review PRs instead of approving opaque pipeline kubectl steps.
    
    **Trap**
    
    - Tracking mutable tags (`latest`) makes “Git is truth” meaningless.

**5. What is ArgoCD and what problem does it solve?**

??? success "Reveal answer"
    **In short:** Argo CD solves cluster drift and unsafe push-deploy credentials with continuous Git reconciliation.
    
    **Key points**
    
    - Desired state is Git; live state is the cluster API.
    - Detects OutOfSync when someone hotfixes live or a sync fails.
    - Reduces long-lived cluster-admin tokens in CI for every app.
    - Enables progressive delivery when paired with Rollouts or sync waves.
    
    **Trap**
    
    - Without PR checks on the GitOps repo, GitOps just automates bad YAML faster.

## Practice questions

**6. How do you design GitOps for 1000+ clusters with environment drift detection, emergency hotfixes, and controlled manual overrides?**

??? success "Reveal answer"
    **In short:** Scale with ApplicationSets, sharded Argo CD, labelled cluster rings, and strict break-glass.
    
    **Key points**
    
    - **ApplicationSet generators** onboard clusters by label (env, region, ring).
    - App-of-apps or mono-repo overlays keep per-cluster config thin.
    - Drift: auto-sync + self-heal for platform apps; manual sync for high-risk.
    - Hotfix: short sync window disable under change control, then commit the fix.
    - Shard controllers/repo-servers; never one mega-instance for everything.
    
    **Try this**
    
    - `argocd app list --output wide`
    - `argocd app get <app> --refresh`
    
    **Trap**
    
    - Manual overrides without a ticket leave 1000 clusters in unknown states.

**7. How do you perform application synchronization in ArgoCD?**

??? success "Reveal answer"
    **In short:** Sync applies the Git revision’s manifests so live state matches desired state.
    
    **Key points**
    
    - Trigger via UI, `argocd app sync`, API, or automated sync policies.
    - **Prune** deletes resources removed from Git; use carefully in prod.
    - **ApplyOutOfSyncOnly** and sync options reduce blast radius.
    - Hooks and sync waves order CRDs, operators, then workloads.
    
    **Try this**
    
    - `argocd app sync my-app --prune`
    - `argocd app wait my-app --health`
    
    **Trap**
    
    - Force sync with prune on the wrong app can delete production resources in seconds.

**8. How does GitOps differ from traditional IaC?**

??? success "Reveal answer"
    **In short:** IaC defines infrastructure; GitOps adds a continuous reconciler that keeps reality matching Git.
    
    **Key points**
    
    - **IaC** (Terraform etc.) often push-applies on demand with a state file.
    - **GitOps** continuously compares live API objects to a Git revision.
    - IaC state maps IDs; GitOps state is Git + cluster (no `tfstate` for manifests).
    - Many platforms use both: Terraform for cloud accounts, Argo CD for Kubernetes apps.
    
    **Trap**
    
    - Calling any YAML in Git “GitOps” without a reconciliation agent is just versioned push.

## Related
- Course: [Argo CD](../argocd/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
