---
title: "Docker Performance and Resource Limits"
description: "Set CPU and memory limits, understand storage drivers, and optimise container lifecycle for production DevOps performance."
difficulty: intermediate
estimated_time: "40–55 min"
technology: docker
category: docker
module: "Module 14 · Performance"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - performance
  - resource-limits
prerequisites:
  - docker/container-logging-and-monitoring
next:
  - docker/docker-in-ci-cd-pipelines
related:
  - docker/production-docker-patterns
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - cpu
  - memory
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker Performance and Resource Limits

## Overview







Apply CPU and memory limits, observe container stats, and relate storage drivers and lifecycle to performance.

Unlimited containers can starve the host. Set `--memory` / `--cpus` (or Compose `deploy.resources`) so noisy neighbours fail safely. Know your storage driver (`overlay2`) and prune policy.

This is a core tutorial in **Module 14 · Performance** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Container Logging and Monitoring](container-logging-and-monitoring.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Set memory and CPU limits  
- [ ] Read `docker stats`  
- [ ] Explain OOM kill behaviour  
- [ ] Name storage driver implications  
- [ ] Prune safely for disk

## Architecture







This topic’s control points and relationships are shown below.

![Container lifecycle](../assets/excalidraw/docker-container-lifecycle.svg)

## Theory







### What

Containers can consume all host CPU, memory, and process slots unless you set **resource limits**. Docker and Compose expose flags such as `--memory`, `--cpus`, and `--pids-limit`. Disk usage from images, layers, and build cache also needs active management with `docker system df` and scheduled prune policies.

### Why

One runaway container can starve neighbours on a shared runner or VM — a classic noisy-neighbour incident. Limits make failure modes predictable (OOM kill) instead of mysterious host freezes. Performance work also includes image size and registry pull time.

### How it works

Memory limits constrain cgroup memory; exceeding them typically triggers the OOM killer and stops the container. CPU limits throttle scheduling share. PIDs limits mitigate fork bombs. Design applications to honour limits (buffer sizes, worker counts). Watch `docker stats` during load tests. On disk, remove unused images and build cache regularly in CI; pin retention for artefacts you still need. Multi-stage and slim bases reduce pull latency more than micro-optimising Go flags alone.

| Limit | Flag / Compose |
|-------|----------------|
| Memory | `--memory` / `mem_limit` |
| CPU | `--cpus` / `cpus` |
| PIDs | `--pids-limit` |

### Key concepts

- **Requests vs limits** — Kubernetes distinguishes them; Docker flags are closer to limits  
- **OOM diagnostics** — exit codes and host dmesg  
- **Build performance** — cache mounts, remote cache  
- **I/O** — volume performance differs bind vs named volume drivers  


Load-test with realistic concurrency before you copy limits from a tutorial. Language runtimes often need explicit memory settings (heap size) that sit *below* the container limit so the kernel OOM killer is not your first garbage collector. In CI, separate heavy image builds onto larger runners instead of raising every job’s limits blindly.

### Common pitfalls

- Unlimited containers on shared CI hosts  
- Setting memory so low the JVM/runtime cannot start  
- Never pruning build cache on busy runners  
- Blaming “Docker slowness” when the image is multi-gigabytes

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Docker Performance and Resource Limits** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-14`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-14 && cd ~/rebash-docker/module-14
```

### Real-world scenario

You are validating **Docker Performance and Resource Limits** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

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







- [ ] Lab commands run under `~/rebash-docker/module-14/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Docker Performance and Resource Limits** always combines:

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







!!! warning "Unlimited containers on shared CI hosts  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Setting memory so low the JVM/runtime cannot start  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Docker Performance and Resource Limits changes as code and review them in pull requests
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







**Docker Performance and Resource Limits** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. How do --memory and --cpus protect a host?
2. What does docker stats show you?
3. OOM kills — how do you confirm?
4. When do limits cause false failures?
5. How do cgroups relate to containers?

!!! tip "Sample answer — question 2"
    Use docker stats and inspect OOM fields / exit codes.

!!! tip "Sample answer — question 4"
    Set limits in shared environments so one container cannot starve neighbours.

## Related Tutorials







- [Course overview](index.md)
- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)

## References







- [Runtime resource constraints](https://docs.docker.com/engine/containers/resource_constraints/)
