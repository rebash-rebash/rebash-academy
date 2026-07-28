---
title: Process Management
description: Monitor and control Linux processes with ps, top, signals, kill, nice, renice, and job control.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - processes
  - signals
  - performance
prerequisites:
  - Complete User and Group Management or equivalent experience
  - Familiarity with basic shell usage
comments: false
---

# Process Management

## Overview

A **process** is a running instance of a program — identified by a Process ID (PID), owned by a user, consuming CPU and memory, and existing in a parent-child tree rooted at PID 1 (systemd on modern distributions). Administrators monitor processes to diagnose performance issues, terminate runaway jobs, adjust scheduling priority, and understand system behaviour during incidents.

This tutorial is part of **Module 3: Processes, Services & Packages** in the REBASH Academy Linux series. You will list and filter processes, interpret CPU/memory columns, send signals for graceful and forced termination, manage background jobs, and understand zombie and orphan process states.

## Prerequisites

- Complete [User and Group Management](user-and-group-management.md) or equivalent experience
- A Linux VM or local machine with terminal access
- Optional: `htop` package for enhanced monitoring (`sudo apt install htop` or `sudo dnf install htop`)
- `sudo` for `renice` on processes owned by other users

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] List and filter processes using `ps`, `pgrep`, and `pidof`
- [ ] Monitor real-time resource usage with `top` and `htop`
- [ ] Send signals with `kill` and interpret SIGTERM vs SIGKILL behaviour
- [ ] Adjust CPU scheduling priority using `nice` and `renice`
- [ ] Manage foreground/background jobs with `&`, `jobs`, `fg`, and `bg`
- [ ] Identify and resolve zombie and orphan process conditions

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Process states

| State | Code | Meaning |
|-------|------|---------|
| Running | R | Executing or ready to run |
| Sleeping | S | Waiting for an event (interruptible) |
| Disk sleep | D | Uninterruptible I/O wait |
| Stopped | T | Paused (SIGSTOP / Ctrl+Z) |
| Zombie | Z | Exited but entry remains until parent reaps |
| Dead | X | Fully terminated (transient) |

View states in `ps aux` (STAT column) or `ps -eo pid,stat,cmd`.

### The process tree

Every process except PID 1 has a parent (PPID). When a parent dies before its child, the child becomes an **orphan** and is adopted by PID 1 (systemd), which reaps it on exit.

A **zombie** is a process that has exited but whose parent has not called `wait()` to read its exit status. Zombies consume no CPU or memory (only a kernel slot) but indicate a buggy parent. Kill the **parent**, not the zombie, to clean up.

### CPU priority (nice values)

Nice values range from **-20** (highest priority) to **+19** (lowest). Default is 0.

- Regular users can only **increase** nice (lower priority): `nice -n 10 command`
- Root can set any value: `nice -n -5 command`
- `renice` adjusts running processes

Nice affects CPU scheduling, not I/O priority (see `ionice` for disk).

### Signals

Signals are software interrupts delivered by the kernel. Common signals:

| Signal | Number | Default action | Typical use |
|--------|--------|----------------|-------------|
| SIGHUP | 1 | Terminate | Reload config (many daemons trap this) |
| SIGINT | 2 | Terminate | Ctrl+C in terminal |
| SIGTERM | 15 | Terminate | Graceful shutdown (default `kill`) |
| SIGKILL | 9 | Kill | Force immediate termination |
| SIGSTOP | 19 | Stop | Pause process (cannot be caught) |
| SIGCONT | 18 | Continue | Resume stopped process |

**Always try SIGTERM first.** SIGKILL cannot be caught or ignored — resources (temp files, locks) may be left inconsistent.

### Background jobs and job control

Shell job control tracks pipelines started in the current session:

- `command &` — run in background
- `Ctrl+Z` — suspend foreground job
- `jobs` — list jobs
- `fg %1` — bring job 1 to foreground
- `bg %1` — resume job 1 in background

Job numbers (`%1`) are shell-local; PIDs are system-wide.

### ps output formats

| Command | Style | Notes |
|---------|-------|-------|
| `ps aux` | BSD | `a`=all users, `u`=user-oriented, `x`=no terminal |
| `ps -ef` | UNIX | Full format listing |
| `ps -eo pid,ppid,stat,cmd` | Custom | Script-friendly columns |

`top` and `htop` show live snapshots sorted by CPU (press `P`) or memory (`M`).

## Hands-on Lab

### Step 1 – List processes with ps

```bash
ps aux | head -8
ps -ef | grep -E "PID|systemd" | head -5
ps -eo pid,ppid,user,stat,pcpu,pmem,cmd --sort=-pcpu | head -10
```

**Expected output:**

```text
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 169000 12000 ?        Ss   09:00   0:02 /sbin/init
root       456  0.0  0.2  50000  8000 ?        Ss   09:00   0:00 sshd: /usr/sbin/sshd
...
  PID  PPID USER     STAT %CPU %MEM CMD
 1234     1 root     Ss    0.0  0.1 /usr/lib/systemd/systemd --user
```

Top CPU consumers appear first in the custom sort output.

### Step 2 – Find processes by name

```bash
pgrep -l bash
pidof systemd
ps aux | grep "[s]shd"
```

**Expected output:**

```text
1234 bash
1
root  456  0.0  0.2  ... sshd: /usr/sbin/sshd
```

The `[s]shd` trick prevents grep from matching itself.

### Step 3 – Monitor with top (batch mode)

```bash
top -b -n 1 | head -20
```

**Expected output:**

```text
top - 14:30:01 up 5:30,  1 user,  load average: 0.08, 0.04, 0.01
Tasks: 120 total,   1 running, 119 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  1.1 sy,  0.0 ni, 96.4 id,  0.2 wa,  0.0 hi,  0.0 si
MiB Mem :   7945.0 total,   3200.0 free,   2100.0 used,   2645.0 buff/cache
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 user      20   0  123456   45678   8901 S   5.0   0.6   0:12.34 python3
```

Note the **zombie count** in the Tasks line — should be 0 on healthy systems.

### Step 4 – Start, background, and manage jobs

```bash
sleep 300 &
sleep 400 &
jobs -l
```

**Expected output:**

```json
[1] 5678
[2] 5679
[1]  5678 Running                 sleep 300 &
[2]  5679 Running                 sleep 400 &
```

Bring job 1 to foreground, suspend, resume in background:

```bash
fg %1
# Press Ctrl+Z
jobs
bg %1
jobs
```

**Expected output after Ctrl+Z:**

```json
[1]+  Stopped                 sleep 300
[1]+ Running                 sleep 300 &
```

### Step 5 – Send signals gracefully and forcefully

```bash
sleep 600 &
SLEEP_PID=$!
kill -0 $SLEEP_PID && echo "Process $SLEEP_PID exists"
kill $SLEEP_PID          # SIGTERM (default)
wait $SLEEP_PID 2>/dev/null; echo "Exit code: $?"
```

**Expected output:**

```json
[1] 5680
Process 5680 exists
Exit code: 143
```

Exit code 143 = 128 + 15 (SIGTERM). Test SIGKILL on a stubborn process:

```bash
sleep 600 &
SP=$!
kill -9 $SP
wait $SP 2>/dev/null; echo "Exit code: $?"
```

**Expected output:** `Exit code: 137` (128 + 9).

### Step 6 – Adjust priority with nice and renice

```bash
nice -n 10 sleep 300 &
NPID=$!
ps -o pid,ni,cmd -p $NPID
sudo renice -n -5 -p $NPID
ps -o pid,ni,cmd -p $NPID
kill $NPID
```

**Expected output:**

```text
  PID  NI CMD
 5681  10 sleep 300
5681 (process ID) old priority 10, new priority -5
  PID  NI CMD
 5681  -5 sleep 300
```

Only root can lower nice below 0.

### Step 7 – Observe a zombie process

Run this in a subshell to create a short-lived zombie:

```bash
bash -c 'sleep 1 & exec sleep 30' &
ZOMBIE_PARENT=$!
sleep 2
ps -o pid,ppid,stat,cmd -p $ZOMBIE_PARENT
ps aux | awk '$8 ~ /Z/ {print}'
kill $ZOMBIE_PARENT
sleep 1
ps aux | awk '$8 ~ /Z/ {print}' || echo "No zombies"
```

**Expected output:**

```text
  PID  PPID STAT CMD
 5690  1234 S    sleep 30
 5689  5690 Z    [sleep] <defunct>
No zombies
```

Killing the parent allows systemd (PID 1) to reap the zombie.

### Step 8 – Inspect process tree

```bash
pstree -p $$ | head -5
pstree -p -s $(pgrep -n sshd 2>/dev/null || pgrep -n systemd)
```

**Expected output:**

```text
bash(5700)───pstree(5705)
systemd(1)───sshd(456)───sshd(890)───bash(5700)
```

Shows parent-child relationships with PIDs in parentheses.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `ps aux` | Snapshot of all processes (BSD format) |
| `ps -ef` | Full listing (UNIX format) |
| `ps -p PID -o stat,cmd` | Show state and command for one PID |
| `pgrep -l NAME` | Find PIDs by name, show name |
| `pidof PROCESS` | Print PIDs of running binary |
| `top` | Interactive real-time monitor |
| `top -b -n 1` | Single batch snapshot (scripting) |
| `htop` | Enhanced interactive monitor |
| `kill PID` | Send SIGTERM (15) to process |
| `kill -9 PID` | Send SIGKILL (force) |
| `kill -HUP PID` | Send SIGHUP (reload on many daemons) |
| `kill -0 PID` | Test if process exists (no signal sent) |
| `killall NAME` | Signal all processes matching name |
| `nice -n 10 CMD` | Start command with lower priority |
| `renice -n 5 -p PID` | Change nice of running process |
| `jobs -l` | List shell background jobs with PIDs |
| `fg %N` | Bring job N to foreground |
| `bg %N` | Resume stopped job N in background |
| `pstree -p` | Display process tree with PIDs |
| `lsof -p PID` | List open files for a process |

## Code Examples

### Find top memory consumers

```bash
#!/bin/bash
# top-mem.sh — report top 10 processes by RSS memory
set -euo pipefail

echo "PID    %MEM   RSS(KB)  COMMAND"
ps -eo pid,pmem,rss,cmd --sort=-rss | head -11 | tail -10 \
  | awk '{printf "%-6s %-6s %-8s %s\n", $1, $2, $3, $4" "$5" "$6}'
```

### Graceful shutdown with timeout

```bash
#!/bin/bash
# graceful-stop.sh — SIGTERM then SIGKILL after timeout
set -euo pipefail

PID="${1:?Usage: $0 <pid>}"
TIMEOUT="${2:-15}"

kill -TERM "$PID" 2>/dev/null || { echo "Process not found"; exit 1; }

for i in $(seq 1 "$TIMEOUT"); do
  kill -0 "$PID" 2>/dev/null || { echo "Stopped gracefully"; exit 0; }
  sleep 1
done

echo "Sending SIGKILL"
kill -9 "$PID"
```

### Detect zombie processes

```bash
#!/bin/bash
# check-zombies.sh — alert if zombies present
set -euo pipefail

ZOMBIES=$(ps aux | awk '$8 ~ /Z/ {count++} END {print count+0}')

if [[ "$ZOMBIES" -gt 0 ]]; then
  echo "WARNING: $ZOMBIES zombie process(es) detected"
  ps aux | awk '$8 ~ /Z/ {print}'
  exit 1
fi
echo "OK: no zombies"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Using kill -9 as the first resort"
    SIGKILL bypasses cleanup handlers. Databases, web servers, and file writers may corrupt data. Always try SIGTERM and wait before escalating.

!!! warning "Killing zombie PIDs directly"
    Zombies are already dead — killing them has no effect. Terminate or restart the **parent** process that failed to reap.

!!! warning "Confusing shell job IDs with PIDs"
    `kill %1` is shell job control; `kill 5680` uses a PID. Mixing them causes "no such process" errors.

!!! warning "Monitoring only CPU, ignoring D state"
    Processes in uninterruptible sleep (D) indicate stuck I/O — often NFS or disk issues. High D-state counts need storage investigation, not more CPU.

## Best Practices

!!! tip "Use SIGTERM then escalate"
    Production runbooks: `kill -15 PID`, wait 30s, verify with `kill -0 PID`, then `kill -9 PID` if needed.

!!! tip "Correlate with systemd for services"
    Prefer `systemctl stop UNIT` over raw `kill` for managed services — systemd handles dependencies and restart policy.

!!! tip "Set ulimits and cgroup limits"
    Prevent fork bombs and runaway memory with `/etc/security/limits.conf` and systemd `MemoryMax=` in unit files.

!!! tip "Capture ps snapshots during incidents"
    `ps auxww > /tmp/ps-$(date +%s).txt` preserves full command lines for post-mortem analysis.

!!! tip "Use htop filters in busy systems"
    Press `F4` in htop to filter by process name; `/` searches in top.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Process won't die | Ignoring SIGTERM or D-state I/O | Wait; check `stat`; use SIGKILL; investigate stuck NFS/disk |
| Zombie count growing | Parent not calling wait() | Identify parent with `ps -o ppid= -p ZPID`; restart parent service |
| High load, low CPU | I/O wait or many blocked threads | Check `wa` in top; use `iostat`, `iotop` |
| Cannot renice | Insufficient privileges | Regular users cannot lower nice below current; use sudo |
| kill: Operation not permitted | Different user's process | Use sudo or kill as root |
| Background job exits on logout | SIGHUP sent to shell | Use `nohup`, `disown`, or systemd service instead |
| Wrong process killed | Name collision with killall | Use PID from `pgrep` instead of `killall` |

## Summary

- Processes form a tree under PID 1; each has a state, owner, and resource consumption profile.
- Use `ps`, `pgrep`, and `top`/`htop` to monitor; sort by CPU and memory to find bottlenecks.
- Send **SIGTERM** for graceful shutdown; reserve **SIGKILL** for unresponsive processes.
- **Nice** values adjust CPU priority; root can favour critical workloads with negative nice.
- Shell **job control** manages background tasks in interactive sessions; use systemd for persistent services.
- **Zombies** indicate parent bugs — fix the parent. **Orphans** are adopted by systemd automatically.

## Interview Questions

**1. What is the difference between SIGTERM and SIGKILL?**

*Sample answer:* SIGTERM (15) asks a process to terminate gracefully — it can catch the signal, flush buffers, and close connections. SIGKILL (9) forces immediate termination and cannot be caught. Always try SIGTERM first.

**2. How do you find the top 5 CPU-consuming processes?**

*Sample answer:* `ps -eo pid,pcpu,cmd --sort=-pcpu | head -6` or interactively in top by pressing `P` to sort by CPU.

**3. What is a zombie process, and how do you remove it?**

*Sample answer:* A zombie (state Z) has exited but remains in the process table until its parent calls wait(). It uses no CPU/memory. Kill or restart the parent process; killing the zombie PID does nothing.

**4. What happens to orphan processes?**

*Sample answer:* When a parent dies before its child, the child is reparented to PID 1 (systemd). Systemd becomes the new parent and reaps the child when it exits.

**5. Explain nice value -20 vs +19.**

*Sample answer:* Nice ranges from -20 (highest CPU priority) to +19 (lowest). Default is 0. Regular users can only increase nice (lower priority). Root can set -20 for critical processes.

**6. What does exit code 137 indicate?**

*Sample answer:* 137 = 128 + 9, meaning the process was killed by SIGKILL. Similarly, 143 = 128 + 15 (SIGTERM).

**7. How do you run a command in the background and keep it after logout?**

*Sample answer:* For ad-hoc tasks: `nohup command & disown`. For production workloads, create a systemd service unit instead of relying on nohup.

**8. What is the difference between `ps aux` and `ps -ef`?**

*Sample answer:* Both list processes but use different column sets and syntax (BSD vs UNIX style). `ps aux` shows %CPU/%MEM; `ps -ef` shows full command with PPID in a familiar UNIX format.

**9. When would you see a process in D state?**

*Sample answer:* D (uninterruptible sleep) means the process waits on I/O that cannot be interrupted — typically disk or NFS. Many D-state processes suggest storage or network filesystem problems.

**10. How do you verify a PID exists without killing it?**

*Sample answer:* `kill -0 PID` sends signal 0, which performs error checking without sending a signal. Also: `ps -p PID` or `test -d /proc/PID`.

1. How would you explain process management to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore process management?
3. Which metrics or logs would you check first when process management misbehaves?
4. What is a secure default related to process management?
5. How would you validate a change involving process management in CI or a staging environment?
6. What trade-off would you accept to simplify operations around process management?
7. Describe a common anti-pattern with process management and how you fix it.
8. How does process management interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for process management?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [User and Group Management](user-and-group-management.md) *(previous)*
- [systemd Service Management](systemd-service-management.md) *(next)*
- [Log Management with journalctl](log-management-journalctl.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [ps man page](https://man7.org/linux/man-pages/man1/ps.1.html)
- [signal man page](https://man7.org/linux/man-pages/man7/signal.7.html)
- [nice man page](https://man7.org/linux/man-pages/man1/nice.1.html)
- [Process states – Linux kernel docs](https://www.kernel.org/doc/html/latest/filesystems/proc.html)
- [REBASH Academy – Linux Overview](index.md)
