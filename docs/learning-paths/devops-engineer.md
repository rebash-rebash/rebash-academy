---
title: DevOps Engineer Learning Path
description: "Recommended order through Linux, Networking, Git, Docker, Kubernetes, and Terraform on REBASH Academy."
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-28"
category: learning-paths
tags:
  - learning-paths
  - devops
comments: false
---

# DevOps Engineer Learning Path

This path matches how production platforms are built: operating system fluency, networks, version control, containers, orchestration, then Infrastructure as Code.

## Ready modules (complete in order)

| # | Track | Start here | Status |
|---|--------|------------|--------|
| 1 | [Linux](../linux/index.md) | [Introduction to Linux](../linux/introduction-to-linux.md) | Ready — 20 tutorials |
| 2 | [Networking](../networking/index.md) | [Introduction to Networking](../networking/introduction-to-networking.md) | Ready — 20 tutorials |
| 3 | [Git](../git/index.md) | [Introduction to Git](../git/introduction-to-git-and-version-control.md) | Ready — 20 tutorials |
| 4 | [Docker](../docker/index.md) | [Introduction to Containers](../docker/introduction-to-containers-and-docker.md) | Ready — 20 tutorials |
| 5 | [Kubernetes](../kubernetes/index.md) | [Introduction to Kubernetes](../kubernetes/introduction-to-kubernetes-and-orchestration.md) | Ready — 20 tutorials |
| 6 | [Terraform](../terraform/index.md) | [Introduction to Terraform](../terraform/introduction-to-terraform-and-iac.md) | Ready — 20 tutorials |

## Supporting assets

| Asset | Linux | Networking | Git | Docker | Kubernetes | Terraform |
|-------|-------|------------|-----|--------|------------|-----------|
| Cheat sheet | [open](../cheatsheets/linux.md) | [open](../cheatsheets/networking.md) | [open](../cheatsheets/git.md) | [open](../cheatsheets/docker.md) | [open](../cheatsheets/kubernetes.md) | [open](../cheatsheets/terraform.md) |
| Interview prep | [open](../interview/linux.md) | [open](../interview/networking.md) | [open](../interview/git.md) | [open](../interview/docker.md) | [open](../interview/kubernetes.md) | [open](../interview/terraform.md) |
| Quiz | [open](../quizzes/linux-fundamentals.md) | — | — | [open](../quizzes/docker-fundamentals.md) | [open](../quizzes/kubernetes-fundamentals.md) | — |

## Standalone labs

| When you finish… | Practise with |
|------------------|---------------|
| Linux modules on systemd and logs | [Linux Production Incident Triage](../labs/linux-production-incident-triage.md) |
| DNS, firewalls, troubleshooting | [DNS and Firewall Site-Down Triage](../labs/networking-dns-firewall-triage.md) |
| Rebase, conflicts, safe force-push | [Git History and PR Recovery](../labs/git-history-pr-recovery.md) |
| Docker Compose and networking | [Docker Compose Stack Recovery](../labs/docker-compose-stack-recovery.md) |
| Deployments and probes | [Kubernetes Deployment Triage](../labs/kubernetes-deployment-triage.md) |
| Terraform CLI + CI concepts | [Terraform Plan Review Workflow](../labs/terraform-plan-review-workflow.md) |

Browse all labs: [Labs](../labs/index.md)

## Quizzes

Self-mark after finishing a track (or early modules): [Quizzes](../quizzes/index.md) — Linux, Docker, and Kubernetes fundamentals (40 questions, 70% pass).

## Portfolio project

After the labs above: [Status API Portfolio Build](../projects/status-api-portfolio.md) — Git → Docker → Kubernetes → Terraform metadata.

## Coming next on this path

Cloud platforms (AWS / Azure / GCP), GitLab CI/CD, monitoring, and DevSecOps are reserved on the [roadmap](../roadmap.md). Finish the six ready tracks first.

## Study rules

- Finish each tutorial lab before skipping ahead
- Keep a short incident notebook (symptom → cause → fix)
- Use interview questions as a gate between modules

## Related

- [Getting Started](../getting-started/index.md)
- [Learning Paths overview](index.md)
- [Roadmap](../roadmap.md)
