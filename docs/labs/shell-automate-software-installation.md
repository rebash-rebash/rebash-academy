---
title: "Lab — Automate Software Installation"
description: "Idempotent package install script with OS detection, dry-run, and clear exit codes."
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

# Lab — Automate Software Installation

## Lab Overview

**Purpose:** Write a package installer that is safe to re-run and works across apt/dnf family labs.

**Scenario:** Bastion images need curl, jq, and git pre-installed. Manual installs drift between Ubuntu and RHEL clones.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

Platform wants a bootstrap script for lab VMs: detect the package manager, install a package list, and skip packages already present.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Detect apt vs dnf/yum
- [ ] Install packages idempotently
- [ ] Support `--dry-run` and a package list file
- [ ] Fail clearly when the OS is unsupported

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [Production Shell Scripting](../shell/production-shell-scripting.md)
- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| apt or dnf | lab package manager |
| sudo | for real installs |

**Estimated cost:** £0.

## Environment

Ubuntu or Fedora/RHEL-like lab VM.

## Initial State

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-shell/bootstrap
cd ~/rebash-lab-shell/bootstrap
printf '%s\n' curl jq git > packages.txt
```

## Lab Tasks

### Task 1 — Detect package manager

```bash
detect_pm() {
  if command -v apt-get >/dev/null 2>&1; then echo apt
  elif command -v dnf >/dev/null 2>&1; then echo dnf
  elif command -v yum >/dev/null 2>&1; then echo yum
  else echo unsupported; return 1
  fi
}
```

### Task 2 — Build `install-packages.sh`

- Read packages from `packages.txt` or arguments
- `--dry-run` prints planned actions
- Skip packages already installed (`dpkg -s` / `rpm -q`)
- Log to stderr

### Task 3 — Validate

```bash
./install-packages.sh --dry-run
# On a disposable VM only:
# sudo ./install-packages.sh
command -v curl
command -v jq || true
```


## Validation

- [ ] Unsupported OS exits non-zero with a clear message
- [ ] Dry-run never modifies the system
- [ ] Second run skips already-installed packages
- [ ] Package list file is supported

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| apt-get update slow/fails | Mirror or network | Retry; document offline labs |
| Permission denied | Not root | Use sudo or dry-run |
| jq not found after install | Wrong package name on distro | Map package names per PM |

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
- [`Production Shell Scripting`](../shell/production-shell-scripting.md)
- [`Error Handling Logging And Debugging`](../shell/error-handling-logging-and-debugging.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
