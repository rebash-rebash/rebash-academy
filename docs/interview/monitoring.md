---
title: "Monitoring & Observability Interview Preparation"
description: "40 curated Monitoring & Observability interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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

**2. Can you explain the ELK stack and how you've used it?**

??? success "Reveal answer"
    Elasticsearch stores and searches large volumes of log data, Logstash collects and processes logs from different
    sources before shipping them to Elasticsearch, and Kibana provides the visualization and search interface on top.
    I've used it to aggregate logs across microservices, filtering and formatting them in Logstash, then building Kibana
    dashboards to monitor error rates, latency, and overall service health.

**3. What are the observibility needed for app?**

??? success "Reveal answer"
    Monitoring, Alerting, Logging, Remediation, PD,.
    
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**4. what is nagios , how to integerate jenknins in nagios?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**5. What is Prometheus, Grafana, Loki?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**6. What are data sources for Grafana, Kibana?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**7. What are indices, index in Kibana?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**8. What are the alerts you setup on graffana?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**9. Difference between observality and monitoring?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**10. What is Logstash Grok filter?**

??? success "Reveal answer"
    A pattern-matching filter that parses unstructured log lines into structured fields using 
    predefined or custom patterns. 
    
     
    grok { 
     match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} 
    %{GREEDYDATA:msg}" } 
    }

**11. What is the difference between Logstash and Fluentd?**

??? success "Reveal answer"
    Logstash: JVM-based, rich plugin ecosystem, higher resource usage. Fluentd: written in Ruby/C, 
    lower memory footprint, better for Kubernetes (Fluentbit is even lighter). Both support multiple 
    inputs, filters, and outputs.

## Scenarios and troubleshooting

**12. Production is down. The error rate just jumped to 40%. Walk me through your incident response. Answer: This question tests your incident response instincts. The interviewer wants to see systematic thinking, not panic. The OODA loop for incidents: Observe → Orient → Decide → Act Minute 0-2: TRIAGE ├── Check monitoring dashboard (Grafana) — what metrics changed?**

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

**13. How do you recover a failed service in production?**

??? success "Reveal answer"
    * Understand the failure scope and impact. * Quick recovery mindset
    | + Apply the quickest safe mitigation (restart, rollback, failover, scale). + Risk assessment
    + Scale resources if needed (CPU, memory, connections). * Monitoring after recovery
    + Validate service health with metrics and smoke tests. * Ensuring full restoration
    | + Monitor closely after recovery to ensure stability. * Stability focus
    GB)

**14. Your production application is completely down. | Users cannot access the service. What do you do first?**

??? success "Reveal answer"
    * Check monitoring & alerts (Grafana,CloudWatch,Datadog). * Calm and structured approach
    * Confirm the impact and scope (is it one service or entire system?). + Impact assessment first
    | * Check status of upstream dependencies (DB, Redis, third-party APIs, DNS). * Good use of monitoring tools
    | + Verify recent changes (deployments, config changes, infra changes). * Prioritization & communication
    | + Start incident timeline and notify the on-call / incident channel. * Incident ownership mindset
    | @

**15. How would you handle logging in Linux?**

??? success "Reveal answer"
    System logs live in /var/log/, managed with rsyslog or syslog for centralized logging, journalctl for viewing and filtering
    logs on systemd-based systems, logrotate for rotating and compressing large log files, and integration with a stack
    like ELK or Grafana Loki for real-time log visualization and analysis at scale.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**16. how the alert is created with which metrics when cpu and memory goes high in vm, what is action group, how do you create an alert explain step by step etc, some basic troubleshooting kql queries in log analytics workspace - check on those things, any automation done with scripting etc for monitoring?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Monitoring, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**17. How do you set up monitoring and observability for ML models in production?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**18. Question : What is your experience with alerts, logging, and incident/problem resolution?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Practice questions

**19. How do you implement distributed tracing in a microservices architecture?**

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

**20. How do you set up alerts for monitoring systems?**

??? success "Reveal answer"
    Prometheus rules define thresholds -- CPU usage above 80%, for example -- routed through Alertmanager to the
    right channel. I set threshold-based alerts for response time and error rate, custom application-specific alerts for
    things like failed transactions, Kubernetes readiness/liveness probes to catch unhealthy services, and Grafana's own
    alerting for anything visualized there.

**21. How do you receive alerts in your project and how is it setup?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**22. How do you handle disk, CPU alerts?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**23. How do you setup Prometheus dashboard?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**24. How do you configure a Grafana dashboard?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**25. What proactive monitoring solutions have you implemented in your projects?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**26. How do you perform infrastructure cost optimization using monitoring and observability tools?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**27. How do you configure Prometheus and Grafana for monitoring?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**28. How will you monitor the cluster through Prometheus?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**29. How will you create the Custom alerts, tell me the procedure?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Monitoring components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. diff between monitoring and observality?**

??? success "Reveal answer"
    Start with a precise definition in the context of Monitoring, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**31. What tools have you used for monitoring?**

??? success "Reveal answer"
    Prometheus for time-series metric collection and PromQL querying, Grafana for visualizing those metrics through
    dashboards, Alertmanager paired with Prometheus for routing alerts to Slack or email, the ELK stack for log
    aggregation and analysis, and the Prometheus Operator specifically for Kubernetes cluster monitoring.

**32. Your Prometheus alerts are firing constantly (alert fatigue). How do you fix it?**

??? success "Reveal answer"
    1. Audit alerts — remove ones nobody acts on. 2) Increase for: duration on flapping alerts. 
    3) Add inhibition rules. 4) Group related alerts. 5) Route low-severity to Slack, critical to 
    PagerDuty. 6) Add runbook links to every alert. Goal: every alert should be actionable and 
    have a documented response.

**33. How do you silence an alert in Alertmanager?**

??? success "Reveal answer"
    Create a Silence with matchers for the alert labels. The silence inhibits notifications for a defined 
    time period — useful during planned maintenance. 
    amtool silence add alertname="HighCPU" instance="web-01" --duration=2h --
    comment="Planned maintenance"

**34. Create a script to monitor the disk usage of a server. If usage exceeds 80%, log the details to a file and send an alert email?**

??? success "Reveal answer"
    Outline the solution first, then give a minimal correct example (commands or config sketch).
    
    Call out the production hardening you would add next (pin versions, least privilege, secrets, health checks) and how you would validate the result.

**35. How do you use Python for log monitoring in DevOps?**

??? success "Reveal answer"
    Reading and filtering log files directly in Python, or integrating with a stack like ELK for larger scale, lets me search
    for patterns like "ERROR" and trigger alerts through Slack or email notifications when specific patterns show up.

**36. How can AI assist us in cloud infrastructure monitoring?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**37. How logs are segregated in ELK?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**38. How does Prometheus collect metrics?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**39. What kind of observability tools have you used, and what metrics have you been monitoring?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

**40. How to integrate grafana with prometheus?**

??? success "Reveal answer"
    Answer directly for Monitoring: definition or decision first, then a short example.
    
    Mention one trade-off or failure mode, and end with the verification step an interviewer expects (command, metric, or review checklist).

## Related

- Hub: [Interview Preparation](index.md)
{% endraw %}
