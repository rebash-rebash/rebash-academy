---
title: "Environment Variables and Shell Configuration"
description: "Linux environment variables, PATH, shell startup files, and systemd Environment= — with a cron-vs-SSH break-and-fix lab."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-04"
category: linux
technology: linux
module: "Module 2 · Command Line"
learning_paths:
  - linux-administrator
  - devops-engineer
  - cloud-engineer
tags:
  - linux
  - environment
  - bash
  - systemd
  - beginners
prerequisites:
  - linux/essential-linux-commands
next:
  - linux/shell-scripting-fundamentals
related:
  - ../shell/index.md
  - linux/shell-scripting-fundamentals
interview: interview/linux
comments: false
---

# Environment Variables and Shell Configuration

## Overview

You will see `export API_URL=...` in tutorials and wonder why it “disappears” tomorrow. Environment variables are how Linux passes **configuration** into programs for a session — and into services for their whole lifetime.

**Plain problem:** A script works in your SSH session but fails in **cron** with “command not found”. Same script — different **environment**. Cron did not load your `.bashrc`; **`PATH`** was shorter.

An **environment variable** is a named string every child process inherits: **`PATH`** (where to find commands), **`HOME`**, **`LANG`**, app settings. They live in three common places: interactive shell, startup files, and **systemd** units.

This is a **Command Line** tutorial in the REBASH Academy **Linux for Cloud & DevOps Engineers** series — practical Linux for Cloud and DevOps work.

## Prerequisites

- Ubuntu practice VM or WSL2
- [Essential Linux Commands](essential-linux-commands.md)
- Basic comfort typing commands in bash

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Explain environment variables in plain language
- [ ] Inspect and set variables with `export`, `env`, and `printenv`
- [ ] Add a lab-safe snippet under `/etc/profile.d/`
- [ ] Understand why cron jobs miss SSH environment variables
- [ ] Set **`Environment=`** in a systemd unit
- [ ] Answer fresher interview questions on environment and shell config

## Architecture

Login shell reads profile files → sets environment → starts processes that inherit copies. Non-interactive cron/systemd paths skip most of your personal `.bashrc` unless you configure them.

![Linux CLI workflow — shell, env, PATH, systemd](../assets/excalidraw/linux-cli-workflow.svg)

## Theory

### The problem (before any jargon)

You add a tool to `~/bin` and it works after `export PATH=$PATH:~/bin` in SSH. Night cron job still says `mytool: not found`. You did not persist **`PATH`** where cron looks.

### What is an environment variable? (simple words)

**Analogy:** Environment variables are **sticky notes on your desk** every helper (process) reads when they start — “find tools in these folders”, “use this language”, “API lives here”.

| Variable | Typical role |
|----------|----------------|
| **PATH** | Directories searched for command names |
| **HOME** | Your home directory |
| **USER** | Username |
| **SHELL** | Default shell program |
| **LANG** | Locale / language |

**Interview line:** “Processes inherit environment at fork time; cron and systemd need explicit PATH or env files.”

### View and set (session vs persistent)

``` {.bash .ra-terminal title="Terminal"}
echo "$PATH"
export REBASH_LAB=hello
env | grep REBASH
```

Session-only `export` dies when you log out unless written to startup files.

### Startup files (Ubuntu bash — simplified)

| File | When |
|------|------|
| `/etc/profile` | Login shells |
| `/etc/profile.d/*.sh` | Modular login snippets (good for admins) |
| `~/.bashrc` | Interactive non-login bash |
| `~/.profile` | User login |

**Do not** edit system files recklessly on production — use drop-ins under `profile.d` with clear names.

### systemd Environment=

Services do not read your `.bashrc`. Set env in the unit:

```ini
[Service]
Environment="APP_MODE=production"
EnvironmentFile=/etc/myapp/env
```

### Cron vs SSH environment

Cron runs with minimal env. **Fix:** absolute paths in scripts, or `PATH=` line at top of crontab, or wrap in systemd timer (prior scheduling tutorial).

### Common pitfalls

- Putting secrets in world-readable env files
- Expecting `~` expansion in systemd `Environment=` (use full paths)
- Mixing login vs non-login shell behaviour
- `export` in script without `export` keyword — child processes miss it

## Hands-on Lab

### Objective

Set lab variables, add a **`profile.d`** snippet, demonstrate **cron missing PATH**, **fix** with absolute path, add **systemd Environment=**, prove — under `~/rebash-linux/lab-env`.

### Prerequisites

| Item | Notes |
|------|--------|
| Ubuntu VM | bash default |
| `sudo` | For profile.d and systemd drop-in |

### Lab environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab-env/bin && cd ~/rebash-linux/lab-env
```

### Real-world scenario

App team adds `~/bin/deploy-helper`. Works interactively; cron deploy fails. You document environment inheritance and fix cron path — ticket style.

### Step-by-step tasks

#### Task 1 – Custom tool and PATH

Create `deploy-helper`:

```bash title="deploy-helper"
#!/usr/bin/env bash
echo "deploy-helper ran OK at $(date -Is)"
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
chmod +x bin/deploy-helper
export PATH="$HOME/rebash-linux/lab-env/bin:$PATH"
deploy-helper | tee path-session-proof.txt
grep -q 'deploy-helper ran OK' path-session-proof.txt
```

!!! example "Expected output"
    Helper runs when `~/rebash-linux/lab-env/bin` is on PATH.


#### Task 2 – profile.d persistence

Create `rebash-lab-env.sh`:

```bash title="rebash-lab-env.sh"
# REBASH lab-env — append lab bin to PATH for login shells
export PATH="$HOME/rebash-linux/lab-env/bin:$PATH"
export REBASH_APP_ENV=lab
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
sudo cp rebash-lab-env.sh /etc/profile.d/rebash-lab-env.sh
sudo chmod 644 /etc/profile.d/rebash-lab-env.sh
bash -lc 'echo PATH=$PATH; echo REBASH_APP_ENV=$REBASH_APP_ENV' | tee login-shell-env.txt
grep -q 'lab-env/bin' login-shell-env.txt
```

!!! example "Expected output"
    Login shell simulation shows lab bin on PATH and `REBASH_APP_ENV=lab`.


#### Task 3 – Break cron env, fix, systemd Environment=

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
( crontab -l 2>/dev/null; echo '* * * * * deploy-helper >> '"$HOME"'/rebash-linux/lab-env/logs/cron-broken.log 2>&1' ) | crontab -
mkdir -p logs
sleep 65
tail -3 logs/cron-broken.log 2>/dev/null | tee cron-broken-tail.txt || true
grep -q 'not found' cron-broken-tail.txt && echo "cron missed PATH — expected break" | tee break-notes.txt
crontab -r
( crontab -l 2>/dev/null; echo '* * * * * '"$HOME"'/rebash-linux/lab-env/bin/deploy-helper >> '"$HOME"'/rebash-linux/lab-env/logs/cron-fixed.log 2>&1' ) | crontab -
sleep 65
grep -q 'deploy-helper ran OK' logs/cron-fixed.log
echo "lab-env OK" | tee evidence.txt
```

Create `rebash-env-demo.service`:

```ini title="rebash-env-demo.service"
[Unit]
Description=REBASH lab env demo oneshot

[Service]
Type=oneshot
Environment="REBASH_APP_ENV=systemd-demo"
ExecStart=/usr/bin/env bash -c 'echo REBASH_APP_ENV=$REBASH_APP_ENV >> /tmp/rebash-systemd-env.log'
```

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
sed "s|/tmp/rebash-systemd-env.log|$HOME/rebash-linux/lab-env/logs/systemd-env.log|" rebash-env-demo.service | sudo tee /etc/systemd/system/rebash-env-demo.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl start rebash-env-demo.service
grep systemd-demo logs/systemd-env.log
crontab -r 2>/dev/null || true
```

!!! example "Expected output"
    Cron fails without full path; succeeds with absolute path. systemd log shows `systemd-demo`.


### Validation steps

- [ ] Session PATH demo works
- [ ] profile.d affects login shell simulation
- [ ] Cron break/fix documented
- [ ] systemd Environment= proven in log file

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| command not found in cron | PATH | Absolute path or PATH= in crontab |
| Variable empty in systemd | Not in unit | Environment= or EnvironmentFile= |
| profile.d not loaded | Non-login shell | Use `bash -l` or correct file |
| Permission denied profile.d | Bad perms | 644, root-owned |

### Challenge exercise

Add `printenv > ~/rebash-linux/lab-env/env-snapshot.txt` from SSH and from a one-line cron job — compare line counts in your notes.

### Learning outcomes

- You understand inheritance vs cron/systemd config
- You fixed a classic “works in SSH only” bug
- You can explain PATH to an interviewer

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
crontab -r 2>/dev/null || true
sudo rm -f /etc/profile.d/rebash-lab-env.sh /etc/systemd/system/rebash-env-demo.service
sudo systemctl daemon-reload
```

## Validation

- [ ] Evidence under `~/rebash-linux/lab-env`
- [ ] Can explain three places env vars are set
- [ ] Ready for filesystem paths tutorial next

## Code Walkthrough

1. **`export PATH=...`** — session only until profile.d or unit file persists.
2. **`/etc/profile.d/`** — modular admin-friendly login snippets.
3. **Cron without PATH** — deliberate break; mirrors production incidents.
4. **Absolute path fix** — simplest reliable cron fix.
5. **systemd Environment=** — services ignore `.bashrc` by design.

## Security Considerations

- Never put passwords or API keys in world-readable profile.d or unit files in Git.
- Use secret managers or restricted `EnvironmentFile` (`0600`, root-only).
- Audit `/etc/environment` and profile.d for stale exports.
- Limit who can edit systemd unit drop-ins.
- Scrub env snapshots before sharing in tickets.

## Common Mistakes

!!! warning "Secrets in export lines"
    Environment leaks via `ps`, logs, and core dumps — use proper secret storage.

!!! warning "Assuming cron loads .bashrc"
    It does not — configure env explicitly.

!!! warning "Tilde in systemd paths"
    Use full paths like `/home/user/bin/app`.

## Best Practices

- Document required env vars in README/runbook
- Use `EnvironmentFile` for services; keep out of Git
- Prefer systemd timers over cron when you need journald + env in one place
- Test jobs with `sudo -u appuser env` to simulate service user
- Version-control non-secret defaults only

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Variable unset in cron | Minimal env | Absolute paths; PATH= line |
| Works sudo, not cron | Different user | Crontab user; file perms |
| Empty in systemd service | Missing Environment | Unit drop-in |
| Lost after reboot | Never persisted | profile.d or unit file |

## Summary

**Environment variables** configure processes via inheritance. **`PATH`** is the classic trap — SSH vs **cron** vs **systemd** load different context. Use **`export`**, **`/etc/profile.d/`**, and **`Environment=`** deliberately, and prefer **absolute paths** in scheduled jobs.

## Interview Questions

**1. What is an environment variable?**

??? success "Reveal answer"
    A named string in a process environment inherited by child processes — e.g. **PATH** (command search path), **HOME**, **LANG**. Set with `export VAR=value`; view with `printenv` or `echo $VAR`.

**2. Why do cron jobs fail to find commands that work in SSH?**

??? success "Reveal answer"
    Cron provides a **minimal environment** — often a short PATH, no `.bashrc`. Fix with **absolute paths** to scripts/binaries, explicit `PATH=` in crontab, or use systemd timer/service with Environment set.

**3. Difference between shell variable and exported variable?**

??? success "Reveal answer"
    Shell variable exists in current shell only. **`export`** puts it in the environment so **child processes** inherit it. Scripts and cron child shells need export (or set in their context).

**4. Where would you set env for a systemd service?**

??? success "Reveal answer"
    In the unit file: **`Environment=`** lines or **`EnvironmentFile=`** pointing to a file. Then `daemon-reload` and restart. Services do not read interactive `.bashrc`.

**5. What is PATH?**

??? success "Reveal answer"
    Colon-separated list of directories the shell searches for executable **by name**. If directory is not on PATH, you need `./script` or full path.

**6. /etc/profile.d vs ~/.bashrc — when each?**

??? success "Reveal answer"
    **`/etc/profile.d/`** — system-wide login snippets (admins, all users). **`~/.bashrc`** — per-user interactive bash. Know login vs non-login shell rules to predict which runs.

**7. How do you debug missing env in a job?**

??? success "Reveal answer"
    Log environment at job start (`env >> /tmp/job-env.log`), compare SSH vs cron vs systemd (`systemctl show unit -p Environment`), fix with absolute paths or explicit Environment/EnvironmentFile.

## Related Tutorials

- Previous: [Essential Linux Commands](essential-linux-commands.md)
- Next: [Filesystem Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md)
- Related: [Shell Scripting Fundamentals](shell-scripting-fundamentals.md)
- Deeper track: [Shell Scripting](../shell/index.md)

## References

- [bash invocation man page](https://manpages.ubuntu.com/manpages/noble/man1/bash.1.html)
- [systemd.exec Environment](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#Environment=)
- [Ubuntu environment variables guide](https://help.ubuntu.com/community/EnvironmentVariables)
