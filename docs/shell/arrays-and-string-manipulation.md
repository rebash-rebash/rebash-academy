---
title: "Arrays and String Manipulation"
description: "Indexed and associative arrays, string slicing and substitution, and pattern matching for ops data shaping."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - arrays
  - strings
  - patterns
prerequisites:
  - Functions, Parameters, and Locals
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Arrays and String Manipulation

## Overview

Host lists, service maps, and path rewriting are array and string problems. Handle them without fragile IFS hacks.

This is **Tutorial 8** in **Module 8: Arrays & Strings** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Functions, Parameters, and Locals
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Arrays and String Manipulation” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Arrays and String Manipulation](../assets/excalidraw/shell-arrays-strings.svg)

## Theory

### What it is

Bash **arrays** store ordered lists (**indexed**) or key/value maps (**associative**, Bash 4+). Alongside arrays, **parameter expansion** offers built-in string surgery: strip prefixes and suffixes, replace substrings, and take slices — without spawning `sed` for every small edit. **Pattern matching** with `[[ ]]`, `case`, and `=~` validates names and selects behaviour. Together these features let ops scripts manage host inventories, port maps, and path rewriting cleanly.

### Why it matters

DevOps work is full of lists: targets to patch, services to restart, files to archive. Storing them in a properly quoted array avoids the “split on spaces” trap that breaks paths and hostnames. Associative arrays replace brittle parallel lists (`names[i]` with `ports[i]`) with named lookups. Built-in string expansions keep simple transforms fast and dependency-free — useful in constrained Continuous Integration (CI) images — while patterns stop unsafe input before a destructive command runs.

### How it works

Indexed arrays hold elements in order. Always expand with `"${array[@]}"` so spaces inside elements are preserved:

```bash
hosts=(web01 web02 web03)
hosts+=("web04")
printf '%s\n' "${hosts[@]}"
n=0
for _ in "${hosts[@]}"; do n=$((n + 1)); done
echo "count=$n"
```

Associative arrays need an explicit declaration:

```bash
declare -A ports=( [web]=80 [db]=5432 )
printf 'web port=%s\n' "${ports[web]}"
```

They require Bash 4+ and suit environment-to-value maps and small inventories. For strings, parameter expansions rewrite without external tools. Combine with `[[ $name == *.log ]]`, `case` patterns, or `=~` regex — and validate before any destructive use.

### Key concepts

| Expansion / form | Use |
|------------------|-----|
| `"${array[@]}"` | All elements, safely quoted |
| `declare -A` | Associative map (Bash 4+) |
| `${var%%.*}` / `${var##*/}` | Strip longest suffix / basename-like |
| `${var%/*}` | Dirname-like |
| `${var/old/new}` | Replace first match |
| `${var:0:3}` | Substring slice |
| `[[ ]]` / `case` / `=~` | Pattern and regex tests |

### Common pitfalls

- Expanding `${array[*]}` or unquoted `$array` and merging elements incorrectly
- Using associative arrays under Bash 3 (for example older macOS defaults)
- Forgetting `declare -A` before assignments to a map
- Applying string replacements to untrusted input without validation
- Confusing `${var%}` (shortest) with `${var%%}` (longest) suffix removal

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab08 && cd ~/rebash-shell/lab08
```

**Focus:** indexed host list; associative ports; string strip/replace; patterns

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab08 arrays-and-string-manipulation on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

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
printf '%s\n' "${hosts[@]}"
declare -A ports=( [web]=80 [db]=5432 )
echo "web=${ports[web]}"
path=/var/log/app.log
echo "base=${path##*/}"
[[ $path == *.log ]] && echo 'pattern ok'
EOF
chmod +x arrays.sh
./arrays.sh
```

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab08/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Arrays and String Manipulation** always combines:

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

**Arrays and String Manipulation** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Functions, Parameters, and Locals](functions-parameters-and-locals.md) *(previous)*
- [File Operations in Shell](file-operations-in-shell.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
