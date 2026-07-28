    ---
    title: "Networking Cheat Sheet"
    description: "Quick-reference commands and patterns for the REBASH Academy Networking track."
    difficulty: beginner
    estimated_time: "10 min"
    author: Shaik Basha
    last_updated: "2026-07-28"
    category: cheatsheets
    tags:
      - cheatsheets
      - networking
    comments: false
    ---

    # Networking Cheat Sheet

    Scannable commands and patterns for the [Networking track](../networking/index.md). Prefer the full tutorials when you need *why*, not only *how*.

    ## Quick reference

    | Area | Commands / notes |
    |------|------------------|
    | Models | OSI vs TCP/IP layers; which headers live where |
| Addressing | CIDR math; private ranges; broadcast vs unicast |
| DNS | `dig +trace`; `dig A/AAAA/CNAME/MX`; TTL behaviour |
| Sockets | `ss -tulpn`; ephemeral ports; TIME_WAIT |
| HTTP | Methods, status codes, TLS handshake overview |
| Routing | `ip route`; default gateway; traceroute/mtr |
| Firewall | iptables/nftables / cloud SG mental model |
| LB / proxy | L4 vs L7; reverse proxy vs ingress |
| Capture | `tcpdump -ni eth0 port 443`; Wireshark follow stream |
| VPN | Tunnel vs transport; common split-tunnel pitfalls |

    ## Common mistakes

    - Copy-pasting without reading expected output
    - Skipping cleanup (leftover containers, state, or temp files)
    - Mixing production credentials into lab shells

    ## Related

    - Track: [Networking](../networking/index.md)
    - Start: [Networking introduction](../networking/introduction-to-networking.md)
    - Interview bank: [Networking interview prep](../interview/networking.md)
    - Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)
