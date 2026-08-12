---
title: "Monitoring & Observability Interview Preparation"
description: "36 curated Monitoring & Observability interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: monitoring
tags:
  - interview
  - monitoring
comments: false
---

{% raw %}
# Monitoring & Observability Interview Preparation

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

**1. What is Prometheus, and how does it collect metrics?**

??? success "Reveal answer"
    **In short:** Prometheus stores time-series metrics and primarily pulls them by scraping HTTP `/metrics` endpoints.
    
    **Key points**
    
    - Scrape configs define targets, intervals, and labels.
    - Service discovery (Kubernetes, EC2, Consul) finds targets dynamically.
    - Exporters expose host/DB metrics; apps use client libraries.
    - Alerting rules evaluate PromQL; Alertmanager handles routing.
    
    **Try this**
    
    - `promtool check config prometheus.yml`
    - `curl -s localhost:9090/metrics | head`
    
    **Trap**
    
    - Pushing everything into Pushgateway — it is for short-lived batch jobs, not normal services.

**2. Can you explain the ELK stack and how you've used it?**

??? success "Reveal answer"
    **In short:** ELK is Elasticsearch + Logstash + Kibana for centralised search and visualisation of logs.
    
    **Key points**
    
    - **Elasticsearch** — stores and indexes documents.
    - **Logstash** (or Beats/Elastic Agent) — ingest and transform.
    - **Kibana** — search, dashboards, alerting.
    - Used for app/audit logs, incident forensics, and ops dashboards.
    
    **Trap**
    
    - Indexing high-cardinality fields (user IDs as field names) and melting the cluster.

**3. What are the observability needed for app?**

??? success "Reveal answer"
    **In short:** Apps need the three pillars: metrics, logs, and traces — tied together with context.
    
    **Key points**
    
    - **Metrics** — RED/USE: rate, errors, duration; saturation.
    - **Logs** — structured, correlatable with request IDs.
    - **Traces** — spans across services for latency paths.
    - Plus health checks, SLOs, and dependency/uptime probes.
    
    **Trap**
    
    - Only CPU graphs — blind to user-facing errors and slow traces.

**4. What is Prometheus, Grafana, Loki?**

??? success "Reveal answer"
    **In short:** Prometheus scrapes metrics; Grafana visualises them; Loki stores log streams with similar labels.
    
    **Key points**
    
    - Prometheus: metrics + rules; Alertmanager for notifications.
    - Grafana: dashboards over Prometheus, Loki, Tempo, and more.
    - Loki: cheap log aggregation keyed by labels, not full-text indexes like ES.
    - Together they form a common open observability stack.
    
    **Trap**
    
    - Treating Loki like Elasticsearch for heavy unstructured full-text forensics without design.

**5. What are data sources for Grafana, Kibana?**

??? success "Reveal answer"
    **In short:** Grafana and Kibana both visualise data — but from different typical backends.
    
    **Key points**
    
    - **Grafana** — Prometheus, Loki, Tempo, CloudWatch, Azure Monitor, SQL, etc.
    - **Kibana** — primarily Elasticsearch (and Elastic stack features).
    - Pick based on where telemetry already lives.
    - Many teams use Grafana for metrics/traces and Elastic for deep log search.
    
    **Trap**
    
    - Duplicating every metric into Elasticsearch “so Kibana can see it” — costly and slow.

**6. What are indices, index in Kibana?**

??? success "Reveal answer"
    **In short:** An Elasticsearch index is a collection of documents; Kibana patterns let you query groups of indices.
    
    **Key points**
    
    - Indices store shards of JSON-like documents with mappings.
    - Time-based indices (`logs-2026.08.12`) aid retention/ILM.
    - Index patterns / data views in Kibana select which indices to search.
    - Aliases point apps at stable names while indices rotate.
    
    **Trap**
    
    - One giant everlasting index with no ILM — disk fills and queries crawl.

**7. What are the alerts you setup on graffana?**

??? success "Reveal answer"
    **In short:** Alert on symptoms that burn error budgets — not every noisy gauge spike.
    
    **Key points**
    
    - SLO burn: error rate, latency p99, saturation.
    - Infra: disk >80%, certificate expiry, kube node NotReady.
    - Dependencies: queue lag, DB connections, upstream 5xx.
    - Route by severity to pager vs ticket; include runbook links.
    
    **Trap**
    
    - Alerting on CPU >70% forever — classic alert fatigue.

**8. Difference between observality and monitoring?**

??? success "Reveal answer"
    **In short:** Monitoring watches known metrics/health; observability lets you ask new questions when something breaks.
    
    **Key points**
    
    - **Monitoring** — predefined checks and alerts (uptime, CPU, error rate).
    - **Observability** — high-cardinality telemetry (logs/metrics/traces) for unknown unknowns.
    - You need both: alerts to wake you; telemetry to explain why.
    - OpenTelemetry is the common instrumentation approach.
    
    **Trap**
    
    - Renaming your Zabbix box “observability platform” without traces or context.

**9. What is Logstash Grok filter?**

??? success "Reveal answer"
    **In short:** Grok parses unstructured log lines into fields using patterns (like named regex).
    
    **Key points**
    
    - Used in Logstash filters: `grok { match => { "message" => "%{COMBINEDAPACHELOG}" } }`.
    - Extracts status, latency, user, path for indexing/alerting.
    - Prefer structured JSON logs to avoid brittle grok.
    - Test patterns before deploying to production ingest.
    
    **Try this**
    
    - Kibana Grok Debugger
    - `%{IP:client} %{WORD:method}`
    
    **Trap**
    
    - One tiny log format change silently breaks grok and drops fields for days.

**10. What is the difference between Logstash and Fluentd?**

??? success "Reveal answer"
    **In short:** Both collect/ship logs; Logstash is a heavy pipeline JVM, Fluentd is a lighter unified logging layer.
    
    **Key points**
    
    - Logstash: rich filter ecosystem inside the Elastic stack.
    - Fluentd/Fluent Bit: CNCF, common as DaemonSets to forward to ES/Loki/S3.
    - Fluent Bit often preferred at the edge for low resource use.
    - Choose based on ops skill, latency, and destination stack.
    
    **Trap**
    
    - Running Logstash on every node “because Elastic” when Fluent Bit would do.

## Scenarios and troubleshooting

**11. How do you recover a failed service in production?**

??? success "Reveal answer"
    **In short:** Restore service first within SLO, then find root cause — don’t debug forever while users burn.
    
    **Key points**
    
    - Mitigate: rollback, failover, scale out, feature-flag off.
    - Confirm with metrics/logs/traces that user impact is falling.
    - Preserve evidence (logs, deploy SHA) before chaotic restarts.
    - Post-incident: fix forward and add a detection for next time.
    
    **Trap**
    
    - Restarting pods in a loop without capturing `--previous` logs.

**12. Your production application is completely down. | Users cannot access the service. What do you do first?**

??? success "Reveal answer"
    **In short:** Declare the incident, stop the blast radius, then restore traffic — communication is part of the fix.
    
    **Key points**
    
    - Page on-call; open an incident channel; assign commander.
    - Check last deploy, dependencies, and platform status pages.
    - Mitigate: rollback/failover; verify with synthetic checks.
    - Update stakeholders with clear impact and ETA.
    
    **Trap**
    
    - Silent debugging for 40 minutes while customers discover the outage on Twitter.

**13. How would you handle logging in Linux?**

??? success "Reveal answer"
    **In short:** On Linux, use the journal and files under `/var/log`, preferably structured and shipped centrally.
    
    **Key points**
    
    - `journalctl -u service` for systemd units.
    - App logs to stdout/stderr in containers; node agents ship them.
    - Rotate with `logrotate`; watch disk usage.
    - Add correlation IDs; avoid secrets in logs.
    
    **Try this**
    
    - `journalctl -u nginx -n 100 --no-pager`
    - `df -h /var/log`
    
    **Trap**
    
    - Debug logging left on in prod filling the disk and taking the box down.

**14. How do you set up monitoring and observability for ML models in production?**

??? success "Reveal answer"
    **In short:** Monitor training/serving pipelines: data drift, prediction quality, latency, and resource use.
    
    **Key points**
    
    - Online metrics: latency, error rate, throughput of model endpoints.
    - Quality: drift vs training distribution; feedback labels when available.
    - Pipeline health: feature store freshness, batch job success.
    - Alert and auto-rollback when online metrics regress after deploy.
    
    **Trap**
    
    - Only watching GPU utilisation while the model’s business KPI collapses.

## Practice questions

**15. How do you implement distributed tracing in a microservices architecture?**

??? success "Reveal answer"
    **In short:** Propagate a trace context across services and export spans to a backend (Jaeger/Tempo/Zipkin/X-Ray).
    
    **Key points**
    
    - Instrument with OpenTelemetry SDKs at edges and clients.
    - Propagate W3C `traceparent` over HTTP/gRPC.
    - Sample thoughtfully; keep useful attributes (not PII).
    - Link traces to logs via trace ID for fast RCA.
    
    **Trap**
    
    - 100% tracing in prod without sampling — cost and noise explode.

**16. How do you set up alerts for monitoring systems?**

??? success "Reveal answer"
    **In short:** Define alert rules on SLOs/symptoms, route via Alertmanager (or cloud), and attach runbooks.
    
    **Key points**
    
    - PromQL/LogQL/metric alerts with severity labels.
    - Route paging vs tickets; inhibit dependent noise.
    - Multi-window burn-rate alerts beat naive thresholds.
    - Test alerts; document owners and silence policy.
    
    **Trap**
    
    - Email-only critical alerts that nobody reads at 03:00.

**17. How do you receive alerts in your project and how is it setup?**

??? success "Reveal answer"
    **In short:** Alerts fire from Prometheus/CloudWatch into Alertmanager/PagerDuty/Slack with on-call schedules.
    
    **Key points**
    
    - Rules live in Git with the stack (GitOps for alert config).
    - Alertmanager routes by severity/team to Slack + PagerDuty.
    - On-call rotations owned by the service team.
    - Every page should have a runbook URL annotation.
    
    **Trap**
    
    - A shared Slack `#alerts` firehose with no ownership.

**18. How do you handle disk, CPU alerts?**

??? success "Reveal answer"
    **In short:** Alert on sustained disk/CPU saturation with actionable thresholds and filesystem context.
    
    **Key points**
    
    - Disk: predict time-to-full; alert before 80–90% on critical mounts.
    - CPU: alert on saturation + latency impact, not brief spikes.
    - Include instance, mount, and top consumers in the message.
    - Auto-remediate safe cases (log cleanup) carefully.
    
    **Try this**
    
    - `node_filesystem_avail_bytes`
    - `rate(node_cpu_seconds_total{mode!='idle'}[5m])`
    
    **Trap**
    
    - Paging on 1-minute CPU blips during deploys.

**19. How do you setup Prometheus dashboard?**

??? success "Reveal answer"
    **In short:** Prometheus itself has an expression UI; rich dashboards usually live in Grafana fed by Prometheus.
    
    **Key points**
    
    - Ensure scrape targets are UP in Prometheus `/targets`.
    - Add Prometheus as a Grafana data source.
    - Import or build dashboards with PromQL panels.
    - Save dashboards as code (JSON/Helm) when possible.
    
    **Trap**
    
    - Editing only in the UI with no export — dashboards vanish on restart.

**20. How do you configure a Grafana dashboard?**

??? success "Reveal answer"
    **In short:** Create a Grafana dashboard with panels bound to a data source and useful variables.
    
    **Key points**
    
    - Add data source (Prometheus/Loki), then new dashboard panels.
    - Use variables for `job`, `namespace`, `pod`.
    - Layout: golden signals first, then dependencies.
    - Provision via ConfigMap/API for durability.
    
    **Try this**
    
    - Grafana Explore to craft queries before paneling
    
    **Trap**
    
    - 50-panel Christmas trees nobody can read during an incident.

**21. What proactive monitoring solutions have you implemented in your projects?**

??? success "Reveal answer"
    **In short:** Proactive means detecting burn before customers do — synthetics, SLO burn, and capacity forecasts.
    
    **Key points**
    
    - Blackbox/synthetic checks on critical user journeys.
    - Error-budget burn-rate alerts.
    - Capacity forecasts for disk/certificate/queue lag.
    - Chaos/game days to validate detection paths.
    
    **Trap**
    
    - Hundreds of low-value alerts pretending to be “proactive”.

**22. How do you perform infrastructure cost optimization using monitoring and observability tools?**

??? success "Reveal answer"
    **In short:** Use utilisation and idle metrics to right-size, schedule, and kill waste — FinOps with evidence.
    
    **Key points**
    
    - Find idle CPUs, unattached disks, zombie namespaces.
    - Rightsizing recommendations from actual p95 usage.
    - Schedule non-prod to sleep; spot/preemptible where safe.
    - Tag resources; allocate cost to owners via dashboards.
    
    **Trap**
    
    - Cutting CPU limits until throttling destroys latency SLOs.

**23. How do you configure Prometheus and Grafana for monitoring?**

??? success "Reveal answer"
    **In short:** Deploy Prometheus to scrape targets, Grafana to graph them, and wire a data source + dashboards.
    
    **Key points**
    
    - Install Prometheus (Helm/operator) with scrape configs/ServiceMonitors.
    - Install Grafana; add Prometheus URL as data source.
    - Import node/k8s dashboards; create app golden-signal boards.
    - Persist Grafana config; secure auth (SSO) and anonymous off.
    
    **Trap**
    
    - Exposing Grafana anonymously on the internet “for convenience”.

**24. How will you monitor the cluster through Prometheus?**

??? success "Reveal answer"
    **In short:** Scrape kube-state-metrics, node exporters, cAdvisor/kubelet, and app ServiceMonitors.
    
    **Key points**
    
    - Cluster metrics: API server, nodes, pods, deployments.
    - Use Prometheus Operator/ServiceMonitor CRDs in Kubernetes.
    - Alert on NotReady, CrashLoop, PVC pending, and control-plane health.
    - Grafana kube dashboards for day-2 views.
    
    **Try this**
    
    - `kubectl get servicemonitors -A`
    - Prometheus `/targets`
    
    **Trap**
    
    - Scraping every pod annotation without metric relabel limits — cardinality bomb.

**25. How will you create the Custom alerts, tell me the procedure?**

??? success "Reveal answer"
    **In short:** Write a PromQL (or cloud) rule with severity labels, route it, and test the page end-to-end.
    
    **Key points**
    
    - Define condition, `for` duration, and annotations (summary/runbook).
    - Commit rules to Git; deploy via your monitoring pipeline.
    - Configure Alertmanager receivers and inhibition.
    - Fire a synthetic breach in staging to prove delivery.
    
    **Trap**
    
    - Shipping alerts that have never been tested — silent pagers.

**26. Diff between monitoring and observality?**

??? success "Reveal answer"
    **In short:** Same distinction: monitoring checks known signals; observability explains novel failures.
    
    **Key points**
    
    - Monitoring: dashboards + alerts on expected failure modes.
    - Observability: explore metrics/logs/traces ad hoc with context.
    - SLOs connect both to user impact.
    - Instrument once (OTel) — query many ways.
    
    **Trap**
    
    - Buying three tools and still only alerting on CPU.

**27. What tools have you used for monitoring?**

??? success "Reveal answer"
    **In short:** Common set: Prometheus/Grafana, Alertmanager, ELK or Loki, and a tracing backend.
    
    **Key points**
    
    - Metrics: Prometheus, CloudWatch, Datadog, Azure Monitor.
    - Logs: ELK, Loki, Cloud Logging.
    - Traces: Jaeger, Tempo, X-Ray, Honeycomb.
    - Pick depth over tool count; standardise labels.
    
    **Trap**
    
    - Name-dropping ten products without saying what you measured.

**28. Your Prometheus alerts are firing constantly (alert fatigue). How do you fix it?**

??? success "Reveal answer"
    **In short:** Fix alert fatigue by alerting on symptoms/SLOs, tuning `for`, and deleting vanity alerts.
    
    **Key points**
    
    - Adopt multi-window burn-rate alerts for SLOs.
    - Increase `for` on flapping metrics; add inhibition.
    - Delete alerts with no owner or no action.
    - Track pages-per-week as a platform KPI.
    
    **Trap**
    
    - Silencing everything for a week and calling the problem solved.

**29. How do you silence an alert in Alertmanager?**

??? success "Reveal answer"
    **In short:** Silences in Alertmanager mute matching alerts for a bounded time with an author and comment.
    
    **Key points**
    
    - UI or API: matchers on labels (`alertname`, `severity`).
    - Always set an end time and reason.
    - Use during maintenance; prefer inhibit rules for dependencies.
    - Audit who silenced what.
    
    **Try this**
    
    - Alertmanager UI → Silences
    - `amtool silence add alertname=DiskFull`
    
    **Trap**
    
    - Open-ended silences that outlive the maintenance window.

**30. Create a script to monitor the disk usage of a server. If usage exceeds 80%, log the details to a file and send an alert email?**

??? success "Reveal answer"
    **In short:** A cron/script checks `df`, logs when over 80%, and emails — better as a real exporter alert long-term.
    
    **Key points**
    
    - Parse `df -P` for the mount; compare use% to threshold.
    - Append timestamp/host/mount to a log file.
    - Send mail via `mail`/`sendmail` or an API.
    - Prefer node_exporter + Alertmanager for production estates.
    
    **Try this**
    
    - `df -P / | awk 'NR==2 {print $5}'`
    - cron every 5 minutes
    
    **Trap**
    
    - Emailing every 5 minutes forever with no dedupe — another fatigue source.

**31. How do you use Python for log monitoring in DevOps?**

??? success "Reveal answer"
    **In short:** Python scripts (or agents) parse logs, detect patterns, and emit metrics/alerts to your stack.
    
    **Key points**
    
    - Tail structured logs; count errors; push to Prometheus Pushgateway or OTel.
    - Use for custom business-log monitors when exporters don’t exist.
    - Keep scripts idempotent and supervised by systemd.
    - Prefer platform agents for commodity log shipping.
    
    **Trap**
    
    - A laptop cron “monitor” that nobody owns when it dies.

**32. How can AI assist us in cloud infrastructure monitoring?**

??? success "Reveal answer"
    **In short:** AI helps correlate signals and summarise incidents — it does not replace SLOs and runbooks.
    
    **Key points**
    
    - Anomaly detection on metrics; log clustering for unknown errors.
    - Copilots summarise traces/logs during RCA.
    - Forecast capacity and cost anomalies.
    - Keep humans in the loop for prod actions.
    
    **Trap**
    
    - Auto-remediation from opaque models without audit or kill switch.

**33. How logs are segregated in ELK?**

??? success "Reveal answer"
    **In short:** ELK segregates logs with indices, data streams, pipelines, and field-level filters.
    
    **Key points**
    
    - Index-per-service or data streams with ILM policies.
    - Ingest pipelines enrich and drop sensitive fields.
    - RBAC in Kibana spaces limits who sees which indices.
    - Separate audit vs app logs for retention/compliance.
    
    **Trap**
    
    - One shared index for all tenants with no access controls.

**34. How does Prometheus collect metrics?**

??? success "Reveal answer"
    **In short:** Prometheus collects by scraping pull endpoints on an interval (plus limited push for batches).
    
    **Key points**
    
    - `scrape_configs` hit `/metrics` over HTTP/HTTPS.
    - Relabeling keeps cardinality sane.
    - Pushgateway for short-lived jobs only.
    - Federation/remote-write for multi- Prom setups.
    
    **Trap**
    
    - Scrape intervals of 1s on huge targets — self-inflicted DoS.

**35. What kind of observability tools have you used, and what metrics have you been monitoring?**

??? success "Reveal answer"
    **In short:** I’ve used Prometheus/Grafana/ELK (or cloud equivalents) for golden signals and dependency health.
    
    **Key points**
    
    - App: request rate, error rate, latency, saturation.
    - Infra: CPU, memory, disk, network, node readiness.
    - Platform: deploy failures, queue lag, certificate expiry.
    - Always tie metrics to user journeys and SLOs.
    
    **Trap**
    
    - Listing tools without naming the metrics that saved an incident.

**36. How to integrate grafana with prometheus?**

??? success "Reveal answer"
    **In short:** Add Prometheus as a Grafana data source (URL + auth), then build or import dashboards.
    
    **Key points**
    
    - Grafana → Connections → Prometheus → URL `http://prometheus:9090`.
    - Test query in Explore (`up`, `rate(http_requests_total[5m])`).
    - Import community dashboards or provision JSON.
    - Secure Grafana; use service accounts for API access.
    
    **Try this**
    
    - Explore → `up`
    - Import dashboard ID for Node Exporter
    
    **Trap**
    
    - Pointing Grafana at the wrong Prometheus and debugging empty graphs for hours.

## Related
- Hub: [Interview Preparation](index.md)
{% endraw %}
