---
title: Network Security Hardening
description: Apply zero trust principles, network segmentation, DDoS mitigation, TLS best practices, and audit logging for production network defense.
difficulty: advanced
estimated_time: "50 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - security
  - zero-trust
  - segmentation
  - ddos
  - tls
  - audit-logging
  - hardening
prerequisites:
  - VPN and Tunneling Basics (Tutorial 18)
  - Firewalls, VPC design, HTTPS/TLS fundamentals, and load balancing concepts
  - Familiarity with Linux system administration
comments: false
---

# Network Security Hardening

## Overview

Network security is not a product you install once — it is a **continuous discipline** of reducing attack surface, enforcing least privilege, detecting anomalies, and responding to incidents. The perimeter firewall model ("trust everything inside the castle") collapsed as cloud, remote work, and microservices distributed workloads beyond the data center edge. Modern organizations adopt **zero trust** (never trust, always verify), **network segmentation** (limit lateral movement), **DDoS mitigation** (absorb and scrub attack traffic), **TLS best practices** (encrypt and authenticate every connection), and **audit logging** (prove who did what, when, for compliance and forensics).

This tutorial teaches production network hardening for DevOps and SRE teams: how to segment tiers, configure TLS correctly, deploy WAF and DDoS protection layers, and build audit trails that satisfy SOC 2, PCI-DSS, and internal security reviews. You will audit a sample environment, implement segmentation rules, and evaluate TLS configurations with industry-standard tools.

This is **Tutorial 19** in **Module 6: Cloud & Advanced** of the REBASH Academy Networking series. It follows our [documentation standards](../about.md#documentation-standards) with theory, hands-on labs, and interview preparation.

## Prerequisites

- Completed [VPN and Tunneling Basics](vpn-and-tunneling-basics.md) and Module 4–6 networking tutorials
- Understanding of firewalls, security groups, VPC design, and HTTPS/TLS handshake
- Access to a Linux system and optionally a cloud account with WAF/Shield capabilities
- Basic familiarity with certificate concepts (CA, SAN, chain of trust)
- Recommended: [Firewalls and Access Control](firewalls-and-access-control.md) and [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain zero trust networking principles and how they differ from perimeter security
- [ ] Design network segmentation for multi-tier applications in cloud VPCs
- [ ] Describe DDoS attack types and mitigation strategies at each OSI layer
- [ ] Apply TLS best practices including cipher selection, certificate management, and HSTS
- [ ] Configure audit logging for network devices, firewalls, and cloud flow logs
- [ ] Evaluate TLS configurations using testssl.sh or SSL Labs
- [ ] Build a network hardening checklist for production deployments

## Architecture Diagram

The diagram shows defense-in-depth layers: DDoS scrubbing at the edge, WAF for application attacks, segmented VPC tiers, and centralized audit logging.

```mermaid
flowchart TB
    subgraph Internet
        Attacker["Attackers / Bots"]
        Users[Legitimate Users]
    end

    subgraph Edge["Edge Protection"]
        DDoS["DDoS Mitigation<br/>Shield / Cloudflare / WAF"]
        WAF[Web Application Firewall]
        LB[Load Balancer — TLS termination]
    end

    subgraph VPC["Segmented VPC"]
        subgraph DMZ["Public Tier"]
            Proxy["Reverse Proxy / Ingress"]
        end
        subgraph AppTier["Application Tier — Private"]
            App["App Servers<br/>SG: 443 from DMZ only"]
        end
        subgraph DataTier["Data Tier — Private"]
            DB["(Database<br/>SG: 5432 from App only")]
        end
    end

    subgraph Observability["Audit & Monitoring"]
        Flow[VPC Flow Logs]
        SIEM["SIEM / CloudWatch / Splunk"]
    end

    Attacker --> DDoS
    Users --> DDoS
    DDoS --> WAF --> LB --> Proxy
    Proxy --> App
    App --> DB
    Flow --> SIEM
    LB --> SIEM```

## Theory

### Zero Trust Networking — Introduction

**Zero trust** assumes no user, device, or network segment is inherently trustworthy — regardless of whether traffic originates inside or outside the corporate network. Core principles (NIST SP 800-207):

1. **Verify explicitly** — authenticate and authorize every access request using all available data points (identity, device health, location, behavior)
2. **Use least privilege access** — grant minimum permissions required; just-in-time (JIT) access for admin tasks
3. **Assume breach** — design for lateral movement containment; segment networks; monitor continuously

Zero trust is not a single product. It combines identity (MFA, SSO), device trust, network micro-segmentation, application mTLS, data encryption, and continuous visibility through SIEM correlation.

For network engineers, zero trust means **eliminating implicit trust based on IP address alone**. A database in a "private" subnet still requires authentication, encryption, and explicit firewall rules — not just obscurity.

### Network Segmentation

**Segmentation** divides a network into isolated zones with controlled communication between them. Goals:

- **Limit blast radius** — compromise of a web server does not expose the database directly
- **Compliance** — PCI-DSS requires cardholder data environment (CDE) isolation
- **Policy enforcement** — apply different security controls per tier

Cloud segmentation patterns:

| Pattern | Implementation | Use case |
|---------|----------------|----------|
| **Tier-based** | Public / app / data subnets with SG rules | Three-tier web apps |
| **Environment-based** | Separate VPCs or accounts for prod/staging | Prevent staging → prod access |
| **Service-based** | Security group per microservice | Kubernetes NetworkPolicy |
| **Micro-segmentation** | Host-level firewall + identity-aware proxy | Zero trust east-west traffic |

Example security group rules for a three-tier app:

| Source | Destination | Port | Purpose |
|--------|-------------|------|---------|
| 0.0.0.0/0 | ALB (public) | 443 | User HTTPS |
| ALB SG | App SG | 8080 | Proxy to application |
| App SG | DB SG | 5432 | Application to PostgreSQL |
| Bastion/VPN SG | App SG | 22 | Emergency SSH (restrict source IP) |

**Network ACLs (NACLs)** add stateless subnet-level rules as a second layer. Use NACLs for explicit deny lists (block known malicious IP ranges) while security groups handle stateful allow rules.

### DDoS Mitigation Basics

**Distributed Denial of Service (DDoS)** attacks overwhelm targets with traffic volume (volumetric), protocol exploitation (SYN floods), or application-layer requests (HTTP floods). Mitigation strategies by layer:

| Attack type | Layer | Mitigation |
|-------------|-------|------------|
| UDP/ICMP flood | L3/L4 | Rate limiting, BGP blackholing, scrubbing centers |
| SYN flood | L4 | SYN cookies, connection limits, AWS Shield |
| HTTP flood | L7 | WAF rate rules, CAPTCHA, CDN caching, autoscaling |
| DNS amplification | L3/L4 | Response Rate Limiting (RRL), BCP 38 egress filtering |
| Slowloris | L7 | Connection timeouts, reverse proxy buffering |

Cloud provider DDoS services:

| Provider | Service | Notes |
|----------|---------|-------|
| AWS | Shield Standard (free), Shield Advanced ($) | Auto-protects ALB, CloudFront, Route 53 |
| GCP | Cloud Armor + Google Cloud CDN | Adaptive protection, WAF rules |
| Azure | DDoS Network Protection | Basic (free) and Standard tiers |
| Third-party | Cloudflare, Akamai, Fastly | Anycast scrubbing, always-on or on-demand |

**Best practice:** place public endpoints behind a CDN or DDoS-protected load balancer. Never expose raw EC2 public IPs for production web services. Maintain a **DDoS runbook** with escalation contacts and communication templates.

### TLS Best Practices

Transport Layer Security (TLS) encrypts data in transit and authenticates server identity (and optionally client identity via mTLS). Production TLS requirements:

**Protocol versions:**

- **TLS 1.3** — preferred; faster handshake, removes weak cipher suites
- **TLS 1.2** — minimum acceptable for most compliance frameworks
- **TLS 1.0/1.1, SSLv3** — disable everywhere

**Cipher suites (TLS 1.2):**

- Prefer **AEAD** ciphers: `TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384`, `TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256`
- Enable **Forward Secrecy** via ECDHE key exchange
- Disable RSA key transport, 3DES, RC4, NULL ciphers

**Certificate management:**

- Use certificates from trusted public CAs (Let's Encrypt, DigiCert) or internal PKI for mTLS
- Include all domain names in **Subject Alternative Names (SAN)**
- Automate renewal (cert-manager on Kubernetes, ACM on AWS, certbot on VMs)
- Monitor expiration — alert at 30, 14, and 7 days before expiry

**HTTP security headers (complement TLS):**

| Header | Purpose |
|--------|---------|
| `Strict-Transport-Security` | Force HTTPS (HSTS) — `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | Restrict resource loading — mitigates XSS |
| `X-Content-Type-Options: nosniff` | Prevent MIME sniffing |
| `X-Frame-Options: DENY` | Clickjacking protection |

**mTLS (mutual TLS):** both client and server present certificates. Use for service-to-service communication in zero trust architectures (Istio, Linkerd, AWS App Mesh).

### Audit Logging

Audit logs provide **non-repudiation** — proof of who accessed what, when, and from where. Required for SOC 2, PCI-DSS, HIPAA, and incident response.

| Source | What to log | Destination |
|--------|-------------|-------------|
| VPC Flow Logs | Accept/reject, src/dst IP, port, bytes | S3, CloudWatch, SIEM |
| Firewall / SG changes | API calls creating/modifying rules | CloudTrail, Azure Activity Log |
| Load balancer access logs | HTTP requests, status codes, client IP | S3, BigQuery |
| WAF logs | Blocked requests, rule matches | CloudWatch, Splunk |
| DNS query logs | Resolver queries | S3, security analytics |
| VPN connection logs | Tunnel up/down, authentication events | CloudWatch, syslog |
| Linux host | auth.log, auditd (syscall-level) | Centralized logging stack |

**Audit logging best practices:**

- **Centralize** — ship logs to immutable storage (S3 Object Lock, WORM)
- **Correlate** — use SIEM to connect flow logs with application logs and identity events
- **Retain** — match compliance requirements (PCI: 1 year online, 3 months immediately available)
- **Alert** — security group `0.0.0.0/0` on port 22, WAF spike in blocks, VPN auth failures

## Hands-on Lab

Complete these steps on a Linux system. Run TLS tests against domains you own or public reference sites.

### Step 1 – Audit open ports on a Linux host

**Command:**

```bash
sudo ss -tulpn
sudo iptables -L -n -v 2>/dev/null || sudo nft list ruleset 2>/dev/null | head -40
```

**Explanation:** Inventory listening services before hardening. Every open port is attack surface. Document expected listeners and close or firewall everything else.

**Expected output:**

```text
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*     sshd
tcp   LISTEN 0      511          0.0.0.0:80         0.0.0.0:*     nginx
```

Flag `0.0.0.0:22` — SSH open to all interfaces. Restrict to bastion/VPN CIDR in production.

### Step 2 – Implement host firewall (nftables)

**Command:**

```bash
sudo tee /etc/nftables.conf <<'EOF'
#!/usr/sbin/nft -f
flush ruleset

table inet filter {
  chain input {
    type filter hook input priority filter; policy drop;
    ct state established,related accept
    iif "lo" accept
    tcp dport 22 ip saddr 10.0.1.0/24 accept comment "SSH from bastion subnet"
    tcp dport { 80, 443 } accept comment "HTTP/S public"
    icmp type echo-request limit rate 5/second accept
  }
  chain forward {
    type filter hook forward priority filter; policy drop;
  }
}
EOF

sudo systemctl enable --now nftables
sudo nft list ruleset
```

**Explanation:** Default **drop** policy denies unexpected traffic. Explicit allows for SSH (restricted source), HTTP/S, and established connections.

### Step 3 – Evaluate TLS configuration with testssl.sh

**Command:**

```bash
git clone --depth 1 https://github.com/drwetter/testssl.sh.git /tmp/testssl.sh
/tmp/testssl.sh/testssl.sh --quiet --severity HIGH https://example.com | head -30
```

**Explanation:** testssl.sh checks protocol support, cipher suites, certificate chain, HSTS, and known vulnerabilities. Run against your own domains only.

**Expected output (healthy site):**

```text
 Testing protocols
 SSLv2      not offered (OK)
 SSLv3      not offered (OK)
 TLS 1.0    not offered (OK)
 TLS 1.1    not offered (OK)
 TLS 1.2    offered (OK)
 TLS 1.3    offered (OK)
```

### Step 4 – Inspect certificate details with OpenSSL

**Command:**

```bash
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
  openssl x509 -noout -text | grep -E "Subject:|DNS:|Not After|Public-Key"
```

**Explanation:** Inspect SAN entries, expiration, and key size (2048-bit RSA minimum; 4096 or ECDSA P-256 preferred). Automate renewal via certbot or cert-manager.

### Step 5 – Configure nginx TLS hardening

**Command:**

```bash
sudo tee /etc/nginx/snippets/tls-params.conf <<'EOF'
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options nosniff always;
add_header X-Frame-Options DENY always;
EOF

sudo nginx -t && sudo systemctl reload nginx
```

**Explanation:** TLS 1.2+ only, modern cipher suites, OCSP stapling, HSTS for transport enforcement. Mozilla SSL Configuration Generator provides updated templates.

### Step 6 – Enable VPC Flow Logs (AWS)

**Command:**

```bash
LOG_GROUP="/aws/vpc/flowlogs/lab-vpc"
aws logs create-log-group --log-group-name "$LOG_GROUP" 2>/dev/null || true

aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids "$VPC_ID" \
  --traffic-type REJECT \
  --log-destination-type cloud-watch-logs \
  --log-group-name "$LOG_GROUP" \
  --deliver-logs-permission-arn "$ROLE_ARN"
```

**Explanation:** Start with **REJECT** traffic logging — rejected packets often indicate scanning or misconfigured SGs. Expand to ALL traffic for forensics when storage budget allows.

### Step 7 – Configure auditd for network syscalls

**Command:**

```bash
sudo apt-get install -y auditd
sudo tee -a /etc/audit/rules.d/network.rules <<'EOF'
-a always,exit -F arch=b64 -S connect -k network_connect
-a always,exit -F arch=b64 -S bind -k network_bind
EOF

sudo augenrules --load
sudo ausearch -k network_connect --start recent | tail -10
```

**Explanation:** auditd logs syscalls for compliance and forensics. Pair with centralized log shipping (Fluent Bit, Vector) for production SIEM correlation.

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `ss -tulpn` | List listening TCP/UDP ports | `sudo ss -tulpn` |
| `nft list ruleset` | Show nftables firewall rules | `sudo nft list ruleset` |
| `testssl.sh` | Evaluate TLS configuration | `testssl.sh https://example.com` |
| `openssl s_client` | Manual TLS handshake test | `openssl s_client -connect example.com:443 -tls1_2` |
| `aws ec2 create-flow-logs` | Enable VPC flow logging | See lab Step 6 |
| `aws ec2 describe-security-groups` | Audit SG rules | `aws ec2 describe-security-groups --group-ids sg-xxx` |

## Common Mistakes

!!! warning "Security groups allowing 0.0.0.0/0 on admin ports"
    SSH (22), RDP (3389), and database ports (5432, 3306) open to the internet are the most common cloud breach vectors. Restrict to bastion, VPN, or SSM Session Manager CIDR ranges.

!!! warning "TLS termination with weak ciphers downstream"
    Terminating TLS at the load balancer then sending plaintext HTTP to backends exposes traffic to anyone with VPC access. Use HTTPS or mTLS on backend connections.

!!! warning "No log retention or centralized aggregation"
    Logs stored only on the compromised host are useless for forensics. Ship to centralized, immutable storage from day one.

!!! warning "Ignoring certificate expiration"
    Expired certificates cause outages and teach users to click through warnings. Automate renewal and alert weeks before expiry.

## Best Practices

!!! tip "Implement defense in depth"
    Layer DDoS protection, WAF, security groups, NACLs, host firewall, and application auth — no single control is sufficient.

!!! tip "Default deny everywhere"
    Explicitly allow required traffic only. AWS security groups and nftables default-deny patterns enforce this. Document every allow rule with ticket reference.

!!! tip "Use AWS WAF managed rule groups"
    AWSManagedRulesCommonRuleSet and KnownBadInputs block common attacks. Enable count mode first, then block.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| TLS handshake failure | Protocol/cipher mismatch; expired cert | Align client/server TLS versions; renew certificate |
| HSTS breaks dev subdomains | includeSubDomains on wildcard cert | Use separate cert strategy; shorter max-age in non-prod |
| Flow logs missing REJECT entries | Wrong traffic-type filter; IAM role | Set `--traffic-type ALL` or REJECT; verify log delivery role |
| WAF blocking legitimate traffic | Aggressive OWASP rules | Switch to count mode; tune exclusions for false positives |
| auditd not logging | Rules not loaded; disk full | Run `augenrules --load`; check audit log space |

## Summary

- **Zero trust** eliminates implicit network trust — verify every request with identity, device, and context
- **Network segmentation** limits lateral movement via tier-based subnets, security groups, and micro-segmentation
- **DDoS mitigation** combines edge scrubbing, rate limiting, WAF, and autoscaling — never expose raw instances
- **TLS best practices** require TLS 1.2+ (prefer 1.3), strong ciphers, automated cert renewal, and HSTS
- **Audit logging** via flow logs, firewall logs, WAF logs, and host audit trails enables compliance and forensics
- **Defense in depth** layers multiple controls — perimeter-only security fails in cloud and remote-work environments
- Regular **automated audits** of security groups, TLS configs, and open ports prevent configuration drift

## Interview Questions

1. What is zero trust networking, and how does it differ from the traditional perimeter model?
2. Explain network segmentation and give an example for a three-tier web application.
3. What are the three categories of DDoS attacks, and how do you mitigate each?
4. What TLS versions and cipher properties should production systems enforce?
5. What is HSTS, and why does it matter?
6. What is mTLS, and when would you use it?
7. What should VPC flow logs capture, and where should you store them?
8. How do security groups and NACLs differ in AWS?

??? tip "Sample Answers (Questions 1 and 4)"

    **Q1 — Zero trust vs perimeter:** Traditional perimeter security trusts all traffic inside the corporate network/firewall. Zero trust assumes breach — every access request is verified regardless of source IP. Identity (MFA), device posture, least privilege, micro-segmentation, and continuous monitoring replace "inside = trusted."

    **Q4 — TLS requirements:** Minimum TLS 1.2; prefer TLS 1.3. Require forward secrecy (ECDHE). Use AEAD ciphers (AES-GCM, ChaCha20-Poly1305). Disable TLS 1.0/1.1 and weak ciphers. Automate certificate renewal and enable HSTS.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [VPN and Tunneling Basics](vpn-and-tunneling-basics.md) *(previous in Module 6)*
- [Network Automation and Monitoring](network-automation-and-monitoring.md) *(next in Module 6)*
- [Firewalls and Access Control](firewalls-and-access-control.md)
- [Linux – Category Overview](../linux/index.md)

## References

- [NIST SP 800-207 — Zero Trust Architecture](https://csrc.nist.gov/publications/detail/sp/800-207/final)
- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [testssl.sh — TLS testing tool](https://testssl.sh/)
