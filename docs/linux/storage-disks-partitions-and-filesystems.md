---
title: "Storage — Disks, Partitions, and Filesystems"
description: "Discover disks with lsblk, partition with fdisk/parted, create filesystems with mkfs, and mount/umount safely."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - lsblk
  - fdisk
  - parted
  - mkfs
  - mount
prerequisites:
  - systemd Targets, Timers, and Boot
  - Terminal access with a regular user account (sudo where noted)
comments: false
---

# Storage — Disks, Partitions, and Filesystems

## Overview

Attaching an EBS/Azure disk is useless until you partition, format, mount, and persist it.

This is **Tutorial 12** in **Module 8: Storage Management** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for administrators, DevOps engineers, SREs, and platform engineers operating production Linux.

## Prerequisites

- systemd Targets, Timers, and Boot
- Terminal access with a regular user account (sudo where noted)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Storage — Disks, Partitions, and Filesystems” on a real Linux host
- [ ] Use modern tools (`ip`/`ss`, `systemctl`/`journalctl`) where they apply
- [ ] Complete the lab under `~/rebash-linux/` with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

Linux ops work sits between humans/automation and the kernel, services, and network. This topic’s control points are shown below.

![Architecture diagram for Storage — Disks, Partitions, and Filesystems](../assets/excalidraw/linux-storage-layout.svg)

## Theory

### What it is

**Storage** on Linux starts with block devices (virtual disks in the cloud, physical drives on bare metal). You **partition** them (usually GPT today), create a **filesystem** with `mkfs` (commonly ext4 or XFS), then **mount** the filesystem on a directory so it appears in the single directory tree. Discovery tools (`lsblk`, `blkid`) show names, sizes, types, Universally Unique Identifiers (UUIDs), and mount points before you touch anything destructive.

### Why it matters

Attaching a data volume to the wrong device node, formatting the OS disk, or omitting a persistent mount entry are career-limiting mistakes. Cloud VMs routinely add second disks for databases or logs; without correct partitioning, filesystem choice, and `fstab`/`nofail` policy, reboot behaviour becomes lottery. Capacity and performance incidents also start with knowing which mount backs `/var` or `/data`.

### How it works

`lsblk -f` maps NAME → FSTYPE → MOUNTPOINT. Partition with `fdisk` or `parted` (lab VMs only until you are sure of the device). Create a filesystem (`mkfs.ext4`, `mkfs.xfs`), record the UUID from `blkid`, mount at a directory you created, then persist with `/etc/fstab` or a systemd `.mount` unit. Prefer UUID= or LABEL= over `/dev/sdX` names that can reorder. For secondary cloud disks, `nofail` (and often `x-systemd.device-timeout`) lets the host boot if the volume is detached. Unmount with `umount` only when nothing holds open files on that path.

### Key concepts and comparisons

| Layer | Example |
|-------|---------|
| Disk | `/dev/nvme1n1`, `/dev/sdb` |
| Partition | `/dev/nvme1n1p1` |
| Filesystem | ext4, XFS |
| Mount point | `/mnt/data`, `/var/lib/postgresql` |

| Filesystem | Typical choice |
|------------|----------------|
| ext4 | Ubiquitous, simple volumes |
| XFS | Large volumes; common on RHEL-family data disks |

| Persistence | Notes |
|-------------|-------|
| `/etc/fstab` | Classic; use UUID |
| systemd `.mount` | Unit dependencies and journal |

### Common pitfalls

- Formatting the wrong disk because `lsblk` was not checked twice.
- Using `/dev/sdb1` in `fstab` after a reboot renamed devices.
- Forgetting `nofail` on optional data disks and hanging boot.
- Creating a filesystem on a whole disk that already had partitions you needed.
- Unmounting while applications still have files open (`umount` fails or force causes pain).

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab12 && cd ~/rebash-linux/lab12
```

**Focus:** map lsblk; practise mount options on a loop file; draft fstab line

### Step 1 – Loopback filesystem drill

```bash
lsblk -f | tee lsblk.txt
dd if=/dev/zero of=disk.img bs=1M count=64 status=none
mkfs.ext4 -F disk.img
mkdir -p mnt
sudo mount -o loop disk.img mnt
echo hello | sudo tee mnt/hello.txt
findmnt mnt | tee mount.txt
sudo umount mnt
blkid disk.img | tee blkid.txt || true
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab12/`
- [ ] You can explain each Theory bullet in your own words
- [ ] You used modern tooling where applicable (`ip`/`ss`, `systemctl`/`journalctl`)
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production Linux practice for **Storage — Disks, Partitions, and Filesystems** always combines:

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

**Storage — Disks, Partitions, and Filesystems** is essential for Cloud and DevOps engineers operating Linux hosts. Practise the lab until the inspection path is muscle memory, then continue the track.

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
- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md) *(previous)*
- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
- [systemd documentation](https://systemd.io/)
- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
