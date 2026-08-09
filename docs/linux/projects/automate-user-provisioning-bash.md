---
title: "Capstone Project 5 — Automate User Provisioning with Bash"
description: "Build a production Bash script that provisions Linux users from CSV — groups, passwords, SSH, logging, error handling, and reports."
difficulty: advanced
estimated_time: "5–7 hours"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 15 · Capstone Projects"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
  - security-engineer
tags:
  - linux
  - capstone
  - bash
  - automation
  - users
  - production
  - rebash-linux-mastery
comments: false
status: ready
---

# Capstone Project 5 — Automate User Provisioning with Bash

> Managing Linux users manually becomes inefficient and error-prone as organizations grow. System administrators often need to provision dozens or even hundreds of users while ensuring consistent usernames, groups, home directories, SSH access, passwords, and permissions. In this capstone project, you'll build a **production-ready Bash automation script** that provisions Linux users from a CSV file, applies security policies, generates reports, and logs every action. This project demonstrates real-world Linux automation using Bash scripting.

---

# Project Overview

## Objective

Build a Bash automation solution that provisions Linux users securely and consistently.

---

## Skills Covered

- Bash Scripting
- Linux User Management
- File Permissions
- Groups
- CSV Processing
- Loops
- Functions
- Logging
- Error Handling
- Automation
- Security
- Production Validation

---

# Estimated Time

**5–7 Hours**

---

# Difficulty

Beginner → Advanced

---

# Project Architecture

```text
                users.csv
                     │
                     ▼
          user_provision.sh
                     │
      ┌──────────────┼──────────────┐
      │              │              │
Create User     Create Group    Set Password
      │              │              │
      └──────────────┼──────────────┘
                     │
          Configure Home Directory
                     │
                     ▼
          Generate Log & Report
```

---

# Learning Outcomes

By completing this project, you'll be able to:

- Build production Bash scripts
- Read CSV files
- Automate Linux user creation
- Configure groups and permissions
- Generate secure passwords
- Implement logging
- Handle script errors
- Validate provisioning results

---

# Project Requirements

## Hardware

Minimum

- 2 vCPU
- 2 GB RAM
- 20 GB Disk

Recommended

- 2–4 vCPU
- 4 GB RAM
- 40 GB SSD

---

## Operating System

Choose one:

- Ubuntu Server 24.04 LTS
- Ubuntu Server 22.04 LTS
- Rocky Linux 9
- AlmaLinux 9

This project uses **Ubuntu Server**.

---

# Software Stack

- Ubuntu Linux
- Bash
- passwd
- useradd
- groupadd
- chage
- openssl
- awk
- cron

---

# Project Tasks

| Phase | Task |
|---------|------|
| 1 | Prepare CSV File |
| 2 | Create Bash Script |
| 3 | Read CSV Data |
| 4 | Create Groups |
| 5 | Create Users |
| 6 | Configure Passwords |
| 7 | Configure Home Directories |
| 8 | Configure SSH Access |
| 9 | Generate Logs |
| 10 | Error Handling |
| 11 | Validate Users |
| 12 | Production Review |

---

# Phase 1 — Prepare CSV File

Create a file named:

```text
users.csv
```

Example:

```csv
username,fullname,group
john,John Doe,developers
alice,Alice Smith,developers
bob,Bob Wilson,admins
david,David Lee,devops
```

---

# Phase 2 — Create Bash Script

Create the project.

```bash
touch user_provision.sh

chmod +x user_provision.sh
```

Script structure.

```text
Variables

↓

Functions

↓

Validation

↓

Processing

↓

Logging
```

---

# Phase 3 — Read CSV File

Read the file.

Example:

```bash
while IFS=',' read username fullname group
do
    echo "$username"
done < users.csv
```

Skip the header row during processing.

---

# Phase 4 — Create Groups

Check if the group exists.

```bash
getent group developers
```

Create if missing.

```bash
groupadd developers
```

Verify.

```bash
getent group developers
```

---

# Phase 5 — Create Users

Check if user exists.

```bash
id john
```

Create user.

```bash
useradd -m -s /bin/bash -g developers john
```

Verify.

```bash
id john
```

---

# Phase 6 — Configure Passwords

Generate secure password.

Example:

```bash
openssl rand -base64 16
```

Assign password.

```bash
echo "john:Password123" | chpasswd
```

Force password change.

```bash
chage -d 0 john
```

---

# Phase 7 — Configure Home Directories

Verify.

```bash
ls -ld /home/john
```

Set permissions.

```bash
chmod 700 /home/john
```

Assign ownership.

```bash
chown john:developers /home/john
```

---

# Phase 8 — Configure SSH Access

Create SSH directory.

```bash
mkdir -p /home/john/.ssh
```

Set permissions.

```bash
chmod 700 /home/john/.ssh
```

Copy public key.

```bash
cp authorized_keys /home/john/.ssh/
```

Set ownership.

```bash
chown -R john:developers /home/john/.ssh
```

---

# Phase 9 — Generate Logs

Create log file.

```text
/var/log/user-provision.log
```

Example entry:

```text
2026-08-09 10:30

User Created

john

developers
```

Append logs.

```bash
echo "User created: john" >> /var/log/user-provision.log
```

---

# Phase 10 — Error Handling

Handle errors such as:

- Missing CSV file
- Empty records
- Duplicate users
- Duplicate groups
- Invalid usernames
- Password generation failures

Exit on fatal errors.

```bash
exit 1
```

---

# Phase 11 — Validate Users

Verify.

```bash
id john
```

Display groups.

```bash
groups john
```

Verify password policy.

```bash
chage -l john
```

Check home directory.

```bash
ls -ld /home/john
```

---

# Phase 12 — Production Review

Validate:

Users.

```bash
getent passwd
```

Groups.

```bash
getent group
```

Logs.

```bash
cat /var/log/user-provision.log
```

Permissions.

```bash
ls -l /home
```

---

# Sample Script Workflow

```text
Read CSV

↓

Validate Data

↓

Create Group

↓

Create User

↓

Generate Password

↓

Configure Home

↓

Configure SSH

↓

Log Result

↓

Generate Report
```

---

# Final Project Checklist

| Item | Status |
|--------|--------|
| CSV Created | ☐ |
| Bash Script Written | ☐ |
| Groups Created | ☐ |
| Users Created | ☐ |
| Passwords Generated | ☐ |
| Home Directories Configured | ☐ |
| SSH Access Configured | ☐ |
| Logging Implemented | ☐ |
| Error Handling Added | ☐ |
| Validation Completed | ☐ |
| Report Generated | ☐ |
| Production Review Completed | ☐ |

---

# Production Perspective

User provisioning automation is commonly used for:

- Employee onboarding
- Student laboratory accounts
- Cloud virtual machines
- Development environments
- CI/CD servers
- Kubernetes worker nodes
- Enterprise Linux servers
- Training environments

Large organizations automate user lifecycle management to improve consistency, security, and efficiency.

---

# Hands-on Lab

## Task 1

Create a CSV containing ten users.

---

## Task 2

Write a Bash script to process the CSV.

---

## Task 3

Automatically create groups.

---

## Task 4

Automatically create users.

---

## Task 5

Generate random passwords.

---

## Task 6

Force password changes on first login.

---

## Task 7

Generate a provisioning log.

---

## Task 8

Generate a summary report showing:

- Total users processed
- Users created
- Existing users skipped
- Groups created
- Errors encountered
- Execution time

---

# Production Best Practices

- Validate input before processing.
- Check whether users already exist.
- Avoid hardcoded passwords.
- Use strong random password generation.
- Log every administrative action.
- Handle failures gracefully.
- Run scripts with least required privileges.
- Test automation in a non-production environment first.
- Version-control automation scripts.
- Document script usage and recovery procedures.

---

# Challenge Tasks

Complete these additional tasks to extend the project:

- Import users from a JSON file.
- Generate individual SSH key pairs automatically.
- Send welcome emails after account creation.
- Automatically disable inactive users after 90 days.
- Generate HTML and CSV provisioning reports.
- Add rollback functionality to remove partially created accounts on failure.
- Integrate the script with LDAP or Active Directory.
- Schedule automated provisioning using cron.
- Create a companion script to deprovision users.
- Build a menu-driven interactive version of the provisioning tool.

---

# Skills Demonstrated

After completing this project, you will have demonstrated proficiency in:

- Bash Scripting
- Linux User Administration
- CSV Processing
- Automation
- Functions and Loops
- Logging
- Error Handling
- Security
- Production Scripting
- Enterprise Linux Administration

---

# Congratulations!

You have successfully built a **production-ready User Provisioning Automation** solution using Bash.

Your script can now create Linux users consistently, configure groups and permissions, generate secure passwords, log administrative actions, and reduce manual effort through automation.

This type of automation is widely used by Linux administrators, DevOps engineers, and IT operations teams for employee onboarding, server administration, and large-scale infrastructure management.

---

## What's Next?

**[Capstone Project 6 — Build a Linux Server Baseline](linux-server-baseline.md)**

You'll learn how to:


- Standardize Linux server configuration
- Configure security baselines
- Apply operating system hardening
- Install essential packages
- Configure logging and monitoring
- Validate compliance
- Prepare production-ready server templates

By the end of the project, you'll build a reusable Linux Server Baseline that can be applied across multiple servers to ensure consistency, security, and operational excellence in enterprise environments.
