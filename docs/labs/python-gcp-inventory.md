---
title: "Lab — Python GCP Inventory"
description: "Inventory GCP Compute Engine instances from fixtures or optional google-cloud libraries — dry-run friendly without credentials."
difficulty: intermediate
estimated_time: "50–60 min"
category: labs
author: Shaik Basha
last_updated: "2026-07-29"
tags:
  - labs
  - python
  - gcp
  - inventory
comments: false
---

# Lab — Python GCP Inventory

## Lab Overview

**Purpose:** Produce a GCE instance inventory (name, zone, status, labels).

**Scenario:** Learners may lack GCP projects; fixtures keep the lab runnable everywhere.

**Expected outcome:** `--fixture` path always works; live path optional with Application Default Credentials.

!!! tip "This is a lab, not a tutorial"
    Apply [Cloud Automation — AWS, Azure, GCP](../python/cloud-automation-aws-azure-gcp.md).

## Business Scenario

A multi-project landing zone needs a weekly inventory of running VMs missing `owner` labels.

## Learning Objectives

- [ ] Flatten instance records to a common schema
- [ ] Flag missing required labels
- [ ] Fixture-first; graceful live failures

## Prerequisites

### Knowledge

- [Cloud Automation — AWS, Azure, GCP](../python/cloud-automation-aws-azure-gcp.md)

### Software

Fixtures required; `google-cloud-compute` optional. **Estimated cost:** £0.

## Architecture

![Cloud inventory fixture and dry-run path](../assets/images/lab-python-cloud-inventory.svg)

## Environment

```bash
mkdir -p ~/rebash-lab-python-gcp/{fixtures,out}
cd ~/rebash-lab-python-gcp
python3 -m venv .venv && source .venv/bin/activate
```

## Initial State

```bash
cat > fixtures/instances.json << 'EOF'
[
  {"name": "api-1", "zone": "europe-west2-a", "status": "RUNNING", "labels": {"owner": "platform"}},
  {"name": "scratch", "zone": "europe-west2-b", "status": "TERMINATED", "labels": {}}
]
EOF
```

## Task

`gcp_inventory.py --fixture fixtures/instances.json` → `out/inventory.json` plus `out/missing_labels.json` for instances lacking `owner`.

## Validation

```bash
python gcp_inventory.py --fixture fixtures/instances.json
python -c 'import json; assert len(json.load(open("out/missing_labels.json")))==1'
```

- [ ] Fixture works offline
- [ ] Missing label detection works
- [ ] No service account JSON committed

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| ADC errors | Expected without GCP — use fixtures |

## Cleanup

```bash
deactivate 2>/dev/null || true
rm -rf ~/rebash-lab-python-gcp
```

## Production Discussion

Use workload identity federation for CI; prefer Cloud Asset Inventory for organisation-scale queries.

## Related

- Next: [Certificate Expiry Monitor](python-certificate-expiry-monitor.md)
