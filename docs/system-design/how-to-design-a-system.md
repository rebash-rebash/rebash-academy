---
title: "How to design a system"
description: "Learn a repeatable System Design process — business goals, requirements, capacity estimation, assumptions, trade-offs, and architecture — with a Python lab."
difficulty: beginner
estimated_time: "60–75 min"
technology: system-design
category: architecture
module: "Module 1 · Design foundations"
learning_paths:
  - beginner
  - devops-engineer
  - platform-engineer
skills:
  - system-design
  - requirements
  - capacity-estimation
prerequisites: []
next:
  - system-design/quality-attributes-and-trade-offs
related:
  - networking/index
  - python/index
tags:
  - system-design
  - architecture
  - requirements
author: Shaik Basha
last_updated: "2026-08-05"
comments: false
---

# How to design a system

## Overview

System Design is not “draw boxes until it looks smart.” It is a **repeatable thinking process** that turns a vague idea (“build Instagram”) into something an engineer can build, review, and operate.

In this tutorial you learn the process used in production design reviews and strong interviews:

**Business goals → Functional requirements → Non-functional requirements → Constraints → Assumptions → Capacity sketch → Trade-offs → Architecture → Validate**

You will practise on a small but realistic example: a **URL shortener** design brief (we implement full shorteners later; here we only practise the *process*).

This is **Module 1** of the REBASH Academy **System Design** course.

## Prerequisites

- Can read JSON and HTTP status codes
- Can run Python 3 on your machine
- Curiosity about how large systems behave

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Separate functional requirements from non-functional requirements  
- [ ] List constraints and assumptions explicitly  
- [ ] Perform a simple capacity estimate (requests/day, storage, bandwidth)  
- [ ] Name at least two trade-offs before proposing components  
- [ ] Produce a one-page design brief another engineer could challenge  

## Architecture

The process itself is an architecture of *thinking*. Keep this flow visible whenever you design:

![System design process](../assets/excalidraw/system-design-process.svg)

## Theory

### What System Design really is

When someone says “design Twitter,” beginners jump to Kafka and Kubernetes. Experts ask:

1. **Who is the user and what do they need to succeed?**  
2. **What must work on day one vs later?**  
3. **How big is “big” — numbers, not adjectives?**  
4. **What are we willing to give up?**  

Technology choices come **after** those answers. If you reverse the order, you decorate a solution that does not match the problem.

### Why a process beats improvisation

Without a process you get:

- Missing requirements discovered in production  
- Over-engineering (“we might need multi-region”) with no traffic  
- Under-engineering (single database) with no plan for growth  
- Interviews that wander because neither side shares a frame  

A shared process lets you and a reviewer argue about the *same* facts.

### Step 1 — Business goals (why the system exists)

Start with outcomes, not features.

| Weak | Stronger |
|------|----------|
| “Build a shortener” | “Let marketers share trackable short links so campaigns fit on SMS and billboards” |
| “Make it fast” | “Redirects must feel instant so users do not abandon the click” |

Ask: **What decision or user success does this enable?** If you cannot answer, you are not ready to design.

### Step 2 — Functional requirements (what it must do)

Write behaviours as **user stories or API capabilities**. Prefer verbs.

For a URL shortener MVP:

| ID | Requirement |
|----|-------------|
| F1 | Authenticated user can create a short link for a long URL |
| F2 | Anyone with the short link can be redirected to the long URL |
| F3 | Owner can see click count (basic analytics) |
| F4 | Short codes are unique |

Also list **out of scope for v1** (as important as in-scope):

- Custom domains  
- A/B testing  
- QR codes  
- Enterprise SSO  

Out-of-scope stops silent scope creep.

### Step 3 — Non-functional requirements (how well)

Non-functional requirements (NFRs) are measurable qualities. Vague words become numbers.

| Quality | Vague | Measurable (example) |
|---------|-------|----------------------|
| Latency | “Fast redirects” | p95 redirect &lt; 100 ms in-region |
| Availability | “Always up” | 99.9% monthly for redirect path |
| Durability | “Don’t lose links” | Zero accepted writes lost after ACK |
| Scale | “Lots of users” | 10M redirects/day year-one |
| Security | “Safe” | HTTPS only; no open redirects to `javascript:` |

If you cannot measure it, you cannot know when you are done.

### Step 4 — Constraints (hard walls)

Constraints are not preferences. Examples:

- Must launch in 6 weeks with 2 engineers  
- Must stay under $X/month cloud spend at year-one load  
- Must use company-approved languages (here: Python for labs)  
- Must keep personally identifiable data in region Y  

Design inside the walls. Fighting constraints wastes time.

### Step 5 — Assumptions (beliefs you will revisit)

Assumptions fill gaps. Write them down so others can challenge them.

Examples:

- Average long URL length ≈ 100 bytes  
- Read:write ratio ≈ 100:1 (many clicks, fewer creates)  
- Peak traffic ≈ 2× average  
- Short codes are 7 characters from a 62-char alphabet  

Wrong assumptions are fine **if visible**. Hidden assumptions become outages.

### Step 6 — Capacity sketch (back-of-envelope)

You are not predicting the future to three decimals. You are checking whether the design is **plausible**.

Worked example — **10 million redirects/day**:

1. **Requests/second (average)**  
   \(10{,}000{,}000 / 86{,}400 ≈ 116\) redirects/s average.  
   With 2× peak ≈ **230 redirects/s**. That is modest for a simple redirect service.

2. **New links/day** (assume 100:1 read:write)  
   \(10{,}000{,}000 / 100 = 100{,}000\) creates/day ≈ **1.2 creates/s**.

3. **Storage for 5 years of links**  
   100k/day × 365 × 5 ≈ 182.5M links.  
   If each record is ~500 bytes (URL + metadata) → ≈ **90 GB**. Fits on one large disk; plan for growth and backups.

4. **Bandwidth**  
   Redirect responses are small (HTTP 302 + headers). Bandwidth is rarely the first bottleneck; **lookup latency and availability** usually are.

Numbers tell you: start simple (one primary DB + cache), but design the **key** and **API** so you can shard later.

### Step 7 — Trade-offs before boxes

Before naming Redis or Kafka, name tensions:

| Tension | Option A | Option B |
|---------|----------|----------|
| Short code length | Short (pretty) → fewer combinations | Longer → more capacity, uglier links |
| Analytics | Sync write on every click → accurate, slower | Async queue → fast redirect, eventual counts |
| Consistency of creates | Strong uniqueness in one DB | Distributed IDs → harder uniqueness |

You will deepen trade-offs in [Module 2](quality-attributes-and-trade-offs.md). Here, habit matters: **trade-offs first, components second**.

### Step 8 — High-level architecture (only now)

For the shortener MVP, a honest first cut:

1. **API service** — create short links (auth, validate URL, store)  
2. **Redirect service** — lookup code → 302 (can be same deploy unit at first)  
3. **Datastore** — map `code → long_url`  
4. **Optional cache** — hot codes in memory  
5. **Async worker** (later) — click events for analytics  

Draw it. Label arrows with protocols (`HTTPS`, `SQL`). Mark what is sync vs async.

### Step 9 — Validate and iterate

Ask:

- Does this meet F1–F4 and the NFRs?  
- What fails first under 10× traffic?  
- What is the blast radius if the DB dies?  
- Can a new engineer implement the API from this brief?

If not, revise requirements or design — do not add random technology.

### Key concepts

| Concept | Remember |
|---------|----------|
| Functional vs non-functional | *What* vs *how well* |
| Constraints vs assumptions | Hard walls vs revisable beliefs |
| Capacity sketch | Order-of-magnitude, not precision theatre |
| Trade-off | Explicit sacrifice, not accidental |
| MVP scope | Ship learning; defer fancy |

### How it works in interviews

Strong candidates narrate the process out loud:

1. Clarify goals and scope (2–3 minutes)  
2. Agree NFRs and rough numbers  
3. Propose API + data model  
4. Walk the critical path (redirect)  
5. Deep-dive bottlenecks  
6. Call out failures and next scale step  

Weak candidates jump to buzzwords. Interviewers notice.

## Hands-on Lab

### Objective

Produce a **design brief** for a URL shortener MVP and a **Python capacity sketch** you can re-run when assumptions change.

### Prerequisites

- Python 3.10+  
- Terminal  

### Lab environment

Local machine only. No cloud account required.

### Real-world scenario

Your product manager says: “We need short links for SMS campaigns. Year one we expect about ten million clicks a day. Keep it simple.” You must return a one-page brief before anyone opens a pull request.

### Step-by-step tasks

#### 1. Create a workspace

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-system-design/module-01-process
cd ~/rebash-system-design/module-01-process
python3 --version | tee python-version.txt
```

!!! example "Expected output"
    `python-version.txt` contains a Python 3.x version line.

#### 2. Write the design brief template

Create `design_brief.md`:

```markdown title="design_brief.md"
# URL shortener — design brief (MVP)

## Business goal
Enable short, trackable links for SMS/billboard campaigns.

## Functional requirements
- F1: Create short link for a valid https URL (authenticated)
- F2: Redirect short code to long URL
- F3: Basic click count for owner
- F4: Unique short codes

## Out of scope (v1)
- Custom domains, A/B tests, QR codes, SSO

## Non-functional targets
- p95 redirect < 100 ms in-region
- 99.9% availability on redirect path
- 10M redirects/day year-one

## Constraints
- Small team; prefer one deployable Python service first
- Budget-conscious; avoid multi-region until needed

## Assumptions
- Read:write = 100:1
- Peak = 2 × average
- Avg long URL ≈ 100 bytes
- Record size ≈ 500 bytes

## Trade-offs (v1)
- Sync uniqueness in one primary DB vs distributed ID generators
- Async analytics vs slowing the redirect path

## High-level components
- API + redirect (same service OK for v1)
- Primary datastore for code → URL
- Cache for hot codes (optional day-one)
```

#### 3. Capacity estimator in Python

Create `capacity.py`:

```python title="capacity.py"
#!/usr/bin/env python3
"""Back-of-envelope capacity helpers for System Design briefs."""

from __future__ import annotations


def rps(daily_requests: float, peak_factor: float = 2.0) -> tuple[float, float]:
    avg = daily_requests / 86_400
    return avg, avg * peak_factor


def storage_gb(
    writes_per_day: float,
    years: float,
    bytes_per_record: float,
) -> float:
    total = writes_per_day * 365 * years * bytes_per_record
    return total / (1024**3)


def main() -> None:
    redirects_per_day = 10_000_000
    read_write_ratio = 100
    years = 5
    bytes_per_record = 500

    creates_per_day = redirects_per_day / read_write_ratio
    avg_rps, peak_rps = rps(redirects_per_day)
    store_gb = storage_gb(creates_per_day, years, bytes_per_record)

    lines = [
        f"redirects_per_day={redirects_per_day}",
        f"creates_per_day={creates_per_day:.0f}",
        f"avg_redirect_rps={avg_rps:.1f}",
        f"peak_redirect_rps={peak_rps:.1f}",
        f"storage_gb_{years}y={store_gb:.1f}",
    ]
    report = "\n".join(lines) + "\n"
    print(report, end="")
    with open("capacity-report.txt", "w", encoding="utf-8") as fh:
        fh.write(report)


if __name__ == "__main__":
    main()
```

#### 4. Run the estimator

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-system-design/module-01-process
python3 capacity.py | tee capacity-run.txt
grep -E 'peak_redirect_rps|storage_gb' capacity-report.txt
```

!!! example "Expected output"
    Report shows peak redirect RPS around `231.5` and multi-year storage on the order of tens of GB (exact figures match the script).

#### 5. Change an assumption and re-run

Edit `capacity.py` so `read_write_ratio = 20` (more creates). Re-run and save:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-system-design/module-01-process
python3 capacity.py | tee capacity-rw20.txt
```

!!! example "Expected output"
    `creates_per_day` and `storage_gb_*` increase versus the 100:1 run — proving assumptions drive capacity.

### Validation steps

- [ ] `design_brief.md` lists goals, FRs, NFRs, out-of-scope, constraints, assumptions, trade-offs  
- [ ] `capacity-report.txt` exists with RPS and storage lines  
- [ ] You can explain why peak RPS matters more than average for sizing  

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Division by zero / wrong RPS | Used hours instead of 86,400 seconds | Keep seconds/day explicit |
| Huge storage scare | Assumed kilobytes per click event forever | Separate link rows from analytics events |
| “Looks fine” without brief | Skipped writing requirements | No PR without a brief |

### Challenge exercise

Add a function that estimates **analytics event storage** if every redirect writes a 200-byte event for 30 days retention. Append results to `capacity-report.txt`.

### Learning outcomes

- Separated goals, functional, and non-functional requirements  
- Made assumptions visible and re-ran maths when they changed  
- Produced an engineer-ready MVP brief  

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-system-design/module-01-process
rm -f python-version.txt capacity-run.txt capacity-rw20.txt 2>/dev/null || true
# Keep design_brief.md and capacity.py as portfolio artefacts if you wish
```

## Validation

- [ ] You can recite the design process without looking  
- [ ] You wrote a brief another engineer could critique  
- [ ] Your capacity numbers match your assumptions  

## Interview Questions

**1. What do you clarify first in a System Design interview?**

??? success "Reveal answer"
    Business goal and scope (in vs out), then functional requirements, then measurable NFRs and rough scale. Technology comes after the problem is shared.

**2. Why write assumptions down?**

??? success "Reveal answer"
    So reviewers can challenge them. Hidden assumptions become silent failures when traffic or product behaviour differs.

**3. Is back-of-envelope maths supposed to be exact?**

??? success "Reveal answer"
    No. It checks order of magnitude — whether a laptop DB might work, or whether you already need sharding and multi-region.

**4. Give one trade-off for a URL shortener redirect path.**

??? success "Reveal answer"
    Accurate sync analytics vs lowest latency redirect. Many systems ACK the redirect fast and enqueue the click event asynchronously.

## Common Mistakes

!!! warning "Jumping to Kafka/Kubernetes before requirements"
    Fancy infrastructure cannot fix an unclear problem statement.

!!! warning "NFRs without numbers"
    “Highly available” is not a requirement until it has a target and a measurement method.

!!! warning "Treating the first architecture as final"
    Designs are hypotheses. Validate with load, failure drills, and product feedback.

## Best Practices

- Time-box clarification; write the brief before coding  
- Keep MVP brutal; schedule scale steps explicitly  
- Revisit assumptions when metrics disagree with the model  
- Prefer boring technology that meets NFRs  

## Summary

System Design starts with **why** and **how well**, not with product logos. You practised a full process: goals, requirements, constraints, assumptions, capacity, trade-offs, then architecture. The Python lab showed that changing one assumption changes the whole sizing story — which is exactly what good design reviews do.

## What's Next

Next, go deeper on the language of quality: [Quality attributes and trade-offs](quality-attributes-and-trade-offs.md).
