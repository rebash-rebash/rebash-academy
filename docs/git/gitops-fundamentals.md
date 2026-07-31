---
title: "GitOps Fundamentals"
description: "Understand GitOps — Git as the source of truth for desired state, reconciliation agents, and how PRs become deployments."
difficulty: intermediate
estimated_time: "45–60 min"
technology: git
category: git
module: "Module 12 · GitOps"
career_paths:
  - devops-engineer
  - platform-engineer
  - kubernetes-engineer
  - site-reliability-engineer
skills:
  - gitops
  - git
  - kubernetes
prerequisites:
  - git/github-actions-for-devops
next:
  - git/git-for-infrastructure-as-code
related:
  - argocd/index
  - git/production-git-practices
labs: []
projects: []
interview: interview/git
certifications:
  - GitOps Working Group concepts
tags:
  - gitops
  - git
  - argocd
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# GitOps Fundamentals

## Overview



Explain GitOps in one paragraph and sketch a repo layout where a reconciler (for example Argo CD) applies desired state from Git.

**GitOps** keeps the desired state of systems in Git. An agent compares live state to Git and reconciles. Changes go through PRs — audit trail and rollback by git revert.

This is a core tutorial in **Module 12 · GitOps** of the REBASH Academy **Git for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.



## Prerequisites



- [GitHub Actions for DevOps](github-actions-for-devops.md)
- Familiarity with containers/Kubernetes helps



## Learning Objectives



By the end of this tutorial, you will be able to:

- [ ] State the four GitOps principles (declarative, versioned, pulled, continuous)  
- [ ] Separate app code repos from config/env repos (common pattern)  
- [ ] Explain PR → merge → sync → cluster  
- [ ] Name rollback as `git revert` + sync



## Architecture



This topic’s control points and relationships are shown below.

![GitOps flow](../assets/excalidraw/git-gitops-flow.svg)



## Theory



### What

**GitOps** is an operational model where Git holds the **desired state** of a system, and software agents continuously **reconcile** the live environment toward that state. Humans change production by merging Git commits — not by running ad-hoc `kubectl apply` from laptops. Typical agents include Argo CD and Flux for Kubernetes.

### Why

Ticket-driven “clickops” drifts from reality and leaves weak audit trails. GitOps makes every production change a reviewed commit with history, rollback (revert or previous commit), and CI validation before the agent syncs. It separates **image build** (CI) from **deployment desire** (config repo update).

### How it works

Four principles guide the practice: (1) **Declarative** desired state (manifests, Helm, Kustomize); (2) **Versioned and immutable** history in Git; (3) **Pulled automatically** by an agent that watches the repo; (4) **Continuously reconciled** so drift is corrected or alerted. App pipelines build and push images; a follow-up commit updates the image tag or digest in the config repository; the agent deploys that digest.

### Key concepts

| Idea | Detail |
|------|--------|
| App repo vs config repo | Code/build vs desired cluster state |
| Sync / reconcile | Agent applies Git to the cluster |
| Drift | Live state differs from Git |
| Rollback | Revert Git or pin previous revision |


Separate concerns clearly: application CI builds and pushes images; a config repository (or path) records which digest each environment should run; the reconciler applies that desire. Promotion is a Git commit, so the same review and CODEOWNERS rules protect production as any other change. Measure drift and sync failures as first-class reliability signals.

### Common pitfalls

- Manual hotfixes in the cluster that Git overwrites on the next sync  
- Storing secrets as plain YAML in Git without sealing/SOPS/External Secrets  
- Pointing GitOps at mutable `:latest` tags  
- Letting CI deploy directly *and* GitOps deploy the same apps without a clear boundary



## Hands-on Lab


Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-git/module-12/{apps/demo,clusters/dev} && cd ~/rebash-git/module-12/{apps/demo,clusters/dev}
```

**Focus:** practise Git skills for: GitOps Fundamentals

### Step 1 – Init repository

```bash
git init -b main
git config user.email 'lab@rebash.local'
git config user.name 'REBASH Lab'
echo '# lab' > README.md
git add README.md
git commit -m 'Initial commit'
git log --oneline
```

### Step 2 – Desired-state folder

```bash
mkdir -p desired/app
cat > desired/app/deploy.yaml << 'EOF'
apiVersion: v1
kind: ConfigMap
metadata: { name: demo }
data: { ok: "yes" }
EOF
git add desired && git commit -m 'Add desired state'
git ls-tree -r HEAD --name-only | tee tree.txt
```

### Final step – Cleanup note

```bash
# Safe local repo under the lab directory; delete the folder when finished
```



## Validation



- [ ] Lab commands run under `~/rebash-git/module-12/{apps/demo,clusters/dev}/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic



## Code Walkthrough



Production practice for **GitOps Fundamentals** always combines:

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



!!! warning "Manual hotfixes in the cluster that Git overwrites on the next sync  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Storing secrets as plain YAML in Git without sealing/SOPS/External Secrets  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).



## Best Practices



- Encode GitOps Fundamentals changes as code and review them in pull requests
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



**GitOps Fundamentals** is essential for Cloud and DevOps engineers working with git. Practise the lab until the inspection and change path is muscle memory, then continue the track.



## Interview Questions


1. Explain **GitOps Fundamentals** as you would in a senior engineer interview.
2. You rebased a shared branch and teammates are blocked — what now?
3. How do you recover a commit that seems lost?
4. What Git security controls belong in a production org?
5. How should Git history look for Infrastructure as Code (IaC) repos?

!!! tip "Sample answer — question 2"
    Stop force-pushing; communicate; use `reflog` to recover; prefer revert on shared main. Reset/rebase only on private branches.

!!! tip "Sample answer — question 4"
    Signed commits, protected branches, secret scanning, least-privilege tokens, and signed tags for releases.



## Related Tutorials



- [Course overview](index.md)
- [Git for Infrastructure as Code](git-for-infrastructure-as-code.md)
- [Argo CD](../argocd/index.md)



## References



- [OpenGitOps principles](https://opengitops.dev/)
