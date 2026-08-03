---
title: "Production Docker Patterns"
description: "Apply production Docker best practices — image versioning, registry strategy, backups, DR, scaling, and operational excellence for DevOps."
difficulty: advanced
estimated_time: "50–70 min"
technology: docker
category: docker
module: "Module 17 · Production Docker"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - docker
  - production-practices
prerequisites:
  - docker/troubleshooting-docker-containers
  - docker/docker-security-hardening
next:
  - docker/from-docker-to-kubernetes
related:
  - docker/docker-capstone-and-next-steps
  - kubernetes/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
  - CKA
tags:
  - docker
  - production
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Production Docker Patterns

## Overview







Assemble a production checklist: immutable tags, hardened images, registry retention, volume backup, health/resources, and a path to orchestrators.

Production Docker is a set of defaults: small scanned images, non-root, limits, health checks, CI promotion, and documented rollback. Compose may run small fleets; Kubernetes owns large scale.

This is a core tutorial in **Module 17 · Production Docker** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- Modules 9–16 (Compose through troubleshooting)
- [Docker Security Hardening](docker-security-hardening.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Define image versioning (SemVer + git SHA)  
- [ ] Document registry and retention strategy  
- [ ] Plan volume backup / DR  
- [ ] List scaling limits of single-host Docker  
- [ ] Complete an operational excellence checklist

## Architecture







This topic’s control points and relationships are shown below.

![Production platform](../assets/excalidraw/docker-production-platform.svg)

## Theory







### What

**Production Docker patterns** are the non-negotiable defaults for shipping containers safely: immutable digests (not `:latest`), scanning and policy gates, non-root and read-only where possible, CPU/memory limits, healthchecks, secrets outside the image, and rollback by previous digest. Orchestration may be Compose on a single host, Swarm in niches, or **Kubernetes** for multi-node — the image practices stay constant.

### Why

Convenience defaults that work in tutorials fail under load, audit, and attack. Teams that promote digests, scan in CI, and limit resources sleep better. This course prepares OCI images that a platform team can run anywhere.

### How it works

Build with multi-stage Dockerfiles, pin bases, drop privileges, and emit SBOMs. Push digests; deploy manifests reference those digests. Enforce limits and healthchecks in Compose or cluster specs. Inject secrets at runtime. On incident, redeploy the last known-good digest rather than “rebuild latest”. Scale path: single-host Compose → (optional Swarm) → Kubernetes for multi-node scheduling, service discovery, and richer policy.

### Key concepts

| Control | Production stance |
|---------|-------------------|
| Tags | No `:latest` in deploy manifests |
| Supply chain | Scan (+ sign/policy as required) |
| Privilege | Non-root, read-only when possible |
| Resources | CPU/memory limits + healthchecks |
| Secrets | Outside the image |
| Rollback | Previous digest / tag |


Codify these patterns in a platform template repository so every new service inherits sane defaults. Review exceptions (privileged mode, root user, host networking) on a schedule with an expiry date. When you move from Compose to Kubernetes, keep the same image digests and health semantics — only the scheduler changes.

### Common pitfalls

- Different images per environment with untested prod-only Dockerfiles  
- Privileged containers as a permanent exception  
- No resource limits “because the VM is big enough”  
- Rollback plans that require a developer laptop

## Hands-on Lab

### Objective

Stand up a production-minded Compose stack with pinned tags, non-root user, healthcheck, restart policy, and labels — then prove each control via `docker inspect`.

### Prerequisites

- Docker Engine with Compose v2
- Port `18170` available on the host

### Lab environment

Workspace: `~/rebash-docker/module-17`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-docker/module-17 && cd ~/rebash-docker/module-17
```

### Real-world scenario

You are hardening a small edge API before production. Requirements: pinned image tag, `unless-stopped` restart, health gate, observability labels, and non-root UID — all verifiable from inspect output.

### Step-by-step tasks

#### Task 1 – Create hardened service files

Create `Dockerfile`:

```dockerfile title="Dockerfile"
FROM python:3.12-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY app.py .
USER app
EXPOSE 8080
CMD ["python", "app.py"]
```

Create `app.py`:

```python title="app.py"
from http.server import BaseHTTPRequestHandler, HTTPServer

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok\n")
            return
        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"rebash-prod-lab\n")
            return
        self.send_error(404)
    def log_message(self, *args):
        return

HTTPServer(("0.0.0.0", 8080), H).serve_forever()
```

Create `compose.yaml`:

```yaml title="compose.yaml"
services:
  edge:
    build:
      context: .
      dockerfile: Dockerfile
    image: rebash-prod-lab:1.0.0
    user: "app"
    ports:
      - "18170:8080"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz')\""]
      interval: 10s
      timeout: 3s
      retries: 3
    labels:
      app: rebash-prod-lab
      env: lab
      owner: platform
```

Start the stack:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-docker/module-17
docker compose up -d --build
docker compose ps | tee prod-ps.txt
grep -q rebash-prod-lab prod-ps.txt
```

!!! example "Expected output"
    Service shows running in `prod-ps.txt`.


#### Task 2 – HTTP and health verification

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-docker/module-17
sleep 15
curl -sS http://127.0.0.1:18170/healthz | tee prod-health.txt
curl -sS http://127.0.0.1:18170/ | tee prod-root.txt
grep -q ok prod-health.txt
grep -q rebash-prod-lab prod-root.txt
```

!!! example "Expected output"
    Health returns `ok`; root path returns `rebash-prod-lab`.


#### Task 3 – Prove production controls via inspect

{% raw %}
``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-docker/module-17
CID="$(docker compose ps -q edge)"
docker inspect "$CID" --format 'User={{ "{{" }}.Config.User{{ "}}" }} Restart={{ "{{" }}.HostConfig.RestartPolicy.Name{{ "}}" }} Health={{ "{{" }}.State.Health.Status{{ "}}" }}' | tee prod-inspect.txt
docker inspect "$CID" --format '{{ "{{" }}.Config.Labels{{ "}}" }}' | tee prod-labels.txt
grep -q 'User=app' prod-inspect.txt
grep -q 'unless-stopped' prod-inspect.txt
grep -q 'rebash-prod-lab' prod-labels.txt
```
{% endraw %}

!!! example "Expected output"
    Inspect shows non-root user, restart policy, labels, and health status.


### Validation steps

- [ ] Compose file pins image tag and sets restart policy
- [ ] Healthcheck and HTTP endpoints respond
- [ ] Inspect confirms User, RestartPolicy, and Labels
- [ ] Cleanup tears down stack and volumes

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| nginx fails as non-root | Default nginx wants root | Use the Python edge service in this lab |
| Healthcheck fail | Probe before app listens | Wait 15s after `compose up` |
| Port 18170 in use | Another lab | Change host port in compose |
| Permission denied on config mount | Wrong file ownership | Keep config world-readable on host |

### Challenge exercise

Add a `deploy.resources.limits` block (Compose v3+) for memory and prove limits in inspect on supported engines.

### Learning outcomes

- Applied pinned tags, restart policy, and labels in Compose
- Ran nginx as non-root with a custom config
- Validated healthchecks end-to-end
- Proved controls with inspect instead of documentation alone

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-docker/module-17
docker compose down -v --remove-orphans
docker rmi rebash-prod-lab:1.0.0 2>/dev/null || true
rm -f *.txt
```

## Validation







- [ ] Lab commands run under `~/rebash-docker/module-17/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Production Docker Patterns** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations







- Treat credentials and tokens for docker as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes







!!! warning "Different images per environment with untested prod-only Dockerfiles  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Privileged containers as a permanent exception  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Production Docker Patterns changes as code and review them in pull requests
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







You can ship and operate containers with production discipline and hand off cleanly to Kubernetes.

## Interview Questions




1. Restart policies you use in production?
2. Healthchecks — what should they verify?
3. Immutable infrastructure with containers means what?
4. How do you handle config changes safely?
5. Resource requests/limits mindset even on Docker hosts?

!!! tip "Sample answer — question 2"
    Inspect restart policy and health state, then application logs.

!!! tip "Sample answer — question 4"
    Non-root, minimal images, scanned bases, no secrets in images.

## Related Tutorials







- [Course overview](index.md)
- [From Docker to Kubernetes](from-docker-to-kubernetes.md) · [Capstone and next steps](docker-capstone-and-next-steps.md)

## References







- [Docker production best practices](https://docs.docker.com/develop/security-best-practices/)
