---
title: System Design glossary
description: "Key System Design terms used in this course."
technology_id: system-design
author: Shaik Basha
last_updated: "2026-08-05"
---

# System Design glossary

| Term | Meaning |
|------|---------|
| Functional requirement | What the system must *do* (features, APIs, behaviours) |
| Non-functional requirement | How well it must do it (latency, availability, cost) |
| Constraint | Hard limit you cannot ignore (budget, tech, compliance, deadline) |
| Assumption | Believed fact you must state and revisit |
| Trade-off | Choosing more of one quality usually means less of another |
| Latency | Time for one request to complete |
| Throughput | Work completed per unit time |
| Availability | Fraction of time the system is usable |
| Consistency | Whether all readers see the same data at the same moment |
| CAP / PACELC | Frameworks for reasoning about consistency and availability under partition / normal operation |
| Blast radius | How much fails when one component fails |
| CDN | Content Delivery Network — edge caches close to users |
| Load balancer | Distributes traffic across healthy backends |
| API gateway | Edge for APIs — auth, routing, rate limits, aggregation |
| OLTP | Online Transaction Processing — transactional primary datastore |
| Replica lag | Delay between primary write and replica visibility |
| Hot partition | Shard receiving disproportionate traffic |
| Cache-aside | App reads cache; on miss loads DB and fills cache |
| TTL | Time to live — automatic cache expiry |
| Cache stampede | Many concurrent misses on one hot key overwhelm the origin |
| Object storage | Blob store for large files; metadata usually stays in OLTP/KV |
| Queue | Messaging where each message is processed by one consumer |
| Pub/sub | Fan-out messaging to many subscribers |
| Idempotency | Safe to process the same request/message more than once |
| DLQ | Dead-letter queue for repeatedly failing messages |
| Outbox | Transactional table of events to publish safely after commits |
| Circuit breaker | Stop calling a failing dependency; fail fast during cool-down |
| Bulkhead | Isolate resources so one failure cannot exhaust the whole service |
| Load shedding | Reject or degrade work to protect critical paths when saturated |
| Golden signals | Latency, traffic, errors, saturation |
| Fan-out on write | Push new content into followers’ timelines at publish time |
| Fan-out on read | Merge followees’ content when reading the home timeline |
| Presigned URL | Time-limited credential for direct client upload/download to object storage |
| Inverted index | Term → document postings used for full-text search |
| Autocomplete | Prefix-based query/entity suggestions as the user types |
| WebSocket | Persistent bi-directional channel used for chat and live boards |
| Presence | Online/away state derived from heartbeats and TTLs |
| OT | Operational Transformation — transform concurrent ops to converge |
| CRDT | Conflict-free Replicated Data Type — mergeable structure that converges |
| Op log | Append-only log of collaborative operations for replay and sync |
| Snapshot | Compact materialised state so clients need not replay full history |
