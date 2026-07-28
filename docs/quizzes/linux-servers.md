---
title: "Quiz — Linux Servers"
description: "25-question advanced quiz on Linux app servers: nginx, TLS, LVM, backups, exposure, and baseline operations."
difficulty: advanced
estimated_time: "30–40 min"
passing_score: "70% (18/25)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - linux
  - servers
  - assessment
comments: false
---

# Quiz — Linux Servers

## Quiz Overview

Assess Module 7 Advanced Linux Servers skills: baseline, nginx reverse proxy, TLS, LVM/fstab, backups, and exposure control.

| Attribute | Value |
|-----------|--------|
| Topic | Linux servers |
| Questions | 25 |
| Passing score | 70% (18 correct) |
| Estimated time | 30–40 minutes |

!!! tip "How to use this quiz"
    Attempt without peeking. Use Reveal answer only after you choose.

## Learning Objectives

- [ ] Choose correct bind/exposure patterns for app servers
- [ ] Operate nginx proxy and TLS basics
- [ ] Reason about LVM/fstab and backup/restore proof
- [ ] Avoid common hardening lockouts

## Section 1 — Fundamentals

### Question 1

On a hardened app server, where should the application process typically listen?

**Difficulty:** Beginner

**Options:**

- **A.** 127.0.0.1 on a private port behind nginx
- **B.** 0.0.0.0:8080 publicly
- **C.** Only on IPv6 link-local
- **D.** UDP 53

??? success "Reveal answer"
    **Correct answer: A**

    Localhost bind keeps the app off the public exposure path; nginx owns 80/443.

    **Related concepts**

    - Bind address
    - Reverse proxy

### Question 2

Which command best lists TCP listening sockets with processes?

**Difficulty:** Beginner

**Options:**

- **A.** ping -a
- **B.** chmod 777
- **C.** sudo ss -tulpn
- **D.** tar -tzf

??? success "Reveal answer"
    **Correct answer: C**

    ss replaces netstat for socket inspection.

    **Related concepts**

    - ss

### Question 3

What does `nginx -t` do?

**Difficulty:** Beginner

**Options:**

- **A.** Terminates TLS
- **B.** Truncates access logs
- **C.** Opens port 443
- **D.** Tests configuration syntax before reload

??? success "Reveal answer"
    **Correct answer: D**

    Always test before reload.

    **Related concepts**

    - nginx

### Question 4

A curl to nginx /api returns 502 while curl to 127.0.0.1:18080 fails. Likely?

**Difficulty:** Intermediate

**Options:**

- **A.** DNS NXDOMAIN only
- **B.** Upstream app is down or not listening
- **C.** ext4 fragmentation
- **D.** Wrong timezone wallpaper

??? success "Reveal answer"
    **Correct answer: B**

    502 usually means upstream problem.

    **Related concepts**

    - 502
    - Upstream

### Question 5

Self-signed certificates in labs primarily lack what?

**Difficulty:** Beginner

**Options:**

- **A.** Public CA trust in browsers
- **B.** Encryption capability
- **C.** Private keys
- **D.** Ports

??? success "Reveal answer"
    **Correct answer: A**

    Self-signed encrypts but is not publicly trusted.

    **Related concepts**

    - TLS

### Question 6

Preferred fstab device identifier?

**Difficulty:** Intermediate

**Options:**

- **A.** /dev/sdb1 always
- **B.** IDE bus number
- **C.** UUID=...
- **D.** Random major:minor

??? success "Reveal answer"
    **Correct answer: C**

    UUIDs survive device rename.

    **Related concepts**

    - fstab
    - UUID

### Question 7

After `lvextend`, ext4 still shows old size until you?

**Difficulty:** Intermediate

**Options:**

- **A.** Reboot BIOS
- **B.** Delete fstab
- **C.** Disable nginx
- **D.** Run resize2fs (online grow)

??? success "Reveal answer"
    **Correct answer: D**

    Grow the filesystem after the LV.

    **Related concepts**

    - LVM
    - resize2fs

### Question 8

What proves a backup is useful?

**Difficulty:** Beginner

**Options:**

- **A.** File exists on disk
- **B.** Checksum verify plus successful restore drill
- **C.** Cron ran once
- **D.** Screenshot of ls

??? success "Reveal answer"
    **Correct answer: B**

    Untested backups fail incidents.

    **Related concepts**

    - Backup
    - Restore

### Question 9

UFW enable without allowing SSH often causes?

**Difficulty:** Advanced

**Options:**

- **A.** Admin lockout from remote SSH
- **B.** Faster TLS
- **C.** Automatic LVM extend
- **D.** Chrony sync

??? success "Reveal answer"
    **Correct answer: A**

    Allow OpenSSH first; keep console.

    **Related concepts**

    - UFW
    - Lockout

### Question 10

chrony/time sync matters for TLS because?

**Difficulty:** Intermediate

**Options:**

- **A.** Certificates are timezone files
- **B.** nginx ignores time
- **C.** Validity windows depend on correct clock
- **D.** SSH disables NTP

??? success "Reveal answer"
    **Correct answer: C**

    Skew breaks cert validation.

    **Related concepts**

    - NTP
    - TLS


## Section 2 — Practical Knowledge

### Question 11

sites-enabled on Debian/Ubuntu usually contains?

**Difficulty:** Beginner

**Options:**

- **A.** Binary modules only
- **B.** Private keys only
- **C.** LVM metadata
- **D.** Symlinks to sites-available configs

??? success "Reveal answer"
    **Correct answer: D**

    Enable via symlink pattern.

    **Related concepts**

    - nginx

### Question 12

Automatic-Reboot true on a single stateful VM is risky because?

**Difficulty:** Intermediate

**Options:**

- **A.** It upgrades DNS
- **B.** Unexpected downtime without drain/window
- **C.** It disables SSH keys
- **D.** It formats /boot nightly

??? success "Reveal answer"
    **Correct answer: B**

    Need change windows on singleton VMs.

    **Related concepts**

    - Unattended upgrades

### Question 13

PV → VG → LV describes?

**Difficulty:** Beginner

**Options:**

- **A.** LVM layering
- **B.** nginx stages
- **C.** TLS handshake
- **D.** systemd targets only

??? success "Reveal answer"
    **Correct answer: A**

    Physical → group → logical.

    **Related concepts**

    - LVM

### Question 14

Which ports are typical public edge for this design?

**Difficulty:** Beginner

**Options:**

- **A.** 18080, 5432, 6379
- **B.** Only 8080
- **C.** 22, 80, 443
- **D.** 137–139

??? success "Reveal answer"
    **Correct answer: C**

    SSH + HTTP/HTTPS; app private.

    **Related concepts**

    - Exposure matrix

### Question 15

openssl x509 -enddate helps you?

**Difficulty:** Beginner

**Options:**

- **A.** Extend LVM
- **B.** Ban SSH IPs
- **C.** Compile nginx
- **D.** See certificate expiry

??? success "Reveal answer"
    **Correct answer: D**

    Monitor notAfter.

    **Related concepts**

    - OpenSSL

### Question 16

rsync --delete danger?

**Difficulty:** Intermediate

**Options:**

- **A.** It encrypts twice
- **B.** Can wipe backup target to mirror source deletions
- **C.** Disables checksums forever
- **D.** Requires IPv6

??? success "Reveal answer"
    **Correct answer: B**

    Dry-run first.

    **Related concepts**

    - rsync

### Question 17

proxy_pass to http://127.0.0.1:18080/ from location /api/ is for?

**Difficulty:** Intermediate

**Options:**

- **A.** Reverse proxy to local upstream
- **B.** Static files only
- **C.** Firewall bypass on WAN
- **D.** LVM snapshots

??? success "Reveal answer"
    **Correct answer: A**

    Core reverse proxy pattern.

    **Related concepts**

    - nginx
    - proxy_pass


## Section 3 — Scenarios & Operations

### Question 18

fail2ban primarily mitigates?

**Difficulty:** Beginner

**Options:**

- **A.** Disk full
- **B.** Certificate expiry
- **C.** Brute-force auth attempts (e.g. sshd)
- **D.** Slow DNS

??? success "Reveal answer"
    **Correct answer: C**

    Ban repeat offenders.

    **Related concepts**

    - fail2ban

### Question 19

Loop-backed LVM labs are used to?

**Difficulty:** Advanced

**Options:**

- **A.** Replace cloud disks always
- **B.** Speed up TLS
- **C.** Disable fstab
- **D.** Practise safely without risking system disks

??? success "Reveal answer"
    **Correct answer: D**

    Safe pedagogy.

    **Related concepts**

    - LVM lab

### Question 20

3-2-1 backup rule emphasises?

**Difficulty:** Intermediate

**Options:**

- **A.** One disk only
- **B.** Multiple copies/media and off-site copy
- **C.** RAID equals backup
- **D.** Snapshots only in RAM

??? success "Reveal answer"
    **Correct answer: B**

    Industry practice.

    **Related concepts**

    - Backup

### Question 21

server_tokens off reduces?

**Difficulty:** Beginner

**Options:**

- **A.** Version disclosure in nginx headers
- **B.** CPU
- **C.** Disk inodes
- **D.** SSH banner colour

??? success "Reveal answer"
    **Correct answer: A**

    Slight hardening.

    **Related concepts**

    - nginx security

### Question 22

When certbot HTTP-01 fails on pure localhost?

**Difficulty:** Intermediate

**Options:**

- **A.** openssl is broken
- **B.** UFW must disable lo
- **C.** No public DNS/HTTP challenge path — use self-signed/internal CA for lab
- **D.** LVM full

??? success "Reveal answer"
    **Correct answer: C**

    ACME needs reachability.

    **Related concepts**

    - Let's Encrypt

### Question 23

systemd-analyze blame helps baseline by?

**Difficulty:** Intermediate

**Options:**

- **A.** Rotating nginx logs
- **B.** Issuing certificates
- **C.** Creating VGs
- **D.** Listing slow boot units

??? success "Reveal answer"
    **Correct answer: D**

    Boot cost visibility.

    **Related concepts**

    - systemd-analyze

### Question 24

Connection refused on :443 but nginx active — check?

**Difficulty:** Advanced

**Options:**

- **A.** Only dpkg holds
- **B.** Listen directives / firewall / wrong IP
- **C.** tar format
- **D.** Python GIL

??? success "Reveal answer"
    **Correct answer: B**

    Socket and path triage.

    **Related concepts**

    - Troubleshooting

### Question 25

Least privilege sudo for deploy user means?

**Difficulty:** Beginner

**Options:**

- **A.** Allow-list specific commands (e.g. systemctl reload nginx)
- **B.** NOPASSWD ALL
- **C.** Share root password
- **D.** Disable sudo logging

??? success "Reveal answer"
    **Correct answer: A**

    Command allow-lists.

    **Related concepts**

    - sudoers

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 23–25 | Excellent | Ready for the app-server lab and interviews |
| 18–22 | Good | Pass — revise weak Module 7 tutorials |
| 12–17 | Needs improvement | Revisit nginx/TLS/LVM labs |
| ≤11 | Restart Module 7 | Work tutorials 21–25 in order |

**Total questions:** 25 · **Passing score:** 18 (70%)

## Recommended Study Areas

- [Linux Module 7](../linux/index.md)
- Lab: [Linux App Server from Zero](../labs/linux-app-server-from-zero.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)
- Interview: [Linux](../interview/linux.md)

## Interview Connection

Expect bind-address, nginx 502, certificate expiry, fstab UUID, and backup-restore questions. Use your Module 7 lab story.

## References

1. [nginx documentation](https://nginx.org/en/docs/)
2. [Ubuntu Server docs](https://ubuntu.com/server/docs)
3. [LVM HOWTO](https://tldp.org/HOWTO/LVM-HOWTO/)
