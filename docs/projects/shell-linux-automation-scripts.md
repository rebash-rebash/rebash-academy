---
title: "Project — Linux Automation Scripts"
description: "Beginner portfolio project: a small suite of Bash automation scripts for host facts, disk checks, and simple backups."
difficulty: beginner
estimated_time: "3–5 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - shell
  - bash
  - automation
comments: false
---

# Project — Linux Automation Scripts

Beginner portfolio build — ship three reliable Bash scripts an ops team can actually run.

## Project Overview

**Goal:** Deliver a mini toolkit of Linux automation scripts with strict mode, quoting, logging, and documented exit codes.

**Deliverable for your portfolio:**

- `bin/host-info.sh` — host facts (hostname, kernel, uptime, disk summary)
- `bin/check-disk.sh` — threshold-based disk alert with `RESULT` on stdout
- `bin/backup-dir.sh` — tar backup of a configured directory with retention
- Shared `lib/common.sh` (log helpers)
- `README.md` with usage and exit taxonomy
- `validate.sh` smoke suite

**Estimated cost:** £0.

## Goals

- [ ] All scripts use `#!/usr/bin/env bash` and `set -euo pipefail`
- [ ] Paths and arguments are quoted
- [ ] Diagnostics go to stderr; machine-readable lines to stdout
- [ ] Smoke tests cover success and usage-failure paths
- [ ] README explains how to schedule with cron

## Stack

| Piece | Choice |
|-------|--------|
| Language | Bash 4.2+ |
| Layout | `bin/`, `lib/`, `config/`, `out/`, `tests/` or `validate.sh` |
| Scheduling | Documented crontab examples |

## Prerequisites

- Tutorials: [Writing Your First Script](../shell/writing-your-first-script.md), [Variables, Quoting, and Arithmetic](../shell/variables-quoting-and-arithmetic.md), [Control Flow — Conditionals](../shell/control-flow-conditionals.md), [Linux Admin Automation](../shell/linux-admin-automation.md)
- Labs: [Create Your First Script](../labs/shell-first-script.md), [Monitor Disk Usage](../labs/shell-monitor-disk-usage.md), [Build a Backup Utility](../labs/shell-backup-utility.md)

## Milestones

### Milestone 1 — Layout and common library

Create repo layout and `lib/common.sh` with `log` / `die`.

### Milestone 2 — Host info and disk check

Implement fact dump and disk monitor; document exit codes `0/2/3`.

### Milestone 3 — Backup helper

Timestamped archives under `out/backups/` with `--retain-days`.

### Milestone 4 — Validation and README

`validate.sh` runs happy path + `--help` failures; README shows cron examples with absolute paths.

## Success criteria

- Another engineer runs `./validate.sh` successfully on Ubuntu
- Scripts refuse unsafe paths outside a configured prefix
- No secrets in the repository

## Related

- Next: [Linux Administration Toolkit](shell-linux-administration-toolkit.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
