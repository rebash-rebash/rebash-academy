---
title: "Lab — Rotate Logs"
description: "Implement simple log rotation with size thresholds, compression, and retention."
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

# Lab — Rotate Logs

## Lab Overview

**Purpose:** Build a lightweight rotator for app logs when logrotate is unavailable or too heavy for a lab.

**Scenario:** A sidecar writes `app.log` that grows without bound on a temporary jump host.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

Before shipping filebeat, ops needs a stop-gap rotation script: rename, gzip, keep last N files.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Rotate when size exceeds a threshold
- [ ] Compress rotated files with gzip
- [ ] Enforce retention count
- [ ] Avoid rotating an empty or missing file incorrectly

## Prerequisites

### Knowledge

- [Linux Admin Automation](../shell/linux-admin-automation.md)
- [File Operations in Shell](../shell/file-operations-in-shell.md)
- [Loops — for, while, until](../shell/loops-for-while-until.md)

### Software

| Tool | Notes |
|------|--------|
| Bash | required |
| gzip | required |
| stat/find | coreutils |

**Estimated cost:** £0.

## Environment

Any Linux host under `~/rebash-lab-shell/rotate`.

## Initial State

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-shell/rotate/logs
cd ~/rebash-lab-shell/rotate
# Grow a fake log
python3 - <<'PY'
from pathlib import Path
p = Path('logs/app.log')
p.write_text('line\n' * 200000)
print(p.stat().st_size)
PY
```

## Lab Tasks

### Task 1 — Write `rotate-logs.sh`

Arguments: `--file`, `--max-bytes`, `--keep` (default 5).

Behaviour:

1. If file missing → exit 0 (nothing to do) or exit 2 if `--strict`
2. If size < max → exit 0
3. Else move to `app.log.YYYYMMDD-HHMMSS` and `gzip`
4. Truncate/recreate original (or reopen-friendly rename pattern)
5. Delete older compressed files beyond `--keep`

### Task 2 — Validate

```bash
./rotate-logs.sh --file logs/app.log --max-bytes 10000 --keep 3
ls -la logs/
./rotate-logs.sh --file logs/app.log --max-bytes 10000 --keep 3
```


## Validation

- [ ] Large log is rotated and gzipped
- [ ] Original log path exists after rotation
- [ ] Only `--keep` compressed files remain
- [ ] Small logs are left untouched

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| gzip: not found | Minimal image | Install gzip |
| Race with writer | App keeps FD open | Document copytruncate vs rename; prefer proper logrotate in prod |
| Too many files remain | Glob/order bug | Sort by mtime before deletion |

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
- [`File Operations In Shell`](../shell/file-operations-in-shell.md)
- [`Loops For While Until`](../shell/loops-for-while-until.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
