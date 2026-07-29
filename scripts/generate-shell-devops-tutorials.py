#!/usr/bin/env python3
"""Generate REBASH Academy Shell Scripting for DevOps Engineers tutorials 1–18 under docs/shell/."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "shell"
D2_DIR = ROOT / "docs" / "assets" / "d2"
IMG_DIR = ROOT / "docs" / "assets" / "images"
AUTHOR = "Shaik Basha"
DATE = "2026-07-29"

# (num, slug, title, module, difficulty, minutes, diagram, tag_extra, desc, overview, theory, lab_focus)
SPEC: list[tuple] = [
    (
        1,
        "shell-fundamentals-bash-vs-sh-and-execution",
        "Shell Fundamentals — Bash vs sh and Execution",
        "Module 1: Shell Fundamentals",
        "beginner",
        "40 min",
        "shell-execution-flow",
        ["fundamentals", "bash", "sh"],
        "What a shell is, Bash versus sh, interactive and login shells, and how environment variables shape DevOps automation.",
        "Every Linux admin and DevOps engineer lives in a shell. This tutorial builds the mental model for how Bash starts, what it inherits, and why cron and CI behave differently from your terminal.",
        """### What is a Shell?

A **shell** is a command interpreter: it reads text (interactive lines or a script), expands variables and globs, runs programs, and reports exit status. Common shells on Linux include **Bash** (Bourne Again SHell), **dash**, **zsh**, and **fish**.

For DevOps and platform work the shell is the glue between humans, schedulers, CI jobs, and system tools (`systemctl`, `curl`, `kubectl`, package managers).

### Bash vs sh

| Interpreter | Typical path | Notes |
|-------------|--------------|-------|
| Bash | `/bin/bash` or via `env` | Arrays, `[[ ]]`, process substitution, Bashisms |
| POSIX `sh` | `/bin/sh` | Often **dash** on Debian/Ubuntu — not Bash |
| zsh | `/bin/zsh` | Interactive favourite; avoid as script shebang for portability |

If the shebang is `#!/bin/sh`, write POSIX. Bash-only features fail under dash. Prefer `#!/usr/bin/env bash` for this course unless a tool requires POSIX `sh`.

### Shell Execution

When you run `./script.sh` or `bash script.sh`:

1. The kernel loads the interpreter from the shebang (or the explicit `bash`)
2. The shell inherits the caller’s environment (unless started with `env -i`)
3. The script body runs as a new process (unless `source`d)
4. The exit status of the last command (or `exit N`) becomes the process exit code

`source script.sh` / `. script.sh` runs in the **current** shell — useful for loading functions, dangerous for `exit` and `cd` side effects.

### Interactive vs Non-interactive Shell

| Mode | Examples | Behaviour |
|------|----------|-----------|
| Interactive | SSH login, terminal | Prompt, history, aliases, often reads `~/.bashrc` |
| Non-interactive | Cron, CI, `bash script.sh` | No prompt; aliases usually off; leaner startup files |

Ops scripts must not depend on interactive aliases or a fancy `PS1`. Test with `bash script.sh` and under a minimal `env`.

### Login Shell

A **login shell** typically reads `/etc/profile` and `~/.profile` (and Bash may read `~/.bash_profile`). SSH sessions are often login shells; `bash script.sh` is usually not. Put shared `PATH` and umask settings where non-interactive jobs will still see them — preferably **inside the script**.

### Environment Variables

Environment variables are key/value pairs exported to child processes: `PATH`, `HOME`, `USER`, `LANG`, `SSH_AUTH_SOCK`, cloud metadata helpers, and CI secrets.

```bash
echo "$PATH"
printenv | sort | head
export OPS_ENV=lab
env -i PATH=/usr/bin:/bin HOME="$HOME" bash -c 'echo PATH=$PATH'
```

Cron and systemd often provide a short `PATH`. Export what you need or use absolute paths.
""",
        "fingerprint shell/bash/sh; compare interactive vs script env; inspect PATH",
    ),
    (
        2,
        "writing-your-first-script",
        "Writing Your First Script",
        "Module 2: Writing Your First Script",
        "beginner",
        "40 min",
        "shell-script-lifecycle",
        ["shebang", "exit-codes", "structure"],
        "Shebang lines, executable bits, running scripts, exit codes, comments, and a production-ready script structure with strict mode.",
        "A one-liner in history is not automation. This tutorial turns commands into a reviewable script with a clear contract: inputs, side effects, and exit status.",
        """### Shebang

The **shebang** is the first line that names the interpreter:

```bash
#!/usr/bin/env bash
```

`env` resolves `bash` from `PATH`. Absolute `#!/bin/bash` is fine when the path is guaranteed (many cloud images).

### Executable Files

Make a script runnable:

```bash
chmod +x script.sh
./script.sh
```

Without `+x`, call `bash script.sh`. The directory must be searchable; `./` avoids relying on `.` being in `PATH`.

### Running Scripts

| Form | Effect |
|------|--------|
| `./script.sh` | New process; needs execute bit + shebang |
| `bash script.sh` | Explicit Bash; execute bit optional |
| `source script.sh` | Current shell — inherits and mutates it |

Prefer `./` or `bash` for jobs. Reserve `source` for libraries of functions.

### Exit Codes

Every process returns an integer **exit code** (0–255). By convention **0** means success; non-zero means failure. Scripts expose this via `exit N` or the last command’s status (`$?`).

Document a small taxonomy for teammates: `2` usage error, `3` missing dependency, `4` runtime failure.

### Comments

Use `#` for human notes. Explain **why**, not what the next line already shows. Keep comments short; outdated comments are worse than none.

### Script Structure

Production default from this module onward:

```bash
#!/usr/bin/env bash
set -euo pipefail

# usage / constants
# functions
# main
```

`-e` exit on error, `-u` treat unset variables as errors, `pipefail` fails a pipeline if any stage fails. Put `set -euo pipefail` near the top after the shebang.
""",
        "create shebang script; chmod +x; exit codes; strict-mode skeleton",
    ),
    (
        3,
        "variables-quoting-and-arithmetic",
        "Variables, Quoting, and Arithmetic",
        "Module 3: Variables",
        "beginner",
        "45 min",
        "shell-variables-quoting",
        ["variables", "quoting", "arithmetic"],
        "Bash variables, constants, environment variables, command substitution, arithmetic, and quoting rules that prevent ops disasters.",
        "Unquoted expansions destroy filenames with spaces and break cron jobs. Master variables and quoting before control flow.",
        """### Variables

Assign without spaces: `name=value`. Expand with `"$name"` or `"${name}"`. Prefer lowercase for script-local names; uppercase for exported environment contracts.

```bash
host=$(hostname -s)
echo "host=${host}"
```

### Constants

Bash has no true constants. Convention: `readonly MAX_RETRIES=3` or `declare -r MAX_RETRIES=3`. Treat config knobs as read-only after validation.

### Environment Variables

`export VAR=value` publishes to children. Read with `"${VAR}"`. Prefer `"${VAR:-default}"` and `"${VAR:?must set VAR}"` for required ops inputs.

### Command Substitution

`$(command)` captures stdout. Prefer modern `$(...)` over backticks. Quote the result when it is one path or one token: `"$(date -Iseconds)"`.

### Arithmetic

Integer maths with `$((expression))` or `((expression))`:

```bash
n=$((n + 1))
(( n > 0 )) && echo positive
```

For floats, call `bc` or move to Python.

### Quoting Rules

| Form | Effect |
|------|--------|
| `"$var"` | Expand; keep as one word |
| `'$var'` | Literal characters |
| `$var` | Word-split and glob — usually wrong in scripts |
| `"$@"` | Safe forwarding of all positional parameters |

Always quote paths and user input. Prefer `"$1"` over `$1`.
""",
        "break/fix spaced names; defaults; arithmetic counters; quote drills",
    ),
    (
        4,
        "input-output-redirection-and-pipes",
        "Input, Output, Redirection, and Pipes",
        "Module 4: Input & Output",
        "beginner",
        "45 min",
        "shell-io-redirection",
        ["io", "redirection", "pipes"],
        "echo, printf, read, stdin/stdout/stderr, redirection operators, and pipelines for DevOps glue scripts.",
        "Ops scripts speak through streams: data on stdout, diagnostics on stderr, and composition through pipes. Get the streams right and monitoring stays honest.",
        """### echo

`echo` prints arguments with a trailing newline. Portable enough for simple messages; avoid relying on non-POSIX flags (`-e`, `-n` vary). Prefer `printf` when format matters.

### printf

```bash
printf 'host=%s status=%s\\n' "$host" "$status" >&2
```

Use `printf` for structured logs and safe formatting.

### read

`read -r var` reads a line from stdin into `var`. `-r` disables backslash escapes. Combine with `IFS=` for raw lines: `while IFS= read -r line; do ...; done < file`.

### stdin, stdout, stderr

| Stream | FD | Role |
|--------|----|------|
| stdin | 0 | Input |
| stdout | 1 | Data / normal output |
| stderr | 2 | Diagnostics, progress, errors |

Keep machine-readable results on stdout and human diagnostics on stderr so pipes stay clean.

### Redirection

| Operator | Meaning |
|----------|---------|
| `>` | Truncate and write stdout |
| `>>` | Append stdout |
| `2>` | Redirect stderr |
| `&>` | Both streams (Bash) |
| `<` | Read stdin from file |
| `2>&1` | Merge stderr into stdout |

### Pipes

`cmd1 | cmd2` connects stdout of `cmd1` to stdin of `cmd2`. With `set -o pipefail`, any failing stage fails the pipeline — required for honest CI and health checks.
""",
        "printf/read; redirect logs; pipefail demo; stderr vs stdout",
    ),
    (
        5,
        "control-flow-conditionals",
        "Control Flow — Conditionals",
        "Module 5: Control Flow",
        "beginner",
        "45 min",
        "shell-control-flow",
        ["if", "case", "test"],
        "Branch with if/elif/else, case, test/[ ], [[ ]], and logical operators for safe ops preconditions.",
        "Conditionals encode preconditions: file present, argument legal, disk free, service healthy. Prefer explicit tests over clever one-liners.",
        """### if, elif, else

```bash
if [[ -f "$cfg" ]]; then
  echo "ok"
elif [[ -d "$cfg" ]]; then
  echo "directory" >&2
  exit 2
else
  echo "missing" >&2
  exit 3
fi
```

### case

Match patterns for CLI verbs and status strings. Always include a `*)` default:

```bash
case "${1:-}" in
  start|stop|status) action=$1 ;;
  *) echo "usage: $0 start|stop|status" >&2; exit 2 ;;
esac
```

### test and `[ ]`

POSIX tests: `[ -f "$f" ]`, `[ "$a" = "$b" ]`. Quote operands. Prefer `[[ ]]` in Bash scripts.

### `[[ ]]`

Bash conditional with safer parsing, `=~` regex, and `&&` / `||` inside the brackets. No word-splitting surprises for unquoted globs in the same way as `[`.

### Logical Operators

`&&` run next on success; `||` run next on failure. Prefer `if` for multi-line clarity. Combine tests: `[[ -n "$x" && -f "$x" ]]`.
""",
        "[[ vs [; guard preconditions; case CLI verbs; logical chains",
    ),
    (
        6,
        "loops-for-while-until",
        "Loops — for, while, and until",
        "Module 6: Loops",
        "beginner",
        "45 min",
        "shell-loops-flow",
        ["for", "while", "loops"],
        "Iterate with for, while, and until; control flow with break and continue; nest loops carefully for ops batch jobs.",
        "Fleet checks, log scans, and retry loops are everyday DevOps patterns. Write loops that fail loudly and stop cleanly.",
        """### for

```bash
for host in web01 web02 web03; do
  printf 'check %s\\n' "$host"
done

for f in /var/log/*.log; do
  [[ -e "$f" ]] || continue
  wc -l <"$f"
done
```

Prefer `"$@"` and arrays over unquoted globs when inputs are dynamic.

### while

```bash
while IFS= read -r line; do
  printf '%s\\n' "$line"
done <"$infile"
```

Classic for streaming files and process output.

### until

`until condition; do ...; done` loops while the condition is false — handy for “wait until ready” probes (with a timeout).

### break and continue

`break` leaves the loop; `continue` skips to the next iteration. Use `break 2` carefully with nested loops.

### Nested Loops

Keep nesting shallow. Extract the inner body to a function when readability suffers. Always bound retries with a counter to avoid infinite wait loops in production.
""",
        "for over hosts; while read lines; until ready; break/continue drills",
    ),
    (
        7,
        "functions-parameters-and-locals",
        "Functions, Parameters, and Locals",
        "Module 7: Functions",
        "intermediate",
        "45 min",
        "shell-functions-locals",
        ["functions", "locals", "reuse"],
        "Declare Bash functions, pass parameters, return values via exit status and stdout, use local variables, and build reusable helpers.",
        "Copy-paste blocks become drift. Small functions with locals keep ops libraries reviewable and testable.",
        """### Function Declaration

```bash
log() {
  printf '[%s] %s\\n' "$(date -Iseconds)" "$*" >&2
}

die() {
  log "ERROR: $*"
  exit 1
}
```

Define functions before use. Prefer `name()` over `function name` for portability within Bash style guides.

### Parameters

Inside a function, `$1`, `$2`, … and `"$@"` refer to the function’s arguments, not the script’s (unless you forward them).

### Return Values

`return N` sets the function’s exit status (0–255). For data, print to stdout and capture with `"$(fn)"`. Do not mix silent side effects with captured stdout.

### Local Variables

`local var=value` scopes a variable to the function. Without `local`, assignments leak into the global script scope — a common production bug.

### Reusable Functions

Group helpers in `lib/common.sh` and `source` them. Keep functions pure where possible: validate → transform → side effect. Document exit codes for `die`-style helpers.
""",
        "log/die helpers; local vs global; source a tiny library",
    ),
    (
        8,
        "arrays-and-string-manipulation",
        "Arrays and String Manipulation",
        "Module 8: Arrays & Strings",
        "intermediate",
        "50 min",
        "shell-arrays-strings",
        ["arrays", "strings", "patterns"],
        "Indexed and associative arrays, string slicing and substitution, and pattern matching for ops data shaping.",
        "Host lists, service maps, and path rewriting are array and string problems. Handle them without fragile IFS hacks.",
        """### Indexed Arrays

```bash
hosts=(web01 web02 web03)
hosts+=("web04")
printf '%s\\n' "${hosts[@]}"
# count elements without array-length parameter expansion (mkdocs-safe):
n=0
for _ in "${hosts[@]}"; do n=$((n + 1)); done
echo "count=$n"
```

Always expand as `"${array[@]}"` to preserve elements with spaces.

### Associative Arrays

```bash
declare -A ports=( [web]=80 [db]=5432 )
printf 'web port=%s\\n' "${ports[web]}"
```

Requires Bash 4+. Useful for env→value maps and small inventories.

### String Manipulation

| Expansion | Use |
|-----------|-----|
| `${var%%.*}` | Strip longest suffix |
| `${var##*/}` | Basename-like |
| `${var%/*}` | Dirname-like |
| `${var/old/new}` | Replace first match |
| `${var:0:3}` | Substring |

### Pattern Matching

`[[ $name == *.log ]]`, `case` patterns, and `=~` with extended regex. Validate inputs before destructive use.
""",
        "indexed host list; associative ports; string strip/replace; patterns",
    ),
    (
        9,
        "file-operations-in-shell",
        "File Operations in Shell",
        "Module 9: File Operations",
        "intermediate",
        "45 min",
        "shell-file-operations",
        ["files", "temp", "directories"],
        "Read and write files safely, create temporary files, use file tests, and manage directories in automation.",
        "Backup jobs, lock files, and config rewrites all touch the filesystem. Do it with tests, temps, and cleanup traps.",
        """### Reading Files

```bash
while IFS= read -r line; do
  printf '%s\\n' "$line"
done <"$file"
```

Prefer `mapfile`/`readarray` for modest files. Avoid `for line in $(cat file)` — it splits on IFS.

### Writing Files

`printf ... >"$out"` truncates; `>>` appends. Write to a temp file then `mv` for atomic replace on the same filesystem.

### Temporary Files

```bash
tmp=$(mktemp)
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmp" "$tmpdir"' EXIT
```

Never hard-code `/tmp/myjob` — collisions and symlink attacks follow.

### File Tests

`-e` exists, `-f` regular file, `-d` directory, `-r`/`-w`/`-x` permissions, `-s` non-empty, `-L` symlink.

### Directory Operations

`mkdir -p`, `find`, `install -d`, `rsync -a` for trees. Validate paths stay under an allowed root before `rm -rf`.
""",
        "read/write atomically; mktemp + trap; file tests; safe mkdir",
    ),
    (
        10,
        "text-processing-in-shell-scripts",
        "Text Processing in Shell Scripts",
        "Module 10: Text Processing",
        "intermediate",
        "50 min",
        "shell-text-processing",
        ["grep", "sed", "awk", "xargs"],
        "Filter and transform text with grep, sed, awk, cut, tr, sort, uniq, paste, and xargs inside scripts.",
        "Logs and CLI output are the DevOps data plane. Compose filters carefully and keep `pipefail` on.",
        """### grep

Search lines: `grep -E 'error|fail' app.log`, `-F` fixed strings, `-r` recursive, `-v` invert. Prefer `rg` interactively; stick to `grep` in portable scripts.

### sed

Stream editor for substitutions: `sed -E 's/foo/bar/'`. Prefer explicit files over in-place edits without backup in production.

### awk

Column and record processing: `awk -F: '{print $1}' /etc/passwd`. Ideal for reports from structured text.

### cut, tr, sort, uniq, paste

| Tool | Use |
|------|-----|
| `cut` | Field slices (`-d -f`) |
| `tr` | Character translate/delete |
| `sort` | Order lines (`-u` unique) |
| `uniq` | Adjacent duplicates (often after `sort`) |
| `paste` | Merge lines side by side |

### xargs

Build command lines from stdin: `printf '%s\\0' "${files[@]}" | xargs -0 -n 20 gzip`. Prefer `-0` / NUL delimiters for safe paths.
""",
        "grep/sed/awk pipeline; sort|uniq report; xargs batch",
    ),
    (
        11,
        "process-automation-signals-and-traps",
        "Process Automation — Signals and Traps",
        "Module 11: Process Automation",
        "intermediate",
        "50 min",
        "shell-process-automation",
        ["process", "signals", "trap"],
        "Inspect and control processes with ps, kill, pkill, nohup, jobs, and wait; handle signals with trap.",
        "Long jobs, background workers, and cleanup on interrupt separate hobby scripts from production automation.",
        """### ps, kill, pkill

`ps aux` / `ps -ef` list processes. `kill -TERM pid` requests graceful stop; `kill -KILL` is last resort. `pkill -f pattern` matches command lines — scope carefully on shared hosts.

### nohup, jobs, wait

`nohup cmd &` ignores hangup for ad-hoc jobs (prefer systemd for real services). `jobs` lists shell background tasks; `wait` blocks until children finish and surfaces their status with `pipefail`-aware scripting.

### Signals

Common signals: `SIGINT` (Ctrl-C), `SIGTERM` (systemd/docker stop), `SIGHUP`, `EXIT` (pseudo-signal for shell cleanup).

### Trap

```bash
cleanup() { rm -rf "${WORKDIR:-}"; }
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
```

Always clean temps and lock files on `EXIT`. Keep trap handlers short and idempotent.
""",
        "ps/pkill safely; background + wait; trap cleanup on EXIT",
    ),
    (
        12,
        "linux-admin-automation",
        "Linux Administration Automation",
        "Module 12: Linux Administration",
        "intermediate",
        "55 min",
        "shell-linux-admin",
        ["users", "packages", "services", "backup"],
        "Automate user and package management, services, log rotation hooks, disk usage checks, and backup jobs with Bash.",
        "Linux administration is repetitive — perfect for scripts that are idempotent, logged, and safe under sudo.",
        """### User Management

Script `useradd`/`usermod`/`id` checks idempotently: create only if missing; never embed passwords in scripts (use SSH keys or a secrets store).

### Package Management

Detect family and call `apt-get`, `dnf`, or `zypper` non-interactively (`DEBIAN_FRONTEND=noninteractive`). Pin versions when reproducibility matters.

### Service Management

Prefer `systemctl enable --now`, `systemctl is-active`, and `systemctl show`. Parse status; do not scrape unstable English text without care.

### Log Rotation

Call or configure `logrotate`; for app logs, compress and prune by age/size in a dedicated script with dry-run.

### Disk Usage

`df -h`, `df -i`, `du -sh` on critical paths; alert when thresholds breach. Check inodes as well as bytes.

### Backup Automation

`tar`/`rsync` with retention, checksums, and a restore dry-run path. Log start/end and exit non-zero on failure.
""",
        "idempotent user check; disk report; mini backup with retention",
    ),
    (
        13,
        "networking-automation-with-shell",
        "Networking Automation with Shell",
        "Module 13: Networking Automation",
        "intermediate",
        "50 min",
        "shell-networking-auto",
        ["curl", "ssh", "rsync", "dns"],
        "Automate connectivity checks and transfers with ping, curl, wget, nc, dig, SSH, SCP, and rsync.",
        "Health checks, artifact pulls, and remote ops all start as shell networking. Timeouts and exit codes matter more than clever curl flags.",
        """### ping, nc, dig

`ping -c 3 host` for ICMP reachability (may be blocked). `nc -zv host port` for TCP probes. `dig +short` / `getent hosts` for DNS — prefer checking DNS before blaming the app.

### curl and wget

`curl -fsSL --connect-timeout 5 --max-time 30` for APIs and downloads (`-f` fails on HTTP errors). `wget` remains common for simple file fetches. Always set timeouts.

### SSH, SCP, rsync

```bash
ssh -o BatchMode=yes -o ConnectTimeout=5 host 'uname -a'
rsync -az --delete src/ host:dst/
```

Use `BatchMode=yes` in automation so password prompts fail fast. Prefer `rsync` over `scp` for trees and resumes.
""",
        "curl with timeouts; dig/nc probes; SSH BatchMode; rsync dry-run",
    ),
    (
        14,
        "json-and-yaml-with-jq-yq",
        "JSON and YAML with jq and yq",
        "Module 14: JSON & YAML",
        "intermediate",
        "50 min",
        "shell-json-yaml",
        ["jq", "yq", "config"],
        "Parse and transform JSON and YAML configuration with jq and yq in shell pipelines.",
        "Cloud APIs and Kubernetes speak JSON/YAML. Shell stays useful when jq/yq shape data before the next tool runs.",
        """### jq

```bash
jq -r '.items[].metadata.name' < deploy.json
jq --arg env "$ENV" '.env = $env' config.json
```

Prefer `jq` over `grep`/`sed` for JSON. Fail fast on invalid input.

### yq

`yq` (Mike Farah / Python variants exist — pin one) reads and writes YAML. Convert, select keys, and merge overlays for config files.

### Parsing JSON and YAML

Validate before apply. Extract only the fields you need. Keep secrets out of shell history and debug dumps.

### Configuration Files

Treat config as data: version it, validate schema where possible, and rewrite atomically (`tmp` + `mv`). Document required keys in the script’s usage text.
""",
        "jq extract/transform; yq read YAML; validate config keys",
    ),
    (
        15,
        "scheduling-cron-at-and-timers",
        "Scheduling — cron, at, and systemd Timers",
        "Module 15: Scheduling",
        "intermediate",
        "45 min",
        "shell-cron-execution",
        ["cron", "at", "systemd-timers"],
        "Schedule automation with cron, crontab, at, and systemd timers — and make jobs reliable under minimal environments.",
        "Schedulers strip your interactive environment. Scripts must set PATH, cwd, logging, and locking themselves.",
        """### cron and crontab

`crontab -e` installs per-user entries. System drop-ins live under `/etc/cron.*`. Five fields set schedule; sixth is the command.

### at

`at` queues one-shot jobs. Useful for deferred maintenance windows; less common than cron/timers for recurring ops.

### systemd Timers

Prefer **systemd timers** for modern hosts: calendar or monotonic triggers, dependency ordering, and journal logs via the paired `.service`.

```bash
systemctl list-timers --all
systemctl status myjob.timer
```

Wrap the real work in a script with `set -euo pipefail`, explicit `PATH`, log redirection, and a lock file so overlaps do not corrupt state.
""",
        "cron-ready wrapper; PATH fingerprint; timer vs cron notes",
    ),
    (
        16,
        "error-handling-logging-and-debugging",
        "Error Handling, Logging, and Debugging",
        "Module 16: Error Handling",
        "advanced",
        "50 min",
        "shell-error-handling",
        ["errors", "logging", "debugging"],
        "Exit codes, traps, defensive programming, structured logging, and Bash debugging techniques for production scripts.",
        "Silent success is how monitors lie. Make failure audible with strict mode, traps, logs, and a clear exit taxonomy.",
        """### Exit Codes

Map failures to documented integers. Propagate child failures; do not `|| true` away errors you care about.

### Trap

Use `trap` for cleanup and to translate signals into known exit codes. Pair with `set -E` if you need `ERR` traps inside functions.

### Defensive Programming

- `set -euo pipefail`
- Quote expansions
- Validate args early
- Prefer absolute paths under schedulers
- Fail closed on missing dependencies (`command -v jq >/dev/null`)

### Logging

Log to stderr with timestamps and levels (`INFO`, `WARN`, `ERROR`). Reserve stdout for data or `RESULT` lines consumers can parse.

### Debugging

`bash -x script.sh`, `PS4='+${BASH_SOURCE}:${LINENO}: '`, and temporary `set -x` around suspect blocks. Remove noisy traces before shipping.
""",
        "exit taxonomy; ERR/EXIT traps; log levels; bash -x drill",
    ),
    (
        17,
        "production-shell-scripting",
        "Production Shell Scripting",
        "Module 17: Production Shell Scripting",
        "advanced",
        "55 min",
        "shell-automation-workflow",
        ["shellcheck", "idempotent", "secure", "locks"],
        "Ship production Bash: ShellCheck, idempotency, secure patterns, logging, retries, lock files, and configuration management hooks.",
        "Production scripts survive retries, concurrent cron, hostile input, and tired operators. Build those properties in deliberately.",
        """### ShellCheck

Run `shellcheck script.sh` in CI. Treat warnings about quoting and `cd` as defects. Disable rules only with a justified directive.

### Idempotent Scripts

Safe to re-run: create users only if missing, `mkdir -p`, enable services only when needed. Prefer declare desired state over blind mutate.

### Secure Scripting

No `eval`, no unquoted `rm -rf $var`, no secrets in argv or world-readable files. Validate paths stay under an allow-list root. Least privilege.

### Logging and Retry Logic

Structured logs plus bounded retries with sleep/backoff for transient network errors. Cap attempts; escalate after exhaustion.

### Lock Files

```bash
exec 9>"$lock"
flock -n 9 || { echo "already running" >&2; exit 0; }
```

Prevent overlapping cron runs from corrupting backups.

### Configuration Management

Accept config via env files, flags, or drop-in directories. Keep secrets out of the repo; integrate with Ansible/systemd/`EnvironmentFile=` where appropriate.
""",
        "shellcheck clean script; flock; retry helper; idempotent mkdir/user check",
    ),
    (
        18,
        "troubleshooting-shell-scripts",
        "Troubleshooting Shell Scripts",
        "Module 18: Troubleshooting",
        "advanced",
        "50 min",
        "shell-troubleshooting",
        ["debug", "permissions", "cron", "performance"],
        "Debug Bash failures: common errors, permissions, cron environment issues, expansion bugs, and performance optimisation.",
        "When a script works locally and fails in CI or cron, method beats guessing. This tutorial is your incident checklist.",
        """### Debugging Bash

Reproduce with the same interpreter and env: `env -i PATH=... bash -x ./script.sh`. Bisect with `set -x` regions. Confirm shebang and line endings (`file`, `sed -n l`).

### Common Errors

| Symptom | Cause |
|---------|--------|
| `command not found` | PATH / typo / missing package |
| `unbound variable` | `set -u` + missing default |
| `unexpected token` | Windows CRLF or bad quoting |
| `Permission denied` | Mode, mount `noexec`, or directory bits |

### Permission Problems

Check execute bit, directory `x`, SELinux/AppArmor denials, and whether the scheduler user differs from yours.

### Cron Issues

Minimal `PATH`, different cwd, missing tty, and mailed stderr you never read. Log to a file; set `PATH`; use absolute paths.

### Variable Expansion Problems

Unquoted `$var`, wrong `${var:-}` vs `${var-}` , and accidental globbing. Print `declare -p var` while debugging.

### Performance Optimisation

Avoid spawning needless pipelines in tight loops; batch with `xargs`; prefer Bash builtins for simple string work; move heavy JSON transforms to one `jq` invocation. Profile with `time` and reduce process count.
""",
        "reproduce cron env; fix quoting bug; bash -x; time a hot loop",
    ),
]

OBSOLETE = [
    "introduction-to-shell-scripting-for-ops.md",
    "bash-posix-sh-and-the-execution-environment.md",
    "variables-quoting-and-expansions.md",
    "exit-status-strict-mode-and-debugging.md",
    "tests-and-conditionals.md",
    "loops-ifs-and-safe-line-reading.md",
    "functions-locals-and-small-libraries.md",
    "arguments-and-getopts.md",
    "arrays-and-associative-arrays.md",
    "text-pipelines-inside-scripts.md",
    "traps-signals-temp-files-and-locking.md",
    "logging-verbosity-and-exit-taxonomy.md",
    "secure-shell-scripting.md",
    "cron-systemd-oneshots-and-timer-wrappers.md",
    "shell-in-ci-cd.md",
    "capstone-ops-script-toolkit.md",
]

STYLE = (
    "*: { style: { border-radius: 14; font-size: 14; bold: true; "
    "shadow: true; stroke-width: 2 } }\n"
    "direction: right\n"
)


def _flow(
    a: str,
    b: str,
    c: str,
    d: str,
    ca: str = "#dbeafe",
    cb: str = "#dcfce7",
    cc: str = "#ffedd5",
    cd: str = "#fce7f3",
    sa: str = "#2563eb",
    sb: str = "#16a34a",
    sc: str = "#ea580c",
    sd: str = "#db2777",
) -> str:
    return dedent(
        f"""\
        {STYLE}A: "{a}" {{ style.fill: "{ca}"; style.stroke: "{sa}" }}
        B: "{b}" {{ style.fill: "{cb}"; style.stroke: "{sb}" }}
        C: "{c}" {{ style.fill: "{cc}"; style.stroke: "{sc}" }}
        D: "{d}" {{ style.fill: "{cd}"; style.stroke: "{sd}" }}
        A -> B -> C -> D
        """
    )


DIAGRAMS: dict[str, str] = {
    "shell-execution-flow": _flow(
        "Terminal / cron / CI", "Shell process", "Expand + parse", "Exec + exit code"
    ),
    "shell-script-lifecycle": _flow(
        "Shebang", "chmod +x / bash", "Strict mode body", "Exit status"
    ),
    "shell-variables-quoting": _flow(
        "Assign name=value", "Quote expansions", "Command subst", "Arithmetic"
    ),
    "shell-io-redirection": _flow(
        "stdin FD0", "stdout FD1", "stderr FD2", "Files / pipes"
    ),
    "shell-process-pipeline": _flow(
        "Producer cmd", "Pipe |", "Filter stages", "Consumer + pipefail"
    ),
    "shell-control-flow": _flow(
        "Preconditions", "if / [[ ]]", "case verbs", "Branch actions"
    ),
    "shell-loops-flow": _flow(
        "Inputs / lists", "for while until", "break continue", "Aggregated result"
    ),
    "shell-functions-locals": _flow(
        "Call site", "Parameters", "local state", "return / stdout"
    ),
    "shell-arrays-strings": _flow(
        "Indexed / assoc", "Iterate elements", "String ops", "Pattern match"
    ),
    "shell-file-operations": _flow(
        "Path validate", "Read / write", "mktemp + trap", "Atomic mv"
    ),
    "shell-text-processing": _flow(
        "Raw text / logs", "grep filter", "sed / awk / cut", "sort uniq xargs"
    ),
    "shell-process-automation": _flow(
        "ps inspect", "jobs / nohup", "signals", "trap cleanup"
    ),
    "shell-linux-admin": _flow(
        "Users / packages", "systemctl", "disk / logs", "Backup job"
    ),
    "shell-networking-auto": _flow(
        "DNS dig / ping", "curl / nc", "SSH BatchMode", "rsync / scp"
    ),
    "shell-json-yaml": _flow(
        "JSON / YAML file", "jq / yq", "Validate keys", "Atomic config write"
    ),
    "shell-cron-execution": _flow(
        "crontab / timer", "Minimal env", "Wrapper script", "Log + lock"
    ),
    "shell-error-handling": _flow(
        "Strict mode", "Validate inputs", "Log + trap", "Documented exit"
    ),
    "shell-automation-workflow": _flow(
        "ShellCheck CI", "Idempotent run", "flock + retry", "Config + secure"
    ),
    "shell-troubleshooting": _flow(
        "Reproduce env", "bash -x", "Permissions / cron", "Fix + verify"
    ),
}

LAB_EXTRA: dict[int, str] = {
    1: dedent(
        """\
        ### Step 2 – Fingerprint shells and environment

        ```bash
        cat > fingerprint.sh << 'EOF'
        #!/usr/bin/env bash
        echo "bash=$BASH_VERSION"
        echo "sh=$(readlink -f /bin/sh 2>/dev/null || echo /bin/sh)"
        echo "interactive=$([[ $- == *i* ]] && echo yes || echo no)"
        echo "PATH=$PATH"
        printenv | sort | head -n 20
        EOF
        chmod +x fingerprint.sh
        ./fingerprint.sh | tee fingerprint.txt
        env -i PATH=/usr/bin:/bin HOME="$HOME" bash ./fingerprint.sh | tee fingerprint-min.txt
        ```
        """
    ),
    2: dedent(
        """\
        ### Step 2 – First strict-mode script

        ```bash
        cat > hello-ops.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        # hello-ops: tiny contract demo
        host=$(hostname -s)
        echo "hello from ${host}"
        exit 0
        EOF
        chmod +x hello-ops.sh
        ./hello-ops.sh
        bash -c './hello-ops.sh; echo exit=$?'
        ```
        """
    ),
    3: dedent(
        """\
        ### Step 2 – Quoting and arithmetic

        ```bash
        cat > quoting-demo.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        name='my file.txt'
        touch "$name"
        # Broken on purpose if unquoted — keep quoted:
        ls -l -- "$name"
        n=${COUNT:-0}
        n=$((n + 1))
        readonly MAX=3
        echo "n=$n MAX=$MAX"
        echo "subst=$(date -Iseconds)"
        EOF
        chmod +x quoting-demo.sh
        ./quoting-demo.sh
        ```
        """
    ),
    4: dedent(
        """\
        ### Step 2 – Streams, redirect, pipefail

        ```bash
        cat > io-demo.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        printf 'data-line\\n'
        printf 'diag-line\\n' >&2
        EOF
        chmod +x io-demo.sh
        ./io-demo.sh >stdout.txt 2>stderr.txt
        cat stdout.txt stderr.txt
        # pipefail: false in a pipeline must fail
        set -o pipefail
        if false | true; then echo 'unexpected'; else echo 'pipefail ok'; fi
        ```
        """
    ),
    5: dedent(
        """\
        ### Step 2 – Guards and case

        ```bash
        cat > guard.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        cfg=${1:-}
        [[ -n "$cfg" ]] || { echo "usage: $0 <file>" >&2; exit 2; }
        if [[ -f "$cfg" ]]; then
          echo "file ok"
        elif [[ -d "$cfg" ]]; then
          echo "is directory" >&2
          exit 3
        else
          echo "missing" >&2
          exit 4
        fi
        case "${2:-status}" in
          status|check) echo "action=${2:-status}" ;;
          *) echo "bad action" >&2; exit 2 ;;
        esac
        EOF
        chmod +x guard.sh
        echo ok > sample.cfg
        ./guard.sh sample.cfg status
        ```
        """
    ),
    6: dedent(
        """\
        ### Step 2 – Loops and control

        ```bash
        cat > loops.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        for h in a b c; do
          [[ "$h" == b ]] && continue
          echo "host=$h"
        done
        n=0
        while (( n < 3 )); do
          n=$((n + 1))
          echo "while n=$n"
        done
        m=0
        until (( m >= 2 )); do
          m=$((m + 1))
          echo "until m=$m"
        done
        EOF
        chmod +x loops.sh
        ./loops.sh
        ```
        """
    ),
    7: dedent(
        """\
        ### Step 2 – Functions and locals

        ```bash
        mkdir -p lib
        cat > lib/common.sh << 'EOF'
        log() { printf '[%s] %s\\n' "$(date -Iseconds)" "$*" >&2; }
        die() { log "ERROR: $*"; exit 1; }
        add() {
          local a=$1 b=$2
          printf '%s\\n' "$((a + b))"
        }
        EOF
        cat > main.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        # shellcheck source=lib/common.sh
        source "$(dirname "$0")/lib/common.sh"
        log "starting"
        sum=$(add 2 3)
        echo "sum=$sum"
        EOF
        chmod +x main.sh
        ./main.sh
        ```
        """
    ),
    8: dedent(
        """\
        ### Step 2 – Arrays and strings

        ```bash
        cat > arrays.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        hosts=(web01 web02 'web 03')
        hosts+=("web04")
        n=0
        for _ in "${hosts[@]}"; do n=$((n + 1)); done
        echo "count=$n"
        printf '%s\\n' "${hosts[@]}"
        declare -A ports=( [web]=80 [db]=5432 )
        echo "web=${ports[web]}"
        path=/var/log/app.log
        echo "base=${path##*/}"
        [[ $path == *.log ]] && echo 'pattern ok'
        EOF
        chmod +x arrays.sh
        ./arrays.sh
        ```
        """
    ),
    9: dedent(
        """\
        ### Step 2 – Safe file ops

        ```bash
        cat > files.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        root=$PWD/data
        mkdir -p "$root"
        tmp=$(mktemp)
        trap 'rm -f "$tmp"' EXIT
        printf 'line1\\nline2\\n' >"$tmp"
        out=$root/out.txt
        cp "$tmp" "$out.tmp"
        mv "$out.tmp" "$out"
        [[ -f "$out" && -s "$out" ]] || exit 4
        while IFS= read -r line; do echo "got=$line"; done <"$out"
        EOF
        chmod +x files.sh
        ./files.sh
        ```
        """
    ),
    10: dedent(
        """\
        ### Step 2 – Text pipeline

        ```bash
        printf 'b\\na\\nb\\nc\\n' > raw.txt
        cat > text.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        grep -v '^$' raw.txt \\
          | tr '[:upper:]' '[:lower:]' \\
          | sort \\
          | uniq -c \\
          | sort -nr \\
          | tee report.txt
        cut -c1-20 report.txt | paste - -
        printf 'a\\nb\\n' | xargs -n 1 echo item
        EOF
        chmod +x text.sh
        ./text.sh
        ```
        """
    ),
    11: dedent(
        """\
        ### Step 2 – Trap and wait

        ```bash
        cat > trap-demo.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        work=$(mktemp -d)
        cleanup() { rm -rf "$work"; echo "cleaned" >&2; }
        trap cleanup EXIT
        echo job >"$work/out"
        sleep 0.2 &
        wait
        ps -o pid,cmd | head
        EOF
        chmod +x trap-demo.sh
        ./trap-demo.sh
        ```
        """
    ),
    12: dedent(
        """\
        ### Step 2 – Admin toolkit slice

        ```bash
        cat > admin.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "== disk =="; df -h . | tee disk.txt
        echo "== inodes =="; df -i . | tee -a disk.txt
        mkdir -p backup-src backup-out
        echo data > backup-src/note.txt
        ts=$(date +%Y%m%d%H%M%S)
        tar -czf "backup-out/backup-$ts.tgz" -C backup-src .
        ls -l backup-out
        # idempotent user presence check (no create):
        id -u "$(whoami)" >/dev/null
        command -v systemctl >/dev/null && systemctl is-system-running --quiet || true
        EOF
        chmod +x admin.sh
        ./admin.sh
        ```
        """
    ),
    13: dedent(
        """\
        ### Step 2 – Network probes

        ```bash
        cat > net.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        dig +short example.com | head | tee dns.txt || getent hosts example.com | tee dns.txt
        curl -fsS --connect-timeout 5 --max-time 15 -o /dev/null -w 'http=%{http_code}\\n' https://example.com
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
        """
    ),
    14: dedent(
        """\
        ### Step 2 – jq (and yq if present)

        ```bash
        cat > sample.json << 'EOF'
        {"env":"lab","items":[{"name":"web"},{"name":"db"}]}
        EOF
        cat > sample.yaml << 'EOF'
        env: lab
        replicas: 2
        EOF
        cat > parse.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        command -v jq >/dev/null || { echo "install jq" >&2; exit 3; }
        jq -r '.items[].name' sample.json | tee names.txt
        jq --arg e prod '.env=$e' sample.json > out.json
        if command -v yq >/dev/null; then
          yq '.replicas' sample.yaml | tee replicas.txt
        else
          echo 'yq not installed — skipped' | tee replicas.txt
        fi
        EOF
        chmod +x parse.sh
        ./parse.sh
        ```
        """
    ),
    15: dedent(
        """\
        ### Step 2 – Scheduler-ready wrapper

        ```bash
        cat > nightly.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        PATH=/usr/bin:/bin
        LOG="$HOME/rebash-shell/lab15/nightly.log"
        LOCK="$HOME/rebash-shell/lab15/nightly.lock"
        mkdir -p "$(dirname "$LOG")"
        exec 9>"$LOCK"
        flock -n 9 || { echo "already running" >&2; exit 0; }
        exec >>"$LOG" 2>&1
        echo "run $(date -Iseconds) PATH=$PATH"
        EOF
        chmod +x nightly.sh
        ./nightly.sh
        # Example (do not install unless intended):
        # */15 * * * * $HOME/rebash-shell/lab15/nightly.sh
        # Prefer a systemd timer + service pair on modern hosts.
        ```
        """
    ),
    16: dedent(
        """\
        ### Step 2 – Logging and debug

        ```bash
        cat > robust.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        log() { printf '[%s] %s\\n' "$1" "$2" >&2; }
        die() { log ERROR "$1"; exit "${2:-1}"; }
        trap 'log ERROR "failed at line $LINENO"' ERR
        [[ $# -ge 1 ]] || die "usage: $0 <name>" 2
        log INFO "hello $1"
        echo "RESULT ok"
        EOF
        chmod +x robust.sh
        ./robust.sh lab16
        bash -x ./robust.sh lab16 2>&1 | tail -n 15
        ```
        """
    ),
    17: dedent(
        """\
        ### Step 2 – Production patterns

        ```bash
        cat > prod.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        lock=$PWD/prod.lock
        exec 9>"$lock"
        flock -n 9 || { echo "locked" >&2; exit 0; }
        retry() {
          local n=0 max=3
          until "$@"; do
            n=$((n + 1))
            (( n >= max )) && return 1
            sleep 1
          done
        }
        mkdir -p state
        [[ -d state ]] || exit 4
        retry true
        echo "idempotent ok"
        EOF
        chmod +x prod.sh
        ./prod.sh
        command -v shellcheck >/dev/null && shellcheck prod.sh || echo 'shellcheck optional'
        ```
        """
    ),
    18: dedent(
        """\
        ### Step 2 – Troubleshoot checklist

        ```bash
        cat > broken.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        # Intentionally awkward — fix in place:
        target='my file'
        touch "$target"
        ls -l -- "$target"
        EOF
        chmod +x broken.sh
        # Minimal env like cron:
        env -i PATH=/usr/bin:/bin HOME="$HOME" bash -x ./broken.sh 2>&1 | tee trace.txt
        cat > checklist.md << 'EOF'
        - [ ] Same shebang / bash version
        - [ ] PATH and cwd
        - [ ] Permissions / noexec
        - [ ] Quoting
        - [ ] Cron user vs your user
        EOF
        time bash -c 'n=0; while (( n < 1000 )); do n=$((n+1)); done'
        ```
        """
    ),
}


def related(num: int) -> str:
    links = ["- [Shell Scripting for DevOps Engineers – Category Overview](index.md)"]
    if num > 1:
        prev = SPEC[num - 2]
        links.append(f"- [{prev[2]}]({prev[1]}.md) *(previous)*")
    if num < len(SPEC):
        nxt = SPEC[num]
        links.append(f"- [{nxt[2]}]({nxt[1]}.md) *(next)*")
    links.append("- [Learning Paths](../learning-paths/index.md)")
    return "\n".join(links)


def lab_block(num: int, slug: str, focus: str) -> str:
    """Build Hands-on Lab markdown without accidental leading indentation."""
    extra = LAB_EXTRA.get(num, "").rstrip()
    use_strict = num >= 2
    skeleton_lines = [
        "cat > lab.sh << 'EOF'",
        "#!/usr/bin/env bash",
    ]
    if use_strict:
        skeleton_lines.append("set -euo pipefail")
    skeleton_lines.append(f'echo "lab{num:02d} {slug} on $(hostname -s)"')
    skeleton_lines.append("EOF")
    skeleton_lines.append("chmod +x lab.sh")
    skeleton_lines.append("./lab.sh")

    parts = [
        "Create a workspace for this tutorial.",
        "",
        "```bash",
        f"mkdir -p ~/rebash-shell/lab{num:02d} && cd ~/rebash-shell/lab{num:02d}",
        "```",
        "",
        f"**Focus:** {focus}",
        "",
        "### Step 1 – Skeleton",
        "",
        "```bash",
        *skeleton_lines,
        "```",
    ]
    if extra:
        parts.extend(["", extra])
    parts.extend(
        [
            "",
            "### Final step – Trace and cleanup note",
            "",
            "```bash",
            "bash -x ./lab.sh 2>&1 | tail -n 20 || true",
            "# keep ~/rebash-shell for later labs",
            "```",
        ]
    )
    return "\n".join(parts)


def render(sp: tuple) -> str:
    (
        num,
        slug,
        title,
        module,
        difficulty,
        minutes,
        diagram,
        tag_extra,
        desc,
        overview,
        theory,
        lab_focus,
    ) = sp
    tags = ["shell", "bash", *tag_extra]
    tag_yaml = "\n".join(f"  - {t}" for t in tags)
    prev_title = SPEC[num - 2][2] if num > 1 else "Linux Fundamentals"
    prereq = [
        prev_title if num > 1 else "Linux Fundamentals (files, permissions, processes)",
        "Bash 4.2+ on Linux (WSL2/VM/cloud)",
    ]
    objectives = [
        f"Apply the core ideas of “{title}” in a real ops script",
        "Use quoted expansions and clear stderr diagnostics",
        "Produce meaningful exit codes for automation consumers",
        "Debug behaviour with `bash -x` when something fails",
        "Relate this topic to day-to-day Linux admin and DevOps work",
    ]
    if num >= 2:
        objectives.insert(1, "Use `set -euo pipefail` as the production default")
    obj = "\n".join(f"- [ ] {o}" for o in objectives)
    pr = "\n".join(f"- {p}" for p in prereq)
    pr_yaml = "\n".join(f"  - {p}" for p in prereq)

    return f"""---
title: "{title}"
description: "{desc}"
difficulty: {difficulty}
estimated_time: "{minutes}"
author: {AUTHOR}
last_updated: "{DATE}"
category: shell
tags:
{tag_yaml}
prerequisites:
{pr_yaml}
comments: false
---

# {title}

## Overview

{overview}

This is **Tutorial {num}** in **{module}** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

{pr}

## Learning Objectives

By the end of this tutorial, you will be able to:

{obj}

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for {title}](../assets/images/{diagram}.svg)

## Theory

{theory.strip()}

## Hands-on Lab

{lab_block(num, slug, lab_focus).rstrip()}

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab{num:02d}/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **{title}** always combines:

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

**{title}** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

## Interview Questions

1. How does this topic show up in production Linux administration or CI?
2. What failure mode appears if you ignore quoting or strict mode here?
3. How would you test this behaviour under a minimal cron-like environment?
4. When would you move this logic out of Bash into Python or another tool?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Unquoted expansions and missing `pipefail` create silent or partial failures — especially under cron — that look healthy in monitoring until data is wrong.

## Related Tutorials

{related(num)}

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
"""


def write_diagrams() -> tuple[int, int, list[str]]:
    """Write D2 sources and render SVGs when d2 is available."""
    D2_DIR.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    d2_count = 0
    svg_count = 0
    errors: list[str] = []
    d2_bin = shutil.which("d2")
    for name, source in DIAGRAMS.items():
        d2_path = D2_DIR / f"{name}.d2"
        d2_path.write_text(source.lstrip("\n"), encoding="utf-8")
        d2_count += 1
        print(f"wrote {d2_path.relative_to(ROOT)}")
        svg_path = IMG_DIR / f"{name}.svg"
        if not d2_bin:
            errors.append(f"d2 not found; skipped SVG for {name}")
            continue
        try:
            subprocess.run(
                [
                    d2_bin,
                    "--theme",
                    "3",
                    "--layout",
                    "dagre",
                    "--pad",
                    "48",
                    str(d2_path),
                    str(svg_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            svg_count += 1
            print(f"wrote {svg_path.relative_to(ROOT)}")
        except subprocess.CalledProcessError as exc:
            err = (exc.stderr or exc.stdout or str(exc)).strip()
            errors.append(f"d2 failed for {name}: {err}")
    return d2_count, svg_count, errors


def delete_obsolete() -> list[str]:
    keep = {f"{sp[1]}.md" for sp in SPEC} | {"index.md"}
    deleted: list[str] = []
    for name in OBSOLETE:
        if name in keep:
            continue
        path = OUT / name
        if path.exists():
            path.unlink()
            deleted.append(name)
            print(f"deleted {path.relative_to(ROOT)}")
    return deleted


def assert_no_hash_brace(text: str, label: str) -> None:
    """mkdocs-macros breaks on '{#' sequences in page content."""
    if "{#" in text:
        raise AssertionError(f"forbidden '{{#' found in {label}")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(SPEC) == 18, len(SPEC)
    # One diagram per tutorial + required extras (process pipeline)
    assert "shell-process-pipeline" in DIAGRAMS
    assert "shell-io-redirection" in DIAGRAMS
    assert "shell-execution-flow" in DIAGRAMS
    assert "shell-script-lifecycle" in DIAGRAMS
    assert "shell-cron-execution" in DIAGRAMS
    assert "shell-automation-workflow" in DIAGRAMS
    md_count = 0
    for sp in SPEC:
        diagram = sp[6]
        assert diagram in DIAGRAMS, diagram
        body = render(sp)
        assert_no_hash_brace(body, sp[1])
        path = OUT / f"{sp[1]}.md"
        path.write_text(body, encoding="utf-8")
        md_count += 1
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done: {md_count} tutorials")
    d2_count, svg_count, errors = write_diagrams()
    print(f"diagrams: d2={d2_count} svg={svg_count}")
    deleted = delete_obsolete()
    print(f"deleted_obsolete: {len(deleted)}")
    for e in errors:
        print(f"ERROR: {e}")
    print(
        f"SUMMARY md={md_count} d2={d2_count} svg={svg_count} "
        f"deleted={len(deleted)} errors={len(errors)}"
    )


if __name__ == "__main__":
    main()
