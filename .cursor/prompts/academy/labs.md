Create the complete Hands-on Labs section for REBASH Academy.

Follow:

- AGENTS.md
- `.cursor/prompts/CONTENT_QUALITY.md`
- `.cursor/rules/00-foundation/09-content-quality-standard.mdc`
- `.cursor/prompts/tutorials/create_lab.md`
- Material for MkDocs
- Excalidraw diagrams only (not D2/Mermaid)
- Official documentation first
- REBASH Academy standards

Lab design must assume **real-world, copy-paste executable** labs (topic-specific; no note-taking exercises).

Do NOT generate actual lab content.

Generate ONLY the complete Labs section design.

==================================================
GOAL
==================================================

Design a complete Hands-on Labs section that becomes the practical learning area of REBASH Academy.

The Labs section should help learners:

- Practice concepts
- Gain real experience
- Prepare for production environments
- Build confidence
- Complete career paths

The design should scale to thousands of labs.

==================================================
GENERATE
==================================================

Design:

- Repository structure
- MkDocs navigation
- Lab categories
- Lab metadata
- Lab templates
- Difficulty model
- Environment model
- Lab lifecycle
- Learning progression

Do NOT generate individual labs.

==================================================
LAB CATEGORIES
==================================================

Create categories for

Linux

Networking

Shell Scripting

Python

Git

Docker

Kubernetes

Helm

Terraform

Ansible

AWS

Azure

Google Cloud

GitHub Actions

GitLab CI/CD

Jenkins

Argo CD

Flux

Prometheus

Grafana

Loki

Tempo

OpenTelemetry

DevSecOps

Platform Engineering

SRE

Cloud Architecture

AI for DevOps

Each category should contain

Overview

Learning objectives

Lab roadmap

Difficulty progression

Required tutorials

Projects

==================================================
LAB LEVELS
==================================================

Design four levels.

Level 1

Guided Labs

Learner follows instructions.

Level 2

Practice Labs

Partial guidance.

Level 3

Challenge Labs

Problem statement only.

Level 4

Production Labs

Real-world scenarios.

Explain each level.

==================================================
LAB TYPES
==================================================

Design different lab types.

Examples

Quick Lab

Guided Lab

Scenario Lab

Troubleshooting Lab

Challenge Lab

Migration Lab

Performance Lab

Security Lab

Automation Lab

Architecture Lab

Capstone Lab

Explain each.

==================================================
LAB TEMPLATE
==================================================

Design a standard lab template.

Every lab should include

Title

Description

Difficulty

Estimated Time

Prerequisites

Career Paths

Technologies

Learning Objectives

Scenario

Architecture

Tasks

Expected Outcome

Validation Steps

Troubleshooting

Best Practices

Security Considerations

Cleanup Steps

References

==================================================
LAB METADATA
==================================================

Design reusable metadata.

Include

id

title

description

difficulty

estimated_time

technology

module

career_paths

skills

prerequisites

related_tutorials

related_projects

environment

cloud_provider

cost

tags

author

last_updated

==================================================
LAB ENVIRONMENTS
==================================================

Support environments such as

Local Machine

Docker

Virtual Machine

Kind

Minikube

k3d

Kubernetes

AWS

Azure

Google Cloud

GitHub Codespaces

Dev Container

Each lab should define its environment requirements.

==================================================
VALIDATION
==================================================

Every lab should include validation.

Examples

Commands

Expected output

Checklist

Success criteria

Automated verification (where possible)

==================================================
LAB ROADMAP
==================================================

Generate learning progression.

Example

Tutorial

↓

Guided Lab

↓

Practice Lab

↓

Challenge Lab

↓

Project

↓

Capstone

==================================================
PROJECT MAPPING
==================================================

Explain how labs connect to projects.

Example

Terraform Basics

↓

Terraform Lab

↓

Terraform Project

↓

Cloud Landing Zone

==================================================
CAREER PATH MAPPING
==================================================

Every lab should belong to one or more career paths.

Example

Kubernetes Networking Lab

DevOps Engineer

Platform Engineer

SRE

==================================================
MKDOCS NAVIGATION
==================================================

Generate navigation.

Example

Labs

Linux

Networking

Docker

Kubernetes

Terraform

Cloud

CI/CD

Observability

Security

AI

==================================================
REPOSITORY STRUCTURE
==================================================

Generate folders.

Example

docs/

labs/

linux/

networking/

docker/

kubernetes/

terraform/

aws/

azure/

gcp/

cicd/

observability/

security/

platform/

ai/

Each technology contains

index.md

guided/

practice/

challenge/

production/

==================================================
IMPLEMENTATION PLAN
==================================================

Generate

labs_backlog.md

Include

Lab ID

Technology

Module

Title

Difficulty

Estimated Time

Prerequisites

Career Paths

Related Tutorials

Related Projects

Priority

Status

Order all labs from beginner to expert.

==================================================
D2
==================================================

Generate a D2 diagram.

Learning Flow

Tutorial

↓

Guided Lab

↓

Practice Lab

↓

Challenge Lab

↓

Project

↓

Capstone

Store as

docs/assets/d2/labs-learning-flow.d2

Render as

docs/assets/images/labs-learning-flow.svg

==================================================
OUTPUT
==================================================

Generate only

1. Labs repository structure

2. Labs navigation

3. Lab template

4. Lab metadata

5. Lab roadmap

6. Career path mapping

7. labs_backlog.md design

8. D2 diagram

Do NOT generate actual labs.

The output must be scalable, production-ready and require no manual editing.