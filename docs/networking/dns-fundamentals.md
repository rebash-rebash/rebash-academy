---
title: "DNS Fundamentals"
description: "Understand DNS hierarchy, recursive vs iterative resolution, stub and recursive resolvers, Linux name resolution, and hands-on dig and nslookup labs."
difficulty: beginner
estimated_time: "40–55 min"
technology: networking
category: networking
module: "Module 9 · DNS"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - dns
  - dig
  - resolvers
  - nameservers
prerequisites:
  - networking/tcp-and-udp-deep-dive
next:
  - networking/dns-records-and-troubleshooting
related:
  - networking/production-dns-operations
  - networking/http-https-and-application-layer
  - linux/linux-networking-tools
labs:
  - labs/networking-dns-firewall-triage
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - dns
  - dig
  - nslookup
  - resolvers
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# DNS Fundamentals

## Overview

Explain the DNS hierarchy, recursive vs iterative queries, how Linux resolves names, and use `dig` to prove a resolution path end to end.

**DNS (Domain Name System)** maps names to addresses. When DNS fails, applications look like a network outage even if routes and firewalls are healthy. Cloud cutovers, Kubernetes services, and certificate validation all depend on correct resolution and caching.

This is the first tutorial in **Module 9 — DNS**. Complete [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) first (UDP/TCP port 53). Diagrams use Excalidraw only.

This is a core tutorial in **Module 9 · DNS** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- Linux host with outbound DNS allowed
- `dig` / `nslookup` (`dnsutils` on Debian/Ubuntu)

### Recommended

- Ability to edit `/etc/hosts` for a short lab override

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe the hierarchy from root → TLD → authoritative zone  
- [ ] Distinguish recursive vs iterative queries  
- [ ] Explain stub resolvers, recursive resolvers, and TTL caching  
- [ ] Inspect `/etc/hosts`, `/etc/resolv.conf`, and systemd-resolved behaviour  
- [ ] Use `dig` and interpret QUESTION/ANSWER/AUTHORITY sections  
- [ ] Trace delegation with `dig +trace`

## Architecture

The stub asks a recursive resolver; the recursive walker walks root → TLD → authoritative.

![DNS resolution path](../assets/excalidraw/dns-resolution.svg)

## Theory

### Why DNS exists

Addresses change; names stay stable. Applications call `getaddrinfo()`; resolvers chase records. Queries are usually **UDP/53**; large answers and zone transfers use **TCP/53**.

### Namespace hierarchy

Names are read **right to left**, ending at the root `.`:

```text
www.api.example.com.
│   │   │       └── TLD: com
│   │   └────────── domain: example
│   └────────────── subdomain: api
└────────────────── host: www
```

| Level | Example | Role |
|-------|---------|------|
| Root | `.` | Root server operators |
| TLD | `.com` | Registry |
| Zone | `example.com` | Organisation / DNS host |
| Name | `api.example.com` | Owner-managed labels |

**Delegation** uses **NS** records: the parent says “ask these servers for the child zone.”

### Recursive vs iterative

| Type | Who | Behaviour |
|------|-----|-----------|
| **Recursive** | Resolver for the client | Chases referrals until answer or NXDOMAIN |
| **Iterative** | Each server in the chain | Returns answer or referral; querier continues |

Your configured nameserver (public resolver, corporate DNS, or `127.0.0.53`) is usually **recursive**. Root and TLD servers answer **iteratively**.

The **stub resolver** (glibc / systemd-resolved) forwards to the recursive resolvers listed for the host; it does not walk the whole tree itself.

### Caching and TTL

Answers cache for the record **TTL**. Short TTL speeds failover; long TTL cuts query load but slows change. Negative answers (NXDOMAIN) also cache (negative TTL from SOA).

### Linux resolution order

`/etc/nsswitch.conf` often has:

```text
hosts: files dns myhostname
```

1. **`files`** — `/etc/hosts`  
2. **`dns`** — via `/etc/resolv.conf`  
3. **`myhostname`** — local hostname helpers  

`dig` talks to DNS directly and **bypasses** nsswitch — a stale `/etc/hosts` entry can break `curl` while `dig` looks fine.

| File | Purpose |
|------|---------|
| `/etc/hosts` | Static overrides |
| `/etc/resolv.conf` | Nameservers, search, options |
| `/etc/nsswitch.conf` | Lookup order |
| systemd-resolved stub | Often `127.0.0.53` |

On systemd hosts, prefer **netplan**, **NetworkManager**, or **`resolvectl`** over hand-editing a managed `resolv.conf`.

### dig sections and flags

- **QUESTION** — what was asked  
- **ANSWER** — matching records  
- **AUTHORITY** — NS for the zone  
- **ADDITIONAL** — glue (A/AAAA for NS names)  

Useful flags: `qr`, `aa` (authoritative), `rd`/`ra` (recursion), `ad` (DNSSEC authenticated).

## Hands-on Lab

**Focus:** practise the core workflow for DNS Fundamentals

```bash
mkdir -p ~/rebash-networking/module-09
cd ~/rebash-networking/module-09

sudo apt-get update
sudo apt-get install -y dnsutils
```

```bash
dig -v
resolvectl status 2>/dev/null | head -20 || cat /etc/resolv.conf
```

### Step 1 – Basic lookups

```bash
dig example.com A +noall +answer
dig example.com AAAA +short
```

### Step 2 – Full output

```bash
dig example.com
```

Note HEADER status (`NOERROR`), flags, TTL, and ANSWER.

### Step 3 – Query a specific server

```bash
dig @8.8.8.8 example.com A +short
dig @1.1.1.1 example.com A +short
```

### Step 4 – Trace delegation

```bash
dig +trace example.com A | head -80
```

You should see root → TLD → authoritative answers.

### Step 5 – Hosts override vs dig

```bash
# Observe current resolution path for applications
getent hosts example.com || true
dig +short example.com
```

Optional (lab only — revert after):

```bash
# echo '127.0.0.1 example.com' | sudo tee -a /etc/hosts
# getent hosts example.com
# dig +short example.com   # still public DNS
# sudo sed -i '/example.com/d' /etc/hosts
```

### Step 6 – Resolver config

```bash
cat /etc/resolv.conf
resolvectl query example.com 2>/dev/null || true
```

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-09/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **DNS Fundamentals** always combines:

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

!!! warning "Skipping fundamentals for DNS Fundamentals"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for DNS Fundamentals"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode DNS Fundamentals changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Apps fail, dig works | `/etc/hosts` or nsswitch | Check `getent hosts`; compare with `dig` |
| dig SERVFAIL | Resolver or upstream broken | Try `@8.8.8.8`; check corporate DNS |
| dig NXDOMAIN | Name missing or wrong zone | Confirm spelling; check authoritative NS |
| Slow resolution | Search domains / timeouts | Inspect `resolv.conf` options and search list |
| Intermittent wrong IP | Stale cache / short TTL race | Check TTL; flush local cache (`resolvectl flush-caches`) |

## Summary

- DNS is a **delegated hierarchy** ending at authoritative zones  
- Clients use a **stub**; **recursive** resolvers walk the tree  
- **TTL** controls cache freshness  
- Linux apps go through **nsswitch**; `dig` does not  
- **`dig +trace`** proves the delegation path

## Interview Questions

1. How does **DNS Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md)  
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)  
- [Production DNS Operations](production-dns-operations.md)  
- [Networking Cheat Sheet](../cheatsheets/networking.md)

## References

- [RFC 1034 / 1035 — DNS](https://www.rfc-editor.org/rfc/rfc1034)  
- [dig(1)](https://manpages.debian.org/dig.1)  
- [systemd-resolved](https://www.freedesktop.org/software/systemd/man/systemd-resolved.service.html)
