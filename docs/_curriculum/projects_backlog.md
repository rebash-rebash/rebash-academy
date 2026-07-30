---
title: Projects backlog
description: Mini through capstone project backlog for REBASH Academy — ordered beginner to expert.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Projects backlog

Master backlog for portfolio projects. Align IDs and metadata with [`project-frontmatter-schema.md`](project-frontmatter-schema.md) and [`curriculum.yaml`](../../curriculum.yaml).

**Status values:** `published` · `draft` · `planned`

## Published — Foundations (Linux, Shell, Python)

| Project ID | Technology | Level | Title | Duration | Career paths | Related tutorials | Related labs | Skills | Priority | Status |
|------------|------------|-------|-------|----------|--------------|-------------------|--------------|--------|----------|--------|
| `linux-system-information-utility` | linux | mini | Linux System Information Utility | 3–5 h | linux-administrator, beginner | linux/linux-essential-commands | labs/linux-install-and-first-boot | bash, /proc, ip | P1 | published |
| `shell-linux-automation-scripts` | shell | mini | Linux Automation Scripts | 3–5 h | devops-engineer, linux-administrator | shell/shell-intro-ops | labs/shell-first-script | bash, host facts, backup | P1 | published |
| `python-log-analysis-tool` | python | mini | Python Log Analysis Tool | 4–6 h | devops-engineer, ai-for-devops | python/python-intro-devops | labs/python-log-analyser | pathlib, re, argparse, pytest | P1 | published |
| `linux-server-health-dashboard` | linux | intermediate | Linux Server Health Dashboard | 8–12 h | linux-administrator, devops-engineer | linux/linux-host-monitoring | labs/linux-host-monitoring | bash, cron, HTML report | P1 | published |
| `shell-linux-administration-toolkit` | shell | intermediate | Linux Administration Toolkit | 8–12 h | linux-administrator | shell/shell-linux-admin | labs/shell-linux-admin | bash CLI, users, packages | P1 | published |
| `python-infra-inventory-cli` | python | intermediate | Python Infrastructure Inventory CLI | 8–12 h | devops-engineer, cloud-engineer | python/python-http-apis | labs/python-cloud-inventory | Typer, httpx, pytest | P1 | published |
| `linux-operations-toolkit` | linux | enterprise | Linux Operations Toolkit | 12–16 h | linux-administrator, devops-engineer | linux/linux-production-hardening | labs/linux-production-incident-triage | bash CLI, audits, triage | P1 | published |
| `shell-production-operations-toolkit` | shell | enterprise | Production Operations Toolkit | 12–16 h | devops-engineer, site-reliability-engineer | shell/shell-ops-toolkit | labs/shell-ops-script-hardening | health, certs, SSH, deploy | P1 | published |
| `python-cloud-operations-toolkit` | python | enterprise | Python Cloud Operations Toolkit | 12–18 h | devops-engineer, cloud-engineer | python/python-cloud-automation | labs/python-kubernetes-health | cloud SDKs, Docker, Kubernetes | P1 | published |
| `python-platform-engineering-framework` | python | enterprise | Python Platform Engineering Framework | 16–24 h | platform-engineer, devops-engineer | python/python-plugin-architecture | labs/python-docker-cleanup | plugins, packaging, shared libs | P2 | published |
| `linux-production-operations-platform` | linux | capstone | Production Linux Operations Platform | 20–30 h | linux-administrator, site-reliability-engineer | linux/linux-backup-dr | labs/linux-firewall-hardening | hardening, backup, alert, report | P1 | published |
| `shell-production-automation-framework` | shell | capstone | Production Shell Automation Framework | 20–30 h | devops-engineer, platform-engineer | shell/shell-capstone | labs/shell-strict-mode | modular Bash framework | P1 | published |
| `python-devops-automation-framework` | python | capstone | Production DevOps Automation Platform | 24–40 h | devops-engineer, platform-engineer | python/python-prod-patterns | labs/python-kubernetes-health | CLI, plugins, cloud, CI, dry-run | P1 | published |

## Published — Portfolio (multi-stack)

| Project ID | Technology | Level | Title | Duration | Career paths | Related tutorials | Related labs | Skills | Priority | Status |
|------------|------------|-------|-------|----------|--------------|-------------------|--------------|--------|----------|--------|
| `status-api-portfolio` | git, docker, kubernetes, terraform | intermediate | Status API Portfolio Build | 3–4 h | devops-engineer, kubernetes-engineer | docker/, kubernetes/, terraform/ | labs/docker-compose-stack-recovery, labs/kubernetes-deployment-triage | Git, Docker, K8s, Terraform | P1 | published |

## Planned — Cloud

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `aws-ec2-provision-mini` | aws, terraform | mini | Provision an EC2 VM | 3–5 h | cloud-engineer | P2 | planned |
| `aws-terraform-modules` | aws, terraform | intermediate | Reusable Terraform Modules | 8–12 h | cloud-engineer, devops-engineer | P2 | planned |
| `aws-landing-zone` | aws, terraform, gitlab | enterprise | Multi-account AWS Landing Zone | 20–30 h | cloud-engineer, cloud-architect | P1 | planned |
| `multi-cloud-platform` | aws, azure, gcp, terraform | capstone | Multi-cloud Platform | 30–40 h | cloud-architect | P2 | planned |
| `azure-foundation-stack` | azure, terraform | intermediate | Azure Foundation Stack | 8–12 h | cloud-engineer | P3 | planned |
| `gcp-gke-bootstrap` | gcp, terraform, kubernetes | intermediate | GKE Bootstrap Platform | 8–12 h | cloud-engineer, kubernetes-engineer | P3 | planned |

## Planned — Containers & orchestration

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `docker-containerise-app` | docker | mini | Containerise an Application | 3–5 h | devops-engineer | P2 | planned |
| `docker-compose-stack` | docker | intermediate | Production Compose Stack | 8–12 h | devops-engineer | P2 | planned |
| `docker-production-platform` | docker | enterprise | Production Container Platform | 16–24 h | platform-engineer | P2 | planned |
| `docker-container-platform-capstone` | docker | capstone | Enterprise Container Platform | 24–36 h | platform-engineer, devops-engineer | P3 | planned |
| `kubernetes-deploy-app` | kubernetes | mini | Deploy an Application | 3–5 h | kubernetes-engineer | P2 | planned |
| `kubernetes-multi-service` | kubernetes | intermediate | Multi-service Application | 8–12 h | kubernetes-engineer | P2 | planned |
| `kubernetes-production-cluster` | kubernetes, helm | enterprise | Production Cluster Platform | 20–30 h | kubernetes-engineer, platform-engineer | P1 | planned |
| `kubernetes-enterprise-platform` | kubernetes, helm, argocd | capstone | Enterprise Kubernetes Platform | 30–40 h | kubernetes-engineer, platform-engineer | P1 | planned |

## Planned — Infrastructure as Code

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `terraform-ec2-mini` | terraform, aws | mini | Provision an EC2 Instance | 3–5 h | cloud-engineer | P2 | planned |
| `terraform-reusable-modules` | terraform | intermediate | Reusable Terraform Modules | 8–12 h | devops-engineer, cloud-engineer | P2 | planned |
| `terraform-landing-zone` | terraform, aws | enterprise | Organisation Landing Zone | 20–30 h | cloud-architect, cloud-engineer | P1 | planned |
| `terraform-multi-cloud-capstone` | terraform | capstone | Multi-cloud Infrastructure Platform | 30–40 h | cloud-architect | P2 | planned |
| `ansible-config-baseline` | ansible, linux | intermediate | Configuration Baseline with Ansible | 8–12 h | linux-administrator, devops-engineer | P3 | planned |

## Planned — CI/CD & GitOps

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `gitlab-pipeline-mini` | gitlab | mini | First GitLab Pipeline | 3–5 h | devops-engineer | P2 | planned |
| `github-actions-delivery` | github-actions | intermediate | GitHub Actions Delivery Pipeline | 8–12 h | devops-engineer | P3 | planned |
| `jenkins-shared-library` | jenkins | intermediate | Jenkins Shared Library Platform | 8–12 h | devops-engineer | P3 | planned |
| `argocd-gitops-bootstrap` | argocd, kubernetes | enterprise | GitOps Platform Bootstrap | 16–24 h | platform-engineer, kubernetes-engineer | P1 | planned |
| `devsecops-pipeline-capstone` | gitlab, devsecops | capstone | DevSecOps Delivery Platform | 24–36 h | devsecops-engineer, devops-engineer | P1 | planned |

## Planned — Observability

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `prometheus-alerting-mini` | prometheus | mini | First Prometheus Alert | 3–5 h | site-reliability-engineer | P3 | planned |
| `grafana-dashboard-platform` | grafana, prometheus | intermediate | Grafana Dashboard Platform | 8–12 h | site-reliability-engineer | P3 | planned |
| `observability-stack` | prometheus, grafana, loki | enterprise | Observability Stack | 20–30 h | site-reliability-engineer, platform-engineer | P1 | planned |
| `otel-instrumentation-capstone` | opentelemetry, tempo, loki | capstone | Full-stack Observability Platform | 24–36 h | site-reliability-engineer | P2 | planned |

## Planned — Security, platform & AI

| Project ID | Technology | Level | Title | Duration | Career paths | Priority | Status |
|------------|------------|-------|-------|----------|--------------|----------|--------|
| `devsecops-scan-gates` | devsecops, gitlab | intermediate | Pipeline Security Gates | 8–12 h | devsecops-engineer | P2 | planned |
| `internal-developer-platform` | platform-engineering, kubernetes | capstone | Internal Developer Platform | 30–40 h | platform-engineer | P1 | planned |
| `ai-ops-assistant` | ai-for-devops, python | enterprise | AI-assisted Operations Platform | 16–24 h | ai-for-devops, site-reliability-engineer | P2 | planned |

## Portfolio showcase recommendations

Projects learners should prioritise for CV and interview demos:

1. **Status API Portfolio Build** — published; proves Git → Docker → Kubernetes → Terraform
2. **Cloud landing zone** — planned; Terraform organisation patterns
3. **GitOps platform bootstrap** — planned; declarative delivery
4. **Observability stack** — planned; metrics, logs, alerting
5. **DevSecOps pipeline** — planned; secure delivery
6. **Internal developer platform** — planned; golden paths and self-service
7. **Multi-cloud infrastructure** — planned; architecture at scale
8. **AI-assisted operations platform** — planned; practical AI workflows

## Navigation structure

Public MkDocs nav (flat under `docs/projects/` today; group by level in `.pages` as catalogue grows):

```
Projects
  Overview
  Mini / intermediate / enterprise / capstone groupings (future)
  Per-technology indexes (future under docs/<technology>/)
```

Technology indexes link to related projects; the Projects landing page (`projects.html`) is the visual catalogue.
