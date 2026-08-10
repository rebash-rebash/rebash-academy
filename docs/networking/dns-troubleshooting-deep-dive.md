---
title: "DNS Troubleshooting"
description: "Learn DNS troubleshooting — resolution failures, NXDOMAIN, SERVFAIL, dig/nslookup, packet analysis, CoreDNS, and cloud DNS diagnostics."
difficulty: advanced
estimated_time: "220 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 12 · Network Troubleshooting"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - troubleshooting
  - dns
  - dig
  - rebash-networking-mastery
comments: false
status: ready
---

# DNS Troubleshooting — Diagnosing and Resolving Name Resolution Problems

> **DNS Troubleshooting** is the process of identifying and resolving problems related to **domain name resolution**. Since nearly every modern application depends on DNS, even a small DNS issue can make websites, APIs, cloud services, Kubernetes workloads, and enterprise applications appear unavailable. Effective DNS troubleshooting requires understanding the complete resolution process—from the client and local resolver to authoritative name servers—and using tools such as **dig, nslookup, host, ping, tcpdump, and Wireshark**. Every Linux Administrator, Network Engineer, DevOps Engineer, SRE, Cloud Architect, and Kubernetes Administrator should master DNS troubleshooting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 5</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 220 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Troubleshooting</div>

<div markdown>**Lesson:** 5 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the DNS troubleshooting process
- Diagnose DNS resolution failures
- Identify common DNS errors
- Troubleshoot DNS servers
- Analyze DNS packets
- Resolve Kubernetes DNS issues
- Troubleshoot enterprise and cloud DNS environments

---

# Prerequisites

Complete:

- DNS Fundamentals
- DNS Records
- DNS Resolution
- [Ping](ping.md)
- [tcpdump](tcpdump-troubleshooting.md)
- [Wireshark](wireshark.md)

Basic understanding of:

- User Datagram Protocol (UDP)
- Transmission Control Protocol (TCP)
- IP Networking

---

# Why Do We Need DNS Troubleshooting?

Imagine users report:

```text
Website

Cannot

Be

Accessed
```

Possible causes:

- DNS Server Down
- Incorrect DNS Record
- Expired Cache
- Firewall Blocking DNS
- Wrong Resolver
- DNS Timeout

DNS troubleshooting identifies where resolution fails.

---

# DNS Resolution Process

Before troubleshooting, understand the normal flow.

```text
Application

↓

Local Resolver

↓

Recursive DNS

↓

Root Server

↓

TLD Server

↓

Authoritative DNS

↓

IP Address

↓

Application
```

A failure at any step can prevent successful resolution.

---

# Common DNS Problems

Typical issues include:

- NXDOMAIN
- SERVFAIL
- Timeout
- Incorrect Records
- Stale Cache
- DNS Server Unreachable
- Split DNS Misconfiguration

---

# Step 1 — Verify Network Connectivity

Before troubleshooting DNS:

Verify connectivity.

```bash
ping 8.8.8.8
```

If IP connectivity fails:

DNS is **not** the root cause.

Fix network connectivity first.

---

# Step 2 — Verify DNS Resolution

Test using:

```bash
nslookup example.com
```

or

```bash
dig example.com
```

If DNS fails:

Continue investigating DNS infrastructure.

---

# Step 3 — Verify DNS Server

Linux:

```bash
cat /etc/resolv.conf
```

Example:

```text
nameserver 8.8.8.8
```

Verify:

- Correct DNS Server
- Reachable DNS Server

---

# Common DNS Response Codes

| Response | Meaning |
|-----------|----------|
| NOERROR | Successful Resolution |
| NXDOMAIN | Domain Does Not Exist |
| SERVFAIL | Server Failure |
| REFUSED | Query Rejected |
| FORMERR | Invalid Query Format |

---

# NXDOMAIN

Example:

```bash
dig abcxyz.invalid
```

Response:

```text
NXDOMAIN
```

Meaning:

```text
Domain

Does

Not

Exist
```

Possible causes:

- Typographical Error
- Missing DNS Record
- Incorrect Domain Name

---

# SERVFAIL

Example:

```text
SERVFAIL
```

Meaning:

The DNS server could not complete the query.

Possible causes:

- Recursive Resolver Failure
- DNSSEC Issues
- Upstream DNS Failure
- Authoritative Server Unreachable

---

# DNS Timeout

Example:

```text
Connection

Timed Out
```

Possible causes:

- Firewall
- Network Issue
- DNS Server Down
- Packet Loss

---

# Verify DNS Records

Query an A record.

```bash
dig example.com A
```

Query an MX record.

```bash
dig example.com MX
```

Query a TXT record.

```bash
dig example.com TXT
```

Verify that the returned records are correct.

---

# Query a Specific DNS Server

Example:

```bash
dig @8.8.8.8 example.com
```

Useful for comparing responses from multiple DNS servers.

---

# Reverse DNS Lookup

Query a PTR record.

```bash
dig -x 8.8.8.8
```

Useful for:

- Mail Servers
- Security Logs
- Reverse DNS Validation

---

# DNS Cache Issues

Applications may receive outdated responses because of caching.

Flush cache.

Linux (systemd-resolved):

```bash
sudo resolvectl flush-caches
```

Windows:

```powershell
ipconfig /flushdns
```

---

# DNS Packet Capture

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

Observe:

```text
DNS Query

↓

DNS Response
```

Verify:

- Queries Leave
- Responses Return

---

# Analyze DNS in Wireshark

Apply filter:

```text
dns
```

Inspect:

- Query
- Response
- Response Code
- Record Type
- TTL

---

# Split DNS Troubleshooting

Example:

Internal:

```text
app.company.local

↓

10.0.0.15
```

External:

```text
app.company.com

↓

203.0.113.10
```

Verify clients receive the correct response based on their network location.

---

# Kubernetes DNS Troubleshooting

Test from a Pod.

```bash
kubectl exec -it busybox -- nslookup kubernetes.default
```

Verify:

- CoreDNS
- Service Discovery
- DNS Resolution

---

# CoreDNS Troubleshooting

Check CoreDNS Pods.

```bash
kubectl get pods -n kube-system
```

View logs.

```bash
kubectl logs -n kube-system deployment/coredns
```

Inspect configuration.

```bash
kubectl get configmap coredns -n kube-system -o yaml
```

---

# Cloud DNS Troubleshooting

Verify:

- AWS Route 53
- Azure DNS
- Google Cloud DNS

Check:

- DNS Records
- Private Zones
- Public Zones
- VPC/VNet Associations

---

# Enterprise DNS Workflow

```text
Client

↓

DNS Server

↓

Recursive Resolver

↓

Authoritative DNS

↓

Response
```

Every stage should be verified during troubleshooting.

---

# Common DNS Tools

| Tool | Purpose |
|------|----------|
| dig | Detailed DNS Queries |
| nslookup | DNS Lookup |
| host | Quick DNS Query |
| ping | Basic Name Resolution Test |
| tcpdump | DNS Packet Capture |
| Wireshark | DNS Packet Analysis |

---

# CLI Examples

Query DNS.

```bash
dig example.com
```

Query a specific server.

```bash
dig @8.8.8.8 example.com
```

Use nslookup.

```bash
nslookup example.com
```

Perform reverse lookup.

```bash
dig -x 8.8.8.8
```

Capture DNS packets.

```bash
sudo tcpdump port 53
```

---

# Hands-on Lab

## Task 1

Verify internet connectivity.

```bash
ping 8.8.8.8
```

---

## Task 2

Resolve a hostname.

```bash
dig example.com
```

---

## Task 3

Query multiple DNS servers.

Compare results.

---

## Task 4

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

---

## Task 5

Open the packet capture in Wireshark.

Filter:

```text
dns
```

Inspect the DNS query and response.

---

## Task 6

Deploy a BusyBox Pod.

Test Kubernetes DNS.

```bash
kubectl exec -it busybox -- nslookup kubernetes.default
```

---

## Task 7

Flush the DNS cache and repeat the query.

Observe any differences.

---

## Task 8

Draw the complete DNS resolution process from:

```text
Browser

↓

Local Resolver

↓

Recursive DNS

↓

Root

↓

TLD

↓

Authoritative DNS

↓

IP Address

↓

Browser
```

Identify where each failure scenario can occur.

---

# Production Troubleshooting

Problem:

```text
Website

Not

Reachable

By

Hostname
```

Check:

- IP Connectivity
- DNS Server
- DNS Records
- Resolver Configuration
- Cache
- Firewall
- CoreDNS
- Cloud DNS
- Packet Capture

Workflow:

```text
Ping

↓

dig

↓

nslookup

↓

tcpdump

↓

Wireshark

↓

Root Cause
```

---

# dig vs nslookup

| dig | nslookup |
|------|-----------|
| Detailed Output | Simple Output |
| Preferred by Professionals | Beginner Friendly |
| Supports Advanced Queries | Basic Queries |
| Better for Automation | Good for Quick Checks |
| Extensive Debug Information | Limited Detail |

---

# Common Mistakes

❌ Assuming every connectivity issue is a DNS problem.

✅ Verify IP connectivity first.

---

❌ Testing only one DNS server.

✅ Compare responses from multiple resolvers.

---

❌ Ignoring DNS caching.

✅ Flush caches when validating changes.

---

❌ Forgetting reverse lookups.

✅ Verify PTR records where required.

---

❌ Overlooking Kubernetes CoreDNS.

✅ Check CoreDNS health for cluster DNS issues.

---

# Best Practices

- Verify network connectivity before troubleshooting DNS.
- Use **dig** for detailed diagnostics.
- Compare results across multiple DNS servers.
- Capture DNS traffic with tcpdump when necessary.
- Analyze DNS packets using Wireshark.
- Monitor DNS latency in production.
- Keep DNS records accurate and up to date.
- Regularly validate CoreDNS health in Kubernetes clusters.

---

# Interview Questions

## Beginner

1. What is DNS troubleshooting?
2. What does NXDOMAIN mean?
3. What is SERVFAIL?
4. What is the difference between `dig` and `nslookup`?

---

## Intermediate

1. Explain the DNS resolution process.
2. How do you troubleshoot DNS timeouts?
3. How do you verify DNS packet exchanges?
4. How do you troubleshoot Kubernetes DNS?

---

## Architect Level

1. Design a production DNS troubleshooting workflow.
2. Explain how to diagnose intermittent DNS failures in a hybrid cloud environment.
3. How would you troubleshoot inconsistent DNS responses across multiple regions?

---

# Summary

In this lesson, you learned:

- DNS Troubleshooting
- DNS Resolution
- NXDOMAIN
- SERVFAIL
- DNS Timeouts
- DNS Packet Analysis
- CoreDNS Troubleshooting
- Cloud DNS
- Enterprise DNS Troubleshooting

DNS is a foundational service for modern applications, and failures can impact every layer of an infrastructure. By following a structured troubleshooting approach—from verifying connectivity to analyzing DNS packets—you can quickly identify and resolve name resolution issues across enterprise networks, cloud platforms, and Kubernetes clusters.

---

## Key Takeaways

- Verify **network connectivity** before investigating DNS.
- Use **dig** and **nslookup** to validate DNS resolution.
- Understand common DNS responses such as **NOERROR**, **NXDOMAIN**, and **SERVFAIL**.
- Capture DNS traffic with **tcpdump** and inspect it using **Wireshark**.
- Check **CoreDNS** when troubleshooting Kubernetes DNS.
- Follow a systematic workflow to isolate DNS problems efficiently.

---

## What's Next?

**[Routing Issues](routing-issues.md)**

In the next lesson, you'll learn about **Routing Issues**.

You'll explore:

- Route Lookup Process
- Static and Dynamic Routing Problems
- Missing Routes
- Routing Loops
- Asymmetric Routing
- Route Tables
- Production Routing Troubleshooting

By the end of the lesson, you'll be able to identify and resolve routing problems across enterprise networks, cloud infrastructures, and Kubernetes environments.
