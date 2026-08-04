---
title: "Users, Groups, and sudo"
description: "Linux identity users, groups, sudo, useradd, visudo — plain language first, then a real least-privilege lab."
difficulty: beginner
estimated_time: "55–70 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 4 · Users & Permissions"
career_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - users
  - groups
  - sudo
  - identity
  - beginners
prerequisites:
  - linux/disk-usage-and-file-attributes
next:
  - linux/permissions-acls-and-special-bits
related:
  - labs/linux-users-permissions-lab
  - aws/iam-identity-access-and-organizations
labs:
  - labs/linux-users-permissions-lab
interview: interview/linux
comments: false
---

# Users, Groups, and sudo

## Overview

Every Linux server asks three questions on every login:

1. **Who are you?** → **user** (account with a user ID, or **UID**)
2. **Which teams do you belong to?** → **groups** (group ID, or **GID**)
3. **May you run admin commands?** → **sudo** (“superuser do”)

When you SSH to a cloud VM, you log in as a **user** — not as “Linux itself”. File permissions, services, containers, and deploy scripts all depend on this identity layer. Wrong users or groups cause `Permission denied`, failed CI jobs, or accounts with far more power than they should have.

**Plain problem:** Many people stay logged in as **root** (full admin) because it “just works”. In production, one compromised script then owns the entire server. Good teams use normal users + small **sudo** rules.

This is **Tutorial 6** in **Module 4: Users & Permissions** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

!!! warning "Lab safety"
    Create and delete **lab users only** on a **practice VM**. Do **not** run user-management tasks on a shared production server.

## Prerequisites

- [Disk Usage and File Attributes](disk-usage-and-file-attributes.md)
- A **practice Ubuntu 22.04/24.04 VM** where you already have `sudo`
- Willingness to create temporary lab users (`rebash-alice`, `rebash-svc`, …)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain users, groups, and sudo using `/etc/passwd`, `/etc/group`, and `/etc/sudoers.d/`
- [ ] Create a login user and a system (service) account with the correct shell
- [ ] Add a user to a group with `usermod -aG` without removing other groups
- [ ] Create a limited sudoers file with `visudo` and prove it with `sudo -l`
- [ ] Demonstrate both **allow** and **deny** for sudo — then clean up lab accounts

## Architecture

Linux identity sits between people (or automation) and the kernel. Account files store UID/GID. **sudo** decides which privileged commands are allowed. Files and processes then run as those identities.

![Linux permission model — users, groups, sudo](../assets/excalidraw/linux-permission-model.svg)

## Theory

### The problem (before any jargon)

Imagine three people on a small team:

- **Alice** needs to restart one application service
- **Bob** owns files for a background app — but must **not** log in interactively
- **You** need to prove Alice **cannot** become full root

If everyone shares one root password, one stolen laptop key opens everything. Linux separates **identities** and gives **small permission lists** — the same idea as AWS Identity and Access Management (IAM), but on the server itself.

### Users and groups — simple words

**Analogy:** A **user** is an employee badge. A **group** is a department badge shared by many employees. The **UID/GID** are the numeric IDs on the badge — storage systems care about numbers, not names.

| Term | Plain meaning | Where stored |
|------|---------------|--------------|
| **User** | Account with UID, home folder, login shell | `/etc/passwd`, `/etc/shadow` |
| **Group** | Named team with GID and member list | `/etc/group` |
| **Primary group** | Default group for new files the user creates | Field in `/etc/passwd` |
| **Secondary groups** | Extra teams (for example `deploy`, `docker`) | `/etc/group` membership |
| **System user** | Low UID, often `nologin` shell — for apps, not people | `/etc/passwd` |
| **root** | UID 0 — full admin | Special account |

**What you can say in an interview:** “Humans get login shells and limited sudo. Services get system accounts with `nologin` so nobody SSHs in as the app user.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
id
getent passwd "$USER"
getent group sudo
```

### What is sudo?

**sudo** lets an allowed user run **specific commands as another user** (usually root), based on rules in `/etc/sudoers` and files under `/etc/sudoers.d/`.

**Analogy:** sudo is borrowing a **master key** for one named door — not keeping the building master key on your lanyard all day.

| Pattern | Plain meaning | Risk |
|---------|---------------|------|
| `sudo command` | Run one command as root (if allowed) | Safe if allow-list is narrow |
| `sudo -l` | List what **you** may run | Always check before assuming |
| `NOPASSWD:ALL` | No password + any command | **Very dangerous** on shared servers |
| `visudo` | Safe editor that checks syntax | Always use this — never raw vim on sudoers |

**What you can say in an interview:** “I grant exact command paths in `/etc/sudoers.d/`, run `visudo -c`, prove with `sudo -l`, and show one command that must **fail**.”

**Tiny example:**

``` {.bash .ra-terminal title="Terminal"}
sudo -l
sudo systemctl status ssh
```

### How identity work flows

1. **Check** — `id`, `getent passwd name`, `getent group name`, `sudo -l`
2. **Create** — `useradd` / `groupadd` (use `--system` for service accounts)
3. **Add to group** — `usermod -aG group user` (**`-a` means add**; without it you can **replace** the whole secondary group list)
4. **Edit sudo rules** — only with `visudo` or `visudo -f /etc/sudoers.d/file`
5. **Prove** — allow test + deny test + evidence files

### Key comparisons

| Object | Important fields | Files |
|--------|------------------|-------|
| User | UID, home, shell, primary GID | `/etc/passwd`, `/etc/shadow` |
| Group | GID, members | `/etc/group` |
| sudo rule | Who, as whom, which commands | `/etc/sudoers`, `/etc/sudoers.d/*` |

| Account type | Shell | Use for |
|--------------|-------|---------|
| Login user | `/bin/bash` | People |
| System user | `/usr/sbin/nologin` | Apps, daemons |
| root | `/bin/bash` or restricted | Break-glass admin only |

### Common pitfalls

- Using `usermod -G` **without** `-a` — removes other groups silently
- Editing `/etc/sudoers` with nano/vim — one typo locks everyone out of sudo
- Giving `NOPASSWD:ALL` “for CI convenience” on a shared jump server
- Same username, different UID on two servers sharing Network File System (NFS) — ownership breaks
- Assuming cloud “admin” group means least privilege — check `sudo -l` on every new image

## Hands-on Lab

### Objective

On a practice Ubuntu VM, create a team group, one human lab user, one system service account, and a **limited** sudoers file. Prove group membership, sudo allow, and sudo deny — then pack evidence under `~/rebash-linux/lab06`.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu 22.04/24.04 | Admin user with sudo |
| VM snapshot | Recommended before creating users |
| Packages | `sudo`, `passwd` (default on Ubuntu) |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab06 && cd ~/rebash-linux/lab06
set -euo pipefail
whoami | tee admin-user.txt
id | tee admin-id.txt
sudo -n true 2>/dev/null || sudo -v
```

!!! example "Expected output"
    `admin-user.txt` and `admin-id.txt` exist; `sudo` works (you may enter your password once).


### Real-world scenario

Security ticket: set up a practice VM with (1) a shared **deploy group**, (2) a **non-login service account** for app files, and (3) a human engineer who may restart **only** `rebash-lab.service` with sudo — **not** full root. Attach proof to the change ticket.

### Step-by-step tasks

#### Task 1 – Create group, human user, and service account

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab06
set -euo pipefail

sudo groupadd rebash-lab || true

if ! id rebash-alice >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash -G rebash-lab rebash-alice
fi

if ! id rebash-svc >/dev/null 2>&1; then
  sudo useradd --system --home /opt/rebash-lab-svc --shell /usr/sbin/nologin \
    --gid rebash-lab rebash-svc
fi

sudo usermod -aG rebash-lab rebash-alice

id rebash-alice | tee id-alice.txt
id rebash-svc | tee id-svc.txt
getent group rebash-lab | tee group-rebash-lab.txt
grep -E 'rebash-alice|rebash-svc' /etc/passwd | tee passwd-snippet.txt
```

!!! example "Expected output"
    `id-alice.txt` shows group `rebash-lab`. `id-svc.txt` shows `nologin` shell. `group-rebash-lab.txt` lists members.


#### Task 2 – Limited sudoers file (file fence + visudo)

Create the sudoers drop-in as a file first:

```sudoers title="99-rebash-lab-alice"
# REBASH lab — limited sudo for rebash-alice
Defaults:rebash-alice !requiretty
rebash-alice ALL=(root) NOPASSWD: /bin/systemctl status rebash-lab.service, /bin/systemctl restart rebash-lab.service
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab06
set -euo pipefail

# Save the sudoers file-fence above as ~/rebash-linux/lab06/99-rebash-lab-alice first
test -f 99-rebash-lab-alice
sudo visudo -c -f 99-rebash-lab-alice
sudo install -m 0440 99-rebash-lab-alice /etc/sudoers.d/99-rebash-lab-alice
sudo visudo -c

sudo -u rebash-alice sudo -l | tee sudo-l-alice.txt
grep -F 'systemctl' sudo-l-alice.txt
ls -l /etc/sudoers.d/99-rebash-lab-alice | tee sudoers-mode.txt
```

!!! example "Expected output"
    `visudo -c` reports syntax OK. `sudo-l-alice.txt` lists the two `systemctl` paths — not `ALL`. File mode is `-r--r-----` (`0440`).


#### Task 3 – Negative test and evidence pack

Prove alice is **not** full root.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab06
set -euo pipefail

if sudo -u rebash-alice sudo -n /bin/true 2>sudo-denied.txt; then
  echo "ERROR: unrestricted sudo — abort" >&2
  exit 1
fi
grep -Ei 'not allowed|sorry|denied|password' sudo-denied.txt || test -s sudo-denied.txt

tar -czf identity-evidence.tgz \
  admin-user.txt admin-id.txt \
  id-alice.txt id-svc.txt group-rebash-lab.txt passwd-snippet.txt \
  sudo-l-alice.txt sudo-denied.txt sudoers-mode.txt 99-rebash-lab-alice
ls -l identity-evidence.tgz | tee evidence-ls.txt
test -s identity-evidence.tgz
```

!!! example "Expected output"
    `/bin/true` with sudo is **denied** for alice. `identity-evidence.tgz` is not empty.


### Validation steps

- [ ] `id rebash-alice` shows group `rebash-lab`
- [ ] `id rebash-svc` uses a non-login shell
- [ ] `/etc/sudoers.d/99-rebash-lab-alice` mode is `0440`
- [ ] `sudo -u rebash-alice sudo -l` shows only intended `systemctl` commands
- [ ] `identity-evidence.tgz` exists under `~/rebash-linux/lab06`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `useradd: user already exists` | Lab re-run | Script checks with `id`; continue |
| `visudo: parse error` | Wrong sudoers syntax | Fix file; never install broken drop-in |
| `sudo: a password is required` | NOPASSWD rule missing | Check drop-in path; `visudo -c` |
| Locked out after bad sudoers | Edited without `visudo` | Root console / recovery; remove bad file |

### Challenge exercise

Create user `rebash-bob`, add to `rebash-lab`, and add a second drop-in allowing **only** `sudo -u rebash-svc /usr/bin/id`:

```sudoers title="99-rebash-lab-bob"
rebash-bob ALL=(root) NOPASSWD: /usr/bin/id -u rebash-svc
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab06
set -euo pipefail
if ! id rebash-bob >/dev/null 2>&1; then
  sudo useradd -m -s /bin/bash rebash-bob
fi
sudo usermod -aG rebash-lab rebash-bob
sudo visudo -c -f 99-rebash-lab-bob
sudo install -m 0440 99-rebash-lab-bob /etc/sudoers.d/99-rebash-lab-bob
sudo -u rebash-bob sudo -l | tee sudo-l-bob.txt
```

!!! example "Expected output"
    `sudo-l-bob.txt` shows only the narrow `id` command for rebash-svc.


### Learning outcomes

- Created human and system accounts with correct shells
- Used `usermod -aG` safely
- Installed checked sudoers files; proved allow and deny
- Saved identity proof suitable for a change ticket

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab06
set -euo pipefail

sudo rm -f /etc/sudoers.d/99-rebash-lab-alice /etc/sudoers.d/99-rebash-lab-bob
sudo visudo -c

sudo userdel -r rebash-alice 2>/dev/null || sudo userdel rebash-alice || true
sudo userdel -r rebash-bob 2>/dev/null || sudo userdel rebash-bob || true
sudo userdel rebash-svc 2>/dev/null || true
sudo groupdel rebash-lab 2>/dev/null || true
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab06`
- [ ] Can explain UID, GID, and why `usermod -aG` matters
- [ ] Can explain risk of server-wide `NOPASSWD:ALL`
- [ ] Know when to use a system user with `nologin`

## Code Walkthrough

1. **`id` and `getent` before change** — know current state.
2. **Small files under `/etc/sudoers.d/`** — mode `0440`; one file per role.
3. **`visudo -c` before and after** — syntax check is non-negotiable.
4. **Prove allow and deny** — `sudo -l` plus one command that must fail.
5. **Separate people from services** — login shell vs `nologin`.

## Security Considerations

- Treat sudo access as critical — review in change tickets
- Never store passwords or API tokens in sudoers
- Prefer SSH keys for people; disable password login on internet-facing servers (later modules)
- Keep human accounts separate from service accounts
- Log privileged use in `/var/log/auth.log` or `journalctl`

## Common Mistakes

!!! warning "Using `usermod -G` without `-a`"
    Secondary groups are replaced, not added. **Fix:** always `usermod -aG group user`, then `id user`.

!!! warning "Editing sudoers with vim directly"
    One typo can remove sudo for everyone. **Fix:** use `visudo` only; keep root console open while testing.

!!! warning "Giving `NOPASSWD:ALL` for convenience"
    Any process running as that user becomes root. **Fix:** allow only exact command paths.

!!! warning "Deleting users without checking file ownership"
    Old files keep the old UID. **Fix:** `find / -user name` before `userdel`.

## Best Practices

- One sudoers file per team or role, managed by configuration management
- System users for services; login users for people
- Name groups by purpose (`deploy`, `logs-read`), not by person name
- Review `sudo -l` on every new cloud image
- Document emergency admin accounts and test recovery quarterly

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `user is not in the sudoers file` | No rule / wrong user | Check `/etc/sudoers.d/*` and groups |
| `sudo: parse error` | Broken sudoers syntax | Root console; `visudo -c`; remove bad file |
| Group missing in `id` after `usermod` | Session not refreshed | Log out/in, `newgrp`, or reconnect SSH |
| Service cannot write files | Wrong UID/GID on folders | Set ownership to service account |
| CI job suddenly has root | sudo rule too open | Narrow rule; audit and rotate secrets |

## Summary

Users, groups, and sudo decide **who can do what** on Linux. Create accounts with a clear purpose, add groups safely, grant sudo as a short allow-list, and prove both success and failure. Next: [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md).

## Interview Questions

**1. What is the difference between a primary group and secondary groups, and how do you add a secondary group safely?**

??? success "Reveal answer"
    The **primary group** is the default GID used when the user creates new files. **Secondary groups** give extra shared access. Use `usermod -aG groupname username`, then check with `id username`. Without `-a`, the secondary group list can be **replaced** and access breaks.

**2. A junior edited `/etc/sudoers` with vim and now `sudo` fails for everyone. How do you recover?**

??? success "Reveal answer"
    Use a **root console**, single-user mode, or cloud **serial console**. Fix or remove the broken file, then run `visudo -c`. Prevent it by editing only with `visudo`, using small drop-in files, and testing on a practice VM first.

**3. When should an application use a system account with `nologin`?**

??? success "Reveal answer"
    When a service needs a UID to own files and processes but **must not** allow interactive login. Login shells are for people. Service accounts reduce risk if credentials leak and clarify ownership in audits.

**4. Why is `ALL=(ALL) NOPASSWD:ALL` dangerous on a jump server?**

??? success "Reveal answer"
    Any code running as that user becomes **full root** with no password prompt. Prefer a narrow rule like `user ALL=(root) NOPASSWD: /bin/systemctl restart myapp.service`. Prove with `sudo -l` and a deny test.

**5. How would you prove a sudo change is least privilege?**

??? success "Reveal answer"
    Show the drop-in file, successful `visudo -c`, `sudo -l` listing **only** intended commands, and a **deny** test (`sudo /bin/true`) that fails. Attach output to the change ticket.

**6. UIDs differ between two servers sharing NFS — what breaks?**

??? success "Reveal answer"
    NFS checks **numeric UID/GID**, not login names. Same username with different UIDs sees wrong ownership or `Permission denied`. Teams use central directories (LDAP/FreeIPA) or fixed UID ranges.

**7. How does cloud “admin” group membership relate to sudo?**

??? success "Reveal answer"
    Cloud images often put the first user in `sudo` (Ubuntu) or `wheel` (RHEL-like). That group maps to broad sudo in `/etc/sudoers`. Useful for first setup; production hardening often narrows access with role-based drop-ins. Always check `id` and `sudo -l` on new images.

## Related Tutorials

- Previous: [Disk Usage and File Attributes](disk-usage-and-file-attributes.md)
- Next: [Permissions, ACLs, and Special Bits](permissions-acls-and-special-bits.md)
- Related: [IAM on AWS](../aws/iam-identity-access-and-organizations.md) *(same identity ideas in the cloud)*
- Lab: [Users, Groups, and Permissions](../labs/linux-users-permissions-lab.md)

## References

- [`useradd(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/useradd.8.html)
- [`sudoers(5)`](https://www.sudo.ws/docs/man/sudoers.man/)
- [`visudo(8)`](https://www.sudo.ws/docs/man/visudo.man/)
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
