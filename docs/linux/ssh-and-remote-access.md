---
title: "SSH and Remote Access"
description: "Use Secure Shell (SSH) with keys, client config, localhost login, and scp/rsync file copy on a practice Ubuntu VM."
difficulty: intermediate
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
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

**Secure Shell (SSH)** is how you log in to almost every Linux cloud virtual machine (VM), jump server (bastion), and build agent. You type commands on your laptop; they run on the remote host over an encrypted channel. Day-to-day work also uses SSH for file copy (`scp`, `rsync`) and simple port forwarding to reach private services through a bastion.

This tutorial focuses on **access fundamentals**: generate an **Ed25519** key pair, install the public key in `authorized_keys`, log in without a password (to localhost in the lab), write a small `~/.ssh/config` Host stanza, and copy a file with `scp` / `rsync`. Module 13 covers hardening (disable password login, firewalls). Here the goal is correct, key-based access you can explain in an interview or change ticket.

In production, weak key hygiene, shared private keys in chat, `StrictHostKeyChecking=no` “to make CI work”, or agent forwarding to untrusted hosts create lasting security debt. Cloud images often allow the first user with a vendor-injected key. You still need to understand `sshd`, `~/.ssh/authorized_keys` modes (`700` / `600`), and client config aliases so automation (`ssh host 'uptime'`) is reliable under pressure.

This is **Tutorial 15** in **Module 9: Linux Networking** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers.

## Prerequisites

- [Linux Networking Tools](linux-networking-tools.md)
- A **practice Ubuntu 22.04/24.04 VM** where OpenSSH server is installed (or you can install it)
- You may create lab keys under `~/rebash-linux/lab15` (do **not** overwrite your real production keys without a backup)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how SSH client, `sshd`, keys, and `authorized_keys` work together
- [ ] Generate an Ed25519 key pair and install the public key for passwordless login
- [ ] Create a `~/.ssh/config` Host alias and use it for remote commands
- [ ] Copy files with `scp` and `rsync` over SSH
- [ ] Check basic permissions and `sshd` status when login fails

## Architecture

The SSH client authenticates to `sshd` using a key (preferred) or a password. After login, the same channel can carry remote commands and file transfers.

![Architecture diagram for SSH and Remote Access](../assets/excalidraw/linux-ssh-access.svg)

## Theory

### What it is

SSH provides encrypted remote login and a secure channel for commands and file copy. Important pieces:

| Piece | Role |
|-------|------|
| `ssh` client | Connects from your machine |
| `sshd` | Server daemon on the remote host |
| Key pair | Private key stays with you; public key goes on the server |
| `~/.ssh/authorized_keys` | List of public keys allowed to log in as that user |
| `~/.ssh/config` | Client aliases (Host, User, IdentityFile, Port) |
| `scp` / `rsync` | Copy files over SSH |

```bash
ssh-keygen -t ed25519 -f ./lab_ed25519 -N ""
ssh -i ./lab_ed25519 user@host
```

### Why it matters

Almost every cloud VM interaction starts with SSH. Password login on the public internet is risky. Key-based login is the default expectation in DevOps and SRE roles. Fluent client config reduces typing mistakes during incidents and makes scripts reliable.

### How it works

1. **Generate keys** — `ssh-keygen -t ed25519` (strong default on modern OpenSSH).
2. **Install public key** — append the `.pub` line to the remote user’s `~/.ssh/authorized_keys` (`ssh-copy-id` helps when password login still works).
3. **Fix modes** — `~/.ssh` should be `700`; `authorized_keys` and private keys should be `600`.
4. **Connect** — `ssh -i key user@host` or a `Host` stanza in `~/.ssh/config`.
5. **Verify host keys** — the client stores server fingerprints in `known_hosts` to detect impersonation.
6. **Transfer** — `scp file host:path` or `rsync -avz -e ssh …`.
7. **Forward (optional)** — `ssh -L localport:target:port bastion` reaches a private service through a jump host.

```bash
ssh-copy-id -i ./lab_ed25519.pub user@host
ssh -i ./lab_ed25519 user@host 'hostname; whoami'
```

Hardening (disable passwords, restrict users, Fail2Ban) comes later. Here, prove keys and config work.

### Key concepts and comparisons

| Method | Prefer when | Avoid when |
|--------|-------------|------------|
| Public-key auth | Production, cloud VMs, CI | Never share the private key |
| Password auth | Emergency bootstrap only | Internet-facing default |
| Certificate auth | Large fleets, short-lived access | Overkill for a single lab VM |
| Agent forwarding | Rare, carefully controlled | Blind forwarding to untrusted hosts |

### Common pitfalls

- Overwriting `~/.ssh/id_ed25519` without backup.
- Wrong modes on `.ssh` or `authorized_keys` → silent key rejection.
- Using `StrictHostKeyChecking=no` permanently in scripts.
- Putting the **private** key on the server.
- Expecting a new group membership to apply inside an old SSH session without reconnecting.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, generate a lab-only Ed25519 key, enable passwordless SSH to **localhost** as your user, add a `Host` alias, run a remote command, and copy a file with `scp` and `rsync`. Save proof under `~/rebash-linux/lab15`.

### Prerequisites

- Ubuntu 22.04/24.04 with `sudo`
- Packages: `openssh-client`, `openssh-server`, `rsync`
- Local SSH to `127.0.0.1` allowed (default on Ubuntu)

### Lab environment

Workspace: `~/rebash-linux/lab15`

```bash
mkdir -p ~/rebash-linux/lab15 && cd ~/rebash-linux/lab15
set -euo pipefail
whoami | tee admin-user.txt
id -u | tee admin-uid.txt
sudo -n true 2>/dev/null || sudo -v

sudo apt-get update -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y openssh-client openssh-server rsync
sudo systemctl enable --now ssh
sudo systemctl is-active ssh | tee sshd-active.txt
```

**Expected output:** `sshd-active.txt` contains `active`.

### Real-world scenario

A new engineer needs repeatable SSH access to a bastion: key-based login, a short `Host` alias in `~/.ssh/config`, and a way to push a small config file with `rsync`. You practise the same workflow safely against localhost first, then reuse the pattern for real hosts.

### Step-by-step tasks

#### Task 1 – Generate lab key and install for localhost

```bash
cd ~/rebash-linux/lab15
set -euo pipefail

# Lab-only key (empty passphrase for practice VM — use a passphrase on real laptops)
ssh-keygen -t ed25519 -f ./rebash_lab_ed25519 -N "" -C "rebash-lab15@$(hostname)"
test -f rebash_lab_ed25519
test -f rebash_lab_ed25519.pub
chmod 600 rebash_lab_ed25519

mkdir -p ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Install public key if not already present
PUB="$(cat rebash_lab_ed25519.pub)"
grep -Fqx "$PUB" ~/.ssh/authorized_keys || echo "$PUB" >> ~/.ssh/authorized_keys

# Passwordless SSH to localhost
ssh -i ./rebash_lab_ed25519 \
  -o IdentitiesOnly=yes \
  -o BatchMode=yes \
  -o StrictHostKeyChecking=accept-new \
  "$USER@127.0.0.1" 'echo OK; hostname; whoami' | tee ssh-localhost.txt

grep -q OK ssh-localhost.txt
```

**Expected output:** `ssh-localhost.txt` shows `OK`, your hostname, and your username.

#### Task 2 – Client config Host alias

```bash
cd ~/rebash-linux/lab15
set -euo pipefail

LAB_KEY="$(pwd)/rebash_lab_ed25519"
CONFIG_SNIPPET="$HOME/.ssh/config"

# Backup existing config once
if [ -f "$CONFIG_SNIPPET" ] && [ ! -f "$HOME/.ssh/config.rebash-lab15.bak" ]; then
  cp -a "$CONFIG_SNIPPET" "$HOME/.ssh/config.rebash-lab15.bak"
fi

# Remove previous lab block if re-running
if [ -f "$CONFIG_SNIPPET" ]; then
  awk '
    /^# BEGIN REBASH-LAB15$/ {skip=1; next}
    /^# END REBASH-LAB15$/ {skip=0; next}
    !skip {print}
  ' "$CONFIG_SNIPPET" > "$CONFIG_SNIPPET.tmp" && mv "$CONFIG_SNIPPET.tmp" "$CONFIG_SNIPPET"
fi

cat >> "$CONFIG_SNIPPET" << EOF
# BEGIN REBASH-LAB15
Host rebash-lab15
  HostName 127.0.0.1
  User $USER
  IdentityFile $LAB_KEY
  IdentitiesOnly yes
# END REBASH-LAB15
EOF
chmod 600 "$CONFIG_SNIPPET"

ssh -o BatchMode=yes rebash-lab15 'uptime; echo CONFIG_OK' | tee ssh-alias.txt
grep -q CONFIG_OK ssh-alias.txt
```

**Expected output:** `ssh-alias.txt` contains `CONFIG_OK` and an `uptime` line.

#### Task 3 – scp, rsync, and evidence pack

```bash
cd ~/rebash-linux/lab15
set -euo pipefail

echo "rebash lab15 payload $(date -Is)" > payload.txt

# scp to a remote path (localhost)
scp -o BatchMode=yes payload.txt rebash-lab15:~/rebash-linux/lab15/payload-from-scp.txt
ssh -o BatchMode=yes rebash-lab15 'test -f ~/rebash-linux/lab15/payload-from-scp.txt && cat ~/rebash-linux/lab15/payload-from-scp.txt' \
  | tee scp-verify.txt

# rsync over SSH
rsync -avz -e "ssh -o BatchMode=yes" payload.txt rebash-lab15:~/rebash-linux/lab15/payload-from-rsync.txt
ssh -o BatchMode=yes rebash-lab15 'test -f ~/rebash-linux/lab15/payload-from-rsync.txt && wc -c ~/rebash-linux/lab15/payload-from-rsync.txt' \
  | tee rsync-verify.txt

# Permission proof
ls -ld ~/.ssh | tee ssh-dir-mode.txt
ls -l ~/.ssh/authorized_keys rebash_lab_ed25519 | tee key-modes.txt
ssh -o BatchMode=yes rebash-lab15 'sudo systemctl is-active ssh' | tee sshd-remote-check.txt

tar -czf ssh-evidence.tgz \
  admin-user.txt admin-uid.txt sshd-active.txt \
  rebash_lab_ed25519.pub ssh-localhost.txt ssh-alias.txt \
  payload.txt scp-verify.txt rsync-verify.txt \
  ssh-dir-mode.txt key-modes.txt sshd-remote-check.txt
# Do NOT pack the private key into shared tickets
ls -l ssh-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** scp and rsync verify files exist; `ssh-evidence.tgz` is present; private key is **not** inside the archive.

### Validation steps

- [ ] `ssh -i ./rebash_lab_ed25519 "$USER@127.0.0.1"` works in BatchMode
- [ ] `ssh rebash-lab15` works via `~/.ssh/config`
- [ ] `payload-from-scp.txt` and `payload-from-rsync.txt` exist
- [ ] `~/.ssh` is mode `700` and keys are not world-readable
- [ ] `ssh-evidence.tgz` exists under `~/rebash-linux/lab15`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Permission denied (publickey)` | Public key not installed / wrong key | Check `authorized_keys` and `IdentityFile` |
| `Bad owner or permissions on .ssh` | Modes too open | `chmod 700 ~/.ssh`; `chmod 600 authorized_keys` |
| `Connection refused` | `sshd` not running | `sudo systemctl enable --now ssh` |
| Host key prompt blocks BatchMode | First connect | Use one interactive connect, or `accept-new` once in lab |
| Overwrote real keys | Wrong `-f` path | Always use a lab path like `./rebash_lab_ed25519` |

### Challenge exercise

Create a second key `rebash_lab_ed25519_b`, append its public key to `~/.ssh/authorized_keys`, connect with `ssh -i ./rebash_lab_ed25519_b -o IdentitiesOnly=yes -o BatchMode=yes "$USER@127.0.0.1" 'echo SECOND_OK'`, and save the output as `ssh-second-key.txt`. Remove the second public key line and delete the second key files in Cleanup.

### Learning outcomes

- Generated and installed an Ed25519 key for localhost SSH
- Used a `Host` alias from `~/.ssh/config`
- Copied files with `scp` and `rsync`
- Saved access proof without sharing the private key

### Cleanup

```bash
cd ~/rebash-linux/lab15
set -euo pipefail

# Remove lab Host block from config
if [ -f "$HOME/.ssh/config" ]; then
  awk '
    /^# BEGIN REBASH-LAB15$/ {skip=1; next}
    /^# END REBASH-LAB15$/ {skip=0; next}
    !skip {print}
  ' "$HOME/.ssh/config" > "$HOME/.ssh/config.tmp" && mv "$HOME/.ssh/config.tmp" "$HOME/.ssh/config"
fi

# Remove lab public key lines from authorized_keys
if [ -f rebash_lab_ed25519.pub ]; then
  PUB="$(cat rebash_lab_ed25519.pub)"
  grep -Fvx "$PUB" ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp 2>/dev/null || true
  mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
fi
if [ -f rebash_lab_ed25519_b.pub ]; then
  PUBB="$(cat rebash_lab_ed25519_b.pub)"
  grep -Fvx "$PUBB" ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp 2>/dev/null || true
  mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
fi

rm -f rebash_lab_ed25519 rebash_lab_ed25519.pub rebash_lab_ed25519_b rebash_lab_ed25519_b.pub
# Optional: restore config backup if you prefer
# mv ~/.ssh/config.rebash-lab15.bak ~/.ssh/config
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab15/` with evidence files
- [ ] You can explain key-based SSH vs password login
- [ ] You know correct `.ssh` permission modes
- [ ] You can describe one production risk (shared private keys, disabled host key checks)

## Code Walkthrough

Typical production access workflow:

1. **Generate** a personal key (passphrase on real laptops)  
2. **Install** the public key only (never the private key)  
3. **Alias** the host in `~/.ssh/config`  
4. **Prove** with `ssh host 'hostname; whoami'`  
5. **Transfer** with `rsync` over SSH for repeated syncs  

Hardening comes after access works.

## Security Considerations

- Never commit private keys to git or chat  
- Prefer Ed25519; protect private keys with a passphrase outside lab VMs  
- Keep `~/.ssh` mode `700` and private keys `600`  
- Do not leave `StrictHostKeyChecking=no` as a permanent default  
- Limit who can reach `sshd` with security groups / firewalls (covered in hardening)  

## Common Mistakes

!!! warning "Sharing one private key across the whole team"
    Compromise of one laptop compromises every server. **Fix:** one key per person (or short-lived certificates).

!!! warning "World-readable authorized_keys or .ssh"
    `sshd` may ignore the keys. **Fix:** `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys`.

!!! warning "Disabling host key checking in every script"
    You lose protection against impersonation. **Fix:** manage `known_hosts` properly; use `accept-new` only with care.

!!! warning "Putting the private key on the server"
    Attackers who gain the server get lateral movement. **Fix:** only the `.pub` file belongs on the server.

## Best Practices

- Use `IdentitiesOnly yes` in Host stanzas to avoid offering the wrong keys  
- Name keys by purpose (`work-bastion`, `ci-deploy`)  
- Prefer `rsync -avz` for sync; use `scp` for one-off copies  
- Document jump-host patterns (`ProxyJump`) for private subnets  
- Rotate keys when people leave the team  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `Permission denied (publickey)` | Key not authorised / wrong user | Check `authorized_keys`, user, `IdentityFile` |
| `Connection refused` | sshd down / wrong port | `systemctl status ssh`; check port 22 |
| Works interactively, fails in CI | Missing key / BatchMode / passphrase | Use deploy keys or an agent carefully |
| Host key verification failed | Server rebuilt | Verify fingerprint out-of-band; update `known_hosts` |
| Slow first connect | DNS / GSSAPI attempts | Set `GSSAPIAuthentication no` in client config if needed |

## Summary

SSH is the main remote access tool for Linux in the cloud. Generate keys, install only the public key, use a clear client `Host` alias, and prove login and file copy with saved output. Next, keep hosts consistent with [Package Management](package-management.md). For hardening, continue later to [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md).

## Interview Questions

**1. What is the difference between the SSH private key and the public key, and which one goes on the server?**

??? success "Reveal answer"
    The **private key** stays on the client (your laptop or a secured secrets store). The **public key** is placed in the server user’s `~/.ssh/authorized_keys`. Anyone with the private key can prove identity; the public key alone cannot log in. Never copy the private key to the server or into git.

**2. Why do `~/.ssh` mode `777` or `authorized_keys` mode `644` often break key login?**

??? success "Reveal answer"
    OpenSSH refuses overly open permissions to stop other users on the same host from tampering with your keys. Typical safe modes are **`700`** for `~/.ssh` and **`600`** for `authorized_keys` and private keys. Check with `ls -ld ~/.ssh` and `ls -l ~/.ssh/authorized_keys`.

**3. What does a `Host` stanza in `~/.ssh/config` buy you in daily ops?**

??? success "Reveal answer"
    It stores `HostName`, `User`, `IdentityFile`, `Port`, and optional `ProxyJump` under a short alias. Instead of long commands, you run `ssh bastion` or `ssh app1`. That reduces mistakes during incidents and keeps automation consistent.

**4. When would you choose `rsync` over `scp`?**

??? success "Reveal answer"
    Use **`scp`** for a simple one-off copy. Prefer **`rsync`** when you sync directories repeatedly — it can transfer only changes, preserve permissions with `-a`, and is clearer for deploy artefacts. Both commonly run over SSH (`rsync -e ssh`).

**5. A junior engineer sets `StrictHostKeyChecking=no` in CI to stop prompts. What is the risk, and what is better?**

??? success "Reveal answer"
    The client will accept a new host key without verifying it, which enables man-in-the-middle attacks. Better options: pre-load known host keys in the CI image, use a secrets-managed `known_hosts` file, or carefully use `accept-new` only when the environment is already trusted and controlled.

**6. How do you prove passwordless SSH works for an interview or change ticket?**

??? success "Reveal answer"
    Show `ssh -o BatchMode=yes -i key user@host 'whoami; hostname'` succeeding (BatchMode refuses password prompts), show the public key line in `authorized_keys`, and show key file modes. Attach command output — not the private key.

**7. How does cloud “inject my SSH key at boot” relate to `authorized_keys`?**

??? success "Reveal answer"
    Cloud-init (or the vendor agent) usually appends your uploaded public key to the default user’s `~/.ssh/authorized_keys` on first boot. It is still normal OpenSSH afterwards — you manage extra users and keys the same way. Always verify with a test login and correct permissions after image changes.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Linux Networking Tools](linux-networking-tools.md) *(previous)*
- [Package Management](package-management.md) *(next)*
- [Lab — SSH Secure Access](../labs/linux-ssh-secure-access.md) *(more practice)*
- [SSH Hardening and Firewalls](ssh-hardening-and-firewalls.md) *(later hardening)*

## References

- [OpenSSH documentation](https://www.openssh.com/manual.html) — official manuals  
- [`ssh(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/ssh.1.html) — OpenSSH client  
- [`sshd(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/sshd.8.html) — OpenSSH server  
- [`ssh-keygen(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/ssh-keygen.1.html) — key generation  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
