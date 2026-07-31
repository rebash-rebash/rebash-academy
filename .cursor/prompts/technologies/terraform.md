# Technology Definition

## Course

Terraform for Cloud & DevOps Engineers

---

## Description

A production-focused Terraform course designed for Cloud Engineers, DevOps Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches Infrastructure as Code (IaC) using Terraform, progressing from the basics to enterprise-scale infrastructure management, reusable modules, testing, CI/CD integration and multi-cloud deployments.

Learners should finish the course capable of designing, deploying and managing production cloud infrastructure using Terraform.

---

## Target Roles

- Cloud Engineer
- DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- Infrastructure Engineer
- DevSecOps Engineer

---

## Difficulty

Intermediate → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

- Linux Fundamentals
- Networking Fundamentals
- Git & GitHub
- Docker
- Basic Cloud Knowledge

---

## MCP Servers

Primary

- Terraform

Optional

- AWS
- Azure
- Google Cloud
- Kubernetes
- Context7
- GitHub

---

# Modules

## Module 1 — Infrastructure as Code Fundamentals

- What is Infrastructure as Code?
- Imperative vs Declarative
- Why Terraform?
- Terraform Workflow
- Terraform Architecture

---

## Module 2 — Installing Terraform

- Installation
- CLI
- Terraform Version Management
- Provider Installation
- Terraform Registry

---

## Module 3 — Terraform Basics

- terraform init
- terraform plan
- terraform apply
- terraform destroy
- terraform validate
- terraform fmt

---

## Module 4 — HCL Fundamentals

- Blocks
- Arguments
- Expressions
- Variables
- Outputs
- Locals
- Functions

---

## Module 5 — Providers

- Provider Configuration
- Multiple Providers
- Aliases
- Provider Versioning
- Authentication

---

## Module 6 — Resources

- Resource Lifecycle
- Dependencies
- Meta Arguments
- count
- for_each
- lifecycle
- depends_on

---

## Module 7 — Variables & Outputs

- Input Variables
- Variable Validation
- tfvars
- Environment Variables
- Outputs
- Sensitive Values

---

## Module 8 — State Management

- Local State
- Remote State
- State Locking
- State Commands
- State Security
- Drift Detection

---

## Module 9 — Modules

- Creating Modules
- Module Registry
- Reusable Modules
- Module Versioning
- Module Testing

---

## Module 10 — Expressions & Functions

- Conditional Expressions
- Loops
- Dynamic Blocks
- Built-in Functions
- for Expressions

---

## Module 11 — Data Sources

- Data Sources
- Remote Data
- External Data
- Existing Infrastructure

---

## Module 12 — Workspaces

- Terraform Workspaces
- Environment Separation
- Development
- Staging
- Production

---

## Module 13 — Terraform Cloud & Enterprise

- Terraform Cloud
- Workspaces
- Runs
- Policies
- Remote Execution
- Teams

---

## Module 14 — Testing & Validation

- terraform validate
- terraform test
- Terratest
- Policy Validation
- Static Analysis

---

## Module 15 — Security

- Secret Management
- Sensitive Variables
- Vault Integration
- IAM Best Practices
- State Encryption
- Policy as Code

---

## Module 16 — CI/CD

- GitHub Actions
- GitLab CI
- Azure DevOps
- Jenkins
- Atlantis
- Automated Plans

---

## Module 17 — Multi-Cloud Infrastructure

### AWS

- VPC
- EC2
- IAM
- S3

### Azure

- Resource Groups
- Virtual Networks
- Virtual Machines

### Google Cloud

- VPC
- Compute Engine
- Cloud Storage

---

## Module 18 — Kubernetes Infrastructure

- Managed Clusters
- Node Pools
- Kubernetes Provider
- Helm Provider

---

## Module 19 — Production Terraform

- Repository Structure
- Environment Strategy
- Module Strategy
- Versioning
- Upgrade Strategy
- Cost Optimisation
- Disaster Recovery

---

## Module 20 — Troubleshooting

- Provider Errors
- State Corruption
- Dependency Cycles
- Authentication Problems
- Drift
- Locking Issues
- Performance Optimisation

---

# Hands-on Labs

- Install Terraform
- Deploy Local Infrastructure
- Create Variables
- Build Reusable Modules
- Configure Remote State
- Deploy AWS Infrastructure
- Deploy Azure Infrastructure
- Deploy Google Cloud Infrastructure
- Deploy Kubernetes Cluster
- Use Helm Provider
- Integrate Terraform with GitHub Actions
- Manage State Securely
- Detect Infrastructure Drift
- Recover Corrupted State
- Implement Policy Validation

---

# Projects

## Beginner

Deploy a Simple Cloud Environment

---

## Intermediate

Reusable Terraform Module Library

---

## Advanced

Multi-Environment Cloud Platform

---

## Capstone

Production Infrastructure Platform

Features:

- Modular Architecture
- Remote State
- CI/CD
- Multi-Cloud
- Kubernetes Integration
- Security Policies
- Cost Optimisation
- Disaster Recovery
- Automated Validation
- Documentation

---

# Cheat Sheets

Generate:

- Terraform CLI
- HCL Syntax
- Variables
- Modules
- State Commands
- Functions
- Meta Arguments
- Workspaces
- Terraform Cloud
- Troubleshooting

---

# Interview Preparation

Cover:

- Infrastructure as Code
- Terraform Architecture
- Providers
- Modules
- State Management
- Security
- CI/CD
- Multi-Cloud
- Kubernetes Integration
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Terraform tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Terraform Workflow
- Terraform Architecture
- CLI Commands
- HCL Blocks
- Provider Model
- Resources & Meta-Arguments
- Variables Flow
- State Management
- Remote State Backend
- Module Architecture
- Expressions & Functions
- Data Sources
- Workspaces
- HCP Terraform / Cloud
- Testing & Validation
- Security Layers
- CI/CD Pipeline
- Multi-Cloud Deployment
- Kubernetes with Terraform
- Production Repository Structure
- Troubleshooting Ladder

---

# Certifications

Map modules where appropriate to:

- HashiCorp Terraform Associate

---

# Capstone Outcome

After completing this course learners should be able to:

- Design reusable Terraform modules
- Manage infrastructure across multiple clouds
- Secure Terraform deployments
- Build enterprise IaC repositories
- Integrate Terraform into CI/CD
- Manage remote state safely
- Troubleshoot production Terraform environments
- Apply Infrastructure as Code best practices at scale