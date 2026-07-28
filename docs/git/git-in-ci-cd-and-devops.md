---
title: Git in CI/CD and DevOps
description: Integrate Git with CI/CD pipelines, GitOps, webhooks, deployment strategies, and the complete DevOps toolchain from commit to production.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
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

## DevOps Git Pipeline Diagram

```mermaid
flowchart TB
    DEV["Developer Push / PR"]
    GIT["Git Repository"]
    WH["Webhook / Event"]
    CI["CI Pipeline<br/>build · test · scan"]
    ART["Artifact Registry<br/>image · plan"]
    CD["CD / GitOps<br/>Argo CD · Flux"]
    PROD[Production]

    DEV --> GIT
    GIT --> WH --> CI
    CI --> ART
    GIT --> CD
    CD --> PROD
    ART --> PROD```

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

### Step 1 – Simulate CI checkout

**Command:**

```bash
mkdir -p /tmp/git-cicd-lab && cd /tmp/git-cicd-lab
git init -b main
echo "app_version=1.0" > app.env
git add . && git commit -m "feat: initial release"
git init --bare /tmp/cicd-remote.git
git remote add origin /tmp/cicd-remote.git
git push -u origin main
SHA=$(git rev-parse HEAD)
echo "Deploy identity: myapp@$SHA"
```

### Step 2 – Tag production release

**Command:**

```bash
git tag -a v1.0.0 -m "Production release 1.0.0"
git push origin v1.0.0
git show v1.0.0 --no-patch --format="Tag %D points to %H"
```

### Step 3 – Simulate PR merge workflow

**Command:**

```bash
git switch -c feature/ci-demo
echo "app_version=1.1" > app.env
git commit -am "feat: bump version for CI demo"
git push -u origin feature/ci-demo
git switch main
git merge --no-ff feature/ci-demo -m "Merge PR #42: CI demo"
git push origin main
git log --oneline --graph -5
```

### Step 4 – Simulate GitOps manifest update

**Command:**

```bash
mkdir -p k8s/overlays/prod
cat > k8s/overlays/prod/kustomization.yaml << EOF
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
images:
  - name: myapp
    newTag: ${SHA:0:7}
EOF
echo "apiVersion: apps/v1" > k8s/overlays/prod/deployment.yaml
git add k8s/ && git commit -m "deploy: pin image to ${SHA:0:7}"
git log -1 --format="GitOps commit %h — image tag %s"
```

### Step 5 – Pipeline preflight script

**Command:**

```bash
cat > ci-preflight.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "Commit: $(git rev-parse HEAD)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD)"
echo "Signed: $(git log -1 --format='%G?')"
test -f app.env && echo "Config: $(cat app.env)"
EOF
chmod +x ci-preflight.sh
./ci-preflight.sh
```

### Step 6 – Clean up

**Command:**

```bash
cd /tmp && rm -rf git-cicd-lab cicd-remote.git
```

## Commands & Code

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

1. How do Git push events trigger CI pipelines?
2. What is GitOps, and how does it differ from traditional CI/CD push deploy?
3. Why pin deployments to commit SHA rather than branch name?
4. What Git events should trigger terraform plan vs apply?
5. Describe the app repo → GitOps repo → cluster flow.
6. What belongs in Git vs artifact registry vs state backend?
7. How do you roll back a GitOps deployment?
8. What security controls should protect the production Git branch?
9. How do signed tags integrate with release pipelines?
10. What is the complete Git hygiene checklist for a DevOps team?

??? tip "Sample Answers (Questions 2 and 5)"

    **Q2 — GitOps vs push CD:** Traditional CD pushes changes from CI runner to infrastructure (kubectl apply, terraform apply from pipeline). GitOps installs an operator in the cluster that continuously pulls desired state from Git and reconciles. CI updates Git; cluster pulls — reducing CI credentials exposure and enabling drift detection.

    **Q5 — App to cluster flow:** Developer merges to app repo main. CI builds container image tagged with commit SHA, pushes to registry. CI (or bot) commits updated image tag to GitOps repo manifest. Argo CD/Flux detects Git change, pulls manifest, deploys new image to cluster. Full traceability: prod pod → GitOps commit → app SHA → PR → author.

## Related Tutorials

- [Signed Commits and Git Security](signed-commits-and-git-security.md) *(previous)*
- [Git Hooks and Automation](git-hooks-and-automation.md)
- [Advanced Git Workflows](advanced-git-workflows.md)
- [Pull Requests and Code Review](pull-requests-and-code-review.md)
- [Git – Category Overview](index.md) — track complete
- [GitLab CI/CD Overview](../gitlab/index.md)
- [Terraform Overview](../terraform/index.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

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
