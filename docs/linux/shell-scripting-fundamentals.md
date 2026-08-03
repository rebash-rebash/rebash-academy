---
title: "Shell Scripting Fundamentals"
description: "Write safe Bash scripts for Linux ops — shebang, set -euo pipefail, arguments, exit codes — with an Ubuntu lab. Deeper curriculum lives in the Shell track."
difficulty: beginner
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: linux
technology: linux
module: "Module 2 · Command Line"
tags:
  - linux
  - shell
  - bash
  - scripting
prerequisites:
  - linux/essential-linux-commands
next:
  - linux/environment-variables-shell-config
related:
  - ../shell/index.md
interview: interview/linux
comments: false
---

# Shell Scripting Fundamentals

## Overview

A **shell script** is a text file of commands the shell runs in order. On Ubuntu servers, **Bash** scripts automate checks, backups, and small glue tasks between tools. This page teaches the **operations minimum**: shebang, safe modes (`set -euo pipefail`), arguments, exit codes, and readable output — enough to write trustworthy helpers on a Linux host.

The full Bash curriculum (functions, arrays, testing patterns, larger programs) lives in the [Shell Scripting](../shell/index.md) track. Use this tutorial when you need safe automation habits inside the Linux for Cloud & DevOps path. In the lab you will build a small host-check script that fails clearly, produces evidence, and exits with proper codes under `~/rebash-linux/lab-shell`.

In production, prefer idempotent scripts, absolute paths, logging, and code review — the same standards you apply to application code.

## Prerequisites

- [Essential Linux Commands](essential-linux-commands.md)
- A **practice Ubuntu 22.04/24.04 VM** with Bash
- Text editor or heredocs as shown

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write a Bash script with `#!/usr/bin/env bash` and `set -euo pipefail`
- [ ] Use positional arguments and validate input
- [ ] Return meaningful exit codes (`0` success, non-zero failure)
- [ ] Redirect useful output to a log file for tickets
- [ ] Pack evidence under `~/rebash-linux/lab-shell`

## Architecture

Scripts orchestrate existing Linux tools; safe defaults stop silent failures from propagating in automation and CI.

![Architecture diagram for shell CLI workflow](../assets/excalidraw/linux-cli-workflow.svg)

## Theory

### What it is

| Piece | Role |
|-------|------|
| Shebang | Which interpreter runs the file |
| `set -e` | Exit on command failure |
| `set -u` | Exit on unset variables |
| `set -o pipefail` | Pipeline fails if any stage fails |
| Exit code | `0` ok; non-zero means failure to callers |

``` {.bash .ra-terminal title="Terminal"}
#!/usr/bin/env bash
set -euo pipefail
echo "hello"
```

### Why it matters

Scripts without `set -u` hide typos. Pipelines without `pipefail` can “succeed” after a failed `grep`. Cron and CI only see exit codes — silent partial failure is worse than a loud error.

### How it works

1. Create an executable file with a shebang  
2. Enable safe modes  
3. Parse arguments (`$1`, `$#`)  
4. Run commands; write logs  
5. `exit 0` or `exit 1` deliberately  

| Pattern | Prefer |
|---------|--------|
| Paths | Absolute paths in automation |
| Output | Log file + concise stdout |
| Failure | Non-zero exit + message on stderr |

### Common pitfalls

- Running scripts with `sh` when they need Bash features.  
- Forgetting `chmod +x` or calling via `bash script.sh`.  
- Parsing `ls` output instead of globs/`find`.  
- Ignoring exit codes in CI.

## Hands-on Lab

### Objective

Write `hostcheck.sh` that validates an argument directory, checks disk free space and a writable probe file, logs results, and exits non-zero on failure — with evidence under `~/rebash-linux/lab-shell`.

### Prerequisites

- Bash on Ubuntu

### Lab environment

Workspace: `~/rebash-linux/lab-shell`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-linux/lab-shell && cd ~/rebash-linux/lab-shell
set -euo pipefail
bash --version | head -n 1 | tee bash-version.txt
```

!!! example "Expected output"
    Bash version line stored.


### Real-world scenario

On-call wants a tiny pre-deploy check on practice VMs: “can we write to the app directory, and is free space above a threshold?” You ship a script with safe Bash defaults and sample successful/failed runs for the runbook.

### Step-by-step tasks

#### Task 1 – Create `hostcheck.sh`

```bash title="hostcheck.sh"
cd ~/rebash-linux/lab-shell
set -euo pipefail

cat > hostcheck.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <directory> <min_free_mb>" >&2
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

TARGET_DIR=$1
MIN_FREE_MB=$2
LOG=${HOSTCHECK_LOG:-./hostcheck.log}

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "ERROR: not a directory: $TARGET_DIR" >&2
  exit 1
fi

{
  echo "=== hostcheck $(date -Is) ==="
  echo "target=$TARGET_DIR min_free_mb=$MIN_FREE_MB"
  df -hT "$TARGET_DIR"
} | tee -a "$LOG"

# Free space in MB for the filesystem containing TARGET_DIR (POSIX df -P)
FREE_MB=$(df -Pm "$TARGET_DIR" | awk 'NR==2 {print $4}')
echo "free_mb=$FREE_MB" | tee -a "$LOG"

if [[ "$FREE_MB" -lt "$MIN_FREE_MB" ]]; then
  echo "ERROR: free ${FREE_MB}MB < required ${MIN_FREE_MB}MB" >&2
  exit 1
fi

PROBE="$TARGET_DIR/.rebash-hostcheck-probe"
echo ok > "$PROBE"
test -f "$PROBE"
rm -f "$PROBE"
echo "write_probe=ok" | tee -a "$LOG"
echo "RESULT=PASS" | tee -a "$LOG"
exit 0
EOF

chmod +x hostcheck.sh
test -x hostcheck.sh
```

!!! example "Expected output"
    executable `hostcheck.sh` exists.


#### Task 2 – Successful run

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-shell
set -euo pipefail

mkdir -p appdir
HOSTCHECK_LOG="$PWD/hostcheck-success.log" ./hostcheck.sh "$PWD/appdir" 50
test -f hostcheck-success.log
grep -F 'RESULT=PASS' hostcheck-success.log
grep -F 'write_probe=ok' hostcheck-success.log
```

!!! example "Expected output"
    script exits 0; success log contains `RESULT=PASS`.


#### Task 3 – Failure paths + evidence

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-shell
set -euo pipefail

# Bad arity → exit 2
set +e
./hostcheck.sh only-one-arg >arity.out 2>arity.err
EC=$?
set -e
echo "$EC" | tee arity-exit.txt
test "$EC" -eq 2

# Missing directory → exit 1
set +e
./hostcheck.sh "$PWD/does-not-exist" 50 >miss.out 2>miss.err
EC=$?
set -e
echo "$EC" | tee miss-exit.txt
test "$EC" -eq 1
grep -F 'not a directory' miss.err

# Impossible free-space requirement → exit 1
set +e
HOSTCHECK_LOG="$PWD/hostcheck-fail-space.log" ./hostcheck.sh "$PWD/appdir" 999999999 >space.out 2>space.err
EC=$?
set -e
echo "$EC" | tee space-exit.txt
test "$EC" -eq 1
grep -F 'ERROR: free' space.err

tar -czf shell-evidence.tgz \
  bash-version.txt hostcheck.sh \
  hostcheck-success.log arity-exit.txt arity.err \
  miss-exit.txt miss.err space-exit.txt space.err hostcheck-fail-space.log
ls -l shell-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    exit codes `2`, `1`, `1` for the three failure cases; evidence archive exists.


### Validation steps

- [ ] `hostcheck.sh` uses shebang and `set -euo pipefail`
- [ ] Success run writes `RESULT=PASS`
- [ ] Wrong usage exits `2`; missing dir exits `1`
- [ ] `shell-evidence.tgz` exists under `~/rebash-linux/lab-shell`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `./hostcheck.sh: Permission denied` | Not executable | `chmod +x hostcheck.sh` |
| `set: pipefail: invalid` | Running under `dash`/`sh` | Run with `bash` or `./` shebang Bash |
| `df -Pm` unsupported | Unusual df | Use GNU df on Ubuntu; adjust carefully |
| Probe cannot write | Permissions on directory | Fix ownership/mode on `appdir` |

### Challenge exercise

Extend `hostcheck.sh` with an optional third argument `--json` that prints a one-line JSON result to stdout (`{"result":"PASS","free_mb":N}`) while still appending the human log. Keep exit codes unchanged. Save a sample to `json-sample.txt`.

### Learning outcomes

- Built a safe Bash ops script with argument checks
- Used exit codes callers can trust
- Demonstrated pass and fail paths with logs
- Packed scripting evidence for a runbook

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-linux/lab-shell
set -euo pipefail
rm -rf appdir
# Keep hostcheck.sh and shell-evidence.tgz if you want them
```

## Validation

- [ ] Lab finished under `~/rebash-linux/lab-shell/` with evidence files
- [ ] You can explain why `set -euo pipefail` is a default for ops scripts
- [ ] You know exit code `0` vs non-zero for CI/cron
- [ ] You know where to go for deeper Bash ([Shell track](../shell/index.md))

## Code Walkthrough

Ops script checklist:

1. Shebang + safe `set`  
2. Validate arguments early  
3. Absolute paths  
4. Log + clear stderr errors  
5. Explicit exit codes  

## Security Considerations

- Do not pass secrets on the command line if `ps` can see them  
- Quote variables to avoid word-splitting surprises  
- Avoid `curl | sudo bash` patterns in production automation  
- Review scripts like code; least privilege when using sudo  
- Write logs without leaking credentials  

## Common Mistakes

!!! warning "Running Bash scripts with `sh`"
    Ubuntu’s `sh` is dash — many Bash features break. **Fix:** `./script.sh` with a Bash shebang, or `bash script.sh`.

!!! warning "No `pipefail`"
    `false | true` can still look successful. **Fix:** `set -o pipefail`.

!!! warning "Ignoring exit codes in CI"
    Later steps run on bad state. **Fix:** fail fast; check statuses.

!!! warning "Parsing `ls` for automation"
    Fragile output. **Fix:** globs, `find -print0`, or dedicated tools.

## Best Practices

- Keep scripts short and testable  
- Prefer systemd timers/units for long-running automation  
- Use shellcheck when available  
- Version scripts in git  
- Continue with the [Shell](../shell/index.md) track for mastery  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Unbound variable | `set -u` + typo | Fix name; provide default if intentional |
| Script stops early | `set -e` on expected fail | Guard with `if` / `|| true` only when safe |
| Wrong line endings | Windows CRLF | `dos2unix` or recreate with heredoc |
| Works manually, fails in cron | Env/PATH | Absolute paths; see env tutorial |
| Permission denied on probe | Directory mode | `chmod`/`chown` the target dir |

## Summary

Safe Bash defaults turn fragile command piles into reliable ops tools. Validate inputs, log clearly, exit correctly, then deepen skills in the Shell track. Related: [Environment Variables and Shell Configuration](environment-variables-shell-config.md).

## Interview Questions

**1. What does `set -euo pipefail` buy you in an ops script?**

??? success "Reveal answer"
    **`-e`** aborts on failed commands, **`-u`** catches unset variables, **`pipefail`** makes pipelines fail if any stage fails. Together they prevent many silent automation bugs that cron and CI would otherwise ignore.

**2. Why is a shebang of `#!/usr/bin/env bash` often preferred?**

??? success "Reveal answer"
    `env` locates `bash` on `PATH`, which helps across systems where Bash is not always in `/bin/bash`. Still test on your target distro. Never run Bash-only scripts with `sh`.

**3. How should a script signal failure to cron or CI?**

??? success "Reveal answer"
    Exit **non-zero** and print a clear message to **stderr**. Exit `0` only on real success. Callers and monitors key off the exit status more than log wording.

**4. What is wrong with parsing `ls` output in scripts?**

??? success "Reveal answer"
    `ls` formatting is for humans and breaks on spaces/newlines/odd filenames. Prefer globs, `find -print0`, or tools that offer machine-safe output.

**5. When should you automate with a shell script vs a systemd unit/timer?**

??? success "Reveal answer"
    Use a script for the logic; use **systemd** (or cron) to schedule, restart, and journal the run. Long-running daemons belong in units, not bare infinite loops in screen sessions.

**6. How do you keep scripts safe with untrusted input?**

??? success "Reveal answer"
    Validate arguments, quote expansions (`"$1"`), avoid `eval`, use `--` where commands support it, and do not concatenate raw user input into shell syntax. Least privilege for any sudo.

**7. Where do you go next after this fundamentals page?**

??? success "Reveal answer"
    The REBASH [Shell Scripting](../shell/index.md) track for deeper Bash, plus [Environment Variables and Shell Configuration](environment-variables-shell-config.md) for profile/systemd/cron environment behaviour that breaks many scripts in production.

## Related Tutorials

- [Linux for Cloud & DevOps – Overview](index.md)
- [Essential Linux Commands](essential-linux-commands.md) *(previous)*
- [Environment Variables and Shell Configuration](environment-variables-shell-config.md) *(next)*
- [Shell Scripting track](../shell/index.md) *(full Bash curriculum)*

## References

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — GNU Bash  
- [`bash(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/bash.1.html) — Ubuntu man-pages  
- Track index: [Linux for Cloud & DevOps Engineers](index.md)
