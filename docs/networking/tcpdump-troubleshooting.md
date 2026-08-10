---
title: "tcpdump"
description: "Learn tcpdump for real-time packet capture — filters, TCP handshake analysis, DNS/HTTP/HTTPS inspection, and troubleshooting in Linux, cloud, and Kubernetes."
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
  - tcpdump
  - packet-capture
  - rebash-networking-mastery
comments: false
status: ready
---

# tcpdump — Capturing and Analyzing Network Packets in Real Time

> **tcpdump** is a command-line packet analyzer used to **capture, inspect, and analyze network traffic** directly from a network interface. It allows administrators to observe every packet entering or leaving a system, making it one of the most powerful tools for diagnosing **network connectivity issues, DNS failures, TCP handshake problems, HTTP requests, TLS communication, routing issues, packet loss, and Kubernetes networking problems**. Every Linux Administrator, Network Engineer, DevOps Engineer, SRE, Cloud Architect, Security Engineer, and Kubernetes Administrator should master tcpdump.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 3</p>

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

<div markdown>**Lesson:** 3 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand packet capturing
- Capture network traffic using tcpdump
- Apply capture filters
- Analyze TCP handshakes
- Inspect DNS, HTTP, and HTTPS traffic
- Troubleshoot production networking issues
- Capture packets in cloud and Kubernetes environments

---

# Prerequisites

Complete:

- [Ping](ping.md)
- [traceroute](traceroute-troubleshooting.md)
- TCP/IP
- Linux Networking
- Routing

Basic understanding of:

- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)
- Internet Control Message Protocol (ICMP)
- Domain Name System (DNS)
- HTTP

---

# Why Do We Need tcpdump?

Imagine an application reports:

```text
Connection

Timeout
```

Ping works.

Traceroute works.

But:

- Is the packet leaving the server?
- Is the response returning?
- Is DNS working?
- Is TLS failing?
- Is TCP completing the handshake?

The answer is:

```bash
tcpdump
```

---

# What is tcpdump?

tcpdump is:

```text
A

Packet

Capture

And

Analysis

Tool
```

It captures packets directly from a network interface.

---

# Packet Capture Workflow

```text
Application

↓

Network Interface

↓

tcpdump

↓

Packet Analysis
```

tcpdump observes packets before applications process them.

---

# Where tcpdump Works

tcpdump can capture traffic from:

- Ethernet
- Wi-Fi
- Loopback
- Virtual Interfaces
- Docker Networks
- Kubernetes Nodes
- VPN Interfaces

---

# List Network Interfaces

Display available interfaces.

```bash
tcpdump -D
```

Example:

```text
eth0

lo

docker0

cni0
```

---

# Capture All Traffic

Capture packets on:

```text
eth0
```

```bash
sudo tcpdump -i eth0
```

Packets appear in real time.

---

# Capture Limited Packets

Capture only ten packets.

```bash
sudo tcpdump -i eth0 -c 10
```

Useful during quick troubleshooting sessions.

---

# Disable Name Resolution

Avoid DNS lookups.

```bash
sudo tcpdump -n
```

Advantages:

- Faster Output
- Raw IP Addresses
- Easier Troubleshooting

---

# Verbose Output

Increase details.

```bash
sudo tcpdump -vv
```

or

```bash
sudo tcpdump -vvv
```

Displays:

- Time To Live (TTL)
- Window Size
- TCP Options
- Flags

---

# Save Packets

Write captures to a file.

```bash
sudo tcpdump -i eth0 -w capture.pcap
```

The file can later be opened in:

- Wireshark
- tcpdump

---

# Read Saved Packets

```bash
tcpdump -r capture.pcap
```

Analyze previously captured traffic.

---

# Packet Flow

```text
Client

↓

Switch

↓

Router

↓

Server

↓

Network Interface

↓

tcpdump
```

tcpdump records every packet that reaches the selected interface.

---

# Capture Filters

Capture only traffic matching specific conditions.

Examples:

Host:

```bash
tcpdump host 192.168.1.10
```

Source Host:

```bash
tcpdump src host 192.168.1.10
```

Destination Host:

```bash
tcpdump dst host 192.168.1.20
```

---

# Port Filters

Capture traffic on port:

```bash
sudo tcpdump port 80
```

Specific destination port:

```bash
sudo tcpdump dst port 443
```

Multiple ports:

```bash
sudo tcpdump 'port 80 or port 443'
```

---

# Protocol Filters

Capture ICMP.

```bash
sudo tcpdump icmp
```

Capture TCP.

```bash
sudo tcpdump tcp
```

Capture UDP.

```bash
sudo tcpdump udp
```

---

# Network Filters

Capture an entire subnet.

```bash
sudo tcpdump net 192.168.1.0/24
```

Useful for analyzing traffic across multiple hosts.

---

# Boolean Filters

Example:

```bash
sudo tcpdump 'tcp and port 443'
```

Example:

```bash
sudo tcpdump 'host 10.0.0.5 and port 53'
```

Filters can combine:

- and
- or
- not

---

# TCP Three-Way Handshake

Capture:

```text
SYN

↓

SYN-ACK

↓

ACK
```

tcpdump allows you to verify whether the TCP connection completes successfully.

---

# Example TCP Output

```text
SYN

↓

SYN-ACK

↓

ACK

↓

HTTP GET
```

A successful handshake indicates the TCP session is established.

---

# DNS Troubleshooting

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

Observe:

- DNS Query
- DNS Response

Useful when applications cannot resolve hostnames.

---

# HTTP Troubleshooting

Capture HTTP.

```bash
sudo tcpdump port 80
```

View:

- HTTP Requests
- HTTP Responses

---

# HTTPS Troubleshooting

Capture encrypted traffic.

```bash
sudo tcpdump port 443
```

Although payloads are encrypted, you can still inspect:

- TCP Handshake
- TLS Handshake
- Packet Sizes
- Retransmissions

---

# ICMP Troubleshooting

Capture Ping packets.

```bash
sudo tcpdump icmp
```

Observe:

```text
Echo Request

↓

Echo Reply
```

Useful for validating connectivity.

---

# Kubernetes Perspective

Capture packets on a Kubernetes node.

```bash
sudo tcpdump -i cni0
```

Capture Pod traffic.

```bash
sudo tcpdump -i any
```

Useful for:

- Container Network Interface (CNI) Debugging
- Service Issues
- Network Policies
- DNS Resolution

---

# Docker Perspective

Capture Docker bridge traffic.

```bash
sudo tcpdump -i docker0
```

Useful for container networking analysis.

---

# Cloud Perspective

Capture traffic on:

- AWS EC2
- Azure VM
- Google Compute Engine

Common use cases:

- Security Group Validation
- Firewall Troubleshooting
- VPN Diagnostics

---

# Enterprise Troubleshooting Workflow

```text
Ping

↓

traceroute

↓

tcpdump

↓

Wireshark
```

Each tool provides progressively deeper visibility.

---

# Common TCP Flags

| Flag | Meaning |
|------|----------|
| SYN | Start Connection |
| ACK | Acknowledgement |
| FIN | Close Connection |
| RST | Reset Connection |
| PSH | Push Data |
| URG | Urgent Data |

---

# CLI Examples

Capture on interface.

```bash
sudo tcpdump -i eth0
```

Capture ten packets.

```bash
sudo tcpdump -c 10
```

Capture DNS traffic.

```bash
sudo tcpdump port 53
```

Capture HTTPS traffic.

```bash
sudo tcpdump port 443
```

Save capture.

```bash
sudo tcpdump -w traffic.pcap
```

Read capture.

```bash
tcpdump -r traffic.pcap
```

---

# Hands-on Lab

## Task 1

List network interfaces.

```bash
tcpdump -D
```

---

## Task 2

Capture ten packets.

```bash
sudo tcpdump -i eth0 -c 10
```

---

## Task 3

Ping another host while running:

```bash
sudo tcpdump icmp
```

Observe:

- Echo Request
- Echo Reply

---

## Task 4

Capture DNS queries.

```bash
sudo tcpdump port 53
```

Run:

```bash
nslookup example.com
```

Observe the request and response.

---

## Task 5

Capture HTTPS traffic.

```bash
sudo tcpdump port 443
```

Browse a secure website and observe the TCP and TLS handshakes.

---

## Task 6

Save a packet capture.

```bash
sudo tcpdump -i eth0 -w network.pcap
```

Open the file later in Wireshark.

---

## Task 7

Capture traffic on a Kubernetes node while accessing a ClusterIP Service.

---

## Task 8

Draw the packet journey:

```text
Browser

↓

TCP Handshake

↓

HTTP Request

↓

Server

↓

HTTP Response
```

Explain what tcpdump captures at every stage.

---

# Production Troubleshooting

Problem:

```text
Application

Cannot

Connect
```

Check:

- DNS Query
- TCP SYN
- SYN-ACK
- ACK
- TLS Handshake
- HTTP Request
- Firewall
- Packet Loss

Workflow:

```text
Application

↓

Packet Capture

↓

TCP Handshake

↓

Protocol Analysis

↓

Root Cause
```

---

# tcpdump vs Wireshark

| tcpdump | Wireshark |
|----------|-----------|
| Command Line | Graphical Interface |
| Lightweight | Rich Visualization |
| Live Capture | Live & Offline Analysis |
| Ideal for Servers | Ideal for Desktop Analysis |
| Low Resource Usage | Higher Resource Usage |

---

# Common Mistakes

❌ Capturing all traffic without filters.

✅ Apply capture filters to reduce unnecessary data.

---

❌ Forgetting `-n`.

✅ Disable DNS resolution for faster and clearer output.

---

❌ Capturing on the wrong interface.

✅ Verify the correct interface using `tcpdump -D`.

---

❌ Ignoring packet timestamps.

✅ Use timestamps to correlate events with application logs.

---

❌ Leaving long-running captures active.

✅ Limit packet count or duration to avoid large capture files.

---

# Best Practices

- Capture only the traffic you need.
- Always identify the correct interface before capturing.
- Save important captures as `.pcap` files.
- Use filters to minimize noise.
- Combine tcpdump with application logs.
- Analyze complex captures using Wireshark.
- Remove sensitive packet captures after analysis.
- Be aware of privacy and security requirements when capturing production traffic.

---

# Interview Questions

## Beginner

1. What is tcpdump?
2. What is a packet capture?
3. How do you capture packets on an interface?
4. What is a `.pcap` file?

---

## Intermediate

1. Explain the TCP three-way handshake using tcpdump.
2. How do you capture only DNS traffic?
3. Compare tcpdump and Wireshark.
4. How would you troubleshoot a failed HTTPS connection?

---

## Architect Level

1. Design a packet capture strategy for a production Kubernetes cluster.
2. Explain how tcpdump helps diagnose intermittent network failures.
3. How would you troubleshoot application connectivity across cloud regions using packet captures?

---

# Summary

In this lesson, you learned:

- tcpdump
- Packet Capture
- Capture Filters
- TCP Three-Way Handshake
- DNS Analysis
- HTTP Analysis
- HTTPS Analysis
- ICMP Analysis
- Kubernetes Packet Capture
- Production Network Troubleshooting

tcpdump is one of the most powerful command-line tools for network troubleshooting. It provides direct visibility into packets flowing across network interfaces, allowing engineers to diagnose connectivity issues, routing problems, protocol failures, and application communication with precision. It is an essential skill for Linux, cloud, networking, and Kubernetes professionals.

---

## Key Takeaways

- **tcpdump** captures packets directly from network interfaces.
- Use **capture filters** to focus on relevant traffic.
- Verify the **TCP three-way handshake** when troubleshooting connection issues.
- Capture **DNS**, **HTTP**, **HTTPS**, and **ICMP** traffic for protocol-specific analysis.
- Save captures as **`.pcap`** files for later analysis in Wireshark.
- Combine tcpdump with Ping, traceroute, and application logs for systematic troubleshooting.

---

## What's Next?

**[Wireshark](wireshark.md)**

In the next lesson, you'll learn about **Wireshark**.

You'll explore:

- Packet Analysis
- Protocol Decoding
- Display Filters
- TCP Stream Analysis
- DNS Analysis
- HTTP and HTTPS Inspection
- Production Packet Investigation

By the end of the lesson, you'll be able to analyse packet captures visually, inspect network protocols in depth, and diagnose complex networking issues using one of the industry's most powerful protocol analyzers.
