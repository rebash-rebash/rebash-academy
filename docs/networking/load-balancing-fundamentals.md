---
title: "Load Balancing Fundamentals"
description: "Master Layer 4 vs Layer 7 load balancing, scheduling algorithms, health checks, session persistence, and cloud ALB/NLB concepts for DevOps."
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
  - load-balancing
  - health-checks
  - alb
  - nlb
prerequisites:
  - networking/linux-networking-toolkit
next:
  - networking/reverse-proxy-and-ingress-basics
related:
  - networking/http-https-and-application-layer
  - networking/kubernetes-networking-fundamentals
  - networking/load-balancer-operations-and-health-checks
labs: []
projects: []
interview: interview/networking
certifications:
  - CompTIA Network+
  - AWS SAA
tags:
  - networking
  - load-balancer
  - alb
  - nlb
  - health-checks
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Load Balancing Fundamentals

## Overview

Choose L4 vs L7 correctly, explain common scheduling and health-check designs, and map the same ideas to cloud load balancers (ALB/NLB and equivalents).

A **load balancer** presents a stable front door and spreads traffic across healthy backends. It enables scale-out, rolling deploys, and failover. Wrong tier choices cause silent bugs: L4 cannot route by path; L7 adds TLS and parsing complexity.

This is the first tutorial in **Module 13 — Load Balancing**. Complete [Linux Networking Toolkit](linux-networking-toolkit.md) (and HTTP/firewall modules) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 13 · Load Balancing** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Networking Toolkit](linux-networking-toolkit.md)
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)

### Recommended

- Cloud console familiarity for ALB/NLB (or GCP/Azure LB) exploration

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast Layer 4 and Layer 7 load balancing  
- [ ] Compare round-robin, least connections, and IP-hash (session persistence)  
- [ ] Design health checks that match real readiness  
- [ ] Explain active/passive or multi-AZ LB high availability  
- [ ] Choose AWS ALB vs NLB (and equivalents) for common cases  
- [ ] Diagnose uneven distribution and flapping health

## Architecture

Clients hit a VIP; the balancer forwards only to healthy pool members.

![Load balancing](../assets/excalidraw/load-balancing.svg)

## Theory

### Why load balance?

Direct-to-one-server creates a single point of failure, a scale ceiling, and painful deploys. The balancer owns the **VIP** or DNS name; backends form a **target group** / **pool**.

### Layer 4 vs Layer 7

| | Layer 4 | Layer 7 |
|--|---------|---------|
| Sees | IP + port (TCP/UDP) | HTTP/gRPC headers, path, Host |
| Speed | Lower overhead | More processing / TLS terminate |
| Protocols | Any TCP/UDP | HTTP-family (typical) |
| Routing | Port / IP | Path, Host, headers, cookies |

**NLB-style** ≈ L4. **ALB / Application Gateway / HTTP(S) LB** ≈ L7.

### Scheduling

| Algorithm | Behaviour |
|-----------|-----------|
| Round-robin | Rotate members |
| Least connections | Prefer quieter backends |
| IP hash / cookie stickiness | Session persistence |

Sticky sessions help stateful apps but hurt even distribution and draining — prefer shared session stores when you can.

### Health checks

- **TCP** — port open  
- **HTTP** — status path (`/healthz`) returns 200  
- Interval, timeout, healthy/unhealthy thresholds  

Bad checks: probing a path that needs auth, or marking ready before DB connections work. Align with Kubernetes readiness when behind Ingress.

### High availability

Run balancers (or use managed multi-AZ services) so the VIP survives AZ loss. Drain backends before deploy; never rely on a single backend in production.

### Cloud mapping

| Need | Typical choice |
|------|----------------|
| HTTP path / Host routing, TLS terminate | ALB / Application Gateway / HTTP(S) LB |
| Extreme L4, static IP, non-HTTP | NLB / Network LB / TCP LB |
| Preserve client IP | PROXY protocol, X-Forwarded-For, or L4 pass-through patterns |

## Hands-on Lab

**Focus:** practise the core workflow for Load Balancing Fundamentals

```bash
mkdir -p ~/rebash-networking/module-13
cd ~/rebash-networking/module-13

sudo apt-get update
sudo apt-get install -y curl
```

Optional cloud CLIs if you will inspect managed LBs later.

### Step 1 – Observe a public LB from the client

```bash
curl -sI https://example.com/ | head -20
dig +short example.com A
```

Note: DNS may point at anycast or cloud LB edges — you rarely see “the” backend IP.

### Step 2 – Design a pool on paper

```text
VIP: app.example.com → L7 LB
Backends: 10.0.2.10:8080, 10.0.2.11:8080, 10.0.2.12:8080
Health: GET /healthz every 10s, 2 failures → unhealthy
Algorithm: least connections
Stickiness: none (JWT in Authorization header)
```

Save as `~/rebash-networking/module-13/pool-design.md`.

### Step 3 – Health-check failure modes

List three ways a check can lie (always 200 static file; fails only under load; blocks probe SG). Note remediations.

### Step 4 – L4 vs L7 decision drill

For each, pick L4 or L7:

1. Path `/api` vs `/static` to different services  
2. PostgreSQL to three replicas  
3. Mutual TLS passthrough to backends  

### Step 5 – Status code mapping

Recall from HTTP module: **502/503/504** often originate at the balancer when upstreams misbehave — document which symptom maps to “no healthy targets” vs “upstream timeout.”

## Validation

- [ ] Lab commands run under `~/rebash-networking/module-13/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Load Balancing Fundamentals** always combines:

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

!!! warning "Skipping fundamentals for Load Balancing Fundamentals"
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Treating lab defaults as production-ready for Load Balancing Fundamentals"
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Load Balancing Fundamentals changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| 503 | No healthy targets | Fix health path/SG; check deploy |
| Uneven load | Stickiness / long connections | Review algorithm; drain; metrics |
| Flapping | Tight thresholds / slow app | Tune interval; fix cold start |
| Client IP lost | SNAT at LB | PROXY protocol or headers |
| TLS errors | Cert/SNI on L7 | Check listener cert and Host |

## Summary

- L4 forwards transport flows; L7 understands HTTP  
- Algorithms and stickiness trade fairness vs affinity  
- Health checks must reflect real readiness  
- Prefer multi-AZ managed balancers in cloud

## Interview Questions

1. How does **Load Balancing Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md)  
- [Load Balancer Operations and Health Checks](load-balancer-operations-and-health-checks.md)

## References

- [AWS ELB docs](https://docs.aws.amazon.com/elasticloadbalancing/)  
- [GCP Cloud Load Balancing](https://cloud.google.com/load-balancing/docs)  
- [Azure Load Balancer](https://learn.microsoft.com/azure/load-balancer/)
