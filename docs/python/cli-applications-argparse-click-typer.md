---
title: "CLI Applications — argparse, Click, and Typer"
description: "Build operator-friendly CLIs with argparse, Click, and Typer — including Rich output, progress bars, and clean exit codes for DevOps tools."
difficulty: intermediate
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 12 · CLI Applications"
career_paths:
  - beginner
  - devops-engineer
  - cloud-engineer
  - platform-engineer
  - site-reliability-engineer
skills:
  - python
  - argparse
  - click
  - typer
  - rich
prerequisites:
  - python/configuration-management-and-secrets
next:
  - python/linux-automation-subprocess-and-psutil
related:
  - python/functions-parameters-and-scope
  - python/packaging-pyproject-and-wheels
labs: []
projects:
  - projects/python-infra-inventory-cli
interview: interview/python
certifications:
  - PCAP
tags:
  - python
  - cli
  - argparse
  - typer
  - click
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# CLI Applications — argparse, Click, and Typer

## Overview

Ship a small ops CLI with subcommands, `--dry-run`, clear help text, Rich-friendly output, and exit codes that CI can trust.

DevOps tools are CLIs first. **argparse** is stdlib and enough for many wrappers. **Click** and **Typer** speed up subcommands and help. Keep stdout for data and stderr for humans.

Complete [Configuration Management and Secrets](configuration-management-and-secrets.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 12 · CLI Applications** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Configuration Management and Secrets](configuration-management-and-secrets.md)
- Project venv with Python 3.12+

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Build a CLI with argparse (flags, subcommands)  
- [ ] Contrast argparse vs Click vs Typer  
- [ ] Add `--dry-run` as a keyword-safe default  
- [ ] Use Rich for tables/progress (optional dependency)  
- [ ] Return meaningful exit codes from `main`

## Architecture

This topic’s control points and relationships are shown below.

![CLI applications](../assets/excalidraw/python-cli-apps.svg)

## Theory

### What it is

A Command-Line Interface (CLI) is how operators run your automation: flags, subcommands, help text, and exit codes. Python’s stdlib **`argparse`** builds parsers by hand. **Click** uses decorators for groups and options. **Typer** builds on Click with type hints — a strong default for new internal tools. **Rich** (optional) adds tables and progress for humans, not for machine-readable pipes.

### Why it matters

DevOps tools are invoked by humans and by CI. Clear `--help`, predictable exit codes, and a default **dry-run** with explicit `--apply` prevent accidental deletes. Choosing a framework early keeps flag names and JSON-vs-human output consistent across your inventory, SSH, and cloud scripts.

### How it works

Define arguments (paths, booleans, choices), parse `sys.argv`, then call `main()` that returns an integer exit code. Pattern: dry-run on by default; `--apply` enables mutation. Print human summaries to stderr or a TTY; print JSON to stdout when `--format json` so scripts can pipe. Typer maps annotated parameters to options automatically; Click is similar with more explicit decorators. Use Rich only when stdout is interactive — never colourise JSON meant for `jq`.

```python
import argparse
parser = argparse.ArgumentParser(description="Inventory helper")
parser.add_argument("--dry-run", action="store_true", default=True)
parser.add_argument("--apply", action="store_true", help="disable dry-run")
```

### Key concepts and comparisons

| Framework | Pros | Trade-off |
|-----------|------|-----------|
| argparse | Stdlib, no deps | More boilerplate |
| Click | Mature, groups | Slightly more ceremony |
| Typer | Type hints → CLI | Extra dependency |

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Operational failure |
| 2 | Usage / bad arguments |

### Common pitfalls

- Defaulting to apply/mutate instead of dry-run.  
- Mixing JSON and banners on the same stdout stream.  
- Exit code 0 on partial failure (CI thinks green).  
- Required secrets as positional args (visible in `ps` / history).  
- Huge dependency trees for a ten-line wrapper — argparse is enough.

## Hands-on Lab

**Focus:** practise the core workflow for CLI Applications — argparse, Click, and Typer

```bash
mkdir -p ~/rebash-python/module-12
cd ~/rebash-python/module-12

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'typer==0.15.1' 'rich==13.9.4'
```

### Step 1 – argparse inventory CLI

```bash
cd ~/rebash-python/module-12
source .venv/bin/activate

cat > inv_argparse.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

HOSTS = [{"name": "web-a", "ip": "10.0.1.10"}, {"name": "web-b", "ip": "10.0.1.11"}]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Tiny inventory CLI")
    sub = p.add_subparsers(dest="cmd", required=True)
    list_p = sub.add_parser("list", help="list hosts")
    list_p.add_argument("--format", choices=("table", "json"), default="table")
    args = p.parse_args(argv)
    if args.cmd == "list":
        if args.format == "json":
            print(json.dumps(HOSTS))
        else:
            for h in HOSTS:
                print(f"{h['name']:8} {h['ip']}", file=sys.stderr)
            print(json.dumps([h["name"] for h in HOSTS]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
EOF

python inv_argparse.py list --format json
python inv_argparse.py list --format table
```

### Step 2 – Typer + dry-run

```bash
cat > inv_typer.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import typer

app = typer.Typer(help="Inventory CLI (Typer)")


@app.command()
def delete(
    name: str,
    apply: bool = typer.Option(False, "--apply", help="actually delete"),
) -> None:
    """Delete a host record (lab stub)."""
    if not apply:
        typer.secho(f"DRY-RUN delete {name}", err=True)
        raise typer.Exit(code=0)
    typer.secho(f"DELETED {name}", err=True)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
EOF

python inv_typer.py delete web-a
python inv_typer.py delete web-a --apply
```

### Step 3 – Rich progress (optional feel)

```bash
python - <<'PY'
from rich.progress import track
import time
for _ in track(range(5), description="scanning"):
    time.sleep(0.05)
PY
```

## Validation

- [ ] Lab commands run under `~/rebash-python/module-12/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **CLI Applications — argparse, Click, and Typer** always combines:

1. Inspect before you change (status, plan, logs, dry-run)
2. Prefer reversible, documented changes (Git, IaC, drop-ins, version pins)
3. Capture evidence (command output, pipeline logs) for handovers
4. Prefer current tools and APIs over legacy shortcuts
5. Least privilege — escalate credentials only when required

Keep runbooks short enough to follow under pressure. Automate checks; keep humans for judgement.

## Security Considerations

- Treat credentials and tokens for python as privileged — never commit them
- Prefer short-lived auth (OIDC, roles, SSO) over long-lived keys
- Validate blast radius before apply/deploy/delete operations
- Restrict who can approve production changes
- Collect audit logs; limit who can read sensitive traces

## Common Mistakes

!!! warning "Defaulting to apply/mutate instead of dry-run.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Mixing JSON and banners on the same stdout stream.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode CLI Applications — argparse, Click, and Typer changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| JSON mixed with tables | Printing both on stdout | Humans → stderr |
| Accidental delete | No dry-run default | Default safe; require `--apply` |
| Typer not found | Wrong venv | Activate; reinstall |

## Summary

- argparse for stdlib CLIs; Typer/Click for richer tools  
- Dry-run by default for mutating commands  
- Exit codes and stdout/stderr discipline

## Interview Questions

1. How does **CLI Applications — argparse, Click, and Typer** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [Linux Automation — subprocess and psutil](linux-automation-subprocess-and-psutil.md)

## References

- [argparse](https://docs.python.org/3/library/argparse.html)  
- [Typer](https://typer.tiangolo.com/)  
- [Click](https://click.palletsprojects.com/)  
- [Rich](https://rich.readthedocs.io/)
