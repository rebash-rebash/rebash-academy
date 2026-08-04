---
title: "GitHub Fundamentals"
description: "Configure repository settings, Issues, Releases, and team workflows on GitHub for Cloud and DevOps delivery."
difficulty: beginner
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 9 · GitHub Fundamentals"
learning_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - devsecops-engineer
skills:
  - github
  - issues
  - releases
prerequisites:
  - git/working-with-remotes
next:
  - git/pull-requests-and-code-review
related:
  - git/repository-management-and-releases
  - git/signed-commits-and-git-security
tags:
  - github
  - issues
  - releases
  - repository-settings
author: Shaik Basha
last_updated: "2026-08-03"
comments: false
---

# GitHub Fundamentals

## Overview

GitHub extends Git with collaboration features: **Issues** for work tracking, **Releases** for semver artefacts, **Discussions** for design threads, and **repository settings** that enforce visibility, merge methods, and security defaults. DevOps teams treat the GitHub repository as the system of record alongside the Git object database.

This is **Tutorial 1** in **Module 9: GitHub Fundamentals** of the REBASH Academy **Git & GitHub for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers. The lab works locally with optional `gh` CLI if you have a GitHub account.

## Prerequisites

- [Working with Remotes](working-with-remotes.md)
- GitHub account (optional for lab — local checklist artefact)
- [GitHub CLI (`gh`)](https://cli.github.com/) optional

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Navigate repository settings that affect DevOps (visibility, default branch, merge options)
- [ ] Structure Issues for infrastructure and pipeline work
- [ ] Create semver tags and draft release notes locally
- [ ] Produce a repository onboarding settings YAML validated by script
- [ ] Store evidence under `~/rebash-git/module-09`

## Architecture

Developers push to GitHub; Issues link to commits and PRs; Releases attach binaries or manifests to tags; settings enforce org policy.

![Repository architecture](../assets/excalidraw/git-repository-architecture.svg)

## Theory

### What it is

**GitHub** hosts Git remotes with a web UI and API. A **repository** has settings (branch defaults, merge button options, Actions permissions). **Issues** are ticket objects referencing labels, milestones, and assignees. **Releases** bundle a Git tag with notes and optional assets (Helm charts, Terraform modules, binaries).

### Why it matters

Change management ties incident tickets to GitHub Issues. Releases trigger CD when tags match `v*`. Misconfigured settings — allow force-push to `main`, missing secret scanning — cause production incidents. Platform engineers onboard repos with a standard checklist.

### How it works

1. Create repo (empty or import); set default branch `main`.
2. Enable Issues; define labels (`type:infra`, `priority:high`).
3. Protect `main` (detailed in PR tutorial).
4. Tag releases: `git tag v1.0.0 && git push origin v1.0.0`; publish Release on UI or `gh release create`.
5. Use README, SECURITY.md, and template Issue forms for consistency.

### Key concepts and comparisons

| Feature | DevOps use |
|---------|------------|
| Issues | Track infra debt, incidents |
| Releases | Ship versioned modules/charts |
| Wiki | Legacy; prefer docs in repo |
| Discussions | RFCs, design Q&A |
| Settings | Merge strategy, Actions |

| Setting | Recommendation |
|---------|----------------|
| Default branch | main |
| Allow squash merge | Often yes for linear history |
| Allow rebase merge | Team preference |
| Allow merge commit | Optional for audit |
| Visibility | Private for internal IaC |

### Common pitfalls

- Public repo with Actions secrets reachable from forks — use environments and approval gates.
- Releases without tags — CD cannot pin versions.
- Issues without labels — backlog becomes unsearchable.
- Skipping SECURITY.md and private vulnerability reporting setup.

## Hands-on Lab

### Objective

Build a local "forge readiness" repo with Issue templates, `repo-settings.yaml` validated by script, and tag-based release notes as `.txt` — simulating GitHub onboarding without requiring push access.

### Prerequisites

- Git 2.x
- Optional: `gh auth login`

### Lab environment

Workspace: `~/rebash-git/module-09`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-git/module-09 && cd ~/rebash-git/module-09
set -euo pipefail
```

### Real-world scenario

Platform team onboards a new Terraform module repository to GitHub next sprint. You prepare repo settings YAML, sample Issue, and release notes artefact locally for review.

### Step-by-step tasks

#### Task 1 – Repo skeleton and Issue template

Create `.github/ISSUE_TEMPLATE/infra-change.md`:

```markdown title="infra-change.md"
---
name: Infrastructure change
about: Request a Terraform or pipeline change
labels: type:infra
---
## Change summary

## Environment

## Rollback plan
```

Create `README.md`:

```markdown title="README.md"
# module-vpc

Terraform VPC module — GitHub onboarding pending.
```

Initialise the repo:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-09
set -euo pipefail
rm -rf github-lab
mkdir -p github-lab/.github/ISSUE_TEMPLATE
cd github-lab
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
git add .
git commit -m 'chore: initial GitHub-ready skeleton'
test -f .github/ISSUE_TEMPLATE/infra-change.md
cd ..
```

!!! example "Expected output"
    Issue template committed in standard `.github` path.


#### Task 2 – Repo settings YAML and validation script

Create `repo-settings.yaml`:

```yaml title="repo-settings.yaml"
default_branch: main
branch_protection:
  main:
    require_pull_request: true
    required_reviews: 1
    require_codeowners: true
    required_checks:
      - terraform-validate
    block_force_push: true
security:
  secret_scanning: true
  dependabot_alerts: true
merge:
  allow_squash: true
  delete_head_branch: true
visibility: private
```

Create `validate-settings.sh`:

```bash title="validate-settings.sh"
#!/usr/bin/env bash
set -euo pipefail
grep -q 'default_branch: main' repo-settings.yaml
grep -q 'secret_scanning: true' repo-settings.yaml
grep -q 'block_force_push: true' repo-settings.yaml
echo 'settings_ok'
```

Validate and commit:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-09/github-lab
set -euo pipefail
chmod +x validate-settings.sh
./validate-settings.sh | tee ../settings-validate.txt
grep -q 'settings_ok' ../settings-validate.txt
git add repo-settings.yaml validate-settings.sh
git commit -m 'chore: add repo settings YAML and validator'
cd ..
```

!!! example "Expected output"
    Machine-readable settings YAML passes validation script.


#### Task 3 – Tag and release notes (local release simulation)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-git/module-09/github-lab
set -euo pipefail
git tag -a v0.1.0 -m 'Initial lab release — Issue template and repo settings YAML'
git tag -l 'v*' | tee ../tags.txt
grep -q 'v0.1.0' ../tags.txt
{
  echo '# v0.1.0 release notes'
  echo
  echo '## Added'
  echo '- Issue template for infrastructure changes'
  echo '- repo-settings.yaml with validation script'
  echo
  echo '## Commits since init'
  git log --oneline
} > release-notes-v0.1.0.txt
grep -q 'repo-settings.yaml' release-notes-v0.1.0.txt
git add release-notes-v0.1.0.txt
git commit -m 'chore: release notes for v0.1.0'
# Optional if gh authenticated:
# gh release create v0.1.0 --notes-file release-notes-v0.1.0.txt
tar -czf ../module-09-github-evidence.tgz -C .. tags.txt settings-validate.txt release-notes-v0.1.0.txt
ls -l ../module-09-github-evidence.tgz | tee ../github-evidence.txt
cd ..
```

!!! example "Expected output"
    Annotated tag v0.1.0; `release-notes-v0.1.0.txt` generated from log.


### Validation steps

- [ ] Issue template under `.github/ISSUE_TEMPLATE/`
- [ ] `repo-settings.yaml` passes `validate-settings.sh`
- [ ] Tag v0.1.0 exists locally
- [ ] `release-notes-v0.1.0.txt` present

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| gh not found | CLI not installed | Skip optional step; use UI later |
| tag exists | Re-run lab | `git tag -d v0.1.0` |
| template not shown on GitHub | Not pushed | Push when remote available |
| wrong default branch | Old habit | Rename to main on forge |

### Challenge exercise

If you have GitHub access: create a private sandbox repo, push this lab, open one Issue from the template, and run `validate-settings.sh` after verifying three settings in the UI — export screenshot paths list to `ONBOARDING_PROOF.txt` (paths only, no secrets).

### Learning outcomes

- Prepared standard GitHub repo layout
- Authored machine-readable repo settings with validation
- Created tag and release notes workflow locally

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
ls ~/rebash-git/module-09/github-lab
```

## Validation

- [ ] Lab under module-09
- [ ] Can list five critical repo settings
- [ ] Can explain Issue vs Discussion
- [ ] Know tag vs Release relationship

## Code Walkthrough

1. **Checklist per new repo** — automate with org templates where available.
2. **Labels early** — `type:`, `team:`, `priority:` conventions.
3. **Tag from CI** — semver only after checks pass.
4. **README badges** — CI status, latest release (when public).
5. **gh for automation** — script release creation in pipeline.

## Security Considerations

- Enable secret scanning and push protection on org repos.
- Restrict Actions permissions to least privilege.
- Private repos for IaC with cloud credentials context.
- Use GitHub environments for production deployment secrets.
- Rotate PATs; prefer fine-grained tokens with repo scope.

## Common Mistakes

!!! warning "Public fork of internal module"
    Exposes architecture details. **Fix:** Private repos; internal org only.

!!! warning "Releases without changelog"
    Operators cannot assess upgrade risk. **Fix:** release notes per semver tag (`.txt` or GitHub Release body).

!!! warning "Issues disabled"
    Work happens in Slack without traceability. **Fix:** Enable Issues; link PRs.

## Best Practices

- Org-level repository templates with checklist included
- Standard labels across platform repos
- Signed tags for production modules
- Link Issues to PRs with "Fixes #123"
- Archive repos instead of deleting for audit

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Cannot push | Auth or branch protection | Check token/SSH; use PR |
| Release missing tag | Tag not pushed | git push origin v1.0.0 |
| Template not in UI | Wrong path | .github/ISSUE_TEMPLATE/ |
| gh 403 | Token scope | Regenerate with repo scope |

## Summary

GitHub adds Issues, Releases, and settings governance on top of Git — prepare repos with templates and checklists before first push. Next: [Pull Requests and Code Review](pull-requests-and-code-review.md).

## Interview Questions

**1. Difference between Git tag and GitHub Release?**

??? success "Reveal answer"
    Tag is a Git ref pointing to a commit; GitHub Release is forge metadata wrapping a tag with title, notes, and downloadable assets — often triggers CD webhooks.

**2. Why default branch main?**

??? success "Reveal answer"
    Aligns with industry default, branch protection templates, and tooling expectations — reduces friction for CI and new contributors.

**3. Three repo settings for DevSecOps?**

??? success "Reveal answer"
    Secret scanning, Dependabot alerts, branch protection requiring reviews and status checks — baseline before trusting repo with deploy keys.

**4. When use Issues vs Discussions?**

??? success "Reveal answer"
    Issues track actionable work with assignees and milestones; Discussions suit open-ended design questions without a single deliverable.

**5. gh release create purpose?**

??? success "Reveal answer"
    Automates Release publication from CLI/CI — attaches notes, assets, and makes version visible to consumers and deployment pipelines.

**6. Why delete head branch after merge?**

??? success "Reveal answer"
    Reduces stale branch clutter and mistaken pushes to old feature branches — GitHub setting automates cleanup after PR merge.

**7. Merge options on GitHub — why restrict?**

??? success "Reveal answer"
    Team may mandate squash-only for linear main history or forbid merge commits — consistency beats per-PR ad hoc choice.

**8. Repository visibility impact on Actions?**

??? success "Reveal answer"
    Public repos may run untrusted fork PR workflows — require approval for first-time contributors and limit secrets in fork contexts.

## Related Tutorials

- [Working with Remotes](working-with-remotes.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Repository Management and Releases](repository-management-and-releases.md)
- [Course index](index.md)

## References

- [GitHub Docs — Repositories](https://docs.github.com/en/repositories)
- [About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [GitHub CLI manual](https://cli.github.com/manual/)
