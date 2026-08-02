---
title: "Error Handling, Logging, and Debugging"
description: "Build Bash scripts with set -euo pipefail, trap ERR, clear exit codes, and logs on both stderr and a file — then prove failures are visible."
difficulty: advanced
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: shell
technology: shell
module: "Module 16 · Error Handling"
tags:
  - shell
  - bash
  - errors
  - logging
  - debugging
  - trap
prerequisites:
  - shell/scheduling-cron-at-and-timers
next:
  - shell/production-shell-scripting
related:
  - shell/process-automation-signals-and-traps
  - shell/production-shell-scripting
labs: []
interview: interview/shell
comments: false
---

# Error Handling, Logging, and Debugging

## Overview

A script that “looks fine” but exits zero after a failed command is dangerous. Continuous Integration (CI), cron, and monitoring tools only see the **exit code** and the **logs**. If those are wrong, on-call engineers see a green job while the backup never ran.

**Error handling** means the script stops (or recovers) when something fails, and returns a clear code. **Logging** means humans and tools can read what happened on stderr and in a file. **Debugging** means you can turn on a trace (`bash -x`) and find the bad line quickly. The usual production default is `set -euo pipefail`, plus a `trap` on `ERR` (and often `EXIT`) so cleanup and a final message always run.

In Cloud and DevOps work, unattended scripts run on jump servers, build agents, and Kubernetes nodes. A missing variable (`set -u`), a silent pipe failure (`pipefail`), or logs mixed into stdout can break parsers and hide outages. Good scripts document exit codes (for example `0` success, `1` usage, `2` missing dependency, `3` work failed) and never swallow errors with blind `|| true` unless you truly mean to ignore that step.

This is **Tutorial 16** in **Module 16: Error Handling** of the REBASH Academy **Shell Scripting for DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small script that logs, traps errors, and fails with a clear code you can show in a change ticket or interview.

## Prerequisites

- [Scheduling — cron, at, and systemd Timers](scheduling-cron-at-and-timers.md)
- Bash 4.2+ on a practice Linux host (Ubuntu 22.04/24.04 VM, WSL2, or similar)
- Comfort with basic scripts, functions, and redirection (`>`, `2>&1`, pipes)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what `set -e`, `-u`, and `-o pipefail` each catch, and when to use them together
- [ ] Install a `trap` on `ERR` (and `EXIT`) that logs the failing line and cleans up
- [ ] Write a `log` helper that writes to stderr and a log file with a timestamp and level
- [ ] Use documented exit codes and prove an intentional failure path
- [ ] Debug a failing run with `bash -x` and a useful `PS4` prompt

## Architecture

Strict mode, traps, and logging sit between your script logic and the operator (or CI). Failures become visible exit codes and log lines instead of silent success.

![Architecture diagram for Error Handling, Logging, and Debugging](../assets/excalidraw/shell-error-handling.svg)

## Theory

### What it is

**Exit codes** are integers a process returns to its parent (`0` usually means success; non-zero means failure). Bash stores the last command’s status in `$?`. **`set -e`** makes the shell exit when a command fails (with some exceptions). **`set -u`** treats unset variables as errors. **`set -o pipefail`** makes a pipeline fail if any stage fails, not only the last one. Together, `set -euo pipefail` is the common “strict mode” for production Bash.

A **`trap`** runs a function when a signal or special event happens. `trap on_err ERR` runs on command failure (with `set -E` so it also fires inside functions). `trap on_exit EXIT` always runs at the end for cleanup. **Logging** should go to stderr for humans and usually also to a rotating or dated file. **Debugging** uses `bash -x` (xtrace) so each command is printed before it runs.

```bash
set -euo pipefail
set -E
trap 'echo "ERR at line $LINENO" >&2' ERR
```

### Why it matters

Schedulers and CI only trust exit status. If `grep` finds nothing and you do not handle it, or a pipe’s middle stage fails under `set -e` without `pipefail`, the job may still report success. Mixing log lines into stdout breaks tools that expect a single `RESULT=...` line. Without a trap, a crash can leave lock files or temp directories behind. Investing in a small exit-code table and one log helper saves hours during night incidents.

### How it works

1. **Enable strict mode** near the top: `set -euo pipefail` (and often `set -E` for ERR traps in functions).
2. **Define exit codes** as named variables or comments (`readonly E_USAGE=1`).
3. **Install traps** for `ERR` (log line + context) and `EXIT` (remove temp dirs / release locks).
4. **Log with a helper** that prefixes `INFO` / `WARN` / `ERROR`, writes to stderr, and appends to a file.
5. **Fail closed** when a required tool is missing: `command -v jq >/dev/null || exit 2`.
6. **Debug** with `PS4='+${BASH_SOURCE[0]}:${LINENO}: '` and `bash -x ./script.sh`.

```bash
log() {
  local level=$1; shift
  local msg="[$(date '+%Y-%m-%dT%H:%M:%S%z')] ${level}: $*"
  printf '%s\n' "$msg" >&2
  printf '%s\n' "$msg" >>"${LOG_FILE}"
}
```

Reserve stdout for machine-readable output. Keep narrative messages on stderr so pipelines stay clean.

### Key concepts and comparisons

| Option | Catches | Typical miss if omitted |
|--------|---------|-------------------------|
| `set -e` | Failed commands | Script continues after `cp`/`curl` failure |
| `set -u` | Unset variables | Empty expansions delete wrong paths |
| `pipefail` | Any failed pipe stage | `false \| true` still looks successful |
| `trap ERR` | Failure site logging | No line number in the log |
| `trap EXIT` | Always-run cleanup | Leftover temp files / locks |

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| Strict mode everywhere | Unattended ops scripts | Interactive one-offs where you explore |
| Documented exit codes | CI and wrappers that branch on status | Random non-zero values with no meaning |
| Logs on stderr + file | Cron / systemd / ticket evidence | Logging only to stdout into a pipe |
| `|| true` | Truly optional steps | Hiding failures you must know about |

### Common pitfalls

- Using `set -e` without `pipefail`, so pipelines lie.
- Logging with `echo` to stdout while another tool parses the same stream.
- Forgetting `set -E`, so `ERR` traps do not fire inside functions.
- Catching every error with `|| true` “to keep the script going”.
- Leaving `set -x` enabled in production (noise and possible secret leakage).

## Hands-on Lab

### Objective

Build a small ops script under `~/rebash-shell/lab16` that uses strict mode, logs to stderr and a file, traps `ERR`, and demonstrates both a successful path and an intentional failure with a clear exit code.

### Prerequisites

- Bash 4.2+ (`bash --version`)
- Standard tools: `date`, `mktemp`, `tee`, `grep`
- No root required

### Lab environment

Workspace: `~/rebash-shell/lab16`

```bash
mkdir -p ~/rebash-shell/lab16 && cd ~/rebash-shell/lab16
set -euo pipefail
bash --version | head -n1 | tee bash-version.txt
command -v bash | tee bash-path.txt
```

**Expected output:** `bash-version.txt` and `bash-path.txt` exist; Bash version is 4.2 or newer.

### Real-world scenario

Your team runs a nightly “preflight” script before a deploy. Platform asks for: (1) strict mode so missing env vars fail loudly, (2) logs on disk for the change ticket, and (3) exit code `3` when a required check fails so the pipeline can stop the deploy. You build and prove that behaviour on a practice host.

### Step-by-step tasks

#### Task 1 – Strict mode script with logging helper

Create `preflight.sh` with `set -euo pipefail`, a log helper, and an EXIT trap that records the final status.

```bash
cd ~/rebash-shell/lab16
set -euo pipefail

cat > preflight.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
set -E

readonly E_OK=0
readonly E_USAGE=1
readonly E_MISSING=2
readonly E_CHECK=3

LOG_FILE="${LOG_FILE:-./preflight.log}"
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/rebash-preflight.XXXXXX")"

log() {
  local level=$1; shift
  local msg="[$(date '+%Y-%m-%dT%H:%M:%S%z')] ${level}: $*"
  printf '%s\n' "$msg" >&2
  printf '%s\n' "$msg" >>"${LOG_FILE}"
}

on_err() {
  local ec=$?
  log ERROR "command failed (exit ${ec}) near line ${BASH_LINENO[0]} in ${FUNCNAME[1]:-main}"
  exit "${ec}"
}

on_exit() {
  local ec=$?
  rm -rf "${WORKDIR}"
  log INFO "cleanup done; final_exit=${ec}"
  return 0
}

trap on_err ERR
trap on_exit EXIT

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    log ERROR "missing required command: $1"
    exit "${E_MISSING}"
  }
}

usage() {
  cat >&2 <<'USAGE'
Usage: preflight.sh [--fail]
  Default: run checks and exit 0.
  --fail:  intentional check failure (exit 3).
USAGE
}

main() {
  local mode=ok
  case "${1:-}" in
    "") ;;
    --fail) mode=fail ;;
    -h|--help) usage; exit "${E_OK}" ;;
    *) usage; exit "${E_USAGE}" ;;
  esac

  : >"${LOG_FILE}"
  log INFO "starting preflight mode=${mode} workdir=${WORKDIR}"
  require_cmd date
  require_cmd mktemp

  # Simulated check artefact
  printf 'host=%s\n' "$(hostname -s 2>/dev/null || echo labhost)" >"${WORKDIR}/host.txt"

  if [[ "${mode}" == "fail" ]]; then
    log ERROR "intentional check failure (deploy gate)"
    exit "${E_CHECK}"
  fi

  log INFO "all checks passed"
  printf 'RESULT=ok\n' 
  exit "${E_OK}"
}

main "$@"
EOF

chmod +x preflight.sh
./preflight.sh | tee success-stdout.txt
test -f preflight.log
grep -F 'all checks passed' preflight.log | tee success-log-snip.txt
grep -F 'final_exit=0' preflight.log
```

**Expected output:** stdout shows `RESULT=ok`; `preflight.log` contains INFO lines and `final_exit=0`.

#### Task 2 – Intentional failure path and exit code

Run the failure mode and capture the exit code. Confirm the ERR/EXIT path logged the problem.

```bash
cd ~/rebash-shell/lab16
set -euo pipefail

set +e
./preflight.sh --fail >fail-stdout.txt 2>fail-stderr.txt
ec=$?
set -e
printf '%s\n' "${ec}" | tee fail-exit-code.txt
test "${ec}" -eq 3

grep -F 'intentional check failure' fail-stderr.txt
grep -E 'final_exit=3|ERROR' preflight.log | tee fail-log-snip.txt
test ! -s fail-stdout.txt || ! grep -q 'RESULT=ok' fail-stdout.txt
```

**Expected output:** `fail-exit-code.txt` contains `3`; stderr and log show the ERROR; no successful `RESULT=ok` on the fail path.

#### Task 3 – Debug with bash -x and evidence pack

Capture an xtrace of the success path, then pack proof files for the ticket.

```bash
cd ~/rebash-shell/lab16
set -euo pipefail

export PS4='+${BASH_SOURCE[0]}:${LINENO}: '
bash -x ./preflight.sh >trace-stdout.txt 2>trace-xtrace.txt
grep -F 'RESULT=ok' trace-stdout.txt
grep -E 'set -euo|log INFO|all checks passed' trace-xtrace.txt | head -n 20 | tee trace-snip.txt

tar -czf error-handling-evidence.tgz \
  bash-version.txt bash-path.txt preflight.sh \
  success-stdout.txt success-log-snip.txt \
  fail-exit-code.txt fail-stderr.txt fail-log-snip.txt \
  trace-snip.txt preflight.log
ls -l error-handling-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** `trace-xtrace.txt` shows expanded commands; `error-handling-evidence.tgz` is non-empty.

### Validation steps

- [ ] `./preflight.sh` exits `0` and prints `RESULT=ok`
- [ ] `./preflight.sh --fail` exits `3`
- [ ] `preflight.log` has timestamped INFO/ERROR lines
- [ ] EXIT cleanup removed the temp workdir (no leftover `rebash-preflight.*` under `/tmp` from this run)
- [ ] `error-handling-evidence.tgz` exists under `~/rebash-shell/lab16`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Script continues after failure | No `set -e` / error in `if` test context | Enable strict mode; put failing checks outside `if cmd` if you need abort |
| `unbound variable` | `set -u` and missing env/arg | Provide the value or use `${VAR:-default}` only when a default is safe |
| Pipeline exit is `0` after middle fail | Missing `pipefail` | Add `set -o pipefail` |
| ERR trap never fires in function | Missing `set -E` | Add `set -E` after strict mode |
| Logs missing from file | Wrong `LOG_FILE` path / never truncated | Set `LOG_FILE` and create/truncate at start of `main` |

### Challenge exercise

Extend `preflight.sh` (or add `preflight-retry.sh`) so a flaky check retries **twice** with `sleep 1`, logs each attempt at WARN, and exits `3` only after the last attempt fails. Prove with a mode that fails every attempt, and save `challenge-exit-code.txt` plus a log snip showing three attempts. Keep the challenge script ShellCheck-friendly (quoted variables, no unused vars).

### Learning outcomes

- Applied `set -euo pipefail` and `set -E` with ERR/EXIT traps
- Logged to stderr and a file with levels and timestamps
- Proved success (`0`) and intentional failure (`3`) with evidence
- Used `bash -x` to capture a debug trace

### Cleanup

```bash
cd ~/rebash-shell/lab16
set -euo pipefail
rm -f preflight.log fail-stdout.txt fail-stderr.txt trace-stdout.txt trace-xtrace.txt
# Keep evidence archive if you want it; otherwise:
# rm -f error-handling-evidence.tgz *.txt
# Optional challenge files:
# rm -f preflight-retry.sh challenge-exit-code.txt
```

## Validation

- [ ] Lab finished under `~/rebash-shell/lab16/` with evidence files
- [ ] You can explain `set -e`, `-u`, and `pipefail` in your own words
- [ ] You can describe why logs belong on stderr while `RESULT` can stay on stdout
- [ ] You know one production failure mode: silent success after a failed pipe stage

## Code Walkthrough

In production Bash for **Error Handling, Logging, and Debugging**, use this order:

1. **Strict mode first** — `set -euo pipefail` (and `set -E` when using ERR traps in functions)  
2. **Name your exit codes** — document them in `--help` or comments  
3. **Trap early** — ERR for context, EXIT for cleanup  
4. **Log with one helper** — stderr + file; levels; timestamps  
5. **Prove both paths** — success and a deliberate failure with captured `$?`  

Later you can add retries and metrics. Start with honest failure.

## Security Considerations

- Do not log secrets, tokens, or full environment dumps  
- Be careful with `set -x` in CI — traces can print credentials from variables  
- Prefer failing closed when a dependency is missing  
- Write log files with tight permissions (`umask 077` or `chmod 600`) on shared hosts  
- Avoid `eval` when handling error messages or user input  

## Common Mistakes

!!! warning "Relying on `set -e` alone for pipelines"
    Only the last command’s status counts without `pipefail`. **Fix:** always use `set -euo pipefail` in ops scripts.

!!! warning "Swallowing errors with `|| true`"
    The job stays green while the real step failed. **Fix:** use `|| true` only for optional steps; log a WARN when you skip.

!!! warning "Writing diagnostics to stdout"
    Parsers and `RESULT` lines get polluted. **Fix:** send human messages to stderr; keep stdout for data.

!!! warning "No EXIT cleanup"
    Temp dirs and lock files remain after crashes. **Fix:** `trap cleanup EXIT` and make cleanup idempotent.

## Best Practices

- Put strict mode and traps in every unattended script  
- Keep a small, documented exit-code table  
- One log function used everywhere (no bare `echo` for ops messages)  
- Capture failure evidence (`$?`, log snip, xtrace) in tickets  
- Turn off xtrace before merge; leave a note on how to enable it for debug  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Exit `0` after a failed `grep` in a pipe | No `pipefail` | Enable `set -o pipefail` |
| `unbound variable` under CI | Env var not passed | Export required vars or fail with `E_USAGE` |
| ERR trap silent inside function | Missing `set -E` | Add `set -E` |
| Log file empty | Redirected only stderr of outer wrapper | Log from inside the script to an absolute path |
| `bash -x` too noisy | Whole script traced | Wrap one block with `set -x` / `set +x` |

## Summary

Error handling makes failures **loud and clear**: strict mode, traps, logs, and documented exit codes. Prove both the happy path and a deliberate failure, then keep the evidence. Next, harden scripts for real production use — ShellCheck, locks, dry-run, and help text — in [Production Shell Scripting](production-shell-scripting.md).

## Interview Questions

**1. What does each part of `set -euo pipefail` do, and why do teams enable all three together?**

??? success "Reveal answer"
    **`-e`** exits when a command fails (with some exceptions). **`-u`** errors on unset variables. **`pipefail`** makes a pipeline fail if any stage fails. Together they catch the three most common silent-failure classes in unattended Bash: ignored command errors, empty expansions, and pipelines that only check the last stage. Interviewers want this concrete mapping, not just “it is best practice”.

**2. When would you still use `|| true` under strict mode?**

??? success "Reveal answer"
    Only for steps that are **truly optional** — for example `rm -f` of a cache file that may not exist, or a best-effort metric push. Log a WARN when you skip important work. Never use `|| true` on deploy gates, backups, or anything CI must trust.

**3. How do `trap ERR` and `trap EXIT` differ, and why enable `set -E`?**

??? success "Reveal answer"
    **`ERR`** runs when a command fails (good for logging line/context). **`EXIT`** always runs when the shell leaves, success or failure (good for cleanup). **`set -E`** (errtrace) lets ERR traps inherit into functions and subshells that would otherwise skip your handler. Production scripts often install both.

**4. Why should operational logs go to stderr while a `RESULT=ok` line goes to stdout?**

??? success "Reveal answer"
    Tools and pipelines often parse **stdout** as data. Human messages on stdout break that contract. Stderr is for diagnostics; a single clear stdout line (or JSON) is for machines. This pattern also keeps `cmd=$(./script)` free of log noise.

**5. A cron job returns success but the backup folder is empty. How do you investigate with error-handling ideas from this module?**

??? success "Reveal answer"
    Reproduce with a minimal environment, enable `bash -x`, confirm `pipefail` and strict mode, and inspect the log file for the last INFO/ERROR. Check whether a pipeline or `|| true` hid a failure, and whether the script’s exit code was overwritten. Fix by failing closed on the backup step and asserting that expected files exist before exit `0`.

**6. How would you design a small exit-code table for a deploy preflight script?**

??? success "Reveal answer"
    Example: `0` success, `1` bad usage/args, `2` missing dependency, `3` check failed, `4` locked/concurrent run. Document the table in `--help` and in the repo README. Wrappers and CI then branch without scraping log text. Keep the table short and stable.

**7. What is a safe way to use `bash -x` in CI without leaking secrets?**

??? success "Reveal answer"
    Trace only on failure or behind a debug flag, redact known secret variable names, avoid printing full `env`, and never commit permanent `set -x` in production paths. Prefer structured ERROR logs with line numbers from an ERR trap for day-to-day ops; use xtrace when you need the exact command expansion.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Overview](index.md)
- [Scheduling — cron, at, and systemd Timers](scheduling-cron-at-and-timers.md) *(previous)*
- [Production Shell Scripting](production-shell-scripting.md) *(next)*
- [Process Automation — Signals and Traps](process-automation-signals-and-traps.md) *(related)*

## References

- [Bash Reference Manual — The Set Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) — `set -e`, `-u`, `pipefail`  
- [Bash Reference Manual — Trap](https://www.gnu.org/software/bash/manual/html_node/Bourne-Shell-Builtins.html) — `trap`  
- [`bash(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/bash.1.html) — Ubuntu man-page  
- Track index: [Shell Scripting for DevOps Engineers](index.md)
