---
title: "DNS (Domain Name System) — Translating Domain Names into IP Addresses"
description: "Learn DNS on Linux — name resolution, A/AAAA/CNAME/MX/NS/PTR records, configure resolvers, and troubleshoot with dig, nslookup, getent, and resolvectl."
difficulty: intermediate
estimated_time: "75 min"
author: Shaik Basha
last_updated: "2026-08-09"
category: linux
technology: linux
module: "Module 8 · Networking"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
tags:
  - linux
  - networking
  - dns
  - dig
  - name-resolution
  - rebash-linux-mastery
comments: false
status: ready
---

# DNS (Domain Name System) — Translating Domain Names into IP Addresses

> **DNS (Domain Name System)** is the Internet's distributed naming system that translates human-readable domain names (such as `google.com`) into IP addresses that computers use for communication. Without DNS, users would need to remember numerical IP addresses instead of simple domain names. Understanding DNS is essential for Linux administrators, DevOps engineers, Cloud Architects, Network Engineers, and Site Reliability Engineers (SREs).

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Linux Mastery** → Module 8: Networking → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner → Intermediate</div>

<div markdown>**Reading Time:** 75 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Linux Mastery</div>

<div markdown>**Module:** Networking</div>

<div markdown>**Lesson:** 3 of 13</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand DNS
- Learn how name resolution works
- Understand DNS records
- Configure DNS servers
- Troubleshoot DNS issues
- Use common DNS tools
- Apply DNS concepts in production

---

# Prerequisites

Complete:

- Module 1 – Linux Fundamentals
- Module 2 – Linux Command Line Essentials
- Module 3 – Text Processing
- Module 4 – File Management
- Module 5 – Users and Groups
- Module 6 – Process Management
- Module 7 – Package Management
- Module 8 Lessons 1–2

---

# Why Learn DNS?

Imagine you type:

```text
https://www.google.com
```

Your browser does **not** know Google's IP address.

Instead,

it asks a DNS server:

> "What is the IP address of `www.google.com`?"

Only after receiving the IP address can your browser connect to the website.

---

# What is DNS?

DNS stands for:

```text
Domain Name System
```

Its primary job is:

```text
Domain Name

↓

IP Address
```

Example:

```text
www.google.com

↓

142.250.x.x
```

This process is called **name resolution**.

---

# Why DNS is Needed

Without DNS,

users would have to remember addresses like:

```text
142.250.182.100
```

Instead of:

```text
google.com
```

DNS makes networking user-friendly.

---

# DNS Resolution Process

```text
User
   │
   ▼
Browser
   │
   ▼
Local DNS Resolver
   │
   ▼
Recursive DNS Server
   │
   ▼
Authoritative DNS Server
   │
   ▼
IP Address Returned
   │
   ▼
Browser Connects
```

---

# DNS Components

The DNS infrastructure includes:

- Client (Resolver)
- Recursive DNS Server
- Root DNS Server
- Top-Level Domain (TLD) Server
- Authoritative DNS Server

Each plays a role in locating the correct IP address.

---

# Common DNS Record Types

| Record | Purpose |
|---------|----------|
| A | Maps a hostname to an IPv4 address |
| AAAA | Maps a hostname to an IPv6 address |
| CNAME | Creates an alias for another hostname |
| MX | Specifies mail servers |
| NS | Specifies authoritative name servers |
| TXT | Stores text information (SPF, DKIM, verification, etc.) |
| PTR | Reverse DNS (IP address to hostname) |
| SRV | Specifies the location of network services |

---

# A Record

Maps a hostname to an IPv4 address.

Example:

```text
www.example.com

↓

192.168.1.100
```

---

# AAAA Record

Maps a hostname to an IPv6 address.

Example:

```text
www.example.com

↓

2001:db8::10
```

---

# CNAME Record

Creates an alias.

Example:

```text
www.example.com

↓

server.example.com
```

Useful when multiple hostnames should point to the same destination.

---

# MX Record

Specifies mail servers.

Example:

```text
example.com

↓

mail.example.com
```

Email systems use MX records to determine where to deliver messages.

---

# NS Record

Identifies authoritative name servers.

Example:

```text
ns1.example.com

ns2.example.com
```

---

# PTR Record

Performs reverse DNS lookup.

```text
192.168.1.100

↓

server.example.com
```

Commonly used for:

- Mail servers
- Logging
- Security

---

# DNS Port

DNS uses:

```text
53
```

Protocols:

- UDP 53 (most queries)
- TCP 53 (zone transfers and larger responses)

---

# Configure DNS Servers

View configured DNS servers.

```bash
cat /etc/resolv.conf
```

Example:

```text
nameserver 8.8.8.8

nameserver 1.1.1.1
```

> On many modern Linux distributions, `/etc/resolv.conf` is automatically managed by services such as **systemd-resolved** or **NetworkManager**. Direct edits may not persist.

---

# Test DNS Resolution

Using `getent` (works with the system's configured name service):

```bash
getent hosts google.com
```

Example:

```text
142.250.x.x
```

---

# Using dig

Query DNS.

```bash
dig google.com
```

Query a specific record.

```bash
dig google.com MX
```

Query a specific DNS server.

```bash
dig @8.8.8.8 google.com
```

---

# Using nslookup

Basic lookup.

```bash
nslookup google.com
```

Lookup using a specific server.

```bash
nslookup google.com 8.8.8.8
```

---

# Reverse DNS Lookup

Using `dig`.

```bash
dig -x 8.8.8.8
```

Using `nslookup`.

```bash
nslookup 8.8.8.8
```

---

# Flush DNS Cache

If using `systemd-resolved`:

```bash
sudo resolvectl flush-caches
```

Verify cache statistics.

```bash
resolvectl statistics
```

---

# Common Commands

View DNS configuration.

```bash
cat /etc/resolv.conf
```

Resolve hostname.

```bash
getent hosts google.com
```

DNS query.

```bash
dig google.com
```

DNS lookup.

```bash
nslookup google.com
```

Reverse lookup.

```bash
dig -x 8.8.8.8
```

---

# Real Production Examples

Verify Kubernetes API DNS.

```bash
dig kubernetes.default.svc.cluster.local
```

Check mail records.

```bash
dig example.com MX
```

Verify website.

```bash
dig example.com
```

Check reverse DNS.

```bash
dig -x 192.168.1.10
```

---

# Production Perspective

DNS is critical for:

- Web applications
- Cloud infrastructure
- Kubernetes clusters
- Load balancers
- Email delivery
- Databases
- API communication
- Service discovery

A DNS outage can make applications unreachable even when the servers themselves are running.

---

# Hands-on Lab

## Task 1

View DNS configuration.

```bash
cat /etc/resolv.conf
```

---

## Task 2

Resolve a hostname.

```bash
getent hosts google.com
```

---

## Task 3

Query DNS using `dig`.

```bash
dig google.com
```

---

## Task 4

Check mail records.

```bash
dig google.com MX
```

---

## Task 5

Perform a reverse lookup.

```bash
dig -x 8.8.8.8
```

---

## Task 6

Use `nslookup`.

```bash
nslookup google.com
```

---

## Task 7

Query a specific DNS server.

```bash
dig @8.8.8.8 google.com
```

---

## Task 8

View DNS cache statistics (if using `systemd-resolved`).

```bash
resolvectl statistics
```

---

# Command Deep Dive

| Command | Purpose | Production Example |
|----------|----------|--------------------|
| `cat /etc/resolv.conf` | View DNS configuration | Verify DNS servers |
| `getent hosts` | Resolve hostnames | Verify name resolution |
| `dig` | Advanced DNS queries | Troubleshooting |
| `nslookup` | Basic DNS queries | Verification |
| `dig -x` | Reverse lookup | Email troubleshooting |
| `resolvectl` | Manage DNS cache | Cache maintenance |

---

# Production Troubleshooting Scenario

!!! danger "Scenario"

    Users report that a web application is unreachable.

Investigation:

Test network connectivity.

```bash
ping 8.8.8.8
```

The ping succeeds.

Test DNS resolution.

```bash
dig example.com
```

No response is returned.

Check DNS configuration.

```bash
cat /etc/resolv.conf
```

The configured DNS server is unreachable.

Update the DNS configuration using the system's network management tool, then verify:

```bash
dig example.com
```

The hostname now resolves successfully, and the application becomes accessible.

---

# Best Practices

- Use reliable and redundant DNS servers.
- Prefer managing DNS through the operating system's network configuration tools rather than editing `/etc/resolv.conf` directly.
- Verify both forward and reverse DNS when troubleshooting.
- Use `dig` for detailed DNS analysis.
- Monitor DNS latency and availability.
- Configure multiple DNS servers for redundancy.

---

# Common Mistakes

❌ Assuming every connectivity issue is caused by DNS.

✅ Verify every connectivity issue is caused by DNS instead of assuming it.

---

❌ Editing `/etc/resolv.conf` directly on systems where it is automatically managed.

✅ Edit `/etc/resolv.conf` directly on systems where it is automatically managed only when appropriate and with a backup.

---

❌ Configuring only one DNS server.

✅ Avoid this mistake: configuring only one DNS server.

---

❌ Ignoring DNS caching during troubleshooting.

✅ Always review DNS caching during troubleshooting.

---

# Interview Questions
## Beginner

1. What does DNS stand for?
2. Why is DNS important?
3. Which port does DNS use?
4. What is an A record?

---

## Intermediate

1. What is the difference between an A record and a CNAME record?
2. What is the purpose of an MX record?
3. How do you perform a reverse DNS lookup?
4. What is the difference between `dig` and `nslookup`?

---

## Architect Level

1. How would you design a highly available DNS architecture?
2. How would you troubleshoot intermittent DNS failures in a Kubernetes cluster?
3. Why is DNS a critical dependency for cloud-native applications?

---

# Summary

In this lesson, you learned:

- DNS fundamentals
- Name resolution
- DNS records
- DNS configuration
- DNS troubleshooting
- Common DNS tools
- Production DNS best practices

DNS is one of the most important services in modern networking. It enables users and applications to communicate using human-readable names instead of IP addresses, making networks scalable and easier to manage.

---

## Key Takeaways

- DNS translates domain names into IP addresses.
- DNS commonly uses UDP port 53 and TCP port 53.
- A records map hostnames to IPv4 addresses.
- AAAA records map hostnames to IPv6 addresses.
- Use `dig` and `nslookup` to troubleshoot DNS.
- Reliable DNS is essential for production applications.

---

## What's Next?

**[Routing — How Linux Sends Network Traffic](routing-on-linux.md)**

You'll explore:

- What routing is
- Routing tables
- Default gateways
- Static and dynamic routing
- The `ip route` command
- Route troubleshooting
- Production networking best practices

Understanding routing will help you determine how Linux systems decide where to send network traffic.
