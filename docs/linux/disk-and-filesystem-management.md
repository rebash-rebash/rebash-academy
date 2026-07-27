---
title: Disk and Filesystem Management
description: Monitor capacity with df and du, map block devices with lsblk, configure mounts and fstab, introduce LVM, and diagnose inode exhaustion.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - storage
  - filesystem
  - lvm
prerequisites:
  - Remote systemd Service Control
  - Linux Filesystem Hierarchy
comments: false
---

# Disk and Filesystem Management

## Overview

Disk full alerts are among the most common production pages — and among the most misunderstood. A filesystem can report **100% used** because of large files (block exhaustion) or millions of tiny files (**inode exhaustion**). Admins who only watch `df -h` miss half the story.

This tutorial teaches you to inspect block devices, measure usage with `df` and `du`, configure persistent mounts in `/etc/fstab`, understand LVM basics for flexible volume sizing, and diagnose the "disk full but df shows space" paradox.

This is **Module 6, Tutorial 13** in the REBASH Academy Linux series.

## Prerequisites

- [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md) — mount points and `/etc` layout
- [Remote systemd Service Control](remote-systemd-services.md) or comfort with `sudo`
- A Linux VM with at least one disk (labs are read-only except fstab inspection and loop-device demos)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Interpret `df -hT` and `du -sh` output for capacity planning
- [ ] Map disks, partitions, and filesystems with `lsblk` and `findmnt`
- [ ] Mount and unmount filesystems; explain `/etc/fstab` fields and `nofail`
- [ ] Describe LVM components (PV, VG, LV) and when to use them
- [ ] Diagnose inode exhaustion vs block exhaustion
- [ ] Identify large directories and open-but-deleted files consuming space

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Hardware
        A["Physical Disk /dev/sda"]
    end
    subgraph Partitions
        B["/dev/sda1 boot"]
        C["/dev/sda2 LVM PV"]
    end
    subgraph LVM
        D[Volume Group vg0]
        E["LV root /dev/vg0/root"]
        F["LV data /dev/vg0/data"]
    end
    subgraph Filesystems
        G["ext4 on /"]
        H["xfs on /var"]
    end
    subgraph Mount["Points"]
        I["/"]
        J["/var"]
    end
    A --> B
    A --> C
    C --> D
    D --> E
    D --> F
    E --> G
    F --> H
    G --> I
    H --> J```

## Theory

### Block devices, partitions, and filesystems

| Layer | Example | Purpose |
|-------|---------|---------|
| Block device | `/dev/sda`, `/dev/nvme0n1` | Raw disk or virtual disk |
| Partition | `/dev/sda1`, `/dev/nvme0n1p2` | Slice of disk |
| LVM logical volume | `/dev/vg0/root` | Flexible volume on PV(s) |
| Filesystem | ext4, xfs, btrfs | Index of files and free space |
| Mount point | `/`, `/var`, `/data` | Directory where tree attaches |

Formatting (`mkfs.ext4`, `mkfs.xfs`) creates the filesystem structure. **Mounting** attaches it to the directory tree. Until mounted, data on the device is inaccessible through normal paths.

### df — filesystem-level usage

`df` reports **mounted** filesystems:

- `-h` — human-readable sizes
- `-T` — show filesystem type
- `-i` — **inode** usage (critical for mail queues, container layers, `node_modules`)
- `--output=source,fstype,size,used,avail,pcent,target` — custom columns

`df` shows space available to **non-root** users (may reserve 5% on ext4 via `-m`/`tunable`).

### du — directory-level usage

`du` walks directories and sums file sizes:

- `-s` — summary only
- `-h` — human-readable
- `-x` — stay on one filesystem (do not cross mount points)
- `--max-depth=1` — one level of subdirectories
- `-a` — count files, not just directories

`du` is slower than `df` on large trees but finds **which path** grew. Discrepancies between `df` and `du` often mean deleted-but-open files or mount overlays.

### lsblk and findmnt

`lsblk` lists block devices as a tree — essential for understanding **what is mounted where**:

- `-f` — show filesystem type, UUID, label
- `-o NAME,SIZE,FSTYPE,MOUNTPOINT,UUID` — custom columns

`findmnt` reads `/proc/self/mountinfo` — authoritative mount table:

```bash
findmnt /
findmnt -D   # disk usage per mount (if supported)
```

### /etc/fstab — persistent mounts

Each line: `device UUID=... fs_type options dump pass`

Example:

```
UUID=a1b2c3d4-...  /data  xfs  defaults,nofail  0  2
```

| Field | Meaning |
|-------|---------|
| Device | UUID (preferred), LABEL, or path |
| Mount point | Directory (must exist) |
| Type | ext4, xfs, nfs, tmpfs, ... |
| Options | `defaults`, `noatime`, `nofail`, `x-systemd.automount` |
| dump | Legacy backup flag (0 = ignore) |
| pass | fsck order (0 = skip, 1 = root, 2+ = other) |

Use **`UUID=`** — device names (`/dev/sda1`) can shift after reboot on cloud VMs.

`nofail` prevents boot hang if a non-critical volume is missing (common for data disks).

Always run `sudo mount -a` after editing fstab to validate syntax before reboot.

### LVM introduction

**Logical Volume Manager** decouples filesystems from physical disk layout:

| Term | Meaning |
|------|---------|
| PV (Physical Volume) | Disk or partition initialized with `pvcreate` |
| VG (Volume Group) | Pool of PV storage (`vgcreate`) |
| LV (Logical Volume) | Slice of VG presented as `/dev/vgname/lvname` |

Workflow: partition → `pvcreate` → `vgcreate` → `lvcreate` → `mkfs` → mount.

Benefits: grow/shrink volumes (xfs grow online; ext4 resize), snapshots, multi-disk groups.

Inspect:

```bash
pvs && vgs && lvs
lsblk -f
```

Cloud images often ship with LVM on root (`/dev/ubuntu-vg/ubuntu-lv`). Know how to extend when the hypervisor disk grows.

### Inode exhaustion

Filesystems preallocate **inodes** — one per file/directory/symlink. Creating millions of small files (session caches, maildirs, `npm install`, Docker layers) exhausts inodes while **blocks** remain free.

Symptoms:

- `No space left on device` when creating small files
- `df -h` shows available space
- `df -i` shows 100% IUse%

Fix: delete unnecessary small files, archive, or rebuild filesystem with higher inode ratio (requires backup and recreate — plan ahead at format time with `mkfs.ext4 -N`).

## Hands-on Lab

### Step 1 – Filesystem overview with df

```bash
df -hT
df -hT / /tmp
df -i /
```

**Expected output:** table of filesystems with Type, Size, Used, Avail, Use%, and Mountpoint; inode usage for `/` with IUse% column.

Identify the root filesystem device:

```bash
findmnt -n -o SOURCE /
```

**Expected output:** e.g., `/dev/sda1` or `/dev/mapper/vg0-root`.

### Step 2 – Directory sizing with du

```bash
du -sh ~/* 2>/dev/null | sort -hr | head -10
du -x --max-depth=1 /var 2>/dev/null | sort -hr | head -10
```

**Expected output:** largest directories in home and `/var` with human-readable sizes.

Compare du sum on root vs df (expect du lower — it does not count other mount points when using `-x`):

```bash
sudo du -shx / 2>/dev/null
df -h /
```

**Expected output:** two size figures — `du` often slightly less than `df` Used due to reserved blocks and metadata.

### Step 3 – Block device tree with lsblk

```bash
lsblk
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,UUID
lsblk -f
```

**Expected output:** tree showing disks → partitions → LVs with mount points and UUIDs.

List LVM if present:

```bash
sudo pvs 2>/dev/null; sudo vgs 2>/dev/null; sudo lvs 2>/dev/null
```

**Expected output:** PV/VG/LV summary or "command not found" / empty on non-LVM systems.

### Step 4 – Active mounts

```bash
findmnt
mount | column -t | head -15
cat /etc/fstab
```

**Expected output:** hierarchical mount list; `/etc/fstab` entries with UUIDs and options.

Explain one fstab line:

```bash
awk '!/^#/ && NF {print "Device:", $1, "| Mount:", $2, "| Type:", $3, "| Options:", $4}' /etc/fstab | head -5
```

**Expected output:** parsed fields from non-comment fstab lines.

### Step 5 – Manual mount with loop device (safe lab)

Create a file-backed filesystem without touching real disks:

```bash
mkdir -p ~/lab/mnt
dd if=/dev/zero of=~/lab/disk.img bs=1M count=64 status=progress
mkfs.ext4 -F ~/lab/disk.img
sudo mount -o loop ~/lab/disk.img ~/lab/mnt
df -h ~/lab/mnt
echo "lab data" | sudo tee ~/lab/mnt/testfile.txt
```

**Expected output:** ~64M ext4 mounted at `~/lab/mnt`, test file written.

Unmount when done:

```bash
sudo umount ~/lab/mnt
```

### Step 6 – fstab entry for loop mount (inspect only)

Example fstab line you would add for persistence (do not apply blindly):

```
/home/YOURUSER/lab/disk.img  /home/YOURUSER/lab/mnt  ext4  loop,defaults,nofail  0  2
```

Validate syntax concept:

```bash
grep -v '^#' /etc/fstab | awk 'NF {print NR, $0}' | head -5
```

**Expected output:** numbered active fstab entries from your system.

### Step 7 – Simulate inode pressure awareness

Create many tiny files in lab directory (safe, in home):

```bash
mkdir -p ~/lab/inode-test
for i in $(seq 1 5000); do touch ~/lab/inode-test/file_$i; done
df -i ~/lab/inode-test
ls ~/lab/inode-test | wc -l
rm -rf ~/lab/inode-test
```

**Expected output:** inode use percentage ticks up slightly; file count `5000`.

Check current inode headroom:

```bash
df -i | awk 'NR==1 || $5+0 > 50 {print}' | column -t
```

**Expected output:** filesystems with more than 50% inode use (or header row only if all healthy).

### Step 8 – Find deleted-but-open files (df vs du mystery)

Identify processes holding deleted files open (common log rotation issue):

```bash
sudo lsof +L1 2>/dev/null | head -10
```

**Expected output:** processes with `(deleted)` in NAME column if any exist; may be empty on clean systems.

If a deleted log holds space, restarting the service releases it:

```bash
# Diagnostic only — example pattern
sudo lsof +L1 2>/dev/null | awk '/deleted/ {print $1, $2, $7, $NF}' | head -5
```

**Expected output:** PID, size, and filename for deleted open files when present.

## Commands

| Command | Description |
|---------|-------------|
| `df -hT` | Human-readable filesystem usage with types |
| `df -i` | Inode usage per filesystem |
| `df -h /path` | Usage for filesystem containing path |
| `du -sh PATH` | Total size of path |
| `du -h --max-depth=1 DIR` | Size of immediate subdirectories |
| `du -x /` | Summarize root without crossing mounts |
| `lsblk` | List block devices as tree |
| `lsblk -f` | Include filesystem and UUID |
| `findmnt TARGET` | Show mount info for path |
| `mount DEVICE MOUNTPOINT` | Temporary mount |
| `umount MOUNTPOINT` | Unmount filesystem |
| `mount -a` | Mount all fstab entries (test after edits) |
| `blkid` | Show UUID and filesystem type of devices |
| `pvs` / `vgs` / `lvs` | LVM physical/volume/logical volume summary |
| `mkfs.ext4 DEVICE` | Create ext4 filesystem (destructive) |
| `lsof +L1` | Find deleted files still held open |
| `tune2fs -l DEVICE` | ext4 superblock info including inode count |

## Code

### Disk alert script (integrates with shell scripting)

```bash
#!/bin/bash
set -euo pipefail

THRESHOLD="${1:-85}"
WARN=()

while read -r fs used pct mount; do
  pct_num="${pct%%%}"
  if (( pct_num >= THRESHOLD )); then
    WARN+=("$mount at ${pct} ($fs)")
  fi
done < <(df -H | awk 'NR>1 {print $1, $3, $5, $6}')

count=0
for _ in "${WARN[@]}"; do count=$((count + 1)); done
if (( count > 0 )); then
  printf 'DISK WARNING (threshold %s%%):\n' "$THRESHOLD"
  printf '  - %s\n' "${WARN[@]}"
  exit 1
fi
echo "All filesystems below ${THRESHOLD}%"
```

### Inode check script

```bash
#!/bin/bash
set -euo pipefail

THRESHOLD="${1:-90}"

df -i | awk -v t="$THRESHOLD" '
  NR>1 {
    gsub(/%/,"",$5)
    if ($5+0 >= t) printf "INODE ALERT: %s on %s (%s%% used)\n", $1, $6, $5
  }'
```

### Safe fstab backup before edits

```bash
sudo cp -a /etc/fstab "/etc/fstab.bak.$(date +%Y%m%d_%H%M%S)"
sudo chmod 644 /etc/fstab
# edit fstab
sudo mount -a   # validates entries — fails loudly on error
```

## Common Mistakes

!!! warning "Using /dev/sda1 in fstab on cloud VMs"
    Device names reorder after resize or attach. Always use `UUID=` from `blkid` or `lsblk -f`.

!!! warning "Forgetting to create mount point directory"
    `mount /data` fails if `/data` does not exist. `mkdir -p /data` first.

!!! warning "Running mkfs on the wrong device"
    `mkfs.ext4 /dev/sdb` destroys all data. Triple-check with `lsblk` and current mounts.

!!! warning "Ignoring inode usage until creation fails"
    Monitor `df -i` alongside `df -h` on mail servers, CI caches, and container hosts.

## Best Practices

!!! tip "Monitor both bytes and inodes"
    Alert on block **and** inode thresholds (e.g., 85% bytes, 80% inodes).

!!! tip "Use UUIDs and nofail for data volumes"
    Boot should succeed even if a secondary data disk is temporarily unavailable.

!!! tip "Plan LVM before emergency resize"
    Document VG name, LV paths, and whether filesystem is xfs (grow only) or ext4 (shrink possible offline).

!!! tip "Find growth with du before buying disks"
    Weekly `du -x --max-depth=1 /var` trending catches log and cache bloat early.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `No space left on device` but df shows space | Inode exhaustion | `df -i`; delete small files or archive |
| df Used >> du on same mount | Deleted open files | `lsof +L1`; restart holding process |
| `mount: wrong fs type` | Missing module or wrong type | `modprobe xfs`; verify with `blkid` |
| Boot hangs waiting for disk | fstab entry for missing disk | Add `nofail,x-systemd.device-timeout=5` or fix UUID |
| Cannot unmount: target is busy | Process using mount | `sudo fuser -vm /mount`; stop services |
| LVM LV not visible | VG not activated | `sudo vgchange -ay`; check `pvs` |
| Resize failed | Filesystem type limits | xfs: grow only with `xfs_growfs`; ext4: `resize2fs` |
| Permission denied on du /var | Need root for some dirs | `sudo du -sh /var/*` |

## Summary

- **df** measures mounted filesystem capacity; **du** finds which directories consume space — use both.
- **lsblk** and **findmnt** map devices to mount points; prefer **UUID** in `/etc/fstab` over device paths.
- **LVM** (PV → VG → LV) adds flexibility for growing cloud disks and managing storage pools.
- **Inode exhaustion** causes write failures despite free blocks — monitor `df -i` on high-file-count systems.
- Deleted-but-open files explain df/du gaps — `lsof +L1` and service restarts recover "missing" space.

## Interview Questions

1. What is the difference between `df` and `du`? When would they disagree significantly?
2. Explain each field in an `/etc/fstab` line.
3. Why use UUID instead of `/dev/sda1` in fstab?
4. What are PV, VG, and LV in LVM?
5. How do you diagnose inode exhaustion?
6. What does the `nofail` mount option do?
7. A log file was deleted but disk space was not freed. Why, and how do you fix it?
8. Can you shrink an XFS filesystem online? What about ext4?
9. What does `du -x` do, and why is it useful when analyzing `/`?
10. What is the purpose of `pass` field values 0, 1, and 2 in fstab?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Remote systemd Service Control](remote-systemd-services.md) *(previous)*
- [Log Management with journalctl](log-management-journalctl.md) *(next)*
- [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [Linux kernel filesystem documentation](https://www.kernel.org/doc/html/latest/filesystems/index.html)
- [LVM HOWTO (TLDP)](https://tldp.org/HOWTO/LVM-HOWTO/)
- [XFS administration guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/managing_file_systems/assembly_xfs-file-system_managing-file-systems)
- [Filesystem Hierarchy Standard — /etc/fstab role](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [REBASH Academy – Linux Overview](index.md)
