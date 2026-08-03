---
title: FAQ
description: "Frequently asked questions about Git, GitHub, Actions, GitOps, and the REBASH Git course."
technology_id: git
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: git
tags:
  - git
  - github
  - faq
---

# Git & GitHub — FAQ

Answers for learners on the **Git & GitHub for Cloud & DevOps Engineers** course. Tutorials were fully rewritten to the academy standard on **2026-08-03**.

## Course structure

### Who is this course for?

Cloud, DevOps, Platform, SRE, DevSecOps, and software engineers who need **production** Git and GitHub skills — not just `git add` / `git commit`, but branching policy, GitOps repos, Actions, IaC versioning, and incident recovery.

### What was rewritten in the 2026-08-03 update?

All **17 core modules** (19 tutorials) now follow `.cursor/prompts/tutorial-format-linux.md`: full Theory depth, topic-specific labs in `~/rebash-git/module-NN`, Excalidraw diagrams, collapsible interview answers, and British English. Modules 1–2 and the first Module 3 tutorial were rewritten earlier in the same pass; do not overwrite those four files when syncing.

### Do I need Linux first?

Yes — [Linux Fundamentals](../linux/index.md) and comfort with the shell. Labs use bash on macOS, Linux, or WSL.

### Do I need a GitHub account?

Modules 1–8 work with **local bare remotes** only. GitHub-specific modules (9–11) include local checklist artefacts; optional `gh` CLI steps are marked when a account helps.

## Git fundamentals

### Merge vs rebase — which should I use?

**Merge** preserves branch topology and is safe on shared branches. **Rebase** linearises history on **private feature branches** before PR — never rebase commits others have pulled. See [Merging and Merge Conflicts](merging-and-merge-conflicts.md) and [Rebasing and Interactive Rebase](rebasing-and-interactive-rebase.md).

### reset vs revert on main?

**Revert** adds a forward commit that undoes a change — use on **shared/pushed** history. **Reset** moves branch pointers — only for **local/unpushed** fixes. See [Undoing Changes](undoing-changes-reset-revert-stash.md).

### Where should Terraform state live?

Never in Git. Use a remote backend; ignore `*.tfstate` locally. See [.gitignore and .gitattributes](gitignore-and-gitattributes.md) and [Git for IaC](git-for-infrastructure-as-code.md).

### What is detached HEAD?

HEAD points at a commit instead of a branch — common after checking out a tag. Create a branch to keep work: `git switch -c rescue`. See [Git Troubleshooting](git-troubleshooting.md).

## GitHub and collaboration

### What is the difference between Git and GitHub?

**Git** is the distributed version control tool and object database. **GitHub** is a hosted forge (remote, PRs, Issues, Actions, security scanning). You can learn Git modules 1–8 without GitHub.

### When are pull requests required?

Whenever branch protection enforces them — standard for `main` in production repos. PRs bundle diff, review, and CI status. See [Pull Requests and Code Review](pull-requests-and-code-review.md).

### What are CODEOWNERS?

A file mapping paths to teams that must review changes — e.g. `*.tf @platform-team`. See [Pull Requests and Code Review](pull-requests-and-code-review.md).

## GitHub Actions

### Do I need Actions if I use Jenkins or GitLab CI?

Concepts transfer (triggers, jobs, secrets). This course teaches Actions because many GitHub-hosted repos standardise on it. Workflow YAML lives under `.github/workflows/`. See [GitHub Actions for DevOps](github-actions-for-devops.md).

### How do I avoid leaking secrets in Actions logs?

Use GitHub Secrets, OIDC to cloud roles, minimal `permissions:`, and never echo secrets. Enable secret scanning and push protection. See [Signed Commits and Git Security](signed-commits-and-git-security.md).

### Why does MkDocs break on GitHub Actions expressions in docs?

MkDocs macros interpret GitHub Actions expression markers (dollar-brace-brace). Wrap documentation examples in raw Jinja blocks so macros skip them; committed workflow files use normal Actions syntax. See the note at the bottom of [GitHub Actions for DevOps](github-actions-for-devops.md).

## GitOps

### What is GitOps in one sentence?

Git is the **source of truth** for desired cluster state; a controller **pulls** and reconciles — humans avoid ad hoc `kubectl apply` in production. See [GitOps Fundamentals](gitops-fundamentals.md).

### apps/ vs clusters/ layout?

**apps/** holds reusable bases; **clusters/&lt;env&gt;/** holds environment overlays and version pins. See the lab in [GitOps Fundamentals](gitops-fundamentals.md).

### Argo CD or Flux?

Both implement Kubernetes GitOps; course principles apply to either. Links in tutorial References.

## Labs and practice

### Where do labs run?

Topic labs use `~/rebash-git/module-NN` (e.g. `module-03` for Git basics workflow). Each lab has 2–4 tasks, expected output, and asserts — not note-taking exercises.

### How do labs relate to the capstone?

Module labs build skills; the [capstone](capstone/index.md) combines branch protection, Actions, semver, GitOps layout, and security scanning in one repository design.

## Certification and careers

### Which certifications align with this course?

GitHub Foundations, GitHub Actions, GitHub Administration, and Advanced Security topics map across modules 9–15. See [course index](index.md).

### Interview preparation?

Every tutorial includes 6–8 topic-specific questions with `??? success "Reveal answer"` blocks. Consolidated banks live under [Interview](interview/index.md).

## Getting help

### Something broke in a lab — first steps?

1. `git status`
2. Read **Common errors and fixes** in that tutorial
3. [Git Troubleshooting](git-troubleshooting.md) for detached HEAD, auth, merge abort
4. [Cherry-pick and Reflog](cherry-pick-and-reflog.md) for lost commits

### Where is the full module list?

[course index](index.md) and [roadmap](roadmap.md).
