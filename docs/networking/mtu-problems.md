---
title: "MTU Problems"
description: "Learn MTU troubleshooting — fragmentation, Path MTU Discovery (PMTUD), black holes, VPN and Kubernetes overlay MTU, and packet analysis."
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
  - mtu
  - pmtud
  - rebash-networking-mastery
comments: false
status: ready
---

# MTU Problems — Diagnosing Fragmentation and Packet Size Issues

> **MTU (Maximum Transmission Unit)** defines the **largest packet size** that can be transmitted over a network interface without fragmentation. Incorrect MTU settings can cause **packet fragmentation, application timeouts, VPN failures, slow network performance, Kubernetes connectivity issues, TLS handshake failures, and "black-hole" connections**. Understanding MTU is essential for troubleshooting modern enterprise, cloud, container, and hybrid networking environments. Every Network Engineer, Linux Administrator, DevOps Engineer, SRE, Cloud Architect, and Kubernetes Administrator should understand MTU troubleshooting.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 7</p>

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

<div markdown>**Lesson:** 7 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand MTU
- Learn IP fragmentation
- Diagnose MTU mismatches
- Understand Path MTU Discovery (PMTUD)
- Troubleshoot VPN and cloud MTU issues
- Analyze fragmentation problems
- Optimize MTU in production environments

---

# Prerequisites

Complete:

- IPv4
- TCP/IP
- Routing
- [Ping](ping.md)
- [tcpdump](tcpdump-troubleshooting.md)

Basic understanding of:

- Ethernet
- IP Packets
- Transmission Control Protocol (TCP)

---

# Why Do MTU Problems Occur?

Imagine users report:

```text
Website

Loads

Partially
```

or

```text
SSH

Disconnects

Randomly
```

or

```text
VPN

Works

Intermittently
```

Possible causes:

- MTU Mismatch
- Packet Fragmentation
- PMTUD Failure
- Firewall Blocking ICMP
- VPN Overhead

---

# What is MTU?

MTU stands for:

```text
Maximum

Transmission

Unit
```

It defines:

```text
Largest

Packet

Size

Sent

Without

Fragmentation
```

---

# Ethernet MTU

Standard Ethernet MTU:

```text
1500 Bytes
```

This is the default value on most networks.

---

# Jumbo Frames

Some data centres use:

```text
9000 Bytes
```

Benefits:

- Lower CPU Usage
- Higher Throughput
- Better Storage Performance

Common for:

- Storage Area Network (SAN)
- Network-Attached Storage (NAS)
- High-Speed Networks

---

# Packet Flow

```text
Application

↓

TCP

↓

IP

↓

Ethernet

↓

Network
```

The packet must fit within the MTU of every link along the path.

---

# Packet Fits

Example:

```text
Packet

1400 Bytes
```

MTU:

```text
1500 Bytes
```

Result:

```text
Packet

Sent

Successfully
```

---

# Packet Too Large

Example:

```text
Packet

2000 Bytes
```

MTU:

```text
1500 Bytes
```

Result:

```text
Fragment

Packet
```

or

```text
Drop

Packet
```

depending on configuration.

---

# IP Fragmentation

Large packets may be divided into:

```text
Packet

↓

Fragment 1
```

```text
↓

Fragment 2
```

The receiving host reassembles the fragments.

---

# Problems with Fragmentation

Fragmentation causes:

- Increased CPU Usage
- More Packets
- Reduced Performance
- Higher Packet Loss Risk
- Slower Applications

Modern networks generally try to avoid fragmentation.

---

# Don't Fragment (DF) Bit

IPv4 packets may include:

```text
DF

Bit
```

If set:

```text
Packet

Cannot

Be

Fragmented
```

If the packet exceeds the MTU:

```text
Packet

Dropped
```

An ICMP message should be returned indicating that fragmentation is needed.

---

# Path MTU Discovery (PMTUD)

PMTUD automatically determines the smallest MTU along the network path.

Workflow:

```text
Large Packet

↓

DF Bit Set

↓

Router

↓

ICMP

Fragmentation Needed

↓

Reduce Packet Size

↓

Success
```

Applications then transmit packets using the discovered MTU.

---

# PMTUD Failure

Sometimes firewalls block ICMP.

Result:

```text
Large Packet

↓

Dropped

↓

No ICMP

↓

Application

Timeout
```

This is called an:

```text
MTU

Black Hole
```

---

# MTU Black Hole

Symptoms:

- HTTPS Fails
- SSH Freezes
- VPN Disconnects
- Large File Transfers Fail
- Small Packets Work

These issues are often difficult to diagnose.

---

# VPN MTU Problems

VPN encapsulation adds extra headers.

Example:

```text
Original Packet

1500 Bytes
```

↓

VPN Header

↓

```text
1540 Bytes
```

If the tunnel MTU is smaller:

```text
Packet

Dropped
```

The tunnel MTU must account for encapsulation overhead.

---

# Kubernetes MTU

Container networking introduces additional encapsulation.

Examples:

- VXLAN
- Geneve
- Generic Routing Encapsulation (GRE)

Effective MTU becomes smaller.

Typical values:

```text
1450

or

1440
```

depending on the Container Network Interface (CNI) plugin and encapsulation method.

---

# Cloud MTU

Cloud providers typically use:

```text
1500 Bytes
```

Some services support:

```text
9001 Bytes
```

Always verify:

- VPC/VNet MTU
- VPN MTU
- Overlay Network MTU

---

# Check MTU

Linux:

```bash
ip link show
```

Example:

```text
mtu 1500
```

---

# Change MTU

Temporary change:

```bash
sudo ip link set eth0 mtu 1400
```

Verify:

```bash
ip link show eth0
```

---

# Test MTU with Ping

Linux:

```bash
ping -M do -s 1472 8.8.8.8
```

1472 bytes + 28-byte IP/ICMP headers = 1500 bytes.

If the packet succeeds:

```text
MTU

Supports

1500 Bytes
```

If it fails:

Reduce the payload size until it succeeds.

---

# Windows MTU Test

```powershell
ping -f -l 1472 8.8.8.8
```

- `-f` sets the Don't Fragment flag.
- `-l` specifies the payload size.

---

# Detect Fragmentation

Capture packets.

```bash
sudo tcpdump
```

Look for:

- Fragmented IP Packets
- ICMP "Fragmentation Needed"
- Retransmissions

---

# Wireshark Analysis

Look for:

- Fragmented Packets
- ICMP Type 3 Code 4
- Retransmissions
- TCP Timeouts

Useful filters:

```text
ip.flags.mf == 1
```

or

```text
icmp
```

---

# Kubernetes Perspective

Verify:

- Pod MTU
- CNI MTU
- Overlay Network MTU
- VXLAN Configuration

Example:

```bash
ip link
```

inside a Pod or node.

---

# Enterprise Troubleshooting Workflow

```text
Ping

↓

PMTUD

↓

MTU Test

↓

tcpdump

↓

Wireshark

↓

Root Cause
```

---

# Common MTU Values

| Network | Typical MTU |
|-----------|------------:|
| Ethernet | 1500 |
| Jumbo Frame | 9000 |
| VXLAN Overlay | 1450 |
| GRE Tunnel | ~1476 |
| IPsec VPN | ~1400–1438 |
| WireGuard VPN | ~1420 |

> Exact values vary depending on encapsulation overhead and implementation.

---

# CLI Examples

View MTU.

```bash
ip link show
```

Change MTU.

```bash
sudo ip link set eth0 mtu 1450
```

Test MTU.

```bash
ping -M do -s 1472 8.8.8.8
```

Capture fragmented packets.

```bash
sudo tcpdump
```

---

# Hands-on Lab

## Task 1

View the MTU of all interfaces.

```bash
ip link show
```

---

## Task 2

Determine the largest packet that can be sent without fragmentation.

```bash
ping -M do -s 1472 8.8.8.8
```

Reduce the payload size until the test succeeds.

---

## Task 3

Temporarily change the MTU.

```bash
sudo ip link set eth0 mtu 1450
```

Test connectivity again.

---

## Task 4

Capture packets during an MTU test.

```bash
sudo tcpdump
```

Observe fragmentation behavior.

---

## Task 5

Open the packet capture in Wireshark.

Identify:

- Fragmented Packets
- ICMP Fragmentation Needed Messages
- Retransmissions

---

## Task 6

Deploy a VPN tunnel in a lab and identify the optimal MTU.

---

## Task 7

Inspect the MTU configuration used by your Kubernetes CNI plugin.

---

## Task 8

Draw the packet flow:

```text
Application

↓

TCP

↓

IP

↓

Ethernet

↓

Router

↓

Destination
```

Explain what happens when the packet exceeds the MTU of one router along the path.

---

# Production Troubleshooting

Problem:

```text
HTTPS

Fails

Only

For

Large

Requests
```

Check:

- MTU
- PMTUD
- ICMP
- VPN
- Fragmentation
- Overlay Network
- Firewall
- Packet Capture

Workflow:

```text
Ping

↓

MTU Test

↓

tcpdump

↓

Wireshark

↓

Adjust MTU

↓

Verify
```

---

# Fragmentation vs PMTUD

| Fragmentation | PMTUD |
|---------------|-------|
| Splits Large Packets | Finds the Best MTU |
| Higher Overhead | Optimized Packet Size |
| Less Efficient | Better Performance |
| Legacy Approach | Preferred Modern Approach |
| Can Increase Packet Loss | Reduces Fragmentation |

---

# MTU Problems vs Routing Issues

| MTU Problem | Routing Issue |
|--------------|---------------|
| Large Packets Fail | All Traffic May Fail |
| Fragmentation | Missing Route |
| PMTUD Failure | Routing Loop |
| Black-Hole Connections | Destination Unreachable |
| Packet Size Issue | Path Selection Issue |

---

# Common Mistakes

❌ Assuming MTU is always 1500.

✅ Verify MTU on every network segment.

---

❌ Blocking ICMP.

✅ Allow PMTUD-related ICMP messages.

---

❌ Ignoring VPN overhead.

✅ Reduce tunnel MTU appropriately.

---

❌ Using Jumbo Frames on unsupported devices.

✅ Ensure end-to-end Jumbo Frame support.

---

❌ Overlooking CNI MTU settings.

✅ Verify overlay network MTU in Kubernetes.

---

# Best Practices

- Keep MTU consistent across connected networks where possible.
- Allow ICMP messages required for PMTUD.
- Avoid unnecessary fragmentation.
- Validate MTU after VPN deployment.
- Test MTU after cloud network changes.
- Configure overlay networks with appropriate MTU values.
- Monitor retransmissions and fragmentation.
- Document MTU settings for production environments.

---

# Interview Questions

## Beginner

1. What is MTU?
2. What is the default Ethernet MTU?
3. What is fragmentation?
4. What is the DF bit?

---

## Intermediate

1. Explain Path MTU Discovery.
2. What is an MTU black hole?
3. How do VPNs affect MTU?
4. How do you identify MTU problems?

---

## Architect Level

1. Design an MTU troubleshooting workflow for a hybrid cloud environment.
2. Explain why Kubernetes overlay networks require smaller MTU values.
3. How would you troubleshoot intermittent HTTPS failures caused by MTU mismatches?

---

# Summary

In this lesson, you learned:

- MTU
- Maximum Transmission Unit
- IP Fragmentation
- Path MTU Discovery (PMTUD)
- MTU Black Holes
- VPN MTU
- Kubernetes MTU
- Packet Fragmentation Analysis
- Production MTU Troubleshooting

MTU configuration plays a critical role in network reliability and performance. Incorrect MTU values can cause subtle and difficult-to-diagnose issues such as intermittent application failures, VPN instability, and fragmented traffic. By understanding PMTUD, fragmentation, and packet capture analysis, engineers can efficiently diagnose and resolve MTU-related problems across enterprise, cloud, and Kubernetes environments.

---

## Key Takeaways

- **MTU** defines the largest packet that can traverse a network without fragmentation.
- The standard Ethernet MTU is **1500 bytes**.
- **PMTUD** helps determine the optimal packet size for a path.
- Blocking ICMP can cause **MTU black-hole** issues.
- VPNs and overlay networks reduce the effective MTU because of encapsulation.
- Use **Ping**, **tcpdump**, and **Wireshark** together to diagnose MTU-related problems.

---

## What's Next?

**[Latency](latency.md)**

In the next lesson, you'll learn about **Latency**.

You'll explore:

- Network Latency
- Round Trip Time (RTT)
- Jitter
- Throughput
- Bandwidth vs Latency
- Latency Measurement
- Production Performance Troubleshooting

By the end of the lesson, you'll understand how to measure, analyse, and reduce latency across enterprise networks, cloud platforms, and Kubernetes environments.
