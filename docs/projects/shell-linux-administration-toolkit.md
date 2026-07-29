---
title: "Project — Linux Administration Toolkit"
description: "Intermediate portfolio project: package user, package, service, and log helpers behind a cohesive Bash CLI."
difficulty: intermediate
estimated_time: "8–12 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - shell
  - bash
  - linux-admin
comments: false
---

# Project — Linux Administration Toolkit

Intermediate portfolio build — a CLI for everyday Linux administration tasks.

## Project Overview

**Goal:** Ship `rebash-admin` with subcommands for users, packages, services, and log rotation helpers — dry-run by default where actions are privileged.

**Deliverable for your portfolio:**

- Entrypoint: `bin/rebash-admin <command>`
- Commands: `users`, `packages`, `services`, `logs`, `report`
- Shared logging, config file (`config/admin.conf`), exit taxonomy
- Dry-run defaults for mutating commands
- Smoke tests and sample config

**Estimated cost:** £0 (local VM).

## Goals

- [ ] Subcommands share `lib/*.sh` (no copy-pasted logging)
- [ ] Mutating actions require `--apply` (default dry-run)
- [ ] `report` writes a dated summary under `out/`
- [ ] Unsupported OS/package manager fails clearly
- [ ] README includes threat notes (what the toolkit does *not* do)

## Stack

| Piece | Choice |
|-------|--------|
| Language | Bash |
| Layout | `bin/rebash-admin`, `lib/`, `cmd/`, `config/`, `out/` |
| Privileges | sudo only when `--apply` on a lab VM |

## Prerequisites

- Tutorials: [Linux Admin Automation](../shell/linux-admin-automation.md), [Functions, Parameters, and Locals](../shell/functions-parameters-and-locals.md), [Production Shell Scripting](../shell/production-shell-scripting.md), [Scheduling — cron, at, and Timers](../shell/scheduling-cron-at-and-timers.md)
- Labs: [User Management Script](../labs/shell-user-management-script.md), [Automate Software Installation](../labs/shell-automate-software-installation.md), [Rotate Logs](../labs/shell-rotate-logs.md), [Service Health Checker](../labs/shell-service-health-checker.md)
- Project: [Linux Automation Scripts](shell-linux-automation-scripts.md)

## Milestones

### Milestone 1 — CLI skeleton

`case`/getopts parsing, global `--config`, `--help`, `--version`.

### Milestone 2 — Users and packages

Dry-run create/list/disable sketches; idempotent package install detection.

### Milestone 3 — Services and logs

`systemctl is-active` wrappers; log rotate helper for lab paths only.

### Milestone 4 — Report + release notes

Aggregate checks into `out/report-YYYYMMDD.md`; document cron/timer usage.

## Success criteria

- `rebash-admin report` runs without root
- `--apply` is required for changes
- Install via README in under 10 minutes on a clean Ubuntu VM

## Related

- Next: [Production Operations Toolkit](shell-production-operations-toolkit.md)
- Lab: [Linux Operations Toolkit](../labs/shell-linux-operations-toolkit.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
