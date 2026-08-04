---
title: "Linux Fundamentals — Distributions and Architecture"
description: "Linux what Linux is, distributions, kernel vs user space, shell vs terminal — plain language first, then a real host-identity lab."
difficulty: beginner
estimated_time: "50–65 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 1 · Linux Fundamentals"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - fundamentals
  - kernel
  - distributions
  - beginners
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

When companies say “our servers run on Linux”, they mean almost every cloud virtual machine (VM), Continuous Integration (CI) runner, and Kubernetes worker uses a **Linux-based operating system**. This tutorial is the map for that world: what “Linux” means, how **distributions** differ, and how the **kernel**, **user space**, **shell**, and **terminal** fit together.

**Plain problem:** People say “Linux” as if it were one product. In practice you meet Ubuntu, Rocky Linux, Amazon Linux, Alpine, and more. Wrong assumptions lead to wrong package commands (`apt` vs `dnf`) and broken installs.

This tutorial answers, in order:

1. What is Linux, really?
2. What is a **distribution** (distro)?
3. What is the **kernel** vs **user space**?
4. What is the difference between a **shell** and a **terminal**?
5. How do you prove what OS you are on with commands?

This is **Tutorial 1** in **Module 1: Linux Fundamentals** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- Basic computer skills (files, folders, typing commands)
- A practice Linux host: Ubuntu 22.04/24.04 VM, cloud Free Tier VM, or Windows Subsystem for Linux (WSL2) Ubuntu
- A normal user account; use `sudo` only when the lab says so

You do **not** need networking expertise, Docker, or Kubernetes yet.

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain Linux to a friend in two sentences without jargon
- [ ] Explain kernel vs user space with a simple analogy
- [ ] Identify your distro name, version, and package manager
- [ ] Distinguish shell, terminal, and TTY/PTY with commands
- [ ] Capture a small host-identity evidence pack for tickets or interviews
- [ ] Answer common fresher interview questions on this topic

## Architecture

Think of layers: hardware (or a cloud hypervisor) at the bottom, the **kernel** managing CPU/memory/disks/network, then **user space** programs (shell, `sshd`, your app). You type into a **terminal**; a **shell** program reads those commands.

![Linux architecture — hardware, kernel, user space, shell](../assets/excalidraw/linux-architecture.svg)

## Theory

### The problem (before any jargon)

You get SSH access to a “Linux server” for a college project or internship. Your notes say “use `yum install`”. The command fails. A teammate says “try `apt`”. That works.

Nothing was wrong with you — the server was a **different Linux family**. This course teaches you to **ask what you are standing on** before you change anything.

### What Linux is (simple words)

**Analogy:** The **kernel** is the building’s electrical and plumbing system — invisible but everything depends on it. The **distribution** is the fully furnished apartment: kitchen tools (package manager), locks (`sshd`), and house rules (support policy).

| Term | Plain meaning |
|------|----------------|
| **Kernel** | Core program that manages hardware and starts other programs |
| **Distribution / distro** | Kernel + installer + packages + support timeline (Ubuntu, Rocky, …) |
| **User space** | Everything that is not the kernel — apps, shells, libraries |
| **Shell** | Program that reads your typed commands (`bash`, `zsh`) |
| **Terminal** | Window or SSH session that shows text and sends keystrokes |

**What you can say in an interview:** “Linux often means the kernel; what I log into day to day is a distribution that packages the kernel with tools and a package manager.”

### Distributions you will meet at work

| Family | Common names | Package tool | Where you see it |
|--------|--------------|--------------|------------------|
| Debian family | Ubuntu, Debian | `apt` | Cloud VMs, desktops, many tutorials |
| RHEL family | RHEL, Rocky, Alma, Amazon Linux 2023 | `dnf` / `yum` | Enterprises, many AWS images |
| SUSE family | SLES, openSUSE | `zypper` | Some enterprises |
| Alpine | Alpine Linux | `apk` | Containers (small images) |

**Tiny example — read your OS identity:**

``` {.bash .ra-terminal title="Terminal"}
cat /etc/os-release
```

Look for `NAME=`, `VERSION_ID=`, and `ID_LIKE=` (family hints).

### Kernel vs user space

**Analogy:** Kernel = building management. User space = the people and shops inside. If a shop (app) crashes, you usually restart the shop. If the building’s power (kernel) fails, you often need a reboot or a new machine image.

| Layer | Examples | Typical fix |
|-------|----------|-------------|
| Kernel | Drivers, memory, CPU scheduling | Reboot, new AMI/image, kernel update |
| User space | `nginx`, `sshd`, `bash`, your Python app | Restart service, fix config, reinstall package |

``` {.bash .ra-terminal title="Terminal"}
uname -r          # kernel release
hostnamectl       # pretty OS name + kernel (systemd hosts)
```

### Shell vs terminal (students mix these up)

- **Terminal** (or terminal emulator): the window / SSH session UI.
- **Shell**: the program inside that interprets `ls`, `cd`, pipelines.
- **TTY / PTY**: the kernel device connecting keyboard/screen to the shell (`tty` command shows it).

``` {.bash .ra-terminal title="Terminal"}
echo "$SHELL"
tty
ps -p $$ -o args=
```

**Interview line:** “The terminal is the session; the shell is the command interpreter running inside it.”

### How a command runs (simple flow)

1. You type `ls` and press Enter in the terminal.
2. The shell finds the `ls` program (usually `/usr/bin/ls`).
3. The shell asks the kernel to start that program as a new process.
4. The program uses system calls (`open`, `read`, …) via the kernel.
5. Output text returns to your terminal.

You will live in that loop for your whole DevOps career.

### Why Cloud / DevOps teams care

- CI images and production images must match **distro expectations** (glibc vs musl on Alpine).
- Support and security patches follow the distro’s **Long Term Support (LTS)** calendar.
- Runbooks say `systemctl` on Ubuntu/RHEL; Alpine may use different service tools.
- Interviews often start with: “How do you identify an unknown host?”

### Common pitfalls

- Memorising only Ubuntu commands, then failing on Rocky/Amazon Linux
- Calling Alpine “just small Ubuntu”
- Blaming “the kernel” for every app bug
- Running daily work as `root` instead of a normal user + `sudo`

## Hands-on Lab

### Objective

Identify your Linux host like a professional: distro, kernel, architecture, shell, and a short evidence pack you could attach to a ticket.

### Prerequisites

| Item | Notes |
|------|--------|
| Linux practice host | Ubuntu preferred |
| Terminal access | Local, SSH, or WSL2 |
| `sudo` | Only if a command asks; most of this lab is read-only |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab01 && cd ~/rebash-linux/lab01
```

### Real-world scenario

Day one on a team: you receive SSH access to a “build agent”. Before you install anything, your mentor asks: “What OS is it, which kernel, and which package manager should we use?” This lab is that answer with proof files.

### Step-by-step tasks

#### Task 1 – Capture OS and kernel identity

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
cat /etc/os-release | tee os-release.txt
uname -a | tee uname.txt
uname -r | tee kernel-release.txt
test -s os-release.txt && test -s uname.txt
grep -E '^(NAME|VERSION_ID|ID)=' os-release.txt
```

!!! example "Expected output"
    `os-release.txt` shows `NAME` and `VERSION_ID`. `uname.txt` includes kernel and architecture (for example `x86_64`).


#### Task 2 – Shell, terminal, and package-manager hint

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
echo "$SHELL" | tee shell.txt
tty | tee tty.txt
ps -p $$ -o pid=,args= | tee shell-process.txt
command -v apt && echo "package_hint=apt" | tee package-hint.txt
command -v dnf && echo "package_hint=dnf" | tee -a package-hint.txt
command -v yum && echo "package_hint=yum" | tee -a package-hint.txt
command -v apk && echo "package_hint=apk" | tee -a package-hint.txt
test -s package-hint.txt
cat package-hint.txt
```

!!! example "Expected output"
    `shell.txt` shows a path such as `/bin/bash`. `package-hint.txt` lists at least one package manager command found on the host.


#### Task 3 – One-page host summary for humans

Create `host-summary.md`:

```markdown title="host-summary.md"
# Host summary — lab01

- Distro name: (copy from NAME= in os-release.txt)
- Version: (copy from VERSION_ID=)
- Kernel: (copy from kernel-release.txt)
- Shell: (copy from shell.txt)
- Package manager hint: (copy from package-hint.txt)
- What I would install packages with: (apt / dnf / …)
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
test -f host-summary.md
wc -l host-summary.md | tee summary-lines.txt
echo "lab01 identity pack OK" | tee evidence.txt
ls -la
```

!!! example "Expected output"
    `host-summary.md` exists and is filled with your values; `evidence.txt` confirms completion.


### Validation steps

- [ ] You can explain distro vs kernel without looking at notes
- [ ] Evidence files exist under `~/rebash-linux/lab01`
- [ ] Package manager hint matches your distro family
- [ ] You did not needlessly use `sudo` for read-only commands

### Common errors and fixes

| Error | Meaning | Fix |
|-------|---------|-----|
| `cat: /etc/os-release: No such file` | Very old or unusual system | Try `/etc/redhat-release` or `lsb_release -a` |
| Empty `package-hint.txt` | Minimal container without tools | Install nothing yet; note “unknown — ask mentor” |
| Permission denied | Rare on these reads | Check you are logged into the right host |

### Challenge exercise

Create `distro-families.md` listing three families (Debian, RHEL, Alpine) and one package command each, in your own words.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
test -s distro-families.md
echo "challenge OK" | tee challenge.txt
```

### Learning outcomes

- You identified a real Linux host like an engineer
- You separated kernel facts from distro facts
- You have interview-ready evidence files

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab01
# Keep the evidence pack for your notes; optional:
# rm -f *.txt challenge.txt
# Keep host-summary.md and distro-families.md for revision
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab01`
- [ ] Can teach kernel vs distro to a classmate in two minutes
- [ ] Ready for boot process and filesystem hierarchy next

## Code Walkthrough

1. **`/etc/os-release` first** — standard identity file on modern distros.
2. **`uname -r`** — kernel only; do not confuse with Ubuntu version.
3. **`command -v apt`** — safer than guessing the package manager.
4. **Write a human summary** — tickets need prose, not only raw command dumps.
5. **Read-only habit** — gather facts before you change the system.

## Security Considerations

- Prefer a normal user for daily work; escalate with `sudo` only when required.
- Do not paste private hostnames, IPs, or keys into public GitHub gists.
- Treat unknown hosts carefully — identify before you install packages.

## Common Mistakes

!!! warning "Ubuntu commands on every host"
    Rocky/RHEL need `dnf`. Alpine needs `apk`. Always check `/etc/os-release` first.

!!! warning "Kernel version = distro version"
    Ubuntu 24.04 can run different kernel packages. Read both `VERSION_ID` and `uname -r`.

!!! warning "Terminal and shell are the same"
    The terminal is the session UI; the shell is the interpreter. Interviews love this distinction.

## Best Practices

- Document distro family in inventory for every server
- Prefer LTS cloud images for learning and production baselines
- Keep a personal “host identity” checklist (this lab)
- Match container base images to the glibc/musl needs of your binaries

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `apt` not found | RHEL-family or Alpine host | Use `dnf`/`yum` or `apk` after checking `os-release` |
| `hostnamectl` missing | Non-systemd or tiny image | Rely on `uname` + `os-release` |
| Confused by WSL | Windows integration layer | Still use `os-release`; note WSL in your summary |

## Summary

**Linux** at work usually means a **distribution** built on the Linux **kernel**. Learn to identify distro, kernel, shell, and package manager before you change anything. Next you will see how the system boots and where files live on disk.

## Interview Questions

**1. What is Linux, in simple words?**

??? success "Reveal answer"
    Linux usually refers to the open-source kernel that manages hardware and processes. Day to day, engineers work on a **distribution** (Ubuntu, Rocky, …) that packages that kernel with tools, a package manager, and support policies.

**2. What is the difference between the kernel and a distribution?**

??? success "Reveal answer"
    The kernel is the core that talks to hardware and runs processes. A distribution adds user-space tools, an installer, packages, and a release/support model. You install Ubuntu or Rocky — not “bare kernel only” — on servers.

**3. What is user space?**

??? success "Reveal answer"
    User space is everything outside the kernel: shells, system services like `sshd`, libraries, and applications. Most day-to-day fixes (config, packages, service restarts) happen in user space.

**4. Shell vs terminal — what is the difference?**

??? success "Reveal answer"
    The terminal (or SSH session) is the text interface you look at. The shell is the program (often bash) that reads and runs your commands inside that session. `echo $SHELL` and `tty` help show both.

**5. How do you identify an unknown Linux host?**

??? success "Reveal answer"
    Read `/etc/os-release` for name and version, run `uname -r` for the kernel, and check which package manager exists (`apt`, `dnf`, `apk`). That trio prevents wrong install commands.

**6. Why do Alpine containers break some programs that work on Ubuntu?**

??? success "Reveal answer"
    Alpine often uses **musl** instead of **glibc**, and a different package ecosystem (`apk`). Binaries built for glibc Ubuntu may fail on Alpine. Teams choose base images deliberately.

**7. When is a problem likely a kernel issue vs an application issue?**

??? success "Reveal answer"
    App/config/service failures are usually user space (logs, restart, package fix). Kernel issues often involve drivers, sudden whole-system hangs, or features needing a newer kernel — frequently fixed by reboot or a new machine image rather than editing an app config.

## Related Tutorials

- Next: [Boot Process and Filesystem Hierarchy](boot-process-and-filesystem-hierarchy.md)
- Standalone lab: [Linux install and first boot](../labs/linux-install-and-first-boot.md)
- Later: [Essential Linux Commands](essential-linux-commands.md)

## References

- [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) *(preview for next tutorial)*
- [os-release man page](https://www.freedesktop.org/software/systemd/man/os-release.html)
- [Linux kernel documentation](https://docs.kernel.org/)
