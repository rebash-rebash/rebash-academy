---
title: "Monitoring & Observability Interview Preparation"
description: "40 curated interview questions and model answers for Monitoring & Observability — concepts, scenarios, troubleshooting, and production trade-offs."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is Prometheus, and how does it collect metrics?**

??? success "Reveal answer"
    Prometheus is an open-source time-series metrics collection and alerting system. It works on 
    a pull model — instead of applications pushing metrics to a central server, 
    Prometheus scrapes (polls) metrics endpoints at regular intervals. 
    The pull model explained: 
    [Application] exposes metrics at GET /metrics 
     ↑ 
    [Prometheus] scrapes /metrics every 15 seconds 
     ↓ 
    [Prometheus TSDB] stores time-series data 
     ↓ 
    [Grafana / AlertManager] reads and visualizes 
    What metrics look like at /metrics endpoint: 
    # HELP http_requests_total Total number of HTTP requests 
    # TYPE http_requests_total counter 
    http_requests_total{method="GET", endpoint="/api/users", status="200"} 15234 
    http_requests_total{method="GET", endpoint="/api/users", status="500"} 23 
    http_requests_total{method="POST", endpoint="/api/orders", status="201"} 4521 
    
     
    # HELP http_request_duration_seconds HTTP request duration in seconds 
    # TYPE http_request_duration_seconds histogram 
    http_request_duration_seconds_bucket{le="0.1"} 9800 
    http_request_duration_seconds_bucket{le="0.5"} 14900…

**2. Explain the ELK Stack architecture. What does each component do?**

??? success "Reveal answer"
    The ELK Stack components: 
    Application Logs 
     ↓ 
    [Filebeat / Fluentd] ← lightweight log shipper on each server/pod 
     ↓ 
    [Logstash] ← parse, transform, enrich logs (optional but 
    powerful) 
     ↓ 
    [Elasticsearch] ← store, index, and search logs at scale 
     ↓ 
    [Kibana] ← visualize, search, and create dashboards 
    Elasticsearch: A distributed search and analytics engine built on Apache Lucene. It stores data as 
    JSON documents and provides near-real-time full-text search. Key concepts: 
    • 
    Index — equivalent to a database table (e.g., logs-production-2026.03.24) 
    
     
    • 
    Document — a single log entry stored as JSON 
    • 
    Shard — an index is divided into shards, distributed across nodes for scalability 
    • 
    Replica — a copy of a shard for high availability 
    Logstash: A data processing pipeline. Takes data from various inputs (Beats, Kafka, syslog), 
    applies filters (grok parsing, timestamp extraction, geolocation lookup), and outputs to 
    Elasticsearch or elsewhere. 
    Kibana: The visualization layer. Provides Discover (search logs), Visualize (charts), Dashboard 
    (combine…

**3. Can you explain the ELK stack and how you've used it?**

??? success "Reveal answer"
    Elasticsearch stores and searches large volumes of log data, Logstash collects and processes logs from different
    sources before shipping them to Elasticsearch, and Kibana provides the visualization and search interface on top.
    I've used it to aggregate logs across microservices, filtering and formatting them in Logstash, then building Kibana
    dashboards to monitor error rates, latency, and overall service health.

**4. What is a ServiceMonitor?**

??? success "Reveal answer"
    A CRD used by the Prometheus Operator to define how to scrape a Service. Replaces manually 
    editing prometheus.yml. 
    apiVersion: monitoring.coreos.com/v1 
    kind: ServiceMonitor 
    spec: 
     selector: 
     matchLabels: 
     app: my-api 
     endpoints: 
    
     
     - port: metrics 
     interval: 30s

**5. What is Logstash Grok filter?**

??? success "Reveal answer"
    A pattern-matching filter that parses unstructured log lines into structured fields using 
    predefined or custom patterns. 
    
     
    grok { 
     match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} 
    %{GREEDYDATA:msg}" } 
    }

**6. What is the difference between Logstash and Fluentd?**

??? success "Reveal answer"
    Logstash: JVM-based, rich plugin ecosystem, higher resource usage. Fluentd: written in Ruby/C, 
    lower memory footprint, better for Kubernetes (Fluentbit is even lighter). Both support multiple 
    inputs, filters, and outputs.

**7. What is New Relic?**

??? success "Reveal answer"
    An observability platform offering APM, distributed tracing, infrastructure monitoring, and 
    synthetic monitoring as a SaaS solution. Strong .NET and Java monitoring capabilities. 
     
     
    
     
    ADDITIONAL TOOLS (20 Questions)

**8. What is Prometheus recording rules?**

??? success "Reveal answer"
    Pre-computes expensive PromQL expressions and saves results as new metrics. Speeds up 
    dashboard loading and reduces query load. 
    - record: job:http_requests:rate5m 
     expr: sum by (job) (rate(http_requests_total[5m]))

**9. What is predict_linear() in PromQL?**

??? success "Reveal answer"
    Predicts the future value of a metric using linear regression. 
    predict_linear(node_filesystem_free_bytes[6h], 24 * 3600) # Predict disk 
    space in 24 hours 
    Used in alerts: "disk will be full in less than 4 hours."

**10. What is synthetic monitoring?**

??? success "Reveal answer"
    Proactive monitoring using scripted user journeys to test application functionality from external 
    locations. Detects issues before real users encounter them. Tools: Grafana k6 Cloud, Pingdom, 
    Datadog Synthetics.

**11. Difference between for and while?**

??? success "Reveal answer"
    @ for & while
    ~ Best when the number of ¥ Runs until a condition becomes
    iterations is known false
    ¥ Ideal for monitoring or polling
    tasks
    @ Beginner @ Frequently Asked
    © ? How do you make a script executable?
    @

**12. What is Elasticsearch's _cat API?**

??? success "Reveal answer"
    A human-readable API for cluster monitoring. 
    curl "localhost:9200/_cat/indices?v" # List all indices 
    curl "localhost:9200/_cat/nodes?v" # Node status 
    curl "localhost:9200/_cat/health?v" # Cluster health

**13. What is Index Lifecycle Management (ILM) in Elasticsearch?**

??? success "Reveal answer"
    Automates the lifecycle of indices through phases: Hot (active writes), Warm (reduced resources), 
    Cold (infrequent access), Frozen (compressed, searchable), Delete. Saves significant storage costs.

**14. What is the Beats family of log shippers?**

??? success "Reveal answer"
    Lightweight data shippers: Filebeat (logs), Metricbeat (system metrics), Packetbeat (network data), 
    Auditbeat (audit data), Heartbeat (uptime monitoring). Written in Go, minimal resource footprint.

**15. What is log correlation in ELK?**

??? success "Reveal answer"
    Linking logs, metrics, and traces using a common trace ID. When a request generates an error, 
    you can jump from Kibana (logs) to Grafana (metrics) to Jaeger (traces) using the same 
    correlation ID.

**16. What are the three pillars of observability?**

??? success "Reveal answer"
    Metrics: numeric measurements over time (CPU, request rate, error rate). Logs: event records 
    with context (structured JSON logs). Traces: end-to-end journey of a request through multiple 
    services.

**17. What is the difference between monitoring and observability?**

??? success "Reveal answer"
    Monitoring tells you when something is wrong (dashboards, alerts). Observability tells you why — 
    by exploring metrics, logs, and traces together. Observability requires no pre-defined questions.

**18. What is the Prometheus Operator?**

??? success "Reveal answer"
    A Kubernetes operator that manages Prometheus instances using 
    CRDs: Prometheus, ServiceMonitor, PodMonitor, PrometheusRule, AlertmanagerConfig. 
    Installed via kube-prometheus-stack Helm chart.

**19. What is Grafana's $__interval variable?**

??? success "Reveal answer"
    A built-in variable that Grafana calculates based on the dashboard time range and panel width. 
    Used in rate() or increase() to automatically adjust the time window for the display resolution.

**20. What is Elasticsearch refresh_interval?**

??? success "Reveal answer"
    How often Elasticsearch refreshes the index to make new documents searchable. Default: 1 
    second. Setting it higher (e.g., 30s) during bulk indexing dramatically improves write throughput.

**21. What is OpenTelemetry?**

??? success "Reveal answer"
    A CNCF project providing a standardized API, SDK, and tooling for collecting metrics, logs, and 
    traces. Vendor-neutral — instrument once, send to any backend (Jaeger, Grafana, Datadog).

**22. What is a Kibana Space?**

??? success "Reveal answer"
    A tenant-like isolation unit in Kibana. Each Space has its own dashboards, visualizations, and 
    saved searches. Used to separate different teams or projects in a shared Kibana instance.

**23. What is Datadog?**

??? success "Reveal answer"
    A comprehensive SaaS monitoring platform covering infrastructure metrics, APM, logs, synthetics, 
    and security. All-in-one alternative to self-managed Prometheus + Grafana + ELK stacks.

**24. What is Thanos?**

??? success "Reveal answer"
    A highly available Prometheus setup with long-term storage. Adds global query view across 
    multiple Prometheus instances, unlimited retention via object storage (S3), and downsampling.

## Scenarios and troubleshooting

**25. How do you set up a production-grade Grafana dashboard?**

??? success "Reveal answer"
    A Grafana dashboard is only as useful as the questions it answers. Production dashboards should 
    give you the answer to "Is my service healthy right now?" within 5 seconds of opening it. 
    The RED method (the gold standard for service dashboards): 
    • 
    Rate — how many requests per second is the service handling? 
    • 
    Errors — what fraction of requests are failing? 
    • 
    Duration — how long are requests taking? 
    Dashboard as Code using Grafana's JSON model (provisioned via ConfigMap in 
    Kubernetes): 
    # grafana-dashboard-configmap.yaml 
    apiVersion: v1 
    kind: ConfigMap 
    
     
    metadata: 
     name: api-dashboard 
     namespace: monitoring 
     labels: 
     grafana_dashboard: "1" # Grafana sidecar picks this up automatically 
    data: 
     api-dashboard.json: | 
     { 
     "title": "API Service - RED Dashboard", 
     "uid": "api-service-red", 
     "panels": [ 
     { 
     "title": "Request Rate (req/s)", 
     "type": "stat", 
     "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4}, 
     "targets": [{ 
     "expr": "sum(rate(http_requests_total{job='api'}[5m]))", 
     "legendFormat": "Requests/s" 
     }], 
     "fieldConfig": { 
     "defaults": {…

**26. Production is down. The error rate just jumped to 40%. Walk me through your incident response. Answer: This question tests your incident response instincts. The interviewer wants to see systematic thinking, not panic. The OODA loop for incidents: Observe → Orient → Decide → Act Minute 0-2: TRIAGE ├── Check monitoring dashboard (Grafana) — what metrics changed?**

??? success "Reveal answer"
    │ ├── Error rate jumped at 14:32 UTC 
    │ ├── CPU looks normal on app servers 
    │ └── Database connection errors spiking 
    ├── Check recent deployments — was anything deployed in the last 30 minutes? 
    │ └── kubectl rollout history deployment/my-api -n production 
    └── Declare incident severity level → notify on-call team via PagerDuty 
    Minute 2-5: IMMEDIATE MITIGATION 
    ├── If recent deployment → ROLLBACK IMMEDIATELY, ask questions later 
    │ └── kubectl rollout undo deployment/my-api -n production 
    ├── If no recent deployment → investigate further 
    └── Scale up pods to handle potential load issue 
     └── kubectl scale deployment/my-api --replicas=10 -n production 
    Minute 5-15: INVESTIGATION (if not resolved by rollback) 
    ├── Check application logs in Kibana 
    │ └── Filter: kubernetes.namespace: production AND app.level: ERROR AND 
    @timestamp > now-15m 
    
     
    ├── Check database metrics 
    │ ├── RDS CloudWatch: DatabaseConnections, ReadLatency, WriteLatency 
    │ └── Look for connection pool exhaustion 
    ├── Check downstream dependencies 
    │ └── Are third-party API calls failing?…

**27. How do you prevent similar incidents from happening again?**

??? success "Reveal answer"
    ° Improve monitoring & alerting. * Proactive approach
    + Add automated checks and health validations. * Reliability mindset
    + Implement better testing (staging, load, integration). * Architecture improvement
    + Review architecture and remove single points of failure. * Learning feorm incidents
    + Run regular chaos tests and DR drills. * Long-term thinking
    5°) KEY TAKEAWAY: Incidents are not failures, poor response is.
    | Respond fast, communicate well, learn always, and build for resilience. VERIQTA | © @verigta_
    
    cee VERIQTA
    (Q) Instagram: @verigta_
    2 = iy
    vn > DEPLOYMENT & CI/CD FAILURES :
    “Zatiks SLY TOPICS COVERED: «© ak |
    |v Failed deployments v Rollbacks v Pipeline failures Vv Release strategies |
    ® Q:A deployment was triggered and marked successful, but users are facing errors.
    How do you investigate and fix it?
    ANS: + Check application logs, metrics, and error rates. 
    + Compare the new release with the previous stable version. * Structured troubleshooting
    + Validate configs, environment variables, secrets, feature flags. * Fast but safe decision making
    +…

**28. How do you recover a failed service in production?**

??? success "Reveal answer"
    * Understand the failure scope and impact. * Quick recovery mindset
    | + Apply the quickest safe mitigation (restart, rollback, failover, scale). + Risk assessment
    + Scale resources if needed (CPU, memory, connections). * Monitoring after recovery
    + Validate service health with metrics and smoke tests. * Ensuring full restoration
    | + Monitor closely after recovery to ensure stability. * Stability focus
    GB)

**29. Your production application is completely down. | Users cannot access the service. What do you do first?**

??? success "Reveal answer"
    * Check monitoring & alerts (Grafana,CloudWatch,Datadog). * Calm and structured approach
    * Confirm the impact and scope (is it one service or entire system?). + Impact assessment first
    | * Check status of upstream dependencies (DB, Redis, third-party APIs, DNS). * Good use of monitoring tools
    | + Verify recent changes (deployments, config changes, infra changes). * Prioritization & communication
    | + Start incident timeline and notify the on-call / incident channel. * Incident ownership mindset
    | @

**30. How would you handle logging in Linux?**

??? success "Reveal answer"
    System logs live in /var/log/, managed with rsyslog or syslog for centralized logging, journalctl for viewing and filtering
    logs on systemd-based systems, logrotate for rotating and compressing large log files, and integration with a stack
    like ELK or Grafana Loki for real-time log visualization and analysis at scale.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

## Practice questions

**31. How do you write PromQL queries for practical alerting scenarios?**

??? success "Reveal answer"
    PromQL (Prometheus Query Language) is a functional query language for time-series data. 
    Writing effective PromQL is a core skill — it powers both Grafana dashboards and Alertmanager 
    rules. 
    The four key PromQL operations: 
    1. Instant vector selectors: 
    
     
    # Current value of a metric with label filter 
    http_requests_total{job="api-server", status="500"} 
    # All HTTP 5xx errors across all jobs 
    http_requests_total{status=~"5.."} # =~ means regex match 
    2. Range vector + rate() — the most used pattern: 
    # Request rate over the last 5 minutes (requests per second) 
    rate(http_requests_total[5m]) 
    # Error rate per second for the API 
    rate(http_requests_total{job="api", status=~"5.."}[5m]) 
    3. Aggregation: 
    # Total request rate across all instances 
    sum(rate(http_requests_total[5m])) 
    # Request rate per endpoint 
    sum by (endpoint) (rate(http_requests_total[5m])) 
    # P99 latency across all pods 
    histogram_quantile(0.99, sum by (le) 
    (rate(http_request_duration_seconds_bucket[5m]))) 
    4. Arithmetic and comparison: 
    # Error ratio (errors / total requests)…

**32. How do you implement distributed tracing in a microservices architecture?**

??? success "Reveal answer"
    Answer: 
    In a microservices system, a single user request might pass through 10 different services. When 
    something is slow or failing, distributed tracing tells you exactly which service, which function, 
    and which database query is the culprit. Without it, debugging is like trying to find a needle in 10 
    haystacks simultaneously. 
    The OpenTelemetry standard (the modern approach): 
    OpenTelemetry (OTel) is the industry-standard for collecting traces, metrics, and logs. You 
    instrument your application once, and can send data to Jaeger, Zipkin, Tempo, Datadog, or any 
    compatible backend. 
    Instrumenting a Node.js application: 
    // tracing.js — must be loaded before anything else 
    const { NodeSDK } = require('@opentelemetry/sdk-node'); 
    const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-
    instrumentations-node'); 
    const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-
    http'); 
    const { Resource } = require('@opentelemetry/resources'); 
    const { SemanticResourceAttributes } = require('@opentelemetry/semantic-
    conventions'); 
    const…

**33. You have high error rates but logs show nothing useful. a = : Fis _—?**

??? success "Reveal answer"
    + Improve logging: add structured logs with correlation/nequest IDs. # Logging best practices knowledge | o Structured h
    - + Increase log level temporarily (with. caution). Structured logging awareness lisp Coadiectiedl
    a. + Check centralized lage (ELK/Leki/Clnudbatch/Datades) # Correlation & traceability Ny /emaiises |
    + Search by trace ID, user ID, or timestamp. * Systematic troubleshooting ier
    + Add contextual fields: service, env, version, endpoint, latency. * Balance between signal & noise \
    - + Reproduce in lower env and compare lags. :
    OG: thaiss prea tare tery wore ener re? 
    9 ANS: - Get the trace ID from logs / error response / APM. # Understanding of distributed tracing — °V- 120ms 80ms 450ne
    + Open trace in tool (Jaeger, Zipkin, Datadog, AWS X-Ray). * Ability to read traces A-a-oea-§
    a pare latency. Se, : Ld
    -~@ + Check span details: DB calls, external APIs, queues. ty We —,
    + Validate with logs & metrics to coffirm the bottleneck.
    logs 3
    -—3 @

**34. An alert fired at 3AM. What do you check first?**

??? success "Reveal answer"
    + Check clert details: metric, threshold, duration. # Mert triage process |B) Summary
    ~® + Check dashboard linked to the alert. 6 fisdbince aback tat [4] Dashboard
    + Validate if it's a real issue or a false positive. 3 ee | FE Recent
    + Check recent deployments / changes. aie ars aragaa | s
    =) + Check related clerts (eorrelation): * Communication mindset | LR Related Alerts
    ad as woe SE rc nce a forall! INTERVIEWER LOOKS. FOR: © GOOD ALERT Is:
    -2 py togharron rth yi. Ale a p iarlgs i,
    Beet ead ote, acl + RAURD soemon | Baler
    -® + Avoid noisy clerts: use rate of change, anomaly detection. =. Aeteciog) aioe hee)
    + Add runbook links and clear descriptions. * Clear ownership & runbooks | Y Oued
    9 + Review & tune alerts regularly. * Continuous improvement. (7 Documented
    @©a oe a fet ort ereviite pereiee INTERVIEWER LOOKS. FOR: i LOG MANAGEMENT FLOW
    “8 ANS: im Car iA * Cost awareness
    ! + Implement log retention & Lifeeycle policies. ae
    CA tat oabtouln clr oes * Logging strategy 1-y-B-
    - + Filter & drop unnecessary logs ot source. # Retention & governance App Collector |…

**35. How do you optimize a system for better performance?**

??? success "Reveal answer"
    + Optimize code and algorithms. * Optimisation techniques
    + Add caching (Redis, CDN, in-memory). * Trade-off understanding . ;
    
    - + Optimize database (indexes, query tuning). si Caching'® angus patterns se =] 4 a &3
    - + Scale horizontally and use load balancers. * Continuous monitoring ‘ 4
    a = | f " PERFORMANCE ENGINEERING MINDSET i VERIQTA
    | -—G)> Performance is not a one-time task. i] | «all Q & rail ran ——
    
    -9 | It's @ continuous cycle of: Measure > | i ‘ Ss Bree ae Gi ;
    
    : ;
    — VERIQTA See re eae we
    = , | lustagrant Querata { TOPICS COVERED: |
    . Z
    es = v Alerts
    -e | 14) - MONITORING & INCIDENT MANAGEMENT - a
    Pil oz} % Sv Oneal scenarios
    1) Ne ,
    Da tae de ue design ftv, ales? INTERVIEWER LOOKS. FOR: ( GQ0D_ALERT DESIGN EXAMPLE }
    | ANS: . Alert on symptoms (user impact), not on infrastructure. Alerting best practices
    2 . ss -e db
    nl | + Use multiple conditions / multi-window alerts. # Understanding of impact | Triggae Threshold Oumar Rabo Nay
    + Add context: runbook link, dashboard, owner. # Clarity and ownership a sa = rae
    sl + Review and tune alerts regularly.…

**36. How do you set up alerts for monitoring systems?**

??? success "Reveal answer"
    Prometheus rules define thresholds -- CPU usage above 80%, for example -- routed through Alertmanager to the
    right channel. I set threshold-based alerts for response time and error rate, custom application-specific alerts for
    things like failed transactions, Kubernetes readiness/liveness probes to catch unhealthy services, and Grafana's own
    alerting for anything visualized there.

**37. What tools have you used for monitoring?**

??? success "Reveal answer"
    Prometheus for time-series metric collection and PromQL querying, Grafana for visualizing those metrics through
    dashboards, Alertmanager paired with Prometheus for routing alerts to Slack or email, the ELK stack for log
    aggregation and analysis, and the Prometheus Operator specifically for Kubernetes cluster monitoring.

**38. Your Prometheus alerts are firing constantly (alert fatigue). How do you fix it?**

??? success "Reveal answer"
    1. Audit alerts — remove ones nobody acts on. 2) Increase for: duration on flapping alerts. 
    3) Add inhibition rules. 4) Group related alerts. 5) Route low-severity to Slack, critical to 
    PagerDuty. 6) Add runbook links to every alert. Goal: every alert should be actionable and 
    have a documented response.

**39. How do you silence an alert in Alertmanager?**

??? success "Reveal answer"
    Create a Silence with matchers for the alert labels. The silence inhibits notifications for a defined 
    time period — useful during planned maintenance. 
    amtool silence add alertname="HighCPU" instance="web-01" --duration=2h --
    comment="Planned maintenance"

**40. How do you use Python for log monitoring in DevOps?**

??? success "Reveal answer"
    Reading and filtering log files directly in Python, or integrating with a stack like ELK for larger scale, lets me search
    for patterns like "ERROR" and trigger alerts through Slack or email notifications when specific patterns show up.

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
