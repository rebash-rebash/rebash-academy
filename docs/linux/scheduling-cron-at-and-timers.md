---
title: "Scheduling with cron, at, and Timers"
description: "Schedule recurring and one-shot jobs with cron, crontab, at, and systemd timers."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - cron
  - crontab
  - at
  - timers
prerequisites:
  - Package Management
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Scheduling with cron, at, and Timers

## Overview

Backups, reports, and cleanup need reliable schedules with visible logs.

This is **Tutorial 17** in **Module 11: Scheduling & Automation** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Package Management
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Scheduling with cron, at, and Timers” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Scheduling with cron, at, and Timers](../assets/images/linux-scheduling.svg)

## Theory

### cron and crontab

```bash
crontab -l
crontab -e
```

Format: `minute hour dom month dow command`

```cron
*/15 * * * * /usr/local/bin/healthcheck.sh >>/var/log/healthcheck.log 2>&1
```

System crontabs: `/etc/crontab`, `/etc/cron.d/`. Set `PATH` or use absolute paths — cron’s environment is minimal.

### at

One-shot jobs:

```bash
echo 'echo hello' | at now + 2 minutes
atq
atrm JOB
```

### systemd timers

Prefer for services you already manage with systemd:

```bash
systemctl list-timers
# pair foo.service + foo.timer; systemctl enable --now foo.timer
```

Timers integrate with `journalctl -u foo.service` and dependency ordering — better observability than silent cron mail.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab17 && cd ~/rebash-linux/lab17
```

**Focus:** add a user crontab entry; queue an at job; inspect systemd timers

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab17 scheduling-cron-at-and-timers on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Schedule safely

```bash
crontab -l 2>/dev/null | tee crontab-before.txt || true
echo "# lab only — remove after class" > cron.line
echo "*/30 * * * * date >> $HOME/rebash-linux/lab17/cron-tick.log" >> cron.line
cat cron.line
systemctl list-timers --all 2>/dev/null | head | tee timers.txt || true
command -v at && echo 'echo lab-at | at now + 1 minute' || echo 'at not installed'
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab17/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Scheduling with cron, at, and Timers** always combines:

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

**Scheduling with cron, at, and Timers** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Package Management](package-management.md) *(previous)*
- [Logging — syslog, journald, and logrotate](logging-syslog-journald-logrotate.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
