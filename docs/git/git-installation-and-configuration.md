---
title: "Git Installation and Configuration"
description: "Install Git, set user identity and editors, and configure SSH and HTTPS authentication for Cloud and DevOps workflows."
difficulty: beginner
estimated_time: "30–45 min"
technology: git
category: git
module: "Module 2 · Installing Git"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
skills:
  - git
  - ssh
  - configuration
prerequisites:
  - git/understanding-the-git-object-model
next:
  - git/creating-and-cloning-repositories
related:
  - git/signed-commits-and-git-security
  - linux/index
labs: []
projects: []
interview: interview/git
certifications:
  - GitHub Foundations
tags:
  - git
  - install
  - ssh
  - config
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Git Installation and Configuration

## Overview

Install a current Git, set global identity and defaults, and prepare SSH or HTTPS auth for GitHub/GitLab without committing secrets.

Wrong `user.name`/`user.email` pollutes audit trails. Broken SSH blocks every clone in CI. Configure once, verify, then never commit tokens.

Diagrams: [git-workflow](../assets/excalidraw/git-workflow.svg).

This is a core tutorial in **Module 2 · Installing Git** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Linux/macOS/WSL with package install rights  
- [Object model](understanding-the-git-object-model.md) recommended

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install/verify Git  
- [ ] Set `user.name` and `user.email`  
- [ ] Choose editor and useful defaults  
- [ ] Configure SSH keys for hosting  
- [ ] Know when HTTPS + credential helper / PAT applies

## Architecture

This topic’s control points and relationships are shown below.

![Architecture diagram for Git Installation and Configuration](../assets/excalidraw/git-workflow.svg)

## Theory

### What

Installing Git gives you the `git` CLI and a local object database. **Configuration** sets identity (`user.name`, `user.email`), defaults (`init.defaultBranch`), editor choice, pull behaviour, and how you authenticate to remotes — usually **SSH** keys for humans and short-lived tokens or OpenID Connect (OIDC) for Continuous Integration (CI).

### Why

Wrong identity pollutes history with personal emails on corporate repos. Ambiguous pull defaults cause surprise merge commits or rebases. Broken SSH or credential helpers block every push. A few deliberate `git config` choices prevent weeks of friction for DevOps teams.

### How it works

On Debian/Ubuntu you typically install the distribution package, then set **global** config in `~/.gitconfig`. Per-repository settings in `.git/config` override global ones — useful for work vs personal emails. Authentication is separate from Git itself: SSH uses keys loaded in an agent; HTTPS uses a credential helper and personal access tokens (PATs). Prefer SSH for day-to-day human work; CI often uses deploy keys, fine-grained PATs, or cloud OIDC federation.

```bash
# Debian/Ubuntu sketch
sudo apt-get update && sudo apt-get install -y git
git config --global user.name "Your Name"
git config --global user.email "you@company.com"
git config --global init.defaultBranch main
```

### Key concepts

| Setting | Guidance |
|---------|----------|
| `user.name` / `user.email` | Match the hosting account; use work email at work |
| `init.defaultBranch` | Prefer `main` unless the org standard differs |
| `core.editor` | Set once (`vim`, `code --wait`, …) |
| `pull.rebase` | Agree as a team — `true` or `false`, not “whatever happens” |
| `fetch.prune` | `true` removes stale remote-tracking branches |

SSH checklist: `ssh-keygen -t ed25519`, add the public key to GitHub/GitLab, then `ssh -T git@github.com`. Never commit tokens inside remote URLs.

### Common pitfalls

- Embedding PATs in `https://user:token@…` remotes that leak via `git remote -v`  
- Mixing personal and work emails without per-repo overrides  
- Skipping logout/login after adding an SSH key to the agent  
- Leaving `pull` behaviour undefined so juniors get inconsistent histories

## Hands-on Lab

**Focus:** practise the core workflow for Git Installation and Configuration

```bash
mkdir -p ~/rebash-git/module-02
cd ~/rebash-git/module-02
```

### Step 1 – Verify install

```bash
git --version
git config --list --show-origin | head -40
```

### Step 2 – Set lab identity (local to lab dir)

```bash
cd ~/rebash-git/module-02
mkdir cfg && cd cfg && git init -b main
git config user.name "REBASH Lab"
git config user.email "lab@rebash.local"
git config --list --local
```

### Step 3 – SSH check (optional)

```bash
ssh -T git@github.com 2>&1 | head -5 || echo "Configure keys when ready"
```

## Validation

- [ ] Lab commands run under `~/rebash-git/module-02/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Git Installation and Configuration** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for git as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Embedding PATs in `https://user:token@…` remotes that leak via `git remote -v`  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Mixing personal and work emails without per-repo overrides  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Git Installation and Configuration changes as code and review them in pull requests
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

- Install Git; set identity correctly  
- SSH keys for daily work; short-lived tokens for CI  
- Document team defaults (`pull.rebase`, default branch)

## Interview Questions

1. How does **Git Installation and Configuration** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Creating and Cloning Repositories](creating-and-cloning-repositories.md)

## References

- [git-config](https://git-scm.com/docs/git-config)  
- [GitHub SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
