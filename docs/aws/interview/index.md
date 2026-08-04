---
title: Interview Preparation
description: "AWS interview preparation hub — themes, story bank from course labs, and links to module question sets for Cloud, DevOps, and Solutions Architect roles."
technology_id: aws
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - interview
comments: false
---

# AWS — Interview Preparation

Use this hub with the **Interview Questions** at the end of every module (question visible, answer under **Reveal answer**). Practise explaining each answer in plain English, then add one production detail. Prefer **stories with evidence** (“I assumed a role, captured AccessDenied, then DescribeRegions succeeded”) over memorised buzzwords.

## High-frequency themes

| Theme | What interviewers listen for | Study |
|-------|------------------------------|-------|
| Shared responsibility | Concrete EC2/S3/Lambda examples | [Module 1](../aws-fundamentals-and-global-infrastructure.md) |
| IAM + STS | Trust vs permissions; deny wins; OIDC for CI | [Module 2](../iam-identity-access-and-organizations.md) |
| VPC path | Public vs private; SG vs NACL; endpoints vs NAT | [Module 3](../vpc-networking-on-aws.md) |
| Compute scale | AMI/LT/ASG; ALB vs NLB; IMDSv2 | [Module 4](../compute-ec2-asg-and-load-balancing.md) |
| Storage | BPA, policies, classes, EBS vs EFS | [Module 5](../storage-s3-ebs-efs.md) |
| Data | Multi-AZ RDS vs replicas; DynamoDB keys | [Module 6](../databases-on-aws.md) |
| Containers | ECS vs EKS vs Fargate trade-offs | [Module 7](../containers-ecs-eks-ecr.md) |
| Serverless | Events, retries, IAM for functions | [Module 8](../serverless-on-aws.md) |
| Ops | CloudWatch vs CloudTrail vs Config | [Module 9](../monitoring-and-observability-on-aws.md) |
| Security | KMS keys, secrets, GuardDuty/Security Hub | [Module 10](../aws-security-services.md) |
| IaC | State/drift; CFN vs Terraform vs CDK | [Module 11](../infrastructure-as-code-on-aws.md) |
| CI/CD | OIDC; blue/green; CodeBuild vs Actions | [Module 12](../cicd-on-aws.md) |
| Cost | SP/RI/Spot; Budgets; NAT waste | [Module 13](../cost-optimisation-on-aws.md) |
| DR | RTO/RPO; backup vs multi-Region | [Module 14](../reliability-and-disaster-recovery.md) |
| Landing zones | Multi-account; SCP ceilings | [Module 15](../production-aws-landing-zones.md) |
| Triage | Identity vs network vs app | [Module 16](../troubleshooting-aws.md) |

## Story bank (from course labs)

Practise a two-minute narration for each:

1. **Budget before compute** — Module 1 guardrail
2. **Least-privilege AssumeRole** — Module 2 deny/allow files
3. **Missing `0.0.0.0/0` route** — Module 3 break/fix
4. **SG revoke took down HTTP** — Module 4 / 16 curl evidence
5. **Bucket policy denied GetObject** — Module 5
6. **DynamoDB wrong PK returned empty** — Module 6 (not an error)
7. **ECR push + task definition** — Module 7 (why not full EKS in a lab)
8. **Lambda Function URL failure in logs** — Module 8
9. **Alarm ALARM→OK on custom metric** — Module 9
10. **SSE-KMS object get proof** — Module 10

## Standalone deep labs

- [IAM and VPC Reachability Triage](../../labs/aws-iam-vpc-triage.md)
- [SSM Session Manager and S3](../../labs/aws-ssm-s3.md)

## Academy catalog

Browse shared guides in the [Academy interview catalog](../../interview/).
