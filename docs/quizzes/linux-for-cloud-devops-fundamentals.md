---
title: "Quiz — Linux for Cloud & DevOps Fundamentals"
description: "40-question quiz covering all 16 modules of the Linux for Cloud & DevOps Engineers track — fundamentals through production operations."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-29"
category: quizzes
tags:
  - quizzes
  - linux
  - assessment
comments: false
---

# Quiz — Linux for Cloud & DevOps Fundamentals

## Quiz Overview

Assess production Linux skills for Cloud, DevOps, Platform, and SRE roles across the full track.

| Attribute | Value |
|-----------|--------|
| Topic | Linux for Cloud & DevOps Engineers |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Attempt each section without peeking. Use **Reveal answer** only after you commit to a choice.

!!! tip "Older Linux quizzes"
    [Linux Fundamentals](linux-fundamentals.md) and [Linux Servers](linux-servers.md) remain available. Prefer **this quiz** for the rewritten 16-module course.

## Learning Objectives

This quiz assesses whether you can:

- [ ] Explain Linux architecture, boot, and FHS
- [ ] Use core commands, filesystem concepts, and permissions
- [ ] Process text and manage processes
- [ ] Operate systemd, storage, networking, and packages
- [ ] Schedule work, read logs, and monitor hosts
- [ ] Apply security, container basics, troubleshooting, and production judgement


## Section — Fundamentals & Filesystem (Modules 1–3)

### Question 1

What is the Linux kernel primarily responsible for?

**Difficulty:** Beginner

**Options:**

- **A.** Process scheduling, memory, devices, and system calls
- **B.** Providing a graphical desktop theme store
- **C.** Replacing DNS on the public internet
- **D.** Compiling JavaScript for browsers

??? success "Reveal answer"
    **Correct answer: A**

    The kernel mediates hardware and user-space processes.

    **Related concepts**

    - kernel
    - architecture

    **Module focus:** M1 Fundamentals

### Question 2

Ubuntu and Rocky Linux are examples of what?

**Difficulty:** Beginner

**Options:**

- **A.** Kernels only
- **B.** Linux distributions (kernel + userland + packages)
- **C.** Firmware boot ROMs
- **D.** Container runtimes

??? success "Reveal answer"
    **Correct answer: B**

    A distribution packages the kernel with tools, libraries, and policies.

    **Related concepts**

    - distributions

    **Module focus:** M1 Fundamentals

### Question 3

In a typical modern Linux boot, which process is PID 1?

**Difficulty:** Beginner

**Options:**

- **A.** bash
- **B.** sshd
- **C.** systemd (on most Cloud/DevOps hosts)
- **D.** cron

??? success "Reveal answer"
    **Correct answer: C**

    systemd is the init system and PID 1 on most current server distributions.

    **Related concepts**

    - boot
    - systemd

    **Module focus:** M1 Boot/FHS

### Question 4

Which directory traditionally holds host-specific configuration?

**Difficulty:** Beginner

**Options:**

- **A.** /var
- **B.** /proc
- **C.** /home
- **D.** /etc

??? success "Reveal answer"
    **Correct answer: D**

    FHS places configuration under /etc.

    **Related concepts**

    - FHS

    **Module focus:** M1 Boot/FHS

### Question 5

Which command prints the current working directory?

**Difficulty:** Beginner

**Options:**

- **A.** pwd
- **B.** cwd
- **C.** whereami
- **D.** ls -d

??? success "Reveal answer"
    **Correct answer: A**

    pwd = print working directory.

    **Related concepts**

    - commands

    **Module focus:** M2 Commands

### Question 6

Which command follows a growing log file in real time?

**Difficulty:** Beginner

**Options:**

- **A.** head -f
- **B.** tail -f
- **C.** cat -f
- **D.** less -grow

??? success "Reveal answer"
    **Correct answer: B**

    tail -f follows appended output.

    **Related concepts**

    - tail

    **Module focus:** M2 Commands

### Question 7

A symbolic link differs from a hard link because a symlink:

**Difficulty:** Beginner

**Options:**

- **A.** Shares the same inode and cannot cross filesystems
- **B.** Is only available on network filesystems
- **C.** Stores a path reference and can point across filesystems
- **D.** Always requires root to create

??? success "Reveal answer"
    **Correct answer: C**

    Symlinks are path pointers; hard links share inodes on one filesystem.

    **Related concepts**

    - symlinks
    - inodes

    **Module focus:** M3 Filesystem

### Question 8

You suspect inode exhaustion, not block exhaustion. Which check helps most?

**Difficulty:** Intermediate

**Options:**

- **A.** du -sh / only
- **B.** free -h
- **C.** uptime
- **D.** df -i

??? success "Reveal answer"
    **Correct answer: D**

    df -i reports inode usage per filesystem.

    **Related concepts**

    - inodes
    - df

    **Module focus:** M3 Filesystem

## Section — Users, Text, Processes (Modules 4–6)

### Question 9

Which command shows your user identity and group memberships?

**Difficulty:** Beginner

**Options:**

- **A.** id
- **B.** whoami -G
- **C.** passwd -a
- **D.** login

??? success "Reveal answer"
    **Correct answer: A**

    id prints uid, gid, and groups.

    **Related concepts**

    - users

    **Module focus:** M4 Users

### Question 10

What does chmod 640 typically grant?

**Difficulty:** Beginner

**Options:**

- **A.** Owner rwx, group rwx, others rwx
- **B.** Owner rw, group r, others none
- **C.** Owner r, group rw, others rw
- **D.** Sticky bit on a directory only

??? success "Reveal answer"
    **Correct answer: B**

    6=rw, 4=r, 0=none.

    **Related concepts**

    - chmod

    **Module focus:** M4 Permissions

### Question 11

The SGID bit on a directory is commonly used to:

**Difficulty:** Intermediate

**Options:**

- **A.** Make all files world-writable
- **B.** Disable ACLs
- **C.** Force new files to inherit the directory's group
- **D.** Encrypt filenames

??? success "Reveal answer"
    **Correct answer: C**

    SGID on directories preserves group ownership for collaboration.

    **Related concepts**

    - SGID

    **Module focus:** M4 Permissions

### Question 12

Which tool is best for field-oriented reporting from columnar text?

**Difficulty:** Beginner

**Options:**

- **A.** gzip
- **B.** chmod
- **C.** systemctl
- **D.** awk

??? success "Reveal answer"
    **Correct answer: D**

    awk excels at column splitting and reports.

    **Related concepts**

    - awk

    **Module focus:** M5 Text

### Question 13

grep -v inverts the match. What does that mean?

**Difficulty:** Beginner

**Options:**

- **A.** Print lines that do not match the pattern
- **B.** Match only verbose log levels
- **C.** Search compressed files only
- **D.** Ignore binary files silently always

??? success "Reveal answer"
    **Correct answer: A**

    -v selects non-matching lines.

    **Related concepts**

    - grep

    **Module focus:** M5 Text

### Question 14

Which command lists processes in a portable snapshot form?

**Difficulty:** Beginner

**Options:**

- **A.** df -h
- **B.** ps aux (or ps -ef)
- **C.** ip route
- **D.** lsblk

??? success "Reveal answer"
    **Correct answer: B**

    ps snapshots process state.

    **Related concepts**

    - ps

    **Module focus:** M6 Processes

### Question 15

You want a process to keep running after logout. A classic approach is:

**Difficulty:** Intermediate

**Options:**

- **A.** kill -9
- **B.** chmod +x
- **C.** nohup cmd & (or a systemd unit)
- **D.** umask 000

??? success "Reveal answer"
    **Correct answer: C**

    nohup ignores SIGHUP; systemd is preferred for services.

    **Related concepts**

    - nohup
    - signals

    **Module focus:** M6 Processes

### Question 16

renice adjusts which attribute of a running process?

**Difficulty:** Intermediate

**Options:**

- **A.** Filesystem mount options
- **B.** SELinux context only
- **C.** APT pin priority
- **D.** Scheduling nice priority

??? success "Reveal answer"
    **Correct answer: D**

    renice changes nice value for CPU scheduling priority.

    **Related concepts**

    - nice

    **Module focus:** M6 Processes

## Section — systemd, Storage, Networking (Modules 7–9)

### Question 17

Which command shows whether a unit is active and recent logs summary?

**Difficulty:** Beginner

**Options:**

- **A.** systemctl status unit
- **B.** apt status unit
- **C.** cron status unit
- **D.** sshd -T unit

??? success "Reveal answer"
    **Correct answer: A**

    systemctl status is the first service triage step.

    **Related concepts**

    - systemctl

    **Module focus:** M7 systemd

### Question 18

journalctl -u nginx.service -f does what?

**Difficulty:** Beginner

**Options:**

- **A.** Formats disks named nginx
- **B.** Follows the journal for that unit
- **C.** Forces nginx to reload certificates
- **D.** Flushes firewall rules

??? success "Reveal answer"
    **Correct answer: B**

    -u filters by unit; -f follows.

    **Related concepts**

    - journalctl

    **Module focus:** M7 systemd

### Question 19

systemd timers are often preferred over cron when you need:

**Difficulty:** Intermediate

**Options:**

- **A.** Only email on success
- **B.** GUI calendar popups
- **C.** Unit dependencies and journal-integrated runs
- **D.** To avoid all logging

??? success "Reveal answer"
    **Correct answer: C**

    Timers integrate with systemd dependencies and journaling.

    **Related concepts**

    - timers

    **Module focus:** M7 Targets/Timers

### Question 20

Before creating a filesystem, which inventory command is essential?

**Difficulty:** Beginner

**Options:**

- **A.** dig
- **B.** grep
- **C.** last
- **D.** lsblk -f

??? success "Reveal answer"
    **Correct answer: D**

    Always identify the correct block device first.

    **Related concepts**

    - lsblk

    **Module focus:** M8 Storage

### Question 21

Why mount by UUID in /etc/fstab?

**Difficulty:** Intermediate

**Options:**

- **A.** Device names like /dev/sdX can change across reboots
- **B.** UUIDs encrypt the filesystem automatically
- **C.** UUID mounts disable quotas
- **D.** Kernel requires UUID for ext4 only

??? success "Reveal answer"
    **Correct answer: A**

    Persistent identifiers avoid wrong-disk mounts.

    **Related concepts**

    - fstab
    - UUID

    **Module focus:** M8 Storage

### Question 22

Which LVM command lists logical volumes?

**Difficulty:** Intermediate

**Options:**

- **A.** ip -br lvs
- **B.** lvs
- **C.** lsof
- **D.** lvscanctl

??? success "Reveal answer"
    **Correct answer: B**

    pvs/vgs/lvs are the core LVM report tools.

    **Related concepts**

    - LVM

    **Module focus:** M8 LVM

### Question 23

Which command shows listening TCP/UDP sockets with processes (when permitted)?

**Difficulty:** Beginner

**Options:**

- **A.** df -T
- **B.** chmod -R
- **C.** ss -tulpn
- **D.** tar -tz

??? success "Reveal answer"
    **Correct answer: C**

    ss replaced much of netstat usage.

    **Related concepts**

    - ss

    **Module focus:** M9 Networking

### Question 24

dig +short example.com primarily queries which system?

**Difficulty:** Beginner

**Options:**

- **A.** LVM metadata
- **B.** journald
- **C.** SELinux policy store
- **D.** DNS

??? success "Reveal answer"
    **Correct answer: D**

    dig is a DNS lookup utility.

    **Related concepts**

    - DNS

    **Module focus:** M9 Networking

## Section — Packages, Scheduling, Logging & Monitoring (Modules 10–12)

### Question 25

A secure default for SSH server hardening is:

**Difficulty:** Intermediate

**Options:**

- **A.** Pubkey auth on; password auth off; PermitRootLogin no
- **B.** Telnet on port 23 for compatibility
- **C.** Empty passwords for automation users
- **D.** PermitRootLogin yes with password

??? success "Reveal answer"
    **Correct answer: A**

    Keys + no root password login is a standard baseline.

    **Related concepts**

    - SSH

    **Module focus:** M9 SSH

### Question 26

On Debian/Ubuntu, which sequence refreshes indexes then installs a package?

**Difficulty:** Beginner

**Options:**

- **A.** yum update && yum install
- **B.** apt update && apt install pkg
- **C.** pacman -Syyu pkg only on Ubuntu
- **D.** brew install pkg

??? success "Reveal answer"
    **Correct answer: B**

    apt is the Debian/Ubuntu package workflow.

    **Related concepts**

    - apt

    **Module focus:** M10 Packages

### Question 27

dpkg -l is most useful to:

**Difficulty:** Beginner

**Options:**

- **A.** List block devices
- **B.** List listening ports
- **C.** List installed Debian packages
- **D.** List systemd timers

??? success "Reveal answer"
    **Correct answer: C**

    dpkg queries the local package database.

    **Related concepts**

    - dpkg

    **Module focus:** M10 Packages

### Question 28

A user crontab entry runs with whose environment/permissions?

**Difficulty:** Intermediate

**Options:**

- **A.** Always root regardless of owner
- **B.** The kernel keyring daemon
- **C.** Nobody and no groups
- **D.** The crontab owner's account (with a limited environment)

??? success "Reveal answer"
    **Correct answer: D**

    User crontabs run as that user; PATH is often minimal.

    **Related concepts**

    - cron

    **Module focus:** M11 Scheduling

### Question 29

Which systemd unit type is designed to activate another unit on a schedule?

**Difficulty:** Beginner

**Options:**

- **A.** timer
- **B.** mount
- **C.** swap
- **D.** socket only for HTTP

??? success "Reveal answer"
    **Correct answer: A**

    .timer units activate corresponding services.

    **Related concepts**

    - timers

    **Module focus:** M11 Scheduling

### Question 30

Which facility collects and queries structured binary logs on systemd hosts?

**Difficulty:** Beginner

**Options:**

- **A.** Only /var/log/wtmp
- **B.** journald (queried via journalctl)
- **C.** mkfs
- **D.** parted

??? success "Reveal answer"
    **Correct answer: B**

    journald stores journals; journalctl queries them.

    **Related concepts**

    - journald

    **Module focus:** M12 Logging

### Question 31

logrotate is primarily used to:

**Difficulty:** Beginner

**Options:**

- **A.** Balance LVM extents
- **B.** Rotate SSH host keys weekly
- **C.** Manage size/retention of log files
- **D.** Compress kernel modules

??? success "Reveal answer"
    **Correct answer: C**

    logrotate handles rotation, compression, and retention.

    **Related concepts**

    - logrotate

    **Module focus:** M12 Logging

### Question 32

vmstat 1 5 is useful during performance triage because it:

**Difficulty:** Intermediate

**Options:**

- **A.** Rewrites fstab automatically
- **B.** Starts a packet capture
- **C.** Disables swap forever
- **D.** Samples processes, memory, IO, and CPU over time

??? success "Reveal answer"
    **Correct answer: D**

    vmstat gives a rapid host health pulse.

    **Related concepts**

    - vmstat

    **Module focus:** M12 Monitoring

## Section — Security, Containers, Troubleshooting & Production (Modules 13–16)

### Question 33

Before enabling UFW on a remote VM, you should first:

**Difficulty:** Intermediate

**Options:**

- **A.** Allow SSH (OpenSSH) and keep console/out-of-band access
- **B.** Delete all users except root
- **C.** Disable the network interface
- **D.** Set PermitRootLogin yes

??? success "Reveal answer"
    **Correct answer: A**

    Allow administrative access before default deny.

    **Related concepts**

    - UFW
    - firewall

    **Module focus:** M13 Security

### Question 34

Fail2Ban typically helps by:

**Difficulty:** Intermediate

**Options:**

- **A.** Replacing TLS certificates
- **B.** Banning hosts that match abusive patterns in logs
- **C.** Growing LVM volumes
- **D.** Compiling the kernel

??? success "Reveal answer"
    **Correct answer: B**

    Fail2Ban reacts to repeated failures (e.g. SSH).

    **Related concepts**

    - Fail2Ban

    **Module focus:** M13 Security

### Question 35

SELinux or AppArmor denials should usually be handled by:

**Difficulty:** Advanced

**Options:**

- **A.** chmod 777 on /
- **B.** Disabling the firewall permanently
- **C.** Reading audit/journal denials and fixing labels/profiles properly
- **D.** Turning off SSH

??? success "Reveal answer"
    **Correct answer: C**

    Fix policy/labels; avoid blind disable in production.

    **Related concepts**

    - SELinux
    - AppArmor

    **Module focus:** M13 Security

### Question 36

Linux containers isolate processes primarily using:

**Difficulty:** Intermediate

**Options:**

- **A.** Only chroot without kernel help
- **B.** Hyper-V on all Linux hosts
- **C.** BIOS passwords
- **D.** namespaces and cgroups (plus a filesystem like OverlayFS)

??? success "Reveal answer"
    **Correct answer: D**

    Namespaces isolate; cgroups limit; overlay filesystems layer images.

    **Related concepts**

    - namespaces
    - cgroups

    **Module focus:** M14 Containers

### Question 37

First commands for a failed systemd service incident?

**Difficulty:** Intermediate

**Options:**

- **A.** systemctl status and journalctl -u with a time window
- **B.** mkfs on the root device
- **C.** Randomly chmod -R 777 /etc
- **D.** Disable journald

??? success "Reveal answer"
    **Correct answer: A**

    Status + journal is the standard first pass.

    **Related concepts**

    - troubleshooting

    **Module focus:** M15 Troubleshooting

### Question 38

High iowait in CPU stats most strongly suggests:

**Difficulty:** Advanced

**Options:**

- **A.** DNS misconfiguration only
- **B.** Tasks waiting on block I/O (disk pressure/latency)
- **C.** Too many SSH keys
- **D.** Expired apt mirrors only

??? success "Reveal answer"
    **Correct answer: B**

    wa indicates time waiting for I/O.

    **Related concepts**

    - performance
    - iowait

    **Module focus:** M15 Troubleshooting

### Question 39

A backup strategy is incomplete without:

**Difficulty:** Intermediate

**Options:**

- **A.** A colourful dashboard theme
- **B.** Disabling checksums for speed
- **C.** A tested restore drill (prove recovery)
- **D.** Storing secrets in the backup README

??? success "Reveal answer"
    **Correct answer: C**

    Untested backups are assumptions, not recovery capability.

    **Related concepts**

    - backup
    - DR

    **Module focus:** M16 Production

### Question 40

Production Linux hardening commonly includes all EXCEPT:

**Difficulty:** Advanced

**Options:**

- **A.** Least-privilege users and SSH key auth
- **B.** Host firewall with default deny inbound
- **C.** Patch cadence and monitoring/logging
- **D.** World-writable application directories for convenience

??? success "Reveal answer"
    **Correct answer: D**

    World-writable dirs violate least privilege and are not hardening.

    **Related concepts**

    - hardening

    **Module focus:** M16 Production


## Answer key (self-mark)

| Q | Ans | Q | Ans | Q | Ans | Q | Ans |
|---|-----|---|-----|---|-----|---|-----|
| 1 | A | 11 | C | 21 | A | 31 | C |
| 2 | B | 12 | D | 22 | B | 32 | D |
| 3 | C | 13 | A | 23 | C | 33 | A |
| 4 | D | 14 | B | 24 | D | 34 | B |
| 5 | A | 15 | C | 25 | A | 35 | C |
| 6 | B | 16 | D | 26 | B | 36 | D |
| 7 | C | 17 | A | 27 | C | 37 | A |
| 8 | D | 18 | B | 28 | D | 38 | B |
| 9 | A | 19 | C | 29 | A | 39 | C |
| 10 | B | 20 | D | 30 | B | 40 | D |

**Distribution:** A=10, B=10, C=10, D=10.

## Recommended study areas

| If you missed… | Revise |
|----------------|--------|
| Q1–8 | Fundamentals, boot, FHS, commands, filesystem tutorials |
| Q9–16 | Users/permissions, text tools, process management |
| Q17–24 | systemd, storage/LVM, networking/SSH |
| Q25–32 | Packages, cron/timers, logging, vmstat/iostat |
| Q33–40 | Firewalls/LSM, containers, triage, hardening/backup |

## Related

- Path: [Linux for Cloud & DevOps](../learning-paths/linux-administrator/)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
- Interview: [Linux Interview Prep](../interview/linux.md)
- Lab: [Linux Ops Toolkit](../labs/linux-ops-toolkit-lab.md)
- Lab: [Production Incident Triage](../labs/linux-production-incident-triage.md)
