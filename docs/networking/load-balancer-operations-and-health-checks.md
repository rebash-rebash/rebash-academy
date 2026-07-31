---
title: "Load Balancer Operations and Health Checks"
description: "Operate production load balancers: health checks, draining, capacity, TLS listeners, and incident response for 502/503/504 and flapping targets."
difficulty: intermediate
estimated_time: "40–55 min"
technology: networking
category: networking
module: "Module 16 · Production Networking"
career_paths:
  - devops-engineer
  - cloud-engineer
  - site-reliability-engineer
  - platform-engineer
skills:
  - load-balancer-ops
  - health-checks
  - draining
prerequisites:
  - networking/production-dns-operations
next:
  - networking/firewall-change-control-and-production-acls
related:
  - networking/load-balancing-fundamentals
  - networking/reverse-proxy-and-ingress-basics
labs: []
projects: []
interview: interview/networking
certifications:
  - AWS SAA
tags:
  - networking
  - load-balancer
  - health-checks
  - operations
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Load Balancer Operations and Health Checks

## Overview

Operate LBs safely: tune health checks, drain for deploys, watch capacity and TLS, and triage 502/503/504 without guessing.

Day-2 LB work is mostly health, capacity, and change safety. Builds on [Load Balancing Fundamentals](load-balancing-fundamentals.md).

This is a core tutorial in **Module 16 · Production Networking** of the REBASH Academy **Networking for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Load Balancing Fundamentals](load-balancing-fundamentals.md)
- [Production DNS Operations](production-dns-operations.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Tune health check path, interval, thresholds  
- [ ] Drain / deregister before terminate  
- [ ] Interpret LB metrics (healthy host count, 5xx, latency)  
- [ ] Coordinate DNS + LB cutovers  
- [ ] Respond to flapping and cold-start failures

## Architecture

This topic’s control points and relationships are shown below.

![Load balancing](../assets/excalidraw/load-balancing.svg)

## Theory

### What it is

Load balancer operations is day-2 work on pools that already exist: **health checks that reflect truth**, **connection draining** during deploys, capacity and timeout tuning, and diagnosing flapping or uneven distribution. Fundamentals cover Layer 4 vs Layer 7; this module is how you keep the VIP healthy in production.

### Why it matters

Most “outages” users see are balancers sending traffic to dead or overloaded targets — or marking healthy targets down because the probe is wrong. Bad drains cause 502/504 spikes every release. Idle timeout mismatches produce mysterious gateway timeouts while the app is fine. Operators who understand health and drain math ship safer.

### How it works

Health checks must exercise the **same dependency path** users need, or a dedicated readiness that verifies critical backends (for example the database). A static file that always returns 200 while the app is wedged is worse than no check. Tune interval, timeout, and healthy/unhealthy thresholds so brief blips do not empty the pool. For **draining**, stop new connections, allow in-flight work to finish, then terminate. In Kubernetes, align readiness gates and `preStop` sleep with the cloud load balancer’s deregistration delay. Watch concurrent connections, targets per Availability Zone (AZ), Transport Layer Security (TLS) CPU on Layer 7, and idle timeout versus application timeouts.

### Key concepts and comparisons

| Concern | Operational focus |
|---------|-------------------|
| Truthful health | Probe real readiness, not a static page |
| Drain / deregister | No new flows; finish in-flight; then stop |
| Capacity | Conns per target, AZ balance, TLS cost |
| Timeouts | LB idle vs app vs client — avoid 504 loops |
| Flapping | Thresholds too aggressive; fix app or loosen |

| Signal | Often means |
|--------|-------------|
| Rising 5xx at LB | Unhealthy/missing targets or app errors |
| 504 gateway timeout | Idle/upstream timeout mismatch |
| One AZ hot | Uneven registration or sticky sessions |

### Common pitfalls

- Health path requires auth the probe lacks → perpetual unhealthy.  
- Draining shorter than in-flight request time.  
- Sticky sessions hiding broken instances until users stick to them.  
- Registering targets before they listen.  
- Ignoring AZ imbalance until a single AZ failure takes half the capacity “surprisingly.”

## Hands-on Lab

**Focus:** practise the core workflow for Load Balancer Operations and Health Checks

### Step 1 – Runbook: 503

```text
1) Healthy host count = 0?
2) Health path / SG / port wrong?
3) Deploy bad?
4) Rollback or fix readiness
```

### Step 2 – Runbook: 504

```text
1) Upstream latency / DB locks
2) Idle timeout too low
3) Slow dependencies
```

### Step 3 – Deploy checklist

Write: attach → warm → health green → shift traffic → drain old → terminate.

## Validation

- [ ] Lab commands run under `~/rebash-networking//`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Load Balancer Operations and Health Checks** always combines:

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

!!! warning "Health path requires auth the probe lacks → perpetual unhealthy.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Draining shorter than in-flight request time.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Load Balancer Operations and Health Checks changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Flapping | Tight thresholds | Raise failure count; fix GC/cold start |
| Uneven AZ | Imbalanced targets | Cross-zone; equal capacity |
| Cert errors | Listener/SNI | Fix ACM/cert binding |

## Summary

- Health checks = readiness truth  
- Drain before destroy  
- 5xx at LB have layered causes — count healthy hosts first

## Interview Questions

1. How does **Load Balancer Operations and Health Checks** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Firewall Change Control and Production ACLs](firewall-change-control-and-production-acls.md)

## References

- [AWS target group health](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
