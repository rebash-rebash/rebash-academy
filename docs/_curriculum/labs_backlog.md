---
title: Labs backlog
description: Lab delivery backlog — ordered from beginner foundations to expert production scenarios.
author: Shaik Basha
category: curriculum
tags:
  - curriculum
---

# Labs backlog

Master list for lab authoring and curriculum alignment. Align frontmatter with [`lab-frontmatter-schema.md`](lab-frontmatter-schema.md) and ids with [`curriculum.yaml`](../../curriculum.yaml).

**Status values:** `published` (live under `docs/labs/`) · `planned` (on roadmap) · `draft` (in progress)

**Priority:** `P0` foundations · `P1` path-critical · `P2` depth · `P3` stretch

## Published labs (52)

Ordered beginner → expert within each technology group.

| Lab ID | Technology | Module | Title | Level | Type | Difficulty | Time | Learning paths | Prerequisites | Related tutorials | Related projects | Priority | Status |
|--------|------------|--------|-------|-------|------|------------|------|--------------|---------------|-------------------|------------------|----------|--------|
| `labs/linux-install-and-first-boot` | linux | Fundamentals | Install Linux and First Boot | guided | guided | intermediate | 60–120 min | beginner, linux-administrator | — | linux track M1 | — | P0 | published |
| `labs/linux-ssh-secure-access` | linux | Security | Configure SSH Secure Access | guided | security | intermediate | 60 min | devops-engineer, linux-administrator | linux-install-and-first-boot | linux SSH tutorials | — | P0 | published |
| `labs/linux-users-permissions-lab` | linux | Access control | Users, Groups, and Permissions | practice | scenario | intermediate | 60 min | linux-administrator | linux-ssh-secure-access | linux permissions | — | P0 | published |
| `labs/linux-storage-lab` | linux | Storage | Configure Linux Storage | guided | guided | intermediate | 60–90 min | linux-administrator | linux-users-permissions-lab | linux storage | — | P0 | published |
| `labs/linux-services-and-logs-lab` | linux | Services | Manage Services and Analyse Logs | practice | scenario | intermediate | 60 min | devops-engineer, linux-administrator | linux-storage-lab | systemd, journalctl | — | P0 | published |
| `labs/linux-firewall-hardening-lab` | linux | Security | Firewall and Server Hardening | practice | security | intermediate | 60–90 min | devops-engineer, devsecops-engineer | linux-services-and-logs-lab | firewall, hardening | — | P1 | published |
| `labs/linux-performance-troubleshooting-lab` | linux | Operations | Performance Troubleshooting | challenge | troubleshooting | intermediate | 60–90 min | devops-engineer, sre | linux-services-and-logs-lab | performance tuning | — | P1 | published |
| `labs/linux-ops-toolkit-lab` | linux | Automation | Linux Ops Toolkit | practice | automation | intermediate | 90 min | devops-engineer, linux-administrator | shell-first-script | linux automation | — | P1 | published |
| `labs/linux-production-incident-triage` | linux | Operations | Linux Production Incident Triage | production | troubleshooting | intermediate | 60 min | devops-engineer, sre | linux-services-and-logs-lab | systemd triage | status-api-portfolio | P1 | published |
| `labs/linux-app-server-from-zero` | linux | Capstone | Linux App Server from Zero | production | capstone | advanced | 120 min | devops-engineer, linux-administrator | linux-ops-toolkit-lab | full linux track | status-api-portfolio | P2 | published |
| `labs/shell-first-script` | shell | Fundamentals | Create Your First Script | guided | guided | beginner | 30–45 min | beginner, devops-engineer | linux-install-and-first-boot | shell intro | — | P0 | published |
| `labs/shell-user-management-script` | shell | Scripting | Build a User Management Script | guided | automation | intermediate | 45–60 min | linux-administrator | shell-first-script | shell variables | — | P0 | published |
| `labs/shell-automate-software-installation` | shell | Automation | Automate Software Installation | practice | automation | intermediate | 60 min | devops-engineer | shell-first-script | package automation | — | P1 | published |
| `labs/shell-backup-utility` | shell | Automation | Build a Backup Utility | practice | automation | intermediate | 60 min | devops-engineer, linux-administrator | shell-first-script | backup patterns | — | P1 | published |
| `labs/shell-rotate-logs` | shell | Operations | Rotate Logs | practice | scenario | intermediate | 45 min | linux-administrator | shell-backup-utility | log rotation | — | P1 | published |
| `labs/shell-monitor-disk-usage` | shell | Monitoring | Monitor Disk Usage | practice | automation | intermediate | 45 min | devops-engineer, sre | shell-first-script | disk monitoring | — | P1 | published |
| `labs/shell-monitor-cpu-memory` | shell | Monitoring | Monitor CPU and Memory | practice | automation | intermediate | 45 min | devops-engineer, sre | shell-monitor-disk-usage | resource monitoring | — | P1 | published |
| `labs/shell-service-health-checker` | shell | Monitoring | Build a Service Health Checker | practice | automation | intermediate | 60 min | devops-engineer, sre | shell-monitor-cpu-memory | health checks | — | P1 | published |
| `labs/shell-ssl-certificate-monitor` | shell | Security | Build an SSL Certificate Monitor | practice | security | intermediate | 60 min | devops-engineer, devsecops-engineer | shell-service-health-checker | TLS monitoring | — | P2 | published |
| `labs/shell-parse-json-jq` | shell | Data | Parse JSON with jq | guided | quick | intermediate | 30–45 min | devops-engineer | shell-first-script | jq basics | — | P1 | published |
| `labs/shell-parse-yaml-yq` | shell | Data | Parse YAML with yq | guided | quick | intermediate | 30–45 min | devops-engineer | shell-parse-json-jq | yq basics | — | P1 | published |
| `labs/shell-automate-ssh-tasks` | shell | Automation | Automate SSH Tasks | practice | automation | intermediate | 60 min | devops-engineer | linux-ssh-secure-access | SSH automation | — | P1 | published |
| `labs/shell-deployment-script` | shell | CI/CD | Build a Deployment Script | practice | automation | intermediate | 60–90 min | devops-engineer | shell-automate-ssh-tasks | deployment patterns | — | P1 | published |
| `labs/shell-linux-operations-toolkit` | shell | Capstone | Create a Linux Operations Toolkit | production | capstone | advanced | 120 min | devops-engineer, linux-administrator | shell-deployment-script | shell track | ops-toolkit-project | P2 | published |
| `labs/shell-ops-script-hardening` | shell | Security | Shell Ops Script Hardening | production | security | advanced | 60–90 min | devops-engineer, devsecops-engineer | shell-linux-operations-toolkit | strict mode, traps | — | P2 | published |
| `labs/python-log-analyser` | python | Fundamentals | Python Log Analyser | guided | guided | intermediate | 45–60 min | devops-engineer | shell-first-script | python basics | — | P0 | published |
| `labs/python-linux-health-checker` | python | Automation | Python Linux Health Checker | practice | automation | intermediate | 60 min | devops-engineer, sre | python-log-analyser | paramiko, APIs | — | P1 | published |
| `labs/python-yaml-config-validator` | python | Data | Python YAML Config Validator | practice | automation | intermediate | 45 min | devops-engineer | python-log-analyser | pyyaml | — | P1 | published |
| `labs/python-json-validator` | python | Data | Python JSON Validator | practice | automation | intermediate | 45 min | devops-engineer | python-yaml-config-validator | json schema | — | P1 | published |
| `labs/python-github-repository-auditor` | python | DevOps | Python GitHub Repository Auditor | practice | automation | intermediate | 60 min | devops-engineer, platform-engineer | python-json-validator | GitHub API | — | P1 | published |
| `labs/python-docker-cleanup-tool` | python | Containers | Python Docker Cleanup Tool | practice | automation | intermediate | 60 min | devops-engineer | docker track M1 | Docker SDK | — | P1 | published |
| `labs/python-kubernetes-health-checker` | python | Kubernetes | Python Kubernetes Health Checker | practice | automation | intermediate | 60 min | devops-engineer, kubernetes-engineer | python-docker-cleanup-tool | k8s client | — | P1 | published |
| `labs/python-kubernetes-deployment-validator` | python | Kubernetes | Python Kubernetes Deployment Validator | challenge | automation | advanced | 60–90 min | kubernetes-engineer | python-kubernetes-health-checker | deployments | — | P2 | published |
| `labs/python-terraform-wrapper` | python | IaC | Python Terraform Wrapper | practice | automation | intermediate | 60 min | devops-engineer, cloud-engineer | terraform track M1 | subprocess, IaC | — | P1 | published |
| `labs/python-aws-ec2-inventory` | python | Cloud | Python AWS EC2 Inventory | practice | automation | intermediate | 60 min | cloud-engineer, devops-engineer | aws track M1 | boto3 | — | P1 | published |
| `labs/python-azure-resource-inventory` | python | Cloud | Python Azure Resource Inventory | practice | automation | intermediate | 60 min | cloud-engineer | python-aws-ec2-inventory | Azure SDK | — | P2 | published |
| `labs/python-gcp-inventory` | python | Cloud | Python GCP Inventory | practice | automation | intermediate | 60 min | cloud-engineer | python-aws-ec2-inventory | GCP SDK | — | P2 | published |
| `labs/python-certificate-expiry-monitor` | python | Security | Python Certificate Expiry Monitor | practice | security | intermediate | 60 min | devops-engineer, devsecops-engineer | python-linux-health-checker | TLS monitoring | — | P2 | published |
| `labs/python-slack-notification-bot` | python | Integration | Python Slack Notification Bot | practice | automation | intermediate | 60 min | devops-engineer | python-linux-health-checker | webhooks | — | P2 | published |
| `labs/python-rest-api-monitoring-service` | python | SRE | Python REST API Monitoring Service | production | scenario | advanced | 90 min | sre, devops-engineer | python-slack-notification-bot | HTTP monitoring | status-api-portfolio | P2 | published |
| `labs/python-secrets-scanner` | python | Security | Python Secrets Scanner | production | security | advanced | 60–90 min | devsecops-engineer | python-github-repository-auditor | secret scanning | — | P2 | published |
| `labs/python-cicd-automation-tool` | python | CI/CD | Python CI/CD Automation Tool | production | automation | advanced | 90 min | devops-engineer, platform-engineer | cicd-pipeline-triage | pipeline APIs | — | P2 | published |
| `labs/networking-dns-firewall-triage` | networking | Operations | DNS and Firewall Site-Down Triage | production | troubleshooting | intermediate | 60–90 min | devops-engineer, sre | networking track M1 | DNS, firewall | — | P1 | published |
| `labs/networking-edge-failover` | networking | Architecture | Networking Edge Failover | production | scenario | advanced | 90 min | cloud-architect, sre | networking-dns-firewall-triage | load balancing | — | P2 | published |
| `labs/aws-iam-vpc-triage` | aws | Security | AWS IAM and VPC Reachability Triage | production | troubleshooting | intermediate | 60–90 min | cloud-engineer, devops-engineer | aws track M1 | IAM, VPC | — | P1 | published |
| `labs/aws-ssm-s3` | aws | Operations | Secure EC2 via SSM and S3 | production | security | intermediate | 60–90 min | cloud-engineer, devsecops-engineer | aws-iam-vpc-triage | SSM, S3 | — | P1 | published |
| `labs/git-history-pr-recovery` | git | Workflow | Git History and PR Recovery | challenge | troubleshooting | intermediate | 45–60 min | devops-engineer | git track M1 | git recovery | — | P1 | published |
| `labs/cicd-pipeline-triage` | gitlab | CI/CD | CI/CD Pipeline Failure Triage | production | troubleshooting | intermediate | 60 min | devops-engineer | gitlab track M1 | GitLab CI | — | P1 | published |
| `labs/cicd-docker-secure-gate` | gitlab | DevSecOps | Docker Build, Scan, and Deploy Gate | production | security | advanced | 90 min | devsecops-engineer, devops-engineer | cicd-pipeline-triage | container scanning | — | P2 | published |
| `labs/docker-compose-stack-recovery` | docker | Operations | Docker Compose Stack Recovery | production | troubleshooting | intermediate | 60–90 min | devops-engineer | docker track M1 | Compose | — | P1 | published |
| `labs/kubernetes-deployment-triage` | kubernetes | Operations | Kubernetes Deployment Triage | production | troubleshooting | intermediate | 60–90 min | devops-engineer, kubernetes-engineer, sre | kubernetes track M1 | deployments | — | P1 | published |
| `labs/terraform-plan-review-workflow` | terraform | IaC | Terraform Plan Review Workflow | production | scenario | intermediate | 60–90 min | cloud-engineer, devops-engineer | terraform track M1 | plan/apply | landing-zone-project | P1 | published |

## Planned lab tracks

Technologies with tutorial tracks but no dedicated lab series yet. Add rows here before authoring.

| Technology | Target count | First lab (planned) | Priority | Status |
|------------|--------------|---------------------|----------|--------|
| helm | 8 | Chart install and rollback triage | P2 | planned |
| ansible | 10 | Playbook idempotency fix | P2 | planned |
| azure | 8 | Resource group networking triage | P2 | planned |
| gcp | 8 | GKE workload identity lab | P2 | planned |
| github-actions | 8 | Workflow failure triage | P2 | planned |
| jenkins | 8 | Pipeline agent connectivity | P3 | planned |
| argocd | 6 | GitOps sync drift remediation | P2 | planned |
| prometheus | 6 | Alert rule debugging | P2 | planned |
| grafana | 6 | Dashboard datasource failure | P3 | planned |
| loki | 6 | Log ingestion gap triage | P3 | planned |
| tempo | 6 | Trace pipeline break | P3 | planned |
| opentelemetry | 6 | Collector pipeline validation | P3 | planned |
| devsecops | 10 | Pipeline policy gate bypass | P1 | planned |
| platform-engineering | 8 | Golden path template lab | P2 | planned |
| sre | 8 | Error budget burn response | P2 | planned |
| cloud-architecture | 6 | Landing zone design review | P3 | planned |
| ai | 6 | Ops agent workflow lab | P3 | planned |

## Learning progression (per technology)

```
Tutorial → Guided lab → Practice lab → Challenge lab → Project → Capstone
```

## Learning path mapping

Labs declare `learning_paths` in frontmatter. Path detail pages link back to recommended labs via curriculum ids — keep slugs stable under `docs/labs/`.

## Navigation

Public browse: [Labs overview](../labs/index.md) · Sidebar: `docs/labs/.pages` grouped by technology · Do not move published lab URLs when adding subfolders.
