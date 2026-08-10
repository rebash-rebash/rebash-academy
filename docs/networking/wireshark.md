---
title: "Wireshark"
description: "Learn Wireshark for deep packet analysis — display filters, TCP streams, DNS/HTTP/HTTPS/TLS inspection, and production network troubleshooting."
difficulty: advanced
estimated_time: "230 min"
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
  - wireshark
  - packet-analysis
  - rebash-networking-mastery
comments: false
status: ready
---

# Wireshark — Deep Packet Analysis for Network Troubleshooting

> **Wireshark** is the world's most widely used **network protocol analyzer**. It captures, decodes, and analyzes network packets using a powerful graphical interface, allowing engineers to inspect communication at every layer of the network stack. Wireshark is used to troubleshoot **DNS failures, TCP handshake problems, HTTP/HTTPS traffic, TLS negotiations, routing issues, packet loss, latency, VoIP, cloud networking, and Kubernetes networking**. Every Network Engineer, Linux Administrator, DevOps Engineer, SRE, Cloud Architect, Security Engineer, and Kubernetes Administrator should be proficient with Wireshark.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 12: Network Troubleshooting → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Advanced</div>

<div markdown>**Reading Time:** 230 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Troubleshooting</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Wireshark
- Capture live network traffic
- Analyze network protocols
- Apply display filters
- Inspect TCP handshakes
- Analyze DNS, HTTP, HTTPS, and TLS traffic
- Troubleshoot production network issues

---

# Prerequisites

Complete:

- [Ping](ping.md)
- [traceroute](traceroute-troubleshooting.md)
- [tcpdump](tcpdump-troubleshooting.md)
- TCP/IP
- Linux Networking

Basic understanding of:

- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)
- Domain Name System (DNS)
- HTTP
- Transport Layer Security (TLS)

---

# Why Do We Need Wireshark?

Imagine an application reports:

```text
Users

Cannot

Login
```

Ping works.

Traceroute works.

tcpdump captures packets.

But you need answers like:

- Which protocol failed?
- Which packet caused the error?
- Did TLS negotiation succeed?
- Was DNS resolved correctly?
- Which HTTP response code was returned?

The answer is:

```text
Wireshark
```

---

# What is Wireshark?

Wireshark is:

```text
A

Graphical

Network

Protocol

Analyzer
```

It captures and decodes packets in a human-readable format.

---

# Packet Analysis Workflow

```text
Network Interface

↓

Packet Capture

↓

Wireshark

↓

Protocol Analysis

↓

Root Cause
```

Wireshark makes complex network traffic easy to understand.

---

# Live Packet Capture

Capture traffic from:

- Ethernet
- Wi-Fi
- Loopback
- VPN
- Docker
- Kubernetes
- Virtual Interfaces

Simply select the desired interface and start capturing.

---

# Open Packet Capture Files

Wireshark supports:

```text
.pcap

.pcapng
```

These files can be generated using:

- tcpdump
- Wireshark
- tshark
- Cloud packet capture tools

---

# Wireshark Interface

Main components:

```text
Packet List

↓

Packet Details

↓

Packet Bytes
```

Each captured packet can be inspected down to the byte level.

---

# Packet Layers

Wireshark automatically decodes:

```text
Ethernet

↓

IP

↓

TCP

↓

HTTP
```

or

```text
Ethernet

↓

IP

↓

UDP

↓

DNS
```

Each protocol layer can be expanded for detailed inspection.

---

# Display Filters

Unlike tcpdump capture filters, Wireshark primarily uses **display filters** after packets have been captured.

Examples:

Display only HTTP:

```text
http
```

Display only DNS:

```text
dns
```

Display only TCP:

```text
tcp
```

Display only ICMP:

```text
icmp
```

---

# IP Address Filters

Source IP:

```text
ip.src == 192.168.1.10
```

Destination IP:

```text
ip.dst == 10.0.0.5
```

Specific host:

```text
ip.addr == 192.168.1.20
```

---

# Port Filters

Display HTTPS traffic.

```text
tcp.port == 443
```

Display HTTP traffic.

```text
tcp.port == 80
```

Display DNS traffic.

```text
udp.port == 53
```

---

# TCP Three-Way Handshake

Wireshark clearly shows:

```text
SYN

↓

SYN-ACK

↓

ACK
```

You can verify:

- Connection Establishment
- Retransmissions
- Resets
- Delays

---

# TCP Stream Analysis

Right-click:

```text
Follow

↓

TCP Stream
```

Wireshark reconstructs the complete conversation between client and server.

Useful for:

- HTTP Requests
- API Calls
- Application Debugging

---

# DNS Analysis

Example capture:

```text
DNS Query

↓

example.com

↓

DNS Response

↓

93.184.216.34
```

Useful for troubleshooting:

- Slow DNS
- NXDOMAIN
- Timeouts
- Incorrect Records

---

# HTTP Analysis

Wireshark displays:

```text
GET /

↓

200 OK
```

or

```text
POST /login

↓

401 Unauthorized
```

Useful for:

- API Debugging
- Web Applications
- Authentication Problems

---

# HTTPS and TLS Analysis

Although encrypted application data cannot usually be read without decryption keys, Wireshark can inspect:

- TLS Handshake
- Certificate Exchange
- Cipher Suite Negotiation
- Protocol Version
- Session Establishment

Useful for diagnosing TLS failures.

---

# ICMP Analysis

Capture:

```text
Echo Request

↓

Echo Reply
```

Useful for:

- Ping Analysis
- Packet Loss
- Round Trip Time (RTT) Measurement

---

# TCP Flags

Wireshark displays:

- SYN
- ACK
- FIN
- RST
- PSH
- URG

These flags help diagnose:

- Connection Failures
- Unexpected Disconnects
- Application Errors

---

# Packet Timing

Wireshark measures:

- Packet Arrival Time
- Response Time
- TCP Retransmissions
- Connection Duration

Useful for identifying latency problems.

---

# Expert Information

Wireshark automatically highlights:

- Retransmissions
- Duplicate ACKs
- Checksum Errors
- Malformed Packets
- Out-of-Order Segments

This helps identify issues quickly.

---

# Statistics

Useful reports include:

- Protocol Hierarchy
- Conversations
- Endpoints
- IO Graphs
- Flow Graphs

These provide an overview of network behavior.

---

# Flow Graph

Visualise communication.

```text
Client

↓

Server

↓

Database
```

Shows the complete sequence of packets exchanged.

---

# Kubernetes Perspective

Analyze traffic from:

- Pods
- Services
- CoreDNS
- Ingress
- Service Mesh

Capture packets using:

```bash
tcpdump
```

Then open:

```text
capture.pcap
```

in Wireshark.

---

# Cloud Perspective

Wireshark helps troubleshoot:

- AWS EC2
- Azure Virtual Machines
- Google Compute Engine
- VPN Connections
- Hybrid Networking

Analyze captures collected from cloud instances.

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

↓

Root Cause
```

Wireshark provides the deepest protocol visibility.

---

# Common Display Filters

| Filter | Purpose |
|----------|----------|
| ip | IP Traffic |
| tcp | TCP Packets |
| udp | UDP Packets |
| dns | DNS Queries |
| http | HTTP Requests |
| tls | TLS Handshake |
| icmp | Ping Traffic |

---

# CLI Companion

Although Wireshark is graphical, its command-line counterpart is:

```bash
tshark
```

Example:

```bash
tshark -i eth0
```

Useful for servers without graphical interfaces.

---

# Hands-on Lab

## Task 1

Install Wireshark.

---

## Task 2

Capture live traffic on your primary network interface.

---

## Task 3

Open a website.

Observe:

- DNS
- TCP
- TLS
- HTTP

---

## Task 4

Apply filters:

```text
dns
```

```text
http
```

```text
tcp
```

---

## Task 5

Follow a TCP stream.

Observe the complete client-server conversation.

---

## Task 6

Capture HTTPS traffic and inspect the TLS handshake.

---

## Task 7

Capture packets with tcpdump:

```bash
sudo tcpdump -i eth0 -w capture.pcap
```

Open the file in Wireshark and analyze the protocols.

---

## Task 8

Draw the complete communication flow:

```text
Browser

↓

DNS

↓

TCP Handshake

↓

TLS Handshake

↓

HTTP Request

↓

HTTP Response
```

Identify which packets correspond to each stage.

---

# Production Troubleshooting

Problem:

```text
Application

Login

Fails
```

Check:

- DNS Resolution
- TCP Handshake
- TLS Handshake
- HTTP Status Code
- Packet Retransmissions
- Server Response
- Application Errors

Workflow:

```text
Capture Packets

↓

Filter Protocol

↓

Analyze Stream

↓

Identify Failure

↓

Resolve
```

---

# Wireshark vs tcpdump

| Wireshark | tcpdump |
|------------|----------|
| Graphical Interface | Command Line |
| Deep Protocol Decoding | Lightweight Packet Capture |
| Rich Visualization | Fast Live Capture |
| Excellent for Analysis | Excellent for Servers |
| Ideal for Offline Investigation | Ideal for Production Capture |

---

# Wireshark vs tshark

| Wireshark | tshark |
|------------|---------|
| GUI | CLI |
| Interactive Analysis | Terminal-Based Analysis |
| Best for Desktop | Best for Automation |
| Rich Graphs | Script Friendly |
| Manual Investigation | Batch Processing |

---

# Common Mistakes

❌ Capturing excessive traffic.

✅ Apply capture or display filters to reduce noise.

---

❌ Using display filters as capture filters.

✅ Understand the difference between capture and display filtering.

---

❌ Ignoring TCP retransmissions.

✅ Investigate retransmissions as indicators of packet loss or congestion.

---

❌ Focusing only on application packets.

✅ Analyze the full protocol stack from Ethernet to the application layer.

---

❌ Assuming encrypted HTTPS payloads are visible.

✅ Inspect the TLS handshake unless decryption keys are available.

---

# Best Practices

- Capture only relevant traffic.
- Save captures before making configuration changes.
- Use display filters extensively.
- Correlate packet timestamps with application logs.
- Analyze the complete protocol stack.
- Use Expert Information to identify anomalies.
- Protect packet captures containing sensitive information.
- Archive important captures for future analysis.

---

# Interview Questions

## Beginner

1. What is Wireshark?
2. What is a packet capture?
3. What is a display filter?
4. How do you follow a TCP stream?

---

## Intermediate

1. Compare Wireshark and tcpdump.
2. Explain the TCP three-way handshake using Wireshark.
3. How do you troubleshoot DNS using Wireshark?
4. How do you identify TCP retransmissions?

---

## Architect Level

1. Design a packet analysis workflow for production incidents.
2. Explain how Wireshark helps troubleshoot TLS failures.
3. How would you diagnose intermittent API latency using packet captures?

---

# Summary

In this lesson, you learned:

- Wireshark
- Packet Analysis
- Display Filters
- TCP Stream Analysis
- DNS Analysis
- HTTP Analysis
- HTTPS and TLS Analysis
- TCP Flags
- Protocol Statistics
- Production Packet Troubleshooting

Wireshark is the industry's leading protocol analyzer, providing deep visibility into every layer of network communication. By decoding packets, reconstructing conversations, and highlighting protocol anomalies, it enables engineers to diagnose complex networking issues across enterprise, cloud, container, and Kubernetes environments.

---

## Key Takeaways

- **Wireshark** is a graphical network protocol analyzer.
- It decodes packets across multiple protocol layers.
- **Display filters** help isolate relevant traffic.
- **Follow TCP Stream** reconstructs complete client-server conversations.
- Wireshark is ideal for analyzing **DNS**, **HTTP**, **HTTPS**, **TLS**, **TCP**, and **ICMP** traffic.
- Combine **tcpdump** for packet capture with **Wireshark** for detailed protocol analysis.

---

## What's Next?

**[DNS Troubleshooting](dns-troubleshooting-deep-dive.md)**

In the next lesson, you'll learn about **DNS Troubleshooting**.

You'll explore:

- Common DNS Failures
- DNS Resolution Process
- NXDOMAIN Errors
- SERVFAIL Responses
- DNS Timeouts
- DNS Tools
- Production DNS Troubleshooting

By the end of the lesson, you'll be able to diagnose and resolve DNS-related issues across Linux systems, cloud environments, and Kubernetes clusters using systematic troubleshooting techniques.
