---
title: Docker in CI/CD Pipelines
description: Build, test, scan, and push container images in GitHub Actions and GitLab CI — including Docker-in-Docker patterns, caching, and production pipeline design.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - cicd
  - github-actions
  - gitlab-ci
  - dind
prerequisites:
  - Building Images with Dockerfile
  - Container Registries and Distribution
  - Git in CI/CD and DevOps
comments: false
---

# Docker in CI/CD Pipelines

## Overview

Containers are the standard artifact in modern CI/CD: build once in the pipeline, push to a registry, deploy everywhere. This tutorial shows how to integrate Docker builds into **GitHub Actions** and **GitLab CI**, manage credentials safely, cache layers for speed, and choose between **Docker socket binding** and **Docker-in-Docker (DinD)** runners.

This is **Tutorial 16** in **Module 6: Production & Beyond** of the REBASH Academy Docker track.

## Prerequisites

- [Building Images with Dockerfile](building-images-with-dockerfile.md)
- [Container Registries and Distribution](container-registries-and-distribution.md)
- [Git in CI/CD and DevOps](../git/git-in-ci-cd-and-devops.md) — pipeline triggers and commit SHA pinning
- A GitHub or GitLab account with CI minutes available
- A container registry (Docker Hub, GitHub Container Registry, or GitLab Container Registry)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Design a CI pipeline stage that builds and tags Docker images from Git events
- [ ] Push images to a registry using short-lived CI credentials
- [ ] Compare Docker socket binding vs Docker-in-Docker and choose appropriately
- [ ] Implement layer caching in GitHub Actions and GitLab CI
- [ ] Pin image tags to commit SHA for traceability
- [ ] Add image scanning and promotion gates before production deploy

## Architecture

```d2
direction: right

Git: Git {
        PUSH: "Push / PR / Tag"
        SHA: "Commit SHA"
    }
    CI: Runner {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        CLONE: "Clone repo"
        BUILD: "docker build"
        SCAN: "Image scan"
        PUSHIMG: "docker push"
    }
    Registry: Registry {
        REG: "ghcr.io / registry.gitlab.com"
    }
    Deploy: Deploy {
        STG: Staging
        PROD: Production
    }
    Git.PUSH -> CI.CLONE
    CI.CLONE -> CI.BUILD
    Git.SHA -> CI.BUILD
    CI.BUILD -> CI.SCAN
    CI.SCAN -> CI.PUSHIMG
    CI.PUSHIMG -> Registry.REG
    Registry.REG -> Deploy.STG
    Registry.REG -> Deploy.PROD
```

## Theory

### Why Docker in CI?

| Benefit | Explanation |
|---------|-------------|
| **Reproducibility** | Same Dockerfile produces the same artifact on every branch |
| **Immutability** | Image digest + commit SHA = auditable deployment identity |
| **Speed** | Parallel test jobs; cached layers reduce build time |
| **Security gate** | Scan images before they reach production clusters |
| **Deploy parity** | Staging and prod run identical container artifacts |

The pipeline typically runs: **lint → unit test → build image → scan → push → deploy**.

### Image tagging strategy

| Tag | When to use | Example |
|-----|-------------|---------|
| **Commit SHA** | Every build; immutable traceability | `myapp:a1b2c3d4` |
| **Branch name** | Dev/staging latest for a branch | `myapp:main` |
| **Semver tag** | Release promotion from Git tag | `myapp:1.4.2` |
| **latest** | Convenience only — never prod | `myapp:latest` |

Production should reference **digest** or **SHA tag**, not floating `latest`.

### Runner Docker access models

CI runners need a Docker daemon to build images. Two common patterns:

| Model | How it works | Pros | Cons |
|-------|--------------|------|------|
| **Socket bind** | Mount `/var/run/docker.sock` into job | Fast; uses host daemon | Shared daemon; security risk on multi-tenant runners |
| **Docker-in-Docker (DinD)** | Run `docker:dind` sidecar or service | Isolated daemon per job | Slower startup; TLS setup; privileged mode often required |
| **Kaniko / Buildah** | Daemonless build | No Docker socket; good for K8s | Different CLI; not full Docker feature parity |
| **BuildKit remote** | Connect to remote buildkitd | Scalable builds | Extra infrastructure |

For **shared GitHub-hosted runners**, prefer official `docker/build-push-action` (uses BuildKit) or Kaniko. For **self-hosted runners**, socket bind is common but must be locked down.

### Docker-in-Docker (DinD) essentials

DinD runs a Docker daemon **inside** a container. GitLab CI documents this as a `docker:dind` **service** alongside your job image.

Key points:

1. **Privileged mode** — DinD often requires `privileged: true` (GitLab) or equivalent. Treat as a security boundary.
2. **TLS variables** — Set `DOCKER_TLS_CERTDIR` appropriately. GitLab defaults handle cert generation between job and dind service.
3. **Wait for daemon** — Job must wait until `docker info` succeeds before building.
4. **Storage driver** — Use `overlay2`; avoid devicemapper in CI.
5. **Not the same as socket mount** — DinD is isolated; socket mount shares the host daemon.

!!! warning "DinD vs socket mount"
    Documentation and blog posts conflate these. **Socket mount** (`-v /var/run/docker.sock`) is *not* DinD — it delegates to the host daemon. True DinD starts a nested `dockerd`.

### Secrets in CI

Never embed registry passwords in Dockerfiles or compose files. Use:

| Platform | Secret mechanism |
|----------|------------------|
| GitHub Actions | Repository secrets; `GITHUB_TOKEN` for ghcr.io |
| GitLab CI | CI/CD variables (masked, protected) |
| Both | OIDC federation to cloud registries (preferred at scale) |

Login pattern:

```bash
echo "$REGISTRY_PASSWORD" | docker login "$REGISTRY" -u "$REGISTRY_USER" --password-stdin
```

## Hands-on Lab

### Lab 1 — Minimal GitHub Actions build and push

Create `.github/workflows/docker.yml` in a sample Node or Python app with a Dockerfile:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        env:
          REGISTRY: ghcr.io
          IMAGE: ghcr.io/$GITHUB_REPOSITORY
          TAG: $GITHUB_SHA
        run: |
          docker build -t "$IMAGE:$TAG" -t "$IMAGE:$GITHUB_REF_NAME" .
          if [ "$GITHUB_EVENT_NAME" != "pull_request" ]; then
            echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
            docker push "$IMAGE:$TAG"
            docker push "$IMAGE:$GITHUB_REF_NAME"
          fi
```

!!! note "GitHub Actions secrets"
    `GITHUB_TOKEN` is injected automatically by GitHub Actions runners — no manual secret reference required for ghcr.io pushes with default permissions.

Verify:

1. Push to a feature branch — build runs; push skipped on PR.
2. Merge to `main` — image appears in GitHub Packages (ghcr.io).
3. Confirm tag matches short SHA.

### Lab 2 — GitLab CI with Docker-in-Docker

Add `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - scan

variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

build-image:
  stage: build
  image: docker:27-cli
  services:
    - name: docker:27-dind
      alias: docker
  before_script:
    - until docker info; do sleep 1; done
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
  script:
    - docker build -t "$IMAGE_TAG" -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG" .
    - docker push "$IMAGE_TAG"
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_REF_SLUG"
  rules:
    - if: $CI_COMMIT_BRANCH

scan-image:
  stage: scan
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL "$IMAGE_TAG"
  needs: [build-image]
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

GitLab shared runners enable DinD when the runner executor supports it. Self-hosted runners need `privileged = true` in `config.toml` for the Docker executor.

### Lab 3 — Multi-stage Dockerfile optimised for CI

Ensure your Dockerfile leverages layer caching:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
USER node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

Dependency layers rebuild only when `package-lock.json` changes — critical for CI speed.

### Lab 4 — PR validation without push

Add a job that builds but does not push on pull requests:

```yaml
      - name: Build and smoke test (PR only)
        if: github.event_name == 'pull_request'
        run: |
          docker build -t myapp:pr-test .
          docker run -d --name app -p 8080:3000 myapp:pr-test
          sleep 5
          curl -f http://localhost:8080/health
          docker stop app
```

This catches Dockerfile breakage before merge.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

### Useful local equivalents

```bash
# Simulate CI build with SHA tag
export GIT_SHA=$(git rev-parse --short HEAD)
docker build -t myapp:$GIT_SHA .
docker tag myapp:$GIT_SHA myapp:main

# Inspect image labels set in CI
docker inspect myapp:$GIT_SHA \
  | jq -r '.[0].Config.Labels["org.opencontainers.image.revision"]'

# Verify registry auth
docker login ghcr.io -u USERNAME
docker push ghcr.io/org/myapp:$GIT_SHA
```

### GitLab CI — Kaniko alternative (no DinD)

For environments that disallow privileged DinD:

```yaml
build-kaniko:
  stage: build
  image:
    name: gcr.io/kaniko-project/executor:debug
    entrypoint: [""]
  script:
    - mkdir -p /kaniko/.docker
    - echo "{\"auths\":{\"$CI_REGISTRY\":{\"auth\":\"$(printf "%s:%s" "$CI_REGISTRY_USER" "$CI_REGISTRY_PASSWORD" | base64 | tr -d '\n')\"}}}" > /kaniko/.docker/config.json
    - /kaniko/executor
        --context "$CI_PROJECT_DIR"
        --dockerfile "$CI_PROJECT_DIR/Dockerfile"
        --destination "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
```

### Pipeline environment variables reference

| Variable | Platform | Purpose |
|----------|----------|---------|
| `GITHUB_SHA` | GitHub Actions | Full commit SHA |
| `GITHUB_REF_NAME` | GitHub Actions | Branch or tag name |
| `CI_COMMIT_SHA` | GitLab CI | Full commit SHA |
| `CI_COMMIT_SHORT_SHA` | GitLab CI | Short SHA for tags |
| `CI_REGISTRY_IMAGE` | GitLab CI | Pre-built registry path |

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using latest as the only production tag"
    Deployments become untraceable. Always tag with commit SHA; promote semver tags from CI on Git tag events.

!!! warning "Running DinD without waiting for the daemon"
    Race conditions cause `Cannot connect to the Docker daemon`. Always loop on `docker info` in `before_script`.

!!! warning "Storing registry credentials in the Dockerfile"
    Use CI secrets and `docker login --password-stdin`. Rotate credentials if leaked.

!!! warning "Building on every commit without cache"
    Multi-minute builds add up. Enable GHA cache or GitLab `--cache-from` registry cache.

!!! warning "Socket mounting on untrusted multi-tenant runners"
    Any job with socket access can control the host daemon. Prefer BuildKit action, Kaniko, or isolated DinD.

## Best Practices

!!! tip "Pin base images by digest"
    In Dockerfile: `FROM node:22-alpine@sha256:abc123...` — prevents supply-chain drift between CI runs.

!!! tip "Separate build and deploy pipelines"
    CI builds and pushes; CD (or GitOps) deploys from registry. CI runners should not hold production kubeconfig.

!!! tip "Scan before push to prod registry"
    Run Trivy, Grype, or Snyk on every main-branch build. Fail on CRITICAL CVEs with fix available.

!!! tip "Use OCI labels"
    Set `org.opencontainers.image.revision`, `source`, and `version` in CI for SBOM and audit trails.

!!! tip "OIDC for cloud registries"
    GitHub and GitLab support workload identity to AWS ECR, GCP Artifact Registry, and Azure ACR — no long-lived passwords.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `permission denied` on docker.sock | Runner lacks socket access | Enable Docker on runner; use DinD service |
| DinD TLS handshake error | Cert dir mismatch | Set `DOCKER_TLS_CERTDIR=/certs`; use matching dind version |
| `denied: permission_denied` on push | Wrong token scope | Grant `packages: write`; use PAT with `write:packages` |
| Empty layer cache | Cache backend not configured | Enable `cache-from: type=gha` or registry cache |
| Build works locally, fails in CI | Wrong context or platform | Set `platforms: linux/amd64`; verify `.dockerignore` |
| Image too large | Dev deps in final stage | Multi-stage build; `.dockerignore` node_modules |

## Summary

- **CI/CD pipelines** should build immutable container images tagged with **commit SHA**
- **GitHub Actions** uses `docker/build-push-action` with BuildKit and GHA layer cache
- **GitLab CI** commonly uses **Docker-in-Docker** via `docker:dind` service — wait for daemon, handle TLS
- **DinD** is not the same as **socket binding** — understand security trade-offs on your runners
- Add **scan gates**, **PR build-only** jobs, and **OIDC** registry auth for production-grade pipelines
- Connect this workflow to [Production Docker Patterns](production-docker-patterns.md) for runtime hardening

## Interview Questions

1. What is the difference between Docker socket binding and Docker-in-Docker in CI?
2. Why should production deployments pin images to commit SHA or digest rather than `latest`?
3. How do you cache Docker layers in GitHub Actions?
4. What Git events should trigger image build vs image push?
5. How do you secure registry credentials in CI pipelines?
6. When would you choose Kaniko over DinD?
7. What OCI labels should CI attach to built images?
8. How do you run container smoke tests in a PR pipeline without pushing to the registry?
9. What causes `Cannot connect to the Docker daemon` in GitLab DinD jobs?
10. Describe the flow from `git push` to a running container in production.

??? tip "Sample Answers (Questions 1 and 2)"

    **Q1 — Socket vs DinD:** Socket binding mounts the host's `/var/run/docker.sock` into the CI job container, so `docker` CLI commands control the host daemon — fast but shared and risky on multi-tenant infrastructure. DinD runs a separate `dockerd` inside a privileged sidecar container, giving each job an isolated daemon at the cost of startup time, TLS configuration, and privileged mode requirements.

    **Q2 — SHA vs latest:** `latest` is a mutable pointer — rebuilding overwrites what production runs, breaking rollback and audit trails. Commit SHA tags are immutable and map directly to source code, enabling traceability from running container to Git author, PR, and CI logs.

## Related Tutorials

- [Container Registries and Distribution](container-registries-and-distribution.md) *(previous module)*
- [Production Docker Patterns](production-docker-patterns.md) *(next)*
- [Docker Security Hardening](docker-security-hardening.md)
- [Git in CI/CD and DevOps](../git/git-in-ci-cd-and-devops.md)
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Docker – Category Overview](index.md)
- Cheat sheet: [Docker Cheat Sheet](../cheatsheets/docker.md)
- Interview prep: [Docker Interview Prep](../interview/docker.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [GitHub Actions – Publishing Docker images](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
- [docker/build-push-action](https://github.com/docker/build-push-action)
- [GitLab CI – Use Docker to build Docker images](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html)
- [Docker BuildKit](https://docs.docker.com/build/buildkit/)
- [Kaniko Documentation](https://github.com/GoogleContainerTools/kaniko)
- [OCI Image Spec – Annotations](https://github.com/opencontainers/image-spec/blob/main/annotations.md)
- [Trivy – Container scanning](https://aquasecurity.github.io/trivy/)
