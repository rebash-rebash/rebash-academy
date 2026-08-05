---
title: System Design
description: "Learn System Design the engineering way — requirements, trade-offs, architecture diagrams, and Python labs you can run locally."
difficulty: intermediate
estimated_time: "12–14 weeks"
technology: system-design
technology_id: system-design
category: architecture
status: ready
author: Shaik Basha
last_updated: "2026-08-05"
tags:
  - system-design
  - architecture
  - software-engineering
comments: false
---

# System Design

Design systems the way production engineers do: start with goals and constraints, make trade-offs explicit, draw clear diagrams, then prove the critical path with code.

This course is for **working software engineers** and people who want to **become** software engineers. You do not need to be a cloud architect first. You need curiosity about how requests, data, and failures move through a system.

## Who this is for

| You are… | You will practise… |
|----------|--------------------|
| Aspiring software engineer | Turning vague features into APIs and data models |
| Backend / full-stack engineer | Scaling paths, consistency, and failure modes |
| DevOps / platform engineer | Seeing services as products with SLOs and blast radius |
| Interview candidate | Structured design conversations with evidence |

## What you will learn

- Clarify functional and non-functional requirements before drawing boxes
- Estimate capacity with simple, defensible maths
- Choose architecture styles for the problem — not fashion
- Trace a request from client through DNS, CDN, load balancer, and service
- Explain trade-offs (latency vs consistency vs cost) in plain language
- Implement thin but real paths in **Python** so designs stay honest

## Course structure

| Part | Focus | Status |
|------|--------|--------|
| **A · Foundations** | Design process, quality attributes, styles, request path | Modules 1–4 ready |
| **B · Building blocks** | Storage, cache, messaging, APIs, resilience | Modules 5–9 ready |
| **C · Classic systems** | Shortener, feed, uploads, search | Modules 10–13 ready |
| **D · Realtime** | Chat, notifications, collaboration, capstone | Modules 14–17 ready |

## Start here

1. [How to design a system](how-to-design-a-system.md) — the thinking process  
2. [Quality attributes and trade-offs](quality-attributes-and-trade-offs.md) — what “good” means  
3. [Application architecture styles](application-architecture-styles.md) — monolith to events  
4. [Client, edge, and service path](client-edge-and-service-path.md) — where a request travels  
5. [Data storage](data-storage.md) — access patterns and engines  
6. [Caching](caching.md) — layers, TTL, stampede control  
7. [Messaging and async](messaging-and-async.md) — queues and idempotency  
8. [APIs and communication](apis-and-communication.md) — contracts and timeouts  
9. [Observability and resilience](observability-and-resilience.md) — SLOs and failure modes  
10. [URL shortener](url-shortener.md) — redirect-optimised design  
11. [News feed / timeline](news-feed.md) — fan-out trade-offs  
12. [File / media upload](media-upload.md) — direct upload pipelines  
13. [Search / autocomplete](search-and-autocomplete.md) — indexes and suggest  
14. [Realtime chat](realtime-chat.md) — WebSockets and durable fan-out  
15. [Notifications and presence](notifications-and-presence.md) — heartbeats and routing  
16. [Collaborative and streaming patterns](collaborative-streaming.md) — OT/CRDT intuition  
17. [Capstone — collaboration board](capstone-collaboration-board.md) — integrate the course  

See the [roadmap](roadmap.md) for the full journey.

## How each tutorial works

Every lesson follows the same arc:

**Requirements → Trade-offs → Architecture (diagrams) → Python lab → Interview check**

Diagrams are first-class. Labs use Python so you can run and break things on your machine.

## Prerequisites

- Comfortable with HTTP (methods, status codes, JSON)
- Can write small Python scripts
- Basic SQL ideas (tables, primary keys)
- Git installed

All course labs run with Python alone. Docker/Redis are optional upgrades for portfolio demos.
