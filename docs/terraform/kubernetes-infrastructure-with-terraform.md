---
title: "Kubernetes Infrastructure with Terraform"
description: "Provision managed clusters and node pools with Terraform, then use kubernetes and helm providers — and know where GitOps takes over."
difficulty: advanced
estimated_time: "45–60 min"
technology: terraform
category: terraform
module: "Module 18 · Kubernetes Infrastructure"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - terraform
  - kubernetes
  - helm
prerequisites:
  - terraform/multi-cloud-terraform
next:
  - terraform/production-terraform-patterns
related:
  - kubernetes/index
  - helm/index
  - terraform/terraform-in-ci-cd-pipelines
labs: []
projects: []
interview: interview/terraform
certifications:
  - Terraform Associate
tags:
  - terraform
  - kubernetes
  - helm
  - eks
  - aks
  - gke
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Infrastructure with Terraform

## Overview

Provision managed Kubernetes clusters and node pools with Terraform, understand the kubernetes and helm providers, and draw a clear boundary where GitOps owns in-cluster desired state.

Terraform shines at **cluster infrastructure**: control plane, node pools, IAM for the API server, and add-on plumbing at the cloud edge. In-cluster workloads usually belong to **GitOps** (Argo CD / Flux) with Helm charts — not endless `kubernetes_*` resources in the same root that created the cluster. Use the kubernetes/helm providers sparingly for bootstrap (for example CRDs or controllers that GitOps then manages).

This is a core tutorial in **Module 18 · Kubernetes Infrastructure** of the REBASH Academy **Terraform for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Multi-Cloud Terraform](multi-cloud-terraform.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Outline managed cluster + node pool resources (EKS/AKS/GKE class)  
- [ ] Explain kubernetes provider authentication patterns  
- [ ] Describe helm provider use for bootstrap only  
- [ ] Draw the GitOps boundary after cluster create

## Architecture

This topic’s control points and relationships are shown below.

![Terraform and Kubernetes](../assets/excalidraw/terraform-kubernetes.svg)

## Theory

### What it is

**Kubernetes infrastructure with Terraform** means declaring the cluster and its cloud dependencies as code, then optionally talking to the Kubernetes API via the **kubernetes** and **helm** providers.

| Layer | Typical owner | Examples |
|-------|---------------|----------|
| Cloud underlay | Terraform | VPC, subnets, NAT, IAM |
| Managed control plane | Terraform | EKS / AKS / GKE cluster |
| Node pools / node groups | Terraform | Size, instance type, labels/taints |
| Bootstrap add-ons | Terraform (thin) or GitOps | ingress-nginx, cert-manager install once |
| App / platform workloads | GitOps + Helm | Deployments, Helm releases ongoing |

Managed offerings differ in resource names but share the shape: cluster resource → node pool → kubeconfig / OIDC trust → optional provider blocks that use the cluster endpoint.

### Why it matters

Cluster click-ops does not survive audit or DR. Terraform gives reviewable plans for expensive, slow-changing objects (control plane, node IAM). Mixing day-2 application deploys into the same Terraform state creates long plans, state contention, and fights with GitOps controllers. Platform teams succeed when Terraform builds the landing pad and GitOps flies the planes.

### How it works

1. **Underlay:** network, security groups / firewall rules, private API endpoint choices.  
2. **Cluster:** create managed control plane with version pin and logging settings.  
3. **Node pools:** separate pools for system vs workloads; taints/labels for placement.  
4. **Access:** output kubeconfig pieces or configure OIDC; CI/GitOps identities get RBAC, not admin keys forever.  
5. **Providers:** after cluster exists, a `kubernetes` / `helm` provider can authenticate (exec plugin, token, or kubeconfig). Prefer **depends_on** / explicit sequencing so providers do not configure against an incomplete API.  
6. **Hand-off:** install only what GitOps needs to start (for example the GitOps controller itself), then stop managing app Helm releases in Terraform.

Conceptual sketch (not cloud-complete):

```hcl
# Cloud cluster (illustrative)
# resource "aws_eks_cluster" "this" { ... }
# resource "aws_eks_node_group" "default" { ... }

provider "kubernetes" {
  host                   = var.cluster_endpoint
  cluster_ca_certificate = base64decode(var.cluster_ca)
  token                  = var.cluster_token # prefer exec/OIDC in production
}

# Bootstrap only — prefer GitOps for ongoing chart upgrades
# resource "helm_release" "argo_cd" {
#   name       = "argocd"
#   repository = "https://argoproj.github.io/argo-helm"
#   chart      = "argo-cd"
#   version    = "7.7.12"
#   namespace  = "argocd"
#   create_namespace = true
# }
```

### Key concepts and comparisons

| Concern | Terraform | GitOps |
|---------|-----------|--------|
| Cluster create/upgrade | Yes | Rarely |
| Node pool resize | Often yes | Sometimes cloud autoscaler |
| App Helm release | Bootstrap only | Yes |
| Drift of Deployments | Avoid fighting | Controller reconciles |

| Provider | Use for |
|----------|---------|
| Cloud (aws/azurerm/google) | Cluster + IAM + network |
| `kubernetes` | Raw manifests / objects at bootstrap |
| `helm` | Chart install for platform seeds |

### Common pitfalls

- Managing every microservice as `helm_release` in the cluster root — plans become unusable.  
- Configuring kubernetes provider at plan time before the cluster exists (chicken-and-egg; use staged roots or `-target` carefully once).  
- Storing long-lived cluster-admin kubeconfigs in Terraform state without ACL discipline.  
- Letting Terraform and Argo CD both own the same Deployment.  
- Untested control-plane version bumps in production without a staging cluster.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-terraform/module-18 && cd ~/rebash-terraform/module-18
```

**Focus:** hands-on practice for Kubernetes Infrastructure with Terraform

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-terraform/module-18 && cd ~/rebash-terraform/module-18

cat > boundary.md << 'EOF'

### Final step – Cleanup note

```bash
# Keep ~/rebash-terraform/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-terraform/module-18/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Kubernetes Infrastructure with Terraform** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for terraform as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Managing every microservice as `helm_release` in the cluster root — plans become unusable."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Configuring kubernetes provider at plan time before the cluster exists (chicken-and-egg; u"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Kubernetes Infrastructure with Terraform changes as code and review them in pull requests
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

**Kubernetes Infrastructure with Terraform** is essential for Cloud and DevOps engineers working with terraform. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Kubernetes Infrastructure with Terraform** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Production Terraform Patterns](production-terraform-patterns.md)

## References

- [Kubernetes provider](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) · [Helm provider](https://registry.terraform.io/providers/hashicorp/helm/latest/docs) · [EKS](https://docs.aws.amazon.com/eks/) / [AKS](https://learn.microsoft.com/azure/aks/) / [GKE](https://cloud.google.com/kubernetes-engine/docs)
