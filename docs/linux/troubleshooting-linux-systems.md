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

![Architecture diagram for Troubleshooting Linux Systems](../assets/excalidraw/linux-troubleshooting.svg)

## Theory

### What it is

**Troubleshooting** is a disciplined loop: define blast radius and recent changes, gather host signals, narrow the domain, confirm with logs, change one variable, and record evidence. Domains include boot, CPU, memory, disk, permissions, network, and services. The goal is not clever guesses — it is reproducible diagnosis that works at 03:00 under pressure.

### Why it matters

Cloud and Kubernetes incidents still terminate on Linux nodes. Without a method, teams thrash: restarting healthy services, widening permissions, or rebooting away evidence. A shared checklist (`systemctl --failed`, `df`, `ip`/`ss`, `journalctl`) aligns on-call engineers and shortens Mean Time To Recovery (MTTR). Post-incident learning depends on the notes you took while debugging.

### How it works

Start with urgency signals: load, memory, disk, failed units. Classify: boot (GRUB, fstab, emergency target), CPU (`top`/`ps`, then careful `strace`/`perf`), memory (`free`, OOM in `dmesg`/`journalctl -k`), disk (`df`/`df -i`/`du`, deleted-open files), permissions (`namei -l`, ACLs, MAC), network (`ip route`, `ss`, DNS, firewalls, `curl -v`), services (`systemctl status`, `journalctl -u`, config `-t`). Time-box log analysis to since deploy or since alert. Apply the USE method for performance: utilisation, saturation, errors. Fix forward with evidence; prefer reversible changes.

### Key concepts and comparisons

| Domain | First tools |
|--------|-------------|
| Boot | `journalctl -b -p err`, failed units, fstab |
| CPU | `top`, `ps`, load vs run queue |
| Memory | `free`, OOM logs, top consumers |
| Disk | `df -h`, `df -i`, `du`, `lsof +L1` |
| Perms | `namei -l`, `id`, `getfacl`, MAC logs |
| Network | `ip`, `ss`, `dig`, SG/firewall |
| Service | `systemctl`, `journalctl -u`, config test |

| Anti-pattern | Better |
|--------------|--------|
| Change five things at once | One change + evidence |
| Reboot immediately | Capture journal/metrics first |
| Disable SELinux to pass | Read denials; fix labels |

### Common pitfalls

- Skipping blast radius — rebooting a shared node for a single pod symptom.
- Trusting only application logs while systemd shows the unit never started.
- Clearing disk by deleting files still held open — space does not return.
- Chasing DNS when the security group is the deny.
- Leaving the host worse (debug packages, permissive MAC) after the incident.

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
