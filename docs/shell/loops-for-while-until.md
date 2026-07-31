---
title: "Loops — for, while, and until"
description: "Iterate with for, while, and until; control flow with break and continue; nest loops carefully for ops batch jobs."
difficulty: beginner
estimated_time: "45 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - for
  - while
  - loops
prerequisites:
  - Control Flow — Conditionals
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Loops — for, while, and until

## Overview

Fleet checks, log scans, and retry loops are everyday DevOps patterns. Write loops that fail loudly and stop cleanly.

This is **Tutorial 6** in **Module 6: Loops** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Control Flow — Conditionals
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Loops — for, while, and until” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Loops — for, while, and until](../assets/excalidraw/shell-loops-flow.svg)

## Theory

### What it is

**Loops** repeat a block of commands over a list, a stream of lines, or until a condition changes. Bash offers `for` (iterate items or a C-style count), `while` (repeat while a command succeeds), and `until` (repeat while a command fails). Inside any loop, `break` leaves early and `continue` skips to the next iteration. Together these constructs drive host inventories, log scans, readiness probes, and batch file processing — everyday DevOps work.

### Why it matters

Manual repetition does not scale: checking twenty hosts or pruning a thousand log files by hand invites mistakes. Loops encode that repetition so Continuous Integration (CI), cron, and admin tooling apply the same steps consistently. The cost of a wrong loop is high: an unbounded `until` can hang a deployment, and an unquoted glob can expand to nothing or to surprising paths. Learning safe patterns — quoted lists, `read -r` line loops, and retry counters — keeps automation both powerful and predictable.

### How it works

A `for` loop walks a fixed list or a glob. Prefer arrays and `"$@"` when inputs are dynamic; when using globs, guard empty matches:

```bash
for host in web01 web02 web03; do
  printf 'check %s\n' "$host"
done

for f in /var/log/*.log; do
  [[ -e "$f" ]] || continue
  wc -l <"$f"
done
```

A `while` loop is the classic way to stream files and process output one line at a time:

```bash
while IFS= read -r line; do
  printf '%s\n' "$line"
done <"$infile"
```

`until condition; do ...; done` runs while the condition is false — handy for “wait until ready” probes. Always pair it with a counter or timeout so production jobs cannot loop forever. Keep nested loops shallow; extract the inner body to a function when readability suffers. Use `break 2` only when you intentionally leave an outer loop.

### Key concepts

| Loop | Typical use |
|------|-------------|
| `for item in list` | Hosts, files, arguments |
| `while read -r` | Line-oriented files and pipelines |
| `until` | Wait-until-ready with a bound |
| `break` / `continue` | Early exit or skip one iteration |
| Arrays / `"$@"` | Safer than unquoted globs for dynamic input |

### Common pitfalls

- Writing `for line in $(cat file)` and splitting on spaces inside lines
- Forgetting `[[ -e "$f" ]]` so a non-matching glob becomes a literal string
- Infinite `until` readiness loops without a max-attempts counter
- Deep nesting instead of a function, making `break` targets unclear
- Ignoring non-zero status from loop bodies when `set -e` is active and a command is allowed to fail

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab06 && cd ~/rebash-shell/lab06
```

**Focus:** for over hosts; while read lines; until ready; break/continue drills

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab06 loops-for-while-until on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

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

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab06/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Loops — for, while, and until** always combines:

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

**Loops — for, while, and until** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Control Flow — Conditionals](control-flow-conditionals.md) *(previous)*
- [Functions, Parameters, and Locals](functions-parameters-and-locals.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
