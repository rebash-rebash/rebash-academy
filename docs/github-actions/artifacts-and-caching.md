---
title: "Artifacts and Caching"
description: "Upload and download workflow artefacts, cache dependencies, choose cache keys, and avoid common correctness pitfalls."
difficulty: intermediate
estimated_time: "40–55 min"
technology: github-actions
category: github-actions
module: "Module 6 · Artifacts & Caching"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - github-actions
  - artifacts
  - caching
prerequisites:
  - github-actions/secrets-variables-and-oidc
next:
  - github-actions/docker-pipelines-with-github-actions
related:
  - github-actions/testing-in-github-actions
  - github-actions/docker-pipelines-with-github-actions
labs: []
projects: []
interview: interview/github-actions
certifications:
  - GitHub Actions
tags:
  - github-actions
  - artifacts
  - cache
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Artifacts and Caching

## Overview

Configure artefact upload/download so a build job produces a shareable package a test job consumes, and add a lockfile-keyed dependency cache without treating cache as a correctness guarantee.

**Artefacts** (GitHub spelling in the product UI: *artifacts*) are job outputs GitHub stores for download, retention, and sharing across jobs in a workflow run — packages, binaries, test reports, and logs. **Caching** restores dependency directories between runs to cut install time; cache is **best-effort** and must never replace pinned lockfiles. Confusing the two causes flaky pipelines and bloated storage bills.

This is a core tutorial in **Module 6 · Artifacts & Caching** of the REBASH Academy **GitHub Actions for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Secrets, Variables, and OIDC](secrets-variables-and-oidc.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Upload artefacts with `actions/upload-artifact` and retention  
- [ ] Download artefacts in a later job with `actions/download-artifact`  
- [ ] Configure `actions/cache` (or setup-* cache) with a lockfile key  
- [ ] Distinguish artefact vs cache vs container registry image  
- [ ] List pitfalls that cause stale or missing caches

## Architecture

This topic’s control points and relationships are shown below.

![Artifacts and caching](../assets/excalidraw/gha-artifacts-cache.svg)

## Theory

### What it is

GitHub Actions separates **what you ship between jobs** from **what you hope to reuse for speed**:

| Mechanism | Purpose | Guaranteed? |
|-----------|---------|-------------|
| Artefacts | Persist outputs for later jobs / humans | Yes (within retention) |
| Cache | Speed dependency or build dirs across runs | No — miss, evict, or empty |
| Package / container registry | Immutable release distribution | Via your registry policy |

**Upload artefact** actions package paths from the runner and store them against the workflow run. Downstream jobs **download** by name (and optional pattern). Retention defaults apply; set shorter retention for intermediate builds and keep release artefacts on tags or push immutable images to GHCR / another registry.

**Cache** stores a keyed blob (for example `~/.npm` or `~/.cache/pip`). Keys usually hash `package-lock.json`, `poetry.lock`, or `go.sum` so installs invalidate when dependencies change. Restore keys allow partial matches (same OS, older lockfile hash) as a softer fallback. Official setup actions (`actions/setup-node`, `setup-python`, …) often wrap caching for you.

### Why it matters

Slow pipelines waste runner minutes and delay review feedback. Wrong cache design causes “works on my branch” builds when a stale cache hides a missing lockfile or native binary mismatch. Artefacts make builds auditable: the same tarball that passed tests can be promoted or attached to a release. Platform teams set retention and size policies so Actions storage does not become an unbounded object store. In regulated environments, knowing *which artefact SHA* was deployed matters as much as the Git commit.

### How it works

1. A **build** job writes files under a path (for example `dist/`) and uploads them with a stable artefact name.  
2. A **test** job declares `needs: [build]`, downloads that artefact, and runs checks against the exact bits.  
3. An optional **cache** step restores a dependency directory using a key derived from the lockfile; the job still runs install if the cache is cold.  
4. Failed jobs can still upload (`if-no-files-found`, `if: always()`) when you need logs or reports.  
5. Expired artefacts disappear; caches may be evicted — never assume either is permanent storage.

Prefer short retention for intermediate binaries; publish releases to a registry or GitHub Releases rather than relying on 90-day artefact downloads.

### Key concepts and comparisons

| Concern | Artefacts | Cache |
|---------|-----------|-------|
| Correctness | Part of the pipeline contract | Optimisation only |
| Scope | Same workflow run (primarily) | Cross-run within repo/branch scope rules |
| UI | Downloadable from the run | Opaque speed-up |
| Security | Can contain secrets — scope carefully | Same if you cache credentials |

| Strategy | Key idea |
|----------|----------|
| Exact lockfile key | Invalidate on dependency change |
| Restore-keys prefix | Warm partial hit when exact misses |
| Per-OS in key | Avoid Linux cache on macOS runners |
| Segment by job | Prevent test caches poisoning build caches |

### Common pitfalls

- Treating cache as a substitute for committing lockfiles.  
- Caching the entire workspace including `.env` or cloud credentials.  
- Omitting retention and filling storage with huge `node_modules` artefacts (artefacts are the wrong tool for that — use cache or registry).  
- Expecting downloads without `needs:` ordering or mismatched artefact names.  
- Sharing mutable caches across privileged and untrusted jobs without isolation.  
- Confusing job artefacts with images in GitHub Container Registry (GHCR).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-github-actions/module-06/.github/workflows && cd ~/rebash-github-actions/module-06/.github/workflows
```

**Focus:** hands-on practice for Artifacts and Caching

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Artifacts and Caching"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-github-actions/module-06/.github/workflows
cd ~/rebash-github-actions/module-06
```

Credentials are not required — push when you have a repository. The workflow builds a tiny artefact and uses a pip cache key file.

```bash
cd ~/rebash-github-actions/module-06
printf 'pytest\n' > requirements.txt
mkdir -p src
printf 'print("hello")\n' > src/app.py
```

{% raw %}
```yaml
# .github/workflows/artifacts-cache.yml
name: Module 6 artifacts and cache

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
          cache-dependency-path: requirements.txt

      - name: Install and package
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          mkdir -p dist
          cp src/app.py dist/app.py
          echo "build-${GITHUB_SHA}" > dist/build-id.txt

      - name: Upload dist artefact
        uses: actions/upload-artifact@v4
        with:
          name: app-dist
          path: dist/
          retention-days: 3

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download dist artefact
        uses: actions/download-artifact@v4
        with:
          name: app-dist
          path: dist/

      - name: Verify artefact
        run: |
          test -f dist/app.py
          test -f dist/build-id.txt
          cat dist/build-id.txt
          python dist/app.py

      - name: Explicit cache example (optional pattern)
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
```
{% endraw %}

```bash
# After push: open the workflow run → Artifacts → app-dist
# Confirm test job downloaded build-id.txt matching the commit
# actionlint .github/workflows/artifacts-cache.yml 2>/dev/null || true
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-github-actions/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-github-actions/module-06/.github/workflows/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Artifacts and Caching** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for github-actions as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Treating cache as a substitute for committing lockfiles.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Caching the entire workspace including `.env` or cloud credentials.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Artifacts and Caching changes as code and review them in pull requests
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

**Artifacts and Caching** is essential for Cloud and DevOps engineers working with github-actions. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Artifacts and Caching** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Docker Pipelines with GitHub Actions](docker-pipelines-with-github-actions.md)

## References

- [Storing workflow data as artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)  
- [Caching dependencies to speed up workflows](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)  
- [upload-artifact](https://github.com/actions/upload-artifact) · [cache](https://github.com/actions/cache)
