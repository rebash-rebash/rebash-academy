---
title: "Concurrency — Threads, asyncio, and Futures"
description: "Choose threads, multiprocessing, asyncio, and concurrent.futures for DevOps I/O fan-out — with queues and practical safety notes."
difficulty: advanced
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 21 · Concurrency"
career_paths:
  - devops-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - asyncio
  - threading
  - concurrency
prerequisites:
  - python/ssh-automation-paramiko-and-fabric
next:
  - python/testing-with-pytest
related:
  - python/rest-apis-requests-auth-and-resilience
  - python/production-engineering-patterns
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - asyncio
  - threads
  - concurrency
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Concurrency — Threads, asyncio, and Futures

## Overview

Pick the right concurrency model for ops fan-out (HTTP checks, host probes), use `concurrent.futures` pools safely, and know when asyncio helps — without over-complicating simple scripts.

Most DevOps concurrency is **I/O-bound**: waiting on APIs and SSH. Threads or asyncio beat processes for that. CPU-heavy parsing may need multiprocessing. Cap workers; respect rate limits.

Diagrams use Excalidraw only.

This is a core tutorial in **Module 21 · Concurrency** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [REST APIs](rest-apis-requests-auth-and-resilience.md)
- Functions and error handling modules

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast threads vs processes vs asyncio  
- [ ] Use `ThreadPoolExecutor` / `ProcessPoolExecutor`  
- [ ] Sketch an asyncio gather for many HTTP GETs  
- [ ] Use a queue for producer/consumer jobs  
- [ ] Avoid unbounded fan-out against APIs

## Architecture

This topic’s control points and relationships are shown below.

![Concurrency models](../assets/excalidraw/python-concurrency.svg)

## Theory

### What it is

Concurrency means overlapping work so waiting time (network, disk, SSH) does not idle the whole script. Python offers three common models for DevOps tooling: **threads** (`ThreadPoolExecutor`), **processes** (`ProcessPoolExecutor` / `multiprocessing`), and **asyncio** (cooperative tasks on one thread). Parallelism for CPU-heavy work is different: the Global Interpreter Lock (GIL) limits CPU speed-up in threads, so processes are the usual escape hatch.

### Why it matters

Inventory jobs hit hundreds of HTTP APIs or hosts. Sequential loops finish overnight; bounded fan-out finishes in minutes. Wrong model wastes effort: threads do not speed up pure JSON crunching, and naïve asyncio mixed with blocking `requests` can freeze the event loop. Choosing deliberately keeps automation fast, predictable, and easier to cancel cleanly under timeouts.

### How it works

**Threads** share memory; the OS schedules them. While one thread waits on a socket, others run. Use `concurrent.futures.ThreadPoolExecutor` with a small `max_workers` and futures for results/exceptions. **Multiprocessing** starts separate interpreters — true multi-core CPU work — but arguments must pickle and memory cost is higher. **asyncio** runs many coroutines on one thread; each must `await` I/O (for example `httpx` AsyncClient). Blocking calls inside asyncio should go through `asyncio.to_thread` or an executor. Bounded **queues** (`queue.Queue` or `asyncio.Queue`) keep producers from flooding memory.

### Key concepts and comparisons

| Workload | Prefer | Why |
|----------|--------|-----|
| Many HTTP/SSH waits | Threads or asyncio | Time is spent blocked on I/O |
| CPU-bound parsing / hashing | multiprocessing | Bypass GIL |
| Simple scripts / few hosts | Sequential first | Easier to debug |
| Structured async pipelines | asyncio + Queue | Back-pressure and cancel scope |

| Concept | Meaning |
|---------|---------|
| Fan-out | Start N similar tasks, gather results |
| Back-pressure | Bound workers/queue size so you do not OOM |
| Cancellation | Timeouts and shutdown of executors / tasks |

### Common pitfalls

- Spawning unbounded threads (one per host with no pool).  
- Using threads for CPU-heavy loops and expecting linear speed-up.  
- Calling blocking `requests` or `subprocess` inside `async def` without offloading.  
- Ignoring exceptions on futures — always retrieve results or use `as_completed`.  
- Sharing mutable state across threads without locks (prefer return values).

## Hands-on Lab

**Focus:** practise the core workflow for Concurrency — Threads, asyncio, and Futures

```bash
mkdir -p ~/rebash-python/module-21
cd ~/rebash-python/module-21

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'requests==2.32.3'
```

### Step 1 – Thread pool HTTP checks

```bash
cd ~/rebash-python/module-21
source .venv/bin/activate

cat > fanout.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

URLS = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/delay/1",
]


def check(url: str) -> tuple[str, int]:
    r = requests.get(url, timeout=10)
    return url, r.status_code


def main() -> int:
    worst = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(check, u): u for u in URLS}
        for fut in as_completed(futures):
            url, code = fut.result()
            print(f"{code} {url}")
            if code >= 400:
                worst = 1
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python fanout.py; echo exit=$?
```

### Step 2 – Bounded workers note

Change `max_workers` to 1 vs 4 and observe wall time for the delay URL.

### Step 3 – asyncio sketch

```bash
python - <<'PY'
import asyncio

async def poke(n: int) -> int:
    await asyncio.sleep(0.05)
    return n

async def main() -> None:
    results = await asyncio.gather(*(poke(i) for i in range(5)))
    print(results)

asyncio.run(main())
PY
```

### Step 4 – Queue sketch

```bash
python - <<'PY'
from queue import Queue
from threading import Thread

q: Queue[str | None] = Queue()

def worker() -> None:
    while True:
        item = q.get()
        if item is None:
            break
        print("work", item)
        q.task_done()

t = Thread(target=worker)
t.start()
for name in ("web-a", "web-b"):
    q.put(name)
q.put(None)
t.join()
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-21/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Concurrency — Threads, asyncio, and Futures** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Spawning unbounded threads (one per host with no pool).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Using threads for CPU-heavy loops and expecting linear speed-up.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Concurrency — Threads, asyncio, and Futures changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Rate limits | Too many workers | Lower pool size; backoff |
| Deadlocks | Joining wrong order / shared locks | Keep critical sections tiny |
| Blocking asyncio | Called `requests` in coro | Use async client or `to_thread` |

## Summary

- I/O fan-out → threads/asyncio; CPU → processes  
- Bound workers; handle per-future errors  
- Sequential is OK until metrics demand concurrency

## Interview Questions

1. How does **Concurrency — Threads, asyncio, and Futures** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Testing with pytest](testing-with-pytest.md)

## References

- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)  
- [asyncio](https://docs.python.org/3/library/asyncio.html)
