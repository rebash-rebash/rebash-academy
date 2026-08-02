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
last_updated: "2026-07-31"
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

Build or run a real Docker solution for **Production Docker Patterns** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-17`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-17 && cd ~/rebash-docker/module-17
```

### Real-world scenario

You are validating **Production Docker Patterns** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

### Step-by-step tasks

#### Task 1 – Run and inspect a container

Start from a known image, publish a port, and verify HTTP.

```bash
docker run -d --name rebash-lab -p 18080:80 nginx:alpine
docker ps --filter name=rebash-lab
curl -sI http://127.0.0.1:18080 | head -n 5 | tee headers.txt
docker logs rebash-lab 2>&1 | head -n 10 | tee logs.txt
```

**Expected output:** Container Up; HTTP 200 in headers.txt.

#### Task 2 – Inspect runtime config

Use inspect for status — production debugging rarely starts with guesswork.

```bash
docker inspect rebash-lab --format '{{ "{{" }}.State.Status{{ "}}" }} {{ "{{" }}.Config.Image{{ "}}" }}' | tee inspect.txt
test -s inspect.txt
```

**Expected output:** inspect.txt shows `running` and the nginx image.

### Validation steps

- [ ] Container or image behaves as Expected output describes
- [ ] Ports respond or command output matches
- [ ] Cleanup removes lab resources

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| port is already allocated | Previous lab left a container | `docker rm -f` the old name or change port |
| permission denied | User not in docker group | Use rootless Docker or fix group membership |
| manifest unknown | Bad tag | Pin a real tag such as `nginx:alpine` |

### Challenge exercise

Add a non-root USER (or Compose healthcheck) and prove it with inspect.

### Learning outcomes

- Executed a real Docker workflow
- Captured evidence files
- Removed disposable resources

### Cleanup

```bash
docker rm -f rebash-lab 2>/dev/null || true
docker rmi rebash-lab:local 2>/dev/null || true
docker compose down -v 2>/dev/null || true
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
