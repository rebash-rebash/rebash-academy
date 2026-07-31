---
title: "HTTP, HTTPS, and the Application Layer"
description: "Master HTTP methods, status codes, headers, cookies, TLS and certificates, curl debugging, and HTTP/1.1 vs HTTP/2 vs HTTP/3 for Cloud and DevOps work."
difficulty: intermediate
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 10 · HTTP & HTTPS"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - linux-administrator
  - site-reliability-engineer
  - kubernetes-engineer
skills:
  - http
  - https
  - tls
  - curl
prerequisites:
  - networking/dns-records-and-troubleshooting
next:
  - networking/nat-and-port-forwarding
related:
  - networking/tcp-and-udp-deep-dive
  - networking/reverse-proxy-and-ingress-basics
  - networking/load-balancing-fundamentals
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - http
  - https
  - tls
  - curl
  - status-codes
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# HTTP, HTTPS, and the Application Layer

## Overview

Read and debug HTTP request/response traffic with `curl`, interpret status codes and headers, and explain what TLS adds for HTTPS — including certificates at a practical level.

**HTTP** is how browsers, APIs, probes, and webhooks talk. **HTTPS** is HTTP over **TLS (Transport Layer Security)**. DevOps work is full of 502/503/504, redirect loops, expired certificates, and Host-header routing mistakes that sit above TCP and DNS.

This is **Module 10 — HTTP & HTTPS**. Complete [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 10 · HTTP & HTTPS** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — ports 80/443
- Linux host with `curl` and `openssl`

### Recommended

- Basic API or web app familiarity

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe HTTP request/response structure  
- [ ] Choose common methods (GET, POST, PUT, PATCH, DELETE, HEAD)  
- [ ] Interpret 2xx–5xx status classes in production  
- [ ] Use Host, Content-Type, Authorization, Cookie, Cache-Control  
- [ ] Explain TLS, certificates, and HTTPS at an ops level  
- [ ] Debug with `curl -v`, `-I`, `-L`, `--resolve`  
- [ ] Compare HTTP/1.1, HTTP/2, and HTTP/3 briefly  
- [ ] Relate HTTP to reverse proxies and ingress

## Architecture

Client → TLS → HTTP semantics, often via a reverse proxy or ingress.

![HTTP and HTTPS path](../assets/excalidraw/http-https.svg)

## Theory

### Where HTTP sits

In TCP/IP, HTTP is an **application** protocol. It needs DNS for names and TCP (or QUIC/UDP for HTTP/3) for transport.

| Concern | Protocol | Ops touchpoint |
|---------|----------|----------------|
| App | HTTP/HTTPS | Ingress, gateways, probes |
| Transport | TCP / QUIC | Timeouts, 443 |
| Network | IP | Routes, security groups |

### Request structure

```http
GET /api/v1/users HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer <token>
```

| Part | Role |
|------|------|
| Request line | Method, path, version |
| Headers | Metadata |
| Blank line | End of headers |
| Body | Optional payload |

**Host** is required in HTTP/1.1 and drives virtual hosting / ingress routing.

### Methods

| Method | Idempotent | Safe | Typical use |
|--------|------------|------|-------------|
| GET | Yes | Yes | Read |
| POST | No | No | Create / actions |
| PUT | Yes | No | Replace |
| PATCH | No* | No | Partial update |
| DELETE | Yes | No | Remove |
| HEAD | Yes | Yes | Headers only |
| OPTIONS | Yes | Yes | CORS / capabilities |

\*PATCH semantics vary by API — treat retries carefully.

### Status codes

| Class | Meaning | Ops examples |
|-------|---------|--------------|
| 2xx | Success | 200, 201, 204 |
| 3xx | Redirect | 301, 302, 304 |
| 4xx | Client | 400, 401, 403, 404, 429 |
| 5xx | Server / gateway | 500, 502, 503, 504 |

Shortcuts:

- **502** — proxy got a bad upstream response  
- **503** — no healthy backend / overload / maintenance  
- **504** — upstream timed out  

### Essential headers

| Header | Purpose |
|--------|---------|
| Host | Virtual host target |
| Content-Type | Body format |
| Authorization | Credentials |
| Cookie / Set-Cookie | Session |
| Cache-Control | Caching policy |
| Location | Redirect target |
| X-Forwarded-For | Original client IP via proxies |
| X-Request-ID | Correlation |

### Cookies and sessions

Cookies store client-side session identifiers. Secure apps set `Secure`, `HttpOnly`, and appropriate `SameSite`. Sticky load balancing sometimes keys on cookies — know when affinity is cookie-based vs IP-based.

### TLS and certificates

HTTPS = HTTP inside a TLS session. Rough ops view:

1. Client connects (SNI often selects certificate)  
2. Server presents certificate chain  
3. Client validates trust, hostname, expiry  
4. Symmetric keys protect the HTTP bytes  

You will debug: expired certs, name mismatch, incomplete chain, and TLS version/cipher policy at load balancers.

### HTTP versions

| Version | Transport notes | Ops note |
|---------|-----------------|----------|
| HTTP/1.1 | TCP, often many connections | Host header, keep-alive |
| HTTP/2 | TCP, multiplexing | One connection, streams |
| HTTP/3 | QUIC over UDP | Different firewall/path needs |

### Reverse proxy / ingress

Proxies terminate TLS, route on Host/path, add forwarding headers, and return gateway status codes. Details continue in [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md).

## Hands-on Lab

**Focus:** practise the core workflow for HTTP, HTTPS, and the Application Layer

```bash
mkdir -p ~/rebash-networking/module-10
cd ~/rebash-networking/module-10

sudo apt-get update
sudo apt-get install -y curl openssl
```

```bash
curl --version | head -1
openssl version
```

### Step 1 – Verbose GET

```bash
curl -v https://example.com/ -o /dev/null
```

Note DNS, TCP, TLS handshake lines, then HTTP status and headers.

### Step 2 – Headers only and redirects

```bash
curl -I https://example.com/
curl -sI -L https://httpbin.org/redirect/2 | head -40
```

### Step 3 – Methods and status

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://httpbin.org/status/404
curl -s -o /dev/null -w "%{http_code}\n" -X POST https://httpbin.org/post
```

### Step 4 – Custom Host / resolve

```bash
curl -sI --resolve example.com:443:93.184.216.34 https://example.com/ | head -15
```

Useful when DNS is wrong but you need to hit a known VIP.

### Step 5 – Certificate inspection

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

### Step 6 – Correlate with transport

```bash
curl -s -o /dev/null https://example.com/
ss -tn state established '( dport = :443 or sport = :443 )' | head -5
```

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-10/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **HTTP, HTTPS, and the Application Layer** always combines:

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

!!! warning "Skipping fundamentals for HTTP, HTTPS, and the Application Layer"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for HTTP, HTTPS, and the Application Layer"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode HTTP, HTTPS, and the Application Layer changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| 502 Bad Gateway | Upstream dead / wrong port | Check backend listen; proxy upstream config |
| 503 | No healthy targets | Health checks; scale; drain |
| 504 | Slow upstream | Timeouts; DB locks; app latency |
| Redirect loop | Mixed HTTP/HTTPS or cookie rules | Trace `-L` carefully; check proxy redirects |
| Certificate error | Expiry / name / chain | `openssl s_client`; fix cert or SNI |
| Empty response | TLS or HTTP mismatch | Confirm scheme and port |

## Summary

- HTTP is request line + headers + optional body  
- Status classes separate client, redirect, and gateway failures  
- HTTPS adds TLS trust and encryption on top of HTTP  
- **`curl`** and **`openssl`** are the everyday debug tools  
- Proxies and ingress sit in the path and own many 5xx codes

## Interview Questions

1. How does **HTTP, HTTPS, and the Application Layer** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [NAT and Port Forwarding](nat-and-port-forwarding.md)  
- [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md)  
- [Load Balancing Fundamentals](load-balancing-fundamentals.md)

## References

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)  
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)  
- [curl man page](https://curl.se/docs/manpage.html)
