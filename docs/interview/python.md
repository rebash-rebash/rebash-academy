---
title: "Python for DevOps Interview Prep"
description: "25–30 interview questions covering Python fundamentals, OOP, files, REST APIs, automation, Kubernetes, Docker, Terraform, cloud SDKs, and production scenarios."
difficulty: intermediate
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: interview
tags:
  - interview
  - python
  - devops
comments: false
---

# Python for DevOps Interview Prep

Practice answers for DevOps, platform, and SRE interviews. Prefer concrete examples from the [Python for DevOps track](../python/index.md).

## Fundamentals (1–5)

1. **When do you choose Python over Bash for ops work?**  
   Bash for composing OS tools and exit-code pipelines; Python for structured data (JSON/YAML), HTTP APIs, retries, unit tests, and packaged CLIs.

2. **Why use a virtual environment?**  
   Isolate dependencies per project so CI and laptops resolve the same versions; avoid polluting the system interpreter.

3. **How do you pin dependencies for automation tools?**  
   Pin ranges or lock with uv/Poetry (`requirements.txt` hashes or `uv.lock`) so builds are reproducible.

4. **What is a sensible exit-code taxonomy for CLIs?**  
   `0` success, `2` usage/validation errors, `1` (or a small set) for runtime failures — document it for callers and CI.

5. **Explain list vs generator for large log files.**  
   Generators/`for line in file` stream; lists hold everything in memory and can OOM on multi-gigabyte logs.

!!! tip "Sample answer — Python vs Bash"
    Use Bash when you are composing OS tools and care about exit codes. Switch to Python when you need models, retries, tests, or a reusable package.

## OOP (6–8)

6. **When are dataclasses useful in ops tooling?**  
   For inventory records, findings, and config models — less boilerplate than hand-written classes, clear fields for JSON serialisation.

7. **Inheritance vs composition for cloud adapters?**  
   Prefer composition: a shared `InventoryClient` protocol with AWS/Azure/GCP adapters keeps blast radius and testing simpler than deep hierarchies.

8. **What belongs in `__init__` vs methods for a CLI service object?**  
   Construct clients/config once in `__init__`; keep side-effecting I/O in methods so tests can inject fakes.

## File handling (9–11)

9. **Why prefer pathlib over string concatenation?**  
   Safer joins across OSes, richer API (`glob`, `read_text`, `resolve`), fewer separator bugs.

10. **Why `yaml.safe_load` not `yaml.load`?**  
   Unsafe loaders can construct arbitrary Python objects — a security risk for untrusted manifests.

11. **How do you handle partial writes of reports?**  
   Write to a temporary file then `replace()` atomically so readers never see truncated JSON.

## REST APIs (12–14)

12. **What must every HTTP client set in automation?**  
   Timeouts (connect and read). Hung calls stall pipelines and on-call scripts.

13. **How do you authenticate without leaking secrets?**  
   Env vars or a secret store; never commit tokens; redact in logs; prefer short-lived OIDC/federation.

14. **How do you handle pagination and rate limits?**  
   Follow next-page tokens/`Link` headers; honour `Retry-After`; exponential backoff on 429/5xx for idempotent GETs.

!!! tip "Sample answer — timeouts"
    Default httpx/requests without a timeout can block forever. Set an explicit timeout and fail with a clear log line the on-call can search.

## Automation (15–17)

15. **Why avoid `shell=True` in subprocess?**  
   Untrusted input can inject metacharacters. Pass argv as a list so each argument is literal.

16. **How do you structure a multi-source inventory CLI?**  
   Shared record model, pluggable adapters, continue-on-error per source, JSON/table export, offline fixtures for tests.

17. **What is a dry-run default and why?**  
   Destructive Docker/K8s/cloud actions should report first; require `--apply` (or equivalent) to mutate — reduces accidental blast radius.

## Kubernetes (18–20)

18. **How do you check Pod readiness with the Python client?**  
   List Pods, inspect `status.conditions` / container ready flags; treat CrashLoopBackOff as unhealthy — read-only.

19. **What identity should automation use in-cluster?**  
   A dedicated ServiceAccount with least-privilege RBAC (get/list in one namespace), not cluster-admin.

20. **How do you test K8s automation in CI without a cluster?**  
   Fixture JSON / recorded API objects; optional kind job gated separately.

## Docker (21–22)

21. **How do you clean dangling images safely?**  
   List and report sizes first; filter by age/label; delete only with `--apply`; never prune volumes blindly on shared hosts.

22. **What if the Docker daemon is unavailable?**  
   Fail clearly or switch to a fixture path so unit tests and workshops still run.

## Terraform (23–24)

23. **How should Python wrap Terraform?**  
   Subprocess with list args for `fmt`/`validate`/`plan`/`show -json`; never hide `apply` behind silent defaults; summarise resource_changes for PRs.

24. **Why parse plan JSON instead of scraping text?**  
   Stable machine-readable fields; better for CI comments and policy checks.

## Cloud SDKs (25–26)

25. **How do you inventory EC2 without embedding keys?**  
   Instance roles, OIDC in CI, or local profiles; labs/tests use fixture `describe_instances` JSON when credentials are absent.

26. **What is a normalised multi-cloud inventory record?**  
   Common fields: id, provider, type, region/location, state, tags/labels — adapters map provider quirks into that shape.

## Production scenarios (27–30)

27. **Cron job works interactively but fails scheduled.**  
   Use the venv’s absolute interpreter; set `PATH`; do not rely on aliases or interactive env vars; log to a file/journald.

28. **Token appeared in pipeline logs — what do you do?**  
   Rotate immediately; mask CI variables; add redacting filters; scan git history; treat as compromise.

29. **pytest strategy for platform CLIs?**  
   Unit-test parsers and exit codes with fixtures; mock HTTP/cloud; one optional integration job gated by secrets.

30. **Memory grows on a long-running monitor.**  
   Avoid unbounded caches; stream responses; profile with `tracemalloc`; bound queues; restart policy as a backstop — fix the leak.

!!! tip "Sample answer — dry-run"
    Default `--dry-run` for prune/delete/apply wrappers. Operators pass `--apply` deliberately. Document the flag in `--help` and the runbook.

## Related

- Track: [Python for DevOps](../python/index.md)
- Cheat sheet: [Python](../cheatsheets/python.md)
- Lab: [Python Log Analyser](../labs/python-log-analyser.md)
- Quiz: [Python for DevOps Engineers Fundamentals](../quizzes/python-for-devops-engineers-fundamentals.md)
- Capstone: [Production DevOps Automation Platform](../projects/python-devops-automation-framework.md)
- Learning path: [Python for DevOps Engineers](../learning-paths/python-for-devops.md)
