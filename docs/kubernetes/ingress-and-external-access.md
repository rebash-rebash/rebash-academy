---
title: "Ingress and Gateway API"
description: "Expose HTTP(S) apps with Ingress controllers, TLS, and Gateway API HTTPRoutes for production Kubernetes traffic routing."
difficulty: intermediate
estimated_time: "45–60 min"
technology: kubernetes
category: kubernetes
module: "Module 6 · Ingress & Gateway API"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - kubernetes
  - ingress
  - gateway-api
prerequisites:
  - kubernetes/services-and-cluster-networking
next:
  - kubernetes/persistent-volumes-and-storage
related:
  - kubernetes/kubernetes-networking-deep-dive
labs: []
projects: []
interview: interview/kubernetes
certifications:
  - CKA
  - CKAD
tags:
  - kubernetes
  - ingress
  - tls
  - gateway-api
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Ingress and Gateway API

## Overview



Route external HTTP traffic to Services via Ingress (and understand Gateway API as the successor model) including TLS secrets.

**Ingress** needs a controller (nginx, Traefik, cloud LB). **Gateway API** (`Gateway`, `HTTPRoute`) is the modern, role-oriented replacement gaining adoption.

This is a core tutorial in **Module 6 · Ingress & Gateway API** of the REBASH Academy **Kubernetes for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Services and Cluster Networking](services-and-cluster-networking.md)
- An Ingress controller installed (kind often needs one)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Write an Ingress rule (host/path → Service)  
- [ ] Attach a TLS secret  
- [ ] Name Gateway API resources  
- [ ] Know controller must exist



## Architecture



This topic’s control points and relationships are shown below.

![Ingress flow](../assets/excalidraw/k8s-ingress-flow.svg)



## Theory



### What it is

**Ingress** is a Kubernetes API for **HTTP(S) routing** into the cluster: host and path rules forward to Services. An **Ingress controller** (nginx, Traefik, cloud L7) watches Ingress objects and programmes the actual proxy or load balancer. **Gateway API** (`Gateway`, `HTTPRoute`, and related resources) is the newer, role-oriented model that many platforms are adopting as the successor.

### Why it matters

Exposing every Service as a LoadBalancer is expensive and noisy. Ingress (or Gateway API) centralises TLS termination, host-based routing, and path splitting for many apps behind one entry point. DevOps teams standardise on one controller and let application teams ship Ingress/HTTPRoute manifests.

### How it works (mental model)

1. Install a controller (DaemonSet/Deployment) that has permission to watch Ingress or Gateway API resources.
2. Create Services for backends (usually ClusterIP).
3. Declare rules: `host` + `path` → Service:port; attach a TLS Secret for HTTPS.
4. The controller configures its dataplane; DNS for the host points at the controller’s external address.
5. Without a controller, Ingress objects sit idle — ADDRESS stays empty.

Gateway API separates infrastructure (**Gateway**) from application routes (**HTTPRoute**), improving multi-team ownership.

### Key concepts / comparisons

| Model | Resources | Notes |
|-------|-----------|-------|
| Ingress | Ingress, IngressClass | Widely deployed today |
| Gateway API | Gateway, HTTPRoute, … | Modern replacement path |

| Piece | Role |
|-------|------|
| Ingress / HTTPRoute | Desired HTTP routing |
| Controller | Implements routing |
| TLS Secret | Certificates for HTTPS |

On kind, install ingress-nginx (or similar). Managed clouds often provide a controller or L7 annotations on Services.

### Common pitfalls

- Creating Ingress YAML with no controller installed — nothing listens.
- Wrong `pathType` or missing trailing-slash assumptions causing 404s.
- TLS Secret in the wrong namespace or wrong keys (`tls.crt` / `tls.key`).
- Pointing DNS at a NodePort by mistake while the controller expects a LoadBalancer.
- Treating Ingress as a Service type — it is a separate API that fronts Services.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-k8s/module-06 && cd ~/rebash-k8s/module-06
```

**Focus:** Expose HTTP traffic through an Ingress resource (controller optional)

### Step 1 – Deploy a backend and Ingress object

```bash
kubectl create namespace rebash-lab
kubectl -n rebash-lab create deployment web --image=nginx:1.27-alpine
kubectl -n rebash-lab expose deployment web --port=80
cat > ingress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web
  namespace: rebash-lab
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: web.rebash.local
    http:
      paths:
      - path: /
pathType: Prefix
backend:
  service:
    name: web
    port:
      number: 80
EOF
kubectl apply -f ingress.yaml
```

### Step 2 – Validate Ingress wiring

```bash
kubectl -n rebash-lab get ingress web -o wide
kubectl -n rebash-lab describe ingress web
# If an Ingress controller is installed, ADDRESS will populate; otherwise the object still validates routing intent
kubectl -n rebash-lab get svc web endpoints
```

### Final step – Cleanup note

```bash
kubectl delete namespace rebash-lab --ignore-not-found
# Workspace kept for notes; remove with: rm -rf "$(pwd)" when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-k8s/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Ingress and Gateway API** always combines:

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



!!! warning "Creating Ingress YAML with no controller installed — nothing listens."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Wrong `pathType` or missing trailing-slash assumptions causing 404s."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Ingress and Gateway API changes as code and review them in pull requests
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



**Ingress and Gateway API** is essential for Cloud and DevOps engineers working with kubernetes. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. What does an Ingress resource declare, and what still needs to exist for traffic to flow?
2. How does Ingress differ from a Service of type LoadBalancer?
3. What is pathType Prefix versus Exact?
4. What security controls should sit in front of Ingress-exposed applications?
5. Why might an Ingress show no ADDRESS even though the object is valid?

!!! tip "Sample answer — question 2"
    Ingress describes HTTP routing rules. A controller must implement them, and backends must be Ready Service Endpoints. Without a controller, the object alone does not open traffic.

!!! tip "Sample answer — question 4"
    Exposing HTTP needs TLS, authentication where appropriate, WAF or rate limiting, network policies, and careful host/path design so internal apps are not accidentally public.



## Related Tutorials



- [Course overview](index.md)
- [Persistent Volumes and Storage](persistent-volumes-and-storage.md)



## References



- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) · [Gateway API](https://gateway-api.sigs.k8s.io/)
