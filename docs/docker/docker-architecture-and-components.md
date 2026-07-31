---
title: "Docker Architecture and Components"
description: "Map Docker CLI, dockerd, containerd, and runc — how the engine, images, and containers fit together for DevOps."
difficulty: beginner
estimated_time: "35–50 min"
technology: docker
category: docker
module: "Module 1 · Container Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - container-runtime
prerequisites:
  - docker/introduction-to-containers-and-docker
next:
  - docker/docker-installation-and-setup
related:
  - kubernetes/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - architecture
  - containerd
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker Architecture and Components

## Overview

Describe the Docker client–daemon path and the roles of `dockerd`, `containerd`, and the OCI runtime so you can debug “where did my request fail?”

You talk to the **Docker CLI**; it calls the **Docker Engine API** on `dockerd`. The daemon uses **containerd** and **runc** to create containers on the host kernel.

This is a core tutorial in **Module 1 · Container Fundamentals** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Introduction to Containers and Docker](introduction-to-containers-and-docker.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Trace CLI → dockerd → containerd → runc  
- [ ] Distinguish image, container, and registry  
- [ ] Know what `docker context` selects  
- [ ] Relate namespaces/cgroups to isolation

## Architecture

This topic’s control points and relationships are shown below.

![Docker architecture](../assets/excalidraw/docker-architecture.svg)

## Theory

### What

Docker’s architecture separates the **CLI**, the **Engine (`dockerd`)**, **containerd**, and an **OCI runtime** such as `runc`, all sitting on the **host kernel**. Images, containers, networks, and volumes are API objects the daemon manages. Registries store images remotely.

### Why

Troubleshooting “Docker is broken” means knowing which layer failed: CLI talking to the wrong context, daemon down, pull failing in containerd, or runtime/kernel limits. Production platforms (and Kubernetes) reuse pieces of this stack — especially containerd and OCI — so the mental model transfers.

### How it works

You type `docker` commands; the CLI calls the Engine API (local Unix socket or TCP). `dockerd` orchestrates networks, volumes, and higher-level UX. It delegates image pull and container lifecycle to **containerd**, which invokes **runc** to start the process in namespaces/cgroups. An **image** is immutable layers plus config; a **container** adds a writable layer and process state; a **registry** (Docker Hub, GitHub Container Registry, Amazon Elastic Container Registry) is the remote store.

| Component | Role |
|-----------|------|
| Docker CLI | User interface (`docker`) |
| dockerd | Engine API, networks, volumes |
| containerd | Image pull, container lifecycle |
| runc | OCI runtime — starts the process |
| Host kernel | Namespaces, cgroups, filesystems |

### Key concepts

- **Client–daemon** — CLI is not the container runtime  
- **Contexts** — CLI can point at remote engines  
- **Rootful vs rootless** — privilege model of the daemon  
- **Shim / supervisors** — keep containers reparented correctly after daemon restarts  

### Common pitfalls

- Exposing the Docker socket without understanding it is root-equivalent  
- Debugging inside the CLI when `dockerd` is the failing component  
- Assuming Desktop networking equals Linux Engine networking  
- Confusing image ID, digest, and tag

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-01-arch && cd ~/rebash-docker/module-01-arch
```

**Focus:** hands-on practice for Docker Architecture and Components

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-01-arch && cd ~/rebash-docker/module-01-arch
cat > architecture.md << 'EOF'
CLI → dockerd → containerd → runc → kernel
EOF
docker info 2>/dev/null | head -n 30 || echo "Need Module 2 install"
docker context ls 2>/dev/null || true
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-docker/module-01-arch/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Docker Architecture and Components** always combines:

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

!!! warning "Exposing the Docker socket without understanding it is root-equivalent  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Debugging inside the CLI when `dockerd` is the failing component  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Docker Architecture and Components changes as code and review them in pull requests
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

**Docker Architecture and Components** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Docker Architecture and Components** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Docker Installation and Setup](docker-installation-and-setup.md)

## References

- [Docker Engine architecture](https://docs.docker.com/engine/)
