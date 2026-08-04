---
title: "Boot Process and Filesystem Hierarchy"
description: "Boot firmware to systemd target, FHS landmarks, and a real boot-timing lab on a practice Ubuntu VM."
difficulty: beginner
estimated_time: "50–65 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 1 · Linux Fundamentals"
career_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - boot
  - fhs
  - systemd
  - initramfs
  - beginners
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

Two maps make Linux feel less mysterious early on:

1. **How a Linux machine starts** (the boot process)
2. **Where important files live** (the **Filesystem Hierarchy Standard**, or **FHS**)

When a cloud virtual machine (VM) will not accept Secure Shell (SSH), hangs at a black screen, or boots into **emergency mode**, operators ask: *Which stage failed?* When an app “mysteriously” loses data after reboot, they ask: *Was it stored under `/tmp` instead of `/var`?*

This tutorial answers, in order:

1. What happens from power-on to a usable system?
2. What is **systemd**, a **target**, and **initramfs**?
3. What are the FHS directories you must recognise (`/etc`, `/var`, `/boot`, …)?
4. How do you **measure** boot time and **prove** layout on a real VM?

This is **Tutorial 2** in **Module 1: Linux Fundamentals** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md) — you can identify your distro and kernel
- A **practice Ubuntu 22.04/24.04 VM** (local, cloud Free Tier, or Windows Subsystem for Linux (WSL2) with systemd)
- A normal user account; use `sudo` only when the lab says so

You do **not** need networking, Docker, or storage expertise yet.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the boot chain from firmware to the default systemd target in plain English
- [ ] Use `systemd-analyze` and `systemctl get-default` on a real host
- [ ] Name and explain key FHS directories (`/etc`, `/var`, `/usr`, `/home`, `/tmp`, `/run`, `/boot`)
- [ ] Check mounts with `findmnt` and explain why a bad `/etc/fstab` line can block boot
- [ ] Capture boot and FHS evidence you could attach to a ticket or discuss in an interview

## Architecture

Boot is a relay race: firmware hands to the bootloader, the bootloader loads the kernel, the kernel starts **systemd** (PID 1), and systemd reaches a **target** such as `multi-user.target`. After the system is up, the **FHS** tells you where configuration, programs, and variable data should live.

![Linux boot process — firmware, bootloader, kernel, systemd, target](../assets/excalidraw/linux-boot-process.svg)

## Theory

### The problem (before any jargon)

Day one on a team: you SSH to a new Ubuntu VM. It never answers. A senior engineer asks on the ticket: *“Did it finish boot? What target? How long did systemd take?”* You have no idea where to look.

Separately, a junior stores application logs under `/tmp` because “it is easy to find.” After reboot, the logs are gone. That is not an application bug — it is an **FHS** mistake.

This section gives you vocabulary and commands so those questions have clear answers.

### Boot process — simple words

**Analogy:** Booting a server is like opening a shop:

| Stage | Shop analogy | Linux term |
|-------|--------------|------------|
| Unlock the building | Power and hardware check | **Firmware** (BIOS/UEFI) |
| Turn on lights and open the front door | Load the OS loader | **Bootloader** (often GRUB) |
| Staff arrive with keys for the stockroom | Early drivers + temporary root | **Kernel + initramfs** |
| Manager opens departments in order | Start services | **systemd** |
| Shop open for customers | Normal multi-user server | **Default target** (`multi-user.target`) |
| Head office sends price tags for this branch | Cloud metadata, SSH keys | **cloud-init** (cloud images) |

| Term | Plain meaning |
|------|----------------|
| **Firmware** | Built-in software that starts hardware and picks a boot disk |
| **Bootloader** | Program that loads the kernel (GRUB is common on Ubuntu) |
| **Kernel** | Core OS that manages CPU, memory, disks, network |
| **initramfs** | Temporary early filesystem with drivers/helpers before the real root mounts |
| **systemd** | PID 1 — starts units (services, mounts) in dependency order |
| **Target** | Named boot state (like “multi-user mode ready”) |
| **cloud-init** | First-boot tool on cloud VMs — users, keys, hostname from metadata |

**What you can say in an interview:** “Boot is firmware → bootloader → kernel/initramfs → systemd → default target. On cloud VMs, cloud-init often runs after the OS is up to apply SSH keys and hostname.”

**Tiny example — inspect boot state:**

``` {.bash .ra-terminal title="Terminal"}
systemctl get-default
systemd-analyze
systemctl is-system-running
```

### How systemd fits in

**Analogy:** systemd is the **building manager**. It does not do every job itself; it opens departments (mount disks, start networking, start `sshd`) in the right order.

| Target | Plain meaning | Typical use |
|--------|---------------|-------------|
| `multi-user.target` | Multi-user, no graphical desktop | Most cloud servers |
| `graphical.target` | Desktop with GUI | Laptops |
| `rescue.target` | Minimal services for repair | Broken config, disk repair |
| `emergency.target` | Even fewer services | Last-resort shell |

**Tiny example — find slow units:**

``` {.bash .ra-terminal title="Terminal"}
systemd-analyze blame | head
systemd-analyze critical-chain
```

**What you can say in an interview:** “If SSH is down, I check whether boot finished (`systemctl is-system-running`), then `systemd-analyze blame` for slow or failed units, and the serial console if I cannot SSH at all.”

### Filesystem Hierarchy Standard (FHS)

**Analogy:** The FHS is the **floor plan** of a building. Every shop knows: electrical panel here, stockroom there, customer area there. Linux packages and operators expect the same predictable paths.

![FHS — standard directory layout under /](../assets/excalidraw/linux-filesystem-hierarchy.svg)

| Path | Plain purpose | Common mistake to avoid |
|------|---------------|---------------------------|
| `/boot` | Kernel, initramfs, bootloader files | Editing here without knowing what you remove |
| `/etc` | Host-specific **configuration** | Treating it like a trash folder |
| `/usr` | Programs and libraries (shareable read-only tree) | Putting your app’s live data here |
| `/var` | **Variable** data — logs, caches, spool | Ignoring log growth until disk full |
| `/home` | Personal user files | Storing service data here on servers |
| `/tmp` | Temporary files — often cleared on reboot | Storing anything that must survive reboot |
| `/run` | Early runtime state (often tmpfs) | Same mistake as `/tmp` — not durable |
| `/opt` | Optional third-party software | Fine for vendor apps, not default OS layout |
| `/proc`, `/sys` | Kernel interfaces (not real disk files) | Trying to “delete” them like normal files |

**What you can say in an interview:** “Config lives in `/etc`, logs and variable state in `/var`, temporary scratch in `/tmp`. If data must survive reboot, it does not belong in `/tmp` or `/run`.”

**Tiny example — check landmarks:**

``` {.bash .ra-terminal title="Terminal"}
ls -ld /etc /var /usr /home /tmp /run /boot
findmnt -o TARGET,SOURCE,FSTYPE /
```

### Why Cloud / DevOps teams care

- A VM that “never boots” is often a bad **`/etc/fstab`** line (missing cloud disk) or a failed systemd unit — not “the app”.
- Logs under `/var/log` can fill the OS disk; separating `/var` onto a larger volume is common on production hosts.
- **`cloud-init`** applies SSH keys on first boot — if keys are wrong, check cloud-init before reinstalling the whole OS.
- Rescue/emergency targets exist so you can fix disk layout **before** declaring the machine dead.

### Common pitfalls

- Storing durable files in `/tmp` or `/run` and losing them after reboot
- Checking only “is SSH up?” without knowing if systemd finished boot
- Editing `/etc/fstab` with a wrong UUID and landing in emergency mode on next reboot
- Assuming a cloud data disk auto-mounts without an `fstab` entry or mount unit
- Confusing “slow SSH” with “slow boot” — measure with `systemd-analyze`

## Hands-on Lab

### Objective

On a practice Ubuntu VM, measure boot timing, record the default target, verify FHS landmarks and mounts, and save evidence under `~/rebash-linux/lab02` — the same proof a mentor would ask for on day one.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu 22.04/24.04 with systemd | Not a tiny container without PID 1 |
| Terminal access | Local, SSH, or WSL2 |
| Optional console | Cloud serial console if you ever test rescue mode (not required here) |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab02 && cd ~/rebash-linux/lab02
set -euo pipefail
test -d /etc && test -d /var
systemctl get-default | tee default-target.txt
```

!!! example "Expected output"
    `default-target.txt` contains a name such as `multi-user.target` or `graphical.target`.


### Real-world scenario

Platform ticket: *“New Ubuntu VM — SSH took two minutes. Confirm boot target, list slow units, prove `/etc` and `/var` exist, show how `/` is mounted.”* You gather command output and attach it — no guessing.

### Step-by-step tasks

#### Task 1 – Measure boot and default target

You are proving **boot behaviour**, not just copying random files.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab02
set -euo pipefail

systemctl get-default | tee default-target.txt
systemctl is-system-running | tee system-state.txt || true
systemd-analyze | tee analyze.txt
systemd-analyze blame | head -n 15 | tee blame-top.txt
systemd-analyze critical-chain 2>/dev/null | tee critical-chain.txt || true

journalctl -b -o short-iso --no-pager 2>/dev/null | head -n 30 | tee journal-boot-head.txt || \
  echo 'journal-unavailable' | tee journal-boot-head.txt

grep -E 'Startup finished|multi-user|graphical' analyze.txt || test -s analyze.txt
wc -l blame-top.txt | tee blame-lines.txt
```

!!! example "Expected output"
    `analyze.txt` shows total startup time (for example `Startup finished in …`). `blame-top.txt` lists unit names with times. `default-target.txt` is non-empty.


#### Task 2 – Verify FHS landmarks and root mount

Map the **floor plan** — which paths exist and how `/` is mounted.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab02
set -euo pipefail

FHS_PATHS="/boot /etc /usr /var /home /tmp /run /opt"
for p in $FHS_PATHS; do
  if [ -e "$p" ]; then
    printf 'OK\t%s\n' "$p"
  else
    printf 'MISSING\t%s\n' "$p"
  fi
done | tee fhs-check.txt

ls -ld /boot /etc /usr /var /home /tmp /run | tee fhs-ls.txt
findmnt -o TARGET,SOURCE,FSTYPE,OPTIONS / | tee root-mount.txt
df -hT / /var /boot 2>/dev/null | tee df-fhs.txt || df -hT / | tee df-fhs.txt

grep -E '^OK\t/(etc|var|usr|boot)$' fhs-check.txt
test -s root-mount.txt
```

!!! example "Expected output"
    `fhs-check.txt` shows `OK` for `/etc`, `/var`, `/usr`, `/boot`. `root-mount.txt` shows filesystem type and source for `/`.


#### Task 3 – Connect `/boot` and `fstab` to persistence

Link boot files to FHS and show how mounts survive reboot (read-only inspection).

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab02
set -euo pipefail

ls -l /boot | head -n 20 | tee boot-listing.txt
test "$(find /boot -maxdepth 1 -type f 2>/dev/null | wc -l)" -ge 1 || \
  echo 'WARN: /boot empty — note container or special image' | tee boot-warn.txt

sudo test -r /etc/fstab
sudo cp /etc/fstab ./fstab.copy
grep -v '^#' fstab.copy | grep -v '^$' | tee fstab-active-lines.txt

tar -czf boot-fhs-evidence.tgz \
  default-target.txt system-state.txt analyze.txt blame-top.txt critical-chain.txt \
  journal-boot-head.txt fhs-check.txt fhs-ls.txt root-mount.txt df-fhs.txt \
  boot-listing.txt fstab.copy fstab-active-lines.txt \
  $(test -f boot-warn.txt && echo boot-warn.txt || true)
ls -l boot-fhs-evidence.tgz | tee evidence-ls.txt
test -s boot-fhs-evidence.tgz
```

!!! example "Expected output"
    `boot-listing.txt` shows kernel/initramfs-related files on a normal VM. `fstab.copy` exists. `boot-fhs-evidence.tgz` is not empty.


### Validation steps

- [ ] You can explain boot stages without reading notes
- [ ] `systemd-analyze` output is saved in `analyze.txt`
- [ ] FHS check shows `OK` for `/etc` and `/var`
- [ ] `root-mount.txt` shows how `/` is mounted
- [ ] `boot-fhs-evidence.tgz` exists under `~/rebash-linux/lab02`

### Common errors and fixes

| Error | Meaning | Fix |
|-------|---------|-----|
| `systemd-analyze: command not found` | Non-systemd environment | Use a full Ubuntu VM, not a minimal container |
| `Permission denied` on journal | User not in `adm` group | `sudo journalctl -b …` or skip journal head |
| Empty `/boot` listing | Container or unusual image | Note in ticket; FHS checks on `/etc`/`/var` still matter |
| `findmnt` missing | Minimal image | Install `util-linux` or use `mount \| head` |

### Challenge exercise

Create `fhs-audit.sh`:

```bash title="fhs-audit.sh"
#!/usr/bin/env bash
set -euo pipefail
REQUIRED="/etc /var /usr /home /tmp /run /boot"
FAIL=0
for p in $REQUIRED; do
  if [ -e "$p" ]; then
    echo "OK  $p"
  else
    echo "MISSING  $p"
    FAIL=1
  fi
done
exit "$FAIL"
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab02
chmod +x fhs-audit.sh
./fhs-audit.sh | tee fhs-audit-out.txt
test "$(tail -1 fhs-audit-out.txt | grep -c MISSING || true)" -eq 0
```

!!! example "Expected output"
    Every required path prints `OK`. Script exits `0`.


### Learning outcomes

- Measured boot with `systemd-analyze` like an on-call engineer
- Verified FHS landmarks and root mount
- Linked `/boot` and `/etc/fstab` to real boot and persistence behaviour
- Saved ticket-ready evidence

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab02
# Keep boot-fhs-evidence.tgz and fhs-audit.sh for revision.
# rm -f *.txt fstab.copy boot-fhs-evidence.tgz
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab02`
- [ ] Can teach boot stages and FHS `/etc` vs `/var` vs `/tmp` to a classmate
- [ ] Ready for everyday file commands in the next tutorial

## Code Walkthrough

1. **`systemctl get-default` first** — know the intended end state before chasing services.
2. **`systemd-analyze blame`** — find slow units; do not guess “network is slow”.
3. **`findmnt` on `/`** — confirm you are on the filesystem you think you are.
4. **FHS landmarks** — `/etc` for config, `/var` for logs, never durable data in `/tmp`.
5. **Read `fstab` before adding disks** — wrong UUID → emergency mode on next boot.

## Security Considerations

- Limit who can edit `/etc/fstab` and bootloader configuration — mistakes cause outages
- Do not store secrets in world-readable paths under `/tmp` or `/var/tmp`
- Treat cloud-init user-data as sensitive (may contain SSH keys or scripts)
- Know your cloud provider’s rescue/serial console before you need it at 03:00
- Protect `/boot` on hosts where Secure Boot or bootloader passwords matter

## Common Mistakes

!!! warning "Durable data in `/tmp` or `/run`"
    These locations are temporary. **Fix:** use `/var` or a dedicated data mount for anything that must survive reboot.

!!! warning "Editing `/etc/fstab` without a console backup plan"
    One bad line → emergency mode on next boot. **Fix:** use UUIDs, test on a snapshot VM, keep serial console access.

!!! warning "Blaming the application when boot never finished"
    SSH timeout may mean systemd never reached multi-user. **Fix:** check console, `systemctl is-system-running`, `systemctl --failed`.

!!! warning "Ignoring cloud-init on first boot"
    Missing SSH keys often come from metadata, not “broken SSH”. **Fix:** check cloud-init status and logs after launch.

## Best Practices

- Record `systemd-analyze` before and after image or package changes
- Prefer UUID (or LABEL) in `fstab`, not unstable `/dev/sdX` names
- Separate OS disk from data volumes on cloud VMs
- Keep `multi-user.target` as default on headless servers
- Document rescue/emergency login steps for your cloud provider

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Emergency mode on boot | Bad `fstab` / missing disk | Console: fix or comment bad line; `systemctl default` |
| Very slow boot | Slow unit or network wait | `systemd-analyze blame`; fix dependencies |
| SSH never ready | Failed unit or cloud-init stuck | Console + `systemctl --failed` + cloud-init logs |
| `/tmp` empty after reboot | Expected behaviour | Store durable files in `/var` or a data mount |
| `/` full, `/home` fine | Logs or data on root disk | `du` under `/var`; move mounts; rotate logs |

## Summary

**Boot** is a chain from firmware to systemd’s default **target**. The **FHS** tells you where config (`/etc`), variable data (`/var`), and temporary scratch (`/tmp`) belong. Measure with `systemd-analyze`, verify mounts with `findmnt`, and keep evidence before you change disks or `fstab`. Next: [Essential Linux Commands](essential-linux-commands.md).

## Interview Questions

**1. List the main stages of a typical Linux server boot with systemd.**

??? success "Reveal answer"
    **Firmware** (BIOS/UEFI) → **bootloader** (for example GRUB) → **kernel + initramfs** → **systemd** (PID 1) → **default target** such as `multi-user.target`. On cloud images, **cloud-init** often runs afterward to apply metadata and SSH keys. Interviewers want the order and one sentence per stage.

**2. What is the difference between `rescue.target` and `multi-user.target`?**

??? success "Reveal answer"
    **`multi-user.target`** is normal server mode — networking and services running. **`rescue.target`** starts far fewer services so you can repair disks, `fstab`, or broken config. Use rescue when a normal boot cannot finish.

**3. Why must operators care about the Filesystem Hierarchy Standard (FHS)?**

??? success "Reveal answer"
    FHS gives predictable locations: configuration in **`/etc`**, variable data in **`/var`**, temporary files in **`/tmp`**, runtime state in **`/run`**. Putting durable data in `/tmp` or filling `/` with logs causes outages that look like application bugs.

**4. A VM boots to emergency mode after you added a data disk. What do you check first?**

??? success "Reveal answer"
    Check **`/etc/fstab`** for a wrong UUID, a missing device, or a line without `nofail` where appropriate. Use the serial console, remount root read-write if needed, fix or comment the bad line, then continue boot. Prefer UUID over `/dev/sdX` device names.

**5. How do you find which systemd units slowed the last boot?**

??? success "Reveal answer"
    Run **`systemd-analyze`** for total time, **`systemd-analyze blame`** for per-unit time, and **`systemd-analyze critical-chain`** for the chain that blocked reaching the default target.

**6. What belongs in `/run` versus `/var`?**

??? success "Reveal answer"
    **`/run`** holds early runtime state (often tmpfs) and does **not** survive reboot. **`/var`** holds logs, caches, and spool files that **must** persist. Confusing them loses data or fills the wrong filesystem.

**7. How does cloud-init fit into boot on a new cloud VM?**

??? success "Reveal answer"
    After the OS reaches a networked multi-user state, **cloud-init** reads instance metadata and user-data to set hostname, users, SSH authorised keys, and optional packages or scripts. If SSH keys are missing on first boot, check cloud-init before blaming `sshd` alone.

## Related Tutorials

- Previous: [Linux Fundamentals — Distributions and Architecture](linux-fundamentals-distributions-and-architecture.md)
- Next: [Essential Linux Commands](essential-linux-commands.md)
- Standalone lab: [Linux install and first boot](../labs/linux-install-and-first-boot.md)

## References

- [systemd bootup documentation](https://www.freedesktop.org/software/systemd/man/latest/bootup.html)
- [`systemd-analyze(1)`](https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html)
- [Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
