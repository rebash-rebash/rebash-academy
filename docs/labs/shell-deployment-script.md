---
title: "Lab — Build a Deployment Script"
description: "Ship a dry-run-aware deployment wrapper with health checks, rollback hooks, and locks."
difficulty: advanced
estimated_time: "55–70 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Build a Deployment Script

## Lab Overview

**Purpose:** Create a production-shaped deploy script for a static app artefact.

**Scenario:** A demo site artefact must be released to `/var/tmp/rebash-app` (lab) with rollback.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

You implement download/stage/activate/healthcheck/rollback with flock and dry-run.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Implement staged deploy directories
- [ ] Support `--dry-run`
- [ ] Health-check after activate
- [ ] Rollback to previous release on failure
- [ ] Prevent overlapping deploys with flock

## Prerequisites

### Knowledge

- [Production Shell Scripting](../shell/production-shell-scripting.md)
- [Process Automation — Signals and Traps](../shell/process-automation-signals-and-traps.md)
- [Networking Automation with Shell](../shell/networking-automation-with-shell.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| curl or local artefact | lab |
| flock | util-linux |

**Estimated cost:** £0.

## Environment

Linux host; deploy only under lab paths.

## Initial State

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-shell/deploy/{releases,shared,logs}
cd ~/rebash-lab-shell/deploy
mkdir -p artefact
echo 'ok' > artefact/index.html
echo 'ok' > artefact/healthz
```

## Lab Tasks

### Task 1 — Layout

- `releases/<id>/` — immutable release trees
- `current` — symlink to active release
- `shared/` — persistent config

### Task 2 — `deploy.sh`

Steps: lock → stage → activate symlink → health check (file exists / curl local) → unlock.

On health failure: relink previous release.

### Task 3 — Dry-run

`--dry-run` prints steps without changing `current`.

### Task 4 — Validate

```bash
./deploy.sh --source ./artefact --dry-run
./deploy.sh --source ./artefact
readlink current
```


## Validation

- [ ] First deploy creates `current` symlink
- [ ] Failed health check rolls back
- [ ] Concurrent deploy blocked by flock
- [ ] Dry-run makes no changes

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| Broken symlink | Activate order wrong | Create new link then `mv -Tf` |
| Rollback target missing | First deploy | Fail closed with clear error |

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

- [`Production Shell Scripting`](../shell/production-shell-scripting.md)
- [`Process Automation Signals And Traps`](../shell/process-automation-signals-and-traps.md)
- [`Troubleshooting Shell Scripts`](../shell/troubleshooting-shell-scripts.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
