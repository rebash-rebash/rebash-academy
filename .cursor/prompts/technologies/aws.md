# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

AWS for Cloud & DevOps Engineers

---

## Description

A production-focused Amazon Web Services (AWS) course designed for Cloud Engineers, DevOps Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches AWS from the fundamentals through production architecture, automation, security, operations and cost optimisation.

Learners should finish the course capable of designing, deploying, operating and troubleshooting production AWS environments.

---

## Target Roles

- Cloud Engineer
- DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer
- Solutions Architect

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

12–16 Weeks

---

## Prerequisites

- Linux Fundamentals
- Networking Fundamentals
- Git & GitHub
- Docker
- Kubernetes (Recommended)
- Terraform (Recommended)

---

## MCP Servers

Primary

- AWS

Optional

- Terraform
- Kubernetes
- Context7
- GitHub

---

# Modules

## Module 1 — AWS Fundamentals

- What is AWS?
- Global Infrastructure
- Regions
- Availability Zones
- Edge Locations
- Shared Responsibility Model
- AWS CLI
- CloudShell

---

## Module 2 — Identity & Access Management

- IAM
- Users
- Groups
- Roles
- Policies
- MFA
- STS
- Cross Account Access
- IAM Identity Center
- Organizations

---

## Module 3 — Networking

- Amazon VPC
- CIDR
- Public & Private Subnets
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs
- VPC Peering
- Transit Gateway
- VPC Endpoints
- Route53

---

## Module 4 — Compute

- EC2
- AMIs
- Launch Templates
- Auto Scaling
- Placement Groups
- Elastic IP
- Load Balancers

---

## Module 5 — Storage

- S3
- EBS
- EFS
- FSx
- Storage Classes
- Lifecycle Policies
- Encryption

---

## Module 6 — Databases

- RDS
- Aurora
- DynamoDB
- ElastiCache
- DocumentDB

---

## Module 7 — Containers

- ECS
- EKS
- Fargate
- ECR
- App Runner

---

## Module 8 — Serverless

- Lambda
- API Gateway
- EventBridge
- SNS
- SQS
- Step Functions

---

## Module 9 — Monitoring & Observability

- CloudWatch
- CloudTrail
- AWS Config
- X-Ray
- Health Dashboard
- Systems Manager

---

## Module 10 — Security

- KMS
- Secrets Manager
- Parameter Store
- GuardDuty
- Inspector
- Security Hub
- Macie
- Shield
- WAF

---

## Module 11 — Infrastructure as Code

- Terraform
- CloudFormation
- CDK
- Service Catalog

---

## Module 12 — CI/CD

- CodePipeline
- CodeBuild
- CodeDeploy
- GitHub Actions
- GitLab CI
- Blue/Green Deployments

---

## Module 13 — Cost Optimisation

- Pricing Models
- Cost Explorer
- Budgets
- Savings Plans
- Reserved Instances
- Spot Instances
- Trusted Advisor

---

## Module 14 — Reliability

- High Availability
- Multi-AZ
- Multi-Region
- Disaster Recovery
- AWS Backup
- Well-Architected Framework

---

## Module 15 — Production AWS

- Landing Zones
- Multi-Account Strategy
- Governance
- Tagging
- Operational Excellence
- Security Best Practices
- Automation

---

## Module 16 — Troubleshooting

- EC2 Failures
- IAM Issues
- VPC Connectivity
- DNS Problems
- Storage Issues
- Lambda Failures
- EKS Troubleshooting
- Cost Analysis

---

# Hands-on Labs

- Create an AWS Account
- Configure AWS CLI
- Launch EC2
- Build a Secure VPC
- Host a Static Website on S3
- Configure CloudFront
- Create IAM Roles
- Configure Auto Scaling
- Deploy an RDS Database
- Deploy Lambda Functions
- Deploy ECS Applications
- Deploy an EKS Cluster
- Build Infrastructure with Terraform
- Configure Monitoring
- Implement Disaster Recovery

---

# Projects

## Beginner

Deploy a Static Website

---

## Intermediate

Three-Tier Web Application

---

## Advanced

Production Cloud Platform

---

## Capstone

Production AWS Landing Zone

Features:

- Multi-Account Architecture
- Secure Networking
- IAM Governance
- EKS
- ECS
- CI/CD
- Monitoring
- Logging
- Security
- Backup
- Disaster Recovery
- Cost Optimisation

---

# Cheat Sheets

Generate:

- AWS CLI
- IAM
- VPC
- EC2
- S3
- Lambda
- EKS
- CloudFormation
- Terraform on AWS
- Troubleshooting

---

# Interview Preparation

Cover:

- AWS Fundamentals
- IAM
- VPC
- EC2
- S3
- Containers
- Serverless
- Security
- Well-Architected Framework
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for AWS tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- AWS Global Infrastructure
- IAM Identity Model
- VPC Architecture
- Three-Tier Application
- Compute Building Blocks
- Storage Services
- Databases on AWS
- EKS / ECS Container Platform
- Serverless Architecture
- Observability on AWS
- AWS Security Services
- IaC on AWS
- CI/CD Pipeline
- Cost Optimisation Loop
- Disaster Recovery Strategies
- Landing Zone / Multi-Account
- Production AWS Platform
- Troubleshooting Ladder

---

# Certifications

Map modules where appropriate to:

- AWS Certified Cloud Practitioner
- AWS Certified Solutions Architect – Associate
- AWS Certified Developer – Associate
- AWS Certified SysOps Administrator – Associate
- AWS Certified DevOps Engineer – Professional

---

# Capstone Outcome

After completing this course learners should be able to:

- Design production AWS architectures
- Build secure cloud environments
- Deploy containerised applications
- Implement Infrastructure as Code
- Build CI/CD pipelines
- Secure AWS workloads
- Optimise cloud costs
- Troubleshoot production AWS environments
- Apply the AWS Well-Architected Framework