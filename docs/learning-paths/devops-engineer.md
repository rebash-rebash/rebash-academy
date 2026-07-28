---
title: DevOps Engineer Learning Path
description: "Recommended order through Linux, Networking, AWS, Git, CI/CD, Docker, Kubernetes, and Terraform on REBASH Academy."
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

This path matches how production platforms are built: operating systems, networks, cloud, version control, pipelines, containers, orchestration, then Infrastructure as Code.

## Ready modules (complete in order)

| # | Track | Start here | Status |
|---|--------|------------|--------|
| 1 | [Linux](../linux/index.md) | [Introduction to Linux](../linux/introduction-to-linux.md) | Ready — 25 tutorials |
| 2 | [Networking](../networking/index.md) | [Introduction to Networking](../networking/introduction-to-networking.md) | Ready — 25 tutorials |
| 3 | [AWS](../aws/index.md) | [Introduction to AWS and Global Infrastructure](../aws/introduction-to-aws-and-global-infrastructure.md) | Ready — 20 tutorials |
| 4 | [Git](../git/index.md) | [Introduction to Git](../git/introduction-to-git-and-version-control.md) | Ready — 20 tutorials |
| 5 | [GitLab CI/CD](../gitlab/index.md) | [Introduction to CI/CD and Delivery Models](../gitlab/introduction-to-cicd-and-delivery-models.md) | Ready — 20 tutorials (GitLab CI) |
| 6 | [Docker](../docker/index.md) | [Introduction to Containers](../docker/introduction-to-containers-and-docker.md) | Ready — 20 tutorials |
| 7 | [Kubernetes](../kubernetes/index.md) | [Introduction to Kubernetes](../kubernetes/introduction-to-kubernetes-and-orchestration.md) | Ready — 20 tutorials |
| 8 | [Terraform](../terraform/index.md) | [Introduction to Terraform](../terraform/introduction-to-terraform-and-iac.md) | Ready — 20 tutorials |

!!! tip "Why CI/CD after Git?"
    Pipelines are triggered by Git events. Learn branching and reviews first, then automate build/test/deploy with **GitLab CI** before deep Docker/Kubernetes deploy labs. Jenkins and GitHub Actions follow in later tracks.

## Supporting assets

| Asset | Linux | Networking | AWS | Git | CI/CD | Docker | Kubernetes | Terraform |
|-------|-------|------------|-----|-----|-------|--------|------------|-----------|
| Cheat sheet | [open](../cheatsheets/linux.md) | [open](../cheatsheets/networking.md) | [open](../cheatsheets/aws.md) | [open](../cheatsheets/git.md) | [open](../cheatsheets/cicd.md) | [open](../cheatsheets/docker.md) | [open](../cheatsheets/kubernetes.md) | [open](../cheatsheets/terraform.md) |
| Interview prep | [open](../interview/linux.md) | [open](../interview/networking.md) | [open](../interview/aws.md) | [open](../interview/git.md) | [open](../interview/cicd.md) | [open](../interview/docker.md) | [open](../interview/kubernetes.md) | [open](../interview/terraform.md) |
| Quiz | [fundamentals](../quizzes/linux-fundamentals.md) · [servers](../quizzes/linux-servers.md) | [production](../quizzes/networking-production.md) | [fundamentals](../quizzes/aws-fundamentals.md) | — | [fundamentals](../quizzes/cicd-fundamentals.md) | [open](../quizzes/docker-fundamentals.md) | [open](../quizzes/kubernetes-fundamentals.md) | — |

## Standalone labs

| When you finish… | Practise with |
|------------------|---------------|
| Linux modules on systemd and logs | [Linux Production Incident Triage](../labs/linux-production-incident-triage.md) |
| Linux Module 7 (nginx/TLS/backup) | [Linux App Server from Zero](../labs/linux-app-server-from-zero.md) |
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

Self-mark after finishing a track: [Quizzes](../quizzes/index.md) — Linux, Networking production, AWS, CI/CD, Docker, and Kubernetes.

## Portfolio project

After the labs above: [Status API Portfolio Build](../projects/status-api-portfolio.md) — Git → Docker → Kubernetes → Terraform metadata.

## Coming next on this path

Azure, GCP, monitoring, and DevSecOps remain on the [roadmap](../roadmap.md).

## Study rules

- Finish each tutorial lab before skipping ahead
- Keep a short incident notebook (symptom → cause → fix)
- Use interview questions as a gate between modules
- Never print secrets in pipeline logs; prefer OIDC/short-lived tokens

## Related

- [Getting Started](../getting-started/index.md)
- [Learning Paths overview](index.md)
- [Roadmap](../roadmap.md)
