---
title: "Lab — Python AWS EC2 Inventory"
description: "Build an EC2 inventory CLI with boto3 — fixture/dry-run mode works without AWS credentials."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - aws
  - boto3
  - inventory
comments: false
---

# Lab — Python AWS EC2 Inventory

## Lab Overview

**Purpose:** Produce a normalised EC2 instance inventory (id, type, state, tags) for cost and compliance reviews.

**Scenario:** FinOps needs a weekly CSV/JSON of running instances tagged `Environment`. Credentials may be unavailable on learner laptops.

**Expected outcome:** CLI with `--fixture` (required offline path) and optional live boto3 describe.

!!! tip "This is a lab, not a tutorial"
    Apply [Cloud Automation — AWS, Azure, GCP](../python/cloud-automation-aws-azure-gcp.md).

## Business Scenario

Accounts sprawled across regions. Spreadsheet exports from the console are stale; you need a repeatable inventory script.

## Learning Objectives

- [ ] Structure inventory records consistently
- [ ] Use fixture JSON when credentials are absent
- [ ] Optional boto3 `describe_instances` with explicit region
- [ ] Never hard-code access keys

## Prerequisites

### Knowledge

- [Cloud Automation — AWS, Azure, GCP](../python/cloud-automation-aws-azure-gcp.md)
- [Configuration Management and Secrets](../python/configuration-management-and-secrets.md)

### Software

| Tool | Notes |
|------|--------|
| boto3 | optional live |
| Fixtures | required |

**Estimated cost:** £0 with fixtures (live: read-only IAM, no creates).

## Architecture

![Cloud inventory fixture and dry-run path](../assets/images/lab-python-cloud-inventory.svg)

## Environment

``` {.bash .ra-terminal title="Terminal"}
mkdir -p ~/rebash-lab-python-aws/{fixtures,out}
cd ~/rebash-lab-python-aws
python3 -m venv .venv && source .venv/bin/activate
pip install 'boto3>=1.34,<2'
```

## Initial State — fixture
Create `fixtures/ec2.json`:

```json title="ec2.json"
{
  "Reservations": [{
    "Instances": [
      {"InstanceId": "i-aaa", "InstanceType": "t3.medium", "State": {"Name": "running"},
       "Tags": [{"Key": "Name", "Value": "api"}, {"Key": "Environment", "Value": "prod"}]},
      {"InstanceId": "i-bbb", "InstanceType": "t3.large", "State": {"Name": "stopped"},
       "Tags": [{"Key": "Name", "Value": "batch"}]}
    ]
  }]
}
```

## Task

Create `ec2_inventory.py`:

- `--fixture fixtures/ec2.json` flattens instances to rows
- Optional `--region eu-west-2` live path using default credential chain; on `NoCredentialsError`, exit `2` with message to use `--fixture`
- Write `out/inventory.json` and optional CSV

## Validation

``` {.bash .ra-terminal title="Terminal"}
python ec2_inventory.py --fixture fixtures/ec2.json
python -c 'import json; d=json.load(open("out/inventory.json")); assert len(d)==2'
```

- [ ] Fixture mode needs no AWS credentials
- [ ] Running and stopped instances both listed
- [ ] No access keys in source or logs

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `NoCredentialsError` | Expected without keys — use `--fixture` |
| Wrong region | Pass `--region` explicitly |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-aws
# Unset AWS_* if you exported temporary keys for optional live mode
```

## Production Discussion

Use IAM roles (IRSA/instance profiles), organisation-wide Config aggregators for multi-account, and never embed long-lived keys in CI.

## Related

- Next: [Azure Resource Inventory](python-azure-resource-inventory.md)
- Project: [Cloud Operations Toolkit](../projects/python-cloud-operations-toolkit.md)
