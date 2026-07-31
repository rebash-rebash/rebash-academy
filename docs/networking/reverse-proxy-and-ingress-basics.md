---
title: "Reverse Proxy and Ingress Basics"
description: "Configure reverse proxies with nginx and HAProxy concepts, terminate TLS at the edge, route by Host and path, and map the same ideas to Kubernetes Ingress."
difficulty: intermediate
estimated_time: "45–60 min"
technology: networking
category: networking
module: "Module 13 · Load Balancing"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - kubernetes-engineer
  - platform-engineer
skills:
  - reverse-proxy
  - nginx
  - haproxy
  - ingress
  - tls
prerequisites:
  - networking/load-balancing-fundamentals
next:
  - networking/kubernetes-networking-fundamentals
related:
  - networking/http-https-and-application-layer
  - networking/kubernetes-networking-fundamentals
  - networking/load-balancer-operations-and-health-checks
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - CKA
tags:
  - networking
  - reverse-proxy
  - nginx
  - haproxy
  - ingress
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Reverse Proxy and Ingress Basics

## Overview

Explain reverse proxy vs load balancer roles, sketch nginx/HAProxy-style routing and TLS termination, and map the pattern to Kubernetes Ingress.

A **reverse proxy** accepts client traffic and forwards it to internal backends — often with TLS termination, Host/path routing, header injection, and rate limits. Many products are both proxy and balancer (ALB, nginx upstreams, Ingress controllers).

This is the second tutorial in **Module 13**. Complete [Load Balancing Fundamentals](load-balancing-fundamentals.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 13 · Load Balancing** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Load Balancing Fundamentals](load-balancing-fundamentals.md)
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- Linux lab host with `sudo`

### Recommended

- Optional: local Kubernetes (kind/minikube) for Ingress observation

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast forward proxy, reverse proxy, and load balancer  
- [ ] Describe TLS terminate vs passthrough  
- [ ] Route by hostname and URL path  
- [ ] Sketch an nginx `upstream` + `proxy_pass` pattern  
- [ ] Explain Kubernetes Ingress at a practical level  
- [ ] Debug 502/504 and wrong-backend routing

## Architecture

Clients reach the proxy; internals stay private. Path/Host selects upstream.

![Reverse proxy and Ingress](../assets/excalidraw/reverse-proxy-ingress.svg)

## Theory

### Roles

| Role | Protects / serves | Typical use |
|------|-------------------|-------------|
| Forward proxy | Clients | Egress control, caching |
| Reverse proxy | Servers | Edge TLS, routing, hide topology |
| Load balancer | Pool fairness/HA | Spread across identical backends |

One process often does reverse proxy **and** L7 balancing.

### TLS at the edge

- **Terminate** at proxy — backends may speak HTTP on a private network; certs managed once  
- **Passthrough** — proxy forwards TLS bytes; backends present certs (mTLS, special apps)  
- **Re-encrypt** — terminate then TLS again to backends  

Always set or trust **`X-Forwarded-For`**, **`X-Forwarded-Proto`**, and **`Host`** behaviour so apps see the real client and scheme.

### nginx pattern (conceptual)

```nginx
upstream api {
    server 10.0.2.10:8080;
    server 10.0.2.11:8080;
}

server {
    listen 443 ssl;
    server_name api.example.com;
    # ssl_certificate ...;

    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

HAProxy uses `frontend` / `backend` with ACLs on Host and path — same ideas, different syntax.

### Kubernetes Ingress

Ingress (and Gateway API) declare HTTP routing; a **controller** (nginx, Traefik, cloud LB controller) implements it. Flow: Client → Service type LoadBalancer / NodePort → Ingress controller → Service → Pods.

## Hands-on Lab

**Focus:** practise the core workflow for Reverse Proxy and Ingress Basics

```bash
mkdir -p ~/rebash-networking/module-13
cd ~/rebash-networking/module-13

sudo apt-get update
sudo apt-get install -y nginx curl openssl
```

### Step 1 – Inspect default nginx

```bash
nginx -v
sudo nginx -t
curl -sI http://127.0.0.1/ | head -15
```

### Step 2 – Local reverse-proxy sketch

Create a notes file with:

1. `server_name` for two hosts (`app.local`, `api.local`)  
2. `location /static` vs `location /` upstreams  
3. Which headers you would forward  

### Step 3 – Simulate upstream failure semantics

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9 || true
```

Relate to **502** (bad gateway) when the proxy cannot get a valid upstream response.

### Step 4 – Certificate glance

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

Edge certs are what clients validate when TLS terminates at the proxy.

### Step 5 – Ingress mental model

If you have a cluster:

```bash
kubectl get ingress -A 2>/dev/null || echo "No cluster — skip; keep the paper model"
```

Otherwise document: Host rule → Service name → Pod port.

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Reverse Proxy and Ingress Basics** always combines:

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

!!! warning "Skipping fundamentals for Reverse Proxy and Ingress Basics"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Reverse Proxy and Ingress Basics"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Reverse Proxy and Ingress Basics changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| 502 | Upstream down / wrong port | Check listen address; upstream DNS |
| 504 | Upstream slow | Timeouts; app/DB latency |
| Wrong site | Host/server_name mismatch | Fix vhost / Ingress host |
| Redirect loop | HTTP↔HTTPS rules fight | Align proxy and app redirects |
| Lost client IP | Missing forward headers | Set X-Forwarded-*; trust hop count |

## Summary

- Reverse proxies front backends with HTTP-aware behaviour  
- TLS usually terminates at the edge; headers preserve client context  
- Ingress is declarative reverse-proxy routing for Kubernetes  
- Gateway status codes often mean “proxy could not complete upstream”

## Interview Questions

1. How does **Reverse Proxy and Ingress Basics** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Kubernetes Networking Fundamentals](kubernetes-networking-fundamentals.md)  
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)

## References

- [nginx reverse proxy](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)  
- [HAProxy documentation](https://www.haproxy.org/download/2.8/doc/configuration.txt)  
- [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
