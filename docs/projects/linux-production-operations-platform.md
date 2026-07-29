---
title: "Project — Production Linux Operations Platform"
description: "Capstone portfolio project: user management, monitoring, logging, hardening, backups, health dashboard, performance, alerting, reporting, and scheduling on Linux."
difficulty: advanced
estimated_time: "20–30 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - linux
  - capstone
  - sre
  - automation
comments: false
---

# Project — Production Linux Operations Platform

Capstone for [Linux for Cloud & DevOps Engineers](../learning-paths/linux-for-cloud-devops.md) — integrate administration, security, and reliability into one coherent platform (scripts + docs + schedule), not a SaaS product.

## Project Overview

**Goal:** Build a **Production Linux Operations Platform** you can demonstrate end-to-end on one or two Ubuntu VMs: identity hygiene, observability basics, hardening, backup drills, dashboards, alerts, and reporting on a schedule.

**Deliverable for your portfolio:**

- Repository with modules mapped to the feature list below
- Installable toolkit (`install.sh` / Ansible optional)
- Runbook (`docs/RUNBOOK.md`) and architecture note
- Demo recording or screenshots of dashboard + alert + restore
- Threat model and limitations section

**Estimated cost:** £0–£10 if using two small cloud VMs for a week.

## Required features

| Feature | Minimum bar |
|---------|-------------|
| User management | Scripted create/disable user + group + SSH key install; audit list |
| Monitoring | Periodic CPU/mem/disk/load collection to `var/metrics/` |
| Logging | Journal export or file logs for platform actions; retention note |
| Security hardening | SSH + UFW baseline as code (idempotent, dry-run default) |
| Backup automation | Scheduled `tar`/`rsync` of a data dir + checksum; restore drill doc |
| System health dashboard | Latest HTML/text dashboard from metrics |
| Performance monitoring | Capture `vmstat`/`iostat` samples into history |
| Alerting | Non-zero exit + local alert file / webhook stub on threshold breach |
| Reporting | Weekly summary report (failures, disk trend, backup status) |
| Scheduling | cron and/or systemd timers for collect, backup, report |

## Stack

| Piece | Choice |
|-------|--------|
| OS | Ubuntu 22.04/24.04 |
| Language | Bash + optional Python |
| Web (optional) | Static HTML only — no public internet required |
| Config | `/etc/rebash-platform/` or `./config` for lab mode |
| State | `./var` or `/var/lib/rebash-platform` |

## Prerequisites

- Complete the Linux track through production modules
- Projects: [Sysinfo](linux-system-information-utility.md) → [Health Dashboard](linux-server-health-dashboard.md) → [Ops Toolkit](linux-operations-toolkit.md)
- Labs: firewall, ops toolkit, performance, services/logs, storage, users

## Milestones

### Milestone 1 — Platform skeleton

Directories, config schema, logging helper, version, dry-run global flag.

### Milestone 2 — Identity + hardening

User module + SSH/UFW hardening module with rollback notes.

### Milestone 3 — Observe

Metrics collectors, dashboard, performance history, failed-unit watch.

### Milestone 4 — Protect data

Backup job, checksum, restore drill script, retention.

### Milestone 5 — Alert + report + schedule

Alert stub, weekly report, timers/cron, full demo script `scripts/demo.sh`.

### Milestone 6 — Hardening review

Document blast radius, secrets handling (no passwords in git), and cleanup.

## Success criteria

- Fresh Ubuntu VM: install → demo → show dashboard, one alert, one backup restore
- Dry-run never changes SSH/UFW until `--apply`
- RUNBOOK covers install, operate, incident, uninstall
- You can explain each feature in an interview in under two minutes

## Stretch

- Ansible playbook wrapping the same modules
- Multi-host inventory file
- Integration with cloud-init for first boot

## Related

- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)
- Interview: [Linux Interview Prep](../interview/linux.md)
- Quiz: [Linux for Cloud & DevOps Fundamentals](../quizzes/linux-for-cloud-devops-fundamentals.md)
- Labs index: [Labs](../labs/index.md)
