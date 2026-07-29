---
title: "Writing Your First Script"
description: "Shebang lines, executable bits, running scripts, exit codes, comments, and a production-ready script structure with strict mode."
difficulty: beginner
estimated_time: "40 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - shebang
  - exit-codes
  - structure
prerequisites:
  - Shell Fundamentals — Bash vs sh and Execution
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# Writing Your First Script

## Overview

A one-liner in history is not automation. This tutorial turns commands into a reviewable script with a clear contract: inputs, side effects, and exit status.

This is **Tutorial 2** in **Module 2: Writing Your First Script** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Shell Fundamentals — Bash vs sh and Execution
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “Writing Your First Script” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for Writing Your First Script](../assets/images/shell-script-lifecycle.svg)

## Theory

### Shebang

The **shebang** is the first line that names the interpreter:

```bash
#!/usr/bin/env bash
```

`env` resolves `bash` from `PATH`. Absolute `#!/bin/bash` is fine when the path is guaranteed (many cloud images).

### Executable Files

Make a script runnable:

```bash
chmod +x script.sh
./script.sh
```

Without `+x`, call `bash script.sh`. The directory must be searchable; `./` avoids relying on `.` being in `PATH`.

### Running Scripts

| Form | Effect |
|------|--------|
| `./script.sh` | New process; needs execute bit + shebang |
| `bash script.sh` | Explicit Bash; execute bit optional |
| `source script.sh` | Current shell — inherits and mutates it |

Prefer `./` or `bash` for jobs. Reserve `source` for libraries of functions.

### Exit Codes

Every process returns an integer **exit code** (0–255). By convention **0** means success; non-zero means failure. Scripts expose this via `exit N` or the last command’s status (`$?`).

Document a small taxonomy for teammates: `2` usage error, `3` missing dependency, `4` runtime failure.

### Comments

Use `#` for human notes. Explain **why**, not what the next line already shows. Keep comments short; outdated comments are worse than none.

### Script Structure

Production default from this module onward:

```bash
#!/usr/bin/env bash
set -euo pipefail

# usage / constants
# functions
# main
```

`-e` exit on error, `-u` treat unset variables as errors, `pipefail` fails a pipeline if any stage fails. Put `set -euo pipefail` near the top after the shebang.

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab02 && cd ~/rebash-shell/lab02
```

**Focus:** create shebang script; chmod +x; exit codes; strict-mode skeleton

### Step 1 – Skeleton

```bash
cat > lab.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "lab02 writing-your-first-script on $(hostname -s)"
EOF
chmod +x lab.sh
./lab.sh
```

### Step 2 – First strict-mode script

```bash
cat > hello-ops.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
# hello-ops: tiny contract demo
host=$(hostname -s)
echo "hello from ${host}"
exit 0
EOF
chmod +x hello-ops.sh
./hello-ops.sh
bash -c './hello-ops.sh; echo exit=$?'
```

### Final step – Trace and cleanup note

```bash
bash -x ./lab.sh 2>&1 | tail -n 20 || true
# keep ~/rebash-shell for later labs
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab02/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **Writing Your First Script** always combines:

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

**Writing Your First Script** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Shell Fundamentals — Bash vs sh and Execution](shell-fundamentals-bash-vs-sh-and-execution.md) *(previous)*
- [Variables, Quoting, and Arithmetic](variables-quoting-and-arithmetic.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
