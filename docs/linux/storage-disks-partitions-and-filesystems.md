---
title: "Disks, Partitions, and Filesystems"
description: "Discover disks with lsblk, create a safe loop-backed partition and filesystem, mount by UUID, and clean up on Ubuntu."
difficulty: intermediate
estimated_time: "55–65 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 8 · Storage"
tags:
  - linux
  - lsblk
  - fdisk
  - parted
  - mkfs
  - mount
prerequisites:
  - linux/systemd-targets-timers-and-boot
next:
  - linux/lvm-swap-and-disk-monitoring
related:
  - linux/disk-usage-and-file-attributes
interview: interview/linux
comments: false
---

# Disks, Partitions, and Filesystems

## Overview

Attaching a cloud disk is useless until you **discover** it, **partition** it, create a **filesystem**, **mount** it, and make the mount survive reboot safely. On Linux, block devices appear under `/dev`. You usually create a GPT partition, format it (often **ext4** or **XFS**), mount it on a directory, and persist it with **UUID** in `/etc/fstab` (or a systemd `.mount` unit).

Wrong device names wipe the wrong disk. Device letters such as `/dev/sdb` can change after reboot; **UUIDs** do not. Secondary cloud volumes should often use `nofail` so the host still boots if the volume is detached. In this tutorial you will practise the full flow on a **file-backed loop device** so you never touch the real OS disk, and save proof under `~/rebash-linux/lab12`.

In production, databases and logs belong on dedicated mounts. Capacity and performance incidents start with knowing which device backs `/var` or `/data`. Always run `lsblk -f` twice before `mkfs`.

This is **Tutorial 12** in **Module 8: Storage** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Packages: `util-linux`, `e2fsprogs` (normally present); `parted` optional
- Do **not** run `mkfs` on real cloud disks until you can identify them with certainty

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Map disks, partitions, filesystem types, and mount points with `lsblk -f` and `blkid`
- [ ] Create a GPT partition on a loop-backed disk image safely
- [ ] Create an ext4 filesystem and mount it by UUID
- [ ] Explain why UUID/`nofail` matter for cloud secondary disks
- [ ] Clean up loop devices and keep evidence under `~/rebash-linux/lab12`

## Architecture

Storage layers stack from disk → partition → filesystem → mount point in the single directory tree.

![Architecture diagram for Disks, Partitions, and Filesystems](../assets/excalidraw/linux-storage-layout.svg)

## Theory

### What it is

A **block device** is a disk (virtual or physical). A **partition** carves that disk. A **filesystem** organises files inside a partition. A **mount point** is the directory where that filesystem appears.

```bash
lsblk -f
sudo blkid
findmnt
```

### Why it matters

Formatting the OS disk, omitting persistent mounts, or using unstable `/dev/sdX` names in `fstab` causes outages and data loss. Cloud VMs routinely add second disks for data; without correct layout and `fstab` policy, reboot behaviour becomes a lottery.

### How it works

1. **Discover** — `lsblk -f`, `blkid`, `findmnt`
2. **Partition** — `parted` or `fdisk` (lab: loop image only)
3. **Format** — `mkfs.ext4` / `mkfs.xfs`
4. **Mount** — `mount UUID=… /mnt/data`
5. **Persist** — `/etc/fstab` with `UUID=` (and often `nofail` for optional disks)

| Layer | Example |
|-------|---------|
| Disk | `/dev/nvme1n1`, `/dev/sdb`, loop device |
| Partition | `/dev/nvme1n1p1` |
| Filesystem | ext4, XFS |
| Mount point | `/mnt/data`, `/var/lib/postgresql` |

| Persistence | Notes |
|-------------|-------|
| `/etc/fstab` | Classic; prefer `UUID=` |
| systemd `.mount` | Unit dependencies and journal |

### Common pitfalls

- Formatting the wrong disk because `lsblk` was not checked twice.
- Using `/dev/sdb1` in `fstab` after devices reorder.
- Forgetting `nofail` on optional data disks and hanging boot.
- Unmounting while applications still hold open files.

## Hands-on Lab

### Objective

Create a 512 MiB disk image, attach it as a loop device, partition and format ext4, mount by UUID under `/mnt/rebash-lab12`, write a test file, then cleanly detach — with evidence under `~/rebash-linux/lab12`.

### Prerequisites

- Ubuntu with `sudo`, `losetup`, `parted` or `sfdisk`, `mkfs.ext4`
- ~1 GiB free under `$HOME`

### Lab environment

Workspace: `~/rebash-linux/lab12`

```bash
mkdir -p ~/rebash-linux/lab12 && cd ~/rebash-linux/lab12
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y parted e2fsprogs
lsblk -f | tee lsblk-before.txt
df -h . | tee df-home.txt
```

**Expected output:** `lsblk-before.txt` exists; enough free space on the home filesystem.

### Real-world scenario

A new empty data volume will be attached to an app VM later. Before you touch a real cloud disk, you rehearse partition → mkfs → UUID mount on a loop-backed image, and keep command output for the change ticket.

### Step-by-step tasks

#### Task 1 – Create disk image and attach loop device

```bash
cd ~/rebash-linux/lab12
set -euo pipefail

dd if=/dev/zero of=labdisk.img bs=1M count=512 status=progress
sudo losetup -fP --show labdisk.img | tee loop-device.txt
LOOP="$(cat loop-device.txt)"
test -b "$LOOP"
lsblk -f "$LOOP" | tee lsblk-loop.txt
echo "Using loop device: $LOOP"
```

**Expected output:** `loop-device.txt` contains a path such as `/dev/loop0`; `lsblk` shows the loop disk.

#### Task 2 – Partition, format, and capture UUID

```bash
cd ~/rebash-linux/lab12
set -euo pipefail
LOOP="$(cat loop-device.txt)"

sudo parted -s "$LOOP" mklabel gpt
sudo parted -s "$LOOP" mkpart primary ext4 1MiB 100%
sudo partprobe "$LOOP" || true
sleep 1

PART="${LOOP}p1"
if [[ ! -b "$PART" ]]; then
  PART="$(lsblk -lnpo NAME,TYPE "$LOOP" | awk '$2=="part"{print $1; exit}')"
fi
test -b "$PART"
echo "$PART" | tee partition.txt

sudo mkfs.ext4 -F -L rebashlab12 "$PART"
sudo blkid "$PART" | tee blkid.txt
UUID="$(blkid -s UUID -o value "$PART")"
test -n "$UUID"
echo "$UUID" | tee uuid.txt
```

**Expected output:** `uuid.txt` holds a UUID; `blkid.txt` shows `TYPE="ext4"` and label `rebashlab12`.

#### Task 3 – Mount by UUID, prove write, evidence pack

```bash
cd ~/rebash-linux/lab12
set -euo pipefail
UUID="$(cat uuid.txt)"

sudo mkdir -p /mnt/rebash-lab12
sudo mount -U "$UUID" /mnt/rebash-lab12
findmnt /mnt/rebash-lab12 | tee findmnt-lab.txt
echo "hello-storage" | sudo tee /mnt/rebash-lab12/proof.txt >/dev/null
sudo cat /mnt/rebash-lab12/proof.txt | tee mount-proof.txt
grep -F 'hello-storage' mount-proof.txt

printf 'UUID=%s /mnt/rebash-lab12 ext4 defaults,nofail 0 2\n' "$UUID" | tee fstab-example.txt

tar -czf storage-evidence.tgz \
  lsblk-before.txt df-home.txt loop-device.txt lsblk-loop.txt \
  partition.txt blkid.txt uuid.txt findmnt-lab.txt mount-proof.txt fstab-example.txt
ls -l storage-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** `findmnt-lab.txt` shows `/mnt/rebash-lab12`; `mount-proof.txt` contains `hello-storage`; evidence archive exists.

### Validation steps

- [ ] Loop device was created from `labdisk.img`
- [ ] Partition has ext4 and a UUID in `uuid.txt`
- [ ] `/mnt/rebash-lab12/proof.txt` was readable while mounted
- [ ] `storage-evidence.tgz` exists under `~/rebash-linux/lab12`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `PART` device missing | Partition not rescanned | `sudo partprobe`; check `lsblk`; use `${LOOP}p1` |
| `mount: special device does not exist` | Wrong UUID / not formatted | Re-run `blkid`; confirm `mkfs` succeeded |
| `losetup: cannot find unused loop` | Many loops in use | `losetup -a`; detach unused with `losetup -d` |
| Accidentally targeting `/dev/sda` | Skipped loop workflow | **Stop** — this lab only uses the loop from `loop-device.txt` |

### Challenge exercise

Unmount `/mnt/rebash-lab12`, remount using the **LABEL** (`rebashlab12`) instead of UUID, write `label-remount.txt` with `findmnt` output, then unmount again. Keep the loop attached until Cleanup.

### Learning outcomes

- Built a safe loop-backed disk workflow
- Partitioned and formatted without touching the OS disk
- Mounted by UUID and drafted an `fstab` line with `nofail`
- Saved storage evidence for a ticket

### Cleanup

```bash
cd ~/rebash-linux/lab12
set -euo pipefail

sudo umount /mnt/rebash-lab12 2>/dev/null || true
LOOP="$(cat loop-device.txt 2>/dev/null || true)"
if [[ -n "${LOOP:-}" ]]; then
  sudo losetup -d "$LOOP" || true
fi
sudo rmdir /mnt/rebash-lab12 2>/dev/null || true
rm -f labdisk.img
# Keep storage-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab12/` with evidence files
- [ ] You can explain disk → partition → filesystem → mount
- [ ] You prefer UUID over `/dev/sdX` in `fstab`
- [ ] You know why `nofail` helps optional cloud volumes

## Code Walkthrough

Production attach workflow:

1. **Snapshot / backup** if the disk is not empty
2. **`lsblk -f` twice** — confirm the new empty device
3. **Partition + mkfs** only on the intended device
4. **Mount by UUID**, write a canary file
5. **Persist** with `fstab` or systemd mount; test reboot on a practice VM

## Security Considerations

- Restrict who can run `mkfs`, `fdisk`, and raw disk access
- Encrypt sensitive data volumes (LUKS) when policy requires it
- Use `nosuid`/`nodev` mount options on untrusted data mounts when appropriate
- Do not leave world-writable mount points
- Protect `fstab` changes with change control — a bad line can block boot

## Common Mistakes

!!! warning "Formatting `/dev/sda` because it was “the second disk yesterday”"
    Names reorder. **Fix:** identify by size, serial, and emptiness with `lsblk -f`/`blkid` every time.

!!! warning "Persisting `/dev/nvme0n1p1` in fstab"
    After hardware changes the path may differ. **Fix:** use `UUID=` or `LABEL=`.

!!! warning "Omitting `nofail` on an optional data disk"
    Boot can hang waiting for a detached volume. **Fix:** add `nofail` (and review systemd mount timeouts).

!!! warning "Forcing `umount` while databases are running"
    Risk of corruption. **Fix:** stop services, then unmount; investigate open files with `lsof`/`fuser`.

## Best Practices

- Separate OS and data disks on cloud VMs
- Document mount points in configuration management
- Prefer GPT + UUID mounts
- Test restore and remount on a twin practice VM
- Monitor free space per mount, not only `/`

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Device missing after attach | Not rescanned / wrong guest tools | Rescan SCSI/NVMe; check cloud console |
| `mount` fails | Bad UUID / dirty FS | `blkid`, `fsck` on **unmounted** FS only |
| Boot hangs on disk | fstab without `nofail` | Rescue mode; fix fstab |
| Empty mount point after reboot | fstab not updated | Add UUID line; `findmnt` |
| Wrong disk wiped | Skipped discovery | Restore from backup; enforce checklists |

## Summary

Discover with `lsblk`, change only the intended device, format deliberately, mount by UUID, and persist mounts carefully. Practise on loop devices before real cloud volumes. Next: [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md).

## Interview Questions

**1. Why prefer UUID in `/etc/fstab` over `/dev/sdb1`?**

??? success "Reveal answer"
    Kernel device names can **reorder** across reboots or when disks are added. A UUID from `blkid` stays with the filesystem, so the correct volume mounts even if the `/dev` name changes.

**2. Walk through attaching a new empty cloud data disk on Ubuntu.**

??? success "Reveal answer"
    Attach in the cloud console → `lsblk -f` to identify the empty disk → partition (GPT) → `mkfs` → create mount point → mount by UUID → write a canary file → add `fstab` with `UUID=` and usually `nofail` → reboot test on a non-prod twin. Never skip discovery.

**3. What does `nofail` do in fstab, and when do you use it?**

??? success "Reveal answer"
    **`nofail`** lets the system continue booting if that mount fails (for example a secondary volume is detached). Use it for optional data disks. Do not put `nofail` on the root filesystem.

**4. How do you unmount a busy filesystem safely?**

??? success "Reveal answer"
    Stop services using it, find open files with `lsof`/`fuser`, then `umount`. Avoid lazy/force unmounts on databases unless you accept corruption risk and have a recovery plan.

**5. When would you choose XFS over ext4 for a data volume?**

??? success "Reveal answer"
    **XFS** is common for large volumes and some RHEL-family defaults; **ext4** is ubiquitous and simple on Ubuntu. Choose based on distro standards, size, and team operational experience — and know how to grow the filesystem you pick.

**6. How does a loop device help you practise safely?**

??? success "Reveal answer"
    A **loop device** presents a file as a block device. You can partition and `mkfs` without risking the real OS disk. It is ideal for labs and CI storage tests.

**7. What evidence would you attach to a “data disk mounted” change ticket?**

??? success "Reveal answer"
    `lsblk -f`, `blkid`, `findmnt` for the mount point, the exact `fstab` line (UUID), and a canary file read test. Before/after reboot proof is even better.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md) *(previous)*
- [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md) *(next)*
- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) *(related)*

## References

- [`lsblk(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/lsblk.8.html) — Ubuntu man-pages
- [`mkfs.ext4(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/mkfs.ext4.8.html) — create ext4
- [systemd mount units](https://www.freedesktop.org/software/systemd/man/systemd.mount.html) — alternative to fstab
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
