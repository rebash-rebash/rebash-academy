---
title: "Docker Security Hardening"
description: "Harden containers with non-root users, dropped capabilities, read-only filesystems, seccomp/AppArmor, and secrets handling for DevOps."
difficulty: advanced
estimated_time: "50–70 min"
technology: docker
category: docker
module: "Module 11 · Security"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - docker
  - container-security
prerequisites:
  - docker/container-registries-and-distribution
next:
  - docker/container-scanning-and-sbom
related:
  - docker/environment-variables-and-secrets
  - security/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - security
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker Security Hardening

## Overview







Run a container as non-root with a read-only root filesystem, dropped capabilities, and no secrets in the image layers.

Default containers often run as root with a writable filesystem — fine for demos, risky in production. Defence in depth: user, capabilities, seccomp/AppArmor, read-only FS, secrets mounts.

This is a core tutorial in **Module 11 · Security** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Container Registries and Distribution](container-registries-and-distribution.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Build/run as non-root `USER`  
- [ ] Drop Linux capabilities  
- [ ] Use `--read-only` + writable tmp mounts  
- [ ] Outline seccomp / AppArmor roles  
- [ ] Keep secrets out of `ENV` in images

## Architecture







This topic’s control points and relationships are shown below.

![Production platform](../assets/excalidraw/docker-production-platform.svg)

## Theory







### What

**Container hardening** reduces privilege and blast radius: non-root users, dropped Linux capabilities, read-only root filesystems, secret handling outside the image, and optionally **rootless** Engine. Orchestrators add further controls (Pod Security, seccomp), but image and runtime defaults still matter on Docker hosts.

### Why

Containers share a kernel. A process running as root with the Docker socket mounted can compromise the host. DevOps images often start from convenience bases that run as UID 0 — fine for demos, unsafe as a production default.

### How it works

Set `USER` in the Dockerfile to a non-root UID and align Kubernetes `runAsNonRoot` later. Start with `--cap-drop=ALL` and add back only required capabilities. Use `--read-only` plus `tmpfs` for `/tmp` when apps allow it. Never `COPY` production secrets into layers; inject at runtime via environment (carefully), files, or orchestrator secret stores. Prefer rootless Engine on locked-down laptops; understand its networking limits. Keep the daemon and hosts patched.

| Control | Practice |
|---------|----------|
| Non-root | `USER` in Dockerfile + `runAsNonRoot` |
| Capabilities | `--cap-drop=ALL` then add minimal |
| Read-only FS | `--read-only` + `tmpfs` for `/tmp` |
| Rootless engine | Reduce daemon privilege |
| Secrets | Runtime mounts — not `COPY secret` |

### Key concepts

- **Docker socket** — treat as root  
- **Seccomp / AppArmor** — default profiles block dangerous syscalls  
- **Supply chain** — signed bases and scanned images complement runtime hardening  
- **Break-glass** — debug images may relax rules temporarily  

### Common pitfalls

- Mounting `docker.sock` into random utility containers  
- Running privileged (`--privileged`) to “make it work”  
- Baking cloud keys into images  
- Dropping capabilities without testing startup (then disabling all hardening)

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Docker Security Hardening** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-11`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-11 && cd ~/rebash-docker/module-11
```

### Real-world scenario

You are validating **Docker Security Hardening** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

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







- [ ] Lab commands run under `~/rebash-docker/module-11/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Docker Security Hardening** always combines:

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







!!! warning "Mounting `docker.sock` into random utility containers  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Running privileged (`--privileged`) to “make it work”  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Docker Security Hardening changes as code and review them in pull requests
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







**Docker Security Hardening** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. List three hardening flags you use on docker run.
2. Why drop capabilities?
3. Read-only root filesystem — when it breaks apps?
4. Risks of privileged containers?
5. How do user namespaces help?

!!! tip "Sample answer — question 2"
    Inspect HostConfig for privileged, capabilities, and mounts.

!!! tip "Sample answer — question 4"
    Default deny: non-root, cap-drop ALL, no privileged, minimal mounts.

## Related Tutorials







- [Course overview](index.md)
- [Container Scanning and SBOM](container-scanning-and-sbom.md)
- Depth: [Environment Variables and Secrets](environment-variables-and-secrets.md)

## References







- [Docker security](https://docs.docker.com/engine/security/)
