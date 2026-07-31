---
title: "Troubleshooting Shell Scripts"
description: "Debug Bash failures: common errors, permissions, cron environment issues, expansion bugs, and performance optimisation."
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - debug
  - permissions
  - cron
  - performance
prerequisites:
  - Production Shell Scripting
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Troubleshooting Shell Scripts

## Overview

When a script works locally and fails in CI or cron, method beats guessing. This tutorial is your incident checklist.

This is **Tutorial 18** in **Module 18: Troubleshooting** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Production Shell Scripting
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Troubleshooting Shell Scripts” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Troubleshooting Shell Scripts](../assets/excalidraw/shell-troubleshooting.svg)

## Theory

### What it is

**Troubleshooting shell scripts** is a systematic way to reproduce failures, isolate causes, and fix them without guesswork. You align the interpreter and environment with production, interpret common error messages, chase permission and cron-specific quirks, inspect variable expansions, and — when needed — profile slow loops. The goal is a short feedback cycle: same symptoms under a controlled `env`, a precise `bash -x` trace, and a verified fix.

### Why it matters

“Works on my machine” is the default state of unfinished automation. Continuous Integration (CI) runners, cron, and service accounts see different `PATH` values, working directories, and security modules. Without a method, engineers change random lines until the symptom moves. A repeatable troubleshooting approach saves hours in outages and prevents “fixes” that only mask the real fault — for example silencing `set -u` instead of supplying a required variable.

### How it works

Reproduce with the same interpreter and a minimal environment: `env -i PATH=/usr/bin:/bin HOME="$HOME" bash -x ./script.sh`. Bisect by wrapping suspect regions with `set -x` / `set +x`. Confirm the shebang, execute bit, and line endings (`file`, `sed -n l`) — Windows CRLF produces baffling syntax errors.

Map symptoms to likely causes, then verify. Permission problems involve the execute bit, directory search (`x`) bits, `noexec` mounts, SELinux/AppArmor denials, and a scheduler user that is not you. Cron issues add a short `PATH`, unexpected cwd, no tty, and stderr mailed somewhere nobody reads — fix with absolute paths, explicit `PATH`, and file logs. For expansion bugs, compare quoted versus unquoted forms, know `${var:-}` versus `${var-}`, and print `declare -p var` while debugging.

When the script is correct but slow, reduce process churn: avoid needless pipelines in tight loops, batch with `xargs`, prefer builtins for simple strings, and collapse heavy JSON work into one `jq` call. Profile with `time` before and after.

### Key concepts

| Symptom | Likely cause |
|---------|--------------|
| `command not found` | `PATH`, typo, or missing package |
| `unbound variable` | `set -u` without a default or export |
| `unexpected token` | CRLF line endings or broken quoting |
| `Permission denied` | Mode, `noexec`, directory bits, MAC |
| Works in SSH, fails in cron | Env, cwd, `PATH`, missing tty |
| Slow loops | Too many process spawns per iteration |

### Common pitfalls

- Debugging under a full interactive environment that hides cron/`PATH` issues
- “Fixing” failures by adding `\|\| true` instead of finding the root cause
- Ignoring CRLF after editing scripts on Windows
- Overlooking that the service user lacks execute permission on a directory in the path
- Premature micro-optimisation before confirming the hot loop with `time`

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab18 && cd ~/rebash-shell/lab18
```

**Focus:** reproduce cron env; fix quoting bug; bash -x; time a hot loop

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab18 troubleshooting-shell-scripts on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Troubleshoot checklist

```bash
cat > broken.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
# Intentionally awkward — fix in place:
target='my file'
touch "$target"
ls -l -- "$target"
EOF
chmod +x broken.sh
# Minimal env like cron:
env -i PATH=/usr/bin:/bin HOME="$HOME" bash -x ./broken.sh 2>&1 | tee trace.txt
cat > checklist.md << 'EOF'
- [ ] Same shebang / bash version
- [ ] PATH and cwd
- [ ] Permissions / noexec
- [ ] Quoting
- [ ] Cron user vs your user
EOF
time bash -c 'n=0; while (( n < 1000 )); do n=$((n+1)); done'
```

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab18/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Troubleshooting Shell Scripts** always combines:

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

**Troubleshooting Shell Scripts** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Production Shell Scripting](production-shell-scripting.md) *(previous)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
