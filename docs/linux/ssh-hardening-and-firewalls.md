---
title: "SSH Hardening and Firewalls"
description: "Linux harden SSH with keys and safe sshd drop-ins, control exposure with UFW — without locking yourself out."
difficulty: advanced
estimated_time: "55–70 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 13 · Linux Security"
learning_paths:
  - linux-administrator
  - devops-engineer
  - security-engineer
tags:
  - linux
  - ssh
  - ufw
  - hardening
  - beginners
prerequisites:
  - linux/host-monitoring-vmstat-iostat-sar
  - linux/ssh-and-remote-access
next:
  - linux/selinux-apparmor-fail2ban-auditd-pam
related:
  - labs/linux-ssh-secure-access
  - labs/linux-firewall-hardening-lab
labs:
  - labs/linux-ssh-secure-access
  - labs/linux-firewall-hardening-lab
interview: interview/linux
comments: false
---

# SSH Hardening and Firewalls

## Overview

**Secure Shell (SSH)** is how you reach almost every Linux server. Hardening and host firewalls reduce attack surface — and the first rule is: never lock yourself out without console access.

**Plain problem:** Default SSH on the public internet gets password-guessing bots within minutes. Teams use **SSH keys**, disable password login, limit users, and put a **firewall** in front — only allowing SSH from trusted networks.

This tutorial covers:

1. SSH keys and safe **`sshd`** drop-in configuration
2. **Uncomplicated Firewall (UFW)** on Ubuntu (and when **firewalld** appears on RHEL)
3. A lab that **breaks** SSH config, **fixes** it, and proves access still works

This is **Tutorial 13a** in **Module 13: Linux Security** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series.

## Prerequisites

- Ubuntu practice VM with SSH access (keep a **console** or cloud “serial console” backup — never lock your only path)
- [SSH and Remote Access](ssh-and-remote-access.md) completed
- `sudo` privileges
- Two terminal sessions recommended (one stays connected while testing)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain SSH keys vs passwords in plain language
- [ ] Add a safe **`sshd`** drop-in (without closing your session)
- [ ] Enable **UFW** allowing SSH before default deny
- [ ] Validate config with `sshd -t` before reload
- [ ] Recover from a bad drop-in using console or a second session
- [ ] Answer fresher interview questions on SSH hardening

## Architecture

Your laptop runs an **SSH client**. The server runs **`sshd`** (daemon) listening on port 22 (by default). **UFW** sits in the kernel **netfilter** path and drops packets before they reach `sshd` unless rules allow them.

![Linux SSH and firewall layers](../assets/excalidraw/linux-ssh-access.svg)

## Theory

### The problem (before any jargon)

Internship day one: someone disables password auth but forgets to install your public key. The whole team uses the cloud console to recover. Hardening is good; **order of operations** matters: key first, test second, disable password third.

### SSH keys (simple words)

**Analogy:** A **password** is repeating a secret phrase through a letterbox — bots can guess forever. An **SSH key pair** is a unique lock (public key on server) and key (private key on your laptop) — mathematically hard to forge.

| Piece | Where it lives |
|-------|----------------|
| Private key | Your laptop (`~/.ssh/id_ed25519`) — never share |
| Public key | Server `~/.ssh/authorized_keys` |

Generate Ed25519 key (modern default):

``` {.bash .ra-terminal title="Terminal"}
ssh-keygen -t ed25519 -C "you@laptop" -f ~/.ssh/id_ed25519_lab
```

**Interview line:** “I use key-based auth, disable root password login, and validate sshd config with `sshd -t` before reload.”

### sshd hardening (safe subset for lab)

Use drop-ins under `/etc/ssh/sshd_config.d/` — do not edit the main file blindly.

| Setting | Lab-safe value | Why |
|---------|----------------|-----|
| `PasswordAuthentication no` | After keys work | Stops brute force |
| `PermitRootLogin prohibit-password` or `no` | Restrict root | Limit blast radius |
| `MaxAuthTries 3` | Lower tries | Slow attackers |
| `AllowUsers yourname` | Optional | Explicit allow list |

Always:

``` {.bash .ra-terminal title="Terminal"}
sudo sshd -t && sudo systemctl reload ssh
```

Keep one existing session open while testing a **new** session.

### UFW firewall

**Analogy:** **UFW** is a bouncer list — “allow SSH (22), deny everything else by default.”

``` {.bash .ra-terminal title="Terminal"}
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose
```

On RHEL family, **firewalld** replaces UFW (`firewall-cmd`). Concept is the same: explicit allow before default deny.

### Common pitfalls

- Enabling UFW before allowing SSH — locked out
- Disabling passwords before copying your public key
- Editing `sshd_config` without `sshd -t`
- Changing SSH port without updating firewall and documentation

## Hands-on Lab

### Objective

Confirm key auth, add a lab **`sshd`** drop-in, enable **UFW**, intentionally introduce a **syntax error**, **fix** it, and prove SSH still works — evidence under `~/rebash-linux/lab20`.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | SSH + console access |
| Second SSH session | Strongly recommended |
| Ed25519 key | Generated in Task 1 |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab20 && cd ~/rebash-linux/lab20
sudo ufw status | tee ufw-before.txt
```

### Real-world scenario

Security ticket: “Harden SSH on the dev sandbox — keys only, UFW on, document proof. Do not lock the team out.” You implement drop-in config, firewall, and validation logs.

### Step-by-step tasks

#### Task 1 – Key-based login proof

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab20
test -f ~/.ssh/id_ed25519 || ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys
ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new localhost 'echo key-auth-ok' | tee key-auth-proof.txt
grep -q key-auth-ok key-auth-proof.txt
```

!!! example "Expected output"
    `key-auth-proof.txt` contains `key-auth-ok` from localhost SSH using keys.


#### Task 2 – sshd drop-in and UFW

Create `99-rebash-lab.conf`:

```text title="99-rebash-lab.conf"
# REBASH lab20 — hardening drop-in (lab VM only)
PasswordAuthentication no
PermitRootLogin prohibit-password
MaxAuthTries 3
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab20
sudo cp 99-rebash-lab.conf /etc/ssh/sshd_config.d/99-rebash-lab.conf
sudo sshd -t 2>&1 | tee sshd-test-ok.txt
sudo systemctl reload ssh
ssh -o BatchMode=yes localhost 'echo after-hardening-ok' | tee ssh-after-harden.txt
sudo ufw allow OpenSSH
echo "y" | sudo ufw enable
sudo ufw status verbose | tee ufw-after.txt
grep -q 'Status: active' ufw-after.txt
```

!!! example "Expected output"
    `sshd-test-ok.txt` has no errors. SSH still works. UFW status is active with OpenSSH allowed.


#### Task 3 – Break, fix, and prove (bad sshd line)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab20
echo 'BadDirective yes' | sudo tee /etc/ssh/sshd_config.d/99-rebash-broken.conf >/dev/null
sudo sshd -t 2>&1 | tee sshd-test-broken.txt || true
grep -qi 'bad\|error\|unknown' sshd-test-broken.txt
sudo rm -f /etc/ssh/sshd_config.d/99-rebash-broken.conf
sudo sshd -t 2>&1 | tee sshd-test-fixed.txt
ssh -o BatchMode=yes localhost 'echo recovery-ok' | tee ssh-recovery-proof.txt
echo "lab20 ssh-firewall OK" | tee evidence.txt
```

!!! example "Expected output"
    `sshd-test-broken.txt` shows config error. After removing bad file, `ssh-recovery-proof.txt` shows `recovery-ok`.


### Validation steps

- [ ] Key auth works before password disable path
- [ ] `sshd -t` clean after good drop-in
- [ ] UFW active with OpenSSH rule
- [ ] Bad config caught by `sshd -t` before reload

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| SSH hang after reload | Bad config applied | Console in; remove bad drop-in |
| UFW lockout | Enabled before allow | Console: `ufw allow OpenSSH` |
| Key auth fails | Wrong permissions | `chmod 700 ~/.ssh`; `600 authorized_keys` |
| `sshd -t` fails | Typo in drop-in | Fix file; test before reload |

### Challenge exercise

Document your cloud provider’s “serial console” recovery path in `recovery-runbook.md` (three bullet steps).

### Learning outcomes

- You hardened SSH without losing access
- You enabled UFW in the correct order
- You used `sshd -t` as a safety gate

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
sudo rm -f /etc/ssh/sshd_config.d/99-rebash-lab.conf
sudo sshd -t && sudo systemctl reload ssh
# Optional: sudo ufw disable   # only on disposable lab VM
```

## Validation

- [ ] Evidence under `~/rebash-linux/lab20`
- [ ] Can explain key-before-password order
- [ ] Ready for MAC / Fail2Ban tutorial next

## Code Walkthrough

1. **`BatchMode=yes`** — non-interactive SSH test; fails if password required.
2. **Drop-in directory** — modular config; remove one file to roll back.
3. **`sshd -t`** — syntax test; never reload on failure.
4. **`ufw allow OpenSSH`** — before `enable`; uses profile for port 22.
5. **Break task** — proves validation catches typos before outage.

## Security Considerations

- Private keys: passphrase on laptops; never commit to Git.
- `AllowUsers` / `AllowGroups` reduce exposure on shared hosts.
- Consider `AllowTcpForwarding no` on sensitive jump boxes (app-specific).
- Fail2Ban (next tutorial) complements SSH hardening.
- Cloud Security Groups are another firewall layer — align with UFW rules.

## Common Mistakes

!!! warning "Disabling passwords before keys work"
    Always verify key login in a second session first.

!!! warning "Reloading sshd without sshd -t"
    One typo can lock every admin out until console recovery.

!!! warning "UFW enable without allow rule"
    Default deny blocks SSH — use console or provider firewall to recover.

## Best Practices

- Use Ed25519 or RSA 4096 keys; rotate on laptop rebuild
- Manage `authorized_keys` with configuration management
- Centralise bastion/jump hosts for production SSH
- Log auth failures (`journalctl -u ssh`)
- Document port, allowed networks, and break-glass (emergency) access

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Permission denied (publickey) | Key not in authorized_keys | Copy pubkey; fix perms |
| Connection refused | sshd down / wrong port | `systemctl status ssh`; `ss -tlnp` |
| Timeout | Firewall / Security Group | UFW status; cloud SG rules |
| Config ignored | Wrong Include path | Check `sshd_config` Include |

## Summary

Harden **SSH** with **keys first**, **`sshd` drop-ins**, and **`sshd -t` before reload**. Put **UFW** (or firewalld) in front with **allow SSH before default deny**. Always keep a recovery path — console or second session — and prove access after every change.

## Interview Questions

**1. Why prefer SSH keys over passwords on servers?**

??? success "Reveal answer"
    Keys are strong cryptographic credentials resistant to brute force. Passwords on internet-exposed SSH get guessed. Best practice: key-based auth, disable password authentication after keys verified.

**2. What does sshd -t do and when do you run it?**

??? success "Reveal answer"
    Tests **`sshd`** configuration syntax without applying. Run before every `systemctl reload ssh` to catch typos that would lock admins out or prevent the daemon starting.

**3. Safe order to harden SSH on a live server?**

??? success "Reveal answer"
    Install/copy public key → verify key login in **new session** → add drop-in hardening → `sshd -t` → reload → disable password auth → keep console access documented.

**4. What is UFW and why allow OpenSSH before enable?**

??? success "Reveal answer"
    **UFW** is Ubuntu’s frontend to netfilter firewall rules. `ufw enable` applies default deny. Without `allow OpenSSH` first, SSH packets drop and you lose remote access.

**5. PermitRootLogin — what should production use?**

??? success "Reveal answer"
    Usually **`no`** or **`prohibit-password`** (keys only if root SSH allowed at all). Better: disable root SSH; admins use sudo from named users — smaller blast radius.

**6. You changed sshd and lost SSH. Recovery steps?**

??? success "Reveal answer"
    Use cloud serial/VNC console or provider “EC2 serial console”. Log in locally, remove bad drop-in under `/etc/ssh/sshd_config.d/`, run `sshd -t`, restart ssh. Fix Security Group/UFW if network block.

**7. UFW vs cloud Security Group — difference?**

??? success "Reveal answer"
    **Security Group** (or Network Security Group) filters at the hypervisor/cloud edge. **UFW** filters on the host OS. Both must allow SSH for remote access — defence in depth uses both.

## Related Tutorials

- Previous: [Host Monitoring — vmstat, iostat, and sar](host-monitoring-vmstat-iostat-sar.md)
- Next: [SELinux, AppArmor, Fail2Ban, Auditd, and PAM](selinux-apparmor-fail2ban-auditd-pam.md)
- Prerequisite: [SSH and Remote Access](ssh-and-remote-access.md)

## References

- [OpenSSH sshd_config man page](https://manpages.ubuntu.com/manpages/noble/man5/sshd_config.5.html)
- [UFW documentation](https://help.ubuntu.com/community/UFW)
- [CIS SSH benchmark guidance](https://www.cisecurity.org/cis-benchmarks)
