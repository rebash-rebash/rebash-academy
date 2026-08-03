---
title: "LVM, Swap, and Disk Monitoring"
description: "Build a loop-backed LVM volume, extend it online, check swap, and monitor disk health signals on Ubuntu."
difficulty: intermediate
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 8 · Storage"
tags:
  - linux
  - lvm
  - swap
  - monitoring
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

**Logical Volume Manager (LVM)** turns “we need 50 GiB more” into an online extend instead of a migration weekend. You group physical volumes (PVs) into a volume group (VG), carve logical volumes (LVs), put a filesystem on an LV, and later grow the LV and filesystem when the VG has free space.

**Swap** is overflow space when RAM is under pressure. Too little swap can cause the Out-Of-Memory (OOM) killer; too much slow disk swap hurts latency. **Disk monitoring** watches free space, inode use, and Input/Output (I/O) errors before users feel pain.

In this tutorial you will create a small loop-backed LVM stack, extend a logical volume, inspect swap, capture basic monitoring signals, and save proof under `~/rebash-linux/lab13`. Practise only on disposable images — never experiment with LVM on the live root disk of a shared server.

This is **Tutorial 13** in **Module 8: Storage** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo`
- Packages: `lvm2`, `e2fsprogs`
- ~1 GiB free under `$HOME`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain PV → VG → LV and why LVM helps grow data volumes
- [ ] Create a loop-backed PV/VG/LV, format and mount it
- [ ] Extend an LV and grow an ext4 filesystem online
- [ ] Inspect swap with `swapon --show` and `free`
- [ ] Capture monitoring evidence under `~/rebash-linux/lab13`

## Architecture

LVM sits between physical disks and filesystems so you can grow logical volumes without remapping application mount points.

![Architecture diagram for LVM, Swap, and Disk Monitoring](../assets/excalidraw/linux-storage-layout.svg)

## Theory

### What it is

| Object | Role |
|--------|------|
| PV | Physical volume — disk or partition initialised for LVM |
| VG | Volume group — pool of space from one or more PVs |
| LV | Logical volume — block device you format and mount |
| Swap | Backing for anonymous memory under RAM pressure |

``` {.bash .ra-terminal title="Terminal"}
sudo pvs; sudo vgs; sudo lvs
swapon --show
free -h
```

### Why it matters

Cloud disks can be resized in the console, but applications need the **LV and filesystem** grown too. Without monitoring, you learn about full disks from failed writes. Swap misconfiguration shows up as latency spikes or sudden OOM kills.

### How it works

1. `pvcreate` → `vgcreate` → `lvcreate`  
2. `mkfs` on `/dev/vg/lv` → mount  
3. Add space: grow disk/PV or add PV → `lvextend` → `resize2fs`/`xfs_growfs`  
4. Watch: `df`, `vgs`, smart/cloud disk metrics, `iostat`

| Task | Command family |
|------|----------------|
| Create | `pvcreate`, `vgcreate`, `lvcreate` |
| Grow LV | `lvextend -L +size` or `-l +100%FREE` |
| Grow ext4 | `resize2fs` (often online while mounted) |
| Swap | `swapon --show`, `mkswap` (careful on prod) |

### Common pitfalls

- Extending the cloud disk but forgetting `pvresize` / `lvextend` / filesystem grow.
- Running LVM experiments on the root VG of a shared host.
- Assuming swap fixes a memory leak (it only delays failure).
- Ignoring read-only remounts after I/O errors.

## Hands-on Lab

### Objective

Build a loop-backed VG with a small LV, mount it, extend the LV using free VG space, grow ext4, inspect swap, and pack evidence under `~/rebash-linux/lab13`.

### Prerequisites

- Ubuntu with `sudo` and ability to install `lvm2`

### Lab environment

Workspace: `~/rebash-linux/lab13`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab13 && cd ~/rebash-linux/lab13
set -euo pipefail
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y lvm2 e2fsprogs
sudo vgs | tee vgs-before.txt || true
free -h | tee free-before.txt
swapon --show | tee swapon-before.txt || true
```

!!! example "Expected output"
    `lvm2` installed; baseline memory/swap files exist.


### Real-world scenario

An app data volume will need growth next month. You rehearse LVM create + online extend on a loop-backed lab VG named `rebashvg`, prove the filesystem grew, and attach command output to the capacity plan.

### Step-by-step tasks

#### Task 1 – Loop PVs, VG, and LV

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
set -euo pipefail

dd if=/dev/zero of=pv1.img bs=1M count=384 status=none
dd if=/dev/zero of=pv2.img bs=1M count=384 status=none
LOOP1="$(sudo losetup -fP --show pv1.img)"
LOOP2="$(sudo losetup -fP --show pv2.img)"
echo "$LOOP1" | tee loop1.txt
echo "$LOOP2" | tee loop2.txt

sudo pvcreate "$LOOP1" "$LOOP2"
sudo vgcreate rebashvg "$LOOP1" "$LOOP2"
# Create a 200MiB LV, leave free space in the VG for Task 2
sudo lvcreate -n data -L 200M rebashvg
sudo mkfs.ext4 -F /dev/rebashvg/data

sudo mkdir -p /mnt/rebash-lvm
sudo mount /dev/rebashvg/data /mnt/rebash-lvm
df -h /mnt/rebash-lvm | tee df-before-extend.txt
sudo vgs rebashvg | tee vgs-lab.txt
sudo lvs rebashvg | tee lvs-lab.txt
echo 'before-extend' | sudo tee /mnt/rebash-lvm/note.txt >/dev/null
```

!!! example "Expected output"
    `vgs-lab.txt` shows free space in `rebashvg`; `df-before-extend.txt` shows ~200M-class size for the mount.


#### Task 2 – Online extend LV + filesystem

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
set -euo pipefail

# Grow LV by 100MiB using free VG space
sudo lvextend -L +100M /dev/rebashvg/data
sudo resize2fs /dev/rebashvg/data
df -h /mnt/rebash-lvm | tee df-after-extend.txt
sudo lvs rebashvg | tee lvs-after.txt
sudo cat /mnt/rebash-lvm/note.txt | tee note-after.txt

# Size after extend should be larger than before (compare 2nd column roughly)
test -s df-after-extend.txt
grep -F 'before-extend' note-after.txt
```

!!! example "Expected output"
    `lvs-after.txt` shows a larger data LV (~300M); file content still present; `df-after-extend.txt` reflects growth.


#### Task 3 – Swap + monitoring signals + evidence

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
set -euo pipefail

free -h | tee free-after.txt
swapon --show | tee swapon-after.txt || true
cat /proc/swaps | tee proc-swaps.txt
df -hT /mnt/rebash-lvm / | tee df-monitor.txt
# Light I/O sample (if iostat present)
iostat -xz 1 2 | tee iostat.txt 2>/dev/null || echo 'iostat not installed' | tee iostat.txt

tar -czf lvm-evidence.tgz \
  vgs-before.txt free-before.txt swapon-before.txt \
  loop1.txt loop2.txt vgs-lab.txt lvs-lab.txt \
  df-before-extend.txt df-after-extend.txt lvs-after.txt note-after.txt \
  free-after.txt swapon-after.txt proc-swaps.txt df-monitor.txt iostat.txt
ls -l lvm-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    evidence archive exists; swap/memory files captured (swap may be empty on some cloud images — that is OK).


### Validation steps

- [ ] `sudo vgs rebashvg` shows the lab volume group
- [ ] LV grew and `resize2fs` completed while mounted
- [ ] Canary file survived the extend
- [ ] `lvm-evidence.tgz` exists under `~/rebash-linux/lab13`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `vgcreate` name in use | Previous lab left VG | Run Cleanup, or use a new VG name |
| `resize2fs: Permission denied` | Not root / wrong path | Use `sudo resize2fs /dev/rebashvg/data` |
| No free space to extend | LV consumed whole VG | Create smaller LV first (as in Task 1) |
| `iostat: command not found` | `sysstat` missing | Optional: `sudo apt-get install -y sysstat` |

### Challenge exercise

Add a third loop file `pv3.img` (128 MiB), `pvcreate` + `vgextend rebashvg`, then `lvextend -l +100%FREE` and `resize2fs`. Save `vgs`/`lvs`/`df` to `challenge-extend.txt`.

### Learning outcomes

- Built PV/VG/LV on loop devices
- Extended an LV and grew ext4 online
- Inspected swap and basic disk signals
- Packed LVM evidence for a capacity plan

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab13
set -euo pipefail

sudo umount /mnt/rebash-lvm 2>/dev/null || true
sudo lvremove -fy rebashvg/data 2>/dev/null || true
sudo vgremove -fy rebashvg 2>/dev/null || true
for f in loop1.txt loop2.txt; do
  if [[ -f "$f" ]]; then sudo losetup -d "$(cat "$f")" 2>/dev/null || true; fi
done
# Detach any remaining loops for pv3 if you did the challenge
sudo rmdir /mnt/rebash-lvm 2>/dev/null || true
rm -f pv1.img pv2.img pv3.img
# Keep lvm-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab13/` with evidence files
- [ ] You can explain PV, VG, and LV in one minute
- [ ] You know the grow order: disk/PV → LV → filesystem  
- [ ] You can read swap state with `free` and `swapon --show`

## Code Walkthrough

Production grow path:

1. Confirm which LV backs the full mount (`lsblk`, `df`, `findmnt`)  
2. Grow the cloud disk / add PV  
3. `pvresize` if the PV disk grew  
4. `lvextend` then filesystem grow tool  
5. Re-check `df` and application health  

## Security Considerations

- Limit who can run LVM and disk resize tools  
- Encrypt sensitive LVs when policy requires it  
- Do not disable swap as a “security tip” without understanding OOM behaviour  
- Monitor for sudden disk errors that can indicate failing hardware  
- Keep backups before destructive `lvremove`  

## Common Mistakes

!!! warning "Growing the cloud disk only"
    The guest still sees the old size until PV/LV/filesystem steps run. **Fix:** complete `pvresize` → `lvextend` → filesystem grow.

!!! warning "Experimenting on the root VG"
    Mistakes can make the host unbootable. **Fix:** use loop labs or a disposable data VG.

!!! warning "Thinking more swap fixes memory leaks"
    Swap delays OOM and adds latency. **Fix:** find the leak; size RAM/swap deliberately.

!!! warning "Ignoring read-only remounts"
    Kernel may remount ext4 read-only after errors. **Fix:** check `dmesg`/`journalctl`, run filesystem checks offline, restore from backup if needed.

## Best Practices

- Keep free space in VGs for emergency extends  
- Alert on VG% and filesystem%  
- Document LV → mount → application mapping  
- Test extend procedures on staging  
- Pair capacity metrics with I/O latency metrics  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `lvextend` fails | No free VG extents | Add PV / grow disk |
| `df` unchanged after `lvextend` | Forgot filesystem grow | `resize2fs` / `xfs_growfs` |
| High swap use | RAM pressure | Inspect processes; add RAM; fix leaks |
| I/O errors in journal | Failing disk / bad path | Cloud replace disk; restore |
| VG missing after reboot | Loop/lab disks gone | Expected for loop labs; real PVs need persistent devices |

## Summary

LVM gives you flexible volumes; swap backs RAM pressure; monitoring tells you before writes fail. Grow in the right order and prove with `df`/`lvs`. Next: [Linux Networking Tools](linux-networking-tools.md).

## Interview Questions

**1. Explain PV, VG, and LV in simple terms.**

??? success "Reveal answer"
    A **physical volume (PV)** is a disk/partition given to LVM. A **volume group (VG)** pools one or more PVs. A **logical volume (LV)** is a virtual disk carved from the VG that you format and mount. Applications mount the LV path, so you can grow underneath without changing the mount point name.

**2. What is the correct order to grow an ext4 filesystem on LVM after the cloud disk is enlarged?**

??? success "Reveal answer"
    Rescan/resize the PV (`pvresize`) → extend the LV (`lvextend`) → grow the filesystem (`resize2fs` for ext4, often online). Then verify with `df` and application checks. Skipping the filesystem step is a classic mistake.

**3. When is swap helpful, and when is it a problem?**

??? success "Reveal answer"
    Swap helps absorb short memory spikes and can support hibernation on some systems. Heavy sustained swapping causes severe latency. Size swap for the workload; fix memory leaks rather than “adding infinite swap”.

**4. How do you monitor disks before users notice?**

??? success "Reveal answer"
    Alert on filesystem use and inodes (`df`), VG free space (`vgs`), I/O latency/errors (`iostat`, cloud metrics), and SMART/cloud disk health. Attach runbooks that start with `df -hT`, `lsblk`, and the application mount map.

**5. Why practise LVM on loop devices in a lab?**

??? success "Reveal answer"
    Loop-backed images let you create and destroy PVs without risking the OS disk. You still use real LVM commands, which transfers to cloud data volumes safely.

**6. What happens if you `lvremove` the wrong volume?**

??? success "Reveal answer"
    Data on that LV is destroyed (unless you have backups/snapshots). Always confirm LV name, mount point, and that the volume is unmounted. Production changes need change control and backups.

**7. How does LVM relate to Kubernetes node storage?**

??? success "Reveal answer"
    Some clusters use LVM for local persistent volumes or node ephemeral layouts; others use cloud disks/CSI only. Operators still need host skills to interpret `df`/`lsblk` when a pod cannot write because the node filesystem or LV is full.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Disks, Partitions, and Filesystems](storage-disks-partitions-and-filesystems.md) *(previous)*
- [Linux Networking Tools](linux-networking-tools.md) *(next)*
- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md) *(related)*

## References

- [LVM2 documentation](https://www.sourceware.org/lvm2/) — upstream LVM  
- [`lvextend(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/lvextend.8.html) — Ubuntu man-pages  
- [`swapon(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/swapon.8.html) — swap control  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
