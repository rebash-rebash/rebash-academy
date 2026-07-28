---
title: NAT and Port Forwarding
description: Understand SNAT, DNAT, and PAT with iptables/nftables, configure cloud NAT gateways, and debug translation failures in VPC and home-lab environments.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - nat
  - snat
  - dnat
  - port-forwarding
  - iptables
  - conntrack
prerequisites:
  - Complete [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) or understand public/private subnets
  - Familiarity with [Firewalls and Access Control](firewalls-and-access-control.md) and conntrack basics
  - Linux VM with sudo access for iptables/nftables labs
comments: false
---

# NAT and Port Forwarding

## Overview

**Network Address Translation (NAT)** modifies IP addresses and ports in packet headers as traffic crosses a boundary. It is everywhere: your home router translates private `192.168.x.x` addresses to a single public IP; cloud **NAT gateways** let private EC2 instances reach the internet; **port forwarding** (DNAT) exposes internal services to external clients. Without NAT, IPv4 address exhaustion would have halted internet growth decades ago.

NAT breaks end-to-end connectivity principles — hosts behind NAT are not directly reachable unless you explicitly forward ports. It complicates debugging: logs show the NAT device's IP, not the original client; protocols embedding IP addresses (FTP, SIP) require **ALG** helpers. This tutorial explains SNAT, DNAT, PAT, Linux netfilter NAT rules, cloud NAT gateways, and how to troubleshoot translation failures.

This is **Tutorial 17** in **Module 6: Cloud & Advanced** of the REBASH Academy Networking series. It includes theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) — public vs private subnets, IGW, route tables
- Understanding of IP addressing and routing from [IP Addressing and Subnetting](ip-addressing-and-subnetting.md)
- Familiarity with iptables/nftables concepts from [Firewalls and Access Control](firewalls-and-access-control.md)
- Linux VM with `sudo`; optional AWS account for NAT gateway discussion

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain SNAT, DNAT, and PAT (NAPT) and when each applies
- [ ] Configure basic NAT rules with iptables/nftables on Linux
- [ ] Describe how cloud NAT gateways provide outbound internet for private subnets
- [ ] Set up port forwarding (DNAT) to expose internal services
- [ ] Debug NAT failures using conntrack and packet capture
- [ ] Identify applications and protocols that break behind NAT

## Architecture

NAT sits at the boundary between private and public address spaces.

```d2
direction: down

Private: "Private Network 10.0.11.0/24" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        APP: "App Server\n10.0.11.50"
        DB: "Database\n10.0.11.60"
    }
    NATDevice: "NAT Gateway / Router" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        SNAT: "SNAT\n10.0.11.x → public IP"
        DNAT: "DNAT\npublic:8080 → 10.0.11.50:80"
    }
    Internet: Internet {
        EXT: "External Clients"
        SVC: "External APIs"
    }
    Private.APP -> NATDevice.SNAT: outbound
    NATDevice.SNAT -> Internet.SVC
    Internet.EXT -> NATDevice.DNAT: "inbound :8080"
    NATDevice.DNAT -> Private.APP
    Private.DB -> Internet.EXT: "no direct inbound" {
      style.stroke-dash: 3
    }
```

## Theory

### Why NAT Exists

IPv4 provides ~3.7 billion usable addresses — insufficient for every device globally. **RFC 1918** private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) are reusable behind NAT. Many organizations and home networks share the same private ranges because NAT isolates them.

NAT also provides **security by obscurity** (not a substitute for firewalls): internal hosts are not directly reachable from the internet unless DNAT rules exist.

### SNAT vs DNAT vs PAT

| Type | Direction | Translation | Example |
|------|-----------|-------------|---------|
| **SNAT** | Outbound | Change source IP (and maybe port) | Private server → internet via NAT GW public IP |
| **DNAT** | Inbound | Change destination IP/port | Public IP:443 → internal 10.0.1.5:8443 |
| **PAT/NAPT** | Both | Many private IPs share one public IP using port mapping | Home router: all LAN devices share WAN IP |

**Masquerade** is dynamic SNAT — the NAT device uses its outgoing interface IP automatically (common on Linux routers):

```bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

### Connection Tracking (conntrack)

NAT depends on **conntrack** — the kernel tracks each connection and reverses translations for return packets. When a packet leaves with SNAT applied, conntrack remembers the mapping so inbound responses are translated back to the original private IP:port.

Inspect active translations:

```bash
sudo conntrack -L | head -20
sudo cat /proc/net/nf_conntrack | head -5
```

If conntrack table fills (`net.netfilter.nf_conntrack_max`), new connections fail — a common production incident on busy NAT instances.

### Linux iptables NAT

NAT rules live in the **`nat` table**:

- **PREROUTING** — DNAT before routing decision (incoming packets)
- **POSTROUTING** — SNAT after routing decision (outgoing packets)

**Enable IP forwarding** (required for NAT router):

```bash
sudo sysctl -w net.ipv4.ip_forward=1
# Persist: net.ipv4.ip_forward=1 in /etc/sysctl.d/
```

**SNAT example** — private subnet outbound via eth0:

```bash
iptables -t nat -A POSTROUTING -s 10.0.11.0/24 -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT
```

**DNAT port forward example** — expose internal web server:

```bash
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 \
  -j DNAT --to-destination 10.0.11.50:80
iptables -t nat -A POSTROUTING -d 10.0.11.50 -p tcp --dport 80 -j MASQUERADE
```

### nftables NAT

Modern systems prefer **nftables**:

```nft
table ip nat {
  chain prerouting {
    type nat hook prerouting priority dstnat;
    tcp dport 8080 dnat to 10.0.11.50:80
  }
  chain postrouting {
    type nat hook postrouting priority srcnat;
    oifname "eth0" masquerade
  }
}
```

### Cloud NAT Gateways

In AWS, a **NAT Gateway** lives in a **public subnet** with a route to the Internet Gateway. Private subnet route tables send `0.0.0.0/0` to the NAT Gateway (not the IGW directly).

Properties:

- **Outbound-only** — internet cannot initiate connections to private instances
- **Elastic IP** — SNAT uses the NAT GW's public IP
- **AZ-scoped** — deploy one NAT GW per AZ for HA (avoid cross-AZ NAT charges and SPOF)
- **Managed** — AWS handles scaling and patching; you pay per hour and per GB processed

Compare with **NAT instances** (self-managed EC2) — cheaper at scale but you maintain patching, scaling, and failover.

GCP **Cloud NAT** and Azure **NAT Gateway** provide equivalent managed outbound NAT for private subnets.

!!! tip "NAT vs IGW"
    Instances in **public subnets** with public IPs use the **Internet Gateway** directly — no SNAT needed. Instances in **private subnets** without public IPs require **NAT Gateway** for outbound internet (package updates, API calls).

### Port Forwarding Use Cases

**DNAT / port forwarding** maps external `public_ip:port` to internal `private_ip:port`:

- Home lab: router forwards external 2222 → internal SSH 22
- Kubernetes **NodePort** / **LoadBalancer** services use DNAT at the node or cloud LB
- Bastion-less admin: forward management port temporarily during migration

Security considerations:

- Minimize exposed ports; use VPN or bastion instead of broad port forwarding
- Combine DNAT with firewall allow rules on specific source IPs
- Log and audit forwarded services

### Protocols That Break Behind NAT

| Protocol | Issue | Mitigation |
|----------|-------|------------|
| FTP | Embedded IP in payload | `nf_conntrack_ftp` ALG module |
| SIP/VoIP | Embedded IP/port | SIP ALG (often buggy — disable and use STUN/TURN) |
| IPsec | ESP/AH not port-based | NAT-T (UDP encapsulation) |
| P2P gaming | Direct peer connection fails | TURN relay servers |
| Custom protocols | App sends private IP to peer | Application-level NAT awareness |

## Hands-on Lab

These labs use a single Linux VM to simulate NAT concepts. Multi-VM setups provide richer exercises.

### Step 1 – Verify IP forwarding and conntrack

**Command:**

```bash
sysctl net.ipv4.ip_forward
lsmod | grep nf_conntrack || echo "conntrack module info"
sudo conntrack -L 2>/dev/null | wc -l
```

**Explanation:** NAT requires IP forwarding enabled. conntrack table size indicates active translated connections.

**Expected output:**

```text
net.ipv4.ip_forward = 0
(conntrack count varies)
```

### Step 2 – Inspect current NAT rules

**Command:**

```bash
sudo iptables -t nat -L -v -n 2>/dev/null | head -25
sudo nft list table ip nat 2>/dev/null || echo "No nftables nat table"
```

**Explanation:** Most servers have empty NAT tables unless acting as routers, Docker hosts, or Kubernetes nodes. Docker creates MASQUERADE rules automatically.

### Step 3 – Simulate outbound connection tracking

**Command:**

```bash
curl -s https://example.com > /dev/null &
sleep 1
sudo conntrack -L 2>/dev/null | grep -E "tcp|dport=443" | head -3
```

**Explanation:** Even without explicit SNAT rules, conntrack tracks outbound connections. On NAT-enabled routers, these entries include translation mappings.

### Step 4 – Docker NAT inspection (if Docker installed)

**Command:**

```bash
docker run -d --name nat-lab -p 8888:80 nginx:alpine 2>/dev/null && \
  sudo iptables -t nat -L DOCKER -v -n 2>/dev/null | head -10
docker rm -f nat-lab 2>/dev/null || echo "Docker not available — skip"
```

**Explanation:** Docker publishes ports via DNAT rules in the `DOCKER` chain — a real-world NAT example on most DevOps workstations.

### Step 5 – Manual port forward lab (requires network namespaces)

**Command:**

```bash
# Create isolated network namespaces simulating private + public sides
sudo ip netns add private 2>/dev/null
sudo ip netns add public 2>/dev/null
sudo ip link add veth-priv type veth peer name veth-pub 2>/dev/null
sudo ip link set veth-priv netns private
sudo ip link set veth-pub netns public
sudo ip netns exec private ip addr add 10.200.1.2/24 dev veth-priv
sudo ip netns exec public ip addr add 10.200.1.1/24 dev veth-pub
sudo ip netns exec private ip link set veth-priv up
sudo ip netns exec public ip link set veth-pub up
sudo ip netns exec private ip route add default via 10.200.1.1
echo "Namespaces created — cleanup with: sudo ip netns del private public"
```

**Explanation:** Network namespaces simulate NAT boundaries without multiple VMs. Production NAT rules would MASQUERADE traffic from `private` namespace outbound via `public`.

### Step 6 – Trace AWS NAT Gateway route (AWS CLI)

**Command:**

```bash
# Replace with your private subnet route table ID
aws ec2 describe-route-tables \
  --filters "Name=tag:Tier,Values=private" \
  --query 'RouteTables[].Routes[?DestinationCidrBlock==`0.0.0.0/0`]' \
  --output table 2>/dev/null || echo "Configure AWS CLI or review route table in console"
```

**Explanation:** Private subnet default routes should point to `nat-xxxxxxxx`, not `igw-xxxxxxxx`. Wrong route is the #1 "private instance can't reach internet" cause.

### Step 7 – Diagnose NAT failure scenario

**Scenario:** EC2 in private subnet cannot `curl https://example.com`. Same instance CAN reach another instance in the same subnet. Route table shows `0.0.0.0/0 → nat-0abc123`. NAT GW is in public subnet with EIP.

**Checklist:**

1. NAT GW in **same AZ** as the instance (cross-AZ works but adds latency/cost)
2. NAT GW subnet route: `0.0.0.0/0 → igw`
3. Security group allows **outbound** HTTPS (443) from instance
4. NACL on private subnet allows outbound ephemeral ports AND inbound ephemeral return
5. NAT GW CloudWatch metrics — ActiveConnectionCount, ErrorPortAllocation

### Step 8 – Cleanup network namespaces

**Command:**

```bash
sudo ip netns del private 2>/dev/null
sudo ip netns del public 2>/dev/null
sudo ip link del veth-priv 2>/dev/null
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
| `iptables -t nat -L` | List NAT rules | `sudo iptables -t nat -L -v -n` |
| `conntrack -L` | Show connection tracking | `sudo conntrack -L \| grep dport` |
| `sysctl ip_forward` | Check forwarding enabled | `sysctl net.ipv4.ip_forward` |
| `nft list table ip nat` | nftables NAT rules | `sudo nft list table ip nat` |
| `ip netns` | Network namespace isolation | `sudo ip netns list` |
| `aws ec2 describe-nat-gateways` | AWS NAT GW status | `aws ec2 describe-nat-gateways` |

### Terraform NAT Gateway snippet

```hcl
resource "aws_nat_gateway" "az_a" {
  allocation_id = aws_eip.nat_a.id
  subnet_id     = aws_subnet.public_a.id

  tags = {
    Name = "nat-gw-az-a"
  }
}

resource "aws_route" "private_default_az_a" {
  route_table_id         = aws_route_table.private_a.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.az_a.id
}
```

### conntrack exhaustion check

```bash
#!/usr/bin/env bash
MAX=$(sysctl -n net.netfilter.nf_conntrack_max)
COUNT=$(cat /proc/sys/net/netfilter/nf_conntrack_count 2>/dev/null || echo 0)
PCT=$(( COUNT * 100 / MAX ))
echo "conntrack: ${COUNT}/${MAX} (${PCT}%)"
[[ $PCT -gt 80 ]] && echo "WARNING: conntrack table over 80% full"
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Private subnet routed to IGW instead of NAT GW"
    Private instances without public IPs cannot use IGW directly. Symptom: outbound traffic fails or asymmetric routing errors.

!!! warning "Missing FORWARD chain rules"
    SNAT/DNAT alone is insufficient — you must allow forwarded packets between interfaces. Symptom: SYN leaves but no return traffic.

!!! warning "NACL blocks ephemeral return ports"
    Stateless NACLs on private subnets must allow inbound TCP 1024-65535 (ephemeral) for return traffic through NAT. Symptom: timeout, not refused.

!!! warning "Single NAT GW for multi-AZ VPC"
    AZ failure takes all private subnets offline for outbound internet. Deploy per-AZ NAT GWs for production HA.

## Best Practices

!!! tip "One NAT GW per availability zone"
    Align NAT GW AZ with private subnet AZ. Avoid cross-AZ NAT traffic charges and single-point-of-failure.

!!! tip "Monitor conntrack and NAT GW metrics"
    Alert on conntrack table usage above 80% and NAT Gateway `ErrorPortAllocation` metrics.

!!! tip "Prefer managed NAT over NAT instances"
    Unless cost optimisation at massive scale justifies operational burden, managed NAT gateways reduce incident surface.

!!! tip "Avoid port forwarding for admin access"
    Use SSM Session Manager, VPN, or bastion hosts instead of exposing SSH via DNAT to the internet.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Private instance no outbound internet | Wrong route table | Point `0.0.0.0/0` to NAT GW, not IGW |
| Outbound works, inbound fails | NAT is outbound-only by design | Use ALB, NLB, or explicit DNAT for inbound |
| Intermittent connection failures | conntrack table full | Increase `nf_conntrack_max`; investigate connection leaks |
| DNAT works but wrong source IP in logs | Expected SNAT behaviour | Use `X-Forwarded-For` at application/proxy layer |
| FTP/SIP fails through NAT | ALG not loaded or broken | Enable conntrack helper or use passive mode / STUN |
| High NAT GW costs | Cross-AZ traffic | Keep NAT GW and instances in same AZ; use VPC endpoints for AWS services |

## Summary

- **SNAT** changes source addresses for outbound traffic; **DNAT** changes destination for inbound; **PAT** multiplexes many flows on one public IP
- Linux implements NAT via **iptables/nftables** `nat` table with **conntrack** tracking return translations
- Cloud **NAT gateways** provide managed outbound internet for **private subnets** — not a substitute for load balancers on inbound traffic
- **Port forwarding** (DNAT) exposes internal services — minimize use and combine with firewall restrictions
- Debug NAT with **route tables**, **conntrack**, **iptables -t nat -L**, and **packet capture**
- Monitor **conntrack exhaustion** and **NAT GW metrics** in production

## Interview Questions

1. What is the difference between SNAT and DNAT?
2. Why do private subnet instances need a NAT gateway to reach the internet?
3. Explain how connection tracking enables NAT to work bidirectionally.
4. What is port forwarding, and how does it relate to DNAT?
5. Why does NAT break some protocols like FTP?
6. How would you troubleshoot a private EC2 instance that cannot reach external APIs?
7. Compare NAT gateway vs Internet Gateway in AWS VPC.
8. What happens when the conntrack table is full?
9. Why deploy one NAT gateway per availability zone?
10. How does Docker publish container ports using NAT?

??? tip "Sample Answers (Questions 1, 3, and 6)"

    **Q1 — SNAT vs DNAT:** SNAT modifies the source IP/port on outbound packets so private addresses appear as the NAT device's public IP. DNAT modifies the destination IP/port on inbound packets to redirect traffic to internal hosts — used for port forwarding. SNAT enables many private hosts to share one public IP outbound; DNAT enables inbound access to specific internal services.

    **Q3 — conntrack role:** When the first outbound packet is SNAT'd, conntrack records the mapping (private IP:port ↔ public IP:port). Return packets arriving at the public IP:port are automatically reverse-translated using this state entry and delivered to the correct private host. Without conntrack, the NAT device would not know where to send inbound responses.

    **Q6 — Private EC2 no external API:** Check route table — `0.0.0.0/0` must target NAT GW. Verify NAT GW is available and in a public subnet with IGW route. Check instance SG allows outbound 443. Check NACL allows outbound and inbound ephemeral ports. Test with `curl -v` and tcpdump on the instance. Review NAT GW CloudWatch for errors. Verify DNS resolution works (separate from NAT but common co-failure).

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md) *(previous in Module 6)*
- [VPN and Tunneling Basics](vpn-and-tunneling-basics.md) *(next in Module 6)*
- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Packet Analysis with tcpdump and Wireshark](packet-analysis-tcpdump-wireshark.md)
- [Linux – Category Overview](../linux/index.md)
- [Docker – Category Overview](../docker/index.md)

## References

- [RFC 3022 — Traditional IP Network Address Translator](https://www.rfc-editor.org/rfc/rfc3022)
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918)
- [Linux netfilter NAT HOWTO](https://www.netfilter.org/documentation/HOWTO/NAT-HOWTO.html)
- [AWS NAT Gateway documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [nftables NAT wiki](https://wiki.nftables.org/wiki-nftables/index.php/Performing_Network_Address_Translation_(NAT))
