---
title: "Private vs Public IP"
description: "Learn private and public IPv4 addresses — RFC 1918 ranges, NAT, Internet routing, and how enterprise and cloud networks expose services safely."
difficulty: beginner
estimated_time: "90 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 2 · IPv4 Addressing"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
tags:
  - networking
  - ipv4
  - nat
  - private-ip
  - public-ip
  - rebash-networking-mastery
comments: false
status: ready
---

# Private vs Public IP Addresses — Understanding Internet and Internal Network Communication

> Every device connected to a network requires an IP address, but **not every IP address is accessible from the Internet**. Some IP addresses are reserved for **private internal networks**, while others are globally unique and reachable across the Internet. Understanding the difference between **Private** and **Public IP Addresses** is essential for designing enterprise networks, configuring cloud infrastructure, implementing security, and troubleshooting connectivity issues. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should master this concept.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 2: IPv4 Addressing → Lesson 4</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 90 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** IPv4 Addressing</div>

<div markdown>**Lesson:** 4 of 10</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand Public IP addresses
- Understand Private IP addresses
- Identify private IP ranges
- Explain Network Address Translation (NAT)
- Understand Internet routing
- Design private enterprise networks
- Troubleshoot public/private IP issues

---

# Prerequisites

Complete:

- [Binary Numbers](binary-numbers.md)
- [IPv4 Address Structure](ipv4-address-structure.md)
- [IPv4 Classes](ipv4-classes.md)

---

# Why Learn Public and Private IP Addresses?

Suppose your laptop has the IP address:

```text
192.168.1.20
```

Can someone on the Internet connect directly to your laptop?

The answer is:

```text
No
```

Now consider a web server with the IP:

```text
142.250.183.110
```

Anyone on the Internet can reach it (assuming firewall rules allow access).

Why?

Because one address is **private**, while the other is **public**.

---

# What is a Public IP Address?

A **Public IP Address** is a globally unique IPv4 address that is routable on the Internet.

Public IP addresses are assigned by:

- Internet Service Providers (ISPs)
- Cloud Providers
- Regional Internet Registries (RIRs)

They allow devices and services to communicate across the Internet.

---

# Public IP Example

```text
8.8.8.8

1.1.1.1

142.250.183.110
```

These addresses are globally reachable.

---

# Where Are Public IPs Used?

Public IPs are assigned to:

- Websites
- Cloud Virtual Machines
- Load Balancers
- Virtual Private Network (VPN) Gateways
- Mail Servers
- Domain Name System (DNS) Servers
- Internet-facing Application Programming Interfaces (APIs)

---

# Characteristics of Public IP Addresses

- Globally unique
- Internet routable
- Assigned by authorised providers
- Reachable from anywhere (subject to security controls)
- Limited IPv4 resource

---

# What is a Private IP Address?

A **Private IP Address** is reserved for use inside private networks.

Private IP addresses:

- Are **not routable on the Internet**
- Can be reused by different organisations
- Require NAT for Internet access

---

# RFC 1918 Private Address Ranges

The following ranges are reserved for private use:

| Range | CIDR | Historical Class |
|--------|------|------------------|
| 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 | Class A |
| 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 | Class B |
| 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 | Class C |

These ranges are defined in **RFC 1918**.

---

# Private IP Examples

```text
10.1.5.20

172.20.10.50

192.168.1.100
```

These addresses are valid only within private networks.

---

# Public vs Private IP

| Public IP | Private IP |
|------------|------------|
| Internet Routable | Local Network Only |
| Globally Unique | Reusable |
| Assigned by ISP/Cloud | Assigned Locally |
| Used for Public Services | Used Inside Organisations |
| Accessible from Internet | Requires NAT for Internet Access |

---

# Why Do We Need Private IP Addresses?

Imagine every smartphone, laptop, printer, and Internet of Things (IoT) device required a public IPv4 address.

The available IPv4 space would be exhausted very quickly.

Private addressing allows millions of devices to share a smaller pool of public addresses through NAT.

---

# What is NAT?

**Network Address Translation (NAT)** converts private IP addresses into public IP addresses.

Example:

```text
Laptop

192.168.1.10

↓

Router (NAT)

↓

Public IP

203.0.113.25

↓

Internet
```

To Internet servers, the traffic appears to come from the public IP.

---

# Example Communication

Laptop:

```text
192.168.1.20
```

Website:

```text
142.250.183.110
```

Communication:

```text
Laptop

↓

Switch

↓

Router (NAT)

↓

Internet

↓

Web Server
```

The router replaces the private source IP with its public IP before sending packets to the Internet.

---

# Why Can't Private IPs Reach the Internet Directly?

Internet routers do not forward RFC 1918 private addresses.

Example:

```text
192.168.1.10
```

Internet routers discard these routes because they are intended only for private networks.

---

# Home Network Example

```text
Laptop

192.168.1.20

↓

Wi-Fi Router

↓

Public IP

49.x.x.x

↓

Internet
```

All devices in the home share the router's public IP through NAT.

---

# Enterprise Network Example

```text
Employees

↓

10.20.30.0/24

↓

Firewall

↓

NAT Gateway

↓

Public IP

↓

Internet
```

Thousands of internal devices may access the Internet using only a few public IP addresses.

---

# Cloud Example

Cloud Virtual Private Clouds (VPCs) primarily use private IP addresses.

Example:

```text
Web Server

10.0.1.10
```

To make it accessible from the Internet:

```text
Private IP

↓

Load Balancer

↓

Public IP
```

This improves security by limiting direct exposure.

---

# Kubernetes Example

Inside a Kubernetes cluster:

Pods:

```text
10.244.x.x
```

Services:

```text
10.96.x.x
```

These are private addresses.

External users connect through:

- Ingress
- Load Balancer
- Public IP

---

# Advantages of Private IP Addresses

- Conserves public IPv4 addresses
- Improves security
- Supports internal communication
- Simplifies enterprise network design
- Reduces Internet exposure

---

# Advantages of Public IP Addresses

- Internet accessibility
- Global uniqueness
- Required for public-facing services
- Enables external communication

---

# Viewing Your Private IP

Display your private IP address.

```bash
ip addr
```

or

```bash
hostname -I
```

---

# Viewing Your Public IP

Display your Internet-facing IP address.

```bash
curl ifconfig.me
```

Example output:

```text
203.0.113.25
```

This is the address visible to external systems.

---

# Production Perspective

Enterprise environments commonly use:

Private IPs for:

- Application Servers
- Databases
- Kubernetes Nodes
- Internal APIs
- Storage Systems

Public IPs for:

- Load Balancers
- VPN Gateways
- Bastion Hosts
- Public APIs
- Web Applications

This separation enhances both security and scalability.

---

# Cloud Perspective

Cloud providers typically assign:

Private IPs:

- Virtual Machines
- Kubernetes Nodes
- Databases
- Internal Load Balancers

Public IPs:

- Internet-facing Load Balancers
- Bastion Hosts
- NAT Gateways
- Public APIs

Most cloud workloads communicate internally using private IP addresses.

---

# Hands-on Lab

## Task 1

Display your private IP address.

```bash
ip addr
```

---

## Task 2

Display your assigned IP addresses.

```bash
hostname -I
```

---

## Task 3

Display your public IP address.

```bash
curl ifconfig.me
```

---

## Task 4

Determine whether the following addresses are public or private:

```text
10.10.5.20

8.8.8.8

172.20.10.5

192.168.100.25

54.239.28.85
```

---

## Task 5

Draw a home network showing:

- Laptop
- Router
- Internet

Identify the private and public IP addresses used.

---

## Task 6

Draw an enterprise network showing:

- Users
- Firewall
- NAT Gateway
- Internet

Explain how NAT works.

---

## Task 7

Research how your cloud provider assigns private and public IP addresses to virtual machines.

---

## Task 8

Design a small office network using:

- 20 employee computers
- One file server
- One web server
- One Internet connection

Assign appropriate private IP addresses and explain which systems require public IP access.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ip addr` | Display private IP addresses |
| `hostname -I` | Display assigned IPs |
| `ip route` | Display default gateway |
| `curl ifconfig.me` | Display public IP |
| `ping` | Test connectivity |

---

# Common Mistakes

❌ Assuming private IPs are Internet reachable.

✅ Private IPs require NAT or a VPN to communicate beyond private networks.

---

❌ Exposing every server with a public IP.

✅ Use private IPs wherever possible and publish services through load balancers or reverse proxies.

---

❌ Confusing private ranges with loopback addresses.

✅ Loopback uses `127.0.0.0/8`; private ranges are defined by RFC 1918.

---

❌ Believing every cloud VM requires a public IP.

✅ Most cloud workloads operate using private IPs only.

---

❌ Ignoring NAT.

✅ Understand that NAT enables private networks to access the Internet.

---

# Best Practices

- Use private IP addresses for internal systems.
- Expose only necessary services through public IP addresses.
- Implement NAT to provide Internet access for private networks.
- Restrict Internet-facing services with firewalls and security groups.
- Document IP address assignments and network architecture.

---

# Interview Questions

## Beginner

1. What is a public IP address?
2. What is a private IP address?
3. List the RFC 1918 private IPv4 ranges.
4. Why are private IP addresses used?

---

## Intermediate

1. Explain how NAT works.
2. Why can't private IP addresses be routed over the Internet?
3. Compare public and private IP addresses.
4. When would you assign a public IP to a server?

---

## Architect Level

1. Design an enterprise network using public and private IP addresses.
2. Explain how cloud providers separate internal and external traffic.
3. How would you securely expose a Kubernetes application to the Internet?

---

# Summary

In this lesson, you learned:

- Public IP addresses
- Private IP addresses
- RFC 1918 address ranges
- NAT (Network Address Translation)
- Internet routing
- Enterprise and cloud networking
- Linux commands for viewing public and private IPs

Private and public IP addresses work together to enable secure, scalable networking. Private IPs support internal communication while conserving IPv4 address space, and public IPs enable communication across the Internet. NAT bridges these two worlds, making modern enterprise and cloud networking possible.

---

## Key Takeaways

- Public IP addresses are globally routable.
- Private IP addresses are reserved for internal networks.
- RFC 1918 defines the three private IPv4 ranges.
- NAT translates private addresses into public addresses for Internet access.
- Most enterprise and cloud workloads communicate using private IP addresses.

---

## What's Next?

**[Loopback](loopback.md)**
