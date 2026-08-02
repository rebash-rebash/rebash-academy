# Technology Definition

> **Content quality:** Follow `.cursor/prompts/CONTENT_QUALITY.md`, `tutorial-format-linux.md`, `create_lab.md`, and `create_interview_questions.md`. Labs: topic-specific, copy-paste executable. Prefer Codex until the user changes agents.


## Course

Shell Scripting for DevOps Engineers

---

## Description

A practical Bash shell scripting course focused on Linux administration, cloud automation, DevOps and Platform Engineering.

This course teaches learners how to automate repetitive operational tasks, build production-ready shell scripts and troubleshoot Linux systems efficiently.

The emphasis is on real-world automation rather than academic scripting.

---

## Target Roles

- Linux Administrator
- DevOps Engineer
- Cloud Engineer
- Platform Engineer
- Site Reliability Engineer (SRE)
- DevSecOps Engineer
- Infrastructure Engineer

---

## Difficulty

Beginner → Advanced

---

## Estimated Duration

6–8 Weeks

---

## Prerequisites

- Linux Fundamentals

---

## MCP Servers

Primary

- Context7

Optional

- Filesystem
- Git
- Kubernetes

---

# Modules

## Module 1 — Shell Fundamentals

- What is a Shell?
- Bash vs sh
- Shell Execution
- Interactive vs Non-interactive Shell
- Login Shell
- Environment Variables

---

## Module 2 — Writing Your First Script

- Shebang
- Executable Files
- Running Scripts
- Exit Codes
- Comments
- Script Structure

---

## Module 3 — Variables

- Variables
- Constants
- Environment Variables
- Command Substitution
- Arithmetic
- Quoting Rules

---

## Module 4 — Input & Output

- echo
- printf
- read
- stdin
- stdout
- stderr
- Redirection
- Pipes

---

## Module 5 — Control Flow

- if
- elif
- else
- case
- test
- [[ ]]
- Logical Operators

---

## Module 6 — Loops

- for
- while
- until
- break
- continue
- Nested Loops

---

## Module 7 — Functions

- Function Declaration
- Parameters
- Return Values
- Local Variables
- Reusable Functions

---

## Module 8 — Arrays & Strings

- Indexed Arrays
- Associative Arrays
- String Manipulation
- Pattern Matching

---

## Module 9 — File Operations

- Reading Files
- Writing Files
- Temporary Files
- File Tests
- Directory Operations

---

## Module 10 — Text Processing

- grep
- sed
- awk
- cut
- tr
- sort
- uniq
- paste
- xargs

---

## Module 11 — Process Automation

- ps
- kill
- pkill
- nohup
- jobs
- wait
- Signals
- Trap

---

## Module 12 — Linux Administration

- User Management
- Package Management
- Service Management
- Log Rotation
- Disk Usage
- Backup Automation

---

## Module 13 — Networking Automation

- ping
- curl
- wget
- nc
- dig
- SSH
- SCP
- rsync

---

## Module 14 — JSON & YAML

- jq
- yq
- Parsing JSON
- Parsing YAML
- Configuration Files

---

## Module 15 — Scheduling

- cron
- crontab
- at
- systemd Timers

---

## Module 16 — Error Handling

- Exit Codes
- Trap
- Defensive Programming
- Logging
- Debugging

---

## Module 17 — Production Shell Scripting

- ShellCheck
- Idempotent Scripts
- Secure Scripting
- Logging
- Retry Logic
- Lock Files
- Configuration Management

---

## Module 18 — Troubleshooting

- Debugging Bash
- Common Errors
- Permission Problems
- Cron Issues
- Variable Expansion Problems
- Performance Optimisation

---

# Hands-on Labs

- Create Your First Script
- Build a User Management Script
- Automate Software Installation
- Build a Backup Utility
- Rotate Logs
- Monitor Disk Usage
- Monitor CPU & Memory
- Build a Service Health Checker
- Build an SSL Certificate Monitor
- Parse JSON with jq
- Parse YAML with yq
- Automate SSH Tasks
- Build a Deployment Script
- Create a Linux Operations Toolkit

---

# Projects

## Beginner

Linux Automation Scripts

---

## Intermediate

Linux Administration Toolkit

---

## Advanced

Production Operations Toolkit

---

## Capstone

Production Shell Automation Framework

Features:

- Modular Scripts
- Logging
- Configuration Files
- Scheduling
- Notifications
- Error Handling
- Reporting
- Backup
- Monitoring
- Security Checks

---

# Cheat Sheets

Generate:

- Bash Syntax
- Variables
- Loops
- Functions
- Redirection
- Text Processing
- jq
- yq
- Cron
- Shell Debugging

---

# Interview Preparation

Cover:

- Bash Fundamentals
- Shell Scripting
- Linux Automation
- Process Management
- Text Processing
- Debugging
- Production Scenarios

---

# Excalidraw Diagrams

**Use Excalidraw only** for course diagrams — do not use D2 or Mermaid for Shell tutorials.

Assets live under `docs/assets/excalidraw/` as `.svg` plus editable `.excalidraw` sources. Regenerate with:

```bash
python3 scripts/generate-excalidraw-svg.py
```

Generate diagrams for:

- Shell Execution Flow
- Bash Script Lifecycle
- Variables & Quoting
- I/O Redirection & Pipes
- Control Flow
- Loops
- Functions & Locals
- Arrays & Strings
- File Operations
- Text Processing
- Process Automation
- Process Pipeline
- Cron Execution
- JSON / YAML (jq · yq)
- Error Handling
- Shell Automation Workflow
- Troubleshooting

---

# Certifications

Map modules where appropriate to:

- RHCSA
- RHCE
- LFCS
- LFCE

---

# Capstone Outcome

After completing this course learners should be able to:

- Write production-quality Bash scripts
- Automate Linux administration
- Build reusable automation tools
- Debug shell scripts efficiently
- Process structured data
- Schedule automation jobs
- Secure shell scripts
- Support DevOps and Platform Engineering workflows