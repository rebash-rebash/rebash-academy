---
title: "Kubernetes Deploys and GitLab Agent"
description: "Deploy with the GitLab Agent for Kubernetes, kubectl and Helm, canary and blue-green patterns, rollbacks, and the GitOps boundary."
difficulty: advanced
estimated_time: "50–65 min"
technology: gitlab
category: gitlab
module: "Module 9 · Kubernetes Deployments"
career_paths:
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - devsecops-engineer
skills:
  - gitlab-ci
  - kubernetes
  - helm
  - gitops
prerequisites:
  - gitlab/building-docker-images-in-ci
next:
  - gitlab/terraform-pipelines-in-gitlab
related:
  - kubernetes/introduction-to-kubernetes-and-orchestration
  - helm/introduction-to-helm
  - gitlab/production-pipelines-and-environments
labs: []
projects: []
interview: interview/gitlab
certifications:
  - GitLab Certified CI/CD Associate
  - GitLab Certified DevOps Professional
tags:
  - gitlab
  - kubernetes
  - gitlab-agent
  - helm
  - gitops
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Kubernetes Deploys and GitLab Agent

## Overview

Describe how the GitLab Agent connects CI to a cluster, sketch a Helm or kubectl deploy job, and contrast push deploys with GitOps pull controllers — including canary, blue-green, and rollback.

Pipelines that **push** manifests with `kubectl` or **Helm** need a secure path into the cluster. The **GitLab Agent for Kubernetes** (`agentk`) establishes a reverse tunnel so runners never hold long-lived kubeconfigs in CI variables. Progressive delivery (canary, blue-green) and rollbacks sit on top of Deployments or Helm releases. **GitOps** (Flux/Argo CD) inverts the model: the cluster pulls desired state from Git (conceptual flow in `gitlab-gitops.svg`).

This is a core tutorial in **Module 9 · Kubernetes Deployments** of the REBASH Academy **GitLab CI/CD for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Building Docker Images in CI](building-docker-images-in-ci.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the GitLab Agent trust boundary vs stored kubeconfig  
- [ ] Sketch a deploy job using `kubectl` or Helm  
- [ ] Compare canary and blue-green  
- [ ] Outline rollback (Helm revision / prior image digest)  
- [ ] State when push CI ends and GitOps begins

## Architecture

This topic’s control points and relationships are shown below.

![Kubernetes deploy from GitLab](../assets/excalidraw/gitlab-kubernetes-deploy.svg)

## Theory

### What it is

**Kubernetes deployment from GitLab** means a job updates cluster state after images are built and scanned. The **GitLab Agent** is a lightweight process in the cluster that authenticates to GitLab and receives CI/`ci_access` connections — CI jobs request Kubernetes API access through the agent rather than embedding admin kubeconfigs.

| Mode | Who applies changes | Fit |
|------|---------------------|-----|
| Push CI (`kubectl` / Helm) | Pipeline job | Simple apps, demos, controlled envs |
| GitOps pull | Controller (Argo CD / Flux) | Multi-cluster, strong drift control |
| Hybrid | CI updates Git; controller syncs | Common enterprise pattern |

### Why it matters

Static kubeconfigs in CI are high-value secrets and hard to rotate. Agents shrink blast radius and support environment-scoped access. Progressive delivery reduces blast radius of bad releases; rollbacks need a practised path (previous Helm revision or prior digest). Confusing push CI with GitOps causes double-writes and drift fights.

### How it works

1. Install `agentk` in the cluster; register it to a GitLab project/group.  
2. Grant `ci_access` (or GitOps access) for selected projects.  
3. CI job uses the agent context to run `kubectl set image` / `helm upgrade --install` with the SHA-tagged image from Module 8.  
4. **Canary**: shift a fraction of traffic (Ingress weight / Flagger / service mesh). **Blue-green**: two full stacks; switch Service or Ingress when healthy.  
5. **Rollback**: `helm rollback`, or redeploy the last known-good digest; GitOps reverts the Git commit and lets the controller sync.

Keep production behind protected environments and manual or approval gates.

### Key concepts and comparisons

| Pattern | Idea | Rollback |
|---------|------|----------|
| Rolling update | Default Deployment surge | Roll back ReplicaSet / Helm |
| Canary | Partial traffic to new version | Shift weight back |
| Blue-green | Two environments, cut over | Point traffic at blue again |
| GitOps | Desired state in Git | Revert commit |

### Common pitfalls

- Cluster-admin credentials in unprotected CI variables.  
- Deploying `latest` instead of the SHA built in the same pipeline.  
- Running canary without metrics or automatic abort.  
- Both CI and Argo CD applying the same Deployment (duelling controllers).  
- Skipping `helm history` / revision notes so rollback targets are unclear.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-gitlab/module-09/manifests && cd ~/rebash-gitlab/module-09/manifests
```

**Focus:** hands-on practice for Kubernetes Deploys and GitLab Agent

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab: Kubernetes Deploys and GitLab Agent"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Core exercise

Credentials and a live cluster are not required — this lab captures the pattern and policy notes.

```bash
mkdir -p ~/rebash-gitlab/module-09/manifests && cd ~/rebash-gitlab/module-09
```

{% raw %}
```yaml
# .gitlab-ci.yml
stages: [deploy]

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    kubernetes:
      agent: path/to/agent:agent-name
  script:
    - kubectl -n staging set image deployment/demo app="$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA"
    - kubectl -n staging rollout status deployment/demo --timeout=120s
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  # Production: protected environment + when: manual
```
{% endraw %}

```bash
cat > manifests/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: { name: demo }
spec:
  replicas: 2
  selector: { matchLabels: { app: demo } }
  template:
    metadata: { labels: { app: demo } }
    spec:
      containers:
        - name: app
          image: registry.example.com/demo:REPLACE_SHA
EOF

cat > deploy-notes.md << 'EOF'
Agent over kubeconfig · promote Module 8 SHA · canary needs metrics
GitOps: CI updates Git; controller syncs (gitlab-gitops concept)
Rollback: helm rollback N or prior digest
EOF
python3 -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-gitlab/ for later labs; destroy cloud resources you created
./lab.sh || true
```

## Validation

- [ ] Lab commands run under `~/rebash-gitlab/module-09/manifests/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Kubernetes Deploys and GitLab Agent** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for gitlab as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Cluster-admin credentials in unprotected CI variables.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Deploying `latest` instead of the SHA built in the same pipeline.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Kubernetes Deploys and GitLab Agent changes as code and review them in pull requests
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

**Kubernetes Deploys and GitLab Agent** is essential for Cloud and DevOps engineers working with gitlab. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Kubernetes Deploys and GitLab Agent** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Terraform Pipelines in GitLab](terraform-pipelines-in-gitlab.md)

## References

- [GitLab Agent for Kubernetes](https://docs.gitlab.com/ee/user/clusters/agent/) · [CI/CD with agent](https://docs.gitlab.com/ee/user/clusters/agent/ci_cd_workflow.html) · [Environments](https://docs.gitlab.com/ee/ci/environments/)
