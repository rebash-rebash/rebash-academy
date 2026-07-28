---
title: Shell Scripting Fundamentals
description: Write production Bash scripts with strict mode, control flow, functions, and a real backup automation example.
difficulty: intermediate
estimated_time: "60 min"
author: Shaik Basha
last_updated: "2026-07-28"
category: linux
tags:
  - linux
  - shell-scripting
  - bash
  - automation
prerequisites:
  - Text Processing with grep, sed, and awk
  - Essential Linux Commands
comments: false
---

# Shell Scripting Fundamentals

## Overview

Shell scripts are the glue of Linux operations: cron jobs, CI/CD hooks, deployment runbooks, and on-call remediation all start as Bash. A well-written script is idempotent, fails loudly on error, and logs what it did — a poorly written one silently corrupts data at 3 AM.

This tutorial takes you from `#!/bin/bash` to a **real backup script** you could run in production (with minor path adjustments). You will learn strict error handling with `set -euo pipefail`, proper variable quoting, conditionals, loops, functions, and how to structure scripts that other engineers can maintain.

This is **Module 4, Tutorial 10** in the REBASH Academy Linux series.

## Prerequisites

- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) — pipes and command substitution
- [Essential Linux Commands](essential-linux-commands.md) — file permissions, `chmod`, redirection
- Bash 4.0+ (default on modern Linux; macOS ships Bash 3.2 — use Linux VM for full compatibility)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Enable and explain `set -euo pipefail` in production scripts
- [ ] Use quoted variables, command substitution, and `$(( ))` arithmetic safely
- [ ] Write `if`, `elif`, `else`, and `case` statements for branching logic
- [ ] Iterate with `for`, `while`, and process substitution over files and command output
- [ ] Define reusable functions with local variables and return codes
- [ ] Build a timestamped backup script with logging, validation, and retention
- [ ] Debug scripts with `bash -x` and meaningful exit codes

## Architecture

This topic is primarily procedural. The mental model is a straight line from inputs (commands, config files, or manifests) to observable system state — verify each change with the validation steps later in this tutorial.

## Theory

### Script anatomy

Every production Bash script starts with:

```bash
#!/bin/bash
set -euo pipefail
```

| Flag | Effect |
|------|--------|
| `-e` | Exit immediately if any command returns non-zero |
| `-u` | Treat unset variables as errors |
| `-o pipefail` | Pipeline fails if **any** command in the pipe fails (not just the last) |

Without `pipefail`, `grep pattern missing.log | wc -l` returns 0 even when grep finds nothing and exits 1 — a silent failure in monitoring scripts.

Add `IFS=$'\n\t'` when splitting on whitespace is dangerous, and use a `trap` for cleanup on exit (shown in the backup script below).

### Variables and quoting

| Form | Use |
|------|-----|
| `$VAR` | Unquoted — word-splits and glob-expands; avoid |
| `"$VAR"` | Safe for strings with spaces |
| `'$VAR'` | Literal — no expansion |
| `$(command)` | Command substitution (preferred over backticks) |
| `${VAR:-default}` | Use default if unset or empty |
| `${VAR:?message}` | Fatal error if unset or empty |

Always quote variable expansions unless you explicitly need word splitting.

### Exit codes and `return`

- `$?` holds the exit code of the last command (0 = success).
- Scripts should `exit 0` on success and non-zero on failure.
- Functions use `return N` (0–255); use `return 1` for boolean false in checks.

### Conditionals — `if` and `case`

**File tests:**

| Test | True when |
|------|-----------|
| `-f FILE` | Regular file exists |
| `-d DIR` | Directory exists |
| `-r FILE` | Readable |
| `-x FILE` | Executable |
| `-z STRING` | String is empty |
| `-n STRING` | String is non-empty |

**Numeric comparison:** use `-eq`, `-ne`, `-lt`, `-gt` inside `[ ]` or `(( ))` for arithmetic.

**case** is ideal for matching script arguments or service states:

```bash
case "$1" in
  start|restart) start_service ;;
  stop)          stop_service ;;
  *)             echo "Usage: $0 {start|stop|restart}"; exit 1 ;;
esac
```

### Loops

- `for item in "$@"; do` — iterate arguments safely (always quote `"$@"`).
- `for f in /path/*.log; do` — glob; use `nullglob` or check `[ -e "$f" ]` when no matches.
- `while IFS= read -r line; do` — read lines without stripping backslashes or breaking on spaces.
- `while read -r line; do ... done < file` — process file line-by-line.

### Functions

Functions improve readability and testability:

```bash
log() { printf '[%s] %s\n' "$(date -Iseconds)" "$*"; }

backup_dir() {
  local src="$1" dest="$2"
  tar -czf "$dest" -C "$(dirname "$src")" "$(basename "$src")"
}
```

Use `local` for function-scoped variables to avoid polluting the global namespace.

## Hands-on Lab

```bash
mkdir -p ~/lab/scripts ~/lab/backup-src ~/lab/backup-dest
echo "config v1" > ~/lab/backup-src/app.conf
echo "data line" > ~/lab/backup-src/data.txt
```

### Step 1 – Hello script with strict mode

```bash
cat > ~/lab/scripts/hello.sh << 'EOF'
#!/bin/bash
set -euo pipefail

readonly GREETING="${1:-World}"

echo "Hello, ${GREETING}!"
echo "Running as: $(whoami) on $(hostname -s)"
echo "Shell: ${BASH_VERSION}"
EOF
chmod +x ~/lab/scripts/hello.sh
~/lab/scripts/hello.sh REBASH
```

**Expected output:**

```text
Hello, REBASH!
Running as: youruser on yourhost
Shell: 5.2.15(1)-release
```

Run without args to test default:

```bash
~/lab/scripts/hello.sh
```

**Expected output:** `Hello, World!`

### Step 2 – Variables, exit codes, and `$?`

```bash
cat > ~/lab/scripts/check_file.sh << 'EOF'
#!/bin/bash
set -euo pipefail

FILE="${1:?Usage: check_file.sh FILE}"

if [[ -f "$FILE" ]]; then
  echo "OK: $FILE exists ($(stat -c%s "$FILE" 2>/dev/null || stat -f%z "$FILE") bytes)"
  exit 0
else
  echo "ERROR: $FILE not found" >&2
  exit 1
fi
EOF
chmod +x ~/lab/scripts/check_file.sh
~/lab/scripts/check_file.sh ~/lab/backup-src/app.conf
echo "Exit code: $?"
~/lab/scripts/check_file.sh /nonexistent 2>/dev/null || echo "Exit code: $?"
```

**Expected output:** OK message with byte count, exit 0; then error message, exit 1.

### Step 3 – if/elif/else and disk threshold

```bash
cat > ~/lab/scripts/disk_alert.sh << 'EOF'
#!/bin/bash
set -euo pipefail

THRESHOLD="${1:-80}"
MOUNT="${2:-/}"

USAGE=$(df "$MOUNT" | awk 'NR==2 {gsub(/%/,"",$5); print $5}')

if (( USAGE >= 90 )); then
  LEVEL="CRITICAL"
elif (( USAGE >= THRESHOLD )); then
  LEVEL="WARNING"
else
  LEVEL="OK"
fi

echo "${LEVEL}: ${MOUNT} is ${USAGE}% full (threshold: ${THRESHOLD}%)"
EOF
chmod +x ~/lab/scripts/disk_alert.sh
~/lab/scripts/disk_alert.sh 80 /
```

**Expected output:** `OK: / is NN% full (threshold: 80%)` (or WARNING/CRITICAL if disk is high).

### Step 4 – case statement for actions

```bash
cat > ~/lab/scripts/service_action.sh << 'EOF'
#!/bin/bash
set -euo pipefail

ACTION="${1:?Usage: service_action.sh {status|ping}}"

case "$ACTION" in
  status)
    uptime
    free -h | head -2
    ;;
  ping)
    ping -c 2 127.0.0.1
    ;;
  *)
    echo "Unknown action: $ACTION" >&2
    exit 1
    ;;
esac
EOF
chmod +x ~/lab/scripts/service_action.sh
~/lab/scripts/service_action.sh status
```

**Expected output:** uptime line and memory summary.

### Step 5 – for and while loops

```bash
cat > ~/lab/scripts/inventory.sh << 'EOF'
#!/bin/bash
set -euo pipefail

echo "=== Files in backup-src ==="
for f in ~/lab/backup-src/*; do
  [[ -f "$f" ]] && printf '  %-20s %s bytes\n' "$(basename "$f")" "$(wc -c < "$f")"
done

echo ""
echo "=== Lines in app.conf ==="
while IFS= read -r line; do
  echo "  > $line"
done < ~/lab/backup-src/app.conf
EOF
chmod +x ~/lab/scripts/inventory.sh
~/lab/scripts/inventory.sh
```

**Expected output:** file listing with sizes, then each line of `app.conf` prefixed with `>`.

### Step 6 – Functions with local variables

```bash
cat > ~/lab/scripts/math.sh << 'EOF'
#!/bin/bash
set -euo pipefail

add() {
  local a="$1" b="$2"
  echo $(( a + b ))
}

multiply() {
  local a="$1" b="$2"
  echo $(( a * b ))
}

result=$(add 10 5)
product=$(multiply "$result" 3)
echo "add(10,5) = $result; multiply($result,3) = $product"
EOF
chmod +x ~/lab/scripts/math.sh
~/lab/scripts/math.sh
```

**Expected output:** `add(10,5) = 15; multiply(15,3) = 45`

### Step 7 – Demonstrate pipefail

```bash
bash -c 'set -eo pipefail; false | true; echo unreachable' 2>/dev/null || echo "pipefail caught the failure"
bash -c 'set -e; false | true; echo silent success' && echo "Without pipefail: script continued"
```

**Expected output:** first line prints "pipefail caught the failure"; second prints "Without pipefail: script continued".

### Step 8 – Production-style backup script

```bash
cat > ~/lab/scripts/backup.sh << 'EOF'
#!/bin/bash
set -euo pipefail

readonly SRC="${1:-$HOME/lab/backup-src}"
readonly DEST="${2:-$HOME/lab/backup-dest}"
readonly RETAIN_DAYS="${3:-7}"
readonly TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
readonly ARCHIVE="${DEST}/backup_${TIMESTAMP}.tar.gz"
readonly LOG="${DEST}/backup.log"

log() { printf '[%s] %s\n' "$(date -Iseconds)" "$*" | tee -a "$LOG"; }

cleanup() {
  local exit_code=$?
  if (( exit_code != 0 )); then
    log "ERROR: backup failed with exit code $exit_code"
  fi
}
trap cleanup EXIT

validate() {
  [[ -d "$SRC" ]] || { log "Source not found: $SRC"; exit 1; }
  mkdir -p "$DEST"
}

prune_old() {
  find "$DEST" -name 'backup_*.tar.gz' -mtime +"$RETAIN_DAYS" -delete
  log "Pruned archives older than ${RETAIN_DAYS} days"
}

main() {
  validate
  log "Starting backup: $SRC -> $ARCHIVE"
  tar -czf "$ARCHIVE" -C "$(dirname "$SRC")" "$(basename "$SRC")"
  log "Created $(du -h "$ARCHIVE" | cut -f1) archive"
  prune_old
  log "Backup complete"
}

main
EOF
chmod +x ~/lab/scripts/backup.sh
~/lab/scripts/backup.sh
ls -lh ~/lab/backup-dest/
tail -3 ~/lab/backup-dest/backup.log
```

**Expected output:** log lines showing start, archive size, prune, and complete; a `backup_YYYYMMDD_HHMMSS.tar.gz` file in `~/lab/backup-dest/`.

Verify the archive:

```bash
tar -tzf ~/lab/backup-dest/backup_*.tar.gz | head -5
```

**Expected output:** paths like `backup-src/app.conf`, `backup-src/data.txt`.

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
| `#!/bin/bash` | Shebang — run script with Bash |
| `set -euo pipefail` | Strict mode for production scripts |
| `readonly VAR=value` | Prevent accidental reassignment |
| `"${VAR:-default}"` | Parameter expansion with default |
| `"${VAR:?error msg}"` | Fail if variable unset/empty |
| `$(command)` | Capture command output |
| `$(( expression ))` | Integer arithmetic |
| `[ -f FILE ]` / `[[ -f FILE ]]` | Test if file exists |
| `test -d DIR` | Test if directory exists |
| `exit N` | Exit script with code N |
| `return N` | Exit function with code N |
| `local var=value` | Function-scoped variable |
| `trap 'cmd' EXIT` | Run command on script exit |
| `bash -x script.sh` | Trace execution (debug) |
| `shellcheck script.sh` | Static analysis for common bugs |

## Code

The backup script from Step 8 is the primary production example. Extend it with argument parsing:

```bash
#!/bin/bash
set -euo pipefail

usage() {
  cat <<USAGE
Usage: $(basename "$0") [-s SOURCE] [-d DEST] [-r RETAIN_DAYS]
  -s  Source directory (default: ~/lab/backup-src)
  -d  Destination directory (default: ~/lab/backup-dest)
  -r  Days to retain archives (default: 7)
USAGE
}

SRC="$HOME/lab/backup-src"
DEST="$HOME/lab/backup-dest"
RETAIN_DAYS=7

while getopts ':s:d:r:h' opt; do
  case "$opt" in
    s) SRC="$OPTARG" ;;
    d) DEST="$OPTARG" ;;
    r) RETAIN_DAYS="$OPTARG" ;;
    h) usage; exit 0 ;;
    *) usage; exit 1 ;;
  esac
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

!!! warning "Unquoted variables break on filenames with spaces"
    `rm $file` fails on `my file.txt`. Always use `"$file"`.

!!! warning "Missing pipefail masks upstream failures"
    Pipelines in strict mode need `set -o pipefail` or errors in `grep`, `curl`, and `tar` go unnoticed.

!!! warning "Using `$*` instead of `$@` in loops"
    `"$@"` preserves individual arguments; `"$*"` merges them into one string.

!!! warning "Running as root without checking paths"
    A backup script with `rm -rf ${DIR}/*` and an empty `$DIR` is catastrophic. Validate paths and use `readonly`.

## Best Practices

!!! tip "Start every script with strict mode"
    `set -euo pipefail` catches 80% of beginner bugs. Add `IFS=$'\n\t'` for data-processing scripts.

!!! tip "Log to stderr, data to stdout"
    `echo "info" >&2` keeps stdout clean for piping. Use structured log prefixes with timestamps.

!!! tip "Use meaningful exit codes"
    Document codes in script header: `0=success, 1=usage error, 2=source missing, 3=archive failed`.

!!! tip "Run shellcheck before committing"
    Install with `apt install shellcheck` or `brew install shellcheck`. Fix warnings unless you have a documented reason not to.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `unbound variable` with `-u` | Variable never set | Use `${VAR:-default}` or set before use |
| Script exits silently mid-run | `set -e` on expected non-zero | Use `if ! cmd; then` or `cmd \|\| true` when failure is OK |
| `[: integer expression expected` | String compared with `-gt` | Use `(( ))` for numbers or validate input |
| `bad substitution` on macOS | Bash 3.2 lacks `${var,,}` | Use Linux Bash 4+ or portable alternatives |
| Loop runs once with spaces | Unquoted `$@` or `$*` | Use `for arg in "$@"; do` |
| Permission denied on execution | Missing `+x` bit | Run `chmod +x script.sh` |
| `tar: Removing leading '/'` warning | Absolute paths in archive | Use `-C` to change directory before archiving |

## Summary

- Production Bash begins with `#!/bin/bash` and `set -euo pipefail` — fail fast, catch unset vars, honor pipeline errors.
- Quote all variable expansions; use `"$@"` for arguments and `"${VAR:-default}"` for optional config.
- Branch with `if`/`case`, iterate with `for`/`while`, and encapsulate logic in functions with `local` variables.
- The backup script demonstrates validation, logging, `trap`, retention, and idempotent directory creation — patterns you will reuse in cron jobs and deploy scripts.
- Debug with `bash -x` and validate with `shellcheck` before shipping to production.

## Interview Questions

1. What does `set -euo pipefail` do, and why is each flag important in production scripts?
2. What is the difference between `$*` and `$@` inside double quotes?
3. How do you safely check if a variable is unset before using it?
4. Explain why `if [ "$USAGE" -gt 80 ]` can fail when `USAGE` is empty, and how `-u` helps.
5. What is the purpose of `trap cleanup EXIT` in a backup script?
6. How would you iterate over all `.log` files in a directory, including paths with spaces?
7. What exit code should a script return on success? What range is available?
8. Why is `local` important inside functions?
9. How does `pipefail` change the behaviour of `cmd1 | cmd2` when `cmd1` fails?
10. Walk through how you would add a `--dry-run` flag to the backup script without executing `tar`.

## Related Tutorials

- [Linux – Category Overview](index.md)
- [Text Processing with grep, sed, and awk](text-processing-grep-sed-awk.md) *(previous)*
- [SSH and Remote Administration](ssh-remote-administration.md) *(next)*
- [Cron and Task Scheduling](cron-and-task-scheduling.md)
- [Learning Paths – DevOps Engineer](../learning-paths/index.md)
- Cheat sheet: [Linux Cheat Sheet](../cheatsheets/linux.md)
- Interview prep: [Linux Interview Prep](../interview/linux.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html)
- [ShellCheck wiki](https://www.shellcheck.net/wiki/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [REBASH Academy – Linux Overview](index.md)
