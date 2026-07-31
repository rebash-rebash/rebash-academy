---
title: "Error Handling, Logging, and Debugging"
description: "Exit codes, traps, defensive programming, structured logging, and Bash debugging techniques for production scripts."
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - errors
  - logging
  - debugging
prerequisites:
  - Scheduling — cron, at, and systemd Timers
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Error Handling, Logging, and Debugging

## Overview

Silent success is how monitors lie. Make failure audible with strict mode, traps, logs, and a clear exit taxonomy.

This is **Tutorial 16** in **Module 16: Error Handling** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Scheduling — cron, at, and systemd Timers
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Error Handling, Logging, and Debugging” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Error Handling, Logging, and Debugging](../assets/excalidraw/shell-error-handling.svg)

## Theory

### What it is

**Error handling, logging, and debugging** turn a happy-path script into something Continuous Integration (CI) and operators can trust. The pillars are documented **exit codes**, **traps** for cleanup and signal translation, **defensive programming** (`set -euo pipefail`, quoting, early validation), structured **logging** on stderr, and disciplined **debugging** with `bash -x` and a useful `PS4` prompt. Together they answer: did it fail, why, and what was left behind?

### Why it matters

Silent success is worse than a loud failure. Swallowing errors with `|| true`, logging to stdout so pipelines parse noise, or shipping without a reproducible debug method creates overnight incidents that look “green” in monitoring. DevOps and Linux admin scripts are usually unattended; the only story they leave is exit status plus logs. Investing in a small taxonomy of codes and consistent log levels pays off every time an on-call engineer opens a file at 02:00.

### How it works

Map failures to documented integers and propagate child failures — do not mask errors you care about. Use `trap` for cleanup and to translate `INT` / `TERM` into known codes. Enable `set -E` if an `ERR` trap must fire inside functions. Defensive defaults include strict mode, quoted expansions, validating arguments before side effects, absolute paths under schedulers, and failing closed when dependencies are missing (`command -v jq >/dev/null`).

Log to stderr with timestamps and levels such as `INFO`, `WARN`, and `ERROR`. Reserve stdout for data or `RESULT` lines that another tool will parse. For debugging, run `bash -x script.sh`, set a precise `PS4` that includes source and line number, and temporarily wrap suspect blocks with `set -x` / `set +x`. Remove noisy traces before merging.

### Key concepts

| Practice | Purpose |
|----------|---------|
| Exit taxonomy | Stable contract for CI and callers |
| `trap` / `ERR` | Cleanup and signal → exit mapping |
| `set -euo pipefail` | Fail fast on errors, unset vars, pipe stages |
| stderr logs | Humans and aggregators; keep stdout clean |
| `bash -x` + `PS4` | Reproduce and locate failing lines |

### Common pitfalls

- Using `|| true` on critical commands to “keep going”
- Printing diagnostics on stdout and breaking `jq` or `grep` consumers
- Logging secrets when dumping environment or request bodies
- Leaving `set -x` enabled in production cron output
- Forgetting cleanup traps so failed runs leave locks that block retries

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab16 && cd ~/rebash-shell/lab16
```

**Focus:** exit taxonomy; ERR/EXIT traps; log levels; bash -x drill

### Step 1 – Logging and debug

```bash
cat > robust.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
log() { printf '[%s] %s\n' "$1" "$2" >&2; }
die() { log ERROR "$1"; exit "${2:-1}"; }
trap 'log ERROR "failed at line $LINENO"' ERR
[[ $# -ge 1 ]] || die "usage: $0 <name>" 2
log INFO "hello $1"
echo "RESULT ok"
EOF
chmod +x robust.sh
./robust.sh lab16
bash -x ./robust.sh lab16 2>&1 | tail -n 15
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-shell/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab16/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Error Handling, Logging, and Debugging** always combines:

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

**Error Handling, Logging, and Debugging** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Scheduling — cron, at, and systemd Timers](scheduling-cron-at-and-timers.md) *(previous)*
- [Production Shell Scripting](production-shell-scripting.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
