#!/usr/bin/env python3
"""Generate Excalidraw-style SVG diagrams (hand-drawn look) for REBASH Academy.

Writes:
  docs/assets/excalidraw/<name>.svg
  docs/assets/excalidraw/<name>.excalidraw  (simple scene JSON for later editing)

Usage:
  python3 scripts/generate-excalidraw-svg.py
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "excalidraw"

# Excalidraw-ish palette
STROKE = "#1e1e1e"
COLORS = {
    "blue": ("#a5d8ff", "#1971c2"),
    "green": ("#b2f2bb", "#2f9e44"),
    "orange": ("#ffd8a8", "#e8590c"),
    "purple": ("#d0bfff", "#7048e8"),
    "pink": ("#eebefa", "#9c36b5"),
    "yellow": ("#ffec99", "#e67700"),
    "teal": ("#99e9f2", "#0c8599"),
    "gray": ("#e9ecef", "#495057"),
    "red": ("#ffc9c9", "#e03131"),
}


def _wiggle(rng: random.Random, x1, y1, x2, y2, waves=2):
    """Slightly imperfect line path between two points."""
    pts = [(x1, y1)]
    for i in range(1, waves + 1):
        t = i / (waves + 1)
        x = x1 + (x2 - x1) * t + rng.uniform(-1.2, 1.2)
        y = y1 + (y2 - y1) * t + rng.uniform(-1.2, 1.2)
        pts.append((x, y))
    pts.append((x2, y2))
    d = f"M {pts[0][0]:.1f},{pts[0][1]:.1f}"
    for x, y in pts[1:]:
        d += f" L {x:.1f},{y:.1f}"
    return d


def _rough_rect(rng, x, y, w, h, r=10):
    """Rough rounded-rect path."""
    # four corners with small jitter
    def j():
        return rng.uniform(-1.0, 1.0)

    x1, y1 = x + j(), y + j()
    x2, y2 = x + w + j(), y + j()
    x3, y3 = x + w + j(), y + h + j()
    x4, y4 = x + j(), y + h + j()
    return (
        f"M {x1+r:.1f},{y1:.1f} "
        f"L {x2-r:.1f},{y2:.1f} Q {x2:.1f},{y2:.1f} {x2:.1f},{y2+r:.1f} "
        f"L {x3:.1f},{y3-r:.1f} Q {x3:.1f},{y3:.1f} {x3-r:.1f},{y3:.1f} "
        f"L {x4+r:.1f},{y4:.1f} Q {x4:.1f},{y4:.1f} {x4:.1f},{y4-r:.1f} "
        f"L {x1:.1f},{y1+r:.1f} Q {x1:.1f},{y1:.1f} {x1+r:.1f},{y1:.1f} Z"
    )


def _hachure(rng, x, y, w, h, stroke, gap=6):
    lines = []
    # diagonal hatch inside box
    start = -h
    while start < w:
        x1 = x + max(0, start)
        y1 = y + max(0, -start)
        x2 = x + min(w, start + h)
        y2 = y + min(h, w - start)
        if x2 > x1 and y2 > y1:
            lines.append(
                f'<path d="{_wiggle(rng, x1, y1, x2, y2, 1)}" '
                f'stroke="{stroke}" stroke-width="1" fill="none" opacity="0.45"/>'
            )
        start += gap
    return "\n".join(lines)


def box(rng, x, y, w, h, title, subtitle="", color="blue", hatch=True):
    fill, stroke = COLORS[color]
    path = _rough_rect(rng, x, y, w, h)
    # soft shadow offset
    shadow = _rough_rect(rng, x + 3, y + 3, w, h)
    hatch_svg = _hachure(rng, x + 4, y + 4, w - 8, h - 8, stroke) if hatch else ""
    sub = ""
    if subtitle:
        sub = (
            f'<text x="{x+w/2:.1f}" y="{y+h/2+14:.1f}" text-anchor="middle" '
            f'font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
            f'font-size="12" fill="{STROKE}">{subtitle}</text>'
        )
    title_y = y + h / 2 + (0 if not subtitle else -6)
    return f"""
  <path d="{shadow}" fill="#00000022" stroke="none"/>
  <path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
  {hatch_svg}
  <text x="{x+w/2:.1f}" y="{title_y:.1f}" text-anchor="middle"
        font-family="Virgil, Segoe Print, Comic Sans MS, cursive"
        font-size="14" font-weight="700" fill="{STROKE}">{title}</text>
  {sub}
"""


def label(x, y, text, size=15, weight="700"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
        f'font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="{size}" font-weight="{weight}" fill="{STROKE}">{text}</text>'
    )


def soft_box(rng, x, y, w, h, title, subtitle="", color="blue"):
    """Cleaner card for polished course diagrams (light hatch)."""
    return box(rng, x, y, w, h, title, subtitle, color, hatch=False)


def arrow(rng, x1, y1, x2, y2, color=STROKE):
    path = _wiggle(rng, x1, y1, x2, y2, 2)
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    s = 8
    hx1, hy1 = x2 + s * math.cos(a1), y2 + s * math.sin(a1)
    hx2, hy2 = x2 + s * math.cos(a2), y2 + s * math.sin(a2)
    return f"""
  <path d="{path}" stroke="{color}" stroke-width="2" fill="none"/>
  <path d="M {x2:.1f},{y2:.1f} L {hx1:.1f},{hy1:.1f} M {x2:.1f},{y2:.1f} L {hx2:.1f},{hy2:.1f}"
        stroke="{color}" stroke-width="2" fill="none"/>
"""


def svg_doc(width, height, body, title):
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" role="img" aria-label="{title}">
  <rect width="100%" height="100%" fill="#fffef8"/>
  {body}
</svg>
"""


def write_pair(name: str, width: int, height: int, body: str, elements: list):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.svg").write_text(svg_doc(width, height, body, name), encoding="utf-8")
    scene = {
        "type": "excalidraw",
        "version": 2,
        "source": "rebash-academy-generator",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#fffef8"},
        "files": {},
    }
    (OUT / f"{name}.excalidraw").write_text(json.dumps(scene, indent=2), encoding="utf-8")
    print(f"wrote {name}")


def diagram_network_types():
    rng = random.Random(11)
    parts = []
    elems = []
    items = [
        (40, 40, "LAN", "Building / Campus", "blue"),
        (240, 40, "MAN", "City scale", "teal"),
        (440, 40, "WAN", "Sites / Regions", "orange"),
        (140, 160, "Internet", "Public global", "purple"),
        (340, 160, "VPN", "Encrypted tunnel", "green"),
        (40, 280, "Intranet", "Private org", "pink"),
        (240, 280, "Extranet", "Partner access", "yellow"),
        (440, 280, "Cloud VPC", "Logical LAN", "gray"),
    ]
    for i, (x, y, t, s, c) in enumerate(items):
        parts.append(box(rng, x, y, 150, 70, t, s, c))
        elems.append({"type": "rectangle", "id": f"b{i}", "x": x, "y": y, "width": 150, "height": 70, "label": t})
    # a few connectors
    parts.append(arrow(rng, 190, 75, 240, 75))
    parts.append(arrow(rng, 390, 75, 440, 75))
    parts.append(arrow(rng, 215, 110, 200, 160))
    parts.append(arrow(rng, 515, 110, 420, 160))
    write_pair("network-types", 640, 380, "\n".join(parts), elems)


def diagram_topologies():
    rng = random.Random(22)
    parts = []
    elems = []
    # Star
    parts.append(
        f'<text x="120" y="28" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="16" font-weight="700" fill="{STROKE}">Star</text>'
    )
    cx, cy = 120, 140
    parts.append(box(rng, cx - 35, cy - 20, 70, 40, "Switch", "", "blue"))
    for ang, label in [(210, "H1"), (270, "H2"), (330, "H3")]:
        rad = math.radians(ang)
        x, y = cx + 90 * math.cos(rad) - 25, cy + 90 * math.sin(rad) - 15
        parts.append(box(rng, x, y, 50, 30, label, "", "green"))
        parts.append(arrow(rng, cx, cy, x + 25, y + 15))
    # Bus
    parts.append(
        f'<text x="360" y="28" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="16" font-weight="700" fill="{STROKE}">Bus</text>'
    )
    parts.append(arrow(rng, 260, 140, 460, 140))
    for i, lab in enumerate(["A", "B", "C"]):
        x = 280 + i * 70
        parts.append(box(rng, x, 70, 50, 30, lab, "", "orange"))
        parts.append(arrow(rng, x + 25, 100, x + 25, 140))
    # Mesh hint
    parts.append(
        f'<text x="560" y="28" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="16" font-weight="700" fill="{STROKE}">Mesh</text>'
    )
    nodes = [(520, 80), (600, 80), (520, 160), (600, 160)]
    for i, (x, y) in enumerate(nodes):
        parts.append(box(rng, x, y, 40, 30, f"N{i+1}", "", "purple"))
    for a in range(len(nodes)):
        for b in range(a + 1, len(nodes)):
            parts.append(arrow(rng, nodes[a][0] + 20, nodes[a][1] + 15, nodes[b][0] + 20, nodes[b][1] + 15))
    write_pair("network-topologies", 680, 240, "\n".join(parts), elems)


def diagram_osi():
    rng = random.Random(33)
    parts = []
    elems = []
    layers = [
        ("7 Application", "HTTP DNS SSH", "blue"),
        ("6 Presentation", "TLS JSON", "teal"),
        ("5 Session", "Sessions / RPC", "green"),
        ("4 Transport", "TCP UDP", "orange"),
        ("3 Network", "IP ICMP", "purple"),
        ("2 Data Link", "Ethernet MAC", "pink"),
        ("1 Physical", "Cable / Radio", "yellow"),
    ]
    y = 20
    for i, (title, sub, color) in enumerate(layers):
        parts.append(box(rng, 80, y, 320, 48, title, sub, color))
        if i < len(layers) - 1:
            parts.append(arrow(rng, 240, y + 48, 240, y + 58))
        y += 58
    parts.append(
        f'<text x="520" y="80" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="14" fill="{STROKE}">Encapsulation ↓</text>'
    )
    parts.append(box(rng, 420, 120, 200, 50, "Data", "", "gray"))
    parts.append(arrow(rng, 520, 170, 520, 200))
    parts.append(box(rng, 420, 200, 200, 50, "Segment", "ports", "orange"))
    parts.append(arrow(rng, 520, 250, 520, 280))
    parts.append(box(rng, 420, 280, 200, 50, "Packet", "IP", "purple"))
    parts.append(arrow(rng, 520, 330, 520, 360))
    parts.append(box(rng, 420, 360, 200, 50, "Frame", "MAC", "pink"))
    write_pair("osi-model", 680, 450, "\n".join(parts), elems)


def diagram_client_path():
    rng = random.Random(44)
    parts = []
    elems = []
    chain = [
        (30, 80, "Client", "Browser / App", "blue"),
        (170, 80, "LAN/VPC", "Switch / Subnet", "green"),
        (310, 80, "Router", "Gateway", "orange"),
        (450, 80, "Firewall", "Policy", "red"),
        (590, 80, "Internet", "Public path", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    parts.append(
        f'<text x="360" y="200" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">Every Cloud / DevOps request travels a path like this</text>'
    )
    write_pair("what-is-networking", 740, 230, "\n".join(parts), elems)


def diagram_tcpip():
    rng = random.Random(55)
    parts = []
    layers = [
        ("Application", "HTTP DNS SSH TLS", "blue", "OSI 5–7"),
        ("Transport", "TCP UDP ports", "orange", "OSI 4"),
        ("Internet", "IP ICMP routing", "purple", "OSI 3"),
        ("Link", "Ethernet ARP Wi‑Fi", "green", "OSI 1–2"),
    ]
    y = 30
    for title, sub, color, map_to in layers:
        parts.append(box(rng, 80, y, 300, 55, title, sub, color))
        parts.append(box(rng, 420, y + 8, 160, 40, map_to, "", "gray"))
        y += 70
    parts.append(
        f'<text x="500" y="20" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="14" font-weight="700" fill="{STROKE}">Maps to OSI</text>'
    )
    write_pair("tcp-ip-model", 640, 330, "\n".join(parts), [])


def diagram_ip_addressing():
    rng = random.Random(66)
    parts = []
    parts.append(box(rng, 40, 40, 180, 70, "IPv4", "32-bit · dotted", "blue"))
    parts.append(box(rng, 260, 40, 180, 70, "IPv6", "128-bit · hex", "teal"))
    parts.append(box(rng, 480, 40, 180, 70, "CIDR", "/prefix length", "orange"))
    parts.append(box(rng, 40, 160, 180, 70, "Private", "RFC 1918", "green"))
    parts.append(box(rng, 260, 160, 180, 70, "Public", "Globally routed", "purple"))
    parts.append(box(rng, 480, 160, 180, 70, "Special", "Loopback · link-local", "pink"))
    parts.append(arrow(rng, 220, 75, 260, 75))
    parts.append(arrow(rng, 440, 75, 480, 75))
    write_pair("ip-addressing", 700, 280, "\n".join(parts), [])


def diagram_subnetting():
    rng = random.Random(77)
    parts = []
    parts.append(box(rng, 200, 20, 240, 55, "Parent /24", "256 addresses", "blue"))
    parts.append(arrow(rng, 320, 75, 160, 110))
    parts.append(arrow(rng, 320, 75, 320, 110))
    parts.append(arrow(rng, 320, 75, 480, 110))
    parts.append(box(rng, 60, 120, 160, 55, "/26 App", "64 addrs", "green"))
    parts.append(box(rng, 240, 120, 160, 55, "/27 Data", "32 addrs", "orange"))
    parts.append(box(rng, 420, 120, 160, 55, "/28 Edge", "16 addrs", "purple"))
    parts.append(
        f'<text x="320" y="220" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">VLSM — unequal subnets, no overlap</text>'
    )
    write_pair("subnetting-vlsm", 640, 250, "\n".join(parts), [])


def diagram_k8s_net():
    rng = random.Random(88)
    parts = []
    parts.append(box(rng, 40, 40, 140, 60, "Pod A", "10.244.1.5", "blue"))
    parts.append(box(rng, 220, 40, 140, 60, "Pod B", "10.244.2.8", "green"))
    parts.append(box(rng, 130, 140, 180, 60, "Service", "ClusterIP", "orange"))
    parts.append(box(rng, 400, 140, 180, 60, "Ingress", "L7 HTTP", "purple"))
    parts.append(box(rng, 400, 40, 180, 60, "CoreDNS", "Cluster DNS", "teal"))
    parts.append(arrow(rng, 180, 70, 220, 70))
    parts.append(arrow(rng, 180, 100, 200, 140))
    parts.append(arrow(rng, 290, 100, 220, 140))
    parts.append(arrow(rng, 310, 170, 400, 170))
    parts.append(arrow(rng, 490, 100, 490, 140))
    write_pair("kubernetes-networking", 640, 240, "\n".join(parts), [])


def diagram_switching():
    rng = random.Random(99)
    parts = []
    parts.append(box(rng, 40, 40, 140, 60, "Host A", "MAC 1", "blue"))
    parts.append(box(rng, 250, 40, 160, 70, "Switch", "MAC table", "orange"))
    parts.append(box(rng, 480, 40, 140, 60, "Host B", "MAC 2", "green"))
    parts.append(box(rng, 250, 160, 160, 60, "VLAN 10", "App tier", "purple"))
    parts.append(box(rng, 450, 160, 160, 60, "VLAN 20", "Data tier", "pink"))
    parts.append(arrow(rng, 180, 70, 250, 70))
    parts.append(arrow(rng, 410, 70, 480, 70))
    write_pair("switching-vlans", 660, 260, "\n".join(parts), [])


def diagram_routing():
    rng = random.Random(101)
    parts = []
    parts.append(box(rng, 40, 80, 140, 60, "Subnet A", "10.0.1.0/24", "blue"))
    parts.append(box(rng, 250, 80, 160, 70, "Router", "route table", "orange"))
    parts.append(box(rng, 480, 40, 140, 60, "Subnet B", "10.0.2.0/24", "green"))
    parts.append(box(rng, 480, 140, 140, 60, "Internet", "0.0.0.0/0", "purple"))
    parts.append(arrow(rng, 180, 110, 250, 110))
    parts.append(arrow(rng, 410, 100, 480, 70))
    parts.append(arrow(rng, 410, 120, 480, 160))
    write_pair("routing-fundamentals", 660, 240, "\n".join(parts), [])


def diagram_tcp_handshake():
    rng = random.Random(111)
    parts = []
    parts.append(box(rng, 40, 40, 140, 50, "Client", "", "blue"))
    parts.append(box(rng, 480, 40, 140, 50, "Server", "", "green"))
    parts.append(arrow(rng, 180, 55, 480, 55))
    parts.append(
        f'<text x="330" y="40" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">1 SYN</text>'
    )
    parts.append(arrow(rng, 480, 110, 180, 110))
    parts.append(
        f'<text x="330" y="100" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">2 SYN-ACK</text>'
    )
    parts.append(box(rng, 40, 140, 140, 50, "Client", "ESTABLISHED", "blue"))
    parts.append(box(rng, 480, 140, 140, 50, "Server", "ESTABLISHED", "green"))
    parts.append(arrow(rng, 180, 165, 480, 165))
    parts.append(
        f'<text x="330" y="155" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">3 ACK</text>'
    )
    parts.append(box(rng, 200, 220, 260, 50, "TCP three-way handshake", "ports + sequence state", "orange"))
    write_pair("tcp-handshake", 660, 300, "\n".join(parts), [])


def diagram_tcp_vs_udp():
    rng = random.Random(112)
    parts = []
    parts.append(box(rng, 40, 40, 280, 200, "TCP", "Reliable · ordered · congest. ctrl", "blue"))
    parts.append(box(rng, 360, 40, 280, 200, "UDP", "Datagram · low overhead", "orange"))
    # overlay bullets as small boxes
    parts.append(box(rng, 60, 100, 240, 40, "HTTP · SSH · DB", "", "teal"))
    parts.append(box(rng, 60, 160, 240, 40, "Handshake · TIME_WAIT", "", "purple"))
    parts.append(box(rng, 380, 100, 240, 40, "DNS · NTP · QUIC base", "", "green"))
    parts.append(box(rng, 380, 160, 240, 40, "No connection state", "", "pink"))
    write_pair("tcp-vs-udp", 680, 280, "\n".join(parts), [])


def diagram_dns_resolution():
    rng = random.Random(113)
    parts = []
    chain = [
        (20, 80, "Stub", "Client resolver", "blue"),
        (160, 80, "Recursive", "Resolver cache", "green"),
        (300, 80, "Root", ".", "orange"),
        (440, 80, "TLD", ".com", "purple"),
        (580, 80, "Auth", "example.com", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    parts.append(
        f'<text x="360" y="200" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">Recursive resolver walks the hierarchy for the stub</text>'
    )
    write_pair("dns-resolution", 740, 230, "\n".join(parts), [])


def diagram_dns_records():
    rng = random.Random(114)
    parts = []
    records = [
        (40, 30, "A", "IPv4", "blue"),
        (200, 30, "AAAA", "IPv6", "teal"),
        (360, 30, "CNAME", "Alias", "green"),
        (520, 30, "TXT", "Text / SPF", "orange"),
        (40, 140, "MX", "Mail", "purple"),
        (200, 140, "NS", "Nameserver", "pink"),
        (360, 140, "PTR", "Reverse", "yellow"),
        (520, 140, "SRV", "Service", "gray"),
    ]
    for x, y, t, s, c in records:
        parts.append(box(rng, x, y, 140, 70, t, s, c))
    write_pair("dns-records", 700, 250, "\n".join(parts), [])


def diagram_http_https():
    rng = random.Random(115)
    parts = []
    parts.append(box(rng, 40, 60, 140, 60, "Client", "Browser", "blue"))
    parts.append(box(rng, 250, 60, 160, 60, "TLS", "Certificates", "green"))
    parts.append(box(rng, 480, 60, 160, 60, "HTTP", "Methods · status", "orange"))
    parts.append(box(rng, 250, 180, 160, 60, "Proxy", "Ingress / nginx", "purple"))
    parts.append(arrow(rng, 180, 90, 250, 90))
    parts.append(arrow(rng, 410, 90, 480, 90))
    parts.append(arrow(rng, 330, 120, 330, 180))
    write_pair("http-https", 680, 280, "\n".join(parts), [])


def diagram_nat():
    rng = random.Random(116)
    parts = []
    parts.append(box(rng, 40, 80, 160, 70, "Private host", "10.0.1.20", "blue"))
    parts.append(box(rng, 260, 70, 180, 90, "NAT gateway", "SNAT / DNAT / PAT", "orange"))
    parts.append(box(rng, 500, 40, 160, 70, "Internet", "public IP", "green"))
    parts.append(box(rng, 500, 140, 160, 70, "Published svc", "DNAT :443→:8080", "purple"))
    parts.append(arrow(rng, 200, 115, 260, 115))
    parts.append(arrow(rng, 440, 100, 500, 75))
    parts.append(arrow(rng, 440, 130, 500, 170))
    write_pair("nat-port-forwarding", 700, 250, "\n".join(parts), [])


def diagram_firewalls():
    rng = random.Random(117)
    parts = []
    parts.append(box(rng, 40, 80, 140, 60, "Client", "", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "NACL", "Stateless", "orange"))
    parts.append(box(rng, 230, 140, 160, 60, "Security group", "Stateful", "green"))
    parts.append(box(rng, 440, 80, 180, 70, "Host firewall", "iptables / nft", "purple"))
    parts.append(box(rng, 660, 80, 120, 70, "App", ":8080", "pink"))
    parts.append(arrow(rng, 180, 110, 230, 70))
    parts.append(arrow(rng, 180, 110, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    parts.append(arrow(rng, 620, 115, 660, 115))
    write_pair("firewalls-access-control", 820, 250, "\n".join(parts), [])


def diagram_load_balancing():
    rng = random.Random(118)
    parts = []
    parts.append(box(rng, 40, 100, 120, 60, "Clients", "", "blue"))
    parts.append(box(rng, 220, 80, 180, 100, "Load balancer", "L4 / L7 · health checks", "orange"))
    parts.append(box(rng, 460, 40, 140, 60, "Backend A", "healthy", "green"))
    parts.append(box(rng, 460, 120, 140, 60, "Backend B", "healthy", "teal"))
    parts.append(box(rng, 460, 200, 140, 60, "Backend C", "draining", "purple"))
    parts.append(arrow(rng, 160, 130, 220, 130))
    parts.append(arrow(rng, 400, 110, 460, 70))
    parts.append(arrow(rng, 400, 130, 460, 150))
    parts.append(arrow(rng, 400, 150, 460, 230))
    write_pair("load-balancing", 640, 300, "\n".join(parts), [])


def diagram_reverse_proxy():
    rng = random.Random(119)
    parts = []
    parts.append(box(rng, 40, 80, 120, 60, "Client", "HTTPS", "blue"))
    parts.append(box(rng, 220, 60, 200, 100, "Reverse proxy", "nginx · HAProxy · Ingress", "orange"))
    parts.append(box(rng, 480, 40, 160, 60, "/api", "app pods", "green"))
    parts.append(box(rng, 480, 130, 160, 60, "/static", "assets", "purple"))
    parts.append(arrow(rng, 160, 110, 220, 110))
    parts.append(arrow(rng, 420, 90, 480, 70))
    parts.append(arrow(rng, 420, 120, 480, 160))
    write_pair("reverse-proxy-ingress", 680, 240, "\n".join(parts), [])


def diagram_cloud_vpc():
    rng = random.Random(120)
    parts = []
    parts.append(box(rng, 40, 40, 620, 240, "VPC 10.0.0.0/16", "multi-AZ", "gray"))
    parts.append(box(rng, 70, 80, 160, 70, "Public AZ-a", "LB · NAT", "blue"))
    parts.append(box(rng, 70, 170, 160, 70, "Private AZ-a", "App · DB", "green"))
    parts.append(box(rng, 280, 80, 160, 70, "Public AZ-b", "LB · NAT", "teal"))
    parts.append(box(rng, 280, 170, 160, 70, "Private AZ-b", "App · DB", "purple"))
    parts.append(box(rng, 480, 110, 150, 70, "IGW", "Internet", "orange"))
    parts.append(arrow(rng, 450, 145, 480, 145))
    write_pair("cloud-vpc", 700, 320, "\n".join(parts), [])


def diagram_vpn():
    rng = random.Random(121)
    parts = []
    parts.append(box(rng, 40, 80, 160, 70, "On-prem", "DC / office", "blue"))
    parts.append(box(rng, 260, 80, 180, 70, "IPsec / WireGuard", "Encrypted tunnel", "orange"))
    parts.append(box(rng, 500, 80, 160, 70, "Cloud VPC", "Private CIDR", "green"))
    parts.append(arrow(rng, 200, 115, 260, 115))
    parts.append(arrow(rng, 440, 115, 500, 115))
    write_pair("vpn-tunneling", 700, 220, "\n".join(parts), [])


def diagram_segmentation():
    rng = random.Random(122)
    parts = []
    parts.append(box(rng, 40, 40, 160, 70, "Public edge", "LB / WAF", "orange"))
    parts.append(box(rng, 240, 40, 160, 70, "App tier", "Private", "blue"))
    parts.append(box(rng, 440, 40, 160, 70, "Data tier", "Locked down", "purple"))
    parts.append(box(rng, 240, 150, 160, 70, "Admin / VPN", "Bastion", "green"))
    parts.append(arrow(rng, 200, 75, 240, 75))
    parts.append(arrow(rng, 400, 75, 440, 75))
    parts.append(arrow(rng, 320, 110, 320, 150))
    write_pair("network-segmentation", 640, 260, "\n".join(parts), [])


def diagram_observability():
    rng = random.Random(123)
    parts = []
    parts.append(box(rng, 40, 80, 140, 60, "Traffic", "Flows", "blue"))
    parts.append(box(rng, 230, 80, 160, 60, "Metrics · logs", "Traces", "green"))
    parts.append(box(rng, 440, 80, 180, 60, "Alerts · runbooks", "On-call", "orange"))
    parts.append(arrow(rng, 180, 110, 230, 110))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("network-observability", 660, 200, "\n".join(parts), [])


def diagram_troubleshoot():
    rng = random.Random(124)
    parts = []
    chain = [
        (20, 80, "Symptom", "Timeout?", "pink"),
        (160, 80, "DNS", "Resolve?", "blue"),
        (300, 80, "Route", "Path?", "green"),
        (440, 80, "Filter", "Allow?", "orange"),
        (580, 80, "App/TLS", "Listen?", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("troubleshooting-method", 740, 200, "\n".join(parts), [])


def diagram_packet_analysis():
    rng = random.Random(125)
    parts = []
    parts.append(box(rng, 40, 60, 160, 70, "Capture", "tcpdump", "blue"))
    parts.append(box(rng, 260, 60, 180, 70, "Filter", "BPF / display", "green"))
    parts.append(box(rng, 500, 60, 160, 70, "Analyse", "Wireshark", "orange"))
    parts.append(box(rng, 260, 170, 180, 60, "pcap file", "Evidence", "purple"))
    parts.append(arrow(rng, 200, 95, 260, 95))
    parts.append(arrow(rng, 440, 95, 500, 95))
    parts.append(arrow(rng, 350, 130, 350, 170))
    write_pair("packet-analysis", 700, 270, "\n".join(parts), [])


# --- Python for DevOps ---


def diagram_python_execution():
    rng = random.Random(201)
    parts = []
    chain = [
        (20, 80, "Source", ".py", "blue"),
        (160, 80, "Interpreter", "python3", "green"),
        (300, 80, "Bytecode", ".pyc", "orange"),
        (440, 80, "Runtime", "stdlib + pkgs", "purple"),
        (580, 80, "Side effects", "files · APIs · CLIs", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("python-execution-flow", 740, 200, "\n".join(parts), [])


def diagram_python_venv():
    rng = random.Random(202)
    parts = []
    parts.append(box(rng, 40, 40, 200, 200, "System Python", "OS packages", "gray"))
    parts.append(box(rng, 300, 40, 360, 200, "Project .venv", "isolated site-packages", "blue"))
    parts.append(box(rng, 330, 90, 140, 60, "pip / uv", "pins", "green"))
    parts.append(box(rng, 490, 90, 140, 60, "Your tools", "scripts", "orange"))
    parts.append(arrow(rng, 240, 140, 300, 140))
    write_pair("python-virtual-env", 700, 280, "\n".join(parts), [])


def diagram_python_basics():
    rng = random.Random(203)
    parts = []
    parts.append(box(rng, 40, 60, 140, 70, "Variables", "names → values", "blue"))
    parts.append(box(rng, 220, 60, 140, 70, "Types", "str int bool", "green"))
    parts.append(box(rng, 400, 60, 140, 70, "Operators", "+ == and", "orange"))
    parts.append(box(rng, 220, 170, 140, 70, "I/O", "print input", "purple"))
    parts.append(box(rng, 400, 170, 140, 70, "Convert", "int() str()", "pink"))
    parts.append(arrow(rng, 180, 95, 220, 95))
    parts.append(arrow(rng, 360, 95, 400, 95))
    parts.append(arrow(rng, 290, 130, 290, 170))
    write_pair("python-basics-types", 580, 280, "\n".join(parts), [])


def diagram_python_control_flow():
    rng = random.Random(204)
    parts = []
    parts.append(box(rng, 40, 80, 140, 60, "Condition", "if / match", "blue"))
    parts.append(box(rng, 240, 40, 160, 60, "True branch", "do work", "green"))
    parts.append(box(rng, 240, 140, 160, 60, "Else / loop", "for / while", "orange"))
    parts.append(box(rng, 460, 80, 160, 60, "Next step", "break/cont", "purple"))
    parts.append(arrow(rng, 180, 100, 240, 70))
    parts.append(arrow(rng, 180, 120, 240, 170))
    parts.append(arrow(rng, 400, 110, 460, 110))
    write_pair("python-control-flow", 660, 240, "\n".join(parts), [])


def diagram_python_package_arch():
    rng = random.Random(205)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Your app", "main.py", "blue"))
    parts.append(box(rng, 230, 40, 160, 70, "Package", "mytool/", "green"))
    parts.append(box(rng, 230, 140, 160, 70, "Stdlib", "pathlib json", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "PyPI deps", "pinned", "purple"))
    parts.append(arrow(rng, 180, 110, 230, 75))
    parts.append(arrow(rng, 180, 120, 230, 175))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-package-architecture", 660, 250, "\n".join(parts), [])


def diagram_python_functions():
    rng = random.Random(206)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Caller", "main()", "blue"))
    parts.append(box(rng, 240, 80, 200, 70, "Function", "args → return", "green"))
    parts.append(box(rng, 500, 40, 160, 60, "Locals", "scope", "orange"))
    parts.append(box(rng, 500, 140, 160, 60, "Side effects", "I/O · exit", "purple"))
    parts.append(arrow(rng, 180, 115, 240, 115))
    parts.append(arrow(rng, 440, 100, 500, 70))
    parts.append(arrow(rng, 440, 130, 500, 170))
    write_pair("python-functions-scope", 700, 240, "\n".join(parts), [])


def diagram_python_data_structures():
    rng = random.Random(207)
    parts = []
    parts.append(box(rng, 40, 40, 140, 70, "list", "ordered", "blue"))
    parts.append(box(rng, 200, 40, 140, 70, "tuple", "immutable", "teal"))
    parts.append(box(rng, 360, 40, 140, 70, "dict", "key → value", "green"))
    parts.append(box(rng, 520, 40, 140, 70, "set", "unique", "orange"))
    parts.append(box(rng, 200, 150, 280, 70, "comprehension / generator", "transform · stream", "purple"))
    write_pair("python-data-structures", 700, 260, "\n".join(parts), [])


def diagram_python_file_handling():
    rng = random.Random(208)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "pathlib", "Path", "blue"))
    parts.append(box(rng, 230, 40, 150, 60, "JSON", "APIs", "green"))
    parts.append(box(rng, 230, 120, 150, 60, "YAML", "config", "orange"))
    parts.append(box(rng, 230, 200, 150, 60, "CSV", "reports", "purple"))
    parts.append(box(rng, 440, 80, 180, 70, "Ops tool", "read · write", "pink"))
    parts.append(arrow(rng, 180, 115, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 150))
    parts.append(arrow(rng, 380, 115, 440, 115))
    write_pair("python-file-handling", 660, 300, "\n".join(parts), [])


def diagram_python_errors():
    rng = random.Random(209)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "try", "risky work", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "except", "handle / log", "orange"))
    parts.append(box(rng, 230, 140, 160, 60, "else", "no error", "green"))
    parts.append(box(rng, 440, 80, 180, 70, "finally", "cleanup", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-error-handling", 660, 240, "\n".join(parts), [])


def diagram_python_oop():
    rng = random.Random(210)
    parts = []
    parts.append(box(rng, 40, 80, 160, 70, "Class", "ServiceCheck", "blue"))
    parts.append(box(rng, 260, 40, 160, 60, "Instance", "attrs", "green"))
    parts.append(box(rng, 260, 140, 160, 60, "dataclass", "config model", "orange"))
    parts.append(box(rng, 480, 80, 160, 70, "Subclass", "override", "purple"))
    parts.append(arrow(rng, 200, 100, 260, 70))
    parts.append(arrow(rng, 200, 120, 260, 170))
    parts.append(arrow(rng, 420, 110, 480, 110))
    write_pair("python-oop-dataclasses", 680, 240, "\n".join(parts), [])


def diagram_python_logging():
    rng = random.Random(211)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "App", "logger", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "Levels", "DEBUG→CRITICAL", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "stderr", "ops humans", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "JSON logs", "aggregators", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-logging-debug", 660, 240, "\n".join(parts), [])


def diagram_python_config():
    rng = random.Random(212)
    parts = []
    parts.append(box(rng, 40, 40, 150, 60, "env vars", "12-factor", "blue"))
    parts.append(box(rng, 40, 120, 150, 60, ".env", "local only", "teal"))
    parts.append(box(rng, 240, 40, 150, 60, "YAML/JSON", "config", "green"))
    parts.append(box(rng, 240, 120, 150, 60, "TOML", "tooling", "orange"))
    parts.append(box(rng, 440, 70, 180, 80, "Secret store", "never commit", "red"))
    parts.append(arrow(rng, 190, 70, 240, 70))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-config-secrets", 660, 220, "\n".join(parts), [])


def diagram_python_cli():
    rng = random.Random(213)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Operator", "argv", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "CLI parser", "argparse · Typer", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "stdout", "data", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "stderr", "logs · UX", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-cli-apps", 660, 240, "\n".join(parts), [])


def diagram_python_linux():
    rng = random.Random(214)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Python", "automation", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "subprocess", "CLIs", "green"))
    parts.append(box(rng, 230, 140, 160, 60, "psutil / os", "process · fs", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "Linux host", "systemd · files", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-linux-automation", 660, 240, "\n".join(parts), [])


def diagram_python_rest():
    rng = random.Random(215)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Client", "requests", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "HTTP", "auth · retry", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "API", "JSON", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "Errors", "429 · 5xx", "red"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-rest-api-flow", 660, 240, "\n".join(parts), [])


def diagram_python_cloud():
    rng = random.Random(216)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Python SDK", "boto3 · azure · gcp", "blue"))
    parts.append(box(rng, 230, 40, 150, 60, "AWS", "EC2 S3 IAM", "orange"))
    parts.append(box(rng, 230, 120, 150, 60, "Azure", "RM + auth", "teal"))
    parts.append(box(rng, 230, 200, 150, 60, "GCP", "compute · GCS", "green"))
    parts.append(box(rng, 440, 100, 180, 70, "Inventory", "dry-run OK", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 115, 230, 150))
    parts.append(arrow(rng, 380, 135, 440, 135))
    write_pair("python-cloud-automation", 660, 300, "\n".join(parts), [])


def diagram_python_git():
    rng = random.Random(217)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Python", "GitPython · HTTP", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "Local repo", "git CLI", "green"))
    parts.append(box(rng, 230, 140, 160, 60, "GitHub/GitLab", "REST · PRs", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "Automation", "audit · webhooks", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-git-automation", 660, 240, "\n".join(parts), [])


def diagram_python_docker():
    rng = random.Random(218)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Docker SDK", "python", "blue"))
    parts.append(box(rng, 230, 40, 150, 60, "Images", "build · pull", "green"))
    parts.append(box(rng, 230, 120, 150, 60, "Containers", "run · stop", "orange"))
    parts.append(box(rng, 440, 40, 150, 60, "Networks", "bridge", "purple"))
    parts.append(box(rng, 440, 120, 150, 60, "Volumes", "data", "teal"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 150))
    write_pair("python-docker-sdk-workflow", 640, 220, "\n".join(parts), [])


def diagram_python_k8s():
    rng = random.Random(219)
    parts = []
    parts.append(box(rng, 40, 80, 150, 70, "Python client", "kubernetes", "blue"))
    parts.append(box(rng, 240, 80, 160, 70, "kubeconfig", "or in-cluster", "green"))
    parts.append(box(rng, 450, 40, 160, 60, "API server", "RBAC", "orange"))
    parts.append(box(rng, 450, 140, 160, 60, "Resources", "Pod DeploySvc", "purple"))
    parts.append(arrow(rng, 190, 115, 240, 115))
    parts.append(arrow(rng, 400, 100, 450, 70))
    parts.append(arrow(rng, 400, 130, 450, 170))
    write_pair("python-k8s-client-architecture", 660, 240, "\n".join(parts), [])


def diagram_python_terraform():
    rng = random.Random(220)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Python", "wrapper", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "Terraform CLI", "fmt · validate · plan", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "State", "inspect", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "cdktf", "overview", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-terraform-automation", 660, 240, "\n".join(parts), [])


def diagram_python_ssh():
    rng = random.Random(221)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Operator", "Paramiko/Fabric", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "SSH", "keys · auth", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "Remote exec", "commands", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "SCP/SFTP", "files", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-ssh-paramiko", 660, 240, "\n".join(parts), [])


def diagram_python_concurrency():
    rng = random.Random(222)
    parts = []
    parts.append(box(rng, 40, 40, 160, 70, "Threads", "I/O wait", "blue"))
    parts.append(box(rng, 220, 40, 160, 70, "Processes", "CPU work", "green"))
    parts.append(box(rng, 400, 40, 160, 70, "asyncio", "many sockets", "orange"))
    parts.append(box(rng, 220, 150, 160, 70, "Futures", "pools · queues", "purple"))
    write_pair("python-concurrency", 600, 260, "\n".join(parts), [])


def diagram_python_pytest():
    rng = random.Random(223)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Tests", "pytest", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "Fixtures", "setup", "green"))
    parts.append(box(rng, 230, 140, 160, 60, "Mocks", "fakes", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "CI", "coverage", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-pytest-testing", 660, 240, "\n".join(parts), [])


def diagram_python_packaging():
    rng = random.Random(224)
    parts = []
    parts.append(box(rng, 40, 80, 160, 70, "pyproject.toml", "metadata", "blue"))
    parts.append(box(rng, 250, 80, 160, 70, "Build", "wheel/sdist", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "Version", "semver", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "Publish", "index", "purple"))
    parts.append(arrow(rng, 200, 115, 250, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-packaging-wheels", 660, 240, "\n".join(parts), [])


def diagram_python_production():
    rng = random.Random(225)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Tool", "CLI / job", "blue"))
    parts.append(box(rng, 230, 40, 160, 60, "Retry/backoff", "resilience", "green"))
    parts.append(box(rng, 230, 140, 160, 60, "Metrics/logs", "health", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "Observability", "pages · SLO", "purple"))
    parts.append(arrow(rng, 180, 100, 230, 70))
    parts.append(arrow(rng, 180, 120, 230, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-automation-pipeline", 660, 240, "\n".join(parts), [])


def diagram_python_security():
    rng = random.Random(226)
    parts = []
    parts.append(box(rng, 40, 40, 160, 70, "Secrets", "vault / env", "red"))
    parts.append(box(rng, 220, 40, 160, 70, "Validate", "inputs", "orange"))
    parts.append(box(rng, 400, 40, 160, 70, "Crypto", "hash · TLS", "green"))
    parts.append(box(rng, 220, 150, 160, 70, "Supply chain", "scan pins", "purple"))
    parts.append(box(rng, 400, 150, 160, 70, "Secure coding", "least priv", "blue"))
    write_pair("python-security-devops", 600, 260, "\n".join(parts), [])


def diagram_python_ai():
    rng = random.Random(227)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Ops ask", "prompt", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "LLM / MCP", "tools", "green"))
    parts.append(box(rng, 460, 40, 160, 60, "Guardrails", "human approve", "orange"))
    parts.append(box(rng, 460, 140, 160, 60, "Automation", "runbooks", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 100, 460, 70))
    parts.append(arrow(rng, 410, 130, 460, 170))
    write_pair("python-ai-devops", 660, 240, "\n".join(parts), [])


def diagram_python_troubleshoot():
    rng = random.Random(228)
    parts = []
    chain = [
        (20, 80, "Symptom", "fail/hang", "pink"),
        (160, 80, "Env", "venv · pins", "blue"),
        (300, 80, "Deps/API", "import · HTTP", "green"),
        (440, 80, "Perf", "CPU · mem", "orange"),
        (580, 80, "Fix", "test · ship", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("python-troubleshooting", 740, 200, "\n".join(parts), [])


def diagram_python_plugin():
    rng = random.Random(229)
    parts = []
    parts.append(box(rng, 40, 80, 150, 70, "Core CLI", "entry", "blue"))
    parts.append(box(rng, 240, 40, 150, 60, "Plugin A", "inventory", "green"))
    parts.append(box(rng, 240, 140, 150, 60, "Plugin B", "notify", "orange"))
    parts.append(box(rng, 440, 80, 180, 70, "Shared", "config · log", "purple"))
    parts.append(arrow(rng, 190, 100, 240, 70))
    parts.append(arrow(rng, 190, 120, 240, 170))
    parts.append(arrow(rng, 390, 110, 440, 110))
    write_pair("python-plugin-architecture", 660, 240, "\n".join(parts), [])


# --- Git & GitHub for Cloud & DevOps ---


def diagram_git_object_model():
    rng = random.Random(301)
    parts = []
    parts.append(box(rng, 40, 40, 140, 60, "blob", "file bytes", "blue"))
    parts.append(box(rng, 220, 40, 140, 60, "tree", "directory", "green"))
    parts.append(box(rng, 400, 40, 140, 60, "commit", "snapshot+meta", "orange"))
    parts.append(box(rng, 580, 40, 140, 60, "tag", "named tip", "purple"))
    parts.append(box(rng, 220, 140, 320, 60, ".git/objects", "content-addressed store", "gray"))
    parts.append(arrow(rng, 180, 70, 220, 70))
    parts.append(arrow(rng, 360, 70, 400, 70))
    parts.append(arrow(rng, 470, 100, 470, 140))
    write_pair("git-object-model", 760, 240, "\n".join(parts), [])


def diagram_git_workflow():
    rng = random.Random(302)
    parts = []
    chain = [
        (20, 80, "Working", "edit files", "blue"),
        (160, 80, "Staging", "git add", "green"),
        (300, 80, "Local repo", "commit", "orange"),
        (440, 80, "Remote", "push/pull", "purple"),
        (580, 80, "CI/GitOps", "pipelines", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("git-workflow", 740, 200, "\n".join(parts), [])


def diagram_git_branching():
    rng = random.Random(303)
    parts = []
    parts.append(box(rng, 40, 100, 140, 60, "main", "protected", "blue"))
    parts.append(box(rng, 240, 40, 160, 60, "feature/*", "work", "green"))
    parts.append(box(rng, 240, 160, 160, 60, "hotfix/*", "urgent", "orange"))
    parts.append(box(rng, 460, 100, 160, 60, "PR / merge", "review", "purple"))
    parts.append(arrow(rng, 180, 120, 240, 70))
    parts.append(arrow(rng, 180, 140, 240, 190))
    parts.append(arrow(rng, 400, 70, 460, 120))
    parts.append(arrow(rng, 400, 190, 460, 140))
    write_pair("git-branching-strategy", 660, 260, "\n".join(parts), [])


def diagram_git_merge():
    rng = random.Random(304)
    parts = []
    parts.append(box(rng, 40, 40, 160, 60, "main", "C1—C2", "blue"))
    parts.append(box(rng, 40, 140, 160, 60, "feature", "C1—C3", "green"))
    parts.append(box(rng, 280, 90, 180, 70, "merge / rebase", "integrate", "orange"))
    parts.append(box(rng, 520, 90, 160, 70, "Result", "history", "purple"))
    parts.append(arrow(rng, 200, 70, 280, 110))
    parts.append(arrow(rng, 200, 170, 280, 130))
    parts.append(arrow(rng, 460, 125, 520, 125))
    write_pair("git-merge-process", 720, 240, "\n".join(parts), [])


def diagram_git_pr_lifecycle():
    rng = random.Random(305)
    parts = []
    chain = [
        (20, 80, "Branch", "push", "blue"),
        (160, 80, "PR open", "checks", "green"),
        (300, 80, "Review", "CODEOWNERS", "orange"),
        (440, 80, "Approve", "protect", "purple"),
        (580, 80, "Merge", "main", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("git-pr-lifecycle", 740, 200, "\n".join(parts), [])


def diagram_git_actions():
    rng = random.Random(306)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Event", "push/PR", "blue"))
    parts.append(box(rng, 230, 80, 160, 70, "Workflow", "jobs · steps", "green"))
    parts.append(box(rng, 440, 40, 160, 60, "Runner", "ubuntu", "orange"))
    parts.append(box(rng, 440, 140, 160, 60, "Secrets", "OIDC", "purple"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 390, 100, 440, 70))
    parts.append(arrow(rng, 390, 130, 440, 170))
    write_pair("git-github-actions", 640, 240, "\n".join(parts), [])


def diagram_git_gitops():
    rng = random.Random(307)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Git repo", "desired state", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "Reconciler", "Argo CD / Flux", "green"))
    parts.append(box(rng, 460, 80, 180, 70, "Cluster", "actual state", "orange"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 115, 460, 115))
    parts.append(
        f'<text x="340" y="200" text-anchor="middle" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">Pull-based sync · Git is source of truth</text>'
    )
    write_pair("git-gitops-flow", 680, 230, "\n".join(parts), [])


def diagram_git_repo_arch():
    rng = random.Random(308)
    parts = []
    parts.append(box(rng, 40, 40, 200, 80, "App repos", "services", "blue"))
    parts.append(box(rng, 280, 40, 200, 80, "Infra repos", "Terraform · K8s", "green"))
    parts.append(box(rng, 160, 160, 200, 70, "Platform / templates", "standards", "orange"))
    parts.append(arrow(rng, 240, 80, 280, 80))
    parts.append(arrow(rng, 260, 120, 260, 160))
    write_pair("git-repository-architecture", 520, 270, "\n".join(parts), [])


# --- Docker for Cloud & DevOps ---


def diagram_docker_architecture():
    rng = random.Random(401)
    parts = []
    parts.append(box(rng, 40, 40, 160, 70, "Docker CLI", "docker", "blue"))
    parts.append(box(rng, 260, 40, 180, 70, "dockerd", "API · engine", "green"))
    parts.append(box(rng, 500, 40, 160, 70, "containerd", "runtime", "orange"))
    parts.append(box(rng, 260, 150, 180, 70, "runc / OCI", "namespaces", "purple"))
    parts.append(box(rng, 500, 150, 160, 70, "Host kernel", "cgroups", "gray"))
    parts.append(arrow(rng, 200, 75, 260, 75))
    parts.append(arrow(rng, 440, 75, 500, 75))
    parts.append(arrow(rng, 350, 110, 350, 150))
    parts.append(arrow(rng, 440, 185, 500, 185))
    write_pair("docker-architecture", 700, 260, "\n".join(parts), [])


def diagram_docker_lifecycle():
    rng = random.Random(402)
    parts = []
    chain = [
        (20, 80, "create", "docker create", "blue"),
        (150, 80, "start", "running", "green"),
        (280, 80, "pause", "optional", "yellow"),
        (410, 80, "stop", "SIGTERM", "orange"),
        (540, 80, "remove", "docker rm", "red"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 110, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 35, chain[i + 1][0], y + 35))
    write_pair("docker-container-lifecycle", 690, 200, "\n".join(parts), [])


def diagram_docker_layers():
    rng = random.Random(403)
    parts = []
    parts.append(box(rng, 80, 40, 400, 40, "App layer", "COPY · CMD", "pink"))
    parts.append(box(rng, 80, 90, 400, 40, "Deps layer", "RUN pip/npm", "orange"))
    parts.append(box(rng, 80, 140, 400, 40, "Base OS layer", "FROM alpine", "green"))
    parts.append(box(rng, 80, 190, 400, 40, "Shared cache", "content-addressed", "blue"))
    parts.append(
        f'<text x="480" y="120" font-family="Virgil, Segoe Print, Comic Sans MS, cursive" '
        f'font-size="13" fill="{STROKE}">Image = stacked layers</text>'
    )
    write_pair("docker-image-layers", 700, 270, "\n".join(parts), [])


def diagram_docker_networking():
    rng = random.Random(404)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Host", ":8080", "gray"))
    parts.append(box(rng, 240, 40, 160, 60, "bridge", "default", "blue"))
    parts.append(box(rng, 240, 130, 160, 60, "Container", ":80", "green"))
    parts.append(box(rng, 460, 80, 160, 70, "DNS", "service name", "orange"))
    parts.append(arrow(rng, 180, 115, 240, 70))
    parts.append(arrow(rng, 180, 115, 240, 160))
    parts.append(arrow(rng, 400, 160, 460, 115))
    write_pair("docker-networking", 660, 240, "\n".join(parts), [])


def diagram_docker_volumes():
    rng = random.Random(405)
    parts = []
    parts.append(box(rng, 40, 80, 160, 70, "Container", "/data", "blue"))
    parts.append(box(rng, 260, 40, 160, 60, "Volume", "named", "green"))
    parts.append(box(rng, 260, 140, 160, 60, "Bind mount", "host path", "orange"))
    parts.append(box(rng, 480, 80, 160, 70, "tmpfs", "memory", "purple"))
    parts.append(arrow(rng, 200, 100, 260, 70))
    parts.append(arrow(rng, 200, 130, 260, 170))
    parts.append(arrow(rng, 420, 100, 480, 115))
    write_pair("docker-volume-architecture", 680, 240, "\n".join(parts), [])


def diagram_docker_compose():
    rng = random.Random(406)
    parts = []
    parts.append(box(rng, 200, 20, 200, 50, "compose.yaml", "services", "gray"))
    parts.append(box(rng, 40, 110, 140, 70, "web", "app", "blue"))
    parts.append(box(rng, 220, 110, 140, 70, "db", "volume", "green"))
    parts.append(box(rng, 400, 110, 140, 70, "cache", "network", "orange"))
    parts.append(arrow(rng, 250, 70, 110, 110))
    parts.append(arrow(rng, 300, 70, 290, 110))
    parts.append(arrow(rng, 350, 70, 470, 110))
    write_pair("docker-compose", 580, 220, "\n".join(parts), [])


def diagram_docker_registry():
    rng = random.Random(407)
    parts = []
    chain = [
        (20, 80, "Build", "docker build", "blue"),
        (160, 80, "Tag", "registry/app:tag", "green"),
        (300, 80, "Push", "docker push", "orange"),
        (440, 80, "Registry", "GHCR · ECR", "purple"),
        (580, 80, "Pull", "deploy", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    write_pair("docker-registry-workflow", 740, 200, "\n".join(parts), [])


def diagram_docker_cicd():
    rng = random.Random(408)
    parts = []
    chain = [
        (20, 80, "Commit", "PR", "blue"),
        (150, 80, "CI build", "buildx", "green"),
        (280, 80, "Scan", "Trivy", "orange"),
        (410, 80, "Push", "registry", "purple"),
        (540, 80, "Promote", "env tags", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 110, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 35, chain[i + 1][0], y + 35))
    write_pair("docker-cicd-pipeline", 690, 200, "\n".join(parts), [])


def diagram_docker_production():
    rng = random.Random(409)
    parts = []
    parts.append(box(rng, 40, 40, 180, 70, "Hardened image", "non-root · scan", "blue"))
    parts.append(box(rng, 260, 40, 180, 70, "Compose / K8s", "limits · probes", "green"))
    parts.append(box(rng, 480, 40, 180, 70, "Registry", "immutable tags", "orange"))
    parts.append(box(rng, 150, 150, 200, 70, "Observability", "logs · metrics", "purple"))
    parts.append(box(rng, 390, 150, 200, 70, "DR / backup", "volumes · IaC", "pink"))
    parts.append(arrow(rng, 220, 75, 260, 75))
    parts.append(arrow(rng, 440, 75, 480, 75))
    parts.append(arrow(rng, 350, 110, 250, 150))
    parts.append(arrow(rng, 370, 110, 490, 150))
    write_pair("docker-production-platform", 700, 260, "\n".join(parts), [])


# --- Kubernetes for Cloud & DevOps ---


def diagram_k8s_architecture():
    rng = random.Random(501)
    parts = []
    parts.append(box(rng, 40, 40, 200, 80, "Control plane", "API · sched · etcd", "blue"))
    parts.append(box(rng, 300, 40, 160, 70, "Worker", "kubelet", "green"))
    parts.append(box(rng, 500, 40, 160, 70, "Worker", "kube-proxy", "green"))
    parts.append(box(rng, 300, 150, 360, 60, "Pods / workloads", "containers", "orange"))
    parts.append(arrow(rng, 240, 80, 300, 75))
    parts.append(arrow(rng, 240, 80, 500, 75))
    parts.append(arrow(rng, 380, 110, 380, 150))
    write_pair("k8s-architecture", 700, 250, "\n".join(parts), [])


def diagram_k8s_control_plane():
    rng = random.Random(502)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "kubectl", "client", "gray"))
    parts.append(box(rng, 220, 80, 150, 70, "API server", "kube-apiserver", "blue"))
    parts.append(box(rng, 420, 20, 140, 55, "etcd", "state", "purple"))
    parts.append(box(rng, 420, 95, 140, 55, "scheduler", "place pods", "green"))
    parts.append(box(rng, 420, 170, 140, 55, "controller", "reconcile", "orange"))
    parts.append(arrow(rng, 180, 115, 220, 115))
    parts.append(arrow(rng, 370, 100, 420, 50))
    parts.append(arrow(rng, 370, 115, 420, 120))
    parts.append(arrow(rng, 370, 130, 420, 195))
    write_pair("k8s-control-plane", 600, 260, "\n".join(parts), [])


def diagram_k8s_pod_lifecycle():
    rng = random.Random(503)
    parts = []
    chain = [
        (20, 80, "Pending", "scheduled?", "yellow"),
        (150, 80, "ContainerCreating", "pull/mount", "blue"),
        (310, 80, "Running", "ready", "green"),
        (440, 80, "Succeeded", "Job", "purple"),
        (570, 80, "Failed", "CrashLoop", "red"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < 3:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    parts.append(arrow(rng, 370, 150, 630, 150))
    write_pair("k8s-pod-lifecycle", 720, 200, "\n".join(parts), [])


def diagram_k8s_service_networking():
    rng = random.Random(504)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Service", "ClusterIP", "blue"))
    parts.append(box(rng, 240, 40, 140, 55, "Pod A", "endpoint", "green"))
    parts.append(box(rng, 240, 120, 140, 55, "Pod B", "endpoint", "green"))
    parts.append(box(rng, 440, 80, 160, 70, "kube-proxy", "iptables/IPVS", "orange"))
    parts.append(arrow(rng, 180, 115, 240, 70))
    parts.append(arrow(rng, 180, 115, 240, 145))
    parts.append(arrow(rng, 380, 115, 440, 115))
    write_pair("k8s-service-networking", 640, 220, "\n".join(parts), [])


def diagram_k8s_ingress_flow():
    rng = random.Random(505)
    parts = []
    chain = [
        (20, 80, "Client", "HTTPS", "gray"),
        (150, 80, "LB / Ingress", "controller", "blue"),
        (310, 80, "Service", "ClusterIP", "green"),
        (450, 80, "Pods", "app", "orange"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(box(rng, x, y, 120, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 35, chain[i + 1][0], y + 35))
    parts.append(box(rng, 310, 180, 140, 50, "TLS secret", "cert", "purple"))
    parts.append(arrow(rng, 210, 150, 380, 180))
    write_pair("k8s-ingress-flow", 620, 260, "\n".join(parts), [])


def diagram_k8s_storage():
    rng = random.Random(506)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Pod", "mount", "blue"))
    parts.append(box(rng, 220, 80, 140, 70, "PVC", "claim", "green"))
    parts.append(box(rng, 400, 80, 140, 70, "PV", "volume", "orange"))
    parts.append(box(rng, 580, 80, 140, 70, "CSI / disk", "cloud", "purple"))
    parts.append(box(rng, 220, 180, 200, 55, "StorageClass", "provisioner", "gray"))
    for x1, x2 in [(180, 220), (360, 400), (540, 580)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    parts.append(arrow(rng, 320, 150, 320, 180))
    write_pair("k8s-storage-architecture", 760, 270, "\n".join(parts), [])


def diagram_k8s_rbac():
    rng = random.Random(507)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Subject", "User / SA", "blue"))
    parts.append(box(rng, 230, 80, 160, 70, "Role / ClusterRole", "verbs · resources", "green"))
    parts.append(box(rng, 440, 80, 180, 70, "RoleBinding", "namespace scope", "orange"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 390, 115, 440, 115))
    write_pair("k8s-rbac-model", 660, 200, "\n".join(parts), [])


def diagram_k8s_helm():
    rng = random.Random(508)
    parts = []
    parts.append(soft_box(rng, 40, 80, 140, 70, "Chart", "templates", "blue"))
    parts.append(soft_box(rng, 220, 80, 140, 70, "values.yaml", "config", "green"))
    parts.append(soft_box(rng, 400, 80, 160, 70, "helm install", "release", "orange"))
    parts.append(soft_box(rng, 600, 80, 140, 70, "Cluster", "objects", "purple"))
    parts.append(arrow(rng, 180, 115, 220, 115))
    parts.append(arrow(rng, 360, 115, 400, 115))
    parts.append(arrow(rng, 560, 115, 600, 115))
    write_pair("k8s-helm-architecture", 780, 200, "\n".join(parts), [])


# --- Helm for Kubernetes Engineers (polished layouts) ---


def diagram_helm_architecture():
    rng = random.Random(601)
    parts = [label(440, 28, "Helm architecture", 18)]
    parts.append(soft_box(rng, 40, 55, 150, 75, "Helm CLI", "client", "blue"))
    parts.append(soft_box(rng, 250, 55, 160, 75, "Chart / repo", "HTTP · OCI", "green"))
    parts.append(soft_box(rng, 470, 55, 160, 75, "Release", "revision history", "orange"))
    parts.append(soft_box(rng, 690, 55, 150, 75, "Kubernetes", "API objects", "purple"))
    parts.append(arrow(rng, 190, 92, 250, 92))
    parts.append(arrow(rng, 410, 92, 470, 92))
    parts.append(arrow(rng, 630, 92, 690, 92))
    parts.append(soft_box(rng, 250, 170, 300, 70, "Templates + values", "rendered manifests", "teal"))
    parts.append(arrow(rng, 330, 130, 360, 170))
    parts.append(arrow(rng, 480, 170, 540, 130))
    parts.append(label(440, 270, "Package → configure → release → cluster", 13, "400"))
    write_pair("helm-architecture", 880, 300, "\n".join(parts), [])


def diagram_helm_chart_structure():
    rng = random.Random(602)
    parts = [label(370, 28, "Chart structure", 18)]
    parts.append(soft_box(rng, 240, 50, 240, 55, "mychart/", "chart root", "gray"))
    parts.append(soft_box(rng, 40, 140, 150, 60, "Chart.yaml", "metadata", "blue"))
    parts.append(soft_box(rng, 210, 140, 150, 60, "values.yaml", "defaults", "green"))
    parts.append(soft_box(rng, 380, 140, 150, 60, "templates/", "manifests", "orange"))
    parts.append(soft_box(rng, 550, 140, 150, 60, "charts/", "deps", "purple"))
    parts.append(arrow(rng, 300, 105, 115, 140))
    parts.append(arrow(rng, 340, 105, 285, 140))
    parts.append(arrow(rng, 380, 105, 455, 140))
    parts.append(arrow(rng, 420, 105, 625, 140))
    parts.append(soft_box(rng, 300, 230, 220, 55, "_helpers.tpl", "named templates", "pink"))
    parts.append(arrow(rng, 455, 200, 410, 230))
    write_pair("helm-chart-structure", 740, 320, "\n".join(parts), [])


def diagram_helm_template_rendering():
    rng = random.Random(603)
    parts = [label(400, 28, "Template rendering", 18)]
    parts.append(soft_box(rng, 30, 70, 150, 80, "templates/", "*.yaml", "blue"))
    parts.append(soft_box(rng, 220, 70, 150, 80, "values", ".Values", "green"))
    parts.append(soft_box(rng, 410, 70, 160, 80, "Helm engine", "Go templates", "orange"))
    parts.append(soft_box(rng, 610, 70, 160, 80, "Manifests", "K8s YAML", "purple"))
    parts.append(arrow(rng, 180, 110, 220, 110))
    parts.append(arrow(rng, 370, 110, 410, 110))
    parts.append(arrow(rng, 570, 110, 610, 110))
    parts.append(label(390, 190, "helm template / install / upgrade", 13, "400"))
    parts.append(soft_box(rng, 220, 210, 340, 60, "Release object", "name · namespace · revision", "teal"))
    write_pair("helm-template-rendering", 800, 300, "\n".join(parts), [])


def diagram_helm_release_lifecycle():
    rng = random.Random(604)
    parts = [label(400, 28, "Release lifecycle", 18)]
    chain = [
        (30, 80, "install", "rev 1", "blue"),
        (180, 80, "upgrade", "rev 2…n", "green"),
        (330, 80, "history", "revisions", "orange"),
        (480, 80, "rollback", "prior rev", "purple"),
        (630, 80, "uninstall", "cleanup", "red"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    parts.append(label(400, 195, "Prefer --atomic on risky upgrades · always check helm history", 13, "400"))
    write_pair("helm-release-lifecycle", 800, 230, "\n".join(parts), [])


def diagram_helm_values_override():
    rng = random.Random(605)
    parts = [label(420, 28, "Values override order", 18)]
    parts.append(soft_box(rng, 40, 60, 160, 70, "chart defaults", "values.yaml", "gray"))
    parts.append(soft_box(rng, 240, 60, 160, 70, "-f values-prod", "file overrides", "blue"))
    parts.append(soft_box(rng, 440, 60, 160, 70, "--set / --set-file", "CLI overrides", "green"))
    parts.append(soft_box(rng, 640, 60, 160, 70, "Effective", "merged values", "orange"))
    parts.append(arrow(rng, 200, 95, 240, 95))
    parts.append(arrow(rng, 400, 95, 440, 95))
    parts.append(arrow(rng, 600, 95, 640, 95))
    parts.append(label(420, 170, "Later sources win · keep secrets out of committed values", 13, "400"))
    parts.append(soft_box(rng, 240, 195, 340, 65, "Environment files", "values-dev.yaml · values-prod.yaml", "purple"))
    write_pair("helm-values-override", 840, 290, "\n".join(parts), [])


def diagram_helm_dependencies():
    rng = random.Random(606)
    parts = [label(430, 28, "Chart dependencies", 18)]
    parts.append(soft_box(rng, 280, 55, 220, 65, "Parent chart", "Chart.yaml deps", "blue"))
    parts.append(soft_box(rng, 40, 170, 170, 70, "Subchart A", "version constraint", "green"))
    parts.append(soft_box(rng, 250, 170, 170, 70, "Subchart B", "OCI / HTTP repo", "orange"))
    parts.append(soft_box(rng, 460, 170, 170, 70, "Library chart", "helpers only", "purple"))
    parts.append(soft_box(rng, 670, 170, 150, 70, "charts/", "vendored", "gray"))
    parts.append(arrow(rng, 340, 120, 125, 170))
    parts.append(arrow(rng, 380, 120, 335, 170))
    parts.append(arrow(rng, 420, 120, 545, 170))
    parts.append(arrow(rng, 480, 120, 720, 170))
    parts.append(label(430, 270, "helm dependency update · pin versions in production", 13, "400"))
    write_pair("helm-dependencies", 860, 300, "\n".join(parts), [])


def diagram_helm_oci_registry():
    rng = random.Random(607)
    parts = [label(400, 28, "OCI chart registry workflow", 18)]
    chain = [
        (30, 80, "Package", "helm package", "blue"),
        (180, 80, "Login", "helm registry", "green"),
        (330, 80, "Push", "oci://…", "orange"),
        (480, 80, "Registry", "GHCR · ECR", "purple"),
        (630, 80, "Pull / install", "version tag", "pink"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    parts.append(label(400, 195, "Prefer OCI + immutable chart versions over floating latest", 13, "400"))
    write_pair("helm-oci-registry", 800, 230, "\n".join(parts), [])


def diagram_helm_gitops():
    rng = random.Random(608)
    parts = [label(370, 28, "Helm + GitOps", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 80, "Git repo", "chart · values", "blue"))
    parts.append(soft_box(rng, 260, 70, 200, 80, "Argo CD / Flux", "Helm release", "green"))
    parts.append(soft_box(rng, 520, 70, 180, 80, "Cluster", "desired state", "orange"))
    parts.append(arrow(rng, 200, 110, 260, 110))
    parts.append(arrow(rng, 460, 110, 520, 110))
    parts.append(soft_box(rng, 160, 190, 400, 65, "CI builds images · GitOps upgrades chart values", "separate concerns", "purple"))
    parts.append(label(360, 285, "Rollback = git revert + sync (or helm rollback for break-glass)", 13, "400"))
    write_pair("helm-gitops-workflow", 740, 310, "\n".join(parts), [])


def diagram_k8s_gitops():
    rng = random.Random(509)
    parts = []
    parts.append(box(rng, 40, 80, 140, 70, "Git", "desired", "blue"))
    parts.append(box(rng, 230, 80, 180, 70, "Argo CD / Flux", "reconcile", "green"))
    parts.append(box(rng, 460, 80, 180, 70, "Cluster", "actual", "orange"))
    parts.append(arrow(rng, 180, 115, 230, 115))
    parts.append(arrow(rng, 410, 115, 460, 115))
    write_pair("k8s-gitops-workflow", 680, 200, "\n".join(parts), [])


def diagram_k8s_production():
    rng = random.Random(510)
    parts = []
    parts.append(box(rng, 40, 40, 180, 70, "HA control plane", "multi-AZ etcd", "blue"))
    parts.append(box(rng, 260, 40, 180, 70, "Workers", "ASG / node pools", "green"))
    parts.append(box(rng, 480, 40, 180, 70, "Ingress + TLS", "policy", "orange"))
    parts.append(box(rng, 100, 150, 200, 70, "Observability", "metrics · logs", "purple"))
    parts.append(box(rng, 360, 150, 220, 70, "GitOps + backup", "DR", "pink"))
    parts.append(arrow(rng, 220, 75, 260, 75))
    parts.append(arrow(rng, 440, 75, 480, 75))
    write_pair("k8s-production-cluster", 700, 260, "\n".join(parts), [])


# --- Linux for Cloud & DevOps (polished Excalidraw) ---


def diagram_linux_architecture():
    rng = random.Random(701)
    parts = [label(430, 28, "Linux architecture", 18)]
    parts.append(soft_box(rng, 40, 60, 160, 70, "User space", "apps · shells", "blue"))
    parts.append(soft_box(rng, 240, 60, 180, 70, "System libraries", "glibc · systemd", "green"))
    parts.append(soft_box(rng, 460, 60, 160, 70, "Kernel", "syscalls", "orange"))
    parts.append(soft_box(rng, 660, 60, 160, 70, "Hardware", "CPU · disk · NIC", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 95, x2, 95))
    parts.append(label(430, 170, "Distributions package kernel + userspace for ops roles", 13, "400"))
    parts.append(soft_box(rng, 200, 195, 440, 60, "Cloud / VM / bare metal", "same mental model", "teal"))
    write_pair("linux-architecture", 860, 290, "\n".join(parts), [])


def diagram_linux_boot_process():
    rng = random.Random(702)
    parts = [label(370, 28, "Boot process", 18)]
    chain = [
        (20, 80, "Firmware", "UEFI/BIOS", "gray"),
        (160, 80, "Bootloader", "GRUB", "blue"),
        (300, 80, "Kernel", "initramfs", "green"),
        (440, 80, "systemd", "PID 1", "orange"),
        (580, 80, "Targets", "multi-user", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    parts.append(label(360, 195, "Failures: firmware → GRUB → kernel panic → unit failures", 13, "400"))
    write_pair("linux-boot-process", 740, 230, "\n".join(parts), [])


def diagram_linux_filesystem():
    rng = random.Random(703)
    parts = [label(370, 28, "Filesystem hierarchy", 18)]
    parts.append(soft_box(rng, 280, 50, 180, 55, "/", "root", "gray"))
    row = [
        (40, 140, "/etc", "config", "blue"),
        (200, 140, "/var", "logs · state", "green"),
        (360, 140, "/home", "users", "orange"),
        (520, 140, "/usr", "programs", "purple"),
    ]
    for x, y, t, s, c in row:
        parts.append(soft_box(rng, x, y, 140, 60, t, s, c))
        parts.append(arrow(rng, 370, 105, x + 70, 140))
    parts.append(soft_box(rng, 200, 230, 340, 55, "inodes · mounts · links", "path ≠ inode", "teal"))
    write_pair("linux-filesystem-hierarchy", 720, 320, "\n".join(parts), [])


def diagram_linux_process_lifecycle():
    rng = random.Random(704)
    parts = [label(400, 28, "Process lifecycle", 18)]
    chain = [
        (30, 80, "fork/exec", "create", "blue"),
        (180, 80, "Running", "R / S", "green"),
        (330, 80, "Stopped", "T · signals", "yellow"),
        (480, 80, "Zombie", "wait", "orange"),
        (630, 80, "Exit", "reaped", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    parts.append(label(400, 195, "Tools: ps · top · nice · kill · systemctl status", 13, "400"))
    write_pair("linux-process-lifecycle", 800, 230, "\n".join(parts), [])


def diagram_linux_storage():
    rng = random.Random(705)
    parts = [label(390, 28, "Storage layout", 18)]
    parts.append(soft_box(rng, 40, 70, 140, 70, "Disk", "nvme/sda", "gray"))
    parts.append(soft_box(rng, 220, 70, 140, 70, "Partition", "GPT", "blue"))
    parts.append(soft_box(rng, 400, 70, 140, 70, "LVM / FS", "ext4/xfs", "green"))
    parts.append(soft_box(rng, 580, 70, 160, 70, "Mount", "/data", "orange"))
    for x1, x2 in [(180, 220), (360, 400), (540, 580)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(soft_box(rng, 220, 180, 360, 60, "Swap · df · iostat · smartctl", "capacity & health", "purple"))
    write_pair("linux-storage-layout", 780, 280, "\n".join(parts), [])


def diagram_linux_networking():
    rng = random.Random(706)
    parts = [label(400, 28, "Linux networking stack", 18)]
    parts.append(soft_box(rng, 40, 70, 150, 70, "App", "sockets", "blue"))
    parts.append(soft_box(rng, 230, 70, 150, 70, "Kernel net", "TCP/IP", "green"))
    parts.append(soft_box(rng, 420, 70, 150, 70, "nftables", "filter/NAT", "orange"))
    parts.append(soft_box(rng, 610, 70, 150, 70, "NIC", "eth0", "purple"))
    for x1, x2 in [(190, 230), (380, 420), (570, 610)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(400, 180, "ip · ss · dig · curl · tcpdump for ops triage", 13, "400"))
    write_pair("linux-networking-stack", 800, 220, "\n".join(parts), [])


def diagram_linux_systemd():
    rng = random.Random(707)
    parts = [label(405, 28, "systemd architecture", 18)]
    parts.append(soft_box(rng, 300, 50, 200, 60, "systemd", "PID 1", "orange"))
    parts.append(soft_box(rng, 40, 150, 160, 65, "Units", ".service", "blue"))
    parts.append(soft_box(rng, 230, 150, 160, 65, "Targets", "boot goals", "green"))
    parts.append(soft_box(rng, 420, 150, 160, 65, "Timers", "cron-like", "purple"))
    parts.append(soft_box(rng, 610, 150, 160, 65, "journald", "logs", "teal"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 400, 110, x, 150))
    write_pair("linux-systemd-architecture", 810, 250, "\n".join(parts), [])


def diagram_linux_permissions():
    rng = random.Random(708)
    parts = [label(405, 28, "Permission model", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "User", "UID", "blue"))
    parts.append(soft_box(rng, 230, 70, 160, 70, "Group", "GID", "green"))
    parts.append(soft_box(rng, 420, 70, 160, 70, "Mode bits", "rwx / ACL", "orange"))
    parts.append(soft_box(rng, 610, 70, 160, 70, "sudo", "escalation", "purple"))
    for x1, x2 in [(200, 230), (390, 420), (580, 610)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(400, 180, "Special bits: setuid · setgid · sticky", 13, "400"))
    write_pair("linux-permission-model", 810, 220, "\n".join(parts), [])


def diagram_linux_containers():
    rng = random.Random(709)
    parts = [label(405, 28, "Container internals", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 75, "Namespaces", "PID · net · mnt", "blue"))
    parts.append(soft_box(rng, 230, 70, 160, 75, "cgroups", "CPU · memory", "green"))
    parts.append(soft_box(rng, 420, 70, 160, 75, "OverlayFS", "layers", "orange"))
    parts.append(soft_box(rng, 610, 70, 160, 75, "OCI runtime", "runc", "purple"))
    for x1, x2 in [(200, 230), (390, 420), (580, 610)]:
        parts.append(arrow(rng, x1, 108, x2, 108))
    parts.append(label(400, 185, "Shared kernel — isolation is not a full VM", 13, "400"))
    write_pair("linux-container-internals", 810, 230, "\n".join(parts), [])


def diagram_linux_cli():
    rng = random.Random(710)
    parts = [label(400, 28, "Essential CLI workflow", 18)]
    chain = [
        (30, 80, "Navigate", "cd · ls · pwd", "blue"),
        (180, 80, "Inspect", "cat · less", "green"),
        (330, 80, "Find", "find · grep", "orange"),
        (480, 80, "Edit", "vim · nano", "purple"),
        (630, 80, "Pipe", "| · >", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    write_pair("linux-cli-workflow", 800, 200, "\n".join(parts), [])


def diagram_linux_text():
    rng = random.Random(711)
    parts = [label(380, 28, "Text processing pipeline", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "Input", "logs · files", "gray"))
    parts.append(soft_box(rng, 220, 80, 140, 70, "grep", "filter", "blue"))
    parts.append(soft_box(rng, 400, 80, 140, 70, "sed", "transform", "green"))
    parts.append(soft_box(rng, 580, 80, 140, 70, "awk", "fields", "orange"))
    for x1, x2 in [(180, 220), (360, 400), (540, 580)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("linux-text-processing", 760, 200, "\n".join(parts), [])


def diagram_linux_ssh():
    rng = random.Random(712)
    parts = [label(350, 28, "SSH access & hardening", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 75, "Client", "ssh · keys", "blue"))
    parts.append(soft_box(rng, 250, 70, 180, 75, "sshd", "auth · config", "green"))
    parts.append(soft_box(rng, 480, 70, 160, 75, "Host", "bastion", "orange"))
    parts.append(soft_box(rng, 250, 180, 180, 60, "Firewall", "22/tcp limit", "purple"))
    parts.append(arrow(rng, 200, 108, 250, 108))
    parts.append(arrow(rng, 430, 108, 480, 108))
    parts.append(arrow(rng, 340, 145, 340, 180))
    write_pair("linux-ssh-access", 700, 280, "\n".join(parts), [])


def diagram_linux_packages():
    rng = random.Random(713)
    parts = [label(420, 28, "Package management", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Repo", "mirror", "blue"))
    parts.append(soft_box(rng, 240, 80, 180, 70, "dnf / apt", "solver", "green"))
    parts.append(soft_box(rng, 460, 80, 160, 70, "Packages", "rpm/deb", "orange"))
    parts.append(soft_box(rng, 660, 80, 140, 70, "System", "files", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("linux-package-management", 840, 200, "\n".join(parts), [])


def diagram_linux_scheduling():
    rng = random.Random(714)
    parts = [label(340, 28, "Scheduling jobs", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "cron", "crontab", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "at", "one-shot", "green"))
    parts.append(soft_box(rng, 440, 80, 180, 70, "systemd timer", "calendar", "orange"))
    parts.append(soft_box(rng, 200, 190, 300, 60, "Logs · mail · OnCalendar", "verify runs", "purple"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 400, 115, 440, 115))
    write_pair("linux-scheduling", 680, 290, "\n".join(parts), [])


def diagram_linux_logging():
    rng = random.Random(715)
    parts = [label(340, 28, "Logging on Linux", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Apps", "stdout · syslog", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "journald", "structured", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "/var/log", "files", "orange"))
    parts.append(soft_box(rng, 240, 180, 180, 60, "logrotate", "retain", "purple"))
    parts.append(arrow(rng, 200, 105, 240, 105))
    parts.append(arrow(rng, 420, 105, 460, 105))
    parts.append(arrow(rng, 330, 140, 330, 180))
    write_pair("linux-logging", 680, 280, "\n".join(parts), [])


def diagram_linux_monitoring():
    rng = random.Random(716)
    parts = [label(405, 28, "Host monitoring signals", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "CPU", "vmstat · top", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "Memory", "free · psi", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "Disk I/O", "iostat", "orange"))
    parts.append(soft_box(rng, 610, 80, 160, 70, "History", "sar", "purple"))
    write_pair("linux-host-monitoring", 810, 200, "\n".join(parts), [])


def diagram_linux_security():
    rng = random.Random(717)
    parts = [label(390, 28, "Linux security layers", 18)]
    parts.append(soft_box(rng, 40, 70, 150, 70, "PAM", "auth stack", "blue"))
    parts.append(soft_box(rng, 220, 70, 150, 70, "MAC", "SELinux/AppArmor", "green"))
    parts.append(soft_box(rng, 400, 70, 150, 70, "Audit", "auditd", "orange"))
    parts.append(soft_box(rng, 580, 70, 160, 70, "Fail2Ban", "bruteforce", "purple"))
    for x1, x2 in [(190, 220), (370, 400), (550, 580)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("linux-security-layers", 780, 200, "\n".join(parts), [])


def diagram_linux_troubleshooting():
    rng = random.Random(718)
    parts = [label(375, 28, "Linux troubleshooting ladder", 18)]
    chain = [
        (20, 80, "Symptom", "who · what", "red"),
        (160, 80, "Logs", "journalctl", "orange"),
        (300, 80, "Resources", "CPU/mem/disk", "yellow"),
        (440, 80, "Services", "systemctl", "green"),
        (580, 80, "Fix/verify", "rollback", "blue"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("linux-troubleshooting", 740, 200, "\n".join(parts), [])


def diagram_linux_backup():
    rng = random.Random(719)
    parts = [label(330, 28, "Backup & DR", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Sources", "data · config", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "Backup", "rsync · snaps", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "Offsite", "object store", "orange"))
    parts.append(soft_box(rng, 200, 190, 280, 60, "Restore test", "RPO / RTO", "purple"))
    for x1, x2 in [(200, 240), (400, 440)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("linux-backup-dr", 660, 290, "\n".join(parts), [])


def diagram_linux_production():
    rng = random.Random(720)
    parts = [label(420, 28, "Production Linux baseline", 18)]
    parts.append(soft_box(rng, 40, 70, 170, 70, "Harden", "SSH · patch", "blue"))
    parts.append(soft_box(rng, 240, 70, 170, 70, "Observe", "logs · metrics", "green"))
    parts.append(soft_box(rng, 440, 70, 170, 70, "Capacity", "disk · CPU", "orange"))
    parts.append(soft_box(rng, 640, 70, 160, 70, "Recover", "backup · runbook", "purple"))
    for x1, x2 in [(210, 240), (410, 440), (610, 640)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("linux-production", 840, 200, "\n".join(parts), [])


# --- Shell Scripting for DevOps (polished Excalidraw) ---


def diagram_shell_execution():
    rng = random.Random(801)
    parts = [label(410, 28, "Shell execution flow", 18)]
    parts.append(soft_box(rng, 40, 70, 150, 70, "Terminal", "TTY", "gray"))
    parts.append(soft_box(rng, 230, 70, 160, 70, "Shell", "bash / sh", "blue"))
    parts.append(soft_box(rng, 430, 70, 160, 70, "Parse/expand", "quotes · globs", "green"))
    parts.append(soft_box(rng, 630, 70, 150, 70, "Exec", "builtins/bin", "orange"))
    for x1, x2 in [(190, 230), (390, 430), (590, 630)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(410, 180, "Bash for scripts · prefer POSIX when portability matters", 13, "400"))
    write_pair("shell-execution-flow", 820, 220, "\n".join(parts), [])


def diagram_shell_lifecycle():
    rng = random.Random(802)
    parts = [label(375, 28, "Bash script lifecycle", 18)]
    chain = [
        (30, 80, "Write", "shebang", "blue"),
        (170, 80, "chmod +x", "execute bit", "green"),
        (310, 80, "Run", "./script.sh", "orange"),
        (450, 80, "Exit code", "0 / non-zero", "purple"),
        (590, 80, "Logs", "stdout/err", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("shell-script-lifecycle", 750, 200, "\n".join(parts), [])


def diagram_shell_variables():
    rng = random.Random(803)
    parts = [label(420, 28, "Variables & quoting", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 75, "Assign", "name=value", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 75, "Expand", "quoted $name", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 75, "Quote", "word-split safe", "orange"))
    parts.append(soft_box(rng, 660, 70, 140, 75, "Arithmetic", "n+1", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 108, x2, 108))
    write_pair("shell-variables-quoting", 840, 200, "\n".join(parts), [])


def diagram_shell_io():
    rng = random.Random(804)
    parts = [label(390, 28, "I/O redirection & pipes", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "stdin", "fd 0", "blue"))
    parts.append(soft_box(rng, 220, 80, 160, 70, "Command", "filter", "green"))
    parts.append(soft_box(rng, 420, 80, 140, 70, "stdout", "fd 1", "orange"))
    parts.append(soft_box(rng, 600, 80, 140, 70, "stderr", "fd 2", "red"))
    parts.append(arrow(rng, 180, 115, 220, 115))
    parts.append(arrow(rng, 380, 115, 420, 115))
    parts.append(arrow(rng, 380, 130, 600, 115))
    parts.append(label(380, 190, "Pipe connects stdout to the next stdin", 13, "400"))
    write_pair("shell-io-redirection", 780, 230, "\n".join(parts), [])


def diagram_shell_control():
    rng = random.Random(805)
    parts = [label(340, 28, "Control flow", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "test / [[ ]]", "condition", "blue"))
    parts.append(soft_box(rng, 250, 40, 160, 60, "then", "true path", "green"))
    parts.append(soft_box(rng, 250, 130, 160, 60, "else", "false path", "orange"))
    parts.append(soft_box(rng, 460, 80, 180, 70, "case / && ||", "branches", "purple"))
    parts.append(arrow(rng, 200, 100, 250, 70))
    parts.append(arrow(rng, 200, 130, 250, 160))
    parts.append(arrow(rng, 410, 115, 460, 115))
    write_pair("shell-control-flow", 680, 230, "\n".join(parts), [])


def diagram_shell_loops():
    rng = random.Random(806)
    parts = [label(330, 28, "Loops", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "for", "lists · globs", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "while", "until false", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "until", "until true", "orange"))
    parts.append(soft_box(rng, 200, 190, 280, 55, "break · continue", "careful with IFS", "purple"))
    write_pair("shell-loops-flow", 660, 280, "\n".join(parts), [])


def diagram_shell_functions():
    rng = random.Random(807)
    parts = [label(370, 28, "Functions & scope", 18)]
    parts.append(soft_box(rng, 40, 80, 180, 70, "Caller", "main script", "blue"))
    parts.append(soft_box(rng, 280, 80, 180, 70, "function", "params", "green"))
    parts.append(soft_box(rng, 520, 80, 180, 70, "local vars", "no leak", "orange"))
    parts.append(arrow(rng, 220, 115, 280, 115))
    parts.append(arrow(rng, 460, 115, 520, 115))
    write_pair("shell-functions-locals", 740, 200, "\n".join(parts), [])


def diagram_shell_arrays():
    rng = random.Random(808)
    parts = [label(380, 28, "Arrays & strings", 18)]
    parts.append(soft_box(rng, 40, 80, 200, 70, "Indexed array", "arr[i]", "blue"))
    parts.append(soft_box(rng, 280, 80, 200, 70, "Associative", "declare -A", "green"))
    parts.append(soft_box(rng, 520, 80, 200, 70, "Expansion", "trim · slice", "orange"))
    write_pair("shell-arrays-strings", 760, 200, "\n".join(parts), [])


def diagram_shell_files():
    rng = random.Random(809)
    parts = [label(350, 28, "File operations in scripts", 18)]
    chain = [
        (40, 80, "Test", "-f -d -r", "blue"),
        (200, 80, "Create", "mkdir · touch", "green"),
        (360, 80, "Copy/move", "cp · mv", "orange"),
        (520, 80, "Safe delete", "rm carefully", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 140, 70, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 140, y + 35, chain[i + 1][0], y + 35))
    write_pair("shell-file-operations", 700, 200, "\n".join(parts), [])


def diagram_shell_text():
    rng = random.Random(810)
    parts = [label(375, 28, "Text tools in scripts", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "grep", "match", "blue"))
    parts.append(soft_box(rng, 210, 80, 140, 70, "sed", "edit stream", "green"))
    parts.append(soft_box(rng, 380, 80, 140, 70, "awk", "columns", "orange"))
    parts.append(soft_box(rng, 550, 80, 160, 70, "cut/sort/uniq", "shape data", "purple"))
    for x1, x2 in [(180, 210), (350, 380), (520, 550)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("shell-text-processing", 750, 200, "\n".join(parts), [])


def diagram_shell_process():
    rng = random.Random(811)
    parts = [label(350, 28, "Signals & process automation", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Script", "foreground", "blue"))
    parts.append(soft_box(rng, 250, 70, 180, 70, "trap", "EXIT · INT · TERM", "green"))
    parts.append(soft_box(rng, 480, 70, 160, 70, "Cleanup", "temp files", "orange"))
    parts.append(soft_box(rng, 210, 180, 300, 55, "Background jobs · wait · kill", "job control", "purple"))
    parts.append(arrow(rng, 200, 105, 250, 105))
    parts.append(arrow(rng, 430, 105, 480, 105))
    write_pair("shell-process-automation", 700, 280, "\n".join(parts), [])


def diagram_shell_pipeline():
    rng = random.Random(812)
    parts = [label(410, 28, "Process pipeline", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Producer", "cmd1", "blue"))
    parts.append(soft_box(rng, 240, 80, 150, 70, "Filter", "cmd2", "green"))
    parts.append(soft_box(rng, 440, 80, 150, 70, "Consumer", "cmd3", "orange"))
    parts.append(soft_box(rng, 640, 80, 140, 70, "Exit", "pipefail", "purple"))
    for x1, x2 in [(190, 240), (390, 440), (590, 640)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("shell-process-pipeline", 820, 200, "\n".join(parts), [])


def diagram_shell_cron():
    rng = random.Random(813)
    parts = [label(340, 28, "Cron / timer execution", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Schedule", "crontab", "blue"))
    parts.append(soft_box(rng, 240, 80, 180, 70, "Environment", "PATH · mail", "green"))
    parts.append(soft_box(rng, 460, 80, 160, 70, "Script", "absolute paths", "orange"))
    parts.append(soft_box(rng, 200, 190, 300, 55, "Logs · exit codes · systemd timer", "verify", "purple"))
    for x1, x2 in [(200, 240), (420, 460)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("shell-cron-execution", 680, 280, "\n".join(parts), [])


def diagram_shell_json():
    rng = random.Random(814)
    parts = [label(330, 28, "JSON / YAML in shell", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "API / file", "JSON/YAML", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "jq", "JSON query", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "yq", "YAML query", "orange"))
    parts.append(soft_box(rng, 200, 190, 280, 55, "Pipe into automation", "safe quoting", "purple"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 400, 115, 440, 115))
    write_pair("shell-json-yaml", 660, 280, "\n".join(parts), [])


def diagram_shell_errors():
    rng = random.Random(815)
    parts = [label(410, 28, "Error handling & debug", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "set -euo", "pipefail", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "trap ERR", "cleanup", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "Logging", "logger · tee", "orange"))
    parts.append(soft_box(rng, 640, 80, 140, 70, "Debug", "bash -x", "purple"))
    for x1, x2 in [(200, 240), (400, 440), (600, 640)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("shell-error-handling", 820, 200, "\n".join(parts), [])


def diagram_shell_automation():
    rng = random.Random(816)
    parts = [label(375, 28, "Shell automation workflow", 18)]
    chain = [
        (30, 80, "Discover", "inventory", "blue"),
        (170, 80, "Act", "ssh · API", "green"),
        (310, 80, "Validate", "exit codes", "orange"),
        (450, 80, "Report", "logs", "purple"),
        (590, 80, "Schedule", "cron/CI", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("shell-automation-workflow", 750, 200, "\n".join(parts), [])


def diagram_shell_troubleshooting():
    rng = random.Random(817)
    parts = [label(380, 28, "Shell troubleshooting", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "Reproduce", "same env", "red"))
    parts.append(soft_box(rng, 210, 80, 140, 70, "bash -x", "trace", "orange"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "Quotes/IFS", "word-split", "yellow"))
    parts.append(soft_box(rng, 560, 80, 160, 70, "PATH · +x", "permissions", "green"))
    for x1, x2 in [(180, 210), (350, 380), (530, 560)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("shell-troubleshooting", 760, 200, "\n".join(parts), [])



# --- Terraform for Cloud & DevOps (polished Excalidraw) ---


def diagram_terraform_workflow():
    rng = random.Random(901)
    parts = [label(400, 28, "Terraform workflow", 18)]
    chain = [
        (20, 80, "Write", "HCL · .tf", "blue"),
        (160, 80, "Init", "providers", "green"),
        (300, 80, "Plan", "preview", "orange"),
        (440, 80, "Apply", "mutate", "purple"),
        (580, 80, "State", "mapping", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    parts.append(label(360, 195, "Destroy reverses apply using the same state mapping", 13, "400"))
    write_pair("terraform-workflow", 740, 230, "\n".join(parts), [])


def diagram_terraform_architecture():
    rng = random.Random(902)
    parts = [label(420, 28, "Terraform architecture", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Config", ".tf · modules", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "Terraform core", "graph · plan", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "Providers", "plugins", "orange"))
    parts.append(soft_box(rng, 660, 70, 160, 70, "APIs", "cloud · k8s", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(soft_box(rng, 240, 180, 360, 60, "State file", "IDs · attributes", "teal"))
    parts.append(arrow(rng, 330, 140, 330, 180))
    write_pair("terraform-architecture", 860, 280, "\n".join(parts), [])


def diagram_terraform_cli():
    rng = random.Random(903)
    parts = [label(390, 28, "Core CLI commands", 18)]
    parts.append(soft_box(rng, 40, 70, 130, 65, "fmt", "style", "gray"))
    parts.append(soft_box(rng, 190, 70, 130, 65, "validate", "syntax", "blue"))
    parts.append(soft_box(rng, 340, 70, 130, 65, "plan", "diff", "green"))
    parts.append(soft_box(rng, 490, 70, 130, 65, "apply", "change", "orange"))
    parts.append(soft_box(rng, 640, 70, 130, 65, "destroy", "remove", "red"))
    write_pair("terraform-cli-commands", 810, 180, "\n".join(parts), [])


def diagram_terraform_hcl():
    rng = random.Random(904)
    parts = [label(380, 28, "HCL building blocks", 18)]
    parts.append(soft_box(rng, 40, 70, 150, 70, "Blocks", "resource · var", "blue"))
    parts.append(soft_box(rng, 220, 70, 150, 70, "Arguments", "key = value", "green"))
    parts.append(soft_box(rng, 400, 70, 150, 70, "Expressions", "refs · funcs", "orange"))
    parts.append(soft_box(rng, 580, 70, 150, 70, "Locals", "computed", "purple"))
    write_pair("terraform-hcl-blocks", 770, 180, "\n".join(parts), [])


def diagram_terraform_providers():
    rng = random.Random(905)
    parts = [label(400, 28, "Provider model", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "required_providers", "version pin", "blue"))
    parts.append(soft_box(rng, 240, 70, 160, 70, "provider {}", "auth · region", "green"))
    parts.append(soft_box(rng, 440, 70, 160, 70, "alias", "multi-region", "orange"))
    parts.append(soft_box(rng, 640, 70, 140, 70, "Registry", "plugins", "purple"))
    for x1, x2 in [(200, 240), (400, 440), (600, 640)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("terraform-providers", 820, 180, "\n".join(parts), [])


def diagram_terraform_resources():
    rng = random.Random(906)
    parts = [label(420, 28, "Resources & meta-arguments", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "resource", "managed", "blue"))
    parts.append(soft_box(rng, 240, 70, 140, 70, "count", "N copies", "green"))
    parts.append(soft_box(rng, 410, 70, 150, 70, "for_each", "map/set", "orange"))
    parts.append(soft_box(rng, 590, 70, 160, 70, "lifecycle", "create_before", "purple"))
    parts.append(soft_box(rng, 220, 180, 360, 55, "depends_on · graph edges", "implicit + explicit", "teal"))
    write_pair("terraform-resources", 800, 270, "\n".join(parts), [])


def diagram_terraform_variables():
    rng = random.Random(907)
    parts = [label(400, 28, "Variables → resources → outputs", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "variable", "tfvars · env", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "locals", "reshape", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "resource", "consume", "orange"))
    parts.append(soft_box(rng, 640, 80, 140, 70, "output", "export", "purple"))
    for x1, x2 in [(200, 240), (400, 440), (600, 640)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("terraform-variables-flow", 820, 200, "\n".join(parts), [])


def diagram_terraform_state():
    rng = random.Random(908)
    parts = [label(360, 28, "State management", 18)]
    parts.append(soft_box(rng, 40, 70, 180, 75, "Configuration", "desired", "blue"))
    parts.append(soft_box(rng, 280, 70, 180, 75, "State", "real IDs", "green"))
    parts.append(soft_box(rng, 520, 70, 180, 75, "Infrastructure", "APIs", "orange"))
    parts.append(arrow(rng, 220, 108, 280, 108))
    parts.append(arrow(rng, 460, 108, 520, 108))
    parts.append(label(360, 185, "Never edit state by hand unless recovering carefully", 13, "400"))
    write_pair("terraform-state", 740, 220, "\n".join(parts), [])


def diagram_terraform_remote():
    rng = random.Random(909)
    parts = [label(400, 28, "Remote state backend", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Engineers / CI", "terraform", "blue"))
    parts.append(soft_box(rng, 250, 70, 200, 70, "Backend", "S3 · Azurerm · GCS", "green"))
    parts.append(soft_box(rng, 500, 70, 180, 70, "Lock table", "DynamoDB etc.", "orange"))
    parts.append(arrow(rng, 200, 105, 250, 105))
    parts.append(arrow(rng, 450, 105, 500, 105))
    parts.append(soft_box(rng, 200, 180, 340, 55, "Encrypt · IAM · no local terraform.tfstate", "team safe", "purple"))
    write_pair("terraform-remote-backend", 720, 270, "\n".join(parts), [])


def diagram_terraform_modules():
    rng = random.Random(910)
    parts = [label(400, 28, "Module architecture", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 60, "Root module", "env · wiring", "orange"))
    parts.append(soft_box(rng, 40, 150, 160, 65, "network", "VPC", "blue"))
    parts.append(soft_box(rng, 230, 150, 160, 65, "compute", "ASG/VM", "green"))
    parts.append(soft_box(rng, 420, 150, 160, 65, "data", "DB · bucket", "purple"))
    parts.append(soft_box(rng, 610, 150, 160, 65, "Registry", "versioned", "teal"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 380, 110, x, 150))
    write_pair("terraform-modules", 810, 250, "\n".join(parts), [])


def diagram_terraform_expressions():
    rng = random.Random(911)
    parts = [label(390, 28, "Expressions & functions", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Conditionals", "a ? b : c", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "for", "transform", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "Functions", "join · coalesce", "orange"))
    parts.append(soft_box(rng, 610, 80, 160, 70, "dynamic", "nested blocks", "purple"))
    write_pair("terraform-expressions", 810, 200, "\n".join(parts), [])


def diagram_terraform_data():
    rng = random.Random(912)
    parts = [label(360, 28, "Data sources", 18)]
    parts.append(soft_box(rng, 40, 80, 180, 70, "Existing infra", "AMI · VPC · DNS", "blue"))
    parts.append(soft_box(rng, 270, 80, 180, 70, "data {}", "read-only", "green"))
    parts.append(soft_box(rng, 500, 80, 180, 70, "Resources", "consume attrs", "orange"))
    parts.append(arrow(rng, 220, 115, 270, 115))
    parts.append(arrow(rng, 450, 115, 500, 115))
    write_pair("terraform-data-sources", 720, 200, "\n".join(parts), [])


def diagram_terraform_workspaces():
    rng = random.Random(913)
    parts = [label(380, 28, "Workspaces & environments", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "dev", "state key", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "staging", "state key", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "prod", "state key", "orange"))
    parts.append(soft_box(rng, 200, 190, 280, 55, "Prefer separate roots for prod", "blast radius", "purple"))
    write_pair("terraform-workspaces", 640, 280, "\n".join(parts), [])


def diagram_terraform_cloud():
    rng = random.Random(914)
    parts = [label(400, 28, "HCP Terraform / Cloud", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "VCS", "Git PR", "blue"))
    parts.append(soft_box(rng, 240, 70, 200, 70, "HCP Terraform", "runs · policy", "green"))
    parts.append(soft_box(rng, 480, 70, 160, 70, "State", "remote", "orange"))
    parts.append(soft_box(rng, 680, 70, 120, 70, "Cloud", "apply", "purple"))
    for x1, x2 in [(200, 240), (440, 480), (640, 680)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("terraform-cloud", 840, 180, "\n".join(parts), [])


def diagram_terraform_testing():
    rng = random.Random(915)
    parts = [label(380, 28, "Testing & validation", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "fmt", "style", "gray"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "validate", "config", "blue"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "terraform test", "assertions", "green"))
    parts.append(soft_box(rng, 550, 80, 160, 70, "Policy / lint", "OPA · tflint", "orange"))
    write_pair("terraform-testing", 750, 200, "\n".join(parts), [])


def diagram_terraform_security():
    rng = random.Random(916)
    parts = [label(400, 28, "Terraform security layers", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Secrets", "Vault · SSM", "blue"))
    parts.append(soft_box(rng, 230, 70, 160, 70, "sensitive", "redact", "green"))
    parts.append(soft_box(rng, 420, 70, 160, 70, "IAM least", "roles", "orange"))
    parts.append(soft_box(rng, 610, 70, 160, 70, "Policy", "Sentinel/OPA", "purple"))
    write_pair("terraform-security", 810, 180, "\n".join(parts), [])


def diagram_terraform_cicd():
    rng = random.Random(917)
    parts = [label(400, 28, "Terraform CI/CD", 18)]
    chain = [
        (20, 80, "PR", "plan", "blue"),
        (160, 80, "Review", "artifact", "green"),
        (300, 80, "Approve", "gate", "orange"),
        (440, 80, "Apply", "main", "purple"),
        (580, 80, "Drift", "detect", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("terraform-cicd-pipeline", 740, 200, "\n".join(parts), [])


def diagram_terraform_multicloud():
    rng = random.Random(918)
    parts = [label(390, 28, "Multi-cloud with Terraform", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "Shared modules", "interfaces", "gray"))
    parts.append(soft_box(rng, 40, 140, 160, 70, "AWS", "aws provider", "orange"))
    parts.append(soft_box(rng, 230, 140, 160, 70, "Azure", "azurerm", "blue"))
    parts.append(soft_box(rng, 420, 140, 160, 70, "GCP", "google", "green"))
    parts.append(soft_box(rng, 610, 140, 160, 70, "Same HCL", "diff providers", "purple"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("terraform-multi-cloud", 810, 250, "\n".join(parts), [])


def diagram_terraform_kubernetes():
    rng = random.Random(919)
    parts = [label(400, 28, "Kubernetes with Terraform", 18)]
    parts.append(soft_box(rng, 40, 70, 180, 70, "Cloud provider", "EKS/AKS/GKE", "blue"))
    parts.append(soft_box(rng, 260, 70, 180, 70, "kubernetes", "objects", "green"))
    parts.append(soft_box(rng, 480, 70, 180, 70, "helm provider", "charts", "orange"))
    parts.append(arrow(rng, 220, 105, 260, 105))
    parts.append(arrow(rng, 440, 105, 480, 105))
    parts.append(label(360, 180, "Prefer GitOps for app deploys; TF for cluster platform", 13, "400"))
    write_pair("terraform-kubernetes", 700, 220, "\n".join(parts), [])


def diagram_terraform_production():
    rng = random.Random(920)
    parts = [label(420, 28, "Production repository structure", 18)]
    parts.append(soft_box(rng, 40, 70, 180, 70, "modules/", "reusable", "blue"))
    parts.append(soft_box(rng, 250, 70, 180, 70, "envs/dev|prod", "roots", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "CI", "plan/apply", "orange"))
    parts.append(soft_box(rng, 650, 70, 140, 70, "Policy", "gates", "purple"))
    write_pair("terraform-repo-structure", 830, 180, "\n".join(parts), [])


def diagram_terraform_troubleshoot():
    rng = random.Random(921)
    parts = [label(390, 28, "Troubleshooting ladder", 18)]
    chain = [
        (20, 80, "Auth", "creds", "red"),
        (150, 80, "Provider", "versions", "orange"),
        (280, 80, "State", "lock/drift", "yellow"),
        (410, 80, "Graph", "cycles", "green"),
        (540, 80, "Fix", "import/move", "blue"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("terraform-troubleshooting", 700, 200, "\n".join(parts), [])



# --- GitLab CI/CD for Cloud & DevOps (polished Excalidraw) ---


def diagram_gitlab_architecture():
    rng = random.Random(1001)
    parts = [label(420, 28, "GitLab CI/CD architecture", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "GitLab", "repo · MR · API", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "CI coordinator", "pipelines", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "Runners", "executors", "orange"))
    parts.append(soft_box(rng, 660, 70, 140, 70, "Targets", "k8s · cloud", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(420, 180, "SaaS or self-managed — same .gitlab-ci.yml model", 13, "400"))
    write_pair("gitlab-architecture", 840, 220, "\n".join(parts), [])


def diagram_gitlab_pipeline_flow():
    rng = random.Random(1002)
    parts = [label(400, 28, "Pipeline flow", 18)]
    chain = [
        (20, 80, "Commit/MR", "trigger", "blue"),
        (160, 80, "Stages", "build·test", "green"),
        (300, 80, "Jobs", "scripts", "orange"),
        (440, 80, "Artifacts", "pass on", "purple"),
        (580, 80, "Deploy", "env", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("gitlab-pipeline-flow", 740, 200, "\n".join(parts), [])


def diagram_gitlab_runners():
    rng = random.Random(1003)
    parts = [label(400, 28, "Runner architecture", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "GitLab", "job queue", "gray"))
    parts.append(soft_box(rng, 40, 140, 150, 70, "Shared", "instance", "blue"))
    parts.append(soft_box(rng, 220, 140, 150, 70, "Group", "org", "green"))
    parts.append(soft_box(rng, 400, 140, 150, 70, "Project", "dedicated", "orange"))
    parts.append(soft_box(rng, 580, 140, 180, 70, "Executors", "shell·docker·k8s", "purple"))
    for x in [115, 295, 475, 670]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("gitlab-runner-architecture", 800, 250, "\n".join(parts), [])


def diagram_gitlab_projects():
    rng = random.Random(1004)
    parts = [label(380, 28, "Projects · MRs · releases", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Repository", "branches", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "Merge request", "pipeline", "green"))
    parts.append(soft_box(rng, 430, 80, 150, 70, "Protected", "main/tags", "orange"))
    parts.append(soft_box(rng, 620, 80, 140, 70, "Release", "changelog", "purple"))
    for x1, x2 in [(190, 230), (390, 430), (580, 620)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("gitlab-projects-mr", 800, 200, "\n".join(parts), [])


def diagram_gitlab_syntax():
    rng = random.Random(1005)
    parts = [label(390, 28, "Pipeline syntax building blocks", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "stages", "order", "blue"))
    parts.append(soft_box(rng, 200, 80, 140, 70, "rules", "when", "green"))
    parts.append(soft_box(rng, 360, 80, 140, 70, "needs", "DAG", "orange"))
    parts.append(soft_box(rng, 520, 80, 140, 70, "variables", "config", "purple"))
    parts.append(soft_box(rng, 680, 80, 120, 70, "workflow", "pipeline", "teal"))
    write_pair("gitlab-pipeline-syntax", 840, 200, "\n".join(parts), [])


def diagram_gitlab_parent_child():
    rng = random.Random(1006)
    parts = [label(400, 28, "Parent / child & includes", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 60, "Parent pipeline", "orchestrate", "orange"))
    parts.append(soft_box(rng, 40, 150, 160, 65, "Child A", "build", "blue"))
    parts.append(soft_box(rng, 230, 150, 160, 65, "Child B", "test", "green"))
    parts.append(soft_box(rng, 420, 150, 160, 65, "include", "templates", "purple"))
    parts.append(soft_box(rng, 610, 150, 160, 65, "trigger", "downstream", "teal"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 380, 110, x, 150))
    write_pair("gitlab-parent-child", 810, 250, "\n".join(parts), [])


def diagram_gitlab_secrets():
    rng = random.Random(1007)
    parts = [label(400, 28, "Variables & secrets", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "CI variables", "masked", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "Protected", "branch/env", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "OIDC", "cloud roles", "orange"))
    parts.append(soft_box(rng, 610, 80, 160, 70, "Vault", "dynamic", "purple"))
    write_pair("gitlab-variables-secrets", 810, 200, "\n".join(parts), [])


def diagram_gitlab_artifacts():
    rng = random.Random(1008)
    parts = [label(390, 28, "Artifacts & cache", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Job A", "build", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "Artifacts", "pass files", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "Job B", "test/deploy", "orange"))
    parts.append(soft_box(rng, 240, 180, 160, 55, "Cache", "deps speed", "purple"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 400, 115, 440, 115))
    parts.append(arrow(rng, 320, 150, 320, 180))
    write_pair("gitlab-artifacts-cache", 660, 270, "\n".join(parts), [])


def diagram_gitlab_docker():
    rng = random.Random(1009)
    parts = [label(400, 28, "Docker pipelines", 18)]
    chain = [
        (30, 80, "Dockerfile", "BuildKit", "blue"),
        (180, 80, "Build", "CI job", "green"),
        (330, 80, "Registry", "GitLab CR", "orange"),
        (480, 80, "Scan", "security", "purple"),
        (630, 80, "Promote", "envs", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    write_pair("gitlab-docker-pipeline", 800, 200, "\n".join(parts), [])


def diagram_gitlab_k8s():
    rng = random.Random(1010)
    parts = [label(400, 28, "Kubernetes deployment", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Pipeline", "deploy job", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "GitLab Agent", "cluster link", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "Helm/kubectl", "manifests", "orange"))
    parts.append(soft_box(rng, 660, 70, 140, 70, "Cluster", "workload", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("gitlab-kubernetes-deploy", 840, 180, "\n".join(parts), [])


def diagram_gitlab_agent():
    rng = random.Random(1011)
    parts = [label(360, 28, "GitLab Agent for Kubernetes", 18)]
    parts.append(soft_box(rng, 40, 80, 180, 70, "GitLab", "agent config", "blue"))
    parts.append(soft_box(rng, 280, 80, 180, 70, "agentk", "in-cluster", "green"))
    parts.append(soft_box(rng, 520, 80, 180, 70, "API server", "deploy/CI", "orange"))
    parts.append(arrow(rng, 220, 115, 280, 115))
    parts.append(arrow(rng, 460, 115, 520, 115))
    parts.append(label(360, 190, "Prefer Agent over long-lived kubeconfig in CI variables", 13, "400"))
    write_pair("gitlab-agent", 740, 230, "\n".join(parts), [])


def diagram_gitlab_terraform():
    rng = random.Random(1012)
    parts = [label(390, 28, "Terraform in GitLab CI", 18)]
    chain = [
        (30, 80, "fmt/validate", "lint", "blue"),
        (180, 80, "plan", "MR artifact", "green"),
        (330, 80, "review", "approve", "orange"),
        (480, 80, "apply", "protected", "purple"),
        (630, 80, "state", "remote", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 130, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 130, y + 38, chain[i + 1][0], y + 38))
    write_pair("gitlab-terraform-pipeline", 800, 200, "\n".join(parts), [])


def diagram_gitlab_multicloud():
    rng = random.Random(1013)
    parts = [label(390, 28, "Multi-cloud from GitLab", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "OIDC / IAM", "short-lived", "gray"))
    parts.append(soft_box(rng, 40, 140, 160, 70, "AWS", "EKS · ECS", "orange"))
    parts.append(soft_box(rng, 230, 140, 160, 70, "Azure", "AKS", "blue"))
    parts.append(soft_box(rng, 420, 140, 160, 70, "GCP", "GKE · Run", "green"))
    parts.append(soft_box(rng, 610, 140, 160, 70, "Same CI", "jobs/rules", "purple"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("gitlab-multi-cloud", 810, 250, "\n".join(parts), [])


def diagram_gitlab_devsecops():
    rng = random.Random(1014)
    parts = [label(420, 28, "DevSecOps scanning", 18)]
    parts.append(soft_box(rng, 40, 80, 130, 70, "SAST", "code", "blue"))
    parts.append(soft_box(rng, 190, 80, 130, 70, "Secrets", "detect", "red"))
    parts.append(soft_box(rng, 340, 80, 140, 70, "Deps", "SCA", "green"))
    parts.append(soft_box(rng, 500, 80, 140, 70, "Container", "image", "orange"))
    parts.append(soft_box(rng, 660, 80, 130, 70, "SBOM", "license", "purple"))
    write_pair("gitlab-devsecops", 830, 200, "\n".join(parts), [])


def diagram_gitlab_testing():
    rng = random.Random(1015)
    parts = [label(360, 28, "Testing in pipelines", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Unit", "fast", "blue"))
    parts.append(soft_box(rng, 220, 80, 150, 70, "Integration", "services", "green"))
    parts.append(soft_box(rng, 400, 80, 150, 70, "E2E", "slower", "orange"))
    parts.append(soft_box(rng, 580, 80, 150, 70, "Reports", "JUnit", "purple"))
    write_pair("gitlab-testing", 770, 200, "\n".join(parts), [])


def diagram_gitlab_release():
    rng = random.Random(1016)
    parts = [label(360, 28, "Release management", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "SemVer tag", "v1.2.3", "blue"))
    parts.append(soft_box(rng, 240, 80, 180, 70, "Release job", "assets", "green"))
    parts.append(soft_box(rng, 460, 80, 180, 70, "Changelog", "notes", "orange"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 420, 115, 460, 115))
    write_pair("gitlab-release", 700, 200, "\n".join(parts), [])


def diagram_gitlab_production():
    rng = random.Random(1017)
    parts = [label(400, 28, "Production promotion", 18)]
    chain = [
        (20, 80, "dev", "auto", "blue"),
        (160, 80, "staging", "gated", "green"),
        (300, 80, "Approve", "manual", "orange"),
        (440, 80, "prod", "protected", "purple"),
        (580, 80, "Rollback", "prior", "red"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 120, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 120, y + 38, chain[i + 1][0], y + 38))
    write_pair("gitlab-production", 740, 200, "\n".join(parts), [])


def diagram_gitlab_monitoring():
    rng = random.Random(1018)
    parts = [label(390, 28, "Pipeline observability", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Job logs", "trace", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "Analytics", "duration", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "Runner metrics", "capacity", "orange"))
    parts.append(soft_box(rng, 610, 80, 160, 70, "Notify", "Slack/email", "purple"))
    write_pair("gitlab-monitoring", 810, 200, "\n".join(parts), [])


def diagram_gitlab_troubleshoot():
    rng = random.Random(1019)
    parts = [label(390, 28, "Troubleshooting ladder", 18)]
    chain = [
        (20, 80, "Job log", "error", "red"),
        (150, 80, "Runner", "tags/exec", "orange"),
        (280, 80, "Auth", "token/OIDC", "yellow"),
        (410, 80, "Cache", "stale", "green"),
        (540, 80, "Fix", "retry/rules", "blue"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("gitlab-troubleshooting", 700, 200, "\n".join(parts), [])


def diagram_gitlab_enterprise():
    rng = random.Random(1020)
    parts = [label(420, 28, "Enterprise GitLab platform", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Groups", "hierarchy", "blue"))
    parts.append(soft_box(rng, 230, 70, 160, 70, "Permissions", "roles", "green"))
    parts.append(soft_box(rng, 420, 70, 180, 70, "Compliance", "required CI", "orange"))
    parts.append(soft_box(rng, 640, 70, 160, 70, "Self-managed", "HA · backup", "purple"))
    write_pair("gitlab-enterprise-platform", 840, 180, "\n".join(parts), [])


def diagram_gitlab_gitops():
    rng = random.Random(1021)
    parts = [label(380, 28, "GitOps with GitLab", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "App repo", "CI build", "blue"))
    parts.append(soft_box(rng, 240, 80, 180, 70, "Manifest repo", "desired", "green"))
    parts.append(soft_box(rng, 460, 80, 180, 70, "Agent / Flux", "reconcile", "orange"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 420, 115, 460, 115))
    write_pair("gitlab-gitops", 700, 200, "\n".join(parts), [])



# --- GitHub Actions for Cloud & DevOps (polished Excalidraw) ---


def diagram_gha_architecture():
    rng = random.Random(1101)
    parts = [label(420, 28, "GitHub Actions architecture", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "GitHub", "events · PRs", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "Actions", "workflows", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "Runners", "hosted / self", "orange"))
    parts.append(soft_box(rng, 660, 70, 140, 70, "Targets", "cloud · k8s", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(420, 180, "YAML in .github/workflows drives the whole delivery loop", 13, "400"))
    write_pair("gha-architecture", 840, 220, "\n".join(parts), [])


def diagram_gha_lifecycle():
    rng = random.Random(1102)
    parts = [label(400, 28, "Workflow lifecycle", 18)]
    chain = [
        (20, 80, "Event", "push/PR", "blue"),
        (150, 80, "Workflow", "YAML", "green"),
        (280, 80, "Jobs", "parallel", "orange"),
        (410, 80, "Steps", "actions", "purple"),
        (540, 80, "Result", "checks", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("gha-workflow-lifecycle", 700, 200, "\n".join(parts), [])


def diagram_gha_basics():
    rng = random.Random(1103)
    parts = [label(400, 28, "Workflow building blocks", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "on:", "events", "blue"))
    parts.append(soft_box(rng, 200, 80, 140, 70, "jobs", "runners", "green"))
    parts.append(soft_box(rng, 360, 80, 140, 70, "steps", "run/uses", "orange"))
    parts.append(soft_box(rng, 520, 80, 140, 70, "actions", "reuse", "purple"))
    parts.append(soft_box(rng, 680, 80, 120, 70, "${{ }}", "expr", "teal"))
    write_pair("gha-basics", 840, 200, "\n".join(parts), [])


def diagram_gha_runners():
    rng = random.Random(1104)
    parts = [label(400, 28, "Runner architecture", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "GitHub", "job queue", "gray"))
    parts.append(soft_box(rng, 40, 140, 180, 70, "GitHub-hosted", "ubuntu/windows", "blue"))
    parts.append(soft_box(rng, 250, 140, 180, 70, "Self-hosted", "labels", "green"))
    parts.append(soft_box(rng, 460, 140, 160, 70, "Groups", "org policy", "orange"))
    parts.append(soft_box(rng, 650, 140, 140, 70, "Autoscaling", "pools", "purple"))
    for x in [130, 340, 540, 720]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("gha-runner-architecture", 830, 250, "\n".join(parts), [])


def diagram_gha_syntax():
    rng = random.Random(1105)
    parts = [label(400, 28, "Workflow syntax power tools", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "matrix", "OS/versions", "blue"))
    parts.append(soft_box(rng, 220, 80, 150, 70, "if:", "conditions", "green"))
    parts.append(soft_box(rng, 400, 80, 160, 70, "inputs/outputs", "wire jobs", "orange"))
    parts.append(soft_box(rng, 590, 80, 180, 70, "reusable", "workflow_call", "purple"))
    write_pair("gha-workflow-syntax", 810, 200, "\n".join(parts), [])


def diagram_gha_secrets():
    rng = random.Random(1106)
    parts = [label(400, 28, "Secrets, variables & OIDC", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Repo secrets", "encrypted", "blue"))
    parts.append(soft_box(rng, 230, 80, 160, 70, "Environments", "approvals", "green"))
    parts.append(soft_box(rng, 420, 80, 160, 70, "Org secrets", "shared", "orange"))
    parts.append(soft_box(rng, 610, 80, 160, 70, "OIDC", "cloud roles", "purple"))
    write_pair("gha-secrets-oidc", 810, 200, "\n".join(parts), [])


def diagram_gha_artifacts():
    rng = random.Random(1107)
    parts = [label(380, 28, "Artifacts & caching", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Job A", "build", "blue"))
    parts.append(soft_box(rng, 240, 80, 160, 70, "Artifact", "upload", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "Job B", "download", "orange"))
    parts.append(soft_box(rng, 240, 180, 160, 55, "Cache", "deps", "purple"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 400, 115, 440, 115))
    parts.append(arrow(rng, 320, 150, 320, 180))
    write_pair("gha-artifacts-cache", 660, 270, "\n".join(parts), [])


def diagram_gha_docker():
    rng = random.Random(1108)
    parts = [label(400, 28, "Docker build pipeline", 18)]
    chain = [
        (20, 80, "Checkout", "code", "blue"),
        (150, 80, "Buildx", "multi-arch", "green"),
        (280, 80, "Build", "image", "orange"),
        (410, 80, "GHCR", "push", "purple"),
        (540, 80, "Scan", "Trivy", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("gha-docker-pipeline", 700, 200, "\n".join(parts), [])


def diagram_gha_k8s():
    rng = random.Random(1109)
    parts = [label(400, 28, "Kubernetes deployment pipeline", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "CI image", "GHCR tag", "blue"))
    parts.append(soft_box(rng, 240, 70, 180, 70, "Deploy job", "kubectl/Helm", "green"))
    parts.append(soft_box(rng, 460, 70, 160, 70, "Cluster", "rollout", "orange"))
    parts.append(soft_box(rng, 660, 70, 140, 70, "Validate", "smoke", "purple"))
    for x1, x2 in [(200, 240), (420, 460), (620, 660)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("gha-kubernetes-pipeline", 840, 180, "\n".join(parts), [])


def diagram_gha_terraform():
    rng = random.Random(1110)
    parts = [label(390, 28, "Terraform pipeline", 18)]
    chain = [
        (20, 80, "fmt", "lint", "blue"),
        (140, 80, "init", "backend", "green"),
        (260, 80, "plan", "PR", "orange"),
        (380, 80, "review", "approve", "purple"),
        (500, 80, "apply", "main", "teal"),
        (620, 80, "state", "remote", "gray"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 100, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 100, y + 38, chain[i + 1][0], y + 38))
    write_pair("gha-terraform-pipeline", 760, 200, "\n".join(parts), [])


def diagram_gha_multicloud():
    rng = random.Random(1111)
    parts = [label(400, 28, "Multi-cloud with OIDC", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "GitHub OIDC", "id-token", "gray"))
    parts.append(soft_box(rng, 40, 140, 160, 70, "AWS", "IAM role", "orange"))
    parts.append(soft_box(rng, 230, 140, 160, 70, "Azure", "federated", "blue"))
    parts.append(soft_box(rng, 420, 140, 160, 70, "GCP", "WIF", "green"))
    parts.append(soft_box(rng, 610, 140, 160, 70, "Same workflow", "env jobs", "purple"))
    for x in [120, 310, 500, 690]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("gha-multi-cloud", 810, 250, "\n".join(parts), [])


def diagram_gha_security():
    rng = random.Random(1112)
    parts = [label(420, 28, "Security & supply chain", 18)]
    parts.append(soft_box(rng, 40, 80, 130, 70, "CodeQL", "SAST", "blue"))
    parts.append(soft_box(rng, 190, 80, 140, 70, "Deps", "review", "green"))
    parts.append(soft_box(rng, 350, 80, 140, 70, "Trivy", "images", "orange"))
    parts.append(soft_box(rng, 510, 80, 140, 70, "SBOM", "attest", "purple"))
    parts.append(soft_box(rng, 670, 80, 130, 70, "Secrets", "scanning", "red"))
    write_pair("gha-security", 840, 200, "\n".join(parts), [])


def diagram_gha_testing():
    rng = random.Random(1113)
    parts = [label(360, 28, "Testing in Actions", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Unit", "fast", "blue"))
    parts.append(soft_box(rng, 220, 80, 150, 70, "Integration", "services", "green"))
    parts.append(soft_box(rng, 400, 80, 150, 70, "E2E / smoke", "gates", "orange"))
    parts.append(soft_box(rng, 580, 80, 150, 70, "Parallel", "matrix", "purple"))
    write_pair("gha-testing", 770, 200, "\n".join(parts), [])


def diagram_gha_release():
    rng = random.Random(1114)
    parts = [label(380, 28, "Release pipeline", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "SemVer tag", "v1.2.3", "blue"))
    parts.append(soft_box(rng, 240, 80, 180, 70, "GitHub Release", "assets", "green"))
    parts.append(soft_box(rng, 460, 80, 180, 70, "Changelog", "notes", "orange"))
    parts.append(arrow(rng, 200, 115, 240, 115))
    parts.append(arrow(rng, 420, 115, 460, 115))
    write_pair("gha-release-pipeline", 700, 200, "\n".join(parts), [])


def diagram_gha_reusable():
    rng = random.Random(1115)
    parts = [label(400, 28, "Reusable components", 18)]
    parts.append(soft_box(rng, 40, 80, 180, 70, "Composite", "action.yml", "blue"))
    parts.append(soft_box(rng, 260, 80, 200, 70, "Reusable workflow", "workflow_call", "green"))
    parts.append(soft_box(rng, 500, 80, 180, 70, "Marketplace", "pinned SHA", "orange"))
    parts.append(soft_box(rng, 260, 180, 200, 55, "Internal org actions", "private", "purple"))
    write_pair("gha-reusable-components", 720, 270, "\n".join(parts), [])


def diagram_gha_production():
    rng = random.Random(1116)
    parts = [label(420, 28, "Enterprise CI/CD promotion", 18)]
    chain = [
        (20, 80, "dev", "auto", "blue"),
        (150, 80, "staging", "checks", "green"),
        (280, 80, "Approve", "env", "orange"),
        (410, 80, "prod", "protect", "purple"),
        (540, 80, "Canary", "observe", "teal"),
        (670, 80, "Rollback", "prior", "red"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("gha-production", 820, 200, "\n".join(parts), [])


def diagram_gha_troubleshoot():
    rng = random.Random(1117)
    parts = [label(400, 28, "Troubleshooting ladder", 18)]
    chain = [
        (20, 80, "Logs", "step fail", "red"),
        (150, 80, "Permissions", "GITHUB_TOKEN", "orange"),
        (280, 80, "Secrets/OIDC", "auth", "yellow"),
        (410, 80, "Runner", "labels", "green"),
        (540, 80, "Cache", "stale", "blue"),
        (670, 80, "Fix", "retry", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("gha-troubleshooting", 820, 200, "\n".join(parts), [])


def diagram_gha_enterprise():
    rng = random.Random(1118)
    parts = [label(420, 28, "Enterprise Actions platform", 18)]
    parts.append(soft_box(rng, 40, 70, 170, 70, "Org policies", "required workflows", "blue"))
    parts.append(soft_box(rng, 240, 70, 170, 70, "Runner groups", "isolation", "green"))
    parts.append(soft_box(rng, 440, 70, 170, 70, "Reusable library", "versioned", "orange"))
    parts.append(soft_box(rng, 640, 70, 160, 70, "Observability", "metrics", "purple"))
    write_pair("gha-enterprise-cicd", 840, 180, "\n".join(parts), [])



# --- AWS for Cloud & DevOps (polished Excalidraw) ---


def diagram_aws_global():
    rng = random.Random(1201)
    parts = [label(400, 28, "AWS global infrastructure", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Region", "geographic", "blue"))
    parts.append(soft_box(rng, 230, 70, 160, 70, "AZs", "isolated DCs", "green"))
    parts.append(soft_box(rng, 420, 70, 160, 70, "Edge", "CloudFront/PoPs", "orange"))
    parts.append(soft_box(rng, 610, 70, 160, 70, "Account", "boundary", "purple"))
    for x1, x2 in [(200, 230), (390, 420), (580, 610)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    parts.append(label(400, 180, "Shared responsibility: AWS secures the cloud; you secure in the cloud", 13, "400"))
    write_pair("aws-global-infrastructure", 810, 220, "\n".join(parts), [])


def diagram_aws_iam():
    rng = random.Random(1202)
    parts = [label(400, 28, "IAM identity model", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Principal", "user/role", "blue"))
    parts.append(soft_box(rng, 220, 80, 150, 70, "Policy", "Allow/Deny", "green"))
    parts.append(soft_box(rng, 400, 80, 150, 70, "STS", "temp creds", "orange"))
    parts.append(soft_box(rng, 580, 80, 180, 70, "Resource", "API action", "purple"))
    for x1, x2 in [(190, 220), (370, 400), (550, 580)]:
        parts.append(arrow(rng, x1, 115, x2, 115))
    write_pair("aws-iam-model", 800, 200, "\n".join(parts), [])


def diagram_aws_vpc():
    rng = random.Random(1203)
    parts = [label(400, 28, "VPC architecture", 18)]
    parts.append(soft_box(rng, 40, 50, 720, 40, "VPC · CIDR", "multi-AZ", "gray"))
    parts.append(soft_box(rng, 60, 110, 200, 70, "Public subnet", "ALB · bastion", "blue"))
    parts.append(soft_box(rng, 290, 110, 200, 70, "Private subnet", "app · data", "green"))
    parts.append(soft_box(rng, 520, 110, 200, 70, "Egress", "NAT / endpoints", "orange"))
    parts.append(soft_box(rng, 200, 210, 360, 55, "SG · NACL · routes · IGW", "controls", "purple"))
    write_pair("aws-vpc-architecture", 800, 300, "\n".join(parts), [])


def diagram_aws_three_tier():
    rng = random.Random(1204)
    parts = [label(380, 28, "Three-tier application", 18)]
    parts.append(soft_box(rng, 40, 80, 180, 70, "Presentation", "ALB · CDN", "blue"))
    parts.append(soft_box(rng, 260, 80, 180, 70, "Application", "ASG · ECS", "green"))
    parts.append(soft_box(rng, 480, 80, 180, 70, "Data", "RDS · cache", "orange"))
    parts.append(arrow(rng, 220, 115, 260, 115))
    parts.append(arrow(rng, 440, 115, 480, 115))
    write_pair("aws-three-tier", 700, 200, "\n".join(parts), [])


def diagram_aws_compute():
    rng = random.Random(1205)
    parts = [label(400, 28, "Compute building blocks", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "EC2", "VMs", "blue"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "ASG", "scale", "green"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "ALB/NLB", "traffic", "orange"))
    parts.append(soft_box(rng, 550, 80, 180, 70, "Launch template", "AMI · user data", "purple"))
    write_pair("aws-compute", 770, 200, "\n".join(parts), [])


def diagram_aws_storage():
    rng = random.Random(1206)
    parts = [label(380, 28, "Storage services", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "S3", "object", "blue"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "EBS", "block", "green"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "EFS/FSx", "file", "orange"))
    parts.append(soft_box(rng, 550, 80, 160, 70, "Lifecycle", "tiers · KMS", "purple"))
    write_pair("aws-storage", 750, 200, "\n".join(parts), [])


def diagram_aws_databases():
    rng = random.Random(1207)
    parts = [label(390, 28, "Databases on AWS", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "RDS", "SQL", "blue"))
    parts.append(soft_box(rng, 200, 80, 140, 70, "Aurora", "cloud SQL", "green"))
    parts.append(soft_box(rng, 360, 80, 150, 70, "DynamoDB", "NoSQL", "orange"))
    parts.append(soft_box(rng, 530, 80, 180, 70, "ElastiCache", "in-memory", "purple"))
    write_pair("aws-databases", 750, 200, "\n".join(parts), [])


def diagram_aws_eks():
    rng = random.Random(1208)
    parts = [label(400, 28, "EKS / ECS container platform", 18)]
    parts.append(soft_box(rng, 40, 70, 150, 70, "ECR", "images", "blue"))
    parts.append(soft_box(rng, 220, 70, 160, 70, "ECS / EKS", "orchestrate", "green"))
    parts.append(soft_box(rng, 410, 70, 160, 70, "Fargate/EC2", "compute", "orange"))
    parts.append(soft_box(rng, 600, 70, 160, 70, "ALB/Ingress", "traffic", "purple"))
    for x1, x2 in [(190, 220), (380, 410), (570, 600)]:
        parts.append(arrow(rng, x1, 105, x2, 105))
    write_pair("aws-eks-architecture", 800, 180, "\n".join(parts), [])


def diagram_aws_serverless():
    rng = random.Random(1209)
    parts = [label(400, 28, "Serverless architecture", 18)]
    parts.append(soft_box(rng, 40, 80, 140, 70, "API GW", "HTTP", "blue"))
    parts.append(soft_box(rng, 200, 80, 140, 70, "Lambda", "compute", "green"))
    parts.append(soft_box(rng, 360, 80, 140, 70, "SQS/SNS", "events", "orange"))
    parts.append(soft_box(rng, 520, 80, 160, 70, "EventBridge", "bus", "purple"))
    parts.append(soft_box(rng, 280, 180, 200, 55, "Step Functions", "orchestrate", "teal"))
    write_pair("aws-serverless", 720, 270, "\n".join(parts), [])


def diagram_aws_monitoring():
    rng = random.Random(1210)
    parts = [label(400, 28, "Observability on AWS", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "CloudWatch", "metrics/logs", "blue"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "CloudTrail", "API audit", "green"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "Config", "drift", "orange"))
    parts.append(soft_box(rng, 550, 80, 180, 70, "X-Ray / SSM", "trace · ops", "purple"))
    write_pair("aws-monitoring", 770, 200, "\n".join(parts), [])


def diagram_aws_security():
    rng = random.Random(1211)
    parts = [label(420, 28, "AWS security services", 18)]
    parts.append(soft_box(rng, 40, 80, 130, 70, "KMS", "keys", "blue"))
    parts.append(soft_box(rng, 190, 80, 140, 70, "Secrets", "SM / SSM", "green"))
    parts.append(soft_box(rng, 350, 80, 140, 70, "GuardDuty", "threats", "orange"))
    parts.append(soft_box(rng, 510, 80, 140, 70, "WAF/Shield", "edge", "purple"))
    parts.append(soft_box(rng, 670, 80, 130, 70, "Hub", "findings", "red"))
    write_pair("aws-security", 840, 200, "\n".join(parts), [])


def diagram_aws_iac():
    rng = random.Random(1212)
    parts = [label(380, 28, "IaC on AWS", 18)]
    parts.append(soft_box(rng, 40, 80, 160, 70, "Terraform", "multi-cloud", "blue"))
    parts.append(soft_box(rng, 230, 80, 180, 70, "CloudFormation", "native", "green"))
    parts.append(soft_box(rng, 440, 80, 160, 70, "CDK", "code → CFN", "orange"))
    parts.append(soft_box(rng, 230, 180, 200, 55, "Service Catalog", "approved", "purple"))
    write_pair("aws-iac", 660, 270, "\n".join(parts), [])


def diagram_aws_cicd():
    rng = random.Random(1213)
    parts = [label(400, 28, "CI/CD on AWS", 18)]
    chain = [
        (20, 80, "Source", "Git", "blue"),
        (150, 80, "Build", "CodeBuild", "green"),
        (280, 80, "Test", "gates", "orange"),
        (410, 80, "Deploy", "CodeDeploy", "purple"),
        (540, 80, "Promote", "envs", "teal"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("aws-cicd-pipeline", 700, 200, "\n".join(parts), [])


def diagram_aws_cost():
    rng = random.Random(1214)
    parts = [label(380, 28, "Cost optimisation loop", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Measure", "Cost Explorer", "blue"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "Budget", "alarms", "green"))
    parts.append(soft_box(rng, 380, 80, 160, 70, "Commit", "RI / SP", "orange"))
    parts.append(soft_box(rng, 560, 80, 160, 70, "Rightsize", "Spot · idle", "purple"))
    write_pair("aws-cost", 760, 200, "\n".join(parts), [])


def diagram_aws_dr():
    rng = random.Random(1215)
    parts = [label(400, 28, "Disaster recovery strategies", 18)]
    parts.append(soft_box(rng, 40, 80, 150, 70, "Backup", "AWS Backup", "blue"))
    parts.append(soft_box(rng, 210, 80, 150, 70, "Pilot light", "warm core", "green"))
    parts.append(soft_box(rng, 380, 80, 150, 70, "Warm standby", "scaled down", "orange"))
    parts.append(soft_box(rng, 550, 80, 180, 70, "Multi-region", "active/active", "purple"))
    write_pair("aws-disaster-recovery", 770, 200, "\n".join(parts), [])


def diagram_aws_landing():
    rng = random.Random(1216)
    parts = [label(400, 28, "Landing zone / multi-account", 18)]
    parts.append(soft_box(rng, 280, 50, 200, 55, "Organizations", "OU · SCP", "gray"))
    parts.append(soft_box(rng, 40, 140, 150, 70, "Security", "log archive", "blue"))
    parts.append(soft_box(rng, 210, 140, 150, 70, "Shared", "network", "green"))
    parts.append(soft_box(rng, 380, 140, 150, 70, "Workloads", "prod/dev", "orange"))
    parts.append(soft_box(rng, 550, 140, 180, 70, "Sandbox", "experiment", "purple"))
    for x in [115, 285, 455, 640]:
        parts.append(arrow(rng, 380, 105, x, 140))
    write_pair("aws-landing-zone", 770, 250, "\n".join(parts), [])


def diagram_aws_production():
    rng = random.Random(1217)
    parts = [label(420, 28, "Production AWS platform", 18)]
    parts.append(soft_box(rng, 40, 70, 160, 70, "Identity", "IAM IC", "blue"))
    parts.append(soft_box(rng, 220, 70, 160, 70, "Network", "hub/spoke", "green"))
    parts.append(soft_box(rng, 400, 70, 160, 70, "Workloads", "EKS/ECS", "orange"))
    parts.append(soft_box(rng, 580, 70, 180, 70, "Ops", "observe · DR", "purple"))
    write_pair("aws-production-platform", 800, 180, "\n".join(parts), [])


def diagram_aws_troubleshoot():
    rng = random.Random(1218)
    parts = [label(400, 28, "AWS troubleshooting ladder", 18)]
    chain = [
        (20, 80, "Symptom", "who/what", "red"),
        (150, 80, "IAM", "authz", "orange"),
        (280, 80, "Network", "SG/route", "yellow"),
        (410, 80, "Compute", "EC2/EKS", "green"),
        (540, 80, "Data", "S3/RDS", "blue"),
        (670, 80, "Fix", "verify", "purple"),
    ]
    for i, (x, y, t, s, c) in enumerate(chain):
        parts.append(soft_box(rng, x, y, 110, 75, t, s, c))
        if i < len(chain) - 1:
            parts.append(arrow(rng, x + 110, y + 38, chain[i + 1][0], y + 38))
    write_pair("aws-troubleshooting", 820, 200, "\n".join(parts), [])


def main():
    diagram_client_path()
    diagram_network_types()
    diagram_topologies()
    diagram_osi()
    diagram_tcpip()
    diagram_ip_addressing()
    diagram_subnetting()
    diagram_k8s_net()
    diagram_switching()
    diagram_routing()
    diagram_tcp_handshake()
    diagram_tcp_vs_udp()
    diagram_dns_resolution()
    diagram_dns_records()
    diagram_http_https()
    diagram_nat()
    diagram_firewalls()
    diagram_load_balancing()
    diagram_reverse_proxy()
    diagram_cloud_vpc()
    diagram_vpn()
    diagram_segmentation()
    diagram_observability()
    diagram_troubleshoot()
    diagram_packet_analysis()
    diagram_python_execution()
    diagram_python_venv()
    diagram_python_basics()
    diagram_python_control_flow()
    diagram_python_package_arch()
    diagram_python_functions()
    diagram_python_data_structures()
    diagram_python_file_handling()
    diagram_python_errors()
    diagram_python_oop()
    diagram_python_logging()
    diagram_python_config()
    diagram_python_cli()
    diagram_python_linux()
    diagram_python_rest()
    diagram_python_cloud()
    diagram_python_git()
    diagram_python_docker()
    diagram_python_k8s()
    diagram_python_terraform()
    diagram_python_ssh()
    diagram_python_concurrency()
    diagram_python_pytest()
    diagram_python_packaging()
    diagram_python_production()
    diagram_python_security()
    diagram_python_ai()
    diagram_python_troubleshoot()
    diagram_python_plugin()
    diagram_git_object_model()
    diagram_git_workflow()
    diagram_git_branching()
    diagram_git_merge()
    diagram_git_pr_lifecycle()
    diagram_git_actions()
    diagram_git_gitops()
    diagram_git_repo_arch()
    diagram_docker_architecture()
    diagram_docker_lifecycle()
    diagram_docker_layers()
    diagram_docker_networking()
    diagram_docker_volumes()
    diagram_docker_compose()
    diagram_docker_registry()
    diagram_docker_cicd()
    diagram_docker_production()
    diagram_k8s_architecture()
    diagram_k8s_control_plane()
    diagram_k8s_pod_lifecycle()
    diagram_k8s_service_networking()
    diagram_k8s_ingress_flow()
    diagram_k8s_storage()
    diagram_k8s_rbac()
    diagram_k8s_helm()
    diagram_k8s_gitops()
    diagram_k8s_production()
    diagram_helm_architecture()
    diagram_helm_chart_structure()
    diagram_helm_template_rendering()
    diagram_helm_release_lifecycle()
    diagram_helm_values_override()
    diagram_helm_dependencies()
    diagram_helm_oci_registry()
    diagram_helm_gitops()
    diagram_linux_architecture()
    diagram_linux_boot_process()
    diagram_linux_filesystem()
    diagram_linux_process_lifecycle()
    diagram_linux_storage()
    diagram_linux_networking()
    diagram_linux_systemd()
    diagram_linux_permissions()
    diagram_linux_containers()
    diagram_linux_cli()
    diagram_linux_text()
    diagram_linux_ssh()
    diagram_linux_packages()
    diagram_linux_scheduling()
    diagram_linux_logging()
    diagram_linux_monitoring()
    diagram_linux_security()
    diagram_linux_troubleshooting()
    diagram_linux_backup()
    diagram_linux_production()
    diagram_shell_execution()
    diagram_shell_lifecycle()
    diagram_shell_variables()
    diagram_shell_io()
    diagram_shell_control()
    diagram_shell_loops()
    diagram_shell_functions()
    diagram_shell_arrays()
    diagram_shell_files()
    diagram_shell_text()
    diagram_shell_process()
    diagram_shell_pipeline()
    diagram_shell_cron()
    diagram_shell_json()
    diagram_shell_errors()
    diagram_shell_automation()
    diagram_shell_troubleshooting()
    diagram_terraform_workflow()
    diagram_terraform_architecture()
    diagram_terraform_cli()
    diagram_terraform_hcl()
    diagram_terraform_providers()
    diagram_terraform_resources()
    diagram_terraform_variables()
    diagram_terraform_state()
    diagram_terraform_remote()
    diagram_terraform_modules()
    diagram_terraform_expressions()
    diagram_terraform_data()
    diagram_terraform_workspaces()
    diagram_terraform_cloud()
    diagram_terraform_testing()
    diagram_terraform_security()
    diagram_terraform_cicd()
    diagram_terraform_multicloud()
    diagram_terraform_kubernetes()
    diagram_terraform_production()
    diagram_terraform_troubleshoot()
    diagram_gitlab_architecture()
    diagram_gitlab_pipeline_flow()
    diagram_gitlab_runners()
    diagram_gitlab_projects()
    diagram_gitlab_syntax()
    diagram_gitlab_parent_child()
    diagram_gitlab_secrets()
    diagram_gitlab_artifacts()
    diagram_gitlab_docker()
    diagram_gitlab_k8s()
    diagram_gitlab_agent()
    diagram_gitlab_terraform()
    diagram_gitlab_multicloud()
    diagram_gitlab_devsecops()
    diagram_gitlab_testing()
    diagram_gitlab_release()
    diagram_gitlab_production()
    diagram_gitlab_monitoring()
    diagram_gitlab_troubleshoot()
    diagram_gitlab_enterprise()
    diagram_gitlab_gitops()
    diagram_gha_architecture()
    diagram_gha_lifecycle()
    diagram_gha_basics()
    diagram_gha_runners()
    diagram_gha_syntax()
    diagram_gha_secrets()
    diagram_gha_artifacts()
    diagram_gha_docker()
    diagram_gha_k8s()
    diagram_gha_terraform()
    diagram_gha_multicloud()
    diagram_gha_security()
    diagram_gha_testing()
    diagram_gha_release()
    diagram_gha_reusable()
    diagram_gha_production()
    diagram_gha_troubleshoot()
    diagram_gha_enterprise()
    diagram_aws_global()
    diagram_aws_iam()
    diagram_aws_vpc()
    diagram_aws_three_tier()
    diagram_aws_compute()
    diagram_aws_storage()
    diagram_aws_databases()
    diagram_aws_eks()
    diagram_aws_serverless()
    diagram_aws_monitoring()
    diagram_aws_security()
    diagram_aws_iac()
    diagram_aws_cicd()
    diagram_aws_cost()
    diagram_aws_dr()
    diagram_aws_landing()
    diagram_aws_production()
    diagram_aws_troubleshoot()
    print(f"output: {OUT}")


if __name__ == "__main__":
    main()
