---
title: "Linux tcpdump Command"
description: "Learn Linux tcpdump — capture and analyse network packets, filter traffic, save PCAP files, and troubleshoot production connectivity and security issues."
difficulty: intermediate
estimated_time: "150 min"
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
  - tcpdump
  - packet-capture
  - rebash-networking-mastery
comments: false
status: ready
---

# Linux `tcpdump` Command — Capturing and Analyzing Network Packets

> **`tcpdump`** is one of the most powerful command-line network packet analyzers available on Linux and Unix systems. It captures and displays **network packets in real time**, allowing administrators to inspect protocols, troubleshoot connectivity issues, analyse application traffic, investigate security incidents, and debug complex network problems. `tcpdump` works directly with network interfaces using the **libpcap** library and is widely used by Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SRE), Network Engineers, and Security Analysts.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 9: Linux Networking → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 150 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Linux Networking</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand `tcpdump`
- Capture network packets
- Filter traffic efficiently
- Analyse network protocols
- Save and read packet captures
- Troubleshoot production networking issues
- Perform basic security investigations

---

# Prerequisites

Complete:

- [Linux `ip` Command](linux-networking-toolkit.md)
- [Linux `ss` Command](ss.md)
- [Linux `netstat` Command](netstat.md)

Basic understanding of:

- TCP/IP
- OSI Model
- Ports
- Routing

---

# Why Learn `tcpdump`?

Suppose users report:

- Website Not Working
- API Timeout
- DNS Failure
- Packet Loss
- Slow Application
- Unknown Network Traffic

Sometimes:

```text
Everything

Looks

Correct
```

But packets are not reaching their destination.

The best way to investigate is to:

```text
Capture

The Packets
```

using:

```bash
tcpdump
```

---

# What is `tcpdump`?

`tcpdump` captures packets directly from a network interface.

It can inspect:

- Ethernet Frames
- IPv4
- IPv6
- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)
- Internet Control Message Protocol (ICMP)
- Address Resolution Protocol (ARP)
- Domain Name System (DNS)
- HTTP
- HTTPS Metadata
- Many Other Protocols

---

# Packet Capture Workflow

```text
Application

↓

TCP/UDP

↓

IP

↓

Network Interface

↓

tcpdump
```

Every packet can be inspected before it leaves or after it reaches the interface.

---

# Basic Syntax

```bash
tcpdump [options] [filter]
```

Example:

```bash
sudo tcpdump
```

Administrator privileges are usually required because packet capture accesses raw network traffic.

---

# List Available Interfaces

```bash
tcpdump -D
```

Example:

```text
1.eth0

2.lo

3.docker0
```

---

# Capture Packets

Capture packets on the default interface.

```bash
sudo tcpdump
```

---

# Capture on Specific Interface

```bash
sudo tcpdump -i eth0
```

---

# Capture on All Interfaces

```bash
sudo tcpdump -i any
```

Useful for servers with multiple interfaces.

---

# Limit Number of Packets

Capture only ten packets.

```bash
sudo tcpdump -c 10
```

---

# Disable Name Resolution

```bash
sudo tcpdump -n
```

Benefits:

- Faster Output
- Displays Numeric IP Addresses
- Easier Troubleshooting

---

# Display Detailed Output

```bash
sudo tcpdump -vv
```

Extra verbosity:

```bash
sudo tcpdump -vvv
```

---

# Display Packet Contents

Hexadecimal:

```bash
sudo tcpdump -X
```

ASCII + Hex:

```bash
sudo tcpdump -XX
```

---

# Save Packets to File

```bash
sudo tcpdump -w capture.pcap
```

This stores packets in **PCAP** format for later analysis.

---

# Read Saved Capture

```bash
tcpdump -r capture.pcap
```

---

# Capture Only TCP Traffic

```bash
sudo tcpdump tcp
```

---

# Capture Only UDP Traffic

```bash
sudo tcpdump udp
```

---

# Capture ICMP Packets

```bash
sudo tcpdump icmp
```

Useful when troubleshooting:

```bash
ping
```

---

# Capture ARP Traffic

```bash
sudo tcpdump arp
```

Useful for Layer 2 troubleshooting.

---

# Filter by Host

Capture traffic to or from:

```bash
sudo tcpdump host 192.168.1.100
```

---

# Filter by Source

```bash
sudo tcpdump src 192.168.1.100
```

---

# Filter by Destination

```bash
sudo tcpdump dst 192.168.1.200
```

---

# Filter by Port

Capture HTTP traffic.

```bash
sudo tcpdump port 80
```

Capture HTTPS traffic.

```bash
sudo tcpdump port 443
```

Capture SSH traffic.

```bash
sudo tcpdump port 22
```

---

# Filter by Source Port

```bash
sudo tcpdump src port 443
```

---

# Filter by Destination Port

```bash
sudo tcpdump dst port 53
```

---

# Combine Filters

Example:

```bash
sudo tcpdump tcp and port 443
```

Another example:

```bash
sudo tcpdump host 192.168.1.10 and port 22
```

---

# Boolean Operators

Supported operators:

```text
and
```

```text
or
```

```text
not
```

Example:

```bash
sudo tcpdump not port 22
```

---

# DNS Troubleshooting

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

Useful for:

- DNS Queries
- DNS Responses
- DNS Timeouts

---

# HTTP Troubleshooting

```bash
sudo tcpdump port 80
```

Inspect:

- HTTP Requests
- HTTP Responses

---

# HTTPS Troubleshooting

```bash
sudo tcpdump port 443
```

Although encrypted payloads cannot be read without appropriate decryption material, you can still analyse:

- TCP Handshake
- TLS Handshake Metadata
- Connection Resets
- Retransmissions

---

# SSH Troubleshooting

```bash
sudo tcpdump port 22
```

Useful for:

- Connection Attempts
- Failed Handshakes
- Session Establishment

---

# Enterprise Example

Web Application:

```text
User

↓

Load Balancer

↓

Web Server

↓

Database
```

Users report slow responses.

Capture:

```bash
sudo tcpdump -i eth0 host LoadBalancer-IP
```

Investigate:

- Retransmissions
- Packet Loss
- Connection Resets
- Delays

---

# Cloud Perspective

Cloud engineers use `tcpdump` to troubleshoot:

- Virtual Machines
- VPN Connectivity
- Load Balancers
- NAT Gateways
- Kubernetes Nodes
- DNS Resolution

---

# Kubernetes Perspective

Run:

```bash
sudo tcpdump -i any
```

Common interfaces:

```text
eth0

cni0

flannel.1

vxlan.calico
```

Useful for:

- Pod Communication
- Service Traffic
- DNS Issues
- Overlay Network Debugging

---

# Linux Perspective

Capture all traffic.

```bash
sudo tcpdump -i any
```

Capture DNS.

```bash
sudo tcpdump port 53
```

Capture SSH.

```bash
sudo tcpdump port 22
```

Save capture.

```bash
sudo tcpdump -w packets.pcap
```

Read capture.

```bash
tcpdump -r packets.pcap
```

---

# Common Packet Filters

| Command | Purpose |
|----------|----------|
| `tcpdump tcp` | TCP packets |
| `tcpdump udp` | UDP packets |
| `tcpdump icmp` | ICMP packets |
| `tcpdump arp` | ARP packets |
| `tcpdump port 80` | HTTP traffic |
| `tcpdump port 443` | HTTPS traffic |
| `tcpdump port 53` | DNS traffic |
| `tcpdump host IP` | Traffic for a specific host |

---

# Hands-on Lab

## Task 1

List interfaces.

```bash
tcpdump -D
```

---

## Task 2

Capture ten packets.

```bash
sudo tcpdump -c 10
```

---

## Task 3

Capture on all interfaces.

```bash
sudo tcpdump -i any
```

---

## Task 4

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

---

## Task 5

Capture HTTP traffic.

```bash
sudo tcpdump port 80
```

---

## Task 6

Save captured packets.

```bash
sudo tcpdump -w traffic.pcap
```

---

## Task 7

Read the saved capture.

```bash
tcpdump -r traffic.pcap
```

---

## Task 8

Capture SSH traffic between your workstation and a Linux server.

```bash
sudo tcpdump host SERVER_IP and port 22
```

Observe the TCP handshake and SSH session establishment.

---

# Production Troubleshooting

Problem:

```text
Application

Cannot Connect

To Database
```

Check:

```bash
sudo tcpdump host DATABASE_IP
```

↓

Packets Leaving?

↓

Packets Returning?

↓

TCP Handshake Complete?

↓

Retransmissions?

↓

RST Packets?

This packet-level visibility helps isolate network, firewall, or application issues.

---

# Common Mistakes

❌ Capturing without filters.

✅ Apply filters to reduce unnecessary traffic.

---

❌ Forgetting `sudo`.

✅ Packet capture generally requires elevated privileges.

---

❌ Leaving long captures running.

✅ Use `-c` or save to a file and stop captures promptly.

---

❌ Capturing on the wrong interface.

✅ Verify interfaces with `tcpdump -D` or `ip link`.

---

❌ Expecting HTTPS payloads to be readable.

✅ Remember that TLS encrypts application data.

---

# Best Practices

- Capture only the traffic you need.
- Use filters to reduce noise.
- Save captures in PCAP format for later analysis.
- Disable DNS resolution using `-n` during troubleshooting.
- Capture on the correct interface.
- Protect packet capture files because they may contain sensitive metadata or data.
- Remove packet capture files after investigations if they are no longer required.

---

# Interview Questions

## Beginner

1. What is `tcpdump`?
2. How do you capture packets on a specific interface?
3. How do you save captured packets?
4. What is a PCAP file?

---

## Intermediate

1. How do you filter traffic by host and port?
2. Why is `tcpdump` useful for DNS troubleshooting?
3. How do you analyse HTTPS traffic with `tcpdump`?
4. Explain the difference between capturing and reading packets.

---

## Architect Level

1. Explain how you would troubleshoot intermittent packet loss using `tcpdump`.
2. Design a packet capture strategy for a production Kubernetes cluster.
3. How would you investigate an application that experiences random connection resets?

---

# Summary

In this lesson, you learned:

- The `tcpdump` command
- Packet Capture
- Traffic Filtering
- Protocol Analysis
- PCAP Files
- DNS Troubleshooting
- HTTP and HTTPS Analysis
- Enterprise Network Diagnostics

`tcpdump` is one of the most valuable networking tools available on Linux. It allows engineers to inspect network traffic at the packet level, making it possible to troubleshoot connectivity issues, investigate performance problems, verify protocol behaviour, and support security investigations. Mastering `tcpdump` is an essential skill for production Linux, cloud, Kubernetes, and enterprise networking environments.

---

## Key Takeaways

- `tcpdump` captures **live network packets**.
- Use **`-i`** to select a network interface.
- Use **`-w`** to save packets in **PCAP** format.
- Use **`-r`** to read previously captured packets.
- Apply filters by **host**, **port**, or **protocol** to simplify analysis.
- `tcpdump` is a fundamental tool for troubleshooting DNS, TCP, HTTP, VPN, Kubernetes, and cloud networking issues.

---

## What's Next?

**[traceroute](traceroute.md)**

In the next lesson, you'll learn about **`traceroute`**.

You'll explore:

- What `traceroute` is
- How packet forwarding works
- Hop-by-Hop Path Discovery
- TTL (Time To Live)
- Network Latency Analysis
- Routing Troubleshooting
- Enterprise Connectivity Diagnostics

By the end of the lesson, you'll understand how to trace the path packets take across networks, identify routing problems, locate high-latency links, and troubleshoot connectivity issues in enterprise, cloud, and Internet environments.
