---
title: "Linux Password Policies — Securing User Authentication"
description: "Enforce Linux password policies — use passwd and chage for aging, expiration, and account locking, and understand /etc/shadow for secure authentication."
difficulty: intermediate
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 5 · Users and Groups"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - passwords
  - chage
  - shadow
  - security
  - rebash-linux-mastery
comments: false
status: ready
---

# Linux Password Policies — Securing User Authentication

> Passwords are the first line of defense in Linux security. Weak passwords or poorly configured password policies can lead to unauthorized access, privilege escalation, and security breaches. Linux provides built-in mechanisms to enforce password complexity, expiration, aging, and account locking to protect systems from misuse.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 5: Users and Groups → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 55 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Users and Groups</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Linux password policies
- Manage user passwords
- Configure password aging
- Set password expiration
- Lock and unlock user accounts
- Understand the `/etc/shadow` file
- Apply password security best practices
- Enforce enterprise password policies

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 Lessons 1–3

---

# Why Learn Password Policies?

Imagine a production Linux server.

A user account has:

- Password: `admin123`
- Never expires
- Shared by multiple administrators

This creates a serious security risk.

Linux password policies help enforce:

- Strong passwords
- Password expiration
- Password history
- Account security
- Compliance requirements

---

# What is a Password Policy?

A password policy defines rules such as:

- Minimum password length
- Password complexity
- Password expiration
- Password aging
- Password reuse restrictions
- Account locking

These policies reduce the risk of unauthorized access.

---

# The Password Lifecycle

```text
Create Password
       │
       ▼
Password Active
       │
       ▼
Password Expires
       │
       ▼
User Changes Password
       │
       ▼
New Password Active
```

---

# Changing a Password

Change your own password.

```bash
passwd
```

Example:

```text
Changing password for basha.

Current password:

New password:

Retype new password:
```

---

# Change Another User's Password

Administrator only.

```bash
sudo passwd developer
```

---

# Password Information

Display password aging information.

```bash
chage -l basha
```

Example:

```text
Last password change

Password expires

Password inactive

Account expires
```

---

# Password Aging

Linux supports:

- Minimum password age
- Maximum password age
- Warning period
- Inactive period

These settings help enforce regular password updates.

---

# Configure Password Expiration

Example:

```bash
sudo chage -M 90 basha
```

Meaning:

```text
Maximum password age

90 Days
```

---

# Minimum Password Age

Prevent immediate password changes.

```bash
sudo chage -m 7 basha
```

Meaning:

```text
Minimum age

7 Days
```

---

# Warning Before Expiration

Warn users before expiration.

```bash
sudo chage -W 14 basha
```

Meaning:

```text
Warn user

14 Days
```

---

# Account Expiration

Set account expiration.

```bash
sudo chage -E 2027-12-31 basha
```

Disable expiration.

```bash
sudo chage -E -1 basha
```

---

# Lock a User Account

Temporarily disable password authentication.

```bash
sudo passwd -l basha
```

Check status.

```bash
sudo passwd -S basha
```

---

# Unlock a User Account

```bash
sudo passwd -u basha
```

---

# Force Password Change

Require the user to change their password at the next login.

```bash
sudo passwd -e basha
```

---

# Understanding /etc/shadow

Linux stores password information in:

```text
/etc/shadow
```

View (requires elevated privileges).

```bash
sudo cat /etc/shadow
```

Example:

```text
basha:$y$j9T$...

:20240:7:90:14:::
```

Fields include:

- Username
- Password hash
- Last password change
- Minimum age
- Maximum age
- Warning period
- Inactive period
- Account expiration

Passwords are stored as **hashed values**, not plain text.

---

# Difference Between /etc/passwd and /etc/shadow

| File | Purpose |
|------|---------|
| `/etc/passwd` | User account information |
| `/etc/shadow` | Password hashes and aging information |

---

# Common Commands

Change password.

```bash
passwd
```

Display aging.

```bash
chage -l basha
```

Set maximum age.

```bash
sudo chage -M 90 basha
```

Set minimum age.

```bash
sudo chage -m 7 basha
```

Set warning days.

```bash
sudo chage -W 14 basha
```

Lock account.

```bash
sudo passwd -l basha
```

Unlock account.

```bash
sudo passwd -u basha
```

Force password reset.

```bash
sudo passwd -e basha
```

---

# Password Complexity

Many Linux systems enforce password complexity using **PAM** modules.

Common requirements include:

- Minimum length
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters
- Password history

We'll learn how Linux enforces these policies in the **PAM Overview** lesson later in this module.

---

# Real Production Examples

Force password reset after onboarding.

```bash
sudo passwd -e developer
```

Lock a terminated employee's account.

```bash
sudo passwd -l employee1
```

Set a 90-day password expiration policy.

```bash
sudo chage -M 90 developer
```

Review password aging.

```bash
sudo chage -l developer
```

---

# Production Perspective

Password policies are essential for:

- Enterprise Linux servers
- Cloud virtual machines
- SSH access
- Compliance standards (CIS, ISO 27001, PCI-DSS)
- Financial systems
- Healthcare systems
- Government environments

Strong password policies reduce the risk of credential compromise.

---

# Hands-on Lab

## Task 1

View password aging information.

```bash
chage -l $USER
```

---

## Task 2

Change your password.

```bash
passwd
```

---

## Task 3

View your account information again.

```bash
chage -l $USER
```

---

## Task 4

Display your password status.

```bash
sudo passwd -S $USER
```

---

## Task 5

View the shadow file.

```bash
sudo cat /etc/shadow
```

Observe the password hash format.

---

## Task 6

Lock a test user account.

```bash
sudo passwd -l testuser
```

*(Replace `testuser` with an existing non-production user.)*

---

## Task 7

Unlock the account.

```bash
sudo passwd -u testuser
```

---

## Task 8

Force a password change at the next login.

```bash
sudo passwd -e testuser
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `passwd` | Change password | User management |
| `passwd -l` | Lock account | Disable access |
| `passwd -u` | Unlock account | Restore access |
| `passwd -e` | Expire password | Force reset |
| `passwd -S` | View password status | Auditing |
| `chage` | Manage password aging | Compliance |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A user cannot log in.

Error:

```text
Your password has expired.
```

Investigation:

```bash
sudo chage -l developer

sudo passwd -S developer
```

The password has exceeded the maximum age.

Solution:

Reset the password.

```bash
sudo passwd developer
```

or require a password change on the next login.

```bash
sudo passwd -e developer
```

The user successfully regains access after updating the password.

---

# Best Practices

- Enforce strong password complexity.
- Set password expiration policies for enterprise accounts.
- Lock accounts that are no longer in use.
- Force password changes for newly created users.
- Protect the `/etc/shadow` file.
- Regularly audit password policies.

---

# Common Mistakes

❌ Using weak or predictable passwords.

✅ Avoid using weak or predictable passwords when a safer approach exists.

---

❌ Sharing user accounts and passwords.

✅ Avoid this mistake: sharing user accounts and passwords.

---

❌ Allowing passwords to never expire in enterprise environments without a justified exception.

✅ Do not allow passwords to never expire in enterprise environments without a justified exception.

---

❌ Granting unnecessary access to the `/etc/shadow` file.

✅ Avoid this mistake: granting unnecessary access to the `/etc/shadow` file.

---

# Interview Questions
## Beginner

1. Which command changes a user's password?
2. What is the purpose of `/etc/shadow`?
3. How do you lock a user account?
4. What is password aging?

---

## Intermediate

1. Explain the difference between `/etc/passwd` and `/etc/shadow`.
2. How do you configure password expiration?
3. How do you force a password change at the next login?
4. What information does `chage -l` display?

---

## Architect Level

1. How would you enforce password policies across hundreds of Linux servers?
2. How do password policies help meet compliance requirements?
3. When would you choose SSH key authentication instead of passwords?

---

# Summary

In this lesson, you learned:

- Password management
- Password aging
- Password expiration
- Account locking
- Account unlocking
- `/etc/shadow`
- Enterprise password policies
- Security best practices

Strong password policies are a critical component of Linux security. They help protect systems against unauthorized access while supporting organizational security standards and compliance requirements.

---

## Key Takeaways

- Use `passwd` to manage passwords.
- Use `chage` to configure password aging.
- Store password hashes securely in `/etc/shadow`.
- Lock unused accounts.
- Force password changes for new users.
- Apply strong password policies for enterprise environments.

---

## What's Next?

**[Environment Variables in Linux — Configuring the Linux Environment](environment-variables.md)**

You'll explore:

- Local variables
- Environment variables
- `PATH`
- `HOME`
- `USER`
- `SHELL`
- `HOSTNAME`
- `export`
- `unset`
- Best practices for configuring application environments

Environment variables are fundamental to Linux, scripting, DevOps automation, Docker, Kubernetes, and cloud-native applications.
