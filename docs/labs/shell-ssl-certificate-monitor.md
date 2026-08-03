---
title: "Lab — Build an SSL Certificate Monitor"
description: "Check TLS certificate expiry with openssl, alert before expiry, and log results."
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

# Lab — Build an SSL Certificate Monitor

## Lab Overview

**Purpose:** Prevent outages by alerting N days before certificate expiry.

**Scenario:** Last quarter a public endpoint expired overnight. Leadership wants a weekly check script.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You build `cert-check.sh` that connects with OpenSSL, parses `notAfter`, and exits non-zero when within the warning window.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Fetch remote certificate with openssl s_client
- [ ] Parse expiry date
- [ ] Compare days remaining to a threshold
- [ ] Log RESULT lines for automation

## Prerequisites

### Knowledge

- [Networking Automation with Shell](../shell/networking-automation-with-shell.md)
- [Scheduling — cron, at, and Timers](../shell/scheduling-cron-at-and-timers.md)
- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| openssl | required |
| date | GNU date preferred |

**Estimated cost:** £0.

## Environment

Host with outbound HTTPS allowed.

## Initial State

```bash title="Terminal"
mkdir -p ~/rebash-lab-shell/certs
cd ~/rebash-lab-shell/certs
```

## Lab Tasks

### Task 1 — Fetch certificate end date

```bash title="Terminal"
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -enddate
```

### Task 2 — Implement `cert-check.sh`

Args: `--host`, `--port` (443), `--warn-days` (30).

Exit:

| Code | Meaning |
|------|---------|
| 0 | Days left > warn |
| 2 | Within warn window |
| 3 | Connection/parse failure |

### Task 3 — Multi-host file

Read hosts from `hosts.txt` and summarise.


## Validation

- [ ] Single-host check prints days remaining
- [ ] Artificial low `--warn-days` can force alert path
- [ ] Connection failures exit 3

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| GNU date vs BSD date | macOS date flags | Use a Linux VM for the lab |
| SNI mismatch | Missing -servername | Always pass `-servername` |

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
- [`Scheduling Cron At And Timers`](../shell/scheduling-cron-at-and-timers.md)
- [`Error Handling Logging And Debugging`](../shell/error-handling-logging-and-debugging.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
