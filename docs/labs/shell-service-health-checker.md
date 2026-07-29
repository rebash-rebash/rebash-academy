---
title: "Lab — Build a Service Health Checker"
description: "Check systemd units and HTTP endpoints, aggregate status, and prepare for cron."
difficulty: intermediate
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Build a Service Health Checker

## Lab Overview

**Purpose:** Combine local service state and HTTP probes into one health script.

**Scenario:** A demo API and `nginx`/`sshd` must be verified after each lab VM reboot.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

Platform needs a bastion-friendly health checker: systemd is-active plus optional curl probe.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Query systemd unit state
- [ ] Probe HTTP with curl timeouts
- [ ] Aggregate multi-check results
- [ ] Sketch a crontab entry

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [Networking Automation with Shell](../shell/networking-automation-with-shell.md)
- [Scheduling — cron, at, and Timers](../shell/scheduling-cron-at-and-timers.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| systemctl | systemd host |
| curl | HTTP probe |

**Estimated cost:** £0.

## Environment

Linux with systemd. HTTP probe may target `https://example.com` or a local service.

## Initial State

```bash
mkdir -p ~/rebash-lab-shell/health
cd ~/rebash-lab-shell/health
```

## Lab Tasks

### Task 1 — Unit check

```bash
systemctl is-active ssh || systemctl is-active sshd || true
```

Wrap in `check-unit.sh <unit>` exiting 0/2.

### Task 2 — HTTP check

`check-http.sh URL` using `curl -fsS --max-time 5 -o /dev/null -w '%{http_code}'`.

### Task 3 — Aggregate

`health-check.sh` runs configured checks from a simple `checks.conf`:

```text
unit ssh
http https://example.com
```

### Task 4 — Cron sketch

Document a user crontab line that runs every 5 minutes and appends logs.


## Validation

- [ ] Unit and HTTP helpers exit correctly on failure
- [ ] Aggregator reads `checks.conf`
- [ ] Cron line is documented (not necessarily installed)

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| systemctl not found | Non-systemd | Skip unit checks; document limitation |
| curl TLS errors | Lab proxy/MITM | Use `-k` only in lab with a warning |

## Cleanup

```bash
rm -rf ~/rebash-lab-shell
```

## Stretch Goals

- Add a `--dry-run` mode that prints actions without changing the system
- Emit a machine-readable `RESULT status=...` line on stdout for CI
- Schedule the script with cron or a systemd timer

## Production Discussion

In production, wrap scripts with lock files, structured logging, explicit `PATH`, and documented exit codes. Prefer configuration files over hard-coded hosts and thresholds. Never embed secrets in scripts — use environment variables or a secrets manager.

## Best Practices

- Use `#!/usr/bin/env bash` and `set -euo pipefail`
- Quote every expansion that may contain spaces
- Log diagnostics to stderr; keep stdout for data
- Prefer absolute paths in scheduled jobs
- Validate inputs before destructive actions

## Common Mistakes

| Mistake | Why it happens | Correct approach |
|---------|----------------|------------------|
| Unquoted paths | Habit from interactive shell | Always `"$var"` |
| Missing `pipefail` | Default Bash pipeline behaviour | `set -o pipefail` |
| Interactive-only PATH | Cron/systemd minimal env | Set `PATH=` at top |
| Skipping dry-run | Time pressure | Default to dry-run for risky ops |

## Success Criteria

- [ ] Script runs under Bash with strict mode
- [ ] Validation and failure paths are tested
- [ ] Exit codes are documented
- [ ] Cleanup leaves no lab artefacts (or documents what remains)

## Reflection Questions

1. What would break if this ran under `/bin/sh` (dash) instead of Bash?
2. How would you make the script idempotent?
3. How would you secure credentials and host inventories?
4. How would you observe failures in production?

## Interview Connection

Interviewers often ask about quoting, exit codes, cron environment differences, and how you prevent overlapping jobs. Be ready to walk through a small script and explain failure modes.

## Related Tutorials

- [`Linux Admin Automation`](../shell/linux-admin-automation.md)
- [`Networking Automation With Shell`](../shell/networking-automation-with-shell.md)
- [`Scheduling Cron At And Timers`](../shell/scheduling-cron-at-and-timers.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
