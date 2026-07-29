#!/usr/bin/env python3
"""Generate REBASH Academy Shell Scripting tutorials 1–16 under docs/shell/."""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "shell"
AUTHOR = "Shaik Basha"
DATE = "2026-07-29"

# (num, slug, title, module, difficulty, minutes, diagram, tag_extra, desc, overview, theory, lab_focus)
SPEC: list[tuple] = [
    (
        1,
        "introduction-to-shell-scripting-for-ops",
        "Introduction to Shell Scripting for Ops",
        "Module 1: Foundations",
        "beginner",
        "35 min",
        "shell-intro-ops",
        ["devops", "ops"],
        "Why Bash is the glue for Linux admins and DevOps — scripts versus one-liners and when to use Python.",
        "Cron, CI, and on-call remediation almost always start as shell. This tutorial sets the ops mental model for the track.",
        """### Why Bash for ops

| Job | Why Bash fits |
|-----|----------------|
| Glue | Native pipes and OS tools |
| Bootstrap | Present on nearly every Linux image |
| CI | Job scripts map 1:1 to local Bash |
| Schedulers | Works under cron and systemd with care |

Bash orchestrates commands; it is not an application platform. Prefer Python/Go for complex data, HTTP SDKs, or long-lived services.

### Script contract

1. Documented inputs (args/env)
2. Clear side effects
3. stdout for data, stderr for diagnostics
4. Exit status as the machine API
""",
        "fingerprint host/user/bash; write a tiny `hello-ops.sh` with strict mode",
    ),
    (
        2,
        "bash-posix-sh-and-the-execution-environment",
        "Bash, POSIX sh, and the Execution Environment",
        "Module 1: Foundations",
        "beginner",
        "40 min",
        "shell-execution-env",
        ["posix", "environment"],
        "Shebang lines, Bash versus dash/sh, PATH in cron/CI, and environment fingerprints.",
        "Scripts fail in cron not because Bash forgot how to run — the environment changed. Make that explicit.",
        """### Shebang

`#!/usr/bin/env bash` resolves Bash from PATH. Absolute `#!/bin/bash` is fine when the path is guaranteed.

### Bash versus `/bin/sh`

On Debian/Ubuntu `/bin/sh` is often **dash**. Bash-only: `[[ ]]`, arrays, process substitution. If the shebang is `sh`, stay POSIX.

### PATH discipline

Cron may provide `/usr/bin:/bin` only. Set `PATH` in the script or use absolute paths. Never rely on interactive aliases.
""",
        "inspect `/bin/sh`; demonstrate `[[` failing under sh; `env -i` fingerprint script",
    ),
    (
        3,
        "variables-quoting-and-expansions",
        "Variables, Quoting, and Expansions",
        "Module 1: Foundations",
        "beginner",
        "45 min",
        "shell-quoting",
        ["quoting", "expansions"],
        "Safe expansions — quoting, defaults, substring operations, and word-splitting disasters.",
        "Unquoted expansions are the number one source of destructive Bash bugs. Build quoting reflexes before control flow.",
        """### Quoting

| Form | Effect |
|------|--------|
| `"$var"` | Expand; keep one word |
| `'$var'` | Literal |
| `$var` | Split and glob — usually wrong |
| `"$@"` | Safe argv forwarding |

### Useful expansions

`${var:-default}`, `${var:?message}`, `${path##*/}`, `${path%/*}`, `$(command)`, `$((n+1))`.
""",
        "break/fix spaced filenames; defaults and `${:?}`; demonstrate `$@`",
    ),
    (
        4,
        "exit-status-strict-mode-and-debugging",
        "Exit Status, Strict Mode, and Debugging",
        "Module 1: Foundations",
        "intermediate",
        "45 min",
        "shell-strict-mode",
        ["pipefail", "debugging"],
        "set -euo pipefail, exit taxonomies, bash -x, and pipeline failure semantics.",
        "Silent pipeline success is how monitors lie. Strict mode makes failure audible.",
        """### Strict mode

```bash
set -euo pipefail
```

`-e` exit on error, `-u` unset variable errors, `pipefail` fails the pipeline if any stage fails.

### Debugging

`bash -x script.sh` and `PS4='+${BASH_SOURCE}:${LINENO}: '`.

### Exit taxonomy

Document small integers: `2` usage, `3` missing dependency, `4` runtime failure.
""",
        "pipefail demo; strict file checker; bash -x trace; grep under `-e`",
    ),
    (
        5,
        "tests-and-conditionals",
        "Tests and Conditionals",
        "Module 2: Control Flow and Structure",
        "beginner",
        "40 min",
        "shell-conditionals",
        ["conditionals", "case"],
        "Reliable branches with [[ ]], test/[ ], (( )), and case for CLI verbs.",
        "Conditionals encode preconditions — file present, argument legal, disk free.",
        """### Dialects

Prefer `[[ ... ]]` in Bash. Use `[` for POSIX. Use `(( ))` for integers.

### File tests

`-f`, `-d`, `-e`, `-r`, `-w`, `-x`, `-s`.

### case

Always include a `*)` usage/default branch.
""",
        "[[ vs [ with spaces; guard.sh preconditions; case CLI; arithmetic if",
    ),
    (
        6,
        "loops-ifs-and-safe-line-reading",
        "Loops, IFS, and Safe Line Reading",
        "Module 2: Control Flow and Structure",
        "intermediate",
        "45 min",
        "shell-loops",
        ["loops", "ifs"],
        "for/while loops, IFS, read -r, nullglob, and safe iteration over files and command output.",
        "Loops amplify quoting mistakes. Iterate safely over names with spaces and empty globs.",
        """### Patterns

```bash
shopt -s nullglob
for f in *.log; do
  [[ -e "$f" ]] || continue
  process "$f"
done

while IFS= read -r line; do
  printf '%s\\n' "$line"
done < file.txt
```

Never parse `ls`. Prefer globs, `find -print0` + `read -d ''`, or arrays.
""",
        "nullglob; while-read; iterate args; process substitution counts",
    ),
    (
        7,
        "functions-locals-and-small-libraries",
        "Functions, Locals, and Small Libraries",
        "Module 2: Control Flow and Structure",
        "intermediate",
        "45 min",
        "shell-functions",
        ["functions", "libraries"],
        "Functions with local scope, return codes, sourced lib/*.sh, and readonly constants.",
        "Functions turn scripts into reviewable units and enable small shared libraries for ops toolkits.",
        """### local and return

```bash
log() { printf '[%s] %s\\n' "$(date -Iseconds)" "$*" >&2; }
exists() { local f="$1"; [[ -e "$f" ]]; }
```

Use `return` for status; print data on stdout.

### Libraries

```bash
# shellcheck source=lib/common.sh
source "${ROOT}/lib/common.sh"
```

Keep libraries idempotent; avoid side effects at source time.
""",
        "log/die helpers; local vs global; source a lib; readonly ROOT",
    ),
    (
        8,
        "arguments-and-getopts",
        "Arguments and getopts",
        "Module 3: Script Interfaces",
        "intermediate",
        "50 min",
        "shell-getopts",
        ["getopts", "cli"],
        "Parse flags with getopts, forward \"$@\", build --help, and structure subcommands.",
        "A script without a clear interface becomes tribal knowledge. getopts and usage text are the UI.",
        """### getopts

```bash
while getopts ':hv:' opt; do
  case "$opt" in
    h) usage; exit 0 ;;
    v) VERBOSE=1 ;;
    :) echo "missing -$OPTARG" >&2; exit 2 ;;
    \\?) echo "unknown -$OPTARG" >&2; exit 2 ;;
  esac
done
shift $((OPTIND - 1))
```

Long options need a manual loop or an external parser; document the choice.

### Subcommands

`case "$1" in start|stop|status)` after option parsing.
""",
        "usage function; getopts -v; remaining args; subcommand dispatch",
    ),
    (
        9,
        "arrays-and-associative-arrays",
        "Arrays and Associative Arrays",
        "Module 3: Script Interfaces",
        "intermediate",
        "45 min",
        "shell-arrays",
        ["arrays"],
        "Indexed and associative arrays for host lists, maps, and safe iteration.",
        "Arrays store lists without IFS pain — essential for multi-host ops scripts (Bash 4+).",
        """### Indexed arrays

```bash
hosts=(app01 app02 app03)
hosts+=("app04")
for h in "${hosts[@]}"; do echo "$h"; done
```

### Associative arrays

```bash
declare -A ports=([api]=8080 [web]=80)
echo "${ports[api]}"
```

Requires Bash 4+. macOS system Bash 3.2 lacks them — use Linux for this track.
""",
        "build host array; assoc map; iterate keys; join with printf",
    ),
    (
        10,
        "text-pipelines-inside-scripts",
        "Text Pipelines Inside Scripts",
        "Module 3: Script Interfaces",
        "intermediate",
        "50 min",
        "shell-pipelines",
        ["grep", "awk", "jq"],
        "Compose grep/sed/awk/jq inside scripts — temp files versus pipes, and when not to parse ls.",
        "Ops scripts wrap text tools. Structure pipelines so failures and empty input are intentional.",
        """### Pipeline design

- Prefer pipes for streaming transforms
- Use temp files when you must rewind or run multiple passes
- `grep -q` in `if` for presence tests under `set -e`
- Prefer `jq` for JSON; do not invent parsers in Bash

### Anti-patterns

Parsing `ls`, counting with `wc` on untrusted binary input without care, and ignoring `pipefail`.
""",
        "log sample; grep ERROR; awk totals; optional jq; wrap in a function",
    ),
    (
        11,
        "traps-signals-temp-files-and-locking",
        "Traps, Signals, Temp Files, and Locking",
        "Module 4: Production Hardening",
        "intermediate",
        "50 min",
        "shell-traps",
        ["trap", "flock", "mktemp"],
        "trap cleanup, mktemp, flock mutual exclusion, and signal-safe ops scripts.",
        "Interrupted scripts leave temp junk and double-run cron jobs. Traps and locks make them house-trained.",
        """### trap

```bash
tmpdir=$(mktemp -d)
cleanup() { rm -rf "$tmpdir"; }
trap cleanup EXIT INT TERM
```

### flock

```bash
exec 9>/run/lock/myjob.lock
flock -n 9 || { echo "already running" >&2; exit 0; }
```

Exit `0` on lock contention for cron (avoid alert spam) or non-zero if overlap is a fault — document it.
""",
        "mktemp dir; EXIT trap; flock wrapper; simulate double start",
    ),
    (
        12,
        "logging-verbosity-and-exit-taxonomy",
        "Logging, Verbosity, and Exit Taxonomy",
        "Module 4: Production Hardening",
        "intermediate",
        "40 min",
        "shell-logging",
        ["logging"],
        "stderr versus stdout, log levels, verbosity flags, and machine-readable summaries for CI.",
        "Humans read logs; machines read exit codes and summary lines. Separate them deliberately.",
        """### Conventions

- **stdout** — primary data (when the script is a filter)
- **stderr** — logs and diagnostics
- Levels: `DEBUG`/`INFO`/`WARN`/`ERROR` gated by `-v`

### CI summaries

Print a final line like `RESULT status=ok files=12` on stdout or a known artefact for parsers.
""",
        "log helpers; -v flag; send logs to stderr; emit RESULT line; map exit codes",
    ),
    (
        13,
        "secure-shell-scripting",
        "Secure Shell Scripting",
        "Module 4: Production Hardening",
        "intermediate",
        "50 min",
        "shell-secure",
        ["security"],
        "Injection via unquoted expansions, avoiding eval, secrets handling, and least privilege.",
        "A script with root and unquoted expansions is a remote control for whoever controls the input file.",
        """### Rules

1. Quote expansions
2. Never `eval` untrusted input
3. Prefer arrays over string-building commands
4. Load secrets from env files with restricted permissions — do not `source` world-readable secret files casually
5. Drop privileges when root is unnecessary
6. Validate paths (`realpath`, prefix checks) before destructive ops

### Dangerous patterns

`rm -rf $TARGET`, `ssh $host $cmd`, building `bash -c "$user_string"`.
""",
        "show injection demo safely; rewrite with arrays; mode 600 env file; refuse relative destructive paths",
    ),
    (
        14,
        "cron-systemd-oneshots-and-timer-wrappers",
        "Cron, systemd oneshots, and Timer Wrappers",
        "Module 5: Ops and DevOps Patterns",
        "intermediate",
        "50 min",
        "shell-cron-systemd",
        ["cron", "systemd"],
        "Schedule hardened scripts via cron and systemd timers — PATH, idempotency, and oneshot units.",
        "Schedulers only run what you give them. Wrap jobs so environment, locking, and logging are explicit.",
        """### Cron checklist

Absolute paths, explicit `PATH`, mail/`LOGFILE`, locking, and a non-interactive shebang script.

### systemd

`Type=oneshot` service + timer. Prefer timers for dependency ordering and journaling.

Link to Linux [Cron and Task Scheduling](../linux/cron-and-task-scheduling.md) for scheduler depth; this tutorial focuses on the **script wrapper**.
""",
        "wrapper script with PATH+flock; user crontab line; optional systemd unit pair sketches",
    ),
    (
        15,
        "shell-in-ci-cd",
        "Shell in CI/CD",
        "Module 5: Ops and DevOps Patterns",
        "intermediate",
        "45 min",
        "shell-cicd",
        ["cicd", "gitlab"],
        "Fail-fast Bash in GitLab CI jobs — set -euo, artefacts, masking, and reusable script files.",
        "CI jobs are Bash under another name. Bring the same strictness you use on servers.",
        """### GitLab job tips

```yaml
script:
  - set -euo pipefail
  - ./scripts/ci/lint.sh
```

- Prefer repo scripts over huge inline YAML blocks
- Mask secrets; never `echo "$TOKEN"`
- Use artefacts for reports
- Fail fast; avoid `|| true` on critical steps

Continue with the [GitLab CI/CD](../gitlab/index.md) track for pipelines, runners, and security scanning.
""",
        "write ci-lint.sh; sketch .gitlab-ci.yml job; demonstrate fail-fast; note masking",
    ),
    (
        16,
        "capstone-ops-script-toolkit",
        "Capstone — Ops Script Toolkit",
        "Module 5: Ops and DevOps Patterns",
        "advanced",
        "60 min",
        "shell-capstone",
        ["capstone", "toolkit"],
        "Package a bin/ + lib/ ops toolkit: health check, backup with retention, and deploy preflight.",
        "Pull the track together into a small toolkit you could drop into a repo's `scripts/` directory.",
        """### Layout

```text
toolkit/
  bin/healthcheck
  bin/backup
  bin/preflight
  lib/common.sh
```

Shared logging, die, and lock helpers live in `lib/`. Each `bin/*` is a thin CLI.

### Behaviours

- healthcheck — verify files/ports/commands; exit non-zero on failure
- backup — tar + checksum + retention count
- preflight — validate env before deploy
""",
        "create layout; implement common.sh; three CLIs; run end-to-end; cleanup",
    ),
]


def related(num: int) -> str:
    by = {n: s for n, s, *_ in [(sp[0], sp[1], sp[2]) for sp in SPEC]}
    titles = {sp[0]: sp[2] for sp in SPEC}
    slugs = {sp[0]: sp[1] for sp in SPEC}
    links = ["- Track overview: [Shell Scripting](index.md)"]
    if num > 1:
        links.append(f"- Previous: [{titles[num-1]}]({slugs[num-1]}.md)")
    if num < 16:
        links.append(f"- Next: [{titles[num+1]}]({slugs[num+1]}.md)")
    links.append("- Linux: [Linux track](../linux/index.md)")
    links.append(
        "- Gateway: [Shell Scripting Fundamentals](../linux/shell-scripting-fundamentals.md)"
    )
    return "\n".join(links)


LAB_EXTRA: dict[int, str] = {
    1: dedent(
        """\
        ### Step 2 – Ops hello script

        ```bash
        cat > hello-ops.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "host=$(hostname -s) user=$(whoami) bash=${BASH_VERSION}"
        exit 0
        EOF
        chmod +x hello-ops.sh
        ./hello-ops.sh
        ```
        """
    ),
    2: dedent(
        """\
        ### Step 2 – Bashism under sh

        ```bash
        cat > bashism.sh << 'EOF'
        #!/bin/sh
        [[ -n "$HOME" ]] && echo ok
        EOF
        chmod +x bashism.sh
        ./bashism.sh || echo "failed under sh (expected)"
        bash bashism.sh
        ```

        ### Step 3 – Minimal env fingerprint

        ```bash
        cat > env-fingerprint.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        printf 'bash=%s path=%s\\n' "${BASH_VERSION}" "$PATH"
        command -v curl || echo 'curl=missing'
        EOF
        chmod +x env-fingerprint.sh
        env -i PATH=/usr/bin:/bin HOME="$HOME" ./env-fingerprint.sh
        ```
        """
    ),
    3: dedent(
        """\
        ### Step 2 – Spaces break unquoted expansions

        ```bash
        file='my file.txt'; touch "$file"
        ls $file || true
        ls "$file"
        ```

        ### Step 3 – Defaults and required vars

        ```bash
        name="${1:-operator}"; echo "hello $name"
        : "${HOME:?HOME required}"
        show() { printf 'argc=%s\\n' "$#"; printf '<%s>\\n' "$@"; }
        show one 'two three'
        ```
        """
    ),
    4: dedent(
        """\
        ### Step 2 – pipefail

        ```bash
        set +e
        false | true; echo "no pipefail => $?"
        set -o pipefail
        false | true; echo "pipefail => $?"
        set +o pipefail
        ```

        ### Step 3 – Strict checker

        ```bash
        cat > strict.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        f="${1:?usage: strict.sh FILE}"
        [[ -f "$f" ]] || { echo "missing $f" >&2; exit 2; }
        wc -l <"$f"
        EOF
        chmod +x strict.sh
        echo a > f.txt
        ./strict.sh f.txt
        ./strict.sh missing || echo exit=$?
        bash -x ./strict.sh f.txt 2>&1 | tail -15
        ```
        """
    ),
    5: dedent(
        """\
        ### Step 2 – Preconditions and case

        ```bash
        cat > guard.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        t="${1:?path required}"
        if [[ -d "$t" ]]; then echo directory
        elif [[ -f "$t" ]]; then echo "file $(wc -c <"$t") bytes"
        else echo "missing" >&2; exit 2; fi
        EOF
        chmod +x guard.sh
        ./guard.sh .
        case "${1:-status}" in status) echo ok ;; *) echo usage >&2; exit 2 ;; esac
        ```
        """
    ),
    6: dedent(
        """\
        ### Step 2 – nullglob and safe read

        ```bash
        shopt -s nullglob
        touch 'a log.log' 'b log.log'
        for f in *.log; do printf 'file=%s\\n' "$f"; done
        printf 'x\\ny z\\n' > lines.txt
        while IFS= read -r line; do printf 'line=<%s>\\n' "$line"; done < lines.txt
        ```
        """
    ),
    7: dedent(
        """\
        ### Step 2 – lib + functions

        ```bash
        mkdir -p lib
        cat > lib/common.sh << 'EOF'
        log() { printf '[%s] %s\\n' "$(date -Iseconds)" "$*" >&2; }
        die() { log "ERROR: $*"; exit 1; }
        EOF
        cat > main.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        ROOT="$(cd "$(dirname "$0")" && pwd)"
        # shellcheck source=lib/common.sh
        source "$ROOT/lib/common.sh"
        log "started"
        [[ $# -ge 1 ]] || die "need an argument"
        log "arg=$1"
        EOF
        chmod +x main.sh
        ./main.sh hello
        ./main.sh || echo exit=$?
        ```
        """
    ),
    8: dedent(
        """\
        ### Step 2 – getopts CLI

        ```bash
        cat > tool.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        VERBOSE=0
        usage() { echo "usage: $0 [-v] [-h] NAME"; }
        while getopts ':vh' opt; do
          case "$opt" in
            v) VERBOSE=1 ;;
            h) usage; exit 0 ;;
            \\?) usage >&2; exit 2 ;;
          esac
        done
        shift $((OPTIND - 1))
        name="${1:?name required}"
        (( VERBOSE )) && echo "verbose on" >&2
        echo "hello $name"
        EOF
        chmod +x tool.sh
        ./tool.sh -v Ada
        ./tool.sh || echo exit=$?
        ```
        """
    ),
    9: dedent(
        """\
        ### Step 2 – arrays

        ```bash
        hosts=(app01 app02)
        hosts+=("app03")
        for h in "${hosts[@]}"; do echo "host=$h"; done
        declare -A ports=([api]=8080 [web]=80)
        echo "api=${ports[api]}"
        for k in "${!ports[@]}"; do echo "$k -> ${ports[$k]}"; done
        ```
        """
    ),
    10: dedent(
        """\
        ### Step 2 – pipeline in a function

        ```bash
        printf '%s\\n' 'INFO ok' 'ERROR disk' 'ERROR mem' 'INFO done' > app.log
        count_errors() { grep -c ERROR "$1" || true; }
        echo "errors=$(count_errors app.log)"
        awk '/ERROR/ {c++} END {print c+0}' app.log
        ```
        """
    ),
    11: dedent(
        """\
        ### Step 2 – trap + flock

        ```bash
        cat > locked-job.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        tmp=$(mktemp -d)
        cleanup() { rm -rf "$tmp"; }
        trap cleanup EXIT INT TERM
        mkdir -p "$HOME/rebash-shell/locks"
        exec 9>"$HOME/rebash-shell/locks/job.lock"
        flock -n 9 || { echo "already running" >&2; exit 0; }
        echo work >"$tmp/out"
        sleep 1
        cat "$tmp/out"
        EOF
        chmod +x locked-job.sh
        ./locked-job.sh
        ```
        """
    ),
    12: dedent(
        """\
        ### Step 2 – log levels and RESULT

        ```bash
        cat > logger.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        VERBOSE=0
        log() { echo "[$1] $2" >&2; }
        [[ "${1:-}" == "-v" ]] && VERBOSE=1 && shift
        (( VERBOSE )) && log DEBUG "starting"
        log INFO "running"
        echo "RESULT status=ok"
        EOF
        chmod +x logger.sh
        ./logger.sh -v >/tmp/out.txt
        cat /tmp/out.txt
        ```
        """
    ),
    13: dedent(
        """\
        ### Step 2 – injection demo (safe)

        ```bash
        # Dangerous pattern (do not use with real rm):
        target='.'
        # Safe: quote and validate prefix
        root="$HOME/rebash-shell/lab13"
        mkdir -p "$root"
        target_path="$root/data"
        mkdir -p "$target_path"
        case "$(realpath "$target_path")" in
          "$root"/*) echo "safe path" ;;
          *) echo "refuse" >&2; exit 2 ;;
        esac
        ```
        """
    ),
    14: dedent(
        """\
        ### Step 2 – cron-ready wrapper

        ```bash
        cat > nightly.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        PATH=/usr/bin:/bin
        LOG="$HOME/rebash-shell/lab14/nightly.log"
        mkdir -p "$(dirname "$LOG")"
        exec >>"$LOG" 2>&1
        echo "run $(date -Iseconds)"
        EOF
        chmod +x nightly.sh
        ./nightly.sh
        # Example crontab line (do not install unless you intend to):
        # */15 * * * * $HOME/rebash-shell/lab14/nightly.sh
        ```
        """
    ),
    15: dedent(
        """\
        ### Step 2 – CI-style script + YAML sketch

        ```bash
        mkdir -p scripts
        cat > scripts/ci-lint.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "lint ok"
        EOF
        chmod +x scripts/ci-lint.sh
        ./scripts/ci-lint.sh
        cat > .gitlab-ci.yml.example << 'EOF'
        lint:
          image: debian:bookworm-slim
          script:
            - set -euo pipefail
            - ./scripts/ci-lint.sh
        EOF
        ```
        """
    ),
    16: dedent(
        """\
        ### Step 2 – toolkit layout

        ```bash
        mkdir -p toolkit/{bin,lib,data}
        cat > toolkit/lib/common.sh << 'EOF'
        log() { printf '[%s] %s\\n' "$(date -Iseconds)" "$*" >&2; }
        die() { log "ERROR: $*"; exit 1; }
        EOF
        cat > toolkit/bin/healthcheck << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        ROOT="$(cd "$(dirname "$0")/.." && pwd)"
        source "$ROOT/lib/common.sh"
        [[ -d "$ROOT/data" ]] || die "data dir missing"
        log "healthy"
        EOF
        cat > toolkit/bin/backup << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        ROOT="$(cd "$(dirname "$0")/.." && pwd)"
        source "$ROOT/lib/common.sh"
        ts=$(date +%Y%m%d%H%M%S)
        tar -czf "$ROOT/data/backup-$ts.tgz" -C "$ROOT" lib
        log "wrote backup-$ts.tgz"
        ls -1 "$ROOT/data"/backup-*.tgz | sort | head -n -3 | xargs -r rm -f
        EOF
        cat > toolkit/bin/preflight << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        ROOT="$(cd "$(dirname "$0")/.." && pwd)"
        source "$ROOT/lib/common.sh"
        command -v tar >/dev/null || die "tar missing"
        log "preflight ok"
        EOF
        chmod +x toolkit/bin/*
        ./toolkit/bin/preflight
        ./toolkit/bin/healthcheck
        ./toolkit/bin/backup
        ```
        """
    ),
}


def lab_block(num: int, slug: str, focus: str) -> str:
    extra = LAB_EXTRA.get(num, "")
    return dedent(
        f"""\
        Create a workspace for this tutorial.

        ```bash
        mkdir -p ~/rebash-shell/lab{num:02d} && cd ~/rebash-shell/lab{num:02d}
        ```

        **Focus:** {focus}

        ### Step 1 – Skeleton

        ```bash
        cat > lab.sh << 'EOF'
        #!/usr/bin/env bash
        set -euo pipefail
        echo "lab{num:02d} {slug} on $(hostname -s)"
        EOF
        chmod +x lab.sh
        ./lab.sh
        ```

        {extra}

        ### Final step – Trace and cleanup

        ```bash
        bash -x ./lab.sh 2>&1 | tail -n 20 || true
        # keep ~/rebash-shell for later labs
        ```
        """
    )


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
    prev_title = SPEC[num - 2][2] if num > 1 else "Linux command-line foundations"
    prereq = [
        prev_title if num > 1 else "Linux essentials (files, permissions, processes)",
        "Bash 4.2+ on Linux (WSL2/VM/cloud)",
    ]
    objectives = [
        f"Apply the core ideas of “{title}” in a real script",
        "Use strict mode and quoted expansions throughout the lab",
        "Produce clear stderr diagnostics and meaningful exit codes",
        "Debug behaviour with `bash -x` when something fails",
        "Relate this topic to day-to-day Linux admin and DevOps work",
    ]
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

This is **Tutorial {num}** in **{module}** of the REBASH Academy Shell Scripting series — written for Linux administrators and DevOps engineers who need production-grade Bash.

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

- [ ] Lab script runs with `set -euo pipefail`
- [ ] Failure path exits non-zero and prints to stderr
- [ ] `bash -x` trace is readable for the happy path
- [ ] You can explain this topic to a teammate without opening notes

## Code Walkthrough

Production Bash for **{title}** always combines:

1. A clear shebang (`#!/usr/bin/env bash`)
2. Strict mode near the top
3. Quoted expansions and explicit tests
4. Functions for reusable behaviour
5. Documented exit codes

Keep scripts short enough to review in a single merge request. When logic grows (JSON APIs, complex state), hand off to Python and keep Bash as the launcher.

## Security Considerations

- Treat all external input (args, files, env) as untrusted until validated
- Never log secrets; prefer masked CI variables
- Prefer least privilege — do not require root for file-local tasks
- Avoid `eval` and unquoted expansions in destructive commands

## Common Mistakes

!!! warning "Skipping strict mode"
    Cron and CI hide failures that an interactive terminal would show. **Fix:** start with `set -euo pipefail`.

!!! warning "Unquoted path expansions"
    Spaces and globs rewrite your command line. **Fix:** always `"$path"` / `"$@"`.

!!! warning "Assuming interactive PATH"
    Aliases and fancy PATH entries disappear under schedulers. **Fix:** set `PATH` or use absolute paths.

## Best Practices

- One purpose per script; compose with functions or small binaries
- Log to stderr; reserve stdout for data
- Idempotent behaviour where scheduling may overlap
- Pair every new script with a failing-path test you actually run
- Link related Linux tutorials for tools (grep/sed/awk, cron) instead of re-teaching them here

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

1. How does this topic show up in production Linux administration?
2. What failure mode appears if you ignore quoting or strict mode here?
3. How would you test this behaviour in CI?
4. When would you move this logic out of Bash?
5. What exit code contract would you document for teammates?

!!! tip "Sample answer — question 2"
    Unquoted expansions and missing `pipefail` create silent or partial failures — especially under cron — that look healthy in monitoring until data is wrong.

## Related Tutorials

{related(num)}

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- Track index: [Shell Scripting](index.md)
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(SPEC) == 16, len(SPEC)
    for sp in SPEC:
        path = OUT / f"{sp[1]}.md"
        path.write_text(render(sp), encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"done: {len(SPEC)} tutorials")


if __name__ == "__main__":
    main()
