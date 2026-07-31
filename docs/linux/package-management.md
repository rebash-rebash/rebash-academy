---
title: "Package Management"
description: "Install and maintain software with apt, dnf, yum, zypper, and understand snap/flatpak on Linux hosts."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - apt
  - dnf
  - yum
  - zypper
  - snap
  - flatpak
prerequisites:
  - SSH and Remote Access
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Package Management

## Overview

Unpatched packages are vulnerability debt. Fluent package ops keep fleets consistent.

This is **Tutorial 16** in **Module 10: Package Management** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- SSH and Remote Access
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Package Management” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Package Management](../assets/excalidraw/linux-package-management.svg)

## Theory

### What it is

A **package manager** installs, updates, and removes software in a consistent way for your distribution: **apt**/**dpkg** on Debian and Ubuntu; **dnf**/**yum**/**rpm** on Red Hat Enterprise Linux (RHEL) family systems; **zypper** on SUSE. Optional desktop-oriented systems such as **snap** and **Flatpak** sandbox apps but are usually secondary on servers. Packages bring dependencies, version metadata, and file inventories the OS can query and verify.

### Why it matters

Unmanaged manual binaries drift; unpatched kernels and libraries are the main host vulnerability class. Golden images, CI runners, and configuration management all assume a known package state. Knowing how to install a tool, pin or hold a version, and reboot after kernel updates keeps fleets reproducible and secure.

### How it works

Refresh metadata (`apt update`, `dnf check-update`, `zypper refresh`), then install (`apt install`, `dnf install`). Query with `apt policy`, `rpm -q`, or `dpkg -l`. Upgrades apply security and bugfix releases; kernel updates typically need a reboot to take effect. Prefer distribution packages for system daemons; use containers or language-specific tools for app runtime isolation. Automate patching carefully (`unattended-upgrades`, `dnf-automatic`) with maintenance windows. Remove unused packages to shrink attack surface. Record critical versions in image build pipelines rather than hand-maintained snowflakes.

### Key concepts and comparisons

| Family | Tools | Query |
|--------|-------|-------|
| Debian/Ubuntu | apt, dpkg | `apt policy`, `dpkg -l` |
| RHEL/Fedora/Rocky/Alma | dnf/yum, rpm | `rpm -q`, `dnf list` |
| SUSE | zypper, rpm | `zypper info` |

| Approach | Server fit |
|----------|------------|
| Distro packages | Best for OS daemons and libs |
| Containers | App shipping and isolation |
| snap/Flatpak | Mostly desktop; use sparingly on servers |

### Common pitfalls

- Running `upgrade` on production without a change window or rollback image.
- Mixing random third-party apt repos without pinning or trust evaluation.
- Installing compilers and debug tools on locked-down production hosts against policy.
- Forgetting that a new kernel is inactive until reboot.
- Assuming package names match across Debian and RHEL families.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab16 && cd ~/rebash-linux/lab16
```

**Focus:** detect package manager; install a CLI tool; query package metadata

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab16 package-management on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Package manager detect

```bash
{
  command -v apt && echo PM=apt
  command -v dnf && echo PM=dnf
  command -v yum && echo PM=yum
  command -v zypper && echo PM=zypper
  command -v snap && snap version | head -n 1
  command -v flatpak && flatpak --version
} | tee pkg-tools.txt
# Non-mutating query examples:
(apt-cache policy bash 2>/dev/null || dnf info bash 2>/dev/null || true) | head | tee pkg-info.txt
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab16/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Package Management** always combines:

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

**Package Management** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [SSH and Remote Access](ssh-and-remote-access.md) *(previous)*
- [Scheduling with cron, at, and Timers](scheduling-cron-at-and-timers.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
