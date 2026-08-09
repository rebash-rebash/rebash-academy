---
title: "SSH Keys — Secure Passwordless Authentication in Linux"
description: "Set up SSH key authentication — generate Ed25519 keys with ssh-keygen, use ssh-copy-id and ssh-agent, and secure passwordless access for Linux and Git."
difficulty: intermediate
estimated_time: "60 min"
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
  - ssh
  - ssh-keys
  - security
  - authentication
  - rebash-linux-mastery
comments: false
status: ready
---

# SSH Keys — Secure Passwordless Authentication in Linux

> SSH keys provide a secure and convenient way to authenticate users without using passwords. Instead of transmitting passwords over the network, SSH uses **public-key cryptography** to verify identities. SSH key authentication is the industry standard for Linux administration, cloud computing, DevOps, Git repositories, CI/CD pipelines, and enterprise infrastructure.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 5: Users and Groups → Lesson 8</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 60 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Users and Groups</div>

<div markdown>**Lesson:** 8 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SSH key authentication
- Differentiate public and private keys
- Generate SSH key pairs
- Configure passwordless login
- Use SSH Agent
- Secure SSH keys
- Authenticate with GitHub and GitLab
- Apply SSH security best practices

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management and Permissions
- Module 5 Lessons 1–7

---

# Why Learn SSH Keys?

Imagine you manage:

- 50 Linux servers
- AWS EC2 instances
- Azure Virtual Machines
- Google Cloud VMs
- Kubernetes nodes
- GitHub repositories

Typing passwords hundreds of times every day is:

- Slow
- Inconvenient
- Less secure

SSH keys solve this problem.

---

# What is an SSH Key?

SSH authentication uses two keys:

```text
Private Key

↓

Stored on your computer

↓

Never shared
```

and

```text
Public Key

↓

Copied to remote servers

↓

Safe to share
```

Authentication succeeds only when the two keys match.

---

# How SSH Authentication Works

```text
Your Laptop
──────────────

Private Key
id_ed25519

        │
        │ Authentication Request
        ▼

Linux Server
────────────────────

authorized_keys

Contains Public Key
```

If the public key matches your private key, access is granted.

---

# Public Key vs Private Key

| Public Key | Private Key |
|------------|-------------|
| Safe to share | Never share |
| Stored on servers | Stored on your computer |
| Used for verification | Used for authentication |
| Can be copied | Must remain secret |

---

# Supported Key Types

Modern SSH supports:

- **Ed25519** (recommended)
- RSA
- ECDSA

For new deployments, prefer **Ed25519** because it provides strong security with shorter keys and faster operations.

---

# Generate an SSH Key Pair

Recommended:

```bash
ssh-keygen -t ed25519 -C "basha@example.com"
```

For compatibility with older systems:

```bash
ssh-keygen -t rsa -b 4096 -C "basha@example.com"
```

---

# Generation Process

Example:

```text
Generating public/private key pair.

Enter file:

~/.ssh/id_ed25519

Enter passphrase:

********
```

Press **Enter** to use the default location.

A passphrase is recommended for better security.

---

# Default Key Location

```text
~/.ssh/
```

Contents:

```text
id_ed25519

id_ed25519.pub
```

or

```text
id_rsa

id_rsa.pub
```

---

# Understanding the Files

Private key:

```text
id_ed25519
```

Never share.

---

Public key:

```text
id_ed25519.pub
```

Safe to copy to servers.

---

# View Your Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Example:

```text
ssh-ed25519 AAAAC3...
```

---

# Copy Public Key to a Server

```bash
ssh-copy-id user@server
```

Example:

```bash
ssh-copy-id basha@192.168.1.100
```

This automatically adds your public key to:

```text
~/.ssh/authorized_keys
```

---

# Manual Installation

If `ssh-copy-id` is unavailable:

Create the directory.

```bash
mkdir -p ~/.ssh
```

Append your public key.

```bash
cat id_ed25519.pub >> ~/.ssh/authorized_keys
```

Set permissions.

```bash
chmod 700 ~/.ssh

chmod 600 ~/.ssh/authorized_keys
```

---

# Connect Without a Password

```bash
ssh basha@server
```

If configured correctly:

No password is required.

---

# SSH Agent

SSH Agent securely stores decrypted private keys in memory.

Start the agent.

```bash
eval "$(ssh-agent -s)"
```

Add your key.

```bash
ssh-add ~/.ssh/id_ed25519
```

List loaded keys.

```bash
ssh-add -l
```

---

# SSH Configuration

Configuration file:

```text
~/.ssh/config
```

Example:

```text
Host production

    HostName 192.168.1.100

    User basha

    IdentityFile ~/.ssh/id_ed25519
```

Connect using:

```bash
ssh production
```

---

# GitHub Authentication

Generate a key.

```bash
ssh-keygen -t ed25519
```

Copy the public key.

```bash
cat ~/.ssh/id_ed25519.pub
```

Add it to your GitHub account.

Test:

```bash
ssh -T git@github.com
```

---

# GitLab Authentication

The same SSH key can be added to GitLab.

Test:

```bash
ssh -T git@gitlab.com
```

---

# SSH Permissions

Secure permissions are critical.

```bash
chmod 700 ~/.ssh

chmod 600 ~/.ssh/id_ed25519

chmod 644 ~/.ssh/id_ed25519.pub

chmod 600 ~/.ssh/authorized_keys
```

Incorrect permissions may prevent SSH authentication.

---

# Common Commands

Generate key.

```bash
ssh-keygen -t ed25519
```

Copy key.

```bash
ssh-copy-id user@host
```

Start SSH Agent.

```bash
eval "$(ssh-agent -s)"
```

Load key.

```bash
ssh-add ~/.ssh/id_ed25519
```

Test connection.

```bash
ssh user@host
```

---

# Real Production Examples

GitHub authentication.

```bash
ssh -T git@github.com
```

GitLab authentication.

```bash
ssh -T git@gitlab.com
```

Production server.

```bash
ssh deploy@app-server
```

AWS EC2.

```bash
ssh -i aws-key.pem ec2-user@public-ip
```

Google Cloud VM.

```bash
ssh user@vm-ip
```

Azure VM.

```bash
ssh azureuser@vm-ip
```

---

# Production Perspective

SSH keys are widely used in:

- Linux servers
- Cloud virtual machines
- GitHub
- GitLab
- Bitbucket
- CI/CD pipelines
- Kubernetes administration
- Bastion hosts
- Infrastructure automation

Password-based authentication is often disabled in enterprise environments in favor of SSH keys.

---

# Hands-on Lab

## Task 1

Generate an Ed25519 key pair.

```bash
ssh-keygen -t ed25519
```

---

## Task 2

List the SSH directory.

```bash
ls -la ~/.ssh
```

---

## Task 3

View the public key.

```bash
cat ~/.ssh/id_ed25519.pub
```

---

## Task 4

Start the SSH Agent.

```bash
eval "$(ssh-agent -s)"
```

---

## Task 5

Add the private key.

```bash
ssh-add ~/.ssh/id_ed25519
```

---

## Task 6

List loaded keys.

```bash
ssh-add -l
```

---

## Task 7

Create an SSH configuration file.

```bash
nano ~/.ssh/config
```

---

## Task 8

Verify file permissions.

```bash
ls -ld ~/.ssh

ls -l ~/.ssh
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `ssh-keygen` | Generate SSH keys | Authentication |
| `ssh-copy-id` | Install public key | Server access |
| `ssh-agent` | Manage private keys | Passwordless workflows |
| `ssh-add` | Load keys into the agent | Git authentication |
| `ssh` | Connect to remote hosts | Administration |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    A DevOps engineer cannot log in using SSH keys.

Error:

```text
Permission denied (publickey).
```

Investigation:

```bash
ls -ld ~/.ssh

ls -l ~/.ssh

cat ~/.ssh/authorized_keys
```

Findings:

The `.ssh` directory permissions are:

```text
777
```

SSH rejects insecure permissions.

Solution:

```bash
chmod 700 ~/.ssh

chmod 600 ~/.ssh/authorized_keys

chmod 600 ~/.ssh/id_ed25519
```

Retry:

```bash
ssh user@server
```

Authentication succeeds.

---

# Best Practices

- Prefer **Ed25519** keys for new systems.
- Protect private keys with a strong passphrase.
- Never share your private key.
- Use SSH Agent to avoid repeated passphrase prompts.
- Disable password authentication on production servers where appropriate.
- Regularly rotate SSH keys.
- Remove unused public keys from servers.

---

# Common Mistakes

❌ Uploading the private key instead of the public key.

✅ Prefer the public key rather than uploading the private key.

---

❌ Setting incorrect permissions on the `.ssh` directory.

✅ Avoid this mistake: setting incorrect permissions on the `.ssh` directory.

---

❌ Storing private keys in shared repositories.

✅ Avoid this mistake: storing private keys in shared repositories.

---

❌ Using the same SSH key for personal and production environments.

✅ Avoid using the same SSH key for personal and production environments when a safer approach exists.

---

# Interview Questions
## Beginner

1. What is an SSH key?
2. What is the difference between a public key and a private key?
3. Which command generates an SSH key pair?
4. What is `authorized_keys`?

---

## Intermediate

1. Why is Ed25519 recommended over RSA for new deployments?
2. What is the purpose of SSH Agent?
3. How do you configure passwordless SSH?
4. Why are file permissions important for SSH authentication?

---

## Architect Level

1. How would you manage SSH keys across thousands of Linux servers?
2. Why is key-based authentication preferred over passwords?
3. How would you secure SSH access for cloud infrastructure and CI/CD pipelines?

---

# Summary

In this lesson, you learned:

- SSH key authentication
- Public and private keys
- Generating key pairs
- Passwordless SSH
- SSH Agent
- SSH configuration
- GitHub and GitLab authentication
- Production security best practices

SSH keys are the industry standard for secure remote access. They eliminate the need for passwords, improve security, support automation, and are widely used in Linux administration, cloud platforms, Git repositories, and enterprise infrastructure.

---

## Key Takeaways

- SSH uses public-key cryptography for authentication.
- Never share your private key.
- Use `ssh-keygen` to generate key pairs.
- Use `ssh-copy-id` to install public keys on remote servers.
- Protect the `.ssh` directory with the correct permissions.
- Prefer Ed25519 keys for new deployments.

---

## What's Next?

**[PAM (Pluggable Authentication Modules) — Understanding Linux Authentication](pam-overview.md)**

You'll explore:

- What PAM is
- How Linux authentication works
- PAM configuration files
- Authentication modules
- Password policies
- Multi-factor authentication (MFA)
- Enterprise authentication workflows

Understanding PAM will help you see how Linux authentication is centralized and how enterprise systems enforce consistent security policies.
