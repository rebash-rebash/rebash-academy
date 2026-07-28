---
title: Remote systemd Service Control
description: Manage systemd units on remote servers with systemctl --host, dedicated service accounts, and polkit authorization rules.
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - systemd
  - remote-admin
  - polkit
prerequisites:
  - SSH and Remote Administration
  - systemd Service Management
comments: false
---

# Remote systemd Service Control

## Overview

When you operate a fleet of Linux servers, logging into each host to run `systemctl restart nginx` does not scale. systemd supports **remote management** over SSH via `systemctl --host`, and **PolicyKit (polkit)** lets you grant narrowly scoped privileges — for example, allowing a `systemd-manager` user to restart specific services without full root access.

This tutorial goes beyond surface-level examples: you will create a dedicated management user, configure SSH keys, write polkit rules that authorize only defined actions, and operate services remotely with the same commands you use locally.

This is **Module 5, Tutorial 12** in the REBASH Academy Linux series.

## Prerequisites

- [SSH and Remote Administration](ssh-remote-administration.md) — key-based auth and `~/.ssh/config`
- [systemd Service Management](systemd-service-management.md) — `systemctl`, units, and journal basics
- Two Linux VMs (or one machine simulating remote via `localhost` and a second user) with systemd 230+
- `sudo` on the **remote** server to create users and polkit rules

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run `systemctl` and `journalctl` against remote hosts with `--host user@server`
- [ ] Create a least-privilege `systemd-manager` service account
- [ ] Write polkit rules granting specific systemd actions to non-root users
- [ ] Diagnose "Access denied" and SSH transport failures in remote systemctl
- [ ] Compare remote systemctl with configuration management and SSH ad-hoc patterns
- [ ] Apply security boundaries so operators cannot reload arbitrary units

## Architecture

```d2
direction: down

Admin: Workstation {
      style: {
        fill: "#dbeafe"
        stroke: "#2563eb"
      }
        A: "systemctl --host"
        B: "journalctl --host"
    }
    SSH: Transport {
      style: {
        fill: "#dcfce7"
        stroke: "#16a34a"
      }
        C: "Encrypted SSH Session"
    }
    Remote: Server {
      style: {
        fill: "#ffedd5"
        stroke: "#ea580c"
      }
        D: "systemd-manager user"
        E: "polkit / pkaction"
        F: "systemd PID 1"
        G: "Unit Files"
        H: "Running Services"
    }
    Admin.A -> SSH.C
    Admin.B -> SSH.C
    SSH.C -> Remote.D
    Remote.D -> Remote.E
    Remote.E -> Remote.F: authorized
    I: "Access Denied"
    Remote.E -> I: denied
    Remote.F -> Remote.G
    Remote.F -> Remote.H
```

## Theory

### How `systemctl --host` works

When you run:

```bash
systemctl --host deploy@web01 status nginx
```

the local `systemctl` binary opens an **SSH connection** to `web01` as user `deploy`, then executes the equivalent command in a **pseudo-terminal** or D-Bus proxy context on the remote side. The remote user must have permission to talk to systemd — typically via polkit rules or membership in a privileged group.

Requirements:

- SSH key auth working for `user@host`
- Remote machine running systemd as PID 1
- Compatible systemd versions (major mismatch can cause protocol errors)
- Polkit authorization for non-root users performing privileged actions

The same `--host` flag works with `journalctl`:

```bash
journalctl --host deploy@web01 -u nginx -n 20
```

### Why not give everyone sudo?

`sudo systemctl restart *` is effectively root. Production teams want **separation of duties**:

| Role | Allowed actions |
|------|-----------------|
| Developer | `status`, `is-active`, read logs |
| On-call SRE | restart specific app units |
| Platform admin | full systemctl, daemon-reload |

Polkit expresses these as **fine-grained rules** evaluated at action time, logged in `/var/log/auth.log` or journal.

### The systemd-manager user pattern

Create a dedicated account:

- No interactive login shell required (use `/bin/bash` or `/sbin/nologin` depending on policy)
- SSH key in `~/.ssh/authorized_keys` — no password
- Member of groups only if needed; authorization primarily via polkit
- Home directory for SSH metadata only

This account is **not** a human user — it is a service identity for automation and jump-box workflows.

### Polkit fundamentals

**PolicyKit** mediates privileged actions for unprivileged processes. systemd registers actions like:

- `org.freedesktop.systemd1.manage-units` — start, stop, restart units
- `org.freedesktop.systemd1.reload-or-restart-unit`
- `org.freedesktop.systemd1.manage-unit-files` — enable, disable (more sensitive)

Rules live in:

- `/etc/polkit-1/rules.d/` — JavaScript-like `.rules` files (evaluated top-down, **first match wins** for allow/deny)
- `/usr/share/polkit-1/actions/` — action definitions with defaults

Example rule structure:

```javascript
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.systemd1.manage-units" &&
        subject.user == "systemd-manager" &&
        action.lookup("unit") == "nginx.service") {
        return polkit.Result.YES;
    }
});
```

After adding rules: no daemon reload needed for polkit — rules are read on each action. Verify with `pkaction` and test remote commands.

### Remote vs local systemctl differences

| Aspect | Local | Remote `--host` |
|--------|-------|-----------------|
| Transport | D-Bus socket | SSH |
| Auth | Session polkit | Remote user's polkit/sudo |
| Latency | Instant | Network + SSH overhead |
| Tab completion | Full | Limited |
| File paths in units | Local paths | Remote paths |

Unit file edits still happen **on the server** — remote systemctl does not sync files. Use Ansible, cloud-init, or CI/CD for unit file deployment; use remote systemctl for **runtime control**.

### Security considerations

- Restrict `systemd-manager` SSH access by source IP in `sshd_config` (`Match Address`)
- Never share the management private key across people — use individual keys mapped to the same polkit-scoped user, or separate users per team
- Audit polkit and SSH logs centrally
- Deny `daemon-reload` and `enable` unless platform team requires it — those change boot behavior

## Hands-on Lab

These steps assume a **remote server** (replace `REMOTE` with hostname/IP). For single-machine practice, use `REMOTE=localhost` and a second user on the same box.

```bash
export REMOTE=localhost   # change to your server IP/hostname
export MGMT_USER=systemd-manager
```

### Step 1 – Create the systemd-manager user (on remote server)

Run on the remote server:

```bash
sudo useradd --create-home --comment "Remote systemd operator" "$MGMT_USER"
sudo mkdir -p /home/$MGMT_USER/.ssh
sudo chmod 700 /home/$MGMT_USER/.ssh
sudo chown -R $MGMT_USER:$MGMT_USER /home/$MGMT_USER/.ssh
id "$MGMT_USER"
```

**Expected output:** user uid/gid lines; home `/home/systemd-manager`.

### Step 2 – Deploy SSH public key

From your workstation (key from [SSH tutorial](ssh-remote-administration.md)):

```bash
ssh-keygen -t ed25519 -f ~/.ssh/systemd_mgr_ed25519 -N "" -C "systemd-manager-key"
sudo bash -c "cat >> /home/$MGMT_USER/.ssh/authorized_keys" < ~/.ssh/systemd_mgr_ed25519.pub
sudo chmod 600 /home/$MGMT_USER/.ssh/authorized_keys
sudo chown $MGMT_USER:$MGMT_USER /home/$MGMT_USER/.ssh/authorized_keys
```

Test SSH:

```bash
ssh -i ~/.ssh/systemd_mgr_ed25519 ${MGMT_USER}@${REMOTE} 'whoami && hostname'
```

**Expected output:** `systemd-manager` and the server hostname.

### Step 3 – Baseline remote status (expect permission errors)

Without polkit rules, privileged actions fail for non-root:

```bash
systemctl --host ${MGMT_USER}@${REMOTE} status ssh 2>/dev/null \
  || systemctl --host ${MGMT_USER}@${REMOTE} status sshd
```

**Expected output:** service status may work (read-only) on some distros, or polkit authentication prompt / access denied for restricted views.

Check failed units:

```bash
systemctl --host ${MGMT_USER}@${REMOTE} --failed --no-pager
```

**Expected output:** list of failed units or `0 loaded units listed`.

### Step 4 – Install polkit rule for nginx management

On the **remote server**, allow `systemd-manager` to manage only `nginx.service` (install nginx if needed for the lab):

```bash
sudo apt-get install -y nginx 2>/dev/null || sudo dnf install -y nginx 2>/dev/null || true
```

Create polkit rule:

```bash
sudo tee /etc/polkit-1/rules.d/50-systemd-manager-nginx.rules << 'EOF'
polkit.addRule(function(action, subject) {
    if (subject.user == "systemd-manager") {
        if (action.id == "org.freedesktop.systemd1.manage-units") {
            var unit = action.lookup("unit");
            if (unit == "nginx.service") {
                return polkit.Result.YES;
            }
        }
        if (action.id == "org.freedesktop.systemd1.manage-units" &&
            action.lookup("verb") == "reload-or-restart") {
            if (action.lookup("unit") == "nginx.service") {
                return polkit.Result.YES;
            }
        }
    }
});
EOF
```

List matching polkit actions:

```bash
pkaction | grep -i systemd | head -5
```

**Expected output:** action IDs like `org.freedesktop.systemd1.manage-units`.

### Step 5 – Remote restart nginx

```bash
systemctl --host ${MGMT_USER}@${REMOTE} restart nginx
systemctl --host ${MGMT_USER}@${REMOTE} is-active nginx
```

**Expected output:** `active`

If nginx is not installed, substitute a running unit you scoped in polkit (e.g., a custom `rebash-demo.service`).

### Step 6 – Verify authorization boundary

Attempt to restart sshd (not authorized):

```bash
systemctl --host ${MGMT_USER}@${REMOTE} restart sshd 2>&1 | head -3
```

**Expected output:** `Access denied`, `Interactive authentication required`, or polkit rejection — **not** a successful restart.

### Step 7 – Remote journal access

```bash
journalctl --host ${MGMT_USER}@${REMOTE} -u nginx -n 5 --no-pager
```

**Expected output:** last five nginx log lines from the remote journal.

Follow logs remotely (Ctrl+C to stop):

```bash
timeout 3 journalctl --host ${MGMT_USER}@${REMOTE} -u nginx -f --no-pager || true
```

**Expected output:** streaming log lines or timeout exit after 3 seconds.

### Step 8 – SSH config shortcut and fleet check script

Add to `~/.ssh/config`:

```
Host web-fleet
    HostName YOUR_REMOTE_IP
    User systemd-manager
    IdentityFile ~/.ssh/systemd_mgr_ed25519
```

Fleet health script:

```bash
cat > ~/lab/check_fleet.sh << 'EOF'
#!/bin/bash
set -euo pipefail

HOSTS=(web-fleet)   # add more Host aliases

for h in "${HOSTS[@]}"; do
  printf '%-20s ' "$h"
  if systemctl --host "$h" is-system-running --wait 2>/dev/null; then
    failed=$(systemctl --host "$h" --failed --no-legend 2>/dev/null | wc -l)
    echo "running (failed units: $failed)"
  else
    echo "UNREACHABLE or degraded"
  fi
done
EOF
chmod +x ~/lab/check_fleet.sh
```

Run against configured host:

```bash
~/lab/check_fleet.sh
```

**Expected output:** host name with `running` and failed unit count.

## Validation

Confirm the lab before moving on:

1. Re-run the critical commands from the Hands-on Lab and compare them to the expected output in each step.
2. Check that you can explain *why* each successful result matters (not only that it printed).
3. Note any warnings or unexpected output — resolve them using Troubleshooting before continuing.

| Check | Pass criteria |
|-------|----------------|
| Lab steps | All required steps completed on your machine |
| Expected output | Matches the tutorial (or a documented equivalent) |
| Cleanup | Temporary files, containers, or resources removed if the lab says so |

## Code Walkthrough

| Command | Description |
|---------|-------------|
| `systemctl --host USER@HOST status UNIT` | Remote service status |
| `systemctl --host USER@HOST start UNIT` | Remote start |
| `systemctl --host USER@HOST stop UNIT` | Remote stop |
| `systemctl --host USER@HOST restart UNIT` | Remote restart |
| `systemctl --host USER@HOST reload UNIT` | Remote reload (if unit supports it) |
| `systemctl --host USER@HOST is-active UNIT` | Check if unit is active |
| `systemctl --host USER@HOST is-enabled UNIT` | Check if unit is enabled at boot |
| `systemctl --host USER@HOST --failed` | List failed units on remote |
| `systemctl --host USER@HOST list-units --type=service` | List remote services |
| `journalctl --host USER@HOST -u UNIT` | Remote unit logs |
| `journalctl --host USER@HOST -p err -n 20` | Recent remote errors |
| `pkaction \| grep systemd` | List polkit actions for systemd |
| `pkcheck --action-id ... --process $$` | Test polkit authorization |
| `systemctl --version` | Verify local/remote systemd compatibility |

## Code

### Polkit rule — read-only status for developers

```javascript
// /etc/polkit-1/rules.d/40-dev-readonly.rules
polkit.addRule(function(action, subject) {
    if (subject.user == "dev-readonly" &&
        action.id == "org.freedesktop.systemd1.properties") {
        return polkit.Result.YES;
    }
});
```

### Polkit rule — multiple allowed units

```javascript
polkit.addRule(function(action, subject) {
    if (subject.user != "systemd-manager") return;

    var allowed = ["nginx.service", "app-backend.service", "worker.service"];
    if (action.id != "org.freedesktop.systemd1.manage-units") return;

    var unit = action.lookup("unit");
    if (allowed.indexOf(unit) >= 0) {
        return polkit.Result.YES;
    }
});
```

### Ansible-style loop without Ansible

```bash
#!/bin/bash
set -euo pipefail

SERVICES=(nginx app-worker)
HOST=systemd-manager@prod-web01

for svc in "${SERVICES[@]}"; do
  echo "=== $svc ==="
  systemctl --host "$HOST" is-active "$svc"
done
```

## Security Considerations

- Prefer least privilege for every account, role, and service identity you create in labs
- Never commit secrets, private keys, kubeconfigs, or cloud credentials to Git
- Prefer official packages and signed images; verify checksums for air-gapped installs
- Limit network exposure: bind services to localhost in labs unless the exercise requires otherwise
- Enable audit logging where the platform supports it, and practise reading those logs
- Treat production as hostile: assume misconfiguration will be probed

## Common Mistakes

!!! warning "Granting org.freedesktop.systemd1.manage-units without unit filter"
    A rule that returns YES for all units is equivalent to passwordless root for service control. Always filter on `action.lookup("unit")`.

!!! warning "Forgetting SSH must work before systemctl --host works"
    Test `ssh user@host true` first. systemctl errors about connection are SSH problems, not systemd problems.

!!! warning "Mixing up user contexts"
    `systemctl --host root@host` vs `systemctl --host systemd-manager@host` hit different polkit policies. Use the least-privileged account that can perform the task.

!!! warning "Editing unit files remotely via shell heredocs"
    Remote systemctl controls runtime state, not configuration management. Deploy unit files through reviewed pipelines, then `daemon-reload` deliberately.

## Best Practices

!!! tip "One polkit rule file per role"
    Name files `50-team-app-restart.rules`, `51-platform-full.rules` for clarity and auditability.

!!! tip "Log and alert on denied polkit actions"
    Forward auth logs to SIEM; repeated denials may indicate compromise attempts or misconfigured automation.

!!! tip "Use SSH config Host aliases in scripts"
    Scripts reference `prod-web-01`, not raw IPs — easier rotation and bastion jumps.

!!! tip "Test rules with a non-production user first"
    Clone polkit rules to staging; verify both allowed and denied actions before promoting.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `Failed to connect to bus` | Remote user cannot access systemd D-Bus | Add polkit rule or use privileged user |
| `Access denied` | Polkit rule missing or wrong unit name | Check exact unit name with `.service` suffix; review rules.d |
| `Host key verification failed` | SSH known_hosts mismatch | Update known_hosts after server rebuild |
| `Connection timed out` | Firewall, wrong IP, sshd down | Verify network path and SSH separately |
| `Unit not found` | Typo or unit not installed on remote | `systemctl --host ... list-unit-files \| grep name` |
| Works locally, fails remotely | Different polkit defaults per user | Compare `pkaction --verbose` and auth logs |
| `systemctl: invalid option --host` | Ancient systemd version | Upgrade systemd or use SSH wrapper script |

## Summary

- `systemctl --host user@server` and `journalctl --host` manage remote systemd over SSH — same CLI, different transport.
- A dedicated **systemd-manager** user with key-based SSH separates human admin accounts from automation identities.
- **Polkit rules** in `/etc/polkit-1/rules.d/` grant least-privilege: specify user, action ID, and unit name — never blanket YES for manage-units.
- Unauthorized restart attempts should fail loudly; authorized restarts should succeed without sudo passwords.
- Remote control handles **runtime**; unit file deployment belongs in configuration management with reviewed changes.

## Interview Questions

1. How does `systemctl --host` transport commands to a remote server?
2. Why create a dedicated `systemd-manager` user instead of sharing root SSH keys?
3. What is polkit, and how does it differ from sudo?
4. Name two polkit action IDs related to systemd unit management.
5. How would you allow a user to restart `nginx.service` but not `sshd.service`?
6. What happens if your polkit rule omits the `.service` suffix in the unit lookup?
7. How do you view remote logs for a unit without SSH-ing in manually?
8. Why should `daemon-reload` and `enable` be more restricted than `restart`?
9. What would you check first if `systemctl --host user@host status nginx` hangs?
10. Compare remote systemctl with running `ssh user@host 'sudo systemctl restart nginx'`.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [SSH and Remote Administration](ssh-remote-administration.md) *(previous)*
- [Disk and Filesystem Management](disk-and-filesystem-management.md) *(next)*
- [systemd Service Management](systemd-service-management.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)

## References

- [systemd.systemctl man page — `--host`](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html)
- [Polkit official documentation](https://gitlab.freedesktop.org/polkit/polkit/-/blob/master/docs/polkit.8.md)
- [Red Hat — Managing systemd units with polkit](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/managing_monitoring_and_updating_the_kernel/managing-systemd-units-with-polkit_managing-monitoring-and-updating-the-kernel)
- [systemd D-Bus API](https://www.freedesktop.org/wiki/Software/systemd/dbus/)
- [REBASH Academy – Linux Overview](index.md)
