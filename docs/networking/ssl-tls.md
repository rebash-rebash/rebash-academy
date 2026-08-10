---
title: "SSL/TLS"
description: "Learn TLS — SSL vs TLS, HTTPS, handshake, digital certificates, PKI, mutual TLS (mTLS), and Linux openssl diagnostics."
difficulty: beginner
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
  - tls
  - https
  - certificates
  - pki
  - rebash-networking-mastery
comments: false
status: ready
---

# SSL/TLS (Secure Sockets Layer / Transport Layer Security) — Securing Communication on the Internet

> **SSL/TLS** is a family of cryptographic protocols that provides **secure communication over computer networks** by ensuring **confidentiality, integrity, and authentication**. While **Secure Sockets Layer (SSL)** is now obsolete, its successor **Transport Layer Security (TLS)** is the modern standard used to secure websites, APIs, email, Virtual Private Networks (VPNs), cloud applications, Kubernetes services, and countless Internet-based systems. Every Linux administrator, DevOps engineer, Cloud Architect, Platform Engineer, Site Reliability Engineer (SRE), and Network Engineer should understand how TLS protects modern applications.

---

## Learning Path

<div class="ra-lesson-meta" markdown>

<p class="ra-lesson-meta__crumb" markdown>**Networking Mastery** → Module 8: Network Security → Lesson 3</p>

<div class="ra-meta-grid" markdown>

<div markdown>**Difficulty:** Beginner</div>

<div markdown>**Reading Time:** 120 Minutes</div>

</div>

</div>

<div class="ra-course-progress" markdown>

**Course Progress**

<div class="ra-meta-grid" markdown>

<div markdown>**Course:** Networking Mastery</div>

<div markdown>**Module:** Network Security</div>

<div markdown>**Lesson:** 3 of 9</div>

</div>

</div>

---

# What You'll Learn

After completing this lesson, you'll be able to:

- Understand SSL and TLS
- Learn why SSL was replaced by TLS
- Understand TLS encryption
- Learn the TLS handshake
- Understand Digital Certificates
- Learn Public Key Infrastructure (PKI)
- Apply TLS in enterprise and cloud environments

---

# Prerequisites

Complete:

- [VPN](vpn-and-tunneling-basics.md)
- [IPSec](ipsec.md)

---

# Why Learn SSL/TLS?

Imagine accessing:

```text
https://bank.com
```

Without TLS:

```text
Browser

↓

Internet

↓

Bank Server
```

Anyone intercepting traffic may read sensitive information.

With TLS:

```text
Browser

↓

Encrypted Connection

↓

Bank Server
```

Sensitive information remains protected during transmission.

---

# What is SSL/TLS?

**SSL/TLS** is a protocol that secures communication between two systems.

It provides:

- Encryption
- Authentication
- Data Integrity

TLS operates above the transport layer and is commonly used with Transmission Control Protocol (TCP)-based applications.

---

# SSL vs TLS

SSL is the predecessor to TLS.

| SSL | TLS |
|-----|-----|
| Older Protocol | Modern Standard |
| Obsolete | Secure and Actively Maintained |
| Vulnerable to Known Attacks | Improved Security |
| Should Not Be Used | Recommended for Production |

Today, organisations should use **TLS** rather than SSL.

---

# Why Use TLS?

TLS protects:

- Websites
- REST APIs
- Email
- Cloud Applications
- Kubernetes Services
- Databases

It prevents:

- Eavesdropping
- Data Tampering
- Impersonation

---

# HTTPS

HTTP sends data in plain text.

```text
HTTP

↓

Unencrypted
```

HTTPS combines:

```text
HTTP

+

TLS
```

Result:

```text
Encrypted Communication
```

Default HTTPS port:

```text
TCP 443
```

---

# TLS Architecture

```text
Application

↓

TLS

↓

TCP

↓

IP

↓

Network
```

TLS encrypts application data before it is transmitted.

---

# TLS Security Services

TLS provides:

- Confidentiality
- Integrity
- Authentication

---

# Confidentiality

Confidentiality ensures:

```text
Only

Authorized Parties

Can Read Data
```

Encryption protects transmitted information.

---

# Integrity

Integrity ensures:

```text
Data

Not Modified

In Transit
```

If data changes unexpectedly, the receiving system detects it.

---

# Authentication

Authentication verifies:

```text
Server Identity
```

Clients can confirm they are communicating with the intended server.

Mutual TLS (mTLS) can also authenticate clients.

---

# TLS Handshake

Before encrypted communication begins:

```text
Client

↓

Server

↓

Negotiate Security

↓

Exchange Keys

↓

Secure Connection
```

This process is called the:

```text
TLS Handshake
```

---

# Simplified TLS Handshake

```text
Client Hello

↓

Server Hello

↓

Certificate

↓

Key Exchange

↓

Session Keys

↓

Encrypted Communication
```

Both sides negotiate supported protocol versions and cryptographic algorithms before exchanging encrypted application data.

---

# Session Keys

After the handshake:

```text
Symmetric Session Key

Created
```

All application traffic uses this symmetric key because it is much faster than public-key encryption for ongoing communication.

---

# Digital Certificates

Servers prove their identity using:

```text
Digital Certificate
```

A certificate contains:

- Domain Name
- Public Key
- Issuing Certificate Authority (CA)
- Validity Period
- Digital Signature

---

# Certificate Authority (CA)

A:

```text
Certificate Authority
```

is a trusted organisation that issues and signs digital certificates.

Examples include public CAs trusted by operating systems and web browsers, as well as private enterprise CAs.

---

# Public Key Infrastructure (PKI)

PKI consists of:

- Certificate Authorities
- Certificates
- Public Keys
- Private Keys
- Trust Chains

PKI enables secure identity verification across distributed systems.

---

# Public Key vs Private Key

Every certificate is associated with a key pair.

Public Key:

```text
Shared

Publicly
```

Private Key:

```text
Secret

Never Shared
```

The private key must always remain protected.

---

# Certificate Validation

The client verifies:

- Certificate Signature
- Certificate Expiration
- Domain Name
- Trusted Certificate Chain

If validation fails:

```text
Connection

Rejected
```

---

# Mutual TLS (mTLS)

Standard TLS authenticates:

```text
Server
```

Mutual TLS authenticates:

```text
Client

AND

Server
```

mTLS is widely used in:

- Microservices
- Kubernetes
- Service Mesh
- Enterprise APIs

---

# Enterprise Example

```text
Browser

↓

HTTPS

↓

Load Balancer

↓

Application

↓

Database
```

TLS protects communication between the client and the application endpoint. Internal services may also use TLS depending on the architecture.

---

# API Example

```text
Client

↓

HTTPS

↓

REST API
```

API authentication tokens travel through an encrypted TLS connection.

---

# Cloud Perspective

Cloud providers support TLS for:

- Load Balancers
- API Gateways
- Managed Databases
- Kubernetes Ingress
- Storage Services

TLS certificates are commonly managed through cloud certificate services.

---

# Kubernetes Perspective

TLS secures:

- Kubernetes API Server
- Ingress Controllers
- Admission Webhooks
- Service Mesh Communication

Many service mesh platforms use **mTLS** to automatically encrypt communication between services.

---

# Linux Perspective

View TLS certificates.

```bash
openssl x509 -in certificate.crt -text -noout
```

Check certificate expiration.

```bash
openssl x509 -enddate -noout -in certificate.crt
```

Test HTTPS connection.

```bash
openssl s_client -connect example.com:443
```

Display listening HTTPS ports.

```bash
ss -tuln
```

---

# TLS Packet Flow

```text
Client

↓

TLS Handshake

↓

Encrypted Session

↓

Server
```

---

# Advantages of TLS

- Strong Encryption
- Authentication
- Data Integrity
- Widely Supported
- High Performance
- Essential for Modern Applications

---

# Limitations

- Certificate management requires operational discipline
- Expired certificates cause service outages
- Incorrect configuration can weaken security
- TLS does not protect applications from all attack types

---

# Hands-on Lab

## Task 1

Display HTTPS listening ports.

```bash
ss -tuln
```

---

## Task 2

View a certificate.

```bash
openssl x509 -in certificate.crt -text -noout
```

---

## Task 3

Check certificate expiration.

```bash
openssl x509 -enddate -noout -in certificate.crt
```

---

## Task 4

Test a TLS connection.

```bash
openssl s_client -connect example.com:443
```

---

## Task 5

Compare:

- SSL
- TLS

---

## Task 6

Draw a TLS handshake.

Include:

- Client Hello
- Server Hello
- Certificate
- Key Exchange
- Secure Session

---

## Task 7

Draw a PKI architecture.

Include:

- Client
- Certificate Authority
- Server
- Certificate

---

## Task 8

Research TLS implementations in:

- Linux
- NGINX
- Apache
- Kubernetes Ingress
- Cloud Load Balancers

---

# Linux Commands

| Command | Purpose |
|----------|----------|
| `openssl x509 -text -noout` | Display certificate details |
| `openssl x509 -enddate -noout` | Display certificate expiration |
| `openssl s_client -connect host:443` | Test TLS connection |
| `ss -tuln` | Display listening ports |
| `curl -v https://host` | Verify HTTPS connectivity |

---

# Common Mistakes

❌ Using obsolete SSL versions.

✅ Use modern TLS versions only.

---

❌ Ignoring certificate expiration.

✅ Monitor and renew certificates before they expire.

---

❌ Using self-signed certificates in production without appropriate trust configuration.

✅ Use certificates issued by a trusted CA or an enterprise PKI.

---

❌ Exposing private keys.

✅ Protect private keys with strict permissions and secure storage.

---

❌ Weak TLS configuration.

✅ Disable insecure protocols and cipher suites.

---

# Best Practices

- Use modern TLS versions.
- Disable obsolete SSL and legacy TLS versions.
- Use strong cipher suites.
- Automate certificate renewal.
- Protect private keys.
- Monitor certificate expiration.
- Enable mTLS for service-to-service communication where appropriate.
- Regularly test TLS configurations.

---

# Interview Questions

## Beginner

1. What is TLS?
2. What is the difference between SSL and TLS?
3. What is HTTPS?
4. What is a Digital Certificate?

---

## Intermediate

1. Explain the TLS handshake.
2. What is PKI?
3. What is the role of a Certificate Authority?
4. What is Mutual TLS?

---

## Architect Level

1. Design a secure TLS architecture for a production web application.
2. Explain certificate lifecycle management.
3. How would you troubleshoot TLS handshake failures?

---

# Summary

In this lesson, you learned:

- SSL
- TLS
- HTTPS
- TLS Handshake
- Digital Certificates
- Certificate Authorities
- Public Key Infrastructure (PKI)
- Mutual TLS (mTLS)
- Enterprise TLS Deployments
- Linux TLS Commands

TLS is the foundation of secure communication on today's Internet. It protects websites, APIs, cloud services, email systems, and enterprise applications by providing encryption, authentication, and data integrity. Combined with proper certificate management and modern cryptographic practices, TLS enables secure communication across enterprise, cloud, and Kubernetes environments.

---

## Key Takeaways

- **TLS** is the modern replacement for SSL.
- TLS provides **confidentiality, integrity, and authentication**.
- HTTPS is **HTTP protected by TLS**.
- The **TLS handshake** establishes a secure encrypted session.
- **Digital certificates** verify server identities.
- **PKI** enables trusted certificate management.
- **Mutual TLS (mTLS)** authenticates both clients and servers.
- TLS is essential for securing modern web applications, APIs, and cloud services.

---

## What's Next?

**[SSH](ssh-networking.md)**

In the next lesson, you'll learn about **SSH (Secure Shell)**.

You'll explore:

- What SSH is
- SSH Architecture
- Public Key Authentication
- Password vs Key-Based Authentication
- SSH Tunneling
- SSH Agent
- SSH Security Best Practices

By the end of the lesson, you'll understand how SSH securely manages Linux servers, network devices, and cloud infrastructure while replacing insecure remote access protocols such as Telnet.
