---
title: "Networking Interview Preparation"
description: "70 curated Networking interview prompts — model answers plus real interview questions collected across companies (deduplicated by topic)."
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
Answer out loud first, then reveal the model answer. Prefer judgement and verification over memorised lists.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

## Core concepts

**1. What is the OSI Model?**

??? success "Reveal answer"
    It's the 7-layer framework I use as a mental checklist for troubleshooting -- physical for raw hardware transmission,
    data link for framing and error detection, network for IP routing, transport for reliable end-to-end delivery, session for
    managing application sessions, presentation for encryption and format translation, and application for the actual
    services users interact with. When something's broken I work up that stack instead of guessing where the problem is.
    KEY POINTS TO MENTION
    • Physical, Data Link, Network, Transport, Session, Presentation, Application

**2. Explain the difference between TCP and UDP.**

??? success "Reveal answer"
    TCP is connection-oriented and reliable -- it guarantees delivery and ordering through acknowledgments and
    retransmission, which is why I use it for anything where correctness matters more than speed, like API calls or
    database connections. UDP is connectionless and faster but doesn't guarantee delivery, so it fits use cases like DNS
    queries or metrics where an occasional dropped packet is an acceptable trade-off for lower latency.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**3. What is Port Mirroring and how does it help DevOps?**

??? success "Reveal answer"
    Port mirroring copies network traffic from one port to another for monitoring purposes without disrupting the original
    traffic flow -- I've used this for deep troubleshooting of microservice communication issues where application-level
    logs alone weren't giving enough visibility into what was actually happening on the wire.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**4. What are some best practices when configuring an Ingress Controller?**

??? success "Reveal answer"
    Always use TLS for anything public-facing, keep Ingress rules simple rather than over-engineering routing logic,
    implement monitoring and logging for troubleshooting, use annotations for controller-specific configuration like
    timeouts, and add rate limiting to protect backend services from being overwhelmed.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**5. Difference between Security Groups and Network ACLs?**

??? success "Reveal answer"
    Security Groups are stateful and operate at the instance level -- return traffic is automatically allowed. Network ACLs
    are stateless and operate at the subnet level -- I have to explicitly allow both inbound and outbound traffic. I use
    security groups for day-to-day access control and NACLs for broader subnet-level rules like explicitly blocking a
    known bad IP range.

**6. What are some common features of an Ingress Controller?**

??? success "Reveal answer"
    Path-based and host-based routing, TLS termination with SSL certificate management, load balancing across
    backend Services, integration with external authentication and authorization, and rate limiting or caching for traffic
    control.
    KEY POINTS TO MENTION
    • Path/host-based routing, TLS termination, load balancing, auth integration, rate limiting/caching

**7. What is a Network Virtual Appliance (NVA) in Azure?**

??? success "Reveal answer"
    An NVA is a VM that provides advanced networking functionality -- a firewall, a custom router -- beyond what native
    Azure networking constructs offer, and route tables are typically used to direct traffic through it for inspection or
    filtering.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    6
    VERSION CONTROL: GIT & GITHUB

**8. What is the difference between Public and Private IP Subnets?**

??? success "Reveal answer"
    Public IP subnets are assigned to resources that need to be reachable from the internet, like a web-facing load
    balancer. Private IP subnets are for internal resources that shouldn't be directly internet-accessible, like application
    or database tiers -- that public/private distinction is exactly how I structure VPC subnets in Terraform.

**9. What is VLSM (Variable Length Subnet Mask) and when do you use it in DevOps?**

??? success "Reveal answer"
    VLSM allows different subnet sizes within the same network rather than forcing every subnet to be identical, which is
    exactly what I need in a real VPC design -- a database tier might only need a handful of IPs while an application tier
    needs room to scale, and VLSM lets me size each appropriately instead of wasting address space.

**10. What is Round-Robin DNS and how does it benefit DevOps?**

??? success "Reveal answer"
    Round-robin DNS returns multiple IP addresses for the same domain name in rotating order, giving a simple form of
    load distribution across servers. It's a lightweight way to add resilience and spread load without needing a dedicated
    load balancer, though it lacks real health-check awareness compared to an actual load balancer.

**11. What is DNS, and why is it important?**

??? success "Reveal answer"
    DNS resolves human-readable domain names into IP addresses, which is what makes the internet usable without
    everyone memorizing IPs. In DevOps it matters a lot beyond just browsing -- service discovery, load balancer
    failover, and CDN routing all depend on DNS behaving correctly and propagating in a predictable time.

**12. What is the difference between subnet mask 255.255.255.0 and 255.255.255.128?**

??? success "Reveal answer"
    255.255.255.0, a /24, allows 256 addresses with 254 usable hosts and is typical for a moderately sized network.
    255.255.255.128, a /25, splits that same original /24 space into two subnets of 128 addresses each, 126 usable
    hosts, which I'd use when I want two smaller isolated segments instead of one larger flat one.

**13. Can you explain what a Virtual Service is in the context of Ingress Controllers?**

??? success "Reveal answer"
    A Virtual Service, from service mesh technologies like Istio, defines finer-grained request routing, traffic splitting, and
    service-level policies within the mesh -- more advanced than what a standard Ingress resource provides, which
    handles the external entry point rather than internal service-to-service routing.

**14. What is Routing Convergence and its importance in DevOps?**

??? success "Reveal answer"
    Convergence is the time it takes for routers to synchronize their routing tables after a network change. Fast
    convergence matters for minimizing downtime during failover events in cloud networking, since a slow-converging
    network means longer periods where traffic might be dropped or misrouted after a change.

**15. What are Network Security Groups (NSGs) in Azure?**

??? success "Reveal answer"
    NSGs filter inbound and outbound traffic to Azure resources at the subnet or NIC level, acting as Azure's version of a
    virtual firewall -- functionally similar to AWS security groups, just applied slightly differently depending on whether you
    attach them to a subnet or an individual network interface.

**16. What are Supernets, and how are they different from Subnets?**

??? success "Reveal answer"
    A supernet combines several smaller networks into one larger one by reducing the subnet mask size -- the opposite
    operation from subnetting. It's useful for reducing the number of entries in a routing table when you have many
    contiguous smaller networks that can be summarized as one route.

**17. What is the role of annotations in an Ingress resource?**

??? success "Reveal answer"
    Annotations configure controller-specific behaviour beyond the standard Ingress spec -- load balancing algorithm, SSL
    settings, rate limits, custom rewrite rules -- and exactly which annotations are available depends on which Ingress
    Controller is actually implementing the resource.

**18. What is a firewall?**

??? success "Reveal answer"
    A firewall controls inbound and outbound traffic based on defined security rules, protecting systems from
    unauthorized access. In cloud environments that concept shows up as security groups and network ACLs, which I
    treat with the same seriousness as a traditional on-prem firewall.

**19. What are CIDR Blocks and how do they assist in DevOps?**

??? success "Reveal answer"
    CIDR blocks define network ranges in the IP/prefix-length format, and I use them constantly for efficient, flexible
    network segmentation in cloud VPC design -- separating dev, test, and production into distinct ranges while making
    efficient use of the available address space.

**20. What is the difference between Routing and Switching in DevOps?**

??? success "Reveal answer"
    Routing manages traffic between different networks -- important for multi-cloud or hybrid setups where traffic crosses
    network boundaries. Switching handles traffic within a single network or data centre, which matters for efficient
    intra-cluster or intra-VPC communication.

**21. What is the delegate_to directive?**

??? success "Reveal answer"
    Runs a task on a different host than the one being managed. Useful for registering DNS, 
    updating load balancers, or running commands on a bastion host. 
    - name: Register with load balancer 
     command: add_host.sh {{ inventory_hostname }} 
     delegate_to: loadbalancer.internal

**22. What is the difference between a /24 and a /30 subnet?**

??? success "Reveal answer"
    A /24, mask 255.255.255.0, gives 254 usable hosts, suitable for a general-purpose subnet. A /30, mask
    255.255.255.252, gives just 2 usable hosts, which is exactly the size I'd use for a point-to-point link where only two
    devices ever need to talk to each other directly.

**23. What is Load Balancing?**

??? success "Reveal answer"
    Load balancing distributes incoming traffic across multiple servers so no single instance is overwhelmed, and it's also
    what gives me automatic health-check-based failover -- an unhealthy instance simply stops receiving traffic without
    anyone manually intervening.

**24. What is a Subnet Mask?**

??? success "Reveal answer"
    A subnet mask defines which portion of an IP address is the network and which portion is the host, letting a large
    network be segmented into smaller, more manageable pieces -- something like 255.255.255.0 marks the first 24 bits
    as network and the rest as host.

## Scenarios and troubleshooting

**25. How do you troubleshoot issues with an Ingress Controller?**

??? success "Reveal answer"
    Check the Ingress resource configuration is correct and pointing at the right Service and port, inspect the Ingress
    Controller pod's logs for errors, test connectivity directly with curl, verify DNS actually points at the controller's
    external IP, and confirm the backend Service has healthy endpoints at all.

**26. How does DNS Failover support DevOps?**

??? success "Reveal answer"
    DNS failover uses health checks to automatically redirect traffic away from an unhealthy endpoint to a backup, which
    is how I've implemented cross-region failover in Route 53 -- if the primary region's health check fails, traffic
    automatically shifts to the secondary without manual DNS changes.

## Practice questions

**27. Cluster internal DNS is not resolving services?**

??? success "Reveal answer"
    + Check CoreDNS pods: kubectl -n kube-system get pods -l k8s-app=kube-dns * CoreDNS knowledge
    ; > + Check CoreDNS logs: kubectl -n kube-system logs <coredns-pod> * DNS troubleshooting flow
    + Verify CoreDNS configmap. * Config & logs analysis
    + Check network connectivity between pods and CoreDNS. * Networking understanding
    + Restart CoreDNS or fix upstream DNS if required. * Service availability mindset |
    =D | GD O: ingress te returning S6G/SE3 errors. What de you check? 
    ANS: + Check ingress controller logs. * Ingress flow understanding
    + Verify backend service endpoints: kubectl get endpoints <service-name> * Backend service troubleshooting
    + Check pod health and readiness probes. * Probes & endpoint awareness
    = ) + Validate service port, targetPort, and selector. * Layered debugging approach
    + Check timeouts, resource limits, and network connectivity. * Attention to details
    QY They are signals. Follow the flow, trust the data, | TROUBLESHOOTING FLOW (REMEMBER): NVERIQTA.
    = ) i eo ee ee | See Teel - ats ~ Fix + Validate nest © @verigta_
    
    2
    = VERIQTA
    = a 4…

**28. High lat is reported between applicat ‘tion servers in different -9 i) eal ail > a ll a dh?**

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

**29. You see intermittent connection drops between client and server. ———— ae — What would you investigate?**

??? success "Reveal answer"
    + Check network interface errors: ifconfig/ethtool or ip -s link. Knmladge of packst Ines & lateney tools | ping
    - 9 + Lock for packet loss: ping -< 100 <ip> or mtr <ip>. # Network interface metrics | mtr / traceroute
    + Check network device logs: switches/routers. # Layer 1/2/3 understanding | ae / stat 4
    9 + Verify duplex mismatch, MTU issues. * Experience with real-world issues [era
    ss leosk fer Natwers conertien. (albendenart, exzuratiir * Root cause correlation \eepdemne/. sarsthary j
    9 @ + Monitor for flapping links. <4

**30. How do you calculate the number of subnets and hosts in a given subnet?**

??? success "Reveal answer"
    Number of subnets is 2 to the power of the bits borrowed from the host portion, and hosts per subnet is 2 to the
    power of the remaining host bits, minus 2 to account for the network and broadcast addresses. I use this constantly
    when deciding how to size VPC subnets so I don't over- or under-allocate address space.
    KEY POINTS TO MENTION
    • Subnets = 2^n (n = borrowed bits)
    • Hosts per subnet = 2^h − 2
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026

**31. How do you design a highly available application in the cloud?**

??? success "Reveal answer"
    + Distribute across multiple AZs. ‘ sng of AZs & fault |
    =) + Use load balancers to distribute traffic. faa | @”
    4 + Remove single points of failure. # Elimination of SPOF | 35 re pee
    r| + Implement health checks auto-recovery. aaa R j ' a = m3 !
    + Test failure scenarios regularly. SE rir: deans | eee”
    — 2 9 vat} Geen
    @

**32. How do you secure your Ingress Controller?**

??? success "Reveal answer"
    TLS on all traffic, authentication mechanisms like OAuth or JWT where appropriate, network policies restricting
    access to the controller itself, rate limiting to guard against DDoS-style abuse, and keeping the controller updated to
    the latest stable version to avoid known vulnerabilities.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    1
    4
    INFRASTRUCTURE AS CODE: TERRAFORM &
    ANSIBLE

**33. How does CIDR notation improve IP address management in DevOps?**

??? success "Reveal answer"
    CIDR gives flexible, efficient address allocation instead of the rigid class-based system, letting me size a subnet to
    exactly what an environment needs -- a small management subnet doesn't have to waste an entire class C's worth of
    addresses the way older addressing schemes would have forced.
    
    The Complete DevOps Engineer Interview Guide (Exhaustive) — 2026
    
    0
    4
    AWS NETWORKING QUESTIONS

**34. After a firewall rule change, applications stopped working. ——_ x i Few: ddl eoal etd x conde?**

??? success "Reveal answer"
    « Review firewall rules (inbound/oubound). * Firewall rule evaluation skills | DROP IN-ettO OUT>
    + Check rule ordor and default deny policies. # Understanding of stateful inspection | SRC10.0.1.25 DST#10.0.2.10
    é R conntrack -L. 5 Ruliseedae Seek |
    + Test from both sides: source -> destination and reverse. s rey | Coe see ar
    -9 + Review firewall logs for denied traffic. ‘ 3 \ y

**35. How does an Ingress Controller differ from a Load Balancer?**

??? success "Reveal answer"
    An Ingress Controller is purpose-built for HTTP/S traffic and sophisticated routing based on host or path, while a
    generic Load Balancer distributes traffic across instances and can handle traffic types beyond HTTP. In practice they
    work together -- a cloud load balancer often sits in front of the Ingress Controller, which then does the finer-grained
    routing.

**36. How do Symmetric and Asymmetric Encryption support DevOps?**

??? success "Reveal answer"
    Symmetric encryption uses one shared key and is fast, which is why it's used for bulk data encryption once a
    connection is established. Asymmetric encryption uses a public/private key pair and is slower but solves the
    key-exchange problem securely -- both work together in protocols like TLS and SSH, which I rely on constantly for
    securing data in transit.

**37. How do Firewall Rules apply to DevOps?**

??? success "Reveal answer"
    Firewall rules -- security groups and NACLs in cloud terms -- restrict which traffic can reach a CI/CD environment or
    production application. I use them to limit exposure, allowing only the specific ports and sources a service actually
    needs, especially tightening things down for production compared to more permissive dev environments.

**38. How does the TCP 3-Way Handshake apply to DevOps?**

??? success "Reveal answer"
    SYN, SYN-ACK, ACK establishes a connection before any data flows, and understanding it is genuinely useful for
    troubleshooting -- if a handshake never completes, I know it's a network or firewall-level block, versus a connection
    that completes but the application itself hangs, which points to an application-layer problem instead.

**39. How do Latency and Throughput impact DevOps?**

??? success "Reveal answer"
    Latency and throughput directly shape user-perceived performance, especially in distributed systems where a single
    user request might hop across several services. I monitor both because a service can have plenty of throughput
    capacity while still delivering a poor experience due to high latency on the critical path.

**40. Why is DNS Propagation important for DevOps?**

??? success "Reveal answer"
    DNS changes don't take effect everywhere instantly -- propagation delay depends on TTLs and resolver caching. I
    plan DNS cutovers around that, lowering TTLs in advance of a planned change so the transition happens faster and
    doesn't cause a prolonged period where some users hit the old endpoint.

**41. How do you handle SSL termination with an Ingress Controller?**

??? success "Reveal answer"
    I store the TLS certificate and key in a Kubernetes Secret and reference it in the Ingress resource's tls section,
    specifying the host it applies to -- the Ingress Controller then handles decrypting HTTPS traffic at that layer before
    forwarding it to the backend Service.

**42. Why is Subnetting important in DevOps?**

??? success "Reveal answer"
    It lets me isolate environments -- dev, test, production -- from each other, allocate IP address space efficiently
    instead of wasting it, and reduce unnecessary broadcast traffic, all of which directly supports both security and
    performance in the environments I manage.

**43. Why is Network Topology important in DevOps?**

??? success "Reveal answer"
    Understanding topology -- how nodes and network paths are physically or logically arranged -- helps me design
    infrastructure that's resilient and scalable, and helps me reason about traffic flow when diagnosing latency or
    connectivity issues inside a cluster.

**44. How do VPN Tunnels aid DevOps?**

??? success "Reveal answer"
    VPN tunnels secure the connection between on-prem infrastructure and cloud environments, which is essential in
    hybrid cloud setups where sensitive traffic needs to stay encrypted and private as it crosses between two otherwise
    separate network environments.

**45. Given 192.168.1.0/24, if you borrow 2 bits for subnetting, what do you get?**

??? success "Reveal answer"
    Borrowing 2 bits gives a new mask of 255.255.255.192, or /26, which creates 4 subnets of 62 usable hosts each -- 2
    squared for subnets, 2 to the 6th minus 2 for hosts, since 6 bits remain for hosts.
    KEY POINTS TO MENTION
    • 4 subnets, 62 usable hosts each

## Real interview prompts

Additional questions reported from real DevOps / SRE interviews. Company names are omitted — practise these out loud without notes.

- I have webapp in India and slowly users from abroad are also tyring to access it but there is latency. How would fix this issue, which service can help in reducing latency?
- How does NAT gateway protect my private subnet, what concept does it use to secure the resource (same masking) = masking is protecting the private subnet ✅ (vpc)?
- Question : What is your understanding of software architecture components (Load balancers, web servers, application servers, databases, and integrations)?
- Explain the complete request flow when using Gateway API with multiple GatewayClasses across regions. How do you prevent split-brain routing?
- What happens when an user hits "www.clarify.com" how the request pass through the network ?? write a diagram and explain it to me?
- If the frontend, backend, and database are all deployed in private subnets, how can an end user access the application?
- Once you create that subnet, the instance will get created, but will it be able to communicate with the old instances?
- You need to expose an application internally without using a LoadBalancer or NodePort service. How would you do it?
- How do you mentor or support junior DevOps engineers in your team while ensuring timely project delivery?,?
- Explain amazon traffic architecture how it goes to private subnet? I write diagram and explained it?
- In which subnet are you placing your EKS cluster and which networking components have you used?
- Q16. During peak traffic, ingress controller is routing requests slowly. How do you debug it?
- Suppose we configured a load balancer but it’s not accepting HTTPS request what would you do?
- In terms of Cost optimisation which one should we use, Az App gateway or network gateway?
- Can you tell me the difference between REST APIs and WebSocket APIs in API Gateway?
- How to desgin an web appl handle flucting low latency and how traffice flow in it?
- Tell me the flow of network packets starting from user hit the application url?
- What is WAF (Web Application Firewall) and AAF (Application Access Firewall)?
- Create multiple subnets for different layers (bastion, application, database)?
- If I don't specify TargetPort in the service object, what is it going to do?
- How to provide HTTPS access to an application hosted in a private subnet?
- Can you tell me the difference between NAT Gateway and Internet Gateway?
- Q10. If NACL denies a CIDR, but SG allows same IP, can the IP access LB?
- Which App gateway setting is used to upload SSL certification and why?
- How you will direct traffic to and from a instance in private subnet?

## Related

- Course: [Networking](../networking/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
