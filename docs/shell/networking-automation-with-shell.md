---
title: "Networking Automation with Shell"
description: "Automate connectivity checks and transfers with ping, curl, wget, nc, dig, SSH, SCP, and rsync."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - curl
  - ssh
  - rsync
  - dns
prerequisites:
  - Linux Administration Automation
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Networking Automation with Shell

## Overview

Health checks, artifact pulls, and remote ops all start as shell networking. Timeouts and exit codes matter more than clever curl flags.

This is **Tutorial 13** in **Module 13: Networking Automation** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Linux Administration Automation
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Networking Automation with Shell” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Networking Automation with Shell](../assets/images/shell-networking-auto.svg)

## Theory

### ping, nc, dig

`ping -c 3 host` for ICMP reachability (may be blocked). `nc -zv host port` for TCP probes. `dig +short` / `getent hosts` for DNS — prefer checking DNS before blaming the app.

### curl and wget

`curl -fsSL --connect-timeout 5 --max-time 30` for APIs and downloads (`-f` fails on HTTP errors). `wget` remains common for simple file fetches. Always set timeouts.

### SSH, SCP, rsync

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 host 'uname -a'
rsync -az --delete src/ host:dst/
```

Use `BatchMode=yes` in automation so password prompts fail fast. Prefer `rsync` over `scp` for trees and resumes.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab13 && cd ~/rebash-shell/lab13
```

**Focus:** curl with timeouts; dig/nc probes; SSH BatchMode; rsync dry-run

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab13 networking-automation-with-shell on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – Network probes

```bash
cat > net.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
dig +short example.com | head | tee dns.txt || getent hosts example.com | tee dns.txt
curl -fsS --connect-timeout 5 --max-time 15 -o /dev/null -w 'http=%{http_code}\n' https://example.com
# local TCP smoke (may fail if nothing listens — ok):
nc -z -w 2 127.0.0.1 22 && echo 'ssh port open' || echo 'ssh port closed'
echo 'rsync dry-run local:'
mkdir -p src dst
echo x > src/f
rsync -an src/ dst/
EOF
chmod +x net.sh
./net.sh
```

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab13/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Networking Automation with Shell** always combines:

1. A clear shebang (`#!/usr/bin/env bash`)
2. Strict mode near the top (`set -euo pipefail`) from Module 2 onward
3. Quoted expansions and explicit tests
4. Functions with `local` for reusable behaviour
5. Documented exit codes and stderr logging

Keep scripts short enough to review in a single merge request. When logic grows (complex JSON APIs, heavy state), hand off to Python and keep Bash as the launcher.

## Security Considerations

- Treat all external input (args, files, env) as untrusted until validated
- Never log secrets; prefer masked CI variables and secret stores
- Prefer least privilege — do not require root for file-local tasks
- Avoid `eval` and unquoted expansions in destructive commands
- Validate paths stay under an allow-listed root before `rm` or overwrite

## Common Mistakes

!!! warning "Skipping strict mode"
    Cron and CI hide failures that an interactive terminal would show. **Fix:** start with `set -euo pipefail` from Module 2 onward.

!!! warning "Unquoted path expansions"
    Spaces and globs rewrite your command line. **Fix:** always `"$path"` / `"$@"`.

!!! warning "Assuming interactive PATH"
    Aliases and fancy PATH entries disappear under schedulers. **Fix:** set `PATH` or use absolute paths.

## Best Practices

- One purpose per script; compose with functions or small binaries
- Log to stderr; reserve stdout for data or RESULT lines
- Idempotent behaviour where scheduling may overlap
- Pair every new script with a failing-path test you actually run
- Run ShellCheck in CI before merging automation

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Works in terminal, fails in cron | PATH / cwd / env | Fingerprint env; set PATH |
| `unbound variable` | `set -u` | Provide defaults or export vars |
| Pipeline “succeeds” incorrectly | Missing `pipefail` | `set -o pipefail` |
| `[[` unexpected operator | Running under `sh`/dash | Fix shebang to Bash |

## Summary

**Networking Automation with Shell** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

## Interview Questions

1. How does this topic show up in production Linux administration or CI?
2. What failure mode appears if you ignore quoting or strict mode here?
3. How would you test this behaviour under a minimal cron-like environment?
4. When would you move this logic out of Bash into Python or another tool?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Unquoted expansions and missing `pipefail` create silent or partial failures — especially under cron — that look healthy in monitoring until data is wrong.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Category Overview](index.md)
- [Linux Administration Automation](linux-admin-automation.md) *(previous)*
- [JSON and YAML with jq and yq](json-and-yaml-with-jq-yq.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
