---
title: Cheat Sheets
description: "AWS cheat sheets and quick references for CLI triage, IAM, VPC, and cost hygiene."
technology_id: aws
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - cheatsheets
comments: false
---

# AWS — Cheat Sheets

## Always-first triage

``` {.bash .ra-terminal title="Terminal"}
export AWS_PAGER=""
aws sts get-caller-identity
aws configure get region
echo "AWS_REGION=${AWS_REGION:-}"
```

## Identity vs network

| Symptom | Suspect |
|---------|---------|
| `AccessDenied` / `UnauthorizedOperation` | IAM, SCP, boundary, wrong account |
| TCP timeout / curl hang | SG, NACL, route, public IP, NATGW |
| DNS fail | Route 53 / resolver / private DNS |

## Cost killers to avoid in labs

- NAT Gateway  
- Idle Application Load Balancer  
- Unattached Elastic IP  
- RDS left running  
- Interface VPC endpoints forgotten on  

## Module quick links

Use each tutorial’s Theory tables as the living cheat sheet — especially Modules [2](../iam-identity-access-and-organizations.md), [3](../vpc-networking-on-aws.md), [4](../compute-ec2-asg-and-load-balancing.md), and [16](../troubleshooting-aws.md).

Academy-wide sheets: [Cheat sheets](../../cheatsheets/).
