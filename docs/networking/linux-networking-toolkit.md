---
title: "Linux Networking Toolkit"
description: "Operational Linux networking for Cloud and DevOps — ip, ss, ping, traceroute, dig, curl, tcpdump, netcat, and socat with production triage patterns."
difficulty: intermediate
estimated_time: "60–75 min"
technology: networking
category: networking
module: "Module 12 · Linux Networking"
career_paths:
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - platform-engineer
skills:
  - linux-networking-tools
  - packet-triage
prerequisites:
  - networking/routing-fundamentals
  - networking/icmp-arp-dhcp-and-network-services
next:
  - networking/load-balancing-fundamentals
related:
  - linux/linux-networking-tools
  - networking/packet-analysis-tcpdump-wireshark
interview: interview/networking
certifications:
  - RHCSA
  - CompTIA Network+
tags:
  - networking
  - linux
  - ip
  - ss
  - tcpdump
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Linux Networking Toolkit

## Overview

Use the core Linux networking CLI as a single triage toolkit: identity → route → port → DNS → HTTP → capture.

Consoles show symptoms; the host shows truth. This module is the operator’s toolbox named in the Networking course prompt: `ip`, `ss`, `ping`, `traceroute`, `tracepath`, `dig`, `host`, `nslookup`, `curl`, `wget`, `tcpdump`, `tshark`, `netcat`, `socat`.

This is a core tutorial in **Module 12 · Linux Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- Modules 1–7 recommended  
- Ubuntu lab with `sudo`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Inspect addresses, links, and routes with `ip`  
- [ ] List sockets with `ss`  
- [ ] Test DNS with `dig` / `host`  
- [ ] Probe ports with `nc`  
- [ ] Capture traffic safely with `tcpdump`  
- [ ] Run a repeatable triage sequence

## Architecture

Use Excalidraw path thinking: client tools interrogate each layer of the stack on the local host.

![Path reminder](../assets/excalidraw/what-is-networking.svg)

## Theory

### What it is

The Linux networking toolkit is the set of command-line tools you use on a host to answer: Who am I on the network? Can I reach them? Which process is listening? What does Domain Name System (DNS) say? What do packets look like? Core tools include `ip`, `ss`, `ping`, `traceroute`/`tracepath`, `dig`/`host`, `curl`/`wget`, `nc`/`socat`, and `tcpdump`/`tshark`. Consoles and dashboards show symptoms; the host often shows truth.

### Why it matters

Cloud tickets rarely start with “the VPC is wrong” — they start with timeouts and 502s. A repeatable triage sequence (identity → route → port → DNS → HTTP → capture) stops random tool hopping and produces evidence you can paste into an incident channel. Every later production module (load balancers, DNS ops, packet analysis) assumes you can run this ladder under pressure.

### How it works

Start with **identity and routing**: `ip -br addr`, `ip route`. Check **sockets** with `ss -tulpn` to see listeners. Test **reachability** with `ping` only when Internet Control Message Protocol (ICMP) is allowed; otherwise move to Transmission Control Protocol (TCP) probes (`nc -vz`) and Hypertext Transfer Protocol (HTTP) (`curl -sI`). Resolve names with `dig`/`host` against the resolvers the host actually uses. Capture with `tcpdump` using tight filters and a packet count so you do not flood disks. Script the sequence so every engineer runs the same checks.

### Key concepts and comparisons

| Tool | Job |
|------|-----|
| `ip` | Links, addresses, routes, neighbours |
| `ss` | Sockets / listeners (prefer over legacy `netstat`) |
| `ping` / `traceroute` / `tracepath` | Reachability and path (ICMP/UDP) |
| `dig` / `host` / `nslookup` | DNS |
| `curl` / `wget` | HTTP(S) clients |
| `nc` / `socat` | Port probes / relays |
| `tcpdump` / `tshark` | Packet capture / decode |

| Step | Question |
|------|----------|
| Identity | Which addresses and default route? |
| Socket | Is anything listening on the port? |
| DNS | Does the name resolve as expected? |
| L4/L7 | Does TCP/HTTP succeed with a timeout? |
| Capture | What is on the wire when it fails? |

### Common pitfalls

- Declaring a host “down” because ICMP is filtered.  
- Using `curl` without `--max-time` and hanging the triage.  
- Capturing `any` with no filter until the disk fills.  
- Trusting laptop DNS when the failing workload uses different resolvers.  
- Skipping `ss` and blaming the load balancer when nothing listens locally.

## Hands-on Lab

**Focus:** practise the core workflow for Linux Networking Toolkit

```bash
mkdir -p ~/rebash-networking/module-12
cd ~/rebash-networking/module-12
sudo apt-get update
sudo apt-get install -y iproute2 iputils-ping traceroute dnsutils curl wget \
  tcpdump netcat-openbsd socat
```

### Step 1 — Identity

```bash
ip -br link
ip -br addr
ip route
```

### Step 2 — Sockets

```bash
ss -tulpn
```

### Step 3 — DNS

```bash
dig +short example.com A
host example.com
```

### Step 4 — Port & HTTP

```bash
nc -vz example.com 443
curl -sI --max-time 10 https://example.com/ | head
```

### Step 5 — Controlled capture

```bash
sudo tcpdump -ni any -c 20 host example.com and port 443
```

Run a curl in another terminal while capturing.

### Step 6 — Toolkit script

```bash
cat > linux-net-triage.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
t="${1:-example.com}"
echo "== ip =="; ip -br addr; ip route show default
echo "== dns =="; dig +short "$t" A | head
echo "== tcp =="; nc -vz -w 5 "$t" 443
echo "== http =="; curl -sI --max-time 10 "https://$t/" | head -n 5
EOF
chmod +x linux-net-triage.sh
./linux-net-triage.sh example.com | tee triage-out.txt
```

## Validation

- [ ] `ss` shows listeners  
- [ ] `dig` returns answers  
- [ ] Capture shows TCP/443 traffic  
- [ ] `triage-out.txt` saved

## Code Walkthrough

Production practice for **Linux Networking Toolkit** always combines:

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

!!! warning "Declaring a host “down” because ICMP is filtered.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using `curl` without `--max-time` and hanging the triage.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Linux Networking Toolkit changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

Order: address → route → neighbour → DNS → port → HTTP → capture.

## Summary

Linux tools are the production networking IDE. Automate the triage order; capture last.

## Interview Questions

1. How does **Linux Networking Toolkit** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Load Balancing Fundamentals](load-balancing-fundamentals.md)

## References

- [ip(8)](https://man7.org/linux/man-pages/man8/ip.8.html) · [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html) · [tcpdump](https://www.tcpdump.org/)
