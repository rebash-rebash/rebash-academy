---
title: "Project — Python Cloud Operations Toolkit"
description: "Advanced project: multi-cloud inventory and ops helpers (AWS/Azure/GCP fixtures), plus Docker/K8s read-only commands with dry-run defaults."
difficulty: advanced
estimated_time: "12–18 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - python
  - cloud
  - kubernetes
  - docker
comments: false
---

# Project — Python Cloud Operations Toolkit

Advanced portfolio build — one CLI for cloud inventory and platform read-only operations.

## Project Overview

**Goal:** Combine cloud inventory (AWS EC2, Azure resources, GCP instances) with Docker and Kubernetes health helpers behind a shared CLI, defaulting to fixtures/dry-run.

**Deliverable for your portfolio:**

- Packaged multi-command CLI (`cloudops ...`)
- Adapters: AWS, Azure, GCP (fixture-first)
- `docker dangling` and `k8s health` read-only commands
- Shared logging, config, and exit taxonomy
- pytest suite with no live credentials required

**Estimated cost:** £0 with fixtures (optional live read-only).

## Goals

- [ ] `cloudops inventory {aws,azure,gcp}` with `--fixture`
- [ ] `cloudops docker report` dry-run; `--apply` optional and documented
- [ ] `cloudops k8s health --fixture` / optional kubeconfig
- [ ] Unified JSON schema for inventory rows
- [ ] CI green without cloud credentials

## Stack

| Piece | Choice |
|-------|--------|
| CLI | Typer |
| Cloud | boto3 / Azure SDK / google-cloud (optional) |
| Platform | Docker SDK, kubernetes client |
| Test | pytest + fixtures |

## Prerequisites

- Intermediate: [Infrastructure Inventory CLI](python-infra-inventory-cli.md)
- Labs: AWS/Azure/GCP inventory, Docker cleanup, Kubernetes health
- Tutorials: [Cloud Automation](../python/cloud-automation-aws-azure-gcp.md), [Docker SDK](../python/docker-sdk-automation.md), [Kubernetes Client](../python/kubernetes-python-client-automation.md)

## Milestones

### Milestone 1 — CLI skeleton and shared models

### Milestone 2 — Cloud inventory adapters (fixtures)

### Milestone 3 — Docker + Kubernetes read-only commands

### Milestone 4 — Docs, dry-run policy, CI

## Success criteria

- Every mutating path defaults to dry-run
- Offline tests cover parsers and CLI wiring
- README includes blast-radius and credential guidance

## Related

- Next: [Platform Engineering Framework](python-platform-engineering-framework.md)
- Labs: [AWS EC2 Inventory](../labs/python-aws-ec2-inventory.md)
