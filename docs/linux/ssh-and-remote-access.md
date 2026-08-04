---
title: "SSH and Remote Access"
description: "Linux SSH keys, client config, localhost login, and scp/rsync — plain language first, then a key-based auth lab."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 9 · Linux Networking"
tags:
  - linux
  - ssh
  - remote
  - keys
  - scp
  - rsync
  - beginners
prerequisites:
  - linux/linux-networking-tools
next:
  - linux/package-management
related:
  - labs/linux-ssh-secure-access
labs:
  - labs/linux-ssh-secure-access
interview: interview/linux
comments: false
---

# SSH and Remote Access

## Overview

**Secure Shell (SSH)** is how you reach almost every Linux server. Keys, config, and safe habits matter more than memorising flags.

**Secure Shell (SSH)** is how you log in to almost every Linux cloud virtual machine (VM), jump server, and build agent. Commands you type on your laptop run on the remote host over an encrypted channel. File copy uses the same security: **`scp`** and **`rsync`**.

**Plain problem:** A team shares one password in chat. Someone leaves the company. Keys are safer: your **private key** stays on your machine; the server stores only the **public key** in `authorized_keys`.

This tutorial teaches **key-based login** on **localhost** (safe lab). It does **not** disable password login or change `sshd_config` in ways that could lock you out — never break your only SSH path without **console access**.

This is **Tutorial 15** in **Module 9: Linux Networking** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- [Linux Networking Tools](linux-networking-tools.md)
- A practice Ubuntu 22.04/24.04 VM where OpenSSH server runs (`sudo systemctl status ssh` or `sshd`)
- A normal user account with working local login
- **Keep a second session open** while experimenting — if SSH breaks, you still have one window to fix it

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain public/private keys and `authorized_keys` in plain words
- [ ] Generate an Ed25519 key pair in an isolated lab directory
- [ ] Log in with `ssh -i` to localhost using key auth
- [ ] Write a `~/.ssh/config` Host stanza for shorter commands
- [ ] Copy files with `scp` and `rsync` over SSH
- [ ] Complete the lab under `~/rebash-linux/lab15` with evidence files
- [ ] Answer common fresher interview questions on SSH

## Architecture

The SSH client proves identity with a key (or password). sshd on the server checks `~/.ssh/authorized_keys` and starts your shell session.

![SSH access — client key, encrypted channel, sshd, authorized_keys](../assets/excalidraw/linux-ssh-access.svg)

## Theory

### The problem (before any jargon)

Passwords leak in chat, reuse across sites, and appear in brute-force logs. Cloud providers inject your **public key** at first boot — you should understand that model before hardening production (Module 13).

### Keys (simple words)

**Analogy:** A **private key** is your house key — never post it online. A **public key** is the lock pattern you install on the server door (`authorized_keys`). Anyone can see the lock pattern; only you hold the key.

| File | Permission | Purpose |
|------|------------|---------|
| `~/.ssh/id_ed25519` | `600` | Private key — secret |
| `~/.ssh/id_ed25519.pub` | `644` | Public key — copy to servers |
| `~/.ssh/authorized_keys` | `600` | Public keys allowed to log in |
| `~/.ssh` directory | `700` | SSH refuses loose permissions |

**What you can say in an interview:** “I use Ed25519 keys, install pub keys in authorized_keys, chmod 700/600, and never share private keys.”

**Tiny example — generate key:**

``` {.bash .ra-terminal title="Terminal"}
ssh-keygen -t ed25519 -f ~/.ssh/lab_key -C "lab-only" -N ""
ssh-keygen -lf ~/.ssh/lab_key.pub
```

**Interview line:** “Ed25519 is modern default — smaller and faster than RSA for most cases.”

### ssh client basics

``` {.bash .ra-terminal title="Terminal"}
ssh -i ~/.ssh/lab_key user@localhost
ssh -v user@host              # verbose debug
ssh user@host 'uptime'        # remote one-liner
```

### ~/.ssh/config — aliases

```sshconfig title="config-snippet"
Host labvm
    HostName localhost
    User myuser
    IdentityFile ~/.ssh/lab_key
    StrictHostKeyChecking accept-new
```

Then: `ssh labvm`

**Interview line:** “Config Host stanzas reduce typos in automation and on-call stress.”

### scp and rsync

``` {.bash .ra-terminal title="Terminal"}
scp -i ~/.ssh/lab_key local.txt user@localhost:~/remote.txt
rsync -avz -e "ssh -i ~/.ssh/lab_key" ./dir/ user@localhost:~/dir/
```

### Production warnings (read before any hardening)

- **Never** disable password auth or restart sshd on your **only** SSH session without console/serial access.
- **Never** set `PermitRootLogin yes` for convenience.
- **Never** commit private keys to Git.
- **`StrictHostKeyChecking=no`** in CI is a trade-off — document and scope it.
- Test sshd config: **`sudo sshd -t`** before **`systemctl restart ssh`**.

### Common pitfalls

- Wrong permissions on `~/.ssh` — sshd silently rejects keys
- Editing `authorized_keys` for wrong user
- Overwriting your only personal key without backup
- Confusing `ssh-copy-id` target user@host

## Hands-on Lab

### Objective

Generate lab keys under `~/rebash-linux/lab15`, install public key for localhost login, connect with key auth, copy a file with scp, and save evidence — without changing global sshd hardening.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | `sshd` running on port 22 |
| Local login | Console or existing SSH session |
| OpenSSH client | `ssh`, `scp`, `ssh-keygen` |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab15 && cd ~/rebash-linux/lab15
```

### Real-world scenario

You join a team that provisions VMs with your public key. Before touching production, you prove you can generate a key, install it, log in, and copy a deploy artefact with scp — all documented for the access request ticket.

### Step-by-step tasks

#### Task 1 – Generate lab key pair (isolated path)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
ssh-keygen -t ed25519 -f ./lab15_ed25519 -C "rebash-lab15" -N ""
ls -la lab15_ed25519 lab15_ed25519.pub | tee key-perms.txt
ssh-keygen -lf ./lab15_ed25519.pub | tee key-fingerprint.txt
test -f lab15_ed25519 && test -f lab15_ed25519.pub
```

!!! example "Expected output"
    Two key files exist. `key-fingerprint.txt` shows Ed25519 fingerprint and comment `rebash-lab15`.


#### Task 2 – Install public key for localhost (your user)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
mkdir -p ~/.ssh
chmod 700 ~/.ssh
grep -qF "$(cat lab15_ed25519.pub)" ~/.ssh/authorized_keys 2>/dev/null || cat lab15_ed25519.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
grep 'rebash-lab15' ~/.ssh/authorized_keys | tee auth-key-line.txt
test -s auth-key-line.txt
```

!!! example "Expected output"
    `auth-key-line.txt` contains your lab public key line ending with `rebash-lab15`.


#### Task 3 – Key-based SSH to localhost

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
ssh -i ./lab15_ed25519 -o StrictHostKeyChecking=accept-new -o BatchMode=yes "$USER@localhost" 'hostname; whoami; pwd' | tee ssh-localhost.txt
grep -q "$USER" ssh-localhost.txt
grep -q "$(hostname)" ssh-localhost.txt
```

!!! example "Expected output"
    `ssh-localhost.txt` shows hostname, your username, and home directory — without password prompt (`BatchMode=yes` proves key auth).


#### Task 4 – scp and config stanza

Create `deploy.txt`:

```text title="deploy.txt"
lab15 artefact created at PLACEHOLDER
```

Create `ssh-config-snippet`:

```sshconfig title="ssh-config-snippet"
Host rebash-lab15
    HostName localhost
    User PLACEHOLDER_USER
    IdentityFile PLACEHOLDER_KEY
    StrictHostKeyChecking accept-new
```

Prepare and test:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
sed "s/PLACEHOLDER/$(date -Is)/" deploy.txt > deploy.local.txt
sed -e "s/PLACEHOLDER_USER/$USER/" -e "s|PLACEHOLDER_KEY|$HOME/rebash-linux/lab15/lab15_ed25519|" ssh-config-snippet > ssh-config.local
scp -i ./lab15_ed25519 -o StrictHostKeyChecking=accept-new deploy.local.txt "$USER@localhost:~/rebash-linux/lab15/deploy-received.txt"
ssh -i ./lab15_ed25519 "$USER@localhost" 'test -s ~/rebash-linux/lab15/deploy-received.txt && wc -c ~/rebash-linux/lab15/deploy-received.txt' | tee scp-proof.txt
test -s ssh-config.local
echo "lab15 ssh OK" | tee evidence.txt
```

!!! example "Expected output"
    `deploy-received.txt` exists on the same host via scp. `scp-proof.txt` shows non-zero byte count.


### Validation steps

- [ ] Key login works with `BatchMode=yes` (no password)
- [ ] `~/.ssh` is `700` and `authorized_keys` is `600`
- [ ] scp copied file successfully
- [ ] You did **not** disable PasswordAuthentication or restart sshd into a lockout

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Permission denied (publickey)` | Key not in authorized_keys or wrong perms | Fix modes 700/600; verify pub key line |
| `WARNING: UNPROTECTED PRIVATE KEY` | Key file world-readable | `chmod 600 lab15_ed25519` |
| `Host key verification failed` | Known hosts mismatch | Lab uses `accept-new`; do not blindly delete production known_hosts |
| scp: Connection refused | sshd not running | `sudo systemctl start ssh` |

### Challenge exercise

Use `rsync -avz` with the lab key to sync a directory to localhost and prove with a manifest file.

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
mkdir -p sync-src && echo "sync $(date -Is)" > sync-src/mark.txt
rsync -avz -e "ssh -i $PWD/lab15_ed25519 -o StrictHostKeyChecking=accept-new" sync-src/ "$USER@localhost:~/rebash-linux/lab15/sync-dest/"
ssh -i ./lab15_ed25519 "$USER@localhost" 'cat ~/rebash-linux/lab15/sync-dest/mark.txt' | tee rsync-proof.txt
grep -q sync rsync-proof.txt
```

### Learning outcomes

- You generated and used Ed25519 keys without touching production keys
- You proved key-based localhost login and scp/rsync
- You understand permission requirements on `~/.ssh`

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab15
# Remove lab public key line from authorized_keys (optional — keeps file tidy):
grep -v 'rebash-lab15' ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp && mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
# Keep lab15_ed25519* in lab dir for revision — do NOT commit private key to Git
```

## Validation

- [ ] Lab completed under `~/rebash-linux/lab15`
- [ ] Can explain public vs private key to a classmate
- [ ] Ready for package management next

## Code Walkthrough

1. **Separate lab keys** — never overwrite `~/.ssh/id_ed25519` without backup.
2. **`BatchMode=yes`** — proves non-interactive key auth (CI pattern).
3. **`ssh -i`** — explicit identity file for multiple keys.
4. **Permissions** — sshd rejects keys if `~/.ssh` or `authorized_keys` is too open.
5. **`sshd -t` before restart** — production habit when you eventually harden sshd.

## Security Considerations

- Private keys are secrets — store in agent or hardware token; never in Slack/Git.
- Use separate keys per environment (lab/staging/prod).
- `authorized_keys` options can restrict commands (`command="..."`) for automation.
- Disable root login and password auth only with confirmed console access.
- Audit `~/.ssh/authorized_keys` during offboarding — remove departed users’ keys.

## Common Mistakes

!!! warning "chmod 644 on private key"
    SSH refuses the key. Fix: **`chmod 600`** on private key; **`700`** on `.ssh`.

!!! warning "Disabling passwords on only SSH session"
    Typo in sshd_config locks everyone out. Fix: **`sshd -t`**, second session, serial console ready.

!!! warning "Sharing one team private key"
    Cannot revoke one person. Fix: one key pair per engineer; remove one line from authorized_keys.

!!! warning "StrictHostKeyChecking=no everywhere"
    Opens MITM risk. Fix: use known_hosts, `accept-new` once, or CI-only scoped disable with documentation.

## Best Practices

- Prefer **Ed25519** keys for new deployments
- Use **`ssh-copy-id`** carefully with the correct `user@host`
- Maintain **`~/.ssh/config`** for fleet aliases and IdentityFile
- Pass keys to agents with timeout: `ssh-add -t 8h`
- Log access — sshd logs go to journal/auth.log; forward to SIEM in production

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Publickey denied | Wrong key, perms, or user | `-vvv`; fix 700/600; check authorized_keys user |
| Connection timed out | Security group / firewall | Cloud SG port 22; `ss -tlnp \| grep 22` on host |
| Host key changed warning | Rebuilt VM same IP | Verify with provider; update known_hosts entry |
| Agent offers wrong key | Many keys loaded | `ssh -i` explicit path or `IdentitiesOnly yes` in config |

## Summary

**SSH** encrypts remote shell and file copy. Use **key-based auth**: private key on client, public key in **`authorized_keys`**, strict **permissions**. You practised on **localhost** safely. Hardening sshd comes later — always keep **console access** before changing the only SSH path.

## Interview Questions

**1. How does SSH key authentication work?**

??? success "Reveal answer"
    The client proves ownership of a **private key**; the server checks the matching **public key** listed in **`~/.ssh/authorized_keys`**. No password is required if the key is trusted. Permissions on `.ssh` and key files must be tight (700/600) or sshd rejects login.

**2. Why Ed25519 over RSA?**

??? success "Reveal answer"
    **Ed25519** keys are shorter, faster, and modern curves with good security at default sizes. RSA remains common in legacy systems; new keys on current OpenSSH defaults favour Ed25519 unless policy requires RSA.

**3. What permissions must ~/.ssh and authorized_keys have?**

??? success "Reveal answer"
    Directory **`~/.ssh` → 700**, **`authorized_keys` → 600**, private key **600**. Group/world read on private key or authorized_keys causes sshd to ignore keys for security.

**4. What is the difference between scp and rsync?**

??? success "Reveal answer"
    Both use SSH. **`scp`** is simple copy. **`rsync`** syncs directories incrementally (only changed blocks), preserves more attributes with `-a`, and scales better for large trees — preferred for deploy artefacts and backups.

**5. What does BatchMode=yes test?**

??? success "Reveal answer"
    SSH runs **non-interactively** — no password or keyboard-interactive prompts. Fails if key auth is not set up. Used in scripts and CI to prove key-based access works.

**6. Why should you run sshd -t before restarting sshd?**

??? success "Reveal answer"
    It **validates config syntax** without applying a broken file. A bad `sshd_config` can stop sshd from starting — locking you out if that was your only access path. Always keep console/serial access when changing sshd.

**7. When is StrictHostKeyChecking=no acceptable?**

??? success "Reveal answer"
    Rarely — mainly **ephemeral CI builders** that are destroyed after one job, with other network controls. It disables MITM host key verification. Prefer **`accept-new`** (trust first sight, then enforce) or proper known_hosts management for production hosts.

## Related Tutorials

- Prior: [Linux Networking Tools](linux-networking-tools.md)
- Next: [Package Management](package-management.md)
- Lab: [Linux SSH secure access](../labs/linux-ssh-secure-access.md)

## References

- [OpenSSH manual — ssh(1)](https://man.openbsd.org/ssh.1)
- [OpenSSH manual — sshd_config(5)](https://man.openbsd.org/sshd_config.5)
- [ssh-keygen(1)](https://man.openbsd.org/ssh-keygen.1)
- [REBASH Linux course index](index.md)
