---
title: Monitoring and Logging in Kubernetes
description: Observe Kubernetes clusters with Prometheus, Grafana, and Alertmanager — collect pod logs with Loki or EFK, and define SLO-driven alerts.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
category: kubernetes
tags:
  - kubernetes
  - monitoring
  - logging
  - prometheus
  - grafana
prerequisites:
  - Production Patterns — HPA, PDB, and Affinity
  - Health Checks, Probes, and Self-Healing
  - Troubleshooting Kubernetes Workloads
comments: false
---

# Monitoring and Logging in Kubernetes

## Overview

You cannot operate what you cannot see. Production Kubernetes requires **metrics** (is the cluster healthy?), **logs** (what happened when the pod crashed?), and **traces** (where did this request spend 2 seconds?). The CNCF stack — **Prometheus**, **Grafana**, **Alertmanager**, and **Loki** — is the de facto observability foundation, often deployed via **kube-prometheus-stack** Helm chart.

This tutorial covers the observability pillars for Kubernetes, ServiceMonitor patterns, log aggregation, golden signals, and alert design that pages humans only when action is required.

This is **Tutorial 18** in **Module 6: Production** of the REBASH Academy Kubernetes series.

## Prerequisites

- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md)
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)
- [Helm Package Management](helm-package-management.md)
- [Services and Cluster Networking](services-and-cluster-networking.md)
- Cluster with Helm 3 and sufficient resources (~4 GB RAM for monitoring stack)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the three pillars of observability in a Kubernetes context
- [ ] Deploy kube-prometheus-stack and access Grafana dashboards
- [ ] Configure ServiceMonitors to scrape application metrics
- [ ] Aggregate container logs with Loki or the EFK pattern
- [ ] Define alerts on golden signals — latency, traffic, errors, saturation
- [ ] Correate metrics, logs, and Kubernetes events during incident response

## Architecture Diagram

```d2
direction: down

Apps: "Application namespace" {
      style: {
        fill: "#e3f2fd"
        stroke: "#1976d2"
      }
        API: votestack-api
        WEB: votestack-web
        PROM: PROM
        API -> PROM: "/metrics"
    }
    Observability: "monitoring namespace" {
      style: {
        fill: "#e8f5e9"
        stroke: "#388e3c"
      }
        AM: Alertmanager
        GRAF: Grafana
        LOKI: Loki
        PROM -> AM
        PROM -> GRAF
        LOKI -> GRAF
    }
    Collection: Collection {
        SM: ServiceMonitor
        FB: "Fluent Bit / Promtail"
    }
    Collection.SM -> Apps.PROM
    Apps.API -> Collection.FB
    Collection.FB -> Observability.LOKI
    ONCALL: "On-call engineer"
    Observability.AM -> ONCALL: "PagerDuty / Slack"
```

## Theory

### Three pillars of observability

| Pillar | Question | Kubernetes tools |
|--------|----------|------------------|
| **Metrics** | How much, how fast? | Prometheus, kube-state-metrics, cAdvisor |
| **Logs** | What exactly happened? | Loki, Elasticsearch, CloudWatch |
| **Traces** | Where did time go? | Jaeger, Tempo, OpenTelemetry |

Metrics are cheap at scale and drive alerts. Logs provide forensic detail. Traces connect microservice hops — essential for VoteStack's api → redis → worker → postgres flow.

### Golden signals (Google SRE)

| Signal | Kubernetes manifestation |
|--------|--------------------------|
| **Latency** | Histogram `http_request_duration_seconds` |
| **Traffic** | Counter `http_requests_total` |
| **Errors** | 5xx rate, `kube_pod_container_status_restarts_total` |
| **Saturation** | CPU/memory vs requests, node disk pressure |

Add **Availability** (uptime) and **Cost** (resource usage) for platform dashboards.

### Prometheus scraping model

Prometheus **pulls** metrics from targets on an interval. In Kubernetes:

1. Pods expose `/metrics` on a named port
2. **ServiceMonitor** CRD tells Prometheus Operator which services to scrape
3. **PodMonitor** scrapes pods directly (sidecar or hostNetwork patterns)

Key metric types:

| Type | Example | Use |
|------|---------|-----|
| Counter | `http_requests_total` | Rate of change |
| Gauge | `memory_usage_bytes` | Current value |
| Histogram | `request_duration_seconds` | Percentiles (p50, p99) |
| Summary | Pre-computed quantiles | Legacy — prefer histogram |

### Logging architecture

Containers log to **stdout/stderr** — Kubernetes captures via kubelet. Collection agents run as DaemonSet:

| Stack | Components |
|-------|------------|
| **PLG** | Promtail → Loki → Grafana |
| **EFK** | Fluent Bit → Elasticsearch → Kibana |
| **Managed** | CloudWatch, GCP Logging, Azure Monitor |

Structured JSON logs (`{"level":"error","msg":"..."}`) enable label-based filtering in Loki.

### Alerting philosophy

**Alert on symptoms, not causes.** Page when users are impacted:

- ✅ Error rate > 1% for 5 minutes
- ✅ API p99 latency > 2s
- ❌ Single pod restart (use ticket, not page)
- ❌ Node NotReady for 30s (may self-heal)

Use Alertmanager for routing, inhibition, and silencing during maintenance.

## Hands-on Lab

### Lab 1 — Install kube-prometheus-stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

kubectl create namespace monitoring

helm install kube-prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --set grafana.adminPassword=changeme \
  --set prometheus.prometheusSpec.retention=15d \
  --wait

kubectl get pods -n monitoring
kubectl port-forward svc/kube-prometheus-grafana -n monitoring 3000:80
# Browser: http://localhost:3000 — admin / changeme
```

Explore built-in dashboards: **Kubernetes / Compute Resources / Namespace**, **Node Exporter**.

### Lab 2 — Instrument VoteStack api

Add Prometheus client to the api (Node.js example):

```javascript
const client = require('prom-client');
const register = new client.Registry();
client.collectDefaultMetrics({ register });

const httpRequests = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register],
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

Rebuild and deploy via GitOps. Verify:

```bash
kubectl port-forward svc/votestack-api -n votestack 8080:8080
curl -s localhost:8080/metrics | head -20
```

### Lab 3 — ServiceMonitor for api

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: votestack-api
  namespace: votestack
  labels:
    release: kube-prometheus   # must match Prometheus release label
spec:
  selector:
    matchLabels:
      app: votestack-api
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
```

Ensure the Service exposes port name `http`:

```yaml
ports:
  - name: http
    port: 8080
    targetPort: 8080
```

Apply and confirm target in Prometheus UI → Status → Targets.

### Lab 4 — Grafana dashboard panel

In Grafana, add panel:

- Query: `rate(http_requests_total{namespace="votestack"}[5m])`
- Legend: `{{method}} {{route}}`
- Add second panel: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`

Save dashboard to ConfigMap for GitOps:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: votestack-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  votestack.json: |
    { "... dashboard JSON ..." }
```

### Lab 5 — Deploy Loki for log aggregation

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki-stack -n monitoring \
  --set promtail.enabled=true \
  --set loki.persistence.enabled=true \
  --wait
```

Query logs in Grafana → Explore → Loki:

```logql
{namespace="votestack", app="votestack-api"} |= "error"
{namespace="votestack"} | json | level="error"
```

Correlate with metrics: click timestamp → view pod logs for same interval.

### Lab 6 — Alert rules

`PrometheusRule` for high error rate:

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: votestack-alerts
  namespace: monitoring
  labels:
    release: kube-prometheus
spec:
  groups:
    - name: votestack
      rules:
        - alert: VoteStackApiHighErrorRate
          expr: |
            sum(rate(http_requests_total{namespace="votestack",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{namespace="votestack"}[5m]))
            > 0.01
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "VoteStack API error rate above 1%"
            runbook: "https://wiki.internal/runbooks/votestack-api-errors"
        - alert: VoteStackApiHighLatency
          expr: |
            histogram_quantile(0.99,
              sum(rate(http_request_duration_seconds_bucket{namespace="votestack"}[5m])) by (le)
            ) > 2
          for: 10m
          labels:
            severity: warning
```

Configure Alertmanager receiver (Slack webhook in Helm values):

```yaml
alertmanager:
  config:
    receivers:
      - name: slack
        slack_configs:
          - channel: '#alerts'
            api_url: <webhook-url>
    route:
      receiver: slack
      routes:
        - match:
            severity: critical
          receiver: slack
```

Test: `kubectl exec -n monitoring alertmanager-kube-prometheus-alertmanager-0 -- amtool alert add`

## Commands & Code

```bash
# Quick health checks
kubectl top nodes
kubectl top pods -A --sort-by=memory
kubectl get --raw /metrics | head

# Prometheus port-forward
kubectl port-forward svc/kube-prometheus-prometheus -n monitoring 9090:9090

# Recent events (correlate with metrics spikes)
kubectl get events -A --sort-by='.lastTimestamp' | tail -20

# Pod logs
kubectl logs -n votestack deploy/votestack-api --tail=100 -f
kubectl logs -n votestack <pod> --previous   # crashed container

# LogQL examples
# {namespace="votestack"} |= "panic"
# rate({namespace="votestack"}[1m])
```

| Tool | Purpose |
|------|---------|
| `kubectl top` | Snapshot CPU/memory (needs metrics-server) |
| Prometheus | Time-series metrics and alerting |
| Grafana | Dashboards and Explore |
| Loki/LogQL | Log query language |
| kube-state-metrics | Kubernetes object state metrics |

## Common Mistakes

!!! warning "Scraping without resource limits on Prometheus"
    Unbounded cardinality (high-cardinality labels like `user_id`) crashes Prometheus — cap label dimensions.

!!! warning "Alerting on every pod restart"
    Restart loops need investigation but single restarts during deploys are normal — use `for:` duration and rate thresholds.

!!! warning "No log retention policy"
    Loki/Elasticsearch disks fill — set retention (15–30 days typical) and sample debug logs in prod.

!!! warning "Missing ServiceMonitor label selector"
    Prometheus Operator only discovers ServiceMonitors matching its `serviceMonitorSelector` — verify label `release: kube-prometheus`.

!!! warning "Metrics on the main app port without auth"
    `/metrics` may expose internal stats — restrict via NetworkPolicy or separate metrics port.

## Best Practices

!!! tip "RED method for services"
    Rate, Errors, Duration — three charts per microservice covers 80% of service health.

!!! tip "USE method for resources"
    Utilization, Saturation, Errors — for nodes and databases.

!!! tip "Structured logging from day one"
    JSON with `trace_id`, `level`, `msg` — enables Loki parsing and cross-service correlation.

!!! tip "Runbooks linked in alert annotations"
    Every page includes `runbook_url` — on-call should never guess first steps.

!!! tip "Separate monitoring cluster for large estates"
    At scale, federate Prometheus or use centralized observability SaaS to isolate blast radius.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Target down in Prometheus | Wrong port name or NetworkPolicy | Match Service port name in ServiceMonitor |
| Grafana no data | Datasource not configured | Add Prometheus/Loki datasources in Helm values |
| High cardinality warning | Unbounded label values | Remove high-cardinality labels from metrics |
| Logs missing in Loki | Promtail not on node | Check DaemonSet; verify pod labels |
| Alerts not firing | Rule syntax or `for` window | Test expr in Prometheus UI → Alerts |
| OOM on Prometheus pod | Too much retention/cardinality | Reduce retention; drop expensive metrics |

## Summary

- **Metrics, logs, and traces** form the observability pillars — Prometheus and Loki are the common Kubernetes stack
- **Golden signals** (latency, traffic, errors, saturation) drive meaningful alerts and dashboards
- **ServiceMonitors** declaratively configure Prometheus scraping for application `/metrics` endpoints
- **Log aggregation** via Promtail/Loki or Fluent Bit/EFK centralizes stdout logs from all pods
- **Alert on symptoms** with runbook links — reduce noise with `for` durations and severity routing
- Next: [Kubernetes Security Hardening](kubernetes-security-hardening.md)

## Interview Questions

1. What are the three pillars of observability?
2. Explain the golden signals and give a Kubernetes example for each.
3. How does Prometheus discover scrape targets in Kubernetes?
4. What is a ServiceMonitor and why use it over static config?
5. Why should applications log to stdout instead of files?
6. How do you avoid alert fatigue in Kubernetes operations?
7. What is metric cardinality and why is it dangerous?
8. Compare PLG stack vs EFK stack for logging.
9. How would you debug a latency spike using metrics and logs together?
10. What is the difference between metrics-server and Prometheus?

??? tip "Sample Answers (Questions 3, 6, and 10)"

    **Q3 — Prometheus discovery:** Prometheus Operator watches ServiceMonitor and PodMonitor CRDs. Each defines label selectors matching Services or Pods, plus scrape endpoints (port, path, interval). Prometheus config is generated dynamically — no manual target list when pods scale.

    **Q6 — Alert fatigue:** Alert only on user-visible symptoms (error rate, SLO breach). Use `for:` windows to ignore transient blips. Route warnings to Slack, criticals to pager. Add inhibition rules (suppress node alerts when cluster is down). Review and delete unused alerts quarterly. Every alert needs a runbook.

    **Q10 — metrics-server vs Prometheus:** metrics-server provides short-term CPU/memory summaries for `kubectl top` and HPA — lightweight, in kube-system. Prometheus is a full time-series database with long retention, alerting, and custom application metrics — deployed separately. They serve different purposes.

## Related Tutorials

- [Production Patterns — HPA, PDB, and Affinity](production-patterns-hpa-pdb-and-affinity.md) *(previous)*
- [Kubernetes Security Hardening](kubernetes-security-hardening.md) *(next)*
- [Troubleshooting Kubernetes Workloads](troubleshooting-kubernetes-workloads.md)
- [Container Logging and Monitoring](../docker/container-logging-and-monitoring.md)
- [Health Checks, Probes, and Self-Healing](health-checks-probes-and-self-healing.md)
- [Kubernetes – Category Overview](index.md)

## References

- [Prometheus – Documentation](https://prometheus.io/docs/)
- [Grafana – Loki](https://grafana.com/docs/loki/latest/)
- [kube-prometheus-stack Helm chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack)
- [Google SRE – Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [OpenTelemetry – Kubernetes](https://opentelemetry.io/docs/platforms/kubernetes/)
- [CNCF Observability Landscape](https://landscape.cncf.io/)
