# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

GitHub Actions for Cloud & DevOps Engineers

---

## Description

A production-focused GitHub Actions course designed for DevOps Engineers, Cloud Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches GitHub Actions from the fundamentals through enterprise CI/CD, Infrastructure as Code, Kubernetes deployments, container pipelines, security scanning and GitOps.

Learners should finish the course capable of designing, building and maintaining production CI/CD pipelines.

---

## Target Roles

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Software Engineer

---

## Difficulty

Intermediate → Advanced

---

## Estimated Duration

6–8 Weeks

---

## Prerequisites

- Git & GitHub
- Docker
- Kubernetes
- Terraform
- Basic Cloud Knowledge

---

## MCP Servers

Primary

- GitHub

Optional

- Kubernetes
- Terraform
- Context7
- AWS
- Azure
- Google Cloud

---

# Modules

## Module 1 — CI/CD Fundamentals

- What is CI?
- What is CD?
- Continuous Delivery
- Continuous Deployment
- GitHub Actions Overview
- Workflow Lifecycle

---

## Module 2 — GitHub Actions Basics

- Workflow Files
- Events
- Jobs
- Steps
- Actions
- Expressions
- Variables

---

## Module 3 — Runners

- GitHub Hosted Runners
- Self-hosted Runners
- Runner Groups
- Labels
- Autoscaling

---

## Module 4 — Workflow Syntax

- YAML
- Matrix Builds
- Conditional Execution
- Inputs
- Outputs
- Reusable Workflows

---

## Module 5 — Secrets & Variables

- Repository Secrets
- Environment Secrets
- Organization Secrets
- Variables
- OIDC Authentication

---

## Module 6 — Artifacts & Caching

- Upload Artifacts
- Download Artifacts
- Cache Dependencies
- Cache Strategies

---

## Module 7 — Docker Pipelines

- Build Images
- Multi-stage Builds
- Buildx
- Multi-Architecture Images
- Push to Registries

---

## Module 8 — Kubernetes Deployments

- Deploy to Kubernetes
- Helm
- kubectl
- Rollbacks
- Deployment Validation

---

## Module 9 — Terraform Pipelines

- Init
- Validate
- Plan
- Apply
- Destroy
- Remote State

---

## Module 10 — Cloud Deployments

### AWS

- IAM Authentication
- OIDC
- ECS
- EKS

### Azure

- Service Principal
- AKS

### Google Cloud

- Workload Identity
- GKE
- Cloud Run

---

## Module 11 — Security

- Secret Scanning
- Dependency Review
- CodeQL
- Trivy
- SBOM
- Supply Chain Security

---

## Module 12 — Testing

- Unit Testing
- Integration Testing
- Smoke Tests
- End-to-End Testing
- Parallel Execution

---

## Module 13 — Release Management

- Semantic Versioning
- Git Tags
- GitHub Releases
- Changelogs
- Automated Releases

---

## Module 14 — Reusable Components

- Composite Actions
- Reusable Workflows
- Marketplace Actions
- Internal Actions

---

## Module 15 — Production Pipelines

- Multi-Environment Deployments
- Manual Approvals
- Protected Environments
- Rollback Strategy
- Blue/Green Deployments
- Canary Deployments

---

## Module 16 — Troubleshooting

- Failed Jobs
- Runner Problems
- Authentication Issues
- Cache Problems
- Deployment Failures
- Performance Optimisation

---

# Hands-on Labs

- Build Your First Workflow
- Configure Matrix Builds
- Build Docker Images
- Publish Images to GHCR
- Deploy to Kubernetes
- Deploy Infrastructure with Terraform
- Deploy to AWS
- Deploy to Azure
- Deploy to Google Cloud
- Configure OIDC Authentication
- Implement Security Scanning
- Create Reusable Workflows
- Configure Self-hosted Runners
- Automate Releases
- Troubleshoot Failed Pipelines

---

# Projects

## Beginner

CI Pipeline for a Python Application

---

## Intermediate

Multi-Environment Deployment Pipeline

---

## Advanced

Enterprise GitHub Actions Platform

---

## Capstone

Production CI/CD Platform

Features:

- Reusable Workflows
- Self-hosted Runners
- OIDC Authentication
- Multi-Cloud Deployments
- Kubernetes Deployments
- Terraform Automation
- Security Scanning
- Release Automation
- Notifications
- Rollback Strategy

---

# Cheat Sheets

Generate:

- Workflow Syntax
- GitHub Expressions
- Secrets
- Matrix Builds
- Docker Pipelines
- Terraform Pipelines
- Kubernetes Deployment
- OIDC
- Composite Actions
- Troubleshooting

---

# Interview Preparation

Cover:

- CI/CD Concepts
- Workflow Design
- GitHub Actions
- Self-hosted Runners
- Security
- Kubernetes Deployments
- Terraform Integration
- Release Management
- Multi-Cloud
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for GitHub Actions tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

**Critical for MkDocs:** wrap every workflow YAML sample that contains `${{ ... }}` in `{% raw %}...{% endraw %}` so mkdocs-macros does not treat expressions as Jinja.

Generate diagrams for:

- GitHub Actions Architecture
- Workflow Lifecycle
- Workflow Building Blocks
- Runner Architecture
- Workflow Syntax Power Tools
- Secrets, Variables & OIDC
- Artifacts & Caching
- Docker Build Pipeline
- Kubernetes Deployment Pipeline
- Terraform Pipeline
- Multi-Cloud with OIDC
- Security & Supply Chain
- Testing in Actions
- Release Pipeline
- Reusable Components
- Enterprise CI/CD Promotion
- Troubleshooting Ladder
- Enterprise Actions Platform

---

# Certifications

Map modules where appropriate to:

- GitHub Foundations
- GitHub Actions
- GitHub Administration

---

# Capstone Outcome

After completing this course learners should be able to:

- Design enterprise CI/CD pipelines
- Build reusable GitHub Actions workflows
- Deploy applications to Kubernetes
- Automate infrastructure with Terraform
- Deploy to AWS, Azure and Google Cloud
- Secure software delivery pipelines
- Operate self-hosted runners
- Implement production CI/CD best practices