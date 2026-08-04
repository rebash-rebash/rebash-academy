---
title: Overview
description: "AWS for Cloud & DevOps Engineers — 16 interview-depth modules from global infrastructure through IAM, VPC, compute, data, containers, serverless, security, IaC, cost, and production landing zones."
difficulty: beginner
estimated_time: "12–16 weeks"
technology_id: aws
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - cloud
  - devops
  - course
comments: false
---

# AWS for Cloud & DevOps Engineers

**Duration:** 12–16 weeks · **Difficulty:** Beginner → Advanced · **Labs:** create → prove → break/fix → destroy
{ .ra-facts }

Learn AWS the way operators use it: start from a clear problem, build a simple mental model, then practise with a real sandbox lab (create → prove → break/fix where useful → destroy). Suitable if you are new to AWS or revising for Cloud and DevOps interviews.

!!! tip "How to use this course"
    Work modules in order. Finish each lab with evidence files, practise Interview Questions aloud, and use [standalone triage labs](../labs/aws-iam-vpc-triage.md) after Modules 3–4.

!!! warning "Cost hygiene"
    Prefer Free Tier. **Never leave NAT Gateways, ALBs, or RDS running overnight.** Create a budget alarm in [Module 1](aws-fundamentals-and-global-infrastructure.md) before you launch compute.

## Learning roadmap

1. **Foundations (Modules 1–2)** — global infrastructure, cost guardrails, Identity and Access Management (IAM) / Security Token Service (STS)
2. **Network & compute (Modules 3–4)** — Virtual Private Cloud (VPC) paths, EC2 / Auto Scaling / load balancing
3. **Data & apps (Modules 5–8)** — storage, databases, containers, serverless
4. **Operate & secure (Modules 9–10)** — observability and security services
5. **Deliver & govern (Modules 11–15)** — Infrastructure as Code (IaC), CI/CD, FinOps, disaster recovery, landing zones
6. **Triage mastery (Module 16)** — decision tree under pressure

!!! tip "Checkpoint after Module 4"
    Complete [IAM and VPC Reachability Triage](../labs/aws-iam-vpc-triage.md) before continuing — it locks Modules 1–4 together.

### Prerequisites

- [Linux](../linux/index.md) · [Networking](../networking/index.md) · [Git](../git/index.md)
- [Docker](../docker/index.md) (required for Module 7 ECR lab)
- [Kubernetes](../kubernetes/index.md) and [Terraform](../terraform/index.md) recommended for Modules 7 and 11+

## Modules

| Module | Focus | Lab proof | Start here |
|-------:|-------|-----------|------------|
| 1 | Fundamentals | STS identity + Budgets alarm | [Global infrastructure](aws-fundamentals-and-global-infrastructure.md) |
| 2 | IAM | AssumeRole deny/allow | [Identity & access](iam-identity-access-and-organizations.md) |
| 3 | Networking | Public VPC + S3 endpoint + route break/fix | [VPC networking](vpc-networking-on-aws.md) |
| 4 | Compute | EC2 nginx + SG break/fix + curl | [EC2 · ASG · LB](compute-ec2-asg-and-load-balancing.md) |
| 5 | Storage | S3 versioning/encryption/policy deny | [S3 · EBS · EFS](storage-s3-ebs-efs.md) |
| 6 | Databases | DynamoDB put/query/PITR | [RDS · DynamoDB](databases-on-aws.md) |
| 7 | Containers | ECR push + task definition artefact | [ECS · EKS · ECR](containers-ecs-eks-ecr.md) |
| 8 | Serverless | Lambda Function URL break/fix | [Lambda & events](serverless-on-aws.md) |
| 9 | Monitoring | Custom metric alarm ALARM→OK | [Observability](monitoring-and-observability-on-aws.md) |
| 10 | Security | KMS + encrypted S3 proof | [Security services](aws-security-services.md) |
| 11 | IaC | CloudFormation stack create/delete | [Terraform · CFN · CDK](infrastructure-as-code-on-aws.md) |
| 12 | CI/CD | CodeBuild SUCCEEDED | [Pipelines on AWS](cicd-on-aws.md) |
| 13 | Cost | USD 5 Budget | [Cost optimisation](cost-optimisation-on-aws.md) |
| 14 | Reliability | EBS snapshot DR drill | [HA & DR](reliability-and-disaster-recovery.md) |
| 15 | Production | Landing-zone artefacts + org/boundary | [Landing zones](production-aws-landing-zones.md) |
| 16 | Troubleshooting | Full STS + SG triage loop | [Troubleshoot AWS](troubleshooting-aws.md) |

## Related

- [Networking](../networking/index.md) · [Linux](../linux/index.md) · [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md) · [Terraform](../terraform/index.md)
- [Azure](../azure/index.md) · [GCP](../gcp/index.md)
- [Cloud Engineer path](../learning-paths/cloud-engineer/index.md)
