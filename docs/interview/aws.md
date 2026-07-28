---
title: "AWS Interview Prep"
description: "Interview themes and practice strategy for the REBASH Academy AWS track."
difficulty: intermediate
estimated_time: "30 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: interview
tags:
  - interview
  - aws
comments: false
---

# AWS Interview Prep

Use this page as a revision map. Every tutorial in the [AWS track](../aws/index.md) already ends with interview questions — work those first, then stress-test the themes below.

## How to practise

1. Answer out loud in two minutes without notes
2. Draw the VPC, IAM, and data flow on a whiteboard
3. Name the failure mode and the first three AWS CLI commands
4. Tie the topic to cost, security, and the shared responsibility model

## High-yield themes

- IAM users vs roles vs instance profiles
- Shared responsibility model (AWS vs customer)
- Public vs private subnets and routing (IGW vs NAT)
- Security groups vs NACLs — stateful vs stateless
- SSM Session Manager vs bastion SSH
- S3 Block Public Access and bucket policies
- ALB vs NLB selection and health checks
- RDS cost, Multi-AZ, and backup windows
- CloudWatch metrics vs logs vs alarms
- CloudTrail for API audit and `AccessDenied` triage
- Free Tier hygiene and billing surprises (NAT, ALB, RDS)
- First-hour unreachable app: IAM deny vs SG vs route table

## Hands-on prompts interviewers love

- Walk through [IAM and VPC Triage](../labs/aws-iam-vpc-triage.md) as if it were a production incident
- Explain how you would administer EC2 with no port 22 open ([SSM and S3 lab](../labs/aws-ssm-s3.md))
- Compare two designs: NAT Gateway vs VPC endpoints for private S3 access
- Defend a trade-off: ALB path routing vs separate NLB for TCP workload

## Related

- Track: [AWS](../aws/index.md)
- Cheat sheet: [AWS cheat sheet](../cheatsheets/aws.md)
- Quiz: [AWS Fundamentals](../quizzes/aws-fundamentals.md)
- Lab: [IAM and VPC Triage](../labs/aws-iam-vpc-triage.md)
- Lab: [SSM and S3](../labs/aws-ssm-s3.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
