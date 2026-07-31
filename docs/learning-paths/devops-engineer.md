---
title: DevOps Engineer Learning Path
description: "Recommended order through Linux, Shell Scripting, Python for DevOps, Networking, AWS, Git, CI/CD, Docker, Kubernetes, and Terraform on REBASH Academy."
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-29"
category: learning-paths
tags:
  - learning-paths
  - devops
comments: false
---

# DevOps Engineer Learning Path

This path matches how production platforms are built: operating systems, **shell automation**, **Python for structured data and APIs**, networks, cloud, version control, pipelines, containers, orchestration, then Infrastructure as Code.

## Ready modules (complete in order)

| # | Track | Start here | Status |
|---|--------|------------|--------|
| 1 | [Linux](../linux/index.md) | [Linux Fundamentals — Distributions and Architecture](../linux/linux-fundamentals-distributions-and-architecture.md) | Ready — 16 modules · 25 tutorials |
| 2 | [Shell Scripting](../shell/index.md) | [Shell Fundamentals — Bash vs sh and Execution](../shell/shell-fundamentals-bash-vs-sh-and-execution.md) | Ready — 18 modules · 18 tutorials |
| 3 | [Python for DevOps](../python/index.md) | [Install, venv, and Tooling](../python/python-fundamentals-install-venv-and-tooling.md) | Ready — 27 modules · 27 tutorials |
| 4 | [Networking](../networking/index.md) | [Introduction to Networking](../networking/introduction-to-networking.md) | Ready — 25 tutorials |
| 5 | [AWS](../aws/index.md) | [AWS Fundamentals and Global Infrastructure](../aws/aws-fundamentals-and-global-infrastructure.md) | Ready — 16 modules · 16 tutorials |
| 6 | [Git](../git/index.md) | [Introduction to Git](../git/introduction-to-git-and-version-control.md) | Ready — 20 tutorials |
| 7 | [GitLab CI/CD](../gitlab/index.md) | [GitLab CI/CD Fundamentals](../gitlab/gitlab-ci-fundamentals.md) | Ready — 18 modules (GitLab CI) |
| 8 | [Docker](../docker/index.md) | [Introduction to Containers](../docker/introduction-to-containers-and-docker.md) | Ready — 20 tutorials |
| 9 | [Kubernetes](../kubernetes/index.md) | [Introduction to Kubernetes](../kubernetes/introduction-to-kubernetes-and-orchestration.md) | Ready — 20 tutorials |
| 10 | [Terraform](../terraform/index.md) | [Introduction to Terraform](../terraform/introduction-to-terraform-and-iac.md) | Ready — 20 tutorials |

!!! tip "Why Linux first?"
    Every cloud VM, container node, and CI runner is Linux underneath. Finish the **16 Cloud & DevOps modules** (fundamentals through production) before Shell. See also [Linux for Cloud & DevOps](linux-for-cloud-devops.md).

!!! tip "Why Shell after Linux?"
    Linux teaches the tools; Shell Scripting turns them into reviewed, schedulable automation for admins and DevOps. Take it before Networking so later labs can assume solid Bash habits.

!!! tip "Why Python after Shell?"
    Bash remains the launcher. Python owns JSON/YAML, HTTP clients, tests, and packaged CLIs. See also the dedicated [Python for DevOps Engineers](python-for-devops.md) path.

!!! tip "Why CI/CD after Git?"
    Pipelines are triggered by Git events. Learn branching and reviews first, then automate build/test/deploy with **GitLab CI** before deep Docker/Kubernetes deploy labs.

## Supporting assets

| Asset | Linux | Shell | Python | Networking | AWS | Git | CI/CD | Docker | Kubernetes | Terraform |
|-------|-------|-------|--------|------------|-----|-----|-------|--------|------------|-----------|
| Cheat sheet | [open](../cheatsheets/linux.md) | [open](../cheatsheets/shell.md) | [open](../cheatsheets/python.md) | [open](../cheatsheets/networking.md) | [open](../cheatsheets/aws.md) | [open](../cheatsheets/git.md) | [open](../cheatsheets/cicd.md) | [open](../cheatsheets/docker.md) | [open](../cheatsheets/kubernetes.md) | [open](../cheatsheets/terraform.md) |
| Interview prep | [open](../interview/linux.md) | [open](../interview/shell.md) | [open](../interview/python.md) | [open](../interview/networking.md) | [open](../interview/aws.md) | [open](../interview/git.md) | [open](../interview/cicd.md) | [open](../interview/docker.md) | [open](../interview/kubernetes.md) | [open](../interview/terraform.md) |
| Quiz | [course fundamentals](../quizzes/linux-for-cloud-devops-fundamentals.md) · [fundamentals](../quizzes/linux-fundamentals.md) · [servers](../quizzes/linux-servers.md) | [course fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md) | [course fundamentals](../quizzes/python-for-devops-engineers-fundamentals.md) | [production](../quizzes/networking-production.md) | [fundamentals](../quizzes/aws-fundamentals.md) | — | [fundamentals](../quizzes/cicd-fundamentals.md) | [open](../quizzes/docker-fundamentals.md) | [open](../quizzes/kubernetes-fundamentals.md) | — |

## Standalone labs

| When you finish… | Practise with |
|------------------|---------------|
| Linux modules on systemd and logs | [Linux Production Incident Triage](../labs/linux-production-incident-triage.md) |
| Linux security / storage / ops labs | [Firewall hardening](../labs/linux-firewall-hardening-lab.md) · [Ops toolkit](../labs/linux-ops-toolkit-lab.md) · [App server from zero](../labs/linux-app-server-from-zero.md) |
| Shell Scripting (any module) | [Shell labs](../labs/shell-first-script.md) · [Ops Script Hardening](../labs/shell-ops-script-hardening.md) · [Operations Toolkit](../labs/shell-linux-operations-toolkit.md) |
| Python Modules 1–2 | [Python Log Analyser](../labs/python-log-analyser.md) · [Linux Health Checker](../labs/python-linux-health-checker.md) · [YAML Config Validator](../labs/python-yaml-config-validator.md) · [JSON Validator](../labs/python-json-validator.md) |
| DNS, firewalls, troubleshooting | [DNS and Firewall Site-Down Triage](../labs/networking-dns-firewall-triage.md) |
| Networking Module 7 (LB/DNS/ACL/IR) | [Networking Edge Failover](../labs/networking-edge-failover.md) |
| AWS IAM + VPC | [AWS IAM and VPC Reachability Triage](../labs/aws-iam-vpc-triage.md) |
| AWS SSM + S3 | [Secure EC2 via SSM and S3](../labs/aws-ssm-s3.md) |
| Rebase, conflicts, safe force-push | [Git History and PR Recovery](../labs/git-history-pr-recovery.md) |
| CI/CD pipeline failures | [CI/CD Pipeline Failure Triage](../labs/cicd-pipeline-triage.md) |
| CI/CD Docker + deploy gate | [Docker Build, Scan, and Deploy Gate](../labs/cicd-docker-secure-gate.md) |
| Docker Compose and networking | [Docker Compose Stack Recovery](../labs/docker-compose-stack-recovery.md) |
| Deployments and probes | [Kubernetes Deployment Triage](../labs/kubernetes-deployment-triage.md) |
| Terraform CLI + CI concepts | [Terraform Plan Review Workflow](../labs/terraform-plan-review-workflow.md) |

Browse all labs: [Labs](../labs/index.md)

## Quizzes

Self-mark after finishing a track: [Quizzes](../quizzes/index.md) — Linux, Shell Scripting, Python for DevOps, Networking production, AWS, CI/CD, Docker, and Kubernetes.

## Portfolio project

After the labs above: [Status API Portfolio Build](../projects/status-api-portfolio.md) — Git → Docker → Kubernetes → Terraform metadata. Python projects: [Log Analysis Tool](../projects/python-log-analysis-tool.md) through [Automation platform](../projects/python-devops-automation-framework.md).

## Coming next on this path

Azure, GCP, monitoring, and DevSecOps remain on the [roadmap](../roadmap.md).

## Study rules

- Finish each tutorial lab before skipping ahead
- Keep a short incident notebook (symptom → cause → fix)
- Use interview questions as a gate between modules
- Never print secrets in pipeline logs; prefer OIDC/short-lived tokens

## Related

- [Getting Started](../getting-started/index.md)
- [Roadmap](../roadmap.md)
- [Learning Paths](index.md)
