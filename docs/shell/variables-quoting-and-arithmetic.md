---
title: "Variables, Quoting, and Arithmetic"
description: "Use Bash variables, quoting, defaults, arithmetic, readonly, and export safely in DevOps scripts."
difficulty: beginner
estimated_time: "50–60 min"
author: Shaik Basha
last_updated: "2026-08-02"
category: shell
technology: shell
module: "Module 3 · Variables"
tags:
  - shell
  - bash
  - variables
  - quoting
  - arithmetic
prerequisites:
  - shell/writing-your-first-script
next:
  - shell/input-output-redirection-and-pipes
related:
  - shell/writing-your-first-script
  - shell/input-output-redirection-and-pipes
comments: false
---

# Variables, Quoting, and Arithmetic

## Overview

Bash **variables** store values you assign once and expand later — host names, file paths, counters, and configuration from the environment. Most Bash values are strings. You still do integer maths with **arithmetic expansion** `$(( ))`. Related tools include **defaults** (`${var:-default}`), **readonly** constants, and **export** so child processes inherit a value.

**Quoting** decides whether an expansion stays one word or is split on spaces and matched as a file glob. This is not a style preference. An unquoted path with a space can become three arguments and delete the wrong files. Double quotes (`"$var"`) keep the value together and still allow expansion. Single quotes (`'$var'`) keep the text literal. For DevOps scripts, the safe default is: quote expansions unless you have a specific reason not to.

Environment variables such as `PATH`, `HOME`, and CI secrets are ordinary variables that were **exported**. A child script sees exported names; it does not see unexported shell-local names. Defaults such as `${REGION:-ap-south-1}` let the same script run in lab and production without editing the file — common on Indian and global cloud teams that promote one artefact across environments.

This is **Tutorial 3** in **Module 3: Variables** of the REBASH Academy **Shell Scripting for DevOps Engineers** series. It is written for Linux administrators, DevOps engineers, Site Reliability Engineering (SRE), and platform engineers. By the end you will demonstrate quoting bugs, safe defaults, arithmetic, and `readonly` / `export` with proof files.

## Prerequisites

- [Writing Your First Script](writing-your-first-script.md)
- Comfort with `set -euo pipefail` from Module 2
- Practice Ubuntu 22.04/24.04 with Bash

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Assign and expand variables with `"$var"` / `"${var}"` under strict mode
- [ ] Explain the difference between unquoted, double-quoted, and single-quoted expansions
- [ ] Use `${var:-default}` and related parameter expansions safely
- [ ] Perform integer arithmetic with `$(( ))`
- [ ] Use `readonly` and `export`, and show what child processes inherit

## Architecture

Variables and quoting sit between script inputs (args, env, files) and the commands those values reach. Wrong quoting changes the argument list the kernel sees.

![Architecture diagram for Variables, Quoting, and Arithmetic](../assets/excalidraw/shell-variables-quoting.svg)

## Theory

### What it is

Assign without spaces around `=`:

```bash
app_name=payments
region="${REGION:-ap-south-1}"
```

Expand with quotes in almost all ops code:

``` {.bash .ra-terminal title="Terminal"}
printf 'region=%s\n' "$region"
```

| Quoting | Expansion | Word-splitting / globbing |
|---------|-----------|---------------------------|
| unquoted `$var` | Yes | Yes — often dangerous |
| `"$var"` | Yes | No — usual safe choice |
| `'$var'` | No | No — literal characters |

Defaults and related forms:

| Form | Meaning |
|------|---------|
| `${var:-default}` | Use `default` if `var` is unset or empty |
| `${var:=default}` | Assign `default` if unset or empty, then expand |
| `${var:?message}` | Exit with error if unset or empty |
| `{{ '${#var}' }}` | Length of the string |

Arithmetic:

```bash
count=$(( count + 1 ))
product=$(( 6 * 7 ))
```

`readonly NAME=value` prevents later assignment. `export NAME=value` marks the name for child processes.

### Why it matters

Unquoted expansions break backup scripts, `rm` cleanups, and CI steps more often than exotic Bash features do. Schedulers pass paths and region names through variables. One missing quote turns a safe command into a surprise. Clear defaults and `export` contracts also make the same script configurable in lab, staging, and production without editing source on the server.

### How it works

1. **Assign** — `name=value` (no spaces around `=`).  
2. **Expand** — prefer `"$name"` or `"${name}"`.  
3. **Default** — `${name:-fallback}` when empty input should be allowed.  
4. **Export** — only names children must see.  
5. **Lock** — `readonly` for true constants such as a script version.  
6. **Count** — integer maths in `$(( ))`, not string concatenation tricks.

Command substitution captures stdout:

```bash
host="$(hostname -s)"
```

Prefer `$(...)` over legacy backticks. Quote the result: `"$host"`.

### Key concepts and comparisons

| Pattern | Prefer when | Avoid when |
|---------|-------------|------------|
| `"$path"` | Almost always for paths and args | Rare intentional splitting |
| `${var:-default}` | Optional config with a safe fallback | Secrets that must be present — use `${var:?}` |
| `export VAR=value` | Child processes need the value | Dumping secrets into every child |
| `readonly` | Constants that must not change | Values you reassign in loops |
| `$(( ))` | Integer counters and simple maths | Floating point (use `awk`/`bc` later) |

### Common pitfalls

- Writing `name = value` (spaces) — Bash tries to run a command named `name`.  
- Unquoted `$files` in `rm` or `mv` when names contain spaces.  
- Forgetting quotes around `"$(command)"` when output has spaces.  
- Using `${var:-default}` for secrets that must fail if missing — prefer `${var:?}`.  
- Assuming a child script sees unexported variables.

## Hands-on Lab

### Objective

Under `~/rebash-shell/lab03`, prove quoting differences, use defaults and arithmetic, and demonstrate `readonly` plus `export` inheritance with evidence files.

### Prerequisites

- Ubuntu 22.04/24.04 with Bash  
- Module 2 skills: shebang, `chmod +x`, `set -euo pipefail`  
- No root required  

### Lab environment

Workspace: `~/rebash-shell/lab03`

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-shell/lab03 && cd ~/rebash-shell/lab03
set -euo pipefail
whoami | tee lab-user.txt
```

!!! example "Expected output"
    workspace exists; `lab-user.txt` is written.


### Real-world scenario

A cleanup script deleted the wrong files because a directory name contained a space and the path was unquoted. Security also wants config defaults for region, and a proof that secrets are not exported to every child. You rebuild a safe demo with quoting, defaults, arithmetic, and export/readonly checks.

### Step-by-step tasks

#### Task 1 – Quoting differences with a path that contains a space

Create `quoting-demo.sh`:

```bash title="quoting-demo.sh"
#!/usr/bin/env bash
set -euo pipefail

path_with_space="data/my reports/summary.txt"

# Safe: one argument
printf 'safe_args='
printf '<%s> ' "$path_with_space"
printf '\n' | tee quoting-safe.txt

# Unsafe illustration: word-splitting (do not use this pattern for rm/mv)
# shellcheck disable=SC2086
printf 'unsafe_args='
printf '<%s> ' $path_with_space
printf '\n' | tee quoting-unsafe.txt

# Prove the file is readable only when quoted correctly
test -f "$path_with_space"
wc -l < "$path_with_space" | tee line-count.txt
```

Run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-shell/lab03
set -euo pipefail

mkdir -p "data/my reports"
printf 'line1\n' > "data/my reports/summary.txt"

chmod +x quoting-demo.sh
./quoting-demo.sh
grep -q '<data/my reports/summary.txt>' quoting-safe.txt
grep -q '<data/my>' quoting-unsafe.txt
```


!!! example "Expected output"
    Safe line shows one `<data/my reports/summary.txt>` argument; unsafe line splits into more than one `<>` chunk; `line-count.txt` is `1`.


#### Task 2 – Defaults and arithmetic

Create `defaults-math.sh`:

```bash title="defaults-math.sh"
#!/usr/bin/env bash
set -euo pipefail

# REGION may be unset in lab; default to Mumbai region code often used in India labs
region="${REGION:-ap-south-1}"
retries="${RETRIES:-3}"

# Integer arithmetic
attempt=0
attempt=$(( attempt + 1 ))
remaining=$(( retries - attempt ))

{
  echo "region=${region}"
  echo "retries=${retries}"
  echo "attempt=${attempt}"
  echo "remaining=${remaining}"
} | tee defaults-math.txt

# Empty override still triggers :- default
empty_region=""
echo "empty_fallback=${empty_region:-ap-south-1}" | tee -a defaults-math.txt

test "$remaining" -eq 2
```

Run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-shell/lab03
set -euo pipefail

chmod +x defaults-math.sh
./defaults-math.sh
REGION=eu-west-1 ./defaults-math.sh | tee defaults-math-override.txt
grep -q 'region=eu-west-1' defaults-math-override.txt
grep -q 'region=ap-south-1' defaults-math.txt
```


!!! example "Expected output"
    Default run uses `ap-south-1` and `remaining=2`; override run shows `eu-west-1`.


#### Task 3 – readonly and export to a child

Create `export-readonly.sh`:

```bash title="export-readonly.sh"
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_VERSION="1.0.0"
readonly SCRIPT_VERSION

export APP_ENV="lab"
LOCAL_ONLY="not-for-children"

# Child sees APP_ENV, not LOCAL_ONLY
bash -c 'echo "child_APP_ENV=${APP_ENV:-missing}"; echo "child_LOCAL_ONLY=${LOCAL_ONLY:-missing}"' \
  | tee child-env.txt

echo "SCRIPT_VERSION=${SCRIPT_VERSION}" | tee readonly-value.txt

# readonly must reject reassignment
set +e
SCRIPT_VERSION="2.0.0" >readonly-reassign.out 2>&1
rc=$?
set -e
echo "reassign_exit=$rc" | tee readonly-reassign-exit.txt
test "$rc" -ne 0
grep -qi 'readonly\|read-only\|readonly variable' readonly-reassign.out \
  || test -s readonly-reassign.out

grep -q 'child_APP_ENV=lab' child-env.txt
grep -q 'child_LOCAL_ONLY=missing' child-env.txt
```

Run:

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-shell/lab03
set -euo pipefail

chmod +x export-readonly.sh
./export-readonly.sh

tar -czf variables-evidence.tgz \
  lab-user.txt quoting-safe.txt quoting-unsafe.txt line-count.txt \
  defaults-math.txt defaults-math-override.txt \
  child-env.txt readonly-value.txt readonly-reassign-exit.txt
ls -l variables-evidence.tgz | tee evidence-ls.txt
```


!!! example "Expected output"
    Child sees `APP_ENV=lab` and missing `LOCAL_ONLY`; reassign exit is non-zero; evidence archive exists.


### Validation steps

- [ ] Quoting demo shows one safe argument vs split unsafe arguments  
- [ ] Defaults script prints `ap-south-1` unless `REGION` is set  
- [ ] Arithmetic produces `remaining=2` after one attempt with `retries=3`  
- [ ] Exported vars appear in the child; local-only vars do not  
- [ ] `variables-evidence.tgz` exists under `~/rebash-shell/lab03`  

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `unbound variable` | `set -u` + unset name | Initialise, pass env, or use `${var:-}` / `${var:?}` |
| `readonly variable` | Reassign after `readonly` | Choose a new name or do not mark it readonly |
| Word-splitting bugs | Unquoted `$path` | Always `"$path"` |
| Child missing config | Forgot `export` | `export VAR=value` or `export VAR` after assign |

### Challenge exercise

Write `config-summary.sh` that reads optional env vars `APP_NAME` (default `demo-app`), `REGION` (default `ap-south-1`), and `MAX_TRIES` (default `5`), computes `next_try=$(( MAX_TRIES - 1 ))`, marks `APP_NAME` readonly after assignment, exports `REGION`, and writes `config.env` containing `APP_NAME=...`, `REGION=...`, `MAX_TRIES=...`, `next_try=...`. Run it twice: once with defaults, once with overrides.

### Learning outcomes

- Demonstrated why quoting protects paths with spaces  
- Used defaults and integer arithmetic in a strict script  
- Proved `export` inheritance and `readonly` protection  

### Cleanup

``` {.bash .ra-terminal title="Terminal"}
cd ~/rebash-shell/lab03
rm -f readonly-reassign.out
# Keep evidence and demos, or remove the workspace:
# rm -rf ~/rebash-shell/lab03
```

## Validation

- [ ] Lab finished under `~/rebash-shell/lab03/` with evidence files  
- [ ] You can explain unquoted vs `"$var"` vs `'$var'`  
- [ ] You can use `${var:-default}` and `$(( ))` correctly  
- [ ] You can explain `export` vs shell-local variables and `readonly`  

## Code Walkthrough

Production variable handling usually follows this order:

1. **Read inputs** — args and environment, with `set -u` in mind  
2. **Apply defaults or required checks** — `${var:-}` vs `${var:?}`  
3. **Quote every expansion** that reaches a command  
4. **Export only the contract** children need  
5. **Lock constants** with `readonly` when reassignment would be a bug  
6. **Prefer `$(( ))`** for integer counters used in retries and limits  

Naming tip: lowercase for script-local names; uppercase for exported environment contracts other tools already expect (`PATH`, `REGION`, CI variables).

## Security Considerations

- Do not export secrets to children that do not need them  
- Never log secret values while debugging expansions  
- Prefer `${SECRET:?secret missing}` over silent empty defaults for credentials  
- Quote paths so spaces and globs cannot rewrite destructive commands  
- Treat environment values from CI as untrusted strings until validated  

## Common Mistakes

!!! warning "Unquoted expansions on paths"
    Spaces and globs rewrite the command line. **Fix:** always `"$path"` and `"$@"`.

!!! warning "Spaces around `=` in assignments"
    `name = value` is not an assignment. **Fix:** `name=value`.

!!! warning "Defaulting secrets with `:-`"
    Empty credentials become a fake default and fail late. **Fix:** `${SECRET:?SECRET must be set}`.

!!! warning "Forgetting `export` for child tools"
    Nested `bash -c` or Python sees nothing. **Fix:** export the contract explicitly and test with a child process.

## Best Practices

- Quote by default; unquote only with a written reason  
- Use `${var:?}` for required configuration  
- Keep arithmetic in `$(( ))` for integers; document units (seconds, retries)  
- Export the minimum set of variables  
- Run ShellCheck — it catches many quoting issues early  

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `unbound variable` | `set -u` + missing value | Provide value or safe default |
| `too many arguments` | Word-splitting | Quote the expansion |
| Child prints `missing` | Not exported | `export` before launching child |
| Arithmetic looks concatenated | Used string `+` outside `$(( ))` | Use `$(( a + b ))` |
| Readonly error unexpected | Constant reassigned | Rename mutable state |

## Summary

Variables carry configuration; quoting protects meaning; defaults and arithmetic keep scripts flexible; `export` and `readonly` define the contract with children and with your future self. Next, learn how those values move through **stdout**, **stderr**, redirections, and pipes in [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md).

## Interview Questions

**1. Why is `"$path"` safer than `$path` in Bash scripts?**

??? success "Reveal answer"
    Without quotes, Bash performs **word-splitting** and **globbing** on the expanded value. A path like `my reports/file.txt` becomes multiple arguments. With `"$path"`, the value stays one argument. Ops scripts that call `rm`, `mv`, or `cp` must quote paths to avoid deleting or moving the wrong targets.

**2. What is the difference between `${var:-default}` and `${var:?message}`?**

??? success "Reveal answer"
    `${var:-default}` substitutes `default` when `var` is unset or empty — useful for optional config such as a region. `${var:?message}` **aborts the script** with an error when the value is missing — better for secrets and required endpoints. Choose based on whether empty input is acceptable.

**3. How does `export` change variable visibility for child processes?**

??? success "Reveal answer"
    A normal shell variable is visible only in the current shell. **`export`** marks it for the environment of child processes (`bash -c`, other scripts, tools). Unexported names do not appear in the child. Export only what children need; avoid exporting secrets globally.

**4. How do you do integer arithmetic in Bash, and what are the limits?**

??? success "Reveal answer"
    Use **arithmetic expansion** `$(( expression ))`, for example `n=$(( n + 1 ))`. Bash arithmetic is integer-oriented. For floating point, teams usually call `awk` or `bc`. Under `set -u`, initialise counters before you increment them.

**5. What does `readonly` give you that a normal variable does not?**

??? success "Reveal answer"
    After `readonly NAME=value` (or `readonly NAME` after assign), Bash **rejects reassignment**, which protects constants such as a script version or a fixed allow-list path. It is a safety guard against accidental overwrites in long scripts, not a security boundary against a hostile user with write access to the file.

**6. A path variable works in `echo` but fails in `cd`. What quoting issue might you look for?**

??? success "Reveal answer"
    `echo` can still print a split path in a confusing way, while `cd` needs exactly one directory argument. Check whether the expansion is quoted (`cd "$dir"`), whether the directory exists, and whether the value contains trailing spaces or newlines from command substitution. Prefer `dir="$(dirname "$file")"` with quotes throughout.

**7. How would you demonstrate word-splitting in an interview without deleting files?**

??? success "Reveal answer"
    Create a path with a space, then print arguments with `printf '<%s> '` once quoted and once unquoted (in a controlled demo). Show that the unquoted form produces multiple `<>` chunks. Never demonstrate with `rm $path`. Interviewers look for safe proof and clear risk language.

**8. When should a DevOps script use environment variables versus positional arguments?**

??? success "Reveal answer"
    Use **positional arguments** for required per-run inputs (hostname, action). Use **environment variables** for deployment configuration that differs by environment (`REGION`, feature flags) and for secrets injected by CI. Combine them: args for the verb/target, env for policy and credentials — and validate both under strict mode.

## Related Tutorials

- [Shell Scripting for DevOps Engineers – Overview](index.md)
- [Writing Your First Script](writing-your-first-script.md) *(previous)*
- [Input, Output, Redirection, and Pipes](input-output-redirection-and-pipes.md) *(next)*

## References

- [GNU Bash manual — Shell Parameters](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameters.html)  
- [GNU Bash manual — Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html)  
- [GNU Bash manual — Shell Arithmetic](https://www.gnu.org/software/bash/manual/html_node/Shell-Arithmetic.html)  
- [ShellCheck](https://www.shellcheck.net/)  
- Track index: [Shell Scripting for DevOps Engineers](index.md)
