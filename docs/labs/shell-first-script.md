---
title: "Lab — Create Your First Script"
description: "Write, chmod, and run a Bash script with shebang, comments, exit codes, and basic logging."
difficulty: beginner
estimated_time: "30–40 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - shell
  - bash
comments: false
---

# Lab — Create Your First Script

## Lab Overview

**Purpose:** Practise Module 1–2 skills by creating a small ops greeting/info script that exits cleanly.

**Scenario:** A new joiner needs a starter script template the team can copy for bastion diagnostics.

**Expected outcome:** A working script under `~/rebash-lab-shell` with clear exit codes, stderr logging, and validation steps you can re-run.

!!! tip "This is a lab, not a tutorial"
    Apply [Shell Scripting](../shell/index.md) skills. Prefer small verified steps over rewriting everything at once.

## Business Scenario

Platform Engineering wants a consistent script skeleton: shebang, strict mode later, comments, and exit codes. You deliver the first version.

## Learning Objectives

By the end of this lab, you will be able to:

- [ ] Create an executable Bash script with a correct shebang
- [ ] Print host facts and separate stdout from stderr logs
- [ ] Use exit codes meaningfully (0 success, 2 usage)
- [ ] Run the script via `./script` and `bash script`

## Prerequisites

### Knowledge

- [Writing Your First Script](../shell/writing-your-first-script.md)
- [Shell Fundamentals — Bash vs sh and Execution](../shell/shell-fundamentals-bash-vs-sh-and-execution.md)

### Software

| Tool | Notes |
|------|--------|
| Bash 4.2+ | `bash --version` |
| coreutils | hostname, date, uname |

**Estimated cost:** £0.

## Environment

Any Linux host or WSL2. Work under `~/rebash-lab-shell`.

## Initial State

```bash title="Terminal"
mkdir -p ~/rebash-lab-shell
cd ~/rebash-lab-shell
```

## Lab Tasks

### Task 1 — Create the script skeleton

Create `first-script.sh`:

```bash title="first-script.sh"
#!/usr/bin/env bash
# first-script.sh — host snapshot for REBASH lab
# Usage: ./first-script.sh [name]

NAME="${1:-operator}"
echo "Hello, ${NAME}" 
echo "host=$(hostname)" 
echo "date=$(date -u +%Y-%m-%dT%H:%M:%SZ)" 
echo "kernel=$(uname -r)" 
exit 0
```

Run:

```bash title="Terminal"
chmod +x first-script.sh
```


### Task 2 — Run and inspect exit codes

```bash
./first-script.sh
echo "exit=$?"
./first-script.sh Ada
bash first-script.sh
```

### Task 3 — Add usage and stderr logging

Update the script so that `-h`/`--help` prints usage to stderr and exits `2`. Log a one-line note to stderr: `log: starting snapshot`.

```bash
# After editing:
./first-script.sh --help; echo "exit=$?"
./first-script.sh 2> first-script.log
cat first-script.log
```

### Task 4 — Compare Bash vs sh invocation

```bash
bash first-script.sh
sh first-script.sh || true
head -1 first-script.sh
```

Confirm the shebang selects Bash when executed as `./first-script.sh`.


## Validation

- [ ] Script is executable and starts with `#!/usr/bin/env bash`
- [ ] `--help` exits with code 2 and writes usage to stderr
- [ ] Normal run prints host, UTC date, and kernel on stdout
- [ ] You can explain the difference between `bash script` and `./script`

## Troubleshooting

| Symptom | Possible cause | Resolution |
|---------|----------------|------------|
| Permission denied | Missing execute bit | `chmod +x first-script.sh` |
| Wrong interpreter | Executed with `sh` and Bashisms present | Use `./` or `bash`; keep POSIX if targeting sh |
| Empty hostname | Restricted container hostname | Fall back to `uname -n` |

## Cleanup

```bash title="Terminal"
rm -rf ~/rebash-lab-shell
```

## Stretch Goals

- Add a `--dry-run` mode that prints actions without changing the system
- Emit a machine-readable `RESULT status=...` line on stdout for CI
- Schedule the script with cron or a systemd timer

## Production Discussion

In production, wrap scripts with lock files, structured logging, explicit `PATH`, and documented exit codes. Prefer configuration files over hard-coded hosts and thresholds. Never embed secrets in scripts — use environment variables or a secrets manager.

## Best Practices

- Use `#!/usr/bin/env bash` and `set -euo pipefail`
- Quote every expansion that may contain spaces
- Log diagnostics to stderr; keep stdout for data
- Prefer absolute paths in scheduled jobs
- Validate inputs before destructive actions

## Common Mistakes

| Mistake | Why it happens | Correct approach |
|---------|----------------|------------------|
| Unquoted paths | Habit from interactive shell | Always `"$var"` |
| Missing `pipefail` | Default Bash pipeline behaviour | `set -o pipefail` |
| Interactive-only PATH | Cron/systemd minimal env | Set `PATH=` at top |
| Skipping dry-run | Time pressure | Default to dry-run for risky ops |

## Success Criteria

- [ ] Script runs under Bash with strict mode
- [ ] Validation and failure paths are tested
- [ ] Exit codes are documented
- [ ] Cleanup leaves no lab artefacts (or documents what remains)

## Reflection Questions

1. What would break if this ran under `/bin/sh` (dash) instead of Bash?
2. How would you make the script idempotent?
3. How would you secure credentials and host inventories?
4. How would you observe failures in production?

## Interview Connection

Interviewers often ask about quoting, exit codes, cron environment differences, and how you prevent overlapping jobs. Be ready to walk through a small script and explain failure modes.

## Related Tutorials

- [`Writing Your First Script`](../shell/writing-your-first-script.md)
- [`Shell Fundamentals Bash Vs Sh And Execution`](../shell/shell-fundamentals-bash-vs-sh-and-execution.md)
- [`Variables Quoting And Arithmetic`](../shell/variables-quoting-and-arithmetic.md)
- Cheat sheet: [Shell Scripting](../cheatsheets/shell.md)
- Interview: [Shell Scripting](../interview/shell.md)
- Quiz: [Shell Scripting for DevOps Fundamentals](../quizzes/shell-scripting-for-devops-fundamentals.md)
- Track: [Shell Scripting](../shell/index.md)
