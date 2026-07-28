---
title: Linux Security Hardening Basics
description: Apply baseline hardening with SSH, firewalls, patching, fail2ban, and CIS-aligned controls.
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - security
  - hardening
  - ssh
  - firewall
prerequisites:
  - Completion of Modules 1–5 Linux tutorials
  - SSH and basic networking knowledge
comments: false
---

# Linux Security Hardening Basics

## Overview

Every Linux server exposed to a network — whether on the public internet or a corporate VLAN — needs baseline hardening before it handles production workloads. Unpatched packages, open SSH with password authentication, missing firewalls, and unnecessary services create an attack surface that automated scanners exploit within minutes of exposure.

This tutorial covers practical hardening steps: **SSH configuration**, **host firewalls** (UFW and firewalld), **patch management**, an introduction to **fail2ban**, and alignment with **CIS Benchmark** principles. These controls form the foundation of DevSecOps and compliance programs.

This tutorial is part of **Module 6: Storage, Logs, Networking & Operations** in the REBASH Academy Linux series.

## Prerequisites

- Complete [SSH and Remote Administration](ssh-remote-administration.md) and [Linux Networking Essentials](linux-networking-essentials.md)
- A non-production Linux VM for lab exercises (mistakes can lock you out)
- `sudo` privileges and console/out-of-band access as a safety net
- Basic understanding of TCP ports and authentication

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Harden SSH with key-based auth, disable root login, and restrict users
- [ ] Configure UFW (Debian/Ubuntu) or firewalld (RHEL) with minimal required rules
- [ ] Apply security updates and enable unattended patching where appropriate
- [ ] Explain fail2ban's role in blocking brute-force attacks
- [ ] Map hardening actions to CIS Benchmark categories for audit readiness

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Defense in depth

Security is layered — no single control is sufficient:

1. **Network:** Firewall, security groups, segmentation
2. **Access:** SSH keys, MFA, sudo policies
3. **System:** Patching, minimal packages, file permissions
4. **Detection:** Logging, fail2ban, intrusion detection
5. **Response:** Backups, incident runbooks, forensics capability

### SSH hardening

SSH is the primary admin entry point and the most attacked service. Key settings in `/etc/ssh/sshd_config`:

| Directive | Recommended | Why |
|-----------|-------------|-----|
| `PermitRootLogin` | `no` or `prohibit-password` | Prevents direct root brute-force |
| `PasswordAuthentication` | `no` | Forces key-based auth |
| `PubkeyAuthentication` | `yes` | Enable public key login |
| `PermitEmptyPasswords` | `no` | Block empty password accounts |
| `MaxAuthTries` | `3` | Limit brute-force attempts per connection |
| `AllowUsers` / `AllowGroups` | Specific admins | Restrict who can SSH |
| `X11Forwarding` | `no` | Disable unless needed |
| `Protocol` | 2 (default on modern) | Legacy check |

Always validate with `sshd -t` before restarting. Keep a second session open during changes.

### Host firewalls

**UFW** (Uncomplicated Firewall) on Debian/Ubuntu wraps iptables/nftables:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw enable
```

**firewalld** on RHEL/Fedora uses zones:

```bash
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --remove-service=cockpit  # example
sudo firewall-cmd --reload
```

Principle: **default deny inbound**, allow only required ports (SSH, HTTP/S, app-specific).

### Patch management

Unpatched CVEs are a leading breach vector:

- **Debian/Ubuntu:** `apt update && apt upgrade`; unattended-upgrades for automation
- **RHEL:** `dnf update`; dnf-automatic or Satellite

Schedule regular maintenance windows; test patches in staging first.

### fail2ban

**fail2ban** monitors log files (e.g., `/var/log/auth.log`, journal) for failed login patterns and temporarily bans offending IPs via firewall rules.

Typical `/etc/fail2ban/jail.local`:

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
bantime = 3600
```

Not a substitute for key-only SSH — it reduces noise from internet-wide scanning.

### CIS Benchmark basics

The [CIS Linux Benchmark](https://www.cisecurity.org/cis-benchmarks) provides prioritized controls:

| Category | Examples |
|----------|----------|
| Initial setup | Filesystem partitions, bootloader permissions |
| Services | Disable unused services (`avahi`, `cups`) |
| Network | Disable unused protocols, host firewall |
| Logging and auditing | rsyslog/journald, auditd |
| Access control | Password policies, sudo logging |
| System maintenance | Patch process, integrity checking |

Use **CIS-CAT** or **Lynis** for automated assessment. Level 1 = essential; Level 2 = stricter (may impact usability).

### Additional hardening

- Remove or disable unused packages and services
- Configure `sudo` with logging (`/var/log/auth.log`)
- Set `/etc/login.defs` password aging policies
- Enable SELinux (RHEL) or AppArmor (Ubuntu) — do not disable without reason
- Restrict file permissions on sensitive files (`/etc/shadow`, SSH keys)

## Hands-on Lab

### Step 1 – Baseline security audit

```bash
echo "=== Listening ports ==="
sudo ss -tulpn
echo "=== Failed SSH attempts (last hour) ==="
sudo journalctl -u ssh -u sshd --since "1 hour ago" 2>/dev/null | grep -i failed | tail -5 || true
echo "=== Pending updates ==="
sudo apt update 2>/dev/null && apt list --upgradable 2>/dev/null | head -5 || \
  sudo dnf check-update 2>/dev/null | head -5 || true
```

**Expected output:** List of open ports, any failed auth lines, and available security updates.

### Step 2 – Review current SSH configuration

```bash
sudo sshd -T | grep -E "permitrootlogin|passwordauthentication|pubkeyauthentication|maxauthtries"
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries)" \
  /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null
```

**Expected output:** Effective settings — note whether password auth is enabled (common default on fresh installs).

### Step 3 – Harden SSH (lab VM only)

Create a drop-in config (safer than editing main file):

```bash
sudo tee /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
X11Forwarding no
AllowUsers YOUR_USERNAME
EOF
# Replace YOUR_USERNAME with your actual user before applying:
sudo sed -i "s/YOUR_USERNAME/$USER/" /etc/ssh/sshd_config.d/99-hardening.conf
sudo sshd -t && echo "Config syntax OK"
```

**Expected output:** `Config syntax OK` — do not restart until you confirm key-based login works.

Verify key auth in a **second terminal** before:

```bash
sudo systemctl reload sshd 2>/dev/null || sudo systemctl reload ssh
```

### Step 4 – Configure UFW (Ubuntu/Debian)

```bash
sudo ufw status verbose 2>/dev/null || echo "UFW not installed"
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw --force enable
sudo ufw status numbered
```

**Expected output:**

```text
Status: active
To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
```

### Step 4b – Configure firewalld (RHEL alternative)

```bash
sudo firewall-cmd --state 2>/dev/null || echo "firewalld not active"
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload
sudo firewall-cmd --list-all
```

**Expected output:** `services: ssh dhcpv6-client` in the public zone.

### Step 5 – Apply security updates

```bash
sudo apt upgrade -y 2>/dev/null | tail -5 || sudo dnf upgrade -y 2>/dev/null | tail -5
```

**Expected output:** Packages upgraded or "0 upgraded" if current.

### Step 6 – Install and configure fail2ban

```bash
sudo apt install -y fail2ban 2>/dev/null || sudo dnf install -y fail2ban 2>/dev/null || true
sudo tee /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
EOF
sudo systemctl enable --now fail2ban
sudo fail2ban-client status sshd 2>/dev/null || sudo fail2ban-client status
```

**Expected output:** fail2ban running with sshd jail enabled.

### Step 7 – Disable unnecessary services

```bash
systemctl list-unit-files --type=service --state=enabled | \
  grep -E "bluetooth|cups|avahi" || echo "No common unnecessary services enabled"
# Example disable (if present and unused):
# sudo systemctl disable --now avahi-daemon
```

**Expected output:** Audit of enabled services; disable only what you confirm is unused.

### Step 8 – Run Lynis quick audit (optional)

```bash
sudo apt install -y lynis 2>/dev/null || sudo dnf install -y lynis 2>/dev/null || true
sudo lynis audit system --quick 2>/dev/null | tail -20
```

**Expected output:** Hardening index score and suggestions aligned with CIS-style checks.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `sudo sshd -T` | Dump effective SSH configuration |
| `sudo sshd -t` | Test SSH config syntax |
| `sudo systemctl reload sshd` | Apply SSH changes without dropping sessions |
| `sudo ufw enable` | Enable UFW firewall |
| `sudo ufw allow 443/tcp` | Allow HTTPS inbound |
| `sudo ufw status numbered` | Show rules with index numbers |
| `sudo ufw delete N` | Delete rule by index |
| `sudo firewall-cmd --list-all` | Show firewalld zone config |
| `sudo firewall-cmd --permanent --add-port=8080/tcp` | Open port permanently |
| `sudo apt update && sudo apt upgrade` | Apply Debian/Ubuntu updates |
| `sudo dnf update` | Apply RHEL/Fedora updates |
| `sudo fail2ban-client status sshd` | fail2ban sshd jail status |
| `sudo fail2ban-client set sshd unbanip IP` | Unban an IP address |
| `systemctl list-units --type=service --state=running` | Audit running services |
| `sudo lynis audit system` | Security audit scan |
| `sudo aa-status` | AppArmor status (Ubuntu) |
| `getenforce` | SELinux status (RHEL) |

## Code Examples

### SSH hardening drop-in (production template)

```ini
# /etc/ssh/sshd_config.d/99-production.conf
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers deploy admin
```

### UFW web server profile

```bash
#!/bin/bash
set -euo pipefail
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status verbose
```

### Unattended upgrades (Debian/Ubuntu)

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
# Verify: /etc/apt/apt.conf.d/50unattended-upgrades
```

### CIS-style service disable script

```bash
#!/bin/bash
# disable-unused-services.sh — review before running
for svc in avahi-daemon cups bluetooth; do
  if systemctl is-enabled "$svc" &>/dev/null; then
    echo "Disabling $svc"
    sudo systemctl disable --now "$svc"
  fi
done
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Disabling password auth before testing SSH keys"
    You will lock yourself out. Always verify key login in a second session before `PasswordAuthentication no`.

!!! warning "Enabling firewall without allowing SSH"
    UFW/f firewalld with default deny and no SSH rule blocks your access. Allow SSH **before** enabling.

!!! warning "Editing sshd_config directly without drop-ins"
    Package updates can overwrite main config. Use `/etc/ssh/sshd_config.d/*.conf` for custom settings.

!!! warning "Installing fail2ban instead of fixing root cause"
    fail2ban mitigates brute force but does not replace key-only auth and network-level controls.

!!! warning "Applying CIS Level 2 blindly"
    Strict controls can break applications. Assess impact; implement Level 1 first.

## Best Practices

!!! tip "Use infrastructure-as-code for hardening"
    Manage firewall rules, SSH config, and packages with Ansible, cloud-init, or golden AMIs.

!!! tip "Maintain break-glass access"
    Console access (cloud serial console, IPMI, hypervisor) for recovery when SSH is misconfigured.

!!! tip "Centralize authentication"
    LDAP, SSO, or certificate-based auth scales better than per-server key management.

!!! tip "Log and alert on auth failures"
    Ship `/var/log/auth.log` or journal SSH events to SIEM; alert on spikes.

!!! tip "Regular vulnerability scanning"
    Combine patching with Nessus, OpenSCAP, or cloud-native scanners for continuous assessment.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Locked out after SSH change | Password disabled, no key | Use console; fix `sshd_config`; restore from backup |
| `sshd -t` fails | Syntax error in config | Check drop-in files; remove invalid directives |
| UFW blocks application | Port not allowed | `ufw allow PORT/tcp`; verify with `ss -tln` |
| fail2ban banned your IP | Failed login attempts | `fail2ban-client set sshd unbanip YOUR_IP` |
| Updates require reboot | Kernel/libc patch | Schedule reboot; check `/var/run/reboot-required` |
| SELinux denies service | Policy violation | Check `audit2why`; set correct context or boolean |
| firewalld rules not active | Missing `--permanent` | Add `--permanent` then `firewall-cmd --reload` |
| Lynis low hardening score | Baseline defaults | Prioritize CIS Level 1 failures; track progress over time |

## Summary

- Harden SSH first: disable root password login, enforce keys, limit users, validate with `sshd -t`.
- Enable host firewalls with default-deny inbound — UFW on Debian, firewalld on RHEL.
- Apply security patches regularly; automate with unattended-upgrades or equivalent.
- fail2ban adds brute-force protection but complements — not replaces — strong authentication.
- Map controls to CIS Benchmark categories for audit-ready baseline hardening.

## Interview Questions

**1. What SSH settings do you change first on a new production server?**

*Sample answer:* Disable root login (`PermitRootLogin no`), disable password authentication, enable pubkey auth, set MaxAuthTries, and restrict AllowUsers. Validate config with `sshd -t` and test keys before reload.

**2. UFW vs firewalld — when do you use each?**

*Sample answer:* UFW is common on Debian/Ubuntu — simple syntax for iptables/nftables. firewalld on RHEL uses zones and runtime/permanent rules. Both implement host firewall; choice follows distribution.

**3. What is fail2ban and how does it work?**

*Sample answer:* fail2ban parses logs for patterns like failed SSH logins and adds firewall rules to block offending IPs temporarily. Configured via jails in `/etc/fail2ban/jail.local`.

**4. Why disable password authentication if you have a strong password?**

*Sample answer:* Passwords are vulnerable to brute force at scale. SSH keys are cryptographically stronger, not transmitted on each login, and pair well with automation. Password auth should be off for admin access.

**5. What is the CIS Benchmark?**

*Sample answer:* Center for Internet Security publishes consensus hardening guidelines for OS and software. Level 1 is practical baseline; Level 2 is stricter for high-security environments.

**6. How do you safely apply SSH config changes?**

*Sample answer:* Edit drop-in files, run `sshd -t`, keep an existing session open, reload sshd, test new connection in parallel before closing old session.

**7. What ports should a minimal web server firewall allow?**

*Sample answer:* SSH (22 or custom), HTTP (80), HTTPS (443), and any app-specific ports. Deny everything else inbound.

**8. How do you verify a server is fully patched?**

*Sample answer:* Run package manager check (`apt list --upgradable`, `dnf check-update`), review security advisories, confirm last update time, and check if reboot is required for kernel updates.

**9. What is the principle of least privilege in Linux hardening?**

*Sample answer:* Run services as non-root users, disable unused services, grant sudo only where needed, restrict SSH to admin accounts, and minimize open ports.

**10. How does SELinux/AppArmor contribute to hardening?**

*Sample answer:* Mandatory access control confines processes to allowed resources even if compromised. Policies limit damage from exploits beyond discretionary file permissions.

1. How would you explain linux security hardening basics to a junior engineer in two minutes?
2. What production failure mode appears when teams ignore linux security hardening basics?
3. Which metrics or logs would you check first when linux security hardening basics misbehaves?
4. What is a secure default related to linux security hardening basics?
5. How would you validate a change involving linux security hardening basics in CI or a staging environment?
6. What trade-off would you accept to simplify operations around linux security hardening basics?
7. Describe a common anti-pattern with linux security hardening basics and how you fix it.
8. How does linux security hardening basics interact with networking, identity, or storage in a real system?
9. What would you put on a runbook checklist for linux security hardening basics?
10. When would you intentionally not follow the default approach taught here?

## Related Tutorials

- [Linux – Category Overview](index.md)
- [File Archiving and Compression](file-archiving-and-compression.md) *(previous)*
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md) *(next)*
- [SSH and Remote Administration](ssh-remote-administration.md)
- [Linux Networking Essentials](linux-networking-essentials.md)
- [User and Group Management](user-and-group-management.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [OpenSSH sshd_config man page](https://man7.org/linux/man-pages/man5/sshd_config.5.html)
- [UFW documentation](https://help.ubuntu.com/community/UFW)
- [firewalld documentation](https://firewalld.org/documentation/)
- [fail2ban wiki](https://github.com/fail2ban/fail2ban)
- [Lynis security auditing](https://cisofy.com/lynis/)
- [REBASH Academy – Linux Overview](index.md)
