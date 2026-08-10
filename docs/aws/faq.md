---
title: FAQ
description: "Frequently asked questions for the AWS for Cloud & DevOps Engineers course — accounts, cost, labs, certifications, and interview prep."
technology_id: aws
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - faq
comments: false
---

# AWS — FAQ

## I am a fresher / college graduate with no AWS experience. Can I follow this?

Yes — that is the primary audience. Modules start with a real-world problem and a simple analogy before AWS jargon. You should know basic Linux terminal use and what an IP address roughly is ([Linux](../linux/index.md), [Networking](../networking/index.md)). You do **not** need prior cloud jobs.

## Do I need a paid AWS account?

A Free Tier-eligible account is enough for most labs. Modules that touch Budgets, EC2, S3, DynamoDB, Lambda, CodeBuild, and CloudWatch stay cheap if you **destroy resources the same day**. Avoid NAT Gateways, always-on ALBs, and RDS unless you accept the cost.

## Will labs create real billable resources?

Yes — by design. Interview-ready practice means `create` → prove → (break/fix) → `delete`. Module 1 creates a budget/alarm first so surprises are visible. Always run each module’s **Cleanup** section.

## Can I use LocalStack instead of AWS?

LocalStack helps for some API drills (STS, basic IAM/S3). VPC reachability, public `curl` to EC2, and several managed services need a **real account** (or LocalStack Pro features we do not assume). Prefer a sandbox AWS account for this course.

## What Region should I use?

Pick one home Region (for example `eu-west-2` or `us-east-1`) and export `AWS_REGION` for every lab. Billing metrics and some global quirks still involve `us-east-1` — Module 1 explains when.

## How does this map to certifications?

| Goal | Course emphasis |
|------|-----------------|
| Cloud Practitioner | Modules 1–2, 13, shared responsibility |
| Solutions Architect – Associate | Modules 3–8, 14, Well-Architected themes |
| SysOps / DevOps | Modules 9–12, 16, IAM + automation |
| Security Specialty themes | Modules 2, 10, 15 |

See Certification mapping.

## I am stuck on AccessDenied — what first?

1. `aws sts get-caller-identity`
2. Confirm Region
3. Decide: IAM deny vs network timeout (different symptoms)
4. Use [Module 16](troubleshooting-aws.md) and the [IAM/VPC triage lab](../labs/aws-iam-vpc-triage.md)

## Do I need Terraform and Kubernetes first?

Helpful, not blocking. Module 7 uses Docker + ECR (not a full EKS cluster). Module 11 uses CloudFormation in-lab and discusses Terraform/CDK. Take the [Terraform](../terraform/index.md) and [Kubernetes](../kubernetes/index.md) courses in parallel if you can.

## How should I revise for interviews?

For each module: redraw the Architecture diagram from memory, re-run or narrate the lab evidence, then answer all Interview Questions without looking. Keep a one-page cheat sheet of deny/allow and packet-path stories.
