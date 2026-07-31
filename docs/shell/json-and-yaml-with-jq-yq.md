---
title: "JSON and YAML with jq and yq"
description: "Parse and transform JSON and YAML configuration with jq and yq in shell pipelines."
difficulty: intermediate
estimated_time: "50 min"
author: Shaik Basha
last_updated: "2026-07-29"
category: shell
tags:
  - shell
  - bash
  - jq
  - yq
  - config
prerequisites:
  - Networking Automation with Shell
  - Bash 4.2+ on Linux (WSL2/VM/cloud)
comments: false
---

# JSON and YAML with jq and yq

## Overview

Cloud APIs and Kubernetes speak JSON/YAML. Shell stays useful when jq/yq shape data before the next tool runs.

This is **Tutorial 14** in **Module 14: JSON & YAML** of the REBASH Academy **Shell Scripting for DevOps Engineers** series — written for Linux administrators, DevOps engineers, SREs, and platform engineers who automate production hosts with Bash.

## Prerequisites

- Networking Automation with Shell
- Bash 4.2+ on Linux (WSL2/VM/cloud)

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Apply the core ideas of “JSON and YAML with jq and yq” in a real ops script
- [ ] Use `set -euo pipefail` as the production default
- [ ] Use quoted expansions and clear stderr diagnostics
- [ ] Produce meaningful exit codes for automation consumers
- [ ] Debug behaviour with `bash -x` when something fails
- [ ] Relate this topic to day-to-day Linux admin and DevOps work

## Architecture

Ops scripts sit between humans/automation and system tools. This topic’s control points are shown below.

![Architecture diagram for JSON and YAML with jq and yq](../assets/excalidraw/shell-json-yaml.svg)

## Theory

### What it is

Modern operations speak **JSON** (JavaScript Object Notation) and **YAML** (YAML Ain’t Markup Language) for APIs, Kubernetes manifests, and application config. Shell scripts should not parse those formats with `grep` and hope. **`jq`** is the standard command-line JSON processor; **`yq`** (pin a specific implementation — Mike Farah’s Go tool and Python variants differ) does the same job for YAML. Together they let Bash extract fields, rewrite keys, and validate structure before a deploy continues.

### Why it matters

Cloud APIs, Continuous Integration (CI) artefacts, and GitOps files are structured data. Brittle text scraping breaks when a field moves or a list grows. Using `jq` / `yq` keeps transforms explicit, testable, and reviewable. It also reduces secret leakage: you can extract one non-sensitive field instead of dumping an entire document into logs. For DevOps and platform engineers, fluency with these tools is the difference between a reliable glue script and a fragile one-liner that fails on the next API version.

### How it works

Pipe or redirect JSON into `jq`. Use `-r` for raw strings and `--arg` to pass shell values safely into the filter:

```bash
jq -r '.items[].metadata.name' < deploy.json
jq --arg env "$ENV" '.env = $env' config.json
```

Invalid JSON should fail the script (`set -e` plus `jq`’s non-zero status). With `yq`, select keys, convert between YAML and JSON when needed, and merge overlays for environment-specific config. Always **validate before apply**: check required keys exist, extract only what you need, and rewrite files atomically (`tmp` + `mv` on the same filesystem).

Treat configuration as versioned data. Document required keys in the script’s usage text. Keep secrets out of shell history, debug dumps, and world-readable files — prefer environment injection or a secrets store over embedding tokens in YAML checked into git.

### Key concepts

| Concern | Practice |
|---------|----------|
| JSON | Prefer `jq` over `grep`/`sed` |
| YAML | Pin one `yq` implementation in docs and CI |
| Injection | `jq --arg` / `yq` equivalents — not string concat |
| Validation | Fail fast on missing keys or invalid documents |
| Rewrite | Atomic temp file + `mv`; never half-written configs |

### Common pitfalls

- Parsing JSON with `grep`/`awk` and breaking on whitespace or key order
- Mixing incompatible `yq` dialects across developer laptops and CI
- Concatenating shell variables into filters instead of `--arg`
- Dumping full documents (with secrets) into CI logs while debugging
- Overwriting config in place so a crash leaves a truncated file

## Hands-on Lab

Create a workspace for this tutorial.

```bash
mkdir -p ~/rebash-shell/lab14 && cd ~/rebash-shell/lab14
```

**Focus:** jq extract/transform; yq read YAML; validate config keys

### Step 1 – jq (and yq if present)

```bash
cat > sample.json << 'EOF'
{"env":"lab","items":[{"name":"web"},{"name":"db"}]}
EOF
cat > sample.yaml << 'EOF'
env: lab
replicas: 2
EOF
cat > parse.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
command -v jq >/dev/null || { echo "install jq" >&2; exit 3; }
jq -r '.items[].name' sample.json | tee names.txt
jq --arg e prod '.env=$e' sample.json > out.json
if command -v yq >/dev/null; then
  yq '.replicas' sample.yaml | tee replicas.txt
else
  echo 'yq not installed — skipped' | tee replicas.txt
fi
EOF
chmod +x parse.sh
./parse.sh
```

### Final step – Cleanup note

```bash
# Keep ~/rebash-shell/ for later tutorials; destroy disposable cloud resources from this lab
```

## Validation

- [ ] Lab commands run under `~/rebash-shell/lab14/`
- [ ] You can explain each Theory heading in your own words
- [ ] Failure path exits non-zero and prints diagnostics to stderr (where applicable)
- [ ] You can relate this topic to a real DevOps or Linux admin task

## Code Walkthrough

Production Bash for **JSON and YAML with jq and yq** always combines:

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

**JSON and YAML with jq and yq** is a core skill for Linux admins and DevOps engineers automating real hosts and pipelines. Practise the lab until the failure path is as familiar as the happy path, then continue the track.

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
- [Networking Automation with Shell](networking-automation-with-shell.md) *(previous)*
- [Scheduling — cron, at, and systemd Timers](scheduling-cron-at-and-timers.md) *(next)*
- [Learning Paths](../learning-paths/index.md)

## References

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/)
- [POSIX shell command language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck](https://www.shellcheck.net/)
- Track index: [Shell Scripting for DevOps Engineers](index.md)
