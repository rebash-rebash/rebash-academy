---
title: "Linux Fundamentals — Distributions and Architecture"
description: "Learn what Linux is, how distributions differ, and how kernel, user space, shell, and terminal fit together for Cloud and DevOps work."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 1 · Linux Fundamentals"
tags:
  - linux
  - fundamentals
  - kernel
  - distributions
  - architecture
prerequisites: []
next:
  - linux/boot-process-and-filesystem-hierarchy
related:
  - labs/linux-install-and-first-boot
labs:
  - labs/linux-install-and-first-boot
interview: interview/linux
comments: false
---

# Linux Fundamentals — Distributions and Architecture

## Overview

When you open a cloud virtual machine (VM), a Continuous Integration (CI) runner, or a Kubernetes worker node, you are almost always working on **Linux**. Before you change files, services, or networks, you need a clear picture of what “Linux” means, which **distribution** you are on, and how the **kernel**, **user space**, **shell**, and **terminal** fit together.

**Linux** started as a **kernel** — the core that manages CPU, memory, disks, and network. A usable server also needs user-space tools: a package manager, a shell, libraries, and services such as `sshd` and `systemd`. A **distribution** (often called a **distro**) packages the kernel with those tools, an installer, and a support policy. Ubuntu and Debian use `apt`. Red Hat Enterprise Linux (RHEL), Rocky Linux, and AlmaLinux use `dnf`/`yum`. Alpine uses `apk` and is common in containers. In this tutorial you will identify your distro, read kernel and user-space facts, and prove the difference between a shell and a terminal.

Cloud teams care about this because images, packages, and support windows differ by family. Mixing Alpine (musl) assumptions with Ubuntu (glibc) tools breaks builds. Treating every host as “just Linux” leads to the wrong package commands, wrong service names, and wrong runbooks. In production you pin known cloud images, document the distro family in inventory, and separate **kernel problems** (rare, often need reboot or a new image) from **user-space problems** (usually fixable with packages, configs, or service restarts).

This is **Tutorial 1** in **Module 1: Linux Fundamentals** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a small evidence pack you can use when onboarding a new VM or explaining Linux architecture in an interview.

## Prerequisites

- Basic computer knowledge (files, folders, login)
- A **practice Ubuntu 22.04/24.04 VM** (or similar Linux host) with terminal access
- A normal user account; `sudo` only where the lab says so

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain what the Linux kernel is and how a distribution differs from “just the kernel”
- [ ] Identify your distro family, version, and package manager from `/etc/os-release` and commands
- [ ] Describe the layers: hardware → kernel → user space → shell/applications
- [ ] Distinguish shell, terminal emulator, and TTY/PTY with real commands
- [ ] Capture host identity evidence suitable for a change ticket or onboarding note

## Architecture

Linux sits between people or automation and the hardware (or hypervisor). The kernel owns resources. User space runs tools and services. The shell is the program that reads your commands inside a terminal session.

![Architecture diagram for Linux Fundamentals — Distributions and Architecture](../assets/excalidraw/linux-architecture.svg)

## Theory

### What it is

**Linux** is an open-source **kernel**. It schedules processes, manages memory, talks to devices through drivers, and exposes a system-call interface (`open`, `read`, `fork`, `exec`, `socket`, and many more).

A **distribution** ships:

| Piece | Examples |
|-------|----------|
| Kernel | Version shown by `uname -r` |
| Init / services | Usually `systemd` on servers |
| Package manager | `apt`, `dnf`, `zypper`, `apk` |
| User-space tools | GNU coreutils, shells, libraries |
| Release policy | LTS vs rolling; security support window |

**User space** is everything that is not the kernel: daemons, CLI tools, libraries under `/usr`, and your applications. The **shell** (`bash`, `zsh`, `sh`) interprets commands. The **terminal** (or terminal emulator) is the window or SSH session that shows text and sends keystrokes. The kernel connects them with a TTY or PTY device.

``` {.bash .ra-terminal title="Terminal"}
uname -r
cat /etc/os-release
echo "$SHELL"
tty
```

### Why it matters

Cloud VM images, container base images, and CI runners are chosen by **distro family** and **support window**, not by fashion. Wrong package commands waste time. Wrong glibc/musl assumptions break binaries. Kernel version matters for features such as cgroup v2, eBPF, and newer filesystems. When an incident happens, your first question is often: “Is this kernel, systemd/user space, or the app?” That split decides whether you restart a service, rebuild a package, or replace the image.

### How it works

1. **Hardware or hypervisor** presents CPU, RAM, disks, and NICs.
2. **Kernel** boots, loads drivers, mounts the root filesystem, and starts PID 1 (usually systemd).
3. **User space** starts services (`sshd`, `cron`, your app).
4. You connect with SSH into a **PTY**; a **shell** process reads your commands and starts child processes.
5. Those processes call the **kernel** through system calls.

``` {.bash .ra-terminal title="Terminal"}
hostnamectl          # OS pretty name, kernel, architecture
ps -p $$ -o pid,tty,comm,args
ls -l /proc/$$/exe   # which shell binary this session uses
```

### Key concepts and comparisons

| Layer | What lives here | Typical failure |
|-------|-----------------|-----------------|
| Hardware / VM | CPU, disk, NIC | Hypervisor, quota, wrong instance type |
| Kernel | Drivers, memory, scheduling | Panic, OOM killer, driver bug |
| User space | systemd, sshd, packages | Bad config, missing package, crashed daemon |
| Shell / app | bash, Python, nginx | Script error, app bug |

| Family | Examples | Package tool | Common Cloud use |
|--------|----------|--------------|------------------|
| Debian | Debian, Ubuntu | `apt` | Popular cloud images, docs, CI |
| RHEL-like | RHEL, Rocky, Alma | `dnf`/`yum` | Enterprise, OpenShift |
| SUSE | SLES, openSUSE | `zypper` | Enterprise niches |
| Minimal | Alpine, Amazon Linux | `apk` / `dnf` | Containers, AWS-tuned hosts |

| Concept | Role |
|---------|------|
| Terminal emulator | UI that shows text (GNOME Terminal, Windows Terminal, `tmux`) |
| Shell | Program that interprets commands |
| TTY / PTY | Kernel device for the login session |

### Common pitfalls

- Saying “Linux” when you mean a full distro — `apt` vs `dnf` vs `apk` are not the same.
- Choosing a distro for popularity instead of support window, image availability, and company standard.
- Debugging only in a graphical terminal and assuming cron or CI has the same environment variables.
- Treating every user-space failure as a reboot problem — many daemon issues do not need a reboot.
- Mixing Alpine (musl) containers with Ubuntu/RHEL (glibc) binaries without testing.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, identify the distribution and architecture layers, prove shell versus terminal facts, and save an identity evidence pack under `~/rebash-linux/lab01`.

### Prerequisites

- Ubuntu 22.04/24.04 (or Debian) practice VM
- Packages already present: `bash`, `coreutils`, `procps`, `hostname` tooling (`hostnamectl` via `systemd`)
- Do **not** run destructive changes on a shared production server

### Lab environment

Workspace: `~/rebash-linux/lab01`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab01 && cd ~/rebash-linux/lab01
set -euo pipefail
whoami | tee lab-user.txt
uname -s | tee kernel-name.txt
test "$(uname -s)" = "Linux"
```

!!! example "Expected output"
    `lab-user.txt` and `kernel-name.txt` exist; `kernel-name.txt` contains `Linux`.


### Real-world scenario

Your team received a new Ubuntu cloud image for application servers. Before the first deploy, platform asks you to confirm the OS family, kernel version, architecture, default shell, and package manager — and to keep proof for the onboarding ticket. You collect facts only; you do not change packages yet.

### Step-by-step tasks

#### Task 1 – Identify distribution and package family

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
set -euo pipefail

cat /etc/os-release | tee os-release.txt
. /etc/os-release
printf 'ID=%s\nVERSION_ID=%s\nID_LIKE=%s\n' "${ID}" "${VERSION_ID}" "${ID_LIKE:-}" | tee distro-summary.txt

if command -v apt-get >/dev/null; then
  echo "package_family=apt" | tee package-family.txt
elif command -v dnf >/dev/null; then
  echo "package_family=dnf" | tee package-family.txt
elif command -v apk >/dev/null; then
  echo "package_family=apk" | tee package-family.txt
else
  echo "package_family=unknown" | tee package-family.txt
fi

grep -E '^(ID|VERSION_ID|ID_LIKE)=' os-release.txt
test -s package-family.txt
```

!!! example "Expected output"
    `os-release.txt` shows Ubuntu (or your distro); `package-family.txt` says `apt` on Ubuntu; `distro-summary.txt` has `ID` and `VERSION_ID`.


#### Task 2 – Map kernel versus user space

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
set -euo pipefail

uname -a | tee uname.txt
uname -r | tee kernel-release.txt
hostnamectl 2>/dev/null | tee hostnamectl.txt || true

# Kernel-exported facts (user space reading kernel interfaces)
head -n 5 /proc/version | tee proc-version.txt
grep -E '^(MemTotal|MemFree):' /proc/meminfo | tee meminfo-snippet.txt
nproc | tee nproc.txt

# User-space binaries that are not the kernel
command -v bash | tee bash-path.txt
command -v systemctl | tee systemctl-path.txt || echo 'no-systemctl' | tee systemctl-path.txt
ls -l "$(command -v bash)" | tee bash-ls.txt

test -s kernel-release.txt
test -s proc-version.txt
```

!!! example "Expected output"
    `kernel-release.txt` shows a version like `6.x.x-…`; `bash-path.txt` points under `/usr` or `/bin`; `proc-version.txt` mentions Linux.


#### Task 3 – Prove shell versus terminal, then pack evidence

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
set -euo pipefail

echo "SHELL=$SHELL" | tee shell-env.txt
ps -p $$ -o pid=,tty=,comm=,args= | tee shell-process.txt
tty | tee tty.txt
ls -l /proc/$$/exe | tee shell-exe.txt

# Same host, different “views”: login name vs process vs device
id -un | tee id-user.txt
printf 'pid=%s tty=%s\n' "$$" "$(tty)" | tee session-map.txt

tar -czf linux-identity-evidence.tgz \
  lab-user.txt kernel-name.txt os-release.txt distro-summary.txt package-family.txt \
  uname.txt kernel-release.txt hostnamectl.txt proc-version.txt meminfo-snippet.txt nproc.txt \
  bash-path.txt systemctl-path.txt bash-ls.txt \
  shell-env.txt shell-process.txt tty.txt shell-exe.txt id-user.txt session-map.txt
ls -l linux-identity-evidence.tgz | tee evidence-ls.txt
test -s linux-identity-evidence.tgz
```

!!! example "Expected output"
    `tty.txt` shows a pts or tty device; `shell-process.txt` shows your shell (often `bash`); evidence archive is not empty.


### Validation steps

- [ ] `ID=` in `os-release.txt` matches the VM you expected
- [ ] `package-family.txt` matches the distro family
- [ ] `kernel-release.txt` and `bash-path.txt` both exist (kernel fact vs user-space binary)
- [ ] `tty.txt` and `shell-env.txt` are different kinds of facts (device vs program)
- [ ] `linux-identity-evidence.tgz` exists under `~/rebash-linux/lab01`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `hostnamectl: command not found` | Minimal image without systemd tools | Use `cat /etc/os-release` and `uname -a`; skip hostnamectl |
| Empty `/etc/os-release` | Unusual or container-minimal image | Check `/usr/lib/os-release` or image docs |
| `tty` says `not a tty` | Non-interactive script context | Run tasks in an interactive SSH/terminal session |
| Wrong package family guess | Custom image | Inspect `command -v apt-get dnf apk` manually |

### Challenge exercise

Write an executable script `~/rebash-linux/lab01/host-identity.sh` that prints four labelled lines: `distro=`, `kernel=`, `package_family=`, and `shell=`, using `/etc/os-release`, `uname -r`, package-manager detection, and `$SHELL`. Run it and save output to `host-identity-out.txt`. Keep the script as your stretch artefact.

``` {.bash .ra-terminal title="Terminal"}
# After you create the script:
chmod +x ~/rebash-linux/lab01/host-identity.sh
~/rebash-linux/lab01/host-identity.sh | tee ~/rebash-linux/lab01/host-identity-out.txt
```

### Learning outcomes

- Identified distro ID, version, and package family from real files
- Separated kernel facts (`uname`, `/proc`) from user-space binaries
- Mapped shell process, `$SHELL`, and TTY device
- Built an evidence archive for onboarding or tickets

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
# Keep the evidence archive and challenge script if you want them for your notes.
# To remove lab text files only:
# rm -f *.txt
# rm -f linux-identity-evidence.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab01/` with evidence files
- [ ] You can explain kernel vs distribution vs user space in plain words
- [ ] You can explain shell vs terminal vs TTY
- [ ] You know why cloud teams pin a distro image instead of “latest random Linux”

## Code Walkthrough

In real servers, Linux identity checks for **distributions and architecture** usually follow this order:

1. **Confirm the OS** — `/etc/os-release`, `hostnamectl`  
2. **Confirm the kernel** — `uname -r`, note architecture (`uname -m`)  
3. **Confirm the package family** — `apt` / `dnf` / `apk` before you install anything  
4. **Confirm the session** — shell path, TTY, whether you are in SSH, `tmux`, or CI  
5. **Capture evidence** — save outputs for tickets and handovers  

Later modules assume you can answer “what am I on?” in under a minute.

## Security Considerations

- Treat SSH and sudo on the host as privileged — know who can log in  
- Do not paste secrets into shell history, tickets, or screenshots  
- Prefer known, patched cloud images over unmanaged “golden” USB installs  
- Record kernel and package versions when you report vulnerabilities  
- Separate human admin access from application service accounts (covered in Module 4)

## Common Mistakes

!!! warning "Calling every host ‘Linux’ without naming the distro"
    Package commands and paths differ. **Fix:** always read `/etc/os-release` and record `ID` + `VERSION_ID` in inventory.

!!! warning "Assuming the terminal program is the shell"
    Closing a window is not the same as understanding `bash` vs `sh`. **Fix:** check `echo $SHELL`, `ps -p $$`, and `/proc/$$/exe`.

!!! warning "Rebooting for every failure"
    User-space service failures often need `systemctl` and logs, not a reboot. **Fix:** decide kernel vs user space before you reboot.

!!! warning "Using Alpine container habits on Ubuntu VMs without thinking"
    musl vs glibc and busybox vs GNU tools behave differently. **Fix:** match base image family to the binary and docs you ship.

## Best Practices

- Pin cloud image IDs (AMI / gallery image version) in Infrastructure as Code (IaC)  
- Document distro family and package manager in the team runbook  
- Prefer Long Term Support (LTS) server images for production fleets  
- Keep a small “first five commands” list for new hosts: `os-release`, `uname -a`, `df -h`, `ip -br a`, `systemctl --failed`  
- Test containers and VMs on the same family you use in production  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `apt-get: command not found` | RHEL-like or Alpine host | Use `dnf` or `apk`; confirm `/etc/os-release` |
| Binary “not found” but file exists | Wrong arch or musl/glibc mismatch | Check `uname -m` and `ldd` / image family |
| `hostnamectl` missing | Minimal/container image | Use `cat /etc/os-release` and `uname` |
| Script works in GUI terminal, fails in cron | Different shell or environment | Use absolute paths; set shebang; do not rely on interactive `$PATH` |
| Unclear if issue is kernel | Panic, hard lock, driver errors | Check `journalctl -k` / console; plan image or kernel update |

## Summary

Linux for Cloud and DevOps means a **kernel plus a distribution’s user space**. Know your distro family, package manager, kernel version, and the difference between shell and terminal — then keep proof. Next, learn how the system starts and where files live in [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md).

## Interview Questions

**1. What is the difference between the Linux kernel and a Linux distribution?**

??? success "Reveal answer"
    The **kernel** is the core that manages CPU, memory, devices, and system calls. A **distribution** packages that kernel with user-space tools, a package manager, an init system, and a support/release policy. When people say “Ubuntu server”, they mean the full distribution, not only the kernel.

**2. A teammate says “install with yum” on an Ubuntu cloud VM. What do you check, and what do you run instead?**

??? success "Reveal answer"
    Check `/etc/os-release` (and optionally `hostnamectl`). On Ubuntu/Debian the package tool is **`apt`** (`apt-get` / `apt`). `yum`/`dnf` belong to RHEL-like systems. Using the wrong tool is a signal that inventory or assumptions about the image are wrong.

**3. How do shell, terminal emulator, and TTY/PTY differ?**

??? success "Reveal answer"
    The **terminal emulator** (or SSH client view) displays text and captures keys. The **shell** (`bash`, `zsh`, …) is the program that parses commands. **TTY/PTY** is the kernel device that connects that session to the shell process. You can see them with `tty`, `echo $SHELL`, and `ps -p $$`.

**4. Why do Cloud and platform teams pin a specific image version instead of always taking “latest Ubuntu”?**

??? success "Reveal answer"
    Pinning keeps kernels, packages, and behaviour **reproducible** across the fleet. “Latest” can change under you and break automation. Teams record image IDs in IaC, test upgrades, then roll forward on purpose.

**5. Give one production symptom that points to the kernel and one that points to user space.**

??? success "Reveal answer"
    **Kernel:** panic, hard lock-up, driver failure, sudden OOM killer behaviour tied to memory management. **User space:** `sshd` or nginx crash loop, bad unit file, missing package, wrong config — often fixed with packages/config/`systemctl` without replacing the kernel. Always gather evidence before you reboot.

**6. Why can a binary that runs on Ubuntu fail inside an Alpine container?**

??? success "Reveal answer"
    Ubuntu uses **glibc**; many Alpine images use **musl** and different library paths. Dynamically linked binaries and some tooling assumptions do not transfer. Teams either rebuild for the target image family or use a matching base image.

**7. What facts would you put in an onboarding ticket for a new Linux VM?**

??? success "Reveal answer"
    At minimum: distro `ID` and `VERSION_ID`, kernel release (`uname -r`), architecture (`uname -m`), package family, hostname, and default admin access model (who has sudo). Attach command output (`os-release`, `uname -a`, `hostnamectl`) so the next engineer does not guess.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md) *(next)*
- [Lab — Install and First Boot](../labs/linux-install-and-first-boot.md) *(more practice)*

## References

- [Linux Kernel documentation](https://docs.kernel.org/) — kernel docs  
- [`os-release(5)`](https://www.freedesktop.org/software/systemd/man/latest/os-release.html) — OS identification  
- [Ubuntu releases](https://ubuntu.com/about/release-cycle) — support windows  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
