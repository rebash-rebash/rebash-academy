---
title: "TCP/IP Model"
description: "Map the four-layer TCP/IP Internet model to OSI, place real protocols, and prove the stack with ss and curl -v on Ubuntu."
difficulty: beginner
estimated_time: "45–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: networking
technology: networking
module: "Module 3 · TCP/IP Model"
tags:
  - networking
  - tcp-ip
  - protocols
  - internet
prerequisites:
  - networking/osi-model
next:
  - networking/ip-addressing
related:
  - networking/tcp-and-udp-deep-dive
  - networking/dns-fundamentals
  - interview/networking
interview: interview/networking
comments: false
---

# TCP/IP Model

## Overview

The Internet does not run on seven OSI layers as a strict implementation. It runs on the **TCP/IP model** (also called the Internet protocol suite): a practical four-layer stack — **Link**, **Internet**, **Transport**, and **Application**. Ethernet and Wi‑Fi live at Link. Internet Protocol (IP) and Internet Control Message Protocol (ICMP) live at Internet. Transmission Control Protocol (TCP) and User Datagram Protocol (UDP) live at Transport. Hypertext Transfer Protocol (HTTP), Domain Name System (DNS), and Secure Shell (SSH) live at Application.

Engineers still use OSI numbers in conversation (“Layer 4 load balancer”) while configuring TCP/IP protocols on real hosts. You need both: OSI for shared vocabulary, TCP/IP for what is deployed. On a Linux VM you can see the stack in action: `ip` and ARP-related neighbours for Link/Internet behaviour, `ss -tuln` for Transport sockets, and `curl -v` for an Application request that rides on TCP and IP.

In Cloud and DevOps work, almost every design diagram is a TCP/IP story: subnet routes (Internet layer), security groups on ports (Transport), and HTTPS APIs (Application). Containers and Kubernetes add virtual links, but the four layers remain. If you mis-place a protocol — for example treating DNS as “only Layer 3” — you will pick the wrong debug tool.

This is **Tutorial 3** in **Module 3: TCP/IP Model** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series. It is written for Cloud, DevOps, Site Reliability Engineering (SRE), and platform engineers. By the end, you will map OSI to TCP/IP with concrete protocol examples and save socket plus HTTP evidence.

## Prerequisites

- [OSI Model](osi-model.md)
- A **practice Ubuntu 22.04/24.04 VM** with outbound HTTPS allowed if possible
- Tools: `ip`, `ss`, `curl`, `ping`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Name the four TCP/IP layers and the job of each
- [ ] Map TCP/IP layers to OSI layers with a clear table
- [ ] Place common protocols (Ethernet, IP, TCP/UDP, HTTP/DNS) on the correct TCP/IP layer
- [ ] Trace an HTTPS request through the stack in plain language
- [ ] Collect Transport and Application evidence with `ss -tuln` and `curl -v`

## Architecture

The diagram maps the four TCP/IP layers to the seven OSI layers and shows where familiar protocols sit.

![TCP/IP model mapped to OSI](../assets/excalidraw/tcp-ip-model.svg)

## Theory

### What it is

The **TCP/IP model** describes the protocol stack used on the Internet. Names vary slightly in textbooks (some say Network Access instead of Link; some say Host-to-Host instead of Transport). This course uses:

| TCP/IP layer | Job | Typical protocols |
|--------------|-----|-------------------|
| Application | User services and APIs | HTTP/HTTPS, DNS, SSH, TLS (as used by apps) |
| Transport | Process-to-process delivery | TCP, UDP |
| Internet | Host-to-host logical addressing / routing | IPv4, IPv6, ICMP |
| Link | Local network delivery | Ethernet, Wi‑Fi, ARP (IPv4 neighbour mapping) |

### Why it matters

Packet flows, security groups, network policies, and service meshes are easier when you know which layer you are changing. Opening port 443 in a cloud security group is a Transport rule. Adding a route to `10.0.0.0/8` is an Internet-layer rule. Rotating a TLS certificate is Application-layer work (with Transport underneath). Mixing those layers in a change ticket causes the wrong team to be paged.

### How it works

1. **Application** creates a request (for example HTTP GET).
2. **Transport** (usually TCP) provides ports and, for TCP, reliable byte streams.
3. **Internet** (IP) routes packets hop by hop toward the destination IP.
4. **Link** delivers frames to the next hop on the local network.
5. On the receiver, the path reverses up the stack to the listening application.

```bash
ss -tuln
curl -v --max-time 8 -o /dev/null https://example.com
```

### Key concepts and comparisons

| OSI layers (approx.) | TCP/IP layer | Memory hook |
|----------------------|--------------|-------------|
| 5–7 | Application | DNS, HTTP, SSH |
| 4 | Transport | TCP/UDP ports |
| 3 | Internet | IP addresses, ICMP |
| 1–2 | Link | MAC, Ethernet, ARP |

| Protocol | TCP/IP layer | OSI-oriented view |
|----------|--------------|-------------------|
| Ethernet | Link | L1–L2 |
| ARP | Link (support for IPv4 on Ethernet) | L2 |
| IPv4/IPv6 | Internet | L3 |
| ICMP | Internet | L3 |
| TCP/UDP | Transport | L4 |
| HTTP/DNS/SSH | Application | L7 (mostly) |

### Common pitfalls

- Believing TCP/IP “replaced” OSI so layer numbers no longer matter — cloud UIs still use L4/L7.
- Placing TLS only in one rigid layer — discuss it as Application security over TCP.
- Forgetting that UDP applications (DNS, QUIC-related stacks) still sit on Transport.
- Debugging HTTP before confirming TCP reachability to the port.
- Using `ifconfig`/`netstat` instead of `ip`/`ss` on modern Ubuntu.

## Hands-on Lab

### Objective

Build an OSI↔TCP/IP mapping artefact with concrete protocol examples, then capture Transport sockets (`ss -tuln`) and Application evidence (`curl -v`) under `~/rebash-networking/lab03`.

### Prerequisites

- Ubuntu 22.04/24.04
- `iproute2`, `curl`, `iputils-ping`
- Optional: `dnsutils` for `dig`

### Lab environment

Workspace: `~/rebash-networking/lab03`

```bash
mkdir -p ~/rebash-networking/lab03 && cd ~/rebash-networking/lab03
set -euo pipefail
hostname | tee hostname.txt
command -v ss curl ip | tee tools-present.txt
```

**Expected output:** `tools-present.txt` shows `ss`, `curl`, and `ip`.

### Real-world scenario

A new engineer asks whether “security groups are Layer 3 or Layer 4.” You produce a one-page mapping of OSI to TCP/IP with protocol examples, then prove on a lab VM that Transport sockets and an HTTPS Application request can be evidenced with standard tools — the same proof style used in production change tickets.

### Step-by-step tasks

#### Task 1 – Write the OSI↔TCP/IP mapping artefact

```bash
cd ~/rebash-networking/lab03
set -euo pipefail

cat > osi-tcpip-map.txt << 'EOF'
TCP/IP layer | OSI layers (approx) | Protocols (examples)        | Linux evidence idea
Application  | 5–7                 | HTTP, HTTPS, DNS, SSH       | curl -v, dig
Transport    | 4                   | TCP, UDP                    | ss -tuln
Internet     | 3                   | IPv4, IPv6, ICMP            | ip addr, ping, ip route
Link         | 1–2                 | Ethernet, Wi-Fi, ARP        | ip -br link, ip neigh

Concrete walkthrough for HTTPS GET example.com:
1. Application: HTTP request inside TLS
2. Transport: TCP destination port 443
3. Internet: packets to the resolved A/AAAA address
4. Link: frames to the local gateway MAC
EOF

cat osi-tcpip-map.txt
grep -E 'Application|Transport|Internet|Link' osi-tcpip-map.txt
```

**Expected output:** `osi-tcpip-map.txt` contains all four TCP/IP layer names and the HTTPS walkthrough.

#### Task 2 – Transport evidence with `ss -tuln`

```bash
cd ~/rebash-networking/lab03
set -euo pipefail

ss -tuln | tee ss-tuln.txt
ss -s | tee ss-summary.txt

# Count listening TCP lines (header excluded carefully)
awk 'NR>1 && /tcp/ && /LISTEN/ {c++} END{print c+0}' ss-tuln.txt | tee ss-listen-tcp-count.txt

# Neighbour / link support for the Internet layer on LAN
ip neigh show | tee ip-neigh.txt || true
ip -br link | tee ip-br-link.txt
```

**Expected output:** `ss-tuln.txt` exists; `ss-listen-tcp-count.txt` contains a number (zero is possible on a minimal VM).

#### Task 3 – Application evidence with `curl -v` and pack

```bash
cd ~/rebash-networking/lab03
set -euo pipefail

curl -v --max-time 10 -o /dev/null https://example.com 2>curl-verbose.txt || true
test -s curl-verbose.txt

# Pull a few useful lines if present
grep -Ei 'Connected to|ALPN|HTTP/|SSL connection|Trying|Could not' curl-verbose.txt \
  | tee curl-highlights.txt || cp curl-verbose.txt curl-highlights.txt

# Internet-layer companion check
ping -c 2 -W 2 127.0.0.1 2>&1 | tee ping-localhost.txt
ip route show default 2>&1 | tee default-route.txt || true

tar -czf tcpip-stack-evidence.tgz \
  hostname.txt tools-present.txt osi-tcpip-map.txt \
  ss-tuln.txt ss-summary.txt ss-listen-tcp-count.txt \
  ip-neigh.txt ip-br-link.txt \
  curl-verbose.txt curl-highlights.txt \
  ping-localhost.txt default-route.txt
ls -l tcpip-stack-evidence.tgz | tee evidence-ls.txt
test -s tcpip-stack-evidence.tgz
```

**Expected output:** `curl-verbose.txt` is non-empty; `tcpip-stack-evidence.tgz` is created and non-empty.

### Validation steps

- [ ] `osi-tcpip-map.txt` maps all four TCP/IP layers to OSI ranges and protocols
- [ ] `ss -tuln` output saved
- [ ] `curl -v` output saved
- [ ] Evidence tarball exists under `~/rebash-networking/lab03`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `curl: (6) Could not resolve host` | DNS / Application dependency | Fix resolvers; still keep verbose log as evidence |
| `curl: (7) Failed to connect` | Transport/Internet path | Check route, security groups, `ss` on server side |
| Empty `ss` LISTEN list | Minimal host | Valid — count can be 0; note it in the ticket |
| Permission noise in neigh table | Normal | `ip neigh` still useful without sudo on many systems |

### Challenge exercise

Create executable script `~/rebash-networking/lab03/stack-probe.sh` that: (1) writes timestamped `ss -tuln` to `probe-ss.txt`, (2) runs `curl -v --max-time 8 -o /dev/null https://example.com` saving stderr to `probe-curl.txt`, (3) appends a one-line summary `TCPIP_PROBE_OK=yes` or `TCPIP_PROBE_OK=no` to `probe-summary.env` depending on whether `curl` exit code was 0. Run it once. Working artefact required — not a markdown notes file.

### Learning outcomes

- Mapped OSI vocabulary onto the deployed TCP/IP stack
- Placed everyday protocols on the correct layer
- Evidenced Transport and Application behaviour on Linux
- Practised the HTTPS-through-the-stack story used in design reviews

### Cleanup

```bash
cd ~/rebash-networking/lab03
set -euo pipefail
# No persistent routes or firewall changes in the main lab
ls -la
# Optional: rm -f *.txt *.env *.tgz
```

## Validation

- [ ] Lab finished under `~/rebash-networking/lab03/` with `tcpip-stack-evidence.tgz`
- [ ] You can list four TCP/IP layers and map them to OSI
- [ ] You can walk an HTTPS request down and up the stack
- [ ] You prefer `ss` over `netstat` on modern Ubuntu

## Code Walkthrough

A practical stack check for TCP/IP:

1. **Link** — `ip -br link`, `ip neigh`  
2. **Internet** — `ip addr`, `ip route`, `ping`  
3. **Transport** — `ss -tuln`, port connectivity  
4. **Application** — `curl -v`, `dig`, client error messages  

Use the mapping file from Task 1 whenever someone mixes OSI numbers with protocol names.

## Security Considerations

- Verbose HTTP logs may include cookies or tokens — redact before sharing  
- Opening Transport ports in cloud security groups widens attack surface — least privilege  
- Prefer TLS (HTTPS) for Application traffic on untrusted networks  
- Do not disable IP-level filtering to “simplify” demos on shared VMs  
- Understand that Link-level access on a LAN can expose ARP spoofing risks on untrusted segments  

## Common Mistakes

!!! warning "Treating TCP/IP and OSI as rivals"
    Production uses both. **Fix:** map them with a table; use OSI numbers when the product UI does.

!!! warning "Calling security groups ‘Layer 7 firewalls’ by default"
    Classic security groups/NACLs are mostly L3/L4. **Fix:** reserve L7 for WAF/proxy rules that read HTTP.

!!! warning "Skipping Transport checks"
    Application retries hide connection failures. **Fix:** prove the TCP port before tuning HTTP timeouts.

!!! warning "Placing IP in the Application layer"
    IP addressing is Internet layer. **Fix:** keep addresses/routes separate from HTTP paths in designs.

## Best Practices

- Keep an OSI↔TCP/IP cheat sheet in the team wiki  
- Name the layer in every network change ticket  
- Use `curl -v` (or equivalent) when explaining TLS/HTTP issues  
- Standardise on `ip`/`ss` in runbooks  
- Teach new joiners with one HTTPS trace through all four layers  

## Troubleshooting

| Symptom | Likely layer | Fix focus |
|---------|--------------|-----------|
| No carrier / NIC DOWN | Link | Attach NIC; check `ip link` |
| No route to host | Internet | Routes, gateways, VPC tables |
| Connection refused | Transport | Process not listening; wrong port |
| Connection timed out | Internet/Transport | Firewall, path, wrong IP |
| HTTP 4xx/5xx after connect | Application | App/proxy logic, not basic IP |

## Summary

The TCP/IP model is the four-layer stack the Internet actually uses. Map it to OSI, place protocols correctly, and prove Transport and Application behaviour with `ss` and `curl -v`. Next, learn how hosts are numbered in [IP Addressing](ip-addressing.md).

## Interview Questions

**1. What are the four layers of the TCP/IP model, and what does each do?**

??? success "Reveal answer"
    **Link** delivers frames on the local network. **Internet** handles logical addressing and routing with IP (and ICMP). **Transport** delivers data to processes with TCP or UDP ports. **Application** is where protocols such as HTTP, DNS, and SSH live. Together they describe real Internet communication.

**2. How do TCP/IP layers map to OSI layers?**

??? success "Reveal answer"
    Rough mapping: TCP/IP **Application** ≈ OSI 5–7, **Transport** ≈ OSI 4, **Internet** ≈ OSI 3, **Link** ≈ OSI 1–2. Exact textbook names vary, but this mapping is what interviewers expect for Cloud/DevOps roles.

**3. At which TCP/IP layer would you place Ethernet, IPv4, TCP, and HTTPS?**

??? success "Reveal answer"
    Ethernet → **Link**; IPv4 → **Internet**; TCP → **Transport**; HTTPS (HTTP over TLS) → **Application** (running on TCP). Mentioning TLS as protecting Application data over Transport earns extra credit.

**4. Walk through an HTTPS request from a VM to `example.com` using TCP/IP layers.**

??? success "Reveal answer"
    Application builds HTTP and uses TLS; Transport opens TCP to port 443; Internet sends IP packets to the resolved address; Link frames carry packets to the local gateway. The server reverses the path up to its web process. DNS is an Application protocol used before the HTTP request if a name must be resolved.

**5. Why do engineers still say “Layer 7 load balancer” if we deploy TCP/IP?**

??? success "Reveal answer"
    OSI numbers remain industry vocabulary. “Layer 7” means the balancer understands application protocols (HTTP), while “Layer 4” means TCP/UDP forwarding. The data plane is still TCP/IP; the label describes feature depth.

**6. Which command evidence would you attach to show Transport vs Application health?**

??? success "Reveal answer"
    Transport: `ss -tuln` (and connection attempts to a port). Application: `curl -v` or application logs/status codes. Together they show whether you failed before the app spoke HTTP or after.

**7. Is ICMP in the Transport layer? Why or why not?**

??? success "Reveal answer"
    **No.** ICMP is part of the **Internet** layer alongside IP. It carries control and error messages (including echo request/reply used by `ping`). It is not a process-port Transport protocol like TCP/UDP.

**8. How does this model help when debugging Kubernetes or cloud security groups?**

??? success "Reveal answer"
    Network policies and security groups often match on IP and ports (Internet + Transport). Ingress/HTTPRoutes act at Application. Knowing the layer prevents fixing the wrong object — for example editing an HTTP route when packets never reach the node IP.

## Related Tutorials

- [OSI Model](osi-model.md) *(previous)*
- [IP Addressing](ip-addressing.md) *(next)*
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- [DNS Fundamentals](dns-fundamentals.md)

## References

- [RFC 1122](https://www.rfc-editor.org/rfc/rfc1122) — Requirements for Internet Hosts — Communication Layers  
- [RFC 793](https://www.rfc-editor.org/rfc/rfc793) — Transmission Control Protocol  
- [RFC 791](https://www.rfc-editor.org/rfc/rfc791) — Internet Protocol  
- [`ss(8)`](https://manpages.ubuntu.com/manpages/jammy/en/man8/ss.8.html) — Ubuntu man-page  
- Track index: [Networking for Cloud & DevOps Engineers](index.md)
