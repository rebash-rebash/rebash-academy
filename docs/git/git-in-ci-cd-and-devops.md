---
title: Git in CI/CD and DevOps
description: Integrate Git with CI/CD pipelines, GitOps, webhooks, deployment strategies, and the complete DevOps toolchain from commit to production.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - cicd
  - devops
  - gitops
prerequisites:
  - Signed Commits and Git Security
  - Git Hooks and Automation
  - Working with Remotes
  - Pull Requests and Code Review
comments: false
---


# Git in CI/CD and DevOps

## Overview






Git is the trigger, transport, and source of truth for modern DevOps delivery. Every push fires webhooks; every merge runs pipelines; every tag deploys to production. GitOps operators reconcile Kubernetes clusters against Git branches. This finale tutorial connects everything you've learned — workflow, hooks, signing, remotes — to the CI/CD and GitOps patterns used in production.

This is **Tutorial 20** in **Module 6: Advanced & DevOps** — the finale of the REBASH Academy Git series.

## Prerequisites






- [Signed Commits and Git Security](signed-commits-and-git-security.md)
- [Git Hooks and Automation](git-hooks-and-automation.md)
- [Working with Remotes](working-with-remotes.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)

## Learning Objectives






By the end of this tutorial, you will be able to:

- [ ] Explain how Git events trigger CI/CD pipelines
- [ ] Configure pipeline triggers for push, PR, and tag events
- [ ] Implement GitOps with pull-based deployment models
- [ ] Pin deployments to commit SHAs and signed tags
- [ ] Design repository layout for IaC and application delivery
- [ ] Integrate Git with Terraform Cloud, GitHub Actions, and GitLab CI
- [ ] Apply complete Git hygiene across the DevOps lifecycle

## Architecture






CI/CD watches remotes for new commits, runs automated verification, and deploys only when policy checks pass.

![GitHub Actions](../assets/excalidraw/git-github-actions.svg)

## Theory






### Git as the System of Record

In DevOps, Git stores:

| Asset | Example path |
|-------|--------------|
| Application source | `src/`, `cmd/` |
| Infrastructure | `terraform/`, `pulumi/` |
| Kubernetes manifests | `k8s/overlays/prod/` |
| CI definitions | `.github/workflows/`, `.gitlab-ci.yml` |
| Policies | `policy/`, OPA Rego |
| Runbooks | `docs/runbooks/` |

If it affects production, it belongs in Git — not wikis or chat.

### CI Trigger Events

| Event | Typical pipeline action |
|-------|-------------------------|
| **Push to feature branch** | Lint, unit tests |
| **Pull request opened/updated** | Full test + plan + security scan |
| **Merge to main** | Build artifact, deploy staging |
| **Tag v*.*.*** | Deploy production |
| **Schedule** | Drift detection, dependency updates |

Webhooks deliver events from Git host to CI within seconds.

### Pipeline Git Operations

CI runners commonly:

```bash
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" workspace
cd workspace
git rev-parse HEAD   # pin SHA in logs and artifacts
```

Advanced patterns:

- **Merge ref checkout** for PRs (`refs/pull/123/merge`)
- **Submodule init** for nested dependencies
- **LFS pull** for large assets
- **Sparse checkout** for monorepos

### Commit SHA as Deployment Identity

Immutable reference for traceability:

```text
myapp:1.4.2@sha-a1b2c3d4
```

Kubernetes deployment annotation:

```yaml
metadata:
  annotations:
    git.commit/sha: a1b2c3d4e5f6789...
    git.commit/message: "fix: patch CVE-2026-1234"
```

Rollback = redeploy previous SHA or revert commit in Git.

### GitOps — Pull-Based Deployment

**Push-based CD:** CI pipeline pushes/applies changes to cluster (kubectl apply from runner).

**GitOps (pull-based):** Operator in cluster watches Git; reconciles desired state:

| Tool | Watches | Action |
|------|---------|--------|
| **Argo CD** | Git repo + path + branch/tag | Sync K8s manifests |
| **Flux** | GitRepository CRD | Apply + helm |
| **Terraform Cloud** | VCS webhook | Plan/apply IaC |

Benefits:

- Cluster pulls changes — no CI cluster credentials
- Drift detection — live vs Git diff
- Audit trail in Git history
- Rollback via Git revert

Example Argo CD Application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service
spec:
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: main
    path: overlays/production/payment
  destination:
    server: https://kubernetes.default.svc
    namespace: payment
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Repository Layout Patterns

**Polyrepo:** App repo + separate infra repo — clear boundaries.

**Monorepo:** App + infra + CI in one repo — atomic changes, complex CI.

**Environment overlays (Kustomize):**

```text
k8s/
  base/
  overlays/
    dev/
    staging/
    production/
```

Git branch != environment; path or overlay selects environment.

### Terraform + Git Integration

Terraform Cloud/Enterprise:

- VCS-driven workflow connects GitHub/GitLab
- PR triggers speculative plan posted as comment
- Merge to main triggers apply (if approved)

Local alternative — CI runs:

```bash
terraform init
terraform plan -out=plan.tfplan
terraform apply plan.tfplan   # main branch only
```

State backends (S3 + DynamoDB) separate from Git — never commit state files.

### GitHub Actions Example

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Verify signed commits
        run: |
          git log --format='%G?' -1 | grep -q G || exit 1
      - name: Terraform plan
        run: |
          terraform init -backend=false
          terraform validate
          terraform plan -detailed-exitcode
```

### GitLab CI Example

```yaml
stages:
  - validate
  - plan
  - apply

terraform-plan:
  stage: plan
  script:
    - terraform init
    - terraform plan -out=plan.cache
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

terraform-apply:
  stage: apply
  script:
    - terraform apply -auto-approve plan.cache
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

### Security Integration Recap

Full stack from this track:

1. **Signed commits** — identity verification
2. **Branch protection** — no direct push to main
3. **PR review** — human gate
4. **Pre-commit hooks** — local lint/secrets
5. **CI scanning** — SAST, IaC policy, container scan
6. **GitOps** — cluster reconciles only from trusted repo/branch

### Multi-Repository Orchestration

Platform teams manage:

- **App repos** — microservices
- **GitOps repo** — Kustomize/Helm values updated by CI (image tag bump commit)
- **Terraform repo** — cloud foundation

CI in app repo commits SHA update to GitOps repo — classic pattern:

```bash
git clone git@github.com:org/gitops.git
cd gitops/apps/payment
kustomize edit set image payment=$IMAGE:$CI_COMMIT_SHA
git commit -am "deploy: payment $CI_COMMIT_SHA"
git push
```

Argo CD detects change and syncs.

### Observability and Git

Link deployments to commits in:

- **Datadog/Sentry release tracking** — version = Git SHA
- **Incident tools** — "what commit is prod?" query
- **Changelog automation** — conventional commits → release notes

## Hands-on Lab



### Objective

Complete a real Git workflow for **Git in CI/CD and DevOps** with commits you can inspect and recover.

### Prerequisites

- Git 2.x installed

### Lab environment

Workspace: `~/rebash-git/git-in-ci-cd-and-devops`

Local Git repository only (no required remote).

```bash
mkdir -p ~/rebash-git/git-in-ci-cd-and-devops && cd ~/rebash-git/git-in-ci-cd-and-devops
```

### Real-world scenario

A delivery team is standardising **Git in CI/CD and DevOps**. You prototype the workflow in a throwaway repo and capture log evidence for the playbook.

### Step-by-step tasks

#### Task 1 – Initialise a repository and first commit

Every production change starts as a commit with clear identity config.

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline | tee log.txt
```

**Expected output:** log.txt shows the initial commit on `main`.

#### Task 2 – Inspect status and diff discipline

Clean working trees prevent accidental commits of secrets.

```bash
echo 'work' > work.txt
git status
git add work.txt
git commit -m 'Add work.txt'
git show --stat HEAD | tee show.txt
```

**Expected output:** show.txt lists work.txt in the commit.

### Validation steps

- [ ] Repository has at least two commits or a merge as designed
- [ ] log/graph evidence files exist

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Author identity unknown | Missing user.name/email | Set local `git config user.*` as in Task 1 |
| merge conflict | Overlapping edits | Edit file, `git add`, complete merge |
| detached HEAD | Checked out a raw SHA | `git switch -c` a branch before committing |

### Challenge exercise

Use `git reflog` to recover a commit after a hard reset on a private branch.

### Learning outcomes

- Performed real Git operations
- Left auditable history
- Understood recovery basics

### Cleanup

```bash
# Safe local repo — delete the lab directory when finished:
# rm -rf "$(pwd)"
```

## Validation






Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Pipeline file | Workflow/CI config validates (or dry-runs) successfully |
| Trigger | Push/PR event path documented and understood |
| Secrets | No plaintext secrets remain in the committed workflow |
| Cleanup | Lab repo cleaned; tokens revoked if created |

## Code Walkthrough






| Command | Description | Example |
|---------|-------------|---------|
| `git rev-parse HEAD` | Deployment SHA | Pin in artifacts |
| `git clone --depth 1` | CI fast checkout | Ephemeral runners |
| `git describe --tags` | Nearest tag + distance | Version strings |
| `git log -1 --format='%B'` | Commit message | Changelog input |
| `git diff main...HEAD` | PR change set | Plan scope |
| `git archive` | Export snapshot | Release tarball |

### Complete DevOps Git checklist

```markdown

## Repository Setup





- [ ] main protected; PR required
- [ ] Signed commits enforced
- [ ] .gitignore for stack
- [ ] pre-commit hooks configured
- [ ] CODEOWNERS defined

## CI Pipeline





- [ ] Trigger on PR and main push
- [ ] Pin checkout to event SHA
- [ ] terraform plan / k8s validate
- [ ] Secret and IaC policy scan
- [ ] Post plan to PR comment

## CD / GitOps





- [ ] Deploy staging on main merge
- [ ] Deploy prod on signed tag
- [ ] GitOps operator watches prod path
- [ ] Rollback = revert or previous tag
- [ ] Deployment annotated with commit SHA
```

## Security Considerations






- Grant CI identities least privilege to cloud and forge APIs; prefer OIDC over static keys
- Mask secrets in pipeline logs and forbid echo-debugging of tokens
- Pin actions/images by digest; review third-party workflows before enabling them
- Separate build, staging, and production deployment roles
- Fail pipelines on secret scanning and signature verification errors

## Common Mistakes






!!! warning "CI always cloning main instead of event SHA"
    Tests wrong code on PR. Use `$GITHUB_SHA` or `$CI_COMMIT_SHA`.

!!! warning "Applying Terraform from developer laptops to prod"
    Prod applies from CI/CD with approval gates — not local `terraform apply`.

!!! warning "GitOps without branch protection"
    Anyone pushing to watched branch deploys to prod. Protect and review.

!!! warning "Mutable tags (latest) in production"
    Use immutable SHA or semver tags — not floating `latest`.

## Best Practices






!!! tip "Treat main as always deployable"
    Feature flags hide incomplete work; CI keeps main green.

!!! tip "Separate plan and apply jobs"
    Plan on PR; apply on main merge with manual approval for prod.

!!! tip "Record commit SHA in every artifact"
    Docker labels, Helm chart annotations, Terraform outputs.

!!! tip "Practice rollback drills"
    Revert commit in Git; verify GitOps syncs; document RTO.

## Troubleshooting






| Issue | Cause | Solution |
|-------|-------|----------|
| Pipeline not triggering | Webhook misconfigured | Verify repo settings; redeliver webhook |
| Wrong code deployed | Tag moved or wrong ref | Immutable tags; verify SHA |
| GitOps out of sync | Manual kubectl edit | selfHeal; disable manual changes |
| Submodule CI failure | Not initialized | checkout submodules: true |
| Plan differs CI vs local | Different vars/backend | Align env; remote backend |
| Deploy before CI pass | Missing branch protection | Require status checks |

## Summary






- **Git events** (push, PR, tag) trigger **CI/CD pipelines** via webhooks
- **Commit SHA** and **signed tags** provide immutable deployment identity
- **GitOps** pulls desired state from Git — Argo CD and Flux reconcile clusters
- Separate **plan (PR)** from **apply (main/tag)** for IaC safety
- Complete Git track skills — workflow, hooks, signing, remotes — integrate here
- Git is step 3 in the DevOps learning path; apply it with [GitLab CI/CD](../gitlab/index.md), [Terraform](../terraform/index.md), and platform tooling

## Interview Questions




1. Which git metadata should CI inject into artifacts?
2. Why prefer commit SHA tags over latest?
3. How do annotated tags support releases?
4. What breaks if CI checks out a shallow clone?
5. How do you trace a production binary back to git?

!!! tip "Sample answer — question 2"
    Print git rev-parse HEAD / git describe in the failing job and confirm checkout depth.

!!! tip "Sample answer — question 4"
    Sign releases when needed and keep provenance (SHA, pipeline ID).

## Related Tutorials






- [Signed Commits and Git Security](signed-commits-and-git-security.md) *(previous)*
- [Git Hooks and Automation](git-hooks-and-automation.md)
- [Advanced Git Workflows](advanced-git-workflows.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Git – Category Overview](index.md) — track complete
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Terraform Overview](../terraform/index.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Git Cheat Sheet](../cheatsheets/git.md)
- Interview prep: [Git Interview Prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References






- [CNCF GitOps Working Group](https://opengitops.dev/)
- [Argo CD Documentation](https://argo-cd.readthedocs.io/)
- [Flux Documentation](https://fluxcd.io/flux/)
- [GitHub Actions – Events that trigger workflows](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)
- [Terraform Cloud VCS-driven workflow](https://developer.hashicorp.com/terraform/cloud-docs/run/ui)
- [DORA Metrics and version control](https://dora.dev/)
- [Pro Git Book – entire book](https://git-scm.com/book/en/v2)
- [REBASH Academy – Git Overview](index.md)

## Congratulations






You have completed all **20 tutorials** in the REBASH Academy Git track — from version control fundamentals through CI/CD and GitOps integration. Return to the [Git Overview](index.md) to review the curriculum or continue to [GitLab CI/CD](../gitlab/index.md) and [Terraform](../terraform/index.md) in the DevOps learning path.
