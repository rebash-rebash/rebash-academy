---
title: VPN and Tunneling Basics
description: Understand site-to-site and remote-access VPNs, IPsec and WireGuard tunnels, TLS VPNs, and hybrid cloud connectivity patterns for secure network extension.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - vpn
  - ipsec
  - wireguard
  - tunneling
  - openvpn
  - site-to-site
prerequisites:
  - Complete [NAT and Port Forwarding](nat-and-port-forwarding.md) and [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)
  - Understanding of routing and firewalls from Module 2–4 tutorials
  - Linux VM with sudo access for WireGuard lab
comments: false
---

# VPN and Tunneling Basics

## Overview

A **VPN (Virtual Private Network)** creates an encrypted tunnel over an untrusted network (the internet), making remote hosts appear as if they are on the same private network. Enterprises use **site-to-site VPNs** to connect on-premises data centers to cloud VPCs; **remote-access VPNs** let employees reach internal tools from home; **mesh VPNs** like Tailscale connect distributed servers without manual route configuration.

**Tunneling** wraps one protocol inside another — IP packets inside encrypted UDP, Ethernet frames inside GRE. VPNs are the primary mechanism for **hybrid cloud** connectivity when dedicated links (Direct Connect, ExpressRoute) are not yet justified. Misconfigured VPNs cause subtle outages: one-way traffic, MTU black holes, and overlapping CIDR blocks with VPC peering.

This is **Tutorial 18** in **Module 6: Cloud & Advanced** of the REBASH Academy Networking series. It includes theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [NAT and Port Forwarding](nat-and-port-forwarding.md) — SNAT/DNAT and conntrack
- Completed [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) — VPC CIDR, route tables, IGW
- Familiarity with [Routing Fundamentals](routing-fundamentals.md) and [Firewalls and Access Control](firewalls-and-access-control.md)
- Linux VM with kernel WireGuard support (Ubuntu 22.04+ includes `wireguard` module)
- Optional: AWS account for VPN Gateway discussion

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Differentiate site-to-site, remote-access, and mesh VPN architectures
- [ ] Compare IPsec, WireGuard, OpenVPN, and TLS-based VPN approaches
- [ ] Configure a basic WireGuard point-to-point tunnel on Linux
- [ ] Describe AWS Site-to-Site VPN and Customer Gateway setup at a high level
- [ ] Troubleshoot VPN connectivity including MTU, routing, and phase 1/2 failures
- [ ] Choose between VPN, VPC peering, and dedicated connectivity for hybrid cloud

## Architecture Diagram

Site-to-site VPN connects on-premises networks to cloud VPCs over encrypted internet tunnels.

```d2
direction: right

OnPrem: "On-Premises 192.168.0.0/16" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        SRV: "App Servers"
        VPNC: "VPN Customer Gateway"
    }
    Internet: Internet {
        TUN: "Encrypted Tunnel\nIPsec / WireGuard"
    }
    Cloud: "AWS VPC 10.0.0.0/16" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        VPNGW: "VPN Gateway / TGW"
        EC2: "EC2 Instances"
    }
    OnPrem.SRV -> OnPrem.VPNC
    OnPrem.VPNC -> Internet.TUN
    Internet.TUN -> Cloud.VPNGW
    Cloud.VPNGW -> Cloud.EC2
```

## Theory

### VPN Types

| Type | Connects | Use case | Example |
|------|----------|----------|---------|
| **Site-to-site** | Two networks | Hybrid cloud, branch offices | On-prem ↔ AWS VPC |
| **Remote-access** | Individual user ↔ network | Work from home, contractor access | OpenVPN, WireGuard client |
| **Mesh / overlay** | Many nodes ↔ many nodes | Distributed infra, zero-trust | Tailscale, Nebula, Consul mesh |
| **SSL/TLS VPN** | Browser or client ↔ gateway | Web portal access, vendor VPN | Cisco AnyConnect, AWS Client VPN |

### Tunneling Concepts

A **tunnel** encapsulates packets:

1. Original packet (inner) destined for remote private network
2. VPN endpoint encrypts and wraps it in outer packet
3. Outer packet routed over internet to peer VPN endpoint
4. Peer decrypts, delivers inner packet to destination

The tunnel creates a **virtual interface** (e.g., `wg0`, `tun0`) with its own IP address. Routes direct traffic for remote CIDR blocks through this interface.

**Split tunnel vs full tunnel:**

- **Full tunnel** — all traffic routes through VPN (corporate inspection, IP masking)
- **Split tunnel** — only corporate CIDR routes through VPN; internet traffic exits locally (better performance, less VPN load)

### IPsec VPN

**IPsec** is the enterprise standard for site-to-site VPNs. Two phases:

**Phase 1 (IKE)** — establishes secure channel between VPN endpoints:

- Authentication (pre-shared key or certificates)
- Encryption and integrity algorithms (AES-256, SHA-256)
- Diffie-Hellman key exchange

**Phase 2 (IPsec SA)** — negotiates parameters for actual data traffic:

- Which subnets (interesting traffic) to encrypt
- PFS (Perfect Forward Secrecy) settings
- SPI and keys for ESP/AH encapsulation

AWS **Site-to-Site VPN** uses IPsec between your **Customer Gateway** (on-prem device or software) and **Virtual Private Gateway** or **Transit Gateway**.

Common IPsec issues:

- **Phase 1 failure** — mismatched pre-shared key, IKE version, or encryption parameters
- **Phase 2 failure** — mismatched subnet definitions (interesting traffic selectors)
- **One-way traffic** — missing return route or asymmetric routing
- **MTU issues** — IPsec overhead requires lower MTU (often 1400 or less)

### WireGuard

**WireGuard** is a modern VPN protocol built into the Linux kernel — simpler than IPsec, faster handshake, fixed crypto suite (Curve25519, ChaCha20, Poly1305).

Configuration uses `wg0.conf`:

```ini
[Interface]
PrivateKey = <server-private-key>
Address = 10.200.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.200.0.2/32, 192.168.50.0/24
```

Key properties:

- **Cryptokey routing** — `AllowedIPs` defines which destinations route through each peer
- **Roaming** — clients reconnect seamlessly when IP changes
- **Minimal attack surface** — ~4,000 lines of code vs OpenVPN's complexity

WireGuard is ideal for server-to-server mesh, remote admin access, and cloud instance interconnect.

### OpenVPN and TLS VPNs

**OpenVPN** uses TLS for key exchange and supports TCP or UDP transport. Mature, widely deployed, but heavier than WireGuard. Runs in userspace (unless using kernel modules).

**TLS/SSL VPNs** (AWS Client VPN, commercial products) authenticate users via SAML/OIDC and assign virtual IPs from a pool. Good for human remote access; less common for automated site-to-site.

### AWS VPN Components

| Component | Role |
|-----------|------|
| **Customer Gateway (CGW)** | Represents on-prem VPN endpoint (IP, BGP ASN) |
| **Virtual Private Gateway (VGW)** | VPN termination on VPC side |
| **Transit Gateway (TGW)** | Hub connecting multiple VPCs and VPNs |
| **Site-to-Site VPN Connection** | Two IPsec tunnels for redundancy |

Best practices:

- Always configure **both tunnels** for HA
- Use **BGP** for dynamic route propagation (preferred over static routes)
- Ensure **non-overlapping CIDR** between on-prem and VPC
- Set TCP MSS clamping or lower MTU on tunnel interfaces

### VPN vs Peering vs Direct Connect

| Option | Throughput | Latency | Cost | Best for |
|--------|------------|---------|------|----------|
| **Site-to-site VPN** | Up to 1.25 Gbps per tunnel | Variable (internet) | Low | Quick hybrid setup, backup link |
| **VPC Peering** | No bandwidth cap (same region) | Low | Low | Cloud-to-cloud, non-overlapping CIDR |
| **Direct Connect / ExpressRoute** | 1 Gbps – 100 Gbps | Consistent low | High | Production hybrid, compliance |

Use VPN for initial hybrid connectivity and disaster recovery backup; migrate to Direct Connect when bandwidth and SLA requirements grow.

### Security Considerations

- Rotate pre-shared keys and certificates on schedule
- Restrict VPN endpoint access to known peer IPs in firewall rules
- Use **certificate-based auth** over PSK in production
- Enable **dead peer detection (DPD)** for fast failover
- Log VPN events; alert on tunnel down
- Combine VPN with **zero-trust** — VPN grants network access, not implicit trust; still enforce application auth

## Hands-on Lab

Complete on Ubuntu 22.04+ with sudo. This lab creates a local WireGuard loopback-style tunnel using two network namespaces.

### Step 1 – Install WireGuard tools

**Command:**

```bash
sudo apt-get update && sudo apt-get install -y wireguard-tools
wg --version
```

**Explanation:** WireGuard userspace tools manage keys and interfaces. Kernel module loads automatically on supported systems.

**Expected output:**

```text
wireguard-tools v1.x
```

### Step 2 – Generate key pairs

**Command:**

```bash
mkdir -p ~/wg-lab && cd ~/wg-lab
umask 077
wg genkey | tee server.key | wg pubkey > server.pub
wg genkey | tee client.key | wg pubkey > client.pub
echo "Server pub: $(cat server.pub)"
echo "Client pub: $(cat client.pub)"
```

**Explanation:** WireGuard uses Curve25519 key pairs. Private keys must be protected (`umask 077`).

### Step 3 – Create server configuration

**Command:**

```bash
SERVER_PRIV=$(cat server.key)
CLIENT_PUB=$(cat client.pub)
sudo tee /etc/wireguard/wg0.conf <<EOF
[Interface]
PrivateKey = ${SERVER_PRIV}
Address = 10.200.0.1/24
ListenPort = 51820

[Peer]
PublicKey = ${CLIENT_PUB}
AllowedIPs = 10.200.0.2/32
EOF
sudo chmod 600 /etc/wireguard/wg0.conf
```

**Explanation:** Server listens on UDP 51820. `AllowedIPs` for the peer defines which source IPs are accepted from that peer.

### Step 4 – Create client configuration

**Command:**

```bash
CLIENT_PRIV=$(cat client.key)
SERVER_PUB=$(cat server.pub)
SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || echo "127.0.0.1")
tee ~/wg-lab/client.conf <<EOF
[Interface]
PrivateKey = ${CLIENT_PRIV}
Address = 10.200.0.2/24

[Peer]
PublicKey = ${SERVER_PUB}
Endpoint = ${SERVER_IP}:51820
AllowedIPs = 10.200.0.0/24
PersistentKeepalive = 25
EOF
```

**Explanation:** Client routes `10.200.0.0/24` through the tunnel. `PersistentKeepalive` maintains NAT mappings for clients behind home routers.

### Step 5 – Start WireGuard and verify

**Command:**

```bash
sudo wg-quick up wg0
sudo wg show
ip addr show wg0
```

**Explanation:** `wg-quick` creates the interface, sets routes, and configures iptables if specified. `wg show` displays peer handshake status.

**Expected output:**

```text
interface: wg0
  public key: ...
  listening port: 51820

peer: ...
  allowed ips: 10.200.0.2/32
```

### Step 6 – Test tunnel connectivity (same-host lab)

For same-machine testing with network namespaces:

```bash
sudo ip netns add wgclient
sudo ip link add veth0 type veth peer name veth1
sudo ip link set veth1 netns wgclient
sudo ip addr add 192.168.99.1/24 dev veth0
sudo ip link set veth0 up
sudo ip netns exec wgclient ip addr add 192.168.99.2/24 dev veth1
sudo ip netns exec wgclient ip link set veth1 up
ping -c 2 192.168.99.2
```

**Explanation:** Namespaces simulate separate hosts. In production, run client.conf on a remote machine and ping `10.200.0.1` through the tunnel.

### Step 7 – Inspect routing and firewall

**Command:**

```bash
ip route | grep wg0
sudo ufw status 2>/dev/null | grep 51820 || echo "Ensure UDP 51820 allowed if UFW enabled"
```

**Explanation:** VPN traffic must pass through firewalls on UDP port 51820 (WireGuard default). Missing firewall rule is a common tunnel failure cause.

### Step 8 – Teardown

**Command:**

```bash
sudo wg-quick down wg0
sudo ip netns del wgclient 2>/dev/null
sudo ip link del veth0 2>/dev/null
rm -rf ~/wg-lab
sudo rm /etc/wireguard/wg0.conf
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `wg genkey` | Generate private key | `wg genkey \| tee private.key` |
| `wg pubkey` | Derive public key | `cat private.key \| wg pubkey` |
| `wg-quick up` | Start WireGuard interface | `sudo wg-quick up wg0` |
| `wg show` | Show interface and peers | `sudo wg show` |
| `ip route` | Verify tunnel routes | `ip route \| grep wg0` |
| `strongswan` | IPsec daemon (common) | `sudo ipsec statusall` |

!!! tip "IPsec MTU"
    Set tunnel interface MTU to 1400–1420 or enable TCP MSS clamping — encryption overhead causes fragmentation black holes on VPN paths.

## Common Mistakes

!!! warning "Overlapping CIDR blocks"
    On-prem `10.0.0.0/16` and VPC `10.0.0.0/16` cannot route over VPN — addresses are ambiguous. Redesign CIDR before connecting.

!!! warning "Missing return routes"
    Traffic reaches cloud but responses take default internet route instead of VPN tunnel. Configure routes on both sides for remote CIDR blocks.

!!! warning "Blocking UDP 500/4500 or ESP"
    IPsec requires UDP 500 (IKE), UDP 4500 (NAT-T), and protocol 50 (ESP). Corporate firewalls often block these.

!!! warning "Ignoring MTU overhead"
    Encryption adds bytes per packet. Standard 1500 MTU causes silent failures. Set tunnel MTU to 1400–1420 and enable MSS clamping.

## Best Practices

!!! tip "Always configure redundant tunnels"
    AWS provides two VPN tunnels per connection. Configure both on-prem endpoints for automatic failover.

!!! tip "Prefer BGP over static routes"
    BGP propagates route changes automatically when subnets are added. Static routes require manual updates and cause drift.

!!! tip "Use WireGuard for server mesh; IPsec for enterprise edge"
    Match protocol to use case — WireGuard for DevOps simplicity; IPsec for vendor-supported site-to-site with existing appliances.

!!! tip "Monitor tunnel state"
    Alert on VPN tunnel down events. AWS CloudWatch `TunnelState` metric; WireGuard `wg show` latest handshake timestamp.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Phase 1 IKE failure | PSK/algorithm mismatch | Compare IKE proposals on both sides; check CGW config |
| Phase 2 failure | Subnet selector mismatch | Align interesting traffic / proxy IDs |
| Tunnel up, no traffic | Missing route | Add routes for remote CIDR via tunnel interface |
| One-way traffic | Asymmetric routing | Ensure return path uses VPN; check NAT rules |
| Intermittent drops | DPD timeout / internet instability | Tune DPD intervals; verify both tunnels configured |
| WireGuard no handshake | Firewall blocks UDP 51820 | Open port; verify Endpoint IP and key exchange |
| Slow throughput | MTU fragmentation | Lower MTU; enable MSS clamping |

## Summary

- **VPNs** encrypt traffic over untrusted networks, connecting sites or remote users to private infrastructure
- **Site-to-site** VPNs link networks (on-prem ↔ cloud); **remote-access** VPNs link users; **mesh** VPNs connect many nodes
- **IPsec** dominates enterprise site-to-site (Phase 1 IKE + Phase 2 SA); **WireGuard** offers simpler modern server-to-server tunnels
- AWS **Site-to-Site VPN** uses Customer Gateway + VPN Gateway/TGW with dual tunnels for HA
- Debug VPNs with **phase logs**, **routing tables**, **MTU testing**, and **packet capture**
- Choose VPN for quick hybrid connectivity; **Direct Connect** when bandwidth and SLA demand it

## Interview Questions

1. What is the difference between site-to-site and remote-access VPN?
2. Explain IPsec Phase 1 and Phase 2 negotiations.
3. Why does WireGuard require `AllowedIPs` configuration?
4. How would you connect an on-premises network to an AWS VPC?
5. What causes VPN tunnel "up" but no traffic flows?
6. Compare VPN, VPC peering, and Direct Connect for hybrid cloud.
7. What is split tunneling, and when would you use it?
8. Why do VPN tunnels often require reduced MTU?
9. How do you achieve high availability with AWS Site-to-Site VPN?
10. What security risks remain even when users connect via VPN?

??? tip "Sample Answers (Questions 2, 5, and 9)"

    **Q2 — IPsec phases:** Phase 1 (IKE) establishes a secure management channel between VPN endpoints — authenticates peers (PSK or certificates), negotiates encryption/integrity algorithms, and performs key exchange. Phase 2 creates IPsec Security Associations for actual data traffic — defines which subnets to encrypt (interesting traffic), sets up ESP keys, and enables PFS. Phase 1 must succeed before Phase 2 can negotiate.

    **Q5 — Tunnel up, no traffic:** The IPsec SA exists but routing is wrong. Common causes: missing route to remote CIDR via tunnel interface on one side, overlapping CIDR blocks, security group/NACL blocking traffic after decryption, or NAT interfering with interesting traffic selectors. Verify with ping/traceroute across tunnel and check route tables on both endpoints.

    **Q9 — AWS VPN HA:** AWS provides two separate VPN tunnels per connection, terminating on different public IPs. Configure your Customer Gateway with both tunnel endpoints and enable BGP (or static routes) for both. If one tunnel fails, traffic fails over to the second. Also deploy redundant CGW devices on-prem for device-level HA.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [NAT and Port Forwarding](nat-and-port-forwarding.md) *(previous in Module 6)*
- [Network Security Hardening](network-security-hardening.md) *(next in Module 6)*
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)
- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Linux – Category Overview](../linux/index.md)
- [Docker – Category Overview](../docker/index.md)

## References

- [WireGuard whitepaper and documentation](https://www.wireguard.com/)
- [RFC 4301 — Security Architecture for IP](https://www.rfc-editor.org/rfc/rfc4301)
- [AWS Site-to-Site VPN documentation](https://docs.aws.amazon.com/vpn/latest/s2svpn/)
- [StrongSwan IPsec documentation](https://www.strongswan.org/docs.html)
- [Tailscale — How WireGuard works](https://tailscale.com/blog/how-wireguard-works)
- [NIST SP 800-77 — Guide to IPsec VPNs](https://csrc.nist.gov/publications/detail/sp/800-77/rev-1/final)
