---
title: "Lab — Linux App Server from Zero"
description: "Build a hardened Ubuntu app server end-to-end: baseline, systemd app, nginx reverse proxy, TLS, and a verified backup restore — with cleanup."
difficulty: advanced
estimated_time: "90 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - linux
  - nginx
  - tls
  - servers
comments: false
---

# Lab — Linux App Server from Zero

## Lab Overview

**Purpose:** Assemble production Linux skills into one production-shaped Ubuntu host (app + reverse proxy + TLS + backup).

**Scenario:** You must stand up an internal status API behind nginx with TLS (self-signed for the lab), then prove you can restore app data from backup.

**Expected outcome:** HTTPS returns the API through nginx, firewall only exposes intended ports, and a restore drill succeeds with checksum verification.

!!! tip "This is a lab, not a tutorial"
    Prefer evidence (`ss`, `curl`, `nginx -t`, checksums) over skipping ahead. Pair with the rewritten track modules below — nginx/TLS deep dives remain useful operational skills even when filenames change.

!!! note "Track alignment"
    Prefer these production modules for theory: [SSH Hardening and Firewalls](../linux/ssh-hardening-and-firewalls.md), [Production Linux Hardening and Performance](../linux/production-linux-hardening-and-performance.md), [Backup, Disaster Recovery, and Capacity](../linux/backup-disaster-recovery-and-capacity.md), [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md).

## Business Scenario

A platform team needs a **single Ubuntu VM** serving a small status API for demos. Containers come later — first you must prove bare-metal/VM fluency: hardening, reverse proxy, TLS, and backup discipline.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Apply a minimal server baseline and SSH/firewall posture
- [ ] Run an app on `127.0.0.1` under a simple process (or unit)
- [ ] Front it with nginx + self-signed TLS
- [ ] Complete a backup/restore proof
- [ ] Clean up lab certificates, sites, and processes

## Prerequisites

### Knowledge

- [SSH Hardening and Firewalls](../linux/ssh-hardening-and-firewalls.md)
- [Production Linux Hardening and Performance](../linux/production-linux-hardening-and-performance.md)
- [Backup, Disaster Recovery, and Capacity](../linux/backup-disaster-recovery-and-capacity.md)
- [systemd Services and journalctl](../linux/systemd-services-and-journalctl.md)
- [Package Management](../linux/package-management.md)
- [Users, Groups, and sudo](../linux/users-groups-and-sudo.md)
- Labs: [Firewall Hardening](linux-firewall-hardening-lab.md), [SSH Secure Access](linux-ssh-secure-access.md)

### Software

| Tool | Notes |
|------|--------|
| Ubuntu 22.04+ / 24.04 VM | systemd, apt, sudo |
| Console access | Avoid lockout during SSH/UFW changes |
| nginx, openssl | Installed in lab steps |

**Estimated cost:** £0 locally.

## Architecture

![Linux app server lab: baseline, harden, nginx+TLS+app, backup proof](../assets/images/lab-linux-app-server-from-zero.svg)

## Environment

Use a disposable VM you own. Do not harden shared production hosts with lab self-signed certs without change control.

## Initial State

Fresh or lightly used Ubuntu server. You will install packages and create lab paths under `/opt/rebash-lab` and `/etc/nginx`.

## Lab Tasks

### Task 1 — Baseline card

```bash
hostnamectl | head -5
timedatectl | grep -iE 'synchronized|NTP' || true
systemctl is-system-running || true
```

**Expected output:** Ubuntu identity; clock sync state known; system running/degraded understood.

### Task 2 — App on localhost

```bash
sudo mkdir -p /opt/rebash-lab/app
sudo tee /opt/rebash-lab/app/server.py >/dev/null <<'EOF'
#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"service":"rebash-lab","ok":true}\n'
        if self.path not in ("/", "/healthz", "/api", "/api/"):
            self.send_response(404); self.end_headers(); return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, *a): return
HTTPServer(("127.0.0.1", 18080), H).serve_forever()
EOF
sudo chmod +x /opt/rebash-lab/app/server.py
sudo python3 /opt/rebash-lab/app/server.py >/var/tmp/rebash-lab-app.log 2>&1 &
echo $! | sudo tee /var/tmp/rebash-lab-app.pid
sleep 1
curl -sS http://127.0.0.1:18080/healthz
ss -tln | grep 18080
```

**Expected output:** JSON OK; listen on `127.0.0.1:18080` only.

### Task 3 — nginx reverse proxy + TLS

```bash
sudo apt update
sudo apt install -y nginx openssl
sudo mkdir -p /etc/nginx/ssl /var/www/rebash-lab
echo '<h1>REBASH lab edge</h1>' | sudo tee /var/www/rebash-lab/index.html
sudo openssl req -x509 -nodes -newkey rsa:2048 -days 30 \
  -keyout /etc/nginx/ssl/rebash-lab.key \
  -out /etc/nginx/ssl/rebash-lab.crt \
  -subj "/CN=rebash-lab.local"
sudo chmod 640 /etc/nginx/ssl/rebash-lab.key
sudo tee /etc/nginx/sites-available/rebash-lab <<'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    ssl_certificate     /etc/nginx/ssl/rebash-lab.crt;
    ssl_certificate_key /etc/nginx/ssl/rebash-lab.key;
    root /var/www/rebash-lab;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
    location /api/ {
        proxy_pass http://127.0.0.1:18080/;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
sudo ln -sf /etc/nginx/sites-available/rebash-lab /etc/nginx/sites-enabled/rebash-lab
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl reload nginx
curl -k -sS https://127.0.0.1/ | head -3
curl -k -sS https://127.0.0.1/api/healthz
```

**Expected output:** Static HTML over HTTPS; API JSON via `/api/`.

### Task 4 — Firewall posture (UFW)

```bash
sudo apt install -y ufw
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status numbered
sudo ss -tuln | awk 'NR==1 || /:22 |:80 |:443 |:18080 /'
```

**Expected output:** UFW active with 22/80/443; app still on localhost only.

!!! warning "Keep a console session"
    Confirm SSH still works in a second session before enabling UFW on remote cloud VMs.

### Task 5 — Backup and restore proof

```bash
mkdir -p ~/rebash-lab-backups
echo 'lab-state=1' | sudo tee /opt/rebash-lab/app/state.txt
TS=$(date +%Y%m%d-%H%M%S)
tar -C /opt -czf ~/rebash-lab-backups/app-$TS.tar.gz rebash-lab
sha256sum ~/rebash-lab-backups/app-$TS.tar.gz | tee ~/rebash-lab-backups/app-$TS.sha256
sudo rm -f /opt/rebash-lab/app/state.txt
tar -C /opt -xzf ~/rebash-lab-backups/app-$TS.tar.gz
sudo cat /opt/rebash-lab/app/state.txt
sha256sum -c ~/rebash-lab-backups/app-$TS.sha256
```

**Expected output:** Checksum OK; `lab-state=1` restored.

## Validation

| Check | Pass criteria |
|-------|----------------|
| Upstream | `127.0.0.1:18080` healthy |
| HTTPS API | `curl -k https://127.0.0.1/api/healthz` → JSON |
| Exposure | `:18080` not on `0.0.0.0` |
| Backup | sha256 verify + restore worked |

## Troubleshooting

| Symptoms | Causes | Resolution | Verification |
|----------|--------|------------|--------------|
| 502 on /api | App dead | Restart python server | curl localhost:18080 |
| CERT errors | Self-signed | Use `curl -k` in lab | openssl s_client |
| UFW lockout | SSH not allowed | Console; `ufw allow OpenSSH` | ssh works |
| nginx -t fail | Typo in site | Fix and retest | nginx -t |

## Challenge Extensions

- Convert the Python process to a proper systemd unit
- Add fail2ban for sshd
- Issue a real cert with certbot on a public DNS name

## Cleanup

```bash
sudo kill "$(cat /var/tmp/rebash-lab-app.pid)" 2>/dev/null || true
sudo rm -f /var/tmp/rebash-lab-app.pid /var/tmp/rebash-lab-app.log
sudo rm -f /etc/nginx/sites-enabled/rebash-lab
sudo rm -f /etc/nginx/sites-available/rebash-lab
sudo rm -rf /etc/nginx/ssl/rebash-lab.* /var/www/rebash-lab /opt/rebash-lab
sudo nginx -t && sudo systemctl reload nginx || true
# Optional: sudo ufw disable  (only on disposable lab VMs)
rm -rf ~/rebash-lab-backups
```

## Production Discussion

Production adds: real CA certificates, systemd units, config management, off-box backups, monitoring, and change windows. This lab is the shape — not the full platform.

## Best Practices

- Localhost upstreams; public edge only 80/443/22
- `nginx -t` before every reload
- Prove restores, not only backups
- Console access before firewall/SSH experiments

## Common Mistakes

| Mistake | Why | Fix |
|---------|-----|-----|
| App on 0.0.0.0 | Bypass proxy | Bind 127.0.0.1 |
| No second SSH session | Lockout | Always keep console |
| Skipping checksum | Corrupt backup | sha256sum -c |

## Success Criteria

HTTPS API works through nginx, exposure matrix is correct, restore drill passed, cleanup done.

## Reflection Questions

1. Why is `:18080` on localhost essential?
2. What changes when you replace self-signed with Let’s Encrypt?
3. How would systemd improve Task 2?

## Interview Connection

Tell this build story in interviews. Continue with [Linux Interview Prep](../interview/linux.md).

## Related Tutorials

- Track: [Linux](../linux/index.md)
- [Production Linux Hardening and Performance](../linux/production-linux-hardening-and-performance.md)
- [Backup, Disaster Recovery, and Capacity](../linux/backup-disaster-recovery-and-capacity.md)
- [Linux Production Incident Triage](linux-production-incident-triage.md)
- Path: [Linux for Cloud & DevOps](../learning-paths/linux-for-cloud-devops.md)
- [Docker](../docker/index.md)

## References

1. [nginx docs](https://nginx.org/en/docs/)
2. [Ubuntu Server Guide](https://ubuntu.com/server/docs)
3. [UFW community help](https://help.ubuntu.com/community/UFW)
