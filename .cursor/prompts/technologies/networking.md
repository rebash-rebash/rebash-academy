# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

Networking for Cloud & DevOps Engineers

---

## Description

A practical networking course focused on Linux, Cloud, Kubernetes and DevOps.

The course teaches networking from an operations, troubleshooting and cloud engineering perspective rather than a traditional network engineering approach.

Learners should finish the course capable of designing, troubleshooting and operating production networks.

---

## Target Roles

- Cloud Engineer
- DevOps Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Kubernetes Administrator
- Infrastructure Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

8–10 Weeks

---

## Prerequisites

- Basic Linux knowledge
- Command line familiarity

---

## MCP Servers

Primary

- Context7

Optional

- Kubernetes
- AWS
- Azure
- GitHub

---

# Modules

## Module 1 — Networking Fundamentals

- What is Networking?
- Network Types
- LAN
- WAN
- MAN
- VPN
- Internet
- Intranet
- Extranet
- Network Topologies

---

## Module 2 — OSI Model

- Layer 1 – Physical
- Layer 2 – Data Link
- Layer 3 – Network
- Layer 4 – Transport
- Layer 5 – Session
- Layer 6 – Presentation
- Layer 7 – Application

---

## Module 3 — TCP/IP Model

- Link Layer
- Internet Layer
- Transport Layer
- Application Layer
- Protocol Mapping

---

## Module 4 — IP Addressing

- IPv4
- IPv6
- Binary Basics
- CIDR
- Subnet Masks
- Public vs Private IP
- Loopback
- Reserved Networks
- Broadcast

---

## Module 5 — Subnetting

- CIDR Calculations
- Network Address
- Broadcast Address
- Host Calculation
- Variable Length Subnet Masking (VLSM)

---

## Module 6 — Routing

- Routing Concepts
- Default Gateway
- Routing Tables
- Static Routing
- Dynamic Routing
- ECMP
- Longest Prefix Match

---

## Module 7 — Switching

- Ethernet
- MAC Address
- ARP
- VLAN
- Trunk Ports
- Layer 2 vs Layer 3

---

## Module 8 — TCP & UDP

- TCP
- UDP
- Ports
- Three-Way Handshake
- Connection Lifecycle
- Flow Control
- Congestion Control

---

## Module 9 — DNS

- DNS Resolution
- Recursive Queries
- Authoritative DNS
- A
- AAAA
- CNAME
- TXT
- MX
- PTR
- SRV

---

## Module 10 — HTTP & HTTPS

- HTTP Methods
- Headers
- Cookies
- Sessions
- TLS
- Certificates
- Reverse Proxy
- HTTP Status Codes

---

## Module 11 — NAT & Firewalls

- SNAT
- DNAT
- PAT
- Port Forwarding
- Stateful Firewalls
- Packet Filtering
- Security Groups
- Network ACLs

---

## Module 12 — Linux Networking

- ip
- ss
- ping
- traceroute
- tracepath
- dig
- host
- nslookup
- curl
- wget
- tcpdump
- tshark
- netcat
- socat

---

## Module 13 — Load Balancing

- Layer 4 Load Balancer
- Layer 7 Load Balancer
- Reverse Proxy
- HAProxy
- NGINX
- Health Checks
- Session Persistence

---

## Module 14 — Kubernetes Networking

- Pod Networking
- CNI
- Services
- ClusterIP
- NodePort
- LoadBalancer
- Ingress
- Gateway API
- CoreDNS
- Network Policies

---

## Module 15 — Cloud Networking

### AWS

- VPC
- Subnets
- Route Tables
- Internet Gateway
- NAT Gateway
- Security Groups
- NACL
- Route53
- Transit Gateway
- Load Balancers

### Azure

- Virtual Network
- NSG
- User Defined Routes
- Azure Firewall
- Load Balancer
- Application Gateway
- Private Link

### Google Cloud

- VPC
- Firewall Rules
- Cloud Router
- Cloud NAT
- Load Balancer
- Cloud DNS

---

## Module 16 — Production Networking

- High Availability
- Zero Trust
- Hybrid Networking
- VPN
- Private Connectivity
- Service Mesh Concepts
- Network Observability
- Performance Optimisation
- Disaster Recovery

---

## Module 17 — Troubleshooting

- DNS Failures
- Routing Problems
- MTU Issues
- Packet Loss
- High Latency
- Firewall Issues
- TLS Errors
- Load Balancer Failures
- Kubernetes Connectivity
- Cloud Networking Problems

---

# Hands-on Labs

- Build a Virtual Network
- Configure IP Addressing
- Perform Subnet Calculations
- Configure Static Routing
- Capture Packets using tcpdump
- Analyse Packets with Wireshark
- Troubleshoot DNS
- Configure SSH Connectivity
- Configure Linux Firewall
- Configure Reverse Proxy
- Deploy Kubernetes Services
- Debug Pod Networking
- Configure Ingress
- Build AWS VPC
- Configure Azure VNet
- Configure Google Cloud VPC
- Troubleshoot Production Networking

---

# Projects

## Beginner

Network Troubleshooting Toolkit

---

## Intermediate

Linux Network Monitoring Dashboard

---

## Advanced

Cloud Network Design Toolkit

---

## Capstone

Production Cloud Network Platform

Features:

- Multi-tier Network
- Public & Private Subnets
- Routing
- DNS
- Load Balancing
- High Availability
- Kubernetes Networking
- Monitoring
- Security Controls
- Disaster Recovery

---

# Cheat Sheets

Generate:

- TCP vs UDP
- OSI Model
- TCP/IP Model
- CIDR & Subnetting
- Linux Networking Commands
- DNS Records
- HTTP Status Codes
- TLS
- Kubernetes Networking
- Cloud Networking

---

# Interview Preparation

Cover:

- Networking Fundamentals
- Linux Networking
- TCP/IP
- DNS
- Routing
- Load Balancing
- Kubernetes Networking
- Cloud Networking
- Troubleshooting
- Production Scenarios

---

# Excalidraw Diagrams

Use **Excalidraw only** — never D2 or Mermaid for this course.

Store under `docs/assets/excalidraw/` as `.svg` (embedded in tutorials) and `.excalidraw` (editable source).

Regenerate shared diagrams: `python3 scripts/generate-excalidraw-svg.py`

Generate diagrams for:

- OSI Model
- TCP/IP Stack
- Packet Flow
- DNS Resolution
- TCP Handshake
- VPC Architecture
- Kubernetes Networking
- Load Balancer Architecture
- Reverse Proxy Flow
- Cloud Network Design
- Network Types
- Topologies
- Subnetting / VLSM

---

# Certifications

Map modules where appropriate to:

- CCNA
- AWS Solutions Architect – Associate
- Azure Administrator Associate
- Google Associate Cloud Engineer
- CKA
- CKAD

---

# Capstone Outcome

After completing this course learners should be able to:

- Design production networks
- Troubleshoot connectivity issues
- Configure Linux networking
- Understand Kubernetes networking
- Build cloud network architectures
- Diagnose DNS and routing issues
- Configure secure communication
- Operate production cloud networking environments