---
title: "Networking Interview Preparation"
description: "45 curated Networking interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
difficulty: intermediate
estimated_time: "45–90 min"
author: Shaik Basha
last_updated: "2026-08-12"
category: interview
technology: networking
tags:
  - interview
  - networking
comments: false
---

{% raw %}
# Networking Interview Preparation

Curated from multiple DevOps interview sources, **deduplicated**, and edited for REBASH Academy.
Every question includes a model answer. Answer out loud first, then reveal it.
Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. Explain the difference between TCP and UDP.**

??? success "Reveal answer"
    TCP is connection-oriented and reliable -- it guarantees delivery and ordering through acknowledgments and
    retransmission, which is why I use it for anything where correctness matters more than speed, like API calls or
    database connections. UDP is connectionless and faster but doesn't guarantee delivery, so it fits use cases like DNS
    queries or metrics where an occasional dropped packet is an acceptable trade-off for lower latency.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**2. What is Port Mirroring and how does it help DevOps?**

??? success "Reveal answer"
    Port mirroring copies network traffic from one port to another for monitoring purposes without disrupting the original
    traffic flow -- I've used this for deep troubleshooting of microservice communication issues where application-level
    logs alone weren't giving enough visibility into what was actually happening on the wire.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**3. What are some best practices when configuring an Ingress Controller?**

??? success "Reveal answer"
    Always use TLS for anything public-facing, keep Ingress rules simple rather than over-engineering routing logic,
    implement monitoring and logging for troubleshooting, use annotations for controller-specific configuration like
    timeouts, and add rate limiting to protect backend services from being overwhelmed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**4. Difference between Security Groups and Network ACLs?**

??? success "Reveal answer"
    Security Groups are stateful and operate at the instance level -- return traffic is automatically allowed. Network ACLs
    are stateless and operate at the subnet level -- I have to explicitly allow both inbound and outbound traffic. I use
    security groups for day-to-day access control and NACLs for broader subnet-level rules like explicitly blocking a
    known bad IP range.

**5. Explain amazon traffic architecture how it goes to private subnet? I write diagram and explained it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**6. Question : What is your understanding of software architecture components (Load balancers, web servers, application servers, databases, and integrations)?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**7. Explain the complete request flow when using Gateway API with multiple GatewayClasses across regions. How do you prevent split-brain routing?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**8. What is a Network Virtual Appliance (NVA) in Azure?**

??? success "Reveal answer"
    An NVA is a VM that provides advanced networking functionality -- a firewall, a custom router -- beyond what native
    Azure networking constructs offer, and route tables are typically used to direct traffic through it for inspection or
    filtering.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    6
    VERSION CONTROL: GIT & GITHUB

**9. What is the difference between Public and Private IP Subnets?**

??? success "Reveal answer"
    Public IP subnets are assigned to resources that need to be reachable from the internet, like a web-facing load
    balancer. Private IP subnets are for internal resources that shouldn't be directly internet-accessible, like application
    or database tiers -- that public/private distinction is exactly how I structure VPC subnets in Terraform.

**10. What is VLSM (Variable Length Subnet Mask) and when do you use it in DevOps?**

??? success "Reveal answer"
    VLSM allows different subnet sizes within the same network rather than forcing every subnet to be identical, which is
    exactly what I need in a real VPC design -- a database tier might only need a handful of IPs while an application tier
    needs room to scale, and VLSM lets me size each appropriately instead of wasting address space.

**11. What is Round-Robin DNS and how does it benefit DevOps?**

??? success "Reveal answer"
    Round-robin DNS returns multiple IP addresses for the same domain name in rotating order, giving a simple form of
    load distribution across servers. It's a lightweight way to add resilience and spread load without needing a dedicated
    load balancer, though it lacks real health-check awareness compared to an actual load balancer.

**12. What is the difference between NAT Gateway and IGW?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**13. Can you tell me the difference between REST APIs and WebSocket APIs in API Gateway?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**14. Can you tell me the difference between NAT Gateway and Internet Gateway?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**15. Difference between NAT gateway and NAT instance?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**16. what is nodeport what are the cases we can use it?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**17. What is Web Application Firewall,?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**18. What is SSL/TLS Handshake.,?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**19. What is difference between coreDNS and kube-proxy?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**20. difference between http and https?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**21. Difference between subnet and nacl?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**22. Difference between nat gateway and internet gateway?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**23. What is Az App Gateway and how it encrypt http/https traffic?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**24. What is mean by Nat Gateway and Nat instance?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

**25. What is WAF (Web Application Firewall) and AAF (Application Access Firewall)?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Scenarios and troubleshooting

**26. Q16. During peak traffic, ingress controller is routing requests slowly. How do you debug it?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Networking, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**27. I have webapp in India and slowly users from abroad are also tyring to access it but there is latency. How would fix this issue, which service can help in reducing latency?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Networking, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**28. How would you setup DNS here?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**29. How would you manage SSL and TLS?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**30. You need to expose an application internally without using a LoadBalancer or NodePort service. How would you do it?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**31. How do you troubleshoot issues with an Ingress Controller?**

??? success "Reveal answer"
    Check the Ingress resource configuration is correct and pointing at the right Service and port, inspect the Ingress
    Controller pod's logs for errors, test connectivity directly with curl, verify DNS actually points at the controller's
    external IP, and confirm the backend Service has healthy endpoints at all.

**32. How does DNS Failover support DevOps?**

??? success "Reveal answer"
    DNS failover uses health checks to automatically redirect traffic away from an unhealthy endpoint to a backup, which
    is how I've implemented cross-region failover in Route 53 -- if the primary region's health check fails, traffic
    automatically shifts to the secondary without manual DNS changes.

## Practice questions

**33. High lat is reported between applicat ‘tion servers in different -9 i) eal ail > a ll a dh?**

??? success "Reveal answer"
    - Check public IP / DNS is correct. a NAT & Port fe acPen ds ¢
    -9 + Verify security group / firewall allows inbound traffic. ee | I
    + Check NAT / Port Forwarding rules. gy Service pining janes a -e&—
    . + Validate the service is boond to public interface (0.0.0.0). * Security group & firewall logic Internet ficrwall NAT/Router Server
    7 + Check ISP / upstream blocks. # End-to-end visibility
    @ Q:: DNS resolves but the website is still not loading. 
    -9 What's your next step? a [Boye DS ‘Alaning | Reto TATE)
    ANS: + Check HTTP(S) connectivity: curl -I https://domain.com # Application layer : (Transport (TCP)
    Fr) + Verify SSL/TLS handshake: openssl s_client -connect domain.com:443 eerie)
    + Check web server logs for errors. S.SoeZTSihawaese | scl
    + Validate load balancer health & backend availability. * Load balancer awareness | ink (etherner/nry
    -9 + Use browser dev tools / netwerk tab. * Layered investigation i Physical)
    Ore ro = = /
    1 KEY TAKEAWAY: ;
    | SNE ‘ener inant are tanya | Si ee ea : VERIQTA
    -9 \ ae ‘3 E ai Bas gaa | Observe Identify Isolate Test Fix Verify…

**34. You see intermittent connection drops between client and server. ———— ae — What would you investigate?**

??? success "Reveal answer"
    + Check network interface errors: ifconfig/ethtool or ip -s link. Knmladge of packst Ines & lateney tools | ping
    - 9 + Lock for packet loss: ping -< 100 <ip> or mtr <ip>. # Network interface metrics | mtr / traceroute
    + Check network device logs: switches/routers. # Layer 1/2/3 understanding | ae / stat 4
    9 + Verify duplex mismatch, MTU issues. * Experience with real-world issues [era
    ss leosk fer Natwers conertien. (albendenart, exzuratiir * Root cause correlation \eepdemne/. sarsthary j
    9 @ + Monitor for flapping links. <4

**35. How do you design a highly available application in the cloud?**

??? success "Reveal answer"
    + Distribute across multiple AZs. ‘ sng of AZs & fault |
    =) + Use load balancers to distribute traffic. faa | @”
    4 + Remove single points of failure. # Elimination of SPOF | 35 re pee
    r| + Implement health checks auto-recovery. aaa R j ' a = m3 !
    + Test failure scenarios regularly. SE rir: deans | eee”
    — 2 9 vat} Geen
    @

**36. How do you secure your Ingress Controller?**

??? success "Reveal answer"
    TLS on all traffic, authentication mechanisms like OAuth or JWT where appropriate, network policies restricting
    access to the controller itself, rate limiting to guard against DDoS-style abuse, and keeping the controller updated to
    the latest stable version to avoid known vulnerabilities.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    4
    INFRASTRUCTURE AS CODE: TERRAFORM &
    ANSIBLE

**37. How does CIDR notation improve IP address management in DevOps?**

??? success "Reveal answer"
    CIDR gives flexible, efficient address allocation instead of the rigid class-based system, letting me size a subnet to
    exactly what an environment needs -- a small management subnet doesn't have to waste an entire class C's worth of
    addresses the way older addressing schemes would have forced.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    4
    AWS NETWORKING QUESTIONS

**38. Load balancer throttling issues?**

??? success "Reveal answer"
    Use a structured triage: confirm blast radius, check recent changes, then gather evidence (logs, metrics, events) before changing anything.
    
    For Networking, name the first three checks you would run, what each result tells you, and when you would escalate versus roll back.
    
    Finish with prevention: monitoring/alert, guardrail, or automation that would catch this earlier.

**39. How does an Ingress Controller differ from a Load Balancer?**

??? success "Reveal answer"
    An Ingress Controller is purpose-built for HTTP/S traffic and sophisticated routing based on host or path, while a
    generic Load Balancer distributes traffic across instances and can handle traffic types beyond HTTP. In practice they
    work together -- a cloud load balancer often sits in front of the Ingress Controller, which then does the finer-grained
    routing.

**40. How do Symmetric and Asymmetric Encryption support DevOps?**

??? success "Reveal answer"
    Symmetric encryption uses one shared key and is fast, which is why it's used for bulk data encryption once a
    connection is established. Asymmetric encryption uses a public/private key pair and is slower but solves the
    key-exchange problem securely -- both work together in protocols like TLS and SSH, which I rely on constantly for
    securing data in transit.

**41. How do you mentor or support junior DevOps engineers in your team while ensuring timely project delivery?,?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**42. How will you restart http service from VM?**

??? success "Reveal answer"
    State assumptions and constraints first (scale, RTO/RPO, blast radius, cost), then outline the design.
    
    Walk through the Networking components you would use, why each is chosen, and the trade-offs you rejected (for example complexity versus resilience).
    
    Explain rollout/rollback and how you would prove the design works (tests, canary, dashboards).

**43. How do Firewall Rules apply to DevOps?**

??? success "Reveal answer"
    Firewall rules -- security groups and NACLs in cloud terms -- restrict which traffic can reach a CI/CD environment or
    production application. I use them to limit exposure, allowing only the specific ports and sources a service actually
    needs, especially tightening things down for production compared to more permissive dev environments.

**44. How does the TCP 3-Way Handshake apply to DevOps?**

??? success "Reveal answer"
    SYN, SYN-ACK, ACK establishes a connection before any data flows, and understanding it is genuinely useful for
    troubleshooting -- if a handshake never completes, I know it's a network or firewall-level block, versus a connection
    that completes but the application itself hangs, which points to an application-layer problem instead.

**45. Diff b/w Public and Private subnet?**

??? success "Reveal answer"
    Start with a precise definition in the context of Networking, then say what problem it solves.
    
    Give one concrete production example, contrast it with the closest alternative, and name a failure mode teams hit when they misuse it.
    
    Close with how you would verify it in a real environment (command, console check, or metric).

## Related

- Course: [Networking](../networking/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
