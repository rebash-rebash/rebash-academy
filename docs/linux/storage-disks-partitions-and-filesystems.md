---
title: "Disks, Partitions, and Filesystems"
description: "Linux discover disks, partition safely on a loop device, mkfs, mount by UUID — plain language first, then a hands-on lab."
difficulty: beginner
estimated_time: "55–65 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 8 · Storage"
tags:
  - linux
  - lsblk
  - fdisk
  - mkfs
  - mount
  - beginners
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

Disks, partitions, and filesystems decide whether your data is mountable, resumable after reboot, and safe to grow.

Attaching a cloud disk does nothing until you **discover** it, **partition** it, create a **filesystem**, **mount** it on a folder, and make that mount survive reboot. One wrong `mkfs` on the wrong device wipes data — learn safe patterns first.

**Plain problem:** You add a 50 GiB volume in AWS. It appears as `/dev/nvme1n1` but `df` does not show it. You need `lsblk`, a partition, `mkfs.ext4`, `mount`, and `/etc/fstab` with **UUID**.

This tutorial practises the full flow on a **file-backed loop device** — never touching your real OS disk.

This is **Tutorial 12** in **Module 8: Storage** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md)
- A practice Ubuntu 22.04/24.04 VM with `sudo`
- Packages: `util-linux`, `e2fsprogs` (usually preinstalled)
- **Warning:** Do **not** run `mkfs` or `fdisk` on real cloud disks until you can identify them with certainty

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain block device, partition, filesystem, and mount point in plain words
- [ ] Discover devices with `lsblk` and read UUIDs with `blkid`
- [ ] Create a GPT partition on a loop device and format ext4 safely
- [ ] Mount by UUID and draft a correct `/etc/fstab` line (lab uses a test mount)
- [ ] Complete the lab under `~/rebash-linux/lab12` and clean up completely
- [ ] Answer common fresher interview questions on Linux storage

## Architecture

Applications see files in directories. The kernel maps those paths to a **filesystem** on a **partition** on a **block device** (disk or loop file).

![Linux storage layout — disk, partition, filesystem, mount](../assets/excalidraw/linux-storage-layout.svg)

## Theory

### The problem (before any jargon)

You SSH to a new VM. Someone says “put logs on `/data`.” There is no `/data` mount — only root `/`. You attach a volume in the cloud console. It shows up as `/dev/xvdf` but you still cannot write until you partition and format it.

Worse: `/dev/sdb` today might be `/dev/sdc` after reboot. **UUIDs** stay stable.

### Key terms (simple words)

**Analogy:** A **disk** is a plot of land. A **partition** is a fenced section. A **filesystem** is the filing system inside (ext4, XFS). A **mount point** is the door path (e.g. `/data`) where that filing system appears.

| Term | Plain meaning |
|------|----------------|
| **Block device** | `/dev/sda`, `/dev/nvme0n1`, `/dev/loop0` |
| **Partition** | Slice of a disk — `/dev/sda1`, `/dev/nvme0n1p1` |
| **Filesystem** | How files are stored — ext4, XFS |
| **Mount** | Attach filesystem tree to a directory |
| **UUID** | Unique ID for partition — use in fstab |

**What you can say in an interview:** “I lsblk to identify devices, partition with GPT, mkfs, mount by UUID, and fstab with nofail for cloud volumes.”

### Discover before you destroy

``` {.bash .ra-terminal title="Terminal"}
lsblk -f
sudo fdisk -l /dev/sda    # read only — do NOT experiment on root disk in prod
blkid
df -hT
```

**Interview line:** “I run `lsblk -f` twice and confirm serial/size before any mkfs — wrong device ends careers.”

### Partitioning and formatting (loop lab only here)

On a **loop file** (safe lab):

``` {.bash .ra-terminal title="Terminal"}
fallocate -l 256M disk.img
sudo losetup -fP --show disk.img    # creates /dev/loopN
sudo parted /dev/loopN mklabel gpt
sudo parted /dev/loopN mkpart primary ext4 1MiB 100%
sudo mkfs.ext4 -L labdata /dev/loopNp1
```

**Production warning:** On real servers, triple-check device names. Cloud APIs also expose serial numbers — match them to `lsblk`.

### Mount and fstab

``` {.bash .ra-terminal title="Terminal"}
sudo mkdir -p /mnt/data
sudo mount /dev/disk/by-uuid/YOUR-UUID /mnt/data
grep UUID /etc/fstab   # example line shown in lab — test with mount -a
```

fstab fields: `UUID=…  /mount  ext4  defaults,nofail  0  2`

**Interview line:** “nofail lets the host boot if a secondary cloud volume is detached; without it boot can hang in maintenance mode.”

### Common pitfalls

- `mkfs` on `/dev/sda` instead of `/dev/sdb` — wipes OS
- Using device names in fstab — order changes; use UUID
- Forgetting `partprobe` / `losetup -P` — partition nodes missing
- Skipping `umount` before cleanup — “device is busy”

## Hands-on Lab

### Objective

Build a complete loop-backed disk: partition, ext4, mount by UUID, prove with files, unmount and detach — zero impact on the OS disk.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | ~300 MiB free in `$HOME` |
| `sudo` | Required for loop, mkfs, mount |
| Safety | **Only** `disk.img` in lab dir is formatted |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab12 && cd ~/rebash-linux/lab12
```

### Real-world scenario

Platform team provisions a new data volume for `/var/log/app`. You must document: device name, partition, UUID, mount point, and fstab line. This lab rehearses those steps on a loop file so you cannot destroy the root disk.

### Step-by-step tasks

#### Task 1 – Create loop-backed disk image

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
fallocate -l 256M disk.img
LOOP="$(sudo losetup -fP --show disk.img)"
echo "$LOOP" | tee loop-device.txt
lsblk "$LOOP" | tee lsblk-before.txt
test -s loop-device.txt
```

!!! example "Expected output"
    `loop-device.txt` contains `/dev/loopN`. `lsblk` shows the loop device with no partitions yet.


#### Task 2 – GPT partition and ext4

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
LOOP="$(cat loop-device.txt)"
sudo parted -s "$LOOP" mklabel gpt
sudo parted -s "$LOOP" mkpart primary ext4 1MiB 100%
sudo partprobe "$LOOP"
PART="${LOOP}p1"
lsblk -f "$LOOP" | tee lsblk-after-part.txt
sudo mkfs.ext4 -L lab12data "$PART"
sudo blkid "$PART" | tee blkid.txt
grep -q 'UUID=' blkid.txt
```

!!! example "Expected output"
    `lsblk-after-part.txt` shows partition `p1`. `blkid.txt` includes `UUID="..."` and `LABEL="lab12data"`.


#### Task 3 – Mount by UUID and write proof file

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
UUID="$(grep -oP 'UUID="\K[^"]+' blkid.txt)"
echo "$UUID" | tee uuid.txt
sudo mkdir -p /mnt/rebash-lab12
sudo mount "UUID=$UUID" /mnt/rebash-lab12
mount | grep rebash-lab12 | tee mount-proof.txt
echo "lab12 stored $(date -Is)" | sudo tee /mnt/rebash-lab12/proof.txt
sudo cat /mnt/rebash-lab12/proof.txt | tee proof-readback.txt
df -h /mnt/rebash-lab12 | tee df-lab12.txt
test -s proof-readback.txt
```

!!! example "Expected output"
    `mount-proof.txt` shows ext4 on `/mnt/rebash-lab12`. `proof.txt` content appears in readback.


#### Task 4 – Draft fstab line (not installed) and diagnose busy umount

Create `fstab-snippet.txt`:

```text title="fstab-snippet.txt"
UUID=REPLACE-UUID  /mnt/rebash-lab12  ext4  defaults,nofail  0  2
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
sed "s/REPLACE-UUID/$(cat uuid.txt)/" fstab-snippet.txt > fstab-snippet.local.txt
grep "$(cat uuid.txt)" fstab-snippet.local.txt | tee fstab-line.txt
sudo umount /mnt/rebash-lab12
mount | grep rebash-lab12 && echo "still mounted" || echo "unmounted OK" | tee umount-proof.txt
grep -q 'unmounted OK' umount-proof.txt
echo "lab12 storage OK" | tee evidence.txt
```

!!! example "Expected output"
    `fstab-line.txt` is a valid-looking fstab entry. `umount-proof.txt` shows `unmounted OK`.


### Validation steps

- [ ] Only `disk.img` / loop device was formatted — root disk untouched
- [ ] UUID recorded in `uuid.txt` and used for mount
- [ ] Proof file written on mounted filesystem
- [ ] Successfully unmounted before cleanup continues

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `parted: invalid device` | Loop not attached | Re-run losetup; check `loop-device.txt` |
| `mkfs.ext4: Device size` | Partition not created | `partprobe`; check `${LOOP}p1` exists |
| `mount: unknown UUID` | Typo in UUID | Copy from `blkid.txt` exactly |
| `target is busy` on umount | Shell cwd on mount | `cd ~`; `sudo lsof +f -- /mnt/rebash-lab12` |

### Challenge exercise

Create `lab12-mount-check.sh` that reads `uuid.txt`, mounts if unmounted, runs `touch` proof, and unmounts.

Create `lab12-mount-check.sh`:

```bash title="lab12-mount-check.sh"
#!/usr/bin/env bash
set -euo pipefail
lab="$HOME/rebash-linux/lab12"
uuid="$(cat "$lab/uuid.txt")"
mp="/mnt/rebash-lab12"
sudo mkdir -p "$mp"
if mountpoint -q "$mp"; then
  echo "already mounted"
else
  sudo mount "UUID=$uuid" "$mp"
fi
echo "challenge $(date -Is)" | sudo tee -a "$mp/challenge.txt"
sudo umount "$mp"
echo "mount cycle OK"
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
chmod +x lab12-mount-check.sh
./lab12-mount-check.sh | tee challenge-out.txt
grep -q 'mount cycle OK' challenge-out.txt
sudo cat /mnt/rebash-lab12/challenge.txt 2>/dev/null || sudo mount UUID="$(cat uuid.txt)" /mnt/rebash-lab12 && sudo cat /mnt/rebash-lab12/challenge.txt | tail -1
sudo umount /mnt/rebash-lab12 2>/dev/null || true
```

### Learning outcomes

- You practised full disk workflow on a safe loop device
- You mounted by UUID and drafted fstab with nofail
- You can explain why device names are risky in fstab

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab12
sudo umount /mnt/rebash-lab12 2>/dev/null || true
LOOP="$(cat loop-device.txt 2>/dev/null || true)"
if [ -n "${LOOP:-}" ]; then sudo losetup -d "$LOOP"; fi
sudo rmdir /mnt/rebash-lab12 2>/dev/null || true
# Keep disk.img and evidence for revision; losetup -d releases loop
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab12`
- [ ] Can explain block device → partition → filesystem → mount
- [ ] Ready for LVM and swap next

## Code Walkthrough

1. **`lsblk -f`** — one view of name, size, FSTYPE, UUID.
2. **Loop lab** — same commands as cloud disk without risking `/dev/sda`.
3. **`mount UUID=…`** — survives device rename across reboots.
4. **`nofail` in fstab** — cloud volumes may detach; host should still boot.
5. **`umount` before `losetup -d`** — clean teardown order.

## Security Considerations

- Destructive commands (`mkfs`, `parted mklabel`) require change tickets on production.
- Encrypt sensitive data volumes (LUKS or cloud-managed keys) at rest.
- Restrict `sudo` for disk operations on shared hosts.
- Label volumes in cloud console to match `lsblk` serial — reduces wrong-disk risk.
- Back up before resize or repartition operations.

## Common Mistakes

!!! warning "mkfs on the OS disk"
    One typo in `/dev/sda` vs `/dev/sdb` destroys the server. Fix: use loop labs first; match cloud serial; read `lsblk` twice.

!!! warning "Device names in /etc/fstab"
    `/dev/xvdf` can reorder. Fix: **`UUID=`** or **`LABEL=`** from `blkid`.

!!! warning "Missing nofail on cloud data volumes"
    Boot hangs in emergency mode if volume absent. Fix: add `nofail` (and often `x-systemd.device-timeout=`).

!!! warning "Formatting without umount"
    mkfs on mounted filesystem corrupts data. Fix: `umount` first; confirm with `findmnt`.

## Best Practices

- Document UUID, mount point, and purpose in inventory
- Use GPT for new disks (>2 TiB needs GPT anyway)
- Test fstab with `sudo mount -a` after edits (on maintenance window)
- Separate `/var`, `/data`, and databases onto dedicated volumes in production
- Snapshot cloud volumes before destructive changes

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| New disk not visible | Not attached in hypervisor | Attach volume; `lsblk` refresh |
| Partition node missing | Kernel not re-read table | `partprobe` or reboot |
| fstab boot failure | Wrong UUID or missing nofail | Use rescue/console; fix fstab |
| `disk full` but df OK | Inodes exhausted | `df -i`; small-file explosion |

## Summary

**Block devices** hold **partitions**; **filesystems** store files; **mount** connects them to paths. Always identify with **`lsblk`**, format the **correct** device, mount by **UUID**, and use **`nofail`** for optional cloud volumes. Next: **LVM**, **swap**, and **disk monitoring**.

## Interview Questions

**1. What is the difference between a partition and a filesystem?**

??? success "Reveal answer"
    A **partition** is a slice of a disk (layout on the block device). A **filesystem** is the structure (ext4, XFS) that stores files inside that partition. You partition first, then `mkfs` to create the filesystem, then mount.

**2. Why use UUID in /etc/fstab instead of /dev/sdb?**

??? success "Reveal answer"
    Device names like `/dev/sdb` can change order across reboots or after attaching volumes. **UUID** (or LABEL) stays tied to the formatted partition — safer for persistent mounts, especially on cloud VMs.

**3. What does lsblk show?**

??? success "Reveal answer"
    A tree of block devices, partitions, sizes, mount points, and filesystem types (`-f` adds FSTYPE and UUID). First diagnostic command before partitioning or mkfs.

**4. What is a loop device?**

??? success "Reveal answer"
    A kernel block device backed by a regular file (`losetup` on `disk.img`). Lets you practise partitioning/mkfs without extra hardware — same tools as real disks, safer for learning.

**5. What does nofail do in fstab?**

??? success "Reveal answer"
    If the volume cannot be mounted at boot, the system **continues booting** instead of dropping to emergency mode. Important for optional or attachable cloud data volumes that may be absent.

**6. How do you safely add a new cloud volume?**

??? success "Reveal answer"
    Attach in console → `lsblk` / match serial → partition (GPT) → `mkfs` on the **data** partition only → mount by UUID → add fstab with `nofail` → `mount -a` test → document.

**7. mkfs says device is mounted — what now?**

??? success "Reveal answer"
    **Never mkfs a mounted filesystem** — you will corrupt live data. `umount` the mount point (fix busy with `lsof`/`fuser`), confirm with `findmnt`, then mkfs only if you intend to erase that partition.

## Related Tutorials

- Prior: [systemd Targets, Timers, and Boot](systemd-targets-timers-and-boot.md)
- Next: [LVM, Swap, and Disk Monitoring](lvm-swap-and-disk-monitoring.md)
- Related: [Disk Usage and File Attributes](disk-usage-and-file-attributes.md)

## References

- [lsblk(8)](https://man7.org/linux/man-pages/man8/lsblk.8.html)
- [fstab(5)](https://man7.org/linux/man-pages/man5/fstab.5.html)
- [ext4 wiki](https://ext4.wiki.kernel.org/)
- [REBASH Linux course index](index.md)
