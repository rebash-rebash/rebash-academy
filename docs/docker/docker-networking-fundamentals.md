---
title: "Docker Networking Fundamentals"
description: "Configure bridge, host, and overlay networks, publish ports, use container DNS, and troubleshoot Docker networking for DevOps."
difficulty: intermediate
estimated_time: "45–60 min"
technology: docker
category: docker
module: "Module 8 · Networking"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
  - cloud-engineer
skills:
  - docker
  - networking
prerequisites:
  - docker/volumes-and-persistent-storage
  - networking/index
next:
  - docker/docker-compose-fundamentals
related:
  - docker/troubleshooting-docker-containers
labs: []
projects: []
interview: interview/docker
certifications:
  - Docker Certified Associate
tags:
  - docker
  - networking
  - bridge
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Docker Networking Fundamentals

## Overview

Create a user-defined bridge network, connect containers by name, publish ports, and know when host/overlay/macvlan apply.

Default **bridge** isolates containers; user-defined bridges add DNS. **Host** shares the host stack. **Overlay** spans Swarm/multi-host. Port mapping publishes container ports to the host.

This is a core tutorial in **Module 8 · Networking** of the REBASH Academy **Docker for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- [Volumes and Persistent Storage](volumes-and-persistent-storage.md)
- Networking basics from the [Networking](../networking/index.md) track help

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Create and inspect a bridge network  
- [ ] Reach containers via DNS names  
- [ ] Publish ports with `-p`  
- [ ] Contrast bridge vs host  
- [ ] Outline overlay / macvlan use cases

## Architecture

This topic’s control points and relationships are shown below.

![Docker networking](../assets/excalidraw/docker-networking.svg)

## Theory

### What

Docker networks connect containers to each other and to the outside world. The default **bridge** network suits single-host apps; **host** shares the host network namespace; **none** isolates; **overlay** serves multi-host Swarm; **macvlan** makes containers appear as LAN hosts. Published ports map container ports to the host.

### Why

Most “container cannot connect” tickets are network misunderstandings: wrong network, unpublished ports, or DNS name mismatches. Compose and Swarm rely on user-defined networks so service names resolve via embedded DNS.

### How it works

User-defined bridge networks give containers IP addresses and DNS entries based on container or Compose service names. `docker run --network` attaches at start; you can also connect later. Publishing `-p 8080:80` forwards host port 8080 to container port 80. Troubleshoot with `docker network inspect`, `docker exec` plus `wget`/`nc`, and host tools such as `ss` or `lsof` for published ports. Firewall rules on the host can still block traffic after Docker’s iptables/nftables integration.

| Driver | Typical use |
|--------|-------------|
| bridge | Single-host apps (default for Compose) |
| host | Max performance / special networking |
| none | Locked down (no NIC) |
| overlay | Multi-host Swarm |
| macvlan | Appear as LAN hosts |

### Key concepts

- **Embedded DNS** — service discovery on user-defined networks  
- **Publish vs expose** — publish creates host forwarding  
- **Hairpin / localhost** — Desktop vs Linux differences  
- **Network policies** — Docker alone is not Kubernetes NetworkPolicy  

### Common pitfalls

- Using the legacy default bridge without DNS service names  
- Binding only to `127.0.0.1` then wondering why other hosts cannot connect  
- Assuming containers share localhost with the host (they do not, except `host` mode)  
- Overlapping subnet CIDRs with corporate VPNs

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-docker/module-08 && cd ~/rebash-docker/module-08
```

**Focus:** hands-on practice for Docker Networking Fundamentals

### Step 1 – Core exercise

```bash
mkdir -p ~/rebash-docker/module-08 && cd ~/rebash-docker/module-08
docker network create rebash-net
docker run -d --name rebash-web --network rebash-net nginx:alpine
docker run --rm --network rebash-net alpine wget -qO- http://rebash-web/ | head -n 3
docker run -d --name rebash-pub -p 8081:80 --network rebash-net nginx:alpine
curl -sI http://127.0.0.1:8081 | head -n 3
docker network inspect rebash-net --format '{{ "{{" }}json .Containers{{ "}}" }}' | head -c 200
docker rm -f rebash-web rebash-pub
docker network rm rebash-net
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-docker/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-docker/module-08/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Docker Networking Fundamentals** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for docker as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Using the legacy default bridge without DNS service names  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Binding only to `127.0.0.1` then wondering why other hosts cannot connect  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Docker Networking Fundamentals changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary

**Docker Networking Fundamentals** is essential for Cloud and DevOps engineers working with docker. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Docker Networking Fundamentals** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Docker Compose Fundamentals](docker-compose-fundamentals.md)

## References

- [Docker networking overview](https://docs.docker.com/engine/network/)
