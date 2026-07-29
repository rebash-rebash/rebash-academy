---
title: "systemd Services and journalctl"
description: "Manage services with systemd and systemctl, and query logs with journalctl."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - systemd
  - systemctl
  - journalctl
prerequisites:
  - Process Management
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# systemd Services and journalctl

## Overview

Almost every Linux Cloud image uses systemd as PID 1. Service control and journal queries are daily ops.

This is **Tutorial 10** in **Module 7: Services & Boot** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Process Management
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “systemd Services and journalctl” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for systemd Services and journalctl](../assets/images/linux-systemd-architecture.svg)

## Theory

### systemd architecture

**systemd** is the init system and service manager: units (`.service`, `.socket`, `.timer`, `.mount`, …), dependencies, cgroups, and the journal.

### systemctl

```bash
systemctl status ssh
systemctl is-active nginx
systemctl start|stop|restart|reload UNIT
systemctl enable|--now UNIT
systemctl disable UNIT
systemctl list-units --type=service --state=failed
systemctl cat UNIT
systemctl edit UNIT   # drop-in overrides
```

Unit files live under `/lib/systemd/system` or `/etc/systemd/system`. Prefer drop-ins over editing vendor units.

### Services

A `.service` unit defines `ExecStart`, user, restart policy, dependencies (`After=`, `Requires=`), and hardening directives (`ProtectSystem=`, `NoNewPrivileges=`).

### journalctl

**journald** stores structured logs:

```bash
journalctl -u ssh -e
journalctl -u nginx --since '1 hour ago'
journalctl -p err..alert -b
journalctl -f
```

`-b` current boot; `_PID=` / `_UID=` match fields. Persist journal on disk for post-reboot forensics (`/var/log/journal`).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab10 && cd ~/rebash-linux/lab10
```

**Focus:** inspect units; read journal; create a simple user service

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab10 systemd-services-and-journalctl on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – systemd and journal

```bash
systemctl list-units --type=service --state=running | head | tee services.txt
systemctl status ssh 2>/dev/null || systemctl status sshd 2>/dev/null || true
journalctl -b -p err -n 20 --no-pager 2>/dev/null | tee journal-err.txt || true
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/rebash-lab.service << 'EOF'
[Unit]
Description=REBASH lab oneshot
[Service]
Type=oneshot
ExecStart=/bin/echo rebash-lab-ok
EOF
systemctl --user daemon-reload 2>/dev/null || true
systemctl --user start rebash-lab.service 2>/dev/null || true
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab10/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **systemd Services and journalctl** always combines:

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

**systemd Services and journalctl** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Process Management](process-management.md) *(previous)*
- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
