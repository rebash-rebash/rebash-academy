---
title: "VPN and Tunneling Basics"
description: "Understand site-to-site and remote-access VPNs, IPsec and WireGuard concepts, hybrid private connectivity, and when to choose VPN vs Direct Connect-style links."
difficulty: intermediate
estimated_time: "40–55 min"
technology: networking
category: networking
module: "Module 16 · Production Networking"
career_paths:
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - platform-engineer
skills:
  - vpn
  - ipsec
  - wireguard
  - hybrid-networking
prerequisites:
  - networking/cloud-networking-vpc-and-subnets
next:
  - networking/network-security-hardening
related:
  - networking/routing-fundamentals
  - networking/network-segmentation-and-trust-boundaries
labs: []
projects: []
interview: interview/networking
certifications:
  - AWS SAA
  - CompTIA Network+
tags:
  - networking
  - vpn
  - ipsec
  - wireguard
  - hybrid
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# VPN and Tunneling Basics

## Overview

Explain site-to-site vs remote-access VPN, compare IPsec and WireGuard at an ops level, and place VPN next to private connectivity options in hybrid designs.

**VPNs** encrypt traffic across untrusted networks so on-prem and cloud private CIDRs can talk — or so admins can reach private ops endpoints. Production also uses **private connectivity** (Direct Connect, ExpressRoute, Interconnect) when bandwidth and SLA matter more than a simple tunnel.

This is the first tutorial in **Module 16**. Complete [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 16 · Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)
- [Routing Fundamentals](routing-fundamentals.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast site-to-site and remote-access VPN  
- [ ] Describe IPsec and WireGuard roles  
- [ ] Explain split tunnel vs full tunnel  
- [ ] Place VPN vs dedicated private links  
- [ ] List common hybrid failure modes (PSK, SA, routes, overlapping CIDR)

## Architecture

On-prem and cloud private networks join through an encrypted tunnel.

![VPN tunneling](../assets/excalidraw/vpn-tunneling.svg)

## Theory

### What it is

A Virtual Private Network (VPN) encrypts traffic between sites or users and a private network over the public internet. **Tunnels** (IPsec, WireGuard, Transport Layer Security (TLS)-based Virtual Private Networks) carry inner packets inside outer encrypted packets. Ops care about tunnel state, routing of private Classless Inter-Domain Routing (CIDR) blocks, and whether clients use split or full tunnel — not only “the VPN app connected.”

### Why it matters

Hybrid cloud and admin access still depend on tunnels. A tunnel that is “up” but missing routes looks identical to a security-group deny from the user’s point of view. Overlapping `10.0.0.0/8` ranges are the classic hybrid blocker. Choosing VPN when you need sustained high throughput or a regulatory private path sets you up for chronic latency and packet-loss tickets.

### How it works

**Site-to-site** links a data centre to a Virtual Private Cloud (VPC) continuously. **Remote access** brings an admin laptop into private subnets. **Client mesh** tools (WireGuard/Tailscale-style) emphasise identity-centric access. IPsec (often IKEv2 with pre-shared keys or certificates) dominates cloud VPN gateways — policy-based or route-based. WireGuard uses a simpler key model over User Datagram Protocol (UDP). TLS-based options (OpenVPN and similar) sometimes traverse restrictive egress more easily. After the tunnel is up, **both sides must route** private CIDRs; without routes, encryption alone does nothing useful.

### Key concepts and comparisons

| Type | Typical use |
|------|-------------|
| Site-to-site | DC ↔ VPC always-on |
| Remote access | Admin laptop → private network |
| Client mesh | Identity-centric access |

| Mode | Behaviour |
|------|-----------|
| Split tunnel | Only private destinations via VPN |
| Full tunnel | All client traffic via VPN (control vs cost/latency) |

| Need | Prefer |
|------|--------|
| Always-on hybrid, moderate volume | Managed IPsec VPN |
| High sustained throughput / strict SLA | Direct Connect / ExpressRoute / Interconnect (VPN as backup) |

### Common pitfalls

- Declaring success when Phase 1/2 is up but routes are missing.  
- Overlapping CIDRs across on-prem and cloud.  
- PSKs in tickets or git; no rotation.  
- Full tunnel without capacity planning (hairpinning all SaaS).  
- Using VPN as the only path with no monitoring of tunnel state or bytes.

## Hands-on Lab

**Focus:** practise the core workflow for VPN and Tunneling Basics

```bash
mkdir -p ~/rebash-networking/module-16
cd ~/rebash-networking/module-16
```

### Step 1 – Design a hybrid path

```text
On-prem 10.50.0.0/16 ↔ VPN ↔ VPC 10.20.0.0/16
Interesting traffic: both CIDRs
Redundant tunnels: AZ-a + AZ-b
```

### Step 2 – Failure checklist

Document checks for: IKE/PSK mismatch, phase-2 selectors, missing routes, NAT-T, firewall UDP 500/4500, asymmetric return path.

### Step 3 – Compare options

One paragraph: when you would pick managed cloud VPN vs WireGuard bastion vs private circuit.

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-16/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **VPN and Tunneling Basics** always combines:

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

!!! warning "Declaring success when Phase 1/2 is up but routes are missing.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Overlapping CIDRs across on-prem and cloud.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode VPN and Tunneling Basics changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Tunnel down | PSK/IKE/firewall | Check gateway logs; UDP 500/4500 |
| Tunnel up, no ping | Routes / selectors | Align CIDRs; check RT |
| One-way traffic | Asymmetric routing | Fix return routes |
| Intermittent | Single AZ VPN | Add redundant tunnels |

## Summary

- VPNs encrypt hybrid paths; routes and CIDRs make them usable  
- IPsec dominates classic cloud site-to-site; WireGuard dominates modern overlays  
- Private circuits complement VPN for production scale

## Interview Questions

1. How does **VPN and Tunneling Basics** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Network Security Hardening](network-security-hardening.md)

## References

- [AWS Site-to-Site VPN](https://docs.aws.amazon.com/vpn/)  
- [WireGuard](https://www.wireguard.com/)
