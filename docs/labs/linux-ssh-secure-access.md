---
title: "Lab — Configure SSH Secure Access"
description: "Generate SSH keys, disable password login for a lab user, harden sshd_config safely, and prove remote access still works."
difficulty: beginner
estimated_time: "40–50 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - ssh
  - security
comments: false
---

# Lab — Configure SSH Secure Access

## Lab Overview

**Purpose:** Configure Secure Shell (SSH) the way Cloud and DevOps teams expect: keys first, least privilege, no accidental lockout.

**Scenario:** A new Ubuntu VM must accept your laptop key only — password authentication for remote login should be off for the ops user.

**Expected outcome:** Key-based SSH works; password auth is disabled (or documented why not yet); a backup console path exists.

!!! tip "This is a lab, not a tutorial"
    Keep a second session or console open before restarting `sshd`. Lockout recovery is part of the exercise.

## Business Scenario

Security asked that bastion and app VMs stop accepting password SSH. You own the first lab host and must implement key auth without breaking the team’s access pattern.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Generate an Ed25519 key pair and install the public key
- [ ] Harden `sshd_config` with safe defaults
- [ ] Validate config with `sshd -t` before reload
- [ ] Prove login still works after password auth is disabled
- [ ] Document rollback if console access is required

## Prerequisites

### Knowledge

- [SSH and Remote Access](../linux/ssh-and-remote-access.md)
- [Users, Groups, and sudo](../linux/users-groups-and-sudo.md)
- [SSH Hardening and Firewalls](../linux/ssh-hardening-and-firewalls.md) (skim)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu VM with `openssh-server` | Cloud images usually include it |
| Client with `ssh` / `ssh-keygen` | Laptop or second host |
| Console access | Hypervisor or cloud serial console |

**Estimated cost:** £0.

## Environment

```bash
mkdir -p ~/rebash-lab-linux-ssh
cd ~/rebash-lab-linux-ssh
```

Use a disposable VM. Do **not** harden a shared production bastion during this lab.

## Initial State

SSH password login may still work. You will add keys, then tighten settings.

## Lab Tasks

### Task 1 — Generate and install a key

**On the client:**

```bash
ssh-keygen -t ed25519 -f ~/.ssh/rebash_lab_ed25519 -C "rebash-lab-$(date +%Y%m%d)" -N ""
ssh-copy-id -i ~/.ssh/rebash_lab_ed25519.pub USER@HOST
# Or manually append the .pub line to ~/.ssh/authorized_keys on the server
```

**On the server (as the target user):**

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
ls -la ~/.ssh
```

Test a **new** session:

```bash
ssh -i ~/.ssh/rebash_lab_ed25519 USER@HOST 'echo OK && whoami'
```

### Task 2 — Snapshot current sshd settings

```bash
sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.pre-lab
sudo sshd -T | egrep '^(passwordauthentication|permitrootlogin|pubkeyauthentication|challengeresponseauthentication|kbdinteractiveauthentication) ' \
  | tee ~/rebash-lab-linux-ssh/sshd-before.txt
```

### Task 3 — Apply a drop-in hardening file

Prefer a drop-in over editing the whole file when supported:

```bash
sudo mkdir -p /etc/ssh/sshd_config.d
sudo tee /etc/ssh/sshd_config.d/99-rebash-lab.conf >/dev/null <<'EOF'
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
sudo sshd -t
sudo systemctl reload ssh || sudo systemctl reload sshd
```

Keep your **existing** SSH session open until a new key login succeeds.

### Task 4 — Negative test

From the client, attempt password auth (should fail):

```bash
ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no USER@HOST || echo "password refused (expected)"
```

Confirm key auth still works. Record results:

```bash
sudo sshd -T | egrep '^(passwordauthentication|permitrootlogin|pubkeyauthentication) ' \
  | tee ~/rebash-lab-linux-ssh/sshd-after.txt
```

### Task 5 — Firewall awareness (optional)

If `ufw` is active, ensure SSH is allowed **before** enabling UFW:

```bash
sudo ufw status || true
sudo ufw allow OpenSSH
```

## Validation

- [ ] Key login succeeds with the lab key
- [ ] Password SSH is refused (or documented exception)
- [ ] `sshd -t` passed before reload
- [ ] `sshd-before.txt` / `sshd-after.txt` saved under the workspace

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| Locked out | Reloaded before key worked | Use console; restore `.pre-lab` or remove drop-in |
| `sshd -t` fails | Typo in drop-in | Fix file; do not reload until test passes |
| Permission denied (publickey) | Bad modes on `.ssh` | `700` on dir, `600` on `authorized_keys` |

## Challenge Extensions

- Require a specific `Match User` for a second account
- Add `AllowUsers` for the ops account only
- Move SSH to a non-default port **and** update the firewall

## Cleanup

```bash
# Restore previous config if this was only a lab host
sudo rm -f /etc/ssh/sshd_config.d/99-rebash-lab.conf
sudo cp -a /etc/ssh/sshd_config.pre-lab /etc/ssh/sshd_config 2>/dev/null || true
sudo sshd -t && sudo systemctl reload ssh || sudo systemctl reload sshd
rm -rf ~/rebash-lab-linux-ssh
# Optionally remove the lab key from authorized_keys and delete client key files
```

## Production Discussion

Production uses configuration management (Ansible/cloud-init), hardware security modules or agent-backed keys, and bastion/Session Manager patterns. The lab teaches the same controls without the fleet tooling.

## Best Practices

- Always validate with a second session before closing the first
- Prefer Ed25519 keys; protect private keys with passphrases in real use
- Never disable the only admin path without console/out-of-band access

## Common Mistakes

| Mistake | Why it happens | Correct approach |
|---------|----------------|------------------|
| Editing live `sshd_config` without `sshd -t` | Speed | Test, then reload |
| Disabling passwords before installing keys | Order error | Keys first |
| Leaving root password SSH on | Defaults | `PermitRootLogin no` |

## Success Criteria

You can explain the exact order of operations that prevents lockout and show before/after `sshd -T` evidence.

## Reflection Questions

1. Why is `sshd -t` mandatory before reload?
2. What out-of-band access do you need in a cloud VPC?
3. How do certificates (SSH CA) change this design?

## Interview Connection

Classic prompt: “Harden SSH on a new server without locking yourself out.” Answer with keys → second session → `sshd -t` → reload → negative test.

## Related Tutorials

- [SSH and Remote Access](../linux/ssh-and-remote-access.md)
- [SSH Hardening and Firewalls](../linux/ssh-hardening-and-firewalls.md)
- Next lab: [Users, Groups, Permissions](linux-users-permissions-lab.md)
- Cheat sheet: [Linux](../cheatsheets/linux.md)

## References

- [OpenSSH manual pages](https://www.openssh.com/manual.html)
- [Ubuntu SSH documentation](https://ubuntu.com/server/docs/openssh-server)
