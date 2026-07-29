---
title: "Process Management"
description: "Monitor and control processes with ps, top, htop, kill, pkill, jobs, fg, bg, nice, renice, and nohup."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - ps
  - top
  - kill
  - nice
  - jobs
prerequisites:
  - Text Processing with grep, sed, and awk
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Process Management

## Overview

Runaway processes burn CPU budgets on cloud VMs. Lifecycle control is core SRE hygiene.

This is **Tutorial 9** in **Module 6: Process Management** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Text Processing with grep, sed, and awk
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Process Management” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Process Management](../assets/images/linux-process-lifecycle.svg)

## Theory

### Viewing processes

| Tool | Role |
|------|------|
| `ps` | Snapshot (`ps aux`, `ps -ef`, `ps -p PID`) |
| `top` | Interactive live view |
| `htop` | Friendlier interactive view (if installed) |

```bash
ps aux --sort=-%cpu | head
ps -ef | grep '[s]shd'
```

### Signals — kill and pkill

```bash
kill -TERM PID
kill -KILL PID    # last resort
pkill -f 'pattern'
killall -TERM name  # where available
```

Prefer `TERM` then wait; `KILL` skips cleanup.

### Job control

| Command | Role |
|---------|------|
| `jobs` | List shell jobs |
| `fg` | Foreground a job |
| `bg` | Background a stopped job |
| `Ctrl-Z` | Suspend | 

```bash
sleep 300 &
jobs
fg %1
```

### Priority — nice / renice

Lower niceness → higher priority (range typically -20..19). Non-root can only increase niceness.

```bash
nice -n 10 ./batch.sh
renice -n 15 -p PID
```

### nohup

Survive hangup when the terminal closes:

```bash
nohup ./long-job.sh > long-job.out 2>&1 &
```

Prefer `systemd --user` services or timers for production longevity over raw nohup.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab09 && cd ~/rebash-linux/lab09
```

**Focus:** inspect ps/top; job control; nice/nohup a background task

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab09 process-management on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Process control

```bash
ps aux --sort=-%cpu | head -n 8 | tee top-cpu.txt
sleep 120 &
SPID=$!
jobs
renice -n 10 -p "$SPID" || true
kill -TERM "$SPID"
wait "$SPID" 2>/dev/null || true
nohup bash -c 'echo nohup-ok; sleep 2' > nohup-lab.out 2>&1 &
wait || true
cat nohup-lab.out
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab09/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Process Management** always combines:

1. Inspect before you change (`status`, `df`, `ip`, logs)
2. Prefer reversible, documented changes (config management, drop-ins)
3. Capture evidence (command output, journal snippets) for handovers
4. Prefer `systemctl`/`journalctl` and `ip`/`ss` over legacy tools
5. Least privilege — escalate with `sudo` only when required

Keep runbooks short enough to follow at 03:00. Automate the boring checks; keep humans for judgement.

## Security Considerations

- Treat host access and sudo as privileged — audit who can do what
- Never paste secrets into shell history, tickets, or screenshots
- Validate device names and paths before destructive disk or `rm` operations
- Prefer key-based SSH and deny password auth on internet-facing hosts
- Collect logs centrally; restrict who can read authentication and audit trails

## Common Mistakes

!!! warning "Using legacy networking tools by default"
    `ifconfig`/`netstat` are missing or incomplete on modern images. **Fix:** use `ip` and `ss`.

!!! warning "Editing vendor unit files in place"
    Package upgrades overwrite `/lib/systemd/system`. **Fix:** `systemctl edit` drop-ins under `/etc`.

!!! warning "Trusting df without checking inodes and mounts"
    A full `/var` or exhausted inodes looks different from root. **Fix:** `df -h`, `df -i`, and `findmnt`.

## Best Practices

- Golden images + config as code over snowflake hosts
- Alert on symptoms (failed units, disk, load) with runbooks attached
- Time-sync (chrony) everywhere — logs and TLS depend on it
- Separate OS and data volumes on Cloud VMs
- Practise restore and rescue paths before you need them

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Permission denied | Mode/owner/ACL/MAC | `namei -l`, `id`, `getfacl`, SELinux/AppArmor logs |
| No route / timeout | Routing, DNS, firewall | `ip route`, `dig`, `ss`, security groups |
| Service won’t start | Unit/config/deps | `systemctl status`, `journalctl -u`, config `-t` |
| Disk full | Logs, containers, deleted-open | `df`/`du`, `lsof +L1`, rotate/expand |
| High load | CPU, I/O wait, thrash | `vmstat`, `iostat`, `ps` |

## Summary

**Process Management** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

## Interview Questions

1. How does this topic show up when operating Cloud VMs or Kubernetes nodes?
2. What would you check first if this area misbehaves in production?
3. Which modern Linux tools replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI or a cron/timer job?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, then gather host signals (`systemctl --failed`, `df`, `ip`/`ss`, `journalctl`) before making changes. Fix forward with evidence, not guesswork.

## Related Tutorials

- [Linux for Cloud & DevOps – Category Overview](index.md)
- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) *(previous)*
- [systemd Services and journalctl](systemd-services-and-journalctl.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
