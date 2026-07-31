---
title: "Kubernetes Python Client Automation"
description: "Automate Kubernetes with kubernetes-python-client — kubeconfig/in-cluster config, Pods, Deployments, Services, ConfigMaps, Secrets, Jobs, and Namespaces."
difficulty: advanced
estimated_time: "55–70 min"
technology: python
category: python
module: "Module 18 · Kubernetes Automation"
career_paths:
  - kubernetes-engineer
  - platform-engineer
  - devops-engineer
  - site-reliability-engineer
skills:
  - python
  - kubernetes
  - kubernetes-python-client
prerequisites:
  - python/docker-sdk-automation
next:
  - python/infrastructure-automation-terraform
related:
  - networking/kubernetes-networking-fundamentals
  - labs/python-kubernetes-health-checker
labs:
  - labs/python-kubernetes-health-checker
  - labs/python-kubernetes-deployment-validator
projects: []
interview: interview/python
certifications:
  - CKA
  - CKAD
tags:
  - python
  - kubernetes
  - client
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Python Client Automation

## Overview

Load kubeconfig or in-cluster config, list core workloads with the official Python client, and build read-only health/inventory reports (mutate only with explicit flags later).

`kubernetes` Python client is a typed wrapper around the API server. Respect **RBAC**, never log Secret data, and default to get/list.

Complete [Docker SDK Automation](docker-sdk-automation.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 18 · Kubernetes Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [REST APIs](rest-apis-requests-auth-and-resilience.md) concepts  
- Optional: local cluster (kind/minikube/k3s) **or** fixture path

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Load kubeconfig / in-cluster config  
- [ ] List Pods and Deployments in a namespace  
- [ ] Sketch Services, ConfigMaps, Jobs, Namespaces  
- [ ] Treat Secrets as opaque (metadata only in reports)  
- [ ] Handle ApiException status codes

## Architecture

This topic’s control points and relationships are shown below.

![Kubernetes client architecture](../assets/excalidraw/python-k8s-client-architecture.svg)

## Theory

### What it is

The official `kubernetes` Python package is a generated client around the Kubernetes API server. Your script loads credentials, builds typed API objects (`CoreV1Api`, `AppsV1Api`, and so on), and issues the same verbs `kubectl` uses — get, list, create, patch, delete — over HTTPS. It is not a replacement for controllers or operators; it is the library you use for inventory, health reports, CI gates, and small automation that must speak Kubernetes fluently.

### Why it matters

Platform and SRE teams live in clusters. Shelling out to `kubectl` works for one-off jobs, but Python clients give structured objects, pagination helpers, and testable code paths. Read-only inventory tools catch Pending Pods, broken Deployments, and missing Services before users do. Mutating tools (when you eventually add them) inherit Role-Based Access Control (RBAC) from a ServiceAccount — so least privilege is enforceable, not optional.

### How it works

Out of cluster, `config.load_kube_config()` reads `KUBECONFIG` or `~/.kube/config`. Inside a Pod, `config.load_incluster_config()` uses the mounted ServiceAccount token and CA. Clients then call namespaced or cluster-scoped list/get methods. Errors surface as `ApiException` with HTTP status codes: 401/403 for auth or RBAC, 404 for missing objects, 409 for conflicts. Prefer namespace-scoped lists for controllers and reports — cluster-wide scans are slower and need broader permissions.

```python
from kubernetes import config
config.load_kube_config()          # laptop / CI with kubeconfig
# config.load_incluster_config()   # Pod ServiceAccount
```

### Key concepts and comparisons

| Resource | Typical client | Automation use |
|----------|----------------|----------------|
| Pods, Namespaces, ConfigMaps, Secrets, Services | `CoreV1Api` | Inventory, health, Service endpoints |
| Deployments | `AppsV1Api` | Ready vs desired replicas |
| Jobs / CronJobs | `BatchV1Api` | Batch completion checks |

| Mode | When | Risk |
|------|------|------|
| List / get | Health checkers, audits | Low if RBAC is list/get only |
| Create / patch / delete | Controllers, apply tools | High — require `--apply`, dry-run, tickets |

Treat Secrets as opaque: report name, namespace, and type — never decode or print `data` values in logs or JSON reports.

### Common pitfalls

- Running with a cluster-admin kubeconfig “just for a script” and accidentally enabling write paths later.  
- Logging full object dumps that include Secret payloads or tokens.  
- Ignoring pagination / large namespaces and timing out CI.  
- Treating 403 as “cluster down” instead of “RBAC denied.”  
- Mutating without server-side dry-run or a clear `--apply` flag.

## Hands-on Lab

**Focus:** practise the core workflow for Kubernetes Python Client Automation

```bash
mkdir -p ~/rebash-python/module-18
cd ~/rebash-python/module-18

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'kubernetes==31.0.0'
```

### Step 1 – Fixture pod inventory

```bash
cd ~/rebash-python/module-18
source .venv/bin/activate

mkdir -p fixtures
cat > fixtures/pods.json << 'EOF'
{
  "items": [
    {"metadata": {"name": "web-a", "namespace": "demo"}, "status": {"phase": "Running"}},
    {"metadata": {"name": "web-b", "namespace": "demo"}, "status": {"phase": "Pending"}}
  ]
}
EOF

cat > k8s_pods.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def from_fixture(path: Path, namespace: str | None) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in data.get("items", []):
        ns = item["metadata"]["namespace"]
        if namespace and ns != namespace:
            continue
        rows.append({
            "name": item["metadata"]["name"],
            "namespace": ns,
            "phase": item.get("status", {}).get("phase"),
        })
    return rows


def from_cluster(namespace: str) -> list[dict]:
    from kubernetes import client, config

    config.load_kube_config()
    v1 = client.CoreV1Api()
    pod_list = v1.list_namespaced_pod(namespace)
    return [
        {
            "name": p.metadata.name,
            "namespace": p.metadata.namespace,
            "phase": p.status.phase,
        }
        for p in pod_list.items
    ]


def main() -> int:
    p = argparse.ArgumentParser(description="Pod inventory")
    p.add_argument("--namespace", default="demo")
    p.add_argument("--fixture", type=Path)
    args = p.parse_args()
    try:
        rows = (
            from_fixture(args.fixture, args.namespace)
            if args.fixture
            else from_cluster(args.namespace)
        )
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        print("hint: pass --fixture fixtures/pods.json", file=sys.stderr)
        return 1
    print(json.dumps(rows, indent=2))
    bad = [r for r in rows if r["phase"] != "Running"]
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python k8s_pods.py --fixture fixtures/pods.json; echo exit=$?
```

### Step 2 – Deployment readiness sketch

```bash
python - <<'PY'
dep = {"name": "api", "ready": 2, "desired": 3}
print("healthy" if dep["ready"] == dep["desired"] else "degraded")
print("# live: AppsV1Api().list_namespaced_deployment")
PY
```

### Step 3 – RBAC note

Document: ServiceAccount + Role `get/list` on pods only for a health checker.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-18/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Kubernetes Python Client Automation** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Running with a cluster-admin kubeconfig “just for a script” and accidentally enabling writ"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Logging full object dumps that include Secret payloads or tokens.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Kubernetes Python Client Automation changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| 403 Forbidden | RBAC | Grant least list/get |
| Config exception | No kubeconfig | Fixture or set `KUBECONFIG` |
| Slow list | Cluster-wide without need | Namespace-scope |

## Summary

- Official client + kubeconfig/in-cluster  
- Read-only inventory/health first  
- Labs for health checker and deployment validator

## Interview Questions

1. How does **Kubernetes Python Client Automation** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Infrastructure Automation — Terraform](infrastructure-automation-terraform.md)  
- [Kubernetes Health Checker lab](../labs/python-kubernetes-health-checker.md)

## References

- [kubernetes-client/python](https://github.com/kubernetes-client/python)
