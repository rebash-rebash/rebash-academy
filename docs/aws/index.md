---
title: Overview
description: "AWS learning track — 20 tutorials from account foundations through VPC, EC2, S3, load balancing, and a three-tier capstone. Free Tier and LocalStack-friendly labs."
difficulty: beginner
estimated_time: "Varies"
author: Shaik Basha
last_updated: "2026-07-28"
category: aws
tags:
  - aws
  - cloud
comments: false
---

# AWS

Amazon Web Services — compute, storage, networking, IAM, and operations for DevOps engineers.

## Overview

The REBASH Academy **AWS** track is a structured, 20-tutorial curriculum. It sits **immediately after [Networking](../networking/index.md)** in the [DevOps Engineer path](../learning-paths/devops-engineer.md). Labs support a real **Free Tier** account and, where CLI-shaped, **LocalStack / dry-run** alternatives. Every resource you create should be destroyed; create a billing alarm before you launch EC2 or RDS.

!!! tip "Prerequisites"
    Finish [Linux](../linux/index.md) and [Networking](../networking/index.md) first. [Terraform](../terraform/index.md) is the recommended follow-on to automate what you learn here — it is not required for Module 1.

!!! warning "Cost hygiene"
    Free Tier has limits. **NAT Gateways**, idle **ALBs**, and **RDS** are common bill surprises. Prefer SSM Session Manager over public SSH, avoid NAT in mandatory labs, and destroy resources at the end of every session.

## Curriculum Plan

<figure class="rebash-diagram rebash-tree-diagram" markdown="0">

<p class="rebash-tree-title">AWS Track</p>

<ul class="rebash-tree">
  <li>1 · Foundations
<ul>
  <li>Introduction to AWS and Global Infrastructure</li>
  <li>Accounts, Free Tier, Billing, and Cost Hygiene</li>
  <li>IAM Fundamentals</li>
  <li>AWS CLI, Credentials, and Profiles</li>
</ul></li>
  <li>2 · VPC Networking
<ul>
  <li>VPC, Subnets, and Multi-AZ Design</li>
  <li>Internet Gateways, Routes, and Egress</li>
  <li>Security Groups and NACLs</li>
  <li>VPC Endpoints and Private AWS Access</li>
</ul></li>
  <li>3 · Compute
<ul>
  <li>EC2 Fundamentals</li>
  <li>User Data, IMDS, and SSM Session Manager</li>
  <li>EBS Volumes, Snapshots, and Encryption</li>
</ul></li>
  <li>4 · Storage
<ul>
  <li>S3 Fundamentals</li>
  <li>S3 Security and Static Hosting</li>
</ul></li>
  <li>5 · Edge and Data
<ul>
  <li>Elastic Load Balancing (ALB and NLB)</li>
  <li>Route 53 DNS and Health Checks</li>
  <li>RDS Fundamentals</li>
  <li>Auto Scaling Groups and Launch Templates</li>
</ul></li>
  <li>6 · Ops and Capstone
<ul>
  <li>CloudWatch Metrics, Logs, and Alarms</li>
  <li>CloudTrail, Config, and Account Guardrails</li>
  <li>Lambda and Three-Tier Capstone</li>
</ul></li>
</ul>
</figure>

### Module 1 – Foundations

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 1 | [Introduction to AWS and Global Infrastructure](introduction-to-aws-and-global-infrastructure.md) | Beginner | 35 min |
| 2 | [Accounts, Free Tier, Billing, and Cost Hygiene](accounts-free-tier-billing-and-cost-hygiene.md) | Beginner | 40 min |
| 3 | [IAM Fundamentals](iam-fundamentals.md) | Beginner | 50 min |
| 4 | [AWS CLI, Credentials, and Profiles](aws-cli-credentials-and-profiles.md) | Beginner | 40 min |

### Module 2 – VPC Networking

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 5 | [VPC, Subnets, and Multi-AZ Design](vpc-subnets-and-multi-az-design.md) | Intermediate | 50 min |
| 6 | [Internet Gateways, Routes, and Egress](internet-gateways-routes-and-egress.md) | Intermediate | 45 min |
| 7 | [Security Groups and NACLs](security-groups-and-nacls.md) | Intermediate | 45 min |
| 8 | [VPC Endpoints and Private AWS Access](vpc-endpoints-and-private-aws-access.md) | Intermediate | 45 min |

### Module 3 – Compute

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 9 | [EC2 Fundamentals](ec2-fundamentals.md) | Intermediate | 50 min |
| 10 | [User Data, IMDS, and SSM Session Manager](user-data-imds-and-ssm-session-manager.md) | Intermediate | 55 min |
| 11 | [EBS Volumes, Snapshots, and Encryption](ebs-volumes-snapshots-and-encryption.md) | Intermediate | 45 min |

### Module 4 – Storage

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 12 | [S3 Fundamentals](s3-fundamentals.md) | Beginner | 45 min |
| 13 | [S3 Security and Static Hosting](s3-security-and-static-hosting.md) | Intermediate | 50 min |

### Module 5 – Edge and Data

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 14 | [Elastic Load Balancing — ALB and NLB](elastic-load-balancing-alb-and-nlb.md) | Intermediate | 55 min |
| 15 | [Route 53 DNS and Health Checks](route-53-dns-and-health-checks.md) | Intermediate | 45 min |
| 16 | [RDS Fundamentals](rds-fundamentals.md) | Intermediate | 50 min |
| 17 | [Auto Scaling Groups and Launch Templates](auto-scaling-groups-and-launch-templates.md) | Intermediate | 50 min |

### Module 6 – Ops and Capstone

| # | Tutorial | Level | Time |
|---|----------|-------|------|
| 18 | [CloudWatch Metrics, Logs, and Alarms](cloudwatch-metrics-logs-and-alarms.md) | Intermediate | 45 min |
| 19 | [CloudTrail, Config, and Account Guardrails](cloudtrail-config-and-account-guardrails.md) | Advanced | 50 min |
| 20 | [Lambda and Three-Tier Capstone](lambda-and-three-tier-capstone.md) | Advanced | 60 min |

**Total estimated time:** ~15 hours of hands-on learning

## Learning Objectives

After completing this track, you will be able to:

- [ ] Navigate Regions, AZs, and the shared responsibility model
- [ ] Secure an account with MFA, IAM roles, and billing alarms
- [ ] Design multi-AZ VPCs with security groups and private API access
- [ ] Run EC2 with SSM (not public SSH) and manage EBS safely
- [ ] Use S3 with Block Public Access and understand static hosting patterns
- [ ] Explain ALB vs NLB, Route 53, RDS basics, and Auto Scaling
- [ ] Use CloudWatch and CloudTrail for operations and audit
- [ ] Sketch a three-tier architecture and hand off to Terraform

## Who Is This For?

| Audience | Benefit |
|----------|---------|
| **DevOps / SRE** | Operate AWS the way production teams do — IAM, VPC, evidence-first triage |
| **Cloud engineers** | Build Free Tier labs without surprise bills |
| **Developers** | Understand where apps, load balancers, and data stores live |
| **Students** | Job-ready AWS fundamentals after Networking |

## Related Sections

- [Networking](../networking/index.md) — VPC concepts before AWS specifics
- [Linux](../linux/index.md) — host skills for EC2
- [Terraform](../terraform/index.md) — automate this track next
- [AWS Cheat Sheet](../cheatsheets/aws.md)
- [AWS Interview Prep](../interview/aws.md)
- [AWS Fundamentals Quiz](../quizzes/aws-fundamentals.md)
- Labs: [IAM + VPC Triage](../labs/aws-iam-vpc-triage.md) · [SSM + S3](../labs/aws-ssm-s3.md)
- [DevOps Engineer path](../learning-paths/devops-engineer.md)
