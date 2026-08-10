---
title: "IDS/IPS"
description: "Learn Intrusion Detection and Prevention Systems — signature and anomaly detection, NIDS vs HIDS, IDS vs IPS, and Linux investigation basics."
difficulty: intermediate
estimated_time: "120 min"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
technology: networking
module: "Module 8 · Network Security"
learning_paths:
  - cloud-engineer
  - devops-engineer
  - site-reliability-engineer
  - linux-administrator
  - platform-engineer
tags:
  - networking
  - ids
  - ips
  - security
  - rebash-networking-mastery
comments: false
status: ready
---

# IDS/IPS (Intrusion Detection System / Intrusion Prevention System) — Detecting and Preventing Cyber Attacks

> An **Intrusion Detection System (IDS)** and **Intrusion Prevention System (IPS)** are network security technologies that monitor network traffic and system activity to identify malicious behaviour, security policy violations, and cyber attacks. While an **IDS detects and alerts** administrators about suspicious activity, an **IPS actively blocks or prevents** malicious traffic in real time. IDS/IPS solutions are essential components of enterprise, cloud, and hybrid security architectures. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand IDS and IPS technologies.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 8: Network Security → Lesson 6</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Intermediate</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Security</div>

<div markdown>**Lesson:** 6 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand IDS and IPS
- Compare Detection and Prevention
- Learn Signature-Based Detection
- Understand Anomaly-Based Detection
- Compare Network IDS and Host IDS
- Apply IDS/IPS in enterprise and cloud environments
- Troubleshoot IDS/IPS deployments

---

# Prerequisites

Complete:

- [VPN](vpn-and-tunneling-basics.md)
- [IPSec](ipsec.md)
- [SSL/TLS](ssl-tls.md)
- [SSH](ssh-networking.md)
- [Network Hardening](network-security-hardening.md)

---

# Why Learn IDS/IPS?

Imagine an attacker scanning your network.

Without IDS/IPS:

```text
Attacker

↓

Network

↓

Servers

↓

No Detection

❌
```

With IDS/IPS:

```text
Attacker

↓

IDS/IPS

↓

Detect

↓

Alert

↓

Block (IPS)

✓
```

Security teams become aware of attacks and, with IPS, can automatically stop them.

---

# What is an IDS?

An **Intrusion Detection System (IDS)** monitors network or system activity to identify suspicious behaviour.

An IDS:

- Detects Attacks
- Generates Alerts
- Logs Events

An IDS **does not automatically block traffic**.

---

# What is an IPS?

An **Intrusion Prevention System (IPS)** performs all IDS functions and additionally:

- Blocks Malicious Traffic
- Terminates Connections
- Drops Packets
- Prevents Exploitation

An IPS operates inline with network traffic.

---

# IDS vs IPS

| IDS | IPS |
|-----|-----|
| Detects Threats | Detects and Blocks Threats |
| Passive Monitoring | Inline Prevention |
| Generates Alerts | Prevents Attacks |
| No Traffic Modification | Drops or Rejects Malicious Traffic |

---

# Detection Workflow

```text
Packet

↓

Analyze

↓

Attack Detected?

↓

Yes

↓

Alert
```

IDS informs administrators of suspicious activity.

---

# Prevention Workflow

```text
Packet

↓

Analyze

↓

Attack Detected?

↓

Yes

↓

Block

↓

Drop Packet
```

IPS prevents malicious traffic from reaching the target.

---

# IDS Deployment

Typical deployment:

```text
Network

↓

Switch

↓

Mirror Port

↓

IDS
```

The IDS receives a copy of traffic for analysis without affecting production traffic.

---

# IPS Deployment

Typical deployment:

```text
Internet

↓

Firewall

↓

IPS

↓

Servers
```

All traffic passes through the IPS before reaching protected systems.

---

# Detection Methods

IDS/IPS solutions commonly use:

- Signature-Based Detection
- Anomaly-Based Detection
- Behavior-Based Detection

---

# Signature-Based Detection

Compares traffic against:

```text
Known Attack Signatures
```

Advantages:

- Accurate
- Fast
- Low False Positives

Limitation:

```text
Cannot Detect

Unknown Attacks
```

---

# Anomaly-Based Detection

Learns:

```text
Normal Network Behavior
```

Detects:

```text
Unusual Activity
```

Advantages:

- Detects Unknown Threats
- Detects Zero-Day Behaviors

Limitation:

- Higher False Positive Rate

---

# Behavior-Based Detection

Analyses user and system behaviour over time.

Examples:

- Unusual Login Times
- Unexpected Data Transfers
- Suspicious Command Execution
- Lateral Movement

---

# Network IDS (NIDS)

Monitors:

```text
Network Traffic
```

Protects:

- Entire Networks
- Data Centres
- Cloud Networks
- Branch Offices

---

# Host IDS (HIDS)

Monitors:

```text
Individual Systems
```

Checks:

- Log Files
- Processes
- File Integrity
- User Activity
- System Configuration

---

# NIDS vs HIDS

| Network IDS | Host IDS |
|-------------|----------|
| Monitors Network Traffic | Monitors Individual Hosts |
| Protects Multiple Systems | Protects Single System |
| Detects Network Attacks | Detects Local Attacks |
| Centralised Visibility | Detailed Host Visibility |

---

# Common Threats Detected

IDS/IPS solutions can identify:

- Port Scanning
- Brute Force Attacks
- Malware Activity
- SQL Injection
- Cross-Site Scripting (XSS)
- Denial of Service (DoS)
- Command Injection
- Suspicious Network Traffic

---

# Enterprise Example

```text
Internet

↓

Firewall

↓

IPS

↓

Demilitarised Zone (DMZ)

↓

Application

↓

Database
```

Traffic is inspected before reaching production systems.

---

# SOC Workflow

```text
Attack

↓

IDS Alert

↓

Security Operations Centre (SOC)

↓

Investigation

↓

Response
```

With IPS:

```text
Attack

↓

Blocked

↓

SOC Notification
```

---

# Cloud Perspective

Cloud environments support IDS/IPS through:

- Managed Threat Detection Services
- Network Security Appliances
- Virtual Firewalls
- Cloud Security Platforms

IDS/IPS helps secure:

- Virtual Machines
- Kubernetes Clusters
- APIs
- Cloud Networks

---

# Kubernetes Perspective

Kubernetes security solutions monitor:

- Network Traffic
- Container Activity
- API Requests
- Runtime Behavior

IDS/IPS complements:

- Network Policies
- Service Mesh
- Admission Controllers
- Runtime Security Tools

---

# Linux Perspective

Useful commands for investigation:

Display active connections.

```bash
ss -tun
```

Display listening ports.

```bash
ss -tuln
```

View authentication logs.

```bash
journalctl -u ssh
```

Display recent login history.

```bash
last
```

View kernel logs.

```bash
journalctl -k
```

---

# Open Source IDS/IPS Solutions

Popular tools include:

- Snort
- Suricata
- Zeek
- Wazuh (Host-based Detection)
- OSSEC

These tools are widely used in enterprise and cloud environments.

---

# Incident Response Workflow

```text
Attack

↓

Detect

↓

Alert

↓

Investigate

↓

Contain

↓

Recover

↓

Lessons Learned
```

IDS/IPS plays a critical role during the detection phase.

---

# Advantages of IDS/IPS

- Early Threat Detection
- Automated Attack Prevention
- Improved Visibility
- Security Monitoring
- Compliance Support
- Faster Incident Response

---

# Limitations

- Signature-based detection cannot identify every new threat
- Anomaly detection may generate false positives
- IPS introduces additional processing because it operates inline
- Continuous tuning is required for optimal performance

---

# Hands-on Lab

## Task 1

Display active connections.

```bash
ss -tun
```

---

## Task 2

Display listening ports.

```bash
ss -tuln
```

---

## Task 3

View SSH authentication logs.

```bash
journalctl -u ssh
```

---

## Task 4

Display recent login history.

```bash
last
```

---

## Task 5

Compare:

- IDS
- IPS

---

## Task 6

Compare:

- Network IDS
- Host IDS

---

## Task 7

Design an enterprise architecture including:

- Firewall
- IPS
- DMZ
- Internal Network
- Security Information and Event Management (SIEM)

---

## Task 8

Research:

- Snort
- Suricata
- Zeek
- Wazuh

Compare their capabilities and common deployment scenarios.

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `ss -tun` | Display active connections |
| `ss -tuln` | Display listening ports |
| `journalctl -u ssh` | Display SSH logs |
| `journalctl -k` | Display kernel logs |
| `last` | Display login history |
| `who` | Display logged-in users |

---

# Common Mistakes

❌ Assuming IDS blocks attacks.

✅ Remember IDS only detects and alerts.

---

❌ Deploying IPS without testing.

✅ Validate policies to avoid blocking legitimate traffic.

---

❌ Ignoring alerts.

✅ Review and investigate alerts promptly.

---

❌ Using only signature-based detection.

✅ Combine multiple detection techniques.

---

❌ Never updating detection rules.

✅ Keep signatures and detection engines current.

---

# Best Practices

- Deploy IDS and IPS together where appropriate.
- Keep detection signatures updated.
- Tune rules to reduce false positives.
- Integrate alerts with a SIEM.
- Monitor logs continuously.
- Regularly test detection capabilities.
- Combine IDS/IPS with firewalls and endpoint security.
- Develop and practise an incident response plan.

---

# Interview Questions

## Beginner

1. What is an IDS?
2. What is an IPS?
3. What is the difference between IDS and IPS?
4. What is Signature-Based Detection?

---

## Intermediate

1. Compare Signature-Based and Anomaly-Based Detection.
2. Compare Network IDS and Host IDS.
3. Why is an IPS deployed inline?
4. How do IDS/IPS improve enterprise security?

---

## Architect Level

1. Design an enterprise IDS/IPS architecture.
2. Explain how IDS/IPS integrates with SIEM and SOC workflows.
3. How would you reduce false positives while maintaining strong detection coverage?

---

# Summary

In this lesson, you learned:

- Intrusion Detection Systems (IDS)
- Intrusion Prevention Systems (IPS)
- Detection vs Prevention
- Signature-Based Detection
- Anomaly-Based Detection
- Network IDS
- Host IDS
- Enterprise IDS/IPS Architecture
- Linux Investigation Commands

IDS and IPS provide critical visibility and protection against cyber threats by monitoring network traffic and system activity. While IDS focuses on detecting and alerting, IPS actively blocks malicious activity before it reaches protected systems. Together with firewalls, endpoint security, and monitoring platforms, IDS/IPS forms a key component of a layered defence strategy.

---

## Key Takeaways

- **IDS detects** suspicious activity and generates alerts.
- **IPS detects and blocks** malicious traffic in real time.
- **Signature-based detection** identifies known attacks.
- **Anomaly-based detection** helps identify unknown or unusual behaviour.
- **Network IDS** monitors network traffic, while **Host IDS** monitors individual systems.
- IDS/IPS should be integrated with **firewalls, SIEM platforms, and incident response processes** for comprehensive security.

---

## What's Next?

**[Zero Trust](zero-trust.md)**

In the next lesson, you'll learn about **Zero Trust**.

You'll explore:

- What Zero Trust is
- Never Trust, Always Verify
- Identity-Based Security
- Least Privilege Access
- Continuous Verification
- Micro-Segmentation
- Enterprise Zero Trust Architecture

By the end of the lesson, you'll understand how Zero Trust replaces traditional perimeter-based security with continuous verification, strong identity controls, and least-privilege access across enterprise, cloud, and hybrid environments.
