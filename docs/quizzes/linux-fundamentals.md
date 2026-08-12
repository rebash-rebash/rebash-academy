---
title: "Quiz — Linux Fundamentals"
description: "40-question Linux fundamentals quiz covering FHS, permissions, systemd, logs, triage, and production hardening judgement."
difficulty: intermediate
estimated_time: "45–60 min"
passing_score: "70% (28/40)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - linux
  - assessment
comments: false
---

# Quiz — Linux Fundamentals

## Quiz Overview

Validate core Linux administration skills used daily by DevOps and SRE engineers: filesystem layout, permissions, processes, systemd, logging, and incident judgement.

| Attribute | Value |
|-----------|--------|
| Topic | Linux |
| Questions | 40 |
| Passing score | 70% (28 correct) |
| Estimated time | 45–60 minutes |
| Format | Multiple choice (single answer) |

!!! tip "How to use this quiz"
    Select an answer for each question, then **Submit quiz** for a scored result. Progress is saved in this browser. Explanations unlock after you submit.

!!! tip "Rewritten course quiz"
    For the **Linux for Cloud & DevOps Engineers** 16-module track, prefer [Linux for Cloud & DevOps Fundamentals](linux-for-cloud-devops-fundamentals.md).

## Learning Objectives

This quiz assesses whether you can:

- [ ] Explain kernel vs user space and FHS basics
- [ ] Apply permissions, ownership, and sudo safely
- [ ] Operate systemd units and journald
- [ ] Triage failed services, disk pressure, and port conflicts
- [ ] Choose hardening and backup patterns that match production norms

## Section 1 — Fundamentals

### Question 1

What is the primary role of the Linux kernel?

**Difficulty:** Beginner

**Options:**

- **A.** Manage hardware, processes, memory, and system calls for user space
- **B.** Provide a graphical desktop environment
- **C.** Replace Bash as the default shell
- **D.** Store user documents in /home only

??? success "Reveal answer"
    **Correct answer: A**

    The kernel is the core of the OS: hardware abstraction, scheduling, memory, and the system-call interface. Desktops and shells are user-space components.

    **Related concepts**

    - Kernel vs user space
    - System calls
    - Process scheduling

### Question 2

Which path is the conventional location for third-party or locally installed software trees on many Linux systems?

**Difficulty:** Beginner

**Options:**

- **A.** /var/log
- **B.** /proc
- **C.** /opt
- **D.** /dev

??? success "Reveal answer"
    **Correct answer: C**

    `/opt` is commonly used for optional/add-on application packages. `/var/log` is logs, `/proc` is process/kernel info, `/dev` is device nodes.

    **Related concepts**

    - FHS
    - /opt
    - Filesystem hierarchy

### Question 3

What does the execute bit on a directory allow a user to do?

**Difficulty:** Beginner

**Options:**

- **A.** List all filenames without reading them
- **B.** Delete the directory itself without write on the parent
- **C.** Change ownership of every file inside
- **D.** Traverse into the directory (access files by known name if other permissions allow)

??? success "Reveal answer"
    **Correct answer: D**

    On directories, execute means search/traverse. Listing needs read; creating/deleting entries needs write on the directory.

    **Related concepts**

    - Directory permissions
    - rwx on directories

### Question 4

Which command shows your effective user id, groups, and supplementary groups?

**Difficulty:** Beginner

**Options:**

- **A.** whoami only
- **B.** id
- **C.** uname -a
- **D.** pwd

??? success "Reveal answer"
    **Correct answer: B**

    `id` prints uid, gid, and groups. `whoami` is only the username; `uname` is kernel/system identity.

    **Related concepts**

    - Users and groups
    - id

### Question 5

What is the difference between a hard link and a symbolic link?

**Difficulty:** Beginner

**Options:**

- **A.** A hard link is another directory entry to the same inode; a symlink is a special file pointing to a path
- **B.** Hard links can cross filesystems; symlinks cannot
- **C.** Symlinks only work for directories; hard links only for devices
- **D.** They are identical on ext4

??? success "Reveal answer"
    **Correct answer: A**

    Hard links share an inode (same filesystem). Symlinks store a path and can cross filesystems.

    **Related concepts**

    - Inodes
    - ln
    - ln -s

### Question 6

Which signal is the default sent by `kill <pid>` when no signal is specified?

**Difficulty:** Beginner

**Options:**

- **A.** SIGKILL (9)
- **B.** SIGSTOP
- **C.** SIGTERM (15)
- **D.** SIGHUP

??? success "Reveal answer"
    **Correct answer: C**

    Default is SIGTERM, allowing graceful shutdown. SIGKILL cannot be caught and should be a last resort.

    **Related concepts**

    - Signals
    - kill

### Question 7

What does systemd use as the primary unit type for long-running daemons?

**Difficulty:** Beginner

**Options:**

- **A.** .timer units only
- **B.** .mount units exclusively
- **C.** .socket units replace all services
- **D.** .service units

??? success "Reveal answer"
    **Correct answer: D**

    Daemons are typically managed as `.service` units. Timers, mounts, and sockets are other unit types.

    **Related concepts**

    - systemd
    - Unit files

### Question 8

Which command is the modern preferred way to follow logs for a systemd service named `nginx`?

**Difficulty:** Beginner

**Options:**

- **A.** tail -f /var/log/messages only
- **B.** journalctl -u nginx -f
- **C.** dmesg -w
- **D.** cat /proc/nginx

??? success "Reveal answer"
    **Correct answer: B**

    `journalctl -u <unit> -f` follows that unit’s journal entries.

    **Related concepts**

    - journalctl
    - Logging

### Question 9

In a classic Unix permission string `-rwxr-xr--`, what can “others” do?

**Difficulty:** Beginner

**Options:**

- **A.** Read only
- **B.** Read, write, and execute
- **C.** Read and execute
- **D.** Nothing

??? success "Reveal answer"
    **Correct answer: A**

    The last triad is `r--` → others may read only.

    **Related concepts**

    - chmod
    - Permission triads

### Question 10

What is the purpose of `/etc/sudoers` (or files under `/etc/sudoers.d`)?

**Difficulty:** Beginner

**Options:**

- **A.** Store user passwords in plaintext
- **B.** Configure SSH host keys
- **C.** Define which users/groups may run commands as root or others via sudo
- **D.** Set the default shell for root only

??? success "Reveal answer"
    **Correct answer: C**

    sudoers controls privilege elevation policy. Edit with `visudo` to avoid syntax lockouts.

    **Related concepts**

    - sudo
    - Least privilege
    - visudo

## Section 2 — Practical Knowledge

### Question 11

You need to find all world-writable files under `/var/www` for a hardening review. Which approach is most appropriate?

**Difficulty:** Intermediate

**Options:**

- **A.** ls -la /var/www
- **B.** chmod -R 777 /var/www
- **C.** cat /etc/passwd
- **D.** find /var/www -type f -perm -0002

??? success "Reveal answer"
    **Correct answer: D**

    `find … -perm -0002` locates files with the others-write bit.

    **Related concepts**

    - find
    - Permissions audit

### Question 12

A service fails immediately after `systemctl start`. What should you run first for evidence?

**Difficulty:** Intermediate

**Options:**

- **A.** reboot
- **B.** systemctl status <unit> and journalctl -u <unit> -e
- **C.** rm -rf /etc/systemd
- **D.** kill -9 1

??? success "Reveal answer"
    **Correct answer: B**

    Status and journal give exit codes, paths, and permission errors.

    **Related concepts**

    - Incident triage
    - journalctl
    - systemctl

### Question 13

Which `chmod` symbolic mode adds execute for user and group on `deploy.sh`?

**Difficulty:** Intermediate

**Options:**

- **A.** chmod ug+x deploy.sh
- **B.** chmod a+s deploy.sh
- **C.** chmod o+w deploy.sh
- **D.** chmod 000 deploy.sh

??? success "Reveal answer"
    **Correct answer: A**

    `ug+x` adds execute for user and group without forcing a full octal mode.

    **Related concepts**

    - chmod symbolic mode

### Question 14

Which command helps identify large directories under `/var`?

**Difficulty:** Intermediate

**Options:**

- **A.** ps aux
- **B.** ip addr
- **C.** du -h --max-depth=1 /var | sort -h
- **D.** systemctl list-timers

??? success "Reveal answer"
    **Correct answer: C**

    `du` summarises disk usage by directory.

    **Related concepts**

    - du
    - Disk pressure

### Question 15

What does `systemctl enable nginx` do?

**Difficulty:** Intermediate

**Options:**

- **A.** Starts nginx once and disables it on reboot
- **B.** Upgrades the nginx package
- **C.** Opens port 80 in the firewall
- **D.** Creates the wants/ symlinks so nginx starts on boot (per unit install section)

??? success "Reveal answer"
    **Correct answer: D**

    enable configures boot-time start via unit WantedBy relationships.

    **Related concepts**

    - systemctl enable

### Question 16

Which crontab field set runs a job at 02:30 every day?

**Difficulty:** Intermediate

**Options:**

- **A.** 2 30 * * *
- **B.** 30 2 * * *
- **C.** * * 2 30 *
- **D.** 30 * 2 * *

??? success "Reveal answer"
    **Correct answer: B**

    Order is minute hour day-of-month month day-of-week → `30 2 * * *`.

    **Related concepts**

    - cron

### Question 17

You need lines containing `ERROR` in `app.log`, case-insensitive. Best simple command?

**Difficulty:** Beginner

**Options:**

- **A.** grep -i ERROR app.log
- **B.** rm app.log
- **C.** chmod 777 app.log
- **D.** ln -s app.log

??? success "Reveal answer"
    **Correct answer: A**

    `grep -i` matches case-insensitively.

    **Related concepts**

    - grep
    - Log analysis

### Question 18

What is a reliable way to see which process holds TCP port 8080?

**Difficulty:** Intermediate

**Options:**

- **A.** cat /etc/services only
- **B.** echo 8080
- **C.** ss -ltnp | grep 8080 (or lsof -iTCP:8080)
- **D.** uname -r

??? success "Reveal answer"
    **Correct answer: C**

    `ss`/`lsof` show listeners and owning processes.

    **Related concepts**

    - ss
    - lsof

### Question 19

A script must fail fast if any command fails. Which Bash option helps?

**Difficulty:** Intermediate

**Options:**

- **A.** set +x only
- **B.** alias rm=rm
- **C.** ulimit -n 1
- **D.** set -e (and often set -u -o pipefail)

??? success "Reveal answer"
    **Correct answer: D**

    `set -e` exits on failure; combining with `-u` and `pipefail` is common.

    **Related concepts**

    - Bash
    - set -e

### Question 20

Which permission bit on a directory makes files deletable only by their owner (or root) — classic `/tmp` behaviour?

**Difficulty:** Intermediate

**Options:**

- **A.** setuid
- **B.** sticky bit (t)
- **C.** setgid
- **D.** immutable attribute only

??? success "Reveal answer"
    **Correct answer: B**

    The sticky bit on directories restricts unlinking to file owner/root.

    **Related concepts**

    - Sticky bit
    - /tmp

## Section 3 — Scenario-Based Questions

### Question 21

PagerDuty: `rebash-api` failed. journalctl reports `Permission denied` opening the ExecStart script. Best next step?

**Difficulty:** Intermediate

**Options:**

- **A.** Check ownership/mode of the script and the user the unit runs as (User=)
- **B.** Open all firewall ports
- **C.** Delete the unit file
- **D.** Disable SELinux permanently without investigation

??? success "Reveal answer"
    **Correct answer: A**

    Permission denied on the executable path implicates ownership/mode vs the service user.

    **Related concepts**

    - systemd User=
    - Permissions

### Question 22

Disk is 100% on `/`. `du` shows `/var/log` huge. Safest immediate mitigation while preserving evidence?

**Difficulty:** Intermediate

**Options:**

- **A.** rm -rf /
- **B.** dd if=/dev/zero of=/var/log/big
- **C.** Rotate/compress old logs, truncate only after copying critical evidence, fix retention
- **D.** chmod -R 777 /var/log

??? success "Reveal answer"
    **Correct answer: C**

    Free space via log rotation/cleanup with care for forensics.

    **Related concepts**

    - Disk full
    - logrotate

### Question 23

A timer-based job did not run. `systemctl list-timers` shows the timer inactive. Likely check?

**Difficulty:** Intermediate

**Options:**

- **A.** Whether Docker is installed
- **B.** Whether /etc/hosts contains google.com
- **C.** Whether the GPU driver exists
- **D.** Whether the `.timer` unit is enabled/started and OnCalendar= is valid

??? success "Reveal answer"
    **Correct answer: D**

    Timers must be enabled/started; calendar expressions and related service units matter.

    **Related concepts**

    - systemd timers

### Question 24

SSH works from your laptop but CI fails with `Permission denied (publickey)`. Most likely?

**Difficulty:** Intermediate

**Options:**

- **A.** The server has no SSH daemon
- **B.** The runner lacks the authorised private key or uses the wrong user
- **C.** iptables blocks ICMP only
- **D.** DNS TTL is 86400

??? success "Reveal answer"
    **Correct answer: B**

    Publickey failures usually mean missing/incorrect key material or wrong account.

    **Related concepts**

    - SSH keys
    - CI authentication

### Question 25

`htop` shows one process at 100% CPU after a release. Sound first step?

**Difficulty:** Intermediate

**Options:**

- **A.** Identify PID, inspect command line/logs, thread state; consider SIGTERM after evidence
- **B.** kill -9 -1
- **C.** Disable the NIC
- **D.** Format /home

??? success "Reveal answer"
    **Correct answer: A**

    Diagnose before killing broadly.

    **Related concepts**

    - CPU saturation
    - Process triage

### Question 26

A junior proposes `chmod -R 777 /var/www` to fix the site. What do you recommend?

**Difficulty:** Beginner

**Options:**

- **A.** Agree — 777 is fine in production
- **B.** World-writable is required for nginx
- **C.** Set owner/group correctly and use the least mode that works (often 755 dirs / 644 files)
- **D.** Put the site in /proc

??? success "Reveal answer"
    **Correct answer: C**

    777 is a common anti-pattern. Fix ownership and minimal modes.

    **Related concepts**

    - Least privilege

### Question 27

You need elevation but policy forbids sharing the root password. Appropriate tool?

**Difficulty:** Beginner

**Options:**

- **A.** Write the root password to Slack
- **B.** Disable PAM
- **C.** chmod 777 /etc/shadow
- **D.** sudo -i (if authorised) or sudo for specific commands

??? success "Reveal answer"
    **Correct answer: D**

    sudo provides audited, policy-controlled elevation.

    **Related concepts**

    - sudo
    - Access control

### Question 28

Application writes to `/var/lib/myapp` but the unit uses `ProtectSystem=strict`. What happens?

**Difficulty:** Advanced

**Options:**

- **A.** Nothing — ProtectSystem is cosmetic
- **B.** Writes outside allowed paths fail; use ReadWritePaths= (or relax carefully)
- **C.** The kernel panics
- **D.** SELinux is disabled

??? success "Reveal answer"
    **Correct answer: B**

    systemd sandboxing restricts filesystem writes.

    **Related concepts**

    - systemd hardening
    - ProtectSystem

### Question 29

SSH latency is fine but authentication takes ~10s. A common cause?

**Difficulty:** Advanced

**Options:**

- **A.** Reverse DNS / GSSAPI / UseDNS delays in sshd
- **B.** MTU 9000 only
- **C.** Missing /etc/hostname always blocks forever
- **D.** Too much free RAM

??? success "Reveal answer"
    **Correct answer: A**

    SSH can stall on reverse DNS or auth method negotiation.

    **Related concepts**

    - sshd
    - UseDNS

### Question 30

Prove a package is installed and which version on Debian/Ubuntu. Best pair?

**Difficulty:** Intermediate

**Options:**

- **A.** brew list
- **B.** systemctl reboot
- **C.** dpkg -l | grep pkg ; apt-cache policy pkg
- **D.** tar -tzf

??? success "Reveal answer"
    **Correct answer: C**

    dpkg/apt query package state on Debian family systems.

    **Related concepts**

    - Package management
    - dpkg

## Section 4 — Troubleshooting

### Question 31

Unit is `active (running)` but curl fails; `ss` shows nothing listening. Likely category?

**Difficulty:** Intermediate

**Options:**

- **A.** The moon phase
- **B.** ext4 fragmentation only
- **C.** Missing swap always
- **D.** Process is up but bound to a different address/port or crashed child listener

??? success "Reveal answer"
    **Correct answer: D**

    A parent can be running while the listener failed or binds elsewhere.

    **Related concepts**

    - Listen address
    - Health checks vs process state

### Question 32

`journalctl -u app` shows ExecStart path not found. Fix?

**Difficulty:** Beginner

**Options:**

- **A.** chmod 777 /
- **B.** Correct the path in the unit, daemon-reload, restart
- **C.** Delete journald
- **D.** Disable the unit forever without fixing

??? success "Reveal answer"
    **Correct answer: B**

    Broken ExecStart paths are fixed in the unit file followed by reload/restart.

    **Related concepts**

    - Unit files
    - daemon-reload

### Question 33

After `apt upgrade`, a service will not start due to a missing shared library. What helps confirm?

**Difficulty:** Advanced

**Options:**

- **A.** ldd on the binary / checking package dependencies
- **B.** ping 8.8.8.8 only
- **C.** changing wallpaper
- **D.** increasing nice value randomly

??? success "Reveal answer"
    **Correct answer: A**

    `ldd` and dependency packages reveal missing libs after upgrades.

    **Related concepts**

    - Shared libraries
    - ldd

### Question 34

`df -h` shows space free but `touch` fails with “No space left”. Likely?

**Difficulty:** Advanced

**Options:**

- **A.** DNS failure
- **B.** Wrong timezone
- **C.** Inode exhaustion (`df -i`)
- **D.** Caps Lock

??? success "Reveal answer"
    **Correct answer: C**

    Exhausted inodes can block new files while byte space remains.

    **Related concepts**

    - Inodes
    - df -i

### Question 35

A privileged port bind fails for a non-root service. Modern approach besides running as root?

**Difficulty:** Advanced

**Options:**

- **A.** Always chmod 777 the binary
- **B.** Disable the firewall globally
- **C.** Bind to port 22
- **D.** Use capabilities (e.g. CAP_NET_BIND_SERVICE), authbind, or reverse proxy on 80/443

??? success "Reveal answer"
    **Correct answer: D**

    Prefer capabilities or a front proxy over running full root.

    **Related concepts**

    - Capabilities
    - Privilege separation

## Section 5 — Architecture

### Question 36

For a single Linux VM hosting a public HTTPS API, which layering is most sound?

**Difficulty:** Intermediate

**Options:**

- **A.** App as root on :443 with 777 configs
- **B.** TLS terminator/reverse proxy + unprivileged app on localhost + firewall allow 80/443 only
- **C.** Disable SSH and hope
- **D.** Store secrets in a world-readable gist

??? success "Reveal answer"
    **Correct answer: B**

    Terminate TLS at a hardened edge, run the app with least privilege, restrict exposure.

    **Related concepts**

    - Defence in depth
    - Reverse proxy

### Question 37

Why separate `/var` (or a dedicated log volume) on production servers?

**Difficulty:** Intermediate

**Options:**

- **A.** Contain log growth so a runaway log cannot fill the root filesystem as easily
- **B.** Aesthetic reasons only
- **C.** Makes kernel upgrades impossible
- **D.** Required by PCI to use XFS only

??? success "Reveal answer"
    **Correct answer: A**

    Filesystem separation limits blast radius of growth and simplifies backups.

    **Related concepts**

    - Filesystem layout
    - Capacity isolation

### Question 38

Which backup statement is most accurate for Linux system state?

**Difficulty:** Intermediate

**Options:**

- **A.** RAID is a backup
- **B.** Snapshots without restore tests are enough forever
- **C.** Backups need retention, restore tests, and off-box copies — RAID is availability not backup
- **D.** Only back up /tmp

??? success "Reveal answer"
    **Correct answer: C**

    RAID/redundancy is not a backup. Test restores.

    **Related concepts**

    - Backup
    - Disaster recovery

### Question 39

For SSH administration at scale, which design is preferable?

**Difficulty:** Advanced

**Options:**

- **A.** Shared root password on a wiki
- **B.** Telnet with OTP sticky notes
- **C.** FTP to edit /etc
- **D.** Per-user keys or SSO/cert auth, sudo for elevation, bastion/session recording as needed

??? success "Reveal answer"
    **Correct answer: D**

    Key/cert auth, individual accounts, and audited sudo are baseline.

    **Related concepts**

    - SSH hardening
    - Bastion

### Question 40

A cost-conscious team runs batch jobs nightly on systemd hosts. Best approach?

**Difficulty:** Intermediate

**Options:**

- **A.** Busy-loop in a screen session
- **B.** systemd `.timer` + `.service` with clear logs and failure alerts
- **C.** Manual login each night
- **D.** Disable NTP so cron drifts

??? success "Reveal answer"
    **Correct answer: B**

    Timers integrate with journald and dependency management.

    **Related concepts**

    - Timers
    - Batch jobs

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 36–40 | Excellent | Ready for interviews and labs at this track level |
| 28–35 | Good | Pass — revise weak sections, then retry |
| 20–27 | Needs improvement | Revisit tutorials for missed topics before labs |
| ≤19 | Restart foundations | Work the track in order, then retake |

**Total questions:** 40 · **Passing score:** 28 (70%)

## Recommended Study Areas

Misses in Sections 1–2 → revisit early Linux tutorials. Misses in 3–4 → practise the Linux production incident lab. Misses in 5 → re-read security hardening and troubleshooting tutorials.

- Track: [Linux](../linux/index.md)
- Lab: [Linux Production Incident Triage](../labs/linux-production-incident-triage.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
- Interview prep: [Linux](../interview/linux.md)
- Path: [DevOps Engineer](../learning-paths/devops-engineer/)

## Interview Connection

Interviewers often ask permission bits on directories, systemd failure triage, journalctl workflows, and “disk full but df looks fine” (inodes). Be ready to narrate a service-down incident end-to-end.

## References

1. [systemd documentation](https://www.freedesktop.org/software/systemd/man/)
2. [Linux man-pages project](https://www.kernel.org/doc/man-pages/)
3. [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)
