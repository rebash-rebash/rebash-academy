---
title: "Environment Variables and Shell Configuration"
description: "Set and inspect environment variables for Linux ops — export, shell startup files, and systemd Environment= — with an Ubuntu lab."
difficulty: beginner
estimated_time: "40–50 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 2 · Command Line"
tags:
  - linux
  - environment
  - bash
  - systemd
prerequisites:
  - linux/essential-linux-commands
next:
  - linux/filesystem-paths-links-mounts-and-inodes
related:
  - ../shell/index.md
interview: interview/linux
comments: false
---

# Environment Variables and Shell Configuration

## Overview

An **environment variable** is a named string value that processes inherit. Shells use variables such as **`PATH`** (where to find commands), **`HOME`**, and **`LANG`**. Applications and Continuous Integration (CI) jobs read variables for configuration (urls, feature flags — not secrets in world-readable files).

On Linux servers you meet variables in three common places: your interactive shell (`export`), shell startup files (`.bashrc`, `/etc/profile.d/`), and **systemd** units (`Environment=` / `EnvironmentFile=`). Cron jobs use a smaller environment than your SSH session — a classic cause of “works in my shell, fails in cron”. In this tutorial you will inspect variables, create a lab `profile.d` script, run a command with a one-shot env override, and save proof under `~/rebash-linux/lab-env`.

For deeper Bash scripting, continue in the [Shell Scripting](../shell/index.md) track after this ops-focused page.

## Prerequisites

- [Essential Linux Commands](essential-linux-commands.md)
- A **practice Ubuntu 22.04/24.04 VM** with `sudo` (for `/etc/profile.d`)
- Bash as your login shell (Ubuntu default)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Print and explain key variables (`PATH`, `HOME`, `USER`)
- [ ] Use `export` and one-shot `VAR=value command` overrides
- [ ] Add a safe drop-in under `/etc/profile.d/` and prove it in a login shell
- [ ] Show how systemd exposes `Environment=` on a oneshot unit
- [ ] Pack evidence under `~/rebash-linux/lab-env`

## Architecture

Environment values flow from system/profile files and service managers into shells and child processes.

![Architecture diagram for CLI and environment](../assets/excalidraw/linux-cli-workflow.svg)

## Theory

### What it is

Variables live in a process environment. Children inherit a copy. `export VAR=value` marks a shell variable for inheritance. `env` / `printenv` list the environment.

```bash
printenv PATH
echo "$HOME"
export REBASH_LAB=1
VAR=tmp printenv VAR
```

### Why it matters

Wrong `PATH` breaks deploys. Missing variables break apps. Putting secrets in exported variables that leak into logs or `ps` is a security problem. systemd and cron each have their own environment rules.

### How it works

| Place | Typical use |
|-------|-------------|
| Current shell | `export`, one-shot prefix |
| `~/.bashrc` / `~/.profile` | Per-user interactive defaults |
| `/etc/profile.d/*.sh` | System-wide login defaults |
| systemd `Environment=` | Service configuration |
| cron | Minimal env — set variables in the crontab |

### Common pitfalls

- Editing `.bashrc` but testing with a non-interactive script.  
- Assuming cron has your SSH `PATH`.  
- Storing passwords in `Environment=` without restricting unit file permissions.  
- Forgetting quotes when values contain spaces.

## Hands-on Lab

### Objective

Inspect the environment, install a lab `/etc/profile.d` script, prove a login shell sees it, run a systemd oneshot with `Environment=`, and save evidence under `~/rebash-linux/lab-env`.

### Prerequisites

- Ubuntu with Bash and systemd

### Lab environment

Workspace: `~/rebash-linux/lab-env`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab-env && cd ~/rebash-linux/lab-env
set -euo pipefail
echo "$SHELL" | tee shell.txt
printenv PATH | tee path.txt
printenv HOME USER | tee home-user.txt
```

!!! example "Expected output"
    `shell.txt` shows a bash path; PATH and HOME captured.


### Real-world scenario

Your team wants every engineer login on a practice jump VM to see `REBASH_LAB_ENV=1`, and a small maintenance unit should run with `APP_ENV=lab`. You implement both and keep proof for the onboarding guide.

### Step-by-step tasks

#### Task 1 – Export and one-shot override

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
set -euo pipefail

export REBASH_SESSION='session-value'
printenv REBASH_SESSION | tee export-session.txt
REBASH_ONESHOT='oneshot-value' printenv REBASH_ONESHOT | tee oneshot.txt
# Parent shell should not keep the oneshot-only assignment unless exported beforehand
if printenv REBASH_ONESHOT >/dev/null 2>&1; then
  echo 'unexpected: oneshot leaked' >&2
  exit 1
fi
echo 'oneshot-not-in-parent=ok' | tee oneshot-scope.txt
test "$(cat export-session.txt)" = 'session-value'
```

!!! example "Expected output"
    exported value persists in the shell; oneshot value does not remain in the parent environment.


#### Task 2 – `/etc/profile.d` drop-in (login shell)

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
set -euo pipefail

sudo tee /etc/profile.d/rebash-lab-env.sh >/dev/null << 'EOF'
# REBASH lab-env — remove in cleanup
export REBASH_LAB_ENV=1
EOF
sudo chmod 644 /etc/profile.d/rebash-lab-env.sh

# Bash login shell should source profile.d
bash --login -c 'printenv REBASH_LAB_ENV' | tee profile-d-login.txt
test "$(cat profile-d-login.txt)" = '1'

# Non-login non-interactive may not see it — capture for learning
bash -c 'printenv REBASH_LAB_ENV || true' | tee profile-d-nologin.txt || true
```

!!! example "Expected output"
    `profile-d-login.txt` is `1`. Non-login output may be empty — that difference is the lesson.


#### Task 3 – systemd Environment= + evidence

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
set -euo pipefail

sudo tee /etc/systemd/system/rebash-lab-env.service >/dev/null << 'EOF'
[Unit]
Description=REBASH lab env printer
[Service]
Type=oneshot
Environment=APP_ENV=lab
Environment=REBASH_UNIT=1
ExecStart=/usr/bin/bash -c 'printenv APP_ENV REBASH_UNIT > /var/tmp/rebash-lab-env.out'
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl start rebash-lab-env.service
sudo cat /var/tmp/rebash-lab-env.out | tee unit-env.txt
grep -F 'lab' unit-env.txt
grep -F '1' unit-env.txt

tar -czf env-evidence.tgz \
  shell.txt path.txt home-user.txt \
  export-session.txt oneshot.txt oneshot-scope.txt \
  profile-d-login.txt profile-d-nologin.txt unit-env.txt
ls -l env-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    `unit-env.txt` contains `lab` and `1`; evidence archive exists.


### Validation steps

- [ ] You can explain export vs one-shot assignment
- [ ] Login shell shows `REBASH_LAB_ENV=1`
- [ ] systemd oneshot wrote `/var/tmp/rebash-lab-env.out`
- [ ] `env-evidence.tgz` exists under `~/rebash-linux/lab-env`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| profile.d value missing | Not a login shell | Use `bash --login -c …` or SSH login |
| Unit file ignored | No daemon-reload | `sudo systemctl daemon-reload` |
| `printenv` empty | Typo / not exported | Check `export` and spelling |
| Secrets visible in `systemctl show` | Env on unit | Prefer locked-down `EnvironmentFile=` with mode `0600` |

### Challenge exercise

Create `/etc/profile.d/rebash-lab-path.sh` that **prepends** `$HOME/rebash-linux/lab-env/bin` to `PATH` if that directory exists. Create a tiny `bin/hello-rebash` script, prove `bash --login -c 'command -v hello-rebash'` works, and save output to `path-prepend.txt`.

### Learning outcomes

- Used export and one-shot environment overrides
- Installed a system `profile.d` script and proved login behaviour
- Passed variables into a systemd oneshot
- Saved environment evidence for onboarding docs

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-env
set -euo pipefail
sudo rm -f /etc/profile.d/rebash-lab-env.sh /etc/profile.d/rebash-lab-path.sh
sudo systemctl stop rebash-lab-env.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/rebash-lab-env.service
sudo systemctl daemon-reload
sudo rm -f /var/tmp/rebash-lab-env.out
# Keep env-evidence.tgz if you want it
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab-env/` with evidence files
- [ ] You know cron/systemd may not share your interactive PATH
- [ ] You avoid putting secrets in world-readable profile scripts
- [ ] You can choose shell export vs unit Environment= appropriately

## Code Walkthrough

Ops configuration order:

1. Inspect current env (`printenv`)  
2. Prefer unit `Environment=` / `EnvironmentFile=` for services  
3. Use `profile.d` for human login defaults  
4. Set variables inside cron entries when needed  
5. Redact secrets from tickets and debug dumps  

## Security Considerations

- Do not commit secrets into `profile.d` or unit files in git without encryption/sealed secrets  
- Mode `0600` for environment files with credentials  
- Remember `systemctl show` can expose unit environment  
- Clear sensitive variables from shells you leave open  
- Prefer secret managers for production credentials  

## Common Mistakes

!!! warning "Fixing cron by only editing `.bashrc`"
    Cron does not read `.bashrc` by default. **Fix:** set `PATH=` and variables in the crontab or call a wrapper script.

!!! warning "Assuming every `bash -c` is a login shell"
    `/etc/profile.d` may not run. **Fix:** test with `bash --login -c` or document the shell type.

!!! warning "Exporting secrets in world-readable scripts"
    Any local user can read them. **Fix:** restricted files, secret stores, least privilege.

!!! warning "Appending PATH forever in nested shells"
    PATH grows duplicates. **Fix:** idempotent path helpers; prepend only if missing.

## Best Practices

- Document required variables for each app  
- Use systemd environment for services, not ad-hoc SSH exports  
- Keep `profile.d` scripts tiny and idempotent  
- Quote variables (`"$VAR"`) in scripts  
- Continue Bash depth in the Shell track  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Command not found in cron | Short PATH | Set full paths / PATH in crontab |
| Variable missing in service | Not in unit env | `Environment=` / `EnvironmentFile=` |
| profile.d not applied | Non-login shell | Use login shell or user systemd |
| Wrong value wins | Multiple exports | Trace order: unit vs shell vs script |
| Secret leaked in process list | Env on command line | Prefer files with tight modes |

## Summary

Environment variables configure shells and services. Know where they are set (shell, profile.d, systemd, cron), prove inheritance with login vs non-login tests, and keep secrets out of world-readable places. Next filesystem work: [Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md). For scripting depth, see the [Shell](../shell/index.md) track.

## Interview Questions

**1. What does `export` do in Bash?**

??? success "Reveal answer"
    `export` marks a shell variable for inclusion in the environment of **child processes**. Without export, a variable may exist in the shell but not be visible to commands it starts. `printenv NAME` is a quick check.

**2. Why can a script fail in cron but work in your SSH session?**

??? success "Reveal answer"
    Cron starts with a **minimal environment**, especially a short `PATH`, and does not load your interactive `.bashrc` the way you expect. Use absolute paths, set variables in the crontab, or call a wrapper that prepares the environment.

**3. Where should a systemd service get its configuration variables?**

??? success "Reveal answer"
    Prefer `Environment=` or `EnvironmentFile=` on the unit (with tight file permissions for secrets). Relying on an admin’s interactive shell exports is not reproducible.

**4. What is the difference between a login shell and a non-login shell for `profile.d`?**

??? success "Reveal answer"
    Login shells typically read `/etc/profile` and `/etc/profile.d/*.sh`. Non-login interactive shells often read `~/.bashrc` instead. That is why a `profile.d` variable can appear over SSH login but not in `bash -c` tests.

**5. How can environment variables become a security problem?**

??? success "Reveal answer"
    Secrets in env can appear in logs, core dumps, `systemctl show`, or child process environments. Prefer secret stores and locked-down environment files; never put production passwords in world-readable `profile.d` scripts.

**6. How do you run one command with a temporary variable without exporting it permanently?**

??? success "Reveal answer"
    Use a one-shot prefix: `VAR=value command args`. The assignment applies to that command’s environment. Confirm the parent shell did not keep it unless you also exported it.

**7. How does this topic connect to CI pipelines?**

??? success "Reveal answer"
    CI injects environment variables for build settings and credentials. Pipelines fail when required variables are missing or when secrets are echoed. Treat CI env like production config: documented, least privilege, and not printed.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Essential Linux Commands](essential-linux-commands.md) *(previous)*
- [Paths, Links, Mounts, and Inodes](filesystem-paths-links-mounts-and-inodes.md) *(next)*
- [Shell Scripting track](../shell/index.md) *(deeper Bash)*

## References

- [`environ(7)`](https://manpages.ubuntu.com/manpages/jammy/en/man7/environ.7.html) — environment overview  
- [systemd environment](https://www.freedesktop.org/software/systemd/man/systemd.exec.html) — `Environment=` / `EnvironmentFile=`  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
