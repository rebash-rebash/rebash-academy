---
title: "OSI Model"
description: "Master the seven layers of the OSI Model — encapsulation, protocols, devices, Linux tools, and layer-by-layer troubleshooting for Cloud and DevOps."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 1 · Networking Fundamentals"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - osi
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# OSI Model — The Seven Layers of Network Communication

> The **Open Systems Interconnection (OSI) Model** is a conceptual framework that explains how data travels from one device to another across a network. It divides network communication into **seven layers**, where each layer performs a specific function and communicates with the layers directly above and below it. Although the modern Internet primarily uses the TCP/IP model, the OSI Model remains the industry standard for learning networking, troubleshooting connectivity issues, and understanding how protocols interact. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master the OSI Model.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Networking Fundamentals</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---


# What You'll Learn

After completing this lesson, you'll be able to:

- Understand the OSI Model
- Explain all seven OSI layers
- Identify protocols operating at each layer
- Understand encapsulation and decapsulation
- Troubleshoot networking problems using the OSI Model
- Relate Linux networking tools to OSI layers

---

# Prerequisites

Complete:

- [What is Networking?](introduction-to-networking.md)
- [Types of Networks](types-of-networks.md)
- [Network Topologies](network-topologies.md)

---

# Why Learn the OSI Model?

Imagine troubleshooting a website that isn't loading.

The problem could be:

- A damaged cable
- Incorrect IP address
- Domain Name System (DNS) failure
- Firewall blocking traffic
- Secure Sockets Layer / Transport Layer Security (SSL/TLS) certificate issue
- Application crash

The OSI Model provides a structured way to isolate and troubleshoot these problems layer by layer.

---

# What is the OSI Model?

The **Open Systems Interconnection (OSI) Model** is a seven-layer reference model developed to standardise network communication.

Each layer has a specific responsibility.

```text
Application

↓

Presentation

↓

Session

↓

Transport

↓

Network

↓

Data Link

↓

Physical
```

Data travels from the top layer to the bottom layer on the sender and from the bottom layer to the top layer on the receiver.

---

# Why Seven Layers?

Separating networking into layers provides:

- Simpler troubleshooting
- Vendor independence
- Easier protocol development
- Modular network design
- Better interoperability

Each layer focuses on one specific function.

---

# OSI Layers

| Layer | Name | Primary Function |
|--------|------|------------------|
| 7 | Application | User-facing network services |
| 6 | Presentation | Data formatting, encryption, compression |
| 5 | Session | Session establishment and management |
| 4 | Transport | Reliable end-to-end communication |
| 3 | Network | Routing and IP addressing |
| 2 | Data Link | MAC addressing and frame delivery |
| 1 | Physical | Electrical, optical, and wireless transmission |

---

# Layer 7 — Application Layer

The Application Layer provides network services directly to applications used by users.

Examples:

- Web browsers
- Email clients
- File Transfer Protocol (FTP) clients
- Secure Shell (SSH) clients

Common protocols:

- Hypertext Transfer Protocol (HTTP)
- Hypertext Transfer Protocol Secure (HTTPS)
- FTP
- Simple Mail Transfer Protocol (SMTP)
- Post Office Protocol version 3 (POP3)
- Internet Message Access Protocol (IMAP)
- DNS
- SSH

---

# Example

Opening a website:

```text
Browser

↓

HTTPS

↓

Application Layer
```

This is the layer closest to the user.

---

# Layer 6 — Presentation Layer

The Presentation Layer prepares data for transmission.

Responsibilities:

- Encryption
- Decryption
- Compression
- Data translation
- Character encoding

Examples:

- SSL/TLS encryption
- JPEG images
- PNG images
- UTF-8 encoding

---

# Example

When accessing an HTTPS website:

```text
Browser

↓

TLS Encryption

↓

Presentation Layer
```

---

# Layer 5 — Session Layer

The Session Layer establishes, manages, and terminates communication sessions.

Responsibilities:

- Session establishment
- Authentication
- Synchronisation
- Session recovery

Examples:

- Remote desktop sessions
- Database connections
- Remote Procedure Call (RPC) communication

---

# Layer 4 — Transport Layer

The Transport Layer provides reliable communication between applications.

Responsibilities:

- Segmentation
- Error recovery
- Flow control
- Reliability
- Port numbers

Protocols:

- Transmission Control Protocol (TCP)
- User Datagram Protocol (UDP)

---

# TCP

Reliable communication.

Features:

- Acknowledgments
- Retransmission
- Ordered delivery
- Error detection

Used by:

- HTTPS
- SSH
- FTP
- SMTP

---

# UDP

Fast communication.

Features:

- No acknowledgments
- No retransmissions
- Lower latency

Used by:

- DNS
- Streaming
- Voice over IP (VoIP)
- Online gaming

---

# Layer 3 — Network Layer

The Network Layer moves packets between different networks.

Responsibilities:

- Routing
- IP addressing
- Path selection

Protocols:

- Internet Protocol version 4 (IPv4)
- Internet Protocol version 6 (IPv6)
- Internet Control Message Protocol (ICMP)

Devices:

- Routers
- Layer 3 Switches

---

# Example

```text
192.168.1.10

↓

Router

↓

8.8.8.8
```

The router forwards packets toward their destination.

---

# Layer 2 — Data Link Layer

The Data Link Layer provides communication between devices on the same local network.

Responsibilities:

- Media Access Control (MAC) addressing
- Frame creation
- Error detection
- Switching

Protocols:

- Ethernet
- Wi-Fi (802.11)
- Point-to-Point Protocol (PPP)

Devices:

- Switches
- Bridges

---

# Example

```text
Laptop

↓

Switch

↓

Server
```

Communication uses MAC addresses within the Local Area Network (LAN).

---

# Layer 1 — Physical Layer

The Physical Layer transmits raw bits across the communication medium.

Responsibilities:

- Electrical signals
- Fibre optics
- Radio waves
- Connectors
- Cables

Examples:

- Ethernet cables
- Fibre cables
- Wi-Fi signals

Devices:

- Network cables
- Repeaters
- Hubs
- Network interface cards (NICs)

---

# Data Flow Through the OSI Model

Sending data:

```text
Application

↓

Presentation

↓

Session

↓

Transport

↓

Network

↓

Data Link

↓

Physical

↓

Cable/Wireless
```

Receiving data:

```text
Cable/Wireless

↓

Physical

↓

Data Link

↓

Network

↓

Transport

↓

Session

↓

Presentation

↓

Application
```

---

# Encapsulation

As data moves down the OSI layers, each layer adds its own header.

```text
Application Data

↓

Segment

↓

Packet

↓

Frame

↓

Bits
```

This process is called **Encapsulation**.

---

# Decapsulation

When data reaches the destination, each layer removes its corresponding header.

```text
Bits

↓

Frame

↓

Packet

↓

Segment

↓

Application Data
```

This process is called **Decapsulation**.

---

# Protocols by Layer

| Layer | Common Protocols |
|--------|------------------|
| Application | HTTP, HTTPS, FTP, DNS, SSH, SMTP |
| Presentation | TLS, SSL, JPEG, PNG |
| Session | RPC, NetBIOS |
| Transport | TCP, UDP |
| Network | IPv4, IPv6, ICMP |
| Data Link | Ethernet, Wi-Fi, PPP |
| Physical | Ethernet Cable, Fiber, Radio |

---

# Devices by Layer

| Layer | Devices |
|--------|----------|
| Application | Web Servers |
| Presentation | SSL/TLS Gateways |
| Session | Session Managers |
| Transport | Firewalls, Load Balancers |
| Network | Routers |
| Data Link | Switches |
| Physical | Cables, Hubs, NICs |

---

# OSI Troubleshooting Example

A website is unreachable.

Possible troubleshooting sequence:

| Layer | Investigation |
|--------|---------------|
| 7 | Is the web application running? |
| 6 | Is the TLS certificate valid? |
| 5 | Is the session established? |
| 4 | Is TCP port 443 open? |
| 3 | Can the server be reached via IP? |
| 2 | Is the switch forwarding traffic? |
| 1 | Is the network cable connected? |

The OSI Model helps isolate the problem systematically.

---

# Linux Commands by OSI Layer

| Layer | Linux Command |
|--------|---------------|
| 7 | `curl`, `wget` |
| 6 | `openssl` |
| 5 | `ssh` |
| 4 | `ss`, `netstat` |
| 3 | `ping`, `ip route` |
| 2 | `ip link`, `arp` |
| 1 | `ethtool` |

---

# Memory Aid

Many engineers remember the layers using:

```text
7  Application

6  Presentation

5  Session

4  Transport

3  Network

2  Data Link

1  Physical
```

Mnemonic (Top to Bottom):

> **All People Seem To Need Data Processing**

Mnemonic (Bottom to Top):

> **Please Do Not Throw Sausage Pizza Away**

Use whichever is easier for you to remember.

---

# Production Perspective

Cloud platforms, Kubernetes, enterprise data centres, and Internet applications rely on all seven OSI concepts.

Examples:

- HTTPS → Layer 7
- TLS → Layer 6
- TCP → Layer 4
- IP Routing → Layer 3
- Ethernet Switching → Layer 2
- Fibre Optics → Layer 1

Although engineers may not explicitly reference the OSI Model every day, it remains invaluable for troubleshooting.

---

# Hands-on Lab

## Task 1

Display IP addresses.

```bash
ip addr
```

---

## Task 2

Display routing table.

```bash
ip route
```

---

## Task 3

Test connectivity.

```bash
ping google.com
```

---

## Task 4

Display listening ports.

```bash
ss -tuln
```

---

## Task 5

Retrieve a webpage.

```bash
curl https://example.com
```

---

## Task 6

View Ethernet interface details.

```bash
ethtool eth0
```

---

## Task 7

Use `openssl` to inspect a website's TLS certificate.

```bash
openssl s_client -connect example.com:443
```

---

## Task 8

Choose a network issue (for example, "cannot access a website") and identify which OSI layer or layers you would investigate first. Explain your reasoning.

---

# Common Mistakes

❌ Memorising layers without understanding their purpose.

✅ Learn what each layer actually does.

---

❌ Confusing IP and MAC addresses.

✅ IP belongs to Layer 3; MAC belongs to Layer 2.

---

❌ Assuming the OSI Model is a real protocol stack.

✅ It is a conceptual reference model.

---

❌ Ignoring lower layers during troubleshooting.

✅ Always troubleshoot from the most likely layer.

---

❌ Believing every protocol maps perfectly to one layer.

✅ Some protocols interact with multiple layers.

---

# Best Practices

- Learn the responsibilities of each layer.
- Use the OSI Model as a troubleshooting framework.
- Associate common protocols with their layers.
- Practice identifying the layer where failures occur.
- Understand how data is encapsulated and decapsulated.

---

# Interview Questions

## Beginner

1. What is the OSI Model?
2. How many layers does it have?
3. Which layer handles IP addressing?
4. Which layer handles MAC addresses?

---

## Intermediate

1. Explain encapsulation and decapsulation.
2. Compare TCP and UDP in the Transport Layer.
3. Which devices operate at Layer 2 and Layer 3?
4. How would you troubleshoot a website using the OSI Model?

---

## Architect Level

1. Why is the OSI Model still relevant in cloud-native environments?
2. How does the OSI Model assist in production incident response?
3. Explain how Kubernetes networking relates to multiple OSI layers.

---

# Summary

In this lesson, you learned:

- The purpose of the OSI Model
- The seven OSI layers
- Responsibilities of each layer
- Common protocols and devices
- Encapsulation and decapsulation
- Troubleshooting using the OSI Model

The OSI Model provides a structured way to understand and troubleshoot network communication. While modern networks primarily implement the TCP/IP protocol suite, the OSI Model remains one of the most valuable conceptual tools for designing, operating, and troubleshooting enterprise networks.

---

## Key Takeaways

- The OSI Model has seven layers.
- Each layer performs a specific networking function.
- Data is encapsulated before transmission and decapsulated at the destination.
- Different protocols and devices operate at different layers.
- The OSI Model is widely used as a troubleshooting framework.

---

## What's Next?

**[TCP/IP Model](tcp-ip-model.md)**
