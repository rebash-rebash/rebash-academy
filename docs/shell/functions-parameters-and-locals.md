---
title: "Functions, Parameters, and Locals"
description: "Declare Bash functions, pass parameters, return values via exit status and stdout, use local variables, and build reusable helpers."
difficulty: intermediate
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - functions
  - locals
  - reuse
prerequisites:
  - Loops — for, while, and until
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Functions, Parameters, and Locals

## Overview

Copy-paste blocks become drift. Small functions with locals keep ops libraries reviewable and testable.

This is **Tutorial 7** in **Module 7: Functions** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Loops — for, while, and until
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Functions, Parameters, and Locals” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Functions, Parameters, and Locals](../assets/excalidraw/shell-functions-locals.svg)

## Theory

### What it is

A **function** is a named block of commands you can call with arguments. Inside the function, positional parameters (`$1`, `$2`, `"$@"`) refer to those arguments. Functions report success or failure with `return` (an exit status from 0 to 255) and can emit data on stdout for the caller to capture. **Local variables** keep temporary state from leaking into the rest of the script. Shared helpers such as `log` and `die` become the backbone of readable ops automation.

### Why it matters

Copy-pasted command blocks drift apart: one path gains a timeout, another forgets quoting, and production only hits the broken copy. Functions give you a single place to fix behaviour, a clear contract for Continuous Integration (CI) callers, and smaller reviewable units. Using `local` prevents the subtle bug where a loop variable or temporary path overwrites a global and the next stage misbehaves. Libraries sourced from `lib/common.sh` let many scripts share the same logging and error style.

### How it works

Define functions before you call them. Prefer the `name()` form over `function name` for a consistent Bash style:

```bash
log() {
  printf '[%s] %s\n' "$(date -Iseconds)" "$*" >&2
}

die() {
  log "ERROR: $*"
  exit 1
}
```

Inside a function, `$1` and `"$@"` are the function’s arguments, not the script’s — forward explicitly when you need both. Use `return N` for status. For data, print to stdout and capture with `"$(fn arg)"`. Do not mix silent side effects with captured stdout, or callers will capture log noise.

Declare temporaries with `local var=value`. Without `local`, assignments affect the global script scope. Group reusable helpers in a small library file and `source` it from scripts that need them. Prefer a clear order: validate inputs → transform data → perform side effects. Document exit codes for helpers that call `exit` or `die`.

### Key concepts

| Idea | Practice |
|------|----------|
| Declaration | `name() { ... }` before first use |
| Parameters | `"$1"`, `"$@"` inside the function |
| Status | `return N` (0–255); data via stdout |
| `local` | Scope variables to the function |
| Libraries | `source lib/common.sh` for shared helpers |

### Common pitfalls

- Forgetting `local` so a helper clobbers a global path or counter
- Capturing `"$(log ...)"` and swallowing messages meant for stderr
- Using `exit` inside a sourced library when `return` would be safer for the caller
- Shadowing script positional parameters without documenting the hand-off
- Defining functions after `main` calls them under `set -e` and getting “command not found”

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab07 && cd ~/rebash-shell/lab07
```

**Focus:** log/die helpers; local vs global; source a tiny library

### Step 1 – Functions and locals

```bash
mkdir -p lib
cat > lib/common.sh << 'EOF'
log() { printf '[%s] %s\n' "$(date -Iseconds)" "$*" >&2; }
die() { log "ERROR: $*"; exit 1; }
add() {
  local a=$1 b=$2
  printf '%s\n' "$((a + b))"
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

### Final step – Cleanup note

```bash
# Keep ~/rebash-shell/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab07/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Functions, Parameters, and Locals** always combines:

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

**Functions, Parameters, and Locals** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Loops — for, while, and until](loops-for-while-until.md) *(previous)*
- [Arrays and String Manipulation](arrays-and-string-manipulation.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
