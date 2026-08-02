---
title: "SSH Hardening and Firewalls"
description: "Harden SSH with keys and safe sshd drop-ins, and control exposure with UFW or firewalld — without locking yourself out."
difficulty: advanced
estimated_time: "55–65 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 13 · Linux Security"
tags:
  - linux
  - ssh
  - firewalld
  - ufw
  - hardening
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

Most internet-facing Linux breaches start with weak Secure Shell (SSH) or open management ports. **SSH hardening** means tightening `sshd` so only the right people can log in, usually with public keys. A **host firewall** (Uncomplicated Firewall (UFW) on Ubuntu, or **firewalld** on RHEL-family systems) blocks unexpected inbound traffic. Together with a cloud security group, these layers protect jump servers (bastions) and application virtual machines (VMs).

A hardened host is not “passwords off and hope”. You must **test config before reload**, keep a second session or serial console open, and **allow SSH in the firewall before you enable default-deny**. One bad `sshd` change or one UFW rule that forgets port 22 can lock you out of a cloud VM. This tutorial teaches safe hardening: keys, drop-in config, `sshd -t`, careful reload, and firewall rules that never cut your own access.

In production, teams also align host firewalls with cloud Network Security Groups (NSGs) / security groups, restrict source Internet Protocol (IP) ranges to office or bastion networks, and monitor auth failures. Fail2ban (next tutorial) can slow password guessing, but it does not fix a wide-open SSH port or a broken `sshd_config`.

This is **Tutorial 20** in **Module 13: Linux Security** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a practice hardening pack you can explain in an interview or change ticket — without locking yourself out.

## Prerequisites

- [Host Monitoring with vmstat, iostat, and sar](host-monitoring-vmstat-iostat-sar.md)
- [SSH and Remote Access](ssh-and-remote-access.md) (keys and basic `ssh` usage)
- A **practice Ubuntu 22.04/24.04 VM** where you already have sudo and SSH access
- Prefer a **second session** open (or cloud serial console) while you change `sshd`
- Do **not** run this lab on a shared production jump server

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how SSH keys, `sshd` drop-ins, and host firewalls work together
- [ ] Install an authorised key and prove login readiness without disabling password auth yet
- [ ] Add a safe `sshd` drop-in, validate with `sshd -t`, and reload without lockout
- [ ] Allow OpenSSH in UFW (or check firewalld) before any default-deny enable
- [ ] Capture evidence that port 22 still listens after the change

## Architecture

SSH hardening sits between the client and the host kernel. Keys authenticate the user. `sshd` enforces policy. The host firewall and cloud security group filter which networks can even reach the SSH port.

![Architecture diagram for SSH Hardening and Firewalls](../assets/excalidraw/linux-ssh-access.svg)

## Theory

### What it is

**SSH** is the encrypted remote login service. The daemon is `sshd`. Client keys live under `~/.ssh/`; authorised public keys for a user live in `~/.ssh/authorized_keys`. Server settings live in `/etc/ssh/sshd_config` and drop-in files under `/etc/ssh/sshd_config.d/` (Ubuntu).

A **host firewall** decides which local ports accept connections. On Ubuntu, **UFW** is a simple front end to `nftables`/`iptables`. On RHEL-like systems, **firewalld** is common. Cloud security groups are a *separate* layer in front of the VM — both must allow SSH for remote access to work.

```bash
ss -lntp | grep -E ':22\b|sshd' || true
sudo sshd -T | grep -Ei 'passwordauthentication|permitrootlogin|pubkeyauthentication|maxauthtries'
sudo ufw status verbose 2>/dev/null || sudo firewall-cmd --list-all 2>/dev/null || true
```

### Why it matters

SSH is the highest-value remote entry point on most Linux servers. Password guessing, reused passwords, and open management ports drive automated compromise. A hardened `sshd` plus a small firewall reduce attack surface even if someone edits a cloud security group by mistake. Lockout is also a real production risk: a bad config at 02:00 can mean an emergency serial-console recovery.

### How it works

1. **Keys** — generate with `ssh-keygen`, install the public key into `authorized_keys`, keep the private key private.
2. **Config** — prefer a drop-in under `sshd_config.d/` instead of rewriting the whole main file.
3. **Test** — always run `sudo sshd -t` (or `sshd -t`) before reload. Fix errors first.
4. **Reload** — `systemctl reload ssh` (Ubuntu) or `systemctl reload sshd` while a second session stays open.
5. **Firewall** — allow OpenSSH / port 22 **before** enabling default-deny. Align with the cloud security group.

Safe hardening knobs for a first change (this lab uses these):

| Setting | Safer first step |
|---------|------------------|
| `MaxAuthTries` | Lower (for example 4) to slow guessing |
| `ClientAliveInterval` / `ClientAliveCountMax` | Drop idle dead sessions |
| `LoginGraceTime` | Limit unauthenticated connection time |
| `X11Forwarding` | `no` on servers that do not need GUI forward |
| `PasswordAuthentication` | Turn off **only after** key login is proven |
| `PermitRootLogin` | Prefer `no` or `prohibit-password` when you have a sudo user |

### Key concepts and comparisons

| Control | Example | Role |
|---------|---------|------|
| Auth method | `PubkeyAuthentication yes` | How you prove identity |
| Identity scope | `AllowUsers deploy` | Who may log in at all |
| Host firewall | UFW / firewalld allow SSH | Local port filter |
| Cloud SG / NSG | Source CIDR = bastion/VPN | Network edge filter |
| Rate limit | fail2ban / equivalent | React to abuse (next tutorial) |

| Stack | Tool |
|-------|------|
| Ubuntu / Debian | UFW (`ufw allow OpenSSH`) |
| RHEL family | firewalld (`firewall-cmd`) |
| Underlying | nftables / iptables |

### Common pitfalls

- Reloading `sshd` after a bad config with only one session — **lockout**.
- Enabling UFW without allowing OpenSSH first — **lockout**.
- Turning off `PasswordAuthentication` before your key works — **lockout**.
- Opening SSH to `0.0.0.0/0` and calling the host “hardened” because passwords are off.
- Host firewall and cloud security group disagreeing until nobody knows the true policy.

## Hands-on Lab

### Objective

On a practice Ubuntu VM, install a lab SSH key, apply a **safe** `sshd` drop-in (no password disable, no port change), validate with `sshd -t`, reload carefully, and ensure the firewall path cannot cut SSH. Save proof under `~/rebash-linux/lab20`.

### Prerequisites

- Ubuntu 22.04/24.04 (or Debian) with an admin user that already has sudo and SSH
- Packages: `openssh-server`, `ufw` (usual on Ubuntu)
- Keep **this SSH session** open until validation passes; open a second session if you can
- Take a VM snapshot before you start, if your hypervisor supports it

### Lab environment

Workspace: `~/rebash-linux/lab20`

```bash
mkdir -p ~/rebash-linux/lab20 && cd ~/rebash-linux/lab20
set -euo pipefail
whoami | tee admin-user.txt
id | tee admin-id.txt
test -n "$(command -v sudo)"
sudo -n true 2>/dev/null || sudo -v
# Prove SSH is listening before we change anything
ss -lntp | tee ss-before.txt
grep -E ':22\b|sshd' ss-before.txt
```

**Expected output:** `admin-user.txt` and `ss-before.txt` exist; something is listening on port 22 (or your SSH port).

!!! danger "Lockout rules for this lab"
    Do **not** set `PasswordAuthentication no` until you have proven key login in a second session.  
    Do **not** change `Port` or `ListenAddress`.  
    Do **not** run `ufw enable` until `ufw status` shows OpenSSH (or port 22) allowed.  
    Prefer `systemctl reload` over `restart` for `sshd`.

### Real-world scenario

Security asks you to harden a new Ubuntu app VM before it goes on the public internet. They want: (1) a documented key for the deploy user path, (2) safer `sshd` defaults that still allow your current login method, and (3) a host firewall that allows SSH before default-deny. You must leave proof for the change ticket and keep a recovery path (second session / serial console).

### Step-by-step tasks

#### Task 1 – Lab key and current sshd effective settings

Create a key used only for this lab, and capture what `sshd` is currently enforcing.

```bash
cd ~/rebash-linux/lab20
set -euo pipefail

# Lab-only key (do not overwrite your real id_ed25519)
KEY="$HOME/rebash-linux/lab20/rebash_lab_ed25519"
if [[ ! -f "$KEY" ]]; then
  ssh-keygen -t ed25519 -N '' -f "$KEY" -C "rebash-lab20@$(hostname)"
fi

mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
touch "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"
grep -Fxf "${KEY}.pub" "$HOME/.ssh/authorized_keys" >/dev/null 2>&1 \
  || cat "${KEY}.pub" >> "$HOME/.ssh/authorized_keys"

# Effective runtime settings (read-only view)
sudo sshd -T | grep -Ei \
  '^(passwordauthentication|pubkeyauthentication|permitrootlogin|maxauthtries|x11forwarding|logingracetime|clientaliveinterval|clientalivecountmax) ' \
  | tee sshd-T-before.txt

ls -l "$KEY" "${KEY}.pub" | tee key-ls.txt
```

**Expected output:** `rebash_lab_ed25519` and `.pub` exist; `sshd-T-before.txt` lists effective settings; public key is in `authorized_keys`.

#### Task 2 – Safe sshd drop-in, test, reload

Add only safe knobs. Do **not** disable passwords in this task.

```bash
cd ~/rebash-linux/lab20
set -euo pipefail

# Keep a second SSH session open if you can (or serial console)
DROP_IN="/etc/ssh/sshd_config.d/99-rebash-lab20.conf"
TMP="$(mktemp)"
cat > "$TMP" << 'EOF'
# REBASH lab20 — safe hardening (does not disable PasswordAuthentication)
MaxAuthTries 4
LoginGraceTime 60
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
EOF

# Install drop-in and validate syntax BEFORE reload
sudo install -m 0644 "$TMP" "$DROP_IN"
rm -f "$TMP"
sudo sshd -t 2>&1 | tee sshd-t.txt
# sshd -t prints nothing on success; confirm exit was 0
test ! -s sshd-t.txt || ! grep -Ei 'error|fatal' sshd-t.txt

# Reload (keeps existing sessions); service name is "ssh" on Ubuntu
sudo systemctl reload ssh 2>/dev/null || sudo systemctl reload sshd

sudo sshd -T | grep -Ei \
  '^(maxauthtries|logingracetime|clientaliveinterval|clientalivecountmax|x11forwarding) ' \
  | tee sshd-T-after.txt

grep -E 'maxauthtries 4|logingracetime 60|x11forwarding no' sshd-T-after.txt
ss -lntp | tee ss-after-reload.txt
grep -E ':22\b|sshd' ss-after-reload.txt
```

**Expected output:** `sshd -t` succeeds; after reload, effective settings show `maxauthtries 4` and `x11forwarding no`; SSH still listens.

#### Task 3 – Firewall: allow SSH first, then enable only if safe

This task never enables UFW unless OpenSSH is already allowed.

```bash
cd ~/rebash-linux/lab20
set -euo pipefail

if command -v ufw >/dev/null 2>&1; then
  sudo ufw status verbose 2>&1 | tee ufw-before.txt

  # Always allow OpenSSH before any enable
  sudo ufw allow OpenSSH comment 'REBASH lab20' 2>&1 | tee ufw-allow.txt || \
    sudo ufw allow 22/tcp comment 'REBASH lab20' 2>&1 | tee ufw-allow.txt

  sudo ufw status verbose 2>&1 | tee ufw-after-allow.txt
  grep -Ei 'OpenSSH|22/tcp' ufw-after-allow.txt

  # Enable only when inactive AND SSH allow is present
  if grep -qi 'Status: inactive' ufw-after-allow.txt; then
    if grep -Ei 'OpenSSH|22/tcp' ufw-after-allow.txt | grep -qi 'ALLOW'; then
      echo 'y' | sudo ufw enable 2>&1 | tee ufw-enable.txt
    else
      echo 'SKIP enable: SSH allow rule not visible' | tee ufw-enable.txt
      exit 1
    fi
  else
    echo 'UFW already active — not forcing re-enable' | tee ufw-enable.txt
  fi

  sudo ufw status verbose 2>&1 | tee ufw-final.txt
else
  # firewalld fallback (RHEL-like practice VMs)
  sudo firewall-cmd --state 2>&1 | tee firewalld-state.txt || true
  sudo firewall-cmd --list-all 2>&1 | tee firewalld-list.txt || true
  echo 'No ufw — captured firewalld (or none)' | tee ufw-final.txt
fi

# Final proof: listener still up
ss -lntp | tee ss-final.txt
grep -E ':22\b|sshd' ss-final.txt

# Pack whatever evidence files exist (UFW vs firewalld hosts differ)
shopt -s nullglob
EVIDENCE=(
  admin-user.txt admin-id.txt
  ss-before.txt ss-after-reload.txt ss-final.txt
  sshd-T-before.txt sshd-T-after.txt sshd-t.txt
  key-ls.txt ufw-final.txt
  ufw-*.txt firewalld-*.txt
)
tar -czf ssh-firewall-evidence.tgz "${EVIDENCE[@]}"
shopt -u nullglob

ls -l ssh-firewall-evidence.tgz | tee evidence-ls.txt
```

**Expected output:** OpenSSH/22 allow is listed (on UFW hosts); SSH still listens; `ssh-firewall-evidence.tgz` is not empty.

### Validation steps

- [ ] Lab key exists under `~/rebash-linux/lab20/` and public key is in `~/.ssh/authorized_keys`
- [ ] `/etc/ssh/sshd_config.d/99-rebash-lab20.conf` exists
- [ ] `sshd -t` succeeded before reload
- [ ] `sshd -T` shows `maxauthtries 4` after reload
- [ ] `ss` still shows SSH listening on port 22 (or your SSH port)
- [ ] UFW (if present) lists OpenSSH or 22/tcp ALLOW before/when enabled
- [ ] `ssh-firewall-evidence.tgz` exists

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `sshd: no hostkeys available` | Broken OpenSSH install | Reinstall `openssh-server`; do not reload until fixed |
| `Reload failed` / connection drop | Bad config or wrong service name | Use serial console; `sshd -t`; fix/remove drop-in; `systemctl reload ssh` |
| Locked out after UFW enable | SSH not allowed first | Serial/console: `ufw allow OpenSSH` then `ufw reload` |
| `Permission denied (publickey)` later | You disabled passwords before testing keys | Keep a console; re-enable passwords temporarily; fix `authorized_keys` modes (`700` / `600`) |
| `ufw: command not found` | Minimal / RHEL image | Use firewalld commands in Task 3 fallback |

### Challenge exercise

Write an executable script `~/rebash-linux/lab20/check-ssh-safe.sh` that exits **0** only if: (1) `sshd -t` is clean, (2) `ss` shows a listener on port 22, and (3) either UFW is inactive **or** OpenSSH/22 is ALLOW. Run it and save stdout to `check-ssh-safe.out`. Do not disable password auth in the challenge.

### Learning outcomes

- Installed a lab SSH key without breaking existing login
- Applied a safe `sshd` drop-in with `sshd -t` before reload
- Allowed SSH in the firewall before enabling default-deny
- Captured evidence suitable for a change ticket

### Cleanup

```bash
cd ~/rebash-linux/lab20
set -euo pipefail

# Remove lab sshd drop-in and reload
sudo rm -f /etc/ssh/sshd_config.d/99-rebash-lab20.conf
sudo sshd -t
sudo systemctl reload ssh 2>/dev/null || sudo systemctl reload sshd || true

# Optional: remove only the lab public key line from authorized_keys
# PUB=$(cat ~/rebash-linux/lab20/rebash_lab_ed25519.pub)
# grep -Fvx "$PUB" ~/.ssh/authorized_keys > ~/.ssh/authorized_keys.tmp && mv ~/.ssh/authorized_keys.tmp ~/.ssh/authorized_keys

# UFW: leave rules if you need them; to remove the lab comment rule manually review `ufw status numbered`
# Keep evidence archive if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab20/` with evidence files
- [ ] You can explain why `sshd -t` and a second session matter
- [ ] You can explain the order: allow SSH → then enable firewall
- [ ] You know when it is safe to turn off `PasswordAuthentication`

## Code Walkthrough

In real servers, SSH and firewall hardening usually follows this order:

1. **Prove access** — second session or serial console open  
2. **Keys first** — install and test key login before disabling passwords  
3. **Small drop-ins** — files under `sshd_config.d/` with clear comments  
4. **Validate then reload** — `sshd -t`, then `systemctl reload`  
5. **Firewall last** — allow OpenSSH, then enable; align with cloud security groups  

Configuration management (Ansible, cloud-init) should own these files. People still keep a break-glass console path.

## Security Considerations

- Never paste private keys into tickets, chat, or git repositories  
- Prefer key-based SSH; disable password auth only after key proof  
- Restrict SSH source CIDRs in the cloud security group, not only on the host  
- Keep `PermitRootLogin no` (or `prohibit-password`) on internet-facing hosts  
- Review auth logs (`journalctl -u ssh` / `/var/log/auth.log`) after changes  

## Common Mistakes

!!! warning "Enabling UFW before allowing OpenSSH"
    Default deny drops your SSH session. **Fix:** `ufw allow OpenSSH` first, confirm with `ufw status`, then enable. Keep serial console ready.

!!! warning "Setting PasswordAuthentication no with only one session"
    A bad key path locks you out. **Fix:** prove key login in a second session, then change auth, then reload.

!!! warning "Editing the whole sshd_config by hand"
    Package upgrades and typos are harder to review. **Fix:** use a drop-in under `sshd_config.d/` and always run `sshd -t`.

!!! warning "Calling the host hardened while SSH is open to the world"
    Keys help, but scanners still find the port. **Fix:** tighten cloud security group source ranges to bastion/VPN/office.

## Best Practices

- Manage `sshd` and firewall rules with configuration management  
- Use short-lived certificates (for example SSH CA) where your platform supports them  
- Prefer bastion / jump host patterns over exposing every VM on port 22  
- Document recovery: serial console, snapshot, break-glass user  
- Test hardening on a practice VM before golden-image bake  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Connection refused after reload | `sshd` failed to start | Serial console; `sshd -t`; `journalctl -u ssh` |
| Timeout after UFW enable | Port 22 not allowed | Console: allow OpenSSH; check cloud SG too |
| `Permission denied (publickey)` | Wrong key / modes / user | Check `authorized_keys`, `chmod 700 ~/.ssh`, `600 authorized_keys` |
| Settings not applied | Drop-in name/order or typo | `sshd -T`; confirm file under `sshd_config.d/` |
| Works from office, not CI | Security group / firewall source mismatch | Align SG and host firewall CIDRs |

## Summary

SSH hardening and host firewalls reduce remote attack surface, but **order and validation prevent lockout**. Install keys, apply small tested drop-ins, reload carefully, and allow SSH before default-deny. Next, learn Mandatory Access Control (MAC), Fail2Ban, auditd, and Pluggable Authentication Modules (PAM) in [SELinux, AppArmor, Fail2Ban, Auditd, and PAM](selinux-apparmor-fail2ban-auditd-pam.md).

## Interview Questions

**1. What is the safe order of operations when hardening SSH and enabling a host firewall on a new cloud VM?**

??? success "Reveal answer"
    Keep a second session or serial console. Install and prove SSH key login. Apply a small `sshd` drop-in and run `sshd -t` before `systemctl reload`. Allow OpenSSH (or port 22) in UFW/firewalld **before** enabling default-deny. Align the cloud security group. Only then consider disabling password authentication. Interviewers want lockout avoidance, not just a list of settings.

**2. Why prefer a drop-in under `/etc/ssh/sshd_config.d/` over rewriting `/etc/ssh/sshd_config`?**

??? success "Reveal answer"
    Drop-ins are easier to review, own in configuration management, and remove in an emergency. The main file may be replaced on package upgrade depending on packaging. A named lab/production drop-in makes intent clear and reduces merge mistakes.

**3. You set `PasswordAuthentication no` and lost access. How do you recover?**

??? success "Reveal answer"
    Use the cloud **serial console**, hypervisor console, or rescue mode. Fix or remove the bad drop-in, restore a working `authorized_keys`, run `sshd -t`, and reload. Temporarily re-enable passwords only if needed, then re-test keys. Prevent by proving key login first and keeping a break-glass path.

**4. How do host UFW/firewalld rules relate to cloud security groups?**

??? success "Reveal answer"
    They are **two layers**. The security group filters traffic before it reaches the VM Network Interface Card (NIC). The host firewall filters on the guest. Both must allow SSH from the intended source. Hardening only one layer while leaving the other open (or blocked) causes false confidence or mysterious timeouts.

**5. Which `sshd` settings would you change first on a practice VM, and which would you delay?**

??? success "Reveal answer"
    First: `MaxAuthTries`, idle keepalive, `LoginGraceTime`, `X11Forwarding no`, confirm `PubkeyAuthentication yes`. Delay: `PasswordAuthentication no`, port changes, and aggressive `AllowUsers` until accounts and keys are proven. Always `sshd -t` and keep a second session.

**6. How would you prove a hardening change is safe for a change ticket?**

??? success "Reveal answer"
    Attach: `sshd -t` success, `sshd -T` before/after for the changed keys, `ss` showing SSH still listening, firewall status showing OpenSSH allowed, and a successful new login test (preferably key-based). Least risk is shown by what you *did not* break.

**7. Why is “keys only, SSH open to 0.0.0.0/0” still weak for a public jump server?**

??? success "Reveal answer"
    Key-only auth stops password guessing, but the service is still exposed to scanning, user enumeration noise, zero-days, and stolen keys. Prefer bastion patterns, source IP restriction in the security group, monitoring of auth failures, and short-lived credentials where possible.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Host Monitoring with vmstat, iostat, and sar](host-monitoring-vmstat-iostat-sar.md) *(previous monitoring)*
- [SSH and Remote Access](ssh-and-remote-access.md) *(SSH basics)*
- [SELinux, AppArmor, Fail2Ban, Auditd, and PAM](selinux-apparmor-fail2ban-auditd-pam.md) *(next)*
- [Lab — SSH Secure Access](../labs/linux-ssh-secure-access.md) *(more practice)*
- [Lab — Firewall Hardening](../labs/linux-firewall-hardening-lab.md) *(more practice)*

## References

- [`sshd_config(5)`](https://man.openbsd.org/sshd_config) — OpenSSH server configuration  
- [OpenSSH documentation](https://www.openssh.com/manual.html) — official manuals  
- [UFW community help (Ubuntu)](https://help.ubuntu.com/community/UFW) — Uncomplicated Firewall  
- [firewalld documentation](https://firewalld.org/documentation/) — firewalld  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
