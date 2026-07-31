---
title: "SSH Automation — Paramiko and Fabric"
description: "Automate remote hosts with Paramiko and Fabric — SSH keys, remote execution, SCP/SFTP, and safe defaults for DevOps Python."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 20 · SSH Automation"
career_paths:
  - devops-engineer
  - linux-administrator
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - paramiko
  - fabric
  - ssh
prerequisites:
  - python/infrastructure-automation-terraform
next:
  - python/concurrency-threads-asyncio-and-futures
related:
  - python/linux-automation-subprocess-and-psutil
  - networking/vpn-and-tunneling-basics
labs: []
projects: []
interview: interview/python
certifications:
  - PCAP
  - RHCSA
tags:
  - python
  - ssh
  - paramiko
  - fabric
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# SSH Automation — Paramiko and Fabric

## Overview

Understand Paramiko and Fabric for remote command execution and file transfer, prefer SSH keys over passwords, and practise patterns safely with a mock/dry-run path when you lack a lab host.

SSH is still how many fleets get bootstrap scripts and emergency fixes. Prefer **config management / cloud-init** for steady state; use Paramiko/Fabric for targeted remote exec. Never hard-code keys or passwords.

Complete prior automation modules first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 20 · SSH Automation** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Automation](linux-automation-subprocess-and-psutil.md)
- SSH client basics

### Recommended

- Optional lab VM with key-based SSH; otherwise use the dry-run lab path

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Contrast Paramiko vs Fabric  
- [ ] Describe key-based auth and `known_hosts` risks  
- [ ] Sketch remote exec and SCP/SFTP flows  
- [ ] Avoid password auth in automation  
- [ ] Gate destructive remote commands behind `--apply`

## Architecture

This topic’s control points and relationships are shown below.

![SSH automation](../assets/excalidraw/python-ssh-paramiko.svg)

## Theory

### What it is

Secure Shell (SSH) automation runs commands and transfers files on remote Linux hosts without an interactive terminal. **Paramiko** is the lower-level Python SSH library (connect, exec, SFTP). **Fabric** sits higher — tasks, `Connection.run()`, put/get — built on Paramiko/Invoke for multi-host scripts. Both use key-based auth and host-key verification the same way OpenSSH does.

### Why it matters

Cloud APIs do not cover every appliance, bastion jump, or legacy box. Fleet checks (`uname`, disk, service status), config pulls, and controlled restarts still travel over SSH. Doing that in Python beats unmaintainable expect scripts — if you treat host keys, allow-lists, and dry-run as first-class controls. A wrong host-key policy is a Man-in-the-Middle (MitM) invitation.

### How it works

Create an `SSHClient`, load `known_hosts`, set **`RejectPolicy`** for unknown keys (not `AutoAddPolicy` in production), then `connect` with username and key (agent or `key_filename` from the environment). Open a session channel to `exec_command`, or use SFTP for put/get. Fabric wraps the same flow in `@task` functions and host lists. Prefer Ed25519 keys; never commit private keys; disable password auth for service accounts. Validate remote paths before writes; avoid world-writable destinations.

```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.RejectPolicy())
# client.load_system_host_keys(); client.connect(...)
```

### Key concepts and comparisons

| Tool | Level | Best for |
|------|-------|----------|
| Paramiko | Low | Fine control, embedding in larger apps |
| Fabric | High | Multi-host task scripts |
| OpenSSH CLI via subprocess | External | One-liners; weaker structure |

| Action | Tutorial default |
|--------|------------------|
| `uname`, read files | Allowed in labs |
| `rm`, service restart | `--apply` + command allow-list |

### Common pitfalls

- `AutoAddPolicy` in production (accepts any host key).  
- Logging command lines that embed passwords.  
- Unbounded parallel SSH that trips fail2ban or MaxStartups.  
- Writing files to `/tmp` world-writable paths without ownership checks.  
- Skipping bastion/ProxyJump modelling so scripts only work on the flat lab network.

## Hands-on Lab

**Focus:** practise the core workflow for SSH Automation — Paramiko and Fabric

```bash
mkdir -p ~/rebash-python/module-20
cd ~/rebash-python/module-20

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'paramiko==3.5.1' 'fabric==3.2.2'
```

### Step 1 – Dry-run remote runner

```bash
cd ~/rebash-python/module-20
source .venv/bin/activate

cat > ssh_run.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shlex
import sys


ALLOWED = {"uname -s", "hostname", "uptime"}


def main() -> int:
    p = argparse.ArgumentParser(description="SSH command helper (lab)")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--user", default="lab")
    p.add_argument("--command", required=True)
    p.add_argument("--apply", action="store_true", help="actually open SSH")
    args = p.parse_args()
    if args.command not in ALLOWED:
        print(f"error: command not allow-listed: {args.command!r}", file=sys.stderr)
        return 2
    if not args.apply:
        print(f"DRY-RUN ssh {args.user}@{args.host} -- {args.command}")
        return 0
    try:
        import paramiko
    except ImportError:
        print("error: paramiko missing", file=sys.stderr)
        return 1
    print("error: live SSH not enabled in default lab — use a dedicated VM and keys", file=sys.stderr)
    print(f"hint: paramiko.SSHClient().connect({args.host!r}, username={args.user!r})", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python ssh_run.py --command "uname -s"
python ssh_run.py --command "rm -rf /" || true
```

### Step 2 – Fabric mental model

```bash
python - <<'PY'
print("Fabric: Connection(host).run('uname -s', hide=True)")
print("Batch: Group from fabric.group — fan-out with care")
PY
```

### Step 3 – Key hygiene checklist

Write `ssh-checklist.md`: agent forwarding off for automation, dedicated deploy keys, `RejectPolicy`, command allow-lists, timeouts.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-20/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **SSH Automation — Paramiko and Fabric** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "`AutoAddPolicy` in production (accepts any host key).  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Logging command lines that embed passwords.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode SSH Automation — Paramiko and Fabric changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Auth failure | Wrong key/user | `ssh -v`; check `authorized_keys` |
| Host key verify fail | First connect / rotation | Verify out-of-band; update known_hosts |
| Hang | No timeout | Set socket/command timeouts |

## Summary

- Paramiko = library; Fabric = task layer  
- Keys only; reject unknown hosts by default  
- Allow-list remote commands; dry-run first

## Interview Questions

1. How does **SSH Automation — Paramiko and Fabric** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Concurrency — Threads, asyncio, and Futures](concurrency-threads-asyncio-and-futures.md)

## References

- [Paramiko](https://docs.paramiko.org/)  
- [Fabric](https://docs.fabfile.org/)
