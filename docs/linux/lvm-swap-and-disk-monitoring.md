---
title: "LVM, Swap, and Disk Monitoring"
description: "Linux LVM basics, swap, and disk health signals — plain language first, then a loop-backed LVM lab."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 8 · Storage"
tags:
  - linux
  - lvm
  - swap
  - monitoring
  - beginners
prerequisites:
  - linux/storage-disks-partitions-and-filesystems
next:
  - linux/linux-networking-tools
related:
  - linux/disk-usage-and-file-attributes
interview: interview/linux
comments: false
---

# LVM, Swap, and Disk Monitoring

## Overview

**Logical Volume Manager (LVM)** and **swap** show up when disks need resizing or memory pressure hits. Monitoring prevents silent full-disk outages.

**Logical Volume Manager (LVM)** lets you grow storage online when a volume group has free space — useful when `/data` fills up on a cloud VM. **Swap** gives the kernel overflow room when Random Access Memory (RAM) is tight. **Disk monitoring** catches full disks and Input/Output (I/O) errors before users notice.

**Plain problem:** A database mount hits 95% full. Without LVM you might need a migration weekend. With LVM you can extend the logical volume and filesystem in minutes — if you planned PV/VG/LV correctly.

This tutorial builds a **loop-backed LVM stack** — never on your live root disk.

This is **Tutorial 13** in **Module 8: Storage** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md)
- A practice Ubuntu 22.04/24.04 VM with `sudo`
- Packages: `lvm2`, `e2fsprogs`
- ~512 MiB free under `$HOME` for loop files

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain PV → VG → LV in plain words and why LVM helps
- [ ] Create a loop-backed PV/VG/LV, format ext4, and mount it
- [ ] Extend an LV and grow ext4 online
- [ ] Inspect swap and basic disk space signals (`df`, `free`)
- [ ] Complete the lab under `~/rebash-linux/lab13` with evidence files
- [ ] Answer common fresher interview questions on LVM and swap

## Architecture

Physical volumes join a volume group; logical volumes are carved from the pool and hold filesystems. Swap is a separate area used when RAM is under pressure.

![Storage layout — PV, VG, LV, filesystem, mount](../assets/excalidraw/linux-storage-layout.svg)

## Theory

### The problem (before any jargon)

A team provisions 100 GiB for `/data`. Six months later they need 150 GiB. With plain partitions you often add a **new** disk and migrate. With **LVM**, if the volume group has free space, you **`lvextend`** the logical volume and **`resize2fs`** the filesystem — often without unmounting (ext4 online grow).

### LVM terms (simple words)

**Analogy:** PVs are bricks. The VG is the warehouse of bricks. LVs are rooms built from the warehouse. The filesystem is furniture inside a room.

| Term | Plain meaning |
|------|----------------|
| **PV** (Physical Volume) | Disk or partition enrolled in LVM |
| **VG** (Volume Group) | Pool of PV space |
| **LV** (Logical Volume) | Slice from VG — looks like `/dev/vg/lv` |
| **PE** | Allocation chunk inside VG |

**What you can say in an interview:** “LVM abstracts disks into a pool; I extend LV then filesystem when VG has free extents.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
sudo pvs
sudo vgs
sudo lvs
sudo lvextend -L +1G /dev/vg0/data
sudo resize2fs /dev/vg0/data
```

**Interview line:** “Extend LV first, then grow filesystem — order matters; shrinking is harder than growing.”

### Swap (simple words)

**Analogy:** RAM is your desk. Swap is a drawer — slower, but stops immediate panic when the desk overflows.

``` {.bash .ra-terminal title="Terminal"}
free -h
swapon --show
cat /proc/swaps
```

Too little swap → **Out-Of-Memory (OOM) killer** may kill random processes. Too much swap on slow disks → latency. Cloud VMs often have swap disabled or a small swap file — know your image policy.

### Disk monitoring basics

``` {.bash .ra-terminal title="Terminal"}
df -hT
df -i
dmesg -T | grep -iE 'I/O error|EXT4-fs error' | tail
```

Watch **space** (`df -h`), **inodes** (`df -i`), and kernel messages for hardware errors.

### Common pitfalls

- Running LVM commands on the **root** disk in a lab on shared server — catastrophic
- Extending LV but forgetting `resize2fs` / `xfs_growfs` — free space invisible to apps
- Shrinking filesystems casually — data loss risk; grow is the common ops path
- Ignoring inode exhaustion — `df -h` OK but cannot create files

## Hands-on Lab

### Objective

Build loop-backed PV/VG/LV, mount ext4, extend LV by 128 MiB and grow filesystem, capture swap/df evidence, tear down safely.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | Previous storage lab helpful |
| `sudo` | LVM and mkfs require root |
| Safety | **Only** files under `~/rebash-linux/lab13` |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab13 && cd ~/rebash-linux/lab13
```

### Real-world scenario

`/data` on a VM is an LV at 90% full. Change ticket: extend by 128 MiB without remount downtime (ext4 online grow). You rehearse on loop devices and attach `pvs/vgs/lvs` output to the ticket.

### Step-by-step tasks

#### Task 1 – Create loop PV and volume group

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
fallocate -l 384M lvm-brick.img
LOOP="$(sudo losetup -fP --show lvm-brick.img)"
echo "$LOOP" | tee loop.txt
sudo pvcreate "$LOOP"
sudo vgcreate lab13vg "$LOOP"
sudo pvs | tee pvs.txt
sudo vgs | tee vgs.txt
grep -q 'lab13vg' vgs.txt
```

!!! example "Expected output"
    `pvs.txt` and `vgs.txt` show `lab13vg` with ~384 MiB total.


#### Task 2 – Create LV, mkfs, mount

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
sudo lvcreate -L 200M -n datalv lab13vg
sudo lvs | tee lvs-before.txt
sudo mkfs.ext4 -L lab13data /dev/lab13vg/datalv
sudo mkdir -p /mnt/rebash-lab13
sudo mount /dev/lab13vg/datalv /mnt/rebash-lab13
df -h /mnt/rebash-lab13 | tee df-before.txt
echo "initial $(date -Is)" | sudo tee /mnt/rebash-lab13/seed.txt
grep -q lab13vg lvs-before.txt
```

!!! example "Expected output"
    `lvs-before.txt` shows `datalv` ~200M. `df-before.txt` shows ~200M size mounted at `/mnt/rebash-lab13`.


#### Task 3 – Extend LV and grow ext4 online

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
sudo lvextend -L +128M /dev/lab13vg/datalv
sudo resize2fs /dev/lab13vg/datalv
sudo lvs /dev/lab13vg/datalv | tee lvs-after.txt
df -h /mnt/rebash-lab13 | tee df-after.txt
grep -q '328M\|325M\|320M' df-after.txt || test "$(df -BM /mnt/rebash-lab13 --output=size | tail -1 | tr -dc '0-9')" -gt 250
```

!!! example "Expected output"
    Logical volume and `df` size increased by roughly 128 MiB while mounted. `seed.txt` still readable.


#### Task 4 – Swap and monitoring snapshot

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
free -h | tee free.txt
swapon --show | tee swap.txt
df -hT | tee df-all.txt
df -i /mnt/rebash-lab13 | tee df-inodes.txt
sudo vgs --noheadings -o vg_free lab13vg | tee vg-free.txt
echo "lab13 lvm OK" | tee evidence.txt
test -s evidence.txt
```

!!! example "Expected output"
    `free.txt` shows Mem and Swap lines. `vg-free.txt` shows remaining free space in `lab13vg`.


### Validation steps

- [ ] PV/VG/LV visible in pvs/vgs/lvs output
- [ ] Filesystem grew after lvextend + resize2fs
- [ ] Root disk untouched — only loop file used
- [ ] Swap and df snapshots saved

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Insufficient free space` on lvcreate | VG too small | Reduce `-L` or enlarge loop file |
| `resize2fs: Bad magic number` | mkfs not run | mkfs.ext4 on LV before mount |
| Size unchanged after lvextend | Forgot resize2fs | Run `resize2fs` for ext4 |
| `Can't deactivate LV` on cleanup | Still mounted | `umount` first |

### Challenge exercise

Add a second loop PV to the same VG (`lvm-brick2.img`), run `vgextend`, show larger VG size in `vgs`.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
fallocate -l 128M lvm-brick2.img
LOOP2="$(sudo losetup -fP --show lvm-brick2.img)"
echo "$LOOP2" | tee loop2.txt
sudo pvcreate "$LOOP2"
sudo vgextend lab13vg "$LOOP2"
sudo vgs lab13vg | tee vgs-extended.txt
grep -q 'lab13vg' vgs-extended.txt
```

### Learning outcomes

- You built PV/VG/LV on safe loop storage
- You extended LV and filesystem online
- You captured swap and disk monitoring baselines

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
sudo umount /mnt/rebash-lab13 2>/dev/null || true
sudo lvremove -f lab13vg/datalv 2>/dev/null || true
sudo vgremove -f lab13vg 2>/dev/null || true
for f in loop.txt loop2.txt; do
  [ -f "$f" ] || continue
  dev="$(cat "$f")"
  sudo pvremove -f "$dev" 2>/dev/null || true
  sudo losetup -d "$dev" 2>/dev/null || true
done
sudo rmdir /mnt/rebash-lab13 2>/dev/null || true
# Keep evidence txt files for revision
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab13`
- [ ] Can draw PV → VG → LV on paper
- [ ] Ready for Linux networking tools next

## Code Walkthrough

1. **`pvcreate` / `vgcreate` / `lvcreate`** — build stack bottom-up on lab loops only.
2. **`lvextend` then `resize2fs`** — two-step grow for ext4.
3. **`lvs` and `vgs`** — show free extents before promising capacity to app team.
4. **`df -i`** — inode checks alongside `-h`.
5. **Teardown order** — umount → lvremove → vgremove → pvremove → losetup -d.

## Security Considerations

- LVM changes on production require change windows and backups.
- Full disks can cause service writes to fail open — monitor thresholds.
- Swap on multi-tenant hosts can leak memory patterns — some clouds disable it.
- Restrict LVM commands via sudo policy on jump servers.
- Encrypt sensitive LVs (LUKS layer) when policy requires.

## Common Mistakes

!!! warning "LVM on root disk in a practice typo"
    `pvcreate /dev/sda2` on wrong host destroys systems. Fix: loop labs; confirm device with `lsblk` and tickets.

!!! warning "lvextend without filesystem grow"
    `df` stays same size. Fix: `resize2fs` (ext4) or `xfs_growfs` (XFS) after extend.

!!! warning "Ignoring inode full"
    Cannot create small files despite GB free. Fix: `df -i`; prune small files or expand.

!!! warning "Swap thrashing mistaken for CPU issue"
    High iowait with slow disk. Fix: `free -h`, `vmstat 1`; add RAM or fix memory leak.

## Best Practices

- Leave free extents in VG for growth — do not allocate 100% to one LV
- Monitor `/`, `/var`, and app mounts at 80% warning / 90% critical
- Document LV names and mount points in inventory
- Snapshot (cloud or LVM) before major shrink or layout changes
- Prefer separate LV for databases/logs from OS root

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| VG full | All extents allocated | Add PV (`vgextend`) or expand underlying disk |
| LV active but wrong size | Filesystem not grown | `resize2fs` / `xfs_growfs` |
| OOM kills despite free disk | No swap / RAM leak | Add RAM; fix leak; tune swap cautiously |
| I/O errors in dmesg | Failing disk / cloud volume | Replace volume; restore from backup |

## Summary

**LVM** pools disks into **VGs** and **LVs** you can extend. After **`lvextend`**, grow the **filesystem**. Monitor **df**, **inodes**, and **swap** before users hit errors. Next: **Linux networking tools**.

## Interview Questions

**1. What are PV, VG, and LV?**

??? success "Reveal answer"
    **Physical Volume (PV)** — disk/partition enrolled in LVM. **Volume Group (VG)** — pool combining PVs. **Logical Volume (LV)** — virtual partition carved from VG, e.g. `/dev/vg0/data`. Filesystems are created on LVs.

**2. Why use LVM?**

??? success "Reveal answer"
    Flexible allocation and **online grow** when free extents exist in the VG. Easier to add disks with `vgextend` than migrating plain partitions — common on cloud VMs with growing data volumes.

**3. What is the order to grow an ext4 filesystem on LVM?**

??? success "Reveal answer"
    **`lvextend`** (or `lvresize`) to enlarge the LV, then **`resize2fs`** on the LV device to grow the ext4 filesystem. Shrink is riskier and often needs unmount. XFS uses **`xfs_growfs`** on the mount point instead.

**4. What is swap used for?**

??? success "Reveal answer"
    Disk-backed overflow when physical RAM is exhausted — kernel pages out cold memory. Prevents immediate failure but is **slower than RAM**. Too little can trigger **OOM killer**; excessive swap use causes latency (thrashing).

**5. How do you check disk space and inodes?**

??? success "Reveal answer"
    **`df -h`** for human-readable space; **`df -i`** for inode usage; **`df -hT`** adds filesystem type. **`du -sh path`** for directory breakdown. Alert before 90% on production mounts.

**6. vgdisplay shows free PE — what does that mean?**

??? success "Reveal answer"
    **Physical Extents (PE)** are chunks in the VG not yet assigned to LVs — capacity you can allocate with `lvcreate` or **`lvextend`** without adding new disks.

**7. When would you avoid LVM?**

??? success "Reveal answer"
    Tiny single-purpose images (some containers), boot partitions, or when simplicity and portability beat flexibility. Some cloud managed disks + plain ext4 are enough for stateless nodes — LVM shines on growing data volumes and multi-disk pooling.

## Related Tutorials

- Prior: [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md)
- Next: [Linux Networking Tools](linux-networking-tools.md)
- Related: [Disk Usage and File Attributes](disk-usage-and-file-attributes.md)

## References

- [LVM HOWTO (Red Hat)](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/configuring_and_managing_logical_volumes/)
- [lvextend(8)](https://man7.org/linux/man-pages/man8/lvextend.8.html)
- [resize2fs(8)](https://man7.org/linux/man-pages/man8/resize2fs.8.html)
- [REBASH Linux course index](index.md)
