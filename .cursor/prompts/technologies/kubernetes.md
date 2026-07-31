# Technology Definition

## Course

Kubernetes for Cloud & DevOps Engineers

---

## Description

A production-focused Kubernetes course designed for Cloud Engineers, DevOps Engineers, Platform Engineers and Site Reliability Engineers.

This course teaches Kubernetes from the ground up, progressing from core concepts to production operations, security, troubleshooting and platform engineering.

Learners should finish the course capable of deploying, operating, securing and troubleshooting production Kubernetes clusters.

---

## Target Roles

- Kubernetes Administrator
- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer

---

## Difficulty

Intermediate → Advanced

---

## Estimated Duration

10–12 Weeks

---

## Prerequisites

- Linux Fundamentals
- Networking Fundamentals
- Shell Scripting
- Python Basics
- Git & GitHub
- Docker

---

## MCP Servers

Primary

- Kubernetes

Optional

- Context7
- GitHub
- Terraform
- AWS
- Azure
- Google Cloud

---

# Modules

## Module 1 — Kubernetes Fundamentals

- What is Kubernetes?
- Why Kubernetes?
- Kubernetes Architecture
- Control Plane
- Worker Nodes
- Cluster Components
- Kubernetes API

---

## Module 2 — Cluster Setup

- Minikube
- Kind
- K3s
- kubeadm
- Managed Kubernetes
- kubectl
- kubeconfig

---

## Module 3 — Kubernetes Objects

- Pods
- ReplicaSets
- Deployments
- Namespaces
- Labels
- Selectors
- Annotations

---

## Module 4 — Workload Management

- Deployments
- StatefulSets
- DaemonSets
- Jobs
- CronJobs
- Rollouts
- Rollbacks

---

## Module 5 — Services & Networking

- ClusterIP
- NodePort
- LoadBalancer
- ExternalName
- Headless Services
- EndpointSlices
- kube-proxy

---

## Module 6 — Ingress & Gateway API

- Ingress
- Ingress Controller
- TLS
- Gateway API
- HTTPRoute
- Traffic Routing

---

## Module 7 — Storage

- Volumes
- Persistent Volumes
- Persistent Volume Claims
- Storage Classes
- CSI
- Dynamic Provisioning

---

## Module 8 — Configuration

- ConfigMaps
- Secrets
- Environment Variables
- Downward API
- Resource Quotas
- LimitRanges

---

## Module 9 — Scheduling

- Node Selectors
- Affinity
- Anti-Affinity
- Taints
- Tolerations
- Topology Spread Constraints

---

## Module 10 — Security

- RBAC
- Service Accounts
- Security Contexts
- Pod Security Admission
- Network Policies
- Secrets
- Image Policies

---

## Module 11 — Networking Deep Dive

- CNI
- CoreDNS
- kube-proxy
- Network Policies
- Service Discovery
- DNS Resolution

---

## Module 12 — Observability

- Metrics Server
- Prometheus
- Grafana
- kube-state-metrics
- Logging
- Events

---

## Module 13 — Autoscaling

- HPA
- VPA
- Cluster Autoscaler
- KEDA

---

## Module 14 — Package Management

- Helm
- Helm Charts
- Repositories
- Chart Development
- Dependencies

---

## Module 15 — GitOps

- GitOps Principles
- Argo CD
- Flux
- Progressive Delivery
- Rollbacks

---

## Module 16 — Platform Engineering

- Operators
- CRDs
- Admission Controllers
- Custom Controllers
- Multi-Tenancy
- Namespaces

---

## Module 17 — Production Operations

- Upgrades
- Backup & Restore
- etcd
- Disaster Recovery
- High Availability
- Maintenance

---

## Module 18 — Troubleshooting

- CrashLoopBackOff
- ImagePullBackOff
- Pending Pods
- DNS Failures
- Scheduling Failures
- Storage Issues
- Networking Issues
- Performance Problems

---

## Module 19 — Managed Kubernetes

### AWS

- Amazon EKS

### Azure

- Azure Kubernetes Service (AKS)

### Google Cloud

- Google Kubernetes Engine (GKE)

---

## Module 20 — Production Kubernetes

- Multi-Cluster
- Security Hardening
- Policy Enforcement
- Cost Optimisation
- Monitoring
- Logging
- Scaling
- Operational Excellence

---

# Hands-on Labs

- Install a Kubernetes Cluster
- Deploy Your First Application
- Scale Applications
- Perform Rolling Updates
- Configure Services
- Configure Ingress
- Deploy Stateful Applications
- Configure Persistent Storage
- Implement RBAC
- Create Network Policies
- Configure Autoscaling
- Deploy Prometheus & Grafana
- Install Helm Charts
- Deploy Argo CD
- Backup & Restore etcd
- Troubleshoot Production Failures
- Build a Highly Available Cluster

---

# Projects

## Beginner

Deploy a Three-Tier Application

---

## Intermediate

Kubernetes Monitoring Platform

---

## Advanced

GitOps-Based Kubernetes Platform

---

## Capstone

Production Kubernetes Platform

Features:

- Highly Available Cluster
- GitOps Deployment
- RBAC
- Network Policies
- Ingress
- Persistent Storage
- Monitoring
- Logging
- Autoscaling
- Backup & Restore
- Disaster Recovery
- Policy Enforcement

---

# Cheat Sheets

Generate:

- kubectl Commands
- YAML Reference
- Workloads
- Services
- Storage
- Networking
- RBAC
- Helm
- Argo CD
- Troubleshooting

---

# Interview Preparation

Cover:

- Kubernetes Architecture
- Scheduling
- Networking
- Storage
- Security
- Helm
- GitOps
- Observability
- Troubleshooting
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Kubernetes tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Kubernetes Architecture
- Control Plane
- Pod Lifecycle
- Service Networking
- Ingress Flow
- Storage Architecture
- RBAC Model
- Helm Architecture
- GitOps Workflow
- Production Cluster Design

---

# Certifications

Map modules where appropriate to:

- KCNA
- CKA
- CKAD
- CKS

---

# Capstone Outcome

After completing this course learners should be able to:

- Deploy production Kubernetes workloads
- Design Kubernetes architectures
- Secure clusters
- Troubleshoot complex issues
- Operate managed Kubernetes platforms
- Implement GitOps
- Monitor and optimise clusters
- Build production-ready cloud-native platforms