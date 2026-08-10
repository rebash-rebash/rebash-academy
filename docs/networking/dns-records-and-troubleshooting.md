---
title: "DNS Records"
description: "Learn DNS Resource Records (RRs) — A, AAAA, CNAME, MX, NS, TXT, PTR, SOA, and SRV — plus TTL, forward and reverse lookups, and Linux dig queries."
difficulty: beginner
estimated_time: "100 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 6 · DNS and DHCP"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - dns
  - dig
  - dns-records
  - rebash-networking-mastery
comments: false
status: ready
---

# DNS Records — The Building Blocks of DNS

> **DNS Records** (also called **Resource Records (RRs)**) are entries stored in a DNS zone that define how a domain behaves. They map domain names to IP addresses, identify mail servers, specify authoritative name servers, verify domain ownership, and provide configuration information for applications and services. Every website, email service, cloud application, Kubernetes cluster, and enterprise network depends on DNS records. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand the most common DNS record types.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 6: DNS & DHCP → Lesson 2</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 100 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** DNS & DHCP</div>

<div markdown>**Lesson:** 2 of 7</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand DNS Records
- Learn the purpose of different record types
- Configure common DNS records
- Understand forward and reverse DNS
- Apply DNS records in enterprise and cloud environments
- Troubleshoot DNS record issues

---

# Prerequisites

Complete:

- [DNS Fundamentals](dns-fundamentals.md)

---

# Why Learn DNS Records?

Imagine typing:

```text
www.rebash.in
```

How does DNS know:

- Website IP Address?
- Mail Server?
- Name Server?
- IPv6 Address?

The answer lies in:

```text
DNS Records
```

---

# What are DNS Records?

DNS Records are entries stored inside a DNS zone.

Example:

```text
google.com

↓

A Record

↓

142.250.x.x
```

Each record has a specific purpose.

---

# Common DNS Records

The most common DNS records are:

- A
- AAAA
- CNAME
- MX
- NS
- TXT
- PTR
- SOA
- SRV

---

# A Record

**A (Address) Record**

Maps:

```text
Hostname

↓

IPv4 Address
```

Example:

```text
www.example.com

↓

192.168.10.20
```

Example DNS record:

```text
www    IN    A      192.168.10.20
```

---

# AAAA Record

Maps:

```text
Hostname

↓

IPv6 Address
```

Example:

```text
www.example.com

↓

2001:db8::20
```

Example record:

```text
www    IN    AAAA   2001:db8::20
```

---

# CNAME Record

**Canonical Name Record**

Creates an alias.

Example:

```text
blog.example.com

↓

www.example.com
```

Example record:

```text
blog    IN    CNAME    www.example.com.
```

Instead of creating multiple A records, several hostnames can point to one canonical name.

---

# MX Record

**Mail Exchange Record**

Specifies where email should be delivered.

Example:

```text
example.com

↓

mail.example.com
```

Record:

```text
example.com.    IN    MX    10 mail.example.com.
```

Priority:

```text
10

↓

Higher Priority
```

Lower preference values indicate higher priority.

---

# NS Record

**Name Server Record**

Identifies the authoritative DNS servers for a domain.

Example:

```text
example.com

↓

ns1.example.com

↓

ns2.example.com
```

Example record:

```text
example.com.    IN    NS    ns1.example.com.
```

---

# TXT Record

Stores arbitrary text information.

Common uses:

- Sender Policy Framework (SPF)
- DomainKeys Identified Mail (DKIM)
- Domain-based Message Authentication, Reporting and Conformance (DMARC)
- Domain Verification
- Cloud Service Validation

Example:

```text
example.com.

↓

TXT

↓

"v=spf1 include:_spf.google.com ~all"
```

---

# PTR Record

**Pointer Record**

Used for:

```text
Reverse DNS

IP Address

↓

Hostname
```

Example:

```text
8.8.8.8

↓

dns.google
```

PTR records are stored in reverse lookup zones.

---

# SOA Record

**Start of Authority Record**

Every DNS zone contains exactly one SOA record.

It defines:

- Primary Name Server
- Administrator Email
- Serial Number
- Refresh Timer
- Retry Timer
- Expire Timer
- Minimum Time To Live (TTL)

Example:

```text
example.com.

↓

SOA
```

---

# SRV Record

**Service Record**

Specifies the location of network services.

Example:

```text
_sip._tcp.example.com
```

Contains:

- Service
- Protocol
- Priority
- Weight
- Port
- Target

Often used by:

- Microsoft Active Directory
- Session Initiation Protocol (SIP)
- Extensible Messaging and Presence Protocol (XMPP)
- Kubernetes
- Service Discovery

---

# Record Comparison

| Record | Purpose |
|----------|----------|
| A | Hostname → IPv4 |
| AAAA | Hostname → IPv6 |
| CNAME | Alias |
| MX | Mail Server |
| NS | Name Server |
| TXT | Text Information |
| PTR | Reverse Lookup |
| SOA | Zone Information |
| SRV | Service Discovery |

---

# Time To Live (TTL)

Every DNS record contains:

```text
TTL

(Time To Live)
```

Example:

```text
3600 Seconds
```

Meaning:

```text
Cache

1 Hour
```

After TTL expires, the resolver requests fresh information.

---

# Forward Lookup

Example:

```text
example.com

↓

A Record

↓

192.168.10.10
```

---

# Reverse Lookup

Example:

```text
192.168.10.10

↓

PTR Record

↓

example.com
```

---

# Enterprise Example

Company:

```text
portal.company.com

↓

A Record
```

```text
mail.company.com

↓

MX Record
```

```text
vpn.company.com

↓

A Record
```

```text
teams.company.com

↓

CNAME
```

Different services use different DNS record types.

---

# Cloud Perspective

Cloud providers commonly create DNS records for:

- Load Balancers
- Public IP Addresses
- Private Endpoints
- Storage Accounts
- Kubernetes Ingress
- Content Delivery Network (CDN) Endpoints

Many cloud services automatically manage DNS records during deployment.

---

# Kubernetes Perspective

Kubernetes uses DNS extensively.

Examples:

```text
frontend.default.svc.cluster.local
```

Service discovery relies on DNS records managed by the cluster DNS service.

External DNS controllers can also automatically create:

- A Records
- CNAME Records

for Kubernetes Ingress resources.

---

# Linux Perspective

Query A record.

```bash
dig google.com
```

Query AAAA record.

```bash
dig AAAA google.com
```

Query MX record.

```bash
dig MX gmail.com
```

Query NS record.

```bash
dig NS example.com
```

Query TXT record.

```bash
dig TXT example.com
```

Reverse lookup.

```bash
dig -x 8.8.8.8
```

Alternative tools.

```bash
host google.com
```

```bash
nslookup google.com
```

---

# Example DNS Zone

```text
example.com.

↓

SOA

↓

NS

↓

A

↓

AAAA

↓

MX

↓

TXT

↓

CNAME

↓

SRV
```

Each record contributes different information to the DNS zone.

---

# Advantages of DNS Records

- Flexible Name Resolution
- Email Routing
- IPv4 and IPv6 Support
- Service Discovery
- Domain Verification
- Cloud Integration

---

# Limitations

- Incorrect records can cause application failures
- DNS changes require propagation time
- Misconfigured MX records can affect email delivery
- Incorrect TTL values can delay updates

---

# Hands-on Lab

## Task 1

Query an A record.

```bash
dig google.com
```

---

## Task 2

Query an AAAA record.

```bash
dig AAAA google.com
```

---

## Task 3

Query MX records.

```bash
dig MX gmail.com
```

---

## Task 4

Query NS records.

```bash
dig NS google.com
```

---

## Task 5

Query TXT records.

```bash
dig TXT google.com
```

---

## Task 6

Perform a reverse lookup.

```bash
dig -x 8.8.8.8
```

---

## Task 7

Create a table comparing:

- A
- AAAA
- CNAME
- MX
- NS
- TXT
- PTR
- SOA
- SRV

---

## Task 8

Design DNS records for:

- Company Website
- Mail Server
- VPN Gateway
- Internal Portal
- Kubernetes Ingress

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `dig domain.com` | Query A record |
| `dig AAAA domain.com` | Query IPv6 record |
| `dig MX domain.com` | Query mail records |
| `dig NS domain.com` | Query name servers |
| `dig TXT domain.com` | Query TXT records |
| `dig SRV domain.com` | Query SRV records |
| `dig -x <IP>` | Reverse DNS lookup |
| `host domain.com` | Display DNS information |
| `nslookup domain.com` | DNS lookup utility |

---

# Common Mistakes

❌ Using a CNAME at the zone apex where unsupported.

✅ Use an A or AAAA record unless your DNS provider supports alias records.

---

❌ Confusing A and AAAA records.

✅ A is for IPv4; AAAA is for IPv6.

---

❌ Incorrect MX priorities.

✅ Lower numbers indicate higher priority.

---

❌ Forgetting to update the SOA serial number on manual DNS servers.

✅ Increment the serial after zone changes.

---

❌ Setting an excessively long TTL during migrations.

✅ Lower the TTL before planned DNS changes.

---

# Best Practices

- Use meaningful hostnames.
- Configure both A and AAAA records where IPv6 is available.
- Keep TTL values appropriate for the environment.
- Protect authoritative DNS zones from unauthorised changes.
- Regularly verify DNS records.
- Document DNS changes and maintain version control for zone files.

---

# Interview Questions

## Beginner

1. What is a DNS record?
2. What is an A record?
3. What is an AAAA record?
4. What is a CNAME record?

---

## Intermediate

1. Explain MX records.
2. What is a PTR record?
3. What is an SOA record?
4. What is TTL?

---

## Architect Level

1. Design DNS records for a multi-region enterprise application.
2. Explain how DNS records support cloud load balancers.
3. How would you troubleshoot incorrect DNS record resolution?

---

# Summary

In this lesson, you learned:

- DNS Records
- A Records
- AAAA Records
- CNAME Records
- MX Records
- NS Records
- TXT Records
- PTR Records
- SOA Records
- SRV Records
- TTL
- Linux DNS Query Commands

DNS records define how domains, services, and applications are discovered on the Internet and within enterprise networks. From mapping hostnames to IP addresses to directing email and enabling service discovery, DNS records are a critical part of modern networking, cloud infrastructure, and Kubernetes environments.

---

## Key Takeaways

- **A Records** map hostnames to IPv4 addresses.
- **AAAA Records** map hostnames to IPv6 addresses.
- **CNAME Records** create aliases.
- **MX Records** identify mail servers.
- **NS Records** specify authoritative name servers.
- **TXT Records** store verification and policy information.
- **PTR Records** support reverse DNS lookups.
- **SOA Records** define DNS zone authority and metadata.
- **SRV Records** enable service discovery.

---

## What's Next?

**[DNS Resolution](dns-resolution.md)**

In the next lesson, you'll learn about **DNS Resolution**.

You'll explore:

- Recursive Resolution
- Iterative Resolution
- DNS Query Process
- DNS Caching
- Root, TLD, and Authoritative Servers
- DNS Response Flow
- Enterprise DNS Architecture

By the end of the lesson, you'll understand the complete journey of a DNS query—from entering a domain name in a browser to receiving the correct IP address from authoritative DNS servers.
