---
title: Load Balancing Fundamentals
description: Master Layer 4 vs Layer 7 load balancing, scheduling algorithms, health checks, high-availability pairs, and AWS ALB/NLB concepts.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - load-balancer
  - alb
  - nlb
  - high-availability
  - health-checks
prerequisites:
  - Complete [Firewalls and Access Control](firewalls-and-access-control.md) or equivalent
  - Understanding of HTTP/HTTPS and TCP connection basics
  - Familiarity with cloud VPC concepts (helpful but not required)
comments: false
---

# Load Balancing Fundamentals

## Overview

Load balancers distribute incoming traffic across multiple backend servers so no single instance bears the full load. They provide **scalability** (add servers to handle growth), **availability** (route around failed nodes), and **operational flexibility** (drain instances for deployments without downtime). Every production web application behind more than one server uses a load balancer — whether hardware appliances, software like HAProxy and nginx, or managed cloud services like AWS ALB and NLB.

Choosing the wrong load balancer tier causes subtle production bugs: an L4 balancer cannot route based on URL path; an L7 balancer adds latency and TLS termination complexity. This tutorial explains when to use each layer, how scheduling algorithms behave under load, and how health checks keep traffic away from broken backends.

This is **Tutorial 12** in **Module 4: Application Layer** of the REBASH Academy Networking series.

## Prerequisites

- Complete [Firewalls and Access Control](firewalls-and-access-control.md) — understand security groups and port-based access
- Complete [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md) or equivalent HTTP knowledge
- Basic understanding of TCP connections from [TCP and UDP Deep Dive](tcp-and-udp-deep-dive.md)
- Optional: AWS account for ALB/NLB console exploration

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Differentiate Layer 4 (transport) and Layer 7 (application) load balancing
- [ ] Compare scheduling algorithms: round-robin, least connections, and IP hash
- [ ] Configure and interpret health checks that accurately reflect backend readiness
- [ ] Design high-availability load balancer pairs with failover mechanisms
- [ ] Choose between AWS Application Load Balancer (ALB) and Network Load Balancer (NLB) for common scenarios
- [ ] Troubleshoot uneven traffic distribution and flapping health checks

## Architecture Diagram

```d2
direction: down

Clients: Clients {
        C1: "Client A"
        C2: "Client B"
        C3: "Client C"
    }
    LB: "Load Balancer Tier" {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        VIP: "Virtual IP / DNS Name"
        HC: "Health Check Engine"
        ALGO: "Scheduler\nround-robin · least conn · ip hash"
    }
    Backends: Backends {
        W1: "Web Server 1\nhealthy"
        W2: "Web Server 2\nhealthy"
        W3: "Web Server 3\nunhealthy"
    }
    Clients.C1 -> LB.VIP
    Clients.C2 -> LB.VIP
    Clients.C3 -> LB.VIP
    LB.VIP -> LB.ALGO
    LB.HC -> Backends.W1: probe {
      style.stroke-dash: 3
    }
    LB.HC -> Backends.W2: probe {
      style.stroke-dash: 3
    }
    LB.HC -> Backends.W3: fail {
      style.stroke-dash: 3
    }
    LB.ALGO -> Backends.W1
    LB.ALGO -> Backends.W2
    LB.ALGO -> Backends.W3: removed {
      style.stroke-dash: 3
    }
```

## Theory

### Why Load Balance?

Without a load balancer, clients connect directly to a single server IP. That creates:

- **Single point of failure** — server death means total outage
- **Scaling ceiling** — one machine's CPU, RAM, and NIC limits throughput
- **Painful deployments** — downtime during restarts unless you accept connection loss

A load balancer presents a **virtual IP (VIP)** or **DNS name** to clients. Backend servers sit in a **pool** or **target group**. The balancer selects a healthy member for each new connection (or request, at L7) according to a **scheduling algorithm**.

### Layer 4 vs Layer 7 Load Balancing

**Layer 4 (L4)** — operates at the **transport layer** (TCP/UDP). The load balancer forwards packets based on IP and port without inspecting HTTP headers or TLS content. It may perform NAT (DNAT) so backends see the balancer's IP as source, or preserve client IP via PROXY protocol.

Characteristics:

- Faster — no HTTP parsing or TLS decryption
- Protocol-agnostic — works for PostgreSQL, Redis, MQTT, not just HTTP
- Cannot route by URL path, Host header, or cookies
- Often uses **Direct Server Return (DSR)** in high-performance setups

**Layer 7 (L7)** — operates at the **application layer**. The balancer terminates HTTP/HTTPS, reads headers, cookies, and paths, then forwards to appropriate backends. Enables **content-based routing**, **SSL termination**, **WAF integration**, and **sticky sessions** via cookies.

| Feature | L4 (NLB, HAProxy TCP mode) | L7 (ALB, HAProxy HTTP mode) |
|---------|---------------------------|-------------------------------|
| Routing basis | IP + port | URL, Host, headers, cookies |
| TLS termination | Pass-through or optional | Native termination |
| Performance | Lower latency | Higher latency (inspection cost) |
| Use case | Gaming, DB proxies, extreme throughput | Web apps, microservices, API gateways |
| WebSocket | TCP pass-through works | Requires L7-aware config |

**Rule of thumb:** Use L7 when you need path-based routing, host-based multi-tenancy, or centralized TLS. Use L4 when you need maximum throughput, non-HTTP protocols, or static IP with TLS pass-through.

### Scheduling Algorithms

The **scheduler** decides which backend receives each new connection or request.

**Round Robin** — distributes sequentially across healthy backends: A → B → C → A → B. Simple and fair when all servers have equal capacity and request cost. Poor choice when requests vary wildly in duration (one slow request blocks a slot on that server while others stay idle).

**Weighted Round Robin** — assigns weights (e.g., server A weight 3, B weight 1) so higher-capacity nodes receive proportionally more traffic.

**Least Connections** — sends the next request to the backend with the fewest active connections. Better for long-lived connections and variable request times. Requires the balancer to track per-backend connection counts.

**IP Hash (Source Hash)** — hashes client source IP to select a backend. Same client consistently hits the same server — useful for **session affinity** when the application stores session state locally (not recommended in cloud-native apps; prefer external session stores).

**Least Response Time** — routes to the backend with lowest average response latency (available on some L7 balancers like NGINX Plus and ALB target group algorithms).

| Algorithm | Best for | Avoid when |
|-----------|----------|------------|
| Round robin | Homogeneous servers, short requests | Variable request duration |
| Least connections | Long polling, WebSockets, mixed workloads | Backends have very different capacities without weights |
| IP hash | Legacy session stickiness without cookies | Clients behind NAT (many users, one IP) |
| Weighted round robin | Mixed instance sizes | Weights not tuned after scaling events |

### Health Checks

A backend marked **unhealthy** is removed from rotation. Health checks must reflect **application readiness**, not just TCP port open.

**Types:**

- **TCP check** — can connect to port 443? Fast but misleading (port open, app crashed)
- **HTTP check** — GET `/health` expects 200 with body `OK`? Better
- **HTTPS check** — validates TLS and application response
- **Custom checks** — gRPC health, database ping (via sidecar)

**Parameters to tune:**

| Parameter | Purpose | Typical value |
|-----------|---------|---------------|
| Interval | Time between checks | 5–30 seconds |
| Timeout | Max wait for response | 2–5 seconds |
| Healthy threshold | Consecutive successes to mark healthy | 2–3 |
| Unhealthy threshold | Consecutive failures to mark unhealthy | 2–5 |

**Flapping** occurs when thresholds are too aggressive — a slow backend alternates healthy/unhealthy, causing user-facing errors. Increase unhealthy threshold and ensure `/health` endpoint is lightweight (no database dependency unless intentional).

!!! warning "Health check path must be lightweight"
    A `/health` endpoint that queries the database on every probe can mark the entire fleet unhealthy during a DB slowdown — causing a cascading outage. Use **liveness** (process up) vs **readiness** (can serve traffic) separation, as Kubernetes does.

### High-Availability Load Balancer Pairs

The load balancer itself must not be a single point of failure. Common HA patterns:

**Active-Passive pair** — two LB nodes share a **Virtual IP (VIP)** via **VRRP** (Keepalived) or cloud-managed failover. Active node holds VIP; passive monitors and takes over on failure. Failover time: seconds to sub-second depending on protocol.

**Active-Active pair** — both nodes handle traffic simultaneously (DNS round-robin, ECMP, or anycast). Higher complexity but better utilization.

**Managed cloud LBs** — AWS ALB/NLB, GCP Cloud Load Balancing, Azure LB run as managed services across availability zones — you do not manage HA pairs directly. You configure multi-AZ target groups and let the provider handle control-plane redundancy.

**DNS failover** — Route 53 health-checked failover between regional LBs. Not instant (TTL-dependent) but provides geographic redundancy.

### AWS ALB vs NLB Concepts

**Application Load Balancer (ALB)** — Layer 7 HTTP/HTTPS. Features:

- Path-based routing (`/api/*` → API targets, `/*` → web targets)
- Host-based routing (`api.example.com` vs `www.example.com`)
- WebSocket and HTTP/2 support
- Integration with AWS WAF, Cognito authentication
- Target types: EC2, IP, Lambda, containers

**Network Load Balancer (NLB)** — Layer 4 TCP/UDP/TLS. Features:

- Extreme performance (millions of requests/sec)
- Static IP per AZ (Elastic IP support)
- Preserves source IP without PROXY protocol
- TLS pass-through or termination
- Target types: EC2, IP, ALB (NLB in front of ALB pattern)

**Classic Load Balancer (CLB)** — legacy; avoid for new designs.

| Scenario | Recommended |
|----------|-------------|
| REST API with path routing | ALB |
| WebSockets with HTTP routing | ALB |
| Static IP requirement | NLB |
| Non-HTTP TCP (PostgreSQL proxy) | NLB |
| Maximum throughput, TLS pass-through | NLB |
| Lambda targets behind HTTP | ALB |

## Hands-on Lab

Use HAProxy or nginx on a lab VM, or AWS free tier. Commands below use **HAProxy** on Ubuntu.

### Step 1 – Install HAProxy and inspect default config

**Command:**

```bash
sudo apt update && sudo apt install -y haproxy
sudo systemctl status haproxy
grep -v '^\s*#' /etc/haproxy/haproxy.cfg | grep -v '^$' | head -20
```

**Explanation:** HAProxy is a production-grade L4/L7 load balancer used by GitHub, Reddit, and Stack Overflow. Review the default config before modifying.

### Step 2 – Start two backend web servers

**Command:**

```bash
mkdir -p /tmp/lb-lab/{web1,web2}
echo "Backend Server 1" > /tmp/lb-lab/web1/index.html
echo "Backend Server 2" > /tmp/lb-lab/web2/index.html
cd /tmp/lb-lab/web1 && python3 -m http.server 8081 &
cd /tmp/lb-lab/web2 && python3 -m http.server 8082 &
curl -s http://127.0.0.1:8081/
curl -s http://127.0.0.1:8082/
```

**Expected output:**

```text
Backend Server 1
Backend Server 2
```

### Step 3 – Configure HAProxy with round-robin

**Command:**

```bash
sudo tee /etc/haproxy/haproxy.cfg <<'EOF'
global
    log /dev/log local0
    maxconn 4096

defaults
    log     global
    mode    http
    option  httplog
    timeout connect 5s
    timeout client  30s
    timeout server  30s

frontend http_front
    bind *:8888
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /
    server web1 127.0.0.1:8081 check
    server web2 127.0.0.1:8082 check
EOF

sudo systemctl restart haproxy
```

**Explanation:** Frontend listens on 8888; backend pool uses round-robin with HTTP health checks against `/`.

### Step 4 – Verify round-robin distribution

**Command:**

```bash
for i in {1..6}; do curl -s http://127.0.0.1:8888/; echo; done
```

**Expected output:**

```text
Backend Server 1
Backend Server 2
Backend Server 1
Backend Server 2
...
```

### Step 5 – Simulate backend failure

**Command:**

```bash
# Stop web1
kill $(lsof -t -i:8081) 2>/dev/null
sleep 3
for i in {1..4}; do curl -s http://127.0.0.1:8888/; echo; done
echo "=== HAProxy stats ==="
echo "show stat" | sudo socat stdio /run/haproxy/admin.sock 2>/dev/null | cut -d, -f1,2,18 | head -5
```

**Explanation:** After health checks fail, HAProxy removes web1. All traffic routes to web2 only.

**Expected output:**

```text
Backend Server 2
Backend Server 2
...
```

### Step 6 – Switch to least connections algorithm

**Command:**

```bash
sudo sed -i 's/balance roundrobin/balance leastconn/' /etc/haproxy/haproxy.cfg
sudo systemctl restart haproxy
grep balance /etc/haproxy/haproxy.cfg
```

**Explanation:** `leastconn` minimizes active connections per backend — observe behavior under concurrent long requests in advanced labs.

### Step 7 – Explore AWS ALB concepts (CLI or console)

**Command:**

```bash
# List load balancers (requires AWS CLI configured)
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[*].[LoadBalancerName,Type,DNSName]' \
  --output table 2>/dev/null || echo "AWS CLI not configured — review ALB in console"
```

**Explanation:** Note `Type` column: `application` vs `network`. Map DNS names to Route 53 records in production.

### Step 8 – Cleanup

**Command:**

```bash
kill $(lsof -t -i:8082) 2>/dev/null
sudo systemctl stop haproxy
rm -rf /tmp/lb-lab
```

## Commands & Code

| Command / Tool | Description | Example |
|----------------|-------------|---------|
| `haproxy -c` | Validate HAProxy config syntax | `sudo haproxy -c -f /etc/haproxy/haproxy.cfg` |
| `systemctl reload haproxy` | Apply config without dropping connections | `sudo systemctl reload haproxy` |
| `aws elbv2 describe-target-health` | Check ALB/NLB target status | See AWS CLI docs |
| `curl` through LB | Test distribution | `curl -s http://lb-vip/` |
| `ss -tn` | Active connections per backend | `ss -tn sport = :8080` |

### nginx upstream block (L7 alternative)

```nginx
upstream backend_pool {
    least_conn;
    server 10.0.1.10:8080 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:8080 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:8080 backup;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /health {
        access_log off;
        return 200 'OK';
    }
}
```

## Common Mistakes

!!! warning "Using round-robin for long-lived connections"
    WebSockets and SSE connections stick to one backend for hours. Round-robin only affects **new** connections — existing ones do not rebalance. Scale by adding backends before capacity saturates, or use connection draining during deploys.

!!! warning "Health checks hitting expensive endpoints"
    Probing `/api/report?full=true` every 5 seconds loads the database unnecessarily. Dedicated `/healthz` returning static 200 is standard practice.

!!! warning "Ignoring connection draining during deploys"
    Killing a backend immediately drops in-flight requests. Use **draining** (ALB deregistration delay, HAProxy `disable` + wait) to allow existing connections to complete.

!!! warning "IP hash behind carrier-grade NAT"
    Thousands of mobile users share one public IP — IP hash sends them all to one backend. Use cookie-based stickiness at L7 instead.

## Best Practices

!!! tip "Terminate TLS at the load balancer for most web apps"
    Centralized certificate management, HTTP/2, and WAF integration justify L7 termination. Use TLS pass-through only when compliance requires end-to-end encryption without intermediary inspection.

!!! tip "Set deregistration delay to match longest request"
    ALB default deregistration delay is 300 seconds. Tune based on your P99 request duration to avoid 502 errors during rolling deploys.

!!! tip "Monitor target health and unhealthy host count"
    Alert when any target group has zero healthy hosts or when unhealthy count exceeds threshold. This catches misconfigured health checks before users notice.

!!! tip "Use separate target groups per service"
    Path-based routing to different target groups (`/api` vs `/static`) enables independent scaling and deployment cadences.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 502 Bad Gateway | No healthy backends | Check target health, SG rules, health check path/port |
| Uneven traffic distribution | Sticky sessions, IP hash, or long connections | Expected for leastconn/IP hash; verify algorithm choice |
| Health check flapping | Timeout too short, slow app, threshold too low | Increase timeout/threshold; optimize health endpoint |
| Clients see wrong backend content | Session state on server without stickiness | Externalize sessions (Redis) or enable cookie stickiness |
| NLB targets unreachable | Wrong target type (instance vs IP), SG mismatch | Verify target registration and SG allows LB subnets |
| SSL errors at ALB | Certificate mismatch, wrong listener | Check ACM cert covers Host header; verify listener protocol |
| High latency after adding L7 LB | TLS termination + inspection overhead | Consider NLB + L7 only where routing needed; enable HTTP keep-alive |

## Summary

- **L4 load balancers** route by IP/port; **L7** route by HTTP content — choose based on routing needs and protocol
- **Round-robin** suits equal servers and short requests; **least connections** suits variable duration; **IP hash** provides crude stickiness
- **Health checks** must be tuned to avoid flapping and should use lightweight readiness endpoints
- **HA pairs** (Keepalived/VRRP) or **managed cloud LBs** eliminate the balancer as a single point of failure
- **AWS ALB** for HTTP routing and WAF; **AWS NLB** for performance, static IP, and non-HTTP TCP
- Always configure **connection draining** and monitor **target health** during deployments

## Interview Questions

1. What is the difference between Layer 4 and Layer 7 load balancing?
2. When would you choose round-robin over least connections?
3. Explain how a health check removes a backend from rotation. What causes flapping?
4. How do you prevent the load balancer itself from becoming a single point of failure?
5. Compare AWS ALB and NLB — when would you use each?
6. What is session persistence (stickiness), and what are the trade-offs?
7. A deployment causes 502 errors for 30 seconds. What load balancer setting might fix this?
8. Why is IP hash problematic for clients behind corporate NAT?
9. What is the difference between liveness and readiness in the context of load balancing?
10. How does a Network Load Balancer preserve client source IP compared to an ALB?

??? tip "Sample Answers (Questions 1, 5, and 7)"

    **Q1 — L4 vs L7:** L4 load balancing forwards TCP/UDP connections based on IP address and port without inspecting application data. It is faster and protocol-agnostic. L7 load balancing terminates HTTP, inspects headers, paths, and cookies, and can route requests differently within the same port — enabling path-based routing, SSL termination, and WAF integration at the cost of higher latency and HTTP-specific scope.

    **Q5 — ALB vs NLB:** ALB is Layer 7 for HTTP/HTTPS with path/host routing, WebSockets, Lambda targets, and WAF integration — ideal for web applications and APIs needing content-based routing. NLB is Layer 4 for TCP/UDP with extreme throughput, static Elastic IPs, source IP preservation, and TLS pass-through — ideal for non-HTTP protocols, gaming, IoT, or when you need predictable IP addresses and maximum performance.

    **Q7 — 502 during deployment:** In-flight requests hit backends being terminated. Increase **deregistration delay** (connection draining) on the target group so the LB stops sending new connections but allows existing ones to complete before the instance shuts down. Also ensure graceful shutdown in the application (SIGTERM handler) and readiness probe removal before SIGKILL.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [Firewalls and Access Control](firewalls-and-access-control.md) *(previous in Module 4)*
- [Reverse Proxy and Ingress Basics](reverse-proxy-and-ingress-basics.md) *(next in Module 4)*
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- [Cloud Networking — VPCs and Subnets](cloud-networking-vpc-and-subnets.md)

## References

- [HAProxy Configuration Manual](https://www.haproxy.org/download/2.9/doc/configuration.txt)
- [AWS Elastic Load Balancing documentation](https://docs.aws.amazon.com/elasticloadbalancing/)
- [AWS ALB vs NLB decision guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/introduction.html)
- [nginx load balancing documentation](https://nginx.org/en/docs/http/load_balancing.html)
- [Google SRE Book — Load Balancing at the Frontend](https://sre.google/sre-book/load-balancing-frontend/)
