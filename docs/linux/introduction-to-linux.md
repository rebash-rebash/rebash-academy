---
title: Introduction to Linux
description: Understand Linux history, kernel vs distribution architecture, the boot process, and why Linux dominates DevOps and cloud infrastructure.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: linux
tags:
  - linux
  - fundamentals
  - kernel
  - boot-process
  - devops
prerequisites:
  - Basic computer literacy (files, folders, and using a keyboard)
  - Access to a Linux system (local VM, WSL, cloud instance, or lab environment)
comments: false
---

# Introduction to Linux

## Overview

Linux powers the majority of the world's servers, cloud instances, and container workloads. From AWS EC2 and Google Cloud VMs to Kubernetes nodes and CI/CD runners, Linux is the default operating system for production infrastructure. Understanding how Linux is structured — and why it became the backbone of modern DevOps — is the first skill every platform engineer, SRE, and cloud administrator must master.

This tutorial takes you from "I've heard of Linux" to a working mental model: what the **kernel** does versus what a **distribution** adds, how a machine boots from power-on to a login shell, and how to identify the system you're working on. These concepts appear in every interview, every incident postmortem, and every architecture diagram you'll encounter in your career.

This is **Tutorial 1** in **Module 1: Foundations** of the REBASH Academy Linux series. It follows our [documentation standards](../about.md#documentation-standards) with theory, hands-on labs, and interview preparation.

## Prerequisites

- Basic computer literacy (understanding files, directories, and keyboard input)
- A Linux environment: Ubuntu VM, WSL2, macOS Terminal with SSH to a Linux host, or a free-tier cloud instance (AWS, GCP, Azure)
- Network access to install packages if needed (`sudo apt update` on Debian/Ubuntu systems)
- No prior Linux experience required — this tutorial starts from zero

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between the Linux kernel, GNU utilities, and a Linux distribution
- [ ] Describe the Linux boot sequence from firmware through init (systemd) to user login
- [ ] Identify your distribution, kernel version, and hardware architecture using CLI tools
- [ ] Articulate why Linux dominates cloud, containers, and DevOps tooling
- [ ] Locate key system directories and understand their role at a high level
- [ ] Analyze boot performance using `systemd-analyze` on systemd-based systems

## Architecture Diagram

The diagram below shows how hardware, firmware, the kernel, userspace, and your applications relate. Every layer has a distinct responsibility — confusing them is a common source of beginner mistakes.

```d2
direction: down

HW: "Hardware Layer" {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        CPU: "CPU / RAM / Disk / NIC"
    }
    FW: Firmware {
      style: {
        fill: "#e8f5e9"
        stroke: "#388e3c"
      }
        UEFI: "UEFI / BIOS"
    }
    BL: Bootloader {
      style: {
        fill: "#fff3e0"
        stroke: "#ef6c00"
      }
        GRUB: "GRUB / systemd-boot"
    }
    KS: "Kernel Space" {
      style: {
        fill: "#f3e5f5"
        stroke: "#7b1fa2"
      }
        KERN: "Linux Kernel\\nscheduling · memory · drivers · syscalls"
    }
    US: "User Space" {
      style: {
        fill: "#fce4ec"
        stroke: "#c2185b"
      }
        INIT: "PID 1 — systemd / init"
        SVC: "systemd units\\nsshd · nginx · docker"
        SHELL: "Login shell\\nbash · zsh"
        APP: "User applications\\ngit · python · kubectl"
    }
    HW.CPU -> FW.UEFI
    FW.UEFI -> BL.GRUB
    BL.GRUB -> KS.KERN
    KS.KERN -> US.INIT
    US.INIT -> US.SVC
    US.INIT -> US.SHELL
    US.SHELL -> US.APP
    US.SVC -> US.APP
    US.APP -> KS.KERN: syscalls
    KS.KERN -> HW.CPU
```

## Theory

### A Brief History: From Unix to Linux

Modern Linux traces its lineage to **Unix**, developed at AT&T Bell Labs in the late 1960s. Unix introduced ideas that still define computing today: everything is a file, small composable programs, and a hierarchical filesystem. In 1983, Richard Stallman launched the **GNU Project** to build a free, Unix-compatible operating system — compilers, shell, core utilities — but GNU lacked a production-ready kernel for many years.

In **1991**, Linus Torvalds, a Finnish computer science student, released the **Linux kernel** as a hobby project on the comp.os.minix newsgroup. Combined with GNU tools, it formed a complete free operating system. Today the Linux Foundation coordinates development; thousands of contributors submit patches every release cycle. Major companies — Red Hat (IBM), Google, Meta, Intel — employ kernel developers because their products depend on Linux at scale.

### Kernel vs Distribution: Know the Difference

The **Linux kernel** is the core program that talks directly to hardware. It handles process scheduling, memory management, device drivers, networking stacks, and the system call interface that applications use to request services. When you run `uname -r`, you see the kernel version (e.g., `6.8.0-45-generic`).

A **Linux distribution** (distro) packages the kernel with:

- **GNU core utilities** — `ls`, `cp`, `grep`, `bash`
- A **package manager** — `apt` (Debian/Ubuntu), `dnf` (Fedora/RHEL), `pacman` (Arch)
- **Init system** — almost always **systemd** on modern server distros
- Default configurations, security policies, and supported software versions

| Component | Example | Analogy |
|-----------|---------|---------|
| Kernel | `6.8.0-45-generic` | Engine of a car |
| Distro | Ubuntu 24.04 LTS | Complete car (engine + body + dashboard) |
| Package manager | `apt`, `dnf` | Dealership parts and upgrade system |
| Init system | systemd | Ignition sequence that starts all subsystems |

Two servers can run the **same kernel** but behave differently because they use different distros. In production, teams standardize on one or two distros (commonly **Ubuntu LTS** or **RHEL/Rocky/Alma**) to simplify patching, automation, and support contracts.

### Open Source and the GPL

Linux is released under the **GNU General Public License (GPL v2)**. The kernel source is publicly available at [kernel.org](https://www.kernel.org/). Distros add their own licenses for bundled software. For DevOps engineers, open source means you can inspect, modify, and redistribute code — and more practically, it means extensive community documentation, no per-seat licensing for servers, and vendor-neutral skills that transfer across AWS, GCP, Azure, and on-premises data centers.

### The Boot Process in Detail

When you power on a Linux server, a sequence of stages executes before you see a login prompt:

1. **Firmware (UEFI/BIOS)** — Performs POST (Power-On Self-Test), initializes hardware, and reads the boot order from NVRAM.
2. **Bootloader (GRUB)** — Loads the kernel image and initial RAM disk (initramfs) from `/boot`. GRUB presents a menu if multiple kernels are installed.
3. **Kernel initialization** — Mounts the root filesystem (initially via initramfs), loads drivers, starts the first userspace process.
4. **Init system (systemd, PID 1)** — Reads unit files from `/etc/systemd/system/` and `/usr/lib/systemd/system/`, starts targets (analogous to runlevels), brings up networking, mounts filesystems, and launches services.
5. **Login / getty** — Spawns login prompts on consoles and starts `sshd` for remote SSH access.
6. **User shell** — After authentication, your shell (`bash`) reads `/etc/profile` and `~/.bashrc`, then presents a prompt.

On cloud VMs, steps 1–2 are often abstracted by the hypervisor, but stages 3–6 behave identically. Understanding boot order helps when a server hangs at "Loading initial ramdisk" or a service fails because a filesystem isn't mounted yet.

### Why Linux Dominates DevOps and Cloud

Several factors make Linux the default for infrastructure:

- **Cost and licensing** — No per-core Windows Server licensing on thousands of cloud instances
- **Stability and uptime** — Designed for long-running server workloads; kernel hot-patching exists on enterprise distros
- **Automation-friendly** — Everything configurable via text files in `/etc`; perfect for Ansible, Terraform, and GitOps
- **Container native** — Docker and Kubernetes run Linux containers using kernel features (namespaces, cgroups)
- **Cloud default** — AWS Amazon Linux, GCP Container-Optimized OS, Azure Linux — all Linux-based
- **Tooling ecosystem** — `systemd`, `journalctl`, `iptables`/`nftables`, `ss`, `strace` — the debugging toolkit assumes Linux

If you learn Linux deeply, you learn the substrate that Docker, Kubernetes, Terraform providers, and CI runners all assume.

## Hands-on Lab

Complete these steps on any Linux system. Commands are safe to run without `sudo` unless noted.

### Step 1 – Confirm you are on Linux and identify the distribution

**Command:**

```bash
uname -s
cat /etc/os-release
```

**Explanation:** `uname -s` prints the kernel name (`Linux`). `/etc/os-release` is a standardized file every major distro ships; it contains the human-readable name, version, and ID used by configuration management tools.

**Expected output:**

```text
Linux
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
ID=ubuntu
ID_LIKE=debian
...
```

Your version string will differ — that is normal. Note whether you are on a Debian-family (`ID_LIKE=debian`) or RHEL-family (`ID_LIKE=rhel`) system.

### Step 2 – Inspect kernel version and CPU architecture

**Command:**

```bash
uname -r
uname -m
```

**Explanation:** `-r` shows the running kernel release; `-m` shows machine hardware name (`x86_64` for 64-bit Intel/AMD, `aarch64` for ARM64 — common on AWS Graviton and Apple Silicon VMs).

**Expected output:**

```text
6.8.0-45-generic
x86_64
```

### Step 3 – Get a consolidated system summary with hostnamectl

**Command:**

```bash
hostnamectl
```

**Explanation:** `hostnamectl` queries systemd-hostnamed and returns static, pretty, and transient hostname plus OS, kernel, and virtualization details in one view.

**Expected output:**

```text
 Static hostname: ip-172-31-10-42
       Icon name: computer-vm
         Chassis: vm
      Machine ID: a1b2c3d4e5f6...
         Boot ID: 7f8e9d0c1b2a...
  Virtualization: amazon
Operating System: Ubuntu 24.04.1 LTS
          Kernel: Linux 6.8.0-45-generic
    Architecture: x86-64
```

### Step 4 – Analyze boot time (systemd systems)

**Command:**

```bash
systemd-analyze
systemd-analyze blame | head -10
```

**Explanation:** The first command shows total boot time split between firmware, loader, kernel, and userspace. The second ranks systemd units by startup duration — useful when a server feels slow after reboot.

**Expected output:**

```text
Startup finished in 3.512s (firmware) + 1.234s (loader) + 2.891s (kernel) + 8.456s (userspace) = 16.093s
graphical.target reached after 8.401s in userspace.

    2.341s NetworkManager-wait-online.service
    1.892s dev-sda1.device
    1.104s systemd-udev-settle.service
    ...
```

If `systemd-analyze` is not found, your system may use a different init (rare on modern distros) — note this for your environment documentation.

### Step 5 – Explore the root filesystem layout

**Command:**

```bash
ls -la /
```

**Explanation:** The root directory `/` is the top of the entire filesystem tree. Each subdirectory has a defined purpose under the Filesystem Hierarchy Standard (FHS). You will study these in depth in the next tutorial.

**Expected output:**

```text
total 84
drwxr-xr-x  20 root root  4096 Jan 15 08:00 .
drwxr-xr-x  20 root root  4096 Jan 15 08:00 ..
lrwxrwxrwx   1 root root     7 Jan 15 08:00 bin -> usr/bin
drwxr-xr-x   4 root root  4096 Jan 15 08:00 boot
drwxr-xr-x  18 root root  3880 Jan 15 08:00 dev
drwxr-xr-x  95 root root  4096 Jan 15 08:00 etc
drwxr-xr-x   3 root root  4096 Jan 15 08:00 home
...
drwxr-xr-x  14 root root  4096 Jan 15 08:00 usr
drwxr-xr-x  11 root root  4096 Jan 15 08:00 var
```

### Step 6 – Verify the init system and PID 1

**Command:**

```bash
ps -p 1 -o pid,comm,args
```

**Explanation:** Process ID 1 is the first process started by the kernel after boot. On virtually all modern server distros, this is `systemd`. Confirming PID 1 tells you which service management tools apply (`systemctl`, `journalctl`).

**Expected output:**

```text
  PID COMMAND         COMMAND
    1 systemd         /sbin/init
```

### Step 7 – Check whether you are in a virtual machine or container

**Command:**

```bash
systemd-detect-virt 2>/dev/null || cat /proc/1/cgroup | head -5
```

**Explanation:** Cloud instances and local VMs run inside hypervisors. Containers share the host kernel. Knowing your environment affects debugging (e.g., `dmesg` in containers may be restricted).

**Expected output:**

```text
kvm
```

Other possible values: `amazon`, `microsoft`, `docker`, `none` (bare metal).

### Step 8 – View recent kernel messages

**Command:**

```bash
dmesg | tail -15
```

**Explanation:** The kernel ring buffer (`dmesg`) logs hardware detection, driver loading, and boot-time errors. This is often the first place to look when a NIC or disk is not recognized.

**Expected output:**

```text
[    3.456789] EXT4-fs (sda1): mounted filesystem with ordered data mode
[    3.567890] systemd[1]: systemd 255.4-1ubuntu8 running in system mode
[    4.123456] input: Power Button as /devices/LNXSYSTM:00/.../input/input0
...
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `uname -a` | All kernel and system information | `uname -a` |
| `uname -r` | Kernel release only | `uname -r` |
| `uname -m` | Machine hardware architecture | `uname -m` |
| `cat /etc/os-release` | Distribution name, version, and ID | `cat /etc/os-release` |
| `hostnamectl` | Hostname, OS, kernel, virtualization | `hostnamectl` |
| `lsb_release -a` | LSB release info (Debian/Ubuntu) | `lsb_release -a` |
| `systemd-analyze` | Boot time breakdown | `systemd-analyze` |
| `systemd-analyze blame` | Slowest systemd units at boot | `systemd-analyze blame \| head` |
| `systemd-detect-virt` | Detect VM/container/bare metal | `systemd-detect-virt` |
| `ps -p 1` | Show PID 1 (init system) | `ps -p 1 -o comm=` |
| `dmesg` | Kernel ring buffer messages | `dmesg \| tail -20` |
| `uptime` | How long system has been running | `uptime` |
| `who -b` | Last system boot time | `who -b` |
| `ls /` | List root filesystem directories | `ls -la /` |
| `cat /proc/version` | Kernel version string from procfs | `cat /proc/version` |

## Code

### System inventory script

Save this as `~/bin/linux-inventory.sh` and run after logging into any unfamiliar server. It produces a quick audit trail for tickets and runbooks.

```bash
#!/usr/bin/env bash
# linux-inventory.sh — gather essential system identity for documentation
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Identity"
echo "Hostname:  $(hostname -f 2>/dev/null || hostname)"
echo "Logged in: $(whoami)@$(hostname -s)"
echo "Uptime:    $(uptime -p 2>/dev/null || uptime)"

section "Operating System"
if [[ -f /etc/os-release ]]; then
  # shellcheck source=/dev/null
  source /etc/os-release
  echo "Name:     ${PRETTY_NAME:-unknown}"
  echo "ID:       ${ID:-unknown} (${VERSION_ID:-?})"
else
  echo "No /etc/os-release found"
fi

section "Kernel"
echo "Release:      $(uname -r)"
echo "Architecture: $(uname -m)"
echo "Version:      $(uname -v | cut -c1-80)"

section "Virtualization"
if command -v systemd-detect-virt >/dev/null 2>&1; then
  echo "Type: $(systemd-detect-virt 2>/dev/null || echo none)"
else
  echo "systemd-detect-virt not available"
fi

section "Init System (PID 1)"
ps -p 1 -o pid=,comm=,args= 2>/dev/null || echo "Cannot read PID 1"

section "Boot Performance"
if command -v systemd-analyze >/dev/null 2>&1; then
  systemd-analyze 2>/dev/null | head -3
else
  who -b 2>/dev/null || true
fi
```

Make it executable: `chmod +x ~/bin/linux-inventory.sh && ~/bin/linux-inventory.sh`

### One-liner for CI/CD pipelines

Use this in deployment scripts to assert the target environment before running Ansible or cloud-init:

```bash
[[ "$(uname -s)" == "Linux" ]] && source /etc/os-release && \
  echo "Deploying to ${PRETTY_NAME} / kernel $(uname -r)" || \
  { echo "ERROR: Not a Linux host"; exit 1; }
```

## Common Mistakes

!!! warning "Confusing the kernel with the distribution"
    Saying "I run Linux 6.8" describes the kernel, not the distro. In change-management tickets, always specify both: "Ubuntu 22.04 LTS, kernel 5.15.0-105-generic." Package compatibility and support lifecycles are tied to the distro, not the kernel alone.

!!! warning "Assuming all Linux systems use systemd"
    Most server distros today use systemd, but embedded systems, containers, and Alpine Linux may use **OpenRC** or **busybox init**. Always verify PID 1 with `ps -p 1` before running `systemctl` commands in an unfamiliar environment.

!!! warning "Ignoring virtualization context"
    Debugging network or storage issues differs between bare metal, KVM VMs, and containers. Run `systemd-detect-virt` early in triage — a "missing disk" in Docker is often a volume mount issue, not a kernel driver problem.

!!! warning "Rebooting production without checking boot order"
    After kernel updates, GRUB may default to an older entry if configuration is wrong. On physical servers, verify `/etc/default/grub` and test reboots in staging. Cloud instances usually recover via console access, but downtime still hurts.

## Best Practices

!!! tip "Standardize on LTS releases in production"
    Use Long Term Support (LTS) distro releases — Ubuntu LTS (5 years) or RHEL (up to 10 years with subscription). LTS versions receive security patches without forcing application re-certification every six months.

!!! tip "Document baseline system identity in runbooks"
    Every runbook should open with how to confirm OS and kernel: `cat /etc/os-release && uname -r`. During incidents, engineers waste minutes re-discovering what they are logged into.

!!! tip "Track kernel versions across your fleet"
    Use configuration management (Ansible facts, AWS SSM Inventory, or a simple script) to detect drift. Mixed kernel versions after patching windows are a common source of "works on server A, fails on server B" bugs.

!!! tip "Learn one Debian-family and one RHEL-family distro"
    Skills transfer, but package names and paths differ (`apt` vs `dnf`, `www-data` vs `nginx` user). Interviewers and employers often expect comfort with both Ubuntu and RHEL/Rocky ecosystems.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `systemd-analyze: command not found` | Non-systemd init or minimal container | Use `who -b` for boot time; check PID 1 with `ps -p 1` |
| `/etc/os-release` missing | Very old or non-standard system | Try `lsb_release -a`, `cat /etc/redhat-release`, or `hostnamectl` |
| `dmesg: read kernel buffer failed: Operation not permitted` | Insufficient privileges or container restriction | Run with `sudo dmesg` or check host logs from hypervisor/cloud console |
| Boot hangs at "Loading initial ramdisk" | Corrupt initramfs or disk failure | Boot previous kernel from GRUB menu; regenerate initramfs with `update-initramfs` (Debian) or `dracut` (RHEL) |
| Wrong kernel running after update | GRUB default entry not updated | Run `sudo update-grub` (Debian/Ubuntu) and verify `/boot` has free space |
| `hostnamectl` shows wrong virtualization | Nested virt or custom hypervisor | Cross-check with `dmidecode -s system-product-name` (requires root) |
| Cloud instance unreachable after reboot | Network service slow to start | Check `systemd-analyze blame` for `NetworkManager-wait-online`; consider timeout tuning |

## Summary

- Linux combines a **monolithic kernel** (hardware management, syscalls) with **userspace** tools and services packaged by **distributions**
- The boot path runs: **firmware → bootloader → kernel → init (systemd) → services → login shell**
- Use `cat /etc/os-release`, `uname -r`, and `hostnamectl` to identify any system quickly
- Linux dominates cloud and DevOps because it is open, automatable, stable, and the foundation of containers
- PID 1 determines your service management model — verify it before assuming systemd
- Kernel messages in `dmesg` and boot analysis via `systemd-analyze` are essential troubleshooting tools

## Interview Questions

1. What is the difference between the Linux kernel and a Linux distribution?
2. Walk me through what happens when you power on a Linux server until you get a shell prompt.
3. Why is Linux preferred over Windows for cloud and container workloads?
4. What is PID 1, and how do you determine which init system is running?
5. Explain the role of GRUB in the boot process.
6. What information does `/etc/os-release` provide, and why is it useful in automation?
7. How would you investigate why a server takes too long to boot?
8. What is the difference between `/bin` and `/usr/bin` on a modern Linux system?
9. What does `uname -a` tell you, and when would you use `hostnamectl` instead?
10. How does open-source licensing (GPL) affect how companies use Linux in production?

??? tip "Sample Answers (Questions 1, 4, and 7)"

    **Q1 — Kernel vs distribution:** The kernel manages hardware and provides system calls — it's the core OS. A distribution bundles the kernel with GNU utilities, a package manager, init system, default configs, and support lifecycle. Example: Ubuntu 24.04 ships kernel 6.8 plus apt, systemd, and Canonical's security updates. You can upgrade the kernel without changing distros, but application compatibility is certified at the distro level.

    **Q4 — PID 1 and init:** PID 1 is the first process started by the kernel after boot; it never exits because the kernel panics if PID 1 dies. It reaps zombie processes and starts all other services. Check with `ps -p 1 -o comm=`. On modern servers the answer is usually `systemd`, which reads unit files and manages dependencies, targets, and logging via journald.

    **Q7 — Slow boot investigation:** Run `systemd-analyze` for the overall breakdown, then `systemd-analyze blame` to rank units by time. Common culprits: `NetworkManager-wait-online` waiting for DHCP, filesystem checks on large disks, and misconfigured services with long timeouts. Use `systemd-analyze critical-chain` to see dependency chains. Fix by adjusting unit timeouts, making services async, or fixing network config — never disable security updates to shave boot seconds.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Linux Filesystem Hierarchy](linux-filesystem-hierarchy.md) *(next in Module 1)*
- [Essential Linux Commands](essential-linux-commands.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [The Linux Kernel Archives](https://www.kernel.org/) — official kernel source and documentation
- [Linux man pages online](https://man7.org/linux/man-pages/) — `man uname`, `man systemd-analyze`, `man hostnamectl`
- [systemd boot analysis](https://www.freedesktop.org/software/systemd/man/latest/systemd-analyze.html)
- [Filesystem Hierarchy Standard (FHS 3.0)](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html)
- [UEFI Specification](https://uefi.org/specifications) — firmware boot interface
- [REBASH Academy – Linux Overview](index.md)
