---
title: "Linux nslookup Command"
description: "Learn Linux nslookup — query DNS records, perform reverse lookups, use interactive mode, and compare nslookup with dig for DNS troubleshooting."
difficulty: beginner
estimated_time: "110 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 9 · Linux Networking"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - linux
  - nslookup
  - dns
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `nslookup` Command — Querying and Troubleshooting DNS

> **`nslookup` (Name Server Lookup)** is a command-line utility used to query the **Domain Name System (DNS)** for information about domain names, IP addresses, mail servers, and other DNS records. It provides a simple way to verify DNS resolution, troubleshoot name resolution problems, perform reverse lookups, and query specific DNS servers. Although modern Linux systems recommend using **`dig`** for advanced DNS troubleshooting, `nslookup` remains widely available and commonly used across Linux, Windows, and enterprise environments. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand how to use `nslookup`.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 110 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `nslookup` command
- Query DNS records
- Perform reverse DNS lookups
- Query specific DNS servers
- Use interactive mode
- Troubleshoot DNS issues
- Compare `nslookup` with `dig`

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)
- [Linux `tcpdump` Command](packet-analysis-tcpdump-wireshark.md)
- [Linux `traceroute` Command](traceroute.md)
- [Linux `dig` Command](dig.md)

Basic understanding of:

- DNS
- DNS Records
- IP Addressing

---

# Why Learn `nslookup`?

Imagine users report:

- Website Not Loading
- Email Delivery Problems
- API Hostname Not Resolving
- Internal DNS Failure

The first question is:

```text
Can DNS

Resolve

The Hostname?
```

One of the quickest tools to verify this is:

```bash
nslookup
```

---

# What is `nslookup`?

`nslookup` stands for:

```text
Name Server Lookup
```

It queries DNS servers to retrieve:

- IP Addresses
- Hostnames
- Mail Servers
- Name Servers
- DNS Records

---

# DNS Resolution Process

```text
Application

↓

Resolver

↓

DNS Server

↓

Authoritative Server

↓

DNS Response
```

`nslookup` verifies whether this process is working correctly.

---

# Basic Syntax

```bash
nslookup domain
```

Example:

```bash
nslookup google.com
```

---

# Install nslookup

Ubuntu/Debian

```bash
sudo apt install dnsutils
```

RHEL/CentOS

```bash
sudo dnf install bind-utils
```

---

# Basic Lookup

```bash
nslookup google.com
```

Example output:

```text
Server: 8.8.8.8

Address: 8.8.8.8

Name: google.com

Address: 142.250.x.x
```

---

# Query a Specific DNS Server

```bash
nslookup google.com 8.8.8.8
```

This sends the query directly to Google's public DNS server.

---

# Query Cloudflare DNS

```bash
nslookup google.com 1.1.1.1
```

---

# Reverse DNS Lookup

Lookup an IP address.

```bash
nslookup 8.8.8.8
```

Returns:

```text
Hostname

Associated

With

The IP
```

---

# Interactive Mode

Start interactive mode.

```bash
nslookup
```

Prompt:

```text
>
```

Example:

```text
> google.com
```

Exit:

```text
exit
```

---

# Change Record Type

Inside interactive mode:

```text
set type=MX
```

Query:

```text
gmail.com
```

Returns:

```text
Mail Servers
```

---

# Query MX Records

Non-interactive:

```bash
nslookup -type=MX gmail.com
```

---

# Query NS Records

```bash
nslookup -type=NS google.com
```

---

# Query A Records

```bash
nslookup -type=A google.com
```

---

# Query AAAA Records

```bash
nslookup -type=AAAA google.com
```

---

# Query TXT Records

```bash
nslookup -type=TXT google.com
```

Useful for viewing:

- Sender Policy Framework (SPF) Records
- Domain Verification
- Security Policies

---

# Query SOA Record

```bash
nslookup -type=SOA google.com
```

Displays the Start of Authority record.

---

# Enterprise Example

Users cannot access:

```text
portal.company.com
```

Administrator runs:

```bash
nslookup portal.company.com
```

Questions answered:

- Does DNS resolve?
- Which DNS server responded?
- Is the IP address correct?

---

# Cloud Perspective

Cloud engineers use `nslookup` to verify:

- Load Balancer Hostnames
- Cloud DNS
- Private DNS Zones
- Hybrid DNS
- Service Discovery

---

# Kubernetes Perspective

Test Kubernetes service resolution.

```bash
nslookup kubernetes.default.svc.cluster.local
```

Useful for troubleshooting:

- CoreDNS
- Service Discovery
- Internal Cluster DNS

---

# Linux Perspective

Basic lookup.

```bash
nslookup google.com
```

Specific DNS server.

```bash
nslookup google.com 8.8.8.8
```

Reverse lookup.

```bash
nslookup 8.8.8.8
```

MX lookup.

```bash
nslookup -type=MX gmail.com
```

---

# Common DNS Record Types

| Record | Purpose |
|----------|----------|
| A | IPv4 Address |
| AAAA | IPv6 Address |
| MX | Mail Server |
| NS | Name Server |
| CNAME | Alias |
| TXT | Text Record |
| PTR | Reverse Lookup |
| SOA | Start of Authority |

---

# Interactive Session Example

```text
$ nslookup

>

set type=MX

>

gmail.com

>

set type=NS

>

google.com

>

exit
```

Interactive mode allows multiple queries without restarting the command.

---

# Common `nslookup` Commands

| Command | Purpose |
|----------|----------|
| `nslookup domain` | Basic lookup |
| `nslookup IP` | Reverse lookup |
| `nslookup domain DNS_SERVER` | Query specific DNS server |
| `nslookup -type=A` | IPv4 lookup |
| `nslookup -type=AAAA` | IPv6 lookup |
| `nslookup -type=MX` | Mail servers |
| `nslookup -type=NS` | Name servers |
| `nslookup -type=TXT` | TXT records |
| `nslookup -type=SOA` | SOA record |

---

# Hands-on Lab

## Task 1

Lookup Google.

```bash
nslookup google.com
```

---

## Task 2

Lookup using Google's DNS.

```bash
nslookup google.com 8.8.8.8
```

---

## Task 3

Perform reverse lookup.

```bash
nslookup 8.8.8.8
```

---

## Task 4

Lookup mail servers.

```bash
nslookup -type=MX gmail.com
```

---

## Task 5

Lookup authoritative name servers.

```bash
nslookup -type=NS google.com
```

---

## Task 6

Lookup TXT records.

```bash
nslookup -type=TXT google.com
```

---

## Task 7

Use interactive mode.

```bash
nslookup
```

Query multiple record types without exiting.

---

## Task 8

Compare the output of:

```bash
nslookup google.com
```

and

```bash
dig google.com
```

Identify differences in output format and diagnostic information.

---

# Production Troubleshooting

Problem:

```text
Application

Cannot Resolve

Database Hostname
```

Step 1

```bash
nslookup database.company.com
```

↓

Resolved?

↓

No

↓

Try:

```bash
nslookup database.company.com 8.8.8.8
```

↓

Works?

↓

Yes

↓

Problem:

```text
Local DNS Server
```

↓

Investigate:

- DNS Server
- DNS Records
- Network Connectivity
- Firewall

---

# nslookup vs dig

| nslookup | dig |
|-----------|-----|
| Simple Output | Detailed Output |
| Easy to Learn | More Powerful |
| Interactive Mode | Advanced Query Options |
| Cross-Platform | Preferred on Linux |
| Good for Quick Checks | Better for Production Troubleshooting |

---

# Common Mistakes

❌ Assuming the local DNS server is always correct.

✅ Test with multiple DNS servers.

---

❌ Forgetting to specify record types.

✅ Query the required record explicitly.

---

❌ Ignoring reverse lookups.

✅ Verify both forward and reverse DNS.

---

❌ Confusing DNS issues with network issues.

✅ Verify connectivity using `ping` and `traceroute`.

---

❌ Relying only on `nslookup`.

✅ Use `dig` for deeper DNS analysis.

---

# Best Practices

- Use `nslookup` for quick DNS verification.
- Query multiple DNS servers when troubleshooting.
- Verify both forward and reverse DNS records.
- Check MX, NS, and TXT records when diagnosing email or domain issues.
- Use `dig` when more detailed DNS diagnostics are required.
- Document production DNS configurations.
- Monitor DNS changes after updates.

---

# Interview Questions

## Beginner

1. What is `nslookup`?
2. How do you perform a reverse DNS lookup?
3. How do you query a specific DNS server?
4. What is an MX record?

---

## Intermediate

1. Compare `nslookup` and `dig`.
2. Explain interactive mode.
3. How do you troubleshoot DNS failures using `nslookup`?
4. What are the common DNS record types?

---

## Architect Level

1. Design a DNS troubleshooting workflow using `nslookup`.
2. How would you diagnose intermittent DNS failures across multiple cloud regions?
3. Explain how you would validate DNS after migrating enterprise services.

---

# Summary

In this lesson, you learned:

- The `nslookup` command
- DNS Queries
- Reverse DNS Lookups
- Interactive Mode
- DNS Record Types
- Querying Specific DNS Servers
- Enterprise DNS Troubleshooting

`nslookup` is a simple and effective DNS diagnostic utility that enables administrators to verify hostname resolution, inspect DNS records, perform reverse lookups, and troubleshoot DNS problems. While `dig` offers more advanced diagnostics, `nslookup` remains widely used due to its simplicity, availability, and cross-platform support.

---

## Key Takeaways

- `nslookup` is a **simple DNS query tool**.
- Query **A**, **AAAA**, **MX**, **NS**, **TXT**, and **SOA** records.
- Perform reverse lookups by querying an IP address.
- Query different DNS servers to compare responses.
- Use interactive mode for multiple DNS queries.
- Use `dig` for advanced DNS troubleshooting and `nslookup` for quick verification.

---

## What's Next?

**[curl](curl.md)**

In the next lesson, you'll learn about **`curl`**.

You'll explore:

- What `curl` is
- HTTP and HTTPS Requests
- REST API Testing
- Request Headers
- Authentication
- File Downloads
- API Debugging

By the end of the lesson, you'll be able to interact with web servers, test REST APIs, inspect HTTP responses, troubleshoot web services, and automate HTTP-based workflows using one of the most widely used command-line tools in Linux.
