---
title: "Process Automation — Signals and Traps"
description: "Control processes with ps, kill, jobs, and wait; clean up safely with Bash trap on EXIT, INT, and TERM."
difficulty: intermediate
estimated_time: "50–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: shell
technology: shell
module: "Module 11 · Process Automation"
tags:
  - shell
  - bash
  - process
  - signals
  - trap
prerequisites:
  - shell/text-processing-in-shell-scripts
next:
  - shell/linux-admin-automation
related:
  - shell/error-handling-logging-and-debugging
interview: interview/shell
comments: false
---

# Process Automation — Signals and Traps

## Overview

Long jobs, background workers, and **cleanup when a script is interrupted** separate hobby scripts from production automation. On Linux, a running program is a **process**. You inspect processes with `ps`, stop them with `kill`, run work in the background with `&`, and join children with `wait`. When someone presses Ctrl-C, or systemd stops a unit, the kernel delivers a **signal**. Bash can catch signals with **`trap`** so you remove temp files and stop children instead of leaving a mess.

This is **Tutorial 11** in **Module 11: Process Automation** of the REBASH Academy **Shell Scripting for DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small trap demo under `~/rebash-shell/lab11` that you can explain in an interview or a change ticket.

In Continuous Integration (CI), cloud virtual machines (VMs), and maintenance windows, orchestrators stop workloads with `SIGTERM`, not with a polite message. A backup script without an `EXIT` trap may leave lock files that block the next run. A broad `pkill -f` can stop a teammate’s job on a shared jump server. Learn the lifecycle: start → observe → signal → clean up → prove the trap ran.

## Prerequisites

- [Text Processing in Shell Scripts](text-processing-in-shell-scripts.md)
- Bash 4.2+ on Linux (Ubuntu 22.04/24.04 practice VM, WSL2, or similar)
- Comfort with `set -euo pipefail` and executable scripts

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what signals (`SIGINT`, `SIGTERM`, `EXIT`) mean for a Bash script
- [ ] Register a `trap` that cleans up temp files and background children
- [ ] Start a background job, stop it with `kill`, and join with `wait`
- [ ] Prove that a trap ran by writing a marker file on exit or interrupt
- [ ] Avoid broad `pkill` patterns and prefer graceful `TERM` before `KILL`

## Architecture

Scripts sit between humans or schedulers and Linux processes. Signals ask the process to stop; traps decide what cleanup runs before the shell exits.

![Architecture diagram for Process Automation — Signals and Traps](../assets/excalidraw/shell-process-automation.svg)

## Theory

### What it is

A **process** is a running program with a process ID (PID). **`ps`** lists processes. **`kill`** sends a signal to a PID (default is `TERM`). **`jobs`**, **`&`**, and **`wait`** manage background work started by the current shell. A **signal** is a small message from the kernel (for example Ctrl-C → `SIGINT`, stop request → `SIGTERM`). Bash **`trap`** runs a command or function when a named signal arrives, or when the shell exits (`EXIT`).

```bash
ps -o pid,ppid,stat,cmd
kill -TERM "$pid"
trap 'rm -rf "$WORKDIR"' EXIT
```

### Why it matters

Schedulers and container runtimes stop jobs with signals. If your script ignores cleanup, the next run may fail on a stale lock, or temp directories fill the disk. Shared hosts make pattern-based kills dangerous. Clear traps and narrow kill targets keep automation safe for CI steps, deploy helpers, and overnight admin scripts.

### How it works

1. **Inspect** — `ps -ef`, `ps -o pid,stat,cmd`, or `pgrep -a name`.
2. **Background** — `cmd &` starts a child; `jobs -l` shows shell-owned jobs; `wait` joins them.
3. **Signal** — `kill -TERM pid` asks for a graceful stop; `kill -KILL` (`-9`) is last resort and skips cleanup inside the target.
4. **Trap** — register handlers early:

```bash
cleanup() {
  rm -rf "${WORKDIR:-}"
  [[ -n "${CHILD_PID:-}" ]] && kill -TERM "$CHILD_PID" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
```

Keep trap bodies short and idempotent: remove temps and locks, stop children, then exit. Avoid slow network calls inside traps.

`nohup cmd &` survives hangup for ad-hoc work, but long-lived services belong under **systemd**, not `nohup` forever.

### Key concepts and comparisons

| Tool / signal | Role |
|---------------|------|
| `ps` / `pgrep` | Inspect running processes |
| `kill -TERM` | Graceful stop (preferred first) |
| `kill -KILL` | Force stop; skip target cleanup |
| `pkill` | Match by name — use narrow patterns |
| `wait` | Join background children; collect status |
| `SIGINT` / `SIGTERM` | Ctrl-C / orchestrator stop |
| `trap` … `EXIT` | Cleanup when the shell ends |

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| `trap` + `EXIT` | Temp dirs, lock files, child PIDs | Complex logic inside the handler |
| `kill -TERM` then wait | Controllable children | Skipping wait and assuming death |
| Narrow PID or exact name | Shared hosts | Broad `pkill -f` on short strings |
| systemd unit | Long-lived services | Forever `nohup` “services” |

### Common pitfalls

- Using `kill -9` first and skipping graceful shutdown.
- Broad `pkill -f` patterns that match unrelated processes.
- Forgetting `trap`, so interrupted runs leave locks and temp trees.
- Putting slow or failing network calls inside trap handlers.
- Starting production services with `nohup` instead of a unit file.

## Hands-on Lab

### Objective

Build a Bash script that registers cleanup traps, starts a background sleeper, stops it with `kill`, and **proves the trap ran** by writing a marker file under `~/rebash-shell/lab11`.

### Prerequisites

- `bash`, `kill`, `ps`, `chmod`
- Practice host where you may start short background sleep processes

### Lab environment

Workspace: `~/rebash-shell/lab11`

```bash
mkdir -p ~/rebash-shell/lab11 && cd ~/rebash-shell/lab11
set -euo pipefail
bash --version | head -n1 | tee bash-version.txt
test -n "$(command -v kill)"
```

**Expected output:** `bash-version.txt` exists; `kill` is on `PATH`.

### Real-world scenario

Your deploy helper creates a temp work directory and starts a short helper process. If CI cancels the job (or someone presses Ctrl-C), the helper must stop and the temp directory must go away. Security asks for proof that cleanup ran — a marker file is enough for the change ticket.

### Step-by-step tasks

#### Task 1 – Trap cleanup on EXIT and INT

Write a script that creates a work directory, registers traps, and leaves a marker when cleanup runs.

```bash
cd ~/rebash-shell/lab11
set -euo pipefail

cat > trap-demo.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$ROOT/work"
MARKER="$ROOT/trap-ran.txt"
CHILD_PID=""

cleanup() {
  local ec=$?
  if [[ -n "${CHILD_PID:-}" ]] && kill -0 "$CHILD_PID" 2>/dev/null; then
    kill -TERM "$CHILD_PID" 2>/dev/null || true
    wait "$CHILD_PID" 2>/dev/null || true
  fi
  rm -rf "${WORKDIR:-}"
  date -u +%Y-%m-%dT%H:%M:%SZ > "$MARKER"
  echo "cleanup_ran=yes exit=$ec" | tee -a "$MARKER"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$WORKDIR"
echo "ready" > "$WORKDIR/ready.txt"
echo "workdir=$WORKDIR"
EOF
chmod +x trap-demo.sh
```

**Expected output:** `trap-demo.sh` is executable.

#### Task 2 – Background job and kill demo

Extend the script to start a background `sleep`, record its PID, stop it with `TERM`, then exit so the `EXIT` trap runs.

```bash
cd ~/rebash-shell/lab11
set -euo pipefail

cat > trap-demo.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$ROOT/work"
MARKER="$ROOT/trap-ran.txt"
CHILD_PID=""

cleanup() {
  local ec=$?
  if [[ -n "${CHILD_PID:-}" ]] && kill -0 "$CHILD_PID" 2>/dev/null; then
    kill -TERM "$CHILD_PID" 2>/dev/null || true
    wait "$CHILD_PID" 2>/dev/null || true
  fi
  rm -rf "${WORKDIR:-}"
  {
    date -u +%Y-%m-%dT%H:%M:%SZ
    echo "cleanup_ran=yes"
    echo "exit_code=$ec"
    echo "child_pid=${CHILD_PID:-none}"
  } | tee "$MARKER"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

mkdir -p "$WORKDIR"
echo "ready" > "$WORKDIR/ready.txt"

# Background helper (stands in for a long job)
sleep 120 &
CHILD_PID=$!
echo "child_started=$CHILD_PID" | tee child-pid.txt
ps -o pid,stat,cmd -p "$CHILD_PID" | tee child-ps.txt

# Graceful stop (what CI/systemd usually send first)
kill -TERM "$CHILD_PID"
wait "$CHILD_PID" 2>/dev/null || true
echo "child_stopped=yes" | tee child-stopped.txt
CHILD_PID=""   # already reaped; cleanup need not kill again

exit 0
EOF
chmod +x trap-demo.sh

./trap-demo.sh | tee run.log
```

**Expected output:** `child-pid.txt` and `child-stopped.txt` exist; `run.log` shows the child PID; script exits 0.

#### Task 3 – Prove the trap ran

Assert the marker file and that the work directory was removed.

```bash
cd ~/rebash-shell/lab11
set -euo pipefail

test -f trap-ran.txt
grep -q 'cleanup_ran=yes' trap-ran.txt
test ! -d work
grep -q 'child_stopped=yes' child-stopped.txt

# Optional: show INT path briefly (subshell so your terminal stays usable)
rm -f trap-ran-int.txt
bash -c '
  set -euo pipefail
  MARKER="'"$PWD"'/trap-ran-int.txt"
  WORKDIR="'"$PWD"'/work-int"
  cleanup() { rm -rf "$WORKDIR"; echo cleanup_ran=yes | tee "$MARKER"; }
  trap cleanup EXIT
  trap "exit 130" INT
  mkdir -p "$WORKDIR"
  kill -INT $$
' || true
test -f trap-ran-int.txt
grep -q 'cleanup_ran=yes' trap-ran-int.txt
test ! -d work-int

tar -czf process-evidence.tgz \
  bash-version.txt trap-demo.sh run.log \
  child-pid.txt child-ps.txt child-stopped.txt \
  trap-ran.txt trap-ran-int.txt
ls -l process-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** Both marker files contain `cleanup_ran=yes`; `work` and `work-int` are gone; `process-evidence.tgz` is not empty.

### Validation steps

- [ ] `./trap-demo.sh` exits 0 and creates `trap-ran.txt`
- [ ] Background child appears in `child-ps.txt` then is stopped
- [ ] `work/` directory does not remain after the script
- [ ] INT demo writes `trap-ran-int.txt`
- [ ] `process-evidence.tgz` exists under `~/rebash-shell/lab11`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `kill: No such process` | Child already exited | Safe — check with `kill -0` before kill |
| Trap did not write marker | Script killed with `KILL` | Use `TERM`/`INT`; `KILL` cannot be trapped |
| `work/` still present | Cleanup not registered | Put `trap cleanup EXIT` before work starts |
| Marker empty | Wrote after failed `tee` path | Use absolute `ROOT` paths as in the lab |
| `wait: pid is not a child` | PID from another shell | Only `wait` on children of this script |

### Challenge exercise

Add a lock file `lab11.lock` that the script creates at start and removes in `cleanup`. If the lock already exists, exit `2` with a clear stderr message. Prove with a second overlapping run that fails, then remove the lock via a successful run. Keep the artefact as `lock-demo.sh` in the lab folder.

### Learning outcomes

- Registered `EXIT` / `INT` / `TERM` traps with idempotent cleanup
- Started and stopped a background job with evidence
- Proved trap execution with marker files
- Packed evidence suitable for a change ticket

### Cleanup

```bash
cd ~/rebash-shell/lab11
set -euo pipefail
rm -rf work work-int
rm -f lab11.lock
# Keep evidence if you want it; otherwise:
# rm -f process-evidence.tgz *.txt run.log
# Optional: rm -f trap-demo.sh lock-demo.sh
```

## Validation

- [ ] Lab finished under `~/rebash-shell/lab11/` with evidence files
- [ ] You can explain `SIGINT`, `SIGTERM`, and why `EXIT` traps matter
- [ ] You prefer `TERM` before `KILL` and narrow kill targets
- [ ] You can describe one production failure from a missing trap (stale lock or orphan child)

## Code Walkthrough

In real servers, process automation usually follows this order:

1. **Register traps early** — before creating temps or starting children  
2. **Record child PIDs** — kill what you started; do not guess with broad patterns  
3. **Prefer TERM, then wait** — give graceful shutdown a chance  
4. **Keep handlers short** — remove locks/temps; avoid network in traps  
5. **Prove cleanup** — marker file, log line, or empty work directory  

Later, long-lived workers move to systemd. People still review trap design in deploy helpers and CI wrappers.

## Security Considerations

- Never `pkill -f` on short or shared strings on multi-user hosts  
- Do not run cleanup as root unless the work required root  
- Treat PIDs from files as untrusted until you verify the command line  
- Avoid world-writable lock directories (race and hijack risk)  
- Do not log secrets in trap markers or process command lines  

## Common Mistakes

!!! warning "Using `kill -9` first"
    The process cannot run its own cleanup. **Fix:** send `TERM`, wait a few seconds, then `KILL` only if still alive.

!!! warning "Broad `pkill -f backup`"
    Matches unrelated jobs. **Fix:** kill a recorded PID, or match a unique script path.

!!! warning "Creating temps before `trap`"
    An early Ctrl-C leaves junk. **Fix:** set `WORKDIR`, register `trap`, then `mkdir`.

!!! warning "Complex logic inside traps"
    Nested failures hide the original exit code. **Fix:** keep handlers idempotent and small.

## Best Practices

- One purpose per helper script; record PIDs you own  
- Log cleanup to stderr or a small marker file for tickets  
- Use absolute paths for work directories under the lab or app root  
- Pair every long job with an `EXIT` trap before first merge  
- Prefer systemd for services; keep Bash traps for short automation  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Orphan `sleep` after script | Forgot kill/wait | Store `CHILD_PID`; kill in cleanup |
| Trap never runs | Process got `KILL` | Stop with `TERM`/`INT` |
| `Permission denied` on kill | Not the process owner | Run as same user or use sudo carefully |
| Lock blocks forever | Previous crash, no trap | Document lock path; clear after review |
| Works in terminal, fails in CI | Different signals/timeouts | Test with `kill -TERM` against the script PID |

## Summary

Process automation is start, observe, signal, and clean up. Use `ps` and recorded PIDs, prefer graceful `TERM`, and register Bash `trap` handlers so `EXIT` and interrupts remove temps and children. Prove cleanup with a marker file. Next, automate safe host checks in [Linux Admin Automation](linux-admin-automation.md).

## Interview Questions

**1. What is the difference between `SIGINT`, `SIGTERM`, and `SIGKILL` for a Bash script?**

??? success "Reveal answer"
    **`SIGINT`** is usually Ctrl-C from a terminal. **`SIGTERM`** is the normal “please stop” signal from systemd, Docker, or operators using `kill`. Both can be caught with `trap`. **`SIGKILL`** (`kill -9`) cannot be caught or ignored — the kernel stops the process immediately, so Bash traps do not run. Prefer `TERM` first; use `KILL` only as last resort.

**2. Why register `trap cleanup EXIT` before creating a temp directory?**

??? success "Reveal answer"
    If the script is interrupted after `mkdir` but before `trap`, cleanup never runs and temps or locks remain. Register the trap first (or immediately after setting path variables), then create resources. Interviewers want to hear “traps early, then allocate”.

**3. How do you stop a background job you started in the same script without harming other users’ processes?**

??? success "Reveal answer"
    Save `CHILD_PID=$!` after `cmd &`, then `kill -TERM "$CHILD_PID"` and `wait`. Do not use a broad `pkill -f` on a short string on a shared host. Verify with `ps -p` when needed.

**4. Can a trap run if the process receives `SIGKILL`? What does that mean for lock files?**

??? success "Reveal answer"
    No — `SIGKILL` skips user-space handlers. Stale lock files are possible after hard kills or power loss. Design locks with clear ownership, timeouts or documentation, and a known path operators can clear after review.

**5. When would you use `nohup` versus a systemd service unit?**

??? success "Reveal answer"
    Use **`nohup`** for short ad-hoc background work that must survive logout. Use a **systemd unit** (or timer) for anything long-lived that needs restart policy, logs, and proper stop signals. Production services should not depend on `nohup` forever.

**6. How would you prove in a change ticket that your cleanup trap works?**

??? success "Reveal answer"
    Run the script, show a marker file or log line from the trap (`cleanup_ran=yes`), show the work directory is gone, and optionally demonstrate an `INT`/`TERM` path. Attach that evidence. Least surprise is shown by cleanup on both success and interrupt.

**7. What goes wrong if a trap handler calls a slow HTTP API?**

??? success "Reveal answer"
    Stop or cancel paths become unreliable: the handler may hang, fail, or hide the original exit code. Keep traps local and fast (files, PIDs). Do notifications in the main flow after cleanup, or in a separate watchdog.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Overview](index.md)
- [Text Processing in Shell Scripts](text-processing-in-shell-scripts.md) *(previous)*
- [Linux Admin Automation](linux-admin-automation.md) *(next)*
- [Error Handling, Logging, and Debugging](error-handling-logging-and-debugging.md) *(related)*

## References

- [Bash Reference Manual — Signals](https://www.gnu.org/software/bash/manual/html_node/Signals.html) — traps and signals  
- [`kill(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/kill.1.html) — send signals  
- [`ps(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/ps.1.html) — process status  
- Track index: [Shell Scripting for DevOps Engineers](index.md)
