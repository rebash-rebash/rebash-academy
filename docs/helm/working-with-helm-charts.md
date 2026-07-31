---
title: "Working with Helm Charts"
description: "Create and explore chart structure — Chart.yaml, values.yaml, templates/, charts/, and helpers for Kubernetes packaging."
difficulty: intermediate
estimated_time: "40–55 min"
technology: helm
category: helm
module: "Module 3 · Working with Charts"
career_paths:
  - kubernetes-engineer
  - devops-engineer
  - platform-engineer
skills:
  - helm
  - charts
prerequisites:
  - helm/installing-helm-and-repositories
next:
  - helm/helm-templates-and-go-templating
related:
  - helm/production-helm-practices
labs: []
projects: []
interview: interview/helm
certifications:
  - CKAD
tags:
  - helm
  - charts
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Working with Helm Charts

## Overview

Scaffold a chart with `helm create`, walk the directory layout, and edit `Chart.yaml` metadata correctly.

A chart is a directory (or packaged `.tgz`) with a fixed layout. Know what belongs in `templates/` vs `values.yaml` vs `charts/`.

This is a core tutorial in **Module 3 · Working with Charts** of the REBASH Academy **Helm for Kubernetes Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Installing Helm and Repositories](installing-helm-and-repositories.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run `helm create`  
- [ ] Explain Chart.yaml fields  
- [ ] Locate values, templates, helpers  
- [ ] List files safely with `helm show`

## Architecture

This topic’s control points and relationships are shown below.

![Chart structure](../assets/excalidraw/helm-chart-structure.svg)

## Theory

### What it is

A **Helm chart** is a directory (or packaged `.tgz`) with a conventional layout. At minimum you care about `Chart.yaml` (metadata), `values.yaml` (defaults), and `templates/` (Kubernetes manifests written as Go templates). Optional pieces include `charts/` for vendored subcharts, `templates/_helpers.tpl` for shared named templates, `NOTES.txt` for post-install messages, and `.helmignore` to exclude files from the package.

| Path | Purpose |
|------|---------|
| `Chart.yaml` | name, `version`, `appVersion`, dependencies |
| `values.yaml` | Default configuration consumers override |
| `templates/` | Templated Kubernetes manifests |
| `templates/_helpers.tpl` | Named templates / labels helpers |
| `charts/` | Packaged subcharts after `helm dependency update` |
| `.helmignore` | Files excluded from `helm package` |

### Why it matters

Charts are how teams share a consistent Deployment/Service/Ingress shape. If you cannot read a chart’s layout quickly, you cannot review pull requests, debug a bad release, or decide what belongs in values versus hard-coded template text. Platform engineering lives or dies on clear chart boundaries: application charts for workloads, library charts for shared snippets, and disciplined SemVer for the package itself.

### How it works

`helm create mychart` scaffolds the layout. Authors edit templates and defaults; consumers override values at install time. `helm lint` checks structure and common mistakes. `helm package` builds a versioned archive using `Chart.yaml`’s `version` field. When dependencies are declared, `helm dependency update` downloads them into `charts/` and records pins in `Chart.lock`.

Distinguish two version fields:

- **`version`** — SemVer of the **chart package** (what you bump when templates/values change).
- **`appVersion`** — informational version of the **application** the chart deploys (not used by Helm’s dependency resolver as a SemVer constraint the same way).

### Key concepts and comparisons

Think of a chart like a software package: metadata (`Chart.yaml`), configuration knobs (`values.yaml`), and build inputs (`templates/`). The rendered output is ordinary Kubernetes YAML — charts do not invent a new runtime. Files under `templates/` whose names start with `_` are partials (helpers), not standalone manifests.

### Common pitfalls

- Treating `appVersion` as the image tag — image tags usually live under `values.yaml` (`image.tag`) and may differ from `appVersion`.
- Putting environment-specific hosts and secrets into the chart defaults and committing them.
- Editing files inside `charts/` by hand instead of declaring dependencies and running `helm dependency update`.
- Shipping huge non-template assets because `.helmignore` was never configured.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-helm/module-03 && cd ~/rebash-helm/module-03
```

**Focus:** hands-on practice for Working with Helm Charts

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Working with Helm Charts"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

```bash
mkdir -p ~/rebash-helm/module-03 && cd ~/rebash-helm/module-03
helm create rebash-app
find rebash-app -type f | sort
head -n 20 rebash-app/Chart.yaml
helm show chart ./rebash-app
helm lint ./rebash-app
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-helm/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-helm/module-03/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Working with Helm Charts** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for helm as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Treating `appVersion` as the image tag — image tags usually live under `values.yaml` (`ima"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Putting environment-specific hosts and secrets into the chart defaults and committing them"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Working with Helm Charts changes as code and review them in pull requests
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

**Working with Helm Charts** is essential for Cloud and DevOps engineers working with helm. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Working with Helm Charts** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Helm Templates and Go Templating](helm-templates-and-go-templating.md)

## References

- [Charts](https://helm.sh/docs/topics/charts/)
