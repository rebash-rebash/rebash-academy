---
title: "Lab — Monitor Disk Usage"
description: "Alert when filesystem usage exceeds a threshold and emit machine-readable RESULT lines."
difficulty: beginner
estimated_time: "35–45 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Monitor Disk Usage

## Lab Overview

**Purpose:** Write a disk usage monitor suitable for cron.

**Scenario:** On-call wants a simple alert when any filesystem crosses 80% before the full monitoring stack is ready.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

A startup runs a few VMs. They need a disk check script that exits non-zero when thresholds are breached.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Parse `df` output safely
- [ ] Compare usage against a threshold
- [ ] Emit human logs on stderr and RESULT on stdout
- [ ] Exclude tmpfs/devtmpfs noise

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [Text Processing in Shell Scripts](../shell/text-processing-in-shell-scripts.md)
- [Control Flow — Conditionals](../shell/control-flow-conditionals.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| df/awk | coreutils |

**Estimated cost:** £0.

## Environment

Any Linux host.

## Initial State

```bash title="Terminal"
mkdir -p ~/rebash-lab-shell/monitor
cd ~/rebash-lab-shell/monitor
```

## Lab Tasks

### Task 1 — Implement `check-disk.sh`

Create `check-disk.sh`:

```bash title="check-disk.sh"
#!/usr/bin/env bash
set -euo pipefail
THRESH="${1:-80}"
alert=0
while read -r use mnt; do
  use="${use%\%}"
  if (( use >= THRESH )); then
    echo "ALERT disk ${use}% on ${mnt}" >&2
    alert=1
  else
    echo "OK disk ${use}% on ${mnt}" >&2
  fi
done < <(df -P -x tmpfs -x devtmpfs | awk 'NR>1 {print $5, $6}')
if (( alert )); then
  echo "RESULT status=alert metric=disk"
  exit 2
fi
echo "RESULT status=ok metric=disk"
exit 0
```

Run:

```bash title="Terminal"
chmod +x check-disk.sh
./check-disk.sh 80
./check-disk.sh 1 || true
```


### Task 2 — Document exit codes

| Code | Meaning |
|------|---------|
| 0 | All filesystems under threshold |
| 2 | One or more alerts |
| 3 | Usage / parse error |


## Validation

- [ ] Script exits 0 on a healthy host with a high threshold
- [ ] Low threshold forces exit 2 and RESULT status=alert
- [ ] tmpfs mounts are excluded

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| df columns differ | BusyBox df | Use `df -P` |
| Arithmetic errors | Percent sign not stripped | Strip `%` before `(( ))` |

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

- [`Linux Admin Automation`](../shell/linux-admin-automation.md)
- [`Text Processing In Shell Scripts`](../shell/text-processing-in-shell-scripts.md)
- [`Scheduling Cron At And Timers`](../shell/scheduling-cron-at-and-timers.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
