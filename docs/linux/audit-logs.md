---
title: "Audit Logs — Monitoring Security Events in Linux"
description: "Monitor Linux security with auditd — audit rules, ausearch, aureport, critical file watches, and production auditing practices."
difficulty: advanced
estimated_time: "95 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 11 · Linux Security"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - security-engineer
tags:
  - linux
  - security
  - auditd
  - logging
  - compliance
  - rebash-linux-mastery
comments: false
status: ready
---

# Audit Logs — Monitoring Security Events in Linux

> **Audit Logs** provide a detailed record of security-related events occurring on a Linux system. They help administrators track user activity, monitor system changes, investigate security incidents, detect unauthorized access, and meet compliance requirements. Linux provides several logging and auditing mechanisms, including **system logs**, **systemd journal**, and the **Linux Audit Framework (`auditd`)**. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, and Site Reliability Engineer (SRE) should understand how to collect, analyze, and manage audit logs in production environments.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 11: Linux Security → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Advanced</div>

<div markdown>**Reading Time:** 95 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Linux Security</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux auditing
- Learn the Linux Audit Framework
- Install and manage `auditd`
- Create audit rules
- Search audit logs
- Investigate security events
- Monitor critical files
- Apply production auditing best practices

---

# Prerequisites

Complete:

- Modules 1–10
- Module 11 Lessons 1–6

---

# Why Learn Audit Logs?

Imagine a critical configuration file changes unexpectedly.

Without auditing:

```text
Configuration Changed

↓

Unknown User

↓

No Evidence
```

With auditing:

```text
Configuration Changed

↓

Audit Log

↓

Username

↓

Time

↓

Action Recorded
```

Audit logs help identify **who**, **what**, **when**, and **how** an event occurred.

---

# What is Linux Auditing?

Linux auditing records security-related events, including:

- User logins
- Authentication failures
- File access
- File modifications
- Command execution
- Permission changes
- System configuration changes

Audit logs support:

- Security investigations
- Compliance
- Troubleshooting
- Incident response

---

# Linux Logging Components

Linux systems commonly use:

```text
Applications

↓

systemd-journald

↓

Syslog (optional)

↓

Log Files
```

For security auditing:

```text
Linux Audit Framework

↓

auditd

↓

Audit Logs
```

---

# What is auditd?

`auditd` is the Linux Audit Daemon.

Responsibilities include:

- Recording security events
- Monitoring important files
- Logging system calls
- Detecting policy violations

---

# Install auditd

Ubuntu/Debian:

```bash
sudo apt install auditd
```

RHEL/Rocky/AlmaLinux:

```bash
sudo dnf install audit
```

---

# Start the Audit Service

```bash
sudo systemctl enable auditd

sudo systemctl start auditd
```

Check status.

```bash
sudo systemctl status auditd
```

---

# Audit Log Location

Most Linux distributions store audit logs in:

```text
/var/log/audit/audit.log
```

---

# View Audit Logs

Display the log.

```bash
sudo less /var/log/audit/audit.log
```

Monitor the log.

```bash
sudo tail -f /var/log/audit/audit.log
```

---

# Search Audit Logs

Use:

```bash
ausearch
```

Example:

```bash
sudo ausearch -m USER_LOGIN
```

Search authentication failures.

```bash
sudo ausearch -m USER_AUTH
```

---

# Generate Audit Reports

Use:

```bash
aureport
```

Summary report.

```bash
sudo aureport
```

Authentication report.

```bash
sudo aureport --auth
```

Login report.

```bash
sudo aureport --login
```

File report.

```bash
sudo aureport --file
```

---

# Add an Audit Rule

Monitor a file.

```bash
sudo auditctl -w /etc/passwd -p wa
```

Meaning:

- `-w` → Watch file
- `-p w` → Monitor writes
- `-p a` → Monitor attribute changes

Combined:

```text
wa

↓

Write + Attribute Changes
```

---

# Add a Rule with a Key

```bash
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
```

Search by key.

```bash
sudo ausearch -k passwd_changes
```

---

# List Active Rules

```bash
sudo auditctl -l
```

---

# Delete a Rule

```bash
sudo auditctl -W /etc/passwd
```

---

# Persistent Rules

Temporary rules disappear after reboot.

Persistent rules are commonly stored in:

```text
/etc/audit/rules.d/
```

After updating rules, restart the service.

```bash
sudo systemctl restart auditd
```

---

# Monitor Failed Logins

Search:

```bash
sudo ausearch -m USER_LOGIN
```

---

# Monitor File Changes

Example:

```bash
sudo ausearch -f /etc/passwd
```

---

# Monitor Command Execution

Example:

```bash
sudo ausearch -x passwd
```

---

# Using journalctl

View security-related journal entries.

```bash
journalctl -xe
```

View SSH logs.

```bash
journalctl -u ssh
```

or

```bash
journalctl -u sshd
```

(depending on the Linux distribution)

---

# Common Commands

View audit log.

```bash
tail -f /var/log/audit/audit.log
```

Search events.

```bash
ausearch
```

Generate reports.

```bash
aureport
```

List rules.

```bash
auditctl -l
```

Add rule.

```bash
auditctl -w
```

---

# Real Production Examples

Monitor password database.

```bash
auditctl -w /etc/passwd -p wa
```

Search login events.

```bash
ausearch -m USER_LOGIN
```

Generate authentication report.

```bash
aureport --auth
```

Monitor SSH service logs.

```bash
journalctl -u ssh
```

---

# Production Perspective

Audit logging is essential for:

- Security investigations
- Compliance (PCI DSS, HIPAA, ISO 27001, SOC 2)
- Incident response
- Insider threat detection
- Forensic analysis
- Enterprise monitoring
- Government environments
- Financial institutions

Many compliance frameworks require security auditing and log retention.

---

# Hands-on Lab

## Task 1

Install `auditd`.

```bash
sudo apt install auditd
```

---

## Task 2

Start the service.

```bash
sudo systemctl start auditd
```

---

## Task 3

Check service status.

```bash
sudo systemctl status auditd
```

---

## Task 4

List current audit rules.

```bash
sudo auditctl -l
```

---

## Task 5

Monitor `/etc/passwd`.

```bash
sudo auditctl -w /etc/passwd -p wa
```

---

## Task 6

Modify `/etc/passwd` (in a test environment) or inspect existing events, then search the audit log.

```bash
sudo ausearch -f /etc/passwd
```

---

## Task 7

Generate an authentication report.

```bash
sudo aureport --auth
```

---

## Task 8

Monitor the audit log in real time.

```bash
sudo tail -f /var/log/audit/audit.log
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `auditctl` | Manage audit rules | Security monitoring |
| `ausearch` | Search audit logs | Incident investigation |
| `aureport` | Generate audit reports | Compliance reporting |
| `journalctl` | View system logs | Troubleshooting |
| `tail -f` | Monitor logs live | Security operations |
| `systemctl status auditd` | Verify audit service | Health checks |

---

# Common Audit Mistakes

| Mistake | Solution |
|----------|----------|
| Not running `auditd` | Enable and start the service |
| Monitoring too few files | Audit critical system files |
| Creating only temporary rules | Store persistent rules |
| Never reviewing logs | Schedule regular audits |
| Ignoring audit storage | Monitor disk usage and log retention |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    An administrator discovers that `/etc/passwd` was modified.

Without auditing:

```text
Unknown User

↓

Unknown Time

↓

No Investigation Possible
```

With auditing:

```bash
sudo ausearch -f /etc/passwd
```

The audit log identifies:

- User
- Process
- Timestamp
- Command
- Result

The security team can investigate the incident quickly and accurately.

---

# Best Practices

- Enable `auditd` on production systems.
- Audit critical system files and directories.
- Create persistent audit rules.
- Review audit logs regularly.
- Protect audit logs from unauthorized modification.
- Synchronize system time using NTP or Chrony for accurate timestamps.
- Archive and retain logs according to organizational policies.
- Forward audit logs to a centralized logging or SIEM platform for long-term analysis.

---

# Common Mistakes

❌ Disabling auditing to save resources.

✅ Avoid disabling auditing to save resources; fix the configuration instead.

---

❌ Monitoring too few security events.

✅ Avoid this mistake: monitoring too few security events.

---

❌ Ignoring authentication failures.

✅ Always review authentication failures.

---

❌ Allowing audit logs to grow without retention planning.

✅ Do not allow audit logs to grow without retention planning.

---

❌ Never reviewing audit reports.

✅ Always reviewing audit reports.

---

# Interview Questions
## Beginner

1. What is Linux auditing?
2. What is `auditd`?
3. Where are audit logs stored?
4. Which command searches audit logs?

---

## Intermediate

1. What is the difference between `ausearch` and `aureport`?
2. How do you monitor changes to `/etc/passwd`?
3. Why should audit rules be persistent?
4. What information is typically recorded in an audit log?

---

## Architect Level

1. How would you design centralized audit logging for hundreds of Linux servers?
2. How would you use audit logs during a security incident investigation?
3. What auditing controls would you implement to satisfy compliance requirements?

---

# Summary

In this lesson, you learned:

- Linux auditing fundamentals
- The Linux Audit Framework
- Managing `auditd`
- Creating audit rules
- Searching audit logs
- Generating audit reports
- Monitoring critical files
- Production auditing best practices

Audit logging provides detailed visibility into system activity and is a critical component of Linux security. By recording security events, monitoring sensitive files, and generating reports, audit logs support incident response, compliance, troubleshooting, and forensic investigations.

---

## Key Takeaways

- `auditd` records security-related events on Linux.
- Use `auditctl` to create audit rules.
- Use `ausearch` to investigate specific events.
- Use `aureport` to generate audit summaries.
- Monitor critical files such as `/etc/passwd`.
- Protect, retain, and regularly review audit logs as part of your security operations.

---

## What's Next?

**[Security Updates — Keeping Linux Systems Protected](security-updates.md)**

You'll explore:

- Why security updates are important
- Updating installed packages
- Checking for security advisories
- Automatic security updates
- Kernel updates
- Reboot requirements
- Production patch management best practices

By the end of the lesson, you'll be able to keep Linux systems secure by applying security patches safely, managing updates effectively, and maintaining a structured patch management process for production environments.
