---
title: "Infrastructure Automation — Terraform"
description: "Wrap Terraform CLI from Python — fmt, validate, plan automation, state inspection, and a practical cdktf overview for DevOps engineers."
difficulty: advanced
estimated_time: "50–65 min"
technology: python
category: python
module: "Module 19 · Infrastructure"
career_paths:
  - devops-engineer
  - platform-engineer
  - cloud-engineer
  - site-reliability-engineer
skills:
  - python
  - terraform
  - cdktf
prerequisites:
  - python/kubernetes-python-client-automation
next:
  - python/ssh-automation-paramiko-and-fabric
related:
  - terraform/index
  - labs/python-terraform-wrapper
labs:
  - labs/python-terraform-wrapper
projects: []
interview: interview/python
certifications:
  - HashiCorp Terraform Associate
tags:
  - python
  - terraform
  - cdktf
  - iac
author: Shaik Basha
last_updated: "2026-07-31"
comments: false
---


# Infrastructure Automation — Terraform

## Overview

Wrap `terraform`/`tofu` CLI safely from Python for `fmt`, `validate`, and `plan` summaries, inspect state cautiously, and know when CDK for Terraform (cdktf) fits.

Python rarely replaces HCL — it **orchestrates** Terraform in CI: run checks, parse plan JSON, fail pipelines, and report. Never auto-`apply` from a tutorial cron.

Complete [Kubernetes Python Client](kubernetes-python-client-automation.md) first. Diagrams use Excalidraw only.

This is a core tutorial in **Module 19 · Infrastructure** of the REBASH Academy **Python for Cloud & DevOps Engineers** series — written for Cloud, DevOps, Platform, and SRE engineers.

## Prerequisites

### Required

- [Linux Automation — subprocess](linux-automation-subprocess-and-psutil.md)  
- Optional: `terraform` or `tofu` on `PATH`

## Learning Objectives

By the end of this tutorial, you will be able to:

- [ ] Run fmt/validate/plan via subprocess with timeouts  
- [ ] Capture plan JSON for reporting  
- [ ] Explain state inspection risks  
- [ ] Summarise cdktf’s role vs HCL  
- [ ] Default to no apply

## Architecture

This topic’s control points and relationships are shown below.

![Terraform automation](../assets/excalidraw/python-terraform-automation.svg)

## Theory

### What it is

Infrastructure as Code (IaC) with Terraform is usually authored in HashiCorp Configuration Language (HCL). Python’s role in this course is **orchestration around the CLI**: format, validate, plan, parse machine-readable plan JSON, and gate Continuous Integration (CI) on policy — not reinventing providers. Optionally, **CDK for Terraform (CDKTF)** lets teams define stacks in Python that synthesise to Terraform JSON when language reuse matters.

### Why it matters

Click-ops drift and unreviewed `apply` cause outages. Wrapping Terraform in Python (or any language) standardises timeouts, exit codes, artefact upload of `tfplan`, and checks such as “no unexpected destroys.” Platform teams build these wrappers once so every pipeline behaves the same. Understanding the boundary — HCL owns resources; Python owns process and policy — keeps both layers honest.

### How it works

Prefer a fixed sequence: `terraform fmt -check`, `validate`, `plan -out=tfplan`, then `terraform show -json tfplan` for analysis. Invoke with `subprocess.run([...], timeout=..., capture_output=True, text=True)` — never `shell=True` with interpolated paths. CI parses the JSON for create/update/delete counts and fails when policy forbids deletes. State backends hold secrets and real inventory: protect them; never commit `terraform.tfstate`. `state list` / `state show` are read-sensitive operations.

```bash
terraform fmt -check -recursive
terraform validate
terraform plan -out=tfplan
terraform show -json tfplan
```

### Key concepts and comparisons

| Approach | Role |
|----------|------|
| HCL + CLI wrappers | Default for most ops teams |
| CDKTF (Python/TS) | Synthesise Terraform; language reuse |
| Pure cloud SDKs | Bypass Terraform — different trade-offs |

| Command | Tutorial default |
|---------|------------------|
| fmt / validate / plan | Allowed |
| apply / destroy | Require `--apply` + extra guard |

### Common pitfalls

- Running apply from a laptop against shared state without a lock or ticket.  
- Parsing human `plan` text instead of `-json`.  
- Committing state or provider credentials.  
- Skipping `timeout=` so stuck providers hang CI forever.  
- Treating CDKTF as “no need to understand Terraform state” — state still exists.

## Hands-on Lab

**Focus:** practise the core workflow for Infrastructure Automation — Terraform

```bash
mkdir -p ~/rebash-python/module-19
cd ~/rebash-python/module-19

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip

command -v terraform || command -v tofu || echo "CLI optional — fixture path available"
```

### Step 1 – Mini module + wrapper

```bash
cd ~/rebash-python/module-19
source .venv/bin/activate

mkdir -p tf
cat > tf/main.tf << 'EOF'
terraform {
  required_version = ">= 1.5.0"
}

output "greeting" {
  value = "rebash-module-19"
}
EOF

cat > tf_wrap.py << 'EOF'
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def terraform_bin() -> str:
    for name in ("terraform", "tofu"):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError("terraform/tofu not found on PATH")


def run(bin_: str, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [bin_, *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=120,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Terraform wrapper")
    p.add_argument("--chdir", type=Path, default=Path("tf"))
    p.add_argument("--apply", action="store_true", help="forbidden in tutorial path")
    p.add_argument("--fixture-plan", type=Path, help="skip CLI; read plan JSON")
    args = p.parse_args()
    if args.apply:
        print("error: --apply disabled in this tutorial", file=sys.stderr)
        return 2
    if args.fixture_plan:
        data = json.loads(args.fixture_plan.read_text(encoding="utf-8"))
        print(json.dumps({"resource_changes": len(data.get("resource_changes", []))}))
        return 0
    try:
        bin_ = terraform_bin()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("hint: use --fixture-plan fixtures/plan.json", file=sys.stderr)
        return 1
    init = run(bin_, ["init", "-backend=false", "-input=false"], args.chdir)
    if init.returncode != 0:
        sys.stderr.write(init.stderr)
        return init.returncode
    val = run(bin_, ["validate", "-json"], args.chdir)
    sys.stdout.write(val.stdout or "")
    if val.returncode != 0:
        sys.stderr.write(val.stderr)
    return val.returncode


if __name__ == "__main__":
    raise SystemExit(main())
EOF

mkdir -p fixtures
cat > fixtures/plan.json << 'EOF'
{
  "resource_changes": [
    {"address": "null_resource.a", "change": {"actions": ["create"]}}
  ]
}
EOF

python tf_wrap.py --fixture-plan fixtures/plan.json
```

### Step 2 – Live validate (optional)

```bash
python tf_wrap.py --chdir tf || echo "install terraform/tofu to run live validate"
```

### Step 3 – Policy sketch

Write: fail CI if plan contains `delete` on production workspaces unless change ticket present.

## Validation

- [ ] Lab commands run under `~/rebash-python/module-19/`
- [ ] You can explain each Theory section in your own words
- [ ] You used modern tooling where it applies to this topic
- [ ] You can describe one production failure mode for this topic

## Code Walkthrough

Production practice for **Infrastructure Automation — Terraform** always combines:

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

!!! warning "Running apply from a laptop against shared state without a lock or ticket.  "
    Validate assumptions against the Theory section and official docs before changing production.

!!! warning "Parsing human `plan` text instead of `-json`.  "
    Lab shortcuts (open security groups, admin roles, skip approvals) must not ship unchanged.

!!! warning "Changing production without a rollback path"
    Always know how to revert (previous artefact, prior release, state rollback, DNS failback).

## Best Practices

- Encode Infrastructure Automation — Terraform changes as code and review them in pull requests
- Pin versions (images, modules, actions, provider plugins)
- Separate environments with clear promotion gates
- Alert on symptoms with runbooks attached
- Destroy lab resources; tag everything with owner and expiry where possible

## Troubleshooting

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| Provider download fails | Network in CI | Cache plugins; `-backend=false` for validate-only |
| State locked | Concurrent apply | Don’t apply from wrappers casually |
| Wrong binary | tofu vs terraform | Detect both |

## Summary

- Python orchestrates Terraform CLI; HCL stays source of truth  
- fmt/validate/plan in CI; apply is gated  
- cdktf is an alternative authoring path  
- Lab: [Terraform Wrapper](../labs/python-terraform-wrapper.md)

## Interview Questions

1. How does **Infrastructure Automation — Terraform** show up when operating Cloud or production platforms?
2. What would you check first if this area misbehaves in production?
3. Which modern tools or APIs replace older equivalents here?
4. What security control should accompany this capability?
5. How would you automate verification of this topic in CI?

!!! tip "Sample answer — question 2"
    Start with blast radius and recent changes, gather evidence (logs, status, plan/diff), then fix forward with a known rollback path — not guesswork.

## Related Tutorials

- [Course overview](index.md)
- - [SSH Automation — Paramiko and Fabric](ssh-automation-paramiko-and-fabric.md)  
- [Terraform Wrapper lab](../labs/python-terraform-wrapper.md)

## References

- [Terraform CLI](https://developer.hashicorp.com/terraform/cli)  
- [CDK for Terraform](https://developer.hashicorp.com/terraform/cdktf)
