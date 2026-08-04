---
title: Overview
description: "Google Cloud for Cloud & DevOps Engineers — 16 interview-depth modules from global infrastructure through IAM, VPC, compute, GKE, Cloud Run, IaC, cost, and production landing zones."
difficulty: beginner
estimated_time: "12–16 weeks"
technology_id: gcp
author: Shaik Basha
last_updated: "2026-08-04"
category: gcp
tags:
  - gcp
  - google-cloud
  - cloud
  - devops
  - course
comments: false
---

# Google Cloud for Cloud & DevOps Engineers

**Duration:** 12–16 weeks · **Difficulty:** Beginner → Advanced · **Labs:** create → prove → break/fix → cleanup
{ .ra-facts }

Learn Google Cloud the way operators use it: start from a clear problem, build a simple mental model, then practise with a real project lab (create → prove → break/fix where useful → cleanup). Suitable if you are new to Google Cloud or revising for Cloud and DevOps interviews.

!!! tip "How to use this course"
    Work modules in order. Finish each lab with evidence files and practise Interview Questions aloud.

!!! warning "Cost hygiene"
    Prefer Free Trial / Always Free. Create a budget alert in [Module 1](google-cloud-fundamentals-and-global-infrastructure.md) before you launch compute. **Never leave idle VMs, Cloud SQL, GKE clusters, or load balancers running overnight.**

## Learning roadmap

1. **Foundations (Modules 1–2)** — projects, regions/zones, `gcloud`, cost guardrails, Identity and Access Management (IAM)
2. **Network & compute (Modules 3–4)** — Virtual Private Cloud (VPC), Compute Engine
3. **Data & apps (Modules 5–8)** — storage, databases, Google Kubernetes Engine (GKE) / Artifact Registry, Cloud Run
4. **Data ops & observe (Modules 9–10)** — BigQuery / Pub/Sub lens, monitoring and logging
5. **Secure & deliver (Modules 11–14)** — security services, Terraform, CI/CD, FinOps
6. **Operate & triage (Modules 15–16)** — landing zones, troubleshooting under pressure

!!! tip "Course complete"
    All **16 modules** are published. After Module 16 you should defend hierarchy, IAM, VPC, compute vs GKE vs Cloud Run, secrets, IaC, pipelines, cost hygiene, landing-zone shape, and triage order.

### Prerequisites

- [Linux](../linux/index.md) · [Networking](../networking/index.md) · [Git](../git/index.md)
- [Docker](../docker/index.md) (recommended before Module 7)
- [Kubernetes](../kubernetes/index.md) and [Terraform](../terraform/index.md) recommended for Modules 7 and 12+

## Modules

| Module | Focus | Lab proof | Start here |
|-------:|-------|-----------|------------|
| 1 | Fundamentals | Auth + project + zones + budget alert | [Global infrastructure](google-cloud-fundamentals-and-global-infrastructure.md) |
| 2 | IAM | Service account + allow/deny proof | [Identity & access](iam-identity-access-and-resource-hierarchy.md) |
| 3 | Networking | Custom VPC + firewall break/fix | [VPC networking](vpc-networking-on-gcp.md) |
| 4 | Compute | Startup script VM + nginx break/fix | [Compute Engine · MIGs · LB](compute-engine-migs-and-load-balancing.md) |
| 5 | Storage | Bucket + lifecycle + IAM break/fix | [GCS · PD · Filestore](storage-gcs-persistent-disk-and-filestore.md) |
| 6 | Databases | Cloud SQL connect (or fallback) | [Databases on GCP](databases-on-gcp.md) |
| 7 | Containers | Artifact Registry + Autopilot (or alternate) | [GKE · Artifact Registry](containers-gke-and-artifact-registry.md) |
| 8 | Serverless | Cloud Run URL + revision break/fix | [Serverless on GCP](serverless-on-gcp.md) |
| 9 | Data & analytics | BigQuery query + Pub/Sub pull | [Data & analytics](data-and-analytics-on-gcp.md) |
| 10 | Monitoring | Log query + log-based metric / alert | [Observability](monitoring-and-observability-on-gcp.md) |
| 11 | Security | Secret Manager allow/deny | [Security services](gcp-security-services.md) |
| 12 | IaC | Terraform VPC + bucket + destroy | [Infrastructure as Code](infrastructure-as-code-on-gcp.md) |
| 13 | CI/CD | Cloud Build → AR → Cloud Run | [CI/CD on GCP](cicd-on-gcp.md) |
| 14 | Cost | Labels + budget review + idle hunt | [Cost optimisation](cost-optimisation-on-gcp.md) |
| 15 | Production | Landing-zone sketch + runbook | [Landing zones](production-gcp-landing-zones.md) |
| 16 | Troubleshooting | Firewall + IAM triage checklist | [Troubleshoot GCP](troubleshooting-gcp.md) |

### Soft certification map

| Exam | Strongest modules |
|------|-------------------|
| Cloud Digital Leader | 1, 14, 15 |
| Associate Cloud Engineer | 1–8, 11–13, 16 |
| Professional Cloud Architect | 3, 7, 11, 12, 15 |
| Professional Cloud DevOps Engineer | 10, 13, 14, 16 |

## Related

- [AWS](../aws/index.md) — parallel cloud course (same module spine)
- [Linux](../linux/index.md) · [Networking](../networking/index.md) · [Docker](../docker/index.md)
- [Kubernetes](../kubernetes/index.md) · [Terraform](../terraform/index.md)
- [Cloud Engineer path](../learning-paths/cloud-engineer/index.md)
