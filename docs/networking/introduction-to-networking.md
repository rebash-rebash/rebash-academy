---
title: "What is Networking?"
description: "Networking fundamentals for Cloud and DevOps — network types (LAN, WAN, MAN, VPN, Internet, Intranet, Extranet), topologies, and how production paths carry application traffic."
difficulty: beginner
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 1 · Networking Fundamentals"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
skills:
  - networking-fundamentals
  - network-types
  - topologies
prerequisites:
  - linux/linux-fundamentals-distributions-and-architecture
next:
  - networking/osi-model
related:
  - linux/linux-networking-tools
  - cheatsheets/networking
  - interview/networking
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - fundamentals
  - lan
  - wan
  - vpn
  - topologies
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# What is Networking?

## Overview

Build a production mental model of networking for Cloud and DevOps: what a network is, how network types differ, which topologies you will meet, and how to capture a baseline of your Linux host’s path to the Internet.

A **network** is a set of systems that exchange data. In Cloud and DevOps work that exchange is never abstract — it is the reason a pod reaches a database, a CI runner pulls an image, or a user hits your load balancer.

This course teaches networking from an **operations and troubleshooting** perspective, not as classic campus switching theory alone. Module 1 answers: what are we connecting, over which kind of network, and in which shape?

This is **Module 1 — Networking Fundamentals** of **Networking for Cloud & DevOps Engineers**.

This is a core tutorial in **Module 1 · Networking Fundamentals** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- Basic Linux knowledge and terminal familiarity
- A Linux lab host (Ubuntu 22.04/24.04, WSL2, or cloud free tier)

### Recommended

- [Linux Fundamentals](../linux/linux-fundamentals-distributions-and-architecture.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Define networking in operational terms (nodes, links, endpoints, paths)
- [ ] Compare LAN, MAN, WAN, Internet, Intranet, Extranet, and VPN
- [ ] Recognise common topologies (star, bus, mesh) and where they appear today
- [ ] Explain bandwidth, latency, and throughput with incident examples
- [ ] Map classic network types to cloud VPC and hybrid designs
- [ ] Capture a Linux network baseline with `ip`, `ping`, and `traceroute`

## Architecture

Every Cloud / DevOps request travels a path of trust boundaries.

![What is networking — client to Internet path](../assets/excalidraw/what-is-networking.svg)

## Theory

### What is networking?

Networking is how **nodes** exchange data over **links** so applications can talk to **endpoints**.

| Term | Meaning | Example |
|------|---------|---------|
| Node | Device that sends/receives | VM, laptop, router, pod |
| Link | Path between nodes | Ethernet, Wi‑Fi, VPN tunnel |
| Host | Node running workloads | EC2 instance, bare metal |
| Endpoint | Service address | `10.0.1.5:5432`, `api.example.com:443` |
| Path | Sequence of hops | Client → LB → app → DB |

If you can name the path, you can troubleshoot the path.

### Network types

![Network types](../assets/excalidraw/network-types.svg)

| Type | Scope | DevOps relevance |
|------|-------|------------------|
| **LAN** | Building, rack, or logical cloud network | Office LAN; **VPC ≈ logical LAN** |
| **MAN** | City / metro | Less common day-to-day; ISP metro links |
| **WAN** | Distant sites / regions | Site-to-site VPN, Direct Connect / ExpressRoute |
| **Internet** | Public global network | Public APIs, registries, CDNs |
| **Intranet** | Private organisational network | Internal apps, private DNS |
| **Extranet** | Controlled partner access | Vendor VPN, private APIs for partners |
| **VPN** | Encrypted overlay across untrusted networks | Remote admin, hybrid cloud |

### Internet vs Intranet vs Extranet

| | Internet | Intranet | Extranet |
|-|----------|----------|----------|
| Audience | Anyone (public) | Employees / internal systems | Specific partners |
| Trust | Untrusted | Higher trust, still segmented | Contractual trust |
| Example | Public website | Internal wiki, CI | Supplier inventory API |

### VPN in one paragraph

A **VPN** creates an encrypted tunnel so private traffic can cross a public or untrusted network. In Cloud/DevOps you meet client VPNs (admin access) and site-to-site VPNs (datacentre ↔ VPC). Later modules cover WireGuard/IPsec patterns; here, treat VPN as “private connectivity over someone else’s network.”

### Network topologies

![Network topologies](../assets/excalidraw/network-topologies.svg)

| Topology | Idea | Where you still see it |
|----------|------|------------------------|
| **Star** | Endpoints meet at a central switch | Most LANs, ToR switches |
| **Bus** | Shared backbone (historic) | Rare in modern Ethernet |
| **Mesh** | Many-to-many links | Spine-leaf fabrics, service meshes (logical), BGP at edge |
| **Hybrid** | Mix of the above | Almost every real enterprise / cloud design |

Modern data centres prefer **spine-leaf** (a structured mesh). Cloud abstracts the cables; your job is still to design **failure domains** and **paths**.

### Bandwidth, latency, throughput

| Metric | Meaning | Unit |
|--------|---------|------|
| Bandwidth | Maximum rate a link can carry | Mbps / Gbps |
| Latency | Time for a packet to travel | ms |
| Throughput | Rate actually achieved | Mbps / Gbps |

A wide pipe with high latency is fine for bulk sync and poor for chatty APIs. Design chatty tiers in the same AZ/region when you can.

### Client-server (the default)

Production systems are usually **client-server**: clients initiate, servers listen, scale happens behind load balancers. Peer-to-peer appears in specialised systems (gossip, some storage), but your first mental model should be client-server.

## Hands-on Lab

**Focus:** practise the core workflow for What is Networking?

```bash
mkdir -p ~/rebash-networking/module-01
cd ~/rebash-networking/module-01

sudo apt-get update
sudo apt-get install -y iproute2 iputils-ping traceroute curl
```

### Step 1 — Confirm the lab host

```bash
cd ~/rebash-networking/module-01
uname -a
. /etc/os-release && echo "$PRETTY_NAME"
```

### Step 2 — Identify your attachment to the network

```bash
ip -br link
ip -br addr
```

**Expected:** A primary interface `UP` with an IPv4 CIDR (LAN/VPC address).

### Step 3 — Find the gateway (edge of your LAN)

```bash
ip route show default
```

**Expected:** `default via <gateway> dev <iface>` — your WAN/Internet exit from this LAN.

### Step 4 — Classify your address

```bash
IP=$(ip -4 -o addr show scope global | awk '{print $4; exit}' | cut -d/ -f1)
echo "Address: $IP"
case "$IP" in
  10.*|192.168.*|172.1[6-9].*|172.2[0-9].*|172.3[0-1].*) echo "Likely private (Intranet / VPC style)" ;;
  *) echo "Public or other — treat as Internet-facing until proven otherwise" ;;
esac
```

### Step 5 — Measure path characteristics

```bash
ping -c 5 1.1.1.1 || echo "ICMP filtered — try TCP next"
traceroute -n 1.1.1.1 | head -n 12 || true
curl -sI --max-time 10 https://example.com/ | head -n 5
```

**Expected:** Either ICMP RTT samples or a clear filter; traceroute hops; HTTP headers proving an application path works.

### Step 6 — Write a fundamentals baseline

```bash
{
  echo "=== identity ==="
  hostnamectl 2>/dev/null || hostname
  echo
  echo "=== addresses ==="
  ip -br addr
  echo
  echo "=== default ==="
  ip route show default
  echo
  echo "=== notes ==="
  echo "network_type_guess: private LAN/VPC or public — fill from Step 4"
  echo "topology_guess: star (typical access LAN) unless told otherwise"
} | tee fundamentals-baseline.txt
```

## Validation

- [ ] You can define node, link, endpoint, and path  
- [ ] You can contrast LAN, WAN, Internet, Intranet, Extranet, and VPN  
- [ ] You can name star vs mesh with one modern example each  
- [ ] `fundamentals-baseline.txt` exists  
- [ ] You reached an HTTPS endpoint from the lab host  

```bash
test -f ~/rebash-networking/module-01/fundamentals-baseline.txt && echo "baseline: OK"
```

## Code Walkthrough

Production practice for **What is Networking?** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for networking as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Skipping fundamentals for What is Networking?"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for What is Networking?"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode What is Networking? changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely meaning | Next check |
|---------|----------------|------------|
| No default route | Not attached to a gateway / DHCP failed | `ip route`, cloud route table |
| Private IP but no Internet | Missing NAT / VPN / proxy | Egress path design |
| Ping fails, HTTPS works | ICMP filtered | Trust application port tests |
| High latency | Distant region / long WAN path | Prefer local AZ |

## Summary

- Networking is how nodes exchange data along paths to endpoints.  
- **LAN / MAN / WAN / Internet / Intranet / Extranet / VPN** describe scope and trust.  
- Topologies (star, mesh, hybrid) still matter as failure-domain thinking.  
- Measure **bandwidth**, **latency**, and **throughput** separately.  
- Capture a Linux baseline before you need it in an incident.

## Interview Questions

1. How does **What is Networking?** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - Continue with [OSI Model](osi-model.md) — the seven-layer vocabulary you will use in every incident.

## References

- [RFC 1122 – Requirements for Internet Hosts](https://www.rfc-editor.org/rfc/rfc1122)  
- [NIST SP 800-47 – Security Guide for Interconnecting IT Systems](https://csrc.nist.gov/publications/detail/sp/800-47/final)  
- [AWS VPC overview](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
