---
title: "Lab — Monitor CPU & Memory"
description: "Collect load and memory metrics, compare against thresholds, and exit with a taxonomy."
difficulty: intermediate
estimated_time: "40–50 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Monitor CPU & Memory

## Lab Overview

**Purpose:** Extend host monitoring beyond disk into load average and memory pressure.

**Scenario:** Night ops sees intermittent saturation and wants a local script before Prometheus arrives.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You deliver `check-load.sh` and `check-mem.sh` plus a tiny aggregator.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Read load average and CPU count
- [ ] Compute available memory percentage
- [ ] Aggregate checks into one status
- [ ] Keep thresholds configurable

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [Text Processing in Shell Scripts](../shell/text-processing-in-shell-scripts.md)
- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| free/nproc | procps/coreutils |

**Estimated cost:** £0.

## Environment

Linux host with `/proc`.

## Initial State

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-shell/monitor/{bin,reports}
cd ~/rebash-lab-shell/monitor
```

## Lab Tasks

### Task 1 — Memory check

Alert if available memory < 10% of total (heuristic). Use `free -b`.

### Task 2 — Load check

Alert if 1-minute load > `2 * nproc`.

### Task 3 — Aggregator `health-cpu-mem.sh`

Run both checks; worst exit code wins. Write a short report under `reports/`.

```bash
./bin/check-mem.sh
./bin/check-load.sh
./bin/health-cpu-mem.sh
```


## Validation

- [ ] Both checks print OK or ALERT on stderr
- [ ] Aggregator creates a report file
- [ ] Exit taxonomy is documented in a README snippet

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| free output differs | Older procps | Parse `Mem:` line carefully |
| High false alerts | Threshold too low | Tune for lab size |

## Cleanup

``` {.bash .ra-terminal title="Terminal"}
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
- [`Text Processing In Shell Scripts`](../shell/text-processing-in-shell-scripts.md)
- [`Error Handling Logging And Debugging`](../shell/error-handling-logging-and-debugging.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
