---
title: "Networking Interview Preparation"
description: "40 curated Networking interview questions with model answers — deduplicated from DevOps / SRE sources and edited for clear practise."
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
Answers are written to scan fast: punchline → bullets → commands → trap.

!!! tip "How to practise"
    1. Answer in two minutes without notes
    2. Name the first three commands or checks you would run
    3. Call out a failure mode and a rollback
    4. Tie the answer to least privilege and blast radius

<div class="ra-interview-qa" markdown="1">

## Core concepts

**1. Explain the difference between TCP and UDP.**

??? success "Reveal answer"
    **In short:** TCP is the reliable courier; UDP is the shout across the room — pick by whether loss or latency hurts more.
    
    **Key points**
    
    - **TCP** — connection-oriented: handshake, ACK, retransmission, ordered byte stream
    - **UDP** — connectionless datagrams: no handshake, no retry, lower overhead
    - **Choose TCP** — APIs, databases, SSH, file transfer
    - **Choose UDP** — DNS, VoIP, gaming, metrics where stale beats late
    
    **Try this**
    
    ```bash
    ss -lntp
    ss -lnup
    ```
    
    **Trap**
    
    - Calling UDP “unreliable so useless” — many production systems need its speed

**2. What is Port Mirroring and how does it help DevOps?**

??? success "Reveal answer"
    **In short:** Port mirroring (SPAN/TAP) copies live packets to a watch port so you can see truth without sitting in the path.
    
    **Key points**
    
    - **What** — source port/VLAN traffic cloned to IDS, NPM, or packet broker
    - **Why DevOps** — catch TLS failures, asymmetric routes, noisy neighbours metrics miss
    - **Inline vs tap** — mirroring adds almost no latency; inline proxies can
    - **Cloud cousins** — VPC Traffic Mirroring / packet capture on NICs
    
    **Try this**
    
    ```bash
    tcpdump -i any port 443 -c 20 -nn
    ```
    
    **Trap**
    
    - Mirroring encrypted traffic without keys — you see sizes and timing, not HTTP bodies

**3. What are some best practices when configuring an Ingress Controller?**

??? success "Reveal answer"
    **In short:** Treat Ingress as your public front door: TLS, limits, logs, and RBAC — not a dump of every Service.
    
    **Key points**
    
    - **TLS** — terminate with cert-manager or managed certs; force HTTPS redirect
    - **Limits** — timeouts, body size, rate limits; avoid catch-all hosts
    - **Observability** — access logs + Prometheus metrics; readiness-aligned upstreams
    - **Tenancy** — separate IngressClasses; RBAC who may create Ingress
    - **GitOps** — pin controller chart/version and values in Git
    
    **Try this**
    
    ```bash
    kubectl get ingress -A
    kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=50
    curl -vI https://host/path
    ```
    
    **Trap**
    
    - Putting TLS private keys or secrets in annotations anyone can read

**4. Difference between Security Groups and Network ACLs?**

??? success "Reveal answer"
    **In short:** Security Groups are stateful ENI firewalls; NACLs are stateless subnet filters that remember nothing.
    
    **Key points**
    
    - **SG** — instance/ENI level; allow-only; return traffic automatic
    - **NACL** — subnet level; allow and deny; numbered rules, first match wins
    - **State** — NACL needs both inbound and outbound (incl. ephemeral ports)
    - **Default use** — SGs for app policy; NACLs for coarse subnet guardrails
    
    **Try this**
    
    ```bash
    nc -vz <target-ip> 443
    ```
    
    **Trap**
    
    - Tightening NACL outbound without ephemeral return ports — silent half-broken connections

**5. Explain the complete request flow when using Gateway API with multiple GatewayClasses across regions. How do you prevent split-brain routing?**

??? success "Reveal answer"
    **In short:** Each region owns its Gateway + controller; global DNS steers users — never two controllers fighting one Gateway object.
    
    **Key points**
    
    - **Objects** — GatewayClass (impl) → Gateway (listeners) → HTTPRoute/GRPCRoute
    - **Flow** — client → geo/latency DNS → regional Gateway → Service → Pods
    - **One owner** — one controller per GatewayClass; clear cluster/namespace bounds
    - **Split-brain** — avoid dual-active writers; use health-based DNS, not dual A records to both
    
    **Trap**
    
    - Two independent controllers reconciling the same Gateway — flapping routes and certs

**6. What is a Network Virtual Appliance (NVA) in Azure?**

??? success "Reveal answer"
    **In short:** An NVA is a VM middlebox — firewall, router, SD-WAN — you force traffic through with UDRs.
    
    **Key points**
    
    - **Role** — inspect or transform east-west/north-south traffic in the VNet
    - **Pathing** — User-Defined Routes (or Gateway Load Balancer) steer packets
    - **Examples** — Palo Alto, Fortinet, Check Point; Azure Firewall is the managed cousin
    - **Ops** — HA pairs, sizing, and UDR failover or you create a black hole
    
    **Try this**
    
    ```bash
    az network nic show-effective-route-table --ids <nic-id> -o table
    ```
    
    **Trap**
    
    - Single NVA with no HA — one reboot takes the whole egress/ingress path down

**7. What is the difference between Public and Private IP Subnets?**

??? success "Reveal answer"
    **In short:** “Public” means a route to an Internet Gateway; “private” means no direct IGW — routing defines the label, not the CIDR name.
    
    **Key points**
    
    - **Public** — default route to IGW; often auto-assign public IPs (LBs, bastions)
    - **Private** — no IGW route; egress via NAT if needed
    - **Inbound** — internet reaches apps via public-tier LB, not DB public IPs
    - **Still reachable** — VPN, Direct Connect, peering, PrivateLink still work
    
    **Try this**
    
    ```bash
    ip route
    curl -4 ifconfig.me
    ```
    
    **Trap**
    
    - Calling a subnet “private” while its route table still points at the IGW

**8. What is VLSM (Variable Length Subnet Mask) and when do you use it in DevOps?**

??? success "Reveal answer"
    **In short:** VLSM carves one block into uneven sizes — /26 for a busy tier, /28 for a tiny management slice — so you stop wasting addresses.
    
    **Key points**
    
    - **What** — different prefix lengths inside one supernet (vs fixed-size subnetting)
    - **Why** — VPC/VNet space is finite; EKS pod CIDRs and peering punish waste
    - **Practice** — allocate large for pods/nodes, tiny for endpoints/management
    - **Review** — document IPAM in Terraform; leave growth headroom
    
    **Trap**
    
    - Overlapping or too-small CIDRs that force painful renumbering later

**9. What is Round-Robin DNS and how does it benefit DevOps?**

??? success "Reveal answer"
    **In short:** Round-robin DNS rotates A/AAAA answers so clients fan out — cheap load spread, blind to health.
    
    **Key points**
    
    - **How** — nameserver returns record sets in rotating order
    - **Benefit** — simple, global, no LB appliance for basic distribution
    - **Limits** — client/DNS caching sticks; no awareness of dead backends
    - **Upgrade path** — health-checked DNS failover or a real L4/L7 LB
    
    **Try this**
    
    ```bash
    dig +short example.com A
    dig +short example.com A
    ```
    
    **Trap**
    
    - Treating round-robin as HA — clients keep hitting a dead IP until TTL expires

**10. What is the difference between NAT Gateway and IGW?**

??? success "Reveal answer"
    **In short:** IGW is the VPC’s two-way door for public IPs; NAT Gateway is a one-way exit for private subnets.
    
    **Key points**
    
    - **IGW** — bidirectional internet for resources with public/Elastic IPs
    - **NAT Gateway** — outbound (and return for established flows) only; no inbound listeners
    - **Placement** — NAT lives in a public subnet; private subnet routes `0.0.0.0/0` to it
    - **Cost/HA** — NAT is AZ-scoped; multi-AZ NAT for production egress
    
    **Try this**
    
    ```bash
    curl -4 ifconfig.me
    ```
    
    **Trap**
    
    - Expecting inbound SSH to a private instance “through” the NAT Gateway

**11. Can you tell me the difference between REST APIs and WebSocket APIs in API Gateway?**

??? success "Reveal answer"
    **In short:** REST is request/response over HTTPS; WebSocket keeps a sticky pipe for push both ways.
    
    **Key points**
    
    - **REST API** — methods/resources, JSON, API keys, usage plans, Lambda/HTTP integrations
    - **WebSocket API** — persistent connections; `$connect` / `$disconnect` / route keys
    - **Use REST** — CRUD, webhooks, classic microservices
    - **Use WebSocket** — chat, live dashboards, notifications
    
    **Try this**
    
    ```bash
    curl -i https://api.example.com/v1/health
    # wscat -c wss://ws.example.com
    ```
    
    **Trap**
    
    - Forcing long-poll REST for real-time push — timeouts and idle LB kills

**12. Can you tell me the difference between NAT Gateway and Internet Gateway?**

??? success "Reveal answer"
    **In short:** Same story, different door: IGW for public inbound/outbound; NAT Gateway for private-subnet egress only.
    
    **Key points**
    
    - **IGW path** — public subnet + public IP → internet both ways
    - **NAT path** — private subnet → NAT in public subnet → internet out
    - **Failure checks** — route tables, NAT AZ after move, SG egress 80/443
    - **Scale** — watch SNAT port exhaustion under high concurrency
    
    **Try this**
    
    ```bash
    curl -4 ifconfig.me
    curl -I https://example.com
    ```
    
    **Trap**
    
    - Giving databases public IPs “so apt works” instead of using NAT or private mirrors

**13. Difference between NAT gateway and NAT instance?**

??? success "Reveal answer"
    **In short:** NAT Gateway is managed and boring (good); NAT instance is DIY EC2 with iptables you babysit.
    
    **Key points**
    
    - **NAT Gateway** — AZ HA within AZ, patched by AWS, high bandwidth, hours+data billing
    - **NAT instance** — self-managed size, failover, patching, monitoring
    - **When instance** — niche cost/control labs; rare in modern prod
    - **Instance must** — disable source/dest check; script failover
    
    **Try this**
    
    ```bash
    curl -I https://example.com
    curl -4 ifconfig.me
    ```
    
    **Trap**
    
    - Forgetting source/destination check on a NAT instance — outbound silently fails

**14. What is nodeport what are the cases we can use it?**

??? success "Reveal answer"
    **In short:** NodePort opens the same high port on every node and forwards into the Service — lab and bare-metal friendly, public-cloud awkward.
    
    **Key points**
    
    - **Range** — default 30000–32767 on each node IP
    - **Use** — kind/labs, on-prem external L4 LB → NodePorts, quick debug
    - **Avoid** — exposing NodePorts directly on the public internet at scale
    - **Prefer** — LoadBalancer / Ingress / Gateway API for production entry
    
    **Try this**
    
    ```bash
    kubectl get svc
    curl -v http://<node-ip>:<nodePort>
    ```
    
    **Trap**
    
    - Using NodePort as the long-term public entry on managed cloud clusters

**15. What is Web Application Firewall?**

??? success "Reveal answer"
    **In short:** A WAF is an L7 bouncer — it reads HTTP and blocks SQLi, XSS, and bot abuse before your app sees it.
    
    **Key points**
    
    - **Where** — in front of ALB, CloudFront, API Gateway, App Gateway, Ingress
    - **Rules** — managed OWASP sets plus custom; start in count/log, then block
    - **Tuning** — false positives on rare query shapes; whitelist carefully
    - **Not enough** — still need secure code, authn, and least-privilege backends
    
    **Trap**
    
    - Flipping to block mode on day one with no logging — you invent outages

**16. What is SSL/TLS Handshake?**

??? success "Reveal answer"
    **In short:** The TLS handshake is the crypto handshake that proves the server and agrees keys before any HTTP body moves.
    
    **Key points**
    
    - **TLS 1.2 sketch** — ClientHello (ciphers, SNI) → ServerHello + cert → key exchange → encrypted
    - **TLS 1.3** — fewer round trips; forward secrecy by default
    - **DevOps cares** — cert validity, SNI, cipher policy, mTLS in mesh
    - **Symptoms** — `SSL certificate problem`, handshake timeout, wrong host cert
    
    **Try this**
    
    ```bash
    openssl s_client -connect example.com:443 -servername example.com </dev/null
    curl -vI https://example.com
    ```
    
    **Trap**
    
    - Ignoring SNI — one IP hosting many certs returns the wrong certificate

**17. What is difference between coreDNS and kube-proxy?**

??? success "Reveal answer"
    **In short:** CoreDNS turns names into ClusterIPs; kube-proxy (or eBPF) turns ClusterIPs into Pod endpoints — name plane vs data plane.
    
    **Key points**
    
    - **CoreDNS** — `svc.ns.svc.cluster.local` → ClusterIP via `kube-dns` Service
    - **kube-proxy** — iptables/ipvs (or Cilium) programs Service → Endpoints forwarding
    - **Debug order** — resolve name, then hit ClusterIP, then Pod IP
    - **Failure modes** — DNS loop/timeouts vs blackhole Services with empty endpoints
    
    **Try this**
    
    ```bash
    kubectl -n kube-system logs deploy/coredns --tail=30
    kubectl get endpointslices -A | head
    nslookup kubernetes.default.svc.cluster.local
    ```
    
    **Trap**
    
    - Blaming CoreDNS when Endpoints are empty — DNS worked; nothing to forward to

**18. Difference between http and https?**

??? success "Reveal answer"
    **In short:** HTTP is plaintext on the wire; HTTPS is HTTP wrapped in TLS — confidentiality, integrity, and server identity.
    
    **Key points**
    
    - **HTTP** — readable by any on-path observer; easy to inject
    - **HTTPS** — encrypts the session; cert authenticates the server name
    - **Ops** — redirect HTTP→HTTPS, HSTS, modern TLS only
    - **Does not fix** — XSS, bad auth, or secrets in query strings/logs
    
    **Try this**
    
    ```bash
    curl -I http://example.com
    openssl s_client -connect example.com:443 -servername example.com </dev/null
    ```
    
    **Trap**
    
    - Putting tokens in URLs even over HTTPS — they land in logs and Referer headers

**19. Difference between subnet and nacl?**

??? success "Reveal answer"
    **In short:** A subnet is where you place resources (CIDR + routes); a NACL is an optional filter on traffic in and out of that place.
    
    **Key points**
    
    - **Subnet** — IP range inside VPC/VNet; owns route table association
    - **NACL** — stateless allow/deny rules attached to the subnet
    - **Together** — placement vs policing; you always have a subnet, NACL is policy
    - **Day-to-day** — most app policy lives in Security Groups, not NACLs
    
    **Trap**
    
    - Confusing “no NACL custom rules” with “no network security” — SGs still apply

**20. Difference between nat gateway and internet gateway?**

??? success "Reveal answer"
    **In short:** IGW serves public-IP resources both ways; NAT Gateway lets private resources phone home without taking inbound calls.
    
    **Key points**
    
    - **Mental model** — ALB in public subnet (IGW inbound); app tasks private, egress via NAT
    - **Routes** — public `0.0.0.0/0` → IGW; private `0.0.0.0/0` → NAT
    - **HA/cost** — multi-AZ NAT; data processing fees add up
    - **Security** — prefer private + NAT over public IPs on app/DB tiers
    
    **Try this**
    
    ```bash
    curl -4 ifconfig.me
    ```
    
    **Trap**
    
    - Routing a private subnet’s default route to the IGW — broken or accidental exposure

**21. What is Az App Gateway and how it encrypt http/https traffic?**

??? success "Reveal answer"
    **In short:** Azure Application Gateway is a regional L7 reverse proxy — it terminates (or passes) TLS, then talks to backends on HTTP or HTTPS.
    
    **Key points**
    
    - **Role** — listeners, rules, HTTP settings, backend pools; optional WAF
    - **Client side** — HTTPS to the gateway with a listener certificate
    - **Backend side** — re-encrypt end-to-end or HTTP inside the VNet by design
    - **Ops** — health probes, SSL policy, Key Vault certs for rotation
    
    **Try this**
    
    ```bash
    curl -vI https://app.example.com
    openssl s_client -connect app.example.com:443 -servername app.example.com </dev/null
    ```
    
    **Trap**
    
    - Assuming “HTTPS listener” means end-to-end encryption when backend is HTTP

**22. What is mean by Nat Gateway and Nat instance?**

??? success "Reveal answer"
    **In short:** Both do source NAT for private hosts; Gateway is the managed default, instance is the EC2 you operate yourself.
    
    **Key points**
    
    - **Shared job** — private IPs appear as a public IP on the internet
    - **Gateway** — less ops, better bandwidth story, multi-AZ design pattern
    - **Instance** — cheaper tiny labs; you own patches and failover
    - **Watch** — SNAT port exhaustion → intermittent outbound failures
    
    **Try this**
    
    ```bash
    curl -4 ifconfig.me
    curl -I https://example.com
    ```
    
    **Trap**
    
    - Single NAT in one AZ — AZ failure kills all private egress

## Scenarios and troubleshooting

**23. During peak traffic, ingress controller is routing requests slowly. How do you debug it?**

??? success "Reveal answer"
    **In short:** Prove where time is spent — controller CPU, upstream pods, DNS/TLS, or queues — before blindly adding replicas.
    
    **Key points**
    
    - **Controller** — `kubectl top`, HPA, access-log latency and 5xx/timeouts
    - **Upstream** — app pod latency and readiness; cull bad backends
    - **Config** — keepalives, `proxy-*` timeouts, connection limits
    - **Path split** — curl Ingress Service inside cluster vs external LB hostname
    
    **Try this**
    
    ```bash
    kubectl top pod -n ingress-nginx
    kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=100
    kubectl run tmp --rm -it --image=nicolaka/netshoot -- bash
    # then: curl -vH 'Host: app.example' http://ingress-svc
    ```
    
    **Trap**
    
    - Scaling Ingress while the app is the bottleneck — you only move the queue

**24. I have webapp in India and slowly users from abroad are also tyring to access it but there is latency. How would fix this issue, which service can help in reducing latency?**

??? success "Reveal answer"
    **In short:** Distant users pay physics — put static content on a CDN and bring compute closer with multi-region or edge, not a bigger India VM.
    
    **Key points**
    
    - **CDN** — CloudFront, Azure CDN, Cloudflare for static/assets and caching
    - **Compute** — regional app stacks + geo/latency DNS or Anycast entry
    - **Data** — avoid cross-region synchronous DB chats; cache and eventual design
    - **Measure** — regional synthetic probes (RTT, TTFB), not only origin dashboards
    
    **Trap**
    
    - Expecting a CDN alone to fix chatty dynamic APIs that always hit origin

**25. How would you setup DNS here?**

??? success "Reveal answer"
    **In short:** Hosted zone in IaC: apex/www Alias to CDN or LB, separate `api`, low TTL during cutover, health-checked failover if multi-region.
    
    **Key points**
    
    - **Records** — Alias/ANAME to LB/CDN; never raw changing IPs if avoidable
    - **Cutover** — drop TTL before change, raise after; document rollback
    - **Mail** — SPF/DKIM/DMARC if sending mail from the domain
    - **Internal** — split-horizon when private names differ from public
    
    **Try this**
    
    ```bash
    dig +short app.example.com
    dig @8.8.8.8 app.example.com A
    curl -I https://app.example.com
    ```
    
    **Trap**
    
    - Hand-editing only prod’s zone — staging and prod drift until the next incident

**26. How would you manage SSL and TLS?**

??? success "Reveal answer"
    **In short:** Automate issue and rotate — ACM, Key Vault, or cert-manager — and alert on expiry like a pager-worthy SLO.
    
    **Key points**
    
    - **Issue** — ACM on ALB/CloudFront; Azure Key Vault + App Gateway; cert-manager in K8s
    - **Policy** — modern TLS versions/ciphers; HTTP→HTTPS; prefer short-lived certs
    - **Internal** — mTLS via mesh or workload identity where needed
    - **Keys** — KMS/HSM-backed stores; never commit private keys
    
    **Try this**
    
    ```bash
    openssl s_client -connect host:443 -servername host </dev/null | openssl x509 -noout -dates -subject
    ```
    
    **Trap**
    
    - Manual yearly renewals with no expiry monitor — classic Friday outage

**27. You need to expose an application internally without using a LoadBalancer or NodePort service. How would you do it?**

??? success "Reveal answer"
    **In short:** ClusterIP plus an internal Ingress/Gateway (or mesh gateway) — stay east-west without punching node high ports.
    
    **Key points**
    
    - **Default** — ClusterIP Service; clients use `svc.ns.svc.cluster.local`
    - **L7 internal** — Ingress/Gateway with internal class or internal LB annotation
    - **Break-glass** — `kubectl port-forward` only for humans, not platforms
    - **Mesh** — Istio/Gateway API internal listeners for zero-trust east-west
    
    **Try this**
    
    ```bash
    kubectl get svc
    curl -v http://myapp.myns.svc.cluster.local
    kubectl get endpointslices -n myns
    ```
    
    **Trap**
    
    - Reaching for NodePort for internal traffic — widens the attack surface for no gain

**28. How do you troubleshoot issues with an Ingress Controller?**

??? success "Reveal answer"
    **In short:** Walk the path in order: Ingress object → Service/Endpoints → controller logs → in-cluster curl → DNS/LB health → TLS secret.
    
    **Key points**
    
    - **Objects** — IngressClass, host/path, service port, EndpointSlices non-empty
    - **Controller** — describe events; watch admission/config reload errors
    - **TLS** — secret exists, SANs match host, not expired
    - **Edge** — cloud LB target health, WAF blocks, NetworkPolicies
    
    **Try this**
    
    ```bash
    kubectl describe ingress -n <ns> <name>
    kubectl get endpointslices -n <ns>
    kubectl logs -n ingress-nginx deploy/ingress-nginx-controller --tail=100
    ```
    
    **Trap**
    
    - Debugging “DNS” when the Service has no ready endpoints — name never was the issue

**29. How does DNS Failover support DevOps?**

??? success "Reveal answer"
    **In short:** Health-checked DNS pulls sick endpoints out of answers so clients land on the surviving region — slow HA, not instant.
    
    **Key points**
    
    - **Mechanism** — Route 53 / Azure Traffic Manager style health checks alter records
    - **RTO** — good for multi-region active-passive at minutes scale
    - **Limits** — TTL and resolver caching delay failover and failback
    - **Pair with** — LB health, warm standby, and app-level readiness
    
    **Try this**
    
    ```bash
    dig +short app.example.com
    curl -I https://app.example.com
    ```
    
    **Trap**
    
    - Ultra-low TTL + flapping health checks — DNS thrash and cache chaos

## Practice questions

**30. High lat is reported between applicat ‘tion servers in different -9 i) eal ail > a ll a dh?**

??? success "Reveal answer"
    **In short:** Read as high latency between app servers across zones/regions — measure the path before you redesign the universe.
    
    **Key points**
    
    - **Measure** — `ping`/`mtr`, app RTT metrics, AZ vs region tags on both ends
    - **Causes** — chatty cross-AZ, sync cross-region calls, MTU/MSS, middleboxes
    - **Fixes** — keep chatty tiers co-located; async/cache across regions; right-size MTU
    - **K8s** — topology-aware routing / topology spread so pods aren’t randomly far
    
    **Try this**
    
    ```bash
    mtr -rwzbc 100 <peer-ip>
    curl -w 'namelookup:%{time_namelookup} connect:%{time_connect} total:%{time_total}\n' -o /dev/null -s http://<peer>
    ```
    
    **Trap**
    
    - Blaming “the network” when the app does N+1 sync calls across regions

**31. How do you design a highly available application in the cloud?**

??? success "Reveal answer"
    **In short:** Multi-AZ by default, stateless apps behind LBs, managed Multi-AZ data, health checks, and a written RPO/RTO you actually rehearse.
    
    **Key points**
    
    - **Compute** — multi-AZ autoscaling; graceful drain on deploy
    - **Data** — managed Multi-AZ + backups/PITR; avoid single-node truth
    - **Edge** — multi-AZ LB; DNS with more than one healthy target
    - **Prove** — game days / chaos; observability is part of HA
    
    **Trap**
    
    - Single NAT, single bastion, or one IP in DNS dressed up as “HA architecture”

**32. How do you secure your Ingress Controller?**

??? success "Reveal answer"
    **In short:** Lock the front door: TLS, WAF/rate limits, auth at the edge, patched controller, and no dangerous config snippets for untrusted tenants.
    
    **Key points**
    
    - **Crypto** — strong TLS; short-lived certs; disable weak ciphers
    - **Access** — OAuth/JWT/IAP; separate public vs internal IngressClasses
    - **Network** — tight cloud SG/NSG; NetworkPolicies to backends
    - **Hardening** — patch controller; disable arbitrary nginx snippets if multi-tenant
    
    **Trap**
    
    - One shared Ingress for public internet and internal admin UIs

**33. How does CIDR notation improve IP address management in DevOps?**

??? success "Reveal answer"
    **In short:** CIDR (`10.0.0.0/16`) is the shared language of IPAM — precise ranges for VPCs, pods, peering, and allow lists.
    
    **Key points**
    
    - **Clarity** — prefix length states size without dotted masks
    - **Automation** — Terraform and SGs consume CIDRs cleanly
    - **Non-overlap** — plan multi-account and hybrid ranges up front
    - **Reviews** — PR diffs of CIDRs beat tribal spreadsheet lore
    
    **Trap**
    
    - Overlapping CIDRs across accounts — peering and PrivateLink become nightmares

**34. Load balancer throttling issues?**

??? success "Reveal answer"
    **In short:** Throttling looks like 429/503, rising latency, or sudden drops when WAF, connection limits, or saturated targets say “enough”.
    
    **Key points**
    
    - **Signals** — LB 4xx/5xx, active connections, target response time, WAF counts
    - **Causes** — rate limits, backend saturation, TLS/SNI mismatches, surge queues
    - **Fixes** — raise justified limits, scale healthy targets, tune WAF, fix keepalives
    - **Prove** — correlate access logs with target metrics before changing the LB
    
    **Try this**
    
    ```bash
    curl -w '%{http_code} %{time_total}\n' -o /dev/null -s https://app.example.com/health
    ss -s
    ```
    
    **Trap**
    
    - Raising LB limits while backends are already OOM — you amplify the outage

**35. How does an Ingress Controller differ from a Load Balancer?**

??? success "Reveal answer"
    **In short:** A cloud LB is the VIP plumbing; an Ingress Controller is the Kubernetes-aware reverse proxy that programs host/path routes from API objects.
    
    **Key points**
    
    - **LB** — infra L4/L7 VIP to instances/IPs; cloud-managed lifecycle
    - **Ingress Controller** — watches Ingress/Gateway API → configures nginx/Envoy/etc.
    - **Together** — often LB → controller Service → Pods (LB is the front VIP)
    - **Routing brain** — host/path/TLS in cluster objects, not only LB console rules
    
    **Trap**
    
    - Saying “we don’t need a LB because we have Ingress” on clouds that still front it with one

**36. How do Symmetric and Asymmetric Encryption support DevOps?**

??? success "Reveal answer"
    **In short:** Symmetric is the fast shared lock for bulk data; asymmetric is the identity handshake and signing layer pipelines rely on.
    
    **Key points**
    
    - **Symmetric (AES-GCM)** — disk encryption, TLS record keys, VPN payloads
    - **Asymmetric (RSA/ECDSA)** — TLS certs, SSH keys, cosign/JWT signing
    - **Together** — handshake with asymmetric, then bulk with symmetric session keys
    - **DevOps** — KMS/Vault, rotate, sign artefacts, verify before deploy
    
    **Trap**
    
    - Committing private keys or long-lived shared secrets into Git “just for CI”

**37. How will you restart http service from VM?**

??? success "Reveal answer"
    **In short:** On systemd: restart the unit — then prove listening ports and a local HTTP response, not just a green `systemctl` line.
    
    **Key points**
    
    - **Command** — `systemctl restart nginx` (or `httpd`/`apache2`)
    - **Prefer reload** — config-only changes: `systemctl reload` to avoid drops
    - **Containers** — restart Deployment/Pod, not a service inside an immutable image
    - **Impact** — check who shares the host before bouncing production
    
    **Try this**
    
    ```bash
    sudo systemctl restart nginx
    systemctl is-active nginx
    ss -lntp | grep -E ':80|:443'
    curl -I http://127.0.0.1
    ```
    
    **Trap**
    
    - Blind `restart` on a shared VM during peak — drops every virtual host at once

**38. How do Firewall Rules apply to DevOps?**

??? success "Reveal answer"
    **In short:** Firewall rules are policy as code — host nftables, cloud SGs/NACLs, or appliances — reviewed like any other merge.
    
    **Key points**
    
    - **Layers** — host, SG/NSG, NACL, WAF; know which layer failed
    - **IaC** — Terraform/Ansible diffs; prefer SG-to-SG over `0.0.0.0/0`
    - **Change control** — staged apply; emergency break-glass with audit
    - **Validate** — `nc`/`curl` from intended source after change
    
    **Try this**
    
    ```bash
    nc -vz <target> 443
    curl -I https://<target>
    ```
    
    **Trap**
    
    - Opening `0.0.0.0/0` “temporarily” and never closing it

**39. How does the TCP 3-Way Handshake apply to DevOps?**

??? success "Reveal answer"
    **In short:** SYN → SYN-ACK → ACK proves both sides can talk on that port before any application byte is trusted.
    
    **Key points**
    
    - **Purpose** — agree sequence numbers; confirm bidirectional reachability
    - **Ops signals** — half-open floods, SYN cookies, LB health check failures
    - **Debug** — connect timeout vs reset tells different stories than HTTP 500
    - **Tools** — `ss`, `tcpdump` on SYN flags, `curl -v` connect timing
    
    **Try this**
    
    ```bash
    ss -s
    tcpdump -ni any 'tcp[tcpflags] & (tcp-syn) != 0' -c 20
    curl -v --http1.1 https://example.com -o /dev/null
    ```
    
    **Trap**
    
    - Blaming the app when the handshake never completes — packets never reached the process

**40. Diff b/w Public and Private subnet?**

??? success "Reveal answer"
    **In short:** Public has a path to the Internet Gateway; private does not — name tags lie, route tables tell the truth.
    
    **Key points**
    
    - **Public** — `0.0.0.0/0` → IGW; LBs/bastions; often public IPs
    - **Private** — no IGW; egress via NAT; apps and databases live here
    - **Inbound** — internet via public LB/WAF, not direct to private instances
    - **Check** — route table + auto-assign public IP setting
    
    **Try this**
    
    ```bash
    curl -4 ifconfig.me
    # compare route tables for public vs private subnet associations
    ```
    
    **Trap**
    
    - Launching a “private” workload that still auto-assigns a public IP

## Related
- Course: [Networking](../networking/index.md)
- Hub: [Interview Preparation](index.md)
{% endraw %}
