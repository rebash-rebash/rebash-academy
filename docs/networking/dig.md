---
title: "Linux dig Command"
description: "Learn Linux dig — query DNS records, perform reverse lookups, trace resolution, and troubleshoot production DNS issues in enterprise and Kubernetes environments."
difficulty: beginner
estimated_time: "140 min"
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
  - dig
  - dns
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `dig` Command — Querying and Troubleshooting DNS

> **`dig` (Domain Information Groper)** is the most powerful command-line utility for querying the **Domain Name System (DNS)**. It is used to retrieve DNS records, verify name resolution, troubleshoot DNS issues, inspect authoritative name servers, perform reverse lookups, and validate DNS configurations. Unlike `nslookup`, `dig` provides detailed information about DNS queries and responses, making it the preferred DNS troubleshooting tool for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SRE), Network Engineers, and Security Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 140 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 6 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the `dig` command
- Query DNS records
- Troubleshoot DNS resolution
- Perform reverse DNS lookups
- Query specific DNS servers
- Understand authoritative responses
- Diagnose production DNS issues

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)
- [Linux `tcpdump` Command](packet-analysis-tcpdump-wireshark.md)
- [Linux `traceroute` Command](traceroute.md)

Basic understanding of:

- DNS
- IP Addressing
- DNS Records

---

# Why Learn `dig`?

Suppose users report:

- Website Not Opening
- API Not Reachable
- Email Delivery Failure
- Kubernetes Service Resolution Problems
- DNS Timeout

Network connectivity works.

```text
Ping

Works
```

But:

```text
google.com

Cannot Resolve
```

The first tool most Linux engineers use is:

```bash
dig
```

---

# What is `dig`?

`dig` stands for:

```text
Domain Information Groper
```

It queries DNS servers and displays:

- DNS Records
- Query Status
- Name Servers
- Response Time
- Time To Live (TTL)
- Authority Information

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

Response
```

`dig` helps inspect every stage of this process.

---

# Basic Syntax

```bash
dig domain
```

Example:

```bash
dig google.com
```

---

# Install dig

Ubuntu/Debian

```bash
sudo apt install dnsutils
```

RHEL/CentOS

```bash
sudo dnf install bind-utils
```

---

# Basic DNS Query

```bash
dig google.com
```

Returns:

- IP Address
- TTL
- Query Time
- DNS Server
- Response Status

---

# Understanding Output

Important sections:

```text
QUESTION SECTION
```

The requested record.

```text
ANSWER SECTION
```

The returned DNS record.

```text
AUTHORITY SECTION
```

Authoritative name servers.

```text
ADDITIONAL SECTION
```

Additional useful records.

---

# Query A Record

```bash
dig google.com A
```

Returns:

```text
IPv4 Address
```

---

# Query AAAA Record

```bash
dig google.com AAAA
```

Returns:

```text
IPv6 Address
```

---

# Query MX Record

```bash
dig gmail.com MX
```

Returns:

```text
Mail Servers
```

---

# Query NS Record

```bash
dig google.com NS
```

Returns:

```text
Authoritative Name Servers
```

---

# Query CNAME Record

```bash
dig www.github.com CNAME
```

Returns:

```text
Canonical Name
```

---

# Query TXT Record

```bash
dig google.com TXT
```

Commonly used for:

- Sender Policy Framework (SPF)
- DomainKeys Identified Mail (DKIM)
- Domain Verification
- Security Policies

---

# Reverse DNS Lookup

```bash
dig -x 8.8.8.8
```

Returns:

```text
PTR Record
```

Maps:

```text
IP Address

↓

Hostname
```

---

# Query Specific DNS Server

Example:

```bash
dig @8.8.8.8 google.com
```

Queries Google's DNS server directly.

---

# Query Cloudflare DNS

```bash
dig @1.1.1.1 google.com
```

---

# Query Any Record

```bash
dig google.com ANY
```

> **Note:** Many public DNS servers restrict or minimise responses to `ANY` queries for security and performance reasons. Do not rely on `ANY` to retrieve all record types.

---

# Short Output

```bash
dig +short google.com
```

Returns only:

```text
IP Address
```

Useful for scripts.

---

# Display Trace

```bash
dig +trace google.com
```

Shows the complete DNS resolution path:

```text
Root

↓

Top-Level Domain (TLD)

↓

Authoritative Server
```

---

# Display TTL

Example output:

```text
300
```

Meaning:

```text
5 Minutes
```

The DNS record can be cached for five minutes.

---

# Check DNSSEC

```bash
dig +dnssec google.com
```

Displays Domain Name System Security Extensions (DNSSEC)-related information when available.

---

# DNS Troubleshooting Workflow

```text
Application

↓

Resolver

↓

DNS Server

↓

Authoritative Server
```

Use `dig` to identify where failures occur.

---

# Enterprise Example

Users cannot access:

```text
portal.company.com
```

Run:

```bash
dig portal.company.com
```

Questions answered:

- Does DNS resolve?
- Correct IP?
- TTL?
- Authoritative Server?
- NXDOMAIN?

---

# Cloud Perspective

Cloud engineers use `dig` to verify:

- Load Balancer DNS
- Kubernetes Ingress
- Private DNS Zones
- Cloud DNS
- Internal Service Discovery

---

# Kubernetes Perspective

DNS is essential for Kubernetes.

Example:

```bash
dig kubernetes.default.svc.cluster.local
```

Useful for troubleshooting:

- CoreDNS
- Service Discovery
- Internal Name Resolution

---

# Linux Perspective

Basic query.

```bash
dig google.com
```

Short output.

```bash
dig +short google.com
```

Reverse lookup.

```bash
dig -x 8.8.8.8
```

Specific DNS server.

```bash
dig @8.8.8.8 google.com
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

# Common `dig` Commands

| Command | Purpose |
|----------|----------|
| `dig domain` | Basic DNS query |
| `dig domain A` | IPv4 lookup |
| `dig domain AAAA` | IPv6 lookup |
| `dig domain MX` | Mail servers |
| `dig domain NS` | Name servers |
| `dig -x IP` | Reverse lookup |
| `dig @DNS_SERVER domain` | Query specific DNS server |
| `dig +short domain` | Short output |
| `dig +trace domain` | Full DNS resolution path |

---

# Hands-on Lab

## Task 1

Query Google.

```bash
dig google.com
```

---

## Task 2

Query IPv4 address.

```bash
dig google.com A
```

---

## Task 3

Query IPv6 address.

```bash
dig google.com AAAA
```

---

## Task 4

Query mail servers.

```bash
dig gmail.com MX
```

---

## Task 5

Query authoritative name servers.

```bash
dig google.com NS
```

---

## Task 6

Perform reverse lookup.

```bash
dig -x 8.8.8.8
```

---

## Task 7

Query Google's public DNS server.

```bash
dig @8.8.8.8 google.com
```

Compare the result with your organisation's default DNS resolver.

---

## Task 8

Trace DNS resolution.

```bash
dig +trace google.com
```

Observe the path from the root servers to the authoritative name servers.

---

# Production Troubleshooting

Problem:

```text
Website

Not Resolving
```

Step 1

```bash
dig website.com
```

↓

Resolved?

↓

No

↓

Check:

```bash
dig @8.8.8.8 website.com
```

↓

Works?

↓

Yes

↓

Problem:

```text
Local DNS
```

↓

No

↓

Investigate:

- Authoritative DNS
- DNS Records
- Firewall
- Network Connectivity

---

# dig vs nslookup

| dig | nslookup |
|------|----------|
| Modern DNS Tool | Legacy DNS Tool |
| Detailed Output | Simpler Output |
| Preferred for Linux | Available on Many Platforms |
| Better for Troubleshooting | Better for Basic Queries |

---

# Common Mistakes

❌ Querying the wrong DNS server.

✅ Specify the server using `@server` when needed.

---

❌ Assuming cached results are authoritative.

✅ Query authoritative servers or use `+trace`.

---

❌ Ignoring TTL values.

✅ Consider DNS caching when troubleshooting changes.

---

❌ Relying on `ANY` queries.

✅ Query specific record types instead.

---

❌ Forgetting reverse lookups.

✅ Use `-x` to troubleshoot IP-to-hostname mappings.

---

# Best Practices

- Query specific record types whenever possible.
- Use `+short` in scripts.
- Use `+trace` for delegation troubleshooting.
- Compare responses from multiple DNS servers.
- Verify TTL before changing DNS records.
- Test both public and private DNS zones.
- Document production DNS configurations.

---

# Interview Questions

## Beginner

1. What is `dig`?
2. How do you query an A record?
3. What is a reverse DNS lookup?
4. What does `dig +short` do?

---

## Intermediate

1. Explain the different sections of `dig` output.
2. How do you query a specific DNS server?
3. What is TTL?
4. Explain `dig +trace`.

---

## Architect Level

1. Design a DNS troubleshooting workflow using `dig`.
2. Explain how you would troubleshoot intermittent DNS failures in Kubernetes.
3. How would you validate DNS propagation after migrating to a new DNS provider?

---

# Summary

In this lesson, you learned:

- The `dig` command
- DNS Queries
- DNS Record Types
- Reverse DNS Lookups
- Authoritative Name Servers
- DNS Tracing
- TTL Analysis
- Enterprise DNS Troubleshooting

`dig` is the most powerful DNS diagnostic tool available on Linux. It enables engineers to query DNS records, inspect authoritative responses, validate DNS configurations, troubleshoot name resolution problems, and analyse DNS behaviour in enterprise, cloud, and Kubernetes environments. Mastering `dig` is essential for production network and infrastructure operations.

---

## Key Takeaways

- `dig` is the **preferred DNS troubleshooting tool** on Linux.
- Query specific record types such as **A**, **AAAA**, **MX**, **NS**, and **TXT**.
- Use **`dig -x`** for reverse DNS lookups.
- Use **`@server`** to query a specific DNS resolver.
- Use **`+short`** for concise output and **`+trace`** to follow the complete DNS resolution path.
- `dig` is indispensable for troubleshooting DNS issues in enterprise, cloud, and Kubernetes environments.

---

## What's Next?

**[nslookup](nslookup.md)**

In the next lesson, you'll learn about **`nslookup`**.

You'll explore:

- What `nslookup` is
- Basic DNS Queries
- Querying Specific Record Types
- Interactive Mode
- Reverse DNS Lookups
- DNS Troubleshooting
- Comparing `nslookup` with `dig`

By the end of the lesson, you'll understand how to use `nslookup` for quick DNS lookups, troubleshoot common DNS issues, and know when to choose `nslookup` versus `dig`.
