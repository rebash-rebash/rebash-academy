---
title: Firewalls and Access Control
description: Understand stateful vs stateless filtering, iptables and nftables, UFW, cloud security groups and NACLs, and least-privilege network design.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - firewall
  - iptables
  - nftables
  - ufw
  - security-groups
  - access-control
prerequisites:
  - Complete [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) or equivalent
  - Basic understanding of TCP/UDP ports and IP addressing
  - Linux VM or cloud instance with sudo access
comments: false
---

# Firewalls and Access Control

## Overview

Firewalls are the first line of defense between your infrastructure and the internet. They enforce **access control** — deciding which packets may enter, leave, or traverse a network boundary based on IP addresses, ports, protocols, and connection state. Every production environment uses firewalls at multiple layers: host-based rules on Linux servers, perimeter appliances, and cloud-native controls like AWS Security Groups and Network ACLs.

Misconfigured firewalls cause more production outages than malicious attacks. A rule that blocks health-check traffic takes down a load-balanced fleet; an overly permissive rule exposes databases to the public internet. This tutorial teaches you how firewalls actually work, how to manage them on Linux, and how to design **least-privilege** policies that balance security with operability.

This is **Tutorial 11** in **Module 4: Application Layer** of the REBASH Academy Networking series. It includes theory, hands-on labs, and interview preparation.

## Prerequisites

- Complete [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) or understand ports 80/443 and TCP connection basics
- Familiarity with IP addresses, CIDR notation, and TCP/UDP from [IP Addressing and Subnetting](ip-addressing-and-subnetting.md)
- A Linux VM (Ubuntu 22.04+ recommended) or cloud instance with `sudo` access
- Optional: AWS/GCP/Azure account for security group exercises (free tier is sufficient)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between stateful and stateless packet filtering
- [ ] Describe how iptables chains and tables work, and why nftables is replacing them
- [ ] Configure host firewalls with UFW on Ubuntu/Debian systems
- [ ] Differentiate cloud Security Groups from Network ACLs and apply least privilege
- [ ] Design firewall rules that allow required traffic without opening unnecessary ports
- [ ] Troubleshoot connectivity failures caused by firewall misconfiguration

## Architecture

Firewalls operate at multiple enforcement points. Defense in depth means layering controls — never relying on a single rule set.

```d2
direction: down

Internet: Internet {
        ATT: "External Clients"
    }
    Perimeter: Perimeter {
        NACL: "Network ACL\nstateless · subnet boundary"
        SG: "Security Group\nstateful · instance ENI"
    }
    Host: Host {
        UFW: "UFW / nftables\nhost firewall"
        APP: "Application\nnginx · postgres"
    }
    Internet.ATT -> Perimeter.NACL
    Perimeter.NACL -> Perimeter.SG
    Perimeter.SG -> Host.UFW
    Host.UFW -> Host.APP
    Host.APP -> Host.UFW: response
    Host.UFW -> Perimeter.SG
    Perimeter.SG -> Perimeter.NACL
    Perimeter.NACL -> Internet.ATT
```

## Theory

### What a Firewall Does

A **firewall** inspects network packets and applies a policy: **allow**, **deny**, or **drop** (silently discard). Policies are expressed as **rules** matched in order until a decision is reached. Rules typically filter on:

- **Source/destination IP** — which hosts or subnets
- **Protocol** — TCP, UDP, ICMP
- **Port** — for TCP/UDP (e.g., 22, 443)
- **Connection state** — new, established, related (stateful firewalls only)
- **Interface** — which NIC the packet arrives on

Firewalls can be **network-based** (between subnets, at the edge) or **host-based** (on each server). In cloud environments, you typically have both.

### Stateful vs Stateless Filtering

**Stateless** firewalls evaluate each packet independently. They do not remember prior packets. A rule allowing inbound TCP port 443 does not automatically allow the return traffic — you must explicitly permit outbound ephemeral ports or bidirectional rules. Network ACLs in AWS are stateless by default.

**Stateful** firewalls track **connections** (flows). When a client initiates a TCP SYN to your web server on port 443, the firewall creates a session entry. Return packets matching that session are automatically permitted without a separate inbound rule. Linux `iptables`/`nftables` with `conntrack`, UFW, and AWS Security Groups are stateful.

| Aspect | Stateless | Stateful |
|--------|-----------|----------|
| Memory of sessions | No | Yes (conntrack table) |
| Return traffic | Must be explicitly allowed | Automatically allowed for established sessions |
| Performance | Lower overhead | Slightly higher (session tracking) |
| Complexity | More rules for bidirectional flows | Simpler for client-initiated connections |
| Example | AWS NACL, early packet filters | UFW, Security Groups, modern iptables |

**Production implication:** When debugging "connection timeout" vs "connection refused," stateful firewalls often drop packets silently if return path rules are missing — the symptom looks like a black hole, not an explicit rejection.

### iptables: Chains, Tables, and Rules

**iptables** is the legacy userspace tool for configuring the Linux kernel's **netfilter** framework. Packets traverse **tables** containing **chains** of rules:

| Table | Purpose |
|-------|---------|
| `filter` | Allow/deny forwarding and local delivery (most common) |
| `nat` | Network Address Translation (SNAT/DNAT) |
| `mangle` | Packet marking, TTL modification |
| `raw` | Connection tracking exemptions |

Common **chains** in the `filter` table:

- **INPUT** — packets destined for this host
- **OUTPUT** — packets originating from this host
- **FORWARD** — packets routed through this host (routers, Docker, K8s nodes)

Rule matching is **first-match-wins**. The default policy on a chain applies if no rule matches. A typical secure baseline sets INPUT default to DROP and explicitly allows SSH, established connections, and loopback.

Example rule semantics:

```bash
# Allow established and related connections
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Allow SSH from admin subnet only
iptables -A INPUT -p tcp -s 10.0.1.0/24 --dport 22 -j ACCEPT
```

!!! warning "iptables vs nftables"
    New Linux deployments should prefer **nftables**, which replaces the iptables kernel backend with a unified, more performant rule engine. Ubuntu 22.04+ uses nftables by default; `iptables` commands often invoke `iptables-nft` compatibility layer. Learn nftables syntax for greenfield work; know iptables for legacy systems and interview questions.

### nftables Overview

**nftables** consolidates IPv4, IPv6, ARP, and bridge filtering into one framework with a cleaner syntax:

```nft
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif lo accept
    tcp dport 22 ip saddr 10.0.1.0/24 accept
    tcp dport { 80, 443 } accept
  }
}
```

Key advantages over legacy iptables:

- Single rule set for IPv4 and IPv6 (`inet` family)
- Atomic rule replacement (no flush-and-rebuild race)
- Better performance on large rule sets
- Native sets and maps for IP/port grouping

On systems running UFW, nftables rules are managed indirectly — UFW generates nftables/iptables rules under the hood.

### UFW: Uncomplicated Firewall

**UFW** (Uncomplicated Firewall) is Ubuntu's user-friendly front end to iptables/nftables. It is ideal for single-server hardening and learning firewall concepts without memorizing netfilter syntax.

Default UFW behaviour:

- Denies all incoming, allows all outgoing
- Rules are numbered and processed in order
- Supports application profiles in `/etc/ufw/applications.d/`

Common operations:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status verbose
```

UFW is **not** a replacement for cloud Security Groups in AWS — use both. Security Groups protect the instance ENI; UFW protects against lateral movement if an attacker reaches the host.

### Cloud Security Groups vs Network ACLs

In AWS (similar concepts exist in GCP/Azure):

**Security Groups (SG)** — **stateful**, attached to ENIs (instances, load balancers). Rules reference other SGs by ID (e.g., "allow PostgreSQL from app-tier SG"). Default: deny all inbound, allow all outbound. Changes apply immediately.

**Network ACLs (NACL)** — **stateless**, attached to subnets. Ordered rule numbers (100, 200, …); first match wins. Explicit allow/deny for inbound and outbound. Default NACL allows all; custom NACLs often deny by default.

| Control | Scope | Stateful | Default |
|---------|-------|----------|---------|
| Security Group | Instance ENI | Yes | Deny inbound |
| NACL | Subnet | No | Varies |

**Defense in depth example:** Public subnet NACL allows 80/443 from `0.0.0.0/0`. Web-tier SG allows 80/443 from ALB SG only. App-tier SG allows 8080 from web-tier SG only. Database SG allows 5432 from app-tier SG only. No rule anywhere allows 5432 from the internet.

### Least Privilege in Network Design

**Least privilege** means granting the minimum network access required for a function — no wider CIDRs, no unnecessary ports, no "allow all" staging rules left in production.

Principles:

1. **Default deny** — start with no inbound access; add rules with justification
2. **Segment by tier** — web, app, data layers in separate subnets/SGs
3. **Use SG references over CIDR** — `source-group: app-sg` beats `10.0.2.0/24` when instances scale
4. **Restrict outbound** — egress filtering prevents data exfiltration (often overlooked)
5. **Document every rule** — tag SG rules with ticket IDs; review quarterly
6. **Separate admin access** — SSH/bastion from known IPs or VPN, never `0.0.0.0/0`

!!! tip "The 0.0.0.0/0 smell test"
    Any rule allowing `0.0.0.0/0` inbound on ports other than 80/443 (and sometimes 22 from a bastion) deserves scrutiny. Database ports, Redis (6379), and Docker API (2375) exposed to the internet are recurring breach patterns in incident reports.

## Hands-on Lab

Complete these exercises on an Ubuntu VM. Use a disposable lab instance — incorrect rules can lock you out of SSH.

### Step 1 – Inspect current firewall status

**Command:**

```bash
sudo ufw status verbose
sudo nft list ruleset 2>/dev/null | head -40
```

**Explanation:** UFW shows enabled/disabled state and active rules. `nft list ruleset` reveals the underlying nftables rules UFW generated (may be empty if UFW is inactive).

**Expected output:**

```text
Status: inactive
```

Or, if enabled:

```text
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
```

### Step 2 – Enable UFW with SSH protection first

**Command:**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 443/tcp comment 'HTTPS web traffic'
sudo ufw enable
```

**Explanation:** Always allow SSH **before** `ufw enable` on remote systems. The `comment` flag documents rule purpose in `ufw status`.

**Expected output:**

```text
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
```

### Step 3 – Verify connectivity and list numbered rules

**Command:**

```bash
sudo ufw status numbered
curl -sI https://example.com | head -3
```

**Explanation:** Numbered rules are required for deletion (`ufw delete 3`). Outbound HTTPS should succeed under default allow-outgoing policy.

**Expected output:**

```text
     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 443/tcp                    ALLOW IN    Anywhere
```

### Step 4 – Add a restrictive source IP rule

**Command:**

```bash
# Replace with your admin IP or lab subnet
sudo ufw allow from 10.0.1.0/24 to any port 22 proto tcp comment 'Admin SSH subnet'
sudo ufw status verbose
```

**Explanation:** Source-restricted rules implement least privilege for administrative access. In production, combine with bastion hosts or SSM Session Manager to avoid exposing SSH broadly.

### Step 5 – Inspect raw iptables/nftables counters

**Command:**

```bash
sudo iptables -L INPUT -v -n --line-numbers 2>/dev/null | head -20
# Or on nftables-native systems:
sudo nft list chain inet filter input 2>/dev/null
```

**Explanation:** Packet and byte counters show which rules are actually hit — essential when debugging "rule exists but traffic still blocked."

**Expected output:**

```text
Chain INPUT (policy DROP 0 packets, 0 bytes)
num   pkts bytes target     prot opt in     out     source               destination
1      142  8520 ACCEPT     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
...
```

### Step 6 – Simulate a blocked port

**Command:**

```bash
# Start a test listener (in one terminal)
python3 -m http.server 8888 &

# Deny inbound 8888
sudo ufw deny 8888/tcp
curl -v --connect-timeout 3 http://127.0.0.1:8888/
```

**Explanation:** UFW inserts deny rules. From localhost, traffic may bypass INPUT chain depending on configuration — test from a remote host for accurate results.

**Cleanup:**

```bash
sudo ufw delete deny 8888/tcp
kill %1 2>/dev/null
```

### Step 7 – Document a Security Group policy (AWS CLI or console)

If you have AWS access:

```bash
aws ec2 describe-security-groups --group-ids sg-0123456789abcdef0 \
  --query 'SecurityGroups[0].IpPermissions' --output table
```

**Explanation:** Practice reading SG rules: protocol, port range, source SG vs CIDR. Map each rule to a tier in your architecture diagram.

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
| `ufw status` | Show firewall state and rules | `sudo ufw status verbose` |
| `ufw allow` | Add allow rule | `sudo ufw allow 443/tcp` |
| `ufw deny` | Add deny rule | `sudo ufw deny 8888/tcp` |
| `ufw delete` | Remove rule by number | `sudo ufw delete 3` |
| `ufw enable` / `disable` | Toggle firewall | `sudo ufw enable` |
| `iptables -L` | List filter table rules | `sudo iptables -L -v -n` |
| `nft list ruleset` | Show all nftables rules | `sudo nft list ruleset` |
| `conntrack -L` | List connection tracking table | `sudo conntrack -L \| head` |
| `ss -tulpn` | Verify listening ports vs rules | `ss -tulpn \| grep LISTEN` |

### Infrastructure-as-Code: Security Group example (Terraform)

```hcl
resource "aws_security_group" "web" {
  name        = "web-tier"
  description = "Allow HTTP/HTTPS from ALB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "HTTP from ALB"
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  ingress {
    description     = "HTTPS from ALB"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "web-tier-sg"
    Tier    = "web"
    Managed = "terraform"
  }
}
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Enabling UFW before allowing SSH"
    Locking yourself out of a remote server is the most common UFW mistake. Always `ufw allow OpenSSH` (or your custom SSH port) before `ufw enable`. Keep a cloud console session open as backup.

!!! warning "Confusing Security Groups with NACLs"
    Fixing an SG rule does not help if NACL blocks return traffic. Stateless NACLs require explicit outbound ephemeral port rules. Symptom: TCP handshake starts but hangs after SYN-ACK.

!!! warning "Relying on deny rules in Security Groups"
    AWS SGs are allow-only — you cannot add explicit deny rules. Use NACLs for deny-list patterns or separate SGs per tier. "Deny bad IP" requires WAF, NACL, or network firewall appliance.

!!! warning "Opening all ports between tiers"
    `allow all traffic from app-sg` on the database SG violates least privilege. Allow only port 5432 (PostgreSQL) or 3306 (MySQL) — not every protocol.

## Best Practices

!!! tip "Layer defenses — never one firewall"
    Combine cloud SGs, NACLs, host UFW, and application auth. A misconfigured SG should not be the only barrier to a database.

!!! tip "Use infrastructure-as-code for firewall rules"
    Manage SGs, NACLs, and firewall rules in Terraform or CloudFormation with peer review. Ad-hoc console changes drift from documented architecture within weeks.

!!! tip "Log dropped packets during incidents"
    Temporarily enable UFW logging (`ufw logging medium`) or VPC Flow Logs to distinguish firewall drops from application failures. Disable verbose logging afterward — volume adds cost.

!!! tip "Review rules on a schedule"
    Quarterly access reviews should include SG and NACL audits. Remove rules tied to decommissioned services and expired contractor IP ranges.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| SSH timeout after enabling UFW | SSH port not allowed | Use cloud console; run `ufw allow OpenSSH`; disable UFW if needed |
| HTTP works locally but not remotely | SG/NACL or UFW blocks inbound 80/443 | Check `ufw status`, SG inbound rules, and NACL inbound/outbound |
| Intermittent connection drops | Stateful table full or conntrack exhaustion | Increase `net.netfilter.nf_conntrack_max`; investigate connection leaks |
| Health checks failing on load balancer | SG allows user traffic but not LB subnet | Allow health-check source SG or LB subnet CIDR on instance port |
| Docker/K8s networking broken after UFW enable | FORWARD chain default deny | Configure UFW forwarding rules or use dedicated CNI network policies |
| Rule exists but counters show zero hits | Wrong chain, interface, or nftables family | Verify with `nft list ruleset`; test from correct source IP |
| IPv6 traffic bypasses IPv4-only rules | Separate ip6tables/nftables inet family | Use `ufw allow` for both or explicit `inet` table rules in nftables |

## Summary

- **Stateful** firewalls track connections and automatically permit return traffic; **stateless** firewalls evaluate each packet independently
- **iptables/nftables** implement Linux netfilter; **UFW** provides a manageable front end for host hardening
- **Security Groups** are stateful, instance-scoped; **NACLs** are stateless, subnet-scoped — both are required for complete cloud network policy
- **Least privilege** means default deny, tier segmentation, SG references over broad CIDRs, and regular rule audits
- Always allow administrative access before enabling host firewalls on remote systems
- Use packet counters, flow logs, and layered testing to distinguish firewall drops from application errors

## Interview Questions

1. What is the difference between a stateful and stateless firewall?
2. Explain the purpose of iptables chains INPUT, OUTPUT, and FORWARD.
3. Why is nftables replacing iptables, and what problems does it solve?
4. How do AWS Security Groups differ from Network ACLs?
5. What is least privilege in network access control, and how do you implement it in a three-tier web application?
6. A user reports SSH works but HTTPS times out. Walk through your firewall troubleshooting steps.
7. Can you add a deny rule to an AWS Security Group? Why or why not?
8. What happens to return traffic in a stateful firewall when the initial outbound connection is allowed?
9. Why should UFW and Security Groups both be configured rather than choosing one?
10. How would you audit a fleet of servers for overly permissive firewall rules?

??? tip "Sample Answers (Questions 1, 4, and 6)"

    **Q1 — Stateful vs stateless:** A stateless firewall evaluates each packet in isolation — return traffic needs explicit rules. A stateful firewall maintains a connection table (conntrack); when it sees an outbound SYN or permitted inbound SYN, it tracks the session and automatically allows matching return packets. Security Groups and UFW are stateful; AWS NACLs are stateless.

    **Q4 — SG vs NACL:** Security Groups attach to ENIs, are stateful, default deny inbound, and support allow-only rules including references to other SGs. NACLs attach to subnets, are stateless, use ordered rule numbers with explicit allow and deny, and require separate inbound/outbound rules including ephemeral ports for TCP return traffic. SGs are the primary instance-level control; NACLs add subnet-level deny lists and defense in depth.

    **Q6 — SSH works, HTTPS times out:** SSH success proves routing and basic connectivity. Timeouts suggest filtered drops, not refusal. Check: (1) `ss -tlnp` — is anything listening on 443? (2) UFW/nftables — is 443 allowed inbound? (3) cloud SG — is 443 open from client source or LB SG? (4) NACL — outbound ephemeral ports allowed? (5) application — TLS misconfig causes refusal, not timeout; timeout implies firewall or no listener. Use `curl -v`, `tcpdump port 443`, and SG flow logs.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) *(previous in Module 4)*
- [Load Balancing Fundamentals](load-balancing-fundamentals.md) *(next in Module 4)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [Network Security Hardening](network-security-hardening.md)
- Cheat sheet: [Networking Cheat Sheet](../cheatsheets/networking.md)
- Interview prep: [Networking Interview Prep](../interview/networking.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [Linux netfilter/iptables documentation](https://www.netfilter.org/documentation/)
- [nftables wiki](https://wiki.nftables.org/)
- [Ubuntu UFW community documentation](https://help.ubuntu.com/community/UFW)
- [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
- [AWS Network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
- [NIST SP 800-41 — Guidelines on Firewalls and Firewall Policy](https://csrc.nist.gov/publications/detail/sp/800-41/rev-1/final)
