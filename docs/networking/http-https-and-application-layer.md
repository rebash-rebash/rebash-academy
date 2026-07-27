---
title: HTTP, HTTPS, and the Application Layer
description: Master HTTP methods, status codes, headers, cookies, TLS handshakes, curl debugging, and HTTP/1.1 vs HTTP/2 vs HTTP/3 for DevOps production work.
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - http
  - https
  - tls
  - curl
  - application-layer
  - status-codes
prerequisites:
  - Complete DNS Records and Troubleshooting or understand hostname resolution
  - TCP and UDP Deep Dive — ports, connections, and socket basics
  - Linux environment with curl and openssl installed
comments: false
---

# HTTP, HTTPS, and the Application Layer

## Overview

**HTTP** is the language of the web — and of most microservice communication. Every `curl`, browser request, Kubernetes liveness probe, and CI/CD webhook speaks HTTP or its encrypted sibling **HTTPS**. As a DevOps engineer, you debug **502 Bad Gateway**, **413 Payload Too Large**, **301 redirect loops**, and **certificate expired** errors daily. These are application-layer problems that sit above TCP and DNS but depend on both working correctly.

This tutorial is **Tutorial 10** in **Module 4: Application Layer** of the REBASH Academy Networking series. You will learn HTTP request/response structure, status codes, essential headers, how **TLS** secures HTTPS, and practical **`curl`** techniques for production troubleshooting. For transport-layer details, see [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md).

## Prerequisites

- [DNS Fundamentals](dns-fundamentals.md) — hostname resolution before HTTP connects
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md) — ports 80/443, connection states
- Linux VM or local machine with `curl`, `openssl`, and optional `httpie`
- Basic familiarity with web applications and APIs

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Describe HTTP request and response structure (method, path, headers, body)
- [ ] Explain common HTTP methods and when to use each (GET, POST, PUT, PATCH, DELETE)
- [ ] Interpret status code classes (1xx–5xx) and diagnose production errors
- [ ] Use essential headers (Host, Content-Type, Authorization, Cache-Control, Cookie)
- [ ] Explain the TLS handshake and what HTTPS adds beyond HTTP
- [ ] Debug HTTP with `curl -v`, `-I`, `-L`, and `--resolve`
- [ ] Compare HTTP/1.1, HTTP/2, and HTTP/3 at a high level
- [ ] Relate application-layer concepts to load balancers and reverse proxies

## Architecture Diagram

```mermaid
sequenceDiagram
    participant Client as curl / Browser
    participant DNS as DNS Resolver
    participant LB as Load Balancer
    participant TLS as TLS Termination
    participant App as Application Server

    Client->>DNS: Resolve api.example.com
    DNS->>Client: 203.0.113.10
    Client->>LB: TCP SYN :443
    LB->>Client: TCP SYN-ACK (established)
    Client->>TLS: ClientHello (TLS 1.3)
    TLS->>Client: ServerHello + Certificate
    Client->>TLS: Encrypted HTTP GET /health

    alt L7 routing
        LB->>App: Forward GET /health (HTTP or re-encrypted)
    end

    App->>LB: 200 OK {"status":"ok"}
    LB->>Client: 200 OK (encrypted)```

## Theory

### Application Layer in the Stack

In the **TCP/IP model**, HTTP operates at the **Application layer** (Layer 7 in OSI terms). It assumes reliable transport (TCP, or QUIC over UDP for HTTP/3) and assumes the client already resolved the hostname via DNS.

| Layer | Protocol | DevOps touchpoint |
|-------|----------|-------------------|
| Application | HTTP, HTTPS, gRPC | Ingress, API gateways, health checks |
| Transport | TCP, UDP | Connection timeouts, port 443 |
| Network | IP | Routing, security groups |
| Link | Ethernet | Rarely direct concern |

### HTTP Request Structure

An HTTP request consists of:

```http
GET /api/v1/users HTTP/1.1
Host: api.example.com
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
User-Agent: curl/8.5.0

```

| Component | Purpose |
|-----------|---------|
| **Request line** | Method, path, HTTP version |
| **Headers** | Metadata (Host, auth, content type, cookies) |
| **Blank line** | Separates headers from body |
| **Body** | Optional payload (POST/PUT/PATCH) |

The **Host header** is mandatory in HTTP/1.1 — it enables **virtual hosting** (many sites on one IP). Load balancers and ingress controllers route based on Host and path.

### HTTP Methods

| Method | Idempotent | Safe | Typical Use |
|--------|------------|------|-------------|
| **GET** | Yes | Yes | Retrieve resource |
| **POST** | No | No | Create resource, submit form |
| **PUT** | Yes | No | Replace resource entirely |
| **PATCH** | No | No | Partial update |
| **DELETE** | Yes | No | Remove resource |
| **HEAD** | Yes | Yes | Like GET but headers only |
| **OPTIONS** | Yes | Yes | CORS preflight, capability discovery |

**Idempotent** means multiple identical requests have the same effect as one. **Safe** means no state change on the server. POST retry logic must handle duplicate submissions; GET can be retried freely.

### HTTP Response and Status Codes

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 47
Cache-Control: no-cache

{"status":"ok","version":"2.1.0"}
```

Status codes are grouped by first digit:

| Class | Range | Meaning | Examples |
|-------|-------|---------|----------|
| **1xx** | 100–199 | Informational | 100 Continue, 101 Switching Protocols |
| **2xx** | 200–299 | Success | 200 OK, 201 Created, 204 No Content |
| **3xx** | 300–399 | Redirection | 301 Moved Permanently, 302 Found, 304 Not Modified |
| **4xx** | 400–499 | Client error | 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Too Many Requests |
| **5xx** | 500–599 | Server error | 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout |

Production debugging shortcuts:

- **502** — Load balancer/proxy received invalid response from upstream (app crashed, wrong port, protocol mismatch)
- **503** — Service unavailable (maintenance, overload, no healthy backends)
- **504** — Upstream timeout (slow app, database lock, missing health check)
- **421 Misdirected Request** — TLS/SNI routed to wrong backend (common in multi-tenant ingress)

### Essential Headers

| Header | Purpose |
|--------|---------|
| **Host** | Target hostname for virtual hosting |
| **Content-Type** | Body format (`application/json`, `multipart/form-data`) |
| **Content-Length** | Body size in bytes |
| **Authorization** | Credentials (Bearer token, Basic auth) |
| **Cookie / Set-Cookie** | Session state |
| **Cache-Control** | Caching policy (`max-age`, `no-store`) |
| **Location** | Redirect target (3xx responses) |
| **X-Forwarded-For** | Original client IP (added by proxies) |
| **X-Request-ID** | Correlation ID for distributed tracing |

!!! note "X-Forwarded-* trust"
    Only trust `X-Forwarded-For` and `X-Forwarded-Proto` from known proxies (load balancer, ingress). Clients can spoof these if the app accepts them directly from the internet.

### HTTPS and TLS

**HTTPS** is HTTP over **TLS (Transport Layer Security)**. TLS provides:

- **Confidentiality** — encrypted data in transit
- **Integrity** — tampering detection
- **Authentication** — server (and optionally client) identity via certificates

#### TLS 1.3 Handshake (simplified)

1. **ClientHello** — supported ciphers, TLS version, SNI (server hostname)
2. **ServerHello** — chosen cipher, certificate chain
3. **Key exchange** — (ECDHE) establishes session keys
4. **Encrypted application data** — HTTP request/response flows encrypted

**SNI (Server Name Indication)** lets multiple HTTPS sites share one IP — the client sends the hostname during handshake. Missing or wrong SNI causes certificate mismatch errors.

Certificate validation checks:

- Hostname matches certificate CN/SAN
- Chain trusted by system CA store
- Not expired (`notBefore` / `notAfter`)
- Not revoked (OCSP stapling where supported)

### HTTP Versions

| Version | Transport | Key Features |
|---------|-----------|--------------|
| **HTTP/1.1** | TCP | Persistent connections, chunked encoding, pipelining (limited) |
| **HTTP/2** | TCP | Multiplexing, header compression (HPACK), server push (rarely used) |
| **HTTP/3** | QUIC (UDP) | Multiplexing without head-of-line blocking, faster handshake |

Most production ingress controllers terminate HTTP/2 from clients and may speak HTTP/1.1 to backends. Check with `curl -v --http2`.

### Cookies and Sessions

**Set-Cookie** from server stores session ID in browser. **Cookie** header sends it back on subsequent requests. Attributes matter for security:

| Attribute | Purpose |
|-----------|---------|
| **HttpOnly** | JavaScript cannot access — mitigates XSS theft |
| **Secure** | Sent only over HTTPS |
| **SameSite** | CSRF mitigation (`Strict`, `Lax`, `None`) |
| **Domain / Path** | Scope of cookie |

Load balancers use **session affinity (sticky sessions)** via cookie injection when stateful apps require it — prefer stateless design when possible.

## Hands-on Lab

These exercises use public endpoints. Replace URLs with your own services for deeper practice.

### Step 1 – Basic GET request

**Command:**

```bash
curl -s -o /dev/null -w "HTTP %{http_code} in %{time_total}s\n" https://example.com
curl -s -D - -o /dev/null https://example.com | head -15
```

**Explanation:** First command shows status and timing. Second dumps response headers only.

**Expected output:**

```text
HTTP 200 in 0.234567s
HTTP/2 200
content-type: text/html; charset=UTF-8
...
```

### Step 2 – Verbose request with TLS details

**Command:**

```bash
curl -v --http1.1 https://example.com 2>&1 | head -35
```

**Explanation:** `-v` shows TCP connection, TLS handshake, certificate info, and HTTP headers. Essential for HTTPS debugging.

**Expected output:**

```text
* Connected to example.com (93.184.216.34) port 443
* TLSv1.3 (OUT), TLS handshake, Client hello
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate: subject: CN=example.com
> GET / HTTP/1.1
< HTTP/1.1 200 OK
```

### Step 3 – HEAD request (headers only)

**Command:**

```bash
curl -I https://example.com
curl -sI https://example.com | grep -iE '^(HTTP|cache|content-type|server|location)'
```

**Explanation:** HEAD is useful for health checks without downloading body. `-I` is shorthand for HEAD.

### Step 4 – Follow redirects

**Command:**

```bash
curl -sI -L http://example.com 2>&1 | grep -E '^HTTP|^Location'
curl -s -o /dev/null -w "Final URL: %{url_effective}\nCode: %{http_code}\n" -L http://example.com
```

**Explanation:** `-L` follows 301/302 redirects. Watch for redirect loops (max 50 by default).

**Expected output:**

```text
HTTP/1.1 301 Moved Permanently
Location: https://example.com/
HTTP/2 200
Final URL: https://example.com/
Code: 200
```

### Step 5 – POST JSON with headers

**Command:**

```bash
curl -s -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: lab-$(date +%s)" \
  -d '{"service":"api","status":"test"}' | head -20
```

**Explanation:** httpbin.org echoes request for learning. In production, replace with your API endpoint.

### Step 6 – Inspect certificate with openssl

**Command:**

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -subject -issuer -dates
```

**Explanation:** Validates certificate subject, issuer, and expiry without HTTP layer. Use when curl reports SSL errors.

**Expected output:**

```text
subject=CN=example.com
issuer=C=US, O=DigiCert Inc, CN=DigiCert Global G3 TLS ECC SHA384 2020 CA1
notBefore=Jan 15 00:00:00 2024 GMT
notAfter=Feb 16 23:59:59 2025 GMT
```

### Step 7 – Test specific Host header (virtual hosting)

**Command:**

```bash
curl -sI -H "Host: example.com" http://93.184.216.34 2>&1 | head -5
curl -sI --resolve example.com:443:93.184.216.34 https://example.com | head -5
```

**Explanation:** `--resolve` forces DNS mapping for testing before propagation. Host header routes to correct vhost on shared IP.

### Step 8 – Compare HTTP/1.1 and HTTP/2

**Command:**

```bash
curl -s -o /dev/null -w "HTTP/1.1: %{http_version} %{http_code}\n" --http1.1 https://example.com
curl -s -o /dev/null -w "HTTP/2:   %{http_version} %{http_code}\n" --http2 https://example.com
```

**Explanation:** Confirms server HTTP/2 support. ALPN negotiates during TLS handshake.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `curl -v URL` | Verbose HTTP + TLS debug | `curl -v https://api.example.com` |
| `curl -I URL` | HEAD request (headers only) | `curl -I https://example.com` |
| `curl -L URL` | Follow redirects | `curl -L http://example.com` |
| `curl -X METHOD` | Specify HTTP method | `curl -X DELETE URL` |
| `curl -H "Header: val"` | Custom request header | `curl -H "Accept: application/json"` |
| `curl -d 'data'` | POST body | `curl -d "name=test" URL` |
| `curl --resolve` | Override DNS for test | `curl --resolve host:443:IP https://host` |
| `curl -w '%{http_code}'` | Print status code only | `curl -s -o /dev/null -w '%{http_code}' URL` |
| `openssl s_client` | TLS/certificate inspection | `openssl s_client -connect host:443` |

### HTTP health check script

```bash
#!/usr/bin/env bash
# http-health.sh — quick endpoint check for monitoring
set -euo pipefail
URL="${1:?Usage: http-health.sh https://example.com/health}"
TIMEOUT="${2:-5}"

code=$(curl -s -o /dev/null -w '%{http_code}' --max-time "$TIMEOUT" "$URL")
time_total=$(curl -s -o /dev/null -w '%{time_total}' --max-time "$TIMEOUT" "$URL")

if [[ "$code" =~ ^2 ]]; then
  echo "OK  $URL → HTTP $code (${time_total}s)"
  exit 0
else
  echo "FAIL $URL → HTTP $code (${time_total}s)"
  exit 1
fi
```

## Common Mistakes

!!! warning "Ignoring redirect chains"
    HTTP → HTTPS redirects add latency. Point health checks and internal services directly at HTTPS endpoints.

!!! warning "Hardcoding HTTP in production"
    Mixed content, session hijacking, and cookie theft. Enforce HTTPS with HSTS after validating TLS works.

!!! warning "Trusting X-Forwarded-For from clients"
    Use only when request passes through known load balancer. Otherwise, log the TCP source IP.

!!! warning "502 blamed on application when upstream is wrong"
    502 often means LB cannot reach backend port or backend speaks wrong protocol (HTTP vs HTTPS mismatch).

!!! warning "Certificate hostname mismatch"
    Cert issued for `*.example.com` does not cover `example.com` unless SAN includes apex. Check with openssl.

## Best Practices

!!! tip "Use curl -v as first HTTP debug step"
    Faster than tcpdump for most L7 issues — shows DNS, TCP, TLS, request, and response in one output.

!!! tip "Set reasonable timeouts everywhere"
    Client, load balancer, and application timeouts should decrease down the chain — avoid 504 cascades.

!!! tip "Return meaningful 4xx/5xx with correlation IDs"
    `X-Request-ID` in logs links user report to server trace instantly.

!!! tip "Prefer 301 over 302 for permanent HTTPS migration"
    301 is cached by browsers; 302 may be re-evaluated repeatedly.

!!! tip "Monitor certificate expiry proactively"
    Alert at 30/14/7 days before expiry. Automate renewal with ACME (Let's Encrypt, cert-manager).

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `502 Bad Gateway` | Backend down, wrong port, protocol mismatch | Check upstream health; verify HTTP vs HTTPS to backend |
| `503 Service Unavailable` | No healthy backends, maintenance mode | Inspect LB target group; review health check path |
| `504 Gateway Timeout` | Backend slower than LB timeout | Increase timeout or fix slow queries; align timeout chain |
| `Connection refused` on :443 | Nothing listening or wrong IP | `ss -tlnp`; verify DNS points to correct LB |
| `SSL certificate problem` | Expired, wrong hostname, untrusted CA | `openssl s_client`; renew cert; fix SAN |
| Redirect loop | HTTP/HTTPS misconfiguration | Check `X-Forwarded-Proto`; fix ingress annotations |
| `421 Misdirected Request` | SNI/route mismatch on shared ingress | Verify Host header and TLS cert match route |
| Slow first request | Cold start or DNS/TLS overhead | Enable keep-alive; HTTP/2; connection pooling |
| 413 Payload Too Large | Body exceeds limit | Increase client_max_body_size / LB limit |
| CORS errors in browser | Missing Access-Control headers | Server-side CORS config — not visible in curl alone |

## Summary

- **HTTP** is the application-layer protocol for web and API communication — built on TCP (or QUIC for HTTP/3)
- **Methods** (GET, POST, PUT, DELETE) and **status codes** (2xx–5xx) tell you what happened at L7
- **Headers** carry metadata: Host for routing, Authorization for auth, Cache-Control for caching
- **HTTPS** adds TLS encryption and certificate-based server authentication
- **`curl -v`** is the primary DevOps tool for HTTP/TLS debugging
- **502/503/504** at the load balancer usually mean upstream or timeout issues — not always application bugs
- Understand **HTTP/2** multiplexing and **HTTP/3** QUIC benefits for modern ingress design

## Interview Questions

1. What are the main parts of an HTTP request?
2. Explain the difference between 301 and 302 redirects.
3. What does a 502 Bad Gateway mean at the load balancer?
4. How does TLS differ from HTTP?
5. What is the purpose of the Host header?
6. Which HTTP methods are idempotent and safe?
7. What is SNI and why does it matter for HTTPS?
8. How would you debug a certificate expiry issue?
9. Compare HTTP/1.1, HTTP/2, and HTTP/3.
10. What is the difference between 401 Unauthorized and 403 Forbidden?

??? tip "Sample Answers (Questions 3, 4, and 10)"

    **Q3 — 502 Bad Gateway:** The load balancer or reverse proxy received an invalid or no response from the upstream backend. Common causes: backend process crashed, wrong port configured, backend speaks HTTP while proxy expects HTTPS (or vice versa), or connection reset mid-response.

    **Q4 — TLS vs HTTP:** HTTP defines request/response semantics for applications. TLS operates below HTTP, encrypting the TCP connection and authenticating the server via certificates. HTTPS is HTTP running inside a TLS-encrypted tunnel.

    **Q10 — 401 vs 403:** 401 Unauthorized means authentication is required or credentials are invalid — client should retry with valid auth. 403 Forbidden means the server understood the request and identity but refuses to authorize access — retrying with same credentials will not help.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [DNS Records and Troubleshooting](dns-records-and-troubleshooting.md) *(previous — Module 3)*
- [Firewalls and Access Control](firewalls-and-access-control.md) *(next in Module 4)*
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- [Load Balancing Fundamentals](load-balancing-fundamentals.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 9110 — HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9112 — HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112)
- [RFC 9113 — HTTP/2](https://www.rfc-editor.org/rfc/rfc9113)
- [RFC 9114 — HTTP/3](https://www.rfc-editor.org/rfc/rfc9114)
- [RFC 8446 — TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [curl man page](https://curl.se/docs/manpage.html)
- [REBASH Academy – Networking Overview](index.md)
