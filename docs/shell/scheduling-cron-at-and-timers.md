---
title: "Scheduling — cron, at, and systemd Timers"
description: "Schedule automation with cron, crontab, at, and systemd timers — and make jobs reliable under minimal environments."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - cron
  - at
  - systemd-timers
prerequisites:
  - JSON and YAML with jq and yq
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Scheduling — cron, at, and systemd Timers

## Overview

Schedulers strip your interactive environment. Scripts must set PATH, cwd, logging, and locking themselves.

This is **Tutorial 15** in **Module 15: Scheduling** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- JSON and YAML with jq and yq
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Scheduling — cron, at, and systemd Timers” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Scheduling — cron, at, and systemd Timers](../assets/excalidraw/shell-cron-execution.svg)

## Theory

### What it is

**Scheduling** runs scripts without a human at the keyboard. Classic **cron** uses five time fields plus a command in a crontab; **`at`** queues one-shot jobs for a future moment; **systemd timers** pair a `.timer` unit with a `.service` for calendar or monotonic triggers on modern Linux. The scheduler only starts your process — your script must still set `PATH`, log results, and prevent overlapping runs.

### Why it matters

Backups, certificate renewals, inventory syncs, and housekeeping all depend on unattended execution. The most common production failure is not “cron is broken” but “the job assumed an interactive environment”: missing binaries on a short `PATH`, wrong working directory, or two nightly runs overlapping and corrupting state. Choosing timers versus cron also affects observability: systemd units integrate with the journal and dependency ordering, which Site Reliability Engineering (SRE) and platform teams often prefer.

### How it works

Per-user cron entries come from `crontab -e`; system drop-ins live under `/etc/cron.*`. Five fields set minute, hour, day of month, month, and day of week; the remainder is the command. `at` is useful for deferred maintenance windows but less common for recurring operations.

On hosts with systemd, prefer timers for new work:

```bash
systemctl list-timers --all
systemctl status myjob.timer
```

Timers provide calendar expressions or monotonic delays, ordering relative to other units, and logs via the paired service. Regardless of scheduler, wrap real work in a script with `set -euo pipefail`, an explicit `PATH` (or absolute paths), log redirection to a file or the journal, and a lock file (`flock`) so overlaps do not corrupt backups or databases. Test under a minimal environment that resembles cron before you trust the schedule.

### Key concepts

| Mechanism | Best fit |
|-----------|----------|
| cron / crontab | Simple recurring jobs; wide familiarity |
| `at` | One-shot deferred maintenance |
| systemd timers | Modern hosts; journal + dependencies |
| Wrapper script | Strict mode, `PATH`, logs, lock |
| Lock (`flock`) | Prevent overlapping scheduled runs |

### Common pitfalls

- Depending on interactive `PATH` or aliases inside a cron command line
- Omitting locks so a slow job overlaps the next schedule
- Never reading mailed cron stderr (or having mail disabled)
- Putting complex logic in the crontab instead of a versioned script
- Forgetting that cron’s working directory is not your home project folder

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab15 && cd ~/rebash-shell/lab15
```

**Focus:** cron-ready wrapper; PATH fingerprint; timer vs cron notes

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab15 scheduling-cron-at-and-timers on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Scheduler-ready wrapper

```bash
cat > nightly.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
PATH=/usr/bin:/bin
LOG="$HOME/rebash-shell/lab15/nightly.log"
LOCK="$HOME/rebash-shell/lab15/nightly.lock"
mkdir -p "$(dirname "$LOG")"
exec 9>"$LOCK"
flock -n 9 || { echo "already running" >&2; exit 0; }
exec >>"$LOG" 2>&1
echo "run $(date -Iseconds) PATH=$PATH"
EOF
chmod +x nightly.sh
./nightly.sh
# Example (do not install unless intended):
# */15 * * * * $HOME/rebash-shell/lab15/nightly.sh
# Prefer a systemd timer + service pair on modern hosts.
```

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab15/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Scheduling — cron, at, and systemd Timers** always combines:

1. A clear shebang (`#!/usr/bin/env bash`)
2. Strict mode near the top (`set -euo pipefail`) from Module 2 onward
3. Quoted expansions and explicit tests
4. Functions with `local` for reusable behaviour
5. Documented exit codes and stderr logging

Keep scripts short enough to review in a single merge request. When logic grows (complex JSON APIs, heavy state), hand off to Python and keep Bash as the launcher.

## Security Considerations

- Treat all external input (args, files, env) as untrusted until validated
- Never log secrets; prefer masked CI variables and secret stores
- Prefer least privilege — do not require root for file-local tasks
- Avoid `eval` and unquoted expansions in destructive commands
- Validate paths stay under an allow-listed root before `rm` or overwrite

## Common Mistakes

!!! warning "Skipping strict mode"
    Cron and CI hide failures that an interactive terminal would show. **Fix:** start with `set -euo pipefail` from Module 2 onward.

!!! warning "Unquoted path expansions"
    Spaces and globs rewrite your command line. **Fix:** always `"$path"` / `"$@"`.

!!! warning "Assuming interactive PATH"
    Aliases and fancy PATH entries disappear under schedulers. **Fix:** set `PATH` or use absolute paths.

## Best Practices

- One purpose per script; compose with functions or small binaries
- Log to stderr; reserve stdout for data or RESULT lines
- Idempotent behaviour where scheduling may overlap
- Pair every new script with a failing-path test you actually run
- Run ShellCheck in CI before merging automation

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Works in terminal, fails in cron | PATH / cwd / env | Fingerprint env; set PATH |
| `unbound variable` | `set -u` | Provide defaults or export vars |
| Pipeline “succeeds” incorrectly | Missing `pipefail` | `set -o pipefail` |
| `[[` unexpected operator | Running under `sh`/dash | Fix shebang to Bash |

## Summary

**Scheduling — cron, at, and systemd Timers** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

## Interview Questions

1. How does this topic show up in production Linux administration or CI?
2. What failure mode appears if you ignore quoting or strict mode here?
3. How would you test this behaviour under a minimal cron-like environment?
4. When would you move this logic out of Bash into Python or another tool?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Unquoted expansions and missing `pipefail` create silent or partial failures — especially under cron — that look healthy in monitoring until data is wrong.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Category Overview](index.md)
- [JSON and YAML with jq and yq](json-and-yaml-with-jq-yq.md) *(previous)*
- [Error Handling, Logging, and Debugging](error-handling-logging-and-debugging.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
