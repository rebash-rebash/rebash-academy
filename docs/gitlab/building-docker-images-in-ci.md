---
title: "Building Docker Images in CI"
description: "Build multi-stage images with BuildKit in GitLab CI, push to GitLab Container Registry, and promote by digest or immutable tag."
difficulty: intermediate
estimated_time: "45–60 min"
technology: gitlab
category: gitlab
module: "Module 8 · Docker Pipelines"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - docker
  - container-registry
prerequisites:
  - gitlab/artifacts-caches-and-dependencies
next:
  - gitlab/kubernetes-deploys-and-gitlab-agent
related:
  - docker/introduction-to-containers-and-docker
  - gitlab/security-scanning-and-devsecops
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
tags:
  - gitlab
  - docker
  - buildkit
  - registry
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Building Docker Images in CI

## Overview



Author a GitLab CI job that builds a multi-stage Dockerfile (BuildKit-friendly), tags the image with the commit SHA, and documents promotion from registry to later environments without rebuilding.

CI builds containers so every merge produces a **reproducible image**. GitLab provides a **Container Registry** per project (`$CI_REGISTRY_IMAGE`). Prefer **BuildKit** (or Kaniko/buildah on locked-down runners) over ad-hoc Docker-in-Docker. Tag with `$CI_COMMIT_SHA` (and optionally a digest); promote that same image through staging and production.

This is a core tutorial in **Module 8 · Docker Pipelines** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [Artifacts, Caches, and Dependencies](artifacts-caches-and-dependencies.md)



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] Sketch a Docker / BuildKit CI job using `$CI_REGISTRY_*`  
- [ ] Write a minimal multi-stage Dockerfile  
- [ ] Explain SHA tags vs floating `latest`  
- [ ] Describe image promotion without rebuild  
- [ ] Note DinD vs rootless / Kaniko trade-offs



## Architecture



This topic’s control points and relationships are shown below.

![GitLab Docker pipeline](../assets/excalidraw/gitlab-docker-pipeline.svg)



## Theory



### What it is

A **Docker pipeline** compiles application code into an OCI image inside a GitLab job, then pushes it to a registry. Common builders:

| Builder | Typical setup | Notes |
|---------|---------------|-------|
| Docker + BuildKit | `docker:cli` + `docker:dind` service | Familiar; needs privileged or socket carefully |
| Kaniko / buildah | No daemon | Better for restricted Kubernetes runners |
| GitLab Container Registry | `$CI_REGISTRY` + job token | Default home for project images |

**Multi-stage** Dockerfiles keep build tools out of the final runtime image. **Promotion** means retagging or deploying the same digest — never “rebuild on main with different base layers” for production.

### Why it matters

Laptop-built images drift from CI and skip scanners. Registry-hosted, SHA-tagged images are the unit of deploy for Kubernetes and cloud services. Layer caching and BuildKit cut minutes; digest pins stop surprise base-image moves. Without promotion discipline, staging and production silently diverge.

### How it works

1. Job authenticates to `$CI_REGISTRY` with `$CI_REGISTRY_USER` / `$CI_REGISTRY_PASSWORD` (or job token).  
2. BuildKit builds the Dockerfile (`DOCKER_BUILDKIT=1` or `docker buildx`).  
3. Tag `$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA` (and maybe a branch tag for non-prod).  
4. Push; optionally record digest as an artefact or release note.  
5. Deploy jobs pull that SHA/digest; production never rebuilds from source for the same commit.

Cache mounts and registry pull-through caches accelerate rebuilds; they do not replace pinning base images by digest in production Dockerfiles.

### Key concepts and comparisons

| Practice | Prefer | Avoid |
|----------|--------|-------|
| Tags | Commit SHA / semver / digest | Only `latest` |
| Stages | Multi-stage slim runtime | Single fat image with compilers |
| Auth | CI job token / short-lived | Long-lived personal tokens in Git |
| Promote | Same digest across envs | Rebuild per environment |

### Common pitfalls

- Privileged DinD on shared runners without isolation.  
- Pushing `latest` from every MR.  
- Baking secrets into image layers (`ENV` with API keys).  
- Assuming cache guarantees bit-identical images across builders.  
- Rebuilding for production instead of promoting the tested digest.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-08 && cd ~/rebash-gitlab/module-08
```

**Focus:** build a Dockerfile and a GitLab job that would build the image

### Step 1 – Dockerfile + CI job

```bash
cat > Dockerfile << 'EOF'
FROM alpine:3.20
WORKDIR /app
COPY hello.txt .
CMD ["cat", "hello.txt"]
EOF
echo 'hello from gitlab ci' > hello.txt
docker build -t rebash-gitlab-lab:local .
docker run --rm rebash-gitlab-lab:local
cat > .gitlab-ci.yml << 'EOF'
build-image:
  image: docker:27
  services: [docker:27-dind]
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
EOF
echo 'CI job documented; local image build verified.'
```

### Final step – Cleanup note

```bash
docker rmi rebash-gitlab-lab:local 2>/dev/null || true
```



## Validation



- [ ] Lab commands run under `~/rebash-gitlab/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **Building Docker Images in CI** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.



## Security Considerations



- Treat credentials and tokens for gitlab as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces



## Common Mistakes



!!! warning "Privileged DinD on shared runners without isolation.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Pushing `latest` from every MR.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode Building Docker Images in CI changes as code and review them in pull requests
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



**Building Docker Images in CI** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. How does **Building Docker Images in CI** show up in a real GitLab delivery workflow?
2. A pipeline is stuck / red — what do you check first?
3. How do `needs`, stages, and artefacts interact?
4. How should secrets and cloud credentials be handled in GitLab CI?
5. How would you keep merge-request pipelines fast but still safe?

!!! tip "Sample answer — question 2"
    Open the failing job log, confirm runner tags/executor, then validate `.gitlab-ci.yml` with CI Lint. Check rules that skipped jobs and artefact dependencies.

!!! tip "Sample answer — question 4"
    Prefer masked/protected variables and OIDC (`id_tokens`) over long-lived keys. Limit who can run protected-branch pipelines.



## Related Tutorials



- [Course overview](index.md)
- [Kubernetes Deploys and GitLab Agent](kubernetes-deploys-and-gitlab-agent.md)



## References



- [Build Docker images with GitLab CI](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html) · [GitLab Container Registry](https://docs.gitlab.com/ee/user/packages/container_registry/) · [BuildKit](https://docs.docker.com/build/buildkit/)
