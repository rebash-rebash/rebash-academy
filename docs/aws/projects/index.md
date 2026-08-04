---
title: Projects
description: "Portfolio projects for the AWS course — static site, three-tier app, and production-minded platform milestones."
technology_id: aws
hide:
  - toc
author: Shaik Basha
last_updated: "2026-08-03"
category: aws
tags:
  - aws
  - projects
comments: false
---

# AWS — Projects

Build these after the matching modules. Prefer **IaC + destroy scripts** and a short README with architecture, cost, and cleanup.

## Beginner — Static website

**After:** Modules 1, 5, 10  

S3 (+ optional CloudFront) static site with Block Public Access patterns appropriate to your design (OAI/OAC vs public website hosting), SSE, and a Budget alarm. Document the URL and teardown.

## Intermediate — Three-tier web app

**After:** Modules 3–6, 9  

Public ALB → ASG (or single EC2 for budget) → data store (RDS only if you accept cost; otherwise DynamoDB). Multi-AZ subnets, SG referencing, CloudWatch alarm on 5xx or CPU. Diagram with Excalidraw.

## Advanced — Deployable platform slice

**After:** Modules 7–12  

ECR image + ECS Fargate **or** EKS (kind locally if AWS EKS cost is too high) + pipeline (CodePipeline/CodeBuild or GitHub Actions OIDC). Include IAM roles, logs, and a rollback note.

## Capstone direction

See [Capstone](../capstone/index.md) for multi-account landing-zone scope.
