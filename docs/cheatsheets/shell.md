---
title: "Shell Scripting Cheat Sheet"
description: "Quick-reference Bash patterns for DevOps — syntax, variables, loops, functions, redirection, text tools, jq, yq, cron, and debugging."
difficulty: beginner
estimated_time: "10–15 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: cheatsheets
tags:
  - cheatsheets
  - shell
  - bash
  - jq
  - yq
  - cron
comments: false
---

# Shell Scripting Cheat Sheet

Scannable Bash reference for the [Shell Scripting for DevOps Engineers](../shell/index.md) track. Prefer tutorials when you need *why*, not only *how*.

## Overview

| Audience | When to use |
|----------|-------------|
| Linux admins, DevOps, SRE, platform engineers | Daily scripting, cron jobs, CI glue, quick ops automation |

## Quick reference

| Topic | Pattern |
|-------|---------|
| Shebang | `#!/usr/bin/env bash` |
| Strict mode | `set -euo pipefail` |
| Quote | `"$var"` · `"$@"` · never bare `$var` for paths |
| Defaults | `${var:-default}` · `${var:?required}` |
| Arithmetic | `$(( i + 1 ))` · `(( i++ ))` |
| Tests | `[[ -f $f ]]` · `[[ $a == "$b" ]]` |
| case | `case "$1" in start) ;; *) usage; exit 2;; esac` |
| Loops | `for f in "${arr[@]}"; do` · `while IFS= read -r line; do` |
| Functions | `fn() { local x="$1"; }` |
| Arrays | `a=(x y)` · `a+=("z")` · `declare -A m=([k]=v)` |
| Redirection | `cmd >out 2>err` · `cmd >>log 2>&1` · `cmd \| tee` |
| Trace | `bash -x ./script.sh` · `PS4='+${LINENO}: '` |
| Temp/clean | `tmp=$(mktemp -d)` · `trap 'rm -rf "$tmp"' EXIT` |
| Lock | `exec 9>lockfile` · `flock -n 9 \|\| exit 0` |
| Cron | set `PATH=`; absolute paths; no aliases |

## Bash syntax

``` {.bash .ra-terminal title="Terminal"}
#!/usr/bin/env bash
set -euo pipefail

usage() { echo "Usage: $0 <arg>" >&2; exit 2; }
[[ $# -ge 1 ]] || usage
```

| Construct | Notes |
|-----------|--------|
| `[[ ]]` | Bash conditional — prefer over `[ ]` in Bash scripts |
| `(( ))` | Integer arithmetic / numeric tests |
| `$( )` | Command substitution (quote when needed) |
| `source file` / `. file` | Load library functions |

!!! tip "Bash vs sh"
    On many Debian/Ubuntu systems `/bin/sh` is **dash**. Avoid Bashisms when the shebang is `#!/bin/sh`.

## Variables

```bash
name="Ada"
readonly CONST="prod"
export PATH="/usr/local/bin:/usr/bin:/bin"

echo "${name:-world}"
: "${REQUIRED:?REQUIRED must be set}"

# Indirect / lengths — avoid MkDocs-breaking length macros in docs;
# in real scripts, prefer counting via loops or tools when publishing Markdown.
count=0
for _ in "${items[@]+"${items[@]}"}"; do count=$((count + 1)); done
```

| Form | Meaning |
|------|---------|
| `"$var"` | Safe expansion |
| `"$@"` | All positional params, separately quoted |
| `"$*"` | Joined as one word (rarely what you want) |
| `${var#prefix}` | Strip shortest prefix |
| `${var##prefix}` | Strip longest prefix |
| `${var%suffix}` | Strip shortest suffix |
| `${var/pattern/repl}` | Replace once |

## Loops

``` {.bash .ra-terminal title="Terminal"}
for host in web db cache; do
  echo "$host"
done

while IFS= read -r line; do
  printf 'line=%s\n' "$line"
done < file.txt

until ping -c1 -W1 "$host" >/dev/null; do
  sleep 2
done
```

| Keyword | Use |
|---------|-----|
| `break` | Leave loop |
| `continue` | Next iteration |
| `nullglob` | `shopt -s nullglob` so unmatched globs expand empty |

## Functions

```bash
greet() {
  local whom="${1:-world}"
  echo "Hello, ${whom}"
}

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >&2; }
die() { log "ERROR: $*"; exit "${2:-1}"; }
```

- Prefer `local` for function variables
- Return status via `return` / `exit`; print data on stdout
- Share helpers with `source "${REPO_ROOT}/lib/common.sh"`

## Redirection and pipes

| Pattern | Effect |
|---------|--------|
| `>file` | stdout overwrite |
| `>>file` | stdout append |
| `2>file` | stderr only |
| `&>file` / `>file 2>&1` | both streams |
| `cmd1 \| cmd2` | pipe stdout |
| `cmd <file` | stdin from file |
| `cmd <<< "text"` | here-string |

``` {.bash .ra-terminal title="Terminal"}
grep ERROR app.log | tee -a errors.txt | wc -l
# Always enable pipefail in automation so mid-pipe failures surface
```

## Text processing

| Tool | Typical use |
|------|-------------|
| `grep -E` | Match lines |
| `sed -E` | Stream edit |
| `awk` | Columns / reports |
| `cut -d -f` | Field split |
| `tr` | Translate/delete chars |
| `sort \| uniq -c` | Frequency |
| `xargs -r` | Build command lines (GNU) |

``` {.bash .ra-terminal title="Terminal"}
df -P -x tmpfs | awk 'NR>1 {print $5, $6}'
journalctl -u nginx -n 200 --no-pager | grep -E 'error|crit'
```

## jq (JSON)

``` {.bash .ra-terminal title="Terminal"}
jq -r '.env' status.json
jq -r '.services[] | select(.status!="ok") | .name' status.json
jq -r '.services[] | [.name,.status] | @tsv' status.json
```

| Filter | Meaning |
|--------|---------|
| `.key` | Field |
| `.[]` | Iterate array |
| `select(expr)` | Filter |
| `@tsv` / `@csv` | Encode row |
| `-e` | Exit non-zero if false/null result (jq 1.6+) |

## yq (YAML)

Prefer **mikefarah/yq** v4 syntax:

``` {.bash .ra-terminal title="Terminal"}
yq -r '.app.name' app.yaml
yq -r '.app.image + ":" + .app.tag' app.yaml
yq -e '.app.replicas >= 1' app.yaml
```

!!! warning "Multiple yq tools exist"
    Confirm `yq --version`. Python `yq` wrappers differ from mikefarah/yq.

## Cron and timers

```cron
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash
*/5 * * * * /home/ops/bin/check-disk.sh 80 >>/home/ops/logs/disk.log 2>&1
```

| Tip | Why |
|-----|-----|
| Absolute paths | Cron PATH is minimal |
| Redirect both streams | Capture failures |
| `flock` | Prevent overlap |
| systemd timer | Better calendar + journaling on modern hosts |

```bash
# oneshot sketch
# ExecStart=/usr/local/bin/backup.sh
# OnCalendar=*-*-* 02:30:00
```

## Shell debugging

| Technique | Command / pattern |
|-----------|-------------------|
| Trace | `bash -x script.sh` |
| Verbose | `set -v` / `set -x` regionally |
| Line prompt | `export PS4='+${BASH_SOURCE}:${LINENO}: '` |
| Syntax check | `bash -n script.sh` |
| Static analysis | `shellcheck script.sh` |
| Exit probe | `echo exit=$?` after commands |

### Troubleshooting table

| Problem | Cause | Resolution |
|---------|-------|------------|
| Works in terminal, fails in cron | PATH/cwd/env | Set `PATH`, use absolute paths |
| `command not found` mid-script | `set -e` after failed lookup | Check `command -v` |
| Empty vars blow up | `set -u` | Provide defaults or `${var-}` carefully |
| Pipeline “succeeds” wrongly | No `pipefail` | `set -o pipefail` |
| Word-splitting bugs | Unquoted `$var` | Quote; use arrays / `read -r` |

## Production tips

- Log humans to **stderr**; emit `RESULT key=value` on **stdout** for CI
- Validate paths with prefix checks before `rm`/`mv`
- Prefer idempotent installs and dry-run flags
- Keep secrets in the environment or a secrets manager — never in git
- Run ShellCheck in CI

## Common mistakes

| Mistake | Correct approach |
|---------|------------------|
| `rm -rf $TARGET` | `rm -rf -- "$TARGET"` after validation |
| Bashisms under `#!/bin/sh` | Use `env bash` or stay POSIX |
| Relying on aliases in scripts | Use full commands / functions |
| Interactive `read` in cron | Fail fast; require args/config |

## Interview nuggets

- Explain `set -euo pipefail` in one minute
- Difference between `$@` and `$*`
- Why cron jobs see a different environment
- When to leave Bash for Python

## Related tutorials

- [Shell Fundamentals — Bash vs sh and Execution](../shell/shell-fundamentals-bash-vs-sh-and-execution.md)
- [Error Handling, Logging, and Debugging](../shell/error-handling-logging-and-debugging.md)
- [Production Shell Scripting](../shell/production-shell-scripting.md)
- Lab: [Shell Ops Script Hardening](../labs/shell-ops-script-hardening.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Learning path: [DevOps Engineer](../learning-paths/devops-engineer.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
- [jq manual](https://jqlang.github.io/jq/manual/)
- [mikefarah/yq](https://mikefarah.gitbook.io/yq/)
- [crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html)
