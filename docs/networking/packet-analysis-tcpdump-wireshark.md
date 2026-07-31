---
title: "Packet Analysis with tcpdump and Wireshark"
description: "Capture and analyse packets with tcpdump and Wireshark, write BPF filters, read TCP handshakes and TLS ClientHello, and use pcaps as incident evidence."
difficulty: intermediate
estimated_time: "50–65 min"
technology: networking
category: networking
module: "Module 17 · Troubleshooting"
career_paths:
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - linux-administrator
skills:
  - tcpdump
  - wireshark
  - bpf
  - packet-analysis
prerequisites:
  - networking/network-troubleshooting-methodology
next:
  - networking/network-incident-response-and-observability
related:
  - networking/tcp-and-udp-deep-dive
  - networking/linux-networking-toolkit
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
tags:
  - networking
  - tcpdump
  - wireshark
  - pcap
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Packet Analysis with tcpdump and Wireshark

## Overview

Capture minimal useful traffic with `tcpdump`, apply BPF filters, and read handshakes and clear failures in Wireshark — without drowning in noise.

Packet capture is the court reporter of networking. Use it when the methodology ladder still disagrees. Mind privacy and PII — capture only what you need.

This is a core tutorial in **Module 17 · Troubleshooting** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Network Troubleshooting Methodology](network-troubleshooting-methodology.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- Linux host with `sudo` for capture

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Capture to pcap with interface and snaplen choices  
- [ ] Write BPF filters (host, port, net)  
- [ ] Recognise SYN / SYN-ACK / ACK and RST  
- [ ] Spot DNS and TLS ClientHello quickly  
- [ ] Know capture limits (encrypted payloads, off-box paths)

## Architecture

This topic’s control points and relationships are shown below.

![Packet analysis](../assets/excalidraw/packet-analysis.svg)

## Theory

### tcpdump essentials

```bash
# List interfaces
ip -br link

# Capture HTTPS-ish to a file (lab)
# sudo tcpdump -i any -n -s 0 -w lab.pcap host example.com and port 443
```

| Flag | Role |
|------|------|
| `-i` | Interface (`any` on Linux) |
| `-n` | No DNS reverse (faster, clearer) |
| `-s 0` | Full snaplen |
| `-w` | Write pcap |
| `-c` | Stop after N packets |

### BPF examples

```text
port 53
host 10.0.1.50 and port 5432
net 10.0.0.0/8 and tcp
tcp[tcpflags] & tcp-syn != 0
```

### What you can see

- Handshake missing SYN-ACK → filter/path  
- Immediate RST → refused / ACL reject style  
- DNS query/response  
- TLS ClientHello SNI (often visible) — payloads encrypted  

### Wireshark / tshark

Open pcap; use display filters (`tcp.flags.syn==1`, `dns`, `tls.handshake.type == 1`). Follow TCP stream for cleartext HTTP labs only.

## Hands-on Lab

**Focus:** practise the core workflow for Packet Analysis with tcpdump and Wireshark

```bash
mkdir -p ~/rebash-networking/module-17
cd ~/rebash-networking/module-17

sudo apt-get update
sudo apt-get install -y tcpdump wireshark-common tshark
```

### Step 1 – Short local capture

```bash
sudo tcpdump -i lo -n -c 20 port 53 or port 80 or port 443 -w lo-sample.pcap &
sleep 1
dig +short example.com @127.0.0.53 2>/dev/null || dig +short example.com
sudo pkill tcpdump || true
ls -la lo-sample.pcap
```

### Step 2 – Read with tshark

```bash
tshark -r lo-sample.pcap -n 2>/dev/null | head -30 || tcpdump -r lo-sample.pcap -n | head -30
```

### Step 3 – Filter drill

Write BPF for: “TCP to 10.0.2.10 port 8080 from 10.0.1.0/24.”

### Step 4 – Ethics note

Document: no capturing credentials on shared networks; redact before attaching to tickets; prefer staging.

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-17/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Packet Analysis with tcpdump and Wireshark** always combines:

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

!!! warning "Skipping fundamentals for Packet Analysis with tcpdump and Wireshark"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Packet Analysis with tcpdump and Wireshark"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Packet Analysis with tcpdump and Wireshark changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Empty pcap | Wrong iface / filter | Broaden filter; check `any` |
| Too huge | No BPF | Narrow host/port; `-c` |
| Missing flows | Not on path (DSR/overlay) | Capture on both ends / node |

## Summary

- Capture narrowly; filter early  
- Handshake and DNS tell most stories  
- Encrypted apps need metadata + app logs too

## Interview Questions

1. How does **Packet Analysis with tcpdump and Wireshark** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Network Incident Response and Observability](network-incident-response-and-observability.md)

## References

- [tcpdump man page](https://www.tcpdump.org/manpages/tcpdump.1.html)  
- [Wireshark User’s Guide](https://www.wireshark.org/docs/wsug_html/)
