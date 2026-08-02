# Shell scripting glossary

Curated terms for the REBASH Shell Scripting course book.

{% raw %}
- **array** — Indexed or associative list of values in Bash (`arr=(a b)`, `${arr[i]}`).
- **Bash** — Bourne Again SHell; the usual interactive and scripting shell on Linux.
- **builtin** — Command implemented inside the shell (for example `cd`, `read`, `printf`).
- **cron** — Time-based scheduler for recurring jobs.
- **exit status** — Integer a process returns; `0` usually means success, non-zero means failure (`$?`).
- **function** — Named block of shell code you can call with arguments (`name() { … }`).
- **glob** — Filename pattern such as `*.log` expanded by the shell before a command runs.
- **here-document** — Multi-line input redirected into a command (`<<EOF` … `EOF`).
- **IFS** — Internal Field Separator; characters used to split words (often space/tab/newline).
- **jq** — Command-line JSON processor used heavily in Cloud and DevOps scripts.
- **parameter expansion** — `${var}`, `${var:-default}`, `${#var}`, and related Bash forms.
- **pipe** — Connects stdout of one command to stdin of the next (`|`).
- **POSIX sh** — Portable shell dialect; stricter than Bash (often `/bin/sh`).
- **quoting** — Rules that control expansion: single quotes literal, double quotes allow `$` and backticks.
- **redirection** — Send stdin/stdout/stderr to files or other descriptors (`>`, `>>`, `2>`, `&>`).
- **set -euo pipefail** — Common strict mode: exit on error, treat unset vars as errors, fail on pipe errors.
- **shebang** — First line `#!/usr/bin/env bash` (or similar) that selects the interpreter.
- **signal** — Kernel notification to a process (for example `SIGINT`, `SIGTERM`); handled with `trap`.
- **stderr** — Standard error stream (file descriptor 2).
- **stdin** — Standard input stream (file descriptor 0).
- **stdout** — Standard output stream (file descriptor 1).
- **subshell** — Child shell environment `( … )` or command substitution `$(…)`.
- **systemd timer** — Modern alternative to cron that activates a service unit on a schedule.
- **trap** — Register commands to run when the shell receives a signal or exits.
- **variable** — Named value in the shell (`name=value`, `"$name"`).
- **yq** — Command-line YAML processor (companion to jq for Kubernetes and config files).
{% endraw %}
