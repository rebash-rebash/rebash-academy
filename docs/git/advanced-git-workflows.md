---
title: Advanced Git Workflows
description: Compare GitFlow, GitHub Flow, trunk-based development, and release branching; choose strategies for DevOps, platform, and application teams.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: git
tags:
  - git
  - workflow
  - gitflow
  - trunk-based
prerequisites:
  - Git Hooks and Automation
  - Pull Requests and Code Review
  - Rebasing and Interactive Rebase
comments: false
---

# Advanced Git Workflows

## Overview

Branching strategy shapes how fast you ship and how painful merges become. GitFlow's long-lived branches suit scheduled releases; trunk-based development suits continuous deployment; GitHub Flow balances simplicity and review. Platform and application teams often need different models — this tutorial helps you choose and implement the right one.

This is **Tutorial 17** in **Module 6: Advanced & DevOps** of the REBASH Academy Git series.

## Prerequisites

- [Git Hooks and Automation](git-hooks-and-automation.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Compare GitFlow, GitHub Flow, and trunk-based development
- [ ] Identify when long-lived vs short-lived branches fit
- [ ] Implement environment promotion with tags and branches
- [ ] Apply feature flags as alternative to long-lived branches
- [ ] Align branching with CI/CD and release cadence
- [ ] Document team workflow in CONTRIBUTING.md
- [ ] Migrate gradually between workflow models

## Workflow Comparison Diagram

```mermaid
flowchart TB
    subgraph TBD["Trunk-Based"]
        MAIN1[main — always deployable]
        FB1["short feature branches<br/>hours to days"]
        FB1 --> MAIN1
    end

    subgraph GHF["GitHub Flow"]
        MAIN2[main]
        FB2[feature branch + PR]
        FB2 --> MAIN2
        MAIN2 --> DEPLOY[deploy from main]
    end

    subgraph GF["GitFlow"]
        MAIN3[main]
        DEV[develop]
        FEAT["feature/*"]
        REL["release/*"]
        HOT["hotfix/*"]
        FEAT --> DEV --> REL --> MAIN3
        HOT --> MAIN3
        HOT --> DEV
    end```

## Theory

### GitHub Flow

Popularized by GitHub — simple model for web apps with continuous deployment:

1. `main` is always deployable
2. Create descriptive branch from `main`
3. Commit and push regularly
4. Open PR when ready
5. Review and discuss
6. Merge to `main` after CI pass
7. Deploy immediately from `main`

**Best for:** SaaS, internal tools, teams deploying multiple times daily.

**DevOps fit:** Argo CD syncs `main` to staging; production deploy on tag or manual promotion.

### Trunk-Based Development

Developers commit to **main** (trunk) or merge within 1–2 days from short branches:

- Branches live < 48 hours
- **Feature flags** hide incomplete work in production
- Strong CI required — main must always pass
- No long-lived `develop` branch

Google and Meta scale this with massive CI investment.

**Best for:** High-performing teams, microservices, continuous deployment.

**DevOps fit:** Single pipeline on main; environment differences via config overlays, not branches.

### GitFlow

Vincent Driessen's model — structured releases:

| Branch | Purpose |
|--------|---------|
| `main` | Production releases only |
| `develop` | Integration branch |
| `feature/*` | New work off develop |
| `release/*` | Stabilization before prod |
| `hotfix/*` | Emergency fix off main |

Release branch gets bug fixes; merges to `main` (tagged) and back to `develop`.

**Best for:** Scheduled releases, mobile apps, shrink-wrapped software.

**DevOps caution:** Long-lived `develop` diverges from `main`; merge pain and drift common in IaC repos.

### GitLab Flow

Adds **environment branches** or **upstream-first** with optional production branch:

- Merge request → `main` → auto-deploy staging
- Cherry-pick or merge to `production` for prod deploy

Bridges GitHub Flow simplicity with environment gates.

### Choosing a Strategy

| Factor | Trunk-based | GitHub Flow | GitFlow |
|--------|-------------|-------------|---------|
| Release cadence | Continuous | Daily–weekly | Weeks/months |
| Team size | Any with CI maturity | Small–medium | Large, multi-team |
| IaC repos | Preferred | Good | Often painful |
| Feature flags needed | Yes | Sometimes | Less |
| Compliance gates | Via PR + CI | Via PR + CI | Via release branch |

**Platform/DevOps recommendation:** Trunk-based or GitHub Flow for Terraform/K8s — environment separation via directories or workspaces, not long-lived branches.

### Feature Flags vs Feature Branches

Long branches hide incomplete features. **Feature flags** (LaunchDarkly, env vars, config toggles) allow merging incomplete code disabled in prod:

```hcl
# Terraform variable
variable "enable_new_waf" {
  default = false
}
```

Merge to main with flag off; enable in staging; flip in prod when ready.

### Release Tagging

Regardless of workflow, **annotated tags** mark releases:

```bash
git tag -a v2.4.0 -m "Release 2.4.0 — CVE fixes"
git push origin v2.4.0
```

Tags trigger production pipelines; immutable deployment references.

### Monorepo Considerations

Large monorepos (Bazel, Nx) often use trunk-based with path-based CI — only test changed modules. Branch strategy matters less than selective CI.

### Documenting Workflow

`CONTRIBUTING.md` should specify:

- Branch naming
- Merge strategy (squash vs merge)
- Required checks
- Hotfix procedure
- Release tagging process

### Measuring Workflow Health

High-performing teams track:

- **Branch lifetime** — median hours from branch create to merge (target: under 48h)
- **PR size** — lines changed per PR (target: under 400)
- **Merge frequency** — commits to main per day
- **Change failure rate** — deploys requiring hotfix revert

Git commands supporting metrics:

```bash
git log --merges --since="30 days ago" --oneline | wc -l
git for-each-ref --sort=-committerdate refs/heads/ --format='%(refname:short) %(committerdate:relative)'
```

Review quarterly with platform team; adjust workflow if branch lifetime exceeds one week consistently.

## Hands-on Lab

### Step 1 – Simulate GitHub Flow

**Command:**

```bash
mkdir -p /tmp/git-workflow-lab && cd /tmp/git-workflow-lab
git init -b main
echo "1.0.0" > VERSION && git add . && git commit -m "release: v1.0.0 baseline"
git switch -c feature/add-metrics
echo "metrics=on" >> config.env && git commit -am "feat: enable metrics"
git switch main && git merge --no-ff feature/add-metrics -m "Merge PR: add metrics"
git tag -a v1.1.0 -m "Release 1.1.0"
git log --oneline --graph --decorate -5
```

### Step 2 – Simulate hotfix (GitFlow-style)

**Command:**

```bash
git switch -c hotfix/security-patch v1.0.0 2>/dev/null || git switch -c hotfix/security-patch HEAD~2
echo "patch=applied" >> security.patch && git add . && git commit -m "fix: security patch"
git switch main && git merge --no-ff hotfix/security-patch -m "Merge hotfix: security"
git tag -a v1.0.1 -m "Hotfix 1.0.1"
git log --oneline --graph --all --decorate -8
```

### Step 3 – Trunk-based short branch

**Command:**

```bash
git switch main
git switch -c fix/typo
echo "# fixed typo" >> README.md 2>/dev/null || echo "# README fixed" > README.md
git commit -am "fix: typo in README"
git switch main && git merge --ff-only fix/typo
git branch -d fix/typo
git log --oneline -3
```

### Step 4 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-workflow-lab
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `git tag -a v1.0.0 -m "msg"` | Annotated release tag | Production deploy trigger |
| `git merge --ff-only` | Trunk-based fast-forward | Enforce linear main |
| `git switch -c hotfix/x main` | Hotfix branch | Emergency fix |
| `git log --graph --decorate --all` | Visualize workflow | Team alignment |
| `git branch --merged main` | Find merged branches | Cleanup |

### CONTRIBUTING.md workflow snippet

```markdown
## Branching
- Branch from `main`: `feature/`, `fix/`, `hotfix/`
- Keep branches < 2 days (trunk-based)
- Open PR when ready; require 1 approval + CI pass
- Squash merge to `main`

## Releases
- Tag `main` with `vX.Y.Z` for production deploy
- Hotfix: branch from tag, merge to `main`, tag patch release
```

## Common Mistakes

!!! warning "GitFlow for Terraform without release cadence"
    Long-lived develop branch drifts; plan diffs become unmanageable. Use trunk-based.

!!! warning "Production branch without protection"
    Direct pushes bypass review. Protect all production-related branches.

!!! warning "Tags moved or deleted"
    Breaks deployment traceability. Immutable tags; never retag released versions.

!!! warning "No documented hotfix path"
    Incidents cause ad-hoc force pushes. Document hotfix branch + cherry-pick procedure.

## Best Practices

!!! tip "Optimize for merge frequency, not branch count"
    Integrate to main daily; reduce merge conflict cost.

!!! tip "Separate environment config from branch strategy"
    Use `environments/dev/` vs `environments/prod/` directories or Terraform workspaces.

!!! tip "Align merge strategy with workflow"
    Trunk-based often uses squash or rebase; GitFlow uses merge commits on release.

!!! tip "Review workflow annually"
    Team scale and release cadence change — workflow should evolve.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| develop/main divergence | GitFlow without back-merge | Regular merges both directions |
| Cannot ff-only merge | Branch diverged | Rebase feature; or allow merge commit |
| Wrong tag deployed | Tag on wrong commit | Protect tags; verify SHA in pipeline |
| Feature branch stale | Long-lived branch | Rebase or abandon; use flags |
| Hotfix missing on develop | Incomplete GitFlow merge | Cherry-pick hotfix to integration branch |
| Monorepo CI too slow | Full test on every commit | Path-based CI filters |

## Summary

- **GitHub Flow:** main + feature PRs — simple, continuous deployment friendly
- **Trunk-based:** very short branches, feature flags — highest merge frequency
- **GitFlow:** main + develop + release/hotfix — scheduled releases, higher overhead
- DevOps/IaC teams typically prefer **trunk-based or GitHub Flow**
- **Annotated tags** mark releases regardless of branching model
- Document workflow in **CONTRIBUTING.md** and align with CI/CD gates

## Interview Questions

1. What is trunk-based development?
2. Compare GitFlow and GitHub Flow.
3. When would you choose GitFlow over trunk-based?
4. What role do feature flags play in branching strategy?
5. How should DevOps/IaC repositories handle environment promotion?
6. What is a hotfix branch, and how does it merge?
7. Why are long-lived feature branches problematic?
8. What merge strategy pairs well with trunk-based development?
9. How do annotated tags relate to release workflow?
10. What should CONTRIBUTING.md document about branching?

??? tip "Sample Answers (Questions 1 and 5)"

    **Q1 — Trunk-based:** Developers integrate to a single main branch frequently — ideally daily or multiple times daily. Feature branches, if used, live less than 48 hours. Incomplete features hide behind feature flags. Requires strong CI keeping main always green. Minimizes merge debt and enables continuous deployment.

    **Q5 — IaC environment promotion:** Avoid long-lived environment branches that diverge. Store environment-specific values in separate directories (`envs/dev/`, `envs/prod/`), Terraform workspaces, or external config stores. Promote by merging to main and deploying with environment-specific pipeline parameters or GitOps paths — not by merging develop → release → main.

## Related Tutorials

- [Git Hooks and Automation](git-hooks-and-automation.md) *(previous)*
- [Git Submodules and Subtrees](git-submodules-and-subtrees.md) *(next)*
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Git in CI/CD and DevOps](git-in-ci-cd-and-devops.md)
- [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md)

## References

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [GitFlow original post](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow guide](https://docs.github.com/en/get-started/using-github/github-flow)
- [GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)
- [DORA Research – trunk-based development](https://dora.dev/)
- [REBASH Academy – Git Overview](index.md)
