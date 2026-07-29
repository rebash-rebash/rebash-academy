---
title: "Project — Linux Server Health Dashboard"
description: "Intermediate portfolio project: schedule host health checks and render a simple text or HTML dashboard from CPU, memory, disk, and systemd signals."
difficulty: intermediate
estimated_time: "8–12 hours"
category: projects
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - projects
  - linux
  - monitoring
  - cron
  - systemd
comments: false
---

# Project — Linux Server Health Dashboard

Intermediate portfolio build — turn periodic host checks into a readable dashboard artifact.

## Project Overview

**Goal:** Collect health samples on a schedule and publish a dashboard file (text + optional HTML) that an on-call engineer can open over SSH or via a simple static path.

**Deliverable for your portfolio:**

- Check scripts (disk, memory, load, failed units, optional network)
- Aggregator that writes `reports/latest.txt` and `reports/latest.html`
- cron **or** systemd timer
- Threshold configuration file
- README with screenshots or sample HTML

**Estimated cost:** £0.

## Goals

- [ ] Thresholds live in config (not only hard-coded)
- [ ] Latest report always overwritten; history retained under `reports/history/`
- [ ] Non-zero exit when any check alerts
- [ ] Document how to install/uninstall the schedule

## Stack

| Piece | Choice |
|-------|--------|
| Language | Bash (+ optional Python for HTML) |
| Scheduling | cron or systemd timer |
| Inputs | `df`, `free`, `/proc/loadavg`, `systemctl --failed` |
| Layout | `bin/`, `config/thresholds.env`, `reports/`, `templates/` |

## Prerequisites

- [Host Monitoring](../linux/host-monitoring-vmstat-iostat-sar.md)
- [Scheduling: cron, at, and Timers](../linux/scheduling-cron-at-and-timers.md)
- [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md)
- Labs: [Ops Toolkit](../labs/linux-ops-toolkit-lab.md), [Services and Logs](../labs/linux-services-and-logs-lab.md)
- Project: [System Information Utility](linux-system-information-utility.md) (recommended)

## Milestones

### Milestone 1 — Checks and config

Port or rewrite lab checks; load `THRESH_DISK`, `THRESH_LOAD_MULT` from `config/thresholds.env`.

### Milestone 2 — Dashboard render

Produce a stable `latest.txt`. Optional: minimal HTML table with green/red status cells (no heavy frameworks).

### Milestone 3 — Schedule

Install a user crontab or systemd user/system timer; log stdout/stderr.

### Milestone 4 — Demo pack

Include `examples/latest.html`, install instructions, and a dry-run mode (`--once`).

## Success criteria

- `./bin/health-dashboard.sh --once` creates `reports/latest.txt`
- Forcing a low disk threshold yields exit `2` and a red/ALERT line
- Uninstall steps remove cron/timer cleanly

## Related

- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)
- Next: [Linux Operations Toolkit](linux-operations-toolkit.md)
- Interview: [Linux Interview Prep](../interview/linux.md)
