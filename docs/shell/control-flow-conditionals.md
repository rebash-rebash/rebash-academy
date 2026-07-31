---
title: "Control Flow — Conditionals"
description: "Branch with if/elif/else, case, test/[ ], [[ ]], and logical operators for safe ops preconditions."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - if
  - case
  - test
prerequisites:
  - Input, Output, Redirection, and Pipes
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Control Flow — Conditionals

## Overview

Conditionals encode preconditions: file present, argument legal, disk free, service healthy. Prefer explicit tests over clever one-liners.

This is **Tutorial 5** in **Module 5: Control Flow** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Input, Output, Redirection, and Pipes
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Control Flow — Conditionals” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Control Flow — Conditionals](../assets/excalidraw/shell-control-flow.svg)

## Theory

### What it is

**Control flow** decides which commands run based on tests: file existence, string equality, exit status, or pattern matches. In Bash the main tools are `if` / `elif` / `else`, the POSIX `[ ]` (and `test`) command, Bash’s safer `[[ ]]` conditional, `case` for pattern matching, and the logical operators `&&` and `||`. Conditionals turn a linear script into decision-making automation — guard preconditions, choose CLI verbs, and exit with a clear status when something is wrong.

### Why it matters

Ops scripts must fail closed. Running a deployment when a config file is missing, or accepting an unknown subcommand, causes outages that a two-line guard would have prevented. Continuous Integration (CI) and systemd units rely on non-zero exits; conditionals are how you produce those exits with a human-readable reason on stderr. Choosing `[[ ]]` over brittle `[ ]` parsing also avoids subtle bugs with empty strings and pattern tests that waste debugging time.

### How it works

An `if` statement runs a command or test; a zero exit status means “true”. Prefer Bash `[[ ]]` in this course:

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

Use `case` for CLI verbs and status strings. Always include a `*)` default so unknown input fails loudly:

```bash
case "${1:-}" in
  start|stop|status) action=$1 ;;
  *) echo "usage: $0 start|stop|status" >&2; exit 2 ;;
esac
```

POSIX `[ -f "$f" ]` still appears in portable `sh` scripts — quote operands carefully. Inside Bash, `[[ ]]` offers safer parsing, `=~` regex matching, and `&&` / `||` within the brackets. Outside tests, `&&` runs the next command on success and `||` on failure; prefer a full `if` block when the body grows beyond one line.

### Key concepts

| Construct | Prefer when |
|-----------|-------------|
| `[[ ]]` | Bash scripts — safer tests, patterns, regex |
| `[ ]` / `test` | Strict POSIX `sh` portability |
| `if` / `elif` / `else` | Multi-branch decisions with clear exits |
| `case` | Matching verbs, statuses, or filename patterns |
| `&&` / `\|\|` | Short one-liners; not deep nesting |

Combine related checks: `[[ -n "$x" && -f "$x" ]]`.

### Common pitfalls

- Using `[ "$a" == "$b" ]` under dash — prefer `=` for POSIX, or `[[ ]]` in Bash
- Forgetting quotes so empty variables break `[` with “unary operator expected”
- Omitting a `*)` default in `case` and silently ignoring bad input
- Chaining long `&&` / `||` trees that obscure which check failed
- Testing interactive-only state (aliases, `tty`) inside scheduled scripts

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab05 && cd ~/rebash-shell/lab05
```

**Focus:** [[ vs [; guard preconditions; case CLI verbs; logical chains

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab05 control-flow-conditionals on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

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

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab05/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Control Flow — Conditionals** always combines:

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

**Control Flow — Conditionals** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md) *(previous)*
- [Loops — for, while, and until](loops-for-while-until.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
