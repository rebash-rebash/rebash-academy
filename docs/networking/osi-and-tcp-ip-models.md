---
title: OSI and TCP/IP Models
description: Master the OSI seven-layer and TCP/IP four-layer models, encapsulation, decapsulation, and which DevOps tools operate at each layer.
difficulty: beginner
estimated_time: "35 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - osi-model
  - tcp-ip
  - encapsulation
  - devops
prerequisites:
  - Introduction to Networking (Tutorial 1 in this series)
  - Basic Linux CLI familiarity from the Linux Foundations track
comments: false
---

# OSI and TCP/IP Models

## Overview

When a user clicks "Checkout" in your web application, data traverses multiple layers of processing — from HTTP headers down to electrical signals on a wire — and back up again on the server. The **OSI model** (Open Systems Interconnection) and the **TCP/IP model** provide standardized frameworks for understanding this journey. They are not protocols themselves; they are **reference models** that describe how network communication is organised.

For DevOps engineers, layered models are the single most useful troubleshooting framework. "Is this a Layer 7 problem or a Layer 3 problem?" determines whether you reach for `curl`, `dig`, `tcpdump`, or `ip route`. This tutorial explains both models, walks through **encapsulation** and **decapsulation**, and maps everyday tools to the layers they inspect.

This is **Tutorial 2** in **Module 1: Foundations** of the REBASH Academy Networking series. Complete [Introduction to Networking](introduction-to-networking.md) first.

## Prerequisites

- [Introduction to Networking](introduction-to-networking.md) — nodes, links, bandwidth, latency, and basic Linux network commands
- [Introduction to Linux](../linux/introduction-to-linux.md) — comfortable running terminal commands
- A Linux lab environment with `curl`, `ping`, and network utilities installed

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Name and describe all seven OSI layers and the four TCP/IP layers
- [ ] Map OSI layers to TCP/IP layers and explain why both models coexist
- [ ] Trace encapsulation from application data to bits on the wire and decapsulation on receive
- [ ] Identify which layer common DevOps tools operate at (curl, dig, tcpdump, iptables, etc.)
- [ ] Apply layered thinking to narrow down connectivity failures systematically
- [ ] Explain Protocol Data Units (PDUs) at each layer — segment, packet, frame
- [ ] Predict where in the stack a given failure symptom originates

## Architecture

The diagram below shows how the OSI and TCP/IP models align, and how data is encapsulated as it descends the stack.

```d2
direction: down

APP: "Application Layer" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        DATA: "Application Data\nHTTP JSON DNS"
    }
    L47: "OSI Layers 5-7 / TCP/IP Application" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        L7: "L7 Application — HTTP TLS DNS"
        L6: "L6 Presentation — Encoding TLS"
        L5: "L5 Session — Connection mgmt"
    }
    L4: "Layer 4 — Transport" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        L4N: "TCP / UDP\nSegment + Port"
    }
    L3: "Layer 3 — Network" {
      style: {
        fill: "#f3e8ff"
        stroke: "#9333ea"
      }
        L3N: "IP — Packet + IP addr"
    }
    L2: "Layer 2 — Data Link" {
      style: {
        fill: "#fce7f3"
        stroke: "#db2777"
      }
        L2N: "Ethernet — Frame + MAC"
    }
    L1: "Layer 1 — Physical" {
      style: {
        fill: "#e0f2f1"
        stroke: "#00796b"
      }
        L1N: "Bits on wire / fiber / radio"
    }
    APP.DATA -> L47.L7
    L47.L7 -> L47.L6
    L47.L6 -> L47.L5
    L47.L5 -> L4.L4N
    L4.L4N -> L3.L3N
    L3.L3N -> L2.L2N
    L2.L2N -> L1.L1N
```

## Theory

### Why Layered Models Exist

Network communication involves dozens of protocols cooperating simultaneously. Layered models provide:

- **Separation of concerns** — each layer solves one problem and exposes a service to the layer above
- **Interoperability** — any Layer 3 protocol (IP) works with any Layer 2 (Ethernet, Wi-Fi, PPP)
- **Troubleshooting vocabulary** — "Layer 4 timeout" instantly tells an engineer to check TCP, ports, and firewalls
- **Tool selection** — knowing the layer narrows which diagnostic tool to use first

The OSI model was defined by ISO in 1984 as a theoretical reference. The TCP/IP model emerged from the ARPANET protocols that became the Internet. In practice, engineers use both — OSI for precision, TCP/IP for how the Internet actually works.

### The OSI Seven-Layer Model

| Layer | Name | PDU | Function | Protocols / Examples |
|-------|------|-----|----------|---------------------|
| **7** | Application | Data | User-facing services and APIs | HTTP, HTTPS, DNS, SSH, SMTP, gRPC |
| **6** | Presentation | Data | Translation, encryption, compression | TLS/SSL, JSON, Protobuf, ASCII |
| **5** | Session | Data | Connection establishment, maintenance, teardown | TLS sessions, RPC, NetBIOS |
| **4** | Transport | Segment/Datagram | End-to-end delivery, ports, reliability | TCP, UDP, QUIC |
| **3** | Network | Packet | Logical addressing, routing between networks | IPv4, IPv6, ICMP, IPsec |
| **2** | Data Link | Frame | Physical addressing (MAC), error detection on LAN | Ethernet, Wi-Fi (802.11), VLAN (802.1Q) |
| **1** | Physical | Bits | Electrical/optical/radio transmission | Cables, fiber, radio frequencies |

**Mnemonic (top to bottom):** "All People Seem To Need Data Processing"

### The TCP/IP Four-Layer Model

| TCP/IP Layer | Maps to OSI | Function | Key Protocols |
|--------------|-------------|----------|---------------|
| **Application** | Layers 5, 6, 7 | Application services | HTTP, DNS, SSH, TLS |
| **Transport** | Layer 4 | Host-to-host communication | TCP, UDP |
| **Internet** | Layer 3 | Routing and logical addressing | IP, ICMP |
| **Network Access** | Layers 1, 2 | Physical transmission and framing | Ethernet, ARP, drivers |

When engineers say "Layer 4 load balancer," they mean **TCP/UDP** (OSI Layer 4). "Layer 7" means **HTTP headers, cookies, paths** (OSI Layer 7).

### Encapsulation Walkthrough

Sending `GET / HTTP/1.1` from browser to server:

1. **Application:** Browser builds HTTP request
2. **Transport:** TCP adds source/dest port, sequence numbers → **segment**
3. **Network:** IP adds source/dest IP addresses → **packet**
4. **Data Link:** Ethernet adds source/dest MAC → **frame**
5. **Physical:** Frame transmitted as bits on the wire

At each hop (switch, router), the device reads headers appropriate to its layer, then forwards. **Routers** strip L2 headers and add new ones — MAC addresses change per hop; IP addresses typically stay end-to-end.

### DevOps Tool-to-Layer Mapping

| Tool / Command | Primary Layer(s) | What It Inspects |
|----------------|------------------|------------------|
| `curl`, `wget` | L7 (Application) | HTTP request/response |
| `dig`, `nslookup`, `host` | L7 (Application) | DNS queries and records |
| `openssl s_client` | L6/L7 (Presentation/App) | TLS certificates and handshake |
| `ssh`, `scp` | L7 (Application) | SSH protocol |
| `nc` (netcat) | L4 (Transport) | Raw TCP/UDP connectivity to ports |
| `ss`, `netstat` | L4 (Transport) | Sockets, listening ports, connections |
| `tcpdump`, Wireshark | L2–L7 (All) | Full packet capture with decode |
| `nmap` | L3–L7 | Port scanning, OS fingerprinting |
| `ping` | L3 (Network) | ICMP echo (IP-level reachability) |
| `traceroute` / `tracepath` | L3 (Network) | IP routing path and hop latency |
| `ip route`, `route` | L3 (Network) | Kernel routing table |
| `ip neigh`, `arp -a` | L2/L3 boundary | MAC ↔ IP mapping |
| `ip link`, `ethtool` | L1/L2 | Interface speed, link state |
| `iptables`, security groups | L3–L4 (sometimes L7) | Filter rules |

### Layered Troubleshooting Methodology

When connectivity fails, work **top-down** (application to physical) or **bottom-up**:

1. **L7** — Does `curl https://api.example.com/health` return 200?
2. **L7 DNS** — Does `dig api.example.com` return the expected IP?
3. **L4** — Does `nc -zv api.example.com 443` connect?
4. **L3** — Does `ping <resolved-ip>` work? (ICMP may be blocked)
5. **L3 routing** — Does `ip route get <ip>` show a valid path?
6. **L2** — Is the interface UP? (`ip link show`)

Stop at the first layer that fails — that is where you investigate.

## Hands-on Lab

### Step 1 – Application layer: HTTP request

**Command:**

```bash
curl -sv --max-time 10 http://example.com/ 2>&1 | head -25
```

**Explanation:** `curl -v` shows the full HTTP conversation — request headers (L7) and TCP connection details (L4).

**Expected output:**

```text
* Connected to example.com (93.184.216.34) port 80
> GET / HTTP/1.1
> Host: example.com
< HTTP/1.1 200 OK
```

### Step 2 – Transport layer: inspect listening ports

**Command:**

```bash
ss -tlnp | head -15
```

**Explanation:** `ss` shows TCP sockets in LISTEN state with port numbers — pure Layer 4 visibility.

### Step 3 – Network layer: routing decision

**Command:**

```bash
ip route get 93.184.216.34
```

**Explanation:** Shows which interface, source IP, and gateway the kernel will use before any frame is built.

**Expected output:**

```text
93.184.216.34 via 10.0.1.1 dev eth0 src 10.0.1.42 uid 1000
```

### Step 4 – Data link layer: MAC and ARP table

**Command:**

```bash
ip link show eth0 | grep link/ether
ip neigh show
```

**Explanation:** Layer 2 uses MAC addresses. The **neighbor table** maps IP addresses to MAC addresses on the local segment.

### Step 5 – Capture encapsulation with tcpdump

**Command:**

```bash
sudo tcpdump -i any -c 5 -n 'host 93.184.216.34' &
sleep 1
curl -s --max-time 5 http://example.com/ > /dev/null
wait
```

**Explanation:** Captures packets showing IP addresses (L3), port numbers (L4), and TCP flags (L4) in one capture.

### Step 6 – Layer-by-layer connectivity test

**Command:**

```bash
TARGET="example.com"
TARGET_IP=$(dig +short "$TARGET" | head -1)

echo "=== Layer 7: HTTP ==="
curl -s -o /dev/null -w "HTTP status: %{http_code}\n" "http://${TARGET}/"

echo "=== Layer 7: DNS ==="
echo "Resolved: ${TARGET} -> ${TARGET_IP}"

echo "=== Layer 4: TCP ==="
nc -zv -w 3 "$TARGET" 80 2>&1

echo "=== Layer 3: ICMP ==="
ping -c 2 -q "$TARGET_IP" 2>&1 | tail -1

echo "=== Layer 3: Route ==="
ip route get "$TARGET_IP"
```

**Explanation:** Systematically tests each layer to the same destination. When a step fails, you have isolated the problem layer.

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

| Command | OSI Layer | Description |
|---------|-----------|-------------|
| `curl -v URL` | L7 | Verbose HTTP with connection details |
| `dig domain` | L7 | DNS resolution |
| `openssl s_client -connect host:443` | L6/L7 | TLS handshake inspection |
| `ss -tuln` | L4 | Socket and port listing |
| `nc -zv host port` | L4 | TCP port connectivity test |
| `ping host` | L3 | ICMP echo (IP reachability) |
| `traceroute host` | L3 | Route path discovery |
| `ip route show` | L3 | Kernel routing table |
| `ip neigh show` | L2/L3 | ARP/neighbor cache |
| `tcpdump -i iface` | L2–L7 | Packet capture and decode |

### Layer-aware health check function

```bash
#!/usr/bin/env bash
# layered-check.sh — test connectivity at L3, L4, and L7
set -euo pipefail

HOST="${1:?Usage: layered-check.sh <hostname> [port]}"
PORT="${2:-443}"

IP=$(dig +short "$HOST" | grep -E '^[0-9.]+$' | head -1)
[[ -z "$IP" ]] && { echo "FAIL L7/DNS: cannot resolve $HOST"; exit 1; }
echo "OK   L7/DNS: $HOST -> $IP"

nc -zv -w 3 "$HOST" "$PORT" &>/dev/null && echo "OK   L4/TCP: $HOST:$PORT open" || \
  { echo "FAIL L4/TCP: $HOST:$PORT closed"; exit 1; }

HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "https://${HOST}/" 2>/dev/null || echo "000")
[[ "$HTTP_CODE" =~ ^[23] ]] && echo "OK   L7/HTTP: $HTTP_CODE" || echo "WARN L7/HTTP: $HTTP_CODE"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Memorizing layers without understanding PDUs"
    Interviewers ask "What happens at Layer 4?" — you must explain that TCP adds port numbers and sequence tracking, producing a **segment** that becomes the payload of an IP **packet**.

!!! warning "Assuming one tool fixes all layers"
    `curl` failing tells you Layer 7 has a problem — but the root cause may be Layer 3 (no route) or Layer 4 (port blocked). Always drill down one layer at a time.

!!! warning "Ignoring that routers re-encapsulate at Layer 2"
    IP addresses stay constant end-to-end, but MAC addresses change at every router hop. ARP is local-only.

!!! warning "Choosing the wrong load balancer type"
    An AWS NLB is Layer 4 (TCP). An ALB is Layer 7 (HTTP). Wrong choice breaks sticky sessions, WebSockets, or gRPC.

## Best Practices

!!! tip "Start troubleshooting at the layer where symptoms appear"
    A 502 Bad Gateway is Layer 7 — start with `curl` and upstream logs, not `tcpdump`. "No route to host" is Layer 3 — start with `ip route`.

!!! tip "Document which layer each monitoring check covers"
    HTTP health checks = L7. TCP port checks = L4. Ping monitors = L3. A green L7 dashboard does not guarantee L4/L3 health for all clients.

!!! tip "Use tcpdump when layers disagree"
    If `curl` fails but `nc` succeeds, something at Layer 7 is wrong. If `nc` fails but `ping` works, suspect a firewall blocking that port.

!!! tip "Learn the Linux network stack as one integrated system"
    The [Linux track](../linux/index.md) covers `ss`, `ip`, and `iptables` in OS context. This series explains *why* those tools map to specific layers.

## Troubleshooting

| Symptom | Likely Layer | First Tool | Common Cause |
|---------|-------------|------------|--------------|
| HTTP 502/503/504 | L7 | `curl -v` | Upstream app down, proxy misconfig |
| DNS resolution failure | L7 | `dig +trace` | Wrong nameserver, stale cache, NXDOMAIN |
| Connection refused | L4 | `nc -zv`, `ss -tlnp` | Service not listening on that port |
| Connection timed out | L4/L3 | `nc -zv`, check firewall | Security group, iptables, routing black hole |
| No route to host | L3 | `ip route get IP` | Missing route or gateway |
| Network unreachable | L3 | `ip route show default` | No default gateway configured |
| Interface DOWN | L2 | `ip link show` | Disabled NIC, unplugged cable, ENI detached |
| TLS certificate error | L6/L7 | `openssl s_client` | Expired cert, wrong hostname, untrusted CA |

## Summary

- The **OSI model** has 7 layers; the **TCP/IP model** has 4 — both describe the same process with different granularity
- **Encapsulation** adds headers as data descends the stack; **decapsulation** strips them on receive
- PDUs: **segment/datagram** (L4), **packet** (L3), **frame** (L2), **bits** (L1)
- DevOps tools map to specific layers — use the right tool for the layer where failure occurs
- Layered troubleshooting (top-down or bottom-up) is the most reliable connectivity debug methodology

## Interview Questions

1. Name the seven OSI layers from top to bottom.
2. How does the TCP/IP four-layer model map to the OSI model?
3. Explain encapsulation and decapsulation with an HTTP request example.
4. What is a PDU, and what are the PDUs at Layers 2, 3, and 4?
5. At which layer does a router operate? A switch? A firewall?
6. What layer does `curl` operate at? What about `ping`? What about `tcpdump`?
7. Why do MAC addresses change at each router hop but IP addresses do not?
8. Describe a top-down troubleshooting approach for "website not loading."
9. What is the difference between the Presentation layer and the Application layer?
10. Why might all layers pass individually but the application still fail?

??? tip "Sample Answers (Questions 3, 5, and 8)"

    **Q3 — Encapsulation example:** When curl sends `GET / HTTP/1.1`, TCP adds a header with ports and sequence numbers (segment, L4). IP adds source and destination IP addresses (packet, L3). Ethernet adds source and destination MAC addresses (frame, L2). The NIC converts the frame to bits (L1). On the server, each layer strips its header — decapsulation.

    **Q5 — Router, switch, firewall layers:** A switch operates at Layer 2 — forwards frames by MAC within a broadcast domain. A router operates at Layer 3 — forwards packets between networks using routing tables. A firewall typically operates at Layers 3–4 (filtering by IP, port, protocol) and optionally Layer 7 (WAF).

    **Q8 — Top-down troubleshooting:** Start at L7 with `curl -v`. Check DNS with `dig`. Test L4 with `nc -zv`. Test L3 with `ping` and `ip route get`. Check L2 with `ip link show`. Stop at the first failing layer.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Introduction to Networking](introduction-to-networking.md) *(previous in Module 1)*
- [IP Addressing and Subnetting](ip-addressing-and-subnetting.md) *(next in Module 1)*
- [Introduction to Linux](../linux/introduction-to-linux.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [ISO/IEC 7498-1 – OSI Basic Reference Model](https://www.iso.org/standard/20269.html)
- [RFC 1122 – Requirements for Internet Hosts](https://www.rfc-editor.org/rfc/rfc1122)
- [Linux network stack overview – kernel.org](https://docs.kernel.org/networking/index.html)
- [Wireshark OSI layer display filters](https://www.wireshark.org/docs/dfref/)
- [REBASH Academy – Networking Overview](index.md)
