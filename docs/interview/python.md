---
title: "Python Interview Preparation"
description: "19 curated Python interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: python
tags:
  - interview
  - python
comments: false
---

{% raw %}
# Python Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. What is Python's role in DevOps?**

??? success "Reveal answer"
    **In short:** Python is the glue language of DevOps — automation, APIs, cloud SDKs, and glue between tools.
    
    **Key points**
    
    - Common uses: boto3/Azure/GCP SDKs, Ansible modules, CLI tools, and data wrangling.
    - Readability and libraries beat micro-benchmarks for ops scripts.
    - Package with `uv`/`pip` + virtualenvs; pin dependencies.
    
    **Try this**
    
    - `python3 -m venv .venv`
    - `pip install boto3`
    
    **Trap**
    
    - Shipping unpinned scripts that break when a transitive dependency updates.

**2. What are Lists and Tuples in Python?**

??? success "Reveal answer"
    **In short:** Lists are mutable sequences; tuples are immutable sequences.
    
    **Key points**
    
    - Lists: grow/shrink, sort in place — good for collections you change.
    - Tuples: hashable when contents are hashable — good for fixed records/dict keys.
    - Prefer tuples for “this will not change” contracts.
    
    **Try this**
    
    - a=[1,2]; a.append(3)
    - t=(1,2); # t[0]=9 fails
    
    **Trap**
    
    - Using a list as a dict key — unhashable type error.

**3. What is search keyword in Python?**

??? success "Reveal answer"
    **In short:** Interviewers usually mean searching collections or strings — Python has no single `search` keyword.
    
    **Key points**
    
    - Strings: `in`, `str.find`, `re.search`.
    - Lists: `in`, or bisect on sorted data.
    - Dicts: key lookup is the common “search”.
    
    **Try this**
    
    - "err" in line
    - re.search(r'ERROR', line)
    
    **Trap**
    
    - Confusing `str.find` (-1 on miss) with `index` (raises).

**4. What is the difference between shallow copy and deep copy in Python?**

??? success "Reveal answer"
    **In short:** A shallow copy duplicates the outer container; nested objects are still shared. A deep copy recurses.
    
    **Key points**
    
    - `list.copy()` / `copy.copy()` are shallow.
    - `copy.deepcopy()` clones nested structures.
    - Mutating a nested list via a shallow copy surprises people.
    
    **Try this**
    
    - import copy
    - copy.copy(x)
    - copy.deepcopy(x)
    
    **Trap**
    
    - Assuming `b = a` copies — it only binds another name.

**5. What is list and tuple in python?**

??? success "Reveal answer"
    **In short:** List = mutable sequence; tuple = immutable sequence — same distinction as Q2.
    
    **Key points**
    
    - Syntax: `[1, 2]` vs `(1, 2)`.
    - Tuples can be dict keys if elements are hashable.
    - Use lists for working sets; tuples for fixed records.
    
    **Try this**
    
    - type([1,2])
    - type((1,2))
    
    **Trap**
    
    - Saying tuples are “faster lists” without mentioning immutability/hashability.

**6. What are decorators in Python?**

??? success "Reveal answer"
    **In short:** Decorators are functions (or classes) that wrap another callable to add behaviour.
    
    **Key points**
    
    - `@timer` / `@lru_cache` / Flask route decorators are everyday examples.
    - They run at definition time and return a wrapper.
    - Use `functools.wraps` to preserve metadata.
    
    **Try this**
    
    - from functools import wraps
    
    **Trap**
    
    - Forgetting `wraps` and breaking introspection/tests.

**7. What is the difference between set and list in python(Counter question of the above)?**

??? success "Reveal answer"
    **In short:** A set is an unordered unique collection; a list is an ordered sequence that allows duplicates.
    
    **Key points**
    
    - Sets give O(1)-average membership tests.
    - Lists keep order and positions.
    - Use set operations for diffs/unions of IDs.
    
    **Try this**
    
    - set([1,1,2])
    - 1 in {1,2,3}
    
    **Trap**
    
    - Expecting sets to preserve insertion order in old interview answers — know your Python version.

**8. Can you explain how Python works with cloud services in DevOps?**

??? success "Reveal answer"
    **In short:** Python drives cloud via official SDKs and HTTP APIs — provision, audit, and automate outside the console.
    
    **Key points**
    
    - Examples: boto3, Azure SDK, google-cloud-* libraries.
    - Use IAM roles/instance identities, not long-lived keys in code.
    - Idempotent scripts + retries + structured logging belong in production glue.
    
    **Try this**
    
    - `python -c 'import boto3; print(boto3.client("s3").list_buckets().keys())'`
    
    **Trap**
    
    - Hard-coding access keys in repositories.

**9. How does Python's GIL affect multi-threaded web service performance and what alternatives exist to overcome it? what is Python's GIL affect multi-threaded web service?**

??? success "Reveal answer"
    **In short:** The Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time — CPU-bound threads do not scale on multicore.
    
    **Key points**
    
    - I/O-bound threads can still help because they release the GIL on I/O.
    - Alternatives: multiprocessing, process pools, asyncio for concurrency, or native extensions.
    - For web services, run multiple processes (gunicorn workers) behind a load balancer.
    
    **Try this**
    
    - Use multiprocessing for CPU-bound work
    - Scale out with more processes/pods
    
    **Trap**
    
    - Adding threads to a CPU-heavy parser and expecting linear speed-up.

**10. In Python, what are lists and tuples, and how do they differ?**

??? success "Reveal answer"
    **In short:** Lists are mutable ordered collections; tuples are immutable ordered collections.
    
    **Key points**
    
    - Choose by mutability needs, not habit.
    - Unpacking and iteration work the same.
    - Immutability enables safer sharing and hashing.
    
    **Try this**
    
    - coords = (10, 20)
    - items = [10, 20]
    
    **Trap**
    
    - Mutating a list that was passed into a function and surprising the caller.

## Scenarios and troubleshooting

**11. If a Python program is failing due to memory issues, what can be the cause?**

??? success "Reveal answer"
    **In short:** Python memory pressure usually comes from unbounded growth: caches, big lists, leaks of references, or reading huge files at once.
    
    **Key points**
    
    - Profile with `tracemalloc`, `objgraph`, or process RSS metrics.
    - Stream files/lines; avoid building giant lists.
    - Watch circular refs and global caches in long-running workers.
    
    **Try this**
    
    - `python -X tracemalloc=1 app.py`
    - `ps aux --sort=-%mem | head`
    
    **Trap**
    
    - Loading an entire multi-GB log into memory to “parse quickly”.

**12. Write a Python function that takes a list of dictionaries representing job logs. The function should return a list of job IDs where the "status" is "FAILED"?**

??? success "Reveal answer"
    **In short:** Filter the list of dicts where `status == "FAILED"` and return their job IDs.
    
    **Key points**
    
    - Comprehension: `[j['id'] for j in jobs if j.get('status') == 'FAILED']`.
    - Defend against missing keys with `.get`.
    - Keep it pure and unit-tested.
    
    **Try this**
    
    ```python
    def failed_job_ids(jobs):
        return [j['id'] for j in jobs if j.get('status') == 'FAILED']
    ```
    
    **Trap**
    
    - Assuming every dict has `id`/`status` without validating input.

**13. How would you manage environment variables in Python for a DevOps project?**

??? success "Reveal answer"
    **In short:** Read configuration from environment variables (and secret stores), not hard-coded constants.
    
    **Key points**
    
    - `os.environ["KEY"]` or `os.getenv` with defaults for non-secrets.
    - Use `.env` only for local dev; inject secrets from CI/vault in prod.
    - Fail fast on missing required variables.
    
    **Try this**
    
    - import os; region = os.environ["AWS_REGION"]
    
    **Trap**
    
    - Committing `.env` files with real credentials.

## Practice questions

**14. How do you handle exceptions in Python scripts for DevOps automation?**

??? success "Reveal answer"
    **In short:** Catch expected exceptions at boundaries, log with context, and exit non-zero for automation.
    
    **Key points**
    
    - Prefer specific exceptions over bare `except:`.
    - Use `try/except/else/finally` for cleanup.
    - In CLIs, map errors to exit codes CI understands.
    
    **Try this**
    
    ```python
    try:
        run()
    except TimeoutError as e:
        logging.exception('timed out')
        raise SystemExit(2) from e
    ```
    
    **Trap**
    
    - Swallowing all exceptions and returning success to CI.

**15. How do you use Python to monitor server health in DevOps?**

??? success "Reveal answer"
    **In short:** Poll host/app signals with Python, emit metrics/logs, and alert on thresholds — or better, scrape with exporters.
    
    **Key points**
    
    - Read `/proc`, call cloud APIs, or hit `/health` endpoints.
    - Prefer Prometheus exporters over custom SSH polling when possible.
    - Include timeouts, retries, and structured logs.
    
    **Try this**
    
    - requests.get(url, timeout=2)
    - psutil.cpu_percent(interval=1)
    
    **Trap**
    
    - SSH fan-out every minute from a laptop script as your “monitoring platform”.

**16. Write python program for reverse a string?**

??? success "Reveal answer"
    **In short:** Reverse a string with slicing: `s[::-1]` — or `''.join(reversed(s))`.
    
    **Key points**
    
    - Slicing is the idiomatic interview answer.
    - Unicode: be careful with code points vs grapheme clusters.
    - For lists, `list.reverse()` mutates in place.
    
    **Try this**
    
    - s = "rebash"; print(s[::-1])
    
    **Trap**
    
    - Manual index loops that break on empty strings.

**17. Create a python script for this requirement?**

??? success "Reveal answer"
    **In short:** Clarify the requirement, then write a small script with `argparse`, logging, and exit codes.
    
    **Key points**
    
    - Interview prompt is incomplete — restate assumptions aloud.
    - Structure: parse args → validate → do work → report.
    - Ship tests for the core function.
    
    **Try this**
    
    - `python script.py --help`
    
    **Trap**
    
    - Coding immediately without confirming inputs/outputs.

**18. Do you have any experience on python scripting?**

??? success "Reveal answer"
    **In short:** Answer with concrete scripts you shipped — not a yes/no.
    
    **Key points**
    
    - Name domains: cloud SDK automation, log parsing, CI helpers, Flask/FastAPI glue.
    - Mention packaging, testing, and how you handled secrets.
    - Be honest about depth; show learning velocity.
    
    **Try this**
    
    - Keep 2–3 repo links or snippets ready
    
    **Trap**
    
    - Claiming “expert” with only notebook one-liners.

**19. How to configure the Flask in Jenkin, tell me procedure?**

??? success "Reveal answer"
    **In short:** Build and test the Flask app in Jenkins, then deploy the artefact — do not run Flask’s dev server as production.
    
    **Key points**
    
    - Pipeline stages: checkout → install deps → unit tests → build image/wheel → deploy.
    - Run production with gunicorn/uvicorn behind a reverse proxy.
    - Inject env/secrets via Jenkins credentials or the platform.
    
    **Try this**
    
    - Jenkinsfile: test → docker build → deploy
    - gunicorn app:app
    
    **Trap**
    
    - Using `flask run` on a prod VM managed by Jenkins.

## Related
- Course: [Python](../python/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
