---
title: "Troubleshooting Linux Systems"
description: "Systematically debug boot failures, high CPU/memory, disk full, permissions, network, service failures, logs, and bottlenecks."
difficulty: advanced
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - troubleshooting
  - incidents
  - performance
prerequisites:
  - Containers — Namespaces, cgroups, OverlayFS, and OCI
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Troubleshooting Linux Systems

## Overview

Incidents reward a checklist over panic. Build a repeatable troubleshooting path.

This is **Tutorial 23** in **Module 15: Troubleshooting** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Containers — Namespaces, cgroups, OverlayFS, and OCI
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Troubleshooting Linux Systems” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Troubleshooting Linux Systems](../assets/images/linux-troubleshooting.svg)

## Theory

### Method

1. Define blast radius and recent changes
2. Check urgency signals: `uptime`, `free`, `df`, `systemctl --failed`
3. Narrow domain: boot / CPU / memory / disk / perms / net / service
4. Confirm with logs (`journalctl`, app logs)
5. Change one variable; write down what you tried

### Boot failures

GRUB → rescue → `journalctl -b -p err`, `systemctl list-units --failed`, filesystem checks, fstab `nofail`, cloud-init status.

### High CPU

`top`/`ps` → identify PID → `perf`/`strace` sparingly → restart or scale → fix root cause (loop, noisy neighbour).

### High memory

`free -h`, `ps --sort=-%mem`, OOM killer (`dmesg`/`journalctl -k`), leak vs undersized VM.

### Disk full

`df -h` + `df -i` → `du` → deleted-open files (`lsof +L1`) → logrotate → expand volume/LVM.

### Permission issues

`namei -l path`, `id`, ACLs (`getfacl`), MAC denials (`ausearch`/`journalctl` for SELinux).

### Network problems

`ip route`, `ss`, DNS (`dig`), security groups/firewalls, `curl -v`, `tcpdump`.

### Service failures

`systemctl status -l`, `journalctl -u`, config test (`nginx -t`, `sshd -t`), dependency targets.

### Log analysis

Time-box: since deploy / since alert. Correlate host journal + app + load balancer.

### Performance bottlenecks

USE method (utilisation, saturation, errors) with `vmstat`, `iostat`, `sar`, application metrics.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab23 && cd ~/rebash-linux/lab23
```

**Focus:** build a troubleshooting toolkit script; run failed-unit and df/cpu checks

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab23 troubleshooting-linux-systems on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Troubleshooting toolkit

```bash
cat > toolkit.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "== failed units =="; systemctl --failed --no-pager || true
echo "== load/mem/disk =="; uptime; free -h; df -h
echo "== top cpu =="; ps aux --sort=-%cpu | head -n 6
echo "== journal err =="; journalctl -b -p err -n 15 --no-pager 2>/dev/null || true
echo "== listeners =="; ss -tulpn | head
EOF
chmod +x toolkit.sh
./toolkit.sh | tee toolkit-out.txt
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab23/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Troubleshooting Linux Systems** always combines:

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

**Troubleshooting Linux Systems** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Containers — Namespaces, cgroups, OverlayFS, and OCI](containers-namespaces-cgroups-and-oci.md) *(previous)*
- [Production Linux — Hardening and Performance](production-linux-hardening-and-performance.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
