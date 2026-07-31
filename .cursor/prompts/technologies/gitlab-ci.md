# Technology Definition

## Course

GitLab CI/CD for Cloud & DevOps Engineers

---

## Description

A production-focused GitLab CI/CD course designed for DevOps Engineers, Cloud Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches GitLab CI/CD from pipeline fundamentals through enterprise automation, Infrastructure as Code, Kubernetes deployments, security scanning, GitOps and release management.

Learners should finish the course capable of designing, building and operating enterprise CI/CD platforms using GitLab.

---

## Target Roles

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer

---

## Difficulty

Intermediate → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

- Git & GitHub Fundamentals
- Docker
- Kubernetes
- Terraform
- Basic Cloud Knowledge

---

## MCP Servers

Primary

- GitHub
- Context7

Optional

- Kubernetes
- Terraform
- AWS
- Azure
- Google Cloud

---

# Modules

## Module 1 — GitLab CI/CD Fundamentals

- CI/CD Concepts
- GitLab Architecture
- Pipelines
- Stages
- Jobs
- Runners
- GitLab Editions

---

## Module 2 — GitLab Projects

- Repositories
- Branches
- Merge Requests
- Protected Branches
- Tags
- Releases

---

## Module 3 — GitLab Runners

- Shared Runners
- Group Runners
- Project Runners
- Shell Executor
- Docker Executor
- Kubernetes Executor
- Autoscaling Runners

---

## Module 4 — Pipeline Syntax

- .gitlab-ci.yml
- Variables
- Rules
- only / except
- workflow
- needs
- dependencies

---

## Module 5 — Pipeline Design

- Multi-stage Pipelines
- DAG Pipelines
- Parent Child Pipelines
- Multi-project Pipelines
- Dynamic Pipelines
- Includes

---

## Module 6 — Variables & Secrets

- CI Variables
- Masked Variables
- Protected Variables
- Environment Variables
- Vault Integration
- OIDC

---

## Module 7 — Artifacts & Cache

- Artifacts
- Reports
- Dependency Cache
- Build Cache
- Expiration
- Sharing Artifacts

---

## Module 8 — Docker Pipelines

- Docker Builds
- BuildKit
- Multi-stage Images
- Docker Registry
- GitLab Container Registry
- Image Promotion

---

## Module 9 — Kubernetes Deployments

- GitLab Agent
- kubectl
- Helm
- Canary Deployments
- Blue/Green Deployments
- Rollbacks

---

## Module 10 — Terraform Pipelines

- Terraform Init
- Validate
- Plan
- Apply
- Destroy
- State Management

---

## Module 11 — Cloud Deployments

### AWS

- IAM
- EKS
- ECS

### Azure

- AKS
- Azure Login

### Google Cloud

- GKE
- Cloud Run

---

## Module 12 — DevSecOps

- SAST
- DAST
- Dependency Scanning
- Secret Detection
- Container Scanning
- License Compliance
- SBOM

---

## Module 13 — Testing

- Unit Tests
- Integration Tests
- End-to-End Tests
- Performance Tests
- Parallel Jobs

---

## Module 14 — Release Management

- Git Tags
- Releases
- Release Automation
- Semantic Versioning
- Changelogs

---

## Module 15 — Production Pipelines

- Environment Promotion
- Manual Approvals
- Protected Environments
- Rollback Strategy
- Progressive Delivery
- Feature Flags

---

## Module 16 — Monitoring & Observability

- Pipeline Analytics
- Job Logs
- Pipeline Metrics
- Runner Metrics
- Notifications

---

## Module 17 — Troubleshooting

- Failed Jobs
- Runner Issues
- Pipeline Debugging
- Authentication Problems
- Cache Problems
- Performance Issues

---

## Module 18 — Enterprise GitLab

- GitLab Groups
- Permissions
- Compliance Pipelines
- Governance
- Self-managed GitLab
- Backup & Restore

---

# Hands-on Labs

- Install GitLab Runner
- Configure Docker Executor
- Configure Kubernetes Executor
- Build Your First Pipeline
- Build Multi-stage Pipelines
- Configure Parent/Child Pipelines
- Build Docker Images
- Push to GitLab Registry
- Deploy to Kubernetes
- Deploy Infrastructure with Terraform
- Configure Security Scanning
- Configure GitLab Agent
- Deploy to AWS
- Deploy to Azure
- Deploy to Google Cloud
- Implement Progressive Delivery
- Troubleshoot Production Pipelines

---

# Projects

## Beginner

Python CI Pipeline

---

## Intermediate

Container Deployment Pipeline

---

## Advanced

Enterprise GitLab Platform

---

## Capstone

Production GitLab CI/CD Platform

Features:

- Autoscaling Runners
- Kubernetes Executor
- GitLab Agent
- Terraform Automation
- Multi-Cloud Deployments
- Security Scanning
- Release Automation
- GitOps Integration
- Monitoring
- Disaster Recovery

---

# Cheat Sheets

Generate:

- .gitlab-ci.yml
- Pipeline Keywords
- Rules
- Variables
- Runners
- Docker Executor
- Kubernetes Executor
- Terraform Pipelines
- GitLab Agent
- Troubleshooting

---

# Interview Preparation

Cover:

- GitLab Architecture
- Runner Types
- Pipeline Design
- GitLab Agent
- Kubernetes Deployments
- Terraform Pipelines
- Security
- Enterprise GitLab
- GitOps
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for GitLab CI tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- GitLab Architecture
- Pipeline Flow
- Runner Architecture
- Projects · MRs · Releases
- Pipeline Syntax
- Parent/Child Pipelines
- Variables & Secrets
- Artifacts & Cache
- Docker Pipelines
- Kubernetes Deployment
- GitLab Agent
- Terraform Pipelines
- Multi-Cloud Deployments
- DevSecOps Scanning
- Testing in Pipelines
- Release Management
- Production Promotion
- Pipeline Observability
- Troubleshooting Ladder
- Enterprise GitLab Platform
- GitOps Workflow

---

# Certifications

Map modules where appropriate to:

- GitLab Certified CI/CD Associate
- GitLab Certified DevOps Professional

---

# Capstone Outcome

After completing this course learners should be able to:

- Design enterprise GitLab pipelines
- Build reusable CI/CD templates
- Operate GitLab Runners
- Deploy to Kubernetes
- Automate Terraform workflows
- Build secure DevSecOps pipelines
- Implement GitOps workflows
- Operate enterprise GitLab platforms