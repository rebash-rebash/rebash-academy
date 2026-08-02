---
title: "Dockerfile Best Practices and Multi-Stage Builds"
description: "Optimise Docker images with multi-stage builds, BuildKit, Alpine vs distroless bases, and layer caching for production DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 6 · Image Optimisation"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - multi-stage-builds
  - buildkit
prerequisites:
  - docker/building-images-with-dockerfile
next:
  - docker/volumes-and-persistent-storage
related:
  - docker/container-scanning-and-sbom
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - multi-stage
  - buildkit
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Dockerfile Best Practices and Multi-Stage Builds

## Overview







Shrink and harden images with multi-stage builds, sensible bases, BuildKit cache, and ordered layers.

Smaller images pull faster, scan cleaner, and attack less surface. **Multi-stage** builds compile in a fat stage and copy artefacts into a slim runtime stage.

This is a core tutorial in **Module 6 · Image Optimisation** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Building Images with Dockerfile](building-images-with-dockerfile.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Write a multi-stage Dockerfile  
- [ ] Compare Alpine, Debian slim, distroless  
- [ ] Order layers for cache hits  
- [ ] Enable BuildKit features  
- [ ] Measure image size before/after

## Architecture







This topic’s control points and relationships are shown below.

![Image layers](../assets/excalidraw/docker-image-layers.svg)

## Theory







### What

**Best practices** keep images small, reproducible, and safer: pin versions, use `.dockerignore`, drop build tools from the final image, and run as non-root. **Multi-stage builds** use multiple `FROM` sections so compile toolchains stay in intermediate stages while the final stage copies only artefacts.

### Why

Fat images slow pulls, expand vulnerability surface, and cost more in registries. Multi-stage builds are the standard way to ship Go, Java, and Node production binaries without compilers. Cache-aware ordering keeps CI fast.

### How it works

Declare a builder stage (`FROM golang:… AS build`) that compiles, then a runtime stage (`FROM gcr.io/distroless/static` or a minimal distro) that `COPY --from=build` the binary. Combine `RUN` lines thoughtfully: fewer layers vs granular cache invalidation is a trade-off. Pin base images and dependency versions. Enable BuildKit features (cache mounts) when appropriate. Distroless or minimal images remove shells — great for production, harder for `docker exec` debugging (use debug sidecars or ephemeral debug images).

| Technique | Why |
|-----------|-----|
| Multi-stage | Drop compilers from the final image |
| `.dockerignore` | Smaller, safer build context |
| Pin versions | Reproducible builds |
| Careful `RUN` grouping | Balance layers vs cache |
| Distroless / minimal | Less shell and CVE surface |

### Key concepts

- **Attack surface** — fewer packages, fewer CVEs  
- **Cache mounts** — accelerate package downloads without bloating layers  
- **SBOM-friendly builds** — know what you shipped  
- **Provenance** — attestations in advanced supply-chain setups  

### Common pitfalls

- Copying the entire build stage into the final image by mistake  
- “Optimising” by disabling cache in CI always (slow feedback)  
- Keeping package manager caches in layers  
- Using multi-stage complexity when a single slim stage would do

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Dockerfile Best Practices and Multi-Stage Builds** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-06`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-06 && cd ~/rebash-docker/module-06
```

### Real-world scenario

You are validating **Dockerfile Best Practices and Multi-Stage Builds** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

### Step-by-step tasks

#### Task 1 – Author Dockerfile and build

Images are the deployment unit — build a tagged local image.

```bash
cat > Dockerfile << 'EOF'
FROM alpine:3.20 AS build
WORKDIR /src
RUN echo 'artefact' > app.txt
FROM alpine:3.20
COPY --from=build /src/app.txt /app.txt
CMD ["cat", "/app.txt"]
EOF
docker build -t rebash-lab:local .
docker image ls rebash-lab:local
```

**Expected output:** Image `rebash-lab:local` listed with a recent CREATED time.

#### Task 2 – Run and verify output

Prove the runtime image does what the Dockerfile claims.

```bash
docker run --rm --name rebash-lab rebash-lab:local | tee out.txt
test "$(cat out.txt)" = 'artefact'
```

**Expected output:** out.txt contains exactly `artefact`.

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







- [ ] Lab commands run under `~/rebash-docker/module-06/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Dockerfile Best Practices and Multi-Stage Builds** always combines:

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







!!! warning "Copying the entire build stage into the final image by mistake  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "“Optimising” by disabling cache in CI always (slow feedback)  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Dockerfile Best Practices and Multi-Stage Builds changes as code and review them in pull requests
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







**Dockerfile Best Practices and Multi-Stage Builds** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. How do multi-stage builds improve security and size?
2. What should the final stage contain?
3. Layer caching tips that actually help CI?
4. Why order Dockerfile instructions carefully?
5. When is distroless a good final base?

!!! tip "Sample answer — question 2"
    Compare image sizes and docker history before/after multi-stage.

!!! tip "Sample answer — question 4"
    Keep build tools out of production images and pin base digests.

## Related Tutorials







- [Course overview](index.md)
- [Volumes and Persistent Storage](volumes-and-persistent-storage.md)

## References







- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/) · [BuildKit](https://docs.docker.com/build/buildkit/)
