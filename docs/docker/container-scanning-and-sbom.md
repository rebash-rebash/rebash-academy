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

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-12 && cd ~/rebash-docker/module-12
```

**Focus:** hands-on practice for Container Scanning and SBOM

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Container Scanning and SBOM"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-12 && cd ~/rebash-docker/module-12
docker pull alpine:3.20
# Install Trivy if needed: https://aquasecurity.github.io/trivy/
if command -v trivy >/dev/null; then
  trivy image --severity CRITICAL,HIGH alpine:3.20 | head -n 40
  trivy image --format cyclonedx -o sbom.json alpine:3.20
  head -n 20 sbom.json
else
  echo "Install Trivy, then re-run scan. Using docker scout if available:"
  docker scout quickview alpine:3.20 2>/dev/null || true
fi
cat > triage.md << 'EOF'
Image:
Critical count:
Action: rebuild base / waive / block
EOF
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later labs; destroy cloud resources you created
./lab.sh || true
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

1. How does **Container Scanning and SBOM** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Container Logging and Monitoring](container-logging-and-monitoring.md)

## References

- [Trivy](https://trivy.dev/) · [Docker Scout](https://docs.docker.com/scout/)
