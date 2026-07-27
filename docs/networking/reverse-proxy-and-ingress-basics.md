---
title: Reverse Proxy and Ingress Basics
description: Configure nginx and HAProxy as reverse proxies, terminate TLS at the edge, route traffic with Kubernetes Ingress, and understand when to proxy vs load balance.
difficulty: intermediate
estimated_time: "40 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - reverse-proxy
  - nginx
  - haproxy
  - ingress
  - kubernetes
  - tls
prerequisites:
  - Complete [Load Balancing Fundamentals](load-balancing-fundamentals.md) or equivalent
  - Understanding of HTTP/HTTPS from [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
  - Linux VM with sudo access; optional Kubernetes cluster for Ingress lab
comments: false
---

# Reverse Proxy and Ingress Basics

## Overview

A **reverse proxy** sits in front of backend servers and handles client requests on their behalf. Unlike a forward proxy (which protects clients), a reverse proxy protects and scales **servers**. It terminates TLS, routes requests by hostname or path, caches static assets, rate-limits abusive clients, and hides internal topology from the internet. Every production web stack uses reverse proxies — nginx in front of Node.js, HAProxy in front of microservices, AWS ALB acting as a managed reverse proxy, or Kubernetes **Ingress** controllers distributing HTTP traffic to pods.

Confusing reverse proxies with load balancers causes architectural mistakes. Load balancers distribute connections across **multiple identical backends**; reverse proxies add **application-aware** behavior — URL rewriting, header injection, WebSocket upgrades, and authentication at the edge. In practice, one component often does both: an ALB load-balances and terminates TLS; nginx reverse-proxies and load-balances upstream pools.

This is **Tutorial 13** in **Module 4: Application Layer** of the REBASH Academy Networking series. It follows our [documentation standards](../about.md#documentation-standards) with theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [Load Balancing Fundamentals](load-balancing-fundamentals.md) — understand L4 vs L7, health checks, and backend pools
- Familiarity with HTTP methods, headers, and status codes from [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- Linux VM (Ubuntu 22.04+) with `sudo`; Docker optional for multi-backend lab
- Optional: local Kubernetes cluster (minikube, kind, or k3s) for Ingress exercises
- Basic comfort editing configuration files and reloading services

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the difference between forward proxy, reverse proxy, and load balancer roles
- [ ] Configure nginx as a reverse proxy with upstream pools and TLS termination
- [ ] Route traffic by hostname and URL path using proxy rules
- [ ] Describe Kubernetes Ingress architecture and common controller implementations
- [ ] Choose between terminating TLS at the proxy vs passing through to backends
- [ ] Debug common reverse proxy failures (502, 504, wrong backend routing)

## Architecture Diagram

Clients connect to the reverse proxy; the proxy forwards requests to internal backends that are not directly exposed.

```mermaid
flowchart LR
    subgraph Internet
        C[Clients]
    end

    subgraph Edge["Reverse Proxy / Ingress"]
        RP["nginx / HAProxy / Ingress Controller"]
        TLS[TLS Termination]
    end

    subgraph Internal["Private Network"]
        B1["Backend 1<br/>app:8080"]
        B2["Backend 2<br/>app:8080"]
        API["API Service<br/>api:3000"]
    end

    C -->|HTTPS 443| RP
    RP --> TLS
    TLS -->|HTTP| B1
    TLS -->|HTTP| B2
    TLS -->|/api/*| API```

## Theory

### Forward Proxy vs Reverse Proxy

A **forward proxy** (corporate proxy, VPN egress) sits between **clients** and the internet. Clients configure the proxy; the destination server sees the proxy's IP, not the client's. Use cases: content filtering, anonymization, caching outbound requests.

A **reverse proxy** sits between the **internet and servers**. Clients connect to the proxy's public address; the proxy selects a backend and forwards the request. Backends may listen only on private IPs — the reverse proxy is the sole public entry point.

| Role | Protects | Client knows | Server sees |
|------|----------|--------------|-------------|
| Forward proxy | Client | Must configure proxy | Proxy IP |
| Reverse proxy | Server | Connects to proxy URL | Proxy-added headers (X-Forwarded-For) |
| Load balancer | Server fleet | Single VIP/DNS | Depends on L4 vs L7 |

### What Reverse Proxies Do

Production reverse proxies typically handle:

1. **TLS termination** — decrypt HTTPS at the edge; backends speak plain HTTP on trusted networks
2. **Request routing** — `Host: api.example.com` → API pool; `/static/*` → object storage
3. **Load distribution** — round-robin, least-conn, or consistent hash across upstream servers
4. **Connection pooling** — reuse TCP connections to backends, reducing handshake overhead
5. **Caching** — store responses for cacheable GET requests
6. **Compression** — gzip/brotli at the edge
7. **Rate limiting and WAF** — throttle abusive clients before traffic hits application code
8. **WebSocket and HTTP/2** — protocol upgrades managed at the proxy layer

### TLS Termination vs Pass-Through

**TLS termination** (SSL offloading): the proxy holds the certificate, decrypts traffic, forwards HTTP to backends. Simplifies certificate management (one cert at the edge) but requires trust in the internal network between proxy and app.

**TLS pass-through** (SSL bridging): the proxy forwards encrypted bytes without decrypting. Backends terminate TLS individually. Preserves end-to-end encryption; the proxy cannot inspect HTTP headers for routing unless it uses **SNI** (Server Name Indication) at connection time for L4 routing.

| Approach | Cert management | Header inspection | Internal traffic |
|----------|-----------------|-------------------|------------------|
| Termination | Centralized at proxy | Full L7 routing | Often plain HTTP |
| Pass-through | Per backend | L4 only (SNI routing) | Encrypted end-to-end |

!!! tip "Production pattern"
    Terminate TLS at the reverse proxy or cloud load balancer on a trusted VPC network. Re-encrypt to backends (TLS to upstream) only when compliance requires encryption in transit inside the VPC.

### nginx as a Reverse Proxy

**nginx** is the most widely deployed open-source reverse proxy. Its `proxy_pass` directive forwards requests to upstream servers defined in `upstream` blocks.

Core concepts:

- **`upstream`** — named backend pool with load-balancing method
- **`proxy_pass`** — forward location-matched requests to an upstream or URL
- **`proxy_set_header`** — inject headers (`Host`, `X-Real-IP`, `X-Forwarded-For`, `X-Forwarded-Proto`)
- **`proxy_read_timeout`** — how long to wait for backend response (504 if exceeded)

Example routing by path:

```nginx
upstream app_backend {
    least_conn;
    server 10.0.11.10:8080;
    server 10.0.11.11:8080;
}

server {
    listen 443 ssl;
    server_name www.example.com;

    ssl_certificate     /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /health {
        access_log off;
        return 200 'ok';
    }
}
```

### HAProxy Overview

**HAProxy** excels at high-concurrency TCP and HTTP proxying with ACL-based routing, stick tables, and a real-time stats page (`/haproxy?stats`). Use HAProxy when you need TCP-mode proxying alongside HTTP or granular health-check control beyond nginx defaults.

### Kubernetes Ingress

In Kubernetes, **Ingress** is an API resource that defines HTTP routing rules. An **Ingress controller** (nginx-ingress, Traefik, AWS Load Balancer Controller, Istio gateway) watches Ingress objects and configures the underlying proxy.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8080
```

**Ingress vs Service LoadBalancer:** A Kubernetes `Service` of type `LoadBalancer` creates one cloud LB per service (expensive at scale). Ingress consolidates many services behind one entry point with host/path routing.

**Gateway API** (successor to Ingress) provides richer routing, role-based resources (`Gateway`, `HTTPRoute`), and better multi-tenancy — learn Ingress first; adopt Gateway API for new clusters.

### Headers and Client IP Preservation

When a reverse proxy forwards requests, the backend sees the proxy's IP as `$remote_addr`. Applications that log client IPs or enforce IP-based rate limits need forwarded headers:

| Header | Purpose |
|--------|---------|
| `X-Forwarded-For` | Chain of client and proxy IPs |
| `X-Real-IP` | Single client IP (first hop) |
| `X-Forwarded-Proto` | Original scheme (`http` or `https`) |
| `X-Forwarded-Host` | Original Host header |

!!! warning "Trust boundary"
    Only trust `X-Forwarded-For` from known proxies. Attackers can spoof these headers if they reach the backend directly. Configure `real_ip` modules in nginx or `set_real_ip_from` to accept headers only from the proxy subnet.

## Hands-on Lab

Complete these exercises on an Ubuntu VM. Use disposable lab instances.

### Step 1 – Start two backend servers

**Command:**

```bash
mkdir -p ~/proxy-lab && cd ~/proxy-lab
python3 -m http.server 8081 --bind 127.0.0.1 &
python3 -m http.server 8082 --bind 127.0.0.1 &
curl -s http://127.0.0.1:8081/ | head -1
curl -s http://127.0.0.1:8082/ | head -1
```

**Explanation:** Two simple HTTP servers simulate distinct backends. Binding to localhost ensures they are reachable only via the reverse proxy once configured.

**Expected output:**

```text
Serving HTTP on 127.0.0.1 port 8081 ...
Serving HTTP on 127.0.0.1 port 8082 ...
<!DOCTYPE HTML>
```

### Step 2 – Install nginx and create upstream config

**Command:**

```bash
sudo apt-get update && sudo apt-get install -y nginx
sudo tee /etc/nginx/conf.d/proxy-lab.conf <<'EOF'
upstream lab_backends {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}

server {
    listen 8888;
    server_name _;

    location / {
        proxy_pass http://lab_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF
sudo nginx -t && sudo systemctl reload nginx
```

**Explanation:** The upstream block defines a backend pool. nginx load-balances across both Python servers by default (round-robin).

**Expected output:**

```text
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Step 3 – Verify load distribution through the proxy

**Command:**

```bash
for i in $(seq 1 6); do curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8888/; done
```

**Explanation:** Repeated requests should alternate between backends (200 responses). Check nginx access log to confirm different upstream response sizes or add custom backend headers in production.

### Step 4 – Add path-based routing

**Command:**

```bash
sudo tee /etc/nginx/conf.d/proxy-lab.conf <<'EOF'
upstream lab_backends {
    server 127.0.0.1:8081;
    server 127.0.0.1:8082;
}

server {
    listen 8888;
    server_name _;

    location /api/ {
        proxy_pass http://127.0.0.1:8082/;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://lab_backends;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
sudo nginx -t && sudo systemctl reload nginx
curl -sI http://127.0.0.1:8888/api/ | head -3
```

**Explanation:** Path-based routing sends `/api/*` to a specific backend while `/` uses the pool. Note the trailing slash in `proxy_pass` — it affects URL rewriting behavior.

### Step 5 – Simulate backend failure (502 Bad Gateway)

**Command:**

```bash
kill $(pgrep -f "http.server 8081") 2>/dev/null
curl -v --connect-timeout 3 http://127.0.0.1:8888/ 2>&1 | grep -E "< HTTP|502"
```

**Explanation:** When all upstreams in a pool fail, nginx returns **502 Bad Gateway**. With one backend down, round-robin still succeeds on alternate requests.

**Cleanup:**

```bash
kill $(pgrep -f "http.server") 2>/dev/null
sudo rm /etc/nginx/conf.d/proxy-lab.conf
sudo systemctl reload nginx
```

### Step 6 – Review Kubernetes Ingress (optional)

If you have kubectl access:

```bash
kubectl get ingress -A
kubectl describe ingress app-ingress -n default 2>/dev/null || echo "No ingress found — apply sample YAML from Theory section"
```

**Explanation:** Inspect which Ingress controller is installed, assigned external IP, and backend service endpoints.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `nginx -t` | Validate configuration syntax | `sudo nginx -t` |
| `nginx -s reload` | Reload config without dropping connections | `sudo systemctl reload nginx` |
| `curl -H "Host:"` | Test virtual host routing | `curl -H "Host: api.local" http://127.0.0.1/` |
| `curl -v` | Verbose HTTP including headers | `curl -v https://example.com` |
| `kubectl get ingress` | List Ingress resources | `kubectl get ingress -A` |
| `haproxy -c` | Validate HAProxy config | `sudo haproxy -c -f /etc/haproxy/haproxy.cfg` |

## Common Mistakes

!!! warning "Wrong proxy_pass trailing slash"
    `location /api/ { proxy_pass http://backend/; }` strips `/api/` from the URL. Omitting the trailing slash on `proxy_pass` preserves the full path. Misconfiguration causes 404s that look like application bugs.

!!! warning "Not setting X-Forwarded-Proto"
    Applications generate HTTP URLs behind an HTTPS-terminating proxy, breaking redirects and cookies. Always set `X-Forwarded-Proto $scheme` and configure the app to trust it.

!!! warning "Exposing backends directly"
    If backends have public IPs alongside the reverse proxy, attackers bypass the proxy's rate limits and WAF. Backends should listen only on private interfaces or security-group-restricted ports.

!!! warning "Infinite redirect loops"
    SSL redirect at both proxy and application without checking `X-Forwarded-Proto` causes redirect loops. Configure one layer to handle HTTPS enforcement.

## Best Practices

!!! tip "Terminate TLS at the edge"
    Centralize certificate management with Let's Encrypt (cert-manager in Kubernetes) at the reverse proxy. Use short-lived certs and automated renewal.

!!! tip "Set appropriate timeouts"
    Configure `proxy_connect_timeout`, `proxy_send_timeout`, and `proxy_read_timeout` to match application SLA. Default nginx timeouts cause 504 errors on slow legitimate requests.

!!! tip "Use separate upstreams per service"
    Do not route all paths to one backend pool. Separate upstreams enable independent scaling, health checks, and circuit breaking.

!!! tip "Enable access logs with upstream timing"
    Log `$upstream_response_time` and `$upstream_addr` to identify slow or failing backends during incidents.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 502 Bad Gateway | All upstreams down or refusing connections | Check backend health with `curl` directly; verify upstream IP/port |
| 504 Gateway Timeout | Backend too slow; proxy read timeout exceeded | Increase `proxy_read_timeout`; fix slow backend queries |
| Wrong backend selected | Host/path rule order or ACL mismatch | Review location block precedence; test with `curl -H "Host: ..."` |
| Client IP shows proxy IP | Missing or untrusted X-Forwarded-For | Set proxy headers; configure `real_ip` trusted sources |
| Redirect loop | HTTP/HTTPS mismatch | Set `X-Forwarded-Proto`; disable duplicate SSL redirects |
| WebSocket fails | Missing upgrade headers | Add `proxy_http_version 1.1; proxy_set_header Upgrade $http_upgrade;` |
| 413 Request Entity Too Large | Default body size limit | Increase `client_max_body_size` for file uploads |

## Summary

- A **reverse proxy** protects backends by handling client connections, TLS, routing, and cross-cutting concerns at the edge
- **nginx** and **HAProxy** are the dominant self-managed options; cloud ALBs and **Kubernetes Ingress** provide managed equivalents
- **TLS termination** centralizes certificates; **pass-through** preserves end-to-end encryption at the cost of L7 inspection
- Route by **hostname** and **path** using location blocks (nginx) or ACLs (HAProxy)
- Always forward **`X-Forwarded-For`** and **`X-Forwarded-Proto`** so backends log correct client metadata
- **502** means no healthy upstream; **504** means upstream too slow — different root causes and fixes

## Interview Questions

1. What is the difference between a forward proxy and a reverse proxy?
2. Why terminate TLS at the reverse proxy instead of on each backend?
3. Explain how nginx `proxy_pass` URL rewriting works with trailing slashes.
4. What is Kubernetes Ingress, and how does it differ from a LoadBalancer Service?
5. What headers must a reverse proxy set for backends to know the client's real IP?
6. A user gets 502 errors intermittently. How do you diagnose whether the proxy or backend is at fault?
7. Compare nginx and HAProxy for a high-traffic API gateway.
8. What is TLS pass-through, and when would you use it?
9. How does path-based routing work in an Ingress resource?

??? tip "Sample Answers (Questions 1, 4, and 6)"

    **Q1 — Forward vs reverse:** A forward proxy sits on the client side — clients configure it to reach the internet, and servers see the proxy's IP. A reverse proxy sits on the server side — clients connect to the proxy's public address, and the proxy forwards to internal backends that may not be directly reachable. Forward proxies protect clients; reverse proxies protect and scale servers.

    **Q4 — Ingress vs LoadBalancer Service:** A LoadBalancer Service provisions one cloud load balancer per service — costly and IP-heavy at scale. Ingress defines HTTP routing rules (host, path) consumed by an Ingress controller that configures a shared reverse proxy fronting many services through one entry point. Ingress is L7 HTTP routing; LoadBalancer is typically L4 with one external IP per service.

    **Q6 — Intermittent 502:** 502 means the proxy received an invalid response or could not connect to upstream. Check nginx error log for `connect() failed` vs `upstream prematurely closed`. Test backends directly bypassing the proxy. Verify upstream health — intermittent 502 often indicates one backend in a pool is failing while others succeed. Check `max_fails` and passive health marking. Review recent deployments and resource exhaustion on backends.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Load Balancing Fundamentals](load-balancing-fundamentals.md) *(previous in Module 4)*
- [Network Troubleshooting Methodology](network-troubleshooting-methodology.md) *(next in Module 4 → Module 5)*
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)

## References

- [HAProxy Configuration Manual](https://www.haproxy.org/download/2.9/doc/configuration.txt)
- [Kubernetes Ingress documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [OWASP — Reverse Proxy Security](https://owasp.org/www-community/controls/Reverse_Proxy)
