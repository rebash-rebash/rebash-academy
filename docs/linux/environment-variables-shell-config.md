---
title: Environment Variables and Shell Configuration
description: "Gateway — environment variables for Linux ops; see Users/sudo, Scheduling, and the Shell Scripting track for full depth."
difficulty: beginner
estimated_time: "5 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: linux
tags:
  - linux
  - environment
  - gateway
comments: false
---


# Environment Variables and Shell Configuration

## Overview



This is a core tutorial in **Module** of the REBASH Academy **Linux for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

- See the course overview for prerequisites

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Environment Variables and Shell Configuration” in a real environment
- [ ] Complete the hands-on lab with clear outputs
- [ ] Relate this topic to Cloud, DevOps, and production operations
- [ ] Explain the failure modes you would check first in an incident

## Architecture

This topic’s control points and relationships are shown below.

![Architecture diagram for Environment Variables and Shell Configuration](../assets/excalidraw/linux-architecture.svg)

## Theory

### What it is

**Environment variables** are key/value pairs inherited by child processes. They configure locale, `PATH`, credentials hooks, proxy settings, and application options without recompiling binaries. **Shell configuration** files (such as `~/.bashrc`, `~/.profile`, and `/etc/profile.d/*`) set interactive and login defaults. This page is a **gateway**: deep Bash configuration and quoting live in the Shell Scripting track; identity and scheduling context appear in the linked Linux tutorials below.

### Why it matters

Cron jobs fail when `PATH` differs from your SSH session. CI runners leak secrets when variables are printed in logs. Containers and systemd units each have their own environment model — confusing them causes “works on my SSH” outages. Operators need a clear mental model of *where* a variable is set and *which* processes inherit it.

### How it works

The shell exports variables into the environment (`export NAME=value`). Login shells source profile files; interactive non-login shells typically source `bashrc`. systemd services use `Environment=` / `EnvironmentFile=`; containers receive `ENV`/`environment:` from the runtime. Prefer secret stores or files with tight permissions over long-lived secrets in world-readable profiles. Inspect with `env`, `printenv`, and `systemctl show-environment` where relevant.

### Key concepts and comparisons

| Context | Where env is set |
|---------|------------------|
| Interactive SSH | `~/.bashrc`, `~/.profile` |
| cron | Minimal env — set explicitly |
| systemd service | Unit `Environment*` directives |
| Container | Image/runtime config |

| Learn next | Tutorial |
|------------|----------|
| Users and sudo | [Users, Groups, and sudo](users-groups-and-sudo.md) |
| Scheduled jobs | [Scheduling — cron, at, and Timers](scheduling-cron-at-and-timers.md) |
| Shell depth | [Shell Scripting track](../shell/index.md) |

### Common pitfalls

- Putting secrets in `~/.bashrc` that sync to dotfile git repos.
- Assuming cron inherits your interactive `PATH`.
- Exporting huge `PATH` prefixes that shadow system binaries unexpectedly.
- Printing env in CI logs without redaction.

## Hands-on Lab
Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-linux/lab01 && cd ~/rebash-linux/lab01
```

**Focus:** practise Environment Variables and Shell Configuration with inspect → change → verify

### Step 1 – Inspect current state

```bash
pwd
whoami
uname -a
echo "PATH=$PATH"
ls -la
```

### Step 2 – Hands-on for this topic

```bash
cat > practise.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "topic: Environment Variables and Shell Configuration"
date -u +"utc=%Y-%m-%dT%H:%M:%SZ"
EOF
chmod +x practise.sh
./practise.sh | tee practise.out
test -s practise.out
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-linux/ for later tutorials
```

## Validation

- [ ] Lab commands run under `~/rebash-linux/lab01/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Environment Variables and Shell Configuration** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for linux as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Putting secrets in `~/.bashrc` that sync to dotfile git repos."
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Assuming cron inherits your interactive `PATH`."
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Environment Variables and Shell Configuration changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Auth / permission denied | Wrong identity, policy, or scope | Check caller identity, roles, and least-privilege policies |
| Timeout / no route | Network, DNS, security group, or endpoint | Trace path, DNS, and allow-lists before retrying |
| Drift / unexpected plan | Manual change or wrong state/workspace | Reconcile desired vs actual; avoid click-ops on managed resources |
| Pipeline/job red | Flaky step, cache, or missing secret | Read failing step logs; bisect recent workflow/config changes |
| Cost spike | Idle load balancer, NAT, oversized compute | Inventory billable resources; stop/delete labs promptly |

## Summary

**Environment Variables and Shell Configuration** is essential for Cloud and DevOps engineers working with linux. Practise the lab until the inspection and change path is muscle memory, then continue the track.

## Interview Questions

1. How does **Environment Variables and Shell Configuration** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - Continue from the course [index](index.md)

## References

- Track index: [Course overview](index.md)
