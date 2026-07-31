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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-15/.github/workflows && cd ~/rebash-docker/module-15/.github/workflows
```

**Focus:** hands-on practice for Docker in CI/CD Pipelines

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-15/.github/workflows
cd ~/rebash-docker/module-15
cat > Dockerfile << 'EOF'
FROM alpine:3.20
CMD ["echo", "ci-image"]
EOF

docker buildx version || docker buildx create --use
docker buildx build -t rebash-ci:local --load .

cat > .github/workflows/docker.yml << 'EOF'
name: docker
on:
  pull_request:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: false
          tags: rebash-ci:${{ "{{" }} github.sha {{ "}}" }}
EOF

git init -b main 2>/dev/null || true
echo "Pipeline skeleton ready" 
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
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

1. How does **Docker in CI/CD Pipelines** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Troubleshooting Docker Containers](troubleshooting-docker-containers.md)

## References

- [Buildx](https://docs.docker.com/build/building/multi-platform/) · [build-push-action](https://github.com/docker/build-push-action)
