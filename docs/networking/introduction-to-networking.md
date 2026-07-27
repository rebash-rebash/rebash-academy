---
title: Introduction to Networking
description: Understand why networking matters for DevOps, core terminology, network types, and the role of NICs, switches, routers, and firewalls in modern infrastructure.
difficulty: beginner
estimated_time: "30 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - fundamentals
  - bandwidth
  - latency
  - devops
prerequisites:
  - Basic computer literacy and familiarity with using a terminal
  - Completion of or concurrent study of the Linux Foundations track
  - A Linux VM, cloud instance, or WSL2 environment with network access
comments: false
---

# Introduction to Networking

## Overview

Every production incident involving "the app is down" eventually becomes a networking question: Can the client reach the load balancer? Is DNS resolving? Did a security group block port 443? Can the pod talk to the database? Networking is not a separate specialty reserved for network engineers — it is the connective tissue of every DevOps workflow, from Kubernetes service meshes to Terraform VPC modules to CI/CD pipeline connectivity.

This tutorial builds your foundational mental model: what a **network** is, how **nodes** and **links** relate, why **bandwidth**, **latency**, and **throughput** are different metrics, and how **client-server** architectures differ from **peer-to-peer** designs. You will also learn to identify the core **network devices** — NICs, switches, routers, and firewalls — that appear in every data center and cloud region diagram.

This is **Tutorial 1** in **Module 1: Foundations** of the REBASH Academy Networking series. We recommend completing the [Linux Foundations track](../linux/index.md) first, since nearly all hands-on labs use Linux CLI tools. This tutorial follows our [documentation standards](../about.md#documentation-standards).

## Prerequisites

- Basic computer literacy and comfort typing commands in a terminal
- A Linux environment: Ubuntu VM, WSL2, or a free-tier cloud instance (AWS, GCP, Azure)
- Familiarity with the [Introduction to Linux](../linux/introduction-to-linux.md) tutorial — especially identifying your system and using basic CLI commands
- Network access on your lab machine (Wi-Fi or Ethernet connected and working)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain why networking knowledge is essential for DevOps, SRE, and cloud engineering roles
- [ ] Define nodes, links, bandwidth, latency, and throughput and distinguish between them
- [ ] Compare client-server and peer-to-peer network architectures with production examples
- [ ] Differentiate LAN, WAN, and the public Internet in terms of scope and use cases
- [ ] Identify the function of NICs, switches, routers, and firewalls in a typical topology
- [ ] Inspect your own system's network interfaces and basic connectivity using Linux tools
- [ ] Relate physical and logical network concepts to cloud VPC and subnet terminology

## Architecture Diagram

The diagram below shows a simplified enterprise-to-cloud topology. Every component you will encounter in DevOps maps to one of these roles — even when the physical switch is replaced by a virtual cloud switch or hypervisor vSwitch.

```mermaid
flowchart TB
    subgraph LAN["Office LAN"]
        PC1[Workstation]
        PC2[Developer Laptop]
        SW[Layer 2 Switch]
        PC1 --> SW
        PC2 --> SW
    end

    subgraph EDGE["Network Edge"]
        FW[Firewall]
        RTR["Router / Gateway"]
        SW --> FW
        FW --> RTR
    end

    subgraph WAN["WAN / Internet"]
        ISP[ISP Backbone]
        RTR --> ISP
    end

    subgraph CLOUD["Cloud VPC"]
        IGW[Internet Gateway]
        ALB[Load Balancer]
        APP[App Servers]
        DB["(Database")]
        ISP --> IGW
        IGW --> ALB
        ALB --> APP
        APP --> DB
    end```

## Theory

### Why Networking Matters for DevOps

Modern infrastructure is distributed by default. Microservices communicate over TCP. Kubernetes pods get IP addresses from CNI plugins. Terraform provisions VPCs, subnets, route tables, and security groups. CI/CD runners pull container images from registries across the Internet. When any of these paths break, the symptom is often vague ("502 Bad Gateway", "connection timed out", "no route to host") but the root cause is almost always at a specific network layer.

DevOps engineers need networking literacy to:

- **Design infrastructure** — choose subnet sizes, plan CIDR blocks, avoid overlapping IP ranges between on-premises and cloud
- **Debug incidents** — trace whether failure is DNS, routing, firewall, or application-level
- **Secure systems** — write security group rules, network policies, and WAF configurations with precise port and protocol knowledge
- **Optimize performance** — distinguish latency problems from bandwidth bottlenecks; right-size load balancers and CDN configurations
- **Pass interviews and certifications** — AWS Solutions Architect, CKA, and LFCS all assume TCP/IP fluency

You do not need to become a CCIE. You need a layered mental model and the ability to use tools like `ping`, `curl`, `dig`, `traceroute`, and `ss` — which we build across this entire track.

### Nodes and Links

A **network** is a collection of **nodes** (devices that send and receive data) connected by **links** (communication channels).

| Term | Definition | Examples |
|------|------------|----------|
| **Node** | Any addressable device on a network | Server, laptop, router, IoT sensor, Kubernetes pod |
| **Link** | Physical or logical connection between nodes | Ethernet cable, Wi-Fi radio, fiber, VPN tunnel |
| **Host** | A node that runs applications | EC2 instance, bare-metal server, container |
| **Endpoint** | A specific service address on a host | `10.0.1.5:5432` (PostgreSQL), `api.example.com:443` |

In cloud environments, the physical cable is abstracted away, but the logical model remains: pods are nodes, overlay networks are links, and services are endpoints.

### Bandwidth, Latency, and Throughput

These three metrics are often confused. In incident response and capacity planning, using the wrong term leads to wrong solutions.

| Metric | Definition | Unit | Analogy |
|--------|------------|------|---------|
| **Bandwidth** | Maximum data rate a link *can* carry | Mbps, Gbps | Width of a highway |
| **Latency** | Time for a single packet to travel from source to destination (one-way or round-trip) | ms | Driving time on the highway |
| **Throughput** | Actual data rate achieved in practice | Mbps, Gbps | Number of cars passing per hour |

Key insights for DevOps:

- A **1 Gbps link** with **150 ms RTT latency** is excellent for streaming large backups but terrible for chatty database queries that require many round trips.
- **Throughput** is always ≤ bandwidth because of protocol overhead, congestion, retransmissions, and CPU limits.
- Cloud instance types advertise **network performance** (e.g., "Up to 10 Gbps") — this is bandwidth. Cross-AZ latency in AWS is typically 1–2 ms; cross-region is 50–150 ms. Design accordingly.

### Client-Server vs Peer-to-Peer

**Client-server** architecture dominates production infrastructure. Clients initiate requests; servers listen and respond. The server is typically always on, centrally managed, and scaled horizontally behind load balancers.

| Aspect | Client-Server | Peer-to-Peer (P2P) |
|--------|---------------|---------------------|
| Roles | Fixed: client requests, server responds | Every node can be both consumer and provider |
| Examples | HTTP/API, SSH, PostgreSQL, gRPC | BitTorrent, blockchain nodes, some WebRTC |
| Scaling | Scale servers (more instances, load balancers) | Scale by adding peers; harder to predict |
| DevOps relevance | Default model for all services you deploy | Appears in service meshes, distributed storage (Ceph), and gossip protocols |

In Kubernetes, a **Service** is a stable client-facing endpoint backed by multiple server **Pods** — classic client-server with indirection. P2P patterns appear in etcd cluster communication and distributed tracing agents, but your application architecture is almost certainly client-server.

### LAN, WAN, and the Internet

| Type | Scope | Typical Speed | DevOps Context |
|------|-------|---------------|----------------|
| **LAN** (Local Area Network) | Single building or campus | 1–100 Gbps | Office network; hypervisor vSwitch; VPC is a logical LAN in cloud |
| **WAN** (Wide Area Network) | City, country, or global private links | Mbps–Gbps (varies) | AWS Direct Connect, Azure ExpressRoute, MPLS between data centers |
| **Internet** | Public global network of networks | Highly variable | Public-facing APIs, CDN, package downloads, SaaS integrations |

A **VPC (Virtual Private Cloud)** is a logically isolated LAN in AWS, GCP, or Azure. Subnets within a VPC behave like LAN segments. Connecting VPCs to on-premises data centers creates a hybrid WAN. Understanding LAN vs WAN boundaries helps you decide where to place NAT gateways, VPN endpoints, and regional load balancers.

### Network Devices Overview

#### Network Interface Card (NIC)

A **NIC** is the hardware (or virtual) interface that connects a host to a network. Every IP address you configure is bound to an interface. In Linux, interfaces appear as `eth0`, `ens5`, `enp0s3`, or `lo` (loopback).

Cloud instances use **virtual NICs** (ENI in AWS) attached to a virtual switch. Containers use **virtual Ethernet pairs** (veth) connected to bridge interfaces. The abstraction changes; the concept does not.

#### Switch (Layer 2)

A **switch** forwards **Ethernet frames** based on **MAC addresses** within the same broadcast domain (typically a VLAN or subnet). Switches maintain a MAC address table and send traffic only to the correct port — unlike old hubs that broadcast everything.

In cloud: the hypervisor's virtual switch performs this role. In AWS, traffic within a subnet stays on the VPC fabric. You rarely touch physical switches as a DevOps engineer, but you configure the logical equivalent via VLANs, security groups, and network ACLs.

#### Router (Layer 3)

A **router** forwards **IP packets** between different networks using routing tables. Your **default gateway** is the router that knows how to reach destinations outside your local subnet.

In Linux, routing is handled by the kernel. The `ip route` command shows the routing table. Cloud **route tables** attached to VPC subnets are the same concept at infrastructure scale.

#### Firewall

A **firewall** filters traffic based on rules — typically source/destination IP, port, and protocol. Firewalls operate at multiple layers:

- **Network firewall** — stateful inspection of IP/TCP/UDP (iptables, nftables, AWS Security Groups)
- **Web Application Firewall (WAF)** — Layer 7 HTTP inspection (AWS WAF, Cloudflare)
- **Host firewall** — software on each server (`ufw`, firewalld)

Defense in depth means firewalls at the edge, between tiers, and on each host. We cover firewall configuration in depth in Module 4.

## Hands-on Lab

Complete these steps on any Linux system with network connectivity. Commands are safe without `sudo` unless noted.

### Step 1 – Confirm you are on Linux and identify the distribution

**Command:**

```bash
uname -s
cat /etc/os-release | head -5
```

**Explanation:** Confirms your lab environment. Networking commands in this series assume a Linux kernel network stack.

**Expected output:**

```text
Linux
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
...
```

### Step 2 – List network interfaces

**Command:**

```bash
ip link show
```

**Explanation:** `ip link` displays all network interfaces, their MAC addresses, and state (UP/DOWN). This is the modern replacement for `ifconfig`.

**Expected output:**

```text
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc mq state UP
    link/ether 0a:1b:2c:3d:4e:5f brd ff:ff:ff:ff:ff:ff
```

### Step 3 – View IP addresses assigned to interfaces

**Command:**

```bash
ip -br addr show
```

**Explanation:** Shows a concise view of interface names, states, and assigned IPv4/IPv6 addresses. Every connected host needs at least one IP (plus `127.0.0.1` on loopback).

**Expected output:**

```text
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             10.0.1.42/24 metric 100 ...
```

### Step 4 – Test basic connectivity with ping

**Command:**

```bash
ping -c 4 8.8.8.8
ping -c 4 google.com
```

**Explanation:** `ping` sends ICMP echo requests to measure reachability and round-trip latency. Testing both an IP and a hostname isolates DNS issues from routing issues.

**Expected output:**

```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=12.3 ms
...
4 packets transmitted, 4 received, 0% packet loss
rtt min/avg/max/mdev = 11.8/12.1/12.5/0.3 ms
```

### Step 5 – Identify your default gateway (router)

**Command:**

```bash
ip route show default
```

**Explanation:** The default route points to your **default gateway** — the router that forwards traffic to destinations outside your local subnet.

**Expected output:**

```text
default via 10.0.1.1 dev eth0 proto dhcp src 10.0.1.42 metric 100
```

### Step 6 – Measure download throughput

**Command:**

```bash
curl -o /dev/null -w "Speed: %{speed_download} bytes/sec\nTime: %{time_total}s\n" \
  https://speed.cloudflare.com/__down?bytes=10000000
```

**Explanation:** Downloads 10 MB and reports real-world **throughput**. Convert bytes/sec to Mbps: `(bytes × 8) / 1,000,000`.

### Step 7 – Trace the path to a remote server

**Command:**

```bash
traceroute -n -m 10 google.com 2>/dev/null || tracepath google.com
```

**Explanation:** Shows each **router hop** between your host and the destination. We cover interpretation in [Routing Fundamentals](routing-fundamentals.md).

### Step 8 – Document your network baseline

**Command:**

```bash
echo "=== Network Baseline ==="
echo "Hostname: $(hostname -f)"
echo "Primary IP: $(ip -4 route get 1.1.1.1 2>/dev/null | awk '{print $7; exit}')"
echo "Default GW: $(ip route | awk '/default/ {print $3; exit}')"
echo "DNS: $(grep -m1 nameserver /etc/resolv.conf 2>/dev/null | awk '{print $2}')"
echo "Latency to 8.8.8.8: $(ping -c 3 -q 8.8.8.8 2>/dev/null | awk -F'/' '{print $5}' | tail -1) ms (avg RTT)"
```

**Explanation:** Capture a baseline snapshot for your lab environment. During incidents, comparing current values to a known-good baseline accelerates triage.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `ip link show` | List interfaces and MAC addresses | `ip link show eth0` |
| `ip -br addr` | Brief IP address summary | `ip -br addr show` |
| `ip route show` | Display routing table | `ip route show default` |
| `ping -c N` | Send N ICMP echo requests | `ping -c 4 8.8.8.8` |
| `traceroute` | Trace router hops to destination | `traceroute -n google.com` |
| `tracepath` | Traceroute alternative (no root) | `tracepath 8.8.8.8` |
| `curl -w` | HTTP request with timing metrics | `curl -o /dev/null -w '%{time_total}\n' URL` |
| `ethtool` | NIC driver and link settings | `ethtool eth0` |
| `ss -tuln` | List listening TCP/UDP ports | `ss -tuln` |

### Network baseline script

Save as `~/bin/net-baseline.sh` for quick environment documentation:

```bash
#!/usr/bin/env bash
# net-baseline.sh — capture essential network identity for runbooks
set -euo pipefail

section() { printf '\n=== %s ===\n' "$1"; }

section "Interfaces"
ip -br link

section "Addresses"
ip -br addr

section "Routes"
ip route show

section "DNS"
grep -E '^nameserver' /etc/resolv.conf 2>/dev/null || echo "No resolv.conf"

section "Connectivity"
ping -c 2 -q 8.8.8.8 2>/dev/null && echo "ICMP to 8.8.8.8: OK" || echo "ICMP to 8.8.8.8: FAIL"
curl -s --max-time 5 -o /dev/null -w "HTTPS to cloudflare: HTTP %{http_code} in %{time_total}s\n" \
  https://1.1.1.1 || echo "HTTPS check failed"
```

Make executable: `chmod +x ~/bin/net-baseline.sh && ~/bin/net-baseline.sh`

## Common Mistakes

!!! warning "Using bandwidth and latency interchangeably"
    Upgrading a link from 1 Gbps to 10 Gbps will not fix a 200 ms latency problem caused by cross-region database calls. Measure both metrics separately: `ping` for latency, throughput tests for bandwidth utilization.

!!! warning "Assuming ping failure means the host is down"
    Many production firewalls and cloud security groups **block ICMP**. A host may be fully reachable on TCP port 443 while `ping` fails. Always test the actual protocol and port your application uses.

!!! warning "Ignoring the default gateway"
    Misconfigured or missing default routes cause "works locally, fails everywhere else" symptoms. Always check `ip route show default` before deep-diving into application logs.

!!! warning "Treating cloud VPCs as 'the Internet'"
    Resources inside a VPC communicate over private LAN-like paths. Outbound Internet access requires explicit configuration: Internet Gateway, NAT Gateway, or proxy.

## Best Practices

!!! tip "Document network baselines for every environment"
    Record default gateway, DNS servers, expected latency to key dependencies, and interface names in your runbooks. Incidents are faster when you know what "normal" looks like.

!!! tip "Test connectivity at the correct layer"
    Follow a top-down approach: application → DNS → TCP port → routing → interface. Do not start with packet captures when `curl` already shows a DNS failure.

!!! tip "Use private networking inside cloud environments"
    Place databases, caches, and internal APIs on private subnets without public IPs. Only load balancers and bastion hosts need Internet-facing addresses.

!!! tip "Learn Linux networking tools before GUI dashboards"
    AWS and GCP consoles show symptoms; `ip`, `ss`, `dig`, and `traceroute` on the actual host reveal causes. The [Linux track](../linux/index.md) complements this series directly.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Network is unreachable` | No route to destination; missing default gateway | Check `ip route`; verify gateway IP and interface are correct |
| `Name or service not known` | DNS resolution failure | Inspect `/etc/resolv.conf`; test with `dig`; try IP directly |
| Interface shows `DOWN` | Cable unplugged, disabled interface, or driver issue | Run `ip link set eth0 up`; check `dmesg` for NIC errors |
| High latency but low bandwidth usage | Geographic distance or suboptimal routing | Compare cross-AZ vs cross-region; use `traceroute` |
| Low throughput near bandwidth cap | Link saturation or CPU bottleneck | Monitor with `iftop`; check instance network limits |
| Can reach IP but not hostname | DNS misconfiguration | Verify `/etc/resolv.conf` and VPC DNS settings |
| `ping` works but application fails | Firewall blocking application port | Test with `curl`, `nc -zv host port`, or `ss` on server |

## Summary

- Networking is foundational for DevOps — every deployment, debug session, and cloud design depends on it
- **Nodes** connect via **links**; understand **bandwidth** (capacity), **latency** (delay), and **throughput** (actual speed) as distinct metrics
- Production systems use **client-server** architecture; **LAN** covers local segments (including VPCs), **WAN** connects sites, and the **Internet** is the public global network
- **NICs** provide host connectivity; **switches** forward at Layer 2; **routers** forward at Layer 3; **firewalls** enforce access policy
- Use `ip link`, `ip addr`, `ip route`, `ping`, and `traceroute` to inspect your Linux system's network state

## Interview Questions

1. Why is networking knowledge important for a DevOps engineer?
2. What is the difference between bandwidth, latency, and throughput?
3. Explain client-server architecture and give three production examples.
4. What is the difference between a LAN, a WAN, and the Internet?
5. What role does a default gateway play in IP networking?
6. How does a switch differ from a router?
7. Why might `ping` fail while HTTPS to the same host succeeds?
8. What is a VPC in cloud networking, and how does it relate to LAN concepts?
9. Name the four network devices covered in this tutorial and their primary function.
10. How would you quickly document the network configuration of an unfamiliar Linux server?

??? tip "Sample Answers (Questions 2, 6, and 7)"

    **Q2 — Bandwidth vs latency vs throughput:** Bandwidth is the maximum data rate a link supports (e.g., 1 Gbps). Latency is the time for a packet to travel from source to destination (e.g., 15 ms RTT). Throughput is the actual data rate achieved in practice, which is always less than or equal to bandwidth due to overhead, congestion, and protocol limitations.

    **Q6 — Switch vs router:** A switch operates at Layer 2 and forwards Ethernet frames based on MAC addresses within the same broadcast domain. A router operates at Layer 3 and forwards IP packets between different networks using routing tables.

    **Q7 — Ping fails, HTTPS works:** Many firewalls block ICMP while allowing TCP port 443. Always test the specific protocol and port your application depends on.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Introduction to Linux](../linux/introduction-to-linux.md) — recommended prerequisite from the Linux track
- [OSI and TCP/IP Models](osi-and-tcp-ip-models.md) *(next in Module 1)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 1122 – Requirements for Internet Hosts](https://www.rfc-editor.org/rfc/rfc1122)
- [Linux `ip-route` man page](https://man7.org/linux/man-pages/man8/ip-route.8.html)
- [Cloudflare Learning Center – What is latency?](https://www.cloudflare.com/learning/performance/glossary/what-is-latency/)
- [AWS VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [REBASH Academy – Linux Overview](../linux/index.md)
- [REBASH Academy – Networking Overview](index.md)
