---
title: Overview
description: "AWS for Cloud & DevOps Engineers — 16 modules from global infrastructure through IAM, VPC, compute, containers, serverless, security, IaC, cost, and production landing zones."
difficulty: beginner
estimated_time: "12–16 weeks"
author: Shaik Basha
last_updated: "2026-07-31"
category: aws
tags:
  - aws
  - cloud
  - devops
  - course
comments: false
---

# AWS for Cloud & DevOps Engineers

**Duration:** 12–16 weeks · **Difficulty:** Beginner → Advanced
{ .ra-facts }

Production Amazon Web Services (AWS) — design, deploy, secure, operate, and optimise cloud environments for Cloud, DevOps, Platform, and SRE roles.

!!! tip "Course status"
    Curriculum follows the REBASH AWS technology prompt (**16 modules**). Tutorials use **Excalidraw** diagrams under `docs/assets/excalidraw/` (not D2). Regenerate with `python3 scripts/generate-excalidraw-svg.py`. Start with [AWS Fundamentals](aws-fundamentals-and-global-infrastructure.md).

!!! warning "Cost hygiene"
    Prefer Free Tier and destroy resources after labs. **NAT Gateways**, idle **ALBs**, and **RDS** are common bill surprises. Create a billing alarm before you launch paid services.

## 1. Course overview

### Purpose

Build production AWS fluency: global infrastructure, IAM, VPC design, compute and data services, containers and serverless, observability, security, Infrastructure as Code (IaC), CI/CD, cost control, reliability, and multi-account landing zones.

### Target roles

Cloud Engineer · DevOps · Platform · SRE · DevSecOps · Infrastructure · Solutions Architect

### Prerequisites

- [Linux](../linux/index.md) · [Networking](../networking/index.md) · [Git](../git/index.md)
- [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md) and [Terraform](../terraform/index.md) recommended for Modules 7 and 11+

### Capstone outcomes

Secure networking · IAM governance · EKS/ECS · serverless patterns · CI/CD · monitoring · backup/DR · cost optimisation · multi-account landing zone

## 2. Modules

| Module | Focus | Start here |
|-------:|-------|------------|
| 1 | AWS fundamentals | [Global infrastructure](aws-fundamentals-and-global-infrastructure.md) |
| 2 | IAM | [Identity & access](iam-identity-access-and-organizations.md) |
| 3 | Networking | [VPC networking](vpc-networking-on-aws.md) |
| 4 | Compute | [EC2 · ASG · LB](compute-ec2-asg-and-load-balancing.md) |
| 5 | Storage | [S3 · EBS · EFS](storage-s3-ebs-efs.md) |
| 6 | Databases | [RDS · DynamoDB](databases-on-aws.md) |
| 7 | Containers | [ECS · EKS · ECR](containers-ecs-eks-ecr.md) |
| 8 | Serverless | [Lambda & events](serverless-on-aws.md) |
| 9 | Monitoring | [Observability](monitoring-and-observability-on-aws.md) |
| 10 | Security | [Security services](aws-security-services.md) |
| 11 | IaC | [Terraform · CFN · CDK](infrastructure-as-code-on-aws.md) |
| 12 | CI/CD | [Pipelines on AWS](cicd-on-aws.md) |
| 13 | Cost | [Cost optimisation](cost-optimisation-on-aws.md) |
| 14 | Reliability | [HA & DR](reliability-and-disaster-recovery.md) |
| 15 | Production | [Landing zones](production-aws-landing-zones.md) |
| 16 | Troubleshooting | [Troubleshoot AWS](troubleshooting-aws.md) |

## 3. Practice

- [Labs](../labs/index.md) · [Projects](projects/index.md) · [Quizzes](quizzes/index.md)
- [Cheat sheets](cheatsheets/index.md) · [Interview](interview/index.md) · [Capstone](capstone/index.md)
- [Roadmap](roadmap.md) · [FAQ](faq.md) · [Certifications](certifications/index.md)

## Diagrams

``` {.bash .ra-terminal title="Terminal"}
python3 scripts/generate-excalidraw-svg.py
```

## Related

- [Networking](../networking/index.md) · [Linux](../linux/index.md) · [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md) · [Terraform](../terraform/index.md)
- [Azure](../azure/index.md) · [GCP](../gcp/index.md)
- [Cloud Engineer path](../career-paths/cloud-engineer/index.md)
