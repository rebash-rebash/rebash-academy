---
title: "Docker in CI/CD Pipelines"
description: "Build, scan, and promote multi-arch images with Buildx in GitHub Actions and GitLab CI for DevOps delivery."
difficulty: intermediate
estimated_time: "50–70 min"
technology: docker
category: docker
module: "Module 15 · Docker in CI/CD"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - docker
  - ci-cd
  - buildx
prerequisites:
  - docker/docker-performance-and-resource-limits
  - docker/container-scanning-and-sbom
next:
  - docker/troubleshooting-docker-containers
related:
  - git/github-actions-for-devops
  - github-actions/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - cicd
  - buildx
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker in CI/CD Pipelines

## Overview







Design a build → scan → push → promote pipeline using Buildx for multi-architecture images and immutable tags.

CI builds images from Git; never “docker build on a laptop then scp.” **Buildx** enables `linux/amd64` + `linux/arm64`. Promote by retagging digests across environments.

This is a core tutorial in **Module 15 · Docker in CI/CD** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Docker Performance and Resource Limits](docker-performance-and-resource-limits.md)
- [Container Scanning and SBOM](container-scanning-and-sbom.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Sketch build/scan/push stages  
- [ ] Use Buildx multi-platform builds  
- [ ] Tag with git SHA  
- [ ] Outline GitHub Actions / GitLab CI jobs

## Architecture







This topic’s control points and relationships are shown below.

![CI/CD pipeline](../assets/excalidraw/docker-cicd-pipeline.svg)

## Theory







### What

CI/CD pipelines **build**, **scan**, **push**, and **promote** container images. Typical steps use `docker buildx build`, a vulnerability gate (for example Trivy), push to a registry, then retag an immutable digest for staging and production. Authentication should prefer **OIDC** to cloud registries over long-lived passwords.

### Why

Images are the deployable unit for most cloud-native systems. Building on laptops and copying tarballs does not scale or audit. Pipelines encode the quality gates that protect production and make promotions repeatable.

### How it works

On pull request, build (and optionally scan) without necessarily pushing production tags. On main, build once, push by digest, record provenance. Promotion moves the same digest across environments — do not rebuild differently “for prod”. GitHub Actions and similar systems need careful permissions: least-privilege `packages: write`, ephemeral credentials, and pinned actions. Cache layers with registry or BuildKit caches to keep feedback fast.

| Stage | Action |
|-------|--------|
| Build | `docker buildx build` |
| Scan | Trivy (or equivalent) gate |
| Push | Registry |
| Promote | Retag digest to staging/prod |

In workflow docs, escape expressions such as {% raw %}`${{ github.sha }}`{% endraw %} when embedding examples in MkDocs.

### Key concepts

- **Build once, promote many** — environment parity  
- **OIDC federation** — short-lived cloud auth  
- **Provenance / attestations** — advanced supply chain  
- **Ephemeral runners** — clean build hosts  


Keep pipeline YAML next to the Dockerfile so reviewers see build and gate changes together. Fail closed on CRITICAL vulnerabilities for images destined to production, with a documented exception path. Emit the image digest as a pipeline output so GitOps commits and release notes can reference it automatically.

### Common pitfalls

- Storing Docker Hub passwords forever in CI secrets  
- Pushing `:latest` as the only promotion signal  
- Using privileged DinD without understanding risks  
- Different Dockerfiles per environment that drift

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Docker in CI/CD Pipelines** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-15/.github/workflows`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-15/.github/workflows && cd ~/rebash-docker/module-15/.github/workflows
```

### Real-world scenario

You are validating **Docker in CI/CD Pipelines** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

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







- [ ] Lab commands run under `~/rebash-docker/module-15/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Docker in CI/CD Pipelines** always combines:

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







!!! warning "Storing Docker Hub passwords forever in CI secrets  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Pushing `:latest` as the only promotion signal  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Docker in CI/CD Pipelines changes as code and review them in pull requests
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







**Docker in CI/CD Pipelines** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. Why tag CI images with git SHA?
2. DinD versus Kaniko/Buildah trade-offs?
3. How do you cache layers safely in CI?
4. What should not be in CI build contexts?
5. How do you prove provenance of an image?

!!! tip "Sample answer — question 2"
    Check Dockerfile path/context, registry login, and whether the job ran on the expected commit SHA.

!!! tip "Sample answer — question 4"
    Never use long-lived registry passwords in clear logs. Prefer OIDC.

## Related Tutorials







- [Course overview](index.md)
- [Troubleshooting Docker Containers](troubleshooting-docker-containers.md)

## References







- [Buildx](https://docs.docker.com/build/building/multi-platform/) · [build-push-action](https://github.com/docker/build-push-action)
