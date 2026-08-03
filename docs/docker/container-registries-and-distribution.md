---
title: "Container Registries and Distribution"
description: "Push and pull images via Docker Hub, GHCR, ECR, ACR, and Artifact Registry — private registry patterns for DevOps."
difficulty: intermediate
estimated_time: "40–55 min"
technology: docker
category: docker
module: "Module 10 · Registries"
career_paths:
  - devops-engineer
  - platform-engineer
  - cloud-engineer
skills:
  - docker
  - container-registry
prerequisites:
  - docker/docker-compose-fundamentals
  - docker/working-with-docker-images
next:
  - docker/docker-security-hardening
related:
  - docker/docker-in-ci-cd-pipelines
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - registry
  - ghcr
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---


# Container Registries and Distribution

## Overview







Tag and push an image to a registry workflow you can repeat in CI — understand Hub vs cloud registries (GHCR, ECR, ACR, GAR).

Registries store and distribute images. Production uses private registries, immutable tags, and retention policies.

This is a core tutorial in **Module 10 · Registries** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Docker Compose Fundamentals](docker-compose-fundamentals.md)
- [Working with Docker Images](working-with-docker-images.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Tag for `registry/org/image:tag`  
- [ ] Login and push (or dry-run the commands)  
- [ ] Compare Hub, GHCR, ECR, ACR, GAR  
- [ ] Prefer digest pins for deploys

## Architecture







This topic’s control points and relationships are shown below.

![Registry workflow](../assets/excalidraw/docker-registry-workflow.svg)

## Theory







### What

A **container registry** stores and serves OCI images. Public defaults include Docker Hub; cloud options include GitHub Container Registry (GHCR), Amazon Elastic Container Registry (ECR), Azure Container Registry (ACR), and Google Artifact Registry. Enterprises also run Harbor or distribution. Clients authenticate, then `pull`/`push` by tag or digest.

### Why

Images must leave the build machine to reach CI promotion paths and clusters. Rate limits, access control, and vulnerability scanning at the registry gate are production concerns. Choosing a registry near your cloud reduces pull latency and aligns Identity and Access Management (IAM).

### How it works

`docker login` (or cloud CLI helpers) stores credentials via a helper. CI should prefer short-lived **OIDC** tokens over long-lived passwords. Tag images with registry prefixes (`ghcr.io/org/app:1.2.0`) and push. Promotion often retags digests across repositories or environments without rebuilding. Enable vulnerability scanning and immutable tags where the product supports them.

| Registry | Notes |
|----------|-------|
| Docker Hub | Public default; rate limits |
| GHCR | Tight GitHub Actions integration |
| Amazon ECR | IAM / OIDC from AWS |
| Azure ACR | Entra ID / tokens |
| Google Artifact Registry | GCP IAM |
| Self-hosted | Harbor, distribution |

### Key concepts

- **Namespace and permissions** — who can push/pull  
- **Immutable tags / digests** — promotion safety  
- **Rate limits** — authenticate pulls even for public images when needed  
- **Replication** — multi-region pull performance  


Document who owns each registry namespace and how break-glass credentials are rotated. Prefer pull-through caches or mirrored bases in constrained networks so builds do not depend on public rate limits during an incident. Record the digest in release notes or GitOps manifests so auditors can answer “what ran?” without guesswork.

### Common pitfalls

- Building once per environment instead of promoting a digest  
- Storing registry passwords in plaintext CI variables forever  
- Pushing untagged or `:latest`-only images  
- Forgetting cleanup policies until storage bills spike

## Hands-on Lab

### Objective

Build a tiny release image, record its immutable `Id`, export it with `docker save`, reload it offline, and prove the reloaded image matches the original digest metadata.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to build and run containers locally
- ~500 MB free disk for layers and the export tarball

### Lab environment

Workspace: `~/rebash-docker/module-10`

Local Docker daemon only — no cloud registry login required.

```bash title="Terminal"
mkdir -p ~/rebash-docker/module-10 && cd ~/rebash-docker/module-10
```

### Real-world scenario

Your platform team mirrors release images to an air-gapped cluster. Before promoting a build, you must capture immutable identity, export a tarball for offline transfer, and verify the reloaded image matches the original `Id`.

### Step-by-step tasks

#### Task 1 – Build and tag a release image

Create `Dockerfile`:

```dockerfile title="Dockerfile"
FROM alpine:3.20
RUN echo "rebash-registry-lab v1" > /version.txt
CMD ["cat", "/version.txt"]
```

Build with a semver tag and a local alias:

{% raw %}
```bash title="Terminal"
cd ~/rebash-docker/module-10
docker build -t rebash-registry-lab:1.0.0 -t rebash-registry-lab:local .
docker images rebash-registry-lab --format '{{ "{{" }}.Repository{{ "}}" }}:{{ "{{" }}.Tag{{ "}}" }} {{ "{{" }}.ID{{ "}}" }}' | tee image-tags.txt
grep -q 'rebash-registry-lab:1.0.0' image-tags.txt
```
{% endraw %}

!!! example "Expected output"
    `image-tags.txt` lists both tags pointing at the same image ID.


#### Task 2 – Record digest metadata and export offline bundle

Capture `Id` and `RepoDigests` (often empty until a registry push) and save a tarball:

{% raw %}
```bash title="Terminal"
cd ~/rebash-docker/module-10
docker inspect rebash-registry-lab:1.0.0 --format 'Id={{ "{{" }}.Id{{ "}}" }} RepoDigests={{ "{{" }}.RepoDigests{{ "}}" }}' | tee digest-id.txt
docker save rebash-registry-lab:1.0.0 -o rebash-registry-lab-1.0.0.tar
test -s rebash-registry-lab-1.0.0.tar
ls -lh rebash-registry-lab-1.0.0.tar | tee tar-size.txt
```
{% endraw %}

!!! example "Expected output"
    `digest-id.txt` contains `Id=sha256:…`; the tarball is non-empty.


#### Task 3 – Load tarball and prove identity

Remove local tags, reload from the tarball, and confirm the same `Id`:

{% raw %}
```bash title="Terminal"
cd ~/rebash-docker/module-10
ORIG_ID="$(grep -o 'Id=sha256:[a-f0-9]*' digest-id.txt | cut -d= -f2)"
docker rmi rebash-registry-lab:1.0.0 rebash-registry-lab:local 2>/dev/null || true
docker load -i rebash-registry-lab-1.0.0.tar | tee load.txt
LOADED_ID="$(docker images --format '{{ "{{" }}.ID{{ "}}" }}' --filter reference='*rebash-registry-lab*' | head -1)"
docker tag "$LOADED_ID" rebash-registry-lab:offline
NEW_ID="$(docker inspect rebash-registry-lab:offline --format '{{ "{{" }}.Id{{ "}}" }}')"
test "$ORIG_ID" = "$NEW_ID"
echo "$NEW_ID" | tee reloaded-id.txt
docker run --rm rebash-registry-lab:offline | tee run-offline.txt
```
{% endraw %}

!!! example "Expected output"
    `reloaded-id.txt` matches the original `Id`; `run-offline.txt` prints `rebash-registry-lab v1`.


### Validation steps

- [ ] Image builds with pinned `alpine:3.20` base
- [ ] `digest-id.txt` records image `Id`
- [ ] `docker save` / `docker load` round-trip succeeds
- [ ] Reloaded image `Id` matches the pre-export value
- [ ] Cleanup removes tags, tarball, and evidence files

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `denied: requested access to the resource is denied` | Push without login | Lab uses offline save/load only — skip push or run `docker login` first |
| Empty `RepoDigests` | Image never pushed to a registry | Expected locally; rely on `Id` for immutability proof |
| `no space left on device` on save | Small disk | Remove unused images: `docker image prune -f` |
| Tag lost after load | Load restores untagged layers | Re-tag as shown in Task 3 |

### Challenge exercise

Run `registry:2.8` as `rebash-local-registry` on host port `50100`, push `rebash-registry-lab:1.0.0` to `localhost:50100/rebash/lab:1.0.0`, pull by digest, and capture `RepoDigests` in `push-digest.txt`.

### Learning outcomes

- Tagged a release image and recorded immutable identity
- Exported and imported images for offline distribution
- Verified reload preserves image `Id`
- Understood when `RepoDigests` appears versus local-only builds

### Cleanup

```bash title="Terminal"
cd ~/rebash-docker/module-10
docker rm -f rebash-local-registry 2>/dev/null || true
docker rmi rebash-registry-lab:1.0.0 rebash-registry-lab:local rebash-registry-lab:offline 2>/dev/null || true
docker rmi localhost:50100/rebash/lab:1.0.0 2>/dev/null || true
rm -f rebash-registry-lab-1.0.0.tar *.txt
```

## Validation







- [ ] Lab commands run under `~/rebash-docker/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Container Registries and Distribution** always combines:

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







!!! warning "Building once per environment instead of promoting a digest  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Storing registry passwords in plaintext CI variables forever  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Container Registries and Distribution changes as code and review them in pull requests
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







**Container Registries and Distribution** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. What is a content digest?
2. How do you authenticate to a private registry in CI?
3. Tag mutation risks?
4. Promotion patterns between registries?
5. How do mirrors/caches help enterprises?

!!! tip "Sample answer — question 2"
    Verify digests and repository permissions. Auth errors dominate first-push failures.

!!! tip "Sample answer — question 4"
    Use short-lived CI credentials/OIDC and immutable tags/digests for prod.

## Related Tutorials







- [Course overview](index.md)
- [Docker Security Hardening](docker-security-hardening.md)

## References







- [GHCR](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) · [ECR](https://docs.aws.amazon.com/ecr/)
