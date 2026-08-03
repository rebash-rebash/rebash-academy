---
title: "Lab — Build a User Management Script"
description: "Automate create, list, and disable user workflows with validation and logging."
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

# Lab — Build a User Management Script

## Lab Overview

**Purpose:** Build a small CLI that wraps safe user administration actions for a lab VM.

**Scenario:** Ops needs a scripted way to create service accounts with a consistent home layout — without pasting ad-hoc commands into Slack.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

A SaaS team provisions short-lived lab users for contractors. Manual `useradd` steps drift. You automate create/list/disable with dry-run and audit logging.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Parse subcommands with `case`
- [ ] Validate usernames before calling privileged tools
- [ ] Log actions and refuse destructive ops without confirmation flags
- [ ] Document an exit taxonomy for automation callers

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [Functions, Parameters, and Locals](../shell/functions-parameters-and-locals.md)
- [Control Flow — Conditionals](../shell/control-flow-conditionals.md)

### Software

| Tool | Notes |
|------|--------|
| Bash 4.2+ | required |
| sudo | for real user ops — use dry-run if unprivileged |

**Estimated cost:** £0.

## Environment

Linux VM where you may use `sudo` (or dry-run only).

## Initial State

```bash
mkdir -p ~/rebash-lab-shell/users/{bin,logs}
cd ~/rebash-lab-shell/users
```

!!! warning "Privileged actions"
    Prefer `--dry-run` first. Only create real users on disposable lab VMs.

## Lab Tasks

### Task 1 — CLI skeleton

Create `bin/usermgr.sh` with subcommands: `list`, `create`, `disable`, and `help`:

```bash
#!/usr/bin/env bash
set -euo pipefail
LOG_DIR="${LOG_DIR:-$HOME/rebash-lab-shell/users/logs}"
mkdir -p "$LOG_DIR"
log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >>"$LOG_DIR/usermgr.log"; }

usage() {
  cat >&2 <<'USAGE'
Usage: usermgr.sh <list|create|disable|help> [options]
  create --user NAME [--dry-run]
  disable --user NAME [--dry-run]
USAGE
}

cmd="${1:-help}"; shift || true
case "$cmd" in
  help|-h|--help) usage; exit 2 ;;
  list|create|disable) ;;
  *) usage; exit 2 ;;
esac
```

Run:

```bash
chmod +x bin/usermgr.sh
```


### Task 2 — Implement list

Print local human users (UID >= 1000) using `getent passwd` and `awk`.

### Task 3 — Implement create (dry-run first)

Accept `--user` and `--dry-run`. Validate `^[a-z_][a-z0-9_-]*$`. In dry-run, print the `useradd` command; otherwise run `sudo useradd -m -s /bin/bash "$user"` on a lab VM.

### Task 4 — Implement disable

Lock the account with `usermod -L` / `passwd -l` (or print the command in dry-run). Log every action.

### Task 5 — Exit taxonomy

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage / validation error |
| 3 | User already exists / not found |
| 4 | Privilege or system failure |


## Validation

- [ ] `list` prints UID>=1000 users
- [ ] `create --dry-run` prints intended command and exits 0
- [ ] Invalid usernames exit 2 without calling useradd
- [ ] Actions append to `logs/usermgr.log`

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| sudo password prompts break automation | Interactive sudo | Configure NOPASSWD for lab or stay in dry-run |
| Username rejected | Regex too strict/loose | Align with local `useradd` policy |
| getent missing entries | NSS/LDAP lab | Document scope as local files only |

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
- [`Functions Parameters And Locals`](../shell/functions-parameters-and-locals.md)
- [`Control Flow Conditionals`](../shell/control-flow-conditionals.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
