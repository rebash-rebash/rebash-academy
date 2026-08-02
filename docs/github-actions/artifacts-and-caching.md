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



### Objective

Author a GitHub Actions workflow that implements **Artifacts and Caching** and validate YAML structure locally.

### Prerequisites

- Python 3 with PyYAML
- Optional: GitHub repo to run the workflow

### Lab environment

Workspace: `~/rebash-github-actions/module-06/.github/workflows`

Workflows under `.github/workflows/`. In docs, wrap GitHub Actions expressions in Jinja raw blocks so MkDocs macros do not parse them; use heredocs in the lab.

```bash
mkdir -p ~/rebash-github-actions/module-06/.github/workflows && cd ~/rebash-github-actions/module-06/.github/workflows
```

### Real-world scenario

Platform engineering wants **Artifacts and Caching** as a reusable workflow pattern. You prototype YAML that passes review and runs on `ubuntu-latest`.

### Step-by-step tasks

#### Task 1 – Create workflow file

Jobs and steps must be explicit; pin mainstream actions.

```bash
mkdir -p .github/workflows
cat > .github/workflows/lab.yml << 'EOF'
name: lab
on:
  workflow_dispatch:
  push:
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Prove workspace
        run: |
          mkdir -p out
          echo ok > out/marker.txt
          test -s out/marker.txt
EOF
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/lab.yml')); print('workflow OK')"
```

**Expected output:** `workflow OK` printed; file exists under `.github/workflows/`.

#### Task 2 – Dry-run the shell steps locally

The `run:` block should work in a normal shell before CI.

```bash
mkdir -p out && echo ok > out/marker.txt
test -s out/marker.txt && cat out/marker.txt
```

**Expected output:** Prints `ok`.

### Validation steps

- [ ] Workflow YAML parses
- [ ] Local run steps succeed

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid workflow file | YAML/indent | Validate with PyYAML / actionlint |
| Action not found | Bad uses ref | Pin `actions/checkout@v4` |
| Permission denied | Missing permissions/OIDC | Set least-privilege `permissions:` |

### Challenge exercise

Add a second job with `needs: build` that uploads `out/` as an artefact (YAML only is fine offline).

### Learning outcomes

- Created a real workflow file
- Validated structure before push

### Cleanup

```bash
# Keep workflow stubs under ~/rebash-github-actions/
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






1. Cache vs artifact — which is authoritative for build outputs?
2. Cache restores but builds still slow — what else matters?
3. How do you pass files from job A to job B reliably?
4. What security caution applies to caches?
5. When should artifact retention be short?

!!! tip "Sample answer — question 2"
    Confirm upload/download names match and the producer job succeeded. Caches are best-effort acceleration, not a contract between jobs.

!!! tip "Sample answer — question 4"
    Do not cache secrets or writable shared directories across untrusted branches without careful keying.

## Related Tutorials








- [Course overview](index.md)
- [Docker Pipelines with GitHub Actions](docker-pipelines-with-github-actions.md)

## References








- [Storing workflow data as artifacts](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts)  
- [Caching dependencies to speed up workflows](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)  
- [upload-artifact](https://github.com/actions/upload-artifact) · [cache](https://github.com/actions/cache)
