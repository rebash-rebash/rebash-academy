# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

Helm for Kubernetes Engineers

---

## Description

A production-focused Helm course designed for Kubernetes Administrators, DevOps Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches Helm from the basics of package management through enterprise chart development, release management and GitOps integration.

Learners should finish the course capable of creating, maintaining and deploying production-grade Helm charts.

---

## Target Roles

- Kubernetes Administrator
- DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Cloud Engineer

---

## Difficulty

Intermediate

---

## Estimated Duration

3–4 Weeks

---

## Prerequisites

- Linux Fundamentals
- Git & GitHub
- Docker
- Kubernetes

---

## MCP Servers

Primary

- Kubernetes

Optional

- Context7
- GitHub

---

# Modules

## Module 1 — Helm Fundamentals

- What is Helm?
- Why Helm?
- Helm Architecture
- Helm Components
- Helm Repositories

---

## Module 2 — Installing Helm

- Installation
- Repository Configuration
- Helm CLI
- Plugin System

---

## Module 3 — Working with Charts

- Chart Structure
- Chart.yaml
- values.yaml
- templates/
- charts/
- helpers.tpl

---

## Module 4 — Templates

- Go Templates
- Variables
- Pipelines
- Functions
- Conditional Logic
- Loops
- Includes
- Named Templates

---

## Module 5 — Values

- values.yaml
- Default Values
- Override Values
- Environment Values
- Secrets

---

## Module 6 — Chart Dependencies

- Dependencies
- Library Charts
- OCI Charts
- Version Constraints
- Repository Management

---

## Module 7 — Releases

- Install
- Upgrade
- Rollback
- History
- Diff
- Atomic Deployments

---

## Module 8 — Testing & Validation

- helm lint
- helm template
- helm test
- Dry Runs
- Debugging

---

## Module 9 — Security

- Secrets
- RBAC
- Image Policies
- Signed Charts
- OCI Registries

---

## Module 10 — GitOps Integration

- Helm + Argo CD
- Helm + Flux
- Progressive Delivery
- Multi-environment Deployments

---

## Module 11 — Production Helm

- Chart Versioning
- Semantic Versioning
- Reusable Charts
- Enterprise Chart Structure
- Best Practices

---

## Module 12 — Troubleshooting

- Template Errors
- Failed Releases
- Rollback Failures
- Upgrade Problems
- Dependency Issues

---

# Hands-on Labs

- Install Helm
- Create Your First Chart
- Deploy an Application
- Configure Values
- Build Reusable Templates
- Package a Chart
- Publish a Chart
- Deploy with Argo CD
- Rollback a Release
- Troubleshoot Failed Deployments

---

# Projects

## Beginner

Deploy an NGINX Helm Chart

---

## Intermediate

Build a Reusable Application Chart

---

## Advanced

Enterprise Helm Chart Library

---

## Capstone

Production Helm Platform

Features:

- OCI Registry
- Versioned Charts
- Reusable Templates
- Multi-environment Deployments
- GitOps Integration
- Automated Testing
- Security Validation
- Documentation

---

# Cheat Sheets

Generate:

- Helm CLI
- Chart Structure
- Template Functions
- Values
- Release Management
- OCI Charts
- GitOps
- Troubleshooting

---

# Interview Preparation

Cover:

- Helm Architecture
- Chart Structure
- Template Engine
- Release Management
- Dependencies
- GitOps
- Security
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Helm tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate polished diagrams for:

- Helm Architecture
- Chart Structure
- Template Rendering
- Release Lifecycle
- Values Override Flow
- Chart Dependencies
- OCI Registry
- GitOps Workflow

---

# Certifications

Map modules where appropriate to:

- CKA
- CKAD
- KCNA

---

# Capstone Outcome

After completing this course learners should be able to:

- Create production-ready Helm charts
- Manage application releases
- Build reusable chart libraries
- Integrate Helm with GitOps
- Troubleshoot Helm deployments
- Manage enterprise Kubernetes applications