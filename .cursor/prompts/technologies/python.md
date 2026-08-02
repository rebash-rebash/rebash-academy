# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

Python for DevOps Engineers

---

## Description

A practical Python course designed specifically for Cloud, DevOps, Platform Engineering and Site Reliability Engineering.

This is not a general Python programming course.

The focus is on infrastructure automation, cloud APIs, Kubernetes, Terraform, CI/CD, Linux administration and production engineering.

Learners should finish the course capable of building production-ready automation tools.

---

## Target Roles

- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer
- Automation Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

- Linux Fundamentals
- Basic Shell Scripting

---

## MCP Servers

Primary

- Context7

Optional

- GitHub
- Kubernetes
- Terraform
- AWS
- Azure

---

# Modules

## Module 1 — Python Fundamentals

- What is Python?
- Installing Python
- Python Versions
- Python Interpreter
- VS Code Setup
- PyCharm Setup
- Virtual Environments
- pip
- uv
- Poetry

---

## Module 2 — Python Basics

- Variables
- Data Types
- Operators
- Strings
- Numbers
- Booleans
- Input
- Output
- Type Conversion

---

## Module 3 — Control Flow

- if
- elif
- else
- match
- for
- while
- break
- continue
- pass

---

## Module 4 — Functions

- Functions
- Parameters
- Return Values
- Default Arguments
- Keyword Arguments
- Variable Arguments
- Lambda Functions
- Scope

---

## Module 5 — Data Structures

- Lists
- Tuples
- Dictionaries
- Sets
- List Comprehensions
- Dictionary Comprehensions
- Iterators
- Generators

---

## Module 6 — Modules & Packages

- import
- Standard Library
- Custom Modules
- Packages
- Dependency Management

---

## Module 7 — File Handling

- Reading Files
- Writing Files
- CSV
- JSON
- YAML
- XML
- pathlib
- shutil
- Temporary Files

---

## Module 8 — Error Handling

- Exceptions
- try
- except
- finally
- raise
- Custom Exceptions
- Defensive Programming

---

## Module 9 — Object-Oriented Programming

- Classes
- Objects
- Methods
- Constructors
- Inheritance
- Encapsulation
- Polymorphism
- Dataclasses

---

## Module 10 — Logging & Debugging

- logging
- Log Levels
- Structured Logging
- pdb
- Tracebacks
- Debugging Techniques

---

## Module 11 — Configuration Management

- Environment Variables
- dotenv
- YAML
- JSON
- TOML
- Configuration Files
- Secret Handling

---

## Module 12 — CLI Applications

- argparse
- Click
- Typer
- Rich
- Progress Bars
- Interactive CLI Applications

---

## Module 13 — Linux Automation

- subprocess
- os
- pathlib
- shutil
- signal
- psutil
- Process Management
- File Permissions

---

## Module 14 — REST APIs

- requests
- HTTP Methods
- Authentication
- OAuth
- Tokens
- Pagination
- Rate Limiting
- Error Handling

---

## Module 15 — Cloud Automation

### AWS

- boto3
- EC2
- S3
- IAM
- Lambda

### Azure

- Azure SDK
- Authentication
- Resource Management

### Google Cloud

- Google Cloud SDK
- Storage
- Compute Engine

---

## Module 16 — Git Automation

- GitPython
- GitHub API
- GitLab API
- Repository Automation
- Pull Requests
- Webhooks

---

## Module 17 — Docker Automation

- Docker SDK
- Containers
- Images
- Networks
- Volumes
- Registry Automation

---

## Module 18 — Kubernetes Automation

- kubernetes-python-client
- Pods
- Deployments
- Services
- ConfigMaps
- Secrets
- Jobs
- Namespaces

---

## Module 19 — Infrastructure Automation

- Terraform CLI
- cdktf Overview
- Terraform Validation
- Plan Automation
- State Inspection

---

## Module 20 — SSH Automation

- Paramiko
- Fabric
- SCP
- SSH Keys
- Remote Execution

---

## Module 21 — Concurrency

- Threads
- Multiprocessing
- asyncio
- concurrent.futures
- Queues

---

## Module 22 — Testing

- unittest
- pytest
- Fixtures
- Mocking
- Coverage
- Integration Testing

---

## Module 23 — Packaging

- pyproject.toml
- Wheels
- Publishing Packages
- Versioning
- Dependency Management

---

## Module 24 — Production Engineering

- Retry Logic
- Exponential Backoff
- Metrics
- Logging
- Health Checks
- Performance
- Memory Profiling
- Observability

---

## Module 25 — Security

- Secret Management
- Encryption
- Hashing
- Secure Coding
- Input Validation
- Dependency Scanning
- Supply Chain Security

---

## Module 26 — AI for DevOps

- OpenAI SDK
- MCP Clients
- LangChain Basics
- AI-assisted Automation
- AI Agents for Operations

---

## Module 27 — Troubleshooting

- Dependency Issues
- Virtual Environment Problems
- API Failures
- Memory Leaks
- Performance Issues
- Production Debugging

---

# Hands-on Labs

- Build a Log Analyser
- Build a Linux Health Checker
- Build a YAML Validator
- Build a JSON Validator
- Build a GitHub Repository Auditor
- Build a Docker Cleanup Tool
- Build a Kubernetes Health Checker
- Build a Kubernetes Deployment Validator
- Build a Terraform Wrapper
- Build an AWS EC2 Inventory Tool
- Build an Azure Resource Inventory Tool
- Build a GCP Inventory Tool
- Build a Certificate Expiry Monitor
- Build a Slack Notification Bot
- Build a REST API Monitoring Service
- Build a Secrets Scanner
- Build a CI/CD Automation Tool

---

# Projects

## Beginner

Python Log Analysis Tool

---

## Intermediate

Infrastructure Inventory CLI

---

## Advanced

Cloud Operations Automation Toolkit

---

## Expert

Platform Engineering Automation Framework

---

## Capstone

Production DevOps Automation Platform

Features:

- CLI Interface
- Plugin Architecture
- Cloud Inventory
- Kubernetes Automation
- Terraform Automation
- GitHub Automation
- Monitoring
- Notifications
- Configuration Management
- Logging
- Testing
- Packaging
- Documentation

---

# Cheat Sheets

Generate:

- Python Syntax
- Data Structures
- File Handling
- Exceptions
- Logging
- requests
- argparse
- Click
- Docker SDK
- Kubernetes Client
- boto3
- pytest

---

# Interview Preparation

Cover:

- Python Fundamentals
- OOP
- File Handling
- REST APIs
- Automation
- Kubernetes
- Docker
- Terraform
- Cloud SDKs
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Python tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Python Execution Flow
- Virtual Environment
- Package Architecture
- REST API Flow
- Kubernetes Client Architecture
- Docker SDK Workflow
- Automation Pipeline
- Plugin Architecture
- Control Flow / Basics (as modules need)

---

# Certifications

Map modules where appropriate to:

- PCAP (Python Certified Associate Programmer)
- AWS DevOps Engineer – Professional
- CKA
- CKAD
- HashiCorp Terraform Associate

---

# Capstone Outcome

After completing this course learners should be able to:

- Develop production-ready Python automation
- Build CLI tools
- Automate Linux administration
- Interact with cloud platforms
- Automate Kubernetes and Docker
- Build CI/CD utilities
- Package and distribute Python applications
- Build reusable DevOps frameworks
- Apply software engineering best practices to infrastructure automation