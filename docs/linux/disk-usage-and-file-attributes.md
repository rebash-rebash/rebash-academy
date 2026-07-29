---
title: "Disk Usage and File Attributes"
description: "Measure disk usage with df and du, and inspect file attributes and timestamps with ls and stat."
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - df
  - du
  - attributes
  - stat
prerequisites:
  - Filesystem Paths, Links, Mounts, and Inodes
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Disk Usage and File Attributes

## Overview

Capacity incidents dominate on-call. Learn to read df/du correctly and interpret file attributes under pressure.

This is **Tutorial 5** in **Module 3: Linux Filesystem** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- Filesystem Paths, Links, Mounts, and Inodes
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Disk Usage and File Attributes” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Disk Usage and File Attributes](../assets/images/linux-disk-usage-attrs.svg)

## Theory

### File attributes

`ls -l` shows mode, link count, owner, group, size, mtime, name. `stat` exposes atime/mtime/ctime, inode, and device.

Extended attributes (xattrs) and flags (`chattr`/`lsattr` on ext4) appear in hardening and immutable-file scenarios:

```bash
lsattr file.txt 2>/dev/null || true
getfattr -d file.txt 2>/dev/null || true
```

### Disk usage — `df`

`df` reports **filesystem** free space (what the mount can still accept):

```bash
df -h
df -hT
df -i
```

Watch mount points, not just `/` — `/var` or `/var/lib/docker` often fill first on container hosts.

### Disk usage — `du`

`du` reports **directory tree** consumption:

```bash
du -sh ~/rebash-linux
du -h --max-depth=1 /var 2>/dev/null | sort -h
```

`df` vs `du` mismatches usually mean deleted-but-open files (restart the holding process) or bind mounts.

### `stat` for attributes

```bash
stat file.txt
stat -c '%a %U:%G %s %n' file.txt
```

Use size, ownership, and mode together when diagnosing permission-denied versus missing-file errors.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab05 && cd ~/rebash-linux/lab05
```

**Focus:** compare df vs du; find largest dirs; capture stat attributes

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab05 disk-usage-and-file-attributes on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Usage and attributes

```bash
dd if=/dev/zero of=blob.bin bs=1M count=5 status=none
df -h . | tee df.txt
du -sh . blob.bin | tee du.txt
stat blob.bin | tee stat.txt
ls -l blob.bin
```

### Final step – Cleanup note

```bash
./lab.sh
# keep ~/rebash-linux for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab05/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Disk Usage and File Attributes** always combines:

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

**Disk Usage and File Attributes** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) *(previous)*
- [Users, Groups, and sudo](users-groups-and-sudo.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
