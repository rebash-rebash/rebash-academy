---
title: Overview
description: "REBASH Networking Mastery — practical networking for Linux, Cloud, Kubernetes, DevOps, and enterprise engineers. 15 modules, production labs, and capstone projects."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "2026-08-10"
category: networking
tags:
  - networking
  - devops
  - cloud
  - kubernetes
  - linux
  - rebash-networking-mastery
comments: false
---

# REBASH Networking Mastery

**Duration:** 8–10 weeks · **Lessons:** ~130 · **Labs / projects:** 40+ planned · **Capstones:** 8

The most practical networking course for **Linux, Cloud, Kubernetes, DevOps, and enterprise engineers**.
Typical networking courses stop at theory — this path trains **production network engineers**.

!!! tip "How this course works"
    Modules build in order. Scaffolded lessons show structure and SEO; full tutorials
    (theory + lab + interview) publish as they are completed. Prefer a Linux lab VM plus
    optional cloud sandbox accounts for Modules 10–13.

## Who this is for

Beginners → network operators → DevOps → Cloud → Kubernetes / Platform / SRE engineers who need
networking that transfers to Linux hosts, containers, and multi-cloud platforms.

## Learning roadmap

1. **Fundamentals & addressing** — Modules 1–3  
2. **Switching & routing** — Modules 4–5  
3. **Services & perimeter** — Modules 6–8  
4. **Linux & cloud platforms** — Modules 9–10  
5. **Kubernetes & troubleshooting** — Modules 11–12  
6. **DevOps & production** — Modules 13–14  
7. **Capstones** — Module 15  

## Modules

### Module 1 · Networking Fundamentals

**Goal:** Build a mental model of how networks move data end to end.

**Lab / project focus:** Map a small home or lab network and identify devices, addresses, and ports.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [What is Networking?](introduction-to-networking.md) | Beginner | Ready |
| 2 | [Types of Networks (LAN, WAN, MAN, PAN)](types-of-networks.md) | Beginner | Ready |
| 3 | [Network Topologies](network-topologies.md) | Beginner | Ready |
| 4 | [OSI Model](osi-model.md) | Beginner | Ready |
| 5 | [TCP/IP Model](tcp-ip-model.md) | Beginner | Ready |
| 6 | [Data Encapsulation](data-encapsulation.md) | Beginner | Ready |
| 7 | [MAC Address](mac-address.md) | Beginner | Ready |
| 8 | [IP Address](ip-addressing.md) | Beginner | Ready |
| 9 | [Ports and Protocols](ports-and-protocols.md) | Beginner | Ready |
| 10 | [Networking Devices](networking-devices.md) | Beginner | Ready |
| — | [Module 1 Summary — Networking Fundamentals](module-1-networking-fundamentals-summary.md) | Beginner | Ready |

!!! success "Module 1 complete"
    All ten **Networking Fundamentals** tutorials plus the
    [Module 1 summary](module-1-networking-fundamentals-summary.md) are published.
    Continue with [Binary Numbers](binary-numbers.md) (Module 2 · IPv4 Addressing).

### Module 2 · IPv4 Addressing

**Goal:** Design and calculate IPv4 networks used in labs and production.

**Lab / project focus:** Subnet a /24 into usable segments for servers, clients, and management.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Binary Numbers](binary-numbers.md) | Beginner | Ready |
| 2 | [IPv4 Address Structure](ipv4-address-structure.md) | Beginner | Ready |
| 3 | [IPv4 Classes](ipv4-classes.md) | Beginner | Ready |
| 4 | [Private vs Public IP](private-vs-public-ip.md) | Beginner | Ready |
| 5 | [Loopback](loopback.md) | Beginner | Ready |
| 6 | [APIPA](apipa.md) | Beginner | Ready |
| 7 | [CIDR](cidr.md) | Intermediate | Ready |
| 8 | [Subnetting](subnetting-and-vlsm.md) | Intermediate | Ready |
| 9 | [VLSM](vlsm.md) | Intermediate | Ready |
| 10 | [Supernetting](supernetting.md) | Intermediate | Ready |
| — | [Module 2 Summary — IPv4 Addressing](module-2-ipv4-addressing-summary.md) | Intermediate | Ready |

!!! success "Module 2 complete"
    All ten **IPv4 Addressing** tutorials plus the
    [Module 2 summary](module-2-ipv4-addressing-summary.md) are published.
    Continue with [Why IPv6](why-ipv6.md) (Module 3 · IPv6).

### Module 3 · IPv6

**Goal:** Operate dual-stack and IPv6-first networks with confidence.

**Lab / project focus:** Enable IPv6 on a lab host and verify addressing, neighbour discovery, and reachability.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Why IPv6](why-ipv6.md) | Beginner | Ready |
| 2 | [IPv6 Structure](ipv6-structure.md) | Beginner | Ready |
| 3 | [Types of IPv6 Addresses](ipv6-address-types.md) | Beginner | Ready |
| 4 | [SLAAC](slaac.md) | Beginner | Ready |
| 5 | [Neighbor Discovery](neighbor-discovery.md) | Intermediate | Ready |
| 6 | [IPv6 Routing](ipv6-routing.md) | Intermediate | Ready |
| 7 | [IPv4 vs IPv6](ipv4-vs-ipv6.md) | Beginner | Ready |
| — | [Module 3 Summary — IPv6](module-3-ipv6-summary.md) | Intermediate | Ready |

!!! success "Module 3 complete"
    All seven **IPv6** tutorials plus the
    [Module 3 summary](module-3-ipv6-summary.md) are published.
    Continue with [Ethernet](ethernet-switching-and-vlans.md) (Module 4 · Switching).

### Module 4 · Switching

**Goal:** Segment Layer 2 networks with VLANs, trunks, and resilient links.

**Lab / project focus:** Build a multi-VLAN switch topology with trunking and inter-VLAN routing.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Ethernet](ethernet-switching-and-vlans.md) | Beginner | Ready |
| 2 | [MAC Address Table](mac-address-table.md) | Beginner | Ready |
| 3 | [Switch Learning](switch-learning.md) | Beginner | Ready |
| 4 | [VLAN](vlan.md) | Beginner | Ready |
| 5 | [Trunking](trunking.md) | Intermediate | Ready |
| 6 | [STP](spanning-tree-protocol.md) | Intermediate | Ready |
| 7 | [EtherChannel](etherchannel.md) | Intermediate | Ready |
| 8 | [Inter-VLAN Routing](inter-vlan-routing.md) | Intermediate | Scaffolded |
| — | [Module 4 Summary — Switching](module-4-switching-summary.md) | Intermediate | Ready |

!!! tip "Module 4 in progress"
    Lessons 1–7 and the [Module 4 summary](module-4-switching-summary.md) are published.
    Publish [Inter-VLAN Routing](inter-vlan-routing.md) to complete Module 4.

### Module 5 · Routing

**Goal:** Move packets between networks with static and dynamic routing.

**Lab / project focus:** Configure static routes and observe a simple dynamic routing exchange in the lab.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Routing Basics](routing-fundamentals.md) | Beginner | Ready |
| 2 | [Static Routing](static-routing.md) | Beginner | Ready |
| 3 | [Dynamic Routing](dynamic-routing.md) | Intermediate | Ready |
| 4 | [RIP](rip.md) | Beginner | Ready |
| 5 | [OSPF](ospf.md) | Intermediate | Ready |
| 6 | [EIGRP Concepts](eigrp-concepts.md) | Intermediate | Ready |
| 7 | [BGP Introduction](bgp-introduction.md) | Advanced | Ready |
| 8 | [Default Routes](default-routes.md) | Beginner | Ready |
| 9 | [Route Summarization](route-summarization.md) | Intermediate | Ready |
| 10 | [Route Redistribution](route-redistribution.md) | Advanced | Ready |
| — | [Module 5 Summary — Routing](module-5-routing-summary.md) | Intermediate | Ready |

!!! success "Module 5 complete"
    All ten **Routing** tutorials plus the
    [Module 5 summary](module-5-routing-summary.md) are published.
    Continue with [DNS Fundamentals](dns-fundamentals.md) (Module 6 · DNS and DHCP).

### Module 6 · DNS and DHCP

**Goal:** Run name resolution and address assignment like a production operator.

**Lab / project focus:** Trace a DNS lookup and capture a DHCP handshake in the lab.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [DNS Fundamentals](dns-fundamentals.md) | Beginner | Ready |
| 2 | [DNS Records](dns-records-and-troubleshooting.md) | Beginner | Ready |
| 3 | [DNS Resolution](dns-resolution.md) | Beginner | Ready |
| 4 | [DHCP Process](icmp-arp-dhcp-and-network-services.md) | Beginner | Ready |
| 5 | [DHCP Relay](dhcp-relay.md) | Intermediate | Ready |
| 6 | [Split DNS](split-dns.md) | Intermediate | Ready |
| 7 | [DNS Troubleshooting](dns-troubleshooting.md) | Intermediate | Ready |
| — | [Module 6 Summary — DNS & DHCP](module-6-dns-dhcp-summary.md) | Intermediate | Ready |

!!! success "Module 6 complete"
    All seven **DNS and DHCP** tutorials plus the
    [Module 6 summary](module-6-dns-dhcp-summary.md) are published.
    Continue with [NAT](nat-and-port-forwarding.md) (Module 7 · NAT and Firewalls).

### Module 7 · NAT and Firewalls

**Goal:** Control address translation and traffic policy on Linux and in the cloud.

**Lab / project focus:** Configure NAT/PAT and a restrictive firewall policy for a lab subnet.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [NAT](nat-and-port-forwarding.md) | Beginner | Ready |
| 2 | [PAT](pat.md) | Beginner | Ready |
| 3 | [Static NAT](static-nat.md) | Beginner | Ready |
| 4 | [Dynamic NAT](dynamic-nat.md) | Intermediate | Ready |
| 5 | [ACL](acl.md) | Intermediate | Ready |
| 6 | [Firewall Basics](firewalls-and-access-control.md) | Beginner | Ready |
| 7 | [Stateful Firewalls](stateful-firewalls.md) | Intermediate | Ready |
| 8 | [Linux Firewall](linux-firewall.md) | Intermediate | Ready |
| 9 | [Cloud Firewalls](cloud-firewalls.md) | Intermediate | Ready |
| 10 | [Security Groups](security-groups.md) | Intermediate | Ready |
| — | [Module 7 Summary — NAT & Firewalls](module-7-nat-firewalls-summary.md) | Intermediate | Ready |

!!! success "Module 7 complete"
    All ten **NAT and Firewalls** tutorials plus the
    [Module 7 summary](module-7-nat-firewalls-summary.md) are published.
    Continue with [VPN](vpn-and-tunneling-basics.md) (Module 8 · Network Security).

### Module 8 · Network Security

**Goal:** Secure paths, identities, and trust boundaries across the network.

**Lab / project focus:** Stand up a VPN path and apply a basic segmentation and hardening checklist.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [VPN](vpn-and-tunneling-basics.md) | Beginner | Ready |
| 2 | [IPSec](ipsec.md) | Intermediate | Ready |
| 3 | [SSL/TLS](ssl-tls.md) | Beginner | Ready |
| 4 | [SSH](ssh-networking.md) | Beginner | Ready |
| 5 | [Network Hardening](network-security-hardening.md) | Intermediate | Ready |
| 6 | [IDS/IPS](ids-ips.md) | Intermediate | Ready |
| 7 | [Zero Trust](zero-trust.md) | Intermediate | Ready |
| 8 | [Network Segmentation](network-segmentation-and-trust-boundaries.md) | Intermediate | Ready |
| 9 | [DDoS Protection](ddos-protection.md) | Intermediate | Ready |
| — | [Module 8 Summary — Network Security](module-8-network-security-summary.md) | Intermediate | Ready |

!!! success "Module 8 complete"
    All nine **Network Security** tutorials plus the
    [Module 8 summary](module-8-network-security-summary.md) are published.
    Continue with [ip Command](linux-networking-toolkit.md) (Module 9 · Linux Networking).

### Module 9 · Linux Networking

**Goal:** Diagnose and configure networking from the Linux command line.

**Lab / project focus:** Use ip, ss, dig, and tcpdump to prove connectivity and capture a flow.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [ip Command](linux-networking-toolkit.md) | Beginner | Ready |
| 2 | [ss](ss.md) | Beginner | Ready |
| 3 | [netstat](netstat.md) | Beginner | Ready |
| 4 | [tcpdump](packet-analysis-tcpdump-wireshark.md) | Intermediate | Ready |
| 5 | [traceroute](traceroute.md) | Beginner | Ready |
| 6 | [dig](dig.md) | Beginner | Ready |
| 7 | [nslookup](nslookup.md) | Beginner | Ready |
| 8 | [curl](curl.md) | Beginner | Ready |
| 9 | [wget](wget.md) | Beginner | Ready |
| 10 | [Network Namespaces](network-namespaces.md) | Intermediate | Ready |
| — | [Module 9 Summary — Linux Networking](module-9-linux-networking-summary.md) | Intermediate | Ready |

!!! success "Module 9 complete"
    All ten **Linux Networking** tutorials plus the
    [Module 9 summary](module-9-linux-networking-summary.md) are published.
    Continue with [AWS VPC](cloud-networking-vpc-and-subnets.md) (Module 10 · Cloud Networking).

### Module 10 · Cloud Networking

**Goal:** Design VPCs/VNets with public, private, and hybrid connectivity patterns.

**Lab / project focus:** Design a multi-tier VPC with public/private subnets, NAT, and a load balancer.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [AWS VPC](cloud-networking-vpc-and-subnets.md) | Intermediate | Ready |
| 2 | [Azure VNet](azure-vnet.md) | Intermediate | Ready |
| 3 | [GCP VPC](gcp-vpc.md) | Intermediate | Ready |
| 4 | [Subnets](cloud-subnets.md) | Intermediate | Ready |
| 5 | [Route Tables](route-tables.md) | Intermediate | Ready |
| 6 | [NAT Gateway](nat-gateway.md) | Intermediate | Ready |
| 7 | [Internet Gateway](internet-gateway.md) | Intermediate | Ready |
| 8 | [Load Balancer](cloud-load-balancer.md) | Intermediate | Ready |
| 9 | [Private Connectivity](private-connectivity.md) | Intermediate | Ready |
| 10 | [Hybrid Networking](hybrid-networking.md) | Advanced | Ready |
| — | [Module 10 Summary — Cloud Networking](module-10-cloud-networking-summary.md) | Intermediate | Ready |

!!! success "Module 10 complete"
    All ten **Cloud Networking** tutorials plus the
    [Module 10 summary](module-10-cloud-networking-summary.md) are published.
    Continue with [CNI](kubernetes-networking-fundamentals.md) (Module 11 · Kubernetes Networking).

### Module 11 · Kubernetes Networking

**Goal:** Understand how pods, Services, Ingress, and policies move traffic in a cluster.

**Lab / project focus:** Trace ClusterIP → node → pod traffic and apply a NetworkPolicy.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [CNI](kubernetes-networking-fundamentals.md) | Advanced | Ready |
| 2 | [Pod Networking](pod-networking.md) | Advanced | Ready |
| 3 | [Service Networking](service-networking.md) | Advanced | Ready |
| 4 | [Ingress](ingress.md) | Advanced | Ready |
| 5 | [Network Policies](network-policies.md) | Advanced | Ready |
| 6 | [CoreDNS](coredns.md) | Advanced | Ready |
| 7 | [kube-proxy](kube-proxy.md) | Advanced | Ready |
| 8 | [Service Mesh](service-mesh.md) | Advanced | Ready |
| 9 | [eBPF](ebpf.md) | Advanced | Ready |
| — | [Module 11 Summary — Kubernetes Networking](module-11-kubernetes-networking-summary.md) | Advanced | Ready |

!!! success "Module 11 complete"
    All nine **Kubernetes Networking** tutorials plus the
    [Module 11 summary](module-11-kubernetes-networking-summary.md) are published.
    Continue with [Ping](ping.md) (Module 12 · Network Troubleshooting).

### Module 12 · Network Troubleshooting

**Goal:** Isolate connectivity failures with a repeatable production method.

**Lab / project focus:** Work a packet-loss or DNS failure scenario from symptom to root cause.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Ping](ping.md) | Intermediate | Ready |
| 2 | [traceroute](traceroute-troubleshooting.md) | Intermediate | Ready |
| 3 | [tcpdump](tcpdump-troubleshooting.md) | Advanced | Ready |
| 4 | [Wireshark](wireshark.md) | Advanced | Ready |
| 5 | [DNS Troubleshooting](dns-troubleshooting-deep-dive.md) | Advanced | Ready |
| 6 | [Routing Issues](routing-issues.md) | Advanced | Ready |
| 7 | [MTU Problems](mtu-problems.md) | Advanced | Ready |
| 8 | [Latency](latency.md) | Advanced | Ready |
| 9 | [Packet Loss](packet-loss.md) | Advanced | Ready |
| 10 | [Production Scenarios](production-scenarios.md) | Advanced | Ready |
| — | [Module 12 Summary — Network Troubleshooting](module-12-network-troubleshooting-summary.md) | Advanced | Ready |

!!! success "Module 12 complete"
    All ten **Network Troubleshooting** tutorials plus the
    [Module 12 summary](module-12-network-troubleshooting-summary.md) are published.
    Continue with [Docker Networking](docker-networking.md) (Module 13 · DevOps Networking).

### Module 13 · DevOps Networking

**Goal:** Connect containers, CI/CD, proxies, and discovery for delivery platforms.

**Lab / project focus:** Map traffic from a CI runner through a reverse proxy to a containerised app.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [Docker Networking](docker-networking.md) | Intermediate | Ready |
| 2 | [Kubernetes Networking](kubernetes-networking-devops.md) | Advanced | Ready |
| 3 | [CI/CD Networking](cicd-networking.md) | Advanced | Ready |
| 4 | [Git Networking](git-networking.md) | Intermediate | Ready |
| 5 | [VPN for DevOps](vpn-for-devops.md) | Intermediate | Ready |
| 6 | [Reverse Proxy](reverse-proxy-and-ingress-basics.md) | Advanced | Ready |
| 7 | [Load Balancing](load-balancing-fundamentals.md) | Advanced | Ready |
| 8 | [CDN](cdn.md) | Intermediate | Ready |
| 9 | [API Gateways](api-gateways.md) | Advanced | Ready |
| 10 | [Service Discovery](service-discovery.md) | Advanced | Ready |
| — | [Module 13 Summary — DevOps Networking](module-13-devops-networking-summary.md) | Advanced | Ready |

!!! success "Module 13 complete"
    All ten **DevOps Networking** tutorials plus the
    [Module 13 summary](module-13-devops-networking-summary.md) are published.
    Continue with [High Availability](high-availability.md) (Module 14 · Production Networking).

### Module 14 · Production Networking

**Goal:** Run networks with HA, monitoring, DR, automation, and clear checklists.

**Lab / project focus:** Complete a production readiness review and an incident response drill.


| # | Lesson | Level | Status |
|---|--------|-------|--------|
| 1 | [High Availability](high-availability.md) | Advanced | Ready |
| 2 | [Redundancy](redundancy.md) | Advanced | Ready |
| 3 | [Network Monitoring](network-monitoring.md) | Advanced | Ready |
| 4 | [Capacity Planning](capacity-planning.md) | Advanced | Ready |
| 5 | [Disaster Recovery](disaster-recovery.md) | Advanced | Ready |
| 6 | [Incident Response](network-incident-response-and-observability.md) | Advanced | Ready |
| 7 | [Network Automation](network-automation-and-monitoring.md) | Advanced | Ready |
| 8 | [Best Practices](networking-best-practices.md) | Advanced | Ready |
| 9 | [Production Checklists](production-checklists.md) | Intermediate | Ready |
| 10 | [Troubleshooting Methodology](network-troubleshooting-methodology.md) | Advanced | Ready |
| — | [Module 14 Summary — Production Networking](module-14-production-networking-summary.md) | Advanced | Ready |

!!! success "Module 14 complete"
    All ten **Production Networking** tutorials plus the
    [Module 14 summary](module-14-production-networking-summary.md) are published.
    Continue with [Build a Home Lab Network](projects/home-lab-network.md) (Module 15 · Capstone Projects).

## Capstone projects (Module 15)

| # | Project | Level | Status |
|---|---------|-------|--------|
| 1 | [Build a Home Lab Network](projects/home-lab-network.md) | Advanced | Ready |
| 2 | [Configure VLANs](projects/configure-vlans.md) | Advanced | Ready |
| 3 | [Build a DNS Server](projects/build-dns-server.md) | Advanced | Ready |
| 4 | [Configure a DHCP Server](projects/configure-dhcp-server.md) | Advanced | Ready |
| 5 | [Build a VPN Server](projects/build-vpn-server.md) | Advanced | Ready |
| 6 | [Create a Firewall Gateway](projects/firewall-gateway.md) | Advanced | Ready |
| 7 | [Cloud VPC Design](projects/cloud-vpc-design.md) | Advanced | Ready |
| 8 | [Enterprise Network Troubleshooting Challenge](projects/enterprise-network-troubleshooting-challenge.md) | Expert | Ready |

!!! success "Networking Mastery complete"
    All eight **Capstone Projects** are published. Start with
    [Build a Home Lab Network](projects/home-lab-network.md), or jump to the final
    [Enterprise Network Troubleshooting Challenge](projects/enterprise-network-troubleshooting-challenge.md).
    Continue with [Networking Interview Prep](interview/index.md).

## Prerequisites

Basic computer literacy and comfort with a Linux terminal. A disposable Ubuntu LTS lab VM
(and optional AWS/Azure/GCP sandbox) with snapshots.

## Related

- [Linux Mastery](../linux/index.md)
- [DevOps Engineer learning path](../learning-paths/devops-engineer/index.md)
- [Cloud Engineer learning path](../learning-paths/cloud-engineer/index.md)
- [Networking interview prep](interview/index.md)
