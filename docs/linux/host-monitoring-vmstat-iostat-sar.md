---
title: "Host Monitoring with vmstat, iostat, and sar"
description: "Read host health with vmstat, iostat, free, uptime, df, du, and sar."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - vmstat
  - iostat
  - sar
  - capacity
prerequisites:
  - Logging — syslog, journald, and logrotate
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Host Monitoring with vmstat, iostat, and sar

## Overview

Before installing a heavyweight agent, know what the classic tools already tell you.

This is **Tutorial 19** in **Module 12: Logging & Monitoring** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Logging — syslog, journald, and logrotate
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Host Monitoring with vmstat, iostat, and sar” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Host Monitoring with vmstat, iostat, and sar](../assets/excalidraw/linux-host-monitoring.svg)

## Theory

### What it is

**Host monitoring** with classic tools gives immediate and historical views of resource health. Instant signals include `uptime` (load averages), `free` (memory and swap), and `df`/`du` (disk). **vmstat** samples processes, memory, swap, and CPU; **iostat** exposes per-device I/O utilisation and latency; **sar** (System Activity Reporter from the sysstat package) records historical samples you can replay after an incident.

### Why it matters

Dashboards lag; SSH-plus-sysstat still saves outages. Distinguishing CPU saturation from I/O wait from memory thrashing changes the fix from “add CPUs” to “fix disk” or “stop the leak.” Historical `sar` data answers “was it already bad before the deploy?” without guessing. These skills transfer to interpreting cloud metrics that use the same underlying ideas (utilisation, saturation, errors).

### How it works

`vmstat 1 5` prints five one-second samples — watch run queue `r`, swap in/out `si`/`so`, and I/O wait `wa`. `iostat -xz 1 5` highlights util%, await, and queue depth; install sysstat if missing. `sar -u/-r/-d` reports CPU, memory, and disk; enable the sysstat timer or cron so history exists before the next incident. Correlate with `ps` for offenders and with application metrics for user impact. The USE method — utilisation, saturation, errors — keeps interpretation disciplined.

### Key concepts and comparisons

| Tool | Primary view |
|------|----------------|
| `uptime` / `free` / `df` | Instant capacity signals |
| `vmstat` | CPU, run queue, swap, I/O wait |
| `iostat` | Disk util, await, saturation |
| `sar` | Historical samples across resources |
| `top`/`ps` | Which PIDs consume CPU/RAM |

| Symptom | First counters |
|---------|----------------|
| Slow app, low CPU | `wa`, iostat await |
| High load | `r` vs CPU count; steal time on VMs |
| Latency spikes | swap `si`/`so`, thrashing |

### Common pitfalls

- Treating load average alone as proof of CPU shortage.
- Ignoring steal time (`st`) on noisy cloud hypervisors.
- Looking at a single iostat snapshot during a brief burst.
- Never enabling sysstat collection — no history when you need it.
- Tuning sysctl based on one sample without a hypothesis or rollback.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab19 && cd ~/rebash-linux/lab19
```

**Focus:** capture uptime/free/df; run vmstat/iostat/sar samples; summarise

### Step 1 – Host sample

```bash
{
  uptime
  free -h
  df -h
  du -sh . 2>/dev/null
  vmstat 1 3
  command -v iostat && iostat -xz 1 2
  command -v sar && sar -u 1 2
} | tee host-sample.txt
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab19/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Host Monitoring with vmstat, iostat, and sar** always combines:

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

**Host Monitoring with vmstat, iostat, and sar** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Logging — syslog, journald, and logrotate](logging-syslog-journald-logrotate.md) *(previous)*
- [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
