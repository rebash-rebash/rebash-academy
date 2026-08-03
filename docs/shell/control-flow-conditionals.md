---
title: "Control Flow — Conditionals"
description: "Branch safely in Bash with if/elif/else, [[ ]], test/[ ], and case for DevOps preconditions and CLI verbs."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: shell
technology: shell
module: "Module 5 · Control Flow"
tags:
  - shell
  - bash
  - conditionals
  - test
  - case
prerequisites:
  - shell/input-output-redirection-and-pipes
next:
  - shell/loops-for-while-until
related:
  - shell/input-output-redirection-and-pipes
  - shell/loops-for-while-until
comments: false
---

# Control Flow — Conditionals

## Overview

**Control flow** decides which commands run based on tests: is a file present, is an argument empty, did the last command succeed, which subcommand did the user ask for? In Bash the main tools are `if` / `elif` / `else`, the POSIX `test` / `[ ]` command, Bash’s safer **`[[ ]]`** conditional, and **`case`** for pattern matching on strings such as CLI verbs.

Ops scripts must **fail closed**. Running a deploy when a config file is missing, or accepting an unknown action quietly, causes outages that a two-line guard would have prevented. Continuous Integration (CI) and systemd units rely on non-zero exits; conditionals are how you produce those exits with a clear reason on stderr. Prefer `[[ ]]` in this course for string and file tests — it handles empty strings and pattern matching more safely than classic `[ ]`.

A practical pattern on Indian and global platform teams is a small wrapper script: check arguments with `[[ -z ... ]]`, verify files with `[[ -f ... ]]`, then `case "$action" in start|stop|status)` to dispatch. That same shape appears in deployment helpers, backup wrappers, and jump-server utilities.

This is **Tutorial 5** in **Module 5: Control Flow** of the REBASH Academy **Shell Scripting for DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end you will ship a branching script with file tests, string tests, and a `case` dispatcher.

## Prerequisites

- [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md)
- Comfort with arguments, exit codes, and `set -euo pipefail`
- Practice Ubuntu 22.04/24.04 with Bash

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Write `if` / `elif` / `else` branches with Bash `[[ ]]`
- [ ] Test files and strings with `[[ -f ]]`, `[[ -z ]]`, `[[ -n ]]`, and POSIX `test` where useful
- [ ] Combine conditions with `&&` and `||` inside `[[ ]]`
- [ ] Dispatch CLI verbs with a `case` statement and a default `*)` branch
- [ ] Return clear non-zero exit codes when preconditions fail

## Architecture

Conditionals sit between inputs (args, files, command statuses) and the actions your script allows. Guards run first; `case` selects a verb; failures exit before side effects.

![Architecture diagram for Control Flow — Conditionals](../assets/excalidraw/shell-control-flow.svg)

## Theory

### What it is

An `if` statement runs a command or test. Exit status **0** means “true”; non-zero means “false”.

```bash title="Terminal"
if [[ -f "$cfg" ]]; then
  printf 'config ok\n'
elif [[ -z "${cfg:-}" ]]; then
  printf 'config path empty\n' >&2
  exit 2
else
  printf 'missing config: %s\n' "$cfg" >&2
  exit 3
fi
```

Common `[[ ]]` tests:

| Test | True when |
|------|-----------|
| `[[ -f $f ]]` | Regular file exists (still quote: `"$f"`) |
| `[[ -d $d ]]` | Directory exists |
| `[[ -z $s ]]` | String length is zero |
| `[[ -n $s ]]` | String length is non-zero |
| `[[ $a == $b ]]` | Strings equal (quote both) |
| `[[ $a != $b ]]` | Strings differ |
| `[[ $s == pat* ]]` | Pattern match (Bash) |

POSIX `[ -f "$f" ]` / `test -f "$f"` still matter for `#!/bin/sh` scripts. This course prefers `[[ ]]` under Bash.

`case` matches patterns:

```bash
case "$1" in
  start)  echo start ;;
  stop)   echo stop ;;
  status) echo status ;;
  *)      echo "unknown: $1" >&2; exit 2 ;;
esac
```

### Why it matters

Without guards, scripts assume the world is healthy. Disks fill, configs vanish, humans typo verbs. Conditionals turn those realities into controlled exits (`2` usage, `3` missing file) instead of half-applied changes. Interviewers and seniors look for fail-closed design: unknown action → error, not silent no-op.

### How it works

1. **Validate inputs** — `$#`, `[[ -z "${1:-}" ]]`.  
2. **Check preconditions** — files, directories, required tools (`command -v`).  
3. **Branch** — `if`/`elif`/`else` for multi-way logic.  
4. **Dispatch verbs** — `case` for CLI subcommands.  
5. **Exit with meaning** — non-zero + stderr message before any destructive work.  

`[[ a && b ]]` and `[[ a || b ]]` combine tests inside `[[ ]]`. Outside, `cmd1 && cmd2` runs `cmd2` only if `cmd1` succeeds — useful, but keep complex logic in `if` for readability.

Under `set -e`, a failing command in the `if test;` position does **not** abort the script; it selects the `else` path. That is intentional. Still keep strict mode for the rest of the body.

### Key concepts and comparisons

| Construct | Prefer when | Avoid when |
|-----------|-------------|------------|
| `[[ ]]` | Bash scripts in this course | Strict POSIX `sh` only |
| `[ ]` / `test` | Portable `#!/bin/sh` | Complex pattern matching |
| `if` / `elif` | File/string/numeric decisions | Long lists of equal string verbs |
| `case` | Subcommands and pattern lists | Deep boolean trees better as `if` |
| `*)` default | Always | Silent fall-through with no error |

### Common pitfalls

- Using `[ -f $f ]` unquoted when `$f` is empty — syntax errors.  
- Writing `==` inside `[ ]` portably — prefer `=` for POSIX `[ ]`, or use `[[ ]]`.  
- Forgetting the `*)` branch in `case`, so typos do nothing.  
- Putting side effects before the guard checks.  
- Using `[[ ]]` under `#!/bin/sh` on Ubuntu dash.

## Hands-on Lab

### Objective

Build a small service-helper style script under `~/rebash-shell/lab05` that validates arguments, checks a config file with `[[ -f ]]` / empty tests, branches with `if`/`elif`/`else`, and dispatches actions with `case`.

### Prerequisites

- Ubuntu 22.04/24.04 with Bash  
- Modules 2–4 skills  
- No root required  

### Lab environment

Workspace: `~/rebash-shell/lab05`

```bash title="Terminal"
mkdir -p ~/rebash-shell/lab05 && cd ~/rebash-shell/lab05
set -euo pipefail
whoami | tee lab-user.txt
mkdir -p conf
printf 'mode=lab\n' > conf/app.conf
```

!!! example "Expected output"
    `conf/app.conf` exists; workspace ready.


### Real-world scenario

Your team wants a tiny wrapper, `svcctl.sh`, for a practice app: actions `start`, `stop`, and `status`. It must refuse to run without an action, refuse unknown actions, and require `conf/app.conf` before `start`. You implement the guards and keep proof of allow and deny paths.

### Step-by-step tasks

#### Task 1 – File and empty-string tests with if/elif/else

Create `precondition.sh`:

```bash title="precondition.sh"
#!/usr/bin/env bash
set -euo pipefail

cfg="${1:-}"

if [[ -z "$cfg" ]]; then
  printf 'error: config path is empty\n' >&2
  exit 2
elif [[ -f "$cfg" ]]; then
  printf 'ok: config file present\n' | tee precheck-ok.txt
  exit 0
elif [[ -d "$cfg" ]]; then
  printf 'error: path is a directory: %s\n' "$cfg" >&2
  exit 3
else
  printf 'error: config not found: %s\n' "$cfg" >&2
  exit 3
fi
```

Run:

```bash title="Terminal"
cd ~/rebash-shell/lab05
set -euo pipefail

chmod +x precondition.sh

./precondition.sh conf/app.conf
grep -q 'config file present' precheck-ok.txt

set +e
./precondition.sh >empty.stdout 2>empty.stderr
rc_empty=$?
./precondition.sh conf/missing.conf >miss.stdout 2>miss.stderr
rc_miss=$?
set -e

echo "empty_exit=$rc_empty" | tee precheck-empty-exit.txt
echo "missing_exit=$rc_miss" | tee precheck-missing-exit.txt
test "$rc_empty" -eq 2
test "$rc_miss" -eq 3
grep -q 'empty' empty.stderr
grep -q 'not found' miss.stderr
```


!!! example "Expected output"
    success path writes `precheck-ok.txt`; empty path exits `2`; missing file exits `3`.


#### Task 2 – case statement on CLI args

Create `svcctl.sh`:

```bash title="svcctl.sh"
#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf 'Usage: %s <start|stop|status>\n' "$0" >&2
  exit 2
}

if [[ $# -lt 1 ]]; then
  usage
fi

action="$1"
cfg="conf/app.conf"

case "$action" in
  start)
    if [[ ! -f "$cfg" ]]; then
      printf 'error: missing %s\n' "$cfg" >&2
      exit 3
    fi
    printf 'action=start config=%s\n' "$cfg" | tee last-action.txt
    ;;
  stop)
    printf 'action=stop\n' | tee last-action.txt
    ;;
  status)
    if [[ -f "$cfg" ]]; then
      printf 'action=status state=configured\n' | tee last-action.txt
    else
      printf 'action=status state=missing-config\n' | tee last-action.txt
    fi
    ;;
  *)
    printf 'error: unknown action: %s\n' "$action" >&2
    usage
    ;;
esac

exit 0
```

Run:

```bash title="Terminal"
cd ~/rebash-shell/lab05
set -euo pipefail

chmod +x svcctl.sh

./svcctl.sh start
grep -q 'action=start' last-action.txt
./svcctl.sh status
grep -q 'state=configured' last-action.txt

set +e
./svcctl.sh restart >unknown.stdout 2>unknown.stderr
rc_unknown=$?
./svcctl.sh >noarg.stdout 2>noarg.stderr
rc_noarg=$?
set -e

echo "unknown_exit=$rc_unknown" | tee case-unknown-exit.txt
echo "noarg_exit=$rc_noarg" | tee case-noarg-exit.txt
test "$rc_unknown" -eq 2
test "$rc_noarg" -eq 2
grep -q 'unknown action' unknown.stderr
grep -q 'Usage:' noarg.stderr
```


!!! example "Expected output"
    `start` and `status` succeed; unknown and missing-arg paths exit `2` with stderr messages.


#### Task 3 – Combine tests and pack evidence

```bash title="Terminal"
cd ~/rebash-shell/lab05
set -euo pipefail

# Negative start path: remove config temporarily
mv conf/app.conf conf/app.conf.bak
set +e
./svcctl.sh start >start-miss.stdout 2>start-miss.stderr
rc_start_miss=$?
set -e
mv conf/app.conf.bak conf/app.conf
echo "start_missing_config_exit=$rc_start_miss" | tee start-miss-exit.txt
test "$rc_start_miss" -eq 3
grep -q 'missing' start-miss.stderr

# POSIX test equivalent check (still under Bash)
test -f conf/app.conf
test -z "" 
test -n "x"

tar -czf conditionals-evidence.tgz \
  lab-user.txt precheck-ok.txt precheck-empty-exit.txt precheck-missing-exit.txt \
  last-action.txt case-unknown-exit.txt case-noarg-exit.txt start-miss-exit.txt \
  empty.stderr miss.stderr unknown.stderr noarg.stderr start-miss.stderr
ls -l conditionals-evidence.tgz | tee evidence-ls.txt
```

!!! example "Expected output"
    start without config exits `3`; evidence archive is non-empty; `conf/app.conf` is restored.


### Validation steps

- [ ] `precondition.sh` distinguishes empty, present, and missing paths  
- [ ] `svcctl.sh` supports `start|stop|status`  
- [ ] Unknown action and missing args exit `2`  
- [ ] `start` without config exits `3`  
- [ ] `conditionals-evidence.tgz` exists under `~/rebash-shell/lab05`  

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `[[: too many arguments` / syntax error | Unquoted empty test in `[ ]` | Use `[[ -z "${var:-}" ]]` |
| Unknown action exits 0 | Missing `*)` branch | Add default error + usage |
| `set -e` aborts inside `if` unexpectedly | Misplaced failing command | Keep tests in `if [[ ... ]]` |
| `start` ignores missing config | Guard after side effects | Check `[[ -f ]]` before work |

### Challenge exercise

Extend `svcctl.sh` into `svcctl-v2.sh` that accepts an optional second argument `env` (`lab|staging|prod`, default `lab`), rejects other env values with exit `2`, writes `last-action.txt` including `env=...`, and adds a `reload` action that requires the config file like `start`. Keep `set -euo pipefail` and a `case` dispatcher.

### Learning outcomes

- Used `[[ -z ]]` / `[[ -f ]]` with `if`/`elif`/`else`  
- Built a `case` based CLI with a fail-closed default  
- Proved allow and deny paths with exit codes and stderr  

### Cleanup

```bash title="Terminal"
cd ~/rebash-shell/lab05
rm -f empty.stdout miss.stdout unknown.stdout noarg.stdout start-miss.stdout
# Keep svcctl.sh and evidence, or:
# rm -rf ~/rebash-shell/lab05
```

## Validation

- [ ] Lab finished under `~/rebash-shell/lab05/` with evidence files  
- [ ] You can explain `[[ ]]` vs `[ ]` / `test`  
- [ ] You can write an `if`/`elif`/`else` guard and a `case` dispatcher  
- [ ] You know why a default `*)` branch matters in production wrappers  

## Code Walkthrough

Production conditional design usually follows this order:

1. **Parse args** — count and emptiness checks first  
2. **Fail closed** — unknown verbs and missing files exit before changes  
3. **Prefer `[[ ]]`** in Bash for readable, safer tests  
4. **Use `case` for verbs** — one pattern per action, always include `*)`  
5. **Send reasons to stderr** — keep stdout for data/`RESULT` if needed  
6. **Document exit codes** — `2` usage, `3` missing preconditions (example contract)  

Loops (next module) will reuse these tests inside `for` / `while`. Get the guards right once, then iterate.

## Security Considerations

- Validate actions against an allow-list (`case`), not free-form `eval`  
- Check file paths stay under expected directories before writing  
- Do not take raw user strings into destructive commands without checks  
- Fail closed on missing config rather than creating insecure defaults silently  
- Log denied actions (unknown verb) for audit on shared jump servers  

## Common Mistakes

!!! warning "Missing `*)` in `case`"
    Typos become silent no-ops. **Fix:** default branch prints an error and exits non-zero.

!!! warning "Unquoted tests with empty values"
    `[ -f $f ]` breaks when `$f` is empty. **Fix:** `[[ -f "$f" ]]` or `[ -f "$f" ]`.

!!! warning "Side effects before guards"
    Partial deploys leave bad state. **Fix:** validate args and files first, then act.

!!! warning "Using `[[ ]]` under `#!/bin/sh`"
    dash rejects Bash conditionals. **Fix:** Bash shebang, or POSIX `[ ]` only.

## Best Practices

- One clear exit taxonomy for usage vs missing resources  
- Keep `case` patterns short; call functions per action as scripts grow  
- Prefer `[[ -f "$cfg" ]]` before reading or sourcing config  
- Write deny-path tests in CI for wrappers  
- Use ShellCheck to catch common `[ ]` mistakes  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `[[: not found` | Running under dash/`sh` | Fix shebang to Bash |
| Branch never taken | Wrong test (`-f` vs `-d`) | `ls -ld` the path; fix test |
| Script exits 0 on typo | No `*)` / usage | Add fail-closed default |
| `set -e` confusion with `if` | Expected abort on test failure | Remember `if` consumes the status |
| Empty string compares oddly | Unquoted expansion | Quote both sides in `[[ ]]` |

## Summary

Conditionals encode preconditions and CLI decisions. Use `[[ ]]` for Bash tests, `if`/`elif`/`else` for branching, and `case` for verbs with a mandatory default error path. Prove both allow and deny exits. Next, repeat work safely with [Loops — for, while, and until](loops-for-while-until.md).

## Interview Questions

**1. Why prefer `[[ ]]` over `[ ]` in Bash ops scripts?**

??? success "Reveal answer"
    **`[[ ]]`** is a Bash keyword with safer parsing: better behaviour with empty strings, `&&` / `||` inside the test, and pattern matching with `==`. Classic `[ ]` is a builtin/command compatible with POSIX `sh` but is easier to break with unquoted empty values. For Bash scripts in this course, prefer `[[ ]]`; for `#!/bin/sh` on dash, use `[ ]`.

**2. What do `[[ -f "$f" ]]` and `[[ -z "$s" ]]` mean?**

??? success "Reveal answer"
    **`-f`** is true when the path exists and is a regular file. **`-z`** is true when the string length is zero (empty). Always quote `"$f"` and `"$s"`. Typical use: reject missing config with `-f`, reject missing arguments with `-z` after you have safely read them (or test `$#` first under `set -u`).

**3. How does `case` improve a CLI wrapper compared with a long `if`/`elif` chain?**

??? success "Reveal answer"
    **`case`** matches a string against patterns (`start|stop|status`) and includes a clear **`*)`** default for unknowns. It is easier to read for verb dispatch than many `elif [[ "$1" == ... ]]` lines. Interviewers look for the default branch that errors instead of doing nothing.

**4. Under `set -e`, does a failing test inside `if [[ ... ]]` abort the script?**

??? success "Reveal answer"
    No. In the `if` test position, a non-zero status selects the `else`/`elif` path instead of aborting. That lets you branch on failure safely. Commands **after** the tests still obey `set -e`. Design guards in `if`/`case`, then let strict mode protect the main body.

**5. A wrapper accepts any string as an action and sometimes runs dangerous cleanup. What control-flow fix do you apply?**

??? success "Reveal answer"
    Use an **allow-list** with `case` and a default `*)` that exits non-zero. Do not pass raw user text into `eval` or unquoted commands. Validate required files before cleanup. Fail closed on unknown verbs.

**6. How would you prove least-surprise behaviour for `svcctl.sh` in a change ticket?**

??? success "Reveal answer"
    Attach runs for: valid `start` with config present, `start` with config missing (non-zero), unknown action (non-zero + stderr), and missing args (usage on stderr). Show `last-action.txt` only for allowed paths. Least surprise means denied paths are explicit and successful paths leave clear evidence.

**7. When is POSIX `test` / `[ ]` still the right choice?**

??? success "Reveal answer"
    When the script must run under **`#!/bin/sh`** (dash) or a strict POSIX policy. Then avoid `[[ ]]`, use `[ -f "$f" ]`, and stick to portable operators. If the organisation standardises on Bash, `[[ ]]` is usually clearer for new ops scripts.

**8. How do you combine “file exists” and “variable non-empty” cleanly?**

??? success "Reveal answer"
    Prefer one `[[` expression: `if [[ -n "$cfg" && -f "$cfg" ]]; then ...`. Alternatively nest `if` statements for clearer error messages (empty vs missing file). Separate exit codes for usage (`2`) versus missing resources (`3`) help CI and humans respond correctly.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Overview](index.md)
- [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md) *(previous)*
- [Loops — for, while, and until](loops-for-while-until.md) *(next)*
- [Variables, Quoting, and Arithmetic](variables-quoting-and-arithmetic.md)

## References

- [GNU Bash manual — Conditional Constructs](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html)  
- [GNU Bash manual — Bash Conditional Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)  
- [`test(1)`](https://manpages.ubuntu.com/manpages/jammy/en/man1/test.1.html) — Ubuntu man-pages  
- [ShellCheck](https://www.shellcheck.net/)  
- Track index: [Shell Scripting for DevOps Engineers](index.md)
