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

![Architecture diagram for Disk Usage and File Attributes](../assets/excalidraw/linux-filesystem-hierarchy.svg)

## Theory

### What it is

**File attributes** are the metadata you see with `ls -l` and `stat`: mode, owner, group, size, timestamps, inode, and device. Extended attributes (xattrs) and filesystem flags (`chattr`/`lsattr` on ext4) add further behaviour such as immutability. **Disk usage** splits into two views: `df` reports free space and inodes **per mounted filesystem**; `du` reports how much space a **directory tree** consumes. Together they answer “who filled the disk?” and “why can’t I write?”

### Why it matters

Disk-full incidents are among the most common production pages. Container hosts fill `/var/lib/docker` or `/var/lib/containerd`; log directories grow without rotation; deleted files stay allocated while a process holds them open — `df` and `du` disagree until that process exits. Attribute checks separate “permission denied” from “wrong owner” and support hardening (immutable configs). Site Reliability Engineering (SRE) runbooks almost always start with `df -h`, `df -i`, then `du`.

### How it works

`df -hT` lists mounts, types, and human-readable capacity; `df -i` shows inode capacity. Always note the mount point, not only `/`. `du -sh path` summarises a tree; `du -h --max-depth=1` finds hot children. When `df` shows full but `du` on `/` seems smaller, look for other mounts and for deleted-but-open files (`lsof +L1` or equivalent). `stat` prints atime/mtime/ctime and mode; formatting with `stat -c` helps scripts. On ext4, `chattr +i` can make a file immutable until cleared — useful for critical configs, dangerous if forgotten.

### Key concepts and comparisons

| Tool | Answers |
|------|---------|
| `df` | How much can this **mount** still accept? |
| `du` | How much does this **tree** use? |
| `stat` / `ls -l` | Who owns it, what mode, what size/times? |
| `lsattr` / `getfattr` | Special flags / extended attributes |

| Symptom | Likely cause |
|---------|--------------|
| `df` full, `du` smaller | Deleted-open files or another mount |
| `df -h` free, create fails | Inode exhaustion (`df -i`) |
| Permission denied | Mode/owner/ACL/MAC — not “disk full” |

### Common pitfalls

- Checking only `/` while `/var` or a data volume is the one that filled.
- Ignoring inodes — millions of small files exhaust them first.
- Restarting nothing when `du` and `df` disagree; the holder process must release the file.
- Leaving `chattr +i` on files and wondering why deploys cannot overwrite them.
- Sorting `du` output incorrectly — use `sort -h` with human-readable sizes.

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
