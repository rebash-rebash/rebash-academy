---
title: "Boot Process and Filesystem Hierarchy"
description: "Follow the Linux boot path from firmware to multi-user target and learn the Filesystem Hierarchy Standard (FHS) used on Cloud VMs."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 1 · Linux Fundamentals"
tags:
  - linux
  - boot
  - fhs
  - systemd
  - initramfs
prerequisites:
  - linux/linux-fundamentals-distributions-and-architecture
next:
  - linux/essential-linux-commands
related:
  - labs/linux-install-and-first-boot
labs:
  - labs/linux-install-and-first-boot
interview: interview/linux
comments: false
---

# Boot Process and Filesystem Hierarchy

## Overview

When a cloud virtual machine (VM) fails to come up, hangs before Secure Shell (SSH), or boots into emergency mode, you need two maps: the **boot process** (how the machine starts) and the **Filesystem Hierarchy Standard (FHS)** (where important files live under `/`).

The **boot process** is the ordered path from power-on to a usable multi-user system: firmware (BIOS or UEFI), bootloader (usually GRUB), kernel plus **initial RAM filesystem (initramfs)**, then PID 1 (**systemd**), which reaches a default **target** such as `multi-user.target`. On many cloud images, **cloud-init** runs next to apply instance metadata, SSH keys, and hostname. The **FHS** is the conventional layout of directories so packages and operators know where configuration (`/etc`), variable data (`/var`), and runtime state (`/run`) belong. In this tutorial you will inspect boot timing with `systemd-analyze`, check the default target, and verify critical FHS paths on a practice Ubuntu VM.

Wrong layout looks like an application bug: logs filling `/` instead of `/var`, or apps writing under `/tmp` that disappear after reboot. Boot failures often sit in one stage — firmware disk selection, bad `initramfs`, broken `/etc/fstab`, or a failed unit blocking the default target. In production you separate OS disk from data volumes, persist mounts correctly, and practise rescue/emergency targets before you need them at 03:00.

This is **Tutorial 2** in **Module 1: Linux Fundamentals** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have boot and FHS evidence you can attach to an incident or change ticket.

## Prerequisites

- [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md)
- A **practice Ubuntu 22.04/24.04 VM** with `systemd` and sudo
- Comfort with a normal user shell (Tutorial 1)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe the boot chain from firmware to the default systemd target
- [ ] Use `systemd-analyze` and `systemctl get-default` to inspect boot behaviour
- [ ] Locate and explain key FHS directories (`/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/run`, `/boot`)
- [ ] Check whether critical paths exist and are mounted as expected
- [ ] Capture boot and layout evidence for troubleshooting

## Architecture

Boot stages hand control from firmware to the kernel, then to systemd. After the system is up, the FHS tells you where config, binaries, and variable data live on the mounted root (and other volumes).

![Architecture diagram for Boot Process and Filesystem Hierarchy](../assets/excalidraw/linux-boot-process.svg)

## Theory

### What it is

**Boot process stages (typical systemd server):**

1. **Firmware** — BIOS/UEFI initialises hardware (or the hypervisor presents virtual firmware) and chooses a boot device.
2. **Bootloader** — GRUB (common on Ubuntu) loads the kernel and initramfs.
3. **Kernel + initramfs** — early drivers and helpers; real root is mounted; PID 1 starts.
4. **systemd** — mounts filesystems, starts units in dependency order, reaches the default **target**.
5. **cloud-init** (cloud images) — applies metadata, users, SSH keys, and first-boot jobs.

**FHS** is the agreed directory layout under `/`. You do not need to memorise every path, but you must know the landmarks operators use every day.

```bash
systemctl get-default
systemd-analyze
ls -ld /etc /var /usr /home /tmp /run /boot
```

### Why it matters

A VM that never accepts SSH may still be “booting” in firmware, stuck in initramfs, or waiting in emergency mode because `/etc/fstab` points at a missing disk. FHS mistakes cause capacity and data-loss incidents: writing state into `/tmp`, filling `/` with logs, or putting application data on the small OS disk. Cloud volumes must be mounted at the right path and listed so they return after reboot.

### How it works

Firmware hands off to the bootloader. The bootloader loads kernel + initramfs. The kernel starts systemd. systemd reads units, mounts from `fstab` or `.mount` units, and enters the default target (`multi-user.target` on most servers; `graphical.target` on desktops). **Rescue** and **emergency** targets start fewer services so you can repair. Inspect timing with `systemd-analyze blame` and `systemd-analyze critical-chain`. Inspect mounts with `findmnt` and `/proc/mounts`.

```bash
systemd-analyze blame | head
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS /
ls /lib/systemd/system/multi-user.target
```

### Key concepts and comparisons

| Stage | Role | What breaks |
|-------|------|-------------|
| Firmware | Boot device selection | Wrong disk, Secure Boot issues |
| Bootloader | Kernel + initramfs | Bad GRUB config, missing kernel |
| Kernel / initramfs | Early root, drivers | Missing module, bad root UUID |
| systemd target | Multi-user services | Failed unit, bad fstab |
| cloud-init | Instance identity | Metadata/network delay |

| Path | Purpose |
|------|---------|
| `/boot` | Kernel, initramfs, bootloader files |
| `/etc` | Host-specific configuration |
| `/usr` | Shareable system programs and libraries |
| `/var` | Variable data (logs, caches, spool) |
| `/home` | User home directories |
| `/tmp` | Temporary files (often cleared on reboot) |
| `/run` | Early runtime data (tmpfs); not for durable storage |
| `/opt` | Optional add-on application software |
| `/proc`, `/sys` | Kernel interfaces (pseudo-filesystems) |

| Target idea | Prefer when |
|-------------|-------------|
| `multi-user.target` | Headless servers, most cloud VMs |
| `graphical.target` | Desktop with GUI |
| `rescue.target` / `emergency.target` | Repair with few services |

### Common pitfalls

- Storing application data under `/tmp` and wondering why it vanished after reboot.
- Filling `/` with logs because `/var` was never on a larger volume.
- Editing `/etc/fstab` with a typo and landing in emergency mode on next boot.
- Assuming cloud data disks auto-mount without `fstab` or a mount unit.
- Confusing “SSH is down” with “boot finished” — check console and `systemd-analyze` when you regain access.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, inspect the boot path and default target, map critical FHS directories and mounts, and save evidence under `~/rebash-linux/lab02`.

### Prerequisites

- Ubuntu 22.04/24.04 with systemd
- Admin user with sudo (only where noted)
- VM console access available if you ever test rescue mode (not required for this lab)

### Lab environment

Workspace: `~/rebash-linux/lab02`

```bash
mkdir -p ~/rebash-linux/lab02 && cd ~/rebash-linux/lab02
set -euo pipefail
test -d /etc && test -d /var
systemctl get-default | tee default-target.txt
```

**Expected output:** `default-target.txt` contains a target name such as `multi-user.target` or `graphical.target`.

### Real-world scenario

A new Ubuntu VM takes a long time before SSH is ready. Platform asks you to measure boot time, list slow units, confirm the default target, and verify that OS landmarks (`/etc`, `/var`, `/boot`) exist and that `/` is mounted as expected — then attach proof to the ticket.

### Step-by-step tasks

#### Task 1 – Inspect boot and default target

```bash
cd ~/rebash-linux/lab02
set -euo pipefail

systemctl get-default | tee default-target.txt
systemctl is-system-running | tee system-state.txt || true
systemd-analyze | tee analyze.txt
systemd-analyze blame | head -n 15 | tee blame-top.txt
systemd-analyze critical-chain 2>/dev/null | tee critical-chain.txt || true

# Recent boot messages (may need privileges on some setups)
journalctl -b -o short-iso --no-pager 2>/dev/null | head -n 40 | tee journal-boot-head.txt || \
  echo 'journal-unavailable' | tee journal-boot-head.txt

grep -E 'Startup finished|multi-user|graphical' analyze.txt || test -s analyze.txt
```

**Expected output:** `analyze.txt` shows total startup time; `blame-top.txt` lists units; `default-target.txt` is non-empty.

#### Task 2 – Map FHS landmarks and root mount

```bash
cd ~/rebash-linux/lab02
set -euo pipefail

FHS_PATHS="/boot /etc /usr /var /home /tmp /run /opt /proc /sys"
for p in $FHS_PATHS; do
  if [ -e "$p" ]; then
    printf 'OK\t%s\n' "$p"
  else
    printf 'MISSING\t%s\n' "$p"
  fi
done | tee fhs-check.txt

ls -ld /boot /etc /usr /var /home /tmp /run | tee fhs-ls.txt
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS / | tee root-mount.txt
findmnt -o TARGET,SOURCE,FSTYPE | tee mounts-all.txt
df -hT / /boot /var 2>/dev/null | tee df-fhs.txt || df -hT / | tee df-fhs.txt

grep -E '^OK\t/(etc|var|usr|boot)$' fhs-check.txt
test -s root-mount.txt
```

**Expected output:** `fhs-check.txt` shows `OK` for `/etc`, `/var`, `/usr`, `/boot`; `root-mount.txt` shows `/` with a real source and filesystem type.

#### Task 3 – Link boot files to FHS and pack evidence

```bash
cd ~/rebash-linux/lab02
set -euo pipefail

ls -l /boot | head -n 30 | tee boot-listing.txt
# Kernel/initramfs names vary; prove /boot is not empty on a normal VM
test "$(find /boot -maxdepth 1 -type f 2>/dev/null | wc -l)" -ge 1 || \
  echo 'WARN: /boot has no regular files (container or special image?)' | tee boot-warn.txt

# fstab is the persistence map for mounts (read-only inspection)
sudo test -r /etc/fstab
sudo cp /etc/fstab ./fstab.copy
wc -l fstab.copy | tee fstab-lines.txt

tar -czf boot-fhs-evidence.tgz \
  default-target.txt system-state.txt analyze.txt blame-top.txt critical-chain.txt \
  journal-boot-head.txt fhs-check.txt fhs-ls.txt root-mount.txt mounts-all.txt \
  df-fhs.txt boot-listing.txt fstab.copy fstab-lines.txt \
  $(test -f boot-warn.txt && echo boot-warn.txt || true)
ls -l boot-fhs-evidence.tgz | tee evidence-ls.txt
test -s boot-fhs-evidence.tgz
```

**Expected output:** `fstab.copy` exists; `boot-fhs-evidence.tgz` is not empty; `/boot` listing is captured.

### Validation steps

- [ ] `systemctl get-default` matches `default-target.txt`
- [ ] `systemd-analyze` produced a startup summary in `analyze.txt`
- [ ] `fhs-check.txt` shows `OK` for `/etc` and `/var`
- [ ] `root-mount.txt` shows filesystem type for `/`
- [ ] `boot-fhs-evidence.tgz` exists under `~/rebash-linux/lab02`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `systemd-analyze: command not found` | Non-systemd environment | Use a full Ubuntu VM, not a tiny container without systemd |
| `Permission denied` reading journal | User not in `adm`/`systemd-journal` | Use `sudo journalctl -b …` or skip journal head |
| Empty `/boot` listing | Container or unusual image | Note it; FHS checks on `/etc` and `/var` still matter |
| `findmnt` missing | Minimal image | Install `util-linux` or use `mount \| head` |

### Challenge exercise

Create an executable script `~/rebash-linux/lab02/fhs-audit.sh` that checks these paths exist: `/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/run`, `/boot`. Print `OK` or `MISSING` per path, exit `1` if any required path is missing, and write the report to `fhs-audit-out.txt`. That script is your stretch artefact (not a markdown runbook).

### Learning outcomes

- Measured boot with `systemd-analyze` and recorded the default target
- Verified FHS landmarks and the root mount
- Linked `/boot` and `/etc/fstab` to real boot/mount behaviour
- Packed evidence for a ticket

### Cleanup

```bash
cd ~/rebash-linux/lab02
# Keep boot-fhs-evidence.tgz and fhs-audit.sh if you created them.
# rm -f *.txt fstab.copy boot-fhs-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab02/` with evidence files
- [ ] You can list boot stages from firmware to default target
- [ ] You can explain why `/etc`, `/var`, `/tmp`, and `/run` are different
- [ ] You know that a bad `fstab` entry can block a normal boot

## Code Walkthrough

In real incidents, **boot and FHS** checks usually follow this order:

1. **Can you reach the console?** — cloud serial console if SSH is down  
2. **Has systemd finished?** — `systemctl is-system-running`, `systemd-analyze`  
3. **What is slow or failed?** — `systemd-analyze blame`, `systemctl --failed`  
4. **Are disks mounted?** — `findmnt`, `df -hT`, read `/etc/fstab`  
5. **Is data on the right volume?** — confirm `/var` and app paths are not silently filling `/`  

Practise these on a healthy lab VM so the path is familiar under pressure.

## Security Considerations

- Limit who can edit `/etc/fstab` and bootloader config — mistakes cause outages  
- Protect `/boot` and bootloader passwords in environments that require them  
- Do not store secrets under world-readable FHS paths  
- Treat cloud-init and instance metadata as sensitive (SSH keys, user-data)  
- Use rescue access procedures that are audited and rarely needed  

## Common Mistakes

!!! warning "Putting durable data in `/tmp` or `/run`"
    These locations are temporary. **Fix:** use `/var` or a dedicated data mount for anything that must survive reboot.

!!! warning "Growing logs on the OS root disk"
    `/var/log` can fill `/` and break the host. **Fix:** separate volume for `/var` when needed; enable logrotate; alert on `df`.

!!! warning "Hand-editing fstab without a test plan"
    A bad UUID sends the next boot to emergency mode. **Fix:** use UUIDs, keep a console path ready, test on a snapshot VM.

!!! warning "Ignoring cloud-init when SSH keys are wrong"
    First-boot identity comes from metadata. **Fix:** check cloud-init status/logs after instance launch.

## Best Practices

- Prefer UUID (or LABEL) in `fstab`, not unstable device names like `/dev/sdb1`  
- Separate OS and data disks on cloud VMs  
- Keep `multi-user.target` as default on servers unless you need a GUI  
- Record `systemd-analyze` before/after large image changes  
- Document rescue/emergency login steps for your cloud provider  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Emergency mode on boot | Bad `fstab` / missing device | Console: remount `/` rw; fix or comment the line; `systemctl default` |
| Very slow boot | Slow unit or network wait | `systemd-analyze blame` / `critical-chain`; fix unit deps |
| SSH never ready | Service failed / cloud-init stuck | Console + `systemctl --failed` + cloud-init logs |
| `/tmp` empty after reboot | Expected for tmpfs/cleanup | Store durable files elsewhere |
| `/` full, `/home` fine | Logs or data on root | `du` under `/var`; move mounts; clean safely |

## Summary

Boot is a chain from firmware to the default systemd target; FHS tells you where config and data should live. Measure with `systemd-analyze`, verify mounts and landmarks, and keep evidence. Next, practise everyday file commands in [Essential Linux Commands](essential-linux-commands.md).

## Interview Questions

**1. List the main stages of a typical Linux server boot with systemd.**

??? success "Reveal answer"
    Firmware (BIOS/UEFI) → bootloader (for example GRUB) → kernel + initramfs → systemd (PID 1) → default target such as `multi-user.target`. On cloud images, cloud-init often runs to apply metadata and SSH keys. Interviewers want the order and what each stage is responsible for.

**2. What is the difference between `rescue.target` and a normal `multi-user.target`?**

??? success "Reveal answer"
    **`multi-user.target`** is the usual multi-user, non-graphical server state with networking and services. **`rescue.target`** (and the tighter **emergency** mode) starts far fewer services so you can repair disks, `fstab`, or critical config. You use rescue/emergency when a normal boot cannot finish cleanly.

**3. Why must operators care about the Filesystem Hierarchy Standard (FHS)?**

??? success "Reveal answer"
    FHS gives predictable locations: config in `/etc`, variable data in `/var`, temporary files in `/tmp`, runtime in `/run`. Apps and packages assume this layout. Putting durable data in `/tmp` or filling `/` with logs causes outages that look like “mystery application failures”.

**4. A VM boots to emergency mode after you added a data disk. What do you check first?**

??? success "Reveal answer"
    Check **`/etc/fstab`** for a wrong UUID, missing `nofail`/`x-systemd.device-timeout` where appropriate, or a device that is not attached. Use the serial console, remount root read-write if needed, fix or comment the bad line, then continue boot. Prefer UUID over `/dev/sdX` names.

**5. How do you find which systemd units slowed down the last boot?**

??? success "Reveal answer"
    Run **`systemd-analyze`** for the total time, **`systemd-analyze blame`** for per-unit time, and **`systemd-analyze critical-chain`** for the chain that blocked reaching the default target. That trio is the standard interview answer for boot performance.

**6. What belongs in `/run` versus `/var`, and what happens if you confuse them?**

??? success "Reveal answer"
    **`/run`** is early runtime state (often tmpfs) and does not survive reboot. **`/var`** holds variable data such as logs, caches, and spool files that must persist. Storing durable state in `/run` loses data on reboot; stuffing huge durable trees into the wrong place also fills the wrong filesystem.

**7. How does cloud-init fit into the boot story on a new cloud VM?**

??? success "Reveal answer"
    After the OS reaches a networked multi-user state, **cloud-init** applies instance user-data and metadata: hostname, users, SSH authorised keys, and optional packages or scripts. If SSH keys are missing or first boot hangs, check cloud-init status and logs, not only `sshd` alone.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md) *(previous)*
- [Essential Linux Commands](essential-linux-commands.md) *(next)*
- [Lab — Install and First Boot](../labs/linux-install-and-first-boot.md) *(more practice)*

## References

- [systemd bootup documentation](https://www.freedesktop.org/software/systemd/man/latest/bootup.html) — boot logic  
- [`systemd-analyze(1)`](https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html) — boot analysis  
- [Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html) — directory layout  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
