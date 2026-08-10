---
title: "SSH (Secure Shell)"
description: "Learn SSH — secure remote access, key-based authentication, tunneling, SSH Agent, SCP/SFTP, and Linux hardening for administration."
difficulty: beginner
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
  - ssh
  - authentication
  - remote-access
  - rebash-networking-mastery
comments: false
status: ready
---

# SSH (Secure Shell) — Secure Remote Access and System Administration

> **Secure Shell (SSH)** is a cryptographic network protocol that provides **secure remote login, command execution, file transfer, and system administration** over untrusted networks. SSH encrypts all communication between the client and the server, protecting credentials and data from eavesdropping, tampering, and impersonation attacks. SSH has replaced insecure protocols such as **Telnet** and is the standard method for managing Linux servers, cloud virtual machines, network devices, and Kubernetes infrastructure. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master SSH.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 8: Network Security → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Security</div>

<div markdown>**Lesson:** 4 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SSH
- Learn SSH architecture
- Understand SSH authentication
- Compare password and key-based authentication
- Learn SSH tunneling
- Understand SSH Agent
- Apply SSH security best practices

---

# Prerequisites

Complete:

- [VPN](vpn-and-tunneling-basics.md)
- [IPSec](ipsec.md)
- [SSL/TLS](ssl-tls.md)

---

# Why Learn SSH?

Imagine administering a Linux server remotely.

Without SSH:

```text
Administrator

↓

Telnet

↓

Linux Server
```

Passwords travel in plain text.

❌ Insecure

With SSH:

```text
Administrator

↓

Encrypted SSH Connection

↓

Linux Server
```

All communication is encrypted.

---

# What is SSH?

**SSH (Secure Shell)** is a secure protocol used for:

- Remote Login
- Remote Command Execution
- File Transfer
- Port Forwarding
- Secure Tunneling

SSH operates over:

```text
TCP Port 22
```

---

# Why Use SSH?

SSH provides:

- Encryption
- Authentication
- Integrity
- Secure Administration
- Secure File Transfer

---

# SSH Architecture

```text
SSH Client

↓

Encrypted Connection

↓

SSH Server

↓

Linux System
```

The SSH client establishes an encrypted session with the SSH server.

---

# SSH Components

SSH consists of:

- SSH Client
- SSH Server
- Authentication
- Encryption
- Session Management

---

# SSH Client

Runs on:

- Linux
- Windows
- macOS

Responsibilities:

- Connect to remote systems
- Authenticate user
- Encrypt communication
- Execute commands

---

# SSH Server

Runs on:

- Linux Servers
- Network Devices
- Cloud Virtual Machines

Responsibilities:

- Accept connections
- Authenticate users
- Execute commands
- Manage sessions

---

# SSH Authentication Methods

SSH supports:

- Password Authentication
- Public Key Authentication

Modern production environments should prefer key-based authentication.

---

# Password Authentication

Workflow:

```text
Username

↓

Password

↓

Authentication

↓

Access
```

Simple to use but less secure than key-based authentication.

---

# Public Key Authentication

Uses a cryptographic key pair.

```text
Public Key

↓

Stored

On Server
```

```text
Private Key

↓

Stored

On Client
```

Only the private key holder can successfully authenticate.

---

# SSH Key Pair

Generate keys:

```bash
ssh-keygen -t ed25519
```

Alternatively:

```bash
ssh-keygen -t rsa -b 4096
```

Files created:

```text
id_ed25519

Private Key
```

```text
id_ed25519.pub

Public Key
```

---

# Copy Public Key

Install the public key on the server.

```bash
ssh-copy-id user@server
```

Or manually append it to:

```text
~/.ssh/authorized_keys
```

---

# SSH Login

Connect to a remote server.

```bash
ssh user@server
```

Example:

```bash
ssh ubuntu@192.168.1.100
```

---

# SSH Configuration File

Client configuration:

```text
~/.ssh/config
```

Example:

```text
Host webserver
    HostName 192.168.1.100
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
```

Connect using:

```bash
ssh webserver
```

---

# SSH Server Configuration

Server configuration file:

```text
/etc/ssh/sshd_config
```

Common settings:

```text
PermitRootLogin no
```

```text
PasswordAuthentication no
```

```text
PubkeyAuthentication yes
```

Restart SSH service:

```bash
sudo systemctl restart ssh
```

---

# SSH Tunneling

SSH can securely forward network traffic.

Types:

- Local Port Forwarding
- Remote Port Forwarding
- Dynamic Port Forwarding

---

# Local Port Forwarding

Example:

```bash
ssh -L 8080:localhost:80 user@server
```

Traffic sent to:

```text
localhost:8080
```

is securely forwarded to:

```text
server:80
```

---

# Remote Port Forwarding

Example:

```bash
ssh -R 9000:localhost:3000 user@server
```

Allows remote systems to reach a local service securely.

---

# Dynamic Port Forwarding

Create a SOCKS proxy.

```bash
ssh -D 1080 user@server
```

Applications configured to use the SOCKS proxy send traffic through the encrypted SSH tunnel.

---

# SSH Agent

SSH Agent securely stores decrypted private keys in memory.

Start the agent.

```bash
eval "$(ssh-agent -s)"
```

Add a key.

```bash
ssh-add ~/.ssh/id_ed25519
```

This avoids repeatedly entering the private key passphrase.

---

# SCP (Secure Copy)

Copy a file to a remote server.

```bash
scp file.txt user@server:/home/user/
```

Copy a file from a server.

```bash
scp user@server:/home/user/file.txt .
```

---

# SFTP (SSH File Transfer Protocol)

Connect using SFTP.

```bash
sftp user@server
```

Useful commands:

```text
put
```

Upload file.

```text
get
```

Download file.

---

# Enterprise Example

```text
Administrator

↓

SSH

↓

Bastion Host

↓

Production Server
```

Administrators access production servers through a secured bastion host.

---

# Cloud Perspective

Cloud platforms commonly use SSH for:

- Virtual Machine Administration
- Bastion Hosts
- Deployment Automation
- Infrastructure Management

Many cloud providers support importing SSH public keys during VM creation.

---

# Kubernetes Perspective

SSH is often used to:

- Access Kubernetes Worker Nodes
- Troubleshoot Control Plane Nodes
- Manage Bastion Hosts
- Investigate Infrastructure Issues

Production Kubernetes administration should primarily use Kubernetes APIs rather than direct node access whenever possible.

---

# Linux Perspective

Generate SSH keys.

```bash
ssh-keygen -t ed25519
```

Connect to a server.

```bash
ssh user@server
```

Copy a public key.

```bash
ssh-copy-id user@server
```

Display SSH service status.

```bash
sudo systemctl status ssh
```

Check listening SSH port.

```bash
ss -tuln | grep :22
```

---

# SSH Packet Flow

```text
SSH Client

↓

Authentication

↓

Key Exchange

↓

Encrypted Session

↓

SSH Server
```

---

# Password vs Key-Based Authentication

| Password | SSH Keys |
|-----------|----------|
| Easier to Set Up | More Secure |
| Vulnerable to Brute Force | Resistant to Password Guessing |
| Requires Password Entry | Can Use SSH Agent |
| Not Recommended for Production | Recommended for Production |

---

# Advantages of SSH

- Strong Encryption
- Secure Authentication
- Secure Remote Administration
- Secure File Transfer
- Port Forwarding
- Cross-Platform Support

---

# Limitations

- Misconfigured SSH servers can expose systems
- Private keys must be protected
- Lost private keys require replacement and redistribution
- SSH does not replace proper authorisation and auditing

---

# Hands-on Lab

## Task 1

Generate an SSH key pair.

```bash
ssh-keygen -t ed25519
```

---

## Task 2

Copy the public key to a server.

```bash
ssh-copy-id user@server
```

---

## Task 3

Connect using SSH.

```bash
ssh user@server
```

---

## Task 4

Display SSH service status.

```bash
sudo systemctl status ssh
```

---

## Task 5

Check whether SSH is listening.

```bash
ss -tuln | grep :22
```

---

## Task 6

Create a local SSH tunnel.

```bash
ssh -L 8080:localhost:80 user@server
```

---

## Task 7

Transfer a file using SCP.

```bash
scp file.txt user@server:/home/user/
```

---

## Task 8

Create an SSH client configuration file for three production servers.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ssh` | Connect to a remote server |
| `ssh-keygen` | Generate SSH keys |
| `ssh-copy-id` | Install public key on server |
| `ssh-add` | Add private key to SSH Agent |
| `scp` | Secure file copy |
| `sftp` | Secure file transfer |
| `systemctl status ssh` | Check SSH service |
| `ss -tuln` | Display listening ports |

---

# Common Mistakes

❌ Enabling password authentication in production.

✅ Use SSH key authentication whenever possible.

---

❌ Allowing direct root login.

✅ Disable root login and use privilege escalation (sudo).

---

❌ Storing private keys insecurely.

✅ Protect keys with proper file permissions and passphrases.

---

❌ Exposing SSH to the entire Internet.

✅ Restrict access using firewalls, VPNs, or bastion hosts.

---

❌ Ignoring SSH logs.

✅ Monitor authentication attempts and failed logins.

---

# Best Practices

- Use **Ed25519** or strong RSA keys.
- Disable root login.
- Disable password authentication where practical.
- Protect private keys with passphrases.
- Enable Multi-Factor Authentication (MFA) if supported.
- Restrict SSH access using firewalls and Security Groups.
- Rotate SSH keys periodically.
- Monitor SSH login activity.

---

# Interview Questions

## Beginner

1. What is SSH?
2. Why is SSH more secure than Telnet?
3. What port does SSH use?
4. What is the difference between SSH Client and SSH Server?

---

## Intermediate

1. Compare password authentication and key-based authentication.
2. What is SSH Agent?
3. Explain SSH tunneling.
4. What is SCP?

---

## Architect Level

1. Design secure SSH access for production servers.
2. Explain bastion host architecture.
3. How would you troubleshoot SSH authentication failures?

---

# Summary

In this lesson, you learned:

- SSH
- SSH Client and Server
- Public Key Authentication
- Password Authentication
- SSH Keys
- SSH Tunneling
- SSH Agent
- SCP
- SFTP
- Enterprise SSH Security

SSH is the industry standard for secure remote administration of Linux servers, cloud infrastructure, and network devices. By providing encrypted communication, strong authentication, secure file transfer, and tunneling capabilities, SSH replaces insecure remote access protocols and forms a critical part of modern infrastructure management.

---

## Key Takeaways

- SSH provides **secure remote administration** over encrypted connections.
- **TCP port 22** is the default SSH port.
- **Key-based authentication** is more secure than passwords.
- SSH supports **remote login, file transfer, and secure tunneling**.
- **SSH Agent** simplifies key management.
- Production environments should disable root login and prefer SSH keys with strong access controls.

---

## What's Next?

**[Network Hardening](network-security-hardening.md)**

In the next lesson, you'll learn about **Network Hardening**.

You'll explore:

- What Network Hardening is
- Secure Network Configuration
- Service Minimization
- Patch Management
- Secure Protocols
- Network Device Hardening
- Enterprise Security Best Practices

By the end of the lesson, you'll understand how to reduce the attack surface of networks and systems by applying security best practices, eliminating unnecessary services, and strengthening infrastructure against common threats.
