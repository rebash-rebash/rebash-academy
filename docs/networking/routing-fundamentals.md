---
title: Routing Fundamentals
description: Master routing tables, default gateways, static and dynamic routes, longest prefix match, Linux ip route commands, and cloud route tables.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - routing
  - ip-route
  - gateway
  - bgp
  - static-routes
prerequisites:
  - Complete Ethernet, Switching, and VLANs or understand Layer 2 vs Layer 3
  - IP Addressing and Subnetting — CIDR, subnets, and broadcast domains
  - Linux CLI familiarity with ip and ping
comments: false
---

# Routing Fundamentals

## Overview

**Routing** is how packets find their way across IP networks. When your application server sends traffic to a database in another subnet — or to a SaaS API on the public internet — the kernel consults a **routing table** to decide which **next hop** receives each packet. Misconfigured routes cause "works locally but not remotely," asymmetric routing, and black holes that look like firewall failures.

This tutorial is **Tutorial 5** in **Module 2: Data Link & Routing** of the REBASH Academy Networking series. You will learn how routers make forwarding decisions, configure static routes on Linux, interpret `ip route` output, and relate on-premises concepts to **cloud route tables** and VPC gateways. Complete [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) first.

## Prerequisites

- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) — CIDR notation, subnet boundaries, and default gateway role
- [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) — ARP, MAC addresses, and same-subnet vs remote delivery
- Linux VM or cloud instance with at least one network interface
- Optional: `sudo` for adding/removing routes and enabling IP forwarding

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain how a host decides whether traffic is local or must go through a gateway
- [ ] Read and interpret Linux routing tables with `ip route`
- [ ] Describe longest prefix match and why more specific routes win
- [ ] Configure static routes and a default gateway on Linux
- [ ] Distinguish static routing from dynamic routing (OSPF, BGP overview)
- [ ] Enable and verify IP forwarding for Linux router lab scenarios
- [ ] Map routing concepts to AWS/GCP route tables and Internet Gateways
- [ ] Diagnose common routing failures using `ip route get` and traceroute

## Architecture

```d2
direction: right

LAN1: "Subnet 10.0.1.0/24" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        H1: "Host 10.0.1.10"
    }
    LAN2: "Subnet 10.0.2.0/24" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        H2: "Host 10.0.2.20"
    }
    LAN3: "Subnet 10.0.3.0/24" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        DB: "Database 10.0.3.5"
    }
    R1: "Router R1\n10.0.1.1 · 10.0.2.1"
    R2: "Router R2\n10.0.2.2 · 10.0.3.1"
    IGW: "Internet Gateway"
    LAN1.H1 -> R1
    R1 -> R2
    R2 -> LAN3.DB
    R2 -> IGW
    LAN2.H2 -> R1
```

Each router maintains a routing table. Traffic from `10.0.1.10` to `10.0.3.5` crosses two routers because the destination is not on the local subnet.

## Theory

### Local Delivery vs Routed Delivery

When a host sends a packet, the kernel compares the destination IP to its own subnet mask:

| Condition | Action |
|-----------|--------|
| Destination on **same subnet** | ARP for destination MAC; deliver directly (Layer 2) |
| Destination on **different subnet** | ARP for **default gateway** MAC; router forwards (Layer 3) |

The **default gateway** (default route) is the router for "everything else." Without it, off-subnet traffic has nowhere to go.

### Routing Tables and Longest Prefix Match

A **routing table** is an ordered list of `(destination prefix, next hop, interface, metric)` entries. When multiple routes match a destination, the kernel selects the **longest prefix match** — the most specific route wins.

| Destination | Next Hop | Interface | Notes |
|-------------|----------|-----------|-------|
| 10.0.2.0/24 | 10.0.1.1 | eth0 | Specific subnet route |
| 10.0.0.0/8 | 10.0.1.1 | eth0 | Broader — loses to /24 for 10.0.2.x |
| 0.0.0.0/0 | 10.0.1.1 | eth0 | Default route — matches everything else |

Example: packet to `10.0.2.50` matches both `10.0.2.0/24` and `10.0.0.0/8`, but `/24` (24-bit prefix) is longer and wins.

**Metric** (or priority) breaks ties when two routes have equal prefix length — lower metric preferred.

### Static vs Dynamic Routing

**Static routes** are manually configured by administrators. Simple, predictable, no protocol overhead — ideal for small networks, point-to-point links, and cloud route tables with fixed paths.

**Dynamic routing** uses protocols so routers exchange reachability information automatically:

| Protocol | Scope | Use Case |
|----------|-------|----------|
| **OSPF** | Interior (within org) | Enterprise LAN/WAN, data center |
| **BGP** | Exterior (between ASes) | Internet routing, multi-homed datacenters, cloud hybrid |
| **RIP** | Interior (legacy) | Small networks — largely obsolete |

**BGP (Border Gateway Protocol)** is how the public internet works. Autonomous Systems (AS) — ISPs, cloud providers, large enterprises — advertise IP prefixes to neighbors. Path selection considers AS path length, policies, and attributes — not just hop count.

In cloud terms, you rarely run BGP yourself unless connecting on-premises via **Direct Connect** or **Cloud VPN** with dynamic routing. You **do** interact with route tables that behave like static routing.

### Linux Routing with ip route

Modern Linux uses the `ip` command from **iproute2**. Legacy `route` and `netstat -r` still appear in old runbooks but should not be used for new work.

Key concepts in `ip route show`:

- **`default via X`** — default gateway at IP X
- **`proto dhcp`** — route installed by DHCP client
- **`src Y`** — preferred source IP for this route
- **`dev eth0`** — egress interface
- **`scope link`** — directly connected network (on-link)

The **`ip route get`** command simulates forwarding decisions — invaluable for debugging:

```bash
ip route get 8.8.8.8
```

Shows which interface, source IP, and next hop the kernel would use for that destination.

### Cloud Route Tables

AWS VPC **route tables** associate subnets with routes:

| Destination | Target | Meaning |
|-------------|--------|---------|
| 10.0.0.0/16 | local | Traffic within VPC stays internal |
| 0.0.0.0/0 | igw-xxx | Default route to Internet Gateway |
| 10.1.0.0/16 | pcx-xxx | Peered VPC traffic |
| 0.0.0.0/0 | nat-xxx | Private subnet outbound via NAT |

Each subnet links to exactly one route table. Missing routes cause silent black holes — packets leave the instance but never return.

### IP Forwarding and Linux as a Router

By default, Linux **does not forward** packets between interfaces — it only routes traffic **to/from itself**. Enabling **`net.ipv4.ip_forward=1`** turns a multi-NIC host into a router (lab, VPN gateway, Kubernetes node).

Production routers use dedicated hardware or cloud virtual appliances. Understanding forwarding explains why a Kubernetes node can reach pod networks on other nodes through the node's routing table and CNI plugins.

## Hands-on Lab

Complete these steps on a Linux host. Route changes may require root; use a lab VM.

### Step 1 – Inspect the routing table

**Command:**

```bash
ip route show
ip -4 route show table main
ip route show default
```

**Explanation:** Lists all IPv4 routes. The default route (if present) shows your gateway for internet-bound traffic.

**Expected output:**

```text
default via 10.0.0.1 dev eth0 proto dhcp src 10.0.0.42 metric 100
10.0.0.0/24 dev eth0 proto kernel scope link src 10.0.0.42
```

### Step 2 – Simulate forwarding decisions

**Command:**

```bash
ip route get 8.8.8.8
ip route get 10.0.0.1
GATEWAY=$(ip route | awk '/default/ {print $3; exit}')
ip route get "$GATEWAY"
```

**Explanation:** Shows exact path the kernel selects — interface, source IP, and next hop. Local gateway should show `dev eth0` with no `via` (on-link).

**Expected output:**

```text
8.8.8.8 via 10.0.0.1 dev eth0 src 10.0.0.42 uid 1000
    cache
10.0.0.1 dev eth0 src 10.0.0.42 uid 1000
    cache
```

### Step 3 – Add and remove a static route (lab)

**Command:**

```bash
# Add route to fictional remote network via gateway
sudo ip route add 192.168.100.0/24 via 10.0.0.1 dev eth0
ip route show 192.168.100.0/24
ip route get 192.168.100.50

# Remove when done
sudo ip route del 192.168.100.0/24 via 10.0.0.1 dev eth0
```

**Explanation:** Static routes persist until reboot unless saved in netplan, NetworkManager, or `/etc/network/interfaces`. More specific than default route for that prefix.

**Expected output:**

```text
192.168.100.0/24 via 10.0.0.1 dev eth0
192.168.100.50 via 10.0.0.1 dev eth0 src 10.0.0.42 uid 0
```

### Step 4 – Observe longest prefix match

**Command:**

```bash
sudo ip route add 10.0.0.0/8 via 10.0.0.1 dev eth0 2>/dev/null || true
ip route get 10.0.0.50
ip route get 10.50.0.1
sudo ip route del 10.0.0.0/8 via 10.0.0.1 dev eth0 2>/dev/null || true
```

**Explanation:** For `10.0.0.50`, the connected `/24` route wins over `/8`. For `10.50.0.1`, only `/8` matches (if `/24` doesn't cover it).

### Step 5 – Check IP forwarding status

**Command:**

```bash
sysctl net.ipv4.ip_forward
cat /proc/sys/net/ipv4/ip_forward
```

**Explanation:** `0` = forwarding disabled (normal for end hosts). `1` = router mode. Kubernetes nodes and VPN servers typically enable this.

**Expected output:**

```text
net.ipv4.ip_forward = 0
```

### Step 6 – Trace the path with traceroute

**Command:**

```bash
traceroute -n 8.8.8.8 2>/dev/null | head -10 \
  || tracepath -n 8.8.8.8 | head -10
```

**Explanation:** Each hop is a router decrementing TTL. First hop is usually your default gateway. Asterisks indicate ICMP filtered at that hop — not necessarily a problem.

### Step 7 – Diagnose missing default route (simulation)

**Command:**

```bash
# Save and temporarily remove default route (lab only!)
DEFAULT=$(ip route | awk '/^default/ {print $0; exit}')
if [ -n "$DEFAULT" ]; then
  sudo ip route del $DEFAULT
  ip route get 8.8.8.8 2>&1 || true
  sudo ip route add $DEFAULT
fi
```

**Explanation:** Without a default route, off-subnet destinations fail with "Network is unreachable" — distinct from firewall timeout.

**Expected output (without default route):**

```text
RTNETLINK answers: Network is unreachable
```

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description | Example |
|---------|-------------|---------|
| `ip route show` | Display routing table | `ip route` |
| `ip route get DST` | Simulate route lookup | `ip route get 10.0.5.1` |
| `ip route add` | Add static route | `sudo ip route add 10.1.0.0/16 via 10.0.0.1` |
| `ip route del` | Remove route | `sudo ip route del 10.1.0.0/16` |
| `ip route replace` | Add or replace route | `sudo ip route replace default via 10.0.0.1` |
| `sysctl net.ipv4.ip_forward` | Check forwarding | `sysctl -w net.ipv4.ip_forward=1` |
| `traceroute -n DST` | Path discovery | `traceroute -n 1.1.1.1` |
| `tracepath DST` | Path without root | `tracepath 8.8.8.8` |

### Route audit script

```bash
#!/usr/bin/env bash
# route-audit.sh — summarize routing configuration for troubleshooting
set -euo pipefail

echo "=== Default Route ==="
ip route show default || echo "(none — off-subnet traffic will fail)"

echo ""
echo "=== All Routes ==="
ip -4 route show

echo ""
echo "=== Sample Lookups ==="
for dst in 8.8.8.8 1.1.1.1; do
  echo -n "$dst → "
  ip route get "$dst" 2>/dev/null | head -1 || echo "unreachable"
done

echo ""
echo "=== IP Forwarding ==="
echo "net.ipv4.ip_forward = $(cat /proc/sys/net/ipv4/ip_forward)"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Wrong subnet mask causes local vs remote confusion"
    A host with `/16` mask may attempt direct ARP for IPs that should go through a gateway. Symptom: works for some hosts in the "logical" subnet but not others.

!!! warning "Asymmetric routing"
    Request takes path A, response returns via path B. Stateful firewalls drop the return traffic. Always verify **both directions** in route and firewall rules.

!!! warning "Overlapping CIDR in peered networks"
    VPC peering and VPN fail silently or route unpredictably when both sides use the same private range. Redesign CIDR before connecting.

!!! warning "Forgetting to persist static routes"
    `ip route add` is lost on reboot. Save in netplan, NetworkManager, or cloud route tables.

!!! warning "Using legacy route command"
    `route -n` output differs from `ip route`. Scripts and runbooks should standardize on iproute2.

## Best Practices

!!! tip "Use ip route get before changing firewalls"
    Confirm the kernel's chosen path and source IP first — misidentified source causes SG/NACL mismatches.

!!! tip "Document every static route with owner and purpose"
    Orphan routes from decommissioned VPNs cause traffic black holes months later.

!!! tip "Design hub-and-spoke or transit gateway for multi-VPC"
    Full mesh peering does not scale. Central transit simplifies route propagation.

!!! tip "Monitor default gateway reachability"
    Alert on ARP/gateway failures — entire off-subnet connectivity dies instantly.

!!! tip "Prefer specific routes over broad summaries"
    Aggregate when possible, but use /32 host routes for critical HA VIP failover scenarios.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Network is unreachable` | No matching route | Add default gateway or specific route; check `ip route` |
| Works by IP, not by hostname | DNS issue, not routing | Use `dig`; see [DNS Fundamentals](dns-fundamentals.md) |
| One-way connectivity | Asymmetric routing or firewall | Compare forward/reverse `traceroute`; check stateful rules |
| Traffic to peered VPC fails | Missing route table entry | Add route to pcx/tgw; verify no CIDR overlap |
| Wrong source IP on outbound | Policy routing or multiple interfaces | `ip route get DST`; check `src` and rule tables |
| Default route missing after reboot | DHCP or config not persisted | Fix netplan/NetworkManager; verify cloud subnet association |
| High latency to nearby host | Suboptimal path via remote gateway | Add direct /32 or fix summary route |
| Cannot reach internet from private subnet | No NAT route or missing NAT GW | Route `0.0.0.0/0` to NAT; verify NAT in public subnet |
| Linux won't forward between NICs | ip_forward disabled | `sysctl -w net.ipv4.ip_forward=1`; check FORWARD chain |

## Summary

- Hosts deliver locally via ARP; **remote traffic** goes to the **default gateway**
- Routers forward using **routing tables** and **longest prefix match**
- **Static routes** are manual; **dynamic protocols** (OSPF, BGP) exchange routes automatically
- Use **`ip route show`** and **`ip route get`** as primary Linux diagnostic tools
- Cloud **route tables** associate subnets with targets (IGW, NAT, peering, TGW)
- **IP forwarding** enables Linux to route between interfaces — required for routers and many K8s/CNI setups
- Routing failures often present as timeouts — distinguish from firewall drops with `ip route get`

## Interview Questions

1. How does a host decide whether to send traffic directly or via a gateway?
2. What is longest prefix match and why does it matter?
3. Explain the difference between static and dynamic routing.
4. What is BGP and where is it used?
5. What does `ip route get 8.8.8.8` tell you?
6. What happens when a host has no default route?
7. What is asymmetric routing and why is it problematic?
8. How do AWS route tables relate to on-premises routing concepts?
9. What is the purpose of `net.ipv4.ip_forward`?
10. Why might traceroute show asterisks for intermediate hops?

??? tip "Sample Answers (Questions 1, 2, and 6)"

    **Q1 — Local vs gateway:** The kernel ANDs the destination IP with the subnet mask. If the result equals the local network address, the destination is on-link — ARP resolves its MAC directly. Otherwise, the packet goes to the configured default gateway (or a more specific route's next hop).

    **Q2 — Longest prefix match:** When multiple routes match a destination IP, the route with the longest (most specific) prefix wins. A /24 route beats a /16 route for addresses within that /24. This allows summary routes with exceptions for specific subnets.

    **Q6 — No default route:** Packets to destinations outside locally connected subnets cannot be forwarded. The kernel returns "Network is unreachable" immediately — no packets leave the interface. On-subnet communication may still work.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Ethernet, Switching, and VLANs](ethernet-switching-and-vlans.md) *(previous)*
- [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) *(next)*
- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md)
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 791 — Internet Protocol](https://www.rfc-editor.org/rfc/rfc791)
- [RFC 4271 — BGP-4](https://www.rfc-editor.org/rfc/rfc4271)
- [ip-route man page](https://man7.org/linux/man-pages/man8/ip-route.8.html)
- [Linux Advanced Routing & Traffic Control HOWTO](https://tldp.org/HOWTO/Adv-Routing-HOWTO/)
- [AWS VPC Route Tables](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html)
- [REBASH Academy – Networking Overview](index.md)
