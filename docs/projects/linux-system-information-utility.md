---
title: "Project — Linux System Information Utility"
description: "Beginner portfolio project: build a Bash system information utility that reports OS, CPU, memory, disk, and network facts with clear exit codes."
difficulty: beginner
estimated_time: "3–5 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - linux
  - bash
  - cli
comments: false
---

# Project — Linux System Information Utility

Beginner portfolio build for the [Linux for Cloud & DevOps](../learning-paths/linux-administrator/) track — ship a small, reliable host inventory CLI.

## Project Overview

**Goal:** Produce a single command that prints a structured system information report suitable for handoff notes and onboarding.

**Deliverable for your portfolio:**

- Git repository with a clear README
- `sysinfo` (or `linux-info`) Bash script
- Human-readable and optional machine-readable (`--json` or key=value) output
- Sample run captured under `examples/`
- Documented exit codes

**Estimated cost:** £0.

## Goals

- [ ] Collect OS, kernel, hostname, uptime, CPU, memory, disk, and primary IPv4
- [ ] Support `--help` and a quiet/machine mode
- [ ] Fail clearly when required tools are missing
- [ ] Include a short validation script or checklist

## Stack

| Piece | Choice |
|-------|--------|
| Language | Bash |
| Tools | `hostnamectl`, `free`, `df`, `ip`, `lscpu` (or `/proc`) |
| Layout | `bin/sysinfo`, `README.md`, `examples/` |

## Prerequisites

- Modules 1–3 of the Linux track ([Fundamentals](../linux/linux-fundamentals-distributions-and-architecture.md), [Commands](../linux/essential-linux-commands.md), [Filesystem](../linux/filesystem-paths-links-mounts-and-inodes.md))
- Lab: [Install Linux and First Boot](../labs/linux-install-and-first-boot.md)

## Milestones

### Milestone 1 — Repo skeleton

Create `~/rebash-linux-sysinfo`, add `.gitignore`, README outline, and `bin/sysinfo` stub with `set -euo pipefail`.

### Milestone 2 — Collectors

Implement functions for identity, memory, disk, and network. Prefer `/proc` and standard utilities over fragile parsing.

### Milestone 3 — Output formats

Default human report; optional `--kv` or `--json` (JSON may use `python3 -c` or `jq` if documented).

### Milestone 4 — Polish

`--help`, non-zero exit on missing dependencies, `examples/sample.txt` from a real run.

## Success criteria

- Another engineer runs `./bin/sysinfo` in under two minutes
- Output includes at least OS, kernel, memory, root disk usage, and one IP
- README lists prerequisites, usage, and exit codes (`0` ok, `2` usage, `3` missing tool)

## Related

- Course path: [Linux for Cloud & DevOps](../learning-paths/linux-administrator/)
- Lab: [Linux Ops Toolkit](../labs/linux-ops-toolkit-lab.md)
- Next project: [Linux Server Health Dashboard](linux-server-health-dashboard.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
