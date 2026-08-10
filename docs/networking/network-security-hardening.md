---
title: "Network Hardening"
description: "Learn network hardening — attack surface reduction, secure protocols, patch management, Linux and device hardening, and layered security practices."
difficulty: intermediate
estimated_time: "120 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 8 · Network Security"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - hardening
  - security
  - least-privilege
  - rebash-networking-mastery
comments: false
status: ready
---

# Network Hardening — Reducing the Attack Surface of Network Infrastructure

> **Network Hardening** is the process of securing network infrastructure by **reducing vulnerabilities, eliminating unnecessary services, enforcing secure configurations, and implementing security best practices**. The goal is to minimise the attack surface and make systems more resistant to cyber attacks while maintaining business functionality. Network hardening applies to routers, switches, firewalls, Linux servers, cloud infrastructure, Kubernetes clusters, and network services. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand network hardening principles.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 8: Network Security → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Security</div>

<div markdown>**Lesson:** 5 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Network Hardening
- Reduce the attack surface
- Secure network devices
- Secure Linux servers
- Apply secure network protocols
- Implement patch management
- Apply enterprise hardening best practices

---

# Prerequisites

Complete:

- [VPN](vpn-and-tunneling-basics.md)
- [IPSec](ipsec.md)
- [SSL/TLS](ssl-tls.md)
- [SSH](ssh-networking.md)

---

# Why Learn Network Hardening?

Imagine a newly deployed Linux server.

By default it has:

- Multiple Open Ports
- Unused Services
- Default Accounts
- Weak Passwords

This creates:

```text
Large Attack Surface

❌
```

After hardening:

```text
Minimal Services

↓

Strong Authentication

↓

Secure Configuration

↓

Reduced Attack Surface

✓
```

---

# What is Network Hardening?

**Network Hardening** is the process of improving security by reducing unnecessary exposure.

It includes:

- Removing Unused Services
- Closing Unused Ports
- Applying Security Patches
- Strengthening Authentication
- Enforcing Security Policies
- Continuous Monitoring

---

# What is Attack Surface?

Attack surface refers to:

```text
All Possible

Entry Points

Into

A System
```

Examples include:

- Open Ports
- Running Services
- Public APIs
- Default Credentials
- Unpatched Software

The objective is:

```text
Smaller

Attack Surface

↓

Better Security
```

---

# Hardening Principles

Core principles include:

- Least Privilege
- Defence in Depth
- Secure by Default
- Continuous Updates
- Strong Authentication
- Continuous Monitoring

---

# Disable Unnecessary Services

Only run services that are required.

List services.

```bash
systemctl list-units --type=service
```

Disable unused service.

```bash
sudo systemctl disable service-name
```

Stop service.

```bash
sudo systemctl stop service-name
```

---

# Close Unused Ports

Display listening ports.

```bash
ss -tuln
```

Example:

```text
22

SSH

✓
```

```text
23

Telnet

❌
```

Disable unnecessary services exposing unwanted ports.

---

# Patch Management

Keep operating systems updated.

Ubuntu:

```bash
sudo apt update

sudo apt upgrade
```

RHEL:

```bash
sudo dnf update
```

Benefits:

- Security Fixes
- Bug Fixes
- Stability
- Compliance

---

# Strong Authentication

Use:

- SSH Keys
- Multi-Factor Authentication (MFA)
- Strong Password Policies
- Identity Providers

Avoid:

```text
Default Passwords
```

---

# Secure Protocols

Use secure protocols:

| Insecure | Secure |
|----------|---------|
| Telnet | SSH |
| HTTP | HTTPS |
| FTP | SFTP |
| POP3 | POP3S |
| IMAP | IMAPS |

Replace insecure protocols wherever possible.

---

# Firewall Hardening

Allow only required traffic.

Example:

```text
HTTPS

443

✓
```

```text
SSH

22

Admin Network Only
```

Everything else:

```text
Blocked
```

---

# Router Hardening

Best practices:

- Change Default Passwords
- Disable Unused Interfaces
- Enable Secure Management
- Restrict Administrative Access
- Update Firmware
- Enable Logging

---

# Switch Hardening

Recommendations:

- Disable Unused Ports
- Enable Port Security
- Use VLAN Segmentation
- Disable Unused VLANs
- Secure Management Access

---

# Linux Server Hardening

Key activities:

- Disable Root SSH Login
- Remove Unnecessary Packages
- Enable Firewall
- Configure Automatic Updates
- Enable Audit Logging
- Restrict File Permissions

Example:

```text
PermitRootLogin no
```

---

# DNS Hardening

Protect Domain Name System (DNS) infrastructure by:

- Restricting Zone Transfers
- Enabling DNSSEC where supported
- Updating DNS Software
- Limiting Recursive Queries
- Monitoring DNS Logs

---

# Network Device Management

Use:

- SSH
- HTTPS
- Simple Network Management Protocol version 3 (SNMPv3)

Avoid:

- Telnet
- HTTP
- SNMPv1
- SNMPv2c (where stronger alternatives are available)

---

# Password Policy

Strong passwords should include:

- Minimum Length
- Complexity
- Expiration Policy (where appropriate)
- Account Lockout
- Password History

Modern environments often combine strong passwords with MFA.

---

# Logging and Monitoring

Enable:

- System Logs
- Firewall Logs
- Authentication Logs
- Audit Logs

Useful Linux commands:

```bash
journalctl
```

```bash
last
```

```bash
who
```

---

# Enterprise Example

```text
Internet

↓

Firewall

↓

Demilitarised Zone (DMZ)

↓

Application

↓

Database
```

Hardening measures include:

- Firewall Rules
- Secure SSH
- Transport Layer Security (TLS)
- Patch Management
- Monitoring

---

# Cloud Perspective

Cloud hardening includes:

- Security Groups
- Identity and Access Management (IAM) Policies
- Private Networks
- Encryption
- Logging
- Continuous Compliance
- Managed Security Services

---

# Kubernetes Perspective

Kubernetes hardening includes:

- Role-Based Access Control (RBAC)
- Network Policies
- Pod Security Standards
- Secrets Management
- Admission Controllers
- Audit Logging
- Image Scanning

---

# Linux Perspective

Display listening ports.

```bash
ss -tuln
```

Display firewall rules.

```bash
sudo iptables -L
```

Display nftables rules.

```bash
sudo nft list ruleset
```

Check running services.

```bash
systemctl list-units --type=service
```

Display logged-in users.

```bash
who
```

View authentication history.

```bash
last
```

---

# Hardening Checklist

```text
✓ Update System

✓ Remove Unused Services

✓ Close Unused Ports

✓ Enable Firewall

✓ Disable Root Login

✓ Use SSH Keys

✓ Enable MFA

✓ Enable Logging

✓ Monitor Continuously
```

---

# Layered Security

```text
Internet

↓

Firewall

↓

VPN

↓

SSH

↓

Linux Firewall

↓

Application

↓

Monitoring
```

Each layer strengthens overall security.

---

# Advantages of Network Hardening

- Reduced Attack Surface
- Improved Security
- Better Compliance
- Lower Risk
- Easier Monitoring
- Increased System Stability

---

# Limitations

- Initial implementation requires planning
- Misconfiguration can impact availability
- Regular maintenance is required
- Continuous monitoring and updates are essential

---

# Hands-on Lab

## Task 1

Display listening ports.

```bash
ss -tuln
```

---

## Task 2

Display running services.

```bash
systemctl list-units --type=service
```

---

## Task 3

Update the operating system.

Ubuntu:

```bash
sudo apt update
sudo apt upgrade
```

---

## Task 4

Display firewall rules.

```bash
sudo iptables -L
```

---

## Task 5

Disable an unused service.

```bash
sudo systemctl disable service-name
```

---

## Task 6

Create a Linux server hardening checklist.

---

## Task 7

Design a hardened enterprise network architecture.

Include:

- Firewall
- VPN
- SSH
- Intrusion Detection System / Intrusion Prevention System (IDS/IPS)
- Logging Server

---

## Task 8

Compare hardening approaches for:

- Linux Servers
- Cloud Infrastructure
- Kubernetes Clusters

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ss -tuln` | Display listening ports |
| `systemctl list-units --type=service` | List running services |
| `systemctl stop service` | Stop a service |
| `systemctl disable service` | Disable a service |
| `apt update` | Update package index |
| `apt upgrade` | Upgrade installed packages |
| `iptables -L` | Display firewall rules |
| `nft list ruleset` | Display nftables rules |
| `who` | Display logged-in users |
| `last` | Display login history |
| `journalctl` | View system logs |

---

# Common Mistakes

❌ Leaving default passwords unchanged.

✅ Change all default credentials immediately.

---

❌ Running unnecessary services.

✅ Disable and remove unused software.

---

❌ Ignoring security updates.

✅ Apply patches regularly.

---

❌ Exposing management interfaces to the Internet.

✅ Restrict access using VPNs, firewalls, or bastion hosts.

---

❌ Disabling security controls for convenience.

✅ Follow documented change management and security policies.

---

# Best Practices

- Apply the principle of least privilege.
- Remove unnecessary software and services.
- Keep systems fully patched.
- Use secure protocols only.
- Enable centralised logging.
- Monitor systems continuously.
- Regularly audit firewall rules.
- Automate hardening using configuration management and Infrastructure as Code (IaC).
- Perform regular vulnerability assessments.

---

# Interview Questions

## Beginner

1. What is Network Hardening?
2. What is an attack surface?
3. Why should unnecessary services be removed?
4. Why are secure protocols preferred?

---

## Intermediate

1. Explain Linux server hardening.
2. How do you reduce the attack surface?
3. Why is patch management important?
4. What are common network device hardening techniques?

---

## Architect Level

1. Design a network hardening strategy for an enterprise.
2. Explain layered security in a production environment.
3. How would you continuously monitor and maintain a hardened infrastructure?

---

# Summary

In this lesson, you learned:

- Network Hardening
- Attack Surface Reduction
- Secure Network Configuration
- Linux Hardening
- Router and Switch Hardening
- Secure Protocols
- Patch Management
- Logging and Monitoring
- Enterprise Security Best Practices

Network hardening is an ongoing process that reduces vulnerabilities and strengthens infrastructure against cyber threats. By disabling unnecessary services, enforcing secure configurations, applying updates, and continuously monitoring systems, organisations can significantly improve the security and resilience of enterprise, cloud, and hybrid environments.

---

## Key Takeaways

- Network hardening **reduces the attack surface**.
- Remove unnecessary services and close unused ports.
- Use **secure protocols** such as SSH, HTTPS, and SFTP.
- Keep operating systems and applications **fully patched**.
- Protect systems using **firewalls, strong authentication, and logging**.
- Apply **least privilege**, **defence in depth**, and **continuous monitoring** across all environments.

---

## What's Next?

**[IDS/IPS](ids-ips.md)**

In the next lesson, you'll learn about **IDS/IPS (Intrusion Detection System / Intrusion Prevention System)**.

You'll explore:

- What IDS and IPS are
- Signature-Based Detection
- Anomaly-Based Detection
- Network IDS vs Host IDS
- Detection vs Prevention
- Enterprise Security Architectures
- Incident Response

By the end of the lesson, you'll understand how IDS and IPS identify, analyse, and respond to malicious activity, providing an essential layer of defence for enterprise, cloud, and hybrid networks.
