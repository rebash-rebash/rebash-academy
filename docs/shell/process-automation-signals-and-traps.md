---
title: "Process Automation — Signals and Traps"
description: "Inspect and control processes with ps, kill, pkill, nohup, jobs, and wait; handle signals with trap."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - process
  - signals
  - trap
prerequisites:
  - Text Processing in Shell Scripts
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Process Automation — Signals and Traps

## Overview

Long jobs, background workers, and cleanup on interrupt separate hobby scripts from production automation.

This is **Tutorial 11** in **Module 11: Process Automation** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Text Processing in Shell Scripts
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Process Automation — Signals and Traps” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Process Automation — Signals and Traps](../assets/excalidraw/shell-process-automation.svg)

## Theory

### What it is

**Process automation** is how scripts start, observe, stop, and clean up other processes. You inspect with `ps`, signal with `kill` / `pkill`, run background work with `&`, `nohup`, `jobs`, and `wait`, and react to **signals** through Bash **`trap`**. Signals such as `SIGINT` (Ctrl-C), `SIGTERM` (systemd or container stop), and the shell’s `EXIT` pseudo-signal let you shut down gracefully instead of leaving temps, locks, or orphan children behind.

### Why it matters

Schedulers and orchestrators stop workloads with signals, not with a polite chat. A backup script that ignores `SIGTERM` may be killed mid-write; one without an `EXIT` trap may leave lock files that block the next run. Shared hosts make broad `pkill -f` patterns dangerous — you can stop a teammate’s job. Understanding process lifecycle is essential for Continuous Integration (CI) steps, maintenance windows, and any script that spawns helpers.

### How it works

List processes with `ps aux` or `ps -ef`. Request a graceful stop with `kill -TERM pid`; reserve `kill -KILL` for last resort. `pkill -f pattern` matches full command lines — scope carefully. For ad-hoc background work, `nohup cmd &` survives hangup, but long-lived services belong under systemd. Within a script, `jobs` lists background tasks owned by the shell; `wait` blocks until children finish and surfaces their status (pair with `set -o pipefail` where relevant).

Register handlers so cleanup always runs:

```bash
cleanup() { rm -rf "${WORKDIR:-}"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
```

Keep trap handlers short and idempotent: remove temps and locks, then exit with a known code. Avoid complex logic or network calls inside traps.

### Key concepts

| Tool / signal | Role |
|---------------|------|
| `ps` | Inspect running processes |
| `kill -TERM` / `-KILL` | Graceful stop vs last resort |
| `pkill` | Match by name or pattern (use narrow patterns) |
| `wait` | Join background children and collect status |
| `SIGINT` / `SIGTERM` | Interactive interrupt / orchestrator stop |
| `trap` … `EXIT` | Guaranteed cleanup when the shell ends |

### Common pitfalls

- Using `kill -9` first and skipping graceful shutdown
- Broad `pkill -f` patterns that match unrelated processes
- Starting “services” with `nohup` instead of a proper unit file
- Forgetting `trap` so interrupted runs leave locks and temp trees
- Putting slow or failing network calls inside trap handlers

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab11 && cd ~/rebash-shell/lab11
```

**Focus:** ps/pkill safely; background + wait; trap cleanup on EXIT

### Step 1 – Trap and wait

```bash
cat > trap-demo.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
work=$(mktemp -d)
cleanup() { rm -rf "$work"; echo "cleaned" >&2; }
trap cleanup EXIT
echo job >"$work/out"
sleep 0.2 &
wait
ps -o pid,cmd | head
EOF
chmod +x trap-demo.sh
./trap-demo.sh
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-shell/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab11/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Process Automation — Signals and Traps** always combines:

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

**Process Automation — Signals and Traps** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Text Processing in Shell Scripts](text-processing-in-shell-scripts.md) *(previous)*
- [Linux Administration Automation](linux-admin-automation.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
