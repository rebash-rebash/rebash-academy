---
title: "Lab — Configure Linux Storage"
description: "Partition a lab disk (or loop device), create a filesystem, mount with UUID fstab entries, and practise safe growth checks with lsblk and df."
difficulty: intermediate
estimated_time: "50–70 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - storage
  - lvm
  - fstab
comments: false
---

# Lab — Configure Linux Storage

## Lab Overview

**Purpose:** Practise disk discovery, filesystem creation, persistent mounts, and monitoring without guessing device names.

**Scenario:** An app needs a dedicated data volume mounted at `/srv/rebash-data`, surviving reboot via UUID in `/etc/fstab`.

**Expected outcome:** Data volume mounts on boot, writes succeed, and you can show `lsblk`, `df`, and `findmnt` evidence.

!!! warning "Destructive commands"
    Prefer a **loopback file** or an extra empty virtual disk. Never `mkfs` a disk that holds your root filesystem.

## Business Scenario

Capacity planning added a second volume for application state. You must format, mount, and persist it the same way production automation would.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Inventory block devices with `lsblk` and `blkid`
- [ ] Create a filesystem and mount by UUID
- [ ] Add a correct `/etc/fstab` entry and validate with `findmnt --verify`
- [ ] Measure usage with `df` / `du` and spot fill risk
- [ ] (Optional) Create a simple Logical Volume Manager (LVM) layout

## Prerequisites

### Knowledge

- [Storage: Disks, Partitions, and Filesystems](../linux/storage-disks-partitions-and-filesystems.md)
- [LVM, Swap, and Disk Monitoring](../linux/lvm-swap-and-disk-monitoring.md)
- [Filesystem Paths, Links, Mounts, and inodes](../linux/filesystem-paths-links-mounts-and-inodes.md)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu with sudo | VM recommended |
| Extra disk **or** loop file | Lab uses loop file by default |
| `xfsprogs` or e2fsprogs | for `mkfs` |

**Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-linux-storage
cd ~/rebash-lab-linux-storage
```

## Initial State

Root disk only (typical). You will create a 1 GiB sparse file and attach it as a loop device.

## Lab Tasks

### Task 1 — Inventory

```bash
lsblk -f
df -hT
sudo findmnt --verify 2>&1 | head
```

Save a snapshot:

```bash
lsblk -f | tee ~/rebash-lab-linux-storage/lsblk-before.txt
```

### Task 2 — Create a loop-backed “disk”

```bash
truncate -s 1G ~/rebash-lab-linux-storage/data.img
LOOP=$(sudo losetup --find --show ~/rebash-lab-linux-storage/data.img)
echo "LOOP=$LOOP" | tee ~/rebash-lab-linux-storage/loop.env
sudo parted -s "$LOOP" mklabel gpt mkpart primary ext4 1MiB 100%
PART="${LOOP}p1"
# Some systems use ${LOOP}p1; if missing, try ${LOOP}1 after partprobe
sudo partprobe "$LOOP" || true
lsblk "$LOOP"
```

If the partition node differs, set `PART` from `lsblk` output and update `loop.env`.

### Task 3 — Filesystem and mount

```bash
source ~/rebash-lab-linux-storage/loop.env
# Adjust PART if needed
sudo mkfs.ext4 -L rebash-data "$PART"
UUID=$(sudo blkid -s UUID -o value "$PART")
echo "UUID=$UUID" | tee -a ~/rebash-lab-linux-storage/loop.env
sudo mkdir -p /srv/rebash-data
sudo mount UUID="$UUID" /srv/rebash-data
echo "lab-storage-ok" | sudo tee /srv/rebash-data/README.txt
df -hT /srv/rebash-data
findmnt /srv/rebash-data
```

### Task 4 — Persist with fstab (careful)

```bash
source ~/rebash-lab-linux-storage/loop.env
sudo cp -a /etc/fstab /etc/fstab.pre-lab
echo "UUID=$UUID  /srv/rebash-data  ext4  defaults,nofail,x-systemd.device-timeout=5  0  2" \
  | sudo tee -a /etc/fstab
sudo findmnt --verify
sudo umount /srv/rebash-data
sudo mount -a
test -f /srv/rebash-data/README.txt && echo "remount ok"
```

`nofail` keeps the host bootable if the loop setup is missing after reboot (loop devices need re-attach — document that limitation).

### Task 5 — Usage and inode awareness

```bash
dd if=/dev/zero of=/srv/rebash-data/fill.bin bs=1M count=100 status=none
df -h /srv/rebash-data
df -i /srv/rebash-data
du -sh /srv/rebash-data/*
rm -f /srv/rebash-data/fill.bin
```

### Task 6 — Optional LVM stretch

If comfortable, create a second 512 MiB image, `pvcreate`/`vgcreate`/`lvcreate`, `mkfs`, and mount at `/srv/rebash-lvm`. Record commands in `~/rebash-lab-linux-storage/lvm-notes.txt`.

## Validation

- [ ] `findmnt /srv/rebash-data` shows the UUID-backed mount
- [ ] `README.txt` survives `umount` + `mount -a` in the same session
- [ ] `lsblk-before.txt` and `loop.env` saved
- [ ] You did **not** format the root disk

## Troubleshooting

| Symptom | Resolution |
|---------|------------|
| No `p1` partition node | `partprobe`; check `ls /dev/loop*` |
| `mount -a` fails | Restore `/etc/fstab.pre-lab`; fix UUID |
| Boot delay | `nofail` + short device timeout; avoid broken fstab |

## Challenge Extensions

- Switch to XFS and practise `xfs_growfs` after expanding the image
- Add a swap file and confirm with `swapon --show`
- Simulate disk-full and recover space safely

## Cleanup

```bash
sudo umount /srv/rebash-data 2>/dev/null || true
sudo sed -i '\#/srv/rebash-data#d' /etc/fstab
# Or restore: sudo cp -a /etc/fstab.pre-lab /etc/fstab
source ~/rebash-lab-linux-storage/loop.env 2>/dev/null || true
sudo losetup -d "$LOOP" 2>/dev/null || true
rm -rf ~/rebash-lab-linux-storage
sudo rmdir /srv/rebash-data 2>/dev/null || true
```

## Production Discussion

Cloud disks use volume IDs and udev; still mount by UUID/LABEL, never by volatile `/dev/sdX` names. Automate fstab or systemd mount units via IaC.

## Best Practices

- Always `lsblk` before `mkfs`
- Mount by UUID/LABEL
- Keep a fstab backup; use `nofail` for non-root data where appropriate

## Common Mistakes

| Mistake | Correct approach |
|---------|------------------|
| `mkfs /dev/sda` by habit | Identify empty device first |
| Device path in fstab | UUID |
| No dry-run verify | `findmnt --verify` |

## Success Criteria

You can explain the full path from block device → filesystem → UUID → fstab → `findmnt` proof.

## Reflection Questions

1. Why are `/dev/sdX` names unsafe in fstab?
2. When would you choose LVM over a single partition?
3. How do you detect inode exhaustion vs block exhaustion?

## Interview Connection

Expect: grow a disk, fix a bad fstab, explain UUID mounts, describe LVM resize order.

## Related Tutorials

- [Storage: Disks, Partitions, and Filesystems](../linux/storage-disks-partitions-and-filesystems.md)
- [LVM, Swap, and Disk Monitoring](../linux/lvm-swap-and-disk-monitoring.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)

## References

- `man losetup`, `man fstab`, `man findmnt`
- [util-linux documentation](https://github.com/util-linux/util-linux)
