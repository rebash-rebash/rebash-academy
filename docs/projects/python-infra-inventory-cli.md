---
title: "Project — Python Infrastructure Inventory CLI"
description: "Intermediate project: multi-source inventory CLI with Typer, adapters (HTTP/Docker/SSH/fixtures), and pytest."
difficulty: intermediate
estimated_time: "8–12 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - python
  - typer
  - inventory
comments: false
---

# Project — Python Infrastructure Inventory CLI

Intermediate portfolio build — collect and normalise inventory from more than one source into a single report.

## Project Overview

**Goal:** Ship a Typer (or Click) CLI that inventories hosts/services from at least two adapters (for example HTTP status + Docker fixtures, or static YAML + SSH), with tests that do not need live cloud.

**Deliverable for your portfolio:**

- Packaged CLI (`inventory ...`)
- Pluggable source adapters behind a common interface
- Table or JSON output
- `pytest` with mocked network/Docker
- README with architecture and dry-run notes

**Estimated cost:** £0 (local mocks; optional Docker Engine).

## Goals

- [ ] Multi-command CLI (`collect`, `show`, `export`)
- [ ] Shared model for inventory records (id, source, status, metadata)
- [ ] Timeouts on all HTTP calls
- [ ] Secrets via env only — never committed
- [ ] Unit tests for parsers and CLI help/exit codes

## Stack

| Piece | Choice |
|-------|--------|
| CLI | Typer or Click |
| HTTP | httpx with timeouts |
| Optional | Docker SDK, Paramiko (lab-scoped keys) |
| Config | YAML + env overlay |
| Test | pytest + fixtures |

## Prerequisites

- Beginner: [Python Log Analysis Tool](python-log-analysis-tool.md)
- Labs: [Linux Health Checker](../labs/python-linux-health-checker.md), [Docker Cleanup Tool](../labs/python-docker-cleanup-tool.md) (optional adapter ideas)
- Tutorials: [CLI Applications](../python/cli-applications-argparse-click-typer.md), [REST APIs](../python/rest-apis-requests-auth-and-resilience.md)

## Milestones

### Milestone 1 — Skeleton

`pyproject.toml`, package layout, `inventory --help`, empty `collect` command.

### Milestone 2 — First adapter

Static YAML or HTTP health adapter with timeout and typed errors.

### Milestone 3 — Second adapter

Docker list *or* SSH remote `hostname`/`uptime` — behind the same interface; mock in tests. Support `--fixture` when daemon/SSH unavailable.

### Milestone 4 — Export and CI

JSON/CSV export; GitHub Actions or GitLab CI job running `pytest` only.

## Success criteria

- `collect` merges sources without crashing when one source is down (record error, continue)
- Tests pass offline
- README documents env vars and blast radius (“read-only by default”)

## Related

- Course: [Python for DevOps](../python/index.md)
- Next: [Cloud Operations Toolkit](python-cloud-operations-toolkit.md)
