---
title: Overview
description: "Git & GitHub for Cloud & DevOps Engineers — 17 modules covering Git workflows, GitHub collaboration, Actions, GitOps, IaC repos, security, and production practices."
difficulty: beginner
estimated_time: "5–7 weeks"
author: Shaik Basha
last_updated: "2026-08-03"
category: git
tags:
  - git
  - github
  - gitops
  - devops
  - course
comments: false
---

# Git & GitHub for Cloud & DevOps Engineers

**Duration:** 5–7 weeks · **Difficulty:** Beginner → Advanced

Practical Git and GitHub for Cloud, DevOps, Platform, and Site Reliability Engineering (SRE) — collaboration, Infrastructure as Code (IaC), GitOps, Continuous Integration/Continuous Delivery (CI/CD), and enterprise repository management.

!!! tip "Course status"
    **Full rewrite complete (2026-08-03).** All **17 modules** follow the academy Linux tutorial standard (`.cursor/prompts/tutorial-format-linux.md`) with topic-specific labs under `~/rebash-git/module-NN`, collapsible interview answers, and **Excalidraw** diagrams in `docs/assets/excalidraw/`. Regenerate diagrams with `python3 scripts/generate-excalidraw-svg.py`. Start with [Introduction to Git and Version Control](introduction-to-git-and-version-control.md).

## 1. Course overview

### Purpose

Manage production Git repositories, collaborate on GitHub, implement GitOps and IaC workflows safely, and recover from complex history incidents.

### Target roles

DevOps Engineer · Cloud Engineer · Platform Engineer · SRE · DevSecOps Engineer · Software Engineer · Infrastructure Engineer

### Prerequisites

- [Linux Fundamentals](../linux/index.md)
- Basic command line

### Capstone outcomes

Use Git in production · collaborate with pull requests · resolve merge/rebase incidents · design branching strategy · build GitHub Actions workflows · implement GitOps · secure repositories · support IaC delivery · apply production governance

## 2. Modules

| Module | Focus | Tutorials |
|-------:|-------|-----------|
| 1 | Version Control Fundamentals | [Introduction](introduction-to-git-and-version-control.md) · [Object model](understanding-the-git-object-model.md) |
| 2 | Installing Git | [Install and configure](git-installation-and-configuration.md) |
| 3 | Git Basics | [Create/clone](creating-and-cloning-repositories.md) · [Add/commit/push](basic-git-workflow-add-commit-push.md) · [History/diffs](viewing-history-and-diffs.md) |
| 4 | Working with Repositories | [gitignore & attributes](gitignore-and-gitattributes.md) |
| 5 | Branching | [Branching fundamentals](branching-fundamentals.md) |
| 6 | Merging | [Merging and conflicts](merging-and-merge-conflicts.md) |
| 7 | Rebasing & History | [Rebase](rebasing-and-interactive-rebase.md) · [Reset/revert/stash](undoing-changes-reset-revert-stash.md) · [Cherry-pick/reflog](cherry-pick-and-reflog.md) |
| 8 | Remotes | [Working with remotes](working-with-remotes.md) |
| 9 | GitHub Fundamentals | [GitHub fundamentals](github-fundamentals.md) |
| 10 | Collaboration | [Pull requests & review](pull-requests-and-code-review.md) |
| 11 | GitHub Actions | [Actions for DevOps](github-actions-for-devops.md) |
| 12 | GitOps | [GitOps fundamentals](gitops-fundamentals.md) |
| 13 | Infrastructure as Code | [Git for IaC](git-for-infrastructure-as-code.md) |
| 14 | Repository Management | [Repos & releases](repository-management-and-releases.md) |
| 15 | Security | [Signed commits & security](signed-commits-and-git-security.md) |
| 16 | Troubleshooting | [Troubleshooting](git-troubleshooting.md) · [Bisect](git-bisect-and-debugging-history.md) |
| 17 | Production practices | [Production Git practices](production-git-practices.md) |

### Optional depth

[Git hooks & automation](git-hooks-and-automation.md) · [Submodules & subtrees](git-submodules-and-subtrees.md) · [Git in CI/CD](git-in-ci-cd-and-devops.md) · [Advanced workflows](advanced-git-workflows.md)

## 3. Practice

- [Labs](../labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)
- [FAQ](faq.md) · [Roadmap](roadmap.md)

## Diagrams

Course diagrams (Excalidraw SVG):

- `git-workflow.svg` · `git-object-model.svg` · `git-branching-strategy.svg`
- `git-merge-process.svg` · `git-pr-lifecycle.svg` · `git-github-actions.svg`
- `git-gitops-flow.svg` · `git-repository-architecture.svg`

```bash
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Linux](../linux/index.md) · [GitHub Actions](../github-actions/index.md) · [Argo CD](../argocd/index.md) · [Terraform](../terraform/index.md)
- [DevOps Engineer path](../career-paths/devops-engineer/index.md)
