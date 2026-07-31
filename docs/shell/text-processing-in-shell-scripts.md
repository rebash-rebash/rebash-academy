---
title: "Text Processing in Shell Scripts"
description: "Filter and transform text with grep, sed, awk, cut, tr, sort, uniq, paste, and xargs inside scripts."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - grep
  - sed
  - awk
  - xargs
prerequisites:
  - File Operations in Shell
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Text Processing in Shell Scripts

## Overview

Logs and CLI output are the DevOps data plane. Compose filters carefully and keep `pipefail` on.

This is **Tutorial 10** in **Module 10: Text Processing** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- File Operations in Shell
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Text Processing in Shell Scripts” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Text Processing in Shell Scripts](../assets/excalidraw/shell-text-processing.svg)

## Theory

### What it is

**Text processing** is the classic Unix pipeline: filter lines, rewrite fields, sort and count, then feed results into the next command. The core toolkit for shell scripts includes `grep` (search), `sed` (stream edit), `awk` (column and record logic), plus helpers such as `cut`, `tr`, `sort`, `uniq`, `paste`, and `xargs`. These tools turn logs, inventories, and command output into reports and actions without loading a heavier language for every small transform.

### Why it matters

Linux administration and DevOps generate oceans of line-oriented text: service logs, `ps` output, package lists, and CSV-like exports. Knowing when to reach for `grep` versus `awk` — and how to batch safely with `xargs` — keeps scripts short, fast, and portable across Continuous Integration (CI) images. Mistakes here are equally costly: a greedy `sed -i` without backup can rewrite production configs, and `xargs` without NUL delimiters breaks on paths with spaces.

### How it works

`grep` selects lines: `grep -E 'error|fail' app.log`, with `-F` for fixed strings, `-r` for recursion, and `-v` to invert. Prefer `rg` interactively if you have it; stick to `grep` in portable scripts. `sed` applies substitutions such as `sed -E 's/foo/bar/'` — prefer writing to a new file over in-place edits without backup. `awk` shines on columns and records: `awk -F: '{print $1}' /etc/passwd` for structured reports.

Smaller tools compose well: `cut` for field slices, `tr` for character classes, `sort` then `uniq` for frequency reports, and `paste` to merge streams. `xargs` builds command lines from stdin. Prefer NUL-safe pipelines when paths may contain spaces:

```bash
printf '%s\0' "${files[@]}" | xargs -0 -n 20 gzip
```

Enable `pipefail` so a failing stage in a text pipeline fails the script.

### Key concepts

| Tool | Use |
|------|-----|
| `grep` | Select or exclude lines by pattern |
| `sed` | Stream substitutions and simple edits |
| `awk` | Fields, records, lightweight reports |
| `cut` / `tr` | Slice fields; translate or delete characters |
| `sort` / `uniq` | Order lines; collapse adjacent duplicates |
| `paste` | Merge lines side by side |
| `xargs -0` | Batch commands with safe path delimiters |

### Common pitfalls

- Editing in place with `sed -i` on production files without a backup or dry-run
- Using `uniq` without sorting first and missing non-adjacent duplicates
- Feeding `xargs` newline-separated paths that contain spaces
- Parsing JSON or YAML with `grep`/`sed` instead of `jq`/`yq`
- Building enormous one-liners that nobody can test or review

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab10 && cd ~/rebash-shell/lab10
```

**Focus:** grep/sed/awk pipeline; sort|uniq report; xargs batch

### Step 1 – Text pipeline

```bash
printf 'b\na\nb\nc\n' > raw.txt
cat > text.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
grep -v '^$' raw.txt \
  | tr '[:upper:]' '[:lower:]' \
  | sort \
  | uniq -c \
  | sort -nr \
  | tee report.txt
cut -c1-20 report.txt | paste - -
printf 'a\nb\n' | xargs -n 1 echo item
EOF
chmod +x text.sh
./text.sh
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-shell/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab10/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Text Processing in Shell Scripts** always combines:

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

**Text Processing in Shell Scripts** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [File Operations in Shell](file-operations-in-shell.md) *(previous)*
- [Process Automation — Signals and Traps](process-automation-signals-and-traps.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
