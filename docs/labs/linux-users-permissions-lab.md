---
title: "Lab — Users, Groups, and Permissions"
description: "Create service and human accounts, apply least-privilege permissions and ACLs, and prove sudo boundaries on a lab Ubuntu host."
difficulty: beginner
estimated_time: "45–55 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - users
  - permissions
  - acl
comments: false
---

# Lab — Users, Groups, and Permissions

## Lab Overview

**Purpose:** Practise user, group, `sudo`, mode bits, and Access Control Lists (ACLs) the way ops teams structure shared directories.

**Scenario:** Two engineers and one service account must share an app directory with least privilege — no world-writable shortcuts.

**Expected outcome:** Accounts exist, group ownership is correct, sticky/ACL behaviour is verified, and a denied access case is documented.

!!! tip "This is a lab, not a tutorial"
    Use `id`, `namei -l`, and `getfacl` as evidence. Guessing `chmod 777` fails the lab.

## Business Scenario

A small team shares `/opt/rebash-app` for configs and logs. Security insists on group collaboration without opening the tree to every user on the host.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Create users and groups with correct shells and homes
- [ ] Apply `chown` / `chmod` and explain octal modes
- [ ] Use SGID directories and optional ACLs for shared trees
- [ ] Grant limited `sudo` and verify with `sudo -l`
- [ ] Demonstrate a permission-denied case and fix it correctly

## Prerequisites

### Knowledge

- [Users, Groups, and sudo](../linux/users-groups-and-sudo.md)
- [Permissions, ACLs, and Special Bits](../linux/permissions-acls-and-special-bits.md)
- [Essential Linux Commands](../linux/essential-linux-commands.md)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu with sudo | Local VM preferred |
| `acl` package | for `setfacl` / `getfacl` |

**Estimated cost:** £0.

## Environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-linux-users
cd ~/rebash-lab-linux-users
sudo apt-get update && sudo apt-get install -y acl
```

## Initial State

No `rebash-app` group or lab users yet. You will create them.

## Lab Tasks

### Task 1 — Create group and accounts

``` {.bash .ra-terminal title="Terminal"}
sudo groupadd --system rebash-app || true
sudo useradd --system --home /opt/rebash-app --shell /usr/sbin/nologin --gid rebash-app rebash-svc 2>/dev/null || true
sudo useradd -m -s /bin/bash -G rebash-app alice 2>/dev/null || true
sudo useradd -m -s /bin/bash -G rebash-app bob 2>/dev/null || true
# Set temporary passwords for alice/bob if you will su - (lab only)
id alice; id bob; id rebash-svc
```

### Task 2 — Shared application tree

``` {.bash .ra-terminal title="Terminal"}
sudo mkdir -p /opt/rebash-app/{bin,etc,logs}
sudo chown -R rebash-svc:rebash-app /opt/rebash-app
sudo chmod 2770 /opt/rebash-app
sudo chmod 2770 /opt/rebash-app/logs
sudo chmod 0750 /opt/rebash-app/bin /opt/rebash-app/etc
echo "listen=127.0.0.1" | sudo tee /opt/rebash-app/etc/app.conf
sudo chown rebash-svc:rebash-app /opt/rebash-app/etc/app.conf
sudo chmod 0640 /opt/rebash-app/etc/app.conf
namei -l /opt/rebash-app/etc/app.conf
```

Explain why `2770` matters (SGID bit keeps new files in the group).

### Task 3 — ACL for a read-only auditor

``` {.bash .ra-terminal title="Terminal"}
sudo useradd -m -s /bin/bash auditor 2>/dev/null || true
sudo setfacl -m u:auditor:rx /opt/rebash-app
sudo setfacl -m u:auditor:r /opt/rebash-app/etc/app.conf
sudo setfacl -m d:u:auditor:rx /opt/rebash-app/logs
getfacl /opt/rebash-app /opt/rebash-app/etc/app.conf | tee ~/rebash-lab-linux-users/acl.txt
```

As `auditor` (via `sudo -u auditor`), confirm read of `app.conf` and that write to `logs` fails unless you grant it.

### Task 4 — Limited sudo

``` {.bash .ra-terminal title="Terminal"}
echo 'alice ALL=(root) NOPASSWD: /usr/bin/systemctl status *, /usr/bin/journalctl *' \
  | sudo tee /etc/sudoers.d/rebash-alice
sudo chmod 0440 /etc/sudoers.d/rebash-alice
sudo visudo -cf /etc/sudoers.d/rebash-alice
sudo -u alice sudo -l | tee ~/rebash-lab-linux-users/sudo-alice.txt
```

Confirm alice **cannot** run arbitrary `apt` via sudo.

### Task 5 — Denied access drill

As a user **not** in `rebash-app` (create `carol` without the group):

``` {.bash .ra-terminal title="Terminal"}
sudo useradd -m -s /bin/bash carol 2>/dev/null || true
sudo -u carol cat /opt/rebash-app/etc/app.conf && echo UNEXPECTED || echo "denied (expected)" | tee ~/rebash-lab-linux-users/deny.txt
```

## Validation

- [ ] `alice`/`bob` are in `rebash-app`; `rebash-svc` is nologin
- [ ] New files under `/opt/rebash-app/logs` inherit group `rebash-app` (SGID)
- [ ] ACL evidence in `acl.txt`
- [ ] `carol` is denied; alice’s sudo is limited

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| ACL commands missing | `sudo apt install acl` |
| SGID not inherited | Recheck `chmod 2770` on directory |
| sudoers syntax error | `visudo -cf`; fix before next sudo |

## Challenge Extensions

- Add a sticky bit on a scratch drop directory under `/opt/rebash-app`
- Demonstrate SUID risk on a toy binary (do not keep it)
- Migrate ACL grants into a documented group-only model

## Cleanup

``` {.bash .ra-terminal title="Terminal"}
sudo rm -f /etc/sudoers.d/rebash-alice
sudo rm -rf /opt/rebash-app
sudo userdel -r alice 2>/dev/null || true
sudo userdel -r bob 2>/dev/null || true
sudo userdel -r carol 2>/dev/null || true
sudo userdel -r auditor 2>/dev/null || true
sudo userdel rebash-svc 2>/dev/null || true
sudo groupdel rebash-app 2>/dev/null || true
rm -rf ~/rebash-lab-linux-users
```

## Production Discussion

Human access increasingly uses SSO + PAM or cloud identity; service accounts remain local or use workload identity. Directory permissions and ACLs still matter for host-local state.

## Best Practices

- Prefer groups over ACLs when a single group is enough
- Never use `chmod 777` to “make it work”
- Audit `sudoers.d` files with `visudo -cf`

## Common Mistakes

| Mistake | Correct approach |
|---------|------------------|
| World-writable shared dirs | 2770 + shared group |
| Login shells for service users | `/usr/sbin/nologin` |
| Broad `ALL=(ALL) NOPASSWD: ALL` | Command-scoped sudo |

## Success Criteria

You can draw the ownership model and show denied vs allowed evidence without opening the tree world-writable.

## Reflection Questions

1. When do ACLs beat an extra group?
2. What breaks if SGID is missing on a shared log directory?
3. How would you review sudo sprawl across 100 hosts?

## Interview Connection

Expect walkthroughs of `chmod` octal, sticky/SUID/SGID, and “how do you share a directory safely?”

## Related Tutorials

- [Users, Groups, and sudo](../linux/users-groups-and-sudo.md)
- [Permissions, ACLs, and Special Bits](../linux/permissions-acls-and-special-bits.md)
- Lab: [SSH Secure Access](linux-ssh-secure-access.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)

## References

- `man 7 credentials`, `man acl`, `man sudoers`
