---
title: TCP and UDP Deep Dive
description: Master the TCP three-way handshake, port and socket mechanics, UDP use cases, connection states, TIME_WAIT, and inspection with ss and netstat.
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
category: networking
tags:
  - networking
  - tcp
  - udp
  - ports
  - sockets
  - ss
  - netstat
prerequisites:
  - Complete Module 2 networking tutorials or understand IP addressing and routing
  - Linux host with network access and optional sudo for process-level socket inspection
  - Basic familiarity with client-server architecture
comments: false
---

# TCP and UDP Deep Dive

## Overview

Transport layer protocols decide **how** data moves between applications: **TCP** provides reliable, ordered, connection-oriented delivery; **UDP** offers lightweight, best-effort datagrams. Every production outage involving "connection refused," "timeout," or "too many open files" eventually leads here — to ports, sockets, handshake state, and kernel connection tables.

This tutorial is **Tutorial 7** in **Module 3: Transport & DNS** of the REBASH Academy Networking series. You will dissect the three-way handshake, interpret `/proc/net/tcp` states via `ss`, understand why **TIME_WAIT** accumulates on busy servers, and know when UDP beats TCP. For command basics, see [Linux Networking Essentials](../linux/linux-networking-essentials.md); this tutorial focuses on transport-layer theory and production debugging.

## Prerequisites

- Complete [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) or equivalent L3 connectivity knowledge
- Linux VM or cloud instance (local lab or SSH session)
- `sudo` for `ss -p` process mapping and sysctl inspection
- Optional: `nc` (netcat) for socket experiments

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain the TCP three-way handshake and connection teardown (FIN/ACK)
- [ ] Describe the difference between ports, sockets, and file descriptors
- [ ] List TCP connection states and interpret `ss` output
- [ ] Explain TIME_WAIT, its purpose, and mitigation strategies
- [ ] Identify appropriate UDP use cases (DNS, NTP, QUIC, streaming)
- [ ] Debug "connection refused" vs "timeout" vs "address already in use"

## Architecture Diagram

```d2
shape: sequence_diagram

Client: Client
Server: Server
# Note over Client,Server: TCP Three-Way Handshake
Client -> Server: "SYN (seq=x)"
Server -> Client: "SYN-ACK (seq=y, ack=x+1)"
Client -> Server: "ACK (ack=y+1)"
# Note over Client,Server: ESTABLISHED — data transfer
Client -> Server: "Data segments (ACKed)"
Server -> Client: "Response data"
# Note over Client,Server: Connection Teardown
Client -> Server: FIN
Server -> Client: ACK
Server -> Client: FIN
Client -> Server: ACK
# Note over Client: TIME_WAIT (2×MSL)
```

## Theory

### Ports and Sockets

A **port** is a 16-bit number (0–65535) identifying an application endpoint on a host:

| Range | Name | Usage |
|-------|------|-------|
| 0–1023 | Well-known | HTTP 80, HTTPS 443, SSH 22 |
| 1024–49151 | Registered | User services, databases |
| 49152–65535 | Ephemeral/dynamic | Client-side source ports |

A **socket** is the kernel data structure `(protocol, local IP, local port, remote IP, remote port)` — the complete conversation identifier. "Listening socket" accepts connections; "connected socket" represents an established session.

On Linux, sockets appear as **file descriptors** — `ulimit -n` limits how many a process may open. High-traffic servers hitting "too many open files" often need ulimit tuning **and** TIME_WAIT management.

### TCP — Transmission Control Protocol

TCP guarantees:

- **Reliability** — lost segments retransmitted
- **Ordering** — sequence numbers reorder datagrams
- **Flow control** — sliding window prevents overwhelming receiver
- **Congestion control** — adjusts rate based on network conditions

#### Three-Way Handshake

1. **SYN** — Client sends synchronizing sequence number
2. **SYN-ACK** — Server acknowledges and sends its own sequence
3. **ACK** — Client acknowledges server's sequence; both enter **ESTABLISHED**

Half-open connections (SYN without completing handshake) are the basis of SYN flood attacks — mitigated by SYN cookies and firewall rate limiting.

#### Connection Teardown

Graceful close uses **FIN-ACK** exchange in both directions (full close) or **RST** for abrupt termination. After active closer sends final ACK, it enters **TIME_WAIT** for **2×MSL** (Maximum Segment Lifetime, typically 60–120 seconds on Linux) to:

- Ensure late duplicates from old connection don't corrupt new sessions
- Allow final ACK to reach peer if retransmission needed

High-connection-rate servers (load balancers, proxies) accumulate thousands of TIME_WAIT sockets — tune `net.ipv4.tcp_tw_reuse` (carefully) and use connection pooling.

#### TCP State Machine

| State | Meaning |
|-------|---------|
| LISTEN | Server waiting for incoming connections |
| SYN-SENT | Client sent SYN, awaiting SYN-ACK |
| SYN-RECV | Server received SYN, sent SYN-ACK |
| ESTABLISHED | Connection active, data flowing |
| FIN-WAIT-1/2 | Active closer initiated shutdown |
| CLOSE-WAIT | Passive side received FIN, app hasn't closed yet |
| TIME-WAIT | Active closer waiting 2×MSL |
| CLOSED | No connection |

**CLOSE-WAIT** stuck high indicates application bug — server received FIN but never called `close()`.

### UDP — User Datagram Protocol

UDP sends self-contained **datagrams** without connection setup:

- No handshake, no guaranteed delivery, no ordering
- Lower latency and overhead — header is 8 bytes vs TCP's 20+
- Used when application handles reliability or loss is acceptable

| Use Case | Why UDP |
|----------|---------|
| DNS queries | Small request/response, low latency |
| NTP | Periodic time sync, tiny packets |
| VoIP / gaming | Tolerates loss; retransmitting old audio is useless |
| QUIC (HTTP/3) | UDP transport with user-space reliability (TLS 1.3) |
| Kubernetes kubelet | Some health probes; service discovery patterns |

### ss vs netstat

Both inspect socket tables. **`ss`** reads from netlink directly — faster, more complete, maintained. **`netstat`** parses `/proc/net/*` — legacy but still common in older runbooks.

Key `ss` flags:

- `-t` TCP, `-u` UDP
- `-l` listening only
- `-a` all (listening + established)
- `-n` numeric (skip DNS reverse lookup)
- `-p` process name (requires root)
- `-i` TCP internal information (RTT, cwnd)
- `-o` timer information (useful for TIME_WAIT)

## Hands-on Lab

### Step 1 – List listening ports

**Command:**

```bash
ss -tuln
sudo ss -tulpn | head -20
```

**Explanation:** Shows all TCP/UDP sockets in LISTEN state. `-p` maps sockets to processes — essential for "what owns port 8080?"

**Expected output:**

```text
Netid State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process
tcp   LISTEN 0      128    0.0.0.0:22          0.0.0.0:*
tcp   LISTEN 0      511    127.0.0.1:6379      0.0.0.0:*     users:(("redis-server",pid=1234,fd=6))
```

`0.0.0.0` means all interfaces; `127.0.0.1` is localhost only.

### Step 2 – Observe established connections

**Command:**

```bash
ss -tn state established
curl -s -o /dev/null https://example.com
ss -tn state established '( dport = :443 or sport = :443 )'
```

**Explanation:** Filters ESTABLISHED TCP sockets. After curl, HTTPS connections appear briefly.

**Expected output:**

```text
ESTAB 0 0 10.0.0.42:45678 93.184.216.34:443
```

### Step 3 – Watch the three-way handshake with ss

**Command:**

```bash
# Terminal 1 — start listener
nc -l 9999 &
LISTEN_PID=$!
sleep 1

# Terminal 2 — connect and observe states
ss -tn state syn-recv 2>/dev/null; ss -tn sport = :9999 || true
echo "hello" | nc -127.0.0.1 9999
wait $LISTEN_PID 2>/dev/null || kill $LISTEN_PID 2>/dev/null
```

**Explanation:** Demonstrates LISTEN → ESTABLISHED transition. `syn-recv` may flash too quickly to catch without `tcpdump`.

### Step 4 – Inspect TIME_WAIT accumulation

**Command:**

```bash
ss -tan | awk '/TIME-WAIT/ {count++} END {print "TIME-WAIT:", count+0}'
sysctl net.ipv4.ip_local_port_range
curl -s -o /dev/null http://127.0.0.1:22 2>/dev/null || true
for i in $(seq 1 20); do curl -s -o /dev/null http://example.com; done
ss -tan | awk '/TIME-WAIT/ {count++} END {print "TIME-WAIT after burst:", count+0}'
```

**Explanation:** Short-lived HTTP clients create TIME_WAIT on the initiator side. Ephemeral port range limits concurrent outbound connections.

**Expected output:**

```text
TIME-WAIT: 0
net.ipv4.ip_local_port_range = 32768    60999
TIME-WAIT after burst: 20
```

### Step 5 – UDP socket inspection

**Command:**

```bash
ss -uln
dig +short example.com @8.8.8.8
ss -un state established 2>/dev/null | head -5
```

**Explanation:** UDP "connections" appear only when connected UDP socket used; connectionless DNS queries may not show as ESTABLISHED.

**Expected output:**

```text
UNCONN 0 0 0.0.0.0:68 0.0.0.0:*   # DHCP client
UNCONN 0 0 127.0.0.53:53 0.0.0.0:*
```

### Step 6 – Compare ss and netstat

**Command:**

```bash
ss -tln | wc -l
netstat -tln 2>/dev/null | wc -l || echo "netstat not installed"
time ss -tan >/dev/null
time netstat -tan >/dev/null 2>&1 || true
```

**Explanation:** Line counts should be similar. `ss` typically completes faster on busy servers with thousands of sockets.

### Step 7 – Diagnose "connection refused" vs "timeout"

**Command:**

```bash
# Refused — nothing listening
nc -zv -w 2 127.0.0.1 19999 2>&1 || true

# Timeout — filtered (try non-routable or firewalled)
nc -zv -w 2 10.255.255.1 443 2>&1 || true
```

**Explanation:** **Connection refused** = RST from host (port closed). **Timeout** = no SYN-ACK (firewall drop or routing blackhole).

**Expected output:**

```text
nc: connect to 127.0.0.1 port 19999 (tcp) failed: Connection refused
nc: connect to 10.255.255.1 port 443 (tcp) timed out: Operation now in progress
```

### Step 8 – TCP internal metrics with ss -i

**Command:**

```bash
ss -ti state established | head -30
```

**Explanation:** Shows RTT, congestion window (cwnd), retransmission counts — valuable for latency debugging without packet capture.

**Expected output:**

```text
ESTAB 0 0 10.0.0.42:22 203.0.113.50:52134
	 cubic wscale:7,7 rto:204 rtt:12.5/6.2 cwnd:10
```

## Commands & Code

| Command | Description | Example |
|---------|-------------|---------|
| `ss -tuln` | TCP/UDP listening ports (numeric) | `ss -tuln` |
| `ss -tulpn` | Include process names | `sudo ss -tulpn` |
| `ss -tn state established` | Filter by TCP state | `ss -tn state time-wait` |
| `ss -ti` | TCP info (RTT, cwnd) | `ss -ti dst 10.0.0.5` |
| `ss -s` | Socket usage summary | `ss -s` |
| `netstat -tulpn` | Legacy socket listing | Prefer `ss` |
| `lsof -i :PORT` | Process using port | `sudo lsof -i :8080` |
| `nc -l PORT` | Listen on TCP port | `nc -l 8080` |
| `nc HOST PORT` | Connect to TCP port | `nc -zv host 443` |
| `sysctl net.ipv4.ip_local_port_range` | Ephemeral port range | Tune for high churn |
| `sysctl net.ipv4.tcp_fin_timeout` | FIN-WAIT-2 timeout | Default 60s |

### Connection state audit script

```bash
#!/usr/bin/env bash
# tcp-state-audit.sh — summarize TCP states for capacity planning
set -euo pipefail

echo "=== TCP State Summary ==="
ss -tan | awk 'NR>1 {state[$1]++} END {for (s in state) printf "%-12s %d\n", s, state[s]}' | sort -k2 -rn

echo ""
echo "=== Top TIME-WAIT local ports ==="
ss -tan state time-wait | awk 'NR>1 {print $4}' | sed 's/.*://' | sort | uniq -c | sort -rn | head -10

echo ""
echo "=== Socket summary ==="
ss -s
```

### Simple TCP echo server (Python lab)

```python
#!/usr/bin/env python3
"""Minimal TCP server for handshake observation — lab use only."""
import socket

HOST, PORT = "0.0.0.0", 9090
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Listening on {PORT}...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected from {addr}")
        data = conn.recv(1024)
        conn.sendall(b"echo:" + data)
```

Run: `python3 tcp_echo.py` then `echo test | nc localhost 9090`

## Common Mistakes

!!! warning "Binding to wrong interface"
    Service on `127.0.0.1:8080` is unreachable remotely. Use `0.0.0.0` or specific production IP — document the choice in runbooks.

!!! warning "Ignoring CLOSE-WAIT accumulation"
    High CLOSE-WAIT means application isn't closing sockets after client disconnect — leads to FD exhaustion. Fix the app, not sysctl.

!!! warning "Enabling tcp_tw_recycle (removed in kernel 4.12+)"
    Historical advice is obsolete and broke NAT. Use `tcp_tw_reuse` judiciously and prefer keep-alive / connection pooling.

!!! warning "Assuming UDP 'connection refused'"
    UDP has no handshake — `nc -u` may report ICMP port unreachable, but silent drops are common. Application-level timeouts required.

!!! warning "Using netstat on busy hosts in production"
    `netstat` scans `/proc` linearly — can stall on 100k+ sockets. Use `ss`.

## Best Practices

!!! tip "Use connection pooling for microservices"
    Short-lived TCP per request creates TIME_WAIT storms. HTTP keep-alive, gRPC channels, and database pools reduce handshake overhead.

!!! tip "Monitor ss -s in dashboards"
    Track TCP alloc, orphan sockets, and TIME-WAIT counts. Alert on abnormal CLOSE-WAIT growth.

!!! tip "Document port registry per environment"
    Maintain a table of which service owns which port — prevents conflicts during deployments.

!!! tip "Test with nc before blaming applications"
    `nc -zv host port` isolates transport from HTTP/TLS layers quickly.

!!! tip "Set sensible somaxconn and backlog"
    High-traffic listeners need `net.core.somaxconn` and application backlog aligned — SYN drops under load indicate mismatch.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | No listener on port | Verify with `ss -tlnp`; start service; check bind address |
| `Connection timed out` | Firewall drop, routing, or host down | Check SG/iptables; traceroute; verify target UP |
| `Address already in use` | Port conflict or TIME_WAIT on same 4-tuple | `ss -tlnp`; enable `SO_REUSEADDR`; wait or tune ports |
| Too many TIME-WAIT | High short-lived client connections | Enable keep-alive; pool connections; widen ephemeral range |
| High CLOSE-WAIT | Application not closing sockets | Fix code; restart service; inspect with `ss -tan state close-wait` |
| `Cannot assign requested address` | Wrong source IP or exhausted ports | Check `ip addr`; expand `ip_local_port_range` |
| SYN flood / backlog drops | `somaxconn` too low or attack | Increase backlog; enable SYN cookies; rate limit at edge |
| Slow TCP on long fat networks | Small window without scaling | Verify window scaling enabled; check `ss -ti` cwnd |
| UDP application hangs | Silent packet loss | Implement timeouts and retries at app layer |

## Summary

- **TCP** provides reliable delivery via three-way handshake, sequence numbers, and stateful connections
- **UDP** is connectionless — ideal for DNS, NTP, and latency-sensitive workloads where app handles reliability
- **Ports** identify services; **sockets** are full 5-tuple endpoints managed as file descriptors
- **TIME_WAIT** protects against stale segments — manage it on high-churn clients and load balancers
- Use **`ss`** as the primary inspection tool; interpret states (ESTABLISHED, CLOSE-WAIT, TIME-WAIT) for root cause
- **Connection refused** vs **timeout** tells you whether the target host responded or traffic was filtered

## Interview Questions

1. Walk through the TCP three-way handshake.
2. What is TIME_WAIT and why does it exist?
3. When would you choose UDP over TCP?
4. Explain the difference between a port and a socket.
5. What does a high CLOSE-WAIT count indicate?
6. How do you find which process is listening on port 8080?
7. What is the difference between `Connection refused` and `Connection timed out`?
8. Why is `ss` preferred over `netstat` on modern Linux?
9. What are ephemeral ports and why do they matter for outbound connections?
10. How does TCP flow control differ from congestion control?

??? tip "Sample Answers (Questions 1, 2, and 7)"

    **Q1 — Three-way handshake:** Client sends SYN with initial sequence X. Server responds SYN-ACK with sequence Y and ack X+1. Client sends ACK with ack Y+1. Both sides now have synchronized sequence numbers and enter ESTABLISHED. Data transfer can begin.

    **Q2 — TIME_WAIT:** After actively closing a TCP connection, the side that sent the first FIN waits 2×MSL before releasing the 4-tuple. This ensures delayed segments from the old connection expire and prevents confusing a new connection using the same ports. Trade-off: consumes memory and ephemeral ports on high-churn clients.

    **Q7 — Refused vs timeout:** Refused means the target host received the SYN and returned RST because no process listens on that port — the host is reachable. Timeout means no SYN-ACK arrived within the timeout — firewall filtering, routing failure, or dead host. Different remediation paths.

## Related Tutorials

- [Networking – Category Overview](index.md)
- [ICMP, ARP, DHCP, and Network Services](icmp-arp-dhcp-and-network-services.md) *(Module 2)*
- [DNS Fundamentals](dns-fundamentals.md) *(next in Module 3)*
- [Linux Networking Essentials](../linux/linux-networking-essentials.md)
- [HTTP, HTTPS, and the Application Layer](http-https-and-application-layer.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [RFC 793 — TCP](https://www.rfc-editor.org/rfc/rfc793)
- [RFC 768 — UDP](https://www.rfc-editor.org/rfc/rfc768)
- [ss man page](https://man7.org/linux/man-pages/man8/ss.8.html)
- [Linux TCP/IP stack tuning](https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt)
- [IANA Service Name and Transport Protocol Port Number Registry](https://www.iana.org/assignments/service-names-port-numbers/)
- [REBASH Academy – Networking Overview](index.md)
