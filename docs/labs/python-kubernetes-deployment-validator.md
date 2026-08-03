---
title: "Lab — Python Kubernetes Deployment Validator"
description: "Validate Deployment manifests for probes, resources, and security context — fixture-first, no cluster apply."
difficulty: intermediate
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - kubernetes
  - validation
  - yaml
comments: false
---

# Lab — Python Kubernetes Deployment Validator

## Lab Overview

**Purpose:** Policy-check Deployment YAML before apply (probes, resources, non-root).

**Scenario:** Platform bans Deployments without readiness probes or resource requests. PRs must pass a validator in CI.

**Expected outcome:** CLI validates manifests offline; exit `2` on policy violations.

!!! tip "This is a lab, not a tutorial"
    Apply [Kubernetes Python Client Automation](../python/kubernetes-python-client-automation.md) and [File Handling](../python/file-handling-pathlib-json-yaml-csv.md).

## Business Scenario

A rushed release omitted readiness probes; traffic hit cold pods. Leadership wants static checks in every merge pipeline.

## Learning Objectives

- [ ] `yaml.safe_load_all` multi-doc manifests
- [ ] Assert `readinessProbe`, `resources.requests`, `securityContext.runAsNonRoot`
- [ ] Work fully offline (no cluster)

## Prerequisites

### Knowledge

- [Kubernetes Python Client Automation](../python/kubernetes-python-client-automation.md)
- [File Handling — pathlib, JSON, YAML, CSV](../python/file-handling-pathlib-json-yaml-csv.md)

### Software

PyYAML. **Estimated cost:** £0.

## Environment

```bash title="Terminal"
mkdir -p ~/rebash-lab-python-deploy/{manifests,out}
cd ~/rebash-lab-python-deploy
python3 -m venv .venv && source .venv/bin/activate
pip install 'PyYAML>=6.0,<7'
```

## Initial State

Create `manifests/good.yaml`:

```yaml title="good.yaml"
apiVersion: apps/v1
kind: Deployment
metadata: {name: api}
spec:
  template:
    spec:
      securityContext: {runAsNonRoot: true}
      containers:
        - name: api
          image: ghcr.io/acme/api:1.2.3
          readinessProbe: {httpGet: {path: /healthz, port: 8080}}
          resources: {requests: {cpu: "100m", memory: "128Mi"}}
```

Create `manifests/bad.yaml`:

```yaml title="bad.yaml"
apiVersion: apps/v1
kind: Deployment
metadata: {name: api}
spec:
  template:
    spec:
      containers:
        - name: api
          image: ghcr.io/acme/api:1.2.3
```

## Task

Create `validate_deployment.py` that walks containers and reports missing probes/resources/non-root. Ignore non-Deployment kinds.

## Validation

```bash title="Terminal"
python validate_deployment.py manifests/good.yaml; echo $?  # 0
python validate_deployment.py manifests/bad.yaml; echo $?   # 2
```

- [ ] Good exits `0`, bad exits `2`
- [ ] No kubectl/cluster required

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Nested None | Guard missing `spec.template.spec` |
| Multi-doc | Use `safe_load_all` |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-deploy
```

## Production Discussion

Graduate to Kyverno/OPA Gatekeeper for admission control; keep this Python validator for local/CI shift-left.

## Related

- Previous: [Kubernetes Health Checker](python-kubernetes-health-checker.md)
- Next: [Terraform Wrapper](python-terraform-wrapper.md)
