---
title: "Working with Docker Images"
description: "Pull, tag, push, save, and load Docker images — understand layers and registries for DevOps image workflows."
difficulty: beginner
estimated_time: "40–55 min"
technology: docker
category: docker
module: "Module 4 · Images"
career_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - docker
  - container-images
prerequisites:
  - docker/running-your-first-container
next:
  - docker/building-images-with-dockerfile
related:
  - docker/container-registries-and-distribution
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - images
  - layers
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Working with Docker Images

## Overview

Manage images end to end: pull, inspect layers, tag for a registry, save/load for air-gapped moves, and prune safely.

Images are layered, content-addressed artefacts. Tags (`:latest`, `:1.2.3`) are mutable pointers — production prefers digests or immutable tags.

This is a core tutorial in **Module 4 · Images** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Running Your First Container](running-your-first-container.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] `docker pull` / `images` / `history`  
- [ ] Tag for a target registry  
- [ ] Explain layers and cache reuse  
- [ ] `docker save` / `load`  
- [ ] Prune unused images carefully

## Architecture

This topic’s control points and relationships are shown below.

![Image layers](../assets/excalidraw/docker-image-layers.svg)

## Theory

### What

**Images** are immutable, layered packages identified by name, tag, and content **digest**. You pull them from registries, tag them for promotion, inspect layer history, save/load tarballs for air-gapped moves, and prune unused images to reclaim disk.

### Why

Deployments should promote digests, not floating tags. Understanding layers explains cache behaviour and image size. Disk-full CI runners are often unpruned images and build cache — operational hygiene is part of image literacy.

### How it works

`docker pull nginx:alpine` downloads missing layers. `docker images` (or `docker image ls`) lists local images. `docker history` shows how layers were created. `docker tag` adds a new name pointing at the same image ID — tagging does not create a new filesystem. `docker push` uploads to a registry after login. `save`/`load` move image tarballs without a registry. Digests (`repo@sha256:…`) pin exact content; tags like `:latest` can move.

| Action | Command |
|--------|---------|
| Pull | `docker pull nginx:alpine` |
| List | `docker images` |
| Layers | `docker history <image>` |
| Tag | `docker tag src registry/app:1.0.0` |
| Save/load | `docker save` / `docker load` |
| Remove | `docker rmi` / `docker image prune` |

### Key concepts

- **Tag vs digest** — human label vs immutable content address  
- **Shared layers** — storage deduplication across images  
- **Multi-arch manifests** — one name, several platform variants  
- **Prune carefully** — do not delete images still needed by stopped containers you care about  

### Common pitfalls

- Promoting only `:latest` through environments  
- Retagging without rebuilding and assuming content changed  
- Leaving dangling images until the disk fills  
- Trusting a tag on a public registry without pinning a digest in production

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-04 && cd ~/rebash-docker/module-04
```

**Focus:** hands-on practice for Working with Docker Images

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-04 && cd ~/rebash-docker/module-04
docker pull alpine:3.20
docker images alpine
docker history alpine:3.20
docker tag alpine:3.20 rebash-local/alpine:lab
docker save rebash-local/alpine:lab -o alpine-lab.tar
docker rmi rebash-local/alpine:lab
docker load -i alpine-lab.tar
docker images rebash-local/alpine
rm -f alpine-lab.tar
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-docker/module-04/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Working with Docker Images** always combines:

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

!!! warning "Promoting only `:latest` through environments  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Retagging without rebuilding and assuming content changed  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Working with Docker Images changes as code and review them in pull requests
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

**Working with Docker Images** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Working with Docker Images** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Building Images with Dockerfile](building-images-with-dockerfile.md)

## References

- [Docker images](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)
