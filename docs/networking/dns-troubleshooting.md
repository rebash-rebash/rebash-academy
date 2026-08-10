---
title: "DNS Troubleshooting"
description: "Diagnose DNS resolution failures with a structured workflow — dig, dig +trace, NXDOMAIN, SERVFAIL, cache, hosts file, and enterprise/cloud checks."
difficulty: intermediate
estimated_time: "110 min"
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
  - troubleshooting
  - dig
  - rebash-networking-mastery
comments: false
status: ready
---

# DNS Troubleshooting — Diagnosing and Resolving Name Resolution Problems

> **DNS Troubleshooting** is the process of identifying and resolving issues that prevent devices from translating domain names into IP addresses. Since almost every Internet application depends on the Domain Name System (DNS), even a small DNS issue can make websites, email, cloud services, Kubernetes applications, APIs, and enterprise systems appear unavailable. A structured troubleshooting methodology helps quickly identify whether the problem lies with the client, DNS server, network, DNS records, or external infrastructure. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master DNS troubleshooting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 6: DNS & DHCP → Lesson 7</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 110 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** DNS & DHCP</div>

<div markdown>**Lesson:** 7 of 7</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Troubleshoot DNS issues
- Diagnose DNS resolution failures
- Verify DNS records
- Understand DNS caching problems
- Use Linux DNS troubleshooting tools
- Troubleshoot enterprise and cloud DNS
- Follow a systematic troubleshooting methodology

---

# Prerequisites

Complete:

- [DNS Fundamentals](dns-fundamentals.md)
- [DNS Records](dns-records-and-troubleshooting.md)
- [DNS Resolution](dns-resolution.md)
- [DHCP Process](icmp-arp-dhcp-and-network-services.md)
- [DHCP Relay](dhcp-relay.md)
- [Split DNS](split-dns.md)

---

# Why Learn DNS Troubleshooting?

Imagine a user reports:

```text
google.com

Not Working
```

Possible causes include:

- Internet Failure
- DNS Server Failure
- Incorrect DNS Records
- Firewall Rules
- DNS Cache
- Network Connectivity

Without systematic troubleshooting:

```text
Hours

Lost
```

---

# Common DNS Problems

Most DNS incidents fall into these categories:

- DNS Server Unreachable
- Incorrect DNS Records
- Expired or Stale Cache
- Wrong DNS Configuration
- DNS Propagation Delay
- Firewall Blocking DNS
- Split DNS Misconfiguration

---

# DNS Troubleshooting Workflow

```text
Identify Problem

↓

Check Network

↓

Check DNS Configuration

↓

Query DNS

↓

Verify DNS Records

↓

Check Cache

↓

Test Resolution

↓

Fix Problem
```

---

# Step 1 — Verify Network Connectivity

Before troubleshooting DNS:

Test connectivity.

```bash
ping 8.8.8.8
```

If the IP is reachable:

```text
Network

Working
```

If not:

```text
Network Problem

Not DNS
```

---

# Step 2 — Verify DNS Configuration

Check configured DNS servers.

```bash
cat /etc/resolv.conf
```

Example:

```text
nameserver 8.8.8.8

nameserver 1.1.1.1
```

Verify that the configured DNS servers are correct and reachable.

---

# Step 3 — Test Name Resolution

Query a domain.

```bash
dig google.com
```

or

```bash
nslookup google.com
```

Successful resolution confirms DNS is functioning.

---

# Step 4 — Query Specific DNS Server

Query a known DNS server.

```bash
dig @8.8.8.8 google.com
```

If this succeeds while the default resolver fails:

```text
Local DNS

Problem
```

---

# Step 5 — Check DNS Records

Query specific record types.

A Record:

```bash
dig A example.com
```

AAAA Record:

```bash
dig AAAA example.com
```

MX Record:

```bash
dig MX example.com
```

NS Record:

```bash
dig NS example.com
```

TXT Record:

```bash
dig TXT example.com
```

---

# Step 6 — Trace DNS Resolution

Trace the complete lookup path.

```bash
dig +trace google.com
```

This shows:

```text
Root

↓

Top-Level Domain (TLD)

↓

Authoritative Server
```

Useful for identifying where resolution fails.

---

# Step 7 — Reverse Lookup

Verify reverse DNS.

```bash
dig -x 8.8.8.8
```

or

```bash
host 8.8.8.8
```

---

# Step 8 — Check Local Hosts File

Linux checks:

```text
/etc/hosts
```

Example:

```text
192.168.10.20

webserver.local
```

Incorrect entries can override DNS results.

---

# Step 9 — Check DNS Cache

Cached records may be outdated.

Depending on the Linux distribution and resolver service, you may need to flush or restart the local DNS cache.

Examples:

```bash
sudo systemctl restart systemd-resolved
```

or

```bash
sudo resolvectl flush-caches
```

Availability depends on the DNS resolver in use.

---

# Step 10 — Verify Firewall

DNS uses:

```text
User Datagram Protocol (UDP) Port 53
```

and sometimes:

```text
Transmission Control Protocol (TCP) Port 53
```

Ensure firewalls allow DNS traffic.

---

# Common DNS Errors

## NXDOMAIN

Meaning:

```text
Domain

Does Not Exist
```

Possible causes:

- Typo
- Missing DNS Record
- Incorrect Zone Configuration

---

## SERVFAIL

Meaning:

```text
DNS Server

Failed
```

Possible causes:

- Server Issues
- Domain Name System Security Extensions (DNSSEC) Problems
- Upstream Failure

---

## Timeout

Meaning:

```text
No Response
```

Possible causes:

- Firewall
- Network Failure
- DNS Server Down

---

## REFUSED

Meaning:

```text
Server

Rejected Request
```

Possible causes:

- Access Restrictions
- Access Control List (ACL) Configuration
- Recursive Queries Disabled

---

# Enterprise Troubleshooting

Scenario:

Employee cannot access:

```text
portal.company.com
```

Checklist:

- Network Connectivity
- DNS Server Reachability
- Internal DNS Zone
- Split DNS Configuration
- Firewall Rules
- Application Availability

---

# Cloud Perspective

Cloud DNS issues may involve:

- Private DNS Zones
- Public DNS Zones
- Load Balancers
- Private Endpoints
- Hybrid Cloud Connectivity

Verify that the correct DNS zone is being queried.

---

# Kubernetes Perspective

Common Kubernetes DNS issues:

- CoreDNS Pod Failure
- Incorrect Service Name
- Network Policy Restrictions
- Service Not Running

Useful commands:

```bash
kubectl get pods -n kube-system
```

```bash
kubectl logs deployment/coredns -n kube-system
```

---

# Linux Perspective

Display DNS configuration.

```bash
cat /etc/resolv.conf
```

Query DNS.

```bash
dig google.com
```

Trace resolution.

```bash
dig +trace google.com
```

Query using host.

```bash
host google.com
```

Display resolver configuration.

```bash
resolvectl status
```

(Test on systems using `systemd-resolved`.)

---

# DNS Troubleshooting Example

Problem:

```text
Cannot Open

github.com
```

Steps:

```text
Ping IP

↓

Check Internet

↓

Check DNS Server

↓

dig github.com

↓

Verify A Record

↓

Check Firewall

↓

Resolve Issue
```

---

# Advantages of a Structured Approach

- Faster Diagnosis
- Consistent Results
- Reduced Downtime
- Easier Root Cause Analysis
- Better Incident Documentation

---

# Hands-on Lab

## Task 1

Display configured DNS servers.

```bash
cat /etc/resolv.conf
```

---

## Task 2

Query a domain.

```bash
dig google.com
```

---

## Task 3

Trace DNS resolution.

```bash
dig +trace google.com
```

---

## Task 4

Query a specific DNS server.

```bash
dig @8.8.8.8 google.com
```

---

## Task 5

Perform a reverse lookup.

```bash
dig -x 8.8.8.8
```

---

## Task 6

Check the hosts file.

```bash
cat /etc/hosts
```

---

## Task 7

Create a troubleshooting checklist for:

- NXDOMAIN
- SERVFAIL
- Timeout
- REFUSED

---

## Task 8

Troubleshoot a simulated DNS issue where users cannot reach an internal application.

Document:

- Symptoms
- Investigation
- Root Cause
- Resolution

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `cat /etc/resolv.conf` | View DNS configuration |
| `dig domain.com` | DNS lookup |
| `dig +trace domain.com` | Trace resolution path |
| `dig @server domain.com` | Query specific DNS server |
| `dig -x <IP>` | Reverse lookup |
| `host domain.com` | Display DNS information |
| `nslookup domain.com` | DNS lookup |
| `resolvectl status` | Display resolver status (systemd-resolved) |

---

# Common Mistakes

❌ Assuming every connectivity problem is DNS-related.

✅ Test connectivity using IP addresses first.

---

❌ Ignoring local hosts file entries.

✅ Verify `/etc/hosts`.

---

❌ Troubleshooting only one DNS server.

✅ Test multiple resolvers.

---

❌ Forgetting DNS cache.

✅ Flush or wait for cache expiration if appropriate.

---

❌ Ignoring firewall rules.

✅ Ensure UDP and TCP port 53 are allowed where required.

---

# Best Practices

- Verify network connectivity before troubleshooting DNS.
- Use `dig` as the primary DNS diagnostic tool.
- Query authoritative servers when validating records.
- Keep DNS records documented.
- Monitor DNS server health.
- Maintain redundant DNS infrastructure.
- Test both internal and external DNS in Split DNS environments.

---

# Interview Questions

## Beginner

1. What is DNS troubleshooting?
2. Which command checks DNS resolution?
3. What is NXDOMAIN?
4. What file stores static hostname mappings in Linux?

---

## Intermediate

1. Explain how `dig +trace` works.
2. What causes SERVFAIL?
3. How do you troubleshoot DNS timeouts?
4. Why is reverse DNS important?

---

## Architect Level

1. Design a DNS troubleshooting workflow for an enterprise.
2. How would you diagnose intermittent DNS failures in a hybrid cloud?
3. Explain how you would troubleshoot Split DNS issues.

---

# Summary

In this lesson, you learned:

- DNS Troubleshooting Methodology
- DNS Resolution Failures
- DNS Error Codes
- DNS Cache
- Hosts File
- DNS Configuration
- Linux DNS Diagnostic Commands
- Enterprise and Cloud DNS Troubleshooting

A systematic DNS troubleshooting process helps quickly isolate and resolve name resolution problems. By verifying connectivity, checking resolver configuration, testing DNS records, tracing resolution paths, and validating caches, administrators can efficiently diagnose issues affecting enterprise, cloud, and Internet services.

---

## Key Takeaways

- Always verify **network connectivity** before assuming a DNS problem.
- Use **`dig`** to test DNS resolution and record types.
- **`dig +trace`** identifies failures along the DNS resolution path.
- Check **`/etc/hosts`** and DNS cache during troubleshooting.
- Understand common DNS errors such as **NXDOMAIN**, **SERVFAIL**, and **Timeout**.
- A structured troubleshooting workflow reduces downtime and speeds up incident resolution.

---

# Module 6 Complete!

Congratulations! You have successfully completed **Module 6: DNS & DHCP**.

You now understand:

- DNS Fundamentals
- DNS Records
- DNS Resolution
- DHCP Process
- DHCP Relay
- Split DNS
- DNS Troubleshooting

You now have a strong foundation in two of the most important network infrastructure services used across enterprise networks, cloud platforms, Kubernetes environments, and the Internet.

---

## What's Next?

**[Module 6 Summary — DNS & DHCP](module-6-dns-dhcp-summary.md)**
