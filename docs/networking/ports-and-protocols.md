---
title: "Ports and Protocols"
description: "Learn network ports and protocols — well-known ports, TCP vs UDP, HTTPS, SSH, DNS, sockets, and how to audit listening services on Linux."
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
  - ports
  - protocols
  - tcp
  - udp
  - fundamentals
  - rebash-networking-mastery
comments: false
status: ready
---

# Ports & Protocols — How Applications Communicate Over Networks

> While an **IP Address** identifies a device on a network, it doesn't identify which application should receive incoming data. A single server may simultaneously host a website, database, SSH service, email server, and DNS server—all using the same IP address. **Ports** solve this problem by directing traffic to the correct application, while **Protocols** define the rules for communication. Understanding ports and protocols is fundamental for Linux administrators, DevOps engineers, Cloud Architects, Platform Engineers, Site Reliability Engineers (SREs), Security Engineers, and Network Engineers.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 1: Networking Fundamentals → Lesson 9</p>

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

<div markdown>**Lesson:** 9 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand network ports
- Explain networking protocols
- Differentiate TCP and UDP ports
- Identify common well-known ports
- Understand secure and insecure protocols
- Troubleshoot port-related issues
- View open ports on Linux

---

# Prerequisites

Complete:

- [What is Networking?](introduction-to-networking.md)
- [Types of Networks](types-of-networks.md)
- [Network Topologies](network-topologies.md)
- [OSI Model](osi-model.md)
- [TCP/IP Model](tcp-ip-model.md)
- [Data Encapsulation](data-encapsulation.md)
- [MAC Address](mac-address.md)
- [IP Address](ip-addressing.md)

---

# Why Learn Ports & Protocols?

Suppose a server has the IP address:

```text
192.168.1.100
```

It hosts:

- Website
- Secure Shell (SSH)
- MySQL Database
- Domain Name System (DNS) Server

How does the operating system know which application should receive incoming data?

The answer is:

**Ports**

---

# What is a Port?

A **Port** is a logical communication endpoint used by applications.

Think of an IP address as an apartment building.

Think of ports as apartment numbers.

Example:

```text
Apartment Building

↓

192.168.1.100

↓

Apartment 22

↓

SSH Server
```

Without ports, every application would receive every packet.

---

# IP Address vs Port

| IP Address | Port |
|-------------|------|
| Identifies Device | Identifies Application |
| Layer 3 | Layer 4 |
| Example: 192.168.1.10 | Example: 22 |

Together:

```text
192.168.1.10:22
```

This uniquely identifies the SSH service running on that device.

---

# Port Number Range

Ports range from:

```text
0 – 65535
```

They are divided into three categories.

---

# Well-Known Ports

Range:

```text
0 – 1023
```

Reserved for standard services.

Examples:

- Hypertext Transfer Protocol (HTTP)
- Hypertext Transfer Protocol Secure (HTTPS)
- SSH
- File Transfer Protocol (FTP)
- DNS

---

# Registered Ports

Range:

```text
1024 – 49151
```

Used by registered applications.

Examples:

- Microsoft SQL Server
- Kubernetes API
- Docker APIs

---

# Dynamic (Ephemeral) Ports

Range:

```text
49152 – 65535
```

Assigned temporarily by the operating system.

Used for:

- Client connections
- Temporary communication
- Outbound requests

---

# Common Port Numbers

| Port | Protocol | Service |
|------|----------|---------|
| 20 | TCP | FTP Data |
| 21 | TCP | FTP Control |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 67 | UDP | DHCP Server |
| 68 | UDP | DHCP Client |
| 69 | UDP | TFTP |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 123 | UDP | NTP |
| 143 | TCP | IMAP |
| 161 | UDP | SNMP |
| 389 | TCP/UDP | LDAP |
| 443 | TCP | HTTPS |
| 445 | TCP | SMB |
| 465 | TCP | SMTPS |
| 514 | UDP | Syslog |
| 587 | TCP | SMTP Submission |
| 636 | TCP | LDAPS |
| 993 | TCP | IMAPS |
| 995 | TCP | POP3S |
| 1433 | TCP | Microsoft SQL Server |
| 1521 | TCP | Oracle Database |
| 2049 | TCP | NFS |
| 2379 | TCP | etcd |
| 3306 | TCP | MySQL |
| 3389 | TCP | RDP |
| 5432 | TCP | PostgreSQL |
| 5672 | TCP | RabbitMQ |
| 6379 | TCP | Redis |
| 6443 | TCP | Kubernetes API Server |
| 8080 | TCP | Alternative HTTP |
| 8443 | TCP | Alternative HTTPS |
| 9090 | TCP | Prometheus |
| 9092 | TCP | Apache Kafka |
| 9200 | TCP | Elasticsearch |
| 9418 | TCP | Git |

---

# What is a Protocol?

A **Protocol** is a set of rules that defines how devices communicate.

Protocols determine:

- Data format
- Error handling
- Authentication
- Transmission rules

Without protocols, devices would not understand each other.

---

# Real-Life Analogy

Imagine two people speaking different languages.

Without a common language:

Communication fails.

Protocols are the "language" computers use.

---

# Common Network Protocols

| Protocol | Purpose |
|----------|----------|
| HTTP | Web Browsing |
| HTTPS | Secure Web Browsing |
| DNS | Name Resolution |
| DHCP | Automatic IP Assignment |
| FTP | File Transfer |
| SSH | Secure Remote Access |
| SMTP | Email Sending |
| POP3 | Email Retrieval |
| IMAP | Email Synchronization |
| NTP | Time Synchronization |
| LDAP | Directory Services |
| SNMP | Network Monitoring |

---

# HTTP

HyperText Transfer Protocol

Port:

```text
80
```

Used for:

- Websites
- Application Programming Interfaces (APIs)
- Web Applications

Not encrypted.

---

# HTTPS

HyperText Transfer Protocol Secure

Port:

```text
443
```

Uses Transport Layer Security (TLS) encryption.

Recommended for all web applications.

---

# SSH

Secure Shell

Port:

```text
22
```

Used for:

- Remote server administration
- Secure file transfers
- Automation

Widely used by Linux administrators.

---

# FTP

File Transfer Protocol

Ports:

```text
20

21
```

Transfers files between systems.

Traditional FTP is not encrypted.

---

# DNS

Domain Name System

Port:

```text
53
```

Converts:

```text
example.com

↓

93.184.216.34
```

Uses both Transmission Control Protocol (TCP) and User Datagram Protocol (UDP).

---

# DHCP

Dynamic Host Configuration Protocol

Ports:

```text
67

68
```

Automatically assigns:

- IP Address
- Gateway
- DNS Server
- Subnet Mask

---

# SMTP

Simple Mail Transfer Protocol

Port:

```text
25
```

Used for sending email.

---

# IMAP

Internet Message Access Protocol

Port:

```text
143
```

Allows email synchronisation across devices.

---

# POP3

Post Office Protocol Version 3

Port:

```text
110
```

Downloads email to the client.

---

# TCP vs UDP Ports

| TCP | UDP |
|------|------|
| Reliable | Fast |
| Connection-Oriented | Connectionless |
| Error Recovery | No Recovery |
| Ordered Delivery | Best-Effort Delivery |

Examples:

TCP:

- SSH
- HTTPS
- MySQL

UDP:

- DNS
- DHCP
- Network Time Protocol (NTP)
- Streaming

---

# Secure vs Insecure Protocols

| Insecure | Secure |
|-----------|---------|
| HTTP | HTTPS |
| FTP | SFTP |
| Telnet | SSH |
| LDAP | LDAPS |
| POP3 | POP3S |
| IMAP | IMAPS |
| SMTP | SMTPS |

Modern production environments should always prefer secure protocols.

---

# Socket

A **Socket** uniquely identifies a communication endpoint.

Example:

```text
192.168.1.10:443
```

Socket =

```text
IP Address

+

Port
```

A network connection is established between two sockets.

---

# Real Communication Example

Opening a website:

```text
Browser

↓

example.com

↓

DNS

↓

IP Address

↓

HTTPS

↓

Port 443

↓

Web Server
```

The browser connects to the server's HTTPS service through port **443**.

---

# Viewing Open Ports in Linux

Display listening ports.

```bash
ss -tuln
```

---

Display processes using ports.

```bash
ss -tulpn
```

---

Traditional command.

```bash
netstat -tuln
```

---

Display specific process.

```bash
lsof -i :443
```

---

# Production Perspective

Common production services:

| Service | Port |
|----------|------|
| Nginx | 80, 443 |
| Apache | 80, 443 |
| MySQL | 3306 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| RabbitMQ | 5672 |
| Prometheus | 9090 |
| Grafana | 3000 |
| Kubernetes API | 6443 |
| Elasticsearch | 9200 |

Understanding these ports is essential for firewall configuration, monitoring, and troubleshooting.

---

# Cloud Perspective

Cloud firewalls commonly allow:

- 22 (SSH)
- 80 (HTTP)
- 443 (HTTPS)

Administrators explicitly open additional ports only when required.

Examples:

- AWS Security Groups
- Azure Network Security Groups (NSGs)
- Google Cloud Firewall Rules

---

# Kubernetes Perspective

Common Kubernetes ports:

| Component | Port |
|-----------|------|
| API Server | 6443 |
| kubelet | 10250 |
| etcd | 2379–2380 |
| NodePort Services | 30000–32767 |

These ports enable cluster communication and application access.

---

# Hands-on Lab

## Task 1

Display listening ports.

```bash
ss -tuln
```

---

## Task 2

Display processes using ports.

```bash
ss -tulpn
```

---

## Task 3

Check whether SSH is listening.

```bash
ss -tulpn | grep :22
```

---

## Task 4

Identify which process is using port 80.

```bash
sudo lsof -i :80
```

---

## Task 5

Test HTTP connectivity.

```bash
curl http://example.com
```

---

## Task 6

Test HTTPS connectivity.

```bash
curl https://example.com
```

---

## Task 7

Identify the protocol and default port for the following services:

- SSH
- HTTPS
- DNS
- MySQL
- PostgreSQL
- Redis
- Kubernetes API

---

## Task 8

Create a table listing ten services you commonly use, their protocols (TCP or UDP), default ports, and whether they use encrypted communication.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ss -tuln` | Display listening ports |
| `ss -tulpn` | Display listening ports with processes |
| `netstat -tuln` | Display network ports (legacy) |
| `lsof -i` | Identify process using a port |
| `curl` | Test HTTP/HTTPS services |
| `nc` | Test TCP or UDP connectivity |

---

# Common Mistakes

❌ Confusing IP addresses and ports.

✅ IP identifies the device; port identifies the application.

---

❌ Assuming every protocol uses TCP.

✅ Some protocols, such as DNS and DHCP, use UDP.

---

❌ Leaving unnecessary ports open.

✅ Close unused ports with firewalls or service configuration.

---

❌ Using insecure protocols in production.

✅ Prefer HTTPS, SSH, SFTP, and other encrypted alternatives.

---

❌ Forgetting to check listening ports during troubleshooting.

✅ Use `ss` or `lsof` to verify services.

---

# Best Practices

- Use secure protocols whenever possible.
- Close unused ports.
- Document service port assignments.
- Restrict access using firewalls.
- Regularly audit open ports.
- Avoid exposing internal services directly to the Internet.

---

# Interview Questions

## Beginner

1. What is a network port?
2. What is the difference between TCP and UDP?
3. Which port does HTTPS use?
4. Which protocol is used for remote Linux administration?

---

## Intermediate

1. Explain the difference between well-known, registered, and dynamic ports.
2. Compare HTTP and HTTPS.
3. How would you identify which process is listening on a specific port?
4. Why does DNS use both TCP and UDP?

---

## Architect Level

1. How would you secure network services in a production environment?
2. Explain firewall design based on application ports.
3. How do Kubernetes and cloud platforms rely on ports and protocols?

---

# Summary

In this lesson, you learned:

- What ports are
- How protocols enable communication
- Port number classifications
- TCP and UDP ports
- Common application protocols
- Secure and insecure protocols
- Linux commands for viewing open ports
- Production networking considerations

Ports and protocols work together to ensure that data reaches the correct application on the correct device. While IP addresses identify **where** data should go, ports identify **which application** should receive it, and protocols define **how** the communication takes place.

---

## Key Takeaways

- Ports identify applications running on a device.
- Protocols define communication rules.
- TCP provides reliable communication; UDP prioritises speed.
- Well-known ports are reserved for standard services.
- Production systems should use secure protocols and expose only required ports.

---

## What's Next?

**[Networking Devices](networking-devices.md)**
