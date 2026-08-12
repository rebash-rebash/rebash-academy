---
title: "Quiz — Networking Production"
description: "25-question advanced quiz on Module 7 production network operations: segmentation, DNS ops, LB health checks, firewall change control, and incident response."
difficulty: advanced
estimated_time: "30–40 min"
passing_score: "70% (18/25)"
author: Shaik Basha
last_updated: "2026-07-28"
category: quizzes
tags:
  - quizzes
  - networking
  - production
  - assessment
comments: false
---

# Quiz — Networking Production

## Quiz Overview

Assess Module 7 Production Network Operations: segmentation, DNS ops, load-balancer health checks, firewall change control, and incident response.

| Attribute | Value |
|-----------|--------|
| Topic | Production network operations |
| Questions | 25 |
| Passing score | 70% (18 correct) |
| Estimated time | 30–40 minutes |

!!! tip "How to use this quiz"
    Select an answer for each question, then **Submit quiz** for a scored result. Progress is saved in this browser. Explanations unlock after you submit.

## Learning Objectives

- [ ] Reason about trust zones, blast radius, and tier allow matrices
- [ ] Plan DNS TTL cutovers and split-horizon behaviour
- [ ] Operate L4/L7 health checks, drain, and sticky-session trade-offs
- [ ] Apply firewall change control with rollback and console safety
- [ ] Execute first-hour incident evidence collection with curl, dig, and ss

## Section 1 — Fundamentals

### Question 1

Which trust zone typically terminates public HTTPS and sits closest to the internet?

**Difficulty:** Beginner

**Options:**

- **A.** Edge tier (load balancers, WAF, CDN)
- **B.** Data tier (databases)
- **C.** Management tier (bastion hosts)
- **D.** Application tier (workers only)

??? success "Reveal answer"
    **Correct answer: A**

    Edge zones accept untrusted inbound traffic and forward to app tiers under policy.

    **Related concepts**

    - Trust zones
    - Segmentation

### Question 2

What does **blast radius** measure in network segmentation?

**Difficulty:** Beginner

**Options:**

- **A.** Maximum cable length in a rack
- **B.** DNS TTL in seconds
- **C.** How far compromise or misconfiguration can spread across tiers
- **D.** HAProxy `maxconn` setting

??? success "Reveal answer"
    **Correct answer: C**

    Segmentation shrinks blast radius by limiting lateral movement.

    **Related concepts**

    - Blast radius
    - Trust boundaries

### Question 3

Before lowering DNS TTL for a migration, you must typically wait because?

**Difficulty:** Intermediate

**Options:**

- **A.** TTL changes propagate instantly worldwide
- **B.** Authoritative servers reject low TTL always
- **C.** curl ignores TTL
- **D.** Resolvers must expire the **previous** TTL before caching the new value

??? success "Reveal answer"
    **Correct answer: D**

    Old cached answers persist until their original TTL expires — plan 24–48 hours ahead.

    **Related concepts**

    - TTL
    - DNS caching

### Question 4

**Split-horizon DNS** means?

**Difficulty:** Intermediate

**Options:**

- **A.** One hostname always resolves to the same global IP
- **B.** Different answers for the same name depending on client location or resolver view
- **C.** DNS records stored only in `/etc/hosts`
- **D.** IPv6-only resolution

??? success "Reveal answer"
    **Correct answer: B**

    Internal and external views may differ — test both VPN and public paths.

    **Related concepts**

    - Split-horizon
    - DNS operations

### Question 5

An L4 (TCP) health check validates?

**Difficulty:** Beginner

**Options:**

- **A.** TCP connection establishment to a port
- **B.** HTTP status code and response body
- **C.** TLS certificate expiry only
- **D.** SQL query success

??? success "Reveal answer"
    **Correct answer: A**

    TCP connect confirms the port accepts — not that the application logic is healthy.

    **Related concepts**

    - L4 health checks
    - Load balancing

### Question 6

An L7 HTTP health check can detect which failure mode that TCP alone often misses?

**Difficulty:** Intermediate

**Options:**

- **A.** Port closed by firewall only
- **B.** Wrong DNS A record
- **C.** Process listening but returning HTTP 503 on `/healthz`
- **D.** Cable unplugged

??? success "Reveal answer"
    **Correct answer: C**

    HTTP probes validate application-layer readiness, not just socket accept.

    **Related concepts**

    - L7 health checks
    - httpchk

### Question 7

**Drain** on a load-balancer backend means?

**Difficulty:** Intermediate

**Options:**

- **A.** Immediately kill all connections to that node
- **B.** Delete the DNS record
- **C.** Format the disk
- **D.** Stop sending new connections; allow existing sessions to complete

??? success "Reveal answer"
    **Correct answer: D**

    Drain enables zero-downtime maintenance windows.

    **Related concepts**

    - Drain
    - Graceful shutdown

### Question 8

Sticky sessions (session affinity) primarily trade what operational cost?

**Difficulty:** Advanced

**Options:**

- **A.** Faster TLS handshakes always
- **B.** Uneven load distribution and lost sessions when a node fails without external state
- **C.** Lower DNS query volume
- **D.** Automatic firewall rollback

??? success "Reveal answer"
    **Correct answer: B**

    Prefer external session stores over stickiness for new systems.

    **Related concepts**

    - Sticky sessions
    - Load distribution

## Section 2 — Practical Knowledge

### Question 9

In HAProxy with `inter 2s fall 3`, approximately how long until a failing backend is marked DOWN?

**Difficulty:** Intermediate

**Options:**

- **A.** About 6 seconds (three failed checks at 2s interval)
- **B.** Instantly on first failed check
- **C.** Exactly 24 hours
- **D.** Never — TCP checks only

??? success "Reveal answer"
    **Correct answer: A**

    `fall 3` requires three consecutive failures at `inter 2s` spacing.

    **Related concepts**

    - HAProxy health checks
    - inter/fall/rise

### Question 10

After killing one backend in a two-node HAProxy pool with working health checks, user traffic should?

**Difficulty:** Beginner

**Options:**

- **A.** Fail entirely until manual intervention
- **B.** Round-robin to the dead node anyway
- **C.** Route only to surviving healthy backends
- **D.** Switch to UDP

??? success "Reveal answer"
    **Correct answer: C**

    Failed nodes are removed from rotation; survivors absorb load.

    **Related concepts**

    - Failover
    - HAProxy backend state

### Question 11

Why should you confirm **console or serial access** before applying restrictive host firewall rules?

**Difficulty:** Advanced

**Options:**

- **A.** Console speeds up DNS TTL
- **B.** ufw requires serial port licensing
- **C.** HAProxy only runs on serial consoles
- **D.** A bad deny rule can lock out SSH — console is the rollback path

??? success "Reveal answer"
    **Correct answer: D**

    Out-of-band access prevents permanent lockout from ACL mistakes.

    **Related concepts**

    - Console access
    - Firewall change control

### Question 12

Before applying a firewall change, capturing `sudo nft list ruleset` or `ufw status numbered` supports?

**Difficulty:** Intermediate

**Options:**

- **A.** Faster round-robin
- **B.** Documented rollback to the pre-change ruleset
- **C.** Automatic DNS failover
- **D.** Sticky session removal

??? success "Reveal answer"
    **Correct answer: B**

    Export current rules before change — rollback values must exist before you need them.

    **Related concepts**

    - ACL rollback
    - Change control

### Question 13

Lowering DNS TTL to 300 seconds **before** a cutover primarily helps?

**Difficulty:** Intermediate

**Options:**

- **A.** Shorten cache lifetime so rollback or new IPs propagate faster after the change
- **B.** Increase steady-state resolver load forever
- **C.** Disable split-horizon
- **D.** Replace authoritative nameservers

??? success "Reveal answer"
    **Correct answer: A**

    Lower TTL during migration windows reduces stale-cache pain.

    **Related concepts**

    - TTL planning
    - DNS cutover

### Question 14

A tier allow matrix documents?

**Difficulty:** Beginner

**Options:**

- **A.** Only usernames and passwords
- **B.** HAProxy algorithm names only
- **C.** Source zone, destination zone, port, protocol, and business justification
- **D.** Certificate SAN lists only

??? success "Reveal answer"
    **Correct answer: C**

    Matrices make segmentation auditable and reviewable.

    **Related concepts**

    - Tier allow matrix
    - Segmentation

## Section 3 — Scenarios & Operations

### Question 15

Friday 17:00: a new deny rule blocks TCP 443 on the edge LB. Synthetic checks fail globally. First stabilisation step?

**Difficulty:** Advanced

**Options:**

- **A.** Reboot all application servers
- **B.** Raise DNS TTL to 86400
- **C.** Enable sticky sessions
- **D.** Roll back or remove the recent ACL change after confirming scope

??? success "Reveal answer"
    **Correct answer: D**

    Assume recent change until proven otherwise — rollback ACL with documented pre-change export.

    **Related concepts**

    - Incident response
    - ACL rollback

### Question 16

During a deploy, ops sets backend weight to 0 and waits for active sessions to finish before restart. This is?

**Difficulty:** Intermediate

**Options:**

- **A.** Hard failover
- **B.** Graceful drain
- **C.** Split-horizon cutover
- **D.** TTL flush

??? success "Reveal answer"
    **Correct answer: B**

    Drain prevents dropping in-flight user requests during maintenance.

    **Related concepts**

    - Drain
    - Deploy windows

### Question 17

VPN users resolve `app.internal.example.com` to `10.0.1.50`; public resolvers return `203.0.113.10` for `app.example.com`. This illustrates?

**Difficulty:** Intermediate

**Options:**

- **A.** Split-horizon / split DNS views
- **B.** Flat network design
- **C.** HAProxy round-robin
- **D.** TCP health check only

??? success "Reveal answer"
    **Correct answer: A**

    Internal and external names or views differ by design — test both.

    **Related concepts**

    - Split-horizon
    - Production DNS

### Question 18

A canary ACL change should be applied first on?

**Difficulty:** Advanced

**Options:**

- **A.** Every production host simultaneously
- **B.** The database primary only
- **C.** A single non-critical host or port with observation before fleet rollout
- **D.** Public internet root servers

??? success "Reveal answer"
    **Correct answer: C**

    Smallest blast radius: canary one target, validate, then promote via IaC.

    **Related concepts**

    - Canary ACL
    - Blast radius

### Question 19

App tier should accept traffic from which source in a standard three-tier web design?

**Difficulty:** Beginner

**Options:**

- **A.** Any IP on the internet directly to port 8080
- **B.** Database tier only
- **C.** Management bastion on all ports
- **D.** Edge/load-balancer tier CIDR or security group only

??? success "Reveal answer"
    **Correct answer: D**

    App tier trusts edge, not the raw internet — segmentation enforces the hop.

    **Related concepts**

    - Trust zones
    - Tier matrix

## Section 4 — Troubleshooting

### Question 20

First-hour network incident evidence collection should start with which command set?

**Difficulty:** Beginner

**Options:**

- **A.** `rm -rf /` then reboot
- **B.** Structured `curl`, `dig`, and `ss` output saved with UTC timestamps
- **C.** Random log grep with no timestamps
- **D.** Disable all monitoring

??? success "Reveal answer"
    **Correct answer: B**

    curl proves HTTP path; dig proves name resolution; ss proves listeners and connections.

    **Related concepts**

    - Incident response
    - Evidence toolkit

### Question 21

`curl` to `127.0.0.1:18080` returns 200, but `curl` to `edge.rebash.lab:18080` fails. `getent` shows `127.0.0.99`. Likely layer?

**Difficulty:** Intermediate

**Options:**

- **A.** Name resolution / hosts override fault
- **B.** Application crash
- **C.** TLS certificate expiry
- **D.** LVM full

??? success "Reveal answer"
    **Correct answer: A**

    IP works, FQDN fails — suspect DNS or `/etc/hosts` before the app.

    **Related concepts**

    - DNS triage
    - getent vs curl

### Question 22

`ss` shows HAProxy listening on 18080, but `curl` to the edge times out. Firewall was changed recently. Likely cause?

**Difficulty:** Intermediate

**Options:**

- **A.** HAProxy not installed
- **B.** Wrong HTTP health-check path only
- **C.** ACL or security group blocking the path despite process listening
- **D.** DNS TTL too low

??? success "Reveal answer"
    **Correct answer: C**

    Listener present + connection failure → path/ACL or routing, not "process down".

    **Related concepts**

    - ss vs curl
    - Firewall triage

### Question 23

`dig @8.8.8.8` returns empty for an internal hostname, but `getent hosts` resolves it. Best explanation?

**Difficulty:** Advanced

**Options:**

- **A.** dig is broken
- **B.** HAProxy removed the backend
- **C.** TTL is infinite on the internet
- **D.** Public recursive DNS has no record; libc resolver uses `/etc/hosts` or internal stub

??? success "Reveal answer"
    **Correct answer: D**

    dig queries configured resolvers; getent honours local hosts — always check both.

    **Related concepts**

    - dig vs getent
    - Split-horizon

## Section 5 — Architecture

### Question 24

In production, why bind application backends to `127.0.0.1` behind a load balancer?

**Difficulty:** Intermediate

**Options:**

- **A.** To bypass health checks
- **B.** To keep the app off the public exposure path; only the LB front door is reachable
- **C.** Because Python requires localhost
- **D.** To disable round-robin

??? success "Reveal answer"
    **Correct answer: B**

    Localhost bind limits blast radius — clients must traverse the LB tier.

    **Related concepts**

    - Exposure control
    - Edge architecture

### Question 25

Module 7 production network operations integrates which concerns holistically?

**Difficulty:** Advanced

**Options:**

- **A.** Segmentation, DNS change control, LB health checks, ACL rollbacks, and incident timelines
- **B.** Only packet capture with tcpdump
- **C.** Only LVM and fstab
- **D.** Container image scanning only

??? success "Reveal answer"
    **Correct answer: A**

    Module 7 ties trust boundaries through to first-hour incident evidence and rollback discipline.

    **Related concepts**

    - Module 7 capstone
    - Production operations

## Score Summary

| Score | Band | Meaning |
|------:|------|---------|
| 23–25 | Excellent | Ready for edge failover lab and networking interviews |
| 18–22 | Good | Pass — revise weak Module 7 tutorials |
| 12–17 | Needs improvement | Revisit tutorials 21–25 and foundation DNS/firewall labs |
| ≤11 | Restart Module 7 | Work tutorials 21–25 in order |

**Total questions:** 25 · **Passing score:** 18 (70%)

## Recommended Study Areas

- [Networking Module 7](../networking/index.md)
- Lab: [Networking Edge Failover](../labs/networking-edge-failover.md)
- Lab: [DNS and Firewall Site-Down Triage](../labs/networking-dns-firewall-triage.md)
- Cheat sheet: [Networking](../cheatsheets/networking.md)
- Interview: [Networking](../interview/networking.md)

## Interview Connection

Expect trust-zone design, TTL cutover planning, L4 vs L7 health checks, drain vs failover, ACL rollback stories, and first-hour curl/dig/ss triage. Use your Module 7 lab narrative.

## References

1. [HAProxy Documentation](https://docs.haproxy.org/)
2. [RFC 1034 — Domain names](https://datatracker.ietf.org/doc/html/rfc1034)
3. [Network Troubleshooting Methodology](../networking/network-troubleshooting-methodology.md)
