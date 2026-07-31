---
title: "ICMP, ARP, DHCP, and Network Services"
description: "Master ICMP diagnostics, ARP/neighbour resolution, the DHCP DORA process, and NTP time sync — the control-plane services every Cloud and DevOps path depends on."
difficulty: intermediate
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 7 · Switching"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - icmp
  - arp
  - dhcp
  - ntp
prerequisites:
  - networking/routing-fundamentals
next:
  - networking/tcp-and-udp-deep-dive
related:
  - networking/ethernet-switching-and-vlans
  - networking/dns-fundamentals
  - linux/linux-networking-tools
labs:
  - labs/networking-dns-firewall-triage
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - RHCSA
tags:
  - networking
  - icmp
  - arp
  - dhcp
  - ntp
  - ping
  - traceroute
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# ICMP, ARP, DHCP, and Network Services

## Overview

Inspect and explain the four services that make “basic connectivity” possible — ICMP, ARP/neighbour, DHCP, and NTP — and capture a lab checklist you can reuse in incidents.

TCP and HTTP only work after quieter protocols do their jobs. **DHCP** assigns addressing, **ARP** finds the next-hop MAC, **ICMP** reports path problems (when allowed), and **NTP** keeps clocks honest for logs and certificates. Failures here masquerade as application bugs.

This is part of **Module 7 — Switching** (ARP) and host network services. Complete [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) first. For command overlap, see [Linux Networking Tools](../linux/linux-networking-tools.md); this page focuses on protocol behaviour and production triage.

This is a core tutorial in **Module 7 · Switching** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Routing Fundamentals](routing-fundamentals.md)
- Linux lab host with outbound network access
- Comfort with `ip`, `ping`, and reading command output

### Recommended

- `sudo` for lease inspection and optional packet capture
- `~/rebash-networking/module-02/` from earlier labs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain key ICMP types and why ping/traceroute can fail while TCP works  
- [ ] Read and interpret `ip neigh` / ARP cache state  
- [ ] Describe the DHCP DORA flow and inspect lease information on Linux  
- [ ] Check time sync with `timedatectl` / `chronyc`  
- [ ] Triage “no gateway”, “no DHCP”, and “clock skew” symptoms  
- [ ] Separate protocol failure from firewall filtering

## Architecture

A new host typically: DHCP → ARP gateway → ICMP check → NTP sync.

![Network services path](../assets/excalidraw/what-is-networking.svg)

## Theory

### What it is

Beneath everyday Transmission Control Protocol (TCP) apps sit control-plane helpers: **Internet Control Message Protocol (ICMP)** for reachability and path errors, **Address Resolution Protocol (ARP)** (and the Linux neighbour table) for Internet Protocol (IP)→Media Access Control (MAC) mapping on a segment, **Dynamic Host Configuration Protocol (DHCP)** for address leases, and **Network Time Protocol (NTP)** for clock sync. None of these replace your application protocol; they make the path and identity of the host possible.

### Why it matters

Failed `ping` is the most misread alert in operations — ICMP is often filtered while HTTPS works. Stale ARP/neighbour entries cause “same IP, wrong MAC” black holes after moves or failover. DHCP mistakes hand out the wrong gateway or DNS. Clock skew breaks Transport Layer Security (TLS), Kerberos, and signed cloud Application Programming Interface (API) requests. Knowing these services stops false root causes during triage.

### How it works

ICMP is a Layer 3 control protocol carried in IP. Echo Request/Reply (types 8/0) power `ping`; Destination Unreachable (type 3) and Time Exceeded (type 11) feed traceroute. On Ethernet, ARP answers “Who has this IP?” for on-link destinations or for the **gateway** when the destination is remote; Linux caches answers as neighbour states (`REACHABLE`, `STALE`, `FAILED`, …). DHCP uses the **DORA** exchange (Discover, Offer, Request, Ack) to lease an address plus options (mask, gateway, DNS, lease time). Cloud metadata often replaces classic DHCP, but you still ask “who gave me this address?” NTP clients (`chrony`, `systemd-timesyncd`) keep clocks honest.

!!! note "ICMP is often filtered"
    Security groups and edge firewalls frequently drop ICMP. Failed ping ≠ host down. Confirm with TCP (`curl`, `nc`) on the real port.

### Key concepts and comparisons

| ICMP type | Common use |
|-----------|------------|
| 8 / 0 | Echo Request / Reply (`ping`) |
| 3 | Destination Unreachable |
| 11 | Time Exceeded (traceroute) |

| DHCP step | Role |
|-----------|------|
| Discover / Offer | Find server; propose lease |
| Request / Ack | Accept offer; confirm |

| Time tooling | Notes |
|--------------|-------|
| `timedatectl` | systemd clock + NTP status |
| `chronyc` | chrony diagnostics |
| `systemd-timesyncd` | lighter sync on many Ubuntu images |

### Common pitfalls

- Equating ping failure with host failure.  
- Ignoring neighbour `FAILED` after IP moves or VIP failover.  
- Rogue or mis-scoped DHCP handing out wrong gateways.  
- Disabling ICMP Time Exceeded and wondering why traceroute is blank.  
- Minutes of clock skew → mysterious TLS and API signature errors.

## Hands-on Lab

**Focus:** practise the core workflow for ICMP, ARP, DHCP, and Network Services

```bash
mkdir -p ~/rebash-networking/module-02
cd ~/rebash-networking/module-02

sudo apt-get update
sudo apt-get install -y iproute2 iputils-ping traceroute dnsutils \
  dhcpcd-base 2>/dev/null || true
sudo apt-get install -y chrony || sudo apt-get install -y systemd-timesyncd
```

Tools used below are available on typical Ubuntu images even when the DHCP client package name differs (`systemd-networkd`, NetworkManager, `dhclient`).

### Step 1 — ICMP baseline

```bash
cd ~/rebash-networking/module-02
ping -c 4 127.0.0.1
ping -c 4 1.1.1.1 || echo "ICMP to 1.1.1.1 filtered or unreachable — continue with TCP checks"
```

**Expected:** Loopback succeeds. Public ping may succeed or time out depending on filters.

### Step 2 — Traceroute vs TCP truth

```bash
traceroute -n 1.1.1.1 | head -n 12 || true
curl -sI --max-time 10 https://1.1.1.1/ | head -n 5 || \
  curl -sI --max-time 10 https://example.com/ | head -n 5
```

**Expected:** Even if traceroute is sparse, HTTPS headers can still succeed — document that difference.

### Step 3 — Neighbour / ARP inspection

```bash
GW=$(ip route show default | awk '/default/ {print $3; exit}')
echo "GW=$GW"
ping -c 1 "$GW" 2>/dev/null || true
ip neigh show
ip -br neigh
```

**Expected:** A neighbour entry for the gateway with a MAC when L2 works.

### Step 4 — Flush and rediscover (lab only)

```bash
# Lab only — briefly clears neighbour entries
sudo ip neigh flush all || true
ip neigh show
ping -c 1 "$GW" 2>/dev/null || true
ip neigh show
```

**Expected:** Table empties (or nearly), then the gateway reappears after traffic.

### Step 5 — DHCP / address origin clues

```bash
ip -4 -br addr
ip route show default

# systemd-networkd leases (when present)
ls /run/systemd/netif/leases 2>/dev/null || true
sudo networkctl status 2>/dev/null | sed -n '1,80p' || true

# NetworkManager (when present)
nmcli -f IP4,DHCP4 device show 2>/dev/null | head -n 40 || true

# Classic dhclient leases (when present)
sudo ls /var/lib/dhcp/ 2>/dev/null || true
```

**Expected:** You can state whether the address looks DHCP/cloud-assigned and what the advertised gateway/DNS are (when tools expose them).

### Step 6 — DNS options vs connectivity

```bash
resolvectl status 2>/dev/null | sed -n '1,60p' || cat /etc/resolv.conf
dig +short example.com A | head
```

**Expected:** Resolver addresses are visible; DNS answers return (unless filtered). DHCP often provided those resolvers.

### Step 7 — Time sync check

```bash
timedatectl
timedatectl show-timesync 2>/dev/null || true
chronyc tracking 2>/dev/null || true
date -Is
```

**Expected:** NTP/systemd-timesync reports synchronised (wording varies), and local time looks correct for your zone.

### Step 8 — Capture a services checklist

```bash
{
  echo "=== icmp ==="
  ping -c 2 127.0.0.1 | tail -n 3
  echo
  echo "=== gateway neigh ==="
  ip neigh show to "$GW" 2>/dev/null || ip neigh show | head
  echo
  echo "=== default route ==="
  ip route show default
  echo
  echo "=== time ==="
  timedatectl | sed -n '1,12p'
} | tee network-services-check.txt
```

## Validation

- [ ] You can name ICMP Echo Request/Reply and Time Exceeded roles  
- [ ] You can explain when ARP targets the gateway vs the destination  
- [ ] You can list DORA in order  
- [ ] `ip neigh` shows the gateway after a ping (when a gateway exists)  
- [ ] You inspected how your host learned its address (DHCP/cloud/static clues)  
- [ ] `timedatectl` shows time sync state  
- [ ] `network-services-check.txt` exists  

```bash
test -f ~/rebash-networking/module-02/network-services-check.txt && echo "services check: OK"
```

## Code Walkthrough

Production practice for **ICMP, ARP, DHCP, and Network Services** always combines:

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

!!! warning "Equating ping failure with host failure.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Ignoring neighbour `FAILED` after IP moves or VIP failover.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode ICMP, ARP, DHCP, and Network Services changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Commands | Fix direction |
|---------|--------------|----------|---------------|
| Ping fails, HTTPS works | ICMP filtered | `curl`, `nc` | Trust app-port tests |
| `Destination Host Unreachable` | ARP failure | `ip neigh`, VLAN/subnet | Fix L2 / addressing |
| No address on interface | DHCP failure | `journalctl -u …`, leases | Fix DHCP/server/security group |
| Wrong gateway | Bad DHCP options / static mistake | `ip route` | Correct options / cloud route |
| TLS mysteriously fails | Clock skew | `timedatectl` | Fix NTP |
| Intermittent neighbour FAILED | L2 instability | `ip monit`, switch/cloud attach | Fix link/VLAN |

## Summary

- **ICMP** diagnoses paths when permitted; it is not the application protocol.  
- **ARP/neighbour** binds IP to MAC for on-link next hops.  
- **DHCP (DORA)** automates address, gateway, and DNS options.  
- **NTP** keeps trust in logs and certificates.  
- Production triage checks these services before deep packet captures.

## Interview Questions

1. How does **ICMP, ARP, DHCP, and Network Services** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - Continue with [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — connection state, ports, and reliability trade-offs at the transport layer.

## References

- [RFC 792 – ICMP](https://www.rfc-editor.org/rfc/rfc792)  
- [RFC 826 – ARP](https://www.rfc-editor.org/rfc/rfc826)  
- [RFC 2131 – DHCP](https://www.rfc-editor.org/rfc/rfc2131)  
- [timedatectl(1)](https://www.freedesktop.org/software/systemd/man/timedatectl.html)  
- [chrony documentation](https://chrony-project.org/documentation.html)
