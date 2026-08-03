---
title: "Lab — Python Terraform Wrapper"
description: "Wrap terraform fmt/validate/plan with a Python CLI using fixtures for plan JSON when Terraform CLI or cloud creds are unavailable."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - terraform
  - subprocess
  - iac
comments: false
---

# Lab — Python Terraform Wrapper

## Lab Overview

**Purpose:** Orchestrate Terraform CLI safely from Python with dry summary output.

**Scenario:** Platform wants a consistent `tfwrap check` for CI: fmt check, validate, and plan summary — without applying.

**Expected outcome:** CLI runs subprocess calls with list args; `--fixture` summarises a saved plan JSON offline.

!!! tip "This is a lab, not a tutorial"
    Apply [Infrastructure Automation — Terraform](../python/infrastructure-automation-terraform.md) and [Linux Automation — subprocess](../python/linux-automation-subprocess-and-psutil.md).

## Business Scenario

Teams paste raw plan logs into Slack. You need a short resource-change summary for PR comments.

## Learning Objectives

- [ ] Invoke `terraform` via `subprocess.run` (no `shell=True`)
- [ ] Parse `terraform show -json` or fixture plan
- [ ] Never run `apply` in this lab
- [ ] Exit non-zero on fmt/validate failure

## Prerequisites

### Knowledge

- [Infrastructure Automation — Terraform](../python/infrastructure-automation-terraform.md)
- [Linux Automation — subprocess and psutil](../python/linux-automation-subprocess-and-psutil.md)

### Software

| Tool | Notes |
|------|--------|
| Terraform CLI | optional |
| Fixture plan JSON | required offline path |

**Estimated cost:** £0 (no cloud apply).

## Environment

```bash
mkdir -p ~/rebash-lab-python-tf/{fixtures,out}
cd ~/rebash-lab-python-tf
python3 -m venv .venv && source .venv/bin/activate
```

## Initial State — fixture plan
Create `fixtures/plan.json`:

```json
{
  "resource_changes": [
    {"address": "aws_instance.web", "change": {"actions": ["update"]}},
    {"address": "aws_s3_bucket.logs", "change": {"actions": ["create"]}},
    {"address": "aws_security_group.old", "change": {"actions": ["delete"]}}
  ]
}
```

## Task

Create `tfwrap.py`:

- `summary --fixture fixtures/plan.json` → counts create/update/delete → `out/summary.json`
- Optional live: `check` runs `terraform fmt -check` and `terraform validate` if binary exists; otherwise print skip reason

## Validation

```bash
python tfwrap.py summary --fixture fixtures/plan.json
python -c 'import json; print(json.load(open("out/summary.json")))'
```

- [ ] Fixture summary: create 1, update 1, delete 1
- [ ] No `terraform apply` anywhere in the script
- [ ] Missing terraform binary does not crash fixture mode

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `FileNotFoundError: terraform` | Use fixture mode; document optional install |
| Huge plan JSON | Stream or only count `resource_changes` |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-tf
```

## Production Discussion

Use remote state backends and policy-as-code (OPA/Sentinel). Python wrappers should never hide plan approval gates.

## Related

- Next: [AWS EC2 Inventory](python-aws-ec2-inventory.md)
- Project: [Cloud Operations Toolkit](../projects/python-cloud-operations-toolkit.md)
