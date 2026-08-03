---
title: "Lab — Shell Ops Script Hardening"
description: "Turn an unsafe Bash job into a production-ready wrapper with strict mode, quoting, flock, traps, logging, and clear exit codes."
difficulty: intermediate
estimated_time: "50 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
  - hardening
comments: false
---

# Lab — Shell Ops Script Hardening

## Lab Overview

**Purpose:** Practise the Shell Scripting track under pressure — fix a deliberately unsafe ops script until it is schedulable.

**Scenario:** A nightly “cleanup” job has been emailing false successes, deleting the wrong paths when names contain spaces, and overlapping itself when cron drifts.

**Expected outcome:** A hardened script with `set -euo pipefail`, quoted paths, `mktemp`+`trap`, `flock`, stderr logging, and documented exit codes.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

On-call inherited `cleanup.sh` from a paste in Slack. It “works on my machine”, uses unquoted `rm -rf $TARGET`, ignores pipeline failures, and has no lock. You must ship a version safe for cron on a shared bastion.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Reproduce failures from unquoted expansions and missing `pipefail`
- [ ] Add strict mode, logging helpers, and an exit taxonomy
- [ ] Protect the job with `flock` and clean up with `trap`
- [ ] Validate success and failure paths before scheduling

## Prerequisites

### Knowledge

- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)
- [Process Automation — Signals and Traps](../shell/process-automation-signals-and-traps.md)
- [Production Shell Scripting](../shell/production-shell-scripting.md)
- [Troubleshooting Shell Scripts](../shell/troubleshooting-shell-scripts.md)

### Software

| Tool | Notes |
|------|--------|
| Bash 4.2+ | `bash --version` |
| flock | util-linux (standard on Linux) |
| mktemp | coreutils |

**Estimated cost:** £0.

## Architecture

![Unsafe cron job hardened with strict mode, lock, trap, and logging](../assets/images/lab-shell-ops-script-hardening.svg)

## Environment

Any Linux host or WSL2. Work under `~/rebash-lab-shell`.

## Initial State

```bash
mkdir -p ~/rebash-lab-shell/{inbox,safe-target}
cd ~/rebash-lab-shell
printf 'x\n' > "inbox/my file.txt"
printf 'y\n' > inbox/keep.txt
```

### Broken script (starting point)

Create `cleanup-broken.sh`:

```bash
#!/bin/bash
TARGET=$1
grep ERROR /var/log/syslog | wc -l
rm -rf $TARGET/*
echo SUCCESS
```

Run:

```bash
chmod +x cleanup-broken.sh
```


## Task

### Step 1 – Reproduce the quoting bug

```bash
# DANGEROUS demo only inside the lab tree:
./cleanup-broken.sh ~/rebash-lab-shell/inbox || true
ls -la inbox || true
```

Recreate files if needed. Observe how spaces break the command.

### Step 2 – Rewrite with strict mode and quotes

Create `cleanup.sh`:

- `#!/usr/bin/env bash` + `set -euo pipefail`
- Require a target under `$HOME/rebash-lab-shell`
- Refuse paths outside that prefix (`realpath` + prefix check)
- Quote all expansions
- Log to stderr; print `RESULT status=...` on stdout

### Step 3 – Add temp dir, trap, and flock

- `mktemp -d` for staging if needed
- `trap cleanup EXIT INT TERM`
- `flock -n` on `~/rebash-lab-shell/cleanup.lock` (exit 0 if already running)

### Step 4 – Exit taxonomy

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage / invalid path |
| 3 | Lock not acquired (optional alternate: 0) |
| 4 | Operational failure |

### Step 5 – Validate

```bash
./cleanup.sh                           # expect usage -> 2
./cleanup.sh "$HOME/rebash-lab-shell/safe-target"
./cleanup.sh /tmp || echo "refused exit=$?"
```

Run two copies in parallel to confirm locking.

## Validation

- [ ] Broken behaviour understood (spaces / missing pipefail)
- [ ] Hardened script uses strict mode and quoted paths
- [ ] Prefix check blocks `/tmp`
- [ ] Lock prevents overlap
- [ ] Trap removes temp dirs

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| flock missing | Install util-linux / use Linux VM |
| realpath missing | `readlink -f` on some distros |
| trap not firing | Ensure `EXIT` is included |

## Cleanup

```bash
rm -rf ~/rebash-lab-shell
```

## Stretch Goals

- Emit a machine-readable `RESULT` line for CI
- Add `-v` verbose logging
- Wrap with a systemd oneshot unit sketch

## Related

- Track: [Shell Scripting](../shell/index.md)
- Tutorials: [Production Shell Scripting](../shell/production-shell-scripting.md), [Process Automation — Signals and Traps](../shell/process-automation-signals-and-traps.md), [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Lab: [Create a Linux Operations Toolkit](shell-linux-operations-toolkit.md)
