#!/usr/bin/env python3
"""Generate Linux Module 7 tutorials (advanced servers)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINUX = ROOT / "docs" / "linux"


def write(slug: str, content: str) -> None:
    path = LINUX / f"{slug}.md"
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({len(content)} bytes)")


def main() -> None:
    # nginx — content loaded from companion files if present; else inline below
    write(
        "nginx-web-server-and-reverse-proxy",
        (ROOT / "scripts" / "_m7_nginx.md").read_text(encoding="utf-8")
        if (ROOT / "scripts" / "_m7_nginx.md").exists()
        else NGINX,
    )
    write(
        "tls-certificates-on-linux-servers",
        (ROOT / "scripts" / "_m7_tls.md").read_text(encoding="utf-8")
        if (ROOT / "scripts" / "_m7_tls.md").exists()
        else TLS,
    )
    write(
        "server-storage-lvm-and-fstab",
        (ROOT / "scripts" / "_m7_lvm.md").read_text(encoding="utf-8")
        if (ROOT / "scripts" / "_m7_lvm.md").exists()
        else LVM,
    )
    write(
        "backup-restore-and-recovery-drills",
        (ROOT / "scripts" / "_m7_backup.md").read_text(encoding="utf-8")
        if (ROOT / "scripts" / "_m7_backup.md").exists()
        else BACKUP,
    )


NGINX = r'''---
title: "nginx Web Server and Reverse Proxy"
description: "Install and configure nginx as a static web server and reverse proxy to a localhost app on Ubuntu."
difficulty: advanced
estimated_time: "65 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - nginx
  - reverse-proxy
  - servers
comments: false
---

# nginx Web Server and Reverse Proxy

## Overview

Most Linux app servers do not expose application ports publicly. **nginx** terminates HTTP at the edge, serves static assets efficiently, and **reverse-proxies** dynamic traffic to an upstream process bound to `127.0.0.1`. That pattern is the same mental model you will later see with Ingress and load balancers — first learn it on a single Ubuntu host.

This tutorial installs nginx, publishes a static site, runs a tiny upstream on localhost, and configures `proxy_pass` with log inspection and a deliberate 502 drill.

This is **Tutorial 22** in **Module 7: Advanced Linux Servers**.

## Prerequisites

- Complete [Linux Server Baseline and Lifecycle](linux-server-baseline-and-lifecycle.md)
- Complete [Linux Networking Essentials](linux-networking-essentials.md) (listeners / bind addresses)
- Ubuntu 22.04+ with `sudo`
- Port 80 free on the lab VM (or adjust)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Install and enable nginx on Ubuntu
- [ ] Serve a static site from `/var/www`
- [ ] Reverse-proxy to an upstream on `127.0.0.1`
- [ ] Manage site configs via `sites-available` / `sites-enabled`
- [ ] Validate with `nginx -t`, `curl`, and access/error logs

## Architecture

Clients hit nginx on port 80; nginx proxies to an app listening only on localhost.

![Architecture diagram for nginx Web Server and Reverse Proxy](../assets/images/nginx-web-server-and-reverse-proxy.svg)

## Theory

### Why nginx in front?

| Concern | Direct app on :8080 public | nginx edge |
|---------|----------------------------|------------|
| TLS | App must implement | Terminate at nginx (next tutorial) |
| Static files | Waste app workers | Served efficiently by nginx |
| Buffering / timeouts | Ad hoc | Central `proxy_*` knobs |
| Exposure | App bind mistakes | App stays on 127.0.0.1 |

### Config layout (Debian/Ubuntu)

| Path | Role |
|------|------|
| `/etc/nginx/nginx.conf` | Global settings, includes |
| `/etc/nginx/sites-available/` | Available virtual hosts |
| `/etc/nginx/sites-enabled/` | Symlinks to enabled sites |
| `/var/log/nginx/access.log` | Access log |
| `/var/log/nginx/error.log` | Error log |

Test config before reload: `sudo nginx -t` then `sudo systemctl reload nginx`.

### Reverse proxy essentials

```nginx
location /api/ {
    proxy_pass http://127.0.0.1:18080/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Upstream must be reachable **from the nginx host**. If the app binds `127.0.0.1` only, remote clients never touch it directly — that is intentional.

### Health and failure modes

- **502 Bad Gateway** — upstream down or wrong `proxy_pass`
- **Connection refused** to :80 — nginx not listening / firewall
- **404** — wrong `root` or location

Always compare `curl http://127.0.0.1/` (edge) vs `curl http://127.0.0.1:18080/` (upstream).

## Hands-on Lab

### Step 1 – Install nginx

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable --now nginx
systemctl is-active nginx
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1/
```

**Expected output:** `active` and HTTP `200` for the default welcome page.

### Step 2 – Static site

```bash
sudo mkdir -p /var/www/rebash-static
echo '<h1>REBASH static</h1>' | sudo tee /var/www/rebash-static/index.html
sudo tee /etc/nginx/sites-available/rebash-static << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    root /var/www/rebash-static;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
sudo rm -f /etc/nginx/sites-enabled/default
sudo ln -sf /etc/nginx/sites-available/rebash-static /etc/nginx/sites-enabled/rebash-static
sudo nginx -t && sudo systemctl reload nginx
curl -sS http://127.0.0.1/ | head -5
```

**Expected output:** Config OK; HTML contains `REBASH static`.

### Step 3 – Local upstream app

```bash
python3 - <<'PY' >/tmp/rebash-upstream.log 2>&1 &
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"service":"rebash-upstream","ok":true}\n'
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        return
HTTPServer(('127.0.0.1', 18080), H).serve_forever()
PY
echo $! > /tmp/rebash-upstream.pid
sleep 1
curl -sS http://127.0.0.1:18080/
ss -tln | grep 18080
```

**Expected output:** JSON OK; listener on `127.0.0.1:18080`.

### Step 4 – Reverse proxy location

```bash
sudo tee /etc/nginx/sites-available/rebash-static << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    root /var/www/rebash-static;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:18080/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
sudo nginx -t && sudo systemctl reload nginx
curl -sS http://127.0.0.1/api/
```

**Expected output:** `/api/` returns upstream JSON.

### Step 5 – Logs

```bash
sudo tail -n 5 /var/log/nginx/access.log
sudo tail -n 5 /var/log/nginx/error.log || true
```

**Expected output:** Access lines for `/` and `/api/`; error log quiet on success.

### Step 6 – Induce and fix a 502

```bash
kill "$(cat /tmp/rebash-upstream.pid)" 2>/dev/null || true
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1/api/ || true
python3 - <<'PY' >/tmp/rebash-upstream.log 2>&1 &
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b'{"ok":true}\n')
    def log_message(self, *a):
        return
HTTPServer(('127.0.0.1', 18080), H).serve_forever()
PY
echo $! > /tmp/rebash-upstream.pid
sleep 1
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1/api/
```

**Expected output:** Failure while upstream dead; `200` after restart.

### Step 7 – Cleanup upstream process

```bash
kill "$(cat /tmp/rebash-upstream.pid)" 2>/dev/null || true
rm -f /tmp/rebash-upstream.pid /tmp/rebash-upstream.log
```

## Validation

| Check | Pass criteria |
|-------|----------------|
| nginx active | `systemctl is-active nginx` → active |
| Static | `GET /` returns REBASH static |
| Proxy | `GET /api/` returns upstream when running |
| Config | `nginx -t` succeeds |

## Code Walkthrough

| Command / path | Description |
|----------------|-------------|
| `nginx -t` | Validate configuration syntax |
| `sites-available` / `sites-enabled` | Enable virtual hosts via symlink |
| `proxy_pass` | Forward to upstream URL |
| `/var/log/nginx/*` | Access and error diagnostics |

## Code Examples

```bash
sudo ss -tulpn | grep nginx
sudo nginx -T 2>/dev/null | grep -E 'listen |server_name |proxy_pass' | head -40
```

## Security Considerations

Keep upstreams on localhost. Do not expose `:18080` via firewall. Set sensible `client_max_body_size`, hide version (`server_tokens off`), and move to TLS in the next tutorial before production traffic.

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| App on `0.0.0.0:18080` | Bypasses nginx controls | Bind `127.0.0.1` |
| Wrong `proxy_pass` slash | Broken upstream paths | Match location slash rules |
| Reload without `nginx -t` | Outage | Always test then reload |
| Leaving default site | Confusing vhost selection | Explicit default_server |

## Best Practices

1. One site file per application
2. Reload for config changes when possible
3. Health-check upstreams before public exposure
4. Document the bind matrix: edge vs localhost ports
5. Ship access logs to your collector in production

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| 502 | Upstream down / wrong port | Start app; fix `proxy_pass` |
| 404 on static | Wrong `root` | Fix path and permissions |
| Permission denied | Root dir mode | Adjust ownership carefully |
| Port 80 in use | Another process | `ss -tulpn \| grep :80` |

## Summary

You placed nginx at the HTTP edge, served static content, and proxied to a localhost upstream — the core Linux app-server pattern before TLS and containers.

## Interview Questions

**Q1 — Why reverse-proxy instead of exposing the app port?**

*Sample answer:* Centralise TLS, static content, buffering, and exposure control; keep the app on localhost.

**Q2 — What usually causes nginx 502?**

*Sample answer:* Upstream not listening, crashed workers, or incorrect `proxy_pass` host/port.

**Q3 — Difference between restart and reload?**

*Sample answer:* Reload applies config with less disruption; restart drops connections.

**Q4 — How do you debug which server block is used?**

*Sample answer:* `nginx -T`, check `server_name`/`default_server`, test with `curl -H 'Host: ...'`.

**Q5 — Where should the app listen in this design?**

*Sample answer:* `127.0.0.1` on a private port; only nginx listens publicly on 80/443.

## Related Tutorials

- Previous: [Linux Server Baseline and Lifecycle](linux-server-baseline-and-lifecycle.md)
- Next: [TLS Certificates on Linux Servers](tls-certificates-on-linux-servers.md)
- [Linux Networking Essentials](linux-networking-essentials.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)
- [Docker](../docker/index.md)

## References

1. [nginx Beginner’s Guide](https://nginx.org/en/docs/beginners_guide.html)
2. [ngx_http_proxy_module](https://nginx.org/en/docs/http/ngx_http_proxy_module.html)
3. [Ubuntu nginx docs](https://ubuntu.com/server/docs/web-servers-nginx)
'''

TLS = r'''---
title: "TLS Certificates on Linux Servers"
description: "Terminate HTTPS on nginx with OpenSSL lab certificates, verify expiry, and understand the Let’s Encrypt production path."
difficulty: advanced
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - tls
  - nginx
  - certificates
  - servers
comments: false
---

# TLS Certificates on Linux Servers

## Overview

HTTP on port 80 is insufficient for credentials and modern browsers. **TLS** wraps HTTP so clients authenticate the server and encrypt the session. On Linux app servers, nginx typically **terminates TLS** and talks HTTP to localhost upstreams.

This tutorial builds a self-signed certificate for lab use, configures nginx on 443, verifies expiry with OpenSSL, and contrasts the Let’s Encrypt/certbot path used in production.

This is **Tutorial 23** in **Module 7: Advanced Linux Servers**.

## Prerequisites

- Complete [nginx Web Server and Reverse Proxy](nginx-web-server-and-reverse-proxy.md)
- nginx installed and running
- `openssl` available

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain certificate, private key, and trust chain roles
- [ ] Generate a self-signed cert/key pair for lab HTTPS
- [ ] Configure nginx `ssl_certificate` / `ssl_certificate_key`
- [ ] Check notAfter expiry dates and diagnose common TLS failures
- [ ] Describe how certbot/Let’s Encrypt differs from self-signed labs

## Architecture

Clients connect with HTTPS to nginx; certificate and key stay on the edge; upstream remains HTTP on localhost.

![Architecture diagram for TLS Certificates on Linux Servers](../assets/images/tls-certificates-on-linux-servers.svg)

## Theory

### Trust model

1. Server presents an X.509 certificate during the TLS handshake
2. Client checks signature chain to a trusted CA
3. Client verifies hostname (SAN/CN) and validity dates
4. Encrypted application data follows

**Self-signed** certificates trigger browser warnings — fine for labs; not for public production trust.

### Files on disk

| Artefact | Permissions | Notes |
|----------|-------------|-------|
| Private key | `640`/`600` | Never commit; never world-readable |
| Certificate | `644` | Public |
| Full chain | Cert + intermediates | Required for public CAs |

### Let’s Encrypt / certbot

Production hosts with public DNS use ACME challenges. Pure localhost VMs cannot complete HTTP-01 — use self-signed or an internal CA for labs.

### Expiry monitoring

Track `notAfter` and alert before expiry. Clock skew causes “not yet valid” failures.

## Hands-on Lab

### Step 1 – Create key and certificate

```bash
sudo mkdir -p /etc/nginx/ssl
sudo openssl req -x509 -nodes -newkey rsa:2048 -days 30 \
  -keyout /etc/nginx/ssl/lab.key \
  -out /etc/nginx/ssl/lab.crt \
  -subj "/CN=lab.rebash.local"
sudo chmod 640 /etc/nginx/ssl/lab.key
sudo chmod 644 /etc/nginx/ssl/lab.crt
sudo openssl x509 -in /etc/nginx/ssl/lab.crt -noout -subject -dates
```

**Expected output:** CN=`lab.rebash.local`; validity dates spanning ~30 days.

### Step 2 – HTTPS server block

```bash
sudo mkdir -p /var/www/rebash-static
echo '<h1>REBASH TLS</h1>' | sudo tee /var/www/rebash-static/index.html
sudo tee /etc/nginx/sites-available/rebash-tls << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;
    ssl_certificate     /etc/nginx/ssl/lab.crt;
    ssl_certificate_key /etc/nginx/ssl/lab.key;
    root /var/www/rebash-static;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/rebash-tls /etc/nginx/sites-enabled/rebash-tls
sudo rm -f /etc/nginx/sites-enabled/rebash-static /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
```

**Expected output:** `nginx -t` OK; reload succeeds.

### Step 3 – Curl HTTPS

```bash
curl -k -sS https://127.0.0.1/ | head -5
curl -k -sS -o /dev/null -w "%{http_code}\n" https://127.0.0.1/
echo | openssl s_client -connect 127.0.0.1:443 -servername lab.rebash.local 2>/dev/null \
  | openssl x509 -noout -dates
```

**Expected output:** HTML content; HTTP 200; certificate dates printed.

### Step 4 – Redirect check

```bash
curl -k -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1/
```

**Expected output:** `301` redirect to HTTPS.

### Step 5 – Certbot awareness

```bash
cat << 'EOF'
Production sketch (needs public DNS):
  sudo apt install -y certbot python3-certbot-nginx
  sudo certbot --nginx -d example.com
  sudo certbot renew --dry-run
EOF
```

**Expected output:** Reminder text only — do not force ACME on localhost.

## Validation

| Check | Pass criteria |
|-------|----------------|
| Key perms | Private key not world-readable |
| HTTPS | `curl -k https://127.0.0.1/` → 200 |
| Dates | Future notAfter |
| Config | `nginx -t` clean |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `openssl req -x509` | Create self-signed certificate |
| `openssl x509 -dates` | Show validity window |
| `openssl s_client` | Inspect live handshake |
| `ssl_certificate` | nginx public cert path |

## Code Examples

```bash
openssl x509 -in /etc/nginx/ssl/lab.crt -noout -enddate
openssl x509 -in /etc/nginx/ssl/lab.crt -noout -fingerprint -sha256
```

## Security Considerations

Protect private keys; prefer automated public CA issuance in production; never email keys; rotate on compromise; enable HSTS only when HTTPS is stable.

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| World-readable key | Trivial theft | Restrict mode/ownership |
| Hostname mismatch | Client errors | Match SAN/CN to URL |
| Expired cert | Outage | Monitor and renew |
| Missing chain | Mobile clients fail | Install fullchain |

## Best Practices

1. Automate renewal and alert on failure
2. Separate lab and production certificates
3. Keep TLS config in version control without private keys
4. Test with real clients, not only `curl -k`
5. Fix clock sync before chasing TLS ghosts

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| CERT_AUTHORITY_INVALID | Self-signed | Expected in lab |
| certificate has expired | notAfter passed | Reissue |
| key values mismatch | Mixed pair | Regenerate matching pair |
| Mixed content | HTTP assets | Serve via HTTPS |

## Summary

You terminated TLS on nginx with a lab certificate and learned how production ACME differs. Next: durable storage with LVM.

## Interview Questions

**Q1 — Where should TLS terminate on a typical Linux app VM?**

*Sample answer:* At the reverse proxy (nginx); keep upstream HTTP on localhost.

**Q2 — What does a self-signed certificate prove?**

*Sample answer:* Encryption yes; public trust no.

**Q3 — How do you check certificate expiry on disk?**

*Sample answer:* `openssl x509 -in file -noout -enddate`.

**Q4 — Why might TLS fail after a correct cert install?**

*Sample answer:* Clock skew, wrong key pair, missing chain, firewall, or hostname mismatch.

**Q5 — What is `certbot renew --dry-run` for?**

*Sample answer:* Prove renewal still works before expiry.

## Related Tutorials

- Previous: [nginx Web Server and Reverse Proxy](nginx-web-server-and-reverse-proxy.md)
- Next: [Server Storage — LVM and fstab](server-storage-lvm-and-fstab.md)
- [Linux Server Baseline and Lifecycle](linux-server-baseline-and-lifecycle.md)
- [Linux Security Hardening Basics](linux-security-hardening-basics.md)

## References

1. [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
2. [OpenSSL x509(1)](https://www.openssl.org/docs/manmaster/man1/openssl-x509.html)
3. [Certbot documentation](https://certbot.eff.org/)
'''

LVM = r'''---
title: "Server Storage — LVM and fstab"
description: "Create and extend LVM volumes on Ubuntu, mount with UUID-based fstab entries, and recover from mount failures."
difficulty: advanced
estimated_time: "65 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - lvm
  - storage
  - fstab
  - servers
comments: false
---

# Server Storage — LVM and fstab

## Overview

App servers outgrow their root disk. **LVM** (Logical Volume Manager) lets you pool disks, grow filesystems online, and keep mount configuration durable via **`/etc/fstab`**. Mistakes here cause boot failures — so labs use a **file-backed loop device** instead of risking the system disk.

This tutorial creates a PV/VG/LV, formats and mounts it, adds a UUID fstab entry, extends the volume, and cleans up safely.

This is **Tutorial 24** in **Module 7: Advanced Linux Servers**.

## Prerequisites

- Complete [Disk and Filesystem Management](disk-and-filesystem-management.md)
- `sudo` on Ubuntu with `lvm2` packages available
- ~1 GB free under `/var/tmp` for the loop file

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain PV, VG, and LV roles
- [ ] Create an LVM stack on a loop-backed disk for safe practice
- [ ] Mount by UUID and persist via `/etc/fstab`
- [ ] Extend a logical volume and filesystem
- [ ] Recover from a bad fstab entry without panic

## Architecture

Physical (or loop) disk → PV → VG → LV → filesystem → fstab UUID mount.

![Architecture diagram for Server Storage — LVM and fstab](../assets/images/server-storage-lvm-and-fstab.svg)

## Theory

### LVM layers

| Layer | Object | Tools |
|-------|--------|-------|
| Physical Volume | Disk/partition | `pvcreate`, `pvs` |
| Volume Group | Pool of PVs | `vgcreate`, `vgs` |
| Logical Volume | Allocated slice | `lvcreate`, `lvs` |

Extend by adding free extents to the LV, then growing the filesystem (`resize2fs` for ext4).

### fstab essentials

Columns: device, mount point, type, options, dump, pass.

Prefer **UUID=** over `/dev/sdX` names that can reorder. Use `nofail` or `x-systemd.device-timeout=` carefully on non-critical mounts so a missing disk does not block boot forever.

### Boot failure pattern

A typo in fstab can drop you to emergency mode. Fix from rescue with `mount -o remount,rw /` and edit fstab, or comment the bad line.

## Hands-on Lab

### Step 1 – Install LVM tools and create loop file

```bash
sudo apt update
sudo apt install -y lvm2
sudo mkdir -p /var/tmp/rebash-lvm
sudo fallocate -l 1G /var/tmp/rebash-lvm/disk.img
sudo losetup -fP /var/tmp/rebash-lvm/disk.img
LOOP=$(losetup -j /var/tmp/rebash-lvm/disk.img | cut -d: -f1)
echo "LOOP=$LOOP"
```

**Expected output:** A `/dev/loopN` path printed.

### Step 2 – PV, VG, LV

```bash
LOOP=$(losetup -j /var/tmp/rebash-lvm/disk.img | cut -d: -f1)
sudo pvcreate "$LOOP"
sudo vgcreate rebash_vg "$LOOP"
sudo lvcreate -n data_lv -L 512M rebash_vg
sudo lvs
sudo vgs
```

**Expected output:** `data_lv` in `rebash_vg` with ~512 MiB.

### Step 3 – Filesystem and mount

```bash
sudo mkfs.ext4 /dev/rebash_vg/data_lv
sudo mkdir -p /mnt/rebash-data
sudo mount /dev/rebash_vg/data_lv /mnt/rebash-data
df -h /mnt/rebash-data
echo 'hello-lvm' | sudo tee /mnt/rebash-data/proof.txt
```

**Expected output:** Mount shows ~512 MB; proof file written.

### Step 4 – UUID fstab entry

```bash
UUID=$(sudo blkid -s UUID -o value /dev/rebash_vg/data_lv)
echo "UUID=$UUID"
echo "UUID=$UUID /mnt/rebash-data ext4 defaults,nofail 0 2" | sudo tee /etc/fstab.rebash-lab-line
# Append once
grep -q "$UUID" /etc/fstab || echo "UUID=$UUID /mnt/rebash-data ext4 defaults,nofail 0 2" | sudo tee -a /etc/fstab
sudo findmnt --verify
sudo umount /mnt/rebash-data
sudo mount -a
cat /mnt/rebash-data/proof.txt
```

**Expected output:** `findmnt --verify` clean (or warnings understood); proof file readable after `mount -a`.

### Step 5 – Extend LV

```bash
sudo lvextend -L +200M /dev/rebash_vg/data_lv
sudo resize2fs /dev/rebash_vg/data_lv
df -h /mnt/rebash-data
```

**Expected output:** Capacity increases (~700 MB class); filesystem grows online.

### Step 6 – Cleanup (important)

```bash
sudo umount /mnt/rebash-data || true
# Remove lab fstab line
UUID=$(sudo blkid -s UUID -o value /dev/rebash_vg/data_lv 2>/dev/null || true)
if [ -n "$UUID" ]; then
  sudo sed -i "\|UUID=$UUID /mnt/rebash-data|d" /etc/fstab
fi
sudo lvremove -y /dev/rebash_vg/data_lv || true
sudo vgremove -y rebash_vg || true
LOOP=$(losetup -j /var/tmp/rebash-lvm/disk.img | cut -d: -f1 || true)
[ -n "$LOOP" ] && sudo pvremove -y "$LOOP" || true
[ -n "$LOOP" ] && sudo losetup -d "$LOOP" || true
sudo rm -rf /var/tmp/rebash-lvm
sudo findmnt --verify || true
```

**Expected output:** Lab VG/LV gone; fstab lab line removed; system mounts healthy.

## Validation

| Check | Pass criteria |
|-------|----------------|
| LVM created | `lvs` showed data_lv during lab |
| fstab | UUID mount worked with `mount -a` |
| Extend | `df` grew after `lvextend` + `resize2fs` |
| Cleanup | No leftover rebash_vg; fstab clean |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `pvcreate` / `vgcreate` / `lvcreate` | Build LVM stack |
| `mkfs.ext4` | Create filesystem on LV |
| `blkid` | Read UUID for fstab |
| `lvextend` + `resize2fs` | Grow volume and ext4 |

## Code Examples

```bash
sudo pvs; sudo vgs; sudo lvs
lsblk -f
```

## Security Considerations

Encrypt sensitive data volumes (LUKS) in production; restrict who can `lvremove`; backup before destructive LVM ops; never experiment on the root PV without snapshots/backups.

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| fstab device `/dev/sdX` | Name changes on reboot | Use UUID/LABEL |
| Forgetting resize2fs | LV grows, FS does not | Always grow FS |
| Leaving bad fstab | Emergency mode | `nofail` for data disks; test `mount -a` |
| Skipping cleanup | Ghost loop devices | Detach losetup; remove fstab lines |

## Best Practices

1. Practise on loop devices before touching cloud data disks
2. Document VG naming (`app_vg`, `db_vg`)
3. Monitor thin pools / free VG space
4. Align backup jobs with volume layout
5. Test restore of data on a separate LV

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Boot emergency | Bad fstab | Rescue, comment line, `systemctl default` |
| resize2fs fails | Unmounted ext needing different flow | Follow ext4 grow rules; check `man resize2fs` |
| PV not found | Loop detached | Recreate losetup before pv ops |
| Permission denied | Not root | Use sudo |

## Summary

You built, mounted, persisted, extended, and destroyed an LVM volume safely — the storage skill behind growing app servers.

## Interview Questions

**Q1 — Why LVM instead of a raw partition?**

*Sample answer:* Flexible growth, pooling multiple disks, snapshots (where used), and easier reorganisation.

**Q2 — Why UUID in fstab?**

*Sample answer:* Kernel device names can reorder; UUIDs stay stable.

**Q3 — Steps to grow an ext4 LV online?**

*Sample answer:* `lvextend` then `resize2fs` on the mounted filesystem (ext4 supports online growth).

**Q4 — How do you avoid boot hangs on optional data disks?**

*Sample answer:* `nofail` and systemd mount timeouts; keep root mounts strict.

**Q5 — What is a volume group?**

*Sample answer:* A pool of one or more PVs from which LVs are carved.

## Related Tutorials

- Previous: [TLS Certificates on Linux Servers](tls-certificates-on-linux-servers.md)
- Next: [Backup, Restore, and Recovery Drills](backup-restore-and-recovery-drills.md)
- [Disk and Filesystem Management](disk-and-filesystem-management.md)
- [Troubleshooting Linux Systems](troubleshooting-linux-systems.md)

## References

1. [LVM HOWTO](https://tldp.org/HOWTO/LVM-HOWTO/)
2. [fstab(5)](https://manpages.debian.org/fstab.5)
3. [Ubuntu LVM](https://ubuntu.com/server/docs/storage-lvm)
'''

BACKUP = r'''---
title: "Backup, Restore, and Recovery Drills"
description: "Design app-server backups with tar/rsync, verify checksums, and practise a restore drill that proves recovery."
difficulty: advanced
estimated_time: "55 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - backup
  - rsync
  - disaster-recovery
  - servers
comments: false
---

# Backup, Restore, and Recovery Drills

## Overview

A server without a tested restore is a hope strategy. Snapshots help, but **application-consistent backups** of `/etc`, app data, and secrets-handling procedures are what get you through mistakes, ransomware, and failed upgrades.

This tutorial inventories what to back up on a Linux app server, creates a tar/rsync backup with verification, destroys a copy on purpose, restores it, and records a minimal recovery checklist.

This is **Tutorial 25** in **Module 7: Advanced Linux Servers** — the Module 7 capstone skill.

## Prerequisites

- Complete Module 7 tutorials 21–24 (baseline through LVM)
- Complete [File Archiving and Compression](file-archiving-and-compression.md)
- Ubuntu lab VM with `sudo`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] List critical paths to back up on an app server
- [ ] Create verified tar and rsync backups
- [ ] Perform a restore drill with checksum proof
- [ ] Distinguish snapshots from backups
- [ ] Write a short recovery checklist for incidents

## Architecture

Source data → backup artefact → checksum verify → restore drill → proof.

![Architecture diagram for Backup, Restore, and Recovery Drills](../assets/images/backup-restore-and-recovery-drills.svg)

## Theory

### What to back up on an app server

| Path / item | Why |
|-------------|-----|
| `/etc` (selectively) | nginx, sshd, sudoers, fstab, ssl metadata |
| App unit files | `/etc/systemd/system/*.service` |
| Application data | `/var/lib/myapp`, uploads, SQLite, etc. |
| TLS material | Keys — encrypt at rest; restrict access |
| Package manifest | `dpkg --get-selections` for rebuild hints |

Do **not** blindly back up caches, `/tmp`, or multi-GB logs without rotation.

### Snapshot vs backup

| | Snapshot | Backup |
|--|----------|--------|
| Purpose | Fast rollback on same system | Copy elsewhere for disaster |
| Survives disk loss? | Often no | Yes if off-box |
| App consistency | Must freeze/flush | Same concern |

Use both: snapshots for operator mistakes; off-box backups for disk/region loss.

### Verify or it did not happen

Always store a checksum (`sha256sum`) and restore to a scratch directory periodically. Untested backups fail in incidents.

## Hands-on Lab

### Step 1 – Create sample app data

```bash
mkdir -p ~/rebash-app/{bin,data,config}
echo 'version=1' > ~/rebash-app/config/app.conf
echo 'user-data' > ~/rebash-app/data/state.txt
printf '%s\n' '#!/bin/sh' 'echo ok' > ~/rebash-app/bin/health.sh
chmod +x ~/rebash-app/bin/health.sh
# Fake /etc snippet copy for lab
mkdir -p ~/rebash-app/etc-snippet
cp /etc/hostname ~/rebash-app/etc-snippet/hostname
find ~/rebash-app -type f
```

**Expected output:** Config, data, and hostname snippet present.

### Step 2 – Tar backup with checksum

```bash
mkdir -p ~/rebash-backups
TS=$(date +%Y%m%d-%H%M%S)
BACKUP=~/rebash-backups/app-$TS.tar.gz
tar -C ~ -czf "$BACKUP" rebash-app
sha256sum "$BACKUP" | tee ~/rebash-backups/app-$TS.sha256
ls -lh "$BACKUP"
```

**Expected output:** `.tar.gz` and matching `.sha256` file.

### Step 3 – rsync copy

```bash
rsync -a --delete ~/rebash-app/ ~/rebash-backups/app-rsync/
find ~/rebash-backups/app-rsync -type f
```

**Expected output:** Mirror of app tree under `app-rsync`.

### Step 4 – Verify checksum and list tar

```bash
cd ~/rebash-backups
sha256sum -c app-$TS.sha256
tar -tzf "app-$TS.tar.gz" | head -20
```

**Expected output:** `OK` from sha256sum; tar lists `rebash-app/...` paths.

### Step 5 – Destroy and restore drill

```bash
rm -rf ~/rebash-app
test ! -d ~/rebash-app && echo 'app tree removed'
tar -C ~ -xzf ~/rebash-backups/app-$TS.tar.gz
cat ~/rebash-app/data/state.txt
~/rebash-app/bin/health.sh
```

**Expected output:** `user-data` restored; `health.sh` prints `ok`.

### Step 6 – Recovery checklist note

```bash
cat > ~/rebash-backups/RESTORE.md << 'EOF'
# App server restore checklist
1. Confirm incident / declare scope
2. Stop writers (systemctl stop myapp / nginx if needed)
3. Verify backup checksum
4. Restore to staging path first
5. Promote / fix permissions / restart units
6. Smoke test URLs and logs
7. Record timeline + improve backup job
EOF
cat ~/rebash-backups/RESTORE.md
```

**Expected output:** Checklist saved beside backups.

### Step 7 – Cleanup lab artefacts (optional keep backups)

```bash
# Keep ~/rebash-backups for your notes, or remove:
# rm -rf ~/rebash-app ~/rebash-backups
true
```

## Validation

| Check | Pass criteria |
|-------|----------------|
| Backup exists | tar.gz + sha256 present |
| Verify | `sha256sum -c` OK |
| Restore | state.txt and health.sh work after delete |
| Checklist | RESTORE.md written |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `tar -czf` | Create compressed archive |
| `sha256sum` | Integrity fingerprint |
| `rsync -a` | Incremental mirror |
| `tar -xzf` | Extract restore |

## Code Examples

```bash
# Daily-style rsync to a mounted backup disk (sketch)
# rsync -aHAX --delete /var/lib/myapp/ /mnt/backup/myapp/
# Prefer off-box copies for disaster scenarios
```

## Security Considerations

Encrypt backups that contain keys or PII; restrict backup share permissions; do not store production private keys in unencrypted tar on laptops; rotate credentials if a backup escapes.

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Never restoring | False confidence | Schedule drills |
| Backing up only root disk snapshot | App consistency / off-box gaps | App-aware + off-site |
| Absolute tar paths | Dangerous extracts | Prefer `-C` relative |
| No checksum | Silent corruption | sha256 + verify |

## Best Practices

1. 3-2-1 rule: copies, media types, off-site
2. Automate with systemd timers or cron; alert on failure
3. Restore to a scratch host monthly
4. Document RPO/RTO with stakeholders
5. Include package lists and infra-as-code pointers

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Checksum fail | Truncated copy | Re-run backup; check disk |
| Permission denied on restore | Ownership | Extract with sudo; fix chown |
| rsync deleted too much | `--delete` misuse | Dry-run first (`-n`) |
| Huge backups | Logs/cache included | Exclude lists |

## Summary

You produced a verified backup, destroyed data on purpose, restored it, and wrote a recovery checklist — the operational proof that Module 7 servers can survive mistakes.

## Interview Questions

**Q1 — Snapshot versus backup?**

*Sample answer:* Snapshots are fast local rollback; backups are durable copies that survive disk/site loss when stored off-box.

**Q2 — How do you know a backup is good?**

*Sample answer:* Checksums plus a successful restore drill to a non-production path.

**Q3 — What must be backed up on an nginx app VM?**

*Sample answer:* Site configs, TLS material (protected), unit files, app data, and enough OS config to rebuild.

**Q4 — Why is `--delete` on rsync dangerous?**

*Sample answer:* It mirrors removals — a bad source can wipe the backup target.

**Q5 — What is RPO?**

*Sample answer:* Recovery Point Objective — how much data you can afford to lose in time.

## Related Tutorials

- Previous: [Server Storage — LVM and fstab](server-storage-lvm-and-fstab.md)
- [File Archiving and Compression](file-archiving-and-compression.md)
- [Linux Security Hardening Basics](linux-security-hardening-basics.md)
- Lab: [Linux Production Incident Triage](../labs/linux-production-incident-triage.md)
- [Docker](../docker/index.md)

## References

1. [rsync(1)](https://download.samba.org/pub/rsync/rsync.html)
2. [GNU tar manual](https://www.gnu.org/software/tar/manual/)
3. [3-2-1 backup rule (industry practice)](https://www.veeam.com/blog/321-backup-rule.html)
'''

if __name__ == "__main__":
    main()
