---
title: Git Submodules and Subtrees
description: Embed external repositories with submodules and subtrees; manage dependencies for Terraform modules, shared configs, and monorepo patterns.
difficulty: advanced
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: git
tags:
  - git
  - submodules
  - subtrees
  - monorepo
prerequisites:
  - Advanced Git Workflows
  - Working with Remotes
comments: false
---


# Git Submodules and Subtrees

## Overview




Platform teams reuse Terraform modules, Helm charts, and shared libraries across repositories. **Submodules** pin exact commits of nested repos; **subtrees** merge external history into a subdirectory. Both solve dependency management — with different tradeoffs in complexity, clone experience, and update workflows.

This is **Tutorial 18** in **Module 6: Advanced & DevOps** of the REBASH Academy Git series.



## Prerequisites




- [Advanced Git Workflows](advanced-git-workflows.md)
- [Working with Remotes](working-with-remotes.md)
- Understanding of commit SHAs and remotes



## Learning Objectives




By the end of this tutorial, you will be able to:

- [ ] Add, update, and clone repositories with submodules
- [ ] Understand `.gitmodules` configuration
- [ ] Compare submodules vs subtrees vs package registries
- [ ] Add and update subtrees with `git subtree`
- [ ] Diagnose common submodule clone and CI failures
- [ ] Choose embedding strategy for shared Terraform modules
- [ ] Remove submodules cleanly



## Architecture




Submodules pin an external repository at a commit; subtrees vendor history into a subdirectory of the parent project.

![Repository architecture](../assets/excalidraw/git-repository-architecture.svg)



## Theory




### Why Embed Repositories?

| Approach | When |
|----------|------|
| **Copy-paste** | Quick, no linkage — drift guaranteed |
| **Package registry** | Terraform Registry, npm, Helm repo — preferred for versioned artifacts |
| **Submodule** | Pin exact source commit; child repo independent |
| **Subtree** | Single clone; external history merged in subdirectory |
| **Monorepo** | Everything in one repo — Bazel/Nx tooling |

Submodules/subtrees fit when source must stay in Git but separate lifecycle.

### Git Submodules

Parent repo stores a **gitlink** — special entry recording submodule path and commit SHA. Configuration in `.gitmodules`:

```ini
[submodule "modules/vpc"]
    path = modules/vpc
    url = git@github.com:org/terraform-vpc.git
    branch = main
```

Add submodule:

```bash
git submodule add git@github.com:org/terraform-vpc.git modules/vpc
git commit -m "chore: add vpc module submodule"
```

Clone with submodules:

```bash
git clone --recurse-submodules URL
# or after clone:
git submodule update --init --recursive
```

Update to latest remote commit:

```bash
cd modules/vpc
git fetch && git checkout origin/main
cd ../..
git add modules/vpc
git commit -m "chore: bump vpc module"
```

Or:

```bash
git submodule update --remote modules/vpc
```

### Submodule Characteristics

**Pros:**

- Exact commit pinning — reproducible builds
- Child repo independent history
- Clear ownership boundary

**Cons:**

- Clone requires extra steps (`--recurse-submodules`)
- Easy to commit parent pointing to wrong SHA
- CI must initialize submodules
- Detached HEAD in submodule confuses developers
- Recursive submodule complexity

### Git Subtrees

Merge external repo into subdirectory — history optionally preserved:

```bash
git subtree add --prefix=modules/vpc \
  git@github.com:org/terraform-vpc.git main --squash
```

Update:

```bash
git subtree pull --prefix=modules/vpc \
  git@github.com:org/terraform-vpc.git main --squash
```

Push changes back upstream (if permitted):

```bash
git subtree push --prefix=modules/vpc \
  git@github.com:org/terraform-vpc.git main
```

**Pros:**

- Single clone — no extra init step
- Works transparently for most developers
- No detached HEAD in subdirectory

**Cons:**

- History can bloat (without --squash)
- Push back to upstream is complex
- Less obvious which external version is pinned

### Submodules vs Subtrees Decision

| Criterion | Submodule | Subtree |
|-----------|-----------|---------|
| Clone simplicity | Poor | Good |
| Pin exact version | Explicit SHA | Merge commit |
| CI complexity | Higher | Lower |
| Upstream contribution | Easy in submodule | Harder push |
| Team familiarity | Lower | Higher |

**Terraform modules:** Prefer **Terraform Registry** or **module source with ref** over submodules when possible. Use submodules when internal modules aren't published.

### CI/CD with Submodules

```yaml
# GitHub Actions example
steps:
  - uses: actions/checkout@v4
    with:
      submodules: recursive
      token: ${{ '{{' }} secrets.PAT_WITH_SUBMODULE_ACCESS {{ '}}' }}
```

PAT or deploy key needs read access to all submodule URLs.

### Removing a Submodule

```bash
git submodule deinit -f modules/vpc
git rm -f modules/vpc
rm -rf .git/modules/modules/vpc
# Remove entry from .gitmodules and commit
```

Manual cleanup required — submodules leave artifacts if removed incorrectly.

### Alternatives in DevOps

- **Terraform module sources** with version constraints
- **Helm chart dependencies** in Chart.yaml
- **Go modules**, **npm workspaces**
- **Monorepo** with shared packages

Submodules are often a last resort when registry isn't available.



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/git-submodules-and-subtrees && cd ~/rebash-git/git-submodules-and-subtrees
```

**Focus:** add a submodule from a local bare repo and update it

### Step 1 – Create dependency repo and add submodule

```bash
mkdir -p modules
git init --bare modules/lib.git
git clone modules/lib.git modules/lib-work
cd modules/lib-work
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
echo "lib-v1" > VERSION
git add VERSION && git commit -m "chore: lib v1"
git push origin HEAD
cd ../..
git init
git config user.name "REBASH Learner"
git config user.email "learner@rebash.local"
git submodule add ./modules/lib.git third_party/lib
git commit -m "chore: add lib submodule"
git submodule status
```

### Step 2 – Update submodule pointer

```bash
cd modules/lib-work
echo "lib-v2" > VERSION
git add VERSION && git commit -m "chore: lib v2"
git push origin HEAD
cd ../..
cd third_party/lib && git pull && cd ../..
git add third_party/lib
git commit -m "chore: bump lib submodule"
git submodule status
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-git/ for later tutorials
```



## Validation




Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Add/update | Submodule commit pin visible in parent tree |
| Init/sync | Fresh clone with submodule init shows expected files |
| Subtree | Subtree add/pull (if practised) updates the vendored path |
| Cleanup | Lab parent and submodule repos removed |



## Code Walkthrough




| Command | Description | Example |
|---------|-------------|---------|
| `git submodule add URL path` | Add submodule | `git submodule add URL modules/x` |
| `git clone --recurse-submodules` | Clone with submodules | Full recursive init |
| `git submodule update --init` | Init after clone | Post-clone setup |
| `git submodule update --remote` | Fetch latest submodule | Bump dependency |
| `git subtree add --prefix=P URL branch` | Add subtree | Merge external repo |
| `git subtree pull --prefix=P URL branch` | Update subtree | Pull upstream changes |
| `git submodule status` | Show submodule SHAs | Verify pinned versions |



## Security Considerations




- Pin submodule commits; floating `main` tips invite supply-chain surprises
- Verify remote URLs for submodules — typosquatting is a real risk
- Update submodules deliberately and run their tests in your CI
- Prefer subtree or vendoring when you need full control of third-party history
- Audit submodule changes in PRs as carefully as first-party code



## Common Mistakes




!!! warning "Clone without --recurse-submodules"
    Empty submodule directories break builds. Document in README; use CI init.

!!! warning "Committing submodule in detached HEAD"
    Parent records unexpected SHA. Always checkout branch in submodule before update.

!!! warning "Relative URLs breaking for external contributors"
    Use full URLs or configurable insteadOf in docs.

!!! warning "Subtree push overwriting upstream"
    `git subtree push` can force complex history. Coordinate with module owners.



## Best Practices




!!! tip "Prefer module registry over submodules for Terraform"
    `source = "app.terraform.io/org/vpc/aws"` with version constraint.

!!! tip "Pin submodule SHAs in PR description"
    Reviewers verify intentional version bumps.

!!! tip "Automate submodule update checks"
    Dependabot and Renovate support submodule updates.

!!! tip "Document clone command in README"
    `git clone --recurse-submodules` prominently at top.



## Troubleshooting




| Issue | Cause | Solution |
|-------|-------|----------|
| Empty submodule dir | Not initialized | `git submodule update --init --recursive` |
| Permission denied on submodule | CI token lacks access | PAT with repo scope |
| Submodule shows modified always | Line endings or detached | Normalize; checkout branch |
| Wrong submodule SHA on CI | Submodule not updated in commit | Verify `git submodule status` |
| Subtree merge conflicts | Diverged histories | Resolve; consider squash |
| Cannot remove submodule | Incomplete removal | deinit + rm + clean .git/modules |



## Summary




- **Submodules** pin external repos at specific commits — separate clone, explicit updates
- **Subtrees** merge external code into a subdirectory — simpler clone, complex push-back
- **`.gitmodules`** configures submodule paths and URLs
- Clone with **`--recurse-submodules`**; CI must initialize submodules
- For DevOps dependencies, prefer **registries** (Terraform, Helm) when available



## Interview Questions


1. Submodule versus subtree — operational differences?
2. Why do clones miss submodule content by default?
3. How do you bump a submodule pointer safely?
4. Common CI pitfalls with submodules?
5. When would you vendor instead?

!!! tip "Sample answer — question 2"
    Check .gitmodules, that git submodule update --init ran, and that the parent commit points at an existing submodule SHA.

!!! tip "Sample answer — question 4"
    Pin submodule URLs to trusted sources and review pointer bumps like dependency upgrades.



## Related Tutorials




- [Advanced Git Workflows](advanced-git-workflows.md) *(previous)*
- [Signed Commits and Git Security](signed-commits-and-git-security.md) *(next)*
- [Working with Remotes](working-with-remotes.md)
- [Creating and Cloning Repositories](creating-and-cloning-repositories.md)
- [Git – Category Overview](index.md)
- Cheat sheet: [Git Cheat Sheet](../cheatsheets/git.md)
- Interview prep: [Git Interview Prep](../interview/git.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)



## References




- [Pro Git Book – Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [git submodule documentation](https://git-scm.com/docs/git-submodule)
- [git subtree documentation](https://git-scm.com/docs/git-subtree)
- [Atlassian – Git submodules](https://www.atlassian.com/git/tutorials/git-submodule)
- [Terraform Module Sources](https://developer.hashicorp.com/terraform/language/modules/sources)
- [REBASH Academy – Git Overview](index.md)
