---
title: Container Registries and Distribution
description: Push and pull images from Docker Hub, Amazon ECR, and Google Artifact Registry with production tagging, authentication, and CI/CD distribution patterns.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: docker
tags:
  - docker
  - registry
  - docker-hub
  - ecr
  - gcr
  - image-tagging
  - distribution
prerequisites:
  - Completion of Module 2 Docker tutorials (images and Dockerfile)
  - Familiarity with Docker networking and basic CLI workflows
  - Cloud account optional for ECR and GCR labs (Docker Hub works without cloud)
comments: false
---

# Container Registries and Distribution

## Overview

Building a container image on your laptop is only half the delivery story. Production systems pull images from a **container registry** — a remote store that versions, authenticates, and distributes OCI-compliant artifacts to hosts, CI runners, and orchestrators. Without a registry, every server would need a local build environment, reproducibility would collapse, and rollbacks would be impossible at scale.

This tutorial covers how registries work, how to authenticate and push to **Docker Hub**, **Amazon Elastic Container Registry (ECR)**, and **Google Artifact Registry** (the modern replacement for Container Registry), and how to design **tagging strategies** that tie images to Git commits, environments, and release channels. You will practice tagging, pushing, pulling, inspecting manifests, and applying immutability patterns used in real pipelines.

This is **Tutorial 11** in **Module 4: Networking & Registry** of the REBASH Academy Docker series. Complete [Docker Networking Fundamentals](docker-networking-fundamentals.md) first, then continue to [Environment Variables and Secrets](environment-variables-and-secrets.md).

## Prerequisites

- Docker Engine installed and running — see [Docker Installation and Setup](docker-installation-and-setup.md)
- Ability to build a simple image — see [Building Images with Dockerfile](building-images-with-dockerfile.md)
- A Docker Hub account (free tier is sufficient for labs)
- Optional: AWS CLI and GCP `gcloud` CLI for cloud registry sections
- Basic understanding of [Git tagging](../git/introduction-to-git-and-version-control.md) concepts

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the role of container registries in build-once, deploy-many workflows
- [ ] Authenticate to Docker Hub, Amazon ECR, and Google Artifact Registry
- [ ] Tag images with semantic, Git SHA, and environment-specific conventions
- [ ] Push, pull, and inspect image manifests and digests
- [ ] Apply immutability and retention policies for production image promotion
- [ ] Describe how CI/CD pipelines integrate with private registries

## Architecture

Registries sit between image builders and runtime consumers. The same image digest can be pulled by development laptops, CI agents, ECS tasks, GKE nodes, and Kubernetes clusters worldwide.

```d2
direction: right

DEV: "Developer / CI Builder"
    BUILD: "docker build"
    REG: "Container Registry\nHub / ECR / Artifact Registry"
    RUN1: "Docker Host"
    RUN2: "Kubernetes Node"
    RUN3: "Cloud Run / ECS"
    DEV -> BUILD
    BUILD -> REG: "docker push"
    REG -> RUN1: "docker pull"
    REG -> RUN2: "kubelet pull"
    REG -> RUN3: "service pull"
```

## Theory

### What Is a Container Registry?

A **container registry** stores **images** — layered filesystem snapshots with metadata (architecture, OS, labels, config). Registries implement the **OCI Distribution Specification**, so Docker, containerd, Podman, and Kubernetes use the same push/pull protocol over HTTPS.

Key concepts:

| Term | Meaning |
|------|---------|
| **Repository** | Named collection of related images (e.g., `myorg/api`) |
| **Tag** | Human-readable label pointing to a manifest (e.g., `v1.4.2`, `main-abc1234`) |
| **Digest** | Immutable SHA256 hash of the manifest (e.g., `sha256:abc123...`) |
| **Manifest** | JSON describing layers, config blob, and platform |
| **Namespace** | Organisation or project scope (`library/nginx`, `123456789012.dkr.ecr...`) |

**Tags are mutable** — pushing `myapp:latest` again overwrites what `latest` points to. **Digests are immutable** — production deployments should pin digests or tags that are never reused.

### Docker Hub

**Docker Hub** is the default public registry. When you run `docker pull nginx`, Docker resolves `docker.io/library/nginx`. Hub provides:

- Public repositories (unlimited pulls with rate limits for anonymous users)
- Private repositories (limited on free accounts; paid plans for teams)
- Automated builds (legacy; most teams use CI instead)
- Organisation namespaces for team ownership

Authentication uses `docker login docker.io` with a username and personal access token (PAT). Passwords are deprecated for CLI login; use Hub access tokens with appropriate scopes.

### Amazon Elastic Container Registry (ECR)

**ECR** is AWS's managed OCI registry. Each repository lives in a region under your AWS account ID. Image URIs look like:

```text
123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app:v1.0.0
```

ECR features relevant to production:

- **IAM integration** — fine-grained push/pull policies via IAM roles and policies
- **Image scanning** — vulnerability scanning on push (Basic scanning or Inspector integration)
- **Lifecycle policies** — automatically expire untagged or old images to control storage cost
- **Replication** — cross-region and cross-account replication for DR and multi-region deploys
- **Private by default** — no public exposure unless you enable ECR Public

Authentication uses short-lived tokens from `aws ecr get-login-password`, piped to `docker login`. CI/CD on AWS typically uses IAM roles (OIDC or instance profiles) instead of long-lived keys.

### Google Artifact Registry

Google's **Artifact Registry** (AR) replaced **Container Registry (GCR)** for new projects. Images are stored in regional repositories with URIs like:

```text
us-docker.pkg.dev/my-project/my-repo/my-app:v1.0.0
```

Artifact Registry supports Docker images, Helm charts, Maven artifacts, and more in unified repositories. Authentication uses:

- `gcloud auth configure-docker REGION-docker.pkg.dev` for developer workstations
- Workload Identity Federation or service account keys in CI (prefer federation)
- IAM roles: `roles/artifactregistry.reader`, `roles/artifactregistry.writer`

GKE pulls images from Artifact Registry when nodes have the appropriate service account permissions.

### Tagging Strategies for Production

Poor tagging causes "works on my machine" deploys and impossible rollbacks. Mature teams combine several tag types:

| Tag pattern | Example | Use case |
|-------------|---------|----------|
| **Semantic version** | `v2.1.0` | Release promotion, changelog alignment |
| **Git commit SHA** | `sha-a1b2c3d4` or `main-a1b2c3d4` | Immutable traceability to source |
| **Branch name** | `feature-login-fix` | Ephemeral CI builds (auto-prune) |
| **Environment** | `staging`, `prod` | Mutable pointers — use with caution |
| **Build number** | `build-1842` | CI pipeline sequence |
| **latest** | `latest` | Dev convenience only — never sole prod tag |

**Recommended production pattern:**

1. CI builds image tagged with Git SHA (immutable)
2. After tests pass, additionally tag `v1.4.2` and push
3. Deployment manifest pins digest or SHA tag
4. `latest` updated only for developer convenience on default branch

### Image Promotion and Immutability

**Promotion** moves a tested artifact through environments without rebuilding:

```text
build → push sha-abc123 → test → tag v1.4.2 → deploy staging → deploy prod
```

Because the digest is unchanged, staging and production run identical bits. Rebuilding per environment introduces drift.

Enable **tag immutability** where supported (ECR, Artifact Registry, Harbor) to prevent accidental overwrites of release tags.

### Registry Security Essentials

- Use **private registries** for proprietary code; scan public base images
- Prefer **short-lived credentials** (ECR tokens expire in 12 hours)
- Grant **least privilege** — CI push role should not have delete on production repos
- Enable **vulnerability scanning** and block deploy on critical CVEs (policy in CI)
- Audit **pull/push logs** via CloudTrail (ECR) or Cloud Logging (GCP)

## Hands-on Lab

These labs use a minimal nginx-based image. Adjust usernames and project IDs to match your accounts.

### Step 1 – Build a lab image locally

**Command:**

```bash
mkdir -p /tmp/registry-lab && cd /tmp/registry-lab
printf 'FROM nginx:1.27-alpine\nLABEL maintainer="lab@example.com"\n' > Dockerfile
docker build -t registry-lab-web:local .
docker images registry-lab-web:local
```

**Explanation:** A tiny image keeps push/pull labs fast. The `local` tag stays on your machine until you retag for a registry.

**Expected output:**

```text
Successfully tagged registry-lab-web:local
REPOSITORY         TAG     IMAGE ID       CREATED         SIZE
registry-lab-web   local   ...            ...             ...
```

### Step 2 – Tag for Docker Hub

Replace `YOUR_DOCKERHUB_USER` with your Hub username.

**Command:**

```bash
export DOCKERHUB_USER="YOUR_DOCKERHUB_USER"
docker tag registry-lab-web:local "${DOCKERHUB_USER}/registry-lab-web:lab-v1"
docker tag registry-lab-web:local "${DOCKERHUB_USER}/registry-lab-web:sha-demo001"
docker images | grep registry-lab-web
```

**Explanation:** One image ID can have many tags. Tags are aliases; they do not duplicate layer storage locally.

### Step 3 – Authenticate and push to Docker Hub

Create a Hub access token under Account Settings → Security → New Access Token.

**Command:**

```bash
docker login docker.io
docker push "${DOCKERHUB_USER}/registry-lab-web:lab-v1"
docker push "${DOCKERHUB_USER}/registry-lab-web:sha-demo001"
```

**Explanation:** `docker login` stores credentials in `~/.docker/config.json` (base64-encoded, not encrypted — protect this file). Push uploads missing layers; subsequent pushes of the same layers are fast.

**Expected output:**

```text
Login Succeeded
...
lab-v1: digest: sha256:... size: ...
sha-demo001: digest: sha256:... size: ...
```

### Step 4 – Inspect manifest and digest

**Command:**

```bash
docker inspect "${DOCKERHUB_USER}/registry-lab-web:lab-v1" | grep -m1 '"Id"'
docker manifest inspect "docker.io/${DOCKERHUB_USER}/registry-lab-web:lab-v1" 2>/dev/null || \
  docker buildx imagetools inspect "docker.io/${DOCKERHUB_USER}/registry-lab-web:lab-v1"
```

**Explanation:** Production deploys often reference digest instead of tag. `buildx imagetools` queries the remote registry without a local pull.

### Step 5 – Pull on a clean host (simulate deployment)

**Command:**

```bash
docker rmi "${DOCKERHUB_USER}/registry-lab-web:lab-v1" 2>/dev/null || true
docker pull "${DOCKERHUB_USER}/registry-lab-web:lab-v1"
docker run -d --name reg-lab-test -p 8080:80 "${DOCKERHUB_USER}/registry-lab-web:lab-v1"
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8080/
docker stop reg-lab-test && docker rm reg-lab-test
```

**Explanation:** Simulates what a production host does: pull by tag, run container, verify HTTP response.

**Expected output:**

```text
200
```

### Step 6 – Amazon ECR push workflow (AWS)

Requires AWS CLI configured with permissions for ECR. Replace region and repository name.

**Command:**

```bash
export AWS_REGION="us-east-1"
export ECR_REPO="registry-lab-web"
aws ecr describe-repositories --repository-names "${ECR_REPO}" 2>/dev/null || \
  aws ecr create-repository --repository-name "${ECR_REPO}" --image-scanning-configuration scanOnPush=true
export ECR_URI=$(aws ecr describe-repositories --repository-names "${ECR_REPO}" \
  --query 'repositories[0].repositoryUri' --output text)
aws ecr get-login-password --region "${AWS_REGION}" | \
  docker login --username AWS --password-stdin "${ECR_URI%%/*}"
docker tag registry-lab-web:local "${ECR_URI}:v1-lab"
docker push "${ECR_URI}:v1-lab"
```

**Explanation:** ECR login tokens expire after 12 hours. CI pipelines refresh tokens on each job. `scanOnPush` enables vulnerability scanning.

### Step 7 – Google Artifact Registry push workflow (GCP)

Replace project, region, and repository names. Enable Artifact Registry API first.

**Command:**

```bash
export GCP_PROJECT="my-gcp-project"
export GCP_REGION="us-central1"
export AR_REPO="docker-lab"
gcloud artifacts repositories describe "${AR_REPO}" \
  --location="${GCP_REGION}" --project="${GCP_PROJECT}" 2>/dev/null || \
  gcloud artifacts repositories create "${AR_REPO}" \
    --repository-format=docker --location="${GCP_REGION}" --project="${GCP_PROJECT}"
gcloud auth configure-docker "${GCP_REGION}-docker.pkg.dev" --quiet
export AR_URI="${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REPO}/registry-lab-web"
docker tag registry-lab-web:local "${AR_URI}:v1-lab"
docker push "${AR_URI}:v1-lab"
```

**Explanation:** Artifact Registry is regional. GKE clusters in the same region pull with lower latency and no cross-region egress charges.

### Step 8 – Clean up lab resources

**Command:**

```bash
cd /tmp && rm -rf registry-lab
docker rmi registry-lab-web:local 2>/dev/null || true
```

**Explanation:** Remove local tags after labs. Delete remote test repositories in Hub/ECR/AR consoles if no longer needed.

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

| Command | Description | Example |
|---------|-------------|---------|
| `docker tag` | Add registry-compatible tag to local image | `docker tag myapp:local reg.io/org/myapp:v1` |
| `docker login` | Authenticate to registry | `docker login docker.io` |
| `docker push` | Upload image layers and manifest | `docker push reg.io/org/myapp:v1` |
| `docker pull` | Download image from registry | `docker pull reg.io/org/myapp:v1` |
| `docker logout` | Remove stored credentials | `docker logout docker.io` |
| `aws ecr get-login-password` | ECR auth token | Pipe to `docker login` |
| `gcloud auth configure-docker` | Configure Docker for Artifact Registry | Region-specific hostname |
| `docker buildx imagetools inspect` | Remote manifest inspection | Shows digest and platforms |

### CI tagging script pattern

Save as `scripts/tag-and-push.sh` in your pipeline repo. Uses environment variables set by CI — no secrets in the script itself.

```bash
#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${CI_REGISTRY_IMAGE:-myregistry.example.com/myapp}"
GIT_SHA="${CI_COMMIT_SHORT_SHA:-dev}"
VERSION="${CI_COMMIT_TAG:-}"

docker build -t "${IMAGE_NAME}:sha-${GIT_SHA}" .

docker push "${IMAGE_NAME}:sha-${GIT_SHA}"

if [ -n "${VERSION}" ]; then
  docker tag "${IMAGE_NAME}:sha-${GIT_SHA}" "${IMAGE_NAME}:${VERSION}"
  docker push "${IMAGE_NAME}:${VERSION}"
fi
```

Make executable: `chmod +x scripts/tag-and-push.sh`

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using only :latest in production"
    `latest` is a moving target. A redeploy without pinning may pull a different image than the one you tested. Always pin SHA tags or digests in production manifests.

!!! warning "Reusing release tags for different builds"
    Pushing `v1.0.0` twice with different content breaks traceability. Enable tag immutability or use unique tags per build.

!!! warning "Embedding registry credentials in images or Dockerfiles"
    Never `docker login` inside a Dockerfile or bake tokens into layers. Use CI secrets, IAM roles, or credential helpers at runtime on the build host.

!!! warning "Ignoring registry rate limits"
    Docker Hub limits anonymous and free-tier pulls. Production clusters should authenticate or mirror images to a private registry.

## Best Practices

!!! tip "Pin images by digest in production"
    Kubernetes, ECS task definitions, and Compose production files should reference `image@sha256:...` or immutable SHA tags tied to CI output.

!!! tip "Separate registries or repos per environment"
    Use distinct repositories or namespaces for `dev`, `staging`, and `prod` — or promote by retagging the same digest without rebuild.

!!! tip "Automate lifecycle cleanup"
    Untagged manifests and ancient feature-branch tags consume storage. Configure ECR lifecycle rules and Artifact Registry cleanup policies.

!!! tip "Mirror critical base images"
    Pull public bases (`nginx`, `python`, `node`) through your private registry to avoid Hub outages and rate limits affecting deploys.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `denied: requested access to the resource is denied` | Not logged in or wrong namespace | `docker login`; verify tag includes your username/org |
| `unauthorized: authentication required` | Expired ECR/GCP token | Re-run `aws ecr get-login-password` or `gcloud auth configure-docker` |
| `name unknown: repository name not known to registry` | Repo does not exist | Create repo in console/CLI before push |
| Push succeeds but pull fails on another host | Wrong architecture tag | Build multi-platform with `docker buildx` or match node arch |
| `toomanyrequests` from Docker Hub | Rate limit exceeded | Authenticate; upgrade plan; use registry mirror |
| Digest mismatch after retag | Expected — tags point to same manifest | Use `docker inspect` to compare image IDs |

## Summary

- Container **registries** distribute OCI images to every runtime environment using push/pull over HTTPS
- **Docker Hub** is the default public registry; **ECR** and **Artifact Registry** are managed private options on AWS and GCP
- **Tags** are human-readable and mutable; **digests** are immutable and preferred for production pinning
- Production tagging combines **semantic versions**, **Git SHAs**, and careful use of environment pointers
- CI/CD should **build once**, push with traceable tags, and **promote** the same digest across environments

## Interview Questions

1. What is the difference between an image tag and a digest?
2. Why should production deployments avoid relying solely on `:latest`?
3. How does authentication work for Amazon ECR?
4. What replaced Google Container Registry, and how do image URIs differ?
5. Describe an image promotion workflow from CI to production.
6. What is an OCI-compliant registry, and why does it matter?
7. How would you trace a running container back to the exact source code commit?
8. What are ECR lifecycle policies used for?
9. Explain the security risk of storing `docker login` credentials on shared build agents.
10. How do registry rate limits affect Kubernetes clusters pulling from Docker Hub?

??? tip "Sample Answers (Questions 1, 5, and 7)"

    **Q1 — Tag vs digest:** A tag is a mutable string label (e.g., `v1.4.2`) that points to an image manifest. A digest is the SHA256 hash of that manifest (e.g., `sha256:abc...`) and cannot change without changing the image content. Two tags can reference the same digest; changing a tag's target does not change the digest of the underlying image.

    **Q5 — Promotion workflow:** CI builds the image once and pushes with an immutable tag such as `sha-a1b2c3d4`. Automated tests run against that artifact. After approval, the same manifest receives additional tags (`v1.4.2`, `staging`) via retag-and-push or registry API — no rebuild. Production deployment references the digest or SHA tag, ensuring staging and prod run identical layers.

    **Q7 — Traceability:** The image should be tagged with the Git commit SHA at build time (label `org.opencontainers.image.revision` or tag `sha-a1b2c3d4`). Query the running container's image with `docker inspect` or the orchestrator API, read the digest, and match it to CI build logs and the Git commit that triggered the pipeline.

## Related Tutorials

- [Docker – Category Overview](index.md)
- [Working with Docker Images](working-with-docker-images.md)
- [Building Images with Dockerfile](building-images-with-dockerfile.md)
- [Docker Networking Fundamentals](docker-networking-fundamentals.md) *(previous in Module 4)*
- [Environment Variables and Secrets](environment-variables-and-secrets.md) *(next in Module 4)*
- [Docker in CI/CD Pipelines](docker-in-ci-cd-pipelines.md)

## References

- [Docker Hub documentation](https://docs.docker.com/docker-hub/)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Google Artifact Registry overview](https://cloud.google.com/artifact-registry/docs/overview)
- [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec)
- [Docker buildx imagetools](https://docs.docker.com/reference/cli/docker/buildx/imagetools/)
- [REBASH Academy – Git Overview](../git/index.md)
