---
title: "Lab — Automate SSH Tasks"
description: "Run remote commands over SSH with BatchMode, timeouts, and aggregated reporting."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Automate SSH Tasks

## Lab Overview

**Purpose:** Orchestrate simple remote checks across a host inventory.

**Scenario:** Ops must run `uptime` and disk checks on a list of lab VMs without interactive prompts.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You build an SSH runner that uses `BatchMode=yes`, connects timeouts, and records per-host results.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Use SSH BatchMode and ConnectTimeout
- [ ] Iterate hosts from a file
- [ ] Capture per-host exit status
- [ ] Never embed passwords; use keys

## Prerequisites

### Knowledge

- [Networking Automation with Shell](../shell/networking-automation-with-shell.md)
- [Functions, Parameters, and Locals](../shell/functions-parameters-and-locals.md)
- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| ssh | OpenSSH client |
| lab hosts or localhost | may use SSH to localhost |

**Estimated cost:** £0.

## Environment

Linux with OpenSSH. You may target `127.0.0.1` if key-based localhost SSH works.

## Initial State

```bash title="Terminal"
mkdir -p ~/rebash-lab-shell/ssh
cd ~/rebash-lab-shell/ssh
printf '%s\n' '127.0.0.1' > hosts.txt
```

!!! tip "Safety"
    Use `BatchMode=yes` so missing keys fail fast instead of password prompts.

## Lab Tasks

### Task 1 — Single-host probe

```bash title="Terminal"
ssh -o BatchMode=yes -o ConnectTimeout=5 127.0.0.1 'uptime' || true
```

### Task 2 — `ssh-run.sh`

```bash
./ssh-run.sh --hosts hosts.txt -- uptime
./ssh-run.sh --hosts hosts.txt -- 'df -P -x tmpfs | tail -n +2'
```

Write `reports/HOST.txt` and a summary with pass/fail counts (count lines — do not use array length macros that break MkDocs).

### Task 3 — Harden options

Document recommended options: `StrictHostKeyChecking=accept-new` (lab only), `ConnectTimeout`, `BatchMode`.


## Validation

- [ ] Hosts file is read line-by-line safely
- [ ] Failures do not abort the whole loop unless configured
- [ ] Summary report exists

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| Permission denied (publickey) | No key configured | Set up localhost keys or skip remote and mock |
| Hangs | No timeout | Set ConnectTimeout |

## Cleanup

```bash title="Terminal"
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

- [`Networking Automation With Shell`](../shell/networking-automation-with-shell.md)
- [`Functions Parameters And Locals`](../shell/functions-parameters-and-locals.md)
- [`Production Shell Scripting`](../shell/production-shell-scripting.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
