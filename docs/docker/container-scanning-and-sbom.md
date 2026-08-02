---
title: "Container Scanning and SBOM"
description: "Scan images with Trivy and Docker Scout, generate SBOMs, triage CVEs, and harden images in a DevOps pipeline gate."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 12 · Container Scanning"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - docker
  - trivy
  - sbom
prerequisites:
  - docker/docker-security-hardening
next:
  - docker/container-logging-and-monitoring
related:
  - docker/docker-in-ci-cd-pipelines
  - security/index
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - trivy
  - sbom
  - cve
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Container Scanning and SBOM

## Overview







Scan an image for CVEs, produce a Software Bill of Materials (SBOM), and decide fix vs accept risk for a release gate.

**Trivy**, **Docker Scout**, and registry scanners find known vulnerabilities. An **SBOM** inventories packages for compliance and incident response. Scanning without a triage process becomes noise.

This is a core tutorial in **Module 12 · Container Scanning** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites







- [Docker Security Hardening](docker-security-hardening.md)

## Learning Objectives







By the end of this tutorial, you will be able to:

- [ ] Run Trivy (or Scout) against a local image  
- [ ] Explain CRITICAL/HIGH triage  
- [ ] Generate an SBOM (Syft/Trivy)  
- [ ] List hardening moves that reduce findings

## Architecture







This topic’s control points and relationships are shown below.

![CI/CD pipeline with scan](../assets/excalidraw/docker-cicd-pipeline.svg)

## Theory







### What

**Vulnerability scanning** analyses image contents for known Common Vulnerabilities and Exposures (CVEs). A **Software Bill of Materials (SBOM)** lists packages and dependencies you shipped. Tools such as Trivy, Docker Scout, Syft, and Grype integrate into CI to gate or inform releases.

### Why

You cannot patch what you cannot see. Base OS packages and language libraries both introduce risk. SBOMs support incident response (“are we affected?”) and emerging compliance expectations. Failing CI on CRITICAL findings for production images is a common policy.

### How it works

Scanners index installed packages and match them to vulnerability databases. Results include severity, fixed versions, and sometimes misconfiguration checks (Dockerfile smells). Generate an SBOM at build time and store it with the artefact. Fix order is usually: upgrade base image → upgrade application dependencies → rebuild → accept residual risk with a ticket if needed. Do not ignore OS packages because “we only care about the app language”.

| Tool | Role |
|------|------|
| Trivy | OSS vuln + misconfig + SBOM |
| Docker Scout | Hub-integrated insights |
| Syft / Grype | SBOM + scan ecosystem |

### Key concepts

- **CVE noise** — triage by reachability and exploitability when possible  
- **Rebuild cadence** — periodic rebuilds pick up base patches  
- **Private base images** — control inheritance  
- **Sign + scan** — complementary supply-chain controls  


Wire scanners into both pull-request and main-branch pipelines so developers see findings early. Keep an allow-list process for accepted risks with expiry dates — permanent mute rules become invisible debt. After a major base-image upgrade, re-scan and redeploy even if application code did not change.

### Common pitfalls

- Scanning once at project start and never again  
- Suppressing all CVEs to keep CI green  
- Treating SBOM generation as paperwork without storing it  
- Scanning only the final stage while shipping a fat single-stage image

## Hands-on Lab



### Objective

Build or run a real Docker solution for **Container Scanning and SBOM** and prove it with inspect/logs/HTTP.

### Prerequisites

- Docker Engine or Docker Desktop
- Permission to run containers

### Lab environment

Workspace: `~/rebash-docker/module-12`

Local Docker daemon. Clean up containers/images after the lab.

```bash
mkdir -p ~/rebash-docker/module-12 && cd ~/rebash-docker/module-12
```

### Real-world scenario

You are validating **Container Scanning and SBOM** before it lands in CI. The change must be reproducible with copy-paste commands and leave no orphan containers.

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







- [ ] Lab commands run under `~/rebash-docker/module-12/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough







Production practice for **Container Scanning and SBOM** always combines:

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







!!! warning "Scanning once at project start and never again  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Suppressing all CVEs to keep CI green  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices







- Encode Container Scanning and SBOM changes as code and review them in pull requests
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







**Container Scanning and SBOM** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions




1. What is an SBOM and why store it in CI?
2. How do you triage a CRITICAL CVE in a base image?
3. Scanner false positives — how do you handle them?
4. When should a pipeline fail on findings?
5. Difference between image scan and runtime detection?

!!! tip "Sample answer — question 2"
    Confirm the package is present in the final image and whether a fixed base exists.

!!! tip "Sample answer — question 4"
    Gate production on policy and keep SBOMs as artifacts for incident response.

## Related Tutorials







- [Course overview](index.md)
- [Container Logging and Monitoring](container-logging-and-monitoring.md)

## References







- [Trivy](https://trivy.dev/) · [Docker Scout](https://docs.docker.com/scout/)
