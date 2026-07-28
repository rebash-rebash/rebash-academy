---
title: Pull Requests and Code Review
description: Open pull requests, request reviews, address feedback, merge strategies, protected branches, and code review best practices for DevOps teams.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - pull-request
  - code-review
  - collaboration
prerequisites:
  - Working with Remotes
  - Merging and Merge Conflicts
comments: false
---

# Pull Requests and Code Review

## Overview

Pull requests (PRs) — merge requests on GitLab — are the collaboration hub where code meets review, CI runs, and changes merge to protected branches. For DevOps teams managing Terraform, Kubernetes YAML, and pipeline configs, PRs enforce four-eyes principles and audit trails required by compliance frameworks.

This is **Tutorial 11** in **Module 4: Collaboration** of the REBASH Academy Git series.

## Prerequisites

- [Working with Remotes](working-with-remotes.md)
- [Merging and Merge Conflicts](merging-and-merge-conflicts.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Open and describe effective pull requests
- [ ] Request reviews and respond to feedback constructively
- [ ] Interpret CI status checks on PRs
- [ ] Choose merge strategies (merge, squash, rebase)
- [ ] Configure and work within protected branch rules
- [ ] Review IaC changes with security and blast-radius mindset
- [ ] Link PRs to tickets and deployment traceability

## PR Lifecycle Diagram

```d2
direction: right

BR: "Feature Branch"
    PR: "Open Pull Request"
    BR -> PR: push
    CI: "CI Checks Run"
    PR -> CI
    REV: "Code Review"
    CI -> REV
    MERGE: "Merge to main"
    REV -> MERGE: approve
    REV -> BR: "changes requested"
    DEPLOY: "CD / GitOps Deploy"
    MERGE -> DEPLOY
```

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### What Is a Pull Request?

A PR is a **request to merge** one branch into another, with:

- Diff of all changes
- Description and linked issues
- Review comments on specific lines
- CI/CD status checks
- Merge button (when requirements met)

PRs are platform features (GitHub/GitLab) — not native Git commands — but they drive Git operations under the hood.

### Opening a Strong PR

**Title:** Conventional commit style — `feat(iam): add S3 bucket policy for logging`

**Description template:**

```markdown
## Summary
- Add CloudWatch log bucket with encryption
- Update IAM role for Lambda write access

## Test plan
- [ ] terraform plan shows expected resources
- [ ] validate in dev account
- [ ] security scan passed

## Ticket
JIRA-4521
```

Small PRs (< 400 lines changed) merge faster and review better.

### Review Roles

| Role | Responsibility |
|------|----------------|
| **Author** | Clear description; respond to feedback; keep CI green |
| **Reviewer** | Check correctness, security, tests; approve or request changes |
| **CODEOWNERS** | Auto-assigned reviewers for path ownership |

### CODEOWNERS Example

```text
# .github/CODEOWNERS
*.tf          @platform-team
/k8s/         @sre-team
/.github/     @devops-team
```

Platform auto-requests reviewers when PR touches owned paths.

### CI on Pull Requests

Typical checks:

- Lint (terraform fmt, yamllint)
- Unit/integration tests
- `terraform plan` (posted as comment)
- Security scan (Checkov, tfsec)
- Required status checks before merge

Failed CI blocks merge on protected branches.

### Merge Strategies on Platform

| Strategy | Result |
|----------|--------|
| **Create merge commit** | Preserves branch; adds merge commit |
| **Squash and merge** | One commit on main |
| **Rebase and merge** | Linear history; replays commits |

Team policy should document chosen strategy. Many DevOps repos prefer squash or rebase for clean main.

### Protected Branches

Rules commonly enforced:

- Require PR before merge (no direct push)
- Require N approvals
- Require CI pass
- Require signed commits
- Restrict force push
- Require linear history

Applies to `main`, `production`, release branches.

### Reviewing IaC and DevOps Changes

Checklist for Terraform/K8s PRs:

- **Blast radius** — what breaks if wrong?
- **Secrets** — no plaintext credentials
- **Idempotency** — plan shows only intended changes
- **Rollback** — can we revert?
- **Environment scope** — dev vs prod paths correct?
- **Cost impact** — new resources priced?

### Draft PRs

Mark WIP PRs as **Draft** — signals reviewers to wait. Convert to ready when CI green and self-review done.

### Review Etiquette

- Comment on code, not people
- Suggest alternatives (`nit:`, `blocking:` prefixes help)
- Authors: don't take feedback personally; batch fixes in commits
- Resolve conversations when addressed

### Platform-Specific Notes

| Platform | PR name | Unique features |
|----------|---------|-----------------|
| **GitHub** | Pull Request | CODEOWNERS, merge queue, auto-merge, Copilot review |
| **GitLab** | Merge Request | Approval rules, security scanning, "merge when pipeline succeeds" |
| **Bitbucket** | Pull Request | Jira smart commits, default reviewers |
| **Azure DevOps** | Pull Request | Work item linking, branch policies |

Regardless of platform, the Git operations underneath — push branch, diff against base, merge — are identical. Skills from this tutorial transfer when your organization changes hosting providers.

### Required Status Checks

Configure required checks that must pass before merge:

- `terraform-plan` — no destructive changes without approval
- `unit-tests` — application logic verified
- `secret-scan` — gitleaks or platform native scanner
- `lint` — formatting and static analysis

Failed required checks display a blocked merge button. Optional checks show warnings but allow merge — use sparingly to avoid alert fatigue.

## Hands-on Lab

### Step 1 – Prepare feature branch (local simulation)

**Command:**

```bash
mkdir -p /tmp/git-pr-lab && cd /tmp/git-pr-lab
git init -b main
echo "# App" > README.md && git add . && git commit -m "docs: initial README"
git init --bare /tmp/pr-remote.git
git remote add origin /tmp/pr-remote.git
git push -u origin main
git switch -c feature/add-healthcheck
cat > healthcheck.sh << 'EOF'
#!/usr/bin/env bash
curl -sf http://localhost:8080/health || exit 1
EOF
chmod +x healthcheck.sh
git add healthcheck.sh && git commit -m "feat: add healthcheck script"
```

### Step 2 – Push feature branch

**Command:**

```bash
git push -u origin feature/add-healthcheck
git log main..feature/add-healthcheck --oneline
git diff main...feature/add-healthcheck --stat
```

**Explanation:** Three-dot diff shows PR diff scope — what reviewers see.

### Step 3 – Simulate review feedback

**Command:**

```bash
# Reviewer suggests timeout flag
git commit --amend -m "feat: add healthcheck script with curl timeout"
sed -i.bak 's/curl -sf/curl -sf --max-time 5/' healthcheck.sh 2>/dev/null || \
  sed -i 's/curl -sf/curl -sf --max-time 5/' healthcheck.sh
git add healthcheck.sh && git commit --amend --no-edit
git push --force-with-lease origin feature/add-healthcheck
```

### Step 4 – Merge (simulating platform merge)

**Command:**

```bash
git switch main
git pull origin main
git merge --no-ff feature/add-healthcheck -m "Merge pull request #1: add healthcheck"
git push origin main
git log --oneline --graph -5
```

### Step 5 – Clean up

**Command:**

```bash
rm -rf /tmp/git-pr-lab /tmp/pr-remote.git
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `git push -u origin branch` | Publish branch for PR | First push of feature branch |
| `git diff main...feature` | PR-scope diff | Review before opening |
| `git log main..feature` | Commits in PR | PR description helper |
| `git push --force-with-lease` | Update PR after amend/rebase | After review fixes |
| `gh pr create` | Open PR (GitHub CLI) | `gh pr create --fill` |
| `gh pr checkout 123` | Checkout PR locally | Review locally |

### PR description generator

```bash
#!/usr/bin/env bash
# pr-summary.sh — generate PR summary from commits
set -euo pipefail
BASE="${1:-main}"
git log "$BASE"..HEAD --oneline
echo ""
git diff "$BASE"...HEAD --stat
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Huge PRs with unrelated changes"
    Split infra module refactor from one-line fix. Reviewers miss critical issues in 2000-line diffs.

!!! warning "Merging with failing CI"
    Bypassing checks defeats purpose of protected branches. Fix or waive with documented exception.

!!! warning "Self-approval on sensitive changes"
    SOC 2 requires independent review — configure branch rules to block author approval.

!!! warning "No test plan in IaC PRs"
    Always include expected `terraform plan` output or `kubectl diff` summary.

## Best Practices

!!! tip "Link every PR to a ticket"
    Audit trail from incident → deploy → commit → ticket.

!!! tip "Use draft PRs for early feedback"
    Architecture direction before full implementation saves rework.

!!! tip "Automate plan output in PR comments"
    Terraform Cloud, Atlantis, and similar tools post plan diffs automatically.

!!! tip "Set review SLA"
    Platform teams target 24h review turnaround — unblocks delivery.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Cannot merge — checks pending | CI still running | Wait or re-run failed jobs |
| Merge conflicts on PR | Main advanced | Rebase/merge main into feature branch |
| Reviewer not assigned | CODEOWNERS missing/wrong | Fix CODEOWNERS path |
| Force push rejected | Branch protection | Push new commits instead of amend |
| Stale PR | Long-lived branch | Rebase onto main; resolve conflicts |
| Wrong base branch | PR targets release not main | Change base on platform |

## Summary

- **Pull requests** integrate review, CI, and merge into one workflow
- Strong PRs have clear titles, summaries, test plans, and small diffs
- **Protected branches** enforce approvals, CI, and no direct pushes
- **Merge strategies** (merge commit, squash, rebase) affect main history — document team policy
- IaC review focuses on blast radius, secrets, plan output, and rollback path

## Interview Questions

1. What is a pull request, and how does it differ from `git merge`?
2. What should a good PR description include for a Terraform change?
3. What are protected branch rules, and why use them?
4. Compare squash merge vs merge commit for main branch.
5. What is CODEOWNERS, and how does it work?
6. How do CI status checks integrate with pull requests?
7. What is a three-dot diff, and why is it used in PRs?
8. When should you use draft pull requests?
9. How do you update a PR after rebase or amend?
10. What should reviewers look for in Kubernetes manifest PRs?

??? tip "Sample Answers (Questions 1 and 4)"

    **Q1 — PR vs git merge:** A pull request is a platform workflow wrapping Git operations — it displays diffs, collects reviews, runs CI, and provides a merge button. `git merge` is the underlying Git command that integrates branches. PR adds governance layer required for team and compliance workflows.

    **Q4 — Squash vs merge commit:** Merge commit preserves full feature branch history and adds explicit merge node — good for tracing branch work. Squash combines all feature commits into one on main — cleaner log, easier revert of entire feature, but loses granular commit history on main.

## Related Tutorials

- [Working with Remotes](working-with-remotes.md) *(previous)*
- [gitignore and gitattributes](gitignore-and-gitattributes.md) *(next)*
- [Advanced Git Workflows](advanced-git-workflows.md)
- [Git in CI/CD and DevOps](git-in-ci-cd-and-devops.md)
- [Signed Commits and Git Security](signed-commits-and-git-security.md)

## References

- [GitHub – About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
- [GitLab – Merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
- [Google Engineering Practices – Code Review](https://google.github.io/eng-practices/review/)
- [GitHub – CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [REBASH Academy – Git Overview](index.md)
