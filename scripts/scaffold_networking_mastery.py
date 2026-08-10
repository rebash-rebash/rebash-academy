#!/usr/bin/env python3
"""Scaffold REBASH Networking Mastery (15 modules) — stubs + nav + curriculum wiring.

Existing full tutorials are reused as anchors when titles/slugs align.
New lessons get SEO-ready stub pages. Bodies are filled when tutorials are supplied.
"""

from __future__ import annotations

from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parent.parent
NET = ROOT / "docs" / "networking"
CURRICULUM = ROOT / "curriculum.yaml"

# Lesson slug → existing filename to keep (do not overwrite body)
REUSE: dict[str, str] = {
    "what-is-networking": "introduction-to-networking.md",
    "osi-model": "osi-model.md",
    "tcp-ip-model": "tcp-ip-model.md",
    "ip-address": "ip-addressing.md",
    "subnetting": "subnetting-and-vlsm.md",
    "routing-basics": "routing-fundamentals.md",
    "ethernet": "ethernet-switching-and-vlans.md",
    "dhcp-process": "icmp-arp-dhcp-and-network-services.md",
    "dns-fundamentals": "dns-fundamentals.md",
    "dns-records": "dns-records-and-troubleshooting.md",
    "nat": "nat-and-port-forwarding.md",
    "firewall-basics": "firewalls-and-access-control.md",
    "vpn": "vpn-and-tunneling-basics.md",
    "network-hardening": "network-security-hardening.md",
    "network-segmentation": "network-segmentation-and-trust-boundaries.md",
    "ip-command": "linux-networking-toolkit.md",
    "tcpdump": "packet-analysis-tcpdump-wireshark.md",
    "aws-vpc": "cloud-networking-vpc-and-subnets.md",
    "cni": "kubernetes-networking-fundamentals.md",
    "ping": "network-troubleshooting-methodology.md",
    "docker-networking": "load-balancing-fundamentals.md",  # wrong — remove
    "reverse-proxy": "reverse-proxy-and-ingress-basics.md",
    "load-balancing": "load-balancing-fundamentals.md",
    "network-automation": "network-automation-and-monitoring.md",
    "incident-response": "network-incident-response-and-observability.md",
    "troubleshooting-methodology": "network-troubleshooting-methodology.md",
}

# Fix mistaken mapping above
del REUSE["docker-networking"]
# ping should not steal troubleshooting methodology — leave methodology for Module 14
del REUSE["ping"]

MODULES: list[dict] = [
    {
        "id": "networking-m1",
        "title": "Module 1 · Networking Fundamentals",
        "goal": "Build a mental model of how networks move data end to end.",
        "lab": "Map a small home or lab network and identify devices, addresses, and ports.",
        "lessons": [
            ("what-is-networking", "What is Networking?", "beginner"),
            ("types-of-networks", "Types of Networks (LAN, WAN, MAN, PAN)", "beginner"),
            ("network-topologies", "Network Topologies", "beginner"),
            ("osi-model", "OSI Model", "beginner"),
            ("tcp-ip-model", "TCP/IP Model", "beginner"),
            ("data-encapsulation", "Data Encapsulation", "beginner"),
            ("mac-address", "MAC Address", "beginner"),
            ("ip-address", "IP Address", "beginner"),
            ("ports-and-protocols", "Ports and Protocols", "beginner"),
            ("networking-devices", "Networking Devices", "beginner"),
        ],
    },
    {
        "id": "networking-m2",
        "title": "Module 2 · IPv4 Addressing",
        "goal": "Design and calculate IPv4 networks used in labs and production.",
        "lab": "Subnet a /24 into usable segments for servers, clients, and management.",
        "lessons": [
            ("binary-numbers", "Binary Numbers", "beginner"),
            ("ipv4-address-structure", "IPv4 Address Structure", "beginner"),
            ("ipv4-classes", "IPv4 Classes", "beginner"),
            ("private-vs-public-ip", "Private vs Public IP", "beginner"),
            ("loopback", "Loopback", "beginner"),
            ("apipa", "APIPA", "beginner"),
            ("cidr", "CIDR", "intermediate"),
            ("subnetting", "Subnetting", "intermediate"),
            ("vlsm", "VLSM", "intermediate"),
            ("supernetting", "Supernetting", "intermediate"),
        ],
    },
    {
        "id": "networking-m3",
        "title": "Module 3 · IPv6",
        "goal": "Operate dual-stack and IPv6-first networks with confidence.",
        "lab": "Enable IPv6 on a lab host and verify addressing, neighbour discovery, and reachability.",
        "lessons": [
            ("why-ipv6", "Why IPv6", "beginner"),
            ("ipv6-structure", "IPv6 Structure", "beginner"),
            ("ipv6-address-types", "Types of IPv6 Addresses", "intermediate"),
            ("slaac", "SLAAC", "intermediate"),
            ("neighbor-discovery", "Neighbor Discovery", "intermediate"),
            ("ipv6-routing", "IPv6 Routing", "intermediate"),
            ("ipv4-vs-ipv6", "IPv4 vs IPv6", "beginner"),
        ],
    },
    {
        "id": "networking-m4",
        "title": "Module 4 · Switching",
        "goal": "Segment Layer 2 networks with VLANs, trunks, and resilient links.",
        "lab": "Build a multi-VLAN switch topology with trunking and inter-VLAN routing.",
        "lessons": [
            ("ethernet", "Ethernet", "beginner"),
            ("mac-address-table", "MAC Address Table", "beginner"),
            ("switch-learning", "Switch Learning", "beginner"),
            ("vlan", "VLAN", "intermediate"),
            ("trunking", "Trunking", "intermediate"),
            ("spanning-tree-protocol", "STP", "intermediate"),
            ("etherchannel", "EtherChannel", "intermediate"),
            ("inter-vlan-routing", "Inter-VLAN Routing", "intermediate"),
        ],
    },
    {
        "id": "networking-m5",
        "title": "Module 5 · Routing",
        "goal": "Move packets between networks with static and dynamic routing.",
        "lab": "Configure static routes and observe a simple dynamic routing exchange in the lab.",
        "lessons": [
            ("routing-basics", "Routing Basics", "beginner"),
            ("static-routing", "Static Routing", "beginner"),
            ("dynamic-routing", "Dynamic Routing", "intermediate"),
            ("rip", "RIP", "intermediate"),
            ("ospf", "OSPF", "intermediate"),
            ("eigrp-concepts", "EIGRP Concepts", "intermediate"),
            ("bgp-introduction", "BGP Introduction", "advanced"),
            ("default-routes", "Default Routes", "beginner"),
            ("route-summarization", "Route Summarization", "intermediate"),
            ("route-redistribution", "Route Redistribution", "advanced"),
        ],
    },
    {
        "id": "networking-m6",
        "title": "Module 6 · DNS and DHCP",
        "goal": "Run name resolution and address assignment like a production operator.",
        "lab": "Trace a DNS lookup and capture a DHCP handshake in the lab.",
        "lessons": [
            ("dns-fundamentals", "DNS Fundamentals", "beginner"),
            ("dns-records", "DNS Records", "beginner"),
            ("dns-resolution", "DNS Resolution", "intermediate"),
            ("dhcp-process", "DHCP Process", "beginner"),
            ("dhcp-relay", "DHCP Relay", "intermediate"),
            ("split-dns", "Split DNS", "intermediate"),
            ("dns-troubleshooting", "DNS Troubleshooting", "intermediate"),
        ],
    },
    {
        "id": "networking-m7",
        "title": "Module 7 · NAT and Firewalls",
        "goal": "Control address translation and traffic policy on Linux and in the cloud.",
        "lab": "Configure NAT/PAT and a restrictive firewall policy for a lab subnet.",
        "lessons": [
            ("nat", "NAT", "beginner"),
            ("pat", "PAT", "beginner"),
            ("static-nat", "Static NAT", "intermediate"),
            ("dynamic-nat", "Dynamic NAT", "intermediate"),
            ("acl", "ACL", "intermediate"),
            ("firewall-basics", "Firewall Basics", "beginner"),
            ("stateful-firewalls", "Stateful Firewalls", "intermediate"),
            ("linux-firewall", "Linux Firewall", "intermediate"),
            ("cloud-firewalls", "Cloud Firewalls", "intermediate"),
            ("security-groups", "Security Groups", "intermediate"),
        ],
    },
    {
        "id": "networking-m8",
        "title": "Module 8 · Network Security",
        "goal": "Secure paths, identities, and trust boundaries across the network.",
        "lab": "Stand up a VPN path and apply a basic segmentation and hardening checklist.",
        "lessons": [
            ("vpn", "VPN", "intermediate"),
            ("ipsec", "IPSec", "intermediate"),
            ("ssl-tls", "SSL/TLS", "intermediate"),
            ("ssh-networking", "SSH", "beginner"),
            ("network-hardening", "Network Hardening", "intermediate"),
            ("ids-ips", "IDS/IPS", "intermediate"),
            ("zero-trust", "Zero Trust", "advanced"),
            ("network-segmentation", "Network Segmentation", "intermediate"),
            ("ddos-protection", "DDoS Protection", "advanced"),
        ],
    },
    {
        "id": "networking-m9",
        "title": "Module 9 · Linux Networking",
        "goal": "Diagnose and configure networking from the Linux command line.",
        "lab": "Use ip, ss, dig, and tcpdump to prove connectivity and capture a flow.",
        "lessons": [
            ("ip-command", "ip Command", "beginner"),
            ("ss", "ss", "beginner"),
            ("netstat", "netstat", "beginner"),
            ("tcpdump", "tcpdump", "intermediate"),
            ("traceroute", "traceroute", "beginner"),
            ("dig", "dig", "beginner"),
            ("nslookup", "nslookup", "beginner"),
            ("curl", "curl", "beginner"),
            ("wget", "wget", "beginner"),
            ("network-namespaces", "Network Namespaces", "intermediate"),
        ],
    },
    {
        "id": "networking-m10",
        "title": "Module 10 · Cloud Networking",
        "goal": "Design VPCs/VNets with public, private, and hybrid connectivity patterns.",
        "lab": "Design a multi-tier VPC with public/private subnets, NAT, and a load balancer.",
        "lessons": [
            ("aws-vpc", "AWS VPC", "intermediate"),
            ("azure-vnet", "Azure VNet", "intermediate"),
            ("gcp-vpc", "GCP VPC", "intermediate"),
            ("cloud-subnets", "Subnets", "intermediate"),
            ("route-tables", "Route Tables", "intermediate"),
            ("nat-gateway", "NAT Gateway", "intermediate"),
            ("internet-gateway", "Internet Gateway", "intermediate"),
            ("cloud-load-balancer", "Load Balancer", "intermediate"),
            ("private-connectivity", "Private Connectivity", "advanced"),
            ("hybrid-networking", "Hybrid Networking", "advanced"),
        ],
    },
    {
        "id": "networking-m11",
        "title": "Module 11 · Kubernetes Networking",
        "goal": "Understand how pods, Services, Ingress, and policies move traffic in a cluster.",
        "lab": "Trace ClusterIP → node → pod traffic and apply a NetworkPolicy.",
        "lessons": [
            ("cni", "CNI", "intermediate"),
            ("pod-networking", "Pod Networking", "intermediate"),
            ("service-networking", "Service Networking", "intermediate"),
            ("ingress", "Ingress", "intermediate"),
            ("network-policies", "Network Policies", "intermediate"),
            ("coredns", "CoreDNS", "intermediate"),
            ("kube-proxy", "kube-proxy", "intermediate"),
            ("service-mesh", "Service Mesh", "advanced"),
            ("ebpf", "eBPF", "advanced"),
        ],
    },
    {
        "id": "networking-m12",
        "title": "Module 12 · Network Troubleshooting",
        "goal": "Isolate connectivity failures with a repeatable production method.",
        "lab": "Work a packet-loss or DNS failure scenario from symptom to root cause.",
        "lessons": [
            ("ping", "Ping", "beginner"),
            ("traceroute-troubleshooting", "traceroute", "beginner"),
            ("tcpdump-troubleshooting", "tcpdump", "intermediate"),
            ("wireshark", "Wireshark", "intermediate"),
            ("dns-troubleshooting-deep-dive", "DNS Troubleshooting", "intermediate"),
            ("routing-issues", "Routing Issues", "intermediate"),
            ("mtu-problems", "MTU Problems", "intermediate"),
            ("latency", "Latency", "intermediate"),
            ("packet-loss", "Packet Loss", "intermediate"),
            ("production-scenarios", "Production Scenarios", "advanced"),
        ],
    },
    {
        "id": "networking-m13",
        "title": "Module 13 · DevOps Networking",
        "goal": "Connect containers, CI/CD, proxies, and discovery for delivery platforms.",
        "lab": "Map traffic from a CI runner through a reverse proxy to a containerised app.",
        "lessons": [
            ("docker-networking", "Docker Networking", "intermediate"),
            ("kubernetes-networking-devops", "Kubernetes Networking", "intermediate"),
            ("cicd-networking", "CI/CD Networking", "intermediate"),
            ("git-networking", "Git Networking", "beginner"),
            ("vpn-for-devops", "VPN for DevOps", "intermediate"),
            ("reverse-proxy", "Reverse Proxy", "intermediate"),
            ("load-balancing", "Load Balancing", "intermediate"),
            ("cdn", "CDN", "intermediate"),
            ("api-gateways", "API Gateways", "intermediate"),
            ("service-discovery", "Service Discovery", "intermediate"),
        ],
    },
    {
        "id": "networking-m14",
        "title": "Module 14 · Production Networking",
        "goal": "Run networks with HA, monitoring, DR, automation, and clear checklists.",
        "lab": "Complete a production readiness review and an incident response drill.",
        "lessons": [
            ("high-availability", "High Availability", "advanced"),
            ("redundancy", "Redundancy", "advanced"),
            ("network-monitoring", "Network Monitoring", "intermediate"),
            ("capacity-planning", "Capacity Planning", "intermediate"),
            ("disaster-recovery", "Disaster Recovery", "advanced"),
            ("incident-response", "Incident Response", "advanced"),
            ("network-automation", "Network Automation", "intermediate"),
            ("networking-best-practices", "Best Practices", "intermediate"),
            ("production-checklists", "Production Checklists", "intermediate"),
            ("troubleshooting-methodology", "Troubleshooting Methodology", "intermediate"),
        ],
    },
]

CAPSTONES: list[tuple[str, str]] = [
    ("home-lab-network", "Build a Home Lab Network"),
    ("configure-vlans", "Configure VLANs"),
    ("build-dns-server", "Build a DNS Server"),
    ("configure-dhcp-server", "Configure a DHCP Server"),
    ("build-vpn-server", "Build a VPN Server"),
    ("firewall-gateway", "Create a Firewall Gateway"),
    ("cloud-vpc-design", "Cloud VPC Design"),
    ("enterprise-network-troubleshooting-challenge", "Enterprise Network Troubleshooting Challenge"),
]

TODAY = "2026-08-10"


def stub_body(
    title: str,
    module: str,
    goal: str,
    difficulty: str,
    est: str,
    desc: str,
    status: str,
) -> str:
    return textwrap.dedent(
        f"""\
        ---
        title: "{title}"
        description: "{desc}"
        difficulty: {difficulty}
        estimated_time: "{est}"
        technology: networking
        module: "{module}"
        learning_paths:
          - cloud-engineer
          - devops-engineer
          - site-reliability-engineer
          - kubernetes-engineer
        skills:
          - networking-fundamentals
        tags:
          - networking
          - devops
          - cloud
          - rebash-networking-mastery
        author: Shaik Basha
        last_updated: "{TODAY}"
        comments: false
        status: {status}
        ---

        # {title}

        !!! note "Tutorial status"
            This lesson is scaffolded for **REBASH Networking Mastery**. Full tutorial content
            (theory, lab, interview questions) will be published next — structure and SEO are ready.

        ## Overview

        {desc}

        **Module goal:** {goal}

        ## Prerequisites

        - Basic Linux command-line familiarity
        - A disposable lab VM or container host for packet and routing experiments
        - Completion of earlier lessons in this module (unless this is lesson 1)

        ## Learning Objectives

        - [ ] Explain the core idea of **{title}** in a production Cloud/DevOps context
        - [ ] Run the hands-on checks for this lesson in a lab environment
        - [ ] Relate the topic to Linux, Kubernetes, or cloud networking where relevant

        ## Architecture

        _Diagram and mental model — forthcoming._

        ## Theory

        _Production-focused theory — forthcoming._

        ## Hands-on Lab

        _Lab steps — forthcoming._

        ## Validation

        _How you know it worked — forthcoming._

        ## Best Practices

        _Coming soon._

        ## Common Mistakes

        ❌ Skipping fundamentals and jumping straight to cloud or Kubernetes networking.

        ✅ Complete earlier modules so Layer 2–4 behaviour is clear before platform overlays.

        ---

        ## Interview Questions

        _Coming soon._

        ## Summary

        Scaffold ready for the full **{title}** tutorial.

        ## References

        - [Networking course overview](index.md)
        """
    )


def capstone_stub(slug: str, title: str) -> str:
    desc = (
        f"Capstone project: {title} — production-style networking build for Cloud, DevOps, "
        "and platform engineers."
    )
    return textwrap.dedent(
        f"""\
        ---
        title: "{title}"
        description: "{desc}"
        difficulty: advanced
        estimated_time: "4–8 hours"
        technology: networking
        module: "Module 15 · Capstone Projects"
        learning_paths:
          - cloud-engineer
          - devops-engineer
          - site-reliability-engineer
        tags:
          - networking
          - capstone
          - project
          - devops
        author: Shaik Basha
        last_updated: "{TODAY}"
        comments: false
        status: planned
        ---

        # {title}

        !!! note "Capstone status"
            Scaffolded for **REBASH Networking Mastery**. Full project brief, acceptance criteria,
            and validation checklist will be published with the tutorial series.

        ## Overview

        {desc}

        ## Goals

        - [ ] Design and implement the solution in a disposable lab or cloud sandbox
        - [ ] Document topology, addressing, and verification as portfolio evidence
        - [ ] Apply security, monitoring, and troubleshooting habits from Modules 8–14

        ## Deliverables

        _Coming soon._

        ## Acceptance criteria

        _Coming soon._

        ## References

        - [Networking course overview](../index.md)
        """
    )


def ensure_stub(slug: str, title: str, module_title: str, goal: str, difficulty: str) -> tuple[str, str]:
    """Return (filename, status) where status is ready|planned."""
    if slug in REUSE:
        src = NET / REUSE[slug]
        if src.exists():
            return REUSE[slug], "ready"

    path = NET / f"{slug}.md"
    if path.exists() and path.stat().st_size > 2000:
        return path.name, "ready"

    desc = (
        f"Learn {title} for Cloud, DevOps, Kubernetes, and platform engineering — "
        f"part of REBASH Networking Mastery ({module_title})."
    ).replace('"', "'")
    est = (
        "35–55 min"
        if difficulty == "beginner"
        else "45–70 min"
        if difficulty != "advanced"
        else "55–80 min"
    )
    status = "planned"
    path.write_text(
        stub_body(title, module_title, goal, difficulty, est, desc, status),
        encoding="utf-8",
    )
    return path.name, status


def write_pages(lesson_nav: list[tuple[str, list[tuple[str, str]]]]) -> None:
    lines = [
        "title: Networking",
        "icon: material/lan",
        "",
        "nav:",
        "  - Overview: index.md",
        "  - Glossary: glossary.md",
    ]
    for module_title, items in lesson_nav:
        lines.append(f'  - "{module_title}":')
        for filename, title in items:
            lines.append(f"    - {title}: {filename}")
    lines.append('  - "Module 15 · Capstone Projects":')
    for slug, title in CAPSTONES:
        lines.append(f"    - {title}: projects/{slug}.md")
    lines.extend(
        [
            "  - Roadmap: roadmap.md",
            "  - FAQ: faq.md",
            "  - Projects: projects/index.md",
            "  - Quizzes: quizzes/index.md",
            "  - Cheat sheets: cheatsheets/index.md",
            "  - Interview: interview/index.md",
            "  - Certifications: certifications/index.md",
            "  - Capstone hub: capstone/index.md",
        ]
    )
    (NET / ".pages").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(modules_meta: list[dict], counts: dict) -> None:
    rows: list[str] = []
    for m in modules_meta:
        rows.append(f"### {m['title']}\n")
        rows.append(f"**Goal:** {m['goal']}\n")
        if m.get("lab"):
            rows.append(f"**Lab / project focus:** {m['lab']}\n")
        rows.append("")
        rows.append("| # | Lesson | Level | Status |")
        rows.append("|---|--------|-------|--------|")
        for i, (fn, title, diff, st) in enumerate(m["rows"], 1):
            link = f"[{title}]({fn})"
            badge = "Ready" if st == "ready" else "Scaffolded"
            rows.append(f"| {i} | {link} | {diff.title()} | {badge} |")
        rows.append("")

    body = f"""---
title: Overview
description: "REBASH Networking Mastery — practical networking for Linux, Cloud, Kubernetes, DevOps, and enterprise engineers. 15 modules, production labs, and capstone projects."
difficulty: beginner
estimated_time: "8–10 weeks"
author: Shaik Basha
last_updated: "{TODAY}"
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

**Duration:** 8–10 weeks · **Lessons:** ~{counts['lessons']} · **Labs / projects:** 40+ planned · **Capstones:** {counts['capstones']}

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

{chr(10).join(rows)}

## Capstone projects (Module 15)

| Project | Status |
|---------|--------|
"""
    for slug, title in CAPSTONES:
        body += f"| [{title}](projects/{slug}.md) | Scaffolded |\n"

    body += """
## Prerequisites

Basic computer literacy and comfort with a Linux terminal. A disposable Ubuntu LTS lab VM
(and optional AWS/Azure/GCP sandbox) with snapshots.

## Related

- [Linux Mastery](../linux/index.md)
- [DevOps Engineer learning path](../learning-paths/devops-engineer/index.md)
- [Cloud Engineer learning path](../learning-paths/cloud-engineer/index.md)
- [Networking interview prep](interview/index.md)
"""
    (NET / "index.md").write_text(body, encoding="utf-8")


def write_projects_index() -> None:
    lines = [
        "---",
        "title: Projects",
        'description: "Capstone and practice projects for REBASH Networking Mastery."',
        "technology_id: networking",
        "hide:",
        "  - toc",
        "author: Shaik Basha",
        "category: networking",
        "tags:",
        "  - networking",
        "  - capstone",
        "  - rebash-networking-mastery",
        "---",
        "",
        "# Networking Mastery projects",
        "",
        "Capstone projects for **REBASH Networking Mastery** (Module 15).",
        "",
        "| Project | Status |",
        "|---------|--------|",
    ]
    for slug, title in CAPSTONES:
        lines.append(f"| [{title}]({slug}.md) | Scaffolded |")
    lines.extend(
        [
            "",
            "Browse the wider [Academy projects catalog](../../projects/) for cross-course builds.",
            "",
        ]
    )
    (NET / "projects" / "index.md").write_text("\n".join(lines), encoding="utf-8")


def patch_curriculum(module_blocks: list[dict], tutorial_count: int) -> None:
    text = CURRICULUM.read_text(encoding="utf-8")
    pattern = re.compile(
        r"(- id: networking\n  title: Networking\n  status: ready\n  path_prefix: networking/\n  difficulty: )\w+(\n  modules:\n)"
        r"(?:.*?)"
        r"(  tutorial_count: )\d+(\n- id: aws\n)",
        re.DOTALL,
    )
    modules_yaml = ""
    for m in module_blocks:
        modules_yaml += f"  - id: {m['id']}\n    title: {m['title']}\n    tutorials:\n"
        for tid in m["tutorial_ids"]:
            modules_yaml += f"    - {tid}\n"
    repl = rf"\g<1>beginner\g<2>{modules_yaml}\g<3>{tutorial_count}\g<4>"
    new_text, n = pattern.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit(f"curriculum.yaml networking block replace failed (matches={n})")
    CURRICULUM.write_text(new_text, encoding="utf-8")


def main() -> None:
    NET.mkdir(parents=True, exist_ok=True)
    (NET / "projects").mkdir(exist_ok=True)

    lesson_nav: list[tuple[str, list[tuple[str, str]]]] = []
    modules_meta: list[dict] = []
    curriculum_modules: list[dict] = []
    ready = planned = 0

    for mod in MODULES:
        nav_items: list[tuple[str, str]] = []
        rows = []
        tutorial_ids = []
        for slug, title, difficulty in mod["lessons"]:
            filename, status = ensure_stub(
                slug, title, mod["title"], mod["goal"], difficulty
            )
            if status == "ready":
                ready += 1
            else:
                planned += 1
            nav_items.append((filename, title))
            rows.append((filename, title, difficulty, status))
            tutorial_ids.append(f"networking/{Path(filename).stem}")
        lesson_nav.append((mod["title"], nav_items))
        modules_meta.append({**mod, "rows": rows})
        curriculum_modules.append(
            {"id": mod["id"], "title": mod["title"], "tutorial_ids": tutorial_ids}
        )

    for slug, title in CAPSTONES:
        path = NET / "projects" / f"{slug}.md"
        if not path.exists():
            path.write_text(capstone_stub(slug, title), encoding="utf-8")
            planned += 1

    lesson_count = sum(len(m["tutorial_ids"]) for m in curriculum_modules)
    cap_ids = [f"networking/projects/{slug}" for slug, _ in CAPSTONES]
    curriculum_modules.append(
        {
            "id": "networking-m15",
            "title": "Module 15 · Capstone Projects",
            "tutorial_ids": cap_ids,
        }
    )

    write_pages(lesson_nav)
    write_index(
        modules_meta,
        {"lessons": lesson_count, "capstones": len(CAPSTONES)},
    )
    write_projects_index()
    patch_curriculum(curriculum_modules, lesson_count + len(CAPSTONES))

    display = ROOT / "docs" / "_curriculum" / "course-display.yaml"
    dtext = display.read_text(encoding="utf-8")
    dtext = re.sub(
        r"(networking:\n(?:  .*\n)*?  eyebrow: ).*",
        r"\1REBASH Networking Mastery",
        dtext,
        count=1,
    )
    dtext = re.sub(
        r"(networking:\n(?:  .*\n)*?  tagline: ).*",
        r"\1Master practical networking for Linux, Cloud, Kubernetes, DevOps, and enterprise — REBASH Networking Mastery.",
        dtext,
        count=1,
    )
    dtext = re.sub(r"(networking:\n(?:  .*\n)*?  labs: )\d+", r"\g<1>40", dtext, count=1)
    dtext = re.sub(r"(networking:\n(?:  .*\n)*?  projects: )\d+", r"\g<1>8", dtext, count=1)
    dtext = re.sub(r"(networking:\n(?:  .*\n)*?  capstones: )\d+", r"\g<1>8", dtext, count=1)
    display.write_text(dtext, encoding="utf-8")

    print(f"ready_anchor={ready} stubs_or_capstones={planned} lessons={lesson_count}")
    print(f"wrote {NET / '.pages'}")
    print(f"wrote {NET / 'index.md'}")
    print("updated curriculum.yaml networking modules")
    print("updated course-display.yaml networking stats")


if __name__ == "__main__":
    main()
