---
title: Learning Roadmap
description: "Structured 17-module learning roadmap with pacing for Git & GitHub for Cloud & DevOps Engineers."
technology_id: git
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: git
tags:
  - git
  - github
  - roadmap
---

# Git & GitHub — Learning Roadmap

Structured path for **Git & GitHub for Cloud & DevOps Engineers**. Estimated **5–7 weeks** at 6–8 hours per week. All core tutorials rewritten **2026-08-03** to the Linux quality bar.

## How to use this roadmap

1. Complete **Modules 1–3** before branching work — vocabulary and daily loop matter.
2. Run each lab in `~/rebash-git/module-NN` on a Linux VM, macOS, or WSL.
3. After **Module 8**, add a GitHub sandbox org for Modules 9–11 optional push steps.
4. Finish **Modules 12–17** before the capstone.
5. Use [FAQ](faq.md) for GitHub Actions, GitOps, and recovery questions.

## Pacing guide

| Week | Modules | Focus | Hours (approx.) |
|------|---------|-------|-----------------|
| 1 | 1–2 | VCS concepts, install, config, object model | 6–8 |
| 2 | 3–4 | Daily workflow, history, gitignore | 6–8 |
| 3 | 5–6 | Branches, merge, conflicts | 6–8 |
| 4 | 7–8 | Rebase, undo, cherry-pick, remotes | 8–10 |
| 5 | 9–10 | GitHub, PRs, CODEOWNERS | 6–8 |
| 6 | 11–13 | Actions, GitOps, IaC repos | 8–10 |
| 7 | 14–17 | Releases, security, troubleshooting, production policy | 8–10 |

Adjust pace if you already use Git daily — skip to Module 5+ assessment via tutorial interview questions.

## Module map

| # | Module | Tutorials | Lab path |
|---|--------|-----------|----------|
| 1 | Version control fundamentals | [Introduction](introduction-to-git-and-version-control.md) · [Object model](understanding-the-git-object-model.md) | `~/rebash-git/module-01` |
| 2 | Installing Git | [Install and configure](git-installation-and-configuration.md) | `~/rebash-git/module-02` |
| 3 | Git basics | [Create/clone](creating-and-cloning-repositories.md) · [Add/commit/push](basic-git-workflow-add-commit-push.md) · [History/diffs](viewing-history-and-diffs.md) | `~/rebash-git/module-03` |
| 4 | Repositories | [gitignore & attributes](gitignore-and-gitattributes.md) | `~/rebash-git/module-04` |
| 5 | Branching | [Branching fundamentals](branching-fundamentals.md) | `~/rebash-git/module-05` |
| 6 | Merging | [Merging and conflicts](merging-and-merge-conflicts.md) | `~/rebash-git/module-06` |
| 7 | Rebase & history | [Rebase](rebasing-and-interactive-rebase.md) · [Reset/revert/stash](undoing-changes-reset-revert-stash.md) · [Cherry-pick/reflog](cherry-pick-and-reflog.md) | `~/rebash-git/module-07` |
| 8 | Remotes | [Working with remotes](working-with-remotes.md) | `~/rebash-git/module-08` |
| 9 | GitHub fundamentals | [GitHub fundamentals](github-fundamentals.md) | `~/rebash-git/module-09` |
| 10 | Collaboration | [Pull requests & review](pull-requests-and-code-review.md) | `~/rebash-git/module-10` |
| 11 | GitHub Actions | [Actions for DevOps](github-actions-for-devops.md) | `~/rebash-git/module-11` |
| 12 | GitOps | [GitOps fundamentals](gitops-fundamentals.md) | `~/rebash-git/module-12` |
| 13 | IaC | [Git for IaC](git-for-infrastructure-as-code.md) | `~/rebash-git/module-13` |
| 14 | Repo management | [Repos & releases](repository-management-and-releases.md) | `~/rebash-git/module-14` |
| 15 | Security | [Signed commits & security](signed-commits-and-git-security.md) | `~/rebash-git/module-15` |
| 16 | Troubleshooting | [Troubleshooting](git-troubleshooting.md) · [Bisect](git-bisect-and-debugging-history.md) | `~/rebash-git/module-16` |
| 17 | Production | [Production Git practices](production-git-practices.md) | `~/rebash-git/module-17` |

## Diagrams by module

| Diagram | Used in |
|---------|---------|
| `git-workflow.svg` | Modules 1, 3, 7, 16 |
| `git-object-model.svg` | Modules 1, 3, 7, 16 |
| `git-repository-architecture.svg` | Modules 3, 4, 8, 9, 13–15 |
| `git-branching-strategy.svg` | Modules 5, 7, 17 |
| `git-merge-process.svg` | Module 6 |
| `git-pr-lifecycle.svg` | Module 10 |
| `git-github-actions.svg` | Module 11 |
| `git-gitops-flow.svg` | Module 12 |

Regenerate: `python3 scripts/generate-excalidraw-svg.py`

## Milestones

| Milestone | You can… | Modules |
|-----------|----------|---------|
| **Git operator** | init, commit, branch, merge, recover locally | 1–7 |
| **Remote collaborator** | multi-remote, fetch, prune, upstream | 8 |
| **GitHub practitioner** | Issues, PRs, Actions validate, CODEOWNERS | 9–11 |
| **Delivery engineer** | GitOps layout, IaC tags, releases | 12–14 |
| **Production ready** | signing, scanning, bisect, branch policy ADR | 15–17 |

## Optional depth (after Module 17)

| Topic | Tutorial |
|-------|----------|
| Hooks & automation | [git-hooks-and-automation.md](git-hooks-and-automation.md) |
| Submodules & subtrees | [git-submodules-and-subtrees.md](git-submodules-and-subtrees.md) |
| Git in CI/CD | [git-in-ci-cd-and-devops.md](git-in-ci-cd-and-devops.md) |
| Advanced workflows | [advanced-git-workflows.md](advanced-git-workflows.md) |

## Next steps after the roadmap

- Capstone — production GitOps platform repository
- Interview prep
- Cheat sheets
- Related courses: [Terraform](../terraform/index.md) · [Argo CD](../argocd/index.md) · [Linux](../linux/index.md)
