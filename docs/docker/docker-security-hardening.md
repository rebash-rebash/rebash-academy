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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-11 && cd ~/rebash-docker/module-11
```

**Focus:** hands-on practice for Docker Security Hardening

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-11 && cd ~/rebash-docker/module-11
cat > Dockerfile << 'EOF'
FROM alpine:3.20
RUN adduser -D -u 10001 appuser
USER appuser
WORKDIR /home/appuser
CMD ["sleep", "3600"]
EOF
docker build -t rebash-secure:0.1.0 .
docker run -d --name rebash-sec \
  --read-only --tmpfs /tmp \
  --cap-drop=ALL \
  --security-opt=no-new-privileges:true \
  rebash-secure:0.1.0
docker exec rebash-sec id
docker rm -f rebash-sec
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
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

1. How does **Docker Security Hardening** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Container Scanning and SBOM](container-scanning-and-sbom.md)
- Depth: [Environment Variables and Secrets](environment-variables-and-secrets.md)

## References

- [Docker security](https://docs.docker.com/engine/security/)
