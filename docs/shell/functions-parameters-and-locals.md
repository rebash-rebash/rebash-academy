---
title: "Functions, Parameters, and Locals"
description: "Define Bash functions, pass parameters with $@ vs $*, use local variables, return status codes, and source a shared lib.sh."
difficulty: intermediate
estimated_time: "45–55 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: shell
technology: shell
module: "Module 7 · Functions"
tags:
  - shell
  - bash
  - functions
  - local
  - source
  - parameters
prerequisites:
  - shell/loops-for-while-until
next:
  - shell/arrays-and-string-manipulation
related:
  - shell/loops-for-while-until
  - shell/arrays-and-string-manipulation
comments: false
---

# Functions, Parameters, and Locals

## Overview

A **function** is a named block of commands you can call with arguments. Instead of copying the same ten lines into every script, you write the logic once, give it a name, and call it. Inside the function, **`$1`**, **`$2`**, and **`"$@"`** are the function’s arguments. **`local`** keeps temporary variables from leaking into the rest of the script. **`return`** sets an exit status (0–255). A small library file such as `lib.sh` can be loaded with **`source`** (or `.`) so many scripts share the same helpers. In this tutorial you will build `lib.sh`, call it from a main script, compare `"$@"` with `$*`, and prove return codes under `~/rebash-shell/lab07`.

Functions are how DevOps and platform teams keep Continuous Integration (CI) jobs and jump-server tools consistent. One `log` and one `die` helper means every script stamps time the same way and fails with a clear message on stderr. Without `local`, a helper can overwrite a global path variable and the next stage deletes or copies the wrong folder. Without a clear return status, callers cannot tell success from failure when stdout is captured for data.

In production, reviewers expect small, named units with documented exit codes. Prefer `return` for “this helper failed” and reserve `exit` for “the whole script must stop”. When a library is sourced, a careless `exit` inside a helper can kill the caller’s shell session if someone sources the library interactively — so design helpers carefully.

This is **Tutorial 7** in **Module 7: Functions** of the REBASH Academy **Shell Scripting for DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end, you will have a reusable library pattern you can show in an interview.

## Prerequisites

- [Loops — for, while, and until](loops-for-while-until.md)
- Bash 4.2+ on a practice Linux host
- Comfort with `set -euo pipefail` and quoting

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Declare a Bash function with `name() { … }` and call it with arguments
- [ ] Explain the difference between `"$@"` and `$*` / `"$*"` when forwarding parameters
- [ ] Use `local` so helper variables do not overwrite globals
- [ ] Return status codes with `return` and test them from the caller
- [ ] `source` a `lib.sh` library and prove shared helpers work from a main script

## Architecture

Scripts call functions; functions receive parameters, use locals, return status, and may live in a sourced library. The diagram shows that flow.

![Architecture diagram for Functions, Parameters, and Locals](../assets/excalidraw/shell-functions-locals.svg)

## Theory

### What it is

A function groups commands under a name. Prefer the portable-looking Bash form:

```bash
greet() {
  local who="$1"
  printf 'hello %s\n' "$who"
}
greet "alice"
```

Positional parameters inside the function refer to **that call**, not the script’s original `"$@"`, unless you forward them. **`local`** limits a variable to the function (and its nested calls in Bash). **`return N`** sets the function’s status; the caller checks `$?` or uses `if fn; then …`.

### Why it matters

Copy-pasted blocks drift: one path gains a timeout, another forgets quoting, and production only hits the broken copy. Functions give you a single place to fix behaviour and a clear contract for CI. Using `local` prevents the subtle bug where a loop variable or temporary path overwrites a global. Shared libraries (`source lib/common.sh`) keep logging and error style consistent across many tools on a jump server.

### How it works

1. **Define before use** — Bash reads the function definition before the first call.
2. **Parameters** — `"$1"`, `"$2"`, `"$@"` (each argument separate), `$*` / `"$*"` (joined).
3. **Locals** — `local var=value` near the top of the function.
4. **Status vs data** — `return` for status; print data on stdout for `"$(fn)"` capture; send logs to stderr.
5. **Libraries** — `source ./lib.sh` or `. ./lib.sh` loads definitions into the current shell.

```bash
log() {
  printf '[%s] %s\n' "$(date -Iseconds)" "$*" >&2
}

die() {
  log "ERROR: $*"
  return 1
}
```

**`"$@"` vs `$*`:** with arguments `a` and `b c`, `"$@"` stays two words (`a` and `b c`); unquoted `$*` or `$@` splits badly; `"$*"` becomes one word `a b c` (first character of `IFS` as joiner). When forwarding to another command, prefer `"$@"`.

### Key concepts and comparisons

| Idea | Practice |
|------|----------|
| Declaration | `name() { … }` before first use |
| Parameters | `"$1"`, `"$@"` inside the function |
| Status | `return N` (0–255); data via stdout |
| `local` | Scope variables to the function |
| Libraries | `source lib.sh` for shared helpers |

| Form | Meaning |
|------|---------|
| `"$@"` | Each parameter as its own word (preferred for forwarding) |
| `"$*"` | All parameters joined into one word |
| `$*` / `$@` (unquoted) | Unsafe splitting — avoid |

### Common pitfalls

- Forgetting `local` so a helper clobbers a global path or counter.
- Capturing `"$(log …)"` and swallowing messages meant for stderr.
- Using `exit` inside a sourced library when `return` would be safer for the caller.
- Shadowing script positional parameters without documenting the hand-off.
- Defining functions after `main` calls them and getting “command not found” under strict scripts.

## Hands-on Lab

### Objective

Under `~/rebash-shell/lab07`, create `lib.sh` with `log`, `dump_args`, and `require_file` helpers; call them from `main.sh`; prove `"$@"` vs `"$*"`, `local` isolation, and return codes with evidence files.

### Prerequisites

- Bash 4.2+, `chmod`, `date`
- Write access under your home directory

### Lab environment

Workspace: `~/rebash-shell/lab07`

```bash
mkdir -p ~/rebash-shell/lab07/out
cd ~/rebash-shell/lab07
set -euo pipefail
bash --version | head -n1 | tee out/bash-version.txt
```

**Expected output:** `out/bash-version.txt` mentions `bash`.

### Real-world scenario

Your platform team wants every ops script on the jump server to share one logging style and one “file must exist” check. You extract helpers into `lib.sh`, source them from `main.sh`, and attach proof that locals do not leak and that a missing file returns a non-zero status without killing an interactive demo carelessly.

### Step-by-step tasks

#### Task 1 – Build `lib.sh` with `local` and return codes

Create `lib.sh`:

```bash
#!/usr/bin/env bash
# Shared helpers for REBASH lab07 — source this file; do not execute alone.

log() {
  printf '[%s] %s\n' "$(date -Iseconds)" "$*" >&2
}

# Demonstrate $@ vs $* — write both forms for evidence
dump_args() {
  local mode="$1"
  shift
  case "$mode" in
    at)
      local a
      for a in "$@"; do
        printf 'AT:%s\n' "$a"
      done
      ;;
    star)
      printf 'STAR:%s\n' "$*"
      ;;
    *)
      log "unknown mode: $mode"
      return 2
      ;;
  esac
  return 0
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    log "missing file: $path"
    return 1
  fi
  return 0
}

# Deliberate local demo — sets a local name only
set_local_name() {
  local NAME="inside-function"
  printf '%s\n' "$NAME"
}
```

Run:

```bash
cd ~/rebash-shell/lab07
set -euo pipefail

# sanity: library is sourceable
# shellcheck disable=SC1091
source ./lib.sh
log "lib sourced"
```


**Expected output:** No error; a log line appears on stderr with a timestamp.

#### Task 2 – `main.sh` proves `"$@"`, `"$*"`, and locals

Create `main.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
# shellcheck disable=SC1091
source "$(dirname "$0")/lib.sh"

outdir="./out"
mkdir -p "$outdir"

NAME="global-name"
set_local_name | tee "$outdir/local-name.txt"
printf '%s\n' "$NAME" | tee "$outdir/global-name.txt"
grep -qx 'inside-function' "$outdir/local-name.txt"
grep -qx 'global-name' "$outdir/global-name.txt"

dump_args at "one" "two three" | tee "$outdir/args-at.txt"
dump_args star "one" "two three" | tee "$outdir/args-star.txt"
grep -c '^AT:' "$outdir/args-at.txt" | grep -qx 2
grep -qx 'STAR:one two three' "$outdir/args-star.txt"

require_file ./sample.txt
printf 'require_ok=1\n' | tee "$outdir/require-ok.txt"
```

Run:

```bash
cd ~/rebash-shell/lab07
set -euo pipefail

printf 'payload\n' > ./sample.txt

chmod +x main.sh
./main.sh
```


**Expected output:** `out/local-name.txt` is `inside-function`; `out/global-name.txt` stays `global-name`; `args-at.txt` has two `AT:` lines; `args-star.txt` is one joined `STAR:` line.

#### Task 3 – Failure path and evidence pack

```bash
cd ~/rebash-shell/lab07
set -euo pipefail
# shellcheck disable=SC1091
source ./lib.sh

set +e
require_file ./does-not-exist.txt
rc=$?
set -e
printf 'require_missing_rc=%s\n' "$rc" | tee out/require-missing-rc.txt
test "$rc" -eq 1

tar -czf out/functions-evidence.tgz \
  out/bash-version.txt out/local-name.txt out/global-name.txt \
  out/args-at.txt out/args-star.txt out/require-ok.txt out/require-missing-rc.txt \
  lib.sh main.sh
ls -l out/functions-evidence.tgz | tee out/evidence-ls.txt
```

**Expected output:** `require_missing_rc=1`; evidence archive is not empty.

### Validation steps

- [ ] `source lib.sh` works and `log` writes to stderr
- [ ] Global `NAME` unchanged after `set_local_name`
- [ ] `"$@"` path shows two `AT:` lines for `"one"` and `"two three"`
- [ ] Missing file returns status `1` and is recorded in `out/require-missing-rc.txt`

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: log` | Forgot `source lib.sh` | Source before calling helpers |
| Global variable changed | Missing `local` | Declare `local var=…` inside the function |
| `STAR` line split wrong | Used unquoted `$*` | Prefer `"$*"` for join demo; `"$@"` for forwarding |
| Script exits on missing file | `set -e` + `return 1` in direct call | Capture with `set +e` / `if ! require_file …; then` |
| `exit` kills interactive shell | Library used `exit` | Prefer `return` in sourced helpers |

### Challenge exercise

Add `retry()` to `lib.sh` with signature `retry <max> <command…>` that runs the command up to `max` times until it succeeds, logging each attempt to stderr, and returns `0` on success or `1` on final failure. Write `challenge-retry.sh` that uses `retry 3 true` (success) and proves a failing command (`retry 2 false`) returns non-zero. Save `out/retry-demo.txt` with both results.

### Learning outcomes

- Built and sourced a shared `lib.sh`
- Forwarded arguments safely with `"$@"` and contrasted `"$*"`
- Used `local` and `return` with proof files

### Cleanup

```bash
cd ~/rebash-shell/lab07
# Keep out/ and scripts for review, or:
# rm -rf ~/rebash-shell/lab07
```

## Validation

- [ ] Lab finished under `~/rebash-shell/lab07/` with evidence archive
- [ ] You can explain `"$@"` vs `"$*"` with a two-argument example
- [ ] You can explain why sourced libraries should prefer `return` over `exit`
- [ ] You know one production bug caused by missing `local`

## Code Walkthrough

Production Bash for **functions** usually follows this order:

1. **Shared helpers first** — `log`, `die` / `require_*` in a small library  
2. **`local` by default** — every temporary in a function is local unless exported on purpose  
3. **Status and data separated** — `return` for status; stdout for data; stderr for logs  
4. **Forward with `"$@"`** — after `shift` when peeling options  
5. **Thin `main`** — parse args, call functions, exit with the final status  

Configuration management can distribute the same `lib.sh` to many hosts. Keep the public helper names stable.

## Security Considerations

- Validate arguments before using them in paths or commands  
- Never log secrets in `log "$*"` helpers — mask tokens  
- Prefer least privilege; helpers should not assume root  
- Treat sourced libraries as code execution — only source trusted paths  
- Avoid `eval` inside helpers that accept user input  

## Common Mistakes

!!! warning "Forgetting `local`"
    A helper overwrites `file`, `i`, or `path` used by the caller. **Fix:** `local` every temporary; name globals in `UPPER_SNAKE` sparingly.

!!! warning "Using `exit` in a sourced library"
    Interactive `source lib.sh` then a failing helper can kill the shell. **Fix:** `return` from helpers; let `main` decide on `exit`.

!!! warning "Forwarding with unquoted `$@`"
    Arguments with spaces split. **Fix:** always `"$@"`.

!!! warning "Mixing logs into stdout"
    `"$(fn)"` captures log lines as data. **Fix:** logs to stderr (`>&2`).

## Best Practices

- One library for logging and fatal errors across a team’s scripts  
- Document return codes in a one-line comment above each helper  
- Keep functions short enough to review in a pull request  
- Run ShellCheck (including sourced files) in CI  
- Version or pin shared libraries when many repos depend on them  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `log: command not found` | Not sourced / wrong path | Fix `source` path; use `"$(dirname "$0")/lib.sh"` |
| Global changed after call | Missing `local` | Add `local`; re-test with before/after files |
| Wrong number of args forwarded | Used `"$*"` or unquoted | Use `"$@"` |
| `set -e` aborts on `return 1` | Expected failure not handled | `if ! fn; then …; fi` |
| Captured output includes timestamps | Logged to stdout | Redirect logs to stderr |

## Summary

Functions turn copy-paste into named, testable units. Use `"$@"` to forward arguments, `local` to protect callers, `return` for status, and `source lib.sh` for shared helpers — then prove behaviour with evidence. Next, store lists cleanly with [Arrays and String Manipulation](arrays-and-string-manipulation.md).

## Interview Questions

**1. What is the difference between `"$@"` and `"$*"` inside a function?**

??? success "Reveal answer"
    **`"$@"`** expands to each argument as a separate word, preserving spaces inside an argument. **`"$*"`** joins all arguments into a **single** word using the first character of `IFS` (usually space). Forward to other commands with `"$@"`. Use `"$*"` only when you intentionally want one combined string (for example a log message).

**2. Why should helpers in a sourced library prefer `return` over `exit`?**

??? success "Reveal answer"
    **`exit` ends the whole shell process.** If an operator runs `source lib.sh` in an interactive session, or a wrapper sources the library, `exit` can kill more than the intended script. **`return`** only ends the function (or the sourced script context) and lets the caller decide whether to exit. Reserve `exit` for the top-level `main` path.

**3. How does missing `local` cause a production bug?**

??? success "Reveal answer"
    A function that sets `path=/tmp/work` without `local` overwrites the caller’s `path`. The next stage may `rm -rf "$path"` on the wrong directory. The bug is intermittent and hard to see because each function looks fine alone. Always `local` temporaries and prove with a before/after global check in tests.

**4. How do you return data and status from the same function cleanly?**

??? success "Reveal answer"
    Print **data on stdout**, send **logs to stderr**, and use **`return`** for status. Callers use `value="$(fn)"` and check `$?` or `if value="$(fn)"; then`. Do not encode status only in stdout strings if callers need a real exit code for `set -e` and CI.

**5. What happens to positional parameters when you enter a function?**

??? success "Reveal answer"
    Inside the function, `$1`, `$2`, and `"$@"` refer to the **function arguments**, not the script’s original arguments. To use both, save script args first (`local -a SCRIPT_ARGS=("$@")` in `main` before calling helpers) or pass them explicitly into the function.

**6. How would you structure shared logging for twenty ops scripts on a bastion host?**

??? success "Reveal answer"
    Put `log` / `die` / `require_file` in a versioned `lib.sh` (or `/usr/local/lib/rebash/common.sh`), source it with an absolute or script-relative path, and keep stdout clean for machine output. Ship the library with configuration management and test it with a small `main.sh` smoke job like this lab.

**7. When is `return 2` better than `return 1`?**

??? success "Reveal answer"
    Use **different non-zero codes** when callers must distinguish failure classes (for example `1` = missing file, `2` = bad usage, `3` = timeout). Document the contract in comments and in your team runbook. Many programs use `2` for misuse of options; keep the convention consistent inside your toolkit.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Overview](index.md)
- [Loops — for, while, and until](loops-for-while-until.md) *(previous)*
- [Arrays and String Manipulation](arrays-and-string-manipulation.md) *(next)*
- [Error Handling, Logging, and Debugging](error-handling-logging-and-debugging.md)

## References

- [Bash functions (GNU Bash manual)](https://www.gnu.org/software/bash/manual/html_node/Shell-Functions.html)  
- [Bash `local` builtin](https://www.gnu.org/software/bash/manual/html_node/Bash-Builtins.html)  
- [ShellCheck](https://www.shellcheck.net/)  
- Track index: [Shell Scripting for DevOps Engineers](index.md)
