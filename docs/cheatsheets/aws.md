---
title: "AWS Cheat Sheet"
description: "Quick-reference commands and patterns for the REBASH Academy AWS track."
difficulty: beginner
estimated_time: "10 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: cheatsheets
tags:
  - cheatsheets
  - aws
comments: false
---

# AWS Cheat Sheet

Scannable commands and patterns for the [AWS track](../aws/index.md). Prefer the full tutorials when you need *why*, not only *how*.

## Quick reference

| Area | Commands / notes |
|------|------------------|
| IAM | Users, groups, roles, policies; least privilege; `sts:AssumeRole`; instance profiles for EC2 |
| CLI identity | `aws sts get-caller-identity`; profiles in `~/.aws/config`; SSO `aws sso login` |
| Billing / Free Tier | Billing alarm; Cost Explorer; destroy same day; watch NAT, ALB, RDS, idle EIPs |
| VPC | CIDR, subnets (public vs private), route tables, IGW, NAT (costly) |
| SG vs NACL | SG = stateful, instance ENI; NACL = stateless, subnet boundary; SG first in triage |
| EC2 / SSM | `run-instances`; no public SSH; SSM agent + `AmazonSSMManagedInstanceCore`; `aws ssm start-session` |
| IMDS | `169.254.169.254`; prefer IMDSv2; role creds via instance profile |
| S3 | `aws s3 cp/sync/ls`; Block Public Access; bucket policies; SSE-S3 / SSE-KMS |
| ELB | ALB = L7 HTTP(S), path routing; NLB = L4 TCP/UDP, static IP; health checks on app path |
| Route 53 | Hosted zones, A/AAAA/CNAME, alias to ALB; health checks + failover routing |
| RDS | Multi-AZ vs read replica; storage autoscaling; **always** a cost landmine in labs |
| ASG | Launch template, desired/min/max, health check grace, target tracking policies |
| CloudWatch | Metrics, log groups, alarms; `PutMetricAlarm`; agent on EC2 for mem/disk |
| CloudTrail | API audit trail; org trail; `AccessDenied` events for IAM triage |
| Cost landmines | NAT Gateway hourly + data; idle ALB; RDS storage; public IPv4; forgotten EBS snapshots |

## Common mistakes

- Opening SSH `0.0.0.0/0` instead of using SSM
- Confusing IAM `AccessDenied` with network unreachable
- Leaving NAT Gateway or ALB running in a lab VPC
- Skipping Block Public Access on new buckets
- Using root account access keys

## Related

- Track: [AWS](../aws/index.md)
- Start: [Introduction to AWS](../aws/introduction-to-aws-and-global-infrastructure.md)
- Lab: [IAM and VPC Triage](../labs/aws-iam-vpc-triage.md)
- Lab: [SSM and S3](../labs/aws-ssm-s3.md)
- Quiz: [AWS Fundamentals](../quizzes/aws-fundamentals.md)
- Interview bank: [AWS interview prep](../interview/aws.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
