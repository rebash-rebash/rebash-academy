---
title: Network Troubleshooting Methodology
description: Apply bottom-up and top-down troubleshooting, divide-and-conquer isolation, incident documentation, runbook templates, and layered network checklists.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: networking
tags:
  - networking
  - troubleshooting
  - runbooks
  - methodology
  - sre
  - incident-response
prerequisites:
  - Complete Module 4 tutorials or equivalent application-layer networking knowledge
  - Familiarity with Linux CLI tools (ping, curl, dig, ss)
  - Basic understanding of TCP/IP from earlier networking modules
comments: false
---

# Network Troubleshooting Methodology

## Overview

When production is down and stakeholders are asking "what's wrong?", ad-hoc guessing wastes precious minutes. Senior engineers follow a **methodology** — a repeatable process that narrows the fault domain systematically, documents findings as they go, and avoids the trap of changing three things at once without knowing which fix worked.

Network outages rarely announce their layer. A "site is down" report might be DNS, TLS, a misconfigured security group, an exhausted connection table, or an application bug masquerading as network failure. This tutorial teaches the **bottom-up**, **top-down**, and **divide-and-conquer** approaches, how to write runbooks that survive 3 AM pages, and a layered checklist you can apply to every connectivity incident.

This is **Tutorial 14** in **Module 5: Troubleshooting** of the REBASH Academy Networking series.

## Prerequisites

- Complete [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md) and prior Module 4 tutorials
- Familiarity with [Linux Networking Essentials](../linux/linux-networking-essentials.md) tools: `ip`, `ss`, `dig`, `curl`
- Access to a Linux lab environment or cloud instance for hands-on exercises
- Optional: past incident experience to map concepts to real scenarios

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply bottom-up and top-down troubleshooting models to isolate network faults
- [ ] Use divide-and-conquer to bisect complex paths and find the failing segment
- [ ] Document incidents with timestamps, commands run, and hypotheses tested
- [ ] Create and maintain network troubleshooting runbooks from a proven template
- [ ] Execute a layered checklist from physical/link through application layers
- [ ] Distinguish network problems from application and DNS failures quickly

## Architecture

The OSI/TCP-IP layered model provides the framework for bottom-up troubleshooting. Each layer must work before the layer above can function.

```d2
direction: down

L7: "Layer 7 — Application" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        APP: "HTTP / API / TLS cert validity"
    }
    L4: "Layer 4 — Transport" {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        TCP: "TCP handshake · ports · firewalls"
    }
    L3: "Layer 3 — Network" {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        IP: "Routing · ICMP · IP reachability"
    }
    L2: "Layer 2 — Data Link" {
      style: {
        fill: "#f3e8ff"
        stroke: "#9333ea"
      }
        ARP: "ARP · MAC · VLAN · switch"
    }
    L1: "Layer 1 — Physical" {
      style: {
        fill: "#fce7f3"
        stroke: "#db2777"
      }
        PHY: "Cable · NIC · link up/down"
    }
    L7.APP -> L4.TCP
    L4.TCP -> L3.IP
    L3.IP -> L2.ARP
    L2.ARP -> L1.PHY
```

## Theory

### Why Methodology Matters

Without methodology, engineers:

- Restart services randomly hoping something sticks
- Fix symptoms (restart nginx) instead of causes (DNS TTL expired to dead IP)
- Cannot explain to leadership what happened or how long recovery takes
- Repeat the same mistakes because incidents are not documented

Methodology provides **structure under pressure**. It does not replace expertise — it channels expertise efficiently. The goal is to answer three questions in order:

1. **What is broken?** — Define the symptom precisely (all users vs one region vs one endpoint)
2. **Where is it broken?** — Isolate the failing segment in the path
3. **Why is it broken?** — Identify root cause and implement durable fix

### Top-Down Troubleshooting

Start at the **application layer** and work downward. Best when:

- User reports are application-specific ("checkout fails" but homepage works)
- You suspect DNS, TLS, or HTTP configuration first
- External monitoring shows HTTP 5xx but ping succeeds

**Top-down flow:**

1. Can the user reach the URL? What HTTP status and latency?
2. Does DNS resolve correctly from affected locations?
3. Does TLS handshake succeed? Certificate valid and trusted?
4. Does TCP connect to the correct IP:port?
5. Is routing and ICMP reachability intact?
6. Is the physical/link layer up?

**Example:** `curl -v https://api.example.com/health` returns `SSL certificate problem`. You stop at Layer 6/7 — no need to check ARP yet. Fix cert expiry or chain.

### Bottom-Up Troubleshooting

Start at **Layer 1** and work upward. Best when:

- "Nothing works" from a host or subnet
- Recent infrastructure change (cable, switch, route, firewall)
- New server or VPC build — verify foundation before app deploy

**Bottom-up flow:**

1. Is the interface up? (`ip link show`)
2. Does ARP resolve the gateway? (`ip neigh`)
3. Can you ping the default gateway and remote IPs?
4. Is routing correct? (`ip route`)
5. Does DNS resolve? (`dig`)
6. Does TCP connect to the service port? (`nc`, `curl`)
7. Does the application respond correctly?

**Example:** New EC2 instance cannot reach anything. `ip link` shows `state DOWN` — fix interface or attach ENI before debugging DNS.

### Divide-and-Conquer

When the path spans many hops (client → CDN → WAF → LB → proxy → app → database), **bisect** the path:

1. Identify the full end-to-end path on a diagram
2. Test from the middle — can the load balancer reach backends?
3. If middle works, problem is client-to-LB segment; if not, problem is LB-to-backend
4. Repeat until the failing component is isolated

This is the fastest approach for **complex distributed systems** and aligns with how senior SREs actually work during incidents — not strictly OSI layer order, but **fault domain isolation**.

| Approach | Start point | Best for |
|----------|-------------|----------|
| Top-down | Application | App-specific errors, HTTP/TLS issues |
| Bottom-up | Physical/link | Total connectivity loss, new builds |
| Divide-and-conquer | Middle of path | Multi-hop production architectures |

### Symptom-to-Layer Quick Reference

| Symptom | Likely layer | First checks |
|---------|--------------|--------------|
| `Connection refused` | L4/L7 — port closed or app down | `ss -tlnp`, process status |
| `Connection timed out` | L3/L4 — filtered or no route | SG/NACL, `traceroute`, `tcpdump` |
| `Could not resolve host` | L7 — DNS | `dig`, `/etc/resolv.conf` |
| `SSL certificate problem` | L6/L7 — TLS | `openssl s_client`, cert expiry |
| `502/504 Bad Gateway` | L7 — proxy to backend | Backend health, proxy logs |
| `Network unreachable` | L3 — routing | `ip route`, default gateway |
| Intermittent failures | L4 state, LB health, MTU | Conntrack, health checks, `ping -M do` |
| One region affected | DNS geo, CDN, routing | Geo DNS, Route 53 health checks |

### Documentation During Incidents

Real-time documentation is not bureaucracy — it is how you:

- Hand off to the next engineer without losing context
- Prove timeline for postmortems and SLA reporting
- Avoid repeating failed remediation attempts

**Document as you go:**

| Field | Example |
|-------|---------|
| Timestamp (UTC) | 2026-07-27T14:32:00Z |
| Reporter / impact | All EU users, checkout 100% fail |
| Hypothesis | DNS pointing to drained LB |
| Command + output | `dig api.example.com` → stale IP 203.0.113.50 |
| Action taken | Flushed Route 53 health check, failed over |
| Result | Recovery confirmed 14:41 UTC |

Use a shared doc, Slack thread, or incident channel — not memory.

### Runbook Template

A **runbook** is a pre-written procedure for known failure modes. Network runbooks should be **action-oriented** with decision trees, not essay paragraphs.

## Hands-on Lab

Simulate a structured troubleshooting session on a Linux lab host. Work through the layered checklist deliberately — do not skip steps.

### Step 1 – Define the problem statement

Before running commands, write a precise problem statement:

**Template:**

```text
WHO:     All users / subset / single host
WHAT:    Cannot reach https://api.example.com/health
WHEN:    Since 2026-07-27 14:00 UTC (after deploy X)
CHANGE:  Security group rule modified on app-tier SG
```

**Explanation:** Vague "network is broken" leads to vague debugging. Scope determines which methodology fits.

### Step 2 – Top-down: application layer check

**Command:**

```bash
curl -sv --connect-timeout 5 https://example.com/ 2>&1 | head -30
curl -sv --connect-timeout 5 http://example.com/ 2>&1 | head -20
```

**Explanation:** Note HTTP status, TLS handshake, redirect behavior, and total time. Compare HTTP vs HTTPS failures.

**Expected output:**

```text
* Connected to example.com (93.184.216.34) port 443
* SSL connection using TLSv1.3 ...
> GET / HTTP/2
< HTTP/2 200
```

### Step 3 – DNS layer verification

**Command:**

```bash
dig example.com +short
dig example.com @8.8.8.8 +short
dig api.example.com +trace 2>/dev/null | tail -15
```

**Explanation:** Compare resolver answers. `+trace` shows delegation chain — useful for "works in US, fails in EU" geo-DNS issues.

**Expected output:**

```text
93.184.216.34
```

### Step 4 – Bottom-up: interface and routing

**Command:**

```bash
ip link show
ip addr show
ip route show
ping -c 3 -W 2 $(ip route | awk '/default/ {print $3}')
```

**Explanation:** Confirm link UP, valid IP, default gateway reachable. No gateway = no internet regardless of DNS or app config.

**Expected output:**

```text
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
default via 10.0.0.1 dev eth0
3 packets transmitted, 3 received, 0% packet loss
```

### Step 5 – Transport layer: TCP connectivity

**Command:**

```bash
nc -zv example.com 443
nc -zv example.com 80
timeout 3 bash -c 'cat < /dev/null > /dev/tcp/example.com/443' && echo "TCP 443 open" || echo "TCP 443 failed"
```

**Explanation:** Distinguishes "DNS works but port filtered" (timeout) from "port closed" (refused).

### Step 6 – Divide-and-conquer: simulate path bisection

Draw your production path on paper. For this lab, simulate:

```text
Client (this host) → DNS → Internet → example.com:443
```

**Command:**

```bash
# Segment 1: DNS resolution
RESOLVED=$(dig +short example.com | head -1)
echo "Resolved IP: $RESOLVED"

# Segment 2: L3 reachability
ping -c 2 -W 2 "$RESOLVED"

# Segment 3: L4 TCP
nc -zv "$RESOLVED" 443

# Segment 4: L7 HTTP
curl -sI --connect-timeout 5 "https://$RESOLVED/" -H "Host: example.com" | head -5
```

**Explanation:** Testing IP directly with Host header isolates DNS from HTTP — classic bisection technique.

### Step 7 – Document findings in incident format

**Command:**

```bash
cat <<'EOF' > /tmp/incident-notes.txt
INCIDENT: Lab connectivity exercise
START:    $(date -u +%Y-%m-%dT%H:%M:%SZ)

FINDINGS:
- DNS: example.com → 93.184.216.34 (consistent across resolvers)
- L3:  ping 0% loss to resolved IP
- L4:  TCP 443 connect success
- L7:  HTTP/2 200 from curl

CONCLUSION: End-to-end path healthy from lab host.
NEXT: If production fails, compare SG/NACL and regional DNS.
EOF
cat /tmp/incident-notes.txt
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

| Command | Layer | Purpose |
|---------|-------|---------|
| `curl -sv` | L7 | Full HTTP/TLS trace |
| `dig` / `nslookup` | L7 (DNS) | Name resolution |
| `openssl s_client -connect host:443` | L6/L7 | TLS handshake debug |
| `nc -zv host port` | L4 | TCP port probe |
| `ss -tulpn` | L4 | Local listeners |
| `ping` / `mtr` | L3 | Reachability and path |
| `traceroute` / `tracepath` | L3 | Hop-by-hop path |
| `ip route` / `ip neigh` | L3/L2 | Routing and ARP |
| `ip link` | L1/L2 | Interface state |
| `tcpdump` | All | Packet evidence |

### Runbook template (copy and customize)

```markdown
# Runbook: [Service] — Connectivity Failure
**Owner:** Platform Team | **Severity:** P1 | **Last tested:** YYYY-MM-DD

## Quick triage (5 min)
1. External synthetic: `curl -sf https://STATUS_URL/health`
2. Confirm scope: all users vs region vs subset
3. Recent changes: deploys, SG rules, DNS, cert renewal

## Decision tree
- **HTTP 5xx from LB** → target health, listener rules, SG
- **Connection timeout** → `nc -zv`, SG/NACL, routing, tcpdump
- **DNS failure** → `dig +trace`, resolver, TTL

## Commands
aws elbv2 describe-target-health --target-group-arn $TG_ARN
nc -zv BACKEND_IP PORT
dig +short SERVICE.example.com @8.8.8.8
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Changing multiple variables at once"
    Restarting nginx, flushing DNS, and modifying SG rules simultaneously means you never know what fixed it — and the problem may return. Change one thing, re-test, document result.

!!! warning "Assuming ping success means HTTP works"
    ICMP may be allowed while TCP 443 is blocked by firewall. Always test the actual protocol and port the application uses.

!!! warning "Skipping scope definition"
    "Site is down" when only mobile users in one country are affected sends you debugging the wrong DNS geo route for an hour.

!!! warning "No baseline for comparison"
    Without knowing normal latency, packet loss, and DNS answers, you cannot identify abnormal. Maintain golden-signal baselines in monitoring.

## Best Practices

!!! tip "Start with recent changes"
    The strongest predictor of outages is change — deploys, cert renewals, firewall tickets. Ask "what changed?" before deep packet analysis.

!!! tip "Use external and internal vantage points"
    Test from outside the network (synthetic monitoring) and inside (bastion, pod). Asymmetric routing failures only appear from one direction.

!!! tip "Time-box hypothesis testing"
    If a hypothesis is not confirmed in 10 minutes, pivot. Stuck engineers should escalate or bisect from a different point.

!!! tip "Maintain runbooks as living documents"
    Runbooks rot within months. Test them in game days; update after every postmortem with new failure modes encountered.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Methodology feels slow under pressure | Lack of practice | Drill runbooks in game days; keep checklist printed/on second monitor |
| Cannot reproduce user report | Geo, auth, or client-specific | Get HAR file, curl from user region, test logged-out vs logged-in |
| Everything looks healthy but app fails | Application layer, not network | Check app logs, DB connectivity, feature flags — hand off with evidence |
| Intermittent — hard to bisect | Race conditions, LB rotation, flaky health | Increase logging; capture during failure window with tcpdump |
| Runbook steps outdated | Infrastructure drift | Assign runbook owner; review quarterly |

## Summary

- **Top-down** starts at the application (HTTP, DNS, TLS); **bottom-up** starts at link/routing — choose based on symptoms
- **Divide-and-conquer** bisects multi-hop paths and is fastest for complex production architectures
- **Document timestamps, commands, and results** during incidents — not after
- **Runbooks** with decision trees and copy-paste commands reduce MTTR and onboarding time
- Use the **layered checklist**: link → IP/route → DNS → TCP port → HTTP/TLS → application
- Symptom vocabulary matters: **refused** vs **timeout** vs **unreachable** point to different layers

## Interview Questions

1. Describe top-down vs bottom-up network troubleshooting. When do you use each?
2. What is divide-and-conquer troubleshooting, and how does it differ from strict OSI layer order?
3. A user reports "connection timed out" to your API. Walk through your diagnostic steps.
4. Why is ping success insufficient to declare "the network is fine"?
5. What should you document during a live incident?
6. How would you structure a runbook for load balancer → backend connectivity failures?
7. What recent change would you investigate first in any outage?
8. How do you distinguish DNS failure from firewall blocking?

??? tip "Sample Answers (Questions 1, 3, and 8)"

    **Q1 — Top-down vs bottom-up:** Top-down starts at the application — curl the URL, check HTTP status, TLS, and DNS — best when symptoms are service-specific. Bottom-up starts at the network interface and routing, then DNS, TCP, and HTTP — best when a host or subnet has total connectivity loss or after infrastructure changes. Divide-and-conquer bisects the path for complex multi-tier architectures regardless of strict layer order.

    **Q3 — Connection timed out:** Timeout implies packets are dropped or not routed back, not actively refused. Steps: (1) confirm scope — all users or subset; (2) `dig` the API hostname — does DNS resolve? (3) `nc -zv host 443` — timeout vs refused; (4) if timeout, check security groups, NACLs, host firewall, and routing; (5) `traceroute` / `mtr` to find last responding hop; (6) test from bastion inside VPC vs external; (7) if internal works, problem is edge SG or WAF; (8) capture packets with tcpdump if still unclear.

    **Q8 — DNS vs firewall:** DNS failure: `dig` returns NXDOMAIN, SERVFAIL, or unexpected IP; `curl` fails with "Could not resolve host" before any TCP attempt. Firewall blocking: `dig` returns correct IP; `ping` may work or fail (ICMP often blocked); `nc` to port 443 **times out** (filtered) or **refused** (closed). Test IP directly with curl `-H Host:` header to remove DNS from the equation.

9. How would you explain network troubleshooting methodology to a junior engineer in two minutes?
10. What production failure mode appears when teams ignore network troubleshooting methodology?

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md) *(previous — Module 4)*
- [Packet Analysis with tcpdump and Wireshark](packet-analysis-tcpdump-wireshark.md) *(next in Module 5)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md)

## References
- [AWS Troubleshooting VPC Connectivity](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-troubleshooting.html)
- [REBASH Academy — Troubleshooting Linux Systems](../linux/troubleshooting-linux-systems.md)
