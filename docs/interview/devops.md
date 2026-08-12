---
title: "DevOps Fundamentals Interview Preparation"
description: "38 curated DevOps Fundamentals interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: devops
tags:
  - interview
  - devops
comments: false
---

{% raw %}
# DevOps Fundamentals Interview Preparation

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

**1. The server is extremely slow. How do you identify if the issue is CPU related and what is causing i?**

??? success "Reveal answer"
    **In short:** Confirm CPU saturation first (`user`/`system`/`steal`/`iowait`), then identify the hot process and why it is busy.
    
    **Key points**
    
    - `top`/`mpstat` show whether CPUs are truly maxed.
    - Sort processes; profile the offender before killing it.
    - High iowait is a disk story, not a pure CPU story.
    
    **Try this**
    
    - mpstat -P ALL 1
    - `ps aux --sort=-%cpu | head`
    
    **Trap**
    
    - Restarting the app before capturing profiles — evidence disappears.

## Scenarios and troubleshooting

**2. How would you handle scenarios where the payment succeeds but the order or shipping service fails?**

??? success "Reveal answer"
    **In short:** Use an outbox/saga pattern: payment success must eventually drive order/shipping, with compensating actions on failure.
    
    **Key points**
    
    - Make each step idempotent and record state transitions.
    - Retry shipping with backoff; alert on poison messages.
    - Compensating transaction: refund or park for manual ops if shipping cannot complete.
    
    **Try this**
    
    - Design: payment → outbox event → order → shipping
    
    **Trap**
    
    - Dual-writing payment and order without a correlation ID or recovery path.

**3. If a production instance is failing, what can be the possible causes?**

??? success "Reveal answer"
    **In short:** Production instance failure is usually health, capacity, config, dependency, or recent change — triage in that order.
    
    **Key points**
    
    - Check instance status, system metrics, and app logs.
    - Validate recent deploys, certs, disk full, OOM, and upstream deps.
    - Replace cattle hosts; debug pets carefully.
    
    **Try this**
    
    - cloud status checks
    - `journalctl -u <service> -e`
    - `df -h; free -h`
    
    **Trap**
    
    - Rebooting as step one without saving logs.

**4. New image has been deployed in production but it fails immediately what steps would you take?**

??? success "Reveal answer"
    **In short:** Treat an immediate prod failure as a bad deploy: freeze rollouts, roll back, then diagnose the image.
    
    **Key points**
    
    - Confirm version/SHA actually running.
    - Check crash logs, probes, config, and secret injection.
    - Reproduce in staging with the same artefact.
    
    **Try this**
    
    - `kubectl rollout undo deploy/<name>`
    - `kubectl logs -p <pod>`
    
    **Trap**
    
    - Hot-patching prod while traffic still hits the broken ReplicaSet.

**5. In Airflow, if a job fails, how do you debug it?**

??? success "Reveal answer"
    **In short:** In Airflow, open the failed task log, inspect the exception, then check upstream data and worker health.
    
    **Key points**
    
    - Read task logs first — most answers are there.
    - Clear/retry only after understanding idempotency.
    - Check scheduler/worker resources and connection/hooks.
    
    **Try this**
    
    - Airflow UI → Graph → Log
    - airflow tasks test <dag> <task> <date>
    
    **Trap**
    
    - Clearing a non-idempotent task and duplicating side effects.

**6. Now it is hosted and one of the services is leaking memory, how would you troubleshoot?**

??? success "Reveal answer"
    **In short:** Prove the leak with rising RSS/heap, capture a profile, then restart under control while you ship a fix.
    
    **Key points**
    
    - Watch container/cgroup memory and restart counts.
    - Use language profilers (`pprof`, `py-spy`, heap dumps).
    - Add limits and alerts so the next leak pages early.
    
    **Try this**
    
    - `kubectl top pod`
    - `heap profile / memory flamegraph`
    
    **Trap**
    
    - Removing memory limits so Kubernetes stops restarting it — you just hide the fire.

**7. How would you design an architecture for a 2 tier application?**

??? success "Reveal answer"
    **In short:** A two-tier design is presentation/app tier plus data tier, separated by networks and scaling axes.
    
    **Key points**
    
    - Web/app servers behind a load balancer.
    - Database on private subnets with backups.
    - Stateless app tier scales horizontally; data tier scales with care.
    
    **Try this**
    
    - LB → app ASG → private DB
    
    **Trap**
    
    - Putting the database on a public subnet for “easy access”.

**8. You are onboarding a new customer with 5 million+ users. How would you design the complete application architecture as a Solution Architect?**

??? success "Reveal answer"
    **In short:** For 5M+ users, design for multi-AZ high availability, horizontal scale, caching, and clear SLOs — not a single huge VM.
    
    **Key points**
    
    - Edge/CDN + API gateway + containerised services.
    - Managed data stores with replicas; cache hot paths.
    - Observability, security baselines, and load-tested autoscaling from day one.
    
    **Try this**
    
    - Sketch: CDN → gateway → services → cache/DB → async workers
    
    **Trap**
    
    - Designing only the happy path with no abuse, failure, or cost controls.

**9. If there is a sudden spike in traffic on the server, how will you troubleshoot it?**

??? success "Reveal answer"
    **In short:** Separate demand spike from failure: check traffic metrics, saturation, errors, then scale or shed load.
    
    **Key points**
    
    - Confirm QPS/latency/error rate vs baseline.
    - Autoscale or enable cache/rate limits; protect the database.
    - Watch downstream dependencies — your spike may be their outage.
    
    **Try this**
    
    - Check LB metrics + app RED metrics
    - Scale app tier; verify DB connections
    
    **Trap**
    
    - Blindly scaling the app when the database is already maxed.

**10. If a rollback fails, how will you handle it?**

??? success "Reveal answer"
    **In short:** If rollback fails, stop the bleed with traffic shift or feature disable, then recover forward with a known-good artefact.
    
    **Key points**
    
    - Fail traffic to the last healthy colour/cluster.
    - Avoid manual snowflake fixes under pressure unless documented.
    - Communicate status; preserve evidence for RCA.
    
    **Try this**
    
    - Shift traffic to previous environment
    - Redeploy last known-good SHA
    
    **Trap**
    
    - Running experimental fixes on all remaining healthy capacity.

**11. What is your approach to debug a CrashLoopBackOff?**

??? success "Reveal answer"
    **In short:** `CrashLoopBackOff` means the container starts, crashes, and Kubernetes backs off restarts — read previous logs first.
    
    **Key points**
    
    - `kubectl describe pod` for events/probes/OOM.
    - `kubectl logs --previous` for the crash.
    - Common causes: bad config, missing secret, failing migrate, probe misconfig.
    
    **Try this**
    
    - `kubectl describe pod <p>`
    - `kubectl logs <p> --previous`
    
    **Trap**
    
    - Deleting the pod repeatedly without reading `--previous` logs.

**12. If clients reporting 504 Gateway Timeout errors. describe your approach to debugging the issue?**

??? success "Reveal answer"
    **In short:** A 504 means a gateway timed out waiting upstream — find which hop is slow or dead.
    
    **Key points**
    
    - Check LB/API gateway timeouts vs app/proxy timeouts.
    - Inspect upstream latency, thread pools, and DB locks.
    - Correlate with deploys and dependency health.
    
    **Try this**
    
    - Compare gateway timeout vs app duration metrics
    - trace a single slow request
    
    **Trap**
    
    - Raising timeouts forever instead of fixing the stuck dependency.

**13. How failover and failback happens in DRS?**

??? success "Reveal answer"
    **In short:** In VMware Distributed Resource Scheduler (DRS) terms, failover/failback is more HA/SRM language — say how workloads move and return.
    
    **Key points**
    
    - HA restarts VMs on surviving hosts after failure.
    - Site Recovery / DR runbooks automate failover to a secondary site and controlled failback.
    - Clarify whether the interviewer means cluster DRS or DR failover.
    
    **Try this**
    
    - Ask: cluster HA vs site DR?
    - Test failback in a planned exercise
    
    **Trap**
    
    - Failing back too early while the primary site is still unstable.

**14. How do you ensure accountability and ownership in a DevOps team, especially during failures?**

??? success "Reveal answer"
    **In short:** Ownership means a named on-call, clear blameless RCA, and follow-up actions with due dates.
    
    **Key points**
    
    - Define service owners and escalation paths.
    - Incident commander role during sev events.
    - Track remediation to closure; do not stop at “restarted it”.
    
    **Try this**
    
    - On-call rota + incident channel + RCA template
    
    **Trap**
    
    - Blameless culture without action tracking — the same page repeats.

**15. If you're facing performance issues on a server, how do you troubleshoot?**

??? success "Reveal answer"
    **In short:** Troubleshoot performance with the USE/RED mindset: utilisation, saturation, errors — then profile the hot tier.
    
    **Key points**
    
    - Host: CPU, memory, disk, network.
    - App: latency percentiles, slow queries, GC, lock contention.
    - Change one variable; keep a timeline.
    
    **Try this**
    
    - `top/iostat/free`
    - app p95 latency + slow query log
    
    **Trap**
    
    - Tuning random configs without a baseline measurement.

**16. How would you redeploy this application with zero down time?**

??? success "Reveal answer"
    **In short:** Zero-downtime redeploy needs overlapping old/new instances, health checks, and traffic shift — blue/green or rolling.
    
    **Key points**
    
    - Rolling update or two colours behind a load balancer.
    - Drain connections; keep DB migrations backward-compatible.
    - Automate rollback on failed health checks.
    
    **Try this**
    
    - Rolling deploy with readiness probes
    - Blue/green cutover
    
    **Trap**
    
    - Running a breaking schema migration before the new code is live.

**17. You have a crashbackloop error. How would you fix this error?**

??? success "Reveal answer"
    **In short:** Fix CrashLoopBackOff by reading previous logs and events, correcting the root cause, then verifying a stable Ready state.
    
    **Key points**
    
    - Config/secret/command errors are the usual suspects.
    - Fix probes that kill slow-starting apps.
    - Confirm with `kubectl get pod` staying Ready.
    
    **Try this**
    
    - `kubectl logs <p> --previous`
    - `kubectl get pod -w`
    
    **Trap**
    
    - Disabling probes permanently to “make it green”.

**18. What happens if master node fails suddenly?**

??? success "Reveal answer"
    **In short:** If a Kubernetes control-plane (master) node fails, workloads usually keep running; API/scheduling may degrade until quorum recovers.
    
    **Key points**
    
    - Multi-master etcd quorum is the real availability story.
    - Node components retry; new scheduling waits on API health.
    - Use managed control planes when you can.
    
    **Try this**
    
    - `kubectl get --raw='/readyz?verbose'`
    - Check etcd/member health
    
    **Trap**
    
    - Assuming all Pods die when one control-plane node dies.

**19. How do you implement a retry mechanism for a failed API call?**

??? success "Reveal answer"
    **In short:** Retry failed API calls with bounded exponential backoff, jitter, and idempotency keys.
    
    **Key points**
    
    - Retry only transient errors (429/5xx/timeouts).
    - Cap attempts; send the rest to a dead-letter queue.
    - Make handlers idempotent so retries are safe.
    
    **Try this**
    
    - backoff + jitter + max attempts
    - Idempotency-Key header
    
    **Trap**
    
    - Retrying non-idempotent POSTs without keys — duplicate charges ensue.

**20. Explain the production issue which you have faced?**

??? success "Reveal answer"
    **In short:** Tell one real incident with symptom, impact, diagnosis, fix, and prevention — structure beats drama.
    
    **Key points**
    
    - State blast radius and customer effect.
    - Show the evidence trail (metrics/logs).
    - End with the change that stopped recurrence.
    
    **Try this**
    
    - Use STAR: Situation → Task → Action → Result
    
    **Trap**
    
    - Vague “we restarted and it worked” with no learning.

**21. Failover happend in DB, so connection is switched from A to B, during this time interval, if user is writing some data, how to manage that?**

??? success "Reveal answer"
    **In short:** During DB failover, writes may fail or split — use retries, fencing, and a single primary writer endpoint.
    
    **Key points**
    
    - Clients should reconnect via DNS/proxy that follows the new primary.
    - Idempotent writes + transactions reduce corruption risk.
    - Reject writes on the old primary (STONITH/fencing).
    
    **Try this**
    
    - Use a writer endpoint/proxy
    - Retry transient failover errors
    
    **Trap**
    
    - Allowing both nodes to accept writes (split brain).

**22. How would you restrict everything except two services?**

??? success "Reveal answer"
    **In short:** Restrict east-west/north-south traffic with allow-lists: only the two services may communicate on required ports.
    
    **Key points**
    
    - Network policies / security groups default deny.
    - Allow explicit service-to-service rules only.
    - Prove with connection tests and policy dry-runs.
    
    **Try this**
    
    - Default-deny NetworkPolicy + two allow rules
    
    **Trap**
    
    - Default-allow with a few deny rules — something always slips through.

**23. How would you implement optimistic locking a RESTful update endpoint to avoid lost updates?**

??? success "Reveal answer"
    **In short:** Optimistic locking uses a version/ETag: update only if the client still holds the latest version.
    
    **Key points**
    
    - Store `version` (or hash) on the resource.
    - `UPDATE … WHERE id=? AND version=?`; bump on success.
    - On mismatch return 409 Conflict for the client to reload.
    
    **Try this**
    
    - If-Match / ETag on REST updates
    - version column increment
    
    **Trap**
    
    - Last-write-wins without versions — silent lost updates.

**24. How would you secure the web app running in cloud from OWASP Top 10 attacks?**

??? success "Reveal answer"
    **In short:** Defend OWASP Top 10 with secure defaults: authn/z, input validation, least privilege, and continuous scanning.
    
    **Key points**
    
    - TLS everywhere; strong session/JWT handling.
    - Parameterised queries; CSP and safe templating against XSS.
    - Dependency scanning, WAF as a layer, secrets out of code.
    
    **Try this**
    
    - SAST/DAST in CI
    - WAF + security headers
    
    **Trap**
    
    - Believing a WAF alone makes the app safe.

**25. How would you get application level metrics?**

??? success "Reveal answer"
    **In short:** Get application metrics from the app itself — RED/USE via Prometheus instrumentation or APM agents.
    
    **Key points**
    
    - Expose `/metrics` or use OpenTelemetry.
    - Track latency, traffic, errors, saturation.
    - Dashboards + SLOs beat raw host CPU alone.
    
    **Try this**
    
    - Prometheus client library
    - Grafana dashboard on p95 + error rate
    
    **Trap**
    
    - Only monitoring host CPU while the app queues melt.

**26. How would you manage these microservices?**

??? success "Reveal answer"
    **In short:** Manage microservices with clear ownership, CI/CD, service mesh/platform standards, and contract testing.
    
    **Key points**
    
    - One pipeline and artefact per service.
    - Shared platform for deploy, secrets, and observability.
    - Avoid a distributed monolith of tight runtime coupling.
    
    **Try this**
    
    - Service catalog + golden path templates
    
    **Trap**
    
    - One giant shared database that couples every service release.

**27. How would you expose the application?**

??? success "Reveal answer"
    **In short:** Expose the app through a managed edge: DNS → load balancer/Ingress/API gateway → services on private networks.
    
    **Key points**
    
    - Terminate TLS at the edge; keep backends private.
    - Use Ingress/Gateway API or cloud LBs as appropriate.
    - Health checks gate registration.
    
    **Try this**
    
    - DNS → LB/Ingress → Service → Pods
    
    **Trap**
    
    - Publishing node ports on every worker for convenience.

**28. How would you update the image and deploy them?**

??? success "Reveal answer"
    **In short:** Update images by pinning a new digest/tag in Git and letting the pipeline or GitOps controller roll out.
    
    **Key points**
    
    - Build once; promote the same digest.
    - Rolling/blue-green with probes and automated rollback.
    - Record the change ticket ↔ SHA mapping.
    
    **Try this**
    
    - Update image digest in manifests
    - `kubectl/argo rollout status`
    
    **Trap**
    
    - Deploying `:latest` and hoping all nodes pulled the same bytes.

**29. If you have an on-prem application, how would you migrate and deploy it in a cloud-native environment?**

??? success "Reveal answer"
    **In short:** Migrate on-prem to cloud-native by strangling capabilities: containerise, externalise config/state, then cut traffic gradually.
    
    **Key points**
    
    - Assess dependencies, data, and compliance first.
    - Lift wisely — refactor where scale/security demands it.
    - Use dual-run and clear rollback until cutover.
    
    **Try this**
    
    - Inventory → pilot service → dual-run → cutover
    
    **Trap**
    
    - Big-bang rewrite with no dual-run period.

**30. How would you structure disaster recovery for your applciation?**

??? success "Reveal answer"
    **In short:** Disaster recovery needs RTO/RPO targets, tested backups, and a documented failover path to another region/site.
    
    **Key points**
    
    - Define tiers: pilot light, warm standby, or active-active.
    - Back up data and GitOps config; test restores.
    - Run game days — untested DR is fiction.
    
    **Try this**
    
    - Write RTO/RPO
    - Restore test from backup quarterly
    
    **Trap**
    
    - Assuming multi-AZ equals multi-region DR.

**31. How would you perform database migration for your database application?**

??? success "Reveal answer"
    **In short:** Migrate databases with expand/contract: additive schema first, dual-write or replicate, then switch reads/writes.
    
    **Key points**
    
    - Prefer backward-compatible migrations.
    - Use logical replication / blue-green DB patterns where available.
    - Always rehearse rollback.
    
    **Try this**
    
    - expand → migrate → contract
    - Take a restorable backup first
    
    **Trap**
    
    - Destructive column drops in the same release as new code.

**32. How would you provision karpenter. What all things are needed in configuration?**

??? success "Reveal answer"
    **In short:** Karpenter needs cluster identity, a node class/pool, subnet/security group discovery, and IAM permission to manage nodes.
    
    **Key points**
    
    - Install controller with IRSA/workload identity.
    - Define NodePool/NodeClass (instance types, capacity type, disruption).
    - Ensure CIAM/tags for subnets and AMI family selection.
    - Watch consolidation settings so it does not thrash.
    
    **Try this**
    
    - Deploy Karpenter controller + NodePool CRDs
    - Verify pending pods schedule onto new nodes
    
    **Trap**
    
    - Over-permissive IAM that lets the controller alter unrelated ASGs.

**33. What is CrashLoopBackOff, and how do you troubleshoot it?**

??? success "Reveal answer"
    **In short:** `CrashLoopBackOff` is Kubernetes backing off restart of a crashing container — debug with describe + previous logs.
    
    **Key points**
    
    - Events reveal probes/OOM/image pulls.
    - Logs reveal app exceptions.
    - Fix root cause; confirm Ready stays true.
    
    **Try this**
    
    - `kubectl describe pod`
    - `kubectl logs --previous`
    
    **Trap**
    
    - Increasing backoff blindly instead of fixing the crash.

**34. What is your approach of doing a troubleshooting?**

??? success "Reveal answer"
    **In short:** Troubleshooting approach: define symptom, scope impact, gather evidence, hypothesise, change one thing, verify, document.
    
    **Key points**
    
    - Time-box and communicate early.
    - Prefer known-good rollback when user impact is high.
    - Capture timelines for RCA.
    
    **Try this**
    
    - Symptom → evidence → hypothesis → action → verify
    
    **Trap**
    
    - Skipping reproduction/evidence and jumping to random restarts.

## Practice questions

**35. What challenges have you faced implementing DevOps in previous projects?**

??? success "Reveal answer"
    **In short:** Common DevOps adoption challenges: culture, flaky pipelines, snowflake servers, and unclear ownership.
    
    **Key points**
    
    - Tooling without process change fails.
    - Measure DORA-ish outcomes, not tool count.
    - Start with a golden path and a pilot team.
    
    **Try this**
    
    - Pilot one service end-to-end before a platform mandate
    
    **Trap**
    
    - Buying a platform tool and expecting culture to rewrite itself.

**36. Design an architecture for the scenario: if I type www.application.com it should get resolved to the backend service?**

??? success "Reveal answer"
    **In short:** Browser → DNS → CDN/WAF → load balancer/Ingress → app service → data stores, with TLS and health checks at each hop.
    
    **Key points**
    
    - DNS points to the edge, not a single VM IP.
    - Private backends; public edge only.
    - Observability from DNS to DB.
    
    **Try this**
    
    - `www → Route53/Cloud DNS → ALB/Ingress → Service`
    
    **Trap**
    
    - One elastic IP on one instance as “the architecture”.

**37. If U want to design a infra for high scalablity, how did u do that?**

??? success "Reveal answer"
    **In short:** High scalability comes from stateless compute, horizontal autoscaling, caching, async work, and partitioned data.
    
    **Key points**
    
    - Remove session stickiness where possible.
    - Autoscale on saturation signals, not CPU alone.
    - Protect data stores with queues and caches.
    
    **Try this**
    
    - Stateless app tier + cache + queue + read replicas
    
    **Trap**
    
    - Vertical scaling a monolith forever and calling it strategy.

**38. Create system design for three tier architecture with secuirty and avalability in place?**

??? success "Reveal answer"
    **In short:** Three-tier with security and availability: edge, app, and data tiers across multiple AZs, private data plane, and tested backups.
    
    **Key points**
    
    - Public edge (CDN/LB/WAF); private app; private DB subnets.
    - Multi-AZ app and database failover.
    - IAM least privilege, secrets manager, encryption in transit/at rest.
    - Health checks, autoscaling, and restore-tested backups.
    
    **Try this**
    
    - Sketch multi-AZ three-tier with WAF and private DB
    
    **Trap**
    
    - Single-AZ “HA” that dies with one data-centre event.

## Related
- Hub: [Interview Preparation](index.md)
{% endraw %}
